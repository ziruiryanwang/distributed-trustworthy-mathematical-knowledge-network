# Independent package01 selection review

Disposition: **PASS_EXACT_FILE_ONLY_SELECTION; NOT EXECUTED**.

Reviewed `experiments/v5-local-checks/kernel-admission-package01.selection.json`,
SHA-256 `22dcd0ad2bc0901f53f52fae311b3b9ed382aa6a6842b88da918df099c7fbec2`.
All four source pins and 191 external pins match current actual bytes. The four
sources are the existing bounded runner, corrected assembler, unchanged installer
and unchanged file helper; no extra controller, native source or selector enters
the snapshot. The prior source audit remains valid and was not repeated.

The external map contains exactly the 181 required files: 154 predecessor package
files, its ASSEMBLY receipt, the adopted native BUILD map, sixteen native
source/object files and nine runtime files. Their keys and hashes agree with the
actual adopted manifests. Ten additional pins bind the package contract/plan/
review, build adoption, control adoption/outcome and four saved control evidence
files. The control adoption refers to all sixteen passing controls and clean
closure; this selects file integration, not protected-state or Std acceptance.

The argv uses the selected Python with `-I -S -B`, the immutable snapshot's
corrected assembler, and `{output}/distribution`. This matches the adapter's
required `kernel-admission-package01` snapshot/output relationship. No native
executable, owner command, database path or shell interpolation occurs in argv.
The fresh run/output directory does not exist at review time.

The selected outer bounds are 120 wall seconds, 60 inclusive Job CPU seconds,
512 MiB, one process and 1 MiB per stream. They agree with the source plan; the
adapter retains its 90-wall/45-controller-CPU checks and passes its original
absolute deadline to the installer. Existing supervisor source remains pinned.
Runtime pins remain the explicitly named, nonhermetic cooperative trust boundary.

Root may select the one file-only execution. Preserve partial output on failure;
no automatic retry or allowance renewal is implied. Actual adoption still needs
independent confirmation of all 154 files, nine changes/145 unchanged, the expected
support-field and implementation-identity delta, unchanged inputs and clean outer
closure. No package execution, product import, native call, owner/database access
or Git mutation occurred during this review.
