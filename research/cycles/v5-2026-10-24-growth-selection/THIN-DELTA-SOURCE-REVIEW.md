# Thin delta materializer: independent source review

2026-10-24. `thin_delta_audit`. Canonical guard passed. Source-only review;
no compiler, native import, test, package, protected state or Git mutation.

## Verdict

**PASS for the exact source correction; GO for root to select a bounded next
integration/compilation boundary.** No blocking changed-source finding. This
does not establish compilation, actual materialization, fresh registration,
ordinary-project use, general compatibility or final-v5 readiness.

A standalone syntax build is optional, not a required extra campaign. The
existing worker executes the source through Lean for actual materialization;
root may include compilation in the separately reviewed useful boundary rather
than pay for a duplicative syntax-only run. This review authorizes no launch.

## Exact reviewed identities and delta

| Source | SHA-256 |
|---|---|
| `ordinary_thin_delta/ReferenceModule.lean` | `026839805f72f8ae9bab99cc4401d878206052ff090175a64bc039405b186c91` |
| Preserved `ordinary_reference/ReferenceModule.lean` | `6660c657e10b7f34bcb2ecc1c32361c34075ff137197be9d87bb54780e03303e` |
| `ordinary_thin_delta/CONTRACT.md` | `44e245ef7141de9b059c423b9de0508204e5834df53b41ca31c4df138d15edb0` |
| Pinned Lean 4.34 `Lean/Environment.lean` | `ee364e4788ce0560c87f621eeb3c4c3dfec62e8db4e15e099fd80e6adc533b86` |

Read the entire fresh source and contract. The line-ending-normalized diff
contains exactly three explanatory comment lines and replacement of the old
unconditional `!env.header.isModule` refusal with:

```lean
if env.header.isModule != publicView then
  fail "IMPORTED_ENVIRONMENT_MODE_MISMATCH"
```

The source uses the same condition on one line. No parser, import flags,
declaration rule, budget, output format, record check or control flow elsewhere
changed. The predecessor was not edited. Actual byte hashes above, rather than
the normalized comparison, identify the two distinct sources.

## Why this is the correct mode distinction

Pinned `Environment.lean:2308` defaults `finalizeImport.isModule` to
`level != .private`. The public `importModules` call at lines 2438-2449 forwards
the requested level without overriding that default. Private inspection thus
has enclosing `header.isModule = false`; exported inspection has true.
This does not determine each imported artifact's own modern-module flag.

The fresh materializer has exactly two `checkBaseHeaders` call sites:

- `importBase` at line 506 supplies `level != .private` immediately after its
  actual import; `run` invokes this separately for private and exported views.
- `reread` at line 602 supplies the same expression after importing the actual
  generated artifact. CLI dispatch supplies only `.private` or `.exported`.

Thus the new equality checks the actual supported import contract. It does
not weaken exported mode to permit a private map. No caller-supplied plan field
chooses this Boolean, and neither the header nor either constant map is mutated.

`setExporting` is a no-op on non-module environments, but that is not a bypass
here: private record/inventory inspection uses false, while public checking
uses a separately imported exported environment with the requisite true header.
The parked special source-authoring path is not repaired by this source.

## Safety and realization obligations retained

- `checkBaseHeaders` still requires every imported module's `isModule`, exact
  per-view original module order, generated chain/order and output suffix.
  `checkModuleHeader` still binds modern generated headers, exact direct imports,
  constant inventories and unique module identity.
- The base request/plan retains exact registered identities and the explicit
  artifact map. `searchPathRef` is empty; plugins and extension loading are off.
  Names alone and native digest labels are not independent base authority.
- `checkBaseRecords` inspects both frontend and kernel maps against the distinct
  registered projections. The new guard does not turn private availability into
  a public frontier or invent a signature-only proof warrant.
- Decoding permits only the registered usable/public/generated frontier and
  earlier new declarations. Collision checks inspect actual private records.
  Both `CheckedExtension.checkBatch` calls remain; its `addDeclCore` has checking
  enabled and rejects unsupported/unsafe/sorry dependencies under its policy.
- `OwnerRebind.exposeAdded` exposes actual new checked recursors and prefixes;
  it does not build a public base from private records. The writer comes from
  the separately checked exported environment, not from private inspection.
- New inventories are checked against both actual maps before writing. Both
  fresh rereads retain exact output/base/header/inventory checks. A failed
  public projection or missing private-only proof dependency still refuses.

The unchanged registered-import preservation argument is reused from
ORDINARY-REFERENCE-DELTA-CONTRACT, not proved anew. Compact metadata checks rely
on exact protected artifacts and current registered correspondence; they do not
become independent mathematical acceptance merely because this guard passes.

## Remaining integration boundary

`reference_registration.support_descriptor` includes the delta native source.
This change requires a new exact support binding and genuine fresh registration
under it, unless a separate migration is justified. The old registration or a
saved matcher report must not be relabeled. The logical installed role remains
`reference/ReferenceModule.lean`; this source directory alone is not an install.

No additional inevitable materialization failure was identified in this narrow
source review. This is not a claim that every later stage will pass: actual
public-frontier proof compatibility, fresh output serialization/imports and
ordinary consumer use still require their selected integration evidence. The
growth payoff is avoiding duplicate bases/new producer execution for the stated
warm compatible workflow, not a measured speedup or general cold-ancestry result.

## File-only assembly successor review

2026-10-24, subsequent bounded assignment. **GO for one root-selected file-only
assembly**, with the selector's original outer limits: 90 wall seconds, 50 CPU
seconds, 512 MiB and two processes. No native/owner/registration operation is
included. This review did not execute or import either adapter or its helper.

Reviewed both complete adapter sources and the supplementary CONTRACT selection:

| Source or input | SHA-256 |
|---|---|
| `ordinary_thin_delta/assemble.py` | `deda266fa8ec2a75ed0fc5dac58b8539c9bf74b04bf480e8629019477774f14f` |
| `ordinary_thin_delta/select_assembly.py` | `9f7775e2e401e2a477b40be7843d463269494d330967f65d6e2cfffe84e16cbf` |
| Exact assembly-03 base `PROFILE.json` | `a10e1f3ae0e1ac04cfa01240c9c07c3ca2d3da91616a3ca34b1f28b88adadbbc` |
| Exact assembly-03 base `ASSEMBLY.json` | `75f7f7c048208b337082c9b0529b02ac4fb6547d143ca178eacb73ba971da202` |
| Canonical one-overlay source map | `b4ea2095856d90190fff17ed455b2b2a4fbeaa78025134a8532eb3186415893b` |

The map is the serialized `source_pins` object, not a separate source-map file.
It contains only `reference/ReferenceModule.lean`, 34,209 bytes, with the already
reviewed `026839805f72...` hash. I independently recomputed that map hash with
the same exact ASCII JSON spelling, without running the selector.

Normalized comparisons against frozen `ordinary_reference_package/assemble03.py`
and `select_assembly03.py` show only the selected successor names/paths, actual
base-03 profile/receipt constants, one overlay mapping, internal loader names,
and honest experimental/new-support claim. No copy, validation, resource or
commit algorithm changed. The original builder helper pin remains
`49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5`.
Its main/build entry is guarded and not invoked by the file-only calls used here.

Read-only actual base inspection confirms 137 profiled auxiliary roles, 165
payloads plus PROFILE/ASSEMBLY, and zero size/hash mismatches across all 165
base payloads. The actual installation manifest remains `32236aa3d7bcbf...`,
implementation `fafc83872c4b...`, as asserted by the exact base receipt. This is
input-identity evidence, not a new mathematical qualification.

The successor requires exactly that base census and one changed existing role;
164 other payloads stay byte-identical. It hashes/checks each copied output and
all inputs again, regenerates the 137-role profile, writes an honest assembly
receipt, and commits PROFILE last. Fresh output is restricted to
`experiments/v5-local-checks/thin-delta-assembly-01/package`; alias/overlap,
unexpected-tree, source drift and failed-copy paths still refuse. Partial files
are retained with no automatic retry. No compiler or owner command is invoked.

The selector reads and pins the exact assembler, base, runtime inputs and five
source snapshots, then writes only its fresh selection JSON. It neither launches
that selection nor opens owner state. Source and input rechecks before writing,
the original finite budgets, and the later runner's hard containment remain.
The source map argument must be the full reviewed hash above.

No changed-boundary finding blocks this single file assembly. Fresh support
registration, native delta checks/rereads and ordinary consumer use remain later
gates. The retained special authoring commands are still parked; including their
unchanged bytes in this experimental package does not qualify or select them.

## File-only assembly actual-output audit

2026-10-24. **PASS for the completed file-only assembly and clean closure.**
Read-only inspection only: no assembler/selector rerun, project Python import,
Lean invocation, support registration, protected owner-state access or Git
mutation. The canonical guard passed, including after audit resumption.

Audited run: `experiments/v5-local-checks/thin-delta-assembly-01`, whose fresh
output is its `package` child. The exact selection is
`94036e6b9bd47a3fc94cc8e88899d5751c57f4b04fe98b444462a5eed3cd9bf3`.

| Actual output | SHA-256 |
|---|---|
| `PROFILE.json` | `dfe0ae9772cde81a98f0a320d7dfcfc82985c9c10acafb594094203d41855219` |
| `ASSEMBLY.json` | `db69f222b9882c36591c63b43726ac04134271587cd1863078f2c0729e77a3d5` |
| Changed `reference/ReferenceModule.lean` | `026839805f72f8ae9bab99cc4401d878206052ff090175a64bc039405b186c91` |

Independent size/hash checks found 165 output payloads, all matching their
profile/installation pins, including 137 auxiliary roles. The exact output tree
has 167 files: those 165 payloads plus PROFILE and ASSEMBLY, with no unexpected
files. Exactly one payload differs from frozen reference-assembly-03:
`reference/ReferenceModule.lean`, 34,209 bytes, with the reviewed hash above.
The other 164 payloads remain byte-identical. All five staged source snapshots
and all 178 runtime/input pins match the selection. Copied payload bytes total
57,985,539; this is packaging volume, not a mathematical closure measurement.

The unchanged installation and implementation identities are respectively
`32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2` and
`fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df`.
The selected base/profile, base/receipt, assembler, selector and one-overlay
source-map identities agree with the reviewed inputs in the previous section.
Parsed command stdout equals the saved ASSEMBLY receipt. Actual stdout is
8,344 bytes and stderr is empty.

`command/command.json` records only `argv`, `cwd` and `limits`. Each field equals
the corresponding value in `RESULT.json.result`. Comparing these two *entire*
objects gives false because the latter additionally records execution status,
cleanup and resources; that is an expected schema difference, not input drift.

The saved outcome is `COMMAND_EXITED_ZERO_AND_CLOSED`, exit code zero, direct
child reaped and Job closed, with no cleanup error or termination request.
Final active processes are zero, terminated processes zero, total Job processes
two. This stays within the selected 90-wall-second, 50-CPU-second, 512-MiB and
two-process envelope.

| Saved resource observation | Value |
|---|---:|
| Outer elapsed through result | 6.618081800173968 s |
| Child operation through cleanup | 6.044655899982899 s |
| Child Job CPU | 2.578125 s |
| Separate outer wrapper CPU | 0.890625 s |
| Nonduplicated observed CPU sum | 3.46875 s |
| Peak Job private commit | 18,370,560 bytes (17.51953125 MiB) |

The nested `wrapper_supervision_cpu_seconds = 0.03125` is not added again.
Resource readings are the saved runner observations, not a new whole-machine
or hermetic-runtime measurement.

This closes only the selected one-overlay file assembly. The changed native
source still needs genuine new support registration before a later selected
owner/native workflow can use it. No new mathematical acceptance, native delta
use, ordinary-project integration, growth speedup, broad compatibility or
final-v5 readiness follows from this packaging PASS. The retained special
source-authoring lane remains parked.

## Retained-A public export selector: source-only review

2026-10-24. **GO for root to select the single bounded `thin-delta-export-01`
operation.** No changed-source blocker found. This review did not execute the
selector, import Python support, launch Lean or open mathematical owner state.
Both the proposed selection and output paths were absent when inspected. The
future integration adapter is not included in this verdict.

| Reviewed fresh source | SHA-256 |
|---|---|
| `ordinary_thin_delta/select_export.py` | `f497b08ecad02805438031a6dd1237bcd469d4bf7ebea28ab9db920e1f911453` |
| `ordinary_thin_delta/project-selection.json` | `a6680d7e6d607cc2f9a2e838eb6273672ea0ab521ae7718e035ee118711fe02e` |

Read both complete files and the actual selected public producer dispatch,
production controller, project-selection parser, runner binding rules and native
export entry. The fresh selector loads only the exactly pinned, previously
reviewed file helpers. Their assembly/build entrypoints are not invoked.
It performs bounded ordinary-file inspection, requires new selection/output
paths, snapshots the new config and selector, and rehashes every retained input
before publishing its fresh selection. Its own allowance is 60 wall / 40 CPU
seconds. No compiler build, support registration, owner initialization, special
reference authoring, automatic intake or migration is selected.

Independent file inspection confirms the actual native-src01 package has exactly
141 payloads plus PROFILE, with zero payload size/hash mismatch; all nine
installation-listed runtime files match too. Its 111-role PROFILE is
`fc45893cef624978f0ab5212d0e1e172ff7c71f821124daa8751727bf7123ef6`.
The actual BUILD-RESULT (`26e975ad71675ccc13cc93e0d80f343922b0a9ff046f20cfe37c54ea713c2f82`)
and outer RESULT (`d7a7b6f42ff0986ab9c2708c8a1a4f2386245f0798931f303eed46aaa8fa5b2f`)
match the selector's package/selection/clean-closure checks. The new-source-built
exporter is 809,472 bytes, SHA-256
`0908634fbab219414acb7fc79bacc077612f39572b1957e22a2fb0d52438057a`;
the helper's historical retained-binary constant is not substituted for it.
No obsolete ASSEMBLY receipt is assumed.

The config exactly matches the supported trusted-project schema: retained
`author-A/modules`, then original P's library root, importing the single actual
`DMKNAuthor_9c9ea8a5496754b2a6e369b198f863ad7cd70c826642c2be283bab15de4a6306`
module. Its 75-byte ASCII name fits the current project-mode 96-byte component
bound. The five A and five P compiled parts independently match the selector's
sizes/hashes and exact directory censuses. A's retained source directly imports
P. Existing target bytes (`ddea2b29e902165a70df7cad854fd8eb2cc3116d18d86f0e43d5d287ae620882`)
select exactly `DMKNReferenceA.flip_apply` and `DMKNReferenceA.flip_involution`.
They are runtime-pinned, not reconstructed from a prior report.

The one selected command is the actual public `owner.py produce-baseline`, with
explicit approved-local-project consent and no owner-state arguments. Dispatch
branches to `run_producer` before opening any owner/catalog. It creates a fresh
bundle and supervises the existing native exporter. That exporter imports the
original private environment with plugins/extensions disabled, requires safe
nonaxiom target declarations, indexes the actual kernel, and invokes
`Export.selected` for complete proof dependencies. It neither recompiles A's
tactics nor treats its old author report as a proof. The binder checks actual
writer output and writes an inert manifest last. Production is not acceptance;
private artifacts are approved local inputs, not a hostile-input sandbox.

The selected inner caps are 120 wall / 90 CPU seconds, 1,536 MiB memory and
144 MiB spool; outer caps are 150 wall / 120 CPU seconds, 1,792 MiB memory,
six processes, 4 MiB stdout and 1 MiB stderr. They fit the established public
export envelope. The runner verifies exact runtime pins before and after the
operation and requires the snapshotted config in the actual command. This is
explicit file binding, not a hermetic pin of the entire installed Lean library.

The useful outcome is a newly produced complete A proof closure, or a retained
failure resolving whether that route fits the supported envelope. Its actual
new units, imports and common-base identities must be inspected before funding
registration/intake/materialization. No predeclared two-unit closure, ordinary
thin reuse, growth advantage or final-v5 claim is justified by this source GO.

## Export01 failure and exact fresh export02 correction

2026-10-24. **Export01 FAILED; GO for one separately selected export02 under
unchanged caps.** The previous source review missed the strict JSON parser's
rejection of the config's terminal newline. It is not evidence that export01
passed, and its failure/source/output remain preserved.

Read export01's saved RESULT/stdout/stderr once. Selection
`69dd93fae1a83db03c62a254e043b437cede04ecff73da21190b680d55a1695f`
ended `COMMAND_FAILED`, exit 1. The actual producer failure is INPUTS
`JSON_LEXICAL_TOKEN`, with `native_entered = false`, zero native grant/charge,
no manifest attempt and no bundle directory. Thus no theorem closure was
extracted. Outer cleanup is complete: child reaped, Job closed, no cleanup error,
zero active/terminated processes, no termination request. Outer elapsed is
1.7622595997527242 s; child Job CPU 0.78125 s plus separate wrapper CPU 0.765625 s
gives 1.546875 s observed CPU without double-counting nested supervision.
Peak Job private commit is 29,810,688 bytes. The 1,320-byte stdout records the
failure; stderr is empty. These costs remain charged, not reset by the successor.

| Fresh reviewed source | SHA-256 |
|---|---|
| `select_export02.py` | `c5560ec4ccc4eb0f16cd48c77c19217bac0ef30b0e30a39a512183d30948a168` |
| `project-selection02.json` | `60376198a6fd6459564d55f1b8cccf0e57ff31ca6b4018ee8a0e17b7142fc59c` |

Read the complete selector and compared it to preserved01. Changes are only the
fresh operation/source/config paths and config pin, plus a bounded exact-byte
preflight requiring `S.encoded(project) == project_raw` and its expected hash.
Independent byte comparison confirms config02 is exactly the old 671-byte file
minus its one terminal LF: 670 bytes ending in `}`. Names, paths, modules, native
program, retained inputs and all resource caps are unchanged. Original selector
and config hashes still match the previous review. The installed strict parser
has no whitespace-token allowance; the corrected compact bytes fit its syntax.

No package re-audit, selector execution, native call, owner/state access or Git
action occurred in this review. The preceding exact package/input review is
reused, while the successor will re-pin its inputs and the runner checks them
before/after execution. The fresh preflight closes this specific needless-run
failure; it does not predict successful complete extraction or qualify the
separately reviewed later integration boundary.

## Actual export02 closure and complete integration-source review

2026-10-24. **Export02 inert production PASS; GO for root to select one
five-call thin-delta integration with the exact actual bundle below.** This is
not mathematical acceptance of that bundle, a prediction that later native
stages succeed, or a final-v5/growth qualification. No selector, project Python,
owner API, Lean command or Git operation was executed by this reviewer. Only
source, saved operational outputs and the pinned inert frontier hint were read.

### Actual retained export02

Outer selection `dc780f08b93f1640c5ff7b55a4b33ebe984206bc8ea5119f4477ea463d0635b4`
returned `COMMAND_EXITED_ZERO_AND_CLOSED`, exit zero, reaped child and closed Job,
no cleanup error or termination request, zero active/terminated processes.
The public reply is `PRODUCED_INERT_BASELINE_NOT_ACCEPTED`, with mathematical
acceptance false. Inner native supervision also closes cleanly; its diagnostic
trace records private import, actual kernel indexing and selected export.
Its 371-byte stderr is the expected phase trace, not the outer command stderr,
which is empty. The outer command stdout is 3,237 bytes.

| Observation | Value |
|---|---:|
| Outer elapsed | 6.989411399699748 s |
| Whole child Job CPU | 3.984375 s |
| Separate wrapper CPU | 0.703125 s |
| Nonduplicated observed CPU sum | 4.6875 s |
| Peak outer Job private commit | 501,133,312 bytes |
| Total outer Job processes | 6 |
| Inner native CPU (already included above) | 2.0 s |

Actual bundle: `experiments/v5-local-checks/thin-delta-export-02/bundle`.
Manifest is 1,548 bytes with SHA-256
`5877f1110daf39573dcb9e1ca3073c1310a07be76fc8cbe42015e59860f45e8d`.
The one batch contains eight units, 47,677 bytes. Independently recomputed raw
hashes, sizes and domain-separated unit identities all match. Six units are
byte-identical to retained original P. Exactly two units are new:

| Target | Unit ID | Raw bytes |
|---|---|---:|
| `DMKNReferenceA.flip_apply` | `1d6516b2864ce1d47584a1f0d6d5e0bc37ecd8850eaf847eaee81874b64e3e0c` | 7,904 |
| `DMKNReferenceA.flip_involution` | `4df12de0b842acd0d9d60998f17bcb028961a1ccfd2d47778d75886402026530` | 8,690 |

Their target export IDs are respectively
`6e4bfef74cce65c220f3230bc830f722de4e5930d7900abed730f2f08289b4a1`
and `8c1b50cb3d4f426a7835352a7dd143f83a40979c0b62108fb0e2c3c6e0b58ea2`.
Each is a theorem declaration with a retained proof DAG, not an erased axiom
interface. Their 12 and 9 imports respectively match the exact public-unit or
usable fixed-basis export identities in the saved `2c225a66...` frontier hint.
Neither imports the other new theorem, an unavailable private name or another
new helper. Thus the two requested targets reach the complete two-unit new
closure without a cycle, extra new mathematics or base-name redeclaration.
The private `hidden_low` target remains absent from that public frontier.
This is an inert compatibility check; the later live registration/owner checks
remain necessary and may refuse.

Actual inventory, request, project-selection and writer bytes match all four
production pins. Actual spool is 19 files / 976,353 bytes, matching the public
result. The preserved PRODUCTION file deliberately says prepared-before-manifest;
completion is established from the actual final manifest/files and successful
live operation report, not by relabeling that intermediate file.

### Reviewed integration source and authority flow

| Complete reviewed source | SHA-256 |
|---|---|
| `ordinary_thin_delta/integrate.py` | `ba11d050b576a2658009bec28b025efa5e1e69e372700cd41a0bf644741b83f4` |
| `ordinary_thin_delta/select_integration.py` | `a7c6a40a3ee05995e6f1cb4d2f8d2e3944e801dc48932766db70e3127312325c` |

The selector requires explicit workflow, thin PROFILE/ASSEMBLY and actual bundle
manifest hashes. Its file-only preflight recomputes complete unit identities,
base/new differences, exact imports, target reachability and a real unavailable
private target. It binds the reviewed one-overlay package and the existing
P bundle/project/artifact report. Old frontier bytes can only reject a selected
closure early: they do not authorize registration, intake or module generation.
The selector snapshots the workflow, helper, itself and runner; all input pins
are rechecked before writing the new selection. No owner is opened by selection.

The workflow then makes exactly these selected calls, with actual reply schemas
checked against the installed controller implementations:

1. Register P at its original root using its retained original snapshot. Require
   new support and reference IDs, actual native matching and no catalog admission.
2. Intake the newly exported eight-unit A bundle at P. Require actual CHECKED
   status, exactly the two new units checked and a new confirmed root. The live
   admission path re-preflights and does not trust the saved producer report.
3. Materialize exactly the two newly warranted theorem units under that new
   reference, excluding every base unit; require actual checked delta status,
   matching support/root/snapshot/targets and the three native build/reread calls.
4. Request the genuine private target and require the exact closure refusal
   before native entry, with zero native charge and no committed delta.
5. Compile one ordinary recipient over original P plus the generated delta.
   The explicit setup map binds original snapshot parts and new delta parts;
   original P bytes must equal the retained original library. Neither A's producer
   module nor generated replacement base definitions are included. The recipient
   derives `flip_injective` using both involution instances and uses `flip_apply`
   at a changed argument while retaining P's notation. Its own compilation is
   not new commons admission, as the report explicitly states.

All operations have fixed ordering, retained outputs and stop-on-failure behavior.
There is no owner initialization, snapshot recopy, fixture/A rebuild, state
migration, proof repair, source-authoring revival or automatic retry. New module
checking and the two fresh rereads remain mandatory under the reviewed materializer.

The workflow's one nonrenewing parent budget is 500 wall / 350 CPU seconds and
1,536 MiB; outer runner is 600 wall / 450 CPU seconds, 1,792 MiB and eight
processes. Individual call grants are capped, shortened by the remaining parent
budget and precharged; unknown child CPU retains the full grant. Actual whole
child Job CPU replaces a grant only with a closed child observation; the separate
clean-closure check still must pass before continuation. Final source/input and
recipient artifact hashes are rechecked. No runtime allowance is enlarged by
this review. No blocker was found for this single current capability boundary.

## Integration01 actual outcome: committed delta, failed return

2026-10-24. **Overall integration FAILED; preserve its successful prefix and
committed delta. Do not regenerate it.** Selection
`fc2bd181e5b4c6862bed7949ede7f3d5acea59ca8c22ed5a59661acb2b96453a`
ran once under the original caps. Saved `RESULT.json` and `workflow/WORKFLOW.json`
are terminal. The workflow stopped during DELTA; the private-frontier refusal
and ordinary recipient calls were not executed. No complete thin-reuse workflow,
ordinary consumer qualification, growth benefit or final-v5 result follows.

Review used saved outputs and source only, with no runtime/import, protected
owner/database API or Git mutation. Root additionally selected one pass over the
exact committed record, its named immutable event files and its five named
artifact parts. No store enumeration, recovery call or broader historical audit
was performed.

### Actual achieved prefix

- Fresh registration returned `REGISTERED_LOCAL_ORIGINAL_REFERENCE`, using the
  retained original snapshot and a live native match. New reference is
  `4722560b5e9eb0399fc43e7e3ebf7ced075c1e27dab7960010b221345806aa9f`;
  new support is
  `1ef735869430cd1464402590454a762ce899d3657b53c1dfb51a1f643d68b1bb`.
  It reports five public units/eight public names and 522 usable basis names,
  with no new catalog acceptance.
- Actual intake of the exact export02 manifest returned CHECKED for two new
  units, reusing the six base units. The confirmed accepted root is
  `25eb64bd776e0fdaa766f455f84129746613d7e0e83a65242611751ba75ba863`.
  No later failure rolls back that accepted prefix.
- Native delta construction completed both new-proof checks and its build,
  private reread and exported reread. All three saved phase exits are zero;
  inner native supervision is clean zero/closed. The resulting delta record was
  committed, but its postcommit loader failed before the public success return.

### Exact committed materialization

Committed ID:
`10a905f4881d4175f755b86bc8ee2f5fa8fcb161989853c20e7c0495638c032e`.
Its record is 5,972 bytes, raw SHA-256
`435059b1e393102c711166d5205f93344a7e29797606786e77a2d4997d482de9`,
under the existing realization store's `records/` directory. Its operation is
`47875cade8bd29e7ddfe979b05fca3627bceb5160ddd2c8a11048052efb8483c`.
The actual module is
`DMKNBridge_c69df1f6cfb6be3df7d4a7dc419e2c9f2cd9d931b509fecb9028437dea135ecb`.

All eight named event-file sizes/hashes and all five named artifact sizes/hashes
match the committed record. The actual request/native report/record agree on
the two A units, two added names and direct import of original
`DMKNBaselineFixture02` only. No P unit is regenerated. The native report records
two units checked, zero units matched, two checking passes and zero preceding
generated names. Native final report SHA-256 is
`a311334857340ff47a63d1e57fc0c8cef99fd6047abefe794f7b36fc54727e29`.

The five generated parts total 10,816 bytes: 9,144 `.olean`, 96 `.olean.server`,
232 `.olean.private`, 176 `.ir.sig` and 1,168 `.ir`. These are retained actual
checked materialization outputs. They do not establish that the public loader
can currently return them successfully or that the unrun recipient can use them.

### Failure cause established, and what remains unknown

The public delta reply records phase `PROTECTED_COMMIT`, error type
`ReferenceCommittedError` and store disposition
`COMMITTED_REFERENCE_REPORTING_FAILED` for the exact ID above. Source tracing
locates this wrapper precisely: `reference_store.py::_commit_delta` has already
renamed the staged record, read it back successfully and cleared its grant;
then `load_delta(identity, context, check)` raises. Its exception is chained in
memory but its type/message are omitted from `ReferenceCommittedError.report`.
The public owner serializes that report, not the chained exception. No saved
selected event supplies the missing loader predicate or traceback. Thus the
exact underlying loader cause remains **unresolved**, not guessed.

The harness's top-level `SMOKE_UNCLEAN_PROCESS_TREE` is misleading in this case:
its shared `clean` predicate combines expected success exit status with cleanup
checks. Delta returned a clean exit 1 where exit 0 was expected. All three
actual public child Jobs and the outer Job have reaped children, closed Jobs,
empty cleanup errors, no termination request and zero active/terminated
processes. This is not observed process leakage or forced timeout.

The 107.03125-second public controller-plus-native observation is below its
108-second owner allowance; the 107.1875-second whole delta Job is below its
110-second cap. Proximity alone does not prove CPU exhaustion. Other internal
checks are possible; without the suppressed exception, neither a budget failure
nor a specific semantic/record bug is established.

### Costs and continuation boundary

| Public child | Wall through cleanup | Whole child Job CPU |
|---|---:|---:|
| Fresh registration | 105.39121820032597 s | 51.65625 s |
| A intake | 4.496079199947417 s | 3.1875 s |
| Delta, including failed postcommit return | 118.455411599949 s | 107.1875 s |

The child-Job sum is 162.03125 CPU seconds. Outer whole child Job CPU is
163.71875 seconds, already including that sum and workflow controller activity;
separate runner wrapper CPU is 2.0625 seconds. The nonduplicated outer observed
total is **165.78125 CPU seconds**, with **230.2190608996898 seconds elapsed**.
Peak outer Job private commit is 1,554,034,688 bytes. Its total process count of
24 is cumulative across serial calls, not simultaneous use beyond the eight-
process cap. Nested native CPU, controller observations and supervision readings
must not be added again. All consumed work remains charged.

An existing public exact-ID retrieval path is source-supported, but **not run**:
`export-reference-delta`, with this accepted parent root, this new reference ID,
`--parent-delta-id` set to the exact committed delta ID and the same two-target
file `thin-delta-integration-01/workflow/delta-targets.json`, plus the normal
pinned profile/runtime/store/allowance arguments. It first validates `load_delta`;
if successful, the already-covered-target branch returns
`REUSED_LOCAL_ORDINARY_REALIZATION` with no native call or new reservation.
It may still fail the same loader. It hashes/validates the selected snapshot and
chain, so no constant-time or cheap measured recovery claim is justified.

The smallest identified diagnostic improvement is preserving a bounded inner
exception type/message in the postcommit error, without weakening checks or
discarding its committed-ID disposition; separating an unexpected child exit
from cleanup failure would also improve reporting. Neither change nor a new
package/run is selected by this audit. Preserve the actual committed record and
accepted root; any later exact-ID retrieval must be separately scoped. Close
this test campaign and assess the architecture's useful-growth payoff before
funding another implementation step.
