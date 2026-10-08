# Guest-cost diagnosis and semantics-preserving construction repair

Mechanism checkpoint. Root owns runtime selection, SDK partial-trace design,
build/proof allocations and adoption. This note is source/data analysis, not a
new experiment, proof certificate or a claim that the dominant cost is known.
Frozen guest02/image/host01 and their used evidence remain unchanged.

## Actual discriminator

The first base execution correctly prepares the exact new-image frame and
216-byte expected journal, but fails at the selected session-cycle bound:
`33557665 >= 33554432`. It neither produces the expected guest conclusion nor
reaches cryptographic proving. Its clean failed operation costs 2.234375 Job
CPU seconds, 0.40625 outer-wrapper CPU seconds and 7.8061117 outer-wall seconds.
Those failed costs remain charged. The error establishes only a lower bound;
it does not identify the phase or total finishing cost.

Exact image ID is
`d9572ba4c2336c1544cae3fba652cc66f47b70144c4051d3a57dd2e25af161bb`.
The actual 1,461,052-byte image has file SHA256
`3f264ccf30db0f5eb6d33809e1fa9716be0b4270083ef49062536cecf90fc42f`.
These are distinct identities. No new image is implied by a mutable-source fix.

## Where work is repeated

The current guest performs these ordered tasks:

1. Read bounded framed JSON, strict-parse it, and canonicalize once to enforce
   canonical structure/size limits.
2. Canonicalize the whole parsed value again for the committed witness hash;
   deserialize the relation's typed outer structure.
3. Clone/canonicalize/hash the selected foundation prefix; recompute its
   independent canonical-byte hash and semantic foundation identity.
4. Validate local group metadata and compute group/Merkle/module commitments;
   authenticate exact parent openings and body hashes.
5. Reconstruct canonical expression/level trees from native DAG rows and compare
   them with committed descriptors/body openings. This includes traversing each
   new theorem proof to validate its reference interpretation, even though its
   reconstructed tree is discarded and the kernel later checks the actual proof.
6. Decode the same raw rows into native owned records, build the checker arena,
   establish exact imported/local roles, and check every new local declaration.
7. Check each parent cryptographic assumption, validate and commit the journal.

For the parent-free base, step7 has no parent verifications. Foundation
declarations are exact premises, not rechecked mathematical declarations.
`check_declar` checks constructors/recursors' information and ownership but does
not rerun `check_inductive_declar` for every constructor; do not diagnose that
nonexistent repetition. The kernel's inference/equality caches are local to
individual declarations; replacing that lifetime requires a separate soundness
analysis of environments, declaration cutoffs and universe parameters.

Several linear passes and clones are real, but the most concrete avoidable
amplification found is in step5, not a speculative cryptographic bottleneck.

## Concrete repeated-tree serialization

Actual pinned guest dependency `serde_json-1.0.151/src/macros.rs:279` expands an
arbitrary expression in `json!` to `serde_json::to_value(&$other)`. Its
`src/value/ser.rs` recursively serializes a `Value` array/map into a new Value
tree. Thus this expression:

```rust
json!(["app", sub(self, left), sub(self, right)])
```

does not simply move each recursively constructed child into the parent. It
constructs the child, serializes/copies its full tree, and later repeats that
work when constructing the grandparent. The same mechanism appears throughout
`Inventory::expression` and `Inventory::level`, plus reference constructors.

Let `n(v)` be the number of JSON Value nodes below a reconstructed expression
or level node `v`. For child roots `children(v)`, a conservative count of
avoidable descendant-node serializations is

```text
C(v) = sum_{u in children(v)} (n(u) + C(u)).
```

This deliberately excludes additional name/reference copying, scalar handling
and the extra vector wrapper in the constant-level list. For a chain of
reconstruction depth h, the repeated work is Theta(h^2), versus Theta(h) moved
construction; generally it is O(N*h) for an expanded output of N nodes. The
current depth/work bounds stop unbounded expansion but do not remove that
constant-factor amplification. DAG unfolding itself can be exponentially larger
than the number of distinct DAG nodes until the expansion bound refuses it;
moving trees does not solve that separate representational issue.

## Exact held-input source census, not a runtime profile

Read-only analysis used the actual base input with SHA256
`025d2ce3c42cf7eeab00d1e6626d22d59afe495c64232ad2687893eea278d4a8`.
It has 91,311 UTF-8 JSON bytes (91,305 decoded characters), 13,425 Value nodes, 1,072 native rows, 11 local groups,
14 local declarations, 11 body openings and no parents. The 413-row foundation
prefix remains exact. The native rows contain 928 expression DAG nodes and22
nonzero level DAG nodes, including foundation material.

Following each local declaration type, local value/proof and recursor rule in
the source's actual traversal produces these structural counts:

| Quantity | Count |
|---|---:|
| Reconstructed type/body/rule roots |26|
| Expression+level visit calls, expanded |2,289|
| Final reconstructed Value nodes across roots |8,202|
| Conservative repeated descendant Value-node serializations |101,904|
| Maximum expression/level expansion depth, root counted as1 |41|

The recurrence above was evaluated over raw-row DAG references without running
the native checker or guest. The first two substantial roots account for most
of this modeled copying:

| Root | Output Value nodes | Repeated descendant-node serializations |
|---|---:|---:|
| CommonsV5.binary_congr proof |1,645|41,322|
| CommonsV5.Tree.brecOn.go body |1,375|19,527|
| CommonsV5.map._f body |682|7,759|
| CommonsV5.fold._f body |570|6,655|

These are source-operation counts, not instructions, cycles, allocation bytes
or measured speedup. They show a substantial avoidable mechanism. They do not
prove that execution reached it before hitting the cycle cap or that fixing it
alone makes a proof economical.

## Source-only repair and equivalence argument

Mutable `software/v5/modules/native/checker/src/module_correspondence.rs` now
uses a small `tagged` helper to move already constructed children into a single
`Value::Array`. Recursive expression/level/reference branches use that helper;
borrowed foundation names and scalar metadata retain explicit necessary clones.
No visitation, reference interpretation, field/type/body comparison, kernel
checking, error condition or accepted proof premise is removed.

New source: 25,782 bytes, SHA256
`f37c855666480553ee9b95f59dc3ba7ad19316e8e707aacd47fecfa29f1d12e2`.
The unchanged guest02 source snapshot remains SHA256
`8f77984f670a8da23b889059fc4650d7c8bcf43fa21675b0994ffde7cd431597`.
This is uncompiled source pending independent review, not a patched live image.

For each reachable Value v, serde's Value-to-Value serialization preserves v;
this follows by induction on scalars, arrays and maps, with the relation's
integer-only domain avoiding unsupported numeric representations. Therefore
`json!([tag, child1, ...])` and an array containing the same tag and moved
children have identical Value structure. Induction on the expression/level
back-reference recursion gives exact output equality. The child calls remain
in the same left-to-right array order and the same depth/work counter is used.
Consequently every downstream Value comparison and canonical/hash input stays
identical for successful evaluations. Allocation failure behavior may improve;
no resource-failure case is promoted into mathematical acceptance without all
existing validation and kernel checks completing.

This repair avoids rebuilding already constructed descendant trees. It does
not memoize expressions, change the expansion budget, omit theorem validation,
skip kernel checks or reinterpret semantic policy. A rebuilt cryptographic
image nevertheless has a new program identity and requires fresh adoption.

## Smallest discriminating next diagnostic

Root found that ordinary `RISC0_PPROF_OUT` output is finalized only after valid
session termination; repeating the capped failing run with that variable would
not answer the question. Do not select that duplicate run or blindly raise the
ceiling merely to obtain a successful-looking result.

Preferred diagnostic: a diagnostic-only host using the existing exact guest
image and the public instruction trace callback, retaining a bounded PC/cycle
summary even when execution returns an error. Root owns this host/SDK analysis.
Use the same 2^25 cycle ceiling and an explicit finite CPU/memory/output budget.
The changed observed boundary is preserved partial progress, not another
attempt to pass. Sampling/counting needs a fixed cap; do not persist an
unbounded event stream. PC/source mapping is conditional on actual available
ELF symbols. Instruction events are not proof rows or full proving cost.

The decisive questions are whether the capped prefix spends most work in
strict parsing/canonical emission, repeated Value construction/correspondence,
or native inference/conversion. If symbols cannot locate a phase, a small
phase-marker guest is the fallback, but requires a diagnostic new image/build.
Increasing the complete-execution budget is justified only by the resulting
cost decision, not by the existence of a larger host maximum.

If root adopts a rebuilt move-construction successor, first verify exact
correspondence outputs/negative boundaries using a targeted unchanged-input
comparison and the same native relation; then compare bounded guest work or
successful exact journal. Repeating unrelated network, Lean or proof campaigns
would not qualify this repair. Actual proof allocation still waits for a
completion screen with known segments/rows and an independently reviewed budget.

## Direct differential source checkpoint

Root selected a smaller constructor check instead of rebuilding the full
checker. `software/v5/tests/correspondence_move_differential.rs` now includes
the frozen guest02 predecessor and source-only successor directly, requiring
only retained serde/json externs. Full plan/source and all five actual input
pins are in `tests/CORRESPONDENCE-MOVE-PLAN.md`. Harness SHA256 is
`a96000ac637bdcc81b269482dd1332b7e81cf8aa1c5566485c5f68d0032ace7a`.
It compares all normalized correspondence fields across five held new-policy
witnesses and six precise new mutations, including exact refusal payloads.
No Nanoda kernel, Lean/proof campaign or network repetition is involved.
Independent source review and root-selected standalone linking/runtime are
pending; no actual differential success or rebuilt guest is claimed here.

Independent source review now clears the move-based implementation and the
standalone differential's full normalization/guards/mutations. Root requested
a minimal compile adapter, now authored as
`software/v5/tests/build_correspondence_test.py`, SHA256
`8d5cb856ae94290d9614cd10d4196fcfde88fa219c0de252655515e57722c4be`.
The exact compile-only selection is
`experiments/v5-local-checks/correspondence-differential-build-01-selection.json`,
SHA256 `d9e5be9389d38e8a65c5d42884be303b43c91477ec76711d5e9b6dd6639576f7`.
Four source/plan snapshots and a separate predecessor snapshot are preserved.
The reused bounded native/compiler map contains168 files/875733544bytes after
excluding the three Nanoda library/metadata records; only serde/json are direct
externs. No giant cryptographic backend tree is scanned/rebuilt. The result
explicitly does not claim hermetic compiler-search-directory/OS pinning.

The adapter uses the reviewed `phase_class(p,a)` and exact Job-owned VCTIP
cleanup; actual profile is180workerCPU/phase-wall seconds,300allocation-wall
seconds,4096MiB,eight processes,6GiB accounted storage. Required interpreter
is `D:\Python314\python.exe -B -I -S`. A separate attempt record retains
preallocation failures without adding overlapping controller costs twice.
Independent exact adapter/selection review and root launch are still pending;
this lane has launched nothing. Root-owned receipt/host/trace files are untouched.

## Actual standalone build and selected eleven-case check

Root launched and reaped the independently reviewed compilation once. Build01
passes with executable654848B, SHA256
`342e86c233e483e9d59a5c8196c42fad30f355e3b731f7498f14f237f1e7faa4`.
RESULT SHA256 is `33069199722445aa24b44c6490aa757d6cbdba14a44f0293c3b9ec5e609dc1a3`.
Worker CPU13.453125seconds, controller2.046875seconds, allocation wall18.3878463.
Closure is assisted clean: selected exact Job-owned/hash-pinned VCTIP PID10980
was terminated and exit observed, final active0. The raw Job terminated counter
is not evidence of unassisted closure. Zero compile diagnostics; no test yet.

Source wrapper `software/v5/tests/run_correspondence_test.py` SHA256
`539b89cf90d59c47c32b549260ed355113fe1b0ea9828ec5e75361f1fdad3729`
and exact runtime selection `correspondence-differential-run-01-selection.json`
SHA256 `55c5b4d4d486b7dd0e140215d043c56040cc59eb235841f2e85dea87e45b84da`
are submitted for review. The latter replaces the unlaunched2process draft;
root requested3processes for wrapper+native+possible Windows helper, matching
observed analogous runtime. CPU30/wall60seconds,512MiB,1MiB each log remain.
It binds the actual binary/build result, three source snapshots and five exact
fixtures. It performs no build/kernel/guest/proof/network work. Root owns launch.

Root's retained partial trace now prioritizes frontend parsing/serialization
over a move-constructor-only guest rebuild. The separate
[frontend cost plan](FRONTEND-COST-PLAN.md) records precise acceptance-preserving
move extraction, guest-only canonical-pass fusion and foundation encoding reuse.
Important: old derived Input/Parent/BodyOpening accept positional struct arrays
as well as exact maps; a purported equivalent extractor must preserve those
forms. Receipt sources remain unchanged by this lane pending root selection.

Root's actual eleven-case run01 is now visible and passes the selected
structural differential: five full positive outputs equal and all six expected
refusals equal. Job CPU0.3125seconds, outer wrapper0.25seconds, total
wall1.3054235seconds; zero stderr and ordinary clean whole-tree closure, no
termination requested. Four lifetime process creations do not mean four
simultaneously active processes; the selected active-process bound is3.
There are still zero kernel/guest/proof/network calls, no VM speedup conclusion,
and no adoption of this constructor into the existing guest02 image. Sources,
selection and this run's evidence are now used/frozen. Independent actual-result
review and root adoption are separate from this lane's direct read.

## Frontend A/B/C implemented, reviewed source; compile awaits selection

Root adopts the eleven-case actual audit and selects the frontend source plan.
The six-file minimal implementation now exists under receipt/src: new input.rs,
canonical.rs, relation.rs, guest main.rs, lib.rs and bin/receipt_native.rs. Full
sizes/hashes and exact test accounting are in
`software/v5/tests/FRONTEND-DIFFERENTIAL-PLAN.md`. Independent assurance source
review finds no blocker: map/sequence forms and typed leaves survive, public
parse/check retain guarantees, only private check_bound accepts an internal
witness digest, and all native/parent/commit checks remain. No new image exists.

The single focused harness `frontend_differential.rs` SHA256
`06515ba4dd360f1713fc7bd9117bbe1a691458d4a981e42a84bc768b48df421a`
also passes source review. It uses actual retained Nanoda/RISC0, frozen old
canonical and the real new frontend: five held journal cases through both
public entries (10nativecalls),58 extractor cases and25canonical cases. No
mocked hashes and no VM/proof/parent-certificate call. Runtime still unexecuted.

Root approves one-link preparation, not a backend/kernel rebuild. Adapter
`build_frontend_test.py` SHA256
`5426b5b75f3d184b0d3a5b7a4882a5547b6880639d13bfb9cbf335b3cd9776ed`
and compile-only selection `frontend-differential-build-01-selection.json`
SHA256 `55f72087731be6658d518358ed8c97192ce829eba49aa2c846da2d946749440f`
await exact review/root launch. It reuses172explicit runtime pins905860373B and
the old receipt-native link recipe; no claim of fully hermetic transitive search
directories/OS. Twelve current sources/plans plus oldcanonical are snapshotted.
Budgets and owned-VCTIP lifecycle match the reviewed standalone build adapter.

Future runtime wrapper `run_frontend_test.py` SHA256
`28969104d5f59b86f36714053cdf8e194fd1436525f8db0fdbda69180006485c`
is source-ready and submitted for review. Its exact selection must wait for an
actual successful reviewed executable hash; no speculative hash/run exists.
The earlier base input census wording has been corrected:91,311UTF8bytes versus
91,305decodedcharacters; its SHA and structural node counts are unchanged.

Frontendbuild01 subsequently completed under root's launch. Direct actual read:
`PASS_FRONTEND_DIFFERENTIAL_COMPILE_ONLY`, executable1,658,368B SHA256
`04129eb3841ad90ea167728a912a6de690ac7607d805d67d1dbd2ce6d0bc1ccf`.
Result SHA256 `4a640b3e01a7db834fed590d5c2d5aec818ccad9727bbe39293b8f4303cf1d25`.
Worker38.40625CPU,controller2.34375CPU,wall44.9241861seconds. Clean assisted
closure: exact owned VCTIP PID14328 terminated/exit observed; no unknown cleanup
and final active0. This is compilation only and the native wrapper's libraries
are retained, not a guest build or cryptographic completion.

Actual-binary runtime selection is now
`frontend-differential-run-01-selection.json`, SHA256
`5c148cb5b6cf77dfe33683420f09b565233746657954e3295094ad9c8152b94c`.
It binds29runtime files: executable/buildresult,twelve compile-source snapshots,
oldcanonical,twelve held fixture/result/vector files and two Python files.
The existing supervisor and reviewed wrapper are snapshotted separately. Limits
90CPU/120wall seconds,768MiB,three active processes,1MiB each log. Sent for
independent actual-build/exact-runtime review; root owns launch. This lane has
not launched it. Used build inputs/snapshots and compiled evidence remain intact.

Frontend run01 now passed under root's launch and independent actual review.
Result SHA256 `0f43fd2fbe69acfc3352e030904415670315f86530cdb118398d199742fd363c`;
harness evidence SHA256
`5be2a01bb0071decca8d4a15f49c3c5743e223161b5bc215528a289dd953006e`.
All five held216B journals match, with exact pending parent arrays0/1/1/3/2;
58shape and25canonical controls pass. Job0.5625CPU,wrapper0.25CPU,
wall1.6810521seconds; clean whole-tree closure. Still no guest/proof/speedup claim.

Root selects preparation for ONE combined guest03. Exact request
`guest-build-03-selection.json` SHA256
`c45048fd3faf68930271ea2738a6772b5254a6f016a3a1f93f8f4ea4334b4793`
contains40sources521778B and unchanged adopted preparation/finite limits.
Compared withguest02: nine changed source/helper/plan files plus newinput.rs;
constructor move and frontend A/B/C are both included. build_guest.py SHA256
`2770498dff199df622b7473cffae1c8b9b7abbf785ffb0d86eadb46e4309086e`
adds input.rs to the exact wrapper topology and removes only one redundant
initial retained-map computation: first full rebind still computes and checks
it before allocation/copy/commands. All subsequent checks remain. No old-target
or cache-sharing optimization is introduced. guest_graph.py SHA256
`d94bdee15f5d31ae7f868e6a625cf9941985dda01811362d79f9a2a97d970dfa`
explicitly enforces default,std for every serde_json1.0.151 unit before compiling,
in addition to full prior exact graph-delta equality. Plan SHA256
`507cbb593232b52bd1c16fc44c4da219ebcd2af06ecaa85a8432eabf9494aae2`.
Submitted for independent exact review/root launch; this lane launches nothing.

## Actual combined guest03 and assembly02 preparation

Root's guest03 build completed and was reaped. Direct actual read/hash checks:
`PASS_NEW_MODULE_GUEST_CROSS_BUILD_ONLY`; RESULT SHA256
`0f1757b7d5f951205accc9aed507c804f1e547f6b58f26f46170433e3d76f7db`.
Actual ELF1,403,812B SHA256
`195cb9cedebceae3844141f68624a9e3b7140399732f675d29909737db9ad50c`.
Worker193.03125CPU,controller197.59375CPU,wall430.3120324seconds. Exact owned
VCTIP PID15792 was terminated and observed exited; final active0, no unknown
cleanup. This is assisted clean closure. Actual graph passes296vs295units,
zero external changes and explicit serde_json default,std. These are build
costs, not VM/proof-performance evidence. Old guest02 remains unchanged.

Exact assembly02 selection now exists:
`experiments/v5-local-checks/module-image-assembly-02-selection.json`, SHA256
`c7c4e9e332344c30139df6a34edba73016ead615d73d77f9cd6111212fa0a5c9`.
It changes only fresh operation name and guest03 actual RESULT/ELF bindings from
the successful assembly01 selection. Source assembler6e757f...,plan da64ca...,
driver/kernel and120CPU/120wall,1024MiB,two-active-process profile stay unchanged.
Submitted to assurance; root owns launch. No guessed imageID/fileSHA exists.

Root will screen the actual new image using one retained snapshot capsule at
the same2^25 ceiling with existing host02, not throwaway execute followed by a
duplicate snapshot. A coherent capsule is not itself a receipt. For eventual
certified network integration, the retained discovery database has old
conditional policy b49e45..., while the receipt relation uses5edfd0.... Actual
receipt modules require newly constructed new-policy index records; do not
relabel or rewrite the old database. No repeated mathematical or compression
campaign is needed merely to form those new records.

## Image02 failure, measured prefix and existential profile selection

Actual image02 is1,462,580B SHA256
103e9fd4e80b6e6101feb89ebd0724a6010138708f169d9b9eba3b82c7e17f63;
imageID e44b00bbb1c675916d3060b782fec7d1eda742b5f1a4aae04b6a8554b20bbceb.
New snapshot01 FAILED at the unchanged2^25 session ceiling
33557665>=33554432. Root's prefix01 used the same frame/image and retained
host02, stopping at its sample-cell bound rather than completing execution.
Actual131,426exclusive samples include40,515kernel::ecall_sha,21,588write_all,
15,099memcpy,11,510deserialize_any and11,374canonical::emit. These are neither
cycle/wall-time shares nor proof costs. The trace's cycle field is weighted
row points,5,040per row-equivalent. All failures and prior passes remain frozen.

Exact retained backend source explains the software SHA path: M3/version3 is
fixed in execution and segment replay; v1compat uses sha2::compress256 for3.
This corrects the initial mistaken inference of acceleration from guest::Impl.
See [representation decision](REPRESENTATION-COST-DECISION.md) for source costs,
foundation specialization/exact-wire/shared-DAG alternatives and backend caveats.

Root now selects SOURCE implementation of existential journal profile2:
DMKNM002/profile2/184B, DMKN_CERTIFIED_MODULES_V2, omitting witness commitment
but retaining every mathematical check and exact recursive parent conclusion.
This lane owns mutable receipt Rust/Python and focused differential preparation;
root owns admission/harness integration; assurance independently challenges.
No foundation specialization, backend migration, new build/runtime or cap
increase is selected by this source decision. The whole goal remains open.

## Profile2 source ready and focused one-link preparation

Implemented only in the selected mutable receipt source:

| File under modules/receipt | SHA256 |
|---|---|
|src/canonical.rs|23ca5fa1bfe536db08136bef9956426e4d43e90fa36d00a1886e97eef6892d9b|
|src/relation.rs|08cc326b096a36208dd6c3a1fd1919e42e4cbc5938ad31eb875fbe946ca482f8|
|src/journal.rs|1a49bdf52fd38852dafb44ecbae772d0aad2456870ed046b15acabcc0c18dbe1|
|src/bin/module_host.rs|1e30b0f2b8aee2dc26af8520172d64fd9a51ac8bebd3243b43ed0562d5cbbbe6|
|src/bin/receipt_native.rs|f1d3a947f484d75276744eb98aa80df48d07580c52320e014147faebe7d9965b|

canonical_size adds an exact nonserializing counter and parse_validated retains
strict parse plus every global canonical bound. Public parse/canonical/hash
remain unchanged. Root approved explicit host capsule3/checkpoint5 and
DMKN-MODULE-SESSION-V2/SNAPSHOT-V2. Python witness helper and current receipt
README/integration contract use184B/profile2 and explicitly existential semantics.
The old native_controls.py and every used test snapshot remain frozen profile1.

Fresh focused test source existential_differential.rs SHA256
e793274c42e0b675ff02dac7321a71203f41222d8ecacd05c6fe6793bdadb8bb
has five held native-journal projections(TESTONLY, not receipt migration),
two different checked theorem proofs yielding the same conclusion, false-proof
refusal, other changed-boundary refusals and183size/parser comparisons against
the independently pinned guest03 canonical source989c2695.... Plan:
software/v5/tests/EXISTENTIAL-DIFFERENTIAL-PLAN.md. No test has run yet.

Prepared build-only selection existential-differential-build-01-selection.json
SHA2561f9b8cda850609ce7991cdc63d6282e550a7bcd457ff74927ec9186e43db67f3
uses a fresh narrow successor of the reviewed native one-link adapter. It
preserves exact retained compiler/runtime map, finite limits, snapshots and
owned-telemetry cleanup; no backend rebuild. Independent review/root selection
are pending. Runtime wrapper SHA256
0bdfd78f00bdfbe00b3dde268915bb71ead0e902cb3c594c1963ed7aa8a62274
is prepared, but actual binary/runtime selection cannot precede a successful
reviewed build. No runtime or budget renewal was launched by this lane.

Source review of root's SnapshotExistentialScreen.py finds its changed-boundary
logic consistent: exact parentless old seed becomes a NEW relationV2 input, exact
actual image/frame/184B journal independently checked, capsule3 stage bounds,
and no provenance/certificate assertion. Actual new host/image pins and outer
process containment remain prerequisites; source agreement is not execution.

Root subsequently launched the independently cleared existential differential
build01 and reaped it. Actual PASS executable1,584,128B SHA256
e7eb402083dd1d575021afd25d27a7e5790e77772d4db0d105e5c6eb4cecb1c0;
RESULT SHA2566b8ddce19eb8d8605137812f5529e1596a6b247321da7b5b407961ff50902519.
39.46875JobCPU+2.40625controllerCPU,53.2810252wall. Assisted clean closure:
exact owned/hash-pinned VCTIP PID14568 terminated and exit observed, finalactive0.
This is native harness compilation only, not an actual differential or proof.

Actual-binary runtime selection existential-differential-run-01-selection.json
SHA256dd8ef8511b131e134688fd7b2f011620297bfbdc2a626fdc0734d38c6a1fd6e3
binds27runtime files: actual executable/result,12compile-source snapshots,
frozen guest03 canonical,10held fixtures and2Pythonruntime files. Supervisor
and wrapper are separately snapshotted. Limits90CPU/120wall/768MiB/3active,
1MiB each log. Submitted for independent actual-build/runtime selection review;
root owns launch. Expected13relation/8native-reaching calls are source-derived
invocation counts, not independently instrumented kernel telemetry.

Prospective source selections also prepared at root's request, no launch:
guest-build-04-selection.json SHA256
7bbce637f3fe89e3b55eef5271e81c7702eedf2fa79ac5b3f4ab825ba569e0f0;
module-host-build-03-selection.json SHA256
a855e500d992592d1569ae8b04d02b8e31594f3a149bd2b6cca627ec849c0920.
Guest40files525380B has exactly four receipt source changes plus guest plan;
checker/backend/dependencies/build adapter/budgets unchanged. Host8files has
profile2 host/canonical/journal plus fresh03adapter paths/plan; same native
link/runtime maps and600CPU/900wall profile. No metadata/library/backend rerun.
Both launches await actual differential pass and root/independent adoption.

## Actual differential fixture failure and narrow continuation

Root's native differential run01 FAILED, preserved RESULT SHA256
d9a9a57033ca24ac46d4d000e66bb17769be6815cbd6f50d7d1a42b9d3eeeb93.
0.40625JobCPU+0.25wrapperCPU,1.4709967wall, clean ordinary closure. The failure
is parser.rs120 `Attempted to insert duplicate Expr`: the test appended bvar0,
already present at native expression index1. This is a correct parser refusal,
not a production defect or failed mathematical soundness check. All five
diagnostic input files were saved after their exact projected conclusion,
summary and parent assertions; independent actual audit adopts only these
scoped successes, not overall PASS. All old source/build/run bytes stay frozen.

Root selects a fresh narrow continuation, NOT another five-case campaign.
existential_continuation.rs SHA256
25d39621dbf161f7aa52f15ecff2c648ae349991999f483df844f9a03e988af4
reuses exact-pinned five saved inputs and independently held original fixtures.
It interns bvar/lambda/app nodes by entire constructor payload excluding ONLY
ie. Existing accepted raw indices correspond one-to-one to native structural
Expr entries; Lambda equality/hash include all binder presentation fields.
Appending uses continuous next indices; all child references already exist.
No parser or production change. Direct base Value-entry assertion remains
because no separate earlier success marker was retained for that entry.

Remaining planned calls8relation/3native-reaching(source-derived),4new layout
refusals and183unexecuted size/parser controls. The five prior positive native
checks/old-layout refusals are evidence reused, not rerun. New plan:
software/v5/tests/EXISTENTIAL-CONTINUATION-PLAN.md. Build-only selection
existential-continuation-build-01-selection.json SHA256
e3e544ded09642c1845f77b79ebfba04475834dca5463c10faf6334ccb767dda
pins12sources with unchanged retained link/runtime/limits. Fresh runtime adapter
SHA256392b78ddab85e8fa3f80d70d03501f78e602b8c0a97989858f8f8cf41adc83ca
binds prior failure/result and5saved inputs. Exact actual-binary runtime remains
pending. Guest04/host03 source selections remain unchanged and unlaunched until
actual continuation success and independent/root adoption.

Actual continuation build01 PASS:1,573,376B executable SHA256
a5e1426234ed619b75657add751e6f2b005ffc1bbb33cf383dad1ab61f115790;
RESULTcfd66405fc446c6608d2b69572fc162369f90556861ccb1a92b7f4c910216e11.
35.90625Job+2.1875controllerCPU,41.6672125wall. Assisted clean closure:
owned/hash-pinned VCTIP10980 terminated with exit observed, finalactive0.
Exact runtime selection719190a59e4c039b382ac871a6c545164ba1476dbac5875915be7cd3b9bd676d
pins33runtime files, including prior failure and5saved successful inputs.

Root's actual continuation run01 now PASS and directly inspected: five prior
cases reused; alternate actual checked proof shares the184B conclusion; all
six relation refusals, four remaining layout refusals and183validation controls
pass.8relation/3native-reaching are source-derived invoked counts, not separately
instrumented checker telemetry. Outer RESULT SHA256
555e50e579882cf96a8a6e5f9f14f27038a7cc774a6bf7ee07d3ec55cf2e8f79;
harness RESULT SHA256e1a95d502aa6248f01a30d9e849fd116ad2255cdc838ca883df28833ace7398b.
0.515625Job+0.21875wrapperCPU,1.5206948wall, ordinary clean closure.
Independent actual adoption follows root's request. Original duplicate-fixture
failure stays FAILED, not rewritten. Guest04/host03 selections remain exact and
unchanged; image03 assembly preparation waits for actual guest04 artifact.

## Actual profile2 builds and next retained-work decision

Native continuation has independent actual adoption. Host03 actual PASS:
66,652,160B executable SHA256
74a58215351a641d9efbbffbc389b5faea350c46f5c1e1a48bf76cf77b99d6c9;
RESULT6e01679707da8d58e286f7c756e698b1870aeab250d3bccda7a9099e1b8344e7.
105.625JobCPU plus19.1875main-controllerCPU,213.198wall. Outer attempt19.203125
CPU includes main; do not count both. Owned VCTIP23988 exit was observed during
assisted clean closure. Guest04 actual PASS, root reaped session75557:
ELF1,404,960B SHA256
7d06d02fff4568e73b05313b3b68ea8b832ad80db3024ba833501acb0d6cd4fa;
RESULT609a78318d69fb7e50d36b7e8caf915cb6f5c2cf587893862dbc195b131dfd1c.
197.609375Job+203.640625controllerCPU,439.4432559wall, finalactive0.

Fresh assembly03 selection SHA256
fd620fce1df09b871217dd72056a4dea77b2a4f734d288811f96530df7caa3b1
uses the same unchanged assembler/kernel/adapter/plan and120CPU/120wall/1024MiB
as02, changing only allocation and actual guest04 result/ELF. Root owns launch
after independent actual build/selection review. No new image ID is invented.

Saved guest03 prefix/source ordering supports materially earlier downstream
arrival, not a completion prediction: strict parsing precedes old whole-witness
canonical/hash (roughly row-equivalent windows3..13), then fixed foundation
hashes, module/group commitments, body hashes, correspondence and native parse/
checking. Profile2 removes the first91,383B serialization and1,429SHA blocks;
a nonserializing validation walk remains. Prefix ends amid commitments with no
native-tail bound. Neither exclusive sample proportions nor weighted row windows
establish padded-session savings or native completion before2^25. No new trace
was run to repeat this source inference.

Root selected source-only preparation of ONE retained-segment0 calibration,
not a proof campaign: `modules/receipt/calibrate_segment.py` and its adjacent
SEGMENT-CALIBRATION-PLAN.md. Exact actual capsule/host/image/input/result hashes
and root runtime selection await successful snapshot. Uses the unchanged owner
supervisor directly,1500JobCPU/300totalwall/4096MiB/60controllerCPU; small-check
supervisor remains unchanged. Capsule3/checkpoint5, zero guest executions,
one cryptographically checked segment retained for later composition. Source
review pending; successful checkpoint is not a full application receipt.

The source-only public bridge contract is now
[VERIFIED-IMPORT-AUTHORING-CONTRACT.md](VERIFIED-IMPORT-AUTHORING-CONTRACT.md).
It separates operation-local live-handle dedup/exact parent construction from
the real missing ordinary-Lean import frontend. The latter must reconstruct
selected definition bodies and whole inductive groups; current hardcoded
workload exporter is not a general public authoring seam. No bridge implementation
selected. Proof-stage note now explicitly defines gross delta, same-unit costing
and equal native/cache endowment, as requested by independent assurance.

## D17 combined structural repair: source complete, no build/run yet

Profile2 snapshot02 still failed at unchanged2^25; no retained capsule exists.
Current-image prefix02 reached correspondence and native row deserialization,
with substantial outer flatten/Content work, so root selected A1+A2 together.
The earlier hash-only suggestion is not current selection. Authoring and
segment-calibration runtime remain held; first complete capsule is prerequisite.

A1 adds receipt/src/foundation_static.rs and generated foundation_data.rs.
Exact compiled-tree comparison removes two foundation SHA passes plus ONE
shared serialization/clone, checking all actual values/lengths/keys. Actual
rows still reach unchanged correspondence/native construction/checking. Source
generator matches exact83,565B file SHA256
ed450bccfc23fa613bb0c8a8bd3c9ba67ab8477c1d59bf5c1eb5c11cf05423ab.
Pinned original input025d2ce3... yields413rows/23,313canonicalbytes,
SHA736792e5..., FoundationIDd931d114.... This source-generation check is not
compiled runtime evidence; the runtime wrapper also verifies reconstruction.

A2 adds parser::decode_corresponded_owned_row: zero/one canonical boundedu32
index plus singleton variant uses unchanged inner enum decoding, other shapes
use unchanged general decoder. Original decoder, enum, text parser, apply_row,
duplicate/backreference guards and kernel are byte-unchanged against guest04;
only diagnostic Eq/Debug derive and the additive function differ. Relation
uses the new function after correspondence. Metadata variants, positional
payloads, ignored all, and BackRef aliases are explicitly tested.

Source-only focused plan software/v5/tests/STRUCTURAL-FRONTEND-PLAN.md and
structural_frontend_differential.rs compare every row of five retained profile2
inputs; no kernel rechecks.421foundation mutations,12extraaccepted rows and
21irregularboundary controls. Reconstructed compiled foundation must equal
held Value and canonical hash; runtime wrapper independently checks original
domain-framed FoundationID. Neither source equivalence nor this test implies
VM completion or speedup, much less a compact-DAG solution.

One-link build proposal: structural-frontend-build-01-selection.json SHA256
5dfbb967879562df74c1a24fdab9d5241ba69571ea5742343ae5d6287662a45e,
31sources537,991B,180JobCPU/300wall/4096MiB/8active/6GiB combinedreserve.
Adapter build_structural_frontend.py reuses reviewed owner Job/telemetry
lifecycle and retained eight native dependency rlibs, no --test/backendlink.
Independent source review is underway; root alone selects/launches. New
run_structural_frontend.py has no exact runtime selection until actualbinary.

Host03 all8 selected sourcefiles are still exact, selectiona855e500...;
module_host.rs includes only canonical,commitments,journal,policy,trace and no
changed relation/parser/static source. Reuse actual Host03 binary/result/runtime
binding; no relink needed. Guest05 requires a fresh builder/plan admitting both
new include dependencies; used build_guest.py and predecessors stay frozen.
Stable ModuleIDs do not waive exact image match for recursive assumptions.

Focused build01 actually FAILED at retained-rlib LLVM bitcode linking before
tests; no checker/harness result. Root identifies missing original LTO flags.
New build_structural_frontend_02.py adds only retained lto=fat/embed-bitcode=yes
plus fresh02 paths; selection439e3df1a7a5e4f259de6f397156aea0c295e79944833123f7099647645e330c.
All other30selected sourcefiles are preserved. Used01 remains unchanged.
Runtime adapter remains unused and now targets actual02; no binary invented.

Guest05 preparation is prospective/HELD until actual focused differential:
selectiona00c36bee72b16edeb12465163686f2e3630e59da1f9eae111a431530eb7579a,
43sources611,653B; fresh build_guest_structural.py admits both include files
and snapshots renderer without modifying used build_guest.py. Host03 reuse
and unchanged future2^25 snapshot ceiling are explicit in its fresh plan.

Root separately requests source-only selective-certification investigation.
[DELTA-FRONTIER-NATIVE-SEAM.md](DELTA-FRONTIER-NATIVE-SEAM.md) identifies actual
check_bytes/returned-parent-journals plus checked_receipt integration, aggregate
uncertified-closure limits, distinct VerifiedDelta authority and the important
current limitation: profile2 does NOT already batch-seal an uncertified DAG.
No implementation/runtime is selected by that source note.

Actual build02 PASS, root session31949 reaped:962,560B executable SHA256
8a14b0fe25f328f6b73ebcb12f9f05838752679edce91610a6203fab0b5c8a5f;
RESULT995b3f873652722634438fed90dab9adb33f4760375144ea2948ff90644c6399.
21.515625Job+2.3125outercontrollerCPU (includes2.296875main),28.0071mainwall.
Owned VCTIP29736 assisted cleanup observed exited, finalactive0. Root alone
launches exact differential runtime selection8987f8919d619be3d83100880b312e10f3f00d83073020bc50e3f7f0cf59d5b0,
40runtimepins30CPU60wall768MiB3active. Actual run/audit remain pending here.

Actual structural-run01 FAILED at genuine parser-domain difference: positional
`const:[0,[]]` passes old flatten/Content but direct Value enum rejects a sequence.
RESULT064a59718ccd3ed05a7b6c22f14dc025d4c1f5740ad5109d68f54a372bbcc33f;
0.359375Job+0.25wrapperCPU,1.5843935wall, clean closure. Retained stderr
a9591b55d168d41fc98982e50b998b4e1d542dcfc707cb61014ee9e76045dc03
identifies the fourth extra; prior five held rows/foundation421/first3extras
finished in straight-line source. Reconstructed foundation23,313B survives.
No native/VM/proof call occurred; original run remains FAILED.

Root selects fresh dev-parser successor: direct path only when no outer object
value is an array; every array payload uses unchanged original decoder. Parser
SHA7a183a1c9e6ff3ee2c32ee6542ed85d3de0835b00e235f80f6982c3e7038d218.
All used snapshots preserve the previous32a6da12...parser. New focused harness
structural_frontend_continuation.rs runs9remainingaccepted,6arraydomain and
21unreachedirregular controls; source plan STRUCTURAL-CONTINUATION-PLAN.md.
New build_structural_continuation.py SHA9bdf244642e6aca020ca765d7fc4b577b97b2eeda47bee3833a95bfbfbcb9246;
selection9ac06819bc60ee22d4326a119d99a08b8d448ba858256d2f8239104f7ce67ce8,
same finite180CPU/300wall, retained fatLTO/embedbitcode, freshallocation.
Independent review pending and root alone launches. Guest05selection now STALE
because parser changed; do not launch it. Runtime continuation wrapper is not
yet authored; it should pin prior actual failure/stderr/harness/parser/foundation,
verify reused canonical+framed hashes, and bind actual fresh continuationbinary.

Root requests source-edit HOLD for safe initial local Git baseline. Mechanism
checkpoint complete; no additional code edits/runtime until root resumes.
Delta-frontier note independently challenged and incorporates actual-returned
edge closure checks, charge-all-submittedmaterial and explicit nativeTCB/profile
broadening. It remains source-only; first real capsule/receipt remains central.

Git baseline7e2c038 plus safeguards2f9be5f are root-owned; sourcework resumed
after canonicalguard/newAGENTSread. Mechanism performs no staging/commits or
other Git mutations. New unused runtimewrapper
software/v5/tests/run_structural_continuation.py SHA256
1422228e51cce1d9d3d1d2f9a99e9a8ec1cb54a904ae14bcacf9c6223fe9cb8b
rebinds all40 prior runtimefiles plus actualfailure/selection/stderr/foundation,
requires preserved overallFAIL and exactconstpanic, verifies raw+domainfoundation
hashes and only invokes fresh9+6+21continuation controls. Source/ASTcheck complete;
independent review pending. Exact runtimeselection awaits actualcontinuation
binary; buildselection9ac06819... unchanged and root alone launches.

Root actual continuationbuild01 PASS/reaped12594:794,112B executable
f6a9719449143899466e2591933491e2ffaaf7ffd8c6b223d844a231e30ee949,
RESULT4c28caa27942523cb888e3ff825dc2ff4229151e349624f1d489567a86b80058.
21.84375JobCPU+2.421875outercontrollerCPU (includes2.40625main),27.6649845mainwall.
OwnedVCTIP17724 assistedcleanup exitobserved; finalactive0. Exact runtime
selection86ec833d93226e349a4525a8caaa1f3d5aa333e2602c4ca1720008c35d241bbb,
77runtimepins30CPU60wall768MiB3active, independently submitted; no launch by
mechanism. The staleguest05selection remains held until actual continuation.
Root's native-delta profile challenge is integrated: EVERY computed own Journal
must match adoptedimage/foundation/policy, including zero-parent deltas.

Actual continuationrun01 PASS independently adopted by root. OuterRESULT
7cfd5d5497a2a267e84c051d2ded86a8d50400243e6f10f3f738b8c3b160ffd5;
innerRESULT8778b688e49e995f8aa22556010388c1c1c9453aca29909d4d9993d91bc8a501.
9remainingaccepted,6/6arraypayloadcontrols,21irregular(9acceptedbyboth),
zeroKernel/VM/proof;0.265625Job+0.25wrapperCPU,1.2481846wall, ordinarycleanclosure.
Fiveheldcases/421foundation/first3extras were reused; oldrun remains FAILED.
Fresh guest05selection guest-build-05-structural-selection.json SHA256
5da04eb9fa61bb667efa2afe35157a86a2bfde6be05a3c0f64f7fc99e27fb74a,
43files612,640B. Only repairedparser7a183... and updated unusedplan57bcc68...
differ from staleproposal a00c...; freshbuilder6c082359... unchanged. Root owns
launch after independentexactreview; mechanism now prepares reusable generic
image/snapshot seams source-only, with no fictitious actualELF/image pins.

Full source read confirms no new assembly/snapshot adapter is needed.
Use frozen assemble_guest.py6e757f... and original IMAGE-ASSEMBLY-PLANda64ca...;
fresh module-image-assembly-04 selection changes only runname and actualguest05
RESULT/ELF paths/pins,120CPU120wall1024MiB unchanged. Then reuse frozen
SnapshotExistentialScreen.py51ac22... and its exact seven helper sources;
fresh module-base-snapshot-03 selection changes only runname/actualassembly04
image+inner/outerRESULT paths/pins and actualimageID. Host03/profile2/heldbase
input unchanged;240CPU300wall2048MiB,2^25/po2=18 unchanged. No new source,
duplicate plan, placeholder selection or assumed imageID is necessary. Root
alone launches after actual-output binding and independent review.
