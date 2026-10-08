# Operating the experimental certified mathematical commons

Operator/agent walkthrough, 2026-09-30. This describes the selected public
source interfaces; its examples were **not executed to write this guide**.
It does not authorize an experiment, provision credentials or qualify a release.

The [support report](RESULTS.md) is the authoritative capability/cost ledger;
it distinguishes adopted outcomes from source plans and open central questions.
The routed-copy transfer/check composite, public preparation, all 122 original
public production stages and one enveloped child return have scoped adopted
audits. Two fresh received-copy cold checks pass after their suppliers stop.
These commands are
interface templates, not evidence that every deployment path is qualified.
A source review or checksum is not a runtime result. Do not repeat completed
project campaigns to follow examples; original failed allocations stay failed.

The useful path is: offer a bundle; place/find its metadata; acquire exact bytes;
independently verify them; prepare an owner's new theorem using those immediate
parents; advance that same operation to completion; offer the new child for
another receiver to acquire and verify. There is no mandatory central server.

## 1. Choose the package and adopt its exact bytes

| Archive | Contents | Intended role |
|---|---|---|
| mathematical-commons-v3-base.zip | app/receiver and app/peer | Find, retain, serve and independently verify existing certified bundles |
| mathematical-commons-v3-contributor.zip | app/contributor | Optional local Lean preparation and certificate production |

The optional contributor tree is about2.35GB uncompressed; the receiver tree is
about97.27MB before peer files. These are selected input sizes, not measured
ZIP sizes or a claim that production work is cheap. Install only the base when
you do not intend to produce a new certificate. The contributor ZIP adds its
component to the same extracted layout; it must not overwrite receiver/peer
files. Obtain both archives and their BASE-FILES/CONTRIBUTOR-FILES maps from the
same independently adopted handoff. Preserve archive and extraction pins.

The selected exact profile identities are:

```text
receiver: app/receiver/profile.json
  bytes: 78882
  SHA256: 840fb95bdbca0b22b0930650f88f08b2e887cf80b387967fa5f38b0cc75fc279
  schema: DMKN_INSTALLED_CERTIFIED_VERIFIER_PROFILE_V2

contributor: app/contributor/profile.json
  bytes: 1881153
  SHA256: b559c172eae67646c0d42d9bf5f9c22f5fe51276d9d19af18f29f6e3ebe46aef
  schema: DMKN_INSTALLED_CERTIFIED_PROFILE_V3

logical profile: dmkn-experimental-certified-collection-01
image: ccaf83d7890224f08ba9cb53c2fb25163a7867fecf94aa8bc5338db69b349b19
foundation: 4eeaab61471a4ab9f93209af9aad66fcb45f6322783b919851d4d95ea33f9f80
```

Those digests identify the selected original profile bytes; adopt them from the
trusted handoff, not a peer advertisement or this document alone. Do not edit a
profile to make a mismatch disappear, normalize JSON or change resource limits.
Its asset map and roles select the checker, registry, runtime and foundation.
Public receiver/contributor calls rebind the complete required installation.
An experimental guest certificate is not native-node Lean admission, universal
Lean/checker equivalence, production recursive-security assurance or usefulness.

Use an ordinary fixed-NTFS Windows installation with the selected Python3.14
runtime. Source-level index codecs are portable; other serving platforms are
not qualified here. Keep immutable app trees separate from writable state,
operation files, owner Lean source and private credentials. No PEM/private key,
database, experiment, proof checkpoint or owner configuration belongs in a ZIP.
No concurrent local writer may mutate adopted code, inputs or operation state.
These are cooperative ownership assumptions, not a hostile-source/OS sandbox.

## 2. Set explicit local paths

Examples below use PowerShell. The paths are illustrative, not project output
locations or already-created directories. Substitute your own absolute ordinary
paths. Angle-bracket values elsewhere are placeholders, not commands to run
verbatim. Create writable parent directories deliberately before their use;
each init/prepare/verify target itself must be fresh when required.

```powershell
$mcV3Root = 'C:\MathCommonsV3'
$mcOpsRoot = 'C:\MathCommonsOps'
$mcReceiver = Join-Path $mcV3Root 'app\receiver'
$mcPeer = Join-Path $mcV3Root 'app\peer'
$mcPython = Join-Path $mcReceiver 'runtime\python\python.exe'
$mcReceiverPin = '840fb95bdbca0b22b0930650f88f08b2e887cf80b387967fa5f38b0cc75fc279'
$mcContributorPin = 'b559c172eae67646c0d42d9bf5f9c22f5fe51276d9d19af18f29f6e3ebe46aef'
$mcPeerConfig = Join-Path $mcOpsRoot 'peer.json'
```

After adopting the handoff's archive pins, extract the base ZIP into a fresh
installation root. If needed, extract the matching contributor ZIP into that
same layout without overwriting existing files. Compare the extracted relative
paths, lengths and SHA256s with the adopted portable file maps before use;
profile identity alone does not prove that all shipped assets match.

The peer API accepts an independently adopted Python using `-I -S -B`, without
`-O`; the bundled receiver runtime is a source-level choice for these examples.
Public contributor calls specifically require its own installed Python. When
configuring an external supervisor, limit its child PATH to the adopted
component's bin/Python/DLLs plus System32; do not depend on an unrelated host
installation as fallback. The public contributor selects its worker environment.
Use the supplied finite peer launcher for peer/routing operations. The public
receiver and contributor already provide their documented Controllers and
finite worker Jobs; ordinary cooperative use does not require you to implement
another supervisor. An optional outer supervisor can impose a shared multi-call
budget or stronger parent-process containment. These sampled/cooperative
controls are not a hostile-source sandbox. Save stdout, stderr, exit code,
configuration pins and resource costs for each call.

### Supplied peer-command supervisor

For peer/routing calls, the separately pinned `peer_run.py` linked on
[START-HERE](START-HERE.md) supplies that finite process-tree envelope; users
do not have to implement it themselves. Its
[exact plan template](../../product-local/certified-v3-operator-tools-01/PEER-RUN.md)
includes relocated base/manifest/profile paths, config tokens, a fresh evidence
run and explicit limits. Adopt that helper independently, keep its directory
outside app/state/input/credential domains, and invoke it using the base's
shipped receiver Python:

```powershell
& $mcPython -I -S -B '<absolute-peer_run.py>' --plan '<absolute-plan.json>' --plan-sha256 '<independently-adopted-plan-sha256>'
```

Put the peer/route script's argument tokens from subsequent examples in the
plan's `argv`, starting with `--config`, and select its `entry`. Do not include
Python, its flags, the script path, `&`, or a shell command string in `argv`.

The subsequent direct peer commands show the inner API syntax. For bounded
operation, run them through the supplied envelope or an equivalent deliberately
adopted external supervisor. The public launcher handles only peer/routing
commands, not contributor or cold verification. Run `cert_workflow.py` and
`cert_verify.py` directly with their adopted profiles: they already supervise
their workers and enforce their documented operation checks. Decide deliberately
whether a stronger combined sequence/parent-process bound is needed; it is not
a missing prerequisite for the ordinary cooperative workflow.

The helper's source-only guide label records its frozen authoring checkpoint.
An independently adopted actual nine-group test and one shipped client-only
init qualify the initial narrow launcher path. The adopted actual child return
adds ten selected public-envelope TLS/serving commands, not fresh identity
provisioning or independent hosting. Require consistent saved evidence, matching final stderr
`public-peer-envelope-controller-final` PASS/exit0 and actual process exit0;
saved RESULT or stdout alone is preliminary. The helper rebinds about97.5MB
of adopted code at startup/closure, not the theorem corpus, so its real cost
must be accounted for rather than described as free.

## 3. Create one local peer configuration

Write a UTF-8 JSON file outside immutable app trees with exactly these fields.
This client-only example starts with no known supplier and no listener:

```json
{
  "schema": "DMKN_CERT_PEER_CONFIG_V1",
  "state": "C:\\MathCommonsOps\\node-state",
  "policy": {
    "profile_id": "dmkn-experimental-certified-collection-01",
    "image_words": [3615731660, 4028891785, 1405856139, 371588034, 4268193850, 2343212239, 3062707141, 429601947],
    "foundation": "4eeaab61471a4ab9f93209af9aad66fcb45f6322783b919851d4d95ea33f9f80",
    "registry_sha256": "63bb37cc7b51bb77dcbae152a0cba1b82ae7925d6ca0822327d3470adb5729e1"
  },
  "contacts": {},
  "listener": null,
  "protected_roots": [
    "C:\\MathCommonsV3\\app\\peer",
    "C:\\MathCommonsV3\\app\\receiver",
    "C:\\MathCommonsOps",
    "C:\\MathCommonsProtected"
  ]
}
```

The eight words are the selected image bytes decoded as little-endian u32s;
they are not an alternate image. All four protected directories must exist.
They exclude TLS identity storage; store private identity files outside all
four. A contributor installation, when present, should be protected too: the
first protected root may instead be the whole immutable `C:\MathCommonsV3`
tree, with three other deliberate existing roots. The exact field is always
four roots, not a list you may extend arbitrarily.

For known-contact retrieval, put an owner-authorized alias in `contacts`:

```text
supplier: {profile:"pinned-tls13-v1", host:"<literal-canonical-IPv4>",
           port:<integer>, certificate_sha256:"<independently-adopted-DER-SHA256>"}
```

Use JSON syntax, not the shorthand above. At most16 aliases are supported. No
DNS, URL, redirect or remote-selected trust policy is accepted. Obtain the
endpoint pin through your deliberate operator channel; TLS identity continuity
does not prove that the operator is independent or the offered mathematics valid.

Neither the base nor contributor ZIP supplies TLS identity provisioning or
private credentials. Client-only initialization, retrieval and cold verification
need no private TLS identity; retrieving from a supplier still requires its
deliberately adopted public endpoint/DER pin. Serving is a separate prerequisite:
the operator must provision its own certificate and matching unencrypted PEM
private key in one ordinary fixed-NTFS, non-reparse directory outside all four
protected roots (and not an ancestor of any). Independently record each exact
file's path, byte length and SHA256, plus the certificate's **DER** SHA256; a
PEM-file digest is not the DER pin. Keep private files under restricted owner
control and out of packages, peer messages and diagnostic exports.

A separately supplied optional aid is the frozen
[New-OwnerTlsIdentity.ps1](<E:/Distributed Trustworthy Mathematical Knowledge Network/product-local/operator-source-05/New-OwnerTlsIdentity.ps1>)
(15570 bytes, SHA256 `78d6315b3744202a8cf901f8bccf19348285bb434de377d5ea926bf9aef14a92`).
Only the identity-provisioning guidance in
[TLS-WALKTHROUGH.md section2](<E:/Distributed Trustworthy Mathematical Knowledge Network/product-local/operator-source-05/TLS-WALKTHROUGH.md>)
(19297 bytes, SHA256 `a267eaee84ac2bb93b69ad14b34aa81c6f674b8aef406e2793d113142c8bcfa0`)
is relevant here. The helper's `Install,State,Scratch,LeanRuntime` parameters are
four exclusion paths, not runtime/profile selectors: for v3 use the actual four
protected roots. Its X509 certificate/unencrypted PKCS8 PEM output matches the
v3 listener's file-format/path checks at source level. It requires PowerShell7
with the used .NET PEM APIs; not every PS7 build is asserted compatible. Its
receipt supplies the DER pin, not the complete v3 listener file-reference pins.
The older assisted same-host qualification does **not** qualify fresh-v3
provisioning/configuration/server startup. Do not use that walkthrough's native
build, Lean runtime, `manage.py`, node configuration or grant workflow as v3.
This optional reference selects no preview, `-Create` or provisioning execution.

After meeting that prerequisite, replace `listener:null` with the owner's exact
`profile,bind_host,port,certificate,private_key,certificate_sha256` fields.
`certificate` and `private_key` are only local `{path,bytes,sha256}` references
to operator-controlled credential files, not credential contents. This guide
contains no real credential paths or keys and selects no provisioning step.
Do not send private listener configuration to peers or put it in the handoff.

After reviewing your own exact config, record its digest. Hashing establishes
file identity, not independent authority for policy values copied from a peer.

```powershell
$mcPeerConfigPin = (Get-FileHash -LiteralPath $mcPeerConfig -Algorithm SHA256).Hash.ToLowerInvariant()
& $mcPython -I -S -B "$mcPeer\cert_peer.py" --config $mcPeerConfig --config-sha256 $mcPeerConfigPin init
if ($LASTEXITCODE -ne 0) { throw 'Peer init refused; preserve output and partial state.' }
```

Expected structural status: `EMPTY_CERTIFIED_SHARD_CREATED`. Source03 uses a
fresh `terminal-shape-v1` namespace. Old discovery stores are refused; there is
no silent migration/backfill. Re-offer only deliberately selected old bundles
into a fresh shard, accounting for that new work.

## 4. Offer, find and acquire through a known contact

A bundle contains exactly `bundle.json,capsule.json,journal.bin,receipt.bin`.
It carries a selected type interface and full collection journal, not source
proofs or proof ancestry. Do not add a README or verification log to its directory.

```powershell
& $mcPython -I -S -B "$mcPeer\cert_peer.py" --config $mcPeerConfig --config-sha256 $mcPeerConfigPin offer --bundle '<absolute-four-file-bundle>' --kind publication
& $mcPython -I -S -B "$mcPeer\cert_peer.py" --config $mcPeerConfig --config-sha256 $mcPeerConfigPin find --key '<typed-key>' --limit 4 --max-scanned 32 --max-bytes 32768 --timeout-ms 250
& $mcPython -I -S -B "$mcPeer\cert_peer.py" --config $mcPeerConfig --config-sha256 $mcPeerConfigPin peer-find --peer supplier --key '<typed-key>' --limit 4 --max-scanned 32 --max-bytes 32768 --timeout-ms 250
```

Check each exit before the next call. `publication` means owner offering intent;
`custody` means retaining selected received bytes. Neither means verified proof.
Typed keys are `bundle:`, `interface:`, `type:`, `constant:` and `shape1:` plus
their exact64-hex values. A bounded partial result is not proof of absence.
Shape/type keys are discovery aids, not mathematical acceptance identities.

Save one selected complete object from `peer-find`'s `remotes` array into a
caller-owned JSON file, not the full reply or a row index. Preserve its exact
holder-bound namespace/key/offer fields; this record is inert untrusted metadata.

```powershell
& $mcPython -I -S -B "$mcPeer\cert_peer.py" --config $mcPeerConfig --config-sha256 $mcPeerConfigPin peer-acquire --peer supplier --remote '<absolute-selected-remote.json>'
```

Successful structural intake returns `ACQUIRED_UNVERIFIED` and an owned
`bundle_directory`; every offer/search/acquisition result remains
`receipt_verified:false`. Quarantine, exact advertised-byte and rederived-key
checks precede custody. Failed transfers retain charged quarantine data. A
commit exception does not universally establish no custody; a bounded exact
lookup can determine visibility. When an origin deadline is supplied, the
distinct `ACQUIRED_UNVERIFIED_DEADLINE_OVERRUN` reports visible-but-late custody,
not successful in-budget completion. Never delete retained immutable evidence
to hide a deadline overrun.

A listener can serve the local shard with an explicit finite lifetime:

```powershell
& $mcPython -I -S -B "$mcPeer\cert_peer.py" --config $mcPeerConfig --config-sha256 $mcPeerConfigPin serve --max-requests 32 --max-bytes 134217728 --wall-seconds 240 --cpu-seconds 60
```

Readiness is a separate JSON line; it is not mathematical verification. This
foreground command serves synchronously until its finite boundary. Do not use
extra readiness probe connections in a fixed-request experiment. A background
launcher, when deliberately used, should be hidden, owned and supervised.

## 5. Optional routed announce and initially unknown holder

Known contacts and routed hints are distinct. Routing additionally adopts an
exact separate configuration with these fields:

```json
{
  "schema": "DMKN_CERT_ROUTING_CONFIG_V1",
  "ads_state": "C:\\MathCommonsOps\\node-ads",
  "self_endpoint": null,
  "neighbors": [],
  "entries": [{"profile":"pinned-tls13-v1","host":"127.0.0.1","port":38471,"certificate_sha256":"<adopted-64-hex-entry-pin>"}],
  "endpoint_policy": {"enabled":true,"cidrs":["127.0.0.1/32"],"ports":[[38471,38479]],"allow_non_global":true},
  "index_role": false
}
```

The pin placeholder must be replaced; the example is not runnable as written.
It is a client-only loopback policy, not a selected deployment or all-node roster.
Referral following defaults off unless explicitly enabled. Admit only the
literal IPv4 CIDRs/ports you deliberately choose; special/private/loopback
addresses also require `allow_non_global:true`. At most2 entries are permitted.

An index/service owner instead supplies its own `self_endpoint`, generic
`neighbors` and `index_role:true` when serving an ad index. A publisher needs its
own serving endpoint too, with the same certificate pin/port as its base listener.
Neighbors are generic contacts, never a key-to-holder table. Reusing a
certificate at another port does not make a new routing identity; conflicting
pins for one socket address refuse. No automatic repair/rebalance is implemented.

```powershell
$mcRouteConfig = Join-Path $mcOpsRoot 'route.json'
$mcRouteConfigPin = (Get-FileHash -LiteralPath $mcRouteConfig -Algorithm SHA256).Hash.ToLowerInvariant()
```

Use the following command prefix for every routed action:

```text
<python> -I -S -B <peer>/cert_route.py
  --config <peer.json> --config-sha256 <adopted-peer-config-digest>
  --routing-config <route.json> --routing-config-sha256 <adopted-route-config-digest>
  <action-and-arguments>
```

For an index owner, `route-init` creates only its separate fresh inert ad store;
the base peer store must already exist. `route-serve --max-requests 32
--max-bytes 134217728 --max-request-bytes 1048576 --wall-seconds 240
--cpu-seconds 60` runs the finite service. A client-only C needs no `route-init`.

After H offers one local bundle and runs its bundle service, H publishes a
deliberately selected exact key:

```text
<routed-prefix> route-announce --bundle-id <offered-id> --key <derived-typed-key>
  --lease-seconds 600 --max-rpcs 32 --max-neighbors 24 --max-finds 4 --max-scanned 128

<routed-prefix> route-discover --key <same-typed-key>
<routed-prefix> route-discover-acquire --key <same-typed-key> --row 0
```

`route-announce` rederives the key from the selected local bundle. It sends an
inert descriptor, then spends a separately reserved find on the **same** ledger
to confirm exact offer/holder placement. A provisional `committed:false` response
alone is not placement. `ANNOUNCEMENTS_VISIBLE` means observed confirming local
replica claims for each selected key, not all replicas, proof of custody or
guaranteed future availability. The fresh receiver can learn H from a returned
ad without H in its initial contacts. `route-discover-acquire` preserves one
ledger across discovery and its one selected acquisition; two separate CLI
invocations are two declared operations, not a secretly renewable allowance.

Default bounds include32 attempted RPCs,24 neighbor calls,4 ad-finds,4 announced
keys,4 returned distinct bundles,2 explicit API acquisition attempts,128 reserved
scanned rows,1MiB metadata plaintext and128MiB selected frames. Metadata8s and
whole60s are shared absolute parent deadlines. Flags may lower caps only; failed
attempts are charged, never refunded by remote claims. Routing is serial, at
most64 candidate identities,8 referrals/reply and3 discovered index replicas;
referrals must be strictly closer. Only unsplit-v1/partition0 is supported.

Ads are unverified cooperative hints with leases60..3600s. `route-expire`
explicitly removes at most64 expired rows; lookup does not secretly sweep them.
Hot keys, missing replica intersection, stale ads, unreachable holders, spam and
eclipsing can produce `PLACEMENT_INCOMPLETE` or `ROUTING_INCOMPLETE`. Those are
honest incomplete outcomes, not global theorem absence. Default64MiB page and
descriptor caps exclude extra SQLite journals/memory; they are not a64MiB
whole-directory guarantee. This admission policy is not production internet
security or permissionless/Sybil-resistant availability.

## 6. Independently verify the acquired bundle

Do this before mathematical reliance. Use your locally adopted receiver and
fresh operation path, not a verifier/profile selected by the received bundle.

```powershell
& "$mcReceiver\runtime\python\python.exe" -B -E -s -S "$mcReceiver\cert_verify.py" --profile "$mcReceiver\profile.json" --profile-sha256 $mcReceiverPin --bundle '<owned-acquired-bundle-directory>' --run '<fresh-verification-operation>'
if ($LASTEXITCODE -ne 0) { throw 'Receipt verification did not pass; preserve all evidence.' }
```

Require `PASS_EXPERIMENTAL_COLD_CERTIFICATE_VERIFIED_NOT_NATIVE_ADMISSION`,
`receipt_verified:true`, exact bundle/profile/image/foundation/member binding,
one actual driver call, unchanged input snapshots, empty cleanup errors and a
closed quiescent Job. Preserve RESULT, inputs and logs. An imported JSON success
record, sender assertion, nonempty receipt file or a network status is not this
verification. The peer index deliberately has no mark_verified API.

## 7. Optional contributor: prepare once, continue only clean READY

This part requires the independently adopted optional contributor profile and
an explicit finite production choice. One real acquired-parent child has now
completed all 122 stages, actual discharge and final cold verification through
the public interface. No proof-production or useful-growth speedup follows. Proof
production can cost far more than native checking. Assess affordability before
starting; a profile ceiling is not a prediction that your theorem will finish.

Only owner-controlled Lean source belongs here; Lean source is executable local
code, not safe hostile peer content. Use a supported fixed-foundation Prop
theorem, not new definitions. Choose0..8 immediate selected-member parent bundles
that the exported proof actually uses. Received parents still undergo the
contributor's real checks even if you separately verified them earlier. Members
sharing one exact full journal/receipt are verified as one group; no parent
ancestor proof bodies, sibling capsules or transitive history are required.

```text
<contributor>/runtime/python/python.exe -I -S -B <contributor>/cert_workflow.py prepare
  --profile <contributor>/profile.json --profile-sha256 <adopted-contributor-profile-digest>
  --run <fresh-operation> --source <absolute-owner-source.lean>
  --root-name <fully-qualified-theorem-name> --parent <selected-acquired-bundle-directory>
  --cpu-budget-seconds <explicit-total-CPU-allowance> --deadline-utc <fixed-future-UTC-deadline>
```

Repeat `--parent` only for deliberately selected distinct interfaces; omit it
without parents. Source is at most65536 bytes. The installed profile caps total
operation CPU at120000s and initially allows a deadline at most86400s ahead;
choose stricter actual limits as appropriate. The path's parent directory must
exist; the operation must not. App/input/operation trees must not overlap.

Preparation verifies parents, imports only their body-free types, elaborates and
cleanly rechecks the owner's theorem, exports the child and captures one coherent
execution snapshot. This is a conditional native result and saved execution,
not a child certificate. Do not prepare again to continue that operation.

For a concrete read-only example, the already prepared
[OwnerChild.lean](../../experiments/certified-collection-01/OwnerChild.lean)
uses the acquired parent's exact name `BatchProbe.left_inverse_injective`
twice to prove `CollectionProbe.left_inverse_composition_injective`.
The importer makes that selected declaration's formal name, universes and
type available in the owner's source environment; the owner need not invent
an axiom or copy the parent's proof. `--parent` selects the exact acquired
four-file bundle, while `--root-name` selects the new owner theorem. This is
an explanation of the retained example, not a new workload to rerun or a
general-mathlib interface. READY still does not authorize offering a child
certificate: complete advance and actual verification remain necessary.

Exit0 with `PASS_PREPARED_OR_BOUNDED_PREFIX_NOT_CERTIFIED` means bounded progress.
Read the matching append-only `records/<index>.closed.json`: only `status:READY`
can continue. Use the same profile/digest/run and retain the original source,
parent snapshots, CPU allowance and deadline; an advance cannot replace them.

```text
<contributor>/runtime/python/python.exe -I -S -B <contributor>/cert_workflow.py advance
  --profile <same-profile> --profile-sha256 <same-adopted-digest>
  --run <same-operation> --max-new-stages <chosen-integer-1..393>
```

Advance performs at most that many new stages. It may return another clean READY
prefix when a full next-stage CPU/wall reservation does not fit. This does not
renew capacity. Each invocation conservatively precharges its entire controller
allowance; inclusive worker costs and prior failed charges remain retained.
Do not automatically loop, increase a budget, extend a deadline, edit records,
remove an unmatched intent, transplant checkpoints or recreate an old operation.
`FAILED_NOT_RESUMABLE`, a failed closed state, unmatched intent, ambiguous closure
or changed pin refuses continuation. Preserve such failures for diagnosis.

Require `PASS_EXPERIMENTAL_CERTIFICATE_BUNDLE_NOT_NATIVE_ADMISSION` plus matching
closed `COMPLETE` state, complete stages/assumption discharge, actual final cold
verification, unchanged installation/operation pins and clean invocation closure.
Only then is `<operation>/bundle` the final four-file contribution. A READY stage
receipt or directory called bundle is not completion. A valid final certificate
may exist after a later bookkeeping failure, but that does not make the failed
contributor invocation pass. Another receiver must check any offered bytes afresh.

## 8. Return the completed child to another participant

Offer the final exact four-file child using `offer --bundle <operation>/bundle
--kind publication`; serve it under an explicitly finite owner listener. Place
one derived key through public route-announce when using routing. Another node
finds/acquires the child and runs its own separate cold receiver operation.
That return is not complete merely because the producer's advance passed.

A second holder may offer exact received bytes as `custody` and serve them without
inventing another theorem. Original-producer loss still requires a reachable
retaining holder/ad intersection; there is no universal availability promise.
Preserve transfer/receipt/member pins, failures and complete costs. Do not send
owner source, intermediate proofs, operation records or parent history as part
of the four-file child transport.

For agents, search ranking, choosing useful investigations and deciding when to
publish remain your local strategy. Discovery, receipt acceptance, availability
and usefulness are different results. This guide does not establish natural
large-network convergence, complete cheap recall, independent-host deployment,
production cryptographic assurance, licensing/public release or exponential
useful growth. The support report states which central gates actually passed.

## Authoritative public references

[Selected peer/routing API](<E:/Distributed Trustworthy Mathematical Knowledge Network/product-local/certified-routed-peer-source-03/CERTIFIED-NETWORK-API.md>)
and [selected contributor04 API](<E:/Distributed Trustworthy Mathematical Knowledge Network/product-local/certified-collection-contributor-source-04/CONTRIBUTOR-API.md>)
specify exact fields, supported limits and result meanings. These are source
references, not replacements for the final handoff's adopted evidence.
