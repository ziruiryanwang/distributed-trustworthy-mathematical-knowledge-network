# Storage cleanup, not a new research campaign

The user requests finishing tasks at hand, temporarily pausing research,
removing genuinely redundant files, and then continuing v5. No deletion is
implied by age, ignored Git status, a failed run, or a `target` directory name.

The initial read-only inventory did not follow reparse points. It found
988,228 regular files and 97,034,927,380 logical bytes (90.371 GiB), including
54,534,914,419 bytes in product-local and 39,100,252,217 in experiments.
These are logical lengths, not allocated clusters or unique hardlink bytes.
The scan skipped the retired junction test and generated Windows cache
junctions; none is a removal target. Concurrent tiny checkpoint writes mean
the inventory is a baseline, not a transactional filesystem snapshot.

## Candidate scope

Prefer exact, archived historical extraction payloads over speculative cache
deletion. Preserve all archives, manifests, reports, source, Git history,
databases, proof results, current installations and active runtime dependencies.

Candidate trees, pending full archive-byte comparison and reference review:

- product-local/certified-v3-package-01/app
- product-local/certified-v4-package-01/app
- experiments/lean-feasibility/runtime/lean-4.34.0-windows

Their retained ZIP files are adjacent. This is archival dehydration, not erasure
of the only copy and not an assertion that historical paths never mattered.
Historical use will require re-extraction to the original path. Current work
must not depend on any removed path. Do not change sealed historical reports
to hide that a formerly present extraction has been archived.

Root's read-only verifier must check complete case-insensitive file-set equality,
safe ZIP paths, no reparse points, exact lengths and SHA-256 for every file in
both extraction and ZIP. It retains a per-file recovery map, ZIP hashes and
directory metadata. Unique or changed files fail the whole candidate; they are
not removed. Every target is an explicit strict descendant of the canonical
project root, never the workspace itself. Root separately reviews the exact
candidate and current references before removal. Removal revalidates the path,
reparse exclusions and unchanged census/metadata. No hardlink replacement,
mass renaming, Git cleanup, broad `target` deletion or external cleanup.

## At-hand work boundary

The minimal fixed-basis support build and corrected 42-group native-free
controls have returned cleanly; independent saved-output audits finish first.
The first control failure and its original source remain preserved. One attempted
controls02 runner invocation used a relative selection path and was refused at
ABSOLUTE_NONROOT_LOCAL_PATH before output creation; the corrected absolute-path
invocation ran the suite once. The larger comparison remains source-only and
unreviewed; it cannot run during cleanup.

After cleanup, record exact deleted paths, bytes and recovery procedure, commit
reviewed checkpoints explicitly, and resume the payoff-led v5 work. Do not call
the overall software goal complete.
