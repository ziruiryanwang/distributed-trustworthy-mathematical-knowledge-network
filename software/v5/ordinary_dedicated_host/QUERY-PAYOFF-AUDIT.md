# Query and inspection payoff audit

2026-10-28. Source-only review of the selection in `source-map.json`. No product
edits, imports, tests, service calls, owner-state reads or runtime qualification
were performed. The independent saved-outcome audit owns the actual failed and
successful operations; this note does not re-audit or relabel them.

## Decision

Correct the incompatible examples and explain the two different byte budgets.
For general unknown-size inspection, recommend one separately selected provider
successor: narrow ordinary locator/evidence requests to the provider's remaining
unreserved byte allowance before dispatch. This needs no wire-schema change,
new size-discovery protocol, new index, automatic retry or larger grant. The
existing source remains frozen; this audit does not authorize implementation.

The reason extends beyond this fixture. A client maximum is an upper bound on
what it will accept, not a demand to receive that many bytes. Independent clients
normally cannot know a provider's current shared allowance, and a preview does
not supply the underlying evidence unit's exact byte length. Merely prescribing
the small cap that fits one known bundle would leave ordinary discovery and
inspection unnecessarily fragile.

Current provider-side search already uses indexed selected-feature postings and
does not scan or replay all local proofs. It is not proportional only to the
final matching set, and it has a corpus-sized worst case. No new search mechanism
or scale experiment is justified by the inspection-budget failure.

## Why the byte failure is possible

Let `G` be the provider lease's aggregate reply-body allowance, `C` its already
charged body bytes, `Q` live reservations and `r` this request's response cap.
Current admission requires:

`C + Q + r <= G`.

`ordinary_multi_source/http_provider.py:498-558` reserves before dispatch,
checks the actual encoded response against that reservation, charges actual
body bytes before sending, then releases the reservation in `finally`. Headers
are separately counted. An in-flight reservation can remain live after its
actual bytes are charged, so admission is deliberately conservative during
sending; this note does not propose changing that behavior.

For ordinary locator/evidence requests, `r` is the client's `max_bytes`. For
preview it is the exact identity-bound advertised `object_bytes`
(`ordinary_multi_source/ordinary_acquisition.py:52-71`). Therefore setting an
evidence request's cap equal to `G` makes it inadmissible after any previous
nonempty reply, even if the requested object is very small.

Inspection performs two sequential requests, locator then evidence. Its client
grant must cover the sum of the two configured maxima before starting
(`ordinary_multi_source/peer_api.py:1073-1137`). These client maxima are distinct
from the provider's shared lease allowance. Successful validated client fetches
settle actual bytes; failed begun attempts retain their full client reservation
(`ordinary_multi_source/ordinary_acquisition.py:343-357,392-442`). A provider
refusal does not silently renew either side's allowance.

There is an independent documentation usability mismatch: `HOSTING.md:114`
illustrates an 8 MiB provider lease, while `operator/examples.json:50-55`
illustrates a 1 MiB locator cap plus an 8 MiB evidence cap. Using those examples
together guarantees that the evidence reservation cannot follow a successful
locator on that lease. The examples file's separate ordinary `serve` example
uses 64 MiB; it is specifically the dedicated-host walkthrough combination that
is incompatible. Whether an actual operator deviated from its selected plan is
a separate outcome-review question, not an excuse for this generic mismatch.

Under existing code, a coordinated operator can select known tight client caps
or explicitly fund a provider grant that covers previous traffic plus each next
request cap and concurrent reservations. A sufficient serial plan is the sum
of the selected request maxima, including search/preview traffic. Do not promote
this fixture's small evidence cap into a universal default, and do not enlarge
an already issued lease implicitly. Preview's exact byte count only describes
the preview, not the evidence unit (`peer_api.py:1191-1236`).

## Small reusable provider correction

For locator/evidence only, the candidate successor would:

1. Validate the original request with the unchanged `request_limit` validator.
2. Calculate `R = G - C - Q`; refuse before dispatch if `R < 1`.
3. On the private parsed request, set `max_bytes = min(r, R)` and reserve that
   effective cap without an intervening suspension.
4. Dispatch through the unchanged bounded store, require the full encoded
   response to fit, charge actual bytes before sending, and release the effective
   reservation on all exit paths as today.

For a successful response of length `b`, this preserves `b <= min(r, R)` and
thus both the client's ceiling and the provider's available allocation. It
returns a complete exact object or refuses; it never truncates an object.
Preview's exact `object_bytes` must not be clamped. Discovery-page/offer budgets,
client ledgers, requests/time limits, concurrent exclusions, grant expiry and
mathematical acceptance are outside this change.

Whole-client-cap reservation is useful for output accounting, but not for
deciding whether an object is unavailable. Current quota refusal occurs before
the object lookup. If dispatch is admitted and the object is absent, lookup
throws and the reservation is released without a successful response body.
Evidence uses an indexed `length(raw)` lookup and checks that length before
materializing the BLOB (`ordinary_acquisition.py:232-258`); locator does the same
at `:271-285`. The smaller effective cap retains that protection for oversized
objects. A missing object still consumes a request and operation time, bounded
by the existing lease. Zero remaining bytes should still refuse before lookup.

This correction removes a false refusal caused solely by an unknown generous
client cap. It does not promise availability, remove conservative client charges
for failed attempts, improve concurrent fairness, or guarantee that a two-read
inspection will finish before the lease expires. Existing close-on-error
behavior remains an unavailable attempt, never global absence. If selected,
review only these changed accounting and complete-object boundaries; do not
restart native mathematics or a broad hosting campaign to establish them.

## What current search scales with

The selected map uses `ordinary_sparse_access/candidate_query.py` and
`discovery_store.py`, with the existing authenticated index and fair client.
`peer_api.py:131-132,493-544` defaults to `atomic-v1`, accepts at most 64 selected
providers, and uses finite serial fair rounds with a five-second attempt ceiling
inside the original session deadline. Its returned metadata is explicitly
incomplete, with no global completeness or verified scan-coverage claim.

For `k <= 8` conjunctive features, each of 256 fixed partitions chooses the
feature with the smallest committed posting count
(`discovery/discovery_query.py:70-75`). Empty partitions skip
(`ordinary_sparse_access/fair_search.py:209-233`). Let `a_p` be that minimum
posting count in partition `p`, `N` the local indexed object count, and `M` the
total posting entries. The atomic candidate driver is the selected posting
union of size `sum_p a_p`, not an unconditional traversal of `N` objects.

For each candidate, source performs an exact anchor-ordinal lookup and up to
`k-1` indexed secondary membership probes. Only conjunction survivors load a
full metadata record, and only full matches receive an authenticated membership
proof (`candidate_query.py:180-263`). The primary/unique posting indexes are
explicit at `discovery_store.py:92-97`. No evidence/proof bodies or transitive
ancestry are read by this search path.

Ignoring bounded page setup and record sizes, its candidate lookup work is
approximately `O(k * sum_p a_p * log M)` with B-tree storage. Membership-vector
work is logarithmic in the selected anchor count per returned hit
(`discovery/authenticated_index.py:169-172`); partition paths have fixed height
eight (`:205-208`) and the feature map uses fixed-width 256-bit keys. Summary
construction visits fixed partition descriptors for the selected features,
not all object records (`discovery_store.py:275-285`). Finite page budgets can
stop early, and repeated/failed attempts can repeat paid work. This is a source
cost argument, not an executed latency or whole-workflow speedup claim.

Consequences:

- Growth outside the selected postings does not add candidate rows to traverse,
  although larger B-trees, cache behavior and storage still affect lookup cost.
- A ubiquitous feature can have `sum_p a_p` near `N`. Even a tiny final
  conjunction can require many probes when every single feature is common.
  Here “relevant subset” means selected feature postings, not mathematical
  relevance or only the final intersection.
- Optional `sparse-v2` can drive from a configured pair intersection instead
  (`candidate_query.py:189-210`), with atomic fallback. This dedicated-host first
  version omits pair access (`CONTRACT.md:50-51`), so that acceleration cannot
  be claimed for this host. It also has maintenance/storage costs.
- Familiar-name query preparation is a separate local path. The adopted
  advisory projection avoids proof-snapshot reads but still validates selected
  lineage metadata and name mappings; `ordinary_advisory_query/ADOPTION.md:36-37`
  explicitly makes no sublinear cold-metadata claim. Provider indexed search
  does not erase that preparation cost.

Retain this architecture for current exact-feature discovery. Prefer selective
features already expressible by the existing query API. Revisit access paths
only when a useful workload demonstrates that broad postings or local metadata
preparation, rather than inspection funding, is the consequential bottleneck.
