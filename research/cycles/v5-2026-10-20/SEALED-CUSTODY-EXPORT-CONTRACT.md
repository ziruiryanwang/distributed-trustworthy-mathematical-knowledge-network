# Sealed custody export and coverage V1

2026-10-22; FUTURE CONTRACT, NOT IMPLEMENTED. Complete supported knowledge of
one local generation, not a selected subset. No global scan, proof replay or
runtime. Basis129 mapa629df82, upgrade2331e8e3; stores580515e4/4264841e,
ledger59f87b93, controller ef1c9b59, lifecycle0fa3dcc4, sessions6e07010c.

## Stable cut and large resumption

Begin under finite byte/row/CPU/time/disk allocations. Authenticate release,
writer, config and marker; require SEALED_SERVING, genuine CLOSED/closure digest,
supervisor QUIESCED and no unresolved session. Seal alone is NOT a freeze.
Acquire existing manager and workspace exclusions in a reviewed consistent
order; recheck closure under exclusion. Manager exclusion covers compliant
allocate/run/retire/reclaim; workspace exclusion covers composer, custody/index,
placement/controller/ledger and route-journal writes. Private raw-store writers,
restores and same-account interference remain excluded premises, not lock safety.

Compare three designs:

- Lock-held export: smallest change; bounded pages while both locks live.
  Lock/process loss invalidates that cut's continuation. Suitable for small cuts,
  NOT the proposed solution for large cross-process enumeration/transfer.
- Durable freeze: avoids duplicate storage, but requires a future persistent
  fence checked under lock by EVERY listed writer, recovery and cleanup path,
  including direct Workspace/store entry points. Seal is not this fence.
  Crash restoration, lock order and intentional unfreeze need specified rules;
  no such new lifecycle phase is adopted here.
- Immutable disk snapshot: SELECTED CONTRACT. Under both exclusions copy the
  supported generation/manager records and required custody bytes into an
  owner-private staging archive with bounded streaming; refuse unexpected
  journals/lineage rather than recover them. Finalize only after all files,
  lengths/hashes and closure bindings are durable. Atomic final-descriptor
  publication distinguishes a complete snapshot from interrupted staging.
  Release exclusions only then. Copy costs O(local captured bytes), temporary
  disk of that order and bounded RAM; no free copy-on-write is assumed.

The completed snapshot, not reopened mutable databases, is the durable cut.
Enumeration and transfer can resume across processes over it, without holding
source locks. Interrupted snapshot creation is INCOMPLETE: preserve charges and
staging; a fresh cut is required unless source identity/exclusion continuity is
separately established. This is an explicit acquisition cost, not a claim that
every phase resumes for free. Unknown files, missing required bytes or exceeded
disk budgets prevent completion. Extra storage may make export unavailable.

Snapshot descriptor binds domain DMKN_SEALED_CUSTODY_EXPORT_V1, cut ID,
release/writer, generation/config/marker/closure, schema and mathematical/wire
domains, exact archive file map and limits. Snapshot reads verify bound bytes.
Keep source obligations in force throughout; snapshot custody alone is not a
substitute service or destination receipt.

## Exact inventory

Enumerate every committed row, including unindexed/unreferenced custody:

- Module summaries, groups, name/group associations; bodies keyed by exact
  module/universes/hash, with permitted declaration locator where available.
- Every packet digest/module/size/content and profile/module offer association.
- Current formal export records and source commitments. Historical index
  snapshots and route caches are rebuildable metadata, not migrated authority.
- Every placement manifest, phase, reservation and public outcome; committed
  receipts determine content duties/horizons. Preserve public grant policies,
  used totals and aggregate charges as history, never live capabilities.

Exclude named bearer-token/private-key classes without exposing them. Validate
commitments and references; report corrupt/unsupported rows and unknown files
explicitly, retaining bytes or UNARCHIVED disposition. Unknown files block full
inventory; unsupported content blocks its own coverage, never silently disappears.
Treat retention as outstanding unless an adopted conservative clock proves
expiry. Ambiguous requests/partial custody remain unresolved.

## Bounded resumable enumeration

Use canonical primary-key keyset order, not OFFSET. A cursor binds snapshot root,
table, last exact key, next page and prior digest. Durable progress records retain
original allocations/charges; each resumed call needs remaining or explicit new
funding, never reset counters. Reserve before work. Duplicate cursor gives the
same saved page, not a second advancement; conflicting progress refuses.
Check snapshot/progress integrity before continuation. Interrupted page emission
is either the already committed page or an incomplete charged attempt.

Hash/archive payloads by bounded streaming under versioned canonical encoding:
h[i+1] = H(domain || h[i] || canonical(page[i])).
Distinct domains bind descriptor, pages and final inventory. Require every table
end marker, reconciled counts/references and no skipped row. Oversize rows yield
INCOMPLETE, not truncation-success. Final root binds all counts/dispositions.
Work is O(local rows + bytes hashed), not global size or proof ancestry.

Completeness relies on admitted exporter/schema and exclusive-source premises.
Hashes authenticate the resulting cut, NOT adversarial nonomission without an
independently committed source root. Storage corruption is not silently repaired.

## Destination coverage and failures

Require compatible interpretations or INCOMPATIBLE. Fresh manager/grants use
existing placement transfers. Each coverage row binds source manifest/item,
destination generation, exact readback, committed receipts and sufficient duty
horizons. Trusted owner checks actual state; remote JSON is insufficient.
Mathematical admission remains the recipient's current independent gate.

Report inventory_complete, supported_coverage_complete, unresolved dispositions
and route observations separately. Coverage includes EVERY supported item and
outstanding supported content duty. Unsupported/corrupt/untransportable items
block whole-cutover claims; unresolved promises prevent retirement. Tokens,
charges and live contexts do not migrate. Failure is charged/uncovered; no
atomic cross-host transaction or automatic retry. Coverage never waives old
retention, retirement or conservative-clock rules.

Eight-body manifests split into separately charged requests; coverage checks
the union and horizons. First-four offers cannot find every retained packet.
EXACT-PACKET-ACQUISITION-DECISION744e12ee identifies the existing exact public
route for known digest AND size: fix explicit client/controller acquisition,
not wire protocol or fabricated offer cache. Until implemented, later packets
stay UNCOVERED. This smaller core fix has priority over inventory implementation.

This contract applies to a future supporting release, not arbitrary old state.
Old-schema offline export needs separately reviewed authority; no marker edits,
new-writer reopen, exhausted-budget bypass or general migration framework.
