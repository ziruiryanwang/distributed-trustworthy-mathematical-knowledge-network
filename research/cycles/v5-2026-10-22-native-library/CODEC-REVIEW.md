# Original expression codec: independent source review

2026-10-22. Reviewer `lean_workflow_trace`. No compiler, Lean runtime, tests,
proof generation, product installation or Git mutation was invoked.

## Disposition and exact inspected source

**SOURCE REVIEW PASS FOR BOUNDED COMPILATION/CONTROLS; NOT EXECUTION OR PRODUCT
ACCEPTANCE.** No blocking metadata, scope, reference or canonical-DAG logic
defect was found in the inspected candidate. Compilation and changed-boundary
tests remain necessary; source plausibility is not evidence that the code builds.

| File | SHA-256 |
|---|---|
| `software/v5/ordinary_lean/OriginalExpr.lean` | `f9b281dfcd2864ec29f92b849a256dc79053262e3cbdc4aa98e38ead3617fc05` |
| `software/v5/ordinary_lean/EXPRESSION-FORMAT.md` | `950fc2c9cadc1f3c3af69cf9ebbece497eebc876c8bd266650645cc0f69b22ce` |

Read both files completely, the author checkpoint `IMPLEMENTATION-CODEC.md`,
root's selection, and relevant pinned `Lean/Expr.lean`, `Lean/Data/Json/Basic.lean`
and `Lean/Data/Json/Parser.lean` definitions. The review does not cover declaration
acceptance, basis adoption, persistence, full ordinary-library compatibility or
hostile-source isolation.

## Concrete contract checks

| Obligation | Inspected implementation |
|---|---|
| Distinct format | `decode` requires the exact four-field `DMKN_LEAN_ORIGINAL_EXPR_V1` envelope; it cannot silently reinterpret the old seed three-field DAG. |
| Original parameter names | Both entrypoints validate the caller-bound ordered nonanonymous unique names; `.param` indices decode under those exact names. There is no post-hoc incomplete renaming. |
| Original binder API | Lambda/forall nodes encode and decode `Name` plus `BinderInfo`; let nodes retain name and `nondep`. Anonymous labels remain allowed. |
| Erase only mdata | Encoder bypasses `.mdata` while preserving the child; it does not invoke the old `removeMData` helper that also erased binder names. |
| Metadata-sensitive memoization | `ExprStructEq` uses `Expr.equal` (verified in pinned `Expr.lean:1542-1557`); full encoded nodes also include binder fields, avoiding lossy interning. |
| Exact names | Names use root-to-leaf tagged components, not dotted string parsing. Native names are bounded before construction; semantic roles additionally reject anonymous/reserved roots. |
| Grounded references | Constant/projection decoding calls `referenceOf`, checking the caller's allowed set and role restriction. This establishes syntactic resolution only, not validity of the referenced declaration. |
| Levels | Only zero/succ/max/imax/original ordered parameters; every edge and parameter index is checked before array access and construction. |
| Expressions | Bound-variable/sort/constant/application/lambda/forall/let/Nat/projection/String forms only; free/metavariable forms have no accepted encoding. |
| Closed root | Bottom-up `needs` propagates domain/value requirements and decrements only binder bodies. Root is final and requires zero loose-variable demand. |
| Native literals | Nat magnitude is minimal big-endian (zero is empty); String bytes require exact UTF-8 roundtrip. Per-literal and aggregate-literal bounds precede native literal construction. |
| Canonical DAG | Re-encoding checks child order, structural sharing, uniqueness and reachability. Memoized traversal reuses shared subexpressions rather than expanding the represented expression tree. |
| Bounds before node creation | Arrays, node arities, indices, tag ranges, depth, universe instance length, name lengths and literal budgets are checked before each corresponding native construction. |
| No authority fabrication | No import, kernel insertion, filesystem access, certificate or accepted-state operation exists in this file. Its allowed-name set is provided by the later trusted adapter. |

The `nondep` flag is retained for source fidelity, not trusted as a theorem;
the source documentation correctly says the actual declaration must still be
kernel-checked. Numeric component and projection UInt32 limits are explicit
compatibility bounds, not claims to cover all conceivable Lean `Name` values.

## Required outer-reader clarification

The source correctly accepts only already parsed `Json` and delegates raw input
limits to the public reader. That future reader must constrain **numeric tokens
before parsing**, not only bytes and nesting depth.

Pinned `Lean/Data/Json/Parser.lean` parses exponent syntax through
`JsonNumber.shiftl`; positive exponents can compute a large power of ten before
the codec's `natOf` UInt64 check executes. A short exponent-bearing token can
therefore request large allocation even when the serialized message is small.

The format needs no negative, fractional or exponent numbers. The simplest
future reader is a bounded lexical preflight that permits only nonnegative
decimal-integer numeric tokens outside strings, with token length bounded for
UInt64 structural values; natural-literal magnitudes already use byte arrays.
Apply the byte/depth limits before the generic parser too, and reject duplicate
object fields if canonical raw-byte identity is claimed. JSON structural
roundtrip alone does not prove a unique original textual spelling.

This does not require broadening the codec's authority or inventing another
mathematical parser. It is a concrete requirement for the later external-byte
boundary. The author and root were notified before runtime selection.

## Cost qualifications

This review supports DAG sharing, not a theorem of linear wall-clock or CPU
cost. Hash collisions, structural equality, large native Nat construction and
ordinary runtime allocation still consume resources. `ExprStructEq.hash` uses
the ordinary expression hash; preserving metadata-sensitive equality does not
by itself establish adversarially robust hashing. Keep actual CPU/memory/wall
limits and suitably small first selected input limits.

Per-name byte limits plus an outer message limit bound repeated name bytes;
the aggregate literal counter intentionally does not count names. The encoder
also charges source traversal depth, so deeply nested mdata can refuse even if
the normalized mathematical output is shallow. This is a resource restriction,
not a change of accepted mathematics.

## Small changed-boundary test selection

One bounded compilation and focused controls should cover:

- Two alpha-equivalent binder expressions with different names/annotations
  remain distinguishable; named-argument type metadata survives roundtrip.
- Original universe names, anonymous binders, both let flags and mdata-only
  erasure preserve the documented projection.
- Shared subexpressions and native Nat/String literals roundtrip without tree
  expansion or successor-chain conversion.
- Forward/out-of-range indices, open roots, foreign names, undeclared universe
  parameters, bad UTF-8, nonminimal Nat magnitudes, duplicate/unreachable nodes
  and selected lowered resource bounds refuse.

These controls target newly introduced behavior; they do not justify rerunning
the old mathematical basis qualification or producing another certificate.
No test is authorized or executed by this review itself.

## Additional declaration, checker and control-source review

Root subsequently requested review of the complete new declaration codec,
checked-extension plumbing and focused syntax controls. All were read in full,
together with `DECLARATION-FORMAT.md`, `IMPLEMENTATION-DECLARATION.md` and
`INTEGRATION.md`.

| Additional inspected file | SHA-256 |
|---|---|
| `OriginalDecl.lean` | `046f654b89906bbb4f627843d398e9f10b0e63e7c8b587908b8ac70517a0f8b8` |
| `CheckedExtension.lean` | `30b657baeec406062cbc153e8c5045c6b25cf89bfe7951013a2da8da42b7746e` |
| `CodecChecks.lean` | `008aaf9e61cdbca2da687b3d08dc585f4fc738aa40cb3466d71b68392c06478e` |
| `INTEGRATION.md` | `961dfe26ceb5116e6ba1992e2555c28ca062f44f96e1302d47b3dd755646f9dc` |

**Additional disposition: no blocking source defect found; proceed to root's
bounded compilation/selected controls, not product acceptance.**

Concrete reviewed points:

- `DeclCodec` preserves original levels, hints and `all`; neither the old
  descriptor nor `withHeight` is reused for new ordinary declaration identity.
- Decoder preflight charges both descriptor and claimed inventory DAG nodes.
  Expected inventory remains JSON claims, not installed `ConstantInfo`.
- An inductive group permits self-reference only to its new type names.
  Arbitrary advertised constructors, recursors or other inventory entries do
  not become premises by being listed. Pairwise introduced-name checks reject
  overlapping type/constructor names, including across later group members.
- Ordinary unit inventory must name exactly that ordinary declaration. Group
  inventories must include their stated types/constructors; actual recursors,
  nested auxiliaries and exact outputs are the checked layer's responsibility.
- `CheckedExtension` rejects axiom/quotient/unsafe/partial new declarations,
  direct `sorryAx`/forbidden-evaluation references and missing external names.
  Existing-parent soundness and implicit literal builtin meanings are explicit
  caller preconditions, not inferred from `quotInit` or a names allowlist.
- All checks enter `Environment.addDeclCore` with finite nonzero limits and
  fixed `doCheck := true`. There is no `Lean.addDecl` fallback-axiom path.
- Expected names must be fresh relative to the current kernel environment and
  prior units. Each promised actual record is compared through the exact
  ordinary inventory projection after checked generation.
- Complete extra-generation detection occurs once at the final bounded stage2
  census. A generated omitted name might temporarily be visible to a subsequent
  unit, but it cannot escape in a successful batch: it changes the final count
  or membership check and the whole batch refuses. A later unit cannot claim
  that name as new, since the current-environment freshness check then fails.
- No successful prefix is returned after an error. Persistent promotion is
  still a separate future controller action. The persistent Lean environment
  value supplied as the parent is not overwritten by this function.
- Stage2 census work is bounded once per batch, not a scan of all imported
  ancestry per declaration. Reimporting committed parents establishes the
  intended snapshot boundary; metadata scans and checking still consume actual
  resources and require aggregate operation limits.

`DecodedUnit` and `Environment` remain ordinary internal typed values, not
unforgeable proof capabilities. A public endpoint must obtain them through the
selected decoding and warranted-parent controller paths; arbitrary caller
construction is not an alternative admission API.

The current `CodecChecks` exercise expression metadata, original universes,
native literals, role-aware names, a 101-node shared expression DAG, malformed
scopes/indices/UTF-8, canonicality and lowered bounds. Its positive expressions
need not be well typed; this is intentional syntax-only coverage. Its success
line explicitly says `syntax_only=true mathematical_acceptance=false`.
It does not test declaration generation or kernel preservation and must not be
reported as doing so. Targeted declaration/checker controls remain separate.

No compile-type errors were established by this source review. Compilation is
the next appropriate inexpensive discriminator; any actual compiler failure
must be preserved and fixed in the mutable successor rather than predicted
away or treated as a reason to launch a broad experiment campaign.
