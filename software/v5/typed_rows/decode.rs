//! Direct strict hybrid syntax decoder. No mathematics, receipt authority or
//! sender-selected policy is established here. Every recognizer error selects
//! the caller's unchanged whole-frame legacy path, before any semantic work.
use crate::canonical::{MAX_BYTES, MAX_NODES};
use nanoda_lib::typed_rows::{DagBinderStyle, DagRow, Row};
use serde::{de::{DeserializeSeed, Error, MapAccess, SeqAccess, Visitor}, Deserializer};
use serde_json::{Map, Number, Value};
use std::fmt;

const FOUNDATION_ROWS: usize = crate::policy::FOUNDATION_ROWS;
const MAX_DEPTH: usize = 256;
const FRAME_FIELDS: [&str; 7] = ["schema", "image", "rank", "local_spec", "rows", "parents", "bodies"];

/// Only decode constructs this immutable syntax/count token. Counts describe
/// the old Value interpretation, not the number of allocated Rust records.
#[derive(Debug)]
pub struct HybridFrame {
    fields: Map<String, Value>,
    rows: Vec<Row>,
    nodes: usize,
    maximum_depth: usize,
}

impl HybridFrame {
    pub fn nodes(&self) -> usize { self.nodes }
    pub fn maximum_depth(&self) -> usize { self.maximum_depth }
    pub fn rows_len(&self) -> usize { self.rows.len() }
    pub fn rows(&self) -> &[Row] { &self.rows }
    /// Non-row fields remain unextracted generic Values until the old relation
    /// extraction point. In particular this does not pre-validate parent shapes.
    pub fn field(&self, name: &str) -> Option<&Value> { self.fields.get(name) }
    pub(crate) fn into_parts(self) -> (Map<String, Value>, Vec<Row>) { (self.fields, self.rows) }
}

#[derive(Debug)]
pub enum DecodeOutcome { Typed(HybridFrame), UnsupportedRepresentation }

/// Unsupported includes malformed/ambiguous input: the literal old path owns
/// its final diagnostics and rejection. This never retries a semantic failure.
pub fn decode(bytes: &[u8]) -> DecodeOutcome {
    if bytes.is_empty() || bytes.len() > MAX_BYTES {
        return DecodeOutcome::UnsupportedRepresentation;
    }
    let mut counts = Counts::default();
    let mut deserializer = serde_json::Deserializer::from_slice(bytes);
    let parsed = FrameSeed { counts: &mut counts }.deserialize(&mut deserializer);
    let Ok((fields, rows)) = parsed else { return DecodeOutcome::UnsupportedRepresentation; };
    if deserializer.end().is_err() { return DecodeOutcome::UnsupportedRepresentation; }
    // Do not disable serde_json's default recursion bound. All nested seeds
    // consume this same deserializer, including generic non-row subtrees.
    DecodeOutcome::Typed(HybridFrame {
        fields, rows, nodes: counts.nodes, maximum_depth: counts.maximum_depth,
    })
}

#[derive(Default)]
struct Counts { nodes: usize, maximum_depth: usize }
impl Counts {
    fn enter<E: Error>(&mut self, depth: usize) -> Result<(), E> {
        self.nodes = self.nodes.checked_add(1).ok_or_else(|| E::custom("structure overflow"))?;
        if depth > MAX_DEPTH || self.nodes > MAX_NODES { return Err(E::custom("structure bound")); }
        self.maximum_depth = self.maximum_depth.max(depth);
        Ok(())
    }
}

// Same accepted scalar domain as canonical::Strict: deserialize_any, u64 only
// for numbers, decoded duplicate keys, unchanged string unescaping. Counting
// occurs while consuming every Value node; object keys are not Value nodes.
struct StrictSeed<'a> { counts: &'a mut Counts, depth: usize }
impl<'de> DeserializeSeed<'de> for StrictSeed<'_> {
    type Value = Value;
    fn deserialize<D: Deserializer<'de>>(self, de: D) -> Result<Value, D::Error> {
        self.counts.enter(self.depth)?;
        de.deserialize_any(self)
    }
}
impl<'de> Visitor<'de> for StrictSeed<'_> {
    type Value = Value;
    fn expecting(&self, f: &mut fmt::Formatter) -> fmt::Result { write!(f, "strict unsigned integer-only JSON") }
    fn visit_bool<E: Error>(self, value: bool) -> Result<Value, E> { Ok(Value::Bool(value)) }
    fn visit_unit<E: Error>(self) -> Result<Value, E> { Ok(Value::Null) }
    fn visit_u64<E: Error>(self, value: u64) -> Result<Value, E> { Ok(Value::Number(Number::from(value))) }
    fn visit_i64<E: Error>(self, _: i64) -> Result<Value, E> { Err(E::custom("negative integer forbidden")) }
    fn visit_f64<E: Error>(self, _: f64) -> Result<Value, E> { Err(E::custom("noninteger number forbidden")) }
    fn visit_str<E: Error>(self, value: &str) -> Result<Value, E> { Ok(Value::String(value.to_owned())) }
    fn visit_string<E: Error>(self, value: String) -> Result<Value, E> { Ok(Value::String(value)) }
    fn visit_seq<A: SeqAccess<'de>>(self, mut seq: A) -> Result<Value, A::Error> {
        let mut values = Vec::new();
        while let Some(value) = seq.next_element_seed(StrictSeed { counts: &mut *self.counts, depth: self.depth + 1 })? {
            if values.len() >= MAX_NODES { return Err(A::Error::custom("array bound")); }
            values.push(value);
        }
        Ok(Value::Array(values))
    }
    fn visit_map<A: MapAccess<'de>>(self, mut map: A) -> Result<Value, A::Error> {
        let mut values = Map::new();
        while let Some(key) = map.next_key::<String>()? {
            if values.len() >= MAX_NODES || values.contains_key(&key) {
                return Err(A::Error::custom("duplicate key or object bound"));
            }
            let value = map.next_value_seed(StrictSeed { counts: &mut *self.counts, depth: self.depth + 1 })?;
            values.insert(key, value);
        }
        Ok(Value::Object(values))
    }
}

#[derive(Clone, Copy)]
enum Kind { U32, U16, Usize, Text, Bool, Binder, List, Pair }
enum Field { U32(u32), U16(u16), Usize(usize), Text(String), Bool(bool), Binder(DagBinderStyle), List(Vec<u32>) }

struct FieldSeed<'a> { counts: &'a mut Counts, depth: usize, kind: Kind }
impl<'de> DeserializeSeed<'de> for FieldSeed<'_> {
    type Value = Field;
    fn deserialize<D: Deserializer<'de>>(self, de: D) -> Result<Field, D::Error> {
        self.counts.enter(self.depth)?;
        de.deserialize_any(self)
    }
}
impl<'de> Visitor<'de> for FieldSeed<'_> {
    type Value = Field;
    fn expecting(&self, f: &mut fmt::Formatter) -> fmt::Result { write!(f, "exact typed DAG field") }
    fn visit_u64<E: Error>(self, value: u64) -> Result<Field, E> {
        match self.kind {
            Kind::U32 => u32::try_from(value).map(Field::U32).map_err(|_| E::custom("u32 bound")),
            Kind::U16 => u16::try_from(value).map(Field::U16).map_err(|_| E::custom("u16 bound")),
            Kind::Usize => usize::try_from(value).map(Field::Usize).map_err(|_| E::custom("target usize bound")),
            _ => Err(E::custom("unexpected unsigned field")),
        }
    }
    fn visit_i64<E: Error>(self, _: i64) -> Result<Field, E> { Err(E::custom("negative integer forbidden")) }
    fn visit_f64<E: Error>(self, _: f64) -> Result<Field, E> { Err(E::custom("noninteger number forbidden")) }
    fn visit_bool<E: Error>(self, value: bool) -> Result<Field, E> {
        if matches!(self.kind, Kind::Bool) { Ok(Field::Bool(value)) } else { Err(E::custom("unexpected bool field")) }
    }
    fn visit_str<E: Error>(self, value: &str) -> Result<Field, E> { self.visit_string(value.to_owned()) }
    fn visit_string<E: Error>(self, value: String) -> Result<Field, E> {
        match self.kind {
            Kind::Text => Ok(Field::Text(value)),
            Kind::Binder => Ok(Field::Binder(match value.as_str() {
                "default" => DagBinderStyle::Default, "implicit" => DagBinderStyle::Implicit,
                "strictImplicit" => DagBinderStyle::StrictImplicit, "instImplicit" => DagBinderStyle::InstImplicit,
                _ => return Err(E::custom("binder style")),
            })),
            _ => Err(E::custom("unexpected string field")),
        }
    }
    fn visit_seq<A: SeqAccess<'de>>(self, mut seq: A) -> Result<Field, A::Error> {
        if !matches!(self.kind, Kind::List | Kind::Pair) { return Err(A::Error::custom("unexpected array field")); }
        let mut values = Vec::new();
        while let Some(value) = seq.next_element_seed(FieldSeed { counts: &mut *self.counts, depth: self.depth + 1, kind: Kind::U32 })? {
            if values.len() >= MAX_NODES || (matches!(self.kind, Kind::Pair) && values.len() >= 2) {
                return Err(A::Error::custom("array field bound"));
            }
            let Field::U32(value) = value else { unreachable!("U32 seed result"); };
            values.push(value);
        }
        if matches!(self.kind, Kind::Pair) && values.len() != 2 { return Err(A::Error::custom("exact pair")); }
        Ok(Field::List(values))
    }
}

/// Temporary typed fields, not generic JSON maps or Value payloads. Constant
/// specifications also detect escaped-equivalent duplicates via decoded keys.
struct RecordSeed<'a, 's> { counts: &'a mut Counts, depth: usize, spec: &'s [(&'static str, Kind)] }
impl<'de> DeserializeSeed<'de> for RecordSeed<'_, '_> {
    type Value = Vec<Field>;
    fn deserialize<D: Deserializer<'de>>(self, de: D) -> Result<Vec<Field>, D::Error> {
        self.counts.enter(self.depth)?;
        de.deserialize_any(self)
    }
}
impl<'de> Visitor<'de> for RecordSeed<'_, '_> {
    type Value = Vec<Field>;
    fn expecting(&self, f: &mut fmt::Formatter) -> fmt::Result { write!(f, "exact DAG payload object") }
    fn visit_map<A: MapAccess<'de>>(self, mut map: A) -> Result<Vec<Field>, A::Error> {
        let mut fields: Vec<Option<Field>> = (0..self.spec.len()).map(|_| None).collect();
        while let Some(key) = map.next_key::<String>()? {
            let position = self.spec.iter().position(|(name, _)| *name == key)
                .ok_or_else(|| A::Error::custom("unsupported payload key"))?;
            if fields[position].is_some() { return Err(A::Error::custom("duplicate payload key")); }
            fields[position] = Some(map.next_value_seed(FieldSeed {
                counts: &mut *self.counts, depth: self.depth + 1, kind: self.spec[position].1,
            })?);
        }
        fields.into_iter().map(|field| field.ok_or_else(|| A::Error::custom("missing payload key"))).collect()
    }
}

#[derive(Clone, Copy)]
enum Tag { Str, Num, Succ, Param, Max, IMax, BVar, Sort, Const, App, Lam, Pi, Let, Proj }
impl Tag {
    fn parse(tag: &str) -> Option<Self> {
        Some(match tag {
            "str" => Self::Str, "num" => Self::Num, "succ" => Self::Succ, "param" => Self::Param,
            "max" => Self::Max, "imax" => Self::IMax, "bvar" => Self::BVar, "sort" => Self::Sort,
            "const" => Self::Const, "app" => Self::App, "lam" => Self::Lam, "forallE" => Self::Pi,
            "letE" => Self::Let, "proj" => Self::Proj, _ => return None,
        })
    }
}

struct PayloadSeed<'a> { counts: &'a mut Counts, depth: usize, tag: Tag }
impl<'de> DeserializeSeed<'de> for PayloadSeed<'_> {
    type Value = DagRow;
    fn deserialize<D: Deserializer<'de>>(self, de: D) -> Result<DagRow, D::Error> {
        use Kind::*;
        // Exact specs determine each Field alternative before extraction. The
        // placeholder index is replaced only after the full outer row closes.
        macro_rules! take {
            ($values:ident, $variant:ident) => {
                match $values.next().expect("exact field count") {
                    Field::$variant(value) => value, _ => unreachable!("exact field kind"),
                }
            };
        }
        let scalar = match self.tag {
            Tag::Succ | Tag::Param | Tag::Sort => Some(U32), Tag::BVar => Some(U16),
            Tag::Max | Tag::IMax => Some(Pair), _ => None,
        };
        if let Some(kind) = scalar {
            let field = FieldSeed { counts: self.counts, depth: self.depth, kind }.deserialize(de)?;
            return Ok(match (self.tag, field) {
                (Tag::Succ, Field::U32(child)) => DagRow::LevelSucc { index: 0, child },
                (Tag::Param, Field::U32(name)) => DagRow::LevelParam { index: 0, name },
                (Tag::Sort, Field::U32(level)) => DagRow::ExprSort { index: 0, level },
                (Tag::BVar, Field::U16(value)) => DagRow::ExprBVar { index: 0, value },
                (Tag::Max, Field::List(pair)) => DagRow::LevelMax { index: 0, left: pair[0], right: pair[1] },
                (Tag::IMax, Field::List(pair)) => DagRow::LevelIMax { index: 0, left: pair[0], right: pair[1] },
                _ => unreachable!("exact scalar payload"),
            });
        }
        let spec: &[(&str, Kind)] = match self.tag {
            Tag::Str => &[("pre", U32), ("str", Text)],
            Tag::Num => &[("pre", U32), ("i", U32)],
            Tag::Const => &[("name", U32), ("us", List)],
            Tag::App => &[("fn", U32), ("arg", U32)],
            Tag::Lam | Tag::Pi => &[("name", U32), ("type", U32), ("body", U32), ("binderInfo", Binder)],
            Tag::Let => &[("name", U32), ("type", U32), ("value", U32), ("body", U32), ("nondep", Bool)],
            Tag::Proj => &[("typeName", U32), ("idx", Usize), ("struct", U32)],
            _ => unreachable!("scalar tags returned above"),
        };
        let mut values = RecordSeed { counts: self.counts, depth: self.depth, spec }.deserialize(de)?.into_iter();
        Ok(match self.tag {
            Tag::Str => DagRow::NameStr { index: 0, pre: take!(values, U32), text: take!(values, Text) },
            Tag::Num => DagRow::NameNum { index: 0, pre: take!(values, U32), value: take!(values, U32) },
            Tag::Const => DagRow::ExprConst { index: 0, name: take!(values, U32), levels: take!(values, List) },
            Tag::App => DagRow::ExprApp { index: 0, fun: take!(values, U32), arg: take!(values, U32) },
            Tag::Lam => DagRow::ExprLambda { index: 0, name: take!(values, U32), ty: take!(values, U32), body: take!(values, U32), binder: take!(values, Binder) },
            Tag::Pi => DagRow::ExprPi { index: 0, name: take!(values, U32), ty: take!(values, U32), body: take!(values, U32), binder: take!(values, Binder) },
            Tag::Let => DagRow::ExprLet { index: 0, name: take!(values, U32), ty: take!(values, U32), value: take!(values, U32), body: take!(values, U32), nondep: take!(values, Bool) },
            Tag::Proj => DagRow::ExprProj { index: 0, type_name: take!(values, U32), field: take!(values, Usize), structure: take!(values, U32) },
            _ => unreachable!("scalar tags returned above"),
        })
    }
}

struct RowSeed<'a> { counts: &'a mut Counts, depth: usize, foundation: bool }
impl<'de> DeserializeSeed<'de> for RowSeed<'_> {
    type Value = Row;
    fn deserialize<D: Deserializer<'de>>(self, de: D) -> Result<Row, D::Error> {
        if self.foundation {
            return StrictSeed { counts: self.counts, depth: self.depth }.deserialize(de).map(Row::Legacy);
        }
        self.counts.enter(self.depth)?;
        de.deserialize_any(self)
    }
}
impl<'de> Visitor<'de> for RowSeed<'_> {
    type Value = Row;
    fn expecting(&self, f: &mut fmt::Formatter) -> fmt::Result { write!(f, "canonical DAG or declaration row") }
    fn visit_map<A: MapAccess<'de>>(self, mut map: A) -> Result<Row, A::Error> {
        let mut index: Option<(String, u32)> = None;
        let mut dag = None;
        let mut declaration = None;
        while let Some(key) = map.next_key::<String>()? {
            if ["in", "il", "ie"].contains(&key.as_str()) {
                if index.is_some() || declaration.is_some() { return Err(A::Error::custom("unsupported row index")); }
                let field = map.next_value_seed(FieldSeed { counts: &mut *self.counts, depth: self.depth + 1, kind: Kind::U32 })?;
                let Field::U32(value) = field else { unreachable!("U32 seed result"); };
                index = Some((key, value));
            } else if let Some(tag) = Tag::parse(&key) {
                if dag.is_some() || declaration.is_some() { return Err(A::Error::custom("duplicate row constructor")); }
                dag = Some(map.next_value_seed(PayloadSeed { counts: &mut *self.counts, depth: self.depth + 1, tag })?);
            } else if ["def", "thm", "opaque", "axiom", "quot", "moduleImportDef", "moduleImportOpaque", "moduleImportTheorem", "inductive"].contains(&key.as_str()) {
                if index.is_some() || dag.is_some() || declaration.is_some() { return Err(A::Error::custom("unsupported declaration shape")); }
                let value = map.next_value_seed(StrictSeed { counts: &mut *self.counts, depth: self.depth + 1 })?;
                declaration = Some((key, value));
            } else { return Err(A::Error::custom("unsupported row key")); }
        }
        if let Some((key, value)) = declaration {
            let mut object = Map::new();
            object.insert(key, value);
            return Ok(Row::Legacy(Value::Object(object)));
        }
        let (domain, index) = index.ok_or_else(|| A::Error::custom("missing row index"))?;
        let dag = dag.ok_or_else(|| A::Error::custom("missing row constructor"))?;
        if domain != dag.domain() { return Err(A::Error::custom("unsupported row domain")); }
        Ok(Row::Dag(dag.with_index(index)))
    }
}

struct RowsSeed<'a> { counts: &'a mut Counts, depth: usize }
impl<'de> DeserializeSeed<'de> for RowsSeed<'_> {
    type Value = Vec<Row>;
    fn deserialize<D: Deserializer<'de>>(self, de: D) -> Result<Vec<Row>, D::Error> {
        self.counts.enter(self.depth)?;
        de.deserialize_any(self)
    }
}
impl<'de> Visitor<'de> for RowsSeed<'_> {
    type Value = Vec<Row>;
    fn expecting(&self, f: &mut fmt::Formatter) -> fmt::Result { write!(f, "rows array") }
    fn visit_seq<A: SeqAccess<'de>>(self, mut seq: A) -> Result<Vec<Row>, A::Error> {
        let mut rows = Vec::new();
        while let Some(row) = seq.next_element_seed(RowSeed {
            counts: &mut *self.counts, depth: self.depth + 1, foundation: rows.len() < FOUNDATION_ROWS,
        })? {
            if rows.len() >= MAX_NODES { return Err(A::Error::custom("array bound")); }
            rows.push(row);
        }
        Ok(rows)
    }
}

struct FrameSeed<'a> { counts: &'a mut Counts }
impl<'de> DeserializeSeed<'de> for FrameSeed<'_> {
    type Value = (Map<String, Value>, Vec<Row>);
    fn deserialize<D: Deserializer<'de>>(self, de: D) -> Result<Self::Value, D::Error> {
        self.counts.enter(0)?;
        de.deserialize_any(self)
    }
}
impl<'de> Visitor<'de> for FrameSeed<'_> {
    type Value = (Map<String, Value>, Vec<Row>);
    fn expecting(&self, f: &mut fmt::Formatter) -> fmt::Result { write!(f, "exact object-form module witness") }
    fn visit_map<A: MapAccess<'de>>(self, mut map: A) -> Result<Self::Value, A::Error> {
        let mut fields = Map::new();
        let mut rows = None;
        while let Some(key) = map.next_key::<String>()? {
            if !FRAME_FIELDS.contains(&key.as_str()) || fields.contains_key(&key) || (key == "rows" && rows.is_some()) {
                return Err(A::Error::custom("unsupported or duplicate module field"));
            }
            if key == "rows" {
                rows = Some(map.next_value_seed(RowsSeed { counts: &mut *self.counts, depth: 1 })?);
            } else {
                let value = map.next_value_seed(StrictSeed { counts: &mut *self.counts, depth: 1 })?;
                fields.insert(key, value);
            }
        }
        if fields.len() != 6 { return Err(A::Error::custom("missing module field")); }
        let rows = rows.ok_or_else(|| A::Error::custom("missing rows field"))?;
        Ok((fields, rows))
    }
}
