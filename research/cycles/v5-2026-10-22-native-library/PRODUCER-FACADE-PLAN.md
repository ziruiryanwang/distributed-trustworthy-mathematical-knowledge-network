# Minimal owner-free producer facade in the consolidated package

2026-10-24. Source-only proposal by `package_continuation`, requested by root.
No implementation, native build, experiment, owner open or live-state change.
The concurrently selected reference continuation was not polled or touched.
Read with GROWTH-NEXT-PAYOFF and the separately owned candidate-offer contract.

**Later source-only reassessment, 2026-10-24:** the final section below supersedes
the additive component-manifest recommendation. Root explicitly asked not to
engineer compatibility merely to preserve the current retained-reference fixture.
The cheaper coherent future packaging is a normal new consolidated package
version with one profile; no implementation or runtime is selected by this note.

## Decision supported by existing source

Expose the existing `baseline_production.produce_bundle` as an ordinary installed
command. Its caller needs an installed checker/exporter profile, an explicitly
approved **already compiled local project**, target names and a finite output
allowance. It does not need a mathematical owner, basis initialization, local
intake, original-reference registration or a cryptographic certificate.

This removes a mandatory producer workflow, not receiver verification. Exported
bytes are inert candidates. The existing accepted `publish` command keeps its
meaning; offering candidates is a separate optional operation. Repositories,
file transfer and existing peer custody can all carry the same exact bundle.
Do not invent another exporter, binder, theorem schema or producer product fork.

## Current consolidated predecessor and exact reusable native artifact

At this inspection the immutable installed predecessor is
`experiments/v5-local-checks/ordinary-reference-assembly-02/package`:

| Item | SHA-256 |
|---|---|
| PROFILE | `1054b9a339503f919ac8f0bd78078c5287a16481cfe6f627b49919b45469aa10` |
| ASSEMBLY | `537b88521344f659c0a439847e8c39f9790b88d9ee0df14e43ae98976821d85f` |
| Installation manifest | `32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2` |

Root reports the live continuation subsequently stopped after successful
registration at author A's long-path failure. That outcome is not audited here.
A later selected authoring-only successor should be the single consolidated base
for this facade, not a competing sibling product. Its exact package pin must be
recorded when selected; this note does not guess a future hash.

The retained binary is
`experiments/v5-local-checks/ordinary-baseline-native-build-04/build/objects/BaselineExporter.exe`:
**809,472 bytes**, SHA-256
`2adcffad1ad4967f093e1acc6c31295c2519e7f9cbf35d04bee37d8580cc3c4f`.
The retained BUILD document's output pin agrees. Its link inputs are
OriginalExpr, OriginalDecl, CheckedExtension, BootstrapSupport, OrdinaryExport
and BaselineExporter object files. No new compiler or link step is necessary.

Existing sources to retain/reuse:

| Source | SHA-256 |
|---|---|
| `ordinary_baseline/baseline_production.py` | `0f64bddaa3e106dd8abfe2790158fd94bdf85c6af26e945e04ebbed5f5f72e7d` |
| `ordinary_baseline/baseline_worker.py` | `c44d14ec5ddcde8be0952eb7fcd4388b48eae79f44c79fdef187467ee9ca2917` |
| `ordinary_baseline/BaselineExporter.lean` | `403f1f4369cd73ea905265f3df42d52f70c68cb5d4f24c03b696dd65f2fc629e` |

Source paths in this table are below `software/v5`. The existing binder is already
installed as `reference/baseline_bundle.py`; the actual ordinary exporter support
and project selector are under `authoring/py`. Reuse those loaded modules, not
second copies with the same Python import names.

## Important package-upgrade issue: do not invalidate checked references

The ordinary reference support descriptor hashes the *source file* `profile.py`
and `owner.py`, plus its selected registration/checking roles. Adding producer
files to the current PROFILE payload set would require changing `profile.py`'s
exact allowlist. That changes support ID and makes existing reference records
unusable under the new support, even though the native checking relation did not
change. Do not silently relabel those records or overlook this cost.

Recommended smallest compatibility-preserving layout: an **additive producer
component within the same package**, with a small independently pinned component
manifest. Keep the existing main PROFILE, `profile.py`, owner and all existing
payload bytes exact. The main loader's directory census does not search a new
`producer/` directory, and the directory is not on its import paths. A producer
entrypoint must explicitly validate its own component, not rely on that exclusion
as authentication.

Proposed mapping (source names are proposals, not selected edits):

| Installed role | Implementation/reuse |
|---|---|
| `producer/producer.py` | Small new CLI/bootstrap; explicit approved-project export, no owner arguments |
| `producer/PRODUCER.json` | Exact producer payload map and exact underlying main PROFILE digest |
| `producer/py/baseline_production.py` | Narrow fresh source successor of the existing controller for split-layout pin checks only |
| `producer/py/baseline_worker.py` | Byte-exact existing worker |
| `producer/bin/BaselineExporter.exe` | Exact retained 809,472-byte executable above |

The component manifest should identify exact roles and allowed relative paths,
bound sizes and list the retained native provenance. It is an artifact-selection
manifest, not a mathematical certificate or publisher authentication. The same
top-level assembly receipt must inventory both core and producer component so
users receive one package. Historical immutable installation snapshots remain
evidence, not separately evolving product lines.

The CLI first authenticates its own selected component and the nested core
PROFILE; then it reuses the current core package bootstrap/loader without opening
any owner. It constructs a `G.AuthoringProfile` from the existing verified profile
plus the component pins, with identical installation ID, existing helper paths
and existing author-worker field. The verifier already accepts a bounded tuple
of up to 4,096 unique pins; no class/schema change is needed. Load the producer
controller by exact verified filename, avoiding a new unbounded import path.

One unavoidable narrow source adaptation: `_selected_support` currently insists
both `baseline_bundle` and `library_extraction` share the producer controller's
directory. The consolidated package already splits those modules. Replace that
obsolete colocation premise with **explicit already-verified role paths**, while
keeping all shared-module identities, pin membership, worker basename and native
executable pin checks. The worker's existing relative layout naturally resolves
from `producer/py/baseline_worker.py` to `producer/bin/BaselineExporter.exe`, so the
worker and native program can remain byte-identical. Do not monkey-patch module
`__file__`, introduce duplicate binders, or change semantic/witness identities.

## Public command semantics and cost boundary

The prospective export CLI selects the producer-component digest, runtime roots,
project-selection file/digest, structured target-name file, fresh output directory
and a finite wall/CPU/memory/spool budget. It must reject catalog, parent-root and
reference arguments rather than invent dummy values. Actual `produce_bundle`
returns `PRODUCED_INERT_BASELINE_NOT_ACCEPTED`, manifest identity, target IDs,
cost/accounting observations and `mathematical_acceptance: false`.

Retain the existing manifest-last semantics. `PRODUCTION.json` deliberately says
PREPARED, not a reusable success token; a later failure can coexist with a complete
manifest. An independent offer operation validates the actual exact manifest and
unit bytes and never adopts saved success metadata.

Do not reuse `owner.Allowance.operation` unchanged: it supplies 64 MiB output,
which is below `produce_bundle`'s required spool. The exact existing formula is

    64 MiB native writer + limits.max_bytes + limits.max_manifest_bytes
    + 12 MiB metadata/control reserve + 2 * log_bytes.

With default bundle bounds that is 142 MiB plus both logs. It is a cooperative
spool reservation, not a hard disk quota or expected output size. Create the one
remaining `OperationBudget` before production; include startup/profile validation
in the CLI's original envelope and charge the actual inclusive native Job CPU
once. Unknown accounting retains its reservation. No per-phase budget renewal.

## Optional candidate offering stays separate

The growth agent's source contract reuses `OrdinaryStore.put_evidence`,
`put_preview`, `portable_preview.preview_from_evidence/resolve`, and
`discovery_store.Store.admit` with OrdinaryExportAdapter. These operations already
describe/store inert exact bytes; they do not need a producer warrant.

Preserve accepted `peer_api.publish` and its exact local-context binding check.
Add an explicitly named candidate offering operation rather than quietly weaken
publish. For the first bounded provider facade, reuse the existing configured
owner lock to serialize provider custody/index access; it need not admit the
offered mathematics. This does not require each contributor to initialize an
owner: contribution/export and provider hosting are different roles.

The provider must validate actual manifest/units/targets and account for complete
selected dependencies before indexing target previews. Candidate admission,
privacy, byte quotas and failed writes remain explicit. Existing partial commits
must be reported; do not imply an atomic multi-target transaction. An index may
choose stricter local quality policies. All candidates still reach the receiver's
unchanged independent admission boundary, never its warranted context directly.

## Compatibility and assurance limits that must be visible

- This is the pinned Windows / Python 3.14 / Lean 4.34.0 route. Other toolchains
  need separately supported adapters; arbitrary `.olean` version portability is
  not established.
- The local project is explicitly approved compiled input. The path/module
  selection does not pin every transitive compiled artifact. Empty plugin list
  and `loadExts := false` are not a hostile-artifact sandbox.
- The native producer imports the private environment and eagerly indexes its
  source before selecting the target closure. Cost depends on that local imported
  environment and emitted proof closure, not just target type size. This facade
  is not a universal low-cost/streaming export or a whole-world scalability proof.
- The fixed 581-name foundation, supported declaration grammar, axiom/unsafe
  policy and whole-unit rules remain. An arbitrary Lean project may be refused;
  the facade must not call that mathematical falsity.
- Default baseline ceilings allow 8,192 units/64 MiB, while current public peer
  receive has a 1,024-unit selected-closure ceiling. Do not label every produced
  bundle one-call peer-admissible. File transfer/intake and peer receive are
  distinct supported routes; no silent cap enlargement is proposed.
- Existing ten producer-controller controls used a native double. Retained
  native workflow evidence exercised the exporter separately. Neither proves
  the prospective installed facade has run. A later test should cover only the
  newly integrated public invocation/offer seam, not rebuild/reprove the fixture.

The theoretical benefit is the removed mandatory producer-adoption cost from
GROWTH-NEXT-PAYOFF, conditional on extraction, hosting and screening costs. This
source plan does not measure demand, growth rate or superiority over ordinary
searchable packages. If normal packages gain the same adapter, that is a useful
contribution rather than a failure to invent a proprietary protocol advantage.

## Root's concurrent authoring-repair question

Separately confirmed from source: a sole `reference/reference_authoring.py`
overlay changes PROFILE's descriptor but not the current reference support ID,
because that controller is outside `support_descriptor`'s selected roles. The
controller still verifies its own exact loaded source, worker, exporter and
environment through the full profile before loading the reference. If owner,
`profile.py`, registration/store, native helpers and the other hashed roles remain
exact, the already registered reference can be reused without another live match.
This supports a later five-call A/delta/B/refusal/status continuation if root
selects it; it is not an implementation or runtime selection by this note.

## Revised minimum: one package, ordinary export, file-first distribution

This is the requested source-only reevaluation after root prioritized growth
architecture over preserving fixture compatibility. No new harness, package,
component manifest, native build or live operation was created. Existing
registration and continuation states were not opened or polled.

### What is actually callable now

`ordinary_baseline/baseline_production.py:142` exposes the Python function
`produce_bundle(installation, profile, *, project_selection_raw,
project_selection_sha256, targets, output_directory, budget, limits=...)`.
It is **not a command-line program**: there is no argument parser or main entry.
`baseline_worker.py` is a fixed subordinate launcher, not the public producer.
The native workflow harness is experimental orchestration, not an installed
owner-free interface. Do not document any of them as an already usable public
producer command.

The consolidated public command is presently `owner.py` (source successor
`ordinary_reference_package/owner02.py`). Its `extract-project` operation is not
an owner-free substitute: every operation currently requires catalog, custody,
store ID and custody limits; extraction additionally requires a parent root and
a retained failed/incomplete contribution with pinned request/candidate bytes.
The dispatcher opens `OrdinaryAdmission` before extraction. That workflow solves
missing imports for existing owner work, not first-time contributor publication.

The public **receiver** already has `owner.py intake-baseline` with exact
`--bundle-directory`, `--bundle-manifest` and `--bundle-manifest-sha256`, selected
parent root and ordinary local owner settings. It calls the real independent
`baseline_intake.intake`. File transfer of an already existing supported bundle
therefore needs no new mathematical protocol or producer acceptance service.

### Cheapest coherent installed producer, if selected

Use the next single consolidated package/profile and add one operation, tentatively
`owner.py produce-baseline`. The owner filename is historical; this operation
must branch before all catalog/custody/store validation or opening. Separate its
allowed/required arguments by operation, rather than making callers provide dummy
owner arguments. Reuse the current exact bootstrap and parent allowance accounting.
Do not create another entrypoint with copied bootstrap or another import namespace.

The smallest layout adjustment is:

| Existing package location | Addition/change |
|---|---|
| `owner.py` | One owner-free dispatch branch, operation-specific arguments and original-envelope accounting |
| `profile.py` / `PROFILE.json` | Add the three selected producer payloads to the existing role map/census; expose the loaded controller |
| `authoring/py/baseline_production.py` | Selected fresh controller successor; only explicit split-layout role checks need adaptation |
| `authoring/py/baseline_worker.py` | Exact retained worker bytes |
| `authoring/bin/BaselineExporter.exe` | Exact retained native executable bytes |

This layout deliberately satisfies the existing worker's
`source.parent.parent / "bin/BaselineExporter.exe"` rule. The existing extraction
module is already colocated with the controller under `authoring/py`; only the
bundle binder remains under `reference/`. Replace its old blanket colocation
requirement with the exact selected `reference/baseline_bundle.py` role, while
retaining loaded-module identity, pin membership and executable/worker checks.
The binder is not copied. No new native build, mathematical schema, verifier,
lock domain or component-manifest protocol is necessary.

The branch takes approved compiled-project selection/hash, nonempty structured
target names, a fresh output directory and an explicit finite spool allowance.
It returns the existing inert-result structure. It constructs one fresh
`OperationBudget` from the **remaining original** wall/CPU envelope and sufficient
explicit output reservation; merely calling the current 64 MiB
`Allowance.operation` would fail the producer's 142 MiB-plus-logs minimum.
CPU accounting must charge the actual native job once, including failed calls;
unknown accounting retains the reserved amount. Controller hard containment is
not implied by cooperative checks or native-child containment.

Adding roles and changing owner/profile source changes the current reference
support identity. **Accept that as an explicit new version boundary for now.**
Keep the previous selected installation and its existing reference records intact;
do not relabel them, alter `support_descriptor` to force compatibility, migrate
private state, or replay registration solely to keep a demonstration fixture warm.
The producer route needs no reference record, so this version boundary is not an
obstacle to its first useful deployment. A general support-version migration
policy is future product work, not the justification for a component system now.

Relative complexity: three existing artifacts are reused; the genuinely new code
is dispatch/argument/budget glue and one layout-binding change. Source controls
should cover the missing owner arguments, rejected irrelevant arguments, role
substitution, output reservation and original accounting. Only a later selected
public-invocation test needs native execution; the passed native build, bundle
format and receiver campaigns do not need repetition.

### Does file-bundle re-offering suffice?

**For the immediate low-friction sharing capability, yes.** An existing complete
bundle can be copied to another local folder, Git repository or ordinary file
host, preserving its exact manifest and entry-derived unit files. The receiving
agent can select it and invoke the existing intake command. The original producer
need not run another exporter, open an owner, hold warrants, issue a certificate
or remain online. No new offer command is needed merely to copy inert bytes.
Provider authorization, retention and actual receiver costs remain necessary.

**For unknown-ID formal discovery through the commons, no.** A file manifest is
not a searchable formal index, does not prove selected dependency supply by itself,
and does not advertise target previews. Existing accepted `peer_api.publish`
requires exact target bindings in the provider's warranted context; leave that
meaning unchanged. A provider that wishes to advertise unaccepted candidates
still needs the narrow candidate-ingest glue in CANDIDATE-OFFER-CONTRACT:
bounded actual manifest/unit/target validation; evidence-first custody; exact
derived previews; existing discovery admission; explicit partial commits and
unchanged receiver checking. Reuse the provider's existing owner lock for current
store serialization without requiring it to accept the advertised mathematics.
Do not turn this into a new public remote-write endpoint or a mandatory service.

Thus file re-offering is an existing transport/fallback, not a final discovery or
growth result. It can defer provider-ingest implementation until root selects a
growth mechanism requiring unknown-ID acquisition. Conversely, if candidate
search is the next real workflow, adding only the exporter would leave its central
gap open; do not count easier export as demonstrated uptake or useful growth.

### Marginal-payoff decision

Let `A` be otherwise unnecessary producer adoption cost, `X` the already-required
approved export cost, `H` hosting/screening cost, and `R_i` each actual consumer's
discovery/check/reuse cost. Owner-free export removes `A`; it does not remove
`X`, `H` or any `R_i`. Existing bundle re-offering removes a repeated `X` as well.
These are conditional avoided costs, not measured demand or an intrinsic advantage
over equally equipped ordinary packages. A producer who already has warrants may
save no adoption work. A large cold closure can still make the route unhelpful.

Before selecting either glue change, root should settle the growth proposition:
who has useful existing mathematics, who benefits from discovering/reusing it,
which acquisition/search/certification costs block that use, and which existing
file/package route supplies the same benefit. Software need not invent a unique
network advantage to be useful, but another adapter alone does not establish
growth. The recommendation is therefore **one normal package version if needed,
file-first reuse now, candidate discovery only when its payoff is selected**;
not compatibility engineering, parallel product forks or another fixture campaign.

## Independent source audit of the selected producer successors

2026-10-24, `package_continuation`, independently assigned by root after the
source-only implementation selection in GROWTH-FIRST-ARCHITECTURE-DECISION.
Disposition: **SOURCE-CLEAR at the exact hashes below**, not installed/runtime
qualification, mathematical acceptance, growth evidence or final-v5 acceptance.
No package, native process, product import, state operation or Git mutation was
performed for this audit. Used full source diffs against the stated predecessors,
read the changed boundaries and underlying controller accounting, and independently
rehashed the selected files.

| Source under `software/v5/ordinary_producer_package` | SHA-256 |
|---|---|
| `owner.py` | `5fab16429ab457ff45e1afd0d7a437d48a62c672441c6db3e67adbb420c1b6ef` |
| `profile.py` | `b5a6430061b0ab6e19f35d0250165a62690663a66f1f70b95a0fa2543b2d65a4` |
| `baseline_production.py` | `4e52450af203027212205f292e5965b94febe7e6b58f12a7b87e052444662926` |
| `README.md` | `8904e3e83c0d93880f488c4df0a003b0e499389cdf4bc4915d10b466ca8d4b45` |

Predecessors are `ordinary_reference_package/owner02.py`, its `profile.py`, and
`ordinary_baseline/baseline_production.py`. The new directory is a source staging
location for one later consolidated package revision, not a separately delivered
product or permission to edit an existing installation.

### Finding corrected before clearance

The initial controller adaptation correctly located the worker/executable under
`authoring/`, but still returned that subdirectory as the protected package root.
`produce_bundle` uses this returned path for output-overlap checks. Consequently,
an output below consolidated `reference/` could mutate authenticated package
contents before failing its final exact census. The author corrected the return
value to the **whole consolidated root**, while retaining `authoring/` solely
for worker/executable resolution. The final controller hash above includes this
correction. Later focused controls should include rejection of output under
`reference/` as well as under `authoring/`; no execution of such a control occurred
in this source audit.

### Argument, ownership and role boundaries

`run` dispatches `produce-baseline` before owner/custody argument validation or
opening. The producer has no owner/catalog/custody call and rejects all unrelated
arguments, including explicit status pagination flags even at their customary
values. It requires an affirmative local compiled-project approval, exact project
selection/hash, targets, fresh output and explicit 144..256 MiB spool allowance.
It neither fabricates an accepted context nor interprets execution approval as
mathematical trust. For old operations, the parser restores the previous status
defaults; the dispatcher still requires all four prior state arguments and now
rejects producer-only flags. Their operational bodies remain unchanged by diff.

The one profile adds the controller, exact worker and retained executable to its
existing map and census. All selected payloads are checked before package imports;
the controller is also checked at its exact `authoring/py` location. Shared module
identity checks remain, and the only allowed binder location is
`reference/baseline_bundle.py`; mere pin-set membership of an alternate binder is
insufficient. The exact worker still resolves the executable at
`authoring/bin/BaselineExporter.exe`. No additional binder, worker namespace,
native build or executable supplied by a peer is introduced.

### Accounting and result boundaries

The parent allowance begins before support loading. The new branch derives one
fresh operation budget from its remaining wall/CPU resources, with the explicit
spool allowance; the shared `operation` default remains 64 MiB for old operations.
The producer controller itself still reserves the fixed native writer plus
evidence/manifest/metadata/log bounds and does not claim that this bounds RAM.

An inner `finally` charges `budget.worker_cpu` to the parent exactly once on
success or failure, followed on success by the original parent allowance check.
The unchanged controller supplies measured inclusive native CPU when known and
retains the entire native grant when accounting is unknown. Failed calls retain
the controller's detail; a late parent-limit failure preserves an already returned
production result and its output rather than asserting rollback. Native phase
observations are not an additional charge on top of the same whole native Job.
The new code does not imply hard controller-memory containment or hard disk quotas.

Success is explicitly inert (`mathematical_acceptance: false`) and states that
receiver-relative acquisition fit is not established. Manifest-last behavior,
retained partial outputs and no automatic retry remain unchanged. Exact bundle
sharing still requires real receiver intake; no report or exported manifest can
become a mathematical warrant. The new branch neither exercises nor repairs the
parked reference-authoring/delta import-mode defect.

### Claims and next evidence

The README accurately calls these source-only successors, limits the current
toolchain/policy, discloses private environment import and full selected closure
cost, distinguishes the 8,192-unit producer envelope from the 1,024-missing-unit
peer receive ceiling, and preserves the undecided actual receiver fit. It does
not infer measured demand, exponential growth, hostile-artifact isolation or a
network service from adding an exporter. Owner/profile changes explicitly create
a new reference-support identity; existing records remain with the old selected
installation, with no relabeling or compatibility framework.

No additional architecture mechanism is needed for this selected seam. Before
adopting a later package, use focused changed-boundary controls for producer
argument rejection/no state opening, support-role/output-root substitution,
insufficient spool, failed/unknown native accounting and old-operation argument
defaults; then only the selected public invocation boundary if still useful.
This is a review recommendation, not experiment authority. Existing passed native
build/bundle/receiver evidence should be reused instead of repeated wholesale.

### Focused CLI controls: independent source clearance

Root's `software/v5/ordinary_producer_package/cli_controls.py`, SHA-256
`87edfba8def9ee9af2f1f012884614067e728543b3136df36a6cbd39e6bd4f0e`,
is **SOURCE-CLEAR** for the proposed single native-free control allocation.
Read the complete file and independently rehashed it. No control was executed
by this reviewer, and this paragraph does not record a runtime pass.

The test imports only the source owner entrypoint and stdlib; its production,
profile-loader, file-reading and budget dependencies are explicit doubles. It
checks owner-free parser defaults, rejection of state/reference/source/status
options before support loading, explicit project approval, spool endpoints,
old-operation state requirements, selected project hash, one producer call,
remaining original allowance, exactly-once successful/failed CPU charges and
preservation of a result on late parent exhaustion. Missing state APIs in the
successful double make accidental owner opening fail that tested path.

The changed resolver is extracted from the actual controller AST, not retyped.
With path/module/profile doubles it checks the exact worker/executable selection,
the returned full consolidated root (including its `reference/` sibling), and
rejection of a deliberately misplaced binder even when that alternate path is
pinned. This is a role-resolution/control-flow test, not filesystem hardening or
an actual attempt to write under a package. The unchanged production overlap
predicate supplies that implication in the separately reviewed source.

The final source/profile assertions are honestly described as structural checks,
not execution of the loader or evidence that the retained executable runs. Test
output explicitly limits its claim to parser/dispatch/accounting with doubles;
no installed, native, mathematical or growth qualification follows.

The proposed fresh `ordinary-producer-cli-controls-01` envelope of 30 wall
seconds / 15 CPU seconds / 256 MiB / two active processes is proportionate to
these stdlib-only bounded checks. It needs only the exact source snapshot and
selected Python runtime, not Lean, a mathematical owner, a compiled fixture or
another run of the existing ten producer controls. Root retains the actual
finite selection/launch and outcome-adoption authority.

### Focused CLI controls: independent actual outcome audit

The separately root-selected `ordinary-producer-cli-controls-01` completed once.
Disposition: **PASS for all 18 native-free CLI boundary cases**, not installed
producer, native exporter, mathematical, network or growth qualification.
Read actual RESULT/command/stdout/stderr and independently rehashed all eight
selected runtime/frozen-source entries: zero mismatches. Stdout contains exactly
18 named cases, `case_count: 18`, `native_calls: 0` and `owner_state_opens: 0`, with
the explicit doubles-only scope. Stderr is empty. These counts are consistent
with the previously reviewed test source, not evidence about unseen production
execution.

Evidence under `experiments/v5-local-checks/ordinary-producer-cli-controls-01`:

| File | SHA-256 |
|---|---|
| `RESULT.json` | `35f4a4a83169eb0aedfb55d9ce0f31c7d750691dbee199ea5566f54d7273af1a` |
| `selection.json` | `4e552787fe08be9feca167253fa4e57e6bdde64afca6f2f8c872fcd7ce92f225` |
| `command/stdout.txt` | `8341877371331f944c6a9348c27c79cefa91cb1a73ba9da8b21c228ad635330a` |
| `command/command.json` | `ec9a733047fd24800ba95a61dc643d18c52bf638e0862c3f1221d8f8c8a503c8` |

Actual cost is **0.308025 wall seconds / 0.21875 known CPU seconds**: 0.140625
inclusive Job CPU plus 0.078125 separate runner CPU. Peak Job private commit was
19,841,024 bytes. The selected 30 wall / 15 CPU / 256 MiB / two-process envelope
was not renewed. Child exit was zero, direct child reaped, Job closed, zero active
and zero terminated processes, no cleanup errors or termination request. No
passing control was repeated by this reviewer; only saved evidence was inspected.

### Consolidated assembly and direct public invocation: source review

Read the complete new assembler/selector, independently rehashed both and
reconstructed the six-entry payload map using ordinal JSON key order.
**SOURCE-CLEAR** at these exact identities; no selector or assembler was run by
this reviewer:

| Item | SHA-256 |
|---|---|
| `ordinary_producer_package/assemble.py` | `39b7525a9881099f1c07190ec13d848c6d9b94078fc8ea0d07298b87ab3d741a` |
| `ordinary_producer_package/select_assembly.py` | `0ffad2fb198de5cadf8497b90d9af81916591205621474c184872733f22ca122` |
| Canonical six-payload map | `db1abbaac7ed9c6a338c287bc9212aab5c0f8abd44829bf3751c174e415f5f34` |

The single fresh `ordinary-producer-assembly-01/package` is derived from exact
assembly03 PROFILE `a10e1f3a...` and ASSEMBLY `75f7f7c0...`. It preserves 163
predecessor payloads, overlays only owner/profile, adds the three reviewed producer
roles plus `PRODUCER.md`, and inventories all 169 payloads. Together with
PROFILE/ASSEMBLY this is 171 files. The profile grows from 137 to 140 entries;
the usage document is in the complete assembly map but not an executable role.
The installation manifest/implementation and existing native bytes remain exact;
the new native role is the retained 809,472-byte exporter, not a rebuild.

Before copying, the assembler authenticates bounded predecessor documents, exact
payload census and selected runtimes; compares the reviewed source map; and
rejects overlap. It writes only the fixed fresh output, reads back copied pins,
rechecks inputs/output census, writes the assembly observation and publishes the
profile last. Failures preserve partial output. Source selection snapshots nine
files and pins the retained native artifact and all runtime/predecessor inputs.
The proposed 90 wall / 50 CPU / 512 MiB / two-process envelope contains file-only
work; no package code, native checker, mathematical owner or old fixture state
is opened by the assembler. Actual assembly integrity still needs an outcome
audit before treating its returned profile as selected support.

Root's proposed next installed invocation can use the existing Run-V5-Check
mechanism directly; another harness is unnecessary. Independently read the exact
`selected_targets.json` (`9e790e05aee9d1ba0ae5fc8fb9273afb815803d698da5085e90d54bc1662c722`):
its two structured names are exactly the retained request's `flip` and `flip_low`.
The retained project selection
`bb2753d5999774e4da0530503734633c48dcbc623ce29f5c3cc8a57f60fdfb45`
selects the already compiled `ordinary-baseline-native-workflow-02` local library.
No new fixture compilation is needed.

The proposed call is one explicit approved `produce-baseline` to fresh
`ordinary-producer-public-export-01/bundle`, with no owner/context/registration
arguments, inner 120 wall / 90 CPU / 1536 MiB / explicit 144 MiB spool, enclosed
by 150 wall / 120 CPU / 1792 MiB / six-process supervision. This is source-clear
**in principle**, conditional on a later exact selection pinning the actual whole
assembled package, selected Python/Lean runtime files, five retained compiled
fixture parts and immutable input snapshots. It is not runtime authority or a
prediction of success. Inspect the actual returned public JSON, manifest and
evidence if selected; qualify only the installed glue, not mathematical growth
or a rerun of all native/bundle/receiver assurances. The old reference campaign
and its original inputs remain closed and unchanged.

### Consolidated assembly: independent actual outcome audit

Inspected only after `ordinary-producer-assembly-01/RESULT.json` became terminal.
Disposition: **PASS for the selected file-only assembly**, not installed producer
execution or mathematical acceptance. All 192 selected runtime/frozen-source pins
match; all 169 actual payload sizes and hashes match the assembly map; the exact
package census is 171 files and PROFILE has 140 entries. Independently compared
all 163 declared unchanged payloads directly with actual base03: no mismatch.
The only overlays are owner/profile; additions are controller, worker, retained
exporter and `PRODUCER.md`. Copied payload bytes: 58,829,822.

| Actual evidence under `ordinary-producer-assembly-01` | SHA-256 |
|---|---|
| `RESULT.json` | `3324a99685ffe9ddee6f28ead0c068968b7ed4e72f8f75efb0c5624cd98cd54a` |
| `selection.json` | `27e0a59bb3d62b2c098f7320a1b38ca0b2ec3c4693eac1145b9916560c0a8053` |
| `package/PROFILE.json` | `3e7caee37ebd969212246cdee6bc56f4d5458c417186537de982f4f09b2cd723` |
| `package/ASSEMBLY.json` | `906634eb009ec7c275bef3a00ae295aebf78e3561fa16fadc7b20c632fc3d6cb` |

Actual cost: **6.048236 wall seconds / 2.84375 known CPU seconds**, comprising
2.125 inclusive Job CPU plus 0.71875 separate runner CPU. Peak Job private commit
was 18,681,856 bytes. Child exit zero, direct child reaped, Job closed, two total
processes, zero active/terminated, no cleanup error or requested termination.
No assembly was rerun and no package code or native exporter was executed by
this audit. Existing reference state and failed continuation remain unchanged.

### Direct public selection source authored for independent review

At root's explicit assignment, authored only
`software/v5/ordinary_producer_package/select_public_export.py`, SHA-256
`239e0878562ba895a66b22cfb8821d4fbb73c8cc30bc9e4f1b63bc403d2cf85d`.
AST parsing passed; no selector/product execution occurred. It is with
`demand_producer` for independent source review; this author's note is not its
clearance or runtime permission.

The selector pins the actual terminal assembly above, validates the full package
map/census and installation runtime map, exact retained project/request/targets
and all five existing compiled fixture parts, then writes one fresh bounded
Run-V5-Check selection. It imports only the pinned file-only assembler/builder
helpers, not product modules. The selected command runs installed `owner.py`
directly. Because Run-V5-Check snapshots only `software/v5` sources and itself,
root explicitly chose the retained absolute project-selection path plus runtime
pin; the target file is snapshotted and the producer preserves selected project
bytes in its own output. Five source snapshots and a bounded runtime-pin set are
selected; no new project-selection copy, execution harness, compilation, owner
state, network call or fixture exists.

The proposed inner/outer budgets and fresh bundle destination remain exactly
those reviewed above. Actual public invocation, its result and exact emitted
manifest/evidence remain future separately selected/audited evidence. This does
not reopen the reference campaign or infer useful growth from file assembly.

## Selected source implementation: owner-free public production

2026-10-24. `demand_producer`, under root's source-only selection in
GROWTH-FIRST-ARCHITECTURE-DECISION. No installed package, native build, runtime,
state opening or Git operation was performed. Three Python successors parse by
AST; this is not execution evidence. Fresh sources under
`software/v5/ordinary_producer_package/`:

| File | SHA-256 |
|---|---|
| `owner.py` | `5fab16429ab457ff45e1afd0d7a437d48a62c672441c6db3e67adbb420c1b6ef` |
| `profile.py` | `b5a6430061b0ab6e19f35d0250165a62690663a66f1f70b95a0fa2543b2d65a4` |
| `baseline_production.py` | `4e52450af203027212205f292e5965b94febe7e6b58f12a7b87e052444662926` |
| `README.md` | `8904e3e83c0d93880f488c4df0a003b0e499389cdf4bc4915d10b466ca8d4b45` |

Owner is a successor of reference `owner02.py`; profile is a successor of the
reference profile; controller derives from the already reviewed baseline producer.
The new `produce-baseline` dispatch precedes all mathematical state handling.
`validate_producer_arguments` is pure: no state/context/reference/other-operation
flags are accepted. Required production options are `--project-production`, its
SHA-256, `--approve-local-project`, `--output-names`, `--output`, common adopted
profile/runtimes/budgets, and explicit `--spool-mib` from 144 through 256. Status
parser defaults are restored only for old operations, so even explicitly supplied
default-valued status flags are rejected for production. Old operations still
require their state arguments and reject production arguments.

`Allowance.operation` gains only an optional output-byte parameter, with its old
64 MiB default retained. The producer chooses the explicit spool allowance and
creates one operation from remaining original wall/CPU resources after support
loading. `budget.worker_cpu` is charged exactly once in `finally`, including an
unknown native event's conservative reservation. A subsequent original-allocation
check remains mandatory; a late failure retains the completed inert result if one
exists. Public output explicitly denies mathematical acceptance and makes no
receiver-fit claim. No target identity is put into a warranted context.

Profile adds exactly the producer controller, byte-exact existing worker and
retained exporter executable roles. All payloads are pinned before import; the
one existing binder stays in `reference/`. The controller adaptation requires exact
installed controller, extraction and binder paths plus existing shared-module
identity/pin checks. Independent source review identified that the old returned
`package` path protected only `authoring/`; this was corrected before runtime to
return the complete consolidated root, so output cannot be placed in sibling
authenticated directories. No native exporter, bundle format, producer body or
receiver rule changed.

The short README records file sharing and existing intake, whole-environment/closure
costs, unsupported toolchains, approved-artifact trust and conservative resource
limits. It explicitly preserves the unresolved original-reference import-mode
defect and the new support-version boundary. This implements no hint index,
candidate-ingest service, remote extraction or growth-rate claim. Root owns
independent controls, later package/runtime selection and actual adoption.

## Root finite native-free selection

Root read the complete changed source and independent source/controls clearances.
Select one `ordinary-producer-cli-controls-01` at 30 wall / 15 aggregate CPU
seconds, 256 MiB, two processes. Its five source snapshots are owner/profile/
producer/controls plus the existing outer runner; only the three selected Python
runtime files are attached. No installation, real native exporter, owner state,
library fixture, network or mathematical checking is invoked. Used source freezes
on launch; actual output is separately audited. No repeated producer campaign.

## Actual controls; narrow package source work

The one native-free run returned all 18 selected cases passing, zero native calls
or owner-state openings, clean closure, 0.308025 wall / 0.21875 known CPU seconds.
Independent saved-outcome audit is assigned; this is not an installed/native pass.
The tested owner/profile/controller/controls bytes are frozen.

Select source-only file assembler/selector under the same development directory
for one consolidated successor from actual assembly03. Overlay owner/profile;
add the selected producer controller, exact old worker and exact retained native
exporter; include the short producer usage document in the assembly map if
possible without changing loader semantics. All native installation/checker bytes
and unrelated payloads stay exact. No build, owner opening, registration, fixture
compilation or original-reference repair. Root will select file-only runtime
after independent source and complete payload-map review. A subsequent public
export invocation remains separately selected; do not repeat prior native tests.

## Consolidated file-only assembly: source-ready checkpoint

2026-10-24. Fresh assembler and selector under
`software/v5/ordinary_producer_package/` are source-ready; they have been parsed
as Python ASTs, not executed. No assembly, selector, owner command, native test,
new installation or Git mutation was performed by the author. Root retains
actual selection, launch and adoption. The preceding owner/profile/controller/
README bytes remain frozen after the actual 18-case CLI control run.

| Source | SHA-256 |
|---|---|
| `assemble.py` | `39b7525a9881099f1c07190ec13d848c6d9b94078fc8ea0d07298b87ab3d741a` |
| `select_assembly.py` | `0ffad2fb198de5cadf8497b90d9af81916591205621474c184872733f22ca122` |

The proposed fresh `ordinary-producer-assembly-01/package` is assembled from
retained `ordinary-reference-assembly-03/package`: PROFILE
`a10e1f3ae0e1ac04cfa01240c9c07c3ca2d3da91616a3ca34b1f28b88adadbbc`, ASSEMBLY
`75f7f7c048208b337082c9b0529b02ac4fb6547d143ca178eacb73ba971da202`.
Installation manifest `32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`
and implementation `fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df`
remain unchanged. The existing trusted file-builder helper is pinned to
`49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5`.

Exact changed/added payload map (ordinal keys; nested keys `bytes`, `sha256`):

| Destination | Bytes | SHA-256 |
|---|---:|---|
| `PRODUCER.md` | 5,051 | `8904e3e83c0d93880f488c4df0a003b0e499389cdf4bc4915d10b466ca8d4b45` |
| `authoring/bin/BaselineExporter.exe` | 809,472 | `2adcffad1ad4967f093e1acc6c31295c2519e7f9cbf35d04bee37d8580cc3c4f` |
| `authoring/py/baseline_production.py` | 18,969 | `4e52450af203027212205f292e5965b94febe7e6b58f12a7b87e052444662926` |
| `authoring/py/baseline_worker.py` | 4,831 | `c44d14ec5ddcde8be0952eb7fcd4388b48eae79f44c79fdef187467ee9ca2917` |
| `owner.py` | 44,596 | `5fab16429ab457ff45e1afd0d7a437d48a62c672441c6db3e67adbb420c1b6ef` |
| `profile.py` | 15,031 | `b5a6430061b0ab6e19f35d0250165a62690663a66f1f70b95a0fa2543b2d65a4` |

Canonical ASCII compact sorted JSON of that six-entry map has SHA-256
`db1abbaac7ed9c6a338c287bc9212aab5c0f8abd44829bf3751c174e415f5f34`.
Read-only calculation projects **58,829,822 payload bytes**, versus predecessor
57,985,278; this excludes PROFILE and ASSEMBLY metadata. Expected census is
**169 payloads plus two metadata files = 171 files**: exactly two changed,
four added and 163 unchanged payloads. PROFILE grows from 137 to 140 entries;
the usage document belongs to the complete assembly map, not executable import
roles. The exporter is an exact retained native artifact from
`ordinary-baseline-native-build-04/build/objects/BaselineExporter.exe`, not a rebuild.

There are nine source snapshots: assembler, selector, trusted builder, outer
runner and five textual payload sources. The native exporter remains an explicit
runtime pin. The proposed envelope is one file-only allocation of 90 wall /
50 aggregate CPU seconds, 512 MiB, two processes; the assembler enforces inner
75 wall / 45 CPU seconds. Exact predecessor/file census, reviewed-map validation,
final input/output rehashes and PROFILE-last commit are retained. A new receipt
schema `DMKN_ORDINARY_PRODUCER_ASSEMBLY_V1` records the full payload map and native
source mapping. No compiled module or package product code is imported.

The independent source reviewer has read the complete assembler/selector and
independently reproduced the same map hash; pin-specific clearance is recorded
separately. No installed producer, mathematical acceptance, useful-growth or
deployable-v5 claim follows from this source checkpoint. Public export invocation
and its resource plan remain root's separate decision, not an automatic sequel.
