//! Commit one immutable parse token in exactly the predecessor's charge order.
//! A discarded structural attempt never mutates this aggregate census.
use dmkn_module_relation::{
    canonical::{array, require, R},
    relation::{prepare, Prepared},
};
use serde_json::Value;

pub const MAX_ROWS: usize = 250_000;
pub const MAX_BODIES: usize = 8_192;
pub const MAX_OPENINGS: usize = 4_096;
pub const MAX_NODES: usize = 500_000;
pub const MAX_DEPTH: usize = 128;

#[derive(Clone, Debug, Default, PartialEq, Eq)]
pub struct Census {
    pub rows: usize,
    pub bodies: usize,
    pub openings: usize,
    pub parent_edges: usize,
    pub nodes: usize,
    pub maximum_depth: usize,
}

fn add(value: &mut usize, more: usize, maximum: usize, reason: &str) -> R<()> {
    *value = value.checked_add(more).ok_or("aggregate census overflow")?;
    require(*value <= maximum, reason)
}

fn field<'a>(value: &'a Value, keys: &[&str], index: usize) -> R<&'a Value> {
    match value {
        Value::Object(map) => {
            require(map.len() == keys.len() && keys.iter().all(|k| map.contains_key(*k)),
                "census exact record fields")?;
            Ok(&map[keys[index]])
        },
        Value::Array(values) => {
            require(values.len() == keys.len(), "census exact record arity")?;
            Ok(&values[index])
        },
        _ => Err("census record required".into()),
    }
}

impl Census {
    pub(crate) fn charge(&mut self, bytes: &[u8]) -> R<Prepared> {
        let prepared = prepare(bytes)?;
        let (nodes, depth) = match &prepared {
            Prepared::Legacy(token) => (token.nodes(), token.maximum_depth()),
            Prepared::Typed(token) => (token.nodes(), token.maximum_depth()),
        };
        require(depth <= MAX_DEPTH, "aggregate JSON depth")?;
        self.maximum_depth = self.maximum_depth.max(depth);
        add(&mut self.nodes, nodes, MAX_NODES, "aggregate JSON node budget")?;

        // Do not eagerly extract image/schema/bodies here. Their old semantic
        // extraction occurs only after these ordered resource charges.
        let keys = ["schema", "image", "rank", "local_spec", "rows", "parents", "bodies"];
        let get = |index| match &prepared {
            Prepared::Legacy(token) => field(token.as_value(), &keys, index),
            Prepared::Typed(token) => token.field(keys[index])
                .ok_or_else(|| "census exact record fields".to_owned()),
        };
        let rows = match &prepared {
            Prepared::Legacy(token) => array(field(token.as_value(), &keys, 4)?)?.len(),
            Prepared::Typed(token) => token.rows_len(),
        };
        add(&mut self.rows, rows, MAX_ROWS, "aggregate row budget")?;
        add(&mut self.bodies, array(get(6)?)?.len(), MAX_BODIES, "aggregate body budget")?;
        let parents = array(get(5)?)?;
        add(&mut self.parent_edges, parents.len(), crate::relation::MAX_EDGES,
            "aggregate parent edge budget")?;
        for parent in parents {
            add(&mut self.openings, array(field(parent, &["journal", "openings"], 1)?)?.len(),
                MAX_OPENINGS, "aggregate opening budget")?;
        }
        Ok(prepared)
    }
}
