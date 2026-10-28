# Current local candidate: advisory search without proof-snapshot reads

Root adopts [OUTCOME.md](OUTCOME.md), SHA-256
`4dec0160ff66a0a7d11283fdf5c62004046d34d3461f638e9d72b651471e6269`.
The complete v5 goal remains active. Work remains local and unpublished, with
license undecided.

Use this package and its matching [operator walkthrough](operator/START-HERE.md):

`experiments/v5-local-checks/advisory-query-assembly01/distribution/package`

Its exact PROFILE is
`135c182496294cb99d8553031b02c6ac19937848960e0711bedd5fe7e72ed828`.

`prepare-symbol-query` accepts familiar Lean names and a selected recorded local
context. It checks the catalog metadata without reading retained theorem-proof
snapshots or opening custody. Its report explicitly distinguishes recorded name
bindings from a context ready for proof use. Ordinary mathematical acceptance
retains the existing snapshot and native checks.

Four focused control groups, file-only assembly and one actual query passed with
clean closure. The query produced exactly the earlier Context binding and search
features. The matching operator kit consumed its report and prepared the identical
previously tested find configuration; no live search was repeated. These three
supervised operations used 3.625 known CPU seconds, excluding preparations and
development work. This is not a measured search or research speedup.

The package changes five files and adds the advisory helper relative to the
tested original current build; 149 files, including all native/core payloads,
are unchanged. No native rebuild or state migration was needed. Existing reports
retain their original PROFILE and must not be relabeled. The source reconstruction
recipe is [build.py](build.py), with exact [source-map.json](source-map.json);
the reviewed auxiliary-map change has not been subjected to another native build.
The executed [assembler](assemble.py) uses the original current build receipt.

Selected lineage metadata processing and package/runtime validation remain.
This optimization does not establish sublinear cold metadata lookup, complete
global discovery or useful mathematical growth. It removes one unnecessary
proof-data cost from search preparation while preserving its advisory status.
