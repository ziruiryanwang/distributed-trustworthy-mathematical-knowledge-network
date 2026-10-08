# CP-001G: checked interface bridges and usable applications

Date: 2026-09-20. Status: selected local-client concept with the [independent bridge audit](../audits/CP-001G-bridge-cross-audit.md) and its residual-context clarification integrated. No implementation, Lean execution, build, source extraction or benchmark. Frozen CP-001F remains unchanged.

## The missing operation

The [v3 specification](../../spec/OPERATIONAL-CORPUS-V3.md) correctly requires explicit checked adapters between genuinely different interfaces. It does not yet give a sufficiently concrete client operation for finding, composing and applying those adapters. Saying that two developments are about the same subject, or that the kernel will eventually check a result, does not supply that operation.

Select **BRIDGE1**, a bounded receiver-local client procedure over existing checked native declarations. It constructs candidate maps and actual application terms, reports any residual premises, and returns a successful application only after exact independent native checking. It uses no natural-language interpretation, public research goal or task registry. It is not a new remote proof-search service and does not execute peer programs.

There are two different problems:

- Multiple proof implementations under one exact mathematical interface require compatible evidence composition. The [proof-instance analysis](CP-001G-proof-instance-composition.md) owns that issue.
- Genuinely different nominal interfaces require maps and property transport, even when all their existing proofs are individually valid. BRIDGE1 addresses this second issue; it does not erase the first.

## Formal boundary: a map is not an equivalence claim

Fix one locally adopted exact FoundationID and a checked local context Gamma. Suppose

\[
\Gamma\vdash b:B,\qquad
\Gamma\vdash f:B\to A,\qquad
\Gamma\vdash \ell:\Pi a:A,\ P(a).
\]

Then ordinary application gives

\[
\Gamma\vdash \ell(f(b)):P(f(b)).
\]

This is useful mathematics without identifying A and B. If the local claim is Q(b), the result supplies it only if the qualified native checker establishes conversion between the actual result type and Q(b), or if an additional checked term supplies the needed transport, for example

\[
\Gamma\vdash t:\Pi x:B,\ P(f(x))\to Q(x).
\]

The final term is then `t b (ell (f b))`, with every implicit-looking parameter actually instantiated in the native term. Merely having a map B→A does not establish the transport theorem. A constant map can discard nearly all relevant structure.

The types and terms above can depend on fixed earlier parameters in Gamma. The initial graph-search edge is nondependent in its final subject argument: after its selected earlier arguments have been instantiated, f has type `B → A` with A not depending on that subject. An arbitrary dependent function `Π b:B, A(b)` remains available for explicit native application but is not silently treated as a fixed B→A graph edge. This restriction is on the generic search procedure, not on admitted mathematics.

Propositions are allowed as types when the ordinary native rules allow them. An existing proof P→Q can consequently be a checked map, but applying it still needs an actual local proof of P. A residual P is not installed as an axiom and is not registered on the network as an unsolved task.

## Exact local records

These are receiver-local derived records, not new trusted wire artifacts or extensions to the frozen Advisory2 whitelist.

`BridgeContext = [FoundationID,localContextIdentity,orderedUniverseParameters,contextTelescope,exactEnvironmentCompatibility,policyGuardBasis]`.

The local context identity binds the actual telescope, parameter order and referenced meanings, not a display name. Free de Bruijn variables with the same raw index under different contexts are not identified. A source alias, class name or embedding never supplies this binding.

`MapCandidate = [contextIdentity,sourceTypeTermID,targetTypeTermID,mapTerm,selectedEvidenceReferences,instantiationRecord,state,observedCost]`.

States distinguish UNCHECKED_HINT, WELL_SCOPED_CANDIDATE, CHECKED_MAP and CURRENTLY_USABLE_MAP. A foreign descriptor can nominate the first state. It cannot populate the latter states without the receiving node's complete evidence, checked term and current-use guards. A map term can reference a safe definition, checked opaque declaration or theorem, with its exact selected evidence; a group constructor is another native candidate only through its actual regenerated checked type.

`ApplicationCandidate = [contextIdentity,localInputTerm,candidateLemmaReference,mapPath,actualArgumentTerms,residualTypes,resultType,transportReferences,costObservation,state]`.

The exact native evidence backend determines compatibility and actual footprints. These records do not hard-code permission to union conflicting v3 witness maps or ignore a future proof-instance backend's context restrictions. Every chosen composition uses the actual selected mathematical profile and compatible native environment.

Remote distribution uses ordinary existing-content discovery, approved public-root acquisition and the separately specified [structural retrieval profile](CP-001G-structural-retrieval.md). The provider returns native identifiers and bounded features, not a script that asks the receiver to install an adapter. BRIDGE1 derives local map metadata from actual checked types after acquisition. Optional display aliases remain inert and cannot add a new advisory semantic kind by implication.

## A concrete bounded procedure

### Inputs and initial checks

The local caller supplies:

1. A checked context/environment under one exact foundation, an actual input term b with known type B, and a selected required argument type A from a candidate theorem or construction.
2. Any already supplied universe/earlier argument terms. Unassigned arguments remain explicit residuals; source implicitness flags are not assumed to survive canonical Native2 encoding.
3. Allowed evidence/axiom footprint and current local disclosure policy for any remote retrieval features.
4. A finite work/byte/memory/elapsed-time allocation, maximum map depth and candidate limits.

This is a private client request to inspect and apply existing objects. The protocol neither asks why the caller selected A nor treats A as an obligation for other agents to solve.

First try the direct checked argument b at A. A successful native conversion needs no nominal-type bridge. A resource timeout is UNKNOWN_CONVERSION, not a proof of incompatibility. The client must not spend unbounded normalization work to claim its search is complete.

### Candidate discovery and instantiation

If direct use has not succeeded, query the local map index and, when independently authorized, structural provider indexes for candidate function types whose input/output features resemble the required types. Input/output exact type heads, constructor/member selectors and other bounded formal features are routing/ranking keys; only the eventual checked function type makes an edge usable.

A candidate definition with type `Π uArgs, Π xArgs, B' → A'` is useful only after its earlier parameters are instantiated or reported as residual. A guessed typeclass dictionary is an ordinary missing argument until an actual checked term supplies it. Native declaration types, not remote binder labels, determine the dependent ordering of argument checks.

If a residual is deliberately retained as a formal parameter, first extend the checked telescope in its actual dependent order and derive a new context identity. The resulting conditional map is an edge only in that extended context, not in the original Gamma. Moving a result back to Gamma requires explicitly abstracting those parameters into a conditional theorem or supplying actual checked arguments. Neither a residual-list field nor an unresolved metavariable is a native assumption declaration.

The client may use bounded unification, local instance search, existing checked transport lemmas, or an LLM to propose those instantiations. These are untrusted construction methods. They cannot discharge a premise without a checked term or replace exact type compatibility with a feature match. Unsupported source metadata may reduce ergonomics but cannot force remote elaborator extension installation.

No record enters the usable bridge graph merely because an unverified header says it has the desired type. Inert header inspection can rank candidates before costly evidence acquisition; the state remains explicitly speculative until the exact complete closure and instantiated map term are checked.

### Search and composition

Select a small finite best-first search over actual candidate values and their exact types. A sample local policy uses map depth at most 3, at most 16 newly considered outgoing candidates per expanded state, at most 256 retained search states, at most four alternatives per exact type/context bucket, and at most 64 MiB combined term/candidate metadata. These are adjustable supplied local envelopes, not mathematical limits or proven optimal settings.

Priority can use estimated marginal evidence-acquisition cost, measured warm checking cost where available, exact target-type agreement, and locally observed useful applications. Unknown cost is not zero. The ordering is a heuristic and makes no shortest-path or optimality claim. A local model may replace it without changing native acceptance.

For a checked state `v : X` and checked map `g : X → Y`, construct the native expression `g v`, verify actual argument/result typing, and retain the resulting state only within its admitted limits. A path f₁,…,fₙ represents the explicit nested term `f_n (... (f_1 b))`; it does not add an axiom equating the endpoint types.

Candidate-state identity includes the actual produced term, its exact context and selected support/footprint, not only Y. Two paths to the same type can have different values, assumptions, required closures and usefulness. A four-alternative bucket may prune a useful path and must report that scope; it is not a completeness-preserving equivalence quotient. Exact repeated states may be deduplicated, but two arbitrary inhabitants of a data type are not proof-irrelevant.

Each state also binds the current evidence-profile interpretation. A changed foundation, relevant incident, unavailable closure or incompatible witness environment invalidates current usability even if the target type's displayed name is unchanged. Receiver-owned warm certificates may be reused only under the ordinary exact compatibility keys.

Cycles and self-maps cannot cause unbounded execution: every occurrence spends the same finite cumulative search allocation and depth/candidate quotas. A repeated request has independently admitted work and cannot inherit free execution from a cached discovery hint. The sample caps do not promise enumeration of all paths; the full 16-branch depth-3 tree already has 4369 vertices, larger than the 256-state envelope.

### Final theorem application and transport

Once a path yields a checked value a of the required exact type A, build the candidate theorem application using a and all other actual arguments. Check the resulting term and its type under the exact receiving context. Return `CHECKED_APPLICATION_AT_RESULT_TYPE` only for that established actual type.

If the caller also supplied a desired result expression Q, separately try bounded native conversion. If it fails or is undecided, search existing checked implication/transport candidates using the actual result-type features and Q's features. The same evidence acquisition, argument and footprint checks apply. A checked transport yields `CHECKED_APPLICATION_AT_REQUESTED_TYPE`; failure leaves the established result plus explicit unresolved correspondence, not a fictional success.

Returning residual hypotheses is useful. To turn them into an unconditional result, the external investigator must eventually provide actual proofs and resubmit the completed term. It is also legitimate to contribute the accurately stated conditional theorem under an explicit telescope; that is different mathematics, not proof that the original unconditional claim was met. The system does not assess the caller's intention in either case.

## Formal composition argument

Assume for each i that the same compatible checked context supplies `f_i : A_(i-1) → A_i`, and supplies `b : A_0`. Repeated application of the native function-elimination rule yields

\[
\Gamma\vdash f_n(\cdots f_1(b)\cdots):A_n.
\]

The proof is induction on n. The base n=0 is the supplied typing of b. For n+1, the induction hypothesis supplies a term at A_n; applying checked f_(n+1) gives A_(n+1). It requires actual compatibility and all argument conversions, not merely a path in an untrusted metadata graph.

If a checked lemma expects A_n and a checked transport has the stated implication type, the same application rule gives the final transported result. The actual evidence footprint is recomputed from the final selected native term/closure, including maps and transports. Logical composability does not imply equal footprints or affordable reduction cost.

The search algorithm's incompleteness does not weaken this conditional typing argument. Conversely, the argument does not establish search recall, branch compatibility, termination of arbitrary type conversion within a small budget, or existence of a useful map.

## Paper example: two record layouts, one underlying operation

Fix a carrier X. Let independently checked nominal groups A(X) and B(X) each carry a binary operation, a unit, and associativity/left-unit/right-unit proofs, but use genuinely different field orders or descriptors. Thus their GroupIDs differ, and an inhabitant of B(X) is not supplied directly where A(X) is expected merely because both are called monoids.

An ordinary checked definition f : B(X) → A(X) can construct an A record using B's exact projections and proof fields in A's constructor order. Its native body is the actual constructor application, not a record of alleged field-name matches. The receiver regenerates/checks the constructor and projection interfaces through the ordinary native profile.

Suppose a checked lemma for A expresses a fold-over-concatenation law using its operation and unit. Applied to f(b), it produces that law over A's projections of f(b). If the selected constructor/projection reductions make these definitionally equal to B's exact operation and unit, native checking establishes the B-form application without declaring A(X)=B(X). If that conversion is expensive or not definitional, an explicit checked operation/unit preservation lemma and the appropriate transport are required.

The resulting root can be an ordinary new theorem about B. It has its actual statement identity and proof support. It does not mutate the original A lemma, merge the GroupIDs or assert that every theorem about arbitrary A inhabitants transfers through f.

## Paper example with a necessary preservation hypothesis

Let A and B have binary operations star_A and star_B. Suppose f : B→A is injective and a checked proof h_mul supplies

\[
\forall x,y:B,\quad f(x\mathbin{\star_B}y)=f(x)\mathbin{\star_A}f(y).
\]

Assume the operation on A is associative. For x,y,z:B, repeated use of h_mul and A-associativity establishes

\[
f((x\star_B y)\star_B z)=f(x\star_B(y\star_B z)).
\]

Checked injectivity then gives B-associativity. Every step is an ordinary equality/congruence/application proof, and the finished proof is independently checked. Without injectivity, a constant homomorphism into a singleton associative algebra need not reflect associativity of the source operation. Without h_mul, an arbitrary injection says nothing about these operations. Neither hypothesis may be inferred from a familiar source type name.

This is not an invented need absent from practical Lean libraries. At the pinned mathlib commit, `Mathlib/Algebra/Group/InjSurj.lean:51–53` defines `Function.Injective.semigroup` from exactly an injective map and a multiplication-preservation proof into a semigroup. Its body explicitly uses injectivity and the repeated preservation/associativity equalities. The source's surjective construction at lines 316–318 transfers in the opposite direction under surjectivity and the corresponding homomorphism equation.

Those source observations justify a concrete family of bridge contributions and application patterns. They do not prove that our content-renamed exporter already supports that whole module or that its constructor/coercion metadata have been reconstructed. The pinned source is evidence of the mathematical route, not an executed commons replay.

## Interface reuse can reduce duplication without imposing a central ontology

The cheapest path remains voluntary reuse of an exact existing interface. BRIDGE1 makes divergence less terminal; it does not make every representation equally cheap.

For m interface variants, supplying all directed pairwise maps can require m(m−1) maps. For properties that genuinely admit transport through a chosen shared interface H, supplying maps to/from H can reduce the map stock to at most 2m. This comparison is conditional: maps may not exist, may lose needed information, or may yield much larger terms. A chosen hub is a reusable mathematical object, not a network authority or required global ontology.

Composition can increase proof depth, conversion work and selected closure costs. Keeping a frequently used directly checked composite map can be a valuable ordinary contribution; it need not be mathematically novel. Its smaller observed application cost is a scoped practical benefit, not permission to discard promised original evidence.

## Cost, cache and lifecycle contracts

The local client separately charges discovery, inert header inspection, complete evidence acquisition, map instantiation/checking, path search, final application/transport and resulting root retention. A small advertised map term may depend on a large library closure. Rank against the actual currently compatible local environment and distinguish cold from warm cost.

A candidate/conversion cache key includes exact foundation and interpretation, local context/telescope, input term/type, chosen map/theorem/transport terms, actual selected evidence compatibility, relevant policy and current-use guard basis. A syntactic candidate cache may survive as inert data after evidence becomes unusable; it cannot supply a current checked edge. Caching just source/target type names or just an endpoint pair is insufficient for dependent arguments, alternative values or footprints.

Proof checking, current local reuse, public contribution and durable custody remain distinct effects. The caller may use a checked temporary result privately and never publish it. Publishing a composite map or transported theorem requires ordinary public indexing/disclosure/retention admission; it does not create a standing global translation service. Cancelling a search cannot release evidence still pinned by another active use or custody obligation.

The sample local search envelope is not a throughput claim. A valid map can still make conversion expensive, and a high-yield candidate can exceed the allocated cold closure. Such cases receive precise resource or compatibility outcomes. They are not evidence that the endpoint mathematics is invalid.

## Required adversarial and usefulness cases

- A wrong field-order hint proposes a constructor map: only the actual checked constructor application can become an edge.
- An alleged A↔B equivalence is only a constant map: it cannot transport an arbitrary property back to B.
- Two paths reach the same type but different data values: endpoint-only deduplication must not erase the distinction or prove their equality.
- A proof bridge P→Q has residual P: the system cannot claim an unconditional Q without its proof.
- A same-named class belongs to another FoundationID or GroupID: explicit compatibility/conversion, not aliases, decides use.
- A valid map's closure contains an inadmissible axiom or conflicting evidence context: discovery remains a hint; no current edge is installed.
- A cache entry predates a relevant checker incident or losing its local complete closure: current use blocks independently of the stored search path.
- A cycle of valid maps fills the candidate graph: bounded state/depth/work prevents unbounded automatic search.
- A one-edge route imports a large cold hierarchy while a two-edge route uses local evidence: candidate ranking can choose either heuristically, but its recorded cost scope must be honest.
- An A theorem transfers to P(f(b)), but the requested Q(b) is stronger: return the established result and residual transport, not a renamed successful answer.
- The source-backed injective semigroup route is supplied with all actual arguments: the client must expose the resulting ordinary checked construction without requiring a natural-language intent statement.

## Integration and remaining question

BRIDGE1 gives a selected local operation where earlier checkpoints only required that some checked adapter exist. It keeps all mathematics inside ordinary exact native checking and all investigation choices outside corpus acceptance. It can improve practical cross-interface reuse without a solved universal equivalence problem.

It does not itself solve broad proof-instance compatibility or guarantee that a useful bridge will be found in the finite candidate window. The v4 integration selects the separate PI1 and STRUCT2 contracts with these exact context, derived-feature and evidence requirements. Practical library coverage and performance remain unexecuted qualification obligations, not reasons to weaken those requirements.

## Sources

- [Frozen v3 integration](../../spec/OPERATIONAL-CORPUS-V3.md).
- [Prior client/interface analysis](CP-001E-agent-reuse-and-discovery.md).
- [Pinned mathlib injective algebra transfer](https://github.com/leanprover-community/mathlib4/blob/5ed2965256430c3649e86755f9576b54eca72435/Mathlib/Algebra/Group/InjSurj.lean#L45).
- [Pinned mathlib surjective algebra transfer](https://github.com/leanprover-community/mathlib4/blob/5ed2965256430c3649e86755f9576b54eca72435/Mathlib/Algebra/Group/InjSurj.lean#L309).

The mathlib source portions were inspected read-only on 2026-09-20. No imported module, tactic, generated declaration or example was executed.
