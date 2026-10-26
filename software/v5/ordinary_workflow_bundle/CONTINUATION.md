# Finish the retained archive check without repacking

2026-10-26. Root recovers the already completed controls03 attempt after the
conversation handoff. No duplicate launch occurred. The exact source ZIP was
successfully created and its complete 143-base/10-companion projection checked.
The suite then failed `WORKFLOW_TEST_EXTRA_FILE` while censusing the fresh
extraction, before public verification, links or negative controls. Preserve the
original test, selection, archive, extraction and failed reports unchanged.

Read-only diagnosis over all 155 extracted members found a Windows/Python
metadata distinction: `DirEntry.stat(follow_symlinks=False).st_nlink` was zero,
whereas a direct `Path.stat` reported one. All filenames were expected. Thus the
test rejected incomplete cached metadata, not an observed extra archive member.
The production helper already uses direct file metadata and remains unchanged.

Root selects a fresh test-only successor `test_bundle02.py` for source review.
Its census obtains direct `Path(item.path).stat(follow_symlinks=False)` while
retaining regular-file, no-reparse, single-link, exact-membership and byte checks.
The original pack call is replaced with reading the existing exact archive and
receipt through explicit externally pinned input arguments. It repeats no pack,
build, mathematics or service operation. The retained input's receipt path,
archive hash, base projection, mapping and complete manifest must still agree.

All remaining checks run unchanged against a fresh extraction and distinct
negative fixtures. Exactly one successful subprocess is planned: the relocated
public verifier. This tests the newly reached distribution boundary, not a
relabeling of the failed run. Source review and a fresh root selection must
precede execution; preserve any later failure with no automatic retry. Use the
existing 120-wall/60-inclusive-CPU/384-MiB/four-process bound; no old allowance
is resumed. The full v5 goal is unchanged, local and unpublished.
