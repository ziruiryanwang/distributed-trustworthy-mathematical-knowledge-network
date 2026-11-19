# Ordinary location backend: independent source review

2026-10-28, growth_design_audit. **PASS for the selected backend source cut.**
The complete operator/HTTP/receiver integration remains separately reviewable;
no runtime or public deployment is qualified by this note. No source import,
compilation, database open, network operation or native experiment was performed.

Reviewed all changed backend code and relevant reused call boundaries against
`WIRE-CONTRACT.md`, SHA-256
`59e9e4257711589876c3695ea46cbcfdb9b3f97ee279e6c82212b460792aec07`.
Exact eleven source identities are recorded in `BACKEND-CHECKPOINT.md`, SHA-256
`1cc595d3af966d60a0c679f46008d4e33747a00a14cef787f466a43c3c10ae5a`.
Independently confirmed the five changed source hashes and exact equality of
all six claimed reused files to their stated retained origins. Principal pins:

| File | SHA-256 |
|---|---|
| controller.py | `b3214f30d31d086535a4d08e71957fc606229407ffda8e8cc0335105264ff58d` |
| maintained_roles.mjs | `60c90522db36a650d6ac511b5ddbfc90003b60859c7f1dfa5cb8fffbe38247b2` |
| protocol.mjs | `a3fb51fcbda838d161e6388f6179c3bdb4094aaeb162dd05be9c800f02ff9304` |
| ipc_wire.mjs | `4ffbf08417f2824ef25de0ff3b473f189ca14552661f2c8d52b98e5ac3c1741f` |
| node_entry.mjs | `37cf40221e0dbb46938a474bfe44900341fac953964fdc9d5892351ac2eaf991` |

## Publication and recovery invariant

Let P be committed `/application/published/` keys and S the process's charged
set. Before constructing libp2p or starting renewal, `_census` validates every
published key/spec, its selected SemanticID and matching intent bytes under the
opened quota store's exclusive ownership. It builds S=P, checks cardinality K,
and separately observes whether a self-provider row exists. Deadline/cancellation
checks enclose this finite census. Failure prevents background startup.

Serialized publication reserves a key in S before calling the unchanged atomic
`enableIntent`. If admission is new, the K check precedes reservation. Commit can
add only that already charged key to P. An exception cannot remove its charge.
Thus both confirmed and ambiguously reported commits preserve P subset-of S and
|S| <= K. A failed reservation/commit may leave a conservative phantom charge;
this is capacity loss, not over-advertisement or an inferred rollback.

Withdrawal calls unchanged atomic `revokeIntent` before deleting the charge.
That transaction removes intent, self-provider and published rows. Subsequent
self-provider writes require intent in the same synchronous datastore operation,
so an in-flight renewal cannot resurrect the revoked key without a later explicit
publication. Background provider maintenance does not insert published rows.
These facts preserve the invariant after confirmed withdrawal; ambiguous failure
retains S. Remote hints may remain stale and are not declared immediately revoked.

Reopen requires the exact persisted configuration hash and identity, and a new
explicit finite service grant. It repeats the census before maintenance rather
than inheriting an old in-memory count. This uses no new durable counter schema,
implicit state migration or deletion. Pending/self-provider observations remain
labelled observations, not a future-availability guarantee.

## Request, peer and lifetime boundaries

The ordinary role, hash domain and descriptor protocol are distinct from
certified-body/formal-feature roles. Request schemas are closed; route keys and
nonces are recomputed/bound. The served descriptor requires a current published
key, matching SemanticID and exactly one owner-approved endpoint. Its duration
is clipped to the provider's original local service deadline at construction.
Only the separate custodian role serves descriptors or publishes; HTTP gateway
role has no own endpoint or publication authority.

Descriptor acquisition dials the exact PeerID through retained Noise/libp2p and
reports that dial target as authenticated_peer. It does not derive identity from
reply JSON. The Python gateway must still parse and compare descriptor peer,
nonce, route and endpoint policy before returning a hint. Lifetime translation
and reader authority remain later integration obligations. The duration does not
prove custody retention, DHT provider TTL or honest upstream availability.

`known` contains at most the latest lookup's 64 peer/address entries. Consequently
the whole HTTP locate-to-descriptor sequence must be serialized, not only each
private command. This requirement is agreed and documented. Retained self-skip
also means a custodian is discovered through a different gateway; combined
local-self discovery is outside this implementation, explicitly disclosed.

## Private IPC and failure ownership

Python and Node agree on 16-KiB bodies, at most 8,192 commands plus lifecycle
frame capacity, and at most 129 MiB per direction. Smaller configured byte and
command caps stop first. Publication, withdrawal, query, descriptor, status and
stop share the sequence/grant; ordinary work reserves report/stop capacity.
Counters grow with admitted work rather than preallocating their maxima.
Controller JSON uses unescaped UTF-8 (`F.compact`), matching Node's canonical
parse; operational profile serialization is not substituted for wire bytes.

`LocationUnavailable` is restricted to BUSY, EXHAUSTED or EXPIRED before a private
command is admitted. After admission, any timeout, cancellation, malformed frame,
child error or uncertain exchange marks the channel failed. The controller owns
the process/spawn task, awaits drain, and refuses future commands. A teardown
failure becomes terminal `LocationChannelFailure` with a saved cleanup diagnostic;
it is never ordinary unavailability. Cancellation cannot restore channel reuse.
Node's narrow descriptor TCP-unavailable case excludes authentication, malformed
protocol, abort and unknown failure. Retained raw-connect cancellation and Ping
composition are preserved; this review does not replace their earlier evidence.

The Node service timer, per-operation narrowing and provider/transport caps remain
finite. Relative durations crossing the private pipe do not compare foreign
absolute clocks. Python still enforces its original local cutoff and owns teardown.
The outer launcher must supply the stated hard process containment and cleanup
allowance; cooperative synchronous source/runtime verification is not a sandbox.

## Remaining integration and decisive validation

No new architectural blocker was found in this source cut. This pass relies on
the selected retained runtime, exclusive trusted local ownership and source pins;
it is not an independent proof of libp2p, Noise, SQLite or JavaScript correctness.
Runtime verification still visits 5,896 payloads; startup visits bounded local
metadata/publications. Per-key publication no longer scans the entire published
set. No claim of constant-cost startup or globally complete discovery follows.

Complete integration must enforce approved-bundle exact locator readback before
publish; role/source closure; the whole-workflow busy guard; bounded HTTP reply
construction; request-start lifetime translation; reader metadata prepayment and
shared custodian/request caps; and unchanged mathematical admission. The root's
pure delta helper has its separate `DELTA-REVIEW.md` pass.

After those sources are settled, focused checks should exercise ambiguous versus
confirmed publication/withdrawal, over-cap/reopened census, command/byte reserve,
issued cancellation/drain and cross-language binding. One finite actual workflow
should demonstrate unknown support-holder acquisition and natural service cleanup.
None requires reproducing Lean proofs, certificates or a broad scale simulation.
