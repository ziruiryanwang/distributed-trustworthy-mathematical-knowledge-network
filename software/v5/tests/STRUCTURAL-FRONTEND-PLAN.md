# D17: exact foundation and owned-row frontend

Source-only until the root selects each finite build/run. No mathematical
acceptance, VM completion, proof, or performance result is asserted here.

## Selected boundary and justification

The relation currently pays two SHA passes over the same fixed 23,313-byte
foundation serialization, then deserializes owned rows through two outer Serde
flatten Content buffers. The selected combined repair changes neither the
foundation, semantic policy, ModuleIDs, journal profile2, nor JSON wire format.

`foundation_static.rs` compares the actual first 413 Value rows to a compiled
immutable tree, checking every node, scalar, key, array length and object length.
Its sorted-object iteration relies on pinned serde_json without preserve_order.
The relation still passes these SAME actual rows to correspondence and native
construction/checking. No caller digest, side cache or supplied validity flag
replaces a check. Exact comparison implies the former two hash checks; the
reverse implication relies on the former hash-binding assumption. SHA collision
inputs formerly admitted are not a compatibility obligation.

`decode_corresponded_owned_row` recognizes only an object with zero/one lowercase
`in`, `il`, `ie` index, representable u32 if present, plus exactly one enum variant.
It moves/removes the index and uses the EXISTING `ExportJsonVal` deserializer.
All other outer shapes delegate to unchanged `decode_owned_row`; the general
text parser, `apply_row`, duplicate/backreference guards, correspondence and
kernel remain unchanged. This matters for unused mdata/nat/string expressions,
positional payload arrays, ignored fields such as `all`, and BackRef aliases.
The only original-row type change is derived Debug/PartialEq/Eq for comparison.

## Compiled foundation provenance

Source: `experiments/v5-local-checks/receipt-prepare-01/prepared/base/receipt-input.json`
SHA256 `025d2ce3c42cf7eeab00d1e6626d22d59afe495c64232ad2687893eea278d4a8`.
Its first 413 rows serialize to 23,313 canonical UTF8 bytes with SHA256
`736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c`, FoundationID
`d931d114155cf3cf0dc0b868aa88c6d38b8ada8ecafe267a5934934075782481`.
The stdout-only renderer independently reproduces the exact 83,565-byte
`foundation_data.rs`, SHA256
`ed450bccfc23fa613bb0c8a8bd3c9ba67ab8477c1d59bf5c1eb5c11cf05423ab`.
The build includes both generated data and comparator in its exact source map;
runtime reconstruction must reproduce the canonical foundation hash as well.

## One focused harness, no kernel repeats

`structural_frontend_differential.rs` compiles the current checker as a module
with crate-root module reexports and existing macro exports, using retained
eight dependency rlibs. No native-library/backend rebuild is needed. Both old
and new decoder calls use the same original enum; their successful decoded
objects must be equal, or both must refuse. Original `decode_owned_row` and
enum source are independently compared to the prior guest04 snapshot.

The five saved profile2 diagnostic inputs from `existential-differential-run-01`
are reused, not rechecked mathematically. All their rows compare old/new;
every first-413-row foundation matches the compiled tree. A reconstructed
compiled tree must equal the held Value and canonical bytes. 421 foundation
mutation controls cover every row, short/long prefixes, extra/changed metadata,
and scalar substitutions. Twelve extra accepted rows cover unused expression
variants, positional payloads, ignored `all`/other fields and uppercase aliases.
Twenty-one irregular inputs compare success/refusal boundaries; acceptance by
both decoders is not native admission and some may later fail `apply_row`.

Build: one link, 180 Job CPU seconds, 300 total wall seconds, 4096 MiB,
8 active processes, 6 GiB combined reserved working bound; reviewed retained
owner Job and exact owned-telemetry cleanup. Runtime proposal: 30 Job CPU,
60 wall, 768 MiB, 3 active processes, 1 MiB each output; exact binary/fixture/
source pins and create-new evidence. No retry or cap increase is authorized.

After independent actual adoption, root may select ONE new guest05 image
including both changes, then one base snapshot under unchanged 2^25 ceiling.
Host03 source and receipt/journal protocol do not change and should be reused
after exact binding confirmation. Stable ModuleIDs do NOT permit cross-image
parent recursion. A complete retained capsule precedes any segment calibration.
This is an incremental cost repair, not a solution to expanded semantic trees;
the compact typed-DAG architectural obligation remains open.
