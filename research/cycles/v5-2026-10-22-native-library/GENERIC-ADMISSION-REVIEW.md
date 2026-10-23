# Generic ordinary admission: final source review

2026-10-23. Reviewer: `admission_event_audit`. Canonical workspace guard passed.
This is a changed-boundary review, not a repeat of the previously passed native
checker, portable storage, acquisition or imported-parent campaigns. No tests,
native process, installation, catalog mutation or Git operation were performed.

## Disposition

**No blocking source defect found in the selected generic admission core or its
narrow absolute-parent-deadline repair.** The four focused, native-free control
groups are suitable for a finite root-selected execution. This does not establish
an actual installed admission or complete v5 release.

| Reviewed source | SHA-256 |
|---|---|
| `software/v5/ordinary_lean/ordinary_admission.py` | `5ff149cd74e9d3f5615629fb279de020dfc8926fbc0685a654a48050688658aa` |
| `software/v5/ordinary_lean/portable_catalog.py` | `aeaf0c7d507baa6b63d401c432ca71557bf29b6b576b1f6cd8381e4e87c7473e` |
| `software/v5/ordinary_lean/ordinary_admission_checks.py` | `30b0211bd0ceeeeb0709ddab29585a1f02a4911b3e06bb012f79aa809284aace5` |

## Real workflow and trust boundary

The intended caller supplies inert V2 units discovered/acquired elsewhere,
preflights their finite dependencies against an accepted local context, obtains
the missing frontier when necessary, and admits only new units. The API retains
their exact portable evidence before mathematical promotion. The product gain
is reusable ordinary checking without requiring a certificate campaign or a
fixture-specific integration driver. A known unit does not need another native
checking call. Local source-authoring and distribution remain separate APIs.

The installation is owner-adopted named support, not a peer assertion. Its exact
manifest binds role layout, native helper search directories and file pins into
implementation identity. The core verifies its own loaded sibling modules and
Python executable, compiled module census and all selected file pins. Separately
rooted Python/Lean runtime attachments avoid duplicating whole installed runtimes;
their logical roles and selected bytes remain committed. This still assumes
immutable owner storage, the runtime/OS and a nonhostile in-process caller. It is
not a hermetic build or an arbitrary-host security claim.

The private worker shim cannot promote a catalog. Only the owner controller's
actual clean selected worker event can reach `_commit_checked`, after matching
the live grant, exact parent/module/unit bindings, report names/counts and actual
artifact size. A saved success file alone does not supply that authority. The
selected underlying Lean checker remains unchanged.

## Examined changed boundaries

- Preflight deduplicates exact unit bytes, derives ExportIDs from the actual unit,
  rejects incompatible names/semantics/imports, sorts selected dependencies and
  reports the whole bounded missing frontier. It does not accept a forged READY
  plan: `admit` recomputes preflight from its raw units and current parent.
- Already-known complete groups may be reused only with exact identities and
  exact existing import lineage. Partial groups, selected cycles and conflicting
  supplying declarations are refused. Finite unit/byte/node/name/edge bounds
  constrain this metadata work; they are not kernel-cost bounds.
- Before native reservation, exact evidence is retained through the adopted
  custody API and read back. This supports later rehosting. Storage callback
  presence/readback is not a proof of crash durability; that remains the adopted
  store's separate contract, never mathematical authority.
- The single `OperationBudget` is claimed once and includes preparation, local
  controller CPU and observed native Job CPU. Native allowance reserves shutdown
  time. Controller limits are cooperative unless an enclosing supervisor imposes
  hard bounds; the native Job is containment, not a hostile-code sandbox.
- On an uncertain native cleanup result, the owner catalog is withdrawn/closed.
  Other failures abandon the live reservation without erasing its charges or
  inert evidence. Atomic promotion remains the acceptance linearization point.
  No retry, rollback of accepted mathematics or allowance renewal is implicit.

## Original-deadline defect and correction

Previously the caller computed a relative duration at time `t0`, then catalog
context/evidence preparation consumed `d` seconds before reservation computed
`t1 + seconds`. For sufficient `d`, this exceeded the original caller deadline
`D`; the core's final guard safely refused an otherwise valid affordable batch.

Both new reservation entry points accept optional absolute `parent_deadline=D`.
They reject invalid/expired values before preparation and again immediately
before the grant is registered, then assign

`grant.deadline = min(monotonic_now + seconds, D)`.

Consequently any returned parent-bounded grant satisfies `grant.deadline <= D`
independently of preparation time. Expiry before registration causes refusal
without insertion or operation-directory creation. If the deadline expires
after reservation, existing grant/budget checks refuse continuation. This is a
cooperative wall-clock contract, not a hard real-time promise that a SQLite or
filesystem operation cannot run past a deadline. Compatibility callers omitting
the argument retain the historical relative-duration behavior.

## Focused controls prepared, not executed here

The four source-level groups test:

1. Exact deduplication, dependency ordering and already-known reuse.
2. The complete finite missing frontier, incompatible missing bindings and a
   forged READY plan refusing before custody/native work.
3. Selected/parent names and imports, semantic identity, aggregate name/edge
   limits.
4. A synthetic delayed reservation that would previously renew its parent's
   clock, unchanged unparented compatibility, expired/NaN/bool parent deadlines,
   and no reservation mutation on expiry.

The last group uses a fake clock/database and intercepts directory creation;
it tests the new time contract without Lean, a real catalog or filesystem output.
It does not test real SQL durability, process cleanup or native acceptance.

Root owns subsequent file-only installation and actual public-path selection.
Do not repeat the imported 2859-unit checking history merely to exercise this
new stable controller identity. The next decision-changing native evidence is a
small ordinary contribution/reuse path through the installed API.
