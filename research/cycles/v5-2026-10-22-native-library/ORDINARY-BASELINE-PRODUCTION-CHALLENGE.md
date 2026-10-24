# Ordinary baseline production: independent source challenge

2026-10-24. Reviewer `module_anchor_audit`; root owns selection, integration,
runtime launches and Git. Canonical root is
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

Scope: fresh producer controller and fixed native-launch worker, then the
separately selected artifact-closure collector when its source is complete.
Only source/evidence-file reads and this Markdown checkpoint are performed.
No imports, tests, native build, owner/database opening or network operation.
Completed baseline syntax/planning controls are not rerun.

## Initial producer review

Read the complete sources against the implementation selection, producer/bundle
contract, actual approved-project grammar, installed authoring profile,
`OperationBudget`, clean-worker predicate and pinned supervisor APIs.

| Source | Reviewed SHA-256 |
|---|---|
| `software/v5/ordinary_baseline/baseline_production.py` | `ab23c20c969bd021aa8e1c2e86dc1793cbbcafb30ffa361a6f66ecf099ac38d0` |
| `software/v5/ordinary_baseline/baseline_worker.py` | `c44d14ec5ddcde8be0952eb7fcd4388b48eae79f44c79fdef187467ee9ca2917` |
| `software/v5/ordinary_project_extraction/library_extraction.py` | `cd79d9050fbc80a94faef845ddf99fe7d1b8ba5e376048aa4a7698f06f396061` |
| `software/v5/ordinary_project_package/ordinary_contribution.py` | `b8eefe6af368d8a7f5c498d563a12b31416c48c877ea471361eadd2a56a90b31` |
| `experiments/v5-local-checks/ordinary-preview-assembly-01/package/installation/supervisor/commons.py` | `6ea16154f4533e80d2e4e27e12fb6fa0ab7abfa0ff2c52cfb7479c1a35a8c1c9` |

The design correctly separates local permission to load the selected project
from mathematical acceptance. The fixed executable and worker roles are bound
to the owner-adopted profile; the loaded extractor/binder helper identities and
installation manifest must agree. The exact fixed inventory and request are
written/read back, passed by exact identities, checked by the worker before and
after the one native call, and rechecked by the controller. The descriptor pin
binds roots/modules only, not transitive project artifact bytes; the source and
documentation say so. No owner or catalog is opened or promoted.

One fresh `OperationBudget` is claimed before work. The selected Job allowance
comes from its original deadline/CPU with the existing cleanup reserve. Native
descendants remain in that same Job; no second allowance or implicit retry is
created. Absent or invalid final native CPU retains the entire finite grant and
stops. Known clean closure requires the actual returned supervisor result and
the unchanged clean-worker rule. Controller CPU checks and final file censuses
are cooperative observations, not hard disk quotas or a hostile-source sandbox.

Fresh derived unit files receive exact length/hash readback. Prepared diagnostic
metadata explicitly does not claim completion; the manifest is the last required
payload, and live return follows its exact readback and final bounded census.
An exception after a manifest-write attempt retains that uncertainty and all
outputs. Saved operational reports cannot replay mathematical acceptance.

## Finding: reserve the native writer ceiling, not the lowered binder ceiling

**Open at initial review.** `required_spool` uses `limits.max_writer_bytes`,
which the caller may lower. The currently selected native exporter and worker
still allow a writer file of up to 64 MiB. The parent applies the lower reader
limit only *after* that file has been written and native execution has closed.
Thus a correct native producer can leave a 64-MiB retained file despite a total
reservation computed from a much lower caller-selected writer ceiling. This is
not an attack requiring a malicious local artifact or racing filesystem.

For example, lowering writer and portable-evidence limits to 1 MiB can authorize
roughly 18 MiB including the remaining maxima/metadata/logs, while the same
native binary may still write 64 MiB before the selected lower limit refuses.
The failure output is deliberately preserved, so it cannot be ignored in the
retained-spool authorization.

The smallest correction is to reserve the **actual fixed native 64-MiB ceiling**
for this producer, retaining lower binder limits as post-extraction acceptance
bounds. Alternatively, pass/enforce a lower limit before native writing, but
that changes the native request/implementation unnecessarily for this seam.
Neither correction turns the final census into a hard during-execution quota;
it merely makes authorization cover the selected producer's legitimate output.

Sent this finding to root and the author. No remaining authority/identity/
closure defect was identified in the other reviewed controller/worker paths.
Final source clearance awaits the correction and exact revised source identity.

### Producer correction reviewed

Root selected the minimal reservation fix. Reread the changed controller at
SHA-256 `0f64bddaa3e106dd8abfe2790158fd94bdf85c6af26e945e04ebbed5f5f72e7d`;
the worker remains `c44d14ec5ddcde8be0952eb7fcd4388b48eae79f44c79fdef187467ee9ca2917`.
`required_spool` now uses the fixed `NATIVE_WRITER_MAXIMUM = 64 MiB`; lower binder
writer limits cannot reduce authorization below the native output ceiling.
The finding is **resolved before execution**. No remaining controller/worker
source blocker was identified. A small changed-boundary inert control may check
the low-writer-ceiling refusal; no old control campaign needs repetition.

## Artifact closure collector: source and runtime-API review

Read complete `software/v5/ordinary_baseline/BaselineArtifacts.lean` at SHA-256
`0bd6e10626b790ec6dd616ca08edbd6786e36dbdcbeddc07bd39ed54f99ff050` and the
relevant pinned runtime definitions of import artifacts, import traversal,
environment finalization and module lookup.

| Runtime source below `software/runtime/lean-4.34.0-windows/src/lean/Lean/` | SHA-256 |
|---|---|
| `Setup.lean` | `eff05a30636e084ecf7c52e4019a1f5497d48b5b023b73f0e979abde91d419a5` |
| `Environment.lean` | `ee364e4788ce0560c87f621eeb3c4c3dfec62e8db4e15e099fd80e6adc533b86` |
| `Util/Path.lean` | `52cf9aa41a82db18d0d3c93bf6257d064f773af9e62b8b43be89ce1b0e00055f` |

For the selected modern layout, `ImportArtifacts` is exactly the nested matrix
`[[.olean, .olean.server, .olean.private], [.ir.sig, .ir]]`. The runtime reads
multipart sequences in order, passing earlier compacted regions to later parts;
they are not interchangeable standalone files. The collector preserves that
layout and refuses missing/legacy parts instead of substituting public data.
It inventories every effective imported module, not merely requested roots,
and retains original direct import flags separately from effective flags.
The runtime's private import mode forces complete imported data and traverses
all direct imports; the code checks that each recorded edge resolves within the
observed census. Its modern-only restriction is material: an ordinary legacy
source without `module` is not qualified by this connector.

Collect mode overwrites `searchPathRef` with the explicit runtime-first roots.
The subsequent locators use the same lookup policy. They remain candidate
locators rather than evidence of byte stability; in particular post-import
resolution could observe changed files. Replay mode first validates the explicit
five-part map, requires each root, then sets `searchPathRef` to empty. The runtime
`loadData` and `loadIR` use a supplied map entry directly; a missing entry invokes
`findOLean`, whose only search input is the now-empty `searchPathRef`. Thus no
inherited path, cwd or implicit runtime fallback can fill an omitted map key.
After import, map-membership checks for each observed module plus equal counts
reject omitted and surplus modules. Exact byte pinning remains the controller's
separate obligation, not a consequence of this set equality.

The collector bounds module/part/edge counts and part/aggregate/report bytes,
checks ordinary file shape and repeated size observations, and emits explicit
nonacceptance assurance. Collect's artifact checks happen after its private
import and are not pre-import resource bounds. Replay checks supplied file
sizes before importing but still needs whole-process containment for parsing,
deserialization and decoded-state memory. Native path checks do not replace
controller ancestor/reparse/single-link checks. Neither size observations nor
the report alone proves immutable artifacts or exact semantic correspondence.

The controller must validate/copy/readback the complete artifact set to a
protected fresh snapshot, perform fresh explicit-map replay, compare selected
roots/direct flags/census and bind exact byte identities before any reference
registration. The separate private/public matcher must still establish the
mathematical correspondence; importing at private level and obtaining a complete
artifact graph does not establish a public reusable interface. Frontend plugin
approval, later executable support and final independent contribution admission
also remain separate premises.

One selection mismatch was raised to root: the source limits collection requests
to 1 MiB but permits replay requests up to 16 MiB, whereas the current written
selection says 1 MiB requests without that exception. Both modes are finite and
the larger matrix may need more bytes, but the selected bound must be explicit.
Root may record a replay-only amendment or retain the original bound for both;
this reviewer does not silently grant the larger ceiling. Subject to resolving
that selection discrepancy, no import-closure/no-fallback source blocker was
identified. No native build or runtime is qualified by this source review.

### Collector bound discrepancy resolved by explicit selection

Reread the implementation selection's appended connector clarification. Root
explicitly selected the separate 1-MiB collect / 16-MiB replay request ceilings
and 65,536 direct-import edge cap. The source-selection discrepancy is resolved;
the collector at the exact hash above has no remaining identified source blocker.
Its native build and actual finite replay remain unexecuted separate gates.

## Snapshot preparer source review

Root separately selected `software/v5/ordinary_baseline/baseline_snapshot.py`.
Read the complete initial source at SHA-256
`f4418c2eef48ae6c4237c66830c78216415cc37e5489da0e1a2a8f13741d1465`.
The helper validates the exact native report schema/default root flags and
approved project descriptor, requires modern five-part artifacts, validates
bounded complete acyclic root-reachable module metadata, and preserves original
module names through an explicit map into derived fresh snapshot paths. It
copies only selected artifact parts, not whole roots. Hash-before/copy/hash-after/
readback checks and metadata-last writes produce an inert prepared snapshot,
not imported mathematics or a protected reference. All partial outputs remain.

The selected spool formula reserves actual validated artifact bytes plus the
64-MiB report/request/manifest maxima; copied bytes are incrementally bounded.
Controller CPU/wall/memory containment remains external/cooperative. Prepared
metadata uses strict 0/1 flags and explicitly says
`PREPARED_NOT_REPLAYED_OR_REGISTERED`. A later native replay and private/public
correspondence must check the complete protected bytes; a locator report's graph
and this preparer's metadata validation are not substitutes for those events.

### Finding: first package-prefix resolution, not first existing full module

**Open at initial snapshot review.** `_first_resolved` searches approved roots
for the first *existing complete module path*. Pinned Lean `SearchPath.findWithExt`
instead selects the first root containing the root-name directory or root-name
`.olean` and only then constructs the full module path. It does not fall through
to a later root when that chosen package lacks a requested submodule.

Concretely, if earlier root `R1` has directory `A/` but lacks `A/B.olean`, and
later `R2` has `A/B.olean`, native import of `A.B` fails at `R1/A/B.olean`. The
initial Python helper would accept a report naming `R2/A/B.olean`, contradicting
its approved-first-resolution claim. It remains inert, but that mismatch matters
to a coherent exact artifact connector and should be fixed before execution.

Resolve the root first using the pinned runtime's package-prefix predicate
`(root / first_component).isDir OR (root / first_component + '.olean').exists`,
then require the full selected path to be an ordinary exact file. A missing or
nonordinary selected target must refuse, not search the next root. Retain the
controller's stricter reparse/ancestry validation. Sent this finding to root,
who owns the implementation. No other source blocker identified in the snapshot
copy, strict metadata, manifest-last or mathematical-authority boundaries.

### Snapshot correction reviewed

Reread the narrow changed resolution helper and recomputed the source identity:
`baseline_snapshot.py` SHA-256
`ab2a0adcdd0b632d14fe2ec7058f9ef496b788760eff4ddd4852d01d11dd3468`.
It now selects the first root with the package-prefix directory or `.olean`,
checks that selected prefix's ordinary shape, and requires the full module file
there. A missing nested module refuses instead of choosing a later shadowed
package. The finding is **resolved before execution**. No remaining source
blocker was identified for this inert prepared-snapshot helper. No actual copy,
artifact replay, correspondence or registration follows from this clearance.

## Producer controls and selector: independent source clearance

Read both complete fresh files and compared their calls to the corrected
producer/controller, installed profile, budget and supervision APIs:

| Source below `software/v5/ordinary_baseline/` | SHA-256 |
|---|---|
| `production_controls.py` | `1f46b82621c9fd6e9dd8000b8ae7eb92f815191f30fca4e17064bccbe32008a2` |
| `select_production_controls.py` | `2ea48937ce7949daf6900cbbf36bbeefdb475b246dd1c450777ab171f35f9e4c` |

No source blocker identified for the ten selected **producer-controller** cases.
They exercise the new controller boundary, not a repetition of the completed
24-case binder/intake campaign. The harness uses actual code/profile/pin/grammar/
budget/binder/file-write functions, but explicitly supplies synthetic module
locations, an inert executable-role file, a native-response double and no real
Job/native worker. This is not a test of native launching or compiled export.

The cases cover insufficient default spool, lower binder limits still requiring
the actual fixed native writer reservation, missing executable role, changed
worker pin, one clean exact produced bundle, unknown CPU, a thrown supervisor
with no accounting, unclean event without writer access, clean event with missing
writer, and a failure after exact manifest write. Four preflight cases require
no native-double call and no destination/output. Unknown outcomes retain the
whole grant; known simulated CPU is explicitly marked simulated. Output tests
require exact held unit bytes, manifest-last required payload order, saved
`PREPARED` rather than success metadata, and truthful late-manifest uncertainty.
The failures preserve files and deny automatic retry.

The actual profile verifier runs over a deliberately synthetic support map;
patched `__file__` locations do not pretend to be a real installed product.
The harness does not import the worker as an execution substitute. Forbidden
mocks cover subprocesses, sockets, database connect, owner/native operations,
catalog promotion and custody writes. Known frozen loader/support reads happen
before these mocks; they do not open an owner. A single bounded saved result
remains nonacceptance evidence and explicitly excludes native build/execution,
installed-profile qualification and admission.

The selector pins exact new controller/worker/binder/harness files, the three
retained syntax fixtures and unchanged frozen package/runtime inputs, plus the
selector and outer runner. It selects a fresh distinct output name and original
60 wall / 35 CPU seconds, 768 MiB, two-active-process envelope; internal controls
retain 45 wall / 25 controller CPU. It carries no prior state or allowance.
Only root may select and launch the actual bounded run, then separately adopt
its saved outcome. This review performs no execution and does not qualify any
unimplemented native-correspondence continuation.

## Saved outcome audit: producer-controller controls01

**PASS for the selected ten producer-controller controls with an inert native
double.** Read the complete saved outer/result/command reports and rehashed all
156 selected runtime inputs and six immutable source snapshots: zero mismatches.
The copied and selected selection files agree exactly. The current package,
held proof-data fixtures and used producer/worker/binder/harness/selector bytes
remain unchanged. No script, control, native binary or owner was executed by
this audit.

| Artifact below `experiments/v5-local-checks/` | SHA-256 |
|---|---|
| `ordinary-baseline-production-controls-01.selection.json` and copied selection | `4f4d521d75e2824a1942d20d1f39ef50a366cc30090b7d010bad1aed42bac6a6` |
| `ordinary-baseline-production-controls-01/RESULT.json` | `6b1ce2e340ff09149d6ef0a5315ebc8efff86089dcfe2718c204b1e53571254a` |
| `ordinary-baseline-production-controls-01/controls/RESULT.json` | `6b0401a0c02baa613a8d12e44e5632b64c3d16dd64f3968d529b494d30e3c547` |

All ten cases have their selected expected outcomes. Four preflight refusals
have zero native-double calls and no payload writes. Each remaining case makes
exactly one native-double call with the original finite allowance. Unknown CPU
and a thrown supervisor retain the entire 18-second **simulated reservation**,
with null observed native CPU and honest closure-known distinctions. The
unclean-event case stops before trying to read its missing writer; the clean
event with missing writer stops in binding instead of presenting output.

The clean case's three materialized units independently match every manifest
length/hash, and the saved manifest has hash
`b8ac554f2c6add44da9222092735fba82c04028e8085bb49bcc70523122f3da7`.
Its directory has exactly 14 files totaling 906,296 bytes, matching the returned
census. Saved `PRODUCTION.json` remains
`PREPARED_FOR_MANIFEST_WRITE_NOT_COMPLETION`; no failure file exists. The
late-manifest case retains the same exact manifest/units plus its truthful
`FAILURE.json`: 15 files, 906,821 bytes, `manifest_write_attempted` and
`manifest_may_exist` both true. Its saved prepared metadata does not conceal the
failure. No retry, rollback or acceptance is asserted in either outcome.

No forbidden operation was called. The report explicitly marks native CPU
charges as simulated, excludes native worker/exporter build or execution,
installation and admission, and retains `mathematical_acceptance: false`.
Real files, hashes, profiles, codec/binding and budget code were exercised; the
native executable filename contains inert fixture bytes and was never launched.
Do not count the simulated grants as actual experiment CPU consumption.

The actual outer operation exited zero, reaped the direct child, observed zero
active/terminated Job processes, closed the Job and recorded no cleanup errors
or termination request. Actual logs are 83 stdout bytes and zero stderr bytes.
Observed outer elapsed time is **4.119646300096065 seconds**; actual known child
Job CPU is 2.875 seconds and wrapper CPU is 0.53125 seconds, totaling
**3.40625 known CPU seconds**. Peak reported Job private commit is 115,982,336
bytes. The internal 3.3427234-wall/2.765625-controller CPU measurements are
contained within that operation, not extra costs. The selected limits remain
60 wall / 35 CPU seconds, 768 MiB and two active processes.

Root's current desk separately records an earlier selector argument rejection
for an uppercase hash character before output creation. The selector's source
validates those arguments before creating a selection/output; the corrected
lowercase argument did not require source mutation or a control-run retry.
The costs above describe the single saved control execution, not every prior
shell invocation. No failed experiment is relabeled or discarded by this audit.

This completed seam should not be rerun. Native exporter/worker qualification,
artifact snapshot replay, live exact correspondence and protected registration
remain separate unfinished gates; the full v5 objective is not complete.

## Snapshot controls: independent source clearance

Read complete `snapshot_controls.py` at SHA-256
`c45e7bfd87da85cfd97a7aaaf363d9cbe30c891566a0d8fc6f483375a54189b6` and
`select_snapshot_controls.py` at SHA-256
`2e019c8ebd814c49ce2b7e8371e2c31b23e51993759345b2a9533514133276c7`, against
the reviewed snapshot helper `ab2a0adcdd0b632d14fe2ec7058f9ef496b788760eff4ddd4852d01d11dd3468`.
No source blocker identified for the selected ten synthetic-artifact controls.
No test was executed during this source review.

The positive case uses a four-module, twenty-part deliberately inert fixture and
real graph/path/hash/copy/metadata functions. It checks exact source preservation,
all copied bytes/pins, dependency-first output order, original names/direct and
effective flag preservation, explicit replay matrix, aggregate counts/bytes,
exact metadata identities and prepared-manifest-last ordering. Synthetic flags
exercise serialization/preservation; they do not establish that native private
import actually returns those flags. No fixture artifact is deserialized.

The eight before-copy refusals address the corrected earlier package-prefix
shadow, changed source length, existing but unapproved part, raw dot components,
missing dependency, extra unreachable module, import cycle and insufficient
metadata reservation. Each requires no snapshot output directory. A distinct
same-length mutation between first hashing and copy must fail exact copy
validation, retain the partial file and leave all three metadata files absent.
Only that fresh fixture is intentionally changed; completed evidence is untouched.

The harness forbids actual subprocess/socket/database/native/owner/promotion/
custody calls and labels itself nonacceptance evidence. Its installed loader is
used only for unchanged support/codec reads. The selector pins the exact fresh
helper/harness plus frozen package/runtime support, selector and outer runner;
it does not import former state or reuse an allowance. Proposed outer limits
remain 60 wall / 35 CPU seconds, 768 MiB and two processes, with internal 45 wall /
25 controller CPU. Root alone may select and launch this distinct bounded run.

## Read-only warrant-to-request adapter

Read complete `reference_request.py` at SHA-256
`a4cadb4beb75bdf86b7314a2c05e301cbbafd42da8500ccd524c82c7a7503923` against the
selected contract, actual `PortableCatalog.context`, portable V2 evidence parser
and frozen binder census helpers. No source blocker identified in the controller
request-preparation boundary. This is not a review of the new matcher's
mathematical private/public relation, assigned independently elsewhere.

The planner requires the actual admission-owner type and shared codec identity.
It asks that owner's current protected catalog for the selected context and
requires exact current semantic/foundation identities. It reads the exact fixed
581-name inventory, recomputes each basis symbol and verifies current context
bindings. Every bundle file must match its manifest raw size/hash and current V2
UnitID. Every complete output must equal that context's actual export identity;
mere bundle or custody presence is insufficient. A fabricated evidence unit
with the same output name but different UnitID therefore cannot become warranted
through name matching.

The exact portable parser establishes the complete import census, including
proof-only references. Each import is checked against current context bindings
and must resolve either to the fixed basis or a selected complete supplied unit.
An already-warranted but unselected private dependency still refuses. A fresh
topological ordering covers all units; cycles refuse. Explicit unique target
name/export pairs must belong to this full selected private set. No private-only
name is thereby promoted to the public interface; that separate decision belongs
to the actual-public-view matcher and later protected registration.

Frozen manifest/per-unit/per-batch and aggregate byte/node/name/edge/binding
bounds remain in force. The helper adds a 64-MiB bare-unit array bound, 1-MiB
target metadata bound and 96-MiB whole-request bound. It materializes the full
selected request, so it is not a streaming or constant-memory operation. Its
check callback must charge the original enclosing operation, including protected
context validation and final serialization; outer process containment is still
needed where hard CPU/memory limits matter.

Snapshot and support hashes are syntactically validated **labels**, not proofs
that the referenced files/support were authenticated. The caller must keep the
actual owner open and serialized through live matching/registration and validate
the snapshot/support separately. The return has no catalog commit, mutation,
native call, acceptance promotion or transferable warrant. Reusing a saved
request cannot replace those lifetime premises. Final native schema/label/census
compatibility must be checked against the completed matcher before any runtime
integration; this source-only adapter clearance does not preapprove that future
boundary or settle the separate mathematical soundness audit.

## Snapshot controls: saved-only independent outcome audit

Disposition: **PASS selected real snapshot path/graph/hash/copy controls with
inert synthetic artifacts**, not native import, mathematical correspondence,
registration or acceptance. Independently read the saved outer result, command
record/log and complete ten-case result; rehashed all 151 runtime pins and four
saved source snapshots against the exact selection, also checking the four
current source files. Zero mismatches. Selected and copied selection bytes agree.
No test, native import, build, owner or database operation was run by this audit.

| Artifact below `experiments/v5-local-checks/` | SHA-256 |
|---|---|
| `ordinary-baseline-snapshot-controls-01.selection.json` and copied selection | `371cdd5432c9ea9171491401034effbc9b795cabd2ff2a910ee1f88198d9c80b` |
| `ordinary-baseline-snapshot-controls-01/RESULT.json` | `34b4a1e4326a061ea6f7296bfe2f09584943f5286a06b7a4cdbde0e4b596cdc0` |
| `ordinary-baseline-snapshot-controls-01/controls/RESULT.json` | `4618a9e82b7f7eb8c7b52dd1c7bcd2a564f114fc25794da4beef9a3cf3cf6883` |

The positive snapshot has exactly four modules and twenty copied artifact parts,
822 artifact bytes, and 23 total files totaling 22,336 bytes. Each copied path
stays inside the exact fresh prepared directory; each copied length/hash matches
its manifest pin and the original fixture part. Module identities, direct import
flags and effective flags match the source report; replay module identities and
the explicit two-group part matrices match the manifest. The prepared manifest
SHA-256 is `b0755f72abc27757e3407d33ff263e4929807e2fde031e84731ed64f7aa99ac9`.
Its source-report and replay-request hashes independently match
`e1692bad0bbf43588461bf2632e0b10f0f97045662509347c67810a5f5e0d230` and
`33333f33eca01787a2ef68fc10ad8df3ff207f29b6b492c6d7ed430c99b1563a`.
Status remains `PREPARED_NOT_REPLAYED_OR_REGISTERED`, with false mathematical
acceptance. Flags in this synthetic fixture are serialization evidence, not
evidence about actual Lean import behavior.

All eight before-copy negative cases have no prepared output directory: package
prefix shadow, source-size change, unapproved location, raw dot component,
missing dependency, unreachable extra module, import cycle and insufficient
spool reservation. The copy-time same-length mutation case retains exactly one
38-byte partial copied artifact and no source-report, replay-request or prepared
manifest. Its retained copied bytes and deliberately mutated source both hash to
`6663e77ef71f53f407f918feaecf1033df9fc7db93dc4c82094b15a87de33a51`, distinct
from the saved premutation pin. This is an honest refusal with retained partial
output, not an atomic-cleanup or completed-snapshot claim. No forbidden operation
was called. All twenty positive fixture artifact parts were inert bytes, never
deserialized by a native importer.

The actual outer operation exited zero, reaped its direct child, observed zero
final active and terminated Job processes, closed the Job and saved no cleanup
error or termination request. It observed two total Job processes. Logs contain
93 stdout bytes and zero stderr bytes. Outer elapsed time was
**2.2836732999421656 seconds**. Known child Job CPU was 1.09375 seconds and
wrapper CPU 0.53125 seconds, totaling **1.625 known actual CPU seconds**. Peak
reported Job private commit was 60,780,544 bytes. Internal 1.5178261-wall and
0.96875-controller CPU measurements are contained costs, not additional charges.
The selected limits remained 60 wall / 35 CPU seconds, 768 MiB and two active
processes. No passing run is repeated or old budget renewed by this audit.

This closes the selected snapshot helper's changed-boundary controls. Actual
collector build/import, immutable snapshot replay, kernel/public correspondence
and protected reference registration remain separate unfinished gates. Snapshot
hashes do not authenticate mathematical meaning or create a reusable warrant.

## Scope still unfinished

This source review is not a producer build, installed-profile qualification,
native extraction, protected baseline admission, A2 correspondence or public
ordinary-library reuse. The unchanged deployable-v5 goal remains unfinished.
Artifact closure and exact private/public correspondence are separate boundaries;
neither can be inferred from this producer's descriptor hash or inert result.
