# Correlation adapter: selected source implementation

2026-10-26 America/Chicago. Author: `pattern_retrieval_options`.
Source only; no product import, compilation, test, native process, state opening,
network call or Git mutation. Independent review and root's separate execution
selection remain required. The full v5 goal is unfinished.

## Exact predecessor and successor

The only product file authored here is `ordinary_export_adapter.py`, installed
later, if selected, as logical `discovery/ordinary_export_adapter.py`.
The predecessor remains unchanged:

- `software/v5/ordinary_formal_query/discovery/ordinary_export_adapter.py`, SHA-256
  `3ddbed2156a393b08543a5da88c89b5c5b9c2b4f65689c46fbd7623cec38db0a`.
- New source: **14,384 bytes**, SHA-256
  `8720f6dd4b0aa7df2e7110ffdac56cace55b8128690b5e66615ea497aea546b3`.

The source was created with `apply_patch` at the absolute canonical path. No
installed or evidence-bound file was edited. All changes are confined to the
CONTRACT.md's correlation metadata/query boundary.

## Retained behavior

All prior object/declaration-kind, exact type-key, type-symbol, result-head and
binder-domain-head validations and extraction remain. The memoized spine walk,
bounded preview parse, exact type-key parse, complete binding census, locator
reconstruction, exact ExportID binding, record rederivation, 1–8 conjunct rule,
and 128-feature cap remain in force. Return fields for `describe` and `resolve`
are unchanged. No mathematical admission or export identity changes.

Every record uses a fresh namespace because the feature revision is now
`kind-symbol-memoized-spine-head-exact-type-correlation-v3` and the namespace
includes `conclusion_correlation_profile`. This applies even when a caller uses
only an old query feature. Old snapshots are refused, not migrated. Ordinary
feature semantics are retained, not old namespace/feature hashes.

## New profile and feature

Public `CORRELATION_PROFILE_ID` is
`57c1341c34762c46b7f2dd9bc83b0d144906cf1fb8d48518a20d95b84c0c1eec`.
This expected digest was computed read-only from canonical source-profile JSON,
not by importing/executing product code. A focused test must independently check it.

The profile commits to:

- schema `DMKN_ORDINARY_CONCLUSION_CORRELATION_PROFILE_V1`;
- paths `[["arg","fn","arg"],["fn","arg","fn","arg"]]` in canonical order;
- source rule `theorem-terminal-same-stripped-parameter-coarsenings`;
- query rule `one-exact-endpoint-partition-distinct-missing`;
- the existing exact type-key profile, currently
  `09fceff93c77a65852e6509db9badfb3330d20737aea5297bd031f8b8845a953`.

Profile hash domain is `DMKN-ORDINARY-CONCLUSION-CORRELATION-PROFILE-V1`;
the new feature uses `DMKN-ORDINARY-CONCLUSION-CORRELATION-FEATURE-V1`.
Old feature kinds retain their prior feature domain under the new namespace.

The only new accepted feature shape is:

```text
{tag: "conclusion-correlation", profile_id: CORRELATION_PROFILE_ID,
 value: "equal" | "separate"}
```

The fixed profile and value require actual strings and exact values. Unknown or
extra fields remain refused. These are possible **query** endpoint partitions,
not asserted equalities of source parameters or mathematical inequalities.

## Source extraction

The existing leading-forall loop now also counts its parameters; it is not
repeated. Only kind-2 theorem previews obtain correlation features. The two
paths follow application edges only and never enter a binder. They return an
endpoint only when the entire path exists. Early parameters or other rigid
missing edges return absence.

Both complete endpoints must be bvars with the same index in the stripped
parameter range to impose equality. Such a source gets only `equal`. Every
other theorem gets both `equal` and `separate`. Non-theorem records get neither.
All keys use the same existing capped `add` helper. If either required key would
overflow capacity, the entire description fails; no partial record escapes and
no required posting is silently omitted.

Existing `describe.work` gains the actual at-most-nine endpoint-position visits
and the one/two new feature-add operations. Telescope visits are already charged.
The count is structural work, not whole parsing, CPU, index-service or storage cost.

## Public query helper

```python
correlation_query_spec(query_raw, *, context_binders, limits=Q.DEFAULT_LIMITS)
```

This returns exactly one feature specification, not a list, OR query, report,
proof or accounting token. It first validates trusted limits and the explicit
integer context count, then reparses the complete raw existing formal-query
document through `Q.read_query`. It strips exactly that many leading foralls.
An incomplete context prefix refuses; remaining goal quantifiers are not stripped.

If either selected endpoint is missing, output is `separate`. Missing positions
are not equated with one shared sentinel. Otherwise call the unchanged
`Q._structural_key` twice, once for each endpoint root. Each call receives a fresh
shallow packet `[schema, original_levels, original_nodes, endpoint]`; it does not
mutate the original packet or tables. The complete original wrapper has already
passed scope/reachability/binding validation. No fabricated standalone closed
subquery is passed to the validator. The private helper only keys the already
validated syntax, retaining all DAG tables and exact known portable bindings.

The key compares full endpoint syntax independently of DAG sharing/numbering,
with the existing display-label quotient and exact remaining fields/universes.
It performs no reduction. A hash collision can add a false-positive `equal`,
not mathematical authority. Any actual keying failure propagates; there is no
exception-to-`separate` fallback.

For N total level/expression nodes, two complete endpoints cause **2N key-node
visits**, plus validation, bindings and context/path handling. Even equal node
indices take the two passes to preserve one simple implementation boundary.
The pure spec helper does not return a cost ledger; this explicit structural
account is not a fabricated runtime measurement. Peak auxiliary key tables are
O(N), and both full pass costs remain charged by enclosing runtime supervision.
No proof, dependency ancestry, native environment or provider is consulted.

New diagnostic codes:

- `ORDINARY_CORRELATION_PROFILE`: wrong/nonstring profile identity.
- `ORDINARY_CORRELATION_VALUE`: value other than actual string equal/separate.
- `ORDINARY_CORRELATION_CONTEXT_COUNT`: bool, noninteger, negative or count above
  selected `limits.codec.max_dag_depth`.
- `ORDINARY_CORRELATION_CONTEXT_TELESCOPE`: requested prefix exceeds available
  leading foralls.

Existing strict query/preview errors and `ORDINARY_FEATURE_PROFILE_EXHAUSTED`
remain unchanged. Integration and independent test authors have the exact helper
signature/profile/refusal codes; no test-specific bypass was added.

## Assurance and payoff boundary

The raw-instance coverage proof is in
`research/cycles/v5-2026-10-26-local-discovery/CORRELATION-TRANSPOSE-THEORY.md`.
A repeated source parameter at both depth-zero endpoints becomes the same query
term; an unconstrained source includes both possible query features. Exact
retrieval still depends on providers, complete indexing and budgets. Correct
application/typing/hypotheses require unchanged mathematical checks.

An `equal` query matches every indexed theorem on this feature alone. A
`separate` query only excludes the selected repeated-parameter class. Neither
outcome proves applicability, mathematical inequality, global absence or useful
growth. New postings/reindexing/maintenance and query-key work must pay for
themselves against exact generalization, existing selective queries and approved
Lean/Loogle alternatives. No performance result is claimed by this source note.
