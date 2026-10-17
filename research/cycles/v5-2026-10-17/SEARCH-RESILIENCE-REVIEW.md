# Independent search-resilience review

Reviewer: `memo_independent_review`. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
This checkpoint records source inspection only. The reviewer launched no import,
test, compiler, proof, server or product operation and made no product-source or
Git changes.

## Selected source: no blocking defect found

| Selected source | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/transport/search_resilience.py` | 13,454 | `e3cf6a06ab59ac28e04411de62ae225a719c6d7d21a7ec17ae3004e735a707b1` |
| `software/v5/client/workspace_resilient.py` | 3,985 | `7c4d72143c4963b25d147496611f56858a6df361aafdc71773b3c6a1d15ab7e6` |

Read both files in full and followed the relevant inherited constructor,
`_active`, `_async_action`, `_enter`, `_fail`, located-search, HTTP framing and
SearchSession reserve/accept/abandon paths. Scope is the fresh selection in
LOCAL-RESUMPTION, not general network reliability or final-v5 acceptance.

### Same operation, not replacement authority

The facade constructs its complete existing evidence client first. It then
requires the two new source paths in the original real issuers' pins and extends
the existing origin/pin maps. The inherited mixed-client `_active` loops over
the extended maps, checks actual loaded module paths and every held owner pin,
and retains the original issuer/profile/storage/deadline checks. No temporary
live-check bypass is introduced. Workspace transfers the grant and owners only
after successful construction and OPEN recording, following the existing
constructor contract; caller cleanup remains required on failed construction.

Only the two public search methods change. Their original action decorator
still charges a call, prevents concurrent owner calls, checks liveness/census
after return and invokes the original fail-stop cleanup on any exception.
Successful recoverable returns therefore preserve the owner's existing live
warrants/context; exceptions do not acquire that privilege.

The helper requires an exact located-client/session/policy, no pending ticket,
zero reservations, unchanged adopted endpoints and owner-approved endpoint.
It snapshots session, query, clock, deadline, limits, contacts/expiries and policy
state, then rechecks them after I/O and before returning a refusal. It creates
one ordinary session ticket and never constructs a session, grant or allowance.
These are trusted serialized-process invariants, not protection against an
arbitrarily malicious Python process rewriting its private objects/code.

### Settlement and acceptance are disjoint

Let `t` be the ticket and `r` its held reservation. Before abandonment the helper
requires `pending = {t.id}`, exact ticket fields and `reserved = r`. It computes
the expected charge and checks the result of the existing `abandon` operation:

- pending becomes empty and all reserved counters become zero;
- reply bytes increase by `t.max_reply_bytes`;
- examined/candidate counters increase by their entire reservations;
- candidate scan charges increase exactly once for a candidates ticket;
- already charged request/page/provider/snapshot costs are not refunded.

The postcondition is checked against the unchanged session, not an alternative
report. Budget exhaustion at reservation, liveness failure, invalid settlement
or another unexpected local failure escapes to the ordinary fail-stop owner.
Fatal pre-accept I/O paths attempt the same conservative settlement but are
never converted into usable normal returns.

An HTTP200 body goes directly to the existing `session.accept` **outside** the
recoverable catch. Invalid JSON, invalid authenticated metadata/proofs, conflicts
and acceptance-accounting failures therefore remain fatal. Non200 bodies cannot
become summaries, candidates, mathematical warrants or coverage. Refusal reports
explicitly deny mathematical acceptance and global completeness.

### Recovery is deliberately narrow

The exact reviewed cases are an unchanged expired contact before dialing,
explicit refused connect, acquired-stream reset/broken pipe/truncated EOF,
bounded HTTP framing failures, acquired-stream attempt timeout and well-framed
400/404/503. The malformed-header conversion is limited to exact parser error
types/codes, not arbitrary exception-message prefixes.

Every acquired writer is closed and `wait_closed` must succeed within one
second before recovery can return. Close failure/timeout, cancellation and
unrecognized OS/local errors remain fatal. TLS configuration/certificate errors
are not classified as recoverable. Connect/handshake timeout or reset before
the writer is returned remains fatal; explicit connection refusal instead relies
on asyncio's failed-connect cleanup contract. Thus this is **not** general
timeout or general provider-outage recovery.

The attempt timeout is bounded by the requested cap and remaining ticket/session
time. Cleanup has a separate one-second bound, not a renewed session deadline;
post-I/O session liveness can still fail and close the owner. This is a finite
cleanup tail, not a guarantee that the call returns before the grant deadline.

Completed-response HTTP counters preserve the existing meaning. Partial physical
traffic is not fully measured; failed reservations remain conservatively charged
at the session layer. No wall-time, CPU or bandwidth saving is established here.

## Consequence and next evidence

For a caller-chosen provider sequence, if all earlier failures are in the
reviewed recoverable class, cleanup is clean, and the original finite allowance
still suffices, an eventual reachable useful provider can be attempted without
discarding live local proof context. The predecessor facade could not continue
after the first thrown provider refusal. This is a conditional operational
capability result, not global recall, availability, or positive full-cost growth.

Source review supports one small changed-boundary control allocation, not a
native/prover campaign. Focused controls must distinguish real loopback I/O from
injected failure/issuer fixtures, exercise failure-then-success in one owner,
exact charges, fatal metadata/cleanup/cancellation, and retain original grants,
deadlines and live-token mappings. Source pass is not a test or release pass.

## Final focused controls and exact plan: source clearance

Read the final test in full: `software/v5/transport/test_search_resilience.py`,
23,776 bytes, SHA-256
`21a540bd9a80fa83214ac25d184195141f8a52f146a424622cad31bf30619f52`.
Its eight methods cover the distinctions above, including full failed candidate
and interval-page reservations, one-request exhaustion before redial, acquired
versus unreturned transport failures and post-I/O invariant corruption.

The suite runs the actual new facade methods/decorator and inherited fail-stop
cleanup, but deliberately replaces facade construction, liveness/census/report,
grant and issuers with inert fixtures. Its held `LiveWarrant`-shaped entry is not
proof authority. Its search clock is synthetic; small timeout triggers use the
actual asyncio timeout mechanism. These tests do **not** qualify construction
of the new source-pin extension or a fully owned persistent workspace.

Most failure cases replace only `asyncio.open_connection` with a real reader
and inert writer, preserving real parser/settlement/acceptance logic. The one
actual socket case is two ephemeral IPv4 loopback servers and exactly three
connections: HTTP503, an honest offered snapshot and a verified candidate.
It checks clean server/handler closure, no failure-step promotion, the unchanged
session/grant/map and accumulated charge. It is not actual TLS, DHT, real
connection-reset recovery, independent-host or mathematical evidence. Existing
candidate fixture construction uses in-memory SQLite only; no predecessor test
suite runs. A Popen-denial patch covers the new suite.

Exact reviewed root selection:

- `experiments/v5-local-checks/search-resilience-controls-01-selection.json`,
  SHA-256 `6615ff9b994a2deca02556936b7a272b74beecb8796829642945eafa970f30af`.
- `research/cycles/v5-2026-10-17/Select-SearchResilienceControls01.ps1`,
  SHA-256 `ebbcc4c2443beb4159e821c6a59a370e0082736f82deea814c64241790e0870c`.
- Unchanged runner `tools/Run-V5-Check.py`, SHA-256
  `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651`.

Independently rehashed all **77 source and 18 runtime selections** with zero
mismatches. The source set exactly equals the controls author's 76-file list
plus the runner. Read-only import inspection independently checked those local
import edges, function-local imports and existing package initializers: no
missing local path was found. Dynamic supervisor imports in verifier/producer
constructors are not called by these inert fixtures. The old launcher overlay,
Node/controller runtime and native executables are neither fixture dependencies
nor selected actions. Actual loaded local origins must still be audited later.

The retained runtime pins include Python executables/DLLs and the explicit
SQLite, asyncio/socket, SSL, queue and ctypes native files. They are **not** a
hermetic manifest of every pure-stdlib file or operating-system dependency;
the unchanged runner explicitly reports this runtime scope. Runtime hashes are
checked before/after its one selected command, and selected source snapshots
are retained and checked after execution.

The selected command is isolated/no-site/no-bytecode Python on the copied test
entrypoint, canonical cwd, fresh `.../search-resilience-controls-01/controls`.
That outer run directory was absent at review. Limits are 30 worker CPU seconds,
90 wall seconds, 512 MiB, two active processes and 1 MiB for each output stream.
This is a proportionate bounded trial for eight small controls, not an upper
bound proof or success prediction. The runner accounts wrapper CPU separately;
its Windows Job/process/output containment is not a security sandbox.

**Disposition:** exact source/plan clearance for root's one selected small
invocation. No reviewer execution occurred, no prior result is repeated, and
actual success remains unobserved at this checkpoint. Failure would retain all
used bytes and evidence; it would not authorize automatic retry.

## Saved actual outcome: PASS for the selected controls

Root executed the one exact selection above. The reviewer inspected saved
`experiments/v5-local-checks/search-resilience-controls-01` only: no rerun, source
edit or evidence rewrite. The prior source-only sections record prelaunch state;
the following is the actual outcome.

All **eight tests passed**, with zero failures, errors or skips. Raw stderr lists
exactly the eight selected methods and reports `OK`; only the new suite ran.
The saved inner RESULT and stdout agree byte-for-byte except stdout's final
Windows CRLF (the saved compact JSON has no trailing newline).

Independently rebound **154 original/snapshot source identities**, all **18
runtime pins** and **76 unique imported local origins**, with no mismatch.
The complete copied file set equals the selected 77 paths. All recorded local
imports resolve inside that snapshot, including the exact helper, facade, test
and one predecessor fixture module; the runner itself is not a worker import.
Saved selection SHA and bytes match the original reviewed selection. Saved
command argv, result argv, cwd and limits agree with its substitutions.

The actual socket row records three IPv4 loopback connections: one unavailable
response and two honest responses; all server sockets closed, no handler errors.
The passing assertions establish the selected HTTP503 -> offered snapshot ->
verified synthetic candidate sequence in one unchanged search session/grant and
held map. Failed attempts remained fully charged and did not promote metadata.
Injected cases also distinguish safe settled refusals from fatal budget,
deadline, local error, cleanup, cancellation and invalid-metadata paths.

The outer result is `COMMAND_EXITED_ZERO_AND_CLOSED`, child exit 0, direct child
reaped, Job closed, zero active or terminated processes, two total processes,
no termination request, no cleanup errors and no finalization override. The
controls output contains only its RESULT; no native executable or mathematical
artifact was produced.

| Observed quantity | Value |
|---|---:|
| Worker Job CPU | 1.625 s |
| Wrapper CPU | 0.515625 s |
| Known combined CPU | **2.140625 s** |
| Total measured wall | 3.205786000005901 s |
| Peak Job private commit | 32,038,912 bytes |
| stdout | 23,425 bytes |
| stderr | 1,487 bytes |

The nested supervision CPU of 0.046875 s is already inside wrapper CPU; it must
not be added a second time. These are observed local costs, not bounds for
arbitrary corpus size or remote networks.

| Retained run-relative artifact | SHA-256 |
|---|---|
| `RESULT.json` | `4f36491b5325dade435408061ce22a7026497f1419b2058a174590852c4299a2` |
| `controls/RESULT.json` | `57519595bdfac874ae90a2281bf8a035c51d09978ad9d197416cdb3d345bb07e` |
| `command/stdout.txt` | `aacc752986a6e34331cf90beaa30589173efa65b42c608f37f7729d710989249` |
| `command/stderr.txt` | `502221449777bee0a411c8c05f849c56d36eb43a2006c022ab1aa2ef7ae32c45` |

**Adoption scope:** the selected bounded-search continuation implementation has
passing source, exact-plan and actual changed-boundary evidence. The new facade
constructor/source-pin extension remains source-reviewed, not actually
constructed with real issuers by this suite. The real socket result is local
plaintext HTTP with synthetic committed metadata; it is not TLS, independently
hosted reliability, genuine mathematics, full-cost useful growth or full v5.
No native/proof/external-network call occurred in the selected suite. Preserve
all used source, selection, tests and results; no repeat is needed.
