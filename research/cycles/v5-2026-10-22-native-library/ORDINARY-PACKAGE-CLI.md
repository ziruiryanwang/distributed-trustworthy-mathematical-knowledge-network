# Persistent ordinary owner CLI: source implementation

2026-10-23. Agent `owner_cli`. Source-only; no build, test, native operation,
state opening, network access or Git mutation was performed. Root owns source
selection, finite runtime validation and adoption. The new sources are
`software/v5/ordinary_package/owner.py`, `profile.py` and `author_worker.py`.
The existing acceptance core and used generic contribution source are unchanged.

## The concrete workflow

An owner builds/selects one package, initializes one local catalog/custody pair,
submits caller-chosen declarations, closes the command, and opens the same owner
again. No diagnostic store copying or experiment fixture plan is required.
Existing ordinary admission, portable catalog, inert custody and generic source
contribution remain the only implementation paths. This is not an alternative
acceptance implementation or a competing mathematical authoring environment.

The package directory is the executed `owner.py` parent. The public invocation is:

```text
<selected-python> -I -S -B <package>/owner.py <init|status|contribute>
  --profile-sha256 <exact PROFILE.json hash>
  --python-runtime <absolute Python distribution root>
  --lean-runtime <absolute Lean distribution root>
  --catalog <absolute local catalog directory>
  --custody <absolute local custody directory>
  --store-id <64 lowercase hex characters>
  --custody-limits <absolute JSON file>
  --wall-seconds <35..3600> --cpu-seconds <4..200000>
  --memory-mib <1..8192>
```

All command-supplied filesystem paths must be absolute. Their parent directories
must already exist. State, package and runtime roots cannot overlap. Contribution
output must also be fresh and disjoint from all those roots. Failures do not
delete any partial directories, restore old state or retry automatically.

`--custody-limits` has exactly the existing `objects`, `exports`, `logical_bytes`
and `db_pages` integer fields. Reopening requires the same existing custody
limits. `init` additionally allows `--catalog-limits <JSON file>`; omission uses
the unchanged `P.Limits()` defaults, including 4,096 roots and 8,192 operations,
not the old example's tiny capacities. Reopening reads exact local catalog limits
from its protected ADOPTION marker and binds the selected store/implementation.
This is normal local opening, not importing a foreign snapshot or warrant.

## Operation-specific interface

- `init` requires fresh catalog and custody paths. It creates those stores and
  calls existing `owner.initialize` once. Success JSON has
  `result.basis.local_root`. Failed initialization leaves its partial state;
  init does not reopen/replay an old library.
- `contribute` additionally requires `--parent-root`, `--source`,
  `--acquired-targets`, `--output-names`, and `--output`. Parent is an explicit
  existing local root, never a guessed/latest root. Source is the owner-approved
  UTF-8 body accepted by the fixed existing wrapper (at most 1 MiB).
- Acquired-target JSON is a list of at most 32 exact `{name,export_id,unit_id}`
  records, possibly `[]`; output-name JSON is a list of 1--32 structured Lean
  names. Each JSON file is bounded to 64 KiB and accepts ordinary whitespace,
  using the existing bounded duplicate-rejecting owner JSON reader.
- `contribute` calls unchanged `contribute_source`, writes its existing result
  and failure files, and returns `result.local_root`, `result.targets` and
  `result.admission`. It does not require use of every acquired target or claim
  theorem novelty. It does not execute index publication or a network request.
- `status` returns at most 32 stored root IDs/parents by default (`--limit` up to
  256), with an explicit lexicographic `--after-root` cursor and `has_more`.
  Optional `--context-root` calls existing `catalog.context` for that exact root
  and summarizes names/modules/artifact bytes without native proof replay.
  No whole-library enumeration or latest-parent inference is necessary.

Status uses a bounded SELECT through the already-open protected catalog
connection because the current catalog has no listing method. It does not
create a separate database opener or mathematical authority. Normal owner open
may settle stale RESERVED operations as INTERRUPTED; status is therefore **not**
advertised as a strictly read-only operation. Inventory IDs and the known basis
root identity alone are not transferable warrants or successful native checks.

The command emits one JSON result on stdout and exits zero only when `ok` is
true. Runtime failures preserve their phase, error and known accepted state.
In particular `ContributionError.report` is retained intact: a later preview or
log failure must not conceal an earlier successful mathematical admission.
Close failures are reported separately. No output is erased to manufacture a
successful retry.

## Selection and import boundary

The descriptor is exactly the shared `DMKN_ORDINARY_OWNER_PROFILE_V1` schema in
`ordinary_package/INTERFACE.md`. It is canonical JSON, not executable peer data.
The root-supplied profile hash selects bytes; it is not publisher authentication.

1. The owner-trusted stdlib entrypoint checks PROFILE's exact hash and the exact
   selected `owner.py` and `profile.py` bytes. It loads the verified loader bytes
   explicitly, not by unqualified `import profile`.
2. The loader validates path components, rejects links/reparse points, checks
   each auxiliary hash/size, and requires exact complete file inventories for
   authoring helpers, authoring Python and namespace support search paths.
3. It binds INSTALLATION.json to the descriptor, checks all six installed core
   Python files before importing them, and rejects extra files in core `py/`.
4. It puts that installed core first on the import path, followed by the six
   selected authoring helpers and eight namespace support files. Preloaded
   conflicting core/helper/namespace modules are refused.
5. Unchanged `NativeInstallation.open` validates remaining installed support,
   named runtime files, running Python/core identities and actual supervisor.
   The loader then constructs unchanged `AuthoringProfile` and calls its verifier,
   which also checks actual shared core identities inside helper imports.

The loader requires all thirteen authoring `.olean` modules; only their selected
`.olean.private`, `.olean.server`, `.ir` and `.ir.sig` companions are additionally
allowed. Receiver native helpers are never added to authoring LEAN_PATH. The
generic API repeats its profile check after source authoring as before.

Entrypoint/Python/OS integrity, owner selection and immutable local storage are
still premises. Before/after byte checks are not defenses against hostile local
race attackers. Named runtime support is not the full Python/Lean distribution.
No self-authentication or hermetic-toolchain claim is made.

## Resource and execution boundary

One parent wall/CPU allowance begins at process startup and spans profile loading,
owner opening, initialization or contribution and result formation. Worker CPU
is charged once into that ledger; subsequent one-use operation budgets are
derived only from the original remainder. No retry or budget reset is present.
The existing native operation keeps its supervisor/quiescence reserve.

Controller wall/CPU checks are cooperative. Native subprocess trees use the
existing Windows Job limits. `--memory-mib` is a native-tree limit, not a hard
controller-RSS limit. An external supervisor is needed for hard controller
containment. Lean source is owner-approved executable code; a Windows Job is not
a hostile-source sandbox. This command is not for remotely supplied source.

The new worker preserves the predecessor's fixed five-argument compile branch:
sanitized Lean/Python environment, explicit helper path, restricted executable
PATH, `-DElab.async=false`, private output and inherited bounded Job. It performs
one compile and does not decide mathematical acceptance.

## Small decision-changing validation, not another benchmark

After independent source review, root should select one clean package build and
one package-only lifecycle: wrong profile refusal before state writes; fresh
init; basis-only caller-chosen definition/theorem contribution; a separate status
process validating the exact new context. All calls use the new package paths,
not old experiment helper paths. Preserve exact stdout/stderr and failure costs.

This validates the new installation/launcher/persistence boundary. It does not
repeat the old acquired-method proof workflow, establish global networking,
justify useful-growth margins, support arbitrary Lake projects or complete v5.

## Saved lifecycle01: public definition visibility

The retained `ordinary-package-lifecycle-01` authoring stdout reports a
definitional-equality validation error for the public theorem
`applyTwice f x = f (f x) := rfl`, with the explicit note that definitions unfolded
for an exported theorem must be exposed. The generated source has `module` and
`public section`, followed by an unannotated `def applyTwice := ...`. Request
construction completed with zero acquired groups and no introduced signatures;
this is not a missing receiver theorem or certificate problem.

Source inspection of the selected Lean 4.34.0 distribution gives a direct
explanation. `Lean/DefEqAttrib.lean`'s `validateDefEqAttr` emits exactly this note
when equality fails in the exporting environment but succeeds under
`withoutExporting`; the file also documents implicit definitional-equality
attributes for the syntactic `:= rfl` form. `Lean/Elab/MutualDef.lean` defines
`@[expose]` as making a definition's body available to importing modules, and
handles it while declaring the `def`. `Lean/AddDecl.lean` describes exposure as
preserving the full representation in the public scope. Thus public visibility
of a name alone does not imply public availability of its reducible body.

The smallest justified caller-only correction is:

```lean
@[expose] def applyTwice {a : Type u} (f : a -> a) (x : a) : a := f (f x)
```

Keep the theorem statement and `:= rfl` unchanged. With that body exposed,
`applyTwice f x` delta/beta-reduces to `f (f x)` in the public environment; the
reflexivity argument is the same. The annotation changes module exposure, not
the definition's mathematical body, permitted axioms, receiver relation or
checking rules. Do not globally expose all definitions or modify the frozen
wrapper/package just to accommodate this example. This is a source-level
justification, not a claim that the corrected actual call has already passed.
The failed call remains retained; root separately selects any caller-only
continuation, using the existing initialized owner without rebuilding/replaying
its basis. No runtime was executed by this diagnosis.

## Independent changed-runner review: continuation01

Reviewed root-authored `ordinary_package/continue_lifecycle.py`, SHA-256
`e2344e4e701655b8a6863a00f8c2ae7b498510680654753b28512f63ab4ab0cc`,
against the saved lifecycle outcome, actual caller body/output names and original
selection SHA-256 `adf5d883fd81b25e293715276f10de1a58240206d2d13089efd748e648f872c7`.
**No source blocker found for root's file-only selection and separately selected
bounded continuation.** This review neither executes it nor claims a passing run.

`--select` checks the exact prior selection and all retained package/runtime
pins, requires the saved three-call failure shape, and adds pins for the prior
outcome, caller body, target/acquired/limit files and immutable ADOPTION marker.
It writes a fresh selection only. Mutable catalog/custody databases are not
misclassified as frozen runtime attachments; their continuation is the selected
state change. No original result, failed contribution file, package or native
artifact is opened for writing by the runner.

`--run` changes the single pinned `def applyTwice ` occurrence by inserting only
`@[expose]` on the preceding line into a fresh output source. It invokes only
public `contribute` and then fresh-process `status`, with the original catalog,
custody, store identity, package and explicit basis parent. Saved success selects
that parent; actual protected owner opening/context/admission remain authority.
There is no init/build/store-copy path and no retry loop. Success checks require
two actual new checked units, exact requested names, two evidence files and two
previews with matching returned pins, then the same two-root context on reopen
with zero native worker CPU for status. The field assumptions match the CLI.

The runner has one original 120-second deadline. Each public invocation has at
most 90 seconds and 60 CPU seconds, shortened by the remaining wall deadline;
the selected outer Job bounds the **aggregate** at 150 wall / 100 CPU seconds,
1,792 MiB and eight processes. The per-call CPU limits are not a claim of a
single 60-second aggregate allowance. Timeouts/refusals preserve raw command
stdout/stderr and partial state; the final continuation report retains completed
call results, including any API-reported accepted state. Outer Job CPU already
includes nested workers and must not be added to their reports again. Existing
lifecycle01 costs/failure stay separately charged. This is one caller-visibility
correction and persistence check, not new mathematical-growth evidence.
