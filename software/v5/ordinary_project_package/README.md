# Trusted-project contribution adapter

Assembled candidate with independently audited native-free controls; real-project
compatibility remains untested. This adds an optional
authoring environment to the [ordinary peer package](../ordinary_peer_package/README.md).
It does not replace Lean projects, install dependencies, or change the receiver's
mathematical acceptance rules. License remains undecided.

## Intended user workflow

Keep your existing, already built, owner-approved Lean project for tactics,
notation and other executable support. Supply imports from it and a source body
that authors new declarations. The adapter constructs one fresh temporary module,
exports inert candidate declarations, then independently checks them against your
selected commons context. Original project files are not rewritten.

This is **not** a way to import arbitrary precompiled project theorems into the
commons for free. Every mathematical dependency must already have an exact
accepted receiver interpretation or be separately acquired and checked. A missing
interpretation is a reported refusal, not an automatic download or source build.

The producer and receiver may interpret the same name differently. Admission
establishes the theorem in the receiver's exact context; it does not establish
equivalence with your project. Inspect the returned statement and exact IDs.

## Runtime and trust boundary

The initial supported environment is the existing Windows Lean 4.34.0 / Python
3.14.6 profile. Other versions are not implicitly compatible. Project dependencies
must already be compiled using the selected toolchain. No Lake command, package
download or toolchain switch is performed.

Imports, tactics, macros and plugins execute as owner-approved local code.
Do not use a peer's configuration as approval to run that code. Process resource
limits are not a security sandbox. The receiver checks inert output independently,
but cannot protect its state from a hostile program with the same operating-system
permissions.

Scratch modules can contain assumed handles for mathematics already accepted by
the receiver. Their generated `.olean` files are **not ordinary proof-complete
libraries**. Share the accepted inert evidence using `publish` and `serve`, not
those scratch binaries.

## Assembly

The file-only assembler takes an exact existing ordinary peer package. It copies
the selected payload into a fresh directory, changes only `owner.py`,
`author_worker.py`, and `authoring/py/ordinary_contribution.py`, then records their
new hashes in `PROFILE.json`. The loader, peer commands, native checker and all
compiled helpers remain byte-identical. No owner state is copied or initialized.

```text
<Python>/python.exe -I -S -B <repository>/software/v5/ordinary_project_package/assemble.py
  --source-root <repository>
  --base-package <peer-package> --base-profile-sha256 <exact-base-profile-hash>
  --python-runtime <Python> --lean-runtime <Lean>
  --output <fresh-package-directory> --wall-seconds 60 --cpu-seconds 40
```

Use absolute paths throughout. Preserve the original package and retain the
successor profile hash. The audited local successor's profile is
`b584cb21266fcf24502355a929939d8e6d662c75d1d7ea520fb23eb6105c7c69`.
Its 116 payload files total 36,680,088 bytes, plus PROFILE and ASSEMBLY metadata.
Assembly took 4.14 elapsed seconds / 2.30 known CPU seconds; no Lean rebuild.

## Select an approved project environment

Use the ordinary `owner.py contribute` arguments with the new package/profile,
and add both of these optional arguments:

```text
--project-authoring <absolute-config.json>
--project-authoring-sha256 <SHA-256-of-that-file>
```

Omitting both keeps the original source-body route. These options are refused
for `init` or `status`. Here is the configuration shape; paths and module names
are illustrative, not a supplied or tested project:

```json
{
  "schema": "DMKN_ORDINARY_TRUSTED_PROJECT_AUTHORING_V1",
  "module_name": "NewWork.Contribution",
  "project_cwd": "E:/MyLeanProject",
  "project_search_paths": ["E:/MyLeanProject/.lake/build/lib/lean"],
  "imports": [
    {"module": "MyLeanProject.Support", "meta": false},
    {"module": "MyLeanProject.Tactics", "meta": true}
  ]
}
```

List all required approved compiled-dependency roots in lookup order; they are
not inferred from Lake. `meta` selects `public meta import`; otherwise the module
uses `public import`. Module names use bounded dotted ASCII identifiers. At most
16 distinct search roots and 64 distinct imports are supported. The configuration
is bounded to 64 KiB and its hash is checked before owner state opens.

Generated source is under the fresh contribution output at
`owner-source/NewWork/Contribution.lean`; that scratch tree is the Lean module
root. `project_cwd` is separate and may support trusted plugins' resource lookup.
Pinned helper roots and the selected Lean runtime precede all project search
roots. This intentionally forbids ordinary lookup overlays of helper, Init,
Lean and Std namespace roots. It is not protection against a hostile plugin.

## Compatibility gate

The [five pure controls](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-PROJECT-CONTROLS-OUTCOME.md)
passed: strict configuration handling, exact default source/argv compatibility,
closed backend validation, explicit worker path order, and pre-open CLI refusal/
forwarding. They loaded the actual successor profile but mocked worker and owner
operations; they took 1.45 elapsed seconds / 1.19 known CPU seconds. They do not
establish ecosystem compatibility or execute the complete project contribution.
No suitable real owner project has yet been selected for an actual contribution.
Until that happens, project/editor compatibility remains unclaimed. We will not
call another elementary fixture a realistic Lean-project evaluation.

When conventional pinned package imports serve a collaboration more cheaply at
the same assurance level, use them. The commons' prospective added value is
selective discovery, inert exchange, independent checking and durable re-serving,
not replacing the established Lean development environment.
