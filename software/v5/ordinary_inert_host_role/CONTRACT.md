# Python-only inert host core contract

2026-10-28. Selected source implementation under IMPLEMENTATION-SELECTION.md.
Candidate `host_core.py` SHA-256:
`e032c40dc3fd2557d42d91176d029a95ffb302aea03cf902332abaa79d71b31f`.
No runtime or package adoption follows from this source checkpoint.

## Exact scope and source reuse

This role stores disclosed ordinary evidence, derives selected discovery records,
and serves bounded read requests. It performs no mathematical acceptance, owner
opening, source execution, native installation, certificate handling or Lean call.
Every result and readiness record retains mathematical_acceptance:false.

The four action bodies are adapted from `ordinary_incremental_host/custodian.py`
`510b922d18f42debaa3cffef5775db61121beccb4883cc352b5ee9d9350dac67`.
Their storage operations, order, schemas, bounds, full-sharing permissions,
permanent lock and stable-descriptor policy are preserved. Paths/JSON helpers
now come from genuine inert support; actual lower codec/store/index/provider
implementations remain the selected unchanged current sources.

The narrow service composition comes from `ordinary_registration_refresh/
peer_api.py` `12c29d1edb3f3bc0483d9fe01abb3a4c69dbc4cdc5225ead32c28842bb4699dc`.
It retains provider/TLS/lease/cleanup behavior and omits the inaccessible owner,
authoring-map and general peer operations. The existing host config never allowed
authoring/contact maps. No general peer API or mathematical guard was changed.
The service index close now explicitly confirms `index.db is None`, matching the
outer host's existing store-close criterion; failure is terminal and retained.

## Genuine support interface

The selected loader executes captured `support.py` as `inert_host_support`, then
this core. Public entrypoints require its exact `InertHostSupport` type, the same
module object in sys.modules and the externally selected source-profile SHA-256.
The support object has actual `.modules` and `.api` module mappings, `.root`,
`.python_runtime_root`, `.semantic_id`, `.namespace`, `.profile_sha256`, `.verify()`,
and bounded `ordinary/read/hexid/fields/uint/write_fresh` methods.

Core validates the exact E/S/PE/B/PP/O/DS/OA/H/F identities against that mapping
and sys.modules, codec references, computed semantic ID and adapter namespace.
It neither creates nor imitates `NativeInstallation`, admission or a catalog.
Its type is a local source-selection interface, not a mathematical warrant.
Cooperative callers, immutable approved code and protected local storage/OS are
premises; these Python object checks are not a hostile in-process sandbox.

The public signatures preserve the existing call shape with support as argument 0:

- `initialize(support, host_root, config, allowance, *, profile_sha256, finalize)`
- `prepare(support, host_root, config, allowance, *, profile_sha256, finalize)`
- `append(support, host_root, config, allowance, *, profile_sha256, expected_host_sha256, finalize)`
- `serve(support, host_root, config, allowance, *, profile_sha256, expected_host_sha256, finalize, ready=None)`

The caller supplies the original allowance with `.check()` and `.deadline` and
a finalizer that rechecks selected source/runtime/configuration bytes. No core
function renews it. The public launcher owns Windows Job containment and clean
process closure. Direct calls require equivalent caller supervision/serialization.

## State and identity

New state must be disjoint from selected software/Python and approved inputs.
Every action uses the same permanent `DMKN-DEDICATED-HOST.json` marker and
one-byte `host.lock` inode. The lock is opened and nonblockingly locked with
msvcrt; no operation deletes, replaces or recreates it to bypass another holder.
New roots cannot be nested under recognized existing host/owner/database roots.

Initialization creates fresh empty existing OrdinaryStore/DiscoveryStore instances,
checks their empty counts/initial snapshot, then closes both. It writes/fsyncs
`.HOST.pending` and renames it to fresh `HOST.json` while still locked. This is
the one-time descriptor installation, not an append journal or recovery protocol.
Preinstallation failure leaves an unusable root; no retry/recovery action exists.
Postinstallation failure preserves the installed descriptor and reports its state.

The immutable `DMKN_INCREMENTAL_HOST_DESCRIPTOR_V1` binds the fresh source profile,
semantic ID, exact namespace, custody/index limits, partial_publication:true and
inert assurance. Its hash identifies operating policy, never the evolving content.
It contains no cumulative target list, frozen current counts or latest snapshot.
Old full-package and mirror roots are not relabeled, migrated or supported under
this new profile. Existing descriptors with another profile refuse before writes
or listening; no migration or descriptor-rewrite command is provided.

`prepare` retains the static `DMKN_DEDICATED_HOST_SEAL_V1` branch. It copies all
approved supplied units, indexes the selected targets and seals exact metadata
only after successful census/readbacks/store closure. A static seal cannot append.
Static preparation uses the same sparse bundle grammar as the current host; the
old mirror's complete-foundation/import-closure rule is not added here.

## Append and permitted failure prefixes

The unchanged schemas and strict operational JSON parser enforce the existing
explicit permissions: initialize requires partial_publication:true; append requires
share_all_bundle:true and allow_partial_publication:true; prepare requires
share_all_bundle:true; serve requires share_all_custody:true and exclusive:true.
Operational metadata uses F.strict; evidence continues using its distinct exact
codec grammar. A boolean/null metadata document is not accepted as evidence.

Append pins its manifest, validates all selected target metadata and the descriptor,
and reads each complete bounded batch before inserting any member of that batch.
The eight-line inert batch boundary retains baseline_intake's exact bounded reads
and unchanged B.validate_batch; the admission-bearing module is never imported.
All listed units, including support-only units, retain their input order and bytes.
Target count is 1..64 per invocation; unchanged bundle bounds include <=64 MiB
aggregate input. Lifetime capacity comes from existing cumulative store quotas.

Under the permanent lock, each supplied unit and selected target follows:

1. Commit evidence and its generated locators via actual OrdinaryStore, then
   verify exact evidence readback.
2. Derive/resolve the selected preview against those bytes, commit it, and verify
   exact preview/locator readback and unit/export binding.
3. Commit the record/postings/snapshot with actual index.admit, then check readback.

Every committed indexed item thus has prior retained evidence/preview/locator
under the selected SQLite/protected-storage premises. A failure may leave approved
unindexed evidence/previews or an unreported committed index prefix. Reports retain
batch_complete:false and COMMITS_MAY_EXCEED_REPORTED_PROGRESS_ON_FAILURE, never
rollback or complete-batch claims. No old objects are removed; identical supplied
duplicates are reread/revalidated under a new invocation and existing conflicts
refuse. No global dependency closure or mathematical truth is inferred.

Store closure is attempted on operational exceptions. Normal append completion
rechecks manifest bytes, exact immutable descriptor, marker and caller finalizer
before releasing the lock and reporting batch_complete:true. The outer supervisor
must settle process closure after failure before another supported invocation.

## Finite service and costs

Static serving checks sealed custody counts, latest index snapshot and object
count. Incremental serving checks bounded current metadata and one actual current
snapshot; it permits any legal committed prefix without a batch recovery seal.
Readiness records the current snapshot/count observation and explicitly states
prior_append_completion:NOT_ASSERTED_BY_SERVICE for incremental hosts.

The actual provider uses existing discovery and ordinary read routes with all
selected custody disclosed. Provider limits, numeric address validation, pinned
certificate/key bytes and required TLS outside loopback are preserved. Optional
map/module routes remain unserved, although their unchanged parser import closure
is retained by the source loader. Request bytes cannot select local code or paths.

Service reserves the existing 10..60-second cleanup interval within the original
deadline, starts one 1..3600-second finite lease, and attempts provider stop/drain
and index closure on every path. Success requires no remaining provider server,
tasks or reserved reply bytes. Fallback cancellation uses that same original
cleanup deadline. asyncio.run shutdown drains while the permanent host lock is
still held; a stuck shutdown remains subject to the original outer Job envelope.
Custody closure and finalization precede releasing the lock. Cleanup uncertainty
is retained as failure, not READY or successful lease completion.

Normal open/serve uses bounded descriptors, metadata and one snapshot plus
existing database/bootstrap work. Append handles supplied bytes/selected records
and their index paths. It does not reconstruct an owner context, traverse proof
histories, copy the existing corpus or rebuild a lifetime target list. SQLite
open/recovery/B-tree costs are not claimed independent of corpus size.

Authoring was source-only: no Python imports, controls, databases, native calls,
service launch or Git mutation. Independent source review and later root-selected
changed-boundary controls/public lifecycle are required before adoption.
