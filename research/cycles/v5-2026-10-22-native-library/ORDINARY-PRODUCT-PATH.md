# Next product seam: ordinary admission with exact dependency resolution

2026-10-23. Source-only assessment by `ordinary_product_path`. Canonical guard
passed. No test, compiler, native import, catalog opening, migration, network
operation or Git change was run. This is a concrete implementation recommendation,
not a new acceptance result. The active full-v5 goal is unchanged.

## Decision

After the selected one-unit native handoff discriminator, stop extending the
migration/alias harnesses. Implement one reusable **ordinary admission core**:
finite complete V2 evidence goes in; an exact missing-dependency frontier or an
actual checked local extension comes out. Connect the already implemented formal
index and the newly assigned typed custody transport to that core. This is the
smallest path from the tested components to a user-operable contribute/reuse loop.

Do not restart the running import merely to polish the proposal below. It is a
historical development context with explicitly selected support, not the final
installed public acceptance core.

## Two concrete missing links

### An imported ExportID is not an evidence locator

`portable_evidence.read_evidence` accepts direct imports `[original_name, symbol]`.
`ordinary_semantics.export_id` computes

\[
e = H_{\mathrm{export}}(S,u,n),
\]

where `u` is the UnitID. The assigned evidence transport accepts `(S, u)`.
A receiver with only `(S, n, e)` cannot recover `u` by reversing this hash.
Consequently, fetching the target unit does not yet enable acquiring a genuinely
missing *peer* dependency. The installed-Std missing-import exporter solves a
different problem: known original names in a selected installed library. It is
not a network ExportID resolver.

The smallest correction is an **untrusted exact export locator**. When inert
custody parses a unit, derive all `(S, e, n, u)` rows from its output census and
store the rows with its exact raw evidence. Offer an explicit lookup by `(S,e,n)`
using the existing `DMKN_ORDINARY_LEAN_EXPORT_LOCATOR_V2` shape, or return that
unit's raw evidence directly. A client verifies the requested S/name, recomputes
UnitID and ExportID, and checks that the unit actually declares the named output.
It then performs ordinary mathematical admission. A lying/absent resolver causes
failure or charged work, never an alternative theorem meaning.

This is exact location, not formal relevance search, a trust registry or a global
name service. Multiple custodians can supply the same bytes. For a fixed-basis
symbol the selected F already fixes its meaning; do not ask a peer to define it.
The request/byte/deadline budget is shared with target acquisition and includes
failed replies. No unbounded ancestry crawl or automatic renewal is required.

### A checked snapshot is not durable public evidence

`PortableCatalog._commit_checked` records ordered UnitIDs, output bindings,
native snapshot bytes and checking provenance. It does not retain the complete
raw V2 units or an export-to-unit reverse index. The alias controller currently
writes `evidence.json` outside its catalog, as experiment evidence. After ordinary
contribution, a provider still needs the actual inert proof-bearing bytes to
publish and answer dependency requests; it cannot reconstruct them from hashes
or names alone.

Use the assigned `OrdinaryStore` for those bytes. Stage each exact, parsed raw
unit and its derived export locator rows durably before the final admission
success can be exposed. Custody insertion is idempotent and not mathematical
authority. Failed checking may leave bounded inert data, charged to custody;
only the protected catalog makes the accepted-name relation. Publication after
commit can be retried explicitly without rechecking the theorem. Public records
and proof-free previews are derived from the same retained evidence.

No distributed transaction is needed: storing inert bytes first is safe. If
the process stops before catalog commit, custody has an unaccepted claim. If
it stops after commit but before advertising, accepted local mathematics remains
usable and its retained evidence can be published later. Storage quotas and the
nonrenewing overall grant still apply.

## Smallest public core

Select one new module, tentatively `ordinary_admission.py`. It should be usable
by a CLI/SDK but should not itself choose research objectives, index providers or
theorems. Suggested boundary:

```text
OrdinaryAdmission.open(installed_support, catalog_directory, evidence_store)

preflight(parent_root, raw_units, limits)
  -> READY(parent_root, ordered_unit_ids, immutable_raw_units, expected_outputs)
   | NEEDS(parent_root, exact_missing_imports)
   | CONFLICT_OR_UNSUPPORTED(reason)

admit(parent_root, ready_plan, operation_budget)
  -> CHECKED(new_local_root, newly_accepted_exports, retained_unit_ids)
   | bounded explicit failure
```

`installed_support` is owner-adopted installed configuration, not a peer-supplied
path or a `compatible=true` declaration. `operation_budget` includes an absolute
parent deadline and finite CPU/output/process limits. A plan is convenience
metadata, not an authority token: the admission path reparses immutable bytes
and uses the actual protected parent before reservation.

Preflight should report the **whole finite frontier**, not fail one name at a
time and repeatedly invoke Lean. For each import `(n,e)`:

- If the protected parent binds `n` to `e`, reuse it.
- If the parent binds `n` to a different ID, report a context conflict; never
  replace the request by a by-name match.
- If a selected new unit exports exactly `(n,e)`, add a dependency edge.
- Otherwise return the exact missing pair for explicit acquisition.

Recompute every proposed export from the actual V2 unit. Reject overlapping new
names, mismatched semantic contracts, unsupported/cyclic or unclosed selected
graphs and exceeded budgets. Topologically order units, preserving generated
declaration groups atomically. A missing answer says only that this bounded
attempt did not acquire it, not that the mathematics does not exist globally.
Use the existing single-batch limit initially; do not invent an unbounded batch
or silently renew a grant. Larger explicit multi-batch workflows can preserve
already checked prefixes under one declared budget later.

The `admit` implementation can reuse the actual-event block already present in
`run_portable_extension.py`: portable reservation; actual stored module plan;
unchanged original worker; exact report/module/output census; clean supervised
closure; private commit; reopen verification. Remove alias construction, hardcoded
target, entire-source catalog copying and experiment result paths from that
reusable core. Normal contributions operate on the owner's active catalog; they
do not duplicate the whole library for each call. No new checker, native snapshot
format, certificate mechanism or math-library replay is needed for this seam.

## Stable acceptance support, not a hash of every workflow script

The development selector currently sets `I.controller_support` to the complete
import selection source map. That map includes selectors, migration driver and
the one-alias controller. `PortableCatalog.open` binds exact I to its marker.
Consequently adding a new trusted admission controller cannot honestly be called
part of that old source map, and opening the old catalog under a changed I is
refused. Including the alias controller before the current import closes that
specific test handoff, not the general public API problem.

For the installed product, identify a small stable **acceptance-core support
manifest**: V2 parser/identity, catalog, native worker/codec/snapshot handling,
bounded supervisor and the generic admission controller. CLI, formal ranking,
transport, authoring prompts and arbitrary candidate generation supply inert
inputs to this fixed boundary; adding such nonauthoritative workflows should not
change the mathematical implementation identity. The importer has separately
recorded translation provenance and should not force every ordinary operation
to depend on a historical test selector.

Do not simply drop needed source pins to make equality pass. Existing accepted
snapshots retain their actual checker/controller origin and withdrawal support.
A future change to the acceptance core still needs explicit owner adoption and
compatibility/update policy; the current one-I catalog does not already implement
arbitrary mixed-I upgrade. That is distinct from implementing the stable first
public core. The ongoing development import should remain retained unchanged.

## V2 authoring is a thin, real remaining adaptation

The ordinary authoring machinery is reusable but not already V2. In
`owner_request.prepare`, V1 basis and export IDs are recomputed from
`profile_id`/`basis_id`; it calls the V1 evidence parser and emits
`DMKN_OWNER_REQUEST_V1`. `OwnerConstructCommand` requires that header, stores
profile/context/basis labels, and `ConstructExportCommand` emits the V1 candidate
bundle. Replacing only a JSON label would therefore be wrong.

Select an explicit V2 request/candidate version with S, F and local context root,
using portable evidence and portable basis/export identities. Reuse the existing
selected semantic-closure traversal, group packets, scratch construction,
deferred import stopping and complete new-unit exporter. Those raw Lean rules
need not be redesigned. The thin command header/export wrapper may change while
the original expression/declaration/checker primitives stay fixed.

The authoring environment and temporary theorem signatures remain nonauthoritative.
An unresolved candidate name may be resolved only against the receiver's chosen
protected context or through explicit exact dependency evidence. Name resolution
for candidate construction must never become an identity-substitution rule for
already advertised V2 evidence. Final complete new units always enter `admit`.

## Coherent user path and priority

1. `contribute`: export complete local candidates, resolve the finite dependency
   frontier, run the generic admission core, retain evidence, publish previews.
2. `discover`: issue local-agent-selected formal predicates through the existing
   SearchSession/SearchClient and inspect returned proof-free types and coverage.
3. `acquire`: bind preview to the record, fetch exact unit and only missing exact
   dependencies under one budget, independently admit them.
4. `reuse`: prepare selected warranted targets for ordinary Lean source authoring;
   exported new work returns through the same contribute path.

The two immediate correctness/integration gaps are the exact missing-dependency
locator and generic actual-event admission; V2 authoring then closes reciprocity.
Removing fixed experiment installation paths and assembling relative installed
support is necessary product work, but not a new mathematical theory. More
migration controls, another alias, full-library replay, larger local peer counts
and mandatory certificates do not advance this public seam.

Do not infer growth benefit from this path merely working. Keep the strong
ordinary-library baseline and full-cost criterion in `PAYOFF-AUDIT.md`. Selective
contexts, context conflict handling, cold loading cost, useful-query selectivity,
hostile-input isolation and public maintenance/update obligations remain real
release issues. The next result should be **one reusable API that real agents can
call with unfamiliar evidence**, not another fixture-specific accepted theorem.

## Selected implementation checkpoint: installation-relative admission core

Root selected source-only authoring of
`software/v5/ordinary_lean/ordinary_admission.py`. The first source cut now exists;
independent `admission_event_audit` is reviewing it. This agent has run **no Python,
parser tests, compiler, Lean worker, catalog opening, migration or network call**.
No installed implementation or actual checking result follows from this source.
The root alone owns later execution/adoption/Git decisions. Existing experimental
I and accepted contexts remain unchanged; no controller-support bypass is added.

### Concrete public API

```python
installation = NativeInstallation.open(
    installation_root, exact_manifest_raw, expected_manifest_sha256,
    runtime_roots={"python_runtime": python_directory,
                   "lean_runtime": lean_distribution_directory})
admission = OrdinaryAdmission.open(
    installation, catalog_directory, store_id, evidence_store,
    create=False, limits=portable_catalog.Limits())

budget = OperationBudget(wall_seconds, cpu_seconds, memory_mib,
    active_processes=4, output_bytes=64*1024*1024, log_bytes=1024*1024)
admission.initialize(budget)  # only a fresh catalog: existing fixed basis worker

plan = admission.preflight(parent_root, raw_units,
    limits=PreflightLimits(), budget=budget)
result = admission.admit(parent_root, plan, budget)
admission.close()  # does not close caller-owned inert custody
```

Use a separate budget for initialization and the later contribution. A budget
starts when created, has one absolute monotonic deadline, charges observed child
CPU plus parent process CPU, and may launch at most one native operation. The
existing selected Job supervisor reserves cleanup time inside that parent budget.
Python checks are cooperative; the native subprocess tree has actual Windows Job
limits. A host requiring hard controller bounds must supervise the Python owner
process too. Neither mechanism is described as a hostile-source sandbox.

`Preflight` is frozen convenience metadata:

- `status`: `READY` or `NEEDS`.
- `parent_root`: the actual protected local context identifier.
- `raw_units`: all unique exact requested V2 units, including entirely reused ones.
- `ordered_units`: new units in deterministic topological order.
- `missing`: the complete finite tuple of `(canonical_name_bytes, ExportID)`.
- `reused_unit_ids`: exact units whose whole output group is already present.

Conflicting names/IDs, incompatible S, partial-known generated groups, selected
cycles and exceeded byte/unit/node/name/edge bounds raise explicit refusals.
Two missing requests demanding different meanings for one original name are
already a conflict, not a solvable two-entry acquisition frontier. Inputs are
reparsed against the protected context in `admit`; forged plan status/order cannot
skip that boundary. Initial native batch ceilings remain 1024 units, 64 MiB,
2,097,152 decoded nodes and 65,536 new names; no silent multi-batch renewal exists.

`admit` inserts and reads back every requested raw unit using an owner-adopted
durable-custody API before a native grant can be promoted. The actual installed
integration must supply the reviewed `OrdinaryStore`; the core's callable checks
and readback establish byte binding, **not crash persistence**. Durability is an
explicit trusted dependency contract under the nonhostile-owner-process model.
It remains outside mathematical I: a dishonest retention promise harms
availability, but cannot replace the actual kernel event. Failed checking
retains inert custody safely. Entirely reused evidence returns `REUSED` without
a worker; new work returns `CHECKED` only after a clean actual worker event,
exact report/grant/module/name/output matching and private catalog commit. Logs
are retained in `catalog/admission-calls/<random-id>` outside the grant's one-file
artifact directory. No full-store copy, arbitrary callback checker, network
dependency crawl, fixture-specific target or experiment path is in this core.
The catalog's artifact-byte quota does **not** charge this orchestration spool.
Each input/report/log has a finite per-call limit and grants have a finite count,
but durable call-spool capacity is a separate owner responsibility. Custody has
its own actual store quota. Do not claim `output_bytes` or the catalog's total
snapshot limit is a whole-process disk-space bound.

If native cleanup is uncertain, the core writes sticky `WITHDRAWN` and closes the
catalog rather than permit new work while a possible child survives. Clean failed
checks preserve and charge their failed grant. A stored supervision report is
diagnostic only; the live returned event is the authority prerequisite.

### Exact installation manifest

The owner-adopted canonical JSON has exactly six fields:

```text
schema = DMKN_ORDINARY_NATIVE_INSTALLATION_V1
implementation = ordinary_semantics implementation descriptor
roles = exact role -> logical relative file
compiled_dirs = flat relative helper directory -> sorted .olean filenames
support_groups = implementation support field -> sorted relative file paths
files = relative file path -> {bytes, sha256}
```

Roles are `python`, `python_dll`, `python_stable_dll`, `lean`, `worker`, `seed`,
`inventory`, `supervisor`, `job`, `domains`, `core`, `evidence`, `semantics`,
`portable_evidence`, `catalog`, and `legacy_catalog`. Paths beginning
`python_runtime/` or `lean_runtime/` resolve under the two explicit owner-supplied
runtime attachments; every other path remains installation-relative. Roles fix
`python_runtime/python.exe`, adjacent `python314.dll` and `python3.dll`, and
`lean_runtime/bin/lean.exe` with the six named Lean binaries in that directory.
Core/source/compiled helpers cannot hide behind runtime attachments. The roots
must be disjoint, ordinary owner paths. Absolute attachment paths are invocation
configuration, not portable mathematical or implementation identities; their
logical roles and actual file pins are committed. This allows an existing
`D:\Python314` interpreter and a separately installed Lean distribution without
copying hundreds of MiB or rebuilding the runtime merely to exercise the API.

The six Python core files
are siblings with their actual fixed filenames. The native worker is the existing
`OrdinaryWorkflowWorker.lean` with all eight actual helper sources/object files;
the flat compiled directories have an exact census, no extra shadowing modules.
Pinned Lean binaries are the existing six named kernel/runtime files. The basis
uses the exact prior seed and inventory SHA256 values and byte sizes, not another
foundation interpretation.

The five support groups cover all named files. Mandatory coverage is:

| Support field | Mandatory selected bytes |
|---|---|
| `kernel_support` | Six named Lean executable/shared-runtime files |
| `adapter_support` | Eight native helper sources and compiled `.olean` files |
| `basis_receiver_support` | Seed/inventory and bootstrap/basis source/object pairs |
| `snapshot_support` | `LocalSnapshot` source/object pair |
| `controller_support` | Six stable Python core modules, supervisor/Job/domains, Python executable and two DLL roles |

For each support field, `support_digest(field, manifest)` hashes the domain
`DMKN-ORDINARY-INSTALLED-SUPPORT-V1` and canonical `{field, files}`. Controller
support also includes the relative `roles` and `compiled_dirs` bindings, so
changing an execution role/search selection cannot retain I merely by keeping
the same unordered file set. The externally pinned manifest includes the exact
implementation descriptor. None of these commitments is itself a proof of
checker correctness; root/owner adoption and retained semantic assurance remain
premises.

Large named support is verified once when opening the owner installation; the
immutable installation/OS premise then applies. Small operation inputs, actual
worker output and live grant/event bindings are checked each call. The internal
worker shim reads the exact pinned operation manifest, invokes only `basis` or
`extend` through selected Lean with scrubbed language paths, and inherits the
parent Job. It cannot open/promote a catalog. This avoids rehashing hundreds of
megabytes of immutable runtime for each small theorem while retaining explicit
named-support integrity. The installation is explicitly not a hermetic build or
an arbitrary-runtime portability claim.

Selectors, experiments, alias fixtures, discovery rankers, provider selection and
owner source-authoring workflows are excluded from controller support. They
supply inert candidates, not the actual acceptance event. Transport custody's
durability is a separate owner-store premise, not mathematical authority.

### Original-deadline repair selected by root

The prior portable catalog computed a grant's deadline after its own context
and evidence parsing. Passing an integer duration computed before that parsing
could put its deadline later than the operation's original deadline. The first
core detected and refused such a grant before native launch, preserving safety
but potentially refusing a large otherwise affordable request. Root preserved
the baseline in Git `56d1f89` and existing experiment snapshots, then explicitly
selected and authored the narrow catalog successor: optional absolute
`parent_deadline` forwarded through both reservations and clamped before grant
registration. The admission core now supplies `budget.deadline` to both calls;
the final `grant.deadline <= budget.deadline` check remains. Independent review
and any changed-boundary runtime selection belong to root; this agent did not
edit or execute the catalog.

Next evidence should exercise the new public core on a small fresh basis and
ordinary substantive contribution/reuse path. It should not replay the adopted
2859-unit development library just to acquire a stable I. Independent source
review precedes any root-selected finite execution.

### Small owner installation assembler

Root additionally selected source-only `ordinary_installation.py` (new file,
not a change to either catalog or frozen installation). Its concrete callable is:

```python
assemble(destination, plan_raw, expected_plan_sha256,
    runtime_roots={"python_runtime": python_directory,
                   "lean_runtime": lean_distribution_directory},
    deadline=absolute_monotonic_parent_deadline)
```

The pinned canonical plan has `schema=DMKN_ORDINARY_INSTALLATION_PLAN_V1`,
`roles`, `compiled_dirs`, `support_groups`, and `files`; each file entry is
`logical_path -> {source: absolute_owner_path, bytes, sha256}`. Role/group/layout
shapes follow the admission manifest. The assembler computes implementation
support digests and host platform, copies only explicitly enumerated nonruntime
files into a fresh destination, and verifies source/copy/source pins. Selected
runtime attachment files are verified in place, never duplicated. Named support
is capped at 512 files/2 GiB; actually copied bytes at 256 MiB. Ordinary path,
file/directory alias, runtime binding, source/destination overlap, exact compiled
directory-file selection and one nonrenewing deadline are enforced.

The manifest is written/fsynced as `.INSTALLATION.pending` and only then renamed
without replacement to `INSTALLATION.json`. Earlier failure leaves a retained
partial destination without a completed manifest; no automatic cleanup, retry,
overwrite or directory-tree copy occurs. Runtime attachment immutability remains
an owner premise; the assembler does not scan the whole runtime installation.
The result is explicitly `ASSEMBLED_NOT_ADOPTED`. Actual supported role/module
structure is checked by `NativeInstallation.open`; file assembly cannot establish
kernel correctness or authorize opening an old-I catalog.

CLI flags are `--destination`, `--plan`, `--plan-sha256`, `--python-runtime`,
`--lean-runtime`, and `--seconds`. No compiler/native process, peer code, catalog,
old math library or experiment-specific path occurs in the assembler. The source
has not been run by this agent; root owns review and any finite invocation.
