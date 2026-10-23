# Portable library-completion planner

2026-10-23, `project_hook_design`. Root-selected source-only implementation at
`software/v5/ordinary_library_package/library_completion.py`; no product import,
execution, tests, builds, Git operation or predecessor edit. Independent source
review is requested. This is a public-completion prerequisite, not a workflow pass.

Source SHA-256:
`b587c74e156c81a392f394b263b27b13de427753c41009ecc3b99193f88b93d9`.

## API and output

```python
complete_candidate(candidate_raw, supplement_raw, *,
    semantic_id, foundation_id, context_root, expected_targets,
    prepared_bindings, warranted_symbol,
    limits=portable_candidate.Limits(), check_budget=None)
```

The two inputs are immutable bytes. `prepared_bindings` is the authenticated
original candidate preparation; `warranted_symbol` is a stable point lookup in
the actual protected parent, never a peer map or a provisional extended parent.
`check_budget` shares the caller's nonrenewing allowance and may raise.

The frozen `CompletionPlan` returns `status="READY"`, exact dependency-ordered
portable `raw_units`, consumer/supplement target-name keys, original/supplement/
composite input hashes, per-lane canonical unit hashes, and selected byte/node/
name/lookup counts. `mathematical_acceptance` is always False. No catalog, file,
network, process, native checker or mutable parent is touched by this module.
Errors propagate without a partial READY result. `raw_units` is suitable for the
existing `owner.preflight` and, only after successful planning, `owner.admit`.

## Wrapper compatibility is not legacy identity translation

The supplement uses the existing `DMKN_ORDINARY_MISSING_IMPORT_BUNDLE_V1` field
layout with exact inert assurance. Its `profile_id` must already equal the
requested portable SemanticID, `basis_id` the portable FoundationID, and
`context_id` the selected parent root. This is explicitly an externally bound
inert encoding. Genuine legacy profile/basis/context/symbol identities are not
converted, promoted or accepted. The original candidate must be portable V2.
No new supplement schema or alternate authority was introduced.

## Construction and assurance argument

1. Call the existing `portable_candidate.bind_candidate` on the original bytes,
   original prepared map and actual parent. Require NEEDS_LOCAL_INTERPRETATIONS.
   This validates original claimed IDs, exact target ownership, complete raw-unit
   syntax and graph ordering before deciding the genuine missing set M.
2. Parse the supplement with the same bounded writer parser. Require its unique
   targets equal M, exact labels, complete nonempty unit array and exact structural
   statistics. Authenticate each declared supplemental boundary pair through the
   same protected lookup; refuse duplicate/conflicting boundary claims.
3. Inspect supplemental units with the existing unit inspector. Each unit may
   refer only to its own declared accepted boundary or earlier supplemental
   outputs, not the consumer's imports or future consumer outputs. Every new
   output is absent from K, distinct from consumer outputs and earlier outputs.
   Every member of M must actually be produced. No provisional ID enters K.
4. Construct an internal composite V2 wrapper: supplemental units followed by
   the exact original consumer unit values. Original claimed IDs are unchanged.
   Satisfied missing names cease to be external unresolved references; they are
   now earlier new-unit references. Accepted unresolved names may merge with an
   identical protected supplemental boundary claim, never a substitute ID.
5. Invoke the unchanged binder again against the REAL protected parent. Its
   controller-derived preparation map contains only original claims already
   authenticated against original P/K, plus separately K-authenticated boundary
   pairs. It contains no supplemental output or fabricated accepted symbol.
   Existing binder logic derives provisional portable IDs and exact envelopes,
   rejects forward/unbound references and enforces the complete combined graph.

The first binder prevents the consumer from acquiring undeclared references just
because a supplement happens to provide them. The supplemental lane-only check
likewise prevents its units from borrowing a protected name declared only by the
consumer. The second binder supplies one shared derivation/order/identity path,
not a second custom implementation of portable evidence binding.

Thus, conditional on the existing parsers/binder and protected lookup premises,
READY supplies one complete inert extension graph over the selected K. Actual
mathematical validity still requires the unchanged native checking and live
byte-bound commit. Imported success tokens and well-formed hashes are not proof.

## Aggregate limits and honest costs

One `Limits` object bounds combined raw input bytes, combined unit count, total
encoded nodes, output names, declared boundary rows and selected distinct names;
the composite also has the same byte ceiling, and the unchanged binder enforces
one combined evidence-byte ceiling. Parent lookup uses one memoized cache with
a finite `2*max_bindings` lookup cap; no parent/library enumeration is performed.
Budget checks run throughout, including after final diagnostic hash construction.
Reported source statistics are inert; only exact structural counts are checked.
Synthetic wrapper export-work counters are zero, not invented measurements.

This implementation deliberately repeats bounded work to reuse checked logic:
original candidate binding, parsing retained input, supplemental inspection,
composite binding, and diagnostic canonical hashes. Selected node/byte counters
are not CPU time or a claim that every node was visited only once. The integration
must charge actual controller/native work under its original allowance.

## Public integration and later extraction reuse

Root's proposed `completion_api.complete_source` can call this planner, then the
existing preflight/admit and custody/evidence/preview retention operations. It
must retain original bytes/hashes and authenticated preparation, select the exact
parent and target list, preserve accepted state on later reporting failure, and
never reauthor the already successful consumer merely to fill missing imports.
An explicit owner-selected inert supplement suffices; interactive extraction is
a separate operation and need not block this API or introduce a new interpreter.

For later extraction, existing `MissingImportExporter.run` already accepts exact
64-hex labels, a finite installed-Std module/target selection and one private
environment. Its synchronous parent-lookup frames remain inert lookup requests.
`run_missing_import_completion.exchange(argv, env, output, lookup, parse,
name_key, seconds=...)` implements bounded reader/writer queues, transcripts,
sequence/name echo checks, one outstanding reply, DONE/EOF/clean-exit checks and
one deadline. Its child runs within the selected outer Job. Reuse those protocol
rules in a separately selected public adapter; the existing controller's hardcoded
V1 context/layout and allowance construction are not a generic installed API.
Std-only trusted source selection also cannot silently become arbitrary project
binary ingestion. No such adaptation or runtime is included in this source task.

## Required focused review/evidence

Check exact missing-set/label matching; original claim preservation; forged or
duplicate boundaries; missing supplemental outputs; parent/cross-lane collisions;
forward and undeclared cross-lane references; each aggregate cap; genuine legacy
ID refusal; and lookup/budget exceptions. Pure controls should assert input
nonmutation, output unit order and unchanged canonical consumer unit bytes.
Then root may select one public completion over eligible existing state. Current
source completion is not native acceptance, project interoperability or final v5.

## Changed-seam control contract (source-only, 2026-10-23)

New control source: `software/v5/ordinary_library_package/completion_controls.py`,
SHA-256 `af0f17bca95b1e58a86dfca0f868a023e670af901d1363f2043526fc9833968c`.
The source was written and read back, not imported, compiled or executed. Root
owns the later exact selection and runtime; independent source review is requested.
All already-used planner, coordinator, CLI and package files remain unchanged.

The runner matches root's five arguments: `--package --profile-sha256
--python-runtime --lean-runtime --output`. It hash-checks and executes the selected
owner bootstrap, loads the real successor profile exactly once, and obtains the
actual binder, planner, coordinator and shared core from that profile. CLI controls
reuse that already loaded namespace through an explicitly mocked loader, rather
than bypassing the first real profile load. The current assembled candidate named
by root is `ordinary-library-package-assembly-01/package`, profile
`82ca3a098fd7a51a4c0246bbddf8003d01557374411b5361fd5c7b3d7f6b9680`.

Seven finite groups are proposed:

| Group | What is checked | Explicit limitation |
|---|---|---|
| Positive graph/preservation | Supplemental-before-consumer ordering, a supplemental helper chain, exact original canonical units and hashes, derived import identity, memoized lookups, unmodified caller maps | Synthetic syntax, not Lean truth |
| Graph/identity refusals | Undeclared original dependencies, wrong S/F/parent/schema/assurance, omitted/extra/duplicate missing targets, unneeded supplementation, missing outputs, forged/duplicate boundary IDs, genuine legacy symbol-domain mismatch, original prepared-map mismatch, existing/duplicate/cross-lane outputs, forward and consumer-only supplemental dependencies | No arbitrary-equivalence or missing-library completeness claim |
| Aggregate limits | Combined input bytes, units, declared boundary rows, encoded nodes, evidence bytes, outputs and distinct selected names; small lanes that individually fit cannot evade the combined cap | No stress benchmark or global scale measurement |
| Cancellation/lookup failure | Early cancellation, cancellation at the final planner callback, thrown protected lookup and non-string lookup result all refuse without READY | Cooperative callback behavior; hard containment belongs to the outer supervisor |
| Coordinator retention | Real pure planning/envelope/preview path with one exact-class owner shell; mocked preflight and admission run once with the same real budget; success, preflight refusal and preview failure retain correct input/admission/failure records | No owner opened, no native check; 0.25 CPU charge is explicitly synthetic |
| CLI pre-open refusals | Missing paired selections, operation-only constraints, each wrong input pin, malformed and duplicate prepared maps fail before owner/custody open | Input pinning does not mean a candidate is mathematically valid |
| CLI forwarding/retention | Exact original bytes, parent, names, prepared map, output path and budget callbacks reach the coordinator; later accepted failure reaches the CLI report; mock handles close | Coordinator and opens are explicitly mocked for this group |

SQLite connect, process creation, socket connection, actual owner open/preflight/
admit and peer exchange/start are forbidden except the named local mocks. Only
fresh fixture files beneath the selected output are written. No ordinary catalog,
network, source authoring, Lean runtime, extractor or certificate is executed.
The runner has one nonrenewing 50-wall-second/30-controller-CPU-second allowance;
root's selector separately supplies the enclosing process limits. A failing group
remains a failure; neither these controls nor a future passing outcome authorizes
changing used sources or repeating an already successful mathematics campaign.

This control source does not duplicate the independently completed resilience
controls. A pass would justify only the changed portable-completion boundaries,
not a full missing-library workflow, real project interoperability, measured
growth or final v5 release readiness.
