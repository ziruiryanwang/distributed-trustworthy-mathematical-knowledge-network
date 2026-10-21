//! Focused native controls. Conditional J/H values here are NOT receipts.

use dmkn_aggregate_relation::{header as ah, membership, relation as aggregate};
use dmkn_module_relation::{canonical::{canonical, hash, hex, require, sha, R},
    journal::Journal, relation as original};
use dmkn_rc_relation::relation as rc;
use serde_json::{json, Value};
use std::panic::{catch_unwind, AssertUnwindSafe};
use std::collections::BTreeMap;
use crate::syntax::{Arena, Node, Level, Style};
use crate::typing::Typing;

#[derive(Default)]
struct Suite {
    executed: Vec<Value>,
    refusals: Vec<String>,
    errors: Vec<Value>,
}

impl Suite {
    fn check(&mut self, name: &str, check: impl FnOnce() -> R<Value>) {
        let result = catch_unwind(AssertUnwindSafe(check));
        match result {
            Ok(Ok(detail)) => self.executed.push(json!({"name": name, "status": "PASS", "detail": detail})),
            Ok(Err(error)) => {
                self.executed.push(json!({"name": name, "status": "FAIL"}));
                self.errors.push(json!({"control": name, "error": error}));
            },
            Err(_) => {
                self.executed.push(json!({"name": name, "status": "FAIL"}));
                self.errors.push(json!({"control": name, "error": "unexpected panic, not an expected refusal"}));
            },
        }
    }

    fn refuse<T>(&mut self, name: &str, check: impl FnOnce() -> R<T>) {
        self.refusals.push(name.into());
        self.check(name, || match check() {
            Err(reason) => Ok(json!({"refusal": reason})),
            Ok(_) => Err("unexpected acceptance".into()),
        });
    }

    // Setup failure is a test failure, never evidence of the intended refusal.
    fn refuse_prepared<P, T>(&mut self, name: &str, prepare: impl FnOnce() -> R<P>,
                             check: impl FnOnce(P) -> R<T>, diagnostic: &str) {
        self.refusals.push(name.into());
        self.check(name, || {
            let prepared = prepare()?;
            match check(prepared) {
                Err(reason) => {
                    require(reason.contains(diagnostic), "unexpected refusal diagnostic")?;
                    Ok(json!({"refusal": reason}))
                },
                Ok(_) => Err("unexpected acceptance".into()),
            }
        });
    }
}

/// Independently decode only the two signatures from the exact canonical F
/// prefix. No production projection, expected index, or cached result is used
/// to derive the names/types. The final equality tests production's table.
fn independent_foundation(witness: &Value) -> R<Value> {
    let rows = witness["rows"].as_array().ok_or("fixture rows array")?;
    require(rows.len() >= crate::foundation::PREFIX_ROWS, "fixture F prefix length")?;
    let prefix = Value::Array(rows[..crate::foundation::PREFIX_ROWS].to_vec());
    let encoded = canonical(&prefix)?;
    require(encoded.len() == crate::foundation::PREFIX_BYTES
        && hex(&sha(&encoded)) == crate::foundation::PREFIX_SHA256,
        "independently pinned F canonical bytes")?;
    let mut names = BTreeMap::from([(0u64, json!([]))]);
    let mut levels = BTreeMap::new();
    let mut expressions = BTreeMap::new();
    let mut declarations = Vec::new();
    for row in prefix.as_array().unwrap() {
        if let Some(i) = row["in"].as_u64() {
            let (item, tag, suffix) = if row.get("str").is_some() {
                (&row["str"], "s", row["str"]["str"].clone())
            } else { (&row["num"], "n", row["num"]["i"].clone()) };
            let p = item["pre"].as_u64().ok_or("F name predecessor")?;
            let mut name = names.get(&p).ok_or("F name predecessor missing")?
                .as_array().ok_or("F name array")?.clone();
            name.push(json!([tag, suffix]));
            require(names.insert(i, Value::Array(name)).is_none(), "F duplicate name index")?;
        } else if let Some(i) = row["il"].as_u64() {
            require(levels.insert(i, row.clone()).is_none(), "F duplicate level index")?;
        } else if let Some(i) = row["ie"].as_u64() {
            require(expressions.insert(i, row.clone()).is_none(), "F duplicate expression index")?;
        } else if let Some(thm) = row.get("thm") { declarations.push(thm.clone());
        } else if let Some(inductive) = row.get("inductive") {
            declarations.extend(inductive["types"].as_array().ok_or("F inductive types")?.iter().cloned());
        }
    }
    fn index(v: &Value) -> R<u64> { v.as_u64().ok_or("F integer index".into()) }
    fn level(i: u64, universes: &[Value], levels: &BTreeMap<u64, Value>) -> R<Value> {
        if i == 0 { return Ok(json!(["zero"])); }
        let raw = levels.get(&i).ok_or("F level missing")?;
        let parameter = index(&raw["param"])?;
        let position = universes.iter().position(|v| v.as_u64() == Some(parameter))
            .ok_or("F parameter not in declaration scope")?;
        Ok(json!(["param", position]))
    }
    fn expression(i: u64, us: &[Value], names: &BTreeMap<u64, Value>, levels: &BTreeMap<u64, Value>,
                  expressions: &BTreeMap<u64, Value>, depth: usize) -> R<Value> {
        require(depth <= 64, "F signature traversal bound")?;
        let raw = expressions.get(&i).ok_or("F expression missing")?;
        let recurse = |n| expression(n, us, names, levels, expressions, depth + 1);
        if let Some(v) = raw.get("bvar") { return Ok(json!(["bvar", index(v)?])); }
        if let Some(v) = raw.get("sort") { return Ok(json!(["sort", level(index(v)?, us, levels)?])); }
        if let Some(v) = raw.get("const") {
            let name = names.get(&index(&v["name"])?).ok_or("F constant name missing")?;
            let ls = v["us"].as_array().ok_or("F constant universes")?.iter()
                .map(|n| level(index(n)?, us, levels)).collect::<R<Vec<_>>>()?;
            return Ok(json!(["const", ["foundation", name], ls]));
        }
        if let Some(v) = raw.get("app") {
            return Ok(json!(["app", recurse(index(&v["fn"])?)?, recurse(index(&v["arg"])?)?]));
        }
        if let Some(v) = raw.get("forallE") {
            return Ok(json!(["forall", v["binderInfo"], index(&v["name"])?,
                recurse(index(&v["type"])?)?, recurse(index(&v["body"])?)?]));
        }
        Err("F target signature uses unsupported projection form".into())
    }
    let mut found = Vec::new();
    for wanted in [json!([["s", "Eq"]]), json!([["s", "Eq"], ["s", "trans"]])] {
        let matching: Vec<_> = declarations.iter().filter(|d| d["name"].as_u64()
            .and_then(|n| names.get(&n)) == Some(&wanted)).collect();
        require(matching.len() == 1, "unique F target declaration")?;
        let d = matching[0];
        let us = d["levelParams"].as_array().ok_or("F declaration universes")?;
        found.push(json!({"name": wanted, "universe_names": us,
            "type": expression(index(&d["type"])?, us, &names, &levels, &expressions, 0)?}));
    }
    Ok(Value::Array(found))
}

fn bytes(value: &Value) -> R<Vec<u8>> {
    serde_json::from_value(value.clone()).map_err(|e| format!("fixture bytes: {e}"))
}

fn proof_body(value: &mut Value) -> &mut Value {
    let mut node = value;
    while node.get(0).and_then(Value::as_str) == Some("lam") {
        node = &mut node[3];
    }
    node
}

fn replace_first(node: &mut Value, predicate: &impl Fn(&Value) -> bool,
                 replacement: &impl Fn(&Value) -> Value) -> bool {
    if predicate(node) {
        *node = replacement(node);
        return true;
    }
    if let Some(items) = node.as_array_mut() {
        for child in items {
            if replace_first(child, predicate, replacement) { return true; }
        }
    }
    false
}

fn external_const(value: &Value) -> bool {
    value.get(0).and_then(Value::as_str) == Some("const")
        && value.get(1).and_then(|v| v.get(0)).and_then(Value::as_str) == Some("external")
}

fn foundation_const(value: &Value) -> bool {
    value.get(0).and_then(Value::as_str) == Some("const")
        && value.get(1).and_then(|v| v.get(0)).and_then(Value::as_str) == Some("foundation")
}

fn differential(frame: &Value, witness: &Value) -> R<Value> {
    for field in ["image", "rank", "local_spec", "parents"] {
        require(frame[field] == witness[field], "fixture exact common witness field")?;
    }
    require(witness["schema"] == "DMKN_CERTIFIED_MODULES_V2"
        && witness["bodies"] == json!([]), "fixture original witness profile")?;
    let checked = rc::check(frame.clone())?;
    let old = original::check(witness.clone())?;
    require(checked.journal.encode()? == old.journal.encode()?
        && checked.parent_journals == old.parent_journals,
        "RC acceptance must equal complete original J and ordered parents")?;
    Ok(json!({"module": hex(&checked.journal.module), "rank": checked.journal.rank,
        "journal_bytes": checked.journal.encode()?.len(), "parents": checked.parent_journals.len(),
        "authority": "CONDITIONAL_RELATION_ONLY"}))
}

fn u32le(out: &mut Vec<u8>, value: usize) {
    out.extend_from_slice(&u32::try_from(value).expect("bounded harness count").to_le_bytes());
}

fn prefix(image: [u32; 8], assumptions: usize, frontiers: usize, deltas: usize, targets: usize) -> Vec<u8> {
    let mut out = b"DMKNRC01".to_vec();
    u32le(&mut out, 1);
    out.extend_from_slice(&ah::image_bytes(image));
    for n in [assumptions, frontiers, deltas, targets] { u32le(&mut out, n); }
    out
}

fn delta(out: &mut Vec<u8>, frame: &Value) -> R<()> {
    let raw = canonical(frame)?;
    u32le(out, raw.len());
    out.extend_from_slice(&raw);
    Ok(())
}

fn initial_wire(first: &Value, second: Option<&Value>, image: [u32; 8], establish: bool) -> R<Vec<u8>> {
    let first_j = rc::check(first.clone())?.journal.encode()?;
    let target = match second { Some(v) => rc::check(v.clone())?.journal.encode()?, None => first_j };
    let parent = bytes(&first["parents"][0]["journal"])?;
    let mut out = prefix(image, usize::from(establish), usize::from(establish),
                         1 + usize::from(second.is_some()), 1);
    if establish {
        out.push(0); out.extend_from_slice(&parent);
        u32le(&mut out, 0); out.extend_from_slice(&parent);
        u32le(&mut out, 0); u32le(&mut out, 0);
    }
    out.extend_from_slice(&target);
    delta(&mut out, first)?;
    if let Some(second) = second { delta(&mut out, second)?; }
    Ok(out)
}

fn continued_wire(previous: &aggregate::ConditionalConclusion, second: &Value,
                  outer_image: [u32; 8]) -> R<Vec<u8>> {
    let parent = bytes(&second["parents"][0]["journal"])?;
    let position = previous.members().iter().position(|v| *v == parent)
        .ok_or("fixture first member not in first conditional aggregate")?;
    let siblings = membership::opening(previous.members(), position as u32)?;
    let target = rc::check(second.clone())?.journal.encode()?;
    let mut out = prefix(outer_image, 1, 1, 1, 1);
    out.push(1); out.extend_from_slice(&previous.header().encode()?);
    u32le(&mut out, 0); out.extend_from_slice(&parent);
    u32le(&mut out, position); u32le(&mut out, siblings.len());
    for sibling in siblings { out.extend_from_slice(&sibling); }
    out.extend_from_slice(&target);
    delta(&mut out, second)?;
    Ok(out)
}

/// Recommit a modified selected import for a conditional-negative test. This
/// constructs inert premise bytes, NOT a receipt or a warrant of its validity.
fn changed_import(mut frame: Value, change: impl FnOnce(&mut Value)) -> R<Value> {
    let old_bytes = bytes(&frame["parents"][0]["journal"])?;
    let mut journal = Journal::decode(&old_bytes)?;
    let old_module = hex(&journal.module);
    let mut group = frame["parents"][0]["openings"][0]["group"].clone();
    change(&mut group);
    journal.group_count = 1;
    journal.group_root = hash("group-leaf", &json!({"index": 0, "group": group}))?;
    journal.module = hash("module-spec", &journal.summary())?;
    let new_module = hex(&journal.module);
    let opening = json!({"schema": "DMKN_MODULE_GROUP_OPENING_V1", "summary": journal.summary(),
        "index": 0, "group": group, "siblings": []});
    frame["parents"] = json!([{"journal": journal.encode()?, "openings": [opening]}]);
    fn relocate(value: &mut Value, old: &str, new: &str) {
        if value.get(0).and_then(Value::as_str) == Some("external")
            && value.get(1).and_then(Value::as_str) == Some(old) {
            value[1] = json!(new);
        }
        match value {
            Value::Array(items) => for child in items { relocate(child, old, new); },
            Value::Object(items) => for child in items.values_mut() { relocate(child, old, new); },
            _ => {},
        }
    }
    relocate(&mut frame["proofs"], &old_module, &new_module);
    relocate(&mut frame["local_spec"], &old_module, &new_module);
    Ok(frame)
}

pub fn run(input: Value) -> Value {
    let mut suite = Suite::default();
    let first = &input["first"];
    let second = &input["second"];
    suite.check("first_exact_original_refinement", || differential(first, &input["first_witness"]));
    suite.check("second_exact_original_refinement", || differential(second, &input["second_witness"]));
    suite.check("second_uses_exact_first_conclusion", || {
        require(bytes(&second["parents"][0]["journal"])? == rc::check(first.clone())?.journal.encode()?,
            "second exact first premise")?;
        Ok(json!({"conditional": true, "receipt_authority": false}))
    });

    let mutations: Vec<(&str, Value)> = {
        let mut entries = Vec::new();
        let mut v = first.clone(); v["image"][0] = json!(v["image"][0].as_u64().unwrap() ^ 1);
        entries.push(("wrong_semantic_image", v));
        let mut v = first.clone(); v["rank"] = json!(v["rank"].as_u64().unwrap() + 1);
        entries.push(("wrong_exact_rank", v));
        let mut v = first.clone(); v["rows"] = json!([]);
        entries.push(("extra_legacy_rows_field", v));
        let mut v = first.clone(); v["proofs"] = json!([]);
        entries.push(("proof_count_mismatch", v));
        let mut v = first.clone(); v["proofs"][0] = json!(["bvar", 0]);
        entries.push(("loose_proof_bvar", v));
        let mut v = first.clone(); v["proofs"][0][2] = json!(["bvar", 0]);
        entries.push(("free_binder_domain", v));
        let mut v = first.clone(); v["proofs"][0][1] = json!("unknown-style");
        entries.push(("unknown_binder_style", v));
        let mut v = first.clone(); v["proofs"][0][2] = json!(["sort", ["param", 4]]);
        entries.push(("out_of_scope_universe", v));
        let mut v = first.clone(); v["proofs"][0][2] = json!(["sort", ["succ", ["zero"]]]);
        entries.push(("unsupported_public_successor_level", v));
        let mut v = first.clone(); *proof_body(&mut v["proofs"][0]) = json!(["let", "default", ["sort", ["zero"]], ["bvar", 0], ["bvar", 0]]);
        entries.push(("unsupported_let", v));
        let mut v = first.clone(); proof_body(&mut v["proofs"][0])[2] = json!(["bvar", 2]);
        entries.push(("wrong_composition_argument", v));
        let mut v = first.clone(); v["local_spec"]["groups"][0]["declarations"][0]["type"] = json!(["sort", ["zero"]]);
        entries.push(("nonproposition_theorem_type", v));
        let mut v = first.clone(); v["local_spec"]["groups"][0]["declarations"][0]["meta"] = json!({"trusted": true});
        entries.push(("extra_theorem_metadata", v));
        let mut v = first.clone();
        let name = v["local_spec"]["groups"][0]["declarations"][0]["name"].clone();
        *proof_body(&mut v["proofs"][0]) = json!(["const", ["local", name], [["param", 0], ["param", 1], ["param", 2], ["param", 3]]]);
        entries.push(("self_reference_not_earlier_local", v));
        entries
    };
    for (name, value) in mutations { suite.refuse(name, || rc::check(value)); }

    suite.refuse_prepared("changed_parent_group_path", || {
        let mut v = first.clone();
        require(v["parents"][0]["openings"][0]["siblings"].as_array()
            .map_or(false, |v| !v.is_empty()), "fixture opening has a path")?;
        v["parents"][0]["openings"][0]["siblings"][0] = json!("00".repeat(32));
        Ok(v)
    }, rc::check, "");
    suite.refuse_prepared("wrong_constant_universe_arity", || {
        let mut v = first.clone();
        require(replace_first(&mut v["proofs"][0], &external_const, &|node| {
            let mut n = node.clone(); n[2].as_array_mut().unwrap().pop(); n
        }), "fixture contains an external constant")?;
        Ok(v)
    }, rc::check, "RC constant exact universe arity");
    suite.refuse_prepared("unavailable_foundation_constant", || {
        let mut v = first.clone();
        require(replace_first(&mut v["proofs"][0], &foundation_const, &|node| {
            let mut n = node.clone(); n[1][1] = json!([["s", "UnadoptedAxiom"]]); n
        }), "fixture contains a foundation constant")?;
        Ok(v)
    }, rc::check, "RC missing authenticated type dependency");
    suite.refuse_prepared("imported_definition_is_not_a_sealed_theorem", || {
        changed_import(first.clone(), |group| {
            group["declarations"][0]["kind"] = json!("definition");
            group["declarations"][0]["value_hash"] = json!("11".repeat(32));
        })
    }, rc::check, "RC theorem only");
    suite.refuse_prepared("missing_import_type_reference_closure", || {
        let mut changed = false;
        let value = changed_import(first.clone(), |group| {
            changed = replace_first(&mut group["declarations"][0]["type"], &foundation_const, &|node| {
                let mut n = node.clone();
                n[1] = json!(["external", "ee".repeat(32), [["s", "MissingType"]]]); n
            });
        })?;
        require(changed, "fixture imported type has a foundation constant")?;
        Ok(value)
    }, rc::check, "RC missing authenticated type dependency");

    // An arbitrary nonzero, distinct image is only a conditional test label.
    // No control claims a cryptographic receipt exists for this image.
    let image = [0x52433031u32; 8];
    suite.check("conditional_two_delta_target_closure", || {
        let wire = initial_wire(first, Some(second), image, true)?;
        let out = aggregate::check_bytes(&wire)?;
        require(out.members().len() == 3 && out.edges() == 2 && out.census().frames == 2
            && out.assumptions().len() == 1 && out.assumptions()[0].image() == ah::relation_image()
            && out.assumptions()[0].journal() == bytes(&first["parents"][0]["journal"])?
            && out.wire_bytes() == wire.len(), "conditional exact two-delta graph")?;
        Ok(json!({"members": 3, "pending_real_receipts": 1, "receipt_verified": false,
            "expression_visits": out.census().expr_visits}))
    });
    suite.check("conditional_same_image_member_continuation", || {
        let previous = aggregate::check_bytes(&initial_wire(first, None, image, true)?)?;
        let out = aggregate::check_bytes(&continued_wire(&previous, second, image)?)?;
        require(out.members().len() == 2 && out.edges() == 1 && out.header().seal_height == 2
            && out.assumptions().len() == 1 && out.assumptions()[0].image() == image
            && out.assumptions()[0].journal() == previous.header().encode()?,
            "conditional recursive exact-image claim")?;
        Ok(json!({"pending_real_receipts": 1, "receipt_verified": false}))
    });
    suite.refuse_prepared("aggregate_wrong_parent_image", || {
        let previous = aggregate::check_bytes(&initial_wire(first, None, image, true)?)?;
        continued_wire(&previous, second, [0x52433032u32; 8])
    }, |wire| aggregate::check_bytes(&wire), "");
    suite.refuse_prepared("aggregate_unestablished_exact_premise",
        || initial_wire(first, None, image, false),
        |wire| aggregate::check_bytes(&wire), "");
    suite.refuse_prepared("aggregate_exact_eof", || {
        let mut wire = initial_wire(first, None, image, true)?; wire.push(0);
        Ok(wire)
    }, |wire| aggregate::check_bytes(&wire), "RC aggregate exact EOF");
    suite.refuse_prepared("aggregate_old_magic", || {
        let mut wire = initial_wire(first, None, image, true)?;
        wire[..8].copy_from_slice(b"DMKNA001"); Ok(wire)
    }, |wire| aggregate::check_bytes(&wire), "");
    suite.refuse("frame_length_before_allocation", || {
        let mut raw = Vec::new(); u32le(&mut raw, crate::census::MAX_FRAME_BYTES + 1);
        crate::wire::Reader::new(std::io::Cursor::new(raw)).frame()
    });
    suite.refuse("duplicate_JSON_field", || {
        crate::census::Census::default().charge(b"{\"schema\":1,\"schema\":2}")
    });

    suite.check("exact_foundation_signature_projection", || {
        require(independent_foundation(&input["first_witness"])?
            == crate::foundation::signature_projection(), "exact F signature projection")?;
        Ok(json!({"prefix_rows": 413, "prefix_bytes": 23313, "signature_count": 2}))
    });
    suite.check("binder_origin_comparison_is_root_only", || {
        let mut tc = Typing::new()?;
        let z = tc.arena.level(Level::Zero)?;
        let p = tc.arena.node(Node::Sort(z))?;
        let b = tc.arena.node(Node::Bvar(0))?;
        let left = tc.arena.node(Node::Pi { origin: 0, style: Style::Default, domain: p, body: b })?;
        let right = tc.arena.node(Node::Pi { origin: 4, style: Style::Implicit, domain: p, body: b })?;
        require(left != right && tc.compare(left, right)?, "actual root binder alpha branch")?;
        let head = tc.arena.node(Node::Local(1_000_000, p))?;
        let a = tc.arena.node(Node::App(head, left))?;
        let b = tc.arena.node(Node::App(head, right))?;
        require(!tc.compare(a, b)?, "no nested application alpha congruence")?;
        Ok(json!({"root_binder_equal": true, "application_equal": false}))
    });
    suite.check("simultaneous_universe_substitution", || {
        let mut tc = Typing::new()?;
        let p0 = tc.arena.level(Level::Param(0))?;
        let p1 = tc.arena.level(Level::Param(1))?;
        let z = tc.arena.level(Level::Zero)?;
        let s = tc.arena.node(Node::Sort(p0))?;
        let out = tc.subst_levels(s, &[p1, z])?;
        require(tc.arena.nodes[out] == Node::Sort(p1), "replacement must not be resubstituted")?;
        Ok(json!({"replacement_param": 1, "not_zero": true}))
    });
    suite.check("capture_safe_open_under_binder", || {
        let mut tc = Typing::new()?;
        let z = tc.arena.level(Level::Zero)?;
        let p = tc.arena.node(Node::Sort(z))?;
        let replacement = tc.arena.node(Node::Local(1_000_000, p))?;
        let b0 = tc.arena.node(Node::Bvar(0))?;
        let b1 = tc.arena.node(Node::Bvar(1))?;
        let body = tc.arena.node(Node::App(b1, b0))?;
        let input = tc.arena.node(Node::Pi { origin: 0, style: Style::Default, domain: b0, body })?;
        let out = tc.open(input, replacement)?;
        let expected_body = tc.arena.node(Node::App(replacement, b0))?;
        require(tc.arena.nodes[out] == Node::Pi { origin: 0, style: Style::Default,
            domain: replacement, body: expected_body }, "outer substitution preserves inner binder")?;
        let reason = tc.open(b1, replacement).err().ok_or("unopened outer variable accepted")?;
        require(reason.contains("RC unopened outer variable"), "opening refusal reason")?;
        Ok(json!({"capture_avoided": true, "unopened_outer_refused": true}))
    });
    suite.check("raw_imax_zero_comparison_is_root_only", || {
        let mut tc = Typing::new()?;
        let z = tc.arena.level(Level::Zero)?;
        let u = tc.arena.level(Level::Param(0))?;
        let iz = tc.arena.level(Level::IMax(u, z))?;
        let chain = tc.arena.level(Level::IMax(u, iz))?;
        let nonzero = tc.arena.level(Level::IMax(z, u))?;
        let sz = tc.arena.node(Node::Sort(z))?;
        let sc = tc.arena.node(Node::Sort(chain))?;
        let sn = tc.arena.node(Node::Sort(nonzero))?;
        require(sz != sc && tc.compare(sz, sc)? && tc.compare(sc, sz)?, "root zero chain equality")?;
        require(!tc.compare(sz, sn)?, "unknown/nonzero right chain is not zero")?;
        let head = tc.arena.node(Node::Local(1_000_000, sz))?;
        let a = tc.arena.node(Node::App(head, sz))?;
        let b = tc.arena.node(Node::App(head, sc))?;
        require(!tc.compare(a, b)?, "no nested zero normalization")?;
        // Exercise the production infer-Pi path, not just raw node construction.
        let proof_type = tc.arena.node(Node::Local(1_000_001, sz))?;
        let pi = tc.arena.node(Node::Pi { origin: 0, style: Style::Default,
            domain: sz, body: proof_type })?;
        let inferred = tc.infer(pi)?;
        let Node::Sort(l) = tc.arena.nodes[inferred] else { return Err("Pi sort required".into()); };
        require(matches!(tc.arena.levels[l], Level::IMax(_, right) if right == z),
            "infer-Pi preserves raw imax structure")?;
        Ok(json!({"root_zero_equal": true, "nested_equal": false, "raw_inference_preserved": true}))
    });
    suite.refuse_prepared("syntactic_beta_redex_refused", || Ok(json!(["app",
        ["lam", "default", ["sort", ["zero"]], ["bvar", 0]], ["sort", ["zero"]]])),
        |v| Arena::new().parse_expr(&v, [0; 32], 0), "RC syntactic beta redex unsupported");
    suite.check("source_counter_exact_boundary", || {
        let mut arena = Arena::new();
        arena.census.expr_visits = crate::syntax::MAX_EXPR_VISITS - 1;
        let v = json!(["sort", ["zero"]]);
        arena.parse_expr(&v, [0; 32], 0)?;
        require(arena.census.expr_visits == crate::syntax::MAX_EXPR_VISITS, "exact source cap")?;
        let reason = arena.parse_expr(&v, [0; 32], 0).err().ok_or("source cap overflow accepted")?;
        require(reason.contains("RC source expression visits"), "source overflow diagnostic")?;
        Ok(json!({"accepted_cap": crate::syntax::MAX_EXPR_VISITS, "next_refused": true}))
    });
    suite.check("work_counter_exact_boundary", || {
        let mut arena = Arena::new();
        arena.census.inference_work = crate::syntax::MAX_WORK - 1;
        arena.charge()?;
        require(arena.census.inference_work == crate::syntax::MAX_WORK, "exact work cap")?;
        let reason = arena.charge().err().ok_or("work overflow accepted")?;
        require(reason.contains("RC inference work"), "work overflow diagnostic")?;
        arena.census.inference_work = usize::MAX;
        let reason = arena.charge().err().ok_or("counter arithmetic overflow accepted")?;
        require(reason.contains("RC counter overflow"), "counter overflow diagnostic")?;
        Ok(json!({"accepted_cap": crate::syntax::MAX_WORK, "next_and_overflow_refused": true}))
    });
    suite.check("aggregate_source_counter_is_shared", || {
        let mut census = crate::census::Census::default();
        let half = dmkn_rc_relation::syntax::SourceCensus { expr_visits: 4096, ..Default::default() };
        census.charge_source(&half)?; census.charge_source(&half)?;
        require(census.expr_visits == 8192, "whole-stream source charge")?;
        let one = dmkn_rc_relation::syntax::SourceCensus { expr_visits: 1, ..Default::default() };
        let reason = census.charge_source(&one).err().ok_or("shared source cap overflow accepted")?;
        require(reason.contains("RC aggregate expression visits"), "aggregate source diagnostic")?;
        Ok(json!({"acceptance_cap": 8192, "core_charge_is_post_work": true}))
    });
    suite.check("aggregate_work_counter_is_shared", || {
        let mut census = crate::census::Census::default();
        let frame = dmkn_rc_relation::syntax::SourceCensus { inference_work: 200000, ..Default::default() };
        for _ in 0..16 { census.charge_source(&frame)?; }
        require(census.inference_work == 3_200_000, "whole-stream work charge")?;
        let one = dmkn_rc_relation::syntax::SourceCensus { inference_work: 1, ..Default::default() };
        let reason = census.charge_source(&one).err().ok_or("aggregate work overflow accepted")?;
        require(reason.contains("RC aggregate inference work"), "aggregate work diagnostic")?;
        Ok(json!({"accepted_cap": 3200000, "no_per_frame_reset": true}))
    });
    json!({"schema": "DMKN_RC0_CONTROLS_V1", "status": if suite.errors.is_empty() {"PASS"} else {"FAIL"},
        "executed_count": suite.executed.len(), "executed": suite.executed,
        "expected_refusals": suite.refusals, "errors": suite.errors,
        "authority": "NATIVE_CONDITIONAL_CONTROLS_NOT_RECEIPT_AUTHORITY",
        "crypto_produced": false, "global_growth_claim": false})
}
