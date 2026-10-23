# Ordinary peer coordinator: source implementation checkpoint

2026-10-23. Owner: `ordinary_api_flow`. Canonical guard PASS; source-only under
the adopted `ORDINARY-PEER-SURFACE-PLAN.md`. No import, test, network request,
native operation, service, Lean build or Git operation was run. Root selects
integration/runtime; independent review remains required before use.

## Owned source and stable review pin

`software/v5/ordinary_peer_package/peer_api.py`, 533 lines:
SHA-256 `a05a7e9a4e40329bbf994cbd1926672bb8c0b02fd6754d8ef62db519718e709a`.
Only this coordinator and this checkpoint were written by this assignment.
The used ordinary package/core/native payloads remain unchanged. Owner CLI owns
new peer/profile files; root owns file-only assembly and integration documents.

## Agreed public interface

- `await find(loaded, config, allowance, *, network_budget=None)`
- `await receive(loaded, owner, custody, config, allowance, *, network_budget=None)`
- `publish(loaded, owner, custody, config, allowance)`
- `await serve(loaded, custody, config, allowance, *, ready=None)`

`loaded` is the verified package namespace with A/O/installation/root; shared
module identities are checked. `allowance` is the existing owner original grant:
deadline, check(), operation(A), account(worker_cpu). It is never replaced.
CLI owns owner/custody open/close and pinned config/result files. API owns any
index and Provider it opens. No operation executes at module import.

`PeerFailure.report` retains completed stages and sanitized error/cleanup data.
Admission is recorded immediately after the unchanged core returns. CHECKED is
new native acceptance; REUSED_LOCAL_ACCEPTANCE explicitly preserves the existing
local warrant without claiming another check. `acceptance_facet` and
`local_acceptance_available` make that distinction machine-readable. Later
deadline/accounting/cleanup failure never undoes or hides the returned admission.
Index batches are not atomic: each committed publication is retained separately.

## Strict owner configuration

All objects reject extra/missing fields. CLI pins a <=2 MiB duplicate-rejecting
config before operational dispatch/state opening and rechecks it afterward. API copies the selected
config and validates operation fields/limits before their consequential action.

- Contacts: label -> {host, port, tls, server_name, ca_file, ca_sha256}.
  Optional values are explicit null; CA file/hash are paired. Plain HTTP is
  loopback-only; remote endpoints use verified TLS and selected server name.
  Null TLS CA selects system trust. Selected CA bytes are pinned before/after
  each network call under the immutable owner-file/OS premise, not remote input.
- Find: {contacts, providers, specs, limits, offer, page}. Limits are the existing
  nine SearchSession fields, further bounded to <=256 candidates, <=512 requests,
  <=32 MiB replies. Offer has max_bytes/max_expanded_bytes/max_age_ms; page has
  the eight existing candidate_query limits. Provider order is explicit.
- Receive: {contacts, selection, parent_root, limits}. Selection is one returned
  {provider, snapshot_id, record}; snapshot is provenance, not a warrant. Limits:
  requests/reply_bytes/units/unit_bytes/total_bytes/missing/preflights/locator_bytes.
- Publish: {index, context_root, targets, max_unit_bytes, max_total_bytes}; targets
  are exact {name, export_id, unit_id} rows, at most 64. Index is {path, limits,
  create}, using the six existing discovery-store limit fields.
- Serve: {index, host, port, tls, lease_seconds, cleanup_seconds, limits,
  share_all_custody, exclusive}. Existing index only; both scope flags must be
  true. Limits are max_connections/max_requests/max_reply_bytes/operation_ms.
  TLS is null or {cert_file, cert_sha256, key_file, key_sha256}; keys are never
  reported. Integer lease plus >=10-second cleanup reserve must fit the original
  allowance. The synchronous readiness callback receives no secret material.

## Resource and authority preservation

Find uses the existing unknown-snapshot offer and positive candidate verifier,
with bounded advisory continuation only. It never claims global completeness or
verified skipped-interval coverage. Metadata alternatives are not suppressed by
first-seen object identity. No retries, referrals or provider expansion exist.
Search is deliberately fail-fast on transport/invalid-provider failure: earlier
matches survive in PeerFailure.report, but later selected contacts are not tried.
It is not availability failover or resilient-federation qualification.

An API-composed find/receive must pass one original OrdinaryBudget. Find prepays
its full search caps before any fetch. Shared receive rejects unless its two
network fields equal the original ledger caps, including discovery prepayment;
it then consumes only that ledger's remaining balance and narrows its deadline.
This is not a new receive grant. Independent CLI commands are separate explicit
owner calls. Failed fetches retain existing full-cap charges; request/header
overhead is reported. Search output retains <=256 records of <=16 KiB each,
bounded summaries/diagnostics, never raw proof units or expanded source bodies.

Receive creates one admission OperationBudget before acquisition, binds exact
preview/evidence/name/output census, and bounds total units/bytes/missing frontier
and iterations. It fetches dependencies only from the selected contact; unavailable
closure is refusal, not global absence. Preflight READY is still inert. The same
parent/remaining grant goes to owner.admit; native CPU is charged once in finally.
No peer `.olean`, saved catalog, native snapshot, source or PASS is imported.

Publish verifies selected targets against the explicit protected local context
and retained exact custody evidence before deriving/indexing previews. Index
admit remains metadata-only. Internal per-operation SQLite budgets do not renew
the enclosing owner deadline; original checks run around work and after cleanup.

Serve exposes ALL addressable objects in the selected custody store, with no
per-object ACL. Root selected CLI-held existing OrdinaryAdmission owner lock
through service cleanup, serializing supported same-owner mutation. API-only
inert rehosting still requires caller serialization. The API closes the listener,
cancels/gathers tracked tasks and verifies no server/tasks/reserved replies remain.
On stop failure it attempts remaining cleanup phases within the original reserve,
closes its index regardless, and reports uncertain cleanup as failure; CLI closes
custody/owner afterward. It does not claim hard containment: all reports say
COOPERATIVE_REQUIRES_EXTERNAL_JOB. Finite external supervision remains necessary.

## Reused closure and next qualification

Only four existing support modules are added by root assembly: ordinary export
adapter, search session, discovery query and candidate query. Their exact pins
are in the adopted plan. No core/install/wire schema, Lean helper or acceptance
relation changes; no old build/campaign should be repeated.

Next independent review should focus on strict config refusal, shared-ledger
prepayment/mismatch, no-progress closure, partial admission/publication outcomes,
CA/TLS scope, lease-timeout distinction and cleanup. After a separate root finite
selection, cheap pure controls plus one installed public reciprocal seam are
the proposed evidence. This source checkpoint is not runtime qualification,
independent-host evidence, a useful-growth advantage or final-v5 completion.
