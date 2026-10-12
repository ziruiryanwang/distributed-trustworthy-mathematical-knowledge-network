# Aggregate execution-capsule host

Source-only snapshot/verify adapter. No build, actual aggregate image, execution,
proof or receiver authority is selected by this document. Existing module host,
producer, legacy I receipts and used evidence remain unchanged. Root owns exact
source/dependency pinning, compilation, resource selection and outcome adoption.

## Purpose

Execute a selected aggregate guest **once**, retaining the complete successful
execution as a bounded prover capsule. Later production may consume that capsule
without another whole-program execution. This adapter implements no proof stage
or automatic fallback. Saved capsules/segments/reports are untrusted proving or
diagnostic material; only a genuine full receipt verification is cryptographic
evidence, and selected-member admission additionally needs its membership check.

Link external crate `dmkn_aggregate_relation` to the independently selected
aggregate relation source, with its exact retained dependencies. Root currently
selects the exact-warrant version2 successor, retaining parse-once checking. The stable
`ConditionalConclusion` API is used directly. Source-relative
`../aggregate/receipt.rs` is reused for full I/A verification. No `ModuleID`
uniqueness rule is introduced by this host: pending receipts match exact typed
`(image,journal)` claims and actual SDK claim digests. Any graph restrictions come
from the separately selected relation, not an inferred host-side identity rule.

Required external crates are `anyhow`, `bincode`, `serde` (derive), `serde_json`,
`risc0_zkvm`, `dmkn_module_relation` and the selected `dmkn_aggregate_relation`.
SDK version and compiler/source/runtime closure must be pinned by the build owner.
No ambient `RISC0_DEV_MODE` or `RISC0_PPROF_OUT` is allowed. The enclosing trusted
owner supervises CPU, wall time, memory, filesystem/output and process closure;
this executable is not a hostile-source sandbox.

## Snapshot command

API shape, not a selected execution:

    snapshot ADOPTED_A ELF WIRE EXPECTED_HEADER CYCLES PO2 MODE
             FRESH_CAPSULE FRESH_DIAGNOSTIC RECEIPT_COUNT [RECEIPTS...]

- `ADOPTED_A`: lowercase64hex independently selected aggregate image, nonzero
  and different from fixed legacy I. `compute_image_id(ELF)` must equal it.
- `WIRE`: exact bounded version2 `DMKNAI02` bytes. The selected native aggregate relation
  must derive the exact192-byte `EXPECTED_HEADER`, including A/I/foundation/policy.
  A native conclusion remains conditional until all listed receipts are verified.
- `RECEIPTS`: exactly one genuine receipt per pending claim, in the relation's
  returned order. `receipt::verify_pending` verifies the selected I or A image,
  exact journal, fully resolved application claim and succinct-Poseidon2 scheme.
  Duplicate, extra or missing exact claims refuse; claimed success JSON is not
  accepted. Multiple member frontiers may share one exact aggregate claim.
- `CYCLES` and `PO2`: finite existing format maxima1..2^28 and12..20. These
  maxima are not runtime authority or a prediction that an input fits. Root must
  separately select a consequential finite execution and its enclosing limits.
- `MODE`: `stats` or `pc-samples`, explicitly selected. Prefer `stats` unless
  partial diagnosis of a capped run justifies same-run callback overhead.
- Outputs are absolute fresh ordinary paths with no symlink/reparse ancestry.
  Capsule and diagnostic paths must differ. Segment custody is the fresh
  directory obtained by appending `.segments` to the exact capsule path.

The host performs one `ExecutorImpl::run_with_callback`. The pinned SDK's `run`
itself delegates to this API; our callback changes only file custody, not guest
checking. Each consecutive segment is serialized into a create-new/fsynced file
with exact byte/hash binding. Its private `SegmentRef` rereads/decodes those bytes
with the same bounded bincode encoding. Limits are enforced before adding another
segment or writing bytes beyond the aggregate segment budget. No ambient SDK
temporary segment directory or unbounded callback output is used.

After successful execution require:

1. `Halted(0)` and exact expected header bytes.
2. No unsupported MMR assumptions, PoVW work or pending Keccak proof work.
   The pinned SDK keeps `pending_keccaks` private. This host uses its supported
   `coprocessor_callback` to reject every Keccak proof request; the SDK's sole
   enqueue path invokes that callback instead of adding pending work. No SDK
   rewrite or integrity-only shortcut is used.
3. Actual `session.claim().digest() == ReceiptClaim::ok(A,H).digest()`.
4. Every actual assumption is proven succinct-Poseidon2, has default zero
   `control_root` as emitted by this guest's `env::verify`, and matches exactly
   one preverified boundary claim digest. No unused or extra assumption.
5. `session.segments()` yields the complete consecutive1..128 segments under
   the selected po2. This API retains/merges the actual final journal and
   assumptions; raw callback references alone are not a complete capsule.

Only then serialize and save:

    AggregateSnapshot {
      magic: [u8;8] = "DMKNAS01", version: u32 = 1,
      session_binding: Digest, session_claim: ReceiptClaim,
      assumption_order: Vec<Digest>, segments: Vec<Segment>
    }

Fixed-integer bounded bincode, exact dependency types. Future consumers must
reject trailing bytes and mismatched magic/version. Domains are:

    session_binding = Hash(encode(
      "DMKN-AGGREGATE-SESSION-V1", Hash(ELF), A,
      I, foundation, policy, Hash(W), Hash(H), cycles, po2,
      ordered_exact_receipt_hashes))

    capsule_binding = Hash(encode(
      "DMKN-AGGREGATE-SNAPSHOT-V1", session_binding, Hash(capsule_bytes)))

This is deliberately not legacy capsule schema3. Successful stdout is the JSON
`DMKN_AGGREGATE_SNAPSHOT_RESULT_V1` with status
`UNTRUSTED_AGGREGATE_EXECUTION_CAPSULE_RETAINED`, exact A/header/capsule path,
bytes/hash/bindings, actual segment/assumption counts, one guest-call count,
zero proof calls and false `mathematical_admission`.

The existing module Producer cannot consume this capsule/header unchanged.
Later aggregate stage/producer implementation requires a fresh selection and
must bind the same exact snapshot and fully resolve all genuine assumptions.

## Verify command and stable result contract

    verify ADOPTED_A RECEIPT EXPECTED_HEADER

Only after `receipt::verify_aggregate` has fully verified a genuine, resolved,
succinct-Poseidon2 receipt for this independently adopted A and exact H does the
host emit exactly these fields:

    {
      "schema": "DMKN_AGGREGATE_VERIFY_RESULT_V1",
      "status": "VERIFIED_RESOLVED_AGGREGATE_RECEIPT",
      "aggregate_image": "<64 lowercase hex>",
      "header": [192 exact u8 values],
      "receipt_sha256": "<SHA-256 of exact input receipt bytes>",
      "receipt_bytes": <exact positive byte count>
    }

No selected-member handle or persistent acceptance credential is claimed. A
receiving controller must bind the exact expected A/H/receipt to this **same**
supervised successful call, not load arbitrary saved stdout as authority.

## Resource and diagnostic semantics

| Material | Format limit |
|---|---:|
| Exact aggregate wire |16MiB|
| Header |192B exactly|
| ELF, individual receipt, capsule, individual retained segment |64MiB each|
| All retained segment files combined |64MiB|
| Boundary receipts |0..8 exact pending claims|
| Input bytes read during preflight |512MiB total|
| Saved segments |1..128 on success|
| Diagnostic |8MiB|
| PC sample cells |131072, stride256 observed instructions|

The source bounds capsule plus segment files plus diagnostic to136MiB, excluding
owner logs/inputs and incomplete-write filesystem metadata. These are explicit
application write limits, not a hard filesystem quota or a proof of a process's
maximum memory/CPU. Root must reserve logs, runtime and diagnostic/write tails
separately. SDK/native parser and serialization temporary memory remain under
the enclosing process limit. Individual input maxima need not fit together under
the aggregate512MiB read allowance.

Defensible initial size reference: the preserved actual
`module-base-snapshot-03/evidence/base.snapshot` is21,274,865B, has110segments
and SHA256 `55eaa583ddfde8ebe827bfa941fcb81b95f9773fd2b2e295df2166501d973980`.
It occupies about20.3MiB of the proposed64MiB capsule ceiling. This is one
observed earlier capsule, not an estimate of aggregate size, a128-segment
upper bound, or justification to raise an execution allocation.

`stats` records actual whole-session rows, padding rows, instruction count and
segment count on a returned session; every saved segment records its own SDK
row/padding/instruction values. Fixed host phase timers are wall time, not CPU.
Execution-phase wall time includes segment custody. An enclosing Job/controller
accounts for full costs; do not add these overlapping phase counters to it.

`pc-samples` attaches a saturating callback to that same execution. It does not
start a second run or change the guest image. If optional sample cells fill,
unseen cells are omitted and omissions flagged; execution does not fail because
of sample saturation. Partial samples and completed segment records can survive
an ordinary capped/failed execution. Those samples are deterministic instruction
samples, not exact phase cycles or proof-production-time attribution. Raw PCs
require later exact-ELF symbolization; unknown/inlined locations remain unknown.

An execution or subsequent claim/materialization failure stays a nonzero failure
after its diagnostic is written. Final diagnostic failure also returns failure;
any capsule/segment bytes already written remain preserved and untrusted. Input
preflight failure happens before execution/segment creation and may produce only
stderr/outer supervisor evidence. Abrupt process death can prevent diagnostic
finalization. Partial segment files are not declared independently resumable
sessions or a substitute for a successful coherent capsule.

No output is deleted or overwritten. No failed operation is retried, no receipt
is invented, and no current aggregate image is presumed to exist. The host does
not hardcode old aggregate magic/version or derive claim identity from ModuleID;
the selected library determines wire/header decoding and exact claim relation.
Current selection uses192-byte `DMKNA002` headers with full exact184-byte journals
as graph/target identities. Its independent review remains a prerequisite to
selecting any guest/build/runtime. Distinct host capsule `DMKNAS01` version1 is
unrelated to aggregate statement version and binds the exact header bytes.
