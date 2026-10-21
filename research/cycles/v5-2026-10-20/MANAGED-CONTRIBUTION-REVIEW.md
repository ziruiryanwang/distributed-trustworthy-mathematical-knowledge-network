# Managed contribution: concrete source review

2026-10-21, support_screen. **PASS, SOURCE ONLY** for the exact successor below,
under `MANAGED-CONTRIBUTION-IMPLEMENTATION-SELECTION.md`. No product import,
runtime, service/secret issuance, helper-control result, build or installed
qualification is claimed. Root owns those separate gates.

| File under `software/v5/managed_contribution/` | Bytes | SHA-256 |
|---|---:|---|
| `client/managed_owner.py` | 26492 | `75c0e8a93c26594d459e716cf55dc6c982b1df079eeaed7834a1347fe4a40d09` |
| `client/private_credentials.py` | 12374 | `7116e2d9161cbb828203bc7eff1e7dd90c1cab7d6e860a6e16801ffb6ecb37f0` |
| `README.md` | 9129 | `4d2db874f6d413c74eb4edc1f9a926c41c4c08c8d28b175c2559fc990980f666` |

Read the complete owner/helper/README and their actual unchanged API callees.
The used predecessor owner still hashes to
`f213baff68319d3c84c9bc93597e4d3f9fe2990ead4f225a29c938626c17d1d4`.
This review records the implementation, not another general design proposal.

## Findings resolved and accepted

- **Exact new selection.** Public/worker/result schemas and worker-profile domain
  advance to V2. The owner requires127 SDK rows,128 owner-inclusive rows, the
  exact installed helper and identical owner copy. Frozen lifecycle/composer/
  supervisor pins remain. `serve`/`seal` add exactly nullable `intake_grant`;
  administrative parameter sets and existing operations are unchanged.
- **Authenticated parent ancestry.** The fixed parent puts its current plan
  hash into internal worker parameters. The child derives the parent plan from
  its current workspace, reads it with the ordinary pinned plan reader, checks
  original request/install/run, then reconstructs and compares the entire child
  plan. This equality carries source maps, owner entry, output caps, limits and
  relocation, not merely a caller-provided path label. The secret exclusions
  include original whole public workspace, original/current run/control/source
  roots, release and manager, with two-way overlap refusal. Parent preflight,
  child binding and publisher preflight occur before issuance. Dynamic paths do
  not alter persistent manager configuration.
- **Unchanged actual issuance authority.** The worker still joins the exact
  prospectively bound live session, allocates/opens through the existing manager
  and starts the actual service. Publisher requires exact `PlacementService`,
  live `ready()`, actual issuing runtime from its route report and selected
  operation/release/profile/session metadata. Only unchanged `issue_token`
  performs issuance. Egress/source selection, current runtime, generation state,
  live UTC horizons, original resource sublimits and grant-count charging remain
  the existing controller/ledger's decisions.
- **One original interval.** Worker computes its serving cutoff once before
  handoff, after original close reservation. It floors the exact float rational
  into integer `service_until_ns`; publication/readback/ready checks use this
  same cutoff. Helper also compares against an exact rational floor of the
  service deadline. That last detail was corrected during review from a
  floating-product floor, eliminating avoidable upward rounding. Reader uses a
  downward `nextafter` conversion and the minimum with its independently chosen
  deadline; it never starts another service duration. Existing async close and
  enclosing finite process supervision remain unchanged.
- **Bounded private output.** Exclusive create; canonical <=8192-byte envelope;
  checked write, flush/fsync/close; bounded ordinary single-link readback with
  stable observed file identity/extent and exact byte equality. No overwrite,
  retry, unlink, reissue or database refund exists. An uncertain committed grant
  remains charged even when writing/delivery/final reporting fails. Public
  failure observation separates stage and known grant ID from completion; new
  placement resource reservations still occur only on admitted manifests.
- **Closed disclosure boundary.** Secret values stay within publisher/parser or
  the unchanged client's private memory. Envelope schema, exact metadata and
  `SHA256(token.encode('ascii'))` are checked. Public ready/return values contain
  explicitly selected metadata and file pin, never the token/envelope. All
  public helper exception paths construct fixed-code `CredentialError` with
  suppressed underlying context; observation emits only code/stage/grant ID.
  Therefore existing owner error stringification does not copy raw parser/I/O
  payloads into ordinary reports. No helper logs or prints secret values.
- **Independent reader authority.** Reader validates an independently adopted
  complete expected metadata object, exact pin, contact equality, canonical
  token binding and live original cutoff before returning the existing
  `PlacementClient` plus whitelisted metadata. Independent egress, contact and
  finite request/byte/operation limits still enter that client. The file does
  not choose new contact rights, caps or executable code.

No blocking source defect remains in these exact bytes. The author's separately
authorized one-pass AST checks, if recorded, are syntax checks only; this
reviewer performed no Python parse/import or runtime check.

## Scope carried into adoption

The README correctly states trusted same-host/current-clock private-directory
provisioning, not Windows ACL enforcement, hostile-writer isolation, remote or
post-reboot freshness, secure erasure or uptime. Hashes/session metadata are not
unknown-issuer authentication. Raw file/exception/client-private inspection by a
hostile cooperating caller is outside this premise. The no-hostile-writer
premise also bounds path/TOCTOU assumptions; these are not adversarial filesystem
operations.

`READY` means the private file was validated and public metadata produced,
not recipient acknowledgement, placement completion or continuing service.
Later ready/boot failure can leave that earlier facet beside overall FAILED;
it never refunds issuance or proves delivery. Old tokens remain historical
status/exact-duplicate capabilities on a later explicit service, not new-write
authority. The code does not pretend file deletion revokes copies.

Structural custody still uses the existing stores and can leave hosting
`workspace/operations` empty. No proof/acceptance/reclamation changes were made.
Populated contribution and actual post-issuance failure behavior still require
their own selected evidence; synthetic helper fixtures cannot establish them.
The later helper-control review and root integration-adapter review are separate
artifacts, not silently covered by this PASS. Preserve this checkpoint once
selected, along with the exact reviewed source bytes.
