# Incremental inert host implementation contract

2026-10-28. Source-only implementation of SELECTION.md and root's
INCREMENTAL-HOST-INVARIANT. Candidate custodian.py SHA256
`510b922d18f42debaa3cffef5775db61121beccb4883cc352b5ee9d9350dac67`.
Copied predecessor ordinary_dedicated_host/custodian.py remains unchanged at
`63c500ce84e6f1bb0459645d93a6bb84b75efc30958b5e6eabcb8623a343daef`.

This supersedes the author's earlier exact-generation append/recovery proposal.
The independent custodian permits partial disclosure of approved inert inputs;
it does not need atomic whole-batch publication. No append intent, pending-update
state, recovery command, rollback, remote write or new store schema is introduced.

## Interfaces and identity

`initialize(loaded, host_root, config, allowance, *, profile_sha256, finalize)`
accepts exactly schema `DMKN_INCREMENTAL_HOST_INIT_V1`, custody_limits,
index_limits and partial_publication:true. The root must be fresh. Initialization
creates the existing permanent marker/host lock, empty custody and empty index,
checks zero object/export/posting/feature counts and the initial snapshot, then
successfully closes both stores. Only afterwards does it write/fsync a bounded
descriptor and rename `.HOST.pending` to fresh `HOST.json`, under the host lock.
That temporary file is only the existing one-time creation mechanism, not an
append journal. Failure before descriptor installation leaves an unusable root;
there is no initialization retry/recovery API. A failure after installation is
reported with initialized:true rather than pretending the installed descriptor
was rolled back; process/lock cleanup must still be established externally.

The descriptor has exactly `DMKN_INCREMENTAL_HOST_DESCRIPTOR_V1`, profile_sha256,
semantic_id, namespace, custody_limits, index_limits, partial_publication:true,
assurance and mathematical_acceptance:false. Its SHA256 is a stable operating
configuration pin. It contains no content counts, latest snapshot or lifetime
target list. No existing profile/root is rebound or migrated.

`append(loaded, host_root, config, allowance, *, profile_sha256,
expected_host_sha256, finalize)` accepts exactly schema
`DMKN_INCREMENTAL_HOST_APPEND_V1`, bundle_directory, manifest, targets,
share_all_bundle:true and allow_partial_publication:true; bundle_limits is the
only optional field. It requires that exact incremental descriptor. Limits come
from the descriptor and must equal the existing databases' configuration; the
append cannot provide replacements or reset counters. A static V1 seal refuses
with HOST_APPEND_REQUIRES_INCREMENTAL_HOST.

Use the existing bounded manifest/batch reader and its <=64 MiB aggregate input
ceiling. The unchanged target validator accepts 1..64 distinct export IDs per
invocation, each with a valid exact unit/name binding and a unit in the approved
manifest. Those limits apply to supplied work, including duplicates, not the
lifetime index. Cumulative capacity remains the existing finite store quotas.
There is no automatic dependency expansion or producer export in this helper.

## Prefix invariant and failure

The full invocation's manifest pin, selected target metadata and explicit
partial-disclosure permission are validated before insertion. Under the same
permanent host lock used by serving, each bounded batch's bytes are read and
validated against the selected manifest before any member is inserted. For each
unit and its selected targets:

1. Existing `put_evidence` commits exact inert evidence and all generated export
   locators atomically. Readback must equal the supplied bytes.
2. Generate/resolve each selected preview against that evidence and verify its
   exact export/unit binding. Existing `put_preview` commits it atomically; check
   exact preview and selected locator readback.
3. Only then call `index.admit` and check the stored record. Its existing
   transaction atomically commits the record, posting paths and immutable
   snapshot. Identical existing objects/records are reused; conflicts refuse.

Every committed index record therefore retains its required preview, evidence
and locator, under the selected store/SQLite/protected-storage premises. A
failure between steps can leave approved unindexed evidence or previews. These
are permitted because the request discloses the entire supplied bundle and
generated objects, including an interrupted prefix. No operation removes old
objects. An inconsistent or unavailable dependency closure is not mathematical
acceptance; recipients keep their own checking obligations.

Store closure is attempted on every operational exception. The descriptor,
manifest and selected configuration/profile are rechecked on normal completion.
Progress is recorded immediately after each returned commit and before its
readback, but a crash or exception inside a committing call can leave more
durable state than reported. Failed reports retain batch_complete:false and
`COMMITS_MAY_EXCEED_REPORTED_PROGRESS_ON_FAILURE`. They neither claim rollback
nor assert which unreported commits completed. A deliberate duplicate append is
a separate newly funded invocation, and rereads/revalidates its supplied bytes.

On normal success, the result is APPENDED_INERT_HOST with batch_complete:true,
observed evidence/preview/publication rows, aggregate supplied census and current
metadata, only after final validation and store/host-lock closure. A failed
append's process/lock cleanup must be settled by the existing outer supervisor
before a new invocation. No code removes a held lock or resumes an old grant.

## Service and preserved static behavior

`prepare` remains text-identical to the predecessor. Its V1 content seal, target
census and exact counts/head contract remain. `serve` retains its existing
configuration/signature, finite provider operation, TLS/cleanup and host lock.
The V1 branch still requires exact sealed custody counts, latest snapshot and
object count before service.

For an incremental descriptor, serve opens the same stores under that lock,
reads current bounded metadata and verifies one actual current snapshot. It
does not compare these values to frozen content counts. The lock remains held
while the provider reopens/uses the index and closes, so supported appends cannot
change that selected state during service. Store opening may perform SQLite
recovery of incomplete individual transactions. A safe durable prefix can then
be served without a separate application recovery mechanism.

V2 init/append/serve reports use
`host_identity_kind: STABLE_INCREMENTAL_CONFIGURATION_NOT_CONTENT_IDENTITY`.
`current_content` contains custody_counts, index_snapshot_id and index_objects.
Successful append additionally records before_content. V2 READY includes the
current_content fields and `prior_append_completion: NOT_ASSERTED_BY_SERVICE`;
the final V2 service report has the same disclaimer. Service never upgrades an
interrupted batch into a successful batch report. The content observation is
scoped to the held-lock operation, not a claim that the collection stays frozen
after it returns. Empty initialized stores can be served with their empty index
snapshot. Static READY/final semantics are unchanged.

## Work and scope

Normal initialize/open/serve reads bounded descriptors, metadata and one
snapshot, plus existing package/bootstrap/database work. Append reads supplied
units and selected previews/records, including selected duplicates, and touches
their existing index paths. There is no enumeration/copy of all previous
knowledge, reconstruction of an owner context, historical-target list, or walk
through prior snapshots. SQLite B-tree/open/journal costs and producer export
costs are not claimed constant or independent of collection size. Disclosure,
indexing and hosting do not check mathematical truth.

No imports, controls, database access, native work, network or Git operations
were executed by this source authoring task. Root owns integration and runtime
selection; independent source review and focused controls have separate owners.
