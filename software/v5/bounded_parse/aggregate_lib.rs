//! Exact-warrant aggregate with immutable bounded-parse tokens.
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

#[cfg(test)]
mod controls;
