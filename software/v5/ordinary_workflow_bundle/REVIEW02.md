# Independent selection-only workflow successor review

2026-10-26. **GO for root to select the single proposed
`workflow-source-controls02` execution.** No utility, test, helper, guide or
runner change is needed. This is prospective source/selection review, not a
successful packing/relocation result or authority to retry automatically.

The original REVIEW, selection, code and failed attempt remain unchanged.
Reviewer owns only this new file for the follow-up; no runtime, product import,
test, archive creation, Git or shared-ledger mutation occurred in this review.

## Preflight failure and correction of the previous verdict

Root's retained [PREFLIGHT01-FAILURE.md](PREFLIGHT01-FAILURE.md) records the actual
`V5_SOURCE_SCOPE` exception, before output creation or supervision. Read-only
inspection confirms that the controls01 output directory does not exist.
The unchanged runner permits snapshot source paths only inside `software/v5`
or its own `tools/Run-V5-Check.py` path. The old selection incorrectly included:

- `software/assets/foundation/seed-inventory-json.json`
- `software/assets/foundation/seed-verified.json`

The earlier independent review verified the file hashes and complete mapping
but missed this runner-scope precondition. Its launchability GO was therefore
incorrect; it is not rescued or relabelled as a passing test. The actual scope
failure establishes no test/pack/native result. The runner had already loaded
its approved supervisor support before refusing, so this is not a claim that
the Python invocation executed no code or consumed zero CPU.

Reviewer reread the complete unchanged runner, including source scope, external
pin checks, snapshots, argv substitution/requirements, supervision and final
binding checks. The correction below uses those existing supported interfaces
instead of broadening the runner or producing another test implementation.

## Exact reviewed successor and complete delta

Selection: `experiments/workflow-source-controls02-selection.json`

SHA-256:
`b9d37275d2f7c89edaa2163cdba44d01d44c8c6446efea662dd1a0b8bef7aeaf`

Compared directly with preserved controls01 selection
`b113376f8e209b5585df5e369dde42c949b73f9acba9641449bb42e4492eb6c4`:

| Field | Exact change |
|---|---|
| Run name | `workflow-source-controls01` to fresh `workflow-source-controls02` |
| Source snapshots | Remove only the two foundation entries above: 156 to 154 |
| External pins | Keep the base ZIP and three Python pins; add all 153 actual canonical pack inputs: 4 to 157 |
| `--source` | Snapshot utility path to canonical `software/v5/ordinary_workflow_bundle/bundle.py` |
| `--source-root` | Snapshot root to canonical project root |
| Test entry, utility hash, other argv and limits | Unchanged |

Independent read-only checks matched **all 154 snapshot-source hashes** and
**all 157 external hashes**. There are no other source-map additions/deletions,
changed retained source hashes, changed original external hashes, unexpected
external keys or changed resource limits. The new external set is exactly the
original 153 pack inputs plus approved base ZIP and three Python files. Each
canonical input's external hash agrees with its original selected source hash.
The two foundation byte selections have not changed; the approved original ZIP
also retains their exact source payloads.

All 154 remaining snapshot paths satisfy the unchanged runner's source scope.
The test remains a pinned snapshot entry, satisfying the runner's requirement
that argv reference its snapshot; the selected Python executable remains an
external pin. The canonical utility/root arguments satisfy the existing test's
`source == source_root/UTILITY` relation. Its `helper()` now resolves the same
approved helper in the canonical tree, whose bytes are both externally pinned
and checked by bootstrap before execution. No new path resolver or code hook is
introduced.

Current output `experiments/v5-local-checks/workflow-source-controls02` was absent
at review. Exact enclosing limits remain 120 wall seconds, 60 inclusive Job CPU
seconds, 384 MiB, four active processes, **2 MiB stdout and 1 MiB stderr**. The
test's original 110-wall/45-controller-CPU horizon, at most one public pack and
one public relocated verify, preserved negative fixtures and no retry are
unchanged. There is no new native, service, network or mathematical allocation.

## Precise evidence boundary: canonical inputs, not a complete mirror

The successor does **not** establish that packing read only a mirrored snapshot.
It intentionally uses selected canonical source inputs. The original TEST-PLAN's
mirror description remains preserved as the initial proposal; this explicit
selection follow-up states the executed candidate's different input route.

Three safeguards already cover that route under existing protected-input premises:

1. Before creating output or launching the test, the runner verifies every one
   of the 153 canonical pack-input hashes, base ZIP and Python pins.
2. The unchanged packer reads only its explicit base-plus-companion source map,
   enforces the original base projection and fixed companion pins, then rechecks
   all selected source bytes after writing/reading the archive. The new utility
   also checks that its running bytes equal the selected copy.
3. After the supervised test returns, the runner verifies the same complete
   external map again, plus its selection/snapshot bindings. A failed final
   binding check yields `FINAL_BINDING_FAILED`, not a passing outcome.

These are endpoint/input identity checks, **not protection against an adversarial
same-account writer changing and restoring files between observations**. Hold all
selected canonical inputs immutable for the operation, as already required by
the utility and project rules. Keep outputs disjoint from those sources; the
selected suite directory and packer's explicit overlap checks do so. No source
document, code pin or mathematical trust claim is relaxed by this correction.

The actual relocated verification remains self-contained: its helper and all
manifest payloads come from the new extraction, and its external union-manifest
hash is selected from the checked pack receipt. The test's independent original
143-byte comparison, ten mapped additions, operational-link checks, bootstrap
refusals and full extraction census remain exactly the same.

## Why selection-only is the smallest sufficient change

Changing the frozen runner to admit a wider filesystem scope would introduce a
new execution boundary solely for this packaging test. Changing the test to
copy missing foundation files would add another copy/association path without
testing a needed user capability. Neither is required: the existing runner
already supports complete external pinning, the test already accepts explicit
canonical source arguments, and the packer already supports a protected
development checkout. Retained eligible snapshots and the approved base ZIP
preserve evidence without requiring a second complete copy mechanism.

This correction is sufficient for the selected file-only gate, not a generalized
repack feature or a weakening of portable end-user build/use. Root must explicitly
select controls02 once; audit the resulting archive, exact mapping/relocation,
negative results, final binding checks, costs and closure before adoption.
The controls01 failure and its unknown final CPU remain retained and charged.
