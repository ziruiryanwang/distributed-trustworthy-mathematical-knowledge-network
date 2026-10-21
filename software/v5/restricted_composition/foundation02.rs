//! Tiny signature projection of the exact adopted 413-row foundation.
//! This is not an independent declaration of Eq: the complete adopted F supplies
//! its inductive support and the authority of Eq.trans. No F proof is replayed.
use crate::syntax::{Address, Arena, Id};
use dmkn_module_relation::canonical::{array, require, uint, R};
use serde_json::{json, Value};

pub(crate) const PREFIX_ROWS: usize = 413;
pub(crate) const PREFIX_BYTES: usize = 23_313;
pub(crate) const PREFIX_SHA256: &str =
    "736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c";

// Exact source: original foundation_data.rs, native Eq type6/parameter-name2;
// Eq.trans type103/parameter-name11. Binder native name indices are retained.
// This projection is inspectable by the independent native source harness and
// is itself used by installation; there is no separate test-only signature.
pub(crate) fn signature_projection() -> Value {
    fn bv(i: usize) -> Value { json!(["bvar", i]) }
    fn pi(name: u32, style: &str, domain: Value, body: Value) -> Value {
        json!(["forall", style, name, domain, body])
    }
    fn eq(a: usize, x: usize, y: usize) -> Value {
        let head = json!(["const", ["foundation", [["s", "Eq"]]], [["param", 0]]]);
        json!(["app", ["app", ["app", head, bv(a)], bv(x)], bv(y)])
    }
    let sort = json!(["sort", ["param", 0]]);
    let eq_type = pi(4, "implicit", sort.clone(),
        pi(9, "default", bv(0), pi(9, "default", bv(1), json!(["sort", ["zero"]]))));
    let trans_type = pi(4, "implicit", sort,
        pi(5, "implicit", bv(0), pi(28, "implicit", bv(1), pi(29, "implicit", bv(2),
            pi(30, "default", eq(3, 2, 1), pi(31, "default", eq(4, 2, 1), eq(5, 4, 2)))))));
    json!([
        {"name": [["s", "Eq"]], "universe_names": [2], "type": eq_type},
        {"name": [["s", "Eq"], ["s", "trans"]], "universe_names": [11], "type": trans_type}
    ])
}

pub(crate) fn install(arena: &mut Arena) -> R<Vec<(Address, usize, Id)>> {
    require(PREFIX_ROWS == dmkn_module_relation::policy::FOUNDATION_ROWS
        && PREFIX_SHA256 == dmkn_module_relation::policy::FOUNDATION_CANONICAL_SHA256,
        "RC compiled foundation profile")?;
    array(&signature_projection())?.iter().map(|entry| {
        let address = arena.address(Address::Foundation(Arena::name(&entry["name"])?))?;
        let universes = array(&entry["universe_names"])?;
        for name in universes { uint(name, u32::MAX as u64)?; }
        let ty = arena.parse_projection(&entry["type"], universes.len())?;
        Ok((address, universes.len(), ty))
    }).collect()
}
