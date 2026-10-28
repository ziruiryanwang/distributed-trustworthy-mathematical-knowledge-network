# Reply-capacity control source review

2026-10-28. **PASS for the bounded root-selected controls, source review only.**
No outstanding defect was found in the final source below. No candidate imports,
test execution, sockets, SQLite opening, theorem execution, owner-state access or
Git operation occurred during this review. Only source/manifest/evidence reads,
static JSON inspection and file hashing were performed.

## Exact reviewed inputs

- `control_tests.py`: SHA-256
  `b9ee3e5e437e4b680ab10283aeeaae251cb838263c4e5fed236d1a0ffdb6ae8d`.
- `http_provider.py`: SHA-256
  `929fbf453bb23d353f89384db3dbb8cd4e11e6fd5383a09a36d93fc92631b93b`.
- Package: `experiments/v5-local-checks/dedicated-host-assembly01/distribution/package`,
  PROFILE SHA-256
  `21bcb169cced5d85c3d2272265ef1f24f6848fbe2da0d2ab3f3acfe27697bba7`.
- Its installation manifest SHA-256 is
  `9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27`,
  matching the PROFILE's `installation_manifest_sha256`.
- Evidence:
  `experiments/v5-local-checks/observation-growth-produce01/units/c59ee7bd4eed61193dc06729ca76e28887ad83171f11173353e93bb46305c2c4.json`,
  26,650 bytes, SHA-256
  `bf13287aed53c34ccf58798d3e77ab0df1b60f74ed780641de88a9dc7fd813bd`.

All paths are relative to the canonical project root. These are source-review
pins, not an execution selection or a claim that controls passed at runtime.

## Findings resolved before execution

The initial `request_reader` omitted `Content-Type: application/json` and
`Connection: close`. Actual provider `_headers` requires both, so all requests
would have failed before reaching dispatch. Root added both headers; the reviewed
source now satisfies the real parser's request-line/header/body profile.

Two assertions were strengthened after review. The too-small-object case now
requires the real `SELECT length(raw),raw_sha256 FROM objects` trace and forbids
`SELECT raw FROM objects`, distinguishing length refusal from an earlier error.
The overquota preview now requires an empty SQLite trace, distinguishing quota
refusal from a lookup of its deliberately unavailable digest. Neither correction
changes product behavior, and no failed control run was consumed discovering them.

## Loader and fixture compatibility

The ordered loader satisfies the actual selected package's imports: ordinary
evidence precedes semantic/portable evidence, the preview helpers follow, then
formal features and authenticated-index dependencies, pair access and discovery
store, module store, candidate provider, clients and ordinary acquisition. The
synthetic package modules have package paths; each loaded child is registered
in `sys.modules` before execution and attached to its parent afterward. This
supports the selected relative imports and dataclasses without ambient product
modules. Deferred imports reached by put/locator/evidence are already present.
Unselected feature-adapter and network-client paths are not used by these cases.

All 13 package support entries were inspected against their actual manifest
keys, sizes and hashes: no mismatch or missing row. Installation files correctly
drop the `installation/` prefix when indexing the installation manifest; other
support files use PROFILE paths. The candidate provider is separately pinned,
and the selected package's original provider is the unchanged predecessor
`d9c342d1dcb5ee3e4b293e8dc0566397a321cc59a6f545e2f2afde452c760251`.

The evidence is V2 ordinary evidence with a three-field ordinary unit and one
five-field declaration. Its sole output name is `ResetEffects.contextual_iff`;
its declaration kind is 2 and its import array has 27 entries. Thus
`parsed.document["unit"][2][0][0]` selects the actual output name, not an import,
expression or census wrapper. `PE.export_id(semantic, unit, name)` is the same
portable identity function used by `OrdinaryStore._export_locators` for that
output. The production parser and scratch put will validate it again during
the selected control run; this static review is not mathematical acceptance.

One object/one output fits the scratch limits of eight objects, 64 exports,
1 MiB logical storage and 256 SQLite pages. The exact 26,650-byte evidence and
short locator fit the 30,000-byte success grant. All chosen provider grants
exceed its 1,024-byte minimum. The 128 KiB writer bound comfortably covers each
complete header/body, and this evidence fits within one 65,536-byte body chunk.

## Seven groups and race behavior

The seven recorded groups cover complete locator/evidence replies despite large
client maxima; length-first refusal of an oversized unit; unavailable evidence
and invalid original Boolean cap; exact exhaustion; retained/released live-write
reservation; cancellation after charging; and unchanged preview/offer quotas.
They invoke the actual request parser, `_serve`, dispatch and scratch ordinary
store. Success compares exact evidence bytes and aggregate charges, while the
original caller dictionaries are checked unchanged.

`_serve` charges the full actual body before `_write` sends the response header.
`Writer.drain` therefore signals its event at the header drain after charge and
before reservation release. With the 40,000-byte cap, the held evidence request
has charge 26,650 and reservation 40,000. The next locator sees a negative
conservative remainder and must refuse. Releasing the event lets both header
and body drains finish; reservation release then permits the small locator.
The harness deliberately calls `_serve` directly for the competing request,
avoiding its serial `call` helper's zero-reservation assertion while another
write is live.

The cancellation case waits for the same event, cancels and awaits the task,
then checks that charge remains and reservation is zero. `CancelledError`
propagates through the provider's `except Exception` and still executes its
reservation `finally`; the harness catches it at the awaited task boundary.
Both race tasks are awaited in `finally`, before store closure. There is no
artificial suspension inserted between admission and charge; that portion of
the real provider is synchronous. The source accounting proof in `CONTRACT.md`
covers uncharged reservations without inventing a race absent from this code.

The exact-preview negative preserves its identity-bound size and now proves
no SQLite lookup occurred. For the offer negative, an incorrectly admitted
ordinary-only provider would return its small `NO_OFFER` envelope; requiring
no response therefore tests the retained quota boundary rather than absence
of an index alone.

## Scope of the eventual result

The harness requires isolated/no-site/no-bytecode Windows Python without
optimization, fresh output under `experiments/v5-local-checks`, bounded reads,
40 wall/15 process-CPU second checks, and exact support/evidence pins. Root must
select the outer finite process envelope and the exact arguments separately.
It creates only fresh scratch custody and closes it in `finally`. Native/process
launch and normal network entry points are blocked; no provider listener is
started and no peer exchange is requested.

A later pass would qualify these seven controlled parser/dispatch/storage
boundaries. It would not qualify sockets/TLS, full connection cleanup, a complete
public inspection session, native mathematics or broad service performance.
The reviewed source emits the narrower controlled-writer scope and no
mathematical-acceptance claim. Runtime outcomes remain to be observed and audited.
