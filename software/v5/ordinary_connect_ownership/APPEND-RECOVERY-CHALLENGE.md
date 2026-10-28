# Independent challenge: incremental hosting needs no batch recovery journal

2026-10-28, growth_design_audit. Source/theory only. Canonical guard passed.
No product imports, database access, execution, network, implementation or Git
operations. Root owns selection. This challenges NEXT-CENTRAL-DECISION and then
the simpler counterproposal adopted in INCREMENTAL-HOST-INVARIANT. It does not
attest current database contents or qualify a future implementation.

## Decision

**Prefer the static configuration descriptor and monotone committed-prefix
contract. Do not implement the proposed intent/pending/recover subsystem.**

An independent inert custodian needs to preserve and serve selected contributions.
It need not promise atomic publication of every multi-object batch. Existing
per-object custody commits and per-record index commits suffice if every prefix
is an authorized, valid host state. The old exact-generation seal creates the
need for reconciliation; that stronger generation contract is not intrinsic to
the role. A fresh V2 policy may explicitly support partial publication while V1
retains its existing immutable semantics.

This removes a consequential source of implementation and assurance cost without
weakening mathematical acceptance: hosting and indexing remain advisory, and
recipients independently check the mathematics they acquire. The policy change
must be visible and authorized, not silently applied to old V1 roots.

## State and proof obligation

Write a host state as H = (D, E, L, P, I, S), where D is its stable descriptor,
E evidence units, L generated export locators, P previews, I discovery records,
and S retained immutable index snapshots. All identities are exact content or
domain-separated identifiers under the selected semantic interpretation.

The relevant hosting invariant is:

1. Every stored E, L and P member is structurally validated, bound to the chosen
   interpretation and explicitly approved for disclosure.
2. For every r in I, there are e in E, l in L and p in P such that r identifies
   exactly p; p resolves against e for the selected export; and l identifies
   that export within e. Hash/length equality and exact byte comparisons are
   retained at the respective boundaries.
3. Every visible snapshot is an internally committed index snapshot over such
   records. A supported operation never removes support for a retained record.
4. Descriptor, store configurations, namespace, profile and finite capacities
   agree. One permanent lock serializes initialization, updates and serving.

This is **not** dependency-closure availability or a claim that stored statements
are true. An evidence unit may name dependencies this host does not hold. Such
acquisition can fail; recipients must not interpret a search record as acceptance.

Base case: create valid empty stores under the permanent lock, verify their
bounded metadata, close them successfully, then install the static descriptor.
No descriptor is published if initialization fails. The empty index satisfies
the invariant vacuously. A partially created root is not initialized merely
because some SQLite files or the permanent marker exist.

Inductive transitions, each under that lock:

- Evidence insertion validates exact approved bytes and atomically commits the
  evidence plus **all** its generated export locators. It adds no discovery
  record. An exact existing duplicate is checked and reused.
- Preview insertion follows resolution against already committed evidence and
  commits the exact validated preview. It still adds no discovery record.
- Index admission validates its adapter-derived record and atomically commits
  that record, its posting structures, metadata and new snapshot. Its evidence,
  locator and preview have already committed. Duplicate admission checks the
  same record and creates no new snapshot.

Each transition preserves the invariant. Failure before an individual commit
leaves that transaction absent after SQLite recovery; failure after it leaves
the permitted new state. Induction therefore applies to every committed prefix
of any bounded append. A failed append does not require a complete plan or an
operation journal to establish that surviving records retain their support.

## Interruption outcomes

| Last completed boundary | Durable permitted state | Later service |
| --- | --- | --- |
| Before any new evidence commit | Previous state | Previous committed snapshot |
| Evidence and locators committed | Approved evidence may be unindexed | Previous index; committed evidence can be served by exact identity |
| Preview committed | Approved preview may be unindexed | Previous index; exact committed custody remains accessible |
| Index transaction committed | New record and snapshot have complete hosting support | Current committed snapshot includes that record |
| Some targets completed, later target fails | Mixture of complete records and approved unindexed custody | Current committed subset; no claim of complete batch publication |
| Commit happened but response was lost | One of the above states; caller may not know which | Service reports actual current metadata; append outcome stays unknown |

Reopening stores performs ordinary SQLite transaction recovery. It does not
retry an append. An operator can deliberately submit a new funded append with
the same bytes; exact duplicate behavior makes that reasonable, but it is a new
operation and all supplied bytes/work are charged again. A successful later
service must never rewrite a failed/unknown batch receipt into success.

## Necessary conditions and concrete failure modes

- **Approval precedes mutation.** The append config binds an exact bounded
  manifest and selected targets and approves all supplied units, locators and
  generated previews, including unindexed declarations and a partial batch.
  Approval only for indexed targets would permit unintended disclosure: one
  evidence unit can export other names whose locators are generated together.
  The general static descriptor policy alone is not approval of arbitrary new
  input bytes; each append needs its own affirmative disclosure fields.
- **Per-unit validation precedes its commit.** Hash/length/identity checks bind
  actual bytes to the pinned manifest; the selected preview must resolve against
  that exact evidence. Whole-batch precomputation is unnecessary for prefix
  safety. A bad later unit can fail without invalidating earlier approved units.
  All normal bounded syntax, target-membership and aggregate input limits remain.
- **Order is an obligation.** Index-first insertion followed by interruption
  creates a visible record without custody. Separate transactions alone do not
  prevent it. The supported append must preserve evidence/locator -> preview ->
  index order even for duplicate paths and error handling.
- **Serialization covers actual work.** Every supported writer and service uses
  the same permanent lock. Never replace its file to bypass contention. Process
  death releases the OS handle; uncertain live worker/task cleanup must first be
  settled by the existing supervisor. Voluntarily releasing the lock while a
  residual writer can still mutate state would violate the premise.
- **Protected local storage remains a premise.** The marker is a role convention,
  not a security sandbox against arbitrary local SQL or a malicious filesystem.
  Unsupported mutation can break the invariant without changing the descriptor.
  Old count equality was not a full integrity audit against such mutation either.
- **Initialization is distinct from append.** Publishing a descriptor before
  both empty stores are valid would make a partially initialized root appear
  usable. Preserve failed fresh roots; no generic initialization recovery is
  required. Descriptor/profile/limits mismatch refuses before an append write.
- **Fixed capacities and monotone data remain.** No counter reset or cap increase
  follows from appending. Index capacity refusal can leave approved custody; that
  is a valid partial result, not an excuse to hide storage charges.

## What the descriptor does and does not identify

For V2, HOST.json identifies fixed policy/configuration, including profile,
interpretation, namespace, capacities and explicit partial-publication semantics.
Its unchanged hash does not identify current corpus contents or completion of a
particular batch. Reports must distinguish these meanings. Current counters and
the selected index snapshot identify actual current service state separately.

The existing offer path obtains index.snapshot(), derives its exact snapshot ID
and supplies authenticated metadata for that snapshot. Historical snapshot reads
already take exact IDs. Under stopped-host writer/service serialization there is
no concurrent append within a finite service lease, so the selected current head
is stable during that lease. No per-append HOST replacement is needed.

The index's coverage claim stays COMMITTED_METADATA_NOT_SOURCE_CORPUS. Neither
that snapshot nor the stable descriptor proves that the host indexed every
stored export, every supplied target in an interrupted batch, or all mathematics.

## Durability boundary

The committed-prefix argument covers process interruption under the selected
SQLite atomicity/durability and protected-storage assumptions. Its cross-store
step is explicit: an earlier successfully committed custody transaction remains
present when the later index transaction survives.

Do not derive arbitrary power-loss tolerance solely from PRAGMA synchronous=FULL
or DELETE journaling. Filesystem/device behavior and successful flush semantics
matter. A hypothetical storage failure retaining the later index commit while
losing the earlier custody commit violates strict hosting closure. Existing
clients must still fail acquisition safely, but that weaker behavior is not a
proof of the hosting invariant. Corruption and arbitrary hardware loss remain
outside this process-interruption argument.

An external intent file is not a magical cure: its own persistence and ordering
also need a supported durability model. Retaining a large reconciliation protocol
solely to avoid stating that model would not justify its cost. If a future
deployment requires stronger crash guarantees, specify the platform failure
model and choose the smallest mechanism that meets it then.

## Why not SQLite ATTACH or the original recovery plan

ATTACH can support cross-database atomicity under suitable SQLite/platform modes,
but current custody and index objects own separate connections and their own
BEGIN/COMMIT scopes. Their SQL and lifecycle would need refactoring for a shared
transaction. Such a change would still not atomically publish an external HOST
file, and could enlarge transaction work. It is unnecessary when prefixes are
approved. Keep it as an option only if a concrete workflow later requires atomic
batch visibility rather than partial publication.

The original intent/recovery design could implement a different contract, but
would add obligations that this role can avoid:

- Intent must precede mutation and bind exact planned inputs and prior state.
  Enumerating every generated locator is not a small <=64-target plan: supplied
  evidence can contain far more exports. A bounded per-unit plan plus locators
  derived from stored planned units is the safer design if ever required.
- A <=64-target update creates at most 64 new snapshots. Recovery could traverse
  that suffix to an exact old head; that is not license to walk all history.
- Custody object/export charges and index object/posting/sequence changes can be
  reconciled against planned identities. Index logical-byte charges additionally
  depend on actual deduplicated CAS-node insertion and shared paths. Planned
  records alone do not independently determine that delta.
- Recovery must distinguish absent/committed/conflicting input, interrupted seal
  replacement, and committed-but-unacknowledged publication. Missing external
  inputs should not force replay or falsely certify completion.

These are real complexities if exact generation sealing is required. With the
chosen stable descriptor there is no seal publication after append, so those
branches disappear rather than being implemented under a weaker name.

## Small implementation checks that would change the decision

Source review should check descriptor readiness, per-append authorization,
target binding, fixed quotas, transaction order, shared-lock coverage and V1/V2
dispatch. Bounded controls should interrupt after evidence, preview and index;
reopen and inspect the permitted state; preserve an exact old snapshot; exercise
duplicate/conflict/capacity refusal; and verify cumulative targets can exceed
64 while each append remains bounded. No mathematical owner, proof replay,
large corpus or new network campaign is needed for this principle.

No whole-history walk or independent counter reconstruction is required at
startup. SQLite recovery/open I/O still has its real platform/storage costs;
the claim is absence of a mandatory application-level corpus replay, not a
constant wall-time guarantee. Producer export may resend a dependency closure;
only actual bounded supplied bytes justify delta-cost claims.

## Source anchors

- NEXT-CENTRAL-DECISION.md reviewed SHA256:
  `0a5ef4bf8d0c351b25c894790fade0e89399a0d5dbce93e7eabb5003a8237dcd`.
- ordinary_multi_source/ordinary_acquisition.py `_put`, getters and status:
  `076130f7a34b505df33ee550501d1c4276bb46e408ff226df765225933a0658e`.
- ordinary_sparse_access/discovery_store.py admit/snapshot/status:
  `26ccca0fda86a255c38f7c3cc39b6b1fd88deba2ae10c6f79bc562b872c9502c`.
- ordinary_dedicated_host/custodian.py lock, prepare, seal and service:
  `63c500ce84e6f1bb0459645d93a6bb84b75efc30958b5e6eabcb8623a343daef`.
- ordinary_binding_reuse/baseline_bundle.py bounded manifest/batch contract:
  `e4b52c2f2e823cc98aa37c8cc7adb0cf79952def9c19b54d7072116a39fa19b6`.
- Additional source-only anchors: ordinary_registration_refresh/http_provider.py
  offer and exact-snapshot routes; its peer_api.py existing incremental publish;
  ordinary_intake_progress/baseline_intake.py `_custody_increment`.

**Verdict:** the simpler V2 principle passes this independent challenge under
the stated conditions. This is permission to implement the selected small
boundary, not evidence that implementation or public deployment already passes.
