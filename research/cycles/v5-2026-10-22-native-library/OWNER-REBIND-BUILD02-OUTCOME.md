# OwnerRebind build02: independent saved-evidence audit

Reviewer: `admission_event_audit`, 2026-10-23. Read-only examination of the
completed operation; no compiler, checker, preparation or admission was rerun.

## Disposition

PASS for compilation of the explicit-field return-record repair. This is not
owner use, successor acceptance, installed discovery or final-v5 qualification.
The prior failed build remains preserved and charged. Retain the five successful
artifacts for subsequent selected support compilation; do not rebuild them.

Operation: `experiments/v5-local-checks/ordinary-owner-rebind-build-02`.

| File | SHA-256 |
|---|---|
| selection.json | `c01bb8b8d36af41414613613cbf8a26eddacc4f921287fcf5d435ed057d9f65d` |
| RESULT.json | `05931b1310099f9a9ae5e818e112b5802152460d9ed6f623496cd934d2663db2` |
| COMPILE-RESULT.json | `0f5466c01c00d11eb16f5b1bd0392cfbb8b8def88d4f15f33acf5ce151958cc5` |
| selected OwnerRebind.lean | `c0fb82558f33b28809b8145b7e053037d485d1d21abfbc2ba9f5c034f8b82b68` |

All three selected source snapshots and every selected runtime/helper pin were
independently hashed and matched. Comparison with the preserved failed
`ordinary-public-remaining-01` OwnerRebind source finds identical text before
the final return record. The remaining difference is exactly explicit fields
and multiline formatting for the same returned values; the namespace tail is
unchanged. Thus the conditional semantic review in OWNER-REBIND-SOURCE-REVIEW
applies to the repaired source without repeating the whole semantic audit.

The saved command compiles only OwnerRebind with `-DElab.async=false`, resolving
the retained public-remaining01 and public-expr-sync01 helpers. It exits zero;
its two native log files are empty. The outer operation reports clean Job
closure, zero active processes, reaped child and no cleanup errors or requested
termination. Recorded inner wall time is 1.7350624 s. Recorded Job CPU is
1.671875 s and wrapper CPU 0.4375 s (2.109375 s known total), outer wall
2.344322 s, peak Job private commit 605601792 bytes. These are measurements of
this operation, not general cost bounds or a security sandbox claim.

## Retained complete artifact set

Exactly five files are present in the fresh lean-build directory.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| OwnerRebind.ir | 539960 | `84abf384dc1098381661f92ca86b174b927883159fe954be876df05d47f17da9` |
| OwnerRebind.ir.sig | 176 | `eedbfbb5221895b1aa3ee0bda03f54a9db6d7d289f0b36349b147a156dae3175` |
| OwnerRebind.olean | 195648 | `bb9f472c5900545cf6ddabc5d5dd83d26026ef0f59c37a5bcf49cb0bb4e97331` |
| OwnerRebind.olean.private | 1379904 | `d30ade1d15d75ff20bf5c9b22265ea1dc9e34087b82c646c63872bceba4dc48e` |
| OwnerRebind.olean.server | 14984 | `d2cf740f229f639aeae966a10b52c6af8cdcef8ad3ecc3a68347c1e59d7dbc1b` |

No prior admission profile, accepted catalog or successful mathematical prefix
was modified by this review. Subsequent owner use and independent receiver
checking remain the central unperformed boundaries.
