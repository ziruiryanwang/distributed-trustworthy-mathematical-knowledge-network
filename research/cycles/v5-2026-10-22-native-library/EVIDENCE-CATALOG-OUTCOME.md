# Independent evidence-reader and protected-catalog outcome audit

## Decision

**PASS for the selected nine storage/identity control groups. This is not native
mathematical admission, basis qualification, or final-v5 acceptance.**

Auditor: `lean_persistence_boundary`, independent of the authors of
`ordinary_evidence.py`, `local_catalog.py`, and `evidence_catalog_checks.py`.
I read the complete saved implementations/tests and actual selection, terminal
report and logs, and independently compared every selected source snapshot's
SHA-256. No experiment was rerun and no retained source/evidence was changed.

Run: `experiments/v5-local-checks/ordinary-evidence-catalog-controls-01`.

The implementation makes the important distinction explicit: syntactic evidence
and stored claims do not establish mathematics. The catalog's private
`_commit_checked` seam requires a trusted controller to have obtained actual
clean, pinned native checking of the exact reserved operation. These tests
deliberately call that seam with `FAKE_BYTES_NOT_LEAN_STORAGE_CONTROL` and a
synthetic 581-name basis. They establish storage behavior only. No Lean process
or native artifact deserialization occurs in this run.

## Actual results and cost

The saved stdout contains exactly these nine ordered PASS markers, followed by
`EVIDENCE_CATALOG_COMPLETE groups=9 storageOnly=true nativeAdmission=false`:

| Control group | Behavior supported by the saved test and source |
|---|---|
| bounded-reader-identity-census | Reject exponent, negative/fractional, oversized integer, duplicate-key, noncanonical-key-order and excessive JSON-depth inputs; bind exact dependency identities; reject missing/duplicate imports and duplicate inventory names. |
| synthetic-storage-lifecycle | Reserve then commit synthetic basis/extension storage, obtain the exact 583 bindings/two-module plan, retain bindings across reopen, refuse uncommitted roots, spent grants and overwrites. |
| dependency-profile-refusals | Refuse wrong dependency identity, evidence profile, uncommitted root and changed profile on reopen. |
| fresh-grants-interruption | Refuse altered/expired grants; reopening changes RESERVED to INTERRUPTED without reviving grants, admitting staging bytes or deleting them. |
| artifact-digest-before-restore | Same-length artifact corruption between owner sessions is refused before returning a native restore plan. |
| output-census-retained-quota | Refuse extra artifact-directory output; preserve and charge abandoned staging so a later reservation exceeds capacity. |
| withdrawal-refusal | A withdrawal marker blocks live commit/context and later reopen. |
| commit-fault-before | Injected failure before real SQLite COMMIT closes the owner; reopen resolves no committed root and INTERRUPTED operation. |
| commit-fault-after | Injected failure after real SQLite COMMIT also closes the owner; reopen resolves the actual committed root and COMMITTED operation, without reviving the old grant. |

Child exit is 0, status `COMMAND_EXITED_ZERO_AND_CLOSED`; direct child reaped,
final active processes 0, Job closed, cleanup errors empty. Stdout is 513 bytes;
stderr is empty. Reported Job CPU is 0.859375 seconds and outer wrapper CPU is
0.046875 seconds: **0.90625 known CPU seconds**. Outer wall time is
1.2236159001477063 seconds; peak Job private commit is 17,104,896 bytes.
Selected limits were 30 CPU seconds, 60 wall seconds, 256 MiB, two processes and
1 MiB each stdout/stderr. The report explicitly labels sampled total-CPU/log
limits and non-hermetic runtime pins; it is not a hard-disk bound or hermetic
toolchain proof. This small storage run is not a whole-workflow performance result.

## Source-boundary judgment

`ordinary_evidence.strict_json` performs byte/depth/integer-token preflight before
general JSON decoding, rejects duplicate keys and requires exact canonical raw
bytes. `read_evidence` derives identity from those same immutable bytes and checks
the declared import census against syntactically referenced external names.
The Python census does not typecheck, prove export existence, or replace Lean's
subsequent decode/re-encode/generated-inventory checks. Its documented inclusion
of all serialized nodes is conservative until that native canonicality gate.

The catalog binds a fixed basis/profile, immutable evidence bytes, exact imported
symbol identities, ordered batch identity and no-shadowing output names before
reservation. It uses a Windows owner lock and SQLite DELETE/FULL, bounded state,
ordinary paths and fresh process-local grants. Failed/interrupted reservations
remain charged. Commit hashes/fsyncs the one allowed output and atomically records
the root with the operation's COMMITTED state. Uncertain commit acknowledgement
forces reopen/resolution instead of blindly replaying the worker.

The selected source consistently maintains these limits:

- Profile/support hashes identify assertions; they do not prove those assertions.
  Authentic fixed inputs, support lineage, the actual native result, request /
  parent / module / output binding, and clean worker supervision remain controller
  obligations. Arbitrary peer `.olean` files must never enter this seam.
- Artifact hash checking is cached for one owner lifetime. Its sound use assumes
  protected immutable owner/OS storage; same-owner malicious mutation, host
  compromise and whole-store rollback are excluded. The corruption test covers
  a fresh owner session, not an adversary racing a live cached import.
- The catalog's close operation does not kill workers. The outer controller must
  settle its Job before abandon/close/release of worker authority.
- Context reconstruction authenticates and loads the selected chain. This is
  durable local proof-replay avoidance, not constant-cost cold onboarding,
  selected-proof-value-byte avoidance, or arbitrary DAG merge support.
- Fault injection brackets real SQLite COMMIT acknowledgement. It is useful
  recovery evidence, not an exhaustive power-loss, hardware or filesystem audit.

No new blocker was found for the selected internal storage/identity role. The
next consequential step is the already selected real fixed-basis/native-method
controller integration, not another run of these unchanged storage controls.

## Evidence identity

All four saved source files equal their selected hashes; the current corresponding
files also matched at audit time:

| Selected path | SHA-256 |
|---|---|
| `tools/Run-V5-Check.py` | `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651` |
| `software/v5/ordinary_lean/ordinary_evidence.py` | `fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6` |
| `software/v5/ordinary_lean/local_catalog.py` | `860a9d731290b2a7fbacd4852bb68185516329ee42845648f4ba3c3856d7c751` |
| `software/v5/ordinary_lean/evidence_catalog_checks.py` | `d9d77fefdad4f4c57a5cb5bbfbdd551aa1dd835f603d7223684e1ca374a08ff8` |

Run-relative evidence SHA-256:

- `selection.json`: `7ff370024afc7d42b6b0f9b38c7da03e9bf9ca22787f30c5842d2411f3e25a79`
  (equals the terminal report's selection binding).
- `RESULT.json`: `0d7a8488938c2bbf1eb324870ff783f6f2d796fee80130ad5b0344c4fc9c8a63`.
- `command/stdout.txt`: `10f2e7b4a10c2c5d7a4de80d08adb3fe37c35bea397ecc8f44bc47da2e2b4a2d`.
- `command/stderr.txt`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

The complete selected runtime pin set is the Python executable and its two named
DLLs in `selection.json`; no broader dependency attestation is inferred.
