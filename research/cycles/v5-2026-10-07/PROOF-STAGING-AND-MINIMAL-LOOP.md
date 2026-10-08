# Actual proof-cost anchors and the minimal certified module loop

Source/evidence planning and newly selected prefix-controller source. No runtime
launch, budget increase, image assembly or old campaign restart is selected by
this note. Mechanism lane; root owns actual launches and release claims. Current
profile2 guest05/host03 sources remain fixed. Historical proof observations below
are NOT new v5 measurements.

## D22 actual prefix and full-base production decision

Implementation update: root subsequently selected the public producer source,
now present in `software/v5/production/{producer.py,__init__.py,API.md}` with
eight focused synthetic control groups in `test_producer.py`. Complete source
review addressed saved-document binding, role-pin conflicts,70MiB/10-entry
prelaunch output reservation and live allowance-history omission. AST-only
inspection passes; root subsequently reports eight synthetic control groups
passed once (independent actual audit requested). Used sources are frozen.
The two actual owner manifests for the325-call remainder are drafted and pinned
in CRYPTO-INTEGRATION; their output remains absent, no full launch is selected
by this note. The proposal below preserves the rationale; exact current interface and
accounting/recovery limitations are in API.md, source hashes/status in
CRYPTO-INTEGRATION.md. No actual prefix/source evidence is changed or replayed.

Prefix01 is now independently audited PASS, root reaped session6942. Its frozen
outer RESULT hash is `fb61eb62eb75a1c40694a4b5ab12c650c39cdb4738153b356591eb895672afee`.
Actual costs are lift0=174.09375, segment1=751.5, lift1=182.5, join1=179.328125
worker CPU seconds; total1287.421875 plus2.0 observed controller seconds and
94.4312573 whole-wall seconds. Stage wall times total92.4811368 seconds,
already inside whole wall, not added to it. Outer output census before RESULT
is950,170 bytes/31 entries. Controller values are observations before final
report writes; process startup/exit and unmeasured tails remain excluded, not
silently zero. No new proof or verifier measurement is needed to learn this.

The two actual lift samples average178.296875CPU, materially above historical
104.2683. Thus the new scenario for remaining108 triplets is:

    108*(751.5 + 178.296875 + 179.328125)
      =119785.5 worker CPU seconds =33.27375 CPU hours.

This excludes finish, controller, cold admission, setup, failed work and a child
proof. Replacing751.5 by observed segment0's565.03125 gives99,646.875 seconds;
neither is a confidence interval or bound. Segment composition and available
resources differ. Current per-stage memory remains below4GiB; both segment
observations are around3.53GB private commit, recursion around1.55–1.58GB.
Keep serialization for this host's existing4GiB stage envelope; parallel proof
processes need a separately funded aggregate-memory decision and are not selected.

The existing source/selection below is now USED/FROZEN. Source-only planning of
a relocatable reusable producer successor is selected; no successor code,
325-call campaign or cold-admission launch follows automatically.

### Proposed successor: a reusable owner-controlled producer

This is a source PLAN, not selected implementation. The concrete smallest next
scope is one public module `software/v5/production/producer.py`, its concise API
documentation, and focused scheduler/accounting controls. Keep the existing
host03, image04, capsule03, checkpoint schema5 and public admission boundary.
Do not build a new host, change the guest/image, make a dependency manager, or
write another controller whose executable code contains `110`, fixture paths,
or this experiment's hashes. The owner supplies adopted configuration and a
finite request; the software checks and executes that request.

The same implementation should be callable from a local agent and a small
owner CLI. It is relocatable on the supported Windows profile, not a claim of
Linux/macOS support or a hostile-code sandbox. Absolute paths are owner inputs,
not mathematical identities. Installation/runtime/helper pins and outputs are
owner-controlled; remote discovery replies cannot configure executables or
resource budgets. Compose with the existing admission supervisor/module-loader
bindings without replacing an already loaded foreign `domains` module.

The interface has three inputs and one non-authoritative operational report:

1. An owner-adopted `ProducerProfile`: pinned host executable, supervisor
   manifest/helpers/runtime, actual image/profile/foundation/policy and finite
   implementation ceilings. Rebind these before and after every actual call.
2. A `SessionSpec`: exact image bytes, frame, expected journal, retained capsule,
   cycle/po2 limits, parent receipt pins, capsule binding, segment count and
   actual assumption count. Counts are bounded plan inputs, not trusted proof
   facts. The unchanged host independently binds/validates them on consumption
   and finish. This operation does not execute the guest again.
3. A finite owner request: exact stage allowance, existing checkpoint inventory,
   fresh attempt directory and budget disposition. Existing artifacts are pinned
   bytes, not accepted because a previous JSON report says PASS. Legacy prefix
   artifacts need no conversion or rewrites. Their actual host validation occurs
   when consumed by a later stage; finish fully verifies the exact result.

The output is a retained checkpoint inventory or a `ReceiptArtifact`, plus exact
process/byte/cost observations. It never fabricates `VerifiedModule` handles.
Only the separate public same-call admission path can mint those handles. No
network operation, search, publication or external message belongs in producer.

### Deterministic finite stage graph and reuse

For n in1..128 actual segments and a in0..8 actual assumptions, generate exactly
n segment nodes, n lift nodes, n-1 left-prefix join nodes, a ordered resolve
nodes and one finish node. The owner request may select a prefix of this graph
or the complete remaining graph. No arbitrary shell commands or caller-supplied
dependency edges are accepted. Enforce these generated dependencies:

- lift(i) consumes segment(i).
- join(1) consumes lift(0),lift(1); join(i>1) consumes join(i-1),lift(i).
- resolve(0) consumes the final joined/lifted prefix plus the host-derived
  actual assumption; later resolve(j) consumes resolve(j-1). Exact parent
  receipts accompany each call as required by the unchanged host protocol.
- finish consumes every segment checkpoint and the final succinct prefix or
  resolved checkpoint. It emits a receipt only after full same-call application
  verification, exact journal/claim equality and empty assumptions.

For n=1 the prefix is lift0, with no joins. Bound the request, checkpoint
inventory and predecessor manifests before graph construction (proposed ≤1MiB
request, ≤392 graph nodes, ≤16 prior attempt records and ≤8MiB prior metadata).
Pin maps have a512MiB aggregate immutable-input envelope, and every planned
host call must fit the existing512MiB aggregate-read/64MiB per-file limits.
These are explicit finite profile restrictions, not universal module support.

An existing checkpoint fills a graph node only after exact session-binding,
schema/kind/index/byte pins are checked. It is never reproved. A supplied joined
prefix can close previously completed intermediate lift/join work; do not
artificially require replay of its vanished execution reports. All supplied
artifacts and costs remain accounted for; intermediate claims alone are not
application authority. Missing retained artifacts cause a typed missing-input
result, not an automatic costly retry. The first stage failure stops the attempt.

Current exact inventory contains segment0,segment1,lift0,lift1,join1. Preserve
all five. New stages use join1 as the prior succinct prefix; finish uses both
retained segment checkpoints. The retained lifts already contributed to join1
and need not be passed as unused finish arguments (the host rejects extras).
The selected prospective remainder is108 triplets for2..109, then finish:
325 new calls, zero guest executions. Cold public admission remains additional.

### Proposed finite resource allocation and its limitations

A concrete next request can use the following POLICIES, subject to root choice
and independent exact review; these are not mathematically proved runtime bounds:

| Resource | Proposed ceiling |
|---|---:|
| Aggregate worker CPU |150,000 seconds|
| Aggregate observed controller CPU |900 seconds|
| Whole attempt wall, including binding and finalization |14,400 seconds|
| Segment stage CPU / wall |1,500 /300 seconds|
| Lift or join stage CPU / wall |250 /120 seconds|
| Finish stage CPU / wall |30 /120 seconds|
| Per-stage Job private commit / active processes |4,096MiB /2|
| Per-stage stdout / stderr |1MiB each|
| New retained attempt output / entries |1GiB /4,096|
| One checkpoint or receipt |64MiB|

150,000 worker CPU gives25.2% headroom over the current119,785.5 triplet
scenario, but only two segment observations and three recursion observations
exist. Completion within it is NOT guaranteed. Sum of all325 maximum stage CPU
caps is216,030 seconds, greater than the aggregate allowance. The controller
must therefore enforce actual settled charges plus outstanding reservation,
not pretend that all stage maxima were simultaneously funded. If the root
instead wants the full sum of stage reservations funded up front,216,030 is the
appropriate structural number; it still does not guarantee stages won't time
out or fail. Whole wall is a separate bound, not CPU divided by guessed cores.

Finish30CPU is prospective headroom above the retained old66-segment finish's
2.796875CPU and its larger110-segment verification vector, not a bound derived
by assuming a universal scaling factor. No repeat finish calibration is needed.
Current finish verifies every segment individually and the composite again,
then the final succinct/application receipt; all of that work remains charged.
An unexpected expensive finish remains a failed, charged operation with all
prior proof work retained. Cold admission is separately owner-budgeted; do not
run an otherwise identical extra cold verifier before the actual public gate.

At each stage: durably record its reservation before launch; require settled
worker charge plus that reservation≤150,000; clamp the call to remaining whole
wall. Only complete final Job accounting and clean closure may reconcile the
reservation to its actual usage. A sampled overshoot is recorded in full and
stops the attempt; never truncate observed costs to the cap. An exception or
missing final counter retains the full reservation and flags accounting/closure
uncertainty. The controller never releases unknown budget merely because a
checkpoint file exists. Controller CPU and whole wall are also checked after
every call and final report; their pre-report observations exclude unmeasured
startup/exit/tails explicitly. No nested supervisor reading is added twice.
The retained Job's hard time limit is user CPU; total CPU/log/wall limits are
sampled. Thus a reserved charge for an unknown outcome is conservative local
budget bookkeeping, NOT a proved ceiling on all actual CPU used. Unknown
closure/accounting holds further automatic work until explicitly resolved.

Disk is a between-stage/post-finalization sampled envelope, not a filesystem
quota. Before the next call reserve64MiB output plus its bounded logs/reports
against the1GiB aggregate; after the call account actual retained bytes, without
deleting successful or failed evidence. Bound entry count while enumerating;
reject reparses/escaped paths. The expected actual checkpoint total is much
smaller (roughly75MB if current sizes persisted), but this is not a size bound.
All110 segment checkpoints must remain available through finish. Original
capsule/runtime/retained inputs are pinned rather than copied for each stage.

### Failure, restart and cost lineage

The durable reservation precedes any host launch. Per-stage completion records
and artifacts are create-new/fsynced; they include exact dependencies, capsule
binding, process disposition and cost observations. An interrupted pending
reservation is never silently forgotten. Successful mathematical checkpoint
bytes may be salvageable after an operational failure, but this requires a
fresh explicit owner adoption of their pins and prior cost/closure disposition;
it does not relabel the failed attempt or its budget as passing.

No process automatically retries a failed stage or starts another attempt.
A fresh resume request names its predecessor attempt manifests and their
unresolved reservations, imports only pinned completed/salvaged checkpoints,
and supplies an explicit remaining allowance. In the same allowance lineage,
prior settled charges and unresolved full reservations are subtracted; a new
larger allowance is explicitly new authorization, never an implicit reset.
Unknown cleanup blocks automatic continuation. Whole-attempt monotonic clocks
restart only under that fresh request; the full-cost ledger carries prior wall
observations separately, not a false continuous original deadline. An owner
requiring a cross-restart deadline must also supply an absolute deadline under
an explicit trusted-wall-clock assumption. First implementation need not invent
a distributed budget ledger: this is one local owner's finite operation.

The portable library must not require dated experiment RESULT schemas as
mathematical authority. Its own request/attempt format can record imported legacy
costs and pins. Cold restart still verifies actual dependency receipts inside
the unchanged host and final receipt at the public admission boundary.

### Smallest qualification before a full launch

Use pure scheduler/supervisor-double controls for graph generation, missing-only
resume, exact argument order, reservation reconciliation/unknown costs, original
deadline exhaustion, source/input mutation, output overlap and finalization
failure. They establish controller behavior, not crypto validity. Reuse the
actual prefix for backend correctness; no proof stages are repeated merely to
test the scheduler. Independently review the public source and exact finite
owner request before root selects any325-call remainder. The ultimate gate is
the actual final receipt plus genuine cold public admission, not the controller
contracts alone. Root's full growth accounting also retains all prior failed
builds, snapshots, calibration, preparation and research costs under their
declared inclusion/scalarization policy; none vanishes in this new attempt.

## D21 decision: existing staged host, not a persistent prover rewrite

The actual base segment0 is retained and independently audited:
565.03125workerJobCPU+0.78125controllerCPU,81.7326653wholewallseconds,
234,817Bcheckpoint. Its stderr reaches `crypto` at135ms and `written` at80,685ms.
135/80,685=0.1673% is an observed wall fraction before crypto, not CPU share,
proof-phase timing or a guarantee for other calls. Saving all repeated capsule
reads therefore does not support a large speedup claim;7.02GBlogicalreads is
not evidence that I/O dominates.

Actual compiled SDK provenance is the compiler-artifact manifest paths under
experiments/general-checker-host-05/build-01/source/
risc0-3bbcd44d6459b9ef6ac0df3846dc9215514934e8/risc0. The host uses retained
native CPU backend features, includingcommons-inprocess-only/disable-dev-mode;
not a hypothetical unmodified SDK or GPU installation. Source establishes:

- zkvm/src/host/server/prove/prover_impl.rs: ProverImpl retains only ProverOpts;
  each prove_preflight creates a newsegment_prover, proves and verifies it.
- circuit/rv32im/src/prove.rs: segment_prover chooses new_cpu on this platform;
  its ProverContext is dropped after the call. Merely retaining ProverImpl does
  not cache that context or skip witness-specific proof work.
- zkvm/src/host/recursion/prove/mod.rs and circuit/recursion/src/prove/zkr.rs:
  each lift/join loads its program through XZdecode and Program::from_encoded.
  circuit/recursion/src/prove/mod.rs::Prover::run constructs a recursion prover,
  clones program/input, and performs preflight/witness/commit/finalize work.
  Recursion po2 is fixed18. Keeping only the public host API alive does not
  automatically eliminate these operations or any of219recursionproofs.

An explicit lower-level context/program cache could change some setup, but its
cost share, mutable-state reset safety and memory lifetime are unknown. It would
need newhost/dependencyintegration, build and assurance; it does not eliminate
109remainingsegmentproofs. No such rewrite is selected now. Avoiding a measured
small boundary is a poor reason to defer the first genuine reusable frontier.

### Cost reference and the cheapest decision-changing prefix

The already audited historical29lifts have mean104.268318965517CPU and
range100.78125..114.21875;29joins mean105.815732758621CPU and
range102.203125..116.703125. These source-linked retained observations are reused,
not reexecuted. Combining them with segment0 only as a SCENARIO gives:

    remaining base worker CPU reference
      =109*565.03125+110*(3023.78125/29)+109*(3068.65625/29)
      =84591.8362069seconds =23.49773CPUhours.

This is not a bound, confidence interval, wall prediction or complete production
cost. It excludesfinish,coldadmission,controller,failures,setup and childproof;
othersegments/tailpadding/resourcecontention may differ. A historical-segment
mean835.64709 instead gives a substantially larger scenario. CPUhours are not
wallhours because the prover is multithreaded. Do not derive runtime allocation
from these point estimates alone.

The selected source controller advances exactly this finite graph:

    retained segment0 -> lift0 ---\
                                  join1 (prefix0..1 only)
    capsule -> segment1 -> lift1 -/

Order is lift0,segment1,lift1,join1. This is four newstages, not reproving0, not
an applicationreceipt and not wholebasecertification. It provides actual new
image/lift/join compatibility while retaining every costly proof for eventual
finish. The analogous workerCPU scenario is879.38362069seconds. All110segment
checkpoints, including0/1, must remain available for finalhostfinish.

### Fresh prefix-controller source contract

software/v5/modules/receipt/advance_stages.py uses the unchanged owner supervisor
from product-local/v4-library-commons-02/commons-v4, the exact host03/image04/
capsule03 and retainedsegment0. It neither imports the used calibrationadapter
nor edits any usedsource/evidence. The owner selection has schema
DMKN_V5_RETAINED_PREFIX_V1; the only executable source pin is advance_stages.py;
this research note stays mutable for actual cost updates, not frozen as runtime
source. The exact selection and controller constants bind the finite operation;
inputs are the originaltenroles plus segment0/segment0_result. ImageID is exact.
No caller-specifiedcommands, arbitraryproofgraph or automaticremainder exists.

- Segment1:1500workerCPU/300wall; eachlift/join:250workerCPU/120wall.
  All have4096MiBJobmemory,2activeprocesses,1MiBstdout and1MiBstderr ceilings.
 250CPU is explicitpolicyheadroom above old114.21875/116.703125maxima, NOT a
  provenbackendbound. Totalselected2250workerCPU+60controllerCPU/660wholewall.
- Every call is clamped to remainingwholewall; setup/pins/writes are inside the
  samewall/deadline. Firstfailure stops; resourceoverrun, uncertaincleanup or
  finalizationfailure never becomes a success. MeasuredworkerCPU includesfailed
  stages; absentfinalJobcounter charges reservedCPU with explicituncertainty.
  The supervisor'sprocessCPU is nested in thiscontroller, never countedtwice.
- Inputs have an aggregate512MiB bound. At mostfournewcheckpoints each≤64MiB
  plus boundedlogs/reports/sources fit a384MiB/128entryretainedoutputenvelope,
  checkedbefore/afterstages and finalization. It is sampled/cooperativesource
  enforcement, not a filesystemquota or a hostileOS guarantee. The host's
  boundedwrite and supervisorlogcaps remain in force. Noinput is recopied.
- A fresh output directory and create-newfsync records preserve allsuccesses and
  failures. No cleanup, deletion, retry or automaticbudgetrenewal occurs.
- A separate fresh ownerselection may pin a contiguous previouslycompleted
  prefix and run only its missingsuffix; the firstselection has completed=[].
  Each retainedstage must match exactinputidentity/binding/kind/index and a
  cleanboundstageRESULT withoutstagefinalizationfailure. It additionally pins
  the enclosing invocationRESULT, requires completedstage membership and valid
  finalinputbinding, and refuses an outerfinalizationfailuremarker. Reuse from
  an outerFAIL requires an explicit ownerallow_failed_invocation=true in the
  newselection; it never relabels the oldinvocation or itsbudget as passing.
  SavedJSON only selects
  resumework: the unchangedhost cryptographically verifies actualdependency
  checkpoints upon consumption. No detached PASS label grantsmathauthority.
- Result accounting is THIS invocation'sworkerJob+controller. Retainedprior
  work is explicitlylisted, not claimedfree and not chargedtwice. Root'sfull
  growthaccounting must additionally include allpriorattempts and setupcosts.

No actuallaunch follows solely from this sourcecontract; independent exactsource/
selection review and root's finite decision are separate. A later fullcontroller
may accept another finitegraph under freshselection, but this source currently
cannot run index2..109,resolve,finish,guestexecution or admission.

Current source proposal: `advance_stages.py` SHA256
`f67e493d409e4b3772e40115a21ee501f59d590ea71d4873e5daced090c82a33`.
Exact first selection: `experiments/v5-local-checks/module-base-prefix01-selection.json`,
SHA256 `6e4b8922bb6bf981ec05917f2bbe7c614118f4a002f34b11c0c9819559625920`.
It retains segment0 and starts with `completed=[]`. Source-only AST inspection
passed; subsequent root launch and independent actual audit now pass as recorded
in D22 above. This lane performed no launch. The completed four-stage prefix
leaves108 segment/lift/join triplets plus finish:
325 further calls, plus cold admission. Any producer successor must reuse all
five retained checkpoints (segments0/1, lifts0/1, join1), not replay them.

### Beyond the base: selective certification is the substantive cost lever

After genuine basecertification and new-image recursive child/coldadmission,
prioritize boundednative deltaDAGs above exactcertifiedfrontiers. They avoid
certifying each smallcontribution and avoid historydownload below a realfrontier.
If sealingcost isS, nativedeltaverificationcostD and receiptreusecostR, sealing
has positive amortization only whenn(D-R)>S after incrementaldiscovery/storage/
service/failure costs and equalbaselineendowment; D>R is necessary. Frequency is
a localheuristic for future n, not proof ofbenefit. See
DELTA-FRONTIER-NATIVE-SEAM.md for exactparentjournalinduction/ownerpolicy/resource
conditions. The presentguest cannot consume nativeVerifiedDelta as a receipt;
selectivefrontiers supplement, not fictionalize, cryptographiccertification.

## Backend cost evidence already available: reuse, do not rerun

The retained independent audit
experiments/certified-collection-01/SUFFIX02-OUTCOME-AUDIT.md fixes actual
indices3..31:29segment,29lift,29join stages. They use the retained native proof
backend and po2=18 selected in SNAPSHOT-OUTCOME.md. It checked exact stage/log/
artifact/result bindings and clean process closure. Do not infer final campaign
completion from that prefix audit, and do not repeat its87stages for calibration.

| Kind | Observed stages | Inclusive worker CPU seconds | Mean per stage |
|---|---:|---:|---:|
| Segment |29|24233.765625|835.64709|
| Lift |29|3023.78125|104.26832|
| Join |29|3068.65625|105.81573|

These are whole-stage costs, not isolated prover timings, extrapolation bounds,
or a prediction for v5. The prefix's largest observed worker stage was893.453125
CPU seconds; largest wall67.1031363seconds; largest Job private commit3,521,454,080
bytes. The three-stage wall sum averaged121.66633seconds per index. Individual
stage controller sums are nested in the enclosing campaign's eventual process
CPU and must not be counted twice. Retained failed/setup/cold-receiving costs
are additional and must not disappear in a new growth comparator.

This demonstrates a central economic issue: cheap VM execution or cold receipt
verification does not imply cheap proof production. No estimate obtained by
multiplying a native Lean/checker timing by a made-up factor is valid. Different
segment composition, tail padding and available host resources can alter cost.
The current backend still uses software SHA in its M3 kernel; changing a version
register alone cannot create a sound accelerated proving backend.

The SAME retained audit has a terminal extension for the old 66-segment
collection; this does not extend the new v5 prefix. Its actual finish was
2.796875 worker CPU seconds and cold verify0.015625 worker CPU seconds
(12ms inner verifier). The complete old campaign's known accounting was
3,309.671875 carried setup/failure CPU +66,163.046875 worker CPU
+166.203125 final controller CPU =69,638.921875 CPU seconds, with
7,690.7769043 saved wall seconds. Those totals include the old campaign's
63 triplets after its recovery; nested per-phase controller figures are not
added again. They are retained producer/finish/cold-cost context, NOT a bound
or speedup measurement for current110segments. Finish's additional segment
verification scales with the finite receipt vector; neither its small old
cost nor a cheap cold receipt justifies ignoring current full proof production.

## Exact operation graph in the current selected host

For n actual capsule segments and p distinct actual parent assumptions, the
module host performs n segment proofs, n lifts, n-1 joins, p resolves, one
finish and one cold application verification. This is3n+p+1commands after the
single snapshot; including snapshot gives3n+p+2. Preparation is additional.
Cold public admission can serve as the cold verification endpoint; do not run
an otherwise identical extra cold verifier just to manufacture another gate.

Every later stage reads the SAME capsule and binds exact image/input/expected
journal/limits/parent receipt bytes plus capsule hash. It does not reexecute
the guest. Segment/lift/join/resolve consume and verify their cryptographic
objects. Finish additionally verifies every segment and the composed receipt,
matches composite and succinct claims to the exact session claim, and performs
full empty-assumption application verification before emitting a receipt.

Cost accounting remains:

    P = snapshot + sum(segment) + sum(lift) + sum(join) + sum(resolve)
        + finish + coldAdmission + allController + allFailedWork + allocatedSetup.

Host input parsing, hashing, parent verification, repeated full-capsule reads
and decoding are inside actual stage costs, not free. Their repeated reads
scale with capsule size times stage count; no claim of constant producer cost
follows from succinct receiving. Current64MiB capsule/file,512MiB aggregate
per-call reads,128segments and8operational parents remain finite limits.
They do not authorize unlimited whole-campaign retained storage or cost.

Once a successful actual new capsule supplies n and segment sizes, a defensible
next calibration is ONE selected segment stage from that SAME capsule, retained
for later composition. It must not be discarded/repeated. Its observed cost
and historical lift/join envelope can inform a finite campaign decision; they
cannot prove an upper bound for every remaining segment. Do not preauthorize
all128possible segments because the host format permits them. If actual cost
is unacceptable, stop the selected campaign and preserve its useful artifacts.

## Smallest real base-to-child certificate integration

### Actual base-capsule census, not a timing forecast

Snapshot03 now exists:110segments,0assumptions,21,274,865capsulebytes. For the
CURRENT host stage interface, a full base receipt requires110segment calls,
110lift calls,109sequential-prefix join calls,0resolve calls and1finish call:
330post-snapshot calls. Snapshot/prepare and cold admission are additional;
the actual retained successful segment0 leaves329 calls, not restart330.
This is an exact source-derived action census for this interface, not a lower
bound on every possible prover API or permission to launch those actions.

Every current post-snapshot stage reads the full capsule before its branch.
Those330 calls therefore logically read at least7,020,705,450capsulebytes
(330 times21,274,865), before wrapper rebinding, decoding/hashing, checkpoints,
image/frame/journal inputs or cryptographic work. Logical reads are not physical
disk traffic: OS caches may satisfy them. This cost does not imply7GB retained
storage. An operation-bound indexed/mapped capsule API could change the repeated
read term, but is neither implemented nor selected by this observation.

One segment calibration cannot bound the other109segment costs,110lifts,
109joins or finish. Full producer budgeting must separately justify their
resource envelopes and retained storage, including failures and any new child
proof. The actual completed execution and110-segment census alone do not make
whole-module certification economical for low-reuse contributions. Selective
native deltas remain a complementary route, not a substitute for this real
certificate/recursive-composition/cold-admission gate.

Base and child use the same actual newly adopted image and existing mathematical
policy. Their ModuleIDs/semantic group/body commitments do not include image
identity. Their certificates nevertheless cannot be relabeled across images.

1. Reuse the actual retained profile2 base snapshot03 and successful segment0.
   Complete only newly selected finite proof stages, then full cold public admission of
   the genuine base receipt. Stage/checkpoint labels alone cannot authorize it.
2. Construct one fresh child request from the held fusion mathematical input:
   one local group, one parent, rank1,11body openings,1054native rows. Preserve
   its semantic spec and native witness rows; use relationV2 and actual image.
   Replace the old SYNTHETIC parent statement with the actual base journal read
   from the newly verified receipt. This is receipt consumption, not profile
   projection. Preserve selected openings and independently require they verify
   against the actual base group root/ModuleID. Require exact rank0parent/rank1child.
3. The current host prepare command does not rewrite parent journals. Supply
   the exact genuine base receipt to child snapshot. Host checks its full
   application receipt and exact selected journal; guest performs env::verify;
   snapshot records the one proven assumption in exact claim order.
4. Produce child's n_c segments/lifts/joins plus exactly one resolve using that
   genuine base assumption. Finish must yield a full empty-assumption receipt;
   stopping at a conditional child claim is NOT completion.
5. In a cold receiver, admit only child receipt, adopted image/profile and
   expected ModuleID through the public same-call gate. No base receipt/source/
   witness/proof ancestry is supplied to this receiver. Selected group openings
   and demanded computational bodies remain necessary for later semantic use.
6. Build new-policy discovery records from these actual certified modules,
   then run root's selected discovery/acquisition/use boundary. The retained old
   policy database cannot be relabeled. Broader feedback/growth evaluation is
   root-owned and is not implied by a two-module crypto loop.

This is the minimum profile2 recursive-composition/ancestry-independent
receiving discriminator. It does not establish broad Lean/Mathlib support,
arbitrary huge-network reachability or net useful-growth advantage. It avoids
another generic negative/control campaign: changed-boundary negatives should
target real certificate admission and unresolved/tampered semantics once those
objects actually exist, retaining prior audited unrelated tests.

## Growth decision supported by this evidence

Let P be measured one-time module certification cost and let delta_i be the
measured/model-supported GROSS consumer-work reduction for independent use i,
before separately charged search, service, storage and other overhead below.
Use a declared same-unit scalarization (or compare the full resource vectors)
and give both systems the same native/library/cache endowment. In particular,
do not charge search twice or handicap the baseline by withholding its existing
reusable checked cache. Certification is beneficial only when
sum(delta_i) exceeds P plus incremental search, service, storage, replication,
failure and migration costs. For constant delta>0 this requires N>P/delta;
neither a theorem count nor library popularity alone establishes that inequality.
Reusable certificates make positive amortization possible at large demand and
large ancestral proof cost; they do not guarantee it for this small fixture.
Scope, assumptions and the useful capability comparator remain explicit.
