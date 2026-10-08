# CP-001F: foundation evolution without fictitious continuity

Date: 2026-09-20. Status: selected concept amendment and cost analysis; no implementation, source build, proof replay or benchmark. Frozen CP-001E remains unchanged.

## Why this is part of the main operating loop

The [v2 contract](../../spec/OPERATIONAL-CORPUS-V2.md) correctly withdrew a known-vulnerable historical checker and selected a corrected foundation. But a mathematical commons intended to operate indefinitely cannot treat upgrades as a rare unaccounted manual event. Its members will use different toolchain versions, security repairs will invalidate old assessments, and some old artifacts will lack current checking tools.

The goal is not automatic reinterpretation. It is an explicit affordable process for retaining old evidence, producing independently checked new representations when possible, recording what correspondence has actually been established, and keeping operating roles coherent during partial migration.

## Four distinct changes

| Change | Identity effect | Required trust work |
|---|---|---|
| More local CPU/storage or a different transport window | Unchanged native mathematics | Admit actual supplied resources; no old UNKNOWN-to-ACCEPT promotion |
| New executable/build for exactly the same declared foundation/interpretation | Mathematical IDs can stay unchanged; assessment keys change | Qualify image/adapter/runtime correspondence, incident policy and actual rechecks required by local adoption |
| Different pinned Lean native source/rules/bootstrap under Native2 | New FoundationID and normally new native object IDs | New qualification and independently checked target objects; no old ACCEPT inheritance |
| Different hash/encoding suite | New typed bindings for differently encoded data | Exact old/new bytes and qualified mapping; after a genuine old-hash collision, an old ambiguous ID alone is insufficient |

The second row does not license calling an arbitrary corrected kernel source the same foundation. Native2 explicitly includes the selected source commitment. An implementation-independent foundation specification and equivalence proof could support a different identity policy later; neither is silently supplied here. Conversely, a different compiler build of the same declared source does not force new mathematical IDs merely because its binary hash differs.

## Identity churn is a real cost

Every Native2 term directly commits to FoundationID. Definitions, groups, statements and proofs commit to terms or contexts, and replay commits to the foundation and selected objects. Under the no-mixed-foundation rule, re-expression into another foundation changes these mathematical identities even when much of the human-readable mathematics is similar.

Assume a migration selects a finite acyclic native graph G, with B canonical source bytes and V declaration units. For every term whose FoundationID changes, its bytes and ContentID change. Every parent reference to a changed object must then change, inductively through the selected graph. A source-proof filename, display alias, or new checker binary cannot suppress that commitment propagation.

For a full newly serialized target closure, reading and writing the distinct relevant information generally costs at least its byte volume; independent target-native checking adds its actual kernel cost. Physical compression/delta storage can reduce storage overhead, but is a separate qualified recovery representation. It does not establish that the new foundation accepted the old proof or that a root hash supplies unseen dependencies.

An illustrative linear-growth model makes the overhead visible. Suppose the selected corpus at release epoch e has B_e = b e bytes, and every release re-expresses the whole selected corpus. Over q releases, serialization work alone is proportional to

\[
\sum_{e=1}^{q}B_e = bq(q+1)/2,
\]

although the newest corpus is only bq bytes. This quadratic aggregate cost is not inevitable for every growth model: if B_e grows geometrically, the sum is within a constant factor of the latest B_q. Nor does it measure actual Lean performance. It disproves the assumption that repeated whole-corpus migration is automatically a negligible version-label edit.

Changing a vulnerable checking basis may genuinely require broad rechecking. That cost must not be optimized away with stale certificates. Avoidable costs are migrating unused material on every release, rebuilding unchanged local operational indexes unnecessarily, repeated target checking of shared declarations, and assuming every node must migrate every collection simultaneously.

## Selected operating policy

Use **parallel explicitly adopted foundations plus incremental locally selected migration**, not a mandatory latest-version switch.

1. Each node keeps a finite locally adopted foundation/image set and explicit activation states. It may retain archival bytes for more foundations than it currently executes.
2. A still-qualified old basis may remain usable while a new basis is introduced. A basis with an applicable unresolved security incident cannot remain reusable merely to preserve uptime.
3. Discovery descriptors and local clients state exact foundations. Cross-foundation candidates are not silently applicable. A client can independently support several admitted environments within finite resource limits.
4. A node migrates selected owned/reused/public roots under an explicit finite plan. Shared source objects and completed target translations are memoized within that plan and across compatible locally qualified plans where exact keys agree.
5. Unmigrated roots remain historical or currently old-foundation-usable according to their actual state; a partially migrated collection is never labeled wholly upgraded.
6. The first contract creates new target evidence. It does not automatically release any source custody, reinterpret a JudgmentID, or claim semantic equivalence across foundations.

This is not a global consensus event. Communities can choose different adopted profiles. Fragmentation and migration work are real interoperability costs; exact metadata and scoped progress make them visible rather than removing them by assertion.

## MIGRATE1: a local staged operation

MIGRATE1 is an owner-authorized local maintenance/import operation. It introduces no remote opcode, no in-system research assignment and no external execution permission. A remote alias or mapping hint may nominate existing bytes, but cannot start a migration or install its target checker.

### Inputs and finite authority

`MigrationPlan = [planVersion, localPlanID, ownerAuthorityID, sourceFoundationID, targetFoundationID, sourceRootScopeID, translationPolicyID, targetNativePolicyID, capacityVector, deadline, publicationPolicy]`.

The initial source-root scope is a complete sorted duplicate-free array of at most 4096 ReplayIDs and 256 KiB encoded metadata. Larger collections use separately admitted scopes sharing exact cached translations; no assertion of whole-collection completeness spans missing scopes. Every plan has finite source-byte reads, target-byte/metadata/staging allocation, native CPU/memory/I/O, wall time, queues and status allowances, all within node-wide accounting.

The target foundation/image/adapter must already be locally qualified and adopted. A candidate-only foundation can support inert preparatory inspection, but cannot produce an ACTIVE target-native acceptance claim. Source bytes may be from a suspended foundation: they are parsed as untrusted old-format data, not accepted as trusted old theorems. Parsing still requires an exact supported source codec and explicit work budget.

An example local policy permits two active plans, two native migration workers, at most four simultaneously owned target-staging roots, and status pages of 64 root records/256 KiB under two seconds of admitted local read work. These are operating defaults, not a global mathematics limit or measured hardware capacity. The actual byte/check budgets must be specified for each admitted plan; a plan does not inherit a free full-library allocation from its root count.

### Exact translation policy

`TranslationPolicy = [sourceEncodingID, targetEncodingID, sourceFoundationID, targetFoundationID, seedReferenceMap, declarationTranslationRuleID, footprintPolicyID, preservationClaimCode]`.

It is locally selected inert configuration for a qualified translator, not publisher-supplied executable code. The initial rule is syntax-directed native re-expression: preserve binder scope, universe structure and the specified expression-constructor correspondence; map exact old declaration references through their exact already constructed target records; reconstruct checked target groups/opaque bodies through the target-native path. Syntactic correspondence is not a theorem of cross-foundation semantic equivalence. Every seed reference uses an explicitly validated finite map; missing or ambiguous mappings stop that root.

The seed map is **not** inferred from equal names, equal arities or equal printed types. In particular a map between old `String.mk` and new `String.ofList` is a substantive version-specific translation requiring actual type/representation analysis. An equal function type does not prove equal operation semantics. A policy needing an unsupported primitive or unknown proof body returns an explicit boundary rather than importing an axiom.

The initial `preservationClaimCode` is `REEXPRESSED_AND_RECHECKED`, not `SEMANTICALLY_EQUIVALENT`. Exact translation choices and target proof checking establish what the target artifact says and that it checks there. They do not, by themselves, prove that every source primitive, rule or intended statement has identical meaning. A stronger cross-foundation preservation claim requires a separately specified checked interpretation/simulation or explicit target-side bridge with stated assumptions; it is not enabled in this first profile.

### State and traversal

`MigrationRootState = [localPlanID, sourceReplayID, sourceProtectionHandle, stateVersion, phase, traversalCursor, partialTargetMapID, completedTargetReplayOption, targetAssessmentOption, correspondenceObservation, costObservation, failureReasonOption]`.

Allowed phases are PROPOSED, ACQUIRING_SOURCE, REEXPRESSING, CHECKING_TARGET, TARGET_CHECKED, PUBLISHING and COMPLETE; finite failures give DECLINED, INCOMPLETE, CANCELLED or FAILED_TARGET_EVIDENCE. A target-native rejection is not automatically a theorem that the source statement is false. Missing data, limits, unsupported syntax, unknown seed correspondence and checker failures remain distinct outcomes.

The operation proceeds as follows:

1. Reserve the finite plan/grant, staging/control and terminal-state allocations. Capture source-root selection and current source physical-generation protection; no unprotected long traversal is assumed.
2. Obtain exact selected source bodies and witnesses. Producer-side full-evidence acquisition follows the [Lean producer path](CP-001F-lean-producer-client-path.md); a public theorem-as-axiom view cannot fill an absent proof.
3. Traverse the exact selected source DAG with visited/cycle state under the source grammar. Do not perform the old vulnerable check and treat its success as authority. Existing old certificates are provenance/diagnostic input only when source trust is suspended.
4. Construct target dependencies before users, preserving explicit maps of old declaration/proof occurrences to new candidates. Schema/reference conflicts and induced proof-identity collisions require the chosen composition algorithm, not guessing a witness by name. The [composition analysis](CP-001F-proof-identity-composition.md) owns that mechanism.
5. Every target native declaration, selected witness map, complete target replay and actual footprint pass ordinary target admission. Target caches are keyed by exact target objects and current qualified basis, never only by the source root.
6. A target root becomes TARGET_CHECKED only after complete protected local target evidence, native assessment and relevant guards commit. Losing the target grant before that commit leaves no positive target claim.
7. If authorized, publish the target using ordinary exact public-root/index/announcement operations. The mapping observation is local advisory data, not a new externally trusted theorem relation. No frozen advisory whitelist or native relation grammar is silently expanded.
8. Set COMPLETE for that source root only after its selected requested effects actually complete. A failed publication can coexist with a locally TARGET_CHECKED result and must be reported separately. A whole plan completes only for its explicitly named scope with every row terminal and each requested success evidenced.

Locally recorded source/target pairing is useful for locating migrated artifacts and avoiding repeated work. It grants neither remote read access nor mathematical equivalence, and does not import the source body's historical checker assumptions into a target certificate.

### Qualified memoization

An exact local translation cache key includes source typed object, source selected-witness context, source/target encoding, source/target foundation, translation-policy ID, **TranslationContextID**, and translator-image/adapter identity. A target check cache separately binds its exact target-native evidence and current qualified checking basis.

The context binds the finite selected source transformation slice, retained source background, exact capsule-versus-retained-theorem occurrence policy, the already selected target background replay/witness maps, and the exact source-reference-to-target-reference mappings available at this topological step. Canonical commitments to those bounded input records suffice; an unbound label naming a plan does not. No context depends on the output object's own still-unknown ID. A cache may omit a field only under a locally qualified deterministic translation rule establishing that the omitted choice cannot affect this output; such independence is not assumed for the capsule route.

This extra context is necessary because identical source objects and witness maps can be transformed differently when one root's eligible capsule slice includes a theorem that another root keeps as background. Binding the translator executable alone does not select which of those valid calls occurred. The cache hit returns candidate target syntax/correspondence, not native acceptance; the exact target closure, actual footprints and relevant current guards still need their ordinary checks. The [independent migration audit](../audits/CP-001F-migration-cross-audit.md) records this correction.

Caching only an old JudgmentID is insufficient: two proofs of it can use different bodies/support, and different plans can choose different witnesses or translation rules. A source-format parser hit is not a target proof-check hit. A changed target checker with an unresolved incident can invalidate target reuse while leaving the bytes and syntax translation available as inert material.

In a compatible multi-root plan, once a shared old declaration under the exact selected context has been re-expressed and its target checked, descendants may reuse that receiver-owned result. This avoids repeating common library prefixes for each target root. It does not imply sublinear cold checking of the whole selected graph, or O(1) arbitrary merges of incompatible proof selections.

## Storage, custody and crash rules

Source and target evidence can coexist. Migration admission includes temporary double-storage and metadata overhead; the existence of a smaller target proof does not authorize deletion of an exact source-replay promise.

The plan's temporary source protection is distinct from an independent custody allocation. The owner may release its ordinary custody scope while an admitted migration still reads the pinned source generation; the finite migration protection ends under its own actual deadline/termination. If all permitted source protection ends first, the plan cannot continue reading reclaimed bytes or claim successful migration from a partial old closure.

Target custody is a separate newly admitted scope. In Native2, changing a foundation generally changes JudgmentID, so even JUDGMENT_RECOVERY custody does not automatically accept the new target as satisfying an old exact target. A cross-foundation source release is an explicit owner risk/contract decision, not an inference from a COMPLETE migration record.

Durable target staging precedes positive state commit. Crash recovery conservatively terminalizes interrupted claims, preserves exact completed objects under their surviving allocations, and never treats an unfinished translation as a successful target check. Resuming after a crash requires fresh local authority and exact recorded progress; prior charged work is not refunded. A new admission epoch or source mapping label cannot reset the plan's resource history.

Plan results and immutable target objects may outlive bounded detailed job history. Compacting progress records cannot forget live protection, unsettled allocations, incomplete-publication state or the exact rule needed to justify a still-used target assessment. Detailed old source correspondence can be discarded only if no promised preservation/recovery operation depends on it; the target's own complete proof closure remains sufficient for native reuse.

## Honest status and growth accounting

Report separately:

- selected source roots, fully examined source roots and missing-body/syntax-boundary counts;
- target roots independently checked and currently reusable;
- target roots actually published and acknowledged only under their ordinary limited service meanings;
- newly supplied canonical bytes versus bytes representing re-expression of prior selected content;
- current exact old/new custody coverage and explicit owner releases;
- checked semantic bridges, if a future qualified bridge profile is actually used, versus merely advisory source/target correspondence;
- source parsing, translation, target checking, temporary peak storage and publication costs.

Counting every new target JudgmentID as a new mathematical discovery would inflate growth whenever foundations change. Conversely, declaring all paired statements semantically identical without bridge evidence would overstate deduplication. The selected baseline reports **version-induced re-expression** as a separate operational category and makes no universal semantic-novelty count.

The commons can still obtain useful new target evidence even when a stronger preservation relation is unknown. That evidence is valid only under its exact target basis and content. This distinction permits practical migration without requiring a solved universal theory-equivalence problem or hiding the user's requirement for trustworthy results.

## Upgrade supply and decentralization

The runtime protocol has no central theorem server. That does not eliminate software-supply trust or generate qualified new checker binaries autonomously.

A local owner may preauthorize a finite update policy naming accepted distributors, source/build attestations, independent review criteria and staging resources. Discovery of an update is nonauthorizing input. Installation and activation are local authority transitions after that policy's actual qualification conditions are met. Mathematics traffic cannot install the update, choose a new axiom basis or clear a security breaker.

Multiple mirrors or signers improve some availability/compromise scenarios but do not prove source correctness or independent review. A software distribution bundled with a corpus archive is still inert until locally installed through the separate policy. No shared root goal, universal signer, global vote or blockchain history is required.

If no qualified replacement is available after a broad checker incident, preserving bytes and suspending affected native reliance is the correct outcome. A concept cannot promise both unconditional continued trusted proving and freedom from every future checker defect without supplying the missing sound checker. Other unaffected qualified foundations and local archival services may continue within their actual scope.

## Required adversarial cases

- An old profile is suspended, but all old bytes remain available: old ACCEPT does not transfer; only independently checked target outputs can become reusable.
- A seed map swaps two equal-typed operations: a checked target artifact is not falsely labeled a semantic-preservation proof.
- Two source roots share most declarations but select incompatible proofs: exact-context translation caches do not substitute one source witness silently.
- Target checking succeeds, publication fails: status distinguishes local target knowledge from remote dissemination.
- Temporary double-storage cannot be admitted: source evidence remains protected; no delete-first migration is performed.
- Source custody is released during an admitted translation: only actual remaining finite read protection permits continuation.
- A new target foundation is merely CANDIDATE: no ACTIVE target proof claim is manufactured by migration.
- A crash occurs after target bytes are durable but before acceptance commits: bytes survive only as inert/protected data under the actual recovery state.
- A year of profile updates produces many new IDs for related old content: growth diagnostics expose the re-expression volume instead of calling it exponential discovery.

## What this amendment does and does not solve

It replaces vague upgrade/re-export language with a selected local operation, cost model, source/target authority distinction, cache keys, custody transitions and truthful progress observations. It avoids a compulsory network-wide full-corpus rewrite while retaining independent target checking.

It does not provide an executed exporter, universal source-to-target translation, full new bootstrap inventory, semantic-equivalence oracle, or evidence that all future updates will be affordable. Those remain specific qualification and supplied-resource conditions. The source and composition audits may identify further mandatory refinements; their actual findings must be integrated before CP-001F is frozen.
