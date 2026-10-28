# Actual flattened current-distribution build audit

Disposition: **PASS_SELECTED_SOURCE_BUILD_AND_ASSEMBLY**. The actual three-stage
build from the verified relocated source bundle closed cleanly and produced the
selected current package. This is build/provenance evidence, not a new owner,
mathematical acceptance, independent-host result or full-v5 release. Root owns
adoption and any next launch. This audit used only saved JSON/logs, source reads,
standard-library hashing and PE-header inspection; it did not import product
modules, compile, replay a build, open owner state or run native executables.

## Exact evidence

All paths below are relative to the canonical project root. The actual run is
`experiments/v5-local-checks/current-distribution-build01`, package is its
`distribution/package`, and build evidence is `distribution/_build`.

| Binding | SHA-256 |
|---|---|
| Exact used selection | `b08498d1a894b1bfb2dd61b0b42cd1e2e552a1f875a1223128d91e2c4134888c` |
| Builder | `d14f2910003b8f8bc36dacc50796b37f87befbc60de76fb9cb575e30e8ce9ef1` |
| Source map | `65fde356b8ce6146b07ab49fad40a859af5bf0ce32e8d7beea76e32da60a9c9e` |
| Outer RESULT.json | `7958c03291efcdb2f30e926959d02b841406c504e090d4b155a42e13c2538e88` |
| BUILD-RESULT.json | `08ef24292afc45b7cfae7075c0ea2231f45ea88e02cc05bca2dd263f95612863` |
| PROFILE.json | `d5e56dd3bb2d1a531abeaabf06aea1864a7037c88a2035749230574455d7d4b0` |
| INSTALLATION.json | `9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27` |

The selected source root is the actual
`current-source-bundle01/controls/relocated-source`, whose bundle/relocation audit
is `../ordinary_current_source_bundle/OUTCOME.md`. All 89 staged input files
(87 mapped sources plus builder and map) match their saved source pins and that
extraction. All 23 explicit runtime pins match the supplied runtime files. This
does not claim a hermetic toolchain. Outer stdout parses to the exact saved
BUILD-RESULT object; outer stderr is empty.

## Sources, compiler lanes and output map

The actual source lanes contain exactly 8 receiver, 13 authoring, 7 extractor
and 1 query modules. Every staged source matches its mapped input and independently
reconstructed transform. The four authoring public-header transforms preserve
their post-import bodies; the extractor's OrdinaryExport uses the selected
legacy-header transform. Receiver CheckedExtension/LocalSnapshot/worker use the
kernel-admission sources; authoring/extractor CheckedExtension use the separate
ordinary_lean source. The seven selected-core files match their selected origins,
including ordinary_parse_reuse/ordinary_admission.py.

The actual worker argv select these staged lanes, the pinned Lean runtime and
fresh object directories. The pinned worker source supplies fixed per-module
compiler arguments; child stdout records module/phase and exit code, rather than
separate full compiler argv. All expected records occur in exact order:

| Stage | Successful records | Wall seconds | Job CPU seconds | Total processes |
|---|---:|---:|---:|---:|
| Receiver + authoring | 21 module compilations | 27.7361859 | 27.484375 | 44 |
| Extractor | 7 codegens + 7 objects + 2 links | 12.9014405 | 14.0625 | 45 |
| Query | 1 module compilation | 0.9394190 | 0.859375 | 4 |

Each stage exits zero, reaps its direct child, closes its Job, has empty stderr,
no cleanup errors or termination request, and zero final active/terminated
processes. Stage grants decrease to 451/316, 423/289 and 410/275 wall/CPU seconds;
each retains the selected 2048 MiB/eight-process ceiling. The complete nested
Job CPU total is 42.40625 seconds. The builder reports 3.765625 controller CPU
seconds and 49.6941021 wall seconds before commit.

All 154 actual package files (39,513,394 bytes) exactly match BUILD-RESULT's full
map: 153 payloads plus PROFILE. PROFILE's 117 auxiliary entries and all eight
documentation entries match actual files. The package census is exactly the
union of those entries, the 27 packaged installation files, INSTALLATION and
PROFILE; the nine additional INSTALLATION runtime bindings are external.
All 72 direct-copy targets match the selected extracted sources. All eight
receiver outputs, 65 authoring outputs, two extractor executables and five query
outputs match their saved compiler-output maps and packaged bytes. All 23
extractor intermediate/output records were also independently hashed.

## Identity and comparison with adopted current package

The comparison baseline is
`experiments/v5-local-checks/frontier-launcher-package01/distribution/package`.
Both packages contain the same 154 paths. **151 payloads are byte-identical**,
including every direct target, every receiver file, all 65 authoring helper
outputs, all five query outputs, and INSTALLATION. Only these three files differ:

| File | Old SHA-256 | New SHA-256 |
|---|---|---|
| PROFILE.json | `efa1e0894a24859bf1c7648ccaf72674c7cf136c9fce32a62020e75cb24bcd45` | `d5e56dd3bb2d1a531abeaabf06aea1864a7037c88a2035749230574455d7d4b0` |
| authoring/bin/BaselineExporter.exe | `7ee4356f4cb2006950b5395a9d0618c6ce4432dafe22978da84332f5046f1ce7` | `cc37da1120c861984e1febd65f7ee4426cb94340dbf8f312647b16b8af55dca7` |
| authoring/bin/MissingImportExporter.exe | `df5d90d0ba006f2e4b3935d83cfb6713c2d7804bc2c166206250b13693dba873` | `a8f8fa1221a1831618c3940b2a850e3a5d7760920df28cb8d5c6874eadb2cf74` |

PROFILE's only semantic differences are the hashes of those two equal-length
executables. Each executable differs in exactly six bytes. Independent PE32+
header/section/RVA inspection places all differences inside two four-byte
timestamp fields: COFF TimeDateStamp at offset 128 and
IMAGE_DEBUG_DIRECTORY.TimeDateStamp at offset 578564 (BaselineExporter) or
544260 (MissingImportExporter). Both timestamp values change from 1793042794 to
1793204925. **Every byte outside these timestamp fields is equal.** No executable
code change follows from the fresh hashes.

Using the source-defined UTF-8 canonical JSON and domain-NUL hashing algorithms,
the audit independently reconstructed all five support digests from actual
verified installation files and the role/compiled-directory bindings:

| Support | Digest |
|---|---|
| kernel_support | `4b24f71f745205e151555ba0e8cf962ec7f26e7d67de5c5f640e089f38b61603` |
| adapter_support | `8f45c9fbd0780a6c4452e76498a4e5e506af4e22020c27f9563d01fcc4451bf0` |
| basis_receiver_support | `e606c461ed5bc8a074dc936b626617d7db65fb079fd2c7a0e0da7c0c6957c347` |
| controller_support | `ea7c4441de85a477c39394155a433b410e5605e935920a1090683254f0043333` |
| snapshot_support | `f32402a7a318a380918470ae51c851be4851cf0b714928ed6b4c8fd76652589b` |

The reconstructed receiver implementation ID is unchanged:
`86b6fcce8d8f13479e8131e1a386782b7bda5b6ee579df46e640ca8005affbea`.
The fresh profile therefore does not create a new receiver identity or justify
repeating the adopted rich Std grounding/reciprocal mathematical campaign.

## Outer closure and next decision

Outer status is COMMAND_EXITED_ZERO_AND_CLOSED: exit zero, direct child reaped,
Job closed, no termination request or cleanup error, zero final active/terminated
processes. It records 95 total processes, 905,678,848 peak private-commit bytes,
23,073 stdout bytes and zero stderr bytes, within the selected outer 540 wall /
440 CPU / 2304 MiB / eight-process envelope. Wall is **50.7916521 seconds**.
Known CPU is **47.234375 seconds** = 46.234375 outer Job CPU + 1.0 wrapper CPU;
nested Job CPU is already included and must not be added again.

The remaining practical boundary is the forthcoming current operator kit: can
an operator prepare exact current-profile requests and follow bounded public
reports without constructing undocumented command lines? Select the smallest
actual public workflow only after its inert preparation path is source-reviewed
and controlled. A fresh init/contribute or exporter run should be justified by
that new workflow, not a changed receiver or changed native code. Existing
checked mathematics and approved compiled tiny projects should be reused where
they suffice; do not repeat rich Std export, grounding or reciprocal work.

Source inspection distinguishes the two exporter roles: owner-free
produce-baseline invokes BaselineExporter; owner extract-project/extract-std
invoke MissingImportExporter for a retained request. One produce-baseline does not
exercise both. A requirement to execute both would entail two different public
paths and needs a concrete operator-workflow reason. No such launch or state
selection is made by this report. Full v5 remains unfinished, local and
unpublished; no discovery or useful-growth speedup claim follows.
