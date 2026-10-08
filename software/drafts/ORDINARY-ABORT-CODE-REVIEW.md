# Ordinary-abort recovery: independent implementation source review

Reviewed 2026-09-21. Verdict: **PASS at the source-review gate for the two
replacement drafts below; no actionable defect found.** This is not an executed
contract result, native recovery qualification, integration approval by itself,
or a mathematical-acceptance claim. The product files were not changed by this
reviewer.

## Scope and immutable cut

The review read the complete OA-1 through OA-4 design review, both complete
replacement drafts, their complete diffs against the current `py` originals,
and the relevant current storage, ordinary visibility, and Windows supervision
paths. Inspection used source reads and file hashes only: no product import,
Python/Lean execution, SQL query, or preserved-evidence mutation.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `drafts/recovery_worker_ordinary.py` | 19,595 | `68D6AC7133B4DF1D58762B81BB13BCC5D3C6512969E308A01D6270589A8529BB` |
| `drafts/recovery_manage_ordinary.py` | 9,348 | `3F10850777A9F22301CD090AD131987747301A78264882AA9E302DEFA856272C` |
| `py/recovery_worker.py` (original) | 18,106 | `D5BF6E09D7E3163E8025BE59C818C6099AE537E3A3A952576B6FBF2DD7BC8C52` |
| `py/recovery_manage.py` (original) | 9,077 | `99B0CD3438607FD1BEFFBB5BBF2B07EB1F82D3868C579EFD97875437841FB7B6` |
| `drafts/ORDINARY-ABORT-RECOVERY-REVIEW.md` | 27,331 | `32996D5B591AB354D5D22BDE6DFC4B9BE4274C9BD527B16E6127EC2AF6C1E9B6` |

Paths in this report are relative to `software`. Supporting current-source pins
were rechecked and match the design-review cut:

| File | SHA-256 |
| --- | --- |
| `py/node.py` | `DC0B2E20C27290270B595122C33385D51FF629B67EF52B94B97DD8A3990F6977` |
| `py/storage.py` | `E33E61DF78984C60E60999D53DB515487E41157F29475E0CBCAF12321968637D` |
| `py/supervise.py` | `E5F35C0A88602757ECB7FF899F923F940B588E11E2A7C9C36D51FDBB2DFCAC1B` |
| `py/run_stage.py` | `2B2A33DE45490D124F0828F0E1DE15E5C57C91FACD326FD4AE054027C7952F4D` |
| `py/checking.py` | `13AFA1FA31F58F273C0364B9679FD56400587F2977EA24BDDD85AAD9471F840B` |

These draft basenames are review artifacts, not standalone launch entrypoints.
The wrapper resolves `recovery_worker.py` beside itself (wrapper line 95).
Integration must replace the two existing modules under their original names;
the current `manage.py` recovery route already calls `invoke_recovery`.

## OA-1 through OA-4 disposition

| Requirement | Source disposition |
| --- | --- |
| OA-1: explicit operation-scoped modes | Satisfied. Worker lines 29–37 and 78–91 admit only the two owner modes, with ordinary recovery restricted to `info`, `find`, `preview`, `select_context`, `admit`, `submit`, and `publish`. The source receipt's parsed operation is checked against the selected mode at lines 155–175. Main derives that mode from the already-validated raw envelope and passes it to both authentication and recovery at lines 331–344. Wrapper lines 45–62 and 99–100 validate and select the same mode; lines 145–147 require its matching worker profile. `init`, owner administration, peer operations in ordinary mode, and unlisted future operations are excluded. |
| OA-2: branch-sensitive authentication and guard order | Satisfied. Authentication of exact request/command inputs, source/config/interpreter pins, and receipt identity precedes opening state (worker lines 93–190 and 338–343). The selected indexed ledger row is bound to exact request bytes at lines 213–223. A terminal row returns bounded exact response bytes before pending-only quiescence, attempt, and active-slot guards (lines 252–264). Pending mutation requires the original attempt and repeats row, configuration, initialization, active-slot, and attempt checks inside the transaction (lines 265–283). |
| OA-3: original whole-tree quiescence authorizes pending mutation | Satisfied within the existing cooperative local Windows trust model. Worker lines 193–210 require exact true lifecycle flags, positive child identity, an integer return code, initial empty Job, final zero active processes with at least one assigned process, checked close, and no cleanup/evidence errors. Lines 230–237 bind the receipt directory to the owner attempt record created at reservation. Deliberate termination is allowed; output success is not required. No inner stage receipt, stale lock disappearance, PID absence, elapsed time, or partial checker output substitutes for this evidence. |
| OA-4: uncertainty and saturation remain distinct from refusal | Satisfied. The worker marks the write attempt before `terminal`, marks commit only after the transaction returns, and maps intervening failures to `UNKNOWN_REPLAY_REQUIRED` (lines 278–298). It does not retry a write after ambiguity. Event-persistence failure produces no successful stdout (lines 355–372). Wrapper lines 74–76 and 137–158 retain unknown-state transport failures. Current storage lines 268–303 conservatively mark failed COMMIT/unconfirmed rollback uncertain. Unsupported SQLite sidecars or unavailable terminal capacity still block; there is no repair, refund, or availability guarantee. |

## Visibility, preservation, and replay

The central ordinary-abort safety premise is supported by the current code:
`node.py:355` opens one visibility transaction containing both
`commit_operation` and `terminal`. The visible context/head, artifact, cursor,
candidate, provider/publication changes in `commit_operation` therefore cannot
become committed changes of this request while its ledger row remains pending,
assuming the documented SQLite atomic-transaction and intact-ledger model.
Filesystem preparation and charged stages may remain outside that visibility
transaction; this implementation neither consumes nor promotes those files.

The recovery write path calls only `store.terminal`, whose current implementation
at `storage.py:366` updates the selected pending request's phase/response and
clears `meta.active`. Worker lines 279–283 verify the resulting selected row and
require the entire metadata row to equal its previous value with only
`active=None`. No recovery path writes authorization, owner grants, stage rows,
heads, artifacts, provider/corpus rows, or refunds request/stage/reserved-byte
charges. Stage files, partial receipts, and an `ACTIVE.lock` are left intact.

Both original peer-only no-stage guards remain: before terminal replay and inside
the pending transaction (worker lines 250–251 and 275–276). They are bypassed
only for the explicit ordinary mode. Peer refusal bytes remain unchanged.
The extra exact-`bytes` terminal response check is a tightening, not a semantic
reinterpretation of a historical response.

Historical replay intentionally does not require the selected request to remain
active or its source receipt to authorize an abort. Thus an authenticated later
same-bytes call receipt may select an already terminal row, even when another
request is active. It cannot abort the original pending attempt because the
stored owner attempt-directory binding would fail. A historical accepted reply
is forwarded byte-for-byte by the wrapper (lines 159–162); the recovery event
continues to state that recovery has no mathematical-acceptance authority.

## Unchanged authority and bounded execution

The original public receipt still requires exactly 12 pins: interpreter,
configuration, and the same ten source files, including `checking` and
`capacity` (worker lines 112–153). Mode switching does not enlarge this pin set.
Exact command serialization distinguishes booleans from integers and requires
the isolated Python flags, original paths/cwd, and suspended process flags.

Current `supervise.py:239–266` creates the public Job before launching the
suspended dispatcher, assigns it before resuming, and records that sequence.
Its quiescence path at lines 161–201 reaps the direct child and queries final Job
activity; close is an additional checked backstop at lines 305–314.
`run_stage.py:155` enables resource/kill-on-close limits without breakaway flags.
Together these support the claimed original descendant-tree boundary on the
supported nested-Job host. They do not establish a hostile-code security sandbox
or authenticity against an owner who can rewrite trusted evidence/source files.

The worker now uses `owner_lock(..., create=False)` at line 341. Current
`storage.py:71–101` requires an existing state directory and existing lock,
opens it without creation, takes the OS byte-range lock, and only then verifies
its exact single-byte content. Missing/invalid locks do not become new recovery
authority. The state store also uses `create=False` and rejects unsupported
nonempty sidecars before opening SQLite.

The wrapper's execution pins, finite standalone owner grant, 30-second wall,
15-second CPU, 256 MiB Job, eight-process, and 1 MiB stdout envelope remain
unchanged. Its grant pins the exact raw request digest and original receipt;
successful/replayed observations must match that receipt. Recovery imports no
checker/peer execution module and allocates no native stage. This source review
does not substitute event assertions for testing those facts at runtime.

## Remaining gates

The root-owned eleven-contract suite and a separately authorized native seam
scenario remain independent gates; this reviewer did not run or certify either.
They should exercise the public authorization chain, wrong-mode receipts,
incomplete original quiescence, original-versus-later attempt selection, existing
stage preservation and unchanged peer rejection, byte-exact historical replies,
existing-lock enforcement, and persistence uncertainty. A fresh source cut after
integration must be qualified on its own; earlier native fixtures do not acquire
ordinary-abort coverage from this source verdict.

## Integrated docstring-only delta confirmation

After the source verdict was handed off, root integrated the two drafts under
their original `py` names. The reviewer compared each complete integrated file
against its pinned draft and independently rehashed the results. The only
differences are their opening module docstrings, replacing proposal/entrypoint
wording with integrated-development/native-qualification-pending wording. No
import, constant, executable statement, or control path differs.

| Integrated file | Bytes | SHA-256 |
| --- | ---: | --- |
| `py/recovery_worker.py` | 19,570 | `EB574CEC2090CE3B337E289FCDF76C230B5C5BDB9E94E2DDB9CA39ABDB99C073` |
| `py/recovery_manage.py` | 9,243 | `0E05E3A7094F8B8C1C6D241AC9F513D64533655067B9AA09C43883AFCE90CACA` |

The same source-review verdict therefore applies to this integrated code cut.
Earlier worker line references are unchanged; integrated wrapper references are
one line earlier than draft references because its opening docstring shortened.
This addendum remains source-only and was supplied before the eleven-contract
launch. Execution and native qualification remain separate evidence gates.
