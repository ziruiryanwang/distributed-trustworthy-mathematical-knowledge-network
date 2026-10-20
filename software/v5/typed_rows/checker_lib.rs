//! Typed syntax/correspondence adapter; original kernel/application unchanged.
#![allow(clippy::too_many_arguments)]
#![deny(clippy::cast_possible_truncation)]

#[path = "../modules/native/checker/src/debug_printer.rs"]
pub mod debug_printer;
#[path = "../modules/native/checker/src/demand.rs"]
pub mod demand;
#[path = "../modules/native/checker/src/env.rs"]
pub mod env;
#[path = "../modules/native/checker/src/expr.rs"]
pub mod expr;
#[path = "../modules/native/checker/src/inductive.rs"]
pub mod inductive;
#[path = "../modules/native/checker/src/level.rs"]
pub mod level;
#[path = "../modules/native/checker/src/module.rs"]
pub mod module;
#[path = "../modules/native/proof_memo/module_correspondence.rs"]
pub mod module_correspondence_legacy;
pub mod module_correspondence;
#[path = "rows.rs"]
pub mod typed_rows;
#[path = "../modules/native/checker/src/name.rs"]
pub mod name;
pub mod parser;
#[path = "../modules/native/checker/src/pretty_printer.rs"]
pub mod pretty_printer;
#[path = "../modules/native/checker/src/quot.rs"]
pub mod quot;
#[path = "../modules/native/checker/src/tc.rs"]
pub mod tc;
#[cfg(test)]
#[path = "../modules/native/checker/src/tests.rs"]
mod tests;
#[path = "../modules/native/checker/src/unique_hasher.rs"]
pub mod unique_hasher;
#[path = "../modules/native/checker/src/util.rs"]
pub mod util;

pub(crate) const STACK_SIZE: usize = 16_777_216;
