# Updating software without silently transferring mathematical trust

This policy accompanies the current [ordinary source handoff](../../START-HERE.md).
It describes existing checks and a conditional recovery procedure, not an automatic
updater or an executed checker-upgrade test. Keep the current installation and its
evidence intact. The supported runtime profile is still Windows x86-64, Python
3.14.6 and Lean 4.34.0 with the selected pins; arbitrary version upgrades are not
currently supported. Licensing and external distribution remain undecided.

## Decide which trust boundary changed

The package PROFILE identifies all selected package files. The checking
implementation identity separately binds the kernel, checking adapter, basis
receiver, admission controller and snapshot support. The portable semantic
identity states what the inert mathematical data means. These are not interchangeable.

| Situation | Correct action |
|---|---|
| A reviewed transport/search update changes the package but not checking or protected-state assumptions | Approve the new exact package. Existing catalog reuse is allowed when its checking implementation remains identical. Use the new actual PROFILE for new operations; never rewrite old reports. |
| A checker, admission or snapshot implementation changes | Ordinary opening rejects old catalog adoption. Use fresh checked state and independently check selected inert mathematics; do not change the marker to force compatibility. |
| Only module-anchor support changes | Existing mathematical acceptance may remain usable, but an old anchor cannot be assumed to be a valid warm reuse point. Recreate the realization through the supported new route. |
| The Lean revision, foundation or portable semantics changes | Do not feed old claims to new semantics by changing their identifiers. A specific supported conversion/re-export and checking path is needed. None is implied by this guide. |
| The owner account, checker or local state may have been compromised | Suspend reliance on affected warrants even if stored hashes match. Re-establish trusted execution and clean state independently. A same-account attacker can alter both data and its recorded hash. |

A changed hash is not proof of incompatibility; an unchanged hash is not proof
that the environment was protected. Classify the actual defect and support change.
For example, a transport vulnerability that allowed arbitrary local writes can
invalidate stored warrants even though the kernel itself never changed.

## Recover selected mathematics, not the whole network

1. Stop the affected service and serialize local operations. Preserve the closed
   old state and diagnostic evidence. Never delete locks, database journals or
   unsuccessful operation records to force a restart.
2. Independently approve a supported replacement implementation and execution
   environment. If no trustworthy supported replacement is available, do not
   resume mathematical acceptance using the suspect checker.
3. Prefer an already retained complete inert bundle. Otherwise use the separately
   approved [selected exporter](ordinary_selected_export/README.md) against intact
   supported custody. It does not open the old acceptance catalog or execute Lean.
   It still runs trusted parser code and is not a sandbox for a hostile database.
4. Initialize a fresh owner/catalog/custody in separate protected locations under
   the approved replacement. Do not import old native snapshots or anchors as
   proof of acceptance. Its basis must be established by the new implementation.
5. If portable semantics and bundle format remain supported and identical, use
   [direct intake](ordinary_selected_export/INTAKE.md) with the **new owner's**
   parent root. Check the actual reports, manifest/state/profile bindings and
   supervisor closure. A failed intake can leave a checked prefix or an uncertain
   final commit; it is not atomic rollback and must not be blindly retried.
6. Publish only after obtaining the new actual accepted root and exact target
   locators. Recreate local compiled modules/anchors as needed. Old reports and
   root identifiers remain historical, not authority for the new owner.

If the bug's affected set cannot be justified, an allegedly unaffected old
snapshot is not a safe shortcut for step 4. Conversely, discovering a checker bug
does not show that every old theorem is false: it removes an assurance premise,
which successful independent checking can restore under the replacement's premises.

## Preserve data and expect real checking costs

Keep the complete closed old catalog and custody, marker/database/operation/import
artifacts, anchors, original limits/configurations, source and runtime selections,
diagnostics, exact target locators and inert bundles. Retain authored project
sources/dependency selections, especially for work never exported. Git does not
contain ignored runtime/state/evidence and is not a replacement for those files.
Do not label a live database copy a consistent backup. The selected exporter
deliberately refuses journal/WAL/SHM states; it is not a repair utility.

The procedure checks the selected proof closure, including proof-only dependencies
and atomic siblings, not all mathematics in the world. Its cost includes basis
initialization, selected proof checking, metadata/snapshots and custody. The current
export helper has finite size/unit limits and may refuse a large request. If only
compiled snapshots survive and inert evidence/source is lost, this procedure
cannot manufacture the missing proof evidence.

The source rationale and implementation-review evidence are retained in the full
project, outside this source distribution. The [workflow guide](../../START-HERE.md)
explains this evidence boundary; those research files are not operation inputs.
No migration campaign, actual checker update or expanded platform support is
claimed. Hash checks establish selected identity, not checker correctness or
authentication of a release received from an untrusted source.
