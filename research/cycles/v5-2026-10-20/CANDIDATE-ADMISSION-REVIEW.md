# Candidate admission: independent source and finite-launch review

2026-10-22. Reviewer: storage_launch_review. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

**Disposition: source/launch review PASS within the scope below.** No remaining
blocking source defect was identified in the final pinned candidate or six-group
control selection. This is not a runtime result, genuine certificate acceptance,
installed-product adoption or final-v5 acceptance. Root alone selects execution.
The reviewer performed source/data reads and hash checks, not imports, tests,
compilation, verifier calls, database opening or Git operations.

## Exact reviewed selection

The controlling implementation decision is now 6672 bytes, SHA-256
`67ea6d37ea9c512b416441bd880369e24b510b8d4d89da82b7b9a1416f43910b`.
It includes the final-census correction described below and supersedes its
5480-byte predecessor. The supporting failure-isolation design is
`8da717a05fda217b0989c18657682cf45f0ccd8c5975a9dd731679ef851b228a`;
the independent clean-exit challenge is
`2d8ccfd815933ad94f34d6a3907432cac30c37c7b8a640be9018d8017d485ad4`.
The controlling decision expressly retains existing import sessions and staged
selections, and lower try_receive returns a live handle or None, not a dictionary.

All paths in this table are relative to the canonical root. Final byte counts
and hashes were independently reread before writing this checkpoint.

| Source/checkpoint | Bytes | SHA-256 |
|---|---:|---|
| software/v5/candidate_admission/admission/clean_refusal.py | 6462 | `7c1386cce693185ac7d6e1dda149993c892ac5b2d417242fb7e02b873648e5a7` |
| software/v5/candidate_admission/admission/verifier.py | 17835 | `ec6474cdd0580df89f9c646a41c0d909ec20e83da0a42274e0510a6e01bbbaea` |
| software/v5/candidate_admission/aggregate_claims/aggregate_admission.py | 20129 | `ce2cfc95f08699c679128448d9d9f5131cf54acbefa91225db2689a2b1574f5c` |
| software/v5/candidate_admission/client/workspace_evidence.py | 63130 | `e81407b9296d14a3f3f2f1a1c8554efa2747829fa6a2639fc29215c7ed29cb44` |
| software/v5/candidate_admission/client/managed_owner.py | 33789 | `3fb4e619ddff115220eee4b6d594a41b2d051e6f8b6c731d63cca15b2c8555a3` |
| software/v5/candidate_admission/controls.py | 32700 | `61e49ac2130e6f5e5368ec6465e06306dbb6128997638274a5d96d7e4502cb71` |
| software/v5/candidate_admission/README.md | 6683 | `15eb943a1a39a1ac8a1785c52f39b6ab15e65ccecaac8429620e6ebb12bf62de` |
| research/cycles/v5-2026-10-20/CANDIDATE-ADMISSION-FACADE.md | 8476 | `a1a39086b11ca94ffbb5f675cfc6df44fefcf8e26159900ff6a053fca24bfccf` |
| research/cycles/v5-2026-10-20/CANDIDATE-ADMISSION-OWNERS.md | 3920 | `d456eac3d964017bc1862d8fa4e18d03af7acf788bdef1da1d89703b89c0c460` |
| research/cycles/v5-2026-10-20/Select-CandidateAdmissionControls01.ps1 | 5899 | `42adc172a36d5d78861c901e58b8b2b497f7823d911f574565c5a0225d81cfec` |

The base 129-row SDK map is distribution-exact-packet-01-input.json, 2813358
bytes, SHA-256 `328c21bb585881d654f1a23f1704fbaa277ee865f7adb1250cf6c19b85647561`.
Its 129 original sources matched their pins on independent review. Composition
adds one helper and replaces four logical files, plus the already tested frozen
offer-enumeration custody replacement, for exactly 130 logical SDK modules.
Managed-owner bytes equal its predecessor after exactly one embedded facade-pin
replacement; no other managed-owner behavior changes.

## Corrected blocker: final census was not a final liveness boundary

Full inherited-wrapper inspection found that workspace_atomic's action wrappers
ended with active(), census(), return. Census performs filesystem work: original
authority or a deadline could expire during it without another check before a
clean trial result escaped. This was reported before execution. Root authorized
only new trial wrappers in the fresh facade; frozen base/strict APIs stay intact.

The final facade's terminal_final performs active, census, fresh active, then
nonblocking checks against the original grant deadline, every non-None original
owner deadline and the original controller CPU allowance. No blocking I/O follows
those last observations. Both trial wrappers preserve entry serialization,
fatal failure cleanup and finally clearing busy. Only the three new public trial
APIs use these wrappers. Eight focused sync/async cases cover authority withdrawal,
grant expiry, original-owner expiry and controller CPU overrun during census.
The correction closes the identified observation-order defect; it does not
promise that authority cannot change after an observation or after return.

## Lower clean-refusal boundary

The new helper and complete I/A successors were read, including their selected
pin_phase and supervisor contracts. Comparison with predecessors found a shared
ordinary execution/binding body plus a narrow opt-in nonzero branch. Strict
receive does not gain a None outcome. Opt-in unsafe exits remain fatal.

Clean None requires the directly returned same-call supervisor object, not
authority inferred from persisted JSON: exact report/final-Job/limit fields;
COMMAND_FAILED; strict integer exit 1; no supervisor error; empty stdout;
complete unforced closure; zero final active/terminated counts; finite consistent
CPU and selected wall/memory/log bounds. Cumulative total processes is not
confused with the simultaneous-process cap. Last observed Job must equal final
Job, including types. Actual ordinary log files and lengths are independently
checked, with correct support for zero-byte stdout.

Output validation uses a bounded own-attempt census, not an old-handle or global
knowledge scan. I's opt-in envelope is receipt bytes plus 1 MiB and 32 entries,
also checked on opt-in success. A retains its existing output reservations and
census. Reads are cap-plus-one bounded and guarded. Refusal evidence is written
as pending final owner guards, never as self-authorizing acceptance.

After subprocess completion the code independently refreshes original pins,
trust and origin, checks actual output, rechecks exact inputs, repeats fresh
finalization and enforces the original final deadline. No pin phase spans the
worker call. No new owner, deadline, refund, negative cache, rollback or restored
revoked handle is introduced. Attempt charges remain. No refusal-branch writes
to old handle/member registries were found. Positive binding/handle insertion
retains the existing checks. Strict A's fatal revocation and strict I's historical
delegation of closing to its client wrapper remain distinct, not silently changed.

The helper is included in the pinned runtime/source-origin requirements. The
selected preparation composition has 109 v5 Python sources, below source cap
120. Its I/A runtime composition reaches exactly 128 pins (109 sources, 16 Python
runtime DLL pins, Python executable/DLL pair and verifier), equal to current cap
128. No cap widening is needed here; another source addition requires a fresh
composition check rather than assuming spare capacity.

## Facade noninterference and unchanged mathematical authority

New APIs are try_admit_terminal_local, try_acquire_terminal and
try_acquire_terminal_exact. ADMITTED carries the ordinary live warrant;
NOT_ADMITTED has no warrant and requires lower clean None. Structurally valid
unsupported mixed evidence is classified before any terminal verifier. This
does not mean arbitrary malformed input is safely ignorable.

The I/A admission ports return None before positive warrant/cache/member writes.
A member binding precedes issuer invocation. Existing cached warrants/aggregate
state remain validated; exact live journal-to-summary equality remains mandatory
even without caller-supplied expected J. Packet caching occurs only after positive
binding. Acquisition retains candidate, offer or exact-byte, and custody checks,
including custody rechecks on nonadmitted/unsupported outcomes.

No new trial assignment/call stages, imports, changes context, replaces a staged
selection, resets the session, acquires transparent bodies or grants native
authority. Existing sessions/selections are not forbidden. Noninterference is
established by the write paths, not by copying/restoring old authority. Focused
controls compare staged dictionary contents as well as identity, after refusal,
positive I/cache reuse and A paths. Success uses ordinary positive caches; this
is not a claim of acceptance by popularity, issuer identity or human intention.

## Six focused groups and evidence limits

| Group | Actual exercised code/data if selected | Explicit doubles / limits |
|---|---|---|
| 01 | Helper conjunctions, field/type/numeric/closure checks and input nonmutation | Synthetic supervisor reports; no real child |
| 02 | Actual ordinary output files, empty stdout, log lengths, entry/byte caps, active failure | Artificial file contents; no cryptography |
| 03 | Selected facade methods, terminal packet/J/A-member parsing, charges/cache dispatch and staged preservation | Fake issuers, warrants and stores; mixed classification explicitly doubled |
| 04 | Actual three public methods/decorators and eight post-census refusals | State/acquisition doubles; no elapsed-time experiment |
| 05 | Actual I owner/helper transition, retained charge/registry checks and fatal cases | Constructor, worker and pin/trust guards doubled |
| 06 | Actual A owner/helper transition, changed-header refusal and retained reservations/member state | Same explicit owner/worker/trust doubles |

Controls do not claim a genuine prior accepted handle, cryptographic verification,
source-origin enforcement at runtime or continued real import after a refusal.
Those remain an actual integration boundary, not a reason to repeat previous
positive campaigns. Passing controls would support only the selected boundaries.

## File-only selector and finite execution envelope

Root's prepared selection is candidate-admission-controls-01-selection.json,
27300 bytes, SHA-256
`dd27460f328620edb63f0dea392eca5af7c3598301bfa2d863ad945c2f224686`.
The selector itself only prepares a fresh selection and refuses reused paths.
It executes no test. Independent data review confirmed all 137 selected physical
source hashes still match and all 29 inherited runtime-pin values equal their
frozen basis. This last value comparison is not a new runtime-binary audit.

The 137 snapshots consist of 129 unchanged physical base-map files, six overlays,
runner and controls. Runtime pins total 30: the frozen build basis's 29 plus the
directly imported frozen supervisor. Selected controls stage exactly 130 logical
modules from snapshots before product imports; predecessor physical bytes remain
preserved. Frozen custody is
`e1e35cecd8f40154a98e40cb1a5a2cca1d8c376966e57ef529c7c878bdd6c634`;
runner is `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651`;
supervisor is `6ea16154f4533e80d2e4e27e12fb6fa0ab7abfa0ff2c52cfb7479c1a35a8c1c9`.

The selected invocation is isolated Python -I -S -B. Limits: 30 CPU seconds,
90 wall seconds, 256 MiB, one simultaneously active process, and 1 MiB per log.
Popen and os.system are prohibited during product imports/control execution.
No loopback service, native work, proof production or verifier subprocess is
selected. Root retains finite-launch, actual outcome/closure audit and adoption
responsibility. This review neither executes the selector again nor renews any
old allocation. One later separately reviewed genuine-I refusal/continued-use
operation can address the remaining integration boundary without rebuilding the
full installation or repeating unrelated completed work.
