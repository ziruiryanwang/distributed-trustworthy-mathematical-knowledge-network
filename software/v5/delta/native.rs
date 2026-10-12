//! A conditional native judgment, NEVER standalone mathematical admission.
//! The owner controller discharges every exact returned parent journal through
//! real live receipt authority or an earlier checked delta in the same packet.
#[path = "../modules/receipt/src/canonical.rs"] mod canonical;
#[path = "../modules/receipt/src/input.rs"] mod input;
#[path = "../modules/receipt/src/foundation_static.rs"] mod foundation_static;
#[path = "../modules/receipt/src/commitments.rs"] mod commitments;
#[path = "../modules/receipt/src/journal.rs"] mod journal;
#[path = "../modules/receipt/src/policy.rs"] mod policy;
#[path = "../modules/receipt/src/relation.rs"] mod relation;

use canonical::{require, R};
use serde_json::{json, Value};
use std::io::Read;

fn check() -> R<Value> {
    let args = std::env::args().collect::<Vec<_>>();
    require(args.len() == 4 && args[1] == "check", "check ADOPTED_IMAGE_ID INPUT")?;
    let selected = canonical::unhex(&args[2])?;
    let file = std::fs::File::open(&args[3]).map_err(|e| e.to_string())?;
    require(file.metadata().map_err(|e| e.to_string())?.len() <= canonical::MAX_BYTES as u64,
        "input byte limit")?;
    let mut raw = Vec::new();
    file.take(canonical::MAX_BYTES as u64 + 1).read_to_end(&mut raw).map_err(|e| e.to_string())?;
    let result = relation::check_bytes(&raw)?;
    let bytes = result.journal.encode()?;
    // The guest's own image is ordinarily pinned by external receipt checking.
    // A native-only conditional conclusion must explicitly bind that field too.
    require(bytes[12..44] == selected, "own adopted image")?;
    require(result.journal.foundation == policy::foundation()
        && result.journal.policy == policy::semantic_id()?, "own adopted policy")?;
    require(result.parent_journals.len() <= 4096, "parent count")?;
    Ok(json!({"schema":"DMKN_NATIVE_DELTA_CONCLUSION_V1",
        "status":"CHECKED_CONDITIONAL_RELATION_NOT_ADMISSION",
        "input_sha256":canonical::hex(&canonical::sha(&raw)), "input_bytes":raw.len(),
        "journal":bytes, "parents":result.parent_journals,
        "mathematical_admission":false}))
}

fn main() {
    let thread = std::thread::Builder::new().name("native_delta".into()).stack_size(16_777_216)
        .spawn(|| std::panic::catch_unwind(check));
    let value = match thread {
        Ok(thread) => match thread.join() {
            Ok(Ok(Ok(value))) => value,
            Ok(Ok(Err(reason))) => json!({"status":"REFUSED", "reason":reason,
                "mathematical_admission":false}),
            _ => json!({"status":"REFUSED", "reason":"CHECKER_PANIC_OR_UNRESOLVED_DEMAND",
                "mathematical_admission":false}),
        },
        Err(_) => json!({"status":"REFUSED", "reason":"CHECKER_THREAD_UNAVAILABLE",
            "mathematical_admission":false}),
    };
    println!("{value}");
    if value["status"] == "REFUSED" { std::process::exit(2); }
}
