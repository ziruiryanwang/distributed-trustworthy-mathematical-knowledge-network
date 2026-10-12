//! Resource precheck, not mathematics. The temporary JSON tree is dropped
//! before the unchanged relation::check_bytes parses/checks the witness.
use dmkn_module_relation::canonical::{array, parse_validated, require, R};
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
    pub(crate) fn charge(&mut self, bytes: &[u8]) -> R<()> {
        let value = parse_validated(bytes)?;
        fn visit(census: &mut Census, value: &Value, depth: usize) -> R<()> {
            require(depth <= MAX_DEPTH, "aggregate JSON depth")?;
            census.maximum_depth = census.maximum_depth.max(depth);
            add(&mut census.nodes, 1, MAX_NODES, "aggregate JSON node budget")?;
            match value {
                Value::Array(values) => for value in values { visit(census, value, depth + 1)?; },
                Value::Object(values) => for value in values.values() { visit(census, value, depth + 1)?; },
                _ => {},
            }
            Ok(())
        }
        visit(self, &value, 0)?;
        let keys = ["schema", "image", "rank", "local_spec", "rows", "parents", "bodies"];
        add(&mut self.rows, array(field(&value, &keys, 4)?)?.len(), MAX_ROWS, "aggregate row budget")?;
        add(&mut self.bodies, array(field(&value, &keys, 6)?)?.len(), MAX_BODIES, "aggregate body budget")?;
        let parents = array(field(&value, &keys, 5)?)?;
        add(&mut self.parent_edges, parents.len(), crate::relation::MAX_EDGES, "aggregate parent edge budget")?;
        for parent in parents {
            add(&mut self.openings, array(field(parent, &["journal", "openings"], 1)?)?.len(),
                MAX_OPENINGS, "aggregate opening budget")?;
        }
        Ok(())
    }
}
