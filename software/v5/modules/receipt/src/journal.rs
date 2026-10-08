//! New, fixed-size module conclusion. V4 journals cannot decode as this profile.

use crate::canonical::{hash, hex, require, R};
use serde_json::{json, Value};

pub const MAGIC: &[u8; 8] = b"DMKNM002";
pub const PROFILE: u32 = 2;
pub const BYTES: usize = 184;
pub const RELATION: &str = "DMKN_CERTIFIED_MODULES_V2";

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Journal {
    pub image: [u32; 8],
    pub foundation: [u8; 32],
    pub policy: [u8; 32],
    pub module: [u8; 32],
    pub group_root: [u8; 32],
    pub group_count: u32,
    pub rank: u64,
}

impl Journal {
    pub fn summary(&self) -> Value {
        json!({"schema":"DMKN_MODULE_SUMMARY_V1", "foundation":hex(&self.foundation),
            "policy":hex(&self.policy), "group_count":self.group_count, "group_root":hex(&self.group_root)})
    }

    pub fn validate(&self) -> R<()> {
        require(self.group_count > 0 && self.group_count <= 4096, "journal group count")?;
        require(hash("module-spec", &self.summary())? == self.module, "journal module identity")
    }

    pub fn encode(&self) -> R<Vec<u8>> {
        self.validate()?;
        let mut out = Vec::with_capacity(BYTES);
        out.extend_from_slice(MAGIC); out.extend_from_slice(&PROFILE.to_le_bytes());
        for word in self.image { out.extend_from_slice(&word.to_le_bytes()); }
        for digest in [self.foundation, self.policy, self.module, self.group_root] { out.extend_from_slice(&digest); }
        out.extend_from_slice(&self.group_count.to_le_bytes());
        out.extend_from_slice(&self.rank.to_le_bytes());
        assert_eq!(out.len(), BYTES);
        Ok(out)
    }

    pub fn decode(bytes: &[u8]) -> R<Self> {
        require(bytes.len() == BYTES && &bytes[..8] == MAGIC, "module journal size/magic")?;
        require(u32::from_le_bytes(bytes[8..12].try_into().unwrap()) == PROFILE, "module journal profile")?;
        let mut image = [0u32; 8];
        for (index, word) in image.iter_mut().enumerate() {
            *word = u32::from_le_bytes(bytes[12 + index * 4..16 + index * 4].try_into().unwrap());
        }
        let out = Self { image, foundation:bytes[44..76].try_into().unwrap(), policy:bytes[76..108].try_into().unwrap(),
            module:bytes[108..140].try_into().unwrap(), group_root:bytes[140..172].try_into().unwrap(),
            group_count:u32::from_le_bytes(bytes[172..176].try_into().unwrap()),
            rank:u64::from_le_bytes(bytes[176..184].try_into().unwrap()) };
        out.validate()?;
        Ok(out)
    }
}
