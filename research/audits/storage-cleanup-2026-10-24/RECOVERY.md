# Restoring an archived extraction

Cleanup keeps the original ZIPs and removes only verified duplicate extracted
payloads. It does not remove proof results, user source, node state or Git history.
The final `RESULTS.md` identifies what was actually removed; candidates in PLAN
are not evidence of removal. The retained sibling `BASE-FILES.json` and
`CONTRIBUTOR-FILES.json` record every application file's relative path, length
and SHA-256. The per-target `v3-PRUNE-INTENT.json` / `v4-PRUNE-INTENT.json`
record archive and manifest hashes and directory paths. The interrupted verifier
did not produce its proposed combined ARCHIVE-VERIFICATION.json; do not rely on it.

| Original extraction to restore | Retained ZIPs | Extract under this parent |
|---|---|---|
| `product-local/certified-v3-package-01/app` | `mathematical-commons-v3-base.zip` and `mathematical-commons-v3-contributor.zip` | `product-local/certified-v3-package-01` |
| `product-local/certified-v4-package-01/app` | `mathematical-commons-v4-base.zip` and `mathematical-commons-v4-contributor.zip` | `product-local/certified-v4-package-01` |

All paths are under `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Archives are adjacent to the removed extraction, not inside it. Historical guides
and scripts naming those paths need restoration first. Current v5 uses the
preserved `software/runtime` and other explicitly selected installations.

## Extraction-only recovery procedure

1. Read the final cleanup result and exact verification map. Verify the recorded
   SHA-256 of each required ZIP before extraction. Do not download a newer version
   or substitute a similar installation.
2. Resolve the original target and its parent, refusing redirected/reparse paths.
   Require the extraction target to be absent. If a partial target exists, inspect
   it; never overwrite it or recursively delete it on assumption.
3. Extract only the validated ZIP members below the stated parent. Their top-level
   prefixes are already `app/`; do not add another nested
   prefix. For each packaged application, both archives are needed. Ordinary
   `Expand-Archive -LiteralPath ... -DestinationPath ...` without `-Force` can
   perform the extraction after these checks; no old packaging script is needed.
4. Recheck the complete restored file census, lengths and SHA-256 against
   the preserved package file manifests. Recreate recorded empty directories if
   any. No recovery of arbitrary original NTFS timestamps is claimed. Reapply
   appropriate owner permissions;
   ZIP payload hashes do not reproduce NTFS ACLs or security policy.
5. Only after validation use the original paths. Restoring software bytes does
   not restart old experiments, renew consumed budgets, import mathematical
   acceptance, recreate credentials or authorize external publication.

No recovery operation is needed for normal current v5 development. Do not restore
every historical extraction automatically; that would recreate the redundancy.

The old Lean extraction was **not removed**. Its unfinished comparison was not
promoted into a pass, and no restoration is needed for that path.
