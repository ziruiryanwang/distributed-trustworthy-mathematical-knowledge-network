# Internal ordinary workflow worker: protected export, basis and extension

Root selected `software/v5/ordinary_lean/OrdinaryWorkflowWorker.lean` as a small
internal CLI. Root subsequently selected the basis and extension branches below
after reading BasisSnapshot and LocalSnapshot. No runtime, compilation, repeated
method/core control or Git action is selected by this source work.

```text
OrdinaryWorkflowWorker export sysroot selectedCompiledMethodDir pinnedInventoryPath freshOutputPath
OrdinaryWorkflowWorker basis seedPath inventoryPath rootHex outputPath reportPath
OrdinaryWorkflowWorker extend planPath validatedUnitsPath rootHex outputPath reportPath
```

All paths must be absolute and are trusted controller inputs. The controller
must authenticate the selected Lean runtime, immutable compiled owner module and
its dependencies, the exact fixed inventory bytes, and output directory before
invocation; supplying paths is not an acceptance grant. This CLI is not a public
peer file-import endpoint. It does not elaborate incoming Lean source.

The only imported target is `examples.ReadFootprint`, at private level, with
`plugins := #[]` and `loadExts := false`. The runtime library directory precedes
the selected method directory in an explicitly replaced search path; inherited
`LEAN_PATH` is not added. The controller's trusted artifact selection must exclude
extra/shadow files. Dynamic plugin/extension initialization is not requested.
This is a locally owner-authorized producer import, never receiver admission.

Read the fixed inventory through a byte-capped handle (1 MiB) before parsing,
requiring valid UTF-8. Every branch first screens raw nesting (64), unsigned
integer tokens (20 digits and UInt64), strings and brackets before `Json.parse`.
Exponents, negatives, fractions, boolean/null and nonfinite tokens are refused
before general parsing. This independent guard prevents an exponent bomb; exact
canonical JSON, duplicate-key refusal, schemas and input identity still belong
to the controller's evidence reader. Then call
`Export.indexSource` once and `Export.selected` for the single fixed target
`DMKN.ReadFootprint.readsOnly_insertMany`.

The output is an inert bundle with a distinct schema, original target and basis
names, original declaration units and finite source/closure/byte counters. Bound
the complete serialized bundle by 64 MiB, then use exclusive `writeNew` and flush.
An existing output must never be overwritten. A crash may leave an incomplete
fresh file; the controller must require successful process completion and validate
the complete returned bundle before canonicalizing per-unit evidence. The output
has no acceptance/verified boolean, certificate, cache or permissive receipt API.

The worker's Lean JSON printer is not the evidence canonical encoding. The root
controller parses this bounded local output, then constructs exact canonical
evidence envelopes and checks profile/import identities at its own protected
boundary. A successful export is still only a producer claim.

## Fixed basis branch

`basis` requires the protected controller to pin the exact selected seed and
inventory before launch. It reads each with the 1 MiB cap and lexical preflight,
derives the exact native module name `DMKNLocal.r<64 lowercase hex root>`, and
calls `BasisSnapshot.checkAndWriteBasis` without changing its defaults. Only the
actual result determines the report's names, module, unit count and artifact
size. This is genuine empty-environment basis checking, not imported Init or
source-correspondence acceptance. No report alone creates a catalog warrant.

## Protected extension branch

`extend` consumes this exact internal plan shape (16 MiB cap):

```text
{basis_module, root_module,
 modules:[{module_name,path,parent_module,artifact_bytes,names_count}, ...]}
```

Names use original-name arrays. `parent_module: []` denotes no parent only on
the first basis entry. These rows come from the authenticated local catalog,
not peer binary advertisements. `LocalSnapshot.restoreLocal` validates the
complete chain and uses an explicit artifacts map with no fallback search path,
plugins or extension loading. Controller authentication/immutability of all
artifact bytes must precede this unsafe native deserialization.

The second input is an array of already-controller-validated OriginalDecl units,
not evidence envelopes, capped at 64 MiB and **1024 units**. Decode against actual
restored parent names; add each earlier claimed output name only for later syntax
decoding. Such a claim cannot become a premise: `checkAndWriteChunk` checks the
whole batch in order and compares actual generated records before succeeding.
Retain its default 65,536 new-name limit, and cap all selected names at 1,048,576.
No caller-supplied accepting environment or success flag enters this path.

Both checking branches require fresh output/report paths and write the report
exclusively only after actual checking and snapshot writing. Report schema is
`DMKN_ORDINARY_WORKER_OUTPUT_V1`, exact fields `schema`, `kind` (`basis` or
`extension`), `module_name`, `parent_module`, `names`, `units_checked`, and
`artifact_bytes`; report size is capped at 16 MiB. Anonymous parent is `[]`.

The outer owner must match exact worker/profile/parent/request/grant identity,
supervise clean exit and validate the actual report and snapshot before private
catalog promotion. A failed/partial file, reused saved report or arbitrary path
cannot establish this event. The worker does not implement catalog mutation,
remote grants, withdrawals, peer `.olean` adoption or public acceptance endpoints.

Before the first selected workflow build, normalized only the exporter final-result and worker import-plan record layouts to explicit multiline fields; semantics unchanged, no execution or Git operation.
