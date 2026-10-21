//! Deliberately incomplete syntax-directed checking. Unsupported conversion
//! refuses; it never falls through to delta reduction or another checker.
use crate::{foundation, syntax::{Address, Arena, Id, Level, LevelId, Node, MAX_OPEN_BINDERS}};
use dmkn_module_relation::canonical::{require, R};
use std::collections::{BTreeMap, BTreeSet};

const MAX_INTERNAL_DEPTH: usize = 128;

#[derive(Clone)]
pub(crate) struct Signature { pub(crate) universes: usize, pub(crate) ty: Id }

pub(crate) struct Typing {
    pub(crate) arena: Arena,
    pub(crate) environment: BTreeMap<Address, Signature>,
    inferred: BTreeMap<Id, Id>,
    next_local: u64,
    open_binders: usize,
}
impl Typing {
    pub(crate) fn new() -> R<Self> {
        let mut arena = Arena::new(); let mut environment = BTreeMap::new();
        for (address, universes, ty) in foundation::install(&mut arena)? {
            require(environment.insert(address, Signature { universes, ty }).is_none(), "RC duplicate foundation signature")?;
        }
        Ok(Self { arena, environment, inferred: BTreeMap::new(), next_local: 0, open_binders: 0 })
    }
    fn depth(&mut self, depth: usize) -> R<()> {
        self.arena.charge()?; require(depth <= MAX_INTERNAL_DEPTH, "RC internal traversal depth")
    }
    fn fresh(&mut self, ty: Id) -> R<Id> {
        require(self.open_binders < MAX_OPEN_BINDERS, "RC simultaneously opened binders")?;
        self.open_binders += 1;
        let id = self.next_local;
        self.next_local = id.checked_add(1).ok_or("RC fresh local overflow")?;
        self.arena.node(Node::Local(id, ty))
    }
    pub(crate) fn add(&mut self, address: Address, signature: Signature) -> R<()> {
        require(!self.environment.contains_key(&address), "RC duplicate qualified declaration")?;
        self.environment.insert(address, signature); Ok(())
    }

    /// Constant closure/arity validation includes unused branches of a selected
    /// type; checking a proof alone cannot hide an unavailable dependency.
    pub(crate) fn references(&mut self, expression: Id) -> R<()> {
        fn visit(tc: &mut Typing, e: Id, seen: &mut BTreeSet<Id>, depth: usize) -> R<()> {
            tc.depth(depth)?;
            if !seen.insert(e) { return Ok(()); }
            match tc.arena.nodes[e].clone() {
                Node::Const(address, levels) => {
                    let signature = tc.environment.get(&address).ok_or("RC missing authenticated type dependency")?;
                    require(levels.len() == signature.universes, "RC constant exact universe arity")?;
                },
                Node::App(f, a) => { visit(tc, f, seen, depth + 1)?; visit(tc, a, seen, depth + 1)?; },
                Node::Pi { domain, body, .. } | Node::Lam { domain, body, .. } => {
                    visit(tc, domain, seen, depth + 1)?; visit(tc, body, seen, depth + 1)?;
                },
                Node::Local(..) => return Err("RC source expression contains internal local".into()),
                _ => {},
            }
            Ok(())
        }
        visit(self, expression, &mut BTreeSet::new(), 0)
    }

    /// Replace the one outer binder after all its outer scopes have already
    /// been opened. No replacement lifting is needed: it has no loose bvars.
    /// This is native inst's reversed singleton vector, not arbitrary beta.
    pub(crate) fn open(&mut self, expression: Id, replacement: Id) -> R<Id> {
        fn visit(tc: &mut Typing, e: Id, r: Id, offset: u16, depth: usize,
                 cache: &mut BTreeMap<(Id, u16), Id>) -> R<Id> {
            tc.depth(depth)?;
            if let Some(out) = cache.get(&(e, offset)) { return Ok(*out); }
            let n = match tc.arena.nodes[e].clone() {
                Node::Bvar(i) if i == offset => { cache.insert((e, offset), r); return Ok(r); },
                Node::Bvar(i) => { require(i < offset, "RC unopened outer variable")?; Node::Bvar(i) },
                Node::App(f, a) => Node::App(visit(tc, f, r, offset, depth + 1, cache)?, visit(tc, a, r, offset, depth + 1, cache)?),
                Node::Pi { origin, style, domain, body } => Node::Pi { origin, style,
                    domain: visit(tc, domain, r, offset, depth + 1, cache)?,
                    body: visit(tc, body, r, offset.checked_add(1).ok_or("RC binder offset overflow")?, depth + 1, cache)? },
                Node::Lam { origin, style, domain, body } => Node::Lam { origin, style,
                    domain: visit(tc, domain, r, offset, depth + 1, cache)?,
                    body: visit(tc, body, r, offset.checked_add(1).ok_or("RC binder offset overflow")?, depth + 1, cache)? },
                other => other,
            };
            let out = tc.arena.node(n)?; cache.insert((e, offset), out); Ok(out)
        }
        visit(self, expression, replacement, 0, 0, &mut BTreeMap::new())
    }
    fn close(&mut self, expression: Id, local: Id) -> R<Id> {
        fn visit(tc: &mut Typing, e: Id, local: Id, offset: u16, depth: usize,
                 cache: &mut BTreeMap<(Id, u16), Id>) -> R<Id> {
            tc.depth(depth)?;
            if let Some(out) = cache.get(&(e, offset)) { return Ok(*out); }
            let n = if e == local { Node::Bvar(offset) } else { match tc.arena.nodes[e].clone() {
                Node::App(f, a) => Node::App(visit(tc, f, local, offset, depth + 1, cache)?, visit(tc, a, local, offset, depth + 1, cache)?),
                Node::Pi { origin, style, domain, body } => Node::Pi { origin, style,
                    domain: visit(tc, domain, local, offset, depth + 1, cache)?,
                    body: visit(tc, body, local, offset.checked_add(1).ok_or("RC close offset overflow")?, depth + 1, cache)? },
                Node::Lam { origin, style, domain, body } => Node::Lam { origin, style,
                    domain: visit(tc, domain, local, offset, depth + 1, cache)?,
                    body: visit(tc, body, local, offset.checked_add(1).ok_or("RC close offset overflow")?, depth + 1, cache)? },
                other => other,
            }};
            let out = tc.arena.node(n)?; cache.insert((e, offset), out); Ok(out)
        }
        visit(self, expression, local, 0, 0, &mut BTreeMap::new())
    }

    pub(crate) fn subst_levels(&mut self, expression: Id, values: &[LevelId]) -> R<Id> {
        fn level(tc: &mut Typing, l: LevelId, values: &[LevelId], depth: usize,
                 cache: &mut BTreeMap<LevelId, LevelId>) -> R<LevelId> {
            tc.depth(depth)?;
            if let Some(out) = cache.get(&l) { return Ok(*out); }
            let out = match tc.arena.levels[l].clone() {
                // Simultaneous: a replacement is returned unchanged, not visited.
                Level::Param(i) => *values.get(i as usize).ok_or("RC universe substitution arity")?,
                Level::Zero => l,
                Level::Succ(a) => { let a = level(tc, a, values, depth + 1, cache)?; tc.arena.level(Level::Succ(a))? },
                Level::IMax(a, b) => {
                    let a = level(tc, a, values, depth + 1, cache)?;
                    let b = level(tc, b, values, depth + 1, cache)?; tc.imax(a, b)?
                },
            };
            cache.insert(l, out); Ok(out)
        }
        fn visit(tc: &mut Typing, e: Id, values: &[LevelId], depth: usize,
                 cache: &mut BTreeMap<Id, Id>, levels: &mut BTreeMap<LevelId, LevelId>) -> R<Id> {
            tc.depth(depth)?;
            if let Some(out) = cache.get(&e) { return Ok(*out); }
            let n = match tc.arena.nodes[e].clone() {
                Node::Sort(l) => Node::Sort(level(tc, l, values, depth + 1, levels)?),
                Node::Const(a, ls) => Node::Const(a, ls.into_iter().map(|l| level(tc, l, values, depth + 1, levels)).collect::<R<_>>()?),
                Node::App(f, a) => Node::App(visit(tc, f, values, depth + 1, cache, levels)?, visit(tc, a, values, depth + 1, cache, levels)?),
                Node::Pi { origin, style, domain, body } => Node::Pi { origin, style,
                    domain: visit(tc, domain, values, depth + 1, cache, levels)?, body: visit(tc, body, values, depth + 1, cache, levels)? },
                Node::Lam { origin, style, domain, body } => Node::Lam { origin, style,
                    domain: visit(tc, domain, values, depth + 1, cache, levels)?, body: visit(tc, body, values, depth + 1, cache, levels)? },
                Node::Local(..) => return Err("RC declaration universe substitution found local".into()),
                other => other,
            };
            let out = tc.arena.node(n)?; cache.insert(e, out); Ok(out)
        }
        visit(self, expression, values, 0, &mut BTreeMap::new(), &mut BTreeMap::new())
    }
    fn imax(&mut self, a: LevelId, b: LevelId) -> R<LevelId> {
        // Native util::imax only interns: retaining raw structure is necessary
        // for exact native-pointer correspondence underneath arbitrary nodes.
        self.arena.level(Level::IMax(a, b))
    }
    fn zero(&mut self, level: LevelId, depth: usize) -> R<bool> {
        self.depth(depth)?;
        match self.arena.levels[level] {
            Level::Zero => Ok(true),
            // A sound subset of native level::is_zero, not a general solver.
            // No allocation/rewrite leaks this equivalence into nested nodes.
            Level::IMax(_, right) => self.zero(right, depth + 1),
            _ => Ok(false),
        }
    }
    pub(crate) fn compare(&mut self, left: Id, right: Id) -> R<bool> { self.compare_at(left, right, 0) }
    fn compare_at(&mut self, left: Id, right: Id, depth: usize) -> R<bool> {
        self.depth(depth)?;
        if left == right { return Ok(true); }
        if let (Node::Sort(a), Node::Sort(b)) = (&self.arena.nodes[left], &self.arena.nodes[right]) {
            let (a, b) = (*a, *b);
            // The original def_eq_quick_check explicitly calls def_eq_sort
            // here. Both recognized-zero levels pass its eq_antisymm branch.
            return Ok(self.zero(a, depth + 1)? && self.zero(b, depth + 1)?);
        }
        // Exact interning includes every nested origin/style. Alpha comparison
        // is permitted ONLY at an actual root-binder quick-check branch.
        let pair = match (self.arena.nodes[left].clone(), self.arena.nodes[right].clone()) {
            (Node::Pi { domain: a, body: x, .. }, Node::Pi { domain: b, body: y, .. }) |
            (Node::Lam { domain: a, body: x, .. }, Node::Lam { domain: b, body: y, .. }) => Some((a, b, x, y)),
            _ => None,
        };
        let Some((a, b, x, y)) = pair else { return Ok(false); };
        if !self.compare_at(a, b, depth + 1)? { return Ok(false); }
        let local = self.fresh(a)?;
        let result = (|| {
            let x = self.open(x, local)?; let y = self.open(y, local)?;
            self.compare_at(x, y, depth + 1)
        })();
        self.open_binders -= 1; result
    }
    fn sort_of(&mut self, expression: Id, depth: usize) -> R<LevelId> {
        let ty = self.infer_at(expression, depth + 1)?;
        match self.arena.nodes[ty] { Node::Sort(level) => Ok(level), _ => Err("RC type requires unsupported sort reduction".into()) }
    }
    pub(crate) fn infer(&mut self, expression: Id) -> R<Id> { self.infer_at(expression, 0) }
    fn infer_at(&mut self, expression: Id, depth: usize) -> R<Id> {
        self.depth(depth)?;
        // Terms are fully opened and fresh local IDs never repeat. Therefore
        // this cache key includes its context; the environment is append-only.
        if let Some(ty) = self.inferred.get(&expression) { return Ok(*ty); }
        let ty = match self.arena.nodes[expression].clone() {
            Node::Bvar(_) => return Err("RC loose variable in inference".into()),
            Node::Local(_, ty) => ty,
            Node::Sort(l) => { let successor = self.arena.level(Level::Succ(l))?; self.arena.node(Node::Sort(successor))? },
            Node::Const(address, levels) => {
                let signature = self.environment.get(&address).ok_or("RC unknown or forward constant")?.clone();
                require(levels.len() == signature.universes, "RC inference universe arity")?;
                self.subst_levels(signature.ty, &levels)?
            },
            Node::App(f, a) => {
                let f_ty = self.infer_at(f, depth + 1)?;
                let Node::Pi { domain, body, .. } = self.arena.nodes[f_ty].clone()
                    else { return Err("RC application requires unsupported Pi reduction".into()); };
                let a_ty = self.infer_at(a, depth + 1)?;
                require(self.compare(domain, a_ty)?, "RC application domain mismatch or unsupported conversion")?;
                self.open(body, a)?
            },
            Node::Pi { domain, body, .. } => {
                let domain_sort = self.sort_of(domain, depth + 1)?;
                let local = self.fresh(domain)?;
                let result = (|| {
                    let opened = self.open(body, local)?;
                    let body_sort = self.sort_of(opened, depth + 1)?;
                    let level = self.imax(domain_sort, body_sort)?;
                    self.arena.node(Node::Sort(level))
                })();
                self.open_binders -= 1; result?
            },
            Node::Lam { origin, style, domain, body } => {
                self.sort_of(domain, depth + 1)?;
                let local = self.fresh(domain)?;
                let result = (|| {
                    let opened = self.open(body, local)?;
                    let body_type = self.infer_at(opened, depth + 1)?;
                    let closed = self.close(body_type, local)?;
                    self.arena.node(Node::Pi { origin, style, domain, body: closed })
                })();
                self.open_binders -= 1; result?
            },
        };
        self.inferred.insert(expression, ty); Ok(ty)
    }
    pub(crate) fn check_theorem(&mut self, ty: Id, proof: Id) -> R<()> {
        self.references(ty)?; self.references(proof)?;
        let sort = self.infer(ty)?;
        let Node::Sort(level) = self.arena.nodes[sort] else { return Err("RC theorem type is not a type".into()); };
        require(self.zero(level, 0)?, "RC theorem type must be Prop")?;
        let inferred = self.infer(proof)?;
        // Preserve original check_declar's comparison orientation too.
        require(self.compare(inferred, ty)?, "RC theorem proof mismatch or unsupported conversion")
    }
}
