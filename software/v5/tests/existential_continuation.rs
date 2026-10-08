//! Profile2 changed-boundary checks. Synthetic projected journals are NOT receipts.
#![allow(dead_code, unused_imports)]

#[path = "E:/Distributed Trustworthy Mathematical Knowledge Network/experiments/v5-local-checks/guest-build-03/project/modules/receipt/src/canonical.rs"]
mod old_canonical;
#[path = "../modules/receipt/src/canonical.rs"] mod canonical;
#[path = "../modules/receipt/src/input.rs"] mod input;
#[path = "../modules/receipt/src/commitments.rs"] mod commitments;
#[path = "../modules/receipt/src/journal.rs"] mod journal;
#[path = "../modules/receipt/src/policy.rs"] mod policy;
#[path = "../modules/receipt/src/relation.rs"] mod relation;

use serde_json::{json, Value};
use std::{fs::{self, OpenOptions}, io::{Read, Write}, path::{Path, PathBuf}};

const ROOT: &str = "E:/Distributed Trustworthy Mathematical Knowledge Network";
const CASES: [&str; 5] = ["base", "fusion", "fold_map", "fusion_map", "project_summary"];

fn read(path: &Path, maximum: u64) -> Vec<u8> {
    let file = fs::File::open(path).unwrap();
    assert!(file.metadata().unwrap().len() <= maximum);
    let mut raw = Vec::new(); file.take(maximum + 1).read_to_end(&mut raw).unwrap();
    assert!(raw.len() <= maximum as usize); raw
}

fn save(path: &Path, value: &Value) {
    let raw = serde_json::to_vec(value).unwrap();
    OpenOptions::new().write(true).create_new(true).open(path).unwrap().write_all(&raw).unwrap();
}

// TEST ONLY semantic projection. No receipt is ever rewritten or accepted.
fn projection(old: &[u8]) -> Vec<u8> {
    assert_eq!(old.len(), 216); assert_eq!(&old[..8], b"DMKNM001");
    assert_eq!(&old[8..12], &1u32.to_le_bytes());
    let mut new = old[..184].to_vec();
    new[..8].copy_from_slice(b"DMKNM002"); new[8..12].copy_from_slice(&2u32.to_le_bytes());
    new
}

fn diagnostic_input(mut old: Value) -> Value {
    assert_eq!(old["schema"], "DMKN_CERTIFIED_MODULES_V1");
    old["schema"] = json!(journal::RELATION);
    for parent in old["parents"].as_array_mut().unwrap() {
        let bytes: Vec<u8> = serde_json::from_value(parent["journal"].clone()).unwrap();
        parent["journal"] = json!(projection(&bytes));
    }
    old
}

fn refused(value: Value) -> bool {
    match std::panic::catch_unwind(|| relation::check(value)) {
        Ok(result) => result.is_err(), Err(_) => true,
    }
}

fn size_case(label: &str, value: Value, accepted: bool, records: &mut Vec<Value>) {
    let encoded = old_canonical::canonical(&value);
    let measured = canonical::canonical_size(&value);
    assert_eq!(encoded.is_ok(), accepted, "emitter:{label}");
    assert_eq!(measured.is_ok(), accepted, "counter:{label}");
    if accepted { assert_eq!(encoded.unwrap().len(), measured.unwrap(), "length:{label}"); }
    records.push(json!({"label":label,"accepted":accepted,"exact_size_or_refusal_equal":true}));
}

fn raw_case(label: &str, bytes: Vec<u8>, accepted: bool, records: &mut Vec<Value>) {
    let old = old_canonical::parse(&bytes); let new = canonical::parse_validated(&bytes);
    assert_eq!(old.is_ok(), accepted, "parse:{label}");
    assert_eq!(new.is_ok(), accepted, "validated:{label}");
    if accepted { assert_eq!(old.unwrap(), new.unwrap(), "values:{label}"); }
    records.push(json!({"label":label,"accepted":accepted,"same_parse_domain":true}));
}

fn validation_controls() -> Vec<Value> {
    let mut records = Vec::new();
    for (label, value) in [
        ("null", Value::Null), ("true", json!(true)), ("false", json!(false)),
        ("zero", json!(0)), ("u64-max", json!(u64::MAX)),
        ("empty-array", json!([])), ("empty-object", json!({})), ("empty-string", json!("")),
        ("nested", json!({"z":[null,true,0,100],"a":{"x":[],"y":{}}})),
    ] { size_case(label, value, true, &mut records); }
    for power in 1..20 {
        let value = 10u64.pow(power);
        size_case(&format!("decimal-{power}"), json!([value-1,value]), true, &mut records);
    }
    for code in 0..=127 {
        let text = char::from_u32(code).unwrap().to_string();
        let mut map = serde_json::Map::new(); map.insert(text.clone(), json!([text.clone(),text]));
        size_case(&format!("ascii-key-value-{code}"), Value::Object(map), true, &mut records);
    }
    for text in ["π数学🧠", "\u{0080}\u{07ff}\u{0800}\u{ffff}\u{10000}\u{10ffff}", "\u{2028}\u{2029}", "/\\\"\n"] {
        let mut map = serde_json::Map::new(); map.insert(text.into(), json!(text));
        size_case(&format!("unicode-{}", records.len()), Value::Object(map), true, &mut records);
    }
    size_case("negative-value", json!(-1), false, &mut records);
    size_case("float-value", json!(1.0), false, &mut records);
    for (depth, accepted) in [(256,true),(257,false)] {
        let mut value = Value::Null; for _ in 0..depth { value = json!([value]); }
        size_case(&format!("value-depth-{depth}"), value, accepted, &mut records);
    }
    for (children, accepted) in [(canonical::MAX_NODES-1,true),(canonical::MAX_NODES,false)] {
        size_case(&format!("value-nodes-{}",children+1), Value::Array(vec![Value::Null; children]), accepted, &mut records);
    }
    for (length, accepted) in [(canonical::MAX_BYTES-2,true),(canonical::MAX_BYTES-1,false)] {
        size_case(&format!("string-canonical-bytes-{}",length+2), json!("x".repeat(length)), accepted, &mut records);
    }
    // Keys count bytes but NOT Value nodes; escaping can exceed raw UTF8 length.
    let mut map = serde_json::Map::new(); map.insert("\0".repeat(canonical::MAX_BYTES/6), Value::Null);
    size_case("escaped-key-byte-overflow", Value::Object(map), false, &mut records);
    for (label, bytes, accepted) in [
        ("whitespace-order", b" {\"z\":[1,true,null],\"a\":0}\n".to_vec(), true),
        ("escaped-unicode", br#"{"\u03c0":"\ud83e\udde0\/\u2028"}"#.to_vec(), true),
        ("duplicate", br#"{"x":{"a":1,"a":2}}"#.to_vec(), false),
        ("trailing", b"{}{}".to_vec(), false), ("negative", b"[-1]".to_vec(), false),
        ("float", b"[1.0]".to_vec(), false), ("exponent", b"[1e0]".to_vec(), false),
        ("u64-overflow", b"[18446744073709551616]".to_vec(), false),
        ("invalid-utf8", vec![b'"',255,b'"'], false),
        ("lone-surrogate", br#""\ud800""#.to_vec(), false), ("empty", Vec::new(), false),
    ] { raw_case(label, bytes, accepted, &mut records); }
    raw_case("parser-depth", [vec![b'[';130],vec![b'0'],vec![b']';130]].concat(), false, &mut records);
    raw_case("raw-byte-overflow", vec![b' ';canonical::MAX_BYTES+1], false, &mut records);
    let mut raw=Vec::with_capacity(canonical::MAX_NODES*2+1); raw.push(b'[');
    for i in 0..canonical::MAX_NODES { if i!=0 {raw.push(b',');} raw.push(b'0'); }
    raw.push(b']'); raw_case("parsed-global-node-overflow",raw,false,&mut records);
    records
}

fn intern_expression(rows: &mut Vec<Value>, expression: Value) -> u64 {
    // The accepted predecessor has one raw index per interned Expr. For these
    // three constructors, raw payload equality is exactly structural Expr
    // equality: binder presentation fields ARE included in native PartialEq.
    let mut next = 0;
    for row in rows.iter() {
        if let Some(index) = row.get("ie").and_then(Value::as_u64) {
            assert_eq!(index,next,"continuous_predecessor_expression_indices");
            next += 1;
            let mut payload=row.as_object().unwrap().clone(); payload.remove("ie");
            if Value::Object(payload)==expression { return index; }
        }
    }
    let mut row=expression.as_object().unwrap().clone(); row.insert("ie".into(),json!(next));
    rows.push(Value::Object(row)); next
}

fn alternate_theorem_proof(value: &Value) -> Value {
    // For closed theorem proof p:T, (fun h:T => h) p has the same type T.
    let mut changed=value.clone(); let rows=changed["rows"].as_array_mut().unwrap();
    let mut last=rows.pop().unwrap(); assert!(last.get("thm").is_some());
    let ty=last["thm"]["type"].as_u64().unwrap(); let proof=last["thm"]["value"].as_u64().unwrap();
    let variable=intern_expression(rows,json!({"bvar":0}));
    let lambda=intern_expression(rows,json!({"lam":{"name":0,"type":ty,"body":variable,"binderInfo":"default"}}));
    let applied=intern_expression(rows,json!({"app":{"fn":lambda,"arg":proof}}));
    assert_ne!(applied,proof,"genuinely_different_proof_root");
    last["thm"]["value"]=json!(applied); rows.push(last); changed
}

fn run() {
    let args=std::env::args_os().collect::<Vec<_>>(); assert_eq!(args.len(),2);
    let root=Path::new(ROOT); assert_eq!(std::env::current_dir().unwrap(),root);
    let out=PathBuf::from(&args[1]);
    assert!(out.is_absolute()&&out.starts_with(root.join("experiments/v5-local-checks"))&&!out.exists());
    fs::create_dir(&out).unwrap(); let mut reused=Vec::new(); let mut base=None;
    let prior=root.join("experiments/v5-local-checks/existential-differential-run-01/evidence");
    for label in CASES {
        let held=root.join("experiments/v5-local-checks/receipt-prepare-01/prepared").join(label);
        let old=canonical::parse(&read(&held.join("receipt-input.json"),2*1024*1024)).unwrap();
        let expected:Value=serde_json::from_slice(&read(&held.join("receipt-result.json"),65536)).unwrap();
        assert_eq!(expected["certificate_verification_performed"],false);
        let old_journal:Vec<u8>=serde_json::from_value(expected["journal"].clone()).unwrap();
        let value=canonical::parse(&read(&prior.join(format!("diagnostic-{label}-input.json")),2*1024*1024)).unwrap();
        assert_eq!(value,diagnostic_input(old.clone()),"exact_prior_saved_input");
        // Its save was reached only after the frozen predecessor's mathematical
        // assertions. Independent actual audit adopts those scoped successes.
        // This continuation does NOT repeat any of those five native calls.
        if label=="base" { base=Some((value,journal::Journal::decode(&projection(&old_journal)).unwrap(),old)); }
        reused.push(json!({"label":label,"reuse":"PRIOR_AUDITED_ASSERTIONS_BEFORE_FIXTURE_FAILURE","new_native_call":false}));
    }
    let (base,expected,old)=base.unwrap();
    assert_eq!(relation::check(base.clone()).unwrap().journal,expected);
    let alternate=alternate_theorem_proof(&base);
    assert_ne!(canonical::canonical(&base).unwrap(),canonical::canonical(&alternate).unwrap());
    assert_eq!(relation::check(alternate.clone()).unwrap().journal,expected);
    save(&out.join("alternate-valid-proof-input.json"),&alternate);
    let mut refusals=Vec::new();
    assert!(refused(old)); refusals.push("old-relation-profile");
    let mut bad=base.clone(); bad["rank"]=json!(1); assert!(refused(bad)); refusals.push("wrong-rank");
    let mut bad=base.clone(); bad["rows"][0]["extra"]=json!(0); assert!(refused(bad)); refusals.push("foundation-mutation");
    let mut bad=base.clone(); bad["bodies"][0]["expression"]=Value::Null; assert!(refused(bad)); refusals.push("body-mutation");
    let mut bad=base.clone(); bad.as_object_mut().unwrap().insert("extra".into(),Value::Null); assert!(refused(bad)); refusals.push("input-shape");
    let mut bad=base.clone(); let last=bad["rows"].as_array_mut().unwrap().last_mut().unwrap();
    last["thm"]["value"]=last["thm"]["type"].clone(); assert!(refused(bad)); refusals.push("false-local-proof");
    let good=expected.encode().unwrap();
    for mode in ["profile","magic","trailing","short"] {
        let mut bad=good.clone();
        match mode {"profile"=>bad[8]=1,"magic"=>bad[7]=b'1',"trailing"=>bad.push(0),_=>{bad.pop();}}
        assert!(journal::Journal::decode(&bad).is_err());
    }
    let controls=validation_controls();
    let result=json!({"schema":"DMKN_EXISTENTIAL_PROFILE2_CONTINUATION_V1",
        "status":"PASS_PROFILE2_CONTINUATION_NOT_GUEST_PROOF_OR_SPEEDUP",
        "held_projected_cases_reused":reused,"alternate_checked_proof_same_conclusion":true,
        "value_and_byte_entry_agree_on_base":true,"relation_calls":8,
        "native_checker_reached_calls":3,"relation_refusals":refusals,
        "journal_layout_refusals":4,"validation_controls":controls,
        "old_journal_projection_is_test_only":true,"guest_executions":0,"proof_calls":0,
        "certificate_verification_performed":false,"mathematical_admission":false});
    save(&out.join("RESULT.json"),&result);
    println!("PASS_PROFILE2_CONTINUATION_NOT_GUEST_PROOF_OR_SPEEDUP");
}

fn main() {
    std::thread::Builder::new().name("existential-differential".into()).stack_size(16*1024*1024)
        .spawn(run).unwrap().join().unwrap();
}
