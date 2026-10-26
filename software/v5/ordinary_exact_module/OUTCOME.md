# Independent saved-output audit: exact installed vocabulary

2026-10-26. Reviewer: `update_trust_lifecycle`. Read-only saved source/data audit;
the reviewer launched no product, native, test or owner-state operation.

## Native elaboration01: PASS, no main execution

Run: `experiments/v5-local-checks/exact-module-typecheck01`.
Selection SHA-256:
`e06d20ec5861eaccd712246a737cbe9aa122644b39aabd08cacf2c4ee1f3fcfe`.
Saved `RESULT.json` SHA-256:
`a63956c3dbb89ac9b80a38ea78255f402d2a588d41ee013482173b2962024711`.

Independently recomputed all three saved source snapshot hashes and the saved
selection hash; they equal the source-reviewed selection. Read the saved command,
stdout, empty stderr and final enclosing report. The actual command has exactly
the reviewed snapshot wrapper/native path and native source digest. Stdout says
`ELABORATED_NO_MAIN`, exit code zero, source
`54f36991e4707b487a21f237e0854f6bd4127c2c2da805440c6119abf7cfd3d5`.
The outer report records `COMMAND_EXITED_ZERO_AND_CLOSED`, direct child reaped,
Job closed, zero active processes and no cleanup errors or termination request.

Measured enclosing wall time: 3.7036247002 seconds. Inclusive Job CPU:
3.3125 seconds; runner CPU separately 0.53125 seconds, known combined 3.84375
seconds. Peak Job private commitment: 645,476,352 bytes. Four total processes;
stdout 135 bytes and stderr zero. These are selected local observations, not
hermetic-toolchain assurance or a certificate-production cost.

Root records an earlier relative-selection invocation that refused before any
selected snapshot/output/child was created; this audit's PASS covers only the
saved exact elaboration above. It does not invent a second native attempt or
erase the invocation error. No mathematical request, owner mutation, module
export, private/public import compatibility, warm reuse or v5 release follows
from successful elaboration. Subsequent tests remain independently selected.

## Focused inert controls01: PASS, 43 cases

Run: `experiments/v5-local-checks/exact-module-controls01`.
Selection SHA-256:
`cc30f101cb41952dd4ef1c76353baa0acfa0278f4656c9dd16ff9dc8abb4fb7e`.
Saved outer `RESULT.json` SHA-256:
`594d877589c97fba20956dfe2fd006f21df98a817d2dc0b7e289ff28b3be0c99`.
Saved `controls/CONTROLS.json` SHA-256:
`65d8fdc9531ddd6dd88dd108f93e7ed8db557880c63c16d7c3fdc0a47406381a`.

All four saved source snapshots and selection were independently rehashed and
match. The saved control report and stdout contain the same parsed result:
43 source-reviewed cases, six positives and 37 exact expected refusals. Case
labels/refusal strings match the source, including mixed theorem/definition/group/
opaque partition, malformed index/accounting controls, descriptor mismatches,
request-derived tags, persisted family restoration, missing sibling warrant and
old-support refusal. No terminal pending file remains. The report's zero owner
opens/native operations is consistent with the guarded reviewed source; invented
records/artifacts remain inert test bytes, not live warrants.

Outer command exited zero and closed; direct child reaped, zero active processes,
no cleanup errors or termination request, empty stderr. Wall time 1.2905271999
seconds; inclusive Job CPU 0.40625 seconds plus runner 0.65625, known combined
1.0625 seconds. Peak Job private commitment 27,525,120 bytes, two total processes.
This is metadata/record-seam evidence, not actual installed equality.

## File-only assembly01: PASS, complete exact map

Run: `experiments/v5-local-checks/exact-module-assembly01`.
Selection SHA-256:
`385c26f0588e773862656e558c400c5985d2861acbf84c1865e6e7615709f426`.
Saved outer `RESULT.json` SHA-256:
`8b1f9911bd1a04d14bb8db9cbd5f49e349ea2e710994a3d4fca35a4bbe43b9bf`.
Saved `assembled/ASSEMBLY.json` SHA-256:
`9e3d68f7f0fd0a90778b6c95a2aafadc44b016d9122c3b657cb0de7c4b0bcba5`.
New package PROFILE SHA-256:
`bde63019d1a6ac2bccd8e0c245a405ad3ca551d0606c01a5193fee6897c60346`.

Independently rehashed all eight source snapshots, saved selection and all files
in both base and output packages. Both have exactly 154 files with the same path
census. The only changed paths are the three reviewed payloads and PROFILE;
all 150 other payloads match the base exactly. The new package totals 39,139,190
bytes. Its 117 auxiliary pins, three overlay pins and 27 local installation
payload pins all match, as do the nine separately located runtime pins after
their declared runtime mapping. External runtimes are intentionally not copied
under the package; their absent logical installation paths are not lost files.
Installation manifest remains
`32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.
The complete map, receipt counts and reviewed changed payload hashes agree.
No pending assembly receipt remains.

The saved command/receipt/stdout and clean outer report agree on the exact
file-only operation. Child exited zero and was reaped; Job closed with zero
active processes, no cleanup errors/termination request and empty stderr.
Wall time 4.9327676003 seconds; inclusive Job CPU 1.5625 seconds plus runner
0.578125, known combined 2.140625 seconds. Peak Job private commitment
17,551,360 bytes, two total processes. No compiler, native main or owner API ran.

Known combined CPU across these three completed selections is 7.046875 seconds,
including separately reported runner CPU once per operation. Inner reported CPU
is already within the Job and is not added again. Controls and assembly ran in
parallel, so their wall durations should not be summed as elapsed project time.
The exact package is ready for root's later separately selected public test;
there is still no AllClosure module, query, growth or release pass from these
three preliminary outcomes.

## Public01: PASS, exact AllClosure realization and warm reuse

Run: `experiments/v5-local-checks/exact-module-public01`.
Selection SHA-256:
`caf8c27696a4652ad739378ffd237596775c0912584eee236a58c40190bec338`.
Outer `RESULT.json` SHA-256:
`e111dfd60898684907771cd7df569cd2d3431cfcd7ad79fde4fd3813076bd0f0`.
Public `RESULT.json` SHA-256:
`319e6104ba46bcc2ae1035e6419e615def52339ce95b4bc716766f5811fa78f4`.
Cold request SHA-256:
`0d582fd771aa7e983043f1219441c0ac08f1584bf79ea965fe84b210810835ee`.
Final native report SHA-256:
`a30107f7ecc95a8e75e9fac9c8008bf940439d20da4526cc48386182a62efff9`.

All three source snapshots and all 167 runtime/input pins were independently
rehashed after execution and match. The two recorded public responses equal the
corresponding saved stdout JSON. Each MODULE manifest equals its public result
before the unchanged owner wrapper adds `manifest_path` and `supported_runtime`.
An initial reviewer assertion omitted that wrapper augmentation and was corrected
after checking owner.py; no product or outcome bytes were changed.

Read-only stdlib JSON/hash analysis independently established:

- All ten request units equal their retained source-bundle units exactly, and
  each source document hashes to the selected evidence-domain unit identity.
  The request/inventory/empty anchor-plan pins equal SELECTION. Cold acquisition
  reports ten fetches, 62,079 evidence bytes and 602 warrant lookups.
- All 21 inventory rows equal the flattened ordered request. Matched indices
  are exactly `[3,4,7,8]`: Membership group, Membership.mem, List.Mem group and
  List.instMembership. Those four units contain nine rows; the other six units
  contain twelve added rows. Full matched/added row and name partitions agree,
  not merely counts. The requested AllClosure target and exact context are bound.
- Pending and final native reports agree in every field except the intended
  schema/assurance promotion. Both bind all request identity fields. The report
  states two checking passes and 581 basis rows. The protected worker's trace
  records exactly build, reread-private and reread-exported, each started once
  and exited zero. Together with the reviewed pinned native/control source,
  this supports successful private/public checks and both fresh rereads for
  these actual units; it is not independent reexecution of Lean.
- The registered anchor is
  `79db183e7c154929cb8aca320082854ddde304466a3dd901da071aac425f9325`.
  Its raw record SHA-256 is
  `d0714947d7cd9259928d5782a0c10360a6dc3ff80efea057a561222121227005`;
  the independently recomputed record-domain hash yields that anchor identity.
  Materialization-key, support-plan and STORE bindings agree. All 21 persisted
  outputs independently match the request name/kind/universe metadata, complete
  inventory-row hash and recomputed export identity. Exactly the four matched
  units use `installed-exact-nontheorem`; all other six use `added`.
- All five module artifacts and seven event files match their registered pins
  and their public cold-output copies. Module artifacts total 19,888 bytes.
  This is a protected local module, not a transferable binary trust token.
- Warm export returns that same exact anchor and module with zero native calls,
  zero fetches and no ordered delta units. It reuses the new persisted tag
  through the public owner path. No new catalog acceptance is reported by either
  call. The warm route still validates selected context/support/metadata and
  artifacts; zero native/fetch does not mean zero cost.
  Because this warm hit invokes no native process, it does not exercise native
  restoration of a nonempty new-tag anchor plan. A substantive downstream
  query/extension can cover that separately without repeating this warm hit.

**Preservation limitation:** saved `PRIOR-SIDECAR.json` is `{}` and the reported
unchanged prior-file count is zero. Thus this run created a new sidecar and did
not test preservation of any preexisting anchor record. The native-free
old-support-refusal control remains separate evidence. There is no claimed
nontrivial previous-sidecar preservation result or silent old-record migration.

Cold native supervision is clean: zero exit, both cleanup indicators true,
zero active processes, no errors/termination request and empty native logs.
It consumed 13.671875 Job CPU seconds within the derived 35-wall/30-CPU/1536-MiB
worker allowance. Public cold response reports 16.3660356998 wall seconds,
1.640625 controller CPU and 13.671875 worker CPU; warm response reports
1.3738845000 wall seconds, 1.328125 controller CPU and zero worker CPU.

The outer selected Job also exited zero and closed cleanly with empty stderr:
19.2552430998 wall seconds, 17.265625 inclusive Job CPU plus 0.6875 runner CPU,
known combined 17.953125 seconds. Peak private commitment was 1,493,745,664 bytes.
Fourteen processes existed over the run, not simultaneously; the active cap was
eight. Inner costs are included in outer Job CPU and are not added again.
Combined known CPU for elaboration, controls, assembly and public01 is exactly
25.0 seconds under the recorded accounting scope.

This closes the demonstrated installed-nonbasis vocabulary obstruction for the
retained AllClosure closure. It does not yet execute a received-vocabulary
proof-free query, establish broad module interoperability or prove discovery/
growth acceleration. Native-negative calls still require their own exact
selection; no retry or broader campaign follows from this pass.

## Native refusals01: PASS, exact two changed-boundary failures

Run: `experiments/v5-local-checks/exact-module-refusals01`.
Selection SHA-256:
`ef64bc894ec8ffdd040b6129881c17abccaa08584b0339e76002bf4d069c17da`.
Outer `RESULT.json` SHA-256:
`cd10405c0301d35e5968c5437115d284d87be73c81ce3b316a511e0f7e116049`.
Saved `refusals/RESULT.json` SHA-256:
`86ef512bfc11fd58d7ea195a5b7b389dac5a869637e8fcbeeeadd53315261d81`.

Independently rehashed the two saved source snapshots and all 170 runtime/input
files, all matching selection. Parsed and compared each complete negative
request against the original successful cold request using stdlib data only:

- Descriptor case changes only Membership.mem's descriptor hint from `[1]` to
  `[0]`; its expected inventory is unchanged. Actual stderr is exactly
  `ORDINARY_MODULE MATCHED_DESCRIPTOR_INVENTORY_MISMATCH`, exit code one.
- Partial-group case changes only List.Mem.rec's expected inventory name to
  List.Mem.DMKNMissingRecursorNegative. Actual stderr is exactly
  `ORDINARY_MODULE PARTIAL_INSTALLED_GROUP`, exit code one.

Both saved COMMAND records identify the intended refusal and no fixture
authority. Each phase trace has exactly build STARTED then build EXITED with
code one: no private/public reread started. Both stdout files are empty; neither
case produced a pending/final native report or `.olean`/IR module artifact.
The terminal refusal report equals stdout's parsed report. No owner API, valid
new unit identity, mathematical acceptance or retry was involved.

Outer command exited zero because both expected refusals occurred, with direct
child reaped, Job closed, zero active processes, no cleanup errors/termination
request and empty outer stderr. Wall time 14.7848257003 seconds; inclusive Job
CPU 13.296875 plus runner 0.78125, known combined 14.078125 seconds. Peak Job
private commitment 1,076,559,872 bytes. Ten processes existed over the sequential
run under the six-active-process cap. Inner observed costs are not added again.

All five selected operations are now closed and independently audited within
their stated scope. Known combined CPU is 39.078125 seconds including separately
reported runner CPU. The accepted result is exact installed vocabulary reuse
for this retained concept, persisted metadata warm reuse, and two targeted
native refusals. It is not a received-vocabulary query or downstream native
anchor-plan use, broad portability, growth-speedup or final v5 release claim.
