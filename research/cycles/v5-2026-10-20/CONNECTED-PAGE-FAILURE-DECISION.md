# Installed page EOF: cumulative provider reservation, not host resources

2026-10-20. Owner: core_search; independent root source trace agrees.
Canonical root is `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Scope: saved-output/source inspection and root-authorized fresh adapter03 only.
No experiment, DB operation, installation rebuild, native/proof call or product
source change was performed by this investigation.

## Concrete cause

Actual02 is failed and preserved at
`experiments/v5-local-checks/installed-connected-service-02/evidence`.
Both roles reached validated readiness. The installed service completed its
finite lifecycle and clean closure, but its counters are two HTTP requests,
one failure and 1,973 reply-body bytes. Client's second request ended at HTTP
header EOF. Provider `status=PASS` describes its lifecycle; it does not claim
every received HTTP request succeeded.

The exact provider class is
`frontier_network.transport.CompositeProvider`, inheriting
`delta.transport.CompositeProvider._serve`, which inherits the ordinary
discovery dispatch from `transport.http_provider_receipts.Provider`.

The second request is `/v5/discovery/page`. Its provider-side reservation is
the fixed `ROUTES[route] = 1,048,576` bytes. That loop special-cases candidate,
offer and compact-summary reservations, **not the legacy page route**. Hence
the page's client `limits.bytes=65,536` does not reduce the provider reservation.
After the successful offer, the second request necessarily violates:

```text
reply_bytes + reserved_reply_bytes + reservation <= max_reply_bytes
1,973       + 0                    + 1,048,576   > 1,048,576
```

`DELTA_PROVIDER_REPLY_QUOTA` occurs before `dispatch`, and therefore before
`index.page`. `_serve` catches the exception, increments `failures` and closes
the connection without a free error body. `SearchClient._send` sees EOF and
abandons its ticket with the existing conservative charge.

The provider did not save its exception string, so the actual report alone does
not name that branch. The source inequality is nevertheless a deterministic
sufficient refusal for the exact successful-offer-then-page sequence, and is
consistent with every saved counter. It needs neither database probing nor a
new experiment to establish that the original request cannot succeed. This is
not a Node, RAM, mathematical verification or index-corruption finding.

The prior CONNECTED-REQUEST-CORRECTION review missed this cross-request
provider reservation. Its request range checks remain relevant, but its claim
that all constraints had been traversed was incomplete. This addendum preserves
that mistake rather than retroactively treating actual02 as unexpected load.

## Source path and remaining constraints

1. `ServiceLocatedWorkflow` issues one route and descriptor under its single
   25-second grant. `_LocatedSearchClient` rechecks the acquired endpoint's owner
   policy and hint expiry before every HTTP send.
2. `SearchSession.begin_offer` accepts 65,536 wire / 131,072 expanded bytes,
   charges one provider/snapshot/request slot and authenticates the offered
   snapshot. The selected nonempty partition comes from its verified summary.
3. `SearchSession.begin_page` constructs the exact request with that snapshot,
   feature conjunction, selected minimum-count anchor, partition and start=0.
   It validates page fields before I/O. Limits are examined=4, matches=4,
   bytes=65,536, timeout=1,000 ms and node_reads=4,096: all allowed.
4. Search aggregate allowance is 262,144 bytes, two requests, one page, four
   examined/candidates and one inflight. At most 65,536 offer bytes plus 65,536
   page bytes fits; descriptor 4,096 plus search capacity 262,144 exactly fits
   workflow 266,240. No attempted request receives a refund or new deadline.
5. Provider admission uses the different cumulative ceiling identified above.
   Once admitted, ordinary dispatch calls `index.page(request)` unchanged.
   It validates the same request, snapshot and anchor. The fixture has one
   record with both features, so its selected anchor interval contains that
   one record; vector height is zero. Four examined/matches are sufficient.
6. For two feature paths, even an uncompressed path upper bound of two node
   reads per each of 257 map positions, nine partition reads per feature and
   one vector leaf is 1,047 reads, below 4,096. The actual four-feature fixture
   is much smaller. This is a read-count argument, not a wall-time guarantee.
   The fixture's fixed short name, four feature hashes, fixed-size identifiers
   and one no-sibling record produce a page far below 65,536 bytes. Native code
   or proof ancestry is not involved.
7. Client coverage verifies the selected committed interval and record. It
   does not turn the synthetic theorem-shaped descriptor into mathematics.
   Time/hint expiry, integrity damage or I/O can still cause honest refusal;
   changing the service quota does not bypass those checks.
8. Post-result predicates use existing emitted schemas: public and boot zero,
   empty active Job/cleanup errors, exactly two HTTP requests, at least three
   health checks, one route dispatch, STOPPED and closed HTTP/location/workspace,
   exact installed source-map roots/manifest, source rehash and workspace reopen.
   Actual02 already reached ordinary service/public lifecycle closure; no
   repeated lifecycle qualification alone is claimed by the next boundary.

The earlier successful `test_serve_workspace` case was **offer plus module-group
acquisition**, not a successful page case. Its provider ceiling was 32 MiB,
which could accommodate the group's fixed 16 MiB reservation. It does not
contradict this one-MiB cumulative page refusal.

## Minimum selected correction

Root selected fresh `installed_service_check03.py`, not a provider refactor:

```text
max_reply_bytes = maximum offer reservation + legacy page reservation
                = 65,536 + 1,048,576
                = 1,114,112 bytes
```

This is a derived service transmission ceiling, not a memory increase.
The client still accepts at most 65,536 bytes per offer/page and the same total
query allowance. CPU, wall, memory, process, request, index, transport, health,
cleanup and output-census limits are unchanged. The product remains frozen.
Making legacy pages reserve their declared cap could be a later product
improvement, but is unnecessary to resolve this exact caller mismatch and
would require another selected product boundary.

The fresh adapter also retains completed route/descriptor/offer/page results as
soon as each returns. Those records identify the last completed steps. A final
guarded `workflow.report()` records actual charged state after an error, including
ticket abandonment; it is not merely the last successful step's budget snapshot.
Failure in final reporting adds a cleanup/evidence error without erasing the
primary cause or allowing PASS. No logging opens a renewed allowance or repeats
an operation.

Because final reporting follows the 120-second service lifetime while the query
budget is 25 seconds, its status may correctly be `DEADLINE_EXHAUSTED` even after
a timely successful page. The retained completed page establishes that earlier
outcome; the final report is a later charged-state snapshot, not a claim that
the earlier successful query missed its deadline.

## Exact fresh delta and bindings

Frozen02: 21,891 bytes, SHA-256
`8467a2c9d0dfc67fa8b14a3494ee4d62c87f4027a552d3c9034474d6a2994cc2`.

Fresh03: `software/v5/distribution_connected/installed_service_check03.py`,
22,398 bytes, SHA-256
`126f2081508b96d4c4e6258d95a6da23770eafb1d22da58e1581fd9868b7c5c5`.

```diff
-NAME = "installed-advertised-02"
+NAME = "installed-advertised-03"
-    reader = public = None
+    reader = public = workflow = None
-                service_limits=dict(max_connections=2, max_requests=4, max_reply_bytes=MIB,
+                service_limits=dict(max_connections=2, max_requests=4, max_reply_bytes=MIB+65536,
```

Immediately after the four corresponding successful awaited operations, add:

```python
report.update(route=route, workflow=workflow.report())
report.update(descriptor=acquired, workflow=workflow.report())
report.update(offer=offer, workflow=workflow.report())
report.update(page=page, workflow=workflow.report())
```

After reader cleanup and before final source checks, add:

```python
if workflow is not None:
    try:
        report["workflow"] = workflow.report()
    except BaseException as error:
        report["cleanup_errors"].append("workflow-final:"+str(error)[:300])
```

Those are the complete textual changes. Exact readiness fields from02 remain.
The original01 and02 adapters, saved inputs/results and installation are untouched.

Principal cause sources below `software/v5/`:

| Source | SHA-256 |
|---|---|
| `delta/transport.py` | `18c1abda1dca45cd8f5e86c09c4e1b8d5b13d4472931173a1db4a080c0c71d40` |
| `transport/http_provider.py` | `e1666a57bfc4d94e1a316c93eedee8b730edaeaf6441a5b22bc4345c32e7b3e4` |
| `transport/http_provider_receipts.py` | `4e00afb1edf7c5fb7c6b3bd3f538e2a1fdbd9aef9af32c23baeeb7717c89bc4b` |
| `transport/clients.py` | `640d1344824829865060712370444b5051720ce7b0a741e8efc0da8a066c6464` |

Core_release independently reviews the fresh source/selector. Root owns any
subsequent finite execution selection; this note makes no actual03 pass claim.
