# V5 module receipt relation

This directory is the new, separate certificate relation for immutable mathematical
modules. It is not a switch that makes v4 receipts certify v5 declarations. Source
review and native diagnostics do not establish cryptographic admission.

## Bound statement and trust boundary

`relation::check` authenticates the exact adopted 413-row foundation, recomputes
the semantic policy and local ModuleID, verifies selected parent-group openings,
recomputes body commitments, independently matches those descriptors to the SAME
native rows, derives imported/new roles, and checks every new local declaration.
There are no caller-supplied role bits or trusted `verified` booleans.

The guest in `src/main.rs` additionally calls genuine `env::verify` on EVERY
exact parent `(image, journal)` before committing its own new journal. The host
must supply real parent receipt witnesses and discharge all assumptions. The
native adapter deliberately does not do this: every output says
`mathematical_admission:false`. Conditional parent statements are not receipts.

The final receiving gate must reject Fake/dev receipts, verify the complete
receipt against an independently adopted actual image with dev mode disabled,
require `journal.image` to equal that image, and check exact foundation, policy
and expected ModuleID. Integrity-only verification is insufficient. This gate
also closes the guest's necessarily external self-image choice. No such public
receiving gate or new guest image is qualified merely by the source in this
directory.

The current profile pins the narrow zero-axiom foundation adopted in D06, not
all Lean/Mathlib. The semantic-policy hash excludes verification-performed
status and image identity; implementation adoption/migration is a separate
acceptance policy. New-policy modules must be reconstructed with new IDs, never
relabel old conditional-policy IDs.

## Diagnostic API

`receipt_native ACTION [INPUT]` uses the same five relation modules as the guest.
Inputs are strict JSON; duplicate keys, negative/floating numbers, oversized
input, and parser-depth overflow refuse. The selected parser retains its default
128-level recursion ceiling, narrower than the pure codec's 192-depth envelope.
Exit 0 means the exact diagnostic status below, NOT mathematical admission.
Exit 2 means `REFUSED`; checker panics and unresolved demands refuse.

| Action | Input | Exact success status |
|---|---|---|
| `profile` | None | `PROFILE_DESCRIPTION_ONLY` |
| `hash` | Array of exact `{domain,value}` objects | `HASHES_COMPUTED` |
| `journal` | 184 bytes as integer array | `JOURNAL_STRUCTURE_ONLY` |
| `openings` | Exact `{journal,openings}` | `OPENING_HASH_BINDINGS_ONLY` |
| `check` | Exact relation input below | `BOUND_RELATION_NATIVE_ONLY_PENDING_PARENT_PROOF_VERIFICATION` |

The relation input schema is:

```text
{
  schema: "DMKN_CERTIFIED_MODULES_V2",
  image: [eight u32 words], rank: u64,
  local_spec: codec ModuleSpec,
  rows: exact native row array, including the fixed foundation prefix,
  parents: [{journal: [184 bytes], openings: [selected codec group openings]}],
  bodies: [{universes: integer, digest: lowercase64hex, expression: codec AST}]
}
```

The wrapper derives all role and parent bindings from these data. `rank` is
exactly zero with no parents, otherwise one plus their maximum rank. Imported
theorem proof bodies are absent. Local theorem proof terms remain in native
rows; do not list them as unused committed definition/rule body openings.
`witness.make_input` is an untrusted producer helper, not a verification gate.

## Existential journal, fixed 184-byte layout

| Bytes | Field |
|---|---|
| 0..8 | `DMKNM002` |
| 8..12 | profile 2, u32 little-endian |
| 12..44 | eight image u32 words, little-endian |
| 44..76 | foundation ID |
| 76..108 | semantic-policy ID |
| 108..140 | ModuleID |
| 140..172 | group Merkle root |
| 172..176 | group count, u32 little-endian |
| 176..184 | rank, u64 little-endian |

Profile2 attests existence of a checked witness for the committed module, not
that an arbitrary supplied proof/input was the one checked. Distinct valid
theorem proofs may yield the same journal. Computational definition bodies,
types, parent group openings, rank and exact recursive verification remain
bound and checked. The removed whole-input digest was execution provenance,
not mathematical identity. All raw/canonical byte, node, depth and numeric
limits survive through strict parsing plus an exact nonserializing size walk.
Profile1 journals and receipts refuse; never relabel their bytes as profile2.

ModuleID recomputes from the codec summary. Canonical hash framing is
`DMKN-V5-MODULE\0 || u32be(domain length) || domain || u64be(payload length) ||
canonical JSON`, with SHA-256. Merkle odd-width duplicate padding is checked,
not merely ignored. Opening authentication proves membership in the selected
conclusion; only genuine receipt verification makes that conclusion authoritative.

## Disjoint focused controls

The used `native_controls.py` campaign is frozen profile1 evidence, not a
profile2 runtime test. The new `tests/existential_differential.rs` covers the
changed journal/parser boundary; synthetic projections of old journals are
explicitly native diagnostic fixtures, never migrated receipts.

Root owns `workloads/PrepareReceiptWorkload.py`, reconstructing the retained
actual Lean owner workload with this semantic policy and making native wrapper
requests. Assurance owns independent `tests/test_receipt_boundary.py` against
the newly constructed fusion request; do not duplicate its full-relation vectors.
All selected runs snapshot exact sources and fresh outputs. No script here
launches itself, renews an old campaign or authorizes a guest/proof build.

See [native build plan](NATIVE-BUILD-PLAN.md) for retained compiler inputs.

## New host source (not yet compiled or qualified)

`src/bin/module_host.rs` is the root-selected real-receipt/staged-prover adapter,
with the shared journal/policy source and no native checker linked into receiving.
Its direct retained-rllib build uses the HOST serde/serde_json versions from
`experiments/certified-collection-01/host-build-01/LINK-INPUTS.json`, alongside
that record's anyhow/bincode/risc0_zkvm. Do not substitute the native diagnostic's
different serde crate instances across SDK Receipt/Segment serialization.

```text
prepare IMAGE RAW_JSON FRESH_FRAME FRESH_EXPECTED_JOURNAL
execute IMAGE INPUT EXPECTED_JOURNAL CYCLES PO2 [REAL_FINAL_PARENTS...]
stage IMAGE INPUT EXPECTED_JOURNAL CYCLES PO2 KIND INDEX FRESH_OUTPUT
      PARENT_COUNT [REAL_FINAL_PARENTS...] [CAPSULE CHECKPOINTS...]
verify ADOPTED_IMAGE_ID RECEIPT EXPECTED_JOURNAL
receive ADOPTED_IMAGE_ID RECEIPT EXPECTED_MODULE_ID
```

`prepare` derives the actual image words but never rewrites parent journals; its
outputs are untrusted data, not checked modules. `snapshot` is one stage kind
which actually executes once and records a coherent capsule(schema3). Subsequent
segment/lift/join/resolve/finish stages use that capsule without guest reruns;
all checkpoints(schema5) bind its exact hash. Session/snapshot domains are V2.
Exact host input/image/expected-journal/limits/parent-receipt pins remain local
engineering protections; they do not restore transferable proof provenance.
Fake/missing/unresolved/wrong-profile
receipts cannot pass final full verification. `receive` has no source/witness/
ancestral-proof input. A public controller must supply its locally adopted
image and expected ModuleID, not a peer's suggested verifier profile.

See [crypto integration](CRYPTO-INTEGRATION.md) for the soundness/cost reasoning
and [guest build selection](GUEST-BUILD-PLAN.md) for the finite offline adapter.
Those sources/commands remain prospective until root-selected actual runs and
independent review. No certificate or image adoption is implied by these files.
