# Benefit case decision: do not manufacture a profitable SAT workload

2026-10-20, core_growth. Source/theory only; no solver, proof, build or Git run.
**NO-GO for the proposed propositional-search experiment.** This supersedes the
construction recommendation, not the cost distinctions, in
`BENEFIT-WORKLOAD-DECISION.md`. No exact supported clause family with a justified
positive full-cost benefit region has been selected. Stop this case construction.

## Existing optimized comparator, not a homemade weak solver

The local Lean distribution contains `software/runtime/lean-4.34.0-windows/bin/
cadical.exe`, 1,176,064 bytes, SHA-256
`e2604fce7746795bf5949a43caaffbda06a9aabd2d038eb512978d87e2d45486`.
Its bundled `Lean/Meta/Tactic/BVDecide/External.lean` uses `cadical INPUT OUTPUT
--lrat --binary=<bool> --quiet --shrink=0` with separately selected solver mode.
This establishes a real locally available alternative, not its runtime cost or
compatibility with our canonical export. No executable was invoked here.
Both arms must receive this solver, structural simplification, short known proofs,
equal initial mathematics, proof reconstruction, generalization and local caching.
The baseline does not receive the producer's *new* proof for free. Conversely,
the network must not pretend to save searches for results already in either cache.

## Why the candidate does not clear source-level gates

| Gate | Concrete obstruction |
|---|---|
| Exact mathematical family | Neither a fixed input nor a parameterized family survives all gates below. Random hard cases without prospective inputs are not evidence; selecting them after observing runtimes would need a disclosed selection protocol. |
| Constructive endpoint | Church disjunction supports the small resolution term in the predecessor note. That does not reconstruct arbitrary CaDiCaL LRAT output. Bundled `Formula/Class.lean` distinguishes RUP `Liff` from RAT `Equisat`; accepting each RAT clause as an implication is invalid. |
| Representation | Canonical defaults bound depth to 192 and nodes to 250,000. A naive type with n atom binders and m clause-premise binders already has depth at least n+m. Balanced encodings change the endpoint and add extraction/elimination costs; named lemmas do not automatically compress expanded expression subtrees. |
| Independent discovery | A fresh consumer cannot construct an exact declared-type key containing a producer's unknown local `OrC`/`FalseC` identities. Inline encodings or an equally supplied shared encoding could fix identity, but no selective query derived from an independently chosen target is specified. Generic arrow features plus corpus scanning do not qualify. |
| Genuine downstream reuse | Renaming atoms is not sufficient evidence. Different substitutions must lead to distinct warranted endpoints, with actual premise proofs and generalization costs included. No such fixed supported pair is supplied. |
| Cost advantage | Tiny Horn/chain examples succumb to propagation; familiar structured families admit structural alternatives; general SAT cases lack a supported proof/reuse boundary. No credible avoided-search bound outweighing integration costs is established. |

Therefore do not implement a DPLL solver, LRAT importer, Church-clause framework,
new index or another certificate just to obtain a flattering growth benchmark.
Exact-type discovery and ordinary author/admit/publish already exist; failure to
find a profitable example is not itself evidence that those features are absent.

## Costs and the two comparisons remain non-negotiable

Sharing a new native proof is compared with independently equipped local libraries.
Optional succinct certification is then compared with that same native-sharing
route. Ordinary sharing need not outperform an identical copy of itself.
Count N independent first discoveries of a missing core, not N warm substitutions.
Charge producer search, clause extraction/generalization, proof reconstruction,
semantic/type/proof bytes, native checks, premise discharge, query planning and
failed queries, provider work, transmission, publication, retention and repair.
Use an explicit finite support horizon and sustainable service allocation.
Common checking cancels only for equivalent proof/check endpoints. Alternative
short proofs and solver/core caches remain available to both arms.
Known integrated startup costs about 14.28 CPU seconds; the denied cold entry
costs about 6.3 seconds. These are NOT query timings. Charge cold startup or give
an explicit live-session workload that amortizes it; repeated cached uses do not
create additional avoided discoveries. No profitable N or horizon follows here.

## Higher-payoff next central boundary: ordinary Lean interoperability

A concrete source-evidenced restriction is more actionable than speculative SAT:
`software/v5/modules/source_rows.py:expression` rejects literal expressions;
`codec.py:validate_expr` has no literal constructor; receipt `policy.rs` sets
`nat_extension=false` and `string_extension=false` over a 22-declaration basis.
Thus existing Std LRAT or Mathlib arithmetic sources cannot be advertised as
usable contributions merely because the runtime supplies Lean and CaDiCaL.
This restriction also affects ordinary numeral-bearing mathematical definitions.
It is a real semantic-import boundary, unlike an invented missing search feature.

Recommended next selection: a bounded SOURCE-ONLY feasibility decision for
admitting native natural-number literals through the existing canonical lane.
Compare exact constructor lowering against an explicit literal-format/policy
extension. Start with the exact term `fun n : Nat => Nat.add n 2` and its ordinary
kernel type, not all of Mathlib or a new native-only contribution framework.
Determine whether the actual adopted foundation/renaming supplies the exact Nat
declarations; how the native literal's type and computation are preserved; and
whether constructor lowering can remain inside the unchanged checker relation.
Reject arbitrary `OfNat` reinterpretation. A pure untrusted lowering is acceptable
only if unchanged fresh checking validates its result and source correspondence
is established; syntactic replacement alone is not that argument.
Account for unary expansion: large numerals need a size refusal or justified
compact elaboration, not a silent limit increase. If literal support requires a
new receipt relation/image, report that exact dependency before selecting work.
The decision's output is one supported minimal lowering seam or a specific
semantic obstruction; no library port, experiment or proof campaign follows
automatically. Root chooses this against other current central obligations.

This note neither demonstrates positive growth nor weakens the final-v5 goal.
It terminates one low-payoff route before implementation, leaving the current
coherent distribution and all predecessor evidence unchanged.
