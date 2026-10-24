# Ordinary formal query: source contract

2026-10-23; `practical_growth_next`. Source/theory only. Root selected this
narrow feasibility task after `ORDINARY-NEXT-BENEFIT-DECISION.md`; no native
build, runtime, index write, owner operation, network or Git mutation is selected.

## Feasibility and comparison

**No blocking theory issue was found.** The existing `OriginalExpr.lean`
serializer already accepts `(ordered universe names, Lean.Expr)` directly.
It neither requires a declaration nor reads theorem proofs. A new owner-local
command can follow Lean 4.34's own `#check` boundary:
`withoutModifyingEnv`, `runTermElabM`, term/type elaboration, metavariable
resolution and `Meta.check`. Close used section variables with
`Meta.mkForallFVars`; then call `ExprCodec.encode` on this type alone.
There is no need for `OrdinaryExport.indexSource`, a theorem unit, scratch axiom,
accepted catalog entry, new kernel rule, proof production or dependency closure.

Ordinary `#check` already elaborates and displays a local expression/type. A
Loogle-style search service may already solve the user's discovery need. This
seam is **not a claim of better theorem search**: it adds a small machine-readable
portable type/query boundary to our replaceable indexes. Give ordinary package
sharing the identical query facility. If an available ordinary search service
already provides the relevant results more cheaply, use it rather than claiming
that an extra custom index is necessary. No external service was queried here.

## Smallest supported owner API

Proposed local syntax:

```lean
import OwnerQueryCommand
universe u
variable {A : Type u} (f : A -> A)
#ordinary_type_query [u] "ABSOLUTE_FRESH_OUTPUT.json" :
  forall x, f (f x) = f x
```

The command emits only `[query-AST-schema, ordered-universe-names, type-DAG]`.
It generalizes the section variables actually needed by the type, preserving
their binder annotations and dependency order. Extra local variables do not
silently become extra premises. Explicit `[u, v, ...]` is the query's ordered
universe list, not a theorem identifier. Unresolved metavariables, unclosed
variables, `sorry`, undeclared universe parameters and oversize output refuse.
The command uses the existing environment without importing another environment;
its direct operation adds no declaration. Owner-approved macros/elaborators can
execute ordinary code: this is not a peer-source sandbox.

A pure Python helper then:

1. Reads the bounded query AST and lists its exact referenced constant names.
2. Accepts the caller's **already known** exact name-to-portable-SymbolID map.
   The map must match the type's complete sorted reference census; absent,
   duplicate or extra entries refuse. It does not guess IDs from spelling.
3. Emits a separate canonical query document containing semantic ID, universe
   list, type DAG and bindings, with no theorem name, UnitID or accepted status.
4. Derives one `declared-type-key` feature for the existing `find` protocol.

Foundation mappings can come from the already selected fixed basis inventory;
acquired-symbol mappings can come from the owner's existing correspondence or
previously retained module/preview bindings. Merely importing a locally named
Std/package symbol does **not** reveal its content-derived portable identity.
If that identity is unknown, this first exact-vocabulary mode refuses. Do not
reconstruct ancestry to ask a query, implicitly accept a provider's mapping, or
pretend a name-only match has established semantics. Caller-supplied mappings
are search inputs, not warrants; a mistaken map may miss or mis-rank candidates
but cannot authorize their mathematical use.

No network API is added. The pure helper's spec is submitted to existing
`peer_api.find` in a separately selected new-profile assembly, with its usual
provider/partition/candidate/byte/request budgets. This is initially a source
SDK seam, not yet an installed public command or deployment qualification.

## Exact matching semantics and implementation invariants

Use the decision note's bottom-up DAG hash. Ignore binder labels and universe
parameter labels but preserve ordered universe positions/arity, constant
SymbolIDs and level instances, binder annotations, let flags, literal values,
projection fields and all expression tags. Node numbering/sharing are absent
from the hash. A different parameter order or hypothesis order need not match.
There is no substitution engine, unfolding, normalization by reduction,
definitional-equality promise or new path-fingerprint engine.

Reuse `ordinary_preview._type_census` for closed, bounded, reachable type syntax
and `ordinary_evidence.strict_json` for pre-parser byte/depth/numeric checks.
The internal census function's declaration-kind slot is only a syntactic helper
argument; no theorem preview or accepted record is manufactured from a query.
The new type key is calculated identically from the ordinary V2 candidate
preview and the separate query document. It is a search hint, never acceptance.
Candidate evidence binding, local symbol matching and native acceptance stay
unchanged.

The new adapter is a fresh source successor, not an edit to the used adapter.
It retains the existing record shape and ordinary locator binding while changing
the explicit feature revision/profile namespace and adding one required key.
The generic index, posting, pagination, transport and acquisition algorithms are
reused. A coherent assembly selects this adapter and helper together. Old
snapshots/configurations are not silently migrated or reinterpreted: indexing
the new profile requires a fresh namespace and charged reindexing/storage.

For bounded fields, key computation is linear in supplied level/expression
nodes and referenced-name/field bytes. No tree expansion, proof/body traversal
or global-environment scan occurs. Elaboration/type conversion has ordinary
Lean's separate cost: finite process limits remain necessary and no polynomial
elaboration claim follows. Common exact-type buckets can still be huge.

## Minimal fresh source selection

Prepare only these under `software/v5/ordinary_formal_query/`:

- `OwnerQueryCommand.lean`: read-only type elaboration and existing-codec output.
- `formal_query.py`: bounded query envelope/binding/key helpers.
- `discovery/ordinary_export_adapter.py`: fresh adapter successor, reusing the
  current adapter and adding the exact key/profile revision only.
- `README.md`: API, required source assembly, limitations and adoption gates.

Do not add a new database, controller, daemon, proof representation, matching
engine or certificate. Root owns later packaging/profile integration and exact
build/runtime selection. No existing used source or evidence is modified.

## Review and smallest later discriminator

Before any build, independently inspect the changed API/namespace and actual
Lean API usage against the pinned source. Later, if selected, test one natural
independently specified contract with local binders; alpha-renamed/shared DAGs
must match and structurally different contracts must not. Include an unknown
symbol refusal, malformed/open/oversize input refusal and a preview/query
agreement check. Only then consider one actual discovery/use check. It must not
take a returned theorem's type as its supposedly independent input.

Stop/redirect if exact contract formulation is unnatural, normal search already
resolves the need, unknown symbol mappings require ancestry reconstruction, or
the ordinary comparator has no plausible saved work. Successful compatibility
still does not instantiate the existing full-cost benefit inequality. No timing
campaign, repeated body-search example or certificate production is justified
by this source contract.

## Fresh source readiness

The four listed files are now prepared, without execution or changes to used
sources. The adapter is a fresh copy of the current ordinary adapter with only
the new helper dependency, stricter-limit preflight, exact-type spec validation,
new feature revision/profile namespace and type-key extraction added. The pure
helper exposes `reference_names`, `bind_native_type`, `query_spec` and the same
`preview_key` computation used by the adapter. No runtime launcher was added.

Concrete API references read from the pinned Lean 4.34 distribution:
`Lean/Elab/BuiltinCommand.lean:433` (`#check` without environment mutation),
`Lean/Elab/Command.lean:980` (section-variable `runTermElabM`),
`Lean/Elab/Term/TermElabM.lean:1952` (`elabType`), and
`Lean/Meta/Basic.lean:1174` (`mkForallFVars`). These establish source plausibility,
not a successful compilation. The next independent source review should focus
on those exact calls, the new namespace and query/preview key identity; a build
and finite controls still require root's separate selection.
