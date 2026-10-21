# Optional pair-anchor planning

Source successor only; installation and runtime adoption are separate decisions.

The existing pair-profile index already stores up to eight selected two-feature
intersections. Its legacy query compiler exposes only the first applicable pair.
This successor can expose additional already-stored pairs to the existing
authenticated least-count-per-partition planner.

`adapter.compile_query(specs)` is unchanged. Use it for existing rendezvous route
plans and legacy callers. `adapter.plan_query(specs)` returns a bounded local
plan whose `features` retain every `legacy_features` key and add eligible pair
keys in canonical profile order, up to the existing eight-key limit. The
`status` is `NO_EXTRA_PAIR`, `ALL_ELIGIBLE`, or `WIRE_CAP`; the plan also lists
eligible, added and omitted pair keys. It is not a server-statistics response,
coverage certificate or mathematical acceptance.

Opt in at an ordinary adaptive operation boundary:

```python
next_query(client, contacts, specs, search_limits, plan_pairs=True)
await next_located_query(
    client, specs, location_limits, search_limits,
    routes=existing_legacy_routes, plan_pairs=True)
```

`plan_pairs` must be a genuine Boolean and defaults to `False`. One-shot `bind`
and `find` are unchanged. Opted-in results and generation rows contain a copied
`query_plan`, including a located no-contacts result. No extra session,
statistics request, generation, owner, child or allowance is created. The
original operation retains all acquisition, proof and cleanup responsibilities.

Keeping all old keys means every formerly valid route remains a valid unchanged
subset of the richer search query. The default compiler, namespace, route keys,
advertisements, extraction, store and wire format do not change. Do not derive
replacement route advertisements from the optional richer query implicitly.

Under correct pair extraction, the mathematical search predicate is unchanged.
The minimum included posting count cannot increase in any partition. If all
eligible pairs fit, it sees the best included atomic/pair anchor. `WIRE_CAP`
means an omitted pair may be more selective; there is no optimality promise.

More feature summaries take space and verification work. They may exceed an
unchanged reply/verification cap even when the old query succeeds. No automatic
fallback, retry, refund or budget renewal follows. Scan-count dominance is not
total-cost or availability dominance. All existing conditional committed-index
coverage limits remain; no global recall, growth or mathematical-trust claim is
added.

The source/theory argument and selection scope are recorded in
`research/cycles/v5-2026-10-20/POST-CUSTODY-DISCOVERY-DECISION.md`.
