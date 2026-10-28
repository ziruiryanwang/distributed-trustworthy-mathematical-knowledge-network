# Own the TCP connection before stream handoff

2026-10-28 root implementation selection after actual public refresh failure.
Adopt ordinary_registration_refresh/TRANSPORT-FAILURE-DECISION.md
`ef83f1b8018f135d2e029938426ef1cf70ecfd9602d66b17a701931dc11589dc`.
The first refresh/read/natural close succeeded; the overall public01 workflow
failed on an unobserved-connect-closure error. Preserve all original sources and
evidence. The saved error does not identify reset versus timeout and is not proof
of a resource leak.

Workflow: an unavailable selected feed must not prevent later selected feeds
from being tried when the client can actually establish safe cleanup within the
original budget. Implement only the pre-transfer owned TCP socket boundary in
a fresh fair_exchange.py. Retain one socket, numeric endpoints, existing exact
TLS identities, original absolute deadline and unchanged wire/return schemas.
Settle known pre-transfer refusal/reset/timeout only after successful own-socket
close and invalid-descriptor observation. External cancellation, unknown errors,
close failures and uncertain no-writer post-transfer failures remain terminal.
Reuse the existing refusal vocabulary; no generic OSError catch, new retry or
private event-loop cache manipulation.

This replaces an implicit socket allocation with an explicit one, not an extra
connection. Constant per-request work and bounded attempted slots do not depend
on the mathematical corpus size. It does not solve all TLS/transport failure
recovery, prove OS cancellation or promise that queued packets disappeared.

Ownership:

- operable_scale_decision: fair_exchange.py and a concise implementation contract.
- growth_design_audit: independent ownership/cancellation source challenge and
  minimal new-seam controls; no duplicate HTTP/parser/refresh groups.
- query_scaling: fresh public-workflow successor only after interface settles,
  retaining the A-to-B identical-policy discriminator and correcting only the
  overly specific stopped-port outcome. Preserve exceptional phase/cause data.
- Root: exact source-map/build/package successor, review, bounded selections,
  adoption and Git. Existing package/installation/native and owner state remain
  untouched. No runtime or native build is selected yet.

A source-reviewed synthetic ownership control and one finite public composition
are sufficient if they resolve the identified uncertainty. Do not repeat Lean
or mathematical growth demonstrations for this transport-only change.
