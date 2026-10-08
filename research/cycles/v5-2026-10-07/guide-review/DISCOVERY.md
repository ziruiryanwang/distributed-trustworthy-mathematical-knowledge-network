# Candidate v5 guide review: discovery, custody and reciprocal use

Documentation-only checkpoint, 2026-10-08. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
All source paths below are relative to that root. This note interprets existing
source and retained checkpoints; it launches no tests, proof, network service or
implementation. Current pause status and runtime claims come from
`research/NOW.md` and `research/cycles/v5-2026-10-07/PAUSE-HANDOFF.md`, not a new
observation of the background process. Root owns the final user-facing guide.

## Central picture

The candidate is a **federation of selectively held, content-addressed,
proof-certified mathematical libraries**, not one globally replicated ledger.
A local agent chooses its own research. The commons provides discoverable formal
interfaces, authenticated data and a mathematical admission boundary. Human
intentions, a global list of open problems, political attribution and a universal
usefulness score are not inputs to mathematical acceptance.

An owner can combine or separate four roles:

| Role | Holds or does | What it does not establish |
| --- | --- | --- |
| Local researcher/consumer | Chooses a query, checks selected imports, authors and certifies new work | No entitlement to unlimited computation or universal discovery |
| Index provider | Builds and serves committed formal-feature snapshots | No mathematical authority, global completeness or custody promise |
| Custodian | Retains selected module interfaces, computational bodies and/or receipt bytes | A stored byte string is not a verified theorem or perpetual availability lease |
| Location service | Advertises and finds possible service contacts through a maintained DHT | An advertisement is not a correct index, held object or mathematical certificate |

Different parties can serve the same immutable snapshot or exact object. A
particular server is not indispensable, but at least one suitable reachable
provider is indispensable for a network operation. No reachable contact means
local-only work or an explicit unavailable result, not magical discovery.

Implemented reader mode prohibits index publication and descriptor serving, but
still listens and participates in DHT routing with `clientMode:false`. It is
**not yet a lightweight, no-service client role**. See
`software/v5/location/maintained_roles.mjs` and
`research/cycles/v5-2026-10-07/DISCOVERY-INTEGRATION.md`, "Adopted controller result
and selected explicit role successor".

## Objects and identities: do not collapse them

| Name | Meaning and use |
| --- | --- |
| `ModuleID` | Commitment to the module summary and its exported declaration groups under a foundation and semantic policy |
| `ExportID` | Exact `(ModuleID, structured relative Lean name)` address; identifies one declaration, not an entire custody blob |
| Group opening | Module summary, group index, complete group and Merkle path; binds a declaration/inductive package to a module |
| Body hash | Commitment to selected computational content needed for unfolding or reduction |
| `ReceiptSHA256` | Digest of exact receipt bytes; junk also has a digest, so this alone establishes no theorem |
| `WireProfileID` | Public certificate-encoding/image/foundation/policy compatibility; distinct from a machine-local adopted verifier configuration |
| `RecordID` | Commitment to one index metadata claim, including locator and formal features |
| `SnapshotID` | Commitment to one provider-selected immutable index cut; not the latest global state |
| Rendezvous key | Domain-separated hash of formal namespace, index role, selected feature conjunction and stripe; locates hints |

Multiple compatible receipts can certify one ModuleID. No global canonical proof
or consensus election is required. Exact byte/name commitments also are not a
universal semantic deduplicator: two isomorphic theories or equivalent statements
can retain different identities.

The formal-feature namespace binds the module format, foundation, semantic
policy, feature schema and partition profile. Old-policy search evidence cannot
be silently relabeled as current-policy certified knowledge. This matters in the
actual evidence: the successful network-location demonstration used retained
old-policy metadata; the currently prepared receipt/module flow has a different
policy and requires its own derived export/index records.

Sources: `software/v5/modules/codec.py`,
`software/v5/discovery/module_export_adapter.py`,
`software/v5/custody/receipt_store.py`,
`software/v5/transport/RECEIPT-ACQUISITION-PLAN.md`.

## End-to-end path

```text
agent chooses a formal query and finite owner allocation
    -> locate possible index providers
    -> obtain a provider-selected snapshot offer
    -> authenticate positive candidates or scanned intervals
    -> acquire an exact export opening and required bodies
    -> acquire exact compatible receipt bytes
    -> genuinely verify the receipt and obtain a live local import handle
    -> reconstruct selected semantic interfaces and author new Lean work
    -> prepare and certify the new module using real parent receipts
    -> retain new material, index exports and advertise selected serving scopes
    -> another agent repeats the receive/use/contribute cycle
```

This is the **intended assembled path**, not a claim that the current complete
path has been executed and qualified. The component/evidence boundary is below.

### Query and location

The agent creates one namespace-specific conjunction of one to eight formal
features. Current exported-declaration features include declaration kind, exact
declared-type key, symbols and imported modules occurring in a type, binder-domain
heads, result head and syntactic parent/child edges. Extraction is deterministic,
bounded and based on the selected declaration type. It does not fetch imported
proof ancestry. One index record describes **one declaration**; taking the union
of a module's unrelated exports would produce spurious conjunctive matches.

Example: an agent working with a tree fold can search for a theorem declaration
whose type mentions selected fold/map exports. This can find an unknown theorem
ExportID; it does not eliminate the need to select a compatible vocabulary or to
interpret whether the returned statement is useful. Query selection belongs to
the agent. No human-language-to-formal translation service is mandatory here.
Current features are syntactic fingerprints, not complete semantic matching.

An owner preselects bootstrap contacts, egress policy and a finite supported route
vocabulary. A bounded Kademlia operation finds provider PeerIDs. A short
Noise-authenticated descriptor exchange supplies advisory HTTPS contacts. The
same original workflow accepts those contacts and creates **one** SearchSession;
it does not create a fresh budget per provider or failed route.

Channel identity comes from the adopted local Noise transport, not a JSON field.
The HTTPS operator need not be the same entity as the Noise peer. TLS uses owner/
system CA trust. Remote descriptors cannot supply CA files, scripts, credentials,
arbitrary schemes or redirects. Public mode currently selects numeric public
IPv4 and owner-listed ports; loopback is a separate explicit test policy. Learned
DHT addresses and HTTP endpoints are checked before each dial. General NAT,
relay, IPv6 and independently hosted public qualification remain separate work.

Sources: `software/v5/discovery/module_export_adapter.py`,
`software/v5/location/protocol.py`, `workflow.py`, `protocol.mjs`,
`maintained_roles.mjs`, `transport.mjs`, `controller_services.py`, and
`software/v5/transport/located_receipts.py`.

### Offer and search

The client initially need not know a SnapshotID. It requests an offer using the
namespace, conjunction and byte bounds. The provider chooses one retained cut;
the client recomputes its identity and authenticates the summary. An offer's
owner-clock expiry limits reuse of the contact/hint. It does **not** certify that
the underlying snapshot is new or complete.

Within each of 256 ExportID-prefix partitions, the query planner chooses the
least-populated committed feature posting as an anchor. There are two deliberately
different query modes:

| Mode | Verification claim | Tradeoff |
| --- | --- | --- |
| Ordinary page | Every ordinal in a specific contiguous anchor interval is included and the returned filtering result matches those records | Transmits nonmatching anchor records too; can accumulate authenticated interval coverage |
| Positive candidates | Each returned record is a committed positive match in the selected snapshot | Avoids transmitting nonmatches; skips and continuation are advisory, with no authenticated scan coverage |

Neither mode establishes correctness of remote feature extraction or mathematical
validity. The client later recomputes the exact feature record from acquired
content. Deduplication uses `(ExportID, RecordID)`, not ExportID alone. A malicious
first provider's bad metadata claim must not suppress a different honest claim
for the same object; alternatives remain visible and consume finite capacity.

Search returns explicit exhaustion/refusal/incompleteness. A zero-hit response,
`NO_OFFER`, an exhausted provider or even a fully scanned committed snapshot
does not prove that the theorem does not exist elsewhere.

Sources: `software/v5/transport/SEARCH-API.md`,
`software/v5/discovery/search_session.py`, `discovery_query.py`,
`candidate_query.py`, `summary_wire.py`, and `software/v5/transport/clients.py`.

### Acquire, retain and verify

The candidate locator identifies `(ModuleID, group index, relative name)` plus a
descriptor binding. Acquisition verifies the group's Merkle opening, selects the
exact declaration, reconstructs the exact export wrapper and recomputes all
features. This establishes **authenticated structural content**, not truth.

If use demands a transparent definition or recursor reduction body, fetch the
body committed by that exact descriptor. Imported theorem proof bodies are not
required by this interface path. The next mathematical gate obtains a compatible
receipt offer, retrieves exactly its declared bytes and checks its raw digest.
The locally adopted verifier then decodes and verifies the receipt, exact image,
foundation, policy, module journal and resolved-assumption requirements. Only its
successful actual verification can issue a private revocable live handle.

`ModuleStore` retains groups/selected bodies; `ReceiptStore` retains opaque bytes
and unverified associations. Saved flags cannot mint handles. A cold process must
reverify the retained receipt and authenticate selected openings/bodies. The
stores have separate transactions: failure can leave partial custody, never a
successful atomic whole-workflow claim. Content-authenticating readback is part
of the custody-ready boundary, and late checks revoke any newly issued handles.

Important present limitation: the integrated located workflow tries custody at
adopted index contacts, without asserting those endpoints have custody roles.
Missing roles consume/refuse the attempt. Generic discovery of an unknown,
independent module/receipt custodian is **not implemented by index rendezvous**.
Separately owner-configured custodians remain usable through lower-level APIs.

Sources: `software/v5/custody/module_store.py`, `receipt_store.py`,
`software/v5/transport/http_provider_receipts.py`, `receipt_client.py`,
`located_receipts.py`, `software/v5/admission/verifier.py`.

### Reuse and contribution

Use the same actual originating verifier in `ImportSession`. The handle, exact
receipt, namespace and selected group/body data remain bound to that live session.
Source preparation requests missing data as typed demands (`NeedVerifiedModule`,
`NeedDeclaration`, `NeedBody`). Acquiring data changes selection; recreate the
source operation instead of silently rebinding an already prepared operation.

The frontend reconstructs the selected semantic context. Imported theorem and
opaque interfaces are authoring-only assumptions with exact types; transparent
definitions and inductive reduction require authenticated computational content.
They are not newly trusted axioms in the child checker. The resulting new-module
request is still untrusted and the independently adopted relation checks it
against exact genuine parent receipts. Only the new checked/certified module
belongs on the mathematical acceptance side of the boundary.

The owner can then retain its new openings, necessary bodies and receipt; index
individual exports; and advertise selected service predicates. DHT `publish`
means **advertise a service hint**, not certify or globally publish a theorem.
Index admission similarly computes metadata, not mathematical acceptance. Current
components do not implement a single globally atomic "publish knowledge"
transaction. A crash between custody, index update and advertisement can leave
accepted-but-unindexed or indexed-but-currently-unavailable material; reconciliation
and accountable retention are release obligations, not silently atomic actions.

Closing the located workflow revokes its verifier handles. Finish verified import
selection/authoring while that verifier remains live. A resulting child prover
input may be retained as untrusted data because the later producer independently
checks parent receipts; a serialized handle is never sufficient.

Sources: `software/v5/authoring/API.md`, `imports.py`, `context.py`, `source.py`,
`acquisition.py`, `module_dependency.py`, `software/v5/preparation/API.md`,
`software/v5/production/API.md`, `software/v5/location/intent.mjs`.

## Exact meaning of index coverage

Four propositions must be separated:

1. A declaration is mathematically warranted under an adopted relation.
2. A record's features equal extraction from its exact committed declaration.
3. A page contains every record in a specified committed anchor interval.
4. A named corpus was completely and truthfully indexed.

Merkle checks establish proposition 3, or membership alone in candidate mode,
assuming the hash commitment is binding. Acquired-content recomputation addresses
2 for returned records. Actual certificate verification addresses 1. No present
remote build proof establishes 4. Therefore complete interval coverage implies
complete answers for a selected source corpus **only if** every relevant source
object was correctly inserted, its features are truthful, and each feature's
posting list contains exactly the appropriate records. It says nothing about
unknown peers or the whole world.

Proof of the conditional page claim: any conjunctive match contains the chosen
anchor feature and belongs to exactly one prefix partition. If every ordinal of
that partition's anchor list was authenticated and checked, that match cannot be
skipped within the correctly built index. An omitted source object or omitted
posting violates the build premise, not the Merkle proof. Candidate mode does
not authenticate all ordinals and cannot use this argument.

This is reflected in `Coverage.report()`: `global_complete=false`,
`mathematical_acceptance=false`, `build_assurance=NOT_PROVIDED`. It is especially
important in an open network: there is no globally authoritative membership list,
global latest root or universally available view during partitions. A blockchain
would order selected admissions but would not make unknown mathematics, honest
feature extraction or available replicas appear automatically.

## Huge-network efficiency: the justified claim and its conditions

### Local indexing and search

Let `M` be locally indexed declarations, `f` their average indexed feature count,
`d` query conjuncts, `C` bounded anchor records examined and `k` returned hits.
The index uses local SQLite B-trees and content-addressed Merkle structures.
Rough candidate data-path cost is `O(C*d*log M)` indexed lookup work plus hit
record/proof construction; positive wire cost follows the `k` returned records
and their paths rather than all `C` nonmatches. These are model terms, not a
claim to bound all interpreter/SQLite/decoder CPU by that expression.

Worst-case intersections remain linear: two frequent disjoint features can
force an honest server to inspect a large anchor to find no match. A fixed
256-way hash partition changes packaging/local work allocation, not total
worst-case work or unlimited scaling. Nor are these 256 partitions a complete
network ownership/sharding mechanism. The current local store caps, refusal
behavior and finite owner-selected index scopes must not be represented as an
automatic worldwide load-balancing system.

Two implemented optimizations have narrower, real purposes:

- Compressed physical sparse-map paths preserve exact logical commitments and
  expanded proofs. One retained comparator reduced SQLite bytes by91.73028%,
  preserving19 snapshots,421 expanded proofs and selected summary/pages. This
  is a finite storage result, not a matched CPU or global-growth theorem.
- Compact summary encoding omits derivable defaults and reconstructs the same
  verified summary under a separate expansion cap. It reduces sparse metadata
  wire cost, not dense worst cases or provider dishonesty.

Immutable retained snapshots support portable continuation against any provider
holding the exact cut. They also consume storage. Current stores refuse quota
exhaustion; indefinite-history garbage collection, snapshot leases and scalable
snapshot-specific replication remain unfinished.

### Location and selective coverage

Expected logarithmic Kademlia route depth is conditional on a well-connected,
well-maintained, sufficiently balanced overlay and a suitable membership/fault
model. The implementation supplies finite event/time/result/resource refusal,
not an adversarial-routing or universal-recall theorem.

Even ideal sampling exposes the unavoidable coverage issue. If `P` providers
advertise a route, `r` are currently useful and `B<=P` are drawn uniformly without
replacement, success probability is

`1 - choose(P-r,B)/choose(P,B) <= min(1, B*r/P)`.

Thus fixed `B` with one relevant provider does not give network-size-independent
recall. Actual retained Kademlia does not promise uniform sampling. Arbitrarily
biased/eclipsed hint selection can give zero success despite honest providers.

A defensible sufficient operating premise is that, conditional on every previous
all-failure history, the next funded attempt succeeds with probability at least
`p>0`. Then `B` attempts succeed with probability at least `1-(1-p)^B` by
multiplying conditional failure bounds. Independence is one sufficient special
case; an observed unconditional average is not enough. "Success" here must
include useful serving scope/reachability, not merely returning a PeerID.

Selective features, selected conjunction advertisements and replicated useful
scopes can improve this `p`; none are free or presently universal. Owners choose
a finite supported vocabulary rather than all subsets of128 features. Unsupported
demands receive no positive lower-bound coverage. Stripes0..255 can spread some
hot-key demand but neither create unlimited capacity nor prevent identity
grinding, Sybil saturation or correlated failures.

### Resource composition and sustainable service

Every investigation has one original deadline and finite allocations for routes,
events, descriptors, contacts, offers, snapshots, scanned allowances, candidates,
requests, bytes and verification. The composed wrapper prepays the earlier
location/search suballocation before acquisition; phase changes do not mint
resources. Unknown transport outcomes conservatively keep their reserved caps.
Candidate replies charge whole reserved scan allowances, not untrusted reports
of "zero work". Duplicate/failed attempts still cost capacity.

The counters are deliberately different units: DHT events are not wire bytes;
observed/admitted raw transport bytes exclude packet/kernel overhead; HTTP
headers/request bodies are additional to response-body bytes. CPU, memory and
whole-process containment require the external supervisor. These mechanisms
bound exposure but do not guarantee useful service under a hostile flood.

For provider `i`, a sustainable maintained route set needs, at minimum,

`sum_j maintenance_work(i,j)/renewal_period(i,j) < maintenance_capacity(i)`

with explicit slack for churn/repair, and analogous offered-work < service-capacity
conditions for index queries, custody and admission. A rough routing renewal
term is proportional to `advertised_keys * routing_replication * log N / period`
under the favorable DHT model. Queue stability by itself is not a worst-case
latency bound. Replica growth reduces read pressure only by paying more storage,
write and renewal work. All such costs belong in the growth comparison.

Sources: `software/v5/transport/SEARCH-API.md`,
`software/v5/location/ADAPTER-PLAN.md`, `CONTROLLER-PLAN.md`,
`research/cycles/v5-2026-10-07/DISCOVERY-INTEGRATION.md`, particularly "What
scalability claim is actually supportable" and "Sustainable selective coverage
is a capacity condition"; prior `research/cycles/v4-2026-10-06-resumed/SCALING-CONTRACT.md`.

## Availability, maintenance and repair

Correctness and availability are separate. A correct unavailable declaration
remains correct; it cannot currently assist an agent lacking its necessary data.
No finite mechanism promises availability through arbitrary network partitions,
loss of every replica, unfunded retention or sustained overload.

Implemented local mechanisms include bounded persistent group/body/receipt
custody, authenticated readback, retained index cuts, maintained provider hints,
finite reprovide/TTL configuration, and durable publication intent. Withdrawal
removes local intent and prevents a queued local renewal from resurrecting it.
Remote hints can remain until expiry. This repairs/maintains **hints**, not lost
mathematical content.

Supplier-independent use requires retaining the exact receipt plus the selected
group openings and every computational body that the intended use needs. A later
new unfolding demand can still require another fetch. A cold user rechecks the
succinct receipt rather than downloading every ancestor proof, but must retain
or recover semantic content and an adopted verifier/runtime.

Still-open global service obligations include:

- Finding a compatible independent custodian when the index provider lacks or
  loses content; current index rendezvous does not advertise arbitrary custody.
- Explicit desired replica counts, independent failure domains, availability
  probes, repair selection and funding, and bounded repair under churn.
- Snapshot-specific replication/retention and garbage collection without falsely
  promising old cursor availability.
- Crash/restart reconciliation across separately committed custody, index and
  hint state; visible distinction between held, indexed, advertised, reachable
  and mathematically admitted.
- Fair admission under hot keys/hostile load, interoperable public roles and
  independently hosted deployment/accessibility.

These are central V5-A/V5-O obligations, not peripheral attribution mechanisms.
Existing v4 provider-loss demonstrations are retained evidence of their own
interfaces; they do not automatically prove all candidate-v5 service paths.

## Actual status versus intended architecture

| Area | Existing evidence/implementation | Remaining claim boundary |
| --- | --- | --- |
| Formal per-export index | Feature extraction, authenticated snapshots, ordinary coverage, candidate mode and finite-store/query controls implemented; compressed storage/summary improvements measured in bounded cases | No remote honest-build/corpus completeness proof, universal semantics or huge-scale recall qualification |
| Maintained provider location | Actual location02: empty search contact map -> bootstrap -> DHT -> Noise descriptor -> unknown-SID offer -> exact candidate, clean closure | Same-host loopback and old-policy metadata only; no current-policy mathematical admission or independent public hosting |
| Receipt transfer and custody | Eight focused synthetic controls, binary framing/digest/quota failures, selected cold readbacks after supplier shutdown | No positive mathematical receipt/handle in those controls; generic custodian discovery and repair remain open |
| Common workflow | LocatedReceiptWorkflow implemented; original-deadline, prepayment, contact expiry and candidate-binding controls pass within documented mocked scope | Genuine current-profile location-to-certificate integration remains open |
| Ordinary imported Lean authoring | Native frontend built/linked; five conditional native controls pass, including substantive Tree/fold/map use and targeted refusals without imported theorem proofs | Conditional context is not a genuinely received receipt/session-to-certified-child endpoint |
| Worker and preparation |20 mock worker controls and9 mock preparation controls independently pass at pause | Actual worker/native integration and full child certification are not implied |
| Base production | One original finite operation was permitted to continue in background at handoff | This documentation pass does not inspect it or claim a terminal receipt; terminal audit/admission remain separately required |
| Final public v5 | Development APIs and source components exist | No completed v5 release, fresh reproducible supported installer, full public workflow, deployment/repair qualification or license selection |

Status authority: `research/NOW.md`,
`research/cycles/v5-2026-10-07/PAUSE-HANDOFF.md`, `ASSURANCE.md`, `PLAN.md`, and
the actual outcome sections of `DISCOVERY-INTEGRATION.md`. Early headings such
as "source-only" in older design documents are historical; later implemented
source/outcome sections supersede them only within their stated scope.

## Guide-writing conclusions for root

The most useful explanation is a ladder of guarantees, not a list of components:
**reachable hint -> authenticated metadata -> authenticated semantic content ->
verified mathematical module -> genuinely checked new contribution**. Explain
exactly which cost and failure each rung removes, and what it does not promise.

The credible huge-network thesis is selective locality: no reader stores the
whole commons or replays transitive theorem proofs; it performs bounded search,
receives a selected certified interface and demanded semantic context, and pays
for new work. The unresolved thesis is how consistently useful relevant scopes
remain reachable and maintained at favorable full cost. Conditional selective-
coverage and capacity arguments are available; a globally implemented repair/
custodian-discovery/publish-operability story is not yet complete.

Do not label isolated positive metadata, synthetic refusal tests or an eventual
base certificate as the whole reciprocal-growth loop. Equally, do not discard
the actual implemented mechanisms: they substantially improve the architecture,
and the precise remaining endpoint is now concrete. Root's guide should state
the intended composition, its actual component evidence, and the deployment
obligations side by side, then honor the user's requested pause.

## Focused assembled-guide review

Reviewed the full `notes/V5-ARCHITECTURE-GUIDE.md`, observed SHA256
`07c0e9980b592f3640fea238f751863ca90dc62f304bb0dac28632b1c8d1a859`,
including the initially truncated middle sections through a separate source
read. Documentation-only: no runtime, background-process audit, tests, product
edit or Git mutation. Root owns any guide corrections; this review appends only
to the assigned checkpoint.

### Assessment

The guide correctly distinguishes mathematical acceptance, metadata membership,
feature truth, interval coverage, availability and usefulness. Positive candidates
do not gain scan coverage. Provider work claims do not refund unbounded budgets.
The no-proof-ancestry cost argument includes interfaces, demanded bodies, actual
verification attempts and new checking work, and explicitly rejects uniform
cheapness for arbitrary mathematics. Tree expansion and the unimplemented delta/
semantic-DAG proposals are identified as such. Section16 and the worked-cycle
wording prevent component successes from becoming an end-to-end v5 claim.

The undergraduate-facing progression is coherent: objects first, certificate
trust next, then reuse, discovery, service and growth. Definitions of Merkle
openings, universes and live handles are appropriate. No new broad restructuring
or additional mechanism is warranted by this review.

Root already intends to clarify index-only rendezvous, no generic independent
custodian lookup/repair/GC, and the current non-lightweight reader role. Those
edits remain necessary; the source-only specification of a role must not be
mistaken for actual deployment capability.

### Additional corrections sent to root

**Make the worked query genuinely constructible without the target ID.**
Section11 step3 says B knows relevant formal symbols/shapes but not A's new module
ID. Current `ModuleExportAdapter` hashes exact ExportIDs for nonfoundation
type-symbol features. Knowing a new library's display name `fold` or `Tree` does
not determine such a key without its owning ModuleID. Specify either:

- a generic initial query, such as theorem declaration + foundation Eq result
  head, then bounded inspection/refinement; or
- a new law over symbols of an already known shared base module, with those
  exact symbol ExportIDs known independently of the new law's ID.

The first option matches the actual retained
`software/v5/transport/FoldFusionSearchSelection.json`: theorem kind and
`result-head-foundation-name` Eq. The more selective second option is a sound
architectural example, not that old run's executed query. This clarification
prevents hidden target knowledge while remaining faithful to the intended
unknown-ID discovery capability.

**Expose the main quantitative selective-coverage condition in the scale
section.** Section12 correctly names routing/selectivity/maintenance assumptions,
but the existing project argument makes them substantially clearer. For `P`
advertised providers, `r` useful ones and `B<=P` uniformly sampled contacts without
replacement, success is `1-choose(P-r,B)/choose(P,B) <= min(1,B*r/P)`. Actual
Kademlia does not promise that uniform sampling. Fixed budgets therefore cannot
promise constant recall as the relevant fraction vanishes. The sufficient
adaptive premise—success probability at least `p` conditional on every preceding
all-failure history—yields `1-(1-p)^B`. Explicit supported scopes, credible serving
probability and offered-work below funded query/renewal/repair capacity with churn
slack are the favorable regime; a tiny loopback test establishes none of them
universally. One short paragraph/equation is enough; do not reproduce the full
technical checkpoint.

**Small precision improvement, not a new blocker:** Section10's `p^r` example is
point-in-time simultaneous unavailability under independent replica events. It
does not by itself describe permanent loss probability over a retention horizon
or resilience of the full set of required interface/body/receipt objects. Calling
it "simultaneous unavailability" and saying what horizon is modeled avoids giving
the elementary formula more operational force than it has.

With the already-planned role/custody corrections and the concrete-query
clarification, no other necessary discovery/operability claim correction was
identified. The network-scale conditional argument is an important explanatory
addition, not certification of the present system. Review complete; lane stops.
