//! Changed-boundary controls only. No guest, aggregate, proof or receipt authority.
use crate::syntax::{Address, Arena, Id, Level, NamePart, Node, Style, MAX_WORK};
use crate::typing::Typing;
use dmkn_module_relation::canonical::{hex, require, sha, R};
use serde_json::{json, Value};
use std::panic::{catch_unwind, AssertUnwindSafe};

#[derive(Default)]
struct Suite { executed: Vec<Value>, refusals: Vec<String>, errors: Vec<Value> }
impl Suite {
    fn check(&mut self, name: &str, f: impl FnOnce() -> R<Value>) {
        match catch_unwind(AssertUnwindSafe(f)) {
            Ok(Ok(detail)) => self.executed.push(json!({"name":name,"status":"PASS","detail":detail})),
            other => {
                let error = match other { Ok(Err(e)) => e, _ => "unexpected panic, not refusal".into() };
                self.executed.push(json!({"name":name,"status":"FAIL"}));
                self.errors.push(json!({"control":name,"error":error}));
            },
        }
    }
    fn negative(&mut self, name: &str, f: impl FnOnce() -> R<Value>) {
        self.refusals.push(name.into()); self.check(name, f);
    }
}
fn refusal<T>(result: R<T>, diagnostic: &str) -> R<Value> {
    match result {
        Err(error) => { require(error.contains(diagnostic), "wrong refusal diagnostic")?;
            Ok(json!({"refusal":error})) },
        Ok(_) => Err("unexpected acceptance".into()),
    }
}
fn sort(arena: &mut Arena) -> R<Id> {
    let zero = arena.level(Level::Zero)?; arena.node(Node::Sort(zero))
}
fn local(tc: &mut Typing, serial: u64, ty: Id) -> R<Id> { tc.arena.node(Node::Local(serial, ty)) }
fn closed_tree(tc: &mut Typing, depth: usize) -> R<(Id, Id)> {
    let leaf = sort(&mut tc.arena)?; let mut tree = leaf;
    for _ in 0..depth { tree = tc.arena.node(Node::App(tree, tree))?; }
    Ok((tree, leaf))
}
fn differential(frame: &Value, expected_journal_sha: &str) -> R<Value> {
    let (old, baseline) = dmkn_rc_baseline::relation::check_with_census(frame.clone())?;
    let (new, support) = dmkn_rc_relation::relation::check_with_census(frame.clone())?;
    let journal = new.journal.encode()?;
    require(journal == old.journal.encode()? && new.parent_journals == old.parent_journals,
        "exact baseline J and ordered pending parent journals")?;
    require(hex(&sha(&journal)) == expected_journal_sha, "adopted actual fixture journal")?;
    require(support.expr_visits == baseline.expr_visits
        && support.level_visits == baseline.level_visits
        && support.address_count == baseline.address_count, "unchanged source census")?;
    Ok(json!({"journal_sha256":expected_journal_sha,"module":hex(&new.journal.module),
        "rank":new.journal.rank,"parent_count":new.parent_journals.len(),
        "expr_visits":support.expr_visits,"level_visits":support.level_visits,
        "address_count":support.address_count,"baseline_work":baseline.inference_work,
        "support_work":support.inference_work,
        "signed_work_removed":baseline.inference_work as i64 - support.inference_work as i64,
        "authority":"CONDITIONAL_ONLY_NOT_RECEIPT_OR_GUEST_COST"}))
}

pub fn run(fixture: Value) -> Value {
    let mut suite = Suite::default();
    suite.check("support_leaf_and_local_atomic", || {
        let mut a = Arena::new(); let zero = sort(&mut a)?;
        let high = a.node(Node::Bvar(u16::MAX))?; let loc = a.node(Node::Local(900, high))?;
        let z = a.support(zero)?; let h = a.support(high)?; let l = a.support(loc)?;
        require(z.loose == 0 && z.locals.is_none() && z.height == 0, "sort leaf")?;
        require(h.loose == 65536 && h.locals.is_none() && h.height == 0, "full u16 loose bound")?;
        require(l.loose == 0 && l.locals == Some((loc,loc)) && l.height == 0, "local type atomic")?;
        Ok(json!({"high_loose":h.loose,"local_id":loc}))
    });
    suite.check("support_app_union", || {
        let mut a = Arena::new(); let ty = sort(&mut a)?;
        let left = a.node(Node::Local(4,ty))?; let right = a.node(Node::Local(5,ty))?;
        let b = a.node(Node::Bvar(3))?; let app = a.node(Node::App(left,right))?;
        let root = a.node(Node::App(app,b))?; let s = a.support(root)?;
        require(s.loose == 4 && s.locals == Some((left,right)) && s.height == 2, "app support union")?;
        Ok(json!({"loose":s.loose,"height":s.height}))
    });
    suite.check("support_binder_domain_body", || {
        let mut a = Arena::new(); let zero = sort(&mut a)?;
        let b3 = a.node(Node::Bvar(3))?; let b4 = a.node(Node::Bvar(4))?;
        let pi = a.node(Node::Pi{origin:19,style:Style::Implicit,domain:b3,body:b4})?;
        let lam = a.node(Node::Lam{origin:23,style:Style::StrictImplicit,domain:zero,body:pi})?;
        let p = a.support(pi)?; let l = a.support(lam)?;
        require(p.loose == 4 && p.height == 1 && l.loose == 3 && l.height == 2,
            "only binder body decreases loose bound")?;
        Ok(json!({"pi_loose":p.loose,"lam_loose":l.loose}))
    });
    suite.check("support_identity_interning_charge", || {
        let mut a = Arena::new(); let id = a.node(Node::Bvar(0))?;
        require(a.census.inference_work == 2, "new leaf charges node and metadata")?;
        let before = a.census.inference_work; let again = a.node(Node::Bvar(0))?;
        require(again == id && a.nodes.len() == 1 && a.census.inference_work == before+1, "intern hit exact identity and charge")?;
        let before = a.census.inference_work; let s = a.support(id)?;
        require(s.loose == 1 && a.census.inference_work == before+1, "metadata query charged")?;
        Ok(json!({"nodes":a.nodes.len(),"work":a.census.inference_work}))
    });
    suite.negative("reject_unknown_support_id", || {
        let mut a = Arena::new(); refusal(a.support(0), "support node outside arena")
    });
    suite.negative("reject_unknown_child_id", || {
        let mut a = Arena::new(); let ty = sort(&mut a)?; let count = a.nodes.len();
        let result = a.node(Node::App(ty,usize::MAX));
        require(a.nodes.len() == count, "invalid child cannot insert partial node")?;
        refusal(result,"support node outside arena")
    });
    suite.check("open_closed_tree_constant_work", || {
        let mut tc = Typing::new()?; let (tree,leaf) = closed_tree(&mut tc,32)?;
        let before = tc.arena.census.inference_work; let out = tc.open(tree,leaf)?;
        let work = tc.arena.census.inference_work-before;
        require(out == tree && work == 2, "closed open is exact identity with depth/query charges")?;
        Ok(json!({"height":32,"open_work":work}))
    });
    suite.check("open_direct_bvar", || {
        let mut tc = Typing::new()?; let replacement = sort(&mut tc.arena)?;
        let b0 = tc.arena.node(Node::Bvar(0))?;
        require(tc.open(b0,replacement)? == replacement,"direct replacement")?; Ok(json!({}))
    });
    suite.check("open_nested_capture_sensitive", || {
        let mut tc = Typing::new()?; let ty = sort(&mut tc.arena)?; let r = local(&mut tc,300,ty)?;
        let b0 = tc.arena.node(Node::Bvar(0))?; let b1 = tc.arena.node(Node::Bvar(1))?;
        let body = tc.arena.node(Node::App(b1,b0))?;
        let e = tc.arena.node(Node::Pi{origin:71,style:Style::InstImplicit,domain:b0,body})?;
        let new_body = tc.arena.node(Node::App(r,b0))?;
        let expected = tc.arena.node(Node::Pi{origin:71,style:Style::InstImplicit,domain:r,body:new_body})?;
        require(tc.open(e,r)? == expected,"domain offset unchanged, body offset incremented")?; Ok(json!({}))
    });
    suite.negative("reject_open_larger_bvar", || {
        let mut tc = Typing::new()?; let r = sort(&mut tc.arena)?; let e = tc.arena.node(Node::Bvar(1))?;
        refusal(tc.open(e,r),"unopened outer variable")
    });
    suite.negative("reject_open_nested_larger_bvar", || {
        let mut tc = Typing::new()?; let r = sort(&mut tc.arena)?; let b2 = tc.arena.node(Node::Bvar(2))?;
        let e = tc.arena.node(Node::Lam{origin:5,style:Style::Default,domain:r,body:b2})?;
        refusal(tc.open(e,r),"unopened outer variable")
    });
    suite.check("open_closed_nested_binder_identity", || {
        let mut tc = Typing::new()?; let r = sort(&mut tc.arena)?; let b0 = tc.arena.node(Node::Bvar(0))?;
        let e = tc.arena.node(Node::Lam{origin:52,style:Style::StrictImplicit,domain:r,body:b0})?;
        require(tc.open(e,r)? == e,"bound variable and origin/style remain exact")?; Ok(json!({}))
    });
    suite.check("close_direct_local", || {
        let mut tc = Typing::new()?; let ty = sort(&mut tc.arena)?; let l = local(&mut tc,301,ty)?;
        let expected = tc.arena.node(Node::Bvar(0))?;
        require(tc.close(l,l)? == expected,"direct local abstraction")?; Ok(json!({}))
    });
    suite.check("close_nested_capture_sensitive", || {
        let mut tc = Typing::new()?; let ty = sort(&mut tc.arena)?; let l = local(&mut tc,302,ty)?;
        let b0 = tc.arena.node(Node::Bvar(0))?; let b1 = tc.arena.node(Node::Bvar(1))?;
        let domain = tc.arena.node(Node::App(l,ty))?; let body = tc.arena.node(Node::App(l,b0))?;
        let e = tc.arena.node(Node::Lam{origin:99,style:Style::Implicit,domain,body})?;
        let domain = tc.arena.node(Node::App(b0,ty))?; let body = tc.arena.node(Node::App(b1,b0))?;
        let expected = tc.arena.node(Node::Lam{origin:99,style:Style::Implicit,domain,body})?;
        require(tc.close(e,l)? == expected,"close under binder preserves offsets/origin/style")?; Ok(json!({}))
    });
    suite.check("close_outside_local_interval", || {
        let mut tc = Typing::new()?; let (e,ty) = closed_tree(&mut tc,32)?; let l = local(&mut tc,303,ty)?;
        let before = tc.arena.census.inference_work; let out = tc.close(e,l)?;
        let work = tc.arena.census.inference_work-before;
        require(out == e && work == 3,"close identity charges target/depth/support")?;
        Ok(json!({"height":32,"close_work":work}))
    });
    suite.check("close_inside_interval_absent", || {
        let mut tc = Typing::new()?; let ty = sort(&mut tc.arena)?;
        let a = local(&mut tc,401,ty)?; let gap = local(&mut tc,402,ty)?; let b = local(&mut tc,403,ty)?;
        let e = tc.arena.node(Node::App(a,b))?; let s = tc.arena.support(e)?;
        require(s.locals == Some((a,b)) && a < gap && gap < b,"conservative gap interval")?;
        let before = tc.arena.census.inference_work; let out = tc.close(e,gap)?;
        require(out == e && tc.arena.census.inference_work-before > 3,"false positive traverses without replacement")?;
        Ok(json!({"close_work":tc.arena.census.inference_work-before}))
    });
    suite.check("close_distinct_local_node_same_serial", || {
        let mut tc = Typing::new()?; let ty = sort(&mut tc.arena)?; let b0 = tc.arena.node(Node::Bvar(0))?;
        let a = local(&mut tc,501,ty)?; let b = local(&mut tc,501,b0)?;
        require(a != b && tc.close(a,b)? == a && tc.close(b,a)? == b,
            "local target is exact node identity in both interval directions, not serial")?; Ok(json!({}))
    });
    suite.check("local_type_is_atomic_for_both", || {
        let mut tc = Typing::new()?; let ty = sort(&mut tc.arena)?; let target = local(&mut tc,601,ty)?;
        let high = tc.arena.node(Node::Bvar(u16::MAX))?; let stored = tc.arena.node(Node::App(target,high))?;
        let outer = local(&mut tc,602,stored)?;
        require(tc.open(outer,ty)? == outer && tc.close(outer,target)? == outer,"stored local type is not traversed")?;
        Ok(json!({}))
    });
    suite.check("depth128_closed_tree", || {
        let mut tc = Typing::new()?; let (e,ty) = closed_tree(&mut tc,128)?; let l = local(&mut tc,701,ty)?;
        require(tc.open(e,ty)? == e && tc.close(e,l)? == e,"exact permitted shortcut height")?; Ok(json!({"height":128}))
    });
    suite.negative("reject_depth129_open", || {
        let mut tc = Typing::new()?; let (e,ty) = closed_tree(&mut tc,129)?;
        refusal(tc.open(e,ty),"internal traversal depth")
    });
    suite.negative("reject_depth129_close", || {
        let mut tc = Typing::new()?; let (e,ty) = closed_tree(&mut tc,129)?; let l = local(&mut tc,702,ty)?;
        refusal(tc.close(e,l),"internal traversal depth")
    });
    suite.negative("reject_open_deep_closed_child", || {
        let mut tc = Typing::new()?; let (tree,ty) = closed_tree(&mut tc,128)?;
        let b0 = tc.arena.node(Node::Bvar(0))?; let e = tc.arena.node(Node::App(tree,b0))?;
        refusal(tc.open(e,ty),"internal traversal depth")
    });
    suite.negative("reject_exhausted_open_budget", || {
        let mut tc = Typing::new()?; let ty = sort(&mut tc.arena)?;
        tc.arena.census.inference_work = MAX_WORK; refusal(tc.open(ty,ty),"inference work")
    });
    suite.check("open_exact_two_work_units", || {
        let mut tc = Typing::new()?; let ty = sort(&mut tc.arena)?;
        tc.arena.census.inference_work = MAX_WORK-2;
        require(tc.open(ty,ty)? == ty && tc.arena.census.inference_work == MAX_WORK,"exact charged shortcut budget")?;
        Ok(json!({"remaining_before":2,"remaining_after":0}))
    });
    suite.negative("reject_one_unit_open_budget", || {
        let mut tc = Typing::new()?; let ty = sort(&mut tc.arena)?;
        tc.arena.census.inference_work = MAX_WORK-1; let result = tc.open(ty,ty);
        require(tc.arena.census.inference_work == MAX_WORK+1,"failed metadata query has no refund")?;
        refusal(result,"inference work")
    });
    suite.negative("reject_partial_metadata_construction", || {
        let mut a = Arena::new(); a.census.inference_work = MAX_WORK-1;
        let result = a.node(Node::Bvar(0));
        require(a.nodes.is_empty() && a.census.inference_work == MAX_WORK+1,"no partial node or cost refund")?;
        refusal(result,"inference work")
    });
    suite.negative("reject_nonlocal_close_target", || {
        let mut tc = Typing::new()?; let ty = sort(&mut tc.arena)?;
        refusal(tc.close(ty,ty),"close requires internal local")
    });
    suite.negative("references_still_reject_unknown_constant", || {
        let mut tc = Typing::new()?; let ty = sort(&mut tc.arena)?;
        let address = Address::Owned([91;32],vec![NamePart::Str("missing".into())]);
        let e = tc.arena.node(Node::Const(address,vec![]))?;
        require(tc.open(e,ty)? == e,"closed constant shortcut is syntactic only")?;
        refusal(tc.references(e),"missing authenticated type dependency")
    });
    suite.check("first_exact_baseline_j_parents_census", || differential(&fixture["first"],
        "0ba261cd27c816223aa56bc6cbe217e67f48264b8d1c707326095492620a1657"));
    suite.check("second_exact_baseline_j_parents_census", || differential(&fixture["second"],
        "dce99babfd2e4e579c2981e6461e4b80c2f794da53b0959eb7494ee1f7c82d86"));
    let passed = suite.errors.is_empty() && suite.executed.len() == 30 && suite.refusals.len() == 12;
    json!({"schema":"DMKN_RC_SUPPORT_CONTROLS_V1","status":if passed {"PASS"} else {"FAIL"},
        "executed_count":suite.executed.len(),"executed":suite.executed,
        "expected_refusals":suite.refusals,"errors":suite.errors,
        "crypto_produced":false,"proof_calls":0,"guest_calls":0,"global_growth_claim":false,
        "authority":"NATIVE_CONDITIONAL_CONTROLS_NOT_RECEIPT_AUTHORITY"})
}
