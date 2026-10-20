# Serve and advertise: independent seam review

2026-10-20, `core_release`. Canonical guard passed. Source/theory inspection
only; no runtime, imports, package changes, experiments, RAM work or Git writes.
This reviews the proposed decision, not an implementation or release.

**Disposition:** a small ordinary-owner composition is coherent. Reuse the
existing HTTP provider and portable `ServiceLocationProcess`; do not build a new
location service. There is no mathematical-authority reason to block this seam.
There are six decision-changing requirements:

1. **Derive the advertised service from the service actually opened.** Open the
   existing workspace with its unchanged exclusive lock, start HTTP, then build
   the provider namespace and endpoint from that workspace and actual returned
   endpoint. Select the `index-provider` role and bounded explicit feature/stripe
   advertisements. A route is an advisory willingness-to-serve claim, not proof
   that the index is complete, nonempty or mathematically valid. No proof owner,
   verifier, received descriptor or network JSON may mint authority here.
2. **Couple the two lifetimes.** Do not call the old `serve()` as an opaque task:
   it publishes its own READY and then sleeps. The composition must own startup,
   one common serving deadline and teardown. It must notice early child exit or
   failed location state rather than continuing to report combined readiness.
   Stop location renewal/descriptor service before HTTP and workspace teardown.
   Reserve the existing location controller's six-second cleanup allowance,
   HTTP drain and final reporting/source verification inside the original outer
   deadline. Node `service_ms`, per-command relative time and the parent deadline
   are different clocks; neither receives a renewed operation allowance.
3. **Readiness claims stay exact.** Node READY means listening and bootstrap
   dial attempted, not a usable routing table. Publish can return INCOMPLETE or
   `HINT_DISPATCHED_UNACKNOWLEDGED`; neither is acknowledged remote placement.
   A failed/incomplete publication may leave a live local intent and later
   background renewal. Expose that outcome; do not label it global registration
   or silently retry under a fresh grant. Any final combined PASS must separately
   identify HTTP, location and advertisement outcomes.
4. **Retain the selected egress and deployment boundary.** The portable policy
   accepts direct IPv4 TCP only, with explicit public ports or exact loopback
   test destinations; public HTTP endpoints require TLS. Ordinary HTTP's IPv6
   support does not make location IPv6-capable. Reject incompatible settings;
   do not invent public/NAT addresses, open firewall rules or widen destinations.
   Local listener success does not establish external reachability. An
   authenticated descriptor binds the announcing peer, not mathematical truth.
5. **Cleanup is local, not global withdrawal.** Stop/withdraw can end local
   renewal and descriptor service. Receiving DHT nodes control their retained
   records; sender TTL is not a proof of remote deletion at a given time. Stale
   hints are expected and must be labelled. Cancellation, failed close, forced
   termination, inconsistent source pins and uncertain process reaping cannot
   become clean combined success. Close the HTTP provider and workspace even if
   location cleanup fails, while retaining that failure in the terminal report.
6. **Preserve the actual launch/runtime boundary.** Use the exact portable
   controller, role-source pins and adopted Node/overlay runtime under the
   existing parent Job. Fresh state/evidence must be disjoint and below the
   selected run workspace, not library or installation paths. The current
   complete distribution's base projection omits Node/overlay; source composition
   alone is therefore not a distributable serving feature. Packaging requires
   explicit reuse of the already adopted artifacts, not dependency resolution or
   a new runtime. The current exclusive workspace lock also means this remains
   a serving stage, not concurrent authoring into the same workspace.

The available-descriptor helper is a reader-side narrow unavailable-dial
transition. It grants no publisher readiness or authority and need not change
for this serving composition. No central semantic blocker was found; the
meaningful local risks are coupled lifecycle, honest readiness and packaging.
Avoid expanding this increment into DHT replacement, autonomous route selection,
mutable multi-owner workspaces, NAT traversal or mathematical admission.

Inspected: `client/serve_workspace.py`, `client/boot.py`, portable
`location/controller.py`, `controller_services.py`, `available_descriptor.py`,
`node_entry_services.mjs`, `maintained_roles.mjs`, `protocol.mjs`, and the
`distribution_complete/distribution.py` base-projection boundary.
