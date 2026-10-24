# Native-first file assembly: source checkpoint

2026-10-24. growth_product_selection, selected by root in SELECTION.md.
Source implementation only. No product import, package assembly, native execution,
owner opening, test campaign, installation, network or Git mutation was performed.
The final v5 goal remains active. Root owns independent review and any finite run.

## Delivered source

| File under software/v5/ordinary_native_package | SHA-256 |
|---|---|
| `assemble.py` | `6f68ed05fd460fc5a7f5742a8875c659481d0697ef2fc2c91bac3d251de3cbe1` |
| `source-map.json` | `18e8ce9b732a4629f36ced822c7ef37101b8ee06954f95d72cea3a54c82c5bb3` |
| Updated `README.md` | `4f558c36200d70603d66ad61331f80c3043aea7a970ef8b6eb08484898b49304` |

The existing reviewed owner/profile files are unchanged. No new mathematical or
anchor-support boundary beyond those reviewed facade bytes is introduced.

## Implementation selection and resulting map

The recipe takes explicit source/base/exporter/runtime/output paths and an exact
source-map digest. Its supported base PROFILE, receipt, installation and exporter
pins are fixed; a relocated identical input is allowed, an arbitrary substitute
is not. It imports only the exact preserved stdlib-only file helper from
`software/v5/ordinary_package/build.py`, never an owner/profile/other product module.
The helper's build functions are not called.

It reads the exact retained base manifest/profile and performs a complete bounded
file census. The resulting map contains:

- 132 unchanged stable-preview payloads;
- two changed facade files;
- four unchanged Python baseline roles and the retained exporter executable;
- README.md and PRODUCER.md as separately counted documents.

This is 141 payloads, plus ASSEMBLY.json and commit-last PROFILE.json. Exactly 111
roles belong to the executable helper profile. The logical reference directory
contains only baseline_bundle.py and baseline_intake.py, not the parked reference
matcher, registry, source authoring, native helpers or separate profile.

The source map pins six source-code roles, one retained executable and two
documents. File sizes and hashes of all eight source/document entries were checked
read-only with PowerShell. The exporter exact pin is reused from retained evidence;
no exporter build or run occurred.

## Reusable API for root's selector

`helper(source_root)` loads the exact adopted file helper.
`inspect_inputs(B, args, check)` performs the same bounded input census as assembly,
without writing. Its returned map contains `pins`, `selected`, `predecessor`,
`source_pins`, `old`, `changed`, `added`, `unchanged`, `base`, `source_root` and
`runtimes`. Each pin is `{bytes, sha256}`; selected values are `(Path, pin)`.

CLI/Namespace fields are `source_root`, `base_package`, `exporter`, `python_runtime`,
`lean_runtime`, `output`, `source_map_sha256`, `wall_seconds`, `cpu_seconds`.
Only assemble needs the final output and finite-time fields. It checks isolated
Python/no-site/no-bytecode/no-optimization and the selected running Python path.

The common exact-input mismatch error is
`NATIVE_ASSEMBLY_INPUT_PIN:<absolute input path>`. A wrong source-map digest fails
before destination creation. No special source-map error name is implied.

Output may be a sibling of a source snapshot, which supports the existing bounded
runner. It cannot contain the source root or overlap any pinned source file,
base package or runtime. Paths are ordinary local Windows paths without redirects;
the preserved helper checks file kinds and rejects hardlinked payloads. Copies
are fresh, bounded, fsynced and read back; inputs and copied bytes are checked again
before publishing the descriptor. Partial failures are retained without retry.

## Source checks and explicit limits

AST parsing completed with 33 top-level statements and no product import. The
first parser invocation had a shell-quoting error in its success-print label
after parsing; a quote-free output invocation completed. It did not run product
code or produce evidence of behavior. No attempt to conceal that diagnostic is
made. JSON input/source pins were checked using ordinary read-only shell tools.

This is reusable **file assembly from pinned inputs**, not a clean-source compiler
build, a fully portable platform implementation or mathematical acceptance.
Original native/build provenance remains separate. Controller time limits are
cooperative; the root-selected enclosing Job provides any hard process limits.
The new recipe does not erase old state/failures or migrate anchors.

README now makes ordinary approved package development followed by selected-output
export and independent intake the primary loop. Optional generated-module and
retained-candidate routes remain narrower capabilities. Mathematical checking does
not authorize package execution or attest original compiled artifact semantics.

The next gate is independent changed-source review. Root may then select one
small file-only boundary check, including role-map loader compatibility, but no
producer fixture, Lean theorem or owner-admission replay follows automatically.
