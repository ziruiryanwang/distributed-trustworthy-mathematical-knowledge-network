# Definition-body discovery: independent changed-source review

2026-10-23. Reviewer: `admission_event_audit`. Read-only source review under
`ORDINARY-BODY-DISCOVERY-SELECTION.md`; no experiment, Lean operation, catalog
change, certificate production or Git mutation. This reviews the economical
two-stage design's implementation boundary, not the already passed reciprocal
native workflow or the superseded reducer proposal.

## Current disposition

**No blocking source issue found in the four reviewed implementation files or
the final focused check source pinned below.**
The new adapter binds a bounded syntactic hint to exact singleton-definition
evidence without granting mathematical acceptance. Existing record meanings
remain unchanged. Runtime evidence remains a separate obligation; this note
does not authorize an execution.

| Reviewed source | SHA-256 |
|---|---|
| `ordinary_body_adapter.py` | `310980b1dab7339c68e4262c02bcff28b81cf61c08bf7c82c54b31966a4aaf32` |
| `formal_features.py` | `f1f53ee40ce32126085f7f776c47d9d0ab2c5b7c679d40f018f6bff70f6430e5` |
| `authenticated_index.py` | `77a12cda9dd4a303153b59d00998de8aa6bf08bb572af10136e21dfa9c96cc95` |
| `discovery_store.py` | `da0c4f51f980353d915a17c98bfc49d40c901d5291dcdc6cb8b3472212d16783` |

Paths above are under `software/v5/discovery/`. These are reviewed working
source bytes, not installation or acceptance identities.

## Source and identity binding

The new record is V4, kind `ordinary-lean-definition-body-v1`, in a namespace
committing to the selected semantic ID, exact fixed path profile, feature and
record schemas, evidence schema, expression format and feature revision.
Its object ID is the exact ExportID; its locator identifies the exact semantic
ID, UnitID and original export name. Its byte count and SHA-256 describe the
**whole portable V2 evidence**, not a proof-free type preview.

`describe` first uses the bounded strict portable reader, which establishes
canonical bytes, grammar, complete serialized name/import census and UnitID.
It requires the selected semantic interpretation, descriptor kind zero,
one inventory row of definition kind one, then exact descriptor/inventory
agreement on name, universe parameters, type, body, reducibility hint and
all-names list. The latter must be precisely the singleton own name. This
closes the ambiguity that the generic syntax census alone intentionally leaves
to later native checking. Theorem, opaque, inductive and inconsistent inventory
inputs cannot enter this particular body profile.

Body constants are interpreted as the exact asserted imported symbol IDs or
the unit's own exact export identity. No dependency body is fetched. These are
still unproved claims: a well-formed unit can fail native checking later.

`resolve` checks the expected namespace/schema, reparses the exact evidence,
recomputes the full record and requires full record equality. Consequently a
changed body, claimed feature, byte count/hash, name or identity cannot silently
retain the original candidate record. Successful resolution explicitly returns
`mathematical_acceptance: false` and directs the caller to match warranted
imports and perform ordinary admission.

## Scope and path semantics

The fixed ordered paths are:

```json
[["body","body","arg","arg"],["body","body","arg"],["body","domain","arg"]]
```

They use ordinary binary DAG edges. A source strips only its leading lambdas;
it does not remove the remaining property's foralls or implication binders.
A consumer validates a **closed** ordinary expression and strips exactly the
explicit `context_binders` leading foralls. Missing telescope structure refuses.
No implicit convention discards all goal-internal quantifiers.

The observer tracks the internal binder count at each path position. A bvar
below that count denotes an internal binder; a source bvar in the stripped
parameter range yields STAR **before** any missing-child decision. A consumer
context bvar is distinguished from an internal binder and forces STAR in its
query coordinate. Thus descending beyond a source parameter cannot falsely
turn a substitutable position into an absent-child constraint. The observer
does not memoize a node without its scope or expand shared DAGs into trees.

The independently recorded Stable/property trace has tokens `local 1`,
`node app`, `local 0`. This profile does not preserve P/Q sharing or recognize
general application/equivalence: intentional collisions remain candidates.
In particular the reduced composite goal need not match the unreduced
parameter-substitution instance. The agent's independently chosen preservation
premise is the relevant operating example, not an automatic goal solver.

Query generation produces at most eight **separate singleton alternatives**,
deduplicated deterministically and sorted by increasing STAR count with
canonical-spec-byte tie breaking. They are not one conjunction and their
generation is not authorization to execute all alternatives for free. In
particular the broad all-STAR fallback is not automatically funded or executed.

## Bounded work and configurable limits

Raw evidence is byte-bounded before parsing. Ordinary syntax validation also
bounds expression/level counts, whole-unit nodes, names, imports, integer
grammar, JSON depth and DAG depth. The body traversal adds at most the admitted
leading-lambda count and **13 path visits**, with no normalization, substitution,
recursive imported-definition fetch or proof expansion. One source emits one
fingerprint feature.

The query entry takes local Python objects, so its explicit iterative preflight
is important: it runs before the ordinary validators, whole encoding or copy.
It counts supplied occurrences rather than unique object identities, charges
encoded size, limits depth and accepts only literal JSON-compatible types.
Repeated references therefore cannot obtain uncharged exponential serialization;
cycles encounter the finite depth limit. String length is bounded before
single-string encoding; integers are bounded before decimal encoding. The
per-string temporary may exceed its charged final byte allowance by a bounded
escaping factor before refusal; this is not a hard process-memory quota.

The final reviewed adapter uses explicit defaults: **1 MiB** raw/query envelope,
32,768 expression nodes and 8,192 level nodes per DAG, 131,072 whole-unit nodes,
DAG depth 256, JSON depth 64, 128 universe parameters, one inventory row,
128 name parts/16 KiB name bytes, 64 KiB literal bytes and 8,192 imports. All
trusted caller overrides must be componentwise no greater than these defaults.
This excludes accidental broadening via a generic ordinary `E.Limits()` value.

During source-only review, initial adapter `f165dbdb` inherited the generic
8 MiB ordinary limits and returned alternatives in hash/spec order. Root
selected the explicit smaller default and fewest-STAR-first order before any
runtime. The changed `310980b1` constructor/order branches were independently
read; neither changes fingerprint identity or the authority boundary. The
revised design now documents actual defaults and structural-work scope.

Reported `work` is a structural node/peel/path census. It omits byte scanning,
canonical encoding, name processing, comparisons, hashing and index/transport
costs. It is not total CPU work or evidence of net savings. Parsing accounts
for the complete envelope, including repeated descriptor/inventory data.

## Compatibility and acquisition

The root changes are additive allowlist entries, a lazy V4 validator branch and
a distinct V4 record-hash domain. V1/V2/V3 validators, domains and namespace
interpretations are unchanged. Old isolated assemblies do not load the body
adapter merely by reading old records. Existing posting, snapshot and store
operations are reused; they still establish metadata commitments, not truth
or population completeness.

The existing `OrdinaryAcquisition` constructor currently takes the ordinary
preview adapter. A caller can retain that S-matching adapter for its generic
`evidence(provider, S, UnitID, max_bytes, expected_export_id=...,
expected_export_name=...)` operation, then call the new body adapter's `resolve`
on the returned full bytes. It must **not** call `preview` on a V4 body record.
After learning a definition's exact symbol, stage two deliberately returns to
the unchanged V3 type-preview index. The definition bytes can be retained and
reused for later admission instead of being downloaded twice.

Candidate membership does not prove honest extraction until full resolution,
and resolution does not prove mathematical validity. Bounded search remains
potentially incomplete. First-stage collisions and second-stage symbol degree,
all attempted alternatives and failed candidates, both index stages and data
acquisition belong in one aggregate cost/deadline allocation. Existing search
prepayments must occur before the first ordinary evidence fetch.

## Remaining changed-boundary evidence

The selected small metadata-only controls should distinguish exact evidence
from type previews; check descriptor/body/hint/all-names consistency, context
vs internal binder scope and STAR-before-child behavior; exercise malformed,
cyclic/shared/oversized local inputs; and compare an independently spelled
property against the retained actual Stable evidence through real index queries.
The source's intentional P/Q collision must survive as an ambiguous candidate.
Use existing evidence and no Lean build or passed-loop rerun. A resulting
selectivity benefit would be conditional on this workload, not a general
useful-growth theorem or full v5 delivery.

## Final focused-check source review

The reviewed `software/v5/discovery/ordinary_body_adapter_checks.py` has SHA-256
`29a55fe05a3c0a5b41acfbca9990893227c21845bbef700eba77eaa62da46442`.
The author confirmed these final bytes. This reviewer read the complete initial
check source and all subsequent changed sections, including the final integration
and its existing query API contracts. No tests or imports were executed here.

The four groups cover the independently constructed query and retained actual
Stable trace; descriptor/inventory consistency, evidence/preview separation and
bounds; exact imported constants and shared DAGs; and a real two-stage local
Store query. The consumer query is constructed, serialized and reported before
either producer input is read, and is checked unchanged afterward. An independent
tiny expression encoder and reference token-mask derivation avoid using a
publisher record as the initial query oracle.

The finite integration corpus has nine definition records and nine method
records. Only the most-specific first alternative, selected before publisher
reads, is attempted. The other seven alternatives are generated and ordered in
separate controls, not broadcast. The all-STAR alias is present but not fetched.
Actual Stable and one intentionally colliding P/Q definition are both acquired
and resolved, and **both** exact-symbol second-stage searches are charged. The
collision is expected to return no method. The one returned method is resolved
as a V3 preview and bound to retained full evidence without claiming acceptance.

The comparator uses the exact preceding workflow's conjunction: theorem kind
and `binder-domain-head(forallE)`. Seven theorem decoys satisfy both conditions;
the non-theorem with the learned symbol is excluded by kind. This corrects the
initial unfair proposal whose bare-constant decoys would not have matched that
preceding query. The gate compares the sum of stage-one and stage-two examined
postings against the comparator's examined postings. It is **not** a total-cost,
CPU-speedup, applicability, native-validation or useful-growth experiment. The
existing query verifier returns the tested `termination` field and the page's
`examined` value is a list, so the reviewed count/termination checks match the API.

Static review also corrected the inherited generic-limits constructor in tighter
limit tests, the earlier inventory-count refusal code and the early-context STAR
expectation. Distinct controls now cover endpoint context variables, unfinished
paths, Python shared-container preflight, cyclic inputs and compact ordinary DAG
sharing. Narrow compatibility checks recompute V3 record and existing snapshot
hash domains, resolve an old preview, and refuse V3/V4 namespace/schema crossing;
they do not repeat an old native or transport campaign.

One local-test ledger spans all queries, both collision branches, acquisitions
and the comparator: 120-second original deadline, 64 calls and 8 MiB returned
bytes. It is explicitly not the product's transport budget or a hard process
resource quota. Both fresh SQLite stores close in `finally`. Root's separately
selected outer supervisor must supply the actual process envelope; a tighter
outer limit does not reset or broaden the check's original inner allocation.
There is no Lean subprocess, certificate operation, network service or accepted
catalog mutation in this check source. No blocking source issue remains known.
