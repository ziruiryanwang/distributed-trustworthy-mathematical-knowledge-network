//! Host-side exact I/A boundary verification. Not linked into the guest library.
//! No receipt-shaped status, membership proof or conditional native result can
//! construct this value. Consumers must separately own lifetime/profile policy.
use anyhow::{ensure, Result};
use bincode::Options;
use dmkn_aggregate_relation::{header::{self, Header}, relation::PendingAssumption};
use dmkn_module_relation::{canonical, journal::Journal};
use risc0_zkvm::{InnerReceipt, Receipt, VerifierContext, sha::Digest};

pub const MAX_RECEIPT_BYTES: usize = 64 * 1024 * 1024;

pub enum Statement {
    Legacy(Journal),
    Aggregate(Header),
}

/// Live trusted-process result, not a persistable acceptance credential.
pub struct VerifiedReceipt {
    receipt: Receipt,
    statement: Statement,
    image: [u32; 8],
}
impl VerifiedReceipt {
    pub fn receipt(&self) -> &Receipt { &self.receipt }
    pub fn statement(&self) -> &Statement { &self.statement }
    pub fn image(&self) -> [u32; 8] { self.image }
}

fn checked<T>(value: canonical::R<T>) -> Result<T> {
    value.map_err(anyhow::Error::msg)
}

fn verify(raw: &[u8], image: [u32; 8]) -> Result<Receipt> {
    ensure!(std::env::var_os("RISC0_DEV_MODE").is_none(), "dev-mode environment forbidden");
    ensure!(!raw.is_empty() && raw.len() <= MAX_RECEIPT_BYTES, "exact bounded receipt bytes");
    let receipt: Receipt = bincode::DefaultOptions::new().with_fixint_encoding()
        .with_limit(MAX_RECEIPT_BYTES as u64).reject_trailing_bytes().deserialize(raw)?;
    match &receipt.inner {
        InnerReceipt::Succinct(inner) => ensure!(inner.hashfn == "poseidon2", "unsupported hash suite"),
        _ => anyhow::bail!("only genuine succinct Poseidon2 receipts are supported"),
    }
    // Full application verification requires successful execution under THIS
    // image and resolved assumptions. Integrity-only verification is not enough.
    let context = VerifierContext::default().with_dev_mode(false);
    receipt.verify_with_context(&context, Digest::from(image))?;
    Ok(receipt)
}

/// Verify one boundary claim returned by the actual aggregate relation.
/// adopted_a is an independently selected image, never inferred from the receipt.
pub fn verify_pending(raw: &[u8], pending: &PendingAssumption,
                      adopted_a: [u32; 8]) -> Result<VerifiedReceipt> {
    checked(header::distinct_aggregate_image(adopted_a))?;
    let image = pending.image();
    let statement = if image == header::relation_image() {
        Statement::Legacy(checked(header::member_journal(pending.journal()))?)
    } else {
        ensure!(image == adopted_a, "pending claim outside adopted I/A profile");
        let header = checked(Header::decode(pending.journal()))?;
        checked(header.bind_image(adopted_a))?;
        Statement::Aggregate(header)
    };
    let receipt = verify(raw, image)?;
    ensure!(receipt.journal.bytes == pending.journal(), "exact pending receipt journal");
    Ok(VerifiedReceipt { receipt, statement, image })
}

/// Verify a final aggregate receipt against the exact independently selected
/// header. Member bindings are separate and may be checked after this call.
pub fn verify_aggregate(raw: &[u8], expected_header: &[u8],
                        adopted_a: [u32; 8]) -> Result<VerifiedReceipt> {
    let header = checked(Header::decode(expected_header))?;
    checked(header.bind_image(adopted_a))?;
    let receipt = verify(raw, adopted_a)?;
    ensure!(receipt.journal.bytes == expected_header, "exact aggregate receipt journal");
    Ok(VerifiedReceipt { receipt, statement: Statement::Aggregate(header), image: adopted_a })
}
