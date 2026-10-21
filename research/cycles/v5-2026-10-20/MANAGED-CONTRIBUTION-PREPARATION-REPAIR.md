# Preparation-only DirectoryInfo correction

2026-10-21, root. The reviewed original selector e3aa2a7f failed before input,
selection, private child directory or credential creation. No product process
started. Preserve that source and this failed preparation outcome.

Actual error: PRIVATE_ORDINARY_ANCESTOR at original selector line 98. Read-only
inspection shows Get-Item's initial DirectoryInfo has PSIsContainer=true, but
its .Parent returns plain DirectoryInfo values whose PSIsContainer is null.
All four inspected ancestors through E:\ are directories and not reparse
points. The guard therefore falsely rejected the first legitimate parent.

Root selects one preparation-only successor,
Select-ManagedContribution01-DirectoryInfo.ps1. Its sole semantic change checks
DirectoryInfo type and Directory attribute instead of the provider-added
PSIsContainer property. The reparse refusal remains unchanged. Source/file pins,
DACL, freshness rules, resource/time envelopes and product sources are unchanged.
The previous input, selection, output and private child paths do not exist, so
the not-yet-created managed-contribution-01 test identity remains unused. No
existing directory ACL is modified. The already-created ordinary private parent
is preserved. This is not renewal of an expired selection or a product retry.

Core_release independently reviews the delta before one new preparation and
the already-selected single public integration. No build, proof or control rerun.

Root read/adopts independent review db8165ae. Exact-text delta and all four
unused target paths were independently checked. Selected successor is10528B,
SHA-2566bd7d82c2d1c65147a97b46eff9f5daca3eb74d7469970c867e8dffe31915d64.
One preparation is now selected with the unchanged release/build/driver/actor/
integration-review pins recorded in MANAGED-CONTRIBUTION-PUBLIC-LAUNCH.md.
