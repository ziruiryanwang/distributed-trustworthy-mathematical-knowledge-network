# Expose selective existing postings in one bounded query

2026-10-20, root. Source implementation only, no runtime/build selected.

Root read/adopts POST-CUSTODY-DISCOVERY-DECISION (`8f22aa5b`), including the
exact three-atom hot-first/rare-later construction and additive-query proof.
Keep the eight-feature wire cap, unchanged profiles/postings and legacy route
keys. Adding eligible redundant pair keys cannot increase the sum of selected
anchor counts; it can increase summary cost. Under correct feature extraction,
the requested predicate is unchanged. This is not universal recall or total-cost
dominance. Overflow must be explicit rather than called an optimal plan.

core_release owns three new successors under `software/v5/pair_planning/`:

- `discovery/module_export_adapter.py`, from current instantiation_discovery;
- `client/direct_contacts.py`, from current iterative_queries;
- `client/located_queries.py`, from current located_queries.

Add `plan_query(specs)` while preserving `compile_query(specs)` exactly.
The direct/located helpers gain strictly Boolean opt-in `plan_pairs=False`;
their default features/routes/reports remain unchanged. Opted-in calls construct
one immutable session with legacy features plus bounded eligible pairs, retain
all old route subsets, and report finite planner coverage/fallback. Do not bind
raw caller feature hashes or change active sessions, provider advertisements,
original budgets, authority, owner pins or grant clocks.

Root owns new focused native-free controls. Reuse real structural codec/store/
summary/page code for a constructible hot/rare corpus; check cap overflow,
default compatibility, old route subset preservation, and actual direct/located
factory binding. No repeat of the already passed pair-storage controls, no Lean
proof, network campaign or installation build merely for this source change.
adaptive_audit reviews exact source/control changes after current installed02
outcome. An independent review and fresh finite selection precede any runtime.

Batch a later coherent installation when justified; do not rebuild the unchanged
842 MB payload per small editing step. Root alone owns integration/adoption/Git.
