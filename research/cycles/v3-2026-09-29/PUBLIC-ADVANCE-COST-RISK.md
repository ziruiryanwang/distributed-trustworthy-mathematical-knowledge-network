# Public advance: controller-cost risk, not an observed failure

2026-09-29; census_review. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

**Decision:** this is a consequential, inherited but unqualified producer-cost
risk. The public controller repeatedly traverses a growing operation and its
large installation; the passing research prover does not use that control
path. Do not infer that one full public advance fits600 controller CPU seconds
or7200 wall seconds. No measurement here establishes that it fails either.
The suspected new Rayon restriction is **not** a difference from the base
campaign: both explicitly set `RAYON_NUM_THREADS=2`.

This source-only review selects no runtime, imports, compilation, proof,
prototype, file copy, installation-wide hash or live91114 inspection.

## Actual control paths

Source04 `cert_stages.py` lines392,478,511,518 and549:

- `Session.observe` checks controller CPU/wall/deadline/memory, then runs
  `storage_census(self.run)`. Every live worker polling iteration calls it,
  followed by a50ms sleep. The interval is scan/check time **plus**50ms,
  not exactly20 scans per wall second.
- Census enumerates the whole operation, not only the current command's
  outputs. Each entry rechecks its ancestor directories; live mode avoids
  repeated leaf resolution but still performs metadata work proportional to
  the visited path/depth population. Quiescent checks additionally resolve
  each entry. No strict asymptotic filesystem-time bound follows.
- Every `invoke` rebinds before launch and after clean closure. Each rebind
  invokes installed rebinding, rehashes **all** retained immutable operation
  pins, and performs a strict whole-operation census. It is not merely a
  constant-size current-stage check. Completed command logs and artifacts
  stay in the pin map and operation tree.
- Installed `cert_workflow.py:206` enumerates its entire file population in
  every `rebind`, including crypto-only calls. The current profile has12,395
  mapped assets. Crypto-only selection changes byte hashing, not the exact
  presence census:599 selected assets/98,658,426 mapped bytes, derived from
  the profile's metadata and actual `crypto_assets` predicate. These counts
  are not a new installation census or timing run. Initialization additionally
  does full asset adoption; other final checks add cost too.
- The public advance wrapper also independently observes its owned roots.
  Its controller is distinct; outer-tree CPU includes the public controller
  and inner workers. Increasing an outer allowance cannot remove the public
  profile's600CPU/7200wall limits.

The installed profile also imposes1800 worker CPU/600wall per ordinary proof
stage,300CPU for finish/verify,8192 operation descendants and12GiB storage.
The600-second controller charge is a conservative **reservation** per public
invocation; it does not mean600 seconds have actually been consumed.

Research comparison: `run_certificate_phase02.py` constructs one fresh
per-stage directory. `scale-equation-01/runtime.py:98..120` polls cheap worker
checks every100ms but schedules `budget.refresh` only every10seconds, plus
final refresh. That refresh scans the small stage allocation, with declared
static inputs separately reserved. It does not revisit a growing public
operation or12,395-file installation at each proof stage. Its low controller
cost therefore cannot qualify the public controller by inheritance.

Both environment constructors explicitly select Rayon2: source04
`cert_stages.py:473` and base phase02's selected
`scale-crypto-01/provision_build.py:84`. This does not establish identical
performance or cap every native thread to two; it refutes this particular
claimed new environment difference. Do not estimate wall by dividing total
worker CPU by2.

## What previous results do and do not establish

The global50ms observer, per-stage installation census and operation rebinding
already appear in contributor03. Source04's live-census change repaired
cooperative temporary-file handling, not their frequency/locality. This is
not a newly introduced source04 defect, and it has not been qualified by an
old successful public advance.

- Collection `CENSUS-TEST-OUTCOME.md` passed33 deterministic contracts and a
  five-descendant ordinary smoke. Its0.09375 inner CPU seconds is not a
  large-operation scan benchmark or a long-running controller test.
- Contributor04 `OUTCOME-AUDIT.md` passed13 changed-boundary contracts. Its
  invoke control used a fake worker and fake Job;1.28125 actual suite-worker
  CPU seconds cannot estimate genuine multi-stage production cost.
- Contributor03 `PREPARE02-OUTCOME.md` measured25.265625 public-controller
  CPU and35.6295188 public wall seconds across three inner commands, whose
  own measured worker CPU totaled9.390625. That successful compatibility
  observation includes initialization/native asset checks and cannot be
  divided by3 to estimate crypto-only stage rebinding. Nor does it validate
  hundreds of public stages. The original raw comparison failure remains.
- The already adopted suffix02 audit cut, stages3..31, measured87 workers
  totaling30,326.203125 CPU seconds; nested phase controllers37.71875CPU;
  summed phase wall3528.32370070013 seconds. Largest phase wall67.1031363
  seconds. Those are preserved **research-path** observations, not source04
  forecasts. No later live stage was inspected for this review.

## The actual risk model

After real preparation, read its actual `N` and `A`; no research/predecessor
segment count may substitute. Full public sequence length is
`S = 3*N + A + 1`; here intendedA=1, soS=3N+2. Before optional extra final
checks, that path performs at least2S full installation presence scans and
approximately2S crypto-subset hash passes. The latter means roughly
`197,316,852*S` logical file bytes presented for hashing; it is not physical
disk traffic because caching and implementation details matter.

The controller-cost decomposition is:

```text
C = initialization + installed rebinds + operation-pin rehashes
    + live and quiescent storage scans + remaining controller work.
```

If `I` denotes measured representative CPU for one crypto installation rebind,
`2*S*I` alone can be compared with600, but a sample is not a rigorous lower
bound on every future call. Growing pin/hash and path work can produce
quadratic cumulative overhead in stage count when each stage contributes a
nonzero retained payload; live scan demand also depends on proof wall time.
Finite maxima bound a particular operation, not its practical affordability.

For scale intuition only, scanning that costs `a` CPU and `d` wall seconds
once per `d+0.05` seconds contributes about `W*a/(d+0.05)` CPU overW worker
wall seconds. Even modest per-scan work can exhaust600CPU during7200wall.
This is a conditional model, **not measured scan latency**, a failure
probability, or permission to spend the whole limit on observation.

The failure consequence matters: an invocation controller-limit error can
kill an active worker and leave `STAGE_FAILED_NOT_RESUMABLE`, not a clean
READY boundary. Do not discover a predictable overhead problem by selecting
a many-hour all-stage invocation without checking its fit.

## Smallest cheap falsifier if root needs a decision before advance

First use the actual successful prepared record to determineN,A,S, current
tree/pin counts, original charges and deadline. This is read-only evidence,
not another preparation or a fabricated workload. If there is no prepared
record, retain this risk as conditional and wait for its existing gate.

If fit remains doubtful, root can separately select **one read-only primitive
cost screen**, not another proof campaign: installed Python, unchanged pinned
modules/profile, a fresh report-only allocation and no mutation to the
prepared operation. After one genuine installed initialization, measure two
crypto-only installed rebind calls and five strict storage/pin observations
of that same quiescent prepared operation. Record each CPU/wall sample,
actual read/entry counts and startup separately. No native/driver/verifier,
public advance or proof calls. Prospective ceilings:30CPU/120wall/512MiB,
64KiB report output and4GiB explicit read budget; independently reviewed
enforcement and root selection are still required. No screen is implemented
or run by this note.

Use the **faster** of the two rebind samples in `2*S*I` as an optimistic
engineering estimate. If even that plus measured initialization and an
explicit safety margin cannot fit600, reject the *one-invocation launch
plan* before spending proof work. A screen timeout is its own failed finite
screen, not a theorem that public advance must fail. If the estimate fits,
that does not qualify later growing-operation scans or total proof wall;
report remaining uncertainty. No cold-cache reset or synthetic thousands-file
tree is needed for this first decision-changing check.

A different legitimate choice is finite public continuation at clean stage
boundaries. It changes the current all-stages-once experiment and adds600CPU
reservations and full startup per invocation; it is not a free fix, and it
must not renew the original operation allowance/deadline. If a source remedy
is selected instead, preserve used source04: a successor should separate
cheap fast resource checks from scheduled storage checks and bind immutable
installation inputs at explicit invocation/stage trust boundaries. Such a
change needs stated cooperative-owner assumptions and changed-boundary tests;
silently removing tamper checks or increasing caps is not the recommendation.

Terminal AB audit takes precedence over this conditional screen. Existing
proof91114, passed contracts and old proof costs must not be rerun to answer it.
