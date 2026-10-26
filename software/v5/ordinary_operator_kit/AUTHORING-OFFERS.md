# Advertise an ordinary Lean project for further investigation

Use this optional route when a discovered definition or theorem has an ordinary
Lean/Lake project that you are authorized to disclose. The product already
supports it; the kit's `serve` request intentionally covers a smaller subset.
This addendum uses the existing public command, not a new helper or package.

Start with the [operator guide](START-HERE.md) and, for an explicitly selected
compatible package, [package selection](SELECTED-PACKAGE.md). Source project
retrieval/execution and mathematical acceptance are separate decisions. The
lookup only returns advisory locations: it never downloads or executes them.

## 1. Select exact mathematics and the project claim

Finish the existing approved-project `produce-baseline`, independent intake and
publication workflow. Select the **terminal command report** from the launcher's
`child/stdout.txt`, with `ok: true`, `operation: produce-baseline`, the selected
profile and `result.status: PRODUCED_INERT_BASELINE_NOT_ACCEPTED`. Do not substitute
launcher `RUN.json` or intermediate `PRODUCTION.json`. Select a particular
published `result.targets[i]`; the index is your explicit choice.

Prepare a map draft in a new owner-controlled file, for example
`C:\commons-work\authoring-map.draft.json`. Its fields are:

| Map field | Value to select |
|---|---|
| `schema` | `DMKN_AUTHORING_OFFER_MAP_V1` |
| `entries[j].semantic_id` | Terminal producer `result.semantic_id` |
| `entries[j].export_id` | Selected `result.targets[i].export_id` |
| `entries[j].offers[k].export_name` | Selected `result.targets[i].name`, copied as the structured JSON name |
| `entries[j].offers[k].module` | Actual structured logical Lean module selected from the approved project/build, not guessed from a declaration prefix |
| `entries[j].offers[k].repository` | Explicitly approved credential-free HTTPS repository URI |
| `entries[j].offers[k].object_format` | `sha1` or `sha256`, matching that repository |
| `entries[j].offers[k].commit` | Full lowercase 40- or 64-hex revision respectively; not a branch or tag |
| `entries[j].offers[k].project_dir` | Repository-relative project directory; empty for the repository root |
| `entries[j].offers[k].toolchain` | Actual asserted toolchain token, for example `leanprover/lean4:v4.34.0` |

`entries` and `offers` are arrays. Each offer has exactly the seven fields above
from `export_name` through `toolchain`; each entry has exactly `semantic_id`,
`export_id`, `offers`. The map has exactly `schema`, `entries`. The existing
[codec specification](../ordinary_authoring_offers/CODEC.md) gives all bounds and
syntax constraints; the [public API](../ordinary_authoring_offers/API.md) explains
the assurance boundary. Do not copy the synthetic example's dummy repository or
commit as a real project location.

The producer report does not prove which Git revision produced the compiled
inputs, identify the correct repository-relative directory, or approve disclosure.
Obtain those values from the actual project/build you chose. Local compiled
search paths are **not** repository-relative `project_dir` values. A structured
Lean name is an array, not a dotted string. Do not rename logical modules merely
to fit a path: that can change generated declaration/export identities.

Approve disclosure of the map separately from custody disclosure: repository
names and revisions may themselves be private. Do not publish a repository or
claim unavailable source just to fill these fields. A provider may offer no hints.
Even a correctly copied report/hash does not authenticate its writer, prove the
project association, or make linked executable code safe.

## 2. Save the canonical map without changing prior files

The map must be canonical UTF-8 JSON: sorted keys, compact separators, no BOM,
no trailing newline, duplicate keys, floating-point numbers or nonfinite values.
Pretty-printed UTF-8 JSON without a BOM is suitable for the **draft**, not the
served map.

The following optional PowerShell snippet reads one explicitly chosen local JSON
draft and writes a **new** canonical file. It imports no product code, starts no
product operation and validates encoding only, not the offer schema or its claims.
Use owner-controlled ordinary paths, outside package contents and protected state;
this small snippet is not a hostile-filesystem sandbox. Its output parent must
already exist. Keep any partial output after an I/O failure; do not overwrite it.

```powershell
$jsonCanonicalize = @'
import hashlib, json, pathlib, sys
def reject_number(value):
    raise ValueError('Floating-point and nonfinite values are forbidden')
def unique_pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError('Duplicate JSON key: ' + key)
        result[key] = value
    return result
source, output = map(pathlib.Path, sys.argv[1:])
if not source.is_absolute() or not output.is_absolute():
    raise ValueError('Use explicit absolute paths')
with source.open('rb') as stream:
    raw = stream.read(2097153)
if not 0 < len(raw) <= 2097152:
    raise ValueError('Draft exceeds the 2 MiB bound or is empty')
value = json.loads(raw.decode('utf-8'), object_pairs_hook=unique_pairs,
                   parse_float=reject_number, parse_constant=reject_number)
encoded = json.dumps(value, sort_keys=True, ensure_ascii=False,
                     separators=(',', ':'), allow_nan=False).encode('utf-8')
if not 0 < len(encoded) <= 2097152:
    raise ValueError('Canonical file exceeds the 2 MiB bound')
with output.open('xb') as stream:
    stream.write(encoded)
print(hashlib.sha256(encoded).hexdigest())
'@
& 'C:\tools\Python314\python.exe' -I -S -B -c $jsonCanonicalize `
  'C:\commons-work\authoring-map.draft.json' `
  'C:\commons-work\authoring-map.json'
if ($LASTEXITCODE -ne 0) { throw 'Canonicalization failed; inspect retained files.' }
```

Record the printed SHA-256. The snippet does not alter the draft. It refuses an
existing output by using exclusive creation. Do not use `Out-File` or append a
newline to the resulting map. The product will independently hash and validate
the selected map before it starts serving.

## 3. Select a fresh serve configuration

Review a normal kit-prepared `serve` config for the existing index/custody, then
copy its complete contents into a **different fresh draft**, for example
`C:\commons-work\serve-with-authoring.draft.json`. Add this one optional field,
replacing the hash with the actual value from step 2:

```json
"authoring_offers": {
  "path": "C:\\commons-work\\authoring-map.json",
  "sha256": "REPLACE_WITH_THE_MAP_SHA256"
}
```

Retain every ordinary serve field; this fragment alone is not a valid config.
Select a finite lease and cleanup reserve (for the example below, 60 and 15
seconds), explicit endpoint/TLS policy, existing index, and service limits.
`share_all_custody: true` and `exclusive: true` disclose the entire addressable
selected custody and require exclusive owner use, not only the mapped theorem.

Use the same snippet with the new draft and a new output path
`C:\commons-work\serve-with-authoring.json`; record its distinct SHA-256. Do not
edit the kit's original `config.json`, `arguments.json` or `RECEIPT.json`, and do
not reuse their config hash. This manual configuration has **not** been prepared
or validated by the kit; the public product performs its own checks.

## 4. Launch the existing public command with explicit arguments

Replace the profile, state/limits paths and store ID with your approved existing
installation and exact initialized owner. The config/hash below refer to step 3.
The output and diagnostics directories must be fresh, with existing ordinary
parents. Do not start other commands using that owner during service.

```powershell
$servePython = 'C:\tools\Python314\python.exe'
$servePackage = 'C:\commons\package'
$serveProfile = 'REPLACE_WITH_APPROVED_PROFILE_SHA256'
$serveConfigHash = 'REPLACE_WITH_NEW_SERVE_CONFIG_SHA256'
$serveStoreId = 'REPLACE_WITH_EXISTING_64_HEX_STORE_ID'
$serveTokens = [string[]]@(
  'serve',
  '--catalog', 'C:\commons-work\catalog-a',
  '--custody', 'C:\commons-work\custody-a',
  '--store-id', $serveStoreId,
  '--custody-limits', 'C:\commons-work\prepared-serve-01\custody-limits.json',
  '--config', 'C:\commons-work\serve-with-authoring.json',
  '--config-sha256', $serveConfigHash,
  '--output', 'C:\commons-work\serve-with-authoring-output-01'
)
& $servePython -I -S -B "$servePackage\run.py" `
  --profile-sha256 $serveProfile `
  --python-runtime 'C:\tools\Python314' `
  --lean-runtime 'C:\tools\lean-4.34.0-windows' `
  --diagnostics 'C:\commons-work\diagnostics-serve-with-authoring-01' `
  --wall-seconds 180 --cpu-seconds 120 --memory-mib 1280 `
  --active-processes 6 --stdout-bytes 8388608 --stderr-bytes 1048576 `
  peer -- @serveTokens
```

These are example finite ceilings, not a promise that setup and service fit.
Runtime/profile approval is independent of this recipe. The launcher supplies
the peer's runtime/profile/resource flags; do not repeat them inside `serveTokens`.
No shell command is built from a returned repository URL or declaration name.

A separate client uses the existing `authoring-offers` kit action after preview.
Wait for the service output's `READY.json` and use its actual host/port/TLS
selection, particularly when port 0 was requested. A failed service or lookup
does not authorize retry, grant renewal or global-absence conclusions. Let the
lease finish; inspect terminal diagnostics before reusing the owner.

The service snapshots the selected map once; changing the file does not change
that running snapshot. Returned associations are still
`UNVERIFIED_AUTHORING_ASSOCIATIONS`. A recipient must independently approve any
source retrieval/execution, export the chosen compiled project and compare its
exact semantic/name/unit/export bindings with the desired mathematics, then
independently admit contributed results. Source hints enable a practical handoff;
they do not establish source availability, mathematical novelty or faster growth.
