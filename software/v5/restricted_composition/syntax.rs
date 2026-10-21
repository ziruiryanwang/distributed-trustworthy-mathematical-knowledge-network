//! Bounded canonical syntax and hash-consed internal terms for RC0.
use dmkn_module_relation::canonical::{array, canonical_size, require, text, uint, unhex, R};
use serde_json::Value;
use std::collections::{BTreeMap, BTreeSet};

pub const MAX_FRAME_BYTES: usize = 256 * 1024;
pub const MAX_JSON_NODES: usize = 32_768;
pub const MAX_JSON_DEPTH: usize = 64;
pub const MAX_EXPR_VISITS: usize = 8_192;
pub const MAX_LEVEL_VISITS: usize = MAX_EXPR_VISITS * 8;
pub const MAX_EXPR_DEPTH: usize = 48;
pub const MAX_OPEN_BINDERS: usize = 64;
pub const MAX_ADDRESSES: usize = 64;
pub const MAX_UNIVERSES: usize = 8;
pub const MAX_WORK: usize = 200_000;
pub const MAX_ARENA_NODES: usize = 32_768;

/// Derived counters only: callers cannot use a census as mathematical authority.
#[derive(Clone, Debug, Default, PartialEq, Eq)]
pub struct SourceCensus {
    pub expr_visits: usize,
    pub level_visits: usize,
    pub address_count: usize,
    pub inference_work: usize,
}

pub(crate) fn increment(value: &mut usize, count: usize, limit: usize, why: &str) -> R<()> {
    *value = value.checked_add(count).ok_or("RC counter overflow")?;
    require(*value <= limit, why)
}

/// Rechecked for Value callers as well as the bounded bytes entry point.
pub(crate) fn frame_bounds(value: &Value) -> R<()> {
    fn visit(value: &Value, depth: usize, count: &mut usize) -> R<()> {
        require(depth <= MAX_JSON_DEPTH, "RC JSON depth")?;
        increment(count, 1, MAX_JSON_NODES, "RC JSON nodes")?;
        match value {
            Value::Array(values) => {
                require(values.len() <= MAX_JSON_NODES, "RC JSON array length")?;
                for child in values { visit(child, depth + 1, count)?; }
            },
            Value::Object(values) => {
                require(values.len() <= MAX_JSON_NODES, "RC JSON object length")?;
                for (key, child) in values {
                    require(key.len() <= MAX_FRAME_BYTES, "RC JSON key bytes")?;
                    visit(child, depth + 1, count)?;
                }
            },
            Value::String(s) => require(s.len() <= MAX_FRAME_BYTES, "RC JSON string bytes")?,
            Value::Number(n) => require(n.as_u64().is_some(), "RC unsigned integers only")?,
            _ => {},
        }
        Ok(())
    }
    visit(value, 0, &mut 0)?;
    require(canonical_size(value)? <= MAX_FRAME_BYTES, "RC canonical frame bytes")
}

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord)]
pub(crate) enum NamePart { Str(String), Num(u32) }
pub(crate) type Name = Vec<NamePart>;
#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord)]
pub(crate) enum Address { Foundation(Name), Owned([u8; 32], Name) }
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
pub(crate) enum Style { Default, Implicit, StrictImplicit, InstImplicit }
impl Style {
    pub(crate) fn parse(value: &Value) -> R<Self> {
        match text(value)? {
            "default" => Ok(Self::Default), "implicit" => Ok(Self::Implicit),
            "strictImplicit" => Ok(Self::StrictImplicit), "instImplicit" => Ok(Self::InstImplicit),
            _ => Err("RC binder style".into()),
        }
    }
}
pub(crate) type Id = usize;
pub(crate) type LevelId = usize;
#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord)]
pub(crate) enum Level { Zero, Param(u8), Succ(LevelId), IMax(LevelId, LevelId) }
#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord)]
pub(crate) enum Node {
    Bvar(u16), Sort(LevelId), Const(Address, Vec<LevelId>), App(Id, Id),
    Lam { origin: u32, style: Style, domain: Id, body: Id },
    Pi { origin: u32, style: Style, domain: Id, body: Id },
    // Fresh IDs are immutable and never reused; their types are closed w.r.t.
    // loose bvars (outer fresh locals may occur). Locals never occur on the wire.
    Local(u64, Id),
}

pub(crate) struct Arena {
    pub(crate) nodes: Vec<Node>,
    pub(crate) levels: Vec<Level>,
    node_map: BTreeMap<Node, Id>,
    level_map: BTreeMap<Level, LevelId>,
    addresses: BTreeSet<Address>,
    pub(crate) census: SourceCensus,
}
impl Arena {
    pub(crate) fn new() -> Self {
        Self { nodes: Vec::new(), levels: Vec::new(), node_map: BTreeMap::new(),
            level_map: BTreeMap::new(), addresses: BTreeSet::new(), census: SourceCensus::default() }
    }
    pub(crate) fn charge(&mut self) -> R<()> {
        increment(&mut self.census.inference_work, 1, MAX_WORK, "RC inference work")
    }
    pub(crate) fn node(&mut self, node: Node) -> R<Id> {
        self.charge()?;
        if let Some(id) = self.node_map.get(&node) { return Ok(*id); }
        require(self.nodes.len() < MAX_ARENA_NODES, "RC expression arena nodes")?;
        let id = self.nodes.len(); self.nodes.push(node.clone()); self.node_map.insert(node, id); Ok(id)
    }
    pub(crate) fn level(&mut self, level: Level) -> R<LevelId> {
        self.charge()?;
        if let Some(id) = self.level_map.get(&level) { return Ok(*id); }
        require(self.levels.len() < MAX_ARENA_NODES, "RC level arena nodes")?;
        let id = self.levels.len(); self.levels.push(level.clone()); self.level_map.insert(level, id); Ok(id)
    }
    pub(crate) fn address(&mut self, address: Address) -> R<Address> {
        self.addresses.insert(address.clone());
        require(self.addresses.len() <= MAX_ADDRESSES, "RC qualified addresses")?;
        self.census.address_count = self.addresses.len(); Ok(address)
    }
    pub(crate) fn name(value: &Value) -> R<Name> {
        let parts = array(value)?;
        require(!parts.is_empty() && parts.len() <= 8, "RC name components")?;
        parts.iter().map(|part| {
            let p = array(part)?; require(p.len() == 2, "RC name component shape")?;
            match text(&p[0])? {
                "s" => { let s = text(&p[1])?;
                    require(!s.is_empty() && s.len() <= 64 && !s.contains('\0'), "RC name string bytes")?;
                    Ok(NamePart::Str(s.into())) },
                "n" => Ok(NamePart::Num(uint(&p[1], u32::MAX as u64)? as u32)),
                _ => Err("RC name component tag".into()),
            }
        }).collect()
    }
    pub(crate) fn owned(&mut self, owner: [u8; 32], value: &Value) -> R<Address> {
        self.address(Address::Owned(owner, Self::name(value)?))
    }
    fn reference(&mut self, value: &Value, owner: [u8; 32]) -> R<Address> {
        let r = array(value)?;
        require(!r.is_empty(), "RC reference shape")?;
        let address = match text(&r[0])? {
            "foundation" if r.len() == 2 => Address::Foundation(Self::name(&r[1])?),
            "local" if r.len() == 2 => Address::Owned(owner, Self::name(&r[1])?),
            "external" if r.len() == 3 => {
                let other = unhex(text(&r[1])?)?;
                require(other != owner, "RC same-owner reference must be local")?;
                Address::Owned(other, Self::name(&r[2])?)
            },
            _ => return Err("RC reference tag/arity".into()),
        };
        self.address(address)
    }
    fn parse_level(&mut self, value: &Value, universes: usize, counted: bool) -> R<LevelId> {
        if counted { increment(&mut self.census.level_visits, 1, MAX_LEVEL_VISITS, "RC source level visits")?; }
        let l = array(value)?; require(!l.is_empty(), "RC level shape")?;
        match text(&l[0])? {
            "zero" if l.len() == 1 => self.level(Level::Zero),
            "param" if l.len() == 2 => {
                let p = uint(&l[1], 7)? as usize;
                require(p < universes, "RC universe parameter scope")?;
                self.level(Level::Param(p as u8))
            },
            _ => Err("RC unsupported public universe".into()),
        }
    }
    pub(crate) fn parse_expr(&mut self, value: &Value, owner: [u8; 32], universes: usize) -> R<Id> {
        require(universes <= MAX_UNIVERSES, "RC universe arity")?;
        self.parse(value, owner, universes, 0, 0, false)
    }
    /// Only the compiled foundation table calls this in production. It retains
    /// native binder-name indices; the public Expr grammar has no such field.
    pub(crate) fn parse_projection(&mut self, value: &Value, universes: usize) -> R<Id> {
        self.parse(value, [0; 32], universes, 0, 0, true)
    }
    fn parse(&mut self, value: &Value, owner: [u8; 32], universes: usize,
             depth: usize, binders: usize, projection: bool) -> R<Id> {
        require(depth <= MAX_EXPR_DEPTH && binders <= MAX_OPEN_BINDERS, "RC expression depth")?;
        if !projection { increment(&mut self.census.expr_visits, 1, MAX_EXPR_VISITS, "RC source expression visits")?; }
        let e = array(value)?; require(!e.is_empty(), "RC expression shape")?;
        let node = match text(&e[0])? {
            "bvar" if e.len() == 2 => {
                let b = uint(&e[1], MAX_OPEN_BINDERS as u64)? as usize;
                require(b < binders, "RC bound variable scope")?; Node::Bvar(b as u16)
            },
            "sort" if e.len() == 2 => Node::Sort(self.parse_level(&e[1], universes, !projection)?),
            "const" if e.len() == 3 => {
                let address = self.reference(&e[1], owner)?;
                let values = array(&e[2])?; require(values.len() <= MAX_UNIVERSES, "RC constant universe count")?;
                let levels = values.iter().map(|v| self.parse_level(v, universes, !projection)).collect::<R<_>>()?;
                Node::Const(address, levels)
            },
            "app" if e.len() == 3 => {
                let f = self.parse(&e[1], owner, universes, depth + 1, binders, projection)?;
                require(!matches!(self.nodes[f], Node::Lam { .. }), "RC syntactic beta redex unsupported")?;
                let a = self.parse(&e[2], owner, universes, depth + 1, binders, projection)?; Node::App(f, a)
            },
            tag @ ("lam" | "forall") if e.len() == if projection { 5 } else { 4 } => {
                let style = Style::parse(&e[1])?;
                let (origin, offset) = if projection { (uint(&e[2], u32::MAX as u64)? as u32, 3) } else { (0, 2) };
                let domain = self.parse(&e[offset], owner, universes, depth + 1, binders, projection)?;
                let body = self.parse(&e[offset + 1], owner, universes, depth + 1, binders + 1, projection)?;
                if tag == "lam" { Node::Lam { origin, style, domain, body } }
                else { Node::Pi { origin, style, domain, body } }
            },
            _ => return Err("RC unsupported expression or arity".into()),
        };
        self.node(node)
    }

    /// Conservative existence bounds for the original full witness. This does
    /// not emit native rows or traverse the adopted foundation per delta.
    pub(crate) fn virtual_witness_bounds(&self) -> R<()> {
        let checked_sum = |values: &[usize]| -> R<usize> {
            values.iter().try_fold(0usize, |a, b| a.checked_add(*b).ok_or("RC virtual bound overflow".into()))
        };
        let rows = checked_sum(&[crate::foundation::PREFIX_ROWS, 768, 8, MAX_EXPR_VISITS, 24])?;
        require(rows <= 250_000 && 22 + 24 <= 16_384, "RC virtual row/declaration bound")?;
        let bytes = checked_sum(&[crate::foundation::PREFIX_BYTES, 768 * 512,
            MAX_EXPR_VISITS * 256, 8 * 128, 24 * 256, MAX_FRAME_BYTES, 4096])?;
        require(bytes < 3 * 1024 * 1024, "RC virtual witness bytes")?;
        let nodes = checked_sum(&[crate::foundation::PREFIX_BYTES,
            32 * (MAX_EXPR_VISITS + 24), 8 * (768 + 8), MAX_JSON_NODES, 1024])?;
        require(nodes < 350_000, "RC virtual witness JSON nodes")?;
        let visits = self.census.expr_visits.checked_add(self.census.level_visits).ok_or("RC correspondence bound overflow")?;
        require(visits <= 250_000 && MAX_EXPR_DEPTH + 1 <= 192, "RC virtual correspondence visits/depth")
    }
}
