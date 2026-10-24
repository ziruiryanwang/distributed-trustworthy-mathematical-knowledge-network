# Upstream validation reuse: a real dependency candidate, not free acceptance

2026-10-24. Root source investigation, paired with
GROWTH-DEFAULT-ARCHITECTURE-AUDIT. Read-only HTTPS source inspection; no clone,
dependency installation, toolchain upgrade, compilation or experiment. Existing
Lean 4.34.0 installations, identities and evidence are unchanged.

## Why this can change the architecture

The [official validation guidance](https://lean-lang.org/doc/reference/4.34.0/ValidatingProofs/)
distinguishes ordinary honest-source checking, replay of compiled declarations,
and sandboxed export plus external rechecking for malicious input. The separate
[Comparator project](https://github.com/leanprover/comparator/blob/865edc14486c3388e9225daa971da8e157488c3e/README.md)
now reports integration into Lean 4.35.0 as `lake check` and `lake comparator`.
This is an actual maintained alternative to parts of bespoke interchange, not
a hypothetical baseline gifted our future implementation. It deserves a bounded
source comparison before further custom parser/checker or sandbox development.

The relevant reusable primitives do not inherently require a human research
question: exporting declarations and checking their derivations is distinct from
Comparator's additional comparison with an independently authored challenge.
Our protocol still has no human-intention field or mandatory mathematical tasks.

## Exact inspected upstream revision

GitHub tag `v4.35.0` resolved to
`eb6cafb7290e8bd5f2937522d8d804f58f02bafc`. Root read the complete files below
at that immutable revision. The source contents, not a promise about a newer
release or binary, support these findings.

| Source | Reusable capability | Boundary found in source |
|---|---|---|
| `src/LeanExport/Basic.lean` | `dumpEnv` selects constants, recursively emits dependencies, shares expression/name/level tables, and handles inductive groups | Full selected closure; `initState` scans imported constants to construct the recursor map. No accepted-frontier protocol or cross-call cache. Kernel declarations, not frontend extension state. |
| `src/LeanExport/Json.lean` | Duplicate-object-key rejecting JSON parser | Parser correctness and resource exposure still matter; this is not a sandbox. |
| `src/LeanExport/Parse.lean` | Reconstructs inert `ExportedEnv`/`ConstantInfo` maps; rejects reused indices and duplicate declarations | Does not grant acceptance or insert into the live environment. First metadata line is consumed without validating its version. No explicit aggregate byte/node quotas in this parser. |
| `src/LeanChecker.lean` | `--from-export` parses data, replays into a fresh kernel environment and checks actual generated quotient records | No project exact foundation identity, finite caller allowance, retained warrant or exact witness inventory supplied by this function. |
| `src/Lean/Replay.lean` | Reconstructs declarations through `addDeclCore`; checks supplied constructors/recursors against generated ones | Axioms are admitted as axiom declarations, unsafe/partial constants are skipped, and duplicate theorem cases may retain a same-interface existing proof. `addDeclCore 0 0` supplies no finite kernel heartbeat/recursion limit here. |

For example, the pinned source is available at
[LeanExport.Basic](https://github.com/leanprover/lean4/blob/eb6cafb7290e8bd5f2937522d8d804f58f02bafc/src/LeanExport/Basic.lean),
[LeanExport.Parse](https://github.com/leanprover/lean4/blob/eb6cafb7290e8bd5f2937522d8d804f58f02bafc/src/LeanExport/Parse.lean),
[LeanChecker](https://github.com/leanprover/lean4/blob/eb6cafb7290e8bd5f2937522d8d804f58f02bafc/src/LeanChecker.lean),
and [Replay](https://github.com/leanprover/lean4/blob/eb6cafb7290e8bd5f2937522d8d804f58f02bafc/src/Lean/Replay.lean).
The independent audit owns the `Lake/CLI/Check` and policy/comparison analysis.

Our retained 4.34 source contains `LeanChecker.lean` with the compiled-module
replay routes, but not the integrated `LeanExport`/`lake check` sources found
above. The version difference is a consequential adoption boundary. A source
read is not proof that a new runtime works with our pinned foundation or states.

## What must not be replaced by an exit code

The project needs a statement of the form:

    exact supported declarations are derivable under this receiver's
    exact adopted foundation and permitted axioms.

Fresh kernel replay by itself instead establishes derivability relative to
whatever well-formed axioms its input supplies. A permitted axiom NAME is not
its exact type/universes/semantic dependencies. A fabricated axiom carrying a
familiar name can be well-formed but state a different proposition. Therefore
name-only whitelisting cannot establish our exact foundation policy. This is a
logical scope argument, not an executed exploit or a claim that the whole
upstream tool is unsound for its documented use. The independent review must
also account for any anchoring performed by the surrounding CLI.

Similarly, exact source-byte identity and mathematical interface equivalence
are different: a duplicate-theorem shortcut may be suitable for replay, but
cannot certify that a selected proof body was used. Any adopter would have to
keep our exact evidence binding separate from that shortcut's warranted claim.
Parsed but skipped declarations must not become accepted exported targets.

The new upstream components neither solve cold ancestry-free verification nor
restore notation, simp databases, class registration or arbitrary automation.
Their value is avoiding duplicate validation infrastructure and benefiting from
upstream maintenance, not automatically obtaining cheaper proof checking or a
complete decentralized library.

## Architectural consequence and bounded next choice

Keep ordinary approved Lean workspaces as the authoring/API plane. Keep exact
receiver admission as a separate plane. Treat upstream export/replay as a
candidate implementation dependency within the latter, not as a new consensus
or trust authority. Preserve the current tested 4.34 lane while comparing the
exact acceptance contracts.

Before selecting a migration, resolve from source: exact basis/axiom anchoring,
selected-target eligibility, bounded input exposure, supported declaration
fidelity, persistent local-frontier integration, and the native platform's
security boundary. Native hostile-source isolation is not supplied merely by
adopting an upstream Linux command on Windows. Do not use an unsafe bypass to
make a compatibility demonstration pass.

This comparison has higher expected marginal payoff than another proof campaign:
it can remove whole categories of custom maintenance. But it has no measured
speedup claim, and an upstream-name substitution without these boundary checks
would reduce assurance. If the contract cannot be preserved economically, retain
the existing path and stop the migration rather than rewriting successful state.

## Concrete cold-adoption contract, without a challenge theorem

This is a source-level target for a narrow upstream-native adapter, not an
implemented API, new wire format or adopted runtime. It is deliberately a cold,
closed-export operation. Incremental imports, original-package artifact binding,
and installation into a consumer's elaboration environment are separate claims.
Do not hide those in the word "adoption".

Inputs are (1) immutable exact export bytes E, (2) a nonempty explicit set T of
structured exported names, (3) an already adopted policy P containing exact
versioned kernel/codec identities and a canonical foundation map F, and (4) one
finite caller allowance. T selects contributed mathematics, not an intended
human problem; no comparison against a user's informal statement is needed.

The adapter may return a protected local validation event only if:

1. **Input binding.** It consumes the same immutable E throughout; the result
   binds its digest, exact selected T and exact P. The adapter validates the
   supported export/version header rather than relying on `parseMdata` to do it.
   No file chosen by E controls the runtime, allowance or approved foundation.
2. **Bounded parsing.** Input bytes, line size, table/declaration counts and
   parser process resources stay within caller bounds. All participating child
   work is charged to that same allowance. No raw upstream process-exit success
   can override a timeout, unfinished child or unknown failed accounting state.
3. **Declaration eligibility.** Selected names exist, are safe supported
   mathematical kinds, and are not new axioms or skipped unsafe/partial entries.
   For this simple first contract, reject all unsafe/partial and all unpermitted
   axiom entries in E, even unused ones. A more permissive unreachable-data filter
   is unnecessary initially. Incomplete closure must fail, not load ambient names.
4. **Foundation anchoring.** Every axiom in E is exactly a permitted record in F,
   including universes/type and grounded semantic dependencies. Match the actual
   kernel-special declarations used by the selected runtime to F as well. Each
   comparison follows the required dependencies; identical printed names alone
   never suffice. The finite comparison domain is policy-owned, not peer-owned.
   It must account for implicit primitive uses, including literal typing/reduction
   and quotient generation; ordinary expression-constant traversal is insufficient.
5. **Actual kernel checking.** Reconstruct E in a fresh empty kernel environment
   using the adopted upstream replay, under enclosing finite containment. No
   imported remote compiled environment or saved peer report is a premise.
6. **Actual-result equality.** Every requested declaration and its required
   supporting records correspond to the actual reconstructed kernel records,
   under one explicitly specified full-record comparison. Generated inductive,
   constructor and recursor fields and exact proof witnesses are included where
   the output claims their identity. A replay skip, duplicate-interface shortcut,
   or extra peer metadata cannot stand in for this check. If the chosen upstream
   normalization loses a claimed field, the contract must reject or explicitly
   narrow that identity claim; it must not borrow old exact object IDs.
7. **Commit after closure.** Record validation only after successful complete
   checking and clean process closure. The event means only that the bound inert
   mathematical records passed P. It neither blesses a separately supplied
   `.olean` nor copies a receipt into another receiver's trusted state. Retain
   exact selected/support coverage, not an unqualified checked flag for all names
   that happen to occur in the input file.

**Conditional soundness argument.** Assuming the adopted parser's interpretation,
kernel rules, foundation and exact-binding/containment implementation are correct,
Step 5 constructs a checked environment. Step 4 ensures its admitted axiom leaves
and special primitive semantics are precisely within P. Step 3 excludes unchecked
selected kinds, and Step 6 ties T to the actual environment rather than only to
the input's claims. Thus each selected result is derivable under P. Step 1 binds
that judgment to the selected data; Step 7 prevents a failed attempt from becoming
a durable warrant. Cryptographic succinctness is not assumed or obtained.

The source existence of a replay function returning a kernel environment makes
this contract implementable in principle. It is **not** evidence that exact
record equality accepts every honest Lean export. Normalization, nested/mutual
groups, memory limits and version-specific supported kinds need a focused
compatibility assessment before implementation is selected. Exact comparison is
a simple sufficient assurance rule, not a claim of mathematical necessity.

This would be an upstream-native representation, not an NDJSON-to-old-V2 bridge.
Creating such a bridge would retain both codecs, both identity obligations and
the conversion layer, defeating the main maintenance-saving hypothesis. Old
4.34 installations/evidence remain valid only under their existing supported
rules; no cross-version warm-cache compatibility follows from this proposal.

## Independent review and one remaining source decision

Root read/adopts the conditional-soundness review in
GROWTH-DEFAULT-ARCHITECTURE-AUDIT and the maintenance/retirement challenge in
UPSTREAM-ADOPTION-CHALLENGE. They support the proposed boundary, not an upgrade or
new acceptance authority. The primitive/coverage clarifications above incorporate
their material cautions.

Root selects one final **source-only** compatibility table in
`UPSTREAM-RECORD-COMPATIBILITY.md`, owned by package_continuation: inspect upstream
normalization, mutual/group replay and the actual returned records; distinguish
fields needed for mathematical semantics from unnecessary inheritance of old
proof-witness/bookkeeping identities. A whole-record equality rule is sufficient
but may be unnecessarily restrictive. The table must choose a concrete comparison
relation and identify reusable source functions, not request a broad benchmark.
Root independently reviews it. No parser implementation, format translation,
toolchain installation, campaign or migration follows automatically.

### Candidate projection for the new claim (not old-ID compatibility)

The new lane need not inherit the old lane's theorem-proof witness identity.
For supplied parsed record c and actual checked record a, the proposed sufficient
comparison is:

    R(c, a) =
      same theorem kind and upstream ConstantVal equality(name, universes, type),
        if both are theorem declarations;
      upstream ConstantInfo equality over the other record fields,
        for the other explicitly supported safe mathematical kinds.

**Equality precision:** derived upstream record equality uses `Expr.eqv`, which
is alpha-equivalence and ignores binder annotations, not `Expr.equal` or byte
equality. Global names and universe parameter lists still follow the record's
equality. Thus R warrants the mathematical interface under this explicitly
declared relation, not preservation of binder spelling/implicit-argument API or
every original serialized field. This matters for the claim, not only its code.

Permitted axioms additionally match the adopted F, and unsupported/skipped kinds
always refuse. Apply this comparison to the complete supported input record map,
not only its selected theorem names; this avoids a new selective-coverage
optimizer. Require each compared actual record to exist after successful replay.
T determines the advertised entrypoints and the event records the comparison's
coverage. Primitive grounding includes implicit kernel uses as specified above.

The claim is **derivability of the selected theorem interface under R in the actual
checked environment**, not proof-body equality or proof of each peer-supplied
historical witness. Definitions and opaque values keep their bodies under upstream
expression equality; generated group, constructor and recursor records keep all
record fields under the stated upstream equality. These checks prevent an
interface-only comparison from changing the meaning of dependent declarations.
All equality is over the explicitly pinned parsed/normalized upstream data model;
loss of a publicly claimed field is never silently ignored.

There is no definition-hole allowance here. Upstream `definitionHoleMatches`
deliberately allows a different definition value and is inappropriate for this
relation. A direct finite loop over existing `ConstantInfo`/`ConstantVal`
equalities is preferable to a new serializer or logical-equivalence engine.
The exact input digest still identifies the received artifact, independently of
the scope of the mathematical claim. No original V2 identity or stored warrant
is reinterpreted. The assigned compatibility table must determine whether honest
supported records can satisfy this relation without recreating old inventory code.

## Closed source decision; no automatic implementation

Root read/adopts UPSTREAM-RECORD-COMPATIBILITY on 2026-10-24. R is a feasible
small finite comparison using upstream records, conditional on the stated
foundation/coverage premises. Retain the original parsed map for the all-record
comparison while using LeanChecker's quotient filtering only for replay. Full
inductive record comparison closes the generated-field gap. Explicit dependency
helpers do not exhaust implicit primitive policy. No tested compatibility, speedup,
toolchain migration, warm import or original-package endorsement follows.

This closes the source assignment. A new cold wrapper is a replacement option,
not the selected next implementation: growth-led workflow decisions have priority
over another validation lane. Existing sources, installs, accepted state and
failures remain unchanged. See ../v5-2026-10-24-growth-selection/SELECTION.md.
