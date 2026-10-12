# Minimal aggregate producer integration

Status: **source/theory plan, not implementation, launch clearance or funding**.
Owner: root selects implementation, exact binaries, inputs and finite runtime.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Decision and immediate purpose

Add a small aggregate-specific Python orchestrator around the reviewed
`software/v5/aggregate_production/stage_host.rs`. Reuse the existing complete
execution capsule and genuine I receipt. Do not execute the aggregate guest
again, repeat the base I proof, or rebuild the checker/proving backend.

The deliverable is a genuine resolved A receipt for the exact adopted aggregate
image and header. It is not a recipient's admission handle. The existing mixed
admission/reciprocal path remains responsible for independently verifying and
using that receipt. Producing one receipt does not close the v5 release goal.

The smallest safe reuse boundary is **composition, not a subclass invoking the
old producer workflow**:

| Component | Reuse or new work |
|---|---|
| `production.producer.graph`, `missing_plan` | Reuse unchanged. The dependency graph is identical. |
| Exact JSON, finite-number, file-pin and closure helpers in that module | Reuse unchanged under source pins. |
| `production.producer.Producer` construction | Reuse only as the already reviewed pinned supervisor/Job loader and file-check helper. |
| Existing `Producer._request`, `_checkpoint`, `_run` | Do not use. They hard-code module schema3/schema5, a 184-byte statement, old argv and text stdout. |
| New `aggregate_production/producer.py` | Own aggregate request/binding, checkpoint parser, finite stage loop and continuation report. |
| New `aggregate_production/__init__.py` | Minimal package marker/export, pinned with the orchestrator. |
| New `aggregate_production/test_producer.py` | Focused pure/fake-supervisor controls; separately reviewed before any execution. |
| Root's exact launch adapter/selection | Supply actual adopted build/screen records and finite limits. Do not copy preparation, discovery or network pipelines into the producer. |

No changes to the used `production/producer.py` or its package are required.
There are no overridable argv/output hooks in its workflow; pretending it is
generic would silently inherit incompatible checks. Reuse its small helpers
and its loader, then write the irreducible aggregate loop once.

## Source and authority boundary

The new public owner has the same small lifetime API:

```text
AggregateProducer(profile)
    .run(request) -> aggregate attempt report
    .report()     -> owner state / last refused-call observation
    .close()
```

`run` is one explicitly selected finite attempt, not an automatic campaign.
Profile/request JSON is supplied by the local owner, never selected by an
offered receipt or untrusted peer. A closed owner cannot run again.

Use dedicated aggregate schema names rather than relabeling module records:
`DMKN_V5_AGGREGATE_PRODUCER_PROFILE_V1`, `...REQUEST_V1`, `...ATTEMPT_V1`,
`...RESERVATION_V1`, `...STAGE_V1`. Exact field sets and duplicate-key rejection
are required. These are proposed controller schemas, not already implemented
wire standards.

The aggregate profile contains the pinned legacy **support profile**, the
additional aggregate source pins, adopted fixed relation image I and exact
host-build/image-adoption records. The support profile retains its real
`production/producer.py` and `production/__init__.py` source pins: its constructor
checks those paths against its own `__file__`. Its host is the adopted new
aggregate stage executable; its `image_id` is A, and its foundation/policy are
the selected F/P. Those fields are loader configuration only; no legacy
module statement routine is called. The new wrapper independently pins and
rechecks its own complete profile and sources. Keep the existing aggregate
512 MiB installation-pin envelope, counting both old and new support inputs.
These are execution dependencies and small build/adoption records, not every
compiler input. Do not put the multi-gigabyte retained SDK/rlib build inventory
into this runtime profile; the separately adopted build record binds it.

The request retains the useful existing shape:

```text
schema, allowance_id, session, checkpoints, output_directory,
stage_limit, budget, prior_attempts, carried_external_costs
```

The aggregate session instead contains:

```text
image, wire, expected, capsule, parents,
session_binding, capsule_binding, cycles, po2, segments, assumptions,
snapshot_evidence
```

The four file inputs and each ordered parent use exact path/bytes/SHA-256 pins.
`snapshot_evidence` identifies the exact adopted inner screen result and its
enclosing selection/closure record. Their concrete parser must match the actual
root-selected screen, not assume that an arbitrary saved `PASS` is adoption.
Bind the source-map/build, actual ELF/image result and successful screen to the
same A. The snapshot relation remains untrusted until genuine proof production.

The profile identity covers actual host/source/runtime pins and adopted A/I/F/P;
the session identity covers content pins, ordered parents, selected cycle/po2
limits, both reported bindings and actual s/m counts. Content identity may omit
file paths to permit relocation; the active request still checks each actual
path and its bytes. A continuation uses the same adopted profile identity.
Cross-host-version checkpoint compatibility requires a separate explicit owner
decision; the first implementation must not infer it from matching schema names.

## Exact native interface and statement

The reviewed stage executable accepts:

```text
stage ADOPTED_A ELF WIRE EXPECTED_HEADER CYCLES PO2
      KIND INDEX FRESH_OUTPUT RECEIPT_COUNT [RECEIPTS...]
      CAPSULE [REQUIRED_CHECKPOINTS...]

verify ADOPTED_A RECEIPT EXPECTED_HEADER
```

For each stage, generate that exact argument order. No automatic snapshot,
native build, guest execution, proof fallback or verification retry is present.
`verify` is the independently usable recipient-side command, not another
mandatory producer stage after already verified `finish`.

H is exactly 192 bytes: **`DMKNA002`, version2**; A at12..44, I at44..76,
F at76..108, P at108..140, member root at140..172, member count at172..176,
maximum member rank at176..184, seal height at184..192. The controller checks
the selected A/I/F/P and layout, A distinct from zero/I, member count1..48 and
positive seal height, matching **`aggregate_claims/header.rs` and
`aggregate_claims/bindings.py`**. The host recomputes the selected native
aggregate relation from WIRE and demands its complete derived H, not only
those fields. The previous `aggregate/header.rs` and `aggregate/bindings.py`
define incompatible v1 semantics and must not supply this controller's H checks.

Members are exact 184-byte `DMKNM002`/version2 journals J, not deduplicated
ModuleIDs. The selected v2 relation keys graph members and premises by complete
J bytes, requires exact checked delta premises and mathematical ranks, and
commits to sorted unique complete J values. Different J warrants can describe
the same semantic ModuleID. Its Merkle domains are
`DMKN-V5-AGGREGATE-V2\0LEAF\0`, `...\0NODE\0` and `...\0ROOT\0`;
membership openings bind the exact J. Counts do not count semantic novelty or
growth. The producer passes the adopted WIRE/H unchanged rather than rebuilding
their members or roots using the legacy module-keyed aggregate helpers.

Do not reinterpret the 184-byte module statement as H. A and I have distinct
roles. The only currently supported parent profile is fixed I / same adopted A;
multi-image semantic compatibility and revocation remain separate work.

The existing snapshot stdout already reports:

```text
DMKN_AGGREGATE_SNAPSHOT_RESULT_V1
UNTRUSTED_AGGREGATE_EXECUTION_CAPSULE_RETAINED
aggregate_image, header, capsule_path, capsule_bytes, capsule_sha256,
capsule_binding, session_binding, segments, assumptions,
mathematical_admission=false, proof_calls=0, guest_execute_calls=1
```

For the selected screen, the enclosing result must also be the adopted
`PASS_ONE_AGGREGATE_EXECUTION_CAPSULE_ONLY`, with actual clean closure and no
overriding finalization failure. At plan-writing time this document does not
assert that the new optimized screen has passed or that its s is known.

The host independently recomputes, using its pinned fixed-integer bincode:

```text
session_binding = Hash(encode(("DMKN-AGGREGATE-SESSION-V1",
    Hash(ELF), A, I, F, P, Hash(WIRE), Hash(H), cycles, po2,
    ordered_parent_receipt_hashes)))

capsule_binding = Hash(encode(("DMKN-AGGREGATE-SNAPSHOT-V1",
    session_binding, Hash(complete_capsule_bytes))))
```

Python must not substitute its own JSON serialization for those encodings.
It compares exact bindings from adopted snapshot evidence and each stage;
the native host computes and enforces the authoritative operation relation.

## Complete capsule reuse and finite stage graph

The capsule is complete `DMKNAS01`, version1, including all consecutive segment
records, target claim and exact assumption order. Partial segment files, an old
module capsule, or a success report without the capsule do not suffice.

The host verifies all ordered supplied parent receipts, checks the exact target
claim and session, and derives actual counts s in1..128 and m in0..8. Require
`assumptions == len(parents) == m`, not the legacy producer's weaker inequality.
The host's exact native pending-claim order governs receipt order; no Python
sorting or deduplication may change it. That argument order is distinct from
the complete capsule's SDK assumption-digest order: the host verifies the
pending claims, then maps their verified claim digests into the capsule order
before `resolve:j`. The controller must not assume the two orders coincide.

| Stage | Count | Exact prerequisites |
|---|---:|---|
| `segment:i` | s | No checkpoint. Complete capsule still supplied. |
| `lift:i` | s | `segment:i`. |
| `join:i`, i=1..s-1 | s-1 | Previous prefix and `lift:i`. |
| `resolve:j`, j=0..m-1 | m | Full prefix for j=0; otherwise `resolve:j-1`. |
| `finish:0` | 1 | All s `segment:i` checkpoints and final resolve; full prefix when m=0. |

Prefix0 is `lift:0`; prefix i>0 is `join:i`. Therefore a fully fresh graph has
`s+s+(s-1)+m+1 = 3s+m` host commands and `3s+m-1` prover operations.
Finish verifies; it does not call a prover. Track attempted host calls, planned
prover-stage invocations and successfully reported prover calls separately:
a failed process may stop before the SDK prover call, so its exact internal
extent cannot be invented.

The retained `missing_plan(s,m,inventory)` computes the needed dependency closure
from finish. **Every segment checkpoint must survive until finish even if a
higher join/resolve checkpoint exists.** Pruning those segments loses inputs
required for complete composite verification. As a graph property, a missing
segment can be regenerated without regenerating a surviving accepted higher
prefix. This is **not** automatic same-allowance loss recovery: the continuation
rule below requires every previously successful checkpoint's exact pin. A lost
or replaced prior-success file therefore refuses ordinary continuation and
requires a separate explicit owner recovery decision that preserves spent
costs. The first controller need not implement replacement records. This plan
does not select deletion or recovery of any retained checkpoint.

Every stage performs zero new whole-session `ExecutorImpl` acquisition calls.
`prove_segment` still performs the SDK's segment witness/preflight computation;
it is real charged proving work, not free capsule playback.

## Checkpoint and output binding

Implement only the small new envelope parser. Aggregate checkpoint offsets are:

```text
0..8           magic "DMKNAP01"
8..12          little-endian u32 version1
12..44         capsule-binding digest
44..52         little-endian u64 kind-string length n
52..52+n       ASCII kind, 1<=n<=7
52+n..56+n     little-endian u32 index
56+n..64+n     little-endian u64 payload length
64+n..EOF      nonempty payload of exactly that declared length
```

Read a prefix of up to71 bytes and require its actual length to be at least
64+n; a maximum-length kind needs71 header bytes. The old 64-byte module-header
read is insufficient. Require an allowed nonfinish kind,
the exact requested stage key, exact total file length and capsule binding.
The legacy schema5 envelope starts eight bytes earlier and must refuse.

This framing is **not authenticated** and does not bind source/profile identity.
Anyone can reframe bytes. The host verifies actual cryptographic payloads, exact
claims and final application receipt; the owner selects which source/profile
may consume them. Neither a matching envelope nor a saved host log is proof.

Bind the exact one-object JSON stdout contract from `aggregate_production/API.md`:
schema/status, kind/index, A, H SHA-256, both bindings, s/m, output bytes/hash,
`application_receipt_created`, `guest_execute_calls`, `proof_stage_calls`,
`mathematical_admission`. Reject extra/missing/duplicate fields, mismatched types,
trailing non-JSON, unexpected statuses or count changes.

Nonfinish expects `REAL_AGGREGATE_CHECKPOINT_NOT_APPLICATION_RECEIPT`,
`application_receipt_created=false`, `proof_stage_calls=1`. Finish expects
`REAL_AGGREGATE_RECEIPT_FINISHED`, true,0 respectively. All successful stages
expect `guest_execute_calls=0` and `mathematical_admission=false`.

Promote an output into the inventory only after zero exit, clean known Job
closure, exact output pin, JSON binding, input/source rebinding and finite
output census. A nonzero exit never promotes bytes even if a file was written.
Finish verifies complete composite integrity, exact `ReceiptClaim::ok(A,H)`,
all resolved assumptions and the serialized non-dev Poseidon2 receipt before
writing it. The producer must not weaken that native contract.

## Attempt state, failure and continuation

```text
PINNED REQUEST
  -> FRESH ATTEMPT + DURABLE CONTROLS
  -> RESERVED STAGE -> SUPERVISED CALL -> BOUND CHECKPOINT
                         | failure/unknown closure
                         v
                    STOP AND RETAIN COSTS
  -> FINAL REBIND + CENSUS -> PREFIX or FINISHED RECEIPT
                         | finalization failure
                         v
                    FAILURE OVERRIDE / OWNER RECOVERY
```

Preserve the existing useful accounting semantics, but with aggregate schemas:

1. Fresh exclusive attempt/stage paths, immutable profile/request copies and a
   reservation before each process launch. No in-place overwrite or retry.
2. Reserve the next worker CPU envelope and output/diagnostic space before launch.
   Enforce finite CPU, wall, memory, process, stdout and stderr limits.
3. On known clean closure, charge measured inclusive Job CPU. On uncertain
   closure, retain the reservation, flag cost/closure unknown, stop and close
   the owner. A reservation is not proof of a real upper CPU bound when closure
   is unknown.
4. Stop at first stage failure. Preserve successful checkpoints, partial outputs,
   diagnostics and all failed costs. Never relabel a failed attempt as success.
5. Final binding and output census must succeed; an explicit
   `FINALIZATION-FAILED.json` overrides any earlier success record.
6. A new owner-authorized request can continue a known, correctly finalized
   failed/prefix attempt in a fresh directory. It supplies complete ordered
   same-allowance history, unchanged session/profile/budget/carry records and
   every previously successful checkpoint. Charges accumulate; limits do not
   silently renew. Unknown closure or failed finalization requires a separate
   recovery decision, not routine resume.

Use an explicit per-attempt stage limit. The maximum fresh graph has392 commands
and391 checkpoint outputs, but these are schema ceilings, not a proposed run.
Finite prior-record count/byte bounds remain required. Saved owner JSON is
bookkeeping, not a globally tamper-proof budget ledger; the in-memory history
only additionally prevents omission during that owner's lifetime.

Account for refusals before a safe attempt directory exists. The old
`report().last_call_failure` observes them but is not a durable complete ledger.
For the selected real campaign, require the enclosing owner to reserve and
record the controller process before invocation and retain its terminal outcome,
including constructor/preflight refusal. This avoids adding another broad
accounting service while making the known boundary explicit. The outer
reservation/result and inner attempt are complementary, not summed twice.

## Finite cost and feasibility before funding

Let M be the missing-stage set for a selected capsule/inventory. For each stage
k, select finite worker CPU u_k, wall w_k, memory r_k, output/log byte e_k and
process limits. These are explicit request limits below reviewed ceilings,
not empirical success predictions. Let C_old denote retained prior charges,
C_ctl the new controller envelope and C_outer the nonoverlapping outer cost.
A conservative planned CPU allocation satisfies:

\[
B_{\rm CPU} \ge C_{\rm old}+C_{\rm ctl}+C_{\rm outer}
  +\sum_{k\in M_{\rm selected}}u_k.
\]

A partial prefix may be selected if the full missing graph does not fit, but
must not be presented as a completed receipt. With an adopted s and m, root
should first check feasibility for the complete intended path, including finish
and reporting tails, before selecting any prefix proof investment. No finite
allowance guarantees successful proof completion.

Actual stage cost includes repeated native relation evaluation and image
computation, all parent receipt checks, complete capsule reading/decoding,
dependency checkpoint verification, SDK proving or finish verification,
artifact writes, diagnostics and closure. Symbolically:

\[
C_{\rm new}=C_{\rm ctl}+C_{\rm outer}
 +\sum_{k\in M_{\rm attempted}}
 (C_{\rm preflight,k}+C_{\rm parents,k}+C_{\rm capsule,k}
  +C_{\rm checkpoints,k}+C_{\rm crypto,k}+C_{\rm IO,k}).
\]

Screen/build/earlier-failure costs remain separately carried in full-workflow
accounting even though the next-stage incremental decision does not redo them.
Do not add measured nested worker CPU twice to an inclusive outer Job total.
The old producer reports pre-final-report controller time, excluding startup,
exit and post-observation tails. The outer record must close those boundaries
or the cost remains explicitly partial. No profitability or speedup follows
from these formulas alone.

Host limits: each ELF/capsule/checkpoint/receipt/output <=64 MiB, WIRE<=16 MiB,
H=192 bytes, all input reads per stage<=512 MiB. Cycles<=2^28 and po2=12..20
are format maxima only. The next exact session uses its adopted values, not
these maxima as permission. Its prospective screen currently selects2^25/18.

Before funding, calculate both the maximum per-call read set and total retained
inventory/output envelopes. Finish reads s segment proofs plus one final
succinct proof, in addition to ELF/WIRE/H/capsule/parents. An admissible s does
not imply that 512 MiB reads or a 2 GiB controller output ceiling will suffice.
Reject an unfundable configuration; do not silently raise limits or delete
needed segments. Rehashing the full inventory per stage is also real controller
cost; for the first small selected capsule use bounded measured inputs and do
not assert global-size independence for this implementation detail.

Nested SDK decoding has no proved total-heap/recursion bound; finite memory
supervision remains necessary. Windows Jobs provide resource/process control,
not a hostile-source security sandbox. No network or arbitrary source execution
is introduced by this producer plan.

## Focused verification and actual prerequisites

First review source and pure controls for graph counts/order, m=0/s=1/maxima,
graph-only missing-segment planning despite surviving join, ordinary-resume
refusal after loss of a prior-success checkpoint, old/new framing rejection,
71-byte header handling, exact JSON/argv, profile mutation, unordered parents,
aggregate/module header confusion, source/session mismatch, refusal/failure
charges, first-failure stopping, and failed-finalization override. Use a fake
supervisor only to test control flow; never advertise mock receipts as real.

Actual production needs all of the following fresh root selections:

- Adopted exact aggregate ELF and A plus the complete successful screen capsule
  and its actual s/m/session/capsule binding. Do not execute the guest to recover
  data already retained in a complete accepted capsule.
- Adopted exact stage-host build from reviewed `stage_host.rs`, retaining the
  selected native relation/checker and backend dependencies. No duplicate base
  checker/backend build is part of this plan.
- Reviewed new aggregate controller and focused changed-boundary controls.
- Exact genuine I receipt already retained at
  `experiments/v5-local-checks/module-base-production-01/finish-0/receipt.bin`,
  SHA-256 `850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47`.
  Reverify it as a premise where the host requires; never prove it again.
- A finite full-path funding/retention decision based on actual s and artifact
  sizes, followed by bounded stages and independent actual outcome review.

After a genuine final receipt is adopted, use the already separately reviewed
reciprocal harness and actual aggregate admission APIs. Do not grow this
producer into an alternate discovery, source-authoring or deployment system.

## Inspected basis and unresolved facts

Source basis: `aggregate_production/API.md` and `stage_host.rs`, complete
`production/producer.py`, `aggregate_host/snapshot.py`, snapshot JSON emission in
`aggregate_host/aggregate_host.rs`, and current aggregate layout/semantics in
`aggregate_claims/header.rs`, `bindings.py`, `membership.rs`, `relation.rs` and
`wire.rs`. This checkpoint writes no implementation and executes
no source, test, compiler, guest, prover or Git operation.

### Corrected predecessor-confusion audit

Root caught an error in the first plan revision: its H paragraph cited legacy
`aggregate/bindings.py` and `DMKNA001`/v1. This revision corrects that error, not
the protocol. The first document hash `8e1d19ed...` is not implementation
authority. A follow-up source trace checked the other layer/version boundaries:

| Boundary | Actual selected authority and required value |
|---|---|
| Python snapshot preparation | `snapshot.py` imports **`aggregate_claims.bindings`**, not `aggregate.bindings`. |
| Native aggregate library | Retained `proof-validation-integration-build-01` command compiles `source/software/v5/aggregate_claims/lib.rs`; its source map binds v2 header/wire/membership/relation. |
| Snapshot/stage native linkage | Snapshot host's retained command links that exact `libdmkn_aggregate_relation.rlib`; stage builder preserves those externs. Both Rust hosts import `dmkn_aggregate_relation::{header,relation}`. The crate name alone does not select a source version. |
| Shared receipt helper | `aggregate/receipt.rs` is intentionally reused. It imports the externally selected crate's `Header`/`PendingAssumption`, so its directory name does not imply use of legacy `aggregate/header.rs`. |
| Aggregate H / input WIRE | H=`DMKNA002`/2/192 bytes; WIRE=`DMKNAI02`/2. Snapshot explicitly checks the latter before rebinding only the A slot. |
| Member J | `DMKNM002`/2/184 bytes; exact complete warrant bytes, not semantic ModuleID alone. |
| Snapshot capsule | `DMKNAS01`/1 remains correct; both Rust hosts use identical fields/encoding. It is not H's version and must not be changed to2. |
| Stage checkpoint | `DMKNAP01`/1 remains correct; dedicated framing is independent of H's version. |
| Snapshot/stage JSON and digest domains | Their documented `_V1` schemas and `...-V1` binding domains remain correct; changing H does not rename them. |
| Legacy producer | Module capsule3/checkpoint5/184-byte journal remain incompatible workflow inputs. Only pure helpers and pinned loader are reused. |

The source trace uses the retained source-map/compile-command records; it does
not execute native libraries or prove compiler correspondence. Build adoption
must still bind the exact selected library bytes and their reviewed sources.
The bounded-parse guest optimization must preserve this same v2 relation;
similar filenames or a valid ELF image do not establish that correspondence.

Independent source-loop review separately identified the missing-checkpoint
versus routine-resume distinction, corrected above. It found no additional
concrete composition/graph/argv/JSON blocker and records its review in
`AGGREGATE-PRODUCTION-SEAM.md`. This is source review, not a test outcome.

Unknown until the live independent build/screen adoption: successful new A,
actual s/capsule size, feasible finite stage costs and exact output pin set.
The plan resolves the controller seam; it does not assert those results or
select proof funding in advance.
