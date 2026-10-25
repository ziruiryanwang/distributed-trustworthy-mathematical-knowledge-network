# Protected fixed-basis anchor: source handoff

2026-10-24. Source successor only; not imported, compiled, executed or adopted.
Owned files: this note and `source_anchor.py`. Frozen grounded-cut predecessor is
unchanged. Root owns integration/selection and independent reviewer owns assurance.

## Shared interface

- `capture(native, selected_root, *, check) -> (binding_raw, context)` retains the
  predecessor call shape. It must run while the genuine native owner remains open
  and locked during paid cut derivation. Returned bytes are inert until that real
  derivation is committed by the protected destination.
- `parse_binding(raw) -> (doc, marker, activation)` retains its call shape but
  recognizes only `DMKN_GROUNDED_CUT_NATIVE_SUPPORT_ANCHOR_V2`; old state is not
  silently reinterpreted. A new support identity/fresh epoch/state is required.
- `SourceAnchor.open(binding_raw, *, check)` retains the fixed owner-lock/readonly
  SQLite guard and existing full identity/withdrawal checks.
- `SourceAnchor.basis_snapshot() -> {module_name, path, artifact_bytes}` validates
  exact fixed artifact bytes once per invocation. Root calls it once per actual
  worker event, before unsafe native loading, and charges its returned byte count.
  The Lean worker constructs the singleton/no-parent/581-name import internally;
  no module list, arbitrary path override or extension root is accepted here.

The three-field worker shape was coordinated with the Lean author and reported
to root before editing. It intentionally omits provenance details: those belong
to the protected anchor/controller, not an untrusted worker request assertion.

## Capture's actual authority chain

1. Require the exact approved `PortableCatalog` type, ACTIVE native-bootstrap
   origin and a live genuine owner lock. Validate the selected native context.
2. Read `state.basis_root` directly from the live activation, then authenticate
   its `_root_row` and `_validate_record`. Require native-check origin, basis kind,
   zero parent, no input units, and the fixed seed/inventory-bound basis request.
3. The existing record validator checks the actual COMMITTED operation tuple,
   derived root/module/path, implementation, writer origin, retained hash/size and
   artifact. This is not a saved report or the selected extension's first filename.
4. Separately require zero snapshot parent and exact agreement with the context's
   first module/basis identity and 581 bindings. Context metadata alone is not origin.
5. Bind a nested `basis` descriptor into the captured canonical source binding:
   `basis_root`, `parent_root`, `request_hash`, `operation_id`, `record_sha256`,
   `module_name`, `parent_module`, `relative_path`, `artifact_path`,
   `artifact_bytes`, `artifact_sha256`, `names_count`, `seed_sha256`,
   `inventory_sha256`. The outer record binds source directory/store, exact native
   marker/activation, semantic/foundation/implementation and retained support.

Parsing checks the activation-derived basis root, fixed request, deterministic
module and operation-derived relative/absolute artifact path, zero parents,
581 names and exact selected seed/inventory hashes. It caps the artifact at the
lesser of the source's authorized limit and 1 GiB (the existing loader ceiling),
with UTF-8 path bytes capped at 32768. Syntax/hash agreement does not prove origin.

## Event authentication and unchanged cadence

`basis_snapshot` calls the original full source check before and after its work.
It resolves the bound ordinary file, verifies exact size, hashes bounded 1 MiB
chunks with the original budget callback, detects truncation/trailing growth and
compares SHA-256. It returns a detached module-name copy. Every invocation hashes
anew; nothing caches authentication across cut events or reopen.

The predecessor's `check()` body is unchanged: original budget callback, sticky
denial, WITHDRAWN, exact ADOPTION bytes and exact one-primary-key-row SQLite
identity validation remain. No artifact hash is inserted into trie/budget checks.
Event failure marks the guard denied. Reopen reads no basis record, operation list
or application-history snapshots; origin is the protected derivation's commitment.

Keep the real source lock and protected immutable-artifact premise until the
worker has finished and the destination event commits/refuses. Hashing does not
prevent a privileged out-of-model replacement after the final read. Source
deletion, relocation or quarantine refuses this lane; no revocation-timing or
rollback guarantee is added. Controller support validation and clean supervised
completion remain mandatory and owned by root.

## Boundaries still required in the other components

- Bind this exact source binding to the actual cut bootstrap, distinct support
  and fresh epoch. Do not open a peer descriptor as a capability.
- Include `basis_snapshot` in the exact request identity; account for parent
  hashing, child fixed-artifact reading and existing seed/inventory/census work.
- Require the Lean singleton module/header/quotient checks, full fixed inventory
  census, concrete checking, grounded signatures, final census and new proof.
- Do not infer mathematical equivalence from inventory alone: normalization of
  `all` metadata still requires trusted checked origin and loader correspondence.
- Keep every old support/metadata check. No persistent worker or metadata
  amortization is part of this successor.

The code remains unexecuted. Required review concerns are changed-path refusal,
wrong basis/operation/hash/parent/path handling, genuine capture provenance,
one event authentication before loading and preservation of original budgets.
Actual correctness and payoff need root's separately selected bounded controls;
no speedup or public accelerator claim follows from this source handoff.
