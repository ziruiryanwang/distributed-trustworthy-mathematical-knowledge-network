# CP-001E: independent preservation, reuse, and interface cross-audit

Date: 2026-09-19  
Status: Completed bounded reads with explicit open integration/release findings below; not a deployment approval  
Method: Adversarial paper reasoning, algebraic checks, and cross-document interface inspection; no code, proof execution, benchmark, or mechanized verification

## Scope and independence

The reviewer independently read the complete [preservation analysis](../analyses/CP-001E-preservation-over-unbounded-time.md), [native scaling analysis](../analyses/CP-001E-native-scaling.md), and [goal-fitness assessment](../analyses/CP-001E-goal-fitness-assessment.md). The [exchange analysis](../analyses/CP-001E-exchange-scaling.md) was read completely in its initial draft and its subsequently changed bundle, export-inventory, scope, and generation-seal clauses were re-read. This is an independent review of those authors' work.

The reviewer authored [agent reuse/discovery](../analyses/CP-001E-agent-reuse-and-discovery.md) and, after the initial audit, the selected [local custody contract](../analyses/CP-001E-custody-contract.md). Inspection of those documents here is therefore a cross-layer/self-check, not an independent endorsement. The discovery note's exact-group-identity and contextual-application claims received a separate bounded spot-check from the native-profile author; the resulting wording correction is recorded below. The custody contract has a separate bounded review by the network author, with its status recorded under F2.

CP-001D remains frozen. All proposed capabilities here require new explicitly negotiated schema/profile behavior. This audit does not authorize implementation or an edit of the frozen checkpoint.

### Revision record

These are the bytes present after the described reads, before any later foundation/custody repair. A later change must be checked and separately recorded; this table is not a blanket approval of a live pathname.

| Artifact | SHA-256 |
|---|---|
| Native scaling | `85c8dc604693d136603c822ca502bf572be17f1e8d68ef69a4ff9fdb31a81ed5` |
| Preservation over unbounded time | `56bf53d9c924165fa79234267af21f9d36d58782dc8ebaafdeeaf8dd295efdbf` |
| Agent reuse/discovery | `295f383daf99c03febb8fbb7f3123c3bebd1902a9737af285081ac589b942b03` |
| Exchange scaling | `490742c153dc8e26007c11bdc4c944f76d3e4d74e41290682b03c5423f62f8d9` |
| Goal-fitness assessment | `019e0b88c64860a8f2d7385ab5563794e50ae907f18a3518338706c6650e982d` |

Subsequent bounded re-reads covered these refinements:

- Native scaling, SHA-256 `2cdfd32a0282e6100c15db1233fb163f0966ca520a3b5a4ef370c24a606bc537`: explicit value-preserving native-width/ABI conversion requirements and an explicit prohibition on using a same-foundation view to inherit affected ACCEPT across a corrected kernel-source commitment.
- Agent reuse/discovery, SHA-256 `0525e8dd334b0ea6f0b6ddf099d9a42a2a6a06afefab370f9d403502318796b0`: distinguishes hash/schema-checked inert hint storage/display from per-entry semantic activation against a checked exact target interface. This implements the network author's independent usability/authority clarification; importing every target in a guide is not required merely to read it as untrusted routing data.
- Preservation over unbounded time, SHA-256 `0e90487f0654d1cf10e4175f0031eb376706cd5bbf5ee7e34779bac02a0acc25`: completely re-read after exact-evidence/judgment-loss distinction, explicit local-only custody selection/link, and clarification that summable per-root budgets are sufficient for the stated marginal union-bound method rather than necessary in every joint failure model.
- Local custody contract, SHA-256 `914e2c9ab6fb41f4927aaa7ca03646d38876d2708e7feb1956caf23af99893b2`: author's self-check and response to network reviewer finding, followed by the network author's independent re-read of ownership, release/replacement, maintenance and status boundaries. That reviewer reported the partial-release defect resolved and no further custody blocker in those reviewed boundaries. This is bounded paper review, not execution qualification.

## Executive disposition

The proposed direct-reference/persistent-map representation, receiver-owned native certificates, relevant current-use guards, bounded bundle transfer, and finite-snapshot continuation form a coherent conditional concept. No new mechanism was found that intentionally turns a peer assertion, advisory label, or missing proof into mathematical acceptance.

That conclusion is substantially weaker than release readiness. In particular:

- The frozen Lean v4.22.0 pin must **not** be treated as a suitable deployment foundation. The subsequent foundation-source work selects a corrected v4.34.0 candidate; its bootstrap/adapter/build/runtime qualification remains required. Efficient caches and transport preserve whatever the checker establishes; they do not repair an unsound checker.
- The preservation model now distinguishes loss of one exact evidence representation from loss of every checked route to the underlying judgment; P3 is resolved at the recorded revised note.
- The custodian role now selects a local-only operational contract using existing remote pin observations/exports without a new remote preservation guarantee; F2's missing-selection finding is resolved, while separate review and future qualification of the authored custody details remain explicit.

The latter two were specific concept-integration findings and have received the dispositions below. The first remains a release-blocking trust-basis finding under separate source investigation, not an invitation to weaken the admission criterion.

## Preservation mathematics

### P1 — The repaired-copy CTMC and expected-loss formula check out

Disposition: no algebraic or probabilistic defect found under the stated model.

For states k in `0..r`, let the downward rate be k lambda, the upward rate be mu when `0 < k < r`, and zero be absorbing. The generator equation at an interior state is

\[
-1=\mu(T_{k+1}-T_k)+k\lambda(T_{k-1}-T_k).
\]

With `Delta_k = T_k - T_(k-1)`, it yields

\[
\Delta_k=\frac{1+\mu\Delta_{k+1}}{k\lambda},
\qquad\Delta_r=\frac1{r\lambda}.
\]

For r = 3, the three increments are

\[
\Delta_3=\frac1{3\lambda},\quad
\Delta_2=\frac1{2\lambda}+\frac{\mu}{6\lambda^2},\quad
\Delta_1=\frac1\lambda+\frac{\mu}{2\lambda^2}+\frac{\mu^2}{6\lambda^3}.
\]

Their sum is the stated `11/(6 lambda) + 2 mu/(3 lambda^2) + mu^2/(6 lambda^3)`. All terms have units of time. The serial-repair assumption matters: a model with independent parallel repair per missing replica would have different upward rates and a different formula.

The almost-sure absorption argument is valid. From each positive state, a finite consecutive sequence of losses has positive probability. There are finitely many such states, so an embedded-jump block has a uniform positive absorption opportunity; positive-state holding rates are positive and bounded in this finite model. Together with nonexplosion, this excludes infinite-horizon survival with positive probability under these fixed stationary assumptions. It is not an empirical estimate of a real storage deployment's hazards.

### P2 — Summable conditional interval risks support the stated union bound

Disposition: correct conditional argument, not a certified production risk estimate.

Let L_t be first unrecoverable loss in interval t. If, for every surviving prior history, its conditional probability is at most epsilon_t, then `Pr(L_t) <= epsilon_t`; summing over first-loss intervals gives `Pr(ever lose) <= sum epsilon_t`. Independence of intervals is not needed. The `6 epsilon/(pi^2 t^2)` allocation is summable to epsilon.

Under the additional model bound `q^(r_t)`, taking logarithms gives the displayed sufficient replica target. The nontrivial setting should explicitly say `0 < epsilon < 1`, `0 < q < 1`, and positive integer interval/replica counts. The target must actually be funded and established; counting keys or unverified receipts cannot justify the probability premise.

Allocating a summable budget over roots as well as time is appropriate for the stronger event "never lose any selected root". A fixed per-root upper bound repeated infinitely often supplies no useful bound on that collection-wide event. The note correctly avoids treating this as free infinite storage or evidence that real failure-domain independence is known.

### P3 — Exact evidence loss is not automatically mathematical-judgment loss

Severity: material interpretation/goal-scope refinement. Disposition: resolved in the independently re-read preservation revision `0e90487f0654d1cf10e4175f0031eb376706cd5bbf5ee7e34779bac02a0acc25`.

State zero is absorbing only after declaring what counts as a recovery source. Losing all modeled copies of an exact ReplayID does not establish that the theorem itself is irrecoverable: another proof, a reconstructive archive, erasure-coded pieces, another custodian outside the modeled set, or subsequent rederivation may still establish it. Conversely, a manifest hash without reconstructible evidence does not provide recovery.

Requested repair: define the CTMC as the loss model for the selected exact evidence representation, excluding additional reconstruction sources by hypothesis. Distinguish an exact-original-byte commitment from a checked-judgment-recoverability commitment. The latter can allow a different permitted proof/representation only after its explicit preservation relation, native admissibility, and retention transition are established. It must not discharge an old exact-byte promise silently.

The absorbing-model result remains valuable after that refinement: fixed copies alone cannot justify permanence. It should not be advertised as a theorem that the mathematical judgment is inevitably forgotten under every possible knowledge-generation system.

The revised note explicitly excludes external archives, alternate proofs, reconstructive shards/codes, and rederivation from the absorbing model and says exact ReplayID evidence loss does not establish judgment loss. Its selected custody contract separately identifies exact replay preservation and checked same-JudgmentID recovery. The scope correction is therefore present, not merely promised.

## Native representations and reuse certificates

### N1 — Direct semantic references preserve the selected binding boundary

Disposition: coherent conditional design; implementation correspondence remains unqualified.

The schema-2 direct set is recomputed from statement/telescope syntax, while transitive meanings are recursively committed by exact referenced declarations. Proof-only dependencies remain outside statement identity. Member selectors and universe instantiations remain in the native terms. On an acyclic exact meaning graph, an induction on reachable declarations justifies the claim that repeating every descendant in the outer SemanticContext supplies no additional cryptographic binding.

This does not remove the need to fetch/check unknown meaning dependencies or distinguish multiple foundations. A root digest is a commitment, not the committed data. The note correctly treats new direct-context bytes as new identities and does not claim that changing the representation preserves the old hash.

### N2 — Canonical witness maps and root-level exactness are adequate on paper

Disposition: no new exactness shortcut found.

The fixed key has 37 bytes, hence 296 bits. Patricia branch selection at the first differing bit, nonempty ordered children, and recursive canonicality determine a unique trie for a finite map under the hash-binding assumptions. The bound of at most 296 branch positions is appropriate; it does not assert logarithmic depth against chosen adversarial keys. Fixed node sizes and checked key kinds prevent a new unbounded page object.

Replay2 reconstructs actual needed judgments through selected native references and compares the rebuilt canonical map root against the supplied map. Missing witnesses, extra witnesses, incompatible proof-to-judgment assignments, and selected cycles do not become accepted support. A proof root includes its own selected judgment/proof pair; nonproof roots do not acquire invented proof identities.

Cold root verification need not first materialize a transitive manifest for every interior node. The note's operation bound excludes the separately stated native checking cost and received-trie validation cost, as it should. Warm chain savings are conditional on retained predecessor certificates/environments and compatible mostly unchanged witness selections, not a universal constant-cost graph-merge claim.

### N3 — Certificate reuse remains local and binds the actual interpretation

Disposition: coherent contract, with foundation replacement tracked separately as F1.

The proposed CheckKey binds the typed root, selected reachable witness map, FoundationID, checker image, decoder/adapter, interpretation view, and semantic options. Child certificates are receiver-owned; compatible map union must equal the candidate map. The native environment must use compatible selected witnesses rather than merely matching theorem names/types.

This appropriately prevents a different legacy interpretation table or auxiliary witness map from inheriting acceptance by accident. Physical byte refetch can restore availability without necessarily rerunning an unchanged trusted historical derivation, but a changed checker/adapter/interpretation basis is a different matter. A new resource allowance cannot convert an old UNKNOWN into ACCEPT.

The added ABI contract correctly makes value-preserving native integer conversion a fixed interpretation requirement rather than a tunable CPU/memory limit. Projection/binder/count fields must satisfy their actual native representability and semantic bounds before conversion; ordinary mathematical Nat values remain arbitrary precision. A short term computing a huge arithmetic/shift operand is not made safe merely by bounding surface literal sizes. Unsupported runtime behavior or a stopped/crashed worker yields nondecision/error, never synthesized acceptance. This review checks the requirement's logic; it does not independently certify every selected kernel ABI conversion or arithmetic routine.

### N4 — Relevant guards avoid unrelated retries without claiming invisible freshness

Disposition: sound conditional paper refinement; the complete change-coverage mechanism is essential.

The final writer transaction must establish current checker/profile/policy guards, protection generation/deadline, and incident clearance from the captured view through the actual commit. A bounded complete journal can establish disjointness of intervening exact-key incidents from exact support. If journal coverage is missing, the permitted choices are complete-current-view revalidation within budget or UNKNOWN, not treating missing history as no event.

A broad/unresolved incident trips the conservative breaker before descendants are enumerated. Exact-key checking against a materialized support trie can cost O(kL) for k new keys; this does not make a broad semantic defect, a large journal, or an unavailable support summary a constant-time event. Every identifier class that an incident can target must either occur in that exact support contract or be protected by an applicable broader guard. An approximate structure cannot authorize clearance through false negatives.

The changed global epoch is an observation label, not an unrelated-write rejection condition. Final guarded revalidation supplies the new linearization point; it cannot merely relabel an old successful snapshot as current. Physical loss/expiry still needs the qualified storage fault/protection pathway. Logical reference counts alone do not detect silent hardware corruption.

### N5 — DAG ownership removes repeated pin enumeration under explicit premises

Disposition: plausible selected local mechanism, not an established implementation property.

Registering child edges once on transition into protected state, and retaining already-protected shared subtrees by root/parent references, can avoid another leaf-by-leaf traversal for every use of an unchanged root. Last-owner propagation, storage-generation fencing, and temporary copy accounting remain necessary. Cold protection establishment and a last-owner deletion may still visit a large graph and must be budgeted.

The availability/protection generation must fail closed on detected loss before a positive use can exploit a stale logical handle. The note names that boundary rather than claiming that a hash or reference count proves physical durability. Exact transaction/durability ordering remains a qualification obligation.

## Scoped views and exchange integration

### S1 — Foundation-compatible views are not cross-foundation proof transport

Disposition: boundary is correctly stated; corrected-foundation qualification is still required.

The selected same-foundation view requires equality of the qualified pinned native semantics, seed/bootstrap inventory, reserved-name interpretation, and admitted rules. Legacy objects still must pass their own frozen schema/limits. Such a view can reinterpret representation wrappers only under that exact qualified agreement; it is not a remotely asserted equivalence of printed types.

In particular, replacing an affected kernel with a corrected source commit is not licensed by the fact that ordinary theorem statements and familiar axiom names look unchanged. Exact FoundationID and checker-image changes require the corresponding requalification/rechecking path. A cached old ACCEPT does not repair a known bad checking basis.

### S2 — Advisory metadata has a selected bounded path, not generic CAS access

Disposition: interface agreed across the two proposed notes; byte/schema activation still needs conformance qualification.

ADVISORY_READ1 declares at most four negotiated public manifest hints. Its scope `[2,manifestCID]` permits that owner-disclosed manifest and only its listed typed LibraryView/CollectionGuide data. The manifest, member count, individual payload, aggregate bundle, and entry counts are all bounded. BUNDLE1 serving remains independently funded and disclosure-version checked.

An alias or route citing a mathematical ContentID does not authorize following it under the advisory scope. Instance/rewrite hints remain inert until locally selected bounded activation; no peer source/plugin is executed. Native bytes still require their own public replay/export scope and actual native admission. The remaining work is a precise entry grammar and qualified name/metadata adapter, not a hidden permission to execute annotation text.

The subsequently clarified activation boundary is per-entry: hash/schema-checked bundle bytes may be stored or displayed as visibly untrusted hints without first importing all named mathematics. Installing an alias/native meaning or activating a class/rewrite entry requires the corresponding exact locally checked target interface and applicable policy. One activated entry grants neither automatic activation nor reads for its neighbors. This avoids turning an optional naming/route guide into an unacknowledged bulk-proof-import obligation.

### S3 — FIND_WINDOW is a selected nonprefix mechanism, not a completeness oracle

Disposition: coherent proposed interface; this review is not independent evaluation of its author's ranking heuristics.

The new operation seeks an exact caller-chosen public-descriptor lower boundary in a fixed public snapshot/source list. Replies expose a processed interval and next unprocessed position; matches advance only after output commitment. There is no implicit wrap. Ending a suffix does not claim that earlier keys or other providers were inspected. A new start or continuation consumes fresh admitted work and does not extend the original snapshot lifetime.

This supplies a concrete escape from repeatedly returning an identical prefix. It is not uniform sampling of stored records, proof of relevant-result recall, or a way to manufacture an old ORG1 cursor. Exact public ordering avoids exposing private assessment-bearing descriptor keys. Qualified sought-index and caller-budget enforcement remain required.

The native author independently found and corrected one identity phrasing issue in the reuse note: independently generated identical canonical inductive descriptors can have the same GroupID. Only genuinely different descriptors yield the incompatible-interface example; different source names/authors alone do not.

### S4 — Generation seals preserve only enumerated funded continuations

Disposition: paper safety boundary checked, including two repaired phase details.

A sealed invocation epoch cannot issue or redeem new old-epoch remote work. Existing claimed local work and exact preallocated reply continuations may survive in a bounded enumerated live set with unchanged budgets/deadlines. A computation that already finalized but has an unclaimed fixed reply is now explicitly covered; it cannot fall into a gap between "running parent" and "new remote claim."

An old-origin still-live snapshot/export lease can constrain a **new paid call** without reviving its old CALL. Holder, immutable cut, predicate/planner, disclosure version, and original expiry still apply. The survivor/floor transaction must be durable before old replay keys are forgotten. Live survivors, old result spools, compaction workspace, and finalization records all remain charged.

Bundle range receivers must validate claimed total length against object/local limits and use checked arithmetic before allocation. The author applied that explicit check. Finite-rate examples were also corrected to distinguish an 8-MiB/s no-burst fluid time from the actual `max(0,B-16 MiB)/8 MiB/s` token-envelope lower bound. These repairs do not change the per-object-RPC bottleneck conclusion.

### S5 — Portable export must scale with the new native representation

Disposition: identified frozen-cap dependency has a concrete selected repair.

Removing aggregate native-closure limits and adding BUNDLE1 would not, by themselves, remove the old export's 16-by-4096-object limit. EXPORT_HEAD2 now uses an explicit bounded-page inventory tree, separate operational IDs, checked complete native inventory, and a holder-bound finite export lease. Its pages do not include themselves in their own native set. The scope separately includes exact reachable inventory pages and listed native objects.

The provider cannot hide an unbounded graph walk inside a cheap HEAD operation; an exact inventory must already exist or be produced by separately funded local work. The receiver independently recomputes the native closure and exact inventory equality. A count, page root, or signed export is not evidence that an omitted proof dependency is acceptable.

## Genuine open integration/release findings

### F1 — The old foundation is not suitable for deployment pending soundness repair

Severity: release-blocking trust-basis issue. Disposition: old pin withdrawn; corrected source candidate selected by separate source investigations, with actual deployment qualification still outstanding. This audit did not independently execute a checker or reproduce the source comparison.

During this review, the root author reported post-v4.22 kernel-soundness corrections in official Lean issues/changes 14613, 14577, and 14616/14621, potentially relevant to this profile's raw universe/`imax`, projection, and inductive inputs. This reviewer has not independently completed that official-source comparison and does not claim an executed exploit. The urgent deployment restriction follows the reported finding and the project's own checker-soundness requirement: do not assume the frozen old pin is safe merely because source elaboration often avoids those forms.

The native note now explicitly calls the old pin a historical audit target, not a deployment recommendation. Before a release claim, select and source-pin a corrected qualified basis, reconcile its bootstrap/adapter/expression behavior, and determine how affected old certificates/interpretation views are invalidated or independently rechecked. Archive/source-count datasets can remain historical evidence without becoming an endorsed execution foundation.

Subsequent integration disposition: V2 selects Lean v4.34.0 source `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b` and matching mathlib `5ed2965256430c3649e86755f9576b54eca72435`. The root's [foundation-security note](../analyses/CP-001E-foundation-security-audit.md) and another author's [independent foundation-source audit](CP-001E-foundation-cross-audit.md) record source-only inclusion checks, including release-branch backports and the follow-on inductive helper correction. This reviewer read their decision/scope/source-selection summaries, not the upstream source independently. The selected first Native2 reader disables mixed legacy mathematical closures and requires new identities/rechecking on migration. These are concrete candidate-selection and interpretation decisions; they do not yet establish the qualified bootstrap, source-to-image correspondence, decoder or native replay implementation.

No batching, persistent map, succinct hash, signature, local vote, advisory view, or replay-cache hit substitutes for that repair. A theorem checker is inside the trust basis. The conditional theorems in these notes remain conditional; they are not evidence that a known-faulty implementation satisfies the premises.

### F2 — Custodianship needs one minimal operational status/handoff contract

Severity: material concept-integration gap. Disposition: missing-selection finding resolved by the independently re-read preservation note and its explicit local-only contract selection; the author of this audit subsequently authored the detailed contract and does not claim independent approval of it here.

The custodian role makes the preservation obligation visible, but "preserved under policy P" and "handoff" are not yet mapped to one selected finite status/transfer protocol in the recorded revision. A local policy name is not, by itself, a interoperable receipt or durable remote promise. Existing native read scopes and ADVISORY_READ1's LibraryView/CollectionGuide whitelist cannot silently become arbitrary custody-record channels.

A minimal acceptable selection is local-only custody policy/state plus existing scoped remote RetentionAck observations and exact funded export/import. Under that selection there is no new remote "preserved forever" claim: a successor locally admits/pins its acquired closure, and the original owner obeys its actual release contract. Another acceptable design is an explicitly bounded dedicated custody-status/handoff record and read path, with fixed authority, disclosure, lease, and acknowledgment semantics. The concept should select one, not leave implementation to infer new public record types.

If the policy requires successor acknowledgment before planned release, that condition must be enforced as a local release precondition. If release is discretionary regardless of handoff, the interface must say so. Neither choice can guarantee that a willing adequately funded successor always exists.

Selected disposition: the local custody contract uses finite owner-release-required storage allocations with separately bounded expiring maintenance/import/status jobs. The only initial release authority is an explicit authenticated owner decision. Maintenance-budget expiry does not silently release durable pins; a remote acknowledgment does not automatically release them either. Handoff is independently funded exact acquisition and destination-local activation; the source records limited observations rather than a remote custody-completion guarantee. Custody records remain local and are not smuggled through the advisory whitelist.

The network reviewer found an initial concrete defect: partial release left the immutable all-target scope without explicit per-target ownership. The authored repair adds a bounded TargetOwnershipState map; OWNED/RELEASING targets retain their exact owning roots, RELEASED targets do not contribute ownership, and all rows remain visible under the original immutable scope. Replacement and maintenance commits recheck ownership/state versions and cannot resurrect released targets. Local custody instance IDs bind operational records and status cursors, so a new acquisition of the same immutable target set does not reuse old release authority. The network author independently re-read those repaired ownership, release/replacement, maintenance and status clauses at the recorded hash and reported the defect resolved with no further blocker in those boundaries. This is an operational contract correction, not evidence of implemented crash safety.

## Remaining qualification, not disguised architectural choices

These are real future obligations even after the findings above receive a concept disposition:

- reproduce and qualify the corrected foundation/bootstrap, raw-expression decoder, native constructor adapter, and checker isolation;
- exercise exact trie and export-inventory conformance, including malicious prefixes/counts, missing leaves, extra witnesses, cycles, and incompatible branch joins;
- show actual local native environments can be extended/branched consistently with the certificate/witness keys and that the claimed warm benefit survives realistic examples;
- qualify complete relevant-incident coverage, conservative breakers, storage availability faults, expiry, and crash/commit interleavings;
- provide the actual inert advisory entry grammar and source/name/typeclass adapter without source execution or silent declaration rebinding;
- measure end-to-end discovery, import, replay, and checked application on representative exact library slices, including cold and warm cases and unfamiliar interfaces;
- demonstrate funded durable-preservation participation, current recoverability observations, and capacity/repair load, not merely counts of accepted proofs or signed keys.

None requires a proof that a heuristic is globally optimal. They require evidence for the specific usability, reliability, and resource claims made by the chosen mechanisms. There remains no demonstrated guarantee of exponential useful mathematical growth, complete global discovery, or indefinite survival from finite fixed replication.

## Audit conclusion at this revision

The performance amendments attack actual avoidable bottlenecks rather than merely raising numerical caps. Their strongest soundness boundary remains exact evidence plus a qualified local checking basis, with independent resource and retention authority. Within the bounded paper review, the CTMC calculations and selected native/guard/scoped-data mechanisms are coherent under their explicit premises.

P3 is resolved in the independently re-read preservation note. F2's local-only design selection is explicit, with separate review status for the detailed authored contract recorded above. F1 remains a release blocker until the corrected basis is selected and qualified; a source correction alone will not constitute full decoder/bootstrap/runtime qualification. This checkpoint is not approved for deployment, and no code or executable model was produced during this audit.
