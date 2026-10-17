# Ordinary A-capable client: bounded source implementation plan

Status: **source design, ready for root selection; no implementation or runtime**.
Canonical root is `E:\Distributed Trustworthy Mathematical Knowledge Network`;
guard and AGENTS were reread. This closes a concrete missing software seam,
not the complete v5 architecture or the outstanding genuine-A certificate gate.

## Decision and scope

Create `software/v5/client/workspace_mixed.py` as a fresh, explained concrete
specialization of frozen `workspace_atomic.py`, using the existing mixed custody,
transport, receipt, import and authoring APIs. Keep `workspace.py` and
`workspace_atomic.py` permanently I-only and unchanged. Add
`software/v5/client/API-MIXED.md`; do not rewrite the frozen I-only guide.

The new client requires one actual A owner and accepts an optional actual I
owner. This is a closed two-case configuration, not a verifier/plugin registry:

| Client | Required actual owners | Permitted configured claim tags |
|---|---|---|
| Existing I-only atomic client, unchanged | I, mixed delta with `(I,None)` | I |
| New A-capable client | A, mixed delta with `(None,A)` or `(I,A)` | A; I only when an I owner is configured |

Requiring an otherwise unused I verifier merely to use an A member would add
installation/lifetime dependencies without supplying additional mathematical
authority. Underlying `MixedDeltaVerifier` and `MixedImportSession` already
support the A-only case; do not fabricate an I owner or borrow its report.
Preparation remains optional; reader-only operations need no authoring owner.

No checker, guest image, packet schema, index/routing algorithm, global registry,
new cryptography, implicit retry or proof production is part of this change.
The prior actual I reuse is retained evidence, not a campaign to repeat.

## Concrete source changes

The present I-only sites are `workspace_atomic.py:29-30,214,344,401,490,570,644,679`.
All inherited methods must also be read for lexical owner/profile assumptions;
changing imports alone is insufficient.

Prefer concrete subclasses of the frozen Workspace/CommonsClient for unchanged
profile-neutral routing, authoring, publication and recovery mechanics, with
explicit overrides at the table below. Do not call the old `open` or client
`__init__`: they construct an I-only PacketStore and require `(I,None)`.
Reuse the existing helper/token classes only with their exact workspace/client
registry membership checks. No monkeypatching, dynamic backend selection or
rewriting inherited globals. The selected source closure must pin/import the
frozen atomic base as well as the new module.

Reviewed baseline `workspace_atomic.py` is 50,535 bytes, SHA-256
`01eefed1804ec5f296aebfcc12441dd283cd77c9bac8f8d5b02e8a4becc5e8c1`.
Root's fresh source selection must enumerate all imported bytes and exact
runtime pins; this note is not a substitute authorization manifest.

| Boundary | Required new behavior |
|---|---|
| Wire/storage construction | Import `mixed_network.custody.PacketStore/public_profile/profile_id`; construct exact `public_profile(A)` from locally configured A, never an offered header. |
| Remote lookup/acquisition | Import existing `MixedLocatedHandoff` and `MixedAcquisition`; pass the exact same mixed profile and shared acquisition budget. |
| Owner transfer | `Workspace.operation(..., aggregate_owner=Aowner, receipt_owner=None or Iowner, delta_owner=delta, ...)`; transfer all owners only after complete construction succeeds. |
| Constructor/active checks | Exact types; `delta._owners == (Iowner,Aowner)` by object identity, `delta._aggregate_image == Aowner._image == configured A`; freeze/check all actual profile IDs and original owners. |
| Packet admission/semantic material/publication | Both `parse_packet` sites receive the independently selected A. No `aggregate_image=None` remains in the new mixed path. |
| Atomic semantic imports | Existing `MixedImportSession(legacy_verifier=Iowner, aggregate_verifier=Aowner, delta_verifier=delta, ...)`; existing `materialize`, immutable selection view and `MixedSourceOperation/MixedOwnerPreparation` remain unchanged. |
| Failure/close/report | Close A as well as delta/I/preparation/import session; clear both A caches and all client warrants. Report I as absent when unconfigured. Preserve cleanup poisoning and original deadlines. |

Use a new workspace schema, e.g. `DMKN_V5_CLIENT_MIXED_WORKSPACE_V1`, and new
report schema. The canonical persisted configuration includes the exact mixed
wire profile with its explicit `aggregate_image`. A workspace is created fresh;
there is no in-place migration/relabeling of an I-only packet database. Reopening
requires exact original configuration and restores bytes/history only.

## Direct A-member API: necessary to start ordinary authoring

Receiving mixed packets alone is insufficient: the first extension may start
from a genuine A receipt plus member openings, before any mixed delta exists.
Add one public method rather than exporting raw issuer handles:

```python
client.admit_aggregate_member(
    receipt_bytes, expected_header, exact_journal, index, siblings,
    *, cpu_seconds=30, wall_seconds=60, memory_mib=1024
) -> LiveWarrant
```

The method must charge all submitted receipt/header/member/path bytes, check
the configured profile and limits, then call the real
`AggregateReceiptVerifier.receive(receipt,H,fresh_output,...)` and
`select_member(handle,J,index,siblings)`. It never constructs a verified handle
from a receipt-shaped JSON record. `H` is exactly 192 bytes; `J` is exactly 184;
existing aggregate bindings enforce membership bounds and the adopted A.

Cache only the same live A receipt handle under the exact key
`(adopted A, owner profile, SHA256(receipt), len(receipt), H)`. A second selected
member may reuse this handle after actual issuer revalidation; do not verify
the whole receipt once per member. Any member-token cache key must additionally
include **exact J, member index and the ordered sibling digests**; one receipt
can contain several distinct members and is not a member identity. If no
separate member cache is used, call the actual issuer's `select_member` each
time and retain its equally exact record. Cache hits still charge submitted bytes and
member work. Failed or closed owners revoke all references. Do not inject this
cache into the mixed verifier's private cache; separate legitimate rechecks are
charged through the common budget rather than silently declared free.

Add a distinct client warrant kind `A-member`, alongside `I` and `mixed`.
Its record holds the genuine `VerifiedAggregateMember`, original receipt bytes
and exact live member fact. `_warrant` rechecks `describe_member` (not
`describe_aggregate`) and binds profile, A/H/J, digest/length, index and siblings.
`import_context` dispatches this kind to
`MixedImportSession.use_aggregate_member(handle,receipt_bytes,resolutions=...)`.
The public `describe` returns the selected member, not an I receipt claim.
Direct I admission explicitly refuses when I is absent.

**Serialization trap:** existing `_issue/_warrant` normalize only `journal`.
A-member facts additionally contain byte-valued `aggregate_header` and sibling
digests. Normalize only the known fact fields exactly, as illustrated by
`mixed_claims/imports_atomic.py:_encoded_fact` (journal/header/aggregate_header
to byte lists; siblings to lists of byte lists). Preserve original bytes for
verification; normalized copies are comparison/report data, never authority.

`semantic_material(A-member)` returns a precise demand for caller/provider
semantic openings and required bodies, like direct I; receipt membership does
not magically supply definition bodies. Mixed-packet semantic extraction stays
the existing bounded structural procedure. Atomic materialization rejects
incomplete declaration groups/conflicting exact warrants and requests missing
bodies; there is no new ad hoc import or definition expansion route.

## Identities, budgets and live ownership

Keep the exact existing mathematical basis:

- I: `9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e`.
- Foundation: `d931d114155cf3cf0dc0b868aa88c6d38b8ada8ecafe267a5934934075782481`.
- Policy: `5edfd0ee15b141b7304e26c1a39cd11f7f7e721713cf099813ae4f4442fad377`.
- Mixed wire profile/schema/receipt encoding: use exactly the values produced
  by current `mixed_network.custody.public_profile(A)`, including header v2,
  192-byte H and genuine succinct Poseidon2 receipts. Do not invent replacements.

A is explicit local adoption, nonzero and distinct from I; it is not discovered
from the incoming receipt. Root's selected launch/source manifest must bind the
actual A-capable executable, supervisor, runtime/source closure and adopted A.
`AggregateReceiptVerifier` already hashes these into its profile. The new client
also binds the exact A-owner, mixed-owner and optional I-owner profiles. A
build or source hash is identity evidence, not mathematical admission. No A
receipt for the current memo image is presumed available by this plan.

Reserve the workspace grant before constructing owners. Require pristine
owner attempts/handles (including A's `live_aggregates`, `live_members` and
member counters), original deadlines no later than the grant, owner caps within
the grant, correct output locations and exact required source pins. The caller
constructs owners; no owner factory or JSON handle loader is introduced.
The legacy I base class has no construction-start field: do not pretend the
client can independently prove its start timestamp. The selected outer owner
strategy must construct it after reserve, as before.

All direct I, direct A and packet admissions use **one** existing
`AcquisitionBudget`. Reserve verification before calling an issuer. Packet cost
is `claims*receipt_cpu + deltas*native_cpu`; several A members of one claim do
not create several proof verifications. Existing per-admission cap (600 CPU
seconds) remains; unsupported envelopes refuse rather than split/retry with
fresh allowances. Owner-local CPU counters are nested accounting, not disjoint
allocations to sum. Preparation worker budget is disjoint and
`preparation + acquisition <= total grant` remains mandatory. A member work,
controller work, bodies, calls, storage and output stay finitely bounded too.

After transfer, failure/expiration/changed pins/changed owner profiles must
prevent mathematical use through every warrant, cache, candidate, selection and
authoring path. Closing delta is not sufficient: it does not own the independent
A issuer. New client close/failure must explicitly close A and optional I and
retain uncertain cleanup in the workspace ledger. Outer Job closure remains
the actual process-containment evidence; this client is not a hostile-code sandbox.

## Publication and independent reuse

**Direct/local A bootstrap and remote mixed-packet discovery are distinct.**
Current `mixed_claims.packet.parse_packet:81-84` requires at least one delta;
`mixed_network.custody.PacketStore.inspect` targets `witnesses[-1]`. These APIs
do not offer a standalone certified A member as their packet's target. The new
direct method accepts owner-supplied receipt/H/member-opening bytes; after a
substantive ordinary extension, existing mixed transport carries its A frontier
and new delta. Do not add an identity/wrapper theorem merely to manufacture a
wire target, and do not describe this seam as remote discovery/acquisition of
bare A members. A standalone-member transport would be a separately justified
later decision, not hidden scope here.

Keep `publish(packet,exports,retention_policy)` structurally bounded. It stores
the exact mixed packet, selected semantic openings/bodies and index records;
partial cross-database publication remains explicit and reconcilable. Neither
publication, a new index entry nor its saved outcome creates mathematical
authority. No new certificate is minted by ordinary authoring or publication.

Serving this workspace uses existing `mixed_network.transport.CompositeProvider`
with its exact `ModuleStore`, mixed `PacketStore` and index. Locations, search
contacts and offers remain advisory. `MixedAcquisition` preserves original query/
acquisition budgets, demands semantic custody and invokes the actual mixed
verifier before granting a warrant. There is no automatic I-wire fallback or
opportunistic switch to a different A image. Independent recipients select their
own matching profile and reverify; saved provider reports are irrelevant.

## Assignment boundaries and finite gates

Root should select the following disjoint work, not another broad campaign:

1. **Author:** only fresh `client/workspace_mixed.py` and `client/API-MIXED.md`;
   preserve baseline bytes and explain each difference. No edits to existing
   receiver/import/authoring/network/checker/source-selection machinery.
2. **Controls author:** fresh `client/test_workspace_mixed.py` and, if needed,
   a separate bounded no-host test owner. Cover exact A/I profile mismatches,
   wrong owner pairing/types, absent-I refusal, A fact normalization, same-live
   multi-member caching, common budget exhaustion, original deadline/fail-stop,
   close of every issuer, foreign/stale warrants and no restart from saved data.
   Synthetic issuer interactions are explicitly control evidence, never genuine
   A acceptance; no production mock mode or fallback is permitted.
3. **Independent reviewer:** source/profile/authority/resource closure and exact
   changed tests only. Inspect import-origin and selected-source closure.
4. **Root integration:** separate fresh launch selection/asset map and finite
   actual owner scenario. Existing `launch.py/boot.py` may be reused unchanged:
   its required old `client/workspace.py` can remain an unused selected source;
   explicitly include the new module and complete transitive mixed/atomic
   closure. Do not loosen origin guards to accommodate an incomplete plan.

The genuine-A integration gate, once a real compatible receipt exists, uses
the new ordinary API: select A member(s), materialize demanded semantics,
author a substantive extension, publish it, close original owners, and cold
acquire/admit/import the exact resulting mixed packet through a surviving
provider. Root may combine this with the pending genuine-A reciprocal gate;
do not run the older fixture-specific `reciprocal_actual.py` and then repeat
the same boundary through this client. Its existing plan explicitly says
implemented-but-unrun and is not positive A evidence. Reuse valid setup/data,
not invented handles or old success flags.

**Source stop condition:** the new concrete client is implemented/reviewed with
distinguishing proof-free controls ready or narrowly passed; no unresolved
acceptance branch is covered by a mock. Genuine-A use remains a separately
identified integration gate, and economical aggregate production remains a
separate central obstacle. This source work can advance while producer memory
capacity is unavailable, without spending proof time or weakening the v5 goal.
