# Inert baseline bundle source checkpoint

2026-10-24. `cold_intake_strategy` source implementation under
[root's exact selection](ORDINARY-BASELINE-IMPLEMENTATION-SELECTION.md).
The initial assignment owned only `software/v5/ordinary_baseline/baseline_bundle.py`
and this checkpoint. Root's later producer-controller continuation also selects
fresh `baseline_production.py` and `baseline_worker.py`; a later disjoint source
assignment selects `production_controls.py` and `select_production_controls.py`.
The binder is now frozen
after its separately adopted inert controls. Canonical root is
`E:\Distributed Trustworthy Mathematical Knowledge Network`; the guard passed.

## Source and status

Initial reviewed-source candidate SHA-256:
`d5a9c13392e2de8b170cbaf4a9a27e4d1e5d99eb2714165848a640069fe42fce`.
Independent changed-source review has been requested. No Python import, syntax
execution, test, native build, owner/database access, network operation, package
adoption or Git mutation was performed. This checkpoint is not a runtime pass.

The preceding source/theory contract `c21182e9...` received an independent
no-blocking-issue assessment for intake and its producer seam. That review does
not review this new implementation. The closure exporter performs structural
extraction/correspondence checks, not receiver-side mathematical admission.

## Public pure API

| API | Result and boundary |
|---|---|
| `Limits(...)` | Frozen caller-lowered ceilings from the root selection; larger or noninteger values refuse. |
| `read_manifest(raw, expected_sha256, *, limits, check_budget)` | Exact canonical schema/hash/semantics, unique bounded entries and derived filenames; returns `Manifest`. Reads no files. |
| `validate_batch(entries, raw_units, *, limits, check_budget)` | Exact raw length/hash/UnitID and supported semantics, full portable unit parsing, structural and native-array bounds; returns `BatchCensus`. No dependency warrant. |
| `split_units(raw_units, *, limits, check_budget)` | Greedy whole-unit partition preserving input order; finite global limits and duplicate UnitID checks. Dependency ordering is a separate preflight obligation for generic inputs. |
| `make_manifest(batches, *, limits, check_budget)` | Preserves chosen batch boundaries, validates each input and cumulative limits, emits and revalidates canonical manifest. |
| `bind_writer(writer_raw, inventory_raw, expected_targets, *, limits, check_budget)` | Exact fixed-seed writer binding and automatic batch/manifest construction, returning `BoundBundle`. No catalog context or local acceptance. |

`Entry` contains `unit_id`, `raw_sha256`, `raw_bytes`; its `relative_path` is
derived only as `units/<hex-unit-id>.json`. `Manifest` contains its exact raw
bytes/hash, semantic ID, tuple of tuple entries, unit count and evidence bytes.
`BoundBundle` contains the manifest, corresponding tuple of raw-byte batches,
exact target records and cumulative census. `Target.name` is immutable canonical
structured-name bytes, not a dotted-name approximation; its other fields are
`export_id` and `unit_id`. Both bundle and manifest explicitly report
`mathematical_acceptance = False`.

The fields agreed with root are `Limits.max_manifest_bytes`, `max_units`,
`max_batches`, `max_bytes`, `max_nodes`, `max_names`, `max_edges`, and
`max_binding_bytes`; additional fields cover individual writer/evidence,
target-count, existing batch and native-array ceilings. `BatchCensus` fields
are `units`, `bytes`, `nodes`, `names`, `edges`, `binding_bytes`, and
`native_array_bytes`.

`binding_bytes` is the exact canonical array size of all `[name, export_id]`
rows in the measured inputs, including brackets/commas. It is conservative for
a receiver that already warrants some of those outputs. `native_array_bytes`
is the exact size of the unit-array serialization, not an estimate from portable
envelope bytes. Aggregating either count across batches must remove the repeated
outer brackets and add the appropriate separating commas; root's intake owns
the whole-operation projection and resource decisions.

## Fixed seed binding, not a manufactured protected root

The module reuses `ordinary_evidence`'s codecs/censuses and canonical encoding,
`portable_evidence`'s actual V2 reader and `ordinary_semantics`' V2 identities.
It does not use old V1 profile-bound identity formulas. It imports only pure
support modules, including the bounded Lean-writer parser from
`portable_candidate`; it never invokes that module's context-dependent binder
with a fabricated root or arbitrary warrant callback.

The fixed inventory is
`software/assets/foundation/seed-inventory-json.json`, verified read-only at
SHA-256 `c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0`,
equal to `ordinary_semantics.INVENTORY`. This exact Lean-written file need not
be Python's canonical portable JSON. The implementation first verifies its
bounded exact bytes and pin, then uses the bounded writer grammar; imposing
portable canonical ordering here would incorrectly reject supported inputs.

It verifies the exact 581-name fixed basis, exact expected nonbasis targets,
writer fields/assurance/statistics, and every whole unit. Imports must resolve
only to fixed basis identities or preceding emitted outputs. New output names
cannot collide with the basis or earlier/current outputs. Target declarations
must actually be emitted. All portable envelopes are reparsed with the current
reader. Hashing and successful binding remain only claim construction; each
receiver still checks its missing units over a real warranted parent.

The native author and this author agreed the producer request keys:
`schema = DMKN_ORDINARY_BASELINE_EXPORT_REQUEST_V1`, `project_search_paths`,
`modules`, `targets`. Native output retains the existing six-field
`DMKN_ORDINARY_EXPORT_BUNDLE_V1` writer wrapper and five statistics. Source
traversal `scan_nodes` is not the encoded-node census; both are separately
bounded. The native request/approval and actual artifact loading are outside
this pure module.

## Remaining integration and verification

Root owns exact file access/spool safety, whole-bundle planning-only dependency
preflight, protected context selection, conservative custody/catalog capacity,
aggregate invocation grants, actual admission and unknown-outcome reporting.
`validate_batch` does not authenticate a root, check global dependency order,
establish availability or reserve quota. Successful manifest parsing does not
prove that its files exist or that a batch is mathematically valid.

The binder materializes a finite writer and output evidence set. It is not a
streaming exporter or a constant-memory claim; parsed Lean/JSON objects may
require much more memory than the byte ceilings. Near-limit native units and
writer bundles can exceed portable envelope limits and correctly refuse.
Native/whole-controller resource envelopes remain necessary before execution.

The separate A2 contract still must bind a selected immutable local artifact
graph and prove its relevant private/public correspondence to the independently
warranted baseline. This module does not preserve frontend metadata or turn an
approved project into a mathematical premise. A final usable ordinary workflow,
not an isolated bundle parser pass, remains the integration objective.

Root's fresh control author received API and exact inventory guidance plus
existing synthetic syntax helpers in `portable_candidate_checks.py` and
`semantic_identity_checks.py`. Such fixtures test syntax/identity/order, not
Lean correctness or durable state. Source review precedes any selected controls.

## Producer-controller continuation: source only

The root selection now additionally authorizes the finite producer controller
and its fixed-role worker. No producer/controller import, syntax run, test, native
build, owner/database access, runtime operation, package adoption or Git mutation
was performed by this assignment. The earlier binder controls were separately
selected and adopted by root; their pass does not qualify this fresh controller.

| Fresh source | SHA-256 |
|---|---|
| `software/v5/ordinary_baseline/baseline_production.py` | `0f64bddaa3e106dd8abfe2790158fd94bdf85c6af26e945e04ebbed5f5f72e7d` |
| `software/v5/ordinary_baseline/baseline_worker.py` | `c44d14ec5ddcde8be0952eb7fcd4388b48eae79f44c79fdef187467ee9ca2917` |

The native partner's source-only `BaselineExporter.lean` remains at
`403f1f4369cd73ea905265f3df42d52f70c68cb5d4f24c03b696dd65f2fc629e`;
the binder remains at `d5a9c13392e2de8b170cbaf4a9a27e4d1e5d99eb2714165848a640069fe42fce`.
Independent changed-source review was requested for the controller and worker.
Neither source hashes nor that future review imply an actual exporter build.

### Accepted controller API and authority boundary

`produce_bundle(installation, profile, *, project_selection_raw,
project_selection_sha256, targets, output_directory, budget,
limits=DEFAULT_LIMITS)` accepts an already verified `NativeInstallation`, an
`AuthoringProfile` bound to that installation manifest, one fresh finite
`OperationBudget`, and the existing approved-project descriptor grammar.
It claims the budget once, before the operation, and never opens a mathematical
owner or catalog. It uses the current runtime, exact fixed inventory, real Job
supervisor and pure V2 binder; there is no new execution or acceptance policy.

The project descriptor authenticates selected roots/modules, **not** their
transitive artifact contents. This is approved-local extraction, not hostile
artifact loading, artifact-closure registration or mathematical admission.
Post-run directory checks do not silently strengthen that premise into immutable
artifact correspondence. The separate A2 closure and realization work must
provide that relation before ordinary-library reference reuse can be adopted.

The worker fixes the native role relative to its installed source as
`../bin/BaselineExporter.exe`. The controller fixes the worker as adjacent
`baseline_worker.py`; callers and peer records cannot select another executable.
The worker runs under the same enclosing Job, with isolated/no-site/no-bytecode,
nonoptimized Windows Python, empty stdin and inherited bounded diagnostics.
It sanitizes language environment variables and supplies the selected Lean
runtime's `bin` as `PATH` so native runtime loading does not inherit the
supervisor's unrelated release-relative path. It creates no second Job or grant.

### Required future installed support map

A future package must install the controller, binder, approved-project extractor
and worker together in its `py` directory, plus the reviewed compiled exporter
in `bin/BaselineExporter.exe`. The controller requires exact profile pins for
itself, the worker/executable, and its loaded binder/extractor support modules:
`baseline_bundle`, `library_extraction`, and the latter's `G`, `B`, `L`, `R`,
`X` imports. The existing installation/profile mechanisms remain responsible for
their ordinary admission/contribution, codecs, runtime and remaining dependency
pins; the controller also checks shared core-module identity and installation
manifest equality. Do not add only the two new Python files to an otherwise
incomplete profile and call that an authenticated producer.

Executable and worker are bounded at 32 MiB and 1 MiB respectively. Inventory
and exact request are <=1 MiB; targets are unique nonbasis structured names and
bounded by the selected binder limits. Package/install/runtime/helper/project
directories and the fresh output directory must be pairwise separated across
the output boundary. The controller pins and reads back exact request, inventory
and project-selection copies before/after native use, then re-verifies its
profile and fixed inventory before manifest publication.

### One allocation and honest spool/accounting semantics

Production uses a **distinct fresh** `OperationBudget`, not intake's grant. For
this API its `output_bytes` authorizes the total retained producer spool. The
required initial reservation is

`64 MiB + max_evidence_bytes + max_manifest_bytes + 12 MiB + 2*log_bytes`.

The independent reviewer found that the initial `ab23c20c...` controller used
caller-lowered `max_writer_bytes` in this reservation, although native/worker
still permits a fixed 64-MiB writer before the controller can refuse it. Root
selected the narrow correction above before any use: reserve the actual fixed
native writer ceiling. A lowered binder writer limit remains an acceptance/refusal
limit only; it does not reduce native output authorization. No worker/native
interface change or extra allocation is introduced.

With full default binder ceilings this exceeds the ordinary 64-MiB default
operation output allowance, so that default deliberately refuses before native
execution. A later selected caller may authorize a sufficient finite value;
the implementation never silently increases it. The allowance must also fit any
outer operation's original budget. This reservation covers the writer, portable
units, manifest, bounded metadata and diagnostics; it is not a claim that actual
output always fills those maxima.

The native call obtains its one allowance from the original deadline, preserving
existing cleanup reserves. Only finite nonnegative final Job CPU observations
are accepted; absent/invalid accounting charges the complete native CPU grant
to `budget.worker_cpu` and stops. An exception in supervision cannot turn work
into a zero-cost attempt. Clean closure requires the actual supervisor result,
reaped child, closed Job, no cleanup errors, zero active processes and the
existing clean-worker predicate. Empty native stdout and bounded stderr are
required; diagnostic phases are emitted on stderr.

Exact bounded file censuses before and after the manifest establish what exists
at those observations. They are **not a hard during-execution disk quota**.
Controller CPU and wall checks are cooperative; any future public operation
requires its selected outer containment and storage lifecycle. Native Job
containment and final file measurements must not be described as a hostile-input
sandbox or an enforced whole-controller disk quota.

### Manifest-last output and failure preservation

Successful output consists of `project-selection.json`, `inventory.json`,
`request.json`, `SELECTION.json`, `writer.json`, `supervision-result.json`,
`supervision/{command.json,stdout.txt,stderr.txt}`, derived `units/<id>.json`,
`PRODUCTION.json`, and `manifest.json`. Every derived unit is written fresh and
read back against exact size/hash. The manifest is written/read back **last among
required bundle payloads**, after bounded census and the final input checks.

The saved `PRODUCTION.json` deliberately says
`PREPARED_FOR_MANIFEST_WRITE_NOT_COMPLETION`. Only a successful live function
return says `PRODUCED_INERT_BASELINE_NOT_ACCEPTED`, with the final spool census,
manifest locator and exact identity. Neither a saved report nor the existence of
a manifest can replay an earlier completion, establish local acceptance, open an
owner or automatically initiate intake.

Failure retains all partial output and raises `ProductionError` with bounded
failure facts. A bounded diagnostic `FAILURE.json` may follow a failed/uncertain
manifest attempt; its report explicitly records `manifest_may_exist`. No rollback,
deletion or retry is inferred. Unknown native closure/accounting stops; a later
attempt requires a new explicit selection and fresh output. The caller remains
responsible for complete and partial spool retention.

### Next decision, not automatic execution

Root owns independent-review adoption, installed profile/worker maps, native
build selection and the finite changed-boundary controls. The useful objective
remains one integrated strict baseline intake, exact immutable ordinary-library
correspondence and substantive small delta use. Do not repeat the retained large
batching campaign or treat this producer's source completion as deployable v5.

## Focused producer controls: authored, not run

Root selected two fresh control sources after reading the producer/worker. They
reuse the frozen installed package, retained three-unit evidence syntax and the
existing finite selector/Job harness, without repeating the 24 binder/intake
controls. This assignment has not imported, compiled, selected, launched or
executed either new file.

| Fresh source | SHA-256 |
|---|---|
| `software/v5/ordinary_baseline/production_controls.py` | `1f46b82621c9fd6e9dd8000b8ae7eb92f815191f30fca4e17064bccbe32008a2` |
| `software/v5/ordinary_baseline/select_production_controls.py` | `2ea48937ce7949daf6900cbbf36bbeefdb475b246dd1c450777ab171f35f9e4c` |

The harness uses real controller/binder/codec/project-grammar/budget code, real
small fresh files and real `AuthoringProfile.verify` over an explicitly synthetic
source-location/support map. The executable role is inert nonexecutable fixture
bytes, not a built exporter. Native execution is replaced by one instrumented
supervisor double returning retained writer syntax; no claim is made that the
native exporter, worker, Lean, installation or mathematics executed. Native CPU
values and grants observed in the controls are explicitly simulated, separate
from actual future outer harness accounting.

The ten selected source cases are:

- Default undersized spool refuses without output/native entry.
- Lowered binder-writer limits still reserve the fixed native ceiling.
- Missing fixed executable role refuses before native entry.
- A bad worker pin fails real profile verification before native entry.
- One inert native response produces exact retained portable bytes and a
  manifest written after required payloads; saved preparation is not completion.
- Unknown native CPU retains the complete grant and stops.
- A supervision exception likewise preserves the complete grant and partial files.
- Unclean native termination refuses before attempting to read its absent writer.
- A clean return without a writer does not produce a bundle.
- An injected late manifest uncertainty leaves manifest/evidence intact, records
  `manifest_may_exist`, and does not convert saved preparation into success.

The harness intercepts forbidden owner/catalog/database/subprocess/network calls.
It does not bypass the actual controller role/pin, file, binder or resource checks.
Only module locations, the deliberately small profile/artifact fixture and the
native supervisor result are synthetic. No runtime worker behavior or real native
export is qualified by these cases.

The selector pins current controller, worker, binder and harness plus its own
source/standard runner; inherits only frozen package/runtime inputs, not any
prior state or allowance; and prepares a fresh named 60-wall-second,
35-CPU-second, 768-MiB, two-process control selection. It does not launch it.
Independent source review and root's separate runtime decision remain required;
no control pass is asserted here.
