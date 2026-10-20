# Advertised workspace service: focused controls

2026-10-20, core_growth. Source prepared only; no import, compilation, test,
Node process, listener, native checking or proof run was performed by this
assignment. Root owns any prospective bounded execution and adoption.

Selected source:
`software/v5/client/test_serve_advertised.py`, 22,679 bytes, SHA-256
`36107587eefd4284970a9a5ac41aa2e8672488e8b55c4714a002918af16384e2`.
Aligned by source inspection with service source `2fd6bff79076f3d49258ed17443387934fd9f702e65fb0aa8d715695539e8d7b`.

## Scope and economy

Reuse only the existing `test_serve_workspace` fixture and assertions: fresh
real SQLite stores contain an explicitly synthetic structural descriptor, with
no mathematical warrant. The predecessor's eleven tests are not selected or
rerun. The new suite explicitly selects nine new methods. HTTP, location
adoption and the location child are inert lifecycle objects. Process and socket
creation APIs are forbidden during the test suite.

The nine methods cover:

1. Endpoint and namespace derived from the opened store/listener; distinct
   explicit retained location runtime; exact source-pin key sets; original
   finite lifetime; reserved final health/stop deadlines; ordered clean closure.
2. Invalid/missing runtime, mutable-runtime overlap, missing role pin, empty
   routes, insufficient command reservation, caller-injected endpoint and
   ephemeral HTTP port all refuse before opening the workspace or HTTP.
3. Location start failure after HTTP startup closes every owned component and
   never publishes READY.
4. Incomplete second dispatch or mismatched route key refuses READY. Successful
   dispatch remains explicitly unacknowledged, not confirmed remote placement.
5. Location process death after READY is terminal before the active cutoff;
   there is no silent successful HTTP-only fallback.
6. Post-READY locator STOPPED while its process lives, a STOPPED result only in
   the final reserved health interval, and an HTTP listener becoming non-serving
   all fail and release the workspace.
7. Cancellation after READY propagates only after location, HTTP and workspace
   cleanup has been attempted in order.
8. Location stop or close failure still attempts HTTP/workspace cleanup and
   cannot produce PASS.
9. HTTP stop failure after location closure still releases the workspace and
   cannot produce PASS.

Each method reopens its retained synthetic workspace to check the data survived.
Terminal service reports remain in distinct operation directories; the suite's
summary is `controls-result.json`, avoiding Windows case-insensitive collisions
with the supervisor's `result.json`.

## Required execution context

The suite requires isolated/no-site/no-bytecode Python at the canonical project
cwd, with an already existing canonical output directory below `experiments`.
Pass the supervisor's created output root; do not pass a nonexistent `controls`
child unless the adapter separately creates that exact directory. The suite
creates only fresh per-method subdirectories and uses exclusive summary writes.

The selected source map must include the inherited fixture, its imports, the
service and all fourteen retained portable location JavaScript source files.
The fixture derives pins from those selected source bytes, not caller claims.
For prevalidation it reads the unchanged retained release manifest and checks
the Node executable exists at the explicit full installation recorded in
`LOCATED-SERVICE-ROLE-MAP.md`. It does not hash/execute the Node binary or perform
the real runtime adoption census because adoption is explicitly inert here.

## What this cannot establish

This is a changed ownership/lifecycle contract, not an integration test of the
DHT, Noise, real provider dispatch, timers, native runtime integrity, sockets,
public reachability, remote retention or mathematical acceptance. Existing
component evidence is neither repeated nor promoted. A real location-to-HTTP
composition, if root judges it decision-changing, needs a separate finite
selection. Full v5 certification, useful growth and public release remain open.
