# Compact public integration: source-only design

2026-10-06. Requested by root after selecting the compact application and
maintained-overlay gates. This is a packaging/API design, not a new source cut,
release qualification, publication, license selection or runtime authorization.
Root owns final implementation, exact inventory and public integration files.

## The user-facing unit

Deliver an ordinary relocatable **Windows local commons node** with two explicit
roles: maintained discovery/custody and local mathematical application/checking.
These cooperate through immutable fragment directories. Neither a discovered
provider nor successful transport is a mathematical acceptance credential.
An optional separately provisioned sealer reduces repeated downstream proof
work; it is not a required central server or secretly bundled authoring runtime.

The useful public loop should be visible in one guide:

```text
owner chooses local work
  -> query bounded provider hints -> fetch bounded exact candidate
  -> apply/check under local adopted policy -> retained checked fragment
  -> offer exact fragment -> independently useful to another local agent
                            \-> optional exact seal handoff
```

No task marketplace, global root goal, global ledger, mathematical intention
model or attribution machinery is introduced. Formal target statements belong
to local proof operations; they do not impose a centrally intended question.

## One compact distribution, explicit optional capabilities

Suggested relative layout (names are prospective, not existing deliverables):

```text
commons-v4/
  RELEASE-MANIFEST.json
  START-HERE.md
  operator/                 # adopted launch/provisioning/API guide
  receiver/                 # exact604-asset compact install + profile
  overlay/                  # exact Node adapter + patched pinned dependencies
  codec/                    # exact frozen11-file inert fragment bridge codec
  runtime/node/             # selected Node executable + required notices
  notices/                  # preserved third-party licensing, vendor deltas
```

Do not put helper bookkeeping inside `receiver/`: its exact action-projection
census refuses unknown files. Keep state/config/evidence outside immutable
payload roots. Manifest paths are relative to the release root; generated
owner configs intentionally use absolute local paths and bind their exact bytes.
On relocation, regenerate fresh unadopted configs; do not edit configs already
adopted by a live state or pretend existing identities/stores migrated safely.

The file-only compact receiver has604 assets /98,920,744 bytes plus its1,881,884-
byte profile. Root's maintained-overlay exact launch selection lists Node at
92,279,112 bytes,5,872 dependency files /37,397,328 bytes,11 frozen codec files /
255,983 bytes and9 overlay source files /137,938 bytes. These are prospective
input-map counts, not a final independent package census. Their combined payload
estimate is about230.9 million bytes including the receiver profile, before
operator files/notices. Python is already in the receiver and should not be
copied a second time. No2.35GB full Lean authoring tree is required for these two
roles. Archive size is not estimated by assuming a compression ratio.

Dependency discipline: retain the exact installed/patched dependency map,
`package-lock.json`, original vendor deltas and notices. Do not run `npm install`
or download dependencies during ordinary node startup. Bundling Node itself
requires preserving applicable third-party notices and verifying its selected
runtime identity. Project licensing remains undecided; do not label the source
open-source or externally publish it because dependencies have licenses.

Do not symlink the old full installation, use machine-specific absolute payload
references, or quietly make the compact artifact depend on the retired workspace.
A separately supplied developer/sealer profile may remain an optional external
capability without copying it into this release.

## Public API surfaces and exact trust boundaries

| Surface | Input/output | Authority |
|---|---|---|
| Provision | Fresh bridge/overlay state, owner-selected listen/bootstrap and quotas | Config and identity creation only |
| Maintained node | Persistent owner stdio; `providers`, `find`, `acquire`, `offer`, `publish`, `withdraw`, `status`, `join`, `maintain`, `stop` | Inert candidate hints/custody only |
| Check | Exact selected fragment; fresh bounded operation | Full local final checking under adopted image/foundation; not transferable certificate |
| Apply | Exact plan, independent target capsule, selected context; fresh bounded operation | Same final checked relation, explicit-term route with no native authoring check |
| Optional seal | Exact fragment manifest/interface and separate adopted full profile | Source-free preparation is only READY; actual completed receipt and fresh verification are separate |

The current owner `node.mjs --create` creates overlay state/identity but calls
bridge **status**, not bridge init. Therefore the provisioning helper/guide must
first run the pinned bridge's one-request `init`, then start the node with
`--create`. Existing restart runs neither init nor create. A starter recipe that
simply launches `node.mjs --create` against empty directories is inoperable.

Owner stdin requests are single-line exact JSON envelopes:

```json
{"id":"query-1","request":{"operation":"providers","key":"type:EXACT_HASH"}}
```

Keep the process stdin open across interactions; owner EOF means shutdown.
Use returned provider/offer objects unchanged after validating their schema,
identity, namespace and bounds. `acquire` returns an absolute retained custody
directory to pass into the checker/application. All successful network results
remain `UNVERIFIED_CANDIDATE`. A service wrapper must not rewrite that label to
verified after seeing a successful stream, identity signature or content hash.

An exact package-bound public launcher should pin Node/Python and selected
payloads before launching, impose whole-process CPU/memory/lifetime/output bounds,
and preserve child/descendant closure evidence. Owner stdio is an interactive
local API, not remotely callable administration. The launch path should not
accept arbitrary executable strings or pass-through shell fragments. Nodes
need finite owner-renewed operating leases or an equivalent explicit local
supervisor policy, not the experiment's fixed11:00UTC deadline as a product API.
Operator budget renewal changes local operating authority, never proof truth.
The launcher should supply an explicit environment, particularly excluding
unselected `NODE_OPTIONS`/`NODE_PATH` preload/module overrides. Python uses its
isolated/no-site flags. System executable/DLL trust is a local bootstrap
assumption, not a theorem receipt property; installing a manifest does not defend
against a hostile owner or concurrent privileged filesystem replacement.

## Bootstrap, maintenance and availability contract

The owner provides a small contact set. These are entry contacts, not a trusted
directory, fixed corpus owner or central server. Persisted routing/identity can
support restart while the original contact is offline when retained peers remain
reachable; it cannot recover a graph with no reachable contact or remembered
address. Separate routing hints, custody retention and mathematical truth:

- A provider lease expires when renewal stops; this withdraws a discovery hint.
- Custody can remain available by direct contact after its hint expires.
- Formal validity does not expire with the advertisement.
- Automatic re-advertisement does not create additional mathematical knowledge.

The prospective maintained successor adds atomic durable publish intent so stale
queued renewal cannot recreate a withdrawn local hint. Preserve this selected
dependency in the eventual manifest; the earlier overlay is held, not its drop-in
equivalent. Already-sent remote advertisements can arrive late: TTL expiry after
withdrawal is conditional on delivery delay, not an instantaneous global erase.

Public IPv4 configuration exists in source, but current runtime qualification is
same-host loopback. NAT traversal, IPv6, hostile-network eclipse/Sybil defenses,
multiple independent physical hosts and long-lived public capacity remain outside
observed evidence. Do not brand an experimental reachable-address mode as tested
global deployment. Explain how an owner supplies contacts/announced addresses;
do not default to a public central bootstrap run by the project.

## Application/check/seal policy guide

Pin image, foundation, registry and profile separately from networking config.
Formal definitions are the supported exact transparent F-closed capsules;
arbitrary mutually recursive/compositional libraries remain a broader limit.
Rank/interface/frontier binding is not inferred from theorem names or popularity.
Every locally checked unsealed fragment still includes its bounded explicit proof
body and genuine certified frontier. Recursive certification removes ancestral
proof replay only across **actually completed adopted receipt boundaries**.

The compact product's current `prepare-seal` action still requires the **full**
installation projection even though its proof preparation is source-free.
Consequently local sealing is not a supported compact role. Offer an exact
sealing handoff record and optional external full-profile invocation, documenting
this implementation boundary rather than invoking an impossible local command.
A later separately selected source change could safely narrow that action closure;
the used application source must not be edited in place to make packaging easier.

The sealing handoff identifies the fragment manifest hash, exact interface,
image/foundation/profile, required output binding and operator budget. It is not
a transferred 'passed' assertion. On return, validate the genuine receipt against
the expected relation locally. Network acquisition currently transports proof
fragments, not a separately established arbitrary certified-bundle service;
do not promise direct seal-bundle discovery unless that path is implemented.
Once a bundle is acquired through an authorized channel, existing `--parent`
application can build a new fragment using it. Broader receipt distribution and
rollover should be specified as their actual supported routes, not implied by
the generic phrase 'blockchain-like'.

## Cost guide: account for what remains

Separate install bytes, working disk, measured CPU, wall latency, booked budget,
network bytes and maintenance. The compact payload is not the whole node's disk
requirement: custody, failed quarantine/transfer reservations, metadata/SQLite
overhead, operation snapshots and evidence need their own finite allocations.
Failed work remains charged and retained; errors may mean a mutation committed.
Do not automatically retry after `REFUSED_OR_COMMIT_UNCERTAIN`.

Current mathematical workflow reserves600 controller seconds in its operation
budget before any work and up to300 for each next short worker. That reserve is
not actual CPU consumption. Show the selected public-run1200 bookkeeping example
under the separate strict120actual-CPU outer limit as two different quantities.
Treat improved small-operation budgeting as a prospective operational fix,
not as a reason to bypass accounting or report a60-second setting as working.

Source-free application eliminates source elaboration/export and unreachable
native-file validation for that route. It does not eliminate plan creation,
search, failed candidates, fragment proof substitution, parent receipt checking,
final guest work or result retention. A fixed template's setup may amortize,
but no universal speedup or exponentially growing useful corpus follows from
that arithmetic alone. Tie every numerical claim to exact observed sources,
profiles, inputs and boundaries, and mark theoretical assumptions separately.

## Smallest nonduplicative public integration qualification

After independent actual mathematical/network outcomes, create one compact
package with a complete selected-file/origin map. Verify one fresh extraction.
Use one fresh public provisioning/start/owner-status/stop sequence to qualify
the owner API and exact launcher; the existing five-node lifecycle already tests
network mechanisms and should not be needlessly repeated. Use the already planned
fresh positive-fragment receiving check from that relocated public installation,
if it has not yet been consumed, so package relocation and mathematical handoff
share one meaningful run. Do not silently rerun an already completed receiving
operation to make a release narrative look cleaner.

Read the source/map/result evidence independently, retain all failures, and
publish only scoped support claims. These release-assembly steps are necessary
for operability but cannot substitute for the two central advances: a scalable
trustworthy reuse boundary and a concretely justified useful-growth mechanism.
