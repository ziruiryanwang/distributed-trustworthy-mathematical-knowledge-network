# Actual remote-placement integration01: failed before custody

Independent outcome audit, 2026-10-21. **FAIL; no placement/discovery/admission
qualification.** This audits the one terminal execution, not a rerun. The
selection, sources, input, ledgers, failed result and consumed authorization
remain unchanged.

## Exact execution and integrity

Evidence root: `experiments/v5-local-checks/placement-network-integration-01`.
Root session 4049 exited 1. Selected adapter SHA-256:
`d71925cd57b2d3b438081bf340984bca272a409b89fec50931ea6fd86c449305`.
The source review was separate from this actual-outcome audit.

Independent SHA-256 comparison found **129/129 original physical sources and
129/129 retained source snapshots exact; 25/25 direct runtime pins exact;
123/123 staged logical files exact in both bytes and hashes** (121 product
files plus two owner query helpers). This is direct-pin integrity, not an
independent revalidation of every transitive installed runtime file.

Retained inputs independently match their selected bytes/hashes: I receipt
223594 B (`850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47`),
journal 184 B (`22fe722c57894cb192a6700954fb045a708431a1470e274440c7d60a5767b682`),
bundle 53769 B (`09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926`).
This audit did not invoke their mathematical verifier.

| Binding | SHA-256 |
|---|---|
| `selection.json` | `d9614d804e508dffd28511371a6a0e63d8712eb5ce771409562f551ffcd38d1c` |
| Adjacent `placement-network-integration-01-input.json` | `e99861ebf3b0571b3b8a019da6f3a7b97c9b20f3a44ae78a4a4b40e0747a2f8f` |
| `integration-sources.json` | `9cec6a4ab7306750d3ad7bb756fe67f1bf67ae2d253c34ddb4f603ef8b076788` |
| Outer `RESULT.json` | `8a5d37deac960baf143304873d464347ce7f119e15f312ce807fe04f6eb1aca8` |
| `placement-network-integration-result.json` | `651a83ee37bb16bb5e11297d8d6d00612522fc21c429cd1ef6655cf766687129` |

## Primary obstruction: source reply authorization cannot serve a group

The actual report stops at `remote-submit`. Read-only SQLite inspection
(`mode=ro`, `query_only=ON`, isolated stdlib-only diagnostic) finds the single
placement request in **INCOMPLETE**, with `error_type=IncompleteReadError`,
`recovery_used=0`. No arbitrary diagnostic text or token is reproduced here.

The selected source gives a deterministic configuration contradiction:

1. Adapter `integration.py:44` configures source A's lifetime reply budget as
   `HTTP.max_reply_bytes = 8 MiB`; B's later read service uses the same limits.
2. `Evidence CompositeProvider` inherits the selected delta provider's serving
   path. Its group route comes from `http_provider_receipts.ROUTES` and has
   `MODULE_MAX = 16 MiB`.
3. Before dispatch, delta `_serve` reserves the **whole route cap** and requires
   `reply_bytes + reserved_reply_bytes + reservation <= max_reply_bytes`.
   Group requests have no request-specific reservation reduction. Therefore
   even the first group request requires `16 MiB <= 8 MiB`, which is false.
4. The provider catches that failure and closes the connection without a reply.
   Placement attempts declaration acquisition first. Its `opening_max_bytes`
   65536 bounds the client, but is not sent as a server group reservation.

Thus this adapter cannot fetch its first declaration from A, independently of
the small actual opening size. This is a source-derived sufficient failure
cause consistent with the observed EOF and empty stores, not a claim that a
saved provider exception explicitly named `DELTA_PROVIDER_REPLY_QUOTA`: A's
failure-path counters/exception were not retained. The final generic
`NETWORK_WORKFLOW_OR_CLEANUP_FAILED` overwrites the adapter's earlier error
fields; the durable placement row preserves the narrower exception type.

Actual B state confirms no hidden successful partial placement:

- Intake: one request, one handler error, zero completed actions; 1333 observed
  incoming bytes and 240 attempted outgoing bytes. One 25600 B incoming and 90112 B
  outgoing application reservation remains charged.
- Placement: one grant/request/cell reservation. Nonrefundable used totals
  equal reserved totals: placements 1, index_calls 2, new_cells 1, recovery_passes 1,
  requests 3, reply_bytes 517519, storage_bytes 34138740,
  structural_bytes 17010880 and wire_overhead_bytes 98304. These are authorization
  charges, **not** observed transferred or stored bytes.
- Custody: modules/groups/names/bodies all 0; packets/offers both 0.
- Index: one initial empty snapshot; objects/postings/feature_heads/cas_nodes all 0.
- Route journal: one allocated run, zero route rows. Allocation remains
  commands 9, health 6, publish 1, stop 1, withdraw 1; one health check occurred.
  B's two locator commands were health and stop, not publication.

## Separate cleanup failure, with actual process closure

B service reports `FAILED`, solely `location_close/CLEANUP_UNCERTAIN`, and
`location_closed=false`. Intake/read/controller/journal/workspace closure all
report true. The saved underlying locator nevertheless reports closed=true,
returncode 0, channel_failed=false and forced_termination=false. R also closes
with returncode 0 and neither failure flag. This does **not** relabel service
cleanup as passing.

There is a concrete deadline-contract mismatch: service `_close` wraps the
whole `location.close()` in `cleanup_seconds + 1 = 7s`; location `_close_core`
uses its 6s budget for child teardown, then synchronously verifies its adopted
runtime in `finally`, outside that teardown budget. The actual B final runtime
check covers 5896 files/130118221 B and takes 8.0636877999641s. `close()` shields
the tracked inner task, so outer timeout/cancellation and completed inner
closure can coexist. This explains the observed uncertain wrapper result
without a leaked child; the exact caught exception is not saved, so that
specific exception attribution remains an inference from source and timing.

R's initial runtime check took 81.83818090008572s (9.5625 CPU); B's initial and
R's final checks took 7.958817099686712s and 7.190838500391692s. These retained
timings do not justify a RAM diagnosis or a new performance campaign.

The outer supervisor reports direct child reaped, Job closed, zero active and
zero terminated processes, total processes 4, no outer cleanup errors and no
termination request. The failed service observation and the successful outer
containment observation are distinct facts.

## Costs and unreached gates

Original limits remain 150 CPU seconds/300 wall seconds/512 MiB/six processes.
Measured Job CPU 34.4375s plus wrapper CPU 1.0625s gives **35.5 known CPU seconds**.
Wrapper supervision 0.5625s is already inside the wrapper figure and is not
added again. Whole-run wall 113.27331840014085s; supervised wall through
cleanup 113.07137650018558s; peak Job private commit 297517056 B. Both output
streams have zero retained bytes. No budget was renewed.

No successful submit, identical replay/status, route dispatch, source-offline
discovery, acquisition by R, receipt verification or mathematical admission
occurred. `source_closed=true` results from failure cleanup, not the intended
post-placement withdrawal milestone. `reader-workspace` and `reader-trust`
do not exist; no mathematical report exists. No new native/proof call was
made. This outcome establishes neither full-cost growth nor public TLS,
independent hosting or full v5 readiness.

The narrow next decision is a **fresh** compatible HTTP authorization and a
correct distinction between process-teardown and full-close validation
deadlines, while retaining the original outer bound and frozen failed run.
No broad campaign or new mathematical certificate is needed to diagnose these
two defects. Selection, successor review and any new execution belong to root.

## Durable-state bindings

All paths below are under the evidence root's `custodian-workspace`.

| State | Bytes | SHA-256 |
|---|---:|---|
| `placement.sqlite` |28672|`668ed41fc5a22197eed12ae659c09d5265fe71be4adbf57d93acde1725daa961`|
| `placement-routes.sqlite` |20480|`e808a0b2ab99fdbd84467d2cbe5ad2b20848361cf3c127f084b6d657bd4cbd57`|
| `modules/modules.sqlite` |24576|`ba46360c8daa00fec40afb239052f17f81f5fd5c3e15043964b99803676883ba`|
| `packets/evidence-packets.sqlite` |16384|`3fa46276c596316bdc136b71df7a7bcfedf1a99453894b8e11e563bbda9c9ef1`|
| `index/discovery.sqlite` |36864|`98446daa809e2cc670b6aaad14117b00a38ea58e94ce7f985d39fd0c6bd50cf6`|
