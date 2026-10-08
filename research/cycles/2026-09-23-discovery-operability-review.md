# Discovery and continued operation: bounded product inspection

Date: 2026-09-23 UTC. Author: independent `discovery_v1_gap` review.

## Scope and decision

Read-only inspection of the frozen `product-local/operator-source-05` public
interface, implementation and selected public operator replies. The canonical
workspace guard passed. No product operation, private-key read, native checker,
node mutation or source edit was performed. This checkpoint is not a runtime
test, mathematical audit or qualification of a new release.

**Decision:** prioritize a minimal owner-authorized append-only contact-addition
operation on initialized nodes in a separately selected successor. Do not run
another near-duplicate fold discovery test. The earlier independently audited
matched-consumer trial already demonstrated unknown-ID selection among seven
entries and substantive reuse. The current code supplies formal statement data
before acquisition; it does not force a caller to know a theorem identifier.
Its documentation and presentation seam may make broader selection expensive,
but no observed blocker currently justifies a search redesign.

The implemented finite owner commands permit further bounded work and service
without a bespoke test harness. They do **not** yet implement sustained evolving
participation in a large network: immutable contacts, finite lifetime ceilings,
one-view hosting and limited replica aggregation are actual product boundaries,
not merely missing second-machine evidence.

## Existing positive evidence must not be erased

The root directed this reviewer to two records, both now read:

- `deliverables/2026-09-21-local-v1-candidate/RESULTS.md`;
- `software/qualification/usefulness-consumers-01/COMPARISON.md`.

In that matched trial both fresh agents submitted and published the same full
polymorphic nested-fold target. Peer-assisted B independently chose the useful
append law from seven catalog entries, acquired and freshly admitted it, then
used its fully applied proof in the reachable induction proof. No root proof
repair or second submission was needed. Thus bounded unknown-ID selection and
substantive reuse are already demonstrated, not wholly missing.

B used more requests/stages and elapsed time than A, with lower observed Job
CPU but incomplete model/wrapper accounting and only one sequential pair. Those
records expressly reject a generalized speedup claim. Broader heterogeneous
recall remains unqualified, but a repeat of this fold mechanism would not be the
highest-value next action. The first drafting hypothesis for this review was a
mixed-corpus discriminator; reading this prior evidence displaced that proposal
in favor of the concrete initialized-node contact boundary below.

## What an independent agent can actually observe and do

Paths below are relative to the frozen `product-local/operator-source-05/`.

| Boundary | Implemented behavior and exact source |
| --- | --- |
| Local discovery | `find` enumerates an immutable local P1 cut, or selects one exact type-symbol posting; maximum four rows and 16 KiB per reply. Rows include `formal_metadata`, `symbol_keys` and a receiver-owned candidate handle. `py/node.py:294`; `py/storage.py:613`. |
| Remote discovery | `peer_find` needs only an already configured peer alias. It fetches the root/page zero, then pinned continuation pages; there is no target-ID argument. `py/peer_node.py:157`. |
| Information before acquisition | Each remote row contains the full advertised `formal_metadata`: `type_dag`, `universe_arity`, `symbols`, `native_ref`, `semantic_target`, descriptor and replay IDs, plus trace. `py/checking.py:260`; `py/peer_node.py:406`; exact field set `py/peer_wire.py:28`. This is richer than an opaque theorem identifier. |
| Selection and transport | The caller chooses a returned `remote` handle; `peer_acquire` receives its bundle, validates objects/closure and independently rederives and compares the complete advertised metadata. It creates a candidate, not mathematical acceptance. `py/peer_node.py:201`. |
| Mathematical use | `admit` checks one to four selected local candidates together with the current context and returns a new checked context. It returns exact receiving names and formal types; source submission uses those names. `py/node.py:235`, `py/node.py:343`; `API.md:125`. |
| Source contribution | `submit` accepts owner-authorized source and a declaration root; checking produces a private artifact. `publish` is separate and requires a current P1 snapshot. Neither discovery nor popularity can bypass checking. `py/node.py:243`, `py/node.py:348`; `API.md:127`. |
| Definition understanding | `manage.py inspect` returns a selected ordinary definition's canonical type/body and direct-reference names from an already admitted historical context. It is not a pre-admission remote preview facility. `py/inspect_context.py:129`, `py/inspect_context.py:156`; `API.md:154`. |

For a finite peer snapshot with `p` pages, successful traversal requires `p`
ordinary discovery calls (the first performs two HTTP downloads: root and first
page). A particular entry can therefore be found by enumeration without its
identifier, assuming service survives, pages fit their bounds and the agent can
interpret them. This is a reachability statement, not semantic search, useful
ranking or a cost bound independent of corpus size.

The received metadata is untrusted even when TLS authenticates its selected
endpoint. No theorem is accepted based on a persuasive statement or a familiar
symbol. Local rederivation and fresh receiving-native admission remain separate.

## The concrete discoverability limits

1. **Formal data is available; convenient pre-admission presentation is not.**
   `find`, `preview` and `peer_find` return canonical DAGs, not Lean `typeText`.
   `native/AgentClient.lean:68` reconstructs the checked context and generates
   the receiving name, formal type, and optional presentation-only `typeText`.
   That description is obtained through native admission, not free discovery.
   The selected actual `operator-02/a-seed-find.stdout.json` contains a full
   DAG and seed/external references; `a-seed-admit.stdout.json` additionally
   contains the readable Lean statement and receiving name. Thus the recent
   single-seed walkthrough is not evidence that an agent can discriminate
   relevant unfamiliar results before spending admission work.

2. **The packaged Markdown does not explain canonical DAG decoding.** It
   documents exact-symbol copying, the existence of the DAG, and inspection,
   but not DAG tag meanings, binder decoding or seed-reference-to-name mapping.
   The package contains code/assets from which an expert could reconstruct
   this information. That is an available fallback, not demonstrated ordinary
   agent usability. This is formal-math presentation, not a human-intention
   acceptance layer or a requirement for natural-language mathematics.

3. **Exact symbol membership is deliberately weak.** Local selection is one
   exact external-reference key in the type. It has no name search,
   conjunction/ranking, unification, unfolding, body search or equivalence
   matching (`API.md:66`). An entry expressed through a new definition may
   hide concepts relevant to the agent's investigation. Absence from one
   posting does not establish absence of useful mathematics. Shared elementary
   symbols can also select many irrelevant entries. These are limits of the
   predicate, not evidence that a richer index is already necessary.

4. **Remote discovery cannot use the local predicate.** It enumerates selected
   unfiltered immutable pages. View limits are 256 entries, 32 rows/64 KiB per
   page and 8 MiB aggregate pages (`py/peer_wire.py:13`; `PEER.md:77`). Real full
   statement metadata can cause substantially fewer than 32 rows per page.
   `complete:true` means only that one advertised view was exhausted.

5. **Contacts and catalog composition are narrow.** Configuration accepts at
   most two fixed peer aliases and one listener (`manage.py:54`). There is no
   peer recommendation, network traversal or automatic endpoint discovery.
   Ordinary `expose` selects only locally published entries
   (`py/peer_node.py:320`); an acquired-only candidate is ineligible even if
   admitted. `replica_expose` can serve exactly one original acquisition
   (`py/peer_node.py:364`). One holder cannot currently create a mixed catalog
   by combining several acquired-only entries through these public operations.
   Do not fabricate publication wrappers or bypass the owner API to hide this
   limitation in an experiment.

6. **Potential local framing blind spot, not an observed failed theorem.**
   `py/storage.py:594` permits a stored offer of up to 32,768 bytes. `find`
   refuses a first row whose full reply exceeds its maximum 16,384 bytes
   (`py/node.py:300`, `py/node.py:324`). The code does not prove that all
   admissible stored metadata fit that smaller discovery allowance. If a
   reachable offer has this shape, unfiltered pagination cannot step over it;
   `preview` needs a candidate handle already obtained elsewhere. This deserves
   a bounded source-only framing test if real corpus measurement encounters
   the range; no such runtime counterexample was executed in this review.

## Smallest central operability improvement

**Concrete obstacle:** after initialization a node cannot contact a newly
encountered participant through its public API while keeping that node's state.
This is not a theorem about network scalability; it follows directly from the
following implementation chain:

1. `manage.py:54` accepts at most two peer aliases during fresh configuration;
   its public command parser (`manage.py:244`) exposes no contact-update command.
2. `py/peer_node.py:126` resolves aliases only from `self.config["peers"]` and
   refuses an absent alias with `UNKNOWN_PEER`.
3. `py/node.py:115` hashes the entire configuration, including peer endpoints,
   into `config_id`; `py/storage.py:266` requires the initialized store to match
   that exact digest. Editing config is not a supported workaround.
4. A fresh node is possible but does not preserve the old node's contexts,
   handles, private work or history. Replica reconstruction of selected available
   mathematics is not migration of those facilities.

The smallest useful successor is a bounded owner command that **adds a new
alias bound to a full validated endpoint**, without rebinding old aliases or
editing immutable mathematical configuration. This is a recommendation, not a
selected schema or authorization to mutate operator05.

Required invariants for the small implementation:

- Only an explicit local-owner envelope adds contacts; received metadata cannot
  nominate a dial target. Addition performs no network operation and no
  mathematical acceptance. Existing strict IPv4/profile/TLS-pin validation is
  reused, without DNS, redirection, key rotation or broad peer discovery.
- Contact authority is bounded, durable and checked under the existing owner
  lock. Equal successful envelope replay is idempotent; conflicting alias/ID
  reuse refuses. Source/config pins and old mathematical records stay intact.
- Every selected snapshot/remote/acquisition continues to bind its exact
  endpoint. Adding an unrelated alias cannot redirect an old handle or change
  the interpretation of custody. In particular, update the existing
  `replica_custody` contact lookup (`py/peer_node.py:52`) consistently, not just
  `endpoint()`.
- Changing an endpoint uses a new alias in this first slice. Old aliases are
  not silently repointed, deleted or revoked. Explicit revocation and listener
  credential rotation remain different future work.
- Ordinary request/stage/byte accounting, exact replay, admission checking and
  published bytes remain unchanged. The new bounded contact facility does not
  increase lifetime authorization or claim indefinite operation.

Qualification should first cover native-free addition/replay/conflict/bounds,
unknown alias, malicious framing, and old-handle endpoint preservation. Then
one fresh successor allocation should initialize and perform checked work
**before** contact addition, add a new contact through the shipped command,
discover/acquire/freshly admit a genuine prior result, and continue normal
contribution without replacing that allocation. Audit unchanged earlier heads,
history and charges alongside the new operation's evidence. A separate small
negative test should show that unrelated additions do not let old selection
handles bind a changed endpoint. Existing frozen operator05 nodes remain intact.

This change is more directly consequential than another fold comparison or
adding a presentation helper without an observed selection failure: users can
join or extend an evolving cooperative neighborhood while retaining local work.
It is narrower than state migration, unlimited retention, a routing mesh or a
global discovery index. Larger-corpus formal presentation and benefit/cost
measurements remain worthwhile later tests, not prerequisites for this slice.

## Can ordinary owners continue without a bespoke harness?

**Yes within explicit finite allocations.** The public commands already offer
`status`, supplied-capacity `renew`, historical `select_context`, one-shot
`serve`, and multi-session `host`. An owner may author another hosting grant
after normal exhaustion; an agent can submit another request while capacity
and context limits allow it. A dedicated experiment harness is not an API
prerequisite. See `API.md:253`, `API.md:289`, and `HOSTING.md`.

**No claim of indefinite evolving operation follows.** Actual limits include:

- Lifetime authorization is at most 4,096 requests, 256 native stages, 64 GiB
  conservative reservation and 64 renewal grants (`py/capacity.py:13`). Renewal
  cannot raise these ceilings or clear uncertain pending work. Failed work is
  not refunded.
- Selected contexts contain at most 16 packages including the five common
  packages (`API.md:120`; `py/checking.py:243`). Historical selection avoids
  forced accumulation of every prior context but cannot shrink a theorem's
  genuine dependency closure.
- `host` repeats one immutable view under one finite grant, up to 128 sessions
  per grant and 360 seconds per session. The hosting journal has lifetime
  limits of 128 grants and 4,096 slots (`py/hosting.py:24`, `py/hosting.py:109`).
  Session transitions have listener gaps; no boot autostart, transfer retry,
  retention pruning, uninterrupted service or automatic grant renewal exists.
- A view does not automatically incorporate later contributions. The owner
  must explicitly expose/select and serve a new view; a reader's old snapshot
  need not remain online after that switch. Identity/address/profile changes
  require a fresh configured successor node, with no state migration or
  contact-update path (`PEER.md:187`).
- The supported recovery modes are narrow authenticated interruption/abort,
  not arbitrary power-loss repair or an indefinite availability guarantee.

These ceilings need not be removed to perform the next experiment, and this
review does not select a budget redesign. For a bounded small-cohort v1 they
can be honest operating limits. For the user's broader long-lived reciprocal
commons, a supported preservation/continuation path across contact changes and
finite-node exhaustion remains a central engineering obligation. Calling it
only an untested large-network scenario would understate the present code
boundary.

## Outcome

The existing architecture exposes unknown-ID formal candidates and has bounded
positive unknown-ID selection/reuse evidence; no theorem-ID prerequisite was
found. Broader heterogeneous retrieval quality and generalized efficiency remain
unqualified. The highest-value next action identified here is a bounded
owner-authorized append-only contact addition on initialized successor nodes.
Finite lifetime and preservation across eventual exhaustion remain later central
scope decisions; current finite `renew`/`host` commands are enough to avoid
redesigning them for this next slice. No frozen bytes or historical outcome
should be rewritten.
