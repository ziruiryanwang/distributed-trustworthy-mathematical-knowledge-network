# Original Lean expression DAG v1

Source-only candidate: `OriginalExpr.lean`, namespace `OrdinaryLean.ExprCodec`.
No build or runtime qualification is implied. The format grants no authority;
the declaration adapter must separately kernel-check every accepted extension.

## API and context

```text
encode (params : List Lean.Name) (expr : Lean.Expr) (limits := {}) : IO Json
decode (params : List Lean.Name) (allowed : Std.HashSet Lean.Name)
       (packet : Json) (limits := {}) : IO Lean.Expr
encodeName / decodeName : exact role-neutral name components
requireSemanticName : declaration/reference-name barrier
```

The caller binds the exact **original ordered** universe-parameter list, the
accepted environment/profile, allowed constant names and trusted resource limits.
The packet does not independently authenticate or supply those contexts. Parameter
names are unique, nonanonymous and bounded; decoded level indices refer directly
to that list. There is no post-decoding universe-name substitution.

Wire envelope:

```text
["DMKN_LEAN_ORIGINAL_EXPR_V1", levelNodes, expressionNodes, rootIndex]
```

This marker prevents reinterpretation as the old seed's lossy three-part DAG.
Normalization is exactly `erase-mdata-only-v1`. All `Expr.mdata` wrappers are
removed; binder names, annotations, let nondep flags, constants, native literals
and level structure remain. Metadata erasure may remove pretty-print/source
hints; this does not claim preservation of all frontend presentation state.

## Primitive data

Names are arrays from root to leaf. Empty means anonymous, allowed for binders
but not semantic constants. Components are `[0, bytes]` for string components
and `[1, UInt32]` for numeric components. Bytes are exactly
`{"$bytes":[0..255,...]}`. UTF-8 must decode and re-encode identically.

Names are not parsed from dotted strings: a string component containing a dot
remains distinct from two separate components. Binder labels may be anonymous
or use internal-looking names. Semantic names instead apply the reserved-name
barrier inherited from the native receiver and must be in the supplied grounded
allowlist. `Lean.reduceBool` and `Lean.reduceNat` are forbidden semantic names;
this is not a complete axiom/closure policy by itself.

All structural integers are nonnegative JSON integers, bounded by UInt64,
with narrower explicit bounds for name numerals, bound variables and projection
fields. Arbitrary natural literals use minimal unsigned big-endian bytes: zero
is the empty byte array, and a nonempty magnitude cannot start with zero.

Level nodes:

```text
[0]                       zero
[1, previousLevel]        succ
[2, leftLevel, rightLevel] max
[3, leftLevel, rightLevel] imax
[4, parameterIndex]       original ordered parameter
```

Expression nodes:

```text
[0, index]                                  bound variable
[1, levelIndex]                             sort
[2, name, [levelIndex,...]]                  constant
[3, functionIndex, argumentIndex]            application
[4, name, binderInfo, typeIndex, bodyIndex]   lambda
[5, name, binderInfo, typeIndex, bodyIndex]   forall
[6, name, typeIndex, valueIndex, bodyIndex, nondep] let
[7, magnitudeBytes]                         native Nat literal
[8, structureName, fieldIndex, valueIndex]   projection
[9, utf8Bytes]                              native String literal
```

Binder-info codes are default=0, implicit=1, strictImplicit=2 and instImplicit=3.
Let nondep is exactly 0 or 1, preserved as elaborator metadata; the codec does
not certify that this hint correctly describes the expression. Kernel checking
must establish the actual declaration's validity.

## Canonical DAG and bounds

Expression/level edges point strictly backward. The final expression is the
root and is closed. Bound-variable requirements are computed bottom-up, with
the enclosing binder discharging exactly one level in its body. Free variables,
expression metavariables and universe metavariables have no encoding.

Encoding traverses children left-to-right and interns full encoded nodes.
Expression memoization uses `ExprStructEq`, whose equality is `Expr.equal`,
not Lean's binder-insensitive `BEq Expr`. Thus alpha-equivalent expressions
with different binder names/annotations remain different nodes. No lossy-DAG
sidecar is used. Decoding re-encodes once to check canonical ordering, unique
sharing and absence of unreachable nodes; it does not tree-expand the DAG.

The trusted default profile caps 65,536 level nodes, 1,048,576 expression nodes,
depth 4,096, 1,024 parameters/constant universe instances, 4,096 name parts,
1 MiB UTF-8 bytes per name, 1 MiB per literal and 64 MiB aggregate literal bytes.
Indices, arity, node counts and depths are checked before constructing each
untrusted expression/level. Name/literal byte bounds precede constructing the
corresponding native Name/String/Nat values. Limits are caller-selected and
can be lowered. They are not a performance guarantee.

**Outer input responsibility:** this API accepts an already parsed `Json` value.
The future public reader must bound serialized bytes and parsing depth *before*
JSON parsing, and bound aggregate declarations, CPU, memory and elapsed time.
It must also reject exponent/fraction/negative numeric syntax before invoking
Lean's general JSON parser: this wire grammar needs only nonnegative decimal
integers, and a short huge-exponent token can cause substantial parser allocation
before the codec's numeric limits execute.
Name bytes repeated across many nodes are bounded by that outer message limit
and per-name limits, not by the aggregate-literal counter. No unbounded peer
message may reach this API merely because its eventual DAG would fit.

The known checked basis must supply the standard builtin semantics of native
Nat/String literals, not arbitrary definitions bearing those names. The codec
does not initialize a basis, load modules, infer types, add declarations, or
establish proof soundness. It is intentionally independent of peer executable
code and of the old restricted cryptographic representation.

## Required targeted checks before adoption

The root-selected execution should distinguish named binders and annotations,
anonymous binders, original universe names, let nondep variants, metadata-only
erasure, native numeral/String roundtrips, noncanonical/shared/orphan DAGs,
forward/out-of-range indices, bad scope, undeclared universes, disallowed names,
malformed UTF-8 and each configurable size/depth boundary. Those checks are
not yet run and do not by themselves establish ordinary-library interoperability.
