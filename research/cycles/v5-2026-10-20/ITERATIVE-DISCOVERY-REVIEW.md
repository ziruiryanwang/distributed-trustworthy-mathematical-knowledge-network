# Iterative discovery: independent source/theory challenge

Reviewer: core_release. Canonical root is
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
No implementation, import, test, native/proof or network operation was run.

## Verdict

**Provisional GO for the four-source opt-in direct-contact successor**, with
the concrete requirements below. Read SEAM `a056a883` and CONTRACT `989e70f6`.
The selected 110-source map is input `e0e22f41`, not historical logical paths.
This is a real operation-lifetime restriction, not a missing agent strategy.

`workspace_atomic.find` and `direct_contacts.bind` share one `_query_used` slot.
`AcquisitionBudget.charge_external` rejects prepayment after its sequence leaves
zero; `EvidenceAcquisition.close` closes that shared budget. Multiple queries
cannot safely be added by resetting a flag, constructing another grant or
reopening the budget. Existing one-shot callers and located find must stay intact.

## Nonrenewal argument

Fix original budget B, search reservation S, absolute deadline Ds <= D and
generation cap q <= 8. Prepay search requests/reply bytes into B exactly once,
before any search/acquisition; leave positive intended acquisition capacity.
For every committed generation charge a_i, require sum a_i <= S over all seven
additive dimensions. Each actual search is bounded by its unchanged session a_i;
failed/unused allocations are not refunded. Acquisition still debits B. Hence
search plus acquisition is bounded by B in shared dimensions and S elsewhere.
The induction requires all entry points to retain the same B, owners, grant,
namespace/policy and Ds. Query choice may adapt, but these identities/caps may not.
Inflight is a fixed cap, not an additive resource; each session's cap must not
exceed it. A shorter per-query wall cap never recomputes Ds as a fresh deadline.

## Required changed-boundary details

1. **Retirement must be real.** Set the old SearchSession state non-ACTIVE;
   merely detaching it leaves retained `SearchClient` references usable. Tombstone
   old EvidenceAcquisition without closing B, expire/reject its structural path,
   invalidate contacts and clear offers. Old `close()` must not close a new
   generation's shared budget. Use no budget resurrection or replacement issuer.
2. **Quiescence precedes replacement.** Existing serialized client guard plus
   zero search tickets/reservations, B.pending=None and structural inflight=0
   are prerequisites. Cancelled work must be awaited and charged. Commit the new
   allocation before I/O; any uncertain retirement/construction is fail-stop,
   with charges preserved, never restoration of the old live generation.
3. **Separate data from handles.** Clear old `_candidates`/`_staged` lookup scopes;
   retain immutable custody and actual warrants/receipt caches with original
   issuer lifetimes. Do not clear cumulative `_staging_counts`, input/store-call
   charges, admission reservations or import state. Old tokens then refuse even
   when a new provider reuses an old label. Local packet admission remains valid.
4. **Bind SemanticReader to its generation.** Its current `_active` checks only
   client/grant and definition mode. Capture exact search/acquisition identity
   (or a client-owned immutable generation token) and reject on replacement
   before every helper action. Closing a stale helper must remain possible and
   must not close the client. No whole helper registry is needed for this check.
5. **Bound reporting before retaining it.** SearchSession.report contains
   coverage, verified/advisory records and offer lists; storing eight full
   reports is not the proposed compact ledger. Store query identity, allocated
   vector, scalar counters and terminal outcome. Count snapshot attempt slots
   (`snapshot_slots`), not only distinct known IDs. Keep request/byte prepayment
   distinct from actual search and acquisition traffic; do not sum the same
   cumulative B report once per generation. Initialize optional state before
   superclass construction can call `report`, and keep legacy reports compatible.
6. **Do not confuse search retirement with import renewal.** `_session`, ready
   context, selection binding and preparation ownership remain unchanged. The
   selected capability is acquire A, acquire B, then one combined import. An
   already sealed context cannot silently absorb B or change definition policy.

## Smallest decisive later evidence

After source review, one finite native-free control set can exercise two
different queries, prospective exhaustion/failure charges, pending retirement,
stale search/contact/candidate/stage/helper refusal and terminal closure. Preserve
an actual issued warrant across rotation using existing retained evidence and
unchanged owners only if root selects that additional integration boundary.
Do not fabricate handles or treat structural fixtures as checked mathematics.
No new proof production or broad regression campaign is needed by this design.

The mechanism adds within-budget adaptive discovery while retaining costly
already-established authority. It does not establish faster mathematical growth,
globally complete discovery, new foundation semantics or final-v5 completion.
The fresh-operation workaround remains correct when independent lifetimes are
desired; the reason for this successor is optional same-lifetime composition.
