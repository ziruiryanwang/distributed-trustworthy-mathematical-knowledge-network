# Post-v2 publication syntax: focused regression design

2026-09-23. Author: `package_cost_probe`. **Read-only test design; no product
implementation or test execution.** Canonical workspace guard passed. Source13,
its used nodes/harnesses, failed attempts and sealed v2 delivery remain frozen.
This note proposes tests for a separately selected successor; it does not
declare the extension selected, implemented or qualified.

## Central discriminator

Can an artifact already accepted under the existing Lean/native policy be
published, found, transferred and freshly admitted without changing its exact
mathematical type merely because the local symbol index rejects its syntax?

The concrete witness is source13's original numeral-bearing `countEquations`:
native submission succeeded; publication refused at the metadata fragment.
The subsequent constructor-spelled success is not publication of that original
artifact. Do not replace this discriminator with another already-supported
theorem or rerun complete transport/custody/lifecycle campaigns.

## Actual implementation boundary

Paths below are relative to the canonical root. Line locations refer to frozen
`product-local/auxiliary-frontend-source-13`.

- `py/source_codec.py:371–477`, `transform_dag`, already validates canonical
  closed DAGs with expression tags 0 through 9. Its callback owns reference
  grammar/membership. It rejects malformed shape, duplicate nodes, forward
  edges, bad universe scope, open root, unreachable/noncanonical order and
  invalid literal bytes before an extractor can claim complete output.
- `py/symbol_index.py:72–127`, `extract_type_symbols`, calls that validator,
  rejects every projection in its callback, then rejects every node outside
  tags 0–5. Its traversal currently visits only application/lambda/Pi children.
  Removing only the tag whitelist would silently omit let/projection children.
- `py/symbol_index.py:182–192`, `describe_root.close_type_ref`, independently
  rejects projections while closing a group's first-original-type DAG. This
  second site requires separate coverage if the extension includes group types.
- `py/source_codec.py:666–683` and `812–848` restrict a projection's structural
  reference to a seed reference or an external group **type** selector. Group-
  local projections are prohibited. `native/AgentReplayCore.lean:299–309` and
  `:351` enforce the corresponding native restrictions. A generic `_ref`
  accepts more semantic reference kinds and is not sufficient by itself as a
  projection resolver.
- `py/checking.py:260–266` turns non-OK metadata into the observed
  `CANDIDATE_TYPE_FRAGMENT:*` refusal. Offer/admit metadata equality also uses
  the extractor's full trace; preserving old symbol sets alone is insufficient.

| Canonical node | Existing representation and validation | Proposed raw-syntax extraction obligation |
| --- | --- | --- |
| 0 variable, 1 sort | Existing leaves; bound variable/universe scope validated | No symbol; one occurrence per visit. |
| 2 constant | `[2, externalReference, universeIndices]` | Exact canonical external reference key; preserve first-occurrence order. |
| 3 application; 4 lambda; 5 Pi | Two expression children in stored order | Existing left-to-right traversal and depth/occurrence trace unchanged. |
| 6 let | `[6, typeChild, valueChild, bodyChild]`; body binds one variable | Visit all three children in that order, even a dead initializer or annotated type. No zeta reduction. |
| 7 natural literal | `[7, magnitudeBytes]`; minimal unsigned magnitude, empty bytes denotes zero | No invented `Nat` key or numeric search token; count one expression occurrence. |
| 8 projection | `[8, structureReference, fieldIndex, baseChild]` | Include the exact structural reference and visit the base child. The structure is not an extra expression node/depth. No invented field-name key. |
| 9 string literal | `[9, utf8Bytes]`; strict UTF-8 | No invented `String` key; count one expression occurrence. |

Literal byte limit is 1,048,576. The index's distinct limits remain 32 symbols,
4,096 expression occurrences and root-relative depth 64, inclusive. Repeated
visits to a shared expression count repeatedly; unique DAG-node count is not
the occurrence measure. Literal bytes/reference bytes are validated by the
existing bounded representation layer, not expanded into occurrence units.

**Important support distinction:** `AgentReplayCore.lean:141` still rejects
`INITIAL_EXTERNAL_STRING_LITERAL_UNSUPPORTED` during source extension capture.
Tag-9 metadata structural coverage is not evidence that arbitrary string-bearing
ordinary source contributions are supported. This work must not change that
native restriction or promise source acceptance on the strength of a synthetic
index fixture.

## Minimal focused matrix

These are proposed test groups, not passed tests. Synthetic closed DAGs test
representation/index behavior only; they need not denote a well-typed Lean
TYPE and must never be labeled native mathematical acceptance.

| Group | Fixed discriminator | Required observation |
| --- | --- | --- |
| A — unchanged domain | Selected existing tags-0–5 definition/theorem/group metadata plus raw lambda/Pi and shared-DAG fixtures | Exact complete output equality against source13, including descriptor/type IDs, symbol order/keys, trace, bytes and no mutation; not just set equality. |
| B — leaves | Canonical zero/nonzero natural and empty/nonempty UTF-8 leaves embedded in synthetic type DAGs | Literals add no keys; each occurrence counts; surrounding ordinary symbols remain ordered. No implicit literal-type symbol injection. |
| C — all let children | Three distinct keys placed solely in type, value and body; body uses a bound variable; include unused initializer and a shared repeated child | All three keys found in source order, no unfolding/reduction, complete exact occurrence/depth trace. No child silently skipped. |
| D — projection | Seed structure plus separately keyed base; external group-type structure absent from base; same structure elsewhere as ordinary constant; two distinct exact type selectors | Structural key included even when absent from base, base traversed, exact-reference deduplication, selector identity preserved. Field index is not a new symbol. |
| E — group metadata route | Synthetic group's first type contains an **external** seed/group-type projection and let children; another case retains legitimate local constant closure | `describe_root` reaches the same complete extraction as the closed effective type; virtual type CID exact; no store mutation/addition. Local projection still refused rather than closed into an external one. |
| F — malformed inputs | Wrong arities/tags; nonminimal natural; invalid UTF-8/oversize literal; bool/negative field index; forward/unreachable/open DAG; bad projection references | Fail closed with no row/symbol result. No coercion, normalization, partial output or accepted-source claim. |
| G — unchanged ceilings with new syntax | Exact and one-over 32 keys/64 depth/4,096 occurrences, with the crossing key/depth/occurrence reached through a new let/projection edge | Inclusive exact limit succeeds; first over-limit refuses with existing bound reason and no partial symbols. A projection's structure can be the 33rd key; let hidden children cannot bypass any cap. |
| H — actual accepted artifact/public seam | Original accepted literal-bearing Count package, plus changed-metadata tamper control | Exact original theorem/root/type/body remain unchanged; successor metadata can describe/offer/find it; acquired metadata mismatch still refuses before native admission. Full positive publication and fresh receiving acceptance require a separately reviewed finite native allocation. |

For G, a small canonical shared binary application DAG can represent 4,095
expression visits; wrapping it in one synthetic projection gives exactly 4,096
without excessive unique nodes/depth. One additional wrapper gives 4,097. This
tests the new edge rather than enlarging limits. A similar projection chain
tests root-relative depth 64/65; keep symbol cardinality low so the depth gate
is the first blocker. Distinct-symbol fixtures should use structurally valid
seed/external references and keep occurrence/depth far below their limits.
Expected counts should be derived by a tiny independent fixture oracle, not
copied from the implementation under test.

For F's projection references explicitly cover: seed index out of range;
definition/theorem/opaque/witness/source/local references; group constructor,
main recursor or auxiliary selector in structure position; malformed CID or
selector; boolean/negative/extra selector fields. Do not claim a syntactically
valid seed index names a real structure, or that a nonnegative field exists:
those semantic obligations stay with native checking. No proof/body reads are
allowed merely to compute a raw type-symbol set.

## Retained test material to reuse selectively

- `experiments/lean-agent-api/test_symbol_index.py`: synthetic immutable Store,
  canonical shared-DAG builder, type-only/no-body-read tests, raw beta/lambda/Pi
  behavior, selector-sensitive keys, occurrence accounting, depth64/65 and
  symbols32/33. Its old let-rejection assertion remains historical; do not edit
  that used test file. Reuse/adapt helpers in a new selected test file rather
  than rerunning its unrelated snapshot/page/cursor campaign.
- `experiments/lean-source-composition/test_source_codec.py`: retained tests
  `test_literal_magnitude_and_utf8_checks`, open/unreachable DAG rejection and
  group-selector/projection membership checks. These justify focused inherited
  grammar expectations, not a new proof of native acceptance.
- `experiments/public-group-roots-01/test_contracts.py`: actual common Subtype,
  definition and proof fixtures; exact predecessor metadata comparison;
  two-type local closure; synthetic no-mutation Store image; snapshot/find;
  actual-offer-to-native-boundary intercept; descriptor/formal-metadata/symbol
  tampering refused before the mocked stage. Reuse only the changed seam.
  Its `CONTRACTS-OUTCOME.md` preserves the existing scoped eight-group pass.
- `product-local/auxiliary-frontend-source-13/assets/common/*`: retained exact
  common packages for unchanged metadata checks. Do not infer that a fixture
  uses let/projection in its TYPE without actually inspecting that type.

Old-domain trace equality matters operationally: selected peer acquisition and
fresh admission compare metadata exactly. An indexing extension must not make
old tags-0–5 offers disagree simply by changing traversal order or metrics.
If new tags cause old peers to refuse, record the observed operation where
refusal occurs; do not assume catalog browsing itself must reject. No implicit
old-node migration or false cross-version interoperability claim follows.

## Actual-source positive boundary and stop condition

The independently audited original source13 evidence is
`experiments/auxiliary-frontend-01/EXERCISE-OUTCOME.md` (5,950 bytes, SHA-256
`0c8f039e417968d9aba2742ec490dcb07b0a89f9c8767b74995b241f9afab9ab`).
It binds original `reciprocal-01/RESULT.json` (108,806 bytes, SHA-256
`6dfbe98d11a156025463d7b07b4411bdfc501b44770ceae918bb3792bc577536`),
the actual full native accepted Count type/proof, two definitions and received
Rose group. Its canonical type has exactly one excluded node: node 26,
`[7, {"$bytes": [1]}]`. Its original native plan is 740,791 bytes, SHA-256
`cefa1ac7105c3e5cc51c91e3f313cc4a7233e0d3073d6679656ae6640448b139`.

This supplies an actual-source witness without guessing new accepted syntax.
The first cheap discriminator can inspect this exact retained inert package
under successor metadata and compare all type/definition/proof identities.
For the consequential integrated test, select fresh successor installation/
allocation explicitly; keep all old nodes and source13 failures unchanged.
Use the **original** Count statement/source, not `CountPublishable.lean`.
Require publication, discovery/acquisition and fresh receiver admission after
the finite sender stops, with exact original type identity throughout. No
rebuild of v2 or account reset is authorized by this design note.

If actual-source let/projection claims are desired, obtain a retained actual
captured TYPE containing those tags or a separately selected native fixture
first. Surface Lean `let` or `x.field` text alone is not evidence: elaboration
may remove a let or encode a named projection as an ordinary constant. A native
run that happens to eliminate the target node does not qualify that boundary.
Do not broaden the test into arbitrary library integration or guess a theorem
and label it supported. String-source capture remains explicitly outside this
index-only change.

Stop after the focused changed-seam matrix and one independently audited
actual original-numeral publication/return result establish the selected
contract, or after a concrete failure refutes it. Preserve all actual costs,
failures and source maps. Neither outcome establishes novelty, useful growth,
global discovery, unlimited operation or a perfect release.
