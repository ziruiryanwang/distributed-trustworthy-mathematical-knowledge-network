//! Real v5 module host. Capsules/checkpoints are untrusted proving aids, NEVER admission.
#[path = "../canonical.rs"] mod canonical;
#[path = "../commitments.rs"] mod commitments;
#[path = "../journal.rs"] mod journal;
#[path = "../policy.rs"] mod policy;
#[path = "../trace.rs"] mod trace;

use std::{collections::{BTreeMap, BTreeSet}, env, fs, io::{Read, Write}, path::Path, time::Instant};
use anyhow::{Context, Result, ensure};
use bincode::Options;
use risc0_zkvm::{compute_image_id, AssumptionReceipt, CompositeReceipt, ExecutorEnv,
    ExecutorImpl, ExitCode, InnerAssumptionReceipt, InnerReceipt, ProverOpts, Receipt,
    ReceiptClaim, Segment, SegmentReceipt, SuccinctReceipt, VerifierContext, get_prover_server,
    Executor, LocalProver, sha::{self, Digest, Digestible, Sha256}};
use serde::{Deserialize, Serialize, de::DeserializeOwned};
use serde_json::{json, Value};

const FILE_LIMIT: u64 = 64 * 1024 * 1024;
const INPUT_LIMIT: u64 = canonical::MAX_BYTES as u64 + 4;
const JOURNAL_LIMIT: u64 = journal::BYTES as u64;
const PARENT_LIMIT: usize = 8;
const SEGMENT_LIMIT: usize = 128;
const TOTAL_READ_LIMIT: u64 = 512 * 1024 * 1024;
const SNAPSHOT_SCHEMA: u32 = 3;
const CHECKPOINT_SCHEMA: u32 = 5;

/// One coherent execution; an attacker may replace it only at the cost of
/// changing its bound hash. Even a forged capsule cannot bypass final receipt
/// verification against the independently selected image and exact journal.
#[derive(Serialize, Deserialize)]
struct Snapshot {
    version: u32,
    session_binding: Digest,
    session_claim: ReceiptClaim,
    assumption_order: Vec<Digest>,
    segments: Vec<Segment>,
}
type Checkpoint = (u32, Digest, String, u32, Vec<u8>);
struct BoundInput { child: journal::Journal, parents: Vec<Vec<u8>> }

fn checked<T>(result: canonical::R<T>) -> Result<T> { result.map_err(anyhow::Error::msg) }

fn read_bounded(path: &str, limit: u64) -> Result<Vec<u8>> {
    ensure!(Path::new(path).is_absolute(), "absolute input path required");
    let file = fs::File::open(path)?;
    let metadata = file.metadata()?;
    ensure!(metadata.is_file() && metadata.len() <= limit, "input size/type");
    let mut out = Vec::new();
    file.take(limit + 1).read_to_end(&mut out)?;
    ensure!(out.len() as u64 <= limit, "input grew past limit");
    Ok(out)
}

fn fresh(path: &str) -> Result<()> {
    ensure!(Path::new(path).is_absolute() && !Path::new(path).exists(),
        "fresh absolute output path required");
    Ok(())
}

fn write_new(path: &str, data: &[u8]) -> Result<()> {
    ensure!(data.len() as u64 <= FILE_LIMIT, "output size");
    fresh(path)?;
    let mut file = fs::OpenOptions::new().write(true).create_new(true).open(path)?;
    file.write_all(data)?;
    file.sync_all()?;
    Ok(())
}

fn encode<T: Serialize>(value: &T) -> Result<Vec<u8>> {
    Ok(bincode::DefaultOptions::new().with_fixint_encoding()
        .with_limit(FILE_LIMIT).serialize(value)?)
}

fn decode<T: DeserializeOwned>(bytes: &[u8]) -> Result<T> {
    ensure!(bytes.len() as u64 <= FILE_LIMIT, "encoded object size");
    Ok(bincode::DefaultOptions::new().with_fixint_encoding()
        .with_limit(FILE_LIMIT).reject_trailing_bytes().deserialize(bytes)?)
}

fn hash(bytes: &[u8]) -> Digest { *sha::Impl::hash_bytes(bytes) }

fn image_id(text: &str) -> Result<Digest> {
    ensure!(text.len() == 64 && text.bytes().all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b)),
        "adopted image ID must be 64 lowercase hex digits");
    let mut bytes = [0u8; 32];
    for (i, byte) in bytes.iter_mut().enumerate() {
        *byte = u8::from_str_radix(&text[2*i..2*i+2], 16)?;
    }
    Ok(Digest::from(bytes))
}


fn application(bytes: &[u8], image: Digest) -> Result<journal::Journal> {
    let decoded = checked(journal::Journal::decode(bytes))?;
    let words: [u32; 8] = image.into();
    ensure!(decoded.image == words && decoded.foundation == policy::foundation()
        && decoded.policy == checked(policy::semantic_id())?, "adopted module image/foundation/policy");
    Ok(decoded)
}

fn checked_receipt(receipt: &Receipt, image: Digest) -> Result<journal::Journal> {
    match &receipt.inner {
        InnerReceipt::Succinct(inner) => ensure!(inner.hashfn == "poseidon2", "unsupported hash suite"),
        // Explicitly excludes Fake, Composite and unselected receipt schemes.
        _ => anyhow::bail!("only real succinct Poseidon2 receipts are supported"),
    }
    let context = VerifierContext::default().with_dev_mode(false);
    // Full application verification, NOT integrity-only. Also requires no assumptions.
    receipt.verify_with_context(&context, image)?;
    application(&receipt.journal.bytes, image)
}

fn byte_array(value: &Value) -> Result<Vec<u8>> {
    checked(canonical::array(value))?.iter()
        .map(|item| checked(canonical::uint(item, 255)).map(|n| n as u8)).collect()
}

fn module_input(input: &[u8], image: Digest) -> Result<BoundInput> {
    ensure!(input.len() >= 5 && input.len() as u64 <= INPUT_LIMIT, "module frame bound");
    let length = u32::from_le_bytes(input[..4].try_into().unwrap()) as usize;
    ensure!(length > 0 && length <= canonical::MAX_BYTES && input.len() == length + 4,
        "exact module frame length");
    let value = checked(canonical::parse(&input[4..]))?;
    checked(canonical::fields(&value, &["schema","image","rank","local_spec","rows","parents","bodies"]))?;
    ensure!(value["schema"] == journal::RELATION, "module relation schema");
    let words: [u32; 8] = image.into();
    let input_image: [u32; 8] = serde_json::from_value(value["image"].clone())?;
    ensure!(input_image == words, "witness actual image");
    let foundation = policy::foundation();
    let semantic_policy = checked(policy::semantic_id())?;
    let rows = checked(canonical::array(&value["rows"]))?;
    ensure!(rows.len() >= policy::FOUNDATION_ROWS && rows.len() <= 250_000, "native row count");
    let prefix = Value::Array(rows[..policy::FOUNDATION_ROWS].to_vec());
    ensure!(canonical::sha(&checked(canonical::canonical(&prefix))?)
        == checked(canonical::unhex(policy::FOUNDATION_CANONICAL_SHA256))?
        && checked(canonical::hash("owner-workload-foundation-candidate", &prefix))? == foundation,
        "exact adopted foundation");
    let summary = checked(commitments::summarize(&value["local_spec"], &foundation, &semantic_policy))?;
    let module = checked(canonical::hash("module-spec", &summary))?;
    let raw_parents = checked(canonical::array(&value["parents"]))?;
    ensure!(raw_parents.len() <= PARENT_LIMIT, "operational parent bound");
    ensure!(checked(canonical::array(&value["bodies"]))?.len() <= 16_384, "body count");
    let mut parents = Vec::new();
    let mut modules = BTreeSet::new();
    let mut groups = BTreeSet::new();
    let mut greatest_rank = None::<u64>;
    for parent in raw_parents {
        checked(canonical::fields(parent, &["journal","openings"]))?;
        let raw = byte_array(&parent["journal"])?;
        let parsed = application(&raw, image)?;
        ensure!(parsed.module != module && modules.insert(parsed.module), "distinct parent module");
        greatest_rank = Some(greatest_rank.map_or(parsed.rank, |n| n.max(parsed.rank)));
        let openings = checked(canonical::array(&parent["openings"]))?;
        ensure!(!openings.is_empty() && openings.len() <= 4096, "selected parent groups");
        for opening in openings {
            let (index, _) = checked(commitments::verify_opening(&parsed, opening))?;
            ensure!(groups.insert((parsed.module,index)) && groups.len() <= 4096, "exact parent group census");
        }
        parents.push(raw);
    }
    let rank = checked(canonical::uint(&value["rank"], u64::MAX))?;
    let expected_rank = match greatest_rank { None => 0, Some(n) => n.checked_add(1).context("rank overflow")? };
    ensure!(rank == expected_rank, "strict exact parent rank");
    let child = journal::Journal {
        image:words, foundation, policy:semantic_policy, module,
        group_root:checked(canonical::unhex(checked(canonical::text(&summary["group_root"]))?))?,
        group_count:checked(canonical::uint(&summary["group_count"],4096))? as u32,
        rank,
    };
    checked(child.validate())?;
    Ok(BoundInput { child, parents })
}

fn parent_receipts(paths: &[String], bound: &BoundInput, image: Digest, read_total: &mut u64)
    -> Result<(Vec<Receipt>, Vec<Digest>, usize)> {
    ensure!(paths.len() <= PARENT_LIMIT && paths.len() == bound.parents.len(), "exact supplied parent count");
    let mut selected: BTreeSet<Vec<u8>> = bound.parents.iter().cloned().collect();
    ensure!(selected.len() == bound.parents.len(), "distinct selected parent journals");
    let mut receipts = Vec::new(); let mut hashes = Vec::new(); let mut total = 0usize;
    for path in paths {
        let raw = read_bounded(path, FILE_LIMIT)?;
        *read_total = read_total.checked_add(raw.len() as u64).context("aggregate byte overflow")?;
        ensure!(*read_total <= TOTAL_READ_LIMIT, "aggregate input byte limit");
        let receipt: Receipt = decode(&raw)?;
        let parent = checked_receipt(&receipt, image)?;
        ensure!(parent.rank < bound.child.rank, "parent rank must decrease");
        ensure!(selected.remove(&receipt.journal.bytes), "unselected or duplicate parent receipt");
        total = total.checked_add(raw.len()).context("parent byte overflow")?;
        hashes.push(hash(&raw)); receipts.push(receipt);
    }
    ensure!(selected.is_empty(), "selected parent receipt absent");
    Ok((receipts, hashes, total))
}

fn ordered_assumptions(receipts: &[Receipt], order: &[Digest], context: &VerifierContext)
    -> Result<Vec<InnerAssumptionReceipt>> {
    ensure!(order.len() == receipts.len() && order.len() <= PARENT_LIMIT, "exact assumption order size");
    let mut actual = BTreeMap::new();
    for receipt in receipts {
        let InnerReceipt::Succinct(value) = &receipt.inner else { anyhow::bail!("non-succinct parent"); };
        value.verify_integrity_with_context(context)?;
        ensure!(actual.insert(value.claim.digest().as_bytes().to_vec(),value.clone()).is_none(),
            "duplicate parent claim");
    }
    let mut output = Vec::new();
    for digest in order {
        let value = actual.remove(digest.as_bytes()).context("capsule assumption not exact verified parent")?;
        // The SDK erases only the claim type by retaining its exact digest;
        // all seal, hash-suite and verifier-parameter fields remain unchanged.
        let unknown = value.into_unknown();
        ensure!(unknown.claim.digest() == *digest, "assumption erasure preserved verified claim");
        output.push(InnerAssumptionReceipt::Succinct(unknown));
    }
    ensure!(actual.is_empty(), "missing capsule parent assumption");
    Ok(output)
}

fn prepare(args: &[String]) -> Result<()> {
    ensure!(args.len() == 6, "prepare IMAGE RAW_JSON FRESH_FRAME FRESH_EXPECTED_JOURNAL");
    fresh(&args[4])?; fresh(&args[5])?;
    ensure!(args[4] != args[5], "distinct preparation outputs");
    let image = read_bounded(&args[2], FILE_LIMIT)?;
    let id = compute_image_id(&image)?;
    let raw = read_bounded(&args[3], canonical::MAX_BYTES as u64)?;
    let mut value = checked(canonical::parse(&raw))?;
    checked(canonical::fields(&value, &["schema","image","rank","local_spec","rows","parents","bodies"]))?;
    let words: [u32; 8] = id.into();
    value["image"] = json!(words);
    // Parent journal bytes are NEVER relabeled; they must already use this image.
    let payload = checked(canonical::canonical(&value))?;
    let mut framed = (payload.len() as u32).to_le_bytes().to_vec(); framed.extend_from_slice(&payload);
    let bound = module_input(&framed,id)?;
    let expected = checked(bound.child.encode())?;
    write_new(&args[4],&framed)?; write_new(&args[5],&expected)?;
    println!("{}",json!({"status":"PREPARED_ONLY_NOT_CERTIFIED","image":words,
        "module":canonical::hex(&bound.child.module),"rank":bound.child.rank,
        "mathematical_admission":false}));
    Ok(())
}

fn execute(args: &[String]) -> Result<()> {
    ensure!((7..=7 + PARENT_LIMIT).contains(&args.len()),
        "execute IMAGE INPUT EXPECTED_JOURNAL CYCLES PO2 [REAL_FINAL_PARENTS...]");
    let image = read_bounded(&args[2],FILE_LIMIT)?; let id = compute_image_id(&image)?;
    let input = read_bounded(&args[3],INPUT_LIMIT)?;
    let expected = read_bounded(&args[4],JOURNAL_LIMIT)?;
    let bound = module_input(&input,id)?;
    ensure!(checked(bound.child.encode())? == expected, "derived expected journal");
    let cycles:u64 = args[5].parse()?; let po2:u32 = args[6].parse()?;
    ensure!((1..=(1 << 28)).contains(&cycles) && (12..=20).contains(&po2),"finite cycle/segment selection");
    let mut read_total = (image.len()+input.len()+expected.len()) as u64;
    let (parents,_,parent_bytes) = parent_receipts(&args[7..],&bound,id,&mut read_total)?;
    let mut builder = ExecutorEnv::builder();
    builder.write_slice(&input).session_limit(Some(cycles)).segment_limit_po2(po2);
    for parent in parents { builder.add_assumption(parent)?; }
    let session = LocalProver::new("dmkn-module-execute").execute(builder.build()?,&image)?;
    ensure!(session.exit_code == ExitCode::Halted(0) && session.journal.bytes == expected,
        "exact successful guest conclusion");
    ensure!(!session.segments.is_empty() && session.segments.len() <= SEGMENT_LIMIT,"segment count");
    let padded_rows:u64 = session.segments.iter().map(|s| s.row_count).sum();
    let padding_rows:u64 = session.segments.iter().map(|s| s.padding_row_count).sum();
    let instructions:u64 = session.segments.iter().map(|s| s.insn_count).sum();
    println!("EXECUTED_ONLY_NOT_A_CERTIFICATE image_id={id} rank={} groups={} parent_bytes={parent_bytes} parents={} segments={} rows={} padded_rows={padded_rows} padding_rows={padding_rows} instructions={instructions}",
        bound.child.rank,bound.child.group_count,bound.parents.len(),session.segments.len(),session.rows());
    Ok(())
}

fn progress(kind: &str, index: u32, phase: &str, started: Instant) {
    let mut err = std::io::stderr().lock();
    let _ = writeln!(err, "CHECKPOINT_PROGRESS kind={kind} index={index} phase={phase} elapsed_ms={}",
        started.elapsed().as_millis());
    let _ = err.flush();
}

fn take_segment(cache: &mut BTreeMap<(String, u32), Vec<u8>>, index: u32,
                ctx: &VerifierContext) -> Result<SegmentReceipt> {
    let raw = cache.remove(&("segment".to_owned(), index)).context("required segment checkpoint absent")?;
    let value: SegmentReceipt = decode(&raw)?;
    ensure!(value.index == index && value.hashfn == "poseidon2", "segment kind/index");
    let params = ctx.segment_verifier_parameters.as_ref().context("segment parameters absent")?;
    ensure!(value.verifier_parameters == params.digest(), "exact segment verifier parameters");
    value.verify_integrity_with_context(ctx)?;
    Ok(value)
}

fn take_succinct(cache: &mut BTreeMap<(String, u32), Vec<u8>>, kind: &str, index: u32,
                 ctx: &VerifierContext) -> Result<SuccinctReceipt<ReceiptClaim>> {
    let raw = cache.remove(&(kind.to_owned(), index)).context("required succinct checkpoint absent")?;
    let value: SuccinctReceipt<ReceiptClaim> = decode(&raw)?;
    ensure!(value.hashfn == "poseidon2", "succinct checkpoint hash suite");
    value.verify_integrity_with_context(ctx)?;
    Ok(value)
}

fn prefix_key(last: u32) -> (&'static str, u32) {
    if last == 0 { ("lift", 0) } else { ("join", last) }
}


fn stage(args: &[String]) -> Result<()> {
    ensure!(args.len() >= 11 && args.len() <= 12+PARENT_LIMIT+SEGMENT_LIMIT+1,
        "stage IMAGE INPUT EXPECTED_JOURNAL CYCLES PO2 KIND INDEX FRESH_OUTPUT PARENT_COUNT [PARENTS...] [SNAPSHOT CHECKPOINTS...]");
    let started=Instant::now(); let kind=args[7].as_str(); let index:u32=args[8].parse()?;
    ensure!(matches!(kind,"snapshot"|"segment"|"lift"|"join"|"resolve"|"finish"),"unknown stage");
    fresh(&args[9])?;
    let parent_count:usize=args[10].parse()?;
    ensure!(parent_count<=PARENT_LIMIT && args.len()>=11+parent_count,"parent count");
    let image=read_bounded(&args[2],FILE_LIMIT)?; let id=compute_image_id(&image)?;
    let input=read_bounded(&args[3],INPUT_LIMIT)?;
    let expected=read_bounded(&args[4],JOURNAL_LIMIT)?;
    let bound=module_input(&input,id)?;
    ensure!(checked(bound.child.encode())?==expected,"derived exact expected journal");
    let child=&bound.child;
    let cycles:u64=args[5].parse()?; let po2:u32=args[6].parse()?;
    ensure!((1..=(1<<28)).contains(&cycles)&&(12..=20).contains(&po2),"finite cycle/segment selection");
    let ctx=VerifierContext::default().with_dev_mode(false);
    let opts=ProverOpts::succinct().with_dev_mode(false).with_prove_guest_errors(false);
    let mut read_total=(image.len()+input.len()+expected.len()) as u64;
    let (parents,parent_hashes,_)=parent_receipts(&args[11..11+parent_count],&bound,id,&mut read_total)?;
    let session_binding=hash(&encode(&("DMKN-MODULE-SESSION-V2",hash(&image),id,hash(&input),
        hash(&expected),cycles,po2,&parent_hashes))?);
    let expected_claim=ReceiptClaim::ok(id,expected.clone());
    if kind=="snapshot" {
        ensure!(index==0 && args.len()==11+parent_count,"snapshot takes parents only, index zero");
        let mut builder=ExecutorEnv::builder();
        builder.write_slice(&input).session_limit(Some(cycles)).segment_limit_po2(po2);
        for parent in &parents { builder.add_assumption(parent.clone())?; }
        progress(kind,index,"execute_once",started);
        let session=ExecutorImpl::from_elf(builder.build()?,&image)?.run()?;
        ensure!(session.exit_code==ExitCode::Halted(0)
            && session.journal.as_ref().context("missing journal")?.bytes==expected,"exact successful guest conclusion");
        ensure!(session.mmr_assumptions.is_empty()&&session.work().is_none(),"unsupported MMR/PoVW");
        let session_claim=session.claim()?;
        ensure!(session_claim.digest()==expected_claim.digest(),"exact resolved expected session claim");
        let segments=session.segments().collect::<Result<Vec<_>>>()?;
        ensure!(!segments.is_empty()&&segments.len()<=SEGMENT_LIMIT,"segment count");
        for (i,segment) in segments.iter().enumerate() {
            ensure!(segment.index as usize==i && segment.po2()<=po2 as usize,"snapshot consecutive segment size");
        }
        let mut order=Vec::new();
        for (_,assumption) in &session.assumptions {
            match assumption {
                AssumptionReceipt::Proven(InnerAssumptionReceipt::Succinct(value))=>{
                    ensure!(value.hashfn=="poseidon2","actual assumption hash suite");
                    value.verify_integrity_with_context(&ctx)?;
                    order.push(value.claim.digest());
                },
                _=>anyhow::bail!("only proven succinct actual assumptions supported"),
            }
        }
        // Cross-bind actual assumption ordering to this call's fully verified parent set.
        ordered_assumptions(&parents,&order,&ctx)?;
        let snapshot=Snapshot {version:SNAPSHOT_SCHEMA,session_binding,session_claim,
            assumption_order:order,segments};
        let raw=encode(&snapshot)?;
        let binding=hash(&encode(&("DMKN-MODULE-SNAPSHOT-V2",session_binding,hash(&raw)))?);
        write_new(&args[9],&raw)?;
        println!("REAL_EXECUTION_SNAPSHOT_NOT_APPLICATION_CERTIFICATE schema={SNAPSHOT_SCHEMA} snapshot_bytes={} segments={} assumptions={} binding={binding}",
            raw.len(),snapshot.segments.len(),snapshot.assumption_order.len());
        return Ok(());
    }
    // All later stages consume this ONE coherent capsule. No guest reexecution.
    ensure!(args.len()>=12+parent_count,"explicit coherent capsule required");
    let snapshot_raw=read_bounded(&args[11+parent_count],FILE_LIMIT)?;
    read_total=read_total.checked_add(snapshot_raw.len() as u64).context("aggregate read overflow")?;
    ensure!(read_total<=TOTAL_READ_LIMIT,"aggregate input byte limit");
    let snapshot:Snapshot=decode(&snapshot_raw)?;
    ensure!(snapshot.version==SNAPSHOT_SCHEMA && snapshot.session_binding==session_binding,
        "capsule version/operation binding");
    ensure!(snapshot.session_claim.digest()==expected_claim.digest(),"capsule exact expected claim");
    let segments=snapshot.segments;
    ensure!(!segments.is_empty()&&segments.len()<=SEGMENT_LIMIT,"capsule segment count");
    for (i,segment) in segments.iter().enumerate() {
        ensure!(segment.index as usize==i && segment.po2()<=po2 as usize,"capsule consecutive segment size");
    }
    let assumptions=ordered_assumptions(&parents,&snapshot.assumption_order,&ctx)?;
    let session_claim=snapshot.session_claim;
    let last=(segments.len()-1) as u32;
    ensure!((kind=="finish"&&index==0)
        ||(kind=="resolve"&&(index as usize)<assumptions.len())
        ||(matches!(kind,"segment"|"lift"|"join")&&index<=last&&(kind!="join"||index>=1)),
        "stage index outside capsule");
    let binding=hash(&encode(&("DMKN-MODULE-SNAPSHOT-V2",session_binding,hash(&snapshot_raw)))?);
    let mut cache=BTreeMap::new();
    for path in &args[12+parent_count..] {
        let raw=read_bounded(path,FILE_LIMIT)?;
        read_total=read_total.checked_add(raw.len() as u64).context("aggregate read overflow")?;
        ensure!(read_total<=TOTAL_READ_LIMIT,"aggregate input byte limit");
        let (version,saved_binding,saved_kind,saved_index,object):Checkpoint=decode(&raw)?;
        ensure!(version==CHECKPOINT_SCHEMA&&saved_binding==binding,"checkpoint capsule binding");
        ensure!(matches!(saved_kind.as_str(),"segment"|"lift"|"join"|"resolve"),"checkpoint kind");
        ensure!(cache.insert((saved_kind,saved_index),object).is_none(),"duplicate checkpoint key");
    }
    let prover = get_prover_server(&opts)?;
    progress(kind, index, "crypto", started);
    let object = match kind {
        "segment" => {
            ensure!(cache.is_empty(), "segment stage takes no checkpoints");
            let value = prover.prove_segment(&ctx, &segments[index as usize])?;
            ensure!(value.index == index && value.hashfn == "poseidon2", "new segment index/hash");
            value.verify_integrity_with_context(&ctx)?;
            encode(&value)?
        }
        "lift" => {
            let segment = take_segment(&mut cache, index, &ctx)?;
            ensure!(cache.is_empty(), "unused checkpoint");
            let value = prover.lift(&segment)?;
            value.verify_integrity_with_context(&ctx)?;
            ensure!(value.claim.digest() == segment.claim.digest(), "lift changed claim");
            encode(&value)?
        }
        "join" => {
            let (left_kind, left_index) = prefix_key(index - 1);
            let left = take_succinct(&mut cache, left_kind, left_index, &ctx)?;
            let right = take_succinct(&mut cache, "lift", index, &ctx)?;
            ensure!(cache.is_empty(), "unused checkpoint");
            let value = prover.join(&left, &right)?;
            value.verify_integrity_with_context(&ctx)?;
            encode(&value)?
        }
        "resolve" => {
            let (prior_kind, prior_index) = if index == 0 { prefix_key(last) } else { ("resolve", index - 1) };
            let prior = take_succinct(&mut cache, prior_kind, prior_index, &ctx)?;
            ensure!(cache.is_empty(), "unused checkpoint");
            let InnerAssumptionReceipt::Succinct(assumption) = &assumptions[index as usize] else {
                anyhow::bail!("non-succinct actual assumption");
            };
            let value = prover.resolve(&prior, assumption)?;
            value.verify_integrity_with_context(&ctx)?;
            encode(&value)?
        }
        "finish" => {
            let mut proven_segments = Vec::new();
            for i in 0..=last { proven_segments.push(take_segment(&mut cache, i, &ctx)?); }
            let (final_kind, final_index) = if assumptions.is_empty() { prefix_key(last) }
                else { ("resolve", (assumptions.len() - 1) as u32) };
            let succinct = take_succinct(&mut cache, final_kind, final_index, &ctx)?;
            ensure!(cache.is_empty(), "unused checkpoint");
            let parameters = ctx.composite_verifier_parameters().context("composite parameters absent")?.digest();
            // CompositeReceipt is non_exhaustive with no public constructor. The pinned SDK's
            // serde field order is (segments, assumption_receipts, verifier_parameters).
            // Roundtrip additionally checks this local adapter convention; cryptographic
            // verification below is still mandatory and is not replaced by serialization.
            let tuple = encode(&(proven_segments, assumptions, parameters))?;
            let composite: CompositeReceipt = decode(&tuple)?;
            ensure!(encode(&composite)? == tuple, "pinned composite serde layout mismatch");
            composite.verify_integrity_with_context(&ctx)?;
            ensure!(composite.claim()?.digest() == session_claim.digest(), "composite differs from exact expected capsule claim");
            ensure!(succinct.claim.digest() == session_claim.digest(), "succinct differs from exact expected capsule claim");
            let receipt = Receipt::new(InnerReceipt::Succinct(succinct), expected.clone());
            checked_receipt(&receipt, id)?;
            ensure!(receipt.journal.bytes == expected, "exact final journal mismatch");
            let raw = encode(&receipt)?;
            write_new(&args[9], &raw)?;
            progress(kind, index, "written", started);
            println!("REAL_SUCCINCT_CHECKPOINT_FINISHED image_id={id} rank={} groups={} receipt_bytes={} parents={parent_count} segments={} binding={binding}",
                child.rank, child.group_count, raw.len(), segments.len());
            return Ok(());
        }
        _ => unreachable!(),
    };
    let checkpoint: Checkpoint = (CHECKPOINT_SCHEMA, binding, kind.to_owned(), index, object);
    let raw = encode(&checkpoint)?;
    write_new(&args[9], &raw)?;
    progress(kind, index, "written", started);
    println!("REAL_PROOF_CHECKPOINT_NOT_APPLICATION_CERTIFICATE kind={kind} index={index} checkpoint_bytes={} segments={} assumptions={} binding={binding}",
        raw.len(), segments.len(), assumptions.len());
    Ok(())
}

fn main() -> Result<()> {
    let args:Vec<String>=env::args().collect();
    ensure!(env::var_os("RISC0_DEV_MODE").is_none(),"dev-mode environment forbidden");
    ensure!(args.len()>=2,"explicit command required");
    match args[1].as_str() {
        "prepare"=>prepare(&args),
        "execute"=>execute(&args),
        "trace"=>trace::trace(&args),
        "stage"=>stage(&args),
        "verify"|"receive"=>{
            ensure!(args.len()==5,
                "verify ADOPTED_IMAGE_ID RECEIPT EXPECTED_JOURNAL | receive ADOPTED_IMAGE_ID RECEIPT EXPECTED_MODULE_ID");
            let id=image_id(&args[2])?;
            let bytes=read_bounded(&args[3],FILE_LIMIT)?;
            let receipt:Receipt=decode(&bytes)?;
            let started=Instant::now();
            let accepted=checked_receipt(&receipt,id)?;
            if args[1]=="verify" {
                let expected=read_bounded(&args[4],JOURNAL_LIMIT)?;
                application(&expected,id)?;
                ensure!(receipt.journal.bytes==expected,"exact final journal mismatch");
            } else {
                ensure!(accepted.module==checked(canonical::unhex(&args[4]))?,
                    "expected requested ModuleID");
            }
            println!("{}",json!({"status":"REAL_MODULE_RECEIPT_VERIFIED",
                "image":accepted.image,"foundation":canonical::hex(&accepted.foundation),
                "policy":canonical::hex(&accepted.policy),"module":canonical::hex(&accepted.module),
                "summary":accepted.summary(),"rank":accepted.rank,
                "receipt_sha256":canonical::hex(&canonical::sha(&bytes)),"receipt_bytes":bytes.len(),
                "journal":receipt.journal.bytes,"inner_verify_ms":started.elapsed().as_millis(),
                "fully_resolved":true,"receipt_kind":"succinct-poseidon2",
                "mathematical_admission":true}));
            // A public controller may mint private evidence from this SAME
            // supervised call. Loading an arbitrary saved success JSON cannot.
            Ok(())
        },
        _=>anyhow::bail!("explicit prepare/execute/trace/stage/verify/receive command required"),
    }
}

