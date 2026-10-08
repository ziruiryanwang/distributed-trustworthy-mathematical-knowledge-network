# Post-operator central gap: add a new peer without abandoning a working node

2026-09-23. Read-only triage; no product execution or source edits. Canonical
workspace guard passes. Root owns integration selection and launch. Frozen
operator05 and every used installation/state remain unchanged.

## Decision

**Select a small owner-authorized, append-only peer-contact addition operation
for the next successor.** Keep existing contacts immutable; allow a bounded
number of newly named contacts after initialization, without resetting the
node, changing old endpoint bindings or granting mathematical authority.
Then test one third-peer use on preserved state. Do not commission another
near-duplicate fold comparison or build semantic search, a DHT, global identity,
unlimited renewal or a general migration system first.

This recommendation corrects the initial triage hypothesis that useful mixed-
catalog selection was wholly missing: it is **already demonstrated in a scoped
predecessor comparison**, as detailed below. The new obstacle is an actual
missing operation, not merely a request for wider statistical evidence.

## What already works, with the proper evidence boundary

- [2026-09-21 results](../../deliverables/2026-09-21-local-v1-candidate/RESULTS.md)
  record two no-history matched consumers that both proved/published the exact
  63-node chunk-reduction type. Peer-assisted B independently selected from
  **seven entries** and used the received proof in its checked induction.
  Total public Job CPU was 288.515625 seconds for A and 275.125 for B, plus
  0.15625 serving CPU for B; source/corpus preparation was separately charged.
  B took longer elapsed time. This is genuine practical discovery/reuse, not
  a causal speedup claim and not evidence about every later source cut.
- Operator05 now has the terminal assisted second-attempt run. Its
  [operator report](../../experiments/operator-onboarding-01/operator-02/OPERATOR-RESULT.md)
  records package-driven setup and two successive independently chosen
  contributions on preserved nodes. [Beta](../../experiments/operator-onboarding-01/BETA-MATH-AUDIT.md)
  and [Alpha](../../experiments/operator-onboarding-01/ALPHA-MATH-AUDIT.md)
  mathematical audits pass exact source/type/proof use and final return.
  Root's operational/cost consolidation is separate; do not promote this
  triage into its pass. The first failed setup and source revision remain.
- Actual discovery is not just opaque IDs: `py/checking.py:260` supplies
  formal type DAG, universe, semantic/native references and symbols;
  `py/peer_node.py:406` returns the complete advertised entry plus local
  selection handle before acquisition. Remote pages are unfiltered and
  presentation is sparse, but the current API is not incapable of selection.

## Concrete obstacle in the selected code

All references below are to frozen `product-local/operator-source-05`.

| Boundary | Actual implementation | Consequence |
| --- | --- | --- |
| At most two initial contacts | `manage.py:54,65`; `py/node.py:68` | A third configured peer is refused. |
| No later contact addition | `py/peer_node.py:125` resolves only `config["peers"]`; unknown aliases refuse | Even a known, owner-approved third endpoint cannot be used by an existing node. |
| Old handles bind endpoints | `py/peer_node.py:157` and `:200` compare snapshot/acquisition endpoint with configured endpoint | Hand-editing config or repointing an alias is not a safe workaround. |
| Config/state are pinned and no in-place migration is provided | `API.md:238` onward; `PEER.md:189` | The documented alternative is a fresh successor node, not reconfiguration of the working one. |

This limitation is immediate, not hypothetical scale arithmetic: operator02
Alpha has already consumed both slots with `seed` and `beta` while still having
13 request credits and four native stages left. It cannot investigate a third
independently supplied publication with that preserved working context through
the supported API. A fixed two-neighbor topology can propagate selected bytes,
so this is not a proof that every degree-two network is impossible; it is a
concrete obstacle to ordinary local agents changing their information sources.

## Smallest consequential implementation

Add a **separate owner operation**, not a generic peer response or an ordinary
agent-controlled destination. Reuse existing endpoint validation, local owner
lock, bounded state accounting and exact-envelope replay patterns. The selected
contract needs only:

1. An envelope binding the immutable node configuration, fresh owner operation
   ID, new alias and exact existing transport-profile endpoint/DER pin. Record
   it in a bounded authenticated local contact table/journal. A small fixed
   ceiling such as 16 total contacts is sufficient for this slice; it is a
   prospective support choice, not a scalability claim.
2. Addition only: an existing alias cannot change address, profile or pin, and
   alias reuse with different bytes refuses. Existing configuration contacts
   and their endpoint bindings remain exactly as before. Rotation/revocation
   and automatic peer discovery are explicitly not part of this change.
3. Exact-envelope replay must not add another contact or spend a second grant;
   interrupted/unknown outcomes use the same ID/envelope. Fresh additions
   require initialized, quiescent state and bounded metadata headroom. No
   network call, key read, source execution or mathematical stage is performed
   by contact administration itself.
4. New `peer_find` calls can use the added alias. Stored snapshot/remote handles
   continue to bind their original endpoint; addition cannot redirect them.
   Fresh local admission remains the only mathematical acceptance boundary.

Implement only in a separately selected successor copied against operator05's
complete 114-file map. Explain every changed payload and any required storage/
configuration profile change. Do not mutate operator05's used code/database,
or infer an old-state migration guarantee from a new successor's capabilities.
The tested preservation claim is *within the new running profile*.

## Simpler alternatives, and why they do not close this gap

- **Keep two contacts and create a fresh node:** supported for selected
  available mathematics and remains an honest fallback. But it imposes fresh
  bootstrap, reacquisition/rechecking and new local handles just to choose
  another supplier; it does not preserve the existing working context.
- **Raise the initial two-contact constant:** cheap, but still requires
  predicting all future peers before initialization. It does not implement
  the missing post-initialization action.
- **Ask the present supplier to relay everything:** may work when that supplier
  voluntarily has the needed bytes; it is not assured local access to another
  willing supplier. `replica_expose` is one acquisition (`peer_node.py:364`),
  while ordinary `expose` requires locally published entries (`:320`). Do not
  pretend the existing API already aggregates arbitrary acquired catalogs.

## Bounded decision-changing gate

First use native-free contract checks for owner-only scope, endpoint/schema
refusal, alias conflict, exact replay, capacity, busy/pending state and retained
failure. Then one local real-TLS test on a fresh successor node:

- Initialize with two contacts, obtain one real checked context and a pinned
  remote selection from an initial contact. Record context/P1/usage and config.
- Add a third named peer once through the owner API; replay the exact envelope
  once. Require one added contact and no reset of context, catalog, counters or
  original config/endpoint authority. Conflicting alias bytes must refuse.
- Use the preserved old selection against its original endpoint, and use
  `peer_find`/`peer_acquire` on the new alias to obtain a **different genuine
  already qualified publication**. Freshly admit the latter using the same
  preserved node, retaining its exact type/reference/foundation.
- Require inert acquisition, final quiescence, no pending work, bounded charged
  metadata/resources and complete observed administration/transfer/check cost.
  No new mathematical theorem, repeated multi-round proof chain, external
  listener or new identity fixture is necessary to test the changed slice.

Root should fix a short finite allocation before execution: one new receiving
node, three contacts, one addition plus one replay/conflict, at most three
native stages including initialization and admissions, and finite existing
TLS service grants. If the proposed source change expands into migration,
revocation, autonomous routing or unlimited service, stop and narrow it. If
the existing profile already offers the action through a demonstrated public
path, use that path instead and do not implement a duplicate.

## Lifetime ceilings: actual limitations, but a separate next decision

`py/storage.py:18` fixes 4,096 requests, 256 stages and 64 GiB cumulative
authorization; `API.md:277` records 64 renewal grants. `py/hosting.py:24-25`
and `:368-376` cap 128 host grants and 4,096 sessions. These are hard lifetime
limits, **not** a tested indefinite-renewal capability. The operator run did
not approach them; it cannot diagnose their practical exhaustion cost.

Do not remove those constants merely to advertise long-running operation.
A supported node-lifecycle handoff or retention/accounting redesign needs its
own preservation argument and bounded experiment. Selected mathematics can
already survive in compatible custody and be freshly checked at another node;
that does not restore all local contexts, handles, private drafts or history.
Choose that lifecycle slice next when defining long-lived support, rather than
combining it with contact addition and weakening both boundaries. No per-node
infinite-lifetime promise is justified by either current or proposed v1.

Remaining release boundaries still include Windows/NTFS and exact runtimes,
finite contexts/catalogs/storage, limited supported Lean capture, no general
restore/upgrade, conditional availability and no independently hosted test.
License/publication remain owner decisions. Wider heterogeneity, relevance,
duplication and amortized useful-work cost remain empirical questions; reuse
the existing matched evidence and complete operator accounting before spending
another experimental allocation on them. A bounded deployable v1 need not
prove exponential growth or solve every future network mechanism first.
