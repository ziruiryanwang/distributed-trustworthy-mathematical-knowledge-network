//! Fail-closed access to missing immutable module witness data.
//!
//! Native preflight may catch ONLY this typed payload as a demand. The guest
//! has panic=abort and cannot turn an unresolved demand into a journal. Other
//! panics remain refusal. No network or mutable arena is accessed here.

use crate::util::{DagMarker, NamePtr};

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Demand {
    Declaration { export_name_index: usize },
    Body { export_name_index: usize, digest: [u8; 32] },
}

fn export_index(name: NamePtr<'_>) -> usize {
    // Temporary names synthesized by inductive checking are not remotely
    // addressable declarations. Their unexpected absence is a checker refusal.
    assert_eq!(name.dag_marker(), DagMarker::ExportFile,
               "MISSING_TEMPORARY_DECLARATION_NOT_FETCHABLE");
    name.idx()
}

pub(crate) fn declaration(name: NamePtr<'_>) -> ! {
    std::panic::panic_any(Demand::Declaration { export_name_index: export_index(name) })
}

pub(crate) fn body(name: NamePtr<'_>, digest: [u8; 32]) -> ! {
    std::panic::panic_any(Demand::Body { export_name_index: export_index(name), digest })
}
