# Deferred proposal: bounded structural applicability views

Superseded before implementation on 2026-10-23 by
[two-stage definition-body discovery](ORDINARY-APPLICABILITY-DESIGN.md).
Root and independent review preferred that smaller intervention. The original
proposal below is retained as research, not implementation authority. Its
pre-deferral SHA-256 was
`18c2837c13f5a875a051e4d9f1fc488fbb4f42e37cbf76a05de0739228790f3c`.
Its VAR/CONST bijection does not cover arbitrary substitution; fixed depth three
does not establish selectivity; and the suggested cross-pair sharing of the
hypothesis's x with the conclusion's x was incorrect (independent binders).

2026-10-23. Source-only design, `portable_integration_audit`.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Root requested this follow-on after the whole-cost audit. No source change,
execution, build or campaign is authorized by this note. Complete the ordinary
reciprocal A/B path first; do not mistake its broad query for scalable discovery.

## Product decision and smallest version

A consumer should be able to search from a **formal local need**, without
already knowing the new theorem or its private abstraction's identifier.
The proposed first version indexes bounded conclusion structure and its
relationship to individual hypothesis/domain structures. It deliberately does
not solve general theorem application, higher-order unification or mathematical
equivalence. Existing exact-symbol search remains useful and unchanged.

The new view is a bounded retrieval hint. A provider's signed or Merkle-bound
hint does not imply that its theorem is true or applicable. A candidate's full
missing evidence still passes ordinary admission; the consumer's eventual
application still passes the Lean checker. Learned ranking may order candidates
or choose searches, but cannot bypass either gate.

Example need, authored in the consumer's own vocabulary:

```lean
hf : ∀ x, P x → P (f x)
hg : ∀ x, P x → P (g x)
⊢ ∀ x, P x → P (f (g x))
```

The provider theorem may instead say
`Stable f P → Stable g P → Stable (fun x => f (g x)) P`.
Its selected transparent definition of `Stable` exposes the same bounded
structural relations. The query uses the consumer's displayed formal sequent,
not `Stable`'s identity, its theorem name, a natural-language intention, or an
ID supplied by the experiment author. An agent needing a threefold composition
may choose this justified intermediate need itself; the system does not pretend
that exact twofold matching automatically solves arbitrary larger goals.

## Namespaces and source objects

Proposed schemas, not existing implemented versions:

```json
{
  "schema": "DMKN_ORDINARY_APPLICABILITY_PROFILE_V1",
  "reducer": "outer-pi-beta-zeta-single-definition-v1",
  "shape": "spine-binder-role-v1",
  "depths": [1, 2, 3],
  "domain_window": 8,
  "max_source_bytes": 1048576,
  "max_definition_units": 16,
  "max_steps": 32768,
  "max_telescope_binders": 128,
  "max_shape_nodes": 512,
  "max_shape_bytes": 8192,
  "max_features": 32
}
```

These numbers are a concrete starting envelope, not measured optimal defaults.
The exact profile is canonical, fixed in the namespace and not an executable
remote configuration. Its ID is a domain-separated hash of canonical bytes.
Namespace binds `(semantic_id, foundation_id, profile_id, ordinary-preview-v2,
ordinary-evidence-v2, new-feature-schema)`, never an owner's ImplementationID,
local root, operator identity or per-query hidden policy. A new profile makes a
new index; used predecessor indexes remain unchanged.

Reuse the exact ordinary V2 type preview and its ExportID→UnitID locator as
source objects. The proposed `DMKN_FORMAL_FEATURE_RECORD_V4` retains the generic
record shape: schema, namespace, kind, object ID, exact preview byte hash/length,
sorted feature IDs and the existing ordinary locator. Its object ID is the
original ExportID, not an invented theorem identity. A V4-specific validator
must recognize the new namespace/profile; it cannot be passed through the
current V3 namespace rule, which recomputes the old atomic namespace.

No new view-object transport is required for this smallest design. The adapter
derives views from the exact preview plus bounded exact ordinary definition
evidence obtained through the existing locator/evidence APIs. Candidate
resolution repeats this derivation and compares the complete record. The
profile's fixed deterministic extraction must produce one record per export.
An unavailable required definition therefore yields `VIEW_UNAVAILABLE`, not a
different record depending on which provider happened to answer. Existing atomic
indexes may still expose the theorem separately. Record insertion in the richer
index occurs only when its deterministic required source prefix is available.

Changing corpus/index coverage does not change mathematical identity. New valid
definition evidence for the same exact portable symbol cannot change its bound
body without failing the existing identity checks. A different abstraction or
checking policy has a different exact identity/namespace.

## Deterministic bounded view derivation

The adapter receives `(exact_preview, profile, fetch_exact_definition)`.
The callback is bounded, inert acquisition; it cannot execute peer source or
install a module. It locates the exact portable symbol, reads its evidence and
checks the export/import bindings using the existing portable evidence reader.
This establishes content binding, not mathematical validity.

1. Read the exact type DAG and its portable symbol bindings. Reject malformed
   scoping or inconsistent identities using the selected ordinary readers.
2. At the current outer type head, use a fixed leftmost order of syntactic
   beta reduction and let substitution, followed by unfolding an encountered
   transparent, single-definition unit when supported. Apply the exact universe
   substitution and capture-avoiding de Bruijn substitution. Count produced as
   well as visited nodes. This is not unrestricted normalization.
3. Peel an exposed outer `forallE`, recording its domain and a stable telescope
   binder identifier, then continue on its body. The terminal expression is the
   conclusion view. Inner binders in domains remain structurally represented;
   bounded head reduction may expose their bodies under the same fixed policy.
4. Retain at most the final `domain_window` recorded domains for relational
   features. No type inference decides which domain is a proposition. A domain
   may be a type, data argument, premise or typeclass argument; all are merely
   syntactic candidates. The consumer's reified local context uses the same rule.
5. Theorem/opaque constants, generated recursive groups, recursors, projections
   needing computation and unsupported reductions remain neutral atoms. No proof
   body is unfolded. Already visited expansion cycles become a documented cut,
   not recursion. Unsupported neutral structure does not claim convertibility.
6. A deterministic work/depth/byte limit produces a `CUT` node at its exact
   stopping position. Scoping or identity failure is a refusal. Missing bytes
   required by the deterministic prefix is `VIEW_UNAVAILABLE`, not `CUT`.
   This distinction prevents availability-dependent features for one export.

The reference algorithm must specify traversal order, counter charging and
the exact cut position before implementation. Counters cover parsing, free
variable/index adjustment, universe substitution, allocations, DAG copying,
hashing and feature construction. Sharing the input DAG does not by itself
prevent exponential beta/substitution expansion; the generated-node/work caps
must stop it. A coherent implementation can avoid redundant work by memoizing
`(node, binder environment, substitution, remaining view depth)` within this
operation, not merely memoizing the raw node under different scopes.

The construction does not require these reductions to be trusted as a proof
checker. They must be reproducible and correctly bound to advertised source
for the *retrieval* claim; final admission/application provides mathematical
authority. A buggy reduction may harm retrieval precision/recall, which still
requires tests and correction, but cannot make its output an accepted theorem.

## Exact shape grammar and feasible matching relation

After bounded derivation, describe each selected term with an n-ary application
spine rather than a deeply left-associated binary application chain:

```text
Shape ::= CUT
        | SORT
        | VAR(role)                    -- a peeled telescope binder
        | BVAR(distance)               -- a binder internal to this shape
        | CONST(role)                  -- portable constant identity, blinded
        | NAT | STRING
        | APP(Shape, [Shape,...])
        | LAM(Shape, Shape) | PI(Shape, Shape)
        | LET(Shape, Shape, Shape)
        | PROJ(role, index, Shape)
```

Binder display names, binder-info flags and universe levels are omitted from
this *hint* shape, not from underlying evidence. Constants are blinded so that
private names are not mandatory query vocabulary. Within one signature,
`CONST(role)` preserves the equality pattern of exact portable symbols, and
`VAR(role)` preserves the equality pattern of outer telescope binders. They
are separate role namespaces. Internal `BVAR(distance)` preserves binding.
Projection index is exact; its structure-symbol role is canonicalized with
other constant roles. Values of literals are omitted in this first profile.

At each selected depth, truncate below that depth to `CUT`; constants/variables
at retained positions remain leaves. Renumber retained free binder roles and
constant roles by first occurrence in a fixed preorder **after truncation**.
For a relational signature, visit the conclusion first and then the selected
domain, sharing one renaming map. Unused telescope positions therefore do not
change a signature, while repeated-variable relationships do. Apply the
shape-node/byte cap before accepting an emitted signature; if not representable,
emit no key for that signature and report that deterministic omission.

Feature specifications are exactly:

```json
{"tag":"declaration-kind","value":"theorem"}
{"tag":"conclusion-shape","depth":2,"shape":["...canonical Shape..."]}
{"tag":"conclusion-domain-shape","depth":2,
 "conclusion":["..."],"domain":["..."]}
```

The notation above illustrates fields; real shape bytes use one fixed array
encoding of the grammar. Feature ID is a domain-separated hash of namespace
and canonical specification. Three depths and eight domains give at most
`1+3+3*8=28` keys, with duplicates collapsed. Definitions may use their actual
kind key; no theorem status is inferred from a type-shaped string.

**Matching is equality of these bounded canonical shapes**, not higher-order
pattern solving. For supported retained terms, equality means the syntactic
skeletons agree modulo the explicit role renamings and stated erasures/cuts.
The proof is structural induction on the retained shape: tags/arity/internal
binding must agree, and first-occurrence roles induce a consistent bijection
between the retained outer variables and separately between retained constants.
Cryptographic feature equality alone additionally relies on collision resistance;
candidate resolution can compare the underlying canonical structures directly.

This claim intentionally does not imply equality of original Lean types,
matching universe constraints, discharge of all premises, or existence of an
instantiation. It handles alpha renaming and partial structural similarity
computably without deciding extensional equality. General term substitution,
eta equivalence, arbitrary rewrites and typeclass search are outside V1.

## Query construction from the actual local need

The owner SDK accepts the local formal context and goal, plus an explicit
selection of optional contextual domains. Close/reify the relevant local free
variables into a well-scoped telescope using ordinary exact local symbols.
Derive the same bounded view. No target theorem or target-private symbol is
an input. An agent may choose a subgoal or intermediate result, but it must
submit that formal need, not secretly insert the sought theorem ID.

The compiler generates candidate feature specifications only from that view:
one conclusion shape at a selected depth, optionally a small number of
conclusion-domain relations that actually occur in the submitted local need,
and a kind filter. The agent may query a weaker depth or omit domain constraints
under a new explicit budget. It may not label a constrained query complete for
all applicable theorems. A useful theorem whose prerequisites are derivable but
not currently in the local context can be missed by a premise-constrained query.

For the example, bounded unfolding exposes the same conclusion chain
`P(f(g(x)))`. A relational feature additionally ties the repeated `P`, `f` and
`x` roles to the domain `∀x, P x → P(f x)`. The exact private word `Stable`
never appears in the query key. Shapes of unrelated commutativity, existence,
injectivity and inversion facts differ at sufficient retained depth, although
some preservation families will share the same shape. This is a reason to
test selectivity, not a universal rare-key theorem.

Syntactic matches can be ranked by remaining premises, full type similarity,
estimated missing dependency bytes, local cache overlap or a learned model.
Those scores are advisory and must be computed within the same aggregate
resource budget. A popularity score is not evidence of correctness. The API
must preserve candidates' exact identities and expose score provenance rather
than turning rank into an acceptance status.

## Three distinct assurance statements

| Stage | Defensible statement | Not established |
|---|---|---|
| Authenticated posting membership | This record/key occurs in this provider's committed finite snapshot. | Correct feature extraction, full corpus coverage, theorem truth. |
| Reconstructed source-bound shape | Exact preview/definition evidence yields this shape/key under the adopted bounded profile. | Applicability, discharged premises, mathematical equivalence. |
| Ordinary mathematical admission and actual use | Missing evidence checks under the local policy; the new contribution checks using exact accepted meanings. | Global novelty, usefulness for every agent, exhaustive discovery. |

Candidate-only pages remain explicitly incomplete about skipped ranges.
Exhaustive query answers, where supported, concern only the committed finite
index and its correctly extracted population, not disconnected mathematics.
Shape omission due to bounds is separately exposed; silent absence is not an
assertion that no useful theorem exists.

## Cost bounds and compatibility path

Let `B` be the selected source-byte bound, `V` the charged-work bound, `h<=28`
the emitted feature count, `P` the selected provider count and `s(q)` the summed
rarest posting populations for the compiled query. View derivation is bounded
by `B` acquired bytes and `V` charged work, subject to implementation accounting.
At least these bounds must include all definition locators/acquisition failures;
a callback cannot spend an independent unbounded allowance for each expansion.
Store the derived feature record, not a duplicated full theorem proof.

Existing authenticated posting indexes can insert these bounded feature keys.
Index costs include at most `h` posting updates per record and their actual
authenticated-tree work; retained storage grows with indexed records/features.
Search cost is routing/summary overhead plus anchor examinations, membership
probes, returned records and their proofs. The material driver remains `s(q)`,
not merely the number of successful hits. This profile improves asymptotics
only for a workload with selective shapes and suitable provider coverage.
If `s(q)=Theta(N)`, it remains linear to exhaust that query. Query and provider
caps safely truncate it; they do not prove recall.

The smallest implementation path, if root selects it, is:

1. A new ordinary shape adapter and V4 record/namespace branch, using unchanged
   ordinary V2 previews/evidence and typed exact-definition acquisition.
2. A query compiler from an explicitly supplied local formal sequent; independent
   source review checks that the Stable test needs no hidden target identity.
3. Reuse existing store, posting trees, query/session budgets and candidate
   authentication. No new DHT, ledger, proof format, verifier or source sandbox.
4. Expose adapter resolution with the bounded acquisition callback. Existing
   V3 adapters/indexes remain usable side by side. No silent in-place migration.

Existing configured conjunction postings may later combine useful new shape
atoms, but are not necessary to establish this first profile. Do not migrate
their old module-export client wholesale or pretend its old schema already
supports ordinary V2. One shared informative shape key should be established
before adding another query planner.

## Decision-changing review and stop condition

Before implementation, resolve the one real semantic-engineering question:
can a small deterministic reducer expose the example's conclusion/domain
relations with capture-safe substitutions and bounded work, while reproducing
the same keys from the consumer's independently spelled formal need? This is
primarily a source/spec question, not a certificate or large benchmark task.

The minimal eventual controls are: alpha-renaming invariance; repeated-variable
distinction; private-definition versus expanded consumer query; exact altered
definition rejection; deterministic exhaustion/unavailability; and one real
index query among structurally diverse decoys. No replay of old catalog or
native correctness campaigns is justified by metadata-only changes.

If the richer keys do not distinguish plausible method candidates, or acquiring
definition views costs more than useful search saves, stop this seam. Prefer
existing exact shared-symbol search, package metadata or another specialist
index rather than expanding the reducer toward general proof search. Its
success criterion is a more usable, affordable unfamiliar-method discovery
step within the same trustworthy ordinary workflow—not a larger codebase or
another isolated test pass.
