# Public inert operations need a shipped whole-operation resource envelope

2026-10-24. Source-only adversarial review by current_security_obstruction.
No runtime, exploit, network call, owner-state access, product edit or Git mutation.
This is one concrete next-decision recommendation, not a security qualification.

## Highest-impact actionable gap

**Ship a supported outer resource-containment entrypoint for ordinary public
operations before describing their CLI allowances as a whole-operation boundary.**
The selected code already requires such an envelope, but the package's normal
documented invocation does not supply it. Existing research tests supplied it
from a canonical-workspace-specific runner. This is a deployment gap in the
implemented safety assumptions, not a claim that a demonstrated exploit exists.

This matters for remote inert input even when no producer code is approved.
The Python controller parses, rederives features, copies data and coordinates
stores in the same process as its cooperative deadline checks. Native child Job
limits do not constrain that controller. An expensive or memory-heavy controller
operation need not yield control before exceeding the operator's selected cap.
Wire byte/node limits remain useful, but are not that process-memory/CPU bound.

## Exact current-source evidence

- ordinary_research_distribution/source-map.json:437-445 ships the supervisor
  primitives and selects ordinary_native_package/owner.py plus the current
  ordinary_authoring_offers peer facade/API. It supplies no ordinary outer CLI.
- ordinary_native_package/owner.py:128-167 explicitly states controller checks
  are cooperative and memory-mib is not a controller RSS cap. Allowance.check
  only checks elapsed time/charged CPU at calls; memory_mib is forwarded to native
  OperationBudget. No parent Job is created by that class.
- ordinary_lean/ordinary_admission.py:321-329 makes the same external-supervision
  premise. Its actual native worker supervision at620 is inside the controller.
- ordinary_authoring_offers/peer_api.py:1-7,27 defines controller containment as
  COOPERATIVE_REQUIRES_EXTERNAL_JOB. inspect:733-738 reparses and deep-copies the
  returned inert evidence synchronously before the next live check. Similar
  ordinary_acquisition.py:150-156,478 reads execute in the calling controller.
  asyncio timeout scopes cannot preempt synchronous Python/native parser work.
- ordinary_research_distribution/README.md:40-42 tells users to run owner.py,
  peer.py and query.py directly using Python -I -S -B. It does not give a concrete
  portable outer-launch command; Python isolation flags do not impose resource caps.
- tools/Run-V5-Check.py:15-16,42-53,89-106 supplies the actual enclosing Job in
  retained experiments, but hard-codes this repository, the old v4 supervisor
  installation and experiment paths. It is not a deployable ordinary user launcher.

The shipped commons.py CLI is not that missing launcher: its Release class binds
the historical v4 release schema/layout and its public action set does not accept
ordinary owner/peer operations. run_stage.py's CLI likewise requires its specific
installed domains/stage layout, including install/py paths (315-329), rather
than being a documented drop-in ordinary-package command. Do not expose arbitrary
raw subprocess commands to remote peers as a shortcut.

## Smallest responsible implementation direction

Reuse installation/supervisor/commons.py:166-319 and run_stage.py's existing Job
class rather than invent new containment. A fresh public launcher can bind the
approved package/profile/runtime, select only the existing local owner/peer/query
entrypoints, and put their entire process tree in one original finite envelope
before remote input is processed. Inputs and command choice remain operator-local.
Keep native nested limits, accepted-state transaction rules and current locks.

The outer controller must be a small trusted supervisor, not another parser of
peer evidence. Keep package/runtime/state/output separation and fresh diagnostic
output. Do not renew resource grants on retries; do not double-count nested CPU.
Resource termination must report an interrupted/unknown operation and preserve
actual committed state for existing recovery, not invent mathematical rejection
or roll back legitimate earlier partial success. A child success string alone
cannot override an exhausted envelope or uncertain cleanup.

The existing primitives provide OS Job private-commit/process/lifetime controls
and sampled wall/total-CPU/log checks; preserve those exact claims and possible
sampling overshoot. They are not hard real-time scheduling or a disk quota.
Using them does not create filesystem/network privilege isolation, protect secrets
from approved hostile code, or repair a checker memory-safety vulnerability.

## Cheapest decision-changing evidence

First inspect the fresh launcher's fixed-command/bootstrap/ownership path and
reuse prior supervisor evidence. Then only focused controls of the new dispatch,
budget forwarding and failure reporting, plus one small actual public-operation
launch and one bounded controller-level resource refusal if source reasoning
leaves the integration uncertain. No new mathematical episode, certificate,
hostile corpus, broad fuzz campaign or full product rebuild is justified here.
Root selects exact execution only after source review.

This does not claim all release security is solved. Approved ordinary project
execution still needs its own policy/isolation, and untrusted native parsing still
depends on checker/runtime integrity. But making a required resource envelope
actually obtainable is a concrete prerequisite for safe multi-agent/public use,
with substantially clearer payoff than another optional search or hosting facade.
