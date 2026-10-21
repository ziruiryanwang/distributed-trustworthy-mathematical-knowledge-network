# Consolidated composition and file-only build review

2026-10-21, independent reviewer `support_guest`.

Disposition: **PASS_SOURCE_COMPOSITION_AND_BUILD_SELECTOR; SMOKE_PENDING.**
Root may select the fresh file-only directory build using the exact selector
below. This is not an executed build, installed smoke pass, mathematical
acceptance, user trust adoption, release qualification or launch authorization.
The restart adapter and its selector require a separate
`CONSOLIDATED-SMOKE-REVIEW.md`; this build review must remain frozen once used.

## Exact reviewed selection

- `Select-ConsolidatedDistribution01.ps1`:
  `497cff81294e8f709996ba8332b33eb8c283244a153289b336565cf4af7daf38`.
- Baseline `experiments/v5-local-checks/distribution-terminal-i-01-input.json`:
  `d3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0`.
- Actual sharing selection `sharing-margin-01-selection.json`:
  `8ab7783837d9b0d56c0801dc36f83c9e11c5c360a1a514f282fe500f93018d9f`.
- Actual retained-advertisement selection
  `retained-advertisement-controls-01-selection.json`:
  `52403f3c0b99f10e7044751c56b78e2c1cd33e9dffc3bd00102b981c313fc3bf`.
- Unchanged builder `software/v5/body_location/distribution.py`:
  `eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813`.
- Unchanged outer runner `tools/Run-V5-Check.py`:
  `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651`.
- Reused build selection `distribution-body-custody-build-01-selection.json`:
  `ec52d60965bcdf885455a4aeb20e9c27fedd87fb0fc73b363c3522aca9b6e0ab`.

Paths for selections above are under `experiments/v5-local-checks`; the new
PowerShell selector is adjacent to this review. Read-only reconstruction from
the selector independently verified every baseline SDK row's current length
and SHA-256, all twelve delta files, their provenance in the two actual
selections, all 28 reused build runtime pins, and PowerShell parse success.
The four fresh input/selection/installation-parent/output paths were absent.
No selector, product module, test, build, proof, native check or network actor
was executed by this reviewer.

## Exact logical delta

Each physical suffix below follows `software/v5/`; each logical name follows
`v5/`. All other 109 baseline logical rows remain exactly unchanged. The
result is 121 SDK rows: 100 `v5/*.py` and 21 unchanged portable rows.

| Logical name | Physical suffix | Kind | Bytes | SHA-256 |
|---|---|---|---:|---|
| `admission/pin_phase.py` | `standalone_validation/admission/pin_phase.py` | replace | 8677 | `ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881` |
| `mixed_claims/imports_atomic.py` | `continuing_context/mixed_claims/imports_atomic.py` | replace | 45513 | `45b082863525fb08c1e8925e998113b55deff4b92482c8cf9b63cea2093725ad` |
| `mixed_claims/receiver.py` | `incremental_native/mixed_claims/receiver.py` | replace | 27837 | `5436569971c272b129fbaec480d51d57a1ec521d43fd4d4ad14133b786691d5b` |
| `client/workspace_atomic.py` | `continuing_context/client/workspace_atomic.py` | replace | 51319 | `32e3b95ea2e6d3f8dc35d63000728e9e075a16de3e13fb1a0b718bce45e11773` |
| `discovery/discovery_store.py` | `selective_placement/discovery/discovery_store.py` | replace | 19886 | `1c8543d4903754174b80d107ee923116ddb402d41a3b5af3f1d255abdfc6a328` |
| `placement/__init__.py` | `selective_placement/placement/__init__.py` | add | 78 | `8fe08470d7fd15e96d1305f0e49a8b359cb53ce0c542bf7473b68d869159112e` |
| `placement/codec.py` | `selective_placement/placement/codec.py` | add | 6363 | `6f32569d4807f96130350b85233161603f6860f082c75f81a8bfacf4f0a58999` |
| `placement/ledger.py` | `selective_placement/placement/ledger.py` | add | 12537 | `d955990c347ed466617c752893dded8b8494dd266a050b045352c77c48f21a91` |
| `placement/controller.py` | `selective_placement/placement/controller.py` | add | 18192 | `ef1c9b59072127379e955bafeea001a22d6e3d10c9c46dca1304f85ab09e2b49` |
| `placement/network.py` | `placement_network/placement/network.py` | add | 31301 | `1ec5c452ec129ae033f0577ebac6223e2cf3192d4724a3d31fe2e5c27a06cd4b` |
| `placement/advertisement.py` | `retained_advertisement/placement/advertisement.py` | add | 23256 | `5aa23ee76115355ad319ae4acfd4ab418e010166e53b6ed02c82eb25d34d4510` |
| `client/serve_placement.py` | `retained_advertisement/client/serve_placement.py` | add | 22670 | `7e735337d595894e25fd07a8dcc9ad8cd3ba9f1c042ba930684b7798232cb7fa` |

The old standalone imports pin `8a831337...` present in placement's exercised
overlay is not added as another module: the continuing-context successor
`45b08286...` occupies the same logical key. Its exact four-file sharing closure
already used the selected incremental receiver and pin phase together. The
retained-advertisement service/advertisement replace their predecessor roles;
old service variants do not enter this union. No experimental support/RC/typed
guest, proof profile, duplicate cache or second location runtime is added.

## Cross-module and capacity reasoning

The placement ledger and service import the unchanged logical
`client.workspace_evidence.Workspace`, including its exact-type requirements.
That class retains its normal mixed/atomic inheritance and imports selected
`Store`, import-session and receiver roles through the logical map. The guarded
Store successor preserves existing call signatures and adds optional
`before_commit` to `admit`; ordinary atomic and evidence-workspace calls remain
valid. Placement controller/ledger/network/advertisement dependencies resolve
to the seven selected package additions and existing custody, transport,
discovery and portable location modules. No parallel class identity or
source-overlay alias is needed in an installed import.

The unchanged builder's build and manifest validation both admit up to 141
SDK entries and require the old roles as a subset, not an exact 114-entry set.
All additions satisfy its path/extension and 2-MiB per-file conditions. It
generates preparation `source_pins` from every selected `v5/*.py`, hence exactly
100 pins. Both manifest profile-list validation and preparation owner allow
128. The unchanged trust-withdrawal runtime reconstructs all selected Python
sources with cap 120. Its receipt/aggregate runtime-pin unions are 100 source
files plus 18 unique Python-runtime files plus one selected executable = 119,
below cap 128. Public launch allows 512 sources; this union is comfortably
inside its count and byte bounds. No capacity patch is justified.

## Selector and remaining boundary

The selector pins this review by caller-supplied full SHA-256, checks the exact
baseline, reconstructs its map, verifies every inherited and replacement row,
requires exactly five preexisting keys and seven genuinely new keys, and
requires the final census 121. It changes only `sdk_sources` in the baseline
distribution input. Base role/root, foundation, images, native/receipt assets,
Lean support/runtime, preparation template and builder remain inherited.

It writes new JSON with `CreateNew`, checks all four outputs are fresh, and
selects only isolated `distribution.py build` into the new consolidated parent.
There is no build invocation, migration, existing-install edit or trust adoption
inside the selector. Its reused 120 CPU seconds, 128 MiB, two-process and 1-MiB
stdout/stderr limits remain unchanged. Wall allowance explicitly changes from
the old 300 to 600 seconds for this fresh directory copy/verification operation;
this is not renewal of any old allocation or expansion of mathematical work.

Root still owns creation, launch and actual build-result audit. A successful
file-only build will establish exact installed bytes, not the new cross-lifecycle
claim. The separately reviewed installed close/reopen/unknown-ID discovery
smoke remains necessary. This note deliberately does not approve that adapter
or claim it has run.
