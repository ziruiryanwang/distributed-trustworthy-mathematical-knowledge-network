# Cold start without a peer or an existing Lean project

2026-10-26. Source-only decision by `cold_start_workflow`. Canonical workspace
guard passed. No product import, native process, test, experiment, owner/database
open, network operation, package mutation or Git mutation was performed. Shell
inspection and exact file hashing were read-only; this checkpoint is the sole
new file. All predecessor source and evidence remain unchanged.

## Decision

**The supported public software already has this edge. There is one small
first-user documentation gap in the self-contained workflow archive.** An
investigator who has approved runtimes and a built ordinary package needs
neither a received theorem nor an existing Lean/Lake project to start. Fresh
`owner init` supplies an admitted basis. `owner contribute` accepts an empty
acquired-target list and a locally authored Lean body, independently checks its
new declarations, and retains exact portable outputs. The existing selected
export, independent offline intake and direct publication routes compose with
that result.

Do not implement a generator, new acceptance mode, fixture-based initialization,
project creator, network bootstrap, helper action or additional proof campaign.
Add only a cold-start branch to the new top-level start guide, then stop this
workstream. This is a supported capability within the existing Init/helper and
size limits, not a guarantee that any desired library-dependent theory fits,
that an agent chooses valuable mathematics, or that discovery accelerates.

## Exact authority and source mapping

Current runtime authority is
`software/v5/ordinary_release_bundle/ADOPTION.md`, whose actual assembled package
is `experiments/v5-local-checks/transport-release-handoff01/suite/assembled/package`.
Its PROFILE is
`b047d4492da79e363fcd154144a6d9088a93100fde7aac3c385f3a296a41dad7`.
This identity identifies the inspected default; new approved builds must use
their own actual PROFILE, not copy this historical value.

`software/v5/ordinary_bounded_operations/source-map.json:425` maps
`authoring/py/ordinary_contribution.py` to
`software/v5/ordinary_project_return/ordinary_contribution.py`; line 455 maps
`owner.py` to `software/v5/ordinary_native_package/owner.py`.
Read-only SHA-256 inspection found both source files byte-identical to their
actual default-package copies and to the PROFILE entries:

| Installed role | Bytes | SHA-256 |
|---|---:|---|
| `owner.py` | 36818 | `56ef042f652fcb88cae7d16ab74883016a469e2e82777c1a173f842f5ef8245a` |
| `authoring/py/ordinary_contribution.py` | 31251 | `09394f523417406aefcad0b47d06fa2d7782940bec3bb5094975f08b68f94ca8` |

Thus the decision does not infer current behavior from the old ordinary-package
facade or the optional reference-package facade.

## Supported operator path

| Step | Actual source/API contract | Required selection |
|---|---|---|
| Initialize | `ordinary_native_package/owner.py:513` calls `owner.initialize`; line 520 returns `INITIALIZED_LOCAL_OWNER` and `basis` | Approved final package/runtimes, fresh catalog and custody, original limits and chosen local store ID |
| Select initial parent | Successful init report `result.basis.local_root`, with `result.basis.status = CHECKED` | Actual owner command report from diagnostics `child/stdout.txt`, plus successful launcher and clean supervision; no guessed root |
| Author without a project | `owner.py:53` documents `--acquired-targets ... or []`; contribution reads source/targets/names at lines 491 onward; optional project selection is not required | UTF-8 Lean body, JSON file containing `[]`, 1..32 fresh structured output names, explicit basis parent and fresh output |
| Resolve basis | `ordinary_project_return/ordinary_contribution.py:162` allows zero acquired targets; `request_targets` at line 197 selects genuine fixed-basis `Eq` and checks its exact protected binding | No fabricated acquired target or downloaded theorem |
| Construct source | `assemble_source` at line 210 supplies `Init`, reconstruction helpers, a public section and export command | Source body only, without replacing the generated preamble; no pre-existing compiled project |
| Independently admit | `contribute_source` binds candidate outputs, preflights at lines 520 onward, calls `owner.admit` at line 539 and requires `CHECKED` for all output units | Compiler output alone never supplies acceptance |
| Retain outputs | Lines 544–575 retain custody previews/evidence and return `CHECKED_CONTRIBUTION_WITH_DURABLE_PUBLICATION_BYTES`, `admission`, `local_root`, exact `targets` | Complete successful owner report and closure, not just the inner `RESULT.json` |
| Extend again | `ordinary_reuse_workflow/README.md` section 2 and final paragraph | Select the previous `result.admission.local_root`; select exact previous `result.targets` as acquired inputs when their declarations are needed |
| Export offline | `ordinary_selected_export/README.md`, “Prepare one explicit request” and “Inspect, move and independently check” | Actual exact target rows and original custody limits; full selected dependency closure; no producer project or producer report |
| Accept at a second owner | `ordinary_selected_export/INTAKE.md`, “Select the receiver and inputs” and “Run one explicitly bounded intake” | Receiver's own fresh init/root or deliberate accepted root; copied manifest and units; exact manifest SHA-256; direct `owner intake-baseline` |
| Publish locally | `ordinary_reuse_workflow/README.md` section 3; receiver-specific adaptation in the final INTAKE section | Actual checked context root and selected target rows, direct `peer publish`; no report relabeling |

Source authoring and independent mathematical admission are separate stages in
the first owner's contribution. Acceptance by another owner requires that
owner's own intake. Neither export nor publication transfers the first owner's
warrant. No live peer is needed for authoring, local indexing or offline export/
intake; remote discovery still requires someone to serve the work later.

The operator can define a concept and derive several consequences in one body,
or continue in later explicit contributions. Choose both useful definitions
and laws as outputs. If a later proof needs to unfold a public definition,
`@[expose]` may be necessary. The generated public section does not by itself
expose its reducible body. The existing Init/helper environment, 1 MiB body,
32 outputs/groups and other request/candidate/admission limits remain; there
is no claim of arbitrary project/frontend recovery. These limitations already
have a separately approved ordinary-project route for appropriate workloads.

## Why the archive's current guides do not finish this first step

The older `software/v5/ordinary_package/README.md` already gives the decisive
instructions in “Use one persistent owner”: lines 70–79 specify the initial
`result.basis.local_root` and `[]` for basis-only work; lines 90–95 explain
`@[expose]`. **For a repository reader with that guide, no new mechanism or
duplicate full recipe is needed.**

However, the actual retained 143-payload
`experiments/v5-local-checks/transport-release-handoff01/suite/relocated-source/SOURCE-MANIFEST.json`
does not include `ordinary_package/README.md` or `ordinary_lean/README.md`.
The new `ordinary_workflow_bundle/bundle.py` companion map does not add either.
The new archive is explicitly supposed to work without the repository.

Its current `ordinary_workflow_bundle/README.md` section 3 provides “Extend
received mathematics” but no fresh-basis authoring route. The included
`ordinary_reuse_workflow/README.md` introduction requires a successful receive,
and section 1 only derives its parent and targets from that receive. The included
`ordinary_operator_kit/START-HERE.md`, “Develop a new concept or theory, then
return it,” starts from an independently obtained approved **compiled** project.
The bounded-operations overview names contribute but does not provide the
empty-target initial-root recipe. A first user can discover the edge by reading
CLI/help/source, but the current top-level navigation does not supply it.

The included operator-kit guide already supplies fresh init preparation,
launching and the exact init report fields. The included reuse guide already
supplies source/output-name preparation, direct contribute, success inspection,
publication and continuation. The exact gap is their missing connection.

## Minimal proposed documentation change

In the new workflow start guide's section 3, add a “Start a local investigation
without a peer or existing project” row and a short adjacent subsection. If its
bytes have already been used/frozen when root acts, make a separately selected
documentation/distribution successor; do not edit a used archive or manifest.
Keep the unchanged reuse guide and original 143 base inputs intact. No new
payload or runtime role is needed; only the existing start-guide hash and the
normal regenerated archive/manifest change in a later selected handoff.

The subsection should concretely say:

1. Perform only the existing fresh-init step, using the final selector/profile
   overrides. There is no obligation to continue into find/receive. Read actual
   init diagnostics `RUN.json`, `SUPERVISION.json` and `child/stdout.txt`; require
   launcher success and clean closure, `ok = true`, `operation = init`, matching
   final profile/catalog/custody/store, no close/budget errors,
   `result.status = INITIALIZED_LOCAL_OWNER`, and `result.basis.status = CHECKED`.
2. Set the reuse recipe's runtime/package/state/limits/work variables to that
   owner, but replace its receive-only section 1 with the initial-root inputs
   below. Use the returned 64-lowercase-hex basis root, never a historical root.
3. Continue directly at reuse section 2, “Author and check an extension,” then
   section 3 for deliberate publication. Include the brief `@[expose]` warning
   above, since the omitted older guide contains a real observed first-use trap.
4. Link to selected export and INTAKE for another independent owner, and state
   that offline export/intake needs no service. A second contribution can use
   the actual first contribution's admitted root and selected output targets.

Suggested concise guide prose, with archive-relative links:

> You can begin with your own definitions and consequences before a peer or an
> ordinary Lean/Lake project exists. Complete only the
> [fresh initialization step](software/v5/ordinary_operator_kit/START-HERE.md#first-independent-use-init-find-preview-receive)
> with this guide's final selector/profile. Inspect the successful init's
> `RUN.json`, clean `SUPERVISION.json` and complete `child/stdout.txt`; do not use
> a receive report or an old example root. In
> [reuse section 1](software/v5/ordinary_reuse_workflow/README.md#1-select-the-actual-receive-and-its-owner),
> set only the variables from `$reusePython` through `$reuseWork` to that same
> initialized owner, original limits, approved package/profile and runtimes.
> Skip `$reuseReceive` and the receive-specific checks. Use the checked init
> report and empty target file below, then continue at
> [reuse section 2](software/v5/ordinary_reuse_workflow/README.md#2-author-and-check-an-extension)
> and section 3. Your source is a Lean body in the existing Init/helper
> environment; select your own completed definition/theorem output names. A
> definition whose body a public theorem must unfold may need `@[expose]`;
> public visibility alone does not expose that body. For further contributions,
> select the actual admitted root and exact earlier target rows. Use selected
> export and independent offline intake to move work to another owner; no
> service is required for that route.

The small input substitution, after the stated report/closure checks and those
variable assignments, is:

```powershell
$coldInit = Get-Content -Raw -LiteralPath 'C:\commons-work\diagnostics-init-01\child\stdout.txt' | ConvertFrom-Json
if ($coldInit.ok -ne $true -or $coldInit.operation -ne 'init' -or
    $coldInit.profile_sha256 -cne $reuseProfile -or
    $coldInit.catalog -cne $reuseCatalog -or $coldInit.custody -cne $reuseCustody -or
    $coldInit.store_id -cne $reuseStore -or $coldInit.close_errors -or $coldInit.final_budget_error -or
    $coldInit.result.status -ne 'INITIALIZED_LOCAL_OWNER' -or
    $coldInit.result.basis.status -ne 'CHECKED' -or
    $coldInit.result.basis.local_root -cnotmatch '^[0-9a-f]{64}$') { throw 'Select a successful init for this owner.' }
$reuseParent = $coldInit.result.basis.local_root
if (Test-Path -LiteralPath "$reuseWork\acquired-targets.json") { throw 'Choose a fresh input filename.' }
[IO.File]::WriteAllText("$reuseWork\acquired-targets.json", '[]', [Text.UTF8Encoding]::new($false))
```

This is a proposed documentation fragment, not executed work or a replacement
for launcher/supervision inspection. It supplies neither a theorem nor an
acceptance fixture. The investigator supplies their own meaningful definitions
and consequences using the already documented source/name format.

## Reuse evidence and stop condition

The independently audited
`research/cycles/v5-2026-10-22-native-library/ORDINARY-PACKAGE-OUTCOME.md`
already records the clean 21-module two-lane build, relocated genuine basis
initialization, preserved caller visibility failure, and corrected basis-parent
contribution followed by persistent reopen. “Continuation01: corrected caller
and persistent reopen” verifies two admitted exports (`applyTwice` and its law),
actual candidate/native/evidence/custody/context correspondence and clean closure.
Its contribution explicitly uses the original basis root. This is engineering
capability evidence, not conceptual novelty or a growth comparison.

The current reuse recipe's `REVIEW.md` checks the direct launcher/contribute/
publication interfaces and their report boundaries. The current release ADOPTION
retains the adopted build/transport/file-only handoff evidence; this decision
does not transfer a historical run's profile or claim a new run. Existing selected
export/intake and native/build evidence remain reusable within their stated scope.

**Smallest decision-changing evidence is already sufficient for this decision:**
the exact current source-map/installed-file identity comparison, the explicit
empty-target basis code path, and the existing native lifecycle audit. For a
later documentation edit, independently read the short added branch against
those exact fields and verify its links exist in the existing archive map.
Reuse the planned consolidation's normal source/manifest/relocation checks if
it is still pending. Do not repeat initialization, native compilation, concept
episodes, reciprocal transfer or broad regression tests for this prose bridge.

Stop once the documentation connection is accurate and reviewable. This finding
does not authorize a mathematical campaign, external publication, a growth study,
source execution, additional automation or changes to the separately owned paper
and growth work. Full deployable v5 remains open.
