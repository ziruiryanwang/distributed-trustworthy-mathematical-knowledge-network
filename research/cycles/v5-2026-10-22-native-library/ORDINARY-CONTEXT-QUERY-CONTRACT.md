# Query binding from an explicit local context

2026-10-23, `usable_v5_next`. Source-only contract selected by root after
ORDINARY-USER-PATH-AUDIT.md (`f3c66b8f...`). No product source, runtime, owner
state, index, package or Git change is selected by this document. Implementation
and changed-boundary tests require root's separate selection.

## Scope and compatibility

Author one fresh `software/v5/ordinary_query_context/query.py`, derived from
`ordinary_query_package/query.py` (`886bdfd6...`). Preserve the current explicit
manual-binding path. Add an optional context-binding path using the existing
package loader and owner lifecycle. The pure resolver lives in this same file;
no bundled helper or profile-loader allowlist change is needed.

Do not modify `owner.py`, `profile.py`, `formal_query.py`, any admission/catalog/
custody/checking code, any query key/schema, or any native helper. A later file-only
successor replaces only the package's `query.py` and its hash/size in PROFILE.
The PROFILE hash changes; the native installation and local-anchor support ID
remain identical. `module_export.support_descriptor` selects owner/loader and
checking/import dependencies, but not query.py. Full profile verification remains
mandatory; this is not permission to ignore the replaced payload.

## CLI

Common required arguments stay unchanged:

```text
--profile-sha256 --python-runtime --lean-runtime --native-type --output
--wall-seconds --cpu-seconds --memory-mib
```

Require exactly one of:

```text
--bindings <existing canonical JSON file>                 # existing manual mode
--context-root <exact 64-lowercase-hex local root>         # new context mode
```

Context mode additionally requires all four existing owner selections:

```text
--catalog <existing absolute directory>
--custody <existing absolute directory>
--store-id <exact 64-lowercase-hex local ID>
--custody-limits <existing absolute JSON file>
```

Manual mode must omit all four. Reject both/no mode, incomplete context tuples,
or manual plus context arguments before any owner opening/output creation.
Use argparse's required mutually exclusive group for the two modes and a bounded
explicit tuple validation for the companion options. Keep `allow_abbrev=False`.
There is no `create`, initialization, automatic root selection, provider, native
source, project-import or certificate option.

Preserve valid manual-mode CLI behavior, query/spec bytes and existing output/result
fields. Do not gratuitously rename or reformat that interface. Invalid argument
combinations can fail through argparse without the normal JSON report, as current
argument errors do; runtime failures still emit one structured JSON report.

## Existing API to reuse exactly

After the ordinary query bootstrap and `loader.load(...)`, obtain
`A=loaded.A`, `O=loaded.O`, `Q=loaded.formal_query` and `installation`.
Retain the existing shared-module checks for Q/E/S and the discovery adapter.

Before state opening:

1. Parse and bound native type bytes with existing Q routines. Normalize/validate
   the output as fresh and paths as ordinary absolute files/directories using
   A.C helpers. Validate root and store IDs with `A.C.hexid`.
2. Read custody limits at most 65536 bytes using `A._writer_json`. Apply
   `A.P.fields(..., O.STORE_LIMITS, ...)` and every existing `A.P.uint` bound.
3. Read `<catalog>/ADOPTION.json` at most 65536 bytes with the existing strict
   evidence JSON reader. Require exact fields `schema,store_id,implementation,limits`,
   `schema == A.P.SCHEMA`, selected StoreID, and exact
   `installation.doc["implementation"]`. Construct `A.P.Limits(**marker["limits"])`.
   Do not substitute defaults, adjust quotas, infer compatibility or migrate.
4. Apply existing `base.separated` to output, catalog, custody, package and both
   selected runtime roots. Native-type and custody-limits files may not lie in
   the fresh output. For context mode also require those two external input files
   outside catalog/custody, so owner lifecycle recovery cannot change selected
   query inputs. Do not broaden manual-mode path rules in this successor.

Then, in one original operation allowance:

```python
custody = O.OrdinaryStore(custody_path, installation.semantic_id,
                          custody_limits, create=False)
owner = A.OrdinaryAdmission.open(installation, catalog_path, store_id,
                                custody, create=False, limits=limits)
context = owner.catalog.context(context_root)
```

This is the actual API, not a callback accepting a JSON manifest as authority.
`OrdinaryAdmission.open` obtains the real catalog lock through PortableCatalog;
`context` validates the selected lineage, exact bindings and retained artifacts.
Require returned `local_root`, semantic/foundation/implementation IDs to match
the explicit selection. No alternative direct SQL path or fake custody object.
The query implementation must not call owner.initialize/preflight/admit,
catalog reserve/commit, custody put/get, Lean, network or anchor-store APIs.

The existing reopen operation can settle abandoned RESERVED operations as
INTERRUPTED, and SQLite open performs ordinary recovery/configuration. Therefore
this mode makes **no new mathematical acceptance**, but is not a strictly
non-mutating database read. Do not assert that all state bytes remain identical.

## Small pure resolver

Define a local function, for example:

```text
resolve_context_bindings(Q, native_type_bytes, context_bindings, check)
    -> (canonical_binding_bytes, empty_missing_names)
     | (None, exact_missing_names)
```

`Q` is the already selected module, not an executable or module name from input.
`context_bindings` is the actual dictionary obtained above; pure tests may supply
an explicitly inert dictionary and must not count that as owner authority.

Use Q.reference_names in its original order. For each name n:

- compute the existing exact encoded key using Q.E.name_key;
- if key is absent, append n to the missing list;
- otherwise validate the exact bound ID and append `[n, ID]` to the rows;
- call the original allocation check during traversal.

Do not iterate/copy the whole K binding map, resolve printed spellings, invent
IDs, accept prefixes, normalize the names differently, or return partial usable
bindings when anything is missing. A present malformed ID is a context-binding
error, not an absent name. Bound canonical binding bytes to the same 1 MiB as
the current manual input. Missing names retain their bounded structured form,
not an unbounded pretty-print trace. Emit all missing names in one response;
do not fetch or auto-retry one dependency at a time.

When complete, call unchanged Q.bind_native_type and Q.query_spec and existing
adapter compilation. The generated binding rows obey the exact same census/order
contract as manual rows. Allow types with zero constant references: `[]` is a
valid complete binding list if the existing native-query validator permits it.

Let K be the selected binding map. READY establishes only that every referenced
name is mapped by rho(n)=K[n], and the query is formed in that interpretation.
It does not establish that a same-named declaration in the producer's unrelated
Lean project has the same meaning. It is not a theorem, proof, typechecking event,
global absence result or a transferable warrant. Neither human intention nor a
new equivalence checker belongs in this boundary.

## Closing, outputs and failure semantics

Keep the owner lock while resolving and constructing the query and while doing
the existing final input/profile integrity checks. Then close owner followed by
custody in a finally path, attempting both even after the first failure. Track
objects only after successful constructor returns; existing constructors already
close their own partial opening on failure. All close errors make the operation
unsuccessful and remain in its structured report; no output may claim success
before known closure. No native process exists to recover or certify here.

Context mode does not create its fresh output directory until input resolution,
query construction, final validation and clean resource closure have succeeded.
Recheck the original allowance after closure, before writes. Unknown references
return `ok:false`, status `UNMAPPED_REFERENCES`, phase `RESOLVE_CONTEXT`, exact
`missing_names`, selected context identifiers and `mathematical_acceptance:false`;
leave the output absent. Bad adoption/lock/context/support/capacity failures
likewise create no usable query output. Preserve their actual error category.

Successful context output contains:

```text
BINDINGS.json    mechanically resolved exact canonical rows
QUERY.json      unchanged query schema
SPECS.json      unchanged existing search specs
RESULT.json     terminal context-mode result, published last
```

The result retains the existing query success fields and adds `binding_mode:
"selected-local-context"` plus `context_selection` containing `store_id`,
`context_root`, `semantic_id`, `foundation_id`, `implementation_id` and
`reference_count`. `bindings_sha256` is already an existing result field and now
binds the generated BINDINGS file. Include an explicit interpretation label
`SELECTED_RECEIVER_CONTEXT_NOT_PROJECT_EQUIVALENCE`. Do not put the entire
owner map or artifact plan in the result. Worker/native CPU stays exactly zero.

Use fresh non-overwriting file writes. For this context mode only, form the
complete success RESULT bytes after closure and write/fsync a fresh pending file;
then publish by non-overwriting same-volume rename to RESULT.json after its final
allowance check. This is a local completion marker, not mathematical commitment
or power-loss durability guarantee. If earlier writes fail, retain partial files
and report failure with output path; never delete or overwrite them. If publication
may have happened before a later reporting failure, retain that ambiguity and the
exact result-file hash; do not retry, revoke or relabel it. Consumers treat raw
QUERY/SPECS without a complete matching terminal result as incomplete operation
output, even though those bytes are inert search data. Preserve manual-mode
publication behavior rather than smuggling unrelated output redesign into it.

## Costs and minimum evidence

Use the existing query limits: 1 MiB native/bindings inputs, bounded Q codec,
4096 type references, 65536 type nodes, existing caller time/CPU/memory ranges.
Apply one original deadline and controller CPU ledger to bootstrap, state opening,
context checks, mapping, closing and writing. Existing catalog/context methods do
not accept fine-grained budget callbacks: check before/after, document cooperative
limits, and use the existing outer Job for hard process containment. Do not claim
hard controller memory/disk limits or introduce hidden renewal.

Mapping itself visits only query references and their encoded bytes. Full owner
opening/context validation can still reconstruct K and hash retained artifacts;
include those costs. No native proof replay, proof acquisition, catalog growth or
anchor registration follows from the query. Query-only package replacement should
be checked against the exact descriptor inputs to establish unchanged anchor
support identity by source/pin comparison, not by repeating a native anchor test.

Minimal focused checks after source review: manual behavior preserved; mode tuple
rejection before owner opening; all-found order/IDs; all-missing/no partial output;
malformed map value; no-constant query; selected-context identity mismatch;
owner and custody closure on exceptions; close failure suppresses success; fresh
output commit/failure retention. Guards can make any native, custody data transfer,
admission or network call fail. One root-selected real-owner call using retained
query bytes can validate actual exact mapping and zero native work; no new Lean
compile, discovery lease, theorem, basis build or reciprocal campaign is needed.

This exposes a missing supported user operation. It does not settle general
approved-project extraction, usefulness against conventional package sharing,
large-context costs, mathematical search completeness or final-v5 release.
