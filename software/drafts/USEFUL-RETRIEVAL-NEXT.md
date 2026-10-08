# Useful retrieval: smallest next decision

Prospective source-only recommendation, 2026-09-21. No implementation, import, database query, test, native execution, or trial was performed for this note. It does not amend any preserved run.

## Recommendation

Run a small **enumeration-versus-local-library screening comparison before adding a query index**. Use the retained real-library Fin case, a seven-root heterogeneous corpus, two fresh independently authoring consumers, and the existing peer/find/preview/admit/submit interfaces. The new question is whether the current interface completes an unknown-answer-ID task affordably relative to ordinary library work, not whether another three-cast theorem can be proved.

No product retrieval delta is justified yet. Normal `peer_acquire` can populate P1 with the retained packages. A bounded fixture publisher can serve actual inert package bytes through the existing loopback protocol; a new configuration option or registry is unnecessary for this first comparison. This is a local, cooperative, exploratory screening trial, not a release gate or a statistical demonstration of retrieval superiority. A negative comparison is a useful reason not to build a richer index for this workload.

Reuse the evaluation principles in [V1 critical path, C](V1-CRITICAL-PATH.md#c-usefulness-and-efficiency-must-become-measured-product-properties), [continued operation](CONTINUED-OPERATION.md#discovery-must-beat-exhaustive-catalog-enumeration), and the [earlier discovery analysis](../../experiments/lean-local-node/NEXT-DISCOVERY.md). The prior [independent-agent API result](../../experiments/lean-agent-api/RESULTS.md), [definition-inspection result](../../experiments/lean-definition-inspection/RESULTS.md), and [library-interoperability result](../../experiments/lean-library-interop/RESULTS.md) supply retained artifacts and conformance evidence, **not** a completed usefulness baseline.

## What the implementation actually exposes

| Interface | Current behavior | Consequence for the trial |
| --- | --- | --- |
| `node.py` public `find` | Indexed append-sequence range lookup over P1; 1–4 rows, 1–16 KiB, immutable snapshot/cursor binding | It is bounded enumeration, not predicate search. No new enumeration feature is needed. |
| `preview` | Returns the same selected candidate's untrusted formal metadata | A preview is not body inspection or native acceptance; do not automatically pay for it when `find` already supplied enough metadata. |
| `peer_find` | Downloads one entire catalog, at most 32 entries/64 KiB; returns formal metadata and remote handles | At seven rows, this is an available enumeration route. Calling a local filter afterward does not remove the catalog transfer. |
| `peer_acquire` | Transfers and checks selected inert package bytes, recomputes advertised metadata, appends/reuses a local candidate; no native stage | It can seed P1 without configuration surgery. A candidate still requires ordinary receiver `admit`. |
| `checking.metadata` | Includes exact replay/native/semantic references, universe arity, type DAG, descriptor and raw-type symbols | Consumers already have enough formal data to make small-corpus selections without natural-language tags. |
| Admission/`info` | Native-checked receiving names and formal types for the requested/current description | Describe rows are context-bound, not a global catalog or full standard-library browser. |
| `manage inspect` | Historical authenticated ordinary-definition type/body and exact direct-reference names | Useful for equal-type/different-body candidates after admission. It is not untrusted-preview body interpretation, an opaque-unfolding permission, or a new native check. |
| `symbol_index.find` | Separate local raw-type `MENTIONS_ALL` helper, 1–8 known semantic keys, up to 128 rows | It is not wired into public `find`. It rebuilds/validates a snapshot and constructs postings during lookup; it is not an already maintained persistent inverted index. |
| `storage.descriptor` | Internal exact descriptor lookup through the existing keyed store | An exact lookup is useful once an ID is known; it does not discover an unknown answer. No public exact-lookup operation currently exists. |

The helper requires a nonempty query. Thus a type with no constant references is unreachable through `MENTIONS_ALL`, including the retained `first` and `second` definitions. Public enumeration does not have that hole. Exact raw-type symbols do not perform unfolding, theorem application, body search, or semantic equivalence. The theorem proof-instance reference `[7, PI]` is also not its semantic search key `[2, JudgmentID]`.

The cooperative fresh-authoring route already exists: `submit` accepts bounded inline owner-authorized source. The older frozen-source-ID limitation in `NEXT-DISCOVERY.md` is historical, not a reason to add registration now. Source remains executable trusted-local input, not a hostile-source service.

## Exact corpus available now

Use these seven existing package directories, copied into a fresh explicitly bounded trial domain. These paths and hashes are evaluator-only, never the consumer packet. The table was checked by read-only file enumeration and manifest hashing. It is an availability inventory, not a new validation of every old proof.

All seven manifests declare foundation `[1,1,2,b06524af0de7abeda40f5f363459c60bbce3d85e4a9ee2de6eb362569e36629b]`. This is also the product's selected foundation. Equality of that field is necessary, not sufficient: preparation still validates actual object bytes, closure, supported metadata, and fresh receiver admission where used.

| Evaluator label / content | Existing directory relative to repository | Manifest SHA-256 | Files / bytes |
| --- | --- | --- | ---: |
| Actual `Fin.castLE_castLE` and reached library closure | `experiments/lean-library-interop/runs/attempt-01/A0/out/inverse` | `b23a39de946b20dd7ace2540cb93f3117ed445211149497b90c30afae4a85389` | 38 / 290,893 |
| Ordinary composition `f (g x)` | `experiments/lean-definition-inspection/runs/attempt-01/A1/out/first-inverse` | `f0e318ebbe159b3b29e70d6e3407ed767e2e870fd843985f7f649704497c8d40` | 10 / 281,205 |
| Same type, body `g (f x)` | `experiments/lean-definition-inspection/runs/attempt-01/A1/out/second-inverse` | `9a214f028fbe37adf95f693b2dadad4ee6279890598a4ac60be31568e1077efd` | 10 / 281,198 |
| Independently authored injective-lift theorem A | `experiments/lean-agent-api/runs/attempt-01/A8/out/inverse` | `204a20ac4c2cb7e8f2f026a0c6255541f18710a60d8661778df49b3dbabf3831` | 37 / 297,642 |
| `val_congr` | `experiments/lean-agent-api/runs/attempt-01/A1/input/corpus/c5` | `7d2da46f56f713d8ee47333e41fd816930763aec1cedbe0ea1f904e3aa3b4742` | 19 / 289,270 |
| `exists_val` | `experiments/lean-agent-api/runs/attempt-01/A1/input/corpus/c7` | `43537980c40a776da55bbe670aeea135f3e29f3b6c836c172c878fb74eed38bf` | 24 / 290,461 |
| Injectivity with an extra subsingleton-domain premise | `experiments/lean-agent-api/runs/attempt-01/A1/input/corpus/c8` | `cf4220c569b8f09a946c2dda1c07ed8bc1f4584bf1bdd4f05636733f075fa91d` | 19 / 289,347 |

The seven complete directory copies total 157 files / 2,020,016 bytes, including repeated foundation payloads and JSON manifests. That is not their deduplicated object stock, network framing size, retained run size, or preparation cost.

This is three mathematical families, not a claimed broad representative corpus. The Fin root is real existing library content; A has retained independent authorship; the rest include hand-authored engineering distractors. The equal-type composition pair tests metadata ambiguity without pretending that the two bodies are semantically identical. Opaque `sealed` is deliberately excluded: the current publication metadata root-kind cut does not support it.

Retain exact-duplicate burden as a small separate control: after a normal acquisition, repeat the same remote selection with a **new** request ID and measure its transfer/validation/storage/charge behavior. Exact request replay is a different control. Do not insert duplicate bundle entries into one catalog: `build_view` rejects duplicate bundle digests. Neither kind of duplication counts as new mathematics.

## Onboarding: existing peer path first

Recommended preparation is a frozen **external fixture publisher**, not a product-node publication bypass:

1. Copy the pinned inert packages into a new trial directory; retain a full inventory. Derive/check their formal metadata with the existing package reader and metadata helper. This setup is charged and is not native acceptance.
2. Bind a stable nonsuggestive catalog order, all actual descriptor IDs, full catalog bytes, and complete bundle bytes before dispatch. Use existing `peer_wire.build_view` under the fixture owner's explicit authority to publish these selected fixtures, and `peer_service.serve` under the real bounded process supervisor. No hand-written favorable responses, altered packages, or invented mathematical rows.
3. Configure the fresh receiver with this fixed loopback contact using the existing operator option. Use normal `peer_find`, `peer_acquire`, `find`/`preview`, `admit`, `inspect`, `submit`, and `publish` as chosen by the consumer. Receiver acceptance never trusts the fixture publisher's historical proof claim.

The service is an external finite data publisher. It is not `manage serve` pretending to have a committed product view. Product `expose` requires a local publication marker, and the current receiver cannot expose acquired-only entries. Do not insert database rows, use private `mark_published`, or call an old research package a newly published product artifact to evade that boundary. Fully product-to-product republication would need its own legitimately authored/publication path or the separate custody work; it is unnecessary for this screening question.

Prefer on-demand acquisition after the full catalog over forcibly transferring all seven bodies. If a local-P1 enumeration submeasurement is wanted, normal acquisition of all seven also works prospectively: count seven acquisition requests, their actual transfers and 448 MiB of conservative request reservation, plus initialization/catalog calls. No new native acceptance follows from seeding P1. Do not hide that onboarding behind the first cheap `find` page.

Alternative: `load_config` accepts at most eight initial offers and `init` already runs `checker.offer`; `manage configure` always writes `offers:[]`. A fresh-only `--offer` frontend could expose that existing mechanism, with bounded package pins and domains. It would need code, tests and a new qualified cut, and would still not grant native acceptance. Do **not** add it solely to make this trial easier while the ordinary peer path is available. Never edit a live node's configuration identity.

## Small paired screening trial

Use one full, already specified interoperability target: the arbitrary-bound three-cast law in [the library result](../../experiments/lean-library-interop/RESULTS.md#result-and-mathematical-content). Do not give either consumer the old solution, theorem `Fin.castLE_castLE` name, exact answer ID, package label, catalog position, proof hints, or previous transcript. The target is stated using the ordinary bound-changing Fin operation, not a hidden contributor identity. If the packet needs receiver-only syntax, define that **problem vocabulary** explicitly by the usual Fin constructor/value and bound proof; do not preload the two-cast theorem to obtain the vocabulary. Exact packet syntax and target equivalence must be reviewed before any consumer launch.

The network consumer starts with only the ordinary five-package common context, unranked common bindings, task/API packet and peer contact. It chooses enumeration, inspection, acquisition and proof construction. It may solve directly without retrieval. A locally written direct proof is not a trial failure merely because no acquired dependency was used.

The local-library consumer starts fresh with the same formal problem and pinned Lean version, ordinary installed Init source/library lookup and direct proof facilities. It may discover and use `Fin.castLE_castLE` or prove the goal by reduction. Do not suppress standard mathematics, `rfl`, or normal library names to favor the network. This is the competent practical alternative to the product, not a deliberately weaker solver. This screening baseline need not import unrelated research corpus merely to pay an artificial fee.

Use two new no-history consumers with the same model/settings and interaction allowance, no communication, and no evaluator mathematical repair. Their sources must be authored after dispatch, not fixed replay of the retained successor. Root runs only requested, reviewed actions and mechanical serialization. Record all documentation differences. A shared-host no-history/cooperation rule is not enforced filesystem isolation; retain full exposure transcripts and describe contamination honestly. Randomize which arm runs first, keep native execution serial, and do not give the second arm observations from the first.

Suggested prospective ceiling, subject to root's explicit freeze: 15 minutes end-to-end per consumer, 24 ordinary requests, two source attempts, two admissions and two definition inspections for the network consumer; the local baseline gets the same source-attempt and elapsed allowance. Retain existing per-operation limits, with an additional common aggregate execution budget (for example 600 measured enclosing-Job CPU seconds per arm) and explicit preparation allowance. The proposed numbers are not execution authority or a claim that the trial will fit. Initialize/prepare outside the consumer timer only if also reporting that time and cost in the cold result. Stop at the frozen ceilings; do not extend one arm after seeing a failure.

Keep endpoints separate:

- **Common primary task endpoint:** correct full target with a kernel-checked source result under the pinned runtime. No weakened universes, bounds or hypotheses. This supports a practical completion comparison.
- **Network contribution endpoint:** the node's accepted canonical/inverse/fresh-replay artifact and, if requested, publication. That stronger artifact service costs extra and must not be compared to bare local compilation as if obligations were identical.
- **Actual reuse:** the exported term supplies substantive evidence from a discovered/admitted theorem or body. Audit reachable applications/dataflow, not source string counts. Direct completion remains valid and is recorded separately.

A whole-pipeline benefit claim requires the local arm to produce an equivalently reusable checked artifact through a prospectively supported export route, or a matched all-canonical local-library arm. That route is not silently supplied by this note. Without it, report the primary proof-completion comparison and the extra contribution service separately; do not announce net savings from mismatched endpoints. This is why the first trial is a screening decision, not completion of critical-path C.

Before dispatch, run only necessary readiness work: verify corpus/canonical metadata and full catalog fit existing bounds, confirm task vocabulary and ordinary source syntax under the chosen environments, and bind the generic request runner. Do not run either retained answer as a consumer rehearsal. Use the existing no-new-axiom/kernel/capture/inverse gates; no benchmark-intention field enters product acceptance.

## Costs, decisions, and only then a delta

Report cold and marginal costs separately: original retained production costs as historical/sunk inputs, new corpus validation/copying, metadata extraction and view build, library/bootstrap onboarding, all catalog bytes, body transfer, selected package validation, native admission, body inspection, source attempts, inverse/fresh replay, publication, failed/refused calls, final retained stock, CPU/wall/peak memory, consumer and broker elapsed time. Enclosing Job CPU already includes its nested native children. Missing model token/compute measurements stay unknown; no complete-compute saving follows from a wall-clock difference. State any amortization horizon rather than calling a warm corpus free.

Predeclare the screening question: does the existing enumerating network route finish the full task within the same elapsed/source-attempt budget, and what fraction of its effort is candidate selection rather than transport, validation, frontend friction or final verification? Report each arm's actual completion/time/cost; one matched pair is noisy and cannot establish a population advantage. Do not call fewer returned candidates or a successfully reused theorem a benefit by itself.

Decision table:

| Observation | Smallest justified next action |
| --- | --- |
| Seven-row enumeration completes cheaply; local direct/library work is as good or better | Keep enumeration. Do not implement an index to rescue this workload. Select a genuinely more demanding independently authored task before claiming usefulness. |
| Both mathematical paths work, but transport/validation/onboarding dominates | Profile that measured phase. Faster ranking cannot remove already downloaded catalog bytes or repeated package checking. |
| Consumer cannot understand/use available formal types or definition bodies | Fix the demonstrated documentation/description gap, with one discriminating case. No general natural-language gateway is implied. |
| Local review of many irrelevant rows dominates on a larger frozen corpus | Add one bounded raw formal filter over existing metadata, retain enumeration fallback, and compare against the unchanged enumeration arm. Start with known-symbol inclusion and/or kind/universe fields, not semantic equivalence. |
| Constant-free targets are missed by symbol filtering | Keep the explicit enumeration fallback; consider exact type lookup only after a real formal-type query-construction path exists. A hidden answer TermID is not that path. |
| Whole peer catalog exceeds the 32-entry/64-KiB profile or repeated catalog downloads dominate | Specify snapshot-consistent remote paging/incremental metadata next. A local symbol index cannot fix that transport limit. |
| Repeated access to an already known descriptor is the bottleneck | Expose the existing exact keyed lookup with current snapshot/client binding; do not market it as unknown-ID discovery. |

If the first Fin comparison is too easy to distinguish policies, say so. The next independent task can use the equal-type/different-body pair to test unknown-ID semantic selection and a fresh checked inverse-composition successor, with a matched local corpus baseline. That is a separate prospective choice, not an automatic extension or another renamed proof claimed as useful growth. A third useful-growth task must involve content not already supplied as a solved answer in the packet; a standard-library floor remains legitimate.

No new universal novelty score, registry hierarchy, human-intention gate, mandatory research agenda, automatic prover policy, or population usefulness claim is selected. The next implementation choice supported by this inspection is **a bounded trial harness and transparent cost accounting, not a product query subsystem**.
