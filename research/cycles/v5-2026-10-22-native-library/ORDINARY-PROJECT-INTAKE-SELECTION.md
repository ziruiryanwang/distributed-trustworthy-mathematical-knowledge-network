# Approved-project intake: implementation selection

2026-10-24. Root decision; source implementation only at this point.

## Why this change

The real workflow is a contributor using a normal Lean project whose new proof
mentions a lemma not yet accepted by the receiver. Current public extraction is
restricted to installed Std. Adding explicit approved local artifact selection
removes that artificial restriction while preserving complete proof extraction
and independent checking. No project is supplied by the user; a later controlled
compatibility check must not be presented as external-user benefit.

Root read the exact contract `ORDINARY-PROJECT-INTAKE-NATIVE.md` (SHA-256
`9463907393807d77c1a16f1fbe1dbefad29fb06df56c9348a25ae94d5135d339`). Adopt its
same-parent, exclusive-mode API and remaining-capacity rules for implementation,
subject to independent source challenge before execution.

The strategy comparison recommends this thin seam before a generic cold intake
scheduler. The saved ReadFootprint closure has 2852 units / 49,499,157 bytes,
which cannot fit the current 32-unit / 4-MiB public completion boundary. Looping
that operation is not a valid scheduler: it changes the accepted context, needs
explicit retained-candidate rebinding, and repeats growing-context work. Do not
implement such a loop or run the saved closure again. Conventional pinned-library
sharing remains the appropriate comparator/default for common approved background.

## Disjoint ownership

All paths below are relative to the sole canonical root
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

| Owner | Fresh editable files | Scope |
|---|---|---|
| project_intake_native | `software/v5/ordinary_project_extraction/MissingImportExporter.lean` | Exact project native request, private runtime-first import, capacities; preserve old Std request and shared codecs/exporter |
| cold_intake_strategy | `software/v5/ordinary_project_extraction/library_extraction.py` | Approved selection, exclusive modes, retained-input capacities, existing completion/exchange/accounting |
| root | `software/v5/ordinary_project_extraction_package/owner.py`, README and later recipe/map | Explicit public `extract-project`, same existing loader/core, no implicit admission or authority migration |
| module_anchor_audit | `ORDINARY-MODULE-ANCHOR-SOURCE-REVIEW.md` | Independent exact contract/source challenge; no duplicate old tests |

Authors save implementation notes in `ORDINARY-PROJECT-INTAKE-NATIVE.md` and
`ORDINARY-COLD-INTAKE-STRATEGY.md` respectively. Root owns NOW/WORK and Git.
Used predecessors, package04, existing states, source pins and failures remain
unchanged. No shared `OrdinaryExport`/codec/receiver modification is selected.

## Decision-changing evidence, not a campaign

First resolve source review of request grammar, unit/node/byte limits, protected
lookups and clean accounting. Then separately select focused pure controls and
at most one small non-Std import discriminator. Reuse unchanged acceptance
evidence. No large-library run, download, new certificate or full dependency
rebuild is selected. Changed native compilation should reuse exact retained
shared objects if compatible; no executable is adopted merely because it links.

Changing the owner facade deliberately changes anchor support identity. This
must be reported, not silently migrated. Do not rerun old anchor acceptance as
part of this narrow intake check. Current installed development selection remains
package04 until the new integrated payload has separate evidence.

The payoff is broader ordinary interoperability and earlier capacity refusal,
not cheap arbitrary cold onboarding, mathematical novelty, full project semantic
equivalence, measured growth, or completion of v5.

## Source-review amendment: generated module compatibility

Before any runtime, the integration author found that our generated public module
`DMKNBridge_<64 hex characters>` has a 75-byte component. The proposed 64-byte
project component ceiling would reject the product's own existing artifacts.
Root therefore selects a 96-byte component ceiling for the new project mode only,
with unchanged ASCII identifier/reserved-name/aggregate grammar. Existing Std
mode stays at 64. Native/controller/contract and focused boundary controls must
agree before use. Preserve the saved artifacts; do not rename or rebuild them to
make the test pass. This is a source compatibility correction, not a relaxed
mathematical checking rule or a previously executed failure.

## Source integration checkpoint

Root read the complete controller/native/facade deltas and the clean-builder
delta. Fresh controller `cd79d905`, native `437caa5a` and facade `2d4de791`
implement the amended project-mode grammar. The facade passes explicit local
selection bytes and their pin; it never obtains approval from the candidate.
Independent review precedes execution and may still require source corrections.

The new clean-source recipe is
`software/v5/ordinary_project_extraction_package/build.py`, with
`source-map.json` hash
`bfa391fb27df944179f256a48aaf268833862084bc14632943adf0f2a9b5cc3f`.
Root's read-only map check found all 71 source length/hash pins equal current
bytes, 54 direct copies and unchanged 47 base inputs. This is not compilation.
The recipe remains available for distribution reproducibility; it is not selected
for a full build now.

The native author additionally owns fresh `assemble.py` / `select_build.py` in
that package-source directory. They will compile/link only the changed native
entry against the five exact retained shared objects, then replace exactly three
package payloads. Proposed output is
`experiments/v5-local-checks/ordinary-project-extraction-build-01/integration/package`.
Source review and a separate root finite selection remain necessary.

The controller author owns source-only `project_check.py` /
`select_project_check.py`: three public calls using the saved initial basis and
already generated approved module, a new retained missing-proof contribution,
explicit project extraction, then real independent completion. The reviewer owns
focused pure/inert controls. No shared-owner operations may overlap. Immutable
saved evidence, anchor records and past failures remain held unchanged. The new
test must not use an already accepted missing theorem in its selected parent.
