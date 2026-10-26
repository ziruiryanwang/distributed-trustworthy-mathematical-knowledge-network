# Independent sparse candidate / HTTP source review

2026-10-25, `search_locality_argument`. **GO for the selected source boundaries;
not execution, package adoption or v5 completion.** No blocking finding in the
complete candidate/HTTP successors and their diffs against the frozen contact
package. This reviewer did not author either file. No import, test, network,
database or Git mutation was performed. Pair/Store review belongs to the other
reviewer and is not duplicated here.

Reviewed files under `software/v5/ordinary_sparse_access`:

| File | SHA-256 |
|---|---|
| `candidate_query.py` | `62de52fdd95df045632e865f90e5ec6ea076c8a1f68937d437597905e63a478b` |
| `http_provider.py` | `f81cdcaebbf05ad97342b81ac64444b33695b576045c8da41ba6f0a0903dd691` |

Baseline: contact-federation-assembly01 package PROFILE
`3d127796190ca3d049bd956288025c10c4ac7e383a15685aca6ea8d2fbc61479`.
Criteria: adopted SPARSE-ACCESS-CONTRACT `e31815e9...` and selected source
CONTRACT.md. The root-owned session/FairSearch/public forwarding integration is
a separate review boundary; these files alone do not establish its correctness.

## Checks and reasoning

- **Explicit mode and V1 preservation.** Public candidate functions require a
  Boolean sparse option. Schema/field/cursor choice is fixed by that option;
  HTTP derives it from the exact route, not a reply. With sparse=False, no pair
  helper is invoked; old schemas, atomic traversal, shared proof verification,
  charges, output fields and the original cursor-distance condition remain.
  The added per-row memberships dictionary does not change default decisions.
- **Original proofs.** Sparse candidates retain the verified summary's original
  minimum atomic anchor. Every emitted canonical record still carries the
  original vector proof at its actual atomic ordinal, satisfies all requested
  features and partition binding, and passes bounded strict hit ordering and
  duplicate checks. No cache claim substitutes for the Merkle proof.
- **Old snapshots / encountered corruption.** The helper is called with the
  exact old anchor-count ceiling. Returned tuple fields are bounded; cached
  object identity, companion ordinal and admission sequence are checked against
  original postings/objects and old-cut counts. Even an extra-conjunct rejection
  loads the canonical record and checks queried-feature membership agreement,
  preventing encountered inconsistent pair/secondary metadata from silently
  becoming a normal rejection. This does not authenticate unvisited omissions.
- **Single finite meter.** Planning and sparse/atomic fallback share one ReadIO.
  Each attempted driver seek is precharged to scanned; pair seek also charges
  a record probe and SQL work. Empty end seek is not free. All SQL statements,
  node reads, hashes, record loads and proof attempts remain bounded; the
  progress handler and busy timeout are restored in finally. No nested page
  call renews an allowance.
- **Early stop and cursor.** Planning finishes before publishing non-null
  anchor_count/access_used. Interrupted seeks and unreported byte-exhausted hits
  do not advance the saved position. Successful rejection may advance; successful
  empty seek may reach the old anchor boundary. The verifier accepts sparse
  distance only in V2, retains counter ceilings/shape and original hit bounds,
  and strictly rejects Boolean cursor integers. Its result always states
  positive-only verification, false scan coverage and false global completeness.
- **Response cap.** Wire upper-bound estimation reserves the longest pair
  diagnostic before planning, plus worst bounded counters/cursor/termination.
  Proposed complete responses are size-checked before accepting each hit.
- **HTTP exposure.** The sole new route has the existing 1 MiB maximum, strict
  V2 validation before reply reservation, caller byte cap, unchanged global
  provider allowance, original remaining operation-time narrowing and one
  dispatch. The provider copies the dispatch request before local narrowing.
  Unsupported/malformed requests close boundedly; no automatic V1 retry,
  negotiation, configuration write, rebuild or new peer-selected authority.

## Retained limits and next evidence

Resource counters, cache selection and terminal cursors remain advisory claims;
they cannot prove skipped-interval coverage. An honest cache is needed for the
selectivity argument, and arbitrary missing rows need not be detected. SQLite
deadline enforcement is cooperative, with the existing external containment
premise. V1's historical behavior is preserved rather than broadly requalified.
The review does not establish semantic usefulness, huge-network completeness,
TLS deployment or growth advantage.

Root can proceed to its separately selected focused source-backed tests and
public integration review. Required changed-boundary evidence remains: tiny
high-ordinal hit, both orientations, old-cut exclusion, extra-conjunct rejection,
meter exhaustion without advance, wrong schema/cursor/proof refusal and charged
unsupported transport. No native mathematical experiment is needed for this seam.

Separately, during this review root explicitly authorized a pre-freeze repair
to this reviewer's own pair_access source after the independent Store reviewer
found persisted bool/integer config equality. That repair is not self-approved
by this candidate review and remains with the independent Store reviewer.
