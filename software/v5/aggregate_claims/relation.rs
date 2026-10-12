//! All new mathematics uses the unchanged checker. This conclusion is ONLY
//! conditional until the guest verifies every unique returned receipt claim.
use crate::{header::{self, Header, MAX_MEMBERS}, membership, wire::{self, Reader}, Census};
use dmkn_module_relation::{canonical::{require, R}, journal::{self, Journal}, policy,
    relation as module_relation};
use std::{collections::{BTreeMap, BTreeSet}, io::Read};

pub const MAX_ASSUMPTIONS: usize = 8;
pub const MAX_FRONTIERS: usize = 32;
pub const MAX_DELTAS: usize = 16;
pub const MAX_EDGES: usize = 128;

/// An exact pending SDK claim, never a serialized `verified` assertion.
#[derive(Debug)]
pub struct PendingAssumption {
    image: [u32; 8],
    journal: Vec<u8>,
}
impl PendingAssumption {
    pub fn image(&self) -> [u32; 8] { self.image }
    pub fn journal(&self) -> &[u8] { &self.journal }
}

/// Private construction prevents alternate public entry points from inventing
/// checked graph conclusions. It still carries NO actual receipt authority.
#[derive(Debug)]
pub struct ConditionalConclusion {
    header: Header,
    assumptions: Vec<PendingAssumption>,
    members: Vec<Vec<u8>>,
    census: Census,
    edges: usize,
    wire_bytes: usize,
}
impl ConditionalConclusion {
    pub fn header(&self) -> &Header { &self.header }
    pub fn assumptions(&self) -> &[PendingAssumption] { &self.assumptions }
    pub fn members(&self) -> &[Vec<u8>] { &self.members }
    pub fn census(&self) -> &Census { &self.census }
    pub fn edges(&self) -> usize { self.edges }
    pub fn wire_bytes(&self) -> usize { self.wire_bytes }
}

struct Descriptor {
    claim: PendingAssumption,
    aggregate: Option<Header>,
}
struct Node {
    journal: Journal,
    bytes: Vec<u8>,
    parents: Vec<Vec<u8>>,
    delta: bool,
}
#[derive(Default)]
struct Graph { nodes: BTreeMap<Vec<u8>, Node>, edges: usize }

impl Graph {
    fn insert(&mut self, journal: Journal, bytes: Vec<u8>, parents: Vec<Vec<u8>>, delta: bool) -> R<()> {
        require(self.nodes.len() < MAX_MEMBERS && !self.nodes.contains_key(&bytes),
            "aggregate member budget or duplicate exact journal")?;
        self.nodes.insert(bytes.clone(), Node { journal, bytes, parents, delta });
        Ok(())
    }
    fn frontier(&mut self, bytes: Vec<u8>) -> R<()> {
        let journal = header::member_journal(&bytes)?;
        self.insert(journal, bytes, Vec::new(), false)
    }
    fn delta(&mut self, conclusion: module_relation::RelationConclusion) -> R<()> {
        let bytes = conclusion.journal.encode()?;
        let journal = header::member_journal(&bytes)?;
        let mut parents = Vec::new();
        let mut unique = BTreeSet::new();
        let mut greatest = None::<u64>;
        for parent_bytes in &conclusion.parent_journals {
            let parent = header::member_journal(parent_bytes)?;
            let established = self.nodes.get(parent_bytes).ok_or("unestablished exact delta premise")?;
            require(established.bytes == *parent_bytes && parent.rank < journal.rank,
                "delta premise exact journal/rank")?;
            require(unique.insert(parent_bytes.clone()), "duplicate delta premise")?;
            greatest = Some(greatest.map_or(parent.rank, |r| r.max(parent.rank)));
            parents.push(parent_bytes.clone());
        }
        let expected_rank = match greatest {
            None => 0,
            Some(rank) => rank.checked_add(1).ok_or("aggregate mathematical rank overflow")?,
        };
        require(journal.rank == expected_rank, "aggregate exact mathematical rank")?;
        self.edges = self.edges.checked_add(parents.len()).ok_or("aggregate edge overflow")?;
        require(self.edges <= MAX_EDGES, "aggregate edge budget")?;
        self.insert(journal, bytes, parents, true)
    }
    fn closure(&self, targets: &[Vec<u8>]) -> R<()> {
        require(!targets.is_empty(), "nonempty aggregate targets")?;
        let mut unique = BTreeSet::new();
        for target in targets {
            require(unique.insert(target.clone()), "unique aggregate targets")?;
            require(self.nodes.get(target).map_or(false, |node| node.delta),
                "aggregate target must be an exact newly checked delta warrant")?;
        }
        let mut pending = targets.to_vec();
        let mut reached = BTreeSet::new();
        while let Some(warrant) = pending.pop() {
            if !reached.insert(warrant.clone()) { continue; }
            let node = self.nodes.get(&warrant).ok_or("target closure missing member")?;
            pending.extend_from_slice(&node.parents);
        }
        require(reached.len() == self.nodes.len(), "unused frontier/delta outside target closure")
    }
}

/// Reads one bounded frame at a time. No verifier/checker callback is accepted.
/// Errors/panics cannot produce a guest journal; the guest wrapper fails closed.
pub fn check_reader<T: Read>(input: T) -> R<ConditionalConclusion> {
    let mut input = Reader::new(input);
    require(&input.fixed::<8>()? == wire::MAGIC && input.u32()? == wire::VERSION,
        "aggregate input magic/version")?;
    let image = header::image_words(input.fixed()?);
    header::distinct_aggregate_image(image)?;
    let assumption_count = input.u32()? as usize;
    let frontier_count = input.u32()? as usize;
    let delta_count = input.u32()? as usize;
    let target_count = input.u32()? as usize;
    require(assumption_count <= MAX_ASSUMPTIONS && frontier_count <= MAX_FRONTIERS
        && delta_count > 0 && delta_count <= MAX_DELTAS && target_count > 0
        && target_count <= delta_count, "aggregate input count limits")?;
    require(frontier_count.checked_add(delta_count).ok_or("member count overflow")? <= MAX_MEMBERS,
        "aggregate total member count")?;
    let mut descriptors = Vec::with_capacity(assumption_count);
    let mut unique_claims = BTreeSet::new();
    let mut maximum_parent_height = 0u64;
    for _ in 0..assumption_count {
        let tag = input.fixed::<1>()?[0];
        let descriptor = match tag {
            0 => {
                let bytes = input.fixed::<{journal::BYTES}>()?.to_vec();
                header::member_journal(&bytes)?;
                Descriptor { claim: PendingAssumption { image: header::relation_image(), journal: bytes }, aggregate: None }
            },
            1 => {
                let bytes = input.fixed::<{header::BYTES}>()?.to_vec();
                let parent = Header::decode(&bytes)?;
                parent.bind_image(image)?;
                maximum_parent_height = maximum_parent_height.max(parent.seal_height);
                Descriptor { claim: PendingAssumption { image, journal: bytes }, aggregate: Some(parent) }
            },
            _ => return Err("unknown aggregate assumption tag".into()),
        };
        require(unique_claims.insert((descriptor.claim.image, descriptor.claim.journal.clone())),
            "duplicate aggregate assumption claim")?;
        descriptors.push(descriptor);
    }
    let seal_height = maximum_parent_height.checked_add(1).ok_or("aggregate seal height overflow")?;
    let mut graph = Graph::default();
    let mut used = vec![false; assumption_count];
    for _ in 0..frontier_count {
        let assumption_index = input.u32()? as usize;
        require(assumption_index < descriptors.len(), "frontier assumption index")?;
        let bytes = input.fixed::<{journal::BYTES}>()?.to_vec();
        let member_index = input.u32()?;
        let sibling_count = input.u32()? as usize;
        require(sibling_count <= membership::MAX_SIBLINGS, "frontier sibling bound")?;
        let mut siblings = Vec::with_capacity(sibling_count);
        for _ in 0..sibling_count { siblings.push(input.fixed::<32>()?); }
        let descriptor = &descriptors[assumption_index];
        match &descriptor.aggregate {
            None => require(member_index == 0 && siblings.is_empty() && bytes == descriptor.claim.journal,
                "legacy frontier exact journal and empty opening")?,
            Some(header) => { membership::verify(header, &bytes, member_index, &siblings)?; },
        }
        graph.frontier(bytes)?;
        used[assumption_index] = true;
    }
    require(used.iter().all(|used| *used), "unused aggregate assumption descriptor")?;
    let mut targets = Vec::with_capacity(target_count);
    let mut unique_targets = BTreeSet::new();
    for _ in 0..target_count {
        let target = input.fixed::<{journal::BYTES}>()?.to_vec();
        header::member_journal(&target)?;
        require(unique_targets.insert(target.clone()), "duplicate input target")?;
        targets.push(target);
    }
    let mut census = Census::default();
    for _ in 0..delta_count {
        let bytes = input.frame()?;
        let value = census.charge(&bytes)?;
        // Same check_bound, retaining the second canonical_size traversal.
        // This is the ONLY production path introducing a new delta conclusion.
        let conclusion = module_relation::check(value)?;
        graph.delta(conclusion)?;
        // `bytes` and all relation-owned expression trees die before next frame.
    }
    let wire_bytes = input.end()?;
    graph.closure(&targets)?;
    require(census.parent_edges == graph.edges, "aggregate actual edge census")?;
    let members = graph.nodes.values().map(|n| n.bytes.clone()).collect::<Vec<_>>();
    let maximum_member_rank = graph.nodes.values().map(|n| n.journal.rank).max()
        .ok_or("aggregate empty graph")?;
    let header = Header {
        aggregate_image: image, relation_image: header::relation_image(),
        foundation: policy::foundation(), policy: policy::semantic_id()?,
        members_root: membership::commitment(&members)?, member_count: members.len() as u32,
        maximum_member_rank, seal_height,
    };
    header.validate()?;
    Ok(ConditionalConclusion { header, assumptions: descriptors.into_iter().map(|d| d.claim).collect(),
        members, census, edges: graph.edges, wire_bytes })
}

pub fn check_bytes(bytes: &[u8]) -> R<ConditionalConclusion> {
    require(bytes.len() <= wire::MAX_BYTES, "aggregate complete input bound")?;
    check_reader(std::io::Cursor::new(bytes))
}

#[cfg(test)]
#[path = "graph_controls.rs"]
mod graph_controls;
