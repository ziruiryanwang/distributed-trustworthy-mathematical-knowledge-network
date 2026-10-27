# Frontier auxiliary package: independent actual audit

2026-10-26. **PASS for exact file assembly and clean closure.** No package
execution, mathematical acceptance, state migration or product adoption is
established. Root owns adoption. This review used only saved file/hash reads;
no assembler rerun, product import, owner/database operation or Git mutation.

Run: `experiments/v5-local-checks/demand-frontier-package01`.
Package: that run's `distribution/package` directory.

| Evidence | SHA-256 |
|---|---|
| selection.json | `16580fe3a9f401354c1089d75ab2175bec7918812f6973cd2fda47d18c22f9a8` |
| RESULT.json | `34a37b8f3d759a13c3132760959598e983362417c4b8c084f5bb291e0e6c57fd` |
| distribution/ASSEMBLY.json | `6ada680868401735ea4abd2fb04b43c064b67d78da7eb46db1032c0b590517a8` |
| package/PROFILE.json | `6af0c3dee0a08d0ba0ec9f126dc6510481fc99569535c41b4ecb56c4bf3c3735` |

All 12 actual source snapshot hashes match the reviewed selection. Independent
enumeration and hashing of all 154 package files reproduces the complete ASSEMBLY
map. All 117 PROFILE entries match actual files. The 24-role replacement map
reproduces the selected hash
`b2cca16ef33e4c909fbcd95958d9f97af249e3477419c52e1a18404a69510a84`.
It consists of the four reviewed Python sources and 20 audited native artifacts.

Exactly 13 files differ from the base: four Python files, eight parts from the
two changed Lean modules, and PROFILE. The other rebuilt parts happen to retain
their bytes. No unselected role changed; all eight documents remain unchanged.
All original base-package files were independently rehashed and still match its
preserved assembly map. No base file was overwritten.

Every installation file is byte-identical. INSTALLATION remains
`9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27`;
independent recomputation of its domain-separated implementation claim yields
`86b6fcce8d8f13479e8131e1a386782b7bda5b6ee579df46e640ca8005affbea`.
The assembly receipt correctly records ASSEMBLED_NOT_ADOPTED, zero native calls
and no owner open. No anchor migration or change in mathematical trust occurred.

The outer command exits zero, direct child is reaped, Job closed, active processes
zero, cleanup errors empty, and no termination was requested. stderr is empty;
stdout is 25,488 bytes. Measured outer wall is 5.3351815 seconds, Job CPU
1.546875 seconds and separate outer-wrapper CPU 0.65625 seconds. Peak Job private
commitment is 18,669,568 bytes. The unchanged 90-wall/45-CPU/768-MiB/three-active-
process selection contains this file-only operation.

Build and native-free control outcomes are separately recorded. Native cut
presence, a genuinely false-under-parent candidate and useful downstream
refinement remain unexecuted obligations; this exact package is ready for their
separate root-selected use, not an accepted full-v5 release.
