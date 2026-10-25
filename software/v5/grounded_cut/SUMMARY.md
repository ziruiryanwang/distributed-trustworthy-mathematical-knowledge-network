# Grounded-cut inert summaries and selected closure

Source-only, 2026-10-24. `cut_summary.py` performs bounded syntax/identity work
and prepares a conditional worker packet. It does not establish an eligible
root, grant mathematical acceptance, open protected state, load native snapshots
or execute Lean. All current source changes require the separate complete
controller/worker review before any runtime selection.

## Existing mechanisms reused

The helper imports `ordinary_evidence`, `portable_evidence` and
`ordinary_semantics`. These provide canonical JSON, encoded names, universe and
expression-DAG grammar, full generated-unit census, V2 evidence identity and
portable export identities. There is no new name, expression or declaration
parser. The theorem type-only traversal follows the existing
`portable_owner_request` approach, but obtains stored compact summaries instead
of reading old complete theorem evidence on each operation.

## Projection format and trust boundary

A canonical summary has exactly these fields:

```text
schema:      DMKN_GROUNDED_CUT_SUMMARY_V1
semantic_id: exact portable interpretation ID
unit_id:     original complete V2 evidence ID
kind:        theorem | concrete
bindings:    sorted [[encodedName, exactExportId], ...]
imports:     sorted [[encodedName, exactImportedSymbolId], ...]
payload:     [universeParameters, typeDAG] OR complete concrete unit
```

Sorting uses exact canonical encoded-name bytes. The summary ID is lowercase
hexadecimal `SHA256(b"DMKN-GROUNDED-CUT-SUMMARY-V1\0" + canonicalSummaryBytes)`.
The trie leaf is controller-owned canonical `[symbolId, summaryId]`; one whole
group has one summary object, rather than copying its body for every generated
name. The helper never stores or accepts that leaf.

`project` first validates the full V2 evidence grammar, complete import census
and identity. A theorem must have descriptor kind 1, one inventory row of kind 2,
and exact descriptor/inventory correspondence for name, parameters, type, proof
and generated-name list. Its projection retains the exact parameters and full
type DAG; only references occurring in that type remain in its imports. The old
proof and its proof-only dependencies disappear from the summary. A self-reference
in the theorem's type refuses. Other supported units must be concrete descriptor
kinds 0, 2 or 3, with no theorem inventory row. Their complete unit, all imports
and whole generated inventory remain unchanged.

`read` checks exact canonical summary fields/bytes, digest when requested, ordered
name/symbol bindings, type/concrete reference census and export-ID consistency.
For concrete summaries it reconstructs the complete original V2 envelope and
recomputes its original unit ID. For a theorem, the erased proof prevents that
recomputation: **the claimed original unit ID plus a matching export-ID formula
does not prove the theorem type came from that original checked event.** This is
intentional and is not cryptographic proof compression. The protected controller
must derive/store the summary from full evidence associated with an eligible
earlier native warrant, or from a newly clean checked cut event. Arbitrary imported
short summaries cannot create that association. Neither read nor project checks
whether a theorem type is Prop; that is a real-kernel obligation of the worker.

## Python API

```python
project(raw_v2, *, limits=Limits()) -> Projected
read(raw_summary, *, expected_id=None, limits=Limits()) -> Projected
prepare(raw_new, *, semantic_id, basis, lookup, read_summary, check,
        limits=Limits()) -> Prepared
```

`Projected` is frozen and contains immutable `raw`, `summary_id`, `semantic_id`,
`unit_id`, `kind`, and sorted `bindings` tuples `(canonicalNameBytes, symbolId)`.
It is a syntactic claim even when created from an invalid-but-well-formed proof.

`prepare` callbacks have deliberately narrow contracts:

- `lookup(encodedName) -> (symbolId, summaryId) | None`: an exact point lookup
  in one stable, protected, eligible root. The argument is the existing encoded
  name JSON, not its dotted spelling. `None` must mean absence under that root.
- `read_summary(summaryId) -> bytes`: one exact content-addressed local summary
  object. The controller bounds its actual I/O before returning bytes. No old
  theorem evidence, snapshot or ancestor-event acquisition is permitted here.
- `check()`: no-argument deadline/shared-resource check, called before and after
  each actual callback and between bounded parse/closure/output phases. It may
  raise to stop the operation. It does not convert a callback into authority.

The `basis` dict is **already authenticated by the controller** against the
selected fixed 581-name foundation, keyed by canonical encoded-name bytes with
exact basis-symbol values. The helper checks shape/count and validates demanded
values, but cannot authenticate a caller-created dict. It does not enumerate
the native root or all 581 names on every request. `prepare` selects only the
current `ordinary_semantics.semantic_id`; generic project/read do not adopt a
semantic interpretation merely by recognizing its syntax.

`Prepared` contains only immutable values:

| Field | Meaning |
|---|---|
| `concrete_units` | Dependency-ordered tuple of canonical full-unit JSON bytes |
| `signature_rows` | Dependency-ordered tuple of canonical `[name,0,symbol,[params,type]]` JSON bytes |
| `new_unit` | Exact canonical full new-theorem unit bytes |
| `new_summary` | Inert projection of that new claim; cannot commit before checking |
| `frontier` | Sorted `(canonicalNameBytes, symbolId, summaryId)` for every demanded nonbasis binding, including all whole-group siblings |
| `absent_names` | Exact new-theorem name whose whole-root absence was checked |
| `stats` | Finite selected input/acquisition/name/lookup/edge/node/payload census |

The controller can decode each already-validated packet for the worker interface.
It must bind this exact content and frontier to the invocation, recheck live
authority/epoch, validate clean completion, and atomically commit its own accepted
event, summary and trie root. `Prepared` itself is not a warrant or reuse token.

## Closure algorithm and refusal rules

The new V2 claim must be one complete genuine-theorem-shaped unit. Resolve its
name against the fixed basis and the **whole** eligible trie, not only the scratch
subset; existing names refuse. All direct imports of the new full proof are
scheduled. For an already-grounded theorem, recursively follow only its retained
type imports. For concrete meanings, follow every full semantic import.

Each distinct nonbasis name is looked up once, with its answer cached only inside
the operation. Each distinct demanded summary digest is read once. After reading
a group, every generated sibling name must resolve to the exact same summary
digest and its exact export ID. Different summaries cannot overlap names or claim
the same original unit ID. Every demanded name, including additional names whose
digest was already scheduled, must actually occur among those verified bindings.
There is no whole-map scan or caller-controlled global query.

The selected group graph is then closed and topologically ordered. A concrete
unit with any direct nonbasis theorem dependency refuses
`CUT_SUMMARY_CONCRETE_NEEDS_OLD_THEOREM`; this also excludes indirect such paths
because the concrete parent at the first such edge refuses. Cycles, self-edges,
unresolved imports, semantic mismatch, inconsistent symbol IDs and partial group
membership refuse. All concrete units are emitted first, followed by signatures.
This partition preserves valid order because no concrete unit depends on a
nonbasis theorem. The new full theorem comes last. Worker checking may still
refuse valid-but-unsupported proof reductions; preparation does not guarantee
kernel success and does not trigger a native fallback or ancestry expansion.

## Costs and finite bounds

The default syntax envelope is the existing 8 MiB V2 grammar. Defaults additionally
bound one summary to 8 MiB, selected groups to 1024, distinct demanded names and
actual nonbasis lookups to 65536 each, selected import edges to 262144, acquired
summary bytes to 64 MiB, encoded-node census to 20000000, and emitted worker
payload bytes to 64 MiB. All limits are explicit trusted configuration; they do
not grow on retry or derive from peer-supplied claims. The worker has separate
scratch, kernel and process-resource ceilings which must also be satisfied.
The helper's payload count excludes the fixed seed/inventory and request framing;
the worker's aggregate input ceiling includes them. The controller must reserve
their exact bytes and serialization overhead when choosing this helper limit or
perform an exact complete-request byte preflight before starting the worker.
Passing a 64 MiB helper payload check alone does not imply worker input eligibility.

Stats count the full new input, acquired summary bytes/count, distinct demanded
names (including new-name absence and demanded basis names), issued nonbasis
lookup calls, all selected import edges including the new proof, encoded nodes
in the new complete unit plus selected summaries, and emitted new/concrete/
signature packet bytes. This is a logical census, not measurement of every
validation pass, serialized-byte copy, map I/O, CPU or peak memory. In particular,
projection separately rechecks the new type, concrete summary validation also
reconstructs a canonical envelope, and root preparation plus worker checking both
cost work. Initial native-to-summary projection still reads old full proofs once;
it is paid setup, not free cold verification.

Lookup-call and scheduled-summary counts are checked before issuing callbacks;
aggregate acquired bytes are checked immediately after a controller-bounded read
and before parsing. The controller must charge failed calls, attempted oversized
reads, original state checks, migration, SQL work, fixed foundation, kernel work,
retention and return. A failed `prepare` raises without a partial usable result;
it does not issue persistent writes or reset its caller's resource grant.

The resulting selected work depends on the new proof, demanded concrete semantics,
old theorem types and their selected closure, plus path-local indexed lookup costs.
It has no mandatory term for all old theorem proof bodies or the complete event
history. This is a locality statement, not a measured speedup or a claim that a
large semantic closure is always cheap. The separate full-cost comparator remains
necessary before promoting this optional lane.

## Focused review before runtime

Review theorem descriptor/inventory mismatch; erased proof-only imports versus
retained type imports; exact reconstructed concrete IDs; mutated summary digests;
forged same-ID theorem types requiring controller rejection; whole-group sibling
rebinding; an imported alias absent from a previously scheduled group's bindings;
freshness outside scratch; concrete-to-theorem edges; cycles; basis substitution;
callback/deadline exceptions; and each finite limit. None should be treated as a
whole acceptance test until the protected controller and recursive reuse path
are reviewed together. No test or native operation was executed by the author.
