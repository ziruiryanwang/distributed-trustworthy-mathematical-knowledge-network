//! Fixed 192-byte aggregate claim; legacy 184-byte claims remain unchanged.
use dmkn_module_relation::{canonical::{require, unhex, R}, journal::Journal, policy};

pub const MAGIC: &[u8; 8] = b"DMKNA001";
pub const VERSION: u32 = 1;
pub const BYTES: usize = 192;
pub const MAX_MEMBERS: usize = 48;
pub const RELATION_IMAGE_HEX: &str =
    "9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e";

pub fn image_bytes(words: [u32; 8]) -> [u8; 32] {
    let mut out = [0; 32];
    for (index, word) in words.iter().enumerate() {
        out[index * 4..index * 4 + 4].copy_from_slice(&word.to_le_bytes());
    }
    out
}

pub fn image_words(bytes: [u8; 32]) -> [u32; 8] {
    std::array::from_fn(|i| u32::from_le_bytes(bytes[i * 4..i * 4 + 4].try_into().unwrap()))
}

pub fn relation_image() -> [u32; 8] {
    image_words(unhex(RELATION_IMAGE_HEX).expect("compiled relation image"))
}

pub fn distinct_aggregate_image(image: [u32; 8]) -> R<()> {
    require(image != [0; 8] && image != relation_image(), "distinct nonzero aggregate image")
}

/// Structural/profile validation only, NEVER a proof of theorem validity.
pub fn member_journal(bytes: &[u8]) -> R<Journal> {
    let journal = Journal::decode(bytes)?;
    require(journal.image == relation_image() && journal.foundation == policy::foundation()
        && journal.policy == policy::semantic_id()?, "member fixed relation profile")?;
    Ok(journal)
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Header {
    pub aggregate_image: [u32; 8],
    pub relation_image: [u32; 8],
    pub foundation: [u8; 32],
    pub policy: [u8; 32],
    pub members_root: [u8; 32],
    pub member_count: u32,
    pub maximum_member_rank: u64,
    pub seal_height: u64,
}

impl Header {
    pub fn validate(&self) -> R<()> {
        distinct_aggregate_image(self.aggregate_image)?;
        require(self.relation_image == relation_image()
            && self.foundation == policy::foundation() && self.policy == policy::semantic_id()?,
            "aggregate fixed relation profile")?;
        require(self.member_count > 0 && self.member_count as usize <= MAX_MEMBERS,
            "aggregate member count")?;
        require(self.seal_height > 0, "aggregate positive seal height")
    }

    /// Necessary after genuine receipt verification under an adopted image.
    /// This binding itself performs NO cryptographic receipt verification.
    pub fn bind_image(&self, actual_adopted_image: [u32; 8]) -> R<()> {
        self.validate()?;
        require(self.aggregate_image == actual_adopted_image, "aggregate actual image binding")
    }

    pub fn encode(&self) -> R<Vec<u8>> {
        self.validate()?;
        let mut bytes = Vec::with_capacity(BYTES);
        bytes.extend_from_slice(MAGIC);
        bytes.extend_from_slice(&VERSION.to_le_bytes());
        bytes.extend_from_slice(&image_bytes(self.aggregate_image));
        bytes.extend_from_slice(&image_bytes(self.relation_image));
        bytes.extend_from_slice(&self.foundation);
        bytes.extend_from_slice(&self.policy);
        bytes.extend_from_slice(&self.members_root);
        bytes.extend_from_slice(&self.member_count.to_le_bytes());
        bytes.extend_from_slice(&self.maximum_member_rank.to_le_bytes());
        bytes.extend_from_slice(&self.seal_height.to_le_bytes());
        require(bytes.len() == BYTES, "aggregate header encoding length")?;
        Ok(bytes)
    }

    pub fn decode(bytes: &[u8]) -> R<Self> {
        require(bytes.len() == BYTES, "aggregate header exact length")?;
        require(&bytes[..8] == MAGIC
            && u32::from_le_bytes(bytes[8..12].try_into().unwrap()) == VERSION,
            "aggregate header magic/version")?;
        let result = Self {
            aggregate_image: image_words(bytes[12..44].try_into().unwrap()),
            relation_image: image_words(bytes[44..76].try_into().unwrap()),
            foundation: bytes[76..108].try_into().unwrap(),
            policy: bytes[108..140].try_into().unwrap(),
            members_root: bytes[140..172].try_into().unwrap(),
            member_count: u32::from_le_bytes(bytes[172..176].try_into().unwrap()),
            maximum_member_rank: u64::from_le_bytes(bytes[176..184].try_into().unwrap()),
            seal_height: u64::from_le_bytes(bytes[184..192].try_into().unwrap()),
        };
        result.validate()?;
        Ok(result)
    }
}
