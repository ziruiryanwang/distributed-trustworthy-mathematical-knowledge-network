# Mathematical commons v5 — development source

This is the single evolving v5 source tree, not a completed release. The frozen
v4 distribution is unchanged. Current architecture, ownership and open gates
are in `../../research/cycles/v5-2026-10-07/PLAN.md` and `DECISIONS.md`.

- [Ordinary runtime construction](client/RUNTIME.md): owner-adopted runtime
  configuration without fixed theorem/receipt/experiment inputs.
- [Serve a retained workspace](client/SERVING.md): ordinary finite HTTP service
  over existing index, semantic and packet stores, with explicit ownership and
  shutdown. No fixture-specific server driver or mathematical issuer is needed.
- [Discovery rejection isolation](client/SEARCH-VALIDATION.md): keep existing
  live work after a classified invalid index reply, within the original budget.
- [Evidence client API](client/API-EVIDENCE.md) and
  [demand-only staging](client/STAGING.md): acquire, verify and reuse selected
  mathematics through the existing exact owners.

- `modules/`: new certified declaration/import/demand relation.
- `discovery/`: formal-feature index, committed snapshots and bounded queries.
- `workloads/`: independently checkable reusable methods and growth comparisons.

Use exact source snapshots and fresh bounded run records. A component test is
not mathematical certification or a claim of global deployment readiness.
Project license remains undecided; preserve all third-party notices.
