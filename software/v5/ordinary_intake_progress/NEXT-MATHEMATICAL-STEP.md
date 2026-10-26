# Next mathematical contribution: exact effects of finite-map update plans

2026-10-26. Source/data-only investigation by `intake_cost_localization`.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Checkpoint: `research/cycles/v5-2026-10-26-local-discovery/CHECKPOINT.md`.
No product import, Lean invocation, owner access, test, Git change or runtime
selection. The completed progress successor stays fixed.

## Decision and investigator's use

Select, in principle, **a complete nonemptiness analysis for finite write-only
map programs**. Its purpose is to decide when a downstream consumer can omit an
emptiness guard after a branching update pipeline. This investigator chooses
that use; it is not a previously observed user's demand, a network-wide agenda,
or a condition of mathematical acceptance.

The output should be a small reusable theory with program syntax, execution
semantics, a computable summary, and a theorem characterizing exactly when every
execution ends with a nonempty map. This adds a concept and a compositional law
above the acquired map library. It is not merely a renamed `isEmpty_insert`.
Effect analysis and weakest preconditions are established ideas; no claim of
historical mathematical novelty or measured discovery acceleration is warranted.

`ordinary_parse_reuse/USER-PAYOFF.md` already specifies the approved-project
contribution route, but deliberately leaves the investigator's mathematics
unselected. This note fills only that content/dependency gap. It does not repeat
the rich-intake, module, deployment or growth architecture.

## Formal object and law

Fix arbitrary types `K`, `V`, with `BEq K`, `Hashable K`, `EquivBEq K` and
`LawfulHashable K`. Keep these as explicit parameters; a concrete key-type
instance is unnecessary and could add unwarranted imports. Let `Map = Std.HashMap K V`.

A finite `Plan K V` has four constructors:

- `skip` leaves the map unchanged.
- `put k v` inserts the given key/value.
- `seq p q` runs `p`, then `q`.
- `choose p q` may run either branch.

Define an inductive relation `Exec p m m'` with exactly the following rules:

1. `Exec skip m m`.
2. `Exec (put k v) m (m.insert k v)`.
3. `Exec p m n` and `Exec q n m'` imply `Exec (seq p q) m m'`.
4. `Exec p m m'` implies `Exec (choose p q) m m'`.
5. `Exec q m m'` implies `Exec (choose p q) m m'`.

Define the Boolean summary `mustWrite` recursively:

\[
\begin{aligned}
W(\mathrm{skip})&=\mathrm{false},&
W(\mathrm{put}\ k\ v)&=\mathrm{true},\\
W(\mathrm{seq}\ p\ q)&=W(p)\lor W(q),&
W(\mathrm{choose}\ p\ q)&=W(p)\land W(q).
\end{aligned}
\]

The central theorem is, for every plan and initial map,

\[
\left(\forall m',\;\operatorname{Exec}(p,m,m')
        \Rightarrow m'.\mathrm{isEmpty}=\mathrm{false}\right)
\iff
\left(m.\mathrm{isEmpty}=\mathrm{false}\;\lor\;W(p)=\mathrm{true}\right).
\]

This is an exact weakest precondition for a nonempty result in this language.
It supports symbolic keys/values, overwrites, arbitrary finite composition and
branching. For example, a possibly-skipped write followed by a choice whose
**both** branches write has a nonempty result even from an empty input. A choice
between one write and `skip` does not establish that property for an empty input.
No map equality, lookup or cardinality law is smuggled into this conclusion.

The language intentionally excludes erase, clear, exceptional exit and loops.
Both branches of `choose` are always possible. When a real program has correlated
guards or unreachable branches, this abstraction may be conservative for that
program; its completeness theorem concerns the stated nondeterministic syntax,
not all feasible executions of arbitrary source code. Do not infer actual source
transformation correctness or runtime speedup from this theorem alone.

## Constructive proof in principle

Two induction lemmas suffice; neither requires map internals or classical choice.

**Preservation and forcing.** If `Exec p m m'` and either `m` is nonempty or
`W(p)=true`, then `m'` is nonempty. The `put` case is exactly the received
`Std.HashMap.isEmpty_insert`. `skip` preserves its input. For sequencing, an
already nonempty input stays nonempty through both parts; otherwise a forced
write in the first part establishes the invariant for the second, or the second
part forces it itself. For choice, `W(p) && W(q)=true` makes either selected
branch write. All Boolean side cases can be discharged by constructor cases.

**Zero-effect witness.** If `W(p)=false`, there is an execution `Exec p m m`
for every `m`. This is proved structurally: skip witnesses itself; put's premise
is impossible; a false sequence summary makes both components false; a false
choice summary provides at least one false branch. Compose the witnesses. This
also makes the converse nonvacuous: a plan without a guaranteed write can retain
the exact initial map, so all results can be nonempty only if that input is.

The central equivalence follows immediately from those two statements by cases
on `W(p)`. Every finite plan also has an execution by the same structural rules;
there is no hidden termination or fairness premise. The proof is valid at the
mathematical level. Actual Lean elaboration, generated dependencies, whole-unit
counts and independent checking remain unexecuted obligations.

## Exact existing mathematical inputs

The inspected restored bundle is
`experiments/v5-local-checks/std-reconstruct01/materialized`, with manifest SHA-256
`1de776b3d131c8c1be3414ed0e0cf066ebd05caebbcd1cf1b6ca80853962e59c` and semantic ID
`9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7`.
Its restoration is adopted; it is not an accepted rich parent.

The target unit is
`units/ab6f1b22d8760ba5615e9ec7e5a1fda99313c71a8cab34183c2fe88aad31381c.json`,
12,692 bytes, raw SHA-256
`6e936b8dc09218bb2fce8d8c6c8ef2dd8d77716462840d192c7b756c403a161a`.
Its sole output is `Std.HashMap.isEmpty_insert`, exported as
`bf281176862c75a7c8be1d00359f85bdcfe4904f4aefd5977c954e822e79070c`
in the retained reconstruction/summary data. Its actual import table contains:

| Required map interface | Export ID in target data |
|---|---|
| `Std.HashMap` | `baa1877cd14b1dc673e5273d7289fac7217bd71ac12087079c32df5503f8d452` |
| `Std.HashMap.insert` | `502e873d45854cf18f1251d1504fa3e6871c044c5e937dbb3db1741194112f9e` |
| `Std.HashMap.isEmpty` | `5bf44971b7f56e16de51a447c02eee4d7cfc620c9cd6572e6682671135aadcb2` |
| `EquivBEq` | `5f2751cd90a4d320aad9020db33f8dcb8fcdcbf53cdf8d7290ec9a86f6dc5676` |
| `LawfulHashable` | `ad9ef3b8aba1e3a435987aa4f025216ed4a3721f5f7bbbb8917c3a065be538a2` |

The same import table binds `BEq`, `Hashable`, `Eq`, `Bool`, and the lower-level
`Std.DHashMap.isEmpty_insert` on which the target depends. The fixed inventory
at `std-export01/bundle/inventory.json` (SHA-256
`c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0`)
contains `Eq.rec/refl/symm/trans`, `Or.inl/inr/rec`, `Iff.intro/rec`,
`Exists.intro/rec`, `True.intro/rec`, `False.rec/elim`, and
`Bool.true/false/rec/casesOn/noConfusion/noConfusionType`. It also contains
`Bool.or/and/not`; the effect definition can use these actual basis operations.
`Prop` is a universe, not an additional imported constant. The new syntax and
evaluation inductives supply their own recursors; no `List` or lookup library is
needed. These names were checked in the exact saved basis inventory, not inferred
from a generic Init import. This was a small data read, not an owner query or
revalidation of every proof. Use constructor cases and explicit terms to minimize
incidental tactic-lemma dependencies; do not assume an arbitrary imported simp
database is warranted.

The explanatory installed source is
`software/runtime/lean-4.34.0-windows/src/lean/Std/Data/HashMap/Lemmas.lean`,
SHA-256 `8dbd6f38ff380dd01898075d255093ccf394897936405ae6f6f80c2de9d56281`.
Its `isEmpty_insert` at line 50 states exactly the put-case law under the stated
classes. Approved authoring can import `Std.Data.HashMap.Lemmas` from the same
runtime's `lib/lean` using the existing project-authoring selection.

These inputs deliberately need neither `get?`, `contains`, extensionality,
`emptyWithCapacity` nor a new Std export. The current target closure does not
license assuming any such neighboring method has a protected binding. The final
candidate's actual unresolved-name set still controls whether the planned
dependency restriction was achieved; source import convenience is not a warrant.

## Minimum implementation and acceptance path

After, and only after, root adopts an actual successful Std intake, select that
owner's actual final root and exact support/profile. Current protected recovery
established only the original basis; no rich root is available by this note.

The minimum new implementation is **one investigator-authored Lean source body**
containing `Plan`, `Exec`, `mustWrite`, the two induction lemmas and the central
equivalence, plus its ordinary output-name and approved-project JSON selections.
No product or protocol change is presently justified. Suggested fresh namespace:
`FiniteMapEffects`; check actual name availability when selecting the contribution.
Generated eliminators/helpers remain complete declaration groups, not split rows.

Use the existing `owner contribute` route with `acquired_targets=[]`, an explicitly
hashed `--project-authoring` document, and the selected actual parent. The authoring
document selects a fresh module name, approved project cwd, this runtime's
`lib/lean` search path, and `Std.Data.HashMap.Lemmas` as a non-meta import. Follow
the exact existing `TrustedProjectAuthoring` schema; the producer's distinct
project-extraction JSON schema is not interchangeable. `request_targets` then
requests the warranted fixed-basis `Eq`, avoiding the 265-group reconstruction
frontier. Safe imported names remain unresolved until the existing binder binds
them to the real protected context. New inert groups undergo actual admission.

Keep the existing 32-new-unit, 4-MiB evidence/candidate and 131,072-node limits.
The small mathematical specification makes fit plausible, not proven. Do not
raise limits or silently add missing parent names if elaboration exceeds them.
Inspect the actual candidate's dependency names before native selection when
available, and require the received map theorem's exact binding in the final
proof dependency path. A hand-coded map replacement or a proof that never uses
the acquired map fact would not demonstrate this intended reuse.

Success must retain the actual checked source/candidate, new output IDs, durable
evidence and checked resulting root under the public contribution's normal clean
closure requirements. Compile success alone is insufficient. Existing publication
can expose those outputs later; a second receiver, network rollout or new export
helper is not required to answer this next local capability question.

## Utility falsifiers and investment boundary

This candidate is worth doing only as a small supported capability step, not as
a reason to continue an expensive intake indefinitely. Its value is falsified or
materially weakened if:

- The requested authoring/admission route cannot express these two small
  inductive definitions and their laws without reconstructing the large frontier.
- The actual candidate imports substantial unexpected mathematics, or the
  selected parent cannot interpret its map operations under exact identities.
- The analysis cannot answer a meaningful client guard question, or a realistic
  desired pipeline needs erase, failure, guards or loops outside its stated model.
- The whole acquisition/contribution cost is unjustified for the expected reuse
  compared with an equally capable approved ordinary Lean library.

The ordinary Lean comparator already knows Std, can define the same abstraction,
and can cache/check it normally. The commons does not gain a speedup merely by
producing this theorem. Its distinct tested capability would be independently
grounding acquired map mathematics and returning a reusable checked extension
through existing interfaces. Demand, actual repeated use, complete costs and a
strong counterfactual are still needed for a growth-benefit claim.

If strict rich intake remains too expensive, favor the already approved local
library path and revisit the strict operating region. Do not select a second
large library or a new certificate mechanism to rescue this proposed example.
This note authorizes no execution and does not assert final-v5 completion.
