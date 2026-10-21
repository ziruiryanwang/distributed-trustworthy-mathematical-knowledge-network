# Optional whole-type pattern discovery

This fresh source overlay adds a candidate-search key for a complete formal
declared type, ignoring only the addresses of nonfoundation constants. It is
not a standalone installation. Root must select these files in a coherent SDK
before using the examples. No installed state is migrated by this overlay.

The existing exact-type key answers "this exact type over these exact symbols."
The new pattern key answers "this whole type shape over consistently renamed
nonfoundation symbols." It retains positions, repeated-symbol identity, binders,
universe syntax, projection indices and exact foundation symbols. For example,
involution `forall x : T, f (f x) = x` is different from idempotence
`forall x : T, f (f x) = f x`, even though their old edge/symbol sets coincide.

## Make a query without knowing a remote module ID

In an SDK assembled with this overlay on its ordinary Python module path, the
following self-contained snippet constructs a closed codec type template and
its query keys. It performs no network call, proof checking or workspace write.
This is canonical formal AST input, not a Lean-source elaboration service.

```python
from aggregate_claims import bindings as B
from modules import codec as C
from discovery.module_export_adapter import ModuleExportAdapter, PATTERN_PROFILE_SCHEMA
from discovery.type_pattern import pattern_spec

def name(text):
    return [["s", text]]

def local(text):
    return ["const", ["local", name(text)], []]

def app(fn, arg):
    return ["app", fn, arg]

# A local template label, not a target/supplier identity or an admitted module.
local_owner = "11" * 32
T, f, x = local("T"), local("f"), ["bvar", 0]
# Eq.{1} on T : Type; foundation names and universe arguments stay exact.
eq = ["const", ["foundation", name("Eq")], [["succ", ["zero"]]]]
law = ["forall", "default", T, app(app(app(eq, T), app(f, app(f, x))), x)]
profile = {"schema": PATTERN_PROFILE_SCHEMA}
adapter = ModuleExportAdapter(C, B.FOUNDATION, B.POLICY, discovery_profile=profile)
specs = [
    {"tag": "declaration-kind", "value": "theorem"},
    pattern_spec(C, local_owner, 0, law),
]
print(specs)
print(adapter.compile_query(specs))
```

Pass `specs` to the existing ordinary client's `find` on a pattern-profile
workspace. The query can find a candidate using different T/f addresses. No
remote module ID, theorem name or candidate descriptor was used to form it.
The template does not prove that T/f exist with the suggested semantics. A
received result does not prove that its f computes the caller's desired function.
Inspect the exact candidate, acquire its needed semantics, and use ordinary
mathematical admission. Reuse its exact vocabulary or independently prove a
transport; a matching pattern is never a transport theorem or trust warrant.

`pattern_spec(codec, owner_module_id, universes, type_expr)` counts a local
reference and an external reference to that same owner/name as one symbol.
Use a consistent owner for actual local/external aliases. Nonfoundation slots
are assigned by first occurrence; both constants and projection names share
the table. Foundation names, universe parameter positions/arity, binder flags
and all remaining syntax are preserved. SHA-256 equality assumes no collision.

## Explicit workspace opt-in

A fresh configuration has the existing evidence-workspace fields plus exactly:

```python
"schema": "DMKN_V5_CLIENT_EVIDENCE_TYPE_PATTERN_WORKSPACE_V1",
"discovery_profile": {"schema": "DMKN_MODULE_EXPORT_TYPE_PATTERN_PROFILE_V1"}
```

Set these fields on a complete, owner-selected fresh configuration; they do not
replace its wire, storage, operation or trust settings. `Workspace.open` checks
the fixed profile before creating directories, locks, ledgers or indexes.
Its immutable persisted config binds the chosen profile on later reopening.
The base schema still accepts no profile; the conjunction schema still accepts
only its explicit pair profile. Pattern mode does not combine with pair mode,
and pattern query tags are refused in either older mode. No implicit upgrade,
old-workspace rewrite, namespace reuse or cross-profile record acceptance occurs.

## Bounds, costs and strict limits

The helper bounds occurrence-expanded input before whole-input serialization,
then applies the unchanged codec syntax/scope checks. Shared subtrees count
each occurrence; cycles or excessive depth/work/bytes are refused. Malformed
input, feature exhaustion or oversize types are explicit failures, not silently
omitted keys. It neither fetches definitions nor evaluates terms.

Each new-profile record adds one pattern feature to ordinary atomic features.
The different namespace requires reindexing and new snapshots. If an operator
serves old and new profiles simultaneously, ALL inherited postings can be
duplicated, not merely the new pattern posting. Rebuild, holding, updating and
failed-search costs matter. This does not require mathematical recertification.

This is whole-type variant retrieval, not general discrimination/substitution
matching. It misses specialization, reordered binders, definitional equality,
different universe expressions and equivalent formulations. Popular schemas
can still occupy enormous buckets. Existing query budgets/coverage outcomes
remain; there is no universal selectivity, complete worldwide search, automatic
applicability or useful-growth guarantee. Keep exact-symbol search for acquired
vocabularies. This feature is worthwhile only where its filtering saves enough
work to justify its separate profile and index costs.
