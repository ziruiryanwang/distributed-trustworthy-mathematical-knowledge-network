# Evidence reader and local snapshot: focused source review

2026-10-22. `lean_workflow_trace`. Source-only independent review; no tests,
runtime, source edits or Git changes. Read both files completely, their author
notes and the relevant retained Lean module-loader/serializer APIs.

**No new soundness blocker found within the stated internal-controller
preconditions.** These are useful integration components, not a complete public
acceptance path. One API repair already selected by root remains to be reviewed:
return the actual checked environment alongside the saved chunk, so same-process
A→B does not require duplicate checking or a needless restore.

**Subsequent narrow delta review:** the selected repair is now read and resolved.
`WrittenExtension` pairs `SavedChunk` with the actual `checked.environment`;
`checkAndWriteChunk` returns those values directly after the same private writer.
No new caller-created CheckedBatch input or altered checking/writer path was
introduced. Reviewed LocalSnapshot SHA-256:
`488a76f4b8599a95bdc748c5e89187bc55e23f63d34cf52952702d93ff68795c`.
This permits warm continuation without establishing catalog promotion or runtime
success. The original version hash below records the first review, not the
currently selected API.

## Evidence identity and census

`ordinary_evidence.py` bounds raw bytes/depth and unsigned numeric tokens before
`json.loads`, rejects duplicate fields and noncanonical encodings, and derives
domain-separated identities from exact canonical raw bytes. Original-name keys
avoid dotted-name ambiguity; profile, unit and exact sorted external bindings
are included. Unrelated local catalog roots are not identity inputs.

The reference census includes descriptor and expected-inventory expression DAGs,
projection names and recursor RHS. It subtracts claimed generated names, which
is safe only because those names remain claims: the mandatory Lean decode and
actual generated-output comparison must precede authority or index promotion.
The scanner is not a substitute for either. Orphan/duplicate DAG nodes are
explicitly left to the Lean canonical decode/re-encode gate.

**Controller action:** bind the actual imported symbol IDs to warranted local
bindings and send the same validated raw unit to Lean. `Evidence.document` is
mutable despite the frozen dataclass; mutation followed by use of the old
`unit_id` must not be allowed to change the accepted profile/imports/unit.
Use the retained raw bytes or independently re-establish their exact binding.

## Snapshot trust and delta correctness

The private writer receives the exact `checkBatch` return and serializes only
`checked.added`. It does not trust expected records, dump cumulative stage2 or
turn imported theorems into axioms. Empty extension entries and IR selection,
one explicit parent, exact names and the protected artifact plan match the
intended small local persistence seam.

Restoration builds the complete finite map, empties fallback search paths,
disables plugins/extensions, and checks loaded module/import/count metadata.
The upstream loader otherwise falls back to module search, so the empty search
path is a useful safeguard. It cannot replace pre-load authentication.

**Controller actions before public integration:** authenticate every selected
artifact digest/profile/lineage before unsafe deserialization; keep paths and
bytes stable; bind the actual parent environment to its recorded module; check
withdrawal/grants; and promote only after clean exit and durable catalog commit.
`quotInit=true`, matching file size or matching module count supplies none of
these warrants. The post-write artifact-size check is not a disk-output cap;
reserve/bound staging capacity in the owner. Failed writes remain unaccepted.

## Whole-workflow cost boundary

The evidence scanner works over the submitted bounded envelope, not the global
corpus. A local snapshot restore, however, hashes/loads the **whole selected
one-parent local chain, including stored theorem values**. It avoids kernel
proof replay; it is not proof-ancestry-byte-free cold acceptance. As a local
library grows, a fresh restore per tiny unit would impose avoidable repeated
loading. Use the selected in-memory environment return for batches/fresh grants,
and keep the chosen local closure bounded; do not advertise this seam as the
strict succinct-certificate lane. Initial useful workflows should measure their
actual selected closure, not global network size or only the new delta.

## Reviewed versions

| Source | SHA-256 |
|---|---|
| `ordinary_evidence.py` | `fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6` |
| `LocalSnapshot.lean` before selected environment-return repair | `bc0f305734ee36268c5e4e65e84c5db4e71fa9d1c9a3089e84bc447959dcdfc2` |

Proceed with the small selected API repair and focused round-trip/reader checks,
then the protected controller and ordinary-project reuse integration. Do not
repeat completed core controls or infer final-v5 readiness from this review.
