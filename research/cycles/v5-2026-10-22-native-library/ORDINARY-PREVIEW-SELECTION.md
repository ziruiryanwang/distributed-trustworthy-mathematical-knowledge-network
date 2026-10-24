# Inspect candidate types before paying for their proofs

2026-10-24. Root selects the following bounded source implementation. Current
approved-project intake is committed as `386fb0c`; its used bytes stay frozen.

## Consequential decision

A local agent should inspect an unfamiliar candidate's full formal type and
referenced-symbol identities before deciding whether to acquire its proof closure.
A preview does not include those symbols' definition bodies or establish applicability. Existing
`find` returns records, while public `receive` immediately follows its internal
preview fetch with evidence acquisition and admission. The lower-level
`OrdinaryAcquisition.preview` already implements exact preview/record binding.
Expose that existing capability; do not design another index or checker.

The new public operation takes one explicit selection, one finite allowance and
the existing selected contacts. It fetches only that candidate's preview and
recomputes the complete record from the returned bytes. It returns the parsed
canonical preview, hash/length and original selection. No owner/catalog/custody,
proof evidence, dependency locator, native compiler or mathematical admission is
opened. Index membership is not reverified by this command. A well-bound preview
can still advertise false mathematics; final acceptance remains unchanged.

The limits are exactly `requests` (must equal one) and `reply_bytes` (positive,
at most the existing 1 MiB preview ceiling). Refuse a larger advertised object
before I/O. Reuse the existing aggregate network ledger; no new budget after
failure and no automatic candidate loop. Close a ledger only if this call owns
it. Preserve charged failures and exact contact/TLS checks. Later `receive`
still fetches its own preview: that duplicate cost is not hidden or called cache
reuse. Source-contract refinements are recorded in ORDINARY-NEXT-PRACTICAL-PAYOFF
and independently challenged in ORDINARY-DISCOVERY-NEXT-CHALLENGE.

## Ownership and unchanged boundaries

All paths are under `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Every shell uses that explicit workdir; edits use absolute paths.

- `cold_intake_strategy`: fresh `software/v5/ordinary_preview_package/peer_api.py`,
  exact resilient-API successor with only additive preview behavior.
- `project_intake_native`: fresh `software/v5/ordinary_preview_package/peer.py`,
  exact current CLI successor adding preview as a state-free operation, and its
  concise README. Existing operation semantics stay unchanged.
- `module_anchor_audit`: independent contract/source challenge in
  `ORDINARY-DISCOVERY-NEXT-CHALLENGE.md`; no duplicate intake/build reviews.
- Root: focused controls, later file-only assembly/source map, navigation/Git
  and exact finite runtime selection.

Only two runtime payloads should change. Preserve loader, acceptance installation,
owner facade, module-anchor support, native artifacts, wire/index namespace and
all prior evidence. No clean compiler campaign or live network experiment is
selected by this source decision. Review the new boundary before its tests.

## Why this earns its cost

This is an operability and avoidable-cost change, not a theorem-count result.
For inspected candidates that the agent rejects, it can avoid their remaining
acquisition/checking cost. For accepted candidates, current separate commands
add an extra preview and startup cost. Hence benefit requires avoided rejected-
candidate cost to exceed the new inspection overhead; it is not unconditional.
An optimized ordinary-library baseline also gets previewing and warm caches.
No novelty, semantic applicability, global completeness or final-v5 claim follows.

Cheap controls should use the real preview/record validation with bounded inert
transport doubles, including malformed/tampered bytes, absent authority, one
request, shared-ledger preservation and zero owner/native/evidence access.
Only a new uncertain packaging/transport boundary could justify a later small
actual call. Do not repeat the passing reciprocal or native campaigns.

## Selected public-command harness source

Root subsequently assigns `cold_intake_strategy` the source-only
`ordinary_preview_package/public_check.py` and `select_public_check.py` for two
actual public metadata calls after the independently reviewed file-only assembly.
The first uses the retained 1,351-byte preview (SHA-256 `362292c8...`); the second
receives same-length altered bytes and must refuse with
`ORDINARY_PREVIEW_EXACT_BYTES`, retaining its one-request/1,351-byte charge.
A static loopback responder allows at most two connections and only the exact
preview route/request. Its synthetic snapshot label is explicitly not search
membership evidence. No owner/index/custody, native build/checker or proof
acquisition runs; the installed public CLI and HTTP transport are real.

The proposed one original envelope is outer 90 wall seconds / 40 CPU seconds /
768 MiB / four active processes, with inner 75 / 32 / 512 and dynamically reduced
child grants. Reused pinned supervision checks clean closure without conflating
cumulative Windows process counts with concurrent-process ceilings. Explicit
thread stop/join and listening-socket close run in `finally`; immutable package,
runtime and saved-preview pins are retained. Source pins at review submission:
`public_check.py` = `0b5fa2e87694e854ce7e6f7c00b533273496a36fa0ac084305bc21b5feebdf55`,
`select_public_check.py` = `082212b250a97474ad86c4ee7d78474a45e690bf34fd94a579e8c1451fc14df7`.
No runtime is selected or performed by this source checkpoint; root owns the
exact reviewed launch and subsequent outcome adoption.
