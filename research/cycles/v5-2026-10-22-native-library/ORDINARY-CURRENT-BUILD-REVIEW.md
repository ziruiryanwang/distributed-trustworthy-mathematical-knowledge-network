# Independent review: current source-to-package build

2026-10-23. Reviewer: `return_actual_audit`. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Scope and present disposition

Source-only review of the selected
[current build plan](ORDINARY-CURRENT-BUILD-PLAN.md) and fresh
`software/v5/ordinary_distribution` implementation. No source/product execution,
native build, test run, owner/database opening, runtime launch or Git mutation is
performed by this reviewer. Read-only file/hash/JSON comparisons are permitted.
The canonical workspace guard passed. Earlier return/runtime outcomes are not
rerun or re-audited here.

**No blocking source defect found in the finalized builder and clean-input
selector identified below.** The selected three-stage shape is implemented:
unchanged base builder as a supervised child, separate fresh six-module native
extractor, then one current-map package assembly. This is source clearance, not
proof that a source-complete build or relocated use has succeeded. Root owns any
finite selection and launch.

## Early exact source-map findings

`source-map.json`, SHA-256
`b021ae3225fe85a874cea82266c0c380d08fc755fee4fc282872f0f506f298bf`,
contains 67 source input pins, 47 base-builder inputs, 51 direct-copy records,
ordered receiver/authoring/extractor lanes, and 14 extra named native-toolchain
pins. All 67 source length/hash pairs independently match current repository
files. All 51 direct-copy payloads independently match their intended current
reference-package bytes. Every source input is beneath `software/`; none names
an experiment, product-local, runtime or `_build` output tree.

The map retains the important selected versions: support02 retained preparation,
resilient peer API, project-return contribution helper, native module03 and
worker03. Receiver `OrdinaryExport` retains its separate checked-in source;
authoring uses its public module form; the extractor declares the exact legacy
header transform. Generated output census is eight receiver `.olean` files,
65 authoring parts, one extractor executable and one installed manifest, plus
the 51 direct copies: 126 payloads and a separate generated outer profile.
Runtime pins describe explicit supported distributions, not hermetic closure.

An independent finite reconstruction of the base builder's listed inputs equals
the map's 47-entry `base_inputs` exactly. Their union with all copy/lane sources
equals the 67-entry source census, with no missing or unused map input. All 27
ordered lane entries have the specified source transformation hash, recomputed
from bytes without executing repository code. The output-name union has exactly
126 case-insensitively distinct paths and exactly matches the current reference
profile/installation payload union; 98 are auxiliary. The retained package was
read only as comparison evidence, not incorporated as a proposed build input.

## Implementation review obligations

- The current orchestrator, map, all 67 selected sources and named runtimes must
  be bound before use, staged without redirected/aliased paths, and rechecked.
  The base child must consume only the selected fresh source snapshot, with no
  dependency on prior package/profile/selection files or generated artifacts.
- One original wall/CPU allowance must include staging, both supervised children,
  assembly and final verification. Child grants must decrease. Charge each full
  child Job once, including the base builder's descendants; do not add its nested
  compile charge again. If final CPU is unavailable, reserve the issued grant,
  preserve evidence and stop. Final and nested process closure are required.
- The original-base behavior and selected existing supervisor are reused under
  the outer composition; reserved cleanup/controller margins must fit the same
  allowance and must not become a renewal after failure.
- All six native objects must be freshly generated in their own lane from the
  selected source forms; compiler/search paths must bind the explicit runtimes.
  No historical `.o`, `.olean`, extractor or old owner state may be an input.
- Installation support hashes and implementation identity must derive from the
  actual new outputs. Final current profile must bind all 98 auxiliary payloads
  and the actual installed manifest, without stamping the old reference ID.
- Final package census must be exact and independently relocatable from `_build`.
  Build sources/logs/intermediates remain separate, and failures retain partial
  outputs without retry or misleading final-profile publication.

These are review gates for the selected implementation, not requests for another
general test campaign or a claim of final deployable v5 completion.

## Finalized builder source disposition

The complete builder, map and README were read. The final builder change from
the author's initial `7210c327...` version adds only core-module collision and
staged-origin checks around the installer import; these final lines were reread.

| Selected new source | SHA-256 |
|---|---|
| `software/v5/ordinary_distribution/build.py` | `a4e720ea936880a4b5e353e04e5b7017645683a23efd30df751a0fec609dda24` |
| `software/v5/ordinary_distribution/source-map.json` | `b021ae3225fe85a874cea82266c0c380d08fc755fee4fc282872f0f506f298bf` |
| `software/v5/ordinary_distribution/README.md` | `d4a716ae97252284164f121bf3ae7e23bd533b6d8fb6cd313c1683c12f550177` |

**Source clearance for this exact implementation.** Bootstrap executes only the
fixed hash-checked unchanged base helper (`49b922dd...`), whose definitions were
read. The new builder then applies that helper's absolute local path, ancestor
reparse/symlink, single-link regular-file and fresh-output checks. The new map
has a fixed expected hash; the running builder must match the selected source
root's builder bytes. All 67 selected inputs plus the new builder and map are
verified and copied into fresh `_build/inputs` before installer/core/supervisor
imports. Core names must be absent before import and must resolve to those
staged source paths afterward. Final verification rechecks both source-root and
snapshot bytes. The only original-tree bootstrap code is the fixed preserved
base helper, not a generated executable or historical package.

The base subprocess runs its unchanged staged builder with `--source-root`
pointing at the staged tree and a fresh `_build/base` output. It performs the
original receiver/authoring construction and installation assembly; the new
controller separately requires both its outer clean Job and its nested compiler
Job to have completed cleanly with finite final CPU and empty stderr. Its saved
public-transform map must match all 13 selected authoring source/generated hashes.
No existing installation or mathematical state is opened to derive the new one.

For the extractor, six selected source files are read from that snapshot. The
legacy transform is the same byte transformation reviewed above and every view
must match its fixed transformed hash. A fresh source directory and empty object
directory precede the worker. The worker runs the six Lean/C/object pairs in the
declared order and links only those six fresh objects. `LEAN_PATH` names only
the fresh object lane; explicit Python/Lean executable directories replace ambient
`PATH`, and inherited Lean/Python settings are removed. The Lean codegen argv
matches both existing native build adapters, which also omit an explicit
`Elab.async` option; the unchanged base lane retains its existing
`-DElab.async=false`. The new native commands are sequential, and the same
supervised Job and absolute deadline govern their descendants.

The accounting composition is consistent with one original allowance. Before
each child, its CPU grant is the floor of remaining original CPU minus 62
seconds, and its wall grant is the floor of remaining wall time minus 25 seconds.
These reserve the existing supervisor's at-most-60 controller CPU seconds,
cleanup and final-work margin inside the original allowance. The base receives
a further reduced inner grant. A full child CPU grant is charged prospectively
before supervision; only a finite nonnegative **final** Job sample replaces that
reservation. An exception or missing final sample leaves the full charge and
forces failure, with no later stage launched. Known full child Job CPU is charged
once; the base's nested compiler charge is checked diagnostically, not added
again. Controller `process_time` covers its own supervisory/copy work. The
controller remains cooperative and the documented enclosing owner Job remains
appropriate; this is not a new hostile-source sandbox or hard disk limit.

The final map selects exactly 51 snapshot copies, eight new receiver artifacts,
all 65 authoring parts, the newly built extractor and the actual new installed
manifest. All 19 installed direct files, eight receiver artifacts and base
runtime pins must equal the manifest's complete file map. The new builder
recomputes every support-group digest and the implementation ID from that
manifest, comparing the result with the actual base assembly report. It does
not stamp the reference package's old implementation ID or profile onto new
bytes. The final profile binds the actual installed-manifest hash and exactly
98 auxiliary payloads with the current loader's schema/layout fields.

Copies are streamed, hash/size checked before and after, and bounded by the
selected total limits. A final exact 126-file package census excludes `_build`;
the 98 auxiliary records and installation manifest use logical names, without
an absolute source/build dependency. The final profile is committed only after
source, runtime, transformed-view and selected output verification. Build logs,
snapshots and partial failures remain under `_build`; no cleanup, retry,
initialization, module export, certificate or network operation is selected by
the implementation. A precommit build receipt alone is not a completed-package
marker; later outcome review must require the actual final profile and closure.

## Clean-input selector source disposition

`software/v5/ordinary_distribution/select_build_check.py`, SHA-256
`4591d3d6867606439ac1636166ef15954d6b2548a6f3424a46c7ee0f30455382`:
**source clearance for file-only staging and exact finite build selection.**
This test adapter's canonical-machine paths are explicit; the product builder
it selects is parameterized and does not require those drive letters.

The selector checks the supplied reviewed builder/map hashes, the fixed base
helper hash and the exact 47-entry base input set. It stages precisely 69 files
into a fresh source tree, preserving their repository-relative paths. Each
original and staged copy is checked against its size/hash pair; the final file
set must equal the map. The 67 map inputs contain no old generated artifacts,
and the two added files are the new builder and map. The 23 named runtime files
are verified against the fixed base/runtime-map pins. The selection pins those
runtimes, all 69 originals, all 69 staged copies and the new staging receipt
(162 runtime/input pins), and snapshots the runner, selector, builder and map.
The selector itself does not import or run the current builder or any compiler.

Its proposed actual build command runs the selected builder snapshot, passes
the fresh 69-file tree as source root and supplies fresh run-local output and
explicit runtimes. The inner allocation is 480 wall seconds / 360 CPU seconds /
2,048 MiB; the separate outer selection is 540 wall seconds / 440 CPU seconds /
2,304 MiB / eight active processes. These are finite proposed limits, not measured
costs or a renewed historical allowance. Selector staging has its own finite
90-second deadline; no actual build is launched by writing this selection.

The clean-input evidence is the exact staged tree, fixed source pins and actual
child argv. It is explicitly **not OS denial of access to the original repository**
or a hermetic filesystem/toolchain claim. Original pins remain in the audit
selection for integrity checks; the selected product build's declared source
reads are from the clean source tree and its own fresh snapshots. Root reports
the 67 map inputs are Git-tracked; this reviewer did not invoke Git or infer that
the new distribution files are committed merely from their presence.

No remaining source blocker was found for the selected one clean-source build
decision. Actual build-to-relocated-use interoperability, newly derived identity
adoption, release packaging and the broader v5 obligations remain unqualified
until their separately selected evidence exists. This review recommends no
repeat of earlier passing mathematical/network campaigns.

## Saved clean-source build01 outcome audit (2026-10-23)

Reviewer: `return_actual_audit`. **PASS for the one selected clean-source build
and exact current package assembly.** This section independently reads saved
files, structured records and hashes. It does not import/run product code, open
owner/database state, execute a compiler or rerun any campaign. The canonical
workspace guard passed again. No relocated-use acceptance is inferred.

### Exact input and source origin

Run: `experiments/v5-local-checks/ordinary-current-source-build-01`.
Original and saved selection bytes are identical at SHA-256
`97a4c0d19aea620d067f9cf2a227706fd460654bf06b978cc201a2b7b2e8790b`.
All four selected source original/snapshot pairs and all 162 runtime/input pins
independently match. This includes the exact reviewed builder `a4e720ea...`,
map `b021ae32...`, selector `4591d3d6...` and runner `44a7bf1b...`.

The selector's fresh source tree and the distribution builder's inner
`_build/inputs` each have exactly the same 69 files recorded by the staging
receipt and builder `SOURCES.json`. All originals and both copies match their
length/hash pairs. The 67-entry map plus builder/map files equals that set
exactly. The base builder's further `_build/base/_build/inputs` snapshot has
exactly the 47 selected base inputs, all matching the same source pins. All 23
named Python/Lean/compiler runtime pins match, and the recorded original
allowance is the selected 480-wall/360-CPU/2,048-MiB allowance.

The actual outer argv selects the clean source tree, the base-child argv selects
the distribution's inner source snapshot, and the nested compiler argv selects
the base's fresh receiver/authoring lanes. The extractor worker argv selects
the fresh extractor source/object directories. Thus the saved source and argv
chain agrees with the reviewed exact-input design. It does not claim that the
OS prohibited every possible read outside those trees; old generated outputs
are absent from the selected build inputs, not hidden by a filesystem sandbox.

### Generated artifacts and complete package

All 27 emitted receiver/authoring/extractor source views independently match
their source and transformed-source hashes. Every authoring-map original,
generated and post-import-body hash matches; the six extractor views match
`EXTRACTOR-SOURCE-MAP.json`. The receiver output lane contains exactly eight
`.olean` files, as intended; the authoring lane contains exactly 65 parts.
Every compiled record's actual size/hash matches its saved compiled-file map.

The base compiler log contains exactly the selected eight receiver and thirteen
authoring phases, in order, each exiting zero. The extractor log contains exactly
six ordered codegen/object pairs and one native link, each exiting zero. The
pinned worker source fixes each compiler argv shape, while its saved top-level
argv binds the fresh directories. All six new `.olean`, `.c` and `.o` files and
the linked executable match the 19 records in `EXTRACTOR-OUTPUTS.json`; no
historical object path enters the reviewed worker command construction.

The final `distribution/package` contains exactly 126 payloads plus `PROFILE.json`,
with no pending marker or build-directory payload. Its 37,507,787 payload bytes
consist of the exact 51 source/asset copies, eight generated receiver artifacts,
65 generated authoring parts, new extractor and generated installed manifest.
Every final payload matches its selected origin and reported length/hash.
The final 98-entry auxiliary profile map and 36-entry installation map
(27 package files plus nine external runtime attachments) match these bytes
exactly. Public builder stdout equals the saved build result; base stdout equals
its saved base result.

| Actual new-package binding | SHA-256 / identity |
|---|---|
| Final `PROFILE.json` | `3f3c0de037fd03907d661e428b6cc3592848ec8b66cc0e6fdbf579b0fb603026` |
| Final `installation/INSTALLATION.json` | `32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2` |
| Independently recomputed implementation ID | `fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df` |
| New 697,344-byte extractor | `77eede87b83b2c3636d5c1a40e24e0d78dcdfaf38f5961cf357bb2dd7a7c911a` |

The profile and installed manifest are canonical JSON and agree with their
actual saved hashes. Independent recomputation of all support-group digests
and the V1 implementation-claim digest from the actual installed manifest gives
the implementation ID above. These are derived results, not adoption of an old
identifier solely because it appeared in the build report. Neither descriptor
contains an absolute build/source path or `_build` reference; their payload
paths are the reviewed logical layout. Relocated execution is still untested.

Comparison with the preserved return package is exact: 125 of 126 payloads,
including all 73 receiver/authoring artifacts and the installed manifest, are
byte-identical. The sole changed payload is the extractor: its previous SHA-256
was `9700c6c2944d327a648e3fcf83453ee1aa019d2f05c182feec13e78211711dc7`,
also at 697,344 bytes. The final profile differs only in that extractor hash.
The reason for this binary difference is not established by this audit, and
equal length is not treated as equal executable behavior. In particular, the
new extractor still requires the selected actual-use qualification. These
results do not establish bit-for-bit reproducibility of the complete build.

### Nested closure and original accounting

All four saved supervision layers have zero exits, reaped direct children,
closed Jobs, zero final active/terminated processes, no requested termination,
no cleanup errors and empty stderr. Their command argv/limits/cwd and actual log
lengths match their command/log records. The run contains no build-failure report
or final-package pending marker. The outer 84 process instances are a lifetime
total, not a claim of 84 simultaneous processes against the eight-active limit.

| Layer | Actual wall seconds through closure | Inclusive Job CPU seconds | Granted wall / CPU seconds |
|---|---:|---:|---:|
| Outer build process tree | 52.0283566 | 46.984375 | 540 / 440 |
| Base child process tree | 33.7566132 | 31.4375 | 452 / 297 |
| Base's nested compiler tree | 30.9051046 | 29.5625 | 400 / 292 |
| Fresh extractor tree | 11.7787539 | 12.8125 | 419 / 265 |

The complete outer runner cost is **52.5020993 wall seconds / 48.015625 known
inclusive CPU seconds** (46.984375 Job + 1.03125 wrapper), with a 924,160,000-byte
peak Job private commit, inside the original 540-wall/440-CPU/2,304-MiB envelope.
The distribution builder's precommit accounting is 51.3327598 wall seconds and
46.890625 CPU seconds: 2.640625 controller plus exactly 44.25 full child Job CPU
(31.4375 base + 12.8125 extractor), inside the original 480-wall/360-CPU allowance.
The nested base compiler's 29.5625 seconds are already included in the base Job
and are not added again. The small difference from complete outer CPU also
includes startup/final work beyond the precommit receipt; the outer result is
the authoritative complete-run total. Both child CPU samples are complete, so
no unknown-CPU reservation substitution occurred.

The base's actual inner request is 427-wall/295-CPU seconds; the later extractor
grant decreases to 419-wall/265-CPU seconds. All selected child memory limits
remain 2,048 MiB. The saved limits are the existing sampled wall/total-CPU/log
and named-runtime scope, not a hard disk quota, complete toolchain attestation
or hostile-source containment proof. No allowance was renewed.

Saved build result SHA-256:
`634820284798fbc1825c70c7b67f66c8ddf70a73783da51e7738dda40872fa02`.
Outer result SHA-256:
`0a3f1c599dc9cd49c1586a9f5622032aa8feeb15f405614e1055c95811d00a8b`.
This establishes the selected source-complete current build and package
assembly. It does not establish relocated public use, new extractor protocol
interoperability, new owner acceptance, network operation, certificates,
useful-growth advantage or completed deployable v5. No build rerun is recommended.
