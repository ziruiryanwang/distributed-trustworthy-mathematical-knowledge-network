# Independent admission event-chain source review

2026-10-22. Reviewer: `admission_event_audit`. Source-only assignment; no runtime,
compilation, tests, Git operation, implementation edit, or mathematical admission
was performed. The failed owner export is not usable input. A new actual export
and a fresh root-selected finite allocation remain prerequisites for execution.

## Disposition

**No blocking event-chain defect found for the proposed owner-controlled local
integration driver.** This is permission to consider that source for a subsequent
root selection, not a passed admission, public security review, or v5 release.

The important property is present: the controller calls `_commit_checked` only
after its own actual selected worker invocation has finished with clean process
closure and exact input/report/output bindings. It does not read a previous PASS
file and turn that into mathematical authority. This conclusion depends on the
documented trusted native toolchain, controller and immutable owner storage; it
does not certify those assumptions or the underlying Lean implementation.

Reviewed primary bytes:

| File | SHA-256 |
|---|---|
| `software/v5/ordinary_lean/run_native_admission.py` | `a9bdbfc826221d21cd6454b1f8171b77e657996d89bac0461bee2f6e74ee897a` |
| `software/v5/ordinary_lean/local_catalog.py` | `860a9d731290b2a7fbacd4852bb68185516329ee42845648f4ba3c3856d7c751` |
| `software/v5/ordinary_lean/ordinary_evidence.py` | `fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6` |
| `software/v5/ordinary_lean/OrdinaryWorkflowWorker.lean` | `442c2d479d4df6b1c7ee456cb521b8c760b54258a3f8d5fb71a15fa391c77f9b` |
| `tools/Run-V5-Check.py` | `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651` |

Also read the actual frozen `operator/commons.py` supervision implementation and
`receiver/helpers/run_stage.py` Job implementation, plus `BasisSnapshot.lean`,
`LocalSnapshot.lean`, `CheckedExtension.lean` and `ACTUAL-ADMISSION-PLAN.md`.
This review is not a repeat of the prior codec/storage test campaigns.

## Acceptance chain

1. **Selection and profile.** `SelectedInputs` requires the source to belong to
   the selected output's immutable source snapshot. It matches all eight support
   source files to their previous compiled-source snapshots, checks the exact
   compiled-directory file census, and binds actual named binaries/artifacts to
   the outer selection. `profile()` commits to those exact maps. Neither source
   equality nor the profile digest is claimed to prove mathematical validity.
2. **Fixed foundation.** Both fixed files are length/hash checked before parsing.
   The exact 456-unit/581-name census, inventory order and exported basis names
   agree with the pinned seed. The basis worker calls the actual `receiveSeed`
   through `BasisSnapshot`; it does not substitute an imported Init environment.
   The written constants come from the returned checked environment.
3. **Exact request construction.** `prepare_bundle` canonicalizes each inert
   original unit, derives its complete external-name bindings, and calls the
   real evidence reader. The evidence and raw-unit array are constructed from
   the same parsed unit; no caller-controlled parallel request substitutes for
   that unit. `reserve_extension` reparses immutable evidence bytes and checks
   profile/import/no-overwrite bindings against accepted parent context and
   earlier batch entries. Claims from later entries cannot authorize earlier
   declarations.
4. **Actual checking.** The extension worker restores only the controller's
   authenticated local plan, decodes the selected raw-unit array, and calls
   `checkAndWriteChunk`. That calls actual `checkBatch`, direct
   `addDeclCore(..., doCheck := true)`, exact generated-record comparison and the
   complete added-name census. The private snapshot writer serializes actual
   checked output, not the received inventory records.
5. **Invocation-to-grant binding.** `execute` derives the request files, exact
   root module and fresh output destination from the current grant and parent
   catalog context. The internal wrapper accepts only basis/extend commands and
   cannot promote catalog state. Parent/request/profile identity need not be
   cryptographically asserted by the report: it is established by this trusted
   invocation path, exact bytes and selected worker semantics.
6. **Clean completion and promotion.** `clean_worker` matches the real supervisor
   contract: exit zero, reaped direct child, closed Job, no cleanup errors,
   termination not requested, zero active processes and zero terminated-process
   counter. Afterwards the controller rechecks all selected inputs and authored
   request bytes, exact report fields/kind/root/parent/ordered names/unit count,
   and actual file size. Only then can the original in-memory grant reach
   `_commit_checked`, which rechecks grant identity/deadline, sole-output census,
   artifact size, flush/hash and atomic catalog promotion.
7. **Persistence check.** Complete resulting bindings must equal the identities
   derived before native execution. A genuine catalog close/reopen then rehashes
   the selected artifact chain and requires identical bindings/module plan.
   This is stronger than merely reading a saved success report.

## Failure and resource behavior

The controller's nested `A.supervise` arguments match the actual signature. Its
wrapper and Lean child fit the nested two-process Job; the outer envelope must
allow at least the three simultaneous driver/wrapper/Lean processes. Both nested
and outer Jobs remain applicable: no breakaway is requested. Actual nested Job
CPU is combined with controller process CPU, and outer supervision independently
bounds the entire process tree. Remaining allowances are not reset per batch.

The no-promotion branch includes failed/unclean workers, changed inputs, wrong
reports, expired grants and exhausted budgets. A failed worker aborts the whole
driver; it cannot use a new batch to reset its spent allowance. Failure CPU is
still visible in saved nested/outer supervision, although `known_worker_cpu` in
the final success document exists only on successful completion. Uncertain
catalog transactions close the owner and are not retried. Failures during setup
can leave a RESERVED row; the store retains its charged reservation and changes
it to INTERRUPTED on reopen rather than resuming worker authority.

Batch planning preserves receiver defaults: at most 1024 units, 65536 new names,
2097152 serialized descriptor-plus-inventory nodes, and 64 MiB raw/evidence bytes
per batch; the evidence reader separately enforces its 8 MiB per-envelope cap.
Serialized node counts conservatively cover the checker's descriptor reference
scan; they do not purport to bound kernel reduction time, which has independent
heartbeats and Job limits. Unit counts, aggregate evidence, authored files,
catalog pages, roots/operations and artifact reservations are finite.

## Limits that must remain visible

- The native profile pins named files, not a hermetic runtime or all standard
  Lean/Python library bytes. Owner/OS immutability and no whole-store rollback
  remain premises. Hash-before/hash-after does not defeat an adversary capable
  of temporary replacement during execution.
- This process/resource enclosure is not a hostile-code security sandbox or
  physical disk quota. Worker artifact size is checked after writing; the native
  snapshot writer's own default is larger than the catalog's reserved output.
  Overlarge output is rejected, but transient or failed output can exceed the
  reservation physically. This is already explicitly outside the driver's scope.
- Every new batch restores its selected accepted ancestor chain. It avoids
  rechecking ancestor proofs, not reading their native snapshot bytes. No
  ancestry-free onboarding or warm-session performance result follows.
- Final catalog reopen authenticates bytes and metadata; it does not execute a
  fresh Lean consumer using the final theorem. The owner's ordinary project
  rebinding/consumer step remains separate and necessary for the user workflow.
- The profile includes the integration support source map, so its IDs are exact
  experiment-profile identities, not yet a stable public interchange policy.
- Actual native admission, useful unknown-ID discovery, substantive reciprocal
  extension, comparative growth benefit and deployable v5 remain unestablished.

## Next decision

Obtain the real source-derived export, inspect its closure sizes and batch plan,
then let root decide whether one bounded actual admission is worth funding. Do
not fabricate a small bundle to label this endpoint successful, increase limits
automatically, repeat passed component tests, or start another certificate job.
The subsequent highest-value endpoint is ordinary-project use of the admitted
method, not polishing this internal controller into an unrelated framework.
