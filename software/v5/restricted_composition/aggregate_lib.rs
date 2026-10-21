//! Restricted-composition aggregate. No receipt authority without real guest
//! verification of every pending exact claim under this aggregate's own image.
#[path = "../aggregate_claims/header.rs"]
pub mod header;
#[path = "../aggregate_claims/membership.rs"]
pub mod membership;
#[path = "aggregate_relation.rs"]
pub mod relation;
mod census;
mod wire;
pub use census::Census;
