# Optional operator and launcher: independent source review

2026-10-28, growth_design_audit. **PASS for the three operational source files
below, with the current gateway API reconciled; complete gateway behavior and
package closure remain separate reviews.** No product import/execution, Node launch, database or network was run.
This is source clearance for integration, not runtime or deployment acceptance.

| Source | SHA-256 |
|---|---|
| operator.py | `2f69cefb4567f1e6dafe42523811f60e59788ce36a4bb01f6da408815acfe512` |
| operator_support.py | `645c0c41a3fa21d9d5f78bdb635f0597abd6f6b9a14083787cbf514c65e1b8a2` |
| run.py | `99dfbd6ec0d16abdce5695dd42cd9455679e1a99d3e525022426e4c64568d58a` |

The independent review found and root repaired three concrete issues before this pin:

- Delta output has operational false flags, so the mathematical syntax parser
  rejected every publication. `proposals()` now uses bounded canonical `F.strict`.
- Publication grants and gateway/TLS/provider configuration were validated after
  Node startup/withdrawals. These deterministic checks now precede effects.
- Per-row locator construction/size could fail after earlier effects. All selected
  locators now pass the real portable locator parser and 1-MiB route bound before
  startup; retained exact locator bytes have a separate 8-MiB aggregate bound.

Runtime exhaustion can still leave a partial publication prefix, as explicitly
selected; the finite grant need not promise that every requested publication
succeeds. Existing custody is not rolled back or deleted.

## Exact publication path

Only the owner-selected new bundle is read. Its manifest hash fixes ordered unit
pins; unit paths derive from validated UnitIDs. The reviewed delta helper parses
every supplied unit and includes support-only exports. The wrapper rechecks the
manifest bytes and derives canonical expected locators from actual proposal
SemanticID, UnitID and structured name. No contribution target list is substituted
for the declaration census.

Before publishing each exact ExportID, `OrdinaryAcquisition.locator` reads the
operator-approved own endpoint under one finite ledger and the original service
horizon. Its exact S/E/name validators run, then the wrapper requires byte equality
with the expected S/U/name locator. Only then does it issue that key's private
publish command. The ordinary default remains terminal on failed readback; no
unbounded retry or alternative unapproved custodian is introduced. A verified
locator is eligibility evidence at that time, not proof of retention or availability.

The wrapper preserves partial effects and records per-publication results. On
failure it now retains both conservative eligibility-budget charges and actual
client HTTP accounting. Confirmed publication remains distinct from remote
placement, maintained intent and availability; backend result fields preserve
those distinctions. The role contains no mathematical owner/admission operation.

## Lifetime, failure and role composition

The original wrapper service horizon starts before child verification/setup and
is supplied separately to the controller. `HANDSHAKE-REVIEW.md` covers the source
repair that conservatively transfers this horizon to Node. Metadata/service work,
eligibility reads and gateway replies do not receive a replacement lifetime.
The separate channel deadline and ten-second wrapper reserve retain room for
status/stop, owned process teardown and reporting under outer containment.

The gateway role forbids publication/withdrawals and has no own custody endpoint.
The custodian role publishes/serves peer descriptors and is discovered through a
different gateway. HTTP admission closes before private backend shutdown. The
wrapper checks settled HTTP tasks/connections/reservations, requests reserved
status/stop when still usable, then always closes the child. Backend/gateway
terminal failure, forced termination or cleanup errors prevent a successful
operation result. They are not silently converted to missing mathematical data.

The current gateway API was read at source snapshot
`f00521d6b1a025a8d6f006c8c6534552f1d454bc7e8284e0d071d8d5d89b144c`.
Its `Gateway(channel, policy, limits, deadline)` constructor now permits the
unstarted concrete controller for pure validation; `_owner` requires a live
process when a lookup is attempted. Root also corrected the wrapper's report
gate to test its boolean `terminal_failure is True`, rather than rejecting the
normal false value. The HTTP provider checks this exact gateway type and awaits
its async lookup route. Those interface mismatches are resolved. The complete
lookup algorithm and reader integration are not qualified by this narrow API check.

## Pinned role and public launcher

The support loader captures exact externally selected SOURCES bytes and a closed
module-role set; it executes captured source bytes in fixed import order. It has
no owner, native installation, seed or executable mathematical-basis role. Node
sources are separately pinned. Only the selected Node/overlay runtime projection
is used by the controller. Reader installation/anchor support is unaffected.

The public launcher checks isolated supported Python, bootstrap/profile/config
pins and nonredirected ordinary paths. Immutable software/runtime roots and the
owned workspace are disjoint. State, output and diagnostics are disjoint children
of that workspace; explicit config/bundle/TLS inputs cannot overlap writable
targets. Fresh output/diagnostics and explicit create versus same-config reopen
are preserved. No implicit state deletion or automatic retry exists.

The retained Job supervisor encloses the worker and descendants; the worker
inherits the original wall deadline, not a fresh allowance. Wrapper CPU is
separately measured/cooperatively bounded and is not represented as part of a
hard aggregate CPU cap. Parent success requires exit zero, clean reaping/Job
closure, a bound successful worker report and final input/profile revalidation.
Partial state/report failures remain explicit unknown/failed outcomes.

Remaining decisive work is exact package/import reconciliation, the final gateway
review, small pure controls for the new delta/readback/pre-effect boundaries and
one finite actual operator workflow. Repeating native mathematics or owned-socket
campaigns would not establish these new properties.
