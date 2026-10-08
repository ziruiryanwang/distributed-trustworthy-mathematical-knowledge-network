# Paged candidate: supported result and limits

2026-09-22. Selected after the independent protocol, native operational and
canonical outcome reviews. This is a locally qualified source candidate, not
an externally published release or a completed global-network qualification.

## What changed

Peer discovery now uses wire/schema 2: an immutable bounded catalog root and
hash-pinned pages, with receiver-owned snapshots/cursors. A continuation reads
one pinned page rather than refreshing the mutable head. Exact replay performs
no network work. The finite ceiling is 256 entries, at most 32 per page; byte,
time and cumulative resource limits may refuse earlier. Exposed packages are
checked sequentially without retaining every per-offer checker cache. Full-view
authentication at service startup remains and is not advertised as inexpensive.

Canonical bundle framing remains 1, configuration/store schema remains 4,
native plans remain 2 and mathematical metadata remains 3. Mathematical
checking, canonical codecs, native sources and bundled assets are unchanged
from the indexed predecessor. There is no wire-v1 discovery fallback, state
migration, remote symbol filtering or global directory. Fresh installations
and fresh state are required; do not overwrite a used node.

## Evidence

| Scope | Observed outcome | Independent review |
| --- | --- | --- |
| Fifteen native-free protocol/metadata contracts | PASS; actual sockets, 65-entry paging, bounded/hostile inputs, ownership/replay and rollback | [Protocol audit](../../experiments/peer-discovery-v2/PROTOCOL-REVIEW.md) |
| Twenty-step genuine Lean receiving/contribution workflow | PASS; page-two discovery, fresh A admission, actual received-proof reuse, ordinary publication/service, fresh B admission | [Operational audit](../../experiments/peer-discovery-v2/NATIVE-REVIEW.md) |
| Mathematical linkage of the derived definition | PASS; six-binder body is the received proof applied to `C` and `g (f a)`; A/B native and canonical descriptions agree | [Canonical audit](../../experiments/peer-discovery-v2/NATIVE-CANONICAL-AUDIT.md) |

The native workflow took 233.1216589 coordinator seconds, 200.78125 inclusive
outer-Job CPU seconds, plus 26.8125 coordinator CPU seconds. Peak observed outer
Job private commit was 2,370,146,304 bytes. Retained endpoint: 892 files and
96,783,091 bytes. No retry, renewal or repair was performed; all services/jobs
were quiescent. Different prior workloads are not valid speedup baselines.

The first supplier was explicitly a fixture with 32 inert decoys and one
genuine historical package. No decoy was admitted. A's new contribution and
its A-to-B service were ordinary product operations. This is not evidence of
33 genuine publications, mathematical novelty, autonomous research or useful
growth. Discovery and acquisition remain candidate-only; fresh receiving
admission, not remote claims or hashes, supplies mathematical acceptance.

## Exact delivered identity

The archive has 112 payload files plus `SOURCE-MANIFEST.json`, 3,662,316 ZIP
bytes and 3,617,004 payload bytes. SHA-256:

- Archive: `01e141823fb3eb1a48d425586672d98a4b5ce10f69ae932d67f32cba3653dffb`.
- Manifest: `fff9c122f04eae35cc16c0b0754074d07f307c1504838147097fc7f65a3ad6d0`.

The packager's unqualified label and machine test labels are preserved: the
linked independent reviews, not rewritten machine records, supply scoped
qualification. The frozen source is `product-local/peer-discovery-source-01`;
the used installation is `product-local/peer-discovery-native-01/install`.
Neither is an editable next-development tree.

## Deployment and continuing work

Use the archive's `QUICKSTART.md`, `AGENT-QUICKSTART.md`, `API.md`, `HOSTING.md`,
`PEER.md` and `RECOVERY.md`. The supported local profile remains Windows x64 on
local NTFS, the selected Python 3.14.6/SQLite 3.50.4 and complete Lean 4.34.0
runtime. Runtime binaries are not bundled. The authenticated same-port SSH
forwarding recipe is documented, but no independent-host/SSH/Internet run has
been qualified. The loopback-only direct service is not a public Internet API.

The ZIP was frozen before these audits. Some in-archive introductions still
describe their then-current qualification as pending or call the source a
development cut. Their commands and API remain the packaged reference; this
outer `START-HERE.md` and the linked independent reviews state the subsequent
qualification. Do not interpret a pre-audit sentence as a failed test, or as
qualification of an untested deployment profile.

Earlier unchanged-core evidence is preserved in the
[indexed candidate](../2026-09-22-indexed-discovery-candidate/START-HERE.md) and
[original support statement](../2026-09-21-local-v1-candidate/RESULTS.md).
Those results do not automatically retest every changed wire path. This cut
does not add new interrupted-transfer, replica, same-port turnover, hostile
filesystem or power-loss guarantees beyond its explicit tests and unchanged
code boundaries.

The whole project goal remains active. Full-workflow cost and continued useful
operation are central remaining work; checked package insertion is currently
only a separate prototype. Large-network discovery, unlimited retention and
exponential useful accumulation are not established. Licensing is undecided;
nothing has been published externally.
