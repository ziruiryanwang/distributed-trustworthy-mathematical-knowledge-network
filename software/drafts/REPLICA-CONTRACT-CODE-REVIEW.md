# Replica custody contracts: independent source review

Reviewed 2026-09-21 by `context_dependency_audit`.

**PASS at the source-review gate for the exact corrected suite below. No blocking correctness or fixture-operability finding identified.** This verdict is conditional on integrating the separately reviewed replica implementation patch. It is not a test result, an exact-launch review, a successful receipt-authentication result, or native custody/serving/availability qualification. The current product still has the pre-replica operation set; the suite intentionally rejects it. Root alone owns integration, registry changes, a fresh pinned allocation, execution, and retained-outcome review.

This reviewer read all 14 methods, their fixtures/helpers/teardown, the complete contract implementation note, the replica patch and its independent code review, and relevant current storage, dispatch, read-only, peer, service, recovery, and runner source. Inspection used source text and inert filesystem/hash operations only. No Python import, parsing/compilation, test/product execution, SQLite query, patch application, or repair was performed. Only this review note was written.

## Exact reviewed cut

Paths in the table are relative to `E:\Distributed Trustworthy Mathematical Knowledge Network\software`.

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `tests/test_replica_custody.py` | 35,765 | `42834201F49FB6FB75F052B4D9BB2D411D91511220C77EB110B0756BFF3122D7` |
| `drafts/REPLICA-CONTRACT-IMPLEMENTATION.md` | 10,007 | `255ED129627C0CBF043FBCE79D79E0F5A46DD84D1B333CDB2383F77154FD892C` |
| `drafts/REPLICA-IMPLEMENTATION.patch` | 22,216 | `5618AE27E3FF592C6D8F1BDD7EAD6DAB23DE81D8CE07103329D917CA6DD72EBA` |
| `drafts/REPLICA-CODE-REVIEW.md` | 11,911 | `83E891FF778DB4F2972973F8BEA96B2DE0F662A2AA71306B35736AC3EF61FC4D` |
| Updated `tests/run_state_contracts.py` | 12,490 | `6D841EF83299961E381576E9966BCE3709DB88F9EE4D2FBDDEF17831AB241088` |
| Prior runner retained in `qualification/ordinary-abort-contract-01/sources/run_state_contracts.py` | 12,029 | `F6DB9EBB9B8573FE6372EF37CAF517BEEB3D131B1406A59415D7CEC657A9A528` |

The suite hash matches root's assigned corrected source. Line references below refer to this suite unless another file is named. During this review root added the exact proposed replica registry entry. This reviewer verified the actual six-line, 461-byte addition and an exact comparison with the retained prior runner after removing that addition: all remaining text is identical. This review includes that registry delta at the source-review gate, not an unobserved exact launch.

## Fixture validity and boundaries

The fixture at lines 122-175 uses actual `ControlStore`, schema 3 SQL transactions and Windows owner locks. Its capacity values satisfy current `initial_authorization`: 8 requests, 4 stages, 1,024 MiB cumulative staging authorization, 8,192 metadata pages, 8-MiB ordinary / 64-MiB acquisition / 80-MiB exposure request grants, and a 128-MiB stage grant. Physical-supply observations alone are mocked at the `storage.physical_supply` binding used by the store. This is not a disk reservation or a measured-supply result.

Initialization, foundation/descriptor/replay IDs, formal metadata, remote selection and acquisition preparation are explicitly synthetic. The initial context says `synthetic-fixture-not-accepted`; no synthetic record is described as accepted mathematics. The advertised entry has the exact required fields, digest shapes, descriptor kind `(0x8111, 3)`, replay kind `(0x15, 3)`, matching metadata identities and positive bounded bundle length. The normalized manifest pin is `a...a`, the original received pin is `b...b`, and both package directories are absent. Thus an accidental collapse of original and normalized representations is discriminated without claiming that either package exists or validates.

The actual acquisition commit appends the local offer, creates the candidate and acquisition records, retains `received_package`, and supplies the real response subsequently terminalized in the same transaction. That exercises commit binding, not acquisition preparation/transport or original supervisor authentication. The fixture-only SQL mutations and replacement content-hashed records are plainly labelled malformed-ledger construction, not supported production mutation interfaces.

`ReadOnlyControl` is not mocked: it opens the actual database read-only/query-only, begins its real read transaction, and requires initialized state and an inactive meta slot. Deliberately malformed origin rows do not silently invent an active meta slot, so these negative fixtures remain openable. The boolean-cut control is also discriminating: SQLite stores its column as integer 1, but the snapshot's hashed JSON preserves `true`; the new helper explicitly rejects the decoded boolean cut after the existing reader returns it.

The dispatcher is assigned a genuine `PeerOperations` instance. This deliberately bypasses dynamic configured-source-pin loading, which therefore remains outside the test claim. In the dispatch tests only that instance's `replica_expose` preparation method is replaced. Request parsing, operation routing, reservation, peer commit, custody recheck, transaction rollback/terminalization and historical replay remain real.

`Dispatcher.checking`, read-only checker loading, `subprocess.Popen`, socket construction, and transport acquire/catalog-fetch/serve entry points are forbidden. Inspected reachable paths introduce no alternate native or network launch. The direct `ControlStore.stage` call in the recovery-negative control is a charged SQL bookkeeping row; current `stage` creates neither the recorded directory nor a process. This must not be confused with invoking the forbidden dispatcher allocator.

## All 14 contracts

Every row below was traced against the proposed patch plus current supporting source. Finite negative-case counts agree with the note.

| Suite line / method suffix | Source-review result and actual boundary |
| --- | --- |
| 249 / `acquire_commit_retains_received_and_normalized_pins` | Actual acquisition commit preserves distinct package pins, 64-MiB charge and zero stages; ordinary publication lookup refuses. It does not exercise preparation, normalization or a remote transfer. |
| 263 / `exact_ledger_both_interfaces_without_source_copies` | Actual helper returns the same acquisition/selection/offer tuple through writable and read-only stores while both package paths are absent. Package-path/read helpers are forbidden; the read-only write guard refuses. Complete ten-table images remain equal. |
| 280 / `legacy_no_custody_and_wrong_client_refuse` | Missing received custody is refused through both stores; wrong-client, candidate-as-acquisition and absent-handle controls produce the current reader's expected codes. Those three reader-identity checks are writable-store controls, not a claim of duplicating every such control through read-only. |
| 291 / `acquisition_exact_fields_received_and_request_key` | Six controls reach the intended exact-field, boolean/integer, lowercase key, lexical incoming-path and received-digest checks. New malformed acquisition handles and terminal-response rebinding keep earlier authenticated-record checks meaningful. |
| 308 / `remote_endpoint_catalog_descriptor_and_bundle_bindings` | Five acquisition mismatches and three remote/configuration controls reach `REPLICA_REMOTE_BINDING`. Remote replacement also rebinds the origin request bytes; the controls do not depend on an unrelated stale remote-handle mismatch. |
| 322 / `snapshot_membership_and_offer_correspondence` | Four sequence, three cut/provider/type and three offer-correspondence controls reach the specified refusal codes. Exact serialized correspondence rejects boolean aliases and metadata/package/descriptor differences. |
| 344 / `original_request_exact_binding_and_terminal_phase` | Seven finite origin controls cover client, request ID, operation, remote argument, empty raw, pending phase and absent row. The schema permits these deliberately malformed test rows; helper refusal happens before promotion and both store interfaces preserve all ten tables. |
| 363 / `candidate_and_terminal_response_exact_binding` | Four candidate and six response controls plus one wrong-client candidate cover exact shape and type-sensitive correspondence. A boolean candidate fails the explicit terminal type guard; the wrong-client string handle reaches the real record guard. |
| 381 / `new_preparation_requires_received_copy_before_checker` | Actual peer preparation traverses custody and foundation checks, then missing incoming `lstat` raises `OSError`, translated to `PEER_LOCAL_IO_FAILURE`. This precedes checker access and leaves all tables unchanged; it proves no successful preparation path. |
| 390 / `dispatch_precise_view_only_charge_and_historical_replay` | Expected ten-table image is constructed exactly: one terminal request, one attempt, one view, request count +1 and charge +80 MiB, with all other values unchanged. Native allocation refuses before store staging; replay returns identical terminal bytes with both reserve and prepare forbidden. The committed view is synthetic and its directory remains absent. |
| 428 / `commit_rechecks_custody_foundation_and_exact_selected_row` | Three prepared-binding controls produce `REPLICA_COMMIT_BINDING`, retain the 144-MiB aggregate charge, clear active, preserve authorization/grants/head/provider/snapshot/entry/stage state and all non-attempt prior records, and create no view/publication/artifact. A fourth control mutates origin bytes after preparation and reaches `REPLICA_REQUEST_BINDING`. These are charged refusal/rollback checks, not crash-durability tests or full byte-by-byte expected images for every refusal request row. |
| 457 / `service_replica_exact_selection_and_absent_source_independence` | Actual selection validator succeeds through both stores with absent source packages and forbids package reads. Nine malformed selections per interface cover row shape/type, provider, basis, descriptor, count, foundation, exact entry and multirow custody. All ten tables remain unchanged. Frozen-file validation, service startup, pin loading, parsing and HTTP are excluded. |
| 489 / `publication_authority_has_no_custody_fallback` | Ordinary unpublished exposure and service publication selection refuse despite valid custody. A deliberately synthetic publication record then tests original-versus-normalized manifest mismatch, exact publication handle and duplicate sequence. The positive read-only publication branch is bookkeeping-only, not a real accepted publication or catalog-build result. |
| 523 / `replica_peer_recovery_and_ordinary_mode_guard` | Exact peer/ordinary operation sets are asserted. Actual peer recovery changes only pending response/phase and active slot, preserving counters and all other rows; historical replay is byte-identical. A staged peer is refused unchanged. Ordinary-mode evidence refusal uses the corrected synthetic envelope below and makes no successful-authentication claim. |

The helper-malformation wrapper snapshots the complete ten tables before/after both writable and read-only calls. Fixture construction is intentionally outside those no-mutation comparisons. Positive dispatch and pending recovery have exact expected images, rather than relying only on row counts. Recovery receives synthetic quiescence directly and uses the actual original-attempt binding; it does not authenticate a real supervisor before that transition in this suite.

## Corrected synthetic command envelope

Lines 551-574 now write and pin both `request.json` and `command.json` alongside the explicitly synthetic receipt. This corrects the prior early `RECOVERY_RECEIPT_FILES` obstruction: `recorded_file` first requires both names in the receipt envelope even when asked to read only the request.

The current `recovery_worker.authenticate_evidence` order is:

1. Resolve the adjacent receipt in the configured scratch `calls` directory and validate its profile.
2. Check the required file-envelope names, read/hash the selected original request, parse it with the integrated operation set, and bind client/request ID.
3. Refuse `replica_expose` in `recover_ordinary` with `RECOVERY_ORDINARY_OPERATION_FORBIDDEN`.
4. Only after that guard, read/parse the command, authenticate the original source/configuration pins, and compare the exact command.

The fixture's `synthetic_unauthenticated_command` payload therefore is intentionally not an authentic supervisor command. It is retained and accurately hashed, but the refusal path does not authenticate its bytes or read the absent config file. No pin set or real quiescence is fabricated for this guard. The expected specific exception would fail if evaluation instead reached the pin-count guard or attempted successful command authentication. Request/envelope checking does occur before the operation guard; “pre-authentication” here must mean before command/source-cut authentication, not before every identity-input check.

## Actual registry delta, closure and finite allocation proposal

The actual added registry entry is consistent with the suite: `test_replica_custody.py`, exactly 14 `test_` methods, prefix `replica-custody-contract`, and the note's explicitly synthetic/no-native/no-serving scope. The original ordinary-abort entry, limits, retention values, ordered pin construction and coordinator/worker behavior are unchanged.

The nine suite-specific source paths are exactly:

```text
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

Together with shared `domains.py`, these are the ten imported product modules asserted by `MODULES` and teardown. Their direct/transitive top-level imports close over the same set and the standard library. The reachable checker-free paths do not import/read `checking.py` or `recovery_manage.py`. The ordinary-mode guard precedes the recovery routine that would require those source pins. The coordinator's shared `run_stage.py`/`supervise.py` are supervisory inputs, not part of the suite's asserted product import set.

The runner's ordered `paths` list therefore has 5 shared inputs (interpreter, runner, `run_stage.py`, `supervise.py`, `domains.py`) + 9 suite sources + 1 suite file = 15. Appending the exact launch gives 16 supervisor pins, at the current maximum. No slot remains for an additional imported/read source without revisiting the envelope. After integration, all actual source hashes and the modified registry/runner hash must be freshly pinned and independently checked; base-file hashes are not the integrated cut.

The unchanged proposed runner bounds are 60 wall seconds, 30 Job CPU seconds, 512 MiB, 8 active processes, 65,536 bytes each for stdout/stderr/event, and endpoint retention of 256 MiB / 4,096 files / 8,192 entries. They are finite execution ceilings, not established timing, memory or storage observations. The suite selects an existing absolute non-reparse external root, creates a new `replica-custody` directory and fresh method/fixture directories, and has no retry/delete path. Its finite method loops construct 54 fixtures in total; the largest method constructs 11. Each method closes retained stores and owner locks, checks exact product imports, and writes a report with a bounded digest census. The per-method census guards at most 2,048 entries / 512 files / 16 MiB, with a 1-MiB per-file and report limit; outer aggregate retention remains independently enforced. These are post-operation observations, not transient filesystem quotas. Exceptional teardown/import/census failures may prevent a report and correctly prevent a passing suite; no report-completeness guarantee on failure is implied.

## Handoff conditions and remaining evidence

No suite correction is required by this source review. Root should integrate the exact reviewed replica patch only after preserving the earlier native cut, then freeze/hash the actual closure, reviewed updated runner and suite, and seek the separate exact-launch review before executing once in a fresh allocation. Preserve any failure and use new allocation/pins for subsequent corrections. Existing ordinary-abort contract counts and exact peer-operation assertions must not be silently treated as compatible with the expanded product set.

A later contract PASS would establish only these bounded, partly synthetic state-machine contracts. It would not establish real acquisition/normalization, new-view canonical reconstruction, actual completed frozen-view serving after source copies disappear, original supervisor authentication, real process-tree quiescence, native acceptance, useful mathematical reuse, multi-host operation or sustained growth. Those remain separate evidence requirements from the replica implementation review and its connecting workflow.
