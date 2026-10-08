# Native diagnostic API: no certificate authority

The selected evolving source is `checker/src/bin/module_preflight.rs`. Root
owns source snapshots, compilation and supervised launches. Invoke the built
binary with one immutable JSON input path. It reads at most 32 MiB, emits one
JSON result to stdout, and writes no result file or database itself. Native
parser/checker diagnostics may appear on stderr. Actual CPU, memory and process
tree limits belong to the root-selected supervisor.

Every mode reports `mathematical_admission: false` and performs no receipt
verification. The diagnostic tool is not a public admission API.

## Common input

The exact top-level schema is:

```json
{
  "schema": "DMKN_V5_NATIVE_PREFLIGHT_V1",
  "mode": "all_new",
  "rows": [],
  "permitted_axioms": []
}
```

`rows` must be a nonempty native row array including export metadata; the empty
array above is only a field-layout illustration. All names/rows must use the
selected Nanoda export format. No arbitrary config, file output path, unsafe
axiom allowance, nat/string extension or parallel checker is enabled.

`all_new` parses the same input rows and calls `check_all_declars`. It forbids
module/foundation/premise/correspondence inputs. Success is exactly
`ALL_DECLARATIONS_CHECKED_UNDER_EXPLICIT_AXIOMS`: every declaration was checked
under the disclosed allowlist, not independently adopted foundation authority,
Lean-kernel correspondence or a portable certificate.

## Conditional module checking

`conditional_module` additionally requires lowercase 64-hex `module` and
`foundation`, and a `premises` array. Each premise has exact `authority` and
`names` fields; names are numeric indices in this input's native name DAG.

Foundation authority shape:

```json
{"kind":"foundation","foundation":"<64 lowercase hex>"}
```

Imported module authority shape:

```json
{"kind":"module","module":"<64 lowercase hex>","group":"<64 lowercase hex>",
 "journal":"<64 lowercase hex>","receipt":"<64 lowercase hex>"}
```

Those are **alleged premises**, not verified authority. The native checker
checks every local declaration/group and skips only the explicit imported
records, subject to its role/namespace/cutoff checks. This mode deliberately
does not claim canonical descriptor correspondence.

## Same-input correspondence plus native checking

`corresponding_module` requires all conditional inputs and `correspondence`:

```json
{
  "foundation_rows": 1,
  "groups": [
    {"owner":"<ModuleSpecID>","imported":false,"descriptor":"<actual group object>"}
  ],
  "bodies": [
    {"universes":0,"digest":"<body hash>","expression":"<actual codec AST>"}
  ]
}
```

Placeholders are not valid input values. `foundation_rows` is the exact prefix
row count including metadata; it does not prove that prefix is the adopted
foundation. Groups are in native group order. Declarations inside an atomic
group are matched by structured qualified name, so descriptor order need not
coincide with native type/constructor/recursor order. Bodies are deduplicated by
universe arity and claimed digest. Imported missing definitions need no body
opening until demanded; full imported recursor-rule bodies are currently eager.

The Rust matcher independently reconstructs relative-reference ASTs and checks
kind, type, universes, hints, full raw group metadata and present value/rule
expressions. It forbids foundation declarations under reserved root `_nested`
and `DMKN.Mod` namespaces. Matching uses an indexed name map, not quadratic
per-descriptor group scans. All proof/value expansion has a 250,000-node work
ceiling. The exact same rows then enter the native parser and checker. Supplied
premise names must agree exactly with matched foundation/imported roles; a
matched local descriptor cannot be reclassified as imported.

Remaining obligations are explicit: body hash equations, group/spec/opening
hashes, exact foundation binding, certificate journals/receipts, rank descent,
and the relation's own pinned identity. The matcher emits only
`STRUCTURAL_CORRESPONDENCE_ONLY_UNVERIFIED_HASHES_AND_PREMISES`. A future guest
must discharge those equations itself and execute the completed relation; it
must not consume host success flags.

## Results and bounds

- `CONDITIONAL_MODULE_EXTENSION_ONLY`: all local checks passed under the stated
  unresolved premises. Not mathematical admission.
- `NEED`: exact `NeedDeclaration` or `NeedBody` with native name index and,
  for bodies, committed digest. The controller must resolve structured names,
  fetch authenticated immutable data, and reconstruct a new invocation.
- `REFUSED`: malformed input, structural mismatch or non-demand checker panic.
  Refusal exits 2. `NEED` currently exits 0; callers **must inspect `status`**,
  not infer success from an OS exit code. Parser fatal errors may also terminate
  without JSON; absence of a complete expected result is never success.

The JSON parser's default nesting ceiling (128) is currently narrower than the
pure codec's 192 AST-depth allowance. Deeper requests may refuse safely. Do not
claim the full codec depth envelope for this CLI; expanding it requires a
bounded parser/stack design and targeted controls, not disabling safety blindly.
