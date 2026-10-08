# Owner source and capsule preparation

New source, not yet runtime-qualified. `OwnerPreparation` composes existing
SourceOperation, the owner-selected native worker, and unchanged module host.
It creates no verification handle, certificate, network request or proof campaign.
The controller is relocatable Windows Python with the adopted `-I -S -B` runtime.
It trusts the owner process, installation and filesystem. Jobs bound resources
and process closure; they do not sandbox hostile Lean/Python or restrict filesystem
and network access by owner source.

```python
from preparation import OwnerPreparation

owner = OwnerPreparation(profile, allowance, fresh_evidence_directory)
try:
    # operation is an actual SourceOperation over the SAME live ImportSession.
    authored = owner.author(operation, "author-one", cpu_seconds=60,
                            wall_seconds=120, memory_mib=2048)
    if authored["status"] == "UNTRUSTED_CHILD_REQUEST_PREPARED":
        prepared = owner.snapshot(authored["child"], "snapshot-one",
                                  cycles=2**25, po2=18)
        # prepared["session"] is input for a SEPARATELY authorized Producer run.
finally:
    owner.close()
```

Numbers in this example are interface illustrations, not a selected allocation,
cost guarantee or permission to run. Root/owner must choose actual finite limits.
No CLI or fixture-specific integration runner is added by this module.

## Owner profile

The exact keys are `schema`, `producer`, `image`, `worker`, `native_executable`,
`lean_root`, `lean_runtime_pins`, `source_pins`. Schema is
`DMKN_V5_PREPARATION_PROFILE_V1`. A file pin is exactly
`{path: absolute_path, bytes: positive_integer, sha256: lowercase_digest}`.

- `producer`: a complete existing `DMKN_V5_PRODUCER_PROFILE_V1`. Its actual
  Producer constructor loads the unchanged adopted supervisor and Job with the
  same module identities used by admission. This does not call Producer.run or
  create a proof allowance. Its two source pins must name the ACTUALLY imported
  producer.py/init paths; equal bytes at different snapshot paths are insufficient.
- `image`: adopted image-file pin, at most64MiB. The owner-adopted image ID remains
  in the nested producer profile; file SHA is not that image ID. Host execution
  and returned journal must match the adopted identity.
- `worker`: at most2MiB, exact installed sibling `authoring/worker.py` pin.
- `native_executable`: at most64MiB, `.exe`, the already adopted native frontend.
- `lean_root`: existing absolute owner-controlled Lean runtime root, with `bin`
  and `lib/lean`. The worker alone constructs its operation-local environment.
- `lean_runtime_pins`:1..128 distinct file pins below that root, including
  `bin/libInit_shared.dll`, `bin/libleanshared.dll`, `_1.dll`, `_2.dll` with their
  full `libleanshared` names, and `bin/libc++.dll`.
- `source_pins`:1..128 adopted source pins. Required installed relative paths
  under the same v5 root are `preparation/owner.py`, `preparation/__init__.py`,
  `authoring/worker.py`, `authoring/source.py`, `authoring/context.py`,
  `authoring/imports.py`, `modules/codec.py`, `modules/model.py`,
  `modules/source_rows.py`, `modules/native_rows.py`, `modules/receipt/witness.py`.
  Add other adopted transitive source/runtime pins here or to the nested producer
  runtime map. This required minimum is **not** a complete dependency-closure
  assertion; admission/transport and Python imports remain part of the trusted
  owner installation. Independently adopt the complete actual source selection
  for an integration run. It is not automatically discovered or authenticated.

Conflicting pins refuse; overlapping identical role pins are harmless. All merged
adopted pins total at most512MiB, each at most128MiB unless a smaller role limit
applies. Use applicable execution DLLs, not the entire native-link compiler/static
library manifest. Known pins are not a hermetic OS/DLL/olean proof. Profile and
allowance are privately copied; exact saved control files are rebound at stages.
Peer data cannot choose executable paths, profiles, limits or environment variables.

## Allowance and persistence

Exact allowance keys:

| Field | Bound |
|---|---|
| allowance_id | Owner-generated lowercase64hex identity |
| operations |1..16 author/snapshot calls, including refusals and demands |
| worker_cpu_seconds |1..3600 aggregate reserved/settled Job CPU |
| controller_cpu_seconds |1..600 inclusive owner-process lifetime CPU |
| wall_seconds |1..3600 from constructor entry, including idle time |
| output_bytes |128MiB..1GiB sampled total retained bytes |
| output_entries |32..4096 sampled retained files/directories |

The evidence root must be fresh and nonoverlapping adopted source/runtime/image,
supervisor installation and Lean runtime. Method names are fresh direct child
labels matching `[a-z0-9][a-z0-9-]{0,63}`. No output is overwritten or deleted.

Before each launch a create-new/fsynced reservation records exact command, limits,
deadline and prior charges. Reliable final Job accounting settles to actual CPU;
observed overshoot remains fully charged and refuses. Unknown closure/counters or
supervise exceptions retain the whole reservation, close the controller and require
explicit owner recovery. A reservation is not a proved upper bound on actual CPU:
the adopted hard Job time limit is user CPU; total CPU/wall/logs are sampled.
Any failed method closes the object. There is no retry, resume, hidden refund or
automatic fresh allowance. Saved reports cannot restore an object or its handles.

Authoring reserves96MiB beyond its saved request for up to64MiB native NDJSON,
16MiB EXPORT, logs/reports and headroom. Snapshot preparation reserves its exact
input/parent material, frame space,64MiB capsule and reporting/log headroom. The
entire evidence tree is censused, not just EXPORT. These are sampled operational
limits, not hard disk quotas against malicious source. Unexpected partial output
is preserved even if it exceeds an envelope, and success is refused.

Controller CPU includes constructor/preflight/materialization/source finishing
and unrelated owner-process work during this object's lifetime; do not add nested
supervisor CPU again. Job CPU excludes the controller. Returned/durable accounting
is observed before its last copy/report write/return; process exit and last tails
remain excluded, not zero. Constructor failures may precede a usable instance or
evidence root and must be accounted by the enclosing owner. `report()` exposes
current observations and failure/history. The owner must retain enclosing-process
costs when assessing whole-workflow economics.

## author

`author(operation, name, *, cpu_seconds, wall_seconds, memory_mib=2048)` accepts
the exact SourceOperation class. CPU1..1200, wall1..600, memory64..4096MiB.
Every subprocess Job has two active processes and1MiB per stdout/stderr stream.
Effective deadline is at most original owner deadline, method entry plus wall
limit, and the originating SourceOperation deadline. No method renews any of them.

The controller calls `operation.prepare()`. Typed `NEED_AUTHORING_CONTEXT_DATA`
returns with no subprocess or automatic acquisition. The owner must use existing
same-budget acquisition, close/recreate the unready operation after selection
changes, and stay within original allowances. A demand still counts a call and
the wall/controller cost remains spent.

A ready request goes to exactly the pinned worker under the unchanged supervisor.
The worker installs fixed Lean lookup inside that Job, because the supervisor
strips Lean environment variables. Its strict config and report schemas are in
`authoring/worker.py`; no argv/environment escape hatch is exposed. Request/config,
worker/native hashes, effective deadline, export bytes/hash and direct reaping
must agree with the same call, in addition to independent clean whole-Job closure.

Only the SAME live operation's one-shot `finish(EXPORT)` creates the returned
untrusted child request. Originating session/verifier identity, original deadline
and operation liveness are rechecked after native closure, before/after finishing,
and immediately before public return after report/census work. Late expiry writes
`FINALIZATION-FAILED.json` if a candidate RESULT already exists; that marker
overrides the candidate success. It never causes fallback acceptance.

Successful return has status `UNTRUSTED_CHILD_REQUEST_PREPARED`, `child` equal to
the existing finish result, export pin, evidence path, accounting and false
mathematical_acceptance. No receipt/handle authority is persisted by this method.
The controller never closes a supplied session, operation or verifier for the owner.

## snapshot

`snapshot(child, name, *, cycles, po2, prepare_cpu_seconds=30,
prepare_wall_seconds=60, cpu_seconds=240, wall_seconds=300, memory_mib=2048)`
accepts the existing SourceOperation.finish result, not the outer author return.
All data remains untrusted. Cycles1..2^28, po2 12..20, prepare CPU1..60, other
per-stage CPU1..1200 and wall1..600; memory64..4096MiB. Snapshot wall covers the
whole method and both commands, with an additional prepare wall clamp. No guest
execute-only warmup or repeated snapshot is performed.

The controller checks profile2/image/foundation/policy, actual local summary and
ModuleID, exact ordered distinct parent journals and receipt bytes, committed
openings, and exact rank. It serializes only child.input, and writes actual parent
bytes to separate immutable files. It cannot structurally establish those bytes
are proofs; the unchanged host must fully verify them. A cold untrusted child
request may outlive its former authoring handles because the host rechecks it.

First, host `prepare` constructs the frame and184-byte expected journal. Both
are independently compared against the exact request/summary/image/rank, as is
the preparation reply. Second, host `stage ... snapshot 0 ... parents...` performs
one actual relation execution and real parent verification. The resulting schema3
capsule, actual1..128 segment count,0..8 exact parent/assumption count and binding
are recorded. No hypothetical child segment count or fixture ModuleID is embedded.

Successful return is `UNTRUSTED_PROVER_CAPSULE_PREPARED`, containing the existing
Producer `session` shape: image/frame/expected/capsule pins, ordered parent receipt
pins, actual binding, cycles, po2, segments and assumptions. The capsule is prover
witness, not a certificate or verified module. A later separately authorized
Producer allocation must consume this exact session and discharge assumptions;
only a separate real receiving call may admit its final child receipt.

The used base-only SnapshotExistentialScreen is not invoked. No existing source,
host, relation, image, prior proof or historical failed allocation is modified.

## Focused control scope

`test_owner.py` has nine synthetic groups for structural parent binding, exact
parent-aware dispatch, shared allowance exhaustion, unknown/overshoot accounting,
worker return binding, postreport source expiry, deadline/invalid-stage refusal,
output reservation/demand behavior and constructor Path types. Native execution
is fake, capsules/receipts are nonproof bytes, and no positive handle is created.
One constructor test replaces only the Producer loader; the rest deliberately
bypass adoption constructors. These tests cannot qualify a real constructor/runtime,
source-derived child, genuine snapshot or mathematical admission. A root-selected
run and independent actual audit remain separate from source review.
