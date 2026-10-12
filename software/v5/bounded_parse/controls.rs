//! Independent, finite changed-boundary controls. No guest/receipt/native worker.
//! The mathematical positive/invalid-proof comparison is a separate root selection.
use crate::{census, Census};
use dmkn_module_relation::{canonical as C, relation as module_relation};
use serde_json::{json, Value};

// The retained parse-once census is an independent traversal oracle. Its strict
// parser entry is intentionally unchanged in the new module crate.
#[path = "../aggregate_parse_once/census.rs"]
mod old_census;

// Exact production scanner source, compiled under cfg(test) for its counter-only
// seam. Tokens of this sibling type NEVER enter production relation/census APIs.
#[path = "canonical.rs"]
mod scanner_for_tests;

fn parse_pair(raw: &[u8], accepted: bool) -> Option<(Value, usize, usize)> {
    let old = C::parse_validated(raw);
    let new = C::parse_bounded(raw);
    assert_eq!(old.is_ok(), new.is_ok(), "strict parse domain differs: {raw:?}");
    assert_eq!(new.is_ok(), accepted, "unexpected parse result: {raw:?}");
    match (old, new) {
        (Ok(value), Ok(token)) => {
            assert_eq!(token.as_value(), &value, "decoded Value changed");
            let canonical = C::canonical(&value).unwrap();
            assert_eq!(C::canonical(token.as_value()).unwrap(), canonical);
            assert_eq!(C::canonical_size(&value).unwrap(), canonical.len());
            assert!(canonical.len() <= raw.len(), "finite lexical length control");
            Some((value, token.nodes(), token.maximum_depth()))
        }
        (Err(_), Err(_)) => None,
        _ => unreachable!("domain comparison above"),
    }
}

fn shaped() -> Value {
    json!({"schema":"not-a-module-schema", "image":[0,0,0,0,0,0,0,0], "rank":0,
        "local_spec":{}, "rows":[0,1],
        "parents":[{"journal":[],"openings":[{},{}]}],
        "bodies":[{"universes":0,"digest":"00".repeat(32),"expression":0}]})
}

fn positional() -> Value {
    json!(["not-a-module-schema", [0,0,0,0,0,0,0,0], 0, {}, [0,1],
        [[[],[{},{}]]], [[0,"00".repeat(32),0]]])
}

fn old_state(value: &old_census::Census) -> [usize; 6] {
    [value.rows, value.bodies, value.openings, value.parent_edges,
        value.nodes, value.maximum_depth]
}

fn new_state(value: &Census) -> [usize; 6] {
    [value.rows, value.bodies, value.openings, value.parent_edges,
        value.nodes, value.maximum_depth]
}

fn old_seed(value: &Census) -> old_census::Census {
    old_census::Census { rows:value.rows, bodies:value.bodies,
        openings:value.openings, parent_edges:value.parent_edges,
        nodes:value.nodes, maximum_depth:value.maximum_depth }
}

fn charge_pair(raw: &[u8], old: &mut old_census::Census, new: &mut Census) -> bool {
    let reference = old.charge(raw);
    let candidate = new.charge(raw);
    assert_eq!(reference.is_ok(), candidate.is_ok(), "aggregate acceptance differs");
    match (reference, candidate) {
        (Ok(value), Ok(token)) => {
            assert_eq!(token.as_value(), &value, "aggregate changed parsed Value");
            assert_eq!(old_state(old), new_state(new), "successful census differs");
            true
        }
        (Err(_), Err(_)) => false, // Failure order/text/partial state may differ.
        _ => unreachable!("domain comparison above"),
    }
}

#[test]
fn legal_strings_and_escape_spellings_preserve_values_and_lengths() {
    let cases = vec![
        b"null".to_vec(), b"true".to_vec(), b"false".to_vec(), br#""""#.to_vec(),
        "\"é漢🙂\"".as_bytes().to_vec(),
        br#""\"\\\/""#.to_vec(),
        br#""\b\f\n\r\t\u0000\u001F""#.to_vec(),
        br#""\u00e9\u6F22\uD83D\uDE42""#.to_vec(),
        br#" [ "\u002f", "/", "\u000A", "\n", null, false ] "#.to_vec(),
    ];
    for raw in cases { parse_pair(&raw, true); }
    let literal = parse_pair("\"🙂\"".as_bytes(), true).unwrap().0;
    let escaped = parse_pair(br#""\uD83D\uDE42""#, true).unwrap().0;
    assert_eq!(literal, escaped);
}

#[test]
fn object_keys_are_unique_decoded_strings_without_unicode_normalization() {
    let first = br#"{"b":1,"a":0,"\u0000":"\u001F"}"#;
    let second = br#" { "\u0061" : 0, "\u0000" : "\u001f", "b" : 1 } "#;
    assert_eq!(parse_pair(first, true).unwrap().0, parse_pair(second, true).unwrap().0);
    let distinct = parse_pair(br#"{"\u00e9":0,"e\u0301":1}"#, true).unwrap().0;
    assert_eq!(distinct.as_object().unwrap().len(), 2);
    assert_ne!(distinct["é"], distinct["e\u{301}"]);
    for raw in [br#"{"a":0,"a":1}"#.as_slice(),
        br#"{"a":0,"\u0061":1}"#.as_slice(),
        br#"{"outer":{"\u00e9":0,"\u00E9":1}}"#.as_slice()] {
        parse_pair(raw, false);
    }
}

#[test]
fn exact_u64_domain_rejects_float_negative_zero_and_overflow() {
    for raw in [b"0".as_slice(), b"127", b"128", b"4294967295", b"18446744073709551615"] {
        let value = parse_pair(raw, true).unwrap().0;
        assert!(value.as_u64().is_some());
    }
    for raw in [b"-1".as_slice(), b"-0", b"-0.0", b"1.0", b"1e0", b"1E+0", b"1e400",
        b"18446744073709551616", b"01", b"+1", b"1.", b".1", b"NaN", b"Infinity"] {
        parse_pair(raw, false);
    }
    let boolean = parse_pair(b"true", true).unwrap().0;
    assert!(boolean.is_boolean() && boolean.as_u64().is_none());
}

#[test]
fn strict_utf8_surrogates_and_exact_eof_are_unchanged() {
    let invalid: &[&[u8]] = &[b"", b" ", b"[", b"{\"a\":", b"[] true", b"{}[]", b"0\0",
        b"\"\xFF\"", b"\"\xC0\xAF\"", b"\"\xED\xA0\x80\"",
        br#""\uD800""#, br#""\uDD1E""#, br#""\uDD1E\uD834""#,
        br#""\uD800x""#, br#""\x41""#];
    for raw in invalid { parse_pair(raw, false); }
    parse_pair(b"\r\n\t 0 \t\r\n", true);
}

#[test]
fn cached_nodes_depth_and_immutable_borrow_match_small_exact_trees() {
    let cases: &[(&[u8], usize, usize)] = &[
        (b"null", 1, 0), (b"[]", 1, 0), (br#"{"key":0}"#, 2, 1),
        (br#"[0,{"key":[true,null]}]"#, 6, 3),
    ];
    for (raw, nodes, depth) in cases {
        let (value, actual_nodes, actual_depth) = parse_pair(raw, true).unwrap();
        assert_eq!((actual_nodes, actual_depth), (*nodes, *depth));
        let token = C::parse_bounded(raw).unwrap();
        let borrowed: &Value = token.as_value();
        assert_eq!(borrowed, &value);
        assert_eq!((token.nodes(), token.maximum_depth()), (*nodes, *depth));
        assert_eq!(token.as_value(), &value);
    }
    // API privacy/nonmutability is separately source/compile reviewed. These
    // observations do not purport to prove the absence of another constructor.
}

fn nested(containers: usize, kind: usize) -> Vec<u8> {
    assert!(containers <= 128 && kind <= 2);
    let mut raw = String::new(); let mut closes = Vec::new();
    for index in 0..containers {
        if kind == 1 || (kind == 2 && index % 2 == 1) {
            raw.push_str("{\"x\":"); closes.push('}');
        } else {
            raw.push('['); closes.push(']');
        }
    }
    raw.push('0');
    for close in closes.into_iter().rev() { raw.push(close); }
    raw.into_bytes()
}

#[test]
fn actual_serde_127_open_container_limit_is_not_value_depth_128() {
    for kind in [0, 1, 2] {
        for containers in [1, 126, 127, 128] {
            let outcome = parse_pair(&nested(containers, kind), containers <= 127);
            if let Some((_, nodes, depth)) = outcome {
                assert_eq!((nodes, depth), (containers + 1, containers));
            }
        }
    }
}

#[test]
fn parameterized_scanner_limits_test_recurrence_not_million_node_runtime() {
    let value = json!([0,{"key":[true,null]}]);
    assert_eq!(scanner_for_tests::test_shape(&value, 6, 3).unwrap(), (6, 3));
    assert!(scanner_for_tests::test_shape(&value, 5, 3).is_err());
    assert!(scanner_for_tests::test_shape(&value, 6, 2).is_err());
    assert_eq!(scanner_for_tests::test_shape(&json!(null), 1, 0).unwrap(), (1, 0));
    assert!(scanner_for_tests::test_shape(&json!(null), 0, 0).is_err());
    assert!(scanner_for_tests::test_shape(&json!([null]), 2, 0).is_err());
    // Shape alone is not strict syntax validation and never creates a token.
    assert_eq!(scanner_for_tests::test_shape(&json!(-1), 1, 0).unwrap(), (1, 0));
    assert!(C::parse_bounded(b"-1").is_err());
    assert!(C::canonical_size(&json!(-1)).is_err());
}

#[test]
fn aggregate_named_positional_and_noncanonical_successes_match_old_census() {
    let mut cases = vec![serde_json::to_vec(&shaped()).unwrap(),
        serde_json::to_vec(&positional()).unwrap()];
    cases.push(br#" { "bodies" : [], "parents" : [[[],[{},{}]]], "rows" : [0,1],
        "local_spec" : {}, "rank" : 0, "image" : [0,0,0,0,0,0,0,0],
        "schema" : "shape\u002donly" } "#.to_vec());
    let mut old = old_census::Census::default(); let mut new = Census::default();
    for raw in cases { assert!(charge_pair(&raw, &mut old, &mut new)); }
    assert_eq!((new.rows, new.bodies, new.openings, new.parent_edges), (6, 2, 6, 3));
}

#[test]
fn aggregate_shape_cumulative_caps_and_overflow_refuse_without_token() {
    let mut missing = shaped(); missing.as_object_mut().unwrap().remove("rows");
    let mut extra = shaped(); extra["unexpected"] = json!(0);
    let mut wrong_rows = shaped(); wrong_rows["rows"] = json!({});
    let mut wrong_parent = shaped(); wrong_parent["parents"] = json!([{"journal":[]}]);
    let mut wrong_openings = shaped(); wrong_openings["parents"][0]["openings"] = json!(false);
    for value in [json!(null), json!([]), missing, extra, wrong_rows, wrong_parent, wrong_openings] {
        assert!(!charge_pair(&serde_json::to_vec(&value).unwrap(),
            &mut old_census::Census::default(), &mut Census::default()));
    }
    let raw = serde_json::to_vec(&shaped()).unwrap();
    let mut reference = old_census::Census::default(); reference.charge(&raw).unwrap();
    let exact_nodes = reference.nodes;
    let maxima = [census::MAX_ROWS, census::MAX_BODIES, census::MAX_OPENINGS,
        crate::relation::MAX_EDGES, census::MAX_NODES];
    let costs = [2, 1, 2, 1, exact_nodes];
    for index in 0..5 {
        let mut new = Census::default();
        match index {
            0 => new.rows = maxima[index] - costs[index],
            1 => new.bodies = maxima[index] - costs[index],
            2 => new.openings = maxima[index] - costs[index],
            3 => new.parent_edges = maxima[index] - costs[index],
            _ => new.nodes = maxima[index] - costs[index],
        }
        let mut old = old_seed(&new);
        assert!(charge_pair(&raw, &mut old, &mut new));
        assert_eq!(new_state(&new)[index], maxima[index]);
        assert!(!charge_pair(&raw, &mut old, &mut new));
    }
    for index in 0..5 {
        let mut new = Census::default();
        match index {
            0 => new.rows = usize::MAX, 1 => new.bodies = usize::MAX,
            2 => new.openings = usize::MAX, 3 => new.parent_edges = usize::MAX,
            _ => new.nodes = usize::MAX,
        }
        let mut old = old_seed(&new);
        assert!(!charge_pair(&raw, &mut old, &mut new));
    }
    let mut new = Census { maximum_depth:100, ..Census::default() };
    let mut old = old_seed(&new);
    assert!(charge_pair(&raw, &mut old, &mut new));
    assert_eq!(new.maximum_depth, 100);
}

#[test]
fn typed_consuming_relation_and_raw_entry_preserve_early_schema_refusal() {
    for value in [shaped(), positional()] {
        let raw = serde_json::to_vec(&value).unwrap();
        let reference = module_relation::check(C::parse_validated(&raw).unwrap())
            .err().expect("deliberately invalid relation schema must refuse");
        let candidate = module_relation::check_validated(C::parse_bounded(&raw).unwrap())
            .err().expect("token is representation evidence, not mathematics");
        let raw_entry = module_relation::check_bytes(&raw)
            .err().expect("raw entry must retain validation and mathematical refusal");
        assert_eq!(reference, "relation schema/limits");
        assert_eq!(reference, candidate);
        assert_eq!(reference, raw_entry);
    }
    // No successful J is fabricated in syntax tests. The separate retained
    // mathematical comparison must check exact actual J and premises later.
}
