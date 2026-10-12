//! Conditional aggregate relation, not native mathematical admission.
//! Only the guest wrapper discharges genuine exact SDK assumptions. A receiver
//! additionally pins the actual aggregate image and verifies the real receipt.
pub mod header;
pub mod membership;
pub mod relation;
mod census;
mod wire;
pub use census::Census;

#[cfg(test)]
mod tests;
