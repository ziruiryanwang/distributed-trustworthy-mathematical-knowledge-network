# Managed contribution seam: independent source challenge

2026-10-21, support_screen. **ACCEPT DESIGN WITH THE IMPLEMENTATION CONDITIONS
BELOW; NOT IMPLEMENTED OR RUN.** Reviewed proposal
`MANAGED-CONTRIBUTION-SEAM.md`, SHA-256
`c1a37054071c8d23c162b49a554ac1fb5113190de9d22b9b7b490a0a48b8e9d1`,
under the adjacent root selection. Existing owner/source/evidence stay frozen.

Final revised proposal was then reread in full: 16,421 bytes, SHA-256
`2e8d6116235fd6d69fc924c874da9019d8f27e7cf46fce9ca20875971f60d26b`.
It incorporates the parent-plan/whole-workspace binding, fixed service cutoff,
closed-code helper failure boundary and client-object return raised during this
review. The remaining details below are implementation conditions, not reasons
to add another subsystem or delay root's narrow source selection.

The one private-file handoff plus small paired helper is a credible minimum.
It reuses the existing actual bearer-token protocol and requires no new identity,
crypto, launcher, broker, SQL or mathematical-acceptance subsystem. Acceptance is
conditional on an operator-provisioned private, non-hostile local directory and
trusted cooperating processes; ordinary-path checks do not establish Windows
ACL confidentiality, isolation from same-account code or secure erasure.

## Source findings and required details

1. **Preserve original output exclusions across relocation.** The existing
   owner `_bindings` protects the current `run`, current request directory,
   installation and original/copied source roots. The child plan relocates
   `workspace_root` into the parent's `work` and `source_roots` into the parent's
   snapshot. Re-running only that existing child check loses the outer public
   request directory and part of the parent operation. Parent preflight plus a
   fresh worker check is necessary, not interchangeable. Prefer excluding the
   entire original public `workspace_root` as well as parent/child run/control/
   source roots, installation and manager. This also rejects a sibling secret
   file inside an otherwise publicly collected operation workspace.

   A minimal implementation can authenticate the fixed nested layout from the
   child plan/source-root relationship and derive the original parent run and
   its public workspace, or copy a parent-generated operation/exclusion binding
   into the pinned worker plan and validate its relationship there. Do not trust
   an arbitrary caller-supplied exclusion list. Retain the original parent
   operation identity in the envelope; the fixed child name `managed-worker`
   alone is not that identity. Do not change persistent manager config to add
   per-call paths. Apply overlap in both directions to each specific protected
   root; excluding all shared ancestors up to `E:\` would accidentally forbid
   every possible local sink. Both request paths and the private directory are
   nonsecret metadata under this local design, not confidential pathnames.

2. **Fix the interval before issuance or file I/O.** The current `_worker`
   computes `until = monotonic()+service_seconds` once after service startup.
   Insert the grant/write/ready sequence after that calculation and reservation,
   and guard against the same `until` before/after every bounded I/O. Never move
   that calculation below handoff or start another service interval afterward.
   Publish the actual owner-selected service cutoff, not just
   `service.ready()['deadline']`: that grant deadline can be later than the
   worker's deliberately shorter `until`. Use `service_until_ns`, an integer
   floored from that original cutoff: the existing `F.strict` rejects every JSON
   float, so copying `service.ready()['deadline']` is not parser-compatible.
   Define this paired helper as same-host/live-clock scope. A recipient caps
   its independently selected original deadline by this cutoff; it does not
   acquire a new duration on reading. Cross-host/after-reboot freshness is not
   inferred from a monotonic number, session nonce or credential-file mtime.

3. **Keep credential parsing/writing errors closed-coded.** Existing owner
   `_error` saves `str(error)` and notes to ordinary results; the helper must
   never let a secret-bearing value, failed serialization object, JSON document
   or token appear there, in a traceback, repr, stdout/stderr or client reports.
   Map secret-handling failures to fixed codes with suppressed exception context.
   Writer returns only a validated nonsecret pin; reader should return an
   in-memory `PlacementClient` plus explicitly whitelisted public metadata,
   not a conveniently printable credential dictionary. Readback checks canonical
   exact fields and the actual ledger identifier formula:
   `SHA256(token.encode('ascii'))`, where token is 64 lowercase hexadecimal
   characters; hashing the decoded 32 bytes would be wrong. The 8192-byte cap,
   exclusive create, flush/fsync/close and exact readback are appropriate under
   the stated no-hostile-writer premise. They are neither atomic publication to
   arbitrary concurrent readers nor ACL enforcement. Recipients consume only
   after the complete ready pin, not by polling a partly written secret file.

4. **Distinguish issued, delivered and accepted work.** Controller issuance
   charges a controller call; ledger `issue` commits the grant-count row before
   returning the token. Failed exclusive-open, write, fsync, close, readback,
   ready publication, boot finalization or recipient receipt cannot refund it.
   An ambiguous issuance commit likewise cannot justify an automatic reissue.
   Record a nonsecret delivery stage/grant ID when known; successful delivery is
   not a placement reservation or completed custody. The nine resource totals
   are charged by `reserve` only when a new valid manifest is admitted. Preserve
   those existing distinctions, keep failed/partial private output, fail the
   owner and attempt the original close. No retry or cleanup-based refund.

5. **Metadata does not confer revocation, current readiness or trust.** The
   exact current `PlacementLedger.reserve` checks for an identical saved request
   before checking issuing runtime/write expiry; `status` authenticates the token
   without requiring its runtime to be current. Therefore old credentials may
   retrieve historical status or repeat an identical request for its old result
   after a later service restart. They cannot reserve a new request then.
   Sealing also forbids new issue/reserve, not all historical observation.
   Deleting the file does not revoke copies. This part of the proposal is correct.

   Include nonsecret issuing-runtime metadata (already available through
   `service.report()['route']['runtime']`) and the exact selected operation,
   release/profile and session binding, beside the four existing service IDs,
   endpoints, source, horizons and limits. The paired reader compares these to
   independently expected selected-operation metadata. None authenticates an
   unknown issuer, proves a server is still live or grants an extra request cap.
   Existing `PlacementClient` independently retains egress, endpoint/TLS and
   request/byte/deadline limits, and its public report excludes the token.
   `source` remains a pull endpoint, not contributor identity or an inferred
   discovery authority. This source review does not select remote provisioning.

## Populated custody and fixed layout

The operations-empty argument is supported by the actual path, not just by
absence of a proof in the example. `Workspace.open(create=True)` creates an
empty `operations/`; the ledger continually requires no `_client` and no
`_grants`. Controller `_run` creates `EvidenceAcquisition(..., verifier=None)`;
that class forbids a verifier/admission operation and uses structural module/
packet custody. Its inherited body/packet methods commit to the same stores.
Controller index writes and route advertisement/retained restoration use the
existing SQLite stores/journal. None creates a Workspace proof-operation
directory. The actual reclaimer lists those databases and their journals plus
an empty `workspace/operations`, not an arbitrary recursive proof-artifact tree.

Thus ordinary populated custody-only hosting can retain the fixed reclaimer
unchanged, conditional on the fresh allowed layout, single owner, actual close,
horizons, finite entry count and apparent-byte cap. This does not cover a workspace
with earlier mathematical operations, external writers or arbitrary extra files.
Do not remove proof evidence or increase deletion scope to make a check pass.
Actual population must still fit its chosen apparent-byte envelope; a cap refusal
is not permission to expand it. A secret file deliberately remains outside this
layout and belongs to the operator's separate secret lifecycle.

## Exact minimal successor recommendation

Select a fresh source cut only after root's decision:

- Replace the owner in that successor with a new closed public schema containing
  one nullable `intake_grant`; implement parent/worker preflight and one
  issue/write/nonsecret-ready sequence within the already fixed interval.
- Add one SDK helper, e.g. `client/private_credentials.py`, with paired bounded
  writer/reader and explicit expected-operation metadata. Reader creates the
  unchanged client from independent egress/caps, without token-returning reprs.
- Update only the corresponding source map, owner/worker profile count/schema
  assumptions and short API documentation. Adding one helper to current126 SDK
  rows yields127 and ordinary owner-inclusive snapshots128; do not leave the
  current exact126/127 guards or stale source-profile assumptions in a successor.

Leave service, controller, ledger, protocol/client, providers, acceptance,
supervisor and reclaimer unchanged. Narrow writer/parser/output-exclusion
controls plus one finite separately running contributor using retained published
artifact bytes suffice for this boundary; no new proof or broad campaign is
justified. The present lifecycle fixture's2020 admission/retention horizons
cannot issue a live grant (`issue_token` checks current UTC). A contribution
selection must explicitly choose its own live finite horizons and real resource
quote, rather than silently reusing or mutating that retired-horizon fixture.
Do not force immediate retirement/reclaim by asserting a false future UTC bound.

## Inspection scope

Read actual source in `retained_advertisement` (service/advertisement),
`selective_placement` (controller/ledger), `placement_network` (client/provider),
`terminal_i` (workspace/evidence transport), current ownerf213baff and
reclaimer19713fc4, plus unchanged installed boot/launch, TLS pin helper and
inherited delta body/packet implementation. The seven proposal source anchors
were hash-checked; no source/runtime execution, Python parse/import, state access,
secret access, Git, product edits or new test selection occurred.

This is an implementable local-owner-premise recommendation with precise
conditions, not evidence of OS-enforced privacy, actual populated managed use,
mathematical acceptance, independent hosts or final v5 completion.
