# CP-001K optional-policy selection audit

Date: 2026-09-20. Reviewer: `qualification_contract_review`, independent of root's checkpoint authorship. Scope: integration and selection claims only. This reviewer also authored the separate resource/lifecycle audit; that earlier work is identified below, not presented as another independent implementation audit. No source file or previous audit was edited. No implementation, native execution, extraction, executable model or benchmark was performed.

## Exact reviewed cuts and disposition

**No remaining blocking integration issue found.** The final K checkpoint faithfully selects the reviewed CACHESEL1 owner-local policy without broadening its authority, capacity or usefulness claims. V6/I remains the network/native baseline, J/VIEWS1 remains unchanged, and all actual qualification remains NOT RUN. The overall project goal is not complete.

| Artifact | SHA-256 |
|---|---|
| Initially read candidate K checkpoint | `0867AA70F09CC83D066C9BB5A5426B4231B9B04FAFD5672C1BD3F42C65D7B023` |
| [Final K checkpoint](../../../../notes/checkpoints/CP-001K-local-cache-feedback.md) | `D84E65507FBFD80D44C7773AA27ACE3228C6201DF2E6A26A778B7D5CC59F1EE1` |
| [CACHESEL1 source](../proposal.md) | `1B3530AD271F1CCD106445D6A7CE941D5BD516E03C2CB9C5876751A9EF9C99BE` |
| [Independent signal-policy audit](signal-policy-audit.md) | `01824A2F4EDAF35443E0A53A563086724843624507C68A92D26B3AF3BDFA7C35` |
| [Separate resource/lifecycle audit](resource-lifecycle-audit.md) | `F767C27DFAE8488955EF0C0E901F9C98D6E5116F23EB7BE01C7A5E51DD04D16A` |

The reviewer read both complete checkpoint cuts, confirmed these hashes and read the complete signal audit. The repaired source and lifecycle audit had already been read completely in the immediately preceding exact-cut review and were rechecked unchanged. This bounded review compares their integration with [V6](../../../../spec/OPERATIONAL-CORPUS-V6.md), [J](../../../../notes/checkpoints/CP-001J-unfamiliar-interface-entry.md) and the inherited custody/retention boundaries; it does not reopen every inherited specification.

## Integration checks

| Seam | Inspected conclusion |
|---|---|
| Selection authority | K selects one optional owner-local discretionary policy. Its exact source remains authoritative for transitions and limits; the unchanged proposal-stage source header is historical, not a competing unselected algorithm. No V7, wire operation, foundation rule or network-wide policy is introduced. |
| Mathematical authority | Checked applications can inform bounded local retention; they do not certify value, publish a result, create durable custody or replace native acceptance. Current P4 bundles retain exact evidence bindings, and an old witness's use score does not establish a replacement's earlier conversion/application behavior. |
| Signal and family scope | One exact judgment is a family, not four separate votes for its P4 alternatives. Once-settled applications, four credited families per event, three saturating daily bins and the 21-point bound are faithful. Zero means no retained credit, not no demand. Genuine cheap-use inflation remains an explicit defeat. |
| Selection limits | K correctly states one zero-history slot and three additional reuse slots; the latter may also choose zero-history families. Four winners, 64 rows, 64 observations, 16 charged term allocations, one round in flight and interval nomination/round ceilings remain subject to the source's smaller work and parent limits. Unknown resource fit is not free capacity. |
| Nomination, renewal and phases | K preserves the one-shot explicit nomination fence, once-only due renewal decision, complete-planning gate, no term from incomplete planning and guarded partial commit only after COMMIT begins. Its reference to a fresh **eligible** nomination does not bypass the source's prohibition while old term/reservation/unsettled obligations remain. |
| Logical union versus physical stock | Shared closure admission and future term fit remain distinct from temporary coexistence, metadata, settling and generation-aware GC. Expiry removes only the lawful cache handle; it does not release another owner, use/export, snapshot or anchor or pretend its bytes are reclaimed. |
| Numerical and timed examples | The 11-unit A/B cache, 19-unit supplied transition payload, C's 21-point defeat, 15-to-16 renewal with control peak 2.2 within 3, and full-16 refusal match the source. The 19-to-12-to-5 active union is not reported as immediate physical reclamation. The added `3 + 3 + 1` prior-admission explanation fits the existing round/nomination limits and introduces no new scheduler or grant. |
| Review and evidence claims | K attributes CS-SIG-001 to the signal review and CS-LIFE-001/002 to the lifecycle review at their actual shared repaired cut. It distinguishes these paper closures from independent integration and from actual software qualification. The six native and eight reciprocal evidence gates remain NOT RUN; no measured cache, resilience or useful-growth result is borrowed. |

No mandatory public task list, shared research agenda, human-intention test, global utility consensus or political attribution mechanism is added. A safe refusal can remain unproductive, and a useful heuristic need not be optimal. Later evaluation must preserve failed admission, lost signals, exposure and maintenance costs rather than treating selection as evidence of benefit.

## Final status delta and freeze boundary

After the candidate-cut read found no substantive integration issue, root changed three passages: the selected-status header and audit/manifest links; removal of “once selected”; and replacement of the pending-review paragraph with the candidate read result and exact-cut/freeze scope. The reviewer read the final file completely. Reversing only those three replacements in memory reproduced candidate SHA-256 `0867AA70F09CC83D066C9BB5A5426B4231B9B04FAFD5672C1BD3F42C65D7B023`. No algorithm, limit, result or benefit claim changed in that final delta.

The checkpoint's manifest is a planned five-artifact freeze: source, two source audits, this integration audit and final checkpoint, excluding the manifest itself and mutable navigation. At this review handoff the manifest has not yet been generated. This audit therefore confirms the final checkpoint/source/review bytes and their selection scope, **not** a completed manifest-row check. Root must record that later integrity check against the emitted manifest without modifying these reviewed bytes.

Closure is only at the exact cuts above. Changed observation identity, nomination/renewal states, phase disposition, evidence bindings, union accounting or release/recovery authority require targeted review. Empirical tuning does not inherit an unmeasured benefit, and a later implementation cannot inherit runtime qualification from this Markdown audit.
