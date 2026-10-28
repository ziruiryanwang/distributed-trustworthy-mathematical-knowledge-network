# Offline pattern query and loader source review

2026-10-28. query_scaling independent source inspection. **PASS within the
selected source-only scope; no blocker found.** No imports, execution, tests,
owner/database access, native calls or Git actions were performed. This does not
qualify runtime behavior or adopt a package.

Reviewed pins:

- `pattern_query.py`:
  `3df3dc0abaabf15952ee7ac2b07a6fe294bef59fcb1864228b7c82024694be76`
- `profile.py`:
  `5d10bc1497e9679f8f08ad87ab6418bc4eab4bf835ed2359486055c64020db83`

The offline path verifies the explicitly supplied PROFILE hash and its own file
pin, then verifies INSTALLATION.json against that profile. Three installed core
modules must occupy their exact manifest roles and match manifest pins. Six
auxiliary modules match PROFILE pins at fixed logical paths. All nine are read
and captured before the first product module executes. Dependency order is
complete for the selected source imports; no product directory is added to
sys.path. Preloaded product modules/namespaces refuse, the discovery namespace
has an empty search path, and the context manager removes inserted modules on
normal or exceptional exit. Approved captured bytes, not later filesystem
contents, supply imports.

The fixed inventory is read from the installed foundation path with a manifest
pin and one-MiB cap. The selected pure helper separately checks the exact
semantic inventory hash before parsing. Neither inventory nor core source paths
come from query bytes. PROFILE/manifest JSON is trusted only as explicitly
hash-approved local metadata; untrusted query bytes go through the original
bounded strict type/preview codecs. Immutable protected files and approved
entrypoint/Python remain stated premises, not hostile-writer protection.

The CLI requires an explicit `native-type` or `preview` discriminator and a raw
input hash. Both readers preserve the existing one-MiB/default DAG limits; no
fallback between kinds occurs. Input, inventory and output are capped at one
MiB, and each selected source plus PROFILE/manifest at two MiB. Ordinary file,
reparse/hardlink, fresh-output and overlap checks are present. PROFILE and raw
input are reread before output. SPECS is written first and RESULT last, so an
incomplete directory is not a completed result.

MODE is fixed to `type-pattern-v1`; namespace and feature compilation use that
same explicit mode and selected semantic contract. The result binds package,
input kind/hash, pattern profile, semantic/foundation identities and inventory
hash. Its distinct operation/schema and explicit specs preserve the existing
exact query/name-directory contracts. It asserts neither semantic equivalence
nor mathematical acceptance. The captured closure has no admission/owner,
subprocess, native loader or service path. The normal `profile.py` loader is not
used by this offline command.

Text comparison confirmed the normal loader differs from the current directory
loader only by adding `ordinary_type_pattern` to AUTHOR and `pattern_query.py`
to required root roles. Consequently the helper enters existing pin/census,
preloaded-module and loaded-path checks. Existing installed/native verification,
support closure and owner-state behavior are unchanged. Normal loader calls
still use NativeInstallation.open; that fact is distinct from the offline path,
which neither opens an installation object nor launches native work.

Accounting limit: the report's elapsed/CPU sample is taken before final input
rechecks, serialization and output writes. Treat it as a precommit sample, not
total process cost. Cooperative checks and finite byte bounds are not hard OS
containment; any selected execution still needs root's outer finite accounting.
This is a reporting-scope observation, not an acceptance or namespace defect.
