# Grounded cuts: first source implementation

2026-10-24. Root selects SOURCE ONLY after reading the grounded-cut contract,
its independent safety review, the retained theory trace and the independent
CUT-INVESTMENT-CHALLENGE. No new runtime, migration, package or acceptance event
is selected. Existing sources/evidence remain frozen. Full deployable v5 remains
ACTIVE; this is not a replacement goal consisting of a checker experiment.

## User benefit and investment boundary

Support sequential, independently timed contributions to a meaningful theory
without restoring all old proof history on each local admission. Ordinary Lean
projects remain the route for inventing definitions, structures and theories.
The optional first accelerator checks ONE new theorem over grounded earlier work.
It does not create concepts automatically or solve cold trust or semantic search.

Current native restore authenticates/deserializes old snapshots; it does not
re-kernel-check all old proofs. Compare against that actual route, batching and
small eligible roots. Rechecking concrete semantics, initial summary derivation,
index maintenance, export, failed checks and custody all remain real costs.

The first source slice has three separable boundaries: a conditional kernel
primitive, a persistent exact-name index, and their protected event controller.
The first two alone MUST NOT produce accepted local warrants. Before selecting
native execution root must review the complete authority/recursive-use path and
show no hidden whole-history scan per event. No worker-only PASS is a release.

## Conditional native primitive

New GroundedCut.lean starts from BootstrapProbe.receiveSeed on controller-bound
EXACT fixed seed/inventory, never an arbitrary owner Environment or native module.
Use the existing codecs and real addDeclCore/doCheck boundary. Return an internal
conditional result; do not save an olean, catalog record or public warrant.

The first supported packet contains topologically ordered concrete units,
topologically ordered old theorem signatures, and exactly one full new theorem
unit. All concrete units are checked as one bounded batch before signatures;
concrete semantics depending on omitted nonbasis theorem proofs are unsupported
in this first slice. Refuse such cases rather than falling back to a large parent.
This restriction fits the retained theory trace and avoids repeated per-group
stage-two censuses. Later broadening requires a fresh demonstrated need.

Signature rows use the existing OwnerRebind row shape:
`[encodedName,0,exactSymbolId,[universeParameters,typeDAG]]`.
Check canonical type encoding, exact names, universe parameters, safe axiom-shaped
construction and Prop type. The controller, NOT this shape, supplies the earlier
local warrant. All concrete declarations retain complete generated inventories;
no theorem, arbitrary axiom, partial declaration or unsafe definition enters the
concrete batch. New output must be exactly one genuine theorem with Prop type,
matching exact complete inventory and no name collision in the scratch context.
Global root freshness is a separate controller obligation.

Before/after exhaustive bounded scratch inventories must consist precisely of
the fixed foundation, checked concrete inventories, selected theorem signatures
and the single new theorem. Every nonfoundation axiom is on that signature list.
Limits bound packet bytes, groups, names, DAG/scanning nodes and kernel work.
Reusing a generic authoring helper that retains arbitrary owner axioms is forbidden.

Expose a small documented Lean function over seed/inventory JSON, concrete-unit
array, signature-row array and the new-unit JSON. No CLI/schema/launcher yet;
root will integrate only after the complete source path passes review.

## Indexed protected state

New cut_map.py is a storage primitive, NOT an acceptance authority. Use an
immutable content-addressed compressed binary trie keyed by SHA-256 of exact
canonical encoded-name bytes, retaining the full key at each leaf. Preserve
path-local positive/negative lookup and path-copy insertion; no full map copy or
history traversal. Hash collision/inconsistent exact key is an explicit refusal.

Store nodes in a caller-owned SQLite transaction with exact primary-key lookup.
Validate canonical node bytes and child hashes along each visited path. Keep
bounded node/key/value sizes and an explicit finite operation allowance. Charge
reads and writes. Reopening a selected root needs no ancestor enumeration; root
eligibility remains the controller's responsibility. A transactional insertion
must not commit the caller's transaction itself. Do not add a general database,
network protocol, daemon, certificate or global registry.

## Protected controller: required before execution/adoption

The controller will have a distinct grounded-cut origin/implementation contract,
not the existing native-check identity. One eligible native-bootstrap lineage
and conservative support epoch only. Initial derivation holds the native owner
lock, validates the chosen root once, binds original accepted V2 units and derives
their exact compact theorem/concrete summaries. Imported short summaries are not
warrants. Initial full cost is paid and recorded, not hidden as free setup.

For each extension: bind the live root/epoch/request; resolve exact demanded
summaries and whole-root name absence through the trie; build the supported
semantic closure; invoke the pinned worker under existing one-shot supervision;
bind its clean completion and exact result; recheck live authority; atomically
insert the result summary, event and new map root. An uncommitted prefix cannot
be reused. Close/reopen must allow later reuse through indexed committed summaries,
without importing scratch snapshots or walking ancestor events. Epoch withdrawal
invalidates affected results; an epoch rename cannot rehabilitate them.

Keep full NEW proof claims for ordinary inert publication. Missing export custody
is not identical to withdrawn checking support. No automatic retries, rollback,
lock removal, support migration or growing allowance. Failed/uncertain events
retain diagnostics and cannot establish a warrant by report text alone.

Root owns this controller design/integration and selection. Security author owns
GroundedCut.lean and WORKER.md; scale author owns cut_map.py and MAP.md. Independent
reviewer owns REVIEW.md and focused source-only controls when selected. No agent
mutates shared Git. Stop before runtime if an authority gap, hidden history scan,
unsupported actual semantic closure or adverse full-cost comparison remains.
