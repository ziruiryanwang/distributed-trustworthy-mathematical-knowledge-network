# Installed connected service: request-contract correction

2026-10-20. Owner: core_search. Source-only review and root-selected fresh
adapter; no invocation, installation change, proof or mathematical acceptance.
All paths are relative to the canonical project root unless stated otherwise.

## Decision

The failed actual01 request supplied `output_limits.bytes = 32 MiB` while
`client.launch.read_plan` requires at least `SOURCE_TOTAL = 64 MiB`.
This is the sole deterministic request-contract mismatch found in the
cross-layer source pass below. It failed before provider boot or advertisement;
the valid reader startup does not establish two live roles.

Root selected a fresh `installed_service_check02.py`, preserving the original
adapter and every failed byte. The fresh request uses exactly the existing
64 MiB minimum, not a changed product limit. No CPU, wall, memory, process,
network, query or service allowance is increased. This disk/output ceiling
does not allocate 64 MiB of RAM.

Source review is not evidence that service timing, network progress or final
output size will succeed. A separately selected actual boundary remains needed.

## Closed request-contract pass

The review traced the adapter through installed `distribution._launch`,
`client.launch.read_plan`, `client.boot`, advertised and HTTP serving,
location Python controllers, Node entry/configuration, the retained datastore
defaults, workflow/search admission and query-page validation.

| Boundary | Selected values and checked constraints | Conclusion |
|---|---|---|
| Installed public entry | Installed Python with `-I -S -B`; fixed release; command `serve-advertised`; `owner=null`, `runtime_mode=null`; caller omits reserved location installation root | Compatible; wrapper injects the installed `base` root |
| Paths and schemas | Absolute canonical ordinary paths; workspace is disjoint from install, run and request-control directories; fresh name matches `[a-z0-9][a-z0-9-]{0,63}`; exact fields at each layer | No extra field/path mismatch found |
| Source plan | Saved actual01 generated plan: 107 files (106 SDK plus owner), 1,202,336 bytes total, largest 50,535 bytes; limits 512 files, 64 MiB total, 2 MiB/file; required launch/boot/workspace and 21 portable files present | Within existing bounds; exact source-map checks stay enabled |
| Parameter and IPC sizes | Saved plan parameters serialize to 3,487 UTF-8 bytes; saved reader config 965 bytes and source map 1,817 bytes; parameter ceiling 65,536 bytes; IPC/config/map ceilings 16,384 bytes | Within bounds; provider adds one endpoint/bootstrap and uses the same 14 MJS keys |
| Output census | 4,096 entries, allowed 1,024..32,768; original 32 MiB versus allowed 64 MiB..2 GiB | Only deterministic mismatch; fresh02 supplies 64 MiB |
| Public child Job | 100 CPU seconds; wall 350..390 seconds as available; 384 MiB; 3 processes; 1 MiB each log | Valid launcher/operator ranges; boot Python + provider Node need 2 child processes |
| Enclosing operation | Unchanged 570-second inner cut, 600-second outer wall, 120 CPU, 512 MiB, 6 processes; original clocks transferred through public launch | Source-supported envelope, not a runtime success prediction; expected simultaneous adapter + reader Node + public wrapper + boot Python + provider Node is 5 |
| HTTP service | 2 connections, 4 requests, 1 MiB reply, 5,000 ms operation, 120-second lifetime; numeric loopback bind on reserved nonzero port; TLS null | Valid ranges; mandatory HTTP close reserve remains 10 seconds |
| Location config | Reader/provider roles; exactly one listen address each; provider bootstrap includes actual reader PeerID; no reader endpoints and exactly one provider endpoint | Compatible with Python, Node and owner egress schemas |
| Location limits | Service 560,000 ms reader / 150,000 ms provider; operation 10,000 ms; 256 events; 2 providers; 1 key; TTL 120,000 ms; reprovide 30,000 ms; maintenance 60,000 ms; 24 commands; 4 descriptors / 16,384 reply bytes | All ranges fit; `3 * reprovide <= TTL`; service duration may be reduced, never renewed |
| Health and shutdown | 10,000 ms health interval; cap `ceil(120/10)+2 = 14`; publish + health + stop at most 16 requests; IPC parent cap 60, Node frame cap 64; 41-second combined close reserve | No static count conflict; final health and stop remain mandatory |
| Transport and metadata | 32 outbound attempts, 32 inbound upgrades, 2 MiB receive/send; metadata `{}` is allowed | Retained defaults valid; see caveat below |
| Workflow | 25,000 ms, one route, 256 events, 2 peer slots, one descriptor/contact, 266,240 reply bytes | Descriptor 4,096 + search 262,144 exactly fits total; no allowance refund |
| Search and page | One provider/snapshot; two requests, one page; four examined/candidates; 262,144 bytes; offer/page each <=65,536 bytes; offer expanded <=131,072; page timeout 1,000 ms/node reads 4,096 | All lower/upper and shared-budget constraints fit; search adopts descriptor then authenticated offer/page |
| Workspace reopening | Same already-created atomic configuration; fresh service state; initial setup succeeded before actual01 launch refusal | No new config mismatch found; no warrant/native/proof owner is called |
| Final evidence | Public exit and boot zero; no active child processes/errors; exactly two HTTP requests; at least three health checks; one dispatched route; STOPPED and all closures; exact post-source pins | Assertions are supported by output schemas, not assumed achieved |

The old runtime datastore defaults selected by metadata `{}` are 16,384
entries, 16 MiB logical bytes, 32,768 bytes/value, 32 providers/key and 16,384
SQLite pages (64 MiB disk ceiling). `intent.mjs` supplies the expected provider
prefix. These are limits, not preallocations. Their maxima plus the source
snapshot could exceed the fresh 64 MiB aggregate output cap; that cap still
rejects excess actual output. This tiny one-key/two-peer operation neither
requests nor needs filling all maxima. No default or cap was loosened to make
the source pass. Timing, port reuse races, DHT progress, OS scheduling and actual
resource use remain possible finite operational failures, not discovered schema
mismatches. A static compatibility pass cannot eliminate them.

## Exact fresh source delta

Original `software/v5/distribution_connected/installed_service_check.py` remains
21,516 bytes, SHA-256
`93ceb7e13afc6cef0fd9f95775051498b14bd8513bfd6ea629dbbef706cc4a76`.

Fresh `software/v5/distribution_connected/installed_service_check02.py` is
21,891 bytes, SHA-256
`8467a2c9d0dfc67fa8b14a3494ee4d62c87f4027a552d3c9034474d6a2994cc2`.
It is a fresh copy with exactly the following textual changes (original frozen
bytes are untouched; fresh file uses LF):

```diff
-NAME = "installed-advertised-01"
+NAME = "installed-advertised-02"

-        proof_calls=0, native_calls=0, real_node_roles=2, cleanup_errors=[],
+        proof_calls=0, native_calls=0, expected_node_roles=2, ready_node_roles=[], cleanup_errors=[],

         need(ready["status"] == "RUNNING" and ready["role"] == "reader", "CHECK_READER_READY")
+        report["ready_node_roles"].append("reader")

-            output_limits=dict(entries=4096, bytes=32*MIB))
+            output_limits=dict(entries=4096, bytes=64*MIB))

              "CHECK_LIVE_READY_QUERY_WINDOW")
+        provider_ready = service_ready["location_ready"]
+        need(provider_ready["status"] == "RUNNING" and provider_ready["role"] == "index-provider"
+             and provider_ready["namespace"] == namespace, "CHECK_PROVIDER_READY")
+        report["ready_node_roles"].append("index-provider")
```

`expected_node_roles` is planning metadata. `ready_node_roles` records only
roles whose readiness checks were reached and passed. It is not a complete
spawn census: a role could have spawned and failed before readiness. The
provider record is observed through the actual installed service's readiness
file, which is written only after provider `_live_status`, publication and
health checks. No provider is counted merely because the request was sent.

## Principal inspected source bindings

| Source | SHA-256 |
|---|---|
| `distribution_connected/distribution.py` | `8e34df2a98fc3bf017f3d57ea2f92211bbcf156ee801479cbfaf9261f76763a6` |
| `client/launch.py` | `523a3031da86457037af3c41f87425cd406e5fe3fcf6a2edb2d87eff9b59ef78` |
| `client/boot.py` | `76cdcd42379d61c5fe37dc86a23363687c084c56887302dcdd922aa9b089ce2b` |
| `client/serve_workspace.py` | `89723f2e8a03abcaa709560f6d991ffc5d2bb349ef6cb662aadad7589a73936c` |
| `client/serve_advertised.py` | `80d6c0746eca23398cfe735af5d8de1076eb3725439414cce68de743c518a7ed` |
| `portable_runtime/location/controller_services.py` | `8591c49dba300a84d1e4b60f3ee1550be5eefd06b22867cf84d5b1080497e595` |
| `portable_runtime/location/node_entry_services.mjs` | `2eae8676469da5ef34fb88539d67774fc3dd115a6662cf24d169046e224fc346` |
| `portable_runtime/location/maintained_roles.mjs` | `9824559f55eca9b1e56786c14cbe090b74904d1786a915f124dc4101b0aa9683` |
| `discovery/search_session.py` | `e82c628eb75a584b33e637d4758cc9e789c3953ef4fb86b7d6e5111e3fd425cf` |
| `discovery/discovery_query.py` | `f9ce09ba74e7656a2f53d813489a43434258208198bcb4784c0e4eb682ac24e2` |
| Installed `base/overlay/quota_store.mjs` | `7c6cbeea0c685ec81f8d263cf84c6b8b9dd2c1f09e9f2f0f063196abc929eca4` |

The first ten are below `software/v5/`; the last is below the adopted
`product-local/v5-distribution-connected-01/Mathematical Commons v5`.
Core_release is asked to review only this fresh delta and the root's fresh
selector. Root alone selects execution. This checkpoint does not authorize it.
