# Construction-local binding reuse: source argument

2026-10-26. `practical_library_route`. Source implementation only; no Python
import, AST execution, test, native operation, build, owner state or Git change.
This note establishes conditional source equivalence, not measured acceleration,
kernel soundness, successful Std intake or final-v5 completion.

## Exact scope

Frozen predecessor: `software/v5/ordinary_baseline/baseline_bundle.py`, SHA256
`d5a9c13392e2de8b170cbaf4a9a27e4d1e5d99eb2714165848a640069fe42fce`.
Successor: this directory's `baseline_bundle.py`, SHA256
`e4b52c2f2e823cc98aa37c8cc7adb0cf79952def9c19b54d7072116a39fa19b6`.
Predecessor was rehashed after writing the successor and remains unchanged.

Only `bind_writer` changes: retain the first unit serialization; replace its
construction-local `PE.read_evidence`/`_measure_parsed` calls with the same
envelope/import checks and measurement while reusing the just-computed unit
census and encoded unit bytes; replace subsequent `parsed.unit_id` uses with
the identically computed local ID. No helper or cached-object argument is added.
`_measure_parsed`, `_measure`, `validate_batch`, `make_manifest`, all other
functions, schemas, signatures, constants and ceilings remain unchanged.

## Assumptions and statement

Assume the selected unchanged E, PE, S and C helpers, their unchanged default
limits and identity domains; no hostile in-process/concurrent mutation of local
objects or helper globals; a nonmutating budget callback. These are construction
assumptions, not permission to trust a peer's supplied census or success report.

For any input tuple on which both algorithms finish without a resource/budget
refusal, the successor returns exactly the predecessor's manifest bytes/hash,
batch boundaries, raw unit bytes, targets/IDs and aggregate census. Every malformed
input rejected through the omitted duplicate inspection is still rejected by
the retained first inspection or the retained envelope checks. This is not a
claim of identical timeout, allocation-failure or wall-clock behavior.

## Local serialization lemma

The unchanged bounded writer parser produces ordinary JSON values: arrays,
objects, strings and unsigned integers. There are no object hooks producing
custom mutable classes, executable values, floats or bool/null tokens. Let U
be the current unit after the retained `E.inspect_unit(U)` succeeds. Let C(U)
be that census and J(U) its successful `E.canonical_json(U)` encoding.

The successor constructs R by canonical encoding the exact dictionary containing
U and locally constructed schema, semantic ID and ordered imports. It then
still calls `E.strict_json(R, PE.DEFAULT_LIMITS)`. If that call succeeds, its
decoded unit is structurally equal to U: canonical encoding and strict decoding
are inverse on this admitted JSON domain. Strings which cannot encode, excessive
raw depth/tokens/size, duplicate keys and noncanonical bytes still refuse.

Consequently, deterministic `E.inspect_unit(decoded_unit)` under the same limits
would return C(U), and `E.canonical_json(decoded_unit)` would return J(U).
Neither recomputation is necessary here. No later external reader receives this
exemption, and no helper accepts caller-provided C(U) or J(U).

## Every portable-reader and measurement obligation

| Obligation from the unchanged reader | Successor justification |
|---|---|
| Exact default E.Limits type | Same explicit check on PE.DEFAULT_LIMITS |
| Raw byte/depth/integer/string/UTF-8/canonical grammar | Full unchanged strict_json call on newly constructed R |
| Exact envelope fields, schema, semantic hex | Same explicit checks after strict decode |
| Complete unit syntax, names, declarations, DAG references and atomic groups | Retained first inspect_unit(U), plus serialization lemma |
| At most 65,536 imports | Same bounded E._array on decoded imports; not inferred from unit size |
| Import row arity, name validity, symbol hex | Same per-row E._array/name_key/_hex checks |
| Exact ordered, duplicate-free external reference census | Same tuple(import_keys)==C(U).external_names check |
| Unit identity | Same SHA256(PE.EVIDENCE_DOMAIN ASCII + NUL + exact R) |
| Raw-unit byte bound and selected semantic equality | Same explicit measurement checks |
| Output binding bytes | Same per-output export ID, canonical row length and budget checkpoint |
| Nodes, output names, imports and native-array bytes | C(U).total_nodes, decoded rows/imports, len(J(U))+2 |
| Per-unit batch and aggregate limits | Same _fits_batch and _total_bound calls before _Measured |
| Raw byte hash/Entry checks | Same Entry(unit_id, SHA256(R), len(R)) |

The prior unit-size, writer-statistics, complete-basis correspondence, target,
topological binding, duplicate-output, aggregate and final manifest checks remain.
Measurement reuses bytes solely from the current unit, never a prior unit or a
caller-provided cache. The output-loop and measurement-loop budget checkpoints
remain at the same logical boundaries, though elapsed computation is reduced.

## Induction over the writer order

Both versions begin with the same exact fixed-basis available map. Suppose their
maps, accumulated census and prior measured units agree before unit i. They inspect
the same U, obtain the same ordered imports and encode the same R. The lemma and
table give the same unit ID and _Measured value. Thus both extend available with
the same export IDs and targets, retaining the induction hypothesis. The unchanged
splitter and manifest constructor then give identical final batches and manifest.

Malformed units still encounter the original inspector before envelope creation;
malformed fresh envelopes/imports still encounter explicit reader checks. Generic
raw-unit entry points retain the complete PE.read_evidence call. Faster work can
legitimately finish where the predecessor exhausted its budget; no cap is raised.

The cost removed is one repeated full unit inspection and one repeated unit
canonical serialization per writer unit. The full writer parse, fresh envelope
strict parse/canonical check, imported-name checks, hashing, filesystem writes,
native extraction and recipient verification all remain. No measured fraction of
the observed 68.71875 controller CPU seconds is attributed to the removed work.
Retaining J(U) can increase overlapping live memory during envelope parsing; no
peak-RAM reduction is claimed. For successful units its bytes fit inside the
bounded evidence envelope; rejected input still needs the outer memory limit.
Duplicated envelope-check source creates a maintenance obligation: future PE
reader changes must trigger a fresh equivalence review of this local construction.

The realistic motivation is the source-supported approved-project warm route in
`research/cycles/v5-2026-10-26-local-discovery/STD-WORKFLOW-DECISION.md`: explicit
independent library grounding followed by bounded new endpoint checking. The
failed std-export01 remains failed; this successor is not installed or executed.
