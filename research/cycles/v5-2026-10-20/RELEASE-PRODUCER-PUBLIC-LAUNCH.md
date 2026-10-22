# Public release-owned producer: stable origins and genuine operation evidence

Status: source-design recommendation, 2026-10-22. No public-launch implementation,
installation, constructor, snapshot, request, proof or test was run for this
checkpoint. The component control used by root is a separate allocation; its
sources and evidence remain frozen. This note does not adopt a release or renew
an allowance.

## Decision in one paragraph

Use one narrowly scoped, producer-owned finite launcher, reached through the
existing installed distribution entry and using the already shipped Windows
Job supervisor. Keep producer modules at stable installed `sdk/v5` origins.
Give this path its own truthful selection and result schemas, and adapt only
the generic snapshot's selection/outer-evidence boundary. Do not change the
general client's copied-source import policy, disguise public results as local
research results, or flatten the producer and reader source maps by overwriting
the newer verifier. Subject to the separate compatibility argument, retain the
current reader verifier and extend the producer's import closure to include its
three existing helper modules. Add an ordinary release-bound profile-creation
operation so public users do not need the research stager or a hand-edited
large profile.

This is an operational adapter around the existing producer and mathematical
checker, not a new installer, agent framework, proof system, scheduler or trust
authority. A producer-specific launcher is justified by a real difference in
execution identity: a resumable producer must retain one installed profile
across operations, whereas the general client intentionally runs source copies.

## Observed sources and the concrete obstruction

The installed consumer candidate is
`product-local/v5-distribution-candidate-preflight-01/Mathematical Commons v5`.
Its release digest is
`bd9f161c43551a578605d5e0c7da34c332cb838c1c70ddb859d2ebd0062b8f03`.
The authoritative 130-entry input is
`experiments/v5-local-checks/distribution-candidate-preflight-01-input.json`,
digest `25e7c849e41f394498e21a60cc7800ecffb67b0cee1b3911d7164977ce4f2364`.
Logical paths must be resolved through that map, not an arbitrary older
`software/v5` directory.

Read for this analysis:

- The complete `client/launch.py`, digest
  `523a3031da86457037af3c41f87425cd406e5fe3fcf6a2edb2d87eff9b59ef78`.
- The complete `client/boot.py`, digest
  `76cdcd42379d61c5fe37dc86a23363687c084c56887302dcdd922aa9b089ce2b`.
- Complete generic lifecycle producer/snapshot, release producer/adoption/entry,
  and the relevant complete supervisor/Job implementation functions.
- Current `body_location/distribution.py` build, manifest validation,
  verification, materialization and launch functions, digest
  `eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813`.
- The aggregate producer's exact outer-evidence validator and request/lineage
  accounting sections. These are not replaced by this proposal.

The current public launch is:

```text
distribution launch
  -> client.launch (trusted finite parent, original public clocks)
     -> client.boot inside a Job
        -> copy selected sources under RUN/sources
        -> execute copied owner.main(context)
```

`boot` keeps exact source bytes in memory, installs a loader that compiles those
bytes, and permits product imports only from selected copied sources. It also
checks the full selected Python subtree at entry and exit. Original installed
SDK product imports are not permitted by that guard. Its result is
`DMKN_V5_CLIENT_BOOT_RESULT_V1`; the parent result is
`DMKN_V5_CLIENT_LAUNCH_RESULT_V1`.

The release producer requires actual core origins beneath its adopted
`ROOT/sdk/v5`, matching descriptor and support-runtime pins. Its profile ID
commits the whole absolute-path profile. Rewriting the profile to each
`RUN/sources/v5` therefore fails in two ways:

1. The current adoption contract confines selected sources to the adopted
   release and fixed logical `sdk/v5` locations.
2. Changing those paths changes the profile ID between snapshot, request and
   proof-stage invocations. Earlier snapshot/session/allowance evidence then
   cannot be continued as the same profile.

There is a separate evidence incompatibility. Generic
`aggregate_lifecycle.snapshot._selection` accepts only
`DMKN_V5_LOCAL_CHECK_V1`; inherited `aggregate_small.producer._local_outer`
accepts only `DMKN_V5_LOCAL_CHECK_RESULT_V1`, reconstructing the research
wrapper's `{snapshot}`/`{output}` argv substitutions. The new release entry's
`_snapshot_selection` also binds that exact research invocation and copied
entry location. A clean public client result is not an instance of this
grammar. Renaming its schema is not an adapter.

Finally, all non-serving current distribution commands materialize a consumer
preparation/runtime adoption and demand atomic/aggregate issuer mode. A
producer command must have an explicit branch; it should not manufacture an
unused consumer adoption merely to satisfy that unrelated branch.

## Options compared

| Route | Real advantage | Additional obligations | Disposition |
|---|---|---|---|
| Add stable-origin mode to general `client.boot` | Reuses its held-byte loader and existing result | Changes all clients' loader/namespace/origin policy; still needs new snapshot evidence; existing result schema must express mode | Unnecessary shared-boundary change for now |
| Run installed producer as a subprocess of copied owner | Keeps `boot` source policy unchanged | Adds boot + producer + host process nesting, another exact invocation/result boundary, repeated client source/runtime setup; still needs truthful snapshot adapter | Feasible fallback, not smallest path |
| Dedicated finite producer launcher using existing supervisor | Stable installed module identities; producer + host inside one outer Job; no client loader changes | New small launch contract and installed-source entry; precise evidence adoption | Recommended |
| Stable identity with arbitrary runtime-source overlays | Could retain one logical profile across copies | Changes meaning of source identity, imports and allowance binding; risks silently discarding location commitments | Reject for this milestone |

The recommended launcher does not need arbitrary user code, service mode,
network calls or runtime-loaded plugins. It supports the selected producer
actions only. The general client's separate trusted-owner API remains intact.

## Source compatibility: preserve the receiver

The independent outcome-audit agent compared current 130 with the 29 installed
producer source roles. There is exactly one divergent shared logical source:

| Logical source | Current reader | Historical producer |
|---|---|---|
| `admission/verifier.py` | 17,835 bytes, `ec6474cdd0580df89f9c646a41c0d909ec20e83da0a42274e0510a6e01bbbaea` | 12,381 bytes, digest prefix `9f77bd17` |

The current verifier requires explicit trust binding, checks withdrawal and
source domains, supports pin-phase origin checking, and continues after the
selected clean refusal while retaining post-process census/pinning. Restoring
the older file would break current callers and remove protections. It is not
a permissible merge strategy.

The reported producer path imports the verifier class indirectly through
package receiver imports, but neither constructs it nor calls it during
preparation/production. This supports forward use of the current verifier,
subject to the independent source-delta argument and one changed-closure check.
Its additional imports must be selected before any product import:

| Logical source | Current digest |
|---|---|
| `admission.pin_phase` | `ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881` |
| `admission.trust` | `c997d2a83ae5246dec9ff30eeca72e405ec0f66c0a307e53e0521eef66fae6d0` |
| `admission.clean_refusal` | `7c1386cce693185ac7d6e1dda149993c892ac5b2d417242fb7e02b873648e5a7` |

These three already belong to current 130. Add them to the producer descriptor,
pre-import closed source list, runtime pin list and actual-origin checks. A
pin added after executing the import is too late. Do not describe the old
27-source closure as complete after this change.

If the forward compatibility argument fails, a physically separate installed
producer component with an independent source root is possible. It is not a
drop-in fix: current adoption hardcodes root-relative `sdk/v5` and confines all
pins beneath that root. A nested component therefore needs genuine component
manifest/root semantics and disjoint processes, not a second `admission` package
on the same `sys.path`. Do not build that more expensive alternative unless
the shared forward closure actually fails a material condition.

## Proposed public flow

```text
immutable release + externally adopted release digest
  -> public producer-profile operation
     -> fresh owner profile outside installation
  -> producer snapshot(profile, exact packet/configuration, finite limits)
     -> one generic capsule + genuine outer completion evidence
  -> producer request(snapshot evidence, explicit allowance/budget)
     -> validated finite stage request, no dispatch
  -> producer preflight(request)        [optional explicit inspection]
  -> producer run(request)
     -> one finite attempt, retained checkpoints or receipt
  -> later run with exact prior lineage and fresh output
```

The diagram is not an automatic pipeline. Each arrow that executes work is a
distinct owner-selected finite operation. No action automatically funds a new
attempt, resumes a proof, rebuilds a binary, extends a deadline, or admits a
mathematical result. Receivers continue to independently check receipts under
their adopted policy.

### Profile creation without a digest cycle

The release must contain a relative producer-profile template or equivalently
an exact closed producer role table. It must contain every selected source,
runtime and artifact role needed to create the profile; the operation may not
consult a research profile, preparer or historical build folder.

The existing builder is the place to add this data. A selected successor
manifest should explicitly expose a production descriptor/template and the
three producer artifacts, with a new manifest contract if required by exact
field validation. Existing six consumer roles retain their meanings; a
receipt-verifier executable is not the stage host, snapshot host or guest.

The manifest pins the descriptor/template; neither descriptor nor template
pins the containing manifest. After the caller supplies the adopted release
digest, `producer-profile`:

1. Validates the release, descriptor and relative template against exact role
   and file-map rules, including ordinary disjoint output paths.
2. Materializes source/runtime/artifact paths under the installed root.
3. Inserts the adopted manifest pin and descriptor pin into the explicit
   release, host, image and snapshot adoption fields.
4. Writes a fresh profile and small result outside the immutable installation,
   with exact bytes/digest and a failure override for failed finalization.

No owner constructor, host call or proof is needed to materialize it. The
operation must still be finite and report its cost. It can be a small branch
of the installed distribution entry; no extra general-purpose profile service
or installer is needed. Validate generated bytes with the same closed profile
shape used by the producer before reporting successful creation.

The template must not contain its own profile file path, a run name, transient
source-copy paths, current clocks or mutable state. Repeating materialization
at the same installation with the same explicit policy options produces the
same profile bytes and profile ID, even when the profile document is saved at
a different external path. Its original snapshot profile document still has
to be retained when cited by snapshot evidence. Relocation changes absolute
paths and therefore deliberately creates a new profile/allowance lineage;
this proposal does not migrate existing attempts.

### Finite launcher and worker

The distribution wrapper verifies a real producer command and its selected
role, then invokes the producer launcher with the *original* public clocks.
The launcher imports only stdlib and exact shipped supervisor helpers before
starting the bounded child. It does not construct the producer in the parent.

The child is one selected installed producer entry, optionally copied as exact
held bytes into the run directory before dispatch. Copying only this bootstrap
entry is compatible with stable producer identity: the installed entry remains
a committed runtime pin, and the actual copy must equal it. Core modules are
not relocated. The existing entry already distinguishes actual entry bytes
from the matching installed entry role; its public successor must preserve and
tighten that distinction rather than redefine the profile.

Inside the child, validate the complete selected product closure before any
product import. Compile imported product modules from held, pin-checked bytes
at their stable installed module origins. Reject preloaded selected packages,
unselected filesystem imports, namespace aliases and later import-policy
changes. Rebind selected original files and input/result pins at completion.
The full selected Python runtime census/origin policy must be explicit, not
silently inferred from the producer's small repeated-rebind pin subset.

This source-byte loader belongs in the successor producer entry. Do not import
`client.boot`, change its global guard, or rely only on reading a file before
and after an ordinary loader executes it: a swap-and-restore is not excluded
by those two reads alone. As in current launchers, the owner-installed Python,
bootstrap entry and OS/DLL behavior still have stable-installation/trusted-host
assumptions; held product bytes do not make arbitrary local mutation safe.

Use the existing `commons.supervise` and `run_stage.Job` without a new process
supervisor. The producer child and its native host descendants share an outer
Job; the existing nested native limit remains. The outer process cap must
accommodate actual topology, not merely the number of native executables.
The dedicated route has producer + host rather than boot + producer + host.
Actual caps remain separately selected; this note grants no increase.

## Explicit selection and outer-result contracts

Use truthful names such as `DMKN_RELEASE_PRODUCER_LAUNCH_V1` and
`DMKN_RELEASE_PRODUCER_LAUNCH_RESULT_V1`. These names describe proposed new
contracts, not records that already exist. Their final field grammar belongs
in one small shared data-validation module, selected in the source closure.

At minimum the selection must commit:

- One action from the closed public producer set and one fresh operation root.
- The externally adopted release/descriptor, exact stable profile document and
  exact action-input document.
- The installed worker role and source/runtime identities needed by its
  bootstrap, including the entire producer operative set.
- Finite process/CPU/memory/wall/log limits and output byte/entry bounds.
- The intended owner-report and action-output locations, disjoint from every
  immutable installation/input/evidence location.

Keep the complete constructor installation pins separate from transient
snapshot/session input pins. Installation bytes are not copied into the
20 MiB fixed-session envelope. The selection and documents themselves must
still fit its metadata reserve. Preserve the current 256 selected-runtime
limit unless an independently justified change is actually necessary; the
release-owned component removes the historical 315-pin obstacle.

Avoid self-referential hashing. One straightforward grammar stores roles,
inputs and output paths in the selection, not an argv containing its own
digest. The launcher computes the selection digest after saving it and derives
the actual fixed argv from those fields plus original clock values. The worker
and adopter derive the identical argv. Record that actual argv in the command
and outer result. Do not place fabricated prior pins for not-yet-produced
wire, capsule or receipt files in the selection.

A successful outer result must establish all of the following, not merely
that the child returned zero:

1. Exact selection document/digest, release, action, profile, input and worker
   identities; exact reconstructed argv, cwd and selected limits.
2. Actual Job terminal closure: zero exit, direct child reaped, no live
   descendant, closed Job, known accounting and no cleanup errors or
   unexpected termination.
3. The exact action-specific worker report, bound to its file pin, with closed
   owner and valid final binding; the snapshot action points to the exact
   generic snapshot result rather than an unrelated successful file.
4. No overriding worker, core snapshot/attempt, bootstrap or public finalization
   failure marker. Checks cover the records actually cited and their specified
   marker locations, not an arbitrary scan of unrelated history.
5. Original input/source/manifest rebinding, bounded final output census and
   original deadlines through report finalization.
6. Complete operational cost fields with explicit scope and any unknown or
   pre-clock startup cost marked unknown, never zero by omission.

The parent writes its result only after child closure. A subsequently failed
final binding/census/deadline writes an overriding marker and returns failure.
Partial outputs remain retained. Request generation must not become usable
merely because a request JSON was written before a failed final check.

These records are trusted-local operational evidence, not cryptographic
attestations from an adversarial operating system. Mathematical validity still
comes from the independently verified certificate and its checking semantics.

## Minimal change to generic snapshot adoption

Two actual generic boundary checks must be adapted, plus the entry's exact
invocation check. Do not duplicate the whole generic snapshot implementation.

Recommended source refactoring in a **fresh selected successor**:

1. Add one protected lifecycle method for validating snapshot outer selection.
   Its default implementation delegates to the existing local-check validator.
2. Change the two calls in generic `snapshot.execute` and `snapshot.adopt` to
   use that protected method. Their configuration, staging, capsule/native
   result, host argv, census, cost and final-rebinding checks remain unchanged.
3. The new release producer overrides the method with the genuine public
   selection contract, and overrides `_local_outer` with the genuine public
   terminal-evidence contract. The old build-adoption methods remain refused.
4. The public entry binds its actual argv to that same public selection
   grammar; it no longer pretends to be the research wrapper's copied entry.

Use explicit methods in the pinned owner implementation, not caller-supplied
permissive callbacks, runtime monkey-patching or a fallback that accepts either
schema after the first validator fails. A profile/source contract must make
the selected evidence lane explicit. The prior component remains a different
frozen source/profile identity; its passing controls are not rewritten.

The five generic snapshot evidence roles can remain `result`, `outer`,
`selection`, `configuration`, `command`. Keeping those role names is not
relabeling if the selected successor validates the genuine new record grammar.
The result's `selection` pin and all staged commitments still name the actual
new selection. Generic session identity includes these evidence contents, so
old and new sessions do not become interchangeable.

Unchanged obligations include exact prepared packet/target equivalence,
ordered parents, selected image, no proof during snapshot, exact host command,
capsule/session bindings, actual saved stdout/command, retained diagnostic,
known cost/closure, immutable profile and finalization overrides. No proof
ancestry replay or new guest/native build is introduced.

## Cost, funding and continuation

The outer Job's measured CPU already includes the producer and nested native
work. The outer wrapper's process CPU is separate. Report full operation CPU
as outer Job CPU plus outer wrapper CPU, with declared startup/OS exclusions;
do not add the inner host CPU again. Nested measurements are breakdowns, not
additional disjoint charges. Preserve original public wall clocks, including
preparation and cleanup, exactly as the current distribution/client path does.

The existing scheduler's allowance measures its documented stage/controller
scope, not every public wrapper expense. Its `carried_external_costs` is
immutable across a same-allowance lineage. Do not silently increase that field
on each continuation, zero it to hide setup, or claim the inner allowance
already bounds every external operation. Retain a genuine outer result for
each public invocation; report their disjoint costs separately and associate
them with the exact inner attempt/request. Each public call has its own
explicit finite owner limit. Any future total-envelope funding policy must
state how these outer costs are charged; it is not supplied by a schema rename.

Profile creation, request construction, preflight and refused calls also cost
resources even with zero host/proof calls. Their reports need the same honest
scope. A failed or unavailable result is not permission to restart, refund,
reset previous charges or continue with unknown closure.

## Packaging and count gates

The existing distribution builder/validator both cap `sdk_sources` at 141.
The correct raw union is **142 = current 130 + 12 added producer roles**, not
141; one shared verifier role is a conflict, not an additional logical source.
The three verifier helpers already occur in current 130.

The current preparation includes 109 Python source pins. Adding the 12 roles
gives 121 before genuinely new public launcher/contract sources; the generic
manifest tree currently caps lists at 128. The 56 component constructor pins
would become 59 from the three helper imports alone. **These are preliminary
counts, not final launch bounds**: new public launcher/evidence modules must
also be accounted for according to their actual execution/ownership role.

Before selecting implementation or assembly, derive one final named source
map and classify each row:

- Core producer modules: descriptor, pre-import held bytes, runtime pins,
  constructor origin checks.
- Entry/evidence helpers: installed roles, bootstrap pins and selection/result
  evidence; include in owner runtime closure when the owner imports them.
- Parent-only launch/distribution code: externally adopted release role and
  outer rebinding; not misleadingly called a core imported module.
- Existing 16 selected non-source Python runtime pins versus full Python tree:
  the former remain a repeated-rebind subset, not a hermetic dependency proof.
- Three immutable native artifacts, support helpers and manifest/descriptor.

Then count SDK rows, preparation rows, actual pre-import closure, repeated
installation pins and total bytes. Preserve the 64 operative/256 selection
limits if that exact design fits. A source-role-aware packaging ceiling may
need an explicit increase from 141 for the real selected union; that is a
different issue from inflating 256 to carry historical build evidence. Do not
copy unneeded producer sources into every consumer operation simply because
the current preparation builder enumerates all Python SDK rows without a
role distinction; decide the required role selection with the final map.

All new payloads belong to the existing fresh distribution build path and
complete file census. Do not call the small staged component fixture a full
V3 distribution. Its operative-subset container was explicitly scoped as a
test component and lacks full public distribution fields/roles.

## Small, decision-changing validation plan

Source arguments precede runtime. Root separately selects any actual operation.

1. Independent source review of the forward verifier import closure, one
   selected final map, profile-generation cycle avoidance and public evidence
   grammar. Resolve counts and known incompatibilities before assembly.
2. Native-free changed-boundary checks: generated profile stability across
   different output paths, wrong release/descriptor/source/action/argv refusal,
   unselected or preloaded product import refusal, copied-entry mismatch,
   incompatible old evidence refusal, output overlap, and finalization-marker
   precedence. Use small groups tied to changed branches, not a repeated broad
   suite or repeated proof.
3. One real installed profile creation and bounded constructor/preflight
   check from a fresh operation directory without research-path dependencies.
   Verify stable profile identity, genuine installed imported origins and exact
   current receiver source preservation. This is not mathematical acceptance.
4. One selected actual public generic snapshot when the required mathematical
   input is available. Its decisive new observation is native-host operation
   through stable installed origins and genuine public evidence, including
   cwd/environment. Retain already valid native binaries; do not rebuild them.
5. Construct an ordinary stage request from that actual evidence. Any later
   proof-stage attempt requires a separately justified finite allocation and
   independently reviewed lineage. Do not run a second heavy proof merely to
   demonstrate that a launcher can call it.

The public adapter gate is satisfied only when an installed owner can create
its profile and use these commands with shipped paths and real evidence. A
passing pure validator does not close that integration gate. This gate also
does not by itself establish independent-host deployment, broad platform
support, licensing, sustained useful growth or final-v5 completion.

## Immediate implementation selection to request from root

Select one fresh physical source cut preserving logical module names and every
used predecessor byte. Expected changed boundaries are: release adoption/core
closure, public entry, one shared public evidence-contract helper, one finite
launcher, the minimal lifecycle selection hook, and existing distribution
profile/packaging/command branches. Exact filenames, counts and new schema
grammar should be fixed together before tests. No change to mathematical
images, native artifacts, scheduler stage graph, receiver trust policy, or
existing client boot is required by this design.

## Settled implementation contract (root agreement after the analysis above)

The recommendation is now selected in principle, not a menu of alternatives.
The independent compatibility checkpoint is
`RELEASE-PRODUCER-SOURCE-COMPATIBILITY.md`, SHA-256
`8e1f418d186682383931cd85c9472ccd3d6bd23b25fb12d25dfd3770f5c31078`;
it was read completely. The new physical overlay is proposed at
`software/v5/installed_production/`, preserving logical module names.

Author responsibilities:

- Integration adapter: fresh release `adoption.py`, `producer.py`, `operator.py`,
  new `launch_contract.py`, and fresh generic lifecycle `producer.py` and
  `snapshot.py` with the protected selection-method seam.
- Root: new release `launch.py`, existing distribution successor, exact source
  selection, assembly and any execution/adoption.
- Independent reviewers: contract/source and changed-boundary controls. No used
  predecessor source is modified.

There are exactly two new logical SDK files: `release_production/launch.py` and
`release_production/launch_contract.py`. The selected map projection is therefore
144 SDK rows and 123 preparation Python rows. Producer core is 31 modules:
old 27, three current verifier imports, and the shared contract. Its selected
runtime has 49 rows: 31 core, operator helper, installed entry, and existing
16 non-source rows. The repeated-rebind union is expected to be 60. The parent
launcher is separately release-pinned, not falsely declared a core import.
Exact assembly still has to verify these projections.

The contract helper is stdlib-only at module import, allowing the trusted parent
to execute its exact held bytes without importing the product core outside its
Job. Core methods may call its owner-specific functions after the closed import
gate. Proposed agreed APIs:

```text
read_selection(path, expected_sha) -> (selection, pin)
validate_selection(selection, selection_pin, *, fresh_run) -> selected namespace
rebind_selection(selected) -> no mutation; recheck original pins
command(selection, selection_pin) -> exact fixed argv
materialize_profile(root, manifest_pin, descriptor_pin, template) -> profile data
```

`selected` includes root, run, profile, input, action_output, runtime_pins, pins,
entry, release, request_output and owner_report. Profile materialization neither
writes a file nor constructs an owner. The parent launcher accepts plan path
and SHA; distribution overrides its clocks with the original public clocks.

The root-agreed launch schema is `DMKN_RELEASE_PRODUCER_LAUNCH_V1`, with exact
fields:

```text
schema, name, action, release, profile, input, entry, run_directory,
runtime_pins, limits, output_limits, prior_launches
```

`release={root,manifest,descriptor}`; `profile`, `input`, `entry` are ordinary
absolute pins. `runtime_pins` maps absolute paths to exact digests and remains
bounded at 256. It binds all operative owner pins and direct input/profile
pins; snapshot additionally binds its packet. `name` equals the run basename.
The fixed installed entry is `ROOT/sdk/v5/release_production/operator.py`; only
its exact bytes are copied to `RUN/entry.py`. The helper derives:

```text
PYTHON -I -S -B RUN/entry.py ACTION
  --source-root ROOT/sdk/v5 --entry-sha256 ENTRY_SHA
  --profile PROFILE --profile-sha256 PROFILE_SHA
  --input INPUT --input-sha256 INPUT_SHA
  --owner-report RUN/OWNER-RESULT.json
  --outer-selection RUN/selection.json --outer-selection-sha256 SELECTION_SHA
```

All four actions require the genuine selection flags. There is no arbitrary
caller argv and no selection self-digest cycle. The parent result is
`DMKN_RELEASE_PRODUCER_LAUNCH_RESULT_V1`, exact fields:

```text
schema, status, selection, worker_report, result, final_error,
observed_output, bootstrap_cpu_seconds, wrapper_cpu_seconds, wall_seconds,
pre_clock_interpreter_startup, bootstrap_containment, authority
```

`result` is the unchanged supervisor result. `selection` is the actual copied
selection pin; `worker_report` pins `RUN/OWNER-RESULT.json`. Actual parent cwd
is the full release root. Snapshot/run action directories are fresh disjoint
siblings rather than mandatory children of the outer run: earlier request
preflight requires the future action output's parent to exist, while the
future outer run must be fresh. Census covers the outer run plus actual action
output. Request's generated request is fixed at `RUN/request.json`; request
and preflight must leave their selected future operation directory absent.

`prior_launches` is at most 16 genuine outer pins in the exact order and length
of the input's `prior_attempts`. Validate each previous outer's exact selection,
action=run, worker report, same profile/allowance and production-result pin
against its corresponding inner attempt, with all named overrides absent.
Do not recursively traverse each previous outer's own prior list; existing
inner request validation already enforces the complete prefix ledger. Bound
the additional metadata count and bytes explicitly. Unknown or failed outer
closure fails closed, even if its inner report looked successful. This is not
recovery authorization.

Root's final agreement adds `input_launch` as the thirteenth exact field.
Run/preflight require a genuine completed request-producing outer pin whose
worker report's request pin equals the selected input. Snapshot/request require
null. There is no path-name inference or direct-owner bypass in this public
lane. The existing trusted low-level API remains separate. Thus a generated
request cannot be used merely because its JSON survived enclosing failure.

Template schema is `DMKN_RELEASE_PRODUCER_PROFILE_TEMPLATE_V1`, exact fields:

```text
schema, support_profile, source_pins, base_source_pins,
stage_memory_ceiling_mib
```

All template pins are relative. `support_profile` has the existing producer
schema, source2, runtime49 and exact runtime/artifact/foundation fields.
`source_pins` lists the core31; `base_source_pins` lists aggregate_small2.
Materialization fills the release and three artifact-reference maps after the
manifest digest is known. Public outer profile schema/domain are explicitly
`DMKN_INSTALLED_RELEASE_AGGREGATE_LIFECYCLE_PROFILE_V1` and
`DMKN-INSTALLED-RELEASE-AGGREGATE-LIFECYCLE-PROFILE-V1\0`; the base profile's
existing shape remains. The public profile is created once outside installation
and reused by exact pin.

The full distribution contract is an explicit V4 successor, not silently
extended V3. Its manifest exposes `production={descriptor,profile_template}`;
metadata paths are `production/ARTIFACTS.json` and
`production/PROFILE-TEMPLATE.json`. Producer binaries occupy
`assets/producer/{stage_host.exe,snapshot_host.exe,aggregate_image.bin}`.
The existing six consumer roles are unchanged. The public adoption successor
accepts V4; the component-only V3 fixture remains frozen and is not promoted.
