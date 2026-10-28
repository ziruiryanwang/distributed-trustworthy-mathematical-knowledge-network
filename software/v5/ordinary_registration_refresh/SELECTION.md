# Policy-scoped contact refresh and finite serving

2026-10-28 root source selection. Adopt the minimal existing-contact composition
in ordinary_directory_kit/NEXT-CORE-DECISION.md
`4323b97bbda77b39e3438243f3b4233d50df374a92694339406a1fbec09d4af4`.
The earlier proposed new feed/revision protocol is rejected as unnecessary.

Workflow: independent providers operate existing advisory contact feeds. A
registrar preapproves origins, exact route scope, endpoint policy and quotas.
One fresh `directory-refresh-serve` invocation retrieves current replies and
serves the accepted union, without per-advertisement manual edits. No owner,
theorem, proof, native build, new wire format, persistent registry or cached
advertisement authority. Failed/empty/truncated sources remain distinct.

Use current deployed sources selected by ordinary_name_directory/source-map.json;
do not build on the deferred pattern integration. All changes are fresh files
under this directory. Keep the exact search namespace, acceptance and old static
directory APIs unchanged. Source-only first; no runtime selected by this note.

Disjoint owners:

- operable_scale_decision: peer_api.py successor and REFRESH-CONTRACT.md with
  the exact finite configuration/report/API; reuse current contact exchange,
  parser, policy and allowance mechanisms.
- query_scaling: http_provider.py successor and CUTOFF-CONTRACT.md. Optional
  contact-only monotonic cutoff; default None preserves all existing behavior.
  Guard direct dispatch and each HTTP response enqueue/write chunk, combining
  existing operation checks. Keep conservative accounting and bounded cleanup.
- Root: peer.py/run.py public routing, profile/source-map/package integration,
  later bounded selections, adoption and Git.
- growth_design_audit: independent source review and smallest meaningful
  changed-seam control source after interfaces settle; no broad audit campaign.

Provider/API agreement: `Provider(..., contact_deadline=None)`. Internal
`directory_serve(..., contact_deadline=None, minimum_service_ms=0)` receives only a trusted caller's
computed cutoff and narrows the ordinary lease. It checks the requested minimum
remaining interval after provider startup, immediately before READY; slow startup
refuses and cleans up without claiming readiness. No mutable allowance wrapper.
Public static config cannot
renew that cutoff. Direct contact dispatch and HTTP writes check it independently.
The guarantee is a monotonic deadline check immediately before each new enqueue;
it is not a hard real-time OS scheduling guarantee or final-byte-arrival promise.
Already queued replies retain their ordinary client horizon and are not revoked.

Policy validates summed per-route slot quotas <=16 before I/O, no retry or
silent quota expansion, aggregate refresh request/byte/time bounds, and minimum
remaining service time. Registrar never dials learned destinations. Expired or
missing slots are omitted with disclosure; empty union finishes without listening.
Same-invocation fresh nonce replies remove cross-boot clock/cached-lease machinery.
Fresh stale claims from an approved live provider remain possible and advisory.

The expected benefit is maintained reachability as independent sources change,
not guaranteed relevance, liveness, global coverage or mathematical growth rate.
Only selected bounded contact data and service work enter this operation's cost;
no global proof corpus is required. Resolve source correctness before one focused
control selection and a finite loopback public-workflow check.
