# Prospective matched consumer packet

Not dispatched. Root fills only the per-arm fields below after common onboarding,
target-statement conformance and launch review. Both fresh no-history consumers
receive the same common text and documentation. This is an evaluation goal, not
a goal field or task queue in the product. Do not send this evaluator preamble.

## Common consumer text

You are independently evaluating a development Lean 4 mathematical node. Choose
your own proof strategy and whether available shared knowledge is useful. The
endpoint is a checked, published portable theorem through the documented API.
A local proof sketch or bare Lean compilation is not that endpoint.

Let `R A op e xs` be the checked receiving definition supplied in your onboarding
description. It is the right fold, with body:

```lean
List.rec (motive := fun (_ : List A) => A) e
  (fun (a : A) (_ : List A) (acc : A) => op a acc) xs
```

For arbitrary `A : Type u`, `op : A -> A -> A`, and `e : A`, assume associativity
and both unit laws:

```text
forall a b c, op (op a b) c = op a (op b c)
forall a, op e a = a
forall a, op a e = a
```

Prove for every `chunks : List (List A)`:

```text
R A op e (List.flatten chunks) =
  R A op e (List.map (R A op e) chunks).
```

These displays specify mathematics; use the actual supported source syntax
documented in your API. Do not add assumptions or specialize the statement.
You may use direct or library-based proofs. You are not required to use a peer.

Read the supplied frozen API and core documentation. You may inspect the
permitted local Lean library sources and seed inventory to understand available
constants. Do not inspect evaluator research, other consumers, producer sources,
corpus directories, trial outcomes, or private node files. There is no permission
to browse the web, spawn another agent, execute product/proof code, edit product
code, or start a service. Bounded read-only file/search tools (for example `rg`
and PowerShell file reads) are permitted within the listed documentation/library
paths. These are cooperative evaluation restrictions, not an OS sandbox.

Only the root operator executes product calls. Send a requested ordinary API
operation as exact JSON, or an inspection request explicitly labeled `inspect`,
using your own returned handles. The operator forwards it unchanged and returns
the result without choosing mathematics, rewriting source or suggesting entries.
For source submission you may place the exact UTF-8 source in your assigned
output file with `apply_patch`; identify the root declaration. The operator may
read those bytes into the request but does not repair them. Do not invoke Python,
Lean or a shell-based substitute to test your proof privately.

The trial permits at most 24 ordinary requests after onboarding, including at
most two submissions, three admissions and seven acquisitions, plus at most two
read-only inspections. Publication consumes an ordinary request. You have 45
minutes from the recorded dispatch timestamp. Publication must finish before
the deadline. The measured trial budget is 600 disjoint Job CPU seconds; this is
an observed qualification ceiling, not a hard aggregate limit. The operator stops
new work at a reached ceiling and retains in-flight costs; late or over-budget
completion will be recorded separately. Unmeasured agent compute is not free.
There are no renewals, recovery attempts, replacements or deadline extensions.

If your arm has a peer, discovery/acquisition is optional and temporarily
available until the supplied retrieval cutoff. Its service costs count toward
your arm. Acquired packages remain usable after expiry, but acquisition alone
is not mathematical admission. No peer restart is available. Unknown/pending
operation outcomes stop the arm for evidence; do not invent another request ID.

Report the published handle if successful. Otherwise report the exact boundary
where you stopped. Do not equate a valid statement definition with a proof of it.

## Per-arm fields (freeze before dispatch)

- Fresh agent name, assigned source-output path and request-ID prefix.
- Actual current context and P1 snapshot from matched onboarding.
- Actual vocabulary reference, receiving name, full checked type/description.
- Identical permitted documentation paths and hashes; exact read-only Lean
  library root and seed inventory path/hash.
- Available peer alias, or none; treatment's absolute retrieval cutoff.
- UTC dispatch timestamp, absolute 45-minute endpoint deadline and host load note.
- Model/effort inherited identically through fresh no-history spawns; preserve
  returned agent metadata without claiming unavailable runtime details.

Root randomizes sequential arm order before either dispatch and preserves the
draw. No inter-arm feedback, consumer repair, target weakening or retrospective
budget change. The two final proofs are independently audited for the full
statement and actual reachable dependencies. An endpoint and substantive shared
reuse are separate outcomes.
