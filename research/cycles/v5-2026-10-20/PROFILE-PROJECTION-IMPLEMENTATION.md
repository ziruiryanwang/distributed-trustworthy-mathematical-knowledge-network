# Base projection helper: implementation checkpoint

2026-10-20, core_growth. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

Implemented only the assigned source helper and README under
`software/v5/base_projection/`. Root owns service/dispatcher integration and
launches; core_release owns focused controls; adaptive_audit owns independent
actual-source review. No imports, tests, builds, native/proof work, process
launches or Git mutations were performed by this assignment.

## Exact basis and source

- Adopted contract: `PROFILE-PROJECTION-CONTRACT.md`, SHA-256
  `25618050d4a7e70ced003856e390b87b9090b442ced6324dd544889e422b08a1`.
- Independent contract review: `PROFILE-PROJECTION-CONTRACT-REVIEW.md`, SHA-256
  `aefb89306dee305c8322d89df67ab289f80939af676a5dd5d8132bf768c68b46`.
- Scope: `PROFILE-PROJECTION-IMPLEMENTATION-SELECTION.md`.
- New helper: `software/v5/base_projection/client/base_projection.py`, SHA-256
  `804147ddb15d9c9758ab8c0b0aebaefcbeefbc98292db262e3849ab25647d2d1`.
- Public guide: `software/v5/base_projection/README.md`, SHA-256
  `a924634a965c20b91d3552e4c7185b55cd5de31d1ee95069f4252402041f9076`.

## Implemented boundary

`validate_selector`, `open_view`, `prepare`, and `main` match the agreed API.
`ProjectionView.index` is an actual existing Store, not a proxy. The source is
an exact selected Workspace class, open under its lock with no client/grants or
prior projection borrow. The original module foundation/policy agree with its
adapter. The target is the fixed ordinary `base-projection-index` subtree.

Preparation performs closed bounded preflight, opens the original workspace
once, derives the default adapter and re-extracts each selected held export.
Exact export identity is preserved; no feature record is relabelled, no packet
is copied, and no mathematical acceptance changes. A finite ordered batch stops
at its first error with explicit conservative byte charges and prefix/commit
uncertainty. Actual final latest-cut verification is required for success.

The real Store is allocated before its original initializer is called. This
retains the partial object's database if initialization or its internal cleanup
fails. Projection cleanup attempts Store.close and any necessary direct DB close;
only known closure releases its matching borrow. A cleanup error remains a failed
operation, including when fallback cleanup succeeds. Original workspace cleanup
still runs after unexpected close exceptions. Serving callers must stop/drain
transports before this close; the helper creates none.

Constructor and each admission's available counters are captured before the next
primitive can reset them. A failed admission whose work dictionary never changed
is marked unknown, not counted as the prior primitive again. Inclusive process
CPU/wall are reported separately; these samples are not a total proof-cost or
physical-I/O accounting claim. The original enclosing Job remains the hard bound.

`open_view` reopens only an exact authenticated latest snapshot, not an old cut
while handlers could answer from a new cut. Its descriptor carries selected and
source namespaces, local cut, explicit owner-selected coverage and
`mathematical_acceptance: false`. `assert_current` checks unchanged selection.
There is no implicit projection preparation during service.

## Report contract

Fixed fresh output: `base-projection-result.json`, at most 64 KiB, under the
launch context's location workspace. Invalid preflight raises before opening
source/target. Runtime failures preserve the finite input and retained state.

Principal fields are `attempted`, ordered `acknowledged`,
`last_acknowledged_snapshot`, `current_export_id`, `outcome`,
`submitted_export_bytes`, `store_work`, `initial`, final
`snapshot_id`/`local_cut`, `error`, and `cleanup`.

Outcomes distinguish:

- `ALL_ACKNOWLEDGED`: complete acknowledgments and authenticated final latest cut;
  PASS additionally requires clean target/workspace closure and saved report.
- `STOPPED_BEFORE_CURRENT_ADMIT`: no current-item admission entered; acknowledged
  prior items may still persist.
- `COMMIT_OUTCOME_UNKNOWN`: failure after current admission entry, including a
  possible returned-commit exception; the actual latest is not inferred.
- `ALL_ACKNOWLEDGED_CUT_UNCONFIRMED`: all acknowledgments returned but final latest
  verification failed/timed out; final snapshot/cut fields remain null.

A missing valid terminal report means unknown batch outcome. Reconciliation is
a separate explicit create=False invocation, not a retry, repair, reset or
conversion of prior failure into success. Broken partial state is retained.

## Review and remaining evidence

Root and independent reviewer read the draft helper. Root requested conservative
pre-reset work accounting and a broad close-exception guard; both are included.
Reviewer reported no blocking defect in partial construction, borrow/cleanup,
source/config binding or expected-latest handling. Its optional clearer final-cut
outcome is also included. Final source review and focused control execution are
separate and were not assumed complete by this checkpoint.

No full scan, multi-index router, catalogue, profile negotiation, proof campaign,
automatic catch-up, new durable ledger or changed mathematical authority was
added. This resolves a concrete cross-profile discovery seam in source, not the
whole v5 release or a claim of globally complete search/useful growth.
