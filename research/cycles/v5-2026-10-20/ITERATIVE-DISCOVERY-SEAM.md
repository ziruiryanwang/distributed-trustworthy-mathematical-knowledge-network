# Iterative formal discovery within one live operation

2026-10-20. Source/theory decision only; no implementation or runtime selected.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Basis: `experiments/v5-local-checks/distribution-discovery-01-input.json`,
SHA-256 `e0e22f412a6d276f172603ad11ff5217ea321b5a038921af2bd7f1b4b028e20b`.
This selected 110-source candidate map governs inspection, not historical paths.

## Finding: a real lifecycle restriction, not a missing agent strategy

An agent can search many providers/pages/candidates for ONE compiled formal query,
acquire several actual warrants, import them together and author a contribution.
`remote_reader.read` leaves its caller's live client open; `run/main` close it.
Exact dependency demands can resolve more declarations, but are not new searches.
No public route permits successive DIFFERENT queries under that same live grant.

The relevant selected physical source barriers are:

| Source under `software/v5/` | Exact restriction |
|---|---|
| `conjunction_index/client/workspace_atomic.py`, `find` | `_query_used` must be false; both located/direct routes share it. |
| `conjunction_index/client/direct_contacts.py`, `bind` | Query slot, channel, handoff, search and acquisition must all be fresh. |
| `transport/receipt_client.py`, `charge_external` | Prepayment requires `pending is None` and `sequence == 0`; label must be unique. |
| `evidence_network/transport.py`, `close` | Closes the SHARED acquisition budget, not merely query-local state. |
| `type_pattern/client/workspace_evidence.py`, `import_context` | At most one real mixed import session. |
| `conjunction_index/client/workspace_atomic.py`, `extend_context` | Only unresolved contexts extend; a ready context is sealed. |

Resetting `_query_used` is therefore not a safe solution. Recreating owners/grants
per query avoids these guards only by incurring startup and losing one-operation
accounting; it does not supply the requested unchanged-lifetime capability.

## Smallest consequential successor

Add an opt-in finite **direct-contact multi-query envelope**, reserved before ANY
acquisition. Leave located `find`, one-shot `bind`, wire protocol and acceptance
unchanged. Query selection remains local/adaptive; no global task list is added.
Proposed source scope: fresh successors of logical `client/direct_contacts.py`,
`client/workspace_validated.py`, `evidence_network/transport.py` and
`client/semantic_reader.py`; no receipt-budget, search, wire or issuer rewrite.

Suggested public shape (names provisional, not existing APIs):

1. `reserve_queries(client, envelope)` once, before the first query/acquisition.
2. `next_query(client, contacts, specs, policy, limits)` starts or replaces one
   generation; normal offer/page/resolve/acquire operations then remain usable.
3. Repeat within the original allowance, acquiring wanted mathematics BEFORE
   retiring its query. Finally select retained warrants in ONE `import_context`.

The envelope fixes a finite generation cap, absolute deadline and consumptive
totals for providers, snapshots, requests, pages, examined rows, candidates and
reply bytes. Its requests/bytes are prepaid ONCE with unchanged `charge_external`.
Each generation's complete prospective limits debit those totals before work;
no unused quota returns. Repeated providers/snapshots consume slots again.
`inflight` is a fixed concurrency cap, not renewable work. Per-query wall time
is capped by the envelope's absolute deadline AND the original grant deadline.
Original client call/input/controller limits and actual issuer budgets also stay.
No partial generation may enlarge these limits or switch the selected namespace.

## Retirement and retained mathematical authority

Use the existing serialized client action guard. Before retirement require no
shared-budget pending request, structural inflight request or search pending
ticket. A generation with uncertain cleanup cannot be replaced; fail-stop it.
Do not call `EvidenceAcquisition.close()` and then reopen its budget. A narrow
retirement operation must permanently retire its acquisition and SearchSession,
without closing the original shared budget, mixed import session or I/A owners.
Original terminal `client.close()` must still close all owners and the budget.

Clear old candidates, offers and query-scoped lookup state; do not reinterpret
old supplier labels under new endpoints. Invalidate old semantic-reader plans
and staged handles, or reject rotation until they are explicitly discarded.
Custodied immutable bytes survive; authentic admitted warrants and their caches
survive with their ORIGINAL issuer lifetimes. No copied receipt becomes authority.
Existing direct `_Binding.check` requires exact current search/acquisition
identity; old SearchSession must also reject calls through retained references.
Never leave a half-installed new binding or restore an uncertain old generation.

Retain a bounded cumulative ledger: generation number, query identity, charged
allocation, terminal search/transport counters and outcome. The current report
otherwise shows only the last search. Full reports must fit original metadata
limits; use cumulative counters plus bounded summaries, not unbounded history.

## Nonrenewal argument and limits

Let original aggregate acquisition limits be B, prepaid search envelope E, and
generation charges q_i. Require sum(q_i) <= E componentwise. Every search uses
at most q_i, including failed attempts; acquisition continues charging B after
the initial E charge. Thus search plus acquisition consumption remains <= B
for shared dimensions. Monotone envelope charges bound the other dimensions.
No generation changes original owners, grants, deadlines or their consumed work.
Induction over committed/failed generations proves nonrenewal, PROVIDED every
entry point enforces retirement, original identity and before-work charging.

This closes multiple searches/acquisitions before a combined import. It does NOT
close author -> discover more -> enlarge an already sealed context. That is a
separate import-lifetime decision, not authority to reset `_session`. Nor does
it prove useful growth, whole-network completeness or a measured speedup.
Smallest later control: two different queries, acquire retained first-generation
data, retire, acquire second, combine once; stale handles, failure charging,
pending rotation and exact exhaustion must refuse. No new proof campaign needed.
