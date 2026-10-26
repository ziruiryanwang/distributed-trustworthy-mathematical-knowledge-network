# Independent saved-output audit: bounded transport assembly01

2026-10-25. **PASS for the exact file-only assembly.** No execution was repeated.
This review used saved JSON, ordinary-file census and SHA-256 reads only. It
does not adopt the product or claim a public-service/mathematical result.

## Exact operation and artifacts

Run: `experiments/v5-local-checks/bounded-transport-assembly01`.

| Artifact | SHA-256 |
|---|---|
| Original and copied selection.json | `d598eb56a1b71bae0aef510a0acf3f4ea7560e03f68a072067cb36d177369dd4` |
| RESULT.json | `0dd89a706296aa7ec83b24bacad25caa25f05cecbcfa5fbc5db0dc818abfefbd` |
| assembled/ASSEMBLY.json | `0e7bb0b41f82652eda542eb1bd8817e228f824a813fd5af617d262035c17285c` |
| assembled/package/PROFILE.json | `b047d4492da79e363fcd154144a6d9088a93100fde7aac3c385f3a296a41dad7` |
| Unchanged installation/INSTALLATION.json | `32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2` |

All seven original/snapshotted source pins and all 156 selected input/runtime
pins were rehashed and matched. The actual command invokes the reviewed
assembler snapshot with the exact sparse base profile/receipt and overlay.
Saved stdout decodes to the same complete assembly receipt. Stderr is empty.

## Independent complete-map check

The reviewer enumerated both trees without following reparse points, hashed
every file, and reconstructed the successor map from PROFILE, the installation
manifest (excluding external runtime references) and receipt documentation pins.
All 154 actual files match all 154 expected names, lengths and hashes; there are
no missing or additional files. Total successor logical bytes: 39,127,248.

| Comparison with the 152-file sparse predecessor | Actual result |
|---|---|
| Existing files with identical bytes | 150 |
| Changed existing files | PROFILE.json and support/transport/http_provider.py |
| Added files | BOUNDED-TRANSPORT.md and EXECUTION-TRUST.md |
| Removed files | None |
| Auxiliary roles | 117, with only the provider pin changed |
| Installation manifest/native payload bytes | Unchanged |

The changed provider is exactly the reviewed 29,560-byte source
`9288996fa1d4e737f500043cddfc1c7935d9b7830ac6638596b6f7f278f2add7`.
The three overlay outputs match their selected pins. The predecessor profile
and receipt still match `97f93cc6...` and `b138a640...`, respectively, with their
full values fixed by the reviewed assembler and selection.

## Closure and actual cost

The saved outer result is `COMMAND_EXITED_ZERO_AND_CLOSED`, child exit 0,
direct child reaped, Job closed, active processes 0, no cleanup errors and no
requested termination. Two total Job processes were recorded. The actual
original limits were 60 wall seconds, 30 CPU seconds, 768 MiB, four processes
and 1 MiB per log; assembler cooperative limits were 35 wall / 20 CPU seconds.

- Outer elapsed: 5.3272415 seconds; supervised command through cleanup:
  5.1800445 seconds (nested, not additive).
- Job user+kernel CPU: 1.359375 seconds; outer wrapper CPU: 0.265625 seconds.
  Known combined CPU: 1.625 seconds. The assembler's 1.265625 seconds is already
  inside the Job total and is not counted again.
- Peak Job private commitment: 17,141,760 bytes. Logs: 2,328 stdout bytes and
  zero stderr bytes.

The reviewed command is file-only: copied native files are inert payloads,
not executed stages. It imports the pinned file helper, not product modules;
there is no native build, mathematical check, owner-state operation or service
start in this assembly. The receipt correctly remains `ASSEMBLED_NOT_ADOPTED`.
Actual public-wrapper/service evidence and its outcome audit are separate.
