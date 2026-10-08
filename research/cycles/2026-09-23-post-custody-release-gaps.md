# Post-custody v1 decision: one participant's shared catalog

2026-09-23. Independent read-only recalibration by `v1_central_gap_checkpoint`.
Canonical workspace guard passed. No product import, execution, test, service,
private-key inspection or source mutation. Source references below are relative
to `product-local/aggregate-custody-source-07/`. This is a prospective decision:
the ongoing installed source07 test is **not assumed to pass**.

## One recommended next capability

After an independently audited source07 pass, make **one managed catalog able
to advertise explicitly selected local publications together with explicitly
selected acquired roots**, retaining their distinct authorities. An ordinary
participant should not need to route its own publication through its own network
service, alternate incompatible catalog snapshots, or operate a second node
merely to share both what it learned and what it contributed.

This is a practical corpus-usability/cost obstruction, not a mathematical
impossibility and not a requirement that every participant retain all mathematics.
Select it only for the bounded v1 role of a participant that both contributes
and retains others' work. Pure producer and pure holder roles already have
appropriate separate operations; they need not be replaced.

## Evidence, not a missing-feature guess

Let P be roots backed by this node's local publication record and C be roots
backed by a client's successful exact acquisition. Source07 allows a committed
managed view selected from P or selected from C; it does not directly construct
a view containing both a P-only root and a C-only root.

- `py/peer_node.py:329` (`expose`) requires a local publication for each
  candidate. Admission of a received result does not manufacture that record.
- `py/peer_node.py:396` (`replica_expose`) accepts only acquisition handles.
  Plural support composes several custody roots, not publication and custody.
- `py/service_worker.py:48,58` separately enforces homogeneous authority using
  `VIEW_MIXED_AUTHORITY`. Hand-building a mixed inert view does not make it
  eligible for managed service.
- `manage.py:55` and `py/node.py:93` permit at most one configured TLS listener.
  More importantly, `py/service_worker.py:102` holds one services-domain owner
  lock across the entire service: two separately selected views cannot be
  served concurrently by two managed sessions on the same node, even with
  different explicit loopback ports.
- `HOSTING.md` binds one immutable view per finite grant. Alternating views is
  possible, but a discovery query sees only the current advertised view;
  later requests for the displaced snapshot may refuse. It is not combined
  discoverability or a safe implicit union of distinct snapshots.

A contribution's dependency closure may contain earlier mathematics, but that
does not necessarily advertise each earlier root as its own discoverable entry.
The obstruction is clearest when the selected retained root is unrelated to
the new local publication. Do not manufacture wrapper theorems to represent
custody as authorship/publication.

## Existing workarounds and their actual limits

**Two nodes:** separate state/scratch domains and listeners can supply separate
views. This is a valid architectural alternative, requiring an additional
configured node and contact plus receiver-side enumeration of both endpoints.
It avoids mixed authority but increases operator and discovery work. No new
two-node experiment is needed merely to rediscover that published interface.

**Self-acquisition:** source inspection permits a more direct workaround, but
it has not been qualified as a full workflow. Configure/authorize a peer alias
for the node's own endpoint; expose its local publication, serve that view,
discover/acquire the root through that alias, then put the resulting acquisition
alongside the other acquisition in a pure `replica_expose` view. Endpoint
validation has no self-endpoint exclusion. Service closes its read-only control
connection before the listening loop (`service_worker.py:132`), while ordinary
requests use a different lock. `PeerOperations.reuse` (`peer_node.py:257`) can
reuse an exactly equal existing offer, and acquisition still records custody.
This is source-feasible, not a promise that any selected resource allocation
or package will succeed.

Relative to one direct mixed exposure, starting with an unexposed publication
requires three extra ordinary requests (`expose`, `peer_find`, `peer_acquire`),
**152 MiB** additional conservative reservations (80 + 8 + 64), one finite
owner service and retained transfer/custody bytes. If its publication view
already exists, the marginal overhead is two requests / **72 MiB** plus service.
One small nonempty catalog uses three successful connections (root, page,
bundle); more pages cost more requests. No additional native stage is needed
for custody. The final pure-custody service starts only after the self-serving
session ends. These are API accounting estimates, not measured CPU/disk costs.

Thus absence of direct mixed exposure is not inability to exchange mathematics.
It is a recurring artificial operational tax on the project's ordinary
learn-and-contribute role, with finite contact, request and retained-byte costs.

## Smallest executable successor, not a new architecture

Preserve existing `expose {selected:[...]}` and both `replica_expose` envelopes.
Extend `expose` with one optional nonempty `acquisitions:[...]` selection when
`selected` contains local-publication candidates. This makes the new case
explicit without introducing another operation, wire format or database table.
Define output order as publication selections followed by custody selections;
combined count and aggregate byte/resource bounds remain unchanged.

Reuse the existing publication validation and `selected_replicas`/custody chain.
Reauthenticate both authority classes at commit, retain their existing per-row
shapes, and let managed service validate each row under its own branch. Do not
convert custody to publication or transfer acceptance. Reject repeated local
sequences/descriptors/bundles across the combined selection, and fail the whole
view if any row fails. Preserve each acquired entry and original bundle exactly.
Retain receiver-local fresh `admit`, replay semantics and all finite limits.

The next executable assignment should be this bounded API/source change in a
separately selected successor, followed by focused native-free authority/limit
contracts and **one** installed discriminator: one genuine locally published
root plus one genuine acquired-only root appear in one managed catalog; after
the original supplier stops, a fresh receiver discovers and freshly admits
both exact roots. Prefer already audited mathematical source/packages; this is
not another proof-research contest. Preserve old sources, failed runs and costs.

Stop at independent scoped outcome audit or a concrete failed invariant. Do not
re-run the passed pure-custody, seven-entry fold search, contact or whole
operator-authoring studies merely because the source successor has a new name.
There is no need to commission another registry hierarchy or formal module.

## Classification and convergence

**Missing implementation:** direct mixed-authority managed exposure, as shown
above. Its absence is intentional in source07; selecting it next would expand
one deliberate v1 usability boundary, not repair a false source07 promise.

**Missing evidence:** installed plural source07 outcome/audit is still pending
at this review. Mixed exposure, if implemented, requires its own scoped evidence.
Current evidence already includes independently authored reciprocal successors
([operator05 qualification](../../experiments/operator-onboarding-01/QUALIFICATION.md))
and unknown-ID useful selection among seven entries
([matched consumers](../../software/qualification/usefulness-consumers-01/COMPARISON.md)).
Those are not evidence of broad retrieval quality, sustained growth or speedup,
but they also are not absent capabilities requiring identical new trials.

**Deliberately unsupported scope:** indefinite nodes, general backup/restore,
profile/database migration, global completeness, broad library compatibility,
large-network performance and automatic retention/ranking. Unexposed material
at irreversible quota exhaustion remains a real separate limitation; planned
exposure plus compatible fresh-node transfer is the existing bounded policy.
The source07 test may qualify service after ordinary authorization exhaustion,
not after damaged state or actual consumption of every lifetime ceiling.
None of these limitations is erased by mixed exposure.

The source07 `CORE.md` opening incorrectly presents config/store 4 and stale
qualification status; selected README/API say config 6/database 5. Fix this
and related live support labels in the next source/handoff pass, without
rewriting frozen package evidence. It is a release consistency defect, not the
central operational capability chosen above.

No second host, public deployment, license decision or proof of exponential
growth is required to execute this next local step. The ultimate goal remains
unfinished; a narrow pass supports an honestly bounded release decision, not
an endless sequence of optional feature prerequisites or a perfect-v1 claim.
