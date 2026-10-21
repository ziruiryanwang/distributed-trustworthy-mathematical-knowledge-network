//! RC0 proves a restricted instance of the original conditional module relation.
//! Nothing here authenticates a parent receipt. The aggregate must discharge
//! each exact parent journal before claiming this conditional conclusion.
use crate::{syntax::{self, Address, Id, SourceCensus, MAX_UNIVERSES}, typing::{Signature, Typing}};
use dmkn_module_relation::{canonical::{array, fields, hash, parse_validated, require, text, uint, unhex, R},
    commitments, journal::{Journal, BYTES as JOURNAL_BYTES}, policy, relation::RelationConclusion};
use serde_json::Value;
use std::collections::BTreeMap;

pub const SCHEMA: &str = "DMKN_RESTRICTED_COMPOSITION_V1";
pub const SEMANTIC_IMAGE_HEX: &str = "9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e";

fn semantic_image() -> R<[u32; 8]> {
    let bytes = unhex(SEMANTIC_IMAGE_HEX)?;
    Ok(std::array::from_fn(|index| u32::from_le_bytes(bytes[index * 4..index * 4 + 4].try_into().unwrap())))
}

fn declaration(tc: &mut Typing, group: &Value, owner: [u8; 32]) -> R<(Address, Signature)> {
    fields(group, &["kind", "declarations"])?;
    require(group["kind"] == "ordinary", "RC ordinary groups only")?;
    let declarations = array(&group["declarations"])?;
    require(declarations.len() == 1, "RC singleton theorem group")?;
    let d = &declarations[0];
    fields(d, &["name", "kind", "universes", "type", "value_hash", "meta"])?;
    require(d["kind"] == "theorem" && d["value_hash"].is_null(), "RC theorem only, no value commitment")?;
    fields(&d["meta"], &[])?;
    let universes = uint(&d["universes"], MAX_UNIVERSES as u64)? as usize;
    let address = tc.arena.owned(owner, &d["name"])?;
    let ty = tc.arena.parse_expr(&d["type"], owner, universes)?;
    Ok((address, Signature { universes, ty }))
}

pub fn check(value: Value) -> R<RelationConclusion> { check_with_census(value).map(|(conclusion, _)| conclusion) }

/// Direct bytes callers get the same raw cap and duplicate-key refusal as the
/// aggregate wire decoder. A successful result still has pending assumptions.
pub fn check_bytes(bytes: &[u8]) -> R<RelationConclusion> {
    require(!bytes.is_empty() && bytes.len() <= syntax::MAX_FRAME_BYTES, "RC raw frame bytes")?;
    check(parse_validated(bytes)?)
}

pub fn check_with_census(value: Value) -> R<(RelationConclusion, SourceCensus)> {
    syntax::frame_bounds(&value)?;
    fields(&value, &["schema", "image", "rank", "local_spec", "parents", "proofs"])?;
    require(value["schema"] == SCHEMA, "RC frame schema")?;
    let image: [u32; 8] = serde_json::from_value(value["image"].clone()).map_err(|e| format!("RC semantic image: {e}"))?;
    require(image == semantic_image()?, "RC fixed original semantic I image")?;
    let rank = uint(&value["rank"], u64::MAX)?;
    let foundation = policy::foundation(); let semantic_policy = policy::semantic_id()?;
    let groups = array(&value["local_spec"]["groups"])?;
    require(!groups.is_empty() && groups.len() <= 8, "RC local group count")?;
    let proofs = array(&value["proofs"])?;
    require(proofs.len() == groups.len(), "RC one proof per local theorem")?;
    let summary = commitments::summarize(&value["local_spec"], &foundation, &semantic_policy)?;
    let module = hash("module-spec", &summary)?;
    let parents = array(&value["parents"])?;
    require(parents.len() <= 8, "RC parent count")?;
    let mut parent_map = BTreeMap::new();
    let mut parent_journals = Vec::new();
    let mut imports = BTreeMap::new();
    let mut greatest_rank = None::<u64>;
    for parent in parents {
        fields(parent, &["journal", "openings"])?;
        let raw = array(&parent["journal"])?;
        require(raw.len() == JOURNAL_BYTES, "RC parent journal bytes")?;
        let bytes = raw.iter().map(|b| uint(b, 255).map(|b| b as u8)).collect::<R<Vec<_>>>()?;
        let journal = Journal::decode(&bytes)?;
        require(journal.image == image && journal.foundation == foundation && journal.policy == semantic_policy
            && journal.module != module, "RC parent exact image/foundation/policy/distinct module")?;
        require(parent_map.insert(journal.module, journal.rank).is_none(), "RC duplicate parent module")?;
        greatest_rank = Some(greatest_rank.map_or(journal.rank, |r| r.max(journal.rank)));
        let openings = array(&parent["openings"])?;
        require(!openings.is_empty() && openings.len() <= 16, "RC selected parent groups")?;
        for opening in openings {
            let (index, group) = commitments::verify_opening(&journal, opening)?;
            require(imports.insert((journal.module, index), group).is_none(), "RC duplicate imported group")?;
            require(imports.len() <= 16, "RC total imported groups")?;
        }
        // Preserve caller order exactly, as the original I relation does.
        parent_journals.push(bytes);
    }
    let expected_rank = match greatest_rank { None => 0, Some(r) => r.checked_add(1).ok_or("RC rank overflow")? };
    require(rank == expected_rank && parent_map.values().all(|r| *r < rank), "RC exact strict parent rank")?;

    let mut tc = Typing::new()?;
    let mut imported_types = Vec::<Id>::new();
    // The original W emitter uses this exact (owner,index) order. All selected
    // imported types are conditional premises, but every type dependency must
    // be explicitly opened too; no hidden declaration can be synthesized.
    for ((owner, _), group) in imports {
        let (address, signature) = declaration(&mut tc, &group, owner)?;
        imported_types.push(signature.ty); tc.add(address, signature)?;
    }
    for ty in imported_types { tc.references(ty)?; }
    for (group, proof) in groups.iter().zip(proofs) {
        let (address, signature) = declaration(&mut tc, group, module)?;
        let proof = tc.arena.parse_expr(proof, module, signature.universes)?;
        tc.check_theorem(signature.ty, proof)?;
        // Self/forward references cannot pass references/inference above.
        tc.add(address, signature)?;
    }
    tc.arena.virtual_witness_bounds()?;
    let journal = Journal { image, foundation, policy: semantic_policy, module,
        group_root: unhex(text(&summary["group_root"])?)?,
        group_count: uint(&summary["group_count"], 4096)? as u32, rank };
    journal.validate()?;
    Ok((RelationConclusion { journal, parent_journals }, tc.arena.census))
}
