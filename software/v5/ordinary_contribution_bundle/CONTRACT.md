# Send new contribution bytes to an inert host

This offline companion turns the public result of `owner contribute` or
`owner complete` into the existing ordinary bundle format. It preserves every
returned complete unit, including new helper definitions and completion support
units, in its original order. It does not rerun Lean, reopen the author, read
databases, traverse old dependencies, or publish to a host.

Use the selected Windows Python with the approved kit's package and its exact
PROFILE hash. Only five fixed, hash-checked inert codec sources execute; no Lean
runtime is needed. The companion does not authenticate the rest of the package
or validate native artifacts. It has a single cooperative 60-second wall /
30-second controller-CPU allowance; hard process containment is separate.

## Prepare the handoff

Copy the author's public helper `RESULT.json` and its `evidence/` directory to
the host machine, or explicitly select the outer owner report containing that
result. Select the report's exact SHA-256. Historical profiles may differ; the
selected codecs check the portable semantic and evidence identities.

The helper status must be the recognized contribution or completion status. An
outer wrapper must match its operation to that result. Outer `ok`, cleanup errors
and profile are recorded as untrusted provenance: an `ok: false` wrapper may still
contain a complete durable result after a cleanup failure. This companion verifies
the selected bytes; it does not attest original success, closure or acceptance.
It cannot reconstruct missing unit lists or missing files from partial outputs.

Every unit is read only as `<chosen-evidence-directory>/<unit_id>.json` after
validating its identifier. The report's `file` paths are never followed. Its
byte count and SHA-256 must match the exact local evidence; each target must be
an actual named output of its selected unit with the matching ExportID. All
listed units are retained, even if none of the selected targets names them.
There is no target-filter mode and no older-corpus search.

The following PowerShell example contains illustrative paths and invalid hash
placeholders. Replace them with explicitly selected local paths and hashes:

```powershell
$handoffPython = 'C:\approved-python\python.exe'
$handoffKit = 'C:\commons-kit'
$handoffPackage = 'C:\commons-kit\package'
$handoffProfile = 'REPLACE_WITH_APPROVED_PROFILE_SHA256'
$handoffReport = 'C:\commons-work\returned\RESULT.json'
$handoffReportHash = (Get-FileHash -LiteralPath $handoffReport -Algorithm SHA256).Hash.ToLower()

& $handoffPython -I -S -B "$handoffKit\contribution\project.py" `
  --package $handoffPackage --profile-sha256 $handoffProfile `
  --report $handoffReport --report-sha256 $handoffReportHash `
  --evidence-directory 'C:\commons-work\returned\evidence' `
  --output 'C:\commons-work\publication-bundle01' `
  --share-all-bundle --allow-partial-publication
```

The two flags are required. They explicitly approve sharing **all** supplied
unit bytes and export locators, including unindexed declarations, and the host's
existing rule that committed prefixes may be served if a later append step fails.
No approval is inferred from the author's report.

The output must be a fresh directory with an existing parent, disjoint from the
selected package, report, evidence directory and companion source directory.
Input paths must be ordinary local paths with no links or reparse points. Limits
are 32 complete units, 4 MiB total evidence and 32 targets, with existing finite
node/name/import ceilings and 2 MiB limits for each metadata file. Report-selected
paths, code, limits or evidence beyond the listed units are never used.

Successful preparation writes:

- `units/<unit_id>.json`: exact original evidence bytes, with no reserialization.
- `manifest.json`: the existing ordinary baseline bundle manifest.
- `append.json`: the existing incremental-host append configuration and all
  selected target rows, with the explicit disclosures and lowered bundle limits.
- `PREPARATION.json`: input/output pins, counts, provenance and the inert boundary.

Use the public launcher and existing host instructions to append this bundle.
Select the host root and its stable descriptor hash separately, and pass the
exact `append.json` path/hash. The projector never opens or verifies that host.
Host append regenerates previews, verifies its own inputs and writes its normal
custody/index records. Receiver mathematical checking remains separate.

`append.json` contains absolute paths local to this projection. Prefer running
the projector on the host over copied report/evidence files. If you instead
transfer the prepared bundle, explicitly replace `bundle_directory` and
`manifest.path` with the new local paths and pin the resulting append config.
The manifest and evidence bytes remain unchanged. Copying the old config alone
does not relocate its paths.

## Availability and failure boundaries

The bundle is an inert claim, never acceptance or a guarantee of dependency
availability. Consumers may already warrant its imports or acquire them from
existing providers. If required older evidence exists only in a disappearing
author store, select its retention/transfer separately through existing public
return/export mechanisms. This companion does not reexport that history on each
new addition. It does not reduce upstream authoring/context/admission costs or
establish a useful-growth speedup.

Validation precedes creating the output where possible. Writes use fresh files,
flush/readback and existing manifest/batch validation. Any failure retains partial
output; a manifest or receipt may exist despite a late failure. No overwrite,
deletion, retry, rollback or renewed allowance occurs automatically. Preserve
the actual command outcome and inspect any retained files before selecting a new
operation. Preparation success is not host publication. A later host append can
leave permitted committed prefixes; follow the existing host failure contract.

The callable API is
`project_selected(package, profile_sha256, report, report_sha256, evidence_directory, output, *, share_all_bundle=False, allow_partial_publication=False)`.
Paths may be absolute strings or `Path` objects. Both booleans must be true. It
returns the saved preparation receipt with status `INERT_PUBLICATION_BUNDLE_PREPARED`.
The API imports no native runtime and temporarily loads/restores only the five
pinned inert codec module slots. Callers must serialize source/input mutations
and concurrent use of those import slots; the CLI is an isolated single invocation.
