# Upstream record compatibility: narrow the warrant, retire the duplicate codec

2026-10-24. Source-only assessment by package_continuation for root review.
This completes the bounded assignment in UPSTREAM-VALIDATION-REUSE. No source
implementation, runtime, upgrade, migration, build or test is selected here.
All existing Lean 4.34 installations, states, identities and evidence remain unchanged.

## Decision

A small **upstream-native cold validation wrapper is feasible in principle**.
Use the upstream parser and fresh kernel replay; compare every parsed safe
record with its actual returned record using the relation below. Do not build
another declaration codec, translate to old V2 objects, or recreate exact
proof-witness identity when the intended claim is only theorem derivability.

This is a maintenance-reduction decision, not a speedup result or an accepted
toolchain migration. The existing resource/controller and exact foundation
policy remain necessary. Pin-specific primitive-policy completeness is a
separate premise, not something this compatibility review establishes.

The new warrant is:

> Under adopted policy P, the selected parsed theorem interfaces are derivable,
> and selected non-theorem mathematical records agree with the actually checked
> records under the declared upstream equality relation.

It is not a warrant that the original proof witnesses, original source,
frontend API, raw fields or separately supplied compiled artifacts were preserved.

## Inspected source and actual equality

All upstream references below are at immutable Lean4 revision
`eb6cafb7290e8bd5f2937522d8d804f58f02bafc` (v4.35.0). The source was read over HTTPS,
not installed. Principal files are
[Basic](https://github.com/leanprover/lean4/blob/eb6cafb7290e8bd5f2937522d8d804f58f02bafc/src/LeanExport/Basic.lean),
[Parse](https://github.com/leanprover/lean4/blob/eb6cafb7290e8bd5f2937522d8d804f58f02bafc/src/LeanExport/Parse.lean),
[Replay](https://github.com/leanprover/lean4/blob/eb6cafb7290e8bd5f2937522d8d804f58f02bafc/src/Lean/Replay.lean),
[Declaration](https://github.com/leanprover/lean4/blob/eb6cafb7290e8bd5f2937522d8d804f58f02bafc/src/Lean/Declaration.lean),
[Expr](https://github.com/leanprover/lean4/blob/eb6cafb7290e8bd5f2937522d8d804f58f02bafc/src/Lean/Expr.lean),
[Compare](https://github.com/leanprover/lean4/blob/eb6cafb7290e8bd5f2937522d8d804f58f02bafc/src/lake/Lake/Check/Compare.lean),
[Util](https://github.com/leanprover/lean4/blob/eb6cafb7290e8bd5f2937522d8d804f58f02bafc/src/lake/Lake/Check/Util.lean), and
[LeanChecker](https://github.com/leanprover/lean4/blob/eb6cafb7290e8bd5f2937522d8d804f58f02bafc/src/LeanChecker.lean).

**Important correction to the word exact:** the derived `BEq` instances for
`ConstantVal` and `ConstantInfo` compare expression fields using `Expr.eqv`.
`Expr.lean:804–819` documents this as alpha-equivalence ignoring binder
annotations; `Expr.equal` is the separate equality that includes binder names
and annotations. Thus full-record `==` is not raw-byte or all-annotation
identity. Here it is intentionally the version-pinned upstream relation.
It is not arbitrary definitional equivalence or a semantic-equivalence oracle.

Names and the ordered universe-parameter list are still compared, as are all
non-expression fields selected by the record instance. Expression intern tables
also use upstream `BEq`, so exact original binder spelling cannot be recovered
by making the post-check stricter.

## The concrete sufficient relation R

Let `C` be the parser's original complete `constMap`, and `K` the actual fresh
kernel environment returned by successful replay. For every name in `C`, require
an actual `K.find?` result and the relation below. The map's key must agree with
the record name. The precheck still rejects all unsafe/partial entries and
unpermitted axioms, including unused ones. Selected names must be present and
supported; an axiom is not a newly proved theorem target.

| Parsed kind | Required actual kind and comparison | Warrant and reason |
|---|---|---|
| `thmInfo` | Actual `thmInfo`; `parsed.toConstantVal == actual.toConstantVal` | Same name, ordered universe parameters and proposition under upstream expression equality. The actual theorem was checked. No equality of proof `value` or bookkeeping `all` is claimed. |
| `defnInfo` | Full `ConstantInfo ==` | Preserves the body, type, safety, reducibility hints and `all` under the declared equality. A different definition of the same type must not pass. |
| `opaqueInfo` | Full `ConstantInfo ==` | Preserves value as well as interface, safety and `all`. Do not silently turn an opaque value into an arbitrary same-type replacement. |
| `inductInfo` | Full `ConstantInfo ==` | Includes universes, parameters/indices, mutual names, constructor list, nested count and recursive/reflexive/safety flags. Replay reconstructs rather than directly admitting all these input fields. |
| `ctorInfo` | Full `ConstantInfo ==` | Includes parent, constructor index, parameter/field counts and safety. Upstream already checks postponed constructors; the all-record check also establishes explicit coverage. |
| `recInfo` | Full `ConstantInfo ==` | Includes mutual group, parameters/indices/motives/minors, constructor rules and right-hand sides, K flag and safety. Upstream already checks postponed recursors. |
| `quotInfo` | Full `ConstantInfo ==`, then policy anchoring | Kernel-generated quotient package must match the input and the adopted foundation. The quotient kind is part of the record. |
| `axiomInfo` | Full `ConstantInfo ==`, and exact adopted-foundation comparison | A replayed axiom is an assumption, not evidence for itself. Name-only allowlisting is insufficient. |

Keeping `all` and hints for definitions/opaque values is a cheap sufficient
rule, not a claim that all these fields are logically necessary.
`Declaration.lean` explicitly describes definition/theorem/opaque `all` as
bookkeeping not used by the kernel. In contrast, inductive/recursor grouping
and reduction rules have semantic roles and are not dropped.

The theorem distinction is deliberate: a checked proof of proposition A gives
the desired derivability warrant even if it is not the submitted witness of A.
The relation must not be reused for a claim that an exact witness was checked,
that a theorem dependency graph is unchanged, or that a submitted proof incurred
the actual measured work. The actual checked environment remains the authority
for proof-support and policy validation.

## Normalization and reconstruction boundaries

| Source behavior | Consequence for this lane |
|---|---|
| `Basic.removeMData` drops expression metadata by default and normalizes `letE.nonDep` to false. Its comment notes that expression `BEq` considers `nonDep`. | Claim the interpreted exported mathematics, not exact original source expressions or flags. Use the ordinary normalized export profile. |
| `Parse.parseExprMdata` reconstructs empty metadata and discards its contents. | Metadata/frontend fidelity cannot be promised even with the export-metadata option. The initial lane should exclude metadata-preservation claims, not invent another parser. |
| `parseDefnInfo` turns a regular hint's natural number into `UInt32`. | R compares the parsed hint with the actual hint. It does not certify preservation of an oversized raw integer. A raw-schema canonicality policy would be a different claim. |
| `parseOpaqueInfo` has an optional unsafe flag defaulting to false; current Basic writes the flag. | Eligibility applies to the parsed mathematical declaration actually checked. Version/header support must be explicit; no faithful interpretation of arbitrary old producer intent follows. |
| Parse rejects duplicate indices/declaration names, but consumes metadata without version validation and generally ignores extra inner fields. | The enclosing header check remains necessary. Exact input digest identifies consumed bytes, not proof that every field was interpreted. |
| Replay skips unsafe/partial entries. | Reject them before replay; never infer acceptance for every serialized name from exit status. |
| Replay's duplicate-theorem branch compares name/type/universes/`all`, not value. | The narrowed theorem R accommodates a checked same-interface witness, but never carries old witness IDs. |

For quotient replay, reuse `LeanChecker.checkExport`'s actual rule: retain the
original map for comparison, remove `Quot.mk`, `Quot.lift`, `Quot.ind` only from
the replay map, and replay `Quot` once. Adding the quotient declaration generates
the entire package. Compare all supplied quotient records against actual output;
foundation policy also fixes the primitive package and its required `Eq` semantics.
Do not remove the three records from the coverage ledger just because replay
must avoid adding them independently.

Mutual inductives need the all-record post-check. Parse merely inserts their
type/constructor/recursor records. Replay gathers the `info.all` members and
their constructors, then submits `inductDecl` using universe parameters,
parameter count, type names/types and constructor names/types; the kernel derives
the remaining fields. Replay checks supplied constructors and recursors, but
does not similarly compare each full supplied `InductiveVal`. R closes that
gap without a custom inductive codec. Missing/malformed group members must fail;
do not fall back to another ambient library.

No source argument here promises that every honest nested/mutual export passes
this sufficient rule. Incompatibility means the lane rejects or narrows support;
it does not justify weakening comparison until a desired example passes.

## Supporting coverage and implicit primitives

The simplest wrapper compares **every parsed safe record**, not only T or a
handpicked theorem-type closure. This is linear in the finite input inventory
plus structural comparison work; it creates no new semantic reachability
optimizer and no complete-network scan. It is still a cold whole-export check,
not ancestry-free or incremental verification.

For the first closed-export profile, additionally require that actual semantic
dependencies needed by the warranted records are covered by compared records
or by explicitly adopted foundation records whose actual instances are checked.
Include types, definition/opaque values, actual theorem support, inductive
mutual members/constructors, and recursor groups/rule constructors/right-hand
sides. A stronger all-input support check is acceptable; selecting only theorem
statement dependencies is insufficient for the claimed complete policy check.

`Lake.Check.runForUsedConsts` is reusable for most explicit dependencies:
it visits a record's type, own name, value with opaque/theorem access, inductive
constructors and mutual names, constructor parent, and recursor rule names/RHS.
It is **not the entire coverage policy**: it does not explicitly traverse
recursor `all` or implicit literal/kernel primitives. Required recursor grouping
can be checked using the existing record fields. Definition/theorem/opaque
bookkeeping `all` is not automatically a semantic dependency or an extra
warranted contribution.

Kernel-generated extra names do not automatically become named accepted outputs.
If a selected supported closure needs an auxiliary record not represented in
the compared input/foundation domain, the simple profile must reject that
coverage claim; a later explicit generated-record policy is possible but is not
selected here. Unused extra kernel-generated declarations do not require a
blanket claim that the whole output environment equals the input map.

Primitive anchoring remains separate from R. Basic itself exposes the gap in
ordinary constant traversal: natural literals trigger `Nat` export; string
literals trigger `Char.ofNat` and `String.ofList` export. Quotient construction
has special kernel behavior. These examples are not a proved exhaustive
inventory of kernel-special semantics. P must supply a complete version-pinned
primitive policy, including implicit typing/reduction uses and grounded semantic
dependencies, and compare actual relevant records to canonical F. The peer's
list of explicit constants cannot choose which primitive checks are omitted.
Canonical axiom type equality also needs this dependency grounding: a correct
axiom name/type expression interpreted over changed referenced definitions is
not the original foundation assumption.

## Why the wrapper can stay small

Use existing `LeanExport.parseStream`, `Kernel.Environment.replay`, `find?`,
`toConstantVal`, derived record `BEq`, and existing explicit-dependency helpers.
The new mathematical glue is a finite kind-dispatch comparison loop plus
receiver policy/coverage checks, not a second parser or serializer.

`Lake.Check.compareAt` demonstrates the theorem-interface/full-support pattern,
but directly looping over C is simpler for this all-record contract. The
function is oriented around two exported maps and selected challenge holes;
its theorem target loop also permits axiom/axiom pairs, so it would need our
independent target-kind restriction. In particular, **do not use
`definitionHoleMatches`**: it intentionally compares only `ConstantVal` and
safety while permitting a new definition value. That is correct for its
challenge use, not for preservation of an imported mathematical definition.

Bind the immutable input-byte digest, selected names and P separately from
the actual mathematical warrant. A protected event may record the exact
compared/support domain after clean completion, but it is neither an old V2
identifier, a transferable cryptographic certificate nor a `.olean` endorsement.

This bounded source question is closed with a conditional yes. Implementing a
new codec or exact-witness inventory would defeat the maintenance-saving reason
for considering upstream reuse. No experiment is needed to establish that
architectural choice. Whether adopting a new cold lane has higher payoff than
ordinary package interoperability/growth work is root's next decision; this
note does not automatically commission it.
