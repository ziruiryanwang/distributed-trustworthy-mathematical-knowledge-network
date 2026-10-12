//! Structural membership only. Callers MUST first verify the genuine A receipt.
use crate::header::{member_journal, Header, MAX_MEMBERS};
use dmkn_module_relation::{canonical::{require, sha, R}, journal::Journal};

pub const MAX_SIBLINGS: usize = 6;
const LEAF_DOMAIN: &[u8] = b"DMKN-V5-AGGREGATE-V2\0LEAF\0";
const NODE_DOMAIN: &[u8] = b"DMKN-V5-AGGREGATE-V2\0NODE\0";
const ROOT_DOMAIN: &[u8] = b"DMKN-V5-AGGREGATE-V2\0ROOT\0";

fn leaf(count: u32, index: u32, journal: &[u8]) -> [u8; 32] {
    let mut bytes = LEAF_DOMAIN.to_vec();
    bytes.extend_from_slice(&count.to_le_bytes());
    bytes.extend_from_slice(&index.to_le_bytes());
    bytes.extend_from_slice(journal);
    sha(&bytes)
}

fn node(count: u32, level: u32, left: [u8; 32], right: [u8; 32]) -> [u8; 32] {
    let mut bytes = NODE_DOMAIN.to_vec();
    bytes.extend_from_slice(&count.to_le_bytes());
    bytes.extend_from_slice(&level.to_le_bytes());
    bytes.extend_from_slice(&left);
    bytes.extend_from_slice(&right);
    sha(&bytes)
}

fn root(count: u32, top: [u8; 32]) -> [u8; 32] {
    let mut bytes = ROOT_DOMAIN.to_vec();
    bytes.extend_from_slice(&count.to_le_bytes());
    bytes.extend_from_slice(&top);
    sha(&bytes)
}

fn leaves(journals: &[Vec<u8>]) -> R<Vec<[u8; 32]>> {
    require(!journals.is_empty() && journals.len() <= MAX_MEMBERS, "member commitment count")?;
    let mut previous: Option<&[u8]> = None;
    let mut hashes = Vec::with_capacity(journals.len());
    for (index, bytes) in journals.iter().enumerate() {
        member_journal(bytes)?;
        require(previous.map_or(true, |journal| journal < bytes.as_slice()),
            "strict exact-journal member order")?;
        previous = Some(bytes.as_slice());
        hashes.push(leaf(journals.len() as u32, index as u32, bytes));
    }
    Ok(hashes)
}

fn next_level(count: u32, level: u32, hashes: &[[u8; 32]]) -> Vec<[u8; 32]> {
    hashes.chunks(2).map(|pair| node(count, level, pair[0], *pair.get(1).unwrap_or(&pair[0]))).collect()
}

/// Requires canonical sorted, unique, structurally valid journals.
pub fn commitment(journals: &[Vec<u8>]) -> R<[u8; 32]> {
    let mut hashes = leaves(journals)?;
    let count = hashes.len() as u32;
    let mut level = 0;
    while hashes.len() > 1 {
        hashes = next_level(count, level, &hashes);
        level += 1;
    }
    Ok(root(count, hashes[0]))
}

/// Produces inert opening material, not mathematical authority.
pub fn opening(journals: &[Vec<u8>], index: u32) -> R<Vec<[u8; 32]>> {
    let mut hashes = leaves(journals)?;
    require((index as usize) < hashes.len(), "member opening index")?;
    let count = hashes.len() as u32;
    let mut position = index as usize;
    let mut level = 0;
    let mut siblings = Vec::new();
    while hashes.len() > 1 {
        let other = position ^ 1;
        siblings.push(*hashes.get(other).unwrap_or(&hashes[position]));
        hashes = next_level(count, level, &hashes);
        position /= 2;
        level += 1;
    }
    Ok(siblings)
}

pub fn verify(header: &Header, bytes: &[u8], index: u32, siblings: &[[u8; 32]]) -> R<Journal> {
    header.validate()?;
    let journal = member_journal(bytes)?;
    require(index < header.member_count && journal.rank <= header.maximum_member_rank,
        "member index/rank")?;
    let mut expected_depth = 0;
    let mut width = header.member_count;
    while width > 1 { expected_depth += 1; width = (width + 1) / 2; }
    require(siblings.len() == expected_depth && siblings.len() <= MAX_SIBLINGS,
        "member exact path length")?;
    let mut hash = leaf(header.member_count, index, bytes);
    let mut position = index;
    width = header.member_count;
    for (level, sibling) in siblings.iter().enumerate() {
        if position % 2 == 0 {
            if position + 1 == width {
                require(*sibling == hash, "member deterministic odd padding")?;
            }
            hash = node(header.member_count, level as u32, hash, *sibling);
        } else {
            hash = node(header.member_count, level as u32, *sibling, hash);
        }
        position /= 2;
        width = (width + 1) / 2;
    }
    require(root(header.member_count, hash) == header.members_root, "member root binding")?;
    Ok(journal)
}
