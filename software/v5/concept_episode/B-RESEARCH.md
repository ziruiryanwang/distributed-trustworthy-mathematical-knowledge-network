# Investigator B: independent extension record

Current status: TheoryB02 is a source-only correction after root's first compile
of TheoryB failed. No compiler, runtime, admission, or exchange was run by B.
The selected mathematical inputs were exactly TheoryA.lean and
A-HANDOFF.md, plus the pinned Lean 4.34.0 Init sources and prior mathematical
knowledge. Root reported successful ordinary compilation of A at SHA-256
`d2391e4a1a69d1ce57274ed011cd16734457e8239d2831a8e6eddd3349cbd9d9`.
That report supersedes the source-only status written in A's original handoff;
it is not a commons-admission report.

Operational context read: canonical AGENTS.md, first 45 lines of GOAL.md,
first 25 lines of research/NOW.md, and the guard. Normal guard invocation met
PowerShell execution policy; the documented process-local Bypass invocation
passed. No persistent policy change was made. No A-RESEARCH, other mathematical
investigator notes, desired continuation, or exchange-route material was read.
The agent-status inventory exposed A's brief completion summary, containing no
mathematical detail beyond its public handoff. No Git operation was performed.

## Selection and reasoning

A makes the difference between preservation and canonical choice explicit.
I independently selected the question: which additional mathematical structure
makes the result canonical without forcing all constraints to have a unique
jointly fixed state? A partial information order and monotone extensive repairs
answer this. Such repairs are the familiar closure operators, since idempotence
already comes from Repair. The extra structure says an output is the least
acceptable extension of its input, rather than an arbitrary acceptable choice.

The main bridge is stronger than merely adding a monotonicity lemma:

`Follows r s` iff `r(s(x)) <= s(r(x))` for every x.

Thus A's directional preservation relation is a comparison between two run
orders. In this setting mutual preservation is exactly commutation. Fixed-state
inclusion also reverses pointwise closure order. For finite safe schedules the
result is the least jointly fixed upper bound of the initial state; schedules
with extensionally identical joint constraints yield the same output even when
their lists differ. These statements reuse A's preservation, settling and
idempotence interface rather than reproving its finite schedule theorem.

This is a connection to established closure-operator/order theory and a useful
reframing of A, not a claim of new mathematics or literature priority. No
literature search was performed. The independent choice and development of the
bridge are distinct evidence from any novelty claim.

## Challenged candidates and limits

1. Mutual preservation of arbitrary repairs implies commutation: already
   refuted by A's choose model. I did not pursue this false generalization.
2. One-way preservation of closure operators implies commutation: false. The
   module gives two Boolean-fact closures: install the left fact, then propagate
   it to the right. This order settles both, while reverse order leaves the
   right fact absent on the all-false input. Both are monotone and extensive.
3. Closure structure automatically makes every repair order safe: refuted by
   the same model. The reverse sequence violates preservation. Consequently
   `same_constraints_same_run` explicitly requires both schedules to be Safe.
4. The choice countermodel might become canonical by choosing a clever partial
   order: impossible for both choice repairs simultaneously. Their mutual
   preservation would force commutation, contradicting their outputs on none.
   The impossibility is proved in the module.
5. A unique global jointly fixed state would trivially settle output equality,
   but would discard the dependence on the initial state. The selected least
   upper-bound result avoids that excessive hypothesis.
6. Repeated incompatible closures on finite ordered state spaces could lead to
   a convergence/fairness theory. That is a separate extension requiring a
   termination argument and a schedule model; it is not claimed here.

At the first source-only checkpoint there were no compiler-driven failed proof
attempts. The rejected variants above are mathematical candidates, not failed
executions. The subsequent actual compiler failure is recorded below. A draft thought using
three-element chain closures was replaced before writing by the smaller
two-Boolean-fact model; the chain idea was not a theorem failure.

## Source design and checkpoint

TheoryB.lean imports TheoryA through the modern module/public header. OrderData
packages only reflexivity, transitivity and antisymmetry; IsClosure is an extra
predicate on A's Repair rather than a competing repair type. The small explicit
order interface avoids requiring a separate library beyond A and Init. Public
definitions are exposed for downstream reduction. The finite models use ordinary
Bool decision proofs, not evaluation commands, new axioms, unsafe code or plugins.

The allowed output/checkpoint paths are TheoryB.lean, B-RESEARCH.md and
B-HANDOFF.md in this directory. Root owns any later bounded compiler selection;
B has not launched one. The public handoff describes the interface without
depending on this private selection record.

Final source-only pass: 183 lines, SHA-256
`bf3b0947459feca323403ea4e1263133efd5ab6a53eb69f44d6ebf9dd0fea54e`.
This source is frozen for root's separately selected first bounded compiler check.
Any compiler-driven correction will require a new recorded revision.

## First compiler feedback and minimal revision

Root's selected first ordinary compilation loaded original A successfully but
failed exactly one elaboration at TheoryB line 69. I read the retained diagnostic
at `experiments/v5-local-checks/concept-theory-b-01/command/stdout.txt`:
`h x` had type `o.le (r.apply x) (s.apply x)`, while the inferred transport
expected `o.le (r.apply (s.apply x)) (s.apply x)`. This is a proof elaboration
failure, not acceptance or a disproved mathematical statement. The process
closed cleanly according to root's report; no other diagnostics were reported.

The equality `hx : s.apply x = x` must change only the right argument of the
relation. TheoryB02 replaces the single line `exact hx ▸ h x` with:

```lean
exact Eq.mp (congrArg (fun y => o.le (r.apply x) y) hx) (h x)
```

The explicit motive yields an equality from `o.le (r.apply x) (s.apply x)` to
`o.le (r.apply x) x`; Eq.mp applies that equality to the original comparison.
No new mathematics or refactoring is included. Namespace and all declarations
are unchanged, and original TheoryB.lean remains at its recorded hash.

Fresh allowed source/checkpoint: TheoryB02.lean, 183 lines, SHA-256
`d1397331c7b633fec21558189c2eaa45b76642c49d5ca3f359a01f6e623c5bb4`.
It is frozen for root's separately selected next ordinary source check. B has
not compiled this revision, run any other execution, or performed any Git action.
