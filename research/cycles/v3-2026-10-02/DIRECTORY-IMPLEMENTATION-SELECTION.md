# Production directory successor: first maintained hot-key split

2026-10-02 UTC. Owner: /root/scale_implementation. Canonical root:
E:\Distributed Trustworthy Mathematical Knowledge Network.

SOURCE_SELECTION_ASSESSMENT_ONLY. No product edit, import, build or runtime.
Inspected source04 `cert_route_store.py`, `cert_route.py`, peer dispatcher hooks,
and the September 30 DIRECTORY-TRANSITION-CONTRACT. Workspace guard passed.

## Minimum editable leaves

1. `cert_route_store.py`: fresh StoreV2; view-qualified ads and indexed durable
   fences, cuts, placement status, reservations, activation and locator records.
2. `cert_route.py`: strict WireV2 validators, bounded public read/write hooks,
   shared caller accounting, local owner-transition commands and split-aware
   discovery/publication. Reuse endpoint policy and existing TLS transport.
3. `cert_peer.py`: narrow dispatcher adaptation. Current GET delegation accepts
   only `/route-v1/`; POST accepts only `/route-v1/announce`. These must admit
   specifically validated `/route-v2/` public endpoints, not arbitrary hooks.
4. `CERTIFIED-NETWORK-API.md`: schema/CLI contracts, maintenance costs, support
   envelope, refusal meanings and locator-refresh duty.

No Lean, certificate, namespace, custody, workflow, identity or proof changes.
Root must create/select a fresh successor; source04 stays frozen. New stores
refuse V1 files rather than silently reinterpret or migrate their targets.

## Concrete durable interfaces

AdStore operations bind `(namespace,key,view_id,partition)` throughout.
`put(..., absolute_expiry, reservation_id=None)` atomically enforces quotas,
matching partition and fence; ordinary publication still derives discovery keys
from owned certified bytes before dispatch. `status(exact_identity)` returns
exact offer/holder/expiry/revision, not a first-four broad approximation.

Local-owner `fence(X)` commits immutable successor slot, write fence and
`{store_id,cut_id,max_sequence,row_count}` in one transaction. Refresh, expiry
and insertion cannot change pinned rows. `cut_page(cut_id,after_sequence,B)`
uses `(view,target,sequence)` index; strict monotonic cursor, count and terminal
marker establish complete enumeration for correct stores. Bounded union checks
exact descriptor agreement and retained maximum expiry; no global scan.

Local-owner `reserve(X,partition,rows,bytes,expiry)` charges capacity before
copying. Selected child `put` followed by exact `status` confirms two replicas
per union row, with expiry at least old expiry plus `2*epsilon`. Reservations,
partial copies and pinned cuts remain charged after any refusal/crash.

`activate(X,coverage_transcript)` checks every old cut, exact two-copy coverage
and leases before committing append-only activation. All three old activation
statuses are required for ACTIVE_ALL. Local commands use a caller-selected
bounded maintenance plan; publishers cannot remotely fence or activate shards.
Public reads return tagged one-hop X after activation. Every peer attempt,
page, row and byte reservation uses the original operation ledger/deadline;
failures are not refunded and referrals never allocate a fresh Budget.

## Necessary addition: reachability after redirect expiry

The existing contract **does not** cover this: section 9 assumes independently
learned V1 or a maintained entry path. Its old-view lease bound only protects
already admitted stale readers. A hot-key split alone is insufficient.

Add `locator_put(namespace,key,generation,parent_digest,view,lease)` and
`locator_get(namespace,key)` at three explicitly configured rendezvous replicas
reachable through existing finite entry routing. Durable compare-and-set slots
refuse conflicting successors; no consensus/latest-view claim. Two exact
post-write confirmations plus attempts to all three tolerate one inaccessible
replica while their leases hold. Current locator rows are small paid metadata,
not permanent retention of old theorem ads or old view histories.

Before redirect retirement, confirm two fresh current-view locator copies
through the declared fresh-query horizon. A finite owner `locator-refresh`
renews them explicitly and records costs; absence/expiry yields INCOMPLETE,
never global empty. Reads start from the stable namespace/key locator target
and obtain V1 even after old redirects/cuts are reclaimed. V1 then directs the
two child partitions; exact known-bundle lookup selects one.

This implementable first slice provides conditional one-split maintained
reachability, not arbitrary churn, automatic repair or universal recall.
Changing rendezvous membership needs its own bounded migration; permanently
assuming fixed live contacts does not close huge-network maintenance. Broad
candidate opportunity, clock-skew assumptions and holder availability remain
explicit. Directory records confer no mathematical validity: acquisition still
rederives key/type and locally checks the certificate independently.
