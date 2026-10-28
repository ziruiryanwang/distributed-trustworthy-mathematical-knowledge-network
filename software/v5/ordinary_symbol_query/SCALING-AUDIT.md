# Query preparation: source-only scaling audit

2026-10-28. Advisory design finding only; no implementation, runtime, database,
artifact inspection, imports, native work, tests or Git operations performed.
The current symbol-query successor remains separately reviewed and unchanged.
Paths below are relative to `software/v5/`.

**Conclusion:** snapshot-byte reads are not logically needed to project exact
names from an owner-recorded checked root for advisory search. They establish
snapshot integrity/availability, not the name projection. Removing them can
preserve the current conditional search provenance and mathematical acceptance,
provided the result explicitly does not assert that the context is load-ready.
Do not mistake this for constant-cost lookup or change the admission path.

## Current cost and the hidden opening path

- `ordinary_symbol_query/query.py:316-332` opens custody and OrdinaryAdmission,
  asks for the full context, then projects only the requested names.
- `ordinary_lean/portable_catalog.py:530-549` walks every ancestor through bounded
  root records; `:492-528` validates records, builds every binding and module plan.
  Its `_validate_record` ends with snapshot verification at `:490`; `_artifact`
  hashes the whole file at `:319-332`, cached only within that owner process.
- Crucially, `PortableCatalog._open:239-240` already calls `context` on the
  activation's selected imported root. `ordinary_parse_reuse/ordinary_admission.py:
  515-516` uses that opener. Changing only query.py:321 leaves this cold I/O intact;
  it can include imported roots beyond an earlier explicitly requested root.
- For lineage depth D, metadata bytes M, names N and retained snapshot bytes A,
  cold context work includes O(M+N+A) byte/name work and O(D+N) bookkeeping,
  plus database access. Imported opening can repeat metadata work before lookup;
  verified overlapping artifacts are not rehashed in the same process.
- Full cost also includes package/runtime verification: `ordinary_parse_reuse/
  ordinary_admission.py:254-255,285-296` hashes installed support. Removing
  snapshot I/O does not remove this fixed package cost or imply measured speedup.

## Smallest concrete seam; preserve existing identity

First candidate: a separately pinned **query-only facade** over the unchanged
catalog validators, retaining full metadata validation initially. Its internal
reader can specialize only `_artifact` for the already validated generated
`operations/.../chunk.olean` and `imports/.../chunk.olean` paths: validate declared
size/hash/path metadata, but do not open/hash snapshots. Delegate all other
artifact handling unchanged, notably the import audit. The inherited open's
eager `context` then uses this same advisory policy, so it cannot secretly hash
the snapshots first. Return only root/identity/name projection, never a module
loading plan; expose no reserve, commit, import, or admission capability.
This is a source seam for review, not an existing public lightweight API or an
instruction to monkey-patch the live owner. A private facade/subclass should
remain confined to this helper and explicitly disallow create/admission use.

Keep the installed core bytes and implementation descriptor unchanged. Editing
portable_catalog.py in place changes controller support (`ordinary_parse_reuse/
ordinary_admission.py:232-243`), hence implementation ID, adoption-marker equality
and native local-root identities (`ordinary_lean/ordinary_semantics.py:170-172,
210-224`; portable_catalog.py:165-181). The auxiliary-package route avoids an
unrelated migration or relabeling old checking. No new database schema is needed.
Using the current OrdinaryAdmission.open instead defeats the facade; the query
must open it directly. Custody is unnecessary for projection itself and can be
omitted in a separately selected query lifecycle, preserving path isolation,
exclusive owner lock, liveness checks, cleanup and publish-only-after-close.
Reusing the existing opener still performs reservation recovery (`:237-238`),
so do not call this database-read-only. Changing recovery requires separate review.

## What must remain, and what this does not solve

- Preserve marker/store/semantic/implementation/activation equality, WITHDRAWN
  and closed checks, owner lock and bounded parsing (`portable_catalog.py:145-188,
  227-241,265-317`). Never query unlocked raw SQL or trust an arbitrary supplied map.
- Preserve full ancestry, basis, no-shadow/duplicate checks and all limits
  (`:390-419,492-516,539-547`). A hit cannot justify early exit if later ancestors
  could reveal a conflicting duplicate; a miss requires complete selected lineage.
- Preserve imported record digest/ordinal and migration provenance: import audit,
  correspondence, source-record hashes and name correspondence (`:334-388,
  440-489`), plus source/module parent chains (`:496-507`). These are metadata
  reads, not proof-snapshot reads; skipping all `_artifact` calls would lose audit
  integrity. No reconstruction of V1 names or new portable identities is needed.
- Native root IDs do not independently authenticate the binding-map contents:
  actual-check commit and protected immutable local records remain premises
  (`:637-674`; ordinary_semantics.py:210-224). Snapshot hashing already does not
  recompute those bindings. This proposal neither fixes nor enlarges that premise.
- Missing/corrupt snapshots may now yield a valid advisory projection. State this
  as `snapshot_integrity: NOT_CHECKED`, never context-ready/custody-ready. Subsequent
  ordinary admission/use must retain original context/snapshot verification.
  Withdrawal, changed activation, damaged metadata and closure failure still refuse.
- Fixed-basis helpers (`ordinary_basis_query/query.py:131-148`) derive IDs from the
  pinned inventory but do not establish membership in an arbitrary selected root.
  Manual bindings and cached reports likewise cannot silently replace current
  root provenance. Anchor querying still calls context (`ordinary_anchor_query/
  query.py:201-217`), so it is not an existing snapshot-free escape hatch.

The first seam removes A, not M or N. A later projection can avoid materializing
all symbol values/module plans, but current JSON records and no-shadow checks
still require scanning all names; memory for a checked-name set remains O(N).
Sublinear cold membership/absence needs maintained root-bound lookup commitments
or authenticated cached projections with explicit lifecycle rules, a larger design.
Select that only if metadata cost is the decision-changing bottleneck. For now,
review the bounded artifact-policy facade before any new schema or performance run.
