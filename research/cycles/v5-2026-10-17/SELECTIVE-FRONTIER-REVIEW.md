# Independent review: certify the required frontier

2026-10-17, `v5_growth_decision`. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
Authority: `SELECTIVE-FRONTIER-SELECTION.md`; read-only source/evidence review
and this checkpoint only. No product imports, native execution, tests, proof,
build, old-source/evidence edits or Git operations. The workspace guard passes.

## Decision: target-preserving at the consumer, changed at the producer

The selected public integration initially acquires exact J_FIRST, uses its
interface with required BASE semantics, authors SECOND by applying FIRST twice,
and has a cold recipient check SECOND. The initial receiving endpoint never
required SECOND to be a certified member. Selecting the prerequisite frontier
therefore preserves this integration's exact mathematical endpoint while
removing work not needed for its initial certificate.

This is nevertheless **not completion of the old producer claim H**. The old
three-member seal contained BASE/FIRST/SECOND; the new two-member seal contains
BASE/FIRST. The old po18 layout failure and old complete po19 capsule remain
frozen. New H, membership paths, wire, session and capsule identities must be
disclosed. A/I/F/P and exact J_BASE/J_FIRST stay unchanged. SECOND retains its
same exact target J_SECOND at the downstream native check; no weaker theorem,
rank substitution, alternate derivation or policy is supplied.

## Source argument: backward-closed restriction

Read `aggregate_claims/input.py`, `relation.rs`, `bindings.py`, `membership.rs`,
the relevant actual native-controls preparation and the complete terminal-gate
plan. V2 graph nodes are exact184-byte journals, not semantic ModuleIDs.

Let the retained successfully conditionally checked graph be

```text
BASE(rank0) <- FIRST(rank1)
BASE(rank0) <- SECOND(rank2) -> FIRST(rank1)
```

Here arrows from a delta point to its required exact premises; equivalently
the premise sets are Parents(FIRST)={BASE} and
Parents(SECOND)={BASE,FIRST}. Thus the backward closure of target FIRST is
exactly {BASE,FIRST}; SECOND is a descendant, not an ancestor.

For the actual source's deterministic per-frame checker, restricting the ordered
witness sequence to this closure preserves FIRST's local check and every exact
premise. The only retained assumption descriptor is the same I/J_BASE claim,
and it is used by BASE's exact legacy frontier. The sole newly checked delta is
FIRST; rank1 equals1+rank(BASE). `Graph::closure([J_FIRST])` reaches every retained
node and no extra member. Census limits are upper bounds on nonnegative frame
charges/maxima; removing a frame cannot increase them. This is a source argument
for the existing relation, not a claim that preparation alone verifies a receipt.

The unchanged guest must still verify the genuine I parent. The unchanged
snapshot host still derives the conditional conclusion from the new wire,
compares its exact new H, verifies parents and completes the actual guest session
before it can emit a complete capsule. The eventual receiving A verification
remains mandatory. No checker, native host, guest, SDK or authority rule changes
are needed merely to select this closed subgraph.

Three source-provable obstructions prevent pretending this is the old claim:

1. Keep SECOND's witness but target only FIRST: `Graph::closure` refuses unused
   delta material outside the target closure.
2. Drop SECOND's witness but retain target J_SECOND: the graph refuses a target
   that is not an exact newly checked delta warrant.
3. Drop BASE's frontier/claim while retaining FIRST unchanged: FIRST's exact
   parent is unestablished; its witness cannot be accepted by erasing its premise.

The old H/member openings cannot certify the new set. Commitment leaves and
internal/root hashes include the member count; even BASE/FIRST's retained bytes
need newly computed openings under the new count-two root. Changing only an
old header's count, or recycling its sibling hashes, is not valid preparation.

## Exact retained data and smallest input change

Read and hash the preserved data, using no project imports:

| Item | Bytes | SHA-256 |
|---|---:|---|
| FIRST witness / original `child-input.json` | 113,220 | `88b71b8282afc99297bf6564d22616fce6211eed9a9e18afa1cb42a41d1206e1` |
| Exact J_FIRST / `child.expected-journal` | 184 | `07734789fd165d5c29667a2925c09b882d346db97a511c75644f2cb4b8ccd0da` |
| SECOND witness frame in old aggregate wire | 101,687 | `ea66d3efa6d4f461ed39adab3a640b9cfa6204def165254225720085ecfb23d4` |
| Corrected retained delta packet | 662,480 | `54c7dac7f83a9a06c2b23b17a77be20364c1b90e4cd3b1db58b69c62fda2dcf1` |

The old215,540-byte wire has exact counts1claim/1frontier/2deltas/1target,
legacy claim tag0, no frontier siblings, and target J_SECOND. A read-only
fixed-integer framing inspection reaches exact EOF and confirms its FIRST
frame is byte-identical to the pinned113,220-byte child input. FIRST has1,355
proof rows, one local theorem group and one exact parent J_BASE; SECOND has
the BASE/FIRST parents. The retained ordinary Lean SECOND source uses FIRST
twice through `Eq.trans`, so omitting SECOND from H does not remove that genuine
use obligation from the downstream gate.

Smallest fresh preparation through the existing encoder:

```text
claims    = [(0, J_BASE)]
frontiers = [(0, J_BASE, 0, [])]
witnesses = [unchanged FIRST witness bytes]
targets   = [exact J_FIRST]
```

The resulting wire length is113,849bytes:60-byte prefix/counts,185-byte legacy
claim,196-byte legacy frontier,184-byte target and4+113,220-byte witness frame.
This removes exactly101,691bytes relative to the old wire (SECOND plus its
length word); it does not quantify execution cycles, proving CPU or peak memory.
The expected H has two sorted members, maximum mathematical rank1 and seal
height1. Its root must be derived from the exact two journals, with all new
member openings structurally rebound before the host call.

Implementation advice: one fresh adapter, not another compiler or protocol.
Reuse the already reviewed bounded owner-record parser/build adoption/closure
helpers. Verify old wire prefix/counts/claim/frontier/target/frame lengths/EOF,
hash and preserve the original FIRST frame, use existing v2 encoder/bindings,
and save a separate old/new-target derivation record. Do not add diagnostic
fields to producer-consumed exact config/result schemas. Keep the actual
po18/N256/2^26 and file/output bounds, one genuine parent and unchanged native
command. Source identity and full original/fresh lineage remain explicit.

## Growth and cost interpretation

This is a legitimate selective-certification design: certify the useful
prerequisite closure, not all locally known descendants. It can reduce avoidable
producer input/work while preserving the selected acquisition-to-extension
capability. It does not prove the remaining workload fits its envelope or that
the smaller seal has positive net benefit.

For comparison with the optimized ordinary-library route O and local route L,
fix the **same consumer workload**: acquire/use exact FIRST and needed BASE
semantics, then check exact SECOND. O may share the same FIRST and use ordinary
proof-DAG sharing/caches; it must not be forced to download or certify SECOND
before authoring it. Both routes get the same local optimizations. For V, include
the new frontier's full certification/distribution/maintenance, all failed
attempts under the declared account, and later SECOND checking/publication.
Do not compare new V's first-only certification cost to old V's whole-three-node
seal and call that an equal-H speedup. It is disclosed target-set selection.

Historical costs remain in the historical ledger; a forward investment does
not repay them artificially, and a from-genesis comparison states which costs
it includes. The existing positive-margin/service-capacity conditions still
apply. SECOND is retained mathematics even though it is now outside the new H;
this gate can demonstrate reciprocal software capability, not global novelty,
positive growth, guaranteed demand or final-v5 readiness.

## Current disposition

**No conceptual blocker to the selected narrower certification frontier for
the unchanged public J_FIRST-to-J_SECOND capability.** The old target-H
obligation is explicitly not completed. Exact adapter/plan review and any actual
complete-layout result remain pending. The current failed full-workload capsule
cannot be reused or relabeled, and no proof/native manifest campaign follows
automatically from this review.

## Exact adapter and selection review

Read complete coherent `software/v5/aggregate_small/frontier_snapshot.py`, then
its final docstring-only `certifies` to `selects` correction. Final file is
13,788bytes/SHA-256
`e734200f76510b73fdb6cd3346d07dfc085ff1eabfce183db97ce0eda5f6a00d`.
The unchanged existing v2 input encoder is5,679bytes/SHA-256
`d40b611e288fd73a060df021809e403f80b1e6c16ca8b81ff2fd528d1f2fe61f`.

The adapter imports its exact sibling02 helper directly, avoiding
`aggregate_small.__init__` and unintended producer imports. That helper installs
the selected v5 source root for existing codec/bindings imports. The new
encoder dependency is explicitly selected, not taken from ambient Python.

The source verifies pinned original wire/reference, exact1/1/2/1 framing,
legacy claim/frontier, original target, both frame extents and exact EOF.
It reconstructs the whole old wire with the existing encoder before producing
the new1/1/1/1 input, preserves the first frame hash/bytes and exact parent/rank,
and constructs/rebinds the two-member header/openings. The independent old-wire
inspection above agrees with its literal offsets and expected113,849-byte result.
Its separate derivation record exposes old/new H, retained target, omitted
descendant, both witness pins and unchanged genuine parent. The file is saved
create-new, final-rebound and included in output census; it is not authority.

The actual snapshot invocation, same host/image/parent adoption, po18/N256/
2^26 limits,96MiB capsule and208MiB/288-entry output restrictions remain.
Successful result/config field sets match the producer's exact `_snapshot`
adoption contract. The changed descriptive scope string is not an authority
condition. No new extra result field, host fallback or implicit receipt exists.

Read `Select-FrontierLayout01.ps1` completely:5,680bytes/SHA-256
`5749ed7f4b644f009dde3f8569e6e6eb623319d76b0db089b8e7ca5e56e7cf14`.
It preserves the old exact preparation basis and actual adopted snapshot build,
pins the two required added sources, requires fresh output, and writes only new
selection/configuration files. It never invokes Python/native/guest/proof.

Exact generated files under `experiments/v5-local-checks/`:

| File | Bytes | SHA-256 |
|---|---:|---|
| `selected-frontier-layout-01-selection.json` | 11,394 | `05888ba9f7fffb600c6b117f39bdfcb8e0b58b870ed311147a557ccd80dfcb45` |
| `selected-frontier-layout-01-configuration.json` | 2,868 | `02cccc1cda2ac7a6a4971f5e077e04b26fcfa4dc384ff01cf84bfa4c3d5b6431` |

All10 selected source hashes and all36 runtime pins match actual bytes.
Thirty-five runtime pins are identical to layout02; only the fresh configuration
replaces its predecessor. Configuration differs only at the output path; the
changed mathematical input is derived by this exactly selected source, not
silently inserted into an old configuration. Limits remain180CPU/240wall/
3072MiB/three processes and1MiB logs. The selected run directory was absent.

**Source/exact-plan disposition: no blocking issue found for this one complete
BASE+FIRST execute-only layout.** Root owns launch; no reviewer execution,
proof funding, full-old-H completion or proof-memory claim is supplied. Actual
outcome and preserved target/semantic/cost boundaries remain to be audited.

## Actual selected-frontier layout01 outcome

Independently inspected the saved terminal run; no rerun or project import.
All10 original sources and10 actual source snapshots match exact plan05888ba9;
all36 runtime pins match. Read both enclosing/native result chains, actual
command, diagnostic and separate derivation. All167 retained segment files
0..166 match their exact diagnostic lengths/SHA-256. All havepo18 and total
32,964,887bytes. The completed session records43,778,048 padded rows,
47,430,434 instructions and4,205,234 padding rows; these measures are distinct.

The113,849-byte actual wire is
`898660ddeea92cefccbf793e35b1ee49ef4867c9daec24b5344f37a1ed375500`.
Its target is byte-identical to exact J_FIRST, and its sole113,220-byte frame is
byte-identical to the original FIRST input. The actual192-byte H is
`49dd845edaec83f5b0cba5af38653f768e51ed95a4bb6ea7824c10bdd1c3169e`.
It has2members/maxrank1/sealheight1. A separate read-only .NET SHA-256 calculation
from exact J_BASE/J_FIRST and the existing count/domain formats reproduces the
new root and both one-sibling openings. Saved derivation H and actual native H
both equal these bytes. SECOND was not substituted into the selected set.

The complete capsule is32,965,324bytes/SHA-256
`6e41621e2595c252328eaf5f34862c6d6f913caecb68117406bcd616a61b44a5`.
Its actual magic/version/session prefix agrees with the recorded
`9c87448ba08ae98273ac6fc1df8a41a22716db8be686ce473eb5fba874a1475d`.
Reported capsule binding is
`e56cb33f432a4c5bbdb0624eb2a072db48562e26c77fc20cefd0da8831585a2b`.
Actual same-A host verified the unchanged genuine I/J_BASE parent and completed
one guest session, resolved claim/materialization and durable capsule write.
Proof calls remain zero and mathematical admission remains false.

| Saved record under `selected-frontier-layout-01/` | Bytes | SHA-256 |
|---|---:|---|
| `RESULT.json` | 2,114 | `f11c567f70d5543fe648f32df2bb254736deada086bcc40e3f6b01c87d493d6f` |
| `evidence/RESULT.json` | 3,857 | `da1acf4d2469e92ffde297648702fe4c281406353fb3691a4a7d5ffa3efd484e` |
| `evidence/diagnostic.json` | 32,640 | `a3e81713cc7438d2c1a385e94fb8679523774056b5452c9f99b35cbce6033e28` |
| `evidence/selection-derivation.json` | 6,350 | `1750785cbde497cbd60f371203ce67cbf35844aaf9422782b65f03c2d1561941` |

Outer exit0, child reaped and Job closed, no active/terminated processes,
cleanup errors or termination request. Inclusive JobCPU3.53125 plus disjoint
wrapper0.296875 gives3.828125 known CPU seconds; outer wall3.1815756s. Do not
add nested supervision/phase measurements again. Peak Job private commit is
98,336,768bytes, an execution observation rather than proof-memory evidence.
Native read reservation is35,048,442bytes. Whole-run final census is192files/
203entries/66,178,982bytes; evidence pre-result census177entries/66,088,738bytes
is a smaller explicitly different scope. Actual native stderr is empty.

**Actual disposition: PASS for this exact complete BASE+FIRST execution layout
and clean closure.** It resolves the immediate missing complete-capsule
prerequisite for the selected smaller frontier. Its graph has3*167+1=502host
calls/501checkpoints under the existing controller, but this is structure, not
proof funding or a measured proof price. Real constructor/request admission,
native manifest behavior and an actual full-po18 segment remain separate.
No A receipt, cold terminal acquisition, net growth, previous three-member-H
completion or v5 release follows. Downstream plans must explicitly adopt this
new H and openings before their future exact selections; old claims stay frozen.

## Ordinary operator and preflight-selector source review

Independently reread complete `aggregate_small/operator.py`, its selected source
contract and `SMALL-OPERATOR.md`; traced the actual retained constructors,
`_request`, snapshot/build adoption, close and run boundaries. Exact operator:
11,480bytes, SHA-256
`8a4876c28b1da2fbf80b3e425aa0f05486aa760a9b77cfe6d2d6c0a66dcffac6`.
**No blocking source finding for this explicit local-owner contract.**

Preflight constructs the real owner and calls `_request` once, with no native
dispatch; all host dispatch remains inside the uncalled run branch. Actual
retained `P.Producer` enforces Windows, isolated/no-site/no-bytecode and no
optimization. Run invokes one finite attempt, checks the exact durable result,
and does not treat a successful prefix as a certificate. The wrapper closes a
constructed owner, checks loaded module origins, bounds and pins documents,
separates fresh report/sentinel paths from inputs/output/installation, rebinds
sources and derived preflight inputs, and marks late failure with a distinct
sentinel. Startup/imports, failed construction and output tails remain the
enclosing owner's resource responsibility; this is not a hostile filesystem
or hostile-source security sandbox.

Also read the complete fresh `Select-FrontierPreflight01.ps1`. It selects six
source files, canonical future snapshot source pins, actual new stage/snapshot
builds, original adopted image and genuine I parent, and exactly the successful
167-segment BASE+FIRST capsule/new H. Its argv is `preflight`, not `run`, with
`--owner-report`; the selected outer limits are30CPU/90wall/512MiB/two processes.
502stage entries are only a full-path quote, with no checkpoints or prior
production attempts. No production output or proof operation is selected.

The quoted cap sum is284,550workerCPU seconds and90,750workerwall seconds,
not an expected cost. The carried subtotal includes retained BASE and both
host links, both failed layouts and the successful selected layout, explicitly
excluding other preserved development/search/service costs rather than setting
them to zero. This is not a full-cost growth comparison. Selector source is
clear to generate one exact selection; generated plan/profile/request and
source pins must still be checked before root chooses any actual preflight.
No execution, project import, test/build/proof, capacity poll or Git operation
was performed for this review.

### Exact preflight selection clearance

Selector source is11,955bytes/SHA-256
`4db4bfb673996d6d60384bd575e0762459b90c1d5a8e8499dc63dab02c6ee08d`.
Independently checked the generated documents and all six original source pins
(98,271bytes), all63 selected runtime pins (129,298,894bytes), and four future
producer-source paths/lengths against the source map. No mismatch. Both run
directory and planned production directory are absent at review time.

| Document under `experiments/v5-local-checks/` | Bytes | SHA-256 |
|---|---:|---|
| `selected-frontier-preflight-01-selection.json` | 17,789 | `ec1f61b7632e368196cb93d89e40c036c6fd7a71656a9aaefd343bf3da2b6b16` |
| `selected-frontier-preflight-01-profile.json` | 18,899 | `d561265970d67ac888909c9edd93578a4dd5298b2ec810b1fe382cab1eaced6c` |
| `selected-frontier-preflight-01-request.json` | 9,989 | `1d8a7a03c7ac0c8f14c3a67e594e70fef9cd69300de4150a2af480397d937d9f` |

**Clear for root to select this exact one preflight only**, under the stated
30CPU/90wall/512MiB/two-process outer limits. No proof funding or cap sufficiency
follows. Prior base/layout/build operational evidence is reused, not rerun.

### Actual ordinary preflight01 outcome

**PASS for this exact constructor/request preflight and clean closure.** No
rerun or project import. All12 original/snapshot source bindings and all63
runtime pins match. Independently reconstructed the full ordered502-stage DAG,
canonical profile ID
`d6a8d91d6f2f068cb13b938c7439b94893f64f81376d3f2fee48d2bdd04a2dc5`
and session ID
`fb1ada11057248e82cc204c95ad676e2d7b35701264a8bb1a251461703b907b9`
using read-only PowerShell/.NET, without calling product code. All agree.

The exact graph has167segments,167lifts,166joins,one resolve andone finish.
Its reconstructed requested cap quote is284,550workerCPU seconds,
90,750workerwall seconds,1,517,551,616output bytes,4,522entries and
123,391,407maximum host-read bytes. All fit the request's corresponding
envelopes. Independently rebuilt installation43-pin map totals88,865,789bytes;
derived request19-pin map totals42,051,359bytes. No retained checkpoints or
prior same-allowance charges exist. These are caps/accounting, not empirical
proof price, memory sufficiency or authorization to run the502-stage path.

Owner report29,079bytes/SHA-256
`34abb4af6979db0fe84f7edb1c3eb0ddffa60d412c3bf63239ef7beecbcba3c4`
records one `_request`, zero run/host/proof calls, owner closed/nonbusy, final
binding validated, and no errors. Captured stdout equals it after the sole
Windows LF-to-CRLF translation; stderr is empty. No production directory or
finalization sentinel exists. Outer result2,537bytes/SHA-256
`5fda4c06f9f4e9fec2b8c96ceb16f5fd585ab0b560605d4b7698cac816e84dba`
binds exact planec1f61b7 and selected argv/limits, exit0/reaped/closed, zero
active/terminated processes and no cleanup error or termination request.
Inclusive JobCPU1.125 plus disjoint wrapper0.4375 gives1.5625knownCPU seconds;
outer wall1.7041693s. Inner observations are not added again. Peak Job commit
26,554,368bytes is preflight memory only. No certification or growth claim follows.

## Native manifest-control source review

Complete fresh `manifest_controls.py` source17,605bytes/SHA-256
`ab897b28fbbdc930e9f775ac8461e07aaf5b6d284da4c329930f6997df5589eb`
and `SMALL-MANIFEST-CONTROLS.md` read independently. **No blocking source
finding for the selected ten-control contract.** Traced exact built native
source975e68df: every argv has `finish 0`; `get_prover_server` and all proving
calls are in the opposite branch. Unexpected manifest acceptance therefore
cannot invoke a prover through these commands. This is source/build-based
assurance, not dynamic instrumentation or a certificate for the binary.

M1–M10 mutate separate boundaries and recompute manifest extents/hashes except
the deliberate outer-hash mismatch. M8's257row fixture has the frozen
s167-dependent count refusal; M9's258rows reaches the parser bound; M10's exact
manifest reaches deterministic magic/version refusal on the shared72zero bytes.
All case oracles agree with native validation order. Correct parser behavior
does not admit a cryptographic artifact. Per-case ordinary failures require
closed/reaped Jobs, known accounting, selected diagnostics, empty stdout and
no artifact/crypto progress. First failure stops; source/config/inputs/generated
fixtures are rebound, aggregate allowances/census include finalization reserves.
The root's enclosing operation must still contain startup/pre-output failures
and finalization. Exact configuration/plan remain to be reviewed; no execution,
project import or proof was performed for this source review.

## Finite production launcher source review

Guard rerun passes. Read complete fresh `tools/Run-V5-Production.py`, SHA-256
`660a93e72e424e3ce355321961e43f8fad6fe0fa494e23c6cf8d76d167023dc9`,
against frozen `Run-V5-Check.py` and the pinned supervisor's limit, process,
cleanup and report paths. **No blocking changed-boundary source finding.**

New schema is explicitly production-only. Exactly16 argv require isolated
Python flags, the literal escaped snapshot operator path, `run` and five ordered
document/report flags. Replacement retains ordinary list argv; the unchanged
supervisor calls `Popen` without a shell, creates its child suspended, assigns
the Job and resumes it, and retains kill/reap/closure failure evidence. Runtime,
selection and snapshot rebinding remain; final binding failure overrides outer
success. Owner reports alone are never sufficient after an outer failure.

All six limits remain explicit integers under unchanged supervisor ceilings:
200,000CPU seconds,86,400wall seconds,8,192MiB/eight processes and8MiB each log.
Thus this is finite, not an unbounded bypass of the smaller test launcher. It
can enclose a separately selected first stage/prefix; it does not make the
284,550CPU502-stage quote fit a single maximum outer call. The exact forthcoming
prefix plan must select actual smaller bounds and remain below them. No runtime
or proof is selected by this source review.

Inherited launcher boundaries stay explicit: startup/pre-output refusal may
terminate without a durable outer RESULT; post-run rebind failure gets a failed
outer record; report-write failure exits unsuccessfully. The enclosing human/
root must retain stderr and failure rather than infer success from an inner
artifact. The cooperative owner filesystem and exact adopted sources remain
assumptions; no new hostile-source or concurrent-hostile-filesystem sandbox is
claimed. No frozen launcher/supervisor/source was modified for this review.

### Pre-use continuation correction

Root identified a real integration obstacle before any use: per-attempt source
snapshot execution changes the path-containing producer profile ID, preventing
same-profile checkpoint continuation. The preceding launcher source review was
limited to new dispatch/containment boundaries and did not establish that
integration property. Retain its review as history, not final source clearance.

The still-unused successor runs from one ordinary, immutable, runtime-pinned
installation and uses fresh snapshots only as evidence. All five actually loaded
operator/producer/package files must match the selected source bytes and runtime
pins; the original profile remains stable across finite attempts. This preserves
existing strict allowance lineage rather than weakening profile identity.
Reviewer supports that design. A further narrow pre-use finding in798e33ac:
literal placeholder tokens in a valid installed pathname could be expanded
after validation. Require the expanded operator path to remain the checked path
(or disallow the tokens there). Exact final successor review remains pending.

### Manifest selector source review

Read complete `Select-ManifestControls01.ps1`,10,236bytes/SHA-256
`ac711c719045b547724551df9c6dcd10533808af8e574eac3f6ce1b0ddbce13d`.
No blocker to generating one exact selection/configuration. Four sources are
explicitly pinned;25inner runtime pins include the three future source paths
only in child configuration, not the outer existing-file runtime map. Actual
s167/m1 host/image/new H/capsule/parent and layout evidence remain pinned. Inner
case/total limits and outer210CPU/300wall/1536MiB/three-process envelope align
with the reviewed finite controls. This selector launches no host or proof.

### Final launcher delta and exact manifest selection

Final still-unused production launcher7,269bytes/SHA-256
`676bb859d8379851092241e86855c0369e13d3d16364ea6f9bead2c530e4afa9`
requires expanded argv[4] to equal the exact ordinary operator path already
checked. The placeholder-origin finding is closed. Stable installation source
binding covers all five files and post-run runtime rebinding. **Source-only
clearance;** any proof/prefix still needs its separate exact plan and capacity
selection. No existing successful prefix or producer profile was rewritten.

Exact manifest-control selection12,233bytes/SHA-256
`846e5c8d3dee0655cc8e3d87c0d9cf3c255cccd472bf5a6c0e7f4d9620201a71`
and configuration15,515bytes/SHA-256
`33e3d21ac2a79c9686141d194e893042ecc789fdbd551a38da4a69ed4a20087d`
match the reviewed selector. Independently checked all four actual sources
(51,615bytes) and43outer runtime pins (121,791,943bytes), all25inner pins
including three future source paths against source-map lengths/hashes, and
all nine input pins against actual extents and outer hashes. No mismatch; run
root absent. Exact argv dispatches only the reviewed control entry; explicit
case/total/outer limits match the preceding review. **Clear for root to select
this one ten-case finish-only gate**, not a proof or any automatic retry.

### Actual ten native manifest controls

**PASS for the ten selected changed native input boundaries.** Read saved
outcome/command/log/fixture evidence without rerun. All eight original/snapshot
source bindings,43outer runtime pins and25actual inner runtime pins match.
All ten manifest sizes/hashes match saved pins; actual commands have17 argv,
explicit `finish 0`, selected manifest operands and distinct absent artifacts.
The shared invalid checkpoint is exactly72zero bytes. M8/M9 have257/258rows;
M2 has two schema keys; normal ordered finish manifest has168rows.

All cases exit1 with ordinary `COMMAND_FAILED`, clean reaped/closed Jobs,
zero active/terminated processes, no cleanup error or termination request and
empty stdout. Actual stderr gives the prospectively required diagnostic for
each case: outer hash, duplicate schema, positional object type, bool/u64,
session/capsule/stage binding, ordered keys, file hash, exact count, row bound,
and checkpoint magic/version respectively. No crypto/written progress or output
artifact appears. In particular M8 does not use the parser-bound oracle and M10
reaches the intended positive-parser/invalid-checkpoint boundary.

Inner report31,977bytes/SHA-256
`f2fdab6bcb77448994bb7f2f60fbe7490c232b3a891a75f6d7128520ad23ab61`
matches captured stdout after Windows newline translation. Saved configuration
matches33e3d21a. Outer result2,140bytes/SHA-256
`592ae832e2d04415203c44db4470522ae65a30434d469977398e14b938401873`
matches exact plan846e5c8d/argv/limits and clean exit0/reaped/closed. No sentinel
exists. Final inner evidence is63entries/628,187bytes; its pre-result census is
62entries/596,210bytes. Both are within the selected16MiB/128entry envelope.

Inclusive outer JobCPU6.1875 plus disjoint wrapper0.484375 gives6.671875knownCPU
seconds; outer wall12.1013172s. Nested ten-hostCPU2.265625 and inner controller
3.75 are already included, not added again. Peak Job commit102,023,168bytes is
verification/refusal memory, not proof-memory sufficiency. Zero prover/guest
calls follows the exact finish-only source/build control flow and observed
early refusals, not dynamic instrumentation. No A receipt, full segment proof,
net growth or full v5 qualification follows from this passing gate.

## Generic mixed-evidence seal-preparation review

Read full selected `MIXED-SEAL-PREPARATION.md`d41af28e and actual existing
mixed parser, delta parser/closure helpers, exact-J derivation, aggregate encoder,
membership bindings and Rust Graph/check_reader. No substantive model gap found.
Backward selection preserves every retained exact premise and topological order;
certified frontiers are leaves only conditionally on separate genuine receipt
and member verification. Parsing the full packet before selection prevents
salvaging structurally malformed omitted material. Native relation confirmation
of every selected witness and expected H remains indispensable.

Complete helper `aggregate_claims/prepare_mixed.py`,7,502bytes/SHA-256
`2d03b635553eaffa406fba57011bf3bd346ec23fd59e0092b29d9442a95802ff`,
has no blocking source finding. It calls the existing bounded parser once,
requires an exact native target, traverses its full closure, preserves original
relative frontier/delta/claim order and remaps selected claims without copying
one A receipt per frontier. Parser-returned canonical witness bytes are passed
unchanged to the existing encoder. Members are full-J byte sorted; retained A
parent heights determine height+1 with explicit u64 overflow refusal. Exact
header/membership functions validate the generated opening. Frozen slotted
records contain only immutable records, tuples, bytes and scalar fields, and
explicitly state untrusted preparation/no admission. No I/O or verifier is added.

Complete root test file `aggregate_claims/test_prepare_mixed.py`,11,315bytes/
SHA-256`f9b3a92ef14ec24c9c4d7c7d06598e405d8cf0ca017ee777efd65594ef68f33c`,
has eight source-reviewed pure controls. Synthetic fixtures cover direct existing
encoding, earlier-branch pruning/nonzero claim remap, omitted versus retained
maximum parent height, shared A receipt plus I ordering, exact-target refusal,
malformed omitted descendants, resource and total-wire one-byte boundaries,
and frozen/untrusted output. The wire-limit patch affects the actual encoder's
module global, not a substitute encoder. A separate saved-real-byte comparison
uses exact113,849byte FIRST wire/H/parent receipt; framing offsets and original
113,220byte witness SHA match the previously audited layout. No new native
checking or cryptographic verification is performed by these tests.

Parser negatives are sampled/reused, not exhaustive. Source review does not
claim the forthcoming eight tests exercise every profile/grammar/duplicate/
unused-material refusal. The helper derives structural candidate plans, never
proof acceptance or net benefit. Exact finite control plan remains pending;
reviewer performed no project import or execution.

### Exact mixed-preparation control selection

Read complete selector `Select-MixedSealControls01.ps1`,3,530bytes/SHA-256
`d311fc6710af5833c5f4338f72d718d1d3841e7e99d57ab903b9436a6b86d3b4`.
It prepares only an exact selection, reusing retained Python/runtime identity
and pinning the three actual byte-comparison inputs, without executing Python.
Exact generated plan8,787bytes/SHA-256
`1e730111ecab39dd2001599c41a695f99f049de8efa376edd1f443549242cf6d`
has21source pins (159,880bytes) and21runtime pins (17,492,995bytes), all checked
with no mismatch. Package import closure is included. Run directory is absent.
Exact argv uses isolated/no-site/no-bytecode flags and the snapshotted test
entry under30CPU/90wall/512MiB/two-process limits. **Clear for root to select
one eight-test pure preparation gate**, with no native/proof call or automatic
retry. Actual disposition remains separate.

### Actual mixed-preparation control outcome

**PASS for eight pure preparation controls.** All eight named tests finish OK,
zero failures/errors, no skipped test shown. All42 original/snapshot source
bindings,21runtime pins and20reported loaded-source origins match the exact
selection and saved files. The actual retained FIRST wire/H/witness/receipt
comparison passes without invoking a native checker or cryptographic verifier.
Synthetic openings/receipt bytes remain synthetic. No production certificate,
network operation or economic advantage is established.

Outer result1,909bytes/SHA-256
`21807bcbc2bfe09192fe4f313c2a0657c93c514104a0eff3d781ad0d49cb2257`;
stdout6,291bytes/SHA-256
`1565ceb77b5798681bee5252f9855b1502df6fbe7281712d95020cf8733b970c`;
stderr test log1,219bytes/SHA-256
`0b420c4b7a678b1a354e30a98f446fcc641a1550e6cebe673563269ad991e5e1`.
Exact plan1e730111/argv/limits, exit0/reaped/closed, zero active/terminated
processes, no cleanup error/termination request or sentinel. Inclusive JobCPU
0.734375 plus disjoint wrapper0.3125 gives1.046875knownCPU seconds; outer wall
1.2815069s; peak Job commit29,827,072bytes. Reviewer did not rerun the gate.

## Selective-certification model challenge

Read complete SELECTIVE-CERTIFICATION-POLICY after the actual controls. The
finite fully-cold-chain advantage inequality, batch minimizer and simple
arrival-plus-latency sufficient bound are algebraically sound under their stated
conditions. No counterexample to those conditional statements was found.
Two narrow refinements are necessary before treating them as a general-DAG
deployment advisor; they require no new experimental campaign or demand ledger.

### Exact certified cuts, not arbitrary single-target promotion

Let the dependency graph use exact J keys and edges child-to-premise. Promoting
a verified member J replaces that representation's serialized native parents
by a certified leaf; it does not remove other paths to old native nodes. In
particular, if T depends on certified X and old native Y outside the promoted
set, T's Y ancestry remains. Therefore one certified target alone does not
justify a bounded native tail for an arbitrary branching graph.

For a promoted set S of available exact members, remove outgoing parent edges
of S and compute the remaining target closure. Every eliminated old ancestor
must be separated from the target by S: every path to it encounters a promoted
member first. This graph-cut condition is sufficient directly by reachability,
and absent it the uncovered path is a counterexample. Count/price the actual
remaining native nodes and needed semantics, not nominal block length. All
demanded cut members require actual receipt/member openings and semantic custody.
The existing helper returns the full member-J list and existing B.opening can
derive their openings; no new certificate format or global coordination is needed.

### Independent cost bounds and explicit finite horizon

The shared d bound is mathematically legitimate but stronger than an owner is
likely to justify. Let d_L>0 lower-bound ordinary missing-node cost and d_S>=0
upper-bound sealed-tail node cost under the fixed matched workload, with q
fully otherwise-cold admissions per target. Then the same summation proves:

`D >= q*d_L*mb*(mb+1)/2 - q*d_S*m*b*(b+1)/2 - q*c*mb - m*K(b,H)`.

The original theorem is the special case d_L=d_S. H is the stated service
horizon; certification/failed attempts/retention/repair costs must be bounded
over H. Feasible m,b must satisfy actual count/byte/semantic/latency and funding
constraints. An interval-based advisor can use conservative lower/upper inputs;
unknown bounds give no guaranteed economic recommendation. Historical estimates
may instead guide a separately labelled heuristic. This is an implementable
local comparison, not a claim that current demand or proof cost meets it.

Root's subsequent precision correction is adopted in the policy appendix:
preexisting certified leaves outside newly promoted S are not native work.
The exact selected native set is Reach(G_S,t) intersect (V_native minus S),
where V_native denotes the pre-promotion native-evidence vertices. This leaves
the old-ancestor cut condition unchanged and avoids charging certified I/A
leaves as native nodes. The policy appendix was edited only under root's fresh
assignment; all used sources/tests/evidence remain unchanged.

## Independent allocation-refinement review

Source-only review of SMALL-LAYOUT-FEASIBILITY appendix, SHA-256
`c9073b6571a594ced151312ea35ca634cab1edd88570196e1396707aa3d39989`,
and fresh `software/v5/prover_memory/preflight.patch`, 1,093 bytes/SHA-256
`a53940b67580e215c55c2eae1e33e12f93a410193dde5f6414f533e4517fdc6c`.
The retained SDK, libraries, inputs and executable remain unchanged; no import,
build, native/proof operation, capacity poll or Git mutation was performed.

**PASS for the local source refinement; not a runtime fit qualification.**
The retained witness census establishes a maximum 612 bytes per reserved row.
`Trace::new` inserts Globals through the same `add_block` path as other blocks.
Each fresh row reserves at most 153 u32 words; its row-buffer index is accessed
before its witness write. Thus any successful old trace reserves at most N rows
and accesses only its first 153N words. `get_block[_mut]` uses recorded witness
indices/sizes, not vector capacity. `finalize` fills and sorts row metadata;
it adds no auxiliary reservation. Both versions zero the same reachable prefix
and make identical writes, offsets, metadata and final length. The patch checks
byte divisibility and multiplication before allocation; `is_multiple_of` is
already used by the retained trace source and introduces no new API dependency.

The synchronous Rust/C++ boundary passes auxiliary pointer and length, not
capacity; the Rust owner lives through the call and C++ copies that length.
Changing the allocation address is harmless, while alignment, lifetime, length
and contents must remain invariant. The selected po18 source change therefore
does not require a new guest, circuit, statement, capsule or receipt format.
It does require fresh host/library/profile identities. Proof-byte identity is
not claimed. The exact requested-vector reduction is 481,296,384 bytes, or
459 MiB; it is not a guaranteed reduction in OS working set or commit peak.

The revised persistent lower bounds, 2,790.8466796875 MiB before correction
and 2,331.8466796875 MiB after correction, do not establish po18 impossibility
or 4 GiB sufficiency. Exact circuit maxima, verification/transcript scratch,
decoded capsule, allocator and thread peaks remain relevant. The independently
established po19 C++-only lower bound still exceeds 4 GiB. Physical headroom is
not commit headroom and neither should be conflated with a proved upper bound.

The retained dependency records support the conservative frontier of circuit
rlib, zkVM rlib, module-relation rlib, aggregate-relation rlib and one final
stage-host compile/link. This is not a promise that arbitrary Cargo invocation
does exactly five commands. A fresh recipe must pin generated sources, compiler
environment/features, native archives and explicit compatible crate identities.
The author is deriving that exact recipe separately; no recipe or build launch
is cleared by this source-refinement pass. Root owns selection and adoption.

## Generic lifecycle independent source review

**PASS for source, not execution or proof qualification.** Reviewed the complete
GENERIC-SEAL-LIFECYCLE contract, fresh producer/snapshot/API, their actual inherited
constructor/build/image/request/lineage machinery and the native snapshot branch.
Exact reviewed producer: 8,724 bytes/SHA-256
`a249bc3505a28aadff20d81e4ce30b43e03fbf5d9d6de45277c81a4c340833f4`;
snapshot: 22,628 bytes/SHA-256
`8c65e623419f846c2b7607716ce7fdec8a611ae2bb340e9a9cab18af3c741546`;
initializer: 152 bytes/SHA-256
`a159ba3ed681f7b8da374af2ce8698be68a67a5d7e4a92a3190c2a228a2f7833`;
API: 8,165 bytes/SHA-256
`5559ec52f09d38d9a19ab26c06fad900e805d656c56c29464dbfeeabaeb0bbc0`.

The constructor preserves the immutable inherited base profile and introduces a
domain-separated lifecycle identity only after actual source/image/build adoption.
Its complete imported module closure, including initializer imports, is checked
against loaded origins. Existing allowance adoption requires the new profile ID;
old lineages cannot silently acquire a different helper or host. The lifecycle
reuses the actual old snapshot-build grammar, not fictional zero-rebuild records
for the resource-refined stage host.

Snapshot rederives the complete preparation from selected original packet/exact J/
envelope, compares the immutable value and uses the derived value thereafter.
Generated wire/header and indexed receipts preserve the exact ordered I/A claims;
they are bound as generated staging inputs, not invented prior outer runtime pins.
The native argv, actual stdout, saved invocation, exact capsule path and digests,
completed session and new-schema report are bound again during adoption. Native
verification and exact halted-A execution remain unchanged; no saved JSON becomes
a mathematical warrant. Finalization sentinels and unknown closure refuse adoption.

One concrete review correction was applied before this pass: measured worker CPU
must not exceed the selected cap before execute reports PASS, rather than being
refused only by later adoption. Source checks now agree at both boundaries.
The 14 MiB reserve plus original/derived inputs conservatively covers the inherited
20 MiB fixed-input bound; oversize valid mathematics may refuse operationally.
Output census is explicitly sampled, not a filesystem quota; the enclosing owner
must bound construction, import, refusal and finalization. Failed attempts retain
costs/files, and new proof funding remains an explicit separate decision.

Only focused source controls remain to review: exact synthetic lifecycle adoption,
forged preparation/target/ordered premises, changed binding/profile, partial or
overridden completion, cap/closure refusal and I/A renewal plumbing. Synthetic
records cannot establish cryptographic completion. Root relayed the user's pause
after current tasks; finish this at-hand source checkpoint only, no runtime.

## Exact allocation build recipe: independent static review

SOURCE.json, 100,153 bytes/SHA-256
`c93a45a6a558718c931c39b121e9bcffa7d464ecaa1d5b0e80185efd6cace710`,
is supported as a fresh explicit recipe, not a claim to replay unavailable
per-crate Cargo argv. Independently checked all 132 original record/source length
and hash pins: 113 SDK source files plus 19 retained records. All 72 direct SDK
extern references match the retained 1,071-entry runtime manifest; their names and
features match retained fingerprints. All 85 externs across the five steps resolve
to retained pinned inputs or a declared preceding fresh artifact. New metadata and
explicit dependency paths propagate through both relation rlibs to the host.

A strict in-memory application of the two patch hunks, without writing the SDK,
reconstructs 6,003 bytes with SHA-256
`88fbf84e1e4b5247d6df5d4206d9335442362dd5a3772d5c4930bd9197b67396`,
exactly the descriptor's derived source. The active external source inclusion is
the pinned generated preflight file through OUT_DIR; VERSION uses explicitly set
CARGO_PKG_VERSION. Other include sites are within inventoried source or disabled
test/guest paths. Retained generated code and native archives are reused, not rebuilt.

No remaining source objection to the five-step dependency recipe was found. This
does not establish compiler success, runtime memory fit or acceptance of a proof.
A concrete finite build runner must still pin expanded paths, actual environment,
source/runtime closure, produced dependency hashes and clean command completion.
A new producer-adoption grammar is required; the old one-link/zero-backend-build
grammar must not be impersonated. No compiler/proof campaign is selected by review.

## Focused lifecycle controls: source only

**PASS for the source of ten controls; NOT RUN.** Complete reviewed file:
`software/v5/aggregate_lifecycle/test_lifecycle.py`, 21,877 bytes/SHA-256
`c4d28107924ea5189a59857fd6c4df04738c3abcadc117934d1bc6c15b575bf1`.
The real new lifecycle constructor, preparation, configuration, staging, adoption
and inherited request path are exercised in the proposed tests. Retained loader/
build adoption and native execution are explicitly synthetic; Popen is globally
denied during tests. No predecessor suite is imported or repeated. Output is fresh
and all synthetic artifacts are labelled as nonproofs.

The ten controls cover immutable composite profile and closed-before-read entry;
two-I then A-premise snapshot/request plumbing with distinct sessions and stable
profile; forged wire or reversed prepared premises; absent target or changed input
pin; decoded-manifest premise reordering; geometry/output caps; missing capsule;
clean measured-CPU overshoot; finalization override; and changed-profile allowance
lineage. The decoded-manifest injection preserves actual saved evidence. The
positive asserts A seal-height advancement and no production directory/host call
from preflight. It is not a native, cryptographic or economic result. Unknown
closure is source-reviewed but not separately sampled by these ten controls.
No test execution is selected by this review or by the pause-after-current-tasks
request; root owns any later fresh finite selection.

## Focused lifecycle controls: selected actual outcome

Root subsequently selected the already-planned cheap ten-control operation before
the user-requested pause; no compiler/proof campaign followed. Exact plan 8,821
bytes/SHA-256 `7beca8c61c0ef66abd82eeae092f5d054d5ee9a89b657a2a409b8ea14f1a21b7`
and selector `ec4413f95488162300cd2e0faca9d8dc5261cda4bf4093d1b19e4266c8c1b540`
received independent prelaunch clearance. The seven argv entries select isolated
Python with -I/-S/-B, the snapshotted test and fresh controls output, under
30 CPU seconds / 90 wall seconds / 512 MiB / two processes. No native branch.

**Actual PASS in the scoped synthetic owner-control lane.** Independently rebound
all 52 original/snapshot source identities, 18 runtime hashes and 25 loaded source
origins. Saved selection matches the exact prelaunch plan. Actual log reports ten
tests, no failures/errors/skips. Seven inert supervisor dispatches comprise five
synthetic completions, one missing capsule and one CPU overshoot. Their use is
explicitly synthetic; Popen denial and reviewed control flow support no native or
proof execution, not a cryptographic-completion claim. The finalization test's
intentional inner sentinel remains preserved; there is no enclosing sentinel.

Outer process exited zero, direct child reaped, Job closed, zero active/terminated
processes, no cleanup errors or termination request. Inclusive worker CPU 4.921875
plus disjoint wrapper CPU 0.28125 gives **5.203125 known CPU seconds**; wall
7.323706399882212 seconds; peak Job private commit 60,547,072 bytes. No rerun.
All used lifecycle/test/selector inputs and actual outputs remain frozen.

Actual run: `experiments/v5-local-checks/generic-seal-lifecycle-controls-01`.
Outer RESULT: 2,058 bytes/SHA-256
`13517183d1abb18b182b806006432dffeafa6cbdb3b48d7ec19c55ff9197f418`.
Inner RESULT: 18,652 bytes/SHA-256
`412b832c7d8a9b618439c7612fa45ff3df8896eb77a058190e37cea492573c69`.
Stdout: 18,653 bytes/SHA-256
`670d0d8c2a5a46384b49bd73b3073805129afe4fc7a45ca55b558af92e8f18a3`;
it equals the inner result after Windows newline normalization only. Stderr:
1,534 bytes/SHA-256
`dc22565852decff14c78a27162c9ffd9c4a8e5af9104bfe2394e27d26899a4e7`.
This qualifies changed owner plumbing, not genuine I/A proofs, useful-growth
advantage, a real renewal or deployable v5.

## Allocation-refined builder and owner: final at-hand source review

**PASS for source correspondence; NOT BUILT OR EXECUTED.** The completed fresh
source-only artifacts reviewed before the requested pause are:

| Artifact under `software/v5/prover_memory` | Bytes | SHA-256 |
|---|---:|---|
| `build.py` | 25,126 | `8ca39b2dc68fdab7ebe96eef2bf53ce212c3a5196acb626f7bc7b99263c91781` |
| `adoption.py` | 15,611 | `56b633aa0a528cb383f47cf5b1e73bd9a8b18387382c23d4c8114348b2cc6459` |
| `producer.py` | 2,714 | `7eed73c709499902bbbc4beff612234cdce1ac8171918f195f4dde9704105e1a` |
| `__init__.py` | 81 | `f442b572d094a1efb5eaa31bee2a54dbd384cd1bbabdc9b513fceed7ea4a03e2` |
| `BUILD-RECIPE.md` | 14,784 | `4973a42b582c635a32810e121005ccbae149b188594da446c904e82ad957ab1d` |

The builder implements the reviewed descriptor, not Cargo discovery: strict exact
two-hunk transformation in memory, fresh copied SDK/integration/stage/adapter and
generated source, explicit five compiler argv and newly produced dependency pins.
The immutable original SDK and previous artifacts are never edited. Full retained
1,071-entry runtime rebinding occurs before/after; smaller source/helper/new-output
rebinding occurs before each phase. The complete output source census is checked
against the derived map. It runs neither a build script nor the produced host,
guest or prover. All execution remains contingent on root's future finite selection.

Read the retained environment constructor, phase invocation and close routines to
check actual control flow. There are five separate serial worker Jobs, each capped
at 240 CPU seconds / 300 wall seconds / 3,072 MiB / six processes; the aggregate
CPU bound is 1,200 seconds. No concurrent large Job is introduced. Closing-phase
accounting is retained even on refusal; failures stop the chain and remain charged.
Source/runtime/final-record checks and a finalization override prevent an apparent
PASS from hiding failed final checks. This is local trusted build tooling, not a
hostile-source sandbox or hard output-disk quota; final report/exit tails are stated.

The adopter recognizes the new honest five-command schema and exact rebuild counts,
not the old zero-rebuild grammar. It independently derives the copied file map from
the pinned descriptor and retained maps, including the single SDK allocation delta,
generated preflight, integration/stage sources and evidence. The one zero-byte
build-script output is separately checked as nonexecutable evidence and rebound on
later owner checks. Base and per-step environment maps match the retained constructor
after exact run-root relocation and declared overlays. Five closed Job records and
their sums/max peak agree with per-command/whole-operation limits; fresh dependency
edges and executable identity are explicit. Full compiler/runtime tree rehashing
belongs to the build operation, not every subsequent proof-owner construction.

The narrow owner mixin changes stage-host adoption only. Both the retained-layout
owner and generic-lifecycle owner preserve their actual snapshot rules and image/
statement policy. All 27 imported source paths are required in the immutable support
runtime map, binding the new implementation into the inherited profile identity;
no internal profile rewrite or old-allowance migration occurs. Ordinary cryptographic
verification is unchanged and remains necessary. No compiler success, measured
memory fit, produced A receipt, full-cost growth advantage or v5 release follows.

All assigned at-hand independent work is now complete. Reviewer stops for the
user-requested pause. No build/proof campaign, retry or new workstream is selected.
The recipe's final documentation update was read after code review; it accurately
describes the implemented source-only builder/adopter and changes no reviewed code.
