//! Native diagnostic of the SAME relation source. Never verifies parent proofs.
//! The guest entry point, not this program, performs actual env::verify calls.
#[path = "../canonical.rs"] mod canonical;
#[path = "../input.rs"] mod input;
#[path = "../foundation_static.rs"] mod foundation_static;
#[path = "../commitments.rs"] mod commitments;
#[path = "../journal.rs"] mod journal;
#[path = "../policy.rs"] mod policy;
#[path = "../relation.rs"] mod relation;

use canonical::{array, fields, hash, hex, parse, require, text, R};
use serde_json::{json, Value};
use std::io::Read;

fn bytes(value: &Value) -> R<Vec<u8>> {
    array(value)?.iter().map(|item| canonical::uint(item,255).map(|n| n as u8)).collect()
}

fn run() -> R<Value> {
    let args = std::env::args_os().collect::<Vec<_>>();
    require(args.len() >= 2, "receipt_native profile | hash INPUT | journal INPUT | openings INPUT | check INPUT")?;
    let action = args[1].to_str().ok_or("action encoding")?;
    if action == "profile" {
        require(args.len() == 2, "profile arguments")?;
        return Ok(json!({"status":"PROFILE_DESCRIPTION_ONLY", "policy":hex(&policy::semantic_id()?),
            "semantic_descriptor":policy::semantic_descriptor(), "foundation":policy::FOUNDATION_ID,
            "foundation_rows":policy::FOUNDATION_ROWS, "foundation_canonical_sha256":policy::FOUNDATION_CANONICAL_SHA256,
            "journal_bytes":journal::BYTES, "mathematical_admission":false}));
    }
    require(args.len() == 3, "input arguments")?;
    let file = std::fs::File::open(&args[2]).map_err(|e| e.to_string())?;
    require(file.metadata().map_err(|e| e.to_string())?.len() <= canonical::MAX_BYTES as u64, "input byte bound")?;
    let mut raw = Vec::new();
    file.take(canonical::MAX_BYTES as u64 + 1).read_to_end(&mut raw).map_err(|e| e.to_string())?;
    let value = parse(&raw)?;
    match action {
        "hash" => {
            let cases = array(&value)?; require(cases.len() <= 4096, "hash case count")?;
            let mut results = Vec::new();
            for case in cases {
                fields(case, &["domain","value"])?;
                results.push(hex(&hash(text(&case["domain"])?, &case["value"])?));
            }
            Ok(json!({"status":"HASHES_COMPUTED", "hashes":results, "mathematical_admission":false}))
        },
        "journal" => {
            let raw = bytes(&value)?; let decoded = journal::Journal::decode(&raw)?;
            Ok(json!({"status":"JOURNAL_STRUCTURE_ONLY", "roundtrip":decoded.encode()?,
                "summary":decoded.summary(), "module":hex(&decoded.module), "rank":decoded.rank,
                "mathematical_admission":false}))
        },
        "openings" => {
            fields(&value, &["journal","openings"])?;
            let parent = journal::Journal::decode(&bytes(&value["journal"])?)?;
            let openings = array(&value["openings"])?; require(openings.len() <= 4096, "opening count")?;
            let mut indices = Vec::new();
            for opening in openings { indices.push(commitments::verify_opening(&parent,opening)?.0); }
            Ok(json!({"status":"OPENING_HASH_BINDINGS_ONLY", "indices":indices, "mathematical_admission":false}))
        },
        "check" => {
            let result = relation::check(value)?;
            Ok(json!({"status":"BOUND_RELATION_NATIVE_ONLY_PENDING_PARENT_PROOF_VERIFICATION",
                "journal":result.journal.encode()?, "summary":result.journal.summary(),
                "module":hex(&result.journal.module), "rank":result.journal.rank,
                "pending_parent_statements":result.parent_journals.len(),
                "certificate_verification_performed":false, "mathematical_admission":false}))
        },
        _ => Err("unknown diagnostic action".into()),
    }
}

fn main() {
    let worker = std::thread::Builder::new().name("receipt_native".into()).stack_size(16_777_216)
        .spawn(|| std::panic::catch_unwind(run)).expect("native wrapper worker");
    let output = match worker.join() {
        Ok(Ok(Ok(value))) => value,
        Ok(Ok(Err(reason))) => json!({"status":"REFUSED", "reason":reason, "mathematical_admission":false}),
        _ => json!({"status":"REFUSED", "reason":"CHECKER_PANIC_OR_UNRESOLVED_DEMAND", "mathematical_admission":false}),
    };
    println!("{output}");
    if output["status"] == "REFUSED" { std::process::exit(2); }
}
