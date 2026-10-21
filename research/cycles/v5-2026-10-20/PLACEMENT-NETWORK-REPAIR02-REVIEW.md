# Placement-network repair02: changed-boundary source review

2026-10-21, adaptive_audit. **PASS for the selected narrow source repair and
fresh-selection construction; not an execution or integration pass.** Root
retains launch/adoption authority. Failed01, its charges and all used source
and evidence remain frozen. No product import, network, test, proof or selector
execution occurred in this review.

Read the repair selection, the close decision with its explicit O+1 headroom
correction, the service author note, exact old/new source diffs, complete new
selector, and the unchanged interfaces directly affected by the repair.

## Exact reviewed files

All paths are relative to the canonical Trustworthy project root.

| File | SHA-256 |
|---|---|
| `software/v5/placement_network02/client/serve_placement.py` | `319ddf075d2bd62c6e408dcc497fc5c507d277787637b0089aa60fbc65c96430` |
| `software/v5/placement_network02/integration.py` | `e5979ec3cd57c0bc74bc025156b6e8d7a146a8dca2513c8f20b6c94381580efd` |
| `research/cycles/v5-2026-10-20/Select-PlacementNetworkIntegration02.ps1` | `19d1e9ff0da0e45cccb0d717e093249a8ff4ab05da3f1294752106419e5f9561` |

The reused wire and advertisement remain respectively
`1ec5c452ec129ae033f0577ebac6223e2cf3192d4724a3d31fe2e5c27a06cd4b`
and `b5523f82f6d5eba4ba9e72639888f1c9da014f298aa9c1081c76aa3f920f35a6`.
Service predecessor `07c60c4f33401d41694228d0f6bde35d9148e769947b75211e9ed4098ec68674`
and adapter predecessor `d71925cd57b2d3b438081bf340984bca272a409b89fec50931ea6fd86c449305`
are not edited. Diffs contain only the changes discussed below.

## Close-budget composition

Let D be the existing maximum role operation interval plus5s, O the locator
operation interval, C its unchanged6s process-teardown allowance, T the original
service outer deadline and A its active deadline.

The successor reserves both role drains:

`A <= T - (2D + 2O + C + 5)`.

Allowing up to2s for the existing two cancellation joins, D for intake drain,
O for the stop command and C for native teardown gives validation start no
later than `T - D - O - 3`. Against the fixed locator-close cutoff
`T - D - 2`, at least **O+1 seconds** remain. The originally proposed O+3
omitted those joins; the selected correction is necessary and used here.

This is conditional allocation algebra, not a scheduling or filesystem-speed
guarantee. The actual code:

- Only enlarges the reserved shutdown portion, possibly shortening service;
  it does not extend the original service/grant/locator deadlines.
- Uses the fixed cutoff in `asyncio.timeout_at`, not a renewed duration from
  the moment cleanup starts, with a positive-remaining precheck.
- Checks the same cutoff after awaiting close, so synchronous validation that
  finishes late cannot receive successful closure merely because the event
  loop did not preempt it.
- Preserves the locator's shielded close task, native teardown code, complete
  adoption/runtime and role validation, actor-idleness/store-close conditions,
  remaining read drain and final original-outer-deadline refusal.

An expired/overrun cutoff still produces cleanup uncertainty. A shielded inner
task may finish after the caller has timed out; that does not become a passing
service close. External process containment remains necessary; asynchronous
timers are not hard preemption of synchronous I/O. The unchanged outer runner
documents sampled wall/combined-CPU accounting, not a new exact real-time bound.

## HTTP authorization and reachable continuation

The adapter changes only its explicit finite provider reply allowance from
8MiB to32MiB. Product route caps and reservation rules do not change. Both A and
B still have two connections, sixteen requests and5s operation limits.

For the selected serial workflow, A serves one group opening, one small packet
offer and one packet. B serves the bounded discovery offer/page, one group
opening and the offer/packet acquisition. The group reservation is16MiB even
when the opening is small; the preceding bounded discovery replies are far
below the extra16MiB. Thus this change removes the proved initial reservation
contradiction for both A's placement pull and B's later reader acquisition.
It does not guarantee admission of every possible sixteen-request sequence.

Checked the newly reachable path rather than repeating previous controls:
declaration acquisition uses its explicit65536B client bound; indexed export
acquisition uses the returned record's committed object size, not a mandatory
16MiB client reservation. The shared reader acquisition budget and the source
placement reservation therefore are not silently enlarged to the server cap.
Group/packet readback, index admission, route-journal precommit, identical replay
and status checks remain unchanged. No receipt is trusted during structural
custody or discovery.

The reader still receives a formal binary-congruence goal without the selected
module ID/name/manifest/packet pin. It uses actual located discovery and checks
the complete returned type. A is stopped and closed before that reader starts.
The network must close before the separate genuine received-I verifier opens
the returned group under a fresh temporary trust domain; that domain is then
withdrawn. No proof-generation or new native-check path was added. These are
preserved required checks, not predictions that the next run will pass them.

## Diagnostics and exact source selection

The adapter stores `primary_error` through the existing bounded closed-code
projection before cleanup. Its outer exception handler separately retains
`terminal_error`, rather than destroying the first failure. Added client
reporting contains expected bindings, endpoint and counters, not its bearer
token. Added source status is scalar accounting independent of closed stores.
Both snapshots are attempted on failure and retain distinct cleanup errors.
The report's existing token-exclusion check remains; raw exceptions and request
bodies are not newly serialized.

Adapter and selector agree on explicit physical paths: old wire, old
advertisement, fresh02 service. Snapshot staging remains anchored at the
adapter's actual copied source root. The 114-file basis, qualified replacements
and two independent query helpers are unchanged:129 physical source pins,
121 staged product logical files plus two helpers,25 direct runtime pins.
The selector still verifies the current map and retained inputs, refuses any
existing02 input/selection/output, uses create-new files and makes no runtime
launch. It preserves150CPU/300wall/512MiB/six-process outer limits. There is no
renewal of failed01, installation copy, verifier weakening or new proof budget.

## Disposition

No blocking source defect found in these changed boundaries or their immediate
now-reachable continuation. Root may separately select one fresh bounded
integration02. Actual hashes, outcomes, costs, process closure and admission
must be audited afterward; this source review cannot replace them. No full-cost
growth, independent-host, public deployment or full-v5 claim follows.
