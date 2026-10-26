# Prospective decisive controls for ordinary sparse access

2026-10-25. `concept_software_bridge`; source-only test plan, not test code or an
execution result. Canonical guard passed. This assignment changes this checkpoint
only. Root owns source selection, package integration, execution and adoption.
No native checking, mathematical episode, network campaign or repeated package
qualification is proposed here.

Reconciled with the completed eager-maintenance contract, including its exact
V2 schema proposal, immutable `candidate_mode`, original-ticket settlement and
per-target publication failure boundary. This plan is prospective; none of its
outcomes is adopted merely because the source argument is plausible.

## Decision and boundary

Test the narrow candidate in [SPARSE-ACCESS-CONTRACT.md](SPARSE-ACCESS-CONTRACT.md):
a fresh, explicitly opted-in ordinary discovery Store with at most eight fixed
feature pairs, maintained transactionally during metadata admission. Use original
atomic record identities, snapshot commitments and positive membership proofs.
The new sparse-positive request/page/cursor protocol is explicitly V2; ordinary
V1 remains the default and retains its old accounting rules.

This supersedes the earlier proposed lazy-builder readiness matrix for this
test plan. There is no dynamic configuration, backfill or partially built cache
in this first candidate. The meaningful states are disabled, no eligible pair,
configured-and-current, an old selected snapshot with a current cache, and an
invalid configured state. A deliberately damaged readiness marker is a fault,
not an operational partially built cache that the implementation must repair.

**Decisive question:** can the same authenticated positive record be reached
after one sparse driver step where V1 requires three atomic driver steps,
without changing its identity, weakening positive verification, renewing an
owner allowance, or corrupting index admission on failure?

Here a driver step is the V2 meaning of `charged.scanned`, including a charged
empty seek when attempted. It is not all SQL operations, record probes, proof
reads or elapsed cost. Never report this as one total database probe or a
threefold whole-workflow speedup.

## Actual seams and small inert fixture

Use the selected successor's real `OrdinaryExportAdapter`, `Store`, authenticated
summary/vector helpers, V1 and V2 candidate paths and `SearchSession`. Source
inspection for this plan used the retained ordinary package at
`experiments/v5-local-checks/fair-investigator-assembly01/assembled/package`, its
`support/discovery/{ordinary_export_adapter,discovery_store,candidate_query,
search_session,fair_search}.py`, and the fresh contact test's actual ordinary
preview construction. Root must select the coherent new package before execution;
this old package is a read-only reference, not a target to patch.

The existing `software/v5/discovery/test_candidate_query.py` provides useful
negative patterns but creates an in-memory Store using `Store.__new__`. Do not
reuse that shortcut for configuration, transactional maintenance or reopening:
those are precisely the new boundaries being tested.

Use two separate small fixtures; do not blur their authority:

1. **Algorithm/transaction fixture.** A deliberately synthetic metadata adapter
   returns valid generic records with explicitly forced same-partition IDs,
   correctly bound raw lengths/hashes and selected atomic features. Actual fresh
   Store startup, `admit`, summary/proof generation and verification run unchanged;
   no direct insertion substitutes for Store admission. This is not an ordinary
   Lean object identity. With A the smaller query-feature ID, admit two A-only,
   two B-only and AB0 records. At S0 both atomic lists have length three and AB0
   has ordinal two in both. Then append A-only to force B as minimum anchor and
   AB1 for the later S2 cut. Seven inert records cover the core discriminator,
   both orientations and old-cut filtering without collision hunting.
   A third feature C on the initial four one-sided records but not AB0 supplies
   the extra-conjunct rejection control without enlarging that initial corpus;
   A-only/B-only means only relative to the two tested pair atoms.
2. **Ordinary end-to-end metadata fixture.** Use the actual ordinary adapter on
   a bounded syntactically valid preview whose type explicitly contains two
   bound portable symbols. Reuse expression/name/binding shapes from
   `software/v5/ordinary_formal_query/query_controls.py` and the fresh contact
   control's preview envelope; do not rerun those completed suites. Derive the
   record and both type-symbol keys, admit it to real plain and opted-in stores,
   obtain/verify the actual summaries, and retrieve it with both V1 and V2 in
   the partition computed from its real export identity. No forced ID prefix,
   replacement ordinary adapter, or imported fake evidence. Compare unchanged
   semantic ID, export ID, preview bytes/hash, locator, RecordID, atomic feature
   keys and snapshot identity across the two paths. Symbol bindings and unit IDs
   are still unproved test metadata, not actual mathematical acceptance.

For comparisons, the plain and opted-in stores use the same fixture adapter,
admission sequence and base limits. Each needs its own fresh path. Additional
tiny stores are allowed only for isolated admission-fault cases. Never copy or
touch retained provider, custody, proof or paper state. Record exact fixture bytes.

## Eight grouped controls

### 1. Identity preservation and fixed configuration

After each paired-fixture admission, compare the two stores' derived records,
RecordIDs, snapshot IDs/descriptors and authenticated atomic summaries. They
must be identical even though the opted-in store has extra local tables and
different local configuration/accounting. Verify the pair rows preserve both
original ordinals and admission sequence, and `completed_seq == Store.seq`.

Close/reopen the opted-in store with its exact original configuration. Refuse a
changed pair set or quota configuration, a ninth pair, duplicates/reversed
duplicates or malformed pairs, according to the selected canonical contract.
Refuse any purported in-place opt-in/migration of an existing default store.
Re-admitting an existing object must not add pair rows, advance the sequence,
change the snapshot, or consume new logical row capacity.

### 2. The one-versus-three discriminator

For S0, query `{A,B}`, partition P, start zero, using generous remaining limits:

- Default V1 with `scanned=2`: no hit, not an absence or completeness result.
- Default V1 with `scanned=3`: AB0 at original ordinal two, one record load and
  one positive proof.
- Explicit sparse V2 with `scanned=1`: the same AB0 at original ordinal two,
  one attempted sparse driver step, one record load and one positive proof.

Compare the exact record and its original atomic membership proof, not only its
name or hit count. Observe executed SQL or the actual driver read boundary to
ensure the sparse path is not secretly scanning rejected atomic IDs while
reporting one step. Account separately for seek, secondary membership, record,
SQL VM, hashing and proof-node work; do not require those to equal one.

Use `matches=1` if necessary to avoid a second end-detection seek after AB0.
Do not count a final empty seek as a second candidate record or insist that an
advisory cursor certify the entire sparse interval. An honest V2 result can jump
over ordinal positions; those positions are not verified scan coverage.

### 3. Current/old cuts, both orientations and fallback

At S2 the minimum atomic anchor is B. Sparse access must still retrieve AB0 and
AB1 with their original B ordinals and proofs. Querying retained S0 through the
same newer cache must exclude AB1 using the selected cut and atomic descriptor
ceilings, returning exactly AB0 with the original S0 proof.

Query `{A,B,C}` at S0, where C has four members and AB0 lacks C: A remains the
minimum anchor, the pair driver visits AB0, but no hit may be returned. This
checks the full query conjunction instead of accepting every pair member.

Issue V2 against the plain disabled store and against an opted-in store with no
eligible configured pair. Both must take the explicitly described atomic V2
fallback within that same request and allowance, with `access_used` identifying
atomic access. No cache creation, backfill, new snapshot or renewed request is
permitted. Also cover a query with an additional conjunct whose authenticated
minimum anchor is not in the configured pair: do not reorder into a pair path
that violates the selected anchor restriction.

Damage the configured readiness/configuration marker in an isolated scratch
store. The path must refuse, not silently treat corruption as a disabled cache,
build a replacement, or return a falsely exhausted empty result. This is a
reachable-corruption check, not proof that all possible cache omissions are
detectable. In particular, deletion of an unvisited sparse row may omit a valid
candidate without invalidating another positive proof; completeness is still
unverified.

Also corrupt an encountered row's companion ordinal or admission sequence past
S0's permitted boundary. Refuse that inconsistent row; do not treat it as a
legitimate absent conjunct or let it enter the old-cut result.

### 4. Unchanged positive verification and strict V2 binding

Starting from a genuine accepted V2 reply, independently mutate original anchor
ordinal, membership sibling, record content/features, record/object identity,
partition, snapshot, anchor, query features, duplicated hit and hit order. Each
invalid positive must refuse before session candidate-state commit. Original
record validation and original vector verification must run, not a new trusted
pair-membership assertion. Pair access metadata is advisory and cannot replace
any of these checks.

Reject false coverage/mathematical-acceptance flags and invalid cursor progress,
range or counter relationships. The required new distinction is precise:
V2 may have `next-start > charged.scanned`; V1 must still reject that shape.
The reply alone must never choose which verifier the session uses. A held V1
ticket rejects a V2 reply and a held V2 ticket rejects a V1 reply, even if their
individual positive proofs would otherwise be valid.

### 5. Finite reads and unfinished-candidate continuation

Use small deterministic exhausted SQL-VM, record-probe, proof-read/hash and
cooperative-deadline allowances at changed sparse boundaries. Observe actual
SQL callback charging for new statements; no unmetered whole-pair census or
linear admission-history scan is allowed inside a query. The driver seek,
including an empty seek when attempted, must consume the declared work budget.

Interrupt after locating a sparse positive but before its full proof/envelope
fits or completes. The result must not advance beyond that unfinished positive:
continuation can reattempt its actual anchor ordinal. Already skipped sparse
gaps need not be replayed as V1 atomic positions. Assert retained connection
settings/progress-handler cleanup and no index mutation after read refusal.
Check whole serialized V2 envelope bytes, including new access metadata, against
the negotiated cap. Reuse existing source-reviewed helper invariants where
unchanged; do not rerun all inherited limit combinations merely for breadth.

### 6. Atomic metadata admission and bounded cache cost

Measure the same actual Store admission transaction, not a separate mock cache.
Record before/after logical contents of `objects`, atomic `postings`, CAS nodes,
feature heads, snapshots and all meta fields, plus pair rows/counters/marker.
Inject one controlled failure after at least one oriented pair insertion and
before commit. All durable logical contents must equal the pre-admission state,
both immediately and after close/reopen. Then an ordinary valid admission on
that scratch store must succeed; no stale in-memory node/cache state may leak
the rolled-back sequence.

Independently exhaust the configured pair-row and pair-logical-byte quotas while
base-index capacity remains available. Refuse the offending metadata admission
atomically; do not commit the base snapshot and leave the pair cache behind.
Count both orientations and any configured local overhead exactly as specified.
The fixed pair count bounds admission maintenance; test one record matching
multiple configured pairs so accounting is not accidentally per-record only.

The shared SQLite maximum-page cap remains effective. A new actual SQLite FULL
control is warranted only if source review finds that new writes/transaction
ordering change the already-tested failure boundary; otherwise retain that
existing evidence and inspect the unchanged cap/rollback path. Byte-for-byte
database-file equality is not required after rollback: logical database state
is the oracle. No process-kill crash campaign is proposed by this plan.

Metadata publication can now refuse because optional pair capacity is exhausted.
Record that cost rather than hiding it. Source review must confirm this does not
delete or revoke separately held mathematics/custody. A synthetic test does not
qualify native custody behavior merely by naming an untouched dummy artifact.

### 7. Aggregate allowance; deferred public forwarding smoke

Exercise `SearchSession.begin_candidates` with the default and explicit sparse
modes, both retaining operation `candidates` and the same full `limits.scanned`
reservation against aggregate `examined`. Accept, malformed reply, wrong-version
reply, invalid proof and transport failure must settle the original ticket once;
provider work claims must not refund its reservation. On refusal candidate and
coverage state remain unchanged; the failure is not a new allowance.

After the source/API controls pass, root may separately select a minimal public
forwarding smoke for immutable FairSearch `candidate_mode`, the exact
`/v5/discovery/sparse-candidates` route, `find` and nested `directory-find` mode
forwarding, unchanged defaults, and explicit Store opt-in on publish/serve. A
recording transport can delegate to actual provider dispatch if a socket adds
no decision-changing evidence. Label that in-process control accurately. One
unsupported-route response from a legacy provider must remain charged and
incomplete: no automatic V1 retry or silent extra owner grant. Do not repeat the
completed directory suite or bundle a public/native campaign into this first
source/API test allocation.

### 8. Explicit V1/non-claim regression

Run a small default-mode smoke on the same real ordinary fixture and preserve
V1 request/page/cursor schema, anchor choice, scan-distance inequality and
conservative session settlement. Source-map review must show no atomic feature,
record, namespace, mathematical verifier or custody-format change. Preserve
existing V1 provider/client compatibility rather than claiming old clients can
request the new optimization.

For every positive, fallback, refusal and exhausted path, retain
`mathematical_acceptance=False`, `global_complete=False`, and
`verified_scan_coverage=False` as applicable to the existing result contract.
No new theorem generation, semantic relevance guarantee, authenticated omission
proof, net growth benefit or worldwide deployment claim follows from this suite.

## Minimal execution proposal and adoption rule

After the contract and exact source successor pass independent review, root may
select one native-free focused run of these changed boundaries against one
coherent pinned package. Prefer a single short process with small fresh SQLite
stores and local session calls; no native setup, socket campaign or large corpus
is needed for the decisive result. Keep any fault injection confined to deliberate
scratch-state corruption or transaction/time/transport boundaries; do not replace
positive record derivation, cryptographic verification, Store admission or session
acceptance. Hash source/fixture inputs and preserve raw group outcomes.

Root should set finite wall/CPU/memory/output allowances after reviewing actual
test code. This plan grants no runtime and invents no measurements. Adoption
requires the one-versus-three discriminator, unchanged positive verification,
identity/cut invariants, atomic failure and finite aggregate accounting together.
A test failure remains a failure; repair requires a fresh reviewed successor,
not edited used evidence or relaxed expected outcomes.

If the implementation cannot meet this boundary without unbounded query-time
builds, namespace-changing records, weakened V1 checks, an uncharged retry or
hidden publication costs, stop and reconsider the design. Once this finite
access-path obstruction is removed, return to the next actual investigator or
deployment obstacle instead of enlarging this cache into a new research platform.
