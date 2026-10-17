//! Bounded po17/N512 aggregate execution retained for later proving; no proof command.
//! Capsules, segment files and diagnostics never confer mathematical authority.
//! Link dmkn_aggregate_relation to the exact selected aggregate source library.
#[path = "../aggregate/receipt.rs"] mod receipt;

use std::{collections::{BTreeMap, BTreeSet}, env, fs, sync::{Arc, Mutex},
    io::{Read, Write}, path::{Component, Path, PathBuf}, time::Instant};
use anyhow::{Context, Result, ensure};
use bincode::Options;
use dmkn_aggregate_relation::{header::{self, Header}, relation};
use dmkn_module_relation::canonical;
use risc0_zkvm::{compute_image_id, AssumptionReceipt, CoprocessorCallback, ProveKeccakRequest, ExecutorEnv, ExecutorImpl,
    ExitCode, InnerAssumptionReceipt, InnerReceipt, Receipt, ReceiptClaim,
    Segment, SegmentRef, TraceEvent, VerifierContext,
    sha::{self, Digest, Digestible, Sha256}};
use serde::{Serialize, Deserialize};
use serde_json::{json, Value};

const FILE_LIMIT: u64 = 64 * 1024 * 1024;
const WIRE_LIMIT: u64 = 16 * 1024 * 1024;
const READ_LIMIT: u64 = 512 * 1024 * 1024;
const DIAGNOSTIC_LIMIT: u64 = 8 * 1024 * 1024;
const SEGMENT_LIMIT: usize = 512;
const CAPSULE_LIMIT: u64 = 96 * 1024 * 1024;
const PARENT_LIMIT: u64 = 1024 * 1024;
const ARTIFACT_LIMIT: u64 = 512 * 1024;
const SAMPLE_STRIDE: u64 = 256;
const SAMPLE_CELLS: usize = 131_072;
const SNAPSHOT_MAGIC: [u8; 8] = *b"DMKNAS01";
const SNAPSHOT_VERSION: u32 = 1;

/// The pinned SDK's pending_keccaks field is private. Its sole enqueue path
/// instead calls this installed public callback, which rejects every request.
/// No pending coprocessor work can be silently omitted from a saved capsule.
struct RejectCoprocessors;
impl CoprocessorCallback for RejectCoprocessors {
    fn prove_keccak(&mut self, _request: ProveKeccakRequest) -> Result<()> {
        anyhow::bail!("unsupported Keccak coprocessor request")
    }
}

#[derive(Serialize, Deserialize)]
struct AggregateSnapshot {
    magic: [u8; 8],
    version: u32,
    session_binding: Digest,
    session_claim: ReceiptClaim,
    assumption_order: Vec<Digest>,
    segments: Vec<Segment>,
}

fn checked<T>(value: canonical::R<T>) -> Result<T> { value.map_err(anyhow::Error::msg) }
fn hash(raw: &[u8]) -> Digest { *sha::Impl::hash_bytes(raw) }
fn sha_hex(raw: &[u8]) -> String { canonical::hex(&canonical::sha(raw)) }

fn ordinary_path(path: &Path, fresh: bool) -> Result<()> {
    ensure!(path.is_absolute() && !path.components().any(|part|
        matches!(part, Component::ParentDir | Component::CurDir)), "absolute normalized path");
    if fresh {
        match fs::symlink_metadata(path) {
            Err(error) if error.kind() == std::io::ErrorKind::NotFound => {},
            _ => anyhow::bail!("fresh output path required"),
        }
    }
    let first = if fresh { path.parent().context("output parent")? } else { path };
    for ancestor in first.ancestors() {
        let metadata = fs::symlink_metadata(ancestor)?;
        ensure!(!metadata.file_type().is_symlink(), "no symlink paths");
        #[cfg(windows)] {
            use std::os::windows::fs::MetadataExt;
            ensure!(metadata.file_attributes() & 0x400 == 0, "no reparse paths");
        }
        if ancestor != path || fresh { ensure!(metadata.is_dir(), "ordinary path parent"); }
    }
    Ok(())
}

fn read_bounded(path: &Path, limit: u64) -> Result<Vec<u8>> {
    ordinary_path(path, false)?;
    let file = fs::File::open(path)?;
    let metadata = file.metadata()?;
    ensure!(metadata.is_file() && metadata.len() > 0 && metadata.len() <= limit,
        "bounded nonempty ordinary input");
    let mut raw = Vec::new();
    (&file).take(metadata.len()).read_to_end(&mut raw)?;
    ensure!(raw.len() as u64 == metadata.len() && file.metadata()?.len() == metadata.len(),
        "input changed extent during bounded read");
    Ok(raw)
}

fn read_charged(path: &Path, maximum: u64, total: &Mutex<u64>) -> Result<Vec<u8>> {
    let mut held = total.lock().map_err(|_| anyhow::anyhow!("read budget lock poisoned"))?;
    let remaining = READ_LIMIT.checked_sub(*held).context("read budget exhausted")?;
    ordinary_path(path, false)?;
    let metadata = fs::metadata(path)?;
    let reserved = metadata.len();
    ensure!(metadata.is_file() && reserved > 0 && reserved <= maximum.min(remaining),
        "bounded read reservation");
    let next = held.checked_add(reserved).context("read byte overflow")?;
    ensure!(next <= READ_LIMIT, "aggregate input read budget");
    // Reserve before I/O and never refund a partial/failed read. The repeated
    // metadata/ordinary checks are intentional, not a filesystem-immutability claim.
    *held = next;
    let raw = read_bounded(path, reserved)?;
    ensure!(raw.len() as u64 == reserved, "reserved input extent changed");
    Ok(raw)
}

fn write_new(path: &Path, raw: &[u8], limit: u64) -> Result<()> {
    ensure!(!raw.is_empty() && raw.len() as u64 <= limit, "output byte bound");
    ordinary_path(path, true)?;
    let mut file = fs::OpenOptions::new().write(true).create_new(true).open(path)?;
    file.write_all(raw)?; file.sync_all()?;
    Ok(())
}

fn encode<T: Serialize>(value: &T) -> Result<Vec<u8>> {
    Ok(bincode::DefaultOptions::new().with_fixint_encoding()
        .with_limit(FILE_LIMIT).serialize(value)?)
}

fn encode_capsule(value: &AggregateSnapshot) -> Result<Vec<u8>> {
    Ok(bincode::DefaultOptions::new().with_fixint_encoding()
        .with_limit(CAPSULE_LIMIT).serialize(value)?)
}

fn adopted_image(text: &str) -> Result<([u32; 8], Digest)> {
    let bytes = checked(canonical::unhex(text))?;
    ensure!(text.len() == 64 && text == canonical::hex(&bytes), "lowercase adopted image");
    let words = header::image_words(bytes);
    checked(header::distinct_aggregate_image(words))?;
    Ok((words, Digest::from(words)))
}

fn phase(phases: &mut Vec<Value>, name: &str, started: Instant) {
    phases.push(json!({"phase":name,"elapsed_ms":started.elapsed().as_millis()}));
}

/// Ordinary immutable segment bytes, never a proof or trusted acceptance cache.
struct StoredSegment { path: PathBuf, bytes: u64, hash: Digest, read_total: Arc<Mutex<u64>> }
impl SegmentRef for StoredSegment {
    fn resolve(&self) -> Result<Segment> {
        let raw = read_charged(&self.path, FILE_LIMIT, &self.read_total)?;
        ensure!(raw.len() as u64 == self.bytes && hash(&raw) == self.hash,
            "retained exact execution segment");
        Ok(bincode::DefaultOptions::new().with_fixint_encoding().with_limit(FILE_LIMIT)
            .reject_trailing_bytes().deserialize(&raw)?)
    }
}

/// Same SDK callback used by run(), with explicit create-new bounded custody.
/// On error these partial files remain diagnostic data, not resumable execution.
struct SegmentStore { directory: PathBuf, bytes: u64, rows: Vec<Value>, po2: u32,
    read_total: Arc<Mutex<u64>> }
impl SegmentStore {
    fn retain(&mut self, segment: Segment) -> Result<Box<dyn SegmentRef>> {
        ensure!(self.rows.len() < SEGMENT_LIMIT && segment.index as usize == self.rows.len()
            && segment.po2() <= self.po2 as usize, "consecutive bounded execution segments");
        let info = segment.get_info();
        let raw = encode(&segment)?;
        let next = self.bytes.checked_add(raw.len() as u64).context("segment byte overflow")?;
        ensure!(next <= CAPSULE_LIMIT, "aggregate retained-segment byte bound");
        let path = self.directory.join(format!("{}.segment", segment.index));
        write_new(&path, &raw, FILE_LIMIT)?;
        self.bytes = next;
        self.rows.push(json!({"index":segment.index,"po2":info.po2,
            "rows":info.row_count,"padding_rows":info.padding_row_count,
            "instructions":info.insn_count,"bytes":raw.len(),"sha256":sha_hex(&raw)}));
        Ok(Box::new(StoredSegment { path, bytes:raw.len() as u64, hash:hash(&raw),
            read_total:Arc::clone(&self.read_total) }))
    }
}

#[derive(Default)]
struct Samples {
    instructions: u64, sampled: u64, omitted: u64, backwards: u64,
    maximum_cycle: u64, last_cycle: Option<u64>, saturated: bool,
    cells: BTreeMap<(u64, u32), u64>,
}
impl Samples {
    fn observe(&mut self, event: TraceEvent) {
        if let TraceEvent::InstructionStart { cycle, pc, .. } = event {
            self.instructions = self.instructions.saturating_add(1);
            if self.last_cycle.is_some_and(|previous| cycle < previous) {
                self.backwards = self.backwards.saturating_add(1);
            }
            self.last_cycle = Some(cycle); self.maximum_cycle = self.maximum_cycle.max(cycle);
            if (self.instructions - 1) % SAMPLE_STRIDE == 0 {
                let key = (cycle >> 20, pc);
                if self.cells.len() == SAMPLE_CELLS && !self.cells.contains_key(&key) {
                    self.saturated = true; self.omitted = self.omitted.saturating_add(1);
                } else {
                    let count = self.cells.entry(key).or_default();
                    *count = count.saturating_add(1);
                    self.sampled = self.sampled.saturating_add(1);
                }
            }
        }
    }
    fn report(&self, enabled: bool) -> Value {
        json!({"enabled":enabled,"measurement":"DETERMINISTIC_INSTRUCTION_SAMPLES_NOT_PROOF_CYCLE_ATTRIBUTION",
            "stride":SAMPLE_STRIDE,"cell_limit":SAMPLE_CELLS,"saturated":self.saturated,
            "instructions_observed":self.instructions,"samples_stored":self.sampled,
            "samples_omitted":self.omitted,"maximum_reported_cycle":self.maximum_cycle,
            "backwards_cycle_events":self.backwards,"cycle_window":1u64<<20,
            "samples":self.cells.iter().map(|((window,pc),count)|json!([window,pc,count])).collect::<Vec<_>>()})
    }
}

fn assumption_order(parents: &[Receipt], actual: &[(risc0_zkvm::Assumption, AssumptionReceipt)],
                    context: &VerifierContext) -> Result<Vec<Digest>> {
    ensure!(parents.len() <= relation::MAX_ASSUMPTIONS && actual.len() == parents.len(),
        "exact actual assumption count");
    let mut expected = BTreeMap::new();
    for parent in parents {
        let InnerReceipt::Succinct(value) = &parent.inner else { anyhow::bail!("non-succinct boundary"); };
        ensure!(value.hashfn == "poseidon2", "boundary hash suite");
        value.verify_integrity_with_context(context)?;
        let digest = value.claim.digest();
        ensure!(expected.insert(digest.as_bytes().to_vec(), ()).is_none(), "duplicate verified boundary claim");
    }
    let mut order = Vec::new();
    for (claim, actual) in actual {
        let AssumptionReceipt::Proven(InnerAssumptionReceipt::Succinct(value)) = actual else {
            anyhow::bail!("only proven succinct actual assumptions");
        };
        ensure!(value.hashfn == "poseidon2", "actual assumption hash suite");
        value.verify_integrity_with_context(context)?;
        let digest = value.claim.digest();
        ensure!(claim.claim == digest && claim.control_root == Digest::ZERO
            && expected.remove(digest.as_bytes()).is_some(),
            "actual assumption outside exact preverified boundary set");
        order.push(digest);
    }
    ensure!(expected.is_empty(), "unused verified boundary claim");
    Ok(order)
}

fn snapshot(args: &[String]) -> Result<()> {
    ensure!(args.len() >= 12, "snapshot ADOPTED_A ELF WIRE EXPECTED_HEADER CYCLES PO2 MODE FRESH_CAPSULE FRESH_DIAGNOSTIC RECEIPT_COUNT [RECEIPTS...]");
    let started = Instant::now(); let mut phases = Vec::new();
    let (words, adopted) = adopted_image(&args[2])?;
    let cycles:u64 = args[6].parse()?; let po2:u32 = args[7].parse()?;
    ensure!((1..=(1u64<<26)).contains(&cycles) && po2 == 17, "selected po17 finite session bounds");
    ensure!(matches!(args[8].as_str(), "stats"|"pc-samples"), "explicit diagnostics mode");
    let sampling = args[8] == "pc-samples";
    let capsule = Path::new(&args[9]); let diagnostic = Path::new(&args[10]);
    let segments_path = PathBuf::from(format!("{}.segments", &args[9]));
    ordinary_path(capsule, true)?; ordinary_path(diagnostic, true)?;
    ordinary_path(&segments_path, true)?;
    ensure!(capsule != diagnostic && diagnostic != segments_path, "distinct fresh output paths");
    let count:usize = args[11].parse()?;
    ensure!(count <= relation::MAX_ASSUMPTIONS && args.len() == 12+count, "exact receipt argument count");
    let preflight = Instant::now();
    let total_read = Arc::new(Mutex::new(0u64));
    let elf = read_charged(Path::new(&args[3]), FILE_LIMIT, &total_read)?;
    ensure!(compute_image_id(&elf)? == adopted, "actual ELF differs from adopted aggregate A");
    let wire = read_charged(Path::new(&args[4]), WIRE_LIMIT, &total_read)?;
    let expected = read_charged(Path::new(&args[5]), header::BYTES as u64, &total_read)?;
    let header = checked(Header::decode(&expected))?; checked(header.bind_image(words))?;
    let conditional = checked(relation::check_bytes(&wire))?;
    ensure!(checked(conditional.header().encode())? == expected && conditional.assumptions().len() == count,
        "exact derived aggregate header and pending count");
    phase(&mut phases,"bounded_read_and_native_preflight",preflight);
    let verify_started = Instant::now();
    let mut parents = Vec::new(); let mut parent_hashes = Vec::new();
    let mut exact_claims = BTreeSet::new(); let mut parent_rows = Vec::new();
    for (path, pending) in args[12..].iter().zip(conditional.assumptions()) {
        ensure!(exact_claims.insert((pending.image(), pending.journal().to_vec())), "unique exact pending claims");
        let raw = read_charged(Path::new(path), PARENT_LIMIT, &total_read)?;
        let verified = receipt::verify_pending(&raw, pending, words)?;
        ensure!(verified.image() == pending.image(), "verified typed boundary image");
        parent_rows.push(json!({"path":path,"bytes":raw.len(),"sha256":sha_hex(&raw),
            "image":canonical::hex(&header::image_bytes(pending.image())),
            "journal_sha256":sha_hex(pending.journal())}));
        parent_hashes.push(hash(&raw)); parents.push(verified.receipt().clone());
    }
    phase(&mut phases,"genuine_boundary_receipt_verification",verify_started);
    let session_binding = hash(&encode(&("DMKN-AGGREGATE-SESSION-V1",hash(&elf),adopted,
        header.relation_image,header.foundation,header.policy,hash(&wire),hash(&expected),cycles,po2,&parent_hashes))?);
    let expected_claim = ReceiptClaim::ok(adopted, expected.clone());
    let context = VerifierContext::default().with_dev_mode(false);
    fs::create_dir(&segments_path)?;
    let mut store = SegmentStore {directory:segments_path.clone(),bytes:0,rows:Vec::new(),po2,
        read_total:Arc::clone(&total_read)};
    let mut samples = Samples::default(); let mut guest_calls = 0u32;
    let execution_started = Instant::now();
    let execution = (|| -> Result<_> {
        let mut builder = ExecutorEnv::builder();
        builder.write_slice(&wire).session_limit(Some(cycles)).segment_limit_po2(po2);
        builder.coprocessor_callback(RejectCoprocessors);
        for parent in &parents { builder.add_assumption(parent.clone())?; }
        if sampling { builder.trace_callback(|event| {samples.observe(event); Ok(())}); }
        let mut executor = ExecutorImpl::from_elf(builder.build()?, &elf)?;
        guest_calls += 1;
        executor.run_with_callback(|segment| store.retain(segment))
    })();
    phase(&mut phases,"guest_execution_and_bounded_segment_custody",execution_started);
    let mut session_stats = Value::Null;
    let outcome = (|| -> Result<Value> {
        let session = execution?;
        session_stats = json!({"row_count":session.row_count,"padding_row_count":session.padding_row_count,
            "instruction_count":session.insn_count,"segment_count":session.segments.len()});
        let collect_started = Instant::now();
        ensure!(session.exit_code == ExitCode::Halted(0)
            && session.journal.as_ref().context("missing aggregate journal")?.bytes == expected,
            "exact successful aggregate guest conclusion");
        ensure!(session.mmr_assumptions.is_empty() && session.work().is_none(),"unsupported MMR/PoVW");
        let session_claim = session.claim()?;
        ensure!(session_claim.digest() == expected_claim.digest(),"exact fully resolved session claim");
        let order = assumption_order(&parents, &session.assumptions, &context)?;
        let segments = session.segments().collect::<Result<Vec<_>>>()?;
        ensure!(!segments.is_empty() && segments.len() <= SEGMENT_LIMIT && segments.len() == store.rows.len(),
            "exact complete segment census");
        for (index,segment) in segments.iter().enumerate() {
            ensure!(segment.index as usize == index && segment.po2() <= po2 as usize,
                "complete consecutive segment cap");
        }
        phase(&mut phases,"resolved_claim_and_complete_segment_materialization",collect_started);
        let snapshot = AggregateSnapshot {magic:SNAPSHOT_MAGIC,version:SNAPSHOT_VERSION,
            session_binding,session_claim,assumption_order:order,segments};
        let write_started = Instant::now();
        let raw = encode_capsule(&snapshot)?;
        let binding = hash(&encode(&("DMKN-AGGREGATE-SNAPSHOT-V1",session_binding,hash(&raw)))?);
        write_new(capsule,&raw,CAPSULE_LIMIT)?;
        phase(&mut phases,"capsule_encode_and_durable_write",write_started);
        Ok(json!({"schema":"DMKN_GEOMETRY17_AGGREGATE_SNAPSHOT_RESULT_V1",
            "status":"UNTRUSTED_AGGREGATE_EXECUTION_CAPSULE_RETAINED",
            "aggregate_image":args[2],"header":expected,"capsule_path":args[9],
            "capsule_bytes":raw.len(),"capsule_sha256":sha_hex(&raw),
            "capsule_binding":binding.to_string(),"session_binding":session_binding.to_string(),
            "segments":snapshot.segments.len(),"assumptions":snapshot.assumption_order.len(),
            "mathematical_admission":false,"proof_calls":0,"guest_execute_calls":guest_calls}))
    })();
    let error = outcome.as_ref().err().map(|error|format!("{error:#}").chars().take(2000).collect::<String>());
    let report = json!({"schema":"DMKN_GEOMETRY17_AGGREGATE_EXECUTION_DIAGNOSTIC_V1",
        "status":if outcome.is_ok(){"CAPSULE_RETAINED_NOT_CERTIFICATE"}else{"FAILED_NO_ACCEPTED_CAPSULE"},
        "aggregate_image":args[2],"elf_sha256":sha_hex(&elf),"wire_sha256":sha_hex(&wire),
        "wire_bytes":wire.len(),"header":expected,"parents":parent_rows,
        "cycles_cap":cycles,"segment_po2":po2,"segment_directory":segments_path,
        "retained_segment_bytes":store.bytes,"retained_segments":store.rows,
        "input_read_bytes":*total_read.lock().map_err(|_| anyhow::anyhow!("read budget lock poisoned"))?,
        "input_read_accounting":"PRE_READ_RESERVATIONS_WITH_NO_FAILURE_REFUND",
        "session_stats":session_stats,"samples":samples.report(sampling),"phases":phases,
        "elapsed_ms_before_diagnostic_write":started.elapsed().as_millis(),"error":error,
        "result":outcome.as_ref().ok(),"guest_execute_calls":guest_calls,"proof_calls":0,
        "mathematical_admission":false,"accounting":"PHASE_WALL_TIME_NOT_CPU;ENCLOSING_OWNER_CHARGES_ALL_COSTS"});
    write_new(diagnostic, &serde_json::to_vec(&report)?, DIAGNOSTIC_LIMIT)?;
    // Failure remains failure after diagnostics. A finalization error likewise
    // returns failure; any written capsule/segments remain preserved, untrusted.
    println!("{}",outcome?);
    Ok(())
}

fn verify(args: &[String]) -> Result<()> {
    ensure!(args.len() == 5,"verify ADOPTED_A RECEIPT EXPECTED_HEADER");
    let (words,_) = adopted_image(&args[2])?;
    let raw = read_bounded(Path::new(&args[3]),ARTIFACT_LIMIT)?;
    let expected = read_bounded(Path::new(&args[4]),header::BYTES as u64)?;
    let verified = receipt::verify_aggregate(&raw,&expected,words)?;
    ensure!(verified.image() == words,"actual verified aggregate image");
    println!("{}",json!({"schema":"DMKN_AGGREGATE_VERIFY_RESULT_V1",
        "status":"VERIFIED_RESOLVED_AGGREGATE_RECEIPT","aggregate_image":args[2],
        "header":expected,"receipt_sha256":sha_hex(&raw),"receipt_bytes":raw.len()}));
    Ok(())
}

fn main() -> Result<()> {
    ensure!(env::var_os("RISC0_DEV_MODE").is_none(),"dev-mode environment forbidden");
    ensure!(env::var_os("RISC0_PPROF_OUT").is_none(),"ambient profiler output forbidden");
    let args = env::args().collect::<Vec<_>>();
    ensure!(args.len() >= 2,"explicit aggregate snapshot/verify command");
    match args[1].as_str() {
        "snapshot" => snapshot(&args),
        "verify" => verify(&args),
        _ => anyhow::bail!("only aggregate snapshot/verify commands are supported"),
    }
}


