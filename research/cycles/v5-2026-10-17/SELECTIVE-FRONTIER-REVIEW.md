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
