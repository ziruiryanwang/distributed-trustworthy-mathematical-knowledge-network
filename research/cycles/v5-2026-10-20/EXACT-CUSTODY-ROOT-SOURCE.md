# Exact-demand custody: root integration source

2026-10-20. Fresh, not yet executed or installed. The source baseline is the
113-entry projection map; the implementation selection is
`EXACT-CUSTODY-IMPLEMENTATION.md`. Other authors own the helper, routing and tests.

## Implemented integration

- The transport now factors one body-attempt engine from the original checked
  HTTP, validation, structural and outer accounting path. `_binding` and
  `_unchanged` remain usable by the declaration helper. The original supplier
  binder retains exact contact-map membership and adds only the missing exact
  adaptive-located class. `_demand_binding` accepts only the helper's exact
  issued `_BodyAttempt`; it snapshots the original endpoint maps, not a new map.
- A token's local expiry is checked after the original budget's `begin`, before
  dialing. The pre-binding check excludes only local hint expiry/egress; owner
  identity and original grant liveness remain required. Reservation callbacks
  are inside the engine's settlement `finally`. No unissued ticket is settled.
- The facade adds optional reservation and two private serialized actions used
  by the reader. The helper and imported transport functions must come from the
  original owners' selected source pins. Body commit/readback/input charging
  remain outside recoverable transport handling; every attempted token is spent
  in `finally`, even on refusal or custody failure.
- The reader exposes the two contract APIs, retaining its current demand,
  candidate, selected packet, original grant and query. Each uses one facade
  action without nesting a `describe_candidate` action. Fulfillment/preview/
  terminal state prunes or invalidates capabilities without resetting counters.
- The fresh distribution-builder successor requires the new helper and accepts
  explicit advertised-service V3 parameter injection. This selects no build.

No mathematical acceptance, global availability or useful-growth claim follows.
Actual correctness remains subject to independent source review and the single
selected changed-boundary suite; no runtime is selected by this note.
