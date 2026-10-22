# Candidate refusal: independent clean-exit predicate challenge

2026-10-22, `storage_outcome_audit`. **SOURCE/THEORY ONLY; NO RUNTIME OR IMPLEMENTATION.**
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Conclusion

A narrowly defined same-call, clean nonacceptance branch can preserve previous
handles without weakening their mathematical authority. It must not classify an
exception by message text, infer safety from `COMMAND_FAILED`, reload a saved
report, or resurrect an owner after revocation. The recommended first scope is
the design author's conservative **exit code exactly 1 plus empty stdout**.
This means **NOT_ADMITTED**, not “the theorem is false” or even “the receipt is
cryptographically invalid”: an ordinary environmental refusal can also exit1.

The existing supervisor contains enough structured evidence for this branch,
but the caller must enforce missing final resource checks itself. No supervisor
rewrite is required merely to distinguish this narrow same-call outcome.

## Exact inspected sources

| Source | Bytes | SHA-256 |
|---|---:|---|
| Selected I admission `origin_phase/admission/verifier.py` | 14570 | `32289cac1c8db4f8a778f5347c4ba843f5e5510d2891b1b8184cc5e6edfc1d80` |
| Selected A admission `trust_withdrawal/aggregate_claims/aggregate_admission.py` | 17385 | `2ef830f849ff214b4e4b3c314332d8d3d3d23844c1a763828e1be5a5f37732aa` |
| Selected `standalone_validation/admission/pin_phase.py` | 8677 | `ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881` |
| Installed `base/operator/commons.py` | 41984 | `6ea16154f4533e80d2e4e27e12fb6fa0ab7abfa0ff2c52cfb7479c1a35a8c1c9` |
| Installed `base/receiver/helpers/run_stage.py` | 30037 | `bdd2cbc28258f49ef08b678ba54b437ff541ef4deb0af4aa36795d2baa19b028` |
| Installed `base/receiver/helpers/domains.py` | 4934 | `651db5f6bb707159c0d29dd6092174bfcebd1dc17b833fdfdacf7e2a66d8522a` |

Installed paths are under the exact-packet release
`product-local/v5-distribution-exact-packet-01/Mathematical Commons v5`, manifest
`ffecdc80e2dc57f062aac0aadf37be2a9dadafa24539b34a2e702c0ec24ee4bb`.
The actual base supervisor manifest is 1,070,384 bytes/SHA-256
`a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed`.
The installed supervisor/Job/helper hashes were independently matched against
the release map. I/A admission and pin-phase hashes were also checked. I/A source,
the supervisor execution/cleanup path, Job construction/statistics, pin-phase
rules and exact-output binding helpers were read; no imported code was run.

## Why the existing status alone is insufficient

`supervise` sets `COMMAND_FAILED` after a naturally exited nonzero child. It also
uses that status for internal exceptions, adding an `error` field. The latter
can involve a failed attach/resume, polling failure or controller limit failure.
Only the zero-exit status receives final CPU/wall/log-cap and terminated-process
reclassification after cleanup. Therefore a fast nonzero child that exceeds a
last-sample bound can still be labeled `COMMAND_FAILED`.

The clean branch must inspect the *returned in-memory report from this invocation*
and its actual output files. A persisted JSON with identical fields is not an
admission/refusal capability. Error strings and stderr contents are diagnostic
data only; neither supplies a safe recovery classification.

## Sufficient gate for the initial conservative branch

All clauses below are conjunctive. Missing, malformed, unexpected or unavailable
evidence fails closed, rather than defaulting to a recoverable refusal.

1. **Same invocation and immutable context.** Capture exact receipt bytes, expected
   summary/header bytes, original owner/trust/profile/image, executable, operation
   path, argv, cwd, effective limits and original deadline before launch. The report
   must have the expected schema/authority and exactly match that argv/cwd/limits.
   No caller-supplied or read-back report is accepted as the process result.
2. **Ordinary child nonacceptance.** `status == COMMAND_FAILED`; strict integer
   `child_exit_code == 1` (not boolean); `error` key absent; service-stop flag false.
   Require actual ordinary stdout file to contain zero bytes. This deliberately
   excludes success-looking output followed by failure and all crash exit codes.
3. **Unforced complete closure.** Strict booleans: direct child reaped and Job
   closed true, termination requested false; cleanup errors exactly the empty
   list; final Job present with strict integer active and terminated counts both
   zero. The observed Job must have existed and had at least one total process.
   Do not confuse the cumulative total with the configured active-process cap.
4. **Final measured bounds, independently of status.** All numeric metrics must
   have the correct nonboolean type, be finite/nonnegative, and remain within
   their selected caps: final Job user/kernel/combined CPU, wall-through-cleanup,
   wrapper supervision CPU (at most its existing60s controller ceiling), and
   stdout/stderr lengths. Compare actual final ordinary-file lengths with the
   report and enforce the16KiB per-log allowance. A strict-integer peak private
   commit check against `memory_mib * MiB` is a useful additional observed bound;
   the Job itself enforces its configured aggregate memory/active-process limits.
   Final total CPU must be consistent with user+kernel within rounding tolerance.
5. **Fresh own-output and exact input.** Use a fresh ordinary operation directory,
   disjoint from installation/runtime pins and existing state. Reread the receipt
   and, for A, header, requiring exact equality to captured bytes. Verify the
   bounded own-output inventory/ordinary paths and an explicit finite byte/entry
   envelope, including saved request/process/refusal evidence. Do not inspect
   unrelated history or a global state tree. I currently lacks A's `_census` and
   owner output reservation, so its new path must not silently omit this step.
6. **Final live authority.** After the process has ended, recheck original source
   origins/imported symbols, manifest/runtime pins, original trust-binding object,
   identity/domain/denial state, image/foundation/policy and owner liveness. Use
   the I `_check_install` / A `_check_live` obligations, with the original guards.
   A pin/trust reuse phase must never span subprocess execution. Complete any
   successful-exit fresh pin/trust/origin sweep before exposing the result.
7. **Original total deadline and accounting.** Keep all attempt/input/CPU/output
   reservations charged. Include preflight, execution, cleanup, rereads, census
   and final evidence I/O in the original effective call deadline, also bounded
   by the owner's deadline. Check monotonic time and owner/controller liveness
   again after the final possibly blocking work; do no further blocking I/O before
   return. No deadline renewal, owner recreation or refunded failure allowance.

Observed low memory use and zero terminated-process count do **not** establish
that no allocation was ever denied. The supervisor does not report all resource
events. That is another reason to say NOT_ADMITTED rather than “invalid proof.”
Memory/resource denial followed by an ordinary clean exit may be safe nonacceptance
under this branch's trust model, but is not classified as a mathematical cause.

Implementation trap: `commons.bounded_read` rejects empty files. Establish empty
stdout through ordinary-file validation plus explicit zero-length/read check,
not by calling that positive-length-only helper and catching its error.

## Handle-preservation argument and fatal boundary

Let `H` denote the live existing warrant registries, `L` the original live-owner
invariant, and `U` monotone charged resources. The desired branch property is:

`L and H and U` before attempt; clean gate above succeeds; no admission/import
commit occurred; therefore return NOT_ADMITTED with the same `H`, still-live `L`
at return, and `U' = U + charged_attempt`, without a new warrant.

The mathematical reason is noninterference: prior accepted handles are immutable
facts under the unchanged adopted trust profile. A later unsuccessful candidate
creates no new derivation and need not invalidate them. Prove registry preservation
from the branch's writes; do not copy/scan every old handle on every attempt.
The guarantee is local and conditional on the already trusted owner process,
filesystem, OS and adopted checker. Windows Jobs are not hostile-code isolation.

I `receive` currently clears busy in `finally` without blanket revocation; A
`receive` revokes all handles/members on every exception. Neither existing API
already supplies the new typed recoverable result. A fresh opt-in implementation
must distinguish the clean branch *inside the owner before* the fatal exception
path, while leaving old APIs and successful acceptance bindings unchanged. Never
catch a revoked-owner error and restore saved registries afterward.

Any timeout, forced termination, supervisor error, uncertain closure, malformed
report, final resource overrun, output/integrity mismatch, trust withdrawal,
pin/origin drift or missed deadline is outside the clean branch. The new owning
path must retain its fatal/revocation behavior. Failure after an irreversible
staging/import action is also outside this minimum; this challenge does not
authorize recovery of mixed/native verification or partially committed imports.

## Minimum future discriminators (not commissioned here)

A successful actual clean candidate refusal followed by ordinary use of a prior
handle is the positive case. Focused adversarial report controls should each
violate one gate: missing/error field, exit type/code, forced kill or nonzero Job
termination, each final resource/log cap, changed input/pin/trust, late deadline,
nonempty stdout and output-census failure. No reason exists to rerun all successful
cryptographic/import tests. Root/design author owns the eventual API and concrete
finite execution selection; this checkpoint creates neither.
