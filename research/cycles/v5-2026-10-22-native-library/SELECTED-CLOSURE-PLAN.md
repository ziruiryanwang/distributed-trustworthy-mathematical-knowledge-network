# Ordinary selected-closure exporter and real fixed-basis bridge

2026-10-22, source-only selection. Root authorized a fresh
`software/v5/ordinary_lean/BootstrapSupport.lean` copy with narrowed imports,
preserving the original support's function bodies, plus `OrdinaryExport.lean`.
No runtime, builds, tests, Git changes or repeated method compilation selected.

## Reuse, not another graph implementation

Reuse the existing `BootstrapProbe.RecordSource`, `lookup`, `owner`,
`groupMembers`, `makeUnit`, original normalized `inventoryRow`, and `receiveSeed`.
The latter remains genuine empty-environment checked seed reconstruction.
Do not use its fixed-root `collect` or seed-specific `orderAndReport` for ordinary
closures. The new wrapper needs a finite selected-root work queue, dependency
scheduling, original-codec emission and a basis comparison, not another kernel.

The frozen source is `software/native/BootstrapSupport.lean`; its only deliberate
copy difference is replacing broad `import Lean` with the actual supporting API
imports (`Lean.Environment`, `Lean.Message`, `Lean.Data.Json.Parser`,
`Lean.Data.Json.FromToJson.Basic`, `Std.Data.HashSet.Basic`). Existing function
bodies, seed policy and codecs remain
unchanged. This fresh support copy does not revise or reinterpret any old product.
Compilation still needs root selection and may identify an omitted minimal API.

## Basis is actual checked mathematics, not the name `Init`

The root-selected profile pins both existing artifacts exactly:

- seed `a0acdc706f5e42dca21950c14db2307a18955c63ff953019aaff413d0a976001`;
- inventory `c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0`.

The protected controller checks byte identity before parsing/using these trusted
fixed files. `BootstrapProbe.receiveSeed` creates the 456 units/581 names from an
empty environment, performs actual kernel checks and output comparison, and
establishes quotient initialization. A later protected snapshot can amortize
that local bootstrap; no imported `Init` is substituted as its warrant.

On the producer side, compare each of those 581 native records with the exact
selected normalized inventory using `BootstrapProbe.inventoryRow`; definitions
use the selected inventory's known regular height as its explicit override.
This tests full normalized type/body/rule equality, not just name/version/type.
The normalization intentionally erases binder labels, universe-parameter names,
let nondep hints, mdata, and singleton block metadata, and chooses regular heights.
It does not claim exact ordinary metadata equality or authorize arbitrary basis
substitution. New extension descriptors retain their original metadata and hints.

Only this compared exact basis name set is excluded from the missing closure.
Literal builtin dependencies are already supplied by this basis. Named bindings
are `basis_symbol_id(profile,basis,name)`, not anonymous or globally trusted names.
Caller-provided seed/inventory JSON remains INTERNAL data requiring that exact
controller pin; the wrapper cannot authenticate a profile merely by receiving it.

## Producer export and cost

Import only the locally owner-authorized compiled source module at private level
with no dynamic plugins/extensions; the eventual driver uses a bounded explicit
artifact map. This is the producer's serialization input, never receiver trust.
Private-level source availability is required; opaque/erased/incomplete records
are explicit export refusals, not new axioms. Initial requested root is
`DMKN.ReadFootprint.readsOnly_insertMany`; its definition dependencies are found
from actual elaborated terms, not manually guessed Std imports.

Build the source inductive-owner/member index once per immutable imported source
environment. The implemented wrapper streams the source map with a finite census,
retains only group records, and presents those to the existing member-index API;
it does not first copy the full source constant map. This is a finite local
source-library pass, not a per-theorem scan and not
a network-wide index. Cache/reuse within that exporter session across requests.
Traverse only selected closure units via `owner` and `makeUnit`, with distinct
unit/node/reference limits. Generated inductive members remain one atomic unit.
No unit may straddle the basis boundary. Reject remaining axioms, Quot init,
unsafe/partial records or missing external dependencies.

Schedule dependencies using a finite Kahn ready queue and reverse edges, not
the old repeated full-remaining-list scan. Each selected unit is constructed
once; all dependency edges are charged. The new codec emits original descriptors
and complete actual source inventory. The Python evidence reader independently
computes exact direct references from these emitted bytes, assigns basis/earlier
export IDs and creates stable domain-separated envelopes in dependency order.
Neither producer order nor claims replace receiver checking.

Cost consists of one bounded local environment census/index, selected expressions
and generated inventories, and linear graph bookkeeping in selected units/edges
(plus deterministic per-unit ordering and output encoding). No claim of constant
cold onboarding or efficient export of all mathematics follows.

## Output and next integration

Return ordinary units in topological order plus original target names; bound
aggregate unit bytes as well as each unit. Do not attach a `verified` field.
The surrounding controller canonicalizes and hashes exact inert envelopes,
matches every import to a warranted basis/previous export identity, and acquires
only the needed missing closure. The receiver decodes/checks units and compares
the actual generated outputs before local persistence or owner-project rebind.

The fresh support's `BootstrapProbe.receiveSeed` remains public to the internal
basis initializer; a separately selected protected basis-snapshot writer may
consume its actual returned environment only through a pinned controller path.
No such writer is supplied by the exporter. No API accepts a
peer `.olean` or equates successful source export with acceptance. Root owns the
later protected profile/controller and actual finite export/admission selection.

## Source implementation completed, not executed

`OrdinaryExport.indexSource` builds the reusable bounded local grouping index.
`compareSourceBasis` checks the caller-pinned normalized basis correspondence.
`selected` uses the existing owner/makeUnit routines, finite queue, deduplicated
edges and Kahn scheduling, then `DeclCodec.encodeUnit` with ordered actual source
inventory. It returns ordinary inert units and accounting; no binary import,
disk/network I/O or mathematical admission is implemented in this wrapper.

Current trusted defaults: 262,144 source records, 65,536 group records, 8,192
selected units, 262,144 edges, 20,000,000 reported scan nodes, 8 MiB per emitted
unit and 64 MiB summed emitted unit JSON. They are finite refusal bounds, not
expected workload costs. The retained `makeUnit` has its own 20-million-node
per-unit scan limit; aggregate refusal occurs after that call. The outer process
CPU/memory/deadline bound is still necessary. Unit byte accounting is the Lean
JSON encoding; final canonical evidence/import-envelope byte bounds must also
be applied by the Python controller, without silently granting more budget.

Source-only textual comparison confirmed all copied support bytes from its first
body comment onward exactly match the frozen original; only import lines differ.
No compilation, tests, method reruns, proof or runtime was performed. The staged
driver path remains: owner-authorized private-level module import, `indexSource`,
`selected` for the chosen target, canonical envelope construction, separately
pinned empty-basis initialization and actual checked admission at the receiver.
