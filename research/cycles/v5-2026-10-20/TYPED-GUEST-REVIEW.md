# Typed guest: build and assembly source review

2026-10-21, adaptive_audit. **PASS for the exact source preparation below.**
Root may separately select the bounded build; actual build adoption must precede
assembly selection. No selector, builder, assembler, native control, guest or
proof was run. Used predecessors and evidence were not changed; no Git mutation.

## Reviewed files

Paths are relative to the sole canonical Trustworthy root.

| File | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/typed_guest/recipes.py` | 8907 | `c938f63f27dd01d7f08a0f3693048d3a6882fca00b6c8220a934f07b3513fb42` |
| `software/v5/typed_guest/build.py` | 23040 | `95903977ce10180480587163102a3c7c4ce98df9191dee93072be71747b2a9ba` |
| `software/v5/typed_guest/assemble.py` | 14834 | `a8fd105ff63655b42c25475222eebc82b67db822f7f3ddfc507d65e1fcd74ef9` |
| `research/cycles/v5-2026-10-20/Select-TypedGuestBuild01.ps1` | 6589 | `c2db56868bbaa03ea386d4c1770be7eb3b6f6a4cd6ba8febeaa920d07f4ad04d` |
| `research/cycles/v5-2026-10-20/Select-TypedGuestAssembly01.ps1` | 6803 | `ed4ec37aa029d3ca1c56f73cb245cf6584fcc1f0e90020b81598a1d2177b55a8` |

Author checkpoint TYPED-GUEST-SOURCE is `9b3aa072`. Read all five new files and
the author checkpoint; compared recipes/build/assembly against their frozen
proof-memo predecessors. Inspected directly referenced source declarations,
genuine aggregate entry and inherited helper interpreter check. Small read-only
JSON/hash diagnostics corroborated the selected source/evidence relationships;
no product module was imported.

## Build selection and dependency binding

The selector and builder agree on the seven-key schema, exact run name, two
adapter pins and unchanged limits. Fresh selection/run/attempt paths are
required. The selector writes create-new and does not launch compilation.

The selector's earlier 63-character native-selection hash was corrected before
invocation. The reviewed exact retained hash is
`b4da69c0b7b925415931f11adb31c690d2f0ae18f57edddc4b74fcbd44d57cb4`.
The saved inner and outer native selections have different serialization hashes
but **equal decoded JSON**, as required by the builder; they are not confused
with interchangeable raw bytes.

The 39-file native selection loses only its builder and two test files; its
remaining 36 files all match current byte/hash pins. The unchanged aggregate
entry is added, giving 37 selected files. `bounded_parse/census.rs` is retained
comparison support, not production reachability. The other 36 form the declared
static guest closure: typed roots/parser/correspondence, literal fallback,
foundation/commitments, existing kernel and aggregate header/membership/wire.
Test-only module declarations are cfg(test), which the new recipes do not set.
This is source reasoning, not an observed compiler dep-info result; the builder
explicitly reports that distinction.

The new recipe changes only the run name, three crate roots and fresh metadata
relative to the four-crate proof-memo recipe. It preserves the 297-unit retained
graph projection, target, dependency feature checks, sequential dependency order,
O3/overflow-checks/panic-abort profile and guest fat LTO. Fresh checker/module/
aggregate rlibs are passed through explicit extern paths; old project rlibs
are excluded. The 236 dependency artifacts are 107 target rlib/rmeta pairs and
22 host macro DLLs, totaling 311693039 bytes. Their selection is an exact subset
of the prior 238-file direct-build map, excluding the old checker pair. No Cargo,
dependency/SDK/C++ rebuild or implicit new dependency resolution is selected.

The builder pins the adopted native build/selection/map/attempt, exact eight-
control output and test-binary identity; it does not rerun those controls or
promote them into guest-performance evidence. All production/dependency inputs
are checked before copying, copied into a fresh exact-membership view, and
rebound after closure. Compiler runtime remains the retained 26-file selection.
The inherited helper checks the actual build interpreter: root must use
`D:\Python314\python.exe -I -S -B`, not the installed receiver interpreter.
The assembler uses its separately selected installed Python as before.

## Mathematical and resource boundaries

`aggregate/main.rs` is unchanged: it calls the selected conditional aggregate
relation, invokes genuine `env::verify` for every returned assumption, and commits
the exact encoded header. No native-success shortcut, fake receipt, changed
kernel rule or old-image relabeling is introduced. This compilation does not
itself produce an image, check the target execution or produce a certificate.
The adopted typed-source correspondence remains the premise; this review does
not re-prove it for unrestricted Lean.

Build limits remain 240 inclusive worker CPU seconds / 300 worker-phase wall,
4096 MiB / six processes, controller 40 ordinary and 60 finalization CPU seconds,
420 whole wall, 512 MiB sampled fresh output / 4096 entries and 8 MiB command
logs. Four sequential compiles share the one Job. Final closure requires no
active or terminated children and the original CPU cap. Failures preserve actual
launched counts; final binding/census failure overrides an earlier apparent
success. Report/exit tails are explicitly excluded from inner timing and require
root's outer completion accounting. Sampled bounds are not a hard disk quota.

## Assembly and later adoption

The fresh assembler is a mechanical successor of the adopted proof-memo wrapper;
its changes are names/schemas and exact 37-selected/36-declared-source binding.
It reuses the pinned pure helper and retained assembler executable/kernel. The
selector requires the reviewed build result, four clean command records/logs,
seven exact outputs, source map, selection and absence of a finalization override.
The inner adapter additionally checks attempt linkage, recipe/actual argv equality,
whole-build limits, exact artifact/link-map/output paths, and input rebinding.

There is exactly one assembler subprocess, timeout 60 seconds, under the selected
outer 120 CPU / 120 wall / 1024 MiB / two-process wrapper. RISC0 environment
overrides are removed. The parsed image ID comes from the pinned assembler's
actual output; it is not confused with the image file SHA-256. Final inputs and
image bytes are rebound. Inner assembly success is explicitly insufficient
without clean outer completion; it grants no mathematical authority.

No remaining blocking defect found in this source boundary. Adopt actual build
and then actual assembly separately before creating fresh A′-bound target inputs.
Neither this PASS nor a future compile/assembly PASS authorizes guest execution,
the substantial proof allowance or a performance/renewability claim. Those
decisions remain the exact endpoint and finite gates in CERTIFIED-RENEWAL-NEXT.
