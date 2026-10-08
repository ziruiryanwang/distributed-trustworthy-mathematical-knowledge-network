# CP-001G: STRUCT2, unknown-statement retrieval for local mathematical reuse

Date: 2026-09-20  
Status: selected deterministic concept profile, reviewed in the [structural audit](../audits/CP-001G-structural-cross-audit.md) and [profile audit](../audits/CP-001G-profile-integration-audit.md); no implementation, proof run, model execution or benchmark  
Scope: finding existing useful declarations when the caller does not know their JudgmentID

## Selected outcome and limits

Select **STRUCT2/1**, a concrete bounded native-syntax feature and discrimination-pattern profile. It supplies a decentralized route from a local formal expression/type to candidate providers and declarations, followed by bounded local instantiation and ordinary exact checking. It replaces the uninstantiated STRUCT2 suggestion in CP-001E for deployments explicitly negotiating this new profile; frozen E/F contracts are not edited.

The principal changes from STRUCT1 are conclusion-first inspection, explicit equality/iff operand views, exact constructor/projection selectors, input/output type-head features for functions, wildcard-aware bounded patterns, and a finite **FULL_FEATURE** publication scope. A node cannot claim this scope while publishing only its 16 most common coarse keys. No part is a public research task, persistent unsolved-statement record, natural-language intention model, or instruction to another node to invent a theorem.

The target is useful candidate recall at affordable declared cost, not complete mathematical search. All features and patterns are retrieval data. A candidate is usable only after its exact selected evidence is admitted and an actual dependent application/transport is checked. No index miss proves mathematical nonexistence or nonapplicability modulo arbitrary definitions, theorems or interface conversions.

## Source precedent and why it cannot be copied blindly

At Lean commit `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`, [DiscrTree.Types](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Meta/DiscrTree/Types.lean) defines constant/arity, projection, literal, free-variable, arrow, wildcard and other keys. [DiscrTree.Main](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Meta/DiscrTree/Main.lean) describes imperfect discrimination trees, ignores universe levels for retrieval, and uses wildcard branches when finding potential matches. Its `ignoreArg` uses native parameter information to ignore instance arguments and proofs while retaining some type arguments. Its reduction behavior depends on Lean reducibility and source metadata.

The pinned [LibrarySearch](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Meta/Tactic/LibrarySearch.lean) indexes declaration result types after `forallTelescope`, adds the two directions of iff, and excludes `[star]` and `[Eq,star,star,star]` from its primary tree because they match too much. It separately supports star fallback, symmetry and bounded candidate application; its default subsequent premise solver is `solveByElim` with a finite search-depth setting. The source is an engineering precedent, not evidence that our distributed retrieval has been executed or achieves the same behavior.

Native2 intentionally reconstructs explicit/default binders and does not accept source class registrations or arbitrary elaborator extensions. Consequently STRUCT2 **does not inherit** `isInstance`, source reducibility annotations, theorem names, private environment extensions, or remote `no_index` hints. It replaces names with exact native references and fixes its own limited syntactic normalization. Ordinary Lean tactics remain optional locally trusted producer/client tools, never network-controlled acceptance machinery.

## Exact profile identity

Allocate organizational type/schema `0x8123/1` for an inert ExtractorDescriptor:

`[1,FoundationID,EqRef,IffRef,limits]`.

EqRef and IffRef are the exact external native references from that foundation's locally qualified bootstrap inventory, checked against its actual intended equality/iff declarations. Familiar spellings or equal-looking types do not install another relation as equality. The fixed limits vector is

`[64,16,8192,64,8,128,16,16,1024,32,4]`,

in this order: maximum leading Pis peeled; inspected binder domains; total native-expression visits; expression inspection depth; focus/normalization variants; pattern nodes per variant; pattern depth; beta/zeta reductions per normalized focus; newly allocated normalization nodes per focus; emitted feature tokens per target; required feature tokens per query. These are fixed STRUCT2/1 constants, not caller-selectable semantics. A changed vector or algorithm needs another declared extractor profile.

ExtractorID is the ordinary typed ContentID of those exact descriptor bytes. The actual digest depends on the qualified FoundationID/role references and is not invented before bootstrap qualification. The algorithm is selected here completely; this missing release-time digest is not a permission to choose another extractor later. A node recognizes only locally installed STRUCT2/1 semantics with the exact supported descriptor. Receiving this descriptor cannot load software, install a plugin, run an arbitrary normalizer or adopt a foreign foundation.

Profiles are isolated by exact FoundationID and ExtractorID. The initial deployment selects the new PI1/rule-4 foundation F4 and does not admit old Proof/Replay objects as mixed evidence. A rule-4 foundation and an old rule-2/3 foundation do not share a structural namespace merely because their source names look alike.

## Indexed targets and their source types

STRUCT2 applies to these exact locally checked, public, retained targets:

- a semantic JudgmentID with a public selected ProofInstance and InstanceReplay (`0x0015/3`) rooted at `[4,ProofInstanceID]`, with that instance's exact target equal to the JudgmentID;
- a safe DefinitionID or body-checked OpaqueID with its InstanceReplay rooted at `[1,DefinitionID]` or `[3,OpaqueID]`;
- an explicitly selected external constructor member of a checked GroupID, using the qualified generated constructor type and InstanceReplay rooted at `[2,GroupID]`.

The target reference uses the existing **semantic** external native constant-reference grammar: `[2,JudgmentID]`, `[1,DefinitionID]`, `[4,OpaqueID]`, or `[3,GroupID,constructorSelector]`. In particular, a target JudgmentID is not replaced by its evidence instance ID. A group-local/bootstrap-local reference cannot escape its owner. Constructors are selected members, not fabricated independent kernel declarations. Recursors and other generated helpers can remain ordinarily accessible but are not automatically all STRUCT2 targets in this first profile. PI1's exact representative map and support accompany the selected InstanceReplay; a descriptor with a convenient-looking target cannot omit that support.

For a judgment, the effective declaration type is its ordered context telescope followed by its conclusion; the data can be inspected without copying a gigantic nested Pi expression. For definitions/opaque constants, inspect their actual checked type, not body or source annotation. For constructors, inspect only the actual generated inventory/type from checked group reconstruction. The same type-head mechanism therefore finds a function `f : B -> A`, an opaque function with that type, and a constructor returning A. It does not identify distinct B/A encodings by human labels.

Peel at most 64 syntactic leading Pis from the declaration's conclusion/type, recording their domains and scope. Judgment context entries are already an explicit telescope and need not be copied/peeled to locate its conclusion. If another leading Pi remains, mark OUTER_PI_TRUNCATED and treat that remaining Pi as the terminal inspected expression; do not pretend the ultimate codomain was found. Inspect at most the last 16 available binder domains, nearest to the result first. All judgment/peeled telescope variables are external parameters for the pattern view, regardless of whether their own domains were selected for inspection.

No kernel reduction or type inference is used to classify an argument as a hidden instance. All explicit native arguments remain in the underlying type and final application. The profile can ignore their detailed syntax in a retrieval pattern without asserting that they are mathematically irrelevant.

## Bounded focus views and normalization

The first focus is the terminal expression, also used as a function-output view. If its fully explicit raw application spine is exactly EqRef applied to three term arguments `[type,left,right]`, add left and right operand foci. If it is exactly IffRef applied to `[left,right]`, add those two proposition foci. Otherwise no equality/iff interpretation is invented. Application-spine inspection is within the same 8192-visit/depth envelope.

The fourth possible raw focus is the last inspected binder domain. Thus at most four raw foci exist. Each raw focus has one optional **deterministically attempted** beta/zeta-normalized companion, giving at most eight variants. Summary/selection focus order is terminal-raw, terminal-normalized, left-raw, left-normalized, right-raw, right-normalized, last-domain-raw, last-domain-normalized, omitting nonexistent/incomplete companions. Extraction work uses the phase order below, so normalizing a large terminal does not preempt all raw operand inspection. Equal expressions can share local immutable data but do not change either declared order.

Normalization performs ordinary capture-avoiding beta substitution and let elimination only, in leftmost-outermost order, restarting the preorder redex search at the root after each contraction. Application, lambda/Pi and let child orders are respectively `[function,argument]`, `[domain,body]` and `[type,value,body]`; projection has its base as its only expression child. It permits no delta unfolding, recursor/iota evaluation, projection reduction, eta reduction, arithmetic evaluator, class search or peer tactic. A companion is emitted only if a final complete search certifies beta/zeta normal form within 16 reductions, 1024 virtual newly constructed expression occurrences, and the shared visit/depth envelope. Logical fuel/allocation exhaustion sets NORMALIZATION_INCOMPLETE and emits no normalized companion, retaining raw features. An implementation interruption before completing the fixed extraction computation yields NOT_EXTRACTED; it cannot publish a hardware-timing-dependent prefix as the profile's deterministic output.

Normalized companions do not trigger another round of Pi peeling or relation-focus creation. A wrapper that hides the whole Pi/equality constructor can therefore remain a miss; this deliberate finite rule is testable, not an unspecified recursive normalizer. A later more powerful normalization profile would occupy a different namespace.

### Deterministic abstract work, distinct from runtime cost

All native-expression operations below use one virtual `READ` counter initially zero. A `READ` of one expression occurrence consumes one unit **even if the node has been read before, shares its DAG address, or its answer is cached**. Before the next read would exceed 8192, that operation reports VISIT_CUT without reading it, sets EXPRESSION_VISITS_TRUNCATED, and every later native read reports the same cut. Expression child depth is root 0; reading a child at depth greater than 64 similarly reports DEPTH_CUT without charging a read and sets EXPRESSION_DEPTH_TRUNCATED. Read failures give no invented head or relation recognition. Universe-level traversal is not an expression read; its decoding/hashing still has actual admission cost. The actual CPU, byte, memory and I/O charges remain additional to this abstract fuel.

Execute these phases, in order, with no implementation-dependent memoization changing their virtual charges:

1. Locate terminal/leading-Pi domains by reading each tested outer node. Inspect the raw terminal application spine by reading the terminal then its function children to recover the ordered arguments and head; a fully recognized Eq/Iff selects operands. Select the nearest-result last 16 domains by telescope positions. The same occurrence examined twice costs two reads. The fixed input's already validated telescope cardinality/position table is not a second unbounded expression walk.
2. For each raw focus in order terminal, left, right, last-domain, read its focus head spine; then take a preorder occurrence inspection to depth 64. At each visited occurrence, before its ordinary child traversal, attempt the operation-edge reads specified below: obtain its head spine and the head spines of its last eight actual arguments, in rightmost-first order. Record visited constants/paths for rigid-reference features. Pattern construction reads this same inspection record, not native nodes again. A cut becomes a pattern CUT and terminates only that subtree. If the global budget is exhausted, remaining scheduled focus patterns are the one-node CUT with no invented features.
3. Read head spines of the selected binder domains, nearest-result first; pair each known informative head with the raw terminal's previously obtained informative output head. These domain-head operations do not manufacture patterns for all 16 domains: the only full domain pattern in this profile is the selected last-domain focus.
4. For each raw focus in the same raw order, attempt normalization. A preorder redex search reads every tested occurrence in the child order above. On encountering an application, test its function node for lambda by an additional read; on encountering a let, contract that let directly. Capture-avoiding contraction uses the de Bruijn procedure below. Every substitution/shift input occurrence is read, and every returned constructed occurrence (including copies) counts toward that focus's 1024 virtual-node ceiling, whether or not an implementation interns it. After successful completion, run the same head/preorder/edge inspection on the companion. For a normalized terminal head, repeat phase 3 using the retained raw domain-head results, with no additional native reads. A failed attempt yields no features/pattern from its unfinished companion. Previously completed raw/normalized variants remain valid bounded extraction output.
5. Generate remaining fixed focus/relation-head and head-pair payloads from recorded results, select features, canonicalize/hash patterns and serialize the descriptor. There are no additional native reads. A paired Eq/Iff token combines either the two raw operand heads or their two completed normalized heads; it never silently runs a new normalization of the whole relation.

For substitution, use `subst(body,v,c)` with c=0 at the removed binder. On a de Bruijn variable k: keep it if k<c; if k=c, return `shift(v,c,0)`; if k>c, return k-1. Recurse through application/projection without changing c, through lambda/Pi domain with c and body with c+1, and through let type/value with c and body with c+1. `shift(t,d,c)` adds d to variable indexes at least c, recursing with the same binder-depth increments. Leaves/constants/levels are copied unchanged. Traverse/build children in the specified native order and then their parent. Both procedures charge each input READ and each constructed output occurrence. There is no cache exception and no unlimited DAG-expansion shortcut. Integer overflow, virtual fuel, node or depth failure aborts that companion; checked native expression index limits apply.

These rules deliberately permit visits spent repeatedly inspecting spines to exhaust extraction before every feature is seen. They specify reproducible logical truncation rather than claiming optimal use of fuel. A hash-consed, memoized or parallel implementation must produce the same tokens/flags/patterns as this abstract ordered procedure. General native serialization/admission bounds still apply before extraction; the 8192 counter is not a waiver for decoding an enormous literal or descriptor.

## Pattern grammar and compatibility

Each variant produces a canonical bounded postorder PatternDAG, at most 128 nodes and depth 16, with no unreachable nodes. Children precede parents and exact identical pattern nodes share representation. The node grammar is:

| Tag | Payload | Meaning |
|---:|---|---|
| 0 | `[0]` | WILD: an external telescope/query parameter, or deliberately unconstrained subtree |
| 1 | `[1,index]` | A de Bruijn variable bound inside this retained pattern focus |
| 2 | `[2]` | Sort, with universe expression erased for retrieval |
| 3 | `[3,constantRef]` | Exact external native constant/group-member/opaque selector |
| 4 | `[4,functionNode,argumentNode]` | Application |
| 5 | `[5,domainNode,bodyNode]` | Lambda |
| 6 | `[6,domainNode,bodyNode]` | Pi |
| 7 | `[7,typeNode,valueNode,bodyNode]` | Raw or unnormalized let |
| 8 | `[8,bucket]` | Natural literal: 0=zero, 1=one, 2=other at most eight magnitude bytes, 3=larger |
| 9 | `[9,lengthBucket]` | String literal length bucket: 0=empty, otherwise `1+floor(log2(byteLength))` |
| 10 | `[10,structureRef,fieldIndex,baseNode]` | Exact native projection selector and base |
| 11 | `[11]` | CUT: syntax omitted by the fixed extraction bound |

WILD does not assert equality of repeated external variables. Erasing their identities deliberately introduces false positives such as treating `x=x` as a shape candidate for `a=b`. Nested bound variables retain their exact indices. Universe expressions, exact large literal values and string contents are not mathematical equalities merely because their pattern representation is shared.

The canonical cut rule is depth-first preorder, using exact child lists `[function,argument]` for application, `[domain,body]` for lambda/Pi, `[type,value,body]` for let and `[base]` for projection, reserving enough one-node CUT children to close every opened constructor. Root depth is 0. When keeping the next complete node and the required child placeholders would exceed 128 nodes/depth 16, replace that subtree with CUT. A native inspection cut also becomes CUT. Then canonicalize the resulting finite tree to postorder sharing in that same child order. The number of nodes is a bound on this finite occurrence tree before sharing, so an exponentially expanded native DAG cannot escape the bound through pattern deduplication.

`Compatible(P,Q)` is the symmetric recursive relation in which WILD or CUT on either side matches any subtree; otherwise tags, exact selectors/bound indices/literal buckets and child compatibility must agree. Sort matches Sort. The relation ignores universes by construction. A finite deterministic comparison returns compatible, incompatible-under-this-projection, or UNKNOWN_WORK_BOUND. It is not Lean definitional equality or a higher-order unifier.

For a fixed raw focus whose relevant rigid syntax is retained, replacing external parameters by terms can only replace WILD-covered portions. The resulting projected instance remains compatible with the original pattern, absent an intervening normalization/representation change. This limited syntactic property motivates discrimination filtering. It does **not** establish recall after delta reduction, proof-dependent type conversion, different dictionary/projection encodings, omitted focus selection, feature truncation or an unknown checked interface map.

## Exact feature tokens and deterministic selection

A HeadAtom is `[0,constantRef]` for an exact constant application head, `[1,structureRef,fieldIndex]` for a projection head, or `[2,nodeTag]` for a nonconstant outer constructor. A rigid informative atom is one of the first two forms, excluding EqRef/IffRef themselves. A fully traversed application spine reports its exact head; a traversal cut reports no informative head, not a guessed constant.

Feature payloads are at most 512 canonical bytes and have these exact shapes:

| Tag | Payload | Purpose |
|---:|---|---|
| 0 | `[0,role,headAtom]` | Focus head |
| 1 | `[1,relationKind,side,headAtom]` | Eq/iff operand head; relationKind 0=Eq, 1=Iff, side 0/1 |
| 2 | `[2,relationKind,leftHead,rightHead]` | Ordered operand-head pair |
| 3 | `[3,role,parentHead,rightArgumentIndex,childHead]` | Rigid operation edge; index 0 is the last explicit argument, at most index 7 |
| 4 | `[4,inputHead,outputHead]` | Binder-domain/input to terminal-output head pair |
| 5 | `[5,domainHead]` | Inspected binder-domain head |
| 6 | `[6,role,constantRef]` | Exact rigid reference occurring in the inspected focus |
| 7 | `[7,outerHeadOrConstructor]` | Explicit broad/generic fallback |

Roles are 0=terminal/output, 1=Eq-left, 2=Eq-right, 3=Iff-left, 4=Iff-right, 5=binder-domain. RightArgumentIndex is a positional feature over the actual explicit application spine; it is not an assertion that earlier arguments are unimportant. The last-eight selection favors ordinary value operands behind type/dictionary arguments without needing erased binder annotations. Arbitrary partial application or unusual argument order can still miss an informative edge.

The exact emission rules, applied to completed recorded inspections, are:

- Tag 0: emit once for each focus variant whose head was completely read, including a noninformative outer constructor; only informative heads enter the directed conclusion lane.
- Tag 1: emit for each recognized raw Eq/Iff operand and each completed normalized companion when that operand head is informative. The kind/side is inherited from the original recognized relation, not guessed from a normalized token.
- Tag 2: emit the ordered pair for a recognized relation only when **both** operand heads are informative. Generate raw/raw and completed-normalized/completed-normalized pairs, with duplicate coalescing. An equality between two parameters therefore has no directed pair token.
- Tag 3: at each inspected application occurrence obtain its fully read head and actual explicit argument vector. If its head is informative, inspect at most the last eight argument head spines, index 0 first. Emit a payload only for each completely read informative child head. A nested application can also be visited as an occurrence later; its distinct arity/position payloads are subject to the same bound and deduplication.
- Tag 4: for each selected binder-domain informative raw head and each completely inspected informative terminal/output raw or completed-normalized head, emit the input/output pair. A dependent codomain head is allowed as a candidate feature, not certified as a nondependent bridge.
- Tag 5: emit each selected completely read informative raw domain head; do not unfold it or infer its ultimate class/type.
- Tag 6: at each visited constant occurrence in a terminal or Eq/Iff-operand focus emit its exact reference with that focus role, excluding EqRef/IffRef themselves. Its supplied universe vector is intentionally not part of the feature. Projection selectors use tags 0/1/3 and are not misencoded as constant references.
- Tag 7: if no informative tag 0/1/2/3 conclusion feature was generated, emit one fallback using the raw terminal's known head; if that head is unknown, emit no fallback. This feature is deliberately broad.

Tag 0 binder-domain and noninformative heads are inspectable local features but do not consume a public token lane; their public substitutes, when available, are tags 5 and 7. Only the selected public tokens define FULL_FEATURE coverage. No caller can enable an undeclared extra emission rule under this ExtractorID.

A token is

`SHA256(ASCII("DTMKN-STRUCT2-TOKEN") || encode([ExtractorID,featurePayload]))`.

Raw and completed normalized variants emit into the same token namespace and duplicates coalesce; the descriptor records which view/truncation states were used, not a false claim of universal normalization. A hash collision can add false candidates. The caller can recompute feature payloads from inspected exact syntax; no token grants equality or native acceptance.

At most 32 distinct tokens are selected per target through fixed reserved lanes:

1. Up to 16 conclusion/relation tokens. Order operand-head pairs, informative operand/focus heads, rigid parent/argument edges, then broad fallback; within each category use focus order, shallower occurrence depth, left-to-right native occurrence path and canonical payload bytes.
2. Up to eight input/output tokens. Inspect the selected last-16 domains nearest-result first; emit an informative input/output pair before its domain-head token, with canonical bytes breaking ties. No pair is emitted if either head is unknown/noninformative. This deliberately prioritizes a final subject binder over earlier carrier/dictionary parameters.
3. Up to four additional binder-domain tokens, in the same nearest-result order, not already selected.
4. Up to four additional rigid-reference tokens from the inspected terminal/relation foci, by focus order, depth, path and canonical bytes.

Deduplicate against earlier lanes; unused slots are not silently lent to another lane. If a generated feature cannot fit its payload bound, mark FEATURE_PAYLOAD_TRUNCATED and omit it; do not hash a truncated reference. A broad tag-7 fallback is added within the conclusion lane when no informative conclusion/relation token exists. Exact type identity is still accessible through normal native IDs and the separate exact-routing lane.

The finite traversal can emit up to eight operation-edge candidates at an application occurrence, plus its fixed head/reference/domain/pair candidates. Its temporary feature-generation budget is at most 32768 payload candidates and 16 MiB of canonical payload bytes, counted before duplicate elimination. Generate traversal-dependent edge/reference candidates at the specified occurrence, and fixed candidates at the end in ascending feature-tag order, then focus/domain order and canonical bytes. Before a next candidate would exceed either bound, stop feature generation, retain its preceding prefix and set FEATURE_ENUMERATION_TRUNCATED. Candidate payloads above 512 bytes instead set FEATURE_PAYLOAD_TRUNCATED and are omitted, with no prefix-byte truncation. Fixed visit/emission ordering determines this output. Actual memory/CPU interruption gives NOT_EXTRACTED instead of pretending that arbitrary work cutoff was a completed feature set.

## Descriptor and query contract

Allocate organizational type/schema `0x8124/1` for StructuralDescriptor:

`[1,FoundationID,ExtractorID,targetRef,anchorReplayID,sortedTokens,flags,viewSummaries]`.

The complete public descriptor is at most 4096 canonical bytes, at most 32 sorted unique 32-byte tokens, at most 16 sorted flag codes, and at most eight view summaries. `anchorReplayID` must have InstanceReplay type/schema `0x0015/3`, with the exact typed-root/target relationship above. A summary is `[role,sourceSelector,normalizationCode,patternDigest,patternFlags]`. SourceSelector is `[0]` for terminal type, `[1,side]` for recognized Eq/iff operands, or `[2,binderIndex]` for an inspected binder domain in the effective telescope; binderIndex is zero-based from the outermost explicit context binder followed by peeled Pis. NormalizationCode 0=raw, 1=completed beta/zeta companion. PatternDigest is SHA-256 of ASCII `DTMKN-STRUCT2-PATTERN` followed by canonical `[ExtractorID,patternNodes,rootIndex]`. Pattern flags are at most four fixed codes: CUT_PRESENT, EXTERNAL_VARS_ERASED, UNIVERSES_ERASED, LITERALS_BUCKETED, represented as codes 0..3.

Descriptor flags are codes 0=OUTER_PI_TRUNCATED, 1=BINDER_DOMAIN_TRUNCATED, 2=EXPRESSION_VISITS_TRUNCATED, 3=EXPRESSION_DEPTH_TRUNCATED, 4=NORMALIZATION_INCOMPLETE, 5=PATTERN_CUT_PRESENT, 6=FEATURE_LANE_TRUNCATED, 7=FEATURE_PAYLOAD_TRUNCATED, 8=FEATURE_ENUMERATION_TRUNCATED. Unknown flags or role/profile mismatches reject this schema. If the fixed descriptor cannot fit 4096 bytes, extraction does not claim this descriptor completed; a larger undeclared record is not sent.

Pattern bodies are bounded local index material, not new arbitrary CAS objects reachable through an ad. The public digest binds the view when a client independently derives it from the exact type; it is not a permission to fetch private index internals. Mathematical source type objects use their existing native public-root/export scopes. Constructor type reconstruction can require a checked group import rather than a nonexistent standalone generated-type object.

Negotiate capability `7=STRUCT2_1` through the existing reciprocal HELLO replies. Following the [exact profile/consumer binding](CP-001G-profile-and-consumer-bindings.md), this first code-4 deployment requires capabilities 3+7+8 for structural FIND_WINDOW; routing K4 additionally requires 5; FULL_FEATURE group operations additionally require 6. Capability 8 selects the exact new rule-4 native/evidence family and schema whitelist in that integration. A routing-only holder can understand these codecs without adopting/checking the mathematical foundation; a client cannot use negotiation as a substitute for its own adoption. No legacy native reader is sent PI1 evidence merely because it implements generic routing. Capability 7 enables the new descriptor/extractor grammar, ROUTE1 key kind

`[4,FoundationID,ExtractorID,featureToken32]`,

and FindPredicate `0x8102/3` mode 6:

`[6,FoundationID,ExtractorID,queryMode,sortedRequiredTokens,patternOption]`.

QueryMode is 0=APPLY_RESULT, 1=REWRITE_OPERAND, 2=FUNCTION_OUTPUT, 3=BINDER_DOMAIN. There are one to four sorted unique required tokens. PatternOption is `[0]` or `[1,patternNodes,rootIndex]`; a supplied pattern has at most 128 nodes, depth 16 and 8192 canonical bytes and obeys the exact postorder/share/no-unreachable-node grammar above. Refs must have the permitted typed semantic reference shape for this foundation/profile; the server validates that bounded syntax, not remotely fetching declarations to establish their semantics. No proof-instance reference appears in these semantic type patterns. All pattern refs remain candidate syntax; they cannot install a declaration or make the provider fetch an object. Query disclosure is locally authorized: even hashed structural features can reveal a subject through dictionary attacks.

Reuse existing FIND_WINDOW/service operation 10 with this predicate only after capability 7. The selected local posting list is the shortest required-token posting in the fixed public snapshot, ties by token bytes. Test the other tokens, then optionally compare the query pattern against the target's permitted view variants: terminal and iff-side views for APPLY_RESULT; Eq sides for REWRITE_OPERAND; terminal/output for FUNCTION_OUTPUT; selected stored domain views for BINDER_DOMAIN. The same descriptor may satisfy several views but appears once. A compatible iff-side result is labeled as requiring the other side as a potential premise, not an unconditional proof of the matched side.

Each page remains bounded by 64 descriptors, 1 MiB encoded bytes, 8192 posting inspections, 0.25 CPU-seconds and two wall-seconds, plus at most 32 descriptor pattern probes and 32768 aggregate pattern-node-pair comparisons. A work-exhausted comparison leaves that descriptor unprocessed at the next position; it is not counted as incompatible. Existing FIND_WINDOW snapshot/holder/lower-bound/cursor rules and explicit current-vs-historical scope apply. PatternOption absent is a useful cheaper token-only lane, not a secretly stronger matching guarantee.

The physical index may be a discrimination tree with wildcard branches or an equivalent bounded posting/filter structure; it must implement exactly this selected predicate and ordering/coverage semantics. No implementation-dependent tree heuristic may relabel a skipped matching row as completely processed. Remote results remain provider assertions until the receiver checks the bindings it relies on.

### New provider record, without a legacy tagged-union ambiguity

Use the integrated `ProviderAd 0x8022/2` with exact payload

`[2,providerNodeID,K,revision,publicContact,anchorPublicDescriptorCID,anchorReplayID]`.

The anchor descriptor has type/schema `0x8111/3`, and the replay has type/schema `0x0015/3`. Schema2 supports the explicitly integrated code-4 K0/K1/K2/K3 keys as well as K4 under capability7; it is not a K4-only record. For K4, the root descriptor's `structuralDescriptorOption` must be `[1,StructuralDescriptorID]` for the actual `0x8124/1` record supplying that feature. Its full signed record retains the 4096-byte maximum and common Ed25519 wrapper binding the exact typed record. `publicContact` is the frozen four-field `[nodeID,endpoints,nativeProfileIDs,indexKeys]` contact, with nodeID=providerNodeID, at most two sorted unique public endpoints, at most 16 sorted unique native profile IDs and index keys, and K's exact FoundationID in nativeProfileIDs. Under capability7 its indexKeys may include K4; old contact parsers are not sent such a record. Revision, authenticated-provider mutation authority, lifetime, actual byte/row accounting and receiver admission remain the existing ROUTE1 rules.

An honest publisher additionally checks the chain ProviderAd2 -> PublicIndexDescriptor3 -> StructuralDescriptor1: the last record has the same FID/ExtractorID as K4, contains K4's token, names the exact same anchor replay as the root descriptor/ad, and is currently public/native-eligible under that replay. The root/target relation must be the exact judgment/declaration/constructor relation specified above. The routing holder validates bounded wire/signature/type/key consistency but does not secretly fetch an anchor or import the evidence. A later client verifies the actual descriptor/token/target bindings and independently acquires the selected native closure. Neither signature nor token establishes theorem acceptance.

K4 routing is legal in cells, contacts and ProviderAd2 only after cap5+7+8, and grouped K4 rows additionally need cap6. ProviderAd1 never acquires an implicit new root/structural descriptor or PI1 replay alternative. Existing F4 exact/foundation/STRUCT1 routing uses the integrated PublicIndexDescriptor3/ProviderAd2/PI1 binding; frozen code-3 records retain their old reader. Existing generic-CID response fields can carry the new typed record only through this exact negotiated whitelist. `FindPredicate 0x8102/3`, mode6 likewise does not change schema2 predicate meanings. No old object gains new meaning merely from a friendly capability name. Mode6 page rows carry bounded StructuralDescriptor records inline, ordered by their own descriptor IDs; exact-judgment page rows instead carry PublicIndexDescriptor3. Snapshot/cursor state binds that record schema as well as the predicate/mode, so these universes cannot be silently exchanged.

## Decentralized FULL_FEATURE publication

Each provider selects a finite immutable local

`FeatureScope = [1,FoundationID,ExtractorID,orderedTargetRefs,emittedTokenUnion]`.

The target refs are sorted/duplicate-free; the token union is recomputed from **every successfully extracted target** in that scope under this exact extractor, sorted/duplicate-free. ScopeID is SHA-256 of ASCII `DTMKN-FEATURE-SCOPE` followed by the canonical payload. A failed extraction makes the proposed complete scope pending/incomplete; dropping the target requires a new explicitly smaller scope. FULL_FEATURE means all emitted tokens of the selected bounded extractor are supplied, not that all semantically useful properties were extracted.

Initial local coverage is at most 128 selected targets and 4096 distinct token memberships. The 32-token/target cap makes that union bound explicit before deduplication. Provider ads under K4 consolidate all matching targets at one provider: their anchor is one actual currently public structural descriptor/replay carrying that token. Multiple statements sharing a token do not create one provider route row per statement. The provider's FIND_WINDOW postings still contain the distinct target descriptors.

Four-copy target placement, adaptive shard cells/ancestor markers, actual group/row accounting and renewal economics are inherited from the exact-routing mechanisms. A larger or continually growing library needs explicitly supplied scope/index capacity and updated scopes; 16 coarse keys or 128 targets do not stand for all of mathlib. Status reports intended target/feature counts, extraction flags, placed/pending keys, snapshot/renewal ages and actual service failures.

To preserve the existing exact-judgment-only group contract, allocate just one new service opcode, **20=ROUTE_FEATURE_GROUP_OPEN**, enabled only after capabilities 5, 6, 7 and 8. Arguments are `[scopeID,FoundationID,ExtractorID,requestedLeaseMillis]`; leases use the same positive at-most-172800000-millisecond rule. This creates an empty group with explicit local mode FULL_FEATURE and that exact ExtractorID. Opcode 16 still creates only FULL_EXACT groups. An already active same-provider/scope group of a different mode/foundation/extractor gives the inherited ROUTE reason REQUEST_MISMATCH within the existing failure-result envelope, not silent reinterpretation or an invented top-level result code.

The existing group observation result shape remains unchanged and is bound to the exact OPEN call; group mode/extractor are retained authoritative local state, not inferred from a later ad. Existing operations 17–19 can mutate/renew/close a FULL_FEATURE group only after cap5+6+7+8, with batch PUTs accepting only ProviderAd2/K4 with that group's exact foundation/extractor. The same operation numbers retain FULL_EXACT's exact-judgment K1 contract: frozen F3 groups require cap5+6 with their legacy records; new F4 groups require cap5+6+8 and the integrated code-4 records. The immutable group mode/foundation profile selects the branch. No request changes a group's mode in place. Base ungrouped PUT/DROP cannot bypass either group's ownership/map/version accounting. All these operational replies keep `publicAssessmentDigestOption=[0]`; their existing result shapes/reason-code mappings do not become native acceptance certificates.

The existing `0x8023/1` group map grammar already stores full canonical cells and therefore represents these new K4 keys without changing old leaf meanings. Its exact key-domain/hash, collision check and 2048-byte node bound still apply. No old FineScope judgment array is interpreted as a feature tuple list. All changed memberships, partial cells, empty/retiring groups, temporary replacements, native/public eligibility summaries, current lease gates, stale-GC fences and replies remain counted exactly as in the fine-routing contract.

For FULL_FEATURE renewal, the producer revalidates that every grouped token still has at least one currently eligible public descriptor in the exact declared scope under this extractor, and that the signed anchor remains eligible or has been replaced. One surviving theorem with another token cannot justify renewing a stale token. Fixed token-extraction bugs can damage discovery and require index rebuild, but cannot change native theorem acceptance.

## Selected local query portfolio and application path

The local request is a well-scoped formal type/expression in the agent's current environment, with an owner-selected operation mode and budget. It need not name a desired theorem. It is not recorded as a public unsolved goal. The client can use a private LLM to suggest that query or rank obtained candidates, but the selected baseline runs without online training.

### Exact bounded query-token lifting

A query is projected with the same native syntax/head/pattern rules and bounded raw/normalized variants. This does not index the query as a proposed theorem. From its retained expression Q and informative head h, the following are the exact allowed lifted **payloads**, hashed with the selected ExtractorID. A lift changes only the stated role/kind/side fields; constant identities, argument indexes and HeadAtoms remain exact:

| Query mode/input | Allowed token templates | Candidate view compared |
|---|---|---|
| APPLY_RESULT with desired Q | `[0,0,h]`; `[1,1,0,h]`; `[1,1,1,h]` | Terminal; stored Iff left; stored Iff right, respectively |
| APPLY_RESULT with a rigid Q operation edge or reference | its tag3/tag6 payload under role0, or the same payload with role3 or role4 | Terminal or corresponding Iff side |
| APPLY_RESULT whose desired terminal is recognized Eq/Iff | raw/completed operand-head pair tag2; the same pair with heads exchanged as a separate symmetry lane | Candidate whole result; any actual symmetry/direction proof is later checked |
| REWRITE_OPERAND with selected local subexpression Q | `[1,0,0,h]`; `[1,0,1,h]`; tag3/tag6 Q payloads remapped to role1 or role2 | Stored Eq left or right, respectively |
| FUNCTION_OUTPUT with desired A and optional available B | `[0,0,head(A)]`; when both are informative, `[4,head(B),head(A)]` | Stored terminal/output, not an Iff side |
| BINDER_DOMAIN with desired B | `[5,head(B)]` | The stored selected domain pattern if present; absence gives no pattern-confirmed match |

For an Iff-side lift, the query pattern is the pattern of Q, **not** an invented `P↔Q` pattern and not a terminal-role token that the stored side never emits. Thus a stored `P(x)↔Q(x)` with informative Q head and a local `Q(y)` query share `[1,1,1,head(Q)]` before pattern filtering. The analogous left-side token supports the reverse direction. For rewriting, both Eq side lifts are explicitly offered; a side-1 hit means the equality is used backwards only after actual checked symmetry/transport. A role-specific edge/reference is conjoined only with tokens lifted to the **same** candidate view; tokens for distinct opposite sides are separate lanes, not an accidental conjunction.

Where an APPLY_RESULT relation-pair symmetry lane is used, form the query comparison pattern with the relation operands exchanged. The forward query pattern would otherwise exclude the intended symmetric candidate. For nonrelation Iff-side lanes, only Q is compared, so no guessed missing premise enters the pattern. A tag4 function lane uses the desired A/output pattern; B is a head constraint, with full dependent input checking postponed to application.

For the one generic lane, generate tag7 from the exact raw terminal head when known. This can find, for example, generic Eq theorems in the same Eq fallback bucket. A fully parameter-headed theorem has a different fallback constructor token and is not promised to be reached from every concrete goal; the client can spend a separately selected generic attempt on `[7,[2,0]]`, where native node tag0 is a bound variable. At most one such broad lane is issued per attempt. Generic selection is an explicit local heuristic, not an extractor completeness theorem.

Build at most eight predicate lanes from these fixed templates:

1. Informative relation operand-head pair or rigid parent/operand edge matching the mode.
2. A single informative operand/operation head, optionally conjoined with another query token.
3. Input/output type-head pair for a desired map B→A; optional concrete interface-symbol token.
4. A relaxed rigid-reference/domain-head lane when no stronger key applies.
5. At most one broad tag-7 generic fallback lane and the explicit symmetry/Iff-side templates above.

Absent categories consume no lane. For APPLY_RESULT reserve up to three of the eight slots for the available single-head terminal/Iff-left/Iff-right templates; for REWRITE_OPERAND reserve up to two for its two single-side head templates. This prevents a token-rich concrete query from automatically starving both Iff directions or one rewrite direction. Deduplicate identical predicates. Fill the remaining slots in the category order above, with at most four same-view conjuncts, and leave the last slot available for the selected generic lane when one exists. Within an unreserved category rank available informative tokens by increasing observed local posting cardinality; unknown counts rank after known counts, with token bytes breaking ties. Remote frequencies are uncertain hints. Head Eq/Iff alone never occupies the first directed lane. The client does not require every query constant to occur in a general lemma: substituting a parameter can introduce constants absent from the theorem, so overconjoining all goal symbols would destroy recall. Different local frequency observations may select different valid bounded portfolios; the provider's interpretation of each transmitted predicate remains exact and deterministic.

For each chosen token, use ROUTE1 K4 to discover providers, then issue the full mode-6 predicate to separately funded selected providers. A provider advertising token A and token B might have them in different declarations; only its actual conjunction query filters that distinction. DHT ads alone do not establish cooccurrence or applicability. Newly suggested contacts do not enlarge an old directory-pinned lookup session for free.

An initial interactive attempt admits at most 16 route-cell lookups, 24 provider FIND_WINDOW pages, four concurrent peers, 8 MiB aggregate discovery traffic, 64 MiB temporary memory, 2 local CPU-seconds and 10 wall-seconds. Any dimension can stop it; these are ceilings, not a ten-second result promise. Retain at most 1536 descriptors under the same byte limit. Deeper routing or import is a separately declared operation. Fair local lane/provider/window cursors prevent always selecting one common-key prefix, without claiming uniform global sampling.

Inspect at most 32 candidate types initially, reserving eight slots for diversity, including at most four generic/fallback candidates when available. At most two evidence alternatives for one exact target take those slots. Client-side candidate matching instantiates leading parameters, compares dependent argument types and records residuals; it neither invents missing premises nor authorizes unchecked higher-order substitutions. Full selected closure acquisition/replay has its own admission envelope and is not hidden inside a cheap index response.

For a theorem `p : Π xs, B(xs)`, a successful local use still requires actual arguments a with each dependent type checked, followed by checking `p a` against the claimed result. For an iff-side candidate, build and check the appropriate implication/application and leave the other side as a residual if not supplied. For a rewrite, construct/check actual equality transport/congruence in the selected context; textual subtree replacement is not proof. For a map candidate, instantiate its parameters first and check the resulting `f:B→A`; output depending on the subject binder is not an ordinary nondependent bridge merely because a head feature matches.

Return distinct outcomes: PROVIDER_NOT_REACHED, NO_CANDIDATE_IN_SCANNED_SCOPE, STRUCTURAL_CANDIDATE, PROJECTED_PATTERN_MISMATCH, TENTATIVE_APPLICATION_WITH_RESIDUALS, NATIVE_IMPORT_NONDECISION, INCOMPATIBLE_CHECKED_INTERFACE, or CHECKED_LOCAL_APPLICATION. A negative earlier outcome is not a native refutation of a potentially useful theorem.

## Typed examples and recall countercases

### Addition commutativity without knowing the theorem ID

In one exact Nat/Add foundation/interface, a local query has type `Eq Nat (add a b) (add b a)`. A stored theorem `∀ x y : Nat, Eq Nat (add x y) (add y x)` has the same informative Eq operand-head pair and addition edge/reference features; telescope parameters become WILD. The exact JudgmentIDs differ because the local instance/context differs. Structural routing can nevertheless reach its provider. Instantiating x=a,y=b and checking the actual application establishes reuse; pattern agreement alone does not.

`∀ x : Nat, Eq Nat x x` produces a largely generic equality shape. It is not allowed to dominate the directed addition lane. It can appear in the bounded generic fallback and be applicable when both goal operands are definitionally equal, but cannot prove arbitrary `a=b` merely because both pattern operands are WILD.

### A nontrivial equality-head bucket

Compare `mul x (add y z) = add (mul x y) (mul x z)` with equalities about `List.map`, `sin`, and arbitrary record fields. They all have Eq as head. The first has informative multiplication/addition operand/edge tokens, including the last explicit argument edge from mul to add. These route/query features are materially narrower than Eq alone when those operations are not ubiquitous in every indexed descriptor. They still do not prove that a distributivity premise or algebra instance is available.

### A checked bridge function, including an opaque definition

A desired local construction needs A but has b:B. A safe transparent or body-checked opaque declaration `f:B→A` emits an input/output pair keyed by exact B and A heads. A generic declaration `∀ c:C, B→A` can also be a candidate, but leaves c unresolved unless supplied. A dependent function `∀ b:B, A b` can share coarse head features and is not automatically an admissible nondependent bridge. The client checks the instantiated type and actual application. Different nominal A/B encodings need explicit checked maps, not a shared English label.

### Iff is useful through a checked direction

A stored `∀ x, P x ↔ Q x` can expose its Q-side view to a local Q query. Applying its checked forward direction leaves P x as a residual. It is not an unconditional Q theorem, and the network does not acquire a task to prove P x. The reverse direction is a separately labeled candidate view with the analogous condition.

### Known recall losses

- An informative constant beyond the fixed visit/depth/domain/lane bounds may receive no token. The descriptor flags the actual truncation; another profile or exact route is needed for stronger coverage.
- A definitionally equal wrapper requiring delta unfolding is not removed by beta/zeta normalization. Two distinct interface GroupIDs are not merged even when isomorphic.
- A beta wrapper that exposes a new leading Pi or Eq only after normalization does not trigger new peeling/focus creation in this profile.
- A theorem headed by a parameter, or a very general `∀ P, ...`, can be useful after specialization while having no informative rigid token. Its fallback bucket can be large; a finite generic budget can miss it.
- An informative function argument before the selected last-eight edge positions, or a relevant earlier binder domain beyond the last-16 selection, can be missed.
- A concrete query may contain a type/instance/operation absent from a polymorphic theorem because it is supplied by substitution. Requiring that token excludes the theorem; relaxed and generic lanes mitigate, not eliminate, the loss.
- A lemma requiring several nontrivial premises may not appear useful until additional reasoning. STRUCT2 does not solve those premises or guarantee optimal lemma selection.
- Token membership on a provider can be true while conjunction match is empty, the chosen witness is incompatible, the full closure is too large, or service has expired.
- A large corpus can generate many meaningful matches even under discriminating keys. Paging, ranking and finite local application work still limit actual recall.

## Qualification and practical acceptance

Source inspection supplies precedents and exact pinned behavior, not a retrieval benchmark. The future qualification pool must contain native, independently checked useful applications whose candidate IDs are hidden from the query client, including polymorphic instances, Eq/iff, overloaded operation projections, safe/opaque maps, constructors, definitions with beta/let wrappers and distinct checked interfaces.

Compare STRUCT1, known-ID-only routing, STRUCT2 token-only, STRUCT2 with pattern filtering, and the same client with a local learned ranker, using identical scope/publication/network/retention budgets. Measure unfamiliar-provider reachability, candidate recall before ranking, actual checked-application yield, residual difficulty, cold/warm import cost, generic bucket load, false leads, feature/group refresh cost and publication gaps. Supplying the correct candidate list to the ranker would not test decentralized discovery.

A useful result is a repeatable improvement in completed checked local reuse under declared costs, with all misses and partial scopes recorded. No formal statement here proves optimal heuristic retrieval, that every helpful unknown lemma is found, or exponential growth. It does select a concrete relevance path that can be implemented and falsified instead of leaving STRUCT2 as an unnamed future extractor.
