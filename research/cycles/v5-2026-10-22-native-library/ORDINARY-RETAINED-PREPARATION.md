# Recover retained preparation without reauthoring

2026-10-23. Source-only successor by `retained_preparation`; no import, test,
build, owner opening, network access or Git mutation. Canonical guard passes.

## Practical endpoint

A successful authoring step can leave an inert candidate that needs additional
library declarations. The original `REQUEST.json`, `owner-request/header.json`,
numbered groups and `targets.json` already retain the preparation. The user
should not manually reconstruct its name-to-ID map or compile the source again.
`software/v5/ordinary_library_support/retained_preparation.py` supplies a pure
bounded decoder; root owns later file acquisition and public integration.

## Interface and authority

`reconstruct_preparation(request_raw, header_raw, group_raws, targets_raw, *,
semantic_id, foundation_id, context_root, warranted_symbol, check_budget)`
returns a frozen `RetainedPreparation`. Binding and output names are canonical
bytes inside tuples, not mutable nested JSON. It includes raw input hashes and
counts. `mathematical_acceptance` is always false.

The caller selects/pins REQUEST bytes and obtains exact bounded files; those
bytes alone do not prove who ran a compiler or what happened historically.
The callback must be a stable lookup in the genuine eligible protected parent,
not a peer map. Every recovered binding is rechecked against it. A forged
historical record cannot grant acceptance. The unchanged candidate/completion
and native-admission boundaries still govern all new mathematics.

## Checks and limits

- Exact REQUEST top-level field set (optional project metadata), selected parent,
  false acceptance marker, exact sequential header/group map and byte/hash pins.
- Canonical V2 header, exact S/F/parent and group count. No V1 translation.
- Exactly 581 basis rows, recomputed basis identities and protected lookup;
  finite group grammar, no duplicate names and exact warranted group IDs.
- Header target IDs are present in the recovered map; target-file pin and exact
  REQUEST output-name bytes agree. Outputs are distinct and absent from parent.
- 32 groups/outputs, 4096 bindings, 1 MiB header/group, 4 MiB request payload,
  1 MiB metadata, 64 KiB outputs, 1 MiB serialized recovered map. Metadata JSON
  rejects duplicate keys, deep nesting, large integers and noninteger numbers.
- Original allowance callback runs before parsing, throughout loops and before
  return. Lookup/cancellation errors propagate; no retry or fresh budget.

Group proof bodies are not rechecked by this utility: their pinned bytes are
only structurally navigated to recover name/ID rows. No body/type from this
record is installed or accepted. The current supporting group format retains
legacy V1 grammar names while the header and IDs are portable V2, exactly as
`portable_owner_request.prepare` produces them.

## Verification boundary

Source-only implementation, not yet reviewed or executed. Future focused
controls should include retained normal data, false file pins, extra/missing
groups, legacy header, wrong parent/IDs, duplicate names/output collisions,
aggregate limits and cancellation. A test here is not native completion or
general Lean-project compatibility evidence. No native experiment is selected.

Source SHA-256:
`f4c51f1a90a75eb153dda10c6c17b9a8eeeca1692275c176f70a15f8499a9bc6`.

## Native-free controls authored, not executed

`software/v5/ordinary_library_support/preparation_controls.py` loads the actual
future selected support package once. Root supplies package/profile/runtime,
fresh output and an explicit `--retained-directory`. Six exact pinned files
from the existing public B-contribution are read, never changed or recreated.
The parent callback is explicitly a fixture-derived map, NOT a protected owner
warrant. Positive checks recover 583 bindings, the exact target bytes/hashes,
and 584 memoized point lookups. This establishes no new mathematical validity.

Seven groups cover actual retained-byte compatibility; metadata/file/context
refusals; forged freshly repinned IDs, duplicate names and target errors;
aggregate/capacity/cancellation failures; installed-Std module path restrictions;
CLI refusals before owner open; and explicitly mocked extraction forwarding,
failure charge/retention and owner/custody closure. Path cases include dot,
separator, absolute-looking, numeric, reserved, control and non-ASCII components.
The synthetic selected-name-cap rows and synthetic 0.25 CPU charge are not
mathematical or actual-native evidence. SQLite, native-child, socket, native
admission/extraction and peer entrypoints are guarded against accidental use.

Internal limits remain 50 wall / 30 controller CPU seconds; a prospective root
selector must enclose them with its finite external envelope and pin all six
fixture files. No test/import/build/owner/native operation has been performed.
