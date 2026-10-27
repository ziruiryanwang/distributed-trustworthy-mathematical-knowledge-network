# File-only auxiliary package source review

2026-10-26. **SOURCE PASS**, conditional on root selecting actual independently
reviewed build/result and replacement-map hashes. No blocking source defect was
found. This is not assembly execution, product qualification or adoption.

Reviewed complete assembler source `assemble.py`, SHA-256
`d6bc12e770f9d3cdfe8cee520159a0089406bcc324cee6711b2585feb4935fa9`,
and PACKAGE-PLAN.md,
`356c4146c313bc4adaf7663082aacb09478c1c8739d82cb0fd3b78fcbe30da58`.
Read the used file-helper functions in ordinary_fair_search/assemble.py and
verified its selected hash
`9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30`.
No entrypoint, product import, test, compiler, package copy, owner/database operation
or Git mutation was executed by this reviewer.

## Exact scope and evidence

The adapter requires canonical cwd, isolated `D:\Python314\python.exe`, a selected
experiment source snapshot, and a new `distribution` sibling of that snapshot's
sources tree. Its native input must be in a different run under the canonical
local-checks directory. The pinned helper supplies bounded ordinary-file/path
validation, rejecting redirection, hard-linked files, unsafe relative names,
existing output and unexpected file censuses. Immutable owner-controlled local
inputs are assumed; these checks are not a hostile concurrent-writer lock.

The pinned base ASSEMBLY/PROFILE/INSTALLATION are cross-checked against the
154-file census, 117 auxiliary roles, eight documents and implementation-claim
hash. Every base file is read and pinned. The base and all installation bytes
remain unchanged; no destination is an existing package or state directory.

Actual BUILD.json and the enclosing closed-success RESULT.json must match
caller-selected hashes. The result's selected launch hash is read and pinned.
The adapter checks four successful commands in dependency order, zero receiver
compilations/owner opens, the exact four-source and 20-artifact census, and source
identity across the build selection, staged build input and assembly snapshot.
Thus partial files alone cannot supply a build-success claim. Root must still
review the actual terminal evidence and choose those hashes: the assembler does
not independently prove that a receipt's assertions were honestly produced.

## Allowed changes and write boundary

The only replacement roles are four Python files plus five emitted artifact
parts for each of four auxiliary Lean modules. Their complete 24-entry map must
match an externally selected canonical SHA-256. All four Python files must
actually differ from the base. Rebuilt artifact parts may be byte-identical;
the report correctly distinguishes replacement roles from changed bytes.
Only PROFILE may additionally change. The 154/117 censuses, all eight documents,
every installation file, INSTALLATION hash and implementation identity are
preserved. The total resulting package is bounded by 256 MiB.

Files are created with exclusive writes, flushed and read back against exact
pins. Input pins and the base census are checked again before PROFILE is written
last. Final package census/PROFILE pin and an external ASSEMBLY receipt follow.
Interrupted partial output is preserved and cannot be silently reused or retried.
The 90-wall/45-process-CPU internal guards are supplemental; the selected outer
Job must supply the actual full-process containment and terminal closure.

For a later exact selection, include this assembler, the pinned utility, all four
Python successors and all four matching Lean sources. Pin the actual build
receipt, outer result, selection and selected artifact files; bind the exact
24-entry payload map. The already completed six-source and build-binding review
is in REVIEW.md. Root alone owns launch, actual-output audit and adoption.
No native-free, semantic-negative or real-use control is promoted by preparing
this package, and no protected anchor migration is selected.

## Exact package selection binding

PASS for source/selection binding of
`experiments/v5-local-checks/demand-frontier-package01.selection.json`, SHA-256
`16580fe3a9f401354c1089d75ab2175bec7918812f6973cd2fda47d18c22f9a8`.
All 12 source and 191 explicit input/runtime pins were independently hashed and
matched. The CLI selects the already audited build receipts
`afeb2fb9e3af2c4d9d86154bafe1c1b594bffc67fe06aacb34ed43e81bded001`
and `db5fc91c1d154923a5300235d6a012ce7faffedca78e6903e222e0dffd734b3a`.
Independent standard-library reconstruction from the actual build's 20 output
pins and four reviewed Python files reproduces the exact 24-role payload map
`b2cca16ef33e4c909fbcd95958d9f97af249e3477419c52e1a18404a69510a84`.

The invocation uses isolated Python and a fresh `{output}/distribution` under
the selected runner, with 90 wall seconds, 45 aggregate Job CPU seconds, 768 MiB,
three active processes and 1 MiB per stream. This selects only file assembly;
it does not invoke product code or mathematical state. Root owns launch and
actual-output adoption. This selection review executed only file/hash reads.
