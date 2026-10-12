//! Private graph bookkeeping controls use synthetic conditional statements.
//! They are not mathematical-checker or cryptographic evidence.
use super::*;
use crate::tests::journal;

fn conditional(seed: u8, rank: u64, parents: &[Journal]) -> module_relation::RelationConclusion {
    module_relation::RelationConclusion { journal: journal(seed, rank),
        parent_journals: parents.iter().map(|j| j.encode().unwrap()).collect() }
}

#[test]
fn exact_branching_closure_and_targets() {
    let base = journal(1, 0); let first = journal(2, 1); let second = journal(3, 2);
    let mut graph = Graph::default(); graph.frontier(base.encode().unwrap()).unwrap();
    graph.delta(conditional(2, 1, &[base.clone()])).unwrap();
    graph.delta(conditional(3, 2, &[base.clone(), first.clone()])).unwrap();
    graph.closure(&[second.module]).unwrap();
    assert_eq!(graph.edges, 3);
    assert!(graph.closure(&[]).is_err());
    assert!(graph.closure(&[base.module]).is_err());
    assert!(graph.closure(&[first.module]).is_err());
    assert!(graph.closure(&[second.module, second.module]).is_err());
    graph.frontier(journal(4, 0).encode().unwrap()).unwrap();
    assert!(graph.closure(&[second.module]).is_err());
}

#[test]
fn premises_cannot_be_missing_reordered_or_changed() {
    let base = journal(1, 0); let first = journal(2, 1);
    let mut graph = Graph::default();
    assert!(graph.delta(conditional(2, 1, &[base.clone()])).is_err());
    graph.frontier(base.encode().unwrap()).unwrap();
    assert!(graph.delta(conditional(3, 2, &[first])).is_err());
    let mut altered = base.clone(); altered.rank = 1;
    assert!(graph.delta(conditional(2, 2, &[altered])).is_err());
    assert!(graph.delta(conditional(2, 1, &[base.clone(), base.clone()])).is_err());
    assert!(graph.delta(conditional(2, 2, &[base.clone()])).is_err());
    assert!(graph.delta(conditional(2, 0, &[base.clone()])).is_err());
    assert!(graph.frontier(base.encode().unwrap()).is_err());
    graph.delta(conditional(2, 1, &[base])).unwrap();
    assert!(graph.delta(conditional(2, 0, &[])).is_err());
}

#[test]
fn limits_and_rank_do_not_wrap() {
    let base = journal(1, u64::MAX);
    let mut graph = Graph::default(); graph.frontier(base.encode().unwrap()).unwrap();
    assert!(graph.delta(conditional(2, 0, &[base])).is_err());
    let mut graph = Graph::default(); graph.frontier(journal(1, 0).encode().unwrap()).unwrap();
    graph.edges = MAX_EDGES;
    assert!(graph.delta(conditional(2, 1, &[journal(1, 0)])).is_err());
    let mut graph = Graph::default();
    for seed in 0..MAX_MEMBERS { graph.frontier(journal(seed as u8, 0).encode().unwrap()).unwrap(); }
    assert!(graph.frontier(journal(99, 0).encode().unwrap()).is_err());
}
