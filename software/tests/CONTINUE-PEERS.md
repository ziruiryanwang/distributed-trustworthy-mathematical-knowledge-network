# Positive reciprocal continuation: two author-separated phases

Prospective source/allocation contract; not executed or qualified. This
coordinator implements only the positive public sequence in
[PEER-RECIPROCITY.md](PEER-RECIPROCITY.md). Full negative controls, interruption
recovery, semantic dependency audit and general deployment qualification remain
separate. Root alone launches after independent source and exact launch review.

## Interface and frozen inputs

```text
python -B -E -s -S software/tests/continue_peers.py --launch ABS_JSON

{
  schema:1,
  phase:"g_to_beta" | "h_to_alpha",
  coordinator:FilePin,
  helper:FilePin,
  python:FilePin,
  prepare:FilePin,
  previous:FilePin,
  author:FilePin,
  limits:{command_seconds:500,active_wall_seconds:1800,
          observed_cpu_seconds:1800,retained_bytes:1073741824,
          service_seconds:120,service_max_requests:2,
          service_max_bytes:67108864}
}

FilePin = {path:absolute_path,bytes:positive_integer,sha256:hex_digest}
author file = {schema:1,node:"alpha" | "beta",context:opaque_context,
               root:author_selected_Lean_declaration,source:FilePin}
```

The helper is exactly the separately pinned, reviewed `tests/prepare_peers.py`.
The coordinator verifies its bytes before loading it as a test-only module.
Its main guard is inert. Only standard-library preparation file/pin/JSON/census
helpers are reused; no product module is imported by this coordinator.
The helper and selected Python executable must be the same exact pins as in the
successful preparation launch. Earlier failed preflight launch records remain
retained historical attempts, not successful preparation predecessors.

`prepare` pins the actual successful
`qualification/peer-01/prepare-result.json`. For G, `previous` is that same pin.
For H, `previous` pins the successful
`qualification/peer-01-g/continue-result.json`. The source/config/support-build
pins are selected transitively from that exact prepared receipt, not invented
from the current development checkout. Both copied installations and their
configured Lean executable are rechecked before and after the phase.

The two exclusively new evidence roots are `qualification/peer-01-g` and
`qualification/peer-01-h`. The existing installed data roots remain
`product-local/peer-01/alpha` and `product-local/peer-01/beta`. No old run is
deleted, overwritten or automatically retried.

An independent author selects mathematics from the actual public packet/API.
The coordinator consumes the exact frozen source bytes, at most 65,536 UTF-8
bytes, and selected declaration root. It does not author, repair or substitute
source. Human intention, theorem interpretation and global unsolved-task lists
are not input fields or mathematical acceptance criteria.

If an author needs an ordinary definition's body, root may separately allocate
the public read-only inspection API before author-source freeze. Such an
approved call legitimately appends scratch evidence. Continuation therefore
does not demand the original entire data/scratch tree still match its old seal.
It preserves a new baseline inventory and checks authoritative config/source
pins and actual public context/snapshot/description against the prior receipt.
Additional unallocated head/publication changes cause refusal. Inspection is
not smuggled into the eleven-command allocation below.

## Exact per-direction sequence

G sends Alpha to Beta; H sends Beta to Alpha. Each phase has exactly eleven
public management commands and two new mathematical stage allocations.

| Command | Required observation |
| --- | --- |
| Sender `info` | Prior public head, P1 snapshot and description still match |
| Receiver `info` | Prior receiving head, snapshot and description still match |
| Sender `submit` | Exact frozen source hash/root; one stage, five pipeline child commands |
| Sender `publish` | New checked local publication; candidate-only for readers; no new native stage |
| Sender `expose` | One explicitly selected locally published result, immutable view |
| Sender `serve` | One finite supervised session, started concurrently |
| Receiver `peer_find` | Discover its previously unknown remote handle through configured alias `other` |
| Receiver `peer_acquire` | Derive/register a new local candidate from transferred bytes; no native stage |
| Receiver `info` before admission | Acquisition has not changed the receiver's head or description |
| Receiver `admit` | Sender has stopped/reaped first; one fresh receiver-local native stage |
| Receiver `info` after admission | Actual new context/description and unchanged acquisition snapshot |

The sender service is confirmed stopped between the ninth and tenth commands;
it may have naturally exited immediately after the bundle send. No stop command
or third connection is issued: the current protocol uses one HTTP connection
for catalog discovery and one for the selected bundle. Its explicit
`max_requests=2` grant then ends naturally. Readiness uses only the atomic local
`ready.json`; no HTTP probe consumes the two-request allowance. The grant fixes
120 service seconds and 64 MiB conservative send allowance, with Alpha port
43171 or Beta port 43172. The existing management supervisor adds its declared
outer service bounds. There is no restart, alternate port or adaptive grant.

Before admission the coordinator waits for the service's direct management
process to exit, validates the actual service response and original supervisor
request/response/event binding, and requires a reaped supervised worker plus
final Job active count zero. The admission command's start offset must exceed
the recorded completed cleanup observation. A stopped flag, exhausted connection
counter or missing PID alone is insufficient. Exactly two successful responses,
no reported service error and the selected catalog/view identity are checked.

Original stopped-service receipts are preserved. The runtime's `job_closed`
field is not used to claim independently confirmed Win32 handle-release success;
the independently observed zero-active process tree and direct-child reap are
the required process-quiescence premises.

## Handoff and claim boundary

G success writes `G_OFFLINE_ADMITTED_BY_BETA_AWAITING_INDEPENDENT_H_AUTHORING` and
a Beta packet containing only its actual admitted public description/context,
snapshot, exact acquired identity, installed API/command locations and evidence
pins. It contains neither Alpha's source nor a suggested H proof. Root obtains
a fresh independent H author before constructing the second launch.

H must publish a different selected descriptor from G. H success is only
`POSITIVE_RECIPROCAL_OFFLINE_LOOP_COMPLETED_AWAITING_DEPENDENCY_AUDIT`.
That status establishes the exercised public transport/admission sequence, not
that H substantively used G. Independent audit must inspect actual bound source
captures, canonical dependency terms/objects and native outputs. An unused
reference, identity republication or irrelevant closure is insufficient. Source
return hashes alone do not settle that audit.

These statuses are not an overall `PEER-RECIPROCITY` PASS. No novelty,
usefulness, retrieval scalability, sustained allocation renewal, independent
hosts, hostile-source isolation or exponential growth is claimed. Both nodes
still share trusted Python and Lean distributions on one owner-controlled host;
executable pins do not authenticate their full transitive runtimes or create an
OS visibility boundary against the old checkout.

## Evidence and finite resource accounting

Each phase preserves exact launch/author-source bytes, CLI argument arrays,
requests/stdout/stderr, actual supervisor and event pins, public handoff packets,
baseline/final data inventories and the final result. It writes no database rows
directly and makes no manual mathematical promotion. Normal public refusal and
resource charges remain part of state even on a stopped phase.

The coordinator/direct management wrappers use cooperative wall/output checks,
not an additional OS CPU/memory Job. Each ordinary command has at most 500 wall
seconds, reduced to the remaining 1,800-second active grant; the service wrapper
has at most 180 seconds. Existing product supervisors retain their own process
tree limits. Readiness is bounded to 30 seconds. Root monitors the trusted outer
coordinator and may stop it at its declared wall allocation; that does not
create a hard total-resource quota or certify descendant cleanup.

Observed CPU is coordinator CPU plus each unique successfully bound public-node
or service Job once. Nested native stages are already inside the public-node
Job and are not added again. Direct management wrapper CPU and Jobs without a
bound final receipt remain unmetered; `cpu_complete=false` is mandatory.
Observed CPU is capped at 1,800 seconds at cooperative accounting checkpoints.

The retained success census includes the whole existing `product-local/peer-01`
data tree plus the current phase's new evidence, conservatively capped at
1 GiB. It excludes the shared runtime and prior qualification/authoring records
outside those selected trees; separately allocated inspection scratch evidence
inside the data tree is included. All other allocations retain their own cost
records. The exact final
seal/result lengths are included in the final success bound. This is not a hard
transient disk quota. No cleanup or refund is performed.

An intermediate failure stops the sequence without new requests or admission.
If a service is live, the coordinator lets its already bounded original grant
finish and attempts to bind its actual final supervision. If its own deadline
or another cleanup failure prevents that, it may kill/reap the direct wrapper
but marks service-descendant quiescence unconfirmed. Direct wrapper termination
is not inferred to terminate its entire tree. All evidence/partial files remain
for root's diagnosis; no automatic recovery or replacement phase is authorized.
