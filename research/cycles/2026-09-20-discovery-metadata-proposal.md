# Gate B: bounded local discovery metadata proposal

Date: 2026-09-20  
Status: implementation proposal, not implemented or qualified  
Owner: `bounded_domains_resource`; this proposal only, no experiment execution

## Decision and scope

Use a local two-provider immutable-snapshot adapter for the existing [STRUCT2/1 contract](../../notes/analyses/CP-001G-structural-retrieval.md) and [FIND_WINDOW operation 10](../../spec/OPERATIONAL-CORPUS-V2.md#finding-and-applying-existing-mathematics). Select **token-only mode-6 queries**, with `patternOption=[0]`, for the first Gate B cut. The extractor still produces the exact required patterns, digests and descriptor summaries; only optional provider-side query-pattern filtering is deferred.

This is the metadata component of the unchanged [full existential Gate B](2026-09-20-subtype-composition-contract.md#gate-b-preregistration-target-corpus-and-access-arms), not a substitute theorem-selection task. The companion controller proposal selects local proof actions and query occasions. Metadata lookup supplies candidates; acquisition, independent replay, checked instantiation and actual proof search remain separate.

Do not add a protocol, coordinator, task queue, useful-first catalogue or central mathematical authority. This local adapter cannot qualify routing, unfamiliar-provider reachability, network framing, signatures, custody, service fairness or remote latency. Do not advertise general capability-7 implementation from this restricted test.

## Exact internal boundary

Provider preparation consumes the qualified foundation/seed inventory and exact selected checked target roots. For each target it resolves:

- `FoundationID`, exact EqRef/IffRef and the corresponding typed ExtractorID; no invented release-time digest.
- Semantic `targetRef`, exact checked declaration type and its scope/universe information.
- Exact `anchorReplayID`, including the required target/root relationship and selected PI1 support.

For this corpus, the selected roots are judgments `[2,JudgmentID]` and the map definition `[1,DefinitionID]`. Only those selected roots are indexed, not all closure dependencies. Coalesce identities that actually coincide. Source aliases and C1-C10 evaluator labels do not enter descriptors, queries or candidate ranking.

The local controller supplies a well-scoped formal query, operation mode and, for FUNCTION_OUTPUT, optionally a locally available input type. Its bridge must abstract local free variables to explicit scoped telescope parameters and map constants to exact already-known semantic references. Instantiate assigned metavariables first. Unresolved metavariables have no native term tag: refuse or omit the affected query under a frozen controller rule, rather than inventing constant identities. Binder scopes must be preserved when peeling Pis or inspecting a binder domain.

The existing request is:

`[predicate,snapshotSelector,startPosition,pageCeilings]`

with predicate:

`[6,FoundationID,ExtractorID,queryMode,sortedRequiredTokens,[0]]`.

Modes are 0=APPLY_RESULT, 1=REWRITE_OPERAND, 2=FUNCTION_OUTPUT and 3=BINDER_DOMAIN. There are one to four unique sorted tokens. Responses carry inline `StructuralDescriptor 0x8124/1` records plus the existing snapshot/processed-interval/continuation information. A descriptor's target/evidence binding is still a provider assertion until independently checked.

## Smallest credible extractor qualification

Choose a **fail-closed, redex-free supported type fragment** initially, rather than implementing substitution before knowing it is needed. Its obligation is exactness on success:

`adapter(x)=descriptor` implies that the complete selected STRUCT2/1 algorithm on x produces those exact descriptor bytes.

An unsupported case returns `NOT_EXTRACTED` and publishes no descriptor. This is implementation incompleteness, not a new extractor profile and not a mathematical rejection. It must not silently drop a target from the frozen corpus or claim FULL_FEATURE coverage for an incomplete scope.

### Grounding in existing source evidence

Read-only inspection of the retained A2 `SOURCE_CAPTURE_JSON` type DAGs gives:

| Existing target | Type DAG nodes | Observed native syntax tags | Applied-lambda / let nodes |
|---|---:|---|---|
| `SharedSubtypeA.val_injective` | 20 | 0,1,2,3,4,5 | 0 / 0 |
| `SharedSubtypeB.map` | 29 | 0,1,2,3,5 | 0 / 0 |
| `SharedSubtypeB.map_val` | 48 | 0,1,2,3,5 | 0 / 0 |

Evidence: [producer A source](../../experiments/lean-source-composition/ProducerA.lean), [producer B source](../../experiments/lean-source-composition/ProducerB.lean), [A capture](../../experiments/lean-source-composition/runs/attempt-04/A2/01.stdout.log), [B capture](../../experiments/lean-source-composition/runs/attempt-04/A2/03.stdout.log). These counts inspect retained source-type syntax; they are **not** STRUCT2 virtual READ counts, extracted features or new proof runs. The source codec replaces names/binder annotations and canonicalizes sharing; it does not beta-reduce these types.

The actual seven control source types are not yet captured here. Their preregistered formulas plausibly use the same redex-free constructors, but formulas do not prove elaborated-type coverage. Author, capture and independently check those targets **before** freezing the supported fragment or predicting their tokens. C7 can contain a lambda under Exists without an applied-lambda redex; C9 requires exact Iff recognition. A projection may be a constant application or native projection node; inspect the actual representation.

### Selected initial support and refusal rule

The smallest presently justified provider scope is validated native types with variables, sorts, semantic constants, application, lambda and Pi (native tags 0-5), and the empty explicit judgment telescope already used by the ordinary-source adapter, retaining the complete Pi type. Add native projection tag 8 if the actual corpus/query bridge requires it. No literals, lets, applied lambdas, other unimplemented native form or unimplemented logical-cut case may produce a descriptor. This is a syntax-and-bound rule, never a whitelist of useful names or target IDs.

All successful cases must still execute the prescribed phase order and virtual accounting:

1. Peel the specified leading Pis, recognize only exact raw Eq/Iff heads, select last domains, and establish the ordered raw foci.
2. Perform raw head/preorder/edge inspection with repeated occurrence READ charges. Construct patterns from that recorded inspection, not an uncharged second native walk.
3. Read selected domain heads and pair them with the retained terminal head.
4. Perform the exact leftmost-outermost normalization redex search, including each application's extra function-node READ. In this fragment the complete search finds no redex. There are zero contractions and zero newly constructed normalization occurrences, but the search is not free.
5. Emit each completed normalized companion **even when identical to its raw focus**, then perform its prescribed inspection with fresh virtual READ charges. Token duplicates coalesce; raw/normalized view summaries remain distinguished. Reuse retained domain heads exactly as specified.
6. Generate payloads in the exact order, apply the distinct 16/8/4/4 quotas, and canonicalize/hash patterns and descriptor bytes.

Finding an unhandled beta/zeta redex means whole-target `NOT_EXTRACTED`, not `NORMALIZATION_INCOMPLETE`: the latter is a specified logical-limit outcome, not an excuse for missing machinery. Likewise a partial implementation may decline an unimplemented cut, but cannot invent truncation flags or substitute its own cutoff. It must implement any actual corpus-required pattern CUT, lane truncation or other limit semantics exactly before claiming those targets extracted. A preflight support scan has actual CPU/memory cost and does not replace or erase any required virtual READs.

The fixed limits remain `[64,16,8192,64,8,128,16,16,1024,32,4]`, with all other payload/enumeration/descriptor bounds inherited unchanged. If an actual target falls outside support, report it before B and extend the implementation under a reviewed cut; do not rewrite the target solely to make the experiment pass. A full beta/zeta implementation is necessary only if observed required inputs need it. No all-ten extraction claim is justified yet.

## Snapshots, postings and cursors

Freeze exactly the declared public targets assigned to P1/P2, their successful descriptors and the evaluator-only role map. Each provider orders rows by **its own StructuralDescriptor CIDs**, not root PublicIndexDescriptor CIDs or source names. Build token postings in that same order.

For a query choose the shortest required-token posting, with token-byte tie break, then test every other required token. The initial adapter accepts only the selected token-only input path; it does not silently ignore a supplied pattern. Each descriptor is returned once per query even if several features/views match.

Implement existing new-scan `[0]` BEGIN or `[1,CID]` inclusive-lower-bound behavior and resume `[2,continuation]` with its corresponding live snapshot. The boundary need not be an existing row. Retained continuation state binds holder, snapshot, full predicate, extractor, planner, row schema/mode, original lower boundary, next unprocessed position and original expiry. Current-view or mismatched/stale resume must refuse, never silently start a fresh scan. Page ceilings may decrease within the original admitted constraints, not enlarge the allocation.

Reply with the processed half-open interval and END/next. A matching row that does not fit output remains unprocessed. No wrap or completeness claim below the boundary. A small in-process opaque handle table can test those bindings, but supplies no signature/network-security qualification. Freeze and test expiry without extending it on continuation.

## Goal-derived lanes and global budgets

The controller chooses subproblems and mode; the adapter performs only permitted lifting:

- A selected witness subproblem `S_p -> S_q` permits `[4,H_S,H_S]` and the output-head lane. This does not follow merely by extracting the outer Exists head. Optional future pattern comparison uses output `S_q`, not the whole arrow.
- A folded Injective goal permits its actual head lanes; unfolding changes the local formal query and belongs to the shared controller policy, not STRUCT2 normalization.
- Equality/Iff operands, rigid operations/references and rewrite views follow the exact mode/role templates. Opposite views are separate lanes, not conjunctions. Initial queries cannot contain an unknown map identity; later queries can contain it only after checked acquisition/instantiation.
- Portfolio ties use the selected contract's local-frequency/byte rules, without evaluator usefulness labels. The controller must freeze when lanes are allocated or retained across fresh proof attempts.

All dimensions below are cumulative; a new subgoal, failed application, resumed page or clean proof-search restart does not reset them:

| Scope | Existing ceiling |
|---|---|
| One discovery attempt per arm | 8 lanes; 24 pages; 10 wall seconds; 2 local CPU seconds; 8 MiB traffic; 64 MiB temporary memory |
| Each provider page | 64 descriptors; 1 MiB encoded bytes; 8192 posting inspections; 0.25 CPU seconds; 2 wall seconds |
| Candidate-root acquisition/application | 8 attempts, including retries/evidence alternatives |
| Whole arm | 300-second wall/CPU envelope; 4 GiB aggregate private memory; one active Lean child |

Other inherited limits still apply, including retained descriptor and initial type-inspection limits. Pattern-probe limits are unused only because these queries request no pattern. Discovery and acquisition have separate accounted stages within the outer envelope; the predeclared acquisition byte cap is not enlarged by this proposal. Publication/index preparation is reported separately and included in any whole-system amortization claim.

Interpret the existing 10-second wall limit literally: the one discovery attempt starts with its first query projection/lane-planning work and has a continuous monotonic deadline ten seconds later. Acquisition/proof-search pauses and restarts do not pause or extend that deadline. No further discovery work may be started after expiry; checked acquisition/local proving can continue under their remaining outer allowances. Thus a slow first import can leave no time for a map-dependent second query. Record that as a real limitation, not a fresh free attempt or secretly accumulated active-service time. Any different clock interpretation requires an explicit preregistered contract revision before trials.

## Required integration evidence

No STRUCT2/FIND_WINDOW implementation symbols were found in repository Python/Lean outside runtime and retained run/held copies during this review. Reuse [source_codec.py](../../experiments/lean-source-composition/source_codec.py) for validated native references, canonical content hashing/storage, checked source correspondence and existing replay machinery. Its `transform_dag` is not a STRUCT2 normalizer or fuel model.

Before a trial, retain actual corpus types and root bindings, support decisions, extractor descriptor/ID, feature payload/token/flag traces, pattern summaries, exact snapshot order and sizes. Test reproducible descriptor output, identical-raw/normalized companions, unsupported-redex refusal, ordering, full-page continuation, arbitrary lower boundary, stale/mismatched holder/snapshot/predicate and cumulative exhaustion. These tests establish the chosen fragment's behavior, not universal retrieval completeness.

Separate evaluator/provider preparation files from consumer-readable inputs. The consumer receives contacts and declared interface access, not producer source/proofs, complete useful-ID maps, evaluator annotations, prior-arm logs or cached contribution evidence. Metadata matches cannot add a declaration; only later checked admission may enlarge the local environment. Preserve failure records and report mathematical completion, acquired-reference use, discovery-origin use, new-to-consumer identity and measured benefit separately.

The immediate next step is corpus capture plus controller/query-bridge feasibility, then a reviewed minimal adapter. It is not a broader architecture investigation or a claim that synthesis or useful growth is already demonstrated.
