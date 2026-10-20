# Advertised serving: independent source review

2026-10-20, `core_release`. Canonical guard passed. Source inspection only;
no imports, execution, RAM investigation or Git mutation.

**Disposition: source clear; single inert-control outcome independently audited
PASS.** No blocking finding remains. This is not clearance of the later actual
Node check or public deployment. Source and saved-outcome review are separate.

| Reviewed source | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/client/serve_advertised.py` | 21,486 | `80d6c0746eca23398cfe735af5d8de1076eb3725439414cce68de743c518a7ed` |
| `software/v5/client/test_serve_advertised.py` | 22,679 | `36107587eefd4284970a9a5ac41aa2e8672488e8b55c4714a002918af16384e2` |
| `research/cycles/v5-2026-10-20/Select-AdvertisedService.ps1` | source-reviewed | `dec618fba363a0902214391d09c228a315f9617447eef7a3b2c9e7c22362bba3` |

## Decisive checks

- The namespace and endpoint come from the actual exclusively opened workspace
  and started HTTP provider. The closed owner input cannot replace them or the
  fixed provider role. Discovery dispatch remains advisory and requires matching
  route identity, positive observed write count and no claimed remote placement,
  global completeness or mathematical acceptance.
- The optional retained location installation is canonical, disjoint from the
  mutable workspace/run, pinned to the existing fixed manifest and adopted by
  the unchanged controller. The exact runtime census and pre/post hashes remain
  that controller's responsibility. Boot-selected source pins are used; no new
  manifest authority, executable search or package resolution is introduced.
- IPv4, explicit nonzero HTTP port, TLS and original egress restrictions are
  retained. Public use needs a certificate valid for the numeric endpoint IP:
  `server_name` exists on the returned endpoint but is `None` in this profile.
  No NAT/public reachability inference or endpoint-policy widening occurs.
- Each publication/status uses the earlier phase deadline or one operation
  allowance. Health checks observe both the child and HTTP listener. An initial
  status precedes READY; a reserved final status catches an internally stopped
  locator during the final sleep even if its IPC child remains alive. Process
  exit is independently awaited. The advertised detection delay is explicitly
  conditional on timely scheduling, not a continuous-availability guarantee.
- `ceil(requested_lifetime/health_interval)+2` reserves initial/final and periodic
  statuses; these, all routes and stop fit at most 60 commands, below the
  inherited 62-command ceiling. Two operation intervals reserve final status
  then stop. Location close, HTTP drain and final work fit inside the unchanged
  outer ceiling; the existing one-second Node minimum does not renew that
  parent ceiling. Synchronous hashing/OS delays can still fail the operation.
- Ordered cleanup attempts location stop and close, HTTP stop, then workspace
  close after preceding failures. Forced kill, channel failure, uncertain close,
  elapsed original deadline or primary failure cannot become PASS. Cancellation
  is propagated after cleanup. Remote hints may remain under receiver policy.

## Narrow findings closed before selection

The initial monitor permitted a status wait until the entire active deadline
and omitted an end-of-interval internal-stop observation; bounded per-operation
waits and the reserved final status close both issues. HTTP `is_serving` checks
were added at the same observations. The inherited test context's port zero was
changed to the explicitly allowed port. The selector now passes its existing
output root, matching the test's required-directory contract.

The nine selected controls use real fresh synthetic SQLite workspaces but
explicitly inert HTTP, location adoption and channel objects. They test endpoint/
namespace/pin wiring, invalid input, partial dispatch, startup failure, early
child exit, post-READY HTTP/internal-location failure including the last interval,
cancellation and cleanup failures. They do not execute predecessor suites.
Subprocess/socket entry points are prohibited. No runtime adoption, network
authentication, mathematical authority or genuine Node lifecycle is proven.

The selector preserves the fixed ordinary-serving basis, adds the 21 previously
selected portable location files plus these two new files, and rechecks selected
hashes before exclusively writing a fresh selection. The inspected import
closure needs no additional product source. Its 20 CPU / 60 wall seconds /
128 MiB / two-process envelope is unchanged. `controls-result.json` avoids the
outer launcher's case-insensitive Windows result-name collision.

The current projected public distribution still omits Node/overlay. This source
increment uses an explicitly retained installation and does not close that
packaging gap. Source changes after these hashes require focused re-review.

## Saved single-run outcome

Read-only audit of `experiments/v5-local-checks/advertised-service-controls-01/`:
**nine tests, zero failures/errors/skips**, with the reviewed production/control
hashes. All 112 selected sources match both original and snapshot bytes; all
19 runtime pins match. Original/saved plan hash is
`e450cbe5590f28e5b857d50eb3c48fa71488f1b1742070e59f7f62946010c3fc`.

The saved successful service observes location close before HTTP stop before
workspace close. Saved injected post-READY HTTP/internal-location failure,
final-interval internal stop, child exit, partial dispatch, cancellation and
cleanup-fault outcomes remain FAILED; later workspace cleanup still runs.
The suite records 12 inert HTTP/location starts and 21 inert publish attempts.
Actual Node/network/native/proof calls are all zero; mathematical acceptance
remains false. This is lifecycle evidence, not real runtime/network evidence.

Outer exit is zero with child reaped, Job closed, zero active processes, no
cleanup errors and no termination request. Known CPU is
`1.484375 + 0.4375 = 1.921875` seconds; whole-run wall time is
`9.164585500024259` seconds under the original unchanged caps. No rerun or
product import was performed by this reviewer.

Evidence SHA-256: `RESULT.json`
`e8a051149153976755bfd5722d96d248fe072d581bd9a23cd1d4c3451e7753fe`;
`controls-result.json`
`442fa4983cf0f99552f993ba6abe1b9a6006df8aa9bddf7704e3fb89b4331c3f`.
Root may adopt this narrow passed boundary; the distinct actual composition
question still needs its separately selected evidence.
