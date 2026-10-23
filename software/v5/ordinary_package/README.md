# Ordinary mathematical owner package

This is the Windows local-owner part of the v5 candidate, not the complete v5
release. It builds without retained experiment helpers and provides persistent
`init`, `status` and `contribute` commands over the existing Lean checking core.
It does not yet expose peer search/acquisition/serving as command-line operations.
The license remains undecided; no external publication has been made.

## What it does

A contributor supplies owner-approved Lean source. The authoring tools produce
inert declarations; a separate checking step admits those declarations against
the exact selected local mathematical context. The owner retains accepted state,
portable evidence and previews. Later operations reopen that state; they do not
reinitialize it or replay previously checked proofs as new contributions.

The authoring environment is a helper for constructing candidates, **not** an
independently proved library: acquired theorem signatures may be scratch axioms.
Only successful ordinary admission establishes the supported local warrant.
Neither a compiler success message nor an index result grants that warrant.

## Build

Supply the exact supported Windows Python 3.14.6 and Lean 4.34.0 distributions.
The nine named executable/DLL hashes are in `build.py`; other runtime libraries
remain owner-supplied. This is not a hermetic or cross-platform build claim.
All paths below are explicit absolute paths; parent directories must exist.

```text
<Python>/python.exe -I -S -B <repository>/software/v5/ordinary_package/build.py
  --source-root <repository> --python-runtime <Python> --lean-runtime <Lean>
  --output <fresh-package-directory>
  --wall-seconds 360 --cpu-seconds 260 --memory-mib 2048
```

The builder compiles separate receiver and authoring lanes, assembles the
unchanged receiver core, and writes `PROFILE.json` last. Its JSON reply includes
`profile_sha256`. Keep that exact hash with the package. A hash selects bytes;
it does not authenticate an unknown publisher or make unknown code safe.
`_build/` records provenance and logs; ordinary owner commands do not need it.
The standalone runtime payload is PROFILE, its listed auxiliary files,
INSTALLATION.json and its non-runtime files. External runtimes remain required.

## Use one persistent owner

Every invocation uses:

```text
<Python>/python.exe -I -S -B <package>/owner.py <operation>
  --profile-sha256 <selected-hash>
  --python-runtime <Python> --lean-runtime <Lean>
  --catalog <catalog-directory> --custody <custody-directory>
  --store-id <64-lowercase-hex-local-identifier>
  --custody-limits <limits-json-file>
  --wall-seconds 120 --cpu-seconds 90 --memory-mib 1536
```

The local store ID is bookkeeping, not a person's identity. A small example
custody-limits file is:

```json
{"objects":512,"exports":4096,"logical_bytes":134217728,"db_pages":16384}
```

Choose capacities for the intended local collection; do not imply that every
owner stores global mathematics. Reopening uses the same custody limits.
Catalog defaults are 4,096 roots and 8,192 operations; `init` optionally accepts
an explicit `--catalog-limits` JSON file using the existing catalog fields.

1. `init` requires fresh catalog/custody directories. Keep the returned
   `result.basis.local_root`. Initialization is performed once, not before each
   contribution.
2. `contribute` additionally requires `--parent-root`, `--source`,
   `--acquired-targets`, `--output-names` and a fresh `--output` directory.
   Source is a UTF-8 body in the supported Init/helper environment, not an
   arbitrary Lake project. Acquired targets are exact `{name,export_id,unit_id}`
   records; use `[]` for basis-only work. Output names select one to 32 new
   definitions/theorems. Success returns the new `result.local_root` and exact
   `result.targets`; publication bytes are retained locally, not sent remotely.
3. `status --context-root <explicit-root>` reopens and validates that stored
   context without native proof replay. Root inventory is paged using
   `--limit` and `--after-root`. It never guesses which branch you intend.

Names use the existing portable Lean-name encoding, not ordinary dotted strings.
For ordinary string components, `A.b` is
`[[0,{"$bytes":[65]}],[0,{"$bytes":[98]}]]`. Output-name JSON is a list of such
names. Numeric Lean-name components require the underlying codec representation;
do not approximate them by printed spelling. The generic API and contract are
documented in [ordinary_lean](../ordinary_lean/README.md).

The generated authoring module uses a public section. A definition needed for
an exported theorem's definitional equality may require `@[expose]`, for example
`@[expose] def applyTwice (f : a -> a) (x : a) := f (f x)`. Public visibility of
a name does not itself expose its reducible body. Keep the native diagnostics;
do not infer acceptance from a candidate file left by failed elaboration.

## Observed package boundary

The clean two-lane source build passed: 21 modules, 46.80 elapsed seconds and
40.98 known inclusive CPU seconds. An exact relocated 111-file payload (36.58 MB)
ran independently of `_build` and experiment helper paths. A wrong profile was
rejected before state creation; fresh initialization passed. The first caller
contribution failed on the visibility rule above and remains recorded/charged.
A separately selected caller-only annotation then admitted two units and reopened
the same owner successfully, with no rebuild or repeated initialization: 7.81
elapsed seconds, 7.25 known inclusive CPU seconds. Status used zero native CPU.

These are small local package-boundary checks, not workload speedup claims.
The package profile is
`881adbf54898e08bf8906614c9cf6b76c1f8aec8428e5a4f26f467719a25b232`.
The [saved outcome audit](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-PACKAGE-OUTCOME.md)
retains identities, failures, costs and state correspondence. A separate peer
successor is under source development; it does not modify this used package.

## Failure and trust boundaries

Commands emit one JSON reply and exit zero only for `ok: true`. Preserve failures
and their output: a later publication/log failure can occur **after** admission.
The error report retains known accepted-state information; no rollback or
automatic retry is implied. A normal owner reopen may mark abandoned reserved
operations interrupted, so `status` is not a strictly read-only database open.

Package/runtime/OS integrity and protected owner storage are assumptions.
Before/after pins detect ordinary changes, not hostile local race attacks.
Caller Lean source can execute code and must be approved by the owner. Windows
Jobs contain native resource use; they are not a hostile-source security sandbox.
Controller limits are cooperative; supervise the whole command for hard
process-tree limits. Keep source execution separate from inert peer data.

The selected build and lifecycle evidence is recorded in the
[package outcome](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-PACKAGE-OUTCOME.md).
This boundary does not establish worldwide operation, arbitrary-library
compatibility, sustained growth benefits, release signing or final-v5 readiness.
