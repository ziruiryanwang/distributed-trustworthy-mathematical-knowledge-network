# Dedicated host: explicit optional discovery profile

2026-10-28, next_value. Source-only implementation under
`INTEGRATION-SELECTION.md`; no imports, syntax compilation, tests, owner/database,
service, native worker, network or Git operation. The canonical guard passed.
Root must independently review this authored source before any execution.

Fresh `custodian.py` was copied from frozen
`ordinary_dedicated_host/custodian.py`, SHA-256
`63c500ce84e6f1bb0459645d93a6bb84b75efc30958b5e6eabcb8623a343daef`.
The new source SHA-256 is
`d6ae33a614d827df7f798d850713dbb8cc7ffae85ee659a27dff10e965552ad4`.
The predecessor was not changed.

Prepare and serve accept optional top-level `discovery_profile`. The selected
peer API factory validates the two supported values: missing or `exact-v2`
selects the existing exact adapter; `type-pattern-v1` selects the pattern mode.
No seal, record, query spec or database supplies the choice. Unknown values
refuse through the factory before host creation or store opening.

The following signatures and properties were confirmed directly with the API
author before dependent edits:

- `_adapter(loaded, config)` returns the same `OrdinaryExportAdapter` class,
  with `semantic_id`, `namespace`, `limits` and `discovery_profile` properties.
  Only pattern mode reads the selected installation's bounded fixed inventory.
- `_index(loaded, owner, custody, config, check, adapter=None)` accepts that
  explicitly selected adapter; its omitted-adapter compatibility remains exact.

Prepare constructs the adapter before state creation and passes it into the
fresh index. It reports the selected mode; the existing seal still records the
actual namespace and exact package profile. No seal field or schema changes.

Serve constructs the adapter from caller configuration before opening the host.
`_read_seal(..., adapter=adapter)` retains the existing hash, exact-field,
canonical-byte, profile, semantic, assurance, target and capacity checks, then
requires both adapter semantic equality and exact sealed namespace equality.
It does not try another mode after mismatch. The preflight index receives the
same selected adapter. The internal `api.serve` configuration explicitly carries
its `discovery_profile`, including the default `exact-v2`, so the service's own
factory reconstructs the same namespace. That service remains responsible for
its own selected-source and index checks.

Permanent marker and lock handling, supported-command storage exclusions,
custody/index counts, snapshot checks, final source/allowance gates, temporary
seal publication, close/error reporting and retention behavior are unchanged.
An existing host's exact package-profile pin still prevents silently resuming
it under changed software. Pattern selection requires a separately selected
fresh host/index; there is no migration, inferred fallback or feature dropping.

The change exposes no mathematical authority: prepared/served material remains
inert, and all reports keep `mathematical_acceptance:false`. A later finite seam
control may use a pinned saved seal with inert reads to demonstrate both-mode
selection and wrong-mode refusal without opening a real host or service. That
control must be independently reviewed and selected by root.

Adapter/API source review and any authored seam-controls source will be recorded
separately after those sources settle. Used pure pattern/helper controls remain
frozen and will not be repeated.
