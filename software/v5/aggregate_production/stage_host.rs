//! Staged aggregate proving from ONE complete DMKNAS01 capsule; no new session.
//! Segment proving still performs SDK segment preflight/witness reconstruction.
//! Checkpoints/reports are untrusted aids, never mathematical admission handles.
//! Outer counts are preallocation-bounded; nested SDK decoding still requires
//! owner process limits. Bincode's byte limit is NOT a total heap bound/sandbox.
#[path = "../aggregate/receipt.rs"] mod receipt;

use std::{collections::{BTreeMap, BTreeSet}, env, fs,
    io::{Read, Write}, marker::PhantomData, path::{Component, Path}, time::Instant};
use anyhow::{Context, Result, ensure};
use bincode::Options;
use dmkn_aggregate_relation::{header::{self, Header}, relation};
use dmkn_module_relation::canonical;
use risc0_zkvm::{compute_image_id, get_prover_server, CompositeReceipt,
    InnerAssumptionReceipt, InnerReceipt, ProverOpts, Receipt, ReceiptClaim,
    Segment, SegmentReceipt, SuccinctReceipt, VerifierContext,
    sha::{self, Digest, Digestible, Sha256}};
use serde::{Deserialize, Deserializer, Serialize,
    de::{DeserializeOwned, SeqAccess, Visitor}};
use serde_json::json;

const FILE_LIMIT: u64 = 64 * 1024 * 1024;
const WIRE_LIMIT: u64 = 16 * 1024 * 1024;
const READ_LIMIT: u64 = 512 * 1024 * 1024;
const SEGMENT_LIMIT: usize = 128;
const SNAPSHOT_MAGIC: [u8; 8] = *b"DMKNAS01";
const SNAPSHOT_VERSION: u32 = 1;
const CHECKPOINT_MAGIC: [u8; 8] = *b"DMKNAP01";
const CHECKPOINT_VERSION: u32 = 1;

/// Bincode supplies the exact declared sequence length as its size hint.
/// Refuse an absent/excessive hint BEFORE allocating or decoding elements.
/// This changes deserialization bounds, NOT the serialized Vec representation.
fn bounded_vec<'de, D, T, const MAX: usize>(deserializer: D)
    -> std::result::Result<Vec<T>, D::Error>
where D: Deserializer<'de>, T: Deserialize<'de> {
    struct Bounded<T, const MAX: usize>(PhantomData<T>);
    impl<'de, T: Deserialize<'de>, const MAX: usize> Visitor<'de> for Bounded<T, MAX> {
        type Value = Vec<T>;
        fn expecting(&self, formatter: &mut std::fmt::Formatter) -> std::fmt::Result {
            write!(formatter, "a fixed-length sequence with at most {MAX} entries")
        }
        fn visit_seq<S: SeqAccess<'de>>(self, mut sequence: S)
            -> std::result::Result<Self::Value, S::Error> {
            let count = sequence.size_hint().ok_or_else(||
                <S::Error as serde::de::Error>::custom("missing exact bincode sequence length"))?;
            if count > MAX {
                return Err(<S::Error as serde::de::Error>::custom("outer sequence count bound"));
            }
            let mut values = Vec::with_capacity(count);
            for _ in 0..count {
                values.push(sequence.next_element()?.ok_or_else(||
                    <S::Error as serde::de::Error>::custom("truncated fixed-length sequence"))?);
            }
            Ok(values)
        }
    }
    deserializer.deserialize_seq(Bounded::<T, MAX>(PhantomData))
}

fn bounded_assumptions<'de, D: Deserializer<'de>>(deserializer: D)
    -> std::result::Result<Vec<Digest>, D::Error> {
    bounded_vec::<D, Digest, {relation::MAX_ASSUMPTIONS}>(deserializer)
}

fn bounded_segments<'de, D: Deserializer<'de>>(deserializer: D)
    -> std::result::Result<Vec<Segment>, D::Error> {
    bounded_vec::<D, Segment, SEGMENT_LIMIT>(deserializer)
}

/// EXACT field order/type/encoding of aggregate_host::AggregateSnapshot.
/// The deserialize-only visitors bound outer counts before allocation.
#[derive(Serialize, Deserialize)]
struct AggregateSnapshot {
    magic: [u8; 8],
    version: u32,
    session_binding: Digest,
    session_claim: ReceiptClaim,
    #[serde(deserialize_with = "bounded_assumptions")]
    assumption_order: Vec<Digest>,
    #[serde(deserialize_with = "bounded_segments")]
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
    file.take(limit + 1).read_to_end(&mut raw)?;
    ensure!(!raw.is_empty() && raw.len() as u64 <= limit, "input grew past bound");
    Ok(raw)
}

fn read_charged(path: &str, maximum: u64, total: &mut u64) -> Result<Vec<u8>> {
    let remaining = READ_LIMIT.checked_sub(*total).context("read budget exhausted")?;
    let raw = read_bounded(Path::new(path), maximum.min(remaining))?;
    *total = total.checked_add(raw.len() as u64).context("read byte overflow")?;
    ensure!(*total <= READ_LIMIT, "aggregate input read budget");
    Ok(raw)
}

fn write_new(path: &Path, raw: &[u8]) -> Result<()> {
    ensure!(!raw.is_empty() && raw.len() as u64 <= FILE_LIMIT, "output byte bound");
    ordinary_path(path, true)?;
    let mut file = fs::OpenOptions::new().write(true).create_new(true).open(path)?;
    file.write_all(raw)?; file.sync_all()?;
    Ok(())
}

fn encode<T: Serialize>(value: &T) -> Result<Vec<u8>> {
    Ok(bincode::DefaultOptions::new().with_fixint_encoding()
        .with_limit(FILE_LIMIT).serialize(value)?)
}

fn decode<T: DeserializeOwned>(raw: &[u8]) -> Result<T> {
    ensure!(!raw.is_empty() && raw.len() as u64 <= FILE_LIMIT, "encoded object byte bound");
    Ok(bincode::DefaultOptions::new().with_fixint_encoding().with_limit(FILE_LIMIT)
        .reject_trailing_bytes().deserialize(raw)?)
}

fn adopted_image(text: &str) -> Result<([u32; 8], Digest)> {
    let bytes = checked(canonical::unhex(text))?;
    ensure!(text.len() == 64 && text == canonical::hex(&bytes), "lowercase adopted image");
    let words = header::image_words(bytes);
    checked(header::distinct_aggregate_image(words))?;
    Ok((words, Digest::from(words)))
}

/// Only after EACH parent had full typed application verification in this call.
fn ordered_assumptions(parents: &[Receipt], order: &[Digest], context: &VerifierContext)
    -> Result<Vec<InnerAssumptionReceipt>> {
    ensure!(order.len() == parents.len() && order.len() <= relation::MAX_ASSUMPTIONS,
        "exact bounded assumption order");
    let mut actual = BTreeMap::new();
    for receipt in parents {
        let InnerReceipt::Succinct(value) = &receipt.inner else { anyhow::bail!("non-succinct parent"); };
        ensure!(value.hashfn == "poseidon2", "parent assumption hash suite");
        value.verify_integrity_with_context(context)?;
        ensure!(actual.insert(value.claim.digest().as_bytes().to_vec(), value.clone()).is_none(),
            "duplicate parent claim digest");
    }
    let mut output = Vec::with_capacity(order.len());
    for digest in order {
        let value = actual.remove(digest.as_bytes())
            .context("capsule assumption not exact verified typed parent")?;
        let unknown = value.into_unknown();
        ensure!(unknown.claim.digest() == *digest, "claim erasure changed digest");
        output.push(InnerAssumptionReceipt::Succinct(unknown));
    }
    ensure!(actual.is_empty(), "missing capsule parent assumption");
    Ok(output)
}

/// Fixed-integer bincode envelope: (magic[8], version:u32, Digest, String,
/// index:u32, Vec<u8>). Validate exact extent BEFORE copying/decoding payload.
fn checkpoint_view<'a>(raw: &'a [u8], binding: &Digest) -> Result<(&'a str, u32, &'a [u8])> {
    ensure!(raw.len() >= 65 && raw.len() as u64 <= FILE_LIMIT, "checkpoint byte bound");
    ensure!(raw[..8] == CHECKPOINT_MAGIC
        && u32::from_le_bytes(raw[8..12].try_into().unwrap()) == CHECKPOINT_VERSION,
        "aggregate checkpoint magic/version");
    ensure!(&raw[12..44] == binding.as_bytes(), "checkpoint capsule binding");
    let length = u64::from_le_bytes(raw[44..52].try_into().unwrap());
    ensure!((1..=7).contains(&length), "checkpoint kind length");
    let n = length as usize;
    ensure!(raw.len() >= 64+n, "truncated checkpoint fields");
    let kind = std::str::from_utf8(&raw[52..52+n])?;
    ensure!(matches!(kind, "segment"|"lift"|"join"|"resolve"), "checkpoint kind");
    let index = u32::from_le_bytes(raw[52+n..56+n].try_into().unwrap());
    let payload = u64::from_le_bytes(raw[56+n..64+n].try_into().unwrap());
    ensure!(payload > 0 && payload == (raw.len()-(64+n)) as u64, "exact checkpoint payload extent");
    Ok((kind, index, &raw[64+n..]))
}

fn take_segment(cache: &mut BTreeMap<(String, u32), Vec<u8>>, index: u32,
                context: &VerifierContext) -> Result<SegmentReceipt> {
    let raw = cache.remove(&("segment".to_owned(), index)).context("segment checkpoint absent")?;
    let value: SegmentReceipt = decode(&raw)?;
    ensure!(value.index == index && value.hashfn == "poseidon2", "segment index/hash suite");
    let parameters = context.segment_verifier_parameters.as_ref().context("segment parameters absent")?;
    ensure!(value.verifier_parameters == parameters.digest(), "exact segment verifier parameters");
    value.verify_integrity_with_context(context)?;
    Ok(value)
}

fn take_succinct(cache: &mut BTreeMap<(String, u32), Vec<u8>>, kind: &str, index: u32,
                 context: &VerifierContext) -> Result<SuccinctReceipt<ReceiptClaim>> {
    let raw = cache.remove(&(kind.to_owned(), index)).context("succinct checkpoint absent")?;
    let value: SuccinctReceipt<ReceiptClaim> = decode(&raw)?;
    ensure!(value.hashfn == "poseidon2", "succinct checkpoint hash suite");
    value.verify_integrity_with_context(context)?;
    Ok(value)
}

fn prefix_key(last: u32) -> (&'static str, u32) {
    if last == 0 { ("lift", 0) } else { ("join", last) }
}

fn progress(kind: &str, index: u32, phase: &str, started: Instant) {
    let mut stderr = std::io::stderr().lock();
    let _ = writeln!(stderr, "AGGREGATE_STAGE_PROGRESS kind={kind} index={index} phase={phase} elapsed_ms={}",
        started.elapsed().as_millis());
    let _ = stderr.flush();
}

fn stage(args: &[String]) -> Result<()> {
    ensure!((13..=13+relation::MAX_ASSUMPTIONS+SEGMENT_LIMIT+1).contains(&args.len()),
        "stage ADOPTED_A ELF WIRE EXPECTED_HEADER CYCLES PO2 KIND INDEX FRESH_OUTPUT RECEIPT_COUNT [RECEIPTS...] CAPSULE [CHECKPOINTS...]");
    let started = Instant::now();
    let (words, adopted) = adopted_image(&args[2])?;
    let cycles: u64 = args[6].parse()?;
    let po2: u32 = args[7].parse()?;
    ensure!((1..=(1u64<<28)).contains(&cycles) && (12..=20).contains(&po2), "finite selected session bounds");
    let kind = args[8].as_str();
    let index: u32 = args[9].parse()?;
    ensure!(matches!(kind, "segment"|"lift"|"join"|"resolve"|"finish"), "explicit proof stage only");
    ordinary_path(Path::new(&args[10]), true)?;
    let count: usize = args[11].parse()?;
    ensure!(count <= relation::MAX_ASSUMPTIONS && args.len() >= 13+count, "exact bounded parent count");

    let mut total_read = 0;
    let elf = read_charged(&args[3], FILE_LIMIT, &mut total_read)?;
    ensure!(compute_image_id(&elf)? == adopted, "actual ELF differs from independently adopted A");
    let wire = read_charged(&args[4], WIRE_LIMIT, &mut total_read)?;
    let expected = read_charged(&args[5], header::BYTES as u64, &mut total_read)?;
    let header = checked(Header::decode(&expected))?;
    checked(header.bind_image(words))?;
    // Same deterministic preflight as the snapshot host, not guest execution.
    let conditional = checked(relation::check_bytes(&wire))?;
    ensure!(checked(conditional.header().encode())? == expected
        && conditional.assumptions().len() == count, "exact derived header and pending claims");
    let mut parents = Vec::with_capacity(count);
    let mut parent_hashes = Vec::with_capacity(count);
    let mut exact_claims = BTreeSet::new();
    for (path, pending) in args[12..12+count].iter().zip(conditional.assumptions()) {
        ensure!(exact_claims.insert((pending.image(), pending.journal().to_vec())), "duplicate typed pending claim");
        let raw = read_charged(path, FILE_LIMIT, &mut total_read)?;
        let verified = receipt::verify_pending(&raw, pending, words)?;
        ensure!(verified.image() == pending.image(), "exact verified boundary image");
        parent_hashes.push(hash(&raw));
        parents.push(verified.receipt().clone());
    }
    let session_binding = hash(&encode(&("DMKN-AGGREGATE-SESSION-V1", hash(&elf), adopted,
        header.relation_image, header.foundation, header.policy, hash(&wire), hash(&expected),
        cycles, po2, &parent_hashes))?);
    let expected_claim = ReceiptClaim::ok(adopted, expected.clone());
    let context = VerifierContext::default().with_dev_mode(false);
    let capsule_raw = read_charged(&args[12+count], FILE_LIMIT, &mut total_read)?;
    ensure!(capsule_raw.len() >= 12 && capsule_raw[..8] == SNAPSHOT_MAGIC
        && u32::from_le_bytes(capsule_raw[8..12].try_into().unwrap()) == SNAPSHOT_VERSION,
        "aggregate capsule magic/version");
    let snapshot: AggregateSnapshot = decode(&capsule_raw)?;
    ensure!(snapshot.magic == SNAPSHOT_MAGIC && snapshot.version == SNAPSHOT_VERSION
        && snapshot.session_binding == session_binding, "capsule exact operation binding");
    ensure!(snapshot.session_claim.digest() == expected_claim.digest(), "capsule exact target application claim");
    let segments = snapshot.segments;
    ensure!(!segments.is_empty() && segments.len() <= SEGMENT_LIMIT, "complete bounded segment vector");
    for (i, segment) in segments.iter().enumerate() {
        ensure!(segment.index as usize == i && segment.po2() <= po2 as usize,
            "capsule consecutive segment index/size");
    }
    let assumptions = ordered_assumptions(&parents, &snapshot.assumption_order, &context)?;
    let s = segments.len(); let m = assumptions.len(); let last = (s-1) as u32;
    ensure!((kind == "finish" && index == 0)
        || (kind == "resolve" && (index as usize) < m)
        || (matches!(kind, "segment"|"lift"|"join") && index <= last && (kind != "join" || index >= 1)),
        "stage index outside actual capsule");
    let binding = hash(&encode(&("DMKN-AGGREGATE-SNAPSHOT-V1", session_binding, hash(&capsule_raw)))?);
    let mut cache = BTreeMap::new();
    for path in &args[13+count..] {
        let raw = read_charged(path, FILE_LIMIT, &mut total_read)?;
        let (saved_kind, saved_index, payload) = checkpoint_view(&raw, &binding)?;
        ensure!(cache.insert((saved_kind.to_owned(), saved_index), payload.to_vec()).is_none(),
            "duplicate checkpoint key");
    }
    // The owner meters this entire call, including repeated native preflight,
    // parent verification, capsule decoding and final reporting/write tails.
    progress(kind, index, "crypto", started);
    let final_receipt = kind == "finish";
    let output = if final_receipt {
        let mut proven_segments = Vec::with_capacity(s);
        for i in 0..=last { proven_segments.push(take_segment(&mut cache, i, &context)?); }
        let (final_kind, final_index) = if m == 0 { prefix_key(last) } else { ("resolve", (m-1) as u32) };
        let succinct = take_succinct(&mut cache, final_kind, final_index, &context)?;
        ensure!(cache.is_empty(), "unused finish checkpoint");
        let parameters = context.composite_verifier_parameters().context("composite parameters absent")?.digest();
        // Pinned SDK non_exhaustive layout; roundtrip is NOT crypto verification.
        let tuple = encode(&(proven_segments, assumptions, parameters))?;
        let composite: CompositeReceipt = decode(&tuple)?;
        ensure!(encode(&composite)? == tuple, "pinned composite serde layout mismatch");
        composite.verify_integrity_with_context(&context)?;
        ensure!(composite.claim()?.digest() == snapshot.session_claim.digest()
            && composite.claim()?.digest() == expected_claim.digest(), "verified composite target claim mismatch");
        ensure!(succinct.claim.digest() == expected_claim.digest(), "final succinct target claim mismatch");
        let application = Receipt::new(InnerReceipt::Succinct(succinct), expected.clone());
        let raw = encode(&application)?;
        let verified = receipt::verify_aggregate(&raw, &expected, words)?;
        ensure!(verified.image() == words && verified.receipt().journal.bytes == expected,
            "final exact aggregate application binding");
        raw
    } else {
        let options = ProverOpts::succinct().with_dev_mode(false).with_prove_guest_errors(false);
        let prover = get_prover_server(&options)?;
        let object = match kind {
            "segment" => {
                ensure!(cache.is_empty(), "segment takes no checkpoint");
                let value = prover.prove_segment(&context, &segments[index as usize])?;
                let parameters = context.segment_verifier_parameters.as_ref().context("segment parameters absent")?;
                ensure!(value.index == index && value.hashfn == "poseidon2"
                    && value.verifier_parameters == parameters.digest(), "new segment index/hash/parameters");
                value.verify_integrity_with_context(&context)?;
                encode(&value)?
            },
            "lift" => {
                let segment = take_segment(&mut cache, index, &context)?;
                ensure!(cache.is_empty(), "unused lift checkpoint");
                let value = prover.lift(&segment)?;
                value.verify_integrity_with_context(&context)?;
                ensure!(value.claim.digest() == segment.claim.digest(), "lift changed claim");
                encode(&value)?
            },
            "join" => {
                let (left_kind, left_index) = prefix_key(index-1);
                let left = take_succinct(&mut cache, left_kind, left_index, &context)?;
                let right = take_succinct(&mut cache, "lift", index, &context)?;
                ensure!(cache.is_empty(), "unused join checkpoint");
                let value = prover.join(&left, &right)?;
                value.verify_integrity_with_context(&context)?;
                encode(&value)?
            },
            "resolve" => {
                let (prior_kind, prior_index) = if index == 0 { prefix_key(last) } else { ("resolve", index-1) };
                let prior = take_succinct(&mut cache, prior_kind, prior_index, &context)?;
                ensure!(cache.is_empty(), "unused resolve checkpoint");
                let InnerAssumptionReceipt::Succinct(assumption) = &assumptions[index as usize] else {
                    anyhow::bail!("non-succinct actual assumption");
                };
                let value = prover.resolve(&prior, assumption)?;
                value.verify_integrity_with_context(&context)?;
                encode(&value)?
            },
            _ => anyhow::bail!("unsupported proving stage"),
        };
        let raw = encode(&(CHECKPOINT_MAGIC, CHECKPOINT_VERSION, binding, kind.to_owned(), index, object))?;
        let (saved_kind, saved_index, _) = checkpoint_view(&raw, &binding)?;
        ensure!(saved_kind == kind && saved_index == index, "aggregate checkpoint serialization layout");
        raw
    };
    write_new(Path::new(&args[10]), &output)?;
    progress(kind, index, "written", started);
    println!("{}", json!({"schema":"DMKN_AGGREGATE_PROOF_STAGE_V1",
        "status":if final_receipt {"REAL_AGGREGATE_RECEIPT_FINISHED"} else {"REAL_AGGREGATE_CHECKPOINT_NOT_APPLICATION_RECEIPT"},
        "kind":kind,"index":index,"aggregate_image":args[2],"header_sha256":sha_hex(&expected),
        "capsule_binding":binding.to_string(),"session_binding":session_binding.to_string(),
        "segments":s,"assumptions":m,"output_bytes":output.len(),"output_sha256":sha_hex(&output),
        // This counts whole-session ExecutorImpl acquisition only, not the
        // segment witness reconstruction included in prove_segment's cost.
        "application_receipt_created":final_receipt,"guest_execute_calls":0,
        "proof_stage_calls":if final_receipt {0} else {1},"mathematical_admission":false}));
    Ok(())
}

fn verify(args: &[String]) -> Result<()> {
    ensure!(args.len() == 5, "verify ADOPTED_A RECEIPT EXPECTED_HEADER");
    let (words, _) = adopted_image(&args[2])?;
    let raw = read_bounded(Path::new(&args[3]), FILE_LIMIT)?;
    let expected = read_bounded(Path::new(&args[4]), header::BYTES as u64)?;
    let verified = receipt::verify_aggregate(&raw, &expected, words)?;
    ensure!(verified.image() == words, "actual verified aggregate image");
    // EXACT existing public aggregate receiver result contract.
    println!("{}", json!({"schema":"DMKN_AGGREGATE_VERIFY_RESULT_V1",
        "status":"VERIFIED_RESOLVED_AGGREGATE_RECEIPT","aggregate_image":args[2],
        "header":expected,"receipt_sha256":sha_hex(&raw),"receipt_bytes":raw.len()}));
    Ok(())
}

fn main() -> Result<()> {
    ensure!(env::var_os("RISC0_DEV_MODE").is_none(), "dev-mode environment forbidden");
    ensure!(env::var_os("RISC0_PPROF_OUT").is_none(), "ambient profiler output forbidden");
    let args = env::args().collect::<Vec<_>>();
    ensure!(args.len() >= 2, "explicit aggregate stage/verify command");
    match args[1].as_str() {
        "stage" => stage(&args),
        "verify" => verify(&args),
        _ => anyhow::bail!("only aggregate stage/verify commands are supported; no guest execution"),
    }
}
