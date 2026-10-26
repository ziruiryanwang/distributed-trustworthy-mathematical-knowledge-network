# Contact federation: actual assembly outcome

Disposition: **PASS_ACTUAL_FILE_ASSEMBLY**, not an API, mathematical, public
deployment or full-v5 qualification. Independent saved-output audit by
`ordinary_routing_gap`; no assembly/test was rerun and no package bytes were
edited. Canonical root is
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Exact operation and evidence

The selected operation is `contact-federation-assembly01`, under
`experiments/v5-local-checks/contact-federation-assembly01`.

| Evidence, relative to that operation | SHA-256 |
|---|---|
| selection.json | `4bdeaf7a5a3548b25dce56da21d80a4293bbeb48d07f399b9376c5c0cced56de` |
| RESULT.json | `ba32f18fdcbc070046fd052838577205851ead3490860c0fd0c320b82c01f245` |
| assembled/ASSEMBLY.json | `02739f6f44aeb0d56765dea12f82a5e195c1040379db9407221254d7f2dbe79d` |
| command/command.json | `b3479afe16e274f84ee36804e1601693970156d1304527846c65301b6e152b75` |
| command/stdout.txt | `e71c402d75498de5b5cb24853ec1594cbb1e7a4d80f6594c7129385c1cbb00dd` |
| command/stderr.txt | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

The actual command/arguments equal the selected arguments after snapshot/output
substitution; command-limit keys and values match the selection. Stdout parses
to the same object as ASSEMBLY.json. Stderr is empty. The outer result is
`COMMAND_EXITED_ZERO_AND_CLOSED`, exit zero, direct child reaped, Job closed,
zero active processes and no cleanup errors. No termination was requested.

## Full-map audit

Read-only checks independently confirmed:

- All 15 saved source snapshots match the exact selected hashes.
- All 152 selected external inputs still match, including every predecessor
  package file, its receipt and the three Python attachments.
- The output census is exactly 150 files, with no reparse entries. Every output
  length/hash matches the predecessor map with the ten selected overlay entries
  applied and the receipt-bound new PROFILE.
- Of the predecessor's 147 non-PROFILE payloads, 139 are identical, eight are
  replaced and two new files are added. No payload is silently dropped.
- PROFILE has exactly 116 auxiliary roles: the predecessor roles plus
  `support/transport/contact_directory.py`. All role pins match their selected
  original/overlay entries. Top-level field sets and all non-files fields are
  unchanged, including installation manifest, helper paths and author worker.
- The installation manifest remains
  `32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.
  All installation/native support bytes are unchanged. The nine manifest-named
  external Python/Lean attachments were additionally length/hash checked while
  preparing the API selection below; all matched.

The resulting package is
`experiments/v5-local-checks/contact-federation-assembly01/assembled/package`.
Its exact PROFILE SHA-256 is
`3d127796190ca3d049bd956288025c10c4ac7e383a15685aca6ea8d2fbc61479`.
The assembly receipt correctly says `ASSEMBLED_NOT_ADOPTED`: this saved file
operation supplies a coherent package for a later selected test, not an
automatic software-release decision.

## Observed cost and closure

Whole wrapper elapsed time: 5.0304141999 seconds. Supervised command through
cleanup: 4.8203671998 seconds. Observed Job CPU: 1.578125 seconds; separately
recorded wrapper CPU: 0.359375 seconds. Assembly's inner counters are
4.2130644997 wall seconds and 1.46875 process CPU seconds; these are nested
measurements and must not be added to the Job totals. Peak Job private commit
was 17,543,168 bytes, not a prediction for subsequent loader/search workloads.
The original 90-wall/60-CPU/512-MiB/three-process outer bounds were unchanged.

## Prepared API-suite selection: not executed

Created `experiments/contact-federation-api01-selection.json`, SHA-256
`fd4616ffc53f9d0fcd0383f750a49b2f0dd313e8c590e7eacc6269df5c229046`.

It selects the existing pinned Run-V5-Check.py and the independently reviewed
`test_directory.py` at
`9104f4525fbaee565c4e6ca6ff30333ee59541c75eae56d5af4142289b06175b`.
The two source snapshots run that test with isolated Python `-I -S -B`, the
exact new package/PROFILE, the selected Python/Lean runtime paths and fresh
`{output}/suite`. All 150 package files and nine named external runtime
attachments are pinned: 159 external files in total.

Outer bounds are 90 wall seconds, 60 CPU seconds, 768 MiB, three active
processes and 1 MiB for each log. The test's inner 70-wall/35-CPU checks remain.
`experiments/v5-local-checks/contact-federation-api01` was absent when selected.
Root must independently approve this exact selection before its one execution.
No runtime, retry, native mathematical stage or certificate production was
started by this audit. The planned 19 controls use synthetic inert metadata and
loopback sockets; their source-review limitations remain in
`software/v5/ordinary_contact_federation/ASSEMBLY-REVIEW.md`.

The reviewer authored the helper/provider changes but not the assembler or test.
This actual file-integrity audit does not replace the other reviewer's independent
product-source judgment. All used sources, input snapshots and output evidence
remain frozen. Full deployable v5 remains unfinished.
