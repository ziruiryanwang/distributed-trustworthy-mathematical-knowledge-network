# Replica custody state contracts: source-only implementation

2026-09-21. Author: `bounded_domains_author`.

Status: **authored, not imported, parsed, compiled or executed by this author**.
The reviewed replica product patch is a prerequisite, not applied by this work.
The tests import installed product files and deliberately refuse a pre-replica
installation. No dynamic execution of the draft patch is used.

## Scope and exact boundary

The new file is `software/tests/test_replica_custody.py`. It contains exactly
**14 unittest methods**, with finite negative-case loops. It exercises real
`ControlStore`, real SQLite schema 3 transactions, real Windows owner locks,
`ReadOnlyControl`, installed dispatch/commit logic, the shared custody helper,
the new service selection validator and the existing peer recovery transition.

Every initialization, mathematical ID, formal-metadata offer, package pin and
original acquisition preparation in the suite is explicitly synthetic. The
fixture's context says `synthetic-fixture-not-accepted`; it contains only the
foundation shape needed by the local ledger paths. It is not an accepted context
or a Lean observation. Supply observations are mocked. The received and
normalized package paths never exist. Their manifest digests intentionally
differ, so retaining the original representation cannot pass by conflating the
two pins. Their schema-valid digest-shaped IDs do not attest to real contents.

Fixture acquisition uses the **actual acquisition commit branch**, with
synthetic preparation supplied directly, followed by actual terminalization.
That branch constructs the candidate/acquisition/response bindings being tested.
Malformed-ledger controls use explicitly labelled fixture-only SQL mutation or
new content-hashed records; no production mutation interface is claimed.

The two dispatch tests replace only the peer operation's `replica_expose`
preparation method. Actual `Dispatcher.execute`, reservation, peer prepare
routing, commit recheck, visibility transaction, terminalization and replay are
retained. The dispatcher is assigned an actual `PeerOperations` instance, so
dynamic configured-source-pin loading is **not** tested. Synthetic prepared
views are ledger fixtures with nonexistent files, not serveable views.

Checker loading, public checker access, subprocess launch, socket creation and
transport/service entry points are forbidden. Each teardown verifies the exact
installed product import closure. One recovery-negative fixture deliberately
allocates a charged **stage bookkeeping row** using `ControlStore.stage`; it
creates no stage directory or process and demonstrates the existing peer
zero-stage refusal. This does not contradict the prohibition on native launch.

## Methods and discriminating assertions

| Method suffix | Actual contract | Explicit exclusion |
| --- | --- | --- |
| `acquire_commit_retains_received_and_normalized_pins` | Actual commit retains both distinct pins, charges 64 MiB, creates no publication or stage | Acquisition preparation/transport |
| `exact_ledger_both_interfaces_without_source_copies` | Helper succeeds identically through writable/read-only stores while paths are absent; ten tables unchanged; write through readonly refused | Package validity or HTTP serving |
| `legacy_no_custody_and_wrong_client_refuse` | Legacy missing custody, wrong client, candidate-as-acquisition and absent handle refused | Migration of legacy acquisitions |
| `acquisition_exact_fields_received_and_request_key` | Six controls: boolean/integer distinction, bad request keys, wrong lexical incoming path, digest mismatch, extra field | Filesystem races |
| `remote_endpoint_catalog_descriptor_and_bundle_bindings` | Eight acquisition/remote identity, configured-endpoint and catalog controls | Real remote authentication |
| `snapshot_membership_and_offer_correspondence` | Ten controls: boolean/zero/out-of-cut/over-ceiling sequence, wrong provider/cut/boolean cut, package/descriptor/metadata mismatch | Global ledger consistency |
| `original_request_exact_binding_and_terminal_phase` | Seven controls: wrong client/ID/operation/remote, empty raw, pending phase and absent origin row | Original supervisor/source-cut authentication |
| `candidate_and_terminal_response_exact_binding` | Eleven controls: candidate shape/bindings, bool/int terminal aliases, extra accepted field, false status, bad candidate type and wrong-client candidate | Mathematical acceptance |
| `new_preparation_requires_received_copy_before_checker` | Real preparation refuses absent incoming copy before checker access, with no ledger mutation | Successful canonical preparation |
| `dispatch_precise_view_only_charge_and_historical_replay` | Exact expected ten-table image, one request and +80 MiB, only attempt/view/terminal changes, hard native-allocation guard and byte-for-byte historical replay without reserve/prepare | Real completed view/files |
| `commit_rechecks_custody_foundation_and_exact_selected_row` | Three prepared-binding controls plus changed origin after preparation; charged refusal, rollback of visibility and no view/publication promotion | Crash durability |
| `service_replica_exact_selection_and_absent_source_independence` | Both store types; nine malformed selections each; no package reads or network; unchanged ten tables | `service_worker.operation`, pins, frozen bundle validation and HTTP |
| `publication_authority_has_no_custody_fallback` | Ordinary unpublished `expose` refused; service publication branch requires exact publication and local metadata/manifest correspondence; duplicate rows refused | Genuine local publication; fixture publication row is synthetic |
| `replica_peer_recovery_and_ordinary_mode_guard` | Exact operation sets, pending peer terminal-only transition/replay without refund, staged-peer refusal; actual ordinary allowlist refusal before authentication | Real supervisor quiescence and successful receipt authentication |

`ReadOnlyControl` is opened against an initialized inactive real fixture and
retains its actual query-only SQLite transaction. The tests do not replace it
with a dictionary stub. Malformed helper calls compare the complete ten-table
contents before/after through both store interfaces. The positive dispatch
comparison derives the exact new request, view record and attempt record, not
just row counts.

The service tests prove source-copy independence of **ledger authorization**
only. The separate connecting workflow must still establish successful real
acquisition, original-versus-normalized manifest handling, exact reconstruction,
committed frozen-view serving with other copies unavailable, and fresh checking
and substantive reuse by a third node.

## Source closure and finite run proposal

No runner edit was made. The existing `run_state_contracts.py` registry can be
extended by root, after separate review, with:

```text
suite: test_replica_custody.py
tests: 14
prefix: replica-custody-contract
scope: replica custody state contracts; synthetic packages/quiescence and mocked preparation/supply; no native acceptance or serving
sources:
  py/capacity.py
  py/storage.py
  py/node.py
  py/peer_wire.py
  py/peer_service.py
  py/peer_node.py
  py/inspect_context.py
  py/service_worker.py
  py/recovery_worker.py
```

These are nine suite-specific modules. `domains.py` is the tenth imported
product module and is already a shared runner pin. The runner's five shared
inputs are interpreter, runner, `run_stage.py`, `supervise.py`, `domains.py`.
Thus five shared inputs + nine suite sources + suite file = fifteen inputs;
the exact launch file is the sixteenth supervisor pin. Neither `checking.py`
nor `recovery_manage.py` is imported/read by this suite. Ordinary-mode receipt
refusal intentionally stops before those source pins would become necessary.
Root's pre-execution review found that the receipt-file envelope requires both
request and command entries before reaching that guard. The fixture now retains
and hashes an explicitly synthetic, unauthenticated command payload too; this
repairs refusal ordering without claiming command or receipt authentication.

Reuse only the existing bounded runner envelope: 60 wall seconds, 30 CPU
seconds, 512 MiB memory, eight processes, and 65,536-byte stdout/stderr/event
bounds; 256 MiB/4,096 files/8,192 entries retained after quiescence. These are
**proposed execution ceilings, not measured results**. Root alone owns the
fresh allocation, registry entry, source pins, launch and outcome audit.

The suite uses external `DTMKN_TEST_ROOT`, checks it is absolute, non-reparse
and separate from installation, and requires a new `replica-custody` directory.
Each test creates its own finite fixture subdirectories and retains them.
All stores and locks close in teardown. Every method writes a bounded
`report.json` with scope, notes, exact imported-product paths, close errors
and a bounded file digest census. Each census permits at most 2,048 entries,
512 files and 16 MiB; each individual file and report is at most 1 MiB. The
outer runner independently enforces its aggregate endpoint retention bound.
These observations are not transient filesystem quotas or proof of future
disk supply.

## Required review and next evidence

The author used textual inspection only. Independent review should verify
schema-valid fixtures, expected refusal order, exact method/import counts,
read-only transactions and absence of accidental native or network execution.
Root should integrate the separately reviewed replica patch, rehash the actual
product and runner cut, and run this suite once under a fresh reviewed launch.
Any correction after a run requires a new allocation and fresh exact pins.

Passing these contracts would establish this bounded state-machine cut, not
qualify the product as available, decentralized, operational across hosts or
capable of sustained useful mathematical growth. Existing native qualification
does not automatically cover replica exposure.
