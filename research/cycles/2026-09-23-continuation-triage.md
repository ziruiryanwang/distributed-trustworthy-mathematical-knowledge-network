# Continuation at finite boundaries: bounded source06 triage

2026-09-23. Read-only product inspection; no imports, calls, tests, builds,
private-key reads or product edits. Canonical workspace guard passed.
Source06 and all used installations remain frozen. Root owns current contact
qualification; this note does not re-audit or replace that evidence.

## Decision

Do **not** select database migration, unlimited counters or hosting rollover
merely because finite limits exist. An existing public path already supports
selective mathematical succession: serve a previously committed view, acquire
it on a fresh compatible node, and freshly admit it there. It does not preserve
old handles/history, but those are not required for mathematical reuse.

The smallest genuine continuation gap is narrower: selected knowledge that
has **not yet acquired a committed exposure view** can become inaccessible
through the normal contribution API when ordinary request/byte/metadata
admission is irreversibly exhausted. Files are not thereby destroyed, but the
public owner API has no credit-independent export/reintroduction path for them.
First test the existing exposed-view exit path at exhaustion; do not implement
a broad replacement lifecycle before that discriminating test.

## What actually exists

| Situation | Supported behavior and exact source evidence |
| --- | --- |
| Initial authorization spent below lifetime limits | `manage renew` explicitly adds capacity. `storage._grant_proposal` (line 487) requires initialized/nonpending state, fewer than 64 grants and totals at most 4096 requests, 256 stages, 64 GiB; it never resets usage. `capacity.parse_grant` (line 45) validates the envelope. |
| Native stages spent, request/byte headroom remains | Metadata/transport operations can still run; native stage allocation alone checks its separate stage allowance (`storage.stage`, line 459). `expose`/`replica_expose` perform no native check but still reserve ordinary requests/bytes (`node.execute`, line 365). |
| Ordinary credits exhausted, committed view exists | `manage.serve` (line 192) issues one new finite owner session directly. It does not call `store.reserve`. `service_worker.operation` (line 67) reads committed authority and frozen view bytes through `ReadOnlyControl`, then serves inert data. |
| Cumulative `host` journal full | `hosting.run_grant` (line 352) stops at 128 grants / 4096 slots. These are limits of that journal/controller, not of all owner service: explicit `manage serve` has its own fresh finite session and does not inspect or reset the hosting journal. No automatic switch is implied. |
| Snapshot/view needed after original supplier disappears | An already committed replica view is independently retained. `peer_node.replica_custody` (line 35) checks ledger authority without reopening original custody packages; `service_worker.validate_selection` (line 33) uses it. Existing view bytes and original state/config are still required. |
| New node with same compatible foundation/profile | Public `configure` creates fresh state with only fixed common packages and empty offers (`manage.configure`, line 78). Ordinary `peer_find`, `peer_acquire`, fresh `admit`, then `replica_expose` or a new derived contribution supply the selective continuation route. |
| Old private artifact/accepted package but no view and no remaining ordinary admission | There is no `manage export`, `restore`, `import` or backup command in the parser (`manage.main`, line 244). `expose` requires published candidates; `replica_expose` requires an acquisition and retained original incoming package (`peer_node`, lines 318/362). Both first need ordinary reservation. Internal codec export is not an operator continuity API. |

`ReadOnlyControl.__init__` (inspect_context.py:27) requires the correct schema,
initialized/nonpending state and no nonempty SQLite auxiliary file. It does
**not** require positive remaining requests/stages. Therefore exhausted credits
and damaged/uncertain state must not be conflated. Manual service is not a way
around unresolved descendants, a pending request, corrupted state or a failed
hosting outcome whose worker quiescence has not been established.

The manual-session path also does not promise indefinite resource availability:
it creates new retained scratch evidence, requires an owner action, retains
finite CPU/wall/connections/bytes, and leaves disk/runtime/key availability as
premises. No old hosting reservation is refunded or erased.

## Scope of selective succession

A fresh node gets its **own** configuration, contexts, local handles, requests
and endpoint authorizations. It checks mathematics itself. It does not inherit
the previous node's accepted flag, grant budget, client namespace, unpublished
draft source, pending-work state or history. This is intentional non-migration.
An old complete exposure may carry a selected root's dependency closure, not
every result ever admitted or published by the old node. A replica exposure
is one acquisition, not an aggregate export of all acquired entries.

Software-profile changes split into distinct cases:

- If old frozen reader/runtime remains usable and new software accepts the
  same wire, canonical formats and foundation, ordinary exchange can bridge
  their different local config/database formats without moving SQL state.
- If wire/foundation/canonical semantics are incompatible, source06 has no
  translator or compatibility promise. Fresh rejection is correct. A new
  explicit mathematical bridge would need its own scope and tests; this is
  not grounds to invent one before a concrete incompatibility is selected.
- An unusable old installation, lost view, disk failure or damaged control
  store is not solved by capacity renewal. `QUICKSTART.md:288` and
  `RECOVERY.md:54` already disclose the absence of qualified backup/restore.

## Next falsifiable test: existing API before new code

Use a separately authorized fresh bounded allocation and an existing genuine
compatible mathematical package; do not author a new theorem benchmark.

1. Prospectively configure predecessor A with exactly five ordinary requests
   and two native stages, with enough byte/metadata supply for the planned
   operations. Initialize, discover, acquire, freshly admit, then
   `replica_expose` the selected acquisition. The fifth request consumes the
   last ordinary credit; the second stage has already been consumed. Retain
   the exact view, acquisition and final status. No counter edits or resets.
2. Confirm a fresh ordinary request refuses `REQUEST_QUOTA` without mutation,
   but owner status remains available. Do not renew A for this case.
3. Use **explicit `manage serve`**, not a new cumulative host grant, on that
   already committed view. A fresh B acquires it and locally admits the exact
   type/reference/proof package; A remains request/stage-exhausted and its
   heads, authorizations and old receipts remain unchanged.
4. Require clean finite service termination and retain every failure and cost.
   B's fresh admission, rather than A's historical acceptance, is decisive.
   No additional proof-authoring benchmark is needed for this boundary test.

Complement with one cheap synthetic boundary check if needed: maximal ordinary
totals and full completed hosting-journal counts must not be prerequisites of
the independent `serve` path; an active/pending control state must still refuse.
Do not create thousands of public requests merely to synthesize a hard ceiling.
The real five-request test establishes authorization exhaustion, **not** actual
consumption of all 4096 lifetime requests or 128 hosting grants.

Pass implies a documented, owner-operated selective exit is viable for already
exposed mathematics. Failure identifies a concrete implementation/operating
obstacle; preserve it before selecting a successor. Existing ordinary transfer
tests do not by themselves establish this exhausted-credit boundary.

## Smallest patch candidate only if that remaining gap is selected

For unexposed published/acquired results at an irreversible ordinary boundary,
consider an explicit, bounded **owner egress** operation selecting existing
owned immutable records and writing a new inert export/view without spending
ordinary research credits. It must validate stored bindings and exact package
closure, preserve all old state, enforce separate finite resource authority,
never execute new source, and never transfer mathematical acceptance. Reuse the
existing canonical bundle/view plus fresh receiver acquisition/admission path;
do not add SQL-state transplantation or general peer trust.

This is a candidate, not an approved implementation: decide whether selected
published candidates/acquisitions are sufficient before including private
artifacts or corpus enumeration. Its decisive test would start with genuine
retained selected mathematics but no view and exhausted ordinary admission,
then export and freshly admit it on B while keeping A unchanged; missing or
corrupt retained bytes must refuse. No need to claim that raw filesystem or
undocumented codec scripting is impossible—only that it is not currently the
supported public operator workflow.
