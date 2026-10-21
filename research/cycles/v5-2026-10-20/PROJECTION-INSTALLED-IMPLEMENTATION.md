# Installed import boundary: source implementation

2026-10-20, core_release. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
Implements only the adapter assigned by
[PROJECTION-INSTALLED-SELECTION.md](PROJECTION-INSTALLED-SELECTION.md), following
plan `3aed9aae`. Root owns the selector, staging and any finite actual launch;
core_growth independently reviews the new source and selector.

Fresh source: `software/v5/base_projection/installed.py`, SHA-256
`df2c63792c5c6924d56430847741f3d618b6cba057452bd6e19628b87687bf53`.
No Python import/execution, runtime, test, build, network or Git operation was
performed by this author. This is source readiness, not an installed PASS.

## Exact entry contract

Synchronous `main(context)`, invoked by the unchanged actual source-pinned
bootstrap. Parameters have exactly two fields:

- `schema`: `DMKN_V5_INSTALLED_PROJECTION_IMPORT_V1`.
- `expected_sources`: exactly the nine relative-v5 paths in `SOURCES`, each
  mapped to `{bytes, sha256}`, with a positive size no greater than 2 MiB and
  a lowercase digest. Root derives these pins from the adopted release/input.

The source map must contain exactly 113 SDK entries under `v5/` or `portable/`
and one selected `owner/` entry, for 114 total, without an extra source domain.
This count does not imply that non-Python SDK entries are imported.

For each of the nine changed modules, normal `import_module` must resolve the
actual loaded `__file__` to the exact copied `context.sources_v5` path. The
context digest, bounded exact file length and SHA-256 must match the selected
expectation. It does not modify paths, import hooks, module caches or classes.
The bootstrap's later actual origin map and final source rechecks remain the
independent enclosing evidence. No test fixture or predecessor adapter is loaded.

## Report and failure handling

One fresh report is saved to
`context.location_workspace / "projection-installed-result.json"`, beneath
the actual launch run. Schema:
`DMKN_V5_INSTALLED_PROJECTION_IMPORT_RESULT_V1`.

The report retains successful source observations incrementally, identifies the
currently failing source when applicable, and records actual source counts,
status/stage, bounded error and original deadline. Its explicit scope is
`INSTALLED_NINE_MODULE_WHITELIST_ORIGINS_AND_BYTES_ONLY`. It does not claim an
algorithm test or hostile-loader qualification. The final report is at most
64 KiB, written exclusively with short-write check, flush and fsync. A missing
report or write failure cannot return success. Zero exit requires completed
origins and the original deadline; enclosing clean launch remains a separate gate.

## Deliberately absent work

No workspace/store creation or reopen, query compilation, projection preparation,
service call, asyncio loop, socket, location process, RuntimeProfile, trust-domain
adoption, mathematical issuer, operation grant, native worker or prover appears
in the adapter. Zero-work fields describe this reviewed source scope, not a new
OS-wide activity monitor. Merely importing a class is not constructing an owner.

The request may retain `runtime_mode=aggregate` only because the ordinary run
launcher requires a mode; the adapter accepts no adoption/foundation placeholder.
There is no reason to repeat the earlier expensive real-owner/location check.

The first projection-control attempt remains separately noisy/held; this source
does not promote it, the pending repaired result or a future package build.
Root must adopt those prerequisites before selecting the one installed action.
