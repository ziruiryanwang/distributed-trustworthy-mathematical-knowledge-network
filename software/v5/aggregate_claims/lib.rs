//! V2 aggregate of exact warrant journals, not semantic ModuleID aliases.
//! Conditional conclusions gain authority only through the real guest receipt.
pub mod header;
pub mod membership;
pub mod relation;
#[path = "../aggregate_parse_once/census.rs"]
mod census;
mod wire;
pub use census::Census;

#[cfg(test)]
mod tests;
#[cfg(test)]
#[path = "../aggregate/census.rs"]
mod reference_census;
#[cfg(test)]
#[path = "../aggregate_parse_once/parse_once_controls.rs"]
mod parse_once_controls;
