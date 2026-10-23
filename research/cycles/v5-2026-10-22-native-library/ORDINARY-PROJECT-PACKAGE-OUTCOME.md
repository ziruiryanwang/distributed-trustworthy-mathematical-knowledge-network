# Trusted-project package assembly: saved outcome audit

2026-10-23, `ordinary_api_flow`. **PASS_FILE_ONLY_PACKAGE_IDENTITY_AND_CLOSURE.**
Canonical guard PASS. This audit inspected saved JSON/logs, source snapshots,
package files and exact retained input hashes only. No rerun, product/test
import, owner-state access, native operation, service or Git action occurred.

## Exact operation and identities

Run: `experiments/v5-local-checks/ordinary-project-package-assembly-01`.
Saved and original selection both hash to
`4abc73a3b88c9d2253586c5744cf94b7042bd21e2faf90f84eca090ff25c7c48`.
RESULT SHA-256:
`10f09429fba6c2e1bc45d83cfd14cf4653cc31a6b9877578783f497d21fa8570`.
ASSEMBLY receipt SHA-256:
`8fe059a86a4af2e5c57dbc1106cdf6c38656e03f59e8559600bf6611796d8a50`.
Its parsed content equals the saved stdout report.

New package PROFILE:
`b584cb21266fcf24502355a929939d8e6d662c75d1d7ea520fb23eb6105c7c69`.
Base peer PROFILE remains
`06649545f962e8ca95b21ab1c87626444bdc06c16e5191b96a8f27e7766505e5`.
The installation manifest is unchanged:
`32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.
Reported native implementation remains
`fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df`.

## Actual file map and selected inputs

Independently hashed all **116 copied payloads / 36,680,088 bytes** against the
new PROFILE and unchanged installation manifest. Compared every nonreplacement
with its actual base file: **113 identical payloads**, including profile.py,
peer code, native installation, compiled helpers and all remaining Python code.
Exactly these three files match the selected source snapshots instead:

| Logical package file | Bytes | SHA-256 |
|---|---:|---|
| `owner.py` | 18,484 | `fed0c9a03833d3ab16338eb84accd84d1458e17d712431260bdad0ca3950f74b` |
| `author_worker.py` | 4,458 | `19f9375fdf4b12cac05baeece6a750aa0d2d363112f51876d451f54c71ab2b02` |
| `authoring/py/ordinary_contribution.py` | 30,879 | `b8eefe6af368d8a7f5c498d563a12b31416c48c877ea471361eadd2a56a90b31` |

Compared the complete old/new PROFILE documents: same file keys and every other
field unchanged; only these three byte/hash records differ. The unchanged loader
is `22fb8b00d76838c7dac77d669c18c72bb253a087be0002c8ef6077a1aa4bdf9b`.
A bounded nonredirected census found exactly **118 package files**: the 116
payloads plus PROFILE.json and ASSEMBLY.json, with no failure marker, pending
profile, extra source, bytecode, catalog or custody state.

All seven saved source snapshots and their live selected source files match
selection pins. All 131 retained runtime-pin paths also still match. This
includes base payloads, manifest/runtime attachments, assembler, preserved
builder and replacement source files. Used source and evidence remain frozen.

## Actual bounded execution and closure

Saved command/RESULT argv equals the selection after snapshot/output expansion.
The actual outer limits equal the selected **90 wall seconds / 50 CPU seconds /
512 MiB / 2 processes**, with 1 MiB per output stream. Inner assembler limits
are the original **60 wall / 40 CPU seconds**.

- Exit code 0; `COMMAND_EXITED_ZERO_AND_CLOSED`.
- Direct child reaped; Job closed; final active processes 0; total processes 2.
- No requested termination, no terminated processes, no cleanup errors.
- Stdout 1,121 bytes; stderr 0 bytes; no final input-binding failure.
- Outer elapsed **4.1426254003 seconds**; through-command-cleanup **3.6660056002**.
- Job CPU **1.640625 seconds** plus outer wrapper CPU **0.65625** gives
  **2.296875 known CPU seconds**. The 0.046875 supervision CPU is already inside
  wrapper CPU; assembler's 1.546875 precommit CPU is inside Job CPU, not additive.
- Peak Job private commit **26,505,216 bytes**.

## Scope

This establishes the selected file-only successor's exact payload identity and
clean bounded assembly. It does not establish new profile-load/CLI behavior,
project import or tactic compatibility, native admission, a network exchange,
performance advantage, hermetic support or final-v5 completion. Those claims
cannot follow from copying unchanged native helpers or a successful assembly
receipt. No new test, repeat or project execution is authorized by this audit.
