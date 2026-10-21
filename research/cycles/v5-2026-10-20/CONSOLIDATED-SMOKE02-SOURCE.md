# Installed restart smoke02: narrow source repair

2026-10-21, support_screen. Source-only implementation of
`CONSOLIDATED-SMOKE02-SELECTION.md`; no execution or new qualification.

Fresh source: `software/v5/consolidated_candidate/restart_smoke02.py`,
39,791 bytes, SHA-256
`a6e4dd616b614cb01181fa482f9340bd817098ea17453e0cd394bc403345912f`.
Used `restart_smoke.py` remains exact 38,004 B /
`e8b3a0257785e82242d20eb98a24fa4b3fad3b5884e77dc6e7a791598a6cccc2`.
Smoke01's failed input, snapshots, installed state, result and charges are
unchanged; it is not resumed or relabeled.

## Exact delta from the used adapter

1. Import the already installed `placement.network.public_response` alongside
   `PlacementClient`. After the actual one remote submit, derive the expected
   complete wire response from `first.ledger.public(committed)` and the actual
   returned route, under the original expected bindings/request ID. Require
   both `committed["manifest"] == raw` and full projected-response equality.
   Do not compare the seven-field durable diagnostic object directly with its
   deliberate two-field public projection.
2. Save the observed response, original manifest and three bounded diagnostic
   hashes before that assertion: committed manifest, full unprojected committed
   outcome and projected full response. The original complete `committed`
   object remains untouched in memory and all cross-restart exact comparisons
   and read-only durable snapshots remain unchanged.
3. Add `pending_observation()`: count all pending noncurrent asyncio tasks and
   save at most 32 coroutine code identities. Each identity contains only a
   bounded source label, code-qualified name and first line number. Installed
   source paths are relative to the selected installation; the current owner
   file is labeled by its name; other source origins use a fixed outside-scope
   marker. Missing code is explicitly UNKNOWN. No task repr/custom task name,
   arguments, frame locals or arbitrary coroutine state is serialized.
4. After all owned roles and stores have closed, record the pending census,
   execute exactly one `await asyncio.sleep(0)`, and record the second census.
   `pending_async_tasks` is the second count. The same strict zero-pending rule
   and original owner-deadline check still determine cleanup success. There
   is no task-kind exemption, generic cancellation, polling/retry loop, real
   duration sleep or renewed authority.

The full installed adoption, 121-file SDK/18 selected Python binary pins,
mandatory concrete Node-runtime validation, exact original fixture, one submit,
sealed two-run generation, B1-close-before-B2 ordering, original horizons,
bounded route/descriptor alternatives, independent full-goal acquisition,
unchanged-data assertions and strict concrete service closure are byte-for-byte
inherited except at the locations above. The CLI/input schema/result filename
are unchanged; root owns fresh02's input/output selector.

## Why this is not weakening the boundary

The wire projection is the product's existing intentional privacy/resource
diagnostic contract, not an ad-hoc omission from expected data. Exact durable
receipt equality is still required across reopening and retained advertisement.
The fresh comparison additionally checks the entire actual wire response
against the same public validator used by the installed provider/client.

One event-loop turn is only scheduled cancellation settlement after actual
role closure. Source diagnosis identified Windows' separate accept-cleanup
coroutine as a compatible explanation for smoke01's single pending count;
smoke01 did not capture its identity and this source does not invent one.
The fresh pre/post observations make that distinction inspectable. Any task
remaining after the fixed settlement, any concrete close failure or any elapsed
original deadline still fails. Outer process containment remains required.

## Review and execution boundary

The fresh file was mechanically derived from the exact used source by the four
narrow edits above. Changed portions were read back and both file hashes checked.
Support_guest owns the independent narrow-diff/selector review after the actual
smoke01 failure audit. Root owns any finite fresh selection and launch.
No product edit, installation copy/rebuild, syntax/import execution, network,
proof/native/verifier call, trust adoption, Git operation or old-data mutation
was performed by this repair assignment. The original same-installation finite
envelope is retained; the full final-v5 objective remains open.
