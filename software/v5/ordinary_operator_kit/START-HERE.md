# Use the ordinary mathematical commons

This kit prepares inputs for the current Windows x86-64 ordinary package. It is
separate from `package/`: do not copy files into its hash-bound contents. Use the
complete approved Python 3.14.6 and Lean 4.34.0 runtimes. The selected package
PROFILE SHA-256 is:

```text
9c41b9a3fe36f7283af130ac6ef290e82c2a78c432980b2bea75ccdcf197a6d4
```

This is an input-preparation tool, not a theorem checker, autonomous investigator
or completed release. Its source/testing disposition is in the adjacent REVIEW.
The existing package README gives its source-build recipe; building another
package can produce a different profile and requires a separately selected kit.
Do not change this profile constant to bypass a mismatch.

## What the helper does

Copy **one** entry from `examples.json`'s `requests` object into a request file.
Fill every required null with your actual choice. Finite policy numbers are
examples, not measured requirements. Deliberate approval booleans start false.
The null TLS/CA values in the loopback examples are intentional, not missing data.

Save request JSON as UTF-8 **without a byte-order mark**. Windows PowerShell 5's
`Out-File`/`Set-Content` encoding defaults are unsuitable. An explicit preparation
example (edit the state choices before saving) is:

```powershell
$kitExamples = Get-Content -Raw -LiteralPath 'C:\commons\operator-kit\examples.json' | ConvertFrom-Json
$kitRequest = $kitExamples.requests.init
$kitRequest.state.catalog = 'C:\commons-work\catalog-a'
$kitRequest.state.custody = 'C:\commons-work\custody-a'
$kitRequest.state.store_id = [guid]::NewGuid().ToString('N') + [guid]::NewGuid().ToString('N')
$kitRequestFile = 'C:\commons-work\request-init.json'
if (Test-Path -LiteralPath $kitRequestFile) { throw 'Choose a fresh request filename.' }
[IO.File]::WriteAllText($kitRequestFile, ($kitRequest | ConvertTo-Json -Depth 64), [Text.UTF8Encoding]::new($false))
```

This manual example writes only your new request. The kit and product never
modify earlier reports. Use a new request filename for each explicit operation.

For example, after editing `C:\commons-work\request-init.json`:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons\operator-kit\prepare.py' `
  --request 'C:\commons-work\request-init.json' `
  --output 'C:\commons-work\prepared-init-01'
```

Use absolute paths. The preparation output must not exist, its parent must exist,
and it must be separate from all inputs, project/state directories and operation
outputs. No redirected paths or shared hardlinked input files are allowed.
The helper opens input JSON and writes only that fresh output directory. It does
not read catalog/custody contents, execute commands, build source, contact peers,
check proofs, retry or clean up failures. Preserve partial outputs after an OS
failure; select a genuinely new output only after understanding what happened.

Success writes config files, `arguments.json` and `RECEIPT.json`. The latter pins
the input/output bytes. Review the generated arguments/config before launching.
Any public report supplied to preparation is just data: even a matching SHA-256
does not authenticate its writer or prove its mathematics. The actual product
independently checks all mathematical/context/target bindings when invoked.

## Launch one prepared operation

Set these paths to your approved installation and selected prepared directory.
Create `C:\commons-work` yourself, but **not** the fresh diagnostic directory.

```powershell
$kitPython = 'C:\tools\Python314\python.exe'
$kitPackage = 'C:\commons\package'
$kitLean = 'C:\tools\lean-4.34.0-windows'
$kitPrepared = 'C:\commons-work\prepared-init-01'
$kitCall = Get-Content -Raw -LiteralPath "$kitPrepared\arguments.json" | ConvertFrom-Json
$kitTokens = [string[]]$kitCall.arguments
& $kitPython -I -S -B "$kitPackage\run.py" `
  --profile-sha256 $kitCall.profile_sha256 `
  --python-runtime 'C:\tools\Python314' --lean-runtime $kitLean `
  --diagnostics 'C:\commons-work\diagnostics-init-01' `
  --wall-seconds 180 --cpu-seconds 120 --memory-mib 1280 `
  --active-processes 6 --stdout-bytes 8388608 --stderr-bytes 1048576 `
  $kitCall.entry -- @kitTokens
```

These are explicit example ceilings, not guarantees of fit. Choose limits for
your workload before launch; do not automatically renew failed allocations.
Large producer reports may need the permitted stdout ceiling. Service wall time
must additionally cover setup, the chosen lease and cleanup. `LAUNCHER.md` in the
package defines all launcher bounds and the distinction between process-resource
containment and a security sandbox. This is neither safe arbitrary-project
execution nor independent security review.

The launcher reports process outcome in diagnostics `RUN.json`; this is **not**
mathematical acceptance. The actual command report is diagnostics
`child\stdout.txt`. Peer commands additionally write their operation output's
`RESULT.json`. An init or intake has no operation output directory; capture its
report from the launcher's child stdout. **Do not add `--output` to init/intake.**
Read failures and retained effects before deciding the next action.

To construct a report reference, select the actual report file and compute:

```powershell
(Get-FileHash -Algorithm SHA256 -LiteralPath 'C:\commons-work\diagnostics-init-01\child\stdout.txt').Hash.ToLowerInvariant()
```

Put its absolute path and the returned lowercase digest in `{ "path": ..., "sha256": ... }`.
Do not use launcher `RUN.json`, `PRODUCTION.json`, truncated console text, a
claimed PASS, or a report from an unrelated installation in place of that report.

## First independent use: init, find, preview, receive

1. **Initialize once.** The init request supplies fresh `catalog` and `custody`
   directories, a chosen unique 64-lowercase-hex `store_id`, and explicit custody
   limits. To generate the local store label without identity politics, use
   `$kitStoreId = [guid]::NewGuid().ToString('N') + [guid]::NewGuid().ToString('N')`.
   This is an opaque local label, not authentication or a secret key. Keep these
   exact state paths/ID and limits for later operations. The product initializes
   the basis; the preparer does not. Successful report operation `init` contains
   `result.status = INITIALIZED_LOCAL_OWNER` and `result.basis.local_root`.
2. **Choose contacts and search features.** The example contact is loopback, not
   a public discovery bootstrap. Use a real running provider's IP, port and
   explicit TLS policy. The kit never follows referrals or approves a provider.
   A `type-symbol` feature's `symbol_id` comes from a known exact binding or an
   earlier preview. A syntactically simple alternative is
   `[{"tag":"declaration-kind","value":"theorem"}]`, but a broad query may
   exhaust its bounded budget and should not be mistaken for useful ranking.
   The kit also accepts object-kind and declared-type-key features. For a manual
   formal query, use the existing packaged `query.py`/`run.py query` interface
   with your actual encoded type and known bindings, then take supported specs
   from its SPECS output. It is query preparation, not a proof or a semantic oracle.
   The kit does not generate formal types or guess theorem IDs.
3. **Run find.** Fill `find` with your contact, provider order, specs and limits.
   It outputs `result.matches`; even successful status `INCOMPLETE_SEARCH` is
   explicitly incomplete. No result does not prove absence. Current find has no
   slow-provider fairness guarantee. Nothing here modifies its search policy.
4. **Preview a particular match.** Supply the exact find report and a deliberate
   zero-based `match_index`. The helper copies that returned provider, snapshot
   and complete record into preview config; it does not invent an identity.
   Preview returns the inert declared type and its `type_bindings`.
5. **Optionally inspect an unfamiliar symbol.** The inspect request takes the
   preview report and a zero-based `binding_index` in `result.preview.type_bindings`.
   It requests that exact `(name, export_id)` from the selected provider, not its
   proof ancestry. Inspection remains inert and might be unavailable. To seek an
   ordinary source realization for the selected theorem/concept itself, the
   authoring-offers request takes the preview report. Replies are unverified
   suggestions; the helper neither follows them nor approves execution.
6. **Receive independently.** Supply your exact state, a deliberately selected
   successful `parent_report`, the find report/match index and an explicit
   `dependency_policy`. Parent reports may be a successful init, completed intake,
   or successful CHECKED/REUSED receive for this same state; no newest root is
   looked up. `selected-unit-only` refuses missing prerequisites with
   `NEED_GROUNDED_PREMISES`; this is not a false theorem. `bounded-closure`
   authorizes the existing bounded ancestor acquisition. Neither makes arbitrary
   cold acceptance cheap. Check the actual receive result: CHECKED or
   REUSED_LOCAL_ACCEPTANCE with an admission is different from a bound preview,
   successful acquisition or a missing-premise outcome.

If you already have the existing encoded native type and exact known-binding
files, the manual query-preparation command is:

```powershell
& $kitPython -I -S -B "$kitPackage\run.py" `
  --profile-sha256 '9c41b9a3fe36f7283af130ac6ef290e82c2a78c432980b2bea75ccdcf197a6d4' `
  --python-runtime 'C:\tools\Python314' --lean-runtime $kitLean `
  --diagnostics 'C:\commons-work\diagnostics-query-01' `
  --wall-seconds 60 --cpu-seconds 30 --memory-mib 512 `
  --active-processes 4 --stdout-bytes 1048576 --stderr-bytes 1048576 `
  query -- --native-type 'C:\commons-work\native-type.json' `
  --bindings 'C:\commons-work\known-bindings.json' `
  --output 'C:\commons-work\query-output-01'
```

Its `SPECS.json` is the exact list to place in find's `specs`. Do not supply prose,
an unelaborated Lean source string or guessed bindings to this byte-oriented
interface. If you do not have these inputs, use an actual known-symbol binding
or an explicitly chosen supported structural feature instead; the kit does not
pretend a human-language interface is required or already implemented.

## Develop a new concept or theory, then return it

Use an independently obtained, explicitly approved compatible ordinary Lean/Lake
project. Define abstractions, examples, counterexamples, connections and theorems
there. No global task list or human-intention predicate is part of acceptance.
The helper does not create a project or claim that every discovered artifact has
available source. Existing inert/math records and source realizations are distinct.

In `produce-baseline`, choose actual **compiled** `project_search_paths`, logical
`modules` and completed `output_names`. Set `approve_local_project` to true only
after deciding that executing/loading this project is acceptable. Resource caps
do not protect you from approved hostile project code. Copy actual structured
Lean names rather than guessing dotted names. For illustration only, the name
`Nat.add_zero` is encoded as:

```json
[[0,{"$bytes":[78,97,116]}],[0,{"$bytes":[97,100,100,95,122,101,114,111]}]]
```

Each string component is UTF-8 bytes; a numeric component is `[1, n]`. Modules
are lists of such components too. The helper supports ordinary ASCII logical
module identifiers; it does not transform filenames into approved modules.
The project selection contains exactly schema
`DMKN_ORDINARY_TRUSTED_PROJECT_EXTRACTION_V1`, `project_search_paths`, `modules`.
Choose the actual logical mapping used at build: a renamed module can change
generated declaration identities even when visible source is similar.

Produce emits an inert bundle and a full successful command report with status
`PRODUCED_INERT_BASELINE_NOT_ACCEPTED`. Retain its `manifest.json`, exact unit files
and full public report. `PRODUCTION.json` is only a pre-manifest observation, not
this terminal report. You may share/relocate the exact bundle; source approval
and mathematical admission do not transfer with it.

For `intake-baseline`, choose your current exact parent report, the full producer
report, the actual receiver-local bundle directory and its exact manifest reference.
The kit verifies manifest length/hash/semantic correspondence, not every unit or
proof; the product performs that work. A relocated copy is allowed: producer
report paths are never followed. This producer-based convenience route is not
required by the underlying product when an exact bundle was obtained otherwise.

Only a successful `BASELINE_INTAKE_COMPLETE` is eligible for this kit's publication
handoff. It records the actual final local root and completed batch sequence.
A stopped intake's `last_confirmed_root` may be legitimate partial progress, but
the kit refuses to silently convert it into whole-bundle success. Use the existing
status/recovery rules explicitly; preserve all partial state and failed reports.

## Publish and serve without private-state intervention

Prepare `publish` with the same explicit state, the producer report, the completed
intake report and deliberate zero-based `target_indices`. The helper requires the
same manifest identity and copies only those exact target rows. Choose a separate
index directory and full index limits. `create: true` is for a fresh index;
`false` reopens an existing one. Publication can commit separate targets before a
later failure. The real product validates each target against the actual accepted
local context; neither report JSON nor kit output supplies acceptance authority.

Prepare `serve` using that **existing** index, same custody/owner, chosen endpoint,
finite lease and limits. Set both `share_all_custody` and `exclusive` true only
after choosing to expose **all addressable contents** of this custody. This is not
a per-theorem ACL. Stop other commands using that owner while it serves; the
ordinary public route serializes serving and mutation. Let the finite lease end,
then explicitly update/publish and start a new separately chosen service if needed.
No daemon renewal is installed. A second local client can query the chosen loopback
port during the lease; loopback success is not independent-host qualification.
Wait for the actual service output's `READY.json` before querying; use its
returned `host`, `port` and `tls` fields. If you selected port 0, the returned
port is the chosen listening port: never put port 0 into client contacts. With a
fixed example port such as 38191, a bind failure is a failure, not permission to
silently try a different port or extend the lease. The operator chooses the next
action explicitly.

Remote serving requires explicitly selected TLS certificate/key paths and their
SHA-256 pins. The kit does not open private keys, create credentials, change
firewalls, register a domain or publish externally. For remote contacts a null
server_name permits the product's IP-based TLS check; it is not verification bypass.
License, release authentication, independent hosting and maintenance remain
separate decisions, not implied permission from this walkthrough.

## Deliberate limits and source crosswalk

The kit handles the ordinary common path, not every public operation or recovery
case. It refuses inputs outside its small subset; use reviewed original interfaces
for unsupported modes. No latest-root inference, automatic proof import, automatic
source execution, fallback certificate or useful-growth guarantee is added.
Stable owner-controlled paths are assumed; path checks are not protection against
a malicious same-account process swapping files between checks.

The implementation contracts are the current package's `owner.py`, `peer_api.py`,
`support/transport/ordinary_acquisition.py`, `support/discovery/{search_session,
candidate_query,discovery_store,ordinary_export_adapter}.py`, and its baseline
production/intake helpers. The exact source equivalents are
`ordinary_native_package/owner.py`, `ordinary_bounded_operations/peer_api.py`,
`ordinary_authoring_offers/ordinary_acquisition.py`, `discovery/` and
`ordinary_formal_query/discovery/ordinary_export_adapter.py`,
`ordinary_producer_package/baseline_production.py` and
`ordinary_baseline/baseline_intake.py` under `software/v5/` in the source checkout.
The kit reuses their public shapes. It does not import them or silently generalize
their correctness and deployment claims.
