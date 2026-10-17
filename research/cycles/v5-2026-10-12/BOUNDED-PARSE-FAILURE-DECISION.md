# Bounded-parse screen: offline failure attribution

Status: narrow source selected by root; adapter authored, **not executed**.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Only new source is `software/v5/bounded_parse_guest/attribute.py`; all used
build, assembly, screen and previous-attribution sources/evidence remain frozen.

## Decision being supported

The selected new image failed its unchanged2^25 session cap:
`Session limit exceeded: 33557665 >= 33554432`. Its diagnostic reports one
guest call, zero proof calls, `FAILED_NO_ACCEPTED_CAPSULE`, null result and null
session statistics. The saved128 segment files are not a complete capsule.
No cap increase, guest rerun, proof funding or stage-host build is selected.

The economical next action is one bounded offline interpretation of already
saved samples, with the new ELF and its own link map. It should show which
retained machine-code symbols and coarse categories occur in this failed prefix,
alongside the already adopted old-prefix report. This is a decision aid for
source inspection, not proof of a bottleneck or quantified speedup.

Read-only saved facts before adapter execution:131,614 stored sample events,
22,960 omitted, saturation true,39,570,878 observed instruction-start events,
stride256 and zero backwards reported-cycle events. Native/preflight134ms,
boundary verification13ms and guest/segment custody6484ms are **host wall phase
durations**, not CPU or proving costs. The reported maximum cycle153,071,138,503
is the trace event's coordinate, not the2^25 session-limit denominator.

## Existing helper reuse

Read the complete frozen `software/v5/aggregate_host/attribute.py`,25,115 bytes,
SHA-256 `0fc2ca9b35892cf86b3f8fdbf124db8cdb31f6cd20658125e2d6c23967c3a786`.
Its top-level code contains standard-library imports, constants and definitions;
the operational `main()` is guarded. Importing it under another module name
does not invoke its old operation.

Reuse its pure `elf_headers`, `map_intervals`, `sample_cells`, `attribute`,
strict JSON parsing and integer/digest validation unchanged. Do not copy or
alter interval resolution, namespace classification or count-conservation code.
Its `main` is intentionally not reused: it hard-codes the prior failed-build
revalidation record and `aggregate_host` snapshot location, incompatible with
the successful fresh direct build and current assembly contract.

The new adapter imports only the exact sibling helper in the selected source
snapshot after checking its fixed byte count/hash. It never runs the helper's
main, any old baseline attribution, a compiler, native checker, guest, prover,
subprocess or network call. Old successful attribution is read as data.

## Exact configuration and read closure

CLI: `attribute.py CONFIGURATION_PATH CONFIGURATION_SHA256`, isolated Windows
Python with explicit canonical cwd. Root's three-source snapshot contains
`tools/Run-V5-Check.py`, the new adapter and the frozen helper. The adapter's
snapshot location is exactly under `bounded-parse-pc-attribution-01/sources/`.

Configuration has exactly:

```text
schema = DMKN_BOUNDED_PARSE_ATTRIBUTION_SELECTION_V1
records = {the twelve named file pins below}
output = .../bounded-parse-pc-attribution-01/attribution
```

Each pin is exact `{path,bytes,sha256}`. Fixed record locations, below
`experiments/v5-local-checks`, are:

| Key | Exact relative file |
|---|---|
| build_result | bounded-parse-direct-build-01/RESULT.json |
| build_attempt | bounded-parse-direct-build-01-attempt.json |
| artifact | bounded-parse-direct-build-01/ARTIFACT.json |
| source_map | bounded-parse-direct-build-01/SOURCE-MAP.json |
| assembly_result | bounded-parse-image-assembly-01/assembly/RESULT.json |
| assembly_outer | bounded-parse-image-assembly-01/RESULT.json |
| assembly_command | bounded-parse-image-assembly-01/assembly/COMMAND.json |
| screen_result | bounded-parse-aggregate-snapshot-01/evidence/RESULT.json |
| screen_outer | bounded-parse-aggregate-snapshot-01/RESULT.json |
| screen_command | bounded-parse-aggregate-snapshot-01/evidence/COMMAND.json |
| diagnostic | bounded-parse-aggregate-snapshot-01/evidence/diagnostic.json |
| baseline_report | aggregate-pc-attribution-01/attribution/RESULT.json |

Further exact data reads are derived and rebound from those records:

- Current direct-build ELF and link map from ARTIFACT, including an independent
  pure ELF-header parse compared to ARTIFACT's saved headers.
- Actual assembled image from the current assembly result; image file hash and
  zkVM image identity are explicitly distinct.
- Saved current WIRE and H from the screen command and diagnostic. Check
  `DMKNAI02`/v2 and `DMKNA002`/v2 respectively, with the same exact A slot.
- Existing I receipt from `argv[12]` and the diagnostic's one parent row,
  SHA-256 `850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47`.
  This is an identity read, not new cryptographic verification or proof.

The configuration and frozen helper are also read and rebound. The adapter
checks relevant failure-override and absent-complete-capsule paths without
reading segment contents. No SDK/cache/compiler-tree scan,238-artifact reread,
41-source reread or prior failure rerun is needed. Build/source correspondence
is inherited from the independently adopted exact build/assembly records;
this diagnostic does not repeat that qualification.

Important source-map distinction: the new direct-build RESULT's
`source_map_sha256` refers to the old39-source build02 map. The supplied new
`SOURCE-MAP.json` is separately bound through current assembly COMMAND's
`selected_inputs`; do not compare these distinct map hashes as if they were
one record. The source map is evidence provenance, not DWARF/caller attribution.

## Exact selected anchors

| Object | SHA-256 |
|---|---|
| Direct-build RESULT | `694d205b63082ecd02536eb70b16ae08a271f06d66d5df95f296a51a607ce22b` |
| Direct-build ELF | `16b7f1a26bcabdf95bf6cd85da1c0f8e6cd6c8647c2b7b049c65c7332f0fc701` |
| Direct-build map | `b200d6322acfad9ab454f5fddbfb90dc08d1e476f3282b53956ab9a34e9f4581` |
| Assembly outer | `f92ac44d3b2b12c677e3dcbe819dd64703cfd9f1da00d01efd58bb68e49c47ab` |
| Assembly inner | `696774f9616ffd0f8a058eccf5fbf13f9f6b6e2eb0cfdbb5f7ee6acde75e6b7a` |
| Assembled image file | `e3ec2dbb7742bf6de81ebd0d226bd08f88d63c91e1658fdf262510c296857822` |
| Screen outer | `a4db15321bc9084ba5db4c7f4dbbb702a391909c8cafe7fd7d82f7ecec6237e9` |
| Screen inner | `bc7fae70d1a7cde35a3db76a075ff289d8e082dea90b4ec2f726fb05ed99ba05` |
| Current diagnostic | `dca409e07e44f7647c2b248167cadcba6f5ad0827af83a3aa3173e0aee0bda72` |
| Prior adopted attribution | `31b29b7a8888fbfa0337fbf3a72b3269d2facbf05513d0e27a23ac4ca91de84b` |

Actual A is
`173255698c2bc9030e7528297b627c59d6d35a605ec3a16542b2ba73e5107ac2`.
It is not the assembled file's SHA-256.

## Small report and rigorous interpretation

The sole output is a fresh `attribution/RESULT.json`, maximum16MiB.
Its two independent views are `current` and `previous`, each with:

- Global stored/omitted/observed counts, saturation and backwards-event status.
- Compact sorted `[window, retained_count]` pairs, preserving the actual trace
  coordinate. Missing windows are not declared empty; omitted events have no
  saved window. Do not align old/new window numbers as mathematical phases.
- Unchanged coarse class/category counts and top40 exact uniquely resolved
  symbol ranges: raw symbol name, address range, input object/section, class
  and retained samples. Ambiguous/outside/unclassified cases remain explicit.
- Conservative global missing-label count intervals. For retained category H
  and omitted total O, its count among all sampled events is in `[H,H+O]`,
  with shared denominator `stored+omitted`. These intervals share one missing
  pool; their upper endpoints cannot all be achieved simultaneously.

Per-symbol bounds are explicitly `unique_attribution_sample_count_bounds`:
they concern the helper's unique-attribution labels, not every sampled PC
physically inside a potentially overlapping symbol range. Known ambiguous PCs
are separate labels, not silently assigned to each matching symbol. The old
report's zero ambiguities must not be assumed for the new image.

The helper samples every256th observed instruction-start event deterministically.
Its cell limit is131072 unique `(window,PC)` pairs, not a uniform reservoir.
After saturation, old pairs can gain counts while unseen pairs are omitted.
Consequently stored fractions can be biased; omission bounds are exact missing-
label accounting, not statistical confidence intervals and not bounds on all
instruction/cycle/wall/proof costs. No fractions or speedup ratios are computed
by the new report.

An exact symbol identifies emitted machine code, not inline source provenance
or caller-inclusive cost. Encoded trait-implementation names may stay
unclassified under the unchanged anchored classifier. The absence of a literal
`canonical_size` symbol does not prove that all its inlined work vanished.
The top40 list explicitly reports truncation; class/category totals still cover
all retained samples. Saved old attribution is summarized only, not recomputed.

## Finite selection and stop condition

Root selected in principle one offline envelope:30CPU seconds,60wall seconds,
512MiB,2active processes. Source implementation does not launch it. Per-record
read bound is2MiB except current diagnostic and prior report at8MiB each; the
prior report is4,756,721 bytes and must not inherit a2MiB refusal. ELF/image
caps64MiB, map8MiB, WIRE16MiB, header192bytes, receipt64MiB. Total reads including
final rebind <=128MiB. The frozen helper retains its interval/match-count bounds.

Successful output means only `PASS_OFFLINE_PREFIX_ATTRIBUTION_ONLY`; all
mathematical/proof/guest/build counters stay zero. Failed source binding,
ambiguity/output-limit refusal or final rebinding yields failed offline evidence,
not permission to retry a guest or relabel the screen. Root owns exact source
selection, finite execution and independent actual outcome adoption.

Stop after this offline view and use it with the parallel
`AFTER-BOUNDED-PARSE-OPTIONS.md` theory comparison. The central decision is the
smallest justified acceptance-preserving next improvement, not another broad
campaign or a promise that larger caps alone will complete the current graph.

## Actual report and selected next direction: successful DAG summaries

The adapter subsequently ran once. The actual saved report is1,519,214 bytes,
SHA-256 `9f100a3f56f7645938fae6eb46803d6d742ddbb7cccfdc1070a58c0ae37f893f`,
with `PASS_OFFLINE_PREFIX_ATTRIBUTION_ONLY`. This author read it without
reprofiling or rerunning the old attribution. Independent assurance owns the
separate actual pin/closure audit.

The current118,588 uniquely attributed and13,026 outside-user samples have no
recorded ambiguities. Selected exact symbol counts are:

| Machine-code label | Retained samples |
|---|---:|
| `memcpy` | 14,620 |
| Serde deserializer trait `deserialize_any` | 13,529 |
| Serde `SliceRead::parse_str` | 6,032 |
| `Value` string-key `index_into` | 5,042 |
| Correspondence `fields` | 4,016 |
| Correspondence `validate_expression` | 3,953 |
| Correspondence `reference` | 3,653 |
| Correspondence `validate_level` | 1,890 |

Lexical decoding clearly remains represented, but the `serialization` coarse
class alone omits encoded Serde trait names. Generic memory/string symbols do
not identify callers. None of these counts establishes a cycle fraction or
that either failed prefix reached the same mathematical point. The22,960
omitted events and deterministic aliasing prevent a causal speedup conclusion.

**Directional decision: prioritize per-proof syntax-DAG memoization before
compact transport.** Source inspection exposes repeated logical work with a
direct same-language argument; changing JSON transport would replace a larger
decoding/trust boundary while leaving this repetition intact. Do not reopen
already completed parse-once or proof-tree-materialization optimizations.
The separate author's body/group-copy work is not duplicated here.

The actually selected checker source is
`modules/native/proof_validation/module_correspondence.rs`, SHA-256
`ee4f33a9d4896bd59b2456cb1712d13010d0838b8ba0be34c89c10ebba18bdf8`;
read-only comparison matched the frozen build02 project copy used by the new
direct build. `validate_expression`/`validate_level` avoid discarded output
trees but still recursively expand repeated DAG references. Committed types
and bodies use the separate unchanged `expression`/`level` methods.

A bounded read-only parsing/counting pass over the already retained current
215,540-byte WIRE (not project execution or mathematical verification) followed
the fixed binary frame extents, parsed the two saved JSON frames and counted
native DAG multiplicities. Exact EOF and backward child references were checked.
There is one nonfoundation `thm` root per frame:

| Frame / root | Rows | Distinct expression/level nodes | Unfolded expression/level visits |
|---|---:|---:|---:|
| 0 / expression1200 | 1,355 | 459 / 14 | 11,627 / 7,169 |
| 1 / expression852 | 1,009 | 85 / 8 | 153 / 31 |

Frame lengths are113,220 and101,687 bytes. Implicit universe-zero visits are
included. These are syntax graph counts, not timing measurements or a new
acceptance test. The first proof has18,796 original recursive visits over473
distinct nodes: enough concrete repeated-node structure to justify the seam
without another guest profile. Actual kernel checking remains mandatory.

### Exact invariant and preservation argument

For one top-level theorem-proof syntax call, freeze the Inventory, owner and
ordered universe-parameter list. Keep separate private expression/level maps
indexed by their native indexes. Cache only a completely successful summary
`(c,h)`, where c counts every predecessor `visit` in the unfolded subtree,
including repeated edges and universe zero, and h is its greatest relative
expression-or-level depth. A leaf has `(1,0)`; an ordered child list has
`c=1+sum(c_child)` and `h=max(0,1+max(h_child))`.

A hit can skip recursive structural checks only when checked arithmetic shows
`work+c <= 250000` and `depth+h <= 192`. It then increments cumulative logical
work by exactly c, not by one. Logical work is not measured CPU. If either
guard fails, continue the original recursive `visit` and constructor checks;
do not reject early or reset work. Only successful returns insert summaries.
The memo dies after that top-level proof; it is never a persistent admission
credential or a cache shared between owners/parameter contexts.

Induction on successful subcalls gives identical accepted syntax and final
logical work: a hit has already established every context-dependent check on
unchanged data, and its two bounds imply every skipped visit would succeed.
A miss retains the original constructor, child-extraction/backreference and
sibling order; successful child summaries compose the exact count and height.
For a failing bound, recursive fallback and the same induction on preceding
successful subcalls preserve the predecessor's first error and work prefix.
Malformed syntax cannot enter the cache. This is logical behavior equivalence,
not an assertion of identical timing/allocation failure behavior.

On a successful proof, expensive structural checks occur once per reachable
node, plus bounded cache operations per DAG edge. Sparse ordered maps give
`O((U+E) log U)` lookup work and `O(U)` storage, versus repeated tree traversal
T; name/parameter checks retain their own finite costs. Logical T is still
charged to the old acceptance cap, so sharing does not admit formerly refused
large expansions. This does not promise that the next guest fits its current
cap or quantify whole-workflow benefit.

Root now selects source-only `modules/native/proof_memo/lib.rs`,
`module_correspondence.rs` and `control_root.rs` as fresh successors. The
independent controls author owns `proof_memo/correspondence_controls.rs`, and
assurance owns equivalence/source review. Types, committed bodies, foundation,
proof checker and predecessor sources remain unchanged. No compile, guest,
proof or limit increase is authorized by this source selection.

### Memo integration: minimal source-only plan, 2026-10-16

Inspection of retained direct-build01 `RECIPES.json` (SHA-256
`e6fc21c18e114cc280f7a5fe9bba3beafedae31309e87f940c970ec89ec38510`),
its source/input maps and the frozen build02 unit graph supports **four** new
guest-target compiler commands: `nanoda_lib`, `dmkn_module_relation`,
`dmkn_aggregate_relation`, final guest. Only module directly depends on nanoda
in this retained graph; every descendant must nevertheless be recompiled so
its metadata names the new checker. No SDK, standard-library, dependency,
Cargo, graph-generation or native-host rebuild is needed.

The exact production Rust source closure is 32 files: two new `proof_memo`
files (`lib.rs`, `module_correspondence.rs`), the 14 unchanged `checker/src`
files selected by that wrapper, and the unchanged 16 compiler-read project
files in direct-build01's source map. The kernel files are `debug_printer`,
`demand`, `env`, `expr`, `inductive`, `level`, `module`, `name`, `parser`,
`pretty_printer`, `quot`, `tc`, `unique_hasher`, `util` (all `.rs`). Test sources
are behind `cfg(test)` and are not production inputs. Relative layout must be
preserved if snapshotting these files. Root must bind the two fresh files at
their post-control hashes and the other 30 against the retained map; this is
not a request for a new full-tree census.

Nanoda's retained graph unit is edition 2021, feature-empty, target
`riscv32im-risc0-zkvm-elf`, with the same release profile as the three existing
recipes. It needs exactly 15 externs: seven `noprelude` build-std libraries
(`alloc`, `compiler_builtins`, `core`, `panic_abort`, `panic_unwind`, `proc_macro`,
`std`) and `indexmap`, `num_bigint`, `num_integer`, `num_traits`, `rustc_hash`,
`semver`, `serde`, `serde_json`, with graph-pinned features. The other commands
retain their exact 11/10/11 extern edges; replace module's nanoda edge and all
fresh descendant edges explicitly. Preserve opt-level 3, abort panics,
overflow checks, no debug assertions, lower-atomic/custom-getrandom flags,
linker-plugin LTO on the three libraries and fat LTO on the final guest.
Give all four new crates fresh metadata identities and fresh paired
rlib/rmeta outputs; keep the startup address, linker and map behavior.

The retained dependency view can reuse 107 library pairs and 22 host macro
DLLs (236 files, 311,693,039 bytes), excluding the old nanoda pair of
6,360,054 + 2,446,327 bytes. These totals are arithmetic over the already
adopted input map, not a new artifact scan. A filtered fresh view avoids
exposing an old same-name checker to resolution. Existing compiler/runtime
and supervision helpers remain reusable. The frozen `build_projects.py` and
`recipes.py` hardcode three compiles, old checker reuse and old destinations,
so they need a separately selected thin successor, not an in-place edit or
unqualified rerun. The existing assembler executable/kernel remain reusable;
its Python provenance adapter likewise needs a fresh four-command successor
because its current admission checks intentionally require three commands
and `checker_compiles == 0`.

The **unchanged** `aggregate_host.exe` and `aggregate_host/snapshot.py` can
perform the next selected screen. Source inspection confirms the host receives
adopted A externally, computes the actual image ID, binds the expected header,
derives the same native conclusion from the wire, and verifies the retained
genuine I receipt. The memo preserves accepted syntax and logical bounds, so
the prior native implementation is a valid independent preflight oracle;
the guest still executes the changed code. The screen already changes only
the A slot at bytes 12..44 and accepts generic successful assembly records.
Keep I, foundation, policy, all mathematical member bytes, 2^25 cycle cap,
po2=18, and 128-segment bound unchanged. This is one changed-guest completion/
cost discriminator after source qualification, not a repeated proof campaign
or a guarantee it will fit. No controller implementation, compile, assembly,
guest, proof, new selection or Git operation was performed by this review.

**Selected source implementation, 2026-10-16:** root adopted the plan and
assigned only fresh `software/v5/proof_memo_guest/build.py` and `recipes.py`.
These narrow successors now implement the four-command path above, using the
existing bounded phase supervisor, 32-file production source mirror, exact
236-file dependency subset and unchanged finite build envelope. New selection
schema is `DMKN_V5_PROOF_MEMO_FOUR_CRATE_BUILD_V1`; exact keys are `schema`,
`name`, `adapters`, `production_sources`, `retained_artifacts`, `limits`,
`authorizes_four_compiles_and_retained_artifact_adoption`. Name is
`proof-memo-guest-build-01`; adapters/source/artifact entries are exact byte/hash
pins and the final flag must be true.

The builder binds the completed nine-control inner report separately from its
outer `DESCENDANTS_REQUIRED_TERMINATION` report and retains that failure in
provenance; it does not require or manufacture a wrapper PASS. For future
compiles it uses the established `allow_build_telemetry=True` path: after
successful direct-child exit, only remaining owned Job members whose exact
path/hash is the pinned MSVC telemetry executable may be terminated. Unknown
descendants still fail. No new process-grace mechanism or limit expansion was
introduced. Four commands have fresh metadata and only new outputs plus
filtered dependency directories in their search paths. Success emits seven
library/metadata/guest pins, ELF/link-map artifacts and explicit command counts.
Root owns exact selection, assembly adaptation and launches; independent
source review follows. No compiler, guest, proof or Git action by this lane.

**Fresh assembler source, 2026-10-16:** root separately assigned only
`software/v5/proof_memo_guest/assemble.py`. The adapter now imports pinned
frozen assembly utilities from its sibling source snapshot, without calling
the historical adapter's main function. It requires the independently adopted
new four-crate build, unchanged selected envelope, exact four command records
and eight logs, 32 production source files, two used build adapters, seven
compiler outputs and ELF/link map. It reuses the retained assembly binary and
kernel and does not reread failed Cargo lineage or compiler/dependency trees.
The outer selection must include the frozen helper as a third source alongside
the new adapter and `Run-V5-Check.py`; root owns that selection. CLI remains
`--guest-result`, `--guest-result-sha256`, `--output`. Success preserves
`PASS_NEW_AGGREGATE_IMAGE_ASSEMBLY_ONLY`, actual assembler-derived image ID,
image file pin and zero guest/proof/admission fields, so the unchanged cost
screen can consume it. The existing 60-second assembler timeout and outer
120 CPU/120 wall/1024 MiB/two-process envelope remain. Source review, actual
build adoption and any assembly launch are separate; none was performed here.

**Assembly selector correspondence review:** source-only review clears
`Select-ProofMemoAssembly01.ps1` at SHA-256
`e92a376b5a2a0bbf2b7f8593ec9fb21aa8f4d08dc86f0f49142ce5f993802f20`.
The three source snapshots provide the runner, new adapter and exact sibling
helper path. Its CLI, fresh output and unchanged finite envelope match the
adapter. Expected runtime/data closure is 84 distinct pins by source accounting:
21 Python/driver/kernel, 12 command records/logs, 32 production sources, two
used build adapters, seven compiler outputs, one link map, six build records,
and the attempt/prior-selection/supervisor-manifest trio. The frozen runner
permits zero-byte logs. No required consumed input is missing from this source
closure. This review did not run the selector, recount artifacts, inspect the
actual build outcome or replace independent actual/selection audits.
