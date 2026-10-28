# Root integration review

2026-10-28. Source review of assembler `5e047eb86c38f99fef1b24f645bc7649420a550aafbb6cfc6dd0e4204729c87e`
and map `46709b30199384ad1e14f0d54529fe185d429d83c341dfebb117869bbe22ead3`.

No blocking source issue found. The assembler pins the adopted kit manifest and
external pack receipt, verifies its exact package subtree and source map, permits
only the six intended auxiliary-role changes and regenerates PROFILE last after
copy/readback and input rechecks. It does not imply whole-kit re-verification.
The expected 160-file census preserves 153 old files including all mathematical
support; the five replacements include PROFILE, and two files are new.

Direct textual comparisons show only the new query option in run.py, the two
auxiliary role names in profile.py, and prefix/map/count changes in the source
builder. No native lane, installation, accepted root, catalog schema or old
snapshot is rewritten. The existing Windows Job launcher still controls the
one owner-opening export. Subsequent offline lookup executes its bounded pure
source closure and authenticates selected records without owner/runtime loading.

Root also reviewed lookup_checks.py and caught its initial attempt to read core
codec pins from auxiliary PROFILE.files before execution. The unused test was
corrected to bind those two files through the PROFILE-selected installation
manifest and exact evidence/semantics roles. No product code change or failed
runtime was hidden. Relocated CLI checks remain separately selected after actual
export; the source review is not runtime qualification.
