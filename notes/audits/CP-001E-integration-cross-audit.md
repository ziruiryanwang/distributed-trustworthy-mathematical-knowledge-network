# CP-001E integration cross-audit: exchange, custody and current reliance

Date: 2026-09-20  
Reviewer: independent exchange/decentralization subagent  
Evidence boundary: paper specification audit; no implementation, native proof execution, benchmark, executable model or conformance test

## Scope and conclusion

This review reads the integrated v2 contract against the selected exchange, native, reuse and custody mechanisms. It concentrates on actual selected fields and transitions: bounded byte transfer, exact disclosure membership, native current-use guards, clean-generation sealing, and durable ownership during maintenance/replacement/release. It is not a new claim that the mathematical kernel, adapter or physical storage implementation has been verified.

The reviewed integration resolves the transfer/schema findings below, including the inherited optional-field encoding mismatch. No further concept-level contradiction was found in this review's scope. This conclusion neither makes v2 deployment-qualified nor promises that all future implementation defects have been discovered.

The full v2 draft and selected analysis notes were read in this audit sequence; repaired passages were reread. The foundation-security note was read as source-evidence input. Its upstream observations were not independently reproduced by executing exploits or native builds here. Frozen CP-001D files were not changed.

## Findings and dispositions

| Finding | Why it matters | Selected repair and disposition |
|---|---|---|
| INT-01: successful streamed body lacked the result-code field required by prose | A receiver could not apply the stated grammar consistently | BODY_START now includes `resultCode`; successful typed bundles require code 0; failed top-level calls use ordinary bounded RESULT. Closed on paper. |
| INT-02: existing outcome digest and new stream digest were not explicitly related | Two independently interpreted result commitments could disagree about the exact response | Distinct domain-separated BODY and OUTCOME formulas bind the exact call, status, body length and canonical body. START/END and metadata length agreement is explicit. Closed on paper. |
| INT-03: bundle cardinality/order and failed-item payload shape were insufficiently fixed | Omitted/duplicated ordinals or status-dependent hidden metadata could be interpreted inconsistently | Exactly one row per request in ordinal order; OK_SLICE carries the exact CID/length/offset/bytes; other item codes carry no private object metadata. Closed on paper. |
| INT-04: general schema-2 wording also appeared to bump newly allocated schema-1 export types | Two peers could hash identical intended objects under different typed schemas | The bump now applies only to reused NET1 types; new inventory/head types remain `0x8020/1` and `0x8021/1`. Closed on paper. |
| INT-05: export-head version and successful response body were not selected | Knowing the conceptual head fields did not determine what bounded response arrives | Version is 2; successful RESULT carries `[headCID,headPayloadBytes,inventoryRootNodePayloadBytes]`, with both CID checks and field/bounds checks. Closed on paper. |
| INT-06: BUNDLE1 absent `publicAssessmentDigestOption` used `[]`, while inherited NET1 metadata uses tagged absence | This is an avoidable ambiguity in an expressly retained field layout | Repaired to `[0]`, retaining `[1,value]` for present; the separate new-field advisory `[]/[value]` convention is explicitly distinguished. Closed on paper after rereading the repaired passage. |
| INT-07: exchange prose referred to a separately signed head/issuance record without a selected head signature wrapper | A signature requirement must identify exact bytes and wrapper, or it is not interoperable | Repaired the exchange note to name the content-addressed head carried by the authenticated response. Current lease authority resides in the issuer's live local lease state; offline possession is not live authority. Closed on paper. |

Earlier cross-review also found that partial custody release needed explicit target ownership, rather than merely retaining an immutable original target list. The custody author added `TargetOwnershipState`, local custody-instance binding, exact shared-root ownership, guarded replacement, and per-target status. Those repairs are incorporated by v2's normative reference and pass this integration review.

## Transfer scope, breadth and depth

The read-scope trichotomy is preserved:

- Public Replay scope authorizes its exact currently disclosed native closure, including binding native trie nodes.
- A live holder-bound export scope additionally authorizes reachable operational inventory nodes and its head. Native leaves exclude operational inventory nodes, avoiding recursive self-commitment.
- Advisory scope authorizes only the exact explicitly disclosed manifest and whitelisted advisory members. References inside these pages do not authorize further native, advisory or arbitrary CAS reads.

Knowing a hash is not authority to read arbitrary locally held data. An authenticated peer's scope membership is still checked by the provider; a receiver independently funds parsing, staging, closure discovery and native checking. Scope withdrawal, separate computation/delivery tickets, physical-generation read pins and bounded spool lifetime remain effective. A completed provider computation is neither a completed delivery nor a receiving node's mathematical acceptance.

Bundle cardinality, request bytes, payload bytes, metadata and per-fragment sizes all have separate finite limits. Checked range arithmetic precedes allocation; object CID verification requires complete reconstructed canonical payloads. An interrupted body can leave independently verified inert objects under explicit staging authority without pretending that the whole service succeeded. Retry grants no free budget reset.

Large closure support removes a global fixed cardinality ceiling, not finite local resource admission. Mathematical dependency depth, bounded trie depth, object count, bytes, memory, native conversion cost and active-transfer lifetime remain different limits. BUNDLE1 reduces paid-call overhead where identifiers are known; a previously unknown dependency chain still imposes causal discovery rounds. Persistent export maps make warm exact-delta updates bounded by path copying, but cold completeness still requires complete native-closure reconciliation. The `2N-1` inventory-node cost and possible `3N-1` combined object count are explicit.

## Generation sealing and active-use guards

A seal advances the floor for new remote invocation; it does not act as a crash. Old OFFER/CALL messages cannot create new work after the seal. Precisely enumerated claimed work and already allocated fixed reply continuations may finish under unchanged allocations/deadlines, including a FINALIZED computation whose exact reply remains RESERVED. Snapshot/export leases survive only as finite data scopes usable through newly paid calls. Actual recovery generation, warm-retention time origin and cumulative spend remain separate.

Therefore the following implications remain invalid:

`old live export lease => old CALL may execute again`,

`clean admission seal => fresh maintenance funding`,

`historical native ACCEPT => currently reusable evidence`.

Current reuse requires qualified exact checking, complete protected local selected evidence, current local policy and absence of applicable blocking incidents. The authoritative writer revalidates relevant guards at its commit boundary. Unrelated newly imported mathematics need not invalidate an old scoped clearance; missing incident-delta coverage instead requires current-state revalidation or nondecision. A broad unresolved incident blocks reliance before an expensive descendant walk. Binding context, replay, map, seed/rule and interpretation objects belong to support; checking only leaf theorem IDs would miss affected evidence.

The revised advisory section also distinguishes complete bounded bundle conformance from per-entry semantic activation. All listed advisory payloads must satisfy byte/schema/entry-count bounds before activation through that bundle. Activating one entry then requires only its own exact mathematical prerequisites, not importing every mathematical target mentioned by the bundle. Neither layer supplies missing proof premises.

## Custody and maintenance conservation

The selected custody interface remains local-only. No new remote opcode, advisory member type or signed permanence certificate was silently introduced. Owner-authorized durable ownership is separate from finite maintenance funding and from temporary read/export pins.

For a custody instance S, `OwnedRoots(S)` includes current selected roots of OWNED or RELEASING target rows, never RELEASED rows. The original scope remains immutable historical selection; per-target state determines present ownership. A release transaction removes only the selected owning references. Another target, another scope or an active export/use can still protect shared bytes. Physical reclamation remains a later metered generation-aware operation.

Replacement of judgment-recovery evidence first checks and protects a permitted proof of the same exact JudgmentID, with temporary double-storage admitted. Its commit requires the exact still-OWNED target and current custody/ownership versions. A concurrent release defeats that commit; it does not convert stale work into renewed ownership. EXACT_REPLAY cannot replace its promised bytes with a different proof merely because the statement is alike.

Maintenance expiry marks maintenance degraded/paused, not implicitly released. A stale maintenance cursor cannot reacquire a released target. A remote RetentionAck or successful byte read is a scoped observation, not proof of perpetual service or an automatic source-release condition. Native-basis suspension can coexist with complete protected historical bytes. Refetching the same bytes repairs availability only; it does not repair a suspended checker.

## Remaining qualification obligations, not hidden contract choices

The selected foundation is Lean v4.34.0 at the exact source pin stated in v2, not the withdrawn historical v4.22 candidate. The actual newly derived bootstrap/native-rule/reserved-name bytes and qualified adapter/image are release inputs still to be established. This is acknowledged, rather than a permission for a publisher or implementer to substitute seed meanings. No old native acceptance migrates across a changed foundation source merely because the source-language statement looks unchanged.

STRUCT2 remains an optional research extension without an instantiated interoperable extractor; ordinary exact queries/STRUCT1 remain the selected baseline. Custody local records are conceptual local interfaces, not falsely advertised interoperable wire types. Full future transport/codec conformance, real library object/closure measurements, native checking cost, crashes, fault races and useful reuse must still be exercised before deployment claims. Source-file counts are not native-closure measurements.

## Exact reviewed inputs

These hashes identify the reviewed bytes, not a signature, deployment approval or proof of correctness. A subsequent semantic edit requires re-review of its affected claims.

| Document | SHA-256 |
|---|---|
| `spec/OPERATIONAL-CORPUS-V2.md` | `B3A339FEF326D6E9F195A6BD186457B294ACFC1935B14B74C113C8E4C33B4A91` |
| `notes/analyses/CP-001E-exchange-scaling.md` | `4BB30F0CCCEC9019EAF6CFF337F5280795FE23F7FA4CD462713E808CB9DB4426` |
| `notes/analyses/CP-001E-custody-contract.md` | `914E2C9AB6FB41F4927AAA7CA03646D38876D2708E7FEB1956CAF23AF99893B2` |
| `notes/analyses/CP-001E-native-scaling.md` | `2CDFD32A0282E6100C15DB1233FB163F0966CA520A3B5A4EF370C24A606BC537` |
| `notes/analyses/CP-001E-agent-reuse-and-discovery.md` | `0525E8DD334B0EA6F0B6DDF099D9A42A2A6A06AFEFAB370F9D403502318796B0` |
| `notes/analyses/CP-001E-foundation-security-audit.md` | `C7393FBF236A2C4DDE41E32597B6733D9D4B04481B1F8BF46CC11D7B542EDFE7` |
| `spec/OPERATIONAL-CORPUS-V1-NETWORK.md` (unchanged frozen baseline) | `46529C8040D8D58F9CB6C27FB4DBC148C525AFC0B0FCCA49788A71FD2136871B` |
