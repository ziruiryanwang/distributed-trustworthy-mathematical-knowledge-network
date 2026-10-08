# V1 delivery gap: prioritize useful peer operation

2026-09-22. Independent read-only review of the delivered indexed-discovery
candidate and its actual editable source. No Python, SQL, product, Lean,
network, SSH or deployment execution was performed. The only authored artifact
is this note; earlier sources, deliveries and qualification records are unchanged.

## Decision

Continue with bounded peer discovery beyond the present 32-entry frozen catalog,
with full-workflow cost as a parallel central issue. Preserve the existing
authenticated same-port SSH deployment profile. Native direct-LAN transport,
TLS, a peer identity registry, DHT routing and more simultaneous contacts are
not prerequisites for this next implementation.

The source's hardcoded loopback restriction is a missing direct-network
capability, but it is not an absolute deployment blocker: the documented SSH
forwarding route carries the existing wire protocol between hosts without a
central server. That route is a conditional operator profile, not executed
independent-host evidence. The absent second machine does not block continued
local development. An undecided license blocks permission to publicly distribute,
not local implementation or a preserved development source package.

The distinction matters: wider discovery improves continued reciprocal use;
changing transport solely to replace an already specified tunnel would add
qualification work without resolving the current catalog and cost limits.

## Concrete source evidence

All source references below are relative to
`product-local/indexed-discovery-source-01`.

| Observed boundary | Source | Consequence |
| --- | --- | --- |
| At most two configured peers, each at literal `127.0.0.1` | `py/node.py:68-73`; `manage.py:61-70` | Two simultaneous configured routes, not a general contact mesh. This can still connect independent reciprocal participants without a required central service. |
| Client connect and HTTP Host are fixed to loopback | `py/peer_service.py:107-120` | A config-only non-loopback change would not create working remote transport. |
| Server bind, source-address and HTTP Host checks are loopback-specific | `py/peer_service.py:210-242` | Direct endpoints require reviewed client and server policy changes. |
| Hosting profile and receipt validation are also loopback-specific | `py/hosting.py:20`, `:197`; `py/service_worker.py:70-75`, `:110` | A direct network profile crosses the owner grant, worker and outcome-binding interfaces; removing one address check is insufficient. |
| Peer discovery fetches the whole catalog | `py/peer_node.py:157-165`; `py/peer_service.py:147-153` | It cannot use the new local index to retrieve an unknown remote result beyond the exposed catalog. |
| Remote selection binds the configured endpoint and exact entry | `py/peer_node.py:169-190` | Endpoint changes cannot silently reinterpret old selections; received metadata is independently rederived before visibility. Fresh mathematical admission remains separate. |
| Catalog is at most 64 KiB and 32 entries | `py/peer_wire.py:12`, `:19`, `:225-237` | Independent byte and entry bounds exist. Raising only the entry count is not a complete scaling change. |
| Exposure selects at most 32 publications and revalidates every selected package | `py/peer_node.py:285-307` | Publication work scales with whole selected packages, not just metadata page size. |
| A frozen view materializes a full bundle for every entry under a 64-MiB aggregate ceiling | `py/peer_wire.py:17`, `:364-395` | Metadata pagination alone does not remove closure-copy cost or the total view bound. Larger catalogs need an explicit retained-view resource contract. |

The exact delivered source archive is identified by SHA-256
`0f8c7d3fd853abf09fd8eecf5fa6920df948be2aae1c9bcc50cca3edb7835f74`.
Its latest native test uses two clients in one node and no network. The older
peer/custody qualifications are compositional evidence on their named cuts;
they are not newly executed network tests of every later payload.

## The few real remaining gaps

1. **Bounded discovery and continued accumulation.** The new local exact-symbol
   index reaches 8,192 local entries in its tested metadata profile, while a
   remote view remains limited to 32 entries and prebuilt closure bundles.
   Implement an explicitly bounded remote catalog snapshot with query-bound
   pages or an equally concrete selected-view mechanism. A returned page stays
   an untrusted hint. Acquisition must retain exact selected-byte bindings,
   structural rederivation and separate local Lean acceptance. Publishing or
   querying must not repeatedly scan or rebuild all retained historical state.
   Choose a finite first catalog envelope; do not claim a global index,
   complete recall, automatic peer routing or unlimited accumulation.
2. **Affordable end-to-end operation.** Metadata lookup is no longer the largest
   observed local cost. Use retained per-step receipts to select a consequential
   checking/inspection preparation optimization, then compare a fixed complete
   workflow. Preserve exact canonical identity, corruption checks and receiving
   admission. A faster synthetic query alone cannot establish affordable reuse.
3. **Independent operation and release disposition.** The supported runtime,
   source package, finite hosting and independent-consumer examples already
   exist. Actual independently operated hosts must eventually exercise the
   documented route, fresh receiving checks, return contribution and
   producer-offline supply before claiming cross-host qualification. License
   and external publication are separate owner decisions. None of these
   outstanding conditions licenses an external connection or requires halting
   meaningful local engineering.

Two contact slots and finite grants are legitimate first-release limits. They
reduce reachable suppliers and require deliberate operator continuation; they
do not logically create an indispensable coordinator. Larger contact tables
become a priority when the chosen workload demonstrates that two active routes
prevent useful operation. A finite selected library and fresh-store upgrade
policy can likewise be honest v1 boundaries.

## Smallest deployable peer profile

Retain the already documented `ssh-loopback-v1` operator arrangement in
`deliverables/2026-09-21-local-v1-candidate/TWO-HOST-PROFILE.md` and the current
finite hosting grants. Each participant runs its own installation, local state,
selected foundation and checker. Each receiving alias uses an independently
authenticated, direct SSH forward to the supplier's loopback service; no common
relay is required. Local and remote application ports must match because the
existing HTTP Host check binds the server port. SSH and operator work have costs
outside the application Jobs and must be accounted for separately.

This is the smallest deployment route because it does not require a new wire
protocol or application cryptography. The retained profile still needs real
deployment evidence; listing example SSH commands is not an observed success.
Do not configure or reuse the machine's unrelated SSH service simply because
historical inspection found it running.

Locally implement and test the consequential discovery change on separate
bounded processes, configurations and state directories, using the current
loopback route. Test multiple catalog pages, exact-key filtering, snapshot
replacement, old-selection behavior, producer-offline replica supply and
failure/expiry behavior at their respective layers. Preserve no-checker/no-native
behavior for metadata queries and inert serving. A native follow-through is
needed only for a changed acceptance-facing integration seam; it should not
repeat already qualified tiny proof controls without new coverage.

An optional future direct profile can honestly use plaintext over an explicitly
trusted private network. If chosen, restrict it to owner-configured literal
unicast addresses, fixed endpoints and finite service grants, with deliberate
non-loopback opt-in and precise no-authentication/no-confidentiality claims.
Keep peer-supplied URLs, wildcard exposure, DNS, redirects and automatic routing
outside that initial profile. Add reviewed bind/Host/config/grant/receipt
plumbing and local address-policy/failure tests in a fresh source cut. Local
socket tests and parser tests would qualify those paths only; they would not
establish multi-host administration, public Internet resilience or actual
private-network isolation. This alternative is technically defensible but is
not selected ahead of discovery by this review.

## What TLS and content verification each establish

Content hashes and local checking do not require trusting a peer's mathematical
judgment. Once a receiver deliberately selects an exact bundle identity, a
different supplier cannot substitute different bytes satisfying that identity,
conditional on hash security and correct validation. A coherent replacement
catalog can advertise different valid or invalid mathematics; receiving checks
still decide acceptance under the selected foundation.

An unauthenticated catalog and hashes received over the same connection do not
authenticate the intended supplier. An attacker can replace discovery hints,
withhold or replay entries, redirect attention, consume bounded resources and
observe requests. Local Lean checking does not provide freshness, complete
discovery, confidentiality, availability or peer attribution. IP addresses and
an HTTP Host header are routing checks, not cryptographic authentication.

TLS with correct peer verification, or the existing authenticated SSH route,
addresses route authentication and confidentiality. It does not establish
mathematical correctness, truthful metadata, complete recall or continued
availability. A trusted-network plaintext profile can be an honest bounded v1
only by stating its trusted-network premise and accepting those transport
limitations. It cannot be labeled authenticated or public-Internet ready.
Consequently native TLS/pinning is not immediately necessary for the selected
v1 path: the existing SSH profile already supplies transport authentication,
and neither profile changes the mathematical acceptance boundary.

## Cost evidence available without another experiment

The retained
`software/qualification/indexed-discovery-native-01/result.json` reports
234.609375 inclusive outer-Job CPU seconds and 269.5680225 coordinator elapsed
seconds for the 27-step regression. Disjoint outer-step CPU totals are:

| Work | CPU seconds |
| --- | ---: |
| Two source submissions | 108.156250 |
| Two receiving admissions | 41.140625 |
| Two canonical inspections | 27.187500 |
| Five `find` calls, excluding request helpers | 4.140625 |

These sums are transcribed from the retained step records, not new execution
or exclusive function timings. They do not identify a specific internal
bottleneck. Native receipt CPU is nested and must not be added again. Build,
initialization, helpers, publication and other measured steps explain the
remaining total; coordinator and unmeasured preparation/review costs are separate.

Current `py/checking.py:162-164`, `:197-207` already records package reads/bytes,
read wall time, cache hits and pipeline counts. Those measurements are a better
starting point for the next cost decision than an unsupported assumption that
Lean kernel work dominates. The earlier source-package profile is historical
and predates serialize-once integration; it must not be presented as a fresh
profile of the selected cut.

The earlier matched nontrivial target remains useful bounded evidence: both
consumers reached publication, and the peer consumer actually used its received
lemma. Its observed elapsed time was longer and operator/model work was not
fully measured. Preserve that result as practical capability, without inferring
general speedup, steady-state economics or useful growth.

## Disposition

The candidate is useful local software with real mathematical reuse evidence.
The next product work should improve bounded remote discovery and complete
workflow cost. Preserve a concrete conditional deployment recipe and honest
unexecuted host evidence; do not turn unavailable hardware, undecided licensing
or optional transport machinery into a blanket halt on the broader goal.

## Independent discovery-design review

Read the complete revised `experiments/peer-discovery-v2/DESIGN-DRAFT.md`,
SHA-256 `948d1d40dde49584ff778b4c5d08748aa05ec0ceedf01082cbb6ce3e98f93ba5`.
Disposition: suitable for the selected bounded implementation; no blocking
conceptual issue found. This is a design review, not code or execution approval.

The revised design keeps configuration/store schema 4 with fresh installation
and source/configuration pins, explicitly versions the wire as v2, and avoids
automatic downgrade. It introduces neither live database service, global
directory, new transport infrastructure nor mathematical authority for peers.
Initial discovery fetches one bounded root plus one page; continuation fetches
one pinned page. Owned snapshots/cursors and atomic visibility prevent a failed
page from advancing discovery. Exact remote/acquisition and replica-custody
bindings remain intact; no operation scans accumulated receiving history.

Review concerns were incorporated: exposure clears only its bounded per-offer
memory cache while retaining cumulative canonical-byte, time and work charges;
the unchanged native/context cache semantics stay outside this change. Supplier
publication and startup still process the complete selected view, a limitation
now explicit. A mixed synthetic/genuine fixture may qualify later-page receiving
admission without claiming its decoys are mathematics; ordinary exposure of
more than 32 genuinely published entries remains a separate capacity claim.

Implementation review should verify exact reply/work byte bounds, authority
checks across every page, early cursor/endpoint rejection, no page-zero-only
replica validation, whole-transaction rollback on page-record failure, and
service-startup costs under unchanged grants. The 256-entry ceiling is an
upper bound, not a guarantee that every real corpus fits its time/byte limits.

## Scoped implementation source review

Reviewed the fresh `product-local/peer-discovery-source-01` changes against the
indexed-discovery predecessor, with their relevant unchanged storage, checking,
wire and dispatcher boundaries. No product execution was performed. No remaining
blocking source finding was found in this reviewed cut; runtime qualification is
still required. Reviewed SHA-256 values:

| File | SHA-256 |
| --- | --- |
| `py/peer_wire.py` | `a2f53d39a8e66025c5cb5fb44e4b0e58190ce3b7a7b73d39bbca2ae8e5d8a232` |
| `py/peer_service.py` | `d47eb2c0ec2454f38e107ec10454cb3ca6639aa91d381bba30540a83a7df84a8` |
| `py/peer_node.py` | `11a9780cccb7ba00efc8029a6ba2230768f4c611050a59f035ee204c408f2f2f` |
| `py/service_worker.py` | `fec2e2e6949df9fc435c141b9738f488b1d5a6a9e4fbe39653a8bccfa239340c` |
| `make_request.py` | `7cac92a9bb2aa325a9ed5c0a2d901c8c1a71ef9b9616589ca6f3774edc247db5` |
| Unchanged `py/checking.py` | `13afa1fa31f58f273c0364b9679fd56400587f2977ea24bddd85aad9471f840b` |

Root and page validation binds counts, lengths, hashes, foundation, page index
and globally unique ordered bundle identities. Exact page routes refuse changed
snapshots. Continuation uses its owned root and does not refresh the mutable
peer root. All-page authority checks retain publication/custody distinctions;
replication retains exact selected-entry checks. Dispatcher transactions cover
snapshot, remote handles and next cursor together, with final reply-byte checks
inside that same transaction. Historical request replay precedes network work.

An early observed `wire.encode` spelling had already been corrected by root to
the existing `wire.encoded` before this reviewed cut. Full-view authentication
in the owner worker followed by a second authentication in transport is
deliberate and documented. It adds startup work and is not called a speedup.

Exposure's aggregate canonical-byte check occurs after the next bounded package
has been read. The old checker also read a package before checking aggregate
cache bytes. Thus accepted work retains the cumulative cap; rejection can still
consume one additional bounded package. The new path additionally derives that
last package's metadata before the cumulative check, subject to existing
checkpoint/process limits. Cache release does not reset metrics, deadlines,
evidence or charges, and occurs on failure too. A configured canonical-byte
limit below 64 MiB now also caps the cumulative exposure total, which is stricter
than the old fixed 64-MiB aggregate cache limit.

## Next cost candidate: one checked insertion per decoded object

Read-only aggregation of the fourteen retained
`product-local/indexed-discovery-01/scratch/calls/*/event.json` files found nine
calls with package reads: 55 reads and 70.1387639002 summed package-reader wall
seconds, inside 205.2973331000 summed dispatcher wall seconds for those calls.
These sequential-call sums are not exclusive CPU attribution and omit package
reads performed inside separately launched capture/inverse workers.

| Retained call directory | Operation | Reads | Package-read wall seconds | Dispatcher wall seconds |
| --- | --- | ---: | ---: | ---: |
| `call-01de071c09c74e13bc7300e1bab77c6a` | `index-admit-source` | 6 | 7.5113020001 | 19.7584348000 |
| `call-8142cdc25e2847669786a1a40569606c` | `index-admit-derived` | 6 | 7.6639432001 | 20.0475871000 |
| `call-0835a9cfe702459a842bd4aef0c834ba` | Source inspection; no native stage | 6 | 7.6374700001 | 13.1216912000 |
| `call-7c6c19f5d1fc41e6ab806c6d3366f796` | Derived inspection; no native stage | 6 | 7.6672199000 | 13.0079544000 |

SHA-256 of those event files, in table order:

```text
8e391c90dffa38c3dffc296cb44b57b47240835bf6ecd890c2e7bce64aa72a47
a736737493c02f0b7fb026ea9959b0ae19deec8c3d9de11e252f68558e3c9326
f1c1043f7dfae6ab06240d77bfc40f112f1cce012cb9696d2aa6d4abdb02ba3a
fc93901733a3b051b21d64e4633de1a896b7e1078338c85ac73ae6b597802267
```

The stage-1 and stage-3 receipts linked from
`software/qualification/indexed-discovery-native-01/result.json` also show
capture-worker cumulative-Job CPU increments of 8.984375 and 10.093750 seconds,
respectively. Individual Lean-command increments range from 4.531250 to 5.000000
seconds. These are differences of successive cumulative observations from the
same Job, not a second additive CPU total. Capture merges and checks inherited
packages; this makes reader work relevant to submission as well as inspection.

Concrete remaining duplicate work: in the unchanged `py/source_codec.py`,
`read_package` at lines 969-970 first computes `C.cid(tag, schema, payload)` to
compare against the advertised object ID, then calls `Store.add`, whose line
144 recomputes the same canonical encoding/hash via `C.cid_with_encoding`.
The adopted serialize-once change removed duplication inside `Store.add`; it
did not remove this reader-to-insertion duplication.

A small follow-on candidate is a checked insertion entry point: compute the
canonical encoding and CID once, compare the computed CID with the expected ID
**before** collision checks, accounting or insertion, then use the same encoding
length for the unchanged byte charge. Do not simply insert before checking the
expected ID. Do not accept caller-supplied encoded bytes or an unchecked
precomputed CID. Existing `Store.add` callers should retain their behavior.
Leave actual file reads, decoder/canonical constraints, typed-ID validation,
collision controls, foundation components, inventory, exact closure, plan
validation and `Store.get` mutation revalidation intact. No shared template,
cross-request cache or skipped receiver-native admission is proposed.

This candidate is not implemented in the discovery cut. The metrics identify
a material reader path; they do not measure the duplicated hashing slice or
predict any speedup. A later differential probe must cover complete Store/root/
plan equality, unchanged read traces and failure precedence, wrong IDs without
partial insertion, duplicate/collision behavior and mutation revalidation.
Measure selected-package and complete-operation costs against the current
serialize-once baseline under unchanged bounds before selecting integration.
