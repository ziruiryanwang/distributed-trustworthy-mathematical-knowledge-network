# Standard launcher support for the authoring frontier

2026-10-28. Root-selected **source-only** follow-up. No package, runtime test,
owner operation or Git action is selected by this note.

## Concrete missing capability

The adopted demand-frontier package's `owner.py` accepts
`--authoring-frontier-root`, but its `run.py` fixed owner-option allowlist omits
that flag. Thus the direct owner route can select the protected ancestor while
the standard bounded launcher refuses before the child is launched. This is a
user-facing integration gap; it does not require changing the mathematical
frontier rule or repeating the native build.

## Exact successor

`run_frontier.py` is copied from the frozen
`experiments/v5-local-checks/demand-frontier-package01/distribution/package/run.py`
and has only two changes:

1. Add `authoring-frontier-root` to the owner option allowlist.
2. Call the existing `hexid(value)` for that option before appending it to the
   child argument vector. This checks the existing lowercase 64-hex identity
   format and refuses malformed values with `RUN_SHA256`.

The value is an identity, not a filesystem path. It is not added to path/state
sets and changes no diagnostics, writable-state separation, profile binding,
supervision, resource limit or command allocation. Duplicate/missing options,
tool allowlists and exact-option parsing retain their existing checks.

The unchanged owner separately requires `contribute` with both project-authoring
arguments and revalidates the identity. Ancestor membership, protected frontier
validation, source handling and actual-parent mathematical admission remain the
owner/contribution layer's duties. A well-shaped hash is not evidence that the
frontier exists, is an ancestor or authorizes acceptance.

| Source | Bytes | SHA-256 |
|---|---:|---|
| Frozen package `run.py` | 18,894 | `47a2b63c73f1bd8346c5881c6d6a76abac86d33aa8e55bfc19bf3359ea924a39` |
| Fresh `run_frontier.py` | 18,991 | `63f70a8f27645e4e3e3f2ae85296f9c43bc2f0337b4534744dbd5eb0411029dd` |

A standard-library byte comparison confirms exactly these two substitutions;
`ast.parse` accepts the new source. Neither launcher module was imported or
executed. This is source validation, not an executed launcher qualification.

## Integration boundary

The successor is intended to become `run.py` at the root of a later explicitly
selected fresh package. It deliberately retains the original self-relative
package/profile checks and must not be used as a standalone source-tree wrapper
against an existing package. Frozen package/profile bytes remain unchanged.

Root will decide packaging after the substantive contribution outcome. If then
selected, the minimal changed-boundary evidence is: valid frontier option reaches
the unchanged owner; malformed, duplicate and wrong-tool options still refuse;
and the standard bounded public route runs the selected contribution with clean
closure. Existing passing native/build campaigns need no repetition for an
allowlist-only integration change. No new test or packaging campaign is launched
here.
