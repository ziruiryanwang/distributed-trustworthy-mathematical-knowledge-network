# Compact source handoff

This local handoff removes the historical research workspace from the source
acquisition/build workflow. It does **not** complete v5 or establish faster
mathematical growth. Nothing was published externally; licensing is undecided.

## Use the artifact

- [Source ZIP](../../../experiments/v5-local-checks/source-bundle-controls01/suite/packed/source.zip)
- [External exact receipt](../../../experiments/v5-local-checks/source-bundle-controls01/suite/packed/RECEIPT.json)
- [Build and use guide](README.md)
- [Already extracted source](../../../experiments/v5-local-checks/source-bundle-controls01/suite/relocated-source/software/v5/ordinary_source_bundle/README.md)

The ZIP is **3,195,785 bytes (3.05 MiB)**: 105 source/document payloads plus one
manifest. Source payloads total 3,161,906 bytes. It contains the unchanged baseline
build inputs, fair-search overlay, operator kit and the new file-only bundle tool.
It excludes runtimes, native outputs, private state and historical experiments.

ZIP SHA-256:
`b2305a8241e6892e8ce01a3418e7284c1ed418e53ec78c5f1b0ca583484e8b3b`

Manifest SHA-256:
`e2eba82a5626c0a0b753391ffba777c197d4a37099a8645845c4cfa73303e6f2`

Use the approved complete Windows x86-64 Python 3.14.6 and Lean 4.34.0 runtimes
separately. The guide connects the existing build, file-only fair overlay and
selected-package operator entry. File hashes identify bytes; select the utility
and hashes independently rather than treating a downloaded receipt as authority.

## What actually passed

One finite file-only run created the ZIP, extracted its exact known contents and
invoked the public verifier from that relocated tree. **19 required controls
passed.** Changed/missing/extra files, wrong manifest identity, overwrites,
malformed path aliases, duplicate JSON keys and actual hardlinked files refused.
The optional real symlink control was **not executed**: Windows denied symlink
creation with privilege error 1314. It is not counted as a passing check.

Independent saved-output inspection found zero source/archive/extraction
mismatches, 106 exact files and 29 expected directories. The public verifier was
reaped; no bytecode or extra extraction files appeared. All 105 original inputs
remained unchanged. See [source review](REVIEW.md) and [outcome audit](OUTCOME.md).

The single run took 5.1793463 seconds outer wall time and 1.46875 seconds inclusive
Job CPU plus 0.15625 runner CPU. Its original 90-wall/45-CPU-second, 512-MiB,
four-process envelope was not renewed. The Job closed with zero active or
terminated processes and no cleanup errors. No runtime remains.

There was no Lean compilation, product import, mathematical admission, external
network access or certificate production. Existing native-build evidence was
reused only for unchanged inputs; no new native build from this extraction is
claimed. The utility does not extract arbitrary ZIPs or sandbox hostile source.
Interrupted-write recovery was source-reviewed, not fault-injection tested.

## Continuation discipline

The utility, tests, input documents and actual outputs used here remain frozen.
The earlier [fair-search package](../ordinary_fair_search/ADOPTION.md) and all
state/evidence are unchanged. No Git index/commit or shared research-ledger
mutation was performed during this handoff; concurrent research work is preserved.

This closes source consolidation. Do not repeat the native build, test suite or
archive just to increase the number of checks. Select future implementation from
a concrete unserved investigator behavior or a justified consequence of the
separately owned growth study. Useful discovery/growth, hostile-code isolation,
public licensing and independent operational readiness remain substantive v5
requirements, not properties supplied by this small archive.
