# Exact-custody distribution selector: source review

2026-10-20, `adaptive_audit`. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

**Disposition: SOURCE GO, conditional on root's adoption of the actual controls
outcome and exact reviewed product hashes.** The selector was read, not run.
No build, test, installation, runtime or product edit was performed for this
review. The active controls operation belongs to root; its outcome is outside
this assignment and is not inferred here.

## Reviewed identities

| Input | SHA-256 |
|---|---|
| `research/cycles/v5-2026-10-20/Select-BodyDistribution01.ps1` | `1e918fd9f0131a41ca51c0b2bc4eb0c7259c09f42b1717f2ea1af506bc87437f` |
| `experiments/v5-local-checks/distribution-projection-01-input.json` | `ad2c15a27a51f749104ac09f9cafee210a108fb0bf46bafad8b2a9542f86d38f` |
| `experiments/v5-local-checks/distribution-projection-build-01-selection.json` | `1e558685080a904464a26789a68283a4af07c823632b712da39e861cd1fa7286` |
| `tools/Run-V5-Check.py` | `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651` |
| `software/v5/body_location/distribution.py` | `eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813` |

## Exact source delta

Read-only inspection of the authoritative basis confirms 113 SDK entries, all
eleven requested replacement keys present, and
`v5/client/body_custody.py` absent. The selector's closed replacement list is:

- Seven `portable/location/` entries: `protocol.py`, `protocol.mjs`,
  `intent.mjs`, `maintained_roles.mjs`, `ipc_wire.mjs`,
  `node_entry_services.mjs`, `controller_services.py`.
- Four `v5/` entries: `client/workspace_evidence.py`,
  `client/semantic_reader.py`, `client/serve_advertised.py`,
  `transport/acquisition_resilience.py`.
- One new `v5/client/body_custody.py` entry.

Thus the intended SDK count is **113 - 11 + 11 + 1 = 114**. The separate builder
successor is not counted as an SDK entry. The reviewed-map gate requires exactly
the thirteen product paths (eleven replacements, helper, builder), with no tests
or extra executables. Every reviewed digest is checked against its fixed
canonical source path before output creation; every resulting SDK row is
rechecked for both digest and byte count. Existing unaffected SDK records are
carried from the hash-pinned basis rather than rediscovered from a directory.

I also read the complete two-hunk builder diff against the basis builder.
The only changes require the helper as an SDK dependency and allow explicit V3
parameters for `serve-advertised`. The builder's role map, copying, source
pinning, runtime projection, asset selection, manifest validation and full final
verification are unchanged.

## Runtime, assets and bounds

The selector changes only `sdk_sources` and `distribution_source` in the
distribution input. It does not assign to `base_role`, `base_root`,
`base_manifest`, `assets`, `aggregate_image`, `lean_runtime`, `lean_support` or
`preparation_template`.

Consequently the selected role remains `mathematical-client-location-v1`; the
base remains the adopted v4 library directory and manifest. All six mathematical
assets and the six explicit Lean runtime entries remain those in the authoritative
basis, as does the larger Lean support closure. The unchanged builder rechecks
these exact inputs and pinned copy bytes; this review did not duplicate that
full runtime/asset hash campaign.

The build selection preserves the predecessor's **27** runtime pins and adds
only the newly written input JSON's exact hash, giving **28** pins. It selects
only the unchanged runner and fresh builder as snapshotted executable source.
The executable is the same pinned retained Python with `-I -S -B`; the command
is `build`, not a test, proof producer, network service or deployment action.

The original build limits are carried unchanged:

| Resource | Limit |
|---|---:|
| Job CPU seconds | 120 |
| Wall seconds | 300 |
| Memory MiB | 128 |
| Active processes | 2 |
| Each stdout/stderr bytes | 1,048,576 |

The retained runner snapshots its two selected source files, pins the runtime
and input before/after supervision, uses fresh output, and retains actual exit,
closure and binding status. The builder separately binds its snapshot to the
input's declared builder hash and verifies the finished directory. Therefore
the selector's copied input references do not substitute for final byte checks.

## Fresh output and failure handling

The selector refuses pre-existing input JSON, selection JSON, installation
parent, or named runner-output directory. It writes JSON with `CreateNew`,
flushes it and pins the exact new input. Its only directory creation is the
fixed fresh parent:

`product-local/v5-distribution-body-custody-01`

The later builder destination is its `Mathematical Commons v5` child. The builder
requires a fresh ordinary destination and rejects input/output overlap before
copying. No existing installation is edited, migrated, overwritten or deleted.
If staging fails after a new file is created, that partial artifact remains;
the selector is intentionally not idempotent and must not silently overwrite it.

## Gate interpretation and residual scope

The controls-outcome parameter is an **exact-byte gate**, not an automatic
Markdown verdict parser. Root must read/adopt that actual outcome and pass its
digest only if it justifies the selected product hashes. The reviewed source-map
JSON is likewise trusted local owner input, not peer authority. This matches
the existing source-selection workflow; it is not a cryptographic release
signature or a new automatic acceptance rule.

No source blocker was found for the stated selector. Source GO does not mean
the controls passed, the selector ran, the distribution built, an installed
owner path worked, or v5 is accepted. Actual saved-output/map/closure auditing
and any later installed-path selection remain separate root-owned gates.
