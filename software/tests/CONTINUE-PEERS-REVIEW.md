# Continuation source and exact G launch review

## Verdict and scope

**PASS for the bounded, root-operated G launch review; no execution outcome is
established.** No blocking defect was found in the reviewed continuation source,
its allocation contract, or the exact G launch below. This verdict permits root
to consider the specified once-only run; it is not a claim that G compiles, that
either receiver admits it, or that the reciprocal loop has succeeded.

Reviewer: `feasibility_checkpoint_audit`. This review read all 513 source lines
of `continue_peers.py`, the complete `CONTINUE-PEERS.md`, the exact launch and
author records, relevant preparation helpers, and the installed service worker,
service implementation and public-management service wrapper. Read-only
PowerShell JSON parsing, hashes, source-set comparisons and filesystem inspection
were used. No Python execution/import/compilation, SQLite access, Lean execution,
product call, port binding or service launch was performed. The only authored
file is this review.

This is a continuation review, not a repetition of the earlier 621-pin PREPARE
outcome audit. The previous bounded preparation verdict remains in
`qualification/peer-01/PREPARE-OUTCOME.md`.

## Exact reviewed inputs

All SHA-256 digests below were independently checked against current bytes.
Paths beginning with `software/` are relative to the project root
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `software/tests/continue_peers.py` | 32116 | `eb86ae23bb95e5001d11c511754d242c4c0ca12723c321e7303c113b5e5ac554` |
| `software/tests/CONTINUE-PEERS.md` | 9984 | `9dc90f62d38245a86d55f730f78223e55b2b37e9f182404e5fa3a90dbffc157e` |
| `software/qualification/peer-g-launch-01.json` | 1665 | `663e0aeeb26e00f811770cdb7dfe847f39aea98484ca7555d8c19cb0e0b59165` |
| `software/tests/prepare_peers.py` | 25349 | `1cb723af882f4e3fbb4c65425534cdd3ac9668aecf4dfaef2c05a8ee9b33c660` |
| `D:\Python314\python.exe` | 106208 | `03168c01b7b7491423350e82c26fee71f35b43694d1319d3c668bda6903a0c38` |
| `software/qualification/peer-01/prepare-result.json` | 23416 | `1a9f6fdd9038dfb926e88aa3a689afaefc7b2c53323a023eb6da044e9a8fc6f0` |
| `software/qualification/peer-01-alpha-author/authoring.json` | 415 | `efdfaab24b1b58a44c990ecef2879efbac4a55546ae0edb18ffea461b81943f3` |
| `software/qualification/peer-01-alpha-author/G.lean` | 2739 | `a59be29d09ce29357e2c9778a2a25a56b272cad44871d0d583d2736a74aa6214` |

The phase is `g_to_beta`, the author is `alpha`, and the exact selected root is
`PeerAlpha.lift_injective_on`. Its author context is
`context:968c1489dc6c20d37a9f0888e86403a7581496d300775e8d2ff34915065ce4d8`.
The complete frozen source was read; the review does not substitute an informal
proof assessment for the allocated Lean submission.

The launch's `prepare` and `previous` select the same successful preparation
receipt. Its successful preparation launch has SHA-256
`11be3a60639cd965eafd555338909fe28cf4c628a7223f63b6d6e2aeaacb0cda`.
Helper/Python path, byte count and digest match that launch fieldwise. Object
property order is not used as pin equality.

Independent transitive checks covered **214 distinct file paths**: direct
launch pins, successful preparation launch, shared Lean executable, author
source, both installed source manifests and their selected files, both configs
and configured files, both support-build receipts, public info and author
packets. No pin mismatch or reparse ancestor was observed in that selection.
Each installed source set has exactly **96 files**, matching the coordinator's
four named top-level files, `py/*.py`, and recursive `assets`/`native` selection.
Each config has **15 configured file entries**, all checked. This is a selected
source-set check, not an assertion that arbitrary additional installation files
are inaccessible to the OS.

The mutable development checkout is not the installed input. Later development
edits to recovery modules or `software/manage.py` do not invalidate the retained
old installation bytes. This review intentionally did not demand that original
development paths in the historical PREPARE launch still equal those old pins.

Both public author packets agree with their node's prepared public info:

| Node | Context | P1 snapshot |
| --- | --- | --- |
| Alpha | `context:968c1489dc6c20d37a9f0888e86403a7581496d300775e8d2ff34915065ce4d8` | `snapshot:ff771bca6d70d5e0269f2d4495ca0501412129721400d17a36f9ea0693026ccd` |
| Beta | `context:ad8aa014eb8da4c18d4824f89d1305adf6aeecbb5361e146d88225873b383739` | `snapshot:28e8b36a32d57185ec48d5847990f931a30e7bd34e9c0b2feff406985d5a3f34` |

Alpha's `other` is loopback port 43172; Beta's is loopback port 43171. The
configuration domains name the separate installed/state/scratch roots and
shared Lean runtime. At review time, both `software/qualification/peer-01-g`
and Alpha's `scratch/services/peer-g-service` were absent. No port availability
or current public-state claim was inferred from filesystem absence. Initial
public `info` checks remain mandatory at execution.

## Lifecycle and trust-boundary reasoning

The success path contains eleven management commands, in this order:

1. Sender and receiver `info` establish agreement with the pinned predecessor.
2. Sender `submit` checks the exact frozen source hash, root and context;
   its event must report one native stage and five pipeline child commands.
3. Sender `publish` must create a new candidate-only publication; `expose`
   selects exactly that candidate. Neither allocates a new native stage.
4. Sender `serve` starts one finite session while receiver `peer_find` obtains
   the remote handle from discovery and `peer_acquire` reconstructs a new local
   candidate. Neither operation constitutes mathematical admission.
5. Receiver `info` must show its old context/description and the acquisition's
   P1 snapshot. This is an explicit pre-admission separation check.
6. The original sending service must finish and have bound quiescence evidence.
   Only then may receiver `admit` allocate its fresh, one-child native stage.
7. Final receiver `info` must agree with the actual admission and unchanged
   acquisition snapshot.

The eleven-command count includes the two initial `info` calls and the two
receiver `info` calls around admission. Exactly two native stages, one service
start and one service quiescence must be recorded before the success status.

Every public result is bound to the newly added original call directory, exact
saved request bytes, request hash in event/supervisor, response bytes/hash and
supervisor receipt. The checks require `TRANSPORT_COMPLETE`, exit zero, direct
worker reap, final Job active count exactly zero and no cleanup errors. Normal
events also identify their original directory. The fresh service session's
fixed `cases/serve` path supplies its separate original service binding.

Service readiness is the atomic local `ready.json`, bound to host, port and
catalog digest; it does not use an HTTP probe. The installed protocol creates
one connection for catalog discovery and one for bundle acquisition. The
two-request grant naturally ends after them. The review checked the installed
worker's response schema and the management wrapper's exact forwarding of its
response bytes against the coordinator's `service_finish` expectations.

For a successful phase, `service_finish` requires the expected session/view/
catalog, two connections, two completed responses, no `last_error`, bounded
charged sends, and no checker/native/mathematical-acceptance activity. A response
counter alone would not distinguish HTTP 200 from a completed error response;
here the successful receiver discovery/acquisition checks and exact descriptor
binding are additional necessary premises.

Let `S` be the successful service binding observation and `A` the receiver
admission command start. Control flow first finishes/reaps the service wrapper,
validates its original supervisor's empty Job and reaped worker, records `S`,
and only then starts `A`. The coordinator additionally requires
`A.started_offset > S.observed_offset`. Thus the claimed offline order uses
observed cleanup of the actual service tree, not a counter, vanished PID or
unbound stopped flag. Independent Win32 handle-release success is not inferred
from a `job_closed` field.

This establishes only the prospective checker's obligations. Root must audit
the actual receipts after execution; this source review is not itself a
service-quiescence or mathematical-acceptance receipt.

## Finite allocation and failure handling

The exact launch fixes ordinary commands at 500 wall seconds, aggregate active
wall and observed CPU at 1800 seconds, retained selected data/evidence at 1 GiB,
and one service at 120 seconds, two connections and 64 MiB charged sends.
The continuation wrapper allows the service command at most 180 seconds;
the installed public service supervisor grants 150 wall seconds, 120 CPU
seconds, 256 MiB and eight active processes. Readiness has a 30-second limit.
There is no extra HTTP stop, readiness request, retry, replacement source,
alternate port or restarted service.

These limits have deliberately different strength. Coordinator/direct-wrapper
wall and output checks are cooperative; there is no outer OS CPU/memory Job.
Observed CPU includes coordinator CPU and each successfully bound public Job
once. Nested native work is already included and is not summed twice. Direct
management-wrapper CPU and Jobs without bound final receipts are unmetered;
`cpu_complete=false` is retained. This is not a hard total-machine quota.

The successful retained census covers all of `product-local/peer-01` and the
current phase's evidence. Final seal/result sizes are added to the checked
bound. Shared distributions and earlier external qualification/authoring
records are excluded. This is an end-of-success retained bound, not a transient
disk cap or complete storage-cost measure. Reports explicitly stop accounting
before final serialization/write/stdout.

On failure the sequence stops without automatic admission or replay. If a
service has started, cleanup first attempts to let its already finite original
grant finish and bind that receipt. If the coordinator's own deadline or
cleanup failure prevents this, direct-wrapper kill/reap is labeled as
insufficient evidence about descendants. Root must then inspect the retained
original supervisor; no recovery qualification is implied. Prior changes,
resource charges and partial evidence are retained. An outcome after a failure
is not silently relabeled as successful merely because earlier steps completed.

## Limits of this approval

G success, if observed, is only
`G_OFFLINE_ADMITTED_BY_BETA_AWAITING_INDEPENDENT_H_AUTHORING`. H requires a
separately frozen author source and a new exact launch review. The source's H
path was read, but there is no reviewed H launch in this decision.

H's distinct-descriptor check cannot establish substantive use of G. Even
completion of both directions remains
`POSITIVE_RECIPROCAL_OFFLINE_LOOP_COMPLETED_AWAITING_DEPENDENCY_AUDIT`, with
`substantive_dependency_use_audited=false`. An independent audit must inspect
bound sources, canonical terms/dependencies and native outputs; identity
republication, unused mentions and irrelevant closure cannot stand in for
mathematical reuse.

This review does not establish full `PEER-RECIPROCITY` qualification, negative
controls, interrupted-attempt recovery, independent hosts, hostile local source
isolation, power-loss durability, usefulness, novelty, efficient retrieval,
sustained participation or exponential knowledge growth. The shared Python and
Lean distributions and owner-controlled filesystem remain trusted; executable
pins do not authenticate full transitive runtimes or prevent concurrent owner
mutation. Evidence packets are an honest-author workflow boundary, not an OS
capability boundary against reading other same-host files.

**Next permissible claim boundary:** root may execute this exact G allocation
once if inputs remain unchanged, then request a separate outcome audit. No
execution, success or broader qualification is certified by this document.
