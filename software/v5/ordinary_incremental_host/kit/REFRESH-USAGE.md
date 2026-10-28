# Maintain specialist contacts through existing provider feeds

This companion describes the exact registration-refresh package assembled under
PROFILE `e8d33500db4c0a5ce89b2dfb51c3e1f9ec8f12063bbc58fe5e4eb23c2b6dfb13`.
Its installation manifest remains
`9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27`.
The selected package is the `package/` directory of this kit. This is an additive
usage companion; earlier adopted kits remain unchanged. Assembly identity is
not a claim of independent public deployment or final-v5 completion. The project
remains local and unpublished, with license undecided.

The workflow is: a provider serves its own contact feed; a registrar refreshes
approved feed/route slots and serves their bounded union; readers use the existing
`directory-find` command. Mathematical publication, custody, checking and reuse
keep their current interfaces. The registrar performs no proof work and never
dials the mathematical endpoints it learns.

## Choose routes from real shared-symbol queries

Use a successful retained `SPECS.json` from the existing symbol query or historical
name-directory lookup. An investigator can start with a familiar carrier such as
`Std.HashMap`, without knowing a desired theorem name or full statement. The
earlier six-result finite-map workflow demonstrated this route; it did not prove
general relevance, complete search or a research speedup. No example corpus is
bundled and no completed experiment needs to be repeated.

If you already have an approved historical name directory, the unchanged offline
lookup is available in this package. First set the runtime/package variables in
the next section, then replace the explicit choices below. The
catalog's `shared_symbol_names_example` is the exact name `Std.HashMap`; save that
array alone as `names.json` only if it belongs to your selected directory.

```powershell
& $refreshPython -I -S -B "$refreshPackage\lookup_directory.py" `
  --profile-sha256 $refreshProfile `
  --directory 'C:\REPLACE_WITH_APPROVED_NAME_DIRECTORY' `
  --directory-sha256 'REPLACE_WITH_ACTUAL_DIRECTORY_MANIFEST_SHA256' `
  --symbol-names 'C:\commons-work\names.json' `
  --output 'C:\commons-work\lookup-fresh01'
```

Use `SPECS.json` only after complete success; missing names suppress it. This
is historical advisory name resolution, not present owner validation. A current
context symbol query remains another supported source of specs; follow the
kit guide with this exact package's direct launcher. When using the offline
preparer, use the matching `operator/` files from this kit together.

Choose one selective route array. Use exactly that array for the provider feed's
entry, the registrar slot and the reader's route. The reader's full query can
append `{"tag":"declaration-kind","value":"theorem"}` and
`{"tag":"object-kind","value":"ordinary-lean-export-v2"}` where useful, up
to eight specs total; every route feature must remain in the full query. Several
symbol specs mean conjunction, not synonyms. Never invent an export/symbol hash
or use a printed name where the API expects an exact portable symbol.

## Prepare three direct configs

[REFRESH-REQUESTS.json](REFRESH-REQUESTS.json) contains `provider_feed`, `registrar`
and `reader` config objects plus their actual operation names. Copy the selected
object alone, fill required nulls, and save UTF-8 JSON without a BOM. The paired
null CA fields intentionally select system trust for a known contact. The
catalog is not an operator-preparer request and must not be submitted wholesale.

Set these variables to your approved Windows x86-64 Python 3.14.6 / Lean 4.34.0
runtime distributions and exact selected package. The Lean runtime is still
verified by the loader; these three operations invoke no Lean compiler/checker.

```powershell
$refreshKit = 'C:\commons'
$refreshPackage = Join-Path $refreshKit 'package'
$refreshPythonRoot = 'C:\REPLACE_WITH_APPROVED_PYTHON_3_14_6_ROOT'
$refreshLeanRoot = 'C:\REPLACE_WITH_APPROVED_LEAN_4_34_0_ROOT'
$refreshPython = Join-Path $refreshPythonRoot 'python.exe'
$refreshProfile = 'e8d33500db4c0a5ce89b2dfb51c3e1f9ec8f12063bbc58fe5e4eb23c2b6dfb13'
$refreshCatalog = Get-Content -Raw -LiteralPath "$refreshKit\REFRESH-REQUESTS.json" | ConvertFrom-Json
$refreshRoute = @(Get-Content -Raw -LiteralPath 'C:\REPLACE_WITH_SUCCESSFUL_QUERY\SPECS.json' | ConvertFrom-Json)
$refreshConfig = $refreshCatalog.configs.registrar
$refreshConfig.slots[0].specs = $refreshRoute
# Fill feed origins, scopes, service address and actual TLS-file pins before saving.
$refreshConfigFile = 'C:\commons-work\registrar-config01.json'
if (Test-Path -LiteralPath $refreshConfigFile) { throw 'Choose a fresh config filename.' }
[IO.File]::WriteAllText($refreshConfigFile,
  ($refreshConfig | ConvertTo-Json -Depth 64), [Text.UTF8Encoding]::new($false))
```

The public templates use HTTPS on port 443. The provider-feed config's listener
is the **feed service**; its `entries[].endpoints` are separately running
mathematical index/custody services. The registrar's `contacts.provider-a` points
to the feed. The reader's `contacts.community` points to the registrar. All
advertised endpoints must use the selected namespace and compatible services;
a contact hint does not establish that relationship or availability.

For each feed, approve exact routes and either allowed mathematical-service TLS
names or exact endpoint rows. `endpoint_scopes.tls_names` contains the
mathematical service's certificate name, not the feed's or registrar's name.
Scope and egress both apply. Feed-origin or topic changes need a deliberate
policy edit; allowed provider endpoint changes do not need a registrar edit.
For any route the sum of slot `max_contacts` values must be <=16. Refresh request
and byte budgets must cover all selected slot reservations, including failures.

For a deliberate local-only run, choose distinct loopback ports for feed,
registrar and mathematical service; use host `127.0.0.1`, `tls:false` and
`server_name:null` in contact rows and `tls:null` for listener TLS. Set both
registrar and reader egress to `mode:"loopback-test"`, `public_ports:[]`, and
`test_endpoints:[{"host":"127.0.0.1","port":YOUR_MATHEMATICAL_SERVICE_PORT}]`.
Use `tls_names:[]` plus the exact four-field mathematical endpoint in the feed
scope. These are explicit local choices, not a live example or public deployment.

## Run one finite cycle

1. Have the selected mathematical provider already published and serving under
   its existing finite owner/dedicated-host procedure. Contact services do not
   publish mathematics or start that provider.
2. In the provider's terminal, run `peer -- directory-serve` with its filled
   provider-feed config. Wait for this invocation's `READY.json` while it is
   still active. The provider can change its own feed config in a later cycle.
3. In the registrar's terminal, run `peer -- directory-refresh-serve` with its
   approved policy/config. Inspect its current `READY.json`; if no contacts
   survived, the operation returns without listening. A READY file from an old
   cycle is not evidence that a listener is still alive.
4. While registrar and mathematical service are active, run the unchanged
   `peer -- directory-find` using the reader config. Inspect returned candidate
   previews, then explicitly select any acquisition/checking/reuse through the
   established ordinary workflow. A routing result never accepts mathematics.
5. Preserve each final `RESULT.json` and launcher diagnostics. Require successful
   closure and the server's `quiescent:true` with no cleanup errors before the
   next selected cycle. New cycles use fresh output/diagnostic leaves and new
   explicit allowances; no scheduler, automatic retry or hidden renewal is added.

The command shape is identical for these operations. Run it on the appropriate
operator's computer, changing the operation/config/output paths for that step:

```powershell
$refreshConfigHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $refreshConfigFile).Hash.ToLowerInvariant()
& $refreshPython -I -S -B "$refreshPackage\run.py" `
  --profile-sha256 $refreshProfile `
  --python-runtime $refreshPythonRoot --lean-runtime $refreshLeanRoot `
  --diagnostics 'C:\commons-work\registrar-launch01' `
  --wall-seconds 180 --cpu-seconds 60 --memory-mib 512 --active-processes 3 `
  --stdout-bytes 1048576 --stderr-bytes 1048576 `
  peer -- directory-refresh-serve --config $refreshConfigFile `
  --config-sha256 $refreshConfigHash --output 'C:\commons-work\registrar-result01'
```

Use `directory-serve`/`directory-find` instead for the provider/reader steps.
Every output and diagnostics leaf must be absent with an existing ordinary
parent; keep configs and outputs outside the protected package. Omit catalog,
custody, store-id and custody-limits: these three operations are state-free.
The example ceilings include setup/cleanup but are not performance promises.
Select sufficiently overlapping service intervals; the displayed template has
a 90-second feed lease and at most a 60-second registrar lease.

## Read partial results and expiry correctly

The complete peer `RESULT.json` has wrapper `ok` and a nested `result`. Check both
the wrapper and nested status. Registrar `result.lookups` distinguishes empty,
truncated, rejected, unavailable and too-old slot outcomes. `refresh_complete`
only means all selected slots yielded usable untruncated unrejected metadata;
it does not mean global completeness, relevance or current provider truth.
`INCOMPLETE_REFRESH_SERVICE_FINISHED` can still have served useful allowed rows.
`REFRESHED_EMPTY`/`INCOMPLETE_REFRESH_EMPTY` open no listener. On failure, inspect
the preserved `detail` and nested service cleanup rather than treating it as an
empty answer. Reader matches remain bounded incomplete search results.

Every refresh starts from fresh nonce-bound responses; failed feeds have no
cached fallback. A provider can remove a route from its next feed map while
other routes remain, making that route return empty. The static feed command
requires at least one entry: withdrawing every route means stopping that feed,
which is reported unavailable, not falsely as a valid empty response.

`max_age_ms` starts at each registrar request's local monotonic time. Slow
responses spend it. The registrar omits slots lacking `min_service_ms`, clips
its service to the earliest contributing horizon, and refuses READY after a
startup that leaves too little time. Dispatch and enqueue checks stop issuing
new contact bytes at that cutoff under the execution assumptions. Already
queued bytes can arrive later; readers keep their existing contact-use horizon.
This is no immediate revocation or liveness guarantee. A live feed can freshly
repeat stale claims. The templates and field explanations above give the finite
configuration bounds; the installed command validates them before requests.
