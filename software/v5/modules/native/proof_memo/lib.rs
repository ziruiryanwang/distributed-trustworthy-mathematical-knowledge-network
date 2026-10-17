//! Thin checker successor: unchanged native kernel and public module layout,
//! with successful per-proof syntax-DAG summaries; native kernel unchanged.
#![allow(clippy::too_many_arguments)]
#![deny(clippy::cast_possible_truncation)]

#[path = "../checker/src/debug_printer.rs"]
pub mod debug_printer;
#[path = "../checker/src/demand.rs"]
pub mod demand;
#[path = "../checker/src/env.rs"]
pub mod env;
#[path = "../checker/src/expr.rs"]
pub mod expr;
#[path = "../checker/src/inductive.rs"]
pub mod inductive;
#[path = "../checker/src/level.rs"]
pub mod level;
#[path = "../checker/src/module.rs"]
pub mod module;
pub mod module_correspondence;
#[path = "../checker/src/name.rs"]
pub mod name;
#[path = "../checker/src/parser.rs"]
pub mod parser;
#[path = "../checker/src/pretty_printer.rs"]
pub mod pretty_printer;
#[path = "../checker/src/quot.rs"]
pub mod quot;
#[path = "../checker/src/tc.rs"]
pub mod tc;
#[cfg(test)]
#[path = "../checker/src/tests.rs"]
mod tests;
#[path = "../checker/src/unique_hasher.rs"]
pub mod unique_hasher;
#[path = "../checker/src/util.rs"]
pub mod util;

pub(crate) const STACK_SIZE: usize = 16_777_216;
