//! V2 structure/encoding controls. Synthetic journals and pending claims below
//! are NOT mathematical proofs, receipt verification or native admission.
use crate::{header::{self, Header}, membership, relation, wire, Census};
use dmkn_module_relation::{canonical::{hash, sha}, journal::Journal, policy};
use serde_json::json;

pub(crate) fn journal(seed: u8, rank: u64) -> Journal {
    let mut journal = Journal {
        image: header::relation_image(), foundation: policy::foundation(),
        policy: policy::semantic_id().unwrap(), module: [0; 32], group_root: [seed; 32],
        group_count: 1, rank,
    };
    journal.module = hash("module-spec", &journal.summary()).unwrap();
    journal
}

fn members(count: usize) -> Vec<Vec<u8>> {
    let mut values = (0..count).map(|i| journal(i as u8, i as u64).encode().unwrap()).collect::<Vec<_>>();
    values.sort(); values
}

fn header(members: &[Vec<u8>]) -> Header {
    Header {
        aggregate_image:[7;8], relation_image:header::relation_image(),
        foundation:policy::foundation(), policy:policy::semantic_id().unwrap(),
        members_root:membership::commitment(members).unwrap(), member_count:members.len() as u32,
        maximum_member_rank:members.iter().map(|b| Journal::decode(b).unwrap().rank).max().unwrap(),
        seal_height:1,
    }
}

fn prefix(assumptions: u32, frontiers: u32, deltas: u32, targets: u32) -> Vec<u8> {
    let mut bytes = wire::MAGIC.to_vec(); bytes.extend_from_slice(&wire::VERSION.to_le_bytes());
    bytes.extend_from_slice(&header::image_bytes([7;8]));
    for count in [assumptions,frontiers,deltas,targets] { bytes.extend_from_slice(&count.to_le_bytes()); }
    bytes
}

fn legacy(out: &mut Vec<u8>, bytes: &[u8]) { out.push(0); out.extend_from_slice(bytes); }
fn frontier(out: &mut Vec<u8>, claim: u32, bytes: &[u8]) {
    out.extend_from_slice(&claim.to_le_bytes()); out.extend_from_slice(bytes);
    out.extend_from_slice(&0u32.to_le_bytes()); out.extend_from_slice(&0u32.to_le_bytes());
}

#[test]
fn v2_header_profile_and_explicit_v1_rejection() {
    let original = header(&members(3)); let bytes = original.encode().unwrap();
    assert_eq!(bytes.len(),192); assert_eq!(&bytes[..8],b"DMKNA002");
    assert_eq!(&bytes[8..12],&2u32.to_le_bytes());
    assert_eq!(Header::decode(&bytes).unwrap(),original);
    assert!(Journal::decode(&bytes).is_err());
    let mut v1 = bytes.clone(); v1[..8].copy_from_slice(b"DMKNA001");
    v1[8..12].copy_from_slice(&1u32.to_le_bytes()); assert!(Header::decode(&v1).is_err());
    assert!(Header::decode(&bytes[..191]).is_err());
    let mut extra = bytes.clone(); extra.push(0); assert!(Header::decode(&extra).is_err());
    for offset in [0,8,44,76,108] {
        let mut wrong = bytes.clone(); wrong[offset] ^= 1; assert!(Header::decode(&wrong).is_err());
    }
    assert!(original.bind_image([8;8]).is_err());
    let mut wrong = original.clone(); wrong.aggregate_image = header::relation_image();
    assert!(wrong.validate().is_err()); wrong.aggregate_image = [0;8]; assert!(wrong.validate().is_err());
    wrong = original.clone(); wrong.member_count = 0; assert!(wrong.validate().is_err());
    wrong.member_count = 49; assert!(wrong.validate().is_err());
    wrong = original; wrong.seal_height = 0; assert!(wrong.validate().is_err());
}

#[test]
fn exact_warrant_membership_variants_lexicographic_order_and_domains() {
    let m1 = journal(9,1).encode().unwrap(); let m256 = journal(9,256).encode().unwrap();
    assert_eq!(Journal::decode(&m1).unwrap().module,Journal::decode(&m256).unwrap().module);
    assert!(m256 < m1,"full LE journal ordering is not numeric rank ordering");
    let values = vec![m256.clone(),m1.clone()]; let root = header(&values);
    for (index,bytes) in values.iter().enumerate() {
        let path = membership::opening(&values,index as u32).unwrap();
        assert_eq!(membership::verify(&root,bytes,index as u32,&path).unwrap(),Journal::decode(bytes).unwrap());
        assert!(membership::verify(&root,&values[1-index],index as u32,&path).is_err());
    }
    assert!(membership::commitment(&[m1.clone(),m256]).is_err());
    assert!(membership::commitment(&[m1.clone(),m1.clone()]).is_err());
    // The unchanged legacy J is NOT enough to cross aggregate commitment domains.
    let mut old_leaf = b"DMKN-V5-AGGREGATE\0LEAF\0".to_vec();
    old_leaf.extend_from_slice(&1u32.to_le_bytes()); old_leaf.extend_from_slice(&0u32.to_le_bytes());
    old_leaf.extend_from_slice(&m1);
    let mut old_root = b"DMKN-V5-AGGREGATE\0ROOT\0".to_vec();
    old_root.extend_from_slice(&1u32.to_le_bytes()); old_root.extend_from_slice(&sha(&old_leaf));
    let mut changed = header(&[m1.clone()]); changed.members_root = sha(&old_root);
    assert!(membership::verify(&changed,&m1,0,&[]).is_err());
}

#[test]
fn v2_merkle_odd_padding_limits_and_tampering() {
    for count in [1,2,3,5,16,31,32,33,48] {
        let values = members(count); let root = header(&values);
        for (index,bytes) in values.iter().enumerate() {
            let path = membership::opening(&values,index as u32).unwrap();
            membership::verify(&root,bytes,index as u32,&path).unwrap();
            let mut altered = Journal::decode(bytes).unwrap(); altered.rank += 1;
            assert!(membership::verify(&root,&altered.encode().unwrap(),index as u32,&path).is_err());
            let mut extra = path.clone(); extra.push([0;32]);
            assert!(membership::verify(&root,bytes,index as u32,&extra).is_err());
            if !path.is_empty() {
                let mut wrong = path.clone(); wrong[0][0] ^= 1;
                assert!(membership::verify(&root,bytes,index as u32,&wrong).is_err());
                assert!(membership::verify(&root,bytes,index as u32,&path[..path.len()-1]).is_err());
            }
        }
        assert!(membership::verify(&root,&values[0],count as u32,&[]).is_err());
    }
    let values = members(3); let root = header(&values);
    let mut path = membership::opening(&values,2).unwrap(); path[0][0] ^= 1;
    assert!(membership::verify(&root,&values[2],2,&path).unwrap_err().contains("odd padding"));
    assert!(membership::commitment(&[]).is_err()); assert!(membership::commitment(&members(49)).is_err());
}

#[test]
fn v2_wire_requires_exact_journal_targets_not_semantic_ids() {
    let mut old = prefix(0,0,1,1); old[..8].copy_from_slice(b"DMKNAI01");
    old[8..12].copy_from_slice(&1u32.to_le_bytes());
    assert!(relation::check_bytes(&old).unwrap_err().contains("magic/version"));
    let target = journal(1,0);
    let mut short = prefix(0,0,1,1); short.extend_from_slice(&target.module);
    assert!(relation::check_bytes(&short).unwrap_err().contains("truncated field"));
    let mut duplicates = prefix(0,0,2,2);
    duplicates.extend_from_slice(&target.encode().unwrap()); duplicates.extend_from_slice(&target.encode().unwrap());
    assert!(relation::check_bytes(&duplicates).unwrap_err().contains("duplicate input target"));
    let mut invalid = prefix(0,0,1,1); invalid.extend_from_slice(&[0;184]);
    assert!(relation::check_bytes(&invalid).is_err());
    let mut reader = wire::Reader::new(std::io::Cursor::new(u32::MAX.to_le_bytes()));
    assert!(reader.frame().unwrap_err().contains("wire byte budget"));
    let mut reader = wire::Reader::new(std::io::Cursor::new(0u32.to_le_bytes()));
    assert!(reader.frame().unwrap_err().contains("nonempty"));
    let mut reader = wire::Reader::new(std::io::Cursor::new(2u32.to_le_bytes()));
    assert!(reader.frame().unwrap_err().contains("truncated delta"));
    let mut reader = wire::Reader::new(std::io::Cursor::new([9]));
    assert!(reader.end().unwrap_err().contains("exact EOF"));
}

#[test]
fn v2_metadata_exact_claims_unused_material_and_height() {
    let bytes = journal(1,0).encode().unwrap();
    let mut input = prefix(2,2,1,1); legacy(&mut input,&bytes); legacy(&mut input,&bytes);
    assert!(relation::check_bytes(&input).unwrap_err().contains("duplicate aggregate assumption"));
    let mut input = prefix(1,0,1,1); legacy(&mut input,&bytes);
    assert!(relation::check_bytes(&input).unwrap_err().contains("unused aggregate assumption"));
    let mut input = prefix(1,2,1,1); legacy(&mut input,&bytes);
    frontier(&mut input,0,&bytes); frontier(&mut input,0,&bytes);
    assert!(relation::check_bytes(&input).unwrap_err().contains("duplicate exact journal"));
    let mut input = prefix(1,1,1,1); legacy(&mut input,&bytes);
    frontier(&mut input,0,&journal(1,1).encode().unwrap());
    assert!(relation::check_bytes(&input).unwrap_err().contains("legacy frontier exact"));
    let mut parent = header(&members(2)); parent.aggregate_image = [8;8];
    let mut input = prefix(1,0,1,1); input.push(1); input.extend_from_slice(&parent.encode().unwrap());
    assert!(relation::check_bytes(&input).unwrap_err().contains("actual image binding"));
    parent.aggregate_image = [7;8]; parent.seal_height = u64::MAX;
    let mut input = prefix(1,0,1,1); input.push(1); input.extend_from_slice(&parent.encode().unwrap());
    assert!(relation::check_bytes(&input).unwrap_err().contains("seal height overflow"));
    assert!(relation::check_bytes(&prefix(9,0,1,1)).is_err());
    assert!(relation::check_bytes(&prefix(0,0,0,0)).is_err());
}

#[test]
fn reused_parse_once_census_keeps_global_caps_and_owned_value() {
    let value = json!({"schema":"shape-only","image":[0,0,0,0,0,0,0,0],"rank":0,
        "local_spec":{},"rows":[0,1],"parents":[{"journal":[],"openings":[{},{}]}],"bodies":[{}]});
    let bytes = serde_json::to_vec(&value).unwrap(); let mut census = Census::default();
    assert_eq!(census.charge(&bytes).unwrap(),value); census.charge(&bytes).unwrap();
    assert_eq!((census.rows,census.openings,census.bodies,census.parent_edges),(4,4,2,2));
    census.rows = crate::census::MAX_ROWS; assert!(census.charge(&bytes).is_err());
    let mut census = Census { nodes:usize::MAX, ..Census::default() };
    assert!(census.charge(&bytes).unwrap_err().contains("overflow"));
    assert!(Census::default().charge(br#"{"rows":[],"rows":[]}"#).is_err());
}
