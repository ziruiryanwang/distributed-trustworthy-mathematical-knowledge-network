# Independent review: heterogeneous discovery profiles

2026-10-20, adaptive_audit. Source/theory review only. No product edit,
runtime, build, network call, proof production or Git mutation.

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Reviewed proposal: `PROFILE-INTEROPERABILITY-SEAM.md`, SHA-256
`6d931c9665421116843f9b21149d2659d1dad7aeb062938e264e2e543a21a919`.
Current source selection: `experiments/v5-local-checks/distribution-adaptive-01-input.json`,
SHA-256 `a74eaf51a71b5e0ec49a762fd5c7e6cce4f8fc6b107e97ae6e71fd7ec0cf1e32`.

## Decision

**Support the narrow base-index projection seam, not a new federation protocol.**
The proposal identifies a real capability gap: independent consumers using the
common base profile cannot discover a publication present only in an arbitrary
specialist-profile index. This is intentional isolation, not a verification bug.
Explicit matching configuration is sufficient for today's configured deployments,
but does not provide the heterogeneous discovery intended for the commons.

The smallest justified remedy is an explicitly bounded projection of selected
held exports into an ordinary base index, followed by serving that selected index
with the existing original custody objects. Preserve all namespace checks.
Do not build a catalogue, multi-profile consumer or multi-namespace server merely
to establish this compatibility path.

This is source approval of a design seam, not approval of an implementation or
runtime allocation. No current installed capability changes by this review.

## Independently checked boundary

1. `type_pattern/discovery/module_export_adapter.py:104-128` includes the entire
   selected profile in its namespace descriptor. `feature_id` includes that
   namespace even for ordinary atomic specs. The fingerprint successor preserves
   this construction. Equal atomic predicates across profiles therefore do not
   imply equal query keys or interchangeable index records.
2. `type_pattern/client/workspace_evidence.py:54-128` constructs exactly one adapter
   and index from an immutable config. The full selected pair/profile data is
   required at construction. Successive query generations do not change it.
3. `transport/http_provider_receipts.py:198-238` validates candidate namespaces
   and offers only when the requested namespace equals `self.index.namespace`.
   A known HTTP endpoint alone does not bypass profile separation.
4. `portable_runtime/location/protocol.py` commits namespace and features into
   the exact route. Its closed descriptor authenticates advisory endpoint binding,
   not complete profile parameters. Location and HTTP boundaries agree.
5. `type_pattern/discovery/discovery_store.py:188-259` binds snapshots, records
   and postings to the chosen namespace; `admit` recomputes features from actual
   export bytes. An existing specialist record cannot simply be relabeled base.
6. `iterative_queries/evidence_network/transport.py:19-28` accepts separate
   `index`, `custody` and `packets` arguments, requires actual custody types and
   checks foundation/policy compatibility. Neither a second mathematical store
   nor another certificate is required just to select a base index.
7. `client/serve_workspace.py:168-183` and `client/serve_advertised.py:272-310`
   currently hardwire `workspace.index`. The advertised namespace comes from
   that same index. This is the actual public composition seam to address.
8. `workspace_evidence.py:90-100` acquires the exclusive workspace owner lock.
   Two ordinary service processes cannot concurrently reopen that workspace.
   The proposal correctly uses one open workspace and one selected served view.

The existing `Store` is metadata-only: it stores extracted records, postings and
authenticated index nodes, not the raw opening or proof packet. Its projection
therefore duplicates index metadata/work, not the whole mathematical payload.
The original `ModuleStore.get_group` rechecks the exact module opening and name;
ordinary acquisition continues to retrieve that original opening from custody.

## Why the remedy is sound and what it does not prove

Fix a common foundation/policy and exact module export x. Let b(x) be its
canonical opening object, N0 the ordinary base namespace, and E0 the existing
base extraction algorithm. A successful target admission produces

`r0 = E0(b(x))`, with `r0.namespace = N0` and `r0.object_id = ExportID(x)`.

The source specialist index and its feature keys do not enter this derivation.
Consequently the base snapshot's search predicates are evaluated against the
same base extraction used for any ordinary base publication. The module ID,
export ID, interface opening and later proof-admission requirements stay fixed.
No profile-specific search hint becomes a mathematical warrant.

The conclusion is conditional: a retained projected record can be returned by
an adequately funded base query through a reachable, correctly advertised provider.
It does not establish global recall, usefulness, superior selectivity, continued
availability or mathematical acceptance. A common namespace is a compatibility
coordinate, not a centralized index or global trust authority. Distinct foundations
and semantic policies remain separate deliberately.

This remedy lets a base client find an unknown export without knowing its
specialist profile. It does not let that client exploit the specialist fingerprint
or pair index; that still requires explicit matching configuration. The base path
can be expensive on hot features. Keep richer-profile discovery as optional work,
not an implied consequence of projection.

## Required implementation boundaries

- Materialize only an explicit finite export selection; no whole-corpus scan,
  discovery-profile guessing or automatic every-profile copying. Use actual held
  openings and the target adapter's normal `admit`, never copied feature claims.
- Separate materialization from serving. A renewal reopens retained target state;
  it must not silently reindex new source publications or renew a failed budget.
- Hold the original workspace once. Open the separately bounded target metadata
  store under that owner's operation; pass the original module/packet stores to
  one provider. Keep the original workspace adapter/index immutable. Do not
  assign a base adapter over the specialist workspace's authenticated config.
- Bind the selected store, namespace, actual snapshot/cut and advertisement routes
  consistently. Report the selected view, not the source workspace namespace.
  An index built on disk but not served/advertised is not remote discoverability.
- Preserve bounded paths, retained config/limits, exception-safe closure and
  cleanup. A separate target store must be explicitly closed on every path;
  the old workspace closer knows only its original index, packets and modules.
- Treat every target admission as an individual transaction. Record committed
  prefixes, exact selection and uncertain failures; no cross-database atomicity
  or all-source coverage claim. If a commit outcome is uncertain, reconcile the
  actual target state before claiming completion. Existing idempotent admission
  supports deliberate retries but does not make previous work free.
- Charge raw reads, extraction, hashes, metadata, postings, failures, retained
  snapshots, serving and advertisements. Per-operation `Store.work` resets and
  successful-return counters alone cannot account for a failed batch; retain
  aggregate enclosing consumption and uncertainty. Actual store quotas and the
  finite outer envelope remain in force.
- Preserve independent mathematical verification. A structurally valid opening
  in an index is not a checked theorem. Missing packets or demanded semantic
  bodies are acquisition failures, not permission to trust the index operator.

## Catalogue alternative and next evidence

A closed-schema advisory catalogue could expose supported full profiles at an
already known endpoint. It would not make that endpoint discoverable through an
unadvertised base route, and today's client cannot mutate its immutable namespace.
It therefore does not by itself fix this gap. A future catalogue may be valuable
for selective specialist discovery, with a separately justified consumer/rendezvous
design and no remote feature-extraction code. It is not needed for this seam.

If root selects implementation, a small structural changed-boundary control is
enough: one exact held export, two genuine namespace-distinct indexes, wrong-profile
refusal, successful regenerated base candidate, unchanged opening/export identity,
and actual selected-index/provider/advertisement binding with shared original
custody. Include partial/quota refusal and cleanup because those are new ownership
boundaries. Do not produce a new theorem, duplicate an installed campaign or run
a scale experiment for this compatibility fact.

**Disposition:** GO for the bounded design direction under the above boundaries;
implementation, finite execution and adoption remain root's separate decisions.
