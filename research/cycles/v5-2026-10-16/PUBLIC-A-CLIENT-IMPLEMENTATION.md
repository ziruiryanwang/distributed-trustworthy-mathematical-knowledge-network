# Public A-capable client: implementation checkpoint

Owner: `memo_tests_review`. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
Root selected only new `software/v5/client/workspace_mixed.py`, `API-MIXED.md`
and this checkpoint under `PUBLIC-A-CLIENT-SELECTION.md`, implementing the full
`PUBLIC-A-CLIENT-SEAM.md` design. Guard passed; instructions/design were read.
No imports, tests, native calls, proofs, builds or Git operations were performed.
This checkpoint is source evidence, not a runtime or release pass.

Current author-ready pins before independent review:

- `workspace_mixed.py`:31,054bytes, SHA256
  `eb4e9374707b3e3f03b7e60ad91fd0fd30a3872d3e9fb59fe3f93c039338acbd`.
- `API-MIXED.md`:8,978bytes, SHA256
  `4a809b43d32e7fc5888ce9dda7e994817610006bc1d0a338bc83963786b3383c`.

## Implementation boundary

The concrete `Workspace`/`CommonsClient` subclasses preserve the I-only atomic
base. A is required, I optional, preparation optional. Exact original owner
objects and actual owner profiles are bound to the new workspace's mixed wire
profile. One original grant and one `AcquisitionBudget` cover I/A/mixed admission.
The new direct API is `admit_aggregate_member(receipt_bytes, expected_header,
exact_journal, index, siblings, *, cpu_seconds=30, wall_seconds=60,
memory_mib=1024) -> LiveWarrant`.

Receipt caching keys A/profile/hash/length/exact header. There is deliberately no
member-token cache: every selection invokes actual issuer membership binding
and issues a client-local `A-member` reference. Original receipt bytes and
genuine member handles stay in the client registry. Known byte-valued facts are
normalized only for comparisons; no dictionary is promoted into an issuer handle.

The code reuses the existing mixed packet parser, receiver, atomic imports,
immutable materialization, owner authoring, custody and acquisition. It adds no
checker, proof format, generic plugin registry or source-selection exception.

## Exhaustive inherited/overridden method review

Every baseline method was read before implementation. Its50,535bytes remain
SHA256 `01eefed1804ec5f296aebfcc12441dd283cd77c9bac8f8d5b02e8a4becc5e8c1`.

| Boundary | Treatment and reason |
|---|---|
| Workspace `open` | Explicit successor; does not call I-only constructor. New schema, exact mixed profile and `mixed_network.PacketStore`; same lock/ledger/reopen mechanics. |
| Workspace `operation` | Explicit exact A/I/delta transfer; ownership changes only after complete construction and ledger record. |
| Workspace `status` | Reuses neutral counters and overrides old lexical schema. |
| Workspace `_active`, `_record`, `reserve`, `_grant_active`, `history`, `read_record`, `_release`, `close` | Inherited; config/registry/lifetime/storage operations are profile-neutral. Grant records remain nonrestartable historical data with the existing grant schema. |
| Client `__init__`, `_active` | Replaced; exact A-required/I-optional types, original object identities, profiles, source origins, deadlines, pristine owner state, suballocations and exact mixed storage. No old I-only initializer call. |
| Client `_census`, `_enter`, `_charge`, `_store` | Inherited finite bookkeeping; dynamic `_active` uses mixed rules. |
| Client `_fail`, `close`, `report` | Replaced; close original transferred A/I/delta/preparation and import session, clear all references, preserve cleanup uncertainty and original owner accounting. |
| Client `_issue`, `_warrant`, `describe` | Replaced; closed I/A-member/mixed dispatch, known byte-field normalization, exact live fact/profile/hash/length binding. New `_live_fact`, `_bind_fact`, `_aggregate_fact` are private helpers. |
| Client `admit_receipt` | New outer serialized guard rejects absent I; reuses the frozen unwrapped implementation body, so no double `_enter` or fresh allowance. |
| Client `admit_aggregate_member` | New genuine A receipt/member path and exact same-live receipt cache. All submitted bytes and member work remain charged. |
| Client `_admit_packet` | Explicit successor passes selected A to parser; same claim/delta reservation and actual receiver. |
| Client `admit_local` | Inherited; actual mixed PacketStore inspection and overridden `_admit_packet` supply profile-specific behavior. |
| Client `find` | Inherited unchanged: `FrontierLocatedHandoff` and `MixedLocatedHandoff` are the identical existing `DeltaLocatedHandoff` class. New `_active` explicitly checks that identity. Routing/search remains advisory. |
| Client `search_offer`, `search_page`, `_candidate`, `describe_candidate`, `packet_offers`, `acquire` | Inherited neutral search/byte/semantic workflow. Actual acquisition is created by overridden `resolve`; exact client candidate membership and warrant revalidation remain. |
| Client `resolve` | Explicit `MixedAcquisition.from_search` with selected A profile and the same handoff/budget. No I-wire fallback. |
| Client `_context_data`, `import_context` | Replaced; actual A owner enters unchanged atomic session; A-member dispatch calls `use_aggregate_member`. |
| Client `_live_context`, `extend_context`, `author` | Inherited immutable selected-view and actual preparation workflow; calls concrete mixed-aware context/session. |
| Client `_semantic_plan` | Same bounded structural extraction, with explicit selected A passed to parser. |
| Client `semantic_material` | Direct A requests caller/provider semantics; I/mixed use the frozen unwrapped bounded implementation and dynamic mixed `_semantic_plan`. One serialized wrapper. |
| Client `_publish`, `publish`, `reconcile` | Inherited structural custody/index/intent/recovery workflow. Dynamic mixed `_semantic_plan`, new exact stores and fail-stop `_active` supply changed boundaries. No publication-as-proof claim. |

Tokens and `OperationGrant` use the unchanged exact classes plus per-workspace/
per-client registries; matching type alone never restores authority. The selected
source closure must include the inherited atomic module. The client additionally
requires exact owner pins/import origins for itself, its base, client package
and mixed network package/custody/transport. All transitive source/runtime
selection and actual executable adoption remain the root's responsibility.

## Pre-review corrections and efficiency

Root identified that detecting a substituted owner is insufficient if cleanup
then closes only the replacement. The implementation now closes the frozen
original-owner tuple and reports those originals; a replacement is not thereby
transferred. Cleanup errors set persistent `cleanup_uncertain` and workspace
poisoning. A later successful close cannot erase that uncertainty.

Initial issuance no longer immediately describes the same member twice. A pure
`_bind_fact` checks the already returned genuine fact; later warrant use still
performs genuine issuer revalidation. Likewise I/mixed semantic extraction uses
its existing revalidation once. These remove duplicate source/install scans in
the wrapper logic; no timing or full-workflow speedup is claimed.

## Required evidence and remaining limits

The independent controls lane owns fresh synthetic exact-class fixtures and
changed-boundary tests; no old passing campaign is repeated. Product code has no
synthetic mode. Independent source review and root's exact finite runtime
selection are still required before any import or test.

Direct A is local/bootstrap; the existing remote packet target is its last
substantive delta. This seam does not silently add standalone A-member transport.
Actual current-image A receipt production, public A authoring/cold reuse and all
other final-v5 requirements remain open. No real A receipt or economic benefit
is invented by finishing this source work.
