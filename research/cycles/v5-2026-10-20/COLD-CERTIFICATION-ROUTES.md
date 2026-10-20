# Cold certification: actual routes and marginal-payoff decision

Source/saved-evidence review, 2026-10-20; owner `core_search`. No build,
guest execution, native checking, proof generation, benchmark, RAM inspection,
installation or campaign restart was performed for this review.

## Decision

**Do not commission another full proof or geometry experiment from the present
evidence.** The available small target is already closure-pruned; the measured
dominant cost is cryptographic proof production, not its controller or native
checking. No measured cheaper direct-I substitute is currently available.

The highest-payoff next implementation is instead the separately identified
receiver-side semantic-interface seam: eliminate mandatory acquisition of
irrelevant definition bodies when the existing final acceptance rule needs only
their certified interfaces. This is a separate central scalability improvement,
not a claim to have solved cold certification. Root should first establish that
its exact interface and final acceptance invariants survive; retain full native
checking and the existing receipt requirements. Do not build another planner,
memoization layer or proof-production wrapper.

Cold certification remains an open release obstacle. Revisit a production run
when a concrete changed guest/backend has a justified expected saving and a
finite complete-work budget, or a selected reusable contribution can amortize
the measured cost under the separate economics analysis. Lack of such a run
today is not evidence that the current PC can never produce the receipt.

## Actual relation and trust boundaries

`I` certifies one module journal `J`, checks the module relation, and discharges
each exact parent assumption through `env::verify`. Its frozen guest is
`software/v5/modules/receipt/src/main.rs`; the stage host is
`software/v5/modules/receipt/src/bin/module_host.rs`. Its image is:

`9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e`.

`A` certifies a 192-byte exact-DAG header `H`. The selected guest sources are
resolved by `software/v5/proof_memo_guest/recipes.py`, using:

- `software/v5/modules/native/proof_memo/lib.rs`;
- `software/v5/bounded_parse/module_lib.rs`;
- `software/v5/bounded_parse/aggregate_lib.rs`;
- `software/v5/aggregate/main.rs`.

The selected A image is:

`99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60`.

The bounded aggregate relation invokes module checking on already validated
syntax. It preserves kernel/foundation/correspondence checks, exact parent
bindings and checks on every new local declaration. The aggregate guest then
verifies every unique actual I/A assumption and commits the exact header.
Do not infer current behavior from the original logical-path relation alone.

An A member opening does not itself become an I receipt. I-to-A frontiers and
same-A openings are supported; A-to-I substitution is not obtained by changing
a label or copying a journal. A final accepted certificate must retain its
actual guest image, exact public journal and resolved assumptions.

Native acceptance, an execution capsule, a Merkle opening and a checkpoint
envelope are four distinct objects; none is independently a genuine receipt.

## Retained evidence, not forecasts

### Genuine I base receipt

The completed base capsule is
`experiments/v5-local-checks/module-base-snapshot-03/evidence/base.snapshot`:

- 110 po18 segments, zero assumptions;
- 21,274,865 bytes;
- SHA-256 `55eaa583ddfde8ebe827bfa941fcb81b95f9773fd2b2e295df2166501d973980`;
- binding `4608ca4e3c12d338a86813afa96dbf418a1076eca79b2a8ab2838bb78135d925`.

Its roughly 3.078125 known CPU seconds and 3.4458391 wall seconds measure
execution/snapshot preparation, **not** certification.

The genuine final receipt is
`experiments/v5-local-checks/module-base-production-01/finish-0/receipt.bin`:

- 223,594 bytes;
- SHA-256 `850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47`.

The retained `module-base-production-01/RESULT.json` records
`PASS_FINISHED_RECEIPT_ARTIFACT`, with application receipt creation, final binding
validation and known closure accounting. Later genuine contributor/admission
work verified this receipt; it is not merely a saved native success.

`software/v5/production/producer.py` implements the existing ordered graph:

\[
s\text{ segment} + s\text{ lift} + (s-1)\text{ join}
+ m\text{ resolve} + 1\text{ finish} = 3s+m\text{ host calls}.
\]

The base graph has 330 calls. The final attempt retained five earlier
successful checkpoints and performed the remaining 325 calls:

| Stage kind in final attempt | Calls | Worker CPU seconds | Sum of contained stage wall seconds |
|---|---:|---:|---:|
| Segment | 108 | 90,118.328125 | 8,966.991920 |
| Lift | 108 | 17,937.296875 | 1,540.212126 |
| Join | 108 | 18,046.015625 | 1,579.272186 |
| Finish | 1 | 3.984375 | 4.690200 |

These are aggregations of the 325 existing stage results, not new timings.
Total final-attempt worker CPU is **126,105.625 seconds**, controller CPU
688.375 seconds, and whole attempt wall 12,767.4275038 seconds. Segment proofs
account for approximately 71.46% of worker CPU; lift/join account for 28.53%.
Do not add the contained per-stage figures again to those totals.

The carried earlier calibration/prefix adds 1,852.453125 worker CPU seconds,
2.78125 controller CPU seconds and 176.1639226 summed active wall seconds.
Earlier research/build/failure costs are not included; they are not zero.

The saved first-segment result in `module-base-segment0-01` separately records
565.03125 Job CPU seconds, 0.78125 controller CPU seconds and 81.7326653 wall
seconds. Its recorded precryptographic ordinary work was 135 ms of 80,685 ms,
about 0.1673%. A persistent CLI is therefore not supported as a way to remove
the observed dominant production cost.

### Smallest currently selected A target

`experiments/v5-local-checks/selected-frontier-layout-01/evidence/` already
contains the target-preserving BASE+FIRST cut: BASE is a genuine I frontier,
FIRST is a new checked native witness, and SECOND has been removed. J_FIRST
is unchanged. `aggregate_claims/prepare_mixed.py` already performs exact-J
closure pruning, remapping and wire/header preparation. Do not propose this
same pruning as a new optimization.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `wire.bin` | 113,849 | `898660ddeea92cefccbf793e35b1ee49ef4867c9daec24b5344f37a1ed375500` |
| `header.bin` | 192 | `49dd845edaec83f5b0cba5af38653f768e51ed95a4bb6ea7824c10bdd1c3169e` |
| `aggregate.snapshot` | 32,965,324 | `6e41621e2595c252328eaf5f34862c6d6f913caecb68117406bcd616a61b44a5` |

The complete capsule has **167 po18 segments, one actual I assumption**,
43,778,048 padded rows and 4,205,234 padding rows. Its binding is
`e56cb33f432a4c5bbdb0624eb2a072db48562e26c77fc20cefd0da8831585a2b`;
session binding is
`9c87448ba08ae98273ac6fc1df8a41a22716db8be686ce473eb5fba874a1475d`.
The diagnostic SHA is
`a3e81713cc7438d2c1a385e94fb8679523774056b5452c9f99b35cbce6033e28`.

The result is `PASS_ONE_AGGREGATE_EXECUTION_CAPSULE_ONLY`, with **zero proof
calls**. Recorded outer Job CPU is 3.53125 seconds, wrapper CPU 0.296875 seconds,
wall 3.1815756 seconds; nested supervision CPU is contained rather than a new
disjoint charge. A complete new proof graph would require **502 host calls**.
There is no final genuine A receipt in this evidence.

The 502 versus 330 call comparison is not a 1.5212 times runtime prediction:
the programs, local witness checks, segment traces and assumption resolution
differ. It does rule out describing the selected A capsule as a trivially small
production target merely because snapshot execution took a few seconds.

### Preserved failed and unexecuted routes

- Full BASE+FIRST+SECOND po19 execution completed a 113-segment capsule with
  59,244,544 padded rows, but no receipt.
- The corresponding full po18 attempt stopped at 256 segments with
  `67112097 >= 67108864`. This is a nonterminal partial execution, not a
  completed capsule reusable as the full proof input.
- Earlier memo execution hit `33557665 >= 33554432`. Historical statements
  that no complete A capsule exists are superseded by selected-frontier167;
  absence of a genuine A receipt is not superseded.
- The geometry17 host is linked but unexecuted. Its previously recorded
  launch decision deferred before invocation, not after a failed layout.

Sources: `research/cycles/v5-2026-10-17/SMALL-LAYOUT-FEASIBILITY.md`,
`LOCAL-PROOF-NEXT.md`, and the saved diagnostics under
`frontier-capability-execution-01` and `small-aggregate-layout-02`.

## What smaller or equivalent relations can and cannot remove

For the same fixed J_FIRST, exact parents and checking policy, a sound
implementation improvement may remove duplicated parsing, repeated validation,
dead representation work or a redundant proof representation. It must still
establish the same extension and recursively discharge the same obligations.
It cannot omit a necessary declaration check or required assumption merely
because a native process earlier accepted it.

The A one-witness cut and a possible direct-I FIRST execution share the core
mathematical extension obligation. A has additional DAG/header bookkeeping,
but direct I's frozen guest is older and is not automatically as optimized as
the selected A guest. No completed direct-I FIRST capsule has been identified
in the reviewed evidence. Removing A bookkeeping alone has no established
large reduction; a new direct-I campaign is not presently justified as a
known inexpensive substitute. It would also not demonstrate same-A renewal.

Several concrete reductions are already available or explored:

- Typed-row decoding has native equivalence controls, but its changed guest
  has not been built/executed. No whole-guest row or certificate saving is
  established, so no numerical speedup is credited.
- The byte-to-word allocation correction is already built. Its known change
  removes 459 MiB of requested auxiliary payload per po18 segment; that is
  neither a peak-memory upper bound nor a new optimization proposal.
- Po17 execution does not reduce fixed-po18 recursive lift/join/resolve work.
  Existing capsules cannot be resegmented by a supported conversion. A fresh
  execution would be necessary and may add segments/nonpadding overhead.
- Runtime pin-phase deduplication and exact-J frontier preparation are already
  installed mechanisms, not outstanding design gaps.
- Same-live native memoization was correctly deferred: repeated calls in the
  actual recent contribution consumed only 0.0625 CPU seconds and 0.1692674
  wall seconds, below 0.15% of whole-workflow known CPU.

A specialized mathematical method, alternate checker or new proof backend
could change the cost substantially. Each introduces a real correspondence,
policy-adoption and integration obligation; none is an already established
quick substitute. Replacing J_FIRST with an easier theorem changes the target,
not its certification cost.

## Required distinction in the next project decision

We can improve large-network receiver scalability now without repeatedly
trying to manufacture a receipt whose full cost is not yet justified. We must
not call that improvement a resolution of production affordability. Conversely,
an expensive one-time production receipt could be worthwhile for enough
subsequent reuse; its acceptability depends on demand and cost accounting,
not the number of locally running peers. See the disjoint
`COLD-CERTIFICATION-ECONOMICS.md` and `COLD-CERTIFICATION-ASSURANCE.md`.

Root retains launch, adoption and Git ownership. This checkpoint selects no
new experiment and does not relax the final v5 goal.
