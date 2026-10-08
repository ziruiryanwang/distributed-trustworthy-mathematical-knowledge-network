# CP-001C analysis: formal-native accumulation independent of human intention

Date: 2026-09-19.

Status: conceptual specialization of the reciprocal commons; no implementation, tool-capability benchmark, or formal verification result is claimed.

Question: can a decentralized commons autonomously accumulate and reuse formally verified mathematical objects without human-intent interpretation, a question-answering service, or an unsolved-task registry?

Answer: yes as an architectural possibility. Contributions, interfaces, derivations, counterexamples, residual obligations, retrieval requests, and checking outcomes can all be represented formally. A contribution is checked against its own exact mathematical judgment, imported under a receiver's policy, and used to generate further contributions. None of these operations requires knowing why anyone wanted that judgment, whether it answers a question, or whether it appears on a task list.

The latest v1 scope completely excludes human intention from knowledge recognition. It also excludes an informal-to-formal fidelity service, semantic reviewers for human questions, a Q&A completion service, and any in-system local or global unsolved-task registry. A worker may use temporary proof obligations as algorithmic state, but those are not outstanding human questions or network obligations.

The system boundary is the formal corpus service, checking, exchange, and receiver resource authority. Investigating agents are external clients. Human intention may influence what such a client investigates, and its private workflow may use natural language, prompts, private questions, or any other method. None becomes an input to the system's mathematical recognition predicate. The system does not prescribe an agent's internal architecture.

This removes a particular interface from v1: certifying that a theorem answers an independently intended informal question. It does not remove the meaning of the formal language, the choice of foundations, exact substitution and transport obligations, correctness of the interpreter, or the problem of generating useful mathematics efficiently.

## Corpus growth is the primitive operation

Earlier concepts permit a formal task linked to an informal parent through a fidelity contract. This v1 specialization instead makes independently checked contribution admission the primitive mathematical operation. No task has to exist before or after that operation.

For example, a contribution names its exact judgment

\[
j=(L,E,\Gamma,\varphi)
\]

and supplies evidence \(p\). Recognition concerns whether \(E;\Gamma\vdash_L p:\varphi\) under the exact admitted checking relation. There is no separate English sentence, requester, intention, completion flag, or research-goal parent whose approval creates that derivation.

A participant can explore available definitions and proofs, instantiate known interfaces, search for stronger or simpler results, construct structures, create conservative abstractions, or generate proof terms before selecting any conclusion. It publishes resulting candidate judgments and evidence. Local checks decide what has been derived; receiver policies separately decide what to reuse or retain.

Temporary search states can contain a formula to prove, residual holes, a countermodel search, or a finite generation objective. These are internal strategies, not a required task ontology. Operational jobs still allocate CPU, checking, network, and storage resources. The existence of a resource job does not imply a mathematical question submitted by someone.

If an artifact happened to originate in an attempt to prove a different proposition, that origin does not affect recognition. A valid derivation of \(Q\) is a derivation of \(Q\), whether or not someone once sought \(P\). Determining whether \(P\) was answered is outside v1 and must not gate recognition of \(Q\).

Possible future human adapters are outside this v1 specification. They need not be designed, represented as pending obligations, or anticipated in the contribution acceptance predicate.

## Three different claims

| Claim | What it establishes | What it does not establish |
|---|---|---|
| Formal acceptance boundary | Only formal evidence and exact local policy can create strict mathematical reliance | Agents or discovery tools might still require natural-language prompts internally |
| Formal-native commons | Every required mathematical network input/output and reciprocal operation has a formal interface; v1 has no human-intent field or task registry | It does not specify the internal representation of each contributing model |
| Observable formal-only worker | A worker can operate using formal states, formal action choices, and formal outputs, with no required natural-language intermediate messages or external translator | An interface test cannot establish that a neural model has no language-like latent representations or no mixed-language pretraining history |

V1 requires the second claim and accepts formal contributions from external investigating clients. The third is a possible research profile for a client, not a conformance requirement imposed on contributors or a component the system must implement. The first alone is weaker: a system that checks formal proofs but can only accept them through a human-question translation service still has a mandatory dependence that this v1 avoids.

No claim about an agent's inaccessible latent representation is needed for a formal network contract. Nor should a previous model's training provenance be mistaken for a present runtime dependency. Core requirements concern observable formal contributions, checking, and services. A client's private use of natural language is unrestricted by this contract.

## Formal information is not the same as proved information

A schema-valid formal conjecture can be false. A well-formed proof-search state can be unsolved. A floating-point ranking score can be formally encoded yet wrong or useless. A program can have exact syntax yet crash. A counterexample-shaped record can fail its witness conditions.

The profile therefore has at least three separate predicates:

\[
\operatorname{WellFormed}(x),\qquad
\operatorname{CheckedEvidence}(x,j),\qquad
\operatorname{HelpfulInLaterWork}(x).
\]

None implies the next without further conditions. Formal-native operation removes the need to interpret free-form mathematical prose; it does not turn every formal record into reliable evidence or productive knowledge.

More precisely, keep the following dimensions separate:

- **Verified derivability:** native evidence checks for a particular exact judgment under its stated logic and assumptions.
- **Locally usable knowledge:** the receiver's allowed foundations, assumption footprint, checker/incident state, and available closure permit the result to be used in further derivations.
- **Usefulness:** the artifact improves later mathematical work or representation under a declared measure; validity alone does not establish this.
- **Storage/admission:** the receiver allocates checking, indexing, or retention capacity; a valid judgment does not entitle a sender to that capacity.

Application-question satisfaction would be a further relation in a different product, but is absent from v1. Removing it does not collapse the four remaining dimensions into one Boolean. A checked theorem in an unapproved theory can remain a correctly classified external derivation while being inadmissible as a local premise. A valid tautology can be recognized while receiving no long-term storage allocation.

Similarly, a formally specified protocol is not automatically an implemented, formally verified protocol. This note defines paper-level contracts only.

## Exact formal objects

The network's mathematical content should be structured objects with exact immutable references, not strings whose mathematical interpretation requires a language model. In v1, admitted mathematical content is checked content. Unproved conjectures, heuristic drafts, private search objectives, and unfinished proof states stay in bounded ingress or external clients' workspaces; they do not form a persistent conjecture or task catalogue.

| Object | Formal contents |
|---|---|
| Logic profile | Grammar, judgment relation, inference/checking basis, version, and locally admitted trust assumptions |
| Environment | Exact declarations, axioms, universe information, permitted extension rules, and dependency closure |
| Judgment | Typed expression or formal relation and exact context; no requester or question parent is required |
| Derivation | Native proof object or independently checkable certificate for the exact judgment |
| Definition | Typed declaration and the evidence required by the foundation's definition/extension rules |
| Interface | Formal parameters, dependent assumptions, exported judgments, and checked instantiation conditions |
| Conditional theorem | A completed checked transformer from an explicit assumption telescope to a conclusion; its assumptions create no pending tasks |
| Counterexample | Exact claim, formal witness, and checked failure of the claim's required condition |
| Transport | Exact source and target theories, mapping, scope, side conditions, and target-checkable evidence |
| Certified transformation | A formally represented construction with checked preservation properties and exact side conditions |
| Certified exclusion | A checked theorem about an exactly specified bounded region; an ordinary failed search is not such a theorem |
| Retrieval query | Exact identifiers, typed patterns, symbol/type/dependency structure, or bounded formal predicates |
| Assessment | Exact objects, procedure, context, local policy/snapshot, result code, and scope |

The object grammar may contain arbitrary string literals as mathematical data. A theorem about finite sequences of Unicode symbols is still a formal theorem. Formal identifiers can be spelled `group`, `plus`, or `continuous` without becoming natural-language interpretation requests. Their binding comes from the exact declaration environment.

An unverified tactic, heuristic strategy, or ordinary failure trace is external client material, not established v1 mathematical content. A program can enter the checked corpus as a formal construction with precisely the properties its evidence establishes; merely encoding an executable does not certify its behavior or usefulness. Protocol assessment and retrieval records are operational data, not additional kinds of mathematical theorem.

The prohibited dependency is an operation such as "interpret this comment as the intended theorem" on the required path. A formal string being fed to an untrusted model may generate a candidate, but it cannot acquire proof authority from the model's understanding of that string.

## Syntax, elaboration, and semantic identity

### Kernel input rather than unspecified surface text

A surface expression such as \(a+b\) can refer to integers, matrices, polynomials, strings, or a user-defined operation. A source file can select hidden coercions, type-class instances, notation, universes, macros, or imported namespaces. Eliminating English prose does not eliminate these sources of ambiguity.

There are two sound conceptual paths:

- Exchange an elaborated native representation whose references, arguments, universes, coercions, and selected instances are explicit enough for the declared kernel.
- Exchange formal source together with the exact parser/elaborator profile and environment, and bind the contribution's claimed judgment and accepted result to the actual elaborated objects. The elaborator remains fallible unless independently trusted or verified; target-side kernel checking still enforces the final exact judgment.

The first is preferable for the base semantic identity. A readable source form can be an auxiliary formal representation. A pretty-printer is not a semantic oracle.

### Two identity layers

Use an exact identity for the formal mathematical payload and, when useful, separate descriptors for presentation or commentary. Schematically,

\[
\operatorname{FormalID}(m)=
H(\operatorname{domain},\operatorname{schema},
  \operatorname{logicProfile},\operatorname{canonical}(m)).
\]

The tuple is encoded with an injective canonical encoding and explicit hash profile; commas do not prescribe a particular wire format. The identifier binds exact declaration and environment references required by its schema.

A semantic object must not require an annotation service to resolve an identifier, disambiguate a declaration, elaborate a term, select an axiom policy, or discover a hidden proof obligation. A descriptor can link inert presentation data to an already exact object. V1 requires no explanation or interpretation of such data to recognize a derivation.

Do not promise a universal canonical representation modulo mathematical equivalence. Canonical byte serialization is tractable by design; deciding all useful equivalences or discovering a universally minimal theorem representation is a different problem. Independent formalizations can coexist and later acquire checked relations.

### Formal aliases and mutation

An alias such as `current_group_library` may help find a candidate environment but cannot be the final dependency of an accepted proof. Resolve it to an exact immutable environment first. Changing the alias later creates no change in what the old theorem meant.

A schema upgrade that changes the interpretation of a node in an abstract syntax tree must produce a new representation identity or an explicit checked migration. Formal-looking syntax does not excuse silent reinterpretation.

## Conditions for removing all mandatory natural-language dependence

### FN-INPUT: exact formal input suffices

For every core mathematical operation, its precondition and result type are determined by formal fields, immutable references, and explicit local policy. No free-text field is required to determine whether the operation is admissible, what judgment it attempts, or what evidence would satisfy it.

Human explanations are outside v1. Their absence must not make a complete formal contribution semantically underdetermined.

### FN-CLOSURE: the reciprocal loop is closed over formal objects

Let \(\mathcal F\) be the disjoint union of the versioned formal object types admitted by a profile. Every required network-facing mathematical transition has a declared relation over objects in \(\mathcal F\), local operational state, and resource bounds. Successful outputs are objects in \(\mathcal F\); failures are typed bounded outcomes rather than a request for an undocumented prose interpretation.

This does not require the system to implement an agent or candidate generator. External generation can be stochastic and may produce no contribution. The core requires a formal interface for submitted candidates and its own bounded checking/serving outcomes.

### FN-JUDGMENT: the certificate establishes exactly its claimed judgment

For a contribution claiming \((L,E,\Gamma,\varphi)\), recognition requires evidence for that exact judgment or an allowed checked relation that derives it. A producer cannot replace \(\varphi\) with \(\top\), add a hidden assumption \(\varphi\), or change a quantifier while retaining the same claimed endpoint.

If the producer instead explicitly claims \(\top\), a valid proof is a valid proof of that statement. It is not rejected because it differs from an unrecorded intention. Its usefulness and resource admission remain separate questions.

Adding \(\varphi\) as a new axiom and deriving \(\varphi\) supplies a derivation under that stronger axiom set. It does not supply a new assumption-free proof of \(\varphi\) in the earlier theory. V1's recognition and reuse rules must preserve that distinction even though they never consult human intent.

### FN-ORIGIN: intent and question origin do not affect recognition

Fix the exact evidence, logic, environment, local context, checker relation, and policy-relevant footprint. Changing the producer's private motivation, failed original objective, description of usefulness, or association with a question must not change the native checking judgment. Those data are not recognition inputs and are not represented in v1.

This does not prohibit changing operational treatment for a resource policy: a receiver can decline to fetch an object or choose a different storage allocation. It forbids confusing such choices with whether the exact supplied evidence establishes its stated judgment.

### FN-ERASURE: declared nonsemantic text does not affect the core

Let \(\pi_F\) project an external bundle or event history onto its exact formal fields, preserving formal identifiers, literal data, formal instructions, and all immutable semantic references. It erases only fields explicitly declared to be nonsemantic optional annotations.

Consider two executions supplied with the same formal projection, exact initial formal state, pinned agent/checker/model and policy profiles, random tapes, formal event order, and available resource/service schedule. If optional annotations are excluded before core ingress, or isolated so they do not change that schedule, require

\[
\pi_{\rm core}\bigl(\operatorname{Run}(X,A)\bigr)
=
\pi_{\rm core}\bigl(\operatorname{Run}(X,A')\bigr),
\]

where \(A,A'\) differ only in the optional nonsemantic material. The equation concerns the declared core projection, not rendered UI text or untrusted annotation logs.

For the optional observable formal-only client research profile, its generation inputs and actions would also satisfy this condition. A model that reads private prose to choose the next conjecture need not satisfy that stronger condition and remains a fully eligible contributor. V1 requires equality of checking outcomes for equal formal inputs, not equality of contributions generated by clients with different motivations. Private intentions can change which formal events arrive; that does not violate core noninterference.

Identical resource schedules are essential. Sending large annotation blobs through the same link can delay proof transfer even if no checker reads the blobs. Annotation exclusion, separate envelopes, or explicit isolation must support a scheduling-independent deployment claim. Semantic non-authority alone is not a bandwidth guarantee.

### FN-NO-CALLBACK: no mandatory translator or explanation service

Once a package's exact closure and local checker/profile inputs have been obtained, native replay makes no mandatory live callback to a natural-language interpreter, source author, registry, explanation service, or index. This strengthens the existing independent replay requirement in the relevant direction; ordinary fetch and freshness observations remain separate operations.

### FN-TRANSPORT: formal differences receive formal treatment

Any step from a source judgment to a different target judgment is an exact instantiation, a native inference, an accepted checked rewrite, or a certified scoped transport. "These formulas say the same thing" cannot be an unchecked network primitive, whether that assertion was written in English or emitted as a Boolean flag.

## Conditional proposition: a formal-native reciprocal network is possible

Fix an effectively represented formal system with a terminating checker for each finite candidate proof, finite explicitly represented contexts, and formal contribution/object schemas. Fix resource-bounded storage/transport operations satisfying the inherited local acceptance rules. Suppose local candidate generators accept formal corpus data and return finite formal candidates or typed failure.

Then the complete sequence

\[
\text{formal corpus}\to\text{formal retrieval/exploration}\to
\text{candidate judgment and proof}\to\text{native checking}\to
\text{formal package}\to\text{peer import}\to
\text{next formal derivation}
\]

can be carried out without a natural-language mathematics-to-formalization conversion.

Proof sketch: each arrow's inputs and outputs lie in the declared formal object universe; no arrow's precondition mentions an informal proposition, a requester, or a preexisting task. Finite composition preserves this closure. Formal correctness of the final root follows separately from the checked finite evidence-tree argument, not from closure of the input/output types alone.

One very weak existence witness is fair enumeration of finite proof candidates for the selected effective proof calculus, with each candidate checked and accepted ones retained under local policy. A proof-first enumeration discovers conclusions from accepted derivations; it needs no list of conjectures waiting to be solved. This shows that a language-free formal generation process is conceptually available. It gives no practical efficiency, useful discovery, finite bound for proving an arbitrary target, or useful retention policy. Many possible conjectures are unprovable in the selected theory; failed search is not refutation.

Useful symbolic solvers, theorem provers, formally represented search policies, or trained policies over proof states are more plausible workers. Their efficiency must be established empirically; it does not follow from the existence witness.

### An explicit run with no research-task objects

Start with a finite checked environment and admitted derivations. An exploratory worker selects two compatible existing derivations, applies a checked compositional rule or a proposed proof transformation, and obtains a candidate proof with an exact conclusion. The local verifier checks it, extracts its conservative assumption footprint, and records the derivation when it passes. The local retention policy selects a bounded package for publication. Another node fetches and checks that package, then uses it in another formally admissible construction.

Every node in this trace has a corpus and operational work allocations. None needs a requester, a task ID, a pending question, an informal parent, or a "solved" flag. A worker can internally create and discard proof holes during a transformation without exporting them as research obligations imposed on other nodes.

The minimal corpus state records exact mathematical objects, checked derivation relations, foundation/assumption profiles, current local reliance facts, and availability. Its immutable content set may grow when objects are retained. Current usability is not monotone under checker incidents, policy changes, or closure loss. These changes do not require erasing the exact historical objects or making the theorem logically false.

## What seed material is needed

A node needs more than a bag of axioms. It needs an exact locally available bootstrap package specifying:

- a supported syntax and foundational checking profile;
- a small independently interpretable verification implementation and its declared platform assumptions;
- permitted axiom schemas and declaration-extension rules;
- finite exact seed environments and definitions useful for intended domains;
- proof and certificate representations with bounded parser behavior;
- exact formal lookup, contribution, response, and package formats;
- resource and admission policies;
- local storage and import/export procedures.

Adding prechecked library closures makes work useful sooner; it is not a natural-language runtime dependency. Initial nodes can choose a finite formal library directly as a mathematical starting point.

There are two historical policies to distinguish. The practical policy imports existing formal libraries, many of which were originally written by humans or translated from informal mathematics. That history does not force later operation to use a translator. A stricter policy can build a new corpus from selected formal primitive declarations and formal derivations only. It loses existing library breadth and does not itself solve useful exploratory generation.

Neither policy proves that initial axioms are true in an intended interpretation. Choosing a logic and axioms is still a foundational decision. The fact that their encoding contains no English prose is not a consistency proof.

No online founder, maintainer, or privileged seed server is required once participants hold and can interpret their chosen exact bootstrap material. New participants still need a distribution path or offline copy, as in the existing bootstrap analysis.

## Heterogeneous foundations without natural-language translation

The network can be heterogeneous while remaining formal-native. It must distinguish network interoperability from mathematical interchangeability.

**Network interoperability:** nodes understand enough of a common envelope to locate, transfer, identify, and archive exact objects. A node can store a proof object in an unsupported logic as opaque candidate data without treating it as a theorem in its own logic.

**Mathematical interchangeability:** a receiver can use another logic's result only when it has an accepted evidence path into the exact target contract. A common envelope, matching notation, or shared natural-language name cannot supply that path.

Three architectures remain possible:

| Design | Formal-native status | Principal tradeoff |
|---|---|---|
| One initial native foundation | All inputs and outputs can be formal without translation | Simple checking/interface boundary, narrower initial coverage, common-mode checker/foundation risk |
| Multiple isolated formal islands with common object transport | Still formal-native; no automatic theorem import between islands | Broad archival participation, but some reusable mathematics remains inaccessible across foundations |
| Multiple foundations with certified scoped bridges | Fully formal source/target relations and target checking; no natural-language bridge needed | Bridge construction, side conditions, proof size, and validation cost can be substantial |

The concept should allow all three. Initial implementation scope can choose one native profile without pretending that a single axiom set captures every future form of mathematics.

For a checked transport \(m\) on source fragment \(D\), the relevant conditional form is

\[
S|_D\vdash\varphi
\quad\land\quad
\operatorname{TransportConditions}(S,D,T,m)
\quad\land\quad
\operatorname{TargetCheck}(m(\varphi),p')=\texttt{ACCEPT}.
\]

Then the receiver may rely on the target judgment \(T\vdash m(\varphi)\) when its contract admits the target assumptions and available closure. The transported theorem can differ from a superficially corresponding target theorem. In particular, a translation of a classical theorem into a constructive theory can change its logical form.

For same-logic theory interpretations, mapped declarations and used axioms require target justification. Cross-logic transport may also need treatment of inference rules, binders, universe levels, equality/computation rules, and effects on the conclusion. The current native profile checks the actual target evidence; a future metatheorem-backed translator requires its own exact implementation and trust contract.

A universal metalogic does not make these obligations vanish. Encoding an object theory can let a checker establish object-theory derivability. It does not, without additional assumptions, establish consistency of that object theory or truth of every encoded axiom.

## Formal-native discovery and usefulness

The discovery interface can operate on exact identifiers, type heads, symbols, assumption footprints, declaration dependency patterns, and typed matching variables. Checked definitional equality or bounded rewriting can support more powerful matches. Matching or normalization that exceeds its declared budget returns unknown or a bounded failure, not a conclusion that no result exists.

A trained ranker can consume proof states or formal expression graphs and produce bounded candidate scores. Its suggestions are advisory. Their meaning need not involve human prose. A network profile can also omit learned ranking entirely and use exact and structural indexes.

The difficulty of discovery remains. The same mathematical idea can have several formal encodings, representations, or abstraction levels. Searching only identical syntax misses much useful work. A later formal contribution may supply equivalence proofs, representation maps, simplification lemmas, or structural indexes that improve discovery without any language interface.

Temporary purely formal search objectives can include the following. These are possible worker strategies, not required task records or entries in an unsolved-question registry:

- solving a selected typed proof obligation;
- completing an explicit residual telescope;
- constructing a requested structure or witness;
- deriving a candidate generalization from a constrained formal template;
- removing a particular axiom from an existing result;
- finding a checked counterexample to a formal conjecture;
- constructing a bridge between specified interfaces;
- producing a shorter proof or a proof with a smaller checked dependency footprint;
- improving measured later derivation or library-maintenance performance under an explicit evaluation protocol.

Each objective needs its own success relation. For example, a shorter serialized proof is a measurable property of two representations, not necessarily a faster-checking proof. Removing one declared axiom requires checking the full transitive footprint, not merely deleting an axiom name from metadata.

Formal exploration does not imply a global definition of important mathematics. Agents choose which regions of the corpus to explore, which transformations to attempt, and how to allocate resources. An arithmetic progression of distinct tautologies may satisfy formal validity while contributing little to later useful work. Omitting human intention from recognition does not solve this economic and algorithmic selection problem.

Candidate selection, rarity, compression, assumption reduction, formal reuse frequency, and measured reduction in later proof construction/checking cost can inform local resource policy. None is a new truth rule, and none proves universal mathematical importance. An external evaluation may study later exploratory continuations without making a task suite or evaluation metric part of the live commons.

## A completely formal reciprocal handoff

The existing monoid/group/window example can be expressed without any natural-language protocol field:

- Node A publishes an exact monoid interface and a native proof of the concatenation/fold judgment.
- Node B submits a formal group-to-monoid instantiation, checks the imported judgment, and produces the prefix-product relation with its exact index conditions.
- Node C instantiates B's interface at the integer additive group and checks a formal recurrence for moving windows.

Descriptions such as "prefix product" are explanatory prose in this note. The actual objects need only exact definitions, typed variables, proof terms, and formal relations. The nodes do not need to agree on English names or explanations.

There are still substantive handoff conditions: the group inverse must be multiplied on the correct side; list slicing must have the same formal meaning; index bounds must be proved; and the target context must admit the required group/interface instance. These are formal-to-formal composition questions. They remain necessary even if the system never receives a natural-language sentence.

## Counterexamples to stronger claims

| Claim to reject | Counterexample or reason | Required boundary |
|---|---|---|
| No prose means no ambiguity | The same formal surface token selects different overloaded operations or implicit instances | Bind elaborated objects and exact environments |
| Recognizing a proof requires knowing its producer's intention | A derivation of \(Q\) was found accidentally while exploring unrelated formulas | Recognize the exact derivation of \(Q\); v1 has no intention or question-completion gate |
| A valid bridge can be replaced by a name map | Classical reasoning is imported into a constructive contract without accounting for excluded middle | Check exact scoped transport and target evidence |
| A formal record is reliable knowledge | The record is a well-typed but false conjecture | Separate well-formedness, proof checking, and usefulness |
| All formal statements will eventually be proved or refuted | Expressive effective theories have undecidable and, under suitable consistency assumptions, incomplete theoremhood | Return bounded outcomes; no universal decision guarantee |
| Starting from axioms solves mathematical meaning | A chosen inconsistent axiom set derives every proposition | Keep derivability, consistency, and interpreted truth distinct |
| Removing descriptions preserves runtime performance automatically | Annotation traffic saturates the same link used for proofs | Exclude or isolate traffic under an explicit resource envelope |
| Formal worker I/O proves no language-like cognition | A model can emit formal tokens after mixed-language pretraining or inaccessible latent processing | Specify observable behavior, not unverifiable internal psychology |
| A formal-only worker must use an LLM | Symbolic enumeration and proof-producing algorithms need no LLM | Keep the worker interface model-independent |
| A neural model over ASTs will efficiently generate useful new mathematics | It can repeatedly emit trivial or irrelevant checked statements | Require empirical evidence of downstream mathematical benefit |
| Formal byte identity equals mathematical equivalence | Equivalent algebraic structures have different encodings and IDs | Preserve separate checked equivalence/transport objects |
| Every future foundation can be added by accepting its advertised checker | A malicious or unsound checker accepts arbitrary claims | Local admission of a new profile is a separate trust decision |

## What cannot be eliminated by this design choice

The profile avoids natural-language mathematical translation as a required computational stage. Several other interfaces remain unavoidable.

The parser interprets bytes as formal syntax. The checker implements a judgment relation. The logic and axiom policy determine what that relation permits. A semantic truth claim relates formal expressions to a mathematical interpretation. Hardware and software execute the procedure. A receiver chooses exploration and admission policies and allocates resources. None of these interfaces is made correct merely by refusing natural-language input.

An interpreter or kernel can be verified inside a stronger or different formal system, and independent checkers can reduce implementation risk. Those steps move and clarify the trusted boundary; they do not produce unconditional self-certification of every foundation and every implementation.

The architecture should therefore make the narrower, useful claim: no informal mathematical proposition needs to cross a mandatory translation boundary in the reciprocal core. It should not claim that formal syntax eliminates semantics, interpretation, foundational choices, or all sources of error.

## External client capability versus core architectural possibility

This note proves no claim about how well an available LLM operates on raw formal syntax, typed expression graphs, proof states, or certificate objects. It does not assert that a particular model can autonomously maintain a large formal library, choose valuable new conjectures, or invent useful abstractions without prose scaffolding.

The core architecture need not depend on those capabilities. It accepts formal contributions from external symbolic provers, decision procedures with certificates, formal program synthesis, humans directly constructing formal terms, trained policies, or hybrid agents. All conforming contributions satisfy the same formal boundary. Any client can privately use natural-language reasoning; no such process enters the core recognition relation.

For a separate research experiment on an observable formal-only client, possible contracts would specify the following. They are outside the normative system boundary:

- formal observation vocabulary and exact environment access;
- formal action vocabulary, action bounds, and side effects;
- whether arbitrary tactic programs are allowed and how they are isolated;
- proof-state and residual-obligation representation;
- the formal generation and evaluation signals;
- declared model/version/randomness and resource policy;
- typed handling of unsupported states or exhausted budgets;
- absence of required calls to a prose planner, translator, or explanation service.

Such clients can later be compared with clients that use private prose, without weakening the formal network interface. A positive result for the latter does not establish equal efficacy for the former. Neither client design is compulsory, and both can keep private questions or search state outside the system.

## Proposed conceptual decisions and remaining obligations

V1 should make corpus extension through formal-native contributions the normative base. Every recognized derivation states its exact mathematical content and assumptions independently of human intention. Every contribution offered for formal reuse supplies its exact formal package and required closure. Human explanation, informal fidelity, question completion, and a research-task registry are outside v1, not optional gates awaiting satisfaction.

Before implementation, resolve:

- the exact separation between kernel objects, formal surface syntax, and optional annotations;
- which elaboration choices are explicit in the authoritative representation;
- the smallest practical formal contribution/action/lookup language;
- whether the initial profile admits one foundation or several independently checked foundations;
- the precise contract for adding new checker profiles without creating remote code authority;
- typed partial completion with dependent substitution into the resulting target;
- the certified scope of normalization, matching, and representation bridges;
- a finite portable seed library and its replay/assumption profile;
- a three-generation formal contribution trace with no hidden translation callback in the core, without restricting external clients' private workflows;
- exact text-erasure tests and their resource-isolation assumptions;
- a formal representation of local exploration/admission policies without a task registry or a universal measure of mathematical importance.

Optional later client research can ask what observations would establish useful formal-only agent performance rather than merely syntax compliance. Such an experiment is not an implementation prerequisite for the corpus or a requirement imposed on its contributors.

The proposition that this architecture is possible is substantially easier than the hypothesis that external investigators interacting with the commons will generate useful mathematics rapidly. Keeping the two separate allows the system to remove a fragile mandatory interface while preserving an honest research program for the difficult parts.

## References and relation to earlier notes

- [Reciprocal commons concept](../../spec/RECIPROCAL-COMMONS-CONCEPT-v0.md): native checking, portable closure, policy-relative reliance, open profiles, and producer independence.
- [Reciprocity and composition analysis](CP-001C-reciprocity-analysis.md): explicit contexts, dependent interfaces, partial completion, foundation transport, and the three-generation example.
- [Decentralization analysis](CP-001C-decentralization-analysis.md): replaceable bootstrap, external-service independence, and receiver resource authority.
- [CP-001A](../checkpoints/CP-001A-autonomy-first-cooperation.md): autonomous work and optional shared goals.
- [CP-001B](../checkpoints/CP-001B-distributed-corpus-and-global-status.md): exact external memory, formal/structural retrieval, and learned-component non-authority.

These references were used as conceptual inputs. No new claim of support in a specific current model, prover release, or network implementation is made.
