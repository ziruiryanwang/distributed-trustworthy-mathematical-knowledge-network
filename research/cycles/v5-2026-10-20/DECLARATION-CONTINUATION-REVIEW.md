# Exact-declaration continuation: independent source review

Reviewer: `core_growth`, 2026-10-20. Scope: the fresh implementation and the
root-owned finite-control selector in `DECLARATION-CONTINUATION-SELECTION.md`.
No Python imports, tests, native/guest proofs, RAM investigation, product edits
or Git mutations were performed by this reviewer.

## Disposition

**PASS for the selected source/protocol boundary; runtime outcome not claimed.**
No implementation defect was found. The change completes the optional
one-attempt exact-name declaration path under the same original acquisition
operation. It does not solve certification cost, establish useful-growth
economics, or make v5 release-ready.

The existing fail-stop declaration and body APIs are unchanged. Focused diffs
against `client/supplier_resilient` show only the two declaration imports and
the new source guard/client method/helper method in the fresh overlays. The
frozen predecessor transport and overlays are not edited.

## Reviewed identities

Paths below are relative to the canonical project root.

| Source | SHA-256 |
|---|---|
| `software/v5/transport/declaration_resilience.py` | `d8ee2dafc3237726501a1180ebb6b1be641ea9e5d8092c8ee841e1095da3e06c` |
| `software/v5/client/supplier_complete/workspace_evidence.py` | `2a674d313a6e114394708a02336faefc082142ea29e00d763662147696b59e6e` |
| `software/v5/client/supplier_complete/semantic_reader.py` | `7d8c93ddd7b1aabdcad6e47c864c0a8601e6e84cfbf35f1b4d02cfcc26de65fa` |
| `software/v5/client/supplier_complete/test_declaration.py` | `7101aaf574e9c6ec1a56ec4411ac23d71072719b7b255dc2913cf8a296cb7d69` |
| `research/cycles/v5-2026-10-20/Select-DeclarationContinuation.ps1` | `cc51fadd787b895f287d66e24f88835f66cc3cabef55424883d34762b5332cc9` |

Reviewed supporting seams are the existing `acquisition_resilience` binding
and settlement, `search_resilience._response`, `AcquisitionBudget`,
`_SharedAcquisition`, `EvidenceAcquisition.declaration`,
`ModuleExportAdapter.describe/resolve`, the ordinary client action wrapper and
the existing semantic reader's state transitions. This is a focused changed
boundary review, not a new audit of all predecessor assurance assumptions.

## Acceptance and recovery argument

1. **Exact request.** The transport validates the requested module identifier
   and relative name and copies the name into the fixed group-route request
   with `group_index=None`. A successful HTTP payload must be canonical JSON.
   Its opening is encoded together with that exact requested module/name,
   then passed through the ordinary adapter's `describe` and `resolve`.
   `describe` verifies the group commitment, namespace/foundation/policy and
   unique declaration selection. The new explicit locator check additionally
   requires equality with the requested module/name.

2. **Recovery ends before validation and custody.** Only the shared closed
   set of availability reasons may produce
   `UNAVAILABLE_AT_SELECTED_SUPPLIER`. Refused connection uses asyncio's
   failed-connect contract; interrupted reads must be followed by successful
   socket closure. HTTP 404/503 require the ordinary bounded parser to finish
   and the connection to close. Malformed HTTP, malformed/canonical-invalid
   successful JSON, bad openings or names, HTTP 400, cancellation and uncertain
   closure remain exceptions. A connect timeout without an acquired writer
   remains fatal rather than inventing proof of cleanup.

3. **Original ownership.** The new transport reuses the body path's exact
   acquisition/structural owner/contact/budget binding and unchanged checks.
   These preserve object identity, original deadlines, endpoint/policy,
   allowance limits and the selected source bindings before and after I/O and
   after settlement. An expired or changed contact is fatal even if the peer
   also returned an ordinary availability error. No retry, new contact,
   allowance or deadline is constructed.

4. **Custody is not recoverable.** Only a validated result reaches the client
   `put_group`, exact group/descriptor readback, acquisition liveness check and
   input-byte charge. No availability catch encloses those operations. Only
   then is a new candidate installed. The ordinary action wrapper performs
   its final active/census checks and fails the client if they fail. A
   structurally valid candidate is not mathematical authority.

The small fixed-route exchange duplicates the existing body's transport
shape because the frozen body exchange has a fixed body route. It reuses the
HTTP parser, exact-owner checks, unavailability value and reason set instead
of rebinding that frozen route or introducing a generic retry framework.

## State and resource invariants

Let `H` comprise the helper's origin candidate, name and supplier maps,
selected packet/member/group/body data, pending demands, retained byte count,
revision and ready revision. For a normally returned unavailable attempt:

`H_after = H_before` and the helper remains `COLLECTING`.

The helper charges its ordinary step and the client charges its ordinary
calls/input bytes. In particular this invariant is not a free retry. The
miss branch returns before `_remember`, `_group`, retention or candidate
installation. The caller may then explicitly request another existing
authorized supplier. The origin's provider and mathematical bytes do not
change. Cached responses retain the existing local-data semantics.

For a recoverable attempted reply allowance `M`, the transport checks:

- Original shared budget: requests increase by one, reply bytes by `M`,
  sequence by one, and no ticket remains pending.
- Original structural owner: requests increase by one, charged bytes by `M`,
  failures by one, and inflight/reserved bytes return to zero.
- Request-body/header upper bounds increase conservatively; actually parsed
  reply/header counters reflect only observed data.

Success instead charges the actual nonempty canonical reply length. Fatal
paths still settle the original ticket in `finally`; settlement is cleanup,
not permission to resume after a validation or custody exception.

## Finite selection review

`Select-DeclarationContinuation.ps1` checks the exact existing body-control
basis (`5eff81de1ed686cf3db2d6d901073f7f7070c3497762d22aef998736c4ddc4e4`),
then verifies every inherited source/runtime pin and each of four fresh,
noncolliding source paths. It requires a fresh selection and output path,
retains the isolated Python invocation and sets 20 CPU seconds, 60 wall
seconds, 128 MiB and two active processes. It creates only the selection;
it neither imports product code nor executes the controls.

## Focused control-source review

**PASS after one prelaunch assertion correction.** The original test hash
`5e08685411c2db56732986a44ae08a43d23b53ad79f9cf09fc809d3f4836f65d`
compared the real adapter's five-field locator with a three-field expected
dictionary. The reviewer identified that mismatch before execution. The
author corrected the check to compare the exact requested module/name/group
subset, retaining separate exact opening/descriptor custody readback checks.
The table above identifies the reviewed corrected source.

Logical-source mapping was traced through the fixtures: the new evidence and
reader overlays are loaded before `test_direct_contacts` and
`test_semantic_reader`. The latter reloads the same existing
`staging_members/workspace_staged.py` source but does not replace the selected
evidence/reader APIs. `supplier_resilient/test_resilience.py` is present in the
inherited source snapshot but is not imported or executed by this test.

Only seven named facade controls and three named helper controls form the
suite; inherited test methods are not enumerated. The actual loopback path
uses the new `try_resolve_declaration` through the selected validated client
inheritance chain, original contacts/budget and real SQLite custody. The
helper cases call the new `try_resolve`, with explicitly inert clients and
preexisting packet/member/group/body data. Neither fixture creates genuine
mathematical authority. Their separate scopes must not be combined into a
claim of a genuinely admitted helper context surviving supplier churn.

The output must already be an absolute resolved directory supplied by root;
the direct-contact fixtures receive that output, create fresh per-test
directories, and exclusively create the final result file. Subprocess creation
is blocked during the selected suite. Imports were inspected as definitions
and fixture setup only, not as runtime/proof launches. No predecessor suite,
native check or prover is selected.

The runtime outcome remains a separate gate. Root owns final selection,
execution, evidence adoption and source-map integration. No old campaign,
proof or product installation is renewed by this review.

## Actual outcome audit — completed once

**PASS within the reviewed changed-boundary scope.** Independently inspected
the saved outcome only; no test, import, native process or proof was rerun.
Evidence directory:
`experiments/v5-local-checks/declaration-continuation-controls-01`.

| Evidence | SHA-256 |
|---|---|
| Selected input and retained `selection.json` | `eee5ea43dc626df9754a9e695a24b51334e45ccf5066ab67b65b8540e22f1cda` |
| `RESULT.json` | `f7c24b06bbc042b0fcddfabfbb4b7e232b9c07d3d0786143f8f15d8e68263af3` |
| `controls-result.json` | `691e409aff0e726cde638235522dc3ae936b07e9d4c9e648839c3715b8dfca08` |
| `command/stderr.txt` | `82286232ceaac0c956c95767ea3c0b228202d548206f0f87781e67c8e024ff71` |

All 100 selected original files and their 100 saved source snapshots match
the selection hashes. All 19 selected runtime/input pins match. The saved
command invokes the selected snapshot's corrected test source with `-I -S -B`
and the fresh output directory. Its limits match the selection. The result's
selection digest and the retained selection digest both equal the table's
selected input digest. The seven source hashes reported by the controls agree
with the reviewed implementation, fixtures and snapshot.

The JSON report and saved test log agree: exactly the ten explicitly selected
tests ran, all passed, with zero skips, errors or failures. The log's three
asyncio slow-task notices are timing diagnostics, not test failures. Observed
scope is two real loopback requests, 18 inert streams, seven inert helper
attempts and one inert warrant sentinel. No mathematical acceptance, native
check or proof is claimed.

The decisive loopback trace records the exact `beta` declaration demand at
module `ca4cb25e726fbe3e3465cd8b176bdad3de8c23548719774500a644d13e278790`.
P's missing group returns settled `PEER_EOF`; Q supplies the 687-byte opening.
The executed assertions establish unchanged origin/candidates/custody on the
miss, then the new exact Q-bound candidate and real SQLite opening/descriptor
readback on success. They preserve the original grant/budget and inert
sentinel. The saved accounting independently agrees:

- Structural requests: two; failures: one; actual reply: 687 bytes; charged
  reply: `65,536 + 687 = 66,223` bytes; no inflight/reserved bytes.
- Shared requests: `4 prepaid + 2 = 6`; shared reply charge:
  `262,144 prepaid + 66,223 = 328,367` bytes; no pending request/reservation;
  zero verification attempts/input/CPU charges.
- Each provider records one request and zero active connections/reservations
  after its explicit stop; Q records the same 687-byte reply.

The separate helper assertions passed for preservation of preexisting
packet/member/group/body data, pending demands, retained bytes and revision,
followed by explicit Q resolution. This remains an inert helper composition
test, not a claim that a genuinely admitted mathematical context survived
the live network path. The invalid-data, custody, binding, source, allowance,
cancellation and cleanup controls all passed their expected fatal outcomes.

The enclosing run exited zero with the direct child reaped, job closed,
zero final active processes, no cleanup errors and no requested termination.
Elapsed wall time was 3.994724600110203 seconds. Recorded Job CPU was
1.546875 seconds and outer wrapper CPU was 0.484375 seconds (2.03125 combined;
the nested supervision CPU is not added again). There is no remaining run
to continue. This supports adoption of this acquisition boundary only; it
does not discharge certification affordability, useful-growth benefit or
public-release assurance obligations.
