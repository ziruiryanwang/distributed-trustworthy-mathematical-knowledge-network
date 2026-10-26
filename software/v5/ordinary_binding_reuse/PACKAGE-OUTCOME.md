# Independent saved package outcome

2026-10-26. `inert_rehost_relation`; **PASS_SELECTED_FILE_ONLY_OVERLAY**.
Read-only audit of the already completed `binding-package01`; no product import,
assembler invocation, test, native program, state operation, replay or Git change.
This reviewer did not author the assembler. Root owns adoption and subsequent work.

## Evidence and exact selection

Run root: `experiments/v5-local-checks/binding-package01`.

| Artifact | SHA256 |
|---|---|
| selection.json and original adjacent selection | aeafac34504288f3fee12f78681d0b0bc65b04310dba056d555a6453fd07933c |
| RESULT.json | 9f992a9dda4084869268aa841b04e6befb78d4454c10a2d821a8cfa27c8692c1 |
| assembled/ASSEMBLY.json | c9abd70107b6ba7283be1bb14632f0ddc3583e4d8f204463dc399b747056b1bd |
| assembled/package/PROFILE.json | dc0c19b7cf116742caa0751665da93400f6bc5b4663cfe313c3e81aa0d9c58e0 |
| command/stdout.txt | 351397339be188ee76c6288c99427dbd155b743be43979a3878335adf6e7ce9f |
| command/command.json | 9ff24b44a18a3dce6c57d83a0c412a540f83566522fb26a54f7e247508d56749 |

Independently rehashed all six selected canonical source files and all six
snapshot counterparts: exact selected pins throughout. Rehashed all 158 external
inputs: complete 154-file predecessor, original adjacent receipt and three Python
runtime files. Every pin matches. Original/saved selection and RESULT binding agree.
Command metadata argv/limits equal the saved supervisory report exactly; the CLI
uses the snapshotted assembler, helper and successor with the reviewed inputs.

## Complete maps and receipt

Independently enumerated and hashed both complete actual package trees, using
case-sensitive relative-path maps. Each has exactly 154 files with identical path
sets. All 154 predecessor hashes match selection; every successor length/hash
matches the new receipt's complete 154-row map. No extra/missing path, link or
reparse entry was observed in the successor. The exact two changed paths are:

- `reference/baseline_bundle.py`: 19197 to 21363 bytes; old
  `d5a9c13392e2de8b170cbaf4a9a27e4d1e5d99eb2714165848a640069fe42fce`
  to reviewed successor
  `e4b52c2f2e823cc98aa37c8cc7adb0cf79952def9c19b54d7072116a39fa19b6`.
- `PROFILE.json`: new 15885-byte identity listed above.

The other 152 files, including all eight historical documents, are exact.
Both profiles contain 117 auxiliary roles; only the binder's pin differs.
Schema, installation binding, helper paths and author worker metadata remain
equal. INSTALLATION stays 7547 bytes /
`32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.
Thus installed checking/native bytes are unchanged; this is identity evidence,
not execution of a new mathematical operation or old-state reopen.

The 21523-byte external receipt states `ASSEMBLED_NOT_ADOPTED`, exact output path,
old PROFILE `ca257419f464c2e9d968011983673160377f743ebbe2a27e2399b510dce1ce67`,
old receipt `ec5ab7709aba2c4a896fa1898e925effb8f7a95f17bdb300c55307fcc5c10d6c`,
reviewed assembler `8067e7e862e5e3d6abd5513a30197f9bd167552f9223fd49fc0f263a0dec9e3c`,
helper `9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30`,
two changed files and 152 unchanged. Parsed complete stdout equals the receipt.
No ASSEMBLY-FAILURE file exists. These facts agree with, not replace, closure.

## Closure and cost

Outer status `COMMAND_EXITED_ZERO_AND_CLOSED`, child exit 0, child reaped,
Job closed, final active processes 0, no termination request or cleanup errors.
Stdout 22338 bytes; stderr empty. Reported cumulative process count is 2,
distinct from the configured one-active-process ceiling; no concurrency violation
is reported. Outer limits: 60 wall / 30 CPU seconds, 512 MiB, one active process.
The assembler's inner 45-wall/20-CPU envelope also completed.

Outer wall **4.1398688997 seconds**; Job CPU **1.171875** plus outer wrapper
**0.28125** = **1.453125 known CPU seconds**. Peak Job private commit:
**16351232 bytes**. Assembler's own 3.6668748 wall / 1.078125 CPU and supervisor's
0.015625 CPU are nested observations, not extra additions to that total.

## Scope preserved

This is a complete file-only development overlay, not a new source/prebuilt
distribution, public command pass, Std production success, admission, warm-use
result or final v5. Existing exact-map preparer incompatibility remains explicit
in INTEGRATION.md; old packages and failed Std evidence remain unchanged.
Any direct state-free query or distribution update requires root's separate
selection. No retry or additional campaign is implied by this PASS.
