# Materialized pair index: changed-source review

2026-10-20. Reviewer: core_release. **PASS for the selected source change and
one bounded changed-boundary control run; not runtime or release acceptance.**
Root owns execution and adoption. No product code was imported or executed in
this review; no proof, native verifier, network, installation or Git mutation
was performed. The installed distribution and every used predecessor remain
unchanged.

## Scope and decision

Reviewed the seven successors against their selected predecessors, the complete
adapter implementation, actual client inheritance/query paths, the new controls,
and `Select-ConjunctionIndex.ps1`. The evidence workspace base is the current
`interface_views/workspace_evidence.py`, not its older logical-path predecessor.
Formal features gains one schema constant; Store and authenticated snapshots
gain only its allowlist/import entry. Existing Store/query algorithms and
mathematical acceptance are unchanged. The three client changes are limited to
profile-aware workspace creation/status and the two adopted query-compiler calls.

The selected compiler uses the **first canonical eligible pair only**, not the
earlier overlapping multiple-pair proposal. That simpler choice is sufficient
for the selected obstruction and avoids an unnecessary optimization mechanism.

## Correctness argument

Fix one valid profile namespace, a collision-free interpretation of feature
hashes, and one admitted record whose features are recomputed by this adapter.
Let A be its atomic feature set. For every configured pair p={a,b}, construction
adds c_p exactly when a and b belong to A. All atomics remain. The original
atomic query Q is compiled either unchanged or to

    Q' = (Q \ {a,b}) union {c_p}

for the first configured pair contained in Q. Consequently Q is contained in A
if and only if Q' is contained in the extracted feature set. Overlapping other
pairs do not enter this replacement. Deduplication and the existing 1..8 input
bound are preserved; nested pair specifications are rejected as atomic inputs.
This is predicate preservation for correctly extracted records, not a proof
that a provider indexed every relevant object or used the correct extractor.
`resolve` recomputes the actual record and rejects a forged compound record.

For the same admitted corpus, snapshot and partition, the pair posting list is
the intersection of its two atomic lists. The rarest-anchor scan driver after
replacement is therefore no larger than before. A fixed small intersection can
remain small while the two nonmatching atomic tails grow. This does not bound
the intersection for all corpora, guarantee optimal pair choice, remove output
size, or prove a wall-time/full-cost benefit. Added postings, hashing, storage,
publication and maintenance must be paid for over an actual query workload.
An ordinary shared-library comparator receives this same index improvement.

## Bindings and refusal boundaries

- Profile shape is exactly the selected schema plus 1..8 canonical distinct
  atomic pairs; canonical atom/pair order and the 8192-byte cap are checked.
  The returned profile is copied. Schema and complete profile bind the new
  namespace. Default descriptor and record bytes remain unchanged.
- Adapter binding includes namespace, schema, raw profile and immutable pair
  entries. Accidental internal mutation refuses. This is local trusted-code
  integrity checking, not protection against an attacker modifying Python state.
- Atomic extraction happens once; pair checks use only the original atomic set.
  Existing 128-feature/16 KiB record caps remain. Overflow refuses, never silently
  drops atomics, pairs or exports. Comparisons must disclose any refusals.
- Workspace profile validation precedes filesystem effects. Exact config bytes
  are retained and checked on reopen; changed profiles cannot reinterpret an old
  index. Legacy workspace schema requires its old exact field set.
- Ordinary publication already uses the workspace's adopted adapter/Store.
  Both `find` and direct-contact binding now use that same adapter's compiler.
  No new transport, theorem identity, mathematical acceptance path or authority
  is introduced.

## Controls and their limits

`controls.py` was authored by this reviewer and independently source-reviewed by
root and the client/discovery owners before selection. It imports current
successor overlays in dependency order, never an old test suite. The legacy
adapter is loaded only as a comparator. Nine controls cover:

1. Exact legacy namespace/record bytes and query behavior.
2. Pair iff and first-pair query equivalence over all eight three-atom subsets.
3. Malformed profile, copy isolation, distinct namespaces and mutation refusal.
4. Actual adapter rejection of wrong-profile and forged-compound records.
5. Feature, record and posting caps without truncation or committed rows.
6. Actual structural export to Store/query and exact-profile reopening.
7. Same-corpus synthetic hot lists, old snapshots and extra storage/postings.
8. Actual ordinary workspace config persistence, legacy behavior and prewrite
   malformed-profile refusal.
9. Both changed ordinary function bodies reaching the actual profile compiler.

The 128-atomic-feature fixture has 121 distinct symbol features, three basic
features, three edge features and one result-head feature. Its selected pair
would be feature 129 and must refuse. Record-cap data remain individually valid
name components before exceeding the encoded cap. Store status contains durable
metadata, not attempted-work telemetry, so the quota rollback equality assertion
is appropriate. Workspace and Store close methods are idempotent.

The hot fixture has explicitly synthetic object IDs/types, not accepted
mathematics. Its selected expected scan counts are 5 versus 1 on nine records,
then 8 versus 1 on fifteen records. Adding a second matching record leaves old
snapshots unchanged and gives final pair scan 2. Expected total postings are 20
initially and 36 finally, including respectively 1 and 2 extra pair postings.
All records remain admitted; no rejected row can be claimed as a saving.

The ordinary query wiring control uses an exact-class inert client/channel and
real egress-policy validation. It deliberately throws immediately after the
actual adopted compiler, before sessions, acquisition or I/O. Unchanged action
wrappers are bypassed. This establishes wiring only, not a live client lifecycle,
mathematical authority, network use, process restart or independent-host behavior.
The workspace persistence control performs actual same-process close/reopen.

The runner retains fixtures/output, forbids subprocess launch and socket helper
connections, and makes no performance-timing or mathematical acceptance claim.
Normal asyncio wakeup-loop construction is not itself a remote operation. This
small native-free check is the appropriate implementation discriminator; a new
proof campaign would not test the changed index boundary.

## Exact reviewed bytes

Paths below are relative to the sole canonical root
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

| Source | SHA-256 |
|---|---|
| software/v5/conjunction_index/discovery/formal_features.py | 3ae3fd9abb4e63124120c936f4b3805e7bcda9e95194497b2fe25b7e5e8623ba |
| software/v5/conjunction_index/discovery/authenticated_index.py | 6c5ba1e563f26353b5d42da07558cb53a1a680e6258acc506291333bd3f17a20 |
| software/v5/conjunction_index/discovery/discovery_store.py | c62f357d64ab52959e8d732d89dd8b92d434313a95cdec128f096235bb2c80c4 |
| software/v5/conjunction_index/discovery/module_export_adapter.py | d1e8a437dec4ebe218ab1cc74e8e4bddd91ab4ade77f60e42dac9decb0d2c658 |
| software/v5/conjunction_index/client/workspace_evidence.py | 233562c663c3633e126b6761d10542e48be9145edba8b3fb731a8eafbf9c2baa |
| software/v5/conjunction_index/client/workspace_atomic.py | eea95a6bb12349e5fc7b1e80bc610710ccafc7cbbfd2b40d705d80cdc67c8022 |
| software/v5/conjunction_index/client/direct_contacts.py | 88ce2581a7432421e2619c57ad0645f29f66d400f94c5d12db8c74c5f3d78e51 |
| software/v5/conjunction_index/controls.py | 29ad07944c7468aad3994cde8daf890137115ccf026b38d57491c33b4da2b57b |
| research/cycles/v5-2026-10-20/Select-ConjunctionIndex.ps1 | f749eee1ec0994653fb65706b19484f23923fa5b01ce55354f90bed6fc8afff0 |

The selector requires the exact previous selection
`64be70eb04b7c885fd4ffee485b06b5599b7f682a6244878e856ca92fe95d03c`,
retains its 117 source pins and 19 runtime pins, and adds exactly these eight
source/control files. It checks reviewed hashes and creates a fresh selection
only; it does not run product code. Selected bounds are 60 CPU seconds/90 wall
seconds, 512 MiB and 2 processes. Root must separately launch and adopt the saved
outcome; an independent reviewer other than the controls author should audit it.
