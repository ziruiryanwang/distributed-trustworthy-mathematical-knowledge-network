//! Distinct RC scheme; length caps are checked before allocating each frame.
use dmkn_module_relation::canonical::{require, R};
use std::io::Read;

pub const MAGIC: &[u8; 8] = b"DMKNRC01";
pub const VERSION: u32 = 1;
pub const MAX_BYTES: usize = 16 * 1024 * 1024;

pub(crate) struct Reader<T> { input: T, bytes: usize }

impl<T: Read> Reader<T> {
    pub(crate) fn new(input: T) -> Self { Self { input, bytes: 0 } }
    fn reserve(&mut self, count: usize) -> R<()> {
        self.bytes = self.bytes.checked_add(count).ok_or("RC wire byte overflow")?;
        require(self.bytes <= MAX_BYTES, "RC aggregate wire byte budget")
    }
    pub(crate) fn fixed<const N: usize>(&mut self) -> R<[u8; N]> {
        self.reserve(N)?;
        let mut out = [0; N];
        self.input.read_exact(&mut out).map_err(|e| format!("RC aggregate truncated field: {e}"))?;
        Ok(out)
    }
    pub(crate) fn u32(&mut self) -> R<u32> { Ok(u32::from_le_bytes(self.fixed()?)) }
    pub(crate) fn frame(&mut self) -> R<Vec<u8>> {
        let length = self.u32()? as usize;
        require(length > 0 && length <= crate::census::MAX_FRAME_BYTES, "RC frame length bound")?;
        self.reserve(length)?;
        let mut bytes = vec![0; length];
        self.input.read_exact(&mut bytes).map_err(|e| format!("RC aggregate truncated delta: {e}"))?;
        Ok(bytes)
    }
    pub(crate) fn end(&mut self) -> R<usize> {
        let mut extra = [0];
        require(self.input.read(&mut extra).map_err(|e| e.to_string())? == 0,
            "RC aggregate exact EOF")?;
        Ok(self.bytes)
    }
}
