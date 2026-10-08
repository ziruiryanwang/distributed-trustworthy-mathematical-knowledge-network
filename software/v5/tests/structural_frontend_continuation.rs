//! Array-payload compatibility continuation; no native kernel, VM or proof.
#[path = "../modules/native/checker/src/lib.rs"] mod checker;
pub use checker::{debug_printer, demand, env, expr, inductive, level, module,
    module_correspondence, name, parser, pretty_printer, quot, tc, unique_hasher, util};
pub(crate) const STACK_SIZE: usize = 16_777_216;
use serde_json::{json, Value};
use std::{fs, path::Path, io::Write};

fn compare(value: &Value) -> bool {
    let old = parser::decode_owned_row(value.clone());
    let new = parser::decode_corresponded_owned_row(value.clone());
    match (old, new) {
        (Ok(a), Ok(b)) => { assert_eq!(a, b); true },
        (Err(_), Err(_)) => false,
        (a, b) => panic!("changed row-decoding success boundary: {value:?} old={a:?} new={b:?}"),
    }
}

fn save(path: &Path, bytes: &[u8]) {
    let mut file = fs::OpenOptions::new().write(true).create_new(true).open(path).unwrap();
    file.write_all(bytes).unwrap(); file.sync_all().unwrap();
}

fn main() {
    let args = std::env::args().collect::<Vec<_>>();
    assert_eq!(args.len(), 2);
    let out = Path::new(&args[1]);
    assert!(out.is_absolute() && !out.exists()); fs::create_dir(out).unwrap();
    // Earlier run reached the fourth extra after all five held cases,
    // foundation controls and first three extras. Do not repeat those checks.
    let remaining_valid = vec![
        json!({"ie":0,"const":[0,[]]}),
        json!({"ie":0,"app":{"fn":0,"arg":0,"ignored":true}}),
        json!({"In":1,"str":{"pre":0,"str":"alias"}}),
        json!({"Il":1,"succ":0}), json!({"Ie":0,"sort":0}),
        json!({"ie":0,"moduleImportTheorem":{"name":0,"levelParams":[],"type":0}}),
        json!({"quot":{"name":0,"levelParams":[],"type":0,"kind":"type"}}),
        json!({"opaque":{"name":0,"levelParams":[],"type":0,"value":0,"isUnsafe":false,"all":[0]}}),
        json!({"def":{"name":0,"levelParams":[],"type":0,"value":0,"safety":"safe","hints":"abbrev","all":[0]}}),
    ];
    for value in &remaining_valid { assert!(compare(value)); }
    // All six exercise the new array guard. Max/imax tuple variants must also
    // retain their native accepted representation through general fallback.
    let array_payloads = vec![
        json!({"il":0,"max":[0,1]}), json!({"il":0,"imax":[0,1]}),
        json!({"ie":0,"app":[0,1]}), json!({"ie":0,"letE":[0,0,0,0,false]}),
        json!({"in":0,"str":[0,"tail"]}),
        json!({"ie":0,"forallE":[0,0,0,"default"]}),
    ];
    let mut array_success = 0;
    for value in &array_payloads { array_success += usize::from(compare(value)); }
    assert!(array_success >= 2);
    // These 21 controls were never reached by the failed original run.
    let mut irregular = vec![Value::Null, json!([]), json!({}), json!({"unknown":0}),
        json!({"ie":0}), json!({"ie":0,"il":1,"sort":0}),
        json!({"ie":0,"sort":0,"unrelated":1}), json!({"ie":0,"app":{"fn":0}}),
        json!({"ie":0,"app":[0]}), json!({"ie":0,"app":[0,0,0]}),
        json!({"ie":0,"mdata":{"expr":0,"data":{"deep":[[null]]}}}),
        json!({"ie":0,"natVal":"not-a-natural"}), json!({"ie":0,"strVal":false}),
        json!({"ie":0,"bvar":65536}), json!({"ie":0,"const":{"name":4294967296u64,"us":[]}})];
    for index in [Value::Null, json!(false), json!(-1), json!(4294967296u64), json!("0"), json!(1.5)] {
        irregular.push(json!({"ie":index,"sort":0}));
    }
    let mut irregular_success = 0;
    for value in &irregular { irregular_success += usize::from(compare(value)); }
    let report = json!({"schema":"DMKN_STRUCTURAL_FRONTEND_CONTINUATION_V1",
        "status":"PASS_POSITIONAL_ARRAY_FALLBACK_AND_REMAINING_DECODER_CONTROLS",
        "prior_held_cases_reused":5,"prior_foundation_refusals_reused":421,
        "prior_extra_accepted_rows_reused":3,"remaining_accepted_rows":remaining_valid.len(),
        "array_payload_controls":array_payloads.len(),"array_accepted_by_both":array_success,
        "irregular_rows":irregular.len(),"irregular_accepted_by_both":irregular_success,
        "native_kernel_calls":0,"guest_executions":0,"proof_calls":0,
        "mathematical_admission":false,"speedup_measured":false});
    save(&out.join("RESULT.json"), &serde_json::to_vec(&report).unwrap());
    println!("{}", report);
}
