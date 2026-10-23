# Independent review: ordinary project return

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Reviewer: `practical_path_audit`. Scope: selected source-only import-name repair
and pure changed-boundary controls; no execution, state opening, native build,
network, Git mutation or repeated predecessor audit.

## Predecessor and concrete obstacle

The frozen `software/v5/ordinary_project_package/ordinary_contribution.py`
has SHA-256
`b8eefe6af368d8a7f5c498d563a12b31416c48c877ea471361eadd2a56a90b31`.
Its shared `_project_module` accepts ASCII identifier components no longer than
64 characters, with at most 16 components and 256 total characters. Both output
`module_name` and each imported module use that validator. Generated bridge
modules have a single 75-character name: `DMKNBridge_` plus 64 lowercase hex
digits. The generated name therefore fails the old import validator before
authoring, even though it is a valid Lean identifier.

This is a source-determined interoperability obstacle. It requires neither a
native reproduction nor shorter content identities. The selected repair should
extend the accepted **import** language by precisely that full single-component
pattern, leaving ordinary accepted imports and all output module restrictions
unchanged. It must not treat the pattern as proof of content identity or authority.

## Review obligations

- Exact import-only full-string exception; no suffix/prefix match, uppercase-hex
  widening, dotted wrapper, control characters or filesystem separator escape.
- Existing module-count, total-length, duplicate, Boolean-meta and project-path
  checks stay unchanged. Output module generation still uses the old validator.
- Direct dataclass construction remains revalidated through `to_document`.
  Generated import text may contain only the validated ASCII identifier.
- Full file comparison must show no semantic/export identity, evidence,
  admission, native supervision or acceptance change.
- Pure controls distinguish newly accepted import spellings from unchanged
  ordinary names and unchanged output refusals. They must not classify shorter
  ordinary identifiers already accepted by the predecessor as newly forbidden.

## Helper source clearance

Successor `software/v5/ordinary_project_return/ordinary_contribution.py`:
SHA-256 `09394f523417406aefcad0b47d06fa2d7782940bec3bb5094975f08b68f94ca8`.
**No blocking defect found in the selected helper delta.** Full-text comparison
equals exactly four replacements in the frozen predecessor: function signature,
strict Boolean option validation, the component-length predicate plus three
explanatory/exception lines, and the import-loop call. All other bytes represented
by the UTF-8 source text remain identical; both complete file hashes are pinned.

Let L be the predecessor's accepted module-name strings and let B be exactly
`DMKNBridge_` followed by 64 lowercase hexadecimal characters. With the option
false, the successor accepts L; with it true, it accepts L union B. This follows
because the exception uses `re.fullmatch` on the entire string, every member of
B is a single 75-character valid nonreserved ASCII identifier, and every other
input must satisfy the original component-length condition. The total 256-byte
ASCII bound and component-count/syntax/reserved-name conditions remain in force.
An uppercase hexadecimal suffix, extra segment, separator, trailing newline or
longer arbitrary name is not in B and acquires no new exception. Short prefix-
like identifiers already in L remain accepted, as required for compatibility.

Only the import-loop call passes true. Output `module_name` remains on the
default-false path, and `module_path` still revalidates it before constructing
the fresh relative source path. Direct dataclass construction, duplicate import
checks, exact Boolean meta flags, project paths and import counts all retain
their prior checks. The exceptional name is only authoring syntax: it does not
prove the module's content hash, trustworthiness or acceptance. Evidence export,
semantic identities, owner warrants, native supervision and final admission
code are unchanged.

Focused control source is still pending; no runtime or installed-project return
result is established by this source clearance.

## File-only overlay and selector clearance

| Source | SHA-256 |
|---|---|
| `ordinary_project_return/assemble.py` | `d454d5009f660fbb059ad5af426649b6118580c830beadbff9b63f30f575f2ed` |
| `ordinary_project_return/select_assembly.py` | `26b566869be397baa724d58ef687cc211f9701f10b2b50d460bca9d0150d1055` |

**No blocking source defect found for the intended module-package base.**
The assembler body from `def need` through EOF is exactly identical to the
previously reviewed `ordinary_module_package/assemble.py`. Changes preceding
it are the accurate docstring, base owner/loader hashes, source prefix and a
one-element source map replacing `authoring/py/ordinary_contribution.py` only.
The intended base profile is
`f01398e394a7bfda05f641469077cb74927aafd1cb1a3d42383d4b1d271e9435`;
its actual descriptor binds the predecessor helper `b8eefe6a...`, owner
`c28ba23d...` and loader `da073981...`, matching the chosen base pins.

The selector is exactly its frozen predecessor after the documented filename/
prefix and descriptive-title substitutions. It binds source snapshots and
canonical assembly inputs, every package/installation payload and external
runtime attachments; no source loader or mathematical core is replaced as an
incidental effect. The original 90-wall/50-CPU/512-MiB/two-process outer and
60-wall/40-CPU inner file-only allowances remain. Full-copy verification,
fresh output, profile-last commit, failure preservation and unchanged installed
implementation identity are inherited without further alteration.

This clearance supports a fresh selected overlay; it does not assert that one
has run or that the returned-project contribution workflow has succeeded.

## Saved overlay assembly01 audit

**PASS for the exact one-helper file-only overlay.** Selection
`686be16ecf1df6a0136fa2446fe96c0bdc850d7b9b8f97d5938d132aa15300cc`
matches original/saved copies. All five selected source originals/snapshots
and all 139 runtime/package pins independently match. The complete combined
auxiliary/installed map has 126 payloads and 37,507,787 bytes; every actual
size/hash matches. Comparison with the actual prior package changes exactly
`authoring/py/ordinary_contribution.py`, adds no payload and removes none.
There are no extra files besides `PROFILE.json` and the assembly receipt.
The installed-manifest identity remains unchanged; receipt equals stdout.
Final profile is
`0d8a9ec4d3509e60f8e3155313b1023230c7f9b4f36f103e55464d2c866ae1b5`.

Clean exit zero: 4.605206 wall seconds / 2.3125 known inclusive CPU seconds
(1.71875 Job + 0.59375 wrapper), peak 28,233,728 bytes. Stderr empty; no live or
terminated descendants, termination request or cleanup errors. This validates
the saved file overlay only, not native project execution or return admission.

## Focused pure-control source clearance

`software/v5/ordinary_project_return/project_controls.py` SHA-256:
`2e754900c73f6b64e58d59cae545f79932369e0a3c87ff33feffda292753180a`.
**No blocking source defect found.** The four groups are limited to configuration
validation, roundtrip/dataclass revalidation, exact generated import text and
in-memory source assembly. The selected helper hash is pinned explicitly after
the ordinary complete profile load. Real owner/custody/admission/contribution,
native supervision, SQLite, child process and network entry points are guarded;
any forbidden attempt makes the overall report fail. The single original
50-wall/30-CPU allowance includes package loading and all cases.

The cases directly test the newly admitted 75-character exact name and ordinary
and meta import text; unchanged output refusal through both document and direct
dataclass paths; strict internal Boolean option and closed external fields;
63/65-digit, uppercase/nonhex, dotted and separator/control-character near misses;
unchanged 64-character components, 16 components and 256 total-character limits;
short prefix-like names already accepted by the predecessor; and unchanged
import/path counts, duplicates and meta/path validation. Source assembly is
compared against the default wrapper with exactly one import-header insertion,
before owner construction. The source body and acceptance/export commands remain
unchanged. No actual project/module files or owner state are required or opened.

This is source clearance, not a saved control-run pass or an installed reciprocal
return result. Any execution still requires root's separate finite selection.

## Pure/native selection source clearance

`software/v5/ordinary_project_return/select_checks.py` SHA-256:
`7c464d00b6f314b5ae0a4c621947927621732b7aa2159662113a04dfa9342229`.
**No blocking selector defect found.** This is the reviewed module-public
selector with its unused phase-only branch removed, new source prefix/control
filename, and seven additional retained-module pins for the native branch.
Both remaining branches still require a complete selected package profile,
pin its auxiliary and installed files plus external runtime attachments, and
execute only the selected runner snapshot. No owner state is opened by selection.

The control branch supplies the exact package/runtime arguments expected by
the four-group suite, with 60-wall/35-CPU/512-MiB/two-process outer allowance.
The native branch retains the exact utility pin `20f6c613...`, all nine old
artifact pins and 180-wall/110-CPU/2048-MiB/eight-process limits. It additionally
requires the actual prior public export's manifest SHA
`d447b491cb4166035063377e36757c1f14b1340fe6dcec423a60a3b18b6735e8`,
native report SHA
`035de7d52abe5a71ba41b7a48ba0b1382f0e9037dae50cdb7cb4ba26bb968b48`,
exact full module name and every one of its five artifact size/hash pairs.
The two literal report pins independently match the saved files. No module
export is repeated merely to supply the proposed return test. Fresh-output,
source pinning, bounded reads and complete runtime-map limits remain intact.

The forthcoming native return harness is a distinct assigned review, not cleared
by this selector inspection; root must bind its finalized reviewed source before
any native selection. No runtime is launched by the selector itself.

## Saved pure controls01 outcome

**PASS for the four pure configuration/source-assembly groups.** Selection
`4230a2ec2a82f9fe3f8d58dfa835267d411a41b5050cbf88d5f45ca96d70dbf8`
matches original/saved copies. All three source original/snapshot pairs and all
136 runtime/package pins independently match, including helper `09394f52...`
under package profile `0d8a9ec4...`. All four saved groups are true; forbidden
attempts are empty; saved report equals stdout. The run has no generated Lean,
module or database fixture files. Together with the reviewed guarded source,
this supports the declared zero native/owner/custody operation scope, not
actual project execution or mathematical acceptance.

Clean exit zero: 1.4654581 wall seconds / 1.28125 known inclusive CPU seconds
(0.796875 Job + 0.484375 wrapper), peak 28,065,792 bytes. Stderr empty; both
selected process instances completed, with no live/terminated descendants,
termination request or cleanup errors. No rerun was performed or recommended.

## Next-payoff recommendation after the current return discriminator

This recommendation reuses
[existing-declaration analysis](ORDINARY-MODULE-EXISTING-DECLARATIONS.md) and
[whole-cost analysis](ORDINARY-PRACTICAL-COST.md); it adds no new equivalence
engine, cache design, cost theorem or experimental allocation.

1. **First finish the already prepared real project-return path.** Its outcome,
   not these syntax controls, determines whether normal-project work can return
   through the public contribution API. If it exposes a direct blocker, address
   that concrete failure before expanding the architecture.
2. **Then prioritize mixed installed-declaration reuse.** The saved native03
   refusal already supplies the relevant shape: an accepted
   `CommonsLibraryExample.add_zero` target has the complete two-unit closure
   including installed nonbasis `Nat.add_zero`, and export refuses the duplicate
   before writing. The module is not merely a request to repackage Nat.add_zero
   alone. The same obstruction affects useful new results with common standard
   library proof dependencies. No extra native reproduction is needed to
   establish the obstacle. Ordinary approved package import remains preferable
   when it already supplies the desired result, but it does not itself export a
   newly acquired mixed commons result into a user's project.
3. **Consolidate the usable route, rather than accumulating optional overlays.**
   Once the return path and the justified mixed-declaration boundary work, one
   supported package/entrypoint and an ordinary-project walkthrough have higher
   payoff than more tiny demonstration variants. Packaging must retain exact
   runtime/trust-policy boundaries and not present local compatibility as global
   readiness. This is release usability work, not evidence that license,
   isolation, independent deployment or broader library support is finished.

For item 2 the next decision is source/theory-only: determine whether the chosen
installed singleton's private and exported views satisfy the already specified
exact correspondence, or whether an explicitly linked same-origin public
signature relation is necessary. Private full proof equality alone must not be
mistaken for public-import compatibility; same name/type alone must not preserve
an ExportID. Reuse the existing full-evidence collector and exact inventory
codec, unchanged kernel checking for genuinely added units, and separate
matched-versus-added inventories. Keep generated-group/partial/mismatched cases
refused. Do not enlarge the fixed basis or bypass duplicate checks in the checker.
If the minimal visibility/origin premise cannot be met, retain the refusal and
state the supported boundary rather than build a general equivalence mechanism.

Selected-context scaling is a real, separate limitation, not the highest-payoff
next edit: the existing cost analysis already establishes repeated work in
chosen context K, while no client must ingest global corpus N. Use the existing
bounded project roots and multi-unit batches now; neither a resident checker nor
an automatic module DAG is justified by the current small return fixture. Large
K, cold missing closure D, and search postings S(q) still need explicit limits
and remain part of the final goal. A future context optimization should be
selected only for a concrete required workload whose costs change the decision.

Finally, the optional body-search result trades fewer examined postings for
more reply bytes; do not reopen it as a default-planner speedup. The elementary
module and collision examples establish compatibility only. Useful-growth
claims must continue to use the existing whole-cost comparator and operating-
region conditions against an equally optimized local/package route, not theorem
counts, repeated cached uses or the existence of these passing controls.

### Revised ordering after concrete release-build evidence

Root identified, and this reviewer independently confirmed, a stronger release
blocker than the general consolidation wording above: in
`software/v5/ordinary_library_support/assemble.py:26`, `EXPORTER_SOURCE` is fixed
to `experiments/v5-local-checks/ordinary-missing-import-build-01/native-build/`
`MissingImportExporter.exe`. The preserved base `ordinary_package/build.py`
builds its earlier selected package, not the current overlay set and extractor.
The extractor's Lean source and earlier build adapter do exist in the repository;
the gap is a current complete repository-source build route, not missing original
mathematics. Hash-verified retained artifacts establish the tested package's
identity, **not** clean-clone buildability or bit-for-bit build reproducibility.

Accordingly, after the already prepared return test, the highest-payoff immediate
source/implementation task is **one current source-to-package recipe and complete
payload dependency map with no required experiment-output input**. Reuse the
existing build stages and exact selected source versions, retain the old tested
packages, and distinguish source files, generated build outputs and supplied
external runtimes. An expensive rebuild is not needed to identify/repair the
recipe in principle; root can choose a later bounded build only after the map
is complete and independently checked. No broader security or runtime claim
follows from the recipe alone.

The mixed-Init collision remains the highest-payoff *ordinary mathematics
compatibility* decision, but should proceed in parallel as the already-scoped
private/public exact-match source analysis, not consume another native campaign
ahead of a buildable current product. Selected-context scaling remains third in
this immediate ordering, subject to the explicit K/D/S(q) limitations above.
This revises the earlier relative ordering in response to a concrete dependency,
not an instruction to stop core mathematical work or to label the present
bounded package a final v5 release.

## Saved public native return01 outcome audit (2026-10-23)

Reviewer: `return_actual_audit`. **PASS for the selected public ordinary-project
proof return and actual new-unit admission.** This audit reads saved files and
recomputes their hashes/JSON relationships independently; it does not execute or
import product code, rerun a control/native campaign, open owner/database state,
build a module, or mutate Git. The canonical workspace guard passed. Earlier
passing campaigns are preserved, not requalified by this section.

### Selection, runtime and preserved artifacts

Run: `experiments/v5-local-checks/ordinary-project-return-native-01`.
Both original and saved selection bytes hash to
`435b90e12d9f33070d428c494fde83ed8137128d00b90a5478d7bb9d7695dd90`.
All four original/source-snapshot pairs and all 152 selected runtime/package/
prior-artifact pins independently match. These include the reviewed harness
`5c9d1d3bc7cf66e3aaa5ca46845a78508127e81aa3b1a28e98de95ff59159290`,
utility `20f6c613eb8fdd051b1f7df923e528e2c01874eb2e2c6277e3aca73d8475ccfd`,
and package profile
`0d8a9ec4d3509e60f8e3155313b1023230c7f9b4f36f103e55464d2c866ae1b5`.
This is explicit-runtime identity evidence, not a hermetic-toolchain claim.

The complete before/after maps each contain exactly 16 entries. Every entry's
length and SHA-256 matches its counterpart, current saved file and prospective
selection pin. This covers the nine earlier branch artifacts plus the already
paid module's manifest, native report and five artifact parts. Its exact module
name remains
`DMKNBridge_450bf7c15f3af7aa703934147ce9cd2fa1fbb5a50ec2dca7f7e41bbf1714f458`.
Manifest targets, semantic/foundation binding and source context agree with the
selected request. No module re-export or owner initialization occurs in this
selected invocation; its sole public operation is `contribute`.

### Actual mathematical return and publication bytes

The public stdout JSON equals the saved report's public response, and its nested
result equals `contribution/RESULT.json`. Its admission equals the separate
`ADMISSION.json` and both admission copies in the outer harness report. The
response is `ok: true`; the contribution status is
`CHECKED_CONTRIBUTION_WITH_DURABLE_PUBLICATION_BYTES`, with exactly one checked
and retained unit and one target/preview. The exact identities are:

| Binding | Identity |
|---|---|
| Requested and checked parent | `84dd6a9cf7ece45c4820ab3c28fc50ec072168c77e3cef9b890183bff5af9e13` |
| Acquired `CommonsPeerExample.applyFour_eq` ExportID | `0447787d07c5ada8730972d027bc25c5927e7c6552ef99c8fe4bdcda23285a6b` |
| Acquired UnitID | `d52aed3d1d0f94b8ee2236a7ee84435c983c9523dca0f100f4369c183c3d4e51` |
| New local root | `812a2a9a62f69bdd4e1d6dc1b4f57de9549a88c2aaca910c401589c3f9940337` |
| New UnitID | `f1e862985c8f8ec47efeb03d8eae7fe8128e1a7b45b34cc72022c546efd74d69` |
| New `CommonsReturnExample.mapFour` ExportID | `505276c90dd58ca6503040dae91cf285fe0311f633563918c9fd734ef1396019` |

The 9,409-byte canonical evidence has SHA-256
`a390259cad4124a50157af1f4e5072bdbc9fc520ee1ac2f635708ed44309adbe`.
Independent recomputation of the V2 domain-separated UnitID and ExportID yields
the identities above. The evidence unit equals both the emitted candidate unit
and the actual admission worker's sole `units.json` entry. Its descriptor tag 1
and inventory tag 2 identify the newly authored theorem, with matching name,
universe parameters and type. Candidate parent/target match, unresolved imports
are empty, and `source_records_enumerated` is zero.

Both candidate boundary and final evidence retain the exact acquired theorem
ExportID above and the original `applyTwice` ExportID
`b5054e3c29436f1fe8d175b47df405405f76683d7c1e27531d9e597f2e55ee02`.
The complete six-import census is exactly `applyFour_eq`, `applyTwice`, `Eq`,
`Eq.symm`, `Eq.trans` and `congrArg`, all occurring in the saved unit. In the
124-node proof DAG, acquired-theorem constant nodes 48 and 107 are reachable
from the proof root and carry distinct universe vectors `[0]` and `[2]`.
Their level-table entries are parameters `u` and `v`, respectively. Thus the
saved proof contains two distinct universe-instantiated uses of the same exact
acquired theorem; this is not a general application-count or novelty claim.

The selected source body matches the literal in the reviewed saved harness and
its request hash `983ed6617745cd80de643dc9b304b138b5f438bbf35f3ddf7e373e3261a8f6aa`.
The generated 1,647-byte source, input files, request groups and configuration
match their saved length/hash bindings. It publicly imports the paid module
before owner construction, and the actual author-worker argv names that project
path and generated source. The recorded construction line is exactly consistent
with `introducedNames=0 introducedSignatures=#[] checkedUnits=0`. The fresh
`mapFour` equality chain transports four iterations across `h`, under the stated
commuting-step hypothesis; the previously supplied theorem is not relabeled as
a fresh output. The approved project workspace remains empty.

The 1,976-byte preview has SHA-256
`553cb9134625229af88fed248e666c9b4e1cbeca01ba49dbbb0be361a0ba1c68`.
Independent canonical projection from the exact evidence inventory/type DAG and
its imported type bindings reproduces those preview bytes exactly. The saved
admission worker reports one checked extension, the exact new/parent module
names and the new theorem name. Its actual generated 7,240-byte chunk hashes to
`b76b79e9d708752a4e9ef14e505dd7c64557cca660d13fbfa1bb1dc4c247d8b7`;
its saved installation manifest retains the selected `32236aa3...` identity.

### Closure, original budgets and limits of the result

All four saved supervision layers (outer harness, public CLI, project authoring,
and actual admission) show exit zero, direct-child reaping, closed Jobs, zero
final active/terminated processes, no termination request or cleanup errors,
and empty stderr. Their command argv and observed log lengths match the saved
command/log files. The outer lifetime total of 12 process instances is distinct
from the configured maximum of eight simultaneously active processes.

The original inner 150-wall/90-CPU allowance is unchanged: 22.421995 wall seconds
and 10.09375 accounted CPU seconds (1.390625 controller + 8.703125 public Job).
The original outer envelope remains 180-wall/110-CPU/2,048-MiB/eight-process:
23.2980201 wall seconds and **10.953125 known inclusive CPU seconds**
(10.203125 Job + 0.75 wrapper), with 948,146,176-byte peak Job private commit.
The public Job receives a decreasing 121-wall/87-CPU/1,536-MiB grant; the CLI's
own request is 118-wall/86-CPU. Authoring and admission receive smaller
89-wall/82-CPU and 69-wall/76-CPU grants, each at 1,536 MiB. Their measured CPU
costs, 5.546875 and 1.375 seconds, are already inside the public/outer Jobs and
must not be added again. No unavailable-CPU reservation was needed or charged.
These are the recorded sampled-limit and explicit-runtime scopes, not stronger
hard-disk, hostile-project or system-wide containment guarantees.

The saved harness report is SHA-256
`d6afc3700e06af48a3b5b6fc2ec9a0c8e3390748499eda2beb76e7b23eb16b9b`;
the outer result is
`ed4d250725ca48f56b89b28e6e6ebb92c10b6c06364d342f9940077f05d22582`.
This closes the selected ordinary-project-to-commons local proof return using
the already-paid module. It does not establish index publication, peer acceptance,
new network operation, certificate production, general library compatibility,
mathematical novelty, useful-growth advantage or final deployable v5 completion.
No rerun is recommended; the full v5 goal remains unfinished.
