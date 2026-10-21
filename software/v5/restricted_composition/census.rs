//! Resource census for the RC aggregate, never mathematical authority.
//! One instance spans the entire stream; a new frame does not reset allowances.
use dmkn_module_relation::canonical::{array, fields, parse_validated, require, R};
use dmkn_rc_relation::syntax::SourceCensus;
use serde_json::Value;

pub const SCHEMA: &str = "DMKN_RESTRICTED_COMPOSITION_V1";
pub const MAX_FRAME_BYTES: usize = 256 * 1024;
pub const MAX_FRAME_NODES: usize = 32_768;
pub const MAX_NODES: usize = 131_072;
pub const MAX_DEPTH: usize = 64;
// Whole-stream acceptance cap, not a pre-work hard runtime cap. The source
// census arrives after one bounded core call, so an aggregate refusal can have
// processed up to this allowance plus one additional bounded frame's syntax.
pub const MAX_EXPR_VISITS: usize = 8_192;
pub const MAX_LEVEL_VISITS: usize = MAX_EXPR_VISITS * 8;
pub const MAX_OPENINGS: usize = 16 * crate::relation::MAX_DELTAS;
pub const MAX_INFERENCE_WORK: usize = 200_000 * crate::relation::MAX_DELTAS;

#[derive(Clone, Debug, Default, PartialEq, Eq)]
pub struct Census {
    pub frames: usize,
    pub frame_bytes: usize,
    pub nodes: usize,
    pub maximum_depth: usize,
    pub parent_edges: usize,
    pub openings: usize,
    pub expr_visits: usize,
    pub level_visits: usize,
    pub address_count: usize,
    pub inference_work: usize,
}

fn add(total: &mut usize, more: usize, maximum: usize, reason: &str) -> R<()> {
    *total = total.checked_add(more).ok_or("RC aggregate census overflow")?;
    require(*total <= maximum, reason)
}

impl Census {
    pub(crate) fn charge(&mut self, bytes: &[u8]) -> R<Value> {
        require(!bytes.is_empty() && bytes.len() <= MAX_FRAME_BYTES, "RC frame byte bound")?;
        add(&mut self.frames, 1, crate::relation::MAX_DELTAS, "RC frame count")?;
        add(&mut self.frame_bytes, bytes.len(), crate::wire::MAX_BYTES, "RC total frame bytes")?;
        // Strict parsing rejects duplicate keys, noninteger numbers and trailing
        // data; the raw bounded frame exists before any JSON tree is allocated.
        let value = parse_validated(bytes)?;
        fn visit(census: &mut Census, count: &mut usize, value: &Value, depth: usize) -> R<()> {
            require(depth <= MAX_DEPTH, "RC aggregate JSON depth")?;
            census.maximum_depth = census.maximum_depth.max(depth);
            add(count, 1, MAX_FRAME_NODES, "RC per-frame JSON nodes")?;
            add(&mut census.nodes, 1, MAX_NODES, "RC aggregate JSON nodes")?;
            match value {
                Value::Array(values) => for child in values { visit(census, count, child, depth + 1)?; },
                Value::Object(values) => for child in values.values() { visit(census, count, child, depth + 1)?; },
                _ => {},
            }
            Ok(())
        }
        visit(self, &mut 0, &value, 0)?;
        fields(&value, &["schema", "image", "rank", "local_spec", "parents", "proofs"])?;
        require(value["schema"] == SCHEMA, "RC exact delta schema")?;
        let image: [u32; 8] = serde_json::from_value(value["image"].clone())
            .map_err(|e| format!("RC semantic image: {e}"))?;
        require(image == crate::header::relation_image(), "RC fixed semantic I image")?;
        let parents = array(&value["parents"])?;
        require(parents.len() <= 8, "RC per-frame parents")?;
        add(&mut self.parent_edges, parents.len(), crate::relation::MAX_EDGES, "RC aggregate parent edges")?;
        let mut frame_openings = 0;
        for parent in parents {
            fields(parent, &["journal", "openings"])?;
            let count = array(&parent["openings"])? .len();
            require(count > 0, "RC nonempty selected parent opening")?;
            add(&mut frame_openings, count, 16, "RC per-frame openings")?;
            add(&mut self.openings, count, MAX_OPENINGS, "RC aggregate openings")?;
        }
        Ok(value)
    }

    /// The core's counters are derived, not sender-supplied. Charge before
    /// inserting the conditional delta, but AFTER that frame's core work.
    /// A stream rejected here can spend the accepted syntax allowance plus
    /// one frame's 8,192-expression allowance (16,384 total), not merely8,192.
    /// The call still has at most16 frames, each with its own200,000-work/
    /// 256-KiB bound; refusal grants no conclusion and refunds no work.
    pub(crate) fn charge_source(&mut self, source: &SourceCensus) -> R<()> {
        add(&mut self.expr_visits, source.expr_visits, MAX_EXPR_VISITS, "RC aggregate expression visits")?;
        add(&mut self.level_visits, source.level_visits, MAX_LEVEL_VISITS, "RC aggregate level visits")?;
        add(&mut self.address_count, source.address_count, 64 * crate::relation::MAX_DELTAS,
            "RC aggregate address census")?;
        add(&mut self.inference_work, source.inference_work, MAX_INFERENCE_WORK,
            "RC aggregate inference work")
    }
}
