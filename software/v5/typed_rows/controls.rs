//! Finite representation differentials. No guest, receipt, network or prover.
//! Retained positive integration is mandatory and requires three pinned files.
use crate::{census, old_census, Census};
use dmkn_module_relation::{canonical as C, decode::{self, DecodeOutcome, HybridFrame},
    legacy_relation, policy, relation::{self as module_relation, Prepared}};
use nanoda_lib::{parser::{decode_corresponded_owned_row, decode_typed_dag_row}, typed_rows::Row};
use serde_json::{json, Value};

fn raw_frame(suffix: &str) -> Vec<u8> {
    let prefix = vec!["null"; policy::FOUNDATION_ROWS].join(",");
    let suffix = if suffix.is_empty() { String::new() } else { format!(",{suffix}") };
    format!(r#"{{"schema":"shape-only","image":[0,0,0,0,0,0,0,0],"rank":0,"local_spec":{{}},"rows":[{prefix}{suffix}],"parents":[],"bodies":[]}}"#).into_bytes()
}

fn typed(raw: &[u8]) -> HybridFrame {
    match decode::decode(raw) {
        DecodeOutcome::Typed(frame) => frame,
        DecodeOutcome::UnsupportedRepresentation => panic!("expected typed syntax selection"),
    }
}

fn same_counts(raw: &[u8]) -> HybridFrame {
    let candidate = typed(raw);
    let old = C::parse_bounded(raw).unwrap();
    assert_eq!((candidate.nodes(), candidate.maximum_depth()),
        (old.nodes(), old.maximum_depth()));
    let rows = old.as_value()["rows"].as_array().unwrap();
    assert_eq!(candidate.rows_len(), rows.len());
    for (index, row) in candidate.rows().iter().enumerate() {
        if let Row::Legacy(value) = row { assert_eq!(value, &rows[index]); }
    }
    for key in ["schema", "image", "rank", "local_spec", "parents", "bodies"] {
        assert_eq!(candidate.field(key), old.as_value().get(key));
    }
    candidate
}

fn legacy(raw: &[u8]) {
    assert!(matches!(decode::decode(raw), DecodeOutcome::UnsupportedRepresentation));
    match module_relation::prepare(raw).unwrap() {
        Prepared::Legacy(value) => assert_eq!(value.as_value(), C::parse_bounded(raw).unwrap().as_value()),
        Prepared::Typed(_) => panic!("unsupported shape must select old parse token"),
    }
}

#[test]
fn all_fourteen_direct_native_maps_and_virtual_counts_match() {
    let cases = [
        (r#"{"in":1,"str":{"pre":0,"str":"a\u00e9\uD83D\uDE42"}}"#, 5, 2),
        (r#"{"num":{"i":4294967295,"pre":0},"in":1}"#, 5, 2),
        (r#"{"il":1,"succ":0}"#, 3, 1),
        (r#"{"param":0,"il":1}"#, 3, 1),
        (r#"{"il":1,"max":[0,0]}"#, 5, 2),
        (r#"{"imax":[0,0],"il":1}"#, 5, 2),
        (r#"{"ie":0,"bvar":65535}"#, 3, 1),
        (r#"{"sort":0,"ie":0}"#, 3, 1),
        (r#"{"ie":0,"const":{"name":1,"us":[]}}"#, 5, 2),
        (r#"{"app":{"arg":0,"fn":0},"ie":1}"#, 5, 2),
        (r#"{"ie":1,"lam":{"name":0,"type":0,"body":0,"binderInfo":"default"}}"#, 7, 2),
        (r#"{"forallE":{"binderInfo":"implicit","body":0,"type":0,"name":0},"ie":1}"#, 7, 2),
        (r#"{"ie":1,"letE":{"name":0,"type":0,"value":0,"body":0,"nondep":false}}"#, 8, 2),
        (r#"{"proj":{"struct":0,"idx":0,"typeName":0},"ie":1}"#, 6, 2),
    ];
    for (row, nodes, depth) in cases {
        let frame = same_counts(&raw_frame(row));
        let value = C::parse_bounded(row.as_bytes()).unwrap();
        assert_eq!((value.nodes(), value.maximum_depth()), (nodes, depth));
        let Row::Dag(dag) = frame.rows().last().unwrap() else { panic!("DAG selected"); };
        let expected = decode_corresponded_owned_row(value.as_value().clone()).unwrap();
        assert_eq!(decode_typed_dag_row(dag.clone()), expected);
    }
    for style in ["default", "implicit", "strictImplicit", "instImplicit"] {
        for tag in ["lam", "forallE"] {
            let row = format!(r#"{{"ie":1,"{tag}":{{"name":0,"type":0,"body":0,"binderInfo":"{style}"}}}}"#);
            let frame = same_counts(&raw_frame(&row));
            let Row::Dag(dag) = frame.rows().last().unwrap() else { unreachable!() };
            assert_eq!(decode_typed_dag_row(dag.clone()),
                decode_corresponded_owned_row(C::parse_bounded(row.as_bytes()).unwrap().as_value().clone()).unwrap());
        }
    }
    for row in [format!(r#"{{"ie":0,"proj":{{"typeName":0,"idx":{},"struct":0}}}}"#, usize::MAX),
        r#"{"ie":0,"letE":{"name":0,"type":0,"value":0,"body":0,"nondep":true}}"#.into(),
        r#"{"const":{"us":[0,1,2],"name":0},"ie":0}"#.into()] {
        let frame = same_counts(&raw_frame(&row));
        let Row::Dag(dag) = frame.rows().last().unwrap() else { unreachable!() };
        assert_eq!(decode_typed_dag_row(dag.clone()),
            decode_corresponded_owned_row(C::parse_bounded(row.as_bytes()).unwrap().as_value().clone()).unwrap());
    }
}

#[test]
fn retained_declaration_metadata_and_unreached_semantics_are_not_prevalidated() {
    let row = r#"{"inductive":{"all":[{"meta":[1,{"x":true}]}],"anything":null}}"#;
    let frame = same_counts(&raw_frame(row));
    assert!(matches!(frame.rows().last(), Some(Row::Legacy(_))));
    // Syntactically bounded universes may exceed the reached-only semantic cap.
    let levels = vec!["0"; 257].join(",");
    let raw = raw_frame(&format!(r#"{{"ie":0,"const":{{"name":0,"us":[{levels}]}}}}"#));
    let frame = same_counts(&raw);
    assert!(matches!(frame.rows().last(), Some(Row::Dag(_))));
    let mut value = C::parse_bounded(&raw).unwrap().as_value().clone();
    value["image"] = json!(false);
    value["parents"] = json!([{"journal":false,"openings":[]}]);
    value["bodies"] = json!([{"universes":false,"digest":null,"expression":{}}]);
    same_counts(&serde_json::to_vec(&value).unwrap());
}

#[test]
fn strict_raw_errors_refuse_and_supported_widths_fallback_without_coercion() {
    for row in [
        r#"{"ie":0,"\u0069e":1,"bvar":0}"#,
        r#"{"ie":0,"app":{"fn":0,"\u0066n":0,"arg":0}}"#,
        r#"{"ie":0,"bvar":-0}"#, r#"{"ie":0,"bvar":-1}"#,
        r#"{"ie":0,"bvar":1.0}"#, r#"{"ie":0,"bvar":1e0}"#,
        r#"{"in":1,"str":{"pre":0,"str":"\uD800"}}"#,
    ] {
        let raw = raw_frame(row);
        assert!(matches!(decode::decode(&raw), DecodeOutcome::UnsupportedRepresentation));
        assert!(C::parse_bounded(&raw).is_err());
        assert!(module_relation::prepare(&raw).is_err());
    }
    for row in [r#"{"ie":0,"bvar":65536}"#, r#"{"ie":4294967296,"sort":0}"#,
        r#"{"in":1,"num":{"pre":0,"i":4294967296}}"#,
        r#"{"ie":0,"const":{"name":0,"us":[4294967296]}}"#,
        r#"{"ie":0,"sort":true}"#, r#"{"ie":0,"max":[0,0]}"#,
        r#"{"ie":0,"lam":{"name":0,"type":0,"body":0,"binderInfo":"other"}}"#] {
        legacy(&raw_frame(row));
    }
    let raw = raw_frame(r#"{"ie":0,"bvar":0}"#);
    let mut extra = raw.clone(); extra.extend_from_slice(b" null");
    let mut utf8 = raw.clone(); utf8[11] = 255;
    for bad in [Vec::new(), raw[..raw.len()-1].to_vec(), extra, utf8] {
        assert!(matches!(decode::decode(&bad), DecodeOutcome::UnsupportedRepresentation));
        assert!(module_relation::prepare(&bad).is_err());
    }
}

#[test]
fn default_recursion_limit_and_decoded_duplicates_match_old_parser() {
    let base = String::from_utf8(raw_frame("" )).unwrap();
    for depth in [1, 120, 125, 126, 127, 128] {
        let nested = format!("{}0{}", "[".repeat(depth), "]".repeat(depth));
        let raw = base.replace("\"local_spec\":{}", &format!("\"local_spec\":{nested}")).into_bytes();
        let old = C::parse_bounded(&raw);
        assert_eq!(matches!(decode::decode(&raw), DecodeOutcome::Typed(_)), old.is_ok());
        if old.is_ok() { same_counts(&raw); }
    }
    for replacement in [r#""local_spec":{"x":0,"\u0078":1}"#,
        r#""local_spec":{},"\u0072ows":[]"#] {
        let raw = base.replace("\"local_spec\":{}", replacement).into_bytes();
        assert!(C::parse_bounded(&raw).is_err());
        assert!(module_relation::prepare(&raw).is_err());
    }
}

fn state(c: &Census) -> [usize; 6] {
    [c.rows,c.bodies,c.openings,c.parent_edges,c.nodes,c.maximum_depth]
}
fn old_state(c: &old_census::Census) -> [usize; 6] {
    [c.rows,c.bodies,c.openings,c.parent_edges,c.nodes,c.maximum_depth]
}
fn seed(c: &Census) -> old_census::Census {
    old_census::Census { rows:c.rows,bodies:c.bodies,openings:c.openings,
        parent_edges:c.parent_edges,nodes:c.nodes,maximum_depth:c.maximum_depth }
}
fn charge(raw: &[u8], new: &mut Census, old: &mut old_census::Census) {
    let a=old.charge(raw); let b=new.charge(raw);
    assert_eq!(a.is_ok(), b.is_ok());
    assert_eq!(a.err(), b.err(), "same first refusal");
    assert_eq!(state(new), old_state(old), "including partial mutation on refusal");
}

#[test]
fn aggregate_charge_order_including_partial_failures_is_exact() {
    let mut value=C::parse_bounded(&raw_frame(r#"{"ie":0,"bvar":0}"#)).unwrap().as_value().clone();
    value["parents"]=json!([{"journal":[],"openings":[{},{}]}]);
    value["bodies"]=json!([{}]);
    let raw=serde_json::to_vec(&value).unwrap();
    let nodes=C::parse_bounded(&raw).unwrap().nodes();
    let maxima=[census::MAX_ROWS,census::MAX_BODIES,census::MAX_OPENINGS,crate::relation::MAX_EDGES,census::MAX_NODES];
    let costs=[policy::FOUNDATION_ROWS+1,1,2,1,nodes];
    for index in 0..5 {
        for extra in [0,1,usize::MAX] {
            let mut new=Census::default();
            let initial=if extra==usize::MAX {usize::MAX} else {maxima[index]-costs[index]+extra};
            match index {0=>new.rows=initial,1=>new.bodies=initial,2=>new.openings=initial,
                3=>new.parent_edges=initial,_=>new.nodes=initial};
            let mut old=seed(&new); charge(&raw,&mut new,&mut old);
        }
    }
    let mut cases=vec![value.clone()];
    let mut malformed=value.clone(); malformed["image"]=json!(false);cases.push(malformed);
    for key in ["rows","parents","bodies"] {let mut v=value.clone();v[key]=json!(false);cases.push(v);}
    let mut missing=value.clone();missing.as_object_mut().unwrap().remove("rows");cases.push(missing);
    let mut extra=value.clone();extra["unexpected"]=json!(0);cases.push(extra);
    let mut parent=value.clone();parent["parents"]=json!([{"journal":[],"openings":[{}]},{"journal":[]}]);cases.push(parent);
    let mut new=Census::default();let mut old=seed(&new);
    for case in cases {charge(&serde_json::to_vec(&case).unwrap(),&mut new,&mut old);}
}

#[test]
fn unsupported_shapes_use_legacy_and_typed_semantic_errors_do_not_retry() {
    let mut value=C::parse_bounded(&raw_frame(r#"{"ie":0,"bvar":0}"#)).unwrap().as_value().clone();
    let keys=["schema","image","rank","local_spec","rows","parents","bodies"];
    let positional=Value::Array(keys.iter().map(|key|value[*key].clone()).collect());
    legacy(&serde_json::to_vec(&positional).unwrap());
    for row in [r#"[0,0]"#,r#"{"ie":0,"unknown":0}"#,r#"{"ie":0,"bvar":0,"extra":0}"#] {
        legacy(&raw_frame(row));
    }
    for schema in ["shape-only", dmkn_module_relation::journal::RELATION] {
        value["schema"]=json!(schema);
        let raw=serde_json::to_vec(&value).unwrap();
        assert!(matches!(module_relation::prepare(&raw).unwrap(),Prepared::Typed(_)));
        let old=legacy_relation::check_bytes(&raw).err().expect("invalid schema/foundation");
        let new=module_relation::check_bytes(&raw).err().expect("same semantic refusal");
        assert_eq!(old,new);
        assert_eq!(new,if schema=="shape-only" {"relation schema/limits"} else {"exact adopted foundation values"});
    }
}

fn fixture(name: &str, maximum: u64, digest: &str) -> Vec<u8> {
    let path=std::env::var_os(name).expect("required retained fixture path absent");
    let metadata=std::fs::metadata(&path).unwrap();
    assert!(metadata.is_file() && metadata.len()<=maximum);
    let bytes=std::fs::read(path).unwrap();
    assert_eq!(C::hex(&C::sha(&bytes)),digest,"retained fixture identity");
    bytes
}

#[test]
fn retained_two_frames_select_typed_and_match_actual_legacy_conclusions() {
    let bytes=fixture("DMKN_TYPED_PACKET",1_000_000,
        "54c7dac7f83a9a06c2b23b17a77be20364c1b90e4cd3b1db58b69c62fda2dcf1");
    let packet:Value=serde_json::from_slice(&bytes).unwrap();
    let deltas=packet["deltas"].as_array().unwrap();assert_eq!(deltas.len(),2);
    let mut census=Census::default();let mut old_census=old_census::Census::default();
    for (index,delta) in deltas.iter().enumerate() {
        let raw=serde_json::to_vec(delta).unwrap();let token=same_counts(&raw);
        let typed_count=token.rows().iter().filter(|r|matches!(r,Row::Dag(_))).count();
        assert_eq!(typed_count,[930,583][index]);
        assert_eq!(token.rows_len(),[1355,1009][index]);
        let old=legacy_relation::check_bytes(&raw).expect("retained old-valid module");
        let new=module_relation::check_bytes(&raw).expect("typed module must retain acceptance");
        assert_eq!(old.journal.encode().unwrap(),new.journal.encode().unwrap());
        assert_eq!(old.parent_journals,new.parent_journals);
        charge(&raw,&mut census,&mut old_census);
    }
    assert_eq!(state(&census),[2364,22,23,3,29858,28]);
}

#[test]
fn retained_aggregate_matches_exact_saved_oracle_without_old_graph_rebuild() {
    let input=fixture("DMKN_TYPED_AGGREGATE_INPUT",300_000,
        "7e21d092206b08a9a71231045b8152df4179ee6575cdc5e3afc704ef03c0be58");
    let expected=fixture("DMKN_TYPED_AGGREGATE_EXPECTED",10_000,
        "01d7c9cc45a16f520980e80672f90c0a97a69e31e344f748910df5abb24ffd0b");
    let old:Value=serde_json::from_slice(&expected).unwrap();
    let new=dmkn_aggregate_relation::relation::check_bytes(&input).unwrap();
    assert_eq!(old["header"],json!(new.header().encode().unwrap()));
    assert_eq!(old["assumptions"],json!(new.assumptions().iter().map(|a|
        json!({"image":a.image(),"journal":a.journal()})).collect::<Vec<_>>()));
    let journals:Vec<Value>=old["members"].as_array().unwrap().iter().map(|m|m["journal"].clone()).collect();
    assert_eq!(json!(journals),json!(new.members()));
    let c=new.census();
    assert_eq!(old["census"],json!({"rows":c.rows,"bodies":c.bodies,"openings":c.openings,
        "parent_edges":c.parent_edges,"nodes":c.nodes,"maximum_depth":c.maximum_depth}));
    assert_eq!(old["edges"],json!(new.edges()));
    assert_eq!(old["wire_bytes"],json!(new.wire_bytes()));
    assert_eq!(old["mathematical_admission"],false);
}
