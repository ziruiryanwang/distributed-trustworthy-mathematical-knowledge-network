# Cache and restorable extraction review

2026-10-24. Read-only cleanup investigation by current_security_obstruction.
Canonical guard passed. No deletion, move, archive extraction, script launch,
database open, compiler, test, native process, Git action or duplicate size scan
was performed. This note is the only file written for this assignment. Root owns
exact current-byte validation, live-use checks and any separately recorded prune.

## Recommendation

Prioritize the two archive-backed historical software extractions below. Do not
start pruning Rust targets or registry trees: this project explicitly promotes
some generated intermediates into pinned later build/runtime inputs, and the
likely payoff of careful per-file discrimination is lower than removing exact
restorable extraction copies. Preserve every archive, current runtime, current
v4-library supervisor and all actual mathematical/operational state.

| Exact candidate for root validation | Retained originals outside candidate | Existing payload evidence |
|---|---|---|
| `E:\Distributed Trustworthy Mathematical Knowledge Network\product-local\certified-v3-package-01\app` | Both sibling `mathematical-commons-v3-*.zip`, `BASE-FILES.json`, `CONTRIBUTOR-FILES.json`, `RESULT.json`, selection/audit sources | 13,004 software files; 2,444,576,373 payload bytes from adopted component totals |
| `E:\Distributed Trustworthy Mathematical Knowledge Network\product-local\certified-v4-package-01\app` | Both sibling `mathematical-commons-v4-*.zip`, `BASE-FILES.json`, `CONTRIBUTOR-FILES.json`, `RESULT.json`, selection/audit sources | 13,004 software files; 2,444,835,804 payload bytes from adopted component totals |

Combined historical payload is4,889,412,177bytes (about4.55GiB), not a new size
measurement or a claim about physical disk blocks. Root's separate current scan
supplies current size information. Neither candidate is approved for deletion by
this note alone.

## Evidence for the candidate boundary

The completed v3 package plan describes exactly `app/receiver`, `app/peer` and
`app/contributor`, reconstructed from two ZIPs with portable per-member hashes.
It explicitly excludes experiments, private configuration, keys, SQLite state,
proof checkpoints, bytecode, user source and caches. The completed packager checks
the exact file/directory census with no extras.

- `experiments/certified-v3-package-01/PLAN.md`: fixed output/privacy boundary,
  strict archive validation, streamed extraction and final byte maps.
- `experiments/certified-v3-package-01/OUTCOME-AUDIT.md`: completed actual
  exact-file PASS,13,004 member agreement and independently bound archive hashes.
  V3 base ZIP SHA256
  `e985b03c2abef3d9a74a6b6ef3d36a690046824c27d0c6e09acd7780037428df`;
  contributor ZIP
  `fba95cb4bfb74c2c9286f91cc6cff27dbf542b407c6dfacc10b7a7f218cea7c4`.
- `experiments/certified-v4-package-01/PLAN.md`: same pure-software output
  boundary; excludes state, credentials, proof checkpoints and caches.
- `experiments/certified-v4-package-01/OUTCOME-REVIEW.md`: completed actual
  exact-file PASS,608base/12,396contributor members and no extracted extras.
  V4 base ZIP SHA256
  `773edc7f05ce3c6d3f5224801327c276cfbdd6a1b3c4d36f2197a3d49f238399`;
  contributor ZIP
  `6160546271798a695fd8e823b73fe68426079f1e0a0af40152c5fa84346bf4ed`.

These are historical evidence pins, not claims that this agent rehashed the
multi-gigabyte archives now. Root is checking current archive/member equivalence.
The v3 payload arithmetic is97,267,089receiver +245,865peer +2,347,063,419contributor.
The v4 arithmetic is97,711,559base +2,347,124,245contributor.

## Reference investigation and operational consequence

Direct text-reference searches for both package names in `software/`, `tools/`
and `deliverables/` found references only in historical v3/v4 handoff documents
within those inspected source trees. Searches in the inspected v5 cycles
(2026-10-07,2026-10-12,2026-10-17 and2026-10-22-native-library) did not identify
either candidate as a current runtime input. The v5 discovery contract instead
names `product-local/v4-library-package-01/extracted/commons-v4`, which is not a
candidate and must remain.

This is a bounded reference search, not proof that no arbitrary external script,
saved experiment selection or active process could refer to an old app path.
Root must confirm current selected/live uses before pruning. Existing operation
state must never be included merely because it is adjacent to a package.

The historical v4 `LAYERED-GUIDE.md` directly links/calls the candidate receiver,
contributor and peer API paths. Pruning therefore makes these convenience links
and historical executable examples unavailable until restoration. Retaining the
archives preserves the actual software bytes; it does not preserve immediate
availability of every old extraction. Record that change in a new cleanup ledger,
not by rewriting frozen handoff or outcome evidence.

## Restoration semantics

For either candidate, exact restoration means validating both preserved archive
pins and manifests, then materializing the exact allowlisted `app/...` member
bytes at the original absolute paths. Require ordinary nonredirected paths,
single-link files, no conflicting existing files, no extras and correct final
length/SHA256 maps. Do not substitute symlinks/junctions or hardlink an old
installation to make a deleted path appear present. Reapply appropriate protected
owner permissions; file hashes alone do not establish OS access protection.

The old packer is not a restoration tool to rerun: it has a consumed fresh
destination, expired absolute deadline and historical single-run selection.
A later restore needs a separately bounded extraction-only action; it must not
rebuild, invoke native/proof workers, restart old allocations or alter recorded
outcomes. No such action is created or launched by this review.

Restoring identical software bytes restores a software input, not mathematical
acceptance, process state, a live Job, a credential or permission to replay an
old experiment. These app trees were deliberately packaged without those forms
of state. Keep external state/receipts/intents and their source paths unchanged.

## Concrete exclusions from generic cache cleanup

1. **Retained Rust libraries are not disposable merely because they live under
   `target`.** `research/cycles/v5-2026-10-12/Select-BoundedParseDirect01.ps1`
   explicitly selects238files/320,499,420bytes from
   `experiments/v5-local-checks/aggregate-guest-compile-01/target/`:
   108`.rlib`/`.rmeta` pairs from `riscv32im-risc0-zkvm-elf/release/deps` and22
   proc-macro DLLs from `release/deps`. Preserve both directories until every
   adopted retained-artifact input map has been considered. Do not run Cargo clean.
2. **The host link closure also uses retained target outputs.**
   `research/cycles/v5-2026-10-12/AGGREGATE-PRODUCTION-SEAM.md` records a1071file,
   2,320,491,997byte selected subset of old runtime/link directories, including
   `.rlib`, `.rmeta`, `.dll`, `.lib` and `.a`. It excludes `.d`, `.pdb` and some
   unreferenced generated objects for that particular direct command, but that
   exclusion does not prove those files are absent from every other selected
   build or historical output map. Root's later instruction deprioritizes this
   small/uncertain-payoff trimming; no debug/object deletion candidate is adopted.
3. **Cargo archive and extracted-source caches are different inputs.**
   `BOUNDED-PARSE-GUEST-FAILURE.md` documents an actual offline resolver failure
   after a selector retained compiled-unit packages but omitted resolver-only
   archives. The repaired180archive/379file cache is explicitly selected. Preserve
   registry caches and sparse indexes under the named general-checker and
   aggregate/bounded-parse operations. Extraction existence alone is insufficient.
4. **Provisioning archives and assembled runtimes stay.** Historical
   `scale-crypto-01/runs/run-01/archives`, its assembled `rust` tree, and later
   copied registry/source trees have explicit download/extraction/adoption maps.
   They are not authorized deletion targets. The user/root now explicitly retains
   all archives, including old Lean download archives.
5. **Current Lean and old absolute runtime paths stay until separately resolved.**
   Keep `software/runtime/lean-4.34.0-windows` and the current v4-library extraction
   and supervisor. A byte-identical second Lean extraction may still be named by
   historical or current support manifests; no runtime-path substitution or
   removal is justified here.
6. **Evidence and state are excluded categorically.** Preserve source/selection
   maps, locks, manifests, raw logs, terminal/failure reports, private credentials,
   proof/receipt/checkpoint files, all SQLite catalogs and sidecars, actual native
   artifacts and all current/frozen product sources. Ignored files are not trash.

## Root's minimum decision before removal

Resolve only the two exact `app` targets; verify they are descendants of their
named package directories and contain only the archive-backed manifest members.
Require current archive hashes, member hashes/lengths, no added state or private
files, no reparse traversal and no live/selected dependency that needs immediate
access. Preserve archives, manifests and all historical records outside `app`.
Record exactly what is pruned, recoverability through the retained ZIPs, and the
temporary unavailability of historical extraction links. If any condition fails,
retain the target and report the mismatch; do not widen cleanup into its parent.
