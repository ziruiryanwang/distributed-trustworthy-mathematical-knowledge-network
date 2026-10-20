//! Test wiring only. Production crates are linked, not reimplemented here.
pub use dmkn_aggregate_relation::relation;
mod census;
pub use census::Census;
#[path = "../bounded_parse/census.rs"]
mod old_census;
mod controls;
