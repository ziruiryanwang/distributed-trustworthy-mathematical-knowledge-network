# V5 implementation decisions

Root, 2026-10-07. Full obligations in PLAN remain open. These decisions move
from source/theory investigation into implementation without relabeling v4.

## D01: one evolving implementation, immutable run evidence

New implementation belongs in `software/v5/` under the canonical root. Do not
fork another entire product tree for every small edit. The development tree is
mutable; each selected consequential run must retain exact source snapshots or
an immutable revision plus hashes, its inputs, command, resource bounds and
fresh result location under `experiments/v5-*`. A test result applies only to
the exact selected source. Preserve failed runs; fix development source and run
only the changed boundary. All predecessor used source/product/evidence remains
frozen. No old allocation is restarted.

## D02: distinct module relation, not a v4 trust flag

Adopt authenticated demand/miss/restart as the implementation direction,
subject to the precise MODULE-RELATION and independent ASSURANCE review.
Imports bind declaration kind, universes, type and computation metadata; a
missing transparent body is an unresolved demand, not opacity or an axiom.
New declarations cannot enter the imported-skip-check branch. Certificate
verification must establish the new relation, not merely endorse a sender's
manifest. V4 certificates cannot be relabeled as v5 module certificates.

Initially author and test the pure protocol and native checker boundary before
launching expensive prover builds. Cryptographic integration, Lean
correspondence and production isolation remain release-critical, not deferred
away by that order of implementation.

## D03: separate discovery protocol

Adopt a separate v5 index/store, leaving the frozen v4 exact-type find protocol
unchanged. The intended query predicate is a bounded conjunction of versioned
formal features over a named snapshot; richer ranking is advisory. Candidate
validity, feature extraction correctness, index coverage and network coverage
are distinct outputs. Partition commitments and examined-posting witnesses
must support the coverage claimed, including nonmatching anchor entries.

Selected v4 recipe adapters may seed tests, but their small import/lowering
caps do not define v5's module language. New certified declaration interfaces
need their own adapter. No mathematical proof or whole library download is
required merely to index an exported declared type.

## D04: growth workload and strong baseline

Adopt GROWTH-WORKLOAD.md. Root owns `software/v5/workloads/` and cost/selection
instrumentation. Mechanism owns `software/v5/modules/` when its exact source
plan is approved. Scale owns `software/v5/discovery/` when its contract is
reviewed. Reviewer owns independent review records, not implementation it will
then certify. Do not claim growth from easier representation or a handicapped
baseline. Fixed sharing/certification costs must be amortized by justified use.

## Current runtime selection

No v5 build, network or proof-generation campaign is authorized by this record.
Root may select bounded pure tests and ordinary Lean source checking after
reviewing their inputs/commands. Source authoring for the workload is selected
now. Root has fully read/adopted both contracts and ASSURANCE; module/discovery
source authoring has begun under the stated owners. A next actual native checker
source slice is selected under `modules/native/checker`: bounded exact copy of
the predecessor crate's source/Cargo/license files (no caches), recorded input
hashes, then apply_patch edits for original-kind body demand, imported/new roles
and local cutoffs. No native build is yet selected. External publication,
license choice and remote deployment remain unselected.

## First actual result

Ordinary Lean workload checking: fold-fusion-01 failed on the unavailable
library helper `congrArg2`. Source/evidence preserved. Fold-fusion-02 replaces
only that dependency with an explicit equality-elimination lemma and passes
with no diagnostics, clean Job closure and 0.890625 Job CPU seconds. Independent
source and actual review are in ASSURANCE. This is the new workload's native
identity check, not v5 module certification, network integration or net growth.

## D05: actual module/discovery boundary integration

Root adopts the actual compile01 metadata pass and native-rows8/source-rows7/
export-discovery6/search-session7 focused passes, with independent audits in
ASSURANCE. Lean owner export04 produces the actual fold/fusion dependency rows
after preserved memory/API/initializer failures01-03. Next native execution
will use empty permitted-axiom list (the workload exports no axioms), exact
module-role inventories, complete inductive groups and explicit conditional
premises. A diagnostic NEED status is not success merely because exit code is0.
No synthetic receipt digest establishes admission.

Select source implementation of a small bounded read-only v5 transport plus
typed durable group/body custody under scale ownership; read/adopt the concrete
DISCOVERY-INTEGRATION recommendation. Frozen v4 wire limits/identities cannot
silently carry the new module protocol. Root supplies the actual pinned workload
bundle. Local provider tests remain loopback-only; internet deployment, actual
module certificate discharge and hostile-input isolation are separate gates.

Root may select one new library/native diagnostic binary build after source
review; it will reuse pinned retained toolchain/dependencies without Cargo or
network. Each operation retains fresh immutable inputs/results and finite
resource supervision. This does not authorize a guest or proof campaign.

## D06: actual native seam and exact foundation adoption

The original40-declaration workload and independently compacted22-declaration
foundation pass actual all-new native checking with an EMPTY axiom list. All
five corresponding-module requests pass their expected conditional status:
base14 local declarations, then fusion/fold_map/fusion_map/project_summary one
local theorem each. Imported theorem proof bodies are not supplied by the
producer fixture. Seven independent native controls pass body/declaration
demands, exact restoration, false-new-proof refusal, descriptor mismatch,
malicious local skipping and partial-inductive-role rejection. Exact source,
input and results remain under native-positives01/native-controls01.

Root adopts the exact compact foundation for the first v5 semantic profile:
foundation.json SHA256
`736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c`,
413 raw rows,22 declarations, no axioms or quotient primitives; candidate
foundation hash `d931d114155cf3cf0dc0b868aa88c6d38b8ada8ecafe267a5934934075782481`.
This follows independent native-output/census auditing, not file identity
alone. It is not a claim of full Lean/Mathlib correspondence.

Select source-only real module receipt-wrapper work under mechanism ownership.
Long-term semantic policy excludes verification-performed state and image
identity; the acceptance profile separately binds checker, cryptographic image
and migration rules. The fixture policy marks unperformed certification, so
strict-policy ModuleIDs must be recomputed, not relabeled. Actual receipt
verification, rank descent, group/body hash equations and foundation/profile
binding must replace every unresolved synthetic premise.

Native-binary01 failed linking retained LTO-only dependencies. Binary02 linked
with compiler exit0/zero diagnostics but required descendant termination; its
build lifecycle remains FAILED. Independently reviewed produced executable
`90ca34afa0da078a4fe843dbfa1eba809665037b183ce8d5979d18fb19d62236`
was separately selected for actual passing diagnostic checks. No repeated
compiler campaign or relabeling was necessary. Release build lifecycle is open.

## D07: functional discovery is not yet economical indexing

Provider-contract01 passes5 actual loopback/SQLite controls. Discovery-network01
passes actual symbolic theorem/equality query over18 exports: first index stops,
four more pages come from another provider under the same snapshot, fusion's
typed locator resolves, its type supplies the owner of fold, and a restarted
custodian returns the committed fold body. This is same-host transport/retention
evidence, not independent hosting or mathematical admission. Actual query body
traffic is105,068 reply bytes and2,947 request bytes; six requests. Whole setup
plus operations cost44.1875 Job CPU seconds,49.8023 wall seconds.

Each18-export index occupies28,975,104 SQLite bytes. This observed amplification
is a CENTRAL growth/service-cost issue. Scale is redirected from public CLI
design to source-backed and retained-state diagnosis of the sparse256-bit map,
then a concrete bounded cost repair. Do not rerun the whole passed network
campaign or claim that asymptotic corpus locality alone makes this deployable.

## D08: central physical amplification repair and receipt diagnostics

Root reads/adopts DISCOVERY-INTEGRATION's compressed-map design. Select scale's
source implementation in authenticated_index.py/discovery_store.py and focused
tests: fresh V2 physical stores, canonical maximal authenticated runs, unchanged
logical sparse-map commitments and wire proofs. Existing databases stay frozen.
One new 18-export index must reproduce all 19 retained snapshot roots and
query/proof bindings, with a prospective >=90% physical-size reduction against
the exact 28,975,104-byte single-index baseline. The old 44.1875-second whole
network operation is NOT a matched single-index timing baseline. Wire summary
amplification remains a separate next boundary. Root selects runtime after
source/selection review; no unchanged network campaign is repeated.

Mechanism owns the native diagnostic of the real receipt relation and updated
semantic-policy fixtures. Assurance owns independent cross-language and refusal
vectors. Native diagnostic success never discharges parent cryptographic
premises. No guest/proof operation is selected by this entry. Small warm-module
checking costs also do not support a receipt speedup claim: sharing, useful
methods, and succinct verification require separate comparator accounting.

## D09: actual binding/storage results and next central implementation

The same-source receipt native wrapper compiled with rustc exit0 and zero
diagnostics, but again required descendant termination. Preserve build01's
FAILED lifecycle (43.03125 Job CPU seconds); no repeat build was selected.
After independent exact-artifact review, its 1,474,560-byte executable
`8a688b45f5a1a495d48fd4b2aa869fd923d99940c8622cc55faad9eeb3e67f07`
was separately used for actual diagnostic checks. These are not certificates.

Parallel controls completed cleanly: compressed-map6 contracts (0.84375 Job
CPU), receipt cross-language10 calls (0.46875), new-policy five-module wrapper
preparation (1.171875). Nine distinct binding-negative calls also passed
(0.515625), reusing the retained successful fusion output rather than rerunning
it. The semantic policy is
`5edfd0ee15b141b7304e26c1a39cd11f7f7e721713cf099813ae4f4442fad377`.
All five new ModuleIDs are reconstructed, with exact journal/witness bindings;
their zero image and undisclosed parent proofs remain diagnostic only.

One-index comparison passes the prospective physical-cost gate:
28,975,104 -> 2,396,160 SQLite bytes, a 91.73028% reduction. All 19 retained
snapshot identities, 421 expanded map proofs, the 89,988-byte summary and six
selected page proofs/results match. New index build alone is 1.296875 process
CPU seconds; the complete comparison uses 14.28125 Job CPU seconds. No old
single-index timing exists, so no matched CPU speedup is asserted. Old database
bytes remain unchanged. Independent actual comparison and negative audits now
pass; the scoped actual audits are recorded in ASSURANCE.

Select two subsequent source boundaries, not runtime/proof campaigns:

- Scale: new compact-summary wire codec/tests, explicit encoding discriminator,
  sparse nondefault siblings/partitions reconstructing exact V1 summary before
  unchanged authentication. Keep real wire-byte budgets separate from expanded
  bounded decoding. Current compression comparison snapshots remain untouched.
- Mechanism: new-profile real host/receiver and immutable single-execution proof
  capsule over the retained staged cryptographic backend; fresh guest build
  preparation with explicit dependency graph delta. Adopt CRYPTO-INTEGRATION's
  full receipt verification, exact image/F/P/module/witness and empty-assumption
  requirements. A capsule is untrusted prover input, never acceptance authority.

Actual new guest build, execute-only cost screen and any proof generation require
their own reviewed finite selection. No old proof is migrated or renewed. All
full release obligations remain open; current successes do not label final v5.

## D10: public wire result, real guest build, and the next scale obstacle

Root adopts the independently audited actual public summary comparison: exact
retained 89,988-byte authenticated summary -> 3,017 compact bytes (96.64733%
reduction), two actual loopback requests, no index rebuild or repeated failover
campaign. Expanded and compact clients authenticate the same reconstructed
summary. Actual body bytes are charged, with separate expansion limits; no
coverage is committed on invalid proof, expired deadline or decode refusal.
Seven changed public-boundary controls pass. This is lower discovery transport
cost for the selected corpus, not a general semantic-search complexity theorem.

Host metadata01 failed at SDK typed-assumption conversion. Metadata02 uses the
SDK's claim-erasure operation, retains an explicit digest equality check, and
passes actual compilation with zero diagnostics and clean closure. It is not
an executable or certificate. Exact real host linkage is the next source task.

Selected guest-build01 failed before graph/compiler execution at the inherited
census bookkeeping: a list-valued pruned_aliases entry was included in numeric
resource totals. Its 48.96875 controller CPU seconds and 178.927 wall seconds
remain charged; no build/proof result is claimed. Narrowly repair the adapter
against actual inherited contracts and select a fresh run after review. Do not
widen dependency graph allowances or restart old proof campaigns.

Next search decision is more fundamental than encoding: two frequent, disjoint
features can require linear aggregate anchor scans to prove their intersection
empty. Partitioning alone cannot remove this worst case. Scale compares actual
indexed intersection/joint-feature alternatives and bounded advisory provider
offers. Preserve complete-within-snapshot queries as one mode, distinguish
candidate-only search without a completeness claim, and do not invent a cheap
global-completeness guarantee. Actual public use currently lacks bootstrapping
from contacts to suitable namespace/snapshot offers; tests inject these values.

The final six release obligations remain unchanged and open. The next central
integration remains: discover a reusable method, verify its resolved certificate,
check a new extension using demanded semantics only, and return that extension
through surviving independent services. Lower metadata cost supports this path;
it does not replace it.

## D11: adopt the actual new module image for the bounded cost screen

Root adopts independently reviewed guest02/host01/image-assembly01 outcomes.
This is the first actual v5 module image, not relabeled v4:

- Image ID: `d9572ba4c2336c1544cae3fba652cc66f47b70144c4051d3a57dd2e25af161bb`.
- Image bytes: 1,461,052; SHA256
  `3f264ccf30db0f5eb6d33809e1fa9716be0b4270083ef49062536cecf90fc42f`.
- Exact host: 66,621,952 bytes; SHA256
  `e3b357bb719db9c3e02fa65fde704e0cbd4dd73f48ee0157a6bf1e55dc5c9190`.
- Foundation and semantic policy remain the adopted new receipt relation,
  with the actual source snapshot and SDK/crypto dependencies bound by the
  independently audited builds. Profile adoption for this owner execution is
  not a production security signoff.

Guest02 cost: 209.5625 worker + 216.046875 controller CPU seconds; 422.9368438
wall seconds. Its exact Job-owned/hash-pinned VCTIP descendant was terminated
under the selected cleanup rule; this was not unassisted closure. Host01 cost:
122.015625 worker + 20.296875 controller CPU seconds; 241.1658761 wall seconds,
unassisted clean closure. Both have zero remaining processes. Image assembly
cost is 0.453125 Job + 0.359375 wrapper CPU seconds, with clean closure.

Select exactly module-base-execute01: one preparation, independent exact-frame/
journal checking, then one real base-module guest execution with no parents,
2^25 cycle ceiling and po2=18. Exact selection
`421dc668052d6b60ba3bc7eae9904a2f9dd78c96b7ff907ab90f2eb525ef8123`
has passed independent source/input review. Outer 240 CPU/300 wall seconds,
2GiB, three active processes. No proof call is selected. The actual output
will decide segment/proving feasibility; native timings are not substituted.

The provider-offer nine changed-boundary controls also pass independent audit.
Their mocked/memory transport evidence does not establish the real socket
entry path. A separate two-request retained-index offer->page test is selected
for source preparation, with no index rebuild or repeated failover campaign.
Scale owns the next isolated bounded positive-candidate query, preserving the
existing omission-evident scan API and its distinct coverage meaning.

### D11 actual outcome and cost redirection

module-base-execute01 FAILED: preparation and independent frame/journal checks
passed, but actual execute exited 1 with `Session limit exceeded: 33557665 >=
33554432`. There is no completed cost, segment count or certificate. Independently
reviewed outer RESULT SHA256 is
`22c9ccda6d8f06a2b94eac4d69ab7da83ce593ceba28d1c4d2c8d5d488940379`.
Job CPU 2.234375 seconds, wrapper 0.40625, wall 7.8061117, clean closure.
Do not infer which phase dominated from this error. Root investigates SDK
profiling hooks while mechanism derives source-level cost discriminators.
No automatic cycle-ceiling increase, guest rebuild or proof campaign is selected.

Separately select exactly the independently source/selection-reviewed
offer-public-integration01, SHA256
`72f13c0e1c80694503c2a3e8e9c73e14f1fecb599c65e33c0089e7e7b5723587`:
45 CPU/90 wall seconds, 1GiB, two processes. Copy the closed retained index;
perform exactly one actual no-SID offer and one authenticated returned-SID page
in the same SearchSession, with exact accounting and clean closure assertions.
No database rebuild, mathematical admission, native check, failover or proof.

## D12: remove avoidable construction work; measure before proving

Adopt actual offer-public-integration01 independent PASS: exactly two HTTP
requests, 811 request/6,203 reply/447 header bytes, one fusion candidate,
one shared snapshot slot, no pending/reserved/active resources on closure.
No snapshot was preloaded, no index rebuilt, no mathematical acceptance made.

Source inspection identifies a concrete avoidable asymptotic cost in
module_correspondence: `json!` reserializes already constructed child Values at
each ancestor. Mechanism owns a move-based construction repair preserving every
Value, reference, node visit and canonical commitment; independent differential
review precedes compilation. Static recurrence is not measured VM dominance.

Root selects source-only partial instruction sampling in a successor host:
`receipt/src/trace.rs`, explicit trace dispatch, host build02 path/input update.
Retained SDK `RISC0_PPROF_OUT` only writes after successful finalization, so a
repeat failing run with that environment variable would not answer the question.
The new diagnostic instead retains bounded samples after errors at the SAME
2^25 ceiling, on the SAME guest image. It does not change acceptance or guest
semantics and has no proof call. First metadata-check the small changed boundary,
then link once if independently reviewed. Runtime selection follows separately.

Scale continues candidate-only indexed filtering without completeness claims;
its new code cannot update omission-evident coverage or trust provider-reported
work as client authorization. Existing exhaustive coverage remains distinct.
The full six release obligations remain open, not replaced by these diagnostics.

D12 execution selection: metadata03
`640554848855faae8a1fbbfdfe3dccfaba2b368193047dc22f9fc2f0fcc8cf5c`
passed after independent clearance, zero diagnostics and clean closure;
0.796875 Job CPU, 2.0 wrapper CPU seconds. Its actual pass satisfies the
independently reviewed condition for host-link02, exact selection
`0fe57c014d0c9331de3448040847db8dc77556330749074709d34b1a9b36ed66`.
Root selects that one fresh link with the unchanged 600 worker CPU/900 wall,
4GiB/eight-process and exact owned-telemetry cleanup limits. No guest rebuild,
guest execution or proof is selected by the host link.

Select candidate-query-controls01 after independent full source/selection
review: `55cf42282c6322087800823cbe4f4957a8d7349a22f9d3eee56fa59157665856`,
45 CPU/90 wall seconds, 512MiB, two processes, nine isolated SQLite/proof controls.
This changes the retrieval boundary, not the mathematics or coverage protocol.
Scale separately prepares public integration with conservative full requested
scan charging, common session caps and no candidate-to-coverage promotion.

Actual candidate-controls01 FAILED with 3 passes, 5 errors and 1 failure:
the fixture used pure feature_root hashes without storing nonempty partition
nodes. Both independent reviewer and author locate the missing partition_set
construction; actual Store admission already materializes these nodes. Repair
only the fixture, preserve failed evidence, select fresh02 after exact review.
Failed cost is 0.8125 Job + 0.28125 wrapper CPU seconds, clean closure.

Host-link02 now passes with zero diagnostics and assisted clean closure:
104.0625 worker + 17.28125 controller CPU seconds, 191.5439068 wall seconds.
The produced executable is 66,654,208 bytes, SHA256
`5d5e738f125b189ae424e4b94076b2e6660239a714c4f6ffab341a881136cb74`.
Independent actual review corrects root's first closure interpretation: the
selected exact Job-owned/hash-pinned VCTIP PID33172 was explicitly terminated
and observed exited. Job.terminated_processes=0 does not imply absence of this
separately recorded process cleanup. No worker remains.
The reviewed source-only move-construction repair still awaits actual differential
checking before a guest rebuild. No new guest/proof is selected by this result.

Select fixture-only candidate-controls02 after independent review, unchanged
resource bounds and candidate algorithm; exact selection
`f2866c2b4c1e26f87636fa26f625aa1eb698a4ba3cc55bf1bef906be0aa66d61`.
The partition nodes are now actually stored and their root equality is asserted.
This fresh operation tests the formerly blocked candidate behavior; failed01
and its source snapshots remain unchanged.

Select exact module-base-trace01 after independent source/input/selection
review: `7ef54dd3217a7d1d20b5f0fefdb71051a02ab5dd4db70b70ee845799057ca1d7`.
The prelaunch frame-pin typo was corrected before use; no failed operation is
rewritten. Same old image, same prepared input/journal, same 2^25 cycle ceiling
and po2=18; 240 CPU/300 wall seconds, 2GiB, three processes. One diagnostic
execution, no preparation repeat or proof, bounded partial PC samples preserved
even on execution error. Diagnostic collection success is not guest success.

Trace01 actual FAILED its complete-prefix collection gate at the diagnostic's
131,072-cell limit; raw samples are retained. There were 33,661,697 instruction
events and 131,491 saved samples, before a refused new sample. Job CPU 4.796875,
wrapper 0.453125, wall 10.132599, clean closure. It did not reach the original
session ceiling or a successful conclusion. SDK source actually emits weighted
row points in TraceEvent.cycle (5040 points/row), not the documented instruction
cycle unit; this made the raw windows far finer than intended. Do not rebuild
or rerun solely to repair the histogram. Root selects source-only OFFLINE
analysis of the retained prefix with explicit corrected units and sampling
limits. Original trace01 remains failed; partial evidence has narrower value.

Select independently reviewed standalone constructor differential BUILD01:
`d9e5be9389d38e8a65c5d42884be303b43c91477ec76711d5e9b6dd6639576f7`,
180 worker CPU/300 total wall seconds, 4GiB/eight processes, 6GiB accounted
working bytes, exact owned-telemetry cleanup only. It compiles old/new standalone
serde correspondence modules, not the kernel/backend/guest. Actual differential
execution requires its own exact executable/input selection. This avoids a
costly whole-checker rebuild for a constructor-only change.

Select independently reviewed OFFLINE trace-analysis01, exact selection
`c9ff810ffcad14b862c9298aaa39dfa2059a2acc10ec5ec691cebc149e72d0ea`,
30 CPU/60 wall seconds, 512MiB, two processes. It reads only pinned retained
trace/ELF bytes and writes a fresh analysis. Census accounts for one refused
terminal sample. Weighted points/5040 represent unpadded row-equivalent work,
not exact session-limit progress (which also charges padded segments). No VM,
kernel, network or proof runs. Original failed diagnostic remains unchanged.

Offline analysis01 passes independent actual audit, with per-function/window
census exactly 131,491. Leading exclusive instruction-sample counts are
write_all 28,782, memcpy 20,170, canonical::emit 15,462, deserialize_any 11,775,
escaped-string formatting 7,169; 22,680 samples remain unattributed/overlapping.
The last two available row-equivalent windows include substantial Value
deserialization. This motivates source analysis of input rebuilding and repeated
canonical emission BEFORE a move-only guest rebuild. It does not establish
full-run dominance, inclusive caller costs or cryptographic proving speedup.
Cost: 0.4375 Job + 0.234375 wrapper CPU seconds; clean closure, no VM rerun.

Standalone differential build01 passes independent actual audit: 13.453125
worker + 2.046875 controller CPU seconds, 18.3878463 wall. Closure was assisted
by exact Job-owned/hash-pinned VCTIP PID10980 cleanup. Select the independently
reviewed eleven-case run01, exact selection
`55c5b4d4d486b7dd0e140215d043c56040cc59eb235841f2e85dea87e45b84da`:
30 CPU/60 wall seconds, 512MiB, three processes (Python wrapper, native test,
possible Windows helper). The prelaunch two-process proposal was revised before
use, with all other sources/inputs/bounds unchanged. Five exact retained module
inputs and six changed-boundary negatives; no guest, kernel, proof or network.

## D13: preserve acceptance while removing frontend copying

Adopt eleven-case constructor differential actual PASS: exact five positive
outputs and six refusal payloads; 0.3125 worker + 0.25 wrapper CPU seconds,
1.3054235 wall, clean closure. This establishes tested structural equivalence,
not VM speedup, cryptographic soundness or release completion.

Adopt FRONTEND-COST-PLAN.md after independent source-plan review. Select only
the mutable receipt/guest frontend changes A/B/C and focused differential
preparation. Preserve serde object and positional-sequence acceptance, target
usize conversion, strict parser limits, exact canonical hashes/journals, all
semantic checks and parent receipt verification. No externally supplied witness
digest may acquire authority. Public parse/check retain their contracts. New
guest identity requires freshly bound image/input/journal, not old-frame replay.
Implementation/source review and focused differential precede one combined
guest build; no larger cycle allowance or proof campaign is selected now.

Select public candidate-session-controls01 after independent exact review:
365f6640d384f49c6890c2678ab69860ba47cbe3eaf1a9010dc3ae508f3103e0,
45 CPU/90 wall seconds, 512MiB, two processes. Nine focused controls include
full scan charging, candidate/coverage separation and poison-first metadata
dedup. Next socket test is only offer->candidate on retained compact index bytes;
do not rebuild indexes or repeat already passed native, page or loss campaigns.

Candidate-session-controls01 actual independent PASS: nine controls,
1.296875 Job + 0.25 wrapper CPU seconds, 1.9636709 wall, clean closure.
Select independently reviewed candidate-public-integration01:
`b36def28096695bba3e637e94d79cb19fb1bc8cd275829edb14d88870e056654`,
45 CPU/90 wall seconds, 512MiB/two processes, exactly offer->candidates on a
copy of retained index bytes. Candidate membership is not omission-evident
coverage, nor mathematical acceptance. Provider-location investigation is
separate; configured contacts do not establish global-scale useful routing.

Root additionally selects disjoint `software/v5/admission/` source work under
ADMISSION-INTEGRATION.md: connect exact real-host receiving to process-local
accepted-interface handles through a locally adopted pinned runtime and the
unchanged supervised execution primitive. No source-only or synthetic test
result can mint actual cryptographic evidence. Independent review and focused
controls precede use; the first real positive uses the forthcoming base receipt,
not a new duplicate proof. Scale's acquisition/custody remains structural until
explicitly connected to this gate. No global publication or deployment selected.

## D14: close provider location and same-call public receiving

Actual candidate-public-integration01 exits zero with clean closure, 0.78125
Job + 0.28125 wrapper CPU seconds, 1.7538827 wall. Exactly two actual calls use
877 request/6,305 reply/453 header bytes and return one fusion export claim,
charging the full32 scan allowance without promoting coverage. Retain these
bytes; independent actual audit is separate from raw PASS.

Adopt scale's source-backed maintained-location seam in DISCOVERY-INTEGRATION.
Select new software/v5/location strict domain-separated predicate keys,
advisory service descriptors, owner egress and aggregate workflow budgeting.
Reuse the retained maintained libp2p mechanisms only through a subsequently
reviewed narrow adapter. No new routing runtime, external connection, bulk
transport replacement or global index is selected. Exact matching of advertised
features does not prove usefulness; fixed contact budgets have no universal
recall guarantee as the provider population grows. Preserve the explicit
selective-coverage/availability/maintenance-capacity assumptions and incomplete
outcomes. DHT event bounds do not automatically bound DHT wire bytes.

Public admission source has independent review with two required lifecycle
repairs: recheck deadline after evidence fsync before handle registration, and
after opening validation/copy before returning. Both are applied before any
run. Pure structural tests do not invoke receive or fabricate crypto authority;
real positive admission still waits for the genuine selected-image receipt.

Select independently cleared frontend-differential-build01,
`55f72087731be6658d518358ed8c97192ce829eba49aa2c846da2d946749440f`:
180 worker CPU/300 wall seconds, 4GiB/eight processes/6GiB accounted working
bytes, exact owned-telemetry cleanup only. Twelve source pins and 172 retained
runtime pins bind one actual frontend test-harness link, not a kernel/backend
or guest rebuild. Runtime requires the actual produced executable and a fresh
exact run selection; no proof is authorized by compile success.

Frontend differential build01 passes independent actual audit: 38.40625 Job
+ 2.34375 controller CPU seconds, 44.9241861 wall; assisted closure by exact
Job-owned VCTIP14328 termination and observed exit. Select independently cleared
frontend-differential-run01,
`5c148cb5b6cf77dfe33683420f09b565233746657954e3295094ad9c8152b94c`:
90 CPU/120 wall seconds, 768MiB/three processes. Actual linked harness, five held
witness/journal pairs plus focused shape/canonical controls; no guest or proof.

Candidate-public-integration01 independent actual audit is adopted. Root limits
admission runtime pin-map bytes to512MiB aggregate before pure controls, with a
deadline check between rehashes. This bounds a potential16GiB owner-profile
rehash configuration; it does not remove controller I/O or count it as worker
CPU. Its pure test selection will be repinned before first use, not overwritten
after execution.

Frontend differential run01 passes independent actual audit: five held journals
and pending parent sets match, 58 shape and25 canonical controls agree; ten
native relation calls, 0.5625 Job +0.25 wrapper CPU,1.6810521wall, clean closure.
Select combined guest03 source preparation; actual build needs separate review.

Select independently reviewed admission-binding-controls01 after the pre-use
runtime-map cap repin:
`bc95b17f3c18c67ee8fc49461e40eb62b41f2d7ed17c83b5f6bb34dfdd4fbab3`,
30CPU/60wall/512MiB/two processes. Ten grouped synthetic structural controls,
zero native verifier calls. Separately select source preparation for one actual
malformed-receipt refusal through the public adapter, plus pre-process budget
exhaustion. This tests the new wrapper lifecycle, not repeated host acceptance
or proof behavior. Exact selection review precedes its launch.

Select independently cleared combined guest-build03,
`c45048fd3faf68930271ea2738a6772b5254a6f016a3a1f93f8f4ea4334b4793`:
40 source files/521,778B, same finite1800CPU/1800wall/4GiB/eight-process/16GiB
working allowance. This is the combined constructor+frontend successor after
both actual differential gates, not a move-only or repeated old guest build.
Only the redundant initial retained-map pass is removed; the full first rebind
still occurs before output allocation, and later rebinds remain. Exact graph
explicitly requires serde_json1.0.151 default,std. No dependency/backend change,
assembly, guest execution or proof is authorized by this build selection.

Admission structural controls01 actual independent PASS: ten groups,0.375Job
+0.25wrapperCPU,0.7763563wall, clean. Select independently cleared one-call
admission-refusal-integration01,
`bad0659defab7fe52fe5ca2f98b86729add3b7ed4fb211dfde8eb90f6e26170b`:
60CPU/90wall/1GiB/four outer processes. One real malformed-receipt child call
through the new wrapper, then pre-process exhausted-budget refusal. The held
old-image host is sufficient to test this negative lifecycle boundary; it
cannot establish a new-image positive receipt or mathematical growth.

Select independently reviewed location-contracts01,
`73d40d59e3555fd8d23a694d098d86b5303df7e180ebf6f5f1f71cd51124d116`:
45CPU/90wall/512MiB/two processes,12 native-free controls of exact predicate
keys, descriptor/channel binding, owner egress, expiry and single prepaid
locate-to-search workflow. No DHT or actual socket behavior is claimed by these
controls. Returned provider slots are not all intermediate dials, and DHT event
counts are not a wire-byte cap; the retained adapter must enforce/report these
distinct boundaries before real routing is selected.

Adopt independently reviewed snapshot-as-screen direction for the forthcoming
new image: root's fresh SnapshotModuleScreen prepares/rebinds the base frame
and journal, then invokes the existing host's no-proof snapshot stage once at
the unchanged2^25/po2=18 limits. Retain the coherent capsule for later separately
selected proof stages instead of executing twice. Actual segment count gives
only count*2^18 upper row budget, not measured rows or proof time. Execution can
succeed but capsule serialization fail at64MiB/128segments; no usable snapshot
is claimed until the whole call and binding pass. Exact image selection remains
pending actual guest03 build/assembly; no runtime selected by this paragraph.

Actual admission refusal and location12controls pass independent audit with
clean closure. Root notes that nested verifier worker cost is already included
in the outer Job, not added twice. Guest03 has completed raw build PASS and root
has reaped session4066; actual audit and assembly02 selection are next.

Important integration invariant: retained compressed discovery fixture uses
conditional policy b49e45c0bde61982e9faa6cbeca7ea0619a33b85fee5579412b45301d95bea2c,
whereas current certificate modules use semantic policy
5edfd0ee15b141b7304e26c1a39cd11f7f7e721713cf099813ae4f4442fad377.
Their different ModuleIDs/namespaces are intentional. Metadata-only discovery
tests do not establish certified-module discovery. The integrated positive
workflow needs new-policy records/index generated once from actual current
modules, never old-ID relabeling or profile substitution. Generic unchanged
query/transport evidence can be reused; no need to repeat its compression or
old mathematics campaigns.

Guest03 actual independent PASS:193.03125Job+197.59375controllerCPU,
430.3120324wall; assisted exact Job-owned VCTIP15792 exit observed. Actual
1,403,812B ELF195cb9cedebceae3844141f68624a9e3b7140399732f675d29909737db9ad50c
and full source/graph/log identities pass. Select independently cleared
module-image-assembly02,
`c7c4e9e332344c30139df6a34edba73016ead615d73d77f9cd6111212fa0a5c9`:
120CPU/120wall/1GiB/two processes; unchanged assembler/kernel, actual new ELF,
fresh image only. No guest execution/proof selected by assembly.

Assembly02 actual independent PASS: image
e44b00bbb1c675916d3060b782fec7d1eda742b5f1a4aae04b6a8554b20bbceb,
1,462,580B SHA103e9fd4e80b6e6101feb89ebd0724a6010138708f169d9b9eba3b82c7e17f63;
0.46875Job+0.328125wrapperCPU,1.5412013wall, clean. Select independently cleared
module-base-snapshot01,
`9586ff05764992d56ad1e7ce5db2e5f6e5537bd71367b9625707c60a7ac465f0`:
240CPU/300wall/2GiB/three processes,8sources/6runtime pins, same2^25/po2=18.
New-image base input is freshly framed/bound; no parents or proof calls.
Only actual whole snapshot success permits later staged-proof selection.

## D15: diagnose the remaining new-image execution cost

Adopt independent actual snapshot01 failure audit: exact unchanged ceiling
33,557,665 >= 33,554,432, 2.609375 Job + 0.40625 wrapper CPU, 3.4023853 wall,
clean closure, no capsule or proof. Do not infer relative speedup from two
ceiling failures. Prepared 91,387-byte frame SHA
67e7485dc5167ffb75061a8bfae2afea79e7dd5efeca662896b0fad6b3a13ab1
and 216-byte journal SHA
1b2ed9ee0969354566a1529af765b5c79b27b81119e7fce2e6f52d0c69b6aa2b
are available for one new-image partial diagnostic, avoiding another preparation.
Root selects source preparation of a harness which accepts explicitly bounded
sample-cell-truncated prefixes, distinguishes the stopping bound, and interprets
the actual SDK weighted row-point units. Reuse host02 unchanged; no new build,
larger VM ceiling or proof selected. Exact pins/review precede one runtime.

Admission verifier's later label-only change is independently confirmed against
the used refusal01 source: all bytes except the diagnostic status string agree.
Current b6faf155a7f2793035ba00a09ee8db7b5d3d34e337f4f209198d846c02707dbc
does not change authority/control flow; no repeated runtime is warranted.

Select independently cleared module-base-prefix01,
a096b968b2b3895ccb9edb3ff82261c8d1fe276f1d09eda40b751d71455fa515:
three source/eight runtime-input pins, 240 CPU/300 wall/2 GiB/three processes.
Exactly one new-image diagnostic at the unchanged 2^25/18 profile, using the
prepared snapshot01 frame/journal and exact user/kernel ELFs. Sample-cell and
session-bound stops remain partial prefixes. No proof or budget increase.

Actual prefix01 passes independent diagnostic audit: 33,645,057 observed
instructions, 131,426 retained samples, 131,072 distinct cells; sample-cell
stop, not completed execution. 5.375 Job + 0.328125 wrapper CPU, 6.7721129 wall,
clean closure. Exact kernel symbol attribution identifies 40,515 samples in
ecall_sha; these are instruction samples, not a total-time or proof-row share.
Outer result SHA 8d633a2b127a5a477794718b0e81e38287feefafc5fa46b921b71417e6ce2307.
The exact kernel source dispatches version3 SHA to software compression; merely
calling the guest SDK SHA implementation does not establish acceleration.
Mechanism must map the actual backend/version before recommending changes.

Root selects source/theory comparison of an existential certificate relation
which omits the whole-proof-witness digest from a NEW journal profile. The
mathematical claim is a valid module extension under the adopted policy, not
the provenance of one chosen proof. Module types, computational body hashes,
exact parent journals, rank, all local checks and recursive discharge must
remain. This is not permission to ignore failed canonical validation or to
zero an existing journal field. Resource validation must survive independently
of serialization; host-only input/capsule pins preserve experiment accounting.
Author and independent reviewer must establish sufficiency before source work
is selected. The large global encode/hash might then be removed rather than
merely optimized. No profile migration, build or proving selected yet.

## D16: existential module certification, explicit protocol successor

Author and independent reviewer agree: the public whole-witness hash is never
a premise of the mathematical relation. Select source implementation of
DMKNM002/profile2/184-byte journals and DMKN_CERTIFIED_MODULES_V2. The public
statement asserts existence of a fully checked module witness. It is not
attestation of separately presented proof/source bytes. Exact parent journal
verification, rank descent, foundation authentication, all type/body/group
commitments and every local declaration check remain. ModuleID and semantic
policy stay unchanged; receipt image and journal profile necessarily change.
Old-profile receipts are rejected, not relabeled or silently truncated.

Mechanism owns receipt Rust/Python helper, independent structural validation
without canonical emission, focused differential controls and documentation.
Root owns public admission/profile2 binding and a new snapshot adapter.
Assurance reviews the argument and changes. Source work is authorized now;
builds and runtime require fresh exact selections. No foundation specialization,
new hash function or backend migration is included. Kernel source confirms that
the current M3 backend executes SHA in software; changing one version constant
is not an authorized or sound backend migration.

Root's profile2 admission now rejects old journals, has no witness/provenance
output, and binds the journal profile into local adoption identity. Prepare six
changed-layout structural controls only; reuse previous unchanged supervision
and malformed-receipt lifecycle evidence. No fabricated successful receipt
test may establish admission. The historical refusal harness stays historical.

Select independently cleared admission-profile2-controls01,
d96e3285a3b59fae8cc2f9a1e9290020f857448fa6730735251eda4df306260b:
six synthetic changed-layout groups, 30 CPU/60 wall/512 MiB/two processes,
seven source/eighteen runtime pins. No real receipt/native invocation.
Also select explicit capsule3/checkpoint5 and session/snapshot V2 domains for
the new host's staging. Prior checkpoints are not migrated. Input, image,
expected journal and parent receipts remain independently session-bound.

Select independently cleared location-node-controls01,
141b3a17d37762b7f487e7743a4418424d6dfd670a6d87d81d8e1c413cfb3dc7:
thirteen changed-boundary groups, 60 CPU/180 wall/512 MiB/two processes.
The launcher verifies the complete selected 5,896-file retained overlay/Node
closure before and after, with all hashing charged inside the one Job.
Actual retained TCP/Network methods use fake sockets/mock RPC; this is not a
real network or cross-language integration. Raw admitted byte caps cover service
work but not kernel packet counts, pre-upgrade allocations or hostile liveness.

Actual location-node-controls01 FAILED in the eighth mock-routing group's
status call because the fake node lacked getMultiaddrs. Seven groups passed;
do not relabel the full operation as passing. Full selected dependency closure
checks passed before/after; 13.34375 Job + 1.09375 wrapper CPU, 112.6655709 wall,
clean closure. Cold preverification took 104.418 seconds versus 5.551 seconds
afterward; it is charged, not evidence of routing cost. Select source preparation
of a fixture-only six-group continuation, reusing the seven completed outcomes
and unchanged production sources. No rerun or production gate weakening.

Select independently cleared existential-differential-build01,
1f9b8cda850609ce7991cdc63d6282e550a7bcd457ff74927ec9186e43db67f3:
twelve source/172 retained runtime pins, frozen guest03 canonical comparison;
compile only, unchanged 180 worker CPU/300 wall/4 GiB/eight-process/6 GiB working
allowance and exact-owned telemetry cleanup. No backend rebuild or test yet.
In parallel select independently cleared location-node-controls02,
f7c5107c885b70d92bc2056afc1656e6010f0e53ba8c194784c855066974d1b2:
same finite limits, remaining six groups only, unchanged production source,
mock getMultiaddrs repaired; no dependency on skipped group's store mutations.

Adopt actual independent continuation02 PASS: six remaining groups, seven
historical skips, zero real sockets/queries, complete selected runtime binding;
6.21875 Job + 0.46875 wrapper CPU, 6.738182 wall, clean closure. Result SHA
1779c5c03b93a2db98a66d8d944084520c86b0c31d8692c836e9d4b4aeb6fd74.
Combined scoped coverage is thirteen groups across two preserved operations,
not a reclassified passing first operation.

Adopt actual independent existential harness build01 PASS: 1,584,128-byte
executable SHA e7eb402083dd1d575021afd25d27a7e5790e77772d4db0d105e5c6eb4cecb1c0;
39.46875 Job + 2.40625 controller CPU, 53.2810252 wall. Exact Job-owned VCTIP
PID14568 terminated and exit observed; no unknown cleanup. Result SHA
6b8ddce19eb8d8605137812f5529e1596a6b247321da7b5b407961ff50902519.
This is compile-only. Actual differential and guest/host launches are separate.

Select independently cleared existential-differential-run01,
dd8ef8511b131e134688fd7b2f011620297bfbdc2a626fdc0734d38c6a1fd6e3:
two source/27 runtime-fixture-build pins, 90 CPU/120 wall/768 MiB/three processes.
Actual native changed-boundary checks only, no guest or cryptographic proof.
Prospective guest04/host03 source clearances remain conditional on this outcome.

Actual native differential run01 FAILED: native parser refused duplicate Expr
in the alternate-theorem construction. The helper blindly appended bvar0,
already present in the unique expression arena. Five projected-case files were
written only after their checked assertions passed; preserve this evidence and
the failed operation. Cost 0.40625 Job + 0.25 wrapper CPU, 1.4709967 wall, clean.
Do not weaken the native uniqueness check. Select a fresh fixture-only
continuation which interns/reuses exact existing nodes and runs the unfinished
alternate-proof/negative/layout/size controls, reusing the five completed cases
after independent outcome audit. No guest04/host03 launch is authorized yet.

Select independently cleared existential-continuation-build01,
e3e544ded09642c1845f77b79ebfba04475834dca5463c10faf6334ccb767dda:
twelve exact source pins, retained172-file runtime/link recipe, same180worker
CPU/300wall/4GiB/eight-process/6GiB working limits and owned-telemetry cleanup.
Only the fixture uses structural interning; native guards and production source
remain unchanged. Reuse the five audited projected cases, preserving run01 as
failed. Actual continuation runtime requires the resulting executable and a
separate selection. Guest04/host03 remain conditional on its completion.

Select independently cleared location-controller-controls01,
ef683441fdbb22fd6c2aa86dcb2db57c6310d60eb454299aa7d8629ca39fff4d:
28source/19runtime pins,30CPU/60wall/512MiB/three-process profile. Seven Python
lifecycle/ticket groups use mocked process/runtime verification; one actual
Node child tests cross-language route/request/IPv4/descriptor vectors and
IPC/composition boundaries. Zero sockets/libp2p imports: real networking is a
separate integration. The pre-core race fixture now has a deterministic barrier;
production lifecycle changes were independently reviewed before selection.

Adopt independent actual existential continuation build01 PASS, result
cfd66405fc446c6608d2b69572fc162369f90556861ccb1a92b7f4c910216e11;
35.90625Job+2.1875controller CPU,41.6672125wall. Exact owned VCTIP10980
termination/exit observed; all other closure/bindings clean. Select independently
cleared continuation-run01,719190a59e4c039b382ac871a6c545164ba1476dbac5875915be7cd3b9bd676d:
two source/33runtime-fixture pins,90CPU/120wall/768MiB/three-process profile.
Fresh executable a5e1426234ed619b75657add751e6f2b005ffc1bbb33cf383dad1ab61f115790.
No guest execution or certificate is authorized by this native differential.

Select a narrow reader/index-provider location-role successor before real
loopback integration. Reader nodes must support zero advertised endpoints and
refuse publication/withdrawal/descriptor service while retaining bounded DHT
discovery. Do not manufacture an advertised service endpoint merely to satisfy
a provider-only configuration. Scale owns fresh wrapper/composition/controller
source and focused changed-role controls; used Node/controller snapshots stay
frozen. Investigate the completed controller test's unhandled shielded-future
diagnostic on cancellation in this same seam, not by repeating passed groups.

Adopt independent actual continuation01 PASS, outer result
555e50e579882cf96a8a6e5f9f14f27038a7cc774a6bf7ee07d3ec55cf2e8f79:
five prior positives retained; base Value entry, distinct valid proof with same
conclusion, six refusals, four layout and183validation controls completed.
0.515625Job+0.21875wrapperCPU/1.5206948wall, clean closure. The false-proof
control emits its expected caught native panic; this is not successful proof.
Actual unchanged guest04/host03 pins are independently reconfirmed. Select
guest04 7bbce637f3fe89e3b55eef5271e81c7702eedf2fa79ac5b3f4ab825ba569e0f0
and host03 a855e500d992592d1569ae8b04d02b8e31594f3a149bd2b6cca627ec849c0920
builds in parallel under their unchanged finite1800CPU/1800wall and600CPU/900wall
profiles. No guest execution or proving is selected yet. All selected source
bytes stay stable; failures/predecessors remain immutable.

Adopt independent actual guest04 and host03 compile-only passes. Guest result
609a78318d69fb7e50d36b7e8caf915cb6f5c2cf587893862dbc195b131dfd1c:
197.609375Job+203.640625controllerCPU/439.4432559wall. Host result
6e01679707da8d58e286f7c756e698b1870aeab250d3bccda7a9099e1b8344e7:
105.625Job+19.203125outer-controllerCPU/213.1983675mainwall; outer controller
contains19.1875main CPU, never sum both. Owned telemetry cleanup was disclosed;
all final Jobs have zero active processes. Select independently cleared image03
assembly fd620fce1df09b871217dd72056a4dea77b2a4f734d288811f96530df7caa3b1
under unchanged120CPU/120wall/1024MiB/two-process limits, retained assembler/kernel.

In parallel select independently cleared location-public-integration01,
6719492c48ff4ed71fadb4fb105b8043905ebf96f0afde7b5586bf35bb096606:
35source/21runtime pins,60CPU/240wall/1024MiB/three-process profile; loopback
DHT ports39171/39172 plus ephemeral HTTP. Four new role control groups followed
by real two-node discovery/Noise referral and same-budget offer/candidate calls.
Prior owner egress permissions include HTTP port but no search contact is
preseeded. Reader advertises no index service, yet still participates as DHT
server. Uses unchanged old-policy metadata; this cannot certify current-policy
mathematics or huge-network coverage. Keep all actual outcomes and charge costs.

Select source-only verified-import/ordinary-Lean authoring investigation under
VERIFIED-IMPORT-AUTHORING-CONTRACT.md. Mechanism owns new software/v5/authoring
files after immediate snapshot/calibration preparation. Live receipt handles,
exact copies and authenticated openings must determine imports; producer requests
remain untrusted and final host/guest/resolved-receipt checks remain mandatory.
Authoring-only theorem assumptions cannot become local admitted axioms. Exact
transparent semantics and complete inductive groups must be reconstructed or
explicitly demanded/refused. No new frontend runtime is selected by this step.

Adopt independent actual image03 assembly PASS (outer cb025e9f4ea5e1069dc2a204e38787f29bb42deefb1c3a465011f2661eefdbdf):
1,463,728B image fc84cd85dfc2e13c60e3776f62171d15146785952915de8f0574ea54310f2764,
actual imageID517205f8ae4fcf2ef35594210248410295d3946cbcbcaf7cdb3e26f2217242f5;
0.453125Job+0.34375wrapperCPU/2.4513144wall, clean. Select independently
cleared module-base-snapshot02 c702e01f191b082f57abadea00963f9c1f94cdad2cdcc873ac9bc599b1b8ac64:
same2^25/po2=18 execution ceiling,240CPU/300wall/2048MiB/three-process profile,
eight source/eight runtime pins. Fresh requestV2 construction only; actual
host03/image03, independently bound184B expected journal. Exactly one prepare
and one retained snapshot execution; no cryptographic proof yet. Earlier
profile1 failure remains preserved, not rerun or relabeled.

## D17: residual execution cost and the first real location failure

Actual profile2 snapshot02 FAILED at the unchanged session bound:
33557665 >= 33554432. Outer result
ae7cd040c71eb580fea84b6998185d296a84972aed02ce6db910f3a70f42083e;
2.78125Job+0.375wrapperCPU/7.360171wall, clean. Preparation succeeded and
independent review bound the91,383B frame and184B journal, but no capsule or
certificate exists. Whole-witness-digest elimination is insufficient. Do not
launch the conditional segment0 calibration or infer improved completed cost.
Investigate current-image residual phase plus compiled fixed-foundation and
supported hash-friendly commitment alternatives before another guest build.
No larger execution cap or new primitive is selected by this investigation.

Actual location01 also FAILED: four new role controls passed, provider startup
ended before READY; no reader or HTTP calls. Outer d220da67c4587ead18260f258a3d68b68c57df84c5a977e700f426c995b17a10;
19.15625Job+1.015625wrapperCPU/118.6758416wall, clean process closure and
full selected runtime pre/post binding. Controller recorded childstderr length
but did not retain its contents: do not invent its exact historical error.
Source inspection establishes a mandatory blocker: retained kad-dht requires
identify AND ping capabilities, but this adapter installs only identify/dht;
the working retained overlay includes ping. Select the minimal retained-Ping
runtime/composition successor and a new continuation preserving bounded stderr.
Reuse four passed role controls; no prior real location success exists to repeat.
No dependency installation or wider service allowance is authorized.

Select independently cleared current-image prefix02 diagnostic,
a76f24c4a74b8fed6d0a49cc99bbf67ee4a6981ddc73c0a40ed17155244e4b58:
unchanged three-source diagnostic helpers, eight exact actual runtime pins,
240CPU/300wall/2048MiB/three-process and2^25/po2=18 limits,131072sample cells
and stride256. This distinguishes sampled residual phases; a partial prefix
cannot bound unsampled native work or establish successful checking. No guest
build, proof or execution-cap increase accompanies this diagnostic.

Select independently cleared location-public-integration02,
86337227efea517ec85e0a0476edc391fbd97c15569b80817af76c6f19722fc7:
36source/21runtime pins, unchanged60CPU/240wall/1024MiB/three-process and
loopback ports. Adds only retained manifest-covered Ping capability to the
exact identify+dht service configuration;5s/four-in/eight-out Ping limits sit
inside unchanged aggregate transport/lifecycle budgets. Fresh harness skips
the four passed role groups and preserves bounded owned childstderr even on
failure. No prior failed run or used source is rewritten, and unavailable
historical diagnostics are not reconstructed as observation.

Adopt independent actual location02 PASS: outer
a07f9ff5ff561d8d9e794d70169649a36d88f12be1ae3589435930d071d59ca3,
28.890625Job+0.5625wrapperCPU/33.2744171wall, clean. Zero initial search
contacts -> real bootstrap/DHT provider -> Noise descriptor -> same-budget
offer/candidate, one expected old-policy formal record. Two HTTP calls used
877request/6305reply/453header bytes; full32scan allowance charged, no verified
coverage or mathematical admission. Raw TCP admitted send/receive match across
peers; both exit0 with no active connection and reader publication/intent rows0.
Four full retained-runtime checks passed. Post-teardown search expiry is not
a late accepted request. This closes the selected actual endpoint-discovery
integration, not worldwide recall, certificate acquisition or growth.

Current-image prefix02 actual diagnostic is independently adopted (outer
60e13767acb528d241c21f338b95d1d2124c14bd049816eb07cd0ef71f535c67).
5.34375Job+0.375wrapperCPU/6.5431868wall, clean;131412 retained samples,
33,641,473observed instructions, sample-cell stop. Unlike prefix01, it reaches
correspondence and native-row parsing. SHA has21,342exclusive samples, not a
complete runtime fraction; no sampled typechecking completion is established.

Select ONE combined preserved-identity source repair before any next build:
(A1) generated immutable exact foundation comparator, preserving parsed witness
and every native check, removing prefix clone/canonicalization/twoSHA computations;
(A2) relation-only direct owned-row outer decoding after exact correspondence,
avoiding serde(flatten) Content maps while retaining existing payload variants,
apply_row, duplicate/backreference checks and public general parser unchanged.
Mechanism owns source/generated data and focused equivalence controls; assurance
reviews before root selects any runtime. Same wire/profile/policy/ModuleIDs;
new implementation image required. This removes identified work, not proof of
completion within the original cap. Do not follow a failure with blind hash-
suite changes or declare huge-network representation solved.

Canonical typed semantic DAGs remain the architecture-level representation
target: unique-node/edge bounded commitments and direct correspondence must
avoid re-expanding to old trees, with binder/universe/reference context and
canonical identity fully specified. That is a real content migration. Poseidon
alone changes hash constants/security assumptions but not expanded semantics
or parser duplication; it is not selected. New cryptography is unnecessary to
exploit a compact DAG. Authoring draft remains unreviewed while A is primary.

## D18: connect discovery to receipt custody and live admission

Root read the complete RECEIPT-ACQUISITION-PLAN and adopts its minimal source
selection. Scale owns fresh custody/receipt_store.py,
transport/http_provider_receipts.py, transport/receipt_client.py and focused
changed-boundary controls. Used provider/search/location snapshots stay frozen.
Independent review precedes any runtime; real mathematical integration waits
for a genuine current-image receipt and current-policy exports/index records.

Additional explicit obligations: the public receipt encoding identifier must
normatively fix byte/layout and verifier-parameter compatibility, not merely a
crate's name; one original absolute deadline and disjoint allocations/shared
reservation ledger must cover the entire path; every required separate-store
durable commit must finish before claiming supplier-independent retained reuse.
Partial commit failure is incomplete, never mathematical or availability success.
Cold restart must reverify receipts. Public WireProfileID is distinct from the
machine-local verifier-adoption ID. Co-hosted index and receipt services are an
initial path, not a solution to general unknown-custodian routing.

D17 remains the immediate proof-cost priority. Exact foundation equality is a
strengthening of the former dual-digest condition, with converse only under
binding; direct-row fallback must preserve accepted parser-domain behavior.
Preserved mathematical IDs do not grant old-image recursive receipt acceptance:
the relation still checks parent.image == input.image. No capsule exists and
no new build, proof, higher cap or hash-suite change is selected here.

Root develops the compact canonical typed semantic-DAG contract in parallel,
specifically end-to-end unique-node processing rather than compact transport
followed by tree expansion. This design work must yield a concrete migration
decision and cannot be presented as implemented growth or receipt performance.

Select independently cleared structural-frontend-build01, selection
5dfbb967879562df74c1a24fdab9d5241ba69571ea5742343ae5d6287662a45e:
31 sources/537,991 bytes, retained eight dependency rlibs, one ordinary binary
link only. Finite 180 Job CPU/300 wall/4096 MiB/eight-process profile and exact
owned-telemetry cleanup remain. Root read the full source/plan and independent
clearance; no tests, VM execution or proving are included. Generated foundation
data and the unchanged general parser are preserved in the source snapshot.

Actual structural-frontend-build01 FAILED at native linking, before any test.
RESULT3759b0cf1b15af6ffe0598f88f133ad09f738d95ee0015f4a3b513ab47fd4ff6:
16.09375 Job +1.734375 controller CPU seconds,9.4999926 wall, clean closure.
Saved stderr reports unresolved dependency symbols and LNK1107 for retained
semver rlib. Root comparison finds the fresh recipe omitted the adopted link's
`-C lto=fat -C embed-bitcode=yes`. Do not infer corrupt disk bytes from the
linker's generic wording: input pins still match. Select a source-only fresh
adapter02 restoring the retained bitcode/LTO linking convention, unchanged
checker/harness/limits. Failure01 and used sources stay frozen. No test success,
guest build or cap increase follows from this failed compile-only operation.

Select independently cleared fresh structural-frontend-build02,
439e3df1a7a5e4f259de6f397156aea0c295e79944833123f7099647645e330c:
31 files/538,057 bytes, unchanged 180 CPU/300 wall limits. Root independently
diffed adapter02: only fresh paths/self-map and retained fat-LTO/embedded-bitcode
flags differ; the other 30 selected files are identical. One compile only;
test execution remains separate and depends on an actual resulting executable.

Adopt independent actual build02 PASS, RESULT
995b3f873652722634438fed90dab9adb33f4760375144ea2948ff90644c6399:
962,560-byte executable8a14b0fe25f328f6b73ebcb12f9f05838752679edce91610a6203fab0b5c8a5f;
21.515625 Job CPU+2.3125 outer controller CPU (includes2.296875 main),
28.0071035 main wall. Exact owned VCTIP29736 cleanup observed its exit; closure
and pins pass. Select independently cleared structural-frontend-run01,
8987f8919d619be3d83100880b312e10f3f00d83073020bc50e3f7f0cf59d5b0:
two sources/40 runtime pins,30 CPU/60 wall/768 MiB/three processes. This compares
decoded rows and compiled foundation only; zero native theorem/VM/proof calls.

Actual structural-run01 FAILED at a genuine decoder compatibility boundary:
`{const:[0,[]],ie:0}` is accepted as a positional struct by the old flattened
decoder but refused by direct serde_json enum decoding. Outer result
064a59718ccd3ed05a7b6c22f14dc025d4c1f5740ad5109d68f54a372bbcc33f;
0.359375 Job +0.25 wrapper CPU,1.5843935 wall, clean. Preserved foundation
reconstruction and exact failure control flow delimit prior successful checks;
independent audit decides evidence reuse. Select source-only minimal array-payload
fallback to unchanged general decoder, plus a fresh narrow continuation. Do not
relabel failure01 or launch stale guest05 before the repaired differential passes.

In parallel select independently cleared receipt-controls01, final selection
450598d2c05b02510f9183dc41b0a974bb263addef32b8556f81a8d5ff211f1c:
20 source/18 runtime pins,30 CPU/90 wall/512 MiB/two processes. Root read new
store/client, provider delta and full eight-group harness. Actual loopback raw
binary/JSON framing, separate durable custody/reopen, partial commits, aggregate
failure charging and exact six-attempt exhaustion are covered. Synthetic receipt
bytes are deliberately nonproofs; no real verifier/prover or positive mathematical
admission is included. Superseded unrun draft8dd907 is not selected.
