# One direct build from the current source distribution

This plan is source-only. Root must first adopt the controls outcome and its
actual source extraction/outer-manifest hash, then independently review the
resulting exact selection before launching it once. This document supplies no
stand-in hash, pre-authorized run or permission to retry a failed allocation.

Controls01 failed in offline preparation because one bounded metadata reader was
reused for 45 source files. Its sources, archives and output stay frozen. No build
selection may be generated from that failed gate. A fresh preparer correction
and separately adopted successful control/extraction must precede this plan;
the unchanged compiler lanes do not justify skipping that usability gate.

## Decision and evidence

The changed boundary is whether the flat current archive alone supplies the
direct builder's complete source closure and produces a coherent current
package. Do not reconstruct old overlays or stage another clean source tree.
Use the sole actual source-ZIP extraction retained by the controls. The builder's
existing internal snapshots remain necessary and unchanged.

The closest completed comparator is `bounded-investigator-src01`, reviewed in
`software/v5/ordinary_bounded_operations/REVIEW.md` under “Actual clean-source
build.” It used the same lower receiver/authoring builder and native/query lanes:

| Retained evidence | Actual observation |
|---|---|
| Outer `RESULT.json` wall | 60.078679 seconds |
| Inclusive outer Job CPU | 52.0 seconds |
| Separate outer wrapper CPU | 1.328125 seconds |
| Peak outer Job private commit | 925,749,248 bytes (about 883 MiB) |
| Closure | Exit zero, child reaped, zero active processes, Job closed |
| Diagnostics | Zero stderr |

Its exact selection was
`f4ad77727bb7e4340c6963e3aa1fbf19ba6d58afa52182a83b93cb7fc5df3ba2`.
The 48.171875 inner child-Job CPU is already included in 52.0 and is not an
additional charge. `native-src01` separately supports relocated clean-input use:
99.4725324 wall seconds, 60.828125 inclusive Job CPU and 1.6875 wrapper CPU.
These are practical budget precedents, not a prediction or new performance claim.

## Exact selection and invocation

`select_build.py` is a local operator selector, not part of the distributed
product. It accepts `--name`, `--source-root` and an independently approved
`--manifest-sha256`. Invoke it only after the controls are adopted, with the
selected Python and `-I -S -B`, from the canonical project root. It uses the
existing `bundle.verify`, requires the source kind, and produces only one fresh
`experiments/v5-local-checks/<name>.selection.json`. It neither builds nor
creates another extraction, imports the product, opens owner state or starts
a network process. The helper's cooperative 60-wall/30-CPU-second cap applies
to selector verification; there is no automatic retry.

The exact input set is:

- 107 extraction files: 106 manifest payloads plus the approved outer manifest.
- 23 external runtime files from the pinned release's combined runtime map.
- Thus 130 absolute `runtime_pins`, below the existing runner limit of 256.
- Seven small source snapshots: existing runner, selector, this plan, current
  builder, current bundle, release map and frozen file helper.

The builder, bundle, release and helper snapshot pins must equal their extracted
counterparts. No original-repository copy of the 93 build inputs is required.
The compiler runtime remains an explicitly installed external distribution;
23 named pins are not a claim to have hermetically pinned every transitive
compiler/library/OS input.

The runner remains `tools/Run-V5-Check.py`, not a new wrapper. Root supplies its
selection path and hash using its existing two-positional-argument interface.
Its resulting direct builder argv is:

```text
D:\Python314\python.exe -I -S -B
  {snapshot}\software\v5\ordinary_current_release\build.py
  --source-root <adopted-source-extraction>
  --python-runtime D:\Python314
  --lean-runtime "E:\Distributed Trustworthy Mathematical Knowledge Network\software\runtime\lean-4.34.0-windows"
  --output {output}\distribution
  --wall-seconds 480 --cpu-seconds 360 --memory-mib 2048
```

`{snapshot}` and `{output}` are the existing runner substitutions, not shell
variables. Fresh selected output is under the canonical `experiments/v5-local-checks`.

## One allowance, nested containment

Retain the already successful limits unchanged:

| Layer | Wall seconds | CPU seconds | MiB | Simultaneously active processes | Logs |
|---|---:|---:|---:|---:|---|
| Existing outer runner Job | 540 | 440 | 2304 | 8 | 1 MiB each stdout/stderr |
| Direct build controller | 480 | 360 aggregate | 2048 for child Jobs | Within outer 8 | Three retained stage logs |
| Each sequential direct child Job | Remaining wall minus 25 | Remaining CPU minus 62 | 2048 | 8, also within outer 8 | 8 MiB each |

The build controller debits its own CPU and inclusive measured CPU of prior
children. It reserves the entire next child CPU grant before launch, replacing
that reservation with the measured final CPU only when known. A failed unknown
child does not become free. The 62-second subtraction preserves the existing
supervisor's 60-second controller cap and two seconds of local finalization
slack; wall slack covers existing cleanup and final copies. Integer flooring
can reduce each grant further.

Three direct child Jobs run serially: lower receiver/authoring build, extractor
build, and query build. The lower build receives its parent's remaining grant
minus another 25 wall seconds and 2 CPU seconds. Its nested compiler Job then
uses the lower builder's own remaining allowance minus 25 wall and 2 CPU seconds.
These are subdivisions, never renewed independent totals. Nested processes
also belong to the outer Job: the simultaneous process caps do not add to
8 + 8 + 8. Lower compiled processes are charged once through the enclosing
direct-child Job, and all direct-child CPU is included in the outer Job CPU.
Report outer wrapper CPU separately; do not add nested inclusive figures again.

The retained supervisor samples total CPU/wall/log caps and applies native Job
containment; it is not a hostile-source or whole-filesystem security sandbox.
Immutable approved source and installed runtime storage remain premises.

## Terminal acceptance and stop condition

Require the actual outer `RESULT.json` to report
`COMMAND_EXITED_ZERO_AND_CLOSED`, exit zero, reaped child, zero active processes,
closed Job, no cleanup errors and zero stderr. Independently review all three
direct child supervision records and the nested base compiler record, including
final samples and source/runtime rechecks. A missing terminal report is not a pass.

The direct builder's receipt is
`distribution/_build/BUILD-RESULT.json`, not `distribution/BUILD-RESULT.json`.
Require `BUILT_NOT_ADOPTED`, complete child CPU accounting, 153 files excluding
PROFILE, 117 auxiliary roles and all eight selected documents. Review the exact
154-file package census, 45 noncompiled auxiliary pins, 72 generated native
auxiliary roles, receiver outputs, and actual INSTALLATION/PROFILE/implementation
bindings against `release.json` and the actual compiler records. Rebuilt native
hashes need not equal the prebuilt reference; do not substitute old identities.

This establishes source-build/assembly coherence only. It does not run owner
state, accept mathematics, prove growth advantage, authorize deployment or
complete v5. Root separately decides the smallest actual public-use check
needed for the new generated profile. Do not repeat prior mathematics merely
because executable timestamps differ. Preserve every partial output or failure;
any correction/retry needs a distinct reviewed selection rather than renewal.
