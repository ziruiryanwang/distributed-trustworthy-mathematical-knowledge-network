# One aggregate execution, retained for later proving

2026-10-12. Source-only investigation commissioned by root. This document
selects no build, guest, execution, proof, extra budget or deployment. It does
not edit the retained module host or the independently owned parse-once relation.

## Decision in plain language

The next useful aggregate feasibility run should also save everything needed
to prove that **same completed execution** later. Do not first run a disposable
guest screen and then repeat a passing execution merely to obtain its capsule.
The retained SDK and module host already implement the necessary mechanism.

The smallest sound successor is an aggregate-specific snapshot adapter followed
by a mechanically adapted staged producer. Reuse its execution/staging mechanics,
not its module-only statement checks. Aggregate image A, the 192-byte aggregate
header, and mixed I/A boundary receipts must remain exact throughout.

Keep four different outcomes distinct:

1. Native conditional aggregate check: mathematical relation passed assuming its
   exact listed boundary claims; no receipt authority.
2. Successful guest execution capsule: a saved prover witness; no transferable
   certificate and no receiving handle.
3. Fully resolved genuine A receipt: cryptographic evidence for its exact header.
4. Accepted selected member: genuine A receipt **plus** exact member opening and
   the receiver's selected foundation/policy/import rules.

Only the last two can participate in the corresponding certified receiving
route. A saved report, execution count or fabricated capsule is not a substitute.

## What existing source actually provides

Paths below are relative to the canonical root
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

| Existing source | Reusable property | Boundary that cannot be reused unchanged |
|---|---|---|
| `software/v5/aggregate/receipt.rs` | Full succinct-Poseidon2 verification against an independently adopted I/A image; exact journal equality; private live `VerifiedReceipt` | Not currently a built aggregate host or receiving controller |
| `software/v5/modules/receipt/src/bin/module_host.rs::stage` | `ExecutorImpl::run`, coherent saved segments and actual assumption order, then segment/lift/join/resolve/finish without a second full guest execution | `module_input`, `application`, parent checks, output reporting and 184-byte expected journal are I-only |
| `software/v5/production/producer.py` | Finite staged DAG, checkpoint reuse, before-launch reservations, actual whole-Job accounting, first-failure stop | Hard-coded 184-byte header offsets, module profile, capsule schema3 and module result markers |
| `software/v5/modules/receipt/src/trace.rs` | Exact-image deterministic PC sampling through the actual executor callback; partial samples survive execution error | Parent-free diagnostic command; does not retain a coherent proving capsule; sample saturation currently aborts execution |
| `software/v5/aggregate/input.py` | Bounded inert mixed-claim/frontier/target/witness wire generation, including retained legacy delta packet conversion | Encoding and membership checks confer no receipt authority |

Inspected source hashes:

| Source | SHA-256 |
|---|---|
| aggregate `receipt.rs` | `41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254` |
| retained `module_host.rs` | `1e30b0f2b8aee2dc26af8520172d64fd9a51ac8bebd3243b43ed0562d5cbbbe6` |
| existing `producer.py` | `5555e944d7473731e3e9095e85c5c57ce89c5f59187f78c5b248b4c1227532f3` |
| retained `trace.rs` | `e74d7392ec5ef3df8354c1ba52c7328d7af0830e5e23a1bba0dcae1cbaa0fb9c` |

The inspected SDK is the existing pinned
`experiments/general-checker-guest-01/host-prepare-01/candidate/`
`risc0-3bbcd44d6459b9ef6ac0df3846dc9215514934e8/risc0/zkvm` tree.
In its `src/host/server/session.rs`, `Session::claim` uses only unresolved
assumptions in the session output; `Session::segments` merges the journal and
actual assumptions into the last saved segment. Consequently save segments
through `session.segments()`, not by copying only raw segment references.

## Exact profile and receipt binding

Let I be the fixed existing relation image, A the independently adopted
aggregate image, H the expected aggregate header, and W the exact aggregate
wire. A is not an arbitrary nonzero token supplied by a peer.

Before execution the adapter must establish:

    compute_image_id(selected_ELF) = adopted_A
    H.aggregate_image = adopted_A != I
    H.relation_image = I
    H.foundation = adopted_foundation
    H.policy = adopted_semantic_policy
    aggregate_relation.check_bytes(W).header.encode() = H_bytes

The exact selected relation implementation must match the source compiled into
A, including the reviewed parse-once successor if adopted. Parsing or checking
W on the host does not itself certify execution under A.

For each actual `PendingAssumption` returned by that relation, supply exactly
one matching genuine receipt and call
`receipt::verify_pending(raw, pending, adopted_A)`. This performs full application
verification, not integrity-only verification, under the exact I or A selected
by the pending claim. Require the exact journal equality already implemented
there. Refuse duplicate/missing/extra receipt claims, wrong profiles, fake or
unresolved receipts, and nonselected hash suites.

Only those verified `Receipt` objects enter `ExecutorEnv::add_assumption`.
Do not pass a `ReceiptClaim` as if it were proven. Multiple selected members
may share one genuine A receipt: deduplicate by the exact claim, not by member,
path name or provider identity. The same claim has one assumption-resolution
obligation even when it supports several frontiers.

Important compatibility limit: the current aggregate relation accepts prior
aggregate headers only under the **same** A. A future changed aggregate image
A2 does not automatically accept A1 receipts. Do not erase or relabel that
boundary. Image-upgrade composition requires a separately reviewed explicit
profile relation; it is not part of this execution adapter.

## Smallest concrete host interface

Proposed fresh source, only after root selects implementation:
`software/v5/aggregate_host/aggregate_host.rs`, with the exact selected relation
library and existing `aggregate/receipt.rs` as dependencies. Do not patch the
used module host or loosen its old command's 184-byte acceptance.

Proposed command shapes (API design, not executable commands):

    snapshot ADOPTED_A ELF WIRE EXPECTED_HEADER CYCLES PO2
             FRESH_CAPSULE FRESH_DIAGNOSTIC RECEIPT_COUNT [RECEIPTS...]

    stage ADOPTED_A ELF WIRE EXPECTED_HEADER CYCLES PO2
          KIND INDEX FRESH_OUTPUT RECEIPT_COUNT [RECEIPTS...]
          CAPSULE [CHECKPOINTS...]

    verify ADOPTED_A RECEIPT EXPECTED_HEADER

The first milestone implements `snapshot` and the exact A verification helper;
its capsule format is designed for the later stage command. It must not launch
a proof or call `LocalProver::execute` first. Root can prepare W/H using the
already selected inert/native interfaces, but the snapshot host independently
binds the actual wire/header and genuine boundary receipts.

The snapshot algorithm:

1. Bounded read exact selected ELF/W/H/receipts, check adopted image and complete
   input census; perform the preflight above. Inputs are immutable pins selected
   by the enclosing owner, not executable paths chosen by remote data.
2. Use one `ExecutorEnv` with W, finite session cycles and segment exponent,
   and only fully verified boundary receipts. Add the optional bounded diagnostic
   callback to this **same** execution. No warmup, alternate branch or fallback.
3. Invoke `ExecutorImpl::from_elf(...).run()` exactly once. Require `Halted(0)`,
   exact H bytes, no unsupported MMR assumptions or PoVW work, and
   `session.claim().digest() == ReceiptClaim::ok(A,H).digest()`.
4. Collect `session.segments()`, checking consecutive index, 1..128 segments,
   and each segment's po2 no larger than the selected cap. Preserve the complete
   SDK `Segment` data, not just its digest/statistics or a native successful flag.
5. Extract actual session assumption order. Each must be a genuine proven
   succinct receipt; rebind claim digests bijectively to the preverified boundary
   set using the retained `ordered_assumptions` logic. No missing/extra claim.
6. Save the bounded capsule with create-new/fsync semantics; calculate the exact
   capsule binding from the bytes actually saved. Separately save diagnostics and
   a pinned nonauthoritative session manifest. A report failure must not destroy
   a successfully written capsule or imply it has become mathematically trusted.

The initial simple adapter can call the exact native relation again to bind
inputs on each later stage, because its public `PendingAssumption` construction
is deliberately private. This repeats bounded native preflight, **not full guest
execution**. Account for that cost explicitly. Removing it would require a
separately designed structural request decoder or frozen manifest parser, not
trusting a cached native-success flag. It is not necessary before first capsule
retention and should not trigger a broad host rewrite.

### Capsule and checkpoint identity

Keep the retained internal fields, but use an explicitly aggregate-tagged schema
that cannot be mistaken for legacy schema3, for example:

    AggregateSnapshotV1 {
      magic: "DMKNAS01", version: 1,
      session_binding, resolved_session_claim,
      actual_assumption_order, segments
    }

Use fixed bounded serialization and reject trailing bytes. Proposed domains:

    session_binding = Hash(encode(
      "DMKN-AGGREGATE-SESSION-V1", Hash(ELF), A, I, F, P,
      Hash(W), Hash(H), cycles, po2, ordered_boundary_receipt_hashes))

    capsule_binding = Hash(encode(
      "DMKN-AGGREGATE-SNAPSHOT-V1", session_binding, Hash(capsule_bytes)))

No capsule change can reuse the same checkpoint binding. Later aggregate
checkpoints likewise carry a distinct aggregate magic/version, capsule binding,
kind, index and cryptographic object. Reusing the shape of the old stage graph
does not justify labeling these as old schema5 module checkpoints.

The nonauthoritative session descriptor records image/W/H/capsule pins,
ordered receipt pins, A/I/F/P, binding, cycles, po2, and **actual** segment and
assumption counts. Never fill those counts from an expected estimate. The old
Python producer rejects this descriptor by design; introduce a narrow fresh
aggregate producer instead of reinterpreting header byte offsets in place.

### Later proving of the same capsule

The retained stages remain conceptually sufficient:

    segment_i -> lift_i -> consecutive joins -> resolve each actual assumption
              -> finish -> full genuine A receipt verification

Every stage rechecks pinned inputs, capsule binding, exact expected resolved
claim and relevant cryptographic checkpoints. `finish` must retain both the
composite check tying all segment receipts to the saved execution and the
succinct fully resolved claim check. Finally use
`receipt::verify_aggregate(final_raw,H,A)`, not module `checked_receipt`.

There is no call to the whole-program executor in these later stages. Segment
proof generation still performs the cryptographic trace/proving work required
by the SDK; "no rerun" must not be advertised as "no work to prove the trace."

For s segments and a assumptions, the retained linear stage graph has
`s + s + (s-1) + a + 1 = 3s+a` calls after the snapshot. Bounds s<=128, a<=8
give at most392. This is an operation count, not a proof-time estimate. Parallel
independent segments are possible only under a separately selected aggregate
resource budget; joins/resolutions retain their dependency order.

## Same-run diagnostics and their precise limits

The SDK already supports `ExecutorEnvBuilder::trace_callback` with
`TraceEvent::InstructionStart { cycle, pc, .. }`. `ExecutorImpl::run` consumes
that same environment. The current module diagnostic instead uses the high-level
execute-only route, which is not what the new capsule adapter should call.

Useful measurements available without changing the guest:

- Host phase elapsed time: bounded input binding, native preflight, parent receipt
  verification, guest execution, segment materialization and capsule write.
- Whole-session `row_count`, `padding_row_count`, `insn_count`, actual segments;
  `Segment::get_info()` gives per-segment row/padding/instruction values.
- Deterministic sparse PC samples from this one execution, with exact image hash,
  stride, bounded storage, count of dropped samples and cycle-reset observations.

These are different metrics. The SDK describes its own `execution_time` as
excluding memory-image hashing, and wall-time phase values are not CPU values.
The enclosing Job/controller accounting remains the cost source. Do not add
overlapping counters or convert instructions directly into proof time.

For PC sampling, reuse the existing stride256/cell131072 idea but **do not throw
when optional sample storage fills**. Saturate collection, count omissions, mark
the diagnostic incomplete and let the already bounded mathematical execution
continue. Otherwise instrumentation alone can discard a successful opportunity.
Callback overhead is real host cost and belongs to this operation's accounting.
On execution error, save partial samples when possible; no successful capsule is
fabricated and no automatic retry follows. Abrupt process death may leave no
diagnostic finalization; retain supervisor evidence instead of promising recovery.

Offline symbolization may classify samples into parsing, correspondence,
checking, commitment or SDK code only using symbols/address ranges from the
**exact selected ELF**. Stripping, inlining and optimized shared helpers may make
some attribution impossible or ambiguous. Preserve an unknown/ambiguous bucket;
sample fractions are not exact phase cycles, proof-time fractions or causal
speedups. The current guest has no explicit fine-grained phase markers. Adding
markers changes the guest image and requires its own adoption; it is not silently
included in this host-only proposal. Default to exact session statistics when
the callback's overhead or missing symbols make samples unhelpful.

## Bounds and safe failure

Carry forward finite existing ceilings as **format maxima**, not runtime
authorizations: W<=16MiB, H exactly192B, at most8 boundary receipts each<=64MiB,
ELF/capsule/checkpoint each<=64MiB, at most128 segments and512MiB aggregate input
read budget. The aggregate read cap can reject a legal combination of individual
maxima; that is intentional. Root selects smaller actual CPU/wall/memory/output
allowances. Nothing here renews the failed child screen's allocation or claims
the revised guest fits it.

`ExecutorImpl::run` uses temporary file-backed segments unless a segment path is
selected. Those transient bytes and final capsule serialization must be covered
by the enclosing storage/cleanup plan. The simple64MiB capsule route can execute
successfully yet fail final serialization/output bounds. Preserve all successful
material still available, but do not call such an operation capsule-ready. A
streaming segmented-capsule format would address that boundary if evidence shows
it is necessary; it is not a reason to rebuild the current SDK preemptively.

Successful durable snapshot reuse is an engineering guarantee under coherent
retained bytes and selected SDK compatibility, not crash-transparent resumption
of an interrupted guest. A failed/capped guest is not a completed session. Do not
claim that the proposed adapter resumes an arbitrary instruction checkpoint.

## Minimal review and implementation sequence

1. Finish independent parse-once equivalence and native changed-boundary evidence.
   Do not repeat existing mathematical authoring or base receipt production.
2. Select the exact aggregate guest source/image and this narrow snapshot adapter.
   Existing receipt verification must be compiled against the same retained SDK;
   `receipt.rs` is currently source-only, not linked by the aggregate library.
3. Review mixed I/A receipt binding, image/header checks, capsule domains and
   same-run diagnostics. Negative controls target wrong A/I, wrong header/journal,
   missing/extra/duplicate assumptions, fake/unresolved receipt, altered capsule
   and mixed checkpoint bindings. Old fabricated A values from native structural
   controls are not actual guest image identities.
4. Only if root selects a consequential finite screen, run **one** real snapshot
   on the retained genuine boundary and selected new deltas. Retain successful
   segments, statistics, capsule and all costs. Failure changes the engineering
   decision; it does not cause an automatic larger-cap rerun.
5. If the actual cost is justified, select a fresh bounded staged production
   allocation consuming that exact capsule. Complete A receiving/member/import
   integration separately; a finished producer does not create that API for free.

Open decisions remain: actual A, guest fit, safe capsule/output envelope,
whether exact-ELF PC sampling earns its overhead, independently reviewed stage
adapter/profile, mixed-boundary runtime evidence, and final receiving authority.
This memo resolves the reusable execution mechanism, not those empirical or
deployment obligations. See [affordability analysis](AFFORDABILITY-NEXT.md) for
the central cost decision; that analysis and parse-once implementation have a
separate owner and are not duplicated here.

## Root-selected source implementation, pending independent review

Root subsequently selected only a fresh snapshot/verify adapter, not a full
stage producer or any build/runtime. Source is
`software/v5/aggregate_host/aggregate_host.rs`, SHA-256
`b2cbfe362de540ec05cf1c8eed81974c4b332943c03b0fc48ad1faa7ae430742`
(18,599bytes). Exact CLI/result/capsule and resource semantics are in adjacent
`API.md`. This implementation refines the earlier plan in three concrete ways:

- Uses the existing SDK `ExecutorImpl::run_with_callback`, which `run()` itself
  delegates to, with a small private exact-hash SegmentRef. Segment custody is
  explicit create-new/fsynced files in `<capsule>.segments`, at most128files and
  64MiB total. It still collects the final `session.segments()` result; no full
  session replay is added. Partial files are not falsely called resumable sessions.
- Adds explicitly selected `stats` versus `pc-samples` mode. The default
  recommendation is exact session/per-segment statistics. Optional partial PC
  sampling is same-run and saturating, never a second diagnostic execution or
  reason to abort successful mathematics on sample-storage saturation.
- Stable verify stdout is the root-agreed six-field
  `DMKN_AGGREGATE_VERIFY_RESULT_V1` result. It appears only after full real
  `receipt::verify_aggregate`; it makes no selected-member authority claim.

The retained base snapshot was read without running it:21,274,865bytes,
110segments, SHA256
`55eaa583ddfde8ebe827bfa941fcb81b95f9773fd2b2e295df2166501d973980`.
This supports keeping a bounded64MiB initial capsule ceiling, not predicting
aggregate size or increasing any old guest allocation. Capsule+segment+diagnostic
application outputs total at most136MiB, with owner logs/input/runtime separate.

Only exact typed pending claims and actual claim digests are matched by the
host. It adds no ModuleID uniqueness/rank-equivalence rule. Root's current
aggregate semantic audit and resulting relation selection remain prerequisites
to compilation or execution; the stable ConditionalConclusion API is preserved.
This lane has run no build, test, guest, proof or Git operation.

### Exact-warrant profile and unsupported coprocessor refinement

Root selects version2 exact-warrant graph/target identities via fresh
`aggregate_claims/`: full184-byte journals,192-byte `DMKNA002` header and
`DMKNAI02` wire, same ConditionalConclusion/PendingAssumption API. The host
imports that selected crate API without embedding the old aggregate magic or
ModuleID uniqueness. Its distinct `DMKNAS01` capsule version1 stays appropriate
because its binding includes the exact header and actual adopted A.

Fresh host source after this source-only refinement is19,158bytes, SHA256
`7548e5b2092f3ece5d9ef93cef6c7ccd7d5e01ad123053f28e836558617857ca`.
The earlier source hash above was never built or executed.

Independent assurance requested explicit exclusion of pending Keccak proof work:
the SDK's `Session::claim` can specially remove that pending root, so relying
only on resolved claim equality would describe broader staging support than we
provide. `Session.pending_keccaks` is private to the SDK crate. The supported
public `coprocessor_callback` now installs an always-error callback. Assurance
confirmed from exact SDK source that the pending list starts empty and the sole
enqueue path is the callback-absent branch of `SysKeccak::keccak_prove`.
Consequently any requested Keccak proof fails earlier; no successful exported
capsule carries unhandled pending work. This performs no coprocessor proof and
changes no SDK. Actual proved-assumption bijection and MMR/PoVW refusals remain
independent checks. Assurance also confirmed `run()` delegates to the used
`run_with_callback` mechanism. Full adapter source review remains separate.
