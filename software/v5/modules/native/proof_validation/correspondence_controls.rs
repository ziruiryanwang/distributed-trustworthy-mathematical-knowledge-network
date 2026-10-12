//! Differential syntax controls against the unchanged tree-producing methods
//! in the same private module. No synthetic row here is a native proof claim.

use super::*;
use std::any::Any;
use std::panic::{catch_unwind, AssertUnwindSafe};

const OWNER: &str = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
const OTHER: &str = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb";

struct Fixture { rows: Vec<Value>, foundation_rows: usize }

fn fixture() -> Fixture {
    let mut rows = vec![json!({"meta": {}})];
    for (index, parent, name) in [
        (1, 0, "u"), (2, 0, "v"), (3, 0, "Foundation"),
        (4, 0, "DMKN"), (5, 4, "Mod"), (6, 5, OWNER), (7, 6, "Local"),
        (8, 5, OTHER), (9, 8, "External"),
    ] {
        rows.push(json!({"in": index, "str": {"pre": parent, "str": name}}));
    }
    rows.push(json!({"axiom": {"name": 3}}));
    let foundation_rows = rows.len();
    rows.extend([
        json!({"il": 1, "param": 1}),
        json!({"il": 2, "succ": 0}),
        json!({"il": 3, "max": [1, 2]}),
        json!({"il": 4, "imax": [2, 3]}),
        json!({"ie": 0, "bvar": 0}),
        json!({"ie": 1, "sort": 0}),
        json!({"ie": 2, "sort": 1}),
        json!({"ie": 3, "const": {"name": 7, "us": [1, 2, 3, 4, 0]}}),
        json!({"ie": 4, "const": {"name": 9, "us": [0]}}),
        json!({"ie": 5, "const": {"name": 3, "us": []}}),
        json!({"ie": 6, "app": {"fn": 3, "arg": 0}}),
        json!({"ie": 7, "lam": {"name": 0, "type": 1, "body": 6, "binderInfo": "default"}}),
        json!({"ie": 8, "forallE": {"name": 1, "type": 2, "body": 7, "binderInfo": "implicit"}}),
        json!({"ie": 9, "letE": {"name": 0, "type": 1, "value": 5, "body": 8, "nondep": false}}),
        json!({"ie": 10, "proj": {"typeName": 3, "idx": 2, "struct": 9}}),
        json!({"ie": 11, "app": {"fn": 10, "arg": 10}}),
    ]);
    Fixture { rows, foundation_rows }
}

fn row_mut<'a>(fixture: &'a mut Fixture, domain: &str, index: usize) -> &'a mut Value {
    fixture.rows.iter_mut().find(|row| row[domain].as_u64() == Some(index as u64)).unwrap()
}

fn diagnostic(payload: Box<dyn Any + Send>) -> String {
    if let Some(value) = payload.downcast_ref::<String>() { return value.clone(); }
    if let Some(value) = payload.downcast_ref::<&str>() { return (*value).to_owned(); }
    panic!("unexpected nonstring panic payload in correspondence control")
}

#[derive(Debug, PartialEq, Eq)]
struct Outcome { result: Result<(), String>, work: usize }

fn expression_run(fixture: &Fixture, index: usize, parameters: &[usize], depth: usize,
                  work: usize, validate: bool) -> Outcome {
    let mut inventory = Inventory::new(&fixture.rows, fixture.foundation_rows);
    inventory.work = work;
    let result = catch_unwind(AssertUnwindSafe(|| {
        if validate { inventory.validate_expression(OWNER, index, parameters, depth); }
        else { drop(inventory.expression(OWNER, index, parameters, depth)); }
    })).map_err(diagnostic);
    Outcome { result, work: inventory.work }
}

fn compare_expression(fixture: &Fixture, index: usize, parameters: &[usize], depth: usize,
                      work: usize) -> Outcome {
    let old = expression_run(fixture, index, parameters, depth, work, false);
    let new = expression_run(fixture, index, parameters, depth, work, true);
    assert_eq!(old, new, "proof validator changed first semantic diagnostic or work prefix");
    new
}

fn level_run(fixture: &Fixture, index: usize, parameters: &[usize], depth: usize,
             work: usize, validate: bool) -> Outcome {
    let mut inventory = Inventory::new(&fixture.rows, fixture.foundation_rows);
    inventory.work = work;
    let result = catch_unwind(AssertUnwindSafe(|| {
        if validate { inventory.validate_level(index, parameters, depth); }
        else { drop(inventory.level(index, parameters, depth)); }
    })).map_err(diagnostic);
    Outcome { result, work: inventory.work }
}

fn compare_level(fixture: &Fixture, index: usize, parameters: &[usize], depth: usize,
                 work: usize) -> Outcome {
    let old = level_run(fixture, index, parameters, depth, work, false);
    let new = level_run(fixture, index, parameters, depth, work, true);
    assert_eq!(old, new, "level validator changed first semantic diagnostic or work prefix");
    new
}

fn succeeds(outcome: Outcome, work: usize) {
    assert_eq!(outcome, Outcome { result: Ok(()), work });
}

fn refuses(outcome: Outcome, message: &str, work: usize) {
    assert!(outcome.result.as_ref().unwrap_err().contains(message), "{outcome:?}");
    assert_eq!(outcome.work, work);
}

#[test]
fn all_expression_constructors_references_and_shared_children_match() {
    let fixture = fixture();
    // Repeated children are charged repeatedly; no DAG memoization is added.
    for (index, work) in [1, 2, 2, 16, 2, 1, 18, 21, 24, 28, 29, 59].into_iter().enumerate() {
        succeeds(compare_expression(&fixture, index, &[1, 2], 0, 0), work);
        succeeds(compare_expression(&fixture, index, &[2, 1], 0, 0), work);
    }
    let mut inventory = Inventory::new(&fixture.rows, fixture.foundation_rows);
    assert_eq!(inventory.expression(OWNER, 5, &[], 0),
               json!(["const", ["foundation", [["s", "Foundation"]]], []]));
    assert_eq!(inventory.expression(OWNER, 4, &[], 0),
               json!(["const", ["external", OTHER, [["s", "External"]]], [["zero"]]]));
    let local = inventory.expression(OWNER, 3, &[1], 0);
    assert_eq!(local[1], json!(["local", [["s", "Local"]]]));
}

#[test]
fn zero_and_all_level_constructors_match() {
    let fixture = fixture();
    for (index, work) in [1, 1, 2, 4, 7].into_iter().enumerate() {
        succeeds(compare_level(&fixture, index, &[1, 2], 0, 0), work);
        succeeds(compare_level(&fixture, index, &[2, 1], 0, 0), work);
    }
    refuses(compare_level(&fixture, 1, &[2], 0, 0), "CORRESPONDENCE_UNBOUND_UNIVERSE", 1);
    refuses(compare_level(&fixture, 99, &[], 0, 0), "CORRESPONDENCE_LEVEL_INDEX", 1);
}

#[test]
fn constants_validate_levels_before_reference_and_charge_failed_prefix() {
    let mut fixture = fixture();
    *row_mut(&mut fixture, "ie", 3) = json!({"ie": 3, "const": {"name": 999, "us": [999]}});
    refuses(compare_expression(&fixture, 3, &[1], 0, 0), "CORRESPONDENCE_LEVEL_INDEX", 2);
    row_mut(&mut fixture, "ie", 3)["const"]["us"] = json!([0, -1]);
    refuses(compare_expression(&fixture, 3, &[1], 0, 0), "CORRESPONDENCE_UINT", 2);
    row_mut(&mut fixture, "ie", 3)["const"]["us"] = json!([]);
    refuses(compare_expression(&fixture, 3, &[1], 0, 0), "CORRESPONDENCE_NAME_INDEX", 1);
    row_mut(&mut fixture, "ie", 3)["const"]["us"] = Value::Array(vec![json!(0); 257]);
    refuses(compare_expression(&fixture, 3, &[1], 0, 0), "CORRESPONDENCE_UNIVERSE_ARITY", 1);
    row_mut(&mut fixture, "ie", 3)["const"]["us"] = json!(null);
    refuses(compare_expression(&fixture, 3, &[1], 0, 0), "CORRESPONDENCE_ARRAY", 1);
}

#[test]
fn projection_reference_then_index_then_child_order_matches() {
    let mut fixture = fixture();
    *row_mut(&mut fixture, "ie", 10) = json!({"ie": 10, "proj": {"typeName": 999, "idx": "bad", "struct": 999}});
    refuses(compare_expression(&fixture, 10, &[], 0, 0), "CORRESPONDENCE_NAME_INDEX", 1);
    row_mut(&mut fixture, "ie", 10)["proj"]["typeName"] = json!(3);
    refuses(compare_expression(&fixture, 10, &[], 0, 0), "CORRESPONDENCE_UINT", 1);
    row_mut(&mut fixture, "ie", 10)["proj"]["idx"] = json!(0);
    refuses(compare_expression(&fixture, 10, &[], 0, 0), "CORRESPONDENCE_EXPRESSION_BACKREF", 1);
    row_mut(&mut fixture, "ie", 10)["proj"]["struct"] = json!(0);
    succeeds(compare_expression(&fixture, 10, &[], 0, 0), 2);
}

#[test]
fn sibling_failures_preserve_left_to_right_evaluation() {
    let mut fixture = fixture();
    *row_mut(&mut fixture, "ie", 0) = json!({"ie": 0, "bvar": "bad"});
    *row_mut(&mut fixture, "ie", 1) = json!({"ie": 1, "sort": 999});
    *row_mut(&mut fixture, "ie", 6) = json!({"ie": 6, "app": {"fn": 0, "arg": 1}});
    refuses(compare_expression(&fixture, 6, &[], 0, 0), "CORRESPONDENCE_UINT", 2);
    row_mut(&mut fixture, "ie", 6)["app"] = json!({"fn": 1, "arg": 0});
    refuses(compare_expression(&fixture, 6, &[], 0, 0), "CORRESPONDENCE_LEVEL_INDEX", 3);
    *row_mut(&mut fixture, "il", 1) = json!({"il": 1, "param": 999});
    *row_mut(&mut fixture, "il", 2) = json!({"il": 2, "succ": "bad"});
    refuses(compare_level(&fixture, 3, &[], 0, 0), "CORRESPONDENCE_NAME_INDEX", 2);
    row_mut(&mut fixture, "il", 3)["max"] = json!([2, 1]);
    refuses(compare_level(&fixture, 3, &[], 0, 0), "CORRESPONDENCE_UINT", 2);
}

#[test]
fn binder_styles_zero_name_and_nondependent_checks_match() {
    let mut fixture = fixture();
    for style in ["default", "implicit", "strictImplicit", "instImplicit"] {
        row_mut(&mut fixture, "ie", 7)["lam"]["binderInfo"] = json!(style);
        succeeds(compare_expression(&fixture, 7, &[1], 0, 0), 21);
    }
    row_mut(&mut fixture, "ie", 7)["lam"]["name"] = json!(999);
    row_mut(&mut fixture, "ie", 7)["lam"]["binderInfo"] = json!("bad");
    refuses(compare_expression(&fixture, 7, &[1], 0, 0), "CORRESPONDENCE_BINDER_NAME", 1);
    row_mut(&mut fixture, "ie", 7)["lam"]["name"] = json!(0);
    refuses(compare_expression(&fixture, 7, &[1], 0, 0), "CORRESPONDENCE_BINDER_STYLE", 1);
    row_mut(&mut fixture, "ie", 7)["lam"]["binderInfo"] = json!(false);
    refuses(compare_expression(&fixture, 7, &[1], 0, 0), "CORRESPONDENCE_STRING", 1);
    row_mut(&mut fixture, "ie", 9)["letE"]["name"] = json!(999);
    row_mut(&mut fixture, "ie", 9)["letE"]["nondep"] = json!(true);
    refuses(compare_expression(&fixture, 9, &[1], 0, 0), "CORRESPONDENCE_BINDER_NAME", 1);
    row_mut(&mut fixture, "ie", 9)["letE"]["name"] = json!(0);
    refuses(compare_expression(&fixture, 9, &[1], 0, 0), "CORRESPONDENCE_CANONICAL_NONDEP", 1);
}

#[test]
fn malformed_tags_shapes_indices_and_level_backreferences_match() {
    let mut fixture = fixture();
    refuses(compare_expression(&fixture, 99, &[], 0, 0), "CORRESPONDENCE_EXPRESSION_INDEX", 1);
    for value in [json!({"ie": 6, "unknown": 0}), json!({"ie": 6, "mdata": 0})] {
        *row_mut(&mut fixture, "ie", 6) = value;
        refuses(compare_expression(&fixture, 6, &[], 0, 0), "CORRESPONDENCE_NONCANONICAL_EXPRESSION", 1);
    }
    *row_mut(&mut fixture, "ie", 6) = json!({"ie": 6, "app": {"fn": 0, "arg": 0, "extra": 0}});
    refuses(compare_expression(&fixture, 6, &[], 0, 0), "CORRESPONDENCE_FIELDS", 1);
    *row_mut(&mut fixture, "ie", 6) = json!({"ie": 6, "app": []});
    refuses(compare_expression(&fixture, 6, &[], 0, 0), "CORRESPONDENCE_OBJECT", 1);
    *row_mut(&mut fixture, "il", 4) = json!({"il": 4, "unknown": 0});
    refuses(compare_level(&fixture, 4, &[], 0, 0), "CORRESPONDENCE_LEVEL_TAG", 1);
    *row_mut(&mut fixture, "il", 4) = json!({"il": 4, "max": [0]});
    refuses(compare_level(&fixture, 4, &[], 0, 0), "CORRESPONDENCE_LEVEL_PAIR", 1);
    row_mut(&mut fixture, "il", 4)["max"] = json!([4, "bad"]);
    refuses(compare_level(&fixture, 4, &[], 0, 0), "CORRESPONDENCE_UINT", 1);
    row_mut(&mut fixture, "il", 4)["max"] = json!([4, 0]);
    refuses(compare_level(&fixture, 4, &[], 0, 0), "CORRESPONDENCE_LEVEL_BACKREF", 1);
    *row_mut(&mut fixture, "il", 2) = json!({"il": 2, "succ": 2});
    refuses(compare_level(&fixture, 2, &[], 0, 0), "CORRESPONDENCE_LEVEL_BACKREF", 1);
}

#[test]
fn identical_reference_subroutine_keeps_owner_and_foundation_refusals() {
    let mut fixture = fixture();
    row_mut(&mut fixture, "ie", 5)["const"]["name"] = json!(1);
    refuses(compare_expression(&fixture, 5, &[], 0, 0), "CORRESPONDENCE_UNKNOWN_FOUNDATION_NAME", 1);
    row_mut(&mut fixture, "ie", 5)["const"]["name"] = json!(0);
    refuses(compare_expression(&fixture, 5, &[], 0, 0), "CORRESPONDENCE_NAME_INDEX", 1);
    row_mut(&mut fixture, "in", 6)["str"]["str"] = json!("A".repeat(64));
    refuses(compare_expression(&fixture, 3, &[1], 0, 0), "CORRESPONDENCE_DIGEST", 16);
    *row_mut(&mut fixture, "in", 6) = json!({"in": 6, "num": {"pre": 5, "i": 0}});
    refuses(compare_expression(&fixture, 3, &[1], 0, 0), "CORRESPONDENCE_MODULE_COMPONENT", 16);
}

#[test]
fn work_and_depth_limits_preserve_entry_and_failed_child_charge() {
    let fixture = fixture();
    succeeds(compare_expression(&fixture, 0, &[], MAX_DEPTH, MAX_NODES - 1), MAX_NODES);
    refuses(compare_expression(&fixture, 0, &[], MAX_DEPTH + 1, 0), "CORRESPONDENCE_EXPANSION_LIMIT", 1);
    refuses(compare_expression(&fixture, 99, &[], 0, MAX_NODES), "CORRESPONDENCE_EXPANSION_LIMIT", MAX_NODES + 1);
    refuses(compare_expression(&fixture, 1, &[], MAX_DEPTH, 0), "CORRESPONDENCE_EXPANSION_LIMIT", 2);
    refuses(compare_expression(&fixture, 1, &[], 0, MAX_NODES - 1), "CORRESPONDENCE_EXPANSION_LIMIT", MAX_NODES + 1);
    succeeds(compare_level(&fixture, 0, &[], MAX_DEPTH, MAX_NODES - 1), MAX_NODES);
    refuses(compare_level(&fixture, 0, &[], MAX_DEPTH + 1, 0), "CORRESPONDENCE_EXPANSION_LIMIT", 1);
    refuses(compare_level(&fixture, 2, &[], MAX_DEPTH, 0), "CORRESPONDENCE_EXPANSION_LIMIT", 2);
}

#[test]
fn consecutive_proofs_retain_shared_cumulative_work_state() {
    let fixture = fixture();
    let run = |validate: bool| {
        let mut inventory = Inventory::new(&fixture.rows, fixture.foundation_rows);
        inventory.work = MAX_NODES - 2;
        let mut outcomes = Vec::new();
        for index in [0, 1, 0] {
            let result = catch_unwind(AssertUnwindSafe(|| {
                if validate { inventory.validate_expression(OWNER, index, &[], 0); }
                else { drop(inventory.expression(OWNER, index, &[], 0)); }
            })).map_err(diagnostic);
            outcomes.push(Outcome { result, work: inventory.work });
        }
        outcomes
    };
    let old = run(false);
    let new = run(true);
    assert_eq!(old, new);
    assert!(new[0].result.is_ok());
    assert_eq!(new.iter().map(|value| value.work).collect::<Vec<_>>(),
               vec![MAX_NODES - 1, MAX_NODES + 1, MAX_NODES + 2]);
    assert!(new[1].result.as_ref().unwrap_err().contains("CORRESPONDENCE_EXPANSION_LIMIT"));
    assert!(new[2].result.as_ref().unwrap_err().contains("CORRESPONDENCE_EXPANSION_LIMIT"));
}

fn constructor_refuses(fixture: &Fixture, expected: &str) {
    // Constructor remains byte-identical. Both production paths construct it
    // before visiting either proof routine, including unused inventory rows.
    let result = catch_unwind(AssertUnwindSafe(|| {
        let _inventory = Inventory::new(&fixture.rows, fixture.foundation_rows);
    })).map_err(diagnostic);
    assert!(result.unwrap_err().contains(expected));
}

#[test]
fn complete_inventory_is_checked_before_reachable_proof_syntax() {
    let mut fixture = fixture();
    row_mut(&mut fixture, "ie", 11)["ie"] = json!(99);
    constructor_refuses(&fixture, "CORRESPONDENCE_EXPRESSION_ORDER");
    let mut fixture = self::fixture();
    fixture.rows[0] = json!({"meta": {}, "extra": true});
    constructor_refuses(&fixture, "CORRESPONDENCE_FIELDS");
    let mut fixture = self::fixture();
    row_mut(&mut fixture, "in", 1)["str"]["pre"] = json!(1);
    constructor_refuses(&fixture, "CORRESPONDENCE_NAME_BACKREF");
    let mut fixture = self::fixture();
    row_mut(&mut fixture, "in", 1)["str"]["str"] = json!("");
    constructor_refuses(&fixture, "CORRESPONDENCE_NAME_STRING");
    let mut fixture = self::fixture();
    fixture.rows.insert(fixture.foundation_rows, json!({"axiom": {"name": 3}}));
    fixture.foundation_rows += 1;
    constructor_refuses(&fixture, "DUPLICATE_FOUNDATION_DECLARATION");
    let mut fixture = self::fixture();
    fixture.rows[fixture.foundation_rows - 1] = json!({"axiom": {"name": 7}});
    constructor_refuses(&fixture, "RESERVED_MODULE_FOUNDATION_NAMESPACE");
    let mut fixture = self::fixture();
    row_mut(&mut fixture, "in", 3)["str"]["str"] = json!("_nested");
    constructor_refuses(&fixture, "RESERVED_NESTED_FOUNDATION_NAMESPACE");
}

#[test]
fn theorem_call_and_imported_early_return_remain_structural_only() {
    let mut fixture = fixture();
    fixture.rows.push(json!({"thm": {
        "name": 7, "levelParams": [], "type": 1, "value": 0, "all": [7]
    }}));
    let mut binding = GroupBinding {
        owner: OWNER.to_owned(), imported: false,
        descriptor: json!({"kind": "ordinary", "declarations": [{
            "name": [["s", "Local"]], "kind": "theorem", "universes": 0,
            "type": ["sort", ["zero"]], "value_hash": null, "meta": {}
        }]}),
    };
    let result = check_rows_correspondence_conditional(&fixture.rows, fixture.foundation_rows,
                                                      &[binding.clone()], &[]);
    assert!(!result.mathematical_admission && !result.hash_verification_performed);
    assert_eq!(result.groups[0].export_name_indices, vec![7]);
    assert!(result.body_hash_obligations.is_empty());
    fixture.rows.last_mut().unwrap()["thm"]["value"] = json!(999);
    let refusal = catch_unwind(AssertUnwindSafe(|| {
        check_rows_correspondence_conditional(&fixture.rows, fixture.foundation_rows,
                                             &[binding.clone()], &[])
    })).map_err(diagnostic);
    assert!(refusal.unwrap_err().contains("CORRESPONDENCE_EXPRESSION_INDEX"));
    *fixture.rows.last_mut().unwrap() = json!({"moduleImportTheorem": {
        "name": 7, "levelParams": [], "type": 1
    }});
    binding.imported = true;
    let imported = check_rows_correspondence_conditional(&fixture.rows, fixture.foundation_rows,
                                                        &[binding], &[]);
    assert!(imported.groups[0].imported);
    assert!(!imported.mathematical_admission && !imported.hash_verification_performed);
}
