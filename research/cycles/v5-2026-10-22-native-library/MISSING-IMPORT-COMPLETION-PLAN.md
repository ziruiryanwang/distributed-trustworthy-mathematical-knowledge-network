# Bounded completion of genuinely missing local-library imports

2026-10-23. `successor_export`. Root-selected source design and new native CLI;
no build, native execution, catalog mutation, Git action or old-artifact edit.

## Decision and practical alternatives

Consumer05 now exported five complete new units, with 37 claimed imports and
eight unresolved names (103,060 bundle bytes). The protected-parent inspection
found seven unresolved names already accepted, and `List.map_congr_left` absent.
This is an actual proof-acquisition seam, not another name-correspondence error.

Use one native private import of the trusted installed library and export the
complete missing closure, stopping on demand at the receiver's accepted names.
Keep the exact original candidate bundle and all five raw units unchanged.

| Route | Decision |
|---|---|
| Rewrite the consumer or patch one lemma name | Reject: avoids the general real-use problem and changes the test. |
| Send the whole accepted parent name map to the owner | Avoid: unnecessary map transfer and poor large-context interface. |
| Export all standard-library proof ancestry from scratch | Reject: repeats already accepted work and loses the useful stopping boundary. |
| Re-elaborate consumer/source commands with broad private imports | Avoid: repeats successful proof construction and reintroduces authoring-environment pressure. |
| Repeated one-unit processes or file-polling rounds | Avoid: repeated library loading or avoidable orchestration state. |
| One native environment plus synchronous bounded parent lookup | Selected: reuses the successful native importer and current selective scheduler. |

No new network service, peer native artifact loading, certificate production or
global index is required. This initial source is the owner's **trusted installed
Std closure**; it is not a solution for arbitrary missing peer proofs.

## Implemented source and narrow build reuse

New file: `software/v5/ordinary_lean/MissingImportExporter.lean`, SHA-256
`7efb8bfa768a97ebcced687fd2a5acb0227e65eb2260e82d1726d8f361b27fbb`.
It imports only `OrdinaryExport` as compiled helper code and later loads exactly
one declaration environment. The current scheduler is SHA-256
`1d4df6817098f5ad9cd0106d98f39a6905a55be8b23484294b5c3d22653a7d4f`.

Root's build should generate a **header-only legacy view** of that scheduler:
remove its exact initial `module` marker and `public section`; change its initial
`public import` lines to `import`; preserve and hash-compare all body bytes.
Compile this view and the new CLI against the retained old four lower `.olean`
files, then link their existing four `.o` files plus the two new objects. Do not
mix current public `.olean` signatures with unrelated old objects, mutate the
old build, or rebuild the lower helpers/Lean/Std merely for this new entry point.
Modern modules cannot directly import those legacy `.olean` files, which is why
the explicit source view is needed.

Retained directory:
`experiments/v5-local-checks/ordinary-native-export-build-01/native-build`.
Its original selection SHA is
`ac56b4084629a357a85223c3115bb6988a40b3733f417d51353a0dc7630fde6f`.

| Retained file | SHA-256 |
|---|---|
| `OriginalExpr.olean` | `435d330a5c3bac37aa7b9bfcdd0a548fc3af0593bf53b6a10645e7cc5001eafd` |
| `OriginalExpr.o` | `354c0d29e3a98c42d12123f18dbe6c23880e4f7d0d92d9cf5359d31720083fcb` |
| `OriginalDecl.olean` | `565821e2a3bbbdd9fd8f912ec69985e3906806cee7c358d9420f6c553f3b82da` |
| `OriginalDecl.o` | `41e7aabd1e80967a05eb4f4e996513ae7aabfd00cc0415afb5a96eff3f3c580f` |
| `CheckedExtension.olean` | `9b34b26e6ab1560390b0f8a8ddc32fd5c21107df4e84b6be828cfcbe87372298` |
| `CheckedExtension.o` | `9ca258256d302c5d636e54b4c217ff1b5c03dfa095f6c5cf71ab244e1fefc66c` |
| `BootstrapSupport.olean` | `e6cf0c191da107ac9cef526e393b598e41bfd7470a8a3cf063a70dcc4d39f63a` |
| `BootstrapSupport.o` | `bee6a91e6d15a5eb9e9baa0026796e83b72bab7ec38ca424d77a75f8ea00b3fc` |

These hashes are identity observations, not new build or compatibility results.
The finite two-module compile/link remains a separate root-selected gate.

## Exact CLI and request

```text
MissingImportExporter.exe <absolute-sysroot> <absolute-request.json> <fresh-output.json>
```

Request has exactly six fields:

```text
schema = DMKN_ORDINARY_MISSING_IMPORT_REQUEST_V1
profile_id, context_id, basis_id = exact 64-hex labels
modules = nonempty array of encoded original module names, at most 16
targets = nonempty distinct array of encoded original missing names, at most 1024
```

Modules must have the `Std` name prefix and are controller-selected, not peer
paths. For this concrete workload select `Std.Data.ExtHashMap.Lemmas`, whose
already used installed closure contains the required List lemma; do not load
umbrella `Std` merely for convenience. `searchPathRef` is set to the pinned
`sysroot/lib/lean` only. `importModules` uses `.private`, no plugins and
`loadExts := false`. Target records must exist, be safe, and carry a complete
nonaxiom declaration. A target that the parent reports accepted is refused,
preventing accidental repeated accepted extraction.

The request is bounded to 1 MiB before parsing. Exact canonical/file identity,
selected runtime/library artifacts, ordinary path ownership, alias checks and
immutable inputs are controller duties. This helper does not authenticate labels.

## Exact synchronous pipe protocol

Only JSON-line frames go to stdout. Diagnostics go to stderr. All names below
are the existing encoded original names, not dotted-name approximations.

```text
LOOKUP:
 {schema: DMKN_ORDINARY_PARENT_LOOKUP_V1, seq: n, name: N}

FOUND response:
 {schema: DMKN_ORDINARY_PARENT_REPLY_V1, seq: n, name: N,
  status: FOUND, symbol_id: ID}

ABSENT response:
 {schema: DMKN_ORDINARY_PARENT_REPLY_V1, seq: n, name: N,
  status: ABSENT}

DONE:
 {schema: DMKN_ORDINARY_MISSING_IMPORT_DONE_V1,
  lookups: count, units: count, output_bytes: count}
```

Sequence begins at zero. Only one query is outstanding; exact schema, field set,
sequence and name echo must match. FOUND requires a valid 64-hex ID; ABSENT must
not contain one. The protected Python controller answers from the same eligible
parent K, retains its exact transcript and rechecks those bindings before any
admission. There is no network callback and no peer-selected resolver.

Each frame has at most 1,048,576 payload bytes plus its LF terminator. Total
sent/received protocol bytes, including terminators and DONE, are at most
33,554,432. At most 65,536 distinct lookups are sent. Both positive and negative
answers are memoized; target preflight and scheduler lookup share that cache.
The scheduler also bounds distinct probes and positive stops at 65,536.

Reply reading uses one-byte bounded reads, not unbounded `getLine`, and applies
depth/integer/token/UTF-8 checks before JSON parsing. EOF before a reply, CR
terminators, malformed frames, wrong replies or exceeded bounds refuse. The
parent supplies an aggregate nonrenewing process deadline; native waiting does
not create a new allowance.

After writing and flushing the bundle, the helper sends DONE and waits for
stdin EOF. The controller closes stdin on DONE and requires clean child exit;
any trailing response byte refuses. DONE or a leftover output file alone is
not success. Failure artifacts remain inert and must not trigger automatic replay.

## Selective complete closure and output

The scheduler starts with no injected full parent map. Its dynamic predicate
queries exact names: FOUND stops traversal; ABSENT requires the complete local
unit and its dependencies. Raw refs and normalized group-owner edges both use
the same rule. Actual raw reached refs alone populate the output boundary map;
generated group straddles remain refused. Unaccepted axioms refuse; already
accepted theorem proof bodies are not scanned or emitted.

Root-selected default extraction limits preserve the current checker scale:
1,024 new units, 2,097,152 scan nodes, 64 MiB unit/bundle ceiling, and existing
per-unit/name/edge/group caps. A genuinely new generated group may invoke the
existing bounded group census. Otherwise lookups are pointwise. The controller
must additionally check combined supplemental-plus-consumer limits; two separate
passing byte caps cannot authorize an oversized merged batch.

Bundle exact fields:

```text
schema = DMKN_ORDINARY_MISSING_IMPORT_BUNDLE_V1
assurance = INERT_OWNER_EXPORT_NOT_MATHEMATICAL_ACCEPTANCE
profile_id, context_id, basis_id
targets, boundary_imports, units, stats
```

`boundary_imports` contains `[originalName, exactFoundID]` only for reached raw
refs. `units` contains complete absent declarations in dependency order.
`stats` has exactly:

```text
source_records_enumerated, selected_units, dependency_edges, scan_nodes,
unit_json_bytes, boundary_imports, lookup_count
```

The output is bounded and `.writeNew`; it cannot overwrite the candidate or
request. Root authenticates local output and canonicalizes evidence later.

## Combined-admission invariant

The supplemental units are still **candidates**, not a newly accepted K.

1. Resolve the original candidate's claimed IDs against prepared bindings and K,
   and its unresolved names against K. The supplement targets must equal exactly
   the genuinely missing set, not merely contain the known example lemma.
2. Resolve supplement boundary claims independently against K and the actual
   lookup transcript. They need not belong to the old prepared authoring map.
3. Derive supplemental envelopes and provisional output IDs in dependency order.
   Reject overlap with K or original new outputs, duplicate output names and
   forward/unbound references. Do not write those provisional IDs into K.
4. Derive envelopes for the **unchanged five original raw units**, resolving
   missing imports through those earlier supplemental outputs. Original claimed
   IDs remain prepared-and-K-bound. Preserve original candidate bytes/hash.
5. Under one aggregate grant, submit the ordered supplemental-plus-original
   batch to the unchanged actual receiver. Only a clean full check, exact report
   and artifact binding, and real commit can accept either part. No successful
   prefix promotion on failure; no new receiver axiom rule.

The extraction process exits before receiver checking starts, avoiding two live
Lean library environments. Ordinary local discovery/construction is not repeated.
If extraction reveals a truly unavailable/unsupported dependency, report it as
the next exact acquisition issue; do not substitute a proofless axiom or increase
resource limits automatically.

## Assurance and remaining evidence

Final soundness still depends on independently checking complete new units in
the real accepted K. The trusted local library and its source lookup only supply
candidate proof data. No equality between local authoring and receiver meanings
is assumed; a mismatch may cause final refusal. Protocol/cache correctness
affects bounded extraction and compatibility, never supplies a mathematical
warrant by itself.

Independent reviewer `admission_event_audit` read the new CLI and reported no
blocking source finding; root owns adoption and finite runtime selection. Native
build, actual extracted closure and combined receiver admission remain separate
evidence. This work does not claim worldwide proof availability, search
completeness or final v5 delivery.
