# Post-reciprocity central controls: draft qualification contract

Status: authored, not imported or executed. Root alone may launch after source
review and an explicit allocation. Only `peer_controls.py` and this note belong
to this task. No installed files, current positive-phase sources, state,
qualification evidence or recovery code is changed by authoring this proposal.

## Gate, interfaces and source separation

The harness accepts `python -B -E -s -S software/tests/peer_controls.py --launch
ABSOLUTE_JSON`. The exact launch object has these fields:

```text
schema: 1
coordinator: FilePin of this reviewed harness
helper: FilePin of frozen tests/prepare_peers.py
python: FilePin matching successful preparation
prepare: FilePin of qualification/peer-01/prepare-result.json
g: FilePin of qualification/peer-01-g02/continue-result.json
h: FilePin of qualification/peer-01-h01/continue-result.json
limits: exact peer_controls.LIMITS record
```

The successful **schema-2 H01** status and its exact **schema-2 G02**/preparation
chain are mandatory, with phases and attempts matched to
[CONTINUE-PEERS-V2.md](CONTINUE-PEERS-V2.md). The controls launch itself remains
schema 1; it is a separate envelope, not the positive coordinator's schema.
The original replay request must be the exact `peer-h01-peer-acquire` request.
The G02 launch must preserve the failed original `peer-01-g` receipt and its
separate `OUTCOME.md`; H01 inherits G02 and has null original-history fields.
Those files are pinned/checked as history, never converted into a passing G
contribution. No author source is read or revised by controls.

Positive phases cannot consume this allocation. Existing Alpha/Beta installations and
state are selected from the actual preparation receipt, not the evolving
development `software/py` or `manage.py`. Their source/config/build/input pins
are checked. A pinned preparation helper supplies only standard-library
file/pin/census/JSON functions; no product module is imported by the harness.

The exclusively new evidence root is `qualification/peer-01-controls`.
Authoritative node mutations occur only through frozen installed `manage.py`
public requests. Existing evidence and retained files are never overwritten,
deleted or refunded. A failure stops the sequence; there is no automatic retry,
replacement server, alternate port or newly enlarged grant.

## Minimal decisive cases

Alpha is the receiver; Beta's real, previously published H view supplies the
frozen catalog/bundle. H must already have been acquired and admitted by Alpha.
No fabricated accepted state, native receipt, remote handle or canonical
mathematical package is used. The original selected bundle is capped at 1 MiB.

| Case | Required observation |
| --- | --- |
| Original H acquisition replay offline | Byte-identical stored response; historical branch; zero request/charge/stage delta |
| Unknown peer alias | `UNKNOWN_PEER`; no connection |
| Configured reviewer client using local's remote handle | `WRONG_CLIENT_HANDLE`; no connection |
| Exposure of acquired/admitted but not locally published H | `NOT_LOCALLY_PUBLISHED`; no native work or authority promotion |
| Fresh-ID exact duplicate acquisition | Successful candidate-only result, existing entry/candidate/snapshot and package path reused; new normal allowance retained |
| Coherently false advertised metadata | Real `peer_find` passes shallow catalog checks; acquisition refuses `ADVERTISED_METADATA_MISMATCH` after local derivation |
| Changed payload with original bundle digest | `BUNDLE_DIGEST_MISMATCH`, not accepted transport/candidate |
| Changed canonical object with updated outer bundle digest | Outer digest passes; original typed CID refuses `OBJECT_ID_MISMATCH` |
| Actual installed service, private database path | HTTP 404; no private bytes/checker load/native stage |
| Actual installed service, unexposed zero-digest bundle route | HTTP 404; bounded clean service termination |

The false-metadata fixture copies the real catalog and changes only advertised
`universe_arity` to another nonnegative integer. Outer descriptor/root references
and all actual bundle bytes stay consistent with each other. “Coherent” here
means coherent under the wire's structural checks, **not** consistency with the
actual declaration. The required discriminator is the real installed receiver's
successful `peer_find` followed by exact full-metadata refusal. No test-only
reimplementation substitutes for that observation.

For both tampering cases, the harness selects an actual canonical object,
independently checks its original typed digest, and changes one short CBOR
unsigned integer to another of equal encoded width. All array/byte lengths and
bundle framing remain untouched. The CID case recomputes only the advertised
outer bundle digest, retaining the original object IDs. If the real fixture
contains no suitable integer or is too large, the controls stop before any
public command; they do not synthesize a passing mathematical fixture.

## Exact accounting and state invariants

There are 12 public management commands: 11 ordinary node calls, including the
one historical replay, and one private-route service session. Ten node calls
consume new request grants: 432 MiB reserved in the current fixed configuration.
There are no new native stages or admissions. Four finite fault sessions provide
one valid duplicate bundle and three catalog-plus-bundle pairs.

Before/after each node call, read actual local SQLite projections using explicit
`Path.as_uri() + '?mode=ro&immutable=1'`, no product store import and no database
write. Only quiescent public-call boundaries are inspected. Nonempty journal,
WAL or shared-memory sidecars cause refusal; no auxiliary recovery/repair occurs.
The immutable connection assumes no concurrent writer. Root must not run another
task on these selected nodes during controls.

Check exact request and charged-byte deltas, unchanged stage count/rows, heads,
provider cuts, entries and authority-bearing record projections. Request/attempt,
remote-selection and acquisition-evidence records may grow normally. A whole
database hash remaining unchanged is intentionally **not** the invariant.
Duplicate acquisition must additionally reuse the original package path and
candidate handle. Beta's authoritative ledger remains entirely unchanged.

Each response also binds to the exact selected readonly request-ledger row:
client, request ID, deterministic key, original request bytes, terminal phase
and stored response bytes must all match. Absent/pending/mismatched rows are
preserved as failed observations, not silently accepted or repaired. These
queries are bounded, immutable reads and do not mint a request or refund a
charge. A post-call snapshot may record a pending active slot for diagnosis;
successful case predicates still require the expected cleared slot.

## Authentication and refusal accounting order

The failed first G attempt exposed a harness-ordering bug; its audit is retained
in [peer-01-g/OUTCOME.md](../qualification/peer-01-g/OUTCOME.md). Controls must not
repeat it. In particular, checking an expected refusal code or zero-stage
profile before recording actual costs would omit precisely the failed cases
that most need diagnosis.

For every completed public call, controls first authenticate the case domain,
the exact ordinary **eleven-pin set**, every selected pin against its frozen
preparation identity, source-byte totals, and the exact original launch command.
That command includes interpreter/startup flags, worker/config/state, adjacent
request/event files, working directory, non-shell launch, creation flags and
environment override. Service calls have their own exact eleven-file set.
All five declared request/command/stdout/stderr/event file records must agree
with actual presence, exact byte length and digest, including empty stderr.
Type-sensitive JSON comparison prevents Boolean/integer aliases in the command.

After IO and process-tree authentication, the harness retains quiescence on the
command record, accounts that unique Job CPU once, records actual native/checker/
pipeline observations and writes an immutable `binding.json`. Missing or
malformed counters are not invented as zeros. Before any expected-case or
aggregate-budget assertion, the request path records its actual public status/
code, measured readonly request/charge deltas, snapshots and terminal-row
correspondence in `checks/<name>.json`. A legitimate unexpected refusal thus
retains its real status, real cost and known cleanup even when the case fails.

Only afterward are expected code/status, historical branch, zero native work,
unchanged authority and exact allocation predicates enforced. Final failure
records include the observed costs and list unbound calls explicitly. Malformed
or unavailable evidence remains incomplete; this does not claim every transport
failure has complete accounting. The original wrapper `result.json` precedes
binding, while `binding.json`, per-case observations and the final/failure report
preserve the stronger later evidence without overwriting the earlier record.

Service observations follow the same ordering. Once its original Job is bound
quiescent, a later service-result mismatch does not trigger duplicate receipt
accounting or downgrade it to unknown cleanup. A genuinely unbound direct
wrapper still cannot substitute for process-tree quiescence.

Preserve baseline/final data censuses. Every preexisting non-database file must
remain byte-identical; new scratch/request/partial-package files are retained.
Charges are never refunded even when a request refuses. The final result names
the exact successful and refused replies, authentic supervisor/event bindings,
ledger deltas, source pins, selected fixtures and resource observations.

## Fault actors, offline evidence and real cleanup

Root selected the minimal trusted cooperative-thread profile for fault actors.
They import no product modules, spawn no process, expose at most two exact GET
routes, and serve only frozen bounded bytes. Each session has at most two
connections, 90 seconds wall, 4 MiB attempted output, 8 KiB request headers and
2-second socket timeouts. Explicit listener closure and actual thread join are
required. No fault-thread Job/hard memory isolation is claimed; coordinator CPU
already includes these threads and is counted only once.

During the offline replay, the stopped Beta service's actual old quiescence
receipt is checked, and the configured port is held exclusively bound without
listening. No new sender can supply the request in this honest owner-host test.
During the local-refusal tests a real fault listener is ready. Its sole accepted
connection must occur only after the fresh-ID duplicate request starts; earlier
unexpected connections make the test fail rather than disappear from evidence.

The final private-route controls run a **real installed** `manage serve`
session, not the fault actor, with exactly two requests and 60 service seconds.
Readiness comes from the real ready file, not a consuming HTTP probe. Its original
supervisor must record a reaped direct child and final Job active count zero;
actual request/response/event hashes are bound. A missing PID or stopped flag is
not used as process-tree evidence. Current `job_closed` alone does not establish
checked Win32 `CloseHandle` success.

Root's pre-execution source review strengthened the private-route assertion:
HTTP 404 alone does not imply that private data is absent from the body. Both
complete responses are now retained, and their bodies must equal exactly the
fixed public `PEER_NOT_FOUND` JSON bytes. This is a test-only change; no installed
service or executed artifact was modified.

On failure, stop/join a fault thread and try to finish the original bounded
product service allocation. Killing/reaping a direct management wrapper does
not certify its supervised descendants; unresolved cleanup is recorded as
unconfirmed and never promoted to a successful controls result.

## Allocation and incomplete-coverage label

The fixed aggregate grant is 900 active wall seconds, 900 observed CPU seconds,
1 GiB observed retained data plus this controls evidence, 12 public commands,
4 fault sessions, one two-request private service and zero native stages.
Ordinary management wrappers are cooperatively polled with 180-second command
ceilings; their existing product children have their real frozen supervision.
There is no new OS container for the coordinator or fault threads. Direct manage
wrapper CPU is unmetered, so `cpu_complete=false` remains mandatory. The shared
Lean runtime and prior qualification roots outside the selected data/evidence
census remain outside this retained-byte observation.

Same-descriptor **genuinely valid** package-variant refusal is deliberately
`NOT_EXERCISED_NO_GENUINE_SEMANTIC_VARIANT_FIXTURE`. Corrupting a package would test
integrity, not the conservative variant branch. A later independent valid
variant fixture and separately allocated case are required. Genuine original-
worker interruption/recovery also remains a separate fresh-source/fresh-state
qualification, never an opportunistic test on these positive-loop nodes.

Consequently the strongest success status is
`MINIMAL_CENTRAL_CONTROLS_COMPLETED_VARIANT_AND_RECOVERY_NOT_EXERCISED`, not an
overall all-controls PASS. It does not establish dependency usefulness,
independent hosts, source isolation, renewal, permanent availability or growth.
