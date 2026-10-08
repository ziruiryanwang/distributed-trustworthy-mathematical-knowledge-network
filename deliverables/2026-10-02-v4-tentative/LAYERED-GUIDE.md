# V4: a layered guide to the mathematical commons

**Tentative local handoff, 2026-10-02 UTC. Contributor-reuse release hold.** The
seed's final certificate, one actual typed TLS transfer into supplier-offline
custody and the extracted small-reader positive/two-refusal gate have
independently adopted outcomes. Acquired-parent preparation failed at
`BRIDGE_RESERVED_FOUNDATION`; that failure is independently audited and adopted.
No repair was implemented in this milestone. This is not a completed typed
contribute–reuse–return loop. This guide selects no launch; the
[results](RESULTS.md) state the handoff boundary and the
[research desk](../../research/NOW.md) records later decisions.

## The idea in one paragraph

An agent works on mathematics of its own choosing. It can find a result someone
else has made available, obtain an exact formal interface and independently
check a compact certificate, then use that interface in its own Lean work. It
can contribute the resulting certified object for others to repeat this loop.
No central server, global research agenda, vote on truth or human-intention test
is required. V4 is a restricted experimental implementation of parts of that
loop, not a representation of all mathematics or a completed huge-network system.

Think of a distributed mathematical library, not a blockchain that every reader
must replay. The library's catalog is a hint about where to look. The downloaded
object carries separate evidence for its exact mathematical meaning.

## 1. The layers and their different responsibilities

| Layer | Question it answers | What it must not be mistaken for |
|---|---|---|
| Mathematical objects | What exact definition or proposition is this? | A human description or a name alone |
| Local assurance | Did the adopted checking program accept this exact object? | Proof that the program itself is sound |
| Custody and transport | Which reachable holder can supply the intact bytes? | Mathematical acceptance or permanent availability |
| Search and directories | Which candidates fit this finite query? | A complete fresh catalog of the whole network |
| Local agent workflow | Can I import the selected meaning, prove something and contribute? | A mandatory shared problem list or automatic research strategy |
| Useful growth | Does accessible prior work improve later work after costs? | More files, citations or certificate counts |

The first five layers can support the sixth, but cannot establish it merely by
existing. In particular, mathematical truth and practical usefulness are separate.
Ranking can be heuristic; the acceptance boundary cannot be a popularity score.

### Layer 1: exact reusable mathematics

A definition includes its checked type and computational body. A proposition
includes its exact formal statement and the definitions its statement needs.
The checking policy fixes a foundation F and a particular checker image. Changing
a definition body, foundation or checker is not an attribution edit: it changes
what the object means or what assurance is being claimed.

Here a foundation is the fixed stock of admitted constants, declarations and
rules on which new work may depend. A checker image identifies the exact program
whose execution a certificate proves. A profile packages the owner's precise
policy, program/file bindings and finite resource limits.

For example, `iter f n x` describes applying a state transformation `f` repeatedly
`n` times, starting at `x`. A theorem can state that a map preserving one step
also preserves repeated steps. Another agent needs the same exact meaning of
`iter`, not an opaque variable with the same friendly name.

The first profile permits safe transparent definitions whose type/body use only
the fixed foundation. They introduce checked vocabulary, not arbitrary axioms.
It does not yet permit arbitrary contributed inductive types, recursive chains
of contributed definitions or unrestricted Lean/mathlib import. Selected theorem
types can use at most four contributed definitions. Every selected premise and
local definition must actually be used under the API's precise rules.

Names and notation in a local Lean source are convenient presentation. Protocol
definition names are content-derived: `DMKN.Def.<64-lowercase-hex-ID>`. Lean source
may need `DMKN.Def.«<ID>»` when that final string starts with a digit; the raw
protocol name and the quoted source spelling are not interchangeable.

### Layer 2: compact, conditional assurance

A certificate is evidence that a particular pinned checking program accepted
particular committed data. It is not evidence that any program bearing the
word "checker" is correct. The owner independently adopts the local profile,
foundation and checker; it does not let a theorem supplier choose them.

The restricted Nanoda relation, its correspondence to the intended Lean semantics,
the admitted foundation and the recursive cryptographic machinery are explicit
assurance assumptions. V4 does not prove full Lean correspondence or foundation
consistency. Matching hashes establish byte identity, not semantic soundness.

There are two checking paths: Lean checks the local source/native terms, and a
separate restricted Nanoda checker checks the selected formal data inside the
cryptographically proved execution. The certificate establishes the latter
program's result, not a theorem that the two implementations agree on all Lean.

For certified theorem reuse, the contributor verifies each explicitly selected
parent's genuine receipt, checks a new proof using its interface, and discharges
the cryptographic assumptions before final acceptance. Dependency ranks strictly
decrease when following certified parents; unresolved assumptions cannot count
as a completed certificate. The final bundle is freshly verified locally.

This is the important large-network design choice: a receiver need not download
and replay the theorem proofs of every ancestor. It verifies the final receipt
and exact selected semantic material instead. That does **not** make a huge
statement, required definition body or demanded computation free. Nor does it
make certificate production cheap: the current seed required substantial work.

### Layer 3: exact objects held by independent peers

The network transfers inert bundles, not executable peer Lean source. A final
bundle contains exactly four files:

| File | Purpose |
|---|---|
| `bundle.json` | Manifest binding the files, profile, member and interface |
| `capsule.json` | Exact selected proposition or definition semantics |
| `journal.bin` | Entire committed public checking result |
| `receipt.bin` | Cryptographic checking certificate |

A proposition capsule carries the exact definition bodies required by its type,
but not its original proof or ancestral theorem proofs. A downloaded final bundle
is therefore different from the much larger private preparation/proving directory.

TLS authenticates the configured endpoint, not its mathematics. Hashes protect
exact received bytes, not future custody. A dishonest holder can withhold data;
a bad directory can omit a good candidate. Local certificate checking still
must refuse invalid mathematics. `ACQUIRED_UNVERIFIED` means intact bytes entered
custody, not permission to rely on their mathematical claims.

Objects can be replicated among holders. Each node keeps its own selected state;
there is no mandatory complete theorem ledger replicated by all nodes. Append-only
local invocation records preserve an operation's history, not a global consensus
chain. The network aspires to collectively hold reusable knowledge, while each
agent obtains only the material it selects. Nobody can guarantee every object
will survive without live holders and paid retention.

### Layer 4: bounded discovery, not omniscience

The typed index supports exact bundle/interface keys, type fingerprints,
constant keys and bounded conclusion-shape keys. It uses indexed metadata seeks,
not a required scan of every theorem body. A query reports its local cut,
coverage and finite row/byte/time limits. A type match is a candidate, not a proof
of applicability. Similar statements are not authenticated substitutions.

Direct queries use configured contacts. The inherited routed directory adds
rendezvous, leases and one explicit cooperative hot-key split with current-view
locators. An advertisement says "try this holder"; a locator says "try this
directory view." Neither verifies a theorem. Query, referral, placement and
acquisition work consume finite budgets rather than secretly contacting everyone.

The one-split mechanism is not arbitrary repeated splitting, automatic membership
maintenance, global latest-state agreement or full Kademlia/libp2p interoperability.
A large dynamic network still needs qualified maintenance and capacity policies.
Budget exhaustion or partitions can make discovery incomplete; "not found" is
not proof of global absence. Full huge-network search remains a central open issue.

### Layer 5: the local acquire–use–contribute loop

1. Choose a problem and write the intended formal statement locally. A direct
   proof without any network lemma is always allowed.
2. Derive a search key from locally known structure, query within declared limits
   and select an actual returned candidate.
3. Acquire its exact bundle. Independently verify it before mathematical reliance.
4. Give the bundle and owner-controlled Lean source to contributor `prepare`.
   It verifies selected parents, installs checked definitions and proposition
   interfaces, checks actual use and captures the new checking execution.
5. Continue that same operation using finite `advance` calls. READY is not a
   certificate. Only complete production, assumption discharge, fresh final
   verification and clean closure produce a final four-file bundle.
6. Offer that completed object. Another agent can independently repeat the loop.

The small reader only checks an existing certificate; it does not install
definitions into Lean or prove a child. Contributor preparation supplies the
separate semantic-import/proof path. It repeats its required parent checks; a
saved reader success flag or index record does not waive them.

Trusted local Lean source can execute code. Do not execute unknown peer source
in the contributor lane; this is not a hostile-source sandbox. Agents' research
strategy, prompts, skills and natural-language interfaces live outside core
mathematical acceptance. Human intention influences chosen work, not validity.

### Layer 6: what useful growth would mean

Fix F. A proved theorem already belongs to F's unrestricted deductive closure;
adding a lemma does not enlarge that closure. Nevertheless finite agents may
gain a capability: finding and using a difficult lemma within an affordable
budget rather than deriving it again. A checked definition can similarly make
useful vocabulary available without adding new logical strength.

That is the project's operational meaning of growth: **more accessible,
independently checkable mathematical capability for finite agents**. To measure
it, compare equally correct downstream endpoints with and without accessible
prior work. Let direct cost be A, search/reuse cost be C, incremental shared
production/setup be J and maintenance/failure cost be M. A finite net advantage
requires total downstream savings to exceed investment:

```text
sum of (A - C) over the stated downstream uses > J + M.
```

Report CPU, elapsed time, bytes, memory and agent effort separately. Unknown
model compute is not zero. Permit the direct baseline shorter proofs, ordinary
tactics and legitimate caches; forcing it to replay history manufactures an
advantage. A dependency occurrence shows use, not necessity or causal benefit.

Use frequency and learned similarity can guide optional local ranking, but
neither determines truth or universally measures mathematical importance.
No general novelty oracle, universal usefulness score or exponential-growth
guarantee is claimed. For the rigorous rationale see
[CORE-MODEL](../../research/cycles/v4-2026-10-02/CORE-MODEL.md) and
[PHILOSOPHY-OF-GROWTH](../../research/cycles/v4-2026-10-02/PHILOSOPHY-OF-GROWTH.md).

## 2. The software roles and current cost picture

The base archive, `mathematical-commons-v4-base.zip`, is 97,817,285 bytes. It
supplies `app/receiver` and `app/peer`. The optional contributor archive,
`mathematical-commons-v4-contributor.zip`, is 2,349,904,469 bytes and adds
`app/contributor` under the same extraction root. A reader need not become a
prover. Archives and extracted byte maps are already audited; do not rebuild
them just to follow this guide. Credentials, node state and proving checkpoints
are not bundled. Public licensing remains undecided.

The receiver closure is 97,302,245 bytes including Python and the verifier but
without Lean, the guest image or proof ancestry. That is installed size, not
the bytes needed for each theorem. The completed current seed bundle is 230,200
bytes; its receipt is 223,610 bytes and full journal 192 bytes.

The seed completed all 250 selected stages at the original contributor install.
Preparation plus production consumed 92,976.578125 known measured CPU seconds,
excluding model/shell/audit and other investment. Its final cold verification
worker consumed 0.046875 CPU / 0.603288 wall seconds, but those numbers are **not**
the shipped reader's full cost, proof-production cost or complete agent loop.
The separate protocol charge 105,270.75 seconds includes controller reservations;
it is an accounting ceiling consumption, not the same measured-cost quantity.

The actual shipped reader accepted that peer-acquired bundle. Its positive
command used 1.390625 inclusive worker CPU seconds and 6.3894983 outer wall
seconds in this single observation. The driver's reported 15ms cryptographic
check is not full-reader latency: asset hashing, profile/input validation and
startup remain payable. The whole positive-plus-two-refusals gate used 6.328125
known CPU seconds and 22.3430084 wall seconds. Nested verifier/controller work
must not be added again to an inclusive worker measurement. These observations
do not establish universal latency, huge-scale checking or net useful growth.

The actual same-host typed TLS transfer02 used 9.109375 known CPU seconds. Failed
transfer01 remains retained and charged 6.46875; both total 15.578125. The supplier
stopped before the final custody checks. This establishes one acquired object
surviving its original service, not independent physical hosting or permanent
availability.

The downstream acquired-parent attempt then failed at
`BRIDGE_RESERVED_FOUNDATION`, after genuine parent receipt verification and the
native conditional proof check, but before a guest snapshot, shape or READY
state. There is no completed child certificate or typed reciprocal certified
return. The adopted failure audit records 46.859375 known CPU seconds and
177.4151509 whole-call wall seconds, within the selected bounds. These costs
remain payable. The intermediate native capsule is byte-identical to the direct
control's capsule: the 8790-byte object binds the same exact endpoint, universes
and embedded iteration/addition definition bodies. This is genuine conditional
native reuse of the verified parent, not completed guest preparation or a child
certificate. Do not infer a successful trace/cost comparison from a failure
before the snapshot. The precise diagnosis and any later repair remain separate
decisions; the current contributor-reuse release stays held.

The attempted owned-row checking optimization passed its finite congruence
controls but failed its efficiency gate: 75 segments versus 66 in its comparison,
despite fewer guest instructions. It is a rejected optimization, not a speedup.
Current v4 does not establish a net useful-growth advantage or affordable broad
production. Compact receiver verification and expensive producer work must both
remain in the big picture.

## 3. Command templates and safety prerequisites

These PowerShell forms match the shipped APIs. They are **templates**, not a
single script to run, deployment authorization or qualification after relocation.
Replace example inputs with your own approved absolute paths, use fresh run/state
directories whose parent already exists, and keep mutable state/credentials out
of immutable application trees. Use finite process-tree supervision for complete
CPU/memory/wall limits. In-process sampled deadlines are not a hard sandbox.

Current evidence location matters: seed production executes at
`product-local/certified-definitions-integration-02/install`; peer transfer
executes source07 at `product-local/certified-typed-directory-source-07`.
Packaged byte equality does not establish execution or relocation of
`app/contributor` or `app/peer`. The adopted positive/two-refusal small-reader
gate actually executes the extracted `app/receiver`; it does not qualify the
other roles after relocation.

### Set role paths and independently adopted profiles

```powershell
$V4Root = 'E:\Distributed Trustworthy Mathematical Knowledge Network\product-local\certified-v4-package-01'
$Reader = Join-Path $V4Root 'app\receiver'
$Peer = Join-Path $V4Root 'app\peer'
$Contributor = Join-Path $V4Root 'app\contributor'
$ReaderPython = Join-Path $Reader 'runtime\python\python.exe'
$ContributorPython = Join-Path $Contributor 'runtime\python\python.exe'
$ReceiverSha = '4803d60f1498635e60a71684709b6b6388935105598ca82e5a06aa64cca00785'
$ContributorSha = 'e3a65bc792029d7fd3f028d127d54d2f8f5e3f72dd0d695003bbbd635f0b9f7c'
Get-FileHash -Algorithm SHA256 -LiteralPath "$Reader\profile.json"
Get-FileHash -Algorithm SHA256 -LiteralPath "$Contributor\profile.json" # add-on only
```

Those expected digests identify the audited **profile files**, not arbitrary
bundles or executables. First independently adopt the distribution's mathematical
policy; then compare local bytes. Do not replace the expected digest with a value
supplied by the theorem's holder. Relocation requires reviewing all absolute
config/state/contact/listener/protected-root/TLS paths and new config digests.

### Verify one acquired bundle

```powershell
$ReaderArgs = @('-I', '-S', '-B', "$Reader\cert_verify.py",
    '--profile', "$Reader\profile.json", '--profile-sha256', $ReceiverSha)
& $ReaderPython @ReaderArgs --bundle 'C:\MathCommons\custody\bundle-01' --run 'C:\MathCommons\checks\check-01'
```

The bundle, installation and fresh check directory must not overlap. A successful
result is `PASS_EXPERIMENTAL_COLD_CERTIFICATE_VERIFIED_NOT_NATIVE_ADMISSION`.
It authenticates the exact selected interface under local policy; it does not
import it into Lean or modify a native-node trust mode. The
[receiver API](../../product-local/certified-v4-package-01/app/receiver/API.md)
specifies actual input, output and refusal rules.

### Prepare and continue a theorem

The forms below document the API, not a qualified downstream workflow in this
held release. Do not bypass the foundation-protection refusal or retry the
retained failed operation to obtain a success label.

```powershell
$WorkflowArgs = @('-I', '-S', '-B', "$Contributor\cert_workflow.py")
$PolicyArgs = @('--profile', "$Contributor\profile.json", '--profile-sha256', $ContributorSha)
$BudgetArgs = @('--cpu-budget-seconds', 3000, '--deadline-utc', 'YYYY-MM-DDTHH:MM:SSZ')
& $ContributorPython @WorkflowArgs prepare @PolicyArgs @BudgetArgs --run 'C:\MathCommons\operations\theorem-01' --source 'C:\MathCommons\owned\Theorem.lean' --root-name MyTheorem --kind proposition --parent 'C:\MathCommons\custody\bundle-01'
& $ContributorPython @WorkflowArgs advance @PolicyArgs --run 'C:\MathCommons\operations\theorem-01' --max-new-stages 1
```

Replace the deadline with a real fixed future UTC time and choose a finite total
allowance. The 3000-second value is an example cap, not a production estimate;
the actual seed was far more expensive. Later `advance` calls continue the same
operation, do not renew its total budget/deadline, and accept 1..393 new stages per
call. Stop on failed or ambiguous unclosed state rather than silently retrying.
Omit `--parent` for a direct proof. A public prepare success/READY state is not
a new certificate.

To create reusable local definition data, use a separate fresh operation:

```powershell
& $ContributorPython @WorkflowArgs prepare @PolicyArgs @BudgetArgs --run 'C:\MathCommons\operations\definition-01' --source 'C:\MathCommons\owned\Definition.lean' --root-name MyDefinition --kind definition
```

After successful READY, `definition-01\child.capsule.json` can be supplied to
another theorem's `--local-definition <absolute-capsule-path>`. This route pays
two native calls and an actual guest snapshot; it is not free extraction. A bare
capsule is not a final bundle and cannot be offered as one. Definitions embedded
in an acquired proposition need no separate ancestral-definition fetch. See the
[contributor API](../../product-local/certified-v4-package-01/app/contributor/CONTRIBUTOR-API.md)
for canonical naming, use checks, safe F-closure and finite limits.

### Find, acquire and offer with separate owner nodes

The [network API](../../product-local/certified-v4-package-01/app/peer/CERTIFIED-NETWORK-API.md)
defines exact `DMKN_CERT_PEER_CONFIG_V1` fields: fresh local state, independently
adopted policy, up to 16 configured contacts, optional listener and four existing
protected roots. Provision owner TLS credentials outside those roots; none are
shipped. Config SHA-256 pins locally reviewed bytes, not remote advertisements.

```powershell
$PeerConfig = 'C:\MathCommons\config\owner.json'
$PeerConfigSha = 'REPLACE_WITH_REVIEWED_CONFIG_SHA256'
$LocalDiscoveryKey = 'constant:REPLACE_WITH_LOCALLY_DERIVED_64_LOWERCASE_HEX_NAME_ID'
$PeerArgs = @('-I', '-S', '-B', "$Peer\cert_peer.py",
    '--config', $PeerConfig, '--config-sha256', $PeerConfigSha)
& $ReaderPython @PeerArgs init
```

Initialize each fresh state once. On a serving owner, offer a completed object
and run a bounded service:

```powershell
& $ReaderPython @PeerArgs offer --bundle 'C:\MathCommons\operations\theorem-01\bundle' --kind publication
& $ReaderPython @PeerArgs serve --max-requests 2 --max-bytes 134217728 --wall-seconds 180 --cpu-seconds 60
```

On a requesting owner with alias `B` already approved in its **own** config:

```powershell
& $ReaderPython @PeerArgs peer-find --peer B --key $LocalDiscoveryKey --limit 2 --max-scanned 4 --max-bytes 16384 --timeout-ms 1000 --mode raw
& $ReaderPython @PeerArgs peer-acquire --peer B --remote 'C:\MathCommons\selected-remote.json'
```

The supplier service must be live while the requester acts in its separate
session. Save one actual `remotes` object returned by `peer-find` as the remote
JSON input; do not invent it or pass the entire reply. The key placeholder must
be replaced by a locally derived structural name ID, not a spelling such as
`Nat`; `shape1:` is another bounded structural key. Direct `type_diverse` is
optional and routed diverse search is unsupported. All offers/search/custody
remain `receipt_verified:false` until separate genuine local verification.

## 4. Reading statuses without overclaiming

| Status or observation | What has happened |
|---|---|
| `ACQUIRED_UNVERIFIED` | Exact bytes entered custody; mathematics not yet verified |
| `PASS_EXPERIMENTAL_COLD_CERTIFICATE_VERIFIED_NOT_NATIVE_ADMISSION` | Fresh small-reader certificate acceptance; no Lean import/new theorem |
| `PASS_PREPARED_OR_BOUNDED_PREFIX_NOT_CERTIFIED` / READY | Preparation or bounded production prefix; not a completed child |
| `PASS_EXPERIMENTAL_CERTIFICATE_BUNDLE_NOT_NATIVE_ADMISSION` | Final experimental certificate, fresh verification and bundle commitment |
| `FAILED_NOT_RESUMABLE` | Preserve failed state/cost; no silent automatic retry |
| Directory complete local cut | That declared finite local view was exhausted, not the entire global network |

Source-time warnings in bundled APIs deliberately remain frozen. Later actual
qualification is reported here and in RESULTS, not retroactively inserted into
used sources.

## 5. Qualification at this tentative handoff

| Boundary | Actual adopted evidence | Still not established |
|---|---|---|
| Byte delivery | Both archives and exact extractions audited | Contributor/peer relocation runtime, public licensing |
| New semantics | Restricted typed/definition checks and preparation gates | Full Lean correspondence, arbitrary mathematics/libraries |
| Seed production | COMPLETE 250 stages, actual final receipt and same-call cold verification | Cheap general proof production |
| Typed exchange | One real pinned-TLS selected-key transfer and supplier-offline A custody | Mathematical reliance from custody alone, independent physical hosts |
| Extracted small reader | Genuine acquired seed accepted; changed required-definition context refused before crypto; changed full journal refused by real verifier | Arbitrary receipt robustness/scale, Lean import and new theorem production |
| Acquired-parent local work | Genuine parent verification and native conditional use of the same exact endpoint; independently adopted bridge failure | No guest snapshot/shape/READY, completed child or certified return; contributor-reuse release hold |
| Search | Indexed selected-key/direct mechanisms and inherited one-split maintenance | Full huge dynamic network maintenance and universal recall |
| Useful growth | Costs retained; nontrivial vocabulary/endpoint chosen | Matched net same-endpoint advantage or exponential growth |

The immediate new-profile reciprocal-path blocker is the exact-interface bridge
refusal; small-reader acceptance and typed custody do not close that path.
The high-priority gaps also remain large-network search/maintenance, trustworthy
semantically useful reuse at broader scale, expensive production, and a fair
resource-accounted growth comparison. Further attribution machinery or a global
ledger does not close these gaps. A tentative version is a usable bounded step
toward the goal, not permission to label those central issues solved.

Evidence: [seed final audit](../../experiments/certified-growth-01/SEED-FINAL-031-OUTCOME.md),
[typed transfer02 audit](../../experiments/certified-typed-exchange-01/TRANSFER-SEED02-OUTCOME.md),
[shipped reader audit](../../experiments/certified-typed-receiver-01/REAL-QUALIFICATION-OUTCOME.md),
[acquired-parent failure audit](../../experiments/certified-growth-01/PREPARE-REUSE01-OUTCOME-REVIEW.md),
[packaging result](../../product-local/certified-v4-package-01/RESULT.json).
