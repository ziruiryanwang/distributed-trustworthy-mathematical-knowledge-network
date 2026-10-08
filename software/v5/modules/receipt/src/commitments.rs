//! Codec-compatible group commitments and exact inclusion openings.

use crate::canonical::{array, canonical, fields, hash, hex, require, text, uint, unhex, R};
use crate::journal::Journal;
use serde_json::{json, Value};
use std::collections::{BTreeMap, BTreeSet};

fn name_key(value: &Value) -> R<Vec<u8>> {
    let parts = array(value)?;
    require(!parts.is_empty() && parts.len() <= 64, "relative name length")?;
    for part in parts {
        let pair = array(part)?; require(pair.len() == 2, "name part")?;
        match text(&pair[0])? {
            "s" => { let s = text(&pair[1])?; require(!s.is_empty() && s.len() <= 1024 && !s.contains('\0'), "name string")?; },
            "n" => { uint(&pair[1], u32::MAX as u64)?; },
            _ => return Err("name part tag".into()),
        }
    }
    canonical(value)
}

fn name_set(value: &Value) -> R<BTreeSet<Vec<u8>>> {
    let values = array(value)?;
    require(values.len() <= 16_384, "name list bound")?;
    let result = values.iter().map(name_key).collect::<R<BTreeSet<_>>>()?;
    require(result.len() == values.len(), "duplicate name list")?;
    Ok(result)
}

/// Group census invariants not implied by comparing one raw declaration.
/// Expression/metadata shape is independently matched to native parser records.
pub fn validate_group(group: &Value) -> R<()> {
    fields(group, &["kind", "declarations"])?;
    let declarations = array(&group["declarations"])?;
    require(!declarations.is_empty() && declarations.len() <= 16_384, "group size")?;
    let mut names = BTreeSet::new(); let mut inds = BTreeMap::new(); let mut ctors = BTreeMap::new(); let mut recs = Vec::new();
    for declaration in declarations {
        fields(declaration, &["name", "kind", "universes", "type", "value_hash", "meta"])?;
        uint(&declaration["universes"], 256)?;
        let name = name_key(&declaration["name"])?;
        require(names.insert(name.clone()), "duplicate group declaration")?;
        match text(&declaration["kind"])? {
            "inductive" => { inds.insert(name, declaration); },
            "constructor" => { ctors.insert(name, declaration); },
            "recursor" => recs.push(declaration),
            "definition" | "opaque" | "theorem" => (),
            _ => return Err("unsupported declaration kind".into()),
        }
    }
    if group["kind"] == "ordinary" {
        return require(declarations.len() == 1 && ["definition", "opaque", "theorem"]
            .contains(&text(&declarations[0]["kind"])?), "ordinary singleton kind");
    }
    require(group["kind"] == "inductive" && !inds.is_empty() && !recs.is_empty()
        && inds.len() + ctors.len() + recs.len() == declarations.len(), "inductive group shape")?;
    let all_inds = inds.keys().cloned().collect::<BTreeSet<_>>();
    let mut listed_ctors = BTreeSet::new();
    for (owner, ind) in &inds {
        require(name_set(&ind["meta"]["all"])? == all_inds, "mutual group census")?;
        let constructors = array(&ind["meta"]["constructors"])?;
        for (index, name) in constructors.iter().enumerate() {
            let key = name_key(name)?;
            require(listed_ctors.insert(key.clone()), "duplicate listed constructor")?;
            let ctor = ctors.get(&key).ok_or("listed constructor absent")?;
            require(name_key(&ctor["meta"]["inductive"])? == *owner
                && uint(&ctor["meta"]["constructor_index"], 65535)? == index as u64, "constructor ownership/index")?;
        }
    }
    require(listed_ctors == ctors.keys().cloned().collect(), "constructor census")?;
    for rec in recs {
        let owners = name_set(&rec["meta"]["all"])?;
        require(!owners.is_empty() && owners.is_subset(&all_inds), "recursor owners")?;
        let rules = array(&rec["meta"]["rules"])?;
        require(rules.len() <= 16_384, "rule count")?;
        let mut seen = BTreeSet::new();
        for rule in rules {
            fields(rule, &["constructor", "num_fields", "value_hash"])?;
            let key = name_key(&rule["constructor"])?;
            require(seen.insert(key.clone()) && ctors.contains_key(&key), "rule constructor census")?;
        }
    }
    Ok(())
}

fn leaf(index: usize, group: &Value) -> R<[u8; 32]> {
    hash("group-leaf", &json!({"index":index,"group":group}))
}
fn branch(left: &[u8; 32], right: &[u8; 32]) -> R<[u8; 32]> { hash("group-node", &json!([hex(left),hex(right)])) }

pub fn summarize(spec: &Value, foundation: &[u8; 32], policy: &[u8; 32]) -> R<Value> {
    fields(spec, &["schema", "foundation", "policy", "groups"])?;
    require(spec["schema"] == "DMKN_MODULE_SPEC_V1" && spec["foundation"] == hex(foundation)
        && spec["policy"] == hex(policy), "local spec schema/foundation/policy")?;
    let groups = array(&spec["groups"])?;
    require(!groups.is_empty() && groups.len() <= 4096, "module group count")?;
    let mut names = BTreeSet::new(); let mut level = Vec::new();
    for (index, group) in groups.iter().enumerate() {
        validate_group(group)?;
        for declaration in array(&group["declarations"])? {
            require(names.insert(name_key(&declaration["name"])?), "duplicate module declaration")?;
            require(names.len() <= 16_384, "module declaration count")?;
        }
        level.push(leaf(index, group)?);
    }
    while level.len() > 1 {
        level = level.chunks(2).map(|pair| branch(&pair[0], pair.get(1).unwrap_or(&pair[0]))).collect::<R<Vec<_>>>()?;
    }
    Ok(json!({"schema":"DMKN_MODULE_SUMMARY_V1", "foundation":hex(foundation), "policy":hex(policy),
        "group_count":groups.len(), "group_root":hex(&level[0])}))
}

pub fn verify_opening(parent: &Journal, opening: &Value) -> R<(usize, Value)> {
    fields(opening, &["schema", "summary", "index", "group", "siblings"])?;
    require(opening["schema"] == "DMKN_MODULE_GROUP_OPENING_V1"
        && opening["summary"] == parent.summary(), "opening exact certified summary")?;
    validate_group(&opening["group"])?;
    let index = uint(&opening["index"], 4095)? as usize;
    let mut cursor = index; let mut width = parent.group_count as usize;
    require(cursor < width, "opening index")?;
    let siblings = array(&opening["siblings"])?;
    require(siblings.len() <= 12, "opening height")?;
    let mut current = leaf(index, &opening["group"])?; let mut position = 0usize;
    while width > 1 {
        let sibling = unhex(text(siblings.get(position).ok_or("missing sibling")?)?)?;
        if (cursor ^ 1) >= width { require(sibling == current, "odd Merkle padding")?; }
        current = if cursor & 1 == 1 { branch(&sibling, &current)? } else { branch(&current, &sibling)? };
        cursor /= 2; width = (width + 1) / 2; position += 1;
    }
    require(position == siblings.len() && current == parent.group_root, "opening root or trailing sibling")?;
    Ok((index, opening["group"].clone()))
}
