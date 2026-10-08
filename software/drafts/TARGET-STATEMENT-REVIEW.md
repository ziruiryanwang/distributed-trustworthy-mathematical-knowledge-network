# Target statement: source and diagnostic review

2026-09-21. **PASS for source correspondence and the proposed bounded diagnostic
sequence only.** No target pipeline has been executed by this reviewer; this
note neither claims executed conformance nor commissions consumers.

Reviewed `UsefulnessTargetStatement.lean`: 643 bytes, SHA-256
`2C1F0832C82E73423D212CA5782CA28EE4088D6EC4C53C4D72F8726E3F76570E`,
against the fixed workload in `USEFULNESS-MATCHED-ENDPOINT.md` (reviewed SHA-256
`B08EDFF4FC95DF9501EB30F7536EBA4D6A2846FD24EBE02CB5266EDFD005FCCB`).

## Semantic finding

`ChunkedReductionStatement` is an ordinary universe-polymorphic definition of
a **Prop-valued family**, not a theorem or proof. Its parameters are arbitrary
`A : Type u`, `op : A -> A -> A`, and `e : A`. Its value requires associativity,
left identity and right identity, then universally quantifies
`chunks : List (List A)`. The conclusion is exactly
`R A op e (List.flatten chunks) = R A op e (List.map (R A op e) chunks)`.
All three `R` occurrences name the already checked right-fold vocabulary
definition ending `61903d4b0e3bb04e9ac15e179d35e6e4ae0b358285c91d29c5426b6c590f318a`.
There is no commutativity assumption, specialization, proof, append-law reference,
placeholder axiom, tactic or solution method. A full theorem must inhabit this
family for every `A`, `op`, `e`; defining the family does not establish that.

## Minimal diagnostic allocation

Fresh configure is followed by exactly five ordinary requests: owner `init`,
vocabulary `submit`, vocabulary `publish`, vocabulary `admit`, target-definition
`submit`. Bind each request to actual preceding returned handles. Vocabulary
publication is necessary to obtain its candidate through the selected ordinary
route; admission supplies its checked receiving name to target elaboration.

This uses four stages and twelve pipeline children: bootstrap 1, vocabulary
submission 5, admission 1, target submission 5. Reservation is
`5 * 8 + 4 * 128 = 552 MiB`. Configure consumes no request/stage. No target
publication/admission, producer lemma, corpus, service, retry, source repair or
consumer run belongs to this diagnostic. Existing per-call/native limits,
external supervision, endpoint census and separately reported preparation
costs remain required; cumulative reservation is not an aggregate CPU quota.

## Required actual-outcome checks

1. Authenticate frozen installation/runtime/source pins and native source
   capture for root `ChunkedReductionStatement`; require unchanged vocabulary
   identity, full package bytes and freshly admitted context.
2. Require all five target-submission commands to complete. Compare actual
   candidate/inverse native `id`, `kind`, `u`, `type`, **value**, replay/root,
   package closure and retained files. Expect ordinary definition kind and one
   universe parameter, never a theorem proof.
3. Inspect the reachable canonical **value**: three outer parameters, both
   correctly directed unit laws, associativity, nested-list binder, flatten on
   the left, map of the same specialized `R` on the right, and universe/type
   instantiations. The public type ending in `Prop` alone is insufficient.
4. Reconcile terminal requests/stages/reservations, receipts, quiescence and
   bounded retained output. Preserve any failed prefix and diagnose its exact
   boundary; do not relabel partial completion as conformance.

Success establishes only this exact statement-family's elaboration, canonical
export and fresh native round trip. It proves no chunked-reduction theorem,
proof-route feasibility, consumer endpoint, reuse, speedup or trial readiness.
