//! Source successor: bounded strict parse, unchanged mathematical relation.
pub mod canonical;
#[path = "module_relation.rs"]
pub mod relation;
#[path = "../modules/receipt/src/input.rs"]
mod input;
#[path = "../modules/receipt/src/foundation_static.rs"]
pub mod foundation_static;
#[path = "../modules/receipt/src/commitments.rs"]
pub mod commitments;
#[path = "../modules/receipt/src/journal.rs"]
pub mod journal;
#[path = "../modules/receipt/src/policy.rs"]
pub mod policy;
