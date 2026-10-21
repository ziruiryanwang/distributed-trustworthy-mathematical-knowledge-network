# Minimum managed contribution seam

2026-10-21, core_release; source/theory only under
`MANAGED-CONTRIBUTION-SEAM-SELECTION.md`. No product edit, import, service,
proof, deletion or new runtime campaign. Current ownerf213baff remains frozen.

## Decision for root

Use the existing token-bearing placement protocol. Add one optional, explicit
finite intake grant to a fresh managed-owner successor and deliver its credential
through one **operator-selected private credential file outside operation
reports and managed state**. A separately running trusted contributor reads that
file into the existing `PlacementClient`. This is local private-file provision,
not public grant vending, a new identity scheme, or a confidentiality claim about
ordinary Windows files. No new cryptography or network service is needed.

This is the smallest credible seam on the current PC. The current public run
path has no private return channel: request/plan bytes and stdout/stderr become
saved evidence. Do not put the token there. The existing wire routes are closed
submit/status routes, not a credential-distribution endpoint. A named-pipe
broker, authenticated callback server or child-process redesign would add more
moving parts than this specific requirement needs. They remain alternatives
if the operator cannot provide a genuinely private file location.

There is no existing credential-file reader in the selected SDK. Do not claim
otherwise: `PlacementClient` currently takes the token in memory; the TLS helper
shows an existing exact-file/pin pattern, not a token-distribution API. A small
paired write/read helper is a proposed addition, not an implemented feature.

## Source facts that constrain the design

1. `PlacementService.issue_token(source, write_until_ms, retention_until_ms,
   limits)` returns `{token, grant_id, generation, horizons, false assurance
   flags}` only to its trusted in-process caller. The current comment expressly
   forbids putting that return in ready/report/configuration or an HTTP route.
2. Controller issuance checks its live finite service grant, egress-selected
   source endpoint, grant sublimits and the generation's admission/retention
   horizons. `PlacementLedger.issue` generates 32 random bytes and commits only
   their SHA-256 identifier, issuing runtime, policy and zero resource use.
   The grant-count cap is consumed before the token is returned.
3. New manifest reservations require the issuing runtime to equal the current
   runtime, enforce token and generation resource totals, and commit the full
   conservative reservation before structural acquisition. A duplicate exact
   request returns its already charged row, not a fresh attempt. Recovery has
   its own already funded one-pass path; handoff adds no recovery authority.
4. `PlacementClient(egress, contact, expected, token, deadline=...,
   requests=..., incoming_bytes=..., outgoing_bytes=..., operation_ms=...)`
   already binds the exact intake endpoint, four service identities and token.
   Its submit/status methods carry the token in bounded canonical request
   bodies; its report excludes it. Public failures are closed codes. Remote
   use requires existing system-CA TLS policy; plaintext is explicit loopback.
5. The token's `source` is the endpoint **from which the custodian pulls bytes**,
   not the contributor's identity or a target selected through discovery.
   The contributor must make its selected module/packet/body bytes available
   through the existing read provider while the placement is outstanding.
6. Read routes themselves require no intake token. Readers independently adopt
   contacts/egress/TLS and their existing finite search/acquisition budgets.
   A custody response does not grant mathematical acceptance: recipients still
   use the existing actual verifier before mathematical use.

## Concrete proposed public interface

Use a new owner schema/source cut, leaving the used owner unchanged. Add exactly
one nullable `intake_grant` field to serve/seal requests:

```text
null
or {
  source: {host, port, tls, server_name},
  write_until_ms: integer,
  retention_until_ms: integer,
  limits: existing placement resource vector,
  credential_path: fresh absolute private file path,
  confidentiality: "OWNER_PROVISIONED_PRIVATE_CREDENTIAL_DIRECTORY_V1"
}
```

One grant is enough to close this missing composition boundary. A bounded list
can be considered only if an actual multi-contributor requirement warrants it.
No token value belongs in the public request. `source`, horizons and all nine
resource limits are explicit operator decisions; neither a discovery response
nor remote contributor can choose/expand them. Grant issuance is legal only on
an OPEN generation; existing API refusal handles an already sealed selection.

The prospective worker, after exact session join and actual service startup:

1. Validates an ordinary fresh credential path and existing ordinary parent.
   Requires disjointness from install, source roots, the entire original public
   output workspace, both parent/child request/run outputs, persistent manager,
   and their ancestors/descendants. Do not add dynamic paths to stored manager
   config. Parent checks this before launching. The fixed parent adds its exact
   current plan SHA to the internal worker parameters; this is not a new public
   caller option. The worker derives the parent plan at
   `context.workspace_root.parent/plan.json`, authenticates that SHA with the
   existing plan reader, and checks that its workspace is the parent's run/work
   and its original source roots are the parent's run/sources. It thus recovers
   the original public workspace/root protections rather than treating relocated
   child roots as a complete ancestry. No arbitrary parent-path input is needed.
2. Calls existing `service.issue_token` once. No generation/ledger method changes.
3. Serializes a new bounded credential envelope, at most 8192 bytes, containing
   schema, token, grant_id, exact service bindings, read/intake endpoints,
   authorized source, horizons, resource vector, adopted release hash, exact
   session number/nonce and the already-fixed same-host `service_until`. This
   is the owner's planned finite serving cutoff, not the service object's later
   possible deadline. These metadata do not grant more authority than the token
   and current service grant already possess.
4. Creates the selected file with exclusive creation, writes the complete
   canonical bytes, flushes/fsyncs and closes it, then freshly validates exact
   bytes/ordinary file identity. No overwrite, auto-retry, token reissue or
   cleanup of uncertain output. A partial file remains a failed handoff.
5. Only after successful close publishes a nonsecret ready facet containing
   `grant_id`, endpoint/bindings, `service_until`, and
   `{path, bytes, sha256}` credential pin.
   Never place the credential contents in ready/results, copied parameters,
   exception messages, captured stdin/stdout/stderr, or HTTP diagnostics. The
   paired helper must raise only fixed closed error codes, suppressing raw
   credential/parse exceptions: current owner `_error` saves `str(error)`.
   Its publishing return contains only the nonsecret ready facet, not the
   original `issue_token` result.

The separately running contributor gets the nonsecret ready information from
the selected local operation and opens the explicitly selected private file.
The paired reader uses ordinary-path checks, a small exact byte cap and the
advertised length/SHA, strict canonical JSON/field validation and checks
`SHA256(token)==grant_id`. It binds metadata to the expected operation/release,
session, endpoints and service identities, then supplies the token in memory to
the unchanged `PlacementClient`. Prefer returning that existing client object
whose report already excludes the token, not a secret-bearing decoded dict.
Reader errors have the same closed-code rule. No arbitrary callback or pickle
is needed.
The file's digest does not authenticate an unknown issuer: its origin is the
operator-selected private path plus selected public operation. The existing
high-entropy token hash is not treated as a secret.

The reader retains its independently supplied egress and request/byte/deadline
caps; it does not take new executable authority from a credential file. For
same-host use, the already-fixed ready `service_until` caps its own original
deadline; the service may still fail earlier, so this is not an uptime promise.
Do not export a raw monotonic clock as portable cross-host time. A
remote recipient uses its own shorter finite deadline and the existing server's
enforced bounds; secure remote credential transfer is operator provisioning,
not a new public network endpoint selected by this change.

## Lifetime, failure and confidentiality argument

**No capability revival:** handoff does not alter the original live service
grant, worker Job, session deadline, write horizon, retention horizon or resource
vector. Generation closure ends current service authority. On a later service
run the old token cannot reserve a new request because its issuing runtime
differs. Sealing prevents new issuance/reservations. Original counters persist.

**Important nonclaim:** expiry/closure is not complete token revocation. A later
explicit service can permit that old token to observe its historical status or
repeat an identical request for the already stored outcome. Do not promise that
deleting the credential file erases recipients' copies or disables all status
access. The current APIs do not implement per-token revocation. Write-horizon
checks also inherit the existing local wall-clock premise; the independent
finite monotonic service grant remains enforced if that clock is wrong.

**No refund after delivery uncertainty:** if issuance commits and writing,
fsync, readback, ready publication or recipient receipt fails, that grant remains
consumed. Do not erase its ledger row or issue a replacement automatically.
An explicitly chosen later operation can spend another remaining grant. The
resource reservation itself occurs when the existing server accepts a manifest;
failed handoff does not invent a placement charge that was never made.

**No renewed service interval:** issuance and file handoff spend the already
allocated service interval. Their guards use the earlier service/worker cutoff;
never start another `service_seconds` timer afterward. Synchronous bounded file
I/O is not hard interruptible; check before/after and rely on the same encompassing
Job for an actual stall. Failed handoff fails the owner while normal close is
still attempted. Do not convert the fallback quiescence path into success.

**Explicit confidentiality premise:** a non-reparse path, `open(...,"xb")`, a
hash and a Unix-style mode600 do not prove Windows ACL privacy. The operator
must provision a directory readable only by the intended trusted local account(s)
and prevent unrelated writers/backups/exposure. This design does not itself
establish or audit that ACL, isolate hostile same-account code, or secure-erasure
the memory/file/pagefile. An explicit private-secret sink is an intentional new
owner-level boundary; it must not be called an ordinary report. Credential
cleanup belongs to the operator's secret lifecycle, not the managed reclaimer.
One fixed file/capped envelope per admitted operation bounds this added output;
repeated issuance still meets the manager/session and ledger-grant caps.

If that private-storage premise is unacceptable for a selected deployment,
choose an existing authenticated confidential provisioning channel or separately
design the OS-enforced handoff. Do not silently weaken the premise or launch a
new authentication framework during the current integration.

## Populated custody is compatible with the fixed reclaimer

This distinction is important: **structural placement is not local proof
authoring.** The actual fresh Workspace constructor creates `operations/` empty.
`PlacementLedger.active` requires `workspace._client is None` and no `_grants`.
`PlacementController._run` creates `EvidenceAcquisition(..., verifier=None)`,
then uses module/packet/index database methods and placement/route ledgers.
It never calls Workspace.grant/operation, creates a proof-output directory,
invokes Lean, or obtains a mathematical warrant. Packet inspection is structural.

The corresponding stores hold groups/bodies, packet blobs and index objects in
`modules.sqlite`, `evidence-packets.sqlite` and `discovery.sqlite`; placement and
route observations are in their two existing SQLite files. Retained restoration
reads those stores and journals finite location commands, without opening a
proof operation. Location runtime state remains inside the selected per-run
fixed layout. Therefore, starting from the allowed fresh layout, ordinary
token-bearing placement and retained restoration can populate the hosted corpus
while `workspace/operations` stays empty.

The fixed reclaimer can consequently remain unchanged for this populated
custody-only role, subject to its actual closed-state, horizon, identity,
bounded-layout and apparent-byte checks. A hosting workspace that also runs
local mathematical operations may accumulate artifacts under `operations/`
and is **not** covered. Keep contributor proof work in its separate ordinary
workspace; do not expand reclamation or delete its proof evidence to make a
fixture pass. Secret files remain outside both managed state and its reclaimer.

## Minimum implementation and decision-changing check

Select only: (a) one fresh managed-owner successor with the nullable grant field,
preflight and one issue/write/ready call; (b) one small paired private-credential
helper available to the contributor; (c) ordinary API documentation and exact
source-map change. Reuse existing grant, client, provider, controller, ledger,
service, supervisor and reclaimer unchanged. No builtin/launcher, daemon,
global identity, custom TLS, crypto proof or mathematical-policy change.

The next meaningful test is one ordinary separately running contributor using
the existing published artifact/provider to submit through that handoff; assert
nonsecret evidence, actual retained acquisition/public receipt, charged caps and
orderly close. Inspect that hosting `operations/` remains empty. A separate
ordinary reopen/restore/read can reuse existing qualification where its exact
boundary is unchanged. No new proof generation or broad search campaign is
needed to establish this composition seam. A later exact nonsecret-file scan of
the small new evidence is useful; copying/printing the credential into the
test report defeats the property being tested. Root decides any implementation
and finite integration after source review; nothing here launches it.

## Exact source anchors

Resolved from consolidated121 input8ba37072, plus reviewed managed additions:

| Logical source | Selected physical branch / SHA-256 |
|---|---|
| `client/serve_placement.py` | `retained_advertisement`, `7e735337d595894e25fd07a8dcc9ad8cd3ba9f1c042ba930684b7798232cb7fa` |
| `placement/controller.py` | `selective_placement`, `ef1c9b59072127379e955bafeea001a22d6e3d10c9c46dca1304f85ab09e2b49` |
| `placement/ledger.py` | `selective_placement`, `d955990c347ed466617c752893dded8b8494dd266a050b045352c77c48f21a91` |
| `placement/network.py` | `placement_network`, `1ec5c452ec129ae033f0577ebac6223e2cf3192d4724a3d31fe2e5c27a06cd4b` |
| `placement/advertisement.py` | `retained_advertisement`, `5aa23ee76115355ad319ae4acfd4ab418e010166e53b6ed02c82eb25d34d4510` |
| `client/workspace_evidence.py` | `terminal_i`, `8531ee14e24d60617491b9f00e14ea1f7c410a279d116322489fe763a421ea68` |
| `evidence_network/transport.py` | `terminal_i`, `7ac7204b6e97b48eb1764c92b98437ad87e45f0fc62aa78973f5985816d63827` |
| `client/managed_owner.py` | `managed_operator`, `f213baff68319d3c84c9bc93597e4d3f9fe2990ead4f225a29c938626c17d1d4` |
| `placement/reclaim.py` | `bounded_reclamation`, `19713fc4baec821a5c77a0071182c63401b292cbe79a7ed7c04b7deba50e1894` |

This proposal is actionable source design, not current software behavior,
OS-enforced secrecy, populated managed runtime evidence or a full-v5 result.
Screen's independent source challenge tightened parent-output ancestry,
closed-coded helper errors and the exact planned service cutoff before any
successor implementation was selected.
