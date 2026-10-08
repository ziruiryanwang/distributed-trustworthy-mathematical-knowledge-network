# Replica native discriminator: independent source gate

2026-09-21, reviewer `context_dependency_audit`.

**PASS for the corrected source cut below. No remaining blocking finding.** One concrete pre-execution harness defect was found and corrected; see below. This is not an exact-launch approval, execution result, canonical-dependency audit, native-custody outcome, or release qualification. Root alone owns the forthcoming launch and execution.

The selected design, full frozen coordinator, full original frozen worker and implementation note were read. The single corrected worker delta and updated note were then checked. Supporting inspection was limited to relevant current product interfaces and preserved historical input/evidence; earlier product/state-contract reviews were not repeated. This reviewer performed only source reads and inert PowerShell/.NET file/hash/text operations: no Python import, parse/compile, execution, tests, SQL, network probe, product copying, fixture mutation or directory move. Only this note was written.

## Reviewed cut

Paths are relative to `E:\Distributed Trustworthy Mathematical Knowledge Network\software`.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `drafts/REPLICA-NATIVE-DESIGN.md` | 16,669 | `372F61D0144271439D9555A387231D563028E76928C4F17C86A3F281A32A452D` |
| `tests/replica_native_worker.py` | 62,527 | `A9579275E6CA7863FF99FADFCA2EC4B89653530E190B6731AD266AA73FAE2B7A` |
| `tests/run_replica_native.py` | 16,262 | `1199EBAA6A0EC753BC90D9A216D89407CE75F0E6B8311A6470A5346F801D47B9` |
| `drafts/REPLICA-NATIVE-IMPLEMENTATION.md` | 8,477 | `46DC528C9166BEFABFC257931B3F31F4550EA09C6E3176383EFCDE2EFF658267` |

## Found and corrected before launch

The original worker (61,733 bytes, `DF42CF37B4449C2BC16E2D213CB8B982F7422010598D99D931D007CEC5B56248`) required empty stderr for every preparation CLI. Current `build.py` deliberately redirects the stage runner's successful status envelope to stderr; preserved native02 build stderr confirms this. That worker would have stopped at `PREPARATION_FAILED:build` after a genuine successful build.

The final `cli` permits only a bounded, strictly parsed JSON stderr record for the actual build role. Before either configure call, `prepare` authenticates the support receipt, binds build stdout exactly to the actual build-receipt status/pin, and binds stderr exactly to `{record: <support-receipt path>, status: <support status>}`. Configure still requires empty stderr; arbitrary/additional stderr is not ignored. Reversing just these text changes in memory reproduces the original worker's exact length and SHA-256, confirming no unrelated worker edits. Coordinator, product, workload, grants and roots did not change. Neither source version was executed by this reviewer.

## Decisive source checks

- **Scope and inputs.** A is a finite static fixture, not a fresh mathematical producer/publication. Six historical files are authenticated then copied as raw bytes into the new allocation; prior outcome notes are interpretation records only. H's exact 1,465-byte UTF-8 source is hash-bound and round-tripped without terminal-text reconstruction. Fresh B/C share one new source installation and support build but have disjoint state/scratch/configuration domains and locally checked bootstrap foundations. No old installation, database, context or prepared node is reused.
- **Real service lifecycles.** A's wrapper uses the pinned installed supervisor/runner for its same-worker static mode, with eight source/grant pins and no product view record. Both B services use actual `manage.py serve` and `service_worker`, with the current thirteen-pin closure. Ordinary requests use the current twelve-pin closure. Readiness is a bounded file observation, never an HTTP probe. Positive services require the actual adjacent request/command/output/event/receipt bindings, two successful connections/responses, checker-free observations, direct reap and final Job active-zero/close before establishing stop offsets. A's stop precedes B replica preparation; positive and tampered B stops precede C admission. Fixed ports 42381/42382 have no fallback or restart.
- **Expected negative service.** The product authenticates the frozen bundle in `load_view` before creating a listening socket/readiness file. The harness binds the genuine nonzero inner receipt and exact wrapper `SERVICE_REFUSED` forwarding, requires `BUNDLE_DIGEST_MISMATCH`, and forbids readiness. It does not turn a missing or failed transport receipt into an expected product refusal.
- **Original representation and B non-admission.** The derivative changes only one leading manifest byte plus the necessary length/digest/catalog/completion commitments; object bytes/order and mathematical metadata remain fixed. Real B acquisition must distinguish inbound and normalized manifest bytes/hashes, match their canonical object maps, and reconstruct the derivative exactly. The actual B replica and C inbound package must reconstruct the same 298,038-byte bundle. Ordinary unpublished exposure must refuse. B's bootstrap head/stage persist, its ledger never receives G admission/publication, and its only new exposure authority is the custody view.
- **Exact new-copy mutations.** `mutation_file` resolves non-reparse targets and requires equality to the separately constructed new B work path before a write handle is opened. Original bytes are saved/fsynced and the intent pins/census recorded first; the post-write map must differ in exactly the selected file. The only overwrites are the inbound manifest's presentation substitution and the completed replica bundle's final-byte XOR fault. `quarantine` resolves both package directories before either move, requires disjoint proper descendants of B's acquisition request directory, rejects overlap with the view/root and existing destinations, preserves file censuses, and verifies the exact renamed request census. These are recoverable moves within the fresh allocation, with no delete, old-file write or repair. Empty directory metadata is not claimed as a byte-level file-census identity.
- **C's fresh selected workload.** C acquires only through B, with unchanged bootstrap head/stages until admission. A/B quiescence gates precede fresh C admission. Exact H source/root and committed artifact source/context are bound; checked publication is distinct from G and the completed H view binds descriptor/root/publication. Real native receipt/plan/domain/request assignments and the one/one/one/five command counts are retained. H's two substantive G applications remain an independent canonical proof traversal, not an inference from source mentions, a descriptor inequality, or successful exit. The worker consequently returns only `PASS_PENDING_INDEPENDENT_OUTCOME_AUDIT`.
- **Failure and observation discipline.** Actual process/output pins, public CPU/cleanup/events and bounded owner-locked read-only table observations precede expected native-count/reservation predicates where available. An early missing output can prevent a later observation; retained receipts and the encompassing Job remain the cost/cleanup evidence, never a zero-work assumption. On failure the sequence stops without SQL repair, retry, renewal or additional mutable-state reads after an unauthenticated lifecycle. Outstanding descendants remain inside the finite outer Job. Coordinator accounting is captured before success predicates, and its census requires tree quiescence.

## Fixed counts and bounds

The sequence has 20 invocations: 19 installed CLIs (one build, two configurations, fourteen requests and two B service invocations) plus one A fixture service. Thirteen requests are new; one is exact byte-for-byte historical replay, with unchanged state and B work-file map and no admission-supply observation. Node stages are B bootstrap plus C bootstrap/admit/submit: four stages and eight mathematical pipeline commands. The support build is separately one stage/two compilations, not mathematical acceptance or a node-stage charge.

| Node | New requests | Node stages | Request charge | Stage charge | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| B | 6 | 1 | 320 MiB | 128 MiB | 448 MiB |
| C | 7 | 3 | 184 MiB | 384 MiB | 568 MiB |

Total charged authorization is 1,016 MiB / 1,065,353,216 bytes, without refund/renewal. B/C configurations use those exact request/stage/reservation grants and 32-MiB metadata ceilings. Real physical-supply samples are checked; they are not OS reservations.

The unchanged outer grant is 450 wall / 450 CPU seconds, 6,144 MiB, sixteen processes and 65,536-byte stdout/stderr/event. Each service gets 120 seconds, two connections, 64-MiB sends under 150-wall/120-CPU seconds, 256 MiB/eight-process supervision. Existing public peer/ordinary limits remain unchanged. Prospective endpoint retention is 1 GiB / 16,384 files / 32,768 entries; local fixture/snapshot/file-map bounds are finite. None is a measured feasibility result or transient disk quota.

The coordinator expects fourteen ordered input pins (eight execution/runtime helpers plus six historical inputs) and the launch as the fifteenth supervisor pin. The 101-file product/asset cut is separately authenticated before copying and rechecked by the worker; six coordinator/helper sources are archived, all copied product sources and historical inputs remain retained. Selected executable pins are not a claim to authenticate every runtime dependency. Actual ordered pins, fresh roots, exact product closure and launch bytes still require the forthcoming short exact-launch review.

## Handoff boundary

Proceed to a fresh exact-launch review for this final cut, then one root-owned bounded execution. Any failure must be retained; changes after a run require a new allocation and pins. A scoped outcome PASS still needs independent actual transfer/mutation/native/canonical/accounting correspondence and reachable proof-value confirmation of both G applications. No fourth-node H admission, independent hosts/installations, novelty, indefinite service, sustained useful growth or general release acceptance is supplied by this source gate.
