# V4 guide draft: understanding and using the experimental pieces

Draft, not a release or installation promise. Updated 2026-10-02 12:36 UTC.
The small typed reader's exact file installation and four structural tests are
independently adopted. The two archives and their exact extraction passed the
byte-delivery audit; shipped runtime is not yet qualified. Prefix010 has 91
independently adopted completed stages out of 250; prefix011's next ten are running.
There is no completed seed certificate or
actual typed acquisition yet, and no useful-growth advantage is claimed.
See [NOW](../../NOW.md) for later decisions. Commands below target the actual
extracted distribution; they are unexecuted templates, not selected launches.

The assembled base archive is 97,817,285 bytes and contains the small receiver
plus peer/index software. The optional contributor archive is 2,349,904,469 bytes.
They are under `product-local/certified-v4-package-01`. Their maps exclude node
state, credentials and research proof checkpoints. These byte-delivery facts do
not establish runtime acceptance, independent-host operation or public licensing.

## 1. What the network exchanges

Independent agents find, check and use one another's mathematics and choose their own problems.
There is no required global task list or vote on truth.
There is also no required central server. Each owner controls its own policy, state,
contacts and serving limits; a supplier serves its own objects, not the whole network.

| Item | Meaning | Example or limit |
|---|---|---|
| Definition | An exact typed operation, including its body | `iter f n x` applies `f` repeatedly; changing the body changes its identity. |
| Proposition | A formal statement under a fixed foundation | A map preserving one step also preserves repeated steps. |
| Proof | A formal term justifying a proposition | The contributor checks the newly written proof using selected prior interfaces. |
| Certificate | Cryptographic evidence that the pinned checking program accepted particular data | Its validity depends on that program, its foundation and the cryptographic assumptions. |
| Advertisement | A searchable hint about an object and a supplier | It can be missing, stale or misleading; it supplies no mathematical authority. |

A completed bundle has exactly `bundle.json`, `capsule.json`, `journal.bin` and
`receipt.bin`: a manifest, exact semantic interface, committed public result and
certificate. A proposition capsule carries required definition bodies, but not the
proposition's original proof or the proofs of its ancestors. Definitions are checked
semantic data, not arbitrary new axioms. This first profile permits safe transparent
definitions built only from its fixed foundation F, the allowed basic constants/rules.

Proving a lemma does not enlarge the unrestricted logical consequences of F. It can
still make a result accessible and affordable to a finite agent. Practical growth means
better later mathematical work after counting production, discovery, verification,
maintenance and failures. More files or citations alone do not demonstrate that benefit.

## 2. What must be trusted, and what must be checked

Locally adopt the exact profile, foundation, checker image and source/install bindings.
A matching digest establishes byte identity; it does not establish the code's soundness.
The restricted Nanoda checking relation and its correspondence to the intended Lean
semantics remain explicit assurance assumptions, alongside the certificate machinery.
Neither foundation consistency nor support for arbitrary Lean libraries is claimed.

The receiver verifies the actual full receipt and journal before relying on a selected
proposition. Certificate recursion discharges prior assumptions and uses decreasing
dependency ranks to exclude circular justification. It avoids mandatory download and
replay of ancestral proof steps. Selected interfaces, definition bodies and any required
computation still have costs; certificate production is currently substantial work.

TLS authenticates the selected endpoint, not mathematics. Search and acquisition always
report `receipt_verified:false`. A popular supplier, an index row or a copied success
flag cannot waive local verification. Direct bounded queries cover only their stated
local view; failure to find a lemma does not establish global absence.

## 3. The local contribute–reuse loop

1. Choose a local problem and formal statement. A shorter direct proof is always allowed.
2. Search with a locally derived constant/type/partial-shape key under finite limits.
3. Save an actual returned candidate and acquire its exact four-file bundle into local custody.
4. Run contributor `prepare` on trusted local Lean source with that bundle as `--parent`.
   The contributor freshly verifies the receipt, installs the selected proposition interface
   and checked definition bodies, checks actual premise use, and records a guest snapshot.
5. Continue that same operation with finite `advance` calls. Only complete assumption
   discharge, final receipt verification and clean closure yield a new certified bundle.
6. Offer the new bundle. Another agent independently repeats discovery, acquisition and checking.

| Observed result | What it permits you to conclude |
|---|---|
| `ACQUIRED_UNVERIFIED` | Exact bytes were committed to custody; no mathematical reliance yet. |
| `PASS_PREPARED_OR_BOUNDED_PREFIX_NOT_CERTIFIED` / saved `READY` | Preparation or a bounded production prefix finished; no child certificate yet. |
| `PASS_EXPERIMENTAL_CERTIFICATE_BUNDLE_NOT_NATIVE_ADMISSION` | Final experimental certificate and bundle completed with fresh verification; not arbitrary native-node admission. |
| `FAILED_NOT_RESUMABLE` | Preserve the failure and cost; do not silently retry or promote its state. |

## 4. Current command surfaces

### One extraction, independent roles

The base ZIP supplies `app/receiver` and `app/peer`; the optional contributor ZIP
adds `app/contributor` under the same extraction root. These are roles, not three
mandatory servers: an owner can read, exchange, contribute, or combine them.
The peer CLI can use the base receiver's Python; it does not require the large add-on.

These PowerShell templates use the current audited extraction. After relocation,
update `$V4Root` and review all absolute config, state, contact, listener,
protected-root and TLS paths; changed config bytes require a newly adopted digest.
Replace the example `C:\MathCommons` input/config/state paths with your own ordinary
absolute paths before use. Parent
directories must exist; new check/operation/state directories must be fresh.
Keep them and TLS credentials outside immutable `app` trees. Use the reviewed
finite process-tree supervision; these command lines are not a deployment sandbox.

The current proof runs at the origin `certified-definitions-integration-02` install,
and the reviewed transfer adapter targets `certified-typed-directory-source-07`.
Their packaged byte maps match, but that does not show execution at `app/contributor`
or `app/peer`. The extracted command forms below were checked against source argument
contracts only; runtime and relocation qualification remain open.

```powershell
$V4Root = 'E:\Distributed Trustworthy Mathematical Knowledge Network\product-local\certified-v4-package-01'
$Reader = Join-Path $V4Root 'app\receiver'
$Peer = Join-Path $V4Root 'app\peer'
$Contributor = Join-Path $V4Root 'app\contributor'
$ReaderPython = Join-Path $Reader 'runtime\python\python.exe'
$ContributorPython = Join-Path $Contributor 'runtime\python\python.exe'
$ReceiverSha = '4803d60f1498635e60a71684709b6b6388935105598ca82e5a06aa64cca00785'
$ContributorSha = 'e3a65bc792029d7fd3f028d127d54d2f8f5e3f72dd0d695003bbbd635f0b9f7c'
```

Those are the audited receiver V3 and contributor V4 **profile-file** digests,
not bundle or executable digests. First adopt the distribution and its mathematical
policy independently of a theorem supplier, then compare local profile bytes:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath "$Reader\profile.json"
Get-FileHash -Algorithm SHA256 -LiteralPath "$Contributor\profile.json" # add-on only
```

Matching hashes detect changed bytes; they do not decide which checker to trust.
The two profiles share the selected image/foundation but have different asset maps
and limits. Never replace either expected digest with whatever a peer supplies.

### Reading does not require becoming a prover

The receiver closure is 97,302,245 bytes including its profile: Python and the
cryptographic verifier, without Lean, a guest image or proof ancestry. This is
an audited size, not yet a measured new-image receipt-verification time.
See the shipped [receiver API](../../../product-local/certified-v4-package-01/app/receiver/API.md).

```powershell
$ReaderArgs = @('-I', '-S', '-B', "$Reader\cert_verify.py",
    '--profile', "$Reader\profile.json", '--profile-sha256', $ReceiverSha)
& $ReaderPython @ReaderArgs --bundle 'C:\MathCommons\custody\bundle-01' --run 'C:\MathCommons\checks\check-01'
```

The bundle and fresh check directory must not overlap each other or the reader.
A successful fresh result authenticates that exact interface under the adopted
policy; it does not install a definition into Lean or prove a new theorem.
The source-reviewed shipped-reader gate needs a real acquired seed and two exact
mismatch controls. It has not run at this checkpoint.

### Contributing a theorem

Use the add-on's [contributor API](../../../product-local/certified-v4-package-01/app/contributor/CONTRIBUTOR-API.md).
Owner Lean source is executable trusted local code, not hostile peer input.
Set a real fixed future UTC deadline. The 3000-second whole-operation CPU allowance
below is only an example, not a cost estimate or a renewed allowance per call.

```powershell
$WorkflowArgs = @('-I', '-S', '-B', "$Contributor\cert_workflow.py")
$PolicyArgs = @('--profile', "$Contributor\profile.json", '--profile-sha256', $ContributorSha)
$BudgetArgs = @('--cpu-budget-seconds', 3000, '--deadline-utc', 'YYYY-MM-DDTHH:MM:SSZ')
& $ContributorPython @WorkflowArgs prepare @PolicyArgs @BudgetArgs --run 'C:\MathCommons\operations\definition-01' --source 'C:\MathCommons\owned\Definition.lean' --root-name MyDefinition --kind definition
& $ContributorPython @WorkflowArgs prepare @PolicyArgs @BudgetArgs --run 'C:\MathCommons\operations\theorem-01' --source 'C:\MathCommons\owned\Theorem.lean' --root-name MyTheorem --kind proposition --parent 'C:\MathCommons\custody\bundle-01'
& $ContributorPython @WorkflowArgs advance @PolicyArgs --run 'C:\MathCommons\operations\theorem-01' --max-new-stages 1
```

These are separate examples, not a script to run all at once. Definition preparation
can stop at READY and supply `definition-01\child.capsule.json` as a later theorem's
optional `--local-definition` argument. READY does not certify that capsule. Omit
`--parent` for a direct proof; add `--local-definition <absolute-capsule-path>` only
when an extra canonical body is needed. Every selected premise/definition must be
used. Embedded definitions require no additional history fetch, and a bare capsule
cannot be offered as a bundle. `advance` continues the same operation for 1..393
selected new stages; its original total allowance and deadline never renew.

### Exchanging and serving bundles

Use the shipped [typed network API](../../../product-local/certified-v4-package-01/app/peer/CERTIFIED-NETWORK-API.md)
for exact config/TLS fields and local key construction. Each owner needs a separate
`DMKN_CERT_PEER_CONFIG_V1` config: state, locally adopted policy, known contacts,
an optional listener and four existing `protected_roots`. Policy binds the matching
profile ID, image words, foundation and registry hash. A serving owner must provision
its own pinned TLS certificate/key outside those roots; credentials are not shipped.
This is not automatic peer discovery or a turnkey public Internet installation.

Review the config first, then record its SHA-256 (for example with `Get-FileHash`).
`--config-sha256` pins those approved local bytes, including contacts and paths;
it is not a digest copied from a remote advertisement. Replace the placeholder:

```powershell
$PeerConfig = 'C:\MathCommons\config\owner.json'
$PeerConfigSha = 'REPLACE_WITH_REVIEWED_CONFIG_SHA256'
$LocalDiscoveryKey = 'constant:REPLACE_WITH_LOCALLY_DERIVED_64_LOWERCASE_HEX_NAME_ID'
$PeerArgs = @('-I', '-S', '-B', "$Peer\cert_peer.py",
    '--config', $PeerConfig, '--config-sha256', $PeerConfigSha)
& $ReaderPython @PeerArgs init
& $ReaderPython @PeerArgs offer --bundle 'C:\MathCommons\operations\theorem-01\bundle' --kind publication
& $ReaderPython @PeerArgs serve --max-requests 2 --max-bytes 134217728 --wall-seconds 180 --cpu-seconds 60
& $ReaderPython @PeerArgs peer-find --peer B --key $LocalDiscoveryKey --limit 2 --max-scanned 4 --max-bytes 16384 --timeout-ms 1000 --mode raw
& $ReaderPython @PeerArgs peer-acquire --peer B --remote 'C:\MathCommons\selected-remote.json'
```

Run the relevant action at its owner node, not this whole block as one sequence.
The supplier's bounded `serve` session must be live while the requester's separate
session searches/acquires; alias `B` must be an approved contact in the requester's
config. No universal server coordinates them. Initialize each fresh state once.
Offer only the actual completed bundle, not the example's READY operation.
Save one actual returned remote object from `peer-find` output as selected-remote.json;
do not invent one or pass the whole reply. Replace the key placeholder with a locally
derived structural Name ID: `constant:` requires 64 lowercase hexadecimal characters,
not a human spelling such as `Nat`. A valid key does not promise a matching result.
`shape1:` describes a bounded conclusion shape;
neither key proves applicability. Direct `type_diverse` is optional; routed diverse
search is unsupported. Acquisition remains unverified until local receipt checking.

## 5. Qualification at this draft's checkpoint

| Boundary | Evidence already adopted | Still pending or outside scope |
|---|---|---|
| Typed semantics | Targeted native checks; six real guest cases: one positive and five intended refusals | Broad Lean correspondence and arbitrary-library support |
| Distribution | Base/contributor archives and exact extracted byte maps independently audited | Shipped runtime/relocation, independent-host deployment and public licensing |
| Small reader | Exact file installation and four structural test groups independently adopted; genuine shipped gate source-reviewed | Real acquired typed receipt positive and two causal refusal controls |
| Current contributor | Fresh integration02 installation; canonical iter and plus preparation; seed and exact direct endpoint READY | Seed final certificate and authenticated endpoint parent preparation |
| Seed production | Prefix010 independently adopted: 91 of 250 completed stages | Prefix011's next ten running; remaining stages, final receipt verification and bundle |
| Directory | Eight source06 inert structural groups adopted; source07 shared-codec delta reviewed | New-image actual typed TLS exchange and mathematical reuse |
| Reciprocal path | Transfer and parent-prepare adapters source-reviewed; conditional endpoint authored | Supplier-offline acquired-parent use, child certificate and return |
| Efficiency/growth | Costs retained; failed optimization gates remain failed | Net same-endpoint advantage, sustained useful growth and huge-network production readiness |

The inherited directory supports one cooperative hot-key split with bounded views and
leases; arbitrary repeated splits, automatic membership maintenance and universal recall
are not established. Archive byte delivery is complete; shipped runtime qualification,
cross-host deployment and licensing remain open. No seed certificate or actual typed
acquisition exists at this checkpoint. This guide neither selects a run nor publishes
a release. Bundled APIs retain historical/source-time status notes; the dated table
above and NOW distinguish current evidence from those older captions.

For rationale use [CORE-MODEL](CORE-MODEL.md) and [PHILOSOPHY-OF-GROWTH](PHILOSOPHY-OF-GROWTH.md); for the next run use [reciprocal readiness](../../../experiments/certified-growth-01/RECIPROCAL-INTEGRATION-NEXT.md) and actual adopted outcomes.
Root's experiment selections govern evaluation resources, not network participants' tasks or acceptance conditions.
