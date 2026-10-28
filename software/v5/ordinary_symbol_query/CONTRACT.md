# Symbol-neighborhood queries from a checked local context

Status: source-ready successor for independent review. No execution, package
adoption, index change, mathematical admission or usefulness result is claimed.
The predecessor `ordinary_query_context/query.py` remains byte-identical at
SHA-256 `449b5fea77f4c19cfbde47346ea255ae1277a1cf53e3030a6baa9de3f8659af6`.
Root owns launcher/package selection and actual operations; the companion
operator kit and independent review have separate owners in this directory.

## Purpose and scope

An agent may know which definitions it is investigating before it has a closed
theorem statement to search for. It can request declarations whose types mention
those definitions, using the existing index's exact `type-symbol` features. This
removes the need to run Lean just to construct that search input. It does not
claim that mention implies usefulness, that every useful result mentions the
chosen symbols, or that the query finds an unknown equivalent definition.

The new entry is a successor to the current query entry. It reuses the selected
owner, evidence codec, formal query helper, discovery adapter and package loader.
There is no new feature revision, namespace formula, wire protocol or authority.
Existing manual and contextual exact-type modes remain available.

## Public inputs

Supply exactly one of `--native-type PATH` and `--symbol-names PATH`.
The first retains the current native-type JSON format and either manual
`--bindings` or a selected `--context-root`. Symbol queries require the contextual
mode: `--context-root`, `--catalog`, `--custody`, `--store-id` and
`--custody-limits`. Supplying `--bindings` with symbol names is refused.
All current profile/runtime, finite allowance and fresh output arguments remain.

The symbol file is canonical JSON containing a list of **one through eight exact
structured Lean names**, no more than 65,536 bytes. Each name is validated by the
existing `E.name_key(name, Q.DEFAULT_LIMITS.codec)` with semantic-name checks.
Names must be unique under that exact key. The codec rejects noncanonical JSON,
unsupported components, invalid UTF-8, forbidden semantic names and malformed
numeric tags. Names are validated before opening owner/custody state.

For example, the complete canonical input for the single name `Eq` is:

```json
[[[0,{"$bytes":[69,113]}]]]
```

This is the original-name encoding, not Lean source syntax. There is no alias,
open-namespace, notation or fuzzy-name resolution. Tag-0 UTF-8 components and
tag-1 numeric components remain distinct. The operator kit can convert a
separately documented restricted dotted-name convenience form into these exact
bytes; this entry performs no such conversion. The file has no trailing newline.

## Resolution and output contract

Let `R` be the explicitly selected checked local root and `B_R` its original-name
to portable-symbol map. Let `N = [n_1, ..., n_k]` be the requested distinct names.
The operation succeeds only if every `key(n_i)` belongs to `dom(B_R)`. It resolves
names exclusively through `context["bindings"]` for `R`; it never looks at another
root, a global name registry, an imported project, an index or a peer.

If all names resolve, the ordered specification list is:

```text
specs[i] = {tag: "type-symbol",
            symbol: {kind: "portable-symbol", symbol_id: B_R[key(n_i)]}}
```

`namespace` and `features` come from the existing adapter's `namespace_for` and
`compile_query`. Features are a conjunction, not a union or ranking. Existing
feature deduplication may collapse repeated portable identities, but no requested
name is silently omitted; all names are present in the binding rows and specs.

If any name is absent, the report has `ok:false`, `status:UNMAPPED_REFERENCES`
and all missing structured names. It has no specs/features and creates no query
output directory. A mapped subset never becomes a weaker ready query. Malformed
selected symbol identities, an invalid context identity or exceeded bounds also
refuse without a ready marker. There is no automatic fetch, admission or retry.

On success, contextual symbol mode writes, in order:

1. `BINDINGS.json`: canonical `[name, portable-symbol-id]` rows in request order.
2. `SYMBOL-NAMES.json`: exact canonical selected input bytes.
3. `SPECS.json`: the existing ordered feature specifications.
4. `RESULT.json`: the final success marker, published by a fresh rename after
   writing `.RESULT.pending`.

The success report has `operation:prepare-symbol-query`,
`query_kind:symbol-neighborhood`, `binding_mode:selected-local-context`,
`mathematical_acceptance:false`, the specs/namespace/features, `names_sha256`,
`bindings_sha256`, and exact `profile_sha256`. Its `context_selection` includes
semantic, foundation and implementation identities, store ID, selected root and
reference count. `input_pins` includes the name bytes and custody-limit hashes.
There is no invented exact-type `query_sha256`, `native_type_sha256` or
`key_profile`. Exact-type success keeps those existing fields and gains
`query_kind:exact-type`; its previous output filenames are unchanged.

## State, closure and failure boundary

The entry uses the current owner/custody lifecycle with `create=False` and its
exclusive-lock discipline. It checks selected root, semantic, foundation and
implementation identities. Opening may recover abandoned reservations, so this
is not a promise of database-read-only access. It submits no admission request,
starts no native worker and writes no index or network state.

Captured input bytes and package profile are rechecked before closing the owner,
then custody. Success output is attempted only after both closes succeed.
Contextual reports record `owner_closure` and `custody_closure` explicitly.
If closure fails, there is no success output. If final output creation/write or
rename fails, partial bytes remain and the returned failure records publication
state and the attempted result hash when available. Only a valid final success
report is consumable as ready. Existing uncertain-rename semantics are preserved;
this change is not a new crash-transaction protocol.

The selected package, Python/OS, immutable local storage and prior checking
assumptions remain. A report hash selects bytes; it is not an independent
authentication or mathematical proof. Equal name spellings in different local
roots do not imply equal portable identities. Conversely, the query operates on
portable identities deliberately shared under the existing checked mapping.

## What is justified

Conditional on the current owner's checked-context invariant, success establishes
that every emitted type-symbol feature uses the exact identity associated with
its requested name in `R`. The argument is finite projection: validate all names,
perform exact key lookup in that single map, validate every selected identity,
abort on any missing key, then apply the unchanged feature compiler.

It establishes **search-input fidelity**, not a new theorem. Provider records
remain candidate hints; acquisition and independent mathematical checking are
still required before use. Neither correctness of the name projection nor a
complete answer within one finite index proves worldwide coverage, mathematical
equivalence, novelty, usefulness or faster discovery. Those remain separate
questions for the larger architecture and workload.

## Cost and practical limit

For `k <= 8` and input size `b <= 65536`, incremental name parsing, projection and
feature preparation cost `O(b + k)` plus codec and hashing constants. There is no
type elaboration or native checking in this operation. This bound describes the
new work, **not** the entire cold operation.

End-to-end work also includes selected package/runtime checks, owner opening and
recovery, `catalog.context(R)`, closures and fresh output. The current context API
walks `R`'s selected lineage, validates its retained snapshot bytes and constructs
its binding map. Thus whole cost depends on that local lineage, metadata and
retained bytes; it is not constant-time lookup in an arbitrarily large local
context. It does not traverse a global network or require a global corpus. No new
sparse-context storage layer is selected here merely to improve this seam.

The inherited finite wall/CPU/memory settings and enclosing whole-operation Job
remain required. The inner report excludes the final marker write; the outer
launcher accounts for whole-operation completion. This source work makes no
measured performance claim. Root may select a small changed-boundary control and
one real contextual query after independent review, without repeating the prior
native/theory campaign.
