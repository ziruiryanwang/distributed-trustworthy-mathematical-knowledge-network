# Authoring over verified mathematical modules

This API lets an owner write Lean source using selected library results without
fetching the old proofs of imported theorems. It is not a release-complete SDK:
the fresh frontend compiles and links and its five conditional native controls
pass. The genuine receipt-to-source-to-certified-child endpoint remains separate.
The selected compiler-successor is `native02/AuthorLean.lean`; the earlier
`AuthorLean.lean` preserves a failed keyword-compatibility build. Do not replace
used bytes to repair failures. Current qualification is at the research live desk.

## Trust and data

A search result is a hint. A stored module opening proves a hash relationship,
not a mathematical theorem. A verified receipt and a live local handle establish
the module under the owner's chosen image, foundation and policy. The handle is
process-local: copied JSON cannot replace it.

Lean's authoring environment is a convenience for producing a new proof. Imported
theorems/opaque declarations appear as authoring-only assumptions with their exact
types. They do not become newly accepted axioms. The child still needs the
independent module relation and real certificate verification with exact parent
receipts. No export status flag grants mathematical acceptance.

Transparent definitions differ: unfolding needs their actual committed bodies.
An inductive group needs its complete type/constructor/recursor interface and
reduction-rule bodies. The frontend uses Lean's checked kernel constructor and
compares generated names, types, metadata and rules with the committed group.
Input cost therefore depends on selected semantic context, not the complete old
theorem proof histories or unrelated network corpus. Not every semantic context
is small; exhaustion explicitly refuses.

## Owner workflow

1. Create `ImportSession(verifier, ...)` from an actually adopted
   `ReceiptVerifier` or `DeadlineReceiptVerifier`. For the network workflow, use
   the same actual deadline-bound verifier, not another with equal settings.
2. Genuinely verify the chosen module receipt; select the returned handle with
   `session.use_handle(handle, exact_receipt_bytes)`, or use the existing session
   `receive(...)` method. Open complete groups using `session.open_group(module,
   opening)` and supply committed bodies with `session.supply_body(module,
   universes, expression)`.
3. Construct `SourceOperation(session, foundation_bytes, foundation_sha256,
   owner_source, roots)`. Roots are structured names, for example
   `[[["s", "MyLibrary"], ["s", "my_theorem"]]]`, not display strings.
4. Inspect `operation.prepare()`. It returns typed missing-data demands or
   canonical untrusted request bytes. If data is missing, acquire it, close the
   operation and recreate it over the changed session. The old selection binding
   must not silently follow session mutation.
5. Run the selected linked frontend as `AuthorLean.exe REQUEST FRESH_DIRECTORY`
   once within the original finite owner allocation. Only explicitly selected
   owner source may run: Lean metaprograms are executable code, and this is not
   a sandbox for downloaded peer source.
6. Give returned `FRESH_DIRECTORY/EXPORT.json` bytes to `operation.finish(...)`.
   It rechecks the same live session/selection, derives the actual local census
   and canonical declarations, and returns an untrusted child prover input plus
   exact genuine parent receipt bytes. Finish is one-shot, even on bad output.
7. Prove/check the child through the adopted producer and receiver. Only that
   separate successful admission makes it verified knowledge. Close the operation
   afterward; this does not close the independently owned session/verifier.

The actual preparation/return API is:

```python
operation = SourceOperation(session, foundation_bytes, foundation_sha256,
                            owner_source, structured_roots)
prepared = operation.prepare()
# If ready, persist prepared["request"] exclusively; run the selected frontend
# through the existing owner-supervised process allocation, not a peer executor.
child = operation.finish(export_bytes)
assert child["mathematical_acceptance"] is False
operation.close()
```

This is not a standalone launch example: missing-data handling, exclusive file
creation, pinned runtime configuration and whole-process supervision are required.
The retained supervisor strips arbitrary inherited `LEAN_*` configuration. The
new owner-pinned `worker.py` supplies the exact selected Lean runtime root and DLL
search path inside the existing Job. Its20 mock-only focused controls pass;
actual worker/native integration remains unqualified. The earlier conditional
harness does this internally.
Do not assume setting an outer shell variable reaches the supervised child.

## Fixed owner worker

The outer owner controller invokes the selected Python interpreter in isolated,
no-site, no-bytecode, nonoptimized mode with `worker.py --config ABS_JSON
--config-sha256 HASH`. The worker never accepts peer-selected commands or a
generic argument list. Its only native command is `AuthorLean.exe REQUEST
FRESH_DIRECTORY`, using the exact pinned executable and request paths.

The configuration has exactly these fields:

```json
{
  "schema": "DMKN_OWNER_LEAN_WORKER_V1",
  "worker": {"path": "ABS_WORKER", "bytes": 1, "sha256": "64-lowercase-hex"},
  "executable": {"path": "ABS_EXE", "bytes": 1, "sha256": "64-lowercase-hex"},
  "lean_root": "ABS_LEAN_ROOT",
  "runtime_pins": [{"path": "ABS_RUNTIME_FILE", "bytes": 1, "sha256": "64-lowercase-hex"}],
  "request": {"path": "ABS_REQUEST", "bytes": 1, "sha256": "64-lowercase-hex"},
  "output_directory": "ABS_OPERATION/frontend",
  "report_path": "ABS_OPERATION/worker-result.json",
  "deadline_monotonic": 12345.6
}
```

This illustrates fields, not valid runnable values. Every path is absolute and
canonical. Output/report must be fresh siblings in an existing operation
directory. `worker` binds the actual running file, not a test substitute. All
selected files and configuration are rechecked before and after native work.
Duplicate JSON keys, nonfinite numbers, unknown fields, bad pins and expired
deadlines refuse. The owner supplies the effective deadline as the minimum of
its original deadline, the live SourceOperation's original deadline and the
per-call wall limit. The worker requires positive remaining time at most600s
and recalculates the remaining wait after spawn; it does not grant fresh time.

Runtime pins are explicit owner-selected execution dependencies under the adopted
Lean root, not the compile/link test's approximately989MB compiler closure. The
minimum five DLL entries are `libInit_shared.dll`, `libleanshared.dll`,
`libleanshared_1.dll`, `libleanshared_2.dll` and `libc++.dll` in `bin`. The owner
must also select any required runtime data. Limits are128 pins,512MiB each and
2GiB total. This is not a hermetic toolchain, hostile-code sandbox or complete OS
DLL closure. Request/export are each at most16MiB; configuration128KiB,
worker2MiB and native executable64MiB. The worker hashes bounded file streams.

Native stdout/stderr are inherited, never captured into worker memory: the outer
supervisor owns their retained partial logs and sampled log caps. On timeout the
worker kills/reaps its direct child; only the outer Job can establish whole-tree
closure. Failure-report writing does not extend the original outer allocation.
Owner byte accounting must include **all** files, especially native
`module.ndjson` (up to64MiB) in addition to `EXPORT.json`, request, configuration,
logs and report. `export_bytes` is not total operation bytes.

The result schema is `DMKN_OWNER_LEAN_WORKER_RESULT_V1`. Its positive status is
only `PASS_NATIVE_EXPORT_ONLY`: exact config/request/executable/worker hashes,
original deadline, native return/timeout/direct-child disposition and export
hash/size. It always has `mathematical_acceptance=false`,
`outer_job_closure_required=true`, `native_logs=INHERITED_OUTER_SUPERVISOR` and
`runtime_scope=EXPLICIT_OWNER_PINS_NOT_HERMETIC_OR_SANDBOX`. The owner must validate
those bindings, actual whole-Job closure, all output costs and the still-live
SourceOperation/selection before calling `finish` once. The returned child still
requires the independent relation/certificate admission described above.

`test_worker.py --out ABS_FRESH_EXPERIMENT_DIRECTORY` is a native-free
control harness. It mocks every subprocess and keeps all fixtures/results. Its
fake runtime/executable/export bytes exercise binding/refusal/control flow only;
no Lean success, live handle, receipt or mathematical authority is fabricated.

## Missing-data handling

| Demand | Same-budget/deadline action |
| --- | --- |
| `NeedVerifiedModule` | Use `ModuleDependencyAcquisition.prepare(...)` for the exact owner/address, acquire a real receipt through the existing workflow, then `admit(...)` into the same session. An offer or opening alone is insufficient. |
| `NeedDeclaration` | Use `DependencyAcquisition.declaration(provider, module, structured_name, max_bytes)` for an already selected verified owner. It opens the exact group without optional search-feature extraction. |
| `NeedBody` | Retrieve the specified committed semantic body through the existing workflow and call `session.supply_body(...)`. Missing transparent definitions never silently become opaque. |

Companions add no transport, automatic retry, renewed deadline or new resource
grant. Contact expiry and request/byte/proof costs remain charged. Custody,
verification and session selection are not a cross-component atomic transaction;
late refusal can leave structural custody. The unselected-owner companion also
revokes its originating verifier on late selection failure, invalidating earlier
imports. Expiry, closure, owner replacement or changed selection prevents return.

## Names and compatibility envelope

Imported names are structurally relocated to
`DMKN.Mod.<ModuleID>.<original-relative-name>`. A string-only Lean example is
`DMKN.Mod.«<64-hex-ID>».CommonsV5.Tree`; the quotes delimit the Lean identifier,
not the module ID. Protocol APIs always use structured names. Do not split display
strings to reconstruct a semantic address.

Pinned Init supplies syntax, but only the exact adopted foundation subset is a
semantic boundary. Other used Init constants must be exported as new local data
and independently checked, or refused. Fresh axioms (including `sorryAx`),
unsafe/partial declarations and fresh quotient constants cannot escape that rule.
All old bindings are preserved across source elaboration. Roots may select
theorems, definitions, opaque values or inductive types; local bodies remain new
checker work.

Namespace, notation, instance and attribute registries are not module descriptors.
Use qualified names and explicit recursors when those conveniences have not been
reconstructed: for example `induction e using DMKN.Mod.«...».CommonsV5.Tree.rec`.
Mathematical source can use `noncomputable section` when executable code generation
is unnecessary. General frontend convenience/native-code compatibility does not
follow merely from kernel-interface reconstruction.

Defaults: eight selected modules per session;256 groups,4096 imported declarations
and16MiB context;64KiB owner source. The new native envelope permits64 universe
parameters/arguments, narrower than codec's256. Export has a separate4096
visited-constant cap. Nested groups must reproduce the exact committed census
and be frontend-visible or refuse. These limits do not bound the whole commons.
`counted_expression_visits` omits hashing/copying/parsing/native CPU; total-cost
accounting and whole-operation time/memory supervision remain mandatory.

## Validation boundary

`test_native_frontend.py link` links the retained successful generated C; it does
not re-elaborate Lean. Its separate `controls` mode tests imported Tree/fold/map
use, binder-info preservation and targeted refusals using an explicitly untrusted
test context. The input bundle contains no imported theorem proofs and the test
fabricates no positive handles or receipts. It does not qualify the live-session
pipeline or certify a child. Runtime pins cover explicit tools/libraries/Lean
headers, not every OS header/DLL or a hermetic toolchain. Captured-log quotas are
posthoc under the outer memory bound; timeout handling preserves partial logs.
