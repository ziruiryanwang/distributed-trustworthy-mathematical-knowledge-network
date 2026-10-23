# Portable authoring wrappers: saved build outcomes

2026-10-23. Reviewer: `admission_event_audit`. Read-only inspection of retained
build01 and separately selected build02. No compilation, test/native execution,
source change or Git operation was performed by this review.

## Disposition

**Build01 remains FAILED. Build02 passes the selected two-wrapper compilation
scope.** This establishes neither actual owner use nor mathematical admission.
No prerequisite rebuild was selected: the actual driver invokes Lean once for
each of the two new wrapper modules and uses the retained compiled helpers on
its explicit import path. Existing helper implementations are not modified.

| Evidence | SHA-256 |
|---|---|
| Build01 selection | `b5b6d9e48165cb6a890ce98a8d94209223bdd0d8bbb1e0c022c67a637e8be7d3` |
| Build01 outer result | `9dba7cc20887b4f83fb8c855ab441c33640a25deff43b946349fc5f5037a84a7` |
| Build02 selection | `cc0e77dd3205ba1886c30fadd848ce89ddea8e4d22f29d3d9649d82c6e1c0b24` |
| Build02 outer result | `8cacf5f0dbcb0ef8b787652734bd723374aef65a280a71507a7d91ae6afae8ed` |
| Build02 compile result | `22e7909e2f5c41a747dcb42fba0b187ae5871da639e3fdaf899a8f7ec20e1b85` |

## Preserved failed first allocation

The first saved controller traceback reports `subprocess.TimeoutExpired` for
`PortableOwnerConstructCommand` after its fixed 45-second module timeout. Both
native stdout/stderr files are empty. The outer controller exited 1, but its
direct child was reaped, Job closed, cleanup error list empty and final active
process count zero. The snapshot matches its source selection. No successful
module completion or authoring capability is inferred from that attempt.

Its actual wall cost was **50.9296814 s**, with **2.859375 s Job CPU** and
**0.90625 s wrapper CPU**: **3.765625 s known accounted CPU**. Empty native logs
and the observed timeout do not identify why the first call took that long.
No stronger diagnosis, retroactive budget renewal or relabeling follows.

## Fresh successful second allocation

Root selected the new `run_deadline_compile.py` source
`e8af76392fb20afe122ba78f304a46063de35b8ea60632ee2d52ffe97f508004`, with one
120-second total internal deadline rather than a renewed per-module allowance.
The unchanged wrapper selections are `PortableOwnerConstructCommand`
`250a8dd1292c1dd5d228d69eaeb7abdbb5f0e9ad96c48a8b32d80203c27619b2` and
`PortableConstructExportCommand`
`8251bc13836fde6620203752b9378bfafccefeef16587788221dec7ad7e95a8b`.
All four retained build02 source files match the selection hashes.

The actual compile result contains exactly two zero-exit steps, targeting those
two new modules under build02's fresh output. Their four native log files are
empty. The generated output contains exactly ten nonempty compiler files (five
per module: object/private/server/IR/signature), totaling **1,151,432 bytes**.
The principal objects independently hash to:

- `PortableOwnerConstructCommand.olean` (194,272 bytes):
  `1a29930ebbefd48da689037d0bcc3acf6a719a999948e96edf8e0bef0f7b76fa`.
- `PortableConstructExportCommand.olean` (116,936 bytes):
  `89e9433415808d17cc2c308b9b65a0a1ecdbd4a26a5bafba9d8eccb433c2f078`.

The outer result is exit zero with a reaped child, closed Job, no requested
termination or cleanup errors, and zero final active/terminated processes.
Outer stderr is empty. Its whole-operation wall cost was **9.3602258 s**;
**3.34375 s Job CPU** plus **0.640625 s wrapper CPU** gives **3.984375 s known
accounted CPU**. Peak Job private commit was 878,964,736 bytes, within the selected
1536 MiB envelope. The earlier failed cost remains separately preserved.

The next worthwhile check is actual portable construction/export through the
installed contribute/reuse workflow, not another wrapper compilation or recheck
of the accepted library. Compilation is supporting evidence, not that workflow.
