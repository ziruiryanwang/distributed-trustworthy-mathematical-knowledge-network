//! Restricted proof composition preserving the original conditional I statement.
//! This crate returns obligations, never receipt authority. The aggregate guest
//! must establish every returned parent journal before committing its conclusion.
pub mod relation;
pub mod syntax;
#[path = "foundation02.rs"]
pub(crate) mod foundation;
pub(crate) mod typing;
