//! Test wiring only: link the already compiled production relation, and test
//! the exact same census source without including its unrelated graph tests.
pub use dmkn_aggregate_relation::relation;
mod census;
pub use census::Census;
mod controls;
