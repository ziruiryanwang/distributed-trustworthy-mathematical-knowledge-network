# Narrow relocated directory-to-find preparation review

2026-10-28. query_scaling source/data review. **PASS for the selected seam; no
blocker found.** Reviewed `relocation_checks.py` SHA-256
`7e66acbb5ee87bf8aa2eff91988996efc4ffc1a4fdeab4c3243f4099388ca05b`.
No imports, subprocesses, tests, owner access, native work or Git operations were
performed by this review.

The runner selects the new kit's externally pinned manifest, checks its expected
PROFILE, and pins the three operator files plus package PROFILE before launching
one isolated `prepare_selected.py` child from the relocated kit. The new wrapper
checks the exact 50 direct/72 generated role interface and actual direct source
pins before the unchanged inert preparer runs. No product command is launched.

Both retained input hashes were independently checked against their actual files:
the genuine directory lookup result `f6ce728d...` is DIRECTORY_QUERY_READY with
mathematical_acceptance=false, and its singleton exact-symbol spec equals the
prior real find configuration's spec (`463c3aee...`). The new request uses that
spec through the existing explicit-spec find mode. Its remaining configuration
comes from the same prior request; there is no target-name, pattern-mode or
current-owner claim added.

Success requires child exit zero/empty stderr, parsed configuration equality to
the old find configuration, the new profile/peer/find argument selection, the
50-role interface and absence of the designated unexecuted find output. Manifest,
operator/profile and retained input bytes must remain unchanged. The equality
assertion is JSON-object equality, not a separate raw-byte configuration assertion.
PASS is written only after these checks.

The one child has a 45-second timeout and one-MiB retained-log checks; hard
aggregate process/memory/time accounting belongs to root's stated outer
Run-V5-Check Job. This is a fixed trusted-source control with explicitly selected
local paths, not an arbitrary manifest or hostile-file race test. Failed partial
output is retained rather than reused. There is no rerun of export, lookup,
preview, manifest-refusal, archive/security, service or theorem campaigns, and
no network or owner operation follows from the prepared find arguments.
