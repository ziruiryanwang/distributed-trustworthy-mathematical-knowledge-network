# Exact-packet acquisition: independent design challenge

2026-10-22, storage_outcome_audit. Source-only review; no import, test, database
connection, service, proof operation, installation change or secret read.

## Decision

**The obstruction and minimum remedy are real.** The existing provider already
supports exact packet SHA-256 plus exact byte count. Requiring a truncated offer
first is unnecessary for a caller that already knows both. An explicit exact
API can remove that obstruction without changing the wire route, store schema,
cryptography or mathematical admission. This is not a claim that knowing a hash
makes a packet available, trustworthy or relevant.

The initial proposal omitted the staged semantic-reuse route. The independent
challenge traced `SemanticReader.stage` to `CommonsClient.stage_packet`, which
has its own offer prerequisite. Root adopted this finding in
`EXACT-PACKET-IMPLEMENTATION-SELECTION.md`: explicit `stage_packet_exact` and
`SemanticReader.stage_exact` now belong to the selected implementation. A
direct-only `acquire_exact` change would not satisfy that selection.

## Source basis and established obstruction

Authoritative base: the129-entry map
`experiments/v5-local-checks/distribution-managed-storage-01-input.json`,
SHA-256 `a629df82718f6a9d0560cacbfdc459739c15a56a1f2a46dd87929a1db51c22a4`.
The six selected predecessor files and actual `workspace_atomic` were rehashed
against that map; all agree. Logical names below refer to this map, not the
oldest similarly named file in `software/v5`.

| Source / SHA prefix | Independently checked fact |
|---|---|
| evidence_network/transport `7ac7204b` | Structural-only subclass, original shared budget, profile-selected typed custody; old packet delegates the offer-gated superclass. |
| delta/transport `18c1abda` | Provider dispatch serves exact `packets.get(sha,size)` without an offer; receiver `_get` owns active/contact/deadline/framing/budget checks. |
| evidence_network/custody `4264841e` | Typed inspection binds selected profile/foundation/policy and target module. Offers use a digest-ordered bounded SQL query. |
| delta/custody `4304e529` | Exact primary-key lookup; offered request maximum8 versus permitted stored maximum64 per module. Typed put checks quotas and before-COMMIT liveness. |
| placement/controller `ef1c9b59` | Exact manifest already identifies wanted packet; local-hit path is exact, but missing packet requires membership among first4 offers. |
| client/workspace_evidence `d94e3825` | Independent offered-choice gate; genuine admission, same-live cache validation, body/group binding and final exact-journal comparison. |
| client/workspace_staged `ae3dc1a7` | Separate offered-choice gate; inert staged token and later independent mathematical admission. |
| client/semantic_reader `17a3da54` | Chooses only origin or pending demanded module and calls the staged gate; selection and exact member/journal checks follow. |
| client/workspace_atomic `32e3b95e` | Decorated calls are serialized and fail closed; candidates must be exact tokens owned by the current client. |
| client/managed_owner `6991ac58` | Frozen workspace source pin plus complete authenticated129-source writer identity. |

The proposal's first4 example alone is not the strongest discriminator: max8
offers could recover a fifth packet. A genuine ninth-or-later lexicographic
variant establishes why raising the prefix cannot solve exact acquisition.

## Required invariants

1. **Immutable exact demand.** Validate closed entry shape, lowercase digest,
   strict integer byte count (`True` is not1), module identity, current profile
   and per-packet capacity before transport. Copy the validated demand before
   the first await and use that same copy for charging, acquisition and readback.
   A caller must not mutate one identity into another while work is suspended.
   Per-packet preflight does not guarantee remaining database capacity: total
   logical/page quotas remain checked transactionally by the existing store.

2. **Original acquisition authority.** Use existing `_get`, not raw exchange or
   a fresh budget. Keep configured/authorized supplier, expiring contact and
   original deadline checks, cancellation settlement, finite reply allowance,
   generation retirement and before-COMMIT `_active`. Never fabricate an offer,
   renew a contact, refund an attempt or silently retry. Provider disappearance
   is an ordinary acquisition failure, not evidence of mathematical absence.

3. **Custody is not acceptance.** Verify exact response size/hash, typed selected
   profile and target module before commit, then exact local readback. Structural
   parsing can accept syntactically shaped fake certificate bytes; only the
   existing real admission owners grant mathematical warrants. `packet_exact`
   and staged tokens must remain explicitly nonmathematical.

4. **Public direct and staged paths stay coherent.** New explicit exact methods
   share private, undecorated bodies with the old offered methods. Calling one
   decorated public action from another would violate busy/reentrancy/accounting
   discipline. Preserve old offered API refusal and exact candidate ownership.
   Stage only the current semantic-reader origin or pending demand, retain the
   one-variant policy and inert snapshot, and leave later admission unchanged.
   Local staged admission must neither redial nor renew the provider contact.

5. **Exact mathematical binding survives cache use.** ModuleID/summary alone
   does not identify journal rank. Preserve same-live warrant checks, selected
   packet bytes, optional exact184-byte expected journal and unconditional final
   journal equality, including cache hits. Preserve demanded bodies, selected
   group opening/descriptor and owner `open_group`; do not infer acceptance
   from a stored custody report or a previously returned token.

6. **Placement remains prospectively funded.** Replace only the missing-packet
   offer branch with exact acquisition. Preserve exact local hit, opening/summary
   comparison, receipt states, retained idempotent request result and separately
   charged new request. The existing conservative quote can remain: removing an
   actual offer request creates no refund. Recovery remains local-only.

7. **Source and state identities remain honest.** Staged construction requires
   selected owner source pins for `workspace_staged`; evidence construction pins
   its transport/evidence modules; body-location activation adds the reader's
   selected pin. The complete SDK map must carry all selected successors, not
   merely the managed owner's changed workspace pin. Any SDK change alters the
   managed writer identity: old state is not automatically compatible. This
   source selection is a fresh successor, not an in-place state migration.

## Accounting and scale claims

An exact missing-packet transfer uses one existing packet HTTP request and the
selected packet's exact payload allowance. Existing `_get` settles measured
response bytes, or the reserved maximum when the failure makes that quantity
unknown. Its accounting must not be confused with placement's distinct retained
full quote or external nonrefundable preallocation.

The existing provider uses indexed digest lookup; under ordinary B-tree
assumptions its lookup/read/hash work is O(log N + L), with local packet count N
and selected bytes L. Typed parsing and insertion retain envelope/quota costs.
No global corpus enumeration or ancestral proof replay is introduced here.
This is neither constant latency nor logarithmic semantic search, and gives no
global search completeness, availability, novelty or net-growth guarantee.

The current transport does not promise a rich typed NOT_FOUND result: malformed,
unavailable or framing failures may surface as ordinary transport exceptions.
The exact API should preserve that honest failure model instead of inventing
structured availability claims unsupported by the provider.

## Finite discriminating controls recommended

- Put a genuine typed target ninth or later in one module's sorted offers;
  show max8 omission and exact transfer through the actual existing HTTP route.
  Show old offered acquisition still refuses it and `_offers` stays unchanged.
- Separate structural staging from mathematical admission. For factored public
  paths test exact dispatch, immutable selection, candidate/semantic demand and
  existing admission invocation; label any synthetic owner/client doubles.
  Unchanged cryptographic evidence does not need a new prover campaign.
- Refuse malformed/bool/oversize demands before dial; refuse wrong bytes/hash,
  target/profile and before-COMMIT expiry without a false stored result/warrant.
- Keep exhausted/shared/closed/retired budgets, expired/missing contacts and
  cancellation charged/closed under the original allowance; no renewal/retry.
- Check exact-journal/cache boundaries and local-hit placement; a remote exact
  placement path should make no offer request, while retaining its full quote.
  Use existing source arguments/evidence where unchanged paths already suffice.

This challenge supports implementing the selected six fresh successor sources.
Concrete source, controls and selector review remain separate from this design
finding. Nothing here authorizes execution or declares the full v5 goal met.
