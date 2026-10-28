# Next core decision: bounded append for an independent inert host

2026-10-28, operable_scale_decision. Source/theory only; canonical guard passed.
Root owns selection. No runtime, database, owner, native, network, code or Git
operation occurred. This revisits the specific deferred boundary in
CONTINUOUS-USE-DECISION, not the wider release audit. Source selection is the
connect-ownership map `80d46cbe...`; its dedicated-host/storage roles are unchanged.

## Decision

**Recommend the smallest stopped-host append plus explicit recovery operation
for fresh dedicated hosts.** Reuse the existing inert custody and index stores,
one host lock, immutable identities and retained index snapshots. Keep the
current mathematical-owner publication path for operators who already need that
owner. Do not build a daemon, remote-write protocol, new storage engine, live
writer/reader concurrency or general migration facility.

The concrete role is an independent library custodian: it repeatedly accepts
operator-selected bounded inert evidence from contributors, preserves earlier
selected knowledge and serves it from the same local endpoint. It neither opens
a mathematical owner nor rechecks the corpus as a condition of hosting. Each
recipient still checks mathematics. Selection/curation and remote acquisition
remain separate from this local update operation.

This role is already represented by dedicated hosting; its growth path is the
missing piece. Source reasoning is sufficient to establish the limitation. The
current host cannot add its 65th indexed target to the same generation, even
though the underlying index supports much larger finite counts. No giant corpus
or repeated mathematical experiment is needed to demonstrate that code bound.
The earlier deferral was reasonable while contact maintenance was the cheaper
cross-cutting obstruction. Root now reports that refresh/contact workflow passed;
that does not remove this distinct ingestion/seal limitation.

## What existing APIs can and cannot do

| Existing route | What it supplies | Why it is not this role's complete growth path |
| --- | --- | --- |
| `peer publish`, `create:false` | Incremental index admission and duplicate reuse | Requires `OrdinaryAdmission`, a selected checked context and matching local bindings; public CLI opens/locks that owner. Creating one solely to host inert bytes changes the role and adds checking/context costs. |
| `host prepare` then repeated `host serve` | Safe fresh inert generation, bounded metadata startup and finite service | `prepare` requires a fresh root. The seal fixes exact custody counts, latest index snapshot and 1..64 lifetime indexed targets. There is no append/recover command. |
| `OrdinaryStore.put_evidence/put_preview` | Per-object atomic, byte-exact, idempotent inserts; evidence and all its export locators commit together | Separate from the discovery database and host seal. Calling these underneath a sealed host makes its normal serve preflight refuse. |
| `Store.admit` | Per-record atomic index update; duplicate equality; new immutable snapshot and retained old snapshots | Does not atomically update custody or HOST.json and cannot establish a complete host lifecycle by itself. |
| Fresh delta-only stable hosts | No repeated base-byte copying | Each generation remains limited to 64 indexed targets and a separate root/service/contact obligation. More providers consume bounded contact/search slots. |

The low-level SDK primitives suffice for a knowledgeable caller to design its own
lifecycle; they do not already provide the public operation and crash contract.
Bypassing the dedicated marker or editing SQLite is not an existing supported
solution. Ordinary commands deliberately refuse dedicated-host state paths.

Inputs need not repeat dependency closure. Existing `baseline_bundle.make_manifest`,
`read_manifest` and `validate_batch` accept selected bounded portable evidence;
batch validation explicitly does not check dependencies against an environment.
The fixed-seed writer's stronger closure construction is a different producer
path. An append can therefore ingest just selected delta units using the existing
manifest format. Missing dependencies remain an availability limitation, never
mathematical acceptance or an instruction to fetch/replay all history.

## Exact proposed semantics

Use a new host seal version with aggregate custody counts, index object count,
latest snapshot, fixed limits, profile/semantic/namespace bindings, previous
seal digest and the exact completed update intent digest. Remove the lifetime
list of every target from the seal. Keep at most 64 selected targets **per update**;
the existing finite index limits bound the cumulative target count. Old target
records live in the index; normal startup must not enumerate all historical
targets or follow the whole update chain.

Start this capability on fresh hosts under the selected successor profile.
Existing PROFILE-bound V1 hosts remain valid through their approved old package;
there is no silent rebind, in-place software upgrade or capacity enlargement.
A one-time new-root copy, if an operator chooses it, belongs in adoption cost.

`host append` takes an exact current seal hash, exact delta manifest/configuration,
the existing finite bundle ceilings, selected targets and explicit disclosure of
**all supplied units, previews and generated locators**, including unindexed
declarations. It runs only after the previous service has actually closed and
under the existing permanent host lock. It cannot overlap service or another
append. Duplicate identical objects/records reuse existing content; conflicting
bytes/records refuse. Names need not be globally unique: exact portable IDs remain
the identities. Existing limits are never reset or increased.

Publication is atomic at the **host generation boundary**, not an all-or-nothing
transaction across the whole input batch. Per-object and per-target commits are
retained. A failed attempt may be explicitly recovered into a new generation
containing its validated durable subset, with a PARTIAL outcome. This is the
same general partial-work principle as existing `publish`, made durable and
visible for the independent host. It must be stated in the request and report;
a batch must never be reported complete because some objects were committed.

## Small crash protocol, with no database copies

The implementation needs one bounded active intent, an immutable seal receipt
and a small pending marker. Reuse the existing host lock and store transactions;
do not introduce an update scheduler or multi-database transaction framework.

1. Under the lock, verify the selected old seal and exact current store metadata.
   Refuse a pre-existing unresolved intent. Fully validate the bounded delta and
   derive every target preview/record before the first live-store mutation.
   Record old counts/snapshot, fixed limits and each planned evidence/preview/
   index identity, byte hash/length, and whether it already existed. Validate
   existing duplicates exactly. Retain the plan in an immutable bounded intent;
   flush it and install its pending marker before any insertion. All paths and
   mutable operation output remain separated as in current hosting.
2. Run deterministic bounded insertions: evidence plus its locators first, then
   the selected previews and index records. Read back selected bytes/records.
   Recheck input pins when rereading external delta files. Every existing SQLite
   transaction remains individually atomic. No networking, native check or
   automatic retry occurs. Capacity refusal or exhausted allowance preserves
   the committed prefix and pending intent; it never deletes prior knowledge.
3. Close both stores successfully. Only then prepare a successor seal/receipt
   from the verified actual counts and snapshot, preserving the full/partial
   distinction. Flush the new bounded file, then replace the current seal using
   a same-directory atomic namespace operation. Retain its prior seal/intent
   evidence. Resolve the pending marker only after verifying that new binding.
   No service starts inside append.
4. Normal `serve` refuses while an unresolved pending marker exists; it also
   retains the existing exact count/latest-snapshot checks. An old HOST.json is
   never treated as rollback after stores have changed. After successful
   publication and marker resolution, a separate finite serve opens the whole
   new sealed generation. Exact old index snapshots remain available through
   the unchanged index; there is no historical-store copy.
5. After interruption, a separately funded `host recover` binds the exact intent
   and old head under the same lock. It **does not retry ingestion**. It opens
   the stores for SQLite recovery, checks the planned durable identities/bytes,
   verifies that index records have their corresponding stored preview/evidence,
   reconciles counts and the bounded new-snapshot suffix, and seals the actual
   valid prefix as COMPLETE, PARTIAL or NO_CHANGE. A later append of missing
   inputs is an explicit new operation against that newly selected head.

Recovery is not just "seal current status." Its receipt must enumerate the
bounded planned units/targets as durable, absent or conflicting. Aggregate
counts must equal the old sealed counts plus the verified newly present planned
objects/locators/records. The new snapshot suffix has at most the number of new
planned target admissions, and must reach the exact old snapshot; recovery need
not traverse history before that point. Impossible order, missing indexed bytes,
unexplained counters, contradictory IDs, failed SQLite recovery or uncertain
closure refuse recovery and leave service closed. This relies on the existing
protected-store/supported-command premise; metadata reconciliation is not an
audit against arbitrary hostile database mutation.

This recovery choice matters: a missing external input or a delta that exceeded
remaining capacity need not strand the host until the original batch can finish.
Already committed approved data can form an honestly partial new generation.
Recovery can validate it from the bounded intent and its stored bytes; it need
not retain another full copy of all proposed evidence or require missing input
files merely to close the interrupted operation. Previously absent targets are
not silently indexed by recovery. No rollback/delete, grant renewal or hidden
acceptance is performed.

A crash after replacing the seal but before clearing pending is a distinct
idempotent recovery branch: verify the already published seal references this
intent and matches the stores, then acknowledge it; do not produce another
generation or reapply the delta. A lost/ambiguous marker or receipt is not grounds
to guess approval. Mismatched old metadata fails closed. Same-directory atomic
replacement and SQLite FULL do not alone prove arbitrary power-loss durability;
retain the approved filesystem/runtime premise and qualify process interruption
separately. The design does not promise uninterrupted service during failure.

## Cost argument and when the change pays

Let retained evidence after cycle i be N_i, newly supplied bounded bytes D_i,
selected targets a_i<=64, and features per target f<=128. D_i includes duplicate
inputs actually reread; sending a whole historical bundle is not a delta saving.
Let K_i cover package checks, opening, close/recovery and operation reporting.

Repeated complete-generation preparation has an unavoidable byte-work term

    sum_i N_i = n*N_0 + sum_j (n-j+1)*D_j

when each D_j is new retained content. For equal deltas this includes a quadratic
term. Appending instead pays one initial preparation plus selected-delta reads,
validation, writes/readbacks and index updates. Current index updates touch a
256-bit feature-map path, an eight-bit partition path and logarithmic vector
paths, not every historical record. A source-derived form is

    sum_i [K_i + O(D_i) + O(a_i*f*(256+8+log p_i)) indexed-node work].

SQLite B-tree accesses, page splits/journaling and recovery add real storage
costs depending on local database size; the expression is not a hard wall-time
bound or a claim of constant I/O. It states that no normal append requires a
whole retained-corpus byte scan/copy. Recovery reads at most the active bounded
delta's present content and its <=64 new-snapshot suffix. Persisted intents and
small generation receipts grow linearly with updates, and should be charged;
startup must read only current state. Per-object and database quotas still stop
finite nodes. Sharding/retention remain necessary at actual capacity.

Stable shards are often better when content rarely changes or topic boundaries
are genuinely useful. But dividing a growing same-topic collection solely to
work around the 64-target seal creates at least ceil(targets/64) host generations,
plus their finite service/contact/curation overhead. The contact map admits at
most 16 endpoints per exact route and public find at most 64 selected providers.
Those bounds correctly permit incomplete search; they do not remove the extra
coverage and scheduling cost of artificial generation shards. Append lets one
funded custodian aggregate its selected records up to existing index quotas
behind one endpoint; it does not create a global index or completeness promise.

For an investigator who already maintains and checks a local owner, existing
incremental publish remains preferable: no second store/lifecycle is necessary.
For a small static mirror, existing fresh host preparation remains preferable.
The append investment pays when repeated preserved-corpus copying, artificial
shard/service overhead or maintaining an otherwise unnecessary mathematical
owner exceeds the fixed implementation/assurance cost and ongoing intent,
recovery, extra indexing and maintenance costs. No elapsed-time speedup or real
operator adoption is claimed. The explicit independent growing-host role and
the source-enforced lifetime 64-target limit justify this narrow capability;
they do not justify a general always-on aggregation platform.

## Smallest next implementation and decision-changing evidence

Select a fresh successor for custodian.py, host.py and the launcher operation
grammar, plus focused host documentation and exact map/package integration.
Add append and recover, a bounded V2 seal/intent grammar, and bounded inspection
helpers if needed. Preserve custody/index data schemas, HTTP routes, namespace,
semantic rules, TLS, owner APIs and native support. Do not raise existing storage
caps or add a daemon, automatic feed ingestion or old-root migration.

Before any runtime, independently challenge intent-before-write ordering,
durable-subset reconciliation, committed-but-unacknowledged publication and
profile/path/limit binding. Then only changed-boundary controls are needed:
duplicate idempotence, wrong head/config refusal, interrupted custody/index/seal
steps, missing-input partial recovery, capacity refusal and refused service while
pending. A small saved-evidence sequence can demonstrate base -> append -> recover
-> serve, preservation of an old exact snapshot and availability of a new target,
with zero mathematical owner/native calls. The 64-to-65 aggregate boundary can
use existing inert target fixtures if necessary; no new theorem or enormous
growth campaign is justified. Actual large-scale benefit remains a conditional
cost argument, not a benchmark claim.

Stop and defer if implementation requires full database copying, a complete
target/history walk at each update, changing mathematical acceptance, or hiding
partial commits. The better fallback is existing owner incremental publication
or honestly bounded stable shards, rather than a broader recovery framework.

## Source evidence

- Prior decisions: CONTINUOUS-USE-DECISION `f8c0cefb3fd47215147f11293dfac5d3a6d7fed0de12402e78dbfa371a344ac0`;
  ordinary_directory_kit/NEXT-CORE-DECISION `4323b97bbda77b39e3438243f3b4233d50df374a92694339406a1fbec09d4af4`.
- dedicated custodian.py, `_targets`, prepare/read_seal/serve:
  `63c500ce84e6f1bb0459645d93a6bb84b75efc30958b5e6eabcb8623a343daef`.
- dedicated host.py, operation grammar and containment/bootstrap:
  `2a6f43fc1e2d36d2720374ab945aae95c06f4df5b934a12cbe073fb5b5b03a36`.
- ordinary_multi_source/ordinary_acquisition.py, `_put`, selected getters/status:
  `076130f7a34b505df33ee550501d1c4276bb46e408ff226df765225933a0658e`.
- ordinary_sparse_access/discovery_store.py, admit/snapshot/status:
  `26ccca0fda86a255c38f7c3cc39b6b1fd88deba2ae10c6f79bc562b872c9502c`.
- ordinary_binding_reuse/baseline_bundle.py, read_manifest/validate_batch/make_manifest:
  `e4b52c2f2e823cc98aa37c8cc7adb0cf79952def9c19b54d7072116a39fa19b6`.
- Additional read anchors: registration-refresh peer_api.py 1070-1148 and peer.py
  220-253; its http_provider.py 464-503; authenticated_index.py append_vector/
  partition_set/map_update; formal_features.py MAX_FEATURES; baseline_intake.py
  `_custody_increment`; contact_directory.py MAX_ENDPOINTS; portable_catalog.py
  `_write_fresh`. These source arguments do not attest current database contents.
