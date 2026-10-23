# Original Lean declaration unit v1

Source-only candidate in `OriginalDecl.lean`, namespace
`OrdinaryLean.DeclCodec`. It consumes the metadata-preserving `ExprCodec`.
It never imports modules, adds declarations or inserts peer ConstantInfo.

```text
DecodedUnit { decl : Lean.Declaration, expected : Array Json }
decodeUnit (allowed : Std.HashSet Lean.Name) (packet : Json) (limits := {})
  : IO DecodedUnit
encodeUnit (decl : Lean.Declaration) (inventory : Array Lean.ConstantInfo)
           (limits := {}) : IO Json
inventoryRow (actual : Lean.ConstantInfo) (limits := {}) : IO Json
expectedNames (expected : Array Json) (limits := {}) : IO (Array Lean.Name)
```

`allowed` means names available from the caller's grounded parent/earlier
checked batch units. Passing that set is not itself a proof of grounding.
The caller must bind its exact environment, checker, basis and policy.

## Envelope and descriptors

```text
["DMKN_LEAN_ORDINARY_UNIT_V1", descriptor, expectedInventory]

descriptor :=
  [0, name, levelParams, typeDag, valueDag, hint, all]  safe definition
  [1, name, levelParams, typeDag, valueDag, all]        theorem
  [2, name, levelParams, typeDag, valueDag, all]        safe opaque
  [3, levelParams, numParams, types]                  safe inductive group

hint := [0] | [1] | [2, UInt32]   opaque / abbrev / regular
types := [[typeName, typeDag,
           [[constructorName, constructorTypeDag], ...]], ...]
```

Name fields use `ExprCodec` components, not dotted strings. `levelParams` retains
the exact original ordered names; expression DAG parameter indices resolve
under that list. `all` retains original order and names, with no duplicate and
with the declaration's own name included. It is nonlogical block metadata,
not permission to use an unprovided declaration or evidence that every member
is present. Definition hint kinds/heights are exact; no `withHeight` replacement.

No axiom, quotient-initialization or unsafe/partial mutual-definition tag
exists. Safety flags in accepted constructors are fixed to safe/false. Safe
mutual definitions elaborate to ordinary lowered declarations and dependency
units. An extension cannot overwrite a name already in the supplied parent.

All group type/constructor names are fresh and pairwise distinct. During
decoding of group types and constructor types, the name allowlist is extended
only by this group's type names, not arbitrary advertised inventory names,
constructors or recursors. The actual kernel's inductive constructor still
checks positivity, group typing and generated computation rules. This codec
does not independently establish those properties.

## Actual inventory projection

Every row is `[name, kind, originalLevelParams, typeDag, details]`.
Expressions erase only mdata. Details retain:

| Kind | Details |
|---|---|
| 1 definition | `[valueDag, hint, all]` |
| 2 theorem | `[valueDag, all]` |
| 3 opaque | `[valueDag, unsafeFlag, all]` |
| 4 inductive | `[numParams,numIndices,all,ctors,numNested,isRec,isUnsafe,isReflexive]` |
| 5 constructor | `[induct,cidx,numParams,numFields,isUnsafe]` |
| 6 recursor | `[all,numParams,numIndices,numMotives,numMinors,rules,k,isUnsafe]` |

Each recursor rule is `[constructorName,nfields,rhsDag]`; flags are 0 or 1,
and unsafe flags must be false. No axiom or quotient inventory row is accepted
in an extension. Counts/heights are UInt32, including those projected from
actual native records. Lists and rules have finite caller-supplied limits.

The supplied inventory is only a **claim**. The decoder validates its header,
kind-specific shape, numeric/name/list bounds and aggregate DAG-node counts;
it does not construct ConstantInfo from the claim. Detailed expression
canonicality/meaning in that claim is enforced by equality to the projection
of actual kernel-generated outputs in the next layer.

Expected names are nonempty, distinct and fresh. An ordinary declaration has
exactly one expected name matching itself. A group must include all declared
type and constructor names. Its actual recursors/nested auxiliaries and full
generated census must be established by the checked-extension adapter; extra
advertised names do not become available premises merely by appearing here.
The inventory order is bound by packet bytes, but the acceptance controller
must compare name sets and each actual named row rather than assume a global
hash-map iteration order.

## Bounds and acceptance responsibilities

`DeclCodec.Limits` contains `expr : ExprCodec.Limits` plus defaults of 4,096
group types, 65,536 constructors, 65,536 inventory rows, 65,536 `all`/group
names and 2,097,152 **total level-plus-expression nodes** across descriptor
DAGs and all expected-inventory DAGs. Repeated DAGs are charged repeatedly
because they occur repeatedly in the input. Preflight totals run before
descriptor expression construction. Expected inventory expressions remain
inert claims pending comparison with actual output.

These bounds do not replace an outer serialized-byte/parser-depth/CPU/memory
budget. In particular, the outer reader should allow only the format's needed
nonnegative decimal integer tokens and refuse exponents/fractions/negative
numbers **before** `Json.parse`; a short hostile huge-exponent token can make
Lean's general JSON parser allocate heavily before this codec gets control.
No raw network parser is implemented by these files.

The next layer must invoke checked kernel insertion, screen actual references
under its axiom/evaluation policy, compare the complete actual generated name
census and `inventoryRow` values, and commit only the resulting accepted state.
Successful descriptor decoding or producer encoding confers no mathematical
acceptance. Unknown parameter names, native literal builtin semantics, exact
parent binding, protected snapshots and owner-project compatibility remain
their explicit surrounding contracts.
