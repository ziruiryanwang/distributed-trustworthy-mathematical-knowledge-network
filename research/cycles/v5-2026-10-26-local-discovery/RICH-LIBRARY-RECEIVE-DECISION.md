# Rich-library grounding, authoring and onward circulation

2026-10-26. `inert_rehost_relation`; source/data-only decision for root.
Canonical guard passed. No product import, native execution, owner-state opening,
retry, Git mutation or modification of used evidence. This note supplies the
detailed API/cap analysis used by `CORE-NEXT-DECISION.md`, not a runtime selection.

## Decision in one paragraph

**The current interfaces already describe a coherent strict route from a complete
2,651-unit inert Std bundle to an independently grounded local parent, then to
small new contributions authored with an approved ordinary Std project.** The
32-group convenience reconstruction limit does not block that project-authoring
route. The saved diagnostic is not yet a consumable complete bundle, and native
intake cost/compatibility/snapshot fit remain unobserved. Three intake batches
require an upfront allocation strictly greater than 180 CPU seconds plus controller
cost; the 60-second batch reservations are not refunded. Onward circulation is
not globally limited to 1,024 ancestors: peer receiving is relative to a grounded
parent, while retained full bundles already support bulk transfer. A different
limitation belongs specifically to the current basis-closed selected-export helper.
Do not commission a new checker, larger reconstruction cap or transfer protocol
before using these existing compositions.

## What the retained evidence establishes

The adopted successor binder completed the exact retained native writer targeting
`Std.HashMap.isEmpty_insert`. The original public `std-export01` remains failed.
The saved-output audit is
`software/v5/ordinary_binding_reuse/SAVED-WRITER-OUTCOME.md`.

| Property | Saved observation |
|---|---:|
| Distinct whole declaration units | 2,651 |
| Portable evidence bytes | 44,912,843 |
| Manifest bytes | 468,097 |
| Batch unit counts | 1,024 / 1,024 / 603 |
| Batch evidence bytes | 9,997,243 / 17,147,916 / 17,767,684 |
| Aggregate nodes / names / import rows | 1,143,590 / 2,821 / 43,120 |
| Binding bytes / native-array bytes | 698,055 / 38,097,072 |
| Timed binder CPU | 28.125 seconds |

The diagnostic retained only its manifest and summary, not the complete unit
files. The 708 files left by the original failed producer total 6,389,257 bytes;
their exact hashes/lengths agree with the successor manifest. This agreement does
not supply the other 1,943 files or recover a production success. A receiver cannot
intake the present manifest-only diagnostic directory as a complete library.

The manifest/summary are under
`experiments/v5-local-checks/binding-saved-writer01/binding/`, with SHA-256:

- Manifest: `1de776b3d131c8c1be3414ed0e0cf066ebd05caebbcd1cf1b6ca80853962e59c`.
- Summary: `7ee48a0939a103a68b142bca37292beb3f2f3114a676ef4af7b454424d5a1d3d`.

The aggregate census is a saved binder observation, not a new independent decoding
of all proof data. Per-batch deeper censuses were not saved; the adopted partitioner
enforces their limits. No real recipient, protected Std root, warm Std contribution
or matched speedup follows from these records.

## Exact independent grounding path

The current flat source map is
`software/v5/ordinary_current_release/release.json`, SHA-256
`821796aa5b4996edd3f34babdb3be186d8321e0b3b4208b1e3f18705400caf78`.
Its relevant selections are the native-package `owner.py`, baseline
`baseline_intake.py`, binding-reuse `baseline_bundle.py`, ordinary-project-return
`ordinary_contribution.py`, and ordinary-Lean checker/catalog modules. Do not infer
the selected version from another similarly named historical directory.

The existing public composition is:

1. A fresh recipient initializes its own owner. Actual checking of the fixed
   456-unit/581-name basis establishes its first protected root. A sender's root
   or report cannot substitute for this recipient-local event.
2. The caller copies a complete inert bundle, selects its exact manifest hash,
   and explicitly selects an eligible parent in this recipient's catalog.
3. `owner intake-baseline` accepts `--bundle-directory`, `--bundle-manifest`,
   `--bundle-manifest-sha256` and `--parent-root`, plus owner and resource settings.
   It has no `--output`. The existing direct recipe is
   `software/v5/ordinary_selected_export/INTAKE.md`; do not create a second script
   that mistakes a producer/export report for a mathematical warrant.
4. `_plan_all` validates all manifest batches and exact evidence identities,
   dependency order, whole-unit outputs, bindings and storage/call capacity before
   checking begins. Its projected bindings are planning hypotheses only.
5. For each batch, intake rereads the exact files and performs real `preflight`
   and `admit` against the last confirmed root. Admission independently preflights,
   stages/readbacks custody, runs the selected native checker, validates the live
   event/report/artifact and commits its protected result. It does not accept a
   serialized planning result or another party's success receipt.
6. `BASELINE_INTAKE_COMPLETE` exposes `result.local_root` and actual per-batch
   `CHECKED`/`REUSED` observations. Registration as an original ordinary library is
   separate: `ordinary_library_registered` is explicitly false.

The soundness shape is induction. Let `W(R)` mean that root `R` is warranted under
the selected checker/foundation and protected-local-state premises. Initialization
establishes `W(R0)`. A successful actual admission of a batch above `Ri` establishes
`W(Ri+1)` by checking every new declaration against the already warranted context;
exact reuse leaves the warrant unchanged. Thus a complete sequence establishes
`W(Rfinal)`. Projected roots, producer success and evidence hashes establish none
of these implications by themselves. Kernel correctness, accepted axioms, exact
support/runtime selection and protected local artifacts remain trust assumptions.

An interrupted intake may preserve a checked prefix and may report
`possible_unreported_commit`. Preserve those facts and use explicit protected
status/context selection before later work. Failure is neither whole-bundle
acceptance nor a guarantee of rollback; there is no automatic retry.

## Capacity and cost: facts versus unknowns

The bundle format permits 8,192 total units, 64 batches, 64 MiB total evidence,
2 MiB manifests, 20,000,000 nodes, 262,144 names and import rows, and 16 MiB binding
bytes. Per-batch limits include 1,024 units, 64 MiB evidence/native arrays,
2,097,152 nodes and 65,536 names. The observed closure fits these structural
bounds; a planning fit is not an observed kernel fit.

The public owner currently supplies default `CallLimits()` to intake. That means
**60 CPU seconds per batch and 64 MiB native output per batch**, not individually
CLI-configurable values. Raising the whole invocation allowance does not raise
either batch cap.

The exact source accounting is important:

- `baseline_intake.py:71-75`: `capacity(batches, calls)` requires
  `controller_elapsed + reserved_cpu + batches * calls.cpu_seconds < cpu_seconds`.
- `:245`: `_plan_all` calls this with the full manifest batch count before the
  first actual admission.
- `:78-87`: each operation reserves another whole batch cap.
- `:308-312`: observed worker CPU is explicitly diagnostic and **not a refund**.
- `ordinary_native_package/owner.py:524-540`: the outer owner first subtracts its
  already consumed controller work/headroom before constructing the intake budget.

Consequently neither 120 nor exactly 180 outer CPU seconds can authorize the
three-batch case. Cheap actual batches do not change the upfront requirement.
The reservation is authorization accounting, not a measurement of expected CPU.
Within each batch, controller work also consumes that operation's allowance;
the native process does not automatically receive all 60 seconds.

Three entirely new batches reserve 192 MiB of snapshot capacity and 390 MiB of
call spool capacity under the current formula. Those are conservative allocation
figures, not measured outputs. Catalog defaults allow 4,096 roots, 8,192 operations,
1,048,576 names, 16 MiB metadata manifests and 4 GiB total artifacts; custody quotas
must independently accommodate all evidence/locators. Exact per-batch CPU, generated
snapshot size, possible kernel refusal, whole-operation memory and elapsed fit are
still unknown. The saved binder's approximately 592 MiB peak commitment and timing
do not predict native intake's peak or timing.

## Ordinary warm authoring without the 32-group bottleneck

The no-project convenience route does reconstruct selected definition semantics.
For this target its saved semantic frontier has 265 units/361 rows, 86,914 nodes,
2,571 selected edges and 3,638,469 native bytes. It genuinely exceeds 32 groups;
the difference cannot be dismissed by observing that theorem proofs are opaque.
See `STD-WORKFLOW-DECISION.md` and saved `std-frontier01.json`, SHA-256
`94e34c98496bd0a4d4c45a2a13cdb2ecf77861a04813248ca16aa98659a20e42`.

The existing approved-project route is different:

1. Use `owner contribute` with an explicit hashed `--project-authoring` document,
   selecting locally approved compiled project paths/imports. This approval permits
   executing the local project/frontend and any approved plugins; it is not a
   sandbox or mathematical trust waiver.
2. Select `acquired_targets=[]`. `request_targets` then prepares only the genuine
   warranted basis `Eq`; it does not reconstruct the 265-unit Std frontier.
3. Author with the approved ordinary Std imports, retaining ordinary notation,
   classes and frontend support. `SuccessorExport.selectedDeferred` stops at safe
   imported constants. Names not prepared as exact portable symbols are emitted
   as **unclaimed/unresolved**, not assigned invented portable identities.
4. `portable_candidate.bind_candidate` resolves those names through the actual
   protected parent bindings. Explicitly claimed IDs still must agree. Missing
   names produce `NEEDS_LOCAL_INTERPRETATIONS`; new names cannot overwrite the
   parent. Every complete new inert unit then undergoes independent admission.

This is a **new recipient-local interpretation and check**, not proof that every
same-named declaration in the approved project has the parent's exact identity.
Changed meaning may make conversion or checking fail. An existing name match is
never permission to silently replace an explicit artifact identity. Moreover,
grounding this selected closure warrants only its exported names, not all Std:
the exporter's 39,939 loaded source records are not 39,939 accepted declarations.

The contribution remains bounded: 1 MiB source, at most 32 selected outputs and
32 new whole units, 4 MiB candidate/evidence, 4,096 bindings and 131,072 nodes.
Thus the route avoids an *imported-frontier convenience limit*; it does not provide
unlimited individual theory submissions. Compatible theories can grow through
small modules. A genuinely indivisible oversized group needs its own justified
route, not a claim that arbitrary Lean projects already fit.

Warm checking does not replay all ancestral theorem proofs, but it is not constant
time. `PortableCatalog.context` validates/collects the selected protected chain;
`LocalSnapshot.restoreLocal` imports the selected exact local artifacts and checks
their chain/module/header constraints. Fresh owner processes rehash selected local
artifacts; metadata bindings and needed transparent semantics still cost resources.
Unrelated worldwide knowledge is not loaded, but selected context size matters.
Successful three-batch grounding above basis would create four snapshot modules,
not one globally synchronized mathematical state.

## Onward circulation: distinguish three routes

| Route | What the existing implementation permits | Actual boundary |
|---|---|---|
| Retain/copy a complete baseline bundle | Any approved recipient can independently run its bounded multi-batch intake | Bundle must remain available; exact copies confer no warrant |
| Peer receive above an explicit protected parent | Acquire/check at most 1,024 currently missing units per invocation; previously grounded names terminate dependency acquisition | Not an automatic bulk scheduler; per-call byte/frontier/checking and cumulative local-state costs remain |
| Current selected-export companion | Copy a selected target's entire basis-closed custody closure to an inert bundle | Hard 1,024-total-unit closure cap; it does not accept a richer trusted stop frontier |

The third row must not be generalized into a global 1,024-unit network limit.
Current `ordinary_multi_source/peer_api.py:714-785` passes the actual parent into
preflight throughout receiving. Successive intermediate targets can therefore
ground more than 1,024 units cumulatively. In the limiting construction, a finite
acyclic whole-unit DAG can be processed topologically, one unit at a time, with
`selected-unit-only`, provided each unit fits, its advertised selection/preview is
available and all local/state/service budgets suffice. That is a composability
argument, not an economical user workflow or an implemented automatic planner.
Thousands of owner calls/snapshot roots may be a poor strategy even when each
individual call fits. Three baseline batches do not imply three target-based
peer calls can achieve the same partition.

Conversely, splitting target lists does not generally repair the selected-export
helper: it recursively closes every selected target to the fixed basis, so the
2,651-unit final target alone still fails its total cap. This is a helper/workflow
limitation, not an unsoundness or lack of data in custody.

Custody stores exact evidence and locators for every stored unit. Existing
`OrdinaryStore.get_evidence` and `/v5/ordinary/evidence` serve one exact UnitID at a
time, independent of receive's closure cap. A retained manifest gives all exact
unit IDs, raw hashes/lengths and relative paths. Therefore reconstructing a missing
bundle from available custody is, in principle, bounded exact-data acquisition
plus the existing manifest validation/intake. It needs no new mathematical trust
rule or wire format. The current shipped selected-export CLI does not expose that
manifest-to-files composition directly; do not describe a new adapter as already
implemented. No `export-batch` command was found in the currently selected owner
or peer facades. Existing raw APIs can underpin a small adapter only if an actual
workflow needs it. For the immediate case, retaining/copying the full materialized
bundle is simpler than creating such an adapter.

## Relation to concepts, theories and the next investment

The route supports agents introducing definitions/structures, deriving new laws,
making countermodels and checking bridges to other developments, then returning
their bounded exact artifacts. Mathematical acceptance is independent of human
intention. Nothing here invents those concepts automatically, guarantees novelty,
finds useful cross-vocabulary bridges or proves that sharing accelerates discovery.
The already adopted concept-continuation analysis owns those distinctions; a new
tiny concept episode would not test the missing rich-base premise.

Root can reasonably select one affordable real-library grounding discriminator,
as recommended by `CORE-NEXT-DECISION.md`, if this closure is a representative
supported user workflow. Its smallest route is materializing fresh complete files
from the retained exact writer with the adopted binder, comparing the retained
manifest/708 partial pins, and selecting the unchanged direct three-batch intake
above an eligible small parent. No repeated native export is needed. Preserve the
old failure and charge all new work. This note does not itself select that run.

Before launch, record sufficient upfront reservation, exact retained inputs and
output bounds. Do not run a known deterministic cap failure or raise caps after
failure merely to finish. Success supplies one actual warranted specialty-base
premise for later unfamiliar work; it is not a full Std compatibility claim,
warm-authoring pass, benefit measurement or final-v5 acceptance. Failure should
select the smallest consequential correction or an explicit operating restriction.
Onward bulk copying, no-project reconstruction, automatic concept discovery and
global search are separate questions, not mandatory new mechanisms for this gate.

Source loci: `ordinary_baseline/baseline_intake.py:28-94,141-334`;
`ordinary_native_package/owner.py:42-83,524-540`;
`ordinary_project_return/ordinary_contribution.py:197-207,438-557`;
`ordinary_lean/SuccessorExport.lean:155-222`, `portable_candidate.py:172-239`,
`portable_catalog.py:492-546`, `LocalSnapshot.lean:170-241`;
`ordinary_selected_export/selected_export.py:18-20,178-311`;
`ordinary_multi_source/peer_api.py:655-809` and
`ordinary_multi_source/ordinary_acquisition.py:226-311`.
