# Installed producer controls: independent actual outcome

2026-10-22; auditor `storage_launch_review`. Canonical root only.

**PASS_ACTUAL_NATIVE_FREE_CHANGED_BOUNDARIES_WITH_EXPLICIT_DOUBLES.**
The one selected run completed all three groups with zero failures, errors,
skips or forbidden calls. This audit used read-only saved JSON, text and hash
checks. No control rerun, import, constructor, native call, proof, build or Git
mutation was performed. Root owns adoption and any subsequent build selection.

## Bound actual evidence

Run: `experiments/v5-local-checks/installed-producer-controls-01`.

| Evidence | SHA-256 |
|---|---|
| Original and copied selection | `00acd575616c9ca7a7768501eb6575929fe925e8b3a4f1f97927e4a952caee71` |
| Real outer `RESULT.json` | `d8a4632776b4b7a998e79bf6951c81cae42d89bc355d496a3eac32f48f29e52a` |
| `installed-producer-controls-result.json` | `f9a6a8a39037f3218f163772591edf41b0a0534673e4ac7883b2b9b0f077b698` |
| `command/command.json` | `17a8ac5f4761b85574f32329348b08db2c7962f09f3cd38570e382bc7c8dd4db` |
| `command/stderr.txt` | `65713a24e1749a2fabc161fa477c17c7ed2e979676929006d267c83ee21aa2d9` |

All five source originals and their saved copies match the selection and
reviewed hashes: runner `44a7bf1b`, contract `ad2e63a2`, launcher `3310fbac`,
distribution `afbea96b`, controls `03918aae`. Their respective copied lengths
are 5,735; 30,932; 16,594; 73,536; and 24,247 bytes. Full hashes remain in the
bound selection and `INSTALLED-PRODUCER-CONTROLS-FINAL-REVIEW.md`.
The controls report's three helper pins and self pin agree with these copies.
All 23 explicitly selected runtime files also matched their selected hashes
during this independent audit. Expanded argv equals the saved actual argv;
the actual cwd and resource limits agree with selection.

Selector01's preparation failure remains preserved. Selector02 corrected only
its byte summation and prepared the previously absent selection/output name;
this was one runtime dispatch, not a rerun of failed tests. Its source correction
is recorded in `INSTALLED-PRODUCER-CONTROLS-SELECTOR02.md`.

## Real outer execution and cost

The real supervisor records `COMMAND_EXITED_ZERO_AND_CLOSED`, integer child
exit 0, direct child reaped, Job closed, no cleanup errors, no termination
request, and final active/terminated process counts both zero. The real outer
status is not a nested synthetic parent status. No pending/failure marker
exists at the real outer output root. The unchanged runner's own final binding
checks did not produce `FINAL_BINDING_FAILED`.

Known measured Job CPU is 1.046875 seconds (0.6875 user + 0.359375 kernel),
wrapper CPU 0.28125, for 1.328125 known combined CPU seconds. Outer wall time
is 3.147393499966711 seconds; supervisor cleanup-inclusive time is
3.066706999670714 seconds. Peak reported Job private commit is 34,676,736
bytes. These are their reported measurement scopes, not zero-cost startup or
whole-machine accounting. The Job records two total process admissions; the
controls' `actual_child_processes: 0` means no child dispatched by the tested
synthetic producer cases, not that the real test harness used no OS processes.

Stdout is empty; 329-byte stderr contains the three named `ok` outcomes,
`Ran 3 tests in 2.163s`, and `OK`. This is ordinary unittest output, not a
warning-free assertion inferred from empty stderr. Selected limits were
30 CPU seconds, 90 wall seconds, 256 MiB, one active process and 1 MiB per log.
The runner records sampled limits and explicit runtime pins, not a hermetic
toolchain or hostile-code security sandbox.

## Actual changed-boundary observations

The metadata group reports deterministic materialization, relocation-sensitive
identity, four intended pure refusals and profile-command commit. It also
reports the real pure projection's 144 full SDK rows -> 130 consumer rows /
109 ordinary Python rows. These are synthetic source-map rows, not a full
distribution build. The saved created profile and expected fixture profile
independently hash identically to
`89de06386c9d67b4a7a69642f431d35cbd91295147930818622e1bd2f2b33c46`;
the profile output contains neither pending nor failed marker. Complete-release
adoption and validation remained explicit doubles.

The public-evidence group reports seven intended refusals, real pin validators,
shallow historical evidence and the precommit/completed pending distinction.
Saved `evidence/pending` has its intended pending marker; `evidence/failed`
has its intended failed marker; `evidence/shallow` has neither. Their synthetic
saved success records do not establish real native execution.

The parent group called real parent code with its disclosed installed-identity,
base-digest, clock, held-module, supervisor and Job doubles. Independently
inspected saved fixtures have exactly the intended states:

| Fixture | Saved result status | Pending | Failed diagnostic | Reported parent return |
|---|---|---|---|---|
| `parent-success` | Success | Absent | Absent | 0 |
| `parent-late-check` | Provisional success | Present | Present: injected late rebind | 1 |
| `parent-late-check-and-marker` | Provisional success | Present | Absent, deliberately unwritable | 1 |
| `parent-commit-unlink` | Provisional success | Present | Present: injected unlink failure | 1 |

The controls asserted completed adoption rejects each fault fixture. Retained
failure sentinels inside these deliberately faulty synthetic fixtures are the
expected test result; they are not failures of the real outer run. Their fake
zero-CPU supervisor reports must not be used as producer performance evidence.

## Exact qualification boundary

This outcome qualifies the three reviewed native-free changed-boundary groups,
including their deliberately faulted local finalization paths. It does not
qualify actual installed core import, the 60-pin constructor, genuine public
snapshot/request/stage execution, proof production, mathematical acceptance,
funding, complete installation, independent hosting, useful-growth advantage or
the final v5 release. Actual child/host/proof/snapshot/constructor dispatches by
the controls are all reported zero. No complete-release validation occurred.

The distinct full-distribution build and genuine installed-path discriminator
remain separate root selections. This pass is not permission to repeat the
completed controls campaign.
