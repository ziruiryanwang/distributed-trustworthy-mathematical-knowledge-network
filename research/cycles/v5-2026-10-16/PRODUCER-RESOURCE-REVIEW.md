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

## Genuine constructor/request preflight: design review

The complete `REAL-PRODUCER-PREFLIGHT-DESIGN.md` was read at SHA-256
`ff3a118effb912c5ccbbe25dc694fec8b29fb8e0cf3946b0e4532476c0af71b4`.
The proposed shortest integration seam is appropriate: construct the actual
owner using the selected retained adoption records, call its actual private
`_request` once, and close it. It must neither call `run` nor invoke a host,
reserve a proof stage or create the prospective production output directory.
The root has separately selected source authoring, not execution.

The source review will check actual imported snapshot origins for both producer
packages; distinct roles for the retained snapshot host and new stage host;
explicit preselected profile/build/image/snapshot pins; real constructor and
request validation without mocks; final identity checks overriding a provisional
pass; and an explicitly unfunded quote whose output path remains absent.
This is an evidence-schema/installation boundary, not fresh cryptographic
verification of the parent receipt or the execution capsule.

The other independent reviewer owns the full-path arithmetic, serialization and
Windows command-line challenge; this review does not duplicate that work.
The proposed 1700 CPU-second segment cap, 8192 MiB memory ceiling and 512 KiB
artifact cap remain planning choices, not proved sufficient limits. Root's
retained historical 325-stage evidence is for the prior po18/I operation, not a
prediction for the present po19/A operation. In particular, syntactically valid
full-path caps establish neither available machine capacity nor an affordable
actual proof. No historical experiment is repeated here.

**Design review supports source authoring only.** Exact adapter source, finite
selection and actual saved outcome still require their respective reviews.

### Marginal-payoff decision before full A production

A successful genuine preflight would close the remaining **known constructor,
adoption-record and request-data integration seam**, not prove actual dispatch,
po19 memory/CPU/artifact feasibility or receipt correctness. Available capacity
and full-path price still govern a separate funding decision; a large syntactic
allowance and a source lower bound are not an adequate machine reservation.

One concrete product blocker can advance while that decision remains open:
the actual ordinary `client/workspace_atomic.py` is deliberately I-only. Its
imports select `frontier_network` (lines29–30), its live-owner checks require
`(receipt, None)` (344/401), and packet parsing supplies `aggregate_image=None`
(490/679). Existing mixed receiver, atomic import and mixed network components
already support explicit A owners; the existing actual-A reciprocal adapter is
a fixture-specific integration instrument, not this ordinary public client.
Consequently a separately selected **explicit A-capable public-client seam**,
preserving fixed I-only mode and exact concrete owner/profile checks, has higher
immediate value than an unfunded full proof or another passing I-client replay.
It needs no new checker, generic plugin registry or fabricated authority.

Recommendation: finish the cheap genuine preflight, then progress that bounded
source integration while resolving producer capacity and complete-path economics.
Reuse the existing actual I import/publication/cold-admission evidence and the
planned genuine-A boundary instead of creating duplicate campaigns. Eliminating
an optional composite finish check may simplify a workflow contract under the
existing recursive assumptions; it neither removes the dominant segment/lift/
join cost nor establishes proof-backend correctness. Full v5 remains open.

## Genuine preflight: exact source and finite-selection clearance

Complete source read: `software/v5/aggregate_resources/preflight_actual.py`,
21982 bytes, SHA-256
`07b8fc63269f8033885747554c99a60e0682cacd54c040f1d7f3c26605eb6a15`.
The adapter constructs the actual retained owner, invokes its real `_request`
exactly once, and closes it. No `run`, host, proof or guest call occurs. The
only subprocess-library use is pure Windows command-line quoting.

Both producer package pairs are pinned to actual imported source snapshots,
including package markers and `R.P is P`. The stage host and snapshot host stay
distinct. All nineteen hard-coded record hashes and seven asset hashes/sizes
match retained files independently. The explicit runtime-selection gate covers
every existing-input binding before the genuine constructor; returned owner
installation/request maps must be subsets of those exact pins plus the selected
package sources. The retained support manifest supplies exactly three pinned
helper imports. Constructor/image/build/snapshot checks are neither mocked nor
replaced by this adapter.

The saved profile/request are a private **unfunded quote**. Its identifier is
derived with `NOT_A_PROOF_ALLOWANCE`; the designated production directory must
remain absent, no stage reservation is created, and results explicitly deny
mathematical admission/proof funding/memory sufficiency. Existing base-I cost
includes its carried prefix and adds the selected build/capsule costs only;
the report explicitly preserves excluded earlier work and nonexhaustive tails.
Initial/final/post-result identity checks include inputs, sources, selection
and generated controls. Final failure overrides provisional PASS; a late failure
is retained in `FINALIZATION-FAILED.json`. The adopted outer runner separately
checks its selected source/runtime/selection closure and physical Job result.

Exact selector `Select-RealProducerPreflight01.ps1` SHA-256:
`858881ec9dbab8a0ca3329458c06861cfe9b9650a7bd7b04eab267e9999e24ab`.
Exact selected JSON `real-producer-preflight-01-selection.json` SHA-256:
`fdea3df7cacef0dd38abc578fd3b21672a2f4fae8648729a92fc0f742945b70c`.
Independent checks match all **six sources /100864 bytes** and **51 runtime
pins /133174462 bytes**. The runtime closure is nineteen records, seven assets,
nineteen retained template pins, three manifest helpers and three build source
snapshots. The expensive compiler/link inventory is not rehashed by this run.
The run root and prospective production root were both absent at review.

The finite outer allowance is30 CPU/90 wall seconds,512 MiB, two processes and
1 MiB each log. Two processes accommodate the retained embedded-Python launcher;
no inner native work is allowed. Adapter evidence is separately bounded by
12 MiB/64 entries. These are unrelated to the hypothetical8192 MiB proof ceiling.

**Source and exact finite-selection review PASS.** This supports root selecting
the one private preflight, not a proof run. The other reviewer independently
owns the full-path serializer/argv reasoning; actual saved-outcome audit follows.

### Prelaunch wall-quote correction: selection01 remains unrun

Root identified a real omission after the above binding review: assigning every
stage600 wall seconds quotes204000 worker-wall seconds against86400 whole-wall
seconds. The actual `_envelope` does not test cumulative wall. Its current true
field must not be represented as guaranteeing that all quoted stage maxima fit.
**Do not launch selection01.** Root is selecting one small correction to the
still-unused adapter and a fresh exact selection, preserving selection01.

The independently proposed per-kind wall caps420/150/150/600/120 sum81930
seconds, leaving4470 seconds for controller, transitions and finalization.
Those residual seconds are available planning headroom, not a proved upper
bound on that overhead or actual proving time. The corrected report should
state the worker-wall sum and headroom separately. My clearance above covers
the source binding/no-launch seam; launch clearance awaits this narrow diff
and the renewed exact selection.
The reviewer's initial message incorrectly said2070; root corrected the
subtraction to86400-81930=4470 before execution. No separate reserve was chosen,
and the3600 CPU-second controller cap must not be treated as a wall-time bound.

### Corrected source and exact selection02 clearance

Corrected adapter:22623 bytes, SHA-256
`4720822d4174c2808db57972046cd23b16189fd6769981d36811540e9f918f27`.
Reversing only its new wall-cap map/use, cap-sum assertion and three reporting
fields reproduces the exact previous21982-byte source hash `07b8fc63...`.
The independently calculated worker-wall sum is81930 seconds; the raw remaining
allowance is4470. The report explicitly denies that this proves overhead fits
or that the operation completes. All genuine-adoption/no-launch paths remain
identical to the reviewed predecessor.

Fresh exact selection02 SHA-256:
`0e6cbd6e160ad1a0753b9b013ad73c2387b6d00fa234f04d7d187a89c0986b3a`.
Selector02 SHA-256:
`612bc9ca0effa391717fa98d04677dfeee875d44b003f87f8bc20e11a3c15edb`.
Mechanical comparison shows that both selector and selection differ from01
only in the operation name and adapter hash. The51 runtime pins, argv and
limits are unchanged; the earlier133174462-byte input verification is reused,
not repeated. The six-source size becomes101505 bytes. Run02 was absent.

**Corrected exact source/selection02 review PASS.** Root may select this one
genuine no-launch preflight. Selection01 remains unrun and preserved. Actual
saved outcome still requires review; no proof allocation follows this clearance.

## Genuine preflight02: actual saved-outcome audit

Run: `experiments/v5-local-checks/real-producer-preflight-02` under selected
`0e6cbd6e...`. This review inspected saved data and source bytes only; it did
not repeat the operation or import/execute product code.

| Saved output | SHA-256 |
|---|---|
| Outer `RESULT.json` | `df9bbc12b877f5f8cb75fa2a7993bfa6d9d2c5228be77275400eaac403b189da` |
| `evidence/RESULT.json` | `281a8915bcb2e3655237a25071c23cc3812418edc04d28e1655220ec1fcbb716` |
| `evidence/profile.json` | `fde140246ce4dac7be3cc12b01a0e614c4066e43304a36c806a7f3dc4589763e` |
| `evidence/prospective-request.json` | `31ea5c042a4f465c8fca06f196cd862539cf6b8bbe6b436b094c310837b3a57a` |
| `evidence/input-map.json` | `ca7a2568d76a3fdcf388736b73ffa71ac343f29a42b87fdaec5de5efe20e06a5` |
| `evidence/argv-envelope.json` | `f4be5c23d1457fa764ba77c57c0cdabc21d6b8db67e649442ad57cf5a977d00b` |

All six originals and six source snapshots match the selection. The saved51
existing-input map has exactly the selected paths, hashes and current lengths;
the reviewed runtime checks and final checks reused those same identities.
Both package source-pin pairs name actual snapshots. Independently reconstructed
installation-pin total is **88803499 bytes** and request-input total is
**46014379 bytes**, exactly the reported values and independently below512 MiB.
The saved profile's file hash equals the owner's reported profile identity.
Parsed stdout and the saved inner result are equal.

The reviewed actual path reached genuine constructor, genuine private request
and `preflight_complete`; no adoption boundary was mocked. It reports
`PASS_REAL_ADOPTION_AND_REQUEST_PREFLIGHT_ONLY`, final binding true, null errors
and no finalization sentinel. The prospective production directory remains
absent. The request has zero retained checkpoints/prior attempts, a quote-only
identifier and the corrected finite planning caps. No native stage, host,
guest, receipt or mathematical admission was produced, and proof funding is false.

The actual quote contains113 segments,113 lifts,112 joins, one resolve and one
finish:340 host calls/339 proving stages **if separately funded in future**.
The saved340 argv rows have maximum17962 UTF-16 units including NUL at finish,
with128 arguments. Worker-wall cap sum81930 and raw slack4470 are independently
recomputed. Other static quote values agree with the reviewed source, including
249250 worker CPU seconds,940048384 output bytes,2724 entries,99141167 maximum
host-read bytes and conditional59468186-byte complete-composite bound.
None of these is an actual proof-size, memory, runtime or completion guarantee.

The retained carried subtotal independently recomputes to128034.046875 worker
CPU seconds,696.609375 controller CPU seconds and13045.632040200057 summed
active-wall seconds using the original floating-point arithmetic. It includes
base-I production/prefix, the selected stage-host build and retained capsule
operation only; earlier excluded work stays preserved, not free. It is not a
fresh charge or a full-project cost result.

The outer Job exited zero, direct child reaped, Job closed, zero active or
terminated processes, no cleanup errors and no termination request. Stderr is
empty. Actual peak private commit is31846400 bytes. New observed cost is
**1.0625 inclusive Job +0.40625 wrapper =1.46875 known CPU seconds**, with
**1.7554457001388073 wall seconds**. The inner0.765625 controller CPU observation
is nested and is not added again. Final run census is184767 bytes,24 entries,
16 files; no production output directory exists.

**Actual outcome PASS for genuine no-launch producer adoption/request
integration.** Reuse this evidence. It removes the known record/schema/path
obstruction cheaply; actual proof capacity, proof economics, public A-client
integration and full v5 remain open. No repeat preflight or proof allowance is
selected by this review.
