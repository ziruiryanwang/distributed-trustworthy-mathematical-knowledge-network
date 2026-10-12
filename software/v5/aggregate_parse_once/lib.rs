//! Parse-once successor of the frozen conditional aggregate relation.
//! It changes representation work only, not mathematical or receipt authority.
//! Unchanged support sources are path-reused and must be pinned by every build.
#[path = "../aggregate/header.rs"]
pub mod header;
#[path = "../aggregate/membership.rs"]
pub mod membership;
pub mod relation;
mod census;
#[path = "../aggregate/wire.rs"]
mod wire;
pub use census::Census;

#[cfg(test)]
#[path = "../aggregate/tests.rs"]
mod tests;
#[cfg(test)]
#[path = "../aggregate/census.rs"]
mod reference_census;
#[cfg(test)]
mod parse_once_controls;
