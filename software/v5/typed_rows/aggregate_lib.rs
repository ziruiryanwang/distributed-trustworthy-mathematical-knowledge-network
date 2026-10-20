//! Same aggregate graph and commitments, one hybrid parse token per frame.
#[path = "../aggregate_claims/header.rs"]
pub mod header;
#[path = "../aggregate_claims/membership.rs"]
pub mod membership;
#[path = "aggregate_relation.rs"]
pub mod relation;
mod census;
#[path = "../aggregate_claims/wire.rs"]
mod wire;
pub use census::Census;
