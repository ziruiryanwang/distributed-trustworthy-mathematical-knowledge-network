# Ordinary v5 distribution: exact retained inputs

2026-10-20, core_growth. Source-only preparation; no copy, generation, product
import, runtime, test or Git action. Root selects execution and adoption;
core_search owns the new builder and public launcher.

## Authoritative existing inputs

The real ordinary remote plan is
`experiments/v5-local-checks/client-remote-check-01-plan.json`, SHA-256
`68af53270016f920822942cef153948eeacdca81b501dc461a1b8dec2a756483`.
It selects 103 sources. Exclude its fixture `owner/remote_check.py`; retain the
102 existing SDK/portable source entries by their exact selected hashes.
Builder/launcher sources need separate fresh reviewed pins, not silent inclusion.

The immutable base is `product-local/v4-library-commons-02/commons-v4`.
Its 1,070,384-byte `RELEASE-MANIFEST.json` has SHA-256
`a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed`
and describes 6,652 payload files totaling 235,662,448 bytes. Nest those exact
bytes under `base/`; adding v5 files must not rewrite that manifest.

The preparation template is
`experiments/v5-local-checks/delta-author-01-profile.json`, 21,137 bytes,
SHA-256 `f03b591c6e9e40346028c35b663d4d2c5daaf9a58ec6eb890810f96c6c984a4b`.
The remote plan supplies pinned native/I/A/foundation roles; the template
supplies the image, AuthorLean frontend and Lean runtime. Template
`producer.host` must equal the selected I host, and all relation/foundation/
policy/image bindings remain unchanged.

| Role | Bytes | Source role |
|---|---:|---|
| I/preparation host | 66,652,160 | Remote adoption `receipt`; template `producer.host` |
| A host | 6,630,400 | Remote adoption `aggregate.executable` |
| Native delta checker | 1,713,152 | Remote adoption `native` |
| Guest image | 1,681,428 | Template `image` |
| AuthorLean frontend | 593,408 | Template `native_executable` |
| Foundation data | 23,313 | Remote reader `foundation` |
| Six Lean runtime files | 212,510,976 | Template `lean_runtime_pins` |

These external inputs total 289,804,837 bytes, before SDK/configuration. Thus
the whole install is approximately 526 MB, not merely the 236 MB base.

## Relocated relationships

`RuntimeProfile` already rebases manifest-backed Python/runtime files and
selected SDK source/worker paths. It does not rebase the external host,
image, frontend or Lean paths: the distribution launcher must construct an
explicitly adopted profile referencing the installed relative asset roles.
No serialized absolute original template path can remain a runtime dependency.

The six Lean files retain their tree below the new Lean root:
`bin/libc++.dll`, `bin/libInit_shared.dll`, `bin/libleanshared.dll`,
`bin/libleanshared_1.dll`, `bin/libleanshared_2.dll`, `lib/lean/Init.olean`.
The preparation owner requires both `bin/` and `lib/lean/` and checks these
pins. The authoring worker sets its Lean path and prepends that `bin/` to PATH;
it retains OS PATH fallback. Source/file pinning is not an adversarial DLL
loader sandbox or proof of independence from every machine-provided system DLL.
The native mixed checker itself does not request a Lean PATH.

The installed relative source/asset map is one owner-adopted release selection,
not a new proof authority. Existing launch/boot exact maps and original finite
Job remain the runtime mechanism. No theorem fixture, receipt, run workspace,
TLS secret or historical result belongs in the generic SDK.

## Builder contract

`select_distribution.py REVIEWED_DISTRIBUTION_SOURCE_SHA` prepares only the fresh
`experiments/v5-local-checks/distribution-01-input.json`. Schema
`DMKN_V5_DISTRIBUTION_INPUT_V1` has exactly `schema`, `base_root`,
`base_manifest`, `sdk_sources`, `preparation_template`, `assets`,
`aggregate_image`, `lean_runtime`, `distribution_source`. All file values are
exact absolute `{path,bytes,sha256}` input pins; SDK keys retain `v5/` or
`portable/`, Lean keys are relative under its root. Builder invocation is
`distribution.py build INPUT SHA OUTPUT`. The release map is relative; the
launcher constructs each absolute preparation profile outside the install.

## Smallest relocation check

After exact file-map review, one fresh install directory with spaces and one
ordinary public launcher invocation should run the retained remote adapter as
explicit owner-selected local code. Copy only its exact mathematical packet to
caller data, outside the installation; use fresh custody/reader workspaces.
Resolve all runtime/source/profile roles from the new installation and verify
no selected dependency points at the repository, research or experiment paths.
Use the same packet and one I/native read/import, not a new proof or another
authoring/network/growth campaign. Current same-call receipt/native admission,
unknown-ID discovery, READY and clean closure remain the necessary assertions.

This check targets changed path/profile/source binding. It does not newly
qualify authoring or prove independent-host operation merely because absolute
paths were rebased. The prior passed mathematical/component campaigns stand.
Full-v5 aggregate production, security assurance, license and public release
obligations remain open.
