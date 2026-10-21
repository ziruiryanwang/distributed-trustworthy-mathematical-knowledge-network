//! One bounded native changed-boundary harness. This is not a guest or verifier.
//! Its sole input is the root-selected fixture path; no saved acceptance is used.

mod controls;

// Source-identical private core units: tests can exercise natural crate-private
// boundaries without adding any production audit API or alternative checker.
#[path = "syntax.rs"]
mod syntax;
#[path = "foundation02.rs"]
mod foundation;
#[path = "typing.rs"]
mod typing;

// Exact selected product census sources, included only to exercise private
// counter methods. Positive/graph checks use the separately compiled aggregate
// library, not a replaceable checker. No production API is widened for tests.
#[path = "census.rs"]
mod census;
#[path = "wire.rs"]
mod wire;
use dmkn_aggregate_relation::{header, relation};

use serde_json::{json, Value};
use std::{env, fs::File, io::Read, process};

const MAX_FIXTURE_BYTES: u64 = 4 * 1024 * 1024;

fn fixture() -> Result<Value, String> {
    let args: Vec<_> = env::args_os().collect();
    if args.len() != 2 {
        return Err("exactly one fixture path is required".into());
    }
    let mut raw = Vec::new();
    File::open(&args[1])
        .map_err(|e| format!("fixture open: {e}"))?
        .take(MAX_FIXTURE_BYTES + 1)
        .read_to_end(&mut raw)
        .map_err(|e| format!("fixture read: {e}"))?;
    if raw.is_empty() || raw.len() as u64 > MAX_FIXTURE_BYTES {
        return Err("fixture byte bound".into());
    }
    let value: Value = serde_json::from_slice(&raw)
        .map_err(|e| format!("fixture JSON: {e}"))?;
    let fields = value.as_object().ok_or("fixture must be an object")?;
    let required = ["first", "second", "first_witness", "second_witness"];
    if fields.len() != required.len() || required.iter().any(|key| !fields.contains_key(*key)) {
        return Err("fixture has exactly first, second, first_witness, second_witness".into());
    }
    Ok(value)
}

fn main() {
    let report = match fixture() {
        Ok(input) => match std::thread::Builder::new()
            .name("rc0-native-controls".into())
            .stack_size(16 * 1024 * 1024)
            .spawn(move || controls::run(input))
        {
            Ok(worker) => match worker.join() {
                Ok(report) => report,
                Err(_) => json!({
                    "schema": "DMKN_RC0_CONTROLS_V1", "status": "FAIL",
                    "executed": [], "executed_count": 0, "expected_refusals": [],
                    "errors": [{"control": "worker", "error": "native control worker panicked"}],
                    "authority": "NATIVE_CONDITIONAL_CONTROLS_NOT_RECEIPT_AUTHORITY"
                }),
            },
            Err(error) => json!({
                "schema": "DMKN_RC0_CONTROLS_V1", "status": "FAIL",
                "executed": [], "executed_count": 0, "expected_refusals": [],
                "errors": [{"control": "worker", "error": error.to_string()}],
                "authority": "NATIVE_CONDITIONAL_CONTROLS_NOT_RECEIPT_AUTHORITY"
            }),
        },
        Err(error) => json!({
            "schema": "DMKN_RC0_CONTROLS_V1", "status": "FAIL",
            "executed": [], "executed_count": 0, "expected_refusals": [],
            "errors": [{"control": "fixture", "error": error}],
            "authority": "NATIVE_CONDITIONAL_CONTROLS_NOT_RECEIPT_AUTHORITY"
        }),
    };
    println!("{}", serde_json::to_string(&report).expect("bounded report JSON"));
    if report.get("status").and_then(Value::as_str) != Some("PASS") {
        process::exit(1);
    }
}
