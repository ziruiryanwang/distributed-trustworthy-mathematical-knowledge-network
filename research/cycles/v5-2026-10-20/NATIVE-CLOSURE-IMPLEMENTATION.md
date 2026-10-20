# Optional ordinary native closure: implementation checkpoint

2026-10-20, `core_growth`. Canonical guard passed. Implemented only the three
new source files selected in NATIVE-CLOSURE-SELECTION.md. No Python imports,
tests, native execution, proof/build, RAM investigation, installation or Git
mutation was performed by the author. Independent source review and root's
separate finite validation/adoption remain required.

## What this adds

`native_closure.binding.bind_output(raw, wire, targets, adopted_image=...)`
binds the exact zero-claims/zero-frontiers frame and target journals to a bounded
native report. It independently verifies complete framing, no unconsumed input,
empty output assumptions, strict numeric/byte types, full member order and
commitment, exact targets, maximum rank, seal height 1 and bounded census.
It returns inert data and cannot grant authority.

`native_closure.owner.NativeClosureOwner` loads only the existing adopted
resource supervisor and Job helpers, not an I/A verifier. Its hardcoded native
artifact identity is the adopted bounded-parse driver `2306e9f3...`; the image
field inside the frame does not authenticate or select executable code.
The new owner is not a subtype of any existing authority.

Public API:

```text
NativeClosureOwner(supervisor_manifest=..., supervisor_manifest_sha256=...,
  executable=..., runtime_pins=..., adopted_image=..., deadline=...,
  submitted_bytes=..., reserved_cpu_seconds=..., controller_cpu_seconds=30)
check(witnesses, targets, operation_directory,
  cpu_seconds=30, wall_seconds=60, memory_mib=512) -> tuple[VerifiedNativeMember]
describe(member) -> exact J/module/summary/profile/input digest/native proof form
members() -> same immutable tuple of owner-local tokens
report() -> local resource accounting only
close() -> irrevocable local revocation
```

All named constructor and per-call limits are keyword-only. The deadline is
required and is an **absolute monotonic deadline**, not a renewable duration.
The parent reserves this child's finite suballocation once before construction;
the owner never replenishes the parent's grant. No existing client-grant or
semantic-authoring dispatch was changed. Source pins must cover the ten modules
in `owner.SOURCE_NAMES`, the exact native executable and locally selected
runtime; loaded supervisor helpers are also pinned from their adopted manifest.

## Authority and resource invariants

The API is confined to the constructing thread object. One check consumes its
entry/CPU reservation before encoding; framed input bytes are charged before
encoding as soon as a bounded byte-list shape is established. Invalid input or
any subsequent failure closes the owner. No second attempt/retry is available.

One immutable wire is staged in a fresh nonoverlapping directory and checked
through one real supervised native invocation. Input, source/runtime pins,
clean closure, actual CPU/wall, same-call stdout and final deadline are checked
before tokens are published. The source process's original conditional JSON
schema/status is not changed. Mathematical authority is the **separate live
local owner**, not that file or an aggregate header.

Tokens map by object identity to immutable exact J bytes. An immutable accepted
state snapshot prevents a changed membership table, wire or binding from being
used through a previously issued token. Foreign/fabricated/expired tokens fail;
failure revokes all tokens. Every member inspection rechecks live source/pins
and shares the same original controller/deadline envelope and a 128-inspection
ceiling. Exported descriptions are data, not transferable authority.

Valid observed worker CPU is retained even if a returned report later fails
closure or budget checks. Once launch is attempted, missing or malformed CPU
evidence is reported as `None` (unknown), never invented zero. Full CPU/input
reservations remain charged on post-reservation failure. Job controls are
resource supervision under a trusted owner/installation/OS, not a security
sandbox.

## Deliberate boundary

This component permits economical ordinary checking of a small complete DAG.
It does not provide ancestry-independent acceptance, a genuine A certificate,
persistent warm-library authority, semantic READY, native authoring integration,
or a positive full-cost growth margin. Those cannot be inferred from a future
successful component invocation. Existing I/A/mixed source and acceptance rules
are unchanged. Both comparator routes retain their legitimate optimizations.

The reviewer identified a pre-encode entry race in the initial source. The
source was corrected before any execution: thread confinement plus early entry
reservation closes it. The same review prompted explicit unknown/failed worker
cost accounting. Focused independent tests are being authored separately; no
old graph, checker or proof campaign is repeated.
