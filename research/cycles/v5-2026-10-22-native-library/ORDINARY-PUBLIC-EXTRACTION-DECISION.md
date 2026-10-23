# Public retained-candidate completion: reuse the installed-Std extractor

2026-10-23, `project_hook_design`; source/theory only. Canonical guard PASS.
No product import, build, test, native process, catalog opening or Git operation.
Frozen controls/package bytes are unchanged. Root subsequently selected the fresh
source helper described below; this note selects no runtime or package adoption.

## Decision and actual user workflow

**Next implement one explicit `extract-std` wrapper feeding the existing `complete`
operation.** An ordinary contribution has already produced a valid
inert candidate but lacks imported library declarations at its selected receiver.
The user selects that retained contribution, exact original parent and a small
installed-Std module list. The wrapper uses the retained-preparation helper,
extracts the missing closure above that parent, and returns pinned supplement,
prepared-map and target inputs ready for existing `complete_source`/CLI.
It must not reauthor the successful candidate, invent an axiom or silently rebase.

This currently has greater marginal payoff than extending the existing-project
source hook: that hook is already available, no real compatible project is yet
selected, and importing a project/new alias does not supply a missing proof to
the receiver. For trusted collaborators needing most of a conventional library,
ordinary pinned project imports remain preferable; the commons complements them.
This Std-only endpoint is not Mathlib/arbitrary-project interoperability. The
separate reverse-library result is already in ORDINARY-PROVED-LIBRARY-EXPORT-DECISION;
do not reopen that investigation or ship scratch theorem axioms as proved modules.

## Reuse exact existing artifacts; no native rebuild

Use `experiments/v5-local-checks/ordinary-missing-import-build-01/native-build/`
`MissingImportExporter.exe`: 697,344 bytes, freshly read hash
`9700c6c2944d327a648e3fcf83453ee1aa019d2f05c182feec13e78211711dc7`.
Its lower helpers and exporter are already linked; deployment does not need their
old `.o`, `.c` or helper `.olean` build directories. Copy the exact executable into
a fresh auxiliary package selection; preserve the current native acceptance core.
Use the same Windows Lean 4.34.0 runtime and its selected shared DLLs, with explicit
runtime `bin` precedence and scrubbed inherited Lean/Python environment variables.

The current installation pins `lean.exe`, `libInit_shared.dll`, `libc++.dll` and
the three `libleanshared*.dll` files. It does **not** hash-authenticate every Std
`.olean`/server/private/IR artifact in the imported closure. Existing evidence
assumes an owner-trusted fixed local installation plus those named runtime pins,
not a hermetic distribution. State that premise; do not infer public update
integrity from it. Never load peer-supplied binary modules under this exception.

The executable accepts absolute `(sysroot, request.json, fresh supplement.json)`.
Its inert request has schema `DMKN_ORDINARY_MISSING_IMPORT_REQUEST_V1`, fields
`profile_id=S`, `basis_id=F`, `context_id=parent`, `modules`, `targets`.
Those three labels are shape-checked and echoed, not interpreted in legacy domains;
use actual portable S/F/root and actual portable K replies. No legacy ID rewriting.
It allows at most 16 Std-prefixed modules; target names can be in their dependency
closure, e.g. `List.map_congr_left`. It fixes search paths to `sysroot/lib/lean`
and loads once with `plugins=[]`, `loadExts=false`, `level=.private`.

## Recover the prepared map from retained authoring, not from candidate claims

Reuse root's separately assigned retained-preparation helper, not another parser.
It binds REQUEST/candidate hashes, S/F/parent, target pin and every declared
header/group file; metadata Boolean fields need the proper metadata parser.
Reconstruct exactly the original basis/group name-to-ID map, reject duplicates,
and check its pairs against real K. Keep 32 groups/4 MiB aggregate/1 MiB files/
4,096 rows, ordinary paths and only exact declared filenames; no directory scan.
Return canonical `prepared-bindings.json` and its pin, never an acceptance token.
Do not regenerate `R.prepare`, fetch old evidence, reauthor or copy the store.
Actual `B.bind_candidate` on unchanged candidate/map/K supplies the missing set;
do not trust diagnostics or a caller subset. READY means extraction unnecessary.
Malformed original graphs/claims refuse before any native extraction.

## Public protocol and resource envelope

Factor the already exercised `run_missing_import_completion.exchange` protocol
into a fresh parameterized helper: no historical ROOT/database/profile constants.
Keep bounded reader/writer queues, sequential echoed names, memoized real-K replies,
1 MiB frames, a 32 MiB combined ceiling, 65,536 lookups, DONE/EOF/zero-exit and
joined-thread checks. Actual stdout and stdin each obey the smaller budget log cap
(default 1 MiB); stderr obeys min(1 MiB, log cap). Supply one original deadline and
parent cancellation checks; cleanup consumes the same enclosing allocation.
Bind output length, units, target set, labels and boundaries to request/DONE/K,
then pass original bytes and supplement through the already packaged planner/API.

**Direct reuse of the pinned Job backend is feasible and is the smaller choice.**
The old `exchange` relies on its experiment's outer Job; `commons.supervise` has
no interactive lookup callback. Reuse `installation._job_module.Job`, creating
Popen suspended with CREATE_NO_WINDOW, then `attach_resume` before protocol work.
Keep lookup in the current owner controller: no owner reopening, K copy or new
service. Poll the queue with a short bounded timeout even while idle; on each
iteration check original parent deadline/controller CPU and Job total CPU stats.
Job already enforces user CPU, aggregate native memory/process limits and kill-on-
close. This adapts the existing protocol, not a second mathematical checker.

On pre-attach failure kill/reap the still-suspended child; on any later fault kill
the Job and reap/join/close every child pipe/thread. Require zero active descendants,
clean exit, final stats and successful Job close before reporting extracted data.
Reserve cleanup via `budget.allowance(parent_deadline)`; legacy fixed waits must
not create a new deadline. Add final Job CPU to `budget.worker_cpu` once even on
failure; caller charges its parent ledger in finally. Missing accounting or uncertain
cleanup is failure, not zero cost or permission to proceed. A created child requires
final fresh-Job total>=1, active=0 and direct reap for measured CPU. Otherwise report
null/incomplete and poison worker CPU with infinity; caller conservatively charges
the full allocation, explicitly not measured CPU. No returned child costs zero.
Controller checks remain cooperative, as in the current owner API;
an outer supervisor is still needed for a hard controller-memory/CPU limit.

Pipe API: `exchange(argv, *, env,cwd,output,lookup,parse,name_key,budget,
parent_deadline,check_parent,job_type) -> (done,answers,protocol_bytes,report)`.
The extractor gets only derived missing names/reached lookup replies. Extraction
and admission are sequential. Separate CLI calls are explicit allocations with
linked historical costs, not silent renewal. One caller may compose both APIs
under one original parent allowance. Neither extraction nor its report accepts math.

Implemented source: `software/v5/ordinary_library_support/supervised_library_exchange.py`,
SHA256 `f6d0ee89d792f3741f74c790914dc8e21cf21dc7ca256bb03360dbc31907dea4`.
It emits fresh `EXTRACTION-SUPERVISION.json` on clean/failure outcomes, records the
actual protocol caps and attach/cleanup/accounting facets, and charges native CPU
once. Root owns `library_extraction.py` and package integration. This helper is
source-only, never imported/executed; final independent source review is pending.

The binary's fixed production caps are 1,024 units/2,097,152 scan nodes/64 MiB
output; new-group indexing can census up to 262,144 source records. Public combined
admission remains 32 units/131,072 nodes/4 MiB. Check available consumer capacity
first and refuse oversized actual output afterwards; process limits bound wasted
production. Do not claim the binary stops at the smaller admission cap, enlarge
admission silently, or rebuild merely to align constants before a demonstrated need.

## Refusals, costs and minimum new evidence

Refuse changed pins/parent, missing preparation files, conflicting names/IDs,
non-Std modules, unavailable private proof records, axioms/unsafe/partial records,
incomplete groups, unknown runtime, malformed IPC, exhausted allowance and unclean
exit. Full native receiver checks remain mandatory; accepted boundary names are
receiver interpretations, not proof of equivalence with an arbitrary local package.
Cost includes retained-request validation + local K materialization + private
module loading + reached missing-closure traversal/IPC + combined receiver checking.
Neither module loading nor current `catalog.context` is O(missing-closure-only).
Already accepted proofs are not serialized down the lookup pipe or rechecked merely
because extraction reaches their names. The earlier legacy extraction measured
3.6365 wall/1.796875 known CPU seconds and 270,876,672 peak Job private bytes for
two units/34 lookups; it is not a guarantee for larger modules or a whole-cost win.
Next evidence should test only public preparation/supervision/portable wiring,
after source review, using existing eligible state. No rebuild, new mathematics,
certificate campaign or repetition of the proven legacy extraction is justified.
