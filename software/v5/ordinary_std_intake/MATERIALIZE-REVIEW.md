# Retained Std materialization: independent source and allocation review

2026-10-26. `current_acceptance_challenge`.

**SOURCE_CLEAR_FOR_ROOT_SELECTION.** No materialization or product command was
run by this reviewer. Root must inspect the newly generated exact selection
before launching it once. This is missing inert-file preparation, not repeated
native export, mathematical acceptance or recovery of the failed producer.

| Reviewed source | Bytes | SHA-256 |
|---|---:|---|
| `materialize.py` | 9,676 | `450b6d41cb98277eb9f0923991699d1596739e6287ee5b96a345c1b68d809f92` |
| `select_materialize.py` | 5,843 | `28d5632346c1df0ae9a43b32fab214a7814b59d5be3c68300a428692bf6715a7` |
| `MATERIALIZE-PLAN.md` | 7,238 | `743cf29d5bdd9d8cb52de4d44ca1d0cfab4a007aa2aebfd6a2496f918b879695` |

Read the complete contract, three sources above and frozen saved-writer helper.
The earlier binder/source-equivalence/31-control review is reused rather than
repeated. Independently rehashed all ten inherited external inputs and the
unchanged runner/helper/binder; they match the prior adopted selection
`412dd6bf0220eb98b03e1746295f840a5eda47a0af42b98bf299f5daa8578299`.
The saved manifest still hashes to
`1de776b3d131c8c1be3414ed0e0cf066ebd05caebbcd1cf1b6ca80853962e59c`.

## Reuse without invoking the old experiment

The materializer loads the exact frozen helper bytes into a module whose name
is not `__main__`. Thus the old diagnostic's main is not invoked. It reuses
only the helper's pinned reads, module loading, hashes and partial census.
The helper's SOURCE_ROOT derives from its own snapshotted path, so its selected
binder resolves within the same runner snapshot. Its four frozen support modules
and three saved writer inputs retain their explicit canonical paths and pins.
The materializer resets the helper's timer origins to its own start, preserving
one cumulative allowance rather than starting a second budget.

There is one call to the unchanged adopted binder. Its returned raw manifest
must be byte-identical to the saved adopted manifest. Strict pairwise iteration
reconciles each unit's ID, canonical relative filename, length and hash with
returned bytes; duplicate IDs fail. The exact three batch counts/byte sums and
2,651-unit / 44,912,843-byte totals are required. The 708 old partials are checked
before binding, compared byte-for-byte to the new units, and checked again after
writing. No old file is modified. This reuses the prior recorded aggregate
identity, not a new claim that the 708 files constitute a complete bundle.

## Output and completion boundary

Only a fresh `materialized` child of the selected run is created. The immediate
parent must already resolve exactly under the canonical experiments tree;
exclusive directory/file creation refuses existing targets. Unit IDs must be
64 lowercase hex characters and relative paths exactly `units/<ID>.json`.
Each write verifies its input hash, flushes/fsyncs, then rereads exact bytes.

A complete pre-manifest census requires exactly 2,651 ordinary unit files and
44,912,843 unit bytes, with no unexpected root entry. The bounded
`MATERIALIZATION.json` is written next, explicitly marked prepared rather than
complete. The unchanged saved manifest is written last. A final census checks
all 2,653 files and their pins, including report and manifest; no further required
file is written afterward.

The final manifest write is not claimed atomic or sufficient for success.
An interrupted or late-refused run may retain a manifest or partial files.
Only the successful terminal stdout **and** independently checked outer
exit-zero/clean-closure result establish materialization completion. This
distinction prevents a partial artifact from being silently used as intake input.
Source/runtime checks by the outer runner and the materializer's final helper,
manifest and input rechecks remain required. Owner-controlled immutable inputs
are a premise; this is not protection against arbitrary concurrent local attacks.

## Selector and finite cost

The selector imports no product and invokes no materializer. It reads the exact
adopted predecessor selection, preserves its ten external pins, and adds the
saved manifest plus predecessor-selection file: twelve external pins total.
The six snapshots are runner, materializer, selector, plan, frozen helper and
adopted binder. Its source and external inputs are rehashed before exclusive
selection creation and readback. The fixed argv uses the selected Python with
`-I -S -B`, the snapshotted materializer and fresh output placeholder. It creates
no run directory or source/output copy itself. Its own checks are cooperatively
bounded to 60 wall / 30 CPU seconds.

The proposed operation retains **90 wall / 70 process CPU seconds** internally
and **120 wall / 90 inclusive CPU seconds / 1,792 MiB / one active process**
externally, with 262,144-byte stdout and 131,072-byte stderr caps. The saved
binder's 28.125 CPU seconds and old diagnostic's 31.3125 known CPU seconds
justify a bounded attempt, not a promised completion. All 2,651 new writes,
fsyncs, rereads and censuses are charged within that unchanged allowance.
Slow storage may still cause refusal. No renewed old allowance or cap increase
is hidden here. Report outer inclusive Job CPU plus separate wrapper CPU;
do not add binder CPU again. There is no hard disk quota or hostile-code sandbox.

## Result boundary

A pass could establish only the exact complete inert bundle and its measured
production cost. It cannot establish that the three batches are accepted by a
fresh recipient, that rich-library circulation fits all public limits, or that
knowledge grows faster. The source/cost screen and any actual initialization or
intake remain separate root decisions. Preserve all old failures and new partial
output; no retry, native re-export, new binder test campaign or cap change follows
automatically from this review.
