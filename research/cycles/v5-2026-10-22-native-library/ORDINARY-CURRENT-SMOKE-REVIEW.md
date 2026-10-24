# Current-distribution relocated smoke: independent source review

Reviewer: `return_actual_audit`, 2026-10-23. This is a separate source-only
review after the completed current-build saved-outcome audit. All paths are
under the canonical root, and the project guard passed on resumption.

## Current decision: HOLD before staging or execution

The newly built package cannot satisfy the planned `extract-std` operation as
currently assembled. This is a source/data incompatibility, found before a
smoke selection or launch, not an observed native extraction failure.

The installed `authoring/py/library_extraction.py` is byte-identical to
`software/v5/ordinary_library_support/library_extraction.py`, SHA-256
`5a71037c38513eb84e588ec571d7cddded316f3eb4561c31bc46c50f72a8f683`.
At lines 26-27 it requires the old executable SHA-256
`9700c6c2944d327a648e3fcf83453ee1aa019d2f05c182feec13e78211711dc7`
and size 697344. At lines 147-151 it first requires the exact selected
`(executable, size, hash)` tuple in `profile.file_pins`, and then independently
rereads the executable against that same historical constant.

The new package's actual executable has size 697344 and SHA-256
`77eede87b83b2c3636d5c1a40e24e0d78dcdfaf38f5961cf357bb2dd7a7c911a`,
as already verified in `ORDINARY-CURRENT-BUILD-REVIEW.md`. Its actual
`PROFILE.json` selects this new hash. The current `profile.py` constructs
`AuthoringProfile.file_pins` directly from its verified profile records; it
does not override either extraction constant. Thus this package's public
extraction path necessarily fails `EXTRACTION_SELECTED_EXECUTABLE` before
launching its newly built extractor, even if preceding smoke steps pass.

Root and the source author were notified immediately. No frozen used source,
package, profile, build evidence or old executable was modified. A fresh
explicit source/assembly successor decision is required; silently substituting
the old executable, relaxing the smoke to skip extraction, or changing the
used build result would not answer the selected boundary.

The previous audit's build/assembly/count/hash/process-closure findings remain
valid. They were not a behavioral-equivalence or relocated-use qualification.
The executable-byte difference was explicitly retained as an actual-use gate;
this review identifies a concrete compatibility failure at that gate.

## Sources inspected so far

- `software/v5/ordinary_distribution/select_relocated_smoke.py`:
  `62a14a9eae52bf73cce782f8de7460cd386fbe0446611a74c91b3da1d8f3ecca`.
- `software/v5/ordinary_distribution/relocated_smoke.py`, first draft read fully:
  `717265a5c06457a1c6cedc29a77c626303c1cae636e3df87d69b05225e262826`.
  The author explicitly reports this is not final and is correcting the basis
  admission assertion: 456 checked basis units and 581 inventory names, with
  no retained extension unit IDs. No clearance attaches to this draft hash.
- The current source map, installed profile/manifest, public owner/profile,
  extraction and completion paths, supervisor status semantics, native worker
  report schema and prior saved source designs were inspected as inert files.

## Selector review to date

The source-only selector has no identified independent blocking defect. It
requires isolated Python in the canonical cwd, hashes its unchanged base
helper and current source map, and accepts explicit selected profile/harness
hashes. It requires fresh relocation, receipt, selection and future-run paths.
It constructs the exact 126 runtime payloads from 98 auxiliary records, the
installed non-runtime records and manifest, then adds `PROFILE.json` for 127
files. Original, copied and post-copy original hashes must match; exact final
file census excludes `_build`, owner state and earlier theorem outputs.

The runtime selection is expected to contain 127 copied payloads, 9 installed
runtime pins, 14 additional named native-toolchain pins, 5 specifically selected
`Std/Data/Internal/List/Defs` companion parts and the relocation receipt: 156
pins. The three source snapshots are runner, selector and smoke harness. These
are named file pins plus the declared full-runtime premise, not hermetic
toolchain authentication or an OS filesystem-denial claim.

An independent inert JSON census confirmed 98 auxiliary records, 27 installed
non-runtime records, 9 installed-runtime records, 14 additional named runtime
records and zero overlap between the two runtime sets. The 156-pin calculation
is therefore exact for this selected map, not an assumed upper bound.

The selector passes fresh `{output}/smoke`, 360 wall / 240 CPU seconds and
1536 MiB native limits inside 420 wall / 300 CPU seconds / 2048 MiB / eight
active processes. The design prose's earlier prospective 300/180 and 330/210
numbers are not authoritative; the author was asked to reconcile them with
root's selected source envelope.

## Harness review to date

The draft uses only hash-verified supervision helpers from the relocated
installation; it does not import product helpers from the source checkout.
It derives the actual implementation/profile bindings, verifies the exact
127-file relocation and uses fresh catalog, custody, fixtures and outputs.
It has the intended six public owner calls and one normal Lean consumer:
fresh initialization; two-unit definition/theorem contribution; two-unit
module export; theorem-application plus reduction consumer; expected missing
`Nat.add_zero` refusal; retained extraction; and combined two-theorem completion.
The module branch uses returned root A for export; the separate library
branch stays at the original basis B.

Per-command grants are reserved before launch and charged using complete child
Job CPU once. Nested native samples are evidence, not a second ledger charge.
An unknown final sample retains the full reservation and stops; the expected
refusal still requires clean closure. Partial accepted results and all output
files are preserved on later failure. Outer supervision remains authoritative.

Exact public-schema/argument compatibility and finalized assertions are still
under review. No product import, test, compiler/build rerun, owner/database
opening, staging, network or Git operation was performed by this reviewer.
All full-deployment and useful-growth claims remain outside this narrow check;
full v5 is unfinished.

## Review follow-up before final source binding

The author has corrected the basis assertion and reconciled the plan with
root's later numeric envelope. The observed intermediate harness hash is
`5ec0b1d8c703f4e3765a21e6ffb74463956bd8c3ff82190296c22f307b9ff751`;
final source clearance still awaits the author's stable-byte notification.

A second, harness-local accounting issue was reported: its expected nonzero
refusal must recheck final child CPU, cleanup-inclusive wall time and log
lengths against that command's grant. The unchanged supervisor only applies
its final post-closure cap recheck to zero-exit success; an expected exit 1 can
otherwise retain `COMMAND_FAILED` after a late final-sample overrun. The
aggregate smoke allowance is still checked, but that is not a substitute for
the claimed individual grant. No failing workload was executed to discover
this; it follows directly from the two source paths.

## Narrow extractor-binding successor: source/theory clearance

Root subsequently selected the separate repair in
`ORDINARY-EXTRACTOR-BINDING.md`, read in full, SHA-256
`e13e369715117883f0c06b7b807010120f792a7e24561b0cbc2cd0ad37db6f6d`.
The new helper is
`software/v5/ordinary_extractor_binding/library_extraction.py`, SHA-256
`28ff83c5a8561b9f5250e9be08b34744aedd23757765feb174e1504d700308aa`.
Decision: **no blocking source/theory defect in this exact narrow delta**.
This is not clearance to run the incompatible build01 package or to mutate it.

The complete new helper and its existing caller/profile dependencies were read.
A standard-library-only inert text diff independently confirmed that the delta
is limited to removal of the two build-specific constants, addition of
`selected_exporter`, replacing the old support check with that helper, and
recording `executable_pin` in selection/result metadata. No repository module
was imported or executed, and no native process or owner was opened.

The code retains the following authority boundary:

- `extract_retained` still requires the exact `AuthoringProfile` type, shared
  core identities and bounded caller budget callbacks. The public loader still
  verifies the externally selected profile and helper bytes before import.
- `selected_exporter` calls full `profile.verify(check)`. The unchanged verifier
  rejects duplicate selected paths, validates ordinary nonredirected files and
  checks every selected file's actual size/hash under its finite input census.
- The executable must be the exact `bin/MissingImportExporter.exe` sibling of
  this installed helper's `authoring/py` directory. The loaded helper itself
  must be present in that verified profile, and exactly one executable tuple
  must exist. Neither candidate contents nor retained metadata nor a module
  name can choose this path or pin.
- The selected size must be a positive integer at most 32 MiB; the digest must
  be 64 lowercase hexadecimal characters. A bounded ordinary-file reread must
  have exactly that size and digest. Thus a freshly approved binary may differ
  from the historical one, but unselected or changed bytes cannot pass.
- Full final `profile.verify` remains after extraction/planning. The native
  protocol, protected point lookups, supplement census, retained-preparation
  binding, original allowance and no-acceptance extraction status are unchanged.
  Mathematical acceptance remains a distinct explicit `complete` operation with
  the unchanged receiver and proof checking.

The argument depends on reviewed operator-selected local software and protected
local storage, not on a hash proving software correctness, not on peer authority,
and not on defense against a hostile actor racing process memory/files. These
are the existing premises, not newly broadened trust. Recording the exact pin
provides a concrete audit link to the actual newly built extractor.

Integration is still pending: the exact fresh map/build successors and one-helper
file-only package successor require independent delta/census verification. If
their compiler inputs and recipes are unchanged, preserving and reusing the
already built generated artifacts is justified; this source review neither
requests nor repeats a compiler campaign. Root's selected pure-control evidence
and a later actual relocated workflow remain distinct checks.

## Final smoke-harness source review

The author declared the smoke harness stable; the complete current source was
reread, including any portion omitted by display truncation, and its file hash
was independently rechecked:

`software/v5/ordinary_distribution/relocated_smoke.py`
`aaba6e2e30906414f539842fd7678aaaf3ab7f9c077b30c6f115db7407584831`.

Decision: **no remaining blocking harness source defect at this exact hash**.
The initially reviewed selector `62a14a9e...` matches its CLI and root's
360/240/1536 inner, 420/300/2048/eight-process outer envelope. This statement
does not approve staging or launching the incompatible build01 package; the
new integration/map/payload boundary remains a distinct gate.

Final-source checks resolve the earlier review points:

- Basis admission expects 456 checked units, zero retained extension IDs and
  the 581 exact names read from the pinned inventory. The native artifact argv
  also binds the returned accepted root.
- Evidence schema/IDs, export IDs and exact preview header bindings are checked.
  The module report binds semantic/context/foundation, structured module name,
  exact target name, ordered unit IDs, names and full declaration inventories.
  Its three phase pairs and all five module artifact parts are required.
- The normal consumer requires its ordinary `.olean`, `.olean.private` and
  `.olean.server` outputs, and pins any IR companions actually emitted. Its
  exact source and output tree are retained. Its search path contains only the
  supported runtime and the just-generated module directory.
- The one expected exit-1 refusal now receives the same explicit final CPU,
  cleanup-inclusive wall and observed-log cap checks as successful ordinary
  commands. Numeric values must be finite/nonnegative and log counts integral.
  Unknown CPU still retains the full prelaunch reservation and stops.
- The extraction branch preserves and binds the exact retained candidate/request
  and selected prepared bindings; completion checks two theorem units, actual
  supplemental export binding and the consumer proof's `Nat.add_zero` constant.
  The unchanged native decode/re-encode gate rejects orphan/noncanonical proof
  nodes; a later independent saved-outcome audit may additionally trace the
  actual reference from the proof root.

This review was source/data inspection only. No harness function, test, product
module, native executable or owner operation was executed. The original build
artifacts and all historical evidence remain unchanged. The repair and final
harness eliminate the identified source blockers only; neither has yet proved
the actual relocated-use result or completed v5.

## Pure role/pin controls: source-only review

After a fresh guard and complete `AGENTS.md` reread, root separately assigned
the minimal changed-boundary controls. Exact source hashes rechecked:

- `software/v5/ordinary_extractor_binding/pin_controls.py`:
  `20a97f1aa073a3e7a50dfe8bfc2ffbd315f164abc3fd0d62252eb063095d534d`.
- `software/v5/ordinary_extractor_binding/select_controls.py`:
  `dc36155da1fd7ef8dd86bc5bc83b3bffbf0c26ea0130979399750333c8c270cc`.

Decision: **no blocking source defect for the explicitly narrow pure-control
scope**. The reviewer read both files without importing or running them.
Root may select this finite check independently of the package assembly gate.

The control extracts exactly one `selected_exporter` function AST from the
hash-selected `28ff83c5...` helper and evaluates it with explicit narrow doubles
for the already-reviewed profile/path helpers. It does not import the full
product module. The only created apparent executable is clearly inert text;
there is no subprocess, native execution, owner operation or network access.

All 15 cases are decisive for the selected function boundary: approved new
nonhistorical binary pin; profile verification first; absent helper pin; absent
executable pin; duplicate executable; wrong fixed role; five invalid sizes
(Boolean, zero, negative, nonintegral, above 32 MiB); malformed digest; wrong
digest; fewer bytes than selected; and an overbound reread. Success and exact
expected refusal are mutually checked, and profile verification must occur
exactly once. Final source bytes and inert binary bytes are rechecked.

The selected original inner allowance is 25 wall / 15 CPU seconds; the outer
runner allowance is 35 wall / 20 CPU seconds / 256 MiB / two active processes.
The selector captures runner, selector, control and exact helper sources plus
three named Python runtime pins, and requires fresh selection/run paths.
Its outputs remain separate from the package and any owner state.

The fake `ordinary` function and deliberately minimal `ProfileDouble` do not
exercise actual reparse/hardlink defenses, full `AuthoringProfile.verify`,
profile authentication, real loader integration, extraction protocol or theorem
checking. Both source documentation and result claim explicitly preserve those
limits. Passing these controls cannot remove the separate actual-use gate.

## Saved pure-control outcome: independent finite audit

Root executed the selected pure controls once and then assigned saved-output
review only. The reviewer did not rerun the controls, import the helper, invoke
an extractor or open owner/database state. Selection:
`6509ebc0bc5f772f3feac4c69d080e1b8a41414a800ea157a8bd5765b0535717`.
Saved run: `experiments/v5-local-checks/ordinary-extractor-binding-controls-01`.

Decision: **PASS for the exact-function/explicit-double 15-case boundary only**.
Independent inert hash/JSON comparisons verified both original and saved
selection bytes; all four current/snapshot source pairs; all three named Python
runtime pins; 11 saved files; the 15 distinct expected control rows; and exact
agreement between saved `PIN-CONTROLS.json` and parsed stdout. The preserved
53-byte apparent executable is exactly the selected inert text, not a native
binary. The reported native-operation count is zero and the actual selected
control source contains no subprocess or native launch.

The saved helper remains `28ff83c5...`, control `20a97f1a...`, selector
`dc36155d...`, and runner `44a7bf1b...`. No row is skipped or treated as an
unexpected-pass success. Each successful assertion followed the exact selected
function and test-double scope reviewed above.

The outer event exited zero with `COMMAND_EXITED_ZERO_AND_CLOSED`, direct child
reaped, Job closed, no cleanup errors or requested termination, zero final
active/terminated processes, two total process records, and empty stderr.
Complete recorded cost is 0.391552799846977 wall seconds, 0.109375 child-Job CPU
and 0.125 wrapper CPU, or **0.234375 known inclusive CPU seconds**. The inner
control reports 0.06965780025348067 wall / 0.03125 CPU, already included in that
Job charge, not additive. Peak Job private commit is 17,043,456 bytes, below the
selected 256 MiB cap. All observed time/log/counter fields satisfy the selected
outer limits; no retry or renewed allowance is involved.

Saved result hashes:

- `RESULT.json`:
  `2005ec87e2bfed08b7aca145f4258f1a9c4653fd5e7a7326d7b6a1a666900693`.
- `PIN-CONTROLS.json`:
  `8f0d100cb4fd9006cded10243846a96841e8693fa8b417932d642cd3badc7e3a`.

This pass does not exercise full profile verification, loader integration,
actual native extraction, proof admission, or the still-pending package
successor. Those boundaries remain separate and full v5 remains unfinished.

## Fresh integration recipe and file-only assembly: source clearance

The author declared these four files stable; their exact hashes and complete
new assembler/selector source were inspected without executing them:

| File | SHA-256 |
|---|---|
| `software/v5/ordinary_distribution/source-map02.json` | `805785e79e9dd8d566709bb785b5f176adda96db2f08bed4f47f0eecd7e945e0` |
| `software/v5/ordinary_distribution/build02.py` | `0a419be2e295ea2a36284256236369e7ccf99e6f19f0aa741d021483454a18ee` |
| `software/v5/ordinary_extractor_binding/assemble.py` | `4484158a35eb3cb0b92816f2480e2537173b042f0dfcb8107084e16a91fdc132` |
| `software/v5/ordinary_extractor_binding/select_assembly.py` | `5985f51a1d6046c7267fa8310d24c51d223ff661fe202570668ba424332278db` |

Decision: **no blocking source defect for the exact selected integration**.
This clears the finite file-only assembly boundary, not a native build or smoke.

Independent read-only exact-text substitution comparisons establish the entire
recipe delta, not just a spot-check of selected fields. `source-map02.json`
equals its frozen predecessor after exactly the one extraction-helper source
path change, 14474-to-15258-byte size change and `5a71037c...`-to-`28ff83c5...`
hash change. The 67 selected source records and 51 direct copies are unchanged
in count. Every other map byte, including receiver/authoring/extractor lanes,
all 27 transformed-source hashes, base inputs and 14 named native-runtime pins,
is identical.

`build02.py` equals its frozen predecessor after exactly the map SHA/name and
its own `build02.py` self/snapshot/worker names are substituted. Compiler source
inputs, transforms, command flags, lane order, output formulas and resource
accounting are unchanged. The new map/build self-identities agree with the
assembler's exact recipe pins. No native recompilation is required to reuse
the already audited generated payloads in this narrow file-only successor.

Frozen originals were rehashed unchanged: build `a4e720ea...`, map `b021ae32...`
and old extraction helper `5a71037c...`. The successful old build and package
are inputs, not edited targets or relabeled actual-use evidence.

The assembler accepts only the exact audited build01 package/profile and current
owner/loader identities. It verifies the current selected loader/profile without
opening catalog or custody state; it uses the loaded data solely for file-map
and support validation. The replacement helper must match the new map. Exact
set/census checks require 126 payloads, 98 auxiliary records and exactly one
changed payload: `authoring/py/library_extraction.py`; all 125 others retain
their original pins. Every direct-copy map record is checked against the
selected payload pin, not merely its name. Source and target byte bounds,
ordinary-file checks, disjoint fresh output and streaming copy/hash checks
remain finite.

Before committing the new profile, it rechecks every selected source/output,
all original payloads, all installed external runtime pins, both new recipe
files, its own running/source bytes, the preserved builder, old profile and
both exact tree censuses. The receipt is `distribution/ASSEMBLY.json`, outside
`distribution/package/`; `PROFILE.json` is renamed into place last. Partial
files remain on failure, with no overwrite, cleanup or retry mechanism.

The assembly selector records seven source snapshots and is expected to record
141 runtime/input pins: 127 original package files, 9 external installed runtime
files and 5 explicitly used original source/recipe files. Its fixed command
targets fresh `{output}/distribution`; inner limits are 60 wall / 40 CPU seconds
and outer limits 90 wall / 50 CPU seconds / 512 MiB / two active processes.
Neither selector nor assembler calls a compiler, extractor, network service or
owner operation. The source root remains an explicit selected read premise,
not a claimed OS sandbox. Actual selection/copy/result identity and complete
successor payload verification remain pending saved evidence from root.

## Saved one-helper assembly: independent exact-payload audit

Root supplied the one terminal file-only assembly. Selection:
`f97d018a6305d3557052e90ab6f6e5c8c888447018c16b2dbd37b1964d2dcfbb`.
Run: `experiments/v5-local-checks/ordinary-extractor-binding-assembly-01`.
Runtime package: `distribution/package` beneath that run.

Decision: **PASS for the exact one-helper file-only successor**. This resolves
the deterministic old-extractor-pin contradiction in this new package only.
The original build01 package remains unchanged and incompatible at that step;
it is not retrospectively relabeled. Actual relocated public use remains a
separate unexecuted qualification gate at the time of this audit.

Independent saved-file comparisons verified:

- Original and saved selection have the exact selected hash; all seven
  current/snapshot source pairs and all 141 runtime/input pins match. The source
  snapshot contains exactly seven files.
- The successor contains exactly 127 files: 126 payloads totaling 37,508,571
  bytes plus `PROFILE.json`. Every file matches the receipt's size/hash; there
  is no extra owner state, build tree, receipt or pending profile inside it.
- Only `authoring/py/library_extraction.py` differs from build01: 15,258 bytes,
  hash `28ff83c5a8561b9f5250e9be08b34744aedd23757765feb174e1504d700308aa`.
  All 125 other payloads are independently byte-identical by SHA-256, including
  every generated receiver/authoring artifact and the newly built extractor.
- That extractor remains exactly 697,344 bytes with hash
  `77eede87b83b2c3636d5c1a40e24e0d78dcdfaf38f5961cf357bb2dd7a7c911a`.
  The replacement helper is the already source-reviewed and pure-controlled
  profile-role binding, not a historical binary substitution.
- The new profile hash is
  `192dfee12ac186fbdac0634212b28c1c6324222da2b035f8f295ec764303a68d`.
  Its complete raw text equals the old canonical profile after exactly the
  one helper size/hash record is replaced; every other record is identical.
- The installed manifest remains
  `32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`,
  retaining the previously independently derived implementation
  `fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df`.
  All 51 direct-copy records agree with `source-map02.json`; both recipe
  receipt pins match the reviewed actual files. Saved stdout parses to exactly
  the external assembly receipt.

The actual outer event exited zero with direct child reaped, Job closed,
zero active/terminated processes, no cleanup errors or requested termination,
and empty stderr. It recorded two total processes, 27,545,600 bytes peak Job
private commit, 5.361332700122148 wall seconds and 2.546875 complete child-Job CPU
plus 0.59375 wrapper CPU: **3.140625 known inclusive CPU seconds**. The inner
before-commit measurement is 4.348863599821925 wall / 2.453125 CPU, already
included rather than added. All values satisfy the original selected limits.

Preserved result hashes:

- `distribution/ASSEMBLY.json`:
  `c3dba323014a93c9c23b2e6e5b60f4da924d59811e065d30a39065699cf86acf`.
- `RESULT.json`:
  `b36bff22cb43a697cbf5f4dbf114796d536e14fd9b698d60b81a3a7a3ba75486`.

The reviewer inspected/hashes inert saved files only: no assembly rerun, compiler
rebuild, test, product import, owner/database access, network or Git operation.
The current full-source recipe is now coherent with this narrow reused-artifact
successor. This does not itself prove native extraction, actual proof completion,
useful growth, release deployment or final v5.

## Actual relocated public smoke: independent saved-outcome audit

Root supplied the terminal run, not a request to rerun it. Exact selection:
`07d9cfc175d7dcb3c624f1c3d735b9bc17dbb28488cf49e188f1d8db1c0ab17b`.
Run: `experiments/v5-local-checks/ordinary-current-relocated-smoke-01`;
public-operation evidence is in its `smoke/` child. Runtime-only relocation:
`experiments/v5-local-checks/ordinary-current-relocated-smoke-01-payload`.

Decision: **PASS_RELOCATED_CURRENT_SOURCE_BUILD_PUBLIC_USE**, independently
confirmed for this selected controlled fresh-project workflow. It completes the
narrow audited build01/generated-artifact, exact one-helper source successor,
runtime-only relocation and actual-use chain. It does not claim `build02.py`
was separately executed: its unchanged compiler recipes justify the explicitly
reviewed artifact reuse. Full v5 remains unfinished.

### Exact input and immutable-output boundary

Read-only independent hashing confirmed the selected original/saved selection,
all three current/snapshot source pairs, all 156 selected runtime/input pins,
and all 252 files recorded in `IMMUTABLE-FILES.json`. Every recorded file still
has its exact length/hash. The relocation is exactly 127 files, with every file
matching both its original assembled-package counterpart and the relocation
receipt. No build tree, old owner state or old proof-result package was copied.

The actual profile remains `192dfee12ac186fbdac0634212b28c1c6324222da2b035f8f295ec764303a68d`;
installed manifest `32236aa3...`, implementation `fafc8387...`, new binding
helper `28ff83c5...` and newly built extractor `77eede87...` are unchanged.
The named runtime checks retain the declared full-runtime/protected-filesystem
premise, not a hermetic installation or OS-denial assertion.

### Seven actual calls and evidence bindings

All seven public/consumer calls occur once in the selected order. Their complete
child-Job CPU samples are known and sum to 45.125 seconds:

| Call | Actual result | Complete child-Job CPU seconds |
|---|---|---:|
| `init` | Fresh local owner; 456 checked basis units, 581 exact inventory names, no retained extension IDs | 20.203125 |
| `contribute-module` | Two checked units, definition plus theorem, durable evidence and previews | 5.8125 |
| `export-module` | Two-unit proof-complete module, no catalog acceptance | 11.28125 |
| `normal-consumer` | Exact theorem application and independent definition reduction elaborate | 0.625 |
| `missing-library` | Expected exit 1, exactly missing `Nat.add_zero`, no acceptance | 3.4375 |
| `extract-std` | One supplemental theorem and one consumer, explicitly not accepted | 1.28125 |
| `complete` | Both theorem units newly checked, durable evidence and preview | 2.484375 |

The three concrete roots are distinct and explicitly bound:

- Basis B: `8c74aadc460b8efdbfedfa4f6a2468c93dc8c7b617b65870040cbbe22a0c2e8e`.
- Module branch A: `03cb53c1e4f134e8acc404f2d92edb7f77a30810df74e9039f9fb59a6e92124f`.
- Library branch C: `94827b21912710d45d0a459d089b741d39a15caf9b60847b5f0553be7457cece`.

Both contribution/completion publications and their actual native admission
`plan.json` inputs use B; module export uses A. Each accepted root matches the
actual admission worker argv and returned admission. All four evidence IDs and
all three target export IDs were independently recomputed using their domain-
separated hashes. Preview bytes, hashes and exact evidence headers match.
Crucially, the actual native admission `units.json` files equal these retained
evidence units, not merely their names or operational status strings.

| Accepted evidence | Unit ID |
|---|---|
| `CommonsPackageExample.applyTwice` | `25ae588e95228a64196a576aa9c9dd78249c23b0c26189c5671a434b93afa1b3` |
| `CommonsPackageExample.applyTwice_eq` | `c4639e6e5f70e259ea1611adba8e168aa74dbfb91f98e2512cd465f82705e61e` |
| Supplemental `Nat.add_zero` | `2951fcf2eb813a9c4472c8a58f6ff51d1389363f9c2d2cace207ca28319887ae` |
| `CommonsLibraryExample.add_zero` | `6f0a5a17f40dbca4e4f0eabb86c6d6a2dfd0eeb0056d36e81373a2e185cd51c8` |

The module is
`DMKNBridge_9609cb4a4b9392e37ec5ffccbc6d66121eb23be6107d9f12cb48f58fa9b4f215`.
Its actual request contains exactly the two retained evidence units. The native
report checks two units/two passes/581 basis rows and binds their exact IDs.
All three actual phases (`build`, `reread-private`, `reread-exported`) have their
selected STARTED/EXITED-zero pair. All five module artifact pins and exact
five-file census were independently checked. The ordinary consumer source imports
only Init and this new module, applies the returned theorem and proves the second
statement by `rfl`; all five produced consumer parts are nonempty and hash-match.
The reviewed pinned consumer worker supplies only runtime/new-module search paths.

### Actual new extractor and reachable proof use

Both extraction selection and result record the exact newly built executable:
697344 bytes,
`77eede87b83b2c3636d5c1a40e24e0d78dcdfaf38f5961cf357bb2dd7a7c911a`.
The actual extraction argv launches it from the relocated package, not the
build directory or historical package. Extraction closes cleanly with 9 lookups,
4538 output bytes, 2861 protocol bytes and 0.109375 native CPU seconds. It retains
`mathematical_acceptance:false` and the same B parent throughout.

The missing candidate is byte-identical across retained refusal, extraction and
completion. The exact retained request hash, supplemental bytes and prepared
bindings remain bound to the same operation; the completion's actual native
input contains the supplied theorem and consumer proof. The independently
derived supplier export is
`3b0568ce9188e3ad9c159ddab4c767f3522cbf689aa1677ffcc32c4f2564312d`.
The consumer's import row binds `Nat.add_zero` to precisely this export. Its
proof root is node 4; the `Nat.add_zero` constant is node 1, reachable from that
root. All five proof nodes are reachable, and the supplier has no self-import.
Thus the result is actual checked supplemental-proof use, not merely a matching
name in dead serialized nodes or an extraction-only JSON success.

### Closure, cost and preserved result identities

The independent inert-data audit checked 15 supervision records: the outer run,
all seven public/consumer Jobs, and seven nested admission/authoring/module/
extraction Jobs. Every direct child is reaped, every Job closed, final active and
terminated counts zero, with no cleanup error or requested termination. Expected
exit 1 remains a clean, fully charged refusal and satisfies its final resource
caps. The extractor additionally has joined threads, complete accounting and
successful attach/resume. The 48 total process records are lifetime records,
not concurrent processes or 48 independent CPU charges.

Complete outer cost is **53.94209899986163 wall seconds / 48.703125 known inclusive
CPU seconds**: 47.234375 complete outer child-Job CPU plus 1.46875 wrapper CPU.
Peak Job private commit is 1,465,085,952 bytes. The inner ledger records
52.41426800005138 wall, 45.125 complete command-Job CPU plus 2.015625 controller
CPU; these inner/nested measurements are already included, not added again.
All observed final times, CPU, log lengths and peak memory satisfy the original
360/240/1536 inner and 420/300/2048 outer limits. No retry or budget renewal ran.

| Preserved artifact | SHA-256 |
|---|---|
| Outer `RESULT.json` | `9da95b9c6b5f4d5d9b634b00760ef1745381f942de73cb91256e10a496ce6992` |
| `smoke/SMOKE-RESULT.json` | `e1d0aac60245722d73ffe21fc2961fc52bf5216931c09d8eccbfb7b18c37301f` |
| `smoke/IMMUTABLE-FILES.json` | `c7f34a6b8b7303c239c38edef6362f49c332d14723e410d4ab0cd4aa388e092c` |
| Relocation receipt | `6b762405a354aadcfac16b9697db1941973d782145c12bce267b0b0aca5024c7` |

This independent review used shell hashing and standard-library-only inert
JSON/hash/graph comparisons. It imported no product modules, opened no databases,
ran no owner/compiler/extractor/test, and performed no network or Git operation.
No used bytes were edited. The demonstrated scope is this controlled source-
complete-build-to-relocated-use interoperability chain, not a real-user project
benchmark, general library support, sustained useful growth, release deployment,
certificate result or completion of the full v5 goal.
