//! Focused actual frontend old/new differential. No guest or parent proof call.
#![allow(dead_code, unused_imports)]

#[path = "E:/Distributed Trustworthy Mathematical Knowledge Network/experiments/v5-local-checks/guest-build-02/project/modules/receipt/src/canonical.rs"]
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
const CASES: [&str;5] = ["base","fusion","fold_map","fusion_map","project_summary"];
const TOP: [&str;7] = ["schema","image","rank","local_spec","rows","parents","bodies"];
const PARENT: [&str;2] = ["journal","openings"];
const BODY: [&str;3] = ["universes","digest","expression"];

fn read(path: &Path, maximum: u64) -> Vec<u8> {
    let file = fs::File::open(path).unwrap();
    assert!(file.metadata().unwrap().len() <= maximum);
    let mut raw = Vec::new(); file.take(maximum+1).read_to_end(&mut raw).unwrap();
    assert!(raw.len() <= maximum as usize); raw
}

fn save(path: &Path, value: &Value) {
    let raw = serde_json::to_vec(value).unwrap();
    OpenOptions::new().write(true).create_new(true).open(path).unwrap().write_all(&raw).unwrap();
}

fn normalized(value: input::Input) -> Value {
    let parents = value.parents.into_iter().map(|p| json!({"journal":p.journal,"openings":p.openings})).collect::<Vec<_>>();
    let bodies = value.bodies.into_iter().map(|b| json!({"universes":b.universes,"digest":b.digest,"expression":b.expression})).collect::<Vec<_>>();
    json!({"schema":value.schema,"image":value.image,"rank":value.rank,"local_spec":value.local_spec,
           "rows":value.rows,"parents":parents,"bodies":bodies})
}

fn compare_input(label: &str, value: Value, accept: bool, out: &Path) -> Value {
    // Same derive attributes/field order as the frozen predecessor. It remains
    // an independent serde conversion, not a second call to the new extractor.
    let old = serde_json::from_value::<input::Input>(value.clone()).map(normalized);
    let new = input::extract(value.clone()).map(normalized);
    assert_eq!(old.is_ok(),accept,"OLD_SHAPE_EXPECTATION:{label}");
    assert_eq!(new.is_ok(),accept,"NEW_SHAPE_EXPECTATION:{label}");
    let result = if accept {
        let old=old.unwrap(); let new=new.unwrap(); assert_eq!(old,new,"EXACT_EXTRACTED_FIELDS:{label}");
        json!({"label":label,"accepted_shape":true,"normalized":new})
    } else {
        json!({"label":label,"accepted_shape":false,"old_error":old.unwrap_err().to_string(),
               "new_error":new.unwrap_err(),"error_text_equality_required":false})
    };
    save(&out.join(format!("shape-{label}.json")),&json!({"input":value,"comparison":result}));
    json!({"label":label,"accepted_shape":accept,"equal":true})
}

fn positional(value: Value, fields: &[&str]) -> Value {
    let mut object=value.as_object().unwrap().clone();
    Value::Array(fields.iter().map(|key| object.remove(*key).unwrap()).collect())
}

fn synthetic() -> Value {
    json!({"schema":"shape-only-not-mathematical", "image":[0,1,2,3,4,5,6,4294967295u64],
        "rank":u64::MAX,"local_spec":{"arbitrary":[null,true,"text",{"nested":[0,7]}]},
        "rows":[null,[1,{"x":[false,"z"]}]],
        "parents":[{"journal":[0,255,1],"openings":[null,{"nested":["a",3]}]}],
        "bodies":[{"universes":256,"digest":"any shape-valid string","expression":[null,true,{"x":[2]}]}]})
}

fn shape_controls(out: &Path) -> Vec<Value> {
    let base=synthetic(); let mut results=Vec::new();
    for mask in 0..8 {
        let mut value=base.clone();
        if mask&2!=0 { value["parents"][0]=positional(value["parents"][0].clone(),&PARENT); }
        if mask&4!=0 { value["bodies"][0]=positional(value["bodies"][0].clone(),&BODY); }
        if mask&1!=0 { value=positional(value,&TOP); }
        results.push(compare_input(&format!("map-sequence-{mask}"),value,true,out));
    }
    for (record,keys) in [("top",TOP.as_slice()),("parent",PARENT.as_slice()),("body",BODY.as_slice())] {
        for key in keys {
            let mut value=base.clone();
            let target=match record {"top"=>&mut value,"parent"=>&mut value["parents"][0],_=>&mut value["bodies"][0]};
            target.as_object_mut().unwrap().remove(*key);
            results.push(compare_input(&format!("missing-{record}-{key}"),value,false,out));
        }
        let mut value=base.clone();
        let target=match record {"top"=>&mut value,"parent"=>&mut value["parents"][0],_=>&mut value["bodies"][0]};
        target.as_object_mut().unwrap().insert("extra".into(),Value::Null);
        results.push(compare_input(&format!("extra-{record}"),value,false,out));
        for short in [true,false] {
            let mut value=base.clone();
            let target=match record {"top"=>&mut value,"parent"=>&mut value["parents"][0],_=>&mut value["bodies"][0]};
            *target=positional(target.clone(),keys);
            if short { target.as_array_mut().unwrap().pop(); } else {target.as_array_mut().unwrap().push(Value::Null);}
            results.push(compare_input(&format!("arity-{record}-{}",if short {"short"} else {"long"}),value,false,out));
        }
    }
    for (label,pointer,bad) in [
        ("schema-number","/schema",json!(3)),("image-string","/image",json!("x")),
        ("image-short","/image",json!([0,1,2,3,4,5,6])),("image-long","/image",json!([0,1,2,3,4,5,6,7,8])),
        ("image-range","/image/0",json!(4294967296u64)),("image-negative","/image/0",json!(-1)),
        ("image-float","/image/0",json!(1.0)),("rank-string","/rank",json!("1")),
        ("rank-negative","/rank",json!(-1)),("rank-float","/rank",json!(1.0)),
        ("rows-object","/rows",json!({})),("parents-null","/parents",Value::Null),
        ("bodies-object","/bodies",json!({})),("parent-scalar","/parents/0",json!(true)),
        ("body-scalar","/bodies/0",json!(0)),("journal-string","/parents/0/journal",json!("abc")),
        ("journal-range","/parents/0/journal/0",json!(256)),("journal-negative","/parents/0/journal/0",json!(-1)),
        ("journal-float","/parents/0/journal/0",json!(1.0)),("openings-object","/parents/0/openings",json!({})),
        ("universes-string","/bodies/0/universes",json!("1")),("universes-negative","/bodies/0/universes",json!(-1)),
        ("universes-float","/bodies/0/universes",json!(1.0)),("digest-number","/bodies/0/digest",json!(1)),
    ] {
        let mut value=base.clone(); *value.pointer_mut(pointer).unwrap()=bad;
        results.push(compare_input(label,value,false,out));
    }
    for (label,value) in [("root-null",Value::Null),("root-string",json!("x")),("root-bool",json!(true)),("root-number",json!(1))] {
        results.push(compare_input(label,value,false,out));
    }
    let mut value=base.clone();value["bodies"][0]["universes"]=json!(u64::MAX);
    results.push(compare_input("universes-native-usize-max",value,usize::BITS==64,out));
    assert_eq!(results.len(),58); results
}

fn raw_control(label:&str, raw:Vec<u8>, accept:bool, results:&mut Vec<Value>) {
    let old=old_canonical::parse(&raw); let new=canonical::parse(&raw);
    let combined=canonical::parse_hashed("module-witness",&raw);
    assert_eq!(old.is_ok(),accept,"OLD_PARSE:{label}");
    assert_eq!(new.is_ok(),accept,"NEW_PARSE:{label}");
    assert_eq!(combined.is_ok(),accept,"NEW_PARSE_HASH:{label}");
    if accept {
        let old=old.unwrap(); assert_eq!(new.unwrap(),old);
        let (value,digest)=combined.unwrap();assert_eq!(value,old);
        assert_eq!(digest,old_canonical::hash("module-witness",&old).unwrap());
    }
    results.push(json!({"label":label,"accepted":accept,"equal":true,"input_bytes":raw.len()}));
}

fn canonical_controls(root:&Path,out:&Path) -> Vec<Value> {
    let mut results=Vec::new();
    let held=root.join("experiments/v5-local-checks/receipt-vectors-01/evidence");
    let vectors:Value=serde_json::from_slice(&read(&held.join("canonical-hashes.input.json"),65536)).unwrap();
    let expected:Value=serde_json::from_slice(&read(&held.join("canonical-hashes.stdout"),65536)).unwrap();
    for (index,case) in vectors.as_array().unwrap().iter().enumerate() {
        let domain=case["domain"].as_str().unwrap(); let value=&case["value"];
        assert_eq!(old_canonical::canonical(value).unwrap(),canonical::canonical(value).unwrap());
        let digest=canonical::hash(domain,value).unwrap();
        assert_eq!(digest,old_canonical::hash(domain,value).unwrap());
        assert_eq!(canonical::hex(&digest),expected["hashes"][index].as_str().unwrap());
        let (raw,doubled)=canonical::hash_with_canonical_sha(domain,value).unwrap();
        assert_eq!(raw,old_canonical::sha(&old_canonical::canonical(value).unwrap()));
        assert_eq!(doubled,digest);
        results.push(json!({"label":format!("held-cross-language-hash-{index}"),"equal":true}));
    }
    assert_eq!(results.len(),9);
    for (label,raw,accept) in [
        ("whitespace-and-order",b" {\"z\": [1,true,null], \"a\":0} \n".to_vec(),true),
        ("nested-duplicate",br#"{"x":{"a":1,"a":2}}"#.to_vec(),false),
        ("trailing-input",b"{}{}".to_vec(),false),
        ("negative",b"[-1]".to_vec(),false),
        ("float",b"[1.0]".to_vec(),false),
        ("exponent",b"[1e0]".to_vec(),false),
        ("overflow-u64",b"[18446744073709551616]".to_vec(),false),
        ("invalid-utf8",vec![b'"',255,b'"'],false),
        ("empty",Vec::new(),false),
    ] {raw_control(label,raw,accept,&mut results);}
    raw_control("parser-depth",[vec![b'[';130],vec![b'0'],vec![b']';130]].concat(),false,&mut results);
    raw_control("raw-byte-bound",vec![b' ';canonical::MAX_BYTES+1],false,&mut results);
    // This raw array has exactly MAX_NODES elements; its root exceeds the
    // global canonical node budget while remaining within the per-array cap.
    let mut raw=Vec::with_capacity(canonical::MAX_NODES*2+1);raw.push(b'[');
    for n in 0..canonical::MAX_NODES {if n!=0 {raw.push(b',');}raw.push(b'0');}
    raw.push(b']');raw_control("canonical-node-bound",raw,false,&mut results);
    let mut deep=Value::Null;for _ in 0..257 {deep=Value::Array(vec![deep]);}
    assert!(old_canonical::canonical(&deep).is_err() && canonical::canonical(&deep).is_err());
    results.push(json!({"label":"canonical-depth-bound","equal":true,"accepted":false}));
    let oversized=Value::String("x".repeat(canonical::MAX_BYTES));
    assert!(old_canonical::canonical(&oversized).is_err() && canonical::canonical(&oversized).is_err());
    results.push(json!({"label":"canonical-byte-bound","equal":true,"accepted":false}));
    for domain in ["x".repeat(129),"nonascii-π".into()] {
        assert!(old_canonical::hash(&domain,&Value::Null).is_err());
        assert!(canonical::hash(&domain,&Value::Null).is_err());
        assert!(canonical::hash_with_canonical_sha(&domain,&Value::Null).is_err());
        results.push(json!({"label":"invalid-domain","domain":domain,"equal":true,"accepted":false}));
    }
    save(&out.join("canonical-controls.json"),&json!(results)); results
}

fn run() {
    let args=std::env::args_os().collect::<Vec<_>>();assert_eq!(args.len(),2);
    let root=Path::new(ROOT);assert_eq!(std::env::current_dir().unwrap(),root);
    let out=PathBuf::from(&args[1]);assert!(out.is_absolute()&&out.starts_with(root.join("experiments/v5-local-checks"))&&!out.exists());
    fs::create_dir(&out).unwrap();let mut fixtures=Vec::new();
    for label in CASES {
        let held=root.join("experiments/v5-local-checks/receipt-prepare-01/prepared").join(label);
        let raw=read(&held.join("receipt-input.json"),2*1024*1024);
        let expected:Value=serde_json::from_slice(&read(&held.join("receipt-result.json"),65536)).unwrap();
        assert_eq!(expected["status"],"BOUND_RELATION_NATIVE_ONLY_PENDING_PARENT_PROOF_VERIFICATION");
        assert_eq!(expected["certificate_verification_performed"],false);
        let value=canonical::parse(&raw).unwrap();assert_eq!(value,old_canonical::parse(&raw).unwrap());
        compare_input(&format!("held-{label}"),value.clone(),true,&out);
        let old_hash=old_canonical::hash("module-witness",&value).unwrap();
        assert_eq!(canonical::hex(&old_hash),expected["witness"]);
        let expected_parents=value["parents"].as_array().unwrap().iter().map(|p|
            serde_json::from_value::<Vec<u8>>(p["journal"].clone()).unwrap()).collect::<Vec<_>>();
        let from_value=relation::check(value.clone()).unwrap();
        let from_bytes=relation::check_bytes(&raw).unwrap();
        assert_eq!(from_value.journal,from_bytes.journal);
        assert_eq!(from_value.parent_journals,from_bytes.parent_journals);
        assert_eq!(from_bytes.parent_journals,expected_parents);
        assert_eq!(json!(from_bytes.journal.encode().unwrap()),expected["journal"]);
        assert_eq!(from_bytes.journal.summary(),expected["summary"]);
        assert_eq!(from_bytes.parent_journals.len() as u64,expected["pending_parent_statements"].as_u64().unwrap());
        let prefix=Value::Array(value["rows"].as_array().unwrap()[..policy::FOUNDATION_ROWS].to_vec());
        let (raw_sha,domain_hash)=canonical::hash_with_canonical_sha("owner-workload-foundation-candidate",&prefix).unwrap();
        assert_eq!(raw_sha,old_canonical::sha(&old_canonical::canonical(&prefix).unwrap()));
        assert_eq!(domain_hash,old_canonical::hash("owner-workload-foundation-candidate",&prefix).unwrap());
        let result=json!({"label":label,"journal":from_bytes.journal.encode().unwrap(),
            "pending_parent_journals":from_bytes.parent_journals,"equal_held_journal":true,
            "equal_public_entries":true,"mathematical_admission":false});
        save(&out.join(format!("relation-{label}.json")),&result);fixtures.push(result);
    }
    let shapes=shape_controls(&out);let canonical=canonical_controls(root,&out);
    let result=json!({"schema":"DMKN_FRONTEND_DIFFERENTIAL_V1","status":"PASS_FRONTEND_EQUIVALENCE_NOT_GUEST_PROOF_OR_SPEEDUP",
        "held_relation_cases":5,"native_relation_calls":10,"shape_controls":shapes,
        "canonical_controls":canonical,"held_journals":fixtures,"guest_executions":0,"proof_calls":0,
        "network_calls":0,"certificate_verification_performed":false,"mathematical_admission":false});
    save(&out.join("RESULT.json"),&result);
    println!("PASS_FRONTEND_EQUIVALENCE_NOT_GUEST_PROOF_OR_SPEEDUP");
}

fn main() {
    std::thread::Builder::new().name("frontend-differential".into()).stack_size(16*1024*1024)
        .spawn(run).unwrap().join().unwrap();
}
