# VIEWS1 proposal: bounded local query-view expansion

Date: 2026-09-20. Status: concept proposal for independent review, not a selected release profile or executed result. No implementation, executable model, native replay, extraction, test or benchmark. This note introduces no wire schema, opcode, remote proof-search service, mandatory research task or central scheduler.

## Question and deliberately small answer

Can an investigator use its known interface B to discover an unfamiliar interface A and then find a useful theorem stated over A, without receiving the answer's theorem or adapter IDs in advance?

Select one optional local heuristic, **VIEWS1**, for a small equality fragment. It searches existing B-domain features for map and preservation/reflection candidates, proposes at most two image-equality views, and queries those views through ordinary candidate services. Any result is brought back to the original problem only by complete native checking and explicit BRIDGE1-style transport. Unchecked headers can guide search; they cannot supply a map, preservation law, reflection law or proof.

The motivating seam is recorded in the [reciprocal-operability review](../reciprocal-operability/next-gap-audit.md). Existing [STRUCT2](../../../notes/analyses/CP-001G-structural-retrieval.md), [BRIDGE1](../../../notes/analyses/CP-001G-interface-bridges-and-applications.md), PI1/native acceptance, source-scoped acquisition and current-use guards remain unchanged. VIEWS1 chooses a finite client schedule where those contracts previously permitted many possible heuristics. It does not claim to be the only route through those interfaces or to prove that their other heuristics fail universally.

## Supported local problem fragment

The caller supplies:

- One exact adopted FoundationID F and locally qualified STRUCT2 ExtractorID E.
- An exact checked local context Gamma, including its telescope order, actual term meanings, coherent evidence interpretation and current policy/incident guards.
- A fixed closed data carrier `B : Type 0`, represented in this first fragment by a rigid monomorphic native type constant, and a fixed closed native definition or opaque constant `op_B : B -> B -> B`.
- Between one and four exact locally checked atomic terms `b_i : B` in Gamma. They may be variables or already constructed local values. Their identity includes Gamma; identical de Bruijn indices in another context are not the same atom.
- A well-formed desired equality `Eq B t u`, represented by two finite trees over the atoms and op_B as below.
- At most two explicitly owner-chosen candidate-service contacts, admitted query disclosure, and one finite parent investigation allocation.

The local tree grammar is

`e ::= Atom(i) | Bin(e_left,e_right)`.

`eval_B(Atom(i)) = b_i` and `eval_B(Bin(l,r)) = op_B (eval_B(l)) (eval_B(r))`.

Both input trees must have a Bin root. Together they have at most 63 nodes, each has depth at most four with leaves at depth zero, and there are at most four distinct atom references. The supplied equality must have exactly these interpreted operands. Initial reification uses bounded exact syntax comparison, not arbitrary definitional unfolding, equivalence search or recognition from printed names. The actual goal and atom terms must already be well typed under Gamma.

This narrow fragment excludes polymorphic unassigned universes, dependent maps, unfilled class arguments, multiple primitive operations, arbitrary dependent predicates and unbounded rewrite normalization. Those remain ordinary mathematical constructions outside this VIEWS1 procedure. UNSUPPORTED_LOCAL_FRAGMENT is a limitation of the heuristic, never a claim that the mathematical problem is impossible.

No input names A, an A operation, a particular map, preservation/reflection proof or the eventual useful A theorem. Known contacts and B's exact local heads are inputs, not hidden answer identifiers. The positive paper fixture below fixes a favorable finite consulted corpus only for explaining the trace.

## Exact candidate signatures

The first profile recognizes only these signatures, with no extra parameters or omitted premises:

`f : B -> A`,

`h : forall x y : B, Eq A (f (op_B x y)) (op_A (f x) (f y))`,

`r : forall x y : B, Eq A (f x) (f y) -> Eq B x y`.

Here A is another closed monomorphic rigid data-type constant of Type 0, and `op_A : A -> A -> A` is another closed native definition or opaque constant. A need not be definitionally equal to B. Neither map direction nor nominal type similarity implies r. Reflection is precisely the required equality-reflection proof, equivalent here to an injectivity witness for this exact f.

The map target is a definition or opaque declaration. The h and r targets are theorem judgments with exact proof/replay alternatives. Earlier type/dictionary/universe parameters are not guessed: a generally useful polymorphic declaration that has not already been specialized into this fixed closed signature is outside the selected matching fragment. A later richer profile can investigate instantiation separately.

### Effective declaration type without changing object identity

For a theorem judgment, first derive a receiver-local **effective declaration type** from its actual stored ordered context telescope Delta and conclusion C: conceptually `Pi Delta, C`. The matching binder sequence consists of those exact telescope entries followed by any syntactically leading Pis in C. Preserve every dependent type, its original order and de Bruijn scope. A binder stored in Delta is not absent merely because C contains no corresponding Pi node. No hypothesis is dropped, reordered, inferred from a source name or installed as a new axiom.

For a definition/opaque map, use its actual ordinary declaration type. In either case, all universe parameters must already be fixed as required by this monomorphic fragment; no omitted carrier/dictionary/earlier argument is inferred. Deriving this local view does not rewrite the canonical Judgment object, claim equality of different judgment encodings, change its ID/replay/support, or reconstruct source binder labels. Exact qualified declaration reconstruction still uses the original object and evidence.

The same effective-type rule applies to helper nomination **and to image-result theorem matching in Phase D**. Mere relocation of a legitimate binder between the stored telescope and syntactically leading Pis must not decide whether an otherwise identical effective signature matches this fragment. All stored telescope types, conclusion nodes and derived view work count against the one type-probe/matching budget; it is not a separate allowance per binder or split.

Helper recognition is bounded syntactic template matching on this actually obtained effective type:

1. Inspect only the exact stated effective binder sequence, using scope-preserving de Bruijn argument positions rather than source binder names.
2. Compare the B term and op_B/f references exactly. Match repeated argument occurrences consistently.
3. For f, extract the closed candidate A expression. For h, require that same A/f and extract its rigid candidate op_A reference from the exact right-hand shape.
4. For r, require that same A/f and the explicit equality premise and B equality conclusion. The equality premise is a binder, not a supplied proof or installed axiom.
5. Reject this template match if additional binders, metavariables, dependent output, casts, wrappers or unequal exact references occur. A timeout is UNKNOWN_TEMPLATE_BUDGET, not mathematical incompatibility.

This procedure does no arbitrary entailment, theorem proving, coercion installation or general higher-order unification. A header may pass the template and still lie about its object, type, native validity or support. Exact type/ref compatibility is independently checked after complete acquisition.

## Why the initial B token can expose the unfamiliar ingredients

Let `H_B` be the actual informative STRUCT2 HeadAtom of the checked rigid B type. The initial query uses the already selected BINDER_DOMAIN lift

`T_B = SHA256(ASCII("DTMKN-STRUCT2-TOKEN") || encode([E,[5,H_B]]))`.

This is the existing tag-5 domain-head token, not a new “map from B” index kind. Its possible cooccurrence with our three signatures follows literally from the selected extractor:

| Candidate type | Where B is inspected | Why tag 5 can enter the selected public tokens in this fixed short case |
|---|---|---|
| `B -> A` | Its single Pi domain is exactly B | That domain is within the last-16-domain selection and completely read. Tag 4 may emit the informative B/A input-output pair first; tag 5 for B follows in the existing eight-token input/output lane. |
| h's exact signature | Its two Pi domains are B | Both lie within the last 16. The terminal Eq head is not an informative input-output head, so it contributes no tag-4 pair with Eq. The completely read B domain emits tag 5, duplicates coalesce, and the short domain lane has room. |
| r's exact signature | Its first two Pi domains are B; its last is `Eq A (f x) (f y)` | The final Eq-domain head is noninformative; it does not erase the earlier B domains. Those are still within the last 16, inspected in nearest-result order, and emit the same tag-5 B token within the reserved domain/input lane. |

These statements require actual successful extraction under exact E: complete relevant head spines, no relevant traversal/emission/payload truncation, no failed extraction and the stated small types. They are not a guarantee that every semantically equivalent or longer helper emits this token. For instance, extra binders, a definitionally equivalent B wrapper, a truncated inspection, or an unsupported extractor can defeat the lane. A claimed descriptor containing T_B is only an untrusted discovery claim until its native binding/feature is independently checked when relied upon.

The B token therefore lets a client *nominate* unfamiliar maps and helpers without knowing A or their IDs. It does not tell the client which returned declarations have these signatures. That is the paid type-probe/filter stage below.

### Publisher-representation dependency and an ordinary defeating form

The table concerns an explicit specialized **effective native type**, not every ordinary library spelling of the same property. In particular, a closed theorem stored with type `Function.Injective f` need not have a visible B telescope/Pi domain at all. A proof body containing lambdas does not insert those binders into the indexed type. STRUCT2's raw domain inspection and beta/zeta companion do not promise arbitrary delta-unfolding of Function.Injective. Such a theorem is therefore not promised to emit T_B or match the selected explicit reflection template. Generic homomorphism structures, extra carrier/class parameters and B domains hidden behind raw beta/delta wrappers can similarly defeat this lane.

The initial query deliberately uses `patternOption=[0]`: the selected domain pattern can correspond to r's last equality-premise domain rather than B, even though its earlier B domains supplied the token. Adding a queried B pattern without accounting for that distinction could filter out the very reflection helper sought here.

A willing producer can separately construct, independently check, retain and index an ordinary specialized wrapper with the explicit required signature. That is a real contribution with its own exact computed statement/evidence IDs, source correspondence and publication cost. It is optional, not automatic library-wide preprocessing, a new metadata-truth assertion or a mandatory convention imposed on all publishers. VIEWS1 does not manufacture such wrappers while nominating headers. This first proposal selects no folded-form fallback query or local arbitrary unfolding policy; one would need its own exact existing-token path, bounded normalization/checking and cost analysis.

Accordingly, the positive fixture demonstrates one falsifiable narrow publication/coverage regime. It is not a claim of broad heterogeneous mathlib operability merely because common libraries contain injectivity or homomorphism facts in other forms.

## Local records and trust states

These are conceptual receiver-local records, not new serialized wire objects.

`ViewContext` binds F/E, exact Gamma/telescope, B/op_B/atoms, input trees and original equality, parent allocation generation and current disclosure/native policy guards.

`NativeHint` binds the exact descriptor d, target reference, replay R, bounded source observations/leads, obtained object/range references and candidate type bytes. It records whether those bytes are merely received, integrity-checked, type-template matched or actually native-qualified. A descriptor's type claim or a partial object prefix is never labeled a checked declaration.

`ViewProposal` binds one exact ViewContext, candidate f/h/r identities and replay choices, candidate A/op_A, its image-tree syntax, issued query predicate IDs and admitted counters. r may be explicitly absent. Changing a helper, replay, context or operation creates a different proposal; it does not replenish the parent allowance.

Keep separate evidence flags rather than one optimistic “valid view” bit:

- SPECULATIVE_SYNTAX: bounded templates and syntactic references only.
- CHECKED_FORWARD_LIFTS: actual f/h and the constructed lifts are checked/current under the receiver's compatible environment.
- CHECKED_REFLECTION: actual r is checked/current for that exact f/B/A.
- CHECKED_IMAGE_APPLICATION: an actual A-side theorem application proves this proposal's image equality.
- CHECKED_LOCAL_APPLICATION: the final composed term proves the original exact `Eq B t u` under Gamma and current guards.

Only the last flag solves the supplied local equality. A forward homomorphism does not imply reflection, and a proved image equality does not fill a missing r. Flags become unusable if their actual evidence/context/current-use guards cease to match; cached syntax may survive only as inert data.

## Type probes are ordinary paid acquisition, not a new endpoint

A type probe follows the chosen candidate's existing real native source path. It negotiates that source's actual capabilities/F and obtains its current public scope or freshly authorized holder-bound export. It reads only explicit permitted native objects/ranges needed to inspect the root and candidate type. There is no BROKER_TYPE operation, generic private CAS lookup, arbitrary URL fetch or implicit permission from a StructuralDescriptor.

Finding the type may require reading a replay root, proof-instance object, judgment/type object or other actual wrapper. This first fragment does not treat constructors as independent map roots. If obtaining a header requires large objects, those bytes and reads count; there is no universal cheap remote-header promise. An incomplete prefix may be inert ranking data but cannot establish its whole object's integrity or authorize further reads outside the actual scope.

Each probe is capped at 256 KiB of acquired payload and eight remote invocation attempts, also charged to the parent totals. For template recognition, at most 512 decoded native type/view nodes and depth 32 may be inspected, including the actual ordered judgment telescope, conclusion and effective-type construction. Larger cases yield TYPE_PROBE_NONDECISION. Parsing/decoding/authentication costs are included. The actual complete native closure/checking stage remains separate and larger only when explicitly reserved from the same parent allocation.

If the candidate came from an untrusted broker, its copied metadata is not native authority; the client recontacts an actual lead source. The BINDER_DOMAIN pattern/filter semantics of a qualified native provider are not inherited by a token-only broker. VIEWS1 uses token-only queries in this first profile, so it claims no absent broker pattern filtering.

## One finite schedule and hard aggregate counters

The following is a selected-for-paper-review local schedule, not a new wire quota or a promise of completion. All dimensions bind simultaneously. Existing per-call native, NET2, STRUCT2 and broker limits remain in force; a smaller actual grant may stop earlier.

| VIEWS1 episode dimension | Hard maximum |
|---|---:|
| Explicitly supplied candidate-service contacts | 2 |
| Actually contacted native source identities | 8 total |
| Map-composition depth | 1 |
| Candidate-service pages | 8 total: at most 4 B-domain pages and at most 4 image-view pages |
| Candidate rows decoded | 512 total, also under byte/CPU caps |
| Retained descriptors | 48 total: 16 map-kind, 16 helper-kind, 16 image-result slots |
| Native type-probe starts | 16 total: at most 4 map, 8 helper, 4 image-result probes |
| Proposed image views | 2 total, including abandoned/failed proposals |
| Local template/matching node-pair inspections | 8192 total |
| Complete evidence-acquisition/qualification starts | 8 total, including failed or interrupted starts |
| Constructed image/final application-check starts | 4 total |
| Remote invocation attempts | 256 total across query, negotiation, offers/control, probes, acquisition and retries |
| Concurrent remote/native work stages | 1 |
| All acquired network payload/setup/control bytes | 256 MiB total, of which candidate discovery uses at most 8 MiB |
| Local bookkeeping/type/view metadata resident bytes | 64 MiB, inside the next total rather than additional |
| Total admitted resident working set | 2 GiB, including actual native, metadata, staging/control and concurrent work allocations |
| Total local CPU | 120 CPU-seconds |
| Elapsed episode horizon | 600 qualified receiver-local seconds |

These are illustrative supplied local limits. They do not imply that a cold foundation, native environment or even one proof fits. Actual source service is independently funded by its owners. Already resident shared qualified state is counted under its real protection/physical resource accounting; it is not charged repeatedly as physically duplicated RAM, nor declared free or absent from the node's aggregate capacity. Complete native checking may require a smaller workload or larger explicitly authorized future experiment.

Eight complete starts do not imply every combination of two maps, two h/r pairs and four image results can be checked: actual counts and budgets stop the schedule first. Dependencies reconstructed inside a started closure still consume all actual bytes/CPU/memory; the word “one root” does not hide their size. Restarted attempts and alternative replay plans count again unless they are the exact inherited once-only invocation reconciliation.

### Phase A: known-domain collection

Issue the BINDER_DOMAIN token T_B to the at-most-two chosen contacts in supplied order. At a qualified native provider use the existing mode-6 query with queryMode BINDER_DOMAIN and `patternOption=[0]`; at a separately negotiated direct broker use the same required token in its token predicate. No desired A/type/theorem ID is transmitted.

Use round-robin paid page opportunities, at most two pages per contact and four total. Continuations retain the exact original snapshot/query meaning. A zero-progress page consumes an opportunity; stale/aborted work does not grant another free page. No automatic new contact or DHT crawl is selected by this profile.

Validate bounded row syntax and deduplicate exact d within this episode. Reserve up to 16 map-kind slots for definition/opaque targets and up to 16 helper-kind slots for judgment targets. Keep the first eligible rows in the actual deterministic contact/page/d order until a lane is full; discarded rows were still received/decoded and charged. This is a simple heuristic, not a source-fairness or useful-prefix theorem.

### Phase B: bounded type nomination

Probe at most the first four retained map-kind rows and first eight helper-kind rows under the same queue order. Probe reuse within this episode is permitted only for the same exact retained bytes/context; its inspection still consumes actual work. No native acceptance follows from the probe.

Apply the fixed syntactic templates above. Form candidate `(f,h)` pairs only when the inspected h type names the exact nominated f/op_B and extracted A/op_A consistently. Attach the first exact-template r for that f if one was nominated; otherwise record the missing reflection type. The template matcher has one global node-inspection allowance, not a fresh one per candidate pair.

Choose at most two pairs in lexicographic `(d_f,d_h)` order, with at most one pair per exact f in this first schedule. At most two resulting A/op_A image views are allocated. An apparently cheaper alternative, a second h or a hidden later valid map is not guaranteed an opportunity. Discarded/failed choices remain charged; this bounded policy makes no optimality claim.

### Phase C: image syntax and unfamiliar-theorem query

For a proposed pair, construct a local image tree:

`image(Atom(i)) = f b_i`,

`image(Bin(l,r)) = op_A (image(l)) (image(r))`.

The proposed equality is `Eq A (image(t)) (image(u))`. With unqualified f/h/A/op_A, this is bounded candidate syntax in the exact local record, not a declaration installed in the checked environment. No proof that it is equivalent to the B problem is asserted. The references must still pass the permitted typed syntax grammar before any query.

Both roots are Bin, so their proposed image heads are the same rigid `H_Aop = [0,constantRef(op_A)]`. Issue exactly the existing Eq operand-pair token

`T_Aop = SHA256(ASCII("DTMKN-STRUCT2-TOKEN") || encode([E,[2,0,H_Aop,H_Aop]]))`.

For native STRUCT2 use queryMode APPLY_RESULT and `patternOption=[0]`. For the direct broker use its ordinary token-only predicate. This token is justified as a **query proposal** even while its references are unqualified; the server receives inert syntax, does not fetch/adopt those declarations and supplies only candidate claims.

The stored desired A theorem must actually emit that token under its extractor for this lane to find it. A generic theorem with variable-headed operands, a differently encoded operation, truncation or a theorem reachable only by a transport not selected here can be missed. The proposal does not invent a FUNCTION_OUTPUT wildcard over unknown A or assume every related theorem has T_Aop.

Give each view at most one paid page from each of the two chosen contacts, for at most four image pages total. Retain at most 16 image-result descriptors across both views under the same bounded ordering/deduplication rules. Inspect at most four image-result types total, cycling views so an available candidate from each receives a first opportunity before a second from either. No second-level map/view expansion is selected.

Every new query is separately checked against the owner's actual disclosure policy. Authorization to disclose a B token is not automatically authorization for arbitrary derived views, identities, contacts or timing. A refused disclosure yields an explicit stopped stage, not another route around that policy.

### Phase D: narrow image-theorem matching

An image result is supported by this first matcher only if its inspected **effective declaration type**, formed from the actual ordered judgment telescope plus leading Pis as above, has at most four ordinary binders of exact A and then an equality over A whose operands are trees using only op_A and those variables, with the same 63-node/depth-four bounds. There are no additional premises, implicit arguments, unsolved universes or dependent binders in this fragment. The actual declaration's complete ordered argument vector is retained; legitimate telescope/Pi splits are not ignored or mistaken for extra assumptions.

Perform one-way syntactic matching of those two theorem trees against the proposed image trees. A theorem variable can bind an actual proposed A-side subterm; repeated occurrences must bind identical exact syntax under the same context. Matching both sides shares the substitution. This is incomplete, bounded matching, not definitional equality or arbitrary theorem application search. No automatic equality symmetry or unbounded rewrite sequence is selected.

Require that the resulting substitution assigns **every** declared effective binder, in its actual order. If a binder occurs in neither operand, this matcher does not guess an inhabitant: return UNASSIGNED_RESULT_ARGUMENT for that candidate and continue only within the remaining fixed probe/matching/check quotas. For example, `forall w x y z:A, assoc_equation(x,y,z)` leaves w unassigned and is not an executable VIEWS1 application, even if its other three variables match perfectly. A future policy could select a checked filler, but none is selected here. A complete speculative argument vector still requires actual type checking after qualification; a complete syntactic assignment is not a proof of its types.

An apparently matching substitution is still only a candidate. In particular, the A-side atoms `f b_i` are not known to be well typed until the selected evidence has actually been checked. A pattern resemblance cannot satisfy a missing r, a forbidden axiom footprint or a native conversion failure.

### Phase E: full checking and explicit return proof

For a shortlisted view/result, reserve an actual complete checking/acquisition stage for the selected f, h, r (if supplied) and result-theorem replays, counted within the eight-start limit. Their ordinary exact complete closures, source scopes, actual realization/PI1 composition, foundation and policy checks apply. It is permissible for one acquired closure to supply already-required dependencies of another; actual protected object reuse is counted, not assumed from names.

Then check actual types against the fixed signatures and recheck the proposed substitution/application through the ordinary local native/BRIDGE1 path. A mismatching untrusted header or illegal footprint cannot be relabeled “close enough.” If the actual combination needs unavailable support or an incompatible realization, report that exact obstruction/nondecision. Speculative queries already spent their resources even if this stage fails.

Once f and h are actually checked, construct forward-lift proof candidates by structural recursion on the small input trees:

- For Atom(i), `L_i : f b_i = f b_i` is reflexivity.
- For Bin(l,r), apply h to the actual B values, then ordinary checked congruence of op_A with `L_l` and `L_r`, obtaining `L_e : f(eval_B(e)) = image(e)`.

This uses ordinary Eq reflexivity, congruence, symmetry and transitivity terms under the qualified basis; any helper declarations used by their local constructor are part of actual checked support. It does not trust an executable peer tactic or install a rewrite axiom. The trees allocate at most 63 lift nodes per view; actual expanded native terms, serialization and checking must still fit the shared bytes/CPU/memory limits. No linear native-memory claim is inferred from that node count.

Let actual checked theorem application supply `q : image(t) = image(u)`. Form the candidate

`c = trans(L_t, trans(q, symm(L_u))) : f(t) = f(u)`

and, only with actual checked reflection, form

`r t u c : Eq B t u`.

Check the final complete native term at the original requested type under Gamma and current guards. This is BRIDGE1's existing final application/transport boundary, not a new mathematical rule. The exact original B result is returned only after this check. Abstracting local parameters and contributing the result later are ordinary separately admitted producer/export/publication operations; VIEWS1 does not auto-publish it or create custody.

If r is missing, the client may retain an actually checked image application and forward implication as useful partial work. It must return the explicit reflection obligation or a scoped missing-witness result, never CHECKED_LOCAL_APPLICATION. An empty finite reflection search does not prove no such witness exists.

## Accounting, lifecycle and outcomes

All query, nomination, helper matching, failed source leads, type reads, native acquisition/checking, view construction and final checking debit the same parent allocation. Child service offers, a second view, a new d, a changed helper, a broker snapshot or a fresh native lease supply no new local resources. Owner-authorized larger follow-up work is a distinct admission, not an implicit continuation of this bounded attempt.

Existing invocation tickets, exact result identities and uncertainty fences apply. The local retry policy may suppress/rotate eligible native leads within its own stricter caps, but cannot replenish these VIEWS1 totals. Broker NOT_SERVABLE/STALE_CURSOR/PARTIAL outcomes are metadata-stage events, not native-source mathematical failures merely because a peer key is shared.

The initial VIEWS1 profile selects no automatic restart/resume. On uncertain local recovery it stops and reconciles actual parent expenditure, in-flight obligations and retained stages under the existing contracts. A later explicitly admitted episode does not pretend earlier spent work was zero. Retained syntax can be reconsidered under new guards; old native acceptance/current-use flags cannot be copied into a different context. No timer, background search, automatic contact crawl or global task assignment follows from partial output.

The result record reports one principal outcome plus bounded exact partial records and actual expenditures. Useful distinctions are:

- UNSUPPORTED_LOCAL_FRAGMENT;
- ADMISSION_OR_DISCLOSURE_BLOCKED;
- NO_SUPPORTED_HINT_IN_SCANNED_SCOPE;
- TYPE_PROBE_NONDECISION or UNKNOWN_TEMPLATE_BUDGET;
- UNASSIGNED_RESULT_ARGUMENT for a candidate with an incomplete ordered application vector;
- SPECULATIVE_VIEW_ONLY;
- MISSING_PRESERVATION_OR_REFLECTION, with the exact unmet type and no negative-existence claim;
- CHECKED_IMAGE_APPLICATION_NO_REFLECTION;
- NATIVE_IMPORT_NONDECISION or INCOMPATIBLE_CHECKED_INTERFACE;
- EXACT_INPUT_REJECTED, scoped to the actual malformed/failed checking case rather than the theorem family;
- VIEWS_BUDGET_EXHAUSTED;
- CHECKED_LOCAL_APPLICATION at the exact original type/context.

No earlier status is silently upgraded to the last one. A valid A equality may remain worth returning as partial work without claiming that it solved the B opportunity.

## Genuine unfamiliar-interface success trace

This is a finite paper fixture, not extracted or compiled artifacts. Let B be a monomorphic record with one Nat field `value`. Let A be a different monomorphic record with a Nat field `value` and a Unit field `marker`. The differing descriptor shapes give genuinely different exact interfaces; source names alone are not being used to force nominal inequality.

Define op_B by adding its input values and constructing B. Define op_A by adding its input values and constructing A with the Unit constructor in its marker field. Define `f b` by copying b's value into A and choosing that Unit marker. Eligible ordinary proofs can establish:

- the exact multiplication-preservation h above, by the actual definitions/projection reductions;
- the exact reflection r, using equality of the A value projection and the B constructor/field interface;
- `ell_A : forall x y z:A, (x op_A y) op_A z = x op_A (y op_A z)`, using ordinary Nat associativity and checked record equality construction.

Those claims state a mathematical source recipe only. Actual exact group regeneration, dependency collection, proof terms, FoundationID, contents and native replay must still be qualified. The paper trace assumes successful complete actual checking and no hidden nonpermitted axioms. The published f/h/r and ell_A have the explicit specialized effective types described here, whether their binders occupy the legitimate judgment telescope or leading Pis; a folded generic library fact is not silently substituted. It does not assert `rfl` succeeds merely from printed source or that a private imported signature supplied proof bodies.

The investigator initially knows only F/E, B/op_B, three local B variables and the desired B-associativity equality. It receives two ordinary service contacts, not A/op_A or IDs of f/h/r/ell_A. Its original two trees contain five nodes each and depth two, inside the input fragment.

Assume the finite consulted provider snapshots contain f, h and r within the admitted B-token pages and selected lane/probe positions, with their successful short extraction as established above. Assume ell_A is within the admitted image-token page/result-probe positions. All actual source/qualification/current-use grants fit the stated episode. These are corpus/order/resource premises, not answer IDs given to the investigator or a guarantee over arbitrary larger libraries.

The actual information path is:

1. The investigator computes T_B from its own checked B and retrieves the candidate rows for f/h/r through an ordinary bounded page.
2. Paid type probes nominate f's previously unknown A and h's previously unknown op_A. r's exact reflection shape is discovered by inspecting the returned helper type, not supplied by the problem setter.
3. VIEWS1 constructs the image associativity syntax over op_A. Both operand heads are op_A, so it computes T_Aop without knowing ell_A's ID.
4. The ordinary image query returns ell_A. In the fixed short stored type, its Eq operand heads are completely read as op_A/op_A, so the existing tag-2 operand-pair rule emits T_Aop within the first conclusion lane. No source theorem ID or invisible special index was needed for that query.
5. Narrow matching binds every one of ell_A's three effective variables to `f x`, `f y`, `f z` in declaration order; there is no unused fourth binder or omitted parameter. Complete independent checking validates that ordered application and the actual f/h/r/ell_A evidence and compatibility.
6. The checked lift–image-application–reflection term proves exactly B-associativity and can become an ordinary new independently replayable contribution after separate publication/custody admission.

This is genuinely unfamiliar-A discovery at the defined client input boundary. It does not prove a utility gain: the investigator might independently prove B-associativity cheaply using Nat. That comparison belongs to a later fixed-budget evaluation. A useful specialized result need not be globally novel, and three successful syntax matches are not a compounding-growth measurement.

## Defeating trace: an honest constant map proves only an image statement

Let B be Bool with `op_B(x,y) = not (x and y)` (NAND). Let A be Unit with its constant Unit-valued binary operation and let f map every Bool to the Unit constructor. There is legitimate checked preservation h: both sides are that same Unit value. A associativity is also legitimate.

The input B-associativity instance at `x=false, y=false, z=true` has left side false and right side true. Thus a checked image equality exists even though the desired B equality is not valid under the intended ordinary Bool basis.

The same discovery schedule can find f/h and the A theorem. Speculative or checked forward image processing is allowed. It must not return the original B equality: the necessary r is missing, and a forged reflection proof fails the ordinary complete checker. For this explicit constant map on two distinct B values, a mathematical argument can show that equality reflection cannot hold; nevertheless the module's *empty finite search alone* does not establish that impossibility. Its operational result is an explicit missing-reflection/partial-image outcome, or exact rejection of a particular purported r.

This countercase is why VIEWS1 does not label an image query an equivalent problem, does not infer injectivity from the word “map,” and does not use successful A theorem checking as a certificate for the original B request.

An independent resource countercase also remains: an otherwise valid f/h/r combination can require more than 256 MiB of missing support or more than the supplied native working set. The attempt stops with a resource nondecision after its actual costs, even if its headers and token query were cheap. Speculative query wins are not evidence of affordable checked transfer.

## Claims, assumptions and exit criteria

### Conditional safety and exact return type

Assume qualified decoding/kernel/reconstruction, correct local accounting/state guards and actual complete compatible evidence for f, h, r and q. Structural induction on the finite input tree constructs each forward lift using h, reflexivity and congruence. Equality transitivity/symmetry then constructs c, and ordinary application of r yields the exact original B equality. The actual final native check remains mandatory: this paper typing argument is not permission to accept without it or to ignore REDUCE1 conversion behavior.

For arbitrary speculative headers, descriptors, views and broker transcripts, no CHECKED_LOCAL_APPLICATION can arise except through that unchanged native checking/current-use transition. Queries and template matches add only inert candidates. This preserves the conditional safety implication, not the set of attempts or their useful success rate.

### Conditional finite work

Every page, retained row, probe, view, match inspection, complete-check start, call, byte and constructed check consumes its shared finite allowance before work. No loop creates new map depth, a third view, a free restart or an uncharged helper search. Existing lower service/resource guards may stop earlier. The invariant bounds admitted work under its ordinary durable single-owner accounting assumptions; it does not prove that parsing/checking is cheap or that all numeric ceilings fit simultaneously.

### Heuristics and unproved outcomes

The two contacts, page order, lane quotas, syntactic templates, pair ordering, single-hop limit and two-view budget are local heuristics. Their superiority, recall, source independence, convenient wall latency and value over direct B reasoning are unproved. A longer adapter chain, different syntax, missing reflection, poorly ordered page, hidden body, incompatible proof realization or expensive cold closure may defeat them. No optimality proof is required to investigate this finite choice.

Before concept selection, independent review should trace the literal B-token and image-token premises; folded/generic publisher forms; effective telescope/Pi binding and malformed headers; exact helper matching and unused result binders; unknown A acquisition without answer-ID leakage; the constant-map case; partial/missing r; contextual/evidence guards; all phase counters and uncertain recovery; and the separation between metadata queries and complete native checking. Repair concrete contradictions or narrow the unsupported claim rather than hiding them behind future work.

Later qualification, only when separately authorized, should compare the selected finite policy against exact-interface/ordinary BRIDGE1 discovery under the same declared opportunities, solver state and total resources. Hide useful candidate IDs, include irrelevant/expensive/unsupported cases, charge probe and cold-check costs, and measure actual original-type checked applications rather than image-query hit counts. No executable evaluation is authorized by this proposal.
