# Installed connected service 02: independent outcome and cause

2026-10-20, `core_release`. Saved evidence/source only. No rerun, runtime,
rebuild, full Node/asset scan, RAM investigation or Git operation.

**Disposition: the end-to-end search attempt FAILED. Actual installed public
hosting, both READY roles, sampled health and orderly closure succeeded.**
These distinct observations do not promote the failed attempt into a pass.

## Cause: underfunded existing page-route reservation

The adapter reports `IncompleteReadError`. The active atomic provider inherits
`delta.transport.CompositeProvider._serve`, with retained page route ceiling
`ROUTES['/v5/discovery/page'] = 1,048,576`. That handler has per-request overrides
for offers, candidates and compact summaries, but not the legacy page route.
Thus a page reserves the full route ceiling even when its client request caps
the actual page at 65,536 bytes.

The successful offer charged 1,973 reply bytes. The configured service total
was only 1,048,576. Before page dispatch, the exact quota condition is false:

`1,973 + 0 + 1,048,576 > 1,048,576`.

The handler catches its `DELTA_PROVIDER_REPLY_QUOTA` exception, increments
failures and closes without an HTTP reply; the client observes EOF. The handler
does not preserve the exception message, so this reason is source-derived from
the fixed control flow and saved counters, not a nonexistent recorded traceback.
The page's fields/caps satisfy `discovery_query.validate_request`; source review
also confirms the accepted-page result shape used by the remaining assertions.
This is a test service-quota provisioning mismatch with the existing coarse
reservation policy, not malformed page syntax or a resource-limit termination.

## Actual extent and evidence boundary

- Both reader and index-provider were actually observed READY. The real
  installed public wrapper and boot exited successfully, with 107 exact
  installed SDK/owner sources snapshotted into the public run.
- The service dispatched one route hint, observed 13 health statuses over its
  exact 120-second active interval, and recorded one successful descriptor
  request (542 reply bytes, no descriptor failure).
- Two HTTP requests were received: one successful 1,973-byte reply and one
  failure. Given the exact adapter's sequential code and validated second
  request, route/descriptor acquisition and OFFERED acceptance preceded the
  page failure. The adapter saved route/offer values only after page success,
  so their individual values are absent from `actual-result.json`; do not
  invent an independently saved successful-page or returned-record result.
- Provider `service-result.json` says PASS for operational lifecycle, not for
  every request: its HTTP counter explicitly records one failure. Final locator
  status is STOPPED, with zero active connections and no exhausted transport.
  Location, HTTP and workspace closure flags are true with no cleanup error.
- Reader and provider processes returned zero, channels remained healthy and
  neither was forcibly terminated. Both preserved exact runtime pre/post checks
  and role-source bindings. Reader commands were locate, descriptor and stop.
- The fresh workspace-reopen assertion was after page success and was therefore
  not reached. Clean provider-reported closure is not relabeled as that check.

## Bindings and costs

Original and saved selection hashes match
`f7f080a1094671de1403c812ed773e45502b1ff217655a50a2f49c3a469fc670`.
Both selected sources match originals/snapshots; all 39 runtime/input pins match.
All 107 public source originals and boot snapshots match their exact pins.
Reader and provider Node maps bind installed `base`, manifest `a93714ec`, and
respectively installed portable source versus the actual public boot snapshot.
No older source/runtime fallback is admitted. Large runtime checks are reused
from their successful saved pre/post evidence, not rerun by this audit.

The public wrapper completed in 130.9139573 seconds with zero remaining child
processes and no cleanup errors. Boot confirms OS Job membership; observed
boot output was 1,262,927 bytes / 144 entries. The service finished before its
original outer deadline. Overall adapter status remains FAIL and child exit is
1. The enclosing Job closed/reaped cleanly with zero active processes, no
termination request and no cleanup error. Known CPU is **21.5625 seconds**
(20.578125 worker + 0.984375 wrapper); wall is **139.13196419971064 seconds**.
The original 570-second inner and 600-second outer deadlines were not renewed.

| Saved evidence under `experiments/v5-local-checks/installed-connected-service-02` | SHA-256 |
|---|---|
| `RESULT.json` | `99081f2bfe5be039209d4a290b5b89e8ff63536147cf3bdf1942f033df1eebe8` |
| `evidence/actual-result.json` | `0339b00356b9151b636a7c20f57edd463cfa87dde6c2a0d9677169c6bfc0990a` |
| `evidence/operations/installed-advertised-02/RESULT.json` | `ede54b8c912a082eb9a41be6a754b9f2607877923a6197b9565edb96af86c1f1` |
| `evidence/operations/installed-advertised-02/BOOT-RESULT.json` | `4830d824ed6deb94e77cb60fe2963f7c03613c0174c01df690da82d4d06a77b2` |
| `evidence/operations/installed-advertised-02/work/service-result.json` | `5fa0d3a68a6685d892b162a1cd0bf6cbc14f90d0f946c55c220d09219bdfff5b` |

## Narrow prospective correction

Without changing the installed product, the finite two-request service can fund
the offer's maximum 65,536 bytes plus the legacy page reservation 1,048,576:
**1,114,112 bytes** total. That is the sufficient worst-case caller allowance
for this sequential request shape, not a RAM increase. A fresh adapter should
retain progress after each route/descriptor/offer/page so later failures do not
erase completed evidence. All other query/runtime/resource caps remain fixed.
Root separately selects any fresh source and operation; actual01/02 remain
failed, charged and frozen. No mathematical or final-v5 claim follows.
