# Independent review: explicit producer memory profile

Owner: `v5_growth_decision`, 2026-10-16. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
Scope: the delta selected in `PRODUCER-RESOURCE-PROFILE.md`, read completely.
No product edits, imports, builds, native invocations, tests, proofs or Git
operations are authorized or performed by this reviewer.

Status: **PASS for the exact narrow source delta, selection and seven-control
actual outcome**. This review does not authorize proof production.

## Preserved baseline and actual supervisor

| File | SHA-256 |
|---|---|
| `software/v5/aggregate_production/producer.py` | `796eb24619370a30192db6d0f63b914516919e7cae90aee32a1750736331b86b` |
| Its `__init__.py` | `0ca27c691b5afe5ad93086251afb3259491f2ebcaf6e2a9b7ff7b209d4489bb2` |
| `product-local/v4-library-commons-02/commons-v4/operator/commons.py` | `6ea16154f4533e80d2e4e27e12fb6fa0ab7abfa0ff2c52cfb7479c1a35a8c1c9` |
| `product-local/v4-library-commons-02/commons-v4/receiver/helpers/run_stage.py` | `bdd2cbc28258f49ef08b678ba54b437ff541ef4deb0af4aa36795d2baa19b028` |

The retained supervisor's `CEILINGS` at line 24 permits memory up to 8192 MiB.
`limits_checked` at line 115 requires exactly the supported fields and exact
built-in positive integers at or below each ceiling. `supervise` calls it at
line 168 and forwards `limits["memory_mib"]` to the adopted Job constructor at
line 195. The latter sets `JobMemoryLimit = memory_mib * 1024 * 1024` at line
238 of the retained helper. The helper CLI's separate 4096 MiB validation is
not the path used here. No supervisor or SDK change is needed to select a cap
within the existing 8192 MiB limit.

## Conditions for source clearance

The successor must change only the exact profile schema/field, validation of
that owner ceiling against both 8192 and the adopted supervisor's actual
ceiling, and the request's per-stage memory upper-bound lookup. Package source
pins must identify the actual fresh package. No default, global mutation,
legacy edit, automatic budget escalation or fixture-specific memory estimator
is allowed. All other limits and native/cryptographic/continuation logic must
remain mechanically equal to the used baseline.

The whole encoded profile must continue to determine immutable `profile_id`;
carried attempts must match it and the entire budget. Thus a submitted prior
history from a different resource profile cannot be treated as ordinary
same-allowance continuation. This is an owner-held budget mechanism, not a
global tamper-proof registry: an unrelated trusted owner supplying a new
allocation is outside the no-silent-renewal claim. No new such global property
is introduced or required by this narrow refinement.

An 8192 MiB policy ceiling neither reserves memory nor proves proof-production
feasibility. The independent memory obstruction for the retained 4096 MiB
candidate remains adopted funding evidence. Current physical/commit capacity
does not authorize a larger-memory launch. Mathematical acceptance and light
receiver resource requirements do not change.

## Exact successor and mechanical delta

| Fresh file | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/aggregate_resources/producer.py` | 44720 | `1d191bdc2079760ce89a57a08924254f01487d24726e10b386c7eca1ef9eec09` |
| `software/v5/aggregate_resources/__init__.py` | 152 | `0ca27c691b5afe5ad93086251afb3259491f2ebcaf6e2a9b7ff7b209d4489bb2` |

The predecessor rehashes to `796eb246...`. This reviewer reconstructed the full
successor text by exactly four explicitly enumerated, unique replacements in
that predecessor. The resulting 44720-character text is exactly equal to the
candidate. Both contain zero CRLF sequences; the initializer is byte-identical.
This was source-text manipulation in PowerShell memory, not product execution,
an import or a test campaign. No unlisted algorithm/control-flow changes exist
in this compared delta.

The four hunks are:

1. Profile docstring adds the explicit memory ceiling.
2. Constructor exact fields add `stage_memory_ceiling_mib`; schema becomes
   `DMKN_V5_AGGREGATE_PRODUCER_PROFILE_V2`; retained `uint` validates it in
   `1..8192` before loading support. `uint` requires `type(value) is int`, so
   booleans, floats, strings and missing fields do not become permissive caps.
3. After the same pinned support-loader construction, the candidate reads
   `self._A.CEILINGS["memory_mib"]`, requires its exact integer type, and
   requires the chosen ceiling not exceed it. A missing or malformed adopted
   value cannot yield successful construction. The actual retained value is
   8192. No mutation of that value or `P.COMMON` occurs.
4. Inside the existing per-kind/per-limit validation loop, only the memory
   upper bound comes from `self.profile["stage_memory_ceiling_mib"]`; all
   other keys retain their exact prior maximum. Stage `memory_mib` remains an
   explicit positive exact integer, and is passed through unchanged to the
   actual supervisor invocation.

Unchanged code resolves each source pin against the actual package directory,
which is now `aggregate_resources`, not an alias to the used predecessor. The
source identity, native host/build/image checks, mathematical formats,
per-stage argv, output reserves, retained checkpoints, complete prior-history
validation and cleanup/accounting code are textually unchanged.

## Identity and same-history argument

The constructor still canonicalizes the **entire** profile, stores `_raw` and
hashes it into `profile_id`. The new required field therefore participates in
the existing identity. `_check` still rejects any later profile mutation.
Every ordinary prior attempt must still match `old["profile_id"]`,
`session_id`, `allowance_id`, complete preceding pin list, the **entire**
budget and carried external-cost record. Thus changing this ceiling or the
per-stage memory allocation cannot silently continue the supplied old history.
This is the scoped guarantee above, not new global budget authority.

## Conclusion

**Source clearance PASS** for exactly the two hashes above and the scope in
`PRODUCER-RESOURCE-PROFILE.md`. The change makes the retained supervisor's
capability explicitly selectable without changing proof verification, producer
arithmetic or receiver requirements. It does not establish actual integration,
memory sufficiency, certificate production, improved growth or final v5.
No source correction is requested. Root owns adoption and any separately
selected focused controls; do not repeat the ten unchanged aggregate controls.

## Focused controls and exact selection clearance

Root resolved a concurrent six-versus-seven-test scope change by explicitly
retaining the completed **seven-method** candidate. No file was reverted or
re-authored for this review. The exact selected test is
`software/v5/aggregate_resources/test_resources.py`, 16067 bytes, SHA-256
`f86ac914fab8851077313a7089391b8ed5c37b7e31a8cb78b6842235056cc111`.
This reviewer read the entire file, the complete retained `Run-V5-Check.py`,
the complete root preparation selector `Select-AggregateResources01.ps1`,
and the resulting selection JSON.

Exact operation selection:
`experiments/v5-local-checks/aggregate-resource-controls-01-selection.json`,
SHA-256 `9a814b486eed15452732293ec7e76a8c2bc1d43ef0a7712972076a8a7f31ef9e`.
Independent read-only hash checks match **all six sources / 94949 bytes** and
**18 runtime pins / 17155360 bytes**, with no mismatch. The source closure has
only the runner, two retained `production` package files, the two new resource
package files and the new test; no old test suite or mathematical dataset is
imported. The selector preserves the existing finite outer limits:
20 CPU seconds, 60 wall seconds, 512 MiB, two processes, 1 MiB each log.
The proposed six/ eight-GiB limits inside the test are inert integers passed to
an explicit synthetic supervisor, not actual large Job allocations.

Coverage:

| Method | Real logic exercised | Deliberately synthetic boundary |
|---|---|---|
| Required field/schema | Constructor exact fields and V2 schema; missing/legacy/extra rejection | Retained support and build/image adoption |
| Exact integer limits | Accepted 1/4096/8192; boolean, float, string, zero, negative and excess refusal | Same loader boundary |
| Supervisor ceiling | Owner ceiling cannot exceed adopted value; exact-type check | Injected supervisor ceiling, including 4096/6144 and malformed cases |
| Per-stage policy | All five kind maps at owner cap and above/type refusal; process/log maxima unchanged; `P.COMMON` unchanged | Snapshot/build/image records |
| Identity/mutation | Full profile hash changes with ceiling; live mutation refuses | Installation adoption only |
| Forwarding | Actual `run` prepares the exact durable reservation and dispatches selected 6144 MiB limit | One captured failed dispatch; no process or proof artifact |
| Prior history | Same-profile/budget validator positive; changed profile/budget refuses exact lineage error | Explicitly labelled synthetic prior record, not an executed PASS |

The forwarding case calls no real supervisor: it verifies captured argv and
reservation equality, returns a known-closed synthetic nonzero failure, and
asserts the attempt remains FAIL with zero reported proof calls and no receipt
or mathematical admission. This checks the policy handoff without allocating
memory or manufacturing a valid-looking proof artifact. The first-failure
path means absent synthetic stdout/proof files are never consumed.

All seven controls use real constructor/profile/request/identity/lineage code,
but mock the retained loader, build/image and snapshot adoption. The suite is
therefore **not real constructor/install adoption, backend integration, memory
sufficiency or mathematical assurance evidence**. Runtime reports explicitly
carry these boundaries and the four selected import origins. The runner pins
and snapshots the source closure, runs only the selected test script under the
bounded Job, and rechecks runtime/snapshot/selection identity afterward.

**Exact test/selection source review PASS.** Root may make the separate finite
launch decision for this selection. Actual outcome review must inspect both
the enclosing Job and the seven-control result; no success is presumed here.

## Actual saved-outcome audit

Root selected and ran the exact operation once. This reviewer inspected saved
data only; no test was repeated. Run directory:
`experiments/v5-local-checks/aggregate-resource-controls-01`.

| Retained result | SHA-256 |
|---|---|
| Outer `RESULT.json` | `05ac2adb5151fc14b7db4ee0e997106493d69e2d65b3d53f75d8e2822cabb331` |
| `evidence/CONTROL-RESULT.json` | `3385017e08e0603e850c30293d77cf5a9172fc25af87a0a7e4c10e711bd8b429` |
| `evidence/FORWARDED-LIMITS.json` | `7a79b32ecee3b3dc61848222216d3fa5490ef2fa703c46b732b3a783c41ec4bb` |
| Synthetic forwarding attempt `RESULT.json` | `523ae6c8845593fb87005c744ff80237ad38124ea655ae64e267f4cfc307818a` |

Independent checks match the original and snapshotted six-source closure, all
18 runtime pins, exact saved selection `9a814b48...`, and the four reported
selected import origins. The outer argv invokes only the selected snapshotted
resource test under isolated/no-site/no-bytecode Python with the approved
limits. Stderr names all seven methods as `ok`, then `Ran 7 tests` and `OK`;
the structured control result agrees: seven tests, zero failures/errors/skips.

The outer command exits zero and reports `COMMAND_EXITED_ZERO_AND_CLOSED`:
direct child reaped, Job closed, zero active/terminated processes, no cleanup
errors and no termination request. Actual observed Job peak private commit is
24,735,744 bytes, well below the 512 MiB enclosing limit. Known inclusive cost
is **0.859375 Job + 0.265625 wrapper = 1.125 CPU seconds**, with
**1.5650671999901533 wall seconds**. Nested supervision CPU is not added again.

There is exactly one captured synthetic forwarding dispatch, carrying 6144 MiB.
Its reservation pin matches bytes; independently parsed captured argv and limits
are exactly equal to the durable reservation. The corresponding proof path does
not exist. Its inner attempt correctly remains **FAIL**, with
`FIRST_FAILURE_STOPS`, known closure, final binding true, zero reported proof
calls, no retained checkpoints, no receipt and no mathematical admission.
The attempt's planned/attempted-stage counters describe a synthetic dispatch,
not a native call. The top-level control report explicitly records zero actual
native attempts, proof/guest/build calls and one synthetic supervisor call.
Do not relabel that retained expected failure as successful production.

No `FINALIZATION-FAILED.json` is present. Final reviewed census is 123346 bytes,
85 entries / 61 files. This census is retained test evidence, not a storage or
proof-efficiency result.

**Actual outcome PASS, narrowly:** the explicit resource policy, handoff and
same-history boundaries behave as selected in synthetic controls. Genuine
retained-loader/build/image/snapshot integration and real proof affordability
remain untested here. Reuse this outcome; no repeat of these controls or the
ten unchanged predecessor controls is recommended.
