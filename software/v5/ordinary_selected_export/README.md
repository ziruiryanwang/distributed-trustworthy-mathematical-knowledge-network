# Export selected mathematics without reopening a producer project

This separate companion copies exact mathematical data from an existing local
ordinary custody into the existing portable baseline-bundle format. It follows
the selected targets' complete dependency closure, preserving every evidence byte
and identity. It does not run Lean, load a project, serve your custody, access a
mathematical owner/catalog or check any proof.

Use it to move relevant work offline, populate a deliberately small new checked
context, or prepare a separate disclosure-approved serving store. If you already
have an exact retained bundle containing the desired closure, use that instead.
This companion does not replace or modify the default package or its archives.
Source review and any actual tests are recorded separately; this guide is not
evidence of a successful execution or full v5 release.

## What gets copied

Select exact `{name, export_id, unit_id}` records from retained investigator
outputs. `name` is the existing structured Lean name, not a dotted-name guess.
The exporter follows **all declared imports**, including proof-only imports,
until the exact fixed basis. Atomic groups are indivisible: their other outputs
are copied too. It cannot decide a mathematically minimal set of assumptions.
Inspect the selected dependency content before sharing it.

Data in custody need not have passed mathematical checking. The exporter checks
structure, exact identities and dependency consistency, not truth. A structurally
valid false claim can be exported. The result deliberately states
`mathematical_acceptance: false` and `source_acceptance: "UNASSERTED"`.
Only a subsequent independently successful receiver admission supplies a warrant.

## Prepare one explicit request

Use the supported approved Windows x86-64 Python 3.14.6 and default package
described in `../ordinary_release_bundle/ADOPTION.md`. Keep this companion
outside the hash-bound package. Independently approve its two code files and
the package/runtime; matching a hash by itself is not code approval.

Save one UTF-8 JSON request with exactly these fields:

| Field | Meaning |
|---|---|
| `schema` | `DMKN_SELECTED_INERT_EXPORT_REQUEST_V1` |
| `custody` | Absolute existing custody directory containing `ordinary.sqlite` |
| `targets` | 1–64 exact target records, at most 65,536 encoded bytes |
| `output` | Absolute absent output directory; its parent must exist |
| `custody_limits` | The store's original exact `objects`, `exports`, `logical_bytes`, `db_pages` limits; not new limits to increase its capacity |
| `limits` | The eight explicit collector/output limits below |

Collector maximums are:

```json
{"units":1024,"bytes":67108864,"nodes":2097152,"names":65536,"edges":262144,"locator_reads":65536,"locator_bytes":67108864,"output_bytes":71303168}
```

Choose smaller positive values where appropriate. These are refusal ceilings,
not promised capacity or default permission to spend every resource. Locator
reads and bytes are separately charged. Whole-unit batching retains existing
baseline-format bounds. No proof/module/custody limit is enlarged.

Source, output, package, runtime, request, companion and diagnostics paths must
obey the existing ordinary-path/protected-filesystem conditions. Output must not
overlap any selected input or state. Use fresh diagnostics and output directories;
no retained failure is overwritten or silently retried.

## Run one bounded export

The entry accepts only a fixed export worker, not arbitrary commands. The example
below has placeholders that must be replaced with actual approved paths/hashes.
It is an example invocation, not an operation already executed here.

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B 'C:\commons-export\export.py' `
  --package 'C:\commons-builds\transport\package' `
  --profile-sha256 'APPROVED_PACKAGE_PROFILE_SHA256' `
  --python-runtime 'C:\tools\Python314' `
  --entry-sha256 'APPROVED_EXPORT_PY_SHA256' `
  --helper-sha256 'APPROVED_SELECTED_EXPORT_PY_SHA256' `
  --request 'C:\commons-requests\export.json' `
  --request-sha256 'APPROVED_REQUEST_SHA256' `
  --diagnostics 'C:\commons-requests\export-diagnostics-01' `
  --wall-seconds 60 --cpu-seconds 30 --memory-mib 512 `
  --active-processes 1 --stdout-bytes 1048576 --stderr-bytes 1048576
```

The finite supervisor may refuse or terminate work. It performs no automatic
renewal. Review its actual completion and cleanup reports, not only a success
phrase or the existence of an output file.
The Windows Job CPU/memory/process limits apply to the one worker. The parent
wrapper checks and reports its own CPU separately; these are not one combined
process-tree CPU/memory ceiling. The original wall deadline covers both stages.

The helper opens SQLite with `mode=ro`, `query_only=ON` and one bounded read
transaction. It refuses journal/WAL/SHM states rather than repairing the source.
A busy source can refuse; its read snapshot may temporarily delay cooperative
writers. No `immutable=1` bypass is used. This does not protect against a hostile
same-account process replacing files or turn an arbitrary hostile SQLite file
into an approved input. Restore a damaged store through its separately approved
recovery workflow, not by editing this export's pins or deleting its journals.

## Inspect, move and independently check

Successful output contains `units/<unit_id>.json`, the existing `manifest.json`,
and terminal helper `RESULT.json` with exact targets, manifest pin and bounded
census. The helper writes RESULT last, but a later budget/cleanup failure can
still leave it present. Require the enclosing operation's successful clean
closure and exact output checks too. Partial outputs remain on failure.
Helper timing fields end before writing its own terminal report; use the enclosing
supervisor's accounting for whole-operation costs rather than adding intervals.

The portable input is the manifest plus all its exact unit files. The helper
RESULT is local operational evidence, contains the source custody path, and is
not required by receiver intake. Do not mistake copying that report for proof
acceptance. You may keep it private when transferring only the inert bundle.

At the destination, use existing explicit `owner intake-baseline` with its
receiver-local parent root, bundle directory and exact manifest hash. The ordinary
producer-report preparation convenience does not accept this report; use the
underlying direct route, never relabel it as producer or admission evidence.
Receiver initialization/intake still require their normal approved runtime,
bounded local checking and successful terminal results.

After admission, selected targets can be published and a finite service can be
started explicitly. **Publication selects advertisements, not read permissions.**
Ordinary serving exposes the entire addressable serving custody, including
unindexed or not-yet-accepted retained inputs. Use a separate disclosure-approved
custody for public service; do not serve the mixed private investigation store.
Neither export nor TLS provides collaborator-only reader authorization.

This is offline portability, not automatic replication, availability guarantees,
free cold verification, novelty, measured useful-growth acceleration or permission
to publish externally. Everything in the present project remains local and
unpublished, with licensing undecided.
