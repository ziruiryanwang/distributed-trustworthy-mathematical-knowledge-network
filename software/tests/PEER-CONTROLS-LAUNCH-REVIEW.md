# Exact post-cycle controls launch review

**PASS for this bounded launch, not an outcome or full independent source audit.**
Reviewer: `feasibility_checkpoint_audit`. Root's complete source review is
inherited explicitly. This reviewer independently read that review, launch,
allocation/lineage/fresh-root checks and the disclosed private-route correction
in context. No product/Python/Lean execution, import, SQL query or socket binding
was performed. Only this note was written for the launch-review assignment.

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `qualification/peer-controls-launch-01.json` | 1723 | `281aaca488c5fbe8959c0e3ea1657e88a9f1638e20e9a50a7e1649250345e4d3` |
| `tests/peer_controls.py` | 49073 | `d2a5fca8441d0d673d7c54a9de6987e1af48bbdd972a9f0a0a662ac80cc87b41` |
| `tests/PEER-CONTROLS.md` | 13521 | `1a7fb2efd3cb3ad4867df2aed789fcb09b452a57948b738935e1371dca7fe0be` |

The inherited root review has SHA-256
`844db565a763c6d3d0edaae9987dece16a3267d5173596ae32f90254b78b3a9b`.
Root authored the disclosed correction and launched earlier phases; this note
does not reclassify root's source review as independent of those edits.

All direct launch pins match current bytes. PREPARE is the retained successful
23416-byte result; G02 is 57621 bytes with SHA-256
`5bab68a1f02bf97883704f4bef1b4c63a341f0f3c81e169bb72123e086831e6c`;
H01 is 44365 bytes with SHA-256
`4f4e1d1531298706461f3448a564a8edf30e68d6516caed6266158b5af446235`.
G02/H01 phases, attempts and required statuses match; H01 points to that exact
G02 and both to the same PREPARE. The successful launches, original failed-G
receipt/audit, H01 acquisition request/reply, exposure and stopped-service
receipt pins were also checked. Helper/Python match successful PREPARE.

Before any controls mutation, the H01 outcome reviewer independently matched
all 1103 final data-seal files and the full 147659193-byte data census. H01's
original service supervisor is active-zero/reaped. At launch review time both
`qualification/peer-01-controls` and Beta's
`scratch/services/peer-controls-private` are absent. Port availability and
current SQL row values were not inferred or queried here.

The exact grant is 900 active-wall/observed-CPU seconds, 180 seconds per public
command, 1 GiB selected retained bytes, twelve public commands and zero new
native stages. Four cooperative fault sessions are each capped at 90 seconds
and 4 MiB. The real private-route service has 60 seconds, two requests and a
source-fixed 1 MiB send allowance. Source's final obligations additionally
require ten new requests and 432 MiB conservative reservation. No extra retry,
counter reset, source replacement or cleanup deletion is approved.

The correction at lines 714–718 checks HTTP 404, splits at the first header/body
separator, requires the complete body to equal the fixed encoded
`PEER_NOT_FOUND` object, and saves both full raw responses with hashes. It closes
the specific loophole in which a 404 body could still carry private contents.
This finite body assertion and retained raw headers are not a general
information-flow/noninterference proof.

Unlike this read-only launch review, the allocated controls intentionally make
bounded product calls and fault-sender connections, and the harness performs
read-only immutable SQLite observations across quiescent boundaries. Root must
remain sole operator during those observations. Inherited same-host trust,
cooperative-fault-thread containment, incomplete CPU accounting and unexercised
variant/interruption-recovery limits remain. Root may execute this exact cut
once; a separate outcome audit is necessary for any runtime conclusion.
