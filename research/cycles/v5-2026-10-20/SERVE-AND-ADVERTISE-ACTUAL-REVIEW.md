# Ordinary advertised hosting: actual-adapter source review

2026-10-20, core_growth. Source-only independent review; no imports, execution,
networking, runtime census, native checking, proof work or Git mutation.

Disposition: **no decisive API, scope, deadline or cleanup blocker found for
the one proposed bounded same-host data-only composition**. This is not an
execution result or final-v5 adoption.

Reviewed adapter: `software/v5/client/advertised_service_check.py`, 10,671 bytes,
SHA-256 `f98ab404edfa0d090f54877ba9cb2a738b7ac328ca07cb1445a2e75fa3ba6127`.
The reviewed service boundary is the fresh advertised-service entry, with the
unchanged portable role-aware controller, workflow, location protocol and
ordinary search client/session. Root must bind the exact current source map
and enclosing Job before any launch.

## Decisive checks

- Three sockets reserve distinct ephemeral loopback port choices concurrently,
  then release them. The sorted exact allowlist covers the reader, provider and
  HTTP ports. Port reassignment remains a normal race/failure, not authority to
  retry or broaden egress. There are no public network addresses.
- The reader starts with no configured HTTP contacts and an empty bootstrap
  list. The provider bootstraps to the reader's actual PeerID/address. The reader
  learns a provider identity through `route`, then its HTTP endpoint through
  the existing Noise-authenticated descriptor path. The shared allowlist does
  contain the eventual HTTP address as permission data, as the report states;
  it is not a discovered contact. The service's saved endpoint is used only
  after descriptor adoption to assert equality, never injected into search.
- `ServiceLocatedWorkflow` accepts precisely the role-aware reader instance.
  Its route returns `peers`/`route_key`; descriptor adoption issues contacts;
  `begin_search` returns the existing located search client. Direct
  `SearchClient.page` returns `VERIFIED_PAGE`; this is correctly distinct from
  the higher client facade's candidate-only lane.
- The structural fixture's theorem-kind and sort-result features match the
  query. The adapter does not execute predecessor test methods: it reuses only
  fixture/setup/context/reopen/teardown helpers. The one exact expected record
  has no proof or mathematical warrant. Offer/page validation authenticates
  committed index data, not mathematical truth or complete global coverage.
- The location workflow reserves one route, 256 events, two provider slots,
  one descriptor and one resulting contact. Its reply envelope is exactly
  262,144 search bytes plus 4,096 descriptor bytes = 266,240. The single search
  reserves two HTTP requests, one snapshot and one page, with at most four
  examined records/candidates; offer/page maxima are each 65,536 bytes.
- Both Node roles have finite service, operation, IPC, descriptor and aggregate
  transport limits. Provider command reservation is 1 publish +
  `(ceil(45/5)+2)` health observations + 1 stop = 13, below both the configured
  24-command budget and retained channel ceiling. Reader performs locate,
  descriptor and stop within its separate budget. No failed operation is
  automatically retried or refunded.
- Provider configured lifetime is 70 seconds, compatible with a maximum
  45-second active interval plus two ten-second phase reservations. The actual
  service derives a possibly shorter active deadline from the original inner
  deadline and preserves HTTP/Node/final cleanup margins. Workflow time is
  capped at 25 seconds and the reader's earlier absolute deadline. A slow
  startup may cause refusal/noncompletion; it does not authorize a new budget.
- On success the adapter waits for the service's terminal PASS, exactly two
  HTTP requests and reopening of the preserved fixture. That service owns
  location-before-HTTP-before-workspace closure. On earlier failure the adapter
  cancels and awaits the service task, then separately attempts reader stop and
  close. Reader nonzero exit, channel failure, forced termination, cleanup
  errors or exhaustion of the original inner deadline prevent PASS. The outer
  Job remains the hard bound if synchronous work or cleanup misbehaves.

## Cost and interpretation

The proposed outer envelope is finite: 45 CPU seconds, 120 wall seconds,
512 MiB, with the adapter's inner deadline at 105 seconds. These are prospective
ceilings, not measured costs or a guaranteed completion prediction. Two real
Node processes will perform the unchanged full runtime/source pre/post checks;
this is not an optimization or bypass of that integrity work. The operation
does not require Lean, a receipt owner, proof production or a rebuilt runtime.

The exact test is useful for the newly composed ordinary service ownership path,
not for scale, repeated renewal, independent operators, public reachability,
continued availability after failure, semantic reuse or net useful growth.
Successful local hint dispatch remains unacknowledged remote placement. The
actual subsequent locate/descriptor/offer/page chain, if it passes, would supply
the separate positive observation of this one discovery path. Failures and
their costs must remain recorded rather than triggering an automatic repeat.

## Selector and prepared-map supplement

Read-only review also clears `Select-AdvertisedActual.ps1`, SHA-256
`253f21c65695b5100e828f3b389c8fed3eaeffe9a312a6baed678762378492a3`.
It checks the fixed control-plan identity, every inherited source/runtime pin,
the reviewed adapter and the retained manifest/Node identity before exclusively
creating a new selection. It does not launch or copy a runtime. The original
controller's exact 5,896-file runtime-role census/pre/post validation remains
mandatory during a selected actual operation.

I read the root-prepared plan
`experiments/v5-local-checks/advertised-service-actual-01-selection.json`,
SHA-256 `54ab4bf6209251540fcc6a51556044457a07a59a3eec943ebeeee6ac61898365`.
Small-map comparison finds exactly 113 source entries: all 112 control-plan
entries unchanged, plus only reviewed adapter `f98ab404`. All 19 inherited
runtime pins are unchanged; the only additions are the retained Node binary
`b3094d0b49f9ad602262a9921551737bb97637c05dd357a06ae98188d7290aa3`
and fixed release manifest `a93714ec`, for 21 entries. This supplement did not
rehash the large runtime or execute the selector.

The selected argv uses the pinned Python with `-I -S -B`, the staged adapter,
and fresh `{output}/actual`, matching this adapter's own output-creation
contract. Limits are exactly 45 CPU / 120 wall seconds / 512 MiB / four active
processes; one Python worker plus two Node children fit that active-process
ceiling. The 112 unchanged sources include final service `80d6c074`, with the
minimum Node timer correction already reflected in the control selection.
No additional operation, retry or installation change is selected by this
review. Runtime authority remains solely root's separate finite decision.
