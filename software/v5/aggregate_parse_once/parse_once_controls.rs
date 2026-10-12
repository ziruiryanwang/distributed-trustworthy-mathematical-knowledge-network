//! Changed-boundary differential controls only. Existing graph/Merkle controls
//! are compiled but need not be rerun. Mathematical fixtures are supplied by the
//! separately selected retained-packet native comparison, not invented here.
use crate::{census, reference_census, Census};
use dmkn_module_relation::{canonical::{parse_validated, R}, relation as module_relation};
use serde_json::{json, Value};
use std::panic::{catch_unwind, AssertUnwindSafe};

fn reference(value: &Census) -> reference_census::Census {
    reference_census::Census {
        rows: value.rows, bodies: value.bodies, openings: value.openings,
        parent_edges: value.parent_edges, nodes: value.nodes,
        maximum_depth: value.maximum_depth,
    }
}

fn state(value: &Census) -> [usize; 6] {
    [value.rows, value.bodies, value.openings, value.parent_edges, value.nodes, value.maximum_depth]
}

fn reference_state(value: &reference_census::Census) -> [usize; 6] {
    [value.rows, value.bodies, value.openings, value.parent_edges, value.nodes, value.maximum_depth]
}

fn charge_pair(bytes: &[u8], before: &mut reference_census::Census, after: &mut Census) -> bool {
    let old = before.charge(bytes);
    let new = after.charge(bytes);
    assert_eq!(old, new.as_ref().map(|_| ()).map_err(Clone::clone));
    assert_eq!(reference_state(before), state(after), "failed-prefix census also must agree");
    if let Ok(value) = new {
        assert_eq!(value, parse_validated(bytes).unwrap(), "returned Value was not mutated");
        true
    } else {
        false
    }
}

fn shaped() -> Value {
    json!({"schema":"shape-only", "image":[0,0,0,0,0,0,0,0], "rank":0,
        "local_spec":{}, "rows":[0,1],
        "parents":[{"journal":[],"openings":[{},{}]}], "bodies":[{}]})
}

type Binding = (Vec<u8>, Vec<Vec<u8>>);

#[derive(Debug, PartialEq, Eq)]
enum Outcome { Returned(R<Binding>), Panicked(String) }

fn observe(f: impl FnOnce() -> R<module_relation::RelationConclusion>) -> Outcome {
    match catch_unwind(AssertUnwindSafe(|| {
        let conclusion = f()?;
        Ok((conclusion.journal.encode()?, conclusion.parent_journals))
    })) {
        Ok(value) => Outcome::Returned(value),
        Err(payload) => Outcome::Panicked(payload.downcast_ref::<String>().cloned()
            .or_else(|| payload.downcast_ref::<&str>().map(|text| (*text).to_owned()))
            .unwrap_or_else(|| "non-string panic".into())),
    }
}

#[test]
fn named_positional_and_noncanonical_spellings_return_exact_value() {
    let positional = json!(["shape-only", [0,0,0,0,0,0,0,0], 0, {}, [0,1],
        [[[],[{},{}]]], [{}]]);
    let mut spellings = vec![serde_json::to_vec(&shaped()).unwrap(),
        serde_json::to_vec(&positional).unwrap()];
    spellings.push(br#" { "bodies" : [ {} ], "parents" : [ { "openings" : [{},{}], "journal" : [] } ],
        "rows" : [0,1], "local_spec" : {}, "rank" : 0, "image" : [0,0,0,0,0,0,0,0],
        "schema" : "shape\u002donly" } "#.to_vec());
    for bytes in spellings {
        let mut before = reference_census::Census::default();
        let mut after = Census::default();
        assert!(charge_pair(&bytes, &mut before, &mut after));
        assert_eq!((after.rows, after.bodies, after.openings, after.parent_edges), (2,1,2,1));
    }
}

#[test]
fn strict_parse_refusals_preserve_unmodified_initial_census() {
    let malformed: &[&[u8]] = &[
        b"", br#"{"rows":[],"rows":[]}"#, br#"{"x":{"a":0,"a":1}}"#,
        b"[1.5]", b"[-1]", b"[18446744073709551616]", b"[] true", b"[",
        b"[\"\xFF\"]", br#"["\uD800"]"#,
    ];
    let seed = Census { rows:1, bodies:2, openings:3, parent_edges:4, nodes:5, maximum_depth:6 };
    for bytes in malformed {
        let mut before = reference(&seed); let mut after = seed.clone();
        assert!(!charge_pair(bytes, &mut before, &mut after));
        assert_eq!(state(&after), state(&seed));
    }
    let over_bytes = vec![b' '; dmkn_module_relation::canonical::MAX_BYTES + 1];
    let mut before = reference(&seed); let mut after = seed.clone();
    assert!(!charge_pair(&over_bytes, &mut before, &mut after));
    assert_eq!(state(&after), state(&seed));
}

#[test]
fn shape_and_depth_failures_preserve_partial_census_state() {
    let mut missing = shaped(); missing.as_object_mut().unwrap().remove("rows");
    let mut extra = shaped(); extra["unexpected"] = json!(0);
    let mut wrong_rows = shaped(); wrong_rows["rows"] = json!({});
    let mut wrong_parent = shaped(); wrong_parent["parents"] = json!([{"journal":[]}]);
    let mut wrong_openings = shaped(); wrong_openings["parents"][0]["openings"] = json!(false);
    let values = vec![json!(null), json!([]), missing, extra, wrong_rows, wrong_parent, wrong_openings];
    for value in values {
        let mut before = reference_census::Census::default(); let mut after = Census::default();
        assert!(!charge_pair(&serde_json::to_vec(&value).unwrap(), &mut before, &mut after));
    }
    // Do not claim serde's own recursion boundary equals MAX_DEPTH. The same
    // exact raw parser remains responsible for its earlier refusal if any.
    for depth in [0, 64, 126, 128, 129, 192] {
        let nested = format!("{}0{}", "[".repeat(depth), "]".repeat(depth));
        let bytes = format!(concat!("{{\"schema\":\"shape-only\",\"image\":[],\"rank\":0,",
            "\"rows\":[],\"parents\":[],\"bodies\":[],\"local_spec\":{}}}"), nested).into_bytes();
        let mut before = reference_census::Census::default(); let mut after = Census::default();
        charge_pair(&bytes, &mut before, &mut after);
    }
}

#[test]
fn cumulative_caps_overflow_and_success_then_refusal_match() {
    let bytes = serde_json::to_vec(&shaped()).unwrap();
    let seeds = [
        Census { rows:census::MAX_ROWS, ..Census::default() },
        Census { bodies:census::MAX_BODIES, ..Census::default() },
        Census { openings:census::MAX_OPENINGS, ..Census::default() },
        Census { parent_edges:crate::relation::MAX_EDGES, ..Census::default() },
        Census { nodes:census::MAX_NODES, ..Census::default() },
        Census { rows:usize::MAX, ..Census::default() },
        Census { bodies:usize::MAX, ..Census::default() },
        Census { openings:usize::MAX, ..Census::default() },
        Census { parent_edges:usize::MAX, ..Census::default() },
        Census { nodes:usize::MAX, ..Census::default() },
    ];
    for seed in seeds {
        let mut before = reference(&seed); let mut after = seed;
        assert!(!charge_pair(&bytes, &mut before, &mut after));
    }
    let mut after = Census { rows:census::MAX_ROWS - 2, ..Census::default() };
    let mut before = reference(&after);
    assert!(charge_pair(&bytes, &mut before, &mut after));
    assert_eq!(after.rows, census::MAX_ROWS);
    assert!(!charge_pair(&bytes, &mut before, &mut after));
}

#[test]
fn public_value_entry_preserves_early_relation_refusals_and_census() {
    let object = shaped();
    let positional = json!(["shape-only", [0,0,0,0,0,0,0,0], 0, {}, [0,1],
        [[[],[{},{}]]], [{}]]);
    for value in [object, positional] {
        let bytes = serde_json::to_vec(&value).unwrap();
        let mut before = reference_census::Census::default(); let mut after = Census::default();
        let old = observe(|| { before.charge(&bytes)?; module_relation::check_bytes(&bytes) });
        let new = observe(|| { let value = after.charge(&bytes)?; module_relation::check(value) });
        assert_eq!(old, new);
        assert_eq!(reference_state(&before), state(&after));
        assert_eq!(new, Outcome::Returned(Err("relation schema/limits".into())));
    }
}
