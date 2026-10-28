# Resolve new names without repeatedly reopening a library

Use this optional route when you expect many different name queries against a
large stable local library. Existing saved specs are cheaper if you only repeat
the same query. Exporting after every small addition defeats the amortization.

This capability is tested in the local development package at
`experiments/v5-local-checks/name-directory-assembly01/distribution/package`.
Its PROFILE is `7687d5276d8a7edc0beeb7066e4cbaae16529b0e88d8a0728b003dad04a4dd34`.
The single current complete kit remains separately adopted; this note does not
relabel its older operator companion or introduce an alternative installation.

## Export once

Through the selected package's existing bounded run.py launcher, use query with:

```text
--catalog <existing-catalog> --store-id <exact-store-id>
--context-root <selected-root> --directory-export v1 --output <fresh-directory>
```

Supply the usual approved profile/runtimes, finite budgets and fresh diagnostics.
Do not supply custody, a native type or a name list. Inspect the complete successful
report and clean closure. Retain its directory_manifest_sha256 independently.
Construction validates the entire selected metadata once under the normal owner
lifecycle; it reads no proof snapshots and runs no Lean worker. It writes all
bindings and the final DIRECTORY.json commitment. A failed export is retained.

## Look up independently selected names

Save one through eight exact structured names as canonical JSON. The format is
the same as the existing symbol-query input; a dotted spelling is not a substitute
for its structured name. For example, `MyTheory.Closure` is:

```json
[[[0,{"$bytes":[77,121,84,104,101,111,114,121]}],[0,{"$bytes":[67,108,111,115,117,114,101]}]]]
```

Run isolated Python directly against the selected package's lookup_directory.py:

```text
python.exe -I -S -B <package>/lookup_directory.py
  --profile-sha256 <selected-package-profile>
  --directory <completed-export>
  --directory-sha256 <approved-DIRECTORY.json-sha256>
  --symbol-names <canonical-name-list.json> --output <fresh-result-directory>
```

This opens no owner, service, Lean worker or proof snapshot. It authenticates
only the final selected records or adjacent absence bounds, using logarithmic
fixed-size reads. The source/manifest/name parsing is additional bounded work.
If every requested name is present, the result includes SPECS.json. Supply its
array as explicit `specs` to a compatible ordinary find request. This is a
conjunction, not several independent searches. Any missing name suppresses specs.

Do not pass the new report as an old `query_report`, change a report's PROFILE,
or treat it as permission to import a theorem. Current find and recipient checks
still apply. The optional directory preserves old exact symbol choices across
compatible auxiliary package changes; it does not certify current owner activity.

## What the commitment means

The manifest must come from an approved successful complete export. A foreign
manifest that merely names a real root does not establish its relationship to
that root. Under this origin premise and hash resistance, point authentication
protects the old name mapping even if directory payload storage later changes.
Corrupt or incomplete proof paths refuse; they do not become missing names.

An absence concerns this historical directory only. Newer roots can have new
names; source withdrawal and deletion are not reflected automatically. A missing
name is not evidence that mathematics is absent from the network. No directory
result grants mathematical acceptance or semantic equivalence between names.

The actual 3,511-name export and a 1,216-byte positive payload lookup establish
the implemented access path, not global-scale timings or useful-growth speedup.
The source argument is O(N log N) initial sorting plus metadata validation and
O(log N) fixed-size reads/hashes per name afterward, with linear directory space.
