# Post-handoff mathematical operability: one concrete coverage boundary

2026-09-23. Bounded read-only investigation by `post_handoff_math_gap`.
Canonical workspace guard passed. Source09, its installations/states and the
six-file local handoff remain frozen. No product import, Lean invocation,
network action, source edit or experiment was performed for this note.

## Recommendation

The most consequential **concretely identifiable mathematical admission
restriction in this inspection** is the exclusion of new nested inductive
families and every theorem/definition whose reached closure requires one.
An ordinary rose-tree datatype with a constructor taking `List Rose` is a
small representative. This is an actual code-level exclusion, not merely
absence of a broad-library benchmark. It belongs to the central ability to
contribute new reusable mathematical vocabulary.

This is a prioritization judgment, not empirical proof that nested datatypes
are the largest cost or most frequent obstacle for prospective users. A
more urgent measured common-case cost or continuation failure could properly
take precedence. Do not turn this note into a requirement for all of mathlib,
a new prerequisite for the already completed local handoff, or a claim that
source09 is mathematically useless.

The smallest useful next investigation is **one exact fresh source-level
coverage discriminator**, not another fold theorem or network catalog test.
It should establish ordinary Lean acceptance of the representative and the
actual product refusal boundary on the same source. Only after inspecting
that evidence should root choose between extending the canonical group model
and explicitly retaining this restriction. Merely deleting the guard is not
a safe repair.

## What is already established

The current source frontend imports the pinned `Init` environment for syntax,
macros and tactics, checks every overlapping declaration against the checked
inventory, then installs missing checked bindings. It does not treat library
imports as mathematical authority. `AgentClient.lean:160-195` implements that
overlay; `:197-243` elaborates and captures a selected root's reached closure.
The public contribution pipeline is five steps: source capture, canonical
compilation, fresh replay, inverse export, second fresh replay
(`py/checking.py:513-522`).

There is positive evidence of real mathematical use, not only fixtures:

- `experiments/lean-library-interop/RESULTS.md:7-30` records actual pinned
  `Fin.castLE_castLE` extraction, complete private-helper/proof-bearing
  definition closure, and a successor with two genuine acquired-theorem
  applications. The independent audit's `:149-161` explicitly does not
  qualify new external groups, arbitrary recursive families, attributes,
  instances, notation, or a larger library. `Fin` itself was already seeded.
- `experiments/operator-onboarding-01/QUALIFICATION.md:27-52` records the
  ordinary-API D1/Beta/Alpha reciprocal chain. The Beta and Alpha mathematical
  audits inspect substantive proof-body use and fresh receiving acceptance.
  This demonstrates operation on already available list/algebra vocabulary.
  The word “Nested” in `BetaNestedHom` refers to `List (List (List A))`, not
  introduction of a **nested inductive declaration**; these are different
  technical claims. See `ALPHA-MATH-AUDIT.md:34` for the actual list type.
- `experiments/lean-source-composition/RESULTS.md:68` states the supported
  external fragment as ordinary nonnested groups. Therefore “new inductives
  are entirely impossible” would be false; the exclusion here is narrower.

The final local support report already avoids broad-library claims:
`deliverables/2026-09-23-v1-local-candidate/RESULTS.md:217-253`. It is frozen;
this note supplements, rather than silently revises, that evidence.

## Exact static inability

Let `K` be the current checked context, `r` the selected root, and
`C_K(r)` its external reached declaration closure. The current capture path
has the following necessary condition for success:

> For every inductive record `I` in `C_K(r)`, `I.numNested = 0`.

The relevant code is in the frozen
`product-local/stage-census-source-09` tree:

| Boundary | Exact evidence |
| --- | --- |
| All reached external declarations must be captured | `native/AgentClient.lean:222-226` calls `collectExtension` relative to the checked bindings, after elaboration. |
| Nested capture is unconditionally refused | `native/AgentReplayCore.lean:50-54` traverses every emitted member and fails with `INITIAL_EXTERNAL_NESTED_GROUP_UNSUPPORTED` when its inductive `numNested != 0`. |
| Canonical group inventory also excludes it | `py/source_codec.py:405-410` requires the nested field to be zero; `:535-541` separately enforces the same source-group condition. |
| Receiver cannot simply admit it from another producer | `native/AgentReplayCore.lean:354-371` kernel-generates the group, rejects `numNested != 0`, and accepts only one ordinary `.rec` name per declared type. Auxiliary nested recursors fail `UNSUPPORTED_NESTED_OR_EXTRA_RECURSOR`. |
| Exact generated correspondence is intentional | `native/AgentReplayCore.lean:374-384` requires the generated inventory count and every record to match. Removing only the capture guard would not supply a sound complete mapping. |

The Lean metadata meaning is not conjectural:
`software/runtime/lean-4.34.0-windows/src/lean/Lean/Declaration.lean:279-282`
defines `numNested` as the number of auxiliary types generated for a
constructor argument `F T`, explicitly mentioning `List T`, `Array T`, and
`T × T`. `:325` defines `isNested` by `numNested > 0`.
The pinned library itself documents the representative form
`inductive T | mk : List T → T` in
`Init/Data/List/BasicAux.lean:235-237`.

Thus a source root directly defining, or actually depending upon, a fresh
nested group cannot pass this profile. The argument is conditional on Lean
producing the nested metadata that its own record documentation specifies;
this assignment has **not** run that source or observed a source09 nested
refusal. Do not label this as an executed negative result, claim a measured
cost, or promise that this named guard must be the first observed diagnostic.
An earlier source/resource failure may prevent the capture loop from reaching
it. That exact distinction is the reason for the bounded discriminator.

## Classification of adjacent limitations

| Concern | Current classification, not a blanket impossibility claim |
| --- | --- |
| New nested inductive families | Concrete capture/codec/receiver exclusion, with the exact seams above. |
| Ordinary new nonnested inductives and safe definitions/theorems | Implemented profile, with bounded historical evidence; not universal coverage. |
| `Init` ambient safe theorem reuse | Positive source-frontend evidence, and the older actual library-closure evidence above. Not restricted to only a hard-coded replay list. |
| Mathematical definitions triggering executable code generation | Documented workaround: `noncomputable def` (`API.md:147-151`). Historical `lcAny` failure and successful revised path are preserved in `software/qualification/context-native-02/OUTCOME.md` and `context-native-03/OUTCOME.md:5-11`. That workaround does not change an inductive's nested metadata. |
| New class/instance registration, notation and binder presentation | Not comprehensively qualified. Missing frontend metadata need not imply missing kernel mathematics: explicit receiving names and explicit arguments can suffice. A concrete failure must be demonstrated before calling this universally unusable. |
| Arbitrary mathlib imports or recursive definition families | Untested/unqualified breadth, not an established all-or-nothing v1 requirement. This note neither demonstrates an exact import failure nor authorizes downloading a library. |
| New axioms, unsafe declarations, excessive closure size | Intentional acceptance/resource restrictions. A valid Lean file may still be outside the declared foundation or budget; refusal is not evidence that its mathematical proposition is false. |
| External string literal | Another explicit capture exclusion at `AgentReplayCore.lean:54`; the historical `BadSorry` run encountered it before `sorryAx`. That security-control failure is not evidence of ordinary string-mathematics usability, nor the central pattern selected here. |

There is no documented identity-preserving nested-group workaround in the
inspected public API. One may encode a rose tree through a different mutual
tree/forest family, or use another mathematical representation. That can be a
legitimate local research choice, but changes formal declarations/identities
and requires conversion theorems to reuse results about the original datatype.
It does not preserve arbitrary earlier work automatically. No such encoding
was executed or qualified here. Extra agent prompting cannot make the current
receiver admit records that its explicit grammar refuses.

## Smallest decision-changing experiment, proposed only

Use a fresh, separately recorded allocation; keep source09 and all earlier
state unchanged. Root should review a finite harness and exact resource bounds
before any native launch. The representative source is deliberately only a
datatype declaration:

```lean
inductive Rose where
  | node : List Rose → Rose
```

1. Establish source validity and actual `numNested`/generated member shape
   with the pinned runtime, without adding axioms or rewriting the example.
   Bind source bytes, runtime and observed records. This is a representation
   diagnostic, not proof of usefulness or a new accepted contribution.
2. Submit those exact source bytes with root `Rose` through the ordinary
   selected product API in a fresh node. Record exact diagnostic, pipeline
   step, unchanged accepted head/no artifact, charges and process cleanup.
   A generic refusal is insufficient to attribute failure to nested groups.
3. Stop and decide. If the ordinary source fails for another reason, preserve
   that failure and diagnose it; do not substitute an easier source and call
   the nested case qualified. If the predicted unsupported-group refusal is
   observed, the code-level limitation is now an actual user-facing boundary.

This experiment adds no network, agents framework, ranking policy, ledger,
identity system or external library. It tests a fresh kind of reusable
mathematical definition rather than repeating the already passing fold chain.
Its success criterion is **accurate diagnosis**, not treating a refusal as
release progress by itself. Stop after one discriminator and a consequential
implementation/scope decision; do not create an indefinite series of red gates.

If root selects support afterwards, the smallest meaningful completion is not
“the source parses.” It is faithful nested-group capture and generated-member
identity/correspondence, fresh data-only receiver acceptance, inverse replay,
and a downstream source that actually uses the received datatype's constructor
or eliminator to publish a further checked result. This would extend the real
agent contribution/reuse loop. The architecture must still reject unexpected
generated records and keep explicit resource/foundation bounds. An encoding
change may need versioning; this note does not assume a backward-compatible
one-line fix.

## Source pins inspected

SHA-256 of the frozen source09 files read in this investigation:

| Relative file | SHA-256 |
| --- | --- |
| `native/AgentClient.lean` | `3843e9baa335e772db21ac127121b276426c4117f1ab508c21f30c04c15f185d` |
| `native/AgentReplayCore.lean` | `a9a9547ed4e302ca12618680ddf62bd790cc1706a86136115e928370bffc4855` |
| `native/BootstrapSupport.lean` | `c859d52fe9d1fcfefbfd4704bdb49d9590f4fead1fa1f1446758302c1e4c3e90` |
| `py/source_codec.py` | `b82ea3e644b39e0996865f01cba3536304f8d6397d1f4fcbc393bbe85f79426b` |
| `py/checking.py` | `13afa1fa31f58f273c0364b9679fd56400587f2977ea24bddd85aad9471f840b` |

These pins identify inspected code, not new behavioral qualification or full
runtime attestation. The full goal and next execution choice belong to root.
