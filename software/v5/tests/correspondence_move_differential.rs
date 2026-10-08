//! Standalone constructor-change differential. No Nanoda kernel/backend link.
//! Owner supervisor must bind both included sources, five retained inputs,
//! compiler/runtime, executable and fresh output. This never admits mathematics.
#![allow(dead_code)]

#[path = r"E:\Distributed Trustworthy Mathematical Knowledge Network\experiments\v5-local-checks\guest-build-02\project\modules\native\checker\src\module_correspondence.rs"]
mod previous;
#[path = "../modules/native/checker/src/module_correspondence.rs"]
mod successor;

use serde_json::{json, Value};
use std::{any::Any, fs::{self, OpenOptions}, io::{Read, Write}, path::{Path, PathBuf}};

const ROOT: &str = r"E:\Distributed Trustworthy Mathematical Knowledge Network";
const CASES: [&str; 5] = ["base", "fusion", "fold_map", "fusion_map", "project_summary"];
const MAX_FILE: u64 = 2 * 1024 * 1024;

macro_rules! normalized {
    ($report:expr) => {{
        let r = $report;
        json!({"status": r.status,
            "groups": r.groups.into_iter().map(|g| json!({"owner":g.owner,
                "imported":g.imported,"export_name_indices":g.export_name_indices})).collect::<Vec<_>>(),
            "foundation_name_indices":r.foundation_name_indices,
            "body_hash_obligations":r.body_hash_obligations.into_iter().map(|b|
                json!({"universes":b.universes,"digest":b.digest,"expression":b.expression})).collect::<Vec<_>>(),
            "hash_verification_performed":r.hash_verification_performed,
            "mathematical_admission":r.mathematical_admission})
    }};
}

fn previous_call(input: &Value) -> Value {
    let c = &input["correspondence"];
    let groups: Vec<previous::GroupBinding> = serde_json::from_value(c["groups"].clone()).unwrap();
    let bodies: Vec<previous::BodyOpening> = serde_json::from_value(c["bodies"].clone()).unwrap();
    normalized!(previous::check_rows_correspondence_conditional(input["rows"].as_array().unwrap(),
        usize::try_from(c["foundation_rows"].as_u64().unwrap()).unwrap(), &groups, &bodies))
}

fn successor_call(input: &Value) -> Value {
    let c = &input["correspondence"];
    let groups: Vec<successor::GroupBinding> = serde_json::from_value(c["groups"].clone()).unwrap();
    let bodies: Vec<successor::BodyOpening> = serde_json::from_value(c["bodies"].clone()).unwrap();
    normalized!(successor::check_rows_correspondence_conditional(input["rows"].as_array().unwrap(),
        usize::try_from(c["foundation_rows"].as_u64().unwrap()).unwrap(), &groups, &bodies))
}

fn panic_text(payload: Box<dyn Any + Send>) -> String {
    if let Some(s) = payload.downcast_ref::<String>() { return s.clone(); }
    if let Some(s) = payload.downcast_ref::<&str>() { return (*s).to_owned(); }
    panic!("NONSTRING_PANIC_IS_NOT_AN_EXPECTED_REFUSAL");
}

fn outcome(input: &Value, call: fn(&Value) -> Value) -> Result<Value, String> {
    // Calls are sequential. Silence only the panic whose payload is captured;
    // restore ordinary diagnostics before the harness's own assertions.
    let hook = std::panic::take_hook();
    std::panic::set_hook(Box::new(|_| {}));
    let result = std::panic::catch_unwind(|| call(input));
    std::panic::set_hook(hook);
    result.map_err(panic_text)
}

fn save(path: &Path, value: &Value) {
    let bytes = serde_json::to_vec(value).unwrap();
    assert!(bytes.len() <= MAX_FILE as usize, "EVIDENCE_BYTE_BOUND");
    OpenOptions::new().write(true).create_new(true).open(path).unwrap().write_all(&bytes).unwrap();
}

fn compare(out: &Path, label: &str, input: &Value, refusal: Option<&str>) -> Value {
    let before = serde_json::to_vec(input).unwrap();
    let old = outcome(input, previous_call);
    let new = outcome(input, successor_call);
    assert_eq!(before, serde_json::to_vec(input).unwrap(), "INPUT_MUTATED");
    assert_eq!(old, new, "OLD_NEW_FULL_STRUCTURAL_RESULT_OR_REFUSAL_DIFFERENCE");
    let result = match (refusal, old) {
        (None, Ok(value)) => {
            assert_eq!(value["status"], "STRUCTURAL_CORRESPONDENCE_ONLY_UNVERIFIED_HASHES_AND_PREMISES");
            assert_eq!(value["hash_verification_performed"], false);
            assert_eq!(value["mathematical_admission"], false);
            json!({"label":label,"equal":true,"expected":"MATCHED_STRUCTURAL_DIAGNOSTIC",
                   "result":value,"mathematical_admission":false})
        },
        (Some(marker), Err(message)) => {
            assert!(message.contains(marker), "DIFFERENT_REFUSAL_BOUNDARY:{label}:{message}");
            json!({"label":label,"equal":true,"expected":"REFUSED","marker":marker,
                   "panic":message,"mathematical_admission":false})
        },
        _ => panic!("UNEXPECTED_ACCEPTANCE_OR_REFUSAL:{label}"),
    };
    save(&out.join(format!("{label}.input.json")), input);
    save(&out.join(format!("{label}.result.json")), &result);
    json!({"label":label,"equal":true,"expected":result["expected"],"mathematical_admission":false})
}

fn negatives(base: &Value) -> Vec<(&'static str, Value, &'static str)> {
    let mut result = Vec::new();
    let mut input = base.clone();
    input["correspondence"]["groups"][0]["descriptor"]["declarations"][0]["type"] = json!(["sort",["zero"]]);
    result.push(("descriptor-type",input,"CORRESPONDENCE_DECLARATION_TYPE"));

    let mut input = base.clone();
    input["correspondence"]["bodies"][0]["expression"] = json!(["sort",["zero"]]);
    result.push(("body-expression",input,"CORRESPONDENCE_BODY_EXPRESSION"));

    let mut input = base.clone();
    let universes = input["correspondence"]["groups"][0]["descriptor"]["declarations"][0]["universes"].as_u64().unwrap();
    input["correspondence"]["groups"][0]["descriptor"]["declarations"][0]["universes"] = json!(universes+1);
    result.push(("universe-count",input,"CORRESPONDENCE_UNIVERSES"));

    // The last theorem is the local binary_congr proof, not a foundation theorem.
    let rows = base["rows"].as_array().unwrap();
    let declaration = rows.iter().rposition(|row| row.get("thm").is_some()).unwrap();
    assert!(declaration >= base["correspondence"]["foundation_rows"].as_u64().unwrap() as usize);
    let proof = rows[declaration]["thm"]["value"].as_u64().unwrap();
    let expression = rows.iter().position(|row| row.get("ie").and_then(Value::as_u64)==Some(proof)).unwrap();
    let mut input = base.clone();
    input["rows"][expression] = json!({"ie":proof,"app":{"fn":proof,"arg":proof}});
    result.push(("proof-forward-backref",input,"CORRESPONDENCE_EXPRESSION_BACKREF"));

    assert!(rows[expression].get("lam").is_some(), "HELD_PROOF_LAMBDA_ROOT");
    let mut input = base.clone();
    input["rows"][expression]["lam"]["binderInfo"] = json!("invalid-binder");
    result.push(("proof-binder-style",input,"CORRESPONDENCE_BINDER_STYLE"));

    let mut input = base.clone();
    assert!(!rows[declaration]["thm"]["levelParams"].as_array().unwrap().is_empty());
    input["rows"][declaration]["thm"]["levelParams"][0] = rows[declaration]["thm"]["name"].clone();
    result.push(("unbound-level-parameter",input,"CORRESPONDENCE_UNBOUND_UNIVERSE"));
    result
}

fn run() {
    let args = std::env::args_os().collect::<Vec<_>>();
    assert_eq!(args.len(), 7, "OUTPUT_THEN_FIVE_EXACT_INPUT_PATHS");
    assert_eq!(std::env::current_dir().unwrap(), Path::new(ROOT));
    let out = PathBuf::from(&args[1]);
    assert!(out.is_absolute() && out.starts_with(Path::new(ROOT).join("experiments/v5-local-checks"))
        && !out.exists(), "FRESH_CANONICAL_OUTPUT");
    fs::create_dir(&out).unwrap();
    let mut results = Vec::new();
    let mut base = None;
    for (label, path) in CASES.into_iter().zip(&args[2..]) {
        let path = PathBuf::from(path);
        assert_eq!(path, Path::new(ROOT).join("experiments/v5-local-checks/receipt-prepare-01/prepared")
            .join(label).join("native.json"), "EXACT_RETAINED_WITNESS_PATH");
        let file = fs::File::open(path).unwrap();
        assert!(file.metadata().unwrap().len() <= MAX_FILE);
        let mut raw = Vec::new(); file.take(MAX_FILE+1).read_to_end(&mut raw).unwrap();
        assert!(raw.len() <= MAX_FILE as usize);
        let input: Value = serde_json::from_slice(&raw).unwrap();
        assert_eq!(input["schema"], "DMKN_V5_NATIVE_PREFLIGHT_V1");
        assert_eq!(input["mode"], "corresponding_module");
        assert_eq!(input["permitted_axioms"], json!([]));
        results.push(compare(&out,label,&input,None));
        if label=="base" { base=Some(input); }
    }
    for (label,input,marker) in negatives(&base.unwrap()) {
        results.push(compare(&out,label,&input,Some(marker)));
    }
    assert_eq!(results.len(),11);
    let report = json!({"schema":"DMKN_CORRESPONDENCE_MOVE_DIFFERENTIAL_V1",
        "status":"PASS_OLD_NEW_STRUCTURAL_EQUIVALENCE_ONLY","positive_cases":5,"negative_cases":6,
        "results":results,"kernel_calls":0,"proof_calls":0,"mathematical_admission":false,
        "scope":"EXACT_FULL_STRUCTURAL_OUTPUTS_AND_REFUSALS_NOT_RUNTIME_SPEEDUP"});
    save(&out.join("RESULT.json"),&report);
    println!("{report}");
}

fn main() {
    std::thread::Builder::new().name("constructor-differential".into())
        .stack_size(16 * 1024 * 1024).spawn(run).expect("HARNESS_THREAD")
        .join().expect("HARNESS_JOIN");
}
