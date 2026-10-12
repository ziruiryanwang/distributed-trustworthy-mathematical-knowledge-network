//! One corrected differential group; no old successful test is rerun.
//! Inert malformed fixtures do not establish mathematical receipt authority.
#[path = "../aggregate/census.rs"] mod reference_census;
#[path = "../aggregate_parse_once/census.rs"] mod census;
// Both frozen census implementations use the unchanged aggregate edge bound.
mod relation { pub const MAX_EDGES: usize = 128; }
use dmkn_module_relation::{canonical::R, relation as module_relation};
use serde_json::{json, Value};
use std::panic::{catch_unwind, AssertUnwindSafe};

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
fn corrected_named_positional_extraction_then_schema_refusals() {
    let object = json!({"schema":"shape-only", "image":[0,0,0,0,0,0,0,0], "rank":0,
        "local_spec":{}, "rows":[0,1],
        "parents":[{"journal":[],"openings":[{},{}]}], "bodies":[{}]});
    let positional = json!(["shape-only", [0,0,0,0,0,0,0,0], 0, {}, [0,1],
        [[[],[{},{}]]], [{}]]);
    let mut object_schema = object.clone(); object_schema["bodies"] = json!([]);
    let mut positional_schema = positional.clone(); positional_schema[6] = json!([]);
    let cases: [(Value,&str);4] = [(object,"exact input record fields"),
        (positional,"exact input record fields"),
        (object_schema,"relation schema/limits"),(positional_schema,"relation schema/limits")];
    for (value,expected) in cases {
        let bytes = serde_json::to_vec(&value).unwrap();
        let mut before = reference_census::Census::default();
        let mut after = census::Census::default();
        let old = observe(|| { before.charge(&bytes)?; module_relation::check_bytes(&bytes) });
        let new = observe(|| { let parsed = after.charge(&bytes)?; module_relation::check(parsed) });
        assert_eq!(old,new,"same semantic first failure");
        assert_eq!([before.rows,before.bodies,before.openings,before.parent_edges,before.nodes,before.maximum_depth],
                   [after.rows,after.bodies,after.openings,after.parent_edges,after.nodes,after.maximum_depth]);
        assert_eq!(new,Outcome::Returned(Err(expected.into())));
    }
}
