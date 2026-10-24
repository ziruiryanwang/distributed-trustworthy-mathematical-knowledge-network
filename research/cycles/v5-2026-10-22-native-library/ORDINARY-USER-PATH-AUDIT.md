# Practical user-path audit after local module anchors

2026-10-23, `usable_v5_next`. Independent source/theory audit. Canonical guard
passed. No product changes, imports, tests, native calls, owner openings, network
operations or Git mutations were performed. Current anchor integration belongs
to other owners and is not predeclared successful here.

## Decision: remove the identity-handwork barrier before another mechanism

**The highest-payoff next user-facing deliverable is a supported query-preparation
operation that resolves the query's referenced symbols from an explicitly selected
local mathematical context.** A user should supply a formal type and the context
whose mathematics they mean, not reverse-engineer hashes and canonical name arrays
from experiment scripts. Keep the existing explicit-binding API as an advanced,
pure interface; add a small adapter, not a new search engine or package manager.

This is a practical priority judgment, not a measured proof that it dominates
every alternative. The current system has separate public query, search,
receive, contribute, publish and module-export operations. The immediately
blocking *public discovery input* remains manual identity plumbing. Local module
anchors address repeated export work but do not repair this input.

The user has no existing project to provide. Do not invent real-user demand or
call another supplied elementary theorem a usefulness benchmark. A documented,
callable operation is nevertheless a real product improvement: it replaces an
unsupported manual procedure for all already-supported contexts without needing
a new corpus or certificate campaign.

## Evidence from current sources, not historical README claims

| Current source | Observed behavior | User consequence |
|---|---|---|
| `ordinary_query_package/query.py`, arguments and run | Requires `--native-type` and `--bindings`; loads supplied binding bytes and passes them unchanged to the query compiler. | Even an owner with the relevant mathematics already accepted must separately manufacture the binding input. |
| `ordinary_formal_query/formal_query.py`, `reference_names`, `_bindings`, `bind_native_type` | Computes the exact reference order and requires one `[structured Lean name, portable symbol ID]` row for each reference; guesses are not made. | The necessary resolver seam already exists; no new mathematical key or AST normalization is needed. |
| `ordinary_module_anchor_package/owner.py`, `status` | Returns roots and selected-context counts, not a referenced-name binding view. | Existing CLI status does not provide the missing query input. |
| `ordinary_module_anchor/module_export.py` | Already obtains the protected selected context and looks up exact name keys in `context["bindings"]`. | Reuse the same selected-context interpretation; do not introduce another source of mathematical identity. |
| `ordinary_extractor_binding/library_extraction.py`, `selected_modules` | Requires every supplied module name to begin with `Std`; selection is bounded to 16 modules. | Arbitrary approved third-party project dependencies cannot be completed by this operation. |
| `ordinary_lean/MissingImportExporter.lean`, lines 170–177 | Independently requires the `Std` namespace and sets the search path to the selected runtime only. | Removing a Python restriction would not supply general project ingestion, and silently changing the native boundary would be unsafe. |

The earlier peer README describes an older fail-fast search boundary. Do not use
that historical paragraph as evidence that current provider-failure handling is
absent. Likewise the original build README describes a predecessor; current
navigation selects build03/query assembly. This audit uses the current mapped
sources above for its concrete claims.

## Minimum useful contract

Proposed user operation, with final CLI spelling left to root:

```text
prepare-query(native_type, explicit_owner_context, existing_package_configuration,
              original_finite_budget)
    -> READY(query, specs, resolved_bindings, source_context_root)
     | UNMAPPED_REFERENCES(exact_names, source_context_root)
     | explicit support/context/budget failure
```

1. Validate the existing owner/package/runtime selection using established code.
   Select one explicit root, never a guessed latest branch. Open owner state only
   through the existing lock/lifecycle boundary. Opening can settle abandoned
   reservations; do not advertise this mode as a strictly read-only database call.
2. Parse the bounded query with existing `reference_names`. For each returned name
   `n`, use precisely `context.bindings[name_key(n)]`. Preserve the established
   reference order; produce the binding JSON mechanically. Do not search by printed
   name, hash the spelling into an ID, fetch evidence, run extraction, build a
   project, or accept a provider's identity assertion as this local binding.
3. Report every missing name together before producing a READY query. Unknown
   vocabulary is an explicit next decision; it is not an excuse to traverse proof
   ancestry merely to ask a query. Existing manual-binding mode remains useful
   for a caller who intentionally formulates a query in another known vocabulary.
4. Call unchanged `bind_native_type` and `query_spec`; emit the resolved map,
   semantic namespace, source context, query and specs with their exact identities.
   There is no theorem UnitID, proof, accepted flag or catalog mutation by the query
   logic. Do not register a module or infer that a searched theorem exists.
5. The next search, candidate selection and receipt remain explicit existing
   operations. Do not combine them with automatic source execution or an unbounded
   retrying agent. A convenience configuration may reduce repeated flags later;
   it must not become a second state/authority system.

The symbolic meaning is deliberately narrow. Let `refs(T)` be the names in the
query and `K` the chosen owner binding map. READY requires
`refs(T) ⊆ dom(K)` and builds `rho(n)=K(n)` for those references. The output means
the existing syntactic query in **K's interpretation**. It does not prove that a
same-named declaration in an unrelated compiled project has that interpretation,
nor that the query is solvable. This is not a new issue created by the adapter:
the current manually supplied bindings have the same limitation. The emitted map
must make the interpretation inspectable instead of concealing it behind a name.

After the owner context is available, mapping costs O(number of query references)
dictionary operations plus encoded bytes; the current owner can still pay O(K)
context reconstruction and artifact validation first. Include those costs. A
cached binding view could be a later optimization, but is not necessary to expose
this missing operation, and must not be introduced as authority by copying JSON.

## Smallest decision-changing validation

First review the adapter against the mapping invariant above. Reuse existing
passed query extraction, exact-key, discovery and module-consumer evidence; no
new end-to-end timing campaign is justified for unchanged downstream operations.

Focused pure controls can use the already saved native type and an explicitly
inert context map to check order, exact identities, all-missing reporting, malformed
references and no output on incomplete mapping. One minimal real-owner call, if
root selects it, should show that the current stored context supplies those exact
bindings without native work or a new mathematical acceptance. This validates the
new public seam, not real-user benefit or broad semantic search.

## Ranking the other central obstacles

1. **Self-service formal query preparation (above):** small changed boundary,
   supported workflow, immediate removal of hand-constructed internal data.
   Do this before increasing query complexity or optimizing anchor lifetimes.
2. **General approved-local-library completion:** the most serious remaining
   ecosystem-coverage restriction. A normal project may elaborate using external
   proof-bearing modules, yet the public completion path is installed-Std-only.
   The existing library-ingest decision already identifies the right mechanism;
   do not rediscover or duplicate it. The next step is a source-level contract for
   explicit approved artifact roots/closure, fixed foundation precedence, complete
   private proof records, finite missing-proof extraction and unchanged independent
   admission. It should reuse retained candidate output, not reauthor it. No
   automatic Lake fetch/build or trusting arbitrary peer `.olean` files. Select a
   compatible narrow project before runtime; a whole mathlib load is not the first
   experiment. This can follow the cheap query bridge or proceed as theory in
   parallel, but does not require a speculative new verifier.
3. **Deployment and sustained utility:** license, supported platforms, honest
   independent hosting/security review, retention/service operation and a justified
   nontrivial workload remain release obligations. More local peers or a larger
   toy library do not settle them. Do not call the current package final v5 merely
   because its component loop works.

This ordering is not a recommendation to polish documentation instead of solving
the ecosystem restriction. Finish one small missing public operation, then move
the engineering frontier to general approved-project ingestion; do not accumulate
more aliases, binding-view formats or onboarding frameworks.

## Comparison with ordinary Lean/Lake sharing

For collaborators who already approve a package and use most of its vocabulary,
normal pinned imports can be the better route. They preserve tactics, attributes,
notation and project integration without the commons' extra encoding and admission
steps. Let that route use the same formal index and query preparation. The commons
need not win against its own useful delivery mode.

The prospective distinct value of inert delivery is selective unknown-provider
acquisition with independent checking, reusable local warrants and redundant
custody. The comparison is therefore between alternative implementations of a
shared discovery/reuse service, at explicitly comparable trust endpoints. A
no-download selected-context query is useful in either implementation.

Removing manual identity work establishes operability, not positive CPU growth.
For useful sharing retain the existing full-history condition:

```text
sum (cost_of_allowed_local_alternative - full_cost_of_sharing)
  > incremental_creation + publication + indexing + custody + failed_attempts.
```

No proof-search lower bound follows from the difficulty of a theorem chosen by
us. Normal library sharing is an allowed alternative, local caches/generalization
must be equal, and producer effort is not zero merely because a consumer benefits.
The implementation should make these routes usable before running another
experiment aimed at declaring that this inequality holds.

## Inspected source hashes

| Source under `software/v5/` | SHA-256 |
|---|---|
| `ordinary_query_package/query.py` | `886bdfd61dbc613411379b5c298fb61492feeae1215beabc783d4d5537110d57` |
| `ordinary_formal_query/formal_query.py` | `7901236768784a399f9ae5c56b374d040bce56536b0a47a6ee85093440cabcee` |
| `ordinary_module_anchor_package/owner.py` | `a17f7905f479929bf55f3ddbe8f857de9d48e528a132e4c27f2a000d1adb028d` |
| `ordinary_extractor_binding/library_extraction.py` | `28ff83c5a8561b9f5250e9be08b34744aedd23757765feb174e1504d700308aa` |
| `ordinary_lean/MissingImportExporter.lean` | `7efb8bfa768a97ebcced687fd2a5acb0227e65eb2260e82d1726d8f361b27fbb` |
| `ordinary_project_return/ordinary_contribution.py` | `09394f523417406aefcad0b47d06fa2d7782940bec3bb5094975f08b68f94ca8` |

Prior work reused: ORDINARY-EXISTING-PROJECT-DECISION, ORDINARY-LIBRARY-INGEST-
DECISION, ORDINARY-PROVED-LIBRARY-EXPORT-DECISION, ORDINARY-PROJECT-RETURN,
ORDINARY-NEXT-BENEFIT-DECISION and the current query/distribution/module-anchor
documentation. Those older implementation-gap statements are historical where
later source implements them; this note does not reopen completed work.
