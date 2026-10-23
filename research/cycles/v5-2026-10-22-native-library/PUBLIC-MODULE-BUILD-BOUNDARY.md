# Public-module build: narrow wait investigation

2026-10-23. `preview_boundary_review`. Read-only/source-only investigation.
No runtime, retry, source modification, limit change or Git operation performed.

## Saved observation

`ordinary-public-support-build-01`, selection
`18753758cd0c85a34457e65bd83c067462a90525517202e28c1743ab9382946e`,
failed at the first generated module, `OriginalExpr`. The inner Python
`subprocess.run(..., timeout=45)` raised `TimeoutExpired`. Both native log files
are exactly zero bytes and the build directory has no emitted artifact.

The completed outer report records 1.765625 Job CPU seconds, 433,418,240 bytes
peak private commit, three total Job processes, zero final active processes,
direct child reaped and Job closed. This is not an OOM report or proof that
three processes were simultaneously active. The report contains no per-process
identities and no phase marker, so it cannot locate the exact wait or attribute
the third process to a missing compiler worker.

The generator only adds `module`, changes leading imports to `public import`,
and inserts `public section`; it retains each original body byte-for-byte.
The receiver's original support artifacts are not involved in this compilation.

## Relevant installed Lean 4.34 source

All references are under the retained `src/lean/Lean` tree.

- `Elab/Import.lean:150`: a modern module imports at `.exported` level in the
  command-line frontend; a legacy file imports at `.private`. The header change
  is a genuine environment/export boundary, not merely an access modifier.
- `Elab/Frontend.lean:292`: the command-line frontend sets `Elab.async := true`
  **only if not explicitly specified**. `CoreM.lean:35` documents the same rule.
- `AddDecl.lean:169`: async mode maps kernel-check work onto the prior checked
  environment task; synchronous mode executes the same check/commit action
  directly. No acceptance bypass follows from disabling async scheduling.
- `CoreM.lean:732`: compilation in async mode creates `promiseChecked`, schedules
  compiler work after `env.checked` and commits the resulting checked state.
  Synchronous mode waits for the checked environment and invokes compilation
  directly. This applies to definitions, not only explicit theorem bodies.
- `Elab/Command.lean:510,557`: async linter/info-tree work adds task/promise
  dependencies; synchronous mode performs those operations directly.
- `Elab/Frontend.lean:339` onward reports/waits on the snapshot tree and final
  command state before serializing the module. `Environment.lean:1838` obtains
  persistent extension state synchronously, and `writeModule` at 1901 emits
  exported/server/private parts and, when enabled, IR parts for modern modules.

These are concrete task-synchronization boundaries that differ from treating
each declaration and code-generation step synchronously. The low CPU/high wall
observation is consistent with a wait but **does not prove an async deadlock**.
Import/filesystem/native-initialization waits remain possible because no phase
was observed.

## What the source does not justify

The normal `Shell.shellMain -> runFrontend -> writeModule` path inspected here
does not launch a separate external module compiler process. Its compiler and
elaboration concurrency use Lean tasks. `findSysroot` can launch
`lean --print-prefix`, but the shell's internal search-path initialization uses
`getBuildDir`, derived from `IO.appDir`; it does not require that helper process.

`LEAN_IMPORT_WORKERS` is read only by `loadIncrSnapshot` in this frontend. This
command has no `--incr-load`, so changing that variable is not a supported
explanation or targeted repair. No evidence supports enlarging the process or
memory allowance, changing machines, loading private dependencies again, or
adding a broad Lake rebuild.

## One selected-next discriminator recommended

Compile **only the same generated OriginalExpr module** in a fresh operation
with one changed compiler option:

```text
-DElab.async=false
```

Keep the same source bodies, import order, Lean runtime, 45-second per-command
timeout, memory cap and process cap. Do not simultaneously change `-j`, imports,
module visibility, IR generation, or run all five modules again. This targets
the demonstrated scheduling boundary while preserving checked elaboration.

- If it finishes, retain its artifacts/evidence and use the actual outcome to
  decide the remaining finite helper builds. This supports a practical serial
  authoring-support route; it does not identify a specific upstream bug.
- If it still waits with similarly little CPU and no diagnostics, do not retry
  longer. The async discriminator did not resolve the boundary. The next
  selection should localize import versus command processing using narrowly
  instrumented source/progress reporting or a fresh minimal module header,
  rather than allocate another unchanged full build.

No compiler result, OwnerRebind semantic qualification or user workflow success
is inferred by this source investigation. Root owns whether to run this one
discriminator; the failed attempt and all used bytes remain preserved.

## Saved outcome audit: first synchronous module succeeded

Later 2026-10-23. The root executed the proposed first-module-only successor;
this subsection reviews saved evidence without rerunning it. Disposition:
**PASS for the selected public OriginalExpr compilation and exact source map,
not for a causal diagnosis or the remaining helper chain.**

Actual run: `ordinary-public-expr-sync-01`, selection SHA-256
`75a53fd0d2905d6b60c52eeb134bf3e2691829eb99e8e697e41d4db8483d93f2`.
The immutable runner is
`aadce94e778c0ac858da922389e743595fc447a6328b06d032a64dbc65682e0c`.
Its `--first-sync` branch compiles only OriginalExpr with
`-DElab.async=false`, retains the 45-second inner timeout and unchanged outer
limits, and has no successful-loop continuation to the other modules.

The saved compiler step exited 0 in **41.222815 seconds**, only about 3.78
seconds below its timeout. Both native stdout/stderr are empty. The outer
operation reports `COMMAND_EXITED_ZERO_AND_CLOSED`, zero final active processes,
direct child reaped, no cleanup errors and 47.810453 seconds wall. Job CPU is
2.453125 seconds; wrapper CPU is 0.546875, giving **3 known CPU seconds**.
Peak Job private commit is 569,872,384 bytes.

**The async explanation remains unproved.** Successful synchronous compilation
establishes a usable artifact, but its 41.22-second low-CPU duration is close
to the original 45-second failure. Cache/I/O/system scheduling or other waits
have not been separated. Do not call this a proven deadlock fix, dramatic
speedup, or justification for more process/RAM allowance. Do not rerun this
passed first module to establish such a claim.

Independent read-only byte reconstruction verified all five source-map rows:
each original hash matches its selected snapshot; each of the four helper
transformations is exactly `module` + public imports + public section with the
entire original body retained; OwnerRebind is unchanged. The generated
OriginalExpr hash is
`2064205249945563302b0ef4c0d3562ff1864730ee4644083a3b888433db2fb9`,
the same as the first failed public attempt. Its body hash is
`b45fd997bfb9b2e30ae73afd47445486b5c8cbfe73245994e81758a9463d8ddb`.
Generating the other four sources does not mean they were compiled.

Exactly five retained OriginalExpr artifacts are present:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `.olean` | 133776 | `70a68712dcdb13b3b52f607d6d14f019190138d0db30609d31fe7f0d3998bcb4` |
| `.olean.server` | 11992 | `491296241cd2759ca5e5f51f56506f5408b77bda187d69595d250d40a474579f` |
| `.olean.private` | 1450872 | `01b0f25619f9005d8f9b252986f03a4bcc6531c492738840866f5a47e1650abd` |
| `.ir.sig` | 176 | `cd0ebce7e616bf8376fbc3bdfa0adb705e20e780702538016d86b5bc34392653` |
| `.ir` | 507584 | `12765236fcbfd7c563bd51d2cd2b166fe76dabdd0f9b56a32390026c1fa41397` |

Root is selecting only the remaining three support modules and OwnerRebind,
reusing these exact first-module artifacts. That continuation is not covered
by this first-module outcome audit. No native mathematical admission or actual
owner-source reuse follows from helper compilation alone.

## Adjacent saved evidence: semantic-identity controls

Also read `ordinary-semantic-identity-01`, selection SHA-256
`ecfa2cf746cfd68fcb98d5289f2e6a53a8b6bc9917c1c600f06c462bbd5e8db3`.
The saved source snapshot matches all four selected source hashes, including
`ordinary_semantics.py` `ee601536...` and checks `9614df54...` recorded in
`SEMANTIC-DESCRIPTORS-IMPLEMENTATION.md`. Actual stdout contains exactly the
four expected PASS groups and final marker:

```text
SEMANTIC_IDENTITY_CHECK exact_selected_descriptors PASS
SEMANTIC_IDENTITY_CHECK implementation_separation PASS
SEMANTIC_IDENTITY_CHECK changed_semantics_not_adopted PASS
SEMANTIC_IDENTITY_CHECK no_legacy_or_parent_relabel PASS
SEMANTIC_IDENTITY_ALL_PASS checks=4 mathematical_acceptance=false
```

Stderr is empty, exit code is 0, and the actual outer Job closed cleanly with
no active process or cleanup error. The cost is 0.078125 Job CPU plus 0.0625
wrapper CPU = **0.140625 known CPU seconds**, 0.265096 seconds outer wall.
This reviewer authored those pure helper/check sources, so this subsection is
a separate saved-outcome examination, **not an independent source audit** of
them. Root separately read the sources. The markers substantiate only the four
synthetic identity/shape discriminators, not Lean validity, a supported alternate
platform, V1 migration, snapshot safety or integrated V2 discovery.
