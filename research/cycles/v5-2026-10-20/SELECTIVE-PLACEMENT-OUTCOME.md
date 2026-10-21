# Selective placement controls01: actual outcome audit

2026-10-21, adaptive_audit. **PASS for the12 selected owner-local structural
placement controls.** Retained-output/source-binding review only; no rerun,
product import, new fixture, native process, network operation or Git mutation.

Output: `experiments/v5-local-checks/selective-placement-controls-01`.
Root reported one terminal exit0. Retained outer report confirms
`COMMAND_EXITED_ZERO_AND_CLOSED`, direct child reaped, Job closed, zero final
active/terminated processes, two total processes, no cleanup errors or requested
termination. The fixed limits were60CPU/120wall/384MiB/two active processes.

Independent SHA-256 checks match all124 selected physical sources at BOTH
original and snapshot paths, all19 runtime pins, and all118 logical staged
copies/source bindings with exact sizes. Reviewed harness remains32002 bytes,
`819bdf18`; product/controller `ef1c9b59` and selector `14d329f2` are unchanged.
Source/control reviews are `1ddd94c5` and `a04a1da5` respectively.

The actual stderr names all12 expected methods individually and marks each OK,
then reports `Ran 12 tests in 2.729s / OK`. Structured result agrees:12 tests,
zero failures/errors/skips, no forbidden-call attempts and no loop errors.
Asyncio's slow-task diagnostic lines concern successfully finished tasks; they
are not ignored exceptions. Stdout is0 bytes and stderr7695 bytes.

Executed assertions cover reserve-before-effect observed by a separate SQLite
connection; real group/packet/body custody and indexing; exact request replay
through expiry/restart; separately charged same-content deduplication; corrupt
custody with no refetch; domain/fingerprint/target bindings; both Store COMMIT
guards and rollback; partial-index-commit prepaid recovery and durable recovery
exhaustion; original guards at all nested custody COMMITs; propagated cleanup
failures retaining historical state; original finite allowances; and sealed
generation/owner registration. State assertions are in the exact reviewed
executed harness, not independently replayed against mutated databases.

Actual saved simulated-exchange counts:4 for positive pull/custody/index,
2 for failed recovery,8 across nested-commit guard faults,2 across cleanup
failure cases, and0 for every other method. Total16 explicitly simulated
exchanges. These call the real provider dispatcher and custody path but are NOT
socket or TLS measurements. Actual network/native/proof counts are all0;
receipt fixtures remain `INERT_UNVERIFIED_FIXTURES_NEVER_ADMITTED` and
mathematical_acceptance is false. No live mathematical owner is fabricated.

Outer JobCPU3.078125 plus wrapperCPU0.46875 yields **3.546875 known measured
CPU seconds**. Whole-run elapsed time is7.965980000328273 seconds; supervised
time through cleanup is7.8391300002112985. Wrapper-supervisionCPU0.03125 is
already included in wrapperCPU and is not added twice. Quota reservations and
synthetic HTTP accounting are not actual resource savings.

| Artifact under output | SHA-256 |
|---|---|
| `selection.json` | `91cb521a65902358bc1319d1c7f295d1ea1c179c1852cc1fbbc5967f0a871cfa` |
| `RESULT.json` | `836a2eaff7ae9eb26134989510acacf01379398eda4d11de91a69658fd6de390` |
| `placement-controls-result.json` | `fd50790785c2f8a1a9c2e484e8a00fd358b3b52d6ad7691e2183d05b0a9848c3` |
| `command/stderr.txt` | `88f96cd7b4715f2b43859fa5f4b0fe638f13bcfeafb77eb008ef5a0687be57a1` |

This closes the selected owner-local transaction's focused implementation gate.
It does not qualify remote intake, authenticated transport, DHT dispatch,
independent custody, mathematical validity, sustained finite-disk rollover,
full-cost growth or final v5. Root owns adoption and any fresh network-seam
selection. No repeat of these passing controls is indicated.
