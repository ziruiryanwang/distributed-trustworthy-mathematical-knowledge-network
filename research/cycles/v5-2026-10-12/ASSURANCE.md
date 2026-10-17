# V5 resumed integration assurance — 2026-10-12

## Explicit implementation resumption after guide delivery

### Memo implementation and exact control selection CLEAR (2026-10-16)

Independently reviewed fresh33,230B `proof_memo/module_correspondence.rs`, SHA
`7877ee22c7e1d4350858e67c8cebbedf057dee1820cd9f61940e37cf51f6508e`;
1,138B lib SHA `51a83c7820bcbd0750fac54e6f95b8e5992911ce023d139c4cbb28afcf9416eb`;
64B control root SHA `78e3bc1d708d86e33414050e598d09667321daa64904adde4f5dc3d3947d7a20`;
and18,660B controls SHA `94907f917ae2d59542f492de8fc08fbc291023dac1de4a34bda67e03fe6c7917`.
Exact diff against frozen proof_validation confines semantic changes to the
selected successful-syntax memo; expression(), level(), reference, all
declaration/body checks and native-kernel source paths are unchanged. New
counters are cfg(test) only.

Each top-level validation creates separate expression/level maps. Only completed
successes are inserted; child summaries include repeated edges and mixed-domain
depth. Checked incoming work/count and depth/height guards run before visit;
failed guards leave work untouched and fall through the original ordered
checks. Summary addition cannot introduce an overflow refusal on a successful
old trace: successful subtree count is bounded by250000 and height by192.
The earlier fixed-context induction applies. Allocation/resource-exhaustion
behavior and total speed remain outside its equivalence claim.

Exact49,406B selection SHA
`75291daea284ec42c991186667011bfbd10338a96432ec095c9f3a2ce37937f6`
and973B configuration SHA
`a74cfb456e0e8cf2f02d8e8f1a808d822cf6f5bab001c11294638f7d5a202c5c`
match the cleared adapter/selector. Reviewer rehashed all5source and200runtime
pins (921,813,400B), with zero mismatches, and confirmed all174retained recipe
pins and exact9test list/order. The fresh operation directory was absent.
Root may execute this one60CPU/120wall/1024MiB/six-active serde-only build and
control allocation. No guest, kernel, proof, larger cap or release is cleared.
This entry records prelaunch review, not execution or a passing outcome.

### Memo control proof-obligation review (2026-10-16 continuation)

Independent reviewer read all nine fresh `proof_memo/correspondence_controls.rs`
groups against the unchanged tree-producing visitor and cleared theory above.
They compare complete caught semantic panic payload and cumulative work, check
actual hit/skip counters, and cover distinct domains, shared-DAG success,
resource-bound fallback, mixed expression/level height, malformed shared nodes,
fresh proof contexts, sibling/reference ordering, and eager inventory checks.
The retained two-delta group separately checks exact structural visit counts;
it does not claim kernel admission or guest-cycle/proving improvement. No
decision-changing coverage gap was found. New implementation and concrete
selection/result review remain required; no test or compiler ran in this review.

### Selected memo control adapter and selector source review

Root subsequently selected fresh memo source and a serde-only differential
control, not guest execution. Read complete7,141B `proof_memo/control.py`, SHA
`0656fe3988571d05b542c03592f0cb511965c94f6b4d3080fbe3a3b7fe4b6502`,
and5,763B `Select-ProofMemoControls01.ps1`, SHA
`0a5c372a0e6d9d3a6af8e5249f810d844cdf366464c43388d4243aefb5b669ab`.
Independent selector PowerShell parse has zero errors; reviewer executed neither.
No concrete blocker found in these two sources.

The adapter substitutes only crate name, test root and fresh output in the
exact adopted serde-only rustc recipe, then runs that new test binary once.
No Cargo/checker/dependency rebuild, native mathematical check, guest or proof
is added. Explicit allowlisted environment uses pinned retained linker/profile
data and the exact retained wire. Descendants remain in the selected outer Job
without breakaway; no second controller hierarchy is introduced. Actual group
names plus full all-passed count must match the unique explicit test list,
and the produced binary hash is rebound after controls. Failed child/timeout
cannot produce the passing inner status.

The selector merges174retained recipe pins with current Python/profile/host
tool/wire/configuration records and selects five test source files; unused
production lib.rs is correctly outside this compile closure. Planned outer
60CPU/120wall/1024MiB/six-active envelope remains finite.2MiB log and64MiB binary
size checks occur after each child, **not hard in-flight disk quotas**; implicit
OS/runtime facilities remain trusted. Final Rust/control source review and
actual exact selection/pin checks are still required before root execution.

### Per-proof successful-syntax memo: independent theory clearance with obligations

This is theory/source review, not implementation or execution authorization.
Read the complete current `modules/native/proof_validation/module_correspondence.rs`
(SHA `ee4f33a9d4896bd59b2456cb1712d13010d0838b8ba0be34c89c10ebba18bdf8`)
and its complete differential controls. The proposed optimization is sound in
principle **only under the invariant below**. Current frozen source is unchanged.

Fix one immutable Inventory, owner string and ordered universe-parameter slice
for a single top-level local-theorem proof validation. Rows, names, foundation
membership and reference interpretation do not change during this call. The
existing syntax routines mutate only the cumulative `Inventory.work`; they do
not inspect binder context or perform kernel proof checking. Private expression
and level maps must be separate: expression0 and level0 are different objects.
Create and discard these maps inside that top-level call, not across declarations,
Inventories or externally supplied state. Keep cumulative work across proofs.

For each successfully cached node x, store exactly `(c(x), h(x))`, where c is
the number of original unfolded `visit` events, including this node, every
repeated edge and every expression-to-level descendant; h is the maximum
relative visit depth. A leaf, including level0, has `(1,0)`. A parent with
children has `c=1+sum(c_child)` and `h=max(0,1+h_child)` over actual visited
children, preserving edge multiplicity. A const with no universe arguments
is a leaf for this count. Successful-child summaries may be composed; a global
maximum-depth accumulator without a properly scoped subtree summary is unsafe.
Do not cache partial, failed or in-progress traversals. Work-before/after
differences give exact counts only if every nested hit charges its full count.

At incoming depth d and cumulative work w, a hit may replace the complete
traversal iff both `w+c<=250000` and `d+h<=192`; then set `work=w+c` and return
the same summary. Evaluate this before charging the root visit, or compensate
exactly: charging root plus c would double count. Use checked arithmetic (or
explicit validated subtraction); saturating depth subtraction alone would
wrongly admit a height0 leaf already beyond the depth cap. A failed hit guard
must fall through the original visitor and diagnostic order, **not reject
early, truncate c or reset work**. It may still use guarded child hits.

Proof sketch: cached success establishes that every nonresource check in the
fixed subtree succeeds. Work is monotone, so the count guard makes every old
work check succeed; the height guard makes every old depth check succeed. The
hit therefore contracts a finite successful trace segment with identical
ending work. On a miss or failed guard, retain the old entry visit and local
checks, then replace only recursively successful segments by the induction
hypothesis. The first failing check remains at the same logical work prefix.
This proves equal acceptance, equal total work on success and equal first
semantic diagnostic/work prefix on refusal. It does not prove identical
allocation failures, wall time, stack traces or compiler source locations.

Important source obligations: retain incoming child `uint`/backreference checks,
the const levels-before-reference order, projection reference/index/child order,
and each existing constructor's precise sibling/field order. Do not eagerly
parse all child indices before the old code would reach them. Heights must mix
expression and level recursion, not bound those domains independently. The
unchanged `expression()` and `level()` still construct committed types/bodies;
the real kernel still validates the new proof. Syntax memo success is neither
a mathematical certificate nor a mechanism for skipping proof checking.

Cache memory has a finite structural bound: at most one entry per reached
expression row, one per reached level row, plus implicit level0; hence no more
than250000entries under the existing inventory row limit. Map allocator
overhead and initialization/drop cost are real costs; do not assert a byte
budget without the selected representation. On a successful proof, physical
syntax work can scale with distinct reachable nodes/edges (plus lookup cost)
rather than unfolded multiplicity. Logical charge remains unchanged. This
cannot rescue an input refused by the existing logical250000/depth192 policy,
does not eliminate kernel or codec work and does not guarantee guest speedup.
Near refusal, fallthrough may retain old repeated work intentionally.

Decision-changing controls for any later selected source: same shared subtree
at different depths; cached reuse crossing work/depth thresholds; level0 vs
expression0; repeated universe levels; malformed sibling after a successful
cached sibling; and separate proofs with changed parameters/Inventory while
global work continues. Compare first semantic panic payload and work, not only
pass/fail. Existing unchanged tree-producing routines remain the differential
oracle, but targeted shared-DAG/threshold cases must actually trigger hits.
Root/base own workload benefit and source selection; no build/test was run here.

### Offline attribution actual PASS adopted in its diagnostic-only scope

Independent actual audit confirms outer2,115B RESULT SHA
`481f5c67df18f368036bae073872d517faefe7dd9796b2cbac29ed79d2f91b49`
and inner1,519,214B report SHA
`9f100a3f56f7645938fae6eb46803d6d742ddbb7cccfdc1070a58c0ae37f893f`.
Outer command exited zero and closed/reaped cleanly: active0, terminated0,
no cleanup error or failure override.0.734375inclusive Job CPU plus0.328125
wrapper CPU gives1.0625knownCPU; outer wall1.2728937seconds before excluded
reporting tails; peak138,825,728B. All3 current/snapshot source pins and39
runtime/data pins match. All19 adapter-bound files match size/hash and are
covered by the exact selection. No source or evidence was changed by review.

Inner status is exactly `PASS_OFFLINE_PREFIX_ATTRIBUTION_ONLY`, with zero
compiler/guest/proof/subprocess calls and no mathematical admission. It retains
the failed screen,128partial segments and original session-cap error; neither
a complete capsule nor a success/speedup claim was created. The frozen helper
was used only for the new exact image. Saved old attribution was not rerun.

Read-only report checks independently confirm stored/omitted/observed metadata
against both adopted inputs, window/category/class count conservation, total
sample count `ceil(observed/256)`, every published missing-label interval and
unchanged old class/category counts. Current131,614stored+22,960omitted events
cover39,570,878observed instructions. Both current ambiguity counts are zero;
118,588stored events resolve to symbols and13,026fall outside user executable.
Both top40 lists are truncated.72,522reported current windows are retained-only
SDK row-point bins, not completed phases or session-cycle intervals.

The actual new coarse labels include canonical-native correspondence18,800,
module canonical7,973, serialization7,261, general runtime35,895 and
unclassified48,410stored events. Example retained symbol counts: memcpy14,620,
serde JSON deserialize_any13,529, memcmp7,379, write_all6,227, parse_str6,032,
JSON index_into5,042, correspondence fields4,016 and validate_expression3,953.
These are **exact retained sample-label counts**, not execution cost fractions.
Several JSON trait symbols are deliberately unclassified by the unchanged
coarse-name classifier, so the serialization class alone does not bound total
JSON work. The old canonical26,530 and current7,973 counts describe different
capped prefixes; their difference is not a measured saving or speedup.

Conclusion: source investigation of parse/copy/correspondence work is justified
by actual retained labels. No ranking of full execution bottlenecks, proof-cost
forecast, cycle-cap sufficiency or completed-work benefit follows. Use this
with the source/theory options comparison to select any next intervention;
stage compilation, proof funding and guest retry remain unselected/HOLD.

### Exact offline attribution selection cleared

Independently read and hash-checked the actual11,057B selection SHA
`8d4ece90a22f79702778e88edc85da14f7204c04c5cb4aa72577349d6b9c0968`
and5,760B configuration SHA
`f6588442d3c3811d86c28d3e316fb6a559a6a61b84fc3d58fcb06404801c2024`.
All three source pins and39runtime/data pins match actual ordinary files;
the latter total31,125,493B. All twelve configuration record sizes/hashes agree
with that closure. Derived ELF/map/image/wire/header/I-receipt pins match the
previously adopted actual records. The new adapter is exactly reviewed e712b33f.

Actual argv invokes only isolated `-I -S -B` Python over the new snapshotted
adapter, exact config path/hash. Limits are30CPU/60wall/512MiB/two active with
1MiB each stdout/stderr. The operation root and output are absent/fresh at
review. Clear **one bounded offline attribution** for root's selection; no
runtime was executed by this reviewer. No guest/proof/cap increase, baseline
reattribution, stage compilation or mathematical admission is authorized.

### New-image offline attribution source and selector cleared

Read the complete final17,231B `bounded_parse_guest/attribute.py`, SHA
`e712b33fea2a46bbc975f9b576c8e844cf8b2d397d163f0925a8c023291007b1`,
the complete failure-decision checkpoint and6,135B root selector SHA
`04f79bdfea40464da8c8c17d4e8c4e8c8c010788f9e5e8bde0b934ae5d5e15b2`.
Independent PowerShell parsing reports zero syntax errors; selector was not
executed by this reviewer. No concrete source blocker remains.

The adapter reuses the previously read frozen25,115B helper0fc2ca9b only under
a non-main module name. Exact current twelve-record binding connects the
successful direct build, actual assembly and failed screen to their own ELF,
map, image, wire,192B header and retained genuine I receipt. The new41-source
map is bound through actual assembly selected_inputs, not confused with the
old39-source hash in direct-build RESULT. Prior attribution31b29b7a is read as
adopted data, never recomputed. No compiler, subprocess, guest or proof call is
introduced, and no old dependency-tree campaign is repeated.

The only new arithmetic summarizes retained windows, conserved coarse-class
counts and top40 unique-attribution symbol labels. Global omission intervals
`[H,H+O]` share one missing-label pool. They are not independent bounds on
physical overlapping symbol ranges, all instructions or execution/proof costs.
The explicit unique-attribution wording resolves the last source precision
concern. Unknown windows, ambiguous labels, deterministic sampling/saturation,
caller/inlining limits and nonalignment of the two failed prefixes remain
explicit; no speedup ratio, matched-phase inference or completion claim occurs.

Selector prospectively pins three sources, eighteen inherited Python files,
twelve records and all derived reads;8MiB caps accommodate the adopted4.7MB
baseline and2.4MB diagnostic. Final rebinding remains inside128MiB total reads;
output <=16MiB. Proposed outer30CPU/60wall/512MiB/two-active envelope is finite.
This is **source clearance only**: root must prepare the actual immutable
selection/configuration for exact review before its one offline operation.
Stage-host compilation, guest retries/cap increases and proof funding stay held.

### Optimized-image execution screen actual FAIL at unchanged cycle cap

Root reports the single selected screen terminal exit1. Targeted independent
audit confirms outer2,100B RESULT SHA
`a4db15321bc9084ba5db4c7f4dbbb702a391909c8cafe7fd7d82f7ecec6237e9`
is COMMAND_FAILED; inner859B RESULT SHA
`bc7fae70d1a7cde35a3db76a075ff289d8e082dea90b4ec2f726fb05ed99ba05`
is FAIL.2,434,863B diagnostic SHA
`dca409e07e44f7647c2b248167cadcba6f5ad0827af83a3aa3173e0aee0bda72`
is FAILED_NO_ACCEPTED_CAPSULE with null result and session_stats. Actual host
stderr says `Session limit exceeded: 33557665 >= 33554432`. This is not compiler,
wall-time or memory exhaustion and not a completed aggregate execution.

All eight current/snapshot source pins and29runtime/data pins match. Actual
215,540B wire SHA
`aeddcc517ac61bc14d93e66abe099b73d4167a2ef26f1ef0363d44ddb39aed1e`
and192B header SHA
`1c81b7b3bf815cc25f5fdcc65a4044280e04838c98cb3933a9b0f05de501e887`
equal the retained reference except the exact32-byte A-image slot. Diagnostic
binds those bytes, the adopted image and the unchanged2^25cap/po2=18. Its one
boundary parent is the unchanged genuine I receipt850c33b2. One host/guest call,
zero proof calls and no mathematical admission occurred.

All128retained partial segment file sizes/hashes match diagnostic; total
25,477,893B. No `aggregate.snapshot` capsule exists. These partial files are
preserved diagnostic evidence, not a completed or resumable production capsule.
Job exits cleanly with active0/terminated0, child reaped, no cleanup error and
153,657,344B peak private commit.8.296875workerCPU+.46875wrapperCPU gives
8.765625knownCPU; outer wall8.685207seconds, final reporting tails excluded.
No prior failure or resource expenditure is erased.

Reported phases are134ms bounded-read/native preflight,13ms genuine boundary
receipt verification and6484ms partial guest execution/segment custody. These
are phase wall times, not CPU or completed-work costs. The deterministic sample
map is saturated at131,072cells with22,960omissions; diagnostic explicitly says
instruction samples are not proof-cycle attribution. It cannot justify an
unbiased whole-execution hotspot percentage, completed total-cycle estimate or
speedup claim. Source/retained-trace investigation remains valid next work.

Adopt the **failure and clean closure**, not guest success. Staged-host compile,
proof funding, a larger cap and another execution remain HOLD/unselected. The
bounded-parse optimization alone did not meet the existing completion gate.

### Held aggregate staged-host one-link source review complete

Read all17,828B `aggregate_production/build.py`, SHA
`a1d2c22427ffa9f8293813ac76359f9cdde6a3f73870c75a209dad2310bc781a`,
the one-link contract/controller sections of AGGREGATE-PRODUCTION-SEAM and root
selector SHA
`7909b346f906b77e94fb3a4332b16d7cf6a64f45585418cdce2ecd60a02f9a67`.
Selector PowerShell syntax passes without execution. Reviewed Rust stage/receipt
source pins remain unchanged. No source blocker found in this held builder.

It preserves the actual successful host argv except exactly crate name/source/
output, retaining seven externs and14search directories. The deterministic
1,071-file/2,320,491,997B runtime subset preserves exact prior versions, native
archives and host linker inputs; implicit Windows facilities stay trusted.
Three-file fresh snapshot contains the builder plus only two compiler-read
Rust files. Stage's sole path module is the reviewed receipt.rs, with no added
Cargo environment/include dependency. Old result/attempt/absence of override
are bound. Complete private environment and cl/link/rc metadata observations
are recorded and compared to their previously pinned environment record.

Full runtime hashing occurs at initial/final binding; the precompile midpoint
rechecks smaller records/helpers/sources. Census has both pre/post envelope
checks. One240inclusiveCPU/300wall/3072MiB/six-process Job,40ordinary+20final
controllerCPU/420totalwall,512MiB/8192entries and1MiB combined logs remain finite;
finalization can override reported success. The more comparable retained stage
host03 cost, not only snapshot-host size, informs this headroom. No claim of
actual new link completion is made. **This source clearance does not bypass
the failed screen or authorize stage compilation; no exact selection exists.**

### Exact unchanged-cap optimized-image screen selection cleared

9,277B selection SHA
`115c00c10b33e75e72b4427061a1b933cb3b632e0ed70681611cb6d766100719`
and568B configuration SHA
`19296697208cc4b6b0b9135bf4baf90a905050bdb926a9718746244e8585d681`
match actual files. All eight unchanged source and29runtime/data pins match,
including snapshot.py d99656a1, the adopted actual assembly696774f9 and new
image17325569/fileSHAe3ec2dbb. Existing actual-two-delta input/native output and
the genuine I receipt are unchanged; old failed executions are not restarted.

Source retains one host snapshot with2^25session cycles and segment_po2=18,
zero proof calls and no mathematical admission.180CPU/240wall/3072MiB/three
active processes and1MiB stdout/stderr remain the selected bounds. Exact fresh
run root is absent at review. Root may launch that one screen; no stage-host
build, proof budget or larger guest cap is authorized by this clearance.

### Fresh aggregate image actual assembly PASS

Root confirms the single assembly launch terminal exit0. Outer RESULT2,295B SHA
`f92ac44d3b2b12c677e3dcbe819dd64703cfd9f1da00d01efd58bb68e49c47ab`
is COMMAND_EXITED_ZERO_AND_CLOSED. Inner2,208B RESULT SHA
`696774f9616ffd0f8a058eccf5fbf13f9f6b6e2eb0cfdbb5f7ee6acde75e6b7a`
is PASS_NEW_AGGREGATE_IMAGE_ASSEMBLY_ONLY; inner17,082B COMMAND SHA
`fa544ea6ce87fee63a1b70e3e443461fa7f535e34b524de5979f9bb456840cde`.

Targeted actual audit matches all81selected runtime/data pins, both current and
snapshotted source pins,60recorded assembler-input pins, actual image and both
inner log pins. No whole dependency-build inventory was repeated. Actual outer
argv equals selected substitution; the inner command uses exactly the adopted
new guest ELF, retained kernel and pinned assembler. The build finalization
failure marker remains absent. Printed and saved inner reports are semantically
equal; their JSON property ordering differs normally. An audit-only order-
sensitive comparison was replaced by a read-only semantic comparison, without
changing evidence or running the operation again.

New image1,739,692B SHA
`e3ec2dbb7742bf6de81ebd0d226bd08f88d63c91e1658fdf262510c296857822`
matches actual bytes. Assembler stdout's exact COMBINED_IMAGE record reports
image ID
`173255698c2bc9030e7528297b627c59d6d35a605ec3a16542b2ba73e5107ac2`
and matching size. This image ID is the pinned assembler's actual computation,
not the file SHA or an independent re-execution by this reviewer.

One assembler call, zero guest/proof calls and mathematical_admission=false.
Child exits0/reaped, Job closed with active0/terminated0 and no cleanup errors;
stderr is empty. Worker0.734375CPU plus wrapper0.59375CPU gives1.328125knownCPU;
outer wall2.8056585seconds, with final reporting tails excluded. Recommend root
adopt this assembly, then separately select the unchanged-cap execution screen.
No capsule, aggregate receipt or mathematical acceptance is established yet.

### Fresh image assembly exact selection cleared

22,532B selection SHA
`f78b388b6b6278ffbae2aa73ab50f5eadfe5f1527a744e2f4cc8799670abcb35`
under `bounded-parse-image-assembly-01-selection.json` matches all two source and
81runtime/data SHA pins on current ordinary files. It binds the adopted actual
direct-build RESULT694d205b, newly linked ELF/map, provenance records,39source
snapshot files, both direct-build adapters, preserved failed02 lineage and the
unchanged pinned assembler/kernel. Selected assembly source is220f54cf;
changed-source review was independently completed by the guest author and root,
so this reviewer did not duplicate their complete source reread.

Actual argv selects the snapshotted adapter with the exact successful guest
result and fresh `{output}/assembly`. Output root was absent at review.
120CPU/120wall/1024MiB/two active processes and1MiB stdout/stderr limits are
unchanged. Root may launch this one assembly. No guest execution, proof,
receipt or mathematical acceptance follows from exact selection clearance.

### Direct three-project build actual PASS; fresh assembly prerequisite satisfied

Root confirms session6763 terminal/reaped exit0. Independently audited actual
`bounded-parse-direct-build-01` without any compile/test rerun.25,069B RESULT SHA
`694d205b63082ecd02536eb70b16ae08a271f06d66d5df95f296a51a607ce22b`
records PASS_BOUNDED_PARSE_THREE_PROJECT_COMPILES_ONLY; matching attempt binds
that exact result and no FINALIZATION-FAILED marker exists. Both reviewed
adapter sources and selected finite limits remain unchanged.

All329original input length/SHA pins and238fresh copied artifact pins match.
Copied view contains exactly those238regular files. All39immutable project
snapshot pins match, and independently parsed compiler dep-info identifies
exactly the16selected non-checker Rust sources, with no additional project file.
All five new code/metadata output pins, six log pins and three separately stored
command records match RESULT. Actual argv arrays equal the saved reconstructed
recipes in module/aggregate/guest order. Each command exits0/COMMAND_COMPLETED,
with no cleanup error or selected telemetry cleanup. The only stderr is three
dead-code warnings in module compilation, not compiler failure diagnostics.

| Phase | Worker CPU seconds | Command wall seconds |
|---|---:|---:|
| Module | 4.734375 | 2.1362851 |
| Aggregate | 1.015625 | 1.0437693 |
| Guest | 23.796875 | 25.8535494 |

Final Job is closed, active0/terminated0, seven total processes and
387,866,624B peak private commit. Worker CPU29.546875 plus recorded controller
CPU6.78125 gives **36.328125known CPU seconds**, with report/write/exit tails
explicitly excluded. Recorded whole-operation wall is40.8754799seconds.
Reported pre-result census/peak is278entries/328,317,496B. These are this fresh
operation's observations, not a matched full-workflow speedup; all previous
failed costs and their unknown tails remain retained and charged.

New1,680,924B guest ELF SHA
`16b7f1a26bcabdf95bf6cd85da1c0f8e6cd6c8647c2b7b049c65c7332f0fc701`
and1,771,273B link map SHA
`b200d6322acfad9ab454f5fddbfb90dc08d1e476f3282b53956ab9a34e9f4581`
match actual files. Independent byte parsing confirms ELF32/little-endian/
RISC-V executable, four bounded LOAD segments and entry2100484inside executable
file-backed bytes, all matching ARTIFACT. Link map contains `_start` at that
entry and `__start`. This confirms a newly linked artifact, not execution or
mathematical validity.

Additional provenance pins:

| File | Bytes | SHA-256 |
|---|---:|---|
| SOURCE-MAP.json | 9666 | `35387a79067d4868e02076c71c9128b1695fe0371524493f87e28de51fa19c3e` |
| INPUT-MAP.json | 142848 | `1977a89a3936ecd3916f889f52b6590e215897df1c377213c073498e82fb353c` |
| RECIPES.json | 17089 | `e6fc21c18e114cc280f7a5fe9bba3beafedae31309e87f940c970ec89ec38510` |
| ARTIFACT.json | 1238 | `d551a90cb1af3ed77c064bb457f34c38aaa9acc0eaf766143393cdb1c09dccb8` |
| GRAPH-COMPARISON.json | 572 | `3f2accd068ea0413dba2126fd03ef14433d6f4eb2a2375493714b94dab41a438` |
| bounded-parse-direct-projects-job.json | 390 | `481812fd34faeec6b6f9680179585d7119177a0b0e6f6a66e7afdf4aaedc3451` |

Recommend root adopt this bounded build result and proceed to a separately
reviewed exact assembly selection. Zero new Cargo/graph/dependency/checker
compiles, network/assembly/guest/proof calls are reported. No image, capsule,
A receipt or final deployable-v5 claim follows from this audit.

### Direct recovery exact selection cleared for one root-owned launch

Selection253,090B SHA
`3f92ea98aa873580929a446635e426717f6d0efe1a1b1a91e272e21ab7eb9bc6`
has exactly the reviewed schema/explicit retained-adoption flag, two matching
adapter pins and unchanged finite limits. Independently reconstructed the
expected artifact set from the pinned old nonverbose stdout:108 matching-stem
rlib/rmeta pairs,22host macro DLLs,41 build-script rows without external native
link paths/libraries, and one successful build-finished record. All238 actual
current file sizes and SHA-256 hashes equal the selected map. Total bytes
320,499,420; library-pair bytes281,325,788. Old project crates are excluded.
The exact fresh output directory and attempt marker do not exist at review.

Root may launch that one unchanged finite three-compile operation. This reviewer
ran only read-only parsing, source inspection, hashing and selector syntax
parsing. An initial audit-only PowerShell property-count assertion omitted the
array wrapper and failed before artifact validation; correcting that local
read-only diagnostic allowed the complete audit above. No product, selection,
retained artifact, source profile or runtime state was changed by the correction.
No compiler/ELF/guest/receipt result is implied by clearance.

### Direct three-project recovery source and selector cleared

Read complete18,648B `bounded_parse_guest/build_projects.py`, SHA
`a2ccf89c795cfafd6f9cc8ec14afb6447a95ab317ae483a323b94b62ce80fb49`,
9,412B `recipes.py`, SHA
`61d020dfc0597cd74c887d162bf88187e446ab1f4a9f67faa2ae2dbd3e7e7927`,
and GUEST-BUILD02-RECOVERY. Root selector SHA
`29cc4c5781d8d4790714ceff09485f5874c02d4de0d9f20c518aa7974f89a328`
was read completely and PowerShell syntax-parsed without execution. No source
blocker found; root may prepare exact selection for separate input-pin review.

Independently inspected the actual retained297-unit graph's three project
profiles and11/10/11 direct dependency edges. It records edition2021, release3,
fat-LTO intent, abort panic, checked overflow, debug assertions off, unspecified
codegen-unit count and no incremental compilation. New library bitcode/final
fat-LTO recipes match that intent, not uncaptured Cargo argv or identical ELF.
Seven standard-library edges retain `noprelude`; the exact relocated checker
package is the only direct package-ID exception and all16 checker source pins
must equal the old map. Linker/text-address/atomic/getrandom flags come from the
bound old environment, with only the fresh map destination changed.

The old compiler child actually records COMMAND_COMPLETED, exit0, clean active0/
terminated0 closure and222.640625workerCPU. Its encompassing finalization remains
failed. Successful child artifact messages identify108 target library pairs and
22host macro DLLs. All41 build-script messages declare no additional native
library/search paths; any embedded native payload remains inside adopted rlib
bytes. This is **explicit present-time adoption of retained compiled artifacts**,
not an invented historical content-hash attestation or source-to-binary proof.

Every target pair has identical stem, one rlib and one rmeta; lookup is keyed by
package ID and target name, preserving distinct versions. The fresh238-file copy
view excludes both old project crates physically. Distinct new metadata salts
and explicit new rlib extern paths enforce sequential new-module/new-aggregate/
new-binary composition; no Cargo cache,297-unit rebuild or retained target search
directory is used. The complete39-file source snapshot remains read-only and is
rebound, as are26selected compiler/linker/runtime files totaling395,093,004B.
Operating-system facilities remain trusted; this is not a hermetic-build theorem.

Independently read the retained SDK entry expansion (mod.rs SHA c149e205): it
emits the const/function wrapper without consumer Cargo-variable lookup. Serde
derive1.0.229's only inspected environment macro occurs inside the compiled
macro implementation's Ident construction, so its `__private229` token is
already fixed in the adopted DLL. No dynamic environment read was found in that
derive source or serde_json's macro definition. The explicit private invocation
environment is recorded; this narrow result says nothing about arbitrary macros.

The strict copied view consumes320,499,420B, leaving216,371,492B inside the total
512MiB output cap for new code/logs/temp/evidence. For context, the old two
project rlib/rmeta pairs total3,897,401B and guest ELF1,682,292B; those are not
upper bounds for new LTO temporary space. The new238-file view avoids the old
11,755-entry census shape, while all three compiles share240workerCPU/300wall,
40ordinary+20finalcontrollerCPU/420totalwall and six processes. This is justified
finite headroom, not a measured speedup or guaranteed pass. Sampled census and
final override remain necessary; failures and unknown old tails stay charged.

Exact238retained-byte pins and fresh selection/outputs remain to audit. No new
compile, ELF, assembly, execution, A receipt or deployable-v5 result follows.

### Combined genuine-A reciprocal harness source review

Read all50,429B `mixed_network/reciprocal_actual.py`, SHA
`9ae9520bc9f01205aa53689149be09606f9ec3bed2e9f907fc0391ebfa482857`,
and the complete REAL-A-RECIPROCAL-PLAN. Independently followed only changed
integration seams into existing import, preparation, transport and location
owners. No core edit, project import, test, native call or network run occurred.
The inherited guide request is already completed; root directly reaffirmed the
newer human software-continuation instruction after this reviewer's resumption.

The source preserves actual authority separation. Author receives a genuine
A/H call and selects only exact BASE/FIRST member Js; membership openings and
retained interface data cannot independently authorize mathematics. Its live
owner survives session/preparation completion. FIRST proof and reference SECOND
are not passed into authoring; reference SECOND is read only after author
closure, with complete witness comparison, not merely a row-count check. This
is explicitly trusted same-process input separation, not hostile isolation.
Ordinary output remains untrusted until each new reader performs its own one-A/
one-native admission. Final ordinary import uses the second reader's live
mixed handle and acquired semantic data; saved reports never re-create it.

Unknown-target discovery uses only the previously known BASE fold vocabulary
and structural theorem/equality features. The neutral bootstrap has no provider
publication; route descriptors supply contacts, the actual returned candidate
supplies the module/export, and expected SECOND assertions follow acquisition.
The test owner's loopback egress allowlist necessarily knows permitted endpoint
ports; it is not a claim of adversarial consumer isolation or Internet recall.
The first actual relevant match is selected within existing finite grants,
without a hidden expected-ID filter or success-driven retry.

Replica index and semantic custody derive solely from reader1's acquired bytes.
Its mathematical owners close before reader2 begins. Origin HTTP/node/stores
are stopped and closed before reader2 route/search; fresh reader2 stores and
owners then independently acquire/admit. Only structural custody survives.
Source counts enforce three A verifications, one ordinary authoring and two
native SECOND checks, with no I verification, guest call or proof generation.

Budget design is feasible in principle, not a measured prediction: the existing
outer launcher accepts at most600worker-wall seconds; inner cap540 leaves
nominal tail headroom. Sequential phases have at most three live location nodes
plus the main worker and at most the existing two-process mathematical child
bound, fitting the proposed eight-process ceiling. Six30CPU child reservations
total180CPU; nested owner/acquisition limits constrain that same work and must
not be added again. Actual installation validation, controller work and cleanup
remain inside enclosing totals. Five node lifetimes imply ten full retained
location installation validations; their cost must not be erased or called
constant-free. Existing finite node/search lifetimes may expire before the
whole outer cap; such expiry is a preserved failed operation, not renewed work.

No changed-source blocker found. **Source clearance is not exact runtime
clearance:** actual A image/receipt/H/member paths, updated snapshot profile and
63-file loaded-source closure, concrete supported allocation, receipt/packet
size fit and fresh output/port selection remain to review. No genuine A artifact
or operation success is established. Direct-project recovery review now takes
priority; this passing source review does not warrant running old campaigns.

### Resolver build02 actual controller failure and diagnostic findings

Tool session84782 is terminal/reaped exit1, confirmed by root. Actual14,187B
RESULT SHA
`792ed5825ae3110dc3ddc1a85b49636b63469f5e4cb1d662e70d8ddf27d6b4b6`
is FAIL; its matching attempt remains FAIL. A223B overriding marker SHA
`36c6f5c6b7084dbb08d461c008ea8b39e71e80bf95cc90860e455936b637cf55`
sets **FAIL_FINALIZATION**, binding that exact RESULT, because the final
controller envelope was exceeded. Never treat the recorded pre-tail counters
as a complete successful resource result.

Independent audit matches all77 current/snapshot source pins and379 copied
cache pins, plus all four actual command-log byte/hash records. Saved16,129B
selection is the cleareda537fdbc object. CACHE-SELECTION6,171B SHA85c7a308 equals
RESULT's explanation and selects180 archives/379 files. Original failed01
descriptor/costs remain in the result. No historical SDK/runtime census was
repeated by this audit.

The one graph command exited0,6.515625workerCPU/17.7477509commandwall. Stored and
stdout graphs both have297 units; GRAPH-COMPARISON232B SHA36b0bd9b records only
the previously reviewed two library/four unit/cache relocations. UNIT-GRAPH
544,592B SHA142224e5 is retained. This establishes the resolver repair's actual
graph outcome, not completion of the subsequent compile.

The compile command failed at the controller ordinary-envelope check after
183.703125workerCPU/128.6510096commandwall. Source error handling killed its
owned Job and reaped the direct child; exit1 is not a recorded compiler
diagnostic. Final392B Job record SHA
`f7fd903607b68ac3abe9184b88ddc8b743e15f18b5ddcc2d2c4bee875ea11237`
has closed=true, active0, no cleanup errors,190.21875cumulative workerCPU and
1,203,777,536B peak private commit. No ELF, link map or ARTIFACT exists; no image,
guest session or proof followed. Preserve partial dependency outputs for a
separately justified reuse decision, never as a complete guest build.

**Accounting:** RESULT records88.640625controllerCPU/179.72636870015413wall
before writing/final reporting. The subsequent override proves total controller
CPU exceeds90; its exact final CPU and final elapsed tail were not recorded.
Thus actual worker+controllerCPU for build02 is **greater than280.21875**, not
the apparently precise pre-tail sum278.859375. Including failed01's recorded
20.125CPU gives a combined lower bound **greater than300.34375CPU**, with
excluded reporting/exit tails explicitly unknown. Do not fill missing tail
measurements with estimates presented as observations.

**Monitor source diagnosis, not measured attribution:** frozen runtime.py polls
CPU/wall/logs about every0.1seconds, but calls Budget.refresh before/after each
command and after10wallseconds have elapsed since the previous census. It does
not census at every poll. Each refresh calls c.census on the full new output
tree (11,755entries at the recorded end), with an initial lstat, another in
regular_stat, and path.resolve plus run.resolve for each ordinary entry. It
also repeats namespace/path checks. The work is at least linear in tree entries
with repeated path-resolution overhead; there are no internal controller-time
checks inside that census. Rebinding separately rehashes selected inputs.
No census timing/call-count record exists, so no numerical fraction of88.64CPU
can be attributed to a particular routine. The final extra whole-tree census
can consume the remaining reserve before its post-scan envelope check refuses.
Simply enlarging an allowance is not a diagnosed efficiency repair.

**Additional latent source defect exposed by retained logs:** the9,903,636B
compile stdout SHA
`c9997034e6cf812da545c2b8e34711a8c3164ca67f234b279d7cc6795e186be4`
contains228 compiler-artifact,1214 compiler-message and37 build-script-executed
JSON rows, plus439 non-JSON bracketed verbose build-script lines. None of the
parsed rows is an error diagnostic, build-finished or guest executable artifact.
All439 other lines have the `[crate version] ...` build-output form. Frozen
build_resolver.py's unconditional json.loads per stdout line would therefore
fail if later reached after a successful `-vv --message-format=json` Cargo call.
That branch was not reached here and did not cause the actual controller failure.
Future direct rustc work avoids this Cargo framing issue; any future Cargo parser
must distinguish structured records from retained verbose output. Root and author
were notified. No retry, source mutation, assembly or runtime by this reviewer.

### Resolver successor source and exact build02 selection cleared

Full new cache_resolver.py7,693B SHA
`afb71f3f19acd90cf6b731e3fa62ff65f382d372e478b8dd75599a34d2565b83`
and build_resolver.py27,749B SHA
`ad8182636c7b87a54bfcf41fbf66983a45f8aaf02f00c1010485d6d990651e8e`
were read, together with BOUNDED-PARSE-GUEST-FAILURE.md. Independent read-only
inventory confirms160 compiled registry versions and173 extracted package
directories in the retained successful target caches. The exact13 additional
resolver-only directories all occur in the new20-archive additions; the remaining
seven are available locked extras. Independently hashed all20 added archives:
their pins match the retained seed map and total1,898,069B. Source parses the
exact TOML locks and enforces their archive checksums, available180, missing40,
198 sparse entries and379total cache files. This is a justified retained-target
repair, not proof that all220 locked versions are available or every Cargo
target/feature combination works.

Fresh controller retains unchanged graph/manifests/Rust sources, same finite
limits, real native comparison, two-command recipe, sampled inclusive CPU gate
and finalization. It separately binds frozen failed01 RESULT/command/stderr/
selection/attempt and preserved costs. It adds the resolver explanation record,
not a new mathematical relation or execution cap. Source review found no blocker.
Guest02 selector3,319B SHA
`f622701f06c2b7802232edcad6838213d55b7dacfd8000ed299d17d2998ff670`
was read completely and syntax-parsed without execution.

Exact16,129B build02 selection
`a537fdbc9bf27b9a0832bb14a72aa07aad4d96abe9cc6bb433473a58935c16e2`
matches all38 current source length/hash pins; all36 inherited pins, every limit
and native-comparison object equal the frozen failed01 selection. Run and attempt
destinations are absent at review. The snapshot will have39 files including the
unchanged lock. Root alone may launch once; this clearance is not graph/compile
success, new-image adoption, guest execution, certification or v5 completion.

### Thin assembly resolver-schema update source-cleared

Final unused assemble.py12,397B SHA
`770e97e454ea16bac1b93cb8793a9577adf9f0dbd3d856228a6125ca02719972`
matches the new resolver result/selection schemas and exact build02 name, while
retaining successful status, two command labels and artifact layout. It requires
CACHE-SELECTION.json equal the adopted result's resolver_cache_selection and
carries its bound predecessor-failure descriptor. Root's prospective assembly
selector now also pins that newly read record:5,300B SHA
`6f16d5fe1bdb6905e717e529b8fd8bec627957a4958267a0e2ce4c61ae49471c`.
This final one-entry selector delta was checked. Actual build adoption and a
fresh exact assembly selection are still prerequisites; no assembly has run.

### Next distinct source review: resolver successor and thin assembly

Root assigns source/exact review of the forthcoming fresh two-file resolver/
build successor, against the frozen build01 failure and retained successful
resolver evidence. No one-crate retry, runtime or old source mutation is assigned.
Read the complete unused bounded_parse_guest/assemble.py candidate. Its adopted
success/attempt/no-override checks, exact artifact/graph records, retained driver/
kernel pins, fresh owner output and pre/final rebinding are coherent. Exact
clearance remains pending adaptation to the successor's selection/result schema
and command/artifact contract, followed by an independently adopted actual build.
No assembly selection or image exists for the bounded-parse successor yet.

Read full10,561B BOUNDED-PARSE-SCREEN-PLAN.md SHA
`acd5fefa37f45e1b5b6ca195727f29538d5499c342832c053b20a7944d543824`.
It leaves the old snapshot host/controller, workload, genuine I receipt and
2^25 cap unchanged; only adopted assembly provenance, A slot and fresh output
change. It does not repeat the old image or imply a precise cycle-speedup from
its saturated failed-prefix samples.

Root's future Assembly01 selector5,255B SHA
`89d5f3df1366b7bd0f636c7a0ef2cffaac5f2c70439140e00b822607801cb150`
is source-reviewed and PowerShell syntax-parses without execution. It requires
root-supplied adopted build02 RESULT and reviewed assembler hashes, two closed
successful build commands and exact artifacts;18 Python and3 retained assembler/
kernel pins precede operation-specific records. This is prospective preparation,
not generated selection or runtime qualification.

Initial unused Snapshot01 selector contained duplicated script bodies inside
ValidatePattern strings; reviewer refused it before execution. Root corrected
the fresh file by full apply_patch replacement. Current6,773B SHA
`f2c92c1d3d91704826d19e7ff44aeefaa701a9c13d9c69e04cb50f995224a7c6`
was reread and independently syntax-parses with zero errors. It additionally
requires independently adopted inner and clean outer assembly RESULT hashes,
actual image pin and unchanged host/workload/receipt, with eight unchanged source
pins and the original180CPU/240wall/3072MiB/three-active envelope. No remaining
source blocker in these selectors; actual prospective selections must still be
reviewed after successful dependencies exist. No selector was executed here.

### Aggregate staged-production host source review complete

Read full stage_host.rs and API.md, then the final requested accounting wording
delta. Final stage_host22,515B SHA
`5865e6afb30bd81adb79d6fe04e09ac8bb7238b40956284fa3bcd2d4da4fe102`;
API6,655B SHA
`d95748f6d008a58170140d09d4a7fd43837386c73f2f5797f34f10e644870ec4`.
Source review finds no outstanding mathematical/source blocker in this seam;
this is not compilation, proof-production or deployable-v5 evidence.

Checked the pinned SDK ProverServer signatures, local non-dev server selection,
SuccinctReceipt.into_unknown digest preservation, exact CompositeReceipt serde
field order and post-integrity claim semantics. Checked the snapshot host's
same DMKNAS01 field ABI, session S and capsule B binding domains. Pinned
bincode1.3.3 SeqAccess supplies an exact declared length and decrements it once
per element; bounded outer visitors therefore reject excessive counts before
allocation without changing the Vec encoding. Manual checkpoint framing checks
actual payload extent before copying. Nested SDK decoding remains bounded by
external memory/CPU/wall supervision, not a proved total decoded-heap bound.

Exact adopted A/image/192-byte H and native pending I/A claims are checked before
every stage; each actual parent has full typed application verification before
claim-type erasure. Checkpoint keys cannot be duplicated or left unused. At
finish, all segment receipts and genuine ordered assumptions are verified as a
composite; both its claim and the final succinct claim must independently equal
ReceiptClaim::ok(A,H), followed by full aggregate application verification on
the serialized output. Unkeyed checkpoint framing is not authenticated provenance
and does not bind a controller source profile; owner selection retains that duty.

Requested wording correction is applied: guest_execute_calls=0 counts absence
of a new whole-session ExecutorImpl acquisition. SDK prove_segment still calls
segment_preflight/prove_preflight and its witness reconstruction costs must be
charged. No claim of zero execution-derived proving work follows. API retains
3s+m explicit stages, fresh output, final-call verification and artifact-only
(not recipient admission-handle) status. No runtime or source edit by reviewer.

### Bounded-parse guest build01 actual failure audit

Actual4,187B RESULT
`1f97e4d5c3a6f0c9d704970adcc91a128eb237d541fa71365a99690c1c58d8e8`
is independently audited as **FAIL**, not compilation success. Its attempt record
has the same FAIL and exact result hash; no finalization override exists.
Saved selection matches the reviewed15,677B be47024a original. All75 current/
snapshot source pins and359 copied cache pins independently match; project has
exactly38 files and private archive cache exactly160 archives. This audit did not
repeat the full retained SDK/runtime census.

The sole actual command is the selected offline locked unit-graph query, exact
argv/cwd and source snapshot. It exited101 after2.3842389001511037 command-wall
seconds, with empty stdout. Its126B stderr SHA
`a54f0ca1f3b418c6a04ed5833b4d5f8d9d11daeb525c80fdf4013b8de872767a`
reports missing `ark-r1cs-std v0.5.0`; Cargo refuses the required download because
offline was specified. No UNIT-GRAPH, ARTIFACT or build-command directory exists.
No second compile command, image assembly, guest execution or proof occurred.

Final Job record379B SHA
`f7d850577ba379a8c91196477575e0c4821928e8f9e025f189a29eba6d09501c`
is closed with active0/terminated0 and no cleanup errors. Direct child exit is
recorded; command/job/result stats agree:0.75inclusive workerCPU (0.203125user+
0.546875kernel),19.375controllerCPU/89.82956409989856totalwall, report/exit tail
excluded as declared. Failure/spend and all used files remain frozen.

**Review miss:** the160 compiled registry units establish compilation demand,
not Cargo's manifest-resolution archive closure. Root, author and reviewer
accepted an insufficient cache-selection premise. Source/selection clearance
above was therefore not evidence that the offline graph could resolve. The next
decision must justify the resolver's selected closure; do not silently add the
first named crate, fetch online, retry used outputs or relabel this failure.
Root owns any distinct successor selection; reviewer ran no build or rerun.

### Bounded-parse guest builder source and exact selection cleared

Read all five fresh builder/graph/manifests and the retained phase supervisor.
Final build.py24,272B SHA
`514b5f743ee7acef21c02719d98aa2b910e67a4966231527a1d4b83ac450f584`
repairs the review finding that the retained supervisor's600-second wall setting
also governed its inclusive CPU check. Its local InclusiveJob now refuses
inclusive worker CPU above480 at every ordinary phase stats poll; finalization
reads raw accounting for cleanup and separately refuses above480. Windows' native
Job user-CPU cap remains480. The inclusive check is sampled, not an instantaneous
hard bound. Used/frozen helpers are unchanged. Absent Cargo configuration guards
cover fresh workspace ancestors and the fresh private CARGO_HOME.

Exact15,677B selection
`be47024a42da96b5d33dcbea8e9ffcc4f2d81be50cc30a1f58ff0b2d4da0e41d`
independently matches all37 current source byte/hash pins. Selector5,065B SHA
`66f648f46ccae7b6f3ff1f58d3254cd99ae1f925d8bcc3aa4871791dc3542134`
was read completely. Fresh run/attempt destinations are absent at review.
Six production source pins bind the adopted native02 source map;26 unchanged
Rust sources bind the retained guest project map. The source separately verifies
the saved/native selection serialization hashes and parsed-value equality.
Adopted native comparison8960B SHAddd41112 is selected, not a rerun.

Unchanged graph.py8,668B SHA
`090744c1b479474399912c2180e8cca8e1e12afe050689f6c310af4c57136c87`
compares the whole297-unit graph modulo only four explicit local unit
relocations, two changed library roots and the private cache path. Manifest
pins7eaa23cd/0435d18f/56364af4 and all four targets remain inside the exact
38-file source+lock snapshot. Strict TOML locks choose160 archive versions and
198 index-name entries plus config:359 cache files. Selected read-only SDK982,
std2192 and runtime27-file maps replace broad old-history/SDK/cache census.
Trusted retained build scripts/toolchain and OS dependencies remain a declared
boundary; offline Cargo and explicit environment do not establish a sandbox.

Source clearance covers one graph and one fresh offline locked build only:
shared480workerCPU/600phasewall/4096MiB/eight-active;
90controllerCPU (ordinary70 plus reserved20)/780totalwall;
3GiB/32768fresh-output entries;32MiB combined logs per command. Final rebinds,
owned-Job cleanup, exact ELF/map and attempt/override semantics remain required.
No source/selection blocker remains. Root alone owns launch/adoption. This is
not actual compilation success, image assembly, guest execution, certification,
mathematical admission or full v5 qualification. Reviewer ran no tests/builds.

### Mixed-network controls01 actual seven-group PASS

Actual outer2,030B RESULT
`f026936975bc5c0ae022e2cab95619e5c4182470134edd2ed2849246be6aa831`
and inner178B RESULT
`4e490df100b83e20260539f0d333e7f8a04776efc8570d989951e356d0263b09`
independently pass their selected boundary. All96current/snapshot source
bindings match; saved12,405B selection is byte-identical to the independently
cleared3273d116 original. Actual command argv exactly matches its snapshot/output
substitution. Stderr1,074B SHA
`45e8a3d66188e2bdefe1636b97188410b7ca25ea3851c05de8f6d0f569f4f69f`
lists all seven intended groups OK, zero failures/errors; stdout is empty.
Seven corresponding evidence directories exist.

Actual0.984375inclusive JobCPU plus0.296875wrapperCPU/2.389480199897662wall;
exit0, direct child reaped, Job closed, active0/terminated0, no cleanup errors
or termination requested. Adopt structural custody, profile, bounded-loopback
and explicit mock gate behavior only. No real mathematical admission, genuine
receipt verification, native kernel, Lean, guest, proof, DHT campaign or
independently hosted availability is established. No rerun by reviewer.

### Mixed-network controls01 exact selection cleared

Read full selector SHA
`2ee095ed8be1843b4c025ea2a44ceaadf8dfafa68345d16d6fbb7e979e15dff8`
and frozen Run-V5-Check.py5,735B SHA
`44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651`.
Exact12,405B selection
`3273d116a942916cb3f57b5ad4441f37cbba0edb0950034483f61e11c30bf331`
passes all48 current source and21 runtime/provenance bindings, with fresh output
absent. Merged prior network/mixed eager-import closure contains the reused
fixture dependencies; old network/packet test suites are not executed. Exact
isolated -I/-S/-B entrypoint selects seven reviewed groups with30CPU/60wall,
512MiB/two-active and1MiB stdout/stderr. Root alone may launch once. This is
source/selection clearance, not an actual passing test or mathematical claim.

### Mixed-network corrected source and seven synthetic controls cleared

Fresh transport6,735B SHA
`fa92fccc3dfec7dcb00c6b5e0d4cc21b5c6c06997026edda93e1efd6cdf836a3`
resolves the promotion issue: after final structural readback it describes the
exact handle through the real verifier, then rechecks the original acquisition
budget before returning. The seam document now distinguishes profile-addressed
offers from digest/size-only blob requests. Unchanged init86B SHA468040d5 and
custody7,313B SHAee845648 retain the previously reviewed semantics.

Read complete14,699B test_network.py SHA
`f59310331c8be7f6a4e4e53d3f22129ef733c72d1d6d9fb6381d14cd95ff9d19`.
Seven finite synthetic groups cover profile/offer confusion, exact/reopened/
corrupt custody, transaction rollback/mixed structural refusals, one local HTTP
loopback and provider-loss readback, no duck/unoffered/changed-owner authority,
one-claim/two-member reservation and final owner-expiry refusal. The last two
use explicit test-only exact-class fakes, not cryptographic/native checking.
Reservation is60CPU for one claim plus one delta; a second admission is refused
without another fake verifier call. No fake positive mathematical authority is
returned by the selected tests.

Loopback uses three requests after two explicit test-prepaid grants; the next
attempt exceeds the five-request budget before dialing. Original provider loss
and reopened packet bytes demonstrate structural custody only, not autonomous
repair, independently hosted operation or mathematical acceptance. No DHT
campaign, actual native/receipt/guest/proof call or test execution by reviewer.
Root's exact supervised runner/source selection remains a separate gate.

### Mixed-network adapter: inherited-method audit and two review corrections

Read all three fresh mixed_network files, the complete frozen delta custody/
transport parents, relevant HTTP provider/structural acquisition methods and
mixed parser/verifier authority paths. The selected subclass reuse does not
silently invoke old mathematical profile parsing: inherited custody put calls
self.inspect; get/status/close are exact-byte/quota mechanics. Provider dispatch
and framing use the unchanged route set and self.packets. from_search calls cls
with the exact shared one-shot handoff. Structural export/body/packet/custody_ready
retain semantic-ID/opening/body bindings; mixed construction/offers/admit/report
replace the old proof-form gates. Store/download reports remain non-authoritative.
The new reserved CPU = claims*receipt_cap + deltas*native_cap matches the actual
mixed receiver and charges once per shared receipt claim, not per member path.

Two corrections requested before final source clearance. First, inherited
acquisition _active checks its budget/origin, not MixedDeltaVerifier liveness.
After open_group succeeds, final custody readback may consume remaining owner
lifetime. Recheck verifier liveness/handle at the actual return point before
claiming a LIVE result; subsequent handle-use checks are not a substitute for
that stated return contract. Second, only offer requests contain wire_profile_id;
raw packet requests are exact digest/size. Document profile discrimination at
offers/local parsing, not a nonexistent blob-request field. No tests, database,
HTTP calls or native/cryptographic execution occurred in this review.

### Aggregate-production plan: exact final authority and allocator challenge

Read full `AGGREGATE-PRODUCTION-SEAM.md` and retained aggregate snapshot/receipt,
module stage, SDK Segment/Session and bincode1.3.3/serde1.0.228 decoder sources.
No conceptual soundness blocker in the proposed stage graph: ssegment + slift +
(s-1)join + mresolve + finish =3s+m, with genuine I/A premises, capsule-order
resolution, verified composite and final full application verification against
independently selected A/exact192B H. Session::claim excluding supplied proven
parents does not eliminate the final segment's real assumption obligations.
No actual aggregate capsule/receipt or resolve success is inferred from this.

Two implementation clarifications were sent to root/author before code review.
Bincode's sequence/map lengths become size_hint without an upfront element-byte
charge; standard serde Vec limits initial preallocation to1MiB per vector, while
slice byte/string decoding checks remaining input and byte limit before copying.
Consequently FILE_LIMIT is not a total decoded-heap or element-count bound.
Use early bounded visitors for <=8assumptions,1..128segments and the checkpoint
kind/payload envelope without changing its serialized ABI. Nested SDK structures
still require selected process memory/time bounds; do not claim graceful refusal
for every hostile nested allocation solely from the bincode byte limit.

The proposed B commits session/capsule, not the stage-host/controller identity.
Thus rejecting a checkpoint from another host/controller profile needs explicit
producer adoption policy, or wording confined to actual supported SDK/verifier
parameter checks. The framing alone cannot establish a profile field it omits.
Mathematical safety still requires real payload verification and final A/H
verification. These source-only challenges neither launch crypto nor change
the guest, previous host, proof artifacts or any selected runtime budget.

### Concrete bounded-parse guest contract: in-principle source clearance

Read the complete appended five-file/API/input/budget contract in24,659B
`BOUNDED-PARSE-GUEST-PLAN.md`, SHA
`9fa2e9dfdfb8021d3ccbc15e23068c34e5eb1aeb5a2dfbe3068c2a567b6a71cf`.
No material architectural blocker was found for root's fresh source-only
implementation: exact38-file snapshot,359-file private Cargo seed,297-unit
whole-graph check, bounded read-only SDK/std/tool inputs, private mutable outputs,
and recorded verbose commands address the previous closure/reuse mistakes.
These are proposed map counts, not an independent current-byte census claim.

Concrete review must enforce all actual wrapper targets within the new snapshot,
explicit pins for cross-subtree include/build inputs, exact graph-used160 archive
and lock-union198 metadata selection, and no broad inherited census hidden in a
helper. Ordinary controller work must stop by70CPU to reserve20 within the90CPU
total; both worker commands share480CPU/600wall without resetting. Final record
tail and cleanup remain inside the selected whole-operation resource boundary.
Read retained command/environment evidence for those obligations; no compiler,
Cargo, cache mutation, graph generation or SDK-wide rehash was performed.
Implementation/diff review and exact runtime selection remain separate.

### Source-only guest-build and revocation plan challenges

Read full `BOUNDED-PARSE-GUEST-PLAN.md`15,211B SHA
`9ae754e609af53266f9e7fa2ad21adaf7923426bd663d64c2b94f5ad3c69c1d3`.
No conceptual blocker found: possible three-unit dependency reuse is not the
same as a recovered exact rustc recipe or actual Cargo cache reuse. Missing
historical per-rustc argv justifies a separately reviewed fresh offline fallback,
not fabricated replay. Its selected input closure, private mutable state, changed
graph and new command recording need concrete implementation review. New wrapper
paths must resolve within the fresh snapshot; native serde is not guest serde.
This is a plan challenge only, not full graph/artifact adoption or runtime clearance.

Read the conservative local-revocation appendix in
`NEXT-AGGREGATE-COST-DECISION.md`. Stable guarded owners, immutable support
metadata, potential-authority closure, monotone updates and final authority
publication checks address hidden sealed ancestry and stale live caches in
principle. Own native/controller profiles and retained delta lane are included;
single-controller/concurrent linearization is stated. Distinguish allowed
same-image self-recursion from forbidden inter-version support cycles. Durable
monotone policy and rollback defense remain necessary for restart-safe revocation:
re-verifying a cryptographic receipt alone cannot establish current policy
freshness. No revocation code, new wire format or proof work is selected here.

### Bounded-parse compare01: actual ten controls and two native differentials PASS

Actual8,960B RESULT
`ddd411125b809fda24be93280329f6d7b7bd3d4b32ac5cbd71beab46e4948a20`
independently passes the scoped comparison. Fifteen targeted current/snapshot
source, selection, adopted build-result, build-output and log bindings match;
both retained native input hashes also match. Terminal marker binds this exact
result and status, with no finalization override. Saved selection retains the
reviewed name/schema/authorization and exact source/build-result bindings.

All ten exact named groups pass;977B test stdout SHA
`81a961d9c563b2fae720caaed350edfe66e536b4f1a9d9a7e3d1306f816e7f83`.
Valid native exit0/full4,444B stdout01d7c9cc and invalid exit2/full98B
stdout42d71010 are independently byte-compared equal to the retained baseline,
not just accepted from the adapter's equality assertion. Invalid357B stderr
`41190c9cd9744143b2f825fd945b6d8c55f7e28dadcce34e76ca37114c8867c1`
contains the actual tc.rs:945 def_eq assertion failure; it is not a setup refusal.
The baseline stderr has a different retained path/length and was not required
to be byte-identical. Valid conclusion remains conditional with three members,
three edges and mathematical_admission:false; invalid output remains refused.

Actual0.0625workerCPU plus0.203125controllerCPU/2.206277900142595wall,
Jobactive0/terminated0/total6 and no cleanup errors. Child environment matches
the reviewed minimal profile. No baseline rerun, build, authoring, receipt,
guest, proof or networking. Adopt native behavior preservation only: neither a
new guest-cycle bound, successful aggregate certificate nor full v5 follows.

### Bounded-parse compare01 exact selection cleared

Selector source `Select-BoundedParseCompare01.ps1` SHA
`5a06a8de0ebc37e6a416733274ce3ba04c9a10144fec0accf5da2cd25c885f1d`
and resulting707B selection
`c75cdf3e2ef83350eb80e2b2bf741f713d50364526806456f7dfffeeb10b5fc2`
are independently cleared. Exact five fields, schema, fixed01 name and literal
true ten-controls/two-native authorization match source-reviewed scope. Current
15,017B compare source240f8cce and adopted18,078B build02 RESULT026770a3 match
all selected path/length/hash bindings. Fresh run/attempt paths are absent;
build02 has no finalization override. Root may launch this one bounded native
comparison; no runtime was performed by reviewer. Actual success, guest cost,
certification and mathematical admission remain separate claims.

### Bounded-parse remaining two links: actual build02 PASS

Actual18,078B RESULT
`026770a3a3f1a74e04b872a13b4572471048362514c52ca2aea2179d7e8ba3b1`
independently passes the selected two-link boundary. All51 bindings match:
42current/snapshot source bindings, four logs and five outputs. Actual and saved
command vectors equal the retained build01 recipes after exact02 relocation;
only the selected test-root/crate-name/production-extern substitutions occur.
The copied selection is semantically identical in every field to original
`15cea3f094621d1d1e8901219db2caa2eb4e9ea2951232008e9e21503895640f`.
Its serializer changes formatting/order, so copied3,562B selection has distinct
SHA`c979e61ee56d9a8eed083971df2dde7d2cb6842999e17a2b46545eee487953aa`;
raw-byte equality is not the selected copied-selection invariant.

Both commands exit0: tests-link48.671875workerCPU and driver-link32.640625,
total81.3125workerCPU plus3.34375controllerCPU/100.1543467999436wall. Final
Jobactive0/terminated0/total8, no cleanup errors; two explicitly selected owned
VCTIP telemetry processes were cleaned up with observed exits. This is not a
claim that no processes were stopped. Matching attempt/result marker and no
finalization override. Test compilation reports22 dead-code warnings from the
test-only duplicate canonical module; no errors. Driver stderr is empty.

Output pins are aggregate_tests.exe2,343,936B
`c2d1cfe43187b68665cf696f52908dfc8f67fc2115b62c663f677e3933a5bfec`,
native_aggregate.exe1,801,216B
`2306e9f32292bdee6e6638a5f9c9cc9f1f9bc288c967a6443ec8862886e942c9`,
libnanoda_lib.rlib11,339,020B
`c0c0b10ba18adf5c20496d751cc9cbbc911677fafe64461d963dadc53a37c4a2`,
libdmkn_module_relation.rlib4,232,130B
`a20dfa506e70b5d781d8dbb087b151702be019c338c29f6654ebbe2a1b13315f`,
libdmkn_aggregate_relation.rlib898,764B
`0d90f603ffdc21c76fbdc2262380d18daa46d66152c5fa5d6bb4ece4c7f99830`.
Production/checker libraries were retained, not rebuilt. Original build01
failure and spent costs remain. No controls, native checks, guest execution,
proofs or networking occurred; actual comparison remains a separate selection.

### Bounded-parse remaining two links: source and exact02 selection cleared

Fresh build_remaining.py15,330B SHA
`ea6f285cd56f5ff8e59b36640a55a006e2a46549499b9e639c308434c5eadd7c`
and controls_root.rs249B SHA
`dfcb4657c70c072fccfb5df98e63f58f9aab685d296ccf6986f44749269dacc6`
are independently source-cleared against preserved build01. The new test root
reexports already compiled production relation rather than compiling its nested
cfg(test) graph_controls; it includes the exact same census.rs and controls.rs.
Those controls include the frozen old census and same canonical.rs counter seam.
This actual nested test closure is checked, not inferred from the top-level root.
Native production aggregate and checker stay linked from unchanged retained rlibs.

The adapter carries all failed01 records, attempt/finalization status, spent costs,
original19-source map/snapshot and three exact rlibs. It copies/rebinds artifacts,
changes only the test crate root/name/extern and output/project locations, and
links tests and driver only. No successful compile is repeated; no old byte edited.
Remaining150workerCPU+17.234375spent <180 original;25controller+2.03125spent <30.
Using prior full14.015542wall even for conservative phase accounting gives
210+14.015542 <240 original phase allowance and330+14.015542 <360 total runtime
allowance. Prior-plus-new working bytes stay<=1GiB;3072MiB/six-active remain.

Selector SHA
`9b530e93e079fc35c96347f321ddd015e616a9222b8ee0e841f1bba8f1a06146`
is source-reviewed. Exact8,070B remaining-build02 selection
`15cea3f094621d1d1e8901219db2caa2eb4e9ea2951232008e9e21503895640f`
is cleared after all21 expected source byte/hash bindings matched and fresh
output/attempt paths were absent. It has the fixed02 name, distinct remaining-
build schema and compile-only flag. Root alone may run this one two-link operation;
tests, actual native comparisons, guest execution and proofs remain separate.

### Bounded-parse comparison adapter source cleared, no runtime yet

Full initial compare.py15,001B SHA
`afe5ccd0064e036631f2574d47728c0c6a0674ad41eb2074cf1d2389aac36c7a`
was source-reviewed. Its unused successor15,017B SHA
`240f8cce7d5fdedddb6bdfa7b7dd0375921a6d1fa2566319b808ad1068bc32d6`
changes only fixed build01 to build02, required remaining-build schema and
required two-remaining-links PASS status. Independently reversing those three
literal changes in memory recovered the original reviewed hash exactly.

The adapter requires the adopted successful fixed build result, all five exact
outputs, matching terminal attempt marker and absence of finalization failure,
with final rebinds. Exactly ten named small test groups must all pass; then two
preserved native inputs run against the new driver. Valid full stdout must match
the retained exact conclusion; invalid exit2/full stdout must match refusal and
stderr must contain actual tc.rs:945 def_eq assertion, not a setup refusal. No
old baseline driver is rerun. Recorded baseline files are pinned, not regenerated.

The native child environment contains only explicit SystemRoot/WINDIR, System32
PATH, private temp/profile/appdata and bounded Rayon setting; no inherited SDK,
compiler or credential variables. Helpers/Python/build/input hashes are targeted
and rebound; no full SDK census. One shared Job60CPU/120wall,1536MiB/two-active;
controller30CPU/180totalwall,16MiB/128entries. No authoring, build, receipt, guest,
proof or network call is permitted by this adapter. Mathematical outputs remain
conditional, not admission. Exact runtime selection and actual successful
build02 are still separate prerequisites; nothing has been run by this reviewer.

### Bounded-parse build01: actual test-packaging FAIL, retained production rlibs

Actual21,164B RESULT
`4780ae9f43aca7dea221c6f32ede060ea0ab96d42e9750830606f0fff9bd9695`
is FAIL, not a four-compile pass. First module and aggregate production compiles
exited0. Third compiler failed before making the tests executable: copied
aggregate_relation.rs:216 retains a cfg(test) `graph_controls.rs` submodule not
in this focused snapshot. The native driver compile was never reached; neither
tests executable nor driver exists. No tests, native checking, guest or proof ran.

**Reviewer correction:** the prelaunch closure review missed this nested retained
cfg(test) inclusion. It was an actual build/test-packaging review gap, not a
mathematical-source failure; preserve the unsuccessful operation and costs.
Do not retrospectively describe the original snapshot as test-closure-complete.

All44 current/snapshot/log bindings matched. The compile recipe is19,424B SHA
`5a5e7bef3468bc719797e8f08e9326a36b131ea0b6313d019dbf2d66a1df3a94`;
source-map2,929B SHA
`2d2e9bcc29c19d84fe8530434eee5f35e937194f3f8e4ab50821092378695c42`.
Attempt marker exactly binds FAIL/resultSHA; no finalization override. All three
commands ended with zero active/terminated processes and no cleanup errors.
Cost17.234375workerCPU plus2.03125controllerCPU,14.015542000066489 totalwall.
Module warnings are three dead-code warnings, not errors; aggregate production
stderr is empty. The original fixed allowance remains spent, not renewed.

Retained artifacts separately inspected and pinned for possible fresh reuse:

| Artifact | Bytes | SHA256 |
|---|---:|---|
| libnanoda_lib.rlib | 11339020 | `c0c0b10ba18adf5c20496d751cc9cbbc911677fafe64461d963dadc53a37c4a2` |
| libdmkn_module_relation.rlib | 4232130 | `a20dfa506e70b5d781d8dbb087b151702be019c338c29f6654ebbe2a1b13315f` |
| libdmkn_aggregate_relation.rlib | 898764 | `0d90f603ffdc21c76fbdc2262380d18daa46d66152c5fa5d6bb4ece4c7f99830` |

Root's proposed fresh controls_root may reexport the linked production relation,
include the exact selected census source and unchanged independent controls,
and thereby avoid compiling unrelated old graph tests. That architecture is
supported in principle. Any successor must preserve failed01, copy/rebind these
three artifacts, compile only tests/driver within the recorded remaining budget,
and undergo exact source/selection review before launch. No old passing compile
or failed test compile is automatically rerun.

### Bounded-parse controls and build controller: source cleared

Independent controls.rs12,143B SHA
`9ea0a9b0da364b9c05d1eb0535d1becc7e070b09e887a05bd7b0bb9cc65db00a`
is source-cleared, with author confirming final bytes. Ten finite groups cover
legal Unicode/escapes, decoded duplicate keys/no normalization, exact u64 grammar,
UTF-8/surrogates/EOF, known counts/immutable borrowing, actual127-container parser
boundary, small parameterized scanner recurrence, both record forms, cumulative
aggregate limits/overflow, and typed/raw/arbitrary-Value early schema refusal.
Old parse_validated and old aggregate traversal are unchanged differential oracles.
Test-only same-source scanner returns counts only; production tokens still come
from linked production crate. Exact typed extraction supports the deliberately
wrong-schema fixtures and refuses before foundation/kernel work. No million-node
or giant raw-length experiment is smuggled into these controls; production fixed
limits and unchanged raw guard are separately source-reviewed.

Root build.py14,075B SHA
`f068cdaa3f3fe24ddceb6ea8aeb0e56080b07bdabb88625b1d3f107aef92d8df`
and `Select-BoundedParseBuild01.ps1` are source-cleared for fresh selection
construction, not launch until the exact artifact is reviewed. The19-source
snapshot is eight fresh plus11 prior-map-equal retained files, including actual
foundation_data and test-only old census/scanner closure. Exactly four compiler
calls produce module/aggregate rlibs, ten-test executable and native driver;
tests themselves are not invoked. Exact checker rlibc0c0b10b is copied, not rebuilt.
All four named retained record/artifact hashes were independently rechecked.
Recipe rewriting replaces each old source/output/project dependency exactly,
forbids leftover old-project paths, preserves flags and dependency identities,
adds required serde/RISC0 test externs, and retains fatLTO for final links.

No Cargo, dependency/checker rebuild, guest, proof or network is selected.
180workerCPU/240phasewall,3072MiB/six-active;30controllerCPU/360totalwall and
1GiB/4096 output entries. Inputs/snapshots are rebound; finalization override
remains explicit. Recent unchanged SDK/recipe assurance is reused, not a new
full toolchain census or hermeticity claim. Exact selection and outcomes pending.

**Exact prelaunch selection:**7,294B
`cfa3402c76bc7504e36702e0759a1aeadb600001fb0dd381b988dc873e113574`
is cleared after all19 exact source sizes/hashes matched, compile-only schema/name
checked and fresh output/attempt paths were absent. Selector SHA is
`11abda94be2e998e79acf626f0754afbfbd2f6f3a2c3021af95767118084c8fe`.
This clears root's single four-compile launch within the stated bounds, not
test/native execution or a successful build outcome.

**Native dependency distinction:** this recipe links serde_json1.0.145 with only
default/std, whereas the actual guest uses1.0.151. Native target fingerprint and
source inspected: ser.rs SHA
`94c189f4586b6eea1fd225c8c25adb6b986e8d3b1fb637fb9b5de249f9ab3e6e`,
de.rs `db7adf3ef0074e15426d31e1cf4bec78ad92c20e4642c136325f0a78547218c7`;
read.rs equals the1.0.151 hash already recorded below. Full source diffs show
serializer differences only in unused float formatting and deserializer
differences only in disabled arbitrary_precision and unused enum-key paths.
Relevant strict u64 grammar, UTF-8/escape/string formatting and recursion limit
are the same. Thus the reviewed length lemma and127-open-container expectation
also apply to the selected native build, without pretending versions are equal.

### Bounded-parse production successor: source cleared, unbuilt

Six exact fresh files are independently source-cleared after full minimal-diff
review and explicit-path crate-root inspection:

| File under `software/v5/bounded_parse/` | SHA256 |
|---|---|
| canonical.rs | `f8356d9300f5436b3b6fb7a76b7d2d19e0b3dcedae0bfd00e1e10abea54de9c1` |
| module_relation.rs | `0f78c1663673f291c7b612cc3bdef423124cc6cc47fd649b71e5bc13d4cd808a` |
| census.rs | `48cad55b54d3cd233d760871308ccfdc54bb50711adb89651f7d2861caa5a1d5` |
| aggregate_relation.rs | `6a2425aa6d26bf10ab6053d92f498d09b6c7bdde598efe118a5bc7bd2ceb0947` |
| module_lib.rs | `328692d04054f54bcb79ce316b14df6c472590160b39615942a027202d55be76` |
| aggregate_lib.rs | `4476115a65c03d5c81250017d4308b2dc8e3d64b8c2190f428c30ac03ed1098a` |

The parser successor only adds the token and structural scanner; retained
strict parse, arbitrary-Value canonical_size and all formatting remain unchanged.
The token has private fields, sole parser construction, read-only getters and
crate-private owned extraction. No mutable borrow, Clone, Default, Deserialize
or conversion from arbitrary Value exists. Structural nodes and depth increments
are checked; production supplies fixed1,000,000/256, values not keys, rootdepth0.
The private parameterized scanner's cfg(test) pub(super) helper returns counts
only and cannot mint a token. Its explicit test-only same-source inclusion is
acceptable; genuine tokens must originate from the linked production crate.

Module check(Value) still performs full canonical_size; byte-entry now calls
parse_bounded then the typed consuming entry. Private check_bound is byte-for-
byte unchanged. Aggregate charge checks cached current depth<=128, uses checked
addition against cumulative500,000 nodes and preserves every schema/rows/bodies/
parent/opening bound. Only immutable access occurs before returning the same
token; one delta call now consumes it through check_validated. Exact-J graph,
mathematics, hashes, foundation and external checker remain unchanged. Thinroots
select all unchanged modules explicitly. Source clearance is not compilation,
actual domain-equivalence testing, speedup or a new guest image/certificate.
Independent controls, root build adapter and exact selection remain pending.

### Bounded-parse API/file plan reviewed before implementation

Root separately selected fresh `software/v5/bounded_parse/` source work; base
owns production, source_loop owns independent controls, root alone owns later
build/runtime/Git. Read `BOUNDED-PARSE-IMPLEMENTATION.md` and independent
`BOUNDED-PARSE-CONTROLS.md` before any changed-source review. The six-file plan
is supported: minimally copied private parser/relation/census/aggregate relation
and two explicit-path crate roots preserve all used predecessor bytes.

`BoundedValue` has private owned Value/exact node/maxdepth fields, immutable
getters and crate-private consuming extraction. Only strict parsing plus the
structural census can construct it; no mutable borrow, Default, Deserialize,
From<Value>, clone or caller-supplied counts. External aggregate code reads the
same Value and cached counts, then passes the original token to typed relation
checking. Arbitrary-Value check, canonical_size and private mathematical
check_bound remain unchanged. Updating byte-entry to use the token is supported
by the reviewed domain-equivalence argument, not an additional trust assumption.

The ten proposed control groups use retained validation/census as oracle, test
successful Values/counts and refusal domain, and distinguish bounded-K partiality
from the K-infinity length argument. Root permits a private parameterized scanner
with a `cfg(test)` counter-only seam to avoid giant fixtures. This seam must not
mint tokens or be exported as a production bypass. Because linked production
rlibs lack cfg(test), exact control wiring needs explicit test-only same-source
inclusion or a separate test root; author notified. This is pre-implementation
API/theory support only. Final source/controls and any exact runtime selection
remain separately reviewable; no test/build/proof has been run by this reviewer.

### Raw-JSON bound lemma: independent source-backed principle review

Read root's `BOUNDED-PARSE-DECISION.md` and actual serde_json1.0.151 source.
The actual aggregate compile target fingerprint declares only `default,std`;
neither arbitrary_precision nor raw_value is enabled. Current compile-cache
source matches the inspected retained origin: ser.rs SHA
`f2b8cc0b97e30c49dbc58698fa22c14a7d56ea616cdb57b067835a59af49a75f`,
de.rs `4998d7e252eb513be85b298e287048b4fb283882e9ba7df905f572f07200f3f3`,
read.rs `17a2efe49e5a6937c8d7d4a5c0b9eac84453de0f86bf8e7ee421387e82341bb3`.
This is the actual1.0.151 dependency, not the separately retained SDK1.0.143.

The proposed lexical lemma holds for the unbounded structural encoding K-infinity
using exactly the current compact formatter: strict syntax parse P(b)=V implies
length(K-infinity(V)) <= length(b). ser.rs's ESCAPE table covers only quote,
backslash and U+0000..U+001F; other UTF-8 bytes pass unchanged. Short escapes are
minimal and remaining controls use six bytes. read.rs validates UTF-8, legal
escapes and surrogate pairs; Unicode escapes cannot be shorter than resulting
UTF-8. de.rs rejects leading zeros, routes overflow/fractions/exponents to the
strictly refused f64 visitor, and routes negative zero to refused f64 too.
Object reordering changes no lengths; duplicates and trailing nonwhitespace
refuse. Induction over punctuation, children and string/key encodings establishes
the inequality without a new experimental campaign.

**Formal wording correction sent to root:** current bounded canonical K is
partial. Syntax-accepted multi-array values can exceed the total node budget,
so P(b)=V does not alone imply K(V) exists. State the lemma for K-infinity, then
separately require exact node/depth constraints for K to succeed. Raw16MiB bounds
only serialization length. The proposed one structural census, parser recursion
guard and aggregate stricter cumulative500,000-node/128-depth checks preserve
these distinct obligations. A private immutable token may cache exact counts;
no unchecked minting/mutation or arbitrary-Value bypass is justified. The
unchanged mathematical check_bound consumes the same Value. Refusal ordering,
partial failed census state and OOM timing need not match; successful conclusions
must. Principle is supported, not implementation clearance or measured speedup.

### Offline attribution01: actual sample-count PASS, failed guest unchanged

Actual inner4,756,721B RESULT
`31b29b7a8888fbfa0337fbf3a72b3269d2facbf05513d0e27a23ac4ca91de84b`
and outer `c7d23d16b20372f718932bf31f2fda6fd7c31eed99f5b99a709781dd8af054a9`
independently pass the offline scope. Eighteen changed source/snapshot/bound-file
bindings match. Independent saved-data arithmetic collapsed131,072 cells to
11,327 PCs and matched every reported sample count. All2,432 reported interval
names/starts/ends match the exact raw map row; reported PC/range containment and
outside-user-executable classifications pass. Category and class totals both
equal131,454 retained samples:118,429 exact-symbol,13,025 outside user executable,
zero unknown/ambiguous/section-only. Adding23,898 omitted events gives155,352,
exactly ceiling(39,769,880/256). Nothing attributes omitted samples.

Raw leading symbols include deserialize_any13,496, memcpy11,672,
canonical_size::Census::visit11,452 and ::string10,772. Mangled trait-owned
deserialize_any remains conservatively coarse-unclassified; its raw label is
recognizable without reclassifying every generic-argument substring. Reported
20.18% module_canonical and other fractions are retained deterministic instruction
sample fractions only, not proof cycles, elapsed/CPU time or causal savings.
There is no accepted capsule: execution stays FAIL/FAILED_EXECUTION_PREFIX_ONLY.

Exact selected argv and stdout209B agree; stderr is empty. Exit0/reaped/Jobclosed,
zero active/terminated processes and no termination/cleanup errors. Cost0.59375
inclusive JobCPU plus0.265625 disjoint wrapperCPU,0.9375579000916332 totalwall.
No guest, proof, compiler or SDK call occurred. Used helper/selection/evidence
freeze. The result motivates source analysis only, not retry or higher caps.

### Mixed imports01: exact selection and actual ten-control PASS

Reviewed selector `Select-MixedImportsControls01.ps1` SHA
`f91225b22f131d5780cba872660a38e5c585909e02d27b6bd237dd9e09e89051`
and exact12,285B selection
`9a45d66fd63615e9bfccd86ec927d385e7474f51dba367cca7760383faeff397`.
All48 source and21 runtime/provenance bindings matched before clearance; output
and attempt paths were fresh. The eager context closure adds22 unchanged files
to the prior mixed closure plus three reviewed phase2 files. Namespace packages
have no omitted `__init__`; retained SSL/SQLite native-stdlib pins are included.
Exact installed Python `-I -S -B` runs only the immutable ten-group control file,
under30CPU/60wall,512MiB/two-active and1MiB per-log bounds. No old network test,
Lean/native invocation, actual receipt verification or socket/database activity
is selected. This explicit runtime set is not a hermetic OS/runtime proof.

Actual RESULT1,885B SHA
`89074bf219d0fb298988da5793b7583a19d5309962f78e106a25919b3dc4fe9c`
independently passes the selected synthetic scope. All96 current/snapshot source
bindings and copied selection match. Actual command matches selection; stderr
1,834B SHA `0a6527e492a601cedc9f71009d074467b72fe082179f4b6309c72fba3a2935a3`
lists all ten intended tests OK, zero errors/failures/skips, stdout empty.
Exit0/reaped/Jobclosed, zero active/terminated processes, no cleanup errors or
termination requested. Cost3.15625 inclusive JobCPU plus0.375 disjoint wrapperCPU,
4.280710899969563 totalwall. The0.015625 nested supervision CPU is included in
wrapperCPU, not an additional charge. No actual A authority, Lean extension,
receipt-backed cut or public deployment follows. Used phase2 sources now freeze.

The API's cut removes outgoing ancestry, but the same live session conservatively
retains prior sources/nodes/receipts, owner liveness and charges. Long-running
bounded use needs a fresh authenticated session/owner rollover; this control
does not prove bounded memory for arbitrarily many edits in one session.

### Offline PC attribution: source and exact selection cleared

Full revised `aggregate_host/attribute.py`25,115B SHA
`0fc2ca9b35892cf86b3f8fdbf124db8cdb31f6cd20658125e2d6c23967c3a786`
is independently source-cleared. The small review correction now binds exact
argv/diagnostic/wrapper cyclecap and po2, actual192B header file and wire length,
and diagnostic completion/failure to wrapper status. A failure with null stats
is only an execution prefix; non-null stats can legitimately mean a later
failure after execution and still do not establish any accepted capsule.

ELF RV32 executable PT_LOAD ranges and link-map columns33/41/49 bind virtual
byte PCs with no guessed rebase/multiplication. Zero-size symbols acquire no
invented range; an interval sweep preserves all actual overlapping candidates,
and disjoint categories conserve retained sample counts. Namespace ownership,
not a generic argument's substring, controls coarse categories. Map/sample/
ambiguity/input/report bounds are explicit. No SDK, compiler, guest, prover or
network is invoked. Deterministic instruction sampling and cell saturation
preclude interpretation as proof-cycle, time or whole-workflow cost shares.

Root selector `Select-AggregateAttribution01.ps1` SHA
`f2551dfd4c45a16494d64f6f4f70f54ac877224250c437febe7d244ba74bec28`
and exact10,356B selection
`8f5ec7caaca68511490683c1e4749ddcd85a0470d881872c089c6c22bcb644cb`
are cleared; all two source and37 runtime/data pins freshly match. Exact2,135B
configuration `fed320d5b8eae0c3baa0081fd6a73f7b860a40350678920ab7f553a9bb8f6fcb`
binds the saved failed execution diagnostic/command/result to adopted assembly,
separate artifact validation, exact ELF/map/image and preserved compile-budget
failure. The original FAIL is not relabeled. Fresh output/attempt paths were
absent;30CPU/60wall,512MiB/two-active and1MiB per-log bounds apply. This is
prelaunch source/exact-input clearance only; actual attribution awaits output.

### Aggregate snapshot01: actual bounded-prefix FAIL, no capsule

Actual outcome is FAIL, independently audited. Inner RESULT
`a873a4b81d36397191ee8e550d6152eb77951f6204bd80406af73994f37820c5`
records `ACTUAL_AGGREGATE_EXECUTION_FAILED`; stderr is the real session-limit
refusal `33557665 >= 33554432`. Outer RESULT
`f91ef77bc4eeb23c0b0945de79d2e4866f173d5a51c285ac3ba4e503f8686d0c`
confirms exit1/reaped/Jobclosed, zero active/terminated processes, no termination
or cleanup errors. Cost6.65625 inclusive JobCPU plus0.390625 disjoint wrapperCPU,
7.831916099879891 totalwall. One host/guest execution, zero proof calls. No
completed capsule exists; partial segments are not a resumable complete proof.

All145 changed bindings matched (16 current/snapshot sources, diagnostic and
all128 retained segments). Their total is25,166,009B. Diagnostic2,428,623B SHA
`ebd87c76cea9c321d1f64f5aee9ac5f1dc0c4aef0659c1937f0af84e4b259388`
is explicitly `FAILED_NO_ACCEPTED_CAPSULE`, null result/sessionstats, exact
actual image/header and same genuine I receipt850c33b2... . Its recorded phases
are150ms bounded read/native preflight,15ms genuine boundary receipt verification,
5279ms guest execution/segment custody; these are wall, not CPU. COMMAND SHA
`4c03605b4bb620f0d314b88292f73f36fd0a811bdbb8a25c91ca4bc216254c6f`
has the exact selected host/args. Independent byte comparison confirmed that
wire/header differ from retained native inputs only in the32-byte A slot. New
wire SHA is `5d648e3e92585447911b67a960fffea1ea3ff1971c4784e8a4721b77d1bf680f`.
Inner host stdout is empty; adapter retains diagnostics and failure normally.

The sample table has131,072 cells, sum of retained sample counts131,454,
23,898 omitted samples,39,769,880 observed instructions, stride256 and no
backwards-coordinate event. Its reported maximum coordinate153,044,530,811
must NOT be called a guest proof-cycle count. Attribution requires the exact
sampler/get-row-points semantics and separately bound ELF/map, and deterministic
saturated instruction samples do not estimate proof-cycle shares by themselves.
This is useful bounded-prefix evidence for source analysis, not completion,
speedup, proof affordability or mathematical admission. Root explicitly declines
automatic cap increase or retry. All used screen inputs/source/evidence freeze.

### Aggregate snapshot01: exact prelaunch cost-screen clearance

Exact9,223B selection
`224ec1f99cb8e9dc59e290eddf526be2bbc7cad7aa13a7146110e31972f08e79`
cleared after all37 bindings matched (eight sources,29 runtime/data pins), with
fresh output absent. Exact550B configuration
`7ba7ae7b407d572b96f84f262c58fdd6ff2e7aef1cff1befee365fc361590c0c`
binds actual assembly097775f5... and image ID51d51ea0... . The previously reviewed
snapshot source d99656a1... is unchanged. Only the32-byte A slot in retained
wire/header is rebound; exact Js, member root, edges, witnesses and genuine I
receipt remain fixed. Actual host independently computes image identity and
checks native relation/header/pending receipt before one guest execution.

Single2^25-cycle,po2=18,pc-samples cost screen,120s inner timeout under
180CPU/240wall,3072MiB/three-active outer bounds; at most144MiB/160 output entries.
No proof, automatic cycle/budget increase or causal speedup comparison is selected.
Unchanged host/assembly/runtime audits are reused. Root owns launch and later
actual adoption; prelaunch clearance is not execution success.

### Aggregate assembly01: actual image-only PASS

Actual inner742B RESULT
`097775f5318420936b3cce6f16485467ae9fccd68d58947ec76facd210907420`
passes independent outcome review. Image is1,741,060B with file SHA
`c19aa3f6e8d27a9c1681bbafd5958b359328520596313c25dd91eba521bc633e`;
actual retained-assembler image ID is
`51d51ea0ba1f4e4402615e04e64c739dcd497145aa8ecf8e89ed8d03f8177c49`.
These are different identifiers and must not be substituted for each other.
All13 changed current/snapshot/selected-lineage/image bindings match, exact
inner stdout agrees with image ID/length, both stderr logs are empty, and no
inner finalization override exists. Previously adopted unchanged driver/runtime
pins are reused, not a new SDK audit.

Outer RESULT
`2da4d6fed5c4d3daee7e44f89d254160a2e751692f52af73b4b93e80a3e11fc0`
confirms exact selected argv, exit0/reaped/Jobclosed, zero active/terminated
processes, no termination/cleanup errors. Cost0.5625 inclusiveJobCPU plus0.4375
disjoint wrapperCPU,5.358370800036937 wall. COMMAND
`22fe99b12e17a6acdd28498dd908bd7144ae39cf09c235b2d2364b33b16f9447`
binds actual artifact adoption a9d60ab0 and preserved old resource failure,
same exact ELF/kernel and one retained assembler call. No guest execution or
proof occurs. Source/selection/assembly evidence are now used/frozen. A local
read-only audit output mistakenly serialized PowerShell string metadata and
became oversized; it changed no project file or runtime result.

### Mixed import/session and ordinary authoring: source clearance

Reviewed full fresh sources and ten prospective synthetic groups:

| Source | SHA-256 |
|---|---|
| `mixed_claims/imports.py` | `50b09b084b7cb54db2b1196e3570f1b15066e85e9ce55002b8d27bb4460cb1df` |
| `mixed_claims/authoring.py` | `8b09cb1b8f0466a5049ed53f7b28098b6022234e3681786b2f4a9f542cd83e1b` |
| `mixed_claims/test_imports.py` | `93ff0a2cd9065bb8ba97fefb9fe9b4e33a0362c28b35156402fa76627e23064a` |

One concrete source gap was corrected before use: a pure A-only session originally
required only four mixed files, while directly calling `delta_claims.claims` and
eagerly importing receiver/delta/production dependencies not required by the A
owner's own nine-file minimum. The final session requires all21 loaded project
origins and their pins through configured owners. These are source-file requirements,
not a requirement for any I/native executable or process. Final new-source
snapshot failure also explicitly closes the session before state publication.

Authority argument: each closed typed entry obtains a live exact I handle,
A-member handle or mixed closure. Copied facts, unrelated-owner handles and
receipt bytes alone do not suffice. Source snapshots bind exact profile, statement,
receipt/packet identity and full member inventory. Chosen records bind complete
proof form, payload and parent tuple; same-J conflicts require exactly the
explicit incoming/existing map, never partial edges or a lower-rank substitution.
All fallible merge construction and final authority checks precede single-owner
map publication. Refused imports retain input/call charges. Independent M-to-J
direct selections are immutable; representation changes increment a monotone
revision and cannot revive old authoring bindings after a reversal.

The onward serializer walks only selected exact-parent ancestry, stopping at
chosen I/A terminals. Same-J native-to-A replacement can therefore cut witnesses
without altering descendant journals, ranks or bytes. It does not prune the
sender's retained authority records or extend their lifetime: all configured
owners/retained sources remain live conservatively. Receipt data deduplicates
exactly; same SDK claim with different receipt bytes refuses until explicit
whole-J resolution. Final new target cannot be substituted by inherited equal-J
material, and the new packet parser checks the complete emitted closure/caps.

The authoring adaptation keeps I/F/P in frozen data-only `RelationBasis`; the
private frozen foundation view exposes only the F/P fields actually read by the
retained pure decoder. It never masquerades as an admission owner or weakens
an exact owner/session gate. Existing semantic traversal, name relocation,
relation-row emission and owner-controlled Lean worker are reused; requests,
exports and returned mixed packets remain untrusted until actual native/receipt
admission. Transparent-body and opened-group commitments remain semantic-M based.

Ten unrun source-read controls cover pure A-only entry/preparation, copied-fact/
foreign-handle/receipt refusal, shared receipt storage with submission charges,
same-J ancestry cut with byte-identical descendant, atomic exact conflict map,
stale-operation reversal, claim-receipt conflict resolution, closed-origin and
final-authority refusal, and required eager pins. They deliberately fabricate
authority, use the frozen mock receiver and mock the pure foundation decoder;
no actual cryptography, Lean worker, native checking or file operation occurs.
No remaining source blocker found. Installed source-origin checking, actual
ordinary authoring and real A-certified ancestry cuts are not established by
these mocks. Repeated local source hashes/live snapshots and finite owner-call
allowances remain real costs, not logarithmic total consumer work.

### Aggregate assembly01: exact prelaunch clearance

Exact9,685B selection
`bfe448433889fe42a3e357317ee59ed7fd3046aecf1ec9045951765bdc69c7fb`
cleared: all35 bindings match (two sources,33 runtime/data pins), fresh output
absent. It invokes reviewed61587d9a snapshot source with the actual adopted
a9d60ab0 validation record, retained assembler/kernel and exact ELF. One assembly
only,120CPU/120wall,1024MiB/two active processes,1MiB logs. The original resource
failure remains required; no guest/proof execution belongs to this gate.

### Artifact validation01: actual separate artifact-adoption PASS

The separately selected named-file validation completed and passes independent
outcome audit. Inner16,788B RESULT
`a9d60ab02a01f87bed72c0ee9053e56e698a6c8f5dae93d6f1ba9b3cc3b3da6f`
records `PASS_REVALIDATED_AGGREGATE_GUEST_ARTIFACT_ONLY`; outer RESULT is
`d01e95e039db45f6a2a638255b90b42d6f2f3659375d67f8ba6149637d818fe0`.
All60 checked bindings match (56 named retained files and four current/snapshot
source bindings); saved selection is exactly48856d2e... . Actual isolated
snapshot argv is correct, no inner finalization marker, exit0/reaped/Jobclosed,
zero active/terminated processes, no termination/cleanup errors, stderr empty.
234B stdout names only the artifact pass and zero new compiles.

Cost0.390625 inclusive JobCPU plus0.390625 disjoint wrapperCPU,
0.8742817000020295 totalwall. Inner0.203125 controllerCPU is already included
in JobCPU and must not be added again. The original FAIL_FINALIZATION and its
228worker/195.203125controller/547.537434700178wall cumulative record remain
explicitly preserved. This gate adopts only the exact retained source-bound
ELF/map; no image assembly, guest execution, receipt or mathematical admission
has occurred. Validator/source and evidence are now used/frozen.

### Artifact validation01: exact prelaunch clearance

Exact20,859B selection
`48856d2e9ba66a7b1de4d2062904d0140cbf94ec63f8d654d5201316d672f212`
cleared after all78 bindings matched (two sources and76 runtime/data records).
Fresh output was absent. The unchanged local-check runner invokes the reviewed
715733a3 immutable source snapshot with installed Python `-I -S -B` and
`--output {output}/validation`,30CPU/60wall,512MiB/two processes,1MiB logs.
It selects only the independent named-file artifact gate; no compilation,
graph/SDK census, image assembly, guest or proof. Root owns the single launch.

### Narrow artifact validator and explicit assembly successor: source clearance

Reviewed `aggregate_guest/validate_artifact.py`,13,843B,
`715733a37e150d307a99008970ea26fca84f5234beba17e4147577d58ed0f7c4`.
It binds12 exact preserved records,39 project/lock files, the used controller,
two compiler logs and ELF/map:56 named files, with a final bounded byte rebind.
No subprocess, project/SDK import, compilation, graph invocation or tree census
occurs. It independently checks actual Cargo artifact/finish records, exact
ELF headers/startup mapping and equality to the preserved records. It requires
the overriding old resource failure, reports old budget unmet and cumulative
charged costs, and emits the distinct artifact-only validation result. The
previous completed SDK rebinding is explicitly reused as provenance. Internal
24CPU/45wall checks and final override leave margin for the separately proposed
30CPU/60wall,512MiB/two-process outer operation. No actual pass is assumed.

Reviewed revised still-unused `aggregate_guest/assemble.py`,12,602B,
`61587d9a15a093c25b89f3e7d76439011c39831cbca8d19d986cd45db5426750`.
Its API now requires the exact new artifact-validation record/pin, distinct
artifact-only PASS and no validator finalization override. It explicitly requires
the preserved original81cce68d compile result AND d0d6d898 resource-failure marker,
with exact artifact equality; raw build PASS alone is no longer an accepted
entry. Validation/failure lineage, ELF, old graph, retained assembler and kernel
rebind before/after the same sole assembly call. Actual image ID remains distinct
from file SHA. This supersedes the unused9f4de50b source clearance below; exact
selection and actual outcomes remain separate. Neither source is executed here.

### Aggregate compile01: actual artifact, failed controller envelope

Root reports session72234 terminal/reaped. The effective operation result is
**FAIL_FINALIZATION**, not PASS. Raw 9,499-byte RESULT
`81cce68d9b20f22b12d12d5d698084eb8eb101493de71c6e35cd6acb7b44f47a`
and attempt contain the earlier PASS status; the explicit 202-byte overriding
`FINALIZATION-FAILED.json`,
`d0d6d8980c492d43a8927825aa153271543fa18d960305db5bde1e51c323dd54`,
binds that result and records `REMAINING_TOTAL_ENVELOPE`. Do not ignore it.

The single selected offline compile itself completed exit0 with clean phase
closure, zero active/terminated processes and no cleanup errors. Worker CPU was
222.640625 seconds, compile-command wall 197.98855440015905; controller CPU was
149.640625, above the remaining 134 by 15.640625. Recorded total operation wall
was 401.11681869998574. With the preserved failed graph prefix, charged totals
are 228 worker CPU, 195.203125 controller CPU and 547.53743470017798 wall seconds.
The controller total exceeds the original180 allowance; this is not repaired by
otherwise spare worker/wall budgets. Final-report/exit tail remains excluded as
disclosed in the result, not invented zero cost.

Read-only independent checks matched all39 frozen source/lock files, both
artifacts and two logs (43 actual bindings), plus controller/selection and
record-to-record equality. The current controller remains the reviewed17,854B
`d8e4bd4c9df8ac3fc8e8b1a4f5eb62333ce97817e954fcd08f1e3e687fc35c0b`.
The reused39-file map equals its preserved predecessor. Actual Cargo stdout
contains one fresh exact intended binary, release opt3/overflow-checks true/test
false, and one successful build-finished row. The existing runtime/SDK closure
review is reused, not independently rehashed in this outcome audit.

| Artifact/record | Bytes | SHA-256 |
|---|---:|---|
| user ELF | 1,682,292 | `8aa35bf0a3ab57ef1caea04cceaae9659fd6c994009a1abad154df8dcd6d5868` |
| link map | 2,614,124 | `2292e7fa3340775db8626529e1e0fd7f743504991afc3c494006b78dc1c9f3b7` |
| SOURCE-MAP | 1,066,113 | `75c710e3ee13f63cb6ef44da8656caa53c300bf649317d2b5669d8b9cde06ce0` |
| GRAPH-COMPARISON | 2,069 | `a7f5ea2fe059e6a57a6aaad48e616986267afe2b7c8a8c60de3194e2b010d458` |
| ARTIFACT | 1,338 | `dc3a4f79e1006bf45d8355829486ee0b2bb019bd4fd12cf45fb0aec37cfc5904` |
| environment profile | 6,049 | `7e1b195a0e075eec9ba8f0d7f8e65c83a9a3cebfc3332e7910d9909be2581ff5` |

Precise source-order finding (`compile_only.py`271-295): finalization first
closes the phase, completes the full source/runtime `rebind`, checks registry
archives, calls `budget.refresh`, and then separately censuses the output a
second time. `refresh` checks controllerCPU/wall at its **entry**, before doing
its own census. The saved PASS status and final census show these checks completed
without exception. Therefore full rebinding/archive checks had finished before
a successful <=134 CPU checkpoint; the later census/report tail produced the
recorded149.640625, and the final refresh detected the overrun. The precise
crossing inside that tail is not measured. Do not claim that all finalization
ran within budget or that the failed allocation passed.

A new finite retained-artifact validation/adoption seam is justified in
principle: bind the failure/override and original selections, exact frozen
project/graph/native lineage, actual Cargo artifact row, ELF/map and completed
rebinding evidence under a fresh explicit bounded read-only operation. No
compiler, graph, guest or proof rerun is necessary. This is a distinct gate,
not automatic artifact adoption or a retroactive resource waiver. The existing
assembly adapter correctly rejects this failed lineage; a separately reviewed
successor must require the new adoption result, never simply bypass the marker.
Old bytes/costs/failure stay frozen. No image or aggregate proof exists yet.

### Mixed receiver controls01: actual twelve-group PASS

Actual RESULT
`c376471ddd74a0352ce21eae8ea4d89f9366eae0a79c303e8b0f672aeceba00a`
passes independent synthetic-outcome audit. All46 source bindings (23 current
and23 snapshots) match, saved selection is exact8b0557bc..., and stderr1684B
`7e518ed67db821906e7f053752fc18da86a8d7a10afda0847b1e019b298c983b`
enumerates all12 selected groups with `ok`; stdout is empty. Actual argv uses
the selected installed isolated Python and immutable test snapshot. Exit0,
direct child reaped, Job closed, no termination/cleanup errors or active/
terminated processes; no finalization override. Cost0.96875 inclusive JobCPU
plus0.328125 disjoint wrapperCPU,3.115848399931565 wall seconds. The fake owners,
native responses and filesystem are intentional; this is not real I/A receipt
admission, actual native mathematics, installed pin-origin qualification or
public session/authoring integration. Source files are now used/frozen.

### Mixed receiver controls01: exact prelaunch clearance

The 9,044-byte selection
`8b0557bca9af01b5db8b23cc5d1a7214cc95eaf849fb84ac343faa49fc5078b4`
passes exact review: all 44 bindings match (23 selected sources, including
the fixed eager closure and runner, plus 21 runtime/prior-selection/manifest
pins). Output was absent. It uses the retained runner and installed Python
with `-I -S -B` against immutable `mixed_claims/test_receiver.py`, under
30 CPU/60 wall seconds, 512 MiB/two processes and 1 MiB each log cap.
The earlier source review covers all twelve groups and explicit mock scope;
no native, crypto, guest, network or real test-side filesystem operation is
selected. Root owns the single launch. This is prelaunch clearance, not PASS.

### Mixed I/A packet and receiver: first-phase source clearance

Read the complete fresh `mixed_claims/{__init__,packet,receiver,test_receiver}.py`
and the used parser, journal, membership, authority and clean-process helpers.
No test, native process, receipt verification or build was executed by this
review. Final reviewed SHA-256 identities:

| Source | SHA-256 |
|---|---|
| `mixed_claims/__init__.py` | `2371afae23fa43f733cb959557a9451df64ce4181a4a9ec5ef72ec28d9290abf` |
| `mixed_claims/packet.py` | `8a18e3d35e33210df9b669b3fe8dc3785e13bfb1184bd0bd2fbec683063758b1` |
| `mixed_claims/receiver.py` | `d292a966469402a24282e40377c8ac9c929504e38de7862aa9a6bd1b3ad3fb00` |
| `mixed_claims/test_receiver.py` | `a75ce1e30e9328ddbe6f27d79dff38d47412001af8d816743702489788ee96b3` |

Caught one eager source-closure omission before use: `delta/__init__.py`
imports `delta.receiver`, so pinning only `delta` and `delta.packet` was
insufficient. The author added its exact loaded-origin and file-pin requirement;
the receiver identity above includes the correction. Other eager project imports
(`delta_claims.receiver`, `production.producer`) were already covered. This is
loaded-source selection under a trusted controller, not Python-memory isolation.

The packet is a new typed wire, not a reinterpretation of the old I-only wire.
Tag0 binds an exact 184-byte J to an I receipt; tag1 binds exact H to an A receipt
and each selected J to its exact opening. All adopted I/F/P/A, byte/count/rank,
duplicate, unused, topological and complete target-backward closure checks occur
before expensive verification. The reused old decoder only parses witnesses;
the new parser separately checks full-J graph closure. Its 32 MiB/32-frontier
limits fit the retained `delta.packet.Envelope` ceilings. Repeated semantic M
with different exact Js remains possible; duplicate exact claims/Js refuse.

The receiver uses exact optional I/A owner classes, at least one. An A-only
supervision donor never replaces native relation image I with A. Each claim is
verified once, its complete statement and live handle are rebound, and the cache
key includes tag, profile, full statement, receipt digest and receipt length.
In particular I admission compares full J including rank, not just semantic M;
A members borrow the same live aggregate owner and exact header/path. Each
native witness reuses retained `bind_native`, closure and `_clean` rules, with
original parent tuple, exact rank and actual same-call input/output binding.
All borrowed origins are checked around native work and again after evidence
I/O, before a distinct local mixed handle can be minted. No file or copied fact
is promoted into receipt authority. All packet/call/CPU reservations precede
cache reuse and survive failure. Mixed-owner failure does not directly close
separately owned I/A authorities.

The twelve source-read controls include typed wire/path/graph/cap refusals,
same-M/different-J coexistence, full-I-rank refusal, mocked A-only native-I
dispatch and one-call receipt sharing, charged cache reuse, pre-worker refusal,
and five native/final-liveness failure modes. Their fake owners intentionally
bypass real installation/cryptographic checking, fake supervisor is in-memory,
and directory creation is patched. They establish no actual receipt, kernel,
filesystem containment or integration outcome until a separately selected run,
and even a passing run establishes only these synthetic boundaries.

No remaining source blocker found in this first phase. Repeated local pin
hashing and member-live calls remain charged implementation costs; this review
does not claim constant total consumer cost. A-only direct session import,
same-J certified cut, ordinary authoring and actual A receipt integration are
separate unfinished seams, not cleared by the packet/receiver review. Root owns
any exact runtime selection and adoption; the live guest compile is unrelated.

### Assembly successor: compile-only lineage and immutable-snapshot invocation

The unused assembly adapter was revised for the new one-command compile
lineage. Latest reviewed source is 10,305 bytes,
`9f4de50bd35d13809eaa7a5340edcd15b7784e6be102cff3e7f7bb577bebe888`.
It requires the new compile result schema/status, one closed compile and zero
new graph calls, plus exact predecessor FAIL/raw graph/attempt identities. The
failed result stays FAIL; its one successful graph is only explicit lineage.
All these bindings recheck before and after unchanged driver/kernel assembly.

Caught the initial adapter's incompatible canonical-__file__ guard before use:
the existing outer runner invokes an immutable source snapshot. Latest code now
requires the resolved six-part path below local-checks exactly
`<operation>/sources/software/v5/aggregate_guest/assemble.py`, with bounded
lowercase operation name, canonical working directory and isolated flags.
This matches the runner and deliberately rejects direct source invocation.
Outer exact selection must still bind the operation/source/runtime/artifacts.
No actual compile result/image or assembly invocation is assumed by this review.

### Compile-only successor: four literal path correction and exact clearance

Reviewed `aggregate_guest/compile_only.py`, 17,854 bytes,
`d8e4bd4c9df8ac3fc8e8b1a4f5eb62333ce97817e954fcd08f1e3e687fc35c0b`.
The four saved Cargo local target paths retain manifest-relative `..` segments.
Independent inspection confirms each resolves to its exact pinned intended
source. The successor corrects exactly those four literal expected fields and
requires complete 297-unit identity/dependency equality; it does not generically
normalize arbitrary strings or weaken external package/profile/feature checks.
Failed RESULT remains FAIL. The saved graph and unchanged 39-file project/lock
are reused, with a fresh target/private byte-identical registry seed and exactly
one offline locked compile. No graph command is repeated. New result schema
explicitly records predecessor result/graph/cost rather than pretending two new
commands ran. Assembly needs a separate explicit one-command lineage branch.

Exact 661-byte selection
`19fef22ed3323d963349d67c131cea7a7b1dea8de82321be9ef2c33ffe06b7cd`
cleared: parsed proposal differs only by true authorization, source pin matches,
five frozen prefix records plus attempt pin match, fresh output/attempt absent.
The prior exact runtime closure is reused. Remaining 1794 worker CPU, 134
controller CPU and 1653 wall seconds give maximum combined actual-prefix plus
allowance 1799.359375/179.5625/1799.420616 seconds, below original 1800/180/1800.
The 4096 MiB/eight-process/16 GiB ceilings remain. Root owns one launch;
no image, guest execution, receipt or proof is selected by this clearance.

### Retained aggregate cost screen and mixed-frontier contract review

Reviewed `aggregate_host/snapshot.py` at
`d99656a17891983e2ae5ee0afb78fd4695b0ac4746a58aade34977b36fd2f442`
and `AGGREGATE-COST-SCREEN.md`. Preparation replaces only the 32-byte A slot
of the exact retained 215540-byte wire and 192-byte header. Exact Js, openings,
membership root, edges, targets and genuine I receipt remain unchanged. The
existing host independently computes actual image ID, checks the complete native
relation/header, genuinely verifies exact pending I, then executes the guest
once with bounded retained segments/capsule and same-run samples. Adapter binds
returned header/capsule/diagnostic and final inputs/census. A failure stays a
failure; diagnostics are available only if the host reaches their durable write.
Future exact root selection must provide actual adopted assembly pins and an
outer 180 CPU/240 wall, 3072 MiB/three-process Job. No proof production or
causal speedup claim follows from this source-only screen.

Reviewed the proposed mixed I/A packet/receiver contract. No semantic blocker
found. Sent critical invariants: A-only supervision still selects native image
I; I receipt imports compare full J including rank, not only M; exact claim/
receipt/owner/profile cache entries retain live-origin checks before/after
checking and final mint; packet/graph/cap gates precede expensive work and no
same-claim/different-receipt ambiguity is silently chosen. Explicit whole-J
selection can resolve such representation conflicts later. Pure A-member
session entry remains separately possible without a dummy delta/I/native owner.
First implementation phase is separately owned and remains source-only.

### Aggregate owner controls01: exact selection and actual PASS

Exact 7,299-byte selection
`4e57759d8aa1f359b996d837bcc00312759e9e9c8a55f99d8fc9bbefe3cf1a95`
cleared after all 31 bindings matched: 11 eager sources and 20 runtime pins.
It invokes the adopted installed Python with -I/-S/-B against one immutable
controls snapshot, under 30 CPU/60 wall, 512 MiB/two processes and 1 MiB each
stdout/stderr. Fresh output/attempt paths were absent; unchanged runner and
runtime reviews are reused. Only the outer supervisor writes real evidence.

Actual RESULT
`cf0faa4a6984675410ba47131b8476b890528aa80d01ec1c6cce67e3481b702d`
passes independent audit. All 22 current/snapshot source bindings and saved
selection match. Stderr is 3,004 bytes,
`8b4f0fd8f2cbe3dbb16a4dc09b3d3b886fdd292d744315409bff48db90d059a4`,
and enumerates all 17 selected method names with `ok`; stdout is empty.
Actual argv uses the exact installed Python and snapshot. Child exits zero,
reaped, Job closed, zero active/terminated processes, no termination or cleanup
errors. Inclusive Job CPU 0.78125, disjoint wrapper CPU 0.28125, total wall
3.2813306997995824 seconds. This is synthetic bookkeeping/mocked-receive
evidence only: no real receipt verification, native checking, guest or proof.

### Aggregate owner controls: final source clearance, not execution

Owner remains `a6a7e8041674de60fff198ed8522b1c28e0662bbf1f8acce8fe3eee60ab03561`.
Final 17-group `aggregate_admission_controls.py` reviewed at
`dc6ba079cb9c2bb60b001ea9a25ea9da7eeea83970d7b68123fa0f34d742fa6a`.
The added in-memory fake supervisor intercepts every write and worker call.
It checks exact `verify A receipt header` arguments, selected header/receipt
bytes, request/process/binding ordering, and the original 60-second allowance
after three seconds of simulated preflight. Six refusal cases reach wrong
statement, unclean closure, changed receipt/header, final pin and final
deadline boundaries. They require no minting, owner revocation and retained
reservations. Prior member/constructor/origin controls remain explicitly
synthetic. No files, host, kernel, guest or proof run in those test bodies.

Public-admission notes now include full repeated O(L+p) local pin-hashing cost,
distinct from Merkle work, and exact entered-receipt-revoke versus malformed-
member-refusal semantics. Source review clears a future root-selected bounded
synthetic run, not actual A receipt admission or full mixed-frontier reuse.

### Guest build01 actual graph-gate failure: preserved, no ELF

Actual RESULT
`231c94114e625a59371fdb1208aa7ae2838c9c35c9b8877b80bead4e7ad7e0ac`
independently audited. All 79 changed file bindings match: 38 current sources,
39 snapshot files including generated lock and two graph logs. Saved selection
and terminal/finalization markers match. One selected offline graph command
exits zero, produces 297 units and empty stderr, then the exact structural
gate raises `UNSELECTED_FULL_AGGREGATE_GUEST_GRAPH_DELTA`. Raw graph SHA256 is
`2cc441345c1cf3cc16e9dd21cca1bf2130319dbfa1124ad3ddb1d6507f2f4609`.
There is no compile command directory or new guest ELF. This is a failed
graph qualification, not a build success or a reason to weaken equality.

Worker CPU 5.359375, disjoint controller CPU 45.5625, total wall
146.42061600019224 seconds; graph phase wall 19.535597099922597, peak Job
private bytes 47210496, eight total processes. Zero active/terminated processes
and no cleanup/finalization error; root reports outer exit one and reaped.
Preflight/final hashing and copy costs remain counted in controller/total wall.
Raw graph diagnosis is separately assigned; no automatic retry is cleared.

The already reviewed assembly adapter remains unchanged at `4b9f0b54...` and
refuses this failed RESULT at its initial build-PASS predicate, before creating
its output directory, looking up the ELF or invoking any assembler. No image,
execution, receipt or admission can follow by that route. All failed bytes stay
preserved. Full v5 remains ACTIVE and unfinished.

### Aggregate image assembly adapter: source-only clearance

Reviewed fresh `aggregate_guest/assemble.py`, 7,814 bytes,
`4b9f0b54b44fcd34d239341b9e6e2081510bf9fa2a74b23202a7fa8476f34b0f`.
It requires an exact successful new aggregate guest build, its two closed
commands, matching terminal marker, no overriding finalization failure and
the exact new guest ELF path/pin. One existing pinned driver04/v1compat-kernel
assembly writes a fresh aggregate image. The actual assembler's image ID is
parsed separately from the file SHA256; input/artifact pins rebind before and
after. No guest execution or proving is added. Source review is conditional on
the explicitly required outer root-selected bounded Job with exact source and
output controls; the inner subprocess capture is not standalone hostile-input
resource containment. No actual guest result or image is assumed yet.

### Aggregate public owner: initial implementation source review

Reviewed fresh `aggregate_claims/aggregate_admission.py` at
`a6a7e8041674de60fff198ed8522b1c28e0662bbf1f8acce8fe3eee60ab03561`.
Two pre-freeze findings were corrected: supervisor allowance now measures the
original absolute call deadline without subtracting preflight twice; nine
actual imported module origins and critical imported symbols bind to required
source pins rather than merely coexisting with pinned files from another install.
Constructor virtual-hook fields are initialized before base invocation. Final
profile is A-specific; all statement-facing inherited methods are overridden.
Exact A/member registries remain distinct from I handles, and every authority
use rechecks sources/install/profile/lifetime. Same-call verify/header/stdout
binding, immutable member records, charged cache hits, owner revocation and
final output/deadline-before-minting behavior are coherent by source review.

Caller Python/controller state remains trusted; group serialization allocates
before byte charge, so external decoder/process limits remain necessary. Jobs
are resource controls, not hostile-code containment. The source does not make
a synthetic image into an adopted actual aggregate checker.

Read the initial 15 explicitly synthetic owner controls. Their fake registries
and mocked constructor cover membership/origin/budget/copy/lifetime bookkeeping,
not real cryptography. Requested one narrow mocked same-call receive control
with command/report/header/stdout/finalization subcases before the first run:
the initial tests only exercised `receive` at malformed-header preflight. This
is to catch an adapter mismatch before real A production, not to simulate
mathematical qualification or authorize any host/guest/proof operation.

### Aggregate-host actual PASS; guest exact selection cleared

Host build01 actual RESULT
`4cdb12b5e3aeaebcfef5e0370bd445f24ff6779b196ca69cbab60f9d57002a75`
passes independent audit. Nine changed source/snapshot/output/log bindings
match. The actual command equals the retained recipe with exactly the selected
crate/source/output substitutions and two new externs/dependency paths, modulo
Windows path-separator spelling. One compiler exits zero. Four unused-field/
method warnings do not alter its outcome. Permitted pinned owned VCTIP cleanup
records its exit; there are no cleanup errors, active or terminated processes,
or overriding finalization marker. Root reports outer process reaped.
Executable: 6,626,304 bytes,
`b1605995c957e06b7c4529d28dfc2a49e496cefae7629b3fdddfc4a1bfb6f6d1`.
Actual worker CPU 65.375, disjoint controller CPU 6.640625, total wall
72.20371129992418 seconds, peak Job private bytes 987435008. Compile-only:
no host execution, image, proof or public aggregate admission yet.

Guest exact 15,652-byte selection
`011ac45c532756eba74a573f66a06e1a2f0e78ba1219aed2bdd6bef8a3d67f70`
is cleared. Its parsed proposal differs only by true authorization. All 38
source pins, five retained guest records, eight preparation records, helper,
native map and actual comparison result pins match. Actual old 296-unit
metadata supports the predicted local package/profile/target transform, including
lib/bin doc/doctest/test flags and std edges. New manifest source paths must
equal canonical targets in actual Cargo output or the precompile graph gate
refuses. Source/graph review is not a prediction that Cargo necessarily succeeds.
Outer 1800 wall and 180 controller CPU start before preflight; one shared worker
allocation covers both Cargo calls. Fresh run/attempt paths were absent. Root
owns the memory-aware timing; no guest execution/image/proof is selected.

### Aggregate guest overlay: builder/graph source review

Reviewed `aggregate_guest/graph.py` at
`2bbab886704aaa72ba4c6415b4187a1f5b0e699b6f3d61c512f16ea0d425af31`
and `aggregate_guest/build.py` at
`4e986f7d2b6d6560b81e98a5d490d9488795ef64111300d12cf264e036c60038`.
All 38 source pins in inert proposal
`e10b3a5d5f32718583e41986d7b46dd6bb514867f31f5c3fc9cfbe0bf3978729`
match. Exact lock parsing permits one added local aggregate package and no
other package/checksum change. Graph canonicalization includes full unit
identity plus dependency metadata, replacing numerical indices by target
identities. Selected transformation relocates two local libraries, replaces
the old binary root and adds one aggregate library. Only root/library direct
nanoda/serde edges disappear; module edges and all build-std edges remain.
Every external package/version/feature/profile/target/edge must compare equal
modulo the selected cache relocation. Actual Cargo output is still unobserved.

Builder preserves the retained RV32 compiler/build-std/SDK/startup recipe,
checks the independently adopted new native comparison, uses fresh target and
offline cache, and runs exactly graph then build. Graph equality must pass
before the compile. Snapshot includes the 32 native Rust sources, unchanged
entry, three overlay manifests and two adapters. Final maps, locks, seed,
runtime, output and cleanup are checked; the emitted ELF/link map are pinned.
Envelope is 1800 cumulative worker CPU/total wall, 4096 MiB/eight active
processes, 180 controller CPU and 16 GiB combined census. Source clearance
does not select execution, prove graph equality, adopt an image, or authorize
guest execution/proving. Root owns a later exact selection and resource timing.

### Native compare01 actual PASS and aggregate-host link clearance

Compare01 RESULT
`f60945682fd510c837a26c6bc1703fe8065e8e1a2a301d675e9f869d44384d33`
independently passes the actual changed-boundary audit. Exactly two selected
native commands exit 0/2. All four actual logs, source snapshot/current source,
parsed selection and finalization bindings match; both stdout byte sequences
are identical to their retained positive/invalid baselines. The negative stderr
is the fresh checker snapshot's native `tc.rs:945:71` equality assertion, not
an input/setup rejection. Jobs close cleanly with zero active or terminated
processes and no cleanup errors. Worker CPU 0.0625, disjoint controller CPU
1.90625, wall 3.217172999866307 seconds. Root reports outer exit zero. This
supports preservation of these mathematical boundaries, not measured speedup,
guest execution, certificate production or final v5 completion.

Fresh `aggregate_host/build.py` source reviewed at
`0c6a98237e63b1245e20af1a95fb91cf42231064345ce8d22d160ad1c99e62a2`.
Exact 962,683-byte selection
`b8c64994f64c66eaa8a90612d5fa0f3ebcad4ce053e86f4f8fe485408cadbb8b`
independently matches all three source and 3,142 runtime pins. Enumerated all
2,962 files under the retained host dependency/native search directories: all
are pinned. Every Rust rlib/rmeta/dll in the added checker dependency directory
is pinned; its unused proc-macro import-library/depinfo files are not Rust
dependency artifacts. The integrated dependency directory contains exactly the
three pinned fresh project rlibs. Retained host RESULT and LINK-INPUTS pins
match, and fresh run/attempt paths were absent.

The one command replaces old host crate/source/output exactly once, retains
five SDK host externs and adds the two selected project externs; fat LTO and
native search paths remain. Three source snapshots include the relative
`../aggregate/receipt.rs` at its correct path. Host SDK serde identity remains
unchanged; the new relation boundary uses primitives and its own Header/J,
not exchanged cross-version serde traits or Values. Cumulative envelope:
240 worker CPU/phase wall, 3072 MiB/six active processes, 120 controller CPU,
600 total wall, 1 GiB/8,192 entries with final pin/map/closure checks. Root
owns one compile/link launch. No host call, guest, proof or admission follows
from this clearance; the full installation is not claimed OS-hermetic.

### Aggregate public-admission principle: source-backed support

Reviewed `AGGREGATE-PUBLIC-ADMISSION.md` against the actual existing admission
owner, journal/member/output binders and aggregate Rust receipt/host paths.
Support the proposed minimal new aggregate owner and later typed mixed frontier.
The base constructor loads and pins supervision but does not perform I admission;
a narrow subclass with final A-specific profile and disjoint exact opaque handle
registries can reuse it. The host really calls full receipt verification with
dev mode disabled, genuine succinct Poseidon2, adopted image and exact H. An
inert output/member binder alone remains incapable of mathematical admission.

Implementation guardrails sent to author: override inherited `describe` as well
as the new describe methods; initialize fields used by any overridden hook
before the base constructor dynamically calls `_check_install`, or retain that
hook unchanged; check source/runtime pins and live parent on all authority uses,
not just `_active`. Member decoding already reconstructs and binds the semantic
summary from exact J. Direct A-member import must not require a dummy delta or
an I verifier process. Later source/exact/runtime reviews remain separate.

Under the stated checker, branching recursive proof and hash-binding assumptions,
the seal-height/native-rank induction and explicit same-J complete-record cut
are coherent: an A terminal establishes the identical child premise, so descendants
need not be rewritten and unreachable unsealed ancestors can be omitted onward.
The fresh-target condition remains separate. No actual A image/receipt, positive
mixed-frontier integration, growth advantage or v5 release is established.

### Proof-validation compare01: source and exact selection clearance

Reviewed fresh `proof_validation/integration/compare.py`, 12,277 bytes,
`d0b0bc18788cd8df2334dec97b488b2a33e61a21999e64bf40ac5fec6d03aff7`.
Exact 704-byte selection
`4f8f35b41fd42ff5a4c5709912a7fe87431d375e784d6d3c68dbf15a692de6c1`
matches proposal `564a464c60d8df4b7f7753d6383104eac40e63aeeaa3fef2590d3a4264df8050`
except true authorization. Six retained baseline pins, four new outputs, exact
build RESULT/finalization, 174 retained recipe runtime pins and the helper
predecessors match; output and attempt were absent. Root owns the one launch.

Exactly two new native calls use the retained positive and invalid-proof inputs;
both stdout byte sequences must equal retained outputs. The invalid case must
still exit two at native kernel `tc.rs:945` with `self.def_eq(u, v)`, not a setup
failure. There is no baseline rerun. One cumulative 60 CPU/60 phase-wall-second
Job, 1536 MiB/two processes, 60 controller CPU/300 total wall, 16 MiB/128 entries
and final input/snapshot/budget/closure checks bound the operation. D:\Python314
is required. This is a mathematical-boundary comparison, not guest affordability,
receipt authority, standalone optimizer speed measurement or deployment evidence.

### Full native optimizer integration build01: actual compile-only PASS

Independently reviewed actual RESULT
`55ba9a702360dd10a6b9bea00f481d5066553a1b8debcb10ca43bbcab4de4069`
under `experiments/v5-local-checks/proof-validation-integration-build-01/`.
All 78 changed bindings match: 33 current sources, 33 immutable snapshot
sources, four outputs and eight logs. Selection remains
`948c505ea10547885cf316ff0ecc336df459c625fa671f185f6659ebc298e9f9`.
The four actual successful commands compile checker, module, aggregate and
driver in order, with all project source/output/extern/search paths selecting
the fresh snapshot and directory. No predecessor checker/module binary is
substituted. Driver keeps fat LTO; intermediate profiles remain unchanged.

All commands exited zero with COMMAND_COMPLETED, clean Jobs, zero active or
terminated processes, no cleanup error or overriding finalization marker.
Root reports outer session12588 reaped with exit zero. Actual worker cumulative
CPU is 74.609375 seconds (36.96875, 13.125, 2.546875, 21.96875 per compile),
disjoint controller CPU 2.578125, wall 41.87628909992054 seconds; peak Job
private bytes 695197696 and total process count 10.

| Output | Bytes | SHA256 |
|---|---:|---|
| libnanoda_lib.rlib | 11339020 | `c0c0b10ba18adf5c20496d751cc9cbbc911677fafe64461d963dadc53a37c4a2` |
| libdmkn_module_relation.rlib | 4217412 | `10efaf57720635b0c347487194283117599ecb3be326b4c51b3c9dbcc144a4bf` |
| libdmkn_aggregate_relation.rlib | 916696 | `829d68c1a2c51138785394e19bcb35692902144d7be19f1dbfc9c9742f1952b4` |
| native_aggregate.exe | 1804800 | `7ca635aa5bb18ce1a2a360d0f5e30f5d5ebf0b2fdce818aa8ae1029c92446635` |

This is compile-only evidence, not native mathematical verification, guest
execution, certificate production, measured optimizer speedup or v5 release.

### Full native optimizer integration: source and exact selection clearance

Fresh thin root `proof_validation/lib.rs` at
`c1961d6722b8d9677b68e6bb8bf318c4b2a4383adf09f82aa3c305e90099341a`
and `proof_validation/integration/build.py` at
`78bcf7fa950d5a350f9bdc1ef0464f79309f994f2a3e30d0974f233be1372d58`
pass changed-boundary source review. Public checker module order/API and
STACK_SIZE remain unchanged. The exact 33-file proposal contains the complete
32-production-Rust closure plus controller; all source length/hash pins match.
Old module/checker/claims source identities are checked against their used maps,
not merely rehashed into a new arbitrary source selection.

Retained command inspection confirms exact checker-root/output substitution,
module-to-fresh-checker binding, claims-to-fresh-module binding, and driver-to-
both-fresh-rlibs binding. All three predecessor project dependency search paths
are replaced by one fresh artifact directory; external paths remain retained.
There are exactly four non-test compiles. Checker keeps its eight externs and
driver keeps fat LTO. One cumulative 240 CPU/240 phase-wall-second Job,
3072 MiB/six processes, 60 controller CPU/600 total wall seconds and 1 GiB
output bounds remain, with final input/snapshot checks and override marker.

Exact 13,267-byte selection
`948c505ea10547885cf316ff0ecc336df459c625fa671f185f6659ebc298e9f9`
passes review: same parsed 33-source map as inert proposal
`da8129fadd3913cf9d36fd196b259b157662065443773a78fcfea9b20346ed6e`,
only compile authorization changed to true, output and attempt absent. All
68 retained checker runtime pins independently rehash correctly; recent
unchanged shared runtime review is retained. D:\Python314 is required. Root
owns one compile-only launch; no native/test/guest/proof outcome follows yet.

### Guest-manifest overlay: source-path review only

Fresh `aggregate_guest/` manifests are reviewed at:

- root Cargo.toml:
  `1ea53d21c8b6503793b96d974eaad22dbf3856b9d0ada77a291e64ad37a9fafe`;
- checker/Cargo.toml:
  `56364af430400d805de9be09d842b70e2f3bc3de9a14ff8082b18bcbcc1ff543`;
- module/Cargo.toml:
  `50b4046fa9b0e1a83e3bc6900bd35be09e729804eb14fa33868004256c459c4d`.

Relative library paths select the reviewed fresh checker root, unchanged module
relation and exact-J claims-v2 source. External version requirements/features
and the eight checker dependencies are preserved; explicit resolver2 and guest
binary are appropriate. The root SDK dependency is intentionally nonoptional
in this guest-only overlay, not a portable native-library manifest. A future
command must select exact package/binary/target and audit actual resolution,
unit graph, feature/profile/build-script closure and new image identity. Source
review does not establish those runtime properties or portability. Existing
host API explicitly requires linking the selected v2 library; no aggregate
host manifest/build is implicitly selected by these three guest manifests.

### Actual explicit-warrant/derivation bookkeeping controls: PASS

Selector `Select-DeltaClaimControls01.ps1` was source-cleared at
`bcd410dca0116881b0be34919b3479211beb2a2545e705c9af0eb5bd9330c20d`.
Generated 8,319-byte selection
`d3a85d4401d4a100a00a475299341ac436ceddbf04aaf184ce71e0b2f764a6fb`
passed exact review: eighteen sources, 21 runtime/provenance pins, isolated
controls interpreter, only the synthetic `test_claims.py` command, 30 CPU/60
wall seconds, 512 MiB/two active processes, fresh output/attempt paths.

Root launched once. Actual RESULT
`97564d017d8cb9eb368ffbf321f4de55287b7f7ad55bbeae42882e00cd72d545`
passes independent audit with all 57 current-source/snapshot/runtime bindings
matching. Raw stderr contains all 25 reviewed test names marked `ok`, then
`Ran 25 tests` and `OK`, with no skipped or failed groups. Actual child exited 0
and reaped; Job closed with zero active/terminated processes, no cleanup errors
and no finalization-failure override. Actual inclusive Job CPU is 0.703125
seconds plus 0.359375 wrapper CPU; recorded wall is 1.8895966 seconds.

This qualifies the scoped synthetic bookkeeping controls for variant identity,
complete explicit derivation choice, exact ancestry/pruning, operation binding,
charges and failed-choice atomicity. Test-only patched owners confer no proof
authority. No native checker, real receipt verification, ordinary-source authoring
or networking occurred. `authoring.py` and API were exact snapshot context, not
runtime authoring coverage. Actual mathematical mixed-branch operation and full
v5 remain separate unfinished endpoints.

The subsequent PROOF-VALIDATION-INTEGRATION.md receives a principle-only review:
the fresh checker/module/aggregate/driver dependency chain and 32-production-file
closure are appropriate; old-project rlibs must not leak through search paths.
Preserving public crate API/stack and rebuilding downstream metadata avoids
mixing checker instances. Cargo overlays and adoption of a newly built aggregate
guest/image remain distinct obligations. No new build adapter or runtime is
cleared by that plan alone.

### Actual remaining claims controls02: independent PASS

Outer RESULT SHA-256
`a35c88435e1dcb466d3e03218b46c1cf64ca863b6d908efb17669f8f5d0a420b`
and inner RESULT
`0ea351dd244c37dd42b94c0dfb915c60602f97022a144fc2034032708d675bd1`
pass independent actual audit. All 95 source/snapshot/runtime/config bindings
match. Exactly four workers ran: one corrected differential group, actual
two-delta v2 relation, wrong exact target and invalid new proof. Their expected
exit codes are 0/0/2/2. All Jobs and direct children closed/reaped with zero
active/terminated processes, no cleanup errors and no finalization override.
Actual outer inclusive Job CPU is 4.25 seconds plus 0.359375 wrapper CPU;
recorded wall is 6.6072433 seconds. Nested costs are not added again.

The actual 215,540-byte v2 input hashes to
`7e21d092206b08a9a71231045b8152df4179ee6575cdc5e3afc704ef03c0be58`.
Its three exact member journals, single pending base assumption and census
equal retained baseline evidence: 2,364 rows, 22 bodies, 23 openings, three
edges, 29,858 JSON nodes and depth 28. Header is DMKNA002/version 2, count 3,
maximum rank 2 and seal height 1. Independent read-only SHA calculation without
loading product code reproduces its root
`a1b5e4422275e0fb811abb84234c740faf166a2624292f1d3614a51a0ab33d43`
and all six returned sibling hashes. Saved cross-language vectors hash to
`01d7c9cc45a16f520980e80672f90c0a97a69e31e344f748910df5abb24ffd0b`.

Wrong exact target refuses with `aggregate target must be an exact newly checked
delta warrant`; changed proof refuses with `CHECKER_PANIC_OR_UNRESOLVED_DEMAND`.
The corrected named/positional extraction/schema group passes all four source
cases. Earlier controls01 remains FAIL. Its fifteen successful Rust groups
and fifteen Python groups are carried, not rerun; raw prior Rust stdout SHA is
`12be9af34589be2d01515ba4e8ab7a493ee2e688472098fd40fb2f6fff42a821`.
This composes changed-boundary evidence without relabeling the failed operation.

No actual aggregate guest/image/receipt, complete optimizer native integration,
real public mixed-branch import, useful-growth or worldwide deployment outcome
is established by these scoped passes. The full v5 goal remains unfinished.

### Two parallel actual outcomes and remaining-controls exact clearance

Both root-launched operations completed and reaped; their independent actual
audits pass without treating overlapping elapsed times as additive wall time.

- Corrected refusal build RESULT
  `16858fcd231266750311919b5b4045a4a7a984115a65761bd4def606daccb4c2`:
  one selected test-only compile, 11 changed source/snapshot/output/log bindings
  match; output 2,302,976 bytes at
  `9b80bd5f0d127e23921310566326425df4160bc9a101f34682ab7bfabdadec1c`.
  Actual cost 29.96875 worker plus 1.953125 controller CPU seconds,
  37.7164956 seconds recorded wall. No test was executed by this build.
- Proof-validation RESULT
  `9855b711053e35438c7b5f8e66662e389e06d366734524297cafde46d84650e2`:
  one serde-only compile and all twelve exact named syntax groups pass;
  13 changed source/snapshot/output/log bindings match. Test executable
  1,052,160 bytes at
  `6ecb97974cd915beadd80342dec06ded129d69846412e09e057229e67e37116e`.
  Actual cost 14.046875 worker plus 1.984375 controller CPU seconds,
  20.516386 seconds recorded wall. Native proof checking was not run.

Both Jobs closed with zero active/terminated processes, no cleanup errors and
no finalization-failure override. Recent unchanged compiler/runtime audit is
retained. These are compile/syntax outcomes, not the complete checker successor,
an optimized guest measurement, or mathematical certification.

Remaining control source
`00982894c9e0ec30ad458bd5c212ddfb38a2cd13e200ee94278bfee7b2badd4a`
and `Select-ClaimsRemaining01.ps1` are source-cleared. Exact controls02 selection
`a573f8d1a6626c338fce01d3c0a2e0a9f851407249a2b9709c0620be6da97389`
and configuration
`96ec18d198efc58c576e2772570fc280a9bb22a5dab50a5ea69f308a8bd88f4c`
pass 78 binding checks, with seventeen sources and 37 unique configuration
runtime paths. They use the retained exact v2 driver, newly audited one-group
test executable, retained packet/reference and prior failed operation's exact
inner RESULT. Output/attempt paths were fresh; controls interpreter and finite
limits remain correct. Only one corrected group and three previously unreached
native calls are selected. Prior fifteen Python and fifteen Rust successes are
carried from independently audited evidence, not rerun. The controller rechecks
the prior failure and Python count; its Rust retained-count statement additionally
depends on the prior independently audited raw stdout. No remaining-control
outcome is inferred before execution.

### Explicit variant/whole-derivation public source clearance

The complete fresh `delta_claims/` implementation, API/theory and 25 synthetic
controls are independently source-cleared at these reviewed pins:

| File | SHA-256 |
|---|---|
| `__init__.py` | `dc919d97068cea9d267b07368d238e4ce7a5689d20439ac5e6d69f7f76bb4987` |
| `receiver.py` | `7731f712902b5c5e0869a51c913b335428309760df604768293f7ab58c301bfd` |
| `claims.py` | `c880964241e5b0f492ab332b2c694896b3b6efdc638e014b25148bd6410e6564` |
| `imports.py` | `216f3ce48543ff4638c7112aa16d6dc430f7bc9a04f6927a7d036b81ddee137f` |
| `authoring.py` | `cc62ebd697d8137f021dbf79feb4e39e41639a8c5864c041da40838469bbc290` |
| `test_claims.py` | `f719bfcaf0e658dac8eeb76b7cce8b365a8da5567563cd37b812af062881860c` |
| `API.md` | `abf2fc482658aad9005fc248aa3fb95540d2c69620f9d9c6b3f352a7d5dd06b2` |

Receiver graph membership and exact lookup retain every checked J, allowing
different-rank same-M warrants without changing mathematical checking or exact
rank/ancestry requirements. Semantic declarations/bodies remain M-keyed. New
direct imports require an explicit immutable established J per M; no duplicate
semantic declaration is installed and no old child J/witness is rewritten.

Same-J ambiguity is now operable: `use_handle(...,resolutions=...)` requires
exactly one existing/incoming directive for each actual complete-representation
conflict, accepts no arbitrary payload or unused directive, and handles repeated
packets through the same decision path. Each incoming whole record is bound to
actual same-verifier live facts and payload identity. All demanded chosen parents
exist. The session commits prepared state maps only after its final live checks;
failed admission/choice leaves old maps unchanged but retains submission charges.
All packet alternatives remain retained/charged. Onward emission follows chosen
exact-J ancestry and prunes unreachable stored records without unioning edges.

Prepared source bindings include every chosen graph record plus a monotone
representation revision, preventing an ancestor-only A-to-B-to-A switch from
reviving an old operation even with unchanged direct semantic imports. This is
a conservative whole-session binding rather than minimal reachable-only binding.
Actual returned packets remain untrusted and require fresh independent admission.

All 25 controls are explicitly fabricated bookkeeping fixtures with patched
test-only owners: zero receipts, kernel proofs or mathematical admissions.
Source clearance does not qualify runtime import closure, native mixed-branch
admission, authoring integration, aggregate-receipt imports or full v5 release.

### Two finite follow-on selections cleared, not yet outcomes

The proof-validation controller at
`91e25c3a3244a106c01ce18da63b07a163b0d07e53eddcf5376b399ee22a9ca1`
is source-cleared: only serde/serde_json test compilation and twelve named
syntax groups, one cumulative 120 CPU/120 wall-second Job, 1536 MiB/six active
processes, 60 controller CPU/300 total wall seconds and 256 MiB output. No
nanoda/module/risc0 extern or native mathematical checking is selected.
Exact selection
`ff93202ecc32a3b84449d74d0423535cc1c540bec88b7de7c3e0d6777cda0e02`
has four matching source pins and fresh output/attempt paths.

The separate corrected-refusal source `586ca944cd74e7b4ed8a3a57bbe8d9afe52397f28dd3c452b3eb918767a42d5f`
contains one group with four cases: named/positional malformed body records
must fail extraction; their empty-body counterparts must reach the later schema
refusal. Both routes' first outcomes and cumulative census are compared.
Its thin builder `4b2064ceb6a5c1fb7615bee3a7d4ab9b924d844716c13782c768fc310323e1f3`
selects only the retained test compile command, changing its root/output to the
one new group. There is no production rebuild or test execution in this build.
Exact selection
`d97ae5137559c800c7e4537c4360be2a728c5f5a01bef9bbf51aff0654027e9f`
has four matching source pins and fresh output/attempt paths. Both operations
require the independently rehashed `D:\Python314` executable/DLL; recent
unchanged retained-runtime checks are reused. Root owns parallel launches and
subsequent outcome adoption.

### Proof-validation allocation refinement: source clearance

The fresh `software/v5/modules/native/proof_validation/` triple is independently
source-cleared at these exact SHA-256 pins:

- `module_correspondence.rs`:
  `ee4f33a9d4896bd59b2456cb1712d13010d0838b8ba0be34c89c10ebba18bdf8`.
- `correspondence_controls.rs`:
  `2162b252894f6653dcaa31f36454c1bb07763d1155d830a7a5a46cff4e9b6d35`.
- `control_root.rs`:
  `74f29dd1ed1a034ad57ec833391dd36a38199429700151a9a1afa3fb6a3d475a`.

Independently removing only the two new private validators and test-module
declaration, then reversing the sole discarded-proof call replacement,
reconstructs the frozen original exact SHA-256
`f37c855666480553ee9b95f59dc3ba7ad19316e8e707aacd47fecfa29f1d12e2`.
Thus whole-inventory construction, original expression/level/reference/visit
methods and committed type/body comparisons are unchanged. The fresh validators
preserve every tag's scalar/shape check and left-to-right recursive call order,
including constant levels before reference, projection reference before index,
visit before row lookup, and exact work 250,000/depth 192 limits.

The source refinement argument in PROOF-VALIDATION-PLAN.md is sound under its
stated observation model: equal success/first semantic refusal and work-state
prefix by ordered traversal induction, excluding allocation, OOM, stack and
timing behavior. Original reference allocation remains; native proof checking
is not removed. All twelve synthetic differential/structural groups were read;
no source blocker found. They are not mathematical admission tests. No actual
compiler/control, CPU saving or guest affordability follows from source review.
The separately drafted controller and exact root runtime selection still need
their own review.

### Actual claims controls01 failure: expectation defect, not a hidden pass

The selected controls01 operation is terminal FAIL, independently audited.
Outer RESULT SHA-256:
`ee38afa9ce5eaa56a183cb24c03d3c3f30c9ca938379d0b878fbbf4fd25479a1`;
inner RESULT:
`3ca0555fc9c9f6f71061457051768f949d3bf4f114e57f65f1127ab3e3f5f651`.
All 94 source/snapshot/runtime/config bindings match. All fifteen inert Python
groups pass, and fifteen of sixteen Rust groups pass. The sole failed group is
`public_value_entry_preserves_early_relation_refusals_and_census`, at its final
hardcoded expected diagnostic. No actual native relation worker was reached.

The first object fixture includes `bodies:[{}]`. The unchanged input extractor
requires each body record's `universes`, `digest` and `expression`, hence returns
`exact input record fields` before `check_bound` reaches `relation schema/limits`.
Both old and new paths returned the same former error; their prior equality and
census assertions passed. The expected latter error is the test defect. The
second positional iteration was never reached, so its result cannot be inferred
as an actual pass. No production acceptance discrepancy was observed.

The single Rust worker exited 101 and closed normally; outer controller exited
1 and closed, with zero active/terminated processes and no cleanup errors.
Actual outer inclusive Job CPU is 4.125 seconds plus 0.375 wrapper CPU, and
recorded wall is 5.794745 seconds. The inner 0.21875 CPU is already included.
No overriding finalization failure exists. Original used source/evidence stays
frozen. Root plans a fresh minimal corrected one-group control and the three
unreached native calls, not a production rebuild or rerun of thirty passing
Python/Rust groups. Fresh source and exact selection remain separate reviews.

### Actual claims build02 and exact controls01 clearance

Independent actual compile audit passes. RESULT SHA-256 is
`06fd5deac8e66853daa72e35b819fa4766943e708264c98166a67ff7c8111ba2`.
All 230 audited bindings match: 12 current sources plus 12 copied sources,
three outputs, six command logs, four retained artifacts, 174 recipe runtime
pins and 19 retained predecessor snapshot files. The three selected commands
compile only the aggregate relation, test executable and driver. Both final
links use fat LTO; no module/checker recompile occurred. All commands exited 0;
the cumulative Job closed with zero active/terminated processes and no cleanup
errors. Selected exact owned telemetry cleanup is recorded. No overriding
finalization-failure marker exists. Root reports its outer invocation reaped.

Actual costs are 61.1875 inclusive worker CPU seconds plus 2.359375 disjoint
controller CPU seconds, with 74.8305412 seconds recorded wall time. Report/exit
tail remains excluded as declared. Executable pins:

- native, 1,797,632 bytes:
  `004cf6ed58610f30d13738fc4497f97741703b2529c71f51da4fce29a4f8017c`.
- tests, 2,471,424 bytes:
  `a01a94a544b095ce5cfeb4ff7d6582e6f1babfa51cd434c7a5c313921782521c`.
- relation rlib, 916,456 bytes:
  `06c36d6f1667e919914d619094fbe226bf8c5bdee714557c0f1c062d825a8ed1`.

Exact controls01 selection
`e11f32038cf3f727e62a0a89189ecdb9b885a4592f450ded5616c3f196610367`
and configuration
`c35f7ed1c52d025f71f0d238811f1cc26356ff3da92a5e3581977a5dc2a90cf9`
are independently cleared for root's four-worker control selection. All 77
checked source/runtime/config bindings match; seventeen sources and all 37
configuration runtime paths are covered, with no duplicate runtime paths.
Native/test path, length and hash fields equal audited build02 outputs. Exact
retained packet/reference and isolated controls interpreter are preserved;
output and attempt paths were absent at review. No control success, guest,
cryptographic aggregate receipt or release result follows from this clearance.

### Whole-derivation choice for identical exact journals: source theorem

The conservative draft session refuses different representations of the same
exact J. That is safe but is not universal honest-branch merge completeness.
Root asks whether explicit complete-representation choice repairs this. Yes,
under the existing live admission and exact-rank premises; no checker weakening
or child-witness substitution is required.

Let a representation of J be either (a) a genuine resolved receipt for J or
(b) the complete unchanged native witness W whose checked conclusion is J and
whose complete exact parent tuple is P(W). Every retained representation must
be bound to an actual still-live admitting handle and its exact payload bytes.
Choose one representation r(J) for each reachable J, not an arbitrary union
or subset of its edges. For a native representation, retain every parent in
P(W); for a receipt representation, retain no unsealed proof ancestry. Require
all demanded choices/material, fixed image/foundation/policy, and original
native rank equation. Every native parent has smaller rank, so a finite chosen
graph terminates. Receipt nodes are independently established base cases.
Induction on rank establishes every selected J and hence every selected target.

An old child names its exact parent J, not the complete derivation of that J.
Replacing the representation establishing that identical J therefore changes
no old child premise, witness byte, rank, or semantic import. Replacing it with
another J sharing only ModuleID is a different operation and remains forbidden.
Unreachable representations and their unused edges can be omitted from the
onward packet; this is pruning proof witnesses, not revoking any mathematics or
discarding the resource costs of having acquired/checked them. Shared parents
still use one complete selected representation; no edge splicing is allowed.

Operability conditions: distinguish representation identity from J and from M;
enumerate ambiguous representations and demand an explicit choice; cap and
charge all submitted alternatives before deduplication; bind the operation to
the chosen reachable graph and live evidence; reject missing choices/material,
mutated witnesses and expired authority; emit unchanged witnesses in rank order.
Proof-form tags must be part of representation identity. A digest or copied
inventory alone grants no authority. Choice can be fixed for a session/operation
without requiring a global canonical proof. Heuristic cost preference may guide
the caller, but mathematical acceptance does not depend on that preference.

Aggregate target freshness is an additional protocol condition: if a target
must be a newly checked delta, choosing its receipt representation cannot satisfy
that rule even though the same J is valid. Require a native representation for
that target or issue a typed refusal. Fresh public authoring avoids this issue
by applying choices only to already established ancestry and checking an entirely
new child separately. Source theorem only: no extended implementation or test
is qualified here.

### Claims build02 delta selection and prospective controls selection

Exact claims-build02 selector SHA-256
`d84d01613ca22939521c7387911271e4151bfbefa0150bd7e5832fb5fc9d6f08`
is independently cleared for root's three-thin-compile selection only. Its
schema, compile-only flag and twelve-source map equal cleared build01; only
the fresh operation name changes. Both output and attempt paths were absent.
The retained 209-binding review is not rerun without a changed boundary.
Required interpreter `D:\Python314\python.exe` independently rehashes to
`03168c01b7b7491423350e82c26fee71f35b43694d1319d3c668bda6903a0c38`,
and `python314.dll` to
`fde89cdb5c2d08ae65de7ef4abca1876c93ba3796002f5ac0bf7e4d4f5a94da0`.

Build01's actual wrong-interpreter failure remains preserved separately in
CLAIMS-BUILD01-PREWORKER-FAILURE.md. `PINNED_PYTHON` precedes output creation,
Job creation and compiler invocation. Root reported exit 1 and 0.8308567 seconds
wall; CPU was uninstrumented, not zero. This is an invocation failure, not
a compiler/source failure. The failed selection is not retried or relabeled.

Prospective `Select-ClaimsControls01.ps1` source review finds no blocker.
Its retained fourteen-source map loses three old aggregate files and gains six
fresh aggregate_claims files: seventeen sources total, covering fifteen imported
product modules, the executing native controller and the outer runner. It
replaces old snapshot and binary pins; new actual binaries must match build02's
passing output records, with no finalization-failure override. It retains the
packet, exact cross-language reference, controls interpreter and outer limits
(240 CPU seconds, 600 wall seconds, 4096 MiB, four active processes). It creates
fresh selection/configuration files only. Exact generated files and actual
results still require independent review; no test/guest/proof result follows.

### Exact-warrant v2 Rust and Python source review

Read all fresh `aggregate_claims` Rust/Python sources and root's
AGGREGATE-V2-PREPARATION.md. No source-level correctness/binding blocker found.
The graph keys, parent edges and targets are full184B journals under fixed I/F/P;
all exact pending claims remain unique and all actual witness conclusions still
come only from the unchanged module relation. Full-journal byte ordering defines
Merkle leaves; both languages agree on V2 magic/version/domains, count/index/level
binding and deterministic odd padding. Member budgets count variants. Missing
exact parent variants cannot be replaced by same-ModuleID evidence. Every target
must be a fresh checked delta and all selected graph material must be reached.

Python's early target-equals-frontier refusal rejects an impossible successful
Rust input: inserting the same exact J as a new delta would itself duplicate an
existing node, while merely naming that frontier fails the fresh-delta target
rule. Repeated semantic ModuleIDs with unequal J are accepted structurally.
Helpers remain inert; they neither predict kernel success nor manufacture receipt
authority. Legacy packet conversion is lazy but still requires the eager delta
package import closure whenever called. Core four helpers require eight product
files total: aggregate_claims four plus admission init/bindings and modules
init/codec. Legacy conversion adds delta init/packet/receiver, admission/verifier
and production init/producer; selecting only packet.py is insufficient.

Reviewed Rust pins (all under `software/v5/aggregate_claims`):

| File | SHA-256 |
|---|---|
| lib.rs |350d08f5afdd3dbb53277547dd9e3fc5d93dbb138b99790481fcc2a6fca53c71|
| header.rs |e4a3426b66506559a8ddb8eb9d06195af3d14676199e6f5a9251b7ff3ff550e1|
| membership.rs |f3671d5305407f11109c5b30ea1f173216c475b2ddc0ba485a4097a266df22ba|
| wire.rs |b3aa350bc0883a5a958ec67d856fb82183c65c9ff56ca9992f7d8e039c3859d8|
| relation.rs |698e0e1bfacdad37fe1720881b2034083b357a2fbeef7b233d83e2f7c1eb6a49|
| tests.rs |55f118ac7cd48c4c6c4ccd8139d8ae47f6eb7b8fa1484b91e917aa2a6fcefbdb|
| graph_controls.rs |5eb665a22ee1ce7edd2160e6ba728a83c11f4aeb512a82bb52c6dab6fef43c62|
| Cargo.toml |1e32f4dc5d43f55f0a819acd59d674b708cad9ef94c94e72c786d3470edbca1c|

Reviewed Python pins:

| File | SHA-256 |
|---|---|
| __init__.py |c9440183d92c887c4f6bac36f4bd51b7cf935ddf0f3f155aac8b8f1d48ad6540|
| bindings.py |a6777395353f0421111cc2a2a0b06208dfbe4d60549899a70a42cda0bda9e543|
| input.py |d40b611e288fd73a060df021809e403f80b1e6c16ca8b81ff2fd528d1f2fe61f|
| admission_binding.py |2746704a28c180df0f549864a7c96b138110f0f6ff57e0de4aae66f198e059f3|

The guest entry is unchanged source
`d7b9b93843b683215e0556e585bc5ea241c672fe4c2a89cc07afa41afb81acad`:
it verifies every returned exact assumption before committing the header.
The parse-once census is path-reused at88e9796b, not copied/changed. Six new
profile/wire/commitment/census groups and five graph groups are source-reviewed,
explicitly synthetic structure rather than mathematical receipt evidence. The
five earlier parse-once differential groups remain unrun and initially unlinked
by this lib; root was advised to path-reuse them in this same fresh test binary
rather than compile another successor later. This is a coverage planning choice,
not a production defect. No build, control, guest, aggregate receipt or public
variant-aware import outcome is established by this review.

Root chose the single-binary16-group option. Revised lib
`91fd74bc5ba9b78b017cb3d20d6a3cedaaaac294027300e87487097e23d6be25`
adds only test-gated paths to old reference census and the five unchanged
parse-once differential groups. Production code is unchanged. Fresh build
controller `5d38b02e640b988eb943004fd0f814f84b8e798db4ed112dd77be13cb1b514b6`
is source-cleared against the earlier reviewed thin builder. Its12-source
snapshot contains8fresh files plus frozen native driver, old census, parse-once
census and five-control source. Those cover all Rust source-relative paths.
It compiles only aggregate rlib/tests/driver, preserving unchanged module/checker
rlibs and all old runtime/envelope/finalization checks. Both final links use fat
LTO; the driver uses the newly produced aggregate rlib. Exact root selection
and actual outcomes remain separate; no old nine-group suite is selected.

Exact root claims-build01 selection
`f7a0dc9891a79817fab9bc318e2eaeeaf091413bc192d0dbb664d0ca118e236a`
is independently cleared:209actual bindings match (12selected sources,
19retained snapshot files,174recipe runtime pins,4retained artifacts), with
fresh output/attempt absent at review. Three compile commands remain the sole
selected work; no automatic test/guest/proof follows.

Root control sources
`binding_controls.py` at
`1f41d83c3a7199d8cc189e9a44b1a17be2daecafd8f72481264f1d892aa45e5d`
and `native_controls.py` at
`b429d37282e9a1fd8b823b6fe4785ecc436e9bed5db5bffaae27811e404712bb`
are source-cleared. The pure
fifteen-group fixture explicitly calls its altered ranks synthetic; its v2
header/membership/wire/status checks confer no proof authority. Actual controls
require sixteen new Rust groups and exactly four bounded workers: unit binary,
actual two-delta v2 relation, absent exact rank-variant target, invalid new proof.
Positive exact member journals/pending assumptions/census/edge counts are compared
to retained controls02, while newly changed commitments/paths are independently
recomputed in Python. No old binary, author, network, receipt or guest call runs.
The control explicitly pins all fifteen actually loaded product modules, including
the eager delta/receiver/verifier/production closure. Each worker is30CPU/60wall
at most, total reservation120CPU plus60ownerCPU/600wall; final files/config/runtime/
reference/source checks and overriding finalization failure remain enforced.
Actual compiled binary pins and exact control configuration are not yet reviewed.

### Central merge defect: semantic module identity is not an exact warrant claim

**Confirmed by source, without execution.** The current aggregate relation is
soundly restrictive but is not closed under merging compatible honest proof
branches. Root holds the parse-once build and any aggregate guest funding while
selecting a correction. No current source/evidence is rewritten by this review.

In `modules/receipt/src/commitments.rs::summarize`, the only ModuleSpec fields
are schema, foundation, policy and groups. The summary contains foundation,
policy, group count and group root. `journal.rs::summary` omits image and rank;
the module digest hashes that summary. Theorem descriptors have a null
`value_hash`, enforced in `native/checker/src/module_correspondence.rs`; the
local proof syntax is independently checked but explicitly excluded from
ModuleSpecID. `receipt/src/relation.rs` takes exact parent journals separately
and computes rank as zero or one plus the largest parent rank. Therefore neither
rank nor the proof-only parent choices are determined by ModuleID.

A small valid mathematical scenario under the adopted foundation is:

- H exports theorem h of type `forall P : Prop, P -> P`, proved by `fun P p => p`.
  Its exact warrant J(H,0) has rank zero.
- M exports theorem m of the same type, with its own distinct relative name.
  Proof `fun P p => p` gives J(M,0). Alternatively proof `H.h` under the exact
  H premise gives J(M,1). M's local descriptors and ModuleID are identical:
  neither its exported type nor any transparent body mentions H.
- X exports x of that type, using M.m under J(M,0), and has rank one.
  Y exports y, using M.m under J(M,1), and has rank two. Distinct relative names
  keep H/M/X/Y module identities distinct, apart from the two intended M claims.

This construction does not rely on unused imports: each imported theorem is
actually used as the local proof. It is a source/model counterexample, not a
claim that these concrete serialized rows or receipts were executed/generated.
Assuming genuine receipts for the two M claims, the intended batch has two
frontier claim nodes J(M,0),J(M,1), two fresh deltas X,Y and two distinct targets.
Every exact parent exists, every rank edge decreases, all four claim nodes are
in target closure, and their mathematical interfaces are compatible. Equally,
H,M0,M1,X,Y can all be fresh checked deltas, with X,Y as targets. Nevertheless:

1. `aggregate_parse_once/relation.rs::Graph` and its predecessor key nodes by
   ModuleID, so the second M variant is rejected as a duplicate/conflict.
2. Delta parent lookup, reached-node accounting and target keys also use that
   semantic identity rather than the exact parent journal.
3. Rust `membership::leaves` and Python `bindings::_leaves` require strictly
   increasing ModuleIDs; neither can commit both valid M variants.
4. Python `input::encode` rejects duplicate frontier ModuleIDs. Targets are
   presently only32B ModuleIDs and cannot distinguish fresh variants.

This is not a false-acceptance attack. One can certify X and Y separately and
then use their distinct module IDs, or reconstruct/recheck a branch against a
different valid M claim. But these impose new certification or rechecking costs
and invalidate an unrestricted efficient-merge claim. It is central to a large,
independently evolving network, not a political/provenance corner case.

**Recommended invariant:** separate semantic identity M from exact admissible
claim identity W = (adopted relation image, exact184B journal). Under this fixed
profile the journal already contains the image; full bytes or a domain-separated
digest with exact-byte equality on lookup suffice. W is an existential warrant
claim, not proof provenance: two different proofs giving the same exact journal
need not have different W. Semantic descriptors, bodies and discovery remain
shared by M. A bounded aggregate graph keys nodes and parent edges by W, retains
the exact journal/rank checks and counts each selected variant against its finite
member/edge/input budget. No global canonical/minimal rank or global history is
needed, and no semantic equality alone may mint an exact warrant.

Use a specified total order such as (ModuleID,exactJournalBytes) for commitment
leaves, and exact claim targets (or an explicitly unambiguous selected-node
reference). Exact duplicate claims may be rejected or coalesced by an explicit
rule; do not silently union two derivation edge sets for one existential claim.
Each single-module checker invocation may still select only one exact warrant
per imported ModuleID, as its current namespace permits. Different invocations
in one batch may select different valid variants. Closure and well-foundedness
are over claim nodes; their semantic quotient need not be a DAG.

The assurance induction survives unchanged: frontier claims follow genuine
I/A receipt verification and exact membership; every delta discharges each exact
established parent with a strictly lower rank and checks all new declarations;
the aggregate commits the exact resulting claims. Claims with equal M but unequal
rank cannot discharge each other's obligations. A rank variant cannot be created
merely by editing J, lowering ranks or projecting an interface. New aggregate
relation/image and matching encoders/commitments/controls require a separately
selected successor; the retained controls02 baseline remains valid only for its
original unique-ModuleID subset. No source-only argument establishes throughput.

Root's adopted design choice refines the recommendation to full184B-journal
graph keys, edges and targets, and strict lexicographic full-journal member order.
That order is canonical despite little-endian rank not sorting numerically; no
ordering proof needs numeric rank order. New header/input magic, versions and
Merkle domains must be consistent in all implementations. Exact duplicate-claim
refusal remains safe; preparation must select one derivation and honor a target's
required fresh-delta role rather than silently replacing it by a frontier.

The public-boundary audit confirms this issue is not isolated to the aggregate:
`delta/receiver.py` already keys its graph by journal bytes but additionally
rejects repeated ModuleIDs at frontier and delta insertion; `describe_member`
selects by ModuleID. `delta/authoring02.py::use_handle` builds its inventories,
pending nodes and retained `_nodes` by ModuleID and rejects alternate journal/
payload/parent tuples even across different accepted packets. Legacy
`authoring/imports.py` selects one receipt/journal per ModuleID; the conditional
environment likewise keeps one exact claim per ModuleID. The last two can remain
valid local-operation selection policies, but collective storage and batch
composition must not confuse them with a global uniqueness theorem. The new
public aggregate receiver/import interface needs a deliberate warrant selector,
not a silent change to these frozen APIs. Existing ReceiptVerifier handle identity
itself can distinguish multiple exact claims for one semantic module.

### Aggregate execution seam: independent plan review

Read the complete AGGREGATE-EXECUTION-SEAM.md and relevant retained SDK/session,
module-host and receipt-verifier sources. The planned one-execution capsule route
is coherent: full real I/A application verification precedes assumptions; actual
session claim must equal the exact resolved A/header claim; complete
`session.segments()` merges final output; actual assumption order is bound
bijectively to preverified exact claims. A capsule remains an untrusted proving
witness and never gives member admission. Fresh v2 relation/image/header binding
must follow the separate claim-variant redesign; no host build/guest is cleared.

The host author's explicit create-new bounded segment callback is a valid
single-execution replacement for ambient temporary files: retained SDK `run()`
delegates to `run_with_callback` with its own file-segment callback. The caller
must still account for both retained segment files and final capsule bytes, and
preserve partial files as diagnostics rather than advertise crash resumption.

SDK `Session::claim` drops proven assumptions and specially excludes a pending
Keccak-root assumption. My initial suggestion to check `session.pending_keccaks`
directly was not API-valid: the field is `pub(crate)`. Independently reviewed the
author's correction. SyscallTable initializes that list empty; its only append
is in `SysKeccak::keccak_prove` when no coprocessor callback is installed. A
supported `CoprocessorCallback` whose `prove_keccak` always returns an error
therefore excludes a successful unsupported Keccak request without producing any
proof or changing the SDK. It fails earlier than a post-run emptiness check, so
resource/diagnostic equality is not claimed. Preserve the exact actual-assumption
bijection and MMR/PoVW refusals independently. No native/guest timing prediction
follows from these source-level findings.

Completed host source review at
`7548e5b2092f3ece5d9ef93cef6c7ccd7d5e01ad123053f28e836558617857ca`
and API documentation
`d53d24a0e111b01c7016a258b9cb23a99cda3d4911c6ce7a57ad35f1de310dfa`:
no source-level acceptance blocker found. Public SDK callback/reexports are
present. The host checks actual ELF=A, exact native-derived header, genuine
preverified I/A receipts, one actual execution, exact resolved session claim,
all actual assumptions and complete consecutive segments. Its callback keeps
at most64MiB total raw segment files, final capsule64MiB and diagnostic8MiB,
not a hard OS quota. New paths are create-new with normalized absolute no-reparse
ancestry and fsync; partial files survive failure. Optional sampling saturates
nonfatally. No callback receipt, saved report or segment can grant admission.
Success requires exact final receipt verification separately. Resource ceilings,
source/ELF correspondence, trusted-owner isolation and executable selection still
belong to root; no actual host build, aggregate image or execution is cleared.

Root's inert `aggregate/admission_binding.py`
`7d60da8bc7b22fe65789f903485f837ee52f4f36c2f75f9d98d09198c39f1b41`
also matches the host's exact six-field verify contract: bounded strict parsing,
selected image/exact header, actual receipt bytes/hash and no extra fields.
It intentionally can accept fabricated success-shaped JSON and grants no
authority; the future owner must bind this to the same actual supervised verified
call and selected member opening. No persisted report cache is an alternative.

### Parse-once thin build and controls source clearance

Exact compile selection
`28625e62a7fc8cb6640c0a5cc52194e0e69360f437998650b6e8f95c25a33a6a`
and controller
`7299aacdfbba7f24e79d24a64e597ba8d438349d9a327528e51c67321c950164`
are independently source-cleared. Read the complete selected controller, retained
four-command recipe and reused phase/Job implementation. The selected successor
executes exactly three commands: changed aggregate rlib, test binary, native
driver. It reuses the successful unchanged module/checker rlibs; restores fat LTO
on both final links; changes only the selected source/output/aggregate-extern
bindings. Shared support and old snapshot stay unchanged. All205 checked
canonical/snapshot/runtime pins match and the selected output did not yet exist.
Worker limits remain one cumulative240CPU/240wall phase,3072MiB,6active processes;
controller60CPU/total600wall and1GiB output remain distinct. Owned exact VCTIP
cleanup is inherited; it is not permission to terminate arbitrary processes.

Controls source
`4a95fee974a069a1f5d4f3f9fe19eddf521260e4a979086bf14e1e8ed3811274`
is independently source-cleared, not executed. It loads only stdlib and pinned
adopted supervisor modules, avoiding the prior eager v5 import-closure error.
Actual executing `__file__` remains a mandatory runtime pin; removing its canonical
source-path equality permits the selected immutable controller snapshot without
weakening that byte binding. Exactly one filtered test call must show5new passes
and9filtered old groups; two new native calls must match retained controls02
positive and invalid-proof stdout byte-for-byte. Thus3workers/at most90CPU,
60ownerCPU/600wall; no old executable, proof, receipt or network call. Inputs,
copied fixtures, references, selected runtime and supervisor are rechecked at
finalization. Exact new binary/config selection still requires independent
review after build. No measured speedup or guest/prover affordability is inferred.

### Retained-network continuation01 actual PASS

Outer RESULT SHA
`70898a9f36f2540697d2008ee2ce3862e02f5e535c91d251b95e2e6d5aeca995`;
inner RESULT SHA
`5f758b0171f1ae9048f0c9660d00996eafce06b93fbff94436bd8f9528918f09`.
All229actual bindings independently match:58canonical sources,50outer pins,
78actual-owner runtime pins,28Node canonical/snapshot pins and15inputs. Retained
reader1 result/packet DB/module DB hashes remain unchanged; no SQLite sidecars
exist. A separate read-only immutable SQL audit compares actual packet, complete
group and complete body rows across preserved reader1 and all three new stores:
transient origin, replica and new reader2 each retain exactly the same1packet,
13groups and11bodies. No old source, custody or acceptance state was repaired.

The new reader starts with no target IDs/HTTP contacts and actually locates the
transient origin through the formal key. The first route's peer equals the
origin's actual freshly generated peer ID. The origin is then stopped/reaped
and its HTTP/custody closed before any acquisition. Its subsequent descriptor
returns the real typed TCP_CONNECT_UNAVAILABLE, with no authenticated-peer
claim and the full reserved4096B charged. The same live child/channel then
performs its second original-ticket route, returning the real replica plus the
stale origin. It skips only its already attempted public result and adopts the
actual replica's authenticated descriptor. That second query has one refused
connection/query error and is honestly INCOMPLETE_QUERY_ERRORS, yet supplies
usable hints. Replica publication in this particular run had1localwrite and
noqueryerrors; the newly allowed zero-write publication branch was not exercised.

Reader2 searches the actual replica index, selects its first actual returned
formal candidate, acquires exact packet662,480B/54c7dac7, verifies the genuine
base receipt223,594B/850c33b2, and checks both native deltas. The three actual
checker processes exit0/clean and return exact prior journals/inputs (base
rank0,delta4adbc049 rank1,target52c564f8 rank2). Receipt is fully resolved under
fixed I/foundation/policy. Native inputs remain88b71b82 andea66d3ef. It then
reconstructs the ordinary authoring context using its newly admitted live handle,
received groups/bodies and independently adopted foundation:16declarations,
13groups,64,003frontend bytes,68,707selected input bytes,2,404counted expression
visits and0frontend theorem-ancestor proof bytes. This is an untrusted authoring
context, not a newly authored theorem. The complete checking packet still retains
both unsealed proof witnesses; this endpoint does not eliminate arbitrary
unsealed ancestry or produce an aggregate certificate.

Origin HTTP handled0requests; replica handled5, nofailures. Actual reader stderr
reports1descriptor-unavailable event,5commands,0active transport connections,
noexhaustion. All4Node lifetimes exit0/closed, no channel/forced-stop failure;
all role pre/post pins agree and runtime inventories each retain5896files/
130,118,221B. All mathematical owners close with0livehandles. Both route
allowances and2descriptor requests remain charged (512events/8peer slots;
4638descriptor reply bytes). Original location deadline still had128685ms and
acquisition407408ms at their saved live reports; no new grant/session was minted.

Overall exit0/reaped/Jobclosed,12total/0active/0terminated processes, no cleanup
errors/finalization override;peak464,642,048B. Inclusive outer CPU93.0 plus
separate wrapper1.0,103.9921983wall. Inner controller84.5 and checker0.109375 are
included in outer and must not be added again. This is composition of actual02's
retained reader1 prefix and one fresh continuation, explicitly not one
uninterrupted operation. Actual02 remains FAIL and all prior costs remain.
The evidence closes this same-host retained-custody/stale-provider suffix, not
independent-host deployment, arbitrary semantic search, useful-growth economics,
aggregate certification or full v5. No passing prefix needs repetition.

### Parse-once aggregate successor: exact minimal source change cleared

Fully read four new files under `software/v5/aggregate_parse_once`:

- `lib.rs`: `6dfb8c28220d074a41492274bcb90fc337b78b354b3b5fdf56ad5d103d43a315`.
- `census.rs`: `88e9796bbb5493187f541d40e7c777afa8bfd4059929a9a2a1f118cfae815b04`.
- `relation.rs`: `5f3733fec79c7ed68d5476b8e804dc7c303aea097b7fa6b92eb98e03d1be2103`.
- `parse_once_controls.rs`:
  `635b9c234e66c6931838dd131510c7c9d4a548acd965f9b0912f1100f1512c6e`.

Independent line comparison against frozen source confirms only the intended
production changes: census returns its existing strictly parsed Value after
identical checks; relation moves that Value into the unchanged public
module_relation::check, preserving the second canonical_size traversal. Graph,
headers, exact pending claims, member commitments, limits and EOF are unchanged.
No public unchecked parse token or alternate checker is introduced. The earlier
call-sequence acceptance argument applies; resource behavior and speedup are
not experimentally established by source review.

Unchanged header/membership/wire and original tests are path-reused. Paths resolve
to the selected frozen aggregate directory; old test calls tolerate charge's
changed return type because they discard success values. Five new differential
test groups compare the frozen census against the returned-Value census,
including successful exact Values, raw duplicate/numeric/UTF8/trailing errors,
named/positional shape, depth, cumulative limits/overflow, and exact failed-prefix
counter state. The public Value entry's early relation refusal is compared too.
Real mathematics is reserved for the separately selected unchanged packet.

Root should select only the five changed-boundary test groups and compare a new
native result against retained controls02 vectors; there is no need to rerun the
old positive binary or its nine passing groups. New builds must bind all reused
paths and the actual module rlib; a future guest still needs a new image adoption.
No compile/test/guest/proof was launched by this review. Exact build/control
envelopes and actual outcomes remain separate root selections.

### Controls02 actual PASS and retained-network continuation exact clearance

Actual controls02 outer RESULT SHA
`492129c6ac5bd23868139125c37756d6ba4165dd4e211636e9d9eff20f37406b`;
inner RESULT SHA
`af619d070f7132de416cf422f8daa084e0b0d1a47bdd22a728aa9bfe1ff57125`.
All70actual source/runtime bindings match. Exactly five workers ran: nine unit
groups pass; actual two-delta conditional aggregate succeeds; missing premise,
wrong rank and invalid proof each refuse at exit2 with exact expected reason.
The invalid proof stderr contains the real checker `tc.rs:945` def_eq assertion,
not an injected expected flag. Every worker is reaped/Job closed, zero active/
terminated, no cleanup errors, no forced termination; no finalization override.

Independent read-only frame decoding and JSON census confirm input215,388B/
`cec1e5fc3e211bd367a9171c2a398e2a1218e627f96d28848d60c9366746c808`;
2,364rows,22bodies,23openings,3parent edges,29,858JSON Values,maxdepth28. The
missing-premise frame is exactly the original second witness only; wrong-rank
changes only second rank2 to3 while preserving the first; invalid proof changes
first theorem value1200 to770 with the second witness unchanged. All three
returned member journals are byte-identical to earlier actual base receipt and
native delta conclusions (ranks0,1,2), with the exact pending base journal.

Independently recomputed the three sorted member leaves, duplicate-last odd
padding, both tree levels and all six opening siblings using .NET SHA-256,
without running product/checker code. The root is
`3ccdf4aad4a9d009be2d644bca03e5b5b889d43b4dbebafe6e8aeeeba897de04`.
The exact192Bheader has DMKNA001/v1, fixedI/foundation/policy,3members,maxrank2,
sealheight1 and explicitly synthetic A=`07000000` repeated8. It is structural
and conditional evidence, not an adopted aggregate image, receipt or authority.

Inclusive outer Job4.03125CPU plus disjoint wrapper0.296875CPU,6.7812959wall,
12total/0active/0terminated processes,peak163,540,992B. Inner owner3.421875 and
worker CPU (0.15625,0.046875,0.015625,0.046875,0.03125) are included in the outer
Job and not additive to it. Original controls01 import failure remains charged.

Fresh retained-network continuation source was revised *before use* to
`39aae5225fb97cbc9fea6095dc280543e5e0ffe906192642dec5cb7fef5e9d5d`.
The revised publication gate correctly drops any global minimum-write condition.
It permits coherent NO_PROVIDER_RECORD_WRITE, partial QUERY_ERRORS, or only
the exact retained local query-cap/operation-timeout texts, while the original
process/channel/deadline remain live. Arbitrary failures remain terminal. No
write count is placement/absence evidence; actual discovery still decides.
No command, retry, resource grant or mathematical acceptance rule is added.

Exact selection
`5699ded6dba1a6dc10e674b033248a3532dec2f4ba4650692b685f375097c5a3`
and config
`0cfa1763f6177adb0cd1ad196fddbae81b04229837227ced528e7d95697019b2`
are independently cleared:128existing bindings plus58future snapshot paths
match; the actual02 executed56-source closure plus two fresh modules covers
the new inherited imports. Node02 snapshot/aliases, all original limits and
ports are unchanged. Retained reader1 DBs match exact pins with no sidecars;
output was absent. This selects only the unreached retained-custody suffix,
one receipt/two native calls, not repetition of reader1 or new source authoring.
No reviewer runtime/Git change was performed; root owns launch and outcome.

### Native-controls01 actual import failure; reviewer closure correction

Controls01 outer RESULT SHA
`316cc0caf5f81127e6e78be11559aded17f31e8eef7b5efe00576c4ec7fcf889`
is FAIL, exit1. Actual stderr stops while importing `aggregate.input`, which
imports `delta.packet`: Python first runs `delta/__init__.py`, whose eager
`.receiver` import was absent from the twelve-file snapshot. No control run(),
unit binary, native checker, receipt, guest or proof executed. This was an
incorrect source-closure clearance by this reviewer, not a product relation
failure. The earlier claim that twelve files covered the import closure is
superseded by this actual finding, without modifying old source or failure.

Independent full package/import reading now finds exactly two additions:

- `software/v5/delta/receiver.py`
  `418708346600bff17d2a8425fb9ca322d8eeb9e6a0ad97a6d63c5637bd4df120`.
- `software/v5/admission/verifier.py`
  `9f77bd17abbf87d8f777c52c047d41cfbfd1b29078f29a173006ccad99839571`.

The receiver imports the verifier, admission bindings, codec, producer and
packet; all except the verifier were already selected. The verifier imports
bindings/codec plus standard-library modules only. Read every initializer:
admission/modules have no eager imports, production imports its already held
producer, delta imports receiver/packet, and aggregate is a namespace package
with no initializer. Neither receiver nor verifier is constructed by import;
their dynamic supervisor loads occur only within constructors not called by
these controls. The controls' actual fixed supervisor loads remain separately
bound through the adopted manifest. A fresh fourteen-file selection can repair
the import closure without changing any control, binary or mathematical fixture.

Actual cost:0.28125 inclusive Job CPU plus0.21875 separate wrapper CPU,
0.7050249wall,2total/0active/0terminated processes,peak24,018,944B; direct child
reaped/Job closed, no cleanup errors. All failed work remains charged. Root owns
the fresh exact selection; no retry/runtime was launched by this reviewer.

Fresh controls02 exact selection
`3aed2221be2dee9727660d4212e72a680ec25e9db633970698d6e427fd01d56d`
and config
`c0f826275a5b6e3eda5f8d8ba5cd4f232f394d92a1f735f5f0a52ec55bda5ce6`
are independently cleared. All56existing and14future snapshot bindings match.
The new map includes the complete traced package closure above; controls,
both actual binaries, packet and all limits are unchanged. Only source closure,
fresh output/config/runtime paths change; output was absent at review. No
passing workload is repeated because01 never executed a worker.

### Retained-reader continuation: source cleared, exact selection separate

Independently read fresh `delta/network_continue.py`
`1d80a4dff3d578d8c5f58793381bf997a9dc314cb9363137309203576c0c5cd2`
and `delta/retained_custody.py`
`bb94845d77cac6016ac1be7a1ac04fc822412c557fa9300309cd1b54d120a901`.
Also reread inherited actual02 Campaign/source-closure/reader/cleanup and the
actual packet/module custody schemas. No source-level blocker was found.

The reader1 result, packet DB and module DB paths are fixed to actual02's
preserved recipient. Exact pins are checked before/after read, links/junctions
and SQLite sidecars refused; DB connections are read-only immutable with
query_only/trusted_schema off, 32MiB file ceilings and200,000 SQL-VM-step query
bound. Packet bytes/size/module/offer/profile match the selected acquired
record. Both fresh provider stores derive only those packet bytes; every retained
group/body byte string must equal the structurally recovered packet semantics,
and the export must equal the original actual returned record. Previous
admission flags and DB metadata confer no mathematical authority.

Four new Node lifetimes (neutral seed, transient holder, fresh reader, replica)
exercise the unreached suffix with no repeated first-recipient admission. The
reader obtains an actual first route, the transient holder really stops, and
the replica starts; the same inherited workflow must observe a stale descriptor,
use the same live channel for an alternative route, find a genuine formal
candidate and perform exactly one receipt plus two native checks. Ordinary
authoring-context reconstruction still uses the newly admitted live handle and
received semantics plus pinned foundation. No authoring/proving is added.

The sole publication gate change permits `INCOMPLETE/QUERY_ERRORS` to continue
when there is at least one local ADD_PROVIDER write, no thrown error, coherent
fixed diagnostics, the exact rendezvous key and original live channel/deadline.
It preserves remote_placement_confirmed=false and all acceptance/completeness
denials. Actual subsequent discovery, not that gate, decides usability. The
predecessor remains FAIL and the new report explicitly composes two operations,
not one uninterrupted success. Source/runtime/input selection and actual outcome
remain separate root decisions; no runtime was launched by this review.

Root subsequently rejected the unnecessary minimum-local-write experiment gate:
publication diagnostics should not prevent an actual discovery attempt solely
because no write was observed. The author is preparing an unused successor;
the source hashes above are therefore historical source-review findings, not
the final selected runtime. Exact revised diagnostics/deadline behavior must be
reviewed before that new selection is cleared.

### Affordability source proposal: focused independent challenge

Read `AFFORDABILITY-NEXT.md` and the actual aggregate census/relation, strict
canonical parser, public module relation entry points, and correspondence
inventory/expression/level/declaration implementation. Intervention1 is a
sound small source direction: P(b);C(V);drop(V);P(b);R(V) can become
P(b);C(V);S(V);R(V), since P is deterministic strict parsing plus S and the census
is read-only on the Value. Both existing canonical-size traversals remain in the
minimal replacement; this does not weaken raw duplicate-key/trailing/numeric/
nesting validation. Mathematical checking sees the same Value, exact graph
premises and conclusion. Resource/diagnostic behavior need not be identical.
This saves a redundant parse/allocation/destruction, not a proved full-program
speedup or peak-memory factor. A changed guest still needs fresh adopted A image
even if its internal legacy I journals/content IDs remain byte-identical.

Intervention2, validating a discarded new-theorem proof tree without constructing
it, is plausible but more consequential. The simulation must preserve ordered
traversal, not only the set of visited nodes: const visits its levels before its
reference; projection validates its reference before its expression child; work
increments precede invalid-index and depth refusals. Include failed-prefix work
counter and every name/universe/constructor/field/backward-reference check. A
lexicographic induction separates expression-child descent and level descent;
no level refers back to expressions. Keep Inventory::new and its global row/name
validation unchanged, even for rows unused by the new theorem. Types and committed
bodies retain actual canonical comparison; the mathematical kernel check remains
untouched. First remove constructed output with O(unfolded occurrences) traversal;
do not silently replace multiplicities with memoized DAG cost. No implementation,
guest screen, proof campaign or quantified saving is selected by this review.

### Network02 actual partial success, overall FAIL preserved

The selected readiness successor ran once. Outer RESULT SHA
`1ab8c1ef52449338cc60116577326235a061a8f3e58b89ee52bacfeee67a3bf1`;
inner RESULT SHA
`0876c37c8b28fa1a2878b06e98f889d7beae8e5b4d6bfbe392b681918774371a`.
All 217 independently checked actual bindings match: 56 canonical sources,
46 outer pins, 76 actual-owner runtime pins including the 56 now-created
snapshot paths, 28 canonical/aliased Node source bindings and 11 selected inputs.

Actual reader1 started with no target IDs or HTTP contacts, discovered the
origin through the real formal-feature rendezvous key, adopted its actual
Noise-authenticated descriptor, and selected the first actual returned formal
candidate. The origin publication had one local provider write and no query
error; reader1 routing returned one provider, no query error and no global
completeness claim. Reader1 acquired exact packet 662,480B/54c7dac7 and the real
223,594B/850c33b2 base receipt. The genuine host verified the base receipt under
fixed image I, fully resolved, with rank0 and exact foundation/policy. Its two
native calls bound actual inputs 113,220B/88b71b82 and 101,687B/ea66d3ef to the
retained rank1 and rank2 journals respectively. The first imports the base;
the second imports the exact base and first-delta journals. The integrated
receiver produced the live target52c564f8 admission and durable custody readback.
The packet-only semantic extraction retains 13groups/11bodies with no missing
selected committed value; this is not all future semantics or fresh authoring.
All three mathematical subprocesses exited0/reaped/closed with no cleanup error.

Reader1 then closed; reader2 genuinely located the origin before its departure,
despite a query error for the now-closed reader1. The real origin was stopped.
Replica publication yielded two local provider writes **and two query errors**;
its preserved result is `INCOMPLETE / QUERY_ERRORS`, not failed mathematics or
proof of no placement. The harness required zero query errors and aborted with
`NETWORK_ACTUAL_FEATURE_HINT_DISPATCH` before reader2 attempted any descriptor.
Thus actual typed stale-descriptor recovery, second search/acquisition/admission
and final reconstructed import context remain unexercised. The overall result
stays FAIL; the successful reader1 prefix is retained and should not be repeated.
The next source decision may use those exact received custody bytes, allowing
incomplete advisory publication to proceed to actual discovery under the same
finite limits; it must not relabel incomplete publication as confirmed delivery.

All five Node processes exited0/closed with unchanged role pins, no forced stop
or channel failure. Every pre/post runtime inventory records the same 5,896 files
and 130,118,221 bytes; CPU/time differ normally because each hashes independently.
Origin HTTP handled five requests, zero failures; replica handled none. All
frontier/delta owners close with zero live handles and no cleanup errors. Outer
exit1 is reaped/Job closed, 13 total processes, zero active/terminated, no
termination requested, peak531,005,440B. Inclusive outer Job CPU41.09375 plus
disjoint wrapper0.65625, wall52.7956683s. Inner controller34.796875 and nested
checker CPU are included in the outer Job and must not be added again. There is
no finalization override. This is actual progress, not independent-host evidence
or full v5 completion.

### Aggregate link02 actual PASS; native-controls01 selection cleared

Actual link02 RESULT SHA
`054f9bf9724640b0963b39f13a9c663a1c7bbe80f1102c53a5e3fe5208e5e8f7`.
Both final links completed exit0. Independently compared actual argv against
retained build01 commands: only fat LTO and fresh output paths differ. All212
retained source/snapshot/runtime bindings, both output hashes and four raw log
pins match. No library was rebuilt and no test/native/guest/proof call ran.

- Test binary: 2,403,840B,
  `8918edad50a65ab16c65f2352794618d2677fc134910034050e2bf6b6a51b378`.
- Native aggregate binary: 1,797,632B,
  `59836fe0a35f58e6db82d873b6f830e2d15560a7419d5e68eb64bfa28c20f51b`.

Worker CPU63.03125 (39.765625 tests-link +23.265625 driver-link), separate
controller2.453125, wall76.8809158s. Final Job has8total/0active/0terminated
processes, peak818,597,888B. Two exact owned MSVC telemetry processes received
the preselected postbuild cleanup, with exit observed; no other cleanup error,
final-check error or finalization override exists. Original build01 stays FAIL.

Exact native-controls01 selection
`ecd54b5c1e42bef493d80ce7f03b8ea8a176f4f98e63fface1e55804fbb05afe`
and configuration
`ae13604947e3a82ee3d3c1d09bb3d5f4c7075ddb4143bd4983f77d431e900ffa`
are source/selection cleared. Independently re-read controls a92e2bfb; 54existing
bindings and12future snapshot bindings match, including the actual new binaries.
The twelve sources cover the loaded local import closure. Fresh evidence output
was absent. At most5workers test9unit groups, the retained real two-delta
conditional relation plus cross-language vectors, and three precise refusals
(missing premise, wrong rank, actual invalid theorem proof). Each worker has
30CPU/at most60wall/3072MiB/2processes; owner60CPU/600wall; enclosing allocation
240CPU/600wall/4096MiB/4processes. The original post-report finalization guard
remains. Synthetic A is explicitly nonauthoritative; this neither verifies a
receipt nor grants aggregate admission, and no guest/proof/author/network runs
are selected. Root owns actual execution and outcome adoption.

### Fresh readiness network02: source and exact selection cleared

Independently read the complete fresh role/route helper and every integration
change against used actual01. The selected bytes are:

- `maintained_roles_ready.mjs`
  `9824559f55eca9b1e56786c14cbe090b74904d1786a915f124dc4101b0aa9683`.
- `observed_route.py`
  `9800b5fd3a1f922dcc2e59818916b2333f79004b7f4b6ed42eb89d40891740f1`.
- `network_actual02.py`
  `f772cce4aa6c33bb1970c931d3483f932b102f97258789673dcad8ab497c4718`.
- Selection
  `0435e839636101824929c31ec1119074f9543b27806120be1012af0b5699e512`;
  configuration
  `7eefe36e52b80d1d2abe42e4284053e1c221f47201c60258a110d6454f8323df`.

Read the actual adopted `kad-dht` query manager, query-self, startup,
content-routing and network implementations, plus the adopted `p-event` and
`race-signal` implementations. With `allowQueryWithZeroPeers:false`, both the
empty-routing-table event wait and initial-self-query wait observe the original
operation signal combined with shutdown and early-exit cancellation. DHT startup
starts QuerySelf by scheduling its first call; it does not await discovery. Thus
the neutral seed can start listening with no peers. The background initial
self-query has no independent short query timeout; its bound is the existing
service lifetime/shutdown and enclosing process envelope, not per-query credit.

The exact source permits dial-before-identify/routing-admission; restoring the
event barrier supplies the missing ordering edge. Old actual01 records do not
identify whether the publication race, reader race, or both actually occurred.
This repair is justified by a reachable source defect, not an invented timeline.
The barrier still cannot guarantee connectivity or provider placement under churn.

ADD_PROVIDER is a no-answer RPC. The actual library yields PEER_RESPONSE after
local message writing and does not await stream.close. The new positive label
therefore correctly requires a yielded write and no query error but remains
`HINT_DISPATCHED_UNACKNOWLEDGED`, with `remote_placement_confirmed:false`.
The fixed-size diagnostics count yielded events, not wire bytes. The observed
route helper uses exactly the existing channel, original WorkflowBudget and one
ticket; it retains diagnostics without inventing peers, authority, retry or grant.
Settlement occurs once through the unchanged budget; malformed/expired/channel
failures close and charge the same allowance. Partial advisory hints can survive
an incomplete route without becoming mathematical or global-completeness claims.

Independent prelaunch pin check: 122 existing bindings match (56 canonical
Python sources, 46 outer runtime/input pins, 20 existing actual-owner runtime
pins). All 56 future Python snapshot paths bind to exact selected source bytes.
The 14-file Node snapshot has the two explicit reviewed aliases. Original limits
and seven loopback ports are unchanged; output was absent at review. Root may
select the bounded full endpoint, whose previously unreached formal discovery,
two cold delta admissions and real stale-origin/alternative path remain unchanged.
This clearance is source/selection evidence only, not an actual network result.

### Aggregate native build01 failure and link-only02 clearance

Actual build01 RESULT SHA256:
`8e60e4315158eb85ce63110234d9e179f88df6ecf8502abe8bc2b158abe5eb91`.
The module and aggregate rlib commands finished exit0; test linking failed exit1
with unresolved dependency symbols and semver LNK1107. The driver command was
not run. No unit test, native mathematical check, guest or proof ran. The retained
recipe contains `-C lto=fat`; build01 dropped it. This is a build/link failure,
not evidence of a mathematical relation failure or damaged pinned dependency.
The earlier reviewer did not identify the missing flag before execution; root
isolated it from the actual failure. Preserve that failure and its full cost.

Successful reusable outputs, independently hashed:

- `libdmkn_module_relation.rlib`: 4,217,310 bytes,
  `3d37e6dc700a7e789f8c0aa5f732ae6a7a4d8f46fd3ec9293f9d19bd35b31c0e`.
- `libdmkn_aggregate_relation.rlib`: 876,346 bytes,
  `268f00c6f62f1c826d63546dc7d44ef0544721f0996732491f60f1799813c1e4`.

All 212 canonical/snapshot/runtime bindings match: 19 canonical source files,
the exact 19-file actual snapshot, and 174 retained native runtime pins. Retained
source-map SHA `82c4dc73df29c9a4b6638ef1dd872ad8a0ccfeb66f97f89c5923ada93494f0d6`
and compile-command SHA
`1f80c02b5049dbb5bdb22fea28ff52d8def582871b27366dd1cd98a73be5e232`
also match the successor's exact pins. Actual worker CPU was 18.96875 seconds
(11.96875, 2.296875, 4.703125 by command), controller CPU 1.546875 separately,
wall 7.0430142 seconds. Final Job: 7 total processes, 0 active/terminated,
655,794,176-byte peak private commit. No telemetry cleanup, cleanup/final-check
error or finalization override is recorded. All six retained command-log pins
match, with empty cleanup-error lists. Eight separately pinned controller,
supervisor and Python helper/runtime files also match. Full v5 remains unfinished.

Fresh link-only source SHA
`59f85991f3206a15000703231530b7c5d232948d92be565cba656ec623d8461a`
and selection SHA
`6659bdb51431f1633c2ce9f5740c05232381e308be3cdad8c66d08d579168726`
are independently cleared. It loads the pinned predecessor helpers without
invoking their main functions, reuses the two successful rlibs and exact old
snapshot, and runs only the retained final two commands. The only command
changes are restoring `-C lto=fat` and choosing fresh executable output paths.
No successful library compile repeats. The worker retains 240 CPU/240 phase-wall
seconds, 3072MiB and six active processes; controller retains 60 CPU/600 wall
seconds, 1GiB/8192-entry output cap and post-report overriding finalization check.
The fresh output and attempt were absent at review. This clears two links, not
test execution or admission. No reviewer runtime or Git mutation was performed.

### Aggregate native build01: exact compile-only selection cleared

Source-reviewed `native.rs`
`b153bdd3ae6be389b1e81d4731bfc7c1fcff22ce64eacb2668f54e835e2195ad`
and `build_native.py`
`4b77bad55119746df2e66cf7b8336b62ee1db8bfa4dca7152b6c1512b4ad892a`.
The native driver directly invokes the aggregate relation, returns exact
conditional claims/header/members/openings/input hash, and labels all output
non-admission. Error or checker panic returns refusal/exit2. It verifies no
receipt. Build source now rechecks original controller wall/CPU and output
census after RESULT and attempt writes, with explicit FAIL_FINALIZATION override
and nonzero return; the earlier pre-write-only draft is not selected.

Root selection:
`50edb1a8c307b1a55a17ba6f7941851402a6ba28461e6d5bad83ef6f983e4d3f`.
Independently checked19exact source files plus174 retained recipe runtime pins
(193bindings), and separately the recipe, native-library02, previous helper,
three provision helpers, finite phase runtime, D:/Python314 executable/DLL and
both exact Job helper files. Output and attempt were absent. Source closure
contains9unchanged module-relation sources and10aggregate/build files.

Only four thin rustc builds are selected: module relation rlib, aggregate rlib,
structural test executable and conditional native driver. There is no Cargo,
checker rebuild, test execution, guest, proof, receipt admission or networking.
All four share one240CPU/240wall worker phase,3072MiB/6active-process cap; the
controller retains600wall/60CPU and1GiB/8192entry output limits. The retained
telemetry cleanup can close only its own exact selected remaining MSVC helper.
This is source/selection clearance, not a successful build or permission to run
the resulting executables; actual outcomes require separate audit.

Reviewed `native_controls.py`
`a92e2bfb21e81c0a5dcae6713fc5d7a929723828111bbab797b356f41a6914c5`
source-only. It proposes at most5bounded workers:9structural unit groups, actual
retained two-delta conditional checking, and missing-premise/rank/invalid-proof
refusals. Python independently binds all3journals, header/root/paths and aggregate
census. Synthetic A is explicit; no receipt verification or authority is claimed.
Exact binaries/config/runtime selection remains pending and no control was run.

### Actual network01 outcome: independently audited FAIL, no math attempted

Root reports session73832 terminal and reaped. Saved outer RESULT
`09f4ebfc23bec4d773ef7c84b9c35904830ad16d8ba5a4f10a642d73dd2ad279`
and inner RESULT
`367be7f9ae7fe13fd2e3ca3af9f734184d9647d2cbbea76a844b5f7021e67706`
independently establish failure at `NETWORK_NO_LOCATED_INDEX_CONTACT` in reader1.
All 210 selected actual bindings still match, now including the actual Python
snapshot files. Copied selection is exactly1718ca6b; config86dbacee remains
unchanged. No FINALIZATION-FAILED marker exists; the raw outcome is simply FAIL.

Origin built structural custody with13groups/11bodies and no missing committed
values, then reported ADVERTISED_HINT for rendezvous4ae286d8. Reader1 actually
joined the neutral bootstrap but its sole route returned an empty peer list.
There was no descriptor request, HTTP search/acquisition, receipt owner, delta
owner, mathematical check or admission. Reader2 and replica were never created;
origin loss and the typed descriptor-recovery seam were never exercised. An
advertisement status is therefore not evidence of successful distributed lookup.
The exact underlying DHT/topology cause is not established by these records.

All3Node controllers closed with exit0, unchanged role/source pins, successful
5896-file runtime pre/post checks, no channel failure or forced termination.
Their raw stderr reports LOCATION_IPC_CLOSED, zero live transport connections,
zero descriptor-unavailable events and no exhausted transport allowance. Origin
HTTP had0requests/0failures/0active; cleanup errors are empty. Outer Job reports
5total processes,0active,0terminated, direct-child reaped and Job closed, exit1.
No proof or admitted artifact was produced or relabeled.

Actual cost:21.578125 inclusive Job CPU plus separate0.703125 wrapper CPU,
90.4038063 outer wall seconds,533635072B peak Job private commitment. Inner
controller18.015625CPU/88.4697278wall is already inside the outer Job cost.
Bootstrap's first full runtime hashing used69.6194914wall;405seconds remained
before reader1 startup, so the failed empty route is not a deadline exhaustion.
All source/config/evidence stays frozen. No retry, cap renewal or automatic
successor was selected by this audit.

### Aggregate input encoder: source correspondence cleared

`aggregate/input.py`
`5c5d51403bb00234f5843a1b6ca4109195285e292bdcdcc08f07ae94c7b0a226`
matches Rust's DMKNAI01/v1 wire: image/counts, tagged184B-I or192B-A claims,
frontier claim indices/member openings, raw target ModuleIDs, and u32LE-length
witness frames. It checks finite list/wire bounds, unique/used claims, exact
legacy or aggregate frontier binding and duplicate frontier modules. It does
not claim topological validity, new-target validity or mathematical correctness;
the actual Rust relation checks those independently.

`from_legacy_packet` correctly compares canonical summary bytes (the existing
packet parser returns bytes, not a summary dictionary), preserves exact pending
receipt/journal pairs and canonically encoded mathematical witnesses. It does
not validate the receipt-to-journal claim. Real host verification and resolved
guest assumptions remain mandatory. No encoder/test/compile/runtime was run.

### Aggregate host receipt boundary: standalone source clearance

Root's unlinked `aggregate/receipt.rs`
`41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254`
uses the same real-cryptography profile as the retained module host: bounded
fixed-integer bincode with trailing-byte refusal, genuine Succinct Poseidon2
only, no RISC0_DEV_MODE variable, explicit verifier dev-mode=false. The retained
SDK implementation was inspected: verify_with_context performs real integrity
verification and compares the exact ReceiptClaim::ok(image,journal digest),
including successful exit and resolved assumptions, not integrity alone.

Pending claims must be the fixed I member statement or the independently
adopted A aggregate header. Exact pending journal bytes are compared to the
real verified receipt. Final aggregate verification first binds expected
header.A to adopted A, then genuinely verifies that image and exact header.
VerifiedReceipt fields are private and accessors immutable; structural helpers
or serialized success reports cannot construct it through this module's API.
This is not a session/expiry implementation. Consumer adoption/lifetime policy,
hostile-deserialization memory/CPU containment, complete producer resolution,
linking/build/execution and a public aggregate member receiver remain separate.

### Actual network01 source and exact selection: cleared, not yet executed

Reviewed the complete `delta/network_actual.py` successor SHA256
`1d3a7802790186a7ceb929fecc2bcdd99bc72a46049ce23f0f0795b379b4ea2c`
and `network_actual_api.md`
`c4675e6f61284292e672a51c6704ebb68b8b6ae9053759cc53602a4de982ac57`.
Before use, review corrected the missing post-report original-deadline check
and a reader2 local-variable shadowing defect that would have replaced custody
evidence with the last body response. The final source retains operation error
separately when cleanup also fails and uses a FINALIZATION-FAILED override.

The source has two fresh genuine receipt/native owners, not transferred live
handles. Reader2 first obtains the real origin route; only then does the harness
close origin HTTP/Node/stores and start replica from reader1 custody. Reader2's
same channel and prepaid grants charge the stale descriptor and route again.
The first actual returned formal candidate is selected without target/provider
ID injection. Expected retained identities are checked only afterwards. This is
trusted same-process orchestration, not adversarial process isolation.

Both readers reconstruct committed selected groups/bodies from acquired packet
bytes. Reader2 opens its own live DeltaImportSession and reconstructs normal
authoring context using those bytes plus the independently adopted foundation.
This adds no Lean authoring or mathematical-verification call. Independent
read-only inspection of the retained packet found 11 available body hashes and
16 selected declarations, with no missing demanded definition/recursor hash;
this inspection is not a successful context reconstruction or admission test.

Root's exact unlaunched selection:
`1718ca6be75e5971d44f5929f52c00350841352c28bcd6f1251013c92744f636`;
configuration:
`86dbaceea85da39233893f3bc300e1bea1f45f34dad1f29ac0bd2d9b64f74865`.
All 210 independent prelaunch bindings match: 55 canonical sources, 43 outer
pins, 75 owner-runtime mappings (including 55 future snapshot paths checked
against their exact canonical bytes), 28 Node snapshot/source checks, 9 inputs.
Future Python snapshot/output is correctly absent; the 14-file Node snapshot
exists with only the selected entry alias. No unexpected source borrowing is
allowed by the loaded-source closure guard.

The enclosing allocation is 300 CPU seconds, 600 wall seconds, 4096 MiB and
8 active processes. The original workflow is 480 seconds; at most 3 location
children coexist. Each of two admissions reserves 30 receipt plus 2 times 30
native CPU seconds under the same app grant, with 32 requests/32 MiB replies;
18 requests and 1,081,344 reply bytes are prepaid before each reader starts.
Seven root-selected loopback ports are 43171..43177; root's preparation bound
and released them, which is not a guarantee against a later bind race.
The generator and frozen snapshot/supervision runner were read. Clearance is
only for this one finite operation, with no automatic retries or renewed grant.

### Aggregate source and Python/Rust bindings: source clearance only

Read the stable eleven-file aggregate crate, its source controls and API in
full. Production delta construction directly calls the unchanged mathematical
relation; no checker callback can inject a conclusion. Private graph edges are
the exact returned parent journals, with existing-member equality, strict rank,
duplicate/conflicting ModuleID refusal and full backward target closure.
Every claim must support a selected frontier. The guest discharges every exact
typed I/A assumption via real env::verify before committing the 192-byte header.

The header's exact A binding and overflow-checked increasing seal height support
induction over prior aggregates independently of mathematical rank; within one
aggregate, topological checking establishes the new members. This reasoning is
conditional on genuine recursive-receipt soundness and the adopted checker's
conditional extension correctness, not an independent proof of either.
The Merkle construction binds domains, member count/index, exact legacy journal
bytes, ordered level nodes and explicit duplicate-last padding. One selected
member needs only its bounded opening, not all sealed proof witnesses.

Wire length is checked before each witness byte-vector allocation. Global
rows/bodies/openings/edges/nodes are bounded; the JSON tree is nevertheless
constructed before the global node census, as the API now states explicitly.
The temporary census tree drops before the unchanged checker parses the frame.
Outer memory/cycle bounds and actual feasibility remain necessary. Test-only
synthetic graph conclusions are not production or cryptographic authority.

Exact reviewed crate hashes:

| File | SHA-256 |
|---|---|
| Cargo.toml | `58d5d9d2ccfde1c060948c9c2ef5978175c809ac187defb8e8c1573a409b9363` |
| lib.rs | `ae71c52390fd47fa3b0cb130b289ff19629bbd8cb976f59c0042e1aabb95c340` |
| header.rs | `642167ddde6a6f134efff58a2ab270916ebe050f7d0f29acf69f8aaa3465a8e8` |
| membership.rs | `25e6a2fa86f4c095dd9bd76ce83de60c55405bc9d52eeec1c668e51c07e04b6d` |
| wire.rs | `2368990cb04186b0e01f3b2075cf7e0505ffaa26f4f2aef6680a342b39f7957d` |
| census.rs | `f6ab62fe777482acb913972a34689eeaec16ed99fedae584cc6b62f6e4ba18df` |
| relation.rs | `0f4e240727511764ef4b86a8185c55eb310b89396dece2e8f12fca055bc3460b` |
| main.rs | `d7b9b93843b683215e0556e585bc5ea241c672fe4c2a89cc07afa41afb81acad` |
| tests.rs | `6a784eb7781284e8560928a5b47089721dadc38ef725f31ba7c3d89d14e089ae` |
| graph_controls.rs | `7a055e63d1a4420ac8187f592342f4574e3604f5eff0a14510cc9526e924bec4` |
| API.md | `90b14c1d415a4f01c80ee4237551d2554b2610c71f4c4f233a19e507d824431e` |

Root's Python `aggregate/bindings.py`
`d749273ef5841afe881407bcb3c2655385dd635bdae12b37e09ca2381a46bcd5`
matches the Rust header/member layout, LE image-word/integer framing, policy,
count/height/rank constraints and domain-separated SHA construction. Canonical
lowercase hex ordering equals Rust digest-byte order. Paths agree for singleton
and odd-width trees; index/count/depth/duplicate-last rules coincide. Python
requires an adopted A when decoding, but performs no cryptographic verification.
No build, test, guest execution, new receipt or public receiver is established
by this source correspondence review. A distinct fully resolved A producer and
receiver, typed frontier/import path and network exposure remain required.

### Recoverable descriptor-unavailability seam: narrow source clearance

Reviewed `node_entry_services_available.mjs` SHA256
`02bbdf1223602aff512ae9cfadcc58f2b5e6efc02e1c1b65b34e3f14ebc75fb2`
and `available_descriptor.py`
`d3b215f59c0b4745562fdc76339a53f22d0fa009932dfecbef4fecfff6743fba`.
No runtime was launched and no outcome is inferred from this source review.

The retained TCP implementation changes an OS connection error's message but
preserves its `code` and `syscall`; transport-manager forwards it, and dial-queue
rethrows one exact error or a nonempty AggregateError of per-address failures.
The locator's `_command` resets busy without aborting the service on such a
failure. Thus an immediate refused TCP connection can reach this narrow seam.
Timeout/abort, authentication, protocol and allowance failures do not acquire
the accepted code/syscall pair; mixed aggregate failures remain terminal.

Recovery requires the original operation, life and locator signals still live,
the locator not stopped and its service deadline unexpired. It returns only a
typed local dial-unavailability observation, never authenticated absence or
nonexistence. Python binds the exact ticket/peer/status, checks the original
deadline, and abandons the ticket at its full reserved reply charge. The same
actual ServiceLocationProcess, WorkflowBudget and grant remain in use; positive
descriptor authentication and validation remain unchanged. All malformed or
other outcomes close the channel. The existing raw transport counters continue
charging failed connection attempts.

Root must use a fresh snapshot with these exact successor Node bytes aliased
as `node_entry_services.mjs` and that successor digest in the original role map;
the frozen predecessor is not modified. This clears only the source seam, not
the complete stale-provider lifecycle or any mathematical/network release claim.

### Actual retained-export repair01: independently audited PASS

Reprepare01 completed exit0. All184 independent bindings match:44 canonical
sources+44 snapshot sources+27 selection runtime+63 actual owner-runtime+6 exact
inputs. Outer RESULT SHA256
`232ef9cb77ffc12d46765fe49d3a428c5e7de6252689d22258fb3c22e6a852a7`;
inner `ae0297103d563c03561e8cc0eb803cdb7756a99d69f0d83dc067943fe1d949d5`.

Independent decoded packet comparison confirms ONLY the final1009-row witness
field changes. All other packet fields, prior witness, genuine receipt frontier,
mathematical spec/body commitments and local proof source are preserved. Exact
new and cold-receiving662,480B packet SHA256 is
`54c7dac7f83a9a06c2b23b17a77be20364c1b90e4cd3b1db58b69c62fda2dcf1`.
Actual first-delta parent equals the actually verified base journal; actual
second-delta parents equal the actual base and first-delta journals. The fresh
receiver admits unchanged target52c564f8 at rank2, opens its selected group and
exports the exact complete packet. This is genuine local native-delta authority
over a real cryptographic frontier, not a new succinct child certificate.

All three workers and outer Job exit0 with clean closure/reap, zero active/
terminated processes, no termination requests and no cleanup errors. Actual CPU
is0.046875s each; receipt/first/second wall0.7192437/0.1416823/0.1193155s. Outer
inclusive6.625CPU plus separate0.5625wrapperCPU,8.638137wall,peak107,601,920B.
Every final owner is closed with zero live handles. No author, guest, proof or
network call runs. Author01's failure and46.796875CPU+1.171875wrapper cost remain
preserved and charged; this recovery does not rewrite that outcome.

The shared corrected emitter has now been exercised with the retained export.
The new authoring02 live ordinary-source API path itself has not yet executed;
future normal use must select that successor, not the frozen faulty authoring.py.
Network circulation, aggregate certification and full-cost growth remain open.

### Retained-export reprepare01 exact source/selection clearance

Reviewed reprepare_actual.py; required one finalization correction: after writing
RESULT, recheck the original deadline and write overriding FINALIZATION-FAILED
on late/error return, as in prior harnesses. Corrected source
`fcb9af85e264047caf31b4936c8fb93e8ae6da71d4d6db1802e30ba1621b68bc`
is cleared with selection
`d20434664f4e94ff20186c659e71851c76c0ce2e394c08aa68551901e2a425d9`
and config `640c3fb38142b6cc1da0686137544a23c62eb3f20c37f458b61c1b42a16ecb77`.
All140 prospective bindings match:44 sources,27 selection runtime,63 actual-owner
runtime and6 exact inputs. Future snapshot references all map to selected
sources; output absent. Actual failed packet40aac392/export268681e0/request17cc9657
and fixed foundation736792e remain exact inputs, not editable prior evidence.

The harness requires only final witness rows to change, retains the same target
and actual successful ordinary-source export, then independently receives the
complete corrected packet with at most one real receipt and two native checks.
It opens the target, verifies exact re-export, checks final pins and closes all
owners before reporting. Earlier preparation profile contributes immutable receipt
host fields only; no old Producer/Owner source origins are loaded. Outer300CPU/
300wall/2048MiB/cap4, original workflow240wall, per worker30CPU/90wall/1024MiB.
No ordinary author, guest, snapshot, proof or network repeat is selected.

### Aggregate-DAG sealing principle audit: coherent, not implemented evidence

Read full DELTA-SEALING-POLICY.md and coordinated directly with its source author.
No blocking architectural contradiction identified. The proposed header is
indeed192B. Unchanged184B internal journals labeled I denote the existing
conditional module relation; real A receipts and exact Merkle member openings
provide a DISTINCT warrant. They must never be passed off as I receipts or
admitted by the frozen exact-I receiver. Preserving ModuleIDs is compatible with
an explicit new proof-form authority, not a permission to bypass image checks.

The top receiver must verify actual adoptedA and bind the header's suppliedA to
it; guest parent aggregate headers must agree onA/I/foundation/policy. Computed
seal_height is1+maximum parent aggregate height, with overflow refusal, and is
separate from mathematical rank. Conditional induction on height followed by
the actual finite relation-returned dependency order is valid under real recursive
application/commitment/checker soundness assumptions. Mathematical source sharing
alone is not a formal checker-to-Lean equivalence proof.

Required source obligations communicated: call unchanged relation::check_bytes
DIRECTLY, never a callback allowed to invent checked conclusions; keep pure
aggregate results explicitly conditional until real env::verify premises all
discharge; check unique/unused assumption descriptors and member openings
separately; derive exact graph edges from actual relation journals; require new
designated targets and complete no-extras backwards reachability; enforce exact
encoding/endian/domain hashes/odd-leaf handling/count/index/path depth; validate
frame length against remaining global budgets BEFORE allocation. Actual SDK
receipt-byte and full-resolve limits remain host obligations. No native/mock
control may grant cryptographic or mathematical authority by flag.

A bounded selected member commitment avoids mandatory global-state growth and
sealed-proof downloads. It does not eliminate demanded definition semantics,
future availability, new proof checking, aggregate prover cost or resource
refusal. The single-moduleI route on an uncertified chain genuinely requires
intermediate receipts; batching can remove separate certificate overhead, not
the sum of new mathematical checks. The documented cost model and capacity
inequality are conditional; they establish neither demand nor full-cost network
advantage. A new guest/host/member receiver requires separate exact review and
selected execution evidence; this principle audit authorizes no build or proof.

### Narrow relation-order repair: source clearance only

Reviewed fresh authoring02.py
`9438a5cb6d3a2e8172b0a655e49c13589c351297e7819760e47b5bc331bcbec1`
against the frozen predecessor: exact differences are documentation, importing
the shared emitter, replacing the import/local row-emission block, using its
returned rows, and requiring own/helper source pins. Frontend topological context,
live-origin obligations, full ancestry retention and mathematical gates do not
change. Used authoring.py remains untouched.

Read complete fresh reprepare.py
`af225a6dbfb6c7b5c28f0b8fb43374f06b2c4e139066c1c77ed3d07f6f739195`.
Validated lowercase64hex owner order equals Rust's binary owner ordering; numeric
group-index order and local-spec group order then match unchanged relation
bindings. Duplicate imported keys refuse. The pure retained-export helper decodes
actual local proof material, requires exactly the prior local spec and exact
context-to-parent-opening group map, verifies supplied body commitments, preserves
every other witness/packet field and changes only final witness rows. It neither
loads a saved acceptance flag nor revives an old live handle.

No blocking source finding. Exact fixed foundation and retained input bytes must
be selected/pinned by the forthcoming harness; preparation output remains fully
untrusted until independent cold receiving. No author/proof rerun or checker
weakening is authorized by this review. Actual corrected bridge qualification
and future ordinary authoring02 integration remain separate from source clearance.

### Actual ordinary-source return01: retained FAIL and independent diagnosis

Root session54525 terminated exit1. All262 independent bindings match:43
canonical and43 snapshot source pins,36 selection runtime pins, plus140 actual
owner/profile/runtime/fixture pin-and-size checks. Outer RESULT SHA256
`b9f04f725f58b82597b8376dbffb8b7491449b528e30fdfcd4ff3900cadb79cb`;
inner `cca82866f3cf3255c872f4747551c8b7e9d6e0b460589594f345efbef323c699`.

The original real receipt+first native admission succeeds. One ordinary Lean
author produces126 export rows, one four-universe new theorem and one local
group. Independent read-only traversal of the actual exported proof DAG takes
153 expression visits and confirms exactly two references to the first module's
fold_map_received, not just two occurrences in source text. Export5813B SHA256
`268681e0e4193badaa073be369ac062b678ef65123d152780182c448c2f902b7`;
request63616B `17cc96571235788c335e7426e9060f43c5ec42bc0a299d83756b6b37092daf38`.
Preparation retains complete662,480B packet
`40aac3921a49b144c19cb7310679741abbd82bb7d796f05a5a0beb71ee60649d`,
target52c564f87f31082468557df6eed0a04bc7adf9d28d9614fe6cf173f5633088bf,
with one actual receipt frontier and two deltas. The cold receiver's packet is
identical; both first-delta copies are exact88b71b82. All origin owners close
before cold receiving. Cold real receipt and first delta pass; second delta
refuses at CORRESPONDENCE_DESCRIPTOR_RECORD_MISSING, exit2. No new target is
mathematically admitted and no return handle survives.

**Independent diagnosis:** the relation collects imported groups in a BTreeMap
keyed by `(ModuleID, group_index)` and correspondence matches their ordered
bindings positionally against native group rows. DeltaSourceOperation.finish
instead emits frontend `context.imports` in its dependency-topological order.
Actual decoded native group position1 is base.binary_congr, while the relation
expects base.Tree.below. Other base groups are similarly permuted; owners and
names themselves are correct. The earlier source review missed this ordering
incompatibility. NativeRows.group and the mathematical checker are not the cause;
do not weaken correspondence to accept mismatched groups. A fresh successor
should emit witness imports in exact relation order while leaving frontend
dependency order unchanged. Used authoring source/harness/failed evidence remain
frozen; retained source export can support a separately selected bridge repair,
without repeating ordinary authoring or increasing unrelated limits.

All six worker Jobs and outer Job have clean closure/reap, zero final active/
terminated processes and no cleanup errors. Real receipt CPU0.03125s each;
origin first native0.03125s; cold first and failing second native0.015625s each.
Author Job3.625CPU/6.8725487wall, peak488,300,544B. Enclosing46.796875CPU plus
separate1.171875wrapperCPU,56.0269228wall,peak523,395,072B; do not add its nested
workers/lifetime counters again. No network, guest, snapshot or proof ran.

### Actual delta-network-controls01: scoped PASS

All five new controls pass with zero failures/errors. All88 bindings match:
34 canonical source+34 snapshot source+20 runtime pins. Outer RESULT SHA256
`2557246477e83baac75e31f430778f859747b900389aa594a205fba98686fca9`;
inner `632188e968ef3ea75284d07371c2292ded1f082c331a9178869b4eb4019f62e6`.
Worker0.71875CPU plus wrapper0.328125CPU,1.7805488wall,peak28,286,976B. Exit0,
closed/reaped,zero active/terminated processes,no requested termination or cleanup
errors. This establishes the selected SQLite/structural/loopback-byte controls
only; no positive mathematical authority, crypto/native/Node worker, positive
located handoff or global-network/growth result. Used source/tests are frozen.

### Exact ordinary-source delta-author01 selection clearance

Prospectively cleared selection
`159c8c6f8a5350b3d3d113187fba1126dbc4be761923f03193d162a9455e740b`,
configuration `3a923f554528848fa42415c9db165d99c4b50b77c69e40101025fe700a2bd41f`
and preparation profile
`f03b591c6e9e40346028c35b663d4d2c5daaf9a58ec6eb890810f96c6c984a4b`.
All219 pin/size checks match, covering43 canonical sources,36 selection runtime
pins,60 owner runtime pins,40 preparation-source pins and the additional actual
worker/producer/Lean/input bindings. Future snapshot references all map to exact
selected source bytes. The output root was absent at review. No arbitrary old
same-byte origin is substituted for the worker, Producer, helpers or fixtures.

Maximum work remains two real frontier checks, three native relation calls and
one ordinary Lean author, each with30CPU maxima:180 worker CPU total. Outer
420CPU/420wall/3072MiB/cap4 leaves controller headroom; original workflow360wall,
owner300wall,120controllerCPU, one30CPU author,256MiB/512entries storage. Per-call
90wall/1024MiB and inherited inner cap2 remain. The112MiB-plus-request transient
authoring storage reservation fits. Actual owner runtime pins total86,016,597B.
Known Lean DLL/Init pins do not imply complete hermetic olean/OS closure.
No snapshot, guest, proof or network work is selected by this clearance; actual
success, complete cleanup and substantive new proof reuse await terminal audit.

### Complete-packet custody/network source review

Exact structural-controls selection84b83dfdef0dd8d11851bbc89c4be7888af838a2b7c0ea4204f1678f9aecfaf9
is prospectively cleared:34 source and20 runtime pins all match; fresh output
absent. The transitive imported controller/workflow/parser graph is included,
but no Node child, native checker or cryptographic verifier is constructed.
Only the five new controls run under30CPU/60wall/512MiB/cap2, in output disjoint
from delta-author01. The old packet suite is not rerun. Outcome audit is pending.

Read the complete source, including the previously truncated transport middle,
and the revised prospective handoff. Source-cleared exact SHA256 values:

- custody.py `4304e529a15e9249d8ba43f5390e94082d0baad1c55db6fb5b74b4160a1fa27c`.
- transport.py `18c1abda1dca45cd8f5e86c09c4e1b8d5b13d4472931173a1db4a080c0c71d40`.
- test_network.py `39d8c9d28fab9ab1e0a2f0a7852a94f02565deabd64d1f15a7a484d6b019f23e`.
- network_api.md `688fac0a8539b61aed288d1d6a784b4a20250cd96f9d4760a606580f3bde47d4`.

Distinct packet profiles/stores/routes preserve the receipt ABI and never turn
structural custody into mathematical admission. The composite provider actually
serves a formal index and selected semantic groups/bodies, so advertising the
existing index role is legitimate; generic custody-only routing is not claimed.
Packet digests, target summaries, quotas and atomic packet/offer writes are
checked. Cross-database commits remain non-atomic; readback establishes current
selected custody, not future retention or availability of every future body.

Review identified that the first `from_search` draft merely required a nonempty
external prepaid ledger. Its replacement uses exact `DeltaLocatedHandoff`:
the actual fresh reader channel is checked before start, the actual existing
workflow is constructed from exact grants, complete route+descriptor+search
request ceilings and descriptor/search reply capacity are prepaid prospectively,
and the original channel/workflow/budget/adapter/policy/query/deadline identities
remain bound. Only one originating search and one acquisition handoff are issued.
Export acquisition requires a candidate actually seen by that search. Contact
expiry/egress is rechecked. The original reader must remain open/unfailed until
the workflow completes, not be closed immediately after obtaining contacts.

Admission reserves the SUM of all frontier and delta CPU maxima under the same
acquisition budget before actual receiving. Original deadlines, exact live
DeltaVerifier identity and post-admission semantic/packet readback are checked;
failed finalization revokes the verifier. Nested reservations are constraints,
not separate actual costs. The inherited600CPU per-admission budget remains.
Application budgets do NOT measure all DHT wire, bootstrap/provider/controller
CPU or framing costs; those still need separate evidence and enclosing Jobs.
Owner Python is trusted; this is not an adversarial-process sandbox.

The five new controls are source-cleared, UNRUN at this review: wire/authority
separation; SQLite reopen/dedup/corruption; transaction/target/profile/quota
refusals; actual bounded loopback byte acquisition and supplier-offline readback;
and unoffered/duck-authority refusals. Their zero-row synthetic packet is
deliberately invalid mathematics and cannot grant admission. They do not test a
positive actual prospective handoff, DHT discovery or real delta admission.
Root must separately select finite exact execution; no old suite is repeated.

### Actual native-delta admission01: independently audited PASS

Root session95240 terminated exit0. Independently checked82 pins:12 canonical
sources,12 retained snapshot sources,27 runtime/input pins and31 exact actual
owner pins; no mismatch. Outer RESULT SHA256
`8faee6c64f9769c807f22138c177c5aad1b8a04b955db78bcfd01d85a6f77132`;
inner `40ff77e5cef75870b79041236488d7297c08035c1405ab0ddb361f0f3fd8c91d`.

The actual host fully verifies base receipt850c33b2 under the adopted image and
policy. The native driver's sole parent journal is byte-equal to that actual
frontier output. Its actual113,220B child input is exactly88b71b82; its computed
184B child journal equals retained expected07734789. The real receiver admitted
child4adbc049, opened child and base groups, exposed the correct distinct two
member proof forms and exported the exact560,792B complete packet SHA256
`a6a1fc259a154a82c489b536ee5bee91b22cf476d8da8fe9d0f12732a07ee3b8`.
This is real conditional-native-plus-certified-frontier admission, not a saved
report substituting for mathematical authority or a newly minted child receipt.

Packet-cap and missing-frontier controls perform no native/receipt work. The
negative native witness differs from the positive bytes ONLY by the unique
theorem proof reference1200 becoming type reference770. The checker reaches its
actual definitional-equality assertion, which the driver catches and returns
as REFUSED (`CHECKER_PANIC_OR_UNRESOLVED_DEMAND`), exit2. This establishes genuine
native refusal without claiming that every such generic refusal proves falsity.
It is not a timeout: closure/reap pass, no termination was requested, and final
active/terminated counts are zero. The earlier positive handle is revoked; every
owner is finally closed with zero live handles. The fabricated handle also refuses.

Actual worker CPU is0.03125s each for real receipt, positive native and negative
native; their wall times are0.7318819/0.9369466/0.1371026s. Enclosing Job CPU8.125s
already includes all workers and controller activity; add only separate outer
wrapper0.46875s, not overlapping lifetime counters. Outer wall10.7333411s, peak
private commit94,916,608B. No cleanup errors, guest, proof, source author or
network calls. This closes only the selected real admission/changed-boundary
gate, not ordinary delta composition, network circulation, net growth or v5.

### Ordinary-source two-delta return harness: source clearance

Read all of `delta/author_actual.py`, SHA256
`a9897ec4a4380cf5b34404ac4a1cbae0b35d4764ea783d22ad5bd3e08d0a17a9`,
the exact DeltaFoldMapTwice source/root fixture and its called public delta
authoring/preparation methods. No blocking source finding. The harness imports
the retained first delta through an actual cold receipt plus native relation;
creates one four-universe ordinary-source theorem using that first theorem twice;
inspects the actual exported proof/value closure for at least two first-theorem
occurrences; and retains exact first witness plus the new witness above the same
genuine base receipt. The returned packet remains untrusted until admitted.

Every originating operation/session/preparation/delta/frontier owner is closed
before a distinct cold recipient verifies the full packet, opens the new group
and exports identical onward bytes. Final owner reports follow cleanup; cleanup,
deadline, source/runtime/configuration changes and late reporting failures override
success. Maximum two receipt calls, three native checks and one ordinary Lean
author; no network, guest, snapshot, sealer or new negative campaign.

This is source clearance only. Exact future-snapshot helper paths (`actual.py`,
`authoring/receipt_integration.py`, this harness and their actual imported graph)
must be included in both applicable profile and runtime selections; inherited
same-byte paths are not sufficient. Root owns the finite configuration/launch.
Actual mathematical success and any full-cost benefit remain unestablished here.

### Driver02 actual audit and exact delta-actual01 clearance

Driver02 completed compile-only PASS. Independently checked all 196 current
bindings: 11 canonical files, 11 retained source snapshot files and 174 runtime/
evidence pins, with no mismatch. The seven compiler warnings are unused imports,
functions or constants, not compilation errors. The executable is 1,713,152B,
SHA256 `37a0af1b08e7176fb0d387b3e8439266d7c2c0befe5b08bc3cdd4c90c62d3e40`.
RESULT SHA256 is `e655d48f89b102e3e41285e6c8dc6594e81b6954f0efcc3b0e2452ff7be99879`.
Compiler exit0; final Job has zero active/terminated processes, no cleanup
errors, and observed exit of the exact selected owned VCTIP helper. Worker CPU
43.59375s plus outer controller CPU2.265625s; the latter includes main controller
CPU, so do not add it twice. Outer wall50.5353079s; peak worker commit746,483,712B.
Report-writing/exit tails retain their explicit accounting exclusions. No
mathematical native check, guest, proof, network or dependency rebuild occurred.

The exact delta-actual01 selection
`f9315f53a9d515ea4f2fd6ac2c33ef0dbdf3ac4a93d5b8ce914663a5b971344c`
and config `7f5b305b1c2977157f90052de965e6831d9641015ba1364532fc921cd6983868`
are prospectively cleared. All 70 checks match:12 canonical sources,27 runtime/
input pins and31 owner runtime pins mapped from exact future snapshot paths.
The output root did not exist at review. Reread the complete actual.py; it
extracts producer configuration fields from the earlier preparation profile
only and never instantiates Producer or OwnerPreparation, so it does not load
the old source-pin origins. The current imported graph and adopted supervisor
manifest remain separately pinned.

Outer budget300CPU/300wall/3072MiB/cap4; original operation wall240; native and
receipt reservations30CPU each. The reviewed one-receipt/two-native maximum,
real clean native negative and final closure requirements remain unchanged.
This clears root selection of one operation, not any assertion of runtime
mathematical success, scalable network operation, growth benefit or release.

### Delta ordinary-source authoring successor: source review only

The separate actual-receiver harness `delta/actual.py` is source-cleared at
`960773b95e1a7cf5f273174f938bcd1c67cef1715b6717494c6993b34e8bebe4`.
It binds retained ordinary-source child88b71b82/expected journal07734789/base
receipt850c33b2, with no source authoring or guest/proof repeat. It selects one
genuine cold frontier admission and one native child admission, opens target and
base member interfaces, exports exact complete onward bytes, rejects a fabricated
handle, then reuses the SAME verified frontier for a native ill-typed-proof
refusal (only actual theorem row value1200 changes to type term770). It requires
nonzero native exit with clean closure, not timeout, and observes prior-handle
revocation. Separate packet-cap/missing-frontier refusals must invoke no worker.
Maximum actual mathematical calls: one receipt and two native checks, although
conservative reservation accounting is intentionally larger and failed native
cost is separate from observed-success worker CPU.

Review corrected the pre-close evidence snapshot ambiguity: final primary
owners/receipt_owner reports now follow close; separately labeled before_closure
preserves the old observation. Cleanup errors and expired original deadline
override success, including after final report write. This is source clearance
only; exact built-native/config/runtime selection and actual evidence remain
root-owned prerequisites.

Read the complete fresh authoring.py33,655B
`bf3f266c0ba2e3ebd2079bb33fac067e88f1309172bc3985a2a92c034e58627e`
and authoring_api.md5,657B
`d7da7e974d5a1b7682a9e6445affdb1ef628093e55903a9924790b36405e1d71`,
then compared the actual frozen context/source/NativeRows/model/OwnerPreparation
APIs they call. No blocking source defect identified; no code executed.

DeltaImportSession requires the exact live originating DeltaVerifier and real
registered VerifiedDelta handles. Parsed packet payloads must match the actual
accepted member inventory, exact journal and proof form. Multi-handle composition
conservatively rejects alternative journals, receipt/witness bytes or forms for
the same module. Opened group commitments and supplied semantic body hashes are
bound; the session's operation selection includes original packet identities.

The ordinary frontend receives only selected interfaces and needed semantics,
plus the fixed foundation, through the unchanged request schema. Its absence of
ancestor theorem proofs does not imply their disappearance from onward evidence.
SourceOperation decodes actual export declarations, checks census/root/source/
selection bindings, emits native rows through actual NativeRows.group methods,
and forms a complete untrusted child witness. It does not insert a fake receipt
or an ImportClaim with invented receipt authority into existing receipt-only APIs.

Onward construction traverses exact parents into the accepted closure, includes
every required uncertified ancestor once, preserves actual receipt frontiers,
orders delta witnesses by checked rank and appends the child last. Unneeded
branches may be pruned; missing required material refuses. The same aggregate
packet parser applies; a larger optional Envelope cannot override the narrower
canonical/native codec domain. Child acceptance still requires independent
native/receipt verification, not successful source preparation.

DeltaOwnerPreparation reuses original owner allowances, worker/config/process
bindings and failure accounting. It reserves storage for native export plus full
packet, pins the final saved packet, and uses the original _call completion
callback after report writing/census and before return to revalidate the live
source origin, bindings and deadlines. snapshot() explicitly refuses. Its local
profile must include the actually loaded authoring successor and transitive
source closure. No actual native author run, second-delta admission, reciprocal
network return or v5 release follows from this source-only clearance.

### Native-delta source and build-proposal review

**Actual build01 FAIL; compatibility-review miss preserved.** The single selected
build exited1 with Rust E0432: retained native-library01 has no
`nanoda_lib::parser::decode_corresponded_owned_row`, required by current relation
source. Its preserved parser snapshot contains `parse_owned_rows` but not the
new owned decoder. Thus the earlier hash/overflow/source review did **not**
establish API compatibility; this reviewer should have compared the library's
actual compiled source snapshot with the relation's imports before clearance.
No native_delta.exe exists. All eleven build snapshot pins match. Root and the
source owner now investigate an actually compatible retained x86_64 checker or
a separately selected fresh build; no rerun, budget widening or fallback to an
older relation is implied.

Actual evidence independently checked: build RESULT
`5aeb9c2729feea819d4400a8206308737fa303ca2a55dcc1a807e644f35d8bb0`,
attempt `e7f39f21fa13fb213b9f4357ac0b56a0d89488dfa0bb0fe002f9df21f2d37f72`,
stderr `bfc149a0bc647aa75f248544334095fea152120697781010231d98a77fee4539`.
One command, no guest/proof calls; Job closed with zero active/terminated and no
cleanup errors or telemetry cleanup. Worker0.734375 CPU, peak629,358,592B;
inclusive controller1.703125 CPU and total observed8.0823074 wall. Main and
attempt controller CPU are the same enclosing cost, not additive. Raw failure
is retained even though process containment and evidence closure succeeded.

Separately, the nine structural controls' exact selection
`c8cc86ce63e63daecc421ce90e7c80362eb50a3e207813faecae1969eb066ae1`
was reviewed before launch:12 source+3 runtime pins independently match, fresh
output,30CPU/45wall/512MiB/cap2. Updated test source
`d16c545bd084c10a9183ba7c65c61b840e9a45f66841119efaf36b15a842d1eb`
adds the fractional telemetry regression to the existing ninth group; its
finite-float local report passes while mathematical JSON refuses decimals.
No positive authority/native/cryptographic call is made by these tests. This
was launch clearance only; terminal outcome is now independently reviewed below.

**Actual delta-packet-controls01 PASS (structural only):** all nine named tests
pass with zero failures/errors in retained stderr and inner RESULT. The updated
fractional-telemetry case is included.27 independent post-run hash checks
(12 canonical sources+12 snapshot sources+3 runtime pins) match. The sole Job
exits0, closes/reaps, ends with zero active/terminated, no termination request or
cleanup errors. Worker0.46875 CPU plus enclosing wrapper0.265625 CPU (do not add
its included0.015625 supervision CPU again),1.1253214 wall, peak24,547,328B.
Outer RESULT `df2023331f82673a8d68844fe4d2cf9d98500c69f3d12b555f6e3977ec283ded`;
inner RESULT `a1c7876e53e5baec0e6d73ba7f64cb9bbee49edc7a6cea4dac45adb9826f452b`.
No native/checker/proof call or positive authority exists. Used packet/receiver/
test bytes are frozen; no passing campaign repetition is warranted.

**Fresh native-library02 selection cleared:** exact proposal and copied selection
`7941f68e3615e7bb1119aa0083ce0cc73525e4b8e978f72ab4e596ba446b2cae`.
All27 source and68 retained runtime pins independently match. The26 actual checker
files additionally match both guest05's compiled source snapshot and its
SOURCE-MAP.checker entries; guest selection5da04eb9/mapdf3d2f88 hashes match.
Current parser7a183a1c exports the required owned decoder and parse_owned_rows;
current lib.rs exports parser/module/correspondence modules. This comparison
addresses the actual earlier source/API mismatch, without changing checker code.
The direct rlib-only argv is exactly library01's previous argv (eight retained
externs, overflow=yes/panic=unwind/opt2). Fresh output,90CPU/120wall/2048MiB/cap4;
no linker, Cargo, guest, proof or dependency rebuild. This is prospective build
clearance, not a compiled artifact or universal native/guest equivalence. Driver02
must bind the actual successfully built rlib hash in a separate fresh selection.
The source owner, not this reviewer, performed the disjoint retained-library
census; no duplicate census was run.

**Actual library02 PASS; driver02 prospectively cleared.** Independent actual
review rehashed122 canonical/snapshot/runtime inputs with zero mismatch. Compile
exit0, no stderr, closed/reaped Job, zero final active/terminated, no cleanup
errors.42.53125 worker CPU+1.03125 wrapper CPU,14.1900198 wall, peak444,993,536B.
Actual rlib11,303,166B:
`ba6d0db2e614c2bb032ca5d92d97d31a7ebfe87f85fa6cce6fe5549483b7c651`;
RESULT `916e05e1118a28b289cd2224a06df2fe5a15f30c85be58f8b692ea03add53600`.
No native driver or theorem check follows from this library build alone.

Fresh driver02 source500c6b35 equals reviewed build01 source under only documented
docstring/output/attempt/proposal/self-path replacements (exact byte comparison
after substitutions). Selection
`031f526e5b8077652e85d6b7ffbb84ff8e9db1549f40359345f46e03f5545d66`
binds proposal
`b0d037459b950c3cbabd1c2554aebf1fe9611820598d370eb40f4d69e700885d`.
All183 proposal pins (nine sources+174 runtime/evidence entries) independently
match. The only compiler argv change is the actual new library02 path; its rlib,
RESULT and selection are pinned. Output and attempt are fresh; original
240CPU/300wall/3072MiB/six-active bounds and reviewed telemetry cleanup remain.
One fresh root launch is cleared; failed driver01 remains failed and preserved.

**Exact build01 selection cleared before its failed launch:** final driver
`b84db1f4ff776b3a3fcd0a4396af3a4ea7e50bb28bdb27dfa107b9c38797347d`
and selection
`4b7b64c22f93f207dd60cb2967d46db2e3ca0db57335a8555168d81e4dd91139`
bind the unchanged proposal below. Complete helper lifecycle review confirms
the exact factory installs240CPU/3072MiB/six active despite the adopted Phase
constructor's default call shape. Phase wall240 is within total300; combined
logs1MiB and controller60CPU/output1GiB8192entry sampled bounds remain finite.
Owned VCTIP cleanup validates exact Job membership/image/hash only after direct
compiler exit0; unknown descendants refuse. All final close errors override PASS.
Seven helper hashes, D:\Python314 executable/DLL and VCTIP hash independently
match; output and attempt paths were fresh. Eleven snapshot sources preserve
the relation's source-relative paths. Review requested explicit final-write/exit
tail scope labels, now present in both main and enclosing attempt reports. No
claim of fully hard wall/disk enforcement follows. This clears one compile-only
launch by root, not a runtime success or mathematical admission.

Independent complete source review finds no blocking defect in the new driver,
packet parser and owner receiver, including the actual-closure member API. This
is source clearance for separately selected build/controls, not an executed
positive admission. Exact reviewed implementation hashes:

- native.rs: `66d5c58a99cccab4ffe1c53264fd1ae1eb0941c15dcadff0a54ef2844caa664e`.
- packet.py: `3ebd338998acefa7808695ec4a0f5320d15a6893b8c339243af21afad456c0f3`.
- receiver.py: `418708346600bff17d2a8425fb9ca322d8eeb9e6a0ad97a6d63c5637bd4df120`.
- test_packet.py: `f7b1279b6d9b34dac385b5b1bbb4eb9224eca7b71c3cb59d688006bcc425c27c`.

The native driver calls unchanged relation3625bc9c, encodes its computed journal,
then checks its own image/foundation/policy even for zero-parent witnesses. It
returns computed exact parent journals with explicit conditional-only status.
The owner obtains frontiers only through the exact originating ReceiptVerifier,
checks complete journal-byte equality rather than ModuleID/rank alone, and adds
each computed conclusion only after all parent premises have already been
established. Strict exact rank and topological order prevent circular support.
No-extras/reachability use that actual checked graph. Immutable packet bytes,
same-call input digest, runtime/source pins, original deadlines and real live
frontier handles are rechecked before final promotion. Saved JSON cannot mint
authority; the opaque VerifiedDelta registry is distinct from VerifiedModule.

Members are drawn from retained tuple(graph), not a remote inventory. Their
copied descriptions/openings remain under the one accepted closure handle and
its originating live frontiers; no fabricated receipt handles are introduced.
The complete original packet is retained for a cold onward receiver. Aggregate
packet/receipt/witness/node/depth/row/edge/opening/body budgets prevent replacing
an ancestry limit by a depth-only bound. Attempts, input bytes and conservative
worker reservations survive failures; observed-success CPU is explicitly partial.
Operational telemetry uses the finite-float local parser, separate from strict
integer-only mathematical input and native output.

The nine source-reviewed structural controls create no positive authority and
make no native or cryptographic calls. Actual selected-child acceptance, wrong
frontier/target/proof/body refusal, a second delta and final-lifetime controls
still need concrete evidence. The fixed native parser may impose a smaller
supported domain than optional larger Envelope ceilings; those cases refuse
conservatively, not complete more cheaply. Jobs are resource containment, not
hostile-source isolation, and output sampling is not a hard disk quota.

Build proposal
`bdd23d50c7e45906e84cda6167f1ea6bf73c25a6b4cfae31924674998258d021`
was independently rehashed:9 sources plus172 retained runtime inputs, zero
mismatches. Its65-argument direct rustc invocation targets x86_64 Windows,
overflow-checks=yes/panic=unwind, reuses existing dependencies and checker rlib,
and does not rebuild dependencies, execute a guest or produce a proof. The
retained native-library01 selection also compiled the checker rlib itself with
overflow-checks=yes/panic=unwind; final-link flags alone would not establish that.
Proposed finite build limits240 CPU/300 wall/3072MiB/six active are not enlarged.

The proposal is **not a launch selection**. Root's fresh supervisor must use
reviewed exact owned VCTIP cleanup and finite-float telemetry, preserving the
prior generic build's failed descendant lifecycle instead of repeating it.
Actual compiler/dependency/architecture correctness remains in the receiver TCB;
shared relation source is not a proof of native/guest semantic equivalence.
Current cryptographic profile2 still requires real receipt parents and cannot
seal an arbitrary uncertified delta DAG merely because native checking passed.

### Actual receipt/source integration01: successful prefixes, failed snapshot

Independent terminal review of root session93713 is complete. The overall raw
operation remains **FAIL / exit1**; this is not a child admission or completed
integration. All 37 selected sources were rehashed in both canonical and frozen
snapshot locations, plus all 33 runtime/input pins: **107 checks, zero mismatches**.
Selection6efbbc8e/profilecd7a4bfa/config8199b31a remain unchanged.

The genuine fresh host receive returned `REAL_MODULE_RECEIPT_VERIFIED`, fully
resolved, profile2/current image04/current foundation and policy, rank0, exact
base module2b54d3be. Both copied receipt files (receive and parent-0) equal the
223,594B final base receipt850c33b2. Same-call binding and the reviewed live
verifier/session path support actual base admission, not merely saved receipt
production. All authority was closed at the end (zero verifier live handles).

The actual native author returned zero and exported526 rows / one local theorem.
An independent read-only traversal of the saved export expression DAG, separate
from the harness census, finds the admitted relocated `binary_congr` in the
theorem proof and Tree/fold/map in its statement. Its canonical child has one
group and1355 rows, module
`4adbc049e4d1e29ec045d64c7dba9e27bdd506dfa6c7fb707f022be40439e742`.
Only committed imported interfaces/needed semantics were supplied; imported
theorem proof ancestry is absent, while fixed foundation proof data remains a
separate supplied input. Ordinary-source authoring is genuine selected-interface
reuse; it is still not independent child mathematical admission.

Host preparation returned `PREPARED_ONLY_NOT_CERTIFIED`, rank1. The sole parent
journal in the retained child input equals the full184-byte journal from actual
base receiving. Expected child journal is184B, profile2/current image, one group,
rank1; the frame is retained113,224B. Snapshot then exited1 with precisely
`Session limit exceeded: 33557665 >= 33554432`. No child.snapshot capsule exists,
no child receipt/proof was created, and no child handle was granted. This is a
clean cycle-limit refusal, not evidence that the child relation passed or that
an additional3,233 cycles would suffice to complete it. Do not rerun receipt
admission/authoring or enlarge/restart this failed snapshot by implication.

All four inner stages and the outer Job report zero final active processes,
reaped direct children, closed Jobs, no termination request and no cleanup errors.
The real positive author fits unchanged concurrent cap2 (total process count3).
Selected observations: receive0.015625 CPU/1.8135803 wall; author4.15625 CPU/
30.398877 wall; prepare0.109375 CPU/0.6890074 wall; snapshot2.125 CPU/1.5943692 wall.
The enclosing Job costs13.515625 CPU, peak521,482,240B; outer measured wall is
44.0268633 seconds. Outer wrapper1.0 CPU is separately recorded. The13.515625
already contains the inner worker/controller costs; do not add them again.
Owner allowance closes with2 calls,6.390625 charged worker CPU and known closure.

Retained audit anchors (SHA256):

- Outer RESULT: `76f6fae8a4dbb3aa8f188736933617a050f4ac4867e9d6ca47426c783837adea`.
- Inner RESULT: `54c48e050860bafb98cbe20b16f173f122e1ad3b3c0e134cad3cde26dbfd4282`.
- Actual export: `36278b75e0a12a0cf92d40510730503a49e2285b316ded674c10af0bd7621d2d`.
- Actual source request: `72208ac51a8794b888ac6d37d3f443175753e66c2c9e2fb3e0f42e4bc75d5f10`.
- Child frame: `dade9928001af41562d5471187fd9d149805e98bd6efdd06511b5e6a5a4c9fea`.
- Expected journal: `07734789fd165d5c29667a2925c09b882d346db97a511c75644f2cb4b8ccd0da`.

Disposition: adopt only the successful real-receipt/imported-source/preparation
prefixes and the clean failed snapshot evidence. Retained child input/frame are
untrusted reusable data for a separately selected native-delta path. Full v5,
independent child admission, onward reciprocal circulation and full-cost growth
remain open. No runtime was launched by this reviewer.

Root has now relayed the user's explicit resumption of real v5 implementation.
The guide/pause paragraphs below are historical. This reviewer again owns only
independent source/preflight review and this checkpoint; root alone selects and
runs finite operations or mutates Git. The still-unrun receipt integration author
is finalizing the harness. No frozen owner/worker source is edited by this lane.

### Process-envelope reassessment

Do not infer a required cap of three from a total-process count of two. The
retained base-production audit also records two total processes for direct host
stages, whose command is a single native executable with no Python worker in
that Job. The worker-control harness has no deliberate real Popen outside its
mocked native calls. The source does not identify an additional process or prove
that it overlaps the native worker child. A source successor raising the cap is
therefore not selected merely on speculation.

Recommended discriminator, if root selects it: unchanged worker plus unchanged
native frontend, exact runtime pins, same cap two, one tiny deliberately malformed
owner request under a fresh short finite allocation. A parser-specific native
refusal with direct reaping, no deadline/Job process termination and final active
zero would establish the actual worker/native launch shape fits the current cap.
It need not redo a mathematical control or receive any certificate. The expected
nonzero child outcome must be distinguished from process-limit failure. This is
a proposal, not runtime clearance or an executed result.

### Initial draft findings sent to author

Validate all later-phase finite limits before spending real cold-admission work;
protect producer host/Python/runtime pin paths in output-overlap preflight too;
retain original deadline through final report writes (with a failure override
if needed). Actual imported-source paths and full source closure must match the
root's immutable selection. Final source review awaits the author's corrections.

### Stable receipt-loop source review

Read all of the corrected 21,755B `authoring/receipt_integration.py`, SHA256
`f0d2697fc6e769d93643c2bfd1b1917e324408540aa5a862775fa316e47f4702`.
**No remaining source blocker found for the selected integration scope.** This
is source clearance only: the cap-two worker discriminator and exact complete
source/runtime/profile/enclosing resource selection remain required before root
chooses a launch.

The harness prevalidates all later grants, constructs the exact adopted owner
profile before spending receipt work, protects all producer/runtime/source input
paths, and starts every local lifetime within one nonrenewing outer wall bound.
It invokes actual receive once, carries the exact live handle/receipt into the
same ImportSession, opens the pinned current semantic bundle, captures the actual
prepared request, and uses the same SourceOperation for ordinary authoring. It
then inspects actual exported proof-value closure for imported binary_congr plus
the Tree/fold/map statement interfaces; it does not rely on source spelling.

The sole exact real parent receipt/journal passes unchanged to the existing
parent-aware snapshot API. Result types explicitly remain untrusted child/prover
data, not child mathematical admission. Input pins are rebound, owner/session/
verifier closure is attempted, failures/unknown accounting retained, and a late
final-report write produces a failure override/nonzero exit. Output and work
accounting retain sampled limits and exclude final tails rather than claiming
hard quotas or double-counting nested controller CPU. The enclosing Job must
also be large enough for actual nested worker/native processes and CPU.

### Actual cap-two probe: failed harness, sufficient retained launch evidence

Prospective clearance was for harness
`8261679860ff393f4f718fb967224c1c8e6fc7e67e7f96a3ea72d7c392ce831b`
under selection
`b0254716a6fa7b1a2cadba67456d6a9d8da580992a59c3ae65f30e1941fc26f5`.
Review required the actual BASE cwd/environment (not project-root cwd), explicit
final resource bounds despite expected nonzero status, and exact worker-report
bindings. All three snapshot source and 24 runtime pins matched before launch.

The root's one selected run ended **raw harness FAIL**. The harness called the
adopted integer-only `supervisor.strict` reader on operational telemetry that
contains floating wall/deadline values. It raised NONINTEGER_JSON_NUMBER after
the inner process and worker report had already been saved. This preflight miss
is preserved, not repaired in used source or relabeled as a passing campaign.
The inner harness RESULT was never written. No native output/export exists.

Read-only independent evaluation of **all ten originally encoded predicates**
against those retained artifacts gives true: expected worker refusal, same-call
worker binding, actual native parser reached, native reaped, no timeout, exact
worker diagnostic, no mathematical promotion, clean whole-Job closure, all inner
resource limits, and unchanged inputs. Additionally checked exact deadline
equality and the unchanged inner active-process cap of two. Rehashed every
snapshot source/runtime pin after the run with zero mismatches.

The actual native stderr is `OWNER_AUTHORING_FAILED AUTHOR_REQUEST_SCHEMA`.
Worker records code 1, `WORKER_NATIVE_REFUSED`, direct reaping and no timeout.
The inner Job records 0.78125 CPU seconds, 6.5493266000412405 wall seconds,
28,655,616 peak private-commit bytes, total processes 3, final active 0,
terminated 0, no requested termination, no cleanup errors, direct reaping and
closed Job. These satisfy unchanged 10 CPU / 20 wall / 512MiB / cap-two limits.
Total process count is therefore demonstrably not the concurrent process cap.
The identity of the additional sequential/transient process remains unproven.

**Disposition: sufficient posthoc evidence for this actual worker/native launch
envelope only.** Do not rerun this already observed boundary or widen the cap
merely to obtain a green harness report. Actual positive authoring is still a
separate integration endpoint. The failed run remains charged: enclosing Job
1.453125 CPU plus outer wrapper 0.6875 CPU, 8.306573099922389 outer wall. Inner
Job/controller costs are contained in that enclosing Job and are not additive.

| Retained item | SHA256 |
|---|---|
| Outer failed RESULT | `b700bf6fd2d7844ef8d99a7d1d8290ba5937ae2b52d7ac36a0f7fe204f71f111` |
| Inner process | `1a295c7d8d4bbfa7ca830d7bd229993432940add46abdda440b603841300053a` |
| Worker report | `bbeaf282a4e3882c9259fb3dde067ad722b0f190d664b571830dc7e7b1596263` |
| Worker config | `651d4708bf0a6c7b70e738eed104b8159bb74eba83d079126424d180c17fc46d` |
| Native stderr | `f254442a5f0cd4e1657162086b97a8ac42381718cb0ec903a71a82da06063bf3` |

Source reinspection confirms receipt_integration and OwnerPreparation use
`production.producer.parse`: duplicate keys and nonfinite JSON constants reject,
ordinary finite decimal telemetry is allowed. Their mathematical object readers
remain separately integer-restricted. The probe's specific reader bug is not
inherited by the pending positive integration path.

### Exact genuine receipt/source/snapshot selection clearance

Independently cleared the following bytes after full source and pin review:

- `receipt-source-integration-01-selection-draft.json` SHA256
  `6efbbc8e43a8704b3f8650ec9b21f589180ecd671e6d21c18152109db994b659`.
- Profile SHA256
  `cd7a4bfac290a717f20af1a00d8e6f1a87939ea8ba7d3203b38d21bea291e56e`.
- Configuration SHA256
  `8199b31aadb0ddce3ca0ba683679b793b3bfac404bd0cdce28a4b58ff552f36e`.

All 37 source and 33 runtime/input pins match actual current files; the future
output does not yet exist at review. The profile's 34 Python files cover the
read local import graph (including transport/discovery dependencies transitively
imported by ImportSession). Namespace packages without an initializer require no
invented initializer. The actual Producer/Owner/worker source paths are the exact
future snapshot paths, not same-byte files imported from another location.
Supervisor helpers are additionally adopted through the pinned release manifest.

Known Lean runtime pins include the five shared DLLs and Init.olean, not a claim
of complete hermetic transitive olean/OS dependency closure. Host03/image04,
current-policy semantic bundle, exact final base receipt, foundation and the
ReceivedFoldMap source/roots all match the selected identities.

The outer allowance is 600 CPU / 600 wall / 4096MiB / six active processes.
Integration wall is 540; owner/session wall is 480 clamped to the original
remaining time. Owner stages reserve 30+15+240=285 worker CPU against 300;
controller lifetime CPU is 120. One receive reserves 30 separately. The selected
1MiB receipt-session cap exceeds the actual 223,594B receipt. Native authoring,
prepare and snapshot remain separate finite stages with unchanged inner cap two.
Snapshot is one execution with unchanged 2^25 cycles/po2=18; no warmup or proving.

**Clearance scope:** root may select this one cold-base receipt → same live
ordinary-source operation → one real-parent child snapshot attempt. No new
child certificate, fresh child receiving, network loop or final v5 release is
implied, and no automatic retry or renewed allowance is cleared. All mathematical
and operational outcome claims still require the saved actual evidence.

**Assignment redirected before runtime:** root clarified that the latest actual
human request was the full theoretical architecture guide followed by a pause.
The integration findings below are preserved as source-only notes, not current
implementation/preflight authority. No runtime, source successor or integration
selection was launched. The completed guide review is GUIDE-ASSURANCE-REVIEW.md.

## Scope and current disposition

Independent source/selection review of the genuine cold-receipt → live imported
interfaces → ordinary Lean author → parent-aware child snapshot path. The root
owns all runtime selections, launches, adoption and Git. This reviewer runs no
proofs/tests and changes no used implementation or evidence. Base-production
outcome review belongs to the separate BASE-PRODUCTION-AUDIT assignment.

Canonical workspace guard passed. Read the canonical AGENTS/GOAL/NOW and current
WORK selection; older pause/live entries are history after explicit resumption.
Full v5 remains unfinished. This note is not public deployment qualification.

## Source-derived obligations

1. `ReceiptVerifier.receive` must really invoke the adopted host with the actual
   final receipt and exact image/module/foundation/policy. Saved reports, expected
   journals, snapshots and synthetic handles are not substitutes. `ImportSession`
   must use the exact live originating verifier and exact receipt bytes.
2. Open the current `receipt-prepare-01` semantic bundle, not the old-policy fold
   bundle. Bind its summary to the actual receipt. Open groups and supply only
   committed bodies using public session methods. Foundation proof bytes are a
   fixed separate input; zero imported-theorem ancestry is not zero foundation.
3. The same `SourceOperation` must remain bound to its original session, verifier,
   deadline and selection through native return, `finish`, report/census and
   public return. Existing source and preparation controller enforce these
   boundaries, including final callback and overriding late-failure marker.
4. Actual exported local proof data must reference the admitted module's
   `binary_congr`, and the intended Tree/fold/map interfaces. Source text alone
   is insufficient to prove actual reuse. Derive local IDs/counts from export.
5. `OwnerPreparation.snapshot` serializes exact untrusted child input and separate
   exact parent receipt bytes; the host independently reverifies the parents.
   Its frame/journal/profile/rank/openings and returned capsule/assumption census
   must bind. A capsule is not a final receipt or positive child handle.
6. Final child certification/cold admission, return discovery/availability and
   complete-workflow economics remain distinct unfinished endpoints. Do not
   promote this integration into those claims.

## Process-cap compatibility — unresolved before launch

The frozen preparation controller's `_limits` fixes two active Job processes.
Its author stage starts a Python worker that starts one native frontend. Prior
`author-worker-controls-01/RESULT.json` reports total processes **2** despite all
native Popen calls being mocked; actual `author-lean-controls-01` reports total
processes **7** for the Python runner and five sequential native invocations.
These observations support an additional process but do not establish its
identity, overlap duration or maximum active count.

Read-only review of adopted `operator/commons.py::supervise` finds a direct
`CREATE_SUSPENDED | CREATE_NO_WINDOW` launch, assignment and resume; it contains
no explicit helper launch. The selected Python executable is the normal 106,208B
Python 3.14.6 executable, with no visible `pyvenv.cfg` at its runtime root. This
does not eliminate Windows/runtime helper behavior. No probe was launched.

**Do not clear cap two solely from the intended process graph.** Root may select
one bounded process-tree discriminator, or a separately frozen minimal successor
with explicit author cap three while retaining all other CPU/wall/memory/output/
binding/closure limits. Existing owner source is used/frozen and cannot be edited
in place. A larger cap alone would not establish hermeticity or a sandbox.

## Pinning and environment

- Owner/Producer minimum source lists are not a complete dependency closure. The
  integration selection must pin all actual imported v5 modules and the adopted
  supervisor/runtime inputs separately.
- Producer validates actual imported `producer.py` and `__init__.py` paths, not
  merely hashes at another copy. Owner likewise binds sibling worker and required
  preparation/authoring/module paths. Runtime selection must match actual import
  locations, including any immutable integration snapshot.
- Worker reconstructs operation-local LEAN_SYSROOT and prefixes selected Lean bin;
  its inherited path comes from the adopted supervisor. Known DLL pins do not
  prove a complete OS/olean dependency closure. Owner source remains trusted code,
  not hostile input contained by Job resource limits.
- One outer controller CPU observation already includes nested supervision CPU;
  do not add that CPU twice in whole-workflow economics. Worker Jobs are separate
  costs. Lifetime CPU includes idle owner work; original deadlines do not renew.

## Deferred until explicit resumption

A fresh `authoring/receipt_integration.py` draft is retained unreviewed, unrun
and unadopted. No implementation or runtime assignment remains live. A later
explicit resumption must separately select its full source/profile review and
any finite execution; none is cleared or assumed successful by the findings
above. The current assignment ends with the guide review and requested pause.
