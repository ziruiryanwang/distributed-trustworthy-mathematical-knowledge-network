# Selected private controller and actual location integration

New source-only selection after frozen location-node-controls01. Root owns
launches. The failed fixture and used adapter source remain unchanged;02 is
only the remaining-six-control continuation, not a production modification.

## Two clocks, one deadline

The Python controller owns WorkflowBudget and invokes begin_route/descriptor
itself, immediately saving the issued ticket and its owner-monotonic expiry.
It does not accept arbitrary serialized tickets or channel-identity claims
from a caller. Immediately before pipe dispatch it refreshes remaining time
against that saved expiry and the single original outer deadline. Every work
await, including lock acquisition, is bounded by that deadline. A separate fixed
six-second total teardown allowance only reaps the already-owned child and joins
startup; it never performs another command. Runtime posthash is synchronous
accounted supervisor work inside the original parent Job, not renewed agent
capacity. The Node duration is only a local
cancellation aid, never authority to extend Python's deadline after transit.
The descriptor's Python `until` is not comparable with performance.now; IPC
omits it, and the Node entry supplies an unused zero sentinel required by the
frozen adapter's exact field interface. Python retains the real private expiry.

An operation either consumes its private ticket through accept_route/descriptor
or abandons it conservatively. A malformed local reply, closed pipe, timeout,
cancelled task, refused command or unknown child outcome cannot refund capacity.
Acceptance errors after `_take` already settle the ticket; do not call abandon
twice. Exactly one later SearchClient comes from the same WorkflowBudget.

## Privately adopted local transport, not JSON authority

The controller creates and owns the actual child stdin/stdout pipes. It pins
the Node executable, retained release manifest, all overlay files/vendor patches
and exact new source before launch, and rechecks afterward. The child receives
only owner-selected local paths and a fixed command map. Node imports are
confined to builtins, the selected overlay and exact snapshotted source. No
remote response can choose a package, executable, path or launch arguments.

Pipe frames have a four-byte body length, canonical JSON, finite body size,
aggregate bytes, frame count and service lifetime. One command is pending at
a time, with exact increasing sequence and response binding. The only source
of authenticated_peer is the owned adopted child after successful Noise
target-authentication, not a caller-provided JSON document. It still conveys
only an advisory endpoint referral; mathematical admission remains separate.
Python's reply-byte counter covers bytes consumed by complete reads or retained
EOF partials, not unread/timeout-buffered OS pipe arrivals. The adopted child
also limits written frames/bytes, and the external Job remains required. The
counter is not misrepresented as complete OS-pipe bandwidth accounting.

The new `composition.mjs` wraps the retained TCP factory so each caller signal
is combined with the service controller signal before the actual dial method.
The frozen outer TransportBudget still charges the attempt first. Its overflow
aborts that service controller, which now directly cancels pending `_connect`
calls even before raw connections are available for byte-meter attachment.
No new allowance or changed byte gate is introduced. This narrow successor
must be reviewed/controlled before actual networking.

## One new loopback scenario, not another broad campaign

Use one retained read-only compact index copy and its existing old-policy
metadata namespace. Do not rebuild or mislabel it as current-policy receipt
evidence. The owner explicitly configures two loopback DHT services and the
provider's actual index endpoint. The consumer gets only query features,
namespace, finite budgets and the provider's bootstrap peer multiaddress.
No index HTTP endpoint, SnapshotID or candidate is injected into its search
client. The provider advertises one selected route; consumer locates a provider,
obtains a real Noise descriptor, adopts its endpoint through the original
WorkflowBudget, then makes the existing offer and positive-candidate requests.
The exact expected fusion record is an output assertion only.

Before that scenario, exchange exact Python/Node vectors for route keys and
canonical descriptor-request bytes, plus relevant IPv4 boundaries. Existing
Node fixtures alone were not executed cross-language agreement. Controls for
IPC truncation/oversize/sequence/cancellation and in-flight connect cancellation
are separate changed seams, not a rerun of the seven passing protocol controls.

Record complete service transport admissions, observed/refused raw bytes,
maintenance and startup work, private-pipe traffic, search request/header/reply
bytes, CPU/wall and terminal closure. Aggregate transport counts are not exact
packet bandwidth; a small loopback pass is not huge-network recall, public-host
deployment or mathematical receipt acceptance. Keep all limits explicit.
