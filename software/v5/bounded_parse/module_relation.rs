//! Fully bound module relation, with pending RISC0 parent assumptions returned
//! only to the guest entry point. The entry point verifies EVERY exact parent
//! journal before committing the new conclusion. No caller-supplied role flags,
//! verification booleans, policy choice or native success transcript are inputs.

use crate::{canonical::{array, canonical_size, hash, hex, parse_bounded, require, sha, text, uint, unhex, BoundedValue, R},
    commitments, foundation_static, journal::{Journal, RELATION}, policy};
use nanoda_lib::{module::{ConditionalPremise, PremiseAuthority},
    module_correspondence::{check_rows_correspondence_conditional, GroupBinding},
    parser::{decode_corresponded_owned_row, parse_owned_rows}, util::Config};
use serde_json::{json, Value};
use std::collections::{BTreeMap, BTreeSet};
pub use crate::input::{Input, Parent};

pub struct RelationConclusion {
    pub journal: Journal,
    /// The guest entry point MUST discharge all these exact (image,journal)
    /// statements using env::verify before committing journal.encode().
    pub parent_journals: Vec<Vec<u8>>,
}

pub fn check(input_value: Value) -> R<RelationConclusion> {
    canonical_size(&input_value)?;
    check_bound(input_value)
}

/// Profile2 proves existence of a checked witness, not exact proof provenance.
/// Whole-input bounds remain mandatory, without a redundant public digest.
pub fn check_bytes(bytes: &[u8]) -> R<RelationConclusion> {
    check_validated(parse_bounded(bytes)?)
}

/// Consume an immutable syntax/resource token, not a mathematical certificate.
/// The unchanged check_bound still performs every relation and kernel check.
pub fn check_validated(input_value: BoundedValue) -> R<RelationConclusion> {
    check_bound(input_value.into_value())
}

fn check_bound(input_value: Value) -> R<RelationConclusion> {
    let input = crate::input::extract(input_value)?;
    require(input.schema == RELATION && input.rows.len() <= 250_000
        && input.rows.len() >= policy::FOUNDATION_ROWS && input.parents.len() <= 4096
        && input.bodies.len() <= 16_384, "relation schema/limits")?;
    let foundation = policy::foundation(); let semantic_policy = policy::semantic_id()?;
    require(foundation_static::matches_rows(&input.rows[..policy::FOUNDATION_ROWS]),
        "exact adopted foundation values")?;

    let summary = commitments::summarize(&input.local_spec, &foundation, &semantic_policy)?;
    let module = hash("module-spec", &summary)?;
    let mut parents = BTreeMap::new();
    let mut imports = BTreeMap::new();
    let mut greatest_rank = None::<u64>;
    for parent in &input.parents {
        let journal = Journal::decode(&parent.journal)?;
        require(journal.image == input.image && journal.foundation == foundation
            && journal.policy == semantic_policy && journal.module != module,
            "parent exact image/foundation/policy/distinct module")?;
        require(!parent.openings.is_empty() && parent.openings.len() <= 4096, "parent selected groups")?;
        require(parents.insert(journal.module, (journal.clone(), &parent.journal)).is_none(), "duplicate parent module")?;
        greatest_rank = Some(greatest_rank.map_or(journal.rank, |r| r.max(journal.rank)));
        for opening in &parent.openings {
            let (index, group) = commitments::verify_opening(&journal, opening)?;
            require(imports.insert((journal.module, index), group).is_none(), "duplicate imported group")?;
            require(imports.len() <= 4096, "imported group count")?;
        }
    }
    let expected_rank = match greatest_rank { None => 0, Some(rank) => rank.checked_add(1).ok_or("rank overflow")? };
    require(input.rank == expected_rank && parents.values().all(|(j, _)| j.rank < input.rank), "strict exact parent rank")?;

    let mut bindings = Vec::new();
    for ((owner, _), group) in &imports {
        bindings.push(GroupBinding { owner:hex(owner), imported:true, descriptor:group.clone() });
    }
    for group in array(&input.local_spec["groups"])? {
        bindings.push(GroupBinding { owner:hex(&module), imported:false, descriptor:group.clone() });
    }
    require(bindings.len() <= 4096, "combined group bound")?;
    let mut bodies = BTreeSet::new();
    for body in &input.bodies {
        require(body.universes <= 256 && bodies.insert((body.universes, body.digest.clone())), "body census")?;
        require(hash("body", &json!({"universes":body.universes,"expr":body.expression}))? == unhex(&body.digest)?,
                "actual canonical body hash")?;
    }
    let correspondence = check_rows_correspondence_conditional(
        &input.rows, policy::FOUNDATION_ROWS, &bindings, &input.bodies);
    require(correspondence.body_hash_obligations.len() == input.bodies.len(), "no unused body openings")?;
    require(correspondence.groups.len() == bindings.len(), "exact matched groups")?;
    let mut premises = vec![ConditionalPremise {
        authority:PremiseAuthority::Foundation { foundation_digest:foundation },
        export_name_indices:correspondence.foundation_name_indices,
    }];
    for (matched, binding) in correspondence.groups.iter().zip(&bindings) {
        require(matched.owner == binding.owner && matched.imported == binding.imported, "derived role correspondence")?;
        if !binding.imported { continue; }
        let owner = unhex(&binding.owner)?;
        let (_, parent_bytes) = parents.get(&owner).ok_or("import without exact parent conclusion")?;
        premises.push(ConditionalPremise {
            authority:PremiseAuthority::Module {
                module:owner, group_descriptor_digest:hash("group-descriptor", &binding.descriptor)?,
                journal_digest:sha(parent_bytes),
                // Receipt bytes are host-side assumption witnesses, not guest
                // mathematical identities. This legacy diagnostic field is not
                // used as authority; real env::verify binds image+journal below.
                receipt_digest:[0;32],
            },
            export_name_indices:matched.export_name_indices.clone(),
        });
    }
    let config: Config = serde_json::from_value(json!({
        "export_file_path":null,"use_stdin":false,"permitted_axioms":[],
        "unpermitted_axiom_hard_error":true,"num_threads":1,"nat_extension":false,
        "string_extension":false,"pp_declars":null,"pp_output_path":null,
        "print_axioms":false,"unsafe_permit_all_axioms":false
    })).map_err(|e| e.to_string())?;
    let rows = input.rows.into_iter().map(decode_corresponded_owned_row).collect::<Result<Vec<_>, _>>().map_err(|e| e.to_string())?;
    let (export, skipped) = parse_owned_rows(rows, config).map_err(|e| e.to_string())?;
    require(skipped.is_empty(), "no skipped native axiom")?;
    let native = export.check_module_extension_conditional(module, foundation, &premises);
    let local_count = array(&input.local_spec["groups"])? .iter()
        .map(|g| array(&g["declarations"]).map(|ds| ds.len())).collect::<R<Vec<_>>>()?.into_iter().sum::<usize>();
    require(native.checked_local_names.len() == local_count, "every local descriptor actually checked")?;
    let journal = Journal { image:input.image, foundation, policy:semantic_policy, module,
        group_root:unhex(text(&summary["group_root"])?)?, group_count:uint(&summary["group_count"],4096)? as u32,
        rank:input.rank };
    journal.validate()?;
    Ok(RelationConclusion { journal, parent_journals:input.parents.into_iter().map(|p| p.journal).collect() })
}
