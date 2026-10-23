# Missing-library completion: independent focused review

2026-10-23. Reviewer: `admission_event_audit`. Canonical workspace guard passed.
This assignment is source/theory only. No build, compiler, test, native worker,
catalog write or Git action is run by the reviewer.

## Decision in principle

**A finite missing-library completion pass is justified. The native CLI, narrow
build, extraction and combined-admission sources below have no blocking finding.
Actual extraction and the later combined receiver acceptance both succeeded.**
Consumer05 already emitted its complete five-unit
candidate; the accepted parent lacks exactly `List.map_congr_left`. Repeating
owner construction/elaboration will not supply that proof. Adding its name as
a trusted axiom would break acceptance. The appropriate new work is to obtain
complete supplementary units and check them with the original candidate.

The proposed short-lived native helper imports the selected trusted installed
library privately, exposes actual proof-bearing records, and uses the existing
inert exporter to traverse only missing units. It asks the protected controller
whether a reached name is already in the actual accepted context. A positive
answer cuts old proof traversal; a negative answer requires a complete local
record or refuses. One environment suffices, and candidate05 is not re-elaborated.

This is preferable here to rebuilding the consumer source, supplying every
parent binding to its authoring environment, or introducing a permanent database
service. All-parent transfer buys nothing that finite on-demand lookup cannot
provide. Direct database access inside Lean would duplicate existing protected
context logic and broaden the seam. A bounded local pipe is an implementation
of point lookup, not a network protocol or a new authority.

## Concrete challenges sent to author and root

- Import only the needed installed owner module, not the umbrella `Std` if
  unnecessary. The successful consumer already used the missing lemma under
  `Std.Data.ExtHashMap.Lemmas`; its selected private import closure is sufficient
  in principle. An explicit finite installed-module selection generalizes this
  without importing all local packages. Availability outside those modules is
  not promised.
- Reuse the four retained lower native helper objects. Current exporter source
  is public-module code, whereas the old native artifacts predate that wrapper.
  Do not mix unrelated signatures and objects. The author's proposed exact
  header-only legacy codegen view of the changed scheduler, against matching old
  lower `.olean` artifacts, avoids the known module-import incompatibility.
  Only the scheduler and new main then need codegen/linking. Source-body equality
  and the exact dependency map must be checked; an actual successful link is
  still a later build result, not assumed here.
- Keep stdout exclusively protocol-framed and diagnostics on stderr. Bound
  frame allocation before parsing, not after an unbounded `getLine`. Bind each
  response to schema, sequential query identity and exact original name. One
  outstanding request simplifies state. Bound lookup count, frame bytes,
  aggregate transcript bytes and process resources; reject malformed/extra
  responses, EOF and incomplete final handshakes. No automatic retry campaign.
- The requested missing set and selected profile/context must be exact. The
  controller resolves lookup answers from the same actual protected K, never
  from untrusted candidate claims or an authoring `.olean`. Query memoization
  may cache negative as well as positive answers within this immutable K.

## Crucial combined-admission invariant

Supplementary outputs are **not accepted K bindings** merely because the helper
exported them. Do not insert them into the prepared map or fabricate a changed
accepted parent. Instead:

1. Preserve the original candidate bytes and their 37 explicit accepted-ID
   claims, still checked against both prepared identity and actual K.
2. Derive supplementary unit envelopes in dependency order, resolving imports
   in K or earlier supplementary units and deriving their exact new output IDs.
3. Resolve the original unresolved names in K or those earlier supplementary
   outputs. Then derive the original five units' envelopes in their old order.
4. Reject collisions with K, duplicate new outputs, overlap with the original
   consumer outputs, incomplete generated groups and forward dependencies.
5. Submit **all** supplementary and original units to the unchanged checker
   under K. Only its actual clean event can commit the combined extension.

The origin of the missing record is not a trust premise: complete proof-bearing
units are checked under receiver meanings. Failure to recover a full installed
record is an availability outcome, not permission to admit an axiom-shaped view.
Root owns the exact controller/source selection and any later runtime.

## Native CLI source reviewed

Read complete `software/v5/ordinary_lean/MissingImportExporter.lean`, SHA-256
`7efb8bfa768a97ebcced687fd2a5acb0227e65eb2260e82d1726d8f361b27fbb`.
**No blocking source finding for this CLI/build seam.** This disposition was
sent immediately to root, separately from this written checkpoint.

The request has exactly schema/profile/context/basis/modules/targets fields.
The request is bounded to 1 MiB before parsing, including token/depth/UTF-8
checks. Names are decoded under existing policy and duplicate-checked; the
module set has at most 16 Std-prefixed names and target set at most 1,024.
Identity fields have the exact lowercase 64-hex shape. The protected controller
must authenticate canonical selected request bytes and actual installed files;
the Lean parser alone does not establish their authenticity.

The process sets the search path to the selected sysroot library directory,
imports the selected modules once with private records, no plugins and no
extension loading, and uses that sole environment. Every target must have an
actual safe non-axiom record and must be absent from K. The shared scheduler
then demands complete new units, bounded to 1,024 units and 2,097,152 scan nodes,
with its earlier group and byte bounds intact. It can fail if required source
records or semantics are unavailable; it never substitutes a trusted axiom.

Each synchronous LOOKUP carries an increasing sequence and original encoded
name. Exactly one reply is read, byte-bounded before parsing, with matching
schema/sequence/name and exact FOUND-or-ABSENT field set. FOUND additionally
requires an exact symbol-ID shape. The callback caches `some id` and `none`,
and the scheduler also memoizes stop decisions. There is no reentrant callback
or controller-owned service inside Lean. The 65,536-query and 32-MiB combined
protocol budgets include both directions and outgoing final frame. LF ends a
reply; CR, premature EOF and excess frame bytes refuse. Blocking-read time is
bounded by the enclosing nonrenewing process supervisor, not by this reader.

Only actual stopped reference names become output boundary imports. The output
schema is distinct, marked inert, with complete supplemental units and exact
lookup/statistics fields. A fresh output is written before DONE. This is safe
only because neither file existence nor DONE grants acceptance: the controller
must bind the file and wait for clean process completion. The final stdin-EOF
handshake rejects trailing unsolicited reply bytes. Progress and bounded errors
go to stderr, leaving stdout for protocol frames.

## Build and extraction-controller source reviewed

Read complete root-authored sources:

| File under `software/v5/ordinary_lean` | SHA-256 |
|---|---|
| `run_missing_import_build.py` | `392361a58980e924f9fda633885ab0c83313bce22804d5fb1d56453d89bd93b0` |
| `run_missing_import_completion.py` | `9f39ea1a9cdb3d645200b16f2ee7ab4e1c38d638c07b383010bc785d8d9d5f4a` |

Also read the complete author plan `MISSING-IMPORT-COMPLETION-PLAN.md`,
`49992eed32c019f06f229bbcff29192f539fdc5134d29629c9fa7c6d5e01a4f6`.
**No blocking source finding for the selected local build/extraction seam.**
The result remains inert supplemental data, not admission.

The build uses a fresh selected directory. It checks four retained pairs,
copies only their exact `.olean` interfaces and links their original `.o`
objects. The current reviewed exporter contains exactly the expected initial
module marker, three public imports and one public section marker: its generated
legacy view removes/changes only those wrappers, retaining the other bytes.
Only that exporter and the new main are compiled. The build environment clears
inherited Lean/Python variables and uses the fresh matching build directory;
all compiler subprocesses share one internal deadline, within outer Job bounds.
This is not a general transformer for arbitrary Lean source. Actual emitted
view/body identity, object map and compile/link success are later saved evidence.

The extraction controller uses immutable/read-only SQLite, not product catalog
opening, to load the exact four-root adopted parent. Database SHA is pinned
before/after; roots, profile, basis, record sizes and 3,622 unique bindings are
checked. This is bounded local materialization, **not** an asymptotically improved
global catalog. Only reached name queries cross the native pipe. The exact
candidate and executable are pinned, and the whole genuinely missing set is
derived before starting native work. The request selects the narrow installed
`Std.Data.ExtHashMap.Lemmas` module, not umbrella Std.

The pipe uses two readers, one writer and bounded queues. Stdout's `readline`
has an explicit preallocation limit; stderr has a total byte cap and cross-chunk
PANIC detection. The controlling thread does not block on native reads/writes:
event waits and queued writes consume the same 100-second deadline. Parsed
queries require exact fields, sequential integer IDs and distinct validated
names. Replies derive solely from the protected parent map. Combined outbound
and inbound protocol bytes are charged. DONE must match actual processed query
count and finite unit/file bounds; only then is stdin closed. Additional stdout
frames or premature EOF refuse. Both pipe EOFs, zero child exit and joined
threads are required. On error the direct child is killed/reaped; the existing
outer Job owns whole-process-tree settlement and the overall resource ceiling.

The actual output size and schema/profile/context/basis/targets/unit count are
bound to request and DONE. Boundary IDs must match both the recorded lookup
answers and K; all selected targets must have been queried and found absent.
Candidate and original database hashes are rechecked. Outer `Run-V5-Check.py`
additionally verifies every selected runtime pin and immutable source snapshot
after process completion. Failed/leftover output cannot constitute accepted
mathematics. The source-only claim is scoped to the trusted operator-selected
local runner, not a public hostile-code sandbox.

Root still owns selectors and any actual operations. The optional combined
supplement-plus-candidate admission source is separately assigned to the author
and remains pending review. Do not rerun successful library, consumer or
baseline-verifier tests to establish this narrow new behavior.

## Selector source and installation assumption

Read complete `select_missing_import.py`, SHA-256
`7a84c4f7e6d6e3360812ab5adba3dd4fb3b2e3a34ca445cdc0485f879c091c94`.
No blocking finding for an operator-selected completion after the actual build
is inspected. It binds all eight retained lower artifact hashes explicitly,
checks the old successful selection, and makes fresh immutable operation names.
Completion requires a successful new build and binds its executable byte count
and digest, old checking-helper source identities, exact parent database and
exact consumer05 bundle. It does not execute the operation. Both modes receive
finite 120 CPU / 150 wall / 1,536 MiB envelopes.

**Installation precision:** the selected pins include runtime binaries and link
libraries, but do not include a transitive hash manifest of all installed Std
`.olean` and private artifacts. The current assumption is a trusted fixed local
Lean installation with explicit selected runtime pins, not a fully hermetic or
individually hash-authenticated installed-module closure. The earlier plan's
"pinned installed library" wording must be read with this limitation. The
reviewer reported this directly; it does not justify an expensive unrelated
closure-pin campaign for this local discriminator. Those installed records
supply only candidate data: complete supplementary units must still undergo
the unchanged independent receiver check. Public distribution/update integrity
is a separate unfinished requirement, not established by this selector.

## Actual build01 and completion01: saved-evidence audit

Root selected and ran these operations separately. The reviewer inspected saved
files only, without rerunning either operation or invoking product catalog code.

| Operation under `experiments/v5-local-checks` | Selection SHA-256 | RESULT SHA-256 |
|---|---|---|
| `ordinary-missing-import-build-01` | `aa2386b506ee91467b97dc7e92b5183160701eb0b955b07fa51b099f7bf01b60` | `a3b8e5200c94ab8d39729ebea871110ec00d7dae47de5c5bc0c04f768c8301b7` |
| `ordinary-missing-import-completion-01` | `80ff619253b886ed18b2698056ccfc4622c2949118af26551c19a729181acc68` | `5b238410df569886f91c7afe2ffb3def71f7085d73725a5528eefe7a23df816c` |

Build01 matches all five snapshot source hashes and 33 runtime pins. Its five
steps (two codegens, two object builds, one link) exited zero; all ten native
logs are empty. Independent byte reconstruction confirms that the emitted
legacy source is exactly the reviewed header-only transform, that all four
copied interfaces equal the retained interfaces, and that the emitted new main
equals the selected source. The transformed source hash is
`3e046d40150127fa1d480b1f4a678dea47a93353eb67b01c542b9ea3df2dcedc`.
The executable is 697,344 bytes, hash
`9700c6c2944d327a648e3fcf83453ee1aa019d2f05c182feec13e78211711dc7`.
`BUILD-RESULT.json` hashes to
`c43944dcc9876b2250c00d58717f12151f16a8833a5b95ea0f58d9184921a194`.

Build01's outer result has zero exit, clean direct-child reap and Job closure,
no errors/termination, and zero active/terminated processes. Job CPU 4.625 plus
wrapper CPU 1.0 gives **5.625 known CPU seconds**; wall 7.9360583 seconds, peak
Job private commit 624,959,488 bytes. The retained lower helpers and installed
Lean/Std were not rebuilt.

Completion01 matches all three snapshot source hashes and 32 runtime pins.
Its stderr contains only the expected import-start, import-completed and
two-unit-closure messages. The saved request selects the exact missing target
`List.map_congr_left` and `Std.Data.ExtHashMap.Lemmas`. Request hash:
`c98759a50a5bedee293d5d1034a377e15de54660c8b56bc131ec13e89926c467`.

Independently parsed **all 34 query/reply pairs** and final DONE. Sequences are
exactly 0 through 33, names echo exactly without duplicates, and every FOUND ID
agrees with an immutable read-only query of the actual K. ABSENT was returned
only for `List.map_congr_left` and its needed helper `List.map_inj_left`. All
32 supplemental boundary IDs agree with both the transcript and K. Combined
protocol length is 11,694 bytes, matching the saved result. Transcript hashes:

- stdout: `9964c458e08f11c2f965c613402fcdf8f65fd98375eaeed538884d24ff7888df`;
- stdin: `b2d168e8bf9dc11d9582e9794e4da787b4ab1ccd95e3cd1646a6c7e419d55898`.

The supplement contains two complete candidate units in order,
`List.map_inj_left`, then `List.map_congr_left`: one dependency edge, 1,122
scan nodes, zero source census, 31,480 unit-JSON bytes and 36,382 bundle bytes.
Bundle SHA-256:
`73e006866ae3435ee35a014fde9b412326e18f1130089353ba098e335a3390af`.
`COMPLETION-RESULT.json` SHA-256:
`f026af3c40f2c167c6cd45638c37adc42d04bc4db8cb75aff1be51476314f52d`.

Completion01's result has zero exit, clean reap/Job closure, no cleanup errors
or termination and zero active/terminated processes. Job CPU 0.859375 plus
wrapper CPU 0.9375 gives **1.796875 known CPU seconds**; wall 3.6365145 seconds,
peak private commit 270,876,672 bytes. The original candidate is still exactly
`a7f6f86b...`; original database hash before/after independent lookup remains
`bcb94ff9695f4d360205eaf8f81151f1cf70437c0e6c434b48f6993d893980e9`.

**Extraction succeeds; supplementary mathematics is not yet accepted.** The
next concrete boundary is one seven-unit independent receiver operation (these
two plus unchanged consumer05's five) after combined-source review. No missing
set remains in this extracted finite closure. Costs above exclude the earlier
consumer, original library adoption and other accumulated work; they are not a
whole-system growth or speedup comparison.

## Combined admission: exact changed-source review

Read the complete changed planning/input seam and unchanged worker-to-commit
seam, plus its file-only selector and focused pure controls:

| Source | SHA-256 |
|---|---|
| `software/v5/ordinary_lean/run_successor_admission.py` | `82a6e63038eff7d74f399bcea87332e0eb771a2dcd86a6f488214ab5a04bfeef` |
| This cycle's `Select-SuccessorAdmission.ps1` | `a69d8b8e4569512d3e2b8f3eb8a732897a3f98d805fcb69630378a86f913cadf` |
| `software/v5/ordinary_lean/combined_admission_checks.py` | `a2338b86888afac1d4199fda725b76dee3be91e0a64908e22bcb177061a3b783` |

**No blocking source finding.** The existing strict resolver remains available:
it partitions all names, then still refuses any missing set when called without
supplementary support. Existing explicit prepared/parent claim checks do not
become optional. The old exact successor schema remains distinct and does not
silently gain missing-name or supplementary authority.

The optional supplement must match schema, assurance, profile, parent and basis.
Its target set must be distinct and **exactly** equal to all genuinely missing
candidate imports. A needless supplement refuses. Supplement boundary claims
resolve only in actual K; unlike original acquired claims they need not appear
in the preparation map. This is necessary for newly discovered proof support,
not a relaxation of the original 37 acquired claims.

`successor_envelopes` has separate supplemental and original-candidate lanes.
Each unit is syntactically censused and gets exact canonical imports from K or
earlier units in its lane. Supplemental outputs get provisional content-derived
IDs in a new-unit map only. At the lane transition, the original candidate sees
its already-resolved K imports plus **only its declared missing names** from
supplementary outputs, not every incidental supplementary name. Every original
raw unit remains unchanged. All emitted names are checked against K and a
shared new-output set, so parent overwrites and cross-lane collisions refuse.
Forward references refuse, the missing outputs must actually be present, and
the final requested target must originate in the original candidate lane.

Counts, aggregate input bytes, node/evidence/stream bytes, emitted names and
per-lane unit byte statistics are bounded jointly. Per-lane byte checks occur
after its last yield, but the real controller **fully exhausts the generator**
before taking a catalog reservation. A late refusal can leave inert diagnostic
files, never a native call or a partial commit. Opening `units.json` before
generator iteration is consequently not an acceptance or trust transition.

The controller still copies/verifies the exact original store, reserves once,
calls the unchanged pinned native worker on all complete units under the same
parent, binds the actual clean exit/report/names/artifact to that live grant,
and only then privately commits and reopens exact final bindings. Both original
and supplement file identities appear in the saved plan/result. No separately
accepted supplemental prefix is manufactured. Original K remains untouched.

The selector's optional absolute local `supplement.json` must match a clean
completion result bound to this exact candidate and parent; its request and
result/selection/bundle bytes are pinned. This provenance supports the selected
local workflow but is not a mathematical acceptance premise: the actual new
unit check remains mandatory. The no-supplement invocation stays supported.

The 16 pure control groups call only `successor_envelopes`, never its runtime
main, filesystem or catalog. Before runtime selection, the reviewer checked
their one-constant root-last DAGs, JSON-list rows, definition/inventory formats,
hint shapes and expected refusal markers against the real evidence parser.
They cover correct provisional-ID use and original-unit identity, no/unneeded
supplement, old exact route, exact missing targets, wrong K/original claimed
IDs, forward references, parent/cross-lane collisions, absent target output,
undeclared incidental support, late byte checks, joint count, final-target
origin, context/assurance and lookup-count bound. Input nonmutation is checked
on success and refusal, including partial-yield refusals. They have not been
executed by this reviewer; root selects their one finite execution separately.

## Later actual closure

Root subsequently ran the 16 controls once and one actual seven-unit combined
admission. The saved-evidence audit is in `CONSTRUCTION-RECIPROCAL-OUTCOME.md`:
controls pass; all two supplemental and five unchanged consumer units were
checked by the retained native receiver and committed in a fresh store copy as
root `98e65adcb09061a78dd3088a4bbf966b9ac1cee9f98da6f8fbcdb410f3edf7b9`.
The original store remains unchanged. This closes the selected missing-import
and reciprocal-admission experiment, not the global v5 objective. No rerun of
these passing operations is indicated.
