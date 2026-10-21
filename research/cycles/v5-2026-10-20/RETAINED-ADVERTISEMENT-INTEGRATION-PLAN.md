# Cross-run discovery: smallest remaining integration boundary

2026-10-21, core_release. Source-only plan; no adapter, runtime, networking,
proof, admission, installation copy or Git operation. The current nine focused
controls are still subject to root adoption. This note does not claim they ran.

## Decision: batch the actual check, do not repeat actual02

**No separate experiment is needed now merely to select the retained primitive.**
Its focused controls exercise exact-store reopening, sealed authority, untouched
retained data, run/config caps, charged uncertainty and task closure. Adopted
actual02 (`PLACEMENT-NETWORK-INTEGRATION02-OUTCOME.md`, `e1771fe0`) already
establishes real placement, source-offline discovery/acquisition and received-I
admission. Repeating its admission or one-run exchange would add little.

One new composition boundary remains: after the first service actually closes,
a fresh Node identity must announce the retained route while the same read
endpoint rebinds, and a goal-only reader must tolerate possible stale peer hints.
Neither simulated restart nor actual02 establishes that composition. Include
the scenario below **once in the next selected installation smoke**, instead of
running both an overlay version now and an installed duplicate later. If a
cross-run network-operability claim is needed before that installation, root
can select this same small scenario earlier; its evidence must retain its
source-overlay scope. Do not label the unrun boundary passed by composition.

## Existing APIs are sufficient

The physical selected APIs were checked against the installed SDK map and the
actual02 successor; no new manager or product route is required:

- `PlacementService.open/start/advertise_retained/close`, fresh successors
  advertisement `5aa23ee7`, service `7e735337` at this source-review checkpoint.
- `service.controller.seal(service.grant)`, existing controller `ef1c9b59`.
- `ServiceLocationProcess` from `body_location/portable/location/controller_services.py`
  (`eeb82d5d`); new state/evidence directories and fresh Node identity per run.
- `observed_route.route` (`9800b5fd`) and `available_descriptor.descriptor`
  (`d3b215f5`) on the same `ServiceLocatedWorkflow`. The selected Node entry
  (`7efae4a2`) returns typed `TCP_CONNECT_UNAVAILABLE` without replacing the child.
- Existing authenticated search and `EvidenceAcquisition`; no acceptance rule
  or mathematical receiver changes.

Actual02's adapter `placement_network02/integration.py` (`e5979ec3`) is a frozen
reference, not editable input. Its `discover` function requires exactly one
peer and calls the fatal ordinary `workflow.descriptor`; **do not copy those
two assumptions into a restart adapter**. Current product capability already
offers the bounded alternative described below.

## One finite scenario

1. Use the retained exact terminal-I fixture already adopted by actual02:
   selected binary-congruence opening 1595 B / `0c74d294...`, packet 447887 B /
   `a737e8f6...`. Seed only source A's custody using the existing structural
   fixture path. Create a new output tree and prospective generation with
   `max_runs=2`; never reopen actual01/02's used `max_runs=1` state.
2. Start reader locator R, then custodian B1 bootstrapping from R. As in
   actual02, R initially holds only routing state, not a supplied mathematical
   answer. One remote submit commits placement and a route; omit duplicate/
   status reruns already covered by adopted evidence. Save request ID and exact
   committed request/receipt plus bounded fixture-store snapshots.
3. Stop A's HTTP listener, observe no remaining tasks, and close A. Seal B1
   through its actual owner controller, then fully `await B1.close()` and require
   `CLOSED`, clean Node exit, all role/store flags true and no pending actor.
   Keep R alive. There is no TTL wait, file deletion or private DHT manipulation.
4. Open B2 over **the same B workspace, generation config, read endpoint and
   journal page cap**, with all three create flags false. Give B2 a fresh
   locator state/evidence directory and a distinct Node listen port; keep B1's
   old port unbound. Bootstrap B2 from the same live R. A new owner service run
   is funded by the original two-run cap; no old token renewal or new grant
   issuance is needed. Require sealed state, run 2 and a different run ID.
5. Call `await B2.advertise_retained(original_request_id, until=B2.deadline)`.
   Require its actual current-run facet and observed add-provider write. Check
   that the original request/receipt/grants/cells/funding and custody/index
   contents are unchanged. Only the core run counter and route run/row may
   grow; the seal transition was recorded before reopening. Whole-store row
   hashes are acceptable for this tiny **test fixture**, not a product scan.
6. Only now open R's fresh reader workspace and invoke a function whose inputs
   are its independently constructed complete binary-congruence goal, policy,
   locator and original budget. Do not give it module/name/object/packet IDs,
   publisher manifest, selected custodian identity or expected answer bytes.
   Discover, authenticate a search result and acquire group plus packet via
   returned contacts. Outside that function, compare the acquired exact bytes
   against the retained fixture and B's unchanged stores.
7. Close B2 and R with original deadlines and clean process/store observations.
   Stop here: **zero proof production, zero verifier calls, zero native checks,
   no new trust adoption**. This run establishes byte-preserving transport and
   restart, not fresh mathematical admission. Its I bytes have prior actual02
   admission evidence; that evidence is not manufactured into a current handle.

## Stale hints: pay for alternatives, never assume one peer

Use one observed route with `peer_cap=2` and `event_cap=256`; the topology has
only B1/B2 as potential providers. Accept zero, one or two unique returned peers,
not an assertion that there is exactly one. In returned order, attempt at most
two descriptors via `available_descriptor.descriptor`, each at most 4096 B.
A typed unavailable result conservatively spends its original reservation and
continues to the next returned peer. Other malformed, authentication, channel,
cancellation or cleanup failures remain fatal; do not broadly catch them.

Begin search only if an unexpired advisory contact exists. Both valid
descriptors would refer to the same exact read endpoint, so existing contact-ID
deduplication suffices. Search once, authenticate the offer/page and match the
complete formal type before structural acquisition. No injected endpoint,
known-answer peer filtering, fresh query budget or unbounded retry follows a
miss. If routing exposes only stale peers or no usable contact, preserve the
bounded incomplete result; it is not proof of nonexistence.

Keep actual02's search caps: providers 1, snapshots 1, requests 4, pages 2,
examined 8, candidates 4, bytes 262144, inflight 1, wall 60000 ms. Location:
one route, 256 events, two peer slots, **two descriptors**, one contact,
270336 reply bytes and 60000 ms. Arithmetic is explicit:
`262144 + 2*4096 = 270336`. Prepay **seven**, not six, location/search requests:
`1 + 2 + 4 = 7`. Existing acquisition allowance 12 requests / 2 MiB then leaves
five requests for the three group/offer/packet reads. Keep all unused verifier
allowances unconsumed. Node commands 16 and provider limit 2 suffice; original
transport caps and per-command deadline still govern dial attempts.

Report whether a stale peer was actually returned and whether a typed stale
dial miss was observed. If neither occurs, successful restart is still evidence,
but this run does not claim an executed stale-hint fallback. Do not add an
extra forced-failure campaign merely to manufacture that observation. Loopback
closed-port refusal is covered; this is not a claim of recovery from every
Internet black-hole timeout or adversarial routing omission.

## Finite envelope and exact future code seams

Retain actual02's 150 CPU / 300 wall seconds, 512 MiB, six-process outer envelope
as a prospective ceiling, subject to root's final source review. There are
three sequential Node identities but at most R plus one custodian alive; no
large proof process. Use the installed runtime in place, not an 842 MB copy.
The extra work is one actual locator start/close and fresh route restoration.
Do not reduce mandatory runtime-pin validation or six-second native teardown.

Use one common `started+280` owner deadline; both custodian locators can retain
the original `started+200` cutoff and R `started+210`. Each service's existing
computed deadline must fit the original receipt retention horizon; refuse
before opening/dispatch if insufficient time remains. Preserve actual02's
210-second locator service envelope, 120-second service lifetime, explicit
32 MiB provider reply capacity and fixed cleanup reserves. These are ceilings,
not sleep durations or authority to renew a slow attempt. Root must select
fresh exact input horizons once; no late extension or automatic rerun.

If selected, author only a fresh adapter and selector. Reuse exact staging,
ports, runtime adoption and fixture patterns; replace the two product source
pins, add B1/B2 sequencing and the two-descriptor loop, and omit `admit_received`
and its verifier/trust dependencies. Preserve failure diagnostics and clean-up
evidence for both custodian runs. No product source change is presently needed.
This plan intentionally leaves the actual integrated boundary unrun so the
team can prioritize the unresolved certificate/useful-growth work now.
