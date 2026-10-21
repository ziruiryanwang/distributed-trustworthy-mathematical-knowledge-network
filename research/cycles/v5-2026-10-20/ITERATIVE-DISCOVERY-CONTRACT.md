# Finite sequential queries without renewing mathematical authority

Decision: opt-in sequential DIRECT-CONTACT search removes the `_query_used`
barrier for adaptive queries while keeping one operation's actual warrants.
No general planner, DHT restart, new proof protocol or mutable authoring context is needed. Source/theory only; no run selected.

## Why resetting the boolean is insufficient

Existing bind prepays the entire SearchSession requests/bytes into AcquisitionBudget.
Its `charge_external` is legal only before network sequence becomes nonzero.
After resolve/acquire, another ordinary bind cannot prepay a fresh search.
EvidenceAcquisition.close also closes the SHARED budget; closing it and resetting
the flag would renew a deliberately terminal lifetime. Neither guard is removed.
SearchSession separately bounds providers, snapshot attempts, pages, examined
rows and candidates; sharing only request/byte counters would reset those limits.

## One prospective envelope, adaptive queries within it

Before the first network/acquisition request, configure an immutable finite plan
with at most q generations, a fixed owner egress policy, current namespace, an
absolute search deadline Ds <= the original grant deadline D, and additive caps
S=(providers,snapshots,pages,examined,candidates,requests,reply_bytes).
Prepay S.requests/S.reply_bytes ONCE through unchanged charge_external. They
remain charged even if little search occurs. Leave explicit acquisition capacity
outside this reservation; export/body/packet attempts still charge the SAME budget.
The first implementation can cap q at 8; this is an engineering bound, not consensus.

For generation i, prospectively choose a vector a_i within remaining S and valid
SearchSession per-call ranges; commit A := A+a_i before dispatch, requiring A<=S
componentwise. No unused suballocation is refunded after retirement or failure.
Query/contact choices may adapt to earlier results; a_i fixes costs, not goals.
Each session still enforces its own limits and the original operation's CPU,
calls, input/output/storage and admission caps remain unchanged.

For every additive dimension d, used_i(d)<=a_i(d), hence sum used_i(d)<=S(d).
Providers count per-generation contact/provider slots, not globally independent
operators; repeated endpoints consume another allocation. Snapshots count charged
attempt slots, not only distinct returned IDs. Repeated candidates/scans remain
charged; replacing a query is not global deduplication or a resource refund.
For wire counters, outer use = prepaid S plus actual acquisition charges, not
prepaid S plus those same search requests charged twice. Diagnostics distinguish
reserved envelope, reserved generation allowances and observed/charged outcomes.

Ds is fixed at plan creation, not recomputed as now+wall on each query. A session
may have a shorter deadline min(Ds, now+its_wall_cap); later generations cannot
extend Ds, D, verifier lifetimes, retention promises or prior contacts. An empty
result is a settled outcome, not permission to create another budget or owner.

## Serialized generation state machine

PlanIdle -> QueryActive(i) -> QueryRetired(i) -> QueryActive(i+1), or Terminal.
At most one query generation exists live; no other client call is in flight.
Retirement requires zero pending search tickets/reservations, shared acquisition
pending=None, structural transport inflight=0 and completed/cancelled-and-awaited
requests. Unknown request outcomes settle conservatively BEFORE retirement.
Never detach a task that might later mutate the new generation or its accounting.

Add an explicit structural retirement operation, separate from terminal close:
snapshot a bounded final generation report; invalidate its search, acquisition,
contact binding, candidate/offer/supplier scope; then detach the client references.
Do not call budget-closing close and resurrect it. Retired contacts must reject
before any dial, and old tickets must not become valid through reused integers.
Bind opaque tokens to generation identity, or remove their whole old lookup scope.
Previously held bytes remain inert custody data; their provider provenance is
not new authority. Finish needed semantic acquisition before retiring its scope.

Preserve the SAME real I/A/mixed/preparation owners, grant, AcquisitionBudget,
issued warrants, exact verified receipt/packet caches and local custody. These
are not issued by a search generation. They remain subject to their own liveness,
policy and original limits; retirement grants no new use or verification allowance.
Unwarranted staged/candidate capabilities do not survive as live provider handles.
Local retained packets can still be admitted through the ordinary local route.

## Failure, cleanup and report invariant

Validate next-query shape/limits before replacing references, then charge before
its first possible I/O. Construction or retirement failure cannot leave both
generations live, reuse the old one, or erase charges. Preserve existing client
fail-stop behavior for unexpected errors; do not introduce silent retries.
Expected metadata-refusal outcomes retain their existing bounded semantics.
Terminal close closes the current structural scope and shared budget/owners once;
already retired scopes cannot close shared authority accidentally. Cleanup failure
is terminal/visible, never a successful rebind or a freshly reset operation.
Keep bounded per-generation counters plus aggregate reservations in the final
report, including failed attempts; reporting only the latest session loses cost.

## Scope and alternative

This supports search/acquire A, retire, search/acquire B, then one combined
import using both actual warrants. It does NOT permit changing a READY sealed
context or reusing a consumed authoring owner. Already-imported mathematics stays
usable under its immutable view; new discoveries can instead be collected for a
later operation. No claim of arbitrary multi-step research in one grant follows.

The existing simpler workaround is a fresh operation per query: correct, but it
loses owner-local warrants/cache and may require fresh evidence checking. Use it
when separate lifetimes are desired; do not describe it as missing functionality.
Sequential queries add within-budget composition, not faster mathematics.
First scope is direct contacts; later located-query reuse needs
its own finite channel/routing reservations, not a reset of existing find().
