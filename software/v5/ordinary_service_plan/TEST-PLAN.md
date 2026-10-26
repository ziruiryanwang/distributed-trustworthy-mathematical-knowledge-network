# Finite service-plan controls: source checkpoint

2026-10-26. Tests owner: `service_plan_tests`. Source preparation only: no import,
test, native process, network call or execution allocation is selected by this
file. Root must review final sources and select exact finite inputs separately.
The unchanged current package and every historical run remain preserved.

## Decision-changing question

Can one owner authorize a finite sequence of ordinary `peer serve` leases while
the companion refuses unintended scope, reserves the entire aggregate allowance
in advance, and prevents every next epoch after an uncertain or failed previous
epoch? This is orchestration evidence, not proof acceptance, useful growth,
independent hosting or continuous availability.

The tests use the author's private pure validation and finite sequencing seams;
test doubles exist only in this test source, not as a public runner option.
The current source is ready for independent review, not execution. The final
test uses `validate_plan(plan, config)`, `validate_service`, `validate_epoch`,
`report_agreement`, `validate_paths`, `pinned`, `selected_identities` and the
private `_sequence(..., origins=(0, 0))` seam. The genuine case invokes only the
three-option public companion CLI, which in turn uses the unchanged public
launcher. No callback, mock or test switch is exposed through that CLI.

## Proposed focused groups

1. Strict plan/service inputs: valid minimum plan, duplicate JSON fields,
   malformed/types/bools/extra fields, nonzero stable loopback port, exact share
   and exclusive approvals, no index creation and no arbitrary executable hook.
2. Up-front reservations: sum of fixed epoch caps must fit total CPU, attempts,
   payload and logs; no renewal after observed savings or failed service; fixed
   horizon and cleanup reserve. Memory/process bounds are simultaneous caps.
3. Filesystem safety: selected input/state/output paths are ordinary and
   disjoint, including index/config/plan paths; fresh atomically claimed output,
   no resume/overwrite and no child after preflight refusal.
4. Report validation: a clean synthetic report envelope passes, while
   missing/misbound reports, contradictory counters, provider error, nonzero
   active descendants, termination request, nonquiescence or cleanup uncertainty
   fail. Ordinary per-request failures and attempt/payload quota exhaustion may
   continue only into already prepaid epochs when ownership and all service
   reports close cleanly. Accept/cleanup failure remains fatal. Synthetic reports
   are explicitly test values, never saved mathematical acceptance evidence.
5. Finite sequencing: two clean doubled epochs consume exactly two reservations;
   failed first epoch, changed inputs or exhausted original horizon stop before
   a second launch. Ordinary client failure/quota exhaustion never buys an extra
   epoch or a renewed allowance. Capture records establish ordering and no retry.
   A test-controlled clock cannot renew the original allowance.
6. If separately approved, one genuine helper CLI subprocess performs two tiny
   loopback leases through the unchanged pinned public launcher. Fresh empty
   inert state is created through existing constructors; no native initialize,
   admission, publication or accepted context is fabricated. Raw RUN/inner and
   outer supervision/peer reports remain available for independent review. A
   second invocation with the same output must refuse before any new epoch;
   the completed report hash and exact two-epoch directory list must survive.

The implementation reports five test groups: strict schema/reservations;
report binding/provider closure; sequencing; filesystem/pins/agreement; and
genuine CLI operation/no-resume. Schema and reservation cases are combined,
while raw-report agreement and actual preflight file safety share a group.

## Native-free genuine fixture feasibility

Source inspection identifies a no-native route:

- `OrdinaryStore(..., create=True)` creates empty inert custody.
- `OrdinaryAdmission.open(..., create=True)` creates an empty ordinary catalog,
  owner lock and admission-call directory. Do **not** call `initialize`, reserve
  a basis, write roots, copy an old catalog or synthesize a checked event.
- `DiscoveryStore(..., create=True)` creates a genuine empty metadata index and
  empty snapshot using its ordinary constructor.
- Close these handles before the public helper starts. `peer serve` opens that
  same empty catalog through its ordinary lock but does not require a checked
  context. It exposes no mathematical objects.

This needs the existing exact Python/Lean installation attachments for loader
verification, but source inspection finds no need to execute Lean or build new
support. Runtime evidence must confirm that distinction. If the actual source
API requires native initialization after all, stop and report the obstruction;
do not broaden the allocation silently. A fixed nonzero loopback port is chosen
in advance; collision is a retained failure, not an automatic retry or new port.

## Economy and preservation

Do not repeat native, transport, mathematical-growth or package-build campaigns.
No cloud, external endpoint, scheduled task or publication is involved. Tests
write only beneath one root-selected fresh evidence directory and preserve every
partial outcome. Exact source hashes, envelope and outcome audit remain root's
separate responsibility.

## Proposed single finite execution envelope

This is a proposal only; root's exact reviewed selection is required.

- Test command: selected Python `-I -S -B test_service_plan.py --source ...
  --source-sha256 ... --package ... --profile-sha256 ... --python-runtime ...
  --lean-runtime ... --output ... --port 38194`. Root may choose another single
  nonzero loopback port before selection. There is no automatic replacement or
  retry if the selected port is occupied.
- One root-selected outer Job: 240 wall seconds, 200 aggregate Job CPU seconds,
  1536 MiB simultaneous commitment, eight active processes, bounded 4 MiB stdout
  and 1 MiB stderr. Test cooperative deadline is 220 seconds / 60 controller CPU
  seconds. The root supervisor's CPU observation includes all test descendants;
  do not add the test's inner/epoch CPU counters to it a second time.
- Exactly two helper subprocess invocations: one authorized two-lease plan;
  then the existing-output refusal (zero epochs). Exactly two ordinary public
  `peer serve` calls occur inside the successful helper. There are no public
  mathematics commands and no external clients; both one-second services listen
  only at the selected loopback port and must report zero accepted attempts.
- Each public lease uses 35 wall / 20 CPU seconds, 512 MiB, three active processes,
  1 MiB stdout and 1 MiB stderr. Each enclosing companion epoch uses 50 wall /
  80 CPU seconds, 640 MiB, four active processes and the same stream caps.
- The plan has a 160-second original horizon and 60 controller-CPU allowance.
  Its prepaid aggregate is 220 CPU seconds, eight accepted attempts, 2 MiB
  response payload and 44 MiB selected stream/metadata reservation. These are
  caps/reservations, not predicted actual use or hard total-wire/disk guarantees.
  The stricter experiment Job may end a malfunctioning test before the entire
  plan authorization is consumed. No automatic replenishment is allowed.
- Peak memory/process limits are simultaneous and nested, not additive runtime
  costs. The largest active tree is the test, companion, launcher and peer;
  no Lean process is selected. The retained public worker-CPU counters and empty
  catalog `roots`/`operations` tables must confirm no native mathematical work.

The test creates only its root-selected fresh evidence root, ordinary inert
SQLite stores and small synthetic controls beneath it. The hardlink negative
creates two names for a new synthetic fixture file; it never links or modifies
project/runtime/state files. Fake PEM/offer bytes test path disjointness only and
are never supplied to an actual network/TLS operation. All partial files remain
after any failure. Actual raw outcome review, not this plan, determines success.
