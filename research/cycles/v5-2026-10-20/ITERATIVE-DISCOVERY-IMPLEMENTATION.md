# Bounded iterative discovery: client implementation checkpoint

2026-10-20. Implemented selected source successors only; no runtime, imports,
tests, build, installation, Git mutation or mathematical acceptance performed.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Selection: `ITERATIVE-DISCOVERY-SELECTION.md`; source basis is the 110-source
`distribution-discovery-01-input.json`, SHA-256 `e0e22f41...b20b`.

## Exact owned sources

All paths below are relative to `software/v5/iterative_queries/`.

| Path | Current SHA-256 | Change relative to selected predecessor |
|---|---|---|
| `client/direct_contacts.py` | `e243a094b9fdce2adef221514923bf6753d04b8cc3ed8ae60e392c0ebd804545` | 230 appended lines; original one-shot implementation unchanged. |
| `client/workspace_validated.py` | `901ffd191131a8eb293c4f11ca8a890a5edd800d3d90156dc298ff13ac15a4be` | 41 inserted lines; optional envelope lifecycle/reporting. |

Growth separately owns `evidence_network/transport.py` retirement and
`client/semantic_reader.py` generation binding. These four successors replace
logical paths only after root selects integration. No predecessor was edited.

## Public API

`reserve_queries(client, envelope, policy)` is a serialized client action.
`envelope` has every `SearchSession.LIMITS` field, plus `generations` in 1..8:
providers, snapshots, requests, pages, examined, candidates, bytes, wall_ms,
inflight, generations. Each normal field keeps its existing SearchSession range.
The seven consumptive fields are totals; inflight is a maximum concurrency cap;
wall_ms fixes ONE absolute deadline capped by the original grant deadline.

Reservation requires a fresh query slot, no channel/handoff/search/acquisition,
and the unchanged budget preallocation phase. It adopts the already pinned
direct-contact source, charges the envelope input, prepays requests/bytes once
with label `direct-query-envelope`, and permanently sets `_query_used=True`.
Thus legacy `bind` and located `find` cannot coexist with the optional envelope.
The fixed policy object and contents, namespace, grant, deadline and budget
identity/limits are rechecked. No owner is created, closed or renewed here.

`next_query(client, contacts, specs, search_limits, contact_lifetime_ms=60000)`
uses the fixed policy. It validates contacts/query/limits and quiescence, charges
query input, debits the FULL next-generation allocation, then retires the prior
generation. Every consumptive dimension must fit the remaining envelope; per
generation wall and inflight caps may not exceed the envelope caps. Actual
session/contact deadlines are capped by both fixed envelope and grant deadlines.
Construction/retirement failure retains allocation and inherits fail-stop; no
retry, refund, old-state restoration or second external prepayment exists.

## Retirement and failure invariants

Replacement requires no budget ticket, search pending/reserved work, structural
inflight work or structural reserved bytes. The old search becomes `RETIRED`;
the explicit `retire_generation()` tombstones its acquisition without closing
the shared budget. Candidate/staging maps are cleared, but their cumulative
charges, authentic warrants, receipt/packet caches, custodied bytes, original
owners and import/session/view state remain unchanged. Old direct contacts still
check exact current identities; the separate reader successor enforces the same.

On failure, even a partially constructed `client._search` is tombstoned before
original owner/budget cleanup. Allocated/active rows receive terminal status
BEFORE diagnostic capture, so a diagnostic exception cannot hide that failure.
Close preserves a prior FAILED outcome. Root/growth identified a cleanup hazard
in the first unused source: a diagnostic exception could skip original close.
The current successor catches it, records uncertainty/poisoning, and always
executes inherited cleanup. No failed experiment is being rewritten.

## Accounting and scope

Optional `client.report()['iterative_queries']` contains limits, aggregate
allocated vector, at most eight generation rows and remaining fixed wall time.
Each row stores a query digest, allocation, status and fixed-width scalar search,
HTTP and structural-transport counters. It does not copy coverage, candidates,
snapshots, offers or the cumulative acquisition ledger into every generation.
Snapshot cost uses charged attempt slots. Envelope prepayment is not summed
again as actual search traffic. Legacy reports have no added key unless opted in.

The change supports successive different searches and acquisitions before one
combined import. Existing sealed contexts cannot be enlarged by this API.
No measured speedup, useful growth, network completeness or final v5 is claimed.
Independent controls/review and any single finite launch remain root decisions.
