# Repair orderly shutdown without cancelling a healthy in-flight health command

2026-10-21, root. Source inspection of actual127 establishes a reachable defect,
independent of the unknown cause of contribution01's close failure. Service
7e735337 cancels its monitor before shutting down the locator. The monitor may
be awaiting advertisement5aa23ee7 health, which uses controller4dc0824d command.
Cancellation after an IPC write legitimately marks that controller channel failed
and kills the child. Service then correctly refuses orderly closure. Therefore
the service can itself invalidate otherwise healthy shutdown. Do not weaken the
controller's frame safety or the service's strict CLOSED requirements.

Select a fresh source successor only at
software/v5/managed_close_drain/client/serve_placement.py. Core_release owns
implementation and MANAGED-CLOSE-DRAIN-SOURCE.md. Preserve the selected service
exactly except the minimum monitor quiescence/close safety seam: wake it, allow
its already-bounded health operation to finish without cancellation, then perform
the existing stop/close sequence. Respect the original outer/stop deadlines and
existing cleanup reservation; any timeout/failure must remain a failure with
bounded cancellation/outer recovery. Do not silently extend service authority,
renew budgets or treat diagnostics as closure authority. Ensure still-live
background actors cannot permit store closure. Startup cancellation and public
protocol/acceptance rules should remain unchanged unless the source argument
demonstrates a necessary adjacent correction.

Screen owns independent exact source/design review after completing its current
finding. Guest, after the pure diagnostic actual audit, owns a smallest
deterministic regression design/implementation in the fresh successor directory:
barrier-controlled status reply during close, plus a bounded unresponsive or
failing status case. Exercise real selected orchestration/controller methods;
synthetic I/O is not actual network evidence. No broad network/proof campaign.
Root owns exact selection, source map and future build. The observed-only build
is held: combine reviewed diagnostics and this repair in one fresh candidate if
the design/review/control gates pass, instead of rebuilding twice.

No runtime, build or public02 is selected by this source decision. Previous
sources, installations, failures, grants and charges remain immutable. Full v5
remains the objective; this is a concrete ordinary-operation defect, not a new
optional mechanism.

Pre-use implementation clarification: author found the original stop-relative
activity cutoff reserves two locator operations but omits intake drain when a
short locator deadline is the limiting cutoff. Select the adjacent stricter
margin `active_end <= stop - drain - 2*operation - 1` (or equivalent reviewed
bound), still inside the unchanged outer reservation. This shortens admitted
activity rather than renewing authority and provides health/drain/stop room for
the repaired close sequence. Reviewer must check the exact arithmetic and the
unchanged public02 fixture's available interval before launch. No general
timing-guarantee claim under arbitrary scheduling or failed components follows.

Root read authored source039c96ff/note8866511d, exact three-block diff, and
independent combined-selector reviewcd245a92; source-only AST parse passes.
For the unchanged public02 fixture, `d=35`, `o=10`, `c=6`; with owner cutoff O
and locator cutoff O-7, S=O-43. The new stop-relative activity bound is O-99,
whereas the unchanged outer reserve already requires activity <=O-101. Thus
this stricter margin does not further reduce that fixture's available service
interval. Actual startup/owner checks still decide feasibility; no allowance is
renewed. Await independent service review and deterministic controls before
the combined build. Selector865d97c1 replaces exactly two of127 SDK entries.

Second pre-use clarification: flooring remaining seconds is not by itself a
proof that the later-created grant deadline is <=active_end; constructor elapsed
time can consume the fractional remainder. Root authorizes one immediate
post-construction guard of that exact inequality, before provider construction.
This validates the reserved cutoff or refuses; it never extends it. Source039c
is therefore superseded before use; final pin requires screen's review.

Root now fully read/adopts final service review922fe5f2 and control review8b450d0e,
plus updated combined-selector reviewd1cd020b. Final servicec815331f and
controls46c0817c both parse. Select exactly the three extracted-method controls
through selectorfe847ceb: six source snapshots,28 retained runtime pins,
10CPU/30wall/128MiB/one process. Guest's explicit synthetic I/O and source-only
construction-margin proof are appropriate; no additional startup campaign.
Read-only root hash of the relevant asyncio/tasks.py matches3dc29324; this does
not make the runtime hermetic. One fresh managed-close-drain-controls-01 output,
no automatic retry. Core independently audits actual evidence after root's run.
Build and public02 remain unselected pending these actual results.
