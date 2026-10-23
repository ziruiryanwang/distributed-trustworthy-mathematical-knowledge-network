# Ordinary library extraction support: independent review

2026-10-23, `practical_path_audit`. Canonical guard passes. Source-only review
and read-only retained-data comparisons; no imports, tests, builds, owner opens,
native/network activity or Git operations. Earlier completion/resilience review
is frozen and is not expanded here.

**Current outcome:** file-only assembly passed, but actual preparation controls01
failed on a retained-helper basis-tag bound. Frozen source is not operationally
qualified for retained reconstruction. Diagnosis and minimal successor scope are
recorded below; earlier source clearances are preserved, not runtime passes.

## Practical question and acceptance boundary

An author has already produced an inert candidate that cannot yet be admitted
because the selected receiver lacks some library declarations. The next useful
step is to recover its retained preparation and extract the actual missing
closure, not ask the author to reconstruct maps manually or recompile successful
source. The original candidate and real protected parent remain authoritative
inputs to the existing binder; neither retained metadata nor extraction confers
mathematical acceptance. The existing completion/admission path stays unchanged.

## Retained preparation: PASS source clearance

Read `software/v5/ordinary_library_support/retained_preparation.py` completely,
its design note, the relevant original contribution writer and V2 preparation
producer. Source SHA-256:
`f4c51f1a90a75eb153dda10c6c17b9a8eeeca1692275c176f70a15f8499a9bc6`.

`reconstruct_preparation` is pure. It requires bounded inert request/header/
group/target bytes and a stable genuine-parent lookup. It checks the selected
S/F/root, exact sequential file set and byte/hash pins, canonical header/group
formats, 581 basis rows, portable basis IDs, disjoint group bindings, prepared
target membership and fresh output names. Every returned name/ID is checked
against the actual selected parent's lookup. Nothing installs the retained
types, theorem assumptions, definition bodies or purported acceptance flags.
The frozen result contains immutable canonical-name bytes and explicit hashes,
counts and `mathematical_acceptance=False`.

Read-only comparison against actual retained
`experiments/v5-local-checks/ordinary-peer-reciprocal-02/B-contribution` confirms:

- REQUEST has the exact 13 required fields; a project-backed record may add
  only the separately ignored `project_authoring` metadata field.
- The header is `DMKN_OWNER_REQUEST_V2`, with seven expected fields, 581 basis
  rows, one prepared target and two groups.
- Group0 has one mode1/body5 definition row and one three-element unit; group1
  has one mode0/body2 theorem row and no unit. Both retain the V1 group grammar
  marker while using portable V2 IDs. This is the actual producer's layout,
  not a legacy identity conversion.
- All request-file pins, target pin and 694,879-byte aggregate payload agree.
  The reconstructed row census would be 583 bindings. The helper itself was
  not executed and these data checks do not validate the protected callback.

Fixed caps bound metadata/header/group parsing, aggregate bytes, names, lookup
count and returned map bytes. The caller's callback is checked around bounded
parses/hashes and throughout name loops; failures propagate without allowance
renewal. Standard JSON decoding and individual canonical-name operations remain
bounded but not internally preemptible. This is consistent with the existing
cooperative controller boundary, not a hard CPU/memory sandbox.

The public caller must separately pin the chosen REQUEST and candidate, acquire
only the declared bounded files, and bind the exact candidate with this recovered
map against the same actual parent. A REQUEST hash does not prove historical
compiler execution. Unused diagnostic fields need not become trusted claims;
recovering IDs does not require rechecking projected theorem bodies.

No source blocker found for this helper. Its costs scale with the selected
retained payload and bounded name set, plus genuine-parent lookup costs; this
does not establish that `catalog.context` materialization is sublinear in the
entire selected context. No new experiment or large-scale claim follows.

## Public API and owner/loader: source result

Read the complete root `library_extraction.py`, `owner.py` and `profile.py`.
The API rechecks exact REQUEST/candidate pins, reads only explicitly numbered
bounded files and reconstructs the map against one actual parent context. The
unchanged binder derives the missing names before native work. Existing candidate
units are preserved; there is no reauthoring, automatic admission or parent rebase.
The exact previously built 697,344-byte exporter must be in the verified profile
and match SHA9700c6c2. Its replies are still checked against genuine parent IDs;
DONE counts, missing-name lookups, supplement boundaries and the unchanged
combined completion planner gate the returned inert inputs.

One concrete source defect was found and fixed before use: formal Lean names
can contain `..`, path separators or numeric components. Testing only the first
component `Std` did not imply installed-Std path containment. The actual Lean
`Util/Path.lean` `modToFilePath` joins string components as paths, and the old
exporter only checks the `Std` name prefix. Revised `selected_modules` requires
1-16 string components, each 1-64 ASCII identifier characters matching
`[A-Za-z_][A-Za-z0-9_]*`, with no Windows reserved components. This also prevents
numeric-component import panics without constraining theorem names themselves.
The check runs in the public facade before owner opening and again in the API.

The revised API also refuses provably futile extraction when consumer units
already occupy all 32 admission slots or candidate bytes exhaust 4 MiB. This is
an economical precheck, not a claim that the existing native binary enforces
the smaller remaining budget. Oversized actual production still refuses before
completion. The binary retains its larger fixed caps and module-load costs.

The public facade adds only explicit `extract-std` arguments and dispatch, with
input pins/module parsing before owner opening. Semantic preparation still
occurs afterwards; ordinary open/recovery is not promised read-only. Existing
`complete` remains separate. Its output files and returned pins are directly
compatible with the complete-only arguments. Original parent allowance checks
cover preparation, support verification and cleanup. Finite measured native CPU
is charged once; unknown accounting is explicitly null plus the whole reserved
CPU charge, not measured zero or permission to continue.

The loader adds exactly three Python helpers and the fixed exporter, including
an exact census of the new binary directory. It preserves the native admission
installation and shared modules. Installed Std transitive private/IR artifacts
are owner-trusted local support, not completely hash-authenticated by named
runtime pins. This endpoint does not accept peer binary modules or establish
Mathlib/arbitrary-project compatibility.

## File-only packaging: source result

Read complete `assemble.py` and `select_assembly.py`. The overlay replaces
owner/loader, adds three helpers and the existing executable, and preserves all
other completion/resilience/native payloads. Expected base owner/loader hashes
match the already assembled library profile. The executable is an exact runtime
pin, not treated as a text source snapshot or rebuilt. Source/runtime/copy/final
pins, fresh destination and profile-last commit remain. The selector and assembler
agree on finite90wall/50CPU/512MiB/2process outer and60wall/40CPU inner allowances.
There is no state open, native extraction or build in the assembly operation.

## Interactive supervision: corrected source clearance

The initial exchange source correctly placed the native child in a suspended
launch before Job attach/resume and used bounded queued IPC with short idle
budget polling. Review found one accounting defect, also independently reported
by root: failed Job assignment after successful process creation could leave an
empty Job with final zero CPU and wrongly label native accounting complete.
That Job does not measure the unassigned process. A source correction must mark
such accounting unknown, retain cleanup uncertainty and trigger the caller's
conservative charge. The initial generic stdout grant also did not describe its
larger fixed protocol cap; root requested explicit matching limits.

Read the complete initial exchange and final corrected boundaries at
SHAf6d0ee89. Created-child finite accounting now requires a final zero-active
Job containing at least one process and the direct child reaped. A created but
unassigned process is unknown, not zero. No returned process is separately
known-zero native work. Final measured Job CPU is added once even on failure;
unknown accounting poisons the budget with infinity, while the serializable
report retains null and the high-level API conservatively charges the reservation.

The same selected Job backend is constructed before suspended Popen; attach/
resume precedes pipe threads. Polling occurs every at most0.05s while idle or
waiting for writes/exit. Every controller poll checks original parent and local
allowances plus sampled Job total CPU. Active work reserves cleanup inside the
original deadline; cleanup never renews the grant. Faults kill the Job and the
direct child as needed, wait for reaping, join/close pipes, quiesce and close the
Job. Unjoined threads, retained late thread faults, unconsumed protocol events,
nonzero exit, active descendants, failed closure or missing accounting all refuse.
Normal success additionally requires DONE, both EOFs, zero termination and final
allowance checks. Report-write failure also refuses without erasing charges.

Sequential echoed names, memoized unique real-parent replies, frame bounds,
at most65,536 lookups, exact DONE fields and the combined32MiB protocol ceiling
remain. Actual stdout is additionally capped by the original stdout allocation,
stderr by min(1MiB, its allocation), and stdin by `budget.log_bytes`; their limits
are now explicit in the report. The ordinary default therefore does not promise
32MiB useful throughput. Queues are bounded. Native output has the trusted
exporter's fixed64MiB cap and is checked against the smaller remaining public
completion capacity afterward; no hard filesystem sandbox or global-size bound
is inferred from the process-memory limit.

The source-level containment/accounting argument depends on the selected Windows
Job backend and OS, trusted callbacks and normal bounded file/pipe operations.
Controller enforcement remains cooperative and needs an outer supervisor for hard
controller limits. The changed failure branches still need focused controls.

## Disposition

**PASS source clearance for the selected helpers/API/owner/loader and one finite
file-only assembly by root.** The original module-path and empty-Job accounting
defects were corrected before selection. No build, native extraction, admission
or test run is authorized or claimed by this reviewer. Later runtime selection
requires its separate finite changed-boundary evidence. The workflow supplies
inert completion inputs, not mathematical acceptance or final-v5 readiness.

## File-only assembly01: independent saved outcome

Read retained selection/RESULT/ASSEMBLY/stdout/stderr for
`experiments/v5-local-checks/ordinary-library-support-assembly-01`. Independently
checked all nine source snapshot hashes, all122 payload lengths/hashes, the exact
124-file census including PROFILE/ASSEMBLY, and the base/new mapping. Exactly
owner.py/profile.py are replaced, three helpers and the existing executable are
added, and116 base payloads are unchanged. All four non-file profile fields,
installation identity32236aa3 and native implementationfafc8387 are unchanged.
The copied executable has the previously selected697344bytes/SHA9700c6c2.

Selection:
`e2f50cc0a8bbf45fcda6c8a670077dc50a30b4b9753b95cdd7a05a6fd927f576`.
New profile:
`1801fee2c3e9e39cef35182478acc693c923fef32ebb47ae2d7099d9a7776d3e`.
Payload total37,450,710bytes. Exit0/empty stderr/clean child reaping and Job
closure, zero active or terminated descendants. Cost:4.5661079wall,
1.546875Job+0.609375wrapper =2.15625 known CPU seconds;
27,074,560-byte peak private. No state/native extraction/build occurred.

**PASS for this file-only assembled package.** New-loader and extraction
behavior are not yet executed by this assembly; no mathematical acceptance,
ordinary-project compatibility or release claim follows. Used sources and this
assembly are frozen. Focused preparation/protocol controls are separate work;
none was run by this reviewer and no repetition is recommended.

## Preparation controls: source clearance only

Read complete `preparation_controls.py` SHAea988574 and shared
`select_validation.py` SHA7742160b. Independently checked all six retained
B-contribution file hashes named by the runner. The seven groups use actual
retained bytes and the real helper/module selector with an explicitly
fixture-derived mocked parent, not a live catalog or new warrant. The successor
profile is loaded once. Guards prohibit database access, subprocess creation,
native extraction, real owner/admission and peer connections.

Expected refusals were checked against the selected code ordering: metadata
duplicate/depth/numeric cases; changed target/header pins; exact file/census
mismatch; legacy or wrong S/F/root headers; unwarranted/duplicate bindings;
wrong prepared targets and duplicate/colliding outputs; per-file/aggregate and
4096-binding caps; cancellation and bad lookup types. The synthetic cap rows
reach the aggregate binding refusal before stale target metadata matters.
Module controls exercise the corrected traversal/separator/numeric/reserved/
non-ASCII boundaries. CLI controls test pre-open argument/pin refusals and exact
forwarding/closure with explicit mocked success/failure. The synthetic0.25 charge
is only a forwarding assertion. The argument loop preserves its helper names.

The preparation selector pins the package/runtime plus six retained fixture
files, with argv matching the runner. Its60wall/35CPU/512MiB/2process outer
encloses the runner's50wall/30CPU limits. **PASS for one finite native-free
preparation control selection by root.** No run is performed or predicted by
this source review. The shared selector's protocol branch is not yet cleared:
its separate runner must be reviewed before any tiny-child/Job experiment.

### Actual preparation controls01: failure and exact diagnosis

Read retained RESULT/seven-group report/stdout/stderr and verified all three
selected source snapshots for `ordinary-retained-preparation-controls-01`.
Selection:
`0fe94ad4dd367308b213e8e6dcadf02088968aa2fe118c8557ce3d322ca78016`.
Groups1,3,4 fail with `INTEGER_BOUND` or the resulting wrong-refusal assertion;
groups2,5,6,7 pass. The run is FAILED, not a partial compatibility pass.
Exit1/empty stderr/clean reaping and Job closure, zero active or terminated
descendants;3.4509317wall,2.5Job+0.65625wrapper =3.15625 known CPU seconds,
61,308,928-byte peak private. No owner/native operations occurred.

The defect is in `retained_preparation.py:211`: `E._uint(row[1], 6)` applies the
ordinary exported-unit kind bound to a **basis inventory** row. The original
`BootstrapSupport.lean` inventory encoder has tags0..7 and explicitly encodes
`.quotInfo` as7; its decoder accepts7 as quotient metadata and rejects other
unrecognized tags. The actual fixed header contains four tag7 rows: `Quot`,
`Quot.mk`, `Quot.ind`, `Quot.lift`. Its full census is0:3,1:267,2:132,4:53,5:67,
6:55,7:4. Reconstruction therefore fails before the intended positive/identity/
aggregate-cap conditions. This is a genuine helper compatibility defect, not a
test-fixture failure. Both root and reviewer independently identified it from
retained data. The earlier review checked the actual group shapes but missed
this basis-versus-export kind-domain distinction.

Minimal justified repair: a fresh helper successor changes only this basis
upper bound6->7, with an explanatory comment if desired. It must preserve exact
portable IDs/protected lookups and leave ordinary exported-unit kind<=6 unchanged.
No broader semantic policy or fixture weakening is warranted. Used helper01,
assembly01, runner and failed evidence stay frozen; no rerun or edit was performed
by reviewer. Successor source/assembly selection remains root-owned.

## Protocol controls: source clearance only

Read complete `protocol_controls.py` SHAde8b02fb, its source note and shared
selector's protocol branch. Five small real-Python child cases use the actual
installed exchange and selected Windows Job: normal two-name FOUND/ABSENT IPC,
wrong initial sequence, trailing frame after DONE, idle cancellation and a last
explicit preassignment failure. The last case creates a real suspended child
but deliberately never assigns/resumes it, while delegating Job stats/kill/close
to the real backend. This directly targets the corrected empty-Job accounting
branch; its reservation is separate from measured native CPU.

Exact argv/environment/cwd/suspended flags are asserted before the single child
launch in each case. All children take an early script branch without package
imports; there is no Lean/exporter, supplement or owner operation. SQLite and
peer networking/admission are guarded. The actual parent source is rechecked.
Error cases require their exact code and cleanup, not any unsuccessful result.
Every case checks persisted report equality, direct reap, closed Job/pipes,
joined threads and zero active descendants. Normal success checks exact counts
and transcript byte accounting. Idle cancellation starts after live IPC and
requires local subsecond observation; this is not a universal scheduling bound.

One70wall/30CPU parent allowance includes controller and measured children;
each30wall operation preserves the original deadline/cleanup reserve and uses
remaining CPU,128MiB/two-process inner limits and4096-byte stream caps. Charged
unknown preassignment work is last; failure stops later children. The shared
selector's90wall/40CPU/512MiB/four-process outer envelope and argv match this
runner. The fixed profile1801fee2 is intentional: the retained-preparation bug
does not execute in these IPC controls and does not require repackaging this
unchanged exchange. Its failure is not excused or qualified by this separate test.

**PASS for root's one finite protocol-control selection.** This is distinct
from source repair/preparation controls and from actual native extraction;
none of those outcomes is inferred. No test or child was run by reviewer.

## Retained-preparation support02: narrow successor source clearance

Independently read the complete helper and controls under
`software/v5/ordinary_library_support02`, plus its assembler and both selectors.
Read-only exact-text comparison confirms the helper differs from frozen01 by
only `E._uint(row[1], 6)` becoming `E._uint(row[1], 7)`; both are11011bytes.
The four quotient IDs/subkinds in the new control independently match the
actual retained header. New assertions require exactly581 basis rows/four
quotient rows, recover their exact IDs, and reject a repinned tag8 header.
All seven prior groups and the explicit mock-parent boundary remain.

The fresh assembler overlays only `authoring/py/retained_preparation.py` on
support-assembly01. Its base owner/loader pins, full input/final copied-file
checks and unchanged installation/non-file profile fields are retained. It
does not rebuild the exporter or open a catalog. The selector snapshots five
sources and pins the base/runtime inputs; the same90wall/50CPU/512MiB/2process
outer and60wall/40CPU inner assembly allowances remain. The preparation
selector retains the six exact fixture files and60wall/35CPU/512MiB/2process
outer allowance. Its inherited protocol branch is not selected: protocol02
uses a separately reviewed runner/selector, not a missing support02 runner.

**PASS source clearance for root's one file-only support02 assembly and its
fresh preparation controls, in that order.** This neither predicts a passing
run nor authorizes native extraction. Preserve failed01 and all used bytes.

| support02 source | SHA-256 |
|---|---|
| `retained_preparation.py` | `49e9550f9d1d231654ef120b7fac8194d9d6707690675c1f0baa96be6463ddb3` |
| `preparation_controls.py` | `fcc401ed42c01b6c8a8b842101a3dab3079c920353557b58bc55aa0107368720` |
| `assemble.py` | `49ca5900b7338d69f7a228ec110298a2883931ac0d1222ff7f4e7b8037323c0f` |
| `select_assembly.py` | `a92f180a0d46fead50b5ea192638ae71c14092c3f82bc9c5a45ef996b2e303b7` |
| `select_validation.py` (preparation branch only) | `f259a5a1a45a17bcb8736cd933a40f0438cbeee187fc458706bbc88926349906` |

## Actual protocol controls01: preserved fixture-census failure

Read retained RESULT/PROTOCOL-CONTROLS, exact success transcripts and inner
supervision report for `ordinary-extraction-protocol-controls-01`; independently
verified all three selected source snapshot hashes. Selection
`06eb81fe611ad258f680ef44e524502008964597547c4338e93bbcf31e6f48ee`.
The run failed its first scenario with `PROTOCOL_CONTROL_MEASURED_JOB_CPU` and
did not attempt the other four. Exit1, empty outer stderr, clean reaping/closure,
zero final active/terminated descendants;1.5350383wall,
0.796875Job+0.484375wrapper =1.28125 known CPU,36,474,880-byte peak private.

The exchange itself returned `EXTRACTED_AND_CLOSED`, direct exit0, attached and
resumed, closed Job, joined threads, no cleanup errors or termination request.
It returned exact FOUND/ABSENT replies for two names and exact DONE counts;
three stdout lines/two stdin lines total783bytes, including403stdin bytes.
The final Job measured0.046875CPU seconds (0.03125user+0.015625kernel), exactly
the reported/charged native CPU. Its total process census was2, active0,
terminated0, peak private10,055,680bytes, wall0.1171037seconds. The fixture
required total==1 although the selected inner grant permits two active
processes. The pinned ordinary Python3.14.6 executable metadata does not
establish why the observed census is2; no redirector explanation is adopted.

A minimal fixture-only successor may require `1 <= total_processes <= 2`
for this finite known script while retaining exact argv, successful attachment,
CPU equality, final active0, direct reap, closed Job/pipes, joined threads and
all preassignment-unknown-cost controls. The upper bound is a prospective
fixture requirement, not an OS theorem equating cumulative and simultaneous
process counts. This does not weaken the product Job limit or justify any
unaccounted process. Failed01 remains failed; no runtime was performed here.

### Protocol02: minimal fixture-only source clearance

Independent exact-text comparisons confirm `protocol_controls02.py` differs
from frozen01 only by the attached-case census predicate described above;
`select_protocol02.py` differs from the original selector only by its own name
and the protocol runner filename. All other assertions, five scenarios, fixed
profile1801fee2, finite bounds and early stop remain unchanged. In particular,
the injected unassigned child's total0/unknown-cost/termination checks remain.

Runner SHA-256:
`8e80bc0a5915fcdba4af484e8c4cac607242ffca286e23e8aef982552f60284b`.
Selector SHA-256:
`9ca16c8411010a2e5793a136825abdcd499eab6aefd9be85d58509926548b7cb`.
**PASS source clearance for root's one fresh protocol02 selection.** Its
read-only support01 package is intentionally independent of support02's
one-helper assembly; disjoint outputs permit concurrent selected operations.
No passing runtime result or native extraction is claimed by this review.

## Combined actual successor outcomes: assembly02, preparation02, protocol02

Read retained selections, RESULTs, complete control reports, assembly receipt,
inner supervision reports and diagnostic transcripts. Independently verified
all11 selected source snapshots (5+3+3) and three selection hashes. All three
outer runs exit0 with empty stderr, clean direct reaping/Job closure, no cleanup
errors and zero final active/terminated processes. This audit ran no controls.

### File-only support assembly02: PASS

Selection `b7baf3bdaf47bfde1ade83ba747cfbf04f6c431970f713b1dfb4e2d5e35bdbf0`.
Independently hashed all122 payloads (37,450,710bytes), verified the exact
124-file census including PROFILE/ASSEMBLY and compared all payloads against
support01. Exactly one file changes: retained_preparation.py SHA49e9550f;
all121 other payloads are byte-identical. All non-file profile fields and
installation identity32236aa3/native implementationfafc8387 remain unchanged.
New profile `e4c1734390c372f6884e14419ed1301825f1f58e98c4d0b86b4d5ac4e454c7bb`.
Cost4.2803364wall,1.59375Job+0.640625wrapper =2.234375known CPU seconds;
26,411,008-byte peak private. No native build, extraction or owner work.

### Retained preparation controls02: PASS, explicit mock-parent scope

Selection `525953ccbe58bd04b197f5246cedb1a57b34495598c65b5264084035302474cd`.
All seven groups pass against profilee4c17343, including the actual retained
quotient basis rows and new repinned tag8 refusal, original identity/capacity
controls, module-path refusals and mocked CLI forwarding. Independently
rechecked all six retained source fixture hashes unchanged. No owner/native
operation occurs; the fixture-derived parent remains explicitly mocked.
Cost7.9385476wall,7.09375Job+0.578125wrapper =7.671875known CPU seconds;
63,348,736-byte peak private. This establishes bounded helper compatibility,
not a live protected-parent reconstruction or mathematical acceptance.

### Extraction protocol controls02: PASS, real process/IPC scope

Selection `8a60d8a4adb96c20781145cbe68401d0a37523cf49ca11bd996d3d74f3eb9e60`.
All five scenarios pass against unchanged profile1801fee2. Independently
checked the five retained report hashes and exact success/fault transcripts.
The success path has exact FOUND/ABSENT/DONE messages and clean exit0. Wrong
sequence and trailing frames refuse with their exact expected errors. Idle
cancellation is observed with cleanup0.0926149seconds after its scheduled
trigger. All four attached cases have total2/active0 and exact Job/native/charge
CPU equality, totaling0.15625 measured child CPU seconds; all close/reap/join
without cleanup errors. This is a finite local observation, not a universal
latency or process-lineage theorem.

The injected preassignment fault has total0, no attachment, direct child
terminated/reaped, closed Job and joined threads, with native CPU null and
accounting_complete false. Its full original28CPU-second reservation is retained
separately, never mislabeled measured CPU or zero-cost work. The outer Job's
known measured aggregate covers the whole harness tree; do not add its nested
measured costs again or add that conservative inner reservation to actual CPU.
Outer cost2.1924904wall,1.03125Job+0.5wrapper =1.53125known CPU seconds;
37,457,920-byte peak private. No Lean exporter, owner or mathematical checking.

**Adopt these three scoped outcomes; retain both failed01 operations unchanged.**
The next meaningful boundary is the separately selected live-parent native
extraction/completion workflow, not repeating these controls or claiming v5.

## Reviewed source identities

All paths below are under `software/v5/ordinary_library_support/`.

| Source | SHA-256 |
|---|---|
| `retained_preparation.py` | `f4c51f1a90a75eb153dda10c6c17b9a8eeeca1692275c176f70a15f8499a9bc6` |
| `supervised_library_exchange.py` | `f6d0ee89d792f3741f74c790914dc8e21cf21dc7ca256bb03360dbc31907dea4` |
| `library_extraction.py` | `5a71037c38513eb84e588ec571d7cddded316f3eb4561c31bc46c50f72a8f683` |
| `owner.py` | `b2ee459feada64e94bf2185bcec0a8ab943908c3779450d05efbdaa590f45990` |
| `profile.py` | `2775cc62d1a8d8a85858de93ce4019485df852b3518b57a82ed2e410c7cce17b` |
| `assemble.py` | `16ad6f395ff52406ef39c2f19ea610d9e53f4867f3007dcea35e84a24d592b79` |
| `select_assembly.py` | `77a6c1bc39d3f877967d1bd824de8d740a309638206ea2b44687c0c4ed016c90` |
| `preparation_controls.py` | `ea988574466558c513e17a6e2f311fa1313cfab160c834c889bdee3de3685122` |
| `protocol_controls.py` | `de8b02fb654fc35f284474d325ce9934d1023df8369debedc8474635ea733ff0` |
| `select_validation.py` (both branches, separately scoped above) | `7742160b65bf6bbdfea36ec213884049fa7c4578eff9f13ab4a0c924a2083a28` |
