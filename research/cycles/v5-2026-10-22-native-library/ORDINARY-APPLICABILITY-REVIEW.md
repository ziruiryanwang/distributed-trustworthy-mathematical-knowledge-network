# Independent ordinary vocabulary-discovery review

2026-10-23. Source/theory review; no new runtime, native checking, acceptance or
growth result. Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Decision

Support the source-bound two-stage route selected in
`ORDINARY-BODY-DISCOVERY-SELECTION.md`: discover a singleton transparent
definition from a local formal property, then use its newly learned exact
ExportID in the existing theorem/type-symbol index. Keep the original ordinary
preview, acquisition, admission and actual-use gates distinct. This is vocabulary
discovery followed by candidate method discovery, not a general applicability
decision procedure.

The original custom beta/zeta/delta reducer and blinded role sketch are not
needed for this decision. Existing `type_pattern` already preserves exact
whole-type syntax while blinding private symbol addresses; it does not expose a
definition body. Existing `instantiation_discovery/conclusion_fingerprint.py`
already supplies bounded paths, STAR alternatives, and explicit local-context
scope. Its observation principle should be adapted to the portable DAG, not
replaced by another normalizer or unifier. Existing conjunction postings can
combine useful filters but cannot cure intrinsically huge matching sets.

## Exact source and local trace

Use these three paths in this exact compact-JSON-byte-sorted order:

```json
[["body","body","arg","arg"],["body","body","arg"],["body","domain","arg"]]
```

The longer shared-prefix path comes first because its comma sorts before the
shorter path's closing bracket. Paths are binary AST edges, not n-ary application
positions. The current source example is structurally:

```lean
fun {α} (f : α → α) (P : α → Prop) => ∀ x : α, P x → P (f x)
```

Strip exactly its three leading parameter lambdas (`k = 3`), retaining both
`forall x` and the implication binder. Independently construct the consumer's
actual local premise `hf : ∀ x, P x → P (f x)` as the closed telescope
`∀ α, ∀ f : α → α, ∀ P : α → Prop, ∀ x : α, P x → P (f x)` and declare exactly
three local-context binders. Remove only those three, never all leading foralls.

| Path | Internal binder count q | Reached expression | Source/local token |
|---|---:|---|---|
| `body/body/arg/arg` | 2 | `x` in `P (f x)` | `["local",1]` |
| `body/body/arg` | 2 | `f x` | `["node","app"]` |
| `body/domain/arg` | 1 | `x` in implication domain `P x` | `["local",0]` |

The source and independent local premise therefore share one vector, without
knowing a remote definition's name or identity. Source parameter occurrences
yield STAR before missing-child handling. Local-context occurrences are forced
to STAR; other observed tokens each optionally become STAR, producing at most
eight separate singleton alternatives, not one conjunction of all alternatives.

The vector deliberately does not establish predicate or function sharing:
`∀ x, P x → Q (f x)` can collide. It also does not identify independently scoped
variables in distinct premises with one another. A composite goal
`∀ x, P x → P (f (g x))` has an application at the first listed path instead of
`x`. Substitution of `f := fun x => f (g x)` creates a beta-redex before reduction,
so raw-substitution recall does not guarantee matching that reduced goal.
Choose the actual preservation premise before seeing remote data; do not silently
claim automatic goal applicability or inject the publisher's private ID.

## Source-bound full-evidence record

Stage one binds the raw exact canonical portable V2 evidence bytes, SHA-256 and
byte count. The record's object identity remains its target ExportID and its
locator remains semantic ID S, UnitID and exact name. Stage two continues to use
the existing ordinary type-preview record and adapter unchanged. A type preview
has no body and cannot stand in for stage-one evidence; the existing
`OrdinaryAcquisition.preview` namespace must not be silently reused for this object.

Before deriving the feature, require all of the following:

- Select the supported exact S, strictly parse canonical V2 bytes, verify exact
  ordered imports, recompute UnitID, and derive the chosen ExportID from
  S/UnitID/exact name. Verify advertised raw hash/bytes separately on acquisition.
- Require one expected export and one inventory row, with the chosen locator
  name equal to that export. Require descriptor kind 0 and length 7:
  `[0,name,params,type,body,hints,all_names]`; inventory row kind 1 and length 5:
  `[name,1,params,type,[body,hints,all_names]]`.
- Require exact descriptor/inventory equality of name, params, type DAG, body
  DAG, hints and all_names. `ordinary_evidence.inspect_unit` validates these
  fields individually but does not prove their equality. Native roundtrip may
  later reject a mismatch; retrieval must not choose one conflicting body now.
- Derive only from that agreed body and strip only its leading lambdas. Refuse
  theorem, opaque, generated/recursive-group or ambiguous body selections in
  this first view. Resolve visited constants through the unit's exact imports;
  derive no authority from their asserted addresses.

Re-deriving the record from fetched full evidence establishes hint/source
correspondence, not mathematical acceptance. Dependencies need not be fetched
to fingerprint raw syntax. A selected full definition can subsequently be reused
for actual admission: charge its one acquisition once, not as both a search
preview and a later duplicate unit. Do not imply global definition download
before searching. Admission and actual application remain independent obligations.

## Work, search and comparator obligations

Retain at most three paths, each at most twelve edges, and at most eight query
alternatives. Bound raw canonical bytes before parsing, total parsed DAG nodes,
leading-lambda/context peel counts, visited positions, query generation and
retained features/postings. Never occurrence-expand a shared DAG, substitute,
normalize or unfold a proof. Parsing cost includes the complete type/body and
duplicated descriptor/inventory envelope, not merely the path visits.

Every selected alternative, page/offer, failed search/candidate, evidence fetch
and stage-two query belongs to one original aggregate request/reply/deadline
allocation. Existing `charge_external` search reservations must all be made
before the first ordinary acquisition fetch. Separate alternatives are not free
fallback attempts and do not renew a deadline or budget. One source fingerprint
adds one feature per supported definition; the distinct profile namespace,
materialized postings, inherited metadata duplication, rebuilds and updates have
real storage and work costs and need their own accounting.

Selectivity is conditional at both stages: many definitions can share the body
fingerprint and many theorems can mention the discovered symbol. The deliberate
P/Q collision must survive as a candidate, not be mislabeled an invalid proof.
There is no completeness, global-search or useful-growth guarantee. A fair local
library/package-manager comparator may use the same structural index and caches,
the same starting knowledge and checking policy, and the shortest local proof.
Stable composition is elementary and may be cheaper to derive locally; this is
a compatibility/selectivity discriminator, not a positive growth witness.

## Implementation decision and next checks

The smallest justified source change is a portable singleton-definition body
adapter plus bounded staged query orchestration using existing index/transport.
The superseded reducer sketch lost premise f-sharing at its depth-three cutoff,
distinguished variable/constant roles too rigidly for instances, and risked
fetching complete units merely to discover opaque declarations. These are
reasons to prefer the smaller selected route, not claims that it solves every
retrieval class.

Root has now separately authorized new metadata-only check source in
`software/v5/discovery/ordinary_body_adapter_checks.py`. It must cover actual
retained producer evidence versus an independently built premise, real two-stage
Store/Query retrieval with diverse decoys and an intentional collision, exact
source binding, scope separation and deterministic bounds. Source authoring is
not execution permission. No native rerun is needed to decide this metadata seam.

Verdict: no principle blocker to that narrow source selection, provided the
binding and budget obligations above are enforced and independently reviewed.

## Source-only controls checkpoint

The revised primary design and adapter `310980b1dab7339c68e4262c02bcff28b81cf61c08bf7c82c54b31966a4aaf32`
were read after the principle checkpoint. They enforce the required source-body
agreement and use an explicit 1 MiB envelope with componentwise tighter caller
limits only. Queries are ordered fewest STAR first, then canonical spec bytes.
The most-specific query is the selected ordinary path; broader alternatives,
especially the potentially hot all-STAR bucket, remain optional and separately
funded. Context variables before an unfinished path give ABSENT; only a final
CONTEXT coordinate is forced to STAR. Source parameters instead give STAR
immediately, before any missing child. The controls distinguish all three cases.

New `software/v5/discovery/ordinary_body_adapter_checks.py`, SHA-256
`29a55fe05a3c0a5b41acfbca9990893227c21845bbef700eba77eaa62da46442`, is source-only.
No Python execution, compilation, native operation, network or Git mutation was
performed by this author. Independent changed-source review is requested.

The CLI takes `--store-root`, `--definition-evidence`, `--definition-sha256`,
`--method-evidence`, and `--method-sha256`. It constructs and reports the complete
query from an independent named-variable AST before opening either publisher
input. The retained producer02 inputs under `experiments/v5-local-checks/` are:

| Evidence | UnitID | Raw SHA-256 |
|---|---|---|
| Stable definition | `06533a9a85bcdab657bf8d066df9c93f33d36c63ee7e57e838604d995de4aede` | `3c49e5918e3e090674b11c2e72069c901a96da96282d412ea205c2063fa4846e` |
| Composition theorem | `e15df5b8efae5a1394da539bfabe3d2f8e82ddc5c7796aaa9c64e7d37a4bab81` | `e4963ac6bbd03e9744f6b47552253777f0cd69edb8b794e8e757b3aceb4dd87c` |

Four bounded groups cover: exact retained trace and scope/STAR order;
descriptor/inventory, byte/ID/namespace/kind and input-limit refusals; exact
constant bindings plus shared DAG/Python-container preflight; and real
Store/Query retrieval. The latter uses nine definition records including the
intentional P/Q collision and an unqueried all-STAR alias, plus nine preview
records. Both matching definition candidates receive exact full-evidence
resolution and a stage-two query; the false candidate's zero-match branch counts.
The expected sole method is then bound to the retained full theorem evidence,
without mathematical admission or native replay.

The baseline is the **actual predecessor** conjunction `declaration-kind=theorem`
and `binder-domain-head=forallE`, not a weaker all-theorems query. All seven
synthetic theorem decoys have a closed forall-bearing type with a forall-headed
domain and a reachable unrelated symbol, so the old broad filter really matches
them. The selected discriminator compares total examined stage-one plus stage-two
postings against that baseline, while reporting requests, reply bytes, false
branches, both store footprints and all generated/attempted alternatives.
It is not a full-cost or stronger-index/package-manager speedup assertion.

The source's one original 120-second local-test deadline, 64 aggregate calls and
8 MiB replies include comparator work and all actual branches. These local-map
accounting checks are not an HTTP or OrdinaryBudget qualification; a separately
selected outer finite runtime envelope remains required. Both fresh SQLite
stores are retained; no old installation, evidence or accepted catalog is edited.
