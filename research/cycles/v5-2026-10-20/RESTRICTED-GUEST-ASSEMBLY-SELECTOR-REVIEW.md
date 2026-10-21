# RC guest assembly selector: separate source-review addendum

2026-10-21, growth. This adds review of root's subsequently authored assembly
selector without rewriting the previously delivered assembly review
`85cbf4ab8eab7a4ed8644206164976c24559822641bb9dcd5bb032961a1bb8ff`.

Disposition: **PASS, source scope only.** No invocation, runtime, import,
assembly, proof or Git operation was performed in this addendum.

Reviewed all 7,246 bytes of
`research/cycles/v5-2026-10-20/Select-RestrictedGuestAssembly01.ps1`, SHA-256
`352093175d39f04c1bef139cc3e356c417b6fcdf632e1240e2b05837cf3e67ee`.
Its intended assembler is the reviewed `97951c28` source; root supplies its
full digest and the independently adopted actual guest-build result digest.

The selector agrees with the exact RC schemas, three commands, 12 production
sources, two build adapters, five outputs and three native-adoption records.
It pins the actual build outputs, source snapshot, maps, command/log records,
native records, assembly helper and selected assembler. The assemble command
uses the correct source-snapshot suffix and fresh `assembly` output expected
by `restricted_guest/assemble.py`; the generic local runner expands both
placeholders without changing the canonical execution directory.

The retained runtime filter selects exactly the 21 pinned Python/driver/
kernel files from its digest-pinned predecessor selection. It does not include
the 236 guest dependencies, 26 compiler artifacts, old failures, Cargo graph,
or source compile commands as executable operations. The frozen runner
manifest is pinned too. The resulting source/runtime counts fit the runner's
256-entry limits. Its 120-second CPU/wall, 1024-MiB and two-process envelope
admits only the Python adapter plus its one assembler child; no guest run or
proof is requested.

The selector is preparation, not proof that build adoption happened. Its
parameters must come from root's independent actual outcome adoption, and
the assembler performs the stronger detailed record/path/argv checks before
calling the retained driver. Clean outer completion and final binding remain
necessary after an inner assembly success. No material source-interface
blocker was found.

## Subsequent fresh-build02 name-coherence rereview

Root reported the first guest adapter failed before compiling because it
incorrectly compared a reserialized native saved selection with the original
selected-byte digest. That failure remains retained; review of the fresh
build02 correction belongs to adaptive, not this addendum.

Root changed only these unused assembly consumers to the fresh attempt:

| Source | Final SHA-256 |
|---|---|
| restricted_guest/assemble.py | b2fa03edc27419611fba51238a1cd3504f332c9977bf07529b9639909b179fdd |
| Select-RestrictedGuestAssembly01.ps1 | 1655f1747e0357a924522f2cea7999a2d4a6894fbef2dc08be0bc9c74afb107d |

The assembler now requires `restricted-guest-build-02` and adapter pair
`build02.py`/`recipes02.py`; the selector reads build02's directory and
attempt record. An intermediate assembler retained `recipes.py`, which this
review identified as an actual rejection blocker against build02's two-file
adapter set. Root corrected it before use. The final pair matches.

A read-only byte-comparison check reversed exactly these name substitutions
in memory and recovered the complete previously reviewed source hashes
`97951c28...` and `35209317...`, respectively. Thus no other source changes
are included in this rereview. No source file was rewritten by that check,
and no product script/import/runtime or Git operation ran.

Disposition: **PASS for the final fresh-build02 consumer names**. Actual
build02 outcome adoption and its independent source correction review remain
required. The prior failed attempt is not adopted or silently retried.
