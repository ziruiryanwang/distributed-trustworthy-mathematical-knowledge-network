# Routing-recovery composition audit

Date: 2026-09-20. Reviewer: `egress_composition_audit`, independent of the source author. Scope: routing observations, conditional recovery, foreign lease/disclosure boundaries and composition with existing F/H/M contracts. Detailed joint resource/calendar feasibility has a separate reviewer. No implementation, extraction, native execution, executable model or benchmark. Only this audit is edited.

Final disposition: **RR-COMP-001 and the later root-raised RR-COMP-002 are closed at source `72ED31CCDC22975784C94AC3F15D6244E83E76444ECE70E214B3FAFBD1C58292`. No remaining blocking routing/status/composition issue was found within this review's scope.** Initial findings below are preserved as history. This audit does not itself select the policy or qualify any runtime behavior.

## Initial held source and disposition

The complete [routing-recovery source](../routing-recovery-contract.md) was independently hash-confirmed and read at SHA-256 `653FD87EB766141D920B6BACF4BC62C7C2F106BF4A46C7B08D30FC222AB6FF30`.

At the initial cut, **RR-COMP-001 required a precise temporal-reference and foreign-eligibility clarification before this review could close.** The other inspected composition seams were conditionally coherent, as recorded below. This finding did not establish that the underlying recovery proposition is false when its attained service/retention premises genuinely hold. It concerned the interpretation and sufficiency of those premises in the numerical witness. Root independently raised the same timing seam; this review records its own source check, not exclusive discovery credit.

Inherited passages checked include [F ROUTE1](../../../../notes/analyses/CP-001F-dissemination-and-routing.md), especially lookup termination, partial/exhausted results, snapshot interpretation and the conditional reachability proposition; [F exact coverage](../../../../notes/analyses/CP-001F-exact-routing-coverage.md), especially actual four-copy placement, direct old-group renewal and the separate routing-refresh cursor; [H shared coverage/resources](../../../../notes/analyses/CP-001H-resource-supply-and-discovery.md); and [M/EGRESS1](../../../../notes/checkpoints/CP-001M-producer-egress-selection.md). This is not a fresh audit of all inherited native or network mechanisms.

## RR-COMP-001: temporal reference and observation-cut binding

Classification: **under-specified supplied timing premise**, not a new cryptographic defect or a requirement for synchronized network clocks.

The eight-day example combines owner-calendar days and renewal windows, remote 48-hour group extensions, fourteen hours of initial lease headroom, elapsed control-call bounds and the proposition's Δ/L/P. It does not explicitly identify the common analysis-time model or the clock/progress relations that make these quantities comparable. F's signed/local lease observations alone do not supply that relation.

### Smallest defeating interpretation

An honest holder's valid monotonic clock advances sufficiently faster than the owner's. The owner dispatches renewals twelve of its hours apart. A granted 48-hour duration in the holder's clock can expire before the next owner-calendar renewal, although the owner retained a genuine successful earlier receipt and every owner-local accounting rule behaved correctly. Calling that receipt forty-eight universally comparable hours would hide a failed service premise.

This is a countercase to inferring the numeric lease coverage from unspecified clocks, not proof that ordinary qualified deployments have that clock behavior. A stipulation of compatible advancing clocks or directly attained eligibility can exclude it; that stipulation must be visible rather than inferred from a duration field.

### Required clarification

State a reference elapsed-time interpretation for the mathematical witness and the sufficient supplied clock/progress/headroom conditions for its calendar. Distinguish those external assumptions from actual node-local clocks and admission authority. The protocol need not acquire a global clock, roster, synchronization service or remotely comparable expiry timestamp.

For the recovery-to-discovery implication, require actual ad/marker eligibility at the relevant holder ROUTE_LIST snapshot/read cuts, with the necessary actual service and disclosure authority. Receipt age or successful source dispatch alone cannot certify that foreign condition. Native acquisition and mathematical reuse retain their own later current guards.

Do **not** replace F's historical-page semantics with a live-at-delivery requirement. An ad present at an admitted snapshot cut may lawfully be delivered after its lease expires, subject to inherited reply-disclosure checks, while still reporting only that historical cut. That reply does not establish current routing eligibility, future source service or successful acquisition. Ordinary lease expiry and actual disclosure withdrawal remain distinct.

## Other initial-cut composition checks

| Seam | Inspected conditional result |
|---|---|
| Honest-join counterexample | Old h1–h12 refuse placement while h13–h16 retain four copies. Four closer arrivals displace those retainers from a newcomer's nearest sixteen. The newcomer can miss despite sound mathematics, healthy old renewals and honest services. This correctly isolates routing displacement, not evidence loss or a malicious attack. |
| Scheduler versus environment | The proposal separates a funded maximum fresh-start gap from actual useful contact reachability, destination admission and reader overlap. A closed incumbent contact graph, unbounded response delay or refusal defeats recovery despite repeated scheduled attempts. Mere fair cursors or quiescence do not imply a finite recovery bound. |
| Post-change freshness | The proposition requires a new lookup after t0. A pre-t0 in-flight lookup cannot satisfy that premise merely by completing later. The finite scope's ownership/path/eligibility changes invalidate affected old-cut claims without discharging actual obligations. |
| Δ+L+P | Given the stated attained premises, choose fresh start s ≤ t0+Δ, lookup completion by s+L and actual placement by s+L+P. The bound follows by addition. Reader traversal needs its own extra R; metadata discovery is not complete acquisition or checked use. RR-COMP-001 concerns the temporal and eligibility interpretation, not this arithmetic. |
| Completion status | F normal completion requires at least sixteen successful contacts and all closer-candidate settlement conditions. CLOSEST_SEEN is not a proof of the globally nearest set. Attempt age, completed-lookup age and eligible-placement observations remain distinct; failed/partial attempts do not reset a completed-refresh age. |
| Four-RPC interpretation | Four-way concurrency is not four total calls. A four-call-limited PARTIAL lookup or genuinely shorter exhausted frontier can provide actual usable contacts for independently paid reads/placements. It cannot establish normal sixteen-contact completion. H's retaining-holder overlap premise can make such a narrow path useful without granting the general nearest-set guarantee. |
| Key scope versus mathematics count | S counts provider/key/cell-path obligations, not target IDs. The main example explicitly covers 16,392 initial keys. Additional daily scopes and new mathematical outputs do not silently enter that same recovery guarantee. Deeper routes require separately supplied marker recovery; the numeric witness is depth zero. |
| Placement and old protection | A successful lookup is not four accepted rows. Actual OPEN/PUT/DROP/CLOSE guards remain in force. Nonempty old groups are not closed merely because one key moves; same-holder owner changes retain DROP-before-PUT gaps. Old and uncertain rows, group generations, snapshots and custody remain charged under their real lifetimes. |
| M coexistence | This policy refreshes admitted F/H routing obligations. M deliberately selects native-only known-contact exposure and refuses targets already included in automatic F/H cuts. Coexistence does not automatically route M's outputs, extend their public horizon, create new owner authority or release their custody. A distinct routed-publication admission remains necessary. |
| Authority and implementation | No new wire operation, global membership authority, compulsory mathematical task, truth vote or native acceptance shortcut is introduced. A local policy can enforce finite work and honest outcomes; it cannot guarantee foreign willingness or future retention by naming a schedule. |

The eight-day case is a conditional paper workload, not an actual route measurement, successful Lean exchange or independently observed recovery. Numerical supplies and calendar feasibility are also subject to the separately assigned resource review. All runtime qualification remains **NOT RUN**.

## Initial review handoff (historical)

At the initial held source, RR-COMP-001 is open. Root is coordinating one source repair with the independent resource review. Closure requires an exact repaired source hash and complete reread; an author's assurance or a successful arithmetic calculation alone is insufficient. No source or frozen document was edited by this reviewer.

## Repaired-source review and final closure

The reviewer independently hash-confirmed and read the complete coordinated repair at `65B395B47DE0CD86EB802C30409276E5202416ADB334378B52EB126846D8F605`, then independently hash-confirmed and read the complete final clarification at `72ED31CCDC22975784C94AC3F15D6244E83E76444ECE70E214B3FAFBD1C58292`. Closure binds the latter exact source, not an author message or the initial wording.

### RR-COMP-001 closure

The numerical witness now explicitly uses one mathematical elapsed-time parameter, continuous unit-rate owner/holder monotonic clocks with arbitrary offsets, uninterrupted scheduling and the stated actual response/grant/headroom assumptions. This is an analytic service model, not synchronized protocol timestamps or permission to compare arbitrary foreign clocks. Incompatible drift, clock discontinuity or insufficient actual eligibility invalidates that witness rather than silently extending a lease. A received duration alone cannot establish the premises.

The reader implication expressly requires actual ad/group/marker eligibility and service/disclosure authority at the relevant holder-authoritative ROUTE_LIST snapshot/read cuts. The separate following paragraph preserves lawful historical-page delivery after ordinary lease expiry, subject to existing disclosure checks. It does not impose live-at-delivery routing eligibility, relabel history as current service, or weaken the later native acquisition/current-use guards. Actual disclosure withdrawal remains distinct from ordinary expiry.

These changes resolve the initial cross-clock/foreign-eligibility ambiguity while preserving the intended conditional proposition. **RR-COMP-001 is closed at the final source above.**

### RR-COMP-002: scope owner versus physical placement references

After the coordinated repair, root identified a distinct wording ambiguity and requested independent checking. The generic rule that a change in "row ownership" invalidates the old-cut recovery claim could be read as invalidating that claim when the policy performs its own successful holder/group replacement. Fixed S, stable ownership and the distinct-holder fixture supported the narrower intended reading, but did not make the generic phrase precise enough.

The final scope-stability paragraph now distinguishes the admitted provider/publication-scope owner and provider/key/cell-path obligation from mutable physical holder/group/row references. Guarded replacement of those physical references within that same obligation is explicitly the recovery transition, not invalidation by itself. Actual scope-owner/membership, cell-path or disclosure/native-eligibility changes still require revalidation and new admission. All actual old/new owners, versions, placements, uncertainty and costs remain in the existing guarded ledger; an intended destination is never an observed placement.

This is a scope-identity clarification, not a new routing operation or exemption from concurrency guards. The reviewer reversed only that final paragraph in memory and reproduced prior repaired SHA-256 `65B395B47DE0CD86EB802C30409276E5202416ADB334378B52EB126846D8F605`. No other source delta was hidden in the final repair. **Root-raised RR-COMP-002 is closed at the final source above.**

### Continued composition and evidence limits

The final full reread retains the following boundaries:

- A fresh post-t0 start, attained useful frontier, actual destination admission and reader overlap remain separate premises. The Δ+L+P result does not infer any of them from a successful local dispatch or CLOSEST_SEEN.
- The repaired calendar counts a paused maintenance occurrence as retained execution state, independently of serialized actual calls. New side targets complete their actual checking/protection/export/index work before routed placement; their input scopes remain pending rather than falsely reporting completed tier consolidation. These cross-stage meanings are coherent. Their detailed numeric/service feasibility remains the separate resource review's scope.
- The eight-day gap applies to the admitted main obligation set and actual continuing funding. New side scopes do not inherit it automatically, and a boundary-crossing claim requires the next cycle's actual authority. Unsettled tails cannot be discarded to repeat a one-cycle stock bound.
- Old-group renewal, ordinary lookup completion, actual retained placement, historical returned leads and checked mathematical reuse stay distinct. Honest join displacement and permanent failure under inadequate contact reachability or admission remain valid defeating executions.
- Four-RPC partial/exhausted observations remain usable only at their reported scope; they never become normal nearest-sixteen completion or the general F convergence guarantee. The full-size recovery witness reserves up to 64 routing calls per managed key instead.
- Existing F/H publication owners, marker paths, guarded row operations, disclosure and custody obligations remain authoritative. M's known-contact native exposure gains no routed publication or longer retention merely because this separate refresh policy exists.

No new wire format, global membership authority, synchronized clock service or mathematical acceptance shortcut is introduced. No machine execution or measured route/native performance occurred. **Qualification remains NOT RUN**, and the whole-project operability/growth goal is not completed by this review. Further changes to scope identity, time interpretation, foreign eligibility, lookup/placement statuses or the controller-versus-environment premises reopen the affected review.
