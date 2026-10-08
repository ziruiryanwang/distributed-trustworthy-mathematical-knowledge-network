//! Focused A1/A2 equivalence: no kernel checking, VM or proving.
#[path = "../modules/native/checker/src/lib.rs"] mod checker;
pub use checker::{debug_printer, demand, env, expr, inductive, level, module,
    module_correspondence, name, parser, pretty_printer, quot, tc, unique_hasher, util};
pub(crate) const STACK_SIZE: usize = 16_777_216;
#[path = "../modules/receipt/src/foundation_static.rs"] mod foundation_static;

use foundation_static::StaticValue;
use serde_json::{json, Value};
use std::{fs, path::Path, io::Write};

fn dynamic(value: &StaticValue) -> Value {
    match value {
        StaticValue::Null => Value::Null,
        StaticValue::Bool(v) => Value::Bool(*v),
        StaticValue::U64(v) => json!(v),
        StaticValue::String(v) => Value::String(std::str::from_utf8(v).unwrap().to_owned()),
        StaticValue::Array(v) => Value::Array(v.iter().map(dynamic).collect()),
        StaticValue::Object(v) => Value::Object(v.iter().map(|(key, value)|
            (std::str::from_utf8(key).unwrap().to_owned(), dynamic(value))).collect()),
    }
}

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
    assert_eq!(args.len(), 3);
    let fixtures = Path::new(&args[1]); let out = Path::new(&args[2]);
    assert!(fixtures.is_absolute() && fixtures.is_dir() && out.is_absolute() && !out.exists());
    fs::create_dir(out).unwrap();
    let mut counts = Vec::new();
    let mut foundation = None;
    for label in ["base", "fusion", "fold_map", "fusion_map", "project_summary"] {
        let raw = fs::read(fixtures.join(format!("diagnostic-{label}-input.json"))).unwrap();
        assert!(raw.len() <= 2*1024*1024);
        let input: Value = serde_json::from_slice(&raw).unwrap();
        let rows = input["rows"].as_array().unwrap();
        assert!(rows.len() >= 413 && foundation_static::matches_rows(&rows[..413]));
        for row in rows { assert!(compare(row)); }
        counts.push(json!({"label":label,"row_decoding_pairs":rows.len()}));
        if foundation.is_none() { foundation = Some(rows[..413].to_vec()); }
    }
    let foundation = foundation.unwrap();
    let reconstructed = dynamic(&foundation_static::ADOPTED_FOUNDATION);
    assert_eq!(reconstructed, Value::Array(foundation.clone()));
    let canonical = serde_json::to_vec(&reconstructed).unwrap();
    assert_eq!(canonical.len(), 23313);
    save(&out.join("reconstructed-foundation.json"), &canonical);
    let mut foundation_controls = 0;
    for index in 0..foundation.len() {
        let mut changed = foundation.clone(); changed[index] = Value::Null;
        assert!(!foundation_static::matches_rows(&changed)); foundation_controls += 1;
    }
    for changed in [foundation[..412].to_vec(), {
        let mut rows = foundation.clone(); rows.push(Value::Null); rows
    }] {
        assert!(!foundation_static::matches_rows(&changed)); foundation_controls += 1;
    }
    for (key, replacement) in [("meta", Value::Null), ("extra", json!(0))] {
        let mut changed = foundation.clone();
        changed[0].as_object_mut().unwrap().insert(key.to_owned(), replacement);
        assert!(!foundation_static::matches_rows(&changed)); foundation_controls += 1;
    }
    for replacement in [json!("4.34.0 "), json!(0), json!(false), Value::Null] {
        let mut changed = foundation.clone(); changed[0]["meta"]["lean"]["version"] = replacement;
        assert!(!foundation_static::matches_rows(&changed)); foundation_controls += 1;
    }
    let valid = vec![
        json!({"ie":0,"mdata":{"expr":0,"data":{"x":[1,true,null]}}}),
        json!({"ie":0,"natVal":"123456789012345678901234567890"}),
        json!({"ie":0,"strVal":"a\u{03b1}\0"}),
        json!({"ie":0,"const":[0,[]]}),
        json!({"ie":0,"app":{"fn":0,"arg":0,"ignored":true}}),
        json!({"In":1,"str":{"pre":0,"str":"alias"}}),
        json!({"Il":1,"succ":0}), json!({"Ie":0,"sort":0}),
        json!({"ie":0,"moduleImportTheorem":{"name":0,"levelParams":[],"type":0}}),
        json!({"quot":{"name":0,"levelParams":[],"type":0,"kind":"type"}}),
        json!({"opaque":{"name":0,"levelParams":[],"type":0,"value":0,"isUnsafe":false,"all":[0]}}),
        json!({"def":{"name":0,"levelParams":[],"type":0,"value":0,"safety":"safe","hints":"abbrev","all":[0]}}),
    ];
    for value in &valid { assert!(compare(value)); }
    // Old flatten Optional<BackRef> has a broad acceptance domain. The new
    // fallback must preserve it even when a later native apply_row would fail.
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
    let report = json!({"schema":"DMKN_STRUCTURAL_FRONTEND_DIFFERENTIAL_V1",
        "status":"PASS_EXACT_FOUNDATION_AND_OWNED_ROW_EQUIVALENCE_ONLY",
        "held_cases":counts,"foundation_refusals":foundation_controls,
        "extra_accepted_rows":valid.len(),"irregular_rows":irregular.len(),
        "irregular_accepted_by_both":irregular_success,"foundation_reconstructed_bytes":canonical.len(),
        "native_kernel_calls":0,"guest_executions":0,"proof_calls":0,
        "mathematical_admission":false,"speedup_measured":false});
    save(&out.join("RESULT.json"), &serde_json::to_vec(&report).unwrap());
    println!("{}", report);
}
