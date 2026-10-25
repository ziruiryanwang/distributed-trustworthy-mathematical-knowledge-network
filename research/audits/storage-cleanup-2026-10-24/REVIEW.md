# Independent archive-verifier review

2026-10-24. Read-only source review; no scan, code import, product operation,
archive extraction, deletion or Git action by this reviewer. Only this review
is edited. Root separately owns exact reference review and any deletion.

## Current disposition: GO for read-only verification

Reviewed corrected script SHA-256
`f46856ba9731c225962229016bf173c9cecbe0d31d41a3d0c3416c4b810c8b70`.
All three requested corrections are present: the audit directory's ancestors are
validated; ZIP components reject the listed ordinary Windows aliases/invalid
forms and Unix symlink entries; local length/time/attributes are captured and
rechecked while the read-share-only handle is held, rechecked after closure,
and recorded without replacing the checked values. The automatic PowerShell
`$input` name was replaced with a task-specific stream variable.

**No identified blocker to root's single read-only verification of the three
explicit candidates.** This is not deletion approval or an adversarial concurrent
filesystem guarantee. The candidate roots/ancestors and archives must remain
under the stated controlled-workspace premise; later deletion must independently
check exact retained archives, unchanged census/metadata/reparse exclusions and
current-reference independence. No scan or deletion was performed by reviewer.
The initial findings below are preserved as resolved source-review history.

## Initial disposition: HOLD for three small safety corrections

Reviewed `Verify-ArchivedExtractions.ps1` SHA-256
`201f9930fc9ac0e9daa2224dfba397feea887b985bc61419057e312f42e346c8`, against
PLAN SHA-256 `d06990f7a75fc528b80a57d500fffda874f1e6191e6b4e45c00de3da4d97a88e`.

The explicit three-target allowlist, strict canonical-root descendant check,
ancestor/recursive reparse refusal, case-insensitive complete file-key comparison,
cross-archive duplicate refusal, exact uncompressed length/SHA comparison, retained
per-file recovery map and `CreateNew` report are appropriate. The script contains
no candidate writes or deletion command. Its report correctly disclaims deletion
authorization.

Before relying on its report:

1. **Bind checked bytes to checked metadata.** Currently a local file is hashed
   under `FileShare.Read`, then its handle is closed, then `Refresh()` captures
   the last-write time stored in the report. A same-length change in that gap
   can pair the old hash with new metadata. Capture length/time/attributes before
   hashing, compare them after hashing while the read handle is still held, and
   record that checked metadata. Any subsequent observation must compare against
   it, not silently replace it. This matters because the planned deletion guard
   revalidates metadata rather than rehashing all payloads.
2. **Validate the report's ancestor path.** Exact spelling and `CreateNew` do not
   exclude an existing reparse directory in the output path. Check the existing
   audit directory through the same ancestor/reparse validation before writing.
3. **Use safe recoverable Windows ZIP components.** Existing checks reject
   absolute/colon/backslash/dot-dot paths, but not empty interior components,
   trailing dot/space aliases, reserved device components or invalid/control
   characters. Reject these component forms before treating the entry as a
   recoverable path; preserve only the ordinary terminal slash for directories.

No broad redesign or repeated full inventory is needed. Review only this delta
before root's first verification. The comparison is still conditional on no
uncoordinated mutation between verification and guarded deletion; initial census
is not a transactional filesystem snapshot. Root must revalidate the exact
recorded file/directory set, unchanged checked metadata and no reparse points,
retain the named archives and establish current-reference independence. A source
GO or byte-equality report alone never authorizes deletion.

## Cleanup-only removal-script review

Initial reviewed `Remove-VerifiedExtractions.ps1` SHA-256:
`6ba4241d1256a97ede54f2c11c35906e53124804d0445bb0b99c5d863cdbcf86`.
**HOLD for one small directory-check correction.** Its file checks compare the
verified length, timestamp and attributes, but its directory check uses only
membership/count and does not compare the recorded `last_write_utc`, contrary to
the plan. Retain directory metadata in a map, compare it at each popped directory,
and reject the popped directory itself if it is a reparse point before enumerating
its children. No broader implementation change is requested.

The rest of the deletion scope is appropriate under root's separately established
quiescence and reference-independence premises: exactly three absolute allowlisted
strict descendants; exact verification-report hash; adjacent recovery ZIP length
and full-SHA rechecks; current file/directory census and file metadata checks;
ancestor/entry reparse refusal; visible running-executable refusal; durable fresh
per-target intent before `Remove-Item -LiteralPath`; post-removal checks and fresh
per-target/overall results. The ZIPs lie outside each removal target and are not
passed to the deletion command. No broad/glob or cross-shell deletion is used.

Limits remain explicit. Metadata comparison is not a defense against hostile
same-size edits with restored timestamps, and the executable-path query is not
proof that no process has a file handle or loaded module. Root must hold project
writers and verify current dependency independence separately. Removal is not a
multi-target transaction: any interrupted deletion leaves its durable intent and
requires inspection/recovery, not a blind rerun. Retain all archives and reports.
This reviewer has not executed verification/removal, opened databases, deleted
files, or changed Git.

### Corrected removal source disposition

**Source GO, conditional on root's separate reference selection and successful
exact verification result.** Corrected removal script SHA-256:
`f018b0bcd1b65b60de2317b8d92bfedd43a46d75755eb57056d2d450fcaf22b7`.
The sole requested delta is present: a case-insensitive directory map retains
the verified record; each popped directory must belong to that map, have the
same `LastWriteTimeUtc`, and not itself be a reparse point before enumeration.
Final directory count uses this map. Initial source HOLD is resolved, with the
quiescence, nontransactional-removal and recovery limits above unchanged.

No candidate deletion has been authorized or executed by this reviewer. This
closes the assigned source review; root alone evaluates the actual report,
current dependencies and exact removal selection before acting.

## Interrupted verification: narrowed two-package source review

Read `INTERRUPTED-VERIFICATION.md` and the complete fresh
`Prune-VerifiedPackages.ps1`, SHA-256
`639f00f5f59a6f50cb14b830ce9342312fcd15c78b4a32c432d792ae60eba77e`.
**Source GO under the stated held-writers/ordinary-metadata premises and root's
actual observation of the two completed comparisons.** This is not a recovered
three-candidate pass or independent review of a nonexistent final JSON report.
The earlier three-target remover is superseded for this maintenance selection;
the Lean extraction remains untouched.

The earlier verifier emits each `VERIFIED` line only after that candidate's full
ZIP/local byte-hash, length and file-set comparison. Root reports seeing both
13,004-file app lines, with 2,444,576,373 and 2,444,835,804 bytes respectively.
This reviewer has not repeated those comparisons or independently recovered their
missing process outcome. Treat the two observations as root's retained operational
evidence, and the unknown final exit/cause as unknown.

The fresh script narrows its literal targets to those two `app` children. It
rehashes four adjacent recovery ZIPs against fixed historical pins, matches
retained manifest membership/lengths to their archive directories, enumerates the
whole current local file set with case-insensitive duplicate rejection, requires
13,004 files and the exact observed byte totals, and refuses any file/directory
write timestamp at or after the conservative pre-start cutoff. It checks current
ancestors/entries for reparse points and visible running executables, records the
current directory paths and pinned backup paths in a flushed fresh intent, and
uses only `Remove-Item -LiteralPath` on the selected app child. Postconditions and
fresh per-target/overall records preserve partial-removal visibility. Archives,
manifests, reports, package parents and the Lean runtime are never deletion
arguments.

This guard does **not** perform a new local-file SHA pass, compare against the
lost per-file timestamps, or independently validate every retained manifest's
SHA field against ZIP contents; those must not become its claims. Byte identity
continues from the completed comparisons only because project writers remained
held and no out-of-model timestamp-preserving mutation occurred. The current
directory list is a recovery census, not equality against a recovered old
directory list. ZIP/archive byte recovery does not promise restoration of every
NTFS-specific metadata feature. These boundaries do not authorize broader cleanup.
Current-reference independence and exact execution selection remain root-owned.

The assigned cleanup source review is closed. No scan, archive comparison,
deletion, product operation or Git mutation was performed by this reviewer.

### Final recovery-map pin delta

The final narrowed script is now
`7bd591d8ac3a264b287743249815d27f00f79a7c39f47360828755be053004b9`.
**The same conditional source GO holds.** Read the new literal four manifest
pins and their check before JSON decode; each agrees with the retained package's
historical `RESULT.json` manifest entry. The four archive literals also agree
with those historical results. This strengthens recovery-map identity without
claiming a second local-payload hash pass. No archives were rehashed by reviewer,
no new issue was identified, and the assigned review remains closed.
