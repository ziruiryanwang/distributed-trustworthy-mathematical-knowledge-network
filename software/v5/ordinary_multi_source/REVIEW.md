# Independent review: bounded multi-source ordinary receiving

2026-10-26. **Contract GO; implementation, test and exact execution selection
remain unreviewed.** Source-only review: no product import, runtime, state API,
database, network, native check or Git mutation. Root owns selection/adoption.

## Contract challenge

Read CONTRACT and the adopted payoff/challenge notes. Confirmed the current
receive source's four acquisition sites bind every demanded object to one
discovery provider, while the lower acquisition API already accepts per-object
providers under one OrdinaryBudget. Optional public composition is a real gap;
it is not a new mathematical acceptance mechanism. Manual complete-mirror
selection or an ordinary approved library import remains preferable when enough.

No architectural blocker found in the selected minimal contract. Successful
exact preview/locator/evidence validation fixes the mathematical inputs before
the existing preflight and sole admission. Changing their transporting supplier
therefore adds availability opportunities, not a warrant. This argument assumes
the unchanged hash/checker/protected-state boundary and does not establish
availability for a missing preview or missing dependency, or Byzantine liveness.

The declared source list replaces acquisition order without altering discovery
origin. One original ledger, parent and fixed network deadline prevent provider
switches from renewing authority or resources. The per-attempt cap plus remaining-
source time division is a conditional opportunity bound: synchronous local work
and final proof checking remain costs, and failed reply-cap charging can correctly
leave no budget for another source. No network-size scan or proof-speedup follows.

## Consequential implementation seams to check

- The default signature/config/report path retains old semantics. All three
  optional fields are required together; labels are distinct existing contacts,
  at most eight, with strict non-boolean integer time limits and no implicit
  source expansion.
- H classifies only inside network exchange after endpoint/request/TLS setup.
  Only its own timeout-manager expiry or enumerated connection/EOF exceptions
  qualify; bare TimeoutError, TLS errors and cancellation do not. Existing close
  cleanup remains outside retry classification.
- O catches typed exchange failures only at that stage, or explicit framed
  HTTP404/503 before validation/retention. Normal failed-ticket settlement must
  succeed before an availability outcome can escape. Local retention, validation,
  identity, budget and settlement failures remain terminal and charged.
- Receive catches only that availability type, rechecks owner/CA/budgets before
  and after each attempt, derives every slot from the same D, and never wraps
  whole-fetch local retention in a retryable timeout. Counts/reasons are bounded
  by the selected source list; no unbounded attempt history is needed.
- Existing finite closure, unit deduplication, PP.resolve and preflight limits
  remain. selected-unit-only must make no ancestor requests; admission occurs
  only once after READY. Source doubles cannot count as new Lean evidence.

These are focused changed-boundary obligations, not authority to repeat native
mathematical campaigns or re-audit unchanged source wholesale. Exact final
implementation/tests/selection still require review before any root launch.

## Root receive delta: focused source review

Compared the complete diff against `ordinary_sparse_access/peer_api.py`, not an
unrelated package or historical implementation. The change consists of the
three-field optional policy parser, pure timeout division, bounded source-order
helper, optional report attachment and four fetch-site substitutions. No concrete
blocker found in this receive delta; H/O implementations and tests remain open.

Exact field checking rejects partial/extra configurations. Sources are a copied,
distinct list of one through eight existing labels; strict uint validation rejects
booleans. The default helper makes the same original provider call without new
keywords, and attaches no new report field. Explicit order never prepends the
discovery provider, which remains separately reported.

The helper fixes D once from the already narrowed operation/ledger deadline minus
the requested reserve. Every attempt recomputes a floored positive millisecond
slot using the remaining source count and one close second per remaining source.
No grant, parent or budget is recreated. Both success and typed unavailability
are followed by live owner/CA/budget checks; all other exceptions propagate. The
per-provider rows stay bounded at eight and explicitly count calls, not tickets.

The four replacements preserve all original arguments and exact expected-export
bindings. Existing unit deduplication and missing-pair no-progress checks prevent
restarting an already demanded dependency; selected-unit-only breaks before the
dependency fetch sites, and the single final owner.admit remains outside the
acquisition loop. Parser checks or retention failures are not caught here unless
the lower layer incorrectly labels them AcquisitionUnavailable; that lower-layer
classification is therefore still a required separate review.

## H/O delta and combined source disposition

Read both complete diffs against their named frozen originals and the source
checkpoint ACQUISITION.md. **Combined three-payload source GO; test/selection
review remains open.** Exact reviewed payloads:

| Payload | SHA-256 |
|---|---|
| http_provider.py | d9c342d1dcb5ee3e4b293e8dc0566397a321cc59a6f545e2f2afde452c760251 |
| ordinary_acquisition.py | 076130f7a34b505df33ee550501d1c4276bb46e408ff226df765225933a0658e |
| peer_api.py | dcaea5226f58e4254dd4cff0d6c621cf593aabe9b4d511d127194816c8ddc0ef |

H's new boolean flag is explicit and defaults false. Endpoint/request encoding
and TLS context construction still occur before the classified network try.
TimeoutError is converted only when this exact timeout manager has expired;
SSLError is explicitly rethrown before narrow connection/IncompleteReadError
classification. The existing writer close/one-second wait occurs in finally,
outside that classification. External cancellation, malformed protocol and
unrelated OSError are not converted to TransportUnavailable. Its reason is an
enumerated fixed string, not a remote exception message.

O validates the optional cap/flag before beginning a ticket, caps the existing
remaining timeout, and omits the new H keyword entirely on the default path.
Only the exchange await catches TransportUnavailable. HTTP404/503 are classified
as explicit framed statuses, after response counters but before validation and
retention; HTTP400 remains terminal. Exact validation and local retention remain
outside the exchange catch, so their TimeoutError/OSError/transport sentinels
cannot masquerade as a source-availability failure.

Every classified branch increments failed_attempts once and retains
charged=None, causing the unchanged finally to charge its full reserved reply
cap. AcquisitionUnavailable is constructed only after that settlement and a
further active-budget check. Settlement/cancellation/budget failures supersede
availability. Ordinary successful accounting and all custody/checking code are
unchanged. The added lower keyword surfaces match all four receive call sites;
authoring-offers is not implicitly enrolled in fallback.

No concrete changed-source blocker found. Source inspection is not evidence
that the public composition or actual timeout/EOF seam ran successfully. The
focused test plan must still cover those boundaries and bind the exact payloads.

## Final test and exact-selection review

2026-10-26. **GO for root's one exact controls01 launch; actual success and
adoption remain pending.** Read the complete corrected test and TEST-PLAN, the
selected loader seam and fixture metadata needed to resolve API compatibility.
No concrete harness/API blocker found. Test SHA-256:
`8a696eef8e9815cc884405758e0e5ca6a4976ef491dbe1b8fe12a96ed11ea10a`;
plan SHA-256:
`a51f0c74a5c0d42fe7ac609b5887dbb435677a5dfa138a9b9a67e211882661ee`.

Exact selection: `experiments/multi-source-controls01-selection.json`, SHA-256
`fffcb8e6ba32322a15e3c59ff59758536356a64233dc2dba432b8bee591c5c75`.
Independently hash-verified all nine selected source and 37 external files
(46 total). The `experiments/v5-local-checks/multi-source-controls01` output
leaf was absent. Selection supplies the reviewed three payloads, test, contract,
plan, unchanged mirror02 loader/map and outer runner; no native source/build or
old database is an input. Runtime uses D:\Python314 with -I -S -B.

The harness installs the selected new H/O modules into the explicit transport
package and checks peer.H/O/A identities. The retained clients.configured helper
only validates endpoints; its bound legacy exchange is unused in this receive
path. Unused search imports and admission identities are explicit test doubles.
Preflight derives the two local dependency stages from retained exact imports;
external basis grounding and REUSED admission are declared doubles. They do not
establish acceptance of the deliberately false fixture. Real codecs, PP.resolve,
custody and OrdinaryBudget remain on the exercised path.

Default exchange accepts only the legacy five positional arguments. The disjoint
case checks six demanded keys, exact ten-request order, one prepaid/shared grant,
three preflights, one READY-only admission-double call, all three exact unit IDs,
and failed full-cap plus successful actual-byte charging. selected-unit-only
cannot reach dependency routes. Missing preview exhausts the explicit list before
preflight even though evidence exists. Config remains unchanged; deadline only
narrows and the caller-owned ledger is not silently closed by receive.

The twelve terminal injections check exactly one real acquisition exchange and
no later source exchange for identity, HTTP400, TLS, unowned timeout, generic OS,
cancellation, retention, settlement, aggregate-budget and live-owner-check
failures. The budget case may increment B's advisory call counter but cannot
begin its HTTP ticket; its distinction is explicitly asserted. Settlement failure
leaves its pending reservation visible rather than repairing accounting in the
test. These injections test orchestration, not real TLS or native acceptance.

Three real loopback exchanges separately cover default premature-body EOF,
opt-in EOF and this exchange's own 200-ms timeout. The test requires the server,
tracked handler tasks and writers to close; additional narrow exception/setup
controls are explicit injections. Endpoint/CA-setup controls forbid dialing.
The pure time cases check fixed-D division/capping/refusal without a slow timing
benchmark. No repeated mathematical or original mirror campaign is included.

The fixed outer envelope is 110 wall / 45 inclusive Job CPU seconds, 512 MiB,
one active process, 2 MiB stdout and 1 MiB stderr; cooperative harness limits are
90 wall / 30 own CPU seconds. No subprocess/native worker or grant renewal is
allowed. Terminal PASS requires all six groups and retained-input rebinding.
Actual saved evidence and clean outer closure still require independent outcome
review; neither source GO nor this selection predicts a passing runtime result.
