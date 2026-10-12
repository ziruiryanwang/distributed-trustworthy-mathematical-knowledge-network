//! Independent native-row/codec structural correspondence.
//!
//! Hash equations, foundation adoption and module certificates are deliberately
//! UNDISCHARGED here. The guest wrapper must authenticate these exact inputs and
//! then parse/check the same rows; a successful host-side report is not authority.

use serde::Deserialize;
use serde_json::{json, Value};
use std::collections::{BTreeMap, BTreeSet};

const MAX_NODES: usize = 250_000;
const MAX_DECLARATIONS: usize = 16_384;
const MAX_DEPTH: usize = 192;

#[derive(Clone, Debug, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct GroupBinding {
    pub owner: String,
    pub imported: bool,
    pub descriptor: Value,
}

#[derive(Clone, Debug, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct BodyOpening {
    pub universes: usize,
    pub digest: String,
    pub expression: Value,
}

#[derive(Clone, Debug)]
pub struct MatchedGroup {
    pub owner: String,
    pub imported: bool,
    pub export_name_indices: Vec<u32>,
}

#[derive(Clone, Debug)]
pub struct StructuralCorrespondence {
    pub status: &'static str,
    pub groups: Vec<MatchedGroup>,
    pub foundation_name_indices: Vec<u32>,
    /// Recompute codec hash_value("body", {universes,expr}) for EACH opening.
    pub body_hash_obligations: Vec<BodyOpening>,
    pub hash_verification_performed: bool,
    pub mathematical_admission: bool,
}

fn fields(value: &Value, expected: &[&str]) {
    let object = value.as_object().expect("CORRESPONDENCE_OBJECT");
    assert_eq!(object.len(), expected.len(), "CORRESPONDENCE_FIELDS");
    assert!(expected.iter().all(|key| object.contains_key(*key)), "CORRESPONDENCE_FIELDS");
}

fn uint(value: &Value) -> usize {
    usize::try_from(value.as_u64().expect("CORRESPONDENCE_UINT")).expect("CORRESPONDENCE_UINT_RANGE")
}

fn text(value: &Value) -> &str { value.as_str().expect("CORRESPONDENCE_STRING") }

fn digest(value: &str) {
    assert!(value.len() == 64 && value.bytes().all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b)),
            "CORRESPONDENCE_DIGEST");
}

fn array(value: &Value) -> &[Value] { value.as_array().expect("CORRESPONDENCE_ARRAY") }

/// Move already reconstructed children into one tagged array. Interpolating
/// those Values through json! calls serde_json::to_value(&child), recursively
/// copying the entire child tree again at every ancestor. This constructor
/// changes neither the Value shape nor validation/visit ordering.
fn tagged<const N: usize>(tag: &str, children: [Value; N]) -> Value {
    let mut values = Vec::with_capacity(N + 1);
    values.push(Value::String(tag.to_owned()));
    values.extend(children);
    Value::Array(values)
}

fn name_parts(value: &Value, maximum: usize) {
    let parts = array(value);
    assert!(!parts.is_empty() && parts.len() <= maximum, "CORRESPONDENCE_NAME_PARTS");
    for part in parts {
        let pair = array(part);
        assert_eq!(pair.len(), 2, "CORRESPONDENCE_NAME_PART");
        match text(&pair[0]) {
            "s" => {
                let string = text(&pair[1]);
                assert!(!string.is_empty() && string.len() <= 1024 && !string.contains('\0'),
                        "CORRESPONDENCE_NAME_STRING");
            },
            "n" => { assert!(uint(&pair[1]) <= u32::MAX as usize, "CORRESPONDENCE_NAME_NUM"); },
            _ => panic!("CORRESPONDENCE_NAME_TAG"),
        }
    }
}

fn absolute(owner: &str, relative: &Value) -> Value {
    digest(owner);
    name_parts(relative, 64);
    let mut result = vec![json!(["s", "DMKN"]), json!(["s", "Mod"]), json!(["s", owner])];
    result.extend_from_slice(array(relative));
    Value::Array(result)
}

struct Inventory<'a> {
    names: Vec<Value>,
    levels: Vec<&'a Value>,
    expressions: Vec<&'a Value>,
    groups: Vec<&'a Value>,
    foundation_names: BTreeSet<u32>,
    work: usize,
}

impl<'a> Inventory<'a> {
    fn new(rows: &'a [Value], foundation_rows: usize) -> Self {
        assert!(!rows.is_empty() && rows.len() <= MAX_NODES, "CORRESPONDENCE_ROW_LIMIT");
        assert!(foundation_rows > 0 && foundation_rows <= rows.len(), "CORRESPONDENCE_FOUNDATION_PREFIX");
        fields(&rows[0], &["meta"]);
        let mut this = Self { names: vec![json!([])], levels: Vec::new(), expressions: Vec::new(),
            groups: Vec::new(), foundation_names: BTreeSet::new(), work: 0 };
        for (position, row) in rows.iter().enumerate().skip(1) {
            let object = row.as_object().expect("CORRESPONDENCE_ROW");
            let indexes = ["in", "il", "ie"].into_iter().filter(|tag| object.contains_key(*tag)).collect::<Vec<_>>();
            if indexes.is_empty() {
                assert_eq!(object.len(), 1, "CORRESPONDENCE_DECLARATION_ROW");
                if position < foundation_rows {
                    for value in Self::declaration_records(row) {
                        let index = u32::try_from(uint(&value["name"])).expect("CORRESPONDENCE_NAME_INDEX");
                        let name = this.name(index as usize);
                        let parts = array(name);
                        assert!(parts[0] != json!(["s", "_nested"]), "RESERVED_NESTED_FOUNDATION_NAMESPACE");
                        assert!(!(parts.len() > 1 && parts[0] == json!(["s", "DMKN"])
                                  && parts[1] == json!(["s", "Mod"])), "RESERVED_MODULE_FOUNDATION_NAMESPACE");
                        assert!(this.foundation_names.insert(index), "DUPLICATE_FOUNDATION_DECLARATION");
                    }
                } else {
                    this.groups.push(row);
                }
                continue;
            }
            assert_eq!(indexes.len(), 1, "CORRESPONDENCE_DAG_DOMAIN");
            assert_eq!(object.len(), 2, "CORRESPONDENCE_DAG_FIELDS");
            let tag = indexes[0];
            let index = uint(&row[tag]);
            let (kind, value) = object.iter().find(|(key, _)| key.as_str() != tag).unwrap();
            match tag {
                "in" => {
                    assert_eq!(index, this.names.len(), "CORRESPONDENCE_NAME_ORDER");
                    fields(value, if kind == "str" { &["pre", "str"] } else { &["pre", "i"] });
                    let parent = uint(&value["pre"]);
                    assert!(parent < index, "CORRESPONDENCE_NAME_BACKREF");
                    let mut parts = array(&this.names[parent]).to_vec();
                    parts.push(match kind.as_str() {
                        "str" => json!(["s", value["str"]]),
                        "num" => json!(["n", value["i"]]),
                        _ => panic!("CORRESPONDENCE_NATIVE_NAME_TAG"),
                    });
                    let name = Value::Array(parts);
                    name_parts(&name, 67);
                    this.names.push(name);
                },
                "il" => {
                    assert_eq!(index, this.levels.len() + 1, "CORRESPONDENCE_LEVEL_ORDER");
                    this.levels.push(row);
                },
                "ie" => {
                    assert_eq!(index, this.expressions.len(), "CORRESPONDENCE_EXPRESSION_ORDER");
                    this.expressions.push(row);
                },
                _ => unreachable!(),
            }
        }
        this
    }

    fn declaration_records(row: &'a Value) -> Vec<&'a Value> {
        let object = row.as_object().unwrap();
        let (tag, value) = object.iter().next().unwrap();
        if tag == "inductive" {
            fields(value, &["types", "ctors", "recs"]);
            ["types", "ctors", "recs"].into_iter().flat_map(|key| array(&value[key])).collect()
        } else {
            assert!(["def", "thm", "opaque", "axiom", "quot", "moduleImportDef", "moduleImportOpaque",
                     "moduleImportTheorem"].contains(&tag.as_str()), "CORRESPONDENCE_DECLARATION_TAG");
            vec![value]
        }
    }

    fn visit(&mut self, depth: usize) {
        self.work += 1;
        assert!(depth <= MAX_DEPTH && self.work <= MAX_NODES, "CORRESPONDENCE_EXPANSION_LIMIT");
    }

    fn name(&self, index: usize) -> &Value {
        assert!(index > 0 && index < self.names.len(), "CORRESPONDENCE_NAME_INDEX");
        &self.names[index]
    }

    fn reference(&self, owner: &str, index: usize) -> Value {
        let name = self.name(index);
        let parts = array(name);
        if parts.len() > 3 && parts[0] == json!(["s", "DMKN"]) && parts[1] == json!(["s", "Mod"]) {
            let component = array(&parts[2]);
            assert_eq!(component[0], "s", "CORRESPONDENCE_MODULE_COMPONENT");
            let module = text(&component[1]);
            digest(module);
            let relative = Value::Array(parts[3..].to_vec());
            name_parts(&relative, 64);
            if module == owner { tagged("local", [relative]) }
            else { tagged("external", [Value::String(module.to_owned()), relative]) }
        } else {
            assert!(self.foundation_names.contains(&u32::try_from(index).unwrap()), "CORRESPONDENCE_UNKNOWN_FOUNDATION_NAME");
            tagged("foundation", [name.clone()])
        }
    }

    fn level(&mut self, index: usize, parameters: &[usize], depth: usize) -> Value {
        self.visit(depth);
        if index == 0 { return tagged("zero", []); }
        let row = *self.levels.get(index - 1).expect("CORRESPONDENCE_LEVEL_INDEX");
        let (tag, value) = row.as_object().unwrap().iter().find(|(key, _)| key.as_str() != "il").unwrap();
        match tag.as_str() {
            "param" => {
                let name = uint(value);
                self.name(name);
                let position = parameters.iter().position(|n| *n == name).expect("CORRESPONDENCE_UNBOUND_UNIVERSE");
                tagged("param", [json!(position)])
            },
            "succ" => {
                let child = uint(value);
                assert!(child < index, "CORRESPONDENCE_LEVEL_BACKREF");
                tagged("succ", [self.level(child, parameters, depth + 1)])
            },
            "max" | "imax" => {
                let pair = array(value);
                assert_eq!(pair.len(), 2, "CORRESPONDENCE_LEVEL_PAIR");
                let a = uint(&pair[0]); let b = uint(&pair[1]);
                assert!(a < index && b < index, "CORRESPONDENCE_LEVEL_BACKREF");
                tagged(tag, [self.level(a, parameters, depth + 1), self.level(b, parameters, depth + 1)])
            },
            _ => panic!("CORRESPONDENCE_LEVEL_TAG"),
        }
    }

    fn expression(&mut self, owner: &str, index: usize, parameters: &[usize], depth: usize) -> Value {
        self.visit(depth);
        let row = *self.expressions.get(index).expect("CORRESPONDENCE_EXPRESSION_INDEX");
        let (tag, value) = row.as_object().unwrap().iter().find(|(key, _)| key.as_str() != "ie").unwrap();
        let sub = |this: &mut Self, value: &Value| {
            let child = uint(value);
            assert!(child < index, "CORRESPONDENCE_EXPRESSION_BACKREF");
            this.expression(owner, child, parameters, depth + 1)
        };
        match tag.as_str() {
            "bvar" => tagged("bvar", [json!(uint(value))]),
            "sort" => tagged("sort", [self.level(uint(value), parameters, depth + 1)]),
            "const" => {
                fields(value, &["name", "us"]);
                let levels = array(&value["us"]);
                assert!(levels.len() <= 256, "CORRESPONDENCE_UNIVERSE_ARITY");
                let levels = levels.iter().map(|level| self.level(uint(level), parameters, depth + 1)).collect::<Vec<_>>();
                tagged("const", [self.reference(owner, uint(&value["name"])), Value::Array(levels)])
            },
            "app" => {
                fields(value, &["fn", "arg"]);
                tagged("app", [sub(self, &value["fn"]), sub(self, &value["arg"])])
            },
            "lam" | "forallE" => {
                fields(value, &["name", "type", "body", "binderInfo"]);
                assert!(uint(&value["name"]) < self.names.len(), "CORRESPONDENCE_BINDER_NAME");
                assert!(["default", "implicit", "strictImplicit", "instImplicit"].contains(&text(&value["binderInfo"])),
                        "CORRESPONDENCE_BINDER_STYLE");
                tagged(if tag == "lam" { "lam" } else { "forall" }, [value["binderInfo"].clone(),
                       sub(self, &value["type"]), sub(self, &value["body"])])
            },
            "letE" => {
                fields(value, &["name", "type", "value", "body", "nondep"]);
                assert!(uint(&value["name"]) < self.names.len(), "CORRESPONDENCE_BINDER_NAME");
                assert_eq!(value["nondep"], false, "CORRESPONDENCE_CANONICAL_NONDEP");
                tagged("let", [sub(self, &value["type"]), sub(self, &value["value"]), sub(self, &value["body"])])
            },
            "proj" => {
                fields(value, &["typeName", "idx", "struct"]);
                tagged("proj", [self.reference(owner, uint(&value["typeName"])), json!(uint(&value["idx"])),
                       sub(self, &value["struct"])])
            },
            _ => panic!("CORRESPONDENCE_NONCANONICAL_EXPRESSION"),
        }
    }

    // Validate the same unfolded proof syntax without materializing the discarded
    // expression/level Value tree. Preserve visit/check order and use the exact
    // original reference routine; committed types/bodies still use expression().
    fn validate_level(&mut self, index: usize, parameters: &[usize], depth: usize) {
        self.visit(depth);
        if index == 0 { return; }
        let row = *self.levels.get(index - 1).expect("CORRESPONDENCE_LEVEL_INDEX");
        let (tag, value) = row.as_object().unwrap().iter().find(|(key, _)| key.as_str() != "il").unwrap();
        match tag.as_str() {
            "param" => {
                let name = uint(value);
                self.name(name);
                let _position = parameters.iter().position(|n| *n == name).expect("CORRESPONDENCE_UNBOUND_UNIVERSE");
            },
            "succ" => {
                let child = uint(value);
                assert!(child < index, "CORRESPONDENCE_LEVEL_BACKREF");
                self.validate_level(child, parameters, depth + 1);
            },
            "max" | "imax" => {
                let pair = array(value);
                assert_eq!(pair.len(), 2, "CORRESPONDENCE_LEVEL_PAIR");
                let a = uint(&pair[0]); let b = uint(&pair[1]);
                assert!(a < index && b < index, "CORRESPONDENCE_LEVEL_BACKREF");
                self.validate_level(a, parameters, depth + 1);
                self.validate_level(b, parameters, depth + 1);
            },
            _ => panic!("CORRESPONDENCE_LEVEL_TAG"),
        }
    }

    fn validate_expression(&mut self, owner: &str, index: usize, parameters: &[usize], depth: usize) {
        self.visit(depth);
        let row = *self.expressions.get(index).expect("CORRESPONDENCE_EXPRESSION_INDEX");
        let (tag, value) = row.as_object().unwrap().iter().find(|(key, _)| key.as_str() != "ie").unwrap();
        let sub = |this: &mut Self, value: &Value| {
            let child = uint(value);
            assert!(child < index, "CORRESPONDENCE_EXPRESSION_BACKREF");
            this.validate_expression(owner, child, parameters, depth + 1)
        };
        match tag.as_str() {
            "bvar" => { let _index = uint(value); },
            "sort" => { self.validate_level(uint(value), parameters, depth + 1); },
            "const" => {
                fields(value, &["name", "us"]);
                let levels = array(&value["us"]);
                assert!(levels.len() <= 256, "CORRESPONDENCE_UNIVERSE_ARITY");
                for level in levels { self.validate_level(uint(level), parameters, depth + 1); }
                drop(self.reference(owner, uint(&value["name"])));
            },
            "app" => {
                fields(value, &["fn", "arg"]);
                sub(self, &value["fn"]);
                sub(self, &value["arg"]);
            },
            "lam" | "forallE" => {
                fields(value, &["name", "type", "body", "binderInfo"]);
                assert!(uint(&value["name"]) < self.names.len(), "CORRESPONDENCE_BINDER_NAME");
                assert!(["default", "implicit", "strictImplicit", "instImplicit"].contains(&text(&value["binderInfo"])),
                        "CORRESPONDENCE_BINDER_STYLE");
                sub(self, &value["type"]);
                sub(self, &value["body"]);
            },
            "letE" => {
                fields(value, &["name", "type", "value", "body", "nondep"]);
                assert!(uint(&value["name"]) < self.names.len(), "CORRESPONDENCE_BINDER_NAME");
                assert_eq!(value["nondep"], false, "CORRESPONDENCE_CANONICAL_NONDEP");
                sub(self, &value["type"]);
                sub(self, &value["value"]);
                sub(self, &value["body"]);
            },
            "proj" => {
                fields(value, &["typeName", "idx", "struct"]);
                drop(self.reference(owner, uint(&value["typeName"])));
                let _index = uint(&value["idx"]);
                sub(self, &value["struct"]);
            },
            _ => panic!("CORRESPONDENCE_NONCANONICAL_EXPRESSION"),
        }
    }
}

fn body_match(inventory: &mut Inventory<'_>, owner: &str, index: &Value, parameters: &[usize],
              commitment: &Value, bodies: &BTreeMap<(usize, String), &BodyOpening>, used: &mut BTreeSet<(usize, String)>) {
    let commitment = text(commitment);
    digest(commitment);
    let key = (parameters.len(), commitment.to_owned());
    let opening = bodies.get(&key).expect("CORRESPONDENCE_BODY_OPENING_MISSING");
    assert_eq!(inventory.expression(owner, uint(index), parameters, 0), opening.expression,
               "CORRESPONDENCE_BODY_EXPRESSION");
    used.insert(key);
}

fn mapped_names(owner: &str, values: &Value) -> Vec<Value> {
    array(values).iter().map(|name| absolute(owner, name)).collect()
}

fn native_names(inventory: &Inventory<'_>, values: &Value) -> Vec<Value> {
    array(values).iter().map(|index| inventory.name(uint(index)).clone()).collect()
}

fn match_declaration(inventory: &mut Inventory<'_>, owner: &str, imported: bool,
                     descriptor: &Value, native_tag: &str, record: &Value,
                     bodies: &BTreeMap<(usize, String), &BodyOpening>, used: &mut BTreeSet<(usize, String)>) {
    fields(descriptor, &["name", "kind", "universes", "type", "value_hash", "meta"]);
    assert_eq!(*inventory.name(uint(&record["name"])), absolute(owner, &descriptor["name"]), "CORRESPONDENCE_DECLARATION_NAME");
    let parameters = array(&record["levelParams"]).iter().map(uint).collect::<Vec<_>>();
    assert!(parameters.len() <= 256 && parameters.iter().copied().collect::<BTreeSet<_>>().len() == parameters.len(),
            "CORRESPONDENCE_UNIVERSE_CENSUS");
    for parameter in &parameters { inventory.name(*parameter); }
    assert_eq!(parameters.len(), uint(&descriptor["universes"]), "CORRESPONDENCE_UNIVERSES");
    assert_eq!(inventory.expression(owner, uint(&record["type"]), &parameters, 0), descriptor["type"],
               "CORRESPONDENCE_DECLARATION_TYPE");
    let kind = text(&descriptor["kind"]);
    let meta = &descriptor["meta"];
    let ordinary = ["definition", "opaque", "theorem"].contains(&kind);
    if ordinary {
        match kind {
            "definition" => {
                fields(meta, &["hint", "safety"]);
                assert_eq!(meta["safety"], "safe", "CORRESPONDENCE_SAFETY");
                assert_eq!(record["hints"], meta["hint"], "CORRESPONDENCE_HINT");
            },
            "opaque" => { fields(meta, &["safety"]); assert_eq!(meta["safety"], "safe", "CORRESPONDENCE_SAFETY"); },
            "theorem" => { fields(meta, &[]); assert!(descriptor["value_hash"].is_null(), "CORRESPONDENCE_THEOREM_COMMITMENT"); },
            _ => unreachable!(),
        }
        if imported && kind == "theorem" {
            assert_eq!(native_tag, "moduleImportTheorem", "CORRESPONDENCE_IMPORTED_THEOREM_KIND");
            fields(record, &["name", "levelParams", "type"]);
            return;
        }
        if native_tag == "moduleImportDef" || native_tag == "moduleImportOpaque" {
            assert!(imported, "CORRESPONDENCE_NEW_VALUE_ABSENT");
            assert_eq!(native_tag, if kind == "definition" { "moduleImportDef" } else { "moduleImportOpaque" },
                       "CORRESPONDENCE_MISSING_KIND");
            fields(record, if kind == "definition" { &["name", "levelParams", "type", "bodyHash", "hints"] }
                           else { &["name", "levelParams", "type", "bodyHash"] });
            let bytes = array(&record["bodyHash"]);
            assert_eq!(bytes.len(), 32, "CORRESPONDENCE_BODY_DIGEST");
            let actual = bytes.iter().map(|byte| { let n = uint(byte); assert!(n <= 255, "CORRESPONDENCE_BODY_DIGEST"); format!("{n:02x}") }).collect::<String>();
            assert_eq!(actual, text(&descriptor["value_hash"]), "CORRESPONDENCE_BODY_COMMITMENT");
            return;
        }
        assert_eq!(native_tag, match kind { "definition" => "def", "opaque" => "opaque", _ => "thm" }, "CORRESPONDENCE_VALUE_KIND");
        fields(record, match kind {
            "definition" => &["name", "levelParams", "type", "value", "all", "hints", "safety"],
            "opaque" => &["name", "levelParams", "type", "value", "all", "isUnsafe"],
            _ => &["name", "levelParams", "type", "value", "all"],
        });
        assert_eq!(record["all"], json!([record["name"]]), "CORRESPONDENCE_ORDINARY_ALL");
        if kind == "definition" { assert_eq!(record["safety"], "safe", "CORRESPONDENCE_SAFETY"); }
        if kind == "opaque" { assert_eq!(record["isUnsafe"], false, "CORRESPONDENCE_SAFETY"); }
        if kind == "theorem" {
            // Proof is deliberately absent from ModuleSpecID; still expand its
            // syntax under the same immutable reference interpretation. The
            // actual mathematical checker must check the entire new proof.
            inventory.validate_expression(owner, uint(&record["value"]), &parameters, 0);
        } else {
            body_match(inventory, owner, &record["value"], &parameters, &descriptor["value_hash"], bodies, used);
        }
        return;
    }
    assert!(descriptor["value_hash"].is_null(), "CORRESPONDENCE_GROUP_VALUE_HASH");
    assert_eq!(native_tag, kind, "CORRESPONDENCE_GROUP_KIND");
    assert_eq!(record["isUnsafe"], false, "CORRESPONDENCE_SAFETY");
    match kind {
        "inductive" => {
            fields(meta, &["all", "constructors", "num_params", "num_indices", "num_nested", "is_recursive", "is_reflexive"]);
            fields(record, &["name", "levelParams", "type", "all", "ctors", "numParams", "numIndices", "numNested", "isRec", "isReflexive", "isUnsafe"]);
            assert_eq!(native_names(inventory, &record["all"]), mapped_names(owner, &meta["all"]), "CORRESPONDENCE_MUTUAL_NAMES");
            assert_eq!(native_names(inventory, &record["ctors"]), mapped_names(owner, &meta["constructors"]), "CORRESPONDENCE_CONSTRUCTOR_NAMES");
            for (native, canonical) in [("numParams", "num_params"), ("numIndices", "num_indices"), ("numNested", "num_nested"), ("isRec", "is_recursive"), ("isReflexive", "is_reflexive")] {
                assert_eq!(record[native], meta[canonical], "CORRESPONDENCE_INDUCTIVE_METADATA");
            }
        },
        "constructor" => {
            fields(meta, &["inductive", "constructor_index", "num_params", "num_fields"]);
            fields(record, &["name", "levelParams", "type", "induct", "cidx", "numParams", "numFields", "isUnsafe"]);
            assert_eq!(*inventory.name(uint(&record["induct"])), absolute(owner, &meta["inductive"]), "CORRESPONDENCE_CONSTRUCTOR_OWNER");
            for (native, canonical) in [("cidx", "constructor_index"), ("numParams", "num_params"), ("numFields", "num_fields")] {
                assert_eq!(record[native], meta[canonical], "CORRESPONDENCE_CONSTRUCTOR_METADATA");
            }
        },
        "recursor" => {
            fields(meta, &["all", "num_params", "num_indices", "num_motives", "num_minors", "is_k", "rules"]);
            fields(record, &["name", "levelParams", "type", "all", "numParams", "numIndices", "numMotives", "numMinors", "k", "rules", "isUnsafe"]);
            assert_eq!(native_names(inventory, &record["all"]), mapped_names(owner, &meta["all"]), "CORRESPONDENCE_RECURSOR_OWNERS");
            for (native, canonical) in [("numParams", "num_params"), ("numIndices", "num_indices"), ("numMotives", "num_motives"), ("numMinors", "num_minors"), ("k", "is_k")] {
                assert_eq!(record[native], meta[canonical], "CORRESPONDENCE_RECURSOR_METADATA");
            }
            let actual = array(&record["rules"]); let expected = array(&meta["rules"]);
            assert_eq!(actual.len(), expected.len(), "CORRESPONDENCE_RULE_CENSUS");
            for (raw, rule) in actual.iter().zip(expected) {
                fields(raw, &["ctor", "nfields", "rhs"]);
                fields(rule, &["constructor", "num_fields", "value_hash"]);
                assert_eq!(*inventory.name(uint(&raw["ctor"])), absolute(owner, &rule["constructor"]), "CORRESPONDENCE_RULE_CONSTRUCTOR");
                assert_eq!(raw["nfields"], rule["num_fields"], "CORRESPONDENCE_RULE_FIELDS");
                body_match(inventory, owner, &raw["rhs"], &parameters, &rule["value_hash"], bodies, used);
            }
        },
        _ => panic!("CORRESPONDENCE_UNSUPPORTED_DECLARATION"),
    }
}

/// Check exact structural correspondence; does NOT authenticate inputs. The
/// caller must bind the exact foundation prefix and every group/body/hash to
/// the adopted relation and genuine certificate premises before admission.
pub fn check_rows_correspondence_conditional(rows: &[Value], foundation_rows: usize,
    bindings: &[GroupBinding], openings: &[BodyOpening]) -> StructuralCorrespondence {
    assert!(bindings.len() <= 4096 && openings.len() <= MAX_DECLARATIONS, "CORRESPONDENCE_INPUT_LIMIT");
    let mut inventory = Inventory::new(rows, foundation_rows);
    assert_eq!(inventory.groups.len(), bindings.len(), "CORRESPONDENCE_GROUP_CENSUS");
    let mut bodies = BTreeMap::new();
    for opening in openings {
        digest(&opening.digest);
        assert!(opening.universes <= 256, "CORRESPONDENCE_BODY_UNIVERSES");
        assert!(bodies.insert((opening.universes, opening.digest.clone()), opening).is_none(), "CORRESPONDENCE_DUPLICATE_BODY_OPENING");
    }
    let mut used = BTreeSet::new();
    let mut matched = Vec::new();
    let mut names = inventory.foundation_names.clone();
    for (position, binding) in bindings.iter().enumerate() {
        digest(&binding.owner);
        fields(&binding.descriptor, &["kind", "declarations"]);
        let row = inventory.groups[position];
        let (native_tag, native_value) = row.as_object().unwrap().iter().next().unwrap();
        let expected = array(&binding.descriptor["declarations"]);
        let ordinary = binding.descriptor["kind"] == "ordinary";
        assert!(ordinary || binding.descriptor["kind"] == "inductive", "CORRESPONDENCE_GROUP_KIND");
        assert_eq!(native_tag == "inductive", !ordinary, "CORRESPONDENCE_NATIVE_GROUP_KIND");
        let actual = if ordinary { vec![(native_tag.as_str(), native_value)] } else {
            fields(native_value, &["types", "ctors", "recs"]);
            [("types", "inductive"), ("ctors", "constructor"), ("recs", "recursor")].into_iter()
                .flat_map(|(key, tag)| array(&native_value[key]).iter().map(move |value| (tag, value))).collect::<Vec<_>>()
        };
        assert!(!expected.is_empty() && expected.len() == actual.len(), "CORRESPONDENCE_DECLARATION_CENSUS");
        assert!(actual.len() <= MAX_DECLARATIONS, "CORRESPONDENCE_GROUP_SIZE");
        // Descriptor order need not equal parser's type/constructor/recursor
        // order. Index exact structured names once, not an O(d^2) scan for
        // every descriptor in a potentially large mutual group.
        let mut by_name = BTreeMap::new();
        for (index, (_, value)) in actual.iter().enumerate() {
            let key = serde_json::to_string(inventory.name(uint(&value["name"]))).unwrap();
            assert!(by_name.insert(key, index).is_none(), "CORRESPONDENCE_DUPLICATE_GROUP_NAME");
        }
        let mut local_indices = Vec::new();
        let mut selected = BTreeSet::new();
        for descriptor in expected {
            let absolute_name = absolute(&binding.owner, &descriptor["name"]);
            let key = serde_json::to_string(&absolute_name).unwrap();
            let index = *by_name.get(&key).expect("CORRESPONDENCE_DESCRIPTOR_RECORD_MISSING");
            assert!(selected.insert(index), "CORRESPONDENCE_DUPLICATE_DESCRIPTOR");
            let (tag, record) = actual[index];
            let name_index = u32::try_from(uint(&record["name"])).expect("CORRESPONDENCE_NAME_INDEX");
            assert!(names.insert(name_index), "CORRESPONDENCE_DUPLICATE_NATIVE_DECLARATION");
            assert!(names.len() <= MAX_DECLARATIONS, "CORRESPONDENCE_DECLARATION_LIMIT");
            match_declaration(&mut inventory, &binding.owner, binding.imported, descriptor, tag, record, &bodies, &mut used);
            local_indices.push(name_index);
        }
        matched.push(MatchedGroup { owner: binding.owner.clone(), imported: binding.imported,
                                    export_name_indices: local_indices });
    }
    StructuralCorrespondence { status: "STRUCTURAL_CORRESPONDENCE_ONLY_UNVERIFIED_HASHES_AND_PREMISES",
        groups: matched, foundation_name_indices: inventory.foundation_names.into_iter().collect(),
        body_hash_obligations: used.into_iter().map(|key| (*bodies[&key]).clone()).collect(),
        hash_verification_performed: false, mathematical_admission: false }
}

#[cfg(test)]
#[path = "correspondence_controls.rs"]
mod correspondence_controls;
