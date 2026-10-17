//! Independent, serde-only controls for successful per-proof syntax memoization.
//! The unchanged tree-producing methods are the semantic/work-prefix oracle.
//! These tests do not check the native kernel or authenticate mathematical claims.

use super::*;
use std::any::Any;
use std::io::Read;
use std::panic::{catch_unwind, AssertUnwindSafe};

const OWNER: &str = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
const OTHER: &str = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb";

struct Fixture { rows: Vec<Value>, foundation_rows: usize }

fn foundation() -> Fixture {
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
    Fixture { rows, foundation_rows }
}

fn constructors() -> Fixture {
    let mut fixture = foundation();
    fixture.rows.extend([
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
    fixture
}

fn binary_dag(last: usize, levels: bool) -> Fixture {
    let mut fixture = foundation();
    if !levels { fixture.rows.push(json!({"ie": 0, "bvar": 0})); }
    for index in 1..=last {
        fixture.rows.push(if levels {
            json!({"il": index, "max": [index - 1, index - 1]})
        } else {
            json!({"ie": index, "app": {"fn": index - 1, "arg": index - 1}})
        });
    }
    fixture
}

fn row_mut<'a>(fixture: &'a mut Fixture, domain: &str, index: usize) -> &'a mut Value {
    fixture.rows.iter_mut().find(|row| row[domain].as_u64() == Some(index as u64)).unwrap()
}

fn diagnostic(payload: Box<dyn Any + Send>) -> String {
    if let Some(value) = payload.downcast_ref::<String>() { return value.clone(); }
    if let Some(value) = payload.downcast_ref::<&str>() { return (*value).to_owned(); }
    panic!("unexpected nonstring panic payload in syntax memo control")
}

#[derive(Debug, PartialEq, Eq)]
struct Outcome { result: Result<(), String>, work: usize }

#[derive(Debug, Clone, Copy)]
struct Counts { expressions: usize, levels: usize, hits: usize, skipped: usize }

fn counts(inventory: &Inventory<'_>) -> Counts {
    Counts {
        expressions: inventory.syntax_expression_expansions,
        levels: inventory.syntax_level_expansions,
        hits: inventory.syntax_cache_hits,
        skipped: inventory.syntax_skipped_visits,
    }
}

fn call(inventory: &mut Inventory<'_>, owner: &str, index: usize,
        parameters: &[usize], depth: usize, level: bool, memo: bool) -> Outcome {
    let result = catch_unwind(AssertUnwindSafe(|| {
        match (level, memo) {
            (false, false) => drop(inventory.expression(owner, index, parameters, depth)),
            (false, true) => inventory.validate_expression(owner, index, parameters, depth),
            (true, false) => drop(inventory.level(index, parameters, depth)),
            (true, true) => inventory.validate_level(index, parameters, depth),
        }
    })).map_err(diagnostic);
    Outcome { result, work: inventory.work }
}

fn compare(fixture: &Fixture, index: usize, parameters: &[usize], depth: usize,
           work: usize, level: bool) -> (Outcome, Counts) {
    let mut old = Inventory::new(&fixture.rows, fixture.foundation_rows);
    let mut new = Inventory::new(&fixture.rows, fixture.foundation_rows);
    old.work = work; new.work = work;
    let baseline = call(&mut old, OWNER, index, parameters, depth, level, false);
    let actual = call(&mut new, OWNER, index, parameters, depth, level, true);
    assert_eq!(actual, baseline, "memo changed semantic diagnostic or logical work prefix");
    (actual, counts(&new))
}

fn succeeds(outcome: &Outcome, work: usize) {
    assert_eq!(*outcome, Outcome { result: Ok(()), work });
}

fn refuses(outcome: &Outcome, message: &str, work: usize) {
    assert!(outcome.result.as_ref().unwrap_err().contains(message), "{outcome:?}");
    assert_eq!(outcome.work, work);
}

#[test]
fn all_constructors_and_separate_index_domains_match() {
    let fixture = constructors();
    for (index, work) in [1, 2, 2, 16, 2, 1, 18, 21, 24, 28, 29, 59].into_iter().enumerate() {
        for parameters in [&[1, 2][..], &[2, 1][..]] {
            let (outcome, stats) = compare(&fixture, index, parameters, 0, 0, false);
            succeeds(&outcome, work);
            assert_eq!(stats.expressions + stats.levels + stats.skipped, work);
        }
    }
    for (index, work) in [1, 1, 2, 4, 7].into_iter().enumerate() {
        succeeds(&compare(&fixture, index, &[1, 2], 0, 0, true).0, work);
    }
    // Expression 0 has cost 2; level 0 has cost 1, so conflating domains fails.
    let mut mixed = foundation();
    mixed.rows.extend([
        json!({"ie": 0, "sort": 0}),
        json!({"ie": 1, "app": {"fn": 0, "arg": 0}}),
    ]);
    let (outcome, stats) = compare(&mixed, 1, &[], 0, 0, false);
    succeeds(&outcome, 5);
    assert_eq!((stats.expressions, stats.levels, stats.hits, stats.skipped), (2, 1, 1, 2));
    for style in ["default", "implicit", "strictImplicit", "instImplicit"] {
        let mut styled = constructors();
        row_mut(&mut styled, "ie", 7)["lam"]["binderInfo"] = json!(style);
        succeeds(&compare(&styled, 11, &[1], 0, 0, false).0, 59);
    }
}

#[test]
fn shared_dags_reduce_revalidation_without_discounting_work() {
    // These are syntax fixtures, not claims that self-application is well typed.
    for levels in [false, true] {
        let fixture = binary_dag(12, levels);
        let (outcome, stats) = compare(&fixture, 12, &[], 0, 0, levels);
        succeeds(&outcome, 8191);
        assert_eq!(stats.expressions + stats.levels, 13);
        assert_eq!(stats.hits, 12);
        assert_eq!(stats.skipped, 8178);
        assert_eq!(stats.levels, if levels { 13 } else { 0 });
    }
}

#[test]
fn cache_hit_work_bound_falls_back_at_original_visit() {
    for levels in [false, true] {
        let fixture = binary_dag(3, levels);
        let (boundary, hit) = compare(&fixture, 3, &[], 0, MAX_NODES - 15, levels);
        succeeds(&boundary, MAX_NODES);
        assert_eq!(hit.expressions + hit.levels, 4);
        assert!(hit.hits > 0);
        // The first child warms the same subtree later needing fallback.
        let (failure, fallback) = compare(&fixture, 3, &[], 0, MAX_NODES - 14, levels);
        refuses(&failure, "CORRESPONDENCE_EXPANSION_LIMIT", MAX_NODES + 1);
        assert!(fallback.hits > 0);
        assert!(fallback.expressions + fallback.levels > 4);
    }
}

#[test]
fn deeper_cache_occurrence_preserves_failed_descendant_and_mixed_height() {
    for levels in [false, true] {
        let mut fixture = binary_dag(3, levels);
        if levels {
            row_mut(&mut fixture, "il", 2)["max"] = json!([1, 0]);
            row_mut(&mut fixture, "il", 3)["max"] = json!([1, 2]);
        } else {
            row_mut(&mut fixture, "ie", 2)["app"] = json!({"fn": 1, "arg": 0});
            row_mut(&mut fixture, "ie", 3)["app"] = json!({"fn": 1, "arg": 2});
        }
        succeeds(&compare(&fixture, 3, &[], MAX_DEPTH - 3, 0, levels).0, 9);
        let (failure, stats) = compare(&fixture, 3, &[], MAX_DEPTH - 2, 0, levels);
        refuses(&failure, "CORRESPONDENCE_EXPANSION_LIMIT", 7);
        assert!(stats.hits > 0); // earlier repeated leaf, before deeper fallback
    }
    let mut mixed = foundation();
    mixed.rows.extend([
        json!({"il": 1, "succ": 0}),
        json!({"ie": 0, "sort": 1}),
        json!({"ie": 1, "app": {"fn": 0, "arg": 0}}),
        json!({"ie": 2, "app": {"fn": 0, "arg": 1}}),
    ]);
    succeeds(&compare(&mixed, 2, &[], MAX_DEPTH - 4, 0, false).0, 11);
    refuses(&compare(&mixed, 2, &[], MAX_DEPTH - 3, 0, false).0,
            "CORRESPONDENCE_EXPANSION_LIMIT", 8);
}

#[test]
fn malformed_shared_children_do_not_become_successful_memo_entries() {
    let mut fixture = binary_dag(3, false);
    *row_mut(&mut fixture, "ie", 0) = json!({"ie": 0, "bvar": "bad"});
    let (failure, stats) = compare(&fixture, 3, &[], 0, 0, false);
    refuses(&failure, "CORRESPONDENCE_UINT", 4);
    assert_eq!((stats.hits, stats.skipped), (0, 0));
    let mut fixture = binary_dag(3, true);
    *row_mut(&mut fixture, "il", 1) = json!({"il": 1, "param": 999});
    refuses(&compare(&fixture, 3, &[], 0, 0, true).0, "CORRESPONDENCE_NAME_INDEX", 3);
    // A forward/self edge must fail before recursion or caching can hide it.
    let mut fixture = binary_dag(2, false);
    row_mut(&mut fixture, "ie", 1)["app"]["arg"] = json!(1);
    refuses(&compare(&fixture, 2, &[], 0, 0, false).0, "CORRESPONDENCE_EXPRESSION_BACKREF", 3);
}

#[test]
fn fresh_proof_context_and_inventory_preserve_cumulative_work() {
    let fixture = constructors();
    let mut old = Inventory::new(&fixture.rows, fixture.foundation_rows);
    let mut new = Inventory::new(&fixture.rows, fixture.foundation_rows);
    let first = call(&mut new, OWNER, 3, &[1, 2], 0, false, true);
    assert_eq!(first, call(&mut old, OWNER, 3, &[1, 2], 0, false, false));
    succeeds(&first, 16);
    let first_expansions = counts(&new).expressions + counts(&new).levels;
    // Owner and ordered universe context both change. No old memo is reused.
    let second = call(&mut new, OTHER, 3, &[2, 1], 0, false, true);
    assert_eq!(second, call(&mut old, OTHER, 3, &[2, 1], 0, false, false));
    succeeds(&second, 32);
    assert_eq!(counts(&new).expressions + counts(&new).levels, 2 * first_expansions);
    let failure = call(&mut new, OWNER, 3, &[2], 0, false, true);
    assert_eq!(failure, call(&mut old, OWNER, 3, &[2], 0, false, false));
    refuses(&failure, "CORRESPONDENCE_UNBOUND_UNIVERSE", 34);

    // Identical numeric indices in a fresh Inventory are not authority.
    let mut changed = constructors();
    row_mut(&mut changed, "in", 6)["str"]["str"] = json!("A".repeat(64));
    refuses(&compare(&changed, 3, &[1, 2], 0, 0, false).0, "CORRESPONDENCE_DIGEST", 16);

    let small = binary_dag(1, false);
    let mut old = Inventory::new(&small.rows, small.foundation_rows);
    let mut new = Inventory::new(&small.rows, small.foundation_rows);
    old.work = MAX_NODES - 4; new.work = MAX_NODES - 4;
    for (index, expected_work) in [(1, MAX_NODES - 1), (1, MAX_NODES + 1), (0, MAX_NODES + 2)] {
        let actual = call(&mut new, OWNER, index, &[], 0, false, true);
        assert_eq!(actual, call(&mut old, OWNER, index, &[], 0, false, false));
        assert_eq!(actual.work, expected_work);
    }
}

#[test]
fn cached_sibling_preserves_first_error_and_logical_prefix() {
    let mut fixture = binary_dag(3, false);
    *row_mut(&mut fixture, "ie", 2) = json!({"ie": 2, "bvar": "bad"});
    row_mut(&mut fixture, "ie", 3)["app"] = json!({"fn": 1, "arg": 2});
    let (malformed, stats) = compare(&fixture, 3, &[], 0, MAX_NODES - 5, false);
    refuses(&malformed, "CORRESPONDENCE_UINT", MAX_NODES);
    assert!(stats.hits > 0);
    refuses(&compare(&fixture, 3, &[], 0, MAX_NODES - 4, false).0,
            "CORRESPONDENCE_EXPANSION_LIMIT", MAX_NODES + 1);
    row_mut(&mut fixture, "ie", 3)["app"] = json!({"fn": 2, "arg": 1});
    refuses(&compare(&fixture, 3, &[], 0, 0, false).0, "CORRESPONDENCE_UINT", 2);

    // A cache hit in constant universes must not move name checking earlier.
    let mut fixture = constructors();
    row_mut(&mut fixture, "ie", 3)["const"] = json!({"name": 999, "us": [0, 0, 999]});
    let (failure, stats) = compare(&fixture, 3, &[], 0, 0, false);
    refuses(&failure, "CORRESPONDENCE_LEVEL_INDEX", 4);
    assert_eq!(stats.hits, 1);
    // Projection checks the reference before its malformed index/child.
    row_mut(&mut fixture, "ie", 10)["proj"] = json!({"typeName": 999, "idx": "bad", "struct": 999});
    refuses(&compare(&fixture, 10, &[], 0, 0, false).0, "CORRESPONDENCE_NAME_INDEX", 1);
    // A let value must follow the repeated valid type, but precede its bad body.
    row_mut(&mut fixture, "ie", 6)["app"] = json!({"fn": 0, "arg": 0});
    row_mut(&mut fixture, "ie", 9)["letE"] = json!({"name": 0, "type": 6, "value": 3, "body": 999, "nondep": false});
    refuses(&compare(&fixture, 9, &[], 0, 0, false).0, "CORRESPONDENCE_LEVEL_INDEX", 8);
}

#[test]
fn unreachable_payload_scope_and_eager_inventory_checks_are_unchanged() {
    let mut fixture = binary_dag(3, false);
    *row_mut(&mut fixture, "ie", 3) = json!({"ie": 3, "unknown": "unreachable"});
    succeeds(&compare(&fixture, 1, &[], 0, 0, false).0, 3);
    refuses(&compare(&fixture, 3, &[], 0, 0, false).0, "CORRESPONDENCE_NONCANONICAL_EXPRESSION", 1);
    // Syntax payload reachability does not defer the original eager row census.
    row_mut(&mut fixture, "ie", 3)["ie"] = json!(999);
    let result = catch_unwind(AssertUnwindSafe(|| {
        let _ = Inventory::new(&fixture.rows, fixture.foundation_rows);
    })).map_err(diagnostic);
    assert!(result.unwrap_err().contains("CORRESPONDENCE_EXPRESSION_ORDER"));
}

// Test-only decoder of the selected fixed wire fixture, not a production codec.
// Outer selection pins the entire exact file hash. Bounds precede its file read.
struct Wire<'a> { bytes: &'a [u8], position: usize }
impl<'a> Wire<'a> {
    fn take(&mut self, count: usize) -> &'a [u8] {
        let end = self.position.checked_add(count).expect("fixture cursor overflow");
        let part = self.bytes.get(self.position..end).expect("truncated fixture");
        self.position = end;
        part
    }
    fn u32(&mut self) -> usize {
        u32::from_le_bytes(self.take(4).try_into().unwrap()) as usize
    }
}

fn retained_frames() -> Vec<Value> {
    let path = std::env::var_os("DMKN_PROOF_MEMO_WIRE")
        .expect("selected retained-fixture path DMKN_PROOF_MEMO_WIRE is mandatory");
    let file = std::fs::File::open(path).expect("read-only retained fixture open");
    assert_eq!(file.metadata().unwrap().len(), 215_540, "selected fixture length");
    let mut bytes = Vec::with_capacity(215_540);
    file.take(215_541).read_to_end(&mut bytes).unwrap();
    assert_eq!(bytes.len(), 215_540, "fixture changed while reading");
    let mut input = Wire { bytes: &bytes, position: 0 };
    assert_eq!(input.take(8), b"DMKNAI02");
    assert_eq!(input.u32(), 2);
    input.take(32); // image slot: outer hash pins it; not receipt verification
    assert_eq!([input.u32(), input.u32(), input.u32(), input.u32()], [1, 1, 2, 1]);
    assert_eq!(input.take(1), &[0]); // one legacy module assumption
    input.take(184);
    assert_eq!(input.u32(), 0); // frontier assumption index
    input.take(184);
    assert_eq!(input.u32(), 0); // member index
    assert_eq!(input.u32(), 0); // no siblings for legacy frontier
    input.take(184); // one target module journal
    let mut frames = Vec::new();
    for expected in [113_220, 101_687] {
        let length = input.u32();
        assert_eq!(length, expected);
        frames.push(serde_json::from_slice(input.take(length)).expect("retained delta JSON"));
    }
    assert_eq!(input.position, bytes.len(), "exact fixture EOF");
    frames
}

#[test]
fn retained_two_delta_proofs_match_and_reduce_syntax_work() {
    let frames = retained_frames();
    // Foundation prefix is exact policy::FOUNDATION_ROWS in the selected source.
    // This test does not reauthenticate it, check the kernel or verify receipts.
    const FOUNDATION_ROWS: usize = 413;
    let expected = [(1355, 1200, 101, 18_796, 459, 14), (1009, 852, 105, 184, 85, 8)];
    for (delta, (frame, (row_count, proof, theorem_name, work, unique_expr, unique_level)))
        in frames.iter().zip(expected).enumerate() {
        let rows = array(&frame["rows"]);
        assert_eq!(rows.len(), row_count);
        let theorems = rows.iter().skip(FOUNDATION_ROWS)
            .filter_map(|row| row.as_object().unwrap().get("thm")).collect::<Vec<_>>();
        assert_eq!(theorems.len(), 1, "one new theorem in each selected delta");
        let record = theorems[0];
        assert_eq!(uint(&record["value"]), proof);
        assert_eq!(uint(&record["name"]), theorem_name);
        let parameters = array(&record["levelParams"]).iter().map(uint).collect::<Vec<_>>();
        let mut old = Inventory::new(rows, FOUNDATION_ROWS);
        let mut new = Inventory::new(rows, FOUNDATION_ROWS);
        let name = array(old.name(theorem_name));
        assert!(name.len() > 3);
        assert_eq!(name[0], json!(["s", "DMKN"]));
        assert_eq!(name[1], json!(["s", "Mod"]));
        let owner_component = array(&name[2]);
        assert_eq!(owner_component[0], "s");
        let owner = text(&owner_component[1]).to_owned();
        digest(&owner);
        let baseline = call(&mut old, &owner, proof, &parameters, 0, false, false);
        let actual = call(&mut new, &owner, proof, &parameters, 0, false, true);
        assert_eq!(actual, baseline);
        succeeds(&actual, work);
        let stats = counts(&new);
        assert_eq!((stats.expressions, stats.levels), (unique_expr, unique_level));
        assert_eq!(stats.expressions + stats.levels + stats.skipped, work);
        assert!(stats.hits > 0 && stats.skipped > 0);
        println!("{}", json!({"schema":"DMKN_PROOF_MEMO_SYNTAX_CONTROL_V1",
            "delta":delta,"rows":row_count,"proof_index":proof,"logical_visits":work,
            "expression_expansions":stats.expressions,"level_expansions":stats.levels,
            "cache_hits":stats.hits,"skipped_logical_visits":stats.skipped,
            "mathematical_admission":false,"native_kernel_executed":false,
            "cost_claim":"SOURCE_REVALIDATION_OPERATIONS_NOT_CYCLES_OR_PROVING_COST"}));
    }
}
