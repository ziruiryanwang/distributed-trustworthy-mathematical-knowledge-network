# Structural staging: focused control source

2026-10-17. Assignment: `memo_tests_review`, under
STRUCTURAL-STAGING-SELECTION. The canonical workspace guard passed. **Source
only: no import, test, native checker, compiler, proof, network exchange or Git
mutation was executed.** Runtime selection/adoption belongs to root.

## Ready source and exact inputs

`software/v5/client/test_workspace_staged.py`: **28,753 bytes**, SHA-256
`81b2fd8e2df54a49f3f2b5a8bb30908c073263dd1df4fc6b11077a4e85009382`.

The source targets the currently unexecuted facade `workspace_staged.py`
(12,836 bytes, `bdd539d5f3fbc48d18215e25811178c5991e8475068156353e3cce7c1a97cf1a`)
and helper `semantic_staging.py`
(10,598 bytes, `1b58f247a4f03c393fe6e52fb22037d56449b183bbb63b2767ab1b344c523be2`).
The facade performs pure structural rejection before held-store loops and uses
immutable staged identity for previews, avoiding repeated whole-packet reads.
Full readback remains at stage/describe and before/after actual admission.

The retained real data-only foundation is
`experiments/v5-local-checks/receipt-prepare-01/prepared/foundation.json`:
23,313 bytes, `736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c`.
Its exact bounded bytes are read by the proposed test entrypoint. The old
`SYNTHETIC-FOUNDATION-NOT-IMPORTED` fixture is deliberately **not** used: it
cannot satisfy the genuine pure foundation decoder.

Two retained test modules provide constructors and data, not their suites:

- `client/test_workspace_evidence.py`: 20,513 bytes,
  `59d826993b68bfa132554c560aec2ffd35979fb5b5ea1ae71d329e6f67d9aae9`.
- `client/test_workspace_mixed.py`: 29,962 bytes,
  `478de57908ebffc98093f0139f83e0a06a9609383f237cec4466086736eb0c3e`.

## Nine selected controls

| Control | Falsifiable changed-boundary behavior |
|---|---|
| 1 | Actual pure preview advances through `NeedModuleEvidence`, `NeedDeclaration`, `NeedBody`, then `STRUCTURAL_CLOSURE_STAGED`, as exact records, a committed group and its committed body are supplied. No theorem proof or receipt verifier is available to this planner. |
| 2 | Supplied groups without staged evidence, duplicate same/different-J module variants, changed bound ModuleID or summary, wrong-arity/uncommitted/malformed bodies, duplicate groups and duplicate bodies refuse. |
| 3 | Data/expression caps, wrong/malformed foundation, zero packet bytes, extra authority fields, empty openings, excessive module count, cyclic/deep data, oversized integers/strings and unsupported object types refuse. The input census agrees with canonical bytes for a Unicode/escaped-string case. Output and cost fields are exact whitelists; no context, packet, binding or warrant census escapes. |
| 4 | Actual facade structural acquisition issues only `StagedEvidence`, with zero verifier reservations/calls. After the inert contact expires, one local admission transition calls its explicitly synthetic receiver without a dial, uses the same grant/deadline, charges one verification attempt, and refuses reuse of that token. |
| 5 | Foreign-client token use, an injected synthetic receiver refusal and ordinary close revoke tokens. The refused admission remains charged; no surviving warrant or restarted allowance appears. |
| 6 | A second packet variant of the same module and exceeding the original `imports.max_sources` cap refuse before another packet transfer. |
| 7 | With packet reads made unavailable, preview still returns only authority-free structural READY using staged identity and held semantics, with zero packet reads. Admission then attempts full packet readback and refuses/revokes before the synthetic receiver. A changed held group descriptor separately refuses admission. |
| 8 | Repeated facade previews charge submitted/reloaded work. A caller-supplied but unheld body refuses. A separate fresh operation actually acquires the committed body into the real custody store; local preview then becomes READY even after the inert contact expires, with no verifier or new dial. |
| 9 | Structurally staging the mixed evidence form does not invoke either native or aggregate receipt checking. Passing its token to the warrant-only API refuses and revokes staged data. |

A static test correction is already included: changing the last J byte changes
only its allowed rank, so that is **not** a valid malformed-J negative. Control
2 instead changes byte108, inside its committed ModuleID. This is a source
correction, not a hidden rerun or reclassification of a failed allocation.

Root subsequently selected one targeted refinement before execution: control7
now asserts zero packet reads during preview, then mandatory readback/refusal at
admission. The unexecuted earlier test48020bea/selection48d5d474 and selector01
are superseded drafts, not failed or passing runtime evidence. Root preserves
the old selection and prepares fresh02 for current81b2fd8e/facadebdd539d5.
No other optional test expansion was made.

## Actual versus fabricated boundary

The prospective run exercises the real pure preview, codec/bindings, foundation
decoder, Merkle openings/body commitments, SQLite custody, workspace/grant,
facade actions and acquisition accounting. Transport is an in-process dispatch
function, with no socket. Exact issuer classes are constructed by the retained
`SyntheticOwners` fixture; their receiver/native/proof results are explicitly
fabricated. Therefore a returned test `LiveWarrant` is **not mathematical
acceptance**, real-owner construction, a genuine A receipt or public deployment
evidence. Test output states this boundary and records synthetic call counts.

The body-positive test uses the ordinary public `acquire_body` path, not a local
store injection on the consumer. The publisher is seeded with inert fixture
data, as in the selected predecessor contracts. Failed clients and fresh client
operations are kept distinct; no failed operation is repaired or renewed.

No old test suite is selected. The source entrypoint lists exactly nine method
names and reports their individual suite count, failures, errors, skips, actual
loaded project-source origins and the exact foundation pin. It requires
canonical cwd, isolated/no-site/no-bytecode Python, a fresh output path below
`experiments`, and ordinary absolute foundation input. The suite patches
`subprocess.Popen` to refuse subprocess launch.

## Proposed closure and launch boundary

Root reuses the already audited 77-source search-resilience selector closure:
remove `transport/test_search_resilience.py` and its unused fixture import
`discovery/test_candidate_query.py`; add `client/test_workspace_mixed.py`,
`client/test_workspace_evidence.py`, `client/test_workspace_staged.py`,
`client/workspace_staged.py`, and `transport/semantic_staging.py`. This yields
**80 source entries including the existing check runner**, subject to independent
exact selection review. The exact foundation is a **19th runtime/data pin**
beside the retained18runtime pins, passed by its original ordinary absolute
path and checked before/after: the runner's source snapshot allowlist permits
only `software/v5` and itself. This is a static closure proposal, not a
loaded-import census. Neither retained fixture imports test_candidate_query.

Entrypoint arguments: `-I -S -B <snapshot>/software/v5/client/test_workspace_staged.py
--output <fresh controls directory> --foundation <exact selected foundation>`.
The predecessor 30CPU/90wall/512MiB/two-process envelope is a reasonable proposed
small local ceiling, not an authorized launch. No passing claim or actual
resource measurement exists yet. Root selects any one finite run only after
source and exact selection review; genuine A and terminal reuse remain separate.
