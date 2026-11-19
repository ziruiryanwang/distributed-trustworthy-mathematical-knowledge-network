# One exported-view census before repairing correspondence

## Decision and scope

Root selected this source-only diagnostic after ordinary-baseline-native-
workflow-02 failed with an unnamed `PUBLIC_COMPUTATIONAL_OR_NONSINGLETON_ERASURE`.
The failure could occur in the fixed 581-name basis before the selected public
closure. Rather than guessing a sequence of matcher repairs, inspect the actual
frontend/kernel visibility and kinds for every relevant name in one exported
import of the retained snapshot.

This is a diagnostic, not a new checker, correspondence event, baseline
registration, certificate or mathematical acceptance. It changes no used source
or evidence. No private import, fixture compile, library collection, selected
export, proof-body decode or snapshot copy is performed by the native probe.

## Native source and exact interface

Fresh source: `software/v5/ordinary_baseline/ReferenceViewProbe.lean`.
Initial source SHA-256:
`ad0a7f45d5713a1addd896ffe9047b47d490f18bb3e07e5880a41f2cfa47fbce`.
It is 179 lines and imports only the existing `BaselineArtifactCore04` helper.
The cold-intake agent owns the separate fresh build adapter/selector. Root owns
runtime selection and saved-snapshot authentication. The semantic auditor owns
source review; this checkpoint is not clearance.

CLI:

```text
ReferenceViewProbe.exe inventory.json replay-request.json test-only-reference-request.json report.json
```

All arguments must be absolute bounded paths. Inputs are read-only; the report
must be fresh and is written with `writeNew`. Inventory/request are each bounded
by 1 MiB; the retained replay-map uses the existing 16-MiB parser/map limits.
The exact saved inventory contains 581 rows; the exact six-unit request contains
nine selected declaration names, so the diagnostic requires **590 distinct
names**, not 591. Only each row's structured name and expected-kind number are
read; signatures and values are not decoded or compared.

The core04 replay parser supplies the complete finite artifact map. The probe
clears `searchPathRef`, performs exactly one `importModules` call with
`plugins=[]`, `loadExts=false`, `leakEnv=false`, `.exported`, and that explicit
map. It checks original root imports, modern module headers, module census,
duplicate/unbound names and bounded dependency edges. Missing inactive modules
may remain unloaded, as in the existing public-view matcher. It checks artifact
sizes again afterward. Cryptographic before/after artifact identity belongs to
root's outer adapter, not these native size checks.

## Diagnostic report

Schema: `DMKN_ORDINARY_REFERENCE_VIEW_PROBE_V1`.
Assurance: `DIAGNOSTIC_ONLY_NO_CORRESPONDENCE_OR_ACCEPTANCE`.
The whole JSON report is bounded by 1 MiB.

Top-level fields:

- `basis_count`: 581; `selected_count`: 9.
- `exported_module_count`: actual loaded-module count.
- `import_count`: 1, the number of native import calls, not imported roots.
- `frontend_missing`, `kernel_missing`, `frontend_axioms`, `kernel_axioms`:
  aggregate counts over the same 590 names.
- `rows`: exactly 590 entries, basis inventory order then selected-unit order.

Each row has:

```text
expected: {name: structured_name, origin: "basis" | "selected", expected_kind: number}
frontend: facts
kernel: facts
```

The two lookups are independent: `(env.setExporting true).find?` with
`skipRealize=true`, and `env.toKernelEnv.find?`. Missing facts are exactly
`{present: 0}`. Present facts contain `present: 1`, `kind`, `unsafe`, `partial`,
`group_count` and `singleton_group`. `kind` is one of `axiom`, `definition`,
`theorem`, `opaque`, `inductive`, `constructor`, `recursor`, `quotient`.
Safety and singleton values are integer bits. Group count/singleton are null
for records without `all` metadata; otherwise they describe the actual record's
`all` list, with singleton meaning exactly `[record.name]`.

No declaration expressions, original proof bodies, signatures, owner authority,
content-ID correctness or acceptance results appear in this report. Original
expected kind is deliberately distinct from observed actual kind. Presence and
matching kind alone do not establish any correspondence.

## How the evidence changes the next decision

The one census should identify all actual shapes relevant to these questions:

1. Which safe definition/theorem/opaque records are abstract in either view?
2. Which fixed-basis private helpers are absent from either view?
3. Does a target's kernel record retain proof support that is hidden in the
   frontend, including the fixture's private `hidden_low` theorem?
4. Are the actual fixture computational interfaces full in both views?

Then root can choose the smallest principled matcher/frontier policy once.
The report must not be treated as permission to ignore missing dependencies or
to accept arbitrary axiom-shaped records. The independent abstraction/closure
argument remains in the semantic audit and integration checkpoints.

## Runtime boundary

No run has been launched by the native author. Root proposed one exported-import
operation capped at 60 wall seconds, 30 aggregate CPU seconds, 1,536 MiB and
four processes, with one-MiB report. A source review, successful exact retained-
core build and root's fresh finite selection are required first. Previously
passing compiler, collector, exporter and snapshot work must not repeat.

## Narrow diagnostic build adapter

`cold_intake_strategy` owns fresh `build_reference_probe.py` and
`select_reference_probe_build.py`. Final hashes:
builder `e709806ab288e04d5165e79563c6018b7db4edaff920c744085aac448ffec43f`;
selector `5631bbda06eec2493d0c60a55a594273e9af35edbc7802570a5586a6592bdbd0`.
Native author now supplies probe `718dcc17dc7365f3f50455832b114d7d690165da4fc5c411be22616f8994947d`
(181lines), superseding unused `ad0a7f45...`; its report additionally lists
`exported_module_names` in actual header order alongside the count.

Exactly three new commands compile only the probe, compile its C object and
link it. Twelve exact retained support files (core04 plus five shared modules,
each `.olean`/`.o`) come from successful build04; no helper is rebuilt. Its
exact receipt/result/selection, core source/snapshot, shared/output pins and23
named toolchain pins are bound. Five source snapshots and47 total input pins
are expected. The fresh output is `ordinary-reference-view-probe-build-01/build`.

The receipt schema is `DMKN_ORDINARY_REFERENCE_NATIVE_BUILD_V1`, status
`BUILT_CANDIDATE_NOT_INSTALLED_OR_ADOPTED`, with explicit purpose
`DIAGNOSTIC_EXPORTED_VIEW_CENSUS_NOT_ACCEPTANCE`, exact source/executable/inputs,
three commands and four generated output pins. It authorizes no probe execution.
Proposed outer120wall/60CPU/1536MiB/four processes and1MiB each log are unchanged;
the controller uses one105wall/50ownCPU deadline.104MiB inner spool plus16MiB
outer source ceiling and logs/metadata fits128MiB total; census is cooperative,
not a hard disk quota. Every copied/original/snapshot/generated pin is rechecked.

AST-only parsing of both Python files passed; no import, selector, native build,
test, owner or Git operation ran. Root supplies final reviewed builder/probe
hashes to the selector, then separately chooses its emitted finite allocation.

## Runtime adapter source review and prelaunch codec repair

`project_intake_native` independently reviewed root's complete runtime adapter
and selector, the actual final native report shape, frozen helper module,
installed profile loader and report parser, snapshot reopening implementation,
and the retained-input identity pins. Reviewed hashes:

- `probe_workflow.py`:
  `9834e46fe72ca3559f6755a972cce038a5402bc8dfe21d576a4c87aa6362714b`.
- `select_probe_workflow.py`:
  `390dee25949f779ddfb941099a1d3bbb948ead99fd4589be1368bf81a9769a6f`.
- Final, still-unexecuted native probe:
  `a5f08241b50da63a1a7314854669dbe3b32b59455a24add8cbc1855f7cf516cf`.

Disposition: **PASS_SOURCE_FOR_ONE_DIAGNOSTIC_SELECTION**, conditional on the
separately reviewed exact three-command build succeeding and root authorizing
its specific BUILD/result/selection hashes. This is source review, not execution
evidence, mathematical correspondence, reference registration or product
qualification.

### Blocker caught and resolved before use

The original probe's `null` group defaults were incompatible with the installed
`ordinary_admission._writer_json`: its lexical grammar permits arrays, objects,
strings and unsigned integers, but rejects `null`. Root selected exactly two
unused-native-source substitutions: absent `all` metadata now yields the string
`"not_applicable"` in **both** `group_count` and `singleton_group`. Root's runtime
validator accepts that exact pair or the bounded integer pair. The frozen core
parser is unchanged. This final schema supersedes the null descriptions and
unused `718dcc17...` source above; it does not change visibility or mathematics.
The semantic auditor separately reviews this narrow native delta.

### Verified binding and execution boundaries

All seven `FIXED` digests were compared read-only to the actual preserved02
result, selection, failure record, inventory, request, snapshot manifest and
replay request; all match. The 1,925,938-byte manifest fits the two-MiB metadata
cap; the 897,749-byte replay map also fits. The selected reopening source hash
`74bb3370...` matches its current file. Runtime verifies these pins before use
and again after the native call.

`inspect_build` binds root-selected exact BUILD/result/selection bytes, clean
enclosing closure, three successful commands, source identity, executable role
and hash, and all build input pins. The selector carries these selected pins
plus the existing package/runtime template into the frozen enclosing runner.
The diagnostic executable is not discovered by a glob or inferred from an old
matcher path.

The frozen workflow02 utility module is loaded only for helper functions; its
guarded `main` is not called. The real package `owner.bootstrap` and `profile.load`
authenticate the installed core and expose its real codecs. No owner state is
opened or invented. `snapshot_reopen.read_snapshot` checks the existing finite
tree and exact part hashes before/after, without opening original library paths,
copying artifacts, importing native binaries or decoding mathematical proofs.

There is exactly one `subprocess.run`: the probe with four exact retained-input
and fresh-report arguments. Native stdout/stderr inherit the enclosing bounded
logs; no repeated compiler, collector, exporter or matcher operation is present.
Environment lookup is restricted; native code additionally clears Lean search
fallback and uses the complete explicit map. The current selected outer
proposal is **90 wall seconds / 45 aggregate CPU seconds / 1,536 MiB / four
processes**, with one original inner 80-wall/40-controller-CPU deadline. This
supersedes the earlier initial 60/30 proposal, not a consumed allocation renewal.

The report validator binds all 590 exact labels in order, both observed views,
bit fields, sentinel/integer group facts and recomputed aggregate counts. It
checks actual ordered module names for uniqueness, root inclusion and membership
in the authenticated snapshot; it does not claim every original private module
must be loaded publicly. The only outputs are the one-MiB-bounded report and a
fresh summary, or a retained failure. The summary explicitly says diagnostic
completion, false mathematical acceptance and false protected registration.

No test, selector, native process, source copy, package mutation or Git operation
was launched by this reviewer. Only the root-selected two-line unused native
compatibility repair and this Markdown checkpoint were edited.
