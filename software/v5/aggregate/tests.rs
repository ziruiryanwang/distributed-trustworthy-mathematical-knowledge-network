//! Structural/source controls only: fabricated well-formed journals below are
//! NOT mathematical receipts. No aggregate acceptance authority is constructed.
use crate::{header::{self, Header}, membership, relation, wire, Census};
use dmkn_module_relation::{canonical::hash, journal::Journal, policy};
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
    let mut values = (0..count).map(|i| journal(i as u8, i as u64)).collect::<Vec<_>>();
    values.sort_by_key(|j| j.module);
    values.into_iter().map(|j| j.encode().unwrap()).collect()
}
fn header(members: &[Vec<u8>]) -> Header {
    Header {
        aggregate_image: [7; 8], relation_image: header::relation_image(),
        foundation: policy::foundation(), policy: policy::semantic_id().unwrap(),
        members_root: membership::commitment(members).unwrap(), member_count: members.len() as u32,
        maximum_member_rank: members.iter().map(|b| Journal::decode(b).unwrap().rank).max().unwrap(),
        seal_height: 1,
    }
}
fn prefix(assumptions: u32, frontiers: u32, deltas: u32, targets: u32) -> Vec<u8> {
    let mut out = wire::MAGIC.to_vec();
    out.extend_from_slice(&wire::VERSION.to_le_bytes());
    out.extend_from_slice(&header::image_bytes([7; 8]));
    for count in [assumptions, frontiers, deltas, targets] { out.extend_from_slice(&count.to_le_bytes()); }
    out
}
fn legacy(out: &mut Vec<u8>, bytes: &[u8]) { out.push(0); out.extend_from_slice(bytes); }
fn frontier(out: &mut Vec<u8>, claim: u32, bytes: &[u8]) {
    out.extend_from_slice(&claim.to_le_bytes()); out.extend_from_slice(bytes);
    out.extend_from_slice(&0u32.to_le_bytes()); out.extend_from_slice(&0u32.to_le_bytes());
}

#[test]
fn header_exact_distinct_roundtrip_and_profile() {
    let original = header(&members(3));
    let bytes = original.encode().unwrap();
    assert_eq!(bytes.len(), 192);
    assert_eq!(&bytes[..8], b"DMKNA001");
    assert_eq!(&bytes[12..44], &header::image_bytes([7; 8]));
    assert_eq!(Header::decode(&bytes).unwrap(), original);
    assert!(Journal::decode(&bytes).is_err());
    assert!(Header::decode(&journal(1, 0).encode().unwrap()).is_err());
    assert!(Header::decode(&bytes[..191]).is_err());
    let mut longer = bytes.clone(); longer.push(0);
    assert!(Header::decode(&longer).is_err());
    for offset in [0, 8, 44, 76, 108] {
        let mut changed = bytes.clone(); changed[offset] ^= 1;
        assert!(Header::decode(&changed).is_err());
    }
    assert!(original.bind_image([8; 8]).is_err());
    let mut wrong = original.clone(); wrong.aggregate_image = header::relation_image();
    assert!(wrong.validate().is_err());
    wrong.aggregate_image = [0; 8]; assert!(wrong.validate().is_err());
    wrong = original.clone(); wrong.member_count = 0; assert!(wrong.validate().is_err());
    wrong.member_count = 49; assert!(wrong.validate().is_err());
    wrong = original; wrong.seal_height = 0; assert!(wrong.validate().is_err());
}

#[test]
fn membership_all_small_sizes_odd_padding_and_tampering() {
    for count in [1, 2, 3, 5, 16, 31, 32, 33, 48] {
        let values = members(count);
        let root = header(&values);
        for (index, bytes) in values.iter().enumerate() {
            let path = membership::opening(&values, index as u32).unwrap();
            assert_eq!(membership::verify(&root, bytes, index as u32, &path).unwrap(), Journal::decode(bytes).unwrap());
            let mut changed = Journal::decode(bytes).unwrap(); changed.rank += 1;
            assert!(membership::verify(&root, &changed.encode().unwrap(), index as u32, &path).is_err());
            let mut extra = path.clone(); extra.push([0; 32]);
            assert!(membership::verify(&root, bytes, index as u32, &extra).is_err());
            if !path.is_empty() {
                let mut altered = path.clone(); altered[0][0] ^= 1;
                assert!(membership::verify(&root, bytes, index as u32, &altered).is_err());
                assert!(membership::verify(&root, bytes, index as u32, &path[..path.len() - 1]).is_err());
            }
        }
        assert!(membership::verify(&root, &values[0], count as u32, &[]).is_err());
    }
    let values = members(3); let root = header(&values);
    let mut path = membership::opening(&values, 2).unwrap(); path[0][0] ^= 1;
    assert!(membership::verify(&root, &values[2], 2, &path).unwrap_err().contains("odd padding"));
    let mut wrong_count = root.clone(); wrong_count.member_count = 4;
    assert!(membership::verify(&wrong_count, &values[0], 0, &membership::opening(&values, 0).unwrap()).is_err());
    let mut duplicate = values.clone(); duplicate.insert(1, duplicate[0].clone());
    assert!(membership::commitment(&duplicate).is_err());
    let mut unsorted = values; unsorted.reverse(); assert!(membership::commitment(&unsorted).is_err());
    assert!(membership::commitment(&[]).is_err());
    assert!(membership::commitment(&members(49)).is_err());
}

#[test]
fn framing_refuses_size_before_payload_read_and_exact_eof() {
    let bytes = u32::MAX.to_le_bytes();
    let mut reader = wire::Reader::new(std::io::Cursor::new(bytes));
    assert!(reader.frame().unwrap_err().contains("wire byte budget"));
    let mut reader = wire::Reader::new(std::io::Cursor::new(0u32.to_le_bytes()));
    assert!(reader.frame().unwrap_err().contains("nonempty"));
    let mut reader = wire::Reader::new(std::io::Cursor::new(2u32.to_le_bytes()));
    assert!(reader.frame().unwrap_err().contains("truncated delta"));
    let mut reader = wire::Reader::new(std::io::Cursor::new([9]));
    assert!(reader.end().unwrap_err().contains("exact EOF"));
    let mut reader = wire::Reader::new(std::io::Cursor::new([]));
    assert_eq!(reader.end().unwrap(), 0);
}

#[test]
fn metadata_refuses_duplicate_unused_and_wrong_claims() {
    let bytes = journal(1, 0).encode().unwrap();
    let mut input = prefix(2, 2, 1, 1); legacy(&mut input, &bytes); legacy(&mut input, &bytes);
    assert!(relation::check_bytes(&input).unwrap_err().contains("duplicate aggregate assumption"));
    let mut input = prefix(1, 0, 1, 1); legacy(&mut input, &bytes);
    assert!(relation::check_bytes(&input).unwrap_err().contains("unused aggregate assumption"));
    let mut input = prefix(1, 2, 1, 1); legacy(&mut input, &bytes);
    frontier(&mut input, 0, &bytes); frontier(&mut input, 0, &bytes);
    assert!(relation::check_bytes(&input).unwrap_err().contains("duplicate/conflicting"));
    let mut input = prefix(1, 1, 1, 1); legacy(&mut input, &bytes);
    frontier(&mut input, 0, &journal(2, 0).encode().unwrap());
    assert!(relation::check_bytes(&input).unwrap_err().contains("legacy frontier exact"));
    let mut input = prefix(1, 1, 1, 1); input.push(2);
    assert!(relation::check_bytes(&input).unwrap_err().contains("unknown aggregate assumption tag"));
    let mut input = prefix(0, 1, 1, 1); input.extend_from_slice(&0u32.to_le_bytes());
    assert!(relation::check_bytes(&input).unwrap_err().contains("frontier assumption index"));
    assert!(relation::check_bytes(&prefix(9, 0, 1, 1)).is_err());
    assert!(relation::check_bytes(&prefix(0, 0, 0, 0)).is_err());
    let mut input = prefix(0, 0, 2, 2);
    input.extend_from_slice(&[9; 32]); input.extend_from_slice(&[9; 32]);
    assert!(relation::check_bytes(&input).unwrap_err().contains("duplicate input target"));
}

#[test]
fn aggregate_parent_actual_image_and_height() {
    let mut parent = header(&members(2)); parent.aggregate_image = [8; 8];
    let mut input = prefix(1, 0, 1, 1); input.push(1); input.extend_from_slice(&parent.encode().unwrap());
    assert!(relation::check_bytes(&input).unwrap_err().contains("actual image binding"));
    parent.aggregate_image = [7; 8]; parent.seal_height = u64::MAX;
    let mut input = prefix(1, 0, 1, 1); input.push(1); input.extend_from_slice(&parent.encode().unwrap());
    assert!(relation::check_bytes(&input).unwrap_err().contains("seal height overflow"));
}

#[test]
fn census_global_sums_named_and_positional_and_strict_json() {
    let value = json!({"schema":"shape-only", "image":[0,0,0,0,0,0,0,0], "rank":0, "local_spec":{},
        "rows":[0,1], "parents":[{"journal":[], "openings":[{},{}]}], "bodies":[{}]});
    let bytes = serde_json::to_vec(&value).unwrap();
    let mut census = Census::default(); census.charge(&bytes).unwrap(); census.charge(&bytes).unwrap();
    assert_eq!((census.rows, census.openings, census.bodies), (4, 4, 2));
    let positional = json!(["shape-only", [0,0,0,0,0,0,0,0], 0, {}, [0,1], [[[],[{},{}]]], [{}]]);
    let mut other = Census::default(); other.charge(&serde_json::to_vec(&positional).unwrap()).unwrap();
    assert_eq!((other.rows, other.openings, other.bodies), (2, 2, 1));
    census.rows = crate::census::MAX_ROWS;
    assert!(census.charge(&bytes).unwrap_err().contains("row budget"));
    let mut census = Census::default(); census.nodes = crate::census::MAX_NODES;
    assert!(census.charge(&bytes).unwrap_err().contains("node budget"));
    let mut census = Census::default(); census.nodes = usize::MAX;
    assert!(census.charge(&bytes).unwrap_err().contains("overflow"));
    assert!(Census::default().charge(br#"{"rows":[],"rows":[]}"#).is_err());
    assert!(Census::default().charge(br#"[1.5]"#).is_err());
}
