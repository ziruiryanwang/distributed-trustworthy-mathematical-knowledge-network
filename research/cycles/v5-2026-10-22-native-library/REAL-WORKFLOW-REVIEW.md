# Selected real ordinary workflow: source review

2026-10-22. `lean_workflow_trace`. Read exporter, basis wrapper and current
export-only worker in full; compared the fresh BootstrapSupport with its retained
source and reused the already reviewed core boundary. No runtime or Git changes.

**No source-level soundness blocker found for bounded compilation followed by
the selected owner-side export.** Receiver integration still has explicit
preconditions and two size/count mismatches to handle prospectively.

## Basis and source compatibility

The new BootstrapSupport differs from `software/native/BootstrapSupport.lean`
only in replacing umbrella `import Lean` with five narrower imports. It retains
the actual empty-environment `receiveSeed` path, checked insertion, generated
record comparisons, Quot initialization and exact final name census.

BasisSnapshot calls that receiver, then serializes only its actual returned
kernel records. The seed/inventory counts581/456 are consistency checks, not
authentication; the outer controller must bind the stated exact fixed-file
hashes before parsing/calling. No imported Init or producer environment enters
the basis writer.

`compareSourceBasis` checks the source's581 selected basis records under the
**legacy normalized representation**. Its definition height override and old
codec intentionally erase original hints/binder/universe labels and normalize
ordinary `all` metadata. Therefore this is not exact ordinary-source metadata
equality or a reason to import the local snapshot alongside ordinary Init.

This does not create an unchecked inference: every new exact ordinary unit is
still decoded and checked against the reconstructed basis, with actual generated
records compared. Binder/universe alpha-renaming is not a new axiom; changed
reduction heuristics or generated metadata may still cause an operational
refusal, which the concrete receiver must report rather than repair silently.
The separate checked owner-project bridge remains necessary for normal-source
use. Source-side normalized correspondence alone does not qualify that bridge.

## Grouping and selected closure

The exporter indexes one bounded local source environment, retaining only
inductive/constructor/recursor grouping records. Reused `owner`/`makeUnit`
select atomic groups, screen original records, collect type/body/recursor-RHS
dependencies and include native literal support. Basis/group straddles refuse.
Dependencies are owner keys, so Kahn ordering operates on the same units that
the pending queue creates; internal inductive edges are omitted deliberately.

Actual original declarations and generated records reach the metadata-preserving
codec. Neither exported inventory claims nor the source environment become
receiver authority. Cycles, missing source records, unsupported axioms and
unsafe declarations fail before a complete export is returned.

## Worker boundary and actionable integration limits

The reviewed OrdinaryWorkflowWorker implements **only export**, not basis
admission, artifact commitment or receipt production. It bounds the trusted
inventory read, imports the selected owner method at private visibility with
no plugins/extensions, uses an explicit runtime-first search path and writes
one fresh bounded inert bundle. This does not authorize peer binaries or source:
the surrounding controller must authenticate the selected owner artifacts,
runtime/library inputs and inventory before native loading/JSON parsing.

Handle these before selecting actual checking:

- Export defaults allow8192 units; catalog and CheckedExtension default batches
  allow1024. Preflight the actual result. Either refuse a larger one-shot request
  or explicitly use dependency-first bounded chunks with committed parents and
  fresh grants; never silently enlarge the limits.
- Export's8 MiB unit limit covers the codec packet, while evidence's8 MiB limit
  covers packet **plus** profile/import envelope. Wrap and validate the final
  bytes, and check the64 MiB batch limit, before reserving receiver work.

The full local-source census is bounded by262,144 records and can be reused for
multiple selected exports; it is not per-query global network enumeration.
The output closure is selected but may still be substantial. Actual costs and
compatibility remain unmeasured for this method until the one selected export
and subsequent receiver run finish; do not repeat older component controls.

| Reviewed source | SHA-256 |
|---|---|
| `BootstrapSupport.lean` | `8a5771cc9f4e51cc0072959174bdc3a917bb0684b3dfdc8cdda2318bb8fd1bb0` |
| `OrdinaryExport.lean` | `9cebb661bf75e2e36285b860533442ed7ec12d6d94775cde0b90d65b1ffb910b` |
| `BasisSnapshot.lean` | `8952d82460d972e4176becdc0f16e09015ccf8298c37898b55e7b7959057727a` |
| `OrdinaryWorkflowWorker.lean` export branch | `f199e1fa8c6fea417ed5bb273b59f535dcc626d030a4f2ff646c1070d291e70a` |

## Subsequent focused delta: basis/extend worker and build wrapper

Read the complete expanded worker and `run_workflow_build.py`; no runtime or
Git actions. No new trust-boundary blocker found. This extends the earlier
export-only review, not its original reviewed hash.

Every input path now reaches a bounded raw-byte read with a nesting64,
unsigned20-digit/UInt64 lexical preflight before Lean's general JSON parser.
Exact canonical encoding, duplicate-key rejection and authenticated input
identity remain controller obligations; this worker is not a peer gateway.
Basis invokes the actual fixed checked-basis writer. Extend restores the
protected complete plan, enumerates actual bounded parent names, decodes at
most1024 units, and calls the actual checked-batch writer. Earlier expected
names help syntax decoding only; they cannot become unchecked premises.
Fresh reports contain returned names/module/parent/count/size, not an arbitrary
caller success flag. Source hashes, snapshot hashes, clean supervision and
exact report-to-grant comparison still belong to the controller.

The build wrapper creates a fresh output directory and compiles exactly
BootstrapSupport, OrdinaryExport, BasisSnapshot and OrdinaryWorkflowWorker.
It does not execute export/basis/extend, rerun old tests or rebuild passed core
modules. It checks exact source equality against core05 and snapshot01 source
snapshots; the outer selection must also pin the compiled `.olean` artifacts
and runtime. It clears inherited Lean paths and gives the new build, core and
snapshot directories explicit search order. Compilation logs and timeout output
are retained; any failed compile stops subsequent compilation.

A source-only syntax-risk note was sent to root/author: worker decodePlan's
`modules.push` record and exporter final return use mixed-inline multiline
record layout resembling the previous parser failures. Normalize those unused
blocks if needed before snapshot, without changing semantics. This is not a
reported runtime failure or a reason for an extra experiment.

Delta hashes at this review:

| Source | SHA-256 |
|---|---|
| expanded `OrdinaryWorkflowWorker.lean` | `14ea003ee2a1e1a227072f119783421d161add89ebf32b2d635f16192bbe4b43` |
| `run_workflow_build.py` | `37e225ab87c11bfe06e79e0e4691a9c91273aa107d726e2b54294ba71dfedd37` |

## Actual workflow-build01 and prospective single owner export

Read saved `ordinary-workflow-build-01` RESULT, WORKFLOW-BUILD, selection and
compiler logs. **PASS_SOURCE_COMPILATION_ONLY:** BootstrapSupport,
OrdinaryExport, BasisSnapshot and OrdinaryWorkflowWorker each exit0 with empty
stdout/stderr. No export/basis/extension mode ran. All10 source snapshot hashes
and eight selected core05/snapshot01 source/olean prerequisites independently
match. The two normalized record blocks are syntax-only; compiled source hashes
are exporter`ecab2be2…9147bf` and worker`442c2d47…c77f9b` as selected.

The run has exit0, reaped child, zero final active processes, closed Job and no
cleanup errors. Cost:6.640625 Job CPU +0.40625 wrapper CPU =7.046875 known CPU
seconds;6.357105799950659 outer wall seconds;677,625,856-byte peak private commit.
No old core/method tests or builds were repeated. RESULT SHA-256 is
`be9b9b01f3093ad6abf694f479523634ac3f83d34020a4b9afdf604878df5a8e`;
WORKFLOW-BUILD SHA-256 is
`ad16a6b3be850c53922f6e271903abd26db92627a72b09332c4925c41e94ebd9`.

Read complete `run_owner_export.py`, SHA-256
`279ec7193e7ef7850c643183e9b17200d3c0d01b91c26c42961ff171714bd6bd`.
**No blocker for root's one bounded selected export.** It checks exact worker
source equality to build01, clears inherited Lean paths, reuses core/snapshot/
new helper modules, and selects the successful ReadFootprint01 artifact. The
`lean --run` entry elaborates the unchanged worker source, rather than directly
running its saved `.olean`; it does not rebuild or re-elaborate the method/core
source. It invokes only export, captures timeout/failure logs, bounds the local
bundle and reports `PASS_INERT_EXPORT_ONLY`. Its Python JSON read is of that
selected local writer's bounded output, not a hostile peer-parser bypass.

Outer selection must pin the helper prerequisites, producer artifact and fixed
inventory before this run. Independently observed method `.olean` SHA-256:
`451b1fd47389095ef5a1942176fb76d4f03588bf3545eba2fd8ef9ecb4266f2d`;
inventory matches the fixed`c81800ab…dba1b0` hash. Complete runtime-library
hermeticity remains outside this test's stated scope. Select admission budgets
only after inspecting the real closure; no basis checking, native receiver
admission, public distribution or growth result follows from successful export.

## Actual owner-export01 failure

Read the saved selected result and logs. **FAILED_OOM_WITH_CLEAN_CLOSURE.**
`owner-export.stderr.txt` contains the explicit marker `INTERNAL PANIC: out of
memory`; stdout is empty. No owner-export bundle or EXPORT-RESULT was produced.
The outer driver reports failure, direct child exit1/reaped, zero final active
processes, Job closed and no cleanup errors. Cost:22.765625 Job CPU +0.59375
wrapper CPU =23.359375 known CPU seconds;25.45874339994043 outer wall seconds;
1,613,631,488-byte peak private commit under the unchanged1,536 MiB limit.

Selection SHA-256 is
`293dc9befaafc41a6324cb71903136d9eced11a21537f2086738a7c35ce115ff`;
RESULT SHA-256 is
`85cd7f0b97c6bf5269a8ea640fb161ca743b2dd6def6f60e29bb2af327cc1e30`;
the stderr SHA-256 is
`cf6e327209e0b84b54d21e7f94dee3b0dbcb5dc178deaef11d95b6585d4c47e5`.

There are no phase markers separating producer import, indexing, closure or
encoding. Consequently the actual out-of-memory diagnosis is established, but
its exact phase and attribution to duplicate environments are not. The selected
source redesign exports from the current owner's `getEnv` instead of calling a
second `importModules`. Removing that explicit second import is a concrete
architectural simplification and a better ordinary publishing interface, not
yet measured proof that the same envelope suffices. Old export01 remains failed;
no retry, increased memory budget or unrelated resource investigation follows.

## Current-owner command and finite adapters: source review

**SOURCE_REVIEW_NO_BLOCKER_FOR_ONE_ROOT_SELECTED_RUN.** Read complete
`OwnerExportCommand.lean`, `OWNER-EXPORT-REVISION.md`, `run_owner_command.py`
and `select_owner_command.py`, and the relevant pinned Lean 4.34 source.
No runtime, compilation, implementation edit or Git action was performed by
this review. This verdict is not compilation success or export qualification.

The command obtains the current command state's `getEnv`, then its
`toKernelEnv`; it never constructs a second environment using `importModules`.
Pinned `Lean/Elab/Command.lean:213` supplies the current environment and
`Lean/Environment.lean:649` returns its checked kernel environment. The exact
requested root must be an actual `thmInfo`; a public `axiomInfo` view is refused.
The unchanged bounded exporter still checks source-basis correspondence and
selected dependency records. An inert serialized bundle never substitutes for
fresh receiver checking.

The driver correctly uses **no `module` header and no `import all`**. Pinned
`Lean/Elab/Import.lean:150-156` selects the private level for a legacy header;
`Lean/Environment.lean:2182` propagates that private import throughout the
transitive closure. `Lean/Parser/Module.lean:103` forbids explicit `import all`
without `module`. This source argument supports availability of actual theorem
bodies, including transitive Std records, rather than public axiom interfaces.
It does not prove that the selected real closure fits the current size limits.

The helper's narrow `Lean.Elab.Command` import is not a demonstrated missing-
elaborator defect. `elab` is registered with `builtin_command_elab` by
`Lean/Elab/ElabRules.lean`; `Lean/KeyedDeclsAttribute.lean` explicitly stores
builtin elaborators in a process-level table and seeds each extension's initial
state from that table. The ordinary compiler includes this frontend. Directly
importing every builtin elaborator's implementation is not required merely to
use its command syntax. The selected compilation, not this argument, will settle
any remaining concrete elaboration incompatibility.

The command bounds and lexically screens the fixed inventory before JSON
parsing, writes a fresh output with `writeNew`, and flushes four distinct phase
markers. Exact inventory authentication, canonicalization, duplicate-key checks
and receiver acceptance remain controller obligations. Owner imports can load
trusted native extension state: this remains an owner-selected source frontend,
not a peer-source endpoint or security sandbox.

The selector authenticates the failed01 selection, preserves its exact producer,
compiler, exporter and inventory pins, and removes only unimported snapshot/
worker dependencies. It snapshots the new command and two adapters under a fresh
operation name. The unchanged outer allowance is 120 CPU seconds, 180 wall
seconds, 1,536 MiB and four active processes. The wrapper clears inherited Lean
paths, compiles just the new command, imports the retained already-compiled
ReadFootprint method and emits the legacy driver. It does not recompile the
mathematics, invoke basis/receiver checking or produce certificates. Direct
exclusive log files preserve flushed diagnostics through outer termination;
the parent Job still supplies aggregate process/time/memory containment. Local
bundle parsing is explicitly inspection of a selected trusted writer's bounded
output, not the untrusted evidence reader. Complete toolchain/import-directory
hermeticity is not claimed by the inherited explicit-pin test mechanism.

Removing the explicit second environment is established by source inspection;
lower memory or CPU is not yet measured. The current command also imports Lean
elaboration machinery, so the total owner environment remains nontrivial. The
phase markers and actual output, if produced, are the relevant next evidence.
No automatic memory increase, second run, receiver admission, growth claim or
full-v5 completion is authorized by this review.

| Reviewed source | SHA-256 |
|---|---|
| `OwnerExportCommand.lean` | `ddea3ee0230701c298c0ba81283629d328f08aa08e54e64811ef65a635f6afb5` |
| `run_owner_command.py` | `0e4f1d4284adf6f4f622c20ca96d6bf75f6d4062c4dc304e54bd57ebb8f59dbb` |
| `select_owner_command.py` | `340ef2c870cf4f7d6aa365e76de209bb20d90dd417498f942a4dea5022b71825` |

## Actual command01 and minimal search-path repair02

Read saved command01 RESULT, wrapper/phase logs, output census and the revised
two adapters. **HELPER_COMPILED_EXPORT_BLOCKED_AT_IMPORT.** New command
compilation exits0 with empty stdout/stderr; compiled artifact SHA-256 is
`5534bf9c46c9b9752ab811c641b465863286ef85b969025af430da15477166db`.
The driver then exits1 at its first import: Lean chooses the earlier core05
`examples` directory, whose `ReadFootprint.olean` does not exist, instead of
the retained method01 artifact. The selected core05 directory is empty and the
method01 build root contains only `examples`, as independently inspected. No
export entry marker, bundle or EXPORT-RESULT exists; this was not an OOM run.

Direct child is reaped, final active processes0, Job closed and cleanup errors
empty. Cost:1.640625 Job CPU +0.5625 wrapper CPU =2.203125 known CPU seconds;
3.023401599843055 outer wall seconds;944,881,664-byte peak private commit.
RESULT SHA-256:
`e78c8dbd50e001e4f1184caddb09fe126709958a244055b91dfdf8e0b15995ee`.

**SOURCE_REVIEW_NO_BLOCKER_FOR_FRESH02.** The repair puts METHODS before CORE
in the explicit Lean path, reuses the command01 compiled helper and checks
exact helper-source equality. The selector pins that artifact and source,
uses fresh02 paths and retains the original resource limits. No old failed
operation is rewritten and neither method nor helper is recompiled. Moving
the inspected methods root earlier does not introduce older core-helper
artifacts. Runner SHA-256 is
`828c3b70b5ea23966fc4101c44f531cde12be2738c894d3e499b56dbfbe9ee99`;
selector SHA-256 is
`3feb0d0465f2f59739b235fb5f79114bc33389a1849dc09133a8d5156e3e984b`.
The prior source verdict's elaborator concern is now settled by actual helper
compilation. Export closure, memory sufficiency and receiver admission remain
unestablished. This reviewer performed no runtime or implementation edit.

## Actual command02: pre-entry OOM, not an export-closure measurement

The fresh02 run is now terminal. Read RESULT, both direct owner logs, wrapper
logs and the actual output census. **FAILED_OOM_BEFORE_OBSERVABLE_COMMAND_ENTRY.**
The retained compiled helper was reused, but owner stdout is empty and stderr
contains `INTERNAL PANIC: out of memory`. No entry/index/selection/output phase
marker, bundle or EXPORT-RESULT exists. Consequently this does not measure
selected-closure construction or establish that `Export.indexSource` ran.
The private-all owner/compiler import path still fails within the selected
envelope; removing the previous explicit second environment was insufficient
for this route. The exact internal allocating call remains unknown.

Direct child exits1 and is reaped; final active processes0, Job closed and no
cleanup errors. Cost:27.078125 Job CPU +0.421875 wrapper CPU =27.5 known CPU
seconds;30.268893599975854 outer wall seconds;1,611,055,104-byte peak private
commit under the unchanged1,536 MiB limit. Selection SHA-256 is
`f8ec045b79d359e834dee517e642b65218ce8fb1b8c38065e815d2f18f296fe9`;
RESULT SHA-256 is
`e639c485ce5de57b6d41936f23b8f859c70eb0ed814c6fd44a5de587538fd392`.
The stderr hash is the same explicit30-byte panic text recorded for export01.

Do not repeat this same private-all frontend or raise memory merely to obtain
a component pass. A subsequent route needs a source-level reason to avoid the
large private compiler/environment import, or a changed practical library
boundary. Root owns that architectural choice. No mathematical export,
receiver admission, cache advantage or growth benefit follows from02.
