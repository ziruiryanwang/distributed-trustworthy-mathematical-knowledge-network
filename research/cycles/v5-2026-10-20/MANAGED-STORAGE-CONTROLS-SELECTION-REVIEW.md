# Managed storage controls: independent selection review

2026-10-22. Reviewer: storage_launch_review. **PASS_SOURCE_SELECTION_ONLY**
for the exact two controls below. No launch blocker found. This does not report
executed controls, adopt the storage envelope or qualify managed integration.
Root owns the finite runtime decision, preparation, launch and actual audit.

## Reviewed identities

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `Select-ManagedStorageControls01.ps1` |5860|`aea004e0e063efbf0ff55d9faad808dbac4a2f3262d3c0b5d991845177d9d053`|
| `software/v5/managed_storage/python_controls.py` |30042|`cda358d759fe0808ea4546601ed343ce764cd0bb222a64f21a7115baf99414c9`|
| `software/v5/managed_storage/node_controls.mjs` |16756|`8996b2e03a34e5085ea620a140a79e12847abcaa899083f94d02a883cf440491`|
| `tools/Run-V5-Check.py` |5735|`44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651`|

Read both complete authored controls, source notes, selector and runner; inspected
the retained supervisor's environment, command and containment paths. Authored
notes read: Python `5aca8a9b8e744b36101fb6038714a4da1dedaa1666bc567f7eb00d90741f4888`;
Node `2c012d6ac0f9152127d4e1f7a72cdd6051a32515ceb1551c8e9036917c90a6ab`.
No prior product review was reopened. All inspections were read-only; the only
new file is this review. No selector, test, product import, parser, build, SQLite
connection, service or Git mutation was executed.

## Findings

- **Fresh fixed paths:** selector requires the exact canonical working directory.
  Each kind has its own fixed `managed-storage-{python,node}-controls-01` output
  and adjacent `-selection.json` below `experiments/v5-local-checks`. All four
  paths were absent at review. Selection creation uses `CreateNew`; the runner
  independently requires a fresh ordinary output and exclusively creates its
  snapshot and copied selection. No prior operation or private credential path
  is targeted. No automatic retry is present.
- **Source binding:** Python is exactly 12 snapshot entries (runner, test and ten
  dependencies); Node is exactly five (runner, test, intent, maintained roles,
  protocol). All thirteen fixed dependency rows were independently hashed and
  match current files. The protocol alias and original are both 13533 bytes,
  SHA `88c2bc34e5ebefc412b564bef06e0d4210e0c44e3102be1d6adacfc6334af986`;
  it is needed only for the real relative import in this test snapshot, not a
  new SDK/product entry. `TestSha256` is intentionally an owner-supplied argument:
  this review approves only the exact corresponding test hash in the table.
- **Runtime binding:** the basis selection is exactly
  `c3257f270ca3b45bfa5a5c7f88798112dac49d9aaea378913ec1df9f98e3b3f6`.
  Excluding only its old build input leaves 28 rows, totaling 39150032 bytes;
  all match their hashes, and the Python executable is one of them. Node adds
  exactly the selected observed-01 base executable, manifest and quota store,
  producing 31 rows. Their hashes match `b3094d0b`, `a93714ec`, `7c6cbeea`
  respectively, including the full selector pins. The original supervisor,
  domains and Job helper also match their manifest rows. This is not a full
  toolchain/5896-file sweep or a new hermetic-runtime claim.
- **Argument compatibility:** Python runs the snapshot script with isolated
  `-I -S -B` and only `--output {output}`; its fixed output and snapshot checks
  agree with the selector/runner. Node runs the selected absolute executable
  with no flags, the snapshot script and the same sole option. The supervisor
  removes `NODE*`, `PYTHON*` and other language-path injection variables before
  launch, satisfying the Node controls' explicit environment refusals.
- **Imports:** Python executes the three authenticated helpers and extracts only
  the exact `ordinary` AST, with empty SDK package paths; the other seven-store
  and allocation checks are static, not full manager imports. Node imports the
  actual intent/QuotaDatastore/Key chain, authenticating selected source or
  manifest-listed overlay code and present enclosing package metadata on
  resolution/load and afterward. Maintained roles are read, not imported. The
  hooks reject other schemes, paths, formats and nonselected builtins. This
  retains the trusted-owner/exclusive-writer premises, not an adversarial local
  filesystem sandbox.
- **Finite envelope:** each independent run selects 10 child Job CPU seconds,
  45 wall seconds, 128 MiB, one active process and 1 MiB per log. The unchanged
  runner snapshots authenticated inputs, supplies canonical cwd, supervises a
  suspended-then-attached child and checks closure and bindings afterward.
  Wrapper CPU is separate; wall/log checks are sampled and postflight wrapper
  work is not a hard child-Job limit. The controls spawn no subprocess, network
  service, proof job or private-key generator. They retain small synthetic
  fixtures; the 1 MiB final fixture census is not a hard physical peak quota.
  These small fixed operations plausibly fit the selected finite allocation;
  this review does not predict success or authorize extending it after failure.

## Required interpretation after execution

Read the actual structured control result, raw errors, final source/runtime
bindings and outer Job closure; an exit code alone is insufficient. Python
requires seven completed groups without failures, errors or skips; Node requires
seven groups, no close/binding errors and retained refusal fixtures. Preserve
any partial outputs or failure under the original allocation. Do not relabel
static order checks as executed lifecycle, a metadata refusal as hot-journal
recovery, or these controls as physical-disk, whole-SDK, mathematical or final-v5
qualification. The selected fresh installed integration remains a separate gate.
