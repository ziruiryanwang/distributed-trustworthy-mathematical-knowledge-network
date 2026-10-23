# Trusted-project authoring: native-free controls

## Decision and status

The practical workflow is to author a new contribution using an owner's already
compiled Lean project, then send inert mathematical data through the unchanged
independent receiver. The selected source adds explicit authoring support, not a
new checker, automatic project build or peer-selected executable dependency.

These controls focus on the new data-selection and dispatch boundaries. They
reuse the existing profile loader and compiled installation instead of repeating
the reciprocal native workflow. This is source-only work: **the harness has not
been imported, compiled or executed by its author**. Root owns the finite runtime
selection; a separate reviewer owns independent source review.

Harness:
`software/v5/ordinary_project_package/project_controls.py`

SHA-256:
`fe329a9ec4c950e2b2fb453bd8e11ae7fa46f69bbfdc86fb5eaf857c6ec64105`

Root reported the assembled package at
`experiments/v5-local-checks/ordinary-project-package-assembly-01/package`, with
profile SHA-256
`b584cb21266fcf24502355a929939d8e6d662c75d1d7ea520fb23eb6105c7c69`.
The harness checks the selected profile and source pins itself. This record does
not independently audit package assembly or establish runtime success.

## Five groups

| Group | Boundary checked | Deliberate substitution |
|---|---|---|
| Owner JSON | Round trip; rejection of duplicate keys, numeric values, excessive depth, unterminated/mismatched brackets and invalid UTF-8 | None in the parser |
| Closed backend and source | Exact allowed fields and schema; module-name and imported-module injection refusals; path and duplicate restrictions; exact unchanged default wrapper; only the selected import-header insertion; callback refusal | Source strings remain inert |
| Worker invocations | Unchanged default argv; separate generated module root and project cwd; helper/runtime/project search precedence; ambient variable scrubbing; source containment and duplicate-path refusals | `subprocess.call` records argv/options and returns 17; Lean never starts |
| Pre-open CLI refusals | Partial configuration pair, wrong content hash, wrong schema, and project options supplied to init/status | Repeated profile bootstrap is replaced by the already loaded package; both state constructors are refusal sentinels |
| CLI forwarding | No backend keyword on the default route; exact closed backend on the selected route; selection metadata retained | Profile bootstrap, both state constructors and `contribute_source` are explicit mocks |

The real profile loader runs once against the selected package. It checks support
identity; successful loading alone is not mathematical acceptance. The owner and
worker are loaded from their exact descriptor-pinned bytes, with the same admission
core shared by the contribution helper and peer API.

## What is and is not executed

Before package loading, guards replace `sqlite3.connect`, `subprocess.Popen` and
socket `connect`/`connect_ex` with refusal sentinels. After loading, the existing
peer exchange and provider start entry points receive the same guards. The worker
group replaces only `subprocess.call` explicitly, so it can inspect the launch
request without starting a process. These are focused regression controls, not a
security sandbox or a proof that arbitrary code cannot bypass Python monkeypatches.

The forwarding group supplies a synthetic return labelled `MOCK_ONLY`. Its
`CHECKED` field tests CLI data flow only; it is not a native result or warrant.
The fixture includes a canonical synthetic `ADOPTION.json` to reach the CLI's
pre-open input checks. It has **no database** and is not an initialized owner.
Both real owner-opening paths remain replaced throughout the CLI groups.

The harness writes only small inert fixture/configuration files and its final
`PROJECT-CONTROLS.json` beneath the selected output directory. It does not open
SQLite, compile Lean, build a project, create an owner, connect to peers or mutate
Git. Existing package/runtime directories are not output destinations. All
generated fixture files use exclusive creation; a used output is not a retry.

## Prospective invocation and allocation

The selected isolated Python runtime must invoke the harness with `-I -S -B` and
the five required arguments:

```text
<selected-python> -I -S -B <absolute-project_controls.py>
  --package <absolute-selected-package>
  --profile-sha256 <selected-profile-hash>
  --python-runtime <absolute-selected-Python-root>
  --lean-runtime <absolute-selected-Lean-root>
  --output <absolute-fresh-supervised-output>
```

Runtime paths, code pins and output allocation must come from root's reviewed
selection, not from the placeholders above. The output directory itself is
prepared by the outer selection; the harness exclusively creates its fixture and
report within it.

The original internal allowance is 50 wall seconds and 30 controller CPU seconds,
measured from process entry and not reset between groups or mocked CLI calls.
Root's proposed outer envelope is 60 wall seconds, 35 CPU seconds, 512 MiB and two
processes. The root-owned `select_validation.py` records the exact selected
envelope and pins before execution. No launch is authorized by this checkpoint.

## Interpretation

A future passing report would establish only that these five focused controls
passed on those exact selected bytes. It would not establish real-project
compatibility, hostile-source isolation, native mathematical acceptance, global
network operation, useful growth or final-v5 completion. No existing user project
has been selected by this subtask, and the inert fixture is not ecosystem evidence.

If a group fails, preserve its output and failure. Do not edit a used harness or
silently repeat its allocation. A consequential repair or native project workflow
requires a separately selected successor and decision-changing scope.
