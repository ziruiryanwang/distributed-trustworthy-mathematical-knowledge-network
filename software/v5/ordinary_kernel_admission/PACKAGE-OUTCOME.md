# Independent actual package01 audit

Disposition: **PASS_FILE_ASSEMBLY; FRESH OWNER AND RICH INTAKE NOT ESTABLISHED**.

Saved run: `experiments/v5-local-checks/kernel-admission-package01`.
The reviewer used read-only JSON, hashes and filesystem metadata. No product
import, package/native execution, database access or Git mutation occurred.
Saved selection and current selection both match reviewed SHA-256
`22dcd0ad2bc0901f53f52fae311b3b9ed382aa6a6842b88da918df099c7fbec2`.

All four selected source/current-snapshot pairs and all 191 external pins match
actual bytes. The package has exactly 154 ordinary single-link files totaling
39,316,958 bytes, with no unexpected file or redirected entry. The actual census,
every file length/hash and the saved ASSEMBLY map agree. Exactly nine files
changed from the adopted predecessor, with 145 unchanged:

- CheckedExtension, LocalSnapshot and OrdinaryWorkflowWorker receiver sources.
- CheckedExtension, LocalSnapshot, OrdinaryExport and OrdinaryWorkflowWorker objects.
- INSTALLATION.json and PROFILE.json.

All 117 auxiliary PROFILE rows, authoring helpers and eight standalone Markdown
documents remain byte-identical. PROFILE changes only its installation-manifest
binding. All eight native source/object pairs agree with the adopted BUILD map;
the rebuilt BasisSnapshot object remains unchanged. The 36 installation-plan
rows bind the actual selected source files to the resulting installation pins.
All six current controller modules remain exact predecessor bytes; the reviewed
selected assembler's origin/object guards passed before assembly completed.

The actual implementation changes exactly `adapter_support` and
`snapshot_support`. Independent reconstruction of every support digest and the
implementation identity agrees with the installer result and prior source-only
expectation. Semantic identity, kernel, controller and basis support, roles,
compiled directories and support-group membership remain unchanged.

| Actual identity | SHA-256 |
|---|---|
| PROFILE.json | `60b6e0d6c7d4e7d7761ed5f7ebb2d449afc55547f46f6924f0b93234a5a30f3b` |
| installation/INSTALLATION.json | `9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27` |
| Implementation identity | `86b6fcce8d8f13479e8131e1a386782b7bda5b6ee579df46e640ca8005affbea` |

The stdout document equals ASSEMBLY semantically; stderr is empty. The outer
report records zero exit, reaped child, closed Job, no termination request,
zero active/terminated processes and no cleanup errors. Wall time is
5.7215804 seconds. Inclusive Job CPU is 2.515625 plus 0.65625 wrapper CPU:
**3.171875 known CPU seconds**. Peak Job private commitment is 21,061,632 bytes.
Adapter CPU 2.4375 is nested in this accounting and must not be added again.
No resource-limit event appears. Source and report agree on zero native calls
and no owner opening; the two recorded process creations are not two Lean calls.

| Saved evidence | SHA-256 |
|---|---|
| RESULT.json | `03c6f6902e8ba9f2aa393cadf5eecae3cc882c293b36564c57103f55c82fc01e` |
| distribution/ASSEMBLY.json | `4515b25967ca432f9512df445eb870b3d5e276356339a5ac6a1ac5f73c6e37fe` |
| distribution/INSTALLATION-PLAN.json | `423a3991701ea193db62b9373772582b790f7838e565cf2fc9c1e7c7161708de` |
| command/stdout.txt | `c06ac502e9098af4ef50a2df90c79f9d4a1fbca381f0c3dc9b53d2ee2595fcec` |

This supports root adoption of the exact file-only successor package. It does
not migrate old state, promote failed Std artifacts, establish a protected basis
under the new identity, demonstrate rich-library intake or prove knowledge-growth
benefit. Those require their separately selected actual workflows. All used
sources, selection, inputs, outputs and evidence remain frozen.
