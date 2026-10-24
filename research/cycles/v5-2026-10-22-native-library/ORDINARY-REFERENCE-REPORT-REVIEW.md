# Reference report binding: independent source compatibility review

2026-10-24. `reference_soundness_audit`. Canonical workspace and explicit shell
workdir retained. Review only: no parser import/run, native build/import, owner
operation, registration, test or Git mutation. This is the newly assigned
report/schema boundary, not another semantic-design or producer review.

## Disposition and exact sources

**PASS for the selected inert metadata-binding source contract.** No blocking
request/native schema, whole-unit census, projection or counter mismatch was
found. This is not executed compatibility evidence and does not authorize a
saved report to register a reference.

| Source below `software/v5/ordinary_baseline/` | SHA-256 |
|---|---|
| Reviewed `reference_report.py` | `00f138f565b5ecae632f9af9f0d0d71f5a648bae98016b76f15ead559eae071e` |
| Prepared request `reference_request.py` | `a4cadb4beb75bdf86b7314a2c05e301cbbafd42da8500ccd524c82c7a7503923` |
| Exact native matcher `OrdinaryReferenceBase.lean` | `5120d6bb7939e32b2c2cd45981dde015d9e041fd9d7a05e11cc453ce5fd3b30a` |

Inspected supporting definitions: `baseline_bundle._measure_parsed`,
`baseline_snapshot._module`, `ordinary_evidence.inspect_unit` and its DAG census,
`ordinary_admission._writer_json`, and `OriginalDecl.descriptorNodes`,
`inventoryNodes` and original descriptor encodings. No support source changed.

## Schema and identity binding

The exact top-level field set matches the current native report, including both
projection fields in every public output, all ten counters, zero `checked_units`
and empty `added_names`. The parser retains the raw output hash rather than
requiring native object-key order to equal Python's canonical order. Its native
writer parser preserves duplicate-key, token/depth, integer and byte limits.

All five identity labels and the full target array must equal the pinned
prepared request. The request's raw hash is rechecked; its exact private unit
order and name/symbol/unit bindings are compared with the planner's companion
data. Unit rows must be distinct, nonempty, bounded and match every requested
output name. The underlying request remains one produced from actual current
warrants; a Python dataclass constructor is explicitly not an authority.

The native `private_unit_ids` array follows request order. Native `publicRows`
walks that same order and emits only selected whole units. The parser therefore
correctly requires a strictly increasing private-order subsequence, complete
matching output-array lengths, exact names/ExportIDs/kinds/ordered universes,
and public inclusion of every selected target. It does not accept a single
advertised constructor as the whole checked inductive unit.

Both `projection` and `kernel_projection` must independently be `full` or the
permitted `erased_singleton_theorem`. `_singleton_theorem` matches the native
criterion using the original six-field theorem descriptor, singleton inventory,
`all = [own]`, and exact expected theorem row. An erased definition, opaque,
group or nonsingleton theorem cannot pass that branch. The two classes need not
be identical, in agreement with the exact native source.

## Module membership

The replay metadata uses the prepared replay schema and size ceiling. Module
names use the same approved grammar as snapshot preparation. Duplicate report
module names refuse. The reported private-module set must equal the complete
replay map; public modules must be its subset and contain all requested roots.
Set comparison, not array-order comparison, is appropriate here: the native
import census order need not equal the preparer's topological map serialization.

Artifact paths, hashes, copied parts and direct/effective flags are deliberately
not reauthenticated by this parser. The function documents that the replay bytes
must already be authenticated by the snapshot controller. Its membership checks
are not an alternative snapshot validator and do not establish map immutability.

## Counter and serialization compatibility

The two easy-to-confuse counters were checked independently:

1. `encoded_nodes` is the sum of serialized level-node and expression-node
   counts in each unit's descriptor and complete expected inventory. Python's
   planner obtains this from `inspect_unit`; Lean sums `descriptorNodes` plus
   every `inventoryNodes`. Both count type/value DAGs and recursor rule DAGs in
   the same places. Thus equality to `request.nodes` is warranted for the selected
   prepared units. Metadata names, `all` lists and byte-object lengths are not
   silently added on one side.
2. `unit_array_bytes` describes only the array of raw ordinary units, excluding
   request-entry wrappers, identity labels and output labels. Native starts at
   two bracket bytes and adds each compressed unit plus one comma after the
   first. Python computes `2 + (unit_count - 1) + sum(encoded_unit_lengths)`.
   Ordinary units contain fixed ASCII format strings, arrays, nonnegative integer
   values and single-key `$bytes` objects; arbitrary identifier/literal text is
   represented as bytes. Consequently the native compressed and existing Python
   canonical encodings have matching lengths for this selected grammar. The
   code does not assume equivalent lengths for arbitrary JSON objects/strings.

Private/public unit and name counts are derived from validated arrays and matched
exactly. Private plus public scan-node counts must respect the native aggregate
20,000,000 limit; scan-edge counts must respect the aggregate 262,144 limit.
The parser correctly does **not** require equality with `request.edges`:
that planner field counts external portable imports, whereas the native scan
also sees generated/internal references and selected implicit literal roots.
These quantities are not interchangeable.

Unsigned bounds reject booleans, negatives and out-of-range counts. The native
parser does not emit booleans for these counters; this matches the actual schema.
Fixed-basis comparison costs remain outside the native nonbasis scan counters,
as documented by the separate semantic audit. No parser check converts those
counters into total CPU or memory accounting.

## Authority boundary and remaining evidence

`BoundReferenceReport` is immutable convenience metadata plus preserved raw
bytes. It performs no native invocation, protected-store write or mathematical
admission. Expected SHA-256 supplies exact-byte binding, not evidence that the
selected native matcher actually ran. A successful shape parse may be obtained
from fabricated metadata; that does not prove correspondence, derive the public
closure independently or authorize local registration.

The future controller must keep the actual current owner/warrant state, exact
snapshot/support and request binding through a clean live native event, then
bind this parsed result to that event before any record-last protected commit.
Root should not use a helper accepting an arbitrary saved `BoundReferenceReport`
as a registration shortcut. These are explicit caller obligations, not missing
work that this narrow inert parser claims to perform.

The next finite evidence should cover an actual current native response and
cheap changed-field controls (wrong identity/target, truncated or reordered
whole unit, invalid erasure in either view, wrong module membership and the two
distinct count families). No broad old admission or producer campaign needs
repeating. This source review does not attest successful matching, registration,
ordinary delta reuse, growth benefit or final v5 readiness.
