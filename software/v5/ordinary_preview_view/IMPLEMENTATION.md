# Pure renderer source checkpoint

2026-10-28. Source-only implementation after root accepted CONTRACT/SPECIMEN.
No renderer import, execution, test, native worker, network or owner operation
has run in this assignment. Root owns wrapper/CLI and later finite selection.

API in `render.py`:

```python
render_preview(raw, *, codec, evidence, limits=None)
```

`raw` is one canonical preview's bytes; `codec` and `evidence` are the selected
`portable_preview` and `ordinary_evidence` modules supplied by root's pinned
loader. The renderer imports only `hashlib` from the standard library and calls
the selected `codec.read_preview` exactly once. Invalid input/limits raise.
No report fields select modules, paths, source execution, or resource renewal.

The returned detached dictionary contains `status`, `complete`, `view_text`,
`semantic_id`, `unit_id`, `export_id`, `preview_sha256`, `preview_bytes`,
`root_node`, `kind_code`, `limits`, `counters`, `limitation`,
`mathematical_acceptance:false` and the explicit advisory `assurance` string.
Status is `TYPE_DISPLAY_COMPLETE` or `TYPE_DISPLAY_INCOMPLETE`. The whole ASCII
view is present only on complete status; incomplete status has `view_text:null`,
including when a limit is hit while writing the legends. The wrapper adds report
hash/provenance and performs report/preview/record consistency checks separately.

The 12 exact limit keys/defaults are recorded in `DEFAULT_LIMITS`. Callers may
only lower known positive limits. `live_frames` counts peak outstanding frames;
all other counters accumulate charged work. `output_bytes` bounds the complete
ASCII view, not the wrapper's serialized metadata overhead. Metadata has a fixed
field set and fixed-size IDs plus bounded numeric counters; the wrapper owns its
own output-file ceiling.

Traversal uses an explicit frame stack and persistent linked binder environments.
Each scope walk is charged before advancing. Lambda/forall domains and let
type/value use the previous environment; only their bodies receive the fresh
binder occurrence. Repeated open DAG nodes are never memoized by node ID.
Application spines alone are flattened without changing scope or dropping actual
arguments; each traversed application and temporary argument slot is charged.
Levels expand independently under their own occurrence cap. Name/UTF-8 decoding,
escaping, binder allocation, frame pushes/pops and appends are bounded before work.

Exact-name keys for constants and projections are projected once from the
already validated input, avoiding repeated name-key serialization for every
expanded occurrence. Names use exact typed-component legends. Printed ASCII
hints do not identify anything. SymbolID terminology preserves the distinction
between ordinary exports and basis symbols. Nat literals print big-endian hex;
all string/non-ASCII name characters are losslessly ASCII-escaped.

The hand-derived specimen is a semantic/layout target, not a byte-exact expected
string: generated output includes generic kind code, may use additional grouping
parentheses and formats the complete legend as plain text. The control review
must check scope/reference/hypothesis preservation rather than compare every
whitespace byte or mirror traversal implementation.

No correctness or runtime pass is asserted. Independent source review and the
root-selected pure control scope remain outstanding.
