# Genuine replica custody: smallest native discriminator

2026-09-21. Source-only design by `bounded_domains_author`; no imports,
execution, allocation creation, fixture mutation or harness implementation.
Prerequisites: independently reviewed replica integration and state contracts.
This note is not authorization to run or deploy a service.

## Decision and scope

Use historically audited G02 as inert source-produced mathematical input and
the exact H01 source as a fixed engineering successor. Fresh A is a supervised
static sender fixture, **not a newly initialized/publishing mathematical node**.
Fresh B and C have separate configurations, databases, work and scratch roots
under one new immutable installation and one newly executed support build.
Their mathematical acceptance is fresh and local. B never admits G.

This is the smallest useful regression of the new custody/service code path:
A stops; B constructs and serves an exact replica; C freshly acquires, admits,
substantively uses G and exports/publishes a checked H. It does not repeat A's
already audited proof pipeline, qualify three independent installations,
establish independent-host availability, or show novel mathematics/useful growth.
The same-host trusted runtime/filesystem premises remain explicit.

## Reusable frozen inputs, never reused acceptance

Read only the exact old fixture files after authenticating their pins. Copy
their bytes into the new allocation; never run an old installation, open an
old database for mutation, restart an old service, or modify an old allocation.

The preserved G view is under
`product-local/peer-01/alpha/state/work/3daeca50176b8a36737de2b41180d13f0a2ab12a8339f57bd1aa988bbbf2acd2/peer-view`.
Textual/hash inspection for this design found:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `catalog.json` | 3,680 | `ab5f311da32b03f03e892069de93c81fee98b020429130ff2359d1c4bb57b55a` |
| `complete.json` | 245 | `b497b792e08d56eaf69d0c209aab2a4e8b30d6780559edc2355eec254b74f456` |
| G bundle in `bundles/` | 298,037 | `32ac4a51e45013550f17b9bbe79fcd453e7f2a96ea50f7f652fb36a5910c1221` |

Pin `qualification/peer-01-g02/OUTCOME.md` and
`qualification/peer-01-h01/OUTCOME.md` as historical interpretation records,
not executable authority. The frozen successor input is
`qualification/peer-01-h01/author-source.lean`, 1,465 bytes, SHA-256
`95d1ffdfff0c93a6dfaa2381c64daf940792b770a292002097960a26e54bebeb`,
root `PeerBetaStableLiftFixed`. Preserve its exact UTF-8 bytes; do not repair
source, substitute generated names, use a normalized terminal rendering, or
consult new diagnostics to adapt the workload within the allocation.

The historical G wrapper digest is
`4ecd5d059e3e5dd9bb466fb431e350aa10554d94226c10100a47d035357ece38`.
H's canonical proof previously applied G twice, first deriving
`F(F a) = F a`, then `F a = a`. The new C run must establish its own source,
canonical proof, replay/inverse replay and publication correspondence; the old
audit does not substitute for those checks. H must be distinct from G; it may
equal historical H, since this is regression rather than novelty evaluation.

## Make the representation distinction executable

Within the new bounded worker, retain an exact copy of G's old view. Produce
one separately named derivative A view by changing **only** raw manifest
presentation: prefix the original manifest JSON with one ASCII space. Preserve
every object byte and its order, all mathematical typed IDs, foundation, root,
descriptor, formal metadata and inventories. Recompute only manifest length and
digest, bundle length/digest, catalog encoding/digest and completion pin. The
new bundle is exactly 298,038 bytes. Strictly parse/authenticate the completed
derivative using the installed inert wire helpers; these grant no acceptance.
Freeze all derivative pins before the first service starts.

This finite untrusted fixture operation does not fabricate a proof, candidate,
publication, acquisition or accepting receipt. In particular, the historical
publication did not advertise this new transport representation; A is an inert
test supplier of the same canonical mathematics. Its grant says so.

B's real `peer_acquire` must retain the prefixed inbound manifest while actual
`Checker.offer` normalizes its local analysis package. Require the two manifest
byte strings and SHA-256 values to differ, while mathematical objects/root and
metadata agree. Do not count the case as discriminating if they accidentally
match. B's actual replica view and C's actual received package must reconstruct
the derivative A bundle **byte-for-byte**, not merely share a descriptor.

## New allocation and economical machinery

Reserve a fresh reviewed `replica-native-01` data/evidence pair; neither may
already exist. Select and prospectively pin the integrated product cut, the
interpreter/runtime, all accessed historical inputs, fixture transformation,
worker and outer driver. Copy only raw product/asset sources into one new
installation and build its support once. Do not copy old support binaries,
configs, databases, accepted contexts or prepared node directories.
Require the actual B/C bootstrap foundations to equal A's selected foundation;
refuse incompatibility rather than translating or silently changing policy.

The proposed outer pin roles fit the sixteen-pin ceiling: eight execution
inputs (Python, Lean, driver, worker, scenario profile, run-stage, supervisor,
domains), six historical inputs (three G view files, H source, two outcome
notes), then the exact launch file: **fifteen pins**. The launch additionally
enumerates the complete product source/asset cut, authenticated before copying
and again in the worker; those data-source pins are not mistaken for fifteen
directly loaded modules. Freeze actual paths/counts only after source review.

Reuse the reviewed `tests/scenario_profile.py` outer-sixteen containment and
the existing native-runner source-copy/pin/census pattern. A small fixed worker
needs public CLI invocation/binding, bounded readonly state snapshots and two
finite service lifecycles. Reuse reviewed helper code where its exact profile
matches; do not import an old scenario driver and invoke its workload, enlarge
production limits, reproduce an independent kernel, or add a native interrupt
hook. Canonical substantive-dependency interpretation remains an independent
outcome audit, not another large in-harness proof validator.

The static A sender may be a small mode of the same pinned worker that calls
installed `peer_service.serve` under the ordinary finite supervisor. It accepts
only the frozen A view and launch-selected port/grant. It writes a genuine
event and returns actual observations; it must not manufacture a product view
record or claim a `manage serve` authorization. B's positive and negative
services must use the actual installed `manage serve`/`service_worker` path.

## Fixed sequence: 20 invocations, four mathematical stages

No extra `info` requests are necessary: retain real public init/acquire/admit
replies and bounded readonly ledger observations after quiescence. The latter
authenticate observations, never insert/promote rows. No ordinary request is
issued while its same-node service starts with a pending active slot.

| Step | Invocation/action | Decisive observation |
| --- | --- | --- |
| 1-3 | Build; configure B; configure C | One fresh install/build; two fresh external state/scratch domains; B knows only A's port and C only B's |
| 4-5 | B init; C init | Two actual bootstrap stages; empty P1; baseline context heads |
| 6 | Start A fixture service | Actual finite supervised sender of the derivative view; no mathematical authority |
| 7-8 | B peer_find; B peer_acquire | Real transfer and structural checking, exact remote/candidate/acquisition bindings, no new head/stage/publication/view |
| gate | A service completes and is reaped | Original A Job active-zero/direct reap and command/event/response binding observed before B replica preparation begins; never restart A |
| 9 | B ordinary expose of acquired candidate | `NOT_LOCALLY_PUBLISHED`; real charged refusal, no native work |
| 10 | B replica_expose | Actual original-byte revalidation and completed exact view; one view record/terminal reply, no G admission or publication |
| fault | Save original inbound manifest; replace only its new-copy bytes with B's normalized manifest | Explicit retained representation-substitution fault; no ledger edits and no old-file writes |
| 11 | New B replica_expose request for the same acquisition | `REPLICA_RECEIVED_CHANGED`, no second view, no native work; charge retained |
| isolation | Move B's inbound and normalized package directories to fresh quarantine names | Resolve exact actual paths, reject reparse/overlap/escape, require both strictly inside this new B work tree and neither its root nor view/bootstrap paths; preserve all bytes/censuses; no delete or repair |
| 12 | Exact replay of step 10 | Original response bytes despite absent copies; no additional reservation, preparation or stage; this is historical, not a live-service claim |
| 13 | B manage serve of committed replica view | Actual checker-free ledger authorization and intact frozen bytes work despite absent source/analysis copies |
| 14-15 | C peer_find; C peer_acquire | C knows only B; real transfer of exact A-derivative bytes; unchanged C bootstrap head and no G admission yet |
| gate | B positive service completes and is reaped | Bound active-zero/reap observation precedes C's fresh admission |
| fault | Save original B bundle, flip one byte in that new view's bundle only | Retain original and fault bytes; no repair; positive C custody is already complete |
| 16 | New B manage serve of the same view | Worker `SERVICE_REFUSED` / `BUNDLE_DIGEST_MISMATCH`, wrapper refusal; no readiness/listening or successful transfer; genuine nonzero inner receipt accepted as expected negative evidence |
| 17 | C admit G | Fresh receiver-local native replay with A/B unavailable; new C context, same acquired identity |
| 18 | C submit exact H source | Actual source check/capture, candidate replay, inverse capture/replay; substantive reachable G use and distinct H |
| 19-20 | C publish H; C expose H | Actual checked portable package, publication marker and completed view; no new native stage |

The two fault writes and recoverable directory moves are prospectively declared
test-only mutations of **new owned copies**. Pin/census before and after each;
never redirect these operations through a computed old allocation path. The
positive B view is immutable until its deliberately separated post-transfer
tamper control. No failed preparation is promoted and no fault is restored.
Only the original manifest and bundle files are overwritten after preserving
their exact original bytes; their saved copies and damaged counterparts remain.

## Exact count and charge arithmetic

There are 19 installed CLIs (one build, two configure, fourteen request CLI
invocations and two B service invocations), plus one A fixture service. Of
fourteen request invocations, thirteen are new and one is exact historical
replay. Services/build/configure have their own resource grants, not hidden
ordinary requests. Source-file fault actions and readonly observations are
worker work, not additional product calls.

| Node | New requests | New stages | Request MiB | Stage MiB | Total charged MiB |
| --- | ---: | ---: | ---: | ---: | ---: |
| B: init, find, acquire, refused expose, replica, refused replica | 6 | 1 bootstrap | 8+8+64+80+80+80 = 320 | 128 | 448 |
| C: init, find, acquire, admit, submit, publish, expose | 7 | 3 | 8+8+64+8+8+8+80 = 184 | 384 | 568 |
| Total | 13 | 4 | 504 | 512 | 1,016 |

Configure exactly these finite request/stage/reservation grants (B 6/1/448 MiB;
C 7/3/568 MiB) and the existing 32-MiB metadata ceiling, subject to genuine
physical-supply checks. Mathematical pipeline children are exactly eight:
B bootstrap 1, C bootstrap 1, C admit 1, C submit 5. The separate support build
has one stage/two compilations and is not a mathematical acceptance or a node
stage charge. B's final head remains its actual bootstrap head; its only native
stage is bootstrap. C publication/exposure append no acceptance stage.

No automatic retry, grant renewal, new source attempt or fourth receiver is
part of this allocation. H's local checked export/replay and actual publication
establish the selected portable-successor boundary; fresh fourth-node H
admission is a later stronger discriminator, not silently claimed here.

## Bounds, receipts and stop rules

Use the reviewed outer profile unchanged: **450 wall seconds, 450 CPU seconds,
6,144 MiB private commit, 16 processes**, 65,536-byte outer stdout/stderr/event.
Prospective retention: **1 GiB, 16,384 files, 32,768 entries**, including new
installation, A fixtures/fault copies, B/C state/scratch and final evidence;
shared external runtime and untouched old allocations are excluded. This is
an endpoint census, not a transient disk quota. If this fixed bound proves
insufficient, the attempt fails and a later separately reviewed allocation is
needed; no live limit increase.

Both successful services get **120 seconds, two connections, 64 MiB sends**;
their service supervisors retain 150 wall seconds, 120 CPU seconds, 256 MiB
and eight processes. The tamper-start service gets the same finite grant but
must refuse before readiness. Readiness waiting is at most 30 seconds, without
HTTP probes. Pair each sender start immediately with its two receiving calls;
do not spend service time bootstrapping. Existing public peer limits remain
120 wall/CPU seconds and 1,024 MiB; native ordinary limits stay unchanged.
The enclosing Job is the aggregate authority and includes wrappers and A.

Bind actual adjacent request/command/stdout/stderr/event/supervisor files and
source pins before interpreting success. Record observed stages/children,
charges, response and quiescence **before** enforcing expected success counts;
a real source refusal may have fewer than five children. Service/nonzero
negative receipts must be accounted without being mistaken for success.
Require zero forced terminations for this non-interruption positive profile.
Use monotonic offsets from the same worker to order A-stop before B replica,
and B-stop before C admission. A stopped flag or direct wrapper exit alone is
insufficient. Bind actual tree cleanup; missing evidence remains unknown.

Measure total executed worker-tree CPU from the outer Job once; nested public,
service, support and native CPU are a stage breakdown, not additive totals.
Report coordinator CPU/copy/census endpoint separately, along with retention,
native memory peaks, send charges versus completed sends, native wall time,
metadata pages and all thirteen request charges. Do not imply executable pins
authenticate every Python/Lean runtime dependency.

On any unexpected response, fault-scope violation, missing pin/receipt, timeout,
resource bound or correspondence failure: stop the sequence without repair or
automatic recovery. Retain all charged work. Let the existing supervisor/outer
Job establish process-tree cleanup; if cleanup cannot be authenticated, stop
auditing mutable state and mark the outcome unknown. Do not launch C admission
when A/B stop evidence is unavailable. Any later attempt has fresh roots/pins.

## Independent outcome gate

Audit the integrated source cut, all actual transfer/ledger/native bindings and
exact mutation targets. Reconstruct C's inbound bundle using its recorded
manifest order and object bytes and compare it with A's derivative and B's
original served bundle. Audit full supported closure/inventories and current
foundation, not only an identity string. Verify no copied old receipt entered
either receiver's acceptance path, and all B stages/heads remain as specified.

For H, traverse its actual canonical proof from its value root and establish
both substantive applications of G, not an unused source mention, redundant
closure item or theorem alias. Bind source capture to exact H bytes, native
plans/outputs to the committed artifact, and checked package to the new public
view. Recheck accounting including expected refusals, replay and failed service.

Only then report a scoped same-host replica-custody/native-reuse PASS. No new
release-critical defect was established by this source-only design. Actual
canonical compatibility, service source-copy independence, resource feasibility
and this integration's fresh native behavior remain executable questions; any
failure is evidence, not a reason to weaken the acceptance or custody boundary.
