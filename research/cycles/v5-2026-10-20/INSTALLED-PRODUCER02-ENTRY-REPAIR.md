# Installed producer02: bounded supervisor-document bootstrap repair

2026-10-22, storage_integration_adapter. Canonical project root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

Root's causal audit reports that actual snapshot01 stopped before product
imports: the entry's generic `_pin_document` imposed1MiB on the actual
1,070,384-byte supervisor manifest. The downstream owner/final checks already
use8MiB for that specific document. No successful snapshot, capsule or request
follows from failed01; its sources and all evidence remain unchanged.

## Exact source change

Fresh source: `software/v5/installed_production02/release_production/operator.py`.
It differs from frozen predecessor by exactly four textual substitutions:

- `_pin_document(path, expected=None, maximum=MIB)` adds a defaulted bound.
- The file-size check uses `maximum` instead of MIB.
- The bounded read uses `maximum+1` instead of MIB+1.
- Only the supervisor-manifest bootstrap call supplies `8*MIB`.

Profile and ordinary input defaults remain1MiB. The supervisor's expected
digest, exact pin equality, full Python-file check, profile/source/entry binding,
final validation, containment, limits, reporting and all action behavior remain
unchanged. This aligns bootstrap with an already selected document role; it
does not raise a public resource envelope or change mathematical acceptance.

| Source | Bytes | SHA-256 |
|---|---:|---|
| Frozen installed_production/release_production/operator.py |26808|`f404f0ba4d5177654fd02e999b00c0d8d104f1a4b85295414dff2720ddf6021a`|
| Fresh installed_production02/release_production/operator.py |26836|`1141f160ad3744734525a08efa5bfe29eb628f3598bedb46ddaaf1fe3974dd7e`|

Read-only exact-string comparison confirms those four substitutions and no
other byte change, including unchanged LF line endings. Source creation used
apply_patch; no source import, syntax execution, test, build, product launch,
proof, Git change or previous-operation rerun was performed. The disjoint
distribution successor belongs to storage_launch_review. Root independently
reviews the combined seam and selects any finite later execution.
