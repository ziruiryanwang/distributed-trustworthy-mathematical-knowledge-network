# Release producer command entry: source checkpoint

Root, 2026-10-22. Source only; independent review and changed-boundary controls
remain required. No import, constructor, snapshot or proof ran in authoring.

`software/v5/release_production/operator.py` is derived through an explicit new
file from the reviewed/frozen typed lifecycle entry a23c24c3. The new initial
source hash is3d783fe81ccb9f30431f1128ce852323461bcd483f4984dfaf631ecc580441bf.
Independent source review found that the whole adopted release directory,
not only its sdk/base subtrees and selected files, must be protected from
new outputs. This was corrected before execution: current entry hash is
d1c5507f00f33df0eb0732e09113e389387e122c6786c460a42e7553695e2287.
All old code and evidence remain unchanged. An initial in-memory text derivation
refused an expected line-ending match before writing; the normalized text was
then applied as the new file. No product execution or failed experiment occurred.

## Contract

The common options remain `--source-root`, `--entry-sha256`, pinned `--profile`,
pinned `--input`, and fresh `--owner-report`. `--outer-selection` is mandatory
only for snapshot. Each invocation selects exactly one action:

| Action | Input | Only dispatched public operation |
|---|---|---|
| snapshot | Existing generic snapshot configuration | prepare then snapshot, no proof |
| request | New DMKN_RELEASE_LIFECYCLE_REQUEST_ENTRY_V1 options and five-role completed snapshot evidence | production_request once; its inherited preflight is not repeated |
| preflight | Ordinary existing aggregate stage request | preflight once, output must remain absent |
| run | Same exact stage-request grammar | run once under the explicitly selected allowance/stage limit |

Only run can dispatch proof stages. It does not run preflight separately first,
choose budgets or retry; the existing scheduler validates the request internally.
A successful prefix is not a finished certificate. A finished artifact is not
receiver mathematical acceptance. The report is never funding authority; an
external owner must explicitly select and bound every run.

## Changed boundary

Bootstrap requires the new five-field release profile and27-module closure.
It loads no typed historical-adoption package. In addition to exact pre-import
source pins and post-import origins, the invoked entry bytes must equal the
stable installed release_production/operator.py runtime row, allowing the
research wrapper's exact copied entry without selecting different installed code.

The unchanged small-file/selection/finalization mechanisms retain the acyclic
snapshot selection,256 runtime-row cap, strict ordinary paths, exact input
digests, fresh nonoverlapping outputs and overriding finalization sentinel.
The full adopted release root is also an ordinary directory and protected
output boundary; an unoccupied subdirectory is not a permitted output location.
The new owner is ReleaseLifecycleProducer; schema/domain/source implementation
is assigned separately. Both request and preflight must leave future proof
output absent through late finalization. Run observes a saved result exactly
equal to the returned canonical report, known closure, valid final binding and
one allowed success status before reporting PASS_ONE_FINITE_ATTEMPT. All
reported generated pins are rebound. A raised run retains unknown host/proof
dispatch extent rather than claiming zero work.

This command still uses generic local-check snapshot evidence. It is not the
installed public-launch evidence adapter or a self-contained release installer.
The independent design review must preserve that remaining deployment boundary;
do not manufacture a local-check PASS from a different public-launch schema.

## Targeted review

Review bootstrap's new class/schema/source/self-copy bindings, the four-way input
dispatch, preflight's no-output condition, and run result/status/closure/sentinel
handling. Reuse the prior entry controls for unchanged helpers as source evidence;
do not repeat their five full groups without a changed premise. Real proof
dispatch is prohibited during new command-flow controls; use explicit doubles
only for these action-dispatch tests. Core constructor/relocation tests have
their separate real-owner contract.
