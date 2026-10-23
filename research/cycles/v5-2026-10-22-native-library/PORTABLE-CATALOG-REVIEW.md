# Portable catalog: independent source review

2026-10-23. Reviewer: `admission_event_audit`. Source-only review; no tests,
native processes, catalog opening/mutation, migration, or Git operation run.

## Disposition

No blocking defect found in the reviewed catalog's **conditional owner-local
storage boundary**. This is clearance for focused changed-boundary controls,
not importer adoption, a native checking result, or final-v5 acceptance.
The catalog deliberately does not establish source eligibility, correspondence
or a clean worker event. Those are obligations of the actual trusted importer
and native controller; their implementation and eventual integration need their
own concrete review. A caller-controlled file or compatibility assertion is not
a warrant merely because this catalog can parse it.

| Reviewed source/context | SHA-256 |
|---|---|
| `software/v5/ordinary_lean/portable_catalog.py` (complete source) | `2d0e91b2920abb69304b920a676da202a5e2444ddec37805d19e953b69eebf35` |
| `PORTABLE-CATALOG-CONTRACT.md` (complete contract) | `26553e975ca5dbb788fe6a217e4ecf1e07144a74ac553fd4eae3604fa6ab993b` |
| `PORTABLE-SUPPORT-CORRESPONDENCE.md` (complete argument) | `ade45957f49d7078c46819dd020cda5c63d19d879571f4b958d6b5ede6386fba` |
| `ordinary_semantics.py` (complete selected identity definitions) | `ee601536f53640a2695e51d37d3e87e6746604ed6433cb3ace9349ae1aedf915` |
| `portable_evidence.py` (complete reader) | `f8ea819bdd9344d696cef2725888828125b2ef5d1b60d2c31a0412657a62cbd8` |
| `local_catalog.py` (retained utility/premise context; focused source read) | `860a9d731290b2a7fbacd4852bb68185516329ee42845648f4ba3c3856d7c751` |
| `OrdinaryWorkflowWorker.lean` (exact plan/extend/report source seam) | `442c2d479d4df6b1c7ee456cb521b8c760b54258a3f8d5fb71a15fa391c77f9b` |

Paths without directory prefixes in this table are in this cycle or, for Python
and Lean files, `software/v5/ordinary_lean`. No claim is made about a later edit.

## Authority and identity

The portable semantic/foundation pair is independent of local implementation,
store, grant and snapshot IDs. The active catalog marker, implementation claim,
platform and limits remain exact local bindings. The source uses composition
with V1's path/lock/size helpers, not inherited V1 admission methods.

`reserve_extension` reparses immutable V2 bytes, matches the selected S, resolves
every complete ordered direct-import binding against the parent/earlier batch
prefix, derives new export IDs and refuses overwrites. A parsed identity is
still only a proposed addition. `_commit_checked` is private and explicitly
requires the exact actual clean worker event; a saved report cannot establish
that prerequisite. Its immutable live grant binds ordered unit IDs, batch hash,
output bindings, new module name, actual parent module and full parent plan.

New-native and retained-import roots have distinct formulas and origin variants.
Retained roots bind source profile/store/root/parent/operation/record bytes,
source checking support and separate translation support. Native roots bind a
committed operation in this catalog and the current implementation. Neither
origin silently becomes the other. Basis-name count checks are syntactic guards:
the actual native basis worker or authenticated fixed inventory is still needed
to establish membership in the foundation.

## Actual native module relationships

The crucial compatibility fact is preserved: old snapshots keep their original
embedded module names and parent-module names even though V2 local root handles
change. Imported records require those names to be derived from the retained V1
root/parent, and `_context_rows` checks them against the preceding actual module
in the selected chain. New-native roots instead use their new grant's module
name and its exact actual parent module. No imported artifact bytes are rewritten.

The returned plan's five module fields match the retained worker's `decodePlan`
schema. That worker restores the explicit plan and checks only the supplied raw
new units; it does not interpret envelope V1/V2 identity hashes. It reports the
actual parent module used. The future controller must therefore compare against
the grant's `parent_module_raw`/plan, not recompute a module from a V2 parent
handle. The current V1 `run_successor_admission.py` is not retroactively a V2
controller and remains unchanged by this review.

## Import activation and interruption

`_create_importing` creates a fresh quarantined destination and a nonresumable
live import grant. Its deadline is established before catalog creation and
clamped to the caller's parent deadline. Normal opening, context lookup, basis
reservation and extension reservation reject `IMPORTING`. No reopening can
recreate its in-process grant or renew its deadline.

Activation validates the complete ordered root-record manifest and chain, exact
source-record and artifact bindings, actual parent modules, support-set union
and correspondence-file digest. It does not parse the audit as mathematical
authority. It bounds and flushes the retained file tree before promotion. The
trusted source recheck is called before the transaction and again immediately
before activation; the same live grant/deadline is rechecked afterward. The
source must remain locked and eligible throughout, and the callback itself must
be bounded by the importer's allocation.

One transaction installs the import record, complete root chain and `ACTIVE`
record. In-transaction failures attempt rollback, close the catalog and require
explicit reopen inspection. Reopen accepts only `ACTIVE`, validates the exact
activation/import-record binding and walks the imported selected chain. A crash
leaving missing files is refusal, not partial activation. No retry or source
mutation is implied by this storage seam.

## Integrity, withdrawal and limits

The implementation preserves ordinary nonaliased paths, single-file checks,
Windows owner locking, bounded SQLite DELETE/FULL storage and bounded record,
name, batch, artifact and operation counts. Paths read as artifacts are first
equated to catalog-generated paths. Failed/reserved work is retained and charged;
reopening interrupts reservations rather than authenticating saved events.

Snapshot hashes are verified once per owner process, then cached. This relies
on the stated protected-owner-state/OS immutability premise; it is not general
adversarial in-process file replacement or arbitrary database-tampering detection.
Likewise, rollback protection is a stated premise, not supplied by SQLite hashes.
The metadata integrity checks do not replace original acceptance authority.

Whole-store `WITHDRAWN` is checked on open/context and before promotion and is
sticky in the live object. Imported retained-support dependencies are preserved.
An owner learning that any such support is withdrawn must quarantine the active
V2 store; the code does not automatically watch subsequent changes to an archival
V1 withdrawal marker. This matches the explicit contract and avoids inventing a
second permanent source-catalog authority. It should remain an operationally
visible rule.

Context reconstruction still visits the selected local chain and a fresh worker
loads that selected context. Portable IDs and translated metadata do not establish
constant-cost cold use, arbitrary branch merging, discovery completeness or
useful growth. Those unresolved claims should not be attached to this change.

## Highest-payoff next discriminators

Use small inert storage controls for the new boundaries: rejection of unactivated
destinations and forged/reopened/modified grants; exact imported module preservation
and new-child parent binding; import/native origin confusion and changed manifest
refusal; deadline and source-recheck failure before activation; withdrawal and
reopen after incomplete/uncertain state. Such tests establish storage behavior,
not mathematical validity. The subsequent decisive integration is one actual
small new checked extension above the eligible imported parent, with unchanged
old snapshots and no old-proof replay. Do not rerun the completed pure identifier
translation or seven-unit reciprocal campaigns.

## Saved focused-controls outcome

Root subsequently ran `ordinary-portable-catalog-controls-01` once. This reviewer
read its complete saved test source, selection, stdout and supervision result;
all nine snapshotted source hashes and three explicit Python runtime hashes match.
No test was rerun and no test or accepted catalog was opened by this review.

- Selection: `6f61fd9a12870c37223680e077c8251025571f0f705280da8c181c78697f4a3e`.
- Result: `c085c5ccc0b7d40b1362f574153da342d0101ad1a9656a5787a3979d767e3e0b`.
- Test source: `98af957a970b75fcac0122020f6b469e56cf9d3ee099806c35343e1b317b4dac`.

All five groups passed: IMPORTING refusal/closed quarantine; full activation,
original-module preservation and immutable child-plan/grant checks; incomplete
manifest/support or missing snapshot refusal; in-transaction second-source-recheck
failure with rollback/closed authority; changed implementation and active-store
withdrawal refusal. The harness asserts expected refusal codes and retained empty
quarantine tables; these are not success messages printed without checks.

The actual saved process result has exit zero, direct-child reap, zero final
active processes, closed Job, no cleanup errors, empty stderr and no termination
request. Known inclusive CPU is **2.015625 seconds** (1.859375 Job + 0.15625
wrapper), with a 25,804,800-byte peak Job private commit. The nested wrapper-
supervision counter is not added a second time.

The fixtures intentionally use unproved synthetic snapshot bytes and private
storage-only commit/activation calls. Both source and output explicitly state
`mathematical_acceptance=false` and `migration_qualified=false`. This is the
selected changed-storage-boundary pass, not an actual eligible import, native
extension, discovery/growth result or public release.
