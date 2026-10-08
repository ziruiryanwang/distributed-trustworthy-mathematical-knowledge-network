# Source08: minimum final local release handoff

2026-09-23. Read-only release-consolidation review by
`v1_central_gap_checkpoint`. Canonical AGENTS read and workspace guard passed.
Only this checkpoint is written. No product import, build, test, service,
runtime invocation or source mutation. Source08 qualification is **not assumed
to pass**. The [convergence decision](2026-09-23-release-convergence.md) controls:
finish the selected mixed-role gate, then consolidate, not add mechanisms.

## Decision

After independently audited source08 qualification, deliver **one authoritative
locally qualified Windows v1 source candidate** with a self-contained startup
page and an exact-cut support report. Reuse the actual tested source archive;
do not repackage merely to replace an internal status label. The packager's
`DEVELOPMENT_SOURCE_PACKAGED_UNQUALIFIED` result is historical packaging evidence;
the companion report supplies subsequent behavioral qualification.

Current standalone operator and agent instructions already describe the core
workflow. What remains central is to bind those instructions, the exact tested
software, practical prerequisites and honest evidence in one usable handoff.
This is more than announcing one additional feature test. It is not a claim
that all mathematical software, machines or research workloads are supported.

## Minimum deliverable, not another registry

Use one new delivery directory, for example
`deliverables/2026-09-23-local-v1-source08/`, without changing the canonical
project root or creating a second editable source tree. Its minimum files are:

| File | Required content / source |
| --- | --- |
| `math-commons-source.zip` | Exact bytes from the source08 package actually extracted/built/tested; no credential, runtime, used database or scratch state. |
| `SOURCE-MANIFEST.json` | Exact external copy of that archive's embedded manifest; 114 payload identities. |
| `PACKAGE-RESULT.json` | Original successful packaging record, not edited to claim later acceptance. |
| `START-HERE.md` | Actual archive/manifest pins and sizes; prerequisites; fresh-install route; agent/API route; no external publication/license claim. |
| `RESULTS.md` | Manifest-bound support/evidence report, including unchanged-code basis, new executed gates, failures, costs and limitations. |
| `HANDOFF-INTEGRITY.md` | Final read-only archive/member/hash/link/document checks and exact checked scope. |

The three package artifacts may be byte-copied and verified; do not rerun their
builder. Do not make basic use depend on links back into `product-local` or a
research harness. START-HERE should tell a recipient to open the extracted
`TLS-WALKTHROUGH.md`, then `AGENT-QUICKSTART.md`/`API.md`. Historical audit links
may point to the preserved project evidence, but RESULTS must state its own
actual conclusions and caveats rather than requiring that entire history to
understand the support promise. No second archive format, installer, portal,
container, protocol version or comprehensive evidence export is required.

## Exact actions and readiness conditions

1. **Close the already selected gate.** Require the actual source08 native-free
   audit, fresh package/support build, installed mixed-publication/custody
   discriminator and independent terminal outcome audit. Preserve every
   failure, original result and charge. An audit must bind fresh Beta publication,
   distinct acquired-only D1 entry, actual managed service and fresh receiver
   admission of both; the producer's source submission is not a new theorem-
   discovery result. Do not repeat operator05, contact06 or custody07 runs.
2. **Freeze the actual candidate.** Check the complete source07-to-08 map and
   package map, not only edited files. At this review the intended delta is
   thirteen changed / 101 unchanged payloads, including ten documents; the
   mathematical checker/native/assets, schema, wire/TLS and supervisors are
   unchanged. If the final reviewed map differs, explain it before selection.
   The installed harness must use that final map, including late doc changes.
3. **Assemble the six-file handoff.** Copy the actual source08 packaging trio,
   write START-HERE and RESULTS using final measured pins/outcomes, and leave
   the tested package/source/installations untouched. No second native build is
   necessary solely because the ZIP acquired a delivery-directory copy.
4. **One final static integrity pass.** Compare archive, embedded/external
   manifest and each of 114 payloads, with 115 unique ZIP members and no extras.
   Verify copied package result; verify operational document links, strict UTF-8,
   code fences and conspicuous placeholders against the actual interfaces.
   Check selected delivered content for credentials; known-key scans must be
   labeled as such, not universal secret-detection claims. Record exact scope
   and pins. Reuse existing successful cleanup receipts; a read-only current
   process/listener check may supplement them without starting new services.
5. **Unify live navigation.** Root README, GOAL's immediate step, NOW and WORK
   must point to the same frozen candidate and handoff. Root has already begun
   correcting stale README selectors. Old dated deliverables and failure records
   remain unchanged and labeled historical. Keep the canonical workspace guard;
   reopening the app at the correct cwd remains separate from package readiness.
6. **Hand over the usable artifact and its limits.** Give the user the one
   START-HERE link, archive link, actual scoped outcome and remaining release
   restrictions. Do not declare the ultimate global-commons goal complete or
   immediately replace delivery with another optional feature investigation.

## What START-HERE must make actionable

- Supported profile: Windows x64, fixed local NTFS/cooperative owner domains,
  PowerShell 7, complete Lean 4.34.0 Windows runtime and selected Python build
  with SQLite 3.50.4; always `-B -E -s -S`. Runtimes are not bundled and no
  third-party Python dependency install is part of this package.
- Give this machine's actually selected runtime locations and recorded
  executable integrity/version identifiers, explicitly as local supplied
  prerequisites. An executable digest is not attestation of an entire runtime
  distribution. Do not advertise an untested arbitrary Python installation or
  invented clean-machine download recipe as compatible.
- Fresh extraction/build/configuration/state/scratch; never overlay bound
  installations or copy test databases/keys. Config 6 / physical database 5,
  wire/catalog 2 and stage-plan 2. Source08 also needs a new bound installation
  despite reusing those version numbers. Use the packaged identity helper for
  owner-created keys; do not make test credentials part of the deliverable.
- The available command route is operator build/configure/init, then agent
  find/acquire/admit/inspect/reuse/submit/publish/expose. The agent chooses the
  mathematics; there is no required human-intention field or global task list.
  Publication/custody/discovery/TLS never substitute for fresh local admission.
- Hosting is a separate finite owner action. The walkthrough's singleton
  three-connection grant is not sufficient for two bundles; it already states
  four successful connections for one two-entry page. Preserve this distinction.
- Continue with status, explicit renewals, historic-context selection and
  newly funded service when supported. Preserve exact request bytes and stop
  on uncertain/pending outcomes. General restore/migration is unsupported;
  plan exposure before irreversible exhaustion. No silent resets or auto-retry.

## Lean coverage: usability envelope, not a hidden whole-mathematics claim

The software is extensible by checked declarations within its selected capture,
foundation and resource profile; it is **not** restricted to replaying a fixed
list of demonstration theorem IDs. Existing independently authored operator05
contributions substantively use acquired results, and the preserved Init
`Fin.castLE_castLE` case shows one actual library/private-helper closure.
These are positive usefulness/operability examples, not broad-library coverage.

API source elaboration exposes selected `Init` syntax/macros/tactics, matches
imported shared declarations to the checked inventory, captures required
dependency closures, and reconstructs on fresh foundation-only replays.
Additional axioms, unsafe or unsupported declarations and oversized closures
refuse. Source may be valid Lean yet outside this product profile. Five common
packages count toward the at-most-sixteen-package context; a successful parser
or arbitrary mathlib import is not a compatibility guarantee. The library
result explicitly did not qualify every external inductive/recursive family,
class/instance registration, notation restoration, all Init or mathlib.

For a bounded research-network **candidate**, this is a support envelope, not
an automatic demand for another broad mathematics campaign before handoff.
RESULTS must disclose it prominently and identify the pinned foundation/assets.
It becomes a real release blocker if instructions promise arbitrary Lean4 or
mathlib compatibility, require an unsupported feature to perform their stated
basic workflow, or claim to contain the whole body of mathematics. Those claims
would be false; silently relaxing the acceptance boundary would not fix them.
Broader interoperability is later capability work, not proof of perfection
required to distribute this honestly scoped local candidate.

## Blockers versus caveats

Real blockers to this handoff are a failed/unreviewed selected gate, source/
archive/evidence mismatch, unresolved selected-run cleanup, missing actionable local
prerequisites, a broken required command, leaked credentials, or contradictory
current source selection. Fix a concrete such defect; do not add a new gate
merely because another unproved property can be named.

No second host is available. Same-host qualification is sufficient for the
declared local handoff, not evidence of independently administered deployment,
NAT/firewall behavior or public-network availability. License remains explicitly
undecided: it does not prevent preserving/delivering the owner's local artifact,
but no public redistribution permission or open-source release is granted.
No external publication, dependency download, public bind or remote deployment
is authorized by this checklist.

Conditional retention, manual trusted contacts, finite node/catalog/work limits,
general crash/restore/migration gaps, limited retrieval coverage, unmeasured
whole-agent comparative efficiency and unproved sustained/exponential growth
remain visible caveats. They are not silently closed by source08, and under the
selected bounded candidate claim they are not invitations to delay this handoff
behind migration, ranking, global indexing, identity or SNARK development.
