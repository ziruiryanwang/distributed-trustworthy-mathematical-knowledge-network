# Use the local mathematical commons

This kit connects ordinary Lean 4 work to decentralized discovery, independent
checking and sharing. You choose the mathematics: definitions, models, proofs,
counterexamples and new theories. The software helps you acquire selected work,
check it in your own context, develop it and return usable results.

This is the current local development distribution. It is unpublished; its license
is undecided. It is not a declaration that the full v5 release is complete.
Use this guide for the prebuilt and for installations produced by the included
source recipe. Their preserved `package/README.md` describes historical assembly
stages; do not follow its overlay/build sequence.

## What is in the kit

| Path | Purpose |
|---|---|
| `package/` | The 160-file ordinary-library implementation, including historical name export, offline lookup and policy-scoped directory refresh. |
| `operator/` | Three matching offline input-preparation files; keep them together. |
| `preview/` | Offline formal-type viewer; keep its two files together. |
| [REQUESTS.json](REQUESTS.json) | Fifteen common request templates, direct name-directory commands, two dedicated-host configurations and one project descriptor. |
| [REFRESH-USAGE.md](REFRESH-USAGE.md), [REFRESH-REQUESTS.json](REFRESH-REQUESTS.json) | Provider-maintained contact feeds and finite registrar refresh, with separate exact configuration templates. |
| `source/` | Exact selected current source/build inputs, retaining their relative source paths. |
| `kit.py`, `file_helpers.py` and `KIT-MANIFEST.json` | Verification utility, its adjacent helper and complete distribution inventory; keep them together. |

Supported external tools are **Windows x86-64, Python 3.14.6 and Lean 4.34.0**.
Supply separately approved complete installations; the kit contains neither runtime.
Other platforms/toolchain versions have not been established by this selection.
No mathematical corpus, owner database, contact server or credentials are bundled.

The selected prebuilt `package/PROFILE.json` SHA-256 is:

```text
f75dda6e534450cdf5d4db2901c3e1964501514da817bc3eb8aadebc0c350f7b
```

Its `installation/INSTALLATION.json` SHA-256 is:

```text
9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27
```

These identify this prebuilt, not every future source build. A matching hash binds
selected bytes; it does not authenticate a publisher or make downloaded code safe.

## Select the extraction once

Obtain and approve the kit utility, archive and external receipt through your
chosen trusted handoff. Compare archive size/hash with that receipt, extract into
a fresh protected directory, and use the receipt's manifest hash for verification.
This example assumes the kit is at `C:\commons` and approved runtimes are elsewhere:

```powershell
$commonsRoot = 'C:\commons'
$commonsPythonRoot = 'C:\approved\Python314'
$commonsLeanRoot = 'C:\approved\lean-4.34.0-windows'
$commonsPython = "$commonsPythonRoot\python.exe"
$commonsPackage = "$commonsRoot\package"
$commonsProfile = 'f75dda6e534450cdf5d4db2901c3e1964501514da817bc3eb8aadebc0c350f7b'

& $commonsPython -I -S -B "$commonsRoot\kit.py" verify `
  --root $commonsRoot --manifest-sha256 'REPLACE_WITH_APPROVED_KIT_MANIFEST_SHA256'
```

Use absolute local paths. Keep your work directories outside the kit and both
runtimes. Inputs must remain stable during an operation. Output leaves must be
fresh, with existing parents; do not reuse a failed output directory. Preserve
failures and partial state for the documented recovery path. Never delete a lock
or alter a report/manifest to make a refused operation appear successful.

## Prepare and run an operation

Choose exactly one object inside `requests` in [REQUESTS.json](REQUESTS.json).
The template's label is descriptive; its `action` is the actual preparer command.
For example, `publish-accepted` has action `publish`. Fill required `null` values
with your selections. Null TLS/CA fields in loopback contacts are intentional.
Approval/sharing booleans start false; select true only for the corresponding
local source/project execution or whole-custody disclosure you approve.

Save the selected request as UTF-8 JSON **without a BOM**. For a PowerShell object:

```powershell
$commonsTemplates = Get-Content -Raw -LiteralPath "$commonsRoot\REQUESTS.json" | ConvertFrom-Json
$commonsRequest = $commonsTemplates.requests.init
# Fill the selected object's required values before writing it.
$commonsRequestFile = 'C:\commons-work\request-01.json'
if (Test-Path -LiteralPath $commonsRequestFile) { throw 'Choose a fresh filename.' }
[IO.File]::WriteAllText($commonsRequestFile,
  ($commonsRequest | ConvertTo-Json -Depth 64), [Text.UTF8Encoding]::new($false))

& $commonsPython -I -S -B "$commonsRoot\operator\prepare_selected.py" `
  --package $commonsPackage --profile-sha256 $commonsProfile `
  --request $commonsRequestFile --output 'C:\commons-work\prepared-01'
```

The helper writes inert inputs, `arguments.json` and `RECEIPT.json`. It does not
search, open mathematical state, compile Lean or check a proof. It checks the
known configuration interface and actual direct-source bytes; it does not approve
native binaries. Review the prepared files, then launch the selected operation:

```powershell
$commonsCall = Get-Content -Raw -LiteralPath 'C:\commons-work\prepared-01\arguments.json' | ConvertFrom-Json
$commonsTokens = [string[]]$commonsCall.arguments
& $commonsPython -I -S -B "$commonsPackage\run.py" `
  --profile-sha256 $commonsCall.profile_sha256 `
  --python-runtime $commonsPythonRoot --lean-runtime $commonsLeanRoot `
  --diagnostics 'C:\commons-work\diagnostics-01' `
  --wall-seconds 180 --cpu-seconds 120 --memory-mib 1280 `
  --active-processes 6 --stdout-bytes 8388608 --stderr-bytes 1048576 `
  $commonsCall.entry -- @commonsTokens
```

These numbers are finite example ceilings, not a capacity promise. Select budgets
appropriate to the work, including setup and cleanup; a cold library intake can
cost much more than a query. [LAUNCHER.md](package/LAUNCHER.md) specifies supported
flags, Windows Job containment and recovery boundaries. Resource limits do not
sandbox arbitrary executable source. A zero launcher exit establishes clean
operation completion, not necessarily mathematical acceptance: read the result.

## Keep exact reports for continuation

A report reference is `{ "path": "absolute-path", "sha256": "lowercase-hash" }`.
Compute the hash from the actual completed file:

```powershell
(Get-FileHash -Algorithm SHA256 -LiteralPath 'C:\commons-work\diagnostics-01\child\stdout.txt').Hash.ToLowerInvariant()
```

| Operation | Complete report to retain | Used next for |
|---|---|---|
| Init or intake | Launcher `child/stdout.txt` owner wrapper | Checked parent selection. |
| Symbol or exact-type query | Operation `RESULT.json` or complete child stdout | `find-query.query_report`. |
| Name-directory export | Complete successful `RESULT.json`, `DIRECTORY.json` hash and all directory files | Offline historical name lookup. |
| Name-directory lookup | `RESULT.json`; `SPECS.json` only when all names resolve | Explicit `find` specs, never `query_report`. |
| Find | Operation `RESULT.json` | Deliberate `match_index` selection. |
| Preview | Operation `RESULT.json` | Offline display, binding inspection or authoring offers. |
| Receive | Operation `RESULT.json` | Checked parent, target index 0, or republication. |
| Contribute | Complete launcher `child/stdout.txt` owner wrapper | Parent, selected acquired targets or publication. |
| Produce-baseline | Complete launcher `child/stdout.txt` producer wrapper | Matching intake/publication selection. |

Do not substitute launcher `RUN.json`, partial stdout, an unwrapped contribution
result, or an earlier accepted field inside a failed operation. Reports select
inputs; current product checks establish actual mathematical acceptance.

## Investigator route

**Create or retain your checked context.** `init` creates fresh catalog and custody
directories. Pick a stable lowercase 64-hex `store_id` for that owner; it is a
local identity, not a human account or proof warrant. State paths are fresh only
for initialization and existing thereafter. To ground a selected library, use
`intake-explicit-manifest` with a complete inert bundle and its pinned manifest.
Intake independently checks that bundle against the selected parent. There is
no compulsory download of a global ledger or complete mathematical corpus.

**Find unfamiliar laws over a concept you know.** You do not need a desired
theorem name, target identifier or exact full theorem statement. Start with a
shared carrier or interface, choose providers likely to cover it, and inspect
their returned theorem types. For example, a local development workflow searched
for the known `Std.HashMap` symbol plus theorem kind, received six unfamiliar laws,
and selected a characterization of nonempty results and an execution witness.
Those interfaces supported a new contextual-refinement theory. This demonstrates
the route; it does not establish general relevance, completeness or a speedup.
Use your own selected library and contacts; no historical experiment needs to be
re-created and no example corpus is bundled.

`prepare-symbol-query` takes one through
eight exact qualified names, such as `MyTheory.Closure`, and a selected parent
report. Its `state` contains only `catalog` and `store_id`; do not add custody
or custody limits. The later query operation projects symbols from that context's
committed metadata without opening proof snapshots. It reports that snapshot
integrity was not checked. Missing names fail the whole query; no meanings are
guessed. Simple dotted names are convenience syntax, not arbitrary Lean parsing.
For unusual/numeric names, replace `symbol_names` with exact `structured_names`.
Alternatively replace `parent_report` with an exact `context_root`.

Use the resulting report in `find-query`, choosing known contacts and aggregate
budgets. For direct features, replace `query_report` with `specs`, for example:

```json
[{"tag":"declaration-kind","value":"theorem"}]
```

This broad example is valid but may be unselective. Available tags also include
`type-symbol`, `object-kind` and `declared-type-key`. Choose selective known
features where possible. `candidate_mode: "sparse-v2"` is optional and needs a
compatible configured provider; see [SPARSE-SEARCH.md](package/SPARSE-SEARCH.md).
Search covers the selected providers/snapshots within its budget. An empty or
partial response cannot establish that no relevant mathematics exists elsewhere.
Several type-symbol specs mean a conjunction: requiring every familiar symbol
can exclude a useful unfamiliar abstraction. Start with a useful common interface,
add selective kind/other constraints where justified, and inspect the result.
An enormous or irrelevant candidate bucket is a reason to revise the query or
provider selection, not to treat a bounded first page as the whole literature.

**Reuse saved queries, or export a stable library's names once.** If you repeat
the same symbol query, reuse its saved specs. If you investigate many different
names in a large retained library, the optional directory below avoids opening
that owner's metadata for each new name. It does not add a new semantic matcher.

**When you already know an exact formal type**, the optional `prepare-query` template takes a pinned
native-type file produced by approved local Lean code. Add the package's
`authoring/helpers` to that approved project's Lean search path and use:

```lean
import OwnerQueryCommand
universe u
variable {A : Type u} (f : A -> A)
#ordinary_type_query [u] "C:/commons-work/fresh-type.json" :
  forall x, f (f x) = f x
```

This is ordinary local elaboration, not execution of remote source. Unlike the
symbol-only query, this route retains the full selected context checks. Its
matching is syntactic; it does not decide arbitrary mathematical equivalence.
There is no whole-type renaming or general analogy profile in this package.

**Read before receiving.** Select a find row and run `preview`. View the saved
result without a service, owner, Lean worker or proof acquisition:

```powershell
$commonsPreviewReport = 'C:\commons-work\preview-01\RESULT.json'
$commonsPreviewHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $commonsPreviewReport).Hash.ToLowerInvariant()
& $commonsPython -I -S -B "$commonsRoot\preview\view_preview.py" `
  --package $commonsPackage --profile-sha256 $commonsProfile `
  --report $commonsPreviewReport --report-sha256 $commonsPreviewHash `
  --output 'C:\commons-work\view-01'
```

The viewer writes `VIEW.json`; a complete display also has `TYPE.txt`. It retains
all encoded premises, binder scopes, universes and exact symbol bindings.
`TYPE_DISPLAY_COMPLETE` means the entire formal display fits its caps.
`TYPE_DISPLAY_INCOMPLETE` contains no partial type masquerading as complete.
Neither means the theorem was checked. Display syntax is not promised to compile
as Lean source. Use its binding indices with `inspect` to request an unfamiliar
definition's inert evidence. `authoring-offers` returns advisory project pointers;
they are never authority to download or execute a project automatically.

**Receive what you choose to use.** The `receive` template requires either
`selected-unit-only` or `bounded-closure`. The first can require already grounded
premises; it does not automatically fetch proof ancestry. The second permits
dependency acquisition only within its explicit limits. Retained compatible local
knowledge avoids unnecessary acquisition, but cold work may still need its
dependency closure. Successful recipient admission, not preview or popularity,
supplies the checked target.

**Develop concepts and consequences.** Ordinary approved Lean source is the
preferred authoring route when already available. `contribute` accepts a pinned
UTF-8 source body, a checked parent, zero through eight acquired-report selections
and one through 32 exact output names. Select the acquired target indices you
actually need; use `acquired: []` when none are needed. A receive report has its
single target at index 0. The combined acquired target limit is 32. Output names
must not repeat an acquired name. A structured name for `Example.law` is:

```json
[[0,{"$bytes":[69,120,97,109,112,108,101]}],[0,{"$bytes":[108,97,119]}]]
```

Place that name inside the `output_names` list. This exact encoding is needed
for output selection; the dotted-string convenience belongs to symbol queries.
New definitions, models, negative results and bridge theorems can all be useful
contributions. Kernel success establishes validity under the selected foundation,
not novelty or scientific importance.

For an approved installed library/project, use `contribute-with-frontier` and
save the catalog's `project_descriptor` as its own pinned file. Fill its module
name, existing project directory, compiled search paths and imports. The optional
`authoring_frontier_report` must select a compatible checked ancestor in the same
owner. The product checks that relationship and reconstructs demanded interfaces
above it; it still checks the final contribution against the actual parent.
Omit the frontier field for project authoring without that optimization. Omit
both project fields and frontier for plain contribution. Missing frontend metadata
or incompatible local definitions can refuse; notations/instances are not recreated
universally. Local source/project approval does not approve downloaded code.

An existing ordinary compiled project can instead use `produce-baseline` to export
selected declarations, followed by independent `intake-explicit-manifest`. Production
is not recipient acceptance. `spool_mib` has the existing 144 through 256 range.
Module names and output names use the structured encoding above. The product's
[PRODUCER.md](package/PRODUCER.md) specifies the exporter boundary.

**Return usable work.** `publish-accepted` selects target indices from a completed
receive or contribution report. `publish-produced` instead combines a producer
report with its completed matching intake report. Both create or extend a selected
local index from actual retained evidence. Set `index.create` true only for a new
index; select false for an existing one with its actual limits. Publication alone
starts no listener. `serve-owner` exposes the selected index and all selected
owner custody during one finite lease, with explicit sharing and exclusive-use
approval. For a host that owns no mathematical state, use the dedicated inert
host route below.

## Resolve new names offline from a historical directory

Choose an existing retained catalog, its exact `store_id` and a checked context
root you have already selected. Run this direct launcher command; it is not an
operator-preparer action. Substitute those three values and use fresh outputs:

```powershell
& $commonsPython -I -S -B "$commonsPackage\run.py" `
  --profile-sha256 $commonsProfile --python-runtime $commonsPythonRoot --lean-runtime $commonsLeanRoot `
  --wall-seconds 90 --cpu-seconds 30 --memory-mib 768 --active-processes 3 `
  --stdout-bytes 1048576 --stderr-bytes 1048576 `
  --diagnostics 'C:\commons-work\directory-export-launch01' `
  query -- --catalog 'C:\commons-work\catalog' `
  --store-id 'REPLACE_WITH_SELECTED_STORE_ID' --context-root 'REPLACE_WITH_SELECTED_CONTEXT_ROOT' `
  --directory-export v1 --output 'C:\commons-work\name-directory01'
```

Do not add custody, a native-type file or a name list. Export validates the whole
selected metadata once under the normal owner lifecycle, closes that owner, and
writes all recorded bindings with a final `DIRECTORY.json` commitment. It runs
no Lean worker and checks no proof snapshots. Require a complete successful
report and clean closure; retain its `directory_receipt.directory_manifest_sha256`
independently. Keep `DIRECTORY.json`, `ENTRIES.bin` and `TREE.bin` together.

For each lookup, save one through eight exact structured names as UTF-8 JSON
without a BOM. For example, this list asks for the single name `Std.HashMap`:

```json
[[[0,{"$bytes":[83,116,100]}],[0,{"$bytes":[72,97,115,104,77,97,112]}]]]
```

Use your own exact names; they must exist in the selected historical directory.
Run the packaged offline command directly:

```powershell
& $commonsPython -I -S -B "$commonsPackage\lookup_directory.py" `
  --profile-sha256 $commonsProfile --directory 'C:\commons-work\name-directory01' `
  --directory-sha256 'REPLACE_WITH_APPROVED_DIRECTORY_MANIFEST_SHA256' `
  --symbol-names 'C:\commons-work\names-01.json' --output 'C:\commons-work\lookup-01'
```

Lookup opens no owner, service or Lean worker. It authenticates selected records
or absence boundaries with logarithmic fixed-size directory reads per name, plus
bounded name/manifest/software work. If every name resolves, `SPECS.json` contains
the query array. In `find-query`, remove `query_report` and supply that array as
`specs`. You may append `object-kind = ordinary-lean-export-v2` and
`declaration-kind = theorem` when useful; the whole conjunction may contain at
most eight specs. The directory's `RESULT.json` is not an accepted `query_report`.
Any missing name suppresses all specs rather than weakening the query.

The approved complete export is the origin of this mapping; a foreign manifest
merely claiming your root does not establish that relationship. A lookup does not
check current owner readiness or prove mathematical truth. Absence means absent
from this directory, not absent from a newer root or the network. Keep using a
stable directory for its old names; deliberately export a fresh one when newer
bindings are needed. Rebuilding after every unrelated contribution defeats its
purpose. New roots never update it implicitly.

## Keep investigating and sharing

Retain your owner and index between operations. Fresh output directories do not
mean resetting mathematical knowledge. For an evolving collection, repeat this
supported cycle:

1. Let the previous owner service finish and inspect actual clean closure.
2. Contribute or intake a batch against your actual selected checked parent.
3. Publish selected accepted targets to the existing index with `create:false`
   and its original limits. Earlier successful target publications remain if a
   later target fails; a multi-target call is not one atomic transaction.
4. Start another finite owner-service lease with fresh diagnostics and outputs.
   Record that invocation's actual endpoint and readiness for clients.

Admission/publication and service on the same owner are serialized by its lock.
Ordinary research outside protected selected inputs can continue while serving;
owner updates wait for a service gap. Do not copy open databases or remove locks.
Each lease and operation has its own explicit budget; nothing renews itself.

Use a dedicated inert host for a stable selected library. Its completed generation
can be served repeatedly, but it has no append/update API: preparing a fresh full
generation copies its included bundle again. Prefer batched incremental owner
publication for frequent changes. Finite quotas eventually refuse growth, and
independent custody/retention arrangements are still needed for continued access.
Neither a successful cycle nor several local processes proves worldwide coverage
or continuous availability.

## Continue across an auxiliary package update

Reports normally must match the selected PROFILE. For existing same-owner parent,
acquired-target and frontier selections, eligible requests may explicitly add:

```json
"selection_report_policy": "prior-profile-extract-only-v1"
```

This is allowed on `contribute`, `receive`, `intake-baseline`, `prepare-query`,
and `prepare-symbol-query` requests that contain `parent_report`. It preserves the
old PROFILE and selected rows in `selection-disclosure.json`; old reports are not
rewritten. Current backend state/identity/proof checks remain required. It does
not relax find, preview, publication, producer or query-result report rules and
does not migrate an owner, change mathematical implementation or rebind a host.

## Dedicated inert host route

This role stores and serves evidence without creating a mathematical owner or
running Lean. The package still requires its selected Python and Lean attachments.
It starts from an existing inert bundle: selected manifest plus `units/` files.
Do not point it at a live owner's custody or copy an open database.

Copy `host_configs.prepare` from the catalog into its own config file, fill the
manifest path/hash and one through 64 exact target rows, and explicitly set
`share_all_bundle` true to approve exposure of the entire bundle and its generated
export locators, including unindexed declarations. Target rows are from actual
producer/return results, not guessed names. Its limits are finite example ceilings.
Host configs are **direct product configs**, not `operator` request actions.

```powershell
$commonsHostConfig = 'C:\commons-work\host-prepare.json'
$commonsHostConfigHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $commonsHostConfig).Hash.ToLowerInvariant()
& $commonsPython -I -S -B "$commonsPackage\run.py" `
  --profile-sha256 $commonsProfile --python-runtime $commonsPythonRoot --lean-runtime $commonsLeanRoot `
  --wall-seconds 90 --cpu-seconds 30 --memory-mib 768 --active-processes 3 `
  --stdout-bytes 1048576 --stderr-bytes 1048576 `
  --diagnostics 'C:\commons-work\host-prepare-launch01' `
  host -- prepare --host-root 'C:\commons-work\host01' `
  --config $commonsHostConfig --config-sha256 $commonsHostConfigHash `
  --output 'C:\commons-work\host-prepare-output01'
```

Successful preparation leaves `HOST.json` and a permanent dedicated-host marker,
lock, custody and index beneath the chosen root. Preserve them together. It is
an immutable logical generation, not a running listener. There is no content
refresh API; create a deliberate fresh generation when needed. SQLite reopening
or recovery can still write its storage files. The marker/lock must not be removed
to bypass exclusions; contribution work belongs in separate owner directories.

After clean preparation, copy `host_configs.serve` into another config, set
`share_all_custody` and `exclusive` true, and select the exact seal:

```powershell
$commonsHostServeConfig = 'C:\commons-work\host-serve.json'
$commonsHostServeHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $commonsHostServeConfig).Hash.ToLowerInvariant()
$commonsHostSealHash = (Get-FileHash -Algorithm SHA256 -LiteralPath 'C:\commons-work\host01\HOST.json').Hash.ToLowerInvariant()
& $commonsPython -I -S -B "$commonsPackage\run.py" `
  --profile-sha256 $commonsProfile --python-runtime $commonsPythonRoot --lean-runtime $commonsLeanRoot `
  --wall-seconds 120 --cpu-seconds 30 --memory-mib 768 --active-processes 3 `
  --stdout-bytes 1048576 --stderr-bytes 1048576 `
  --diagnostics 'C:\commons-work\host-serve-launch01' `
  host -- serve --host-root 'C:\commons-work\host01' --host-sha256 $commonsHostSealHash `
  --config $commonsHostServeConfig --config-sha256 $commonsHostServeHash `
  --output 'C:\commons-work\host-serve-output01'
```

The example binds loopback and requests port 0. Read the actual live `READY.json`
in this invocation's output, then use that endpoint in client contacts. A saved
READY file does not establish a current service. Clients must run during the
lease; no renewal occurs automatically. Leave room for cleanup and inspect final
closure. A complete locator/evidence object can fit the provider's remaining
allowance even when the client's independent maximum is larger; oversized objects
are refused, never truncated into valid evidence.

Non-loopback service requires the existing TLS object with `cert_file`,
`cert_sha256`, `key_file`, `key_sha256`; clients choose matching TLS/CA settings.
This local kit does not configure internet exposure. Host seals remain bound to
their original PROFILE: use their original package or prepare a fresh generation.
Copies on one computer are not independent availability guarantees.

## Maintain discovery contacts across independent providers

For a small stable collection, a locally selected static directory remains useful.
When providers change their own endpoints, the new `directory-refresh-serve`
command fetches their current contact feeds and applies your previously approved
route, endpoint and quota policy. Each finite invocation builds a fresh map;
failed sources have no cached fallback and partial refresh remains explicit.

Follow [REFRESH-USAGE.md](REFRESH-USAGE.md) for the full provider, registrar and
reader procedure. Its direct commands use [REFRESH-REQUESTS.json](REFRESH-REQUESTS.json),
not a new action in the offline preparer. Approved feed origins and topics remain
local choices. The registrar does not connect to learned endpoints, certify
their availability or change the recipient's mathematical checking rules.

## Build from the included current source when needed

No rebuild is needed to use this prebuilt. For a deliberately selected source
build, use the included direct recipe; there is no historical overlay sequence:

```powershell
& $commonsPython -I -S -B "$commonsRoot\source\software\v5\ordinary_registration_refresh\build.py" `
  --source-root "$commonsRoot\source" `
  --python-runtime $commonsPythonRoot --lean-runtime $commonsLeanRoot `
  --output 'C:\commons-builds\current-01' `
  --wall-seconds 600 --cpu-seconds 360 --memory-mib 2048
```

These are example allocations, not automatic retry allowances or promises of fit.
Require terminal success, clean enclosing process closure and actual
`_build/BUILD-RESULT.json`, package PROFILE and installation identities. The direct
recipe's cooperative limits are not a replacement for an enclosing hard process
envelope when one is required. Compiled hashes can differ by environment; this is
selected reproducible source input, not a bit-reproducibility or hermetic-toolchain
claim. Select the actual new PROFILE and independently approve that build before
using it. Do not silently open old owners or rebind host seals under changed support.

## Read results at their actual strength

| Result | What it establishes |
|---|---|
| Kit verification or input preparation | Selected bytes/layout or prepared inputs. |
| Find/preview/inspect | Bounded advertised information; not mathematical acceptance. |
| Name-directory lookup | An authenticated mapping or absence inside the selected historical export; no current-owner or global claim. |
| Complete formal display | Encoded type and legends fit the display limits. |
| Successful independent admission | Selected mathematics checked against the actual accepted context and policy. |
| Checked contribution | New selected work passed that checking path. |
| Publication | Selected retained targets entered the local index. |
| Host READY | This finite invocation reports a listener; not perpetual custody. |

The current software supports reciprocal mathematical development. It does not
guarantee novelty, useful relevance, complete global search or exponential growth.
Warm compatible knowledge, selective indexes and bounded operations are practical
scaling mechanisms; cold dependencies, coverage and sustained independent hosting
remain real costs. Public deployment still needs its licensing, security,
platform, operational and maintenance decisions. Those limits do not change
which local claims the current checker accepts.
