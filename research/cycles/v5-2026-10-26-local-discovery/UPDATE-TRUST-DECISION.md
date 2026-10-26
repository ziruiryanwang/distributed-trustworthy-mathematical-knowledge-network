# Checker updates, retained trust and selective recovery

Source/theory decision, 2026-10-26. No execution, import, network operation,
state mutation or new checker version was performed for this note. Full v5
remains unfinished, local and unpublished.

## Decision

Do not build an automatic migration/revocation framework now. The current
ordinary design already has the important fail-closed separation: portable
mathematical evidence can survive a checker implementation change, but local
checked snapshots cannot silently cross that implementation boundary.

The practical recovery default should be **preserve old state, select inert
mathematics, initialize a fresh owner under an independently approved successor,
and independently check the selected closure there**. Reuse an already retained
complete inert bundle when possible; otherwise the new selected-export companion
provides the needed custody-to-bundle operation without reopening the old owner
or executing Lean. This is a source-supported composition of existing interfaces,
not evidence that a checker-upgrade recovery has been executed.

There is no already-supported arbitrary runtime upgrade. The delivered source
route fixes Windows x86-64 Python 3.14.6, Lean 4.34.0 and specific runtime pins.
A genuine checker fix needs a separately reviewed supported successor first.
Changing a pin or a version string is not that work.

The smallest current release obstruction in this area is the missing explicit
operator update/recovery policy tying these existing routes together. It should
distinguish three identities and state what must be preserved. A generic updater,
whole-corpus replay campaign or crypto migration mechanism is not justified by
the present evidence. A concrete future checker fix may reveal a smaller
implementation compatibility change; no such fixed successor is selected here.

## The identities must not be conflated

Let `P` be the complete installed owner PROFILE, `I` the core implementation
claim, `S` the portable semantic contract, and `A` the module-anchor support
identity. They serve different purposes.

| Change | Existing behavior and required interpretation |
|---|---|
| Transport, search or presentation changes `P` but leaves `I` unchanged | A newly approved package can reopen the existing checked catalog. This is intentional, not silent cross-checker trust. Compatibility and execution safety of the new package still require approval. |
| Kernel, admission controller, native adapter, basis receiver or snapshot support changes `I` | Existing catalog adoption bytes no longer match. Opening the old catalog under the new implementation refuses. Use fresh checked state or a separately justified migration; none is inferred from equal `S`. |
| Only anchor-relevant support changes `A` | Catalog acceptance may remain valid when `I` is unchanged, but an old module anchor cannot be used as a warm cut under the new `A`. New realization is separate from core acceptance. |
| Foundation, interpretation, axiom/extension policy or selected Lean revision changes `S` | Old unit/export identities are not current-contract claims. Existing intake refuses a semantic mismatch. Exact-byte transfer alone is insufficient; a reviewed translator or re-export/recheck path would be needed. |
| Support or state might have been modified by a same-account adversary | Stop relying on affected local warrants even if saved hashes and identifiers look unchanged. Re-establish trust independently; equal hashes stored in the compromised domain do not establish this premise. |

A byte difference is an identity change, not by itself a semantic incompatibility
proof. Conversely, a familiar version number, identical statement text or equal
semantic claim is not proof that a new implementation is sound. The installation
descriptor explicitly *claims* conformance; approval must justify the actual
implementation and protected-state assumptions.

The fresh archive installation illustrates the distinction without simulating
an upgrade: it generated a different final PROFILE while retaining exactly the
same installation manifest. Two linked exporter executables differed only in
parsed PE timestamp fields. That result supports fresh build/install plumbing,
not a new checker, migration, mathematical recheck or policy equivalence theorem.

## Actual source boundaries

For the following table, `P/` is the exact default package:

`experiments/v5-local-checks/transport-release-handoff01/suite/assembled/package/`

Its selected PROFILE is
`b047d4492da79e363fcd154144a6d9088a93100fde7aac3c385f3a296a41dad7`;
the installation manifest is
`32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.
These are references to the existing selection, not new approval by this note.

| Source | Concrete behavior |
|---|---|
| `P/profile.py:156` | Selects exact PROFILE bytes, verifies all declared auxiliary payloads, checks exact installation manifest, then opens installed support. Whole PROFILE is not the catalog's acceptance key. |
| `P/installation/py/ordinary_admission.py:85`, `:158`, `:224` | Support digests commit selected file bytes; controller support also commits roles/search layout. Required kernel/native/basis/controller/snapshot groups are checked and their union covers the selected manifest. Selected runtime attachments are checked; this is not a hermetic toolchain claim. |
| `P/installation/py/ordinary_semantics.py:53`, `:86`, `:140`, `:216` | Foundation and semantic contracts are exact fixed descriptors. `I` commits `S`, platform and support digests; local roots commit `I`, store identity, parent and request. Only the current Lean 4.34 snapshot format is recognized. |
| `P/installation/py/portable_catalog.py:145` | Catalog marker contains exact implementation and limits. `CATALOG_ADOPTION` and database-lineage checks reject a mismatched implementation before using old roots. Activation separately binds `S`, foundation, `I` and store. |
| `P/installation/py/portable_catalog.py:391`, `:530` | Native snapshot provenance must contain the current `I`; root/operation lineage and exact artifact bytes are checked. Context reuse checks stored artifacts, not a fresh proof of all prior mathematics. |
| `P/installation/py/ordinary_admission.py:552`, `:568` | Fresh initialization constructs/checks the selected basis. Admission redoes preflight, stores inert evidence and checks new units. `REUSED` requires an already warranted receiver-local context; copied producer reports cannot create it. |
| `P/authoring/py/module_export.py:30`; `P/authoring/py/anchor_store.py:304`, `:694` | Anchor support is separately committed; record loading requires exact support equality. Query-only changes are deliberately excluded from the narrow support descriptor; owner/loader changes are included. |
| `P/reference/baseline_intake.py:159`, `:266` | Bundle semantics must equal receiver context/installation semantics. Intake checks batches against the chosen local root; failures can leave a confirmed prefix or an uncertain final commit. |
| `software/v5/ordinary_selected_export/export.py:25`, `:164`; `selected_export.py:154` | The separate exporter selects known parser/helper source, reads bounded custody and follows all imports/atomic siblings. It does not open a catalog or load Lean. It is not a universal converter for future formats. |

There is historical V1-to-V2 import machinery in the portable catalog, but the
existence of an import record does not establish a general checker-upgrade
migration. `portable_catalog.py:717` explicitly requires separately authenticated
origin/translation facts; the ordinary owner command surface does not offer an
arbitrary implementation-migration operation.

## Conditional safety argument

Assume protected owner storage, independently approved selected support, an
uncompromised execution environment, correct checking/admission implementation,
and the stated hash/serialization assumptions. These are real premises, not
conclusions obtained from a PROFILE digest.

1. A checked local root accepted under implementation `I_old` has an adoption
   marker and provenance bound to `I_old`.
2. The current opener computes its marker from `I_new` and requires exact equality
   with both the retained marker and database marker. Root validation separately
   requires current implementation provenance.
3. Therefore, when `I_new != I_old`, this ordinary opening path cannot turn the
   old root into a new-implementation warrant. It refuses instead.
4. A fresh owner has no old nonbasis acceptance to reuse. Intake starts from its
   freshly checked basis or an explicitly chosen root previously checked there.
   Portable bytes are merely candidates; each new batch must pass actual native
   checking and clean-event/record validation before catalog commitment.
5. Consequently, successful fresh intake provides a warrant relative to the new
   checking assumptions, without using the old checker's correctness as a premise.

This does not prove the new checker correct or make all old statements invalid.
A checker bug means affected warrants no longer justify the intended assurance;
many old statements may still pass the corrected checker. Preserve both outcomes.
If the bug's affected set cannot be justified, do not use an alleged unaffected
old snapshot as the fresh recovery basis.

Changing only `P` does not imply step 3: unchanged `I` deliberately permits
catalog reuse. This is appropriate for a transport-only update *only if* neither
the earlier defect nor the new code invalidates the protected-state/checking
premises. A remote-execution vulnerability can invalidate those premises without
ever changing the installed checker bytes. Source classification, not filenames
alone, determines the required trust reset.

## Practical recovery sequence, without inventing a new protocol

1. Stop the affected owner's services and serialize operations. Preserve old
   diagnostics and state. Do not edit its ADOPTION, implementation identifiers,
   receipts, `.olean` records or pins to force a new package to open it.
2. Independently approve a supported replacement package/runtime. If none exists,
   stop here for mathematical acceptance; data preservation/export may still be
   possible through separately approved safe tools. Do not execute an executable
   known to be compromised merely to obtain its success report.
3. Select exact desired target locators and a retained complete inert bundle.
   If no bundle exists, use the independently approved selected exporter on
   intact supported custody. It follows all imports, including proof-only imports
   and atomic siblings, down to the fixed basis. It does not need an old acceptance
   report. The current helper still needs its known supported parser/package
   files, so preserve them as data and assess their safety separately.
4. Initialize a genuinely fresh catalog and custody under the approved successor
   in separate owner-controlled locations, using a fresh store identity. Keep old
   and new trees distinct. Never copy old catalog snapshots or module anchors into
   this fresh owner as substitutes for checking.
5. If `S_new == S_old` and the successor supports the unchanged inert bundle
   format, use the existing direct `intake-baseline` route with the **new owner's**
   selected parent. Follow `ordinary_selected_export/INTAKE.md` for exact flags,
   clean closure, manifest/state/profile bindings and partial-prefix semantics.
   If semantics differ, refuse this shortcut and design the specific conversion
   only once the target semantics and fix are known.
6. Select the actual new successful root and republish/recreate local module
   realizations deliberately. Old context roots, native `.olean` paths and anchor
   IDs are historical references, not new receiver authority. Inert unit/export
   IDs can remain identical when `S` and exact evidence bytes remain identical.

The existing guide's statement “same receiver/profile” is a safe report-selection
discipline. It must not be misread as “every PROFILE change invalidates every
theorem,” nor as permission to transplant a report to a fresh receiver.

## Preservation and failure limits

Preserve the complete closed old catalog (marker, database, operation/import
artifacts and anchors), complete custody, original limits/configuration, exact
source/package/runtime selections, diagnostics, target locators and retained
inert bundles. The whole catalog is useful for diagnosis and possible justified
recovery, not required authority for fresh intake. Retain authored project sources
and dependency selections for work that has never been exported to custody.
Git does not contain ignored state/runtime/evidence and cannot replace this data.

Never copy a live database and call it a consistent backup. Require quiescence or
a separately specified consistent backup route; preserve journals rather than
deleting them. The selected exporter intentionally refuses journal/WAL/SHM
states. It does not repair damaged custody or sandbox an attacker-controlled
SQLite database. If only `.olean` snapshots survive and inert evidence/source is
gone, this route cannot manufacture independent proof evidence; reacquisition or
separately trusted recovery is needed.

## Cost, smallest alternative and stop rule

Recovery is demand-selected, not a global recheck of every theorem on the network.
For target set `T`, let `C(T)` be the complete selected evidence closure down to
the basis. Export cost is bounded reads/hash/parsing plus copied bytes for this
closure and its locators. Fresh intake costs basis initialization, full checking
of the selected new units, snapshot/metadata work and retained storage. Proof
work within an invalidated trust boundary cannot honestly be omitted just because
old theorem statements have the same identifiers.

The current selected exporter caps the closure at 1,024 units / 64 MiB with
additional nodes, names, edges and locator limits. These are refusal ceilings,
not arbitrary-scale recovery. Intake's 60 CPU seconds per batch is a reservation,
not a measurement or a promise that two batches fit a 120-second outer budget.
Do not raise caps or buy a full recovery campaign before a real selected workload
hits a relevant boundary.

The cheapest alternative is to use an already preserved complete inert bundle
and the existing fresh-init/intake commands: no new exporter, migrator or proof
system is then needed. If a reviewed update genuinely leaves the checking and
protected-state assumptions unchanged, ordinary same-`I` reuse is cheaper still.

Stop this work at the explicit decision/recipe boundary until there is either
(a) a concrete supported checker fix with a particular changed trust boundary,
(b) a real recovery blocked by the existing routes, or (c) release packaging that
needs this policy exposed. Only then select a minimal changed-boundary test or
implementation. Do not launch a pretend runtime upgrade merely to accumulate
another passing checkpoint. The existing archive-install and selective-export
outcomes are sufficient for their actual scope, not an executed update claim.

## Related reviewed material

- `software/v5/ordinary_release_bundle/README.md` and `ADOPTION.md`: current source,
  runtime and default-package selection; no arbitrary-version promise.
- `software/v5/ordinary_bounded_transport/EXECUTION-TRUST.md`: supported trusted
  project execution, protected-state premises and suspected-compromise response.
- `software/v5/ordinary_selected_export/ADOPTION.md`, `README.md`, `INTAKE.md`:
  bounded inert export evidence and exact independent-intake instructions.
- `software/v5/ordinary_archive_install/OUTCOME-AUDIT.md`: full fresh archive
  installation, same core manifest, different generated PROFILE, no mathematics
  or owner-state transition executed.
