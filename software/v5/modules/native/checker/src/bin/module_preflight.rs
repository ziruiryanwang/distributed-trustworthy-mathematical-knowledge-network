//! Bounded local diagnostic CLI. Never grants mathematical/certificate authority.
//! Root's operation supervisor supplies actual CPU/memory/process-tree limits.

use nanoda_lib::demand::Demand;
use nanoda_lib::module::{native_preflight, ConditionalPremise, PremiseAuthority, Preflight};
use nanoda_lib::module_correspondence::{check_rows_correspondence_conditional,
    BodyOpening, GroupBinding, StructuralCorrespondence};
use nanoda_lib::parser::{decode_owned_row, parse_owned_rows};
use nanoda_lib::util::Config;
use serde::Deserialize;
use serde_json::{json, Value};
use std::io::Read;
use std::collections::BTreeMap;

const MAX_INPUT: u64 = 32 * 1024 * 1024;

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Request {
    schema: String,
    mode: String,
    rows: Vec<Value>,
    permitted_axioms: Vec<String>,
    #[serde(default)]
    module: Option<String>,
    #[serde(default)]
    foundation: Option<String>,
    #[serde(default)]
    premises: Vec<Premise>,
    #[serde(default)]
    correspondence: Option<Correspondence>,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Correspondence {
    foundation_rows: usize,
    groups: Vec<GroupBinding>,
    bodies: Vec<BodyOpening>,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Premise {
    authority: Authority,
    names: Vec<u32>,
}

#[derive(Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case", deny_unknown_fields)]
enum Authority {
    Foundation { foundation: String },
    Module { module: String, group: String, journal: String, receipt: String },
}

fn digest(value: &str) -> Result<[u8; 32], String> {
    if value.len() != 64 || !value.bytes().all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b)) {
        return Err("LOWERCASE_DIGEST".into());
    }
    let mut result = [0u8; 32];
    for (index, slot) in result.iter_mut().enumerate() {
        *slot = u8::from_str_radix(&value[index * 2..index * 2 + 2], 16).map_err(|e| e.to_string())?;
    }
    Ok(result)
}

fn hex(value: &[u8; 32]) -> String {
    value.iter().map(|b| format!("{b:02x}")).collect()
}

fn bind_roles(correspondence: &StructuralCorrespondence, module: &[u8; 32],
              foundation: &[u8; 32], premises: &[ConditionalPremise]) -> Result<(), String> {
    let mut expected = BTreeMap::new();
    for name in &correspondence.foundation_name_indices {
        expected.insert(*name, None);
    }
    let mut locals = Vec::new();
    for group in &correspondence.groups {
        let owner = digest(&group.owner)?;
        if group.imported {
            if owner == *module { return Err("CORRESPONDENCE_CURRENT_MODULE_IMPORT".into()); }
            for name in &group.export_name_indices {
                if expected.insert(*name, Some(owner)).is_some() { return Err("CORRESPONDENCE_ROLE_OVERLAP".into()); }
            }
        } else {
            if owner != *module { return Err("CORRESPONDENCE_LOCAL_MODULE_OWNER".into()); }
            locals.extend_from_slice(&group.export_name_indices);
        }
    }
    for premise in premises {
        let authority = match &premise.authority {
            PremiseAuthority::Foundation { foundation_digest } => {
                if foundation_digest != foundation { return Err("CORRESPONDENCE_FOUNDATION_ROLE".into()); }
                None
            },
            PremiseAuthority::Module { module, .. } => Some(*module),
        };
        for name in &premise.export_name_indices {
            if expected.remove(name) != Some(authority) { return Err("CORRESPONDENCE_EXACT_IMPORT_ROLE".into()); }
        }
    }
    if !expected.is_empty() || locals.is_empty() { return Err("CORRESPONDENCE_ROLE_CENSUS".into()); }
    Ok(())
}

fn run(request: Request) -> Result<Value, String> {
    if request.schema != "DMKN_V5_NATIVE_PREFLIGHT_V1" || request.rows.is_empty()
        || request.rows.len() > 250_000 || request.premises.len() > 4_096
        || request.permitted_axioms.len() > 1_024
        || request.permitted_axioms.iter().any(|name| name.len() > 4_096) {
        return Err("REQUEST_SCHEMA_OR_LIMIT".into());
    }
    let correspondence = match (request.mode.as_str(), request.correspondence.as_ref()) {
        ("corresponding_module", Some(input)) => Some(check_rows_correspondence_conditional(
            &request.rows, input.foundation_rows, &input.groups, &input.bodies)),
        ("all_new" | "conditional_module", None) => None,
        _ => return Err("MODE_CORRESPONDENCE_INPUT_MISMATCH".into()),
    };
    let config: Config = serde_json::from_value(json!({
        "export_file_path": null, "use_stdin": false,
        "permitted_axioms": request.permitted_axioms, "unpermitted_axiom_hard_error": true,
        "num_threads": 1, "nat_extension": false, "string_extension": false,
        "pp_declars": null, "pp_output_path": null, "print_axioms": false,
        "unsafe_permit_all_axioms": false
    })).map_err(|e| e.to_string())?;
    let rows = request.rows.into_iter().map(decode_owned_row)
        .collect::<Result<Vec<_>, _>>().map_err(|e| e.to_string())?;
    let (export, skipped) = parse_owned_rows(rows, config).map_err(|e| e.to_string())?;
    if !skipped.is_empty() { return Err("SKIPPED_AXIOM".into()); }
    if request.mode == "all_new" {
        if request.module.is_some() || request.foundation.is_some() || !request.premises.is_empty() {
            return Err("ALL_NEW_CANNOT_SKIP_PREMISES".into());
        }
        export.check_all_declars();
        return Ok(json!({
            "status": "ALL_DECLARATIONS_CHECKED_UNDER_EXPLICIT_AXIOMS",
            "checked_declarations": export.declars.len(),
            "certificate_verification_performed": false, "mathematical_admission": false
        }));
    }
    if request.mode != "conditional_module" && request.mode != "corresponding_module" {
        return Err("UNKNOWN_MODE".into());
    }
    let module = digest(request.module.as_deref().ok_or("MODULE_REQUIRED")?)?;
    let foundation = digest(request.foundation.as_deref().ok_or("FOUNDATION_REQUIRED")?)?;
    let mut premises = Vec::new();
    for premise in request.premises {
        let authority = match premise.authority {
            Authority::Foundation { foundation } => PremiseAuthority::Foundation {
                foundation_digest: digest(&foundation)?,
            },
            Authority::Module { module, group, journal, receipt } => PremiseAuthority::Module {
                module: digest(&module)?, group_descriptor_digest: digest(&group)?,
                journal_digest: digest(&journal)?, receipt_digest: digest(&receipt)?,
            },
        };
        premises.push(ConditionalPremise { authority, export_name_indices: premise.names });
    }
    if let Some(binding) = &correspondence {
        bind_roles(binding, &module, &foundation, &premises)?;
    }
    let report = export.check_module_extension_conditional(module, foundation, &premises);
    Ok(json!({"status": report.status, "module": hex(&report.module),
              "checked_local_names": report.checked_local_names,
              "unverified_premise_count": report.premises.len(),
              "correspondence": correspondence.as_ref().map(|binding| json!({
                  "status": binding.status, "groups": binding.groups.len(),
                  "unverified_body_hash_equations": binding.body_hash_obligations.len(),
                  "hash_verification_performed": binding.hash_verification_performed,
                  "mathematical_admission": binding.mathematical_admission})),
              "certificate_verification_performed": report.receipt_verification_performed,
              "mathematical_admission": report.mathematical_admission}))
}

fn entry() -> Value {
    let work = || -> Result<Value, String> {
        let args = std::env::args_os().collect::<Vec<_>>();
        if args.len() != 2 { return Err("USAGE: module_preflight INPUT_JSON".into()); }
        let file = std::fs::File::open(&args[1]).map_err(|e| e.to_string())?;
        if file.metadata().map_err(|e| e.to_string())?.len() > MAX_INPUT {
            return Err("INPUT_BYTE_LIMIT".into());
        }
        let mut bytes = Vec::new();
        file.take(MAX_INPUT + 1).read_to_end(&mut bytes).map_err(|e| e.to_string())?;
        if bytes.len() as u64 > MAX_INPUT { return Err("INPUT_BYTE_LIMIT".into()); }
        run(serde_json::from_slice(&bytes).map_err(|e| e.to_string())?)
    };
    match native_preflight(work) {
        Preflight::Conditional(Ok(result)) => result,
        Preflight::Conditional(Err(reason)) => json!({"status": "REFUSED", "reason": reason,
            "certificate_verification_performed": false, "mathematical_admission": false}),
        Preflight::Need(demand) => {
            let detail = match demand {
                Demand::Declaration { export_name_index } =>
                    json!({"kind": "NeedDeclaration", "native_name_index": export_name_index}),
                Demand::Body { export_name_index, digest } =>
                    json!({"kind": "NeedBody", "native_name_index": export_name_index, "body_hash": hex(&digest)}),
            };
            json!({"status": "NEED", "demand": detail, "certificate_verification_performed": false,
                   "mathematical_admission": false})
        },
        Preflight::Refused => json!({"status": "REFUSED", "reason": "NATIVE_CHECKER_PANIC",
            "certificate_verification_performed": false, "mathematical_admission": false}),
    }
}

fn main() {
    let result = std::thread::Builder::new().name("module_preflight".into())
        .stack_size(16_777_216).spawn(entry).expect("PREFLIGHT_THREAD")
        .join().expect("PREFLIGHT_JOIN");
    println!("{}", result);
    if result["status"] == "REFUSED" { std::process::exit(2); }
}
