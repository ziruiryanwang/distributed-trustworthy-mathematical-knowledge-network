# Context-native discriminator: pre-execution review

## Decision and scope

**PASS — bounded source and exact-launch review. No unresolved pre-execution blocker was found in this reviewed cut.** This is permission to interpret the planned single launch as the specified engineering experiment, not evidence that it has run successfully. No Python or Lean execution, import, compilation, SQL query, service, or launch was performed by this reviewer.

The review covered the complete paired coordinator and worker, the discriminator specification, the unchanged enclosing supervisor, and relevant installed product interfaces. It included independent fieldwise checks of the exact launch's pins, ordered product inventory, paths, and fixed bounds. The coordinator's final accounting-order repair was reviewed after the initial complete reading. Both fresh run roots remained absent at the final pin check:

- `product-local/context-native-01`
- `software/qualification/context-native-01`

## Reviewed cut

SHA-256 values below bind this decision; edits to these inputs require review of the changed cut.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `software/tests/run_context_native.py` | 15182 | `5bdfd992ad1b6637654d3418247b5263c82b2ffd89840ada30860475d26cc49a` |
| `software/tests/context_native_worker.py` | 23105 | `13f12cdcc46f39ce86b5260b3fe370b5d9402d755f66d846aa9751319340bd00` |
| `software/drafts/CONTEXT-NATIVE-DISCRIMINATOR.md` | 11344 | `a3a7b9eeda204c772845ea4468f275579b96feaa8cce4a92d37b07b502788aa5` |
| `software/qualification/context-native-launch-01.json` | 40390 | `bbfd0a649e04863600f6e9d13e96add156782dc3792ed49fe77bb3ae1960b374` |

The exact six ordered launch pins were checked against actual files, including both scripts above and these four inputs:

| Input | Bytes | SHA-256 |
|---|---:|---|
| `D:\Python314\python.exe` | 106208 | `03168c01b7b7491423350e82c26fee71f35b43694d1319d3c668bda6903a0c38` |
| `software/py/run_stage.py` | 26505 | `3c84f507dbb788827dbd50de2d0d7552e4f72bd615f425cfd5f1da278ac5a5be` |
| `software/py/supervise.py` | 18611 | `e5f35c0a88602757ecb7ff899f923f940b588e11e2a7c9c36d51fdbb2dfcac1b` |
| `software/runtime/lean-4.34.0-windows/bin/lean.exe` | 83456 | `a8040e2cab341c12116ab591fed9f761816f5f6b08554f6cc1680e86dfbba0a2` |

The launch itself becomes the seventh enclosing supervisor pin. Its product inventory exactly matches **98 files / 3,434,468 bytes**, independently enumerated using ordinal ordering of POSIX relative paths. Every path, length, hash, and row field set matched. The inventory includes the four specified root files, direct `py/*.py`, and recursive regular `native/` and `assets/` files. Coordinator checks reject reparse-point ancestry before resolving source paths.

The reviewed enclosing limits are 450 wall seconds, 450 CPU seconds, 6144 MiB memory, 8 active processes, and 65,536 bytes each for stdout, stderr, and the event. Retained endpoint limits are 1,073,741,824 bytes, 16,384 files, and 32,768 entries. These are not a promise of a hard transient disk quota or a 450-second bound on total coordinator elapsed time.

## Essential evidence properties

The fixed sequence uses 14 installed public CLIs: support build, configure, bootstrap, X submit/publish, Y submit/publish, Y admission, X cap refusal, selection of C0, X admission into C0, Z submission into CX, and exact selection/refusal replays. There are no peers, sockets, sender process, live author pause, automatic retries, or source repair.

The acceptance checks distinguish a package-cap failure in CY from subsequent successful admission of the same original KX into C0. Selection changes the actual head without a native check. Its exact replay returns the historical C0 response without moving the actual head back from CX. Exact refusal replay also performs no new work. The expected endpoint is 10 ordinary requests, 6 receiver stages, and no active request.

The worker uses only installed normal CLIs to mutate the node. Its own SQLite observations are read-only, query-only, bounded snapshots after public-worker quiescence. Replay requires the complete snapshot to remain unchanged, exact historical response bytes, and no checker/stage allocation. The refusal/selection expected-state comparisons allow only their specified request/attempt/accounting changes; selection alone changes the head. Final preservation compares old request and stage rows as well as old records, entries, providers, snapshots, and pre-selection work-file hashes. The database is not incorrectly included in an immutable-file claim.

Each ordinary call binds its exact 11 ordered pins, five output files and hashes, complete command profile, original event directory, and request/reply bytes. The cap refusal explicitly requires checker loaded but zero stage allocations and zero pipeline children. Each of the six final stage rows binds the request key/client, purpose, index, directory, and grant; its receipt and stored plan bind the corresponding request/stage directories, domains, plan hash/pin, and child count.

The X/Y/Z fixture texts agree between worker and specification. For X, the received description must contain one row with `kind == "definition"` and `u == 1`, exactly matching the original checked submission's row. `definition` is the native interface's correct spelling. Z substitutes only the received bounded canonical-name string into the fixed nested-composition fixture. This source-level linkage and name-pattern test do **not** establish canonical declaration identity, branch separation, or reachable substantive use; the separate post-run dependency audit must establish those from the retained native evidence.

## Accounting and containment

Expected reservation charges are 10 × 8 MiB for ordinary requests plus 6 × 128 MiB for receiver native stages: **848 MiB / 889,192,448 bytes**. Receiver native children total 18: bootstrap 1, three submissions at 5 each, and two admissions at 1 each. The support build is separately one stage with two children. Existing installed build logic checks its plans, output/source pins, both child outcomes, and quiescence; the worker additionally checks the build's status, two-step structure, and inactive endpoint. The worker is not claimed to duplicate every build validation.

One unchanged enclosing Windows Job supervisor contains the worker and inherited descendants. It creates the Job before assigning/resuming the suspended root child, does not enable breakaway, observes resource limits, verifies event hashes, reaps the direct child, checks zero active processes, and checks handle closure. Ordinary receipts separately require complete transport, zero return, reaping, Job closure, and no cleanup error. No per-wrapper timeout is misrepresented as descendant cleanup.

Nested CPU measurements must not be added again to enclosing Job CPU. Coordinator CPU is reported separately through final report preparation; unavailable observations remain unknown, not zero. The reviewed coordinator repair assigns actual CPU and cleanup observations before serializing/saving the optional observation copy, preserving those available observations even if that persistence step fails. Endpoint census is permitted only after verified enclosing quiescence or before any invocation; final records have reserved capacity and are not self-hashed.

Containment relies on the reviewed Windows/runtime profile; this is not a proof against hostile local administrators or runtime compromise. Executable pins are not an attestation of all runtime libraries.

## Corrections and remaining outcome obligations

Static-review findings were repaired before this launch cut: incomplete ordinary receipt binding; missing explicit zero-native refusal assertions; incomplete historical row preservation; incomplete stage/request/plan binding; X description-row binding; and the coordinator's cost/cleanup assignment order. They are review corrections, not alleged runtime failures.

The planned strongest worker verdict is deliberately `PASS_PENDING_DEPENDENCY_AUDIT`. After the single launch, an independent operational audit must check actual outcomes, retained grants/receipts, resource and cleanup observations, immutable evidence, replay behavior, and expected counts. A separate canonical dependency audit must check branch separation and Z's actual reachable nested use of X. Missing or failed evidence must narrow or reject the corresponding claim rather than trigger an unreviewed retry.

Even a fully passing outcome would establish only this fixed local engineering regression. It would not establish autonomous mathematical discovery, useful knowledge growth, semantic independence, distributed-network qualification, sustainable capacity, or general recovery correctness.
