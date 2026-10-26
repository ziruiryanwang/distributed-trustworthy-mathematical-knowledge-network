# Bounded challenge: scratch claims cannot promote themselves

2026-10-26. Independent source-only adversarial review. **No actionable new
counterexample found in the selected seam.** This is not a complete security
audit, proof of implementation correctness, runtime result or final-v5 claim.
No product imports, native execution, tests, state/API access, Git operations,
package edits or experiment allocations were performed.

## Scope and attempted counterexample

`P` below is the actual selected ordinary package:
`experiments/v5-local-checks/exact-module-assembly01/assembled/package`.
Distribution selection was read from
`software/v5/ordinary_investigator_bundle/ADOPTION.md`; no rebuild is needed.
The preceding EXACT-INSTALLED-CHALLENGE, ANCHORED-EXTENSION-CHALLENGE and
POST-BUNDLE-ARCHITECTURE-CHALLENGE are reused for their separate boundaries.

Attack considered: a scratch authoring environment proves target `t` using an
unwarranted axiom, a different same-named definition/theorem, or a fabricated
candidate ID; metadata then labels `t` as received/checked and publishes a
preview for it. Required violation: an owner context acquires a new warrant
without checking the supplied declaration under its own selected imports.
This review follows that single path and its shared receive/preview boundary.

## Source trace and why the attempted bypass does not establish acceptance

1. `P/authoring/py/ordinary_contribution.py:402-452` obtains bindings from the
   selected protected catalog context. Each acquired evidence lookup requires
   the exact warranted name/ExportID, an exact locator, UnitID and output name;
   prepared group bindings are checked again. A source environment is not the
   source of these warrants. Scratch request preparation remains authoring aid.
2. `P/authoring/py/portable_candidate.py:114-242` reparses inert candidate bytes.
   Context/semantics/targets are exact; a claimed import must agree with both
   the prepared request and current protected lookup. An explicitly unresolved
   name can use the owner's interpretation only if that lookup exists. Missing
   names yield NEEDS_LOCAL_INTERPRETATIONS, not an assumed theorem. Outputs
   cannot overwrite known names; forward/cyclic selected references are refused.
3. `P/installation/py/portable_evidence.py:46-70` independently parses complete
   units and requires import census/order equality, including proof references.
   UnitID commits to canonical evidence bytes; imports are part of those bytes.
   The candidate's claims and successful source compilation confer no warrant.
4. `P/installation/py/ordinary_admission.py:390-464,562-585` checks exact parent
   and selected-unit imports, refuses conflicting names and partial reused
   groups, and orders dependencies. `admit` recomputes preflight from raw units;
   it does not trust the caller's READY flag, order, missing list or reused IDs.
   `P/installation/py/portable_catalog.py:599-626` independently repeats import
   and no-overwrite bindings when reserving the extension.
5. `P/installation/py/ordinary_admission.py:587-652` binds the live grant to
   exact ordered UnitIDs, parent-module plan and selected context. It launches
   the pinned admission worker, not the authoring process/environment. The
   worker restores the protected chain and calls the checked extension:
   `P/installation/lean-src/OrdinaryWorkflowWorker.lean:196-229` and
   `P/installation/lean-src/LocalSnapshot.lean:149-165,228-244`.
6. `P/installation/lean-src/CheckedExtension.lean:24-75,99-155` refuses
   `sorryAx`, new axioms, unsafe/partial declarations, ungrounded references and
   overwrites. Each new declaration is checked with `addDeclCore` and
   `doCheck := true`; generated records must exactly match claimed inventory.
   A successful prefix of a failed batch is not returned as an accepted batch.
7. Only the actual clean worker result with the exact report/name/unit census
   leads to `_commit_checked`; retained report JSON alone is insufficient
   (`ordinary_admission.py:622-652`; `portable_catalog.py:628-678`). The
   contribution requires actual CHECKED, not REUSED, before publication
   (`ordinary_contribution.py:520-575`). Output IDs are recomputed from exact
   units/names (`:238-265`), and preview projection is resolved against those
   same units (`portable_preview.py:89-121,147-161`).
8. The parallel peer receive entry does not add a metadata shortcut:
   `P/peer_api.py:573-700` validates the selected record, acquires the exact
   ExportID/name evidence, calls `PP.resolve`, and invokes the same admission
   path. Missing grounded premises can terminate without admission. Existing
   REUSED acceptance is explicitly separate from new native checking.

## Adversarial cases and assumptions

An omitted scratch-only axiom cannot escape the complete reference census;
if named as unresolved it needs a protected interpretation, and if supplied as
a new axiom the native declaration policy refuses it. A forged claimed ID
conflicts with prepared/protected bindings. A fabricated theorem body that
survives parsing still faces the actual kernel check in the restored context.

If an unresolved scratch name denotes something different locally, rebinding
can produce different *intended* mathematics, but not an unproved accepted
theorem under the owner's semantics: final native checking uses that semantics.
The system deliberately does not certify source intention. Likewise, mutable
preview/report fields are not acceptance tokens. Exact matching does not depend
on a provider's reputation or claimed successful computation.

This argument assumes trusted selected implementation/kernel/codecs, ordinary
hash integrity, correct protected-context lineage, and immutable protected
artifacts during use. `P/EXECUTION-TRUST.md` explicitly excludes hostile local
executable code with owner-account write permissions: source authoring is
approved code execution, and process Jobs are not an OS security sandbox.
Such code could corrupt local state directly; neither this audit nor the
candidate binding rules claim to prevent that distinct account compromise.

Stop here. No additional generic refusal campaign or acceptance redesign is
justified by this bounded source challenge. A future observed mismatch should
receive its own minimal changed-boundary investigation, not a repeated suite.
