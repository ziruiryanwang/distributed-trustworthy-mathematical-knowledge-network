//! One source-only-selected, per-delta support-refinement control harness.
mod controls;
// Exact production private units, not a replacement acceptance implementation.
#[path = "syntax.rs"]
mod syntax;
#[path = "typing.rs"]
mod typing;
#[path = "../restricted_composition/foundation02.rs"]
mod foundation;

use serde_json::{json, Value};
use std::{env, fs::File, io::Read, process};

fn fixture() -> Result<Value, String> {
    let args: Vec<_> = env::args_os().collect();
    if args.len() != 2 { return Err("exactly one retained fixture path".into()); }
    let mut raw = Vec::new();
    File::open(&args[1]).map_err(|e| e.to_string())?
        .take(4 * 1024 * 1024 + 1).read_to_end(&mut raw).map_err(|e| e.to_string())?;
    if raw.len() != 84727 || dmkn_module_relation::canonical::hex(
        &dmkn_module_relation::canonical::sha(&raw)) !=
        "019219ca4548dafbdaa814c209a4ec087229091750db3f3cf48fcc155269f40a" {
        return Err("exact adopted retained fixture bytes".into());
    }
    let value: Value = serde_json::from_slice(&raw).map_err(|e| e.to_string())?;
    let fields = value.as_object().ok_or("fixture object")?;
    let names = ["first", "second", "first_witness", "second_witness"];
    if fields.len() != names.len() || names.iter().any(|n| !fields.contains_key(*n)) {
        return Err("exact four fixture fields".into());
    }
    Ok(value)
}

fn failure(error: String) -> Value {
    json!({"schema":"DMKN_RC_SUPPORT_CONTROLS_V1", "status":"FAIL",
        "executed":[], "executed_count":0, "expected_refusals":[],
        "errors":[{"control":"harness", "error":error}],
        "crypto_produced":false, "proof_calls":0, "guest_calls":0,
        "global_growth_claim":false,
        "authority":"NATIVE_CONDITIONAL_CONTROLS_NOT_RECEIPT_AUTHORITY"})
}

fn main() {
    let report = match fixture() {
        Ok(value) => match std::thread::Builder::new().name("support-controls".into())
            .stack_size(16 * 1024 * 1024).spawn(move || controls::run(value)) {
            Ok(worker) => worker.join().unwrap_or_else(|_| failure("control worker panicked".into())),
            Err(error) => failure(error.to_string()),
        },
        Err(error) => failure(error),
    };
    println!("{}", serde_json::to_string(&report).expect("bounded JSON report"));
    if report["status"] != "PASS" { process::exit(1); }
}
