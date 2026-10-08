//! First adopted foundation and semantic policy. Image identity is deliberately
//! separate: changing a verifier does not itself rename mathematical modules.

use crate::canonical::{hash, hex, unhex, R};
use serde_json::{json, Value};

pub const FOUNDATION_ROWS: usize = 413;
pub const FOUNDATION_ID: &str = "d931d114155cf3cf0dc0b868aa88c6d38b8ada8ecafe267a5934934075782481";
pub const FOUNDATION_CANONICAL_SHA256: &str = "736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c";

/// Root adopted this exact 22-declaration, no-axiom foundation after independent
/// actual native audit. It does not claim all Lean/Mathlib foundation coverage.
pub fn foundation() -> [u8; 32] { unhex(FOUNDATION_ID).expect("compiled foundation identifier") }

pub fn semantic_descriptor() -> Value {
    json!({
        "schema":"DMKN_MODULE_SEMANTIC_POLICY_V1",
        "semantics_version":1,
        "foundation":hex(&foundation()),
        "module_spec":"DMKN_MODULE_SPEC_V1",
        "relative_reference_interpretation":"DMKN.Mod.<ModuleSpecID>.<structured-relative-name>",
        "universe_binders":"ordered-positional-alpha",
        "new_declarations":["definition","theorem","opaque","inductive","constructor","recursor"],
        "new_axioms":[],
        "new_quotient_primitives":false,
        "unsafe_or_partial_declarations":false,
        "local_visibility":"ordered-groups-with-atomic-inductive-self-visibility",
        "transparent_definition_identity":"type-kind-hint-and-value-commitment",
        "opaque_identity":"type-kind-and-value-commitment",
        "theorem_identity":"certified-Prop-type-not-proof-witness",
        "import_semantics":"immutable-exact-qualified-declarations",
        "missing_definition_body":"unresolved-demand-never-opacity-or-axiom",
        "inductive_import_unit":"complete-types-constructors-recursors-and-rules",
        "nat_extension":false,
        "string_extension":false
    })
}

pub fn semantic_id() -> R<[u8; 32]> { hash("semantic-policy", &semantic_descriptor()) }
