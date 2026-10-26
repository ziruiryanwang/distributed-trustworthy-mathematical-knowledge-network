# One installed Std export: exact public plan

2026-10-26. Source/data review only; root owns input bytes, selection and launch.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
One target, first success/refusal retained; no adapter, retry or downstream run.

## Question and selected support

Can the adopted producer export the full selected closure of
`Std.HashMap.isEmpty_insert` from installed `Std.Data.HashMap.Lemmas` within a
small fixed allocation? Its source at runtime `src/lean/Std/Data/HashMap/Lemmas.lean:50`
states `(m.insert k v).isEmpty = false`, requiring `EquivBEq`/`LawfulHashable`.
This observes real-library conversion/closure cost, not usefulness or acceptance.

Let `P` be canonical-root-relative
`experiments/v5-local-checks/multi-source-package01/suite/assembled/package`,
`L` be `software/runtime/lean-4.34.0-windows`, and `Y` be `D:\Python314`.
Expand these to absolute paths; none is an environment-variable instruction.
PROFILE SHA-256: `ca257419f464c2e9d968011983673160377f743ebbe2a27e2399b510dce1ce67`.
INSTALLATION: `32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.
Implementation: `fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df`.
Adjacent ASSEMBLY: `ec5ab7709aba2c4a896fa1898e925effb8f7a95f17bdb300c55307fcc5c10d6c`.
Keep existing executable/support/runtime identities; no rebuild or package edit.

## Inert inputs, not a fabricated Lean project

Root creates only `PROJECT.json` and `TARGETS.json` here, then snapshots them.
Use UTF-8 canonical compact JSON, sorted keys, no BOM/trailing LF; the project
parser requires exact canonical bytes. Final formatting precedes hashing.
Project has exactly `schema`, `project_search_paths`, `modules`. Its schema is
`DMKN_ORDINARY_TRUSTED_PROJECT_EXTRACTION_V1`; its only search path is absolute
`E:/Distributed Trustworthy Mathematical Knowledge Network/software/runtime/lean-4.34.0-windows/lib/lean`.
Its `modules` field is exactly:

```json
[[[0,{"$bytes":[83,116,100]}],[0,{"$bytes":[68,97,116,97]}],[0,{"$bytes":[72,97,115,104,77,97,112]}],[0,{"$bytes":[76,101,109,109,97,115]}]]]
```

`TARGETS.json` is exactly the following single-element name array:

```json
[[[0,{"$bytes":[83,116,100]}],[0,{"$bytes":[72,97,115,104,77,97,112]}],[0,{"$bytes":[105,115,69,109,112,116,121,95,105,110,115,101,114,116]}]]]
```

`library_extraction.selected_project` requires 1–16 ordinary absolute roots;
the runtime library root is permitted. `BaselineExporter` prepends the same
runtime root and privately imports the selected module (`loadExts=false`, no
plugins). That duplicate across prepend/selection is not a duplicate input root.
The five directly named `L/lib/lean/Std/Data/HashMap/Lemmas` artifacts exist:
`.olean` 1352840 B, `.olean.private` 757592 B, `.olean.server` 167712 B,
`.ir` 5920 B, `.ir.sig` 176 B. Root may pin these plus explanatory source bytes;
this is not transitive artifact hermeticity. Do not scan/rehash the whole runtime.

## Direct public invocation and finite envelope

Existing `Run-V5-Check.py` accepts the pinned launcher because its argv contains
snapshot paths; it does not require a new executable adapter. Expand this argv:

```text
Y/python.exe -I -S -B P/run.py
  --profile-sha256 <PROFILE above> --python-runtime Y --lean-runtime L
  --diagnostics {output}/public-launch
  --wall-seconds 90 --cpu-seconds 45 --memory-mib 1024
  --active-processes 3 --stdout-bytes 1048576 --stderr-bytes 1048576
  owner -- produce-baseline
  --project-production {snapshot}/software/v5/ordinary_std_export/PROJECT.json
  --project-production-sha256 <final PROJECT hash> --approve-local-project
  --output-names {snapshot}/software/v5/ordinary_std_export/TARGETS.json
  --output {output}/bundle --spool-mib 144
```

`owner` is positional; output-names is a file path, not inline JSON. Add no state,
catalog, custody, parent, status or unrelated flags, including explicit defaults.
Root's proposed outer envelope: 120 wall s, 60 CPU s, 1280 MiB, 4 active processes,
4 MiB stdout/1 MiB stderr. Hierarchy is launcher → owner → baseline worker →
native exporter: outer needs 4; launcher's child tree needs 3. The operation's
internal default cap is 4, but its selected worker/native subtree needs 2;
nested Jobs intersect, not add allowances. No extra native memory allowance.
Public minimum is 35 wall/4 CPU; owner needs 30 wall/2 CPU remaining after
subtracting 3 wall/1 CPU. Native grant further subtracts 24 wall/1 CPU for cleanup.
Thus 90/45 is an envelope, not 90 seconds of native work or a completion promise.
144 MiB spool is the existing minimum authorization: 64 writer + 64 evidence +
2 manifest + 12 metadata + two 1 MiB logs. It is neither expected size nor a hard
filesystem quota. Limits are unchanged; first exhaustion is an observed refusal.

## Outcome, accounting and stop

Require outer closure/pin checks, launcher `CLI_EXITED_ZERO`, and actual owner
`ok:true`/`PRODUCED_INERT_BASELINE_NOT_ACCEPTED` for export completion. Launcher
success alone is not mathematics. Owner always says mathematical_acceptance=false
and acquisition_fit=`NOT_ESTABLISHED_RECEIVER_RELATIVE`; `PRODUCTION.json` is a
pre-manifest observation, not replayable success authority. Inspect manifest and
all selected unit bindings, target, full groups, closure and bytes after success.
Compare admission, receive and cold/anchored realization limits independently.

On refusal retain phase/error, native stderr, partial outputs and all reports;
manifest presence alone is not success. Unknown native CPU charges the entire
native grant; owner accounts worker CPU once in `finally`. Report outer inclusive
Job CPU plus its wrapper separately, not the sum of nested inclusive reports.
Saved six-unit predecessor cost 7.393 wall/4.859375 known CPU seconds is context,
not a prediction. Whole loaded-environment indexing precedes selected export.
No intake, new theorem, neighboring target, retry, cap increase or implementation
follows automatically. Root adopts the first outcome and chooses the next step.
