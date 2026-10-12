//! Exact-warrant graph tests ONLY. Synthetic conditional journals exercise
//! bookkeeping, never bypass the production mathematical checker or receipts.
use super::*;
use crate::tests::journal;

fn conditional(seed: u8, rank: u64, parents: &[Journal]) -> module_relation::RelationConclusion {
    module_relation::RelationConclusion { journal:journal(seed,rank),
        parent_journals:parents.iter().map(|j| j.encode().unwrap()).collect() }
}

#[test]
fn honest_variant_branch_shape_merges_without_rewriting_parents() {
    let helper = journal(11,0); let m0 = journal(1,0); let m1 = journal(1,1);
    let c1 = journal(2,1); let c2 = journal(3,2); let target = journal(4,3);
    assert_eq!(m0.module,m1.module); assert_ne!(m0.encode().unwrap(),m1.encode().unwrap());
    let mut graph = Graph::default(); graph.frontier(helper.encode().unwrap()).unwrap();
    graph.delta(conditional(1,0,&[])).unwrap();
    graph.delta(conditional(1,1,&[helper.clone()])).unwrap();
    graph.delta(conditional(2,1,&[m0.clone()])).unwrap();
    graph.delta(conditional(3,2,&[m1.clone()])).unwrap();
    graph.delta(conditional(4,3,&[c1.clone(),c2.clone()])).unwrap();
    graph.closure(&[target.encode().unwrap()]).unwrap();
    assert_eq!((graph.nodes.len(),graph.edges),(6,5));
    assert_eq!(graph.nodes[&c1.encode().unwrap()].parents,vec![m0.encode().unwrap()]);
    assert_eq!(graph.nodes[&c2.encode().unwrap()].parents,vec![m1.encode().unwrap()]);
    let bytes = graph.nodes.keys().cloned().collect::<Vec<_>>();
    assert!(bytes.windows(2).all(|pair| pair[0] < pair[1]));
    membership::commitment(&bytes).unwrap();
}

#[test]
fn missing_or_forged_exact_variant_is_not_replaced_by_same_module() {
    let m0 = journal(1,0); let m1 = journal(1,1);
    let mut graph = Graph::default(); graph.frontier(m0.encode().unwrap()).unwrap();
    assert!(graph.delta(conditional(2,2,&[m1])).unwrap_err().contains("unestablished exact"));
    assert!(graph.delta(conditional(2,2,&[m0.clone()])).unwrap_err().contains("exact mathematical rank"));
    assert!(graph.delta(conditional(2,0,&[m0.clone()])).is_err());
    assert!(graph.delta(conditional(2,1,&[m0.clone(),m0.clone()])).is_err());
    assert!(graph.frontier(m0.encode().unwrap()).unwrap_err().contains("duplicate exact journal"));
    graph.delta(conditional(2,1,&[m0])).unwrap();
}

#[test]
fn exact_targets_disambiguate_variants_and_refuse_unused_material() {
    let helper = journal(11,0); let m0 = journal(1,0); let m1 = journal(1,1);
    let mut graph = Graph::default(); graph.frontier(helper.encode().unwrap()).unwrap();
    graph.delta(conditional(1,0,&[])).unwrap(); graph.delta(conditional(1,1,&[helper])).unwrap();
    assert!(graph.closure(&[m0.module.to_vec()]).is_err());
    assert!(graph.closure(&[journal(1,2).encode().unwrap()]).is_err());
    assert!(graph.closure(&[m0.encode().unwrap()]).unwrap_err().contains("unused"));
    assert!(graph.closure(&[m1.encode().unwrap()]).unwrap_err().contains("unused"));
    graph.closure(&[m0.encode().unwrap(),m1.encode().unwrap()]).unwrap();
    assert!(graph.closure(&[m0.encode().unwrap(),m0.encode().unwrap()]).is_err());
    graph.frontier(journal(1,2).encode().unwrap()).unwrap();
    assert!(graph.closure(&[m0.encode().unwrap(),m1.encode().unwrap()]).unwrap_err().contains("unused"));
}

#[test]
fn cycles_and_overflow_cannot_be_introduced_by_warrant_aliases() {
    let low = journal(1,1); let high = journal(2,2);
    let mut graph = Graph::default();
    assert!(graph.delta(conditional(2,2,&[low.clone()])).is_err());
    graph.frontier(high.encode().unwrap()).unwrap();
    assert!(graph.delta(conditional(1,1,&[high.clone()])).is_err());
    assert!(graph.delta(conditional(2,2,&[high])).is_err());
    let mut graph = Graph::default(); let maximum = journal(3,u64::MAX);
    graph.frontier(maximum.encode().unwrap()).unwrap();
    assert!(graph.delta(conditional(4,0,&[maximum])).is_err());
    let mut graph = Graph::default(); let base = journal(1,0);
    graph.frontier(base.encode().unwrap()).unwrap(); graph.edges = MAX_EDGES;
    assert!(graph.delta(conditional(2,1,&[base])).is_err());
}

#[test]
fn member_limit_counts_exact_variants_not_distinct_semantics() {
    let mut graph = Graph::default();
    for rank in 0..MAX_MEMBERS { graph.frontier(journal(1,rank as u64).encode().unwrap()).unwrap(); }
    assert_eq!(graph.nodes.len(),48);
    assert!(graph.frontier(journal(1,48).encode().unwrap()).is_err());
}
