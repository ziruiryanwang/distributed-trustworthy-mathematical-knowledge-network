# Next core choice: refresh existing contact feeds before serving a directory

2026-10-28. operable_scale_decision. Source/theory only; canonical guard passed.
No imports, tests, owner/database/network access, Lean, product edits or Git.
Root owns implementation selection. Source map:
`ordinary_name_directory/source-map.json`. Existing evidence stays frozen.

## Decision and concrete workflow

**Implement one bounded `directory-refresh-serve` composition using the existing
`/v5/ordinary/contacts` protocol.** A registrar approves provider feeds, route
scope and quotas once per policy revision. Independent providers maintain their
own existing contact maps. Each directory cycle automatically admits their
fresh responses under that policy, then serves one immutable map. No new wire
schema, revision ledger, remote write API or per-advertisement approval.

An investigator knows a shared carrier/interface and a community directory.
Independent libraries add relevant material or change mathematical-service
endpoints. Their operators update their own feed maps; the next directory
cycle exposes the allowed replacements without the registrar editing their
advertisement bytes. Multiple communities can run this role independently.
New feed origins or newly authorized topics still need local policy adoption;
there is no compulsory registrar, global provider census or task list.

The current lookup works, but maintenance stops at hand-authored complete maps:
`peer_api.directory_serve:408-428` accepts an `entries` array and makes one
immutable ContactMap. It has no policy-scoped feed refresh. The reader's current
request-start contact horizon limits use of a reply; it does not age the map's
registrations. Serving an old map in repeated new cycles can issue stale hints.

## Compare the competing implementation choices

| Candidate | Decision-changing fact |
| --- | --- |
| Stopped dedicated-host delta append | Valuable for frequent inert replication, but retained mathematical owners already publish incrementally with `create:false` (`peer_api:827-889`). Stable dedicated hosts restart without scanning all evidence. No current trace establishes a failing 64-target generation or costly high-rate mirror cadence. Append requires cross-store partial-update/recovery rules. Keep deferred per CONTINUOUS-USE-DECISION. |
| Policy-driven contact refresh | Benefits both evolving owners and dedicated hosts. The missing behavior is ordinary metadata maintenance between independent operators; it can reuse deployed contact transport and immutable serving without touching theorem bytes, owner state or native support. Choose this. |
| New matcher, generic capacity migration or DHT | Actual shared-symbol discovery already exposed unfamiliar useful laws; pattern deployment lacks a natural positive use. No actual quota-exhaustion case selects compaction. Existing one-hop directory transport suffices for this workflow. These larger mechanisms do not fix registration maintenance more cheaply. |

This deduplicates RESUMED-ROUTING-CHOICE: manual maps were explicitly an initial
compromise; registration/update churn was its later boundary. Same-core package
updates already permit retained-owner reuse (UPDATE-TRUST-DECISION). Native
output accounting remains deferred by RESOURCE-DECISION.

## Finite API and local policy

Add one public operation, `directory-refresh-serve`, retaining the existing
finite launcher, server TLS, provider quotas and clean-close rules. Providers
use the already shipped `directory-serve` to offer their own advisory maps;
new producer machinery is unnecessary. A dedicated feed endpoint can remain
stable while the mathematical-service endpoints it advertises change.

The operation takes an exact approved policy/configuration plus fresh output.
Policy contains the ordinary namespace, known authenticated feed endpoints,
feed-route slots, local endpoint-admission rules, aggregate refresh limits,
minimum usable service interval, maximum issuance age, and ordinary finite
listen/service/cleanup configuration. Feed origins are explicit known contacts
with their own TLS policy; TLS authority is not learned from a reply.

Each slot is `(feed label, exact route specs, max_contacts, max_bytes)`.
Compile routes through the existing ordinary feature compiler; at most eight
features per exact nonempty key. Approve at most eight feeds and thirty-two
slots/requests. Give each slot 1..16 contacts and at most 32 KiB; reserve at most
1 MiB response bytes across the operation. These are proposed ceilings, not
recommended allocations. For every compiled route, require the **sum of slot
contact quotas <=16** before any I/O. Preserve the 2 MiB/2,048-key final map
bounds. This avoids a new ranking, competition or silent eviction policy.

For advertised endpoints, apply the existing numeric-address/HTTPS/port checks
plus a locally approved bounded set of TLS server names (or exact endpoints
where appropriate). This permits selected service-IP changes without granting
a feed unlimited third-party recommendation scope. It is a local admission
policy, not proof of endpoint control. Existing reader egress and server
certificate checks remain independent. Loopback/plaintext is only explicit
local test policy. The registrar **never dials a learned endpoint**.

For each slot, issue one existing Contact Request with a fresh nonce, exact
namespace/features and its selected quotas. Use the existing settled
`fair_exchange.exchange`, direct-feed TLS pins and original aggregate
request/byte/deadline accounting. Do not add an HTTP client, a new response
schema, recursive feeds, retries, or a new grant after a failed request.

## Partial sources, replacements and withdrawals

A valid response must satisfy the current nonce/namespace/features binding and
endpoint checks. Its returned endpoint subset replaces that slot for this
invocation; there are no eligible cached rows. Union accepted subsets by exact
route and deduplicate canonical endpoint tuples. Preallocated quotas already
bound each final route, irrespective of response arrival order.

Preserve per-slot outcomes separately:

- Valid nonempty response: include the allowed returned subset.
- Valid empty, untruncated response: that source currently offers no contacts
  for this route, including withdrawal of its former contribution.
- Truncated response: include its allowed returned subset and report partial
  source coverage; never increase its quota or retry automatically.
- Unavailable, malformed, disallowed or expired response: omit that slot and
  report the exact failure class. This is **not** a withdrawal or global absence.

Partial-source policy is explicit: serve the union of successful usable slots
and label the refresh incomplete if any selected slot failed or was truncated.
No successful slot can remove another slot's contribution. If the union is
empty, return a closed no-listen result, distinguishing complete selected-slot
empty answers from incomplete refresh. Current `directory-serve` requires at
least one entry; do not work around it with fake rows or a meaningless server.
Existing wire replies already assert false global completeness/mathematical
acceptance; local READY/final reports must preserve refresh incompleteness.

## Expiry, replay and the strict issuance boundary

For request start `t_i` on the registrar's monotonic clock, define its issuance
horizon `h_i = min(original deadline - cleanup reserve, t_i + policy_age_i)`.
No remote timestamp is authoritative. At map assembly and immediately before
READY, omit slots with less than the policy's minimum remaining service interval.
This prevents a permitted very short-lived slot from ending the entire service.
Choose the service cutoff as the minimum remaining included horizon and selected
finite lease. Refresh failures/omissions consume time and keep their charges.

All usable rows come from fresh authenticated nonce-bound responses in **this
same invocation**. No saved map can be relaunched as freshly refreshed, and a
restart fetches again. Thus there is no cross-boot UTC/clock-rollback or cached
lease problem to solve. Old response replay fails the nonce binding. A live
provider can freshly repeat an old configuration; this design does not detect
provider-side rollback, prove liveness or certify current useful coverage.
A new revision protocol would add that narrower historical check, but is not
justified for advisory reachability now. It could still advertise stale endpoints
under a larger revision and would not establish truth or availability.

The existing provider checks only per-request `operation_ms`; its outer asyncio
lease cannot preempt synchronous reply construction. Add an optional provider-wide
monotonic issuance cutoff, combined with the per-operation deadline. Check it
during dispatch and immediately before **each** response write, including body
chunks after an awaited drain. An overrun closes without further hint bytes;
keep conservative reservations and normal bounded cleanup. Do not rely on just
a final map-filter or lease timer. Existing callers without the cutoff retain
their current behavior. This is the only required transport-boundary change.

The promise is no new application-level hint-byte issuance after the cutoff,
under the existing trusted monotonic-clock/execution assumptions. Bytes already
queued in the OS/network may arrive later. A reader that obtained a hint just
before cutoff can still use its own existing request-start horizon (currently
up to 60 seconds). This is not immediate client revocation; that stronger claim
would require a changed reply/reader protocol and is excluded.

## Cost, smallest evidence and counterargument

For `s<=32` selected slots and bounded aggregate reply/map bytes `B`, refresh
adds `O(s)` attempted requests and `O(B)` validation/assembly, then ordinary
service work. No owner history, proof ancestry or complete remote corpus is
read. Rebuilding a <=2 MiB advisory map is a different cost from recopying an
ever-growing mathematical collection. These are source-derived bounds, not a
measured speedup; charge every cycle, failure and curation effort. A large
network still needs funded selective communities, useful route overlap and
reachable feeds. One bounded directory does not supply universal coverage.

The changed-boundary evidence should be narrow: policy quota/scope validation;
fresh replacement, explicit empty and truncated/missing distinction; no cached
fallback; expired/too-short-slot omission; strict dispatch/write cutoff and
clean closure. Use existing authenticated transport/parser controls instead of
retesting them. No Lean, owner, new theorem or semantic-search episode is needed.

The smallest later real workflow is an existing independent library changing
its own allowed endpoint/route offer and the registrar's next selected cycle
exposing it to an unchanged shared-symbol client without registrar edits to ad
bytes. Reuse actual query/theorem material. No external deployment or such
independent-user evidence is claimed or selected by this note.

Counterargument: a few stable providers can already maintain maps cheaply, and
an offline file merger merely shifts editing. That is why the selected change
must include fresh feed retrieval, automatic application of already approved
policy, and finite serving in one operation. This composition is smaller than
a new registration platform and works with existing provider commands. If root
cannot keep it within those boundaries, retain static maps rather than add a
revision database, remote write authority or generic DHT project. The theoretical
choice is resolved; root can select this minimal implementation without another
broad audit or constructed mathematical demonstration.

Source anchors: `ordinary_contact_federation/contact_directory.py:26-35,161-217`;
`ordinary_multi_source/peer_api.py:206-399,401-477,827-889`;
`ordinary_reply_capacity/http_provider.py:125-127,500-568`;
`ordinary_sparse_access/fair_exchange.py`;
`ordinary_dedicated_host/custodian.py:167-278`;
`ordinary_type_pattern/WORKFLOW-CHOICE.md`;
`ordinary_usable_distribution/CONTINUOUS-USE-DECISION.md`;
`research/cycles/v5-2026-10-25-software-continuation/RESUMED-ROUTING-CHOICE.md`.
