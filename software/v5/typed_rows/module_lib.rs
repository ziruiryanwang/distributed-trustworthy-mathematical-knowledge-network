//! Hybrid row representation with a separately compiled literal legacy path.
#[path = "../bounded_parse/canonical.rs"]
pub mod canonical;
pub mod decode;
#[path = "module_relation.rs"]
pub mod relation;
#[path = "../bounded_parse/module_relation.rs"]
pub mod legacy_relation;
#[path = "../modules/receipt/src/input.rs"]
mod input;
pub mod foundation_static;
#[path = "../modules/receipt/src/commitments.rs"]
pub mod commitments;
#[path = "../modules/receipt/src/journal.rs"]
pub mod journal;
#[path = "../modules/receipt/src/policy.rs"]
pub mod policy;
