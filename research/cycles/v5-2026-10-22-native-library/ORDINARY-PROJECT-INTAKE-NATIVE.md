# Approved-project extraction: exact Python/native contract

2026-10-24. Author: `project_intake_native`. **Source/theory proposal for
independent review; not implementation, execution, acceptance or release.**
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
No build, project import, owner opening, experiment or Git mutation was performed.

## Decision and scope

Allow a local operator to fill a retained ordinary candidate's genuinely missing
declarations from explicitly approved, already-compiled non-Std Lean modules.
Reuse the existing private importer, complete-proof exporter, protected parent
lookups, completion planner and independent admission. Do not build another
acceptance engine or make certificates obligatory.

The fresh source pair, only if root selects implementation, is
`software/v5/ordinary_project_extraction/library_extraction.py` and
`software/v5/ordinary_project_extraction/MissingImportExporter.lean`. Preserve
the old controller/native sources and shared `OrdinaryExport.lean`/codec bytes.
The new native entry point still imports the retained compiled shared helper.
No helper modification or full dependency rebuild follows from this proposal.
Root owns the separate public facade, profile/map and any runtime selection.

The user has no existing project to provide. Do not ask again, download mathlib,
or call a controlled compatibility example external-user usefulness evidence.

## Local approval document and Python API

Use exactly these fields in the locally supplied document:

```text
schema: "DMKN_ORDINARY_TRUSTED_PROJECT_EXTRACTION_V1"
project_search_paths: [absolute directory string, ...]
modules: [structured Lean Name, ...]
```

No other fields are allowed. In particular there is no source, working directory,
meta flag, plugin, script, Lake command, toolchain override or remote locator.
This is a local execution selection, never peer mathematical evidence.

The controller successor preserves its existing positional arguments and keyword
names. Its exact extended signature is:

```python
extract_retained(owner, parent_root, retained_directory, *,
    request_sha256, candidate_sha256, modules=None,
    project_selection_raw=None, project_selection_sha256=None,
    exporter, profile, output_directory, parent_deadline,
    make_budget, account_worker_cpu, check_parent)
```

Exactly one mode is permitted:

| Mode | Required local inputs | Refused inputs |
|---|---|---|
| Existing Std | `modules` supplied; existing `selected_modules` grammar | Either project-selection argument |
| Approved project | `modules is None`; selection is exact `bytes`; its expected SHA-256 is supplied | Missing pin, caller-supplied target override, fields from candidate/peer metadata |

`project_selection_sha256` is 64 lowercase hex characters. Strictly parse the
bounded selection, reject duplicate JSON keys, and require canonical re-encoding
to equal the raw bytes. Verify `sha256(raw)` against the operator-provided pin.
The whole document is at most 1 MiB. The pin records the operator's selection;
it is not a signature, independent authorization oracle, or hash of transitive
project artifacts. The public facade must obtain the document/pin as explicit
local command inputs; neither is read from the retained candidate. Do not accept
an authoring selection implicitly as an extraction selection.

### Exact selection grammar

`project_search_paths` has 1 through 16 ordered, distinct entries. Each is a
nonempty string of at most 32768 UTF-8 bytes, with no control character (code point
below 32), search-path-list separator, or literal `.`/`..` path component. On the
currently supported Windows lane accept ordinary absolute drive paths only;
reject UNC, device and extended-namespace spellings. Separators may be `/` or
`\`; validate raw components before `Path` normalization. Reject duplicates
under the current platform's `Path` equality. Reuse `A.C.ordinary(...,
directory=True)` to require existing directories and reject reparse/symlink
ancestors. At most 128 components are allowed. These are root checks, **not** a
recursive authentication or sandbox of every imported artifact.

`modules` has 1 through 16 distinct structured names, each using the existing
`E.name_key`/`ExprCodec.decodeName` format, not dotted source text. Each name has
1 through 16 string components, each 1 through 96 ASCII bytes matching
`[A-Za-z_][A-Za-z0-9_]*`. Reject Windows reserved basename components,
case-insensitively (`CON`, `PRN`, `AUX`, `NUL`, `COM1` through `COM9`, `LPT1`
through `LPT9`); the grammar already excludes other reserved spellings. No
numeric components, separators or anonymous names. Each canonical name is at
most 4096 bytes; the canonical modules array is at most 65536 bytes. Duplicate
names use structured-name identity. Project mode removes the mandatory `Std`
prefix and raises only its component bound from 64 to 96. The original Std
controller grammar remains unchanged. Root selected 96 before execution
because already-generated `DMKNBridge_<64hex>` module names have 75 ASCII bytes;
this supports those existing ordinary artifacts without rebuilding/renaming them.

Controller and native worker both enforce module/path/count/range grammar.
Filesystem ownership, exact selection hash, duplicate-key/canonical validation,
support pins and protected owner stability remain controller prerequisites;
echoed native IDs are not cryptographic verification.

## Exact native request and import

Retain the native CLI arguments `sysroot request output`. Std mode emits and
accepts the existing six-field `DMKN_ORDINARY_MISSING_IMPORT_REQUEST_V1`, retaining
its Std-only guard and behavior. Do not silently broaden the old schema.

Project mode uses exactly the following nine fields:

```text
schema: "DMKN_ORDINARY_PROJECT_MISSING_IMPORT_REQUEST_V1"
profile_id: exact current portable semantic ID
context_id: exact retained receiving parent root
basis_id: exact current foundation ID
modules: approved selection's exact ordered modules
targets: exact ordered missing names derived by the retained-candidate binder
project_search_paths: approved selection's exact ordered roots
project_selection_sha256: verified local selection hash
capacity: {units: U, bytes: B, encoded_nodes: N}
```

All three IDs and the selection hash use the existing lowercase-hex64 grammar.
The capacity object has exactly its three fields. Values are JSON integers,
never booleans/floats: `1 <= U <= 32`, `1 <= B <= 4194304`,
`1 <= N <= 131072`. Targets are nonempty, unique, at most 32 existing-valid
structured names; they are **not** restricted to filesystem module identifiers.
The entire canonical request remains at most 1 MiB with the existing lexical,
depth and frame bounds. Missing target names cannot be supplied independently
by the caller. The native worker refuses an already-warranted requested target.

Before import validate the full request. Set the artifact search path explicitly
to `[sysroot/lib/lean, *project_search_paths]`, preserving project-root order.
No inherited `LEAN_PATH`, source directory or helper directory is appended.
Runtime-first resolution prevents a project search root from shadowing an
installed runtime module through search-order precedence; it is not a claim
that arbitrary local artifact bytes are trustworthy or hermetically fixed.

Load exactly one selected environment using the same runtime and
`importModules ... (plugins := #[]) (loadExts := false) (level := .private)`.
Use ordinary imports only. Targets must have complete safe, nonpartial,
nonaxiom records. Missing private proof data is a refusal, not permission to use
a theorem signature as an axiom. No automatic source compilation, package
resolution, download or code initialization is added. Locally approved artifact
deserialization remains a local trust boundary, not hostile-binary isolation.

Use the already reviewed `OrdinaryModule04.nativePath` rule at actual native
filesystem/import boundaries: normalize ordinary drive paths for extended Win32
access only if no normalized component ends in dot/space; otherwise retain the
original spelling. Keep selection/request/report spelling unchanged. This
preserves the referent instead of silently changing it. It does not add
UNC/device support. Root chooses the exact successor integration, not a second
unreviewed path workaround.

## Remaining capacities and honest bounded refusal

After the existing retained-input reconstruction and successful initial binder
validation, compute from those **same exact bytes**:

```text
U = 32 - len(validated_candidate["units"])
B = 4194304 - len(candidate_raw)
N = 131072 - initial.total_nodes
```

`initial.total_nodes` is already available on `NEEDS_LOCAL_INTERPRETATIONS`.
Refuse nonpositive capacity before starting the native process. Retain the
existing bounded reread for the original unit count; do not introduce another
proof traversal or derive node counts from text length.

Project-mode `Export.Limits` is set as follows; all unlisted fields keep existing
defaults:

```text
maxTargets = 32
maxUnits = U
maxUnitBytes = B
maxOutputBytes = B
maxScanNodes = 2097152
codec.maxUnitNodes = N
codec.expr.maxExprs = min(existing default, N)
codec.expr.maxLevels = min(existing default, N)
```

The protected lookup/reply protocol remains unchanged (65536 lookups, 1 MiB
frame, 32 MiB aggregate protocol bytes). Existing source/group census, edge,
depth, name/literal and native-process time/memory/CPU limits remain. No public
quota is raised. `maxOutputBytes` bounds the shared exporter's sum of unit JSON
bytes; it is **not** the full supplement byte bound.

Native traversal `scanNodes` and portable serialized nodes are different
quantities: traversal omits universe DAG nodes and can count metadata erased by
the codec. Neither equality nor a useful domination is assumed. For each emitted
unit `[format, descriptor, inventory]`, calculate the exact encoded node count as
`DeclCodec.descriptorNodes(descriptor)` plus `DeclCodec.inventoryNodes(row)` for
each inventory row. Sum over units and refuse if the sum exceeds `N`, before
writing the supplement. Those functions count the same level/expression array
entries as Python `ordinary_evidence.inspect_unit(...).total_nodes`.

This uses the shared helper **unchanged**. Its per-unit codec cap is not an
aggregate prospective cap: an export may complete and then fail this final
aggregate census. Before that check, at most `U * N` encoded nodes can occur in
successfully encoded units; this bound is not a bound on imported-environment
memory or every intermediate allocation. Per-DAG codec limits, separate scan
and unit/byte limits, and process supervision constrain other work. Some limits
are checked after constructing one item. Do not promise zero futile work or
that content counters alone are a security sandbox.

After assembling the unchanged full supplement, serialize it and require
`0 < full_bytes <= B` **before opening its fresh output file**. The wrapper,
targets, boundary rows and statistics all count. A small `B` can cause a late
wrapper-overhead refusal even when summed unit bytes fit. Preserve and charge
that outcome; do not add an unsupported feasibility claim or automatic retry.

## Output, acceptance and accounting

Keep `DMKN_ORDINARY_MISSING_IMPORT_BUNDLE_V1`, its exact seven statistics fields,
and the lookup/reply/DONE schemas unchanged. In particular do **not** add an
`encoded_nodes` statistic to the supplement: the current planner rejects unknown
statistics fields. Capacity and project selection belong in local retained
`SELECTION.json`/result metadata, not portable authority.

The controller validates DONE, protocol and boundary replies as before, reads
at most `B` supplement bytes, and calls the unchanged `complete_candidate` with
the original candidate/targets/claims, real parent lookups and public limits.
It must still enforce the planner's distinct combined raw-boundary-row sum,
output-name sum, selected-name union, encoded nodes, unit count, evidence bytes
and composite-wrapper byte checks. Passing the three native capacities does not
imply these other conditions. No new "remaining names" shortcut is asserted.

The returned status remains `EXTRACTED_COMPLETION_INPUTS_NOT_ACCEPTED`, with
`mathematical_acceptance: false` and explicit next action `complete` using the
same parent. Project-mode local result metadata records selection hash, exact
roots/modules, derived capacities, native executable pin and trust boundary
`OWNER_APPROVED_LOCAL_PROJECT_PRIVATE_ARTIFACTS_NOT_PEER_BINARIES`. Preserve
`project-selection.json` exact bytes with a pin beside request/candidate/bindings.
Std result behavior remains unchanged.

Final mathematical authority comes only from existing independent admission of
the complete ordered supplement followed by the unchanged consumer. This
establishes the exported judgment under the receiver's exact accepted name
interpretation, conditional on existing checker assumptions. It does not prove
whole-project equivalence, same-name semantic equality, arbitrary library
compatibility, or agreement with human intention. Whole inductive groups,
collisions, unsupported declarations and conflicting policies keep their
existing refusal rules. Project artifacts never become receiver warrants.

Use the same stable owner/parent, fresh output separation and remaining parent
allowance. Extend existing output/support overlap refusal to every approved
project search root in both ancestor directions; keep facade catalog/custody
separation unchanged. Check approved root directory shape again after native work; do not
claim this detects every concurrent artifact change. All native work is charged
once on success or failure through the existing exchange/finally path; unknown
CPU accounting consumes its reservation and prevents continuation. Extraction
does not auto-admit, auto-rebase or repeat authoring.

## Smallest review and implementation evidence

Independent source review should decide this contract before root selects code.
Then pure/inert controls cover exclusive modes, malformed approval/path/name
grammar, wrong hash, exact retained missing targets, exhausted capacities,
runtime-first search construction, distinct scan/encoded counters, wrapper
overhead and unchanged Std/supplement fields. Existing unchanged receiver
evidence is reused. One separately selected small non-Std private-artifact
import with an actually missing target can test the new boundary; neither a
large cold library campaign nor another broad proof suite is justified here.

The remaining architectural limitation is explicit: importing a selected module
may deserialize its transitive private environment, and missing group recovery
may census it. No total-source-cost `O(missing closure)` claim follows. This thin
adapter does not solve oversized cold onboarding; an independent root-directed
analysis owns that question. It also does not bypass existing anchor support
identity: facade/profile changes may require a fresh correctly bound anchor,
not migration of prior authority.

## Source identity used for this contract

Paths are below `software/v5/`; hashes are SHA-256. These are inspected source
identities, not an execution or product-acceptance manifest.

| Path | SHA-256 |
|---|---|
| `ordinary_lean/MissingImportExporter.lean` | `7efb8bfa768a97ebcced687fd2a5acb0227e65eb2260e82d1726d8f361b27fbb` |
| `ordinary_lean/OrdinaryExport.lean` | `1d4df6817098f5ad9cd0106d98f39a6905a55be8b23484294b5c3d22653a7d4f` |
| `ordinary_lean/OriginalDecl.lean` | `bfb5fc910808d9dc178977cfa6edeacf0b5cbfe7bd99bc6277ee11a456d516c1` |
| `ordinary_lean/ordinary_evidence.py` | `fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6` |
| `ordinary_lean/portable_candidate.py` | `29ae111a362472b09b2b1ff16b567b352be793d76c2cd1b5421e0aee29219331` |
| `ordinary_extractor_binding/library_extraction.py` | `28ff83c5a8561b9f5250e9be08b34744aedd23757765feb174e1504d700308aa` |
| `ordinary_library_package/library_completion.py` | `b587c74e156c81a392f394b263b27b13de427753c41009ecc3b99193f88b93d9` |
| `ordinary_project_package/ordinary_contribution.py` | `b8eefe6af368d8a7f5c498d563a12b31416c48c877ea471361eadd2a56a90b31` |
| `ordinary_module_anchor/OrdinaryModule04.lean` | `901e4fc06351f6ad658eba9b5ea23ab644648646c8567fc035b057aa1883cfe8` |

## Native source implementation checkpoint

Root separately selected native source implementation in
`ORDINARY-PROJECT-INTAKE-SELECTION.md`. Fresh
`software/v5/ordinary_project_extraction/MissingImportExporter.lean` is now
written, SHA-256
`95bca1e1913d7c1b809df698b38e9761d13fbf4245be4e5abdaeccc09c70f326`.
It has not been compiled, executed, packaged or accepted. Independent source
review is pending; no owner or runtime was opened and Git was not mutated.

The implementation separates the exact old Std request from the nine-field
project variant. Project mode validates structured module identifiers, approved
ordinary-drive directory spellings, exact selection-hash shape and positive
capacities before import. Its single private environment uses runtime-first
roots with no plugins/extensions. Per-unit encoded limits and separate scan
limits feed the unchanged shared exporter; the exact post-export aggregate node
census and complete-wrapper byte bound run before output creation. Lookup/DONE,
supplement fields and final mathematical acceptance remain unchanged.

The reviewed `OrdinaryModule04` filesystem-spelling rule is copied locally and
used for request/output I/O and artifact search paths, including Std-mode paths.
This deliberately adds referent-preserving long-path handling to the new
executable; old Std schema, prefix restriction, limits, target rules and output
layout are preserved. Original path spellings remain in controller metadata.
Root/reviewer should include this small common-I/O boundary in source review;
it is not a new path authority or a claim of byte-identical executable behavior.

Post-write read-only hashes confirm the predecessor native exporter remains
`7efb8bfa768a97ebcced687fd2a5acb0227e65eb2260e82d1726d8f361b27fbb`
and shared `OrdinaryExport.lean` remains
`1d4df6817098f5ad9cd0106d98f39a6905a55be8b23484294b5c3d22653a7d4f`.
No codec or receiver source changed. Prospective late-refusal limits and cold
private-import costs retain the qualifications above.

## Changed-native build adapter readiness

Root subsequently selected the project-only 96-byte component amendment and
two source-only build adapters. Current native source SHA-256 is
`437caa5aa3a2085db26b0478db082c492cc8d3aa2f708f0be44e5385a1ede54e`;
the earlier 95bca1e1 value records the pre-amendment source, not current selection.
Std behavior and all used artifacts remain unchanged.

Fresh `software/v5/ordinary_project_extraction_package/assemble.py`
(`c9142540c8e91e550c8f437373845e5523641466eab21e6b7fe89b3e0df9274a`)
and `select_build.py`
(`2030ece95b5e558a4c84c0631fa9feb958687e6a8ddfe36390c052c157538816`)
are ready for independent source review. Neither has been run. The selector
requires the exact assembler SHA as its sole argument and writes one finite
selection; it does not launch it. Only root may select the actual operation.

The adapter uses the existing fixed bootstrap, builder path/hash/copy helpers,
package loader and enclosing `Run-V5-Check.py` Job. It copies the exact five
retained helper `.olean`/`.o` pairs from the successful saved build, authenticated
by `EXTRACTOR-OUTPUTS.json` SHA
`f55d4c5b56fc299564b76d68c66d63d3090f439b44479b597b016113c4b53768`.
It compiles only the new exporter to Lean/C/object output and links it with
those unchanged objects: three compiler subprocesses, not a full rebuild.
The compiler search path contains only the copied shared-object directory;
runtime `bin` is the entire explicit PATH. Every subprocess has the same
nonrenewing inner deadline, and the original outer Job contains descendants.
There is no new supervisor or cumulative-process-count-equals-one assertion.

Proposed outer limits are 180 wall seconds, 120 inclusive Job CPU seconds,
1536 MiB and six simultaneously active processes. The controller has a shorter
160-second internal deadline; reported controller CPU is not confused with
inclusive child CPU, which belongs to the enclosing Job's saved result.
There are at most 178 selected immutable input files before the runner snapshot,
below its 256-file bound: base payloads/metadata, saved support, named runtime
files and selected source. Named runtime pins are not a hermetic toolchain claim.

The fresh destination is
`experiments/v5-local-checks/ordinary-project-extraction-build-01/integration/package`.
Its exact three payload replacements are `owner.py`,
`authoring/py/library_extraction.py` and
`authoring/bin/MissingImportExporter.exe`; the other 131 payloads are unchanged
from assembly04. `ASSEMBLY.json` retains `ASSEMBLED_NOT_ADOPTED`, profile,
installation and implementation identities, `changed`, `unchanged`, and exact
replacement pins. Native build facts are separate receipt metadata. All
selected inputs, staged sources/shared objects, compiled outputs and copied
payloads are rehashed before the profile marker. Partial failures are preserved
without retry. No owner/catalog operation, package adoption or mathematical
acceptance is implied by successful assembly.

