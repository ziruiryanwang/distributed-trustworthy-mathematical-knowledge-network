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
