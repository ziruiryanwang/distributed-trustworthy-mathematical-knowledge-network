# Closure-order bridge: standalone mathematical handoff

Current candidate: `TheoryB02.lean`, namespace `RepairTheory.ClosureBridge`,
Lean 4.34.0, `public import TheoryA`. Status: **minimal source correction complete;
this revision is not compiled**. SHA-256:
`d1397331c7b633fec21558189c2eaa45b76642c49d5ca3f359a01f6e623c5bb4`
(183 lines). B launched no compiler or runtime. No commons admission is claimed.
Later checking status must identify the exact source revision.

The original `TheoryB.lean`, SHA-256
`bf3b0947459feca323403ea4e1263133efd5ab6a53eb69f44d6ebf9dd0fea54e`,
is preserved unchanged. Root's first bounded ordinary compilation loaded TheoryA
but failed one elaboration at line 69, in `pointwise_le_iff_fixed_inclusion`.
The shorthand `hx ▸ h x` inferred transport through both arguments of the order
relation. TheoryB02 changes only that proof line to explicit transport with motive
`fun y => o.le (r.apply x) y`, holding the left argument fixed. There are no
statement, definition, namespace, or other proof changes. Original diagnostic:
`experiments/v5-local-checks/concept-theory-b-01/command/stdout.txt`.

Its dependency TheoryA was reported by root to compile
successfully at SHA-256
`d2391e4a1a69d1ce57274ed011cd16734457e8239d2831a8e6eddd3349cbd9d9`.
An ordinary source check is not commons acceptance or recipient usability.

## Mathematical extension

TheoryA's Repair is an idempotent operation; Follows r s means s preserves states
fixed by r. TheoryB adds an information order. A repair is a closure operator when
it is extensive (x is below r(x)) and monotone. Idempotence is inherited from A.
This supplies canonical least extensions of inputs, while allowing many accepted
states. It connects the asymmetric repair calculus to established closure-operator
theory; no mathematical novelty or literature priority is claimed.

All names below are in `RepairTheory.ClosureBridge`:

| Interface | Meaning |
| --- | --- |
| `OrderData α` | Relation `le` with reflexivity, transitivity and antisymmetry. |
| `IsClosure o r` | Extensivity and monotonicity of A's repair r for order o. |
| `below_fixed` | If x <= y and r fixes y, then r(x) <= y. |
| `follows_iff_swap_le` | For closures, Follows r s iff r(s(x)) <= s(r(x)) for every x. |
| `mutual_follows_iff_commute` | For closures, mutual preservation iff the operations commute. |
| `pointwise_le_iff_fixed_inclusion` | r(x) <= s(x) for every x iff every s-fixed state is r-fixed. |
| `same_fixed_same_output` | Two closures with the same fixed states have equal outputs at every input. |
| `AllClosure o rs` | Every member of the list rs is a closure for o. |
| `run_extensive` | A finite run of closures extends its input; no Safe premise is needed. |
| `run_below_settled` | Any such run stays below every jointly fixed upper bound of its input. |
| `run_is_least` | A Safe run of closures computes the least jointly fixed upper bound of its input. |
| `same_constraints_same_run` | Two Safe closure schedules with equivalent Settled predicates have equal outputs. |

The inequality in `follows_iff_swap_le` has a precise orientation. A runs lists
left to right, so preservation for “r, then s” says that output s(r(x)) dominates
the reverse output r(s(x)). Equality needs both preservation directions.

The last theorem allows different lists and different intermediate repairs. Its
premises are AllClosure for both lists, Safe for both lists, and
`∀ y, Settled rs y ↔ Settled ss y`. It asserts pointwise equality of their runs.
It does not claim arbitrary permutations of closures are safe.

## Models and sharp limitations

`pairOrder` orders Boolean pairs componentwise with false below true.
`installLeft` sets the left fact to true. `propagateRight` replaces the right
fact by the disjunction of both facts. `installLeft_closure` and
`propagateRight_closure` establish the extra order hypotheses.

`propagation_follows_installation` proves the order install then propagate is
valid. `installation_does_not_follow_propagation` refutes the reverse preservation
direction. `directed_closures_need_order` proves the two orders have different
outputs on (false,false): install then propagate yields (true,true), whereas
propagate then install yields (true,false). Closure structure alone therefore
does not eliminate scheduling obligations or imply one-pass settlement.

`choices_have_no_common_closure_order` returns to A's choose false/choose true
repairs. There is no partial order on Option Bool making both closures at once:
their mutual preservation would imply commutation, contradicting their behavior
on none. Thus the new assumptions cannot simply be supplied by reinterpreting
every noncanonical repair example.

The generic theory assumes a partial order and supplied closure proofs. It does
not construct such an order for arbitrary repairs. It does not prove termination
of repeated unsafe runs, infinite-schedule convergence, optimal execution cost,
decidability of the premises, or existence of closure repairs for arbitrary
constraints. “Least” means order-theoretic least among jointly fixed upper bounds,
not least running time or smallest proof.

## Checking and extension boundary

The source contains ordinary structures, list induction, equality transport and
finite Boolean decision proofs. It has no sorry, added axioms, unsafe code,
plugins, evaluation commands or external commands. Definitions are exposed for
downstream reduction. The original B revision failed as recorded above; B02 has
not yet been compiled. Source correctness, kernel acceptance, transportability
and actual recipient reuse must be kept separate. A reader can use the public definitions and statements
without consulting B's private research record.
