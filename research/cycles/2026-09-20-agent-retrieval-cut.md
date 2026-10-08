# Agent retrieval: the smallest unknown-ID conformance cut

Date: 2026-09-20  
Status: bounded proposal; no implementation changes, extraction runs, agent calls or trial results  
Scope: retrieval/client boundary over the fixed ten-target, two-provider corpus; not a solver

## Decision

Use the existing **MENTIONS_ALL** query meaning first, over raw exact symbols in declaration types. A locally known interface symbol can locate contributions whose result IDs the agent does not know. The first useful candidate key is the exact shared Subtype type reference already present in the common checked interface and formal target, not any contribution's identity.

Keep the full existential mathematical target, all ten nominal public targets, both provider allocations, direct local proving, and independent receiving checks. Change only the retrieval baseline in a **new agent/API conformance cut**. This does not silently replace or pass the preregistered mode-6 [Gate B](2026-09-20-subtype-composition-contract.md#gate-b-preregistration-target-corpus-and-access-arms). That mode-6 experiment remains unqualified.

This deliberately coarse test asks whether an independent agent can use documented APIs to find unfamiliar result identities, inspect candidates, admit evidence and produce a checked successor. It does not test sophisticated relevance ranking, general recall, unfamiliar-provider discovery or large-corpus efficiency. On this engineered corpus a Subtype query may return every target; if so, report that fact rather than describing the index as discriminating.

Search timing, choice of symbols, mathematical decomposition, definition use and remaining proof obligations belong to the agent/local authoring tools. The retrieval helper neither chooses a witness nor schedules a proof. API documentation may explain arguments, authority, costs and errors; it must not prescribe the evaluator's useful contribution IDs or proof route.

## Why not require STRUCT2 for this first cut?

The [existing organization modes](../../spec/OPERATIONAL-CORPUS-V1-ORGANIZATION.md#retrieval-protocol-with-fixed-modes) already include mode 2, MENTIONS_ALL, with one to eight exact symbol keys under one extraction profile. [F4 integration](../../notes/analyses/CP-001G-profile-and-consumer-bindings.md#public-root-descriptor) preserves inherited query meanings in the expressly supported new native-ID domain. No mode 0, free-form theorem query or new network opcode is needed.

Token-only STRUCT2 means `patternOption=[0]` in its existing mode-6 predicate. It removes query-pattern filtering, **not** the provider's obligation to produce exact STRUCT2 tokens, normalization/view summaries, pattern digests and flags. Sending a few convenient tokens with invented or omitted summaries is not STRUCT2/1. The current provisional helper does not supply a simpler fully qualified mode-6 path.

MENTIONS_ALL needs only a bounded raw symbol pass and ordered membership lookup for this local cut. It avoids beta/zeta substitution, pattern construction, Eq/Iff focus selection, 16/8/4/4 feature selection and open-goal token lifting. Exact-ID lookup remains a useful access baseline but does not by itself establish unknown-result-ID discovery.

The modes are specified, but a working MENTIONS_ALL helper has not been established here. This proposal authorizes no claim that a complete legacy service, wire codec or extractor identity is already implemented.

## Exact symbol scope and supported fragment

The source of symbols is the **effective declaration type**:

- Judgment: its explicit ordered telescope followed by its conclusion, including all domain types. The selected ordinary-source corpus represents the telescope as leading Pis and has an empty explicit Judgment telescope.
- Definition: its declared type, not its value/body.
- No proof body, definition body, unrelated ContextSet member, closure dependency's own type/body, source name, private annotation or provider label is searched.

A constant occurrence supplies its exact external Native2 semantic reference, including an actual group-member selector where present. For Subtype, retain its actual qualified type-member reference, not a printed name, a guessed digest or a GroupID that silently conflates members. The caller obtains this reference from its already-known common interface. No contribution identity enters the initial request.

For the first local helper, support canonical already-validated closed native type DAGs with native tags 0-5 (bound variable, Sort, constant, application, lambda, Pi), the actual source adapter's empty explicit Judgment telescope, and the exact permitted seed/definition/judgment/group-member semantic references. Traverse the **occurrence tree** in preorder: application function then argument; lambda/Pi domain then body. Shared DAG nodes are revisited at each occurrence. Universe-level expressions supply no constant symbols. No unfolding, beta reduction, theorem application or proof search is performed.

The inherited STRUCT1 raw-symbol limits are 4096 expression occurrences, depth 64 and the first 32 distinct symbol keys. The selected local helper accepts a complete traversal within those inclusive ceilings and declines if another occurrence, depth or distinct symbol would exceed them. It returns no partial symbol set. The earlier prose's boundary flag wording is not thereby qualified: this helper reports its own complete-scan counts, not serialized STRUCT1 extraction flags. Other native forms can be added after actual capture demonstrates a need; silently ignoring their children is not permitted. Raw syntax may contain an applied lambda without requiring reduction, unlike the current redex-free STRUCT2 helper.

All ten actual target types must be inspected during preparation. Verify which contain the selected common symbol within these limits; do not infer their exact keys from their displayed formulas. If any target fails the fragment, the preparation is incomplete: extend the bounded raw pass or report the gap before a trial. Do not remove targets, insert padding or filter to C1-C3. Exact identity coalescing is reported with the resulting target count.

This is a finite implementation of the existing raw symbol-membership semantics, not all STRUCT1 outputs: head, raw shape and optional BETA128 are not implemented or advertised. Bind the local helper/version and supported grammar in the experiment. Do not invent an interoperable ExtractorID from a friendly string or encode an unreviewed wire payload. A local API-semantic conformance result can precede complete network/profile qualification without mislabeling it.

## F4 public rows, lookup and paging

Use the existing `PublicIndexDescriptor 0x8111/3` payload:

`[FoundationID,typedRoot,judgmentOption,InstanceReplayID,[0]]`.

The final `[0]` says no STRUCT2 descriptor is attached. For theorem roots, `typedRoot=[4,ProofInstanceID]` and `judgmentOption=[1,JudgmentID]`; the instance/replay must bind that exact judgment. For the map definition, `typedRoot=[1,DefinitionID]` and `judgmentOption=[0]`. Foundation and replay bindings come from the actual independently checked preparation, never from the source label. Each descriptor remains at most 4096 canonical bytes and is hashed under its actual type/schema.

P1 retains C1/C4/C6/C8/C10; P2 retains C2/C3/C5/C7/C9, subject only to reported exact coalescing. Index precisely those selected roots. Their complete support remains available through the existing root-scoped acquisition path but does not become additional public target rows. Keep evaluator roles and aliases outside consumer-visible data.

Each provider freezes its own descriptor list, sorted by **PublicIndexDescriptor CID**. These are not mode-6 StructuralDescriptor CIDs. Membership postings are sorted in that same order. For a conjunction select the shortest posting, break ties by canonical key bytes, and test every other requested symbol. No useful-first ordering or proof-strength filtering occurs.

For the immediate helper, use a smaller **local-only offset cursor**, explicitly bound to provider, immutable snapshot and exact predicate, identifying the next unprocessed position in the fixed selected posting. Reject a mismatched continuation; output exhaustion cannot skip a matching row. This is not a FIND_WINDOW token: holder authentication, expiry, live snapshot admission and arbitrary CID lower-bound seeks are outside this helper. The richer inherited FIND_WINDOW contract remains unchanged and unqualified. Do not add a network opcode or claim service framing, routing or signatures.

Retain the existing per-page ceilings of 64 descriptors, 1 MiB encoded response, 8192 posting inspections, 0.25 CPU seconds and two wall seconds; lower local ceilings are allowed. Count canonical descriptor bytes, wrapper/cursor bytes and request bytes in the experiment's traffic accounting. Physical traffic is not the sum of payload object sizes alone. The first finite service test should deliberately lower the row ceiling to two so that cursor behavior is exercised even with five targets per provider.

## Candidate types before admission

Allow **at most ten total candidate-type probe calls**, with retries consuming calls. This can display up to the whole nominal corpus without first admitting ten roots. Keep **at most eight complete-root admission/application attempts**, including failed attempts and alternative witnesses. The distinction is explicit for this new cut; it is not a hidden enlargement of the original Gate B policy.

A type probe supplies bounded, **untrusted formal syntax**, not a locally installed declaration or certified applicability judgment. Obtain its bytes through the existing public-root scoped read semantics:

- Theorem: reconcile the descriptor with the replay's PI root and the PI's target judgment, then read that Judgment's type/telescope objects.
- Definition: reconcile the replay's definition root, then read its declared type object.
- Check every supplied object's typed content hash, parser/schema bounds and the links used by the probe. These checks establish the inspected byte binding, not correctness of its proof/body, all dependencies, representative context, or available premises.

No new inline type field is added to PublicIndexDescriptor. A local `inspect_candidate` convenience can compose these existing scoped reads. It must not provide generic CAS access or execute producer code. No proof/definition body is needed merely to display its declared type. Exact unknown references can be rendered as inert identifiers; familiar labels may come only from the consumer's already-checked local map. Candidate syntax cannot become an axiom or modify the Lean environment.

Use at most 1 MiB returned bytes per probe and the same aggregate 8 MiB discovery-traffic allowance across pages, probes and requests. Native bytes obtained by probes also count conservatively against the cumulative contribution-acquisition byte cap; overlapping budget charges are explicit, while physical traffic totals count the transfer once. Parsing/rendering and retained temporary data consume the discovery CPU/memory allowances. Retransfers count again. The existing maximum 32 initial type inspections is not enlarged; this cut chooses the stricter ten-call subset.

Only a later full selected-closure admission through the existing receiving path can make a candidate a checked local declaration. Actual theorem applications, dependent arguments, transports and residual obligations still check locally. The agent can choose which candidate to admit after inspecting syntax; it cannot trust a provider's type display as proof.

Keep one cumulative discovery account, not a fresh account per agent tool call: at most 24 pages, 8 MiB discovery traffic, 64 MiB temporary memory and the declared CPU/wall allowance, all inside the outer arm envelope. If retaining the previous ten-second discovery wall limit, measure one continuous monotonic interval from first discovery work; it does not pause for import/proof work. A change to that timing must be a visible preregistered change, not a consequence of replacing the controller with an agent.

## Smallest honest disposition of the two STRUCT2 questions

These are proposed clarifications for any later STRUCT2 qualification; they do not modify the provisional code or require it for this conformance cut.

**Final rigid-reference lane.** Select the first four distinct not-already-selected tokens under the specified focus/depth/path/canonical-byte ordering. If another eligible token remains, omit it and set `FEATURE_LANE_TRUNCATED=6`; unused capacity in other lanes is not borrowed. This is ordinary finite feature selection, not normalization failure or whole-target rejection. The current helper instead returns `NOT_EXTRACTED` for every lane overflow. That refusal is honest partial implementation, but may unnecessarily exclude a small actual type; C3's several focus-specific reference occurrences must be measured, not guessed. The minimum future repair can implement this final lane only, retaining refusal for unimplemented other-lane cutoff cases.

**Pattern universe flag.** Set `UNIVERSES_ERASED=2` iff the retained pattern erases at least one actual universe expression: any retained Sort, or a retained constant with a nonempty universe vector. An empty constant universe vector alone does not trigger it; a Sort at level zero still does. Set `EXTERNAL_VARS_ERASED=1` iff an actual outer-scope variable becomes WILD. These triggers match the provisional code but require explicit reviewed wording because the selected note names the flags without giving these edge-case tests. This is a proposed resolution, not evidence that previously published bytes already followed it. Any incompatible deployed interpretation would require an explicit version boundary, not silent reuse of its identifier.

The separate phase-2 READ ambiguity remains scoped: the helper attempts both readings, requires identical descriptor bytes and conservatively refuses if the larger occurrence-level count could cut. It labels that count an upper bound, not a normative exact count. This can support a finite invariant-output qualification; it cannot qualify arbitrary inputs or substitute a new algorithm under the same profile identity. Domain-role-5 edges are generated/charged local data with no public lane and cannot suppress conclusion fallback.

## What is implemented, and the next finite test

The [provisional extractor](../../experiments/lean-formal-discovery/metadata_fragment.py) and [authored tests](../../experiments/lean-formal-discovery/test_metadata_fragment.py) remain unchanged and unexecuted. They cover a narrower redex-free, empty-explicit-telescope fragment, reject all current lane-overflow and other unimplemented cutoff cases, and contain no provider/cursor service, query bridge or solver. Running two readings through shared code is not an independent oracle for every descriptor field. No full STRUCT2/capability-7 or actual ten-target extraction claim follows.

The next finite test is **raw-symbol API conformance on the prepared corpus**, before any autonomous proving or retrieval-benefit claim:

1. Freeze the actual ten-target/coalesced inventory, provider allocations, common interface references, checked root bindings, symbol sets, F4 public descriptors and per-provider CID order. An evaluator-only independent enumeration supplies expected memberships and pages; it supplies no useful-ID subset to the consumer.
2. For the exact known Subtype reference, compare MENTIONS_ALL output with that enumeration. Exercise an absent key and a two-key conjunction. Report actual membership; do not promise all ten match before inspecting the types.
3. With two rows per page, resume every returned local continuation to END; check empty scans, no omission, provider/snapshot/predicate mismatch refusal and a stopped partial scan. Measure actual request/response bytes and aggregate accounting. This does not test full FIND_WINDOW lower-bound/expiry/authentication behavior.
4. Probe types through returned descriptor bindings only. Verify that altered links/hashes, wrong foundation and unsupported syntax cannot produce a trusted display or install a declaration. Confirm the ten-probe/eight-admission distinction and cumulative limits.
5. Only after the API test passes, expose the documented tools and common formal environment to a fresh isolated agent. Record the agent's actual query/candidate/admission choices; retain direct construction. End a successful mathematical trial at checked successor export and fresh replay, not a search result or plausible Lean text.

The first four steps qualify a finite lookup/inspection boundary. Step five can demonstrate unknown-ID agent-mediated checked reuse if actual acquired-reference and discovery-origin use occur. A direct proof without acquisition still counts as mathematical completion but not discovery-origin reuse. Neither outcome establishes saved work, scalable relevance, sustained growth or completion of the original mode-6 Gate B.
