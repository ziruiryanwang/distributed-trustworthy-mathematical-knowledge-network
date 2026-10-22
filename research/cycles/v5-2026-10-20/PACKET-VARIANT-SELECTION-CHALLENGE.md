# Packet-variant reachability: independent minimum-step challenge

2026-10-22, storage_launch_review. Source/theory only, no implementation or
runtime. Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge
Network`. This note does not block or change the separately selected installed
exact-I integration. Author draft linkage will be appended when available.

## Current boundary independently confirmed

The authoritative129 map is `distribution-managed-storage-01-input.json`/
`a629df82`, with the six frozen exact-packet successors. The selected evidence
store is `managed_storage/evidence_network/custody.py`/`4264841e`; it imports
limits/offer grammar from `delta/custody.py`/`4304e529`.

- Store `offers_per_module` is configurable from1 through64. This is a local
  per-(module,profile) upper bound, not a global cap or a claim that every
  workspace is configured for64.
- Offer grammar accepts only `module_id`, `wire_profile_id`, `max_offers` and
  `max_bytes`; its count cap is8. The query orders by digest and takes the first
  requested rows. There is no offset, exclusion set, cursor or continuation.
  Repeating the same request against unchanged data cannot reach row9.
- Exact-packet acquisition/staging already solves retrieval when both digest
  and size are known. It does not reveal an unknown later digest. Another
  provider or an owner-supplied manifest may supply that knowledge, but neither
  is a guaranteed replacement for this provider's missing enumeration ability.
- One selected packet per module is enforced in BOTH
  `workspace_staged._stage_packet` (`CLIENT_STAGING_MODULE_ALREADY_SELECTED`)
  and `SemanticReader._stage` (`SEMANTIC_READER_VARIANT_CONFLICT`). Merely
  closing/recreating a reader does not clear the client's staged choice.
- Escaping certificate/admission failures still trigger the actual decorated
  facade failure path, close the original owners/budget and clear warrants and
  candidates. The reader also becomes FAILED. Metadata reachability is not a
  retry-after-refusal mechanism and must not be sold as one.

## Recommended minimum: expose the bounded set, not a cursor subsystem

Challenge to a pagination design: **why introduce cursor state while the complete
per-module set is already capped at64?** The higher-payoff minimum is to permit
`max_offers<=64` under the same bounded metadata operation, keeping existing
defaults and1..8 requests unchanged. A caller wanting the complete local set
explicitly selects `max_offers=64, max_bytes=16384` within its original grant.
No automatic proof choice, packet download, new index, global ledger or policy
relaxation follows. This is a recommendation, not a selected source edit.

Each current packet locator contains only a64-character lowercase SHA256 and
an integer size no larger than33554432. Compact JSON needs at most108 bytes per
row.64 rows plus63 separators occupy6975 bytes; the fixed current envelope is
under1024 bytes, so the complete reply is below8192 bytes and hence the existing
16384-byte ceiling. This is a source-format bound, not a measured benchmark.
The existing default4096-byte allowance must not be silently enlarged: a caller
requesting many rows must explicitly fund sufficient bytes. Reply bounds and
strict ordering/profile/size checks remain mandatory.

The SQL predicates match the offers primary-key prefix `(module,profile,digest)`;
the join retrieves only packet digest/size metadata. The intended implementation
has a bounded64-row output, no packet parsing/hashing and no proof-ancestry walk.
Its indexing cost depends on the local database and query plan, not on a scan of
all global mathematics. This is not an asserted measured SQLite complexity or a
claim that a database page containing a blob is never read.

Cached offers are not free: the current acquisition retains locator tuples.
At most64 new tuples per offer call gives an explicit `64 * funded offer calls`
upper bound before deduplication, still under the original call/request/reply
ceilings and enclosing memory limit. Larger count caps change this constant;
an unbounded cache or refill of an exhausted grant is not licensed by the
recommendation. Provider request/reservation ceilings are also unchanged.

## Concurrency and failure semantics

One SQL SELECT supplies a response-local view. It avoids multi-request cursor
expiry, lost continuation state and insertion-before-cursor gaps entirely.
Concurrent inserts after that view need not appear; deletion/unavailability
after an offer can make later acquisition fail. An offer is not a retention
promise. No indefinite repeat-until-complete loop is justified.

Conditional reachability statement: for a cooperative compatible provider with
an unchanged selected module/profile set of at most64 rows, sufficient live
allowance and a successful64-row/16KiB response, every row in that local query
view is returned. A selected later row can then enter the existing offered or
exact acquisition path. This says nothing about disconnected providers, hidden
rows, future insertions, truthful completeness of a malicious server, valid
certificates, usefulness ranking or guaranteed success of the chosen variant.
Keep `global_complete=false` and mathematical_acceptance=false.

The request grammar remains exact; malformed count/size/order/profile or an
oversized reply must refuse without partial offer-cache adoption. Existing
mathematical failure/revocation behavior remains unchanged. A caller who selected
bad evidence cannot silently clear staged state or resurrect the same owner;
any later independently authorized operation must preserve prior failed costs.

Mixed-version compatibility requires explicit scope. Old1..8 clients can use a
new64-cap provider unchanged. The converse is NOT guaranteed: an old8-cap server
may reject a64 request, and current public failure handling can close the client.
The unchanged wire profile alone does not advertise the increased limit. Do not
probe64 automatically or retry on a revoked owner. The minimum can target
explicitly upgraded/configured peers; general mixed-version capability discovery
is a separate decision, not a hidden promise of this parameter extension.

## Disposition

Prefer the bounded64-row exposure over keyset paging for this current fixed-cap
store. If a future design increases the per-module cap beyond a single affordable
reply, then keyset/snapshot semantics become justified by a changed requirement.
Do not introduce them now merely for future possibility. The later implementation
needs a small changed-boundary control (unknown row beyond8, count64/65, explicit
reply budget, unchanged old request/failure behavior), not another certificate
production or whole circulation campaign.

This minimum removes one concrete reachability defect. It does not solve robust
choice among invalid/unhelpful variants, proof economics, same-grant admission
recovery or the full v5 objective. Those remain separate, explicit decisions.

## Author draft disposition

Read the complete `PACKET-VARIANT-SELECTION-NEXT.md`,12679 bytes/SHA256
`e159c49a7d136be2ea651ce8a18d0ff74a7045ee60cd7878e554c690cc7d7797`.
**Agree with its minimum-step recommendation and stated limits.** The draft
incorporates the fixed64-row alternative, shared delta grammar's broader source
scope, both one-variant guards, cumulative cache cost and asymmetric old-provider
compatibility. It does not claim a certificate-retry capability or global
completeness. Its B-tree argument is explicitly conditional, not a runtime
measurement. No remaining theoretical blocker to root considering that narrow
metadata successor was identified; implementation, exact source pins and its
minimal controls remain separate root selections. No extra review campaign or
runtime is requested by this disposition.
