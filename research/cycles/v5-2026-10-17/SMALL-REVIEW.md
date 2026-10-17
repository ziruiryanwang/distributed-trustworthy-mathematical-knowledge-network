# Independent small-producer implementation review

2026-10-17, `v5_growth_decision`. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
Authority: `SMALL-PRODUCER-SELECTION.md`; owner may inspect source/evidence and
edit only this checkpoint. No product edits/imports, tests, builds, execution,
proof, capacity polling or Git operations are performed by the reviewer.

The adopted design and prior disposition are in `PRODUCER-NEXT-DECISION.md`
(`33e4be91861bd97234620bc1c6148b6624db5da123bb51182e7c07c3e7ffc0ef`)
and `PRODUCER-NEXT-REVIEW.md`
(`dfa9122380a8493b1479a4d8988222accb7bbe60cc54cfaa871521f67235c58e`).
Do not repeat their full argument or old campaigns. This checkpoint records
only changed implementation findings and exact source/runtime dispositions.

## Review boundaries

| Owner/seam | Required changed-boundary evidence | Current state |
|---|---|---|
| Native hosts | N256 and distinct capsule/composite caps; strict bounded manifest parser; host-derived ordered dependencies; exact data pins; unchanged composite and final acceptance | Final source reviewed below; no blocker found |
| Controller | New profile/schema/source origins; bounded iterative graph; retained checkpoint and parent caps; actual full-path/admin accounting; manifest reservation/rebinding; preserved continuation/cleanup | Complete source reviewed below; no blocker found |
| Build/layout adapters | Exact new source/build/record binding using retained libraries; separate finite layouts; no old-capsule relabelling or silent source fallback | Source reviewed; two exact one-link selections reviewed below |
| Focused controls/API | Exercise only changed seams; exact public contract; explicitly synthetic controls; no full proof or v5 inference | Twelve synthetic test sources reviewed; exact execution selection/API pending |

Source builds and runtime need separate exact selection after source review.
No source-readiness or execution result is inferred while authors are editing.

## Build/layout adapter review

Read the complete initial coherent root-owned adapters:

| File below `software/v5/aggregate_small/` | Bytes | SHA-256 |
|---|---:|---|
| `build_snapshot.py` | 17,801 | `e3f2fa01c2c3ff0dd427fa1e2004785e2cd6ab6a7b5797246be575a98db82a67` |
| `build_stage.py` | 17,784 | `3b5ebe002fe5b4fb641c2fbe7a8ca7068789778dbc80d86aa2b69db558677eb6` |
| `capability_snapshot.py` | 13,226 | `15d17d08d3d37c66f455fe4e1e88c06607e1bdb293d13e59bb925ea3ad9242f6` |

Both builders retain the existing actual snapshot-host command and1071-pin
runtime subset, unchanged libraries/supervision/final source/runtime binding,
and one compiler-link call. Changed crate/source/output names and distinct
selection/result schemas are explicit. New host bytes are supplied by the
independently exact selected source map, not a placeholder old-host hash;
unchanged receipt source has its fixed pin. Three-source snapshot paths keep
the native host's relative receipt include valid. Bounds and source maps
remain separate from any future paired-build capacity selection.

The layout adapter adopts the actual new snapshot build through result,
attempt, exact selection, source map and command pins; it checks clean command,
no finalization override, source snapshot and executable. Retained command
record shape agrees with its checks. It keeps the actual A mathematics/input
derivation, chooses po18 and2^26, requires fresh output, N<=256,96MiB exact
capsule pin and208MiB/288-entry final output census. The adapter still requires
a separately selected enclosing Job; its subprocess timeout is not a substitute
for whole-tree resource closure. No proof or optimization claim is created.

**Adapter-source disposition: no blocking issue found in these reviewed bytes.**
Alignment with the new native result schema and controller's `_snapshot`
adoption remains pending coherent host/controller source. There is no runtime
clearance or build/layout result yet at that initial review.

## Final native sources and exact one-link selections

Read the complete initial native hosts, the strict-object parser repair and the
final pre-read reservation refinement. Final selected sources are:

| File below `software/v5/aggregate_small/` | Bytes | SHA-256 |
|---|---:|---|
| `aggregate_host.rs` | 20,755 | `6644d9a03f25a59089fd735b0e2f2229ec8940dedbe2502568dfd8c6a36d9c25` |
| `stage_host.rs` | 32,291 | `975e68dfbc8d091733cee72a18d81fb45617886585f1806fe9425cf4aa847955` |

The native implementation preserves exact same-A/typed-parent mathematics,
complete composite integrity and claim cross-checks, and final actual resolved
A/H receipt verification. N256/po18 changes session identity; no old capsule is
relabeled. Capsule/segment-sum96MiB, internal composite160MiB, parent1MiB,
checkpoint/final512KiB and unchanged general64MiB limits are distinct. Complete
finish dependencies remain all segment proofs plus the final resolved prefix.

Manifest parsing derives the ordered graph from the actual capsule and checks
exact keys, session/capsule binding, lengths, digests and checkpoint envelopes.
The author caught Serde's positional-array acceptance during self-review before
use. The reviewed repair requires JSON maps at manifest/row/file-pin boundaries,
preserves unknown/duplicate/missing-field rejection, incrementally decodes at
most257 rows, and rejects trailing input. The outer manifest caps independently
bound parser input. Native malformed-manifest behavior is not yet executed.

Snapshot StoredSegment reads share the same512MiB meter as initial inputs. Final
both-host read logic reserves current ordinary-file length before I/O, limits
the opened read to that reserved extent and requires equal returned length.
Failed/partial reads receive no refund. Snapshot diagnostics label this as
reservation accounting, not measured physical disk traffic. This does not
establish adversarial filesystem immutability or a total heap bound.

`SMALL-HOSTS.md` was read completely and agrees with these final source limits
and boundaries. Source disposition: **no blocking issue found**.

The plan-only selector `Select-SmallHostBuild01.ps1` was read completely:
2,554 bytes, SHA-256
`c549d77074eb937ce8c29e57e2c209f3d31f712674c5791bb7a586f8b592049c`.
It requires the canonical cwd and absent plan/run/attempt paths, pins the three
selected sources and copies only the fixed retained selection's runtime/limits.
CreateNew/flush preserves plan identity; it does not execute a compiler or host.

Reviewed generated exact plans under `experiments/v5-local-checks/`:

| Selection | Bytes | SHA-256 |
|---|---:|---|
| `small-aggregate-snapshot-host-build-01-selection.json` | 292,299 | `e4493418256735529f7fc19ed606ea459bf35b613b57680d2e0a31a7b858e4bd` |
| `small-aggregate-stage-host-build-01-selection.json` | 292,265 | `049129dacf8b43ea3e4a1796a26098dfb207ddbc80d5c1b49cbfde94fc71fa38` |

All exact source maps match the independently reviewed current bytes. All1,071
runtime path-to-hash values, not merely their count, equal the fixed old plan
`fde4496bea48c5682116c5f2bf7e37bf7834fb422a4abef04b43867dee709326`.
Runtime files themselves are not redundantly rehashed by this review; each
builder retains actual before/after binding. Fresh run/attempt paths were absent
when inspected. Limits are unchanged:240workerCPU/300workerwall/3072MiB/six
processes;40ordinary/60final controllerCPU/420totalwall;512MiB/8,192entries and
1MiB logs. Root selected sequential execution, not two concurrent3GiB links.

**Exact build-selection disposition: no blocker for these two separate one-link
builds within their selected bounds.** This authorizes no guest execution,
layout, proving, fallback, memory-cap increase or whole-proof campaign. A link
success will establish compilation, not that a full po18 proof fits4GiB.

## Complete controller and focused-test source review

Read the complete controller, its new initializer and root's twelve-test suite.
Controller pins are52,625bytes/SHA-256
`a2d23bcfe0b798f747d4a59330655a865a14a73cb4d635a50332fa65c75a6985`
and156bytes/SHA-256
`8226f83b753a224b57d5ef35338e437665fab72849c8f060dd61574a043ff36f`.
Read `SMALL-CONTROLLER.md` completely; source assertions agree with inspection.

The controller uses its own bounded iterative N256 graph, canonical stage keys,
actual16+m argv and quoted Windows UTF16 bound. New build adoption and nested
snapshot-build/source/executable pins match the root adapter/native schema.
Exact same session/profile/allowance lineage and prior-success retention remain;
new maxima do not renew a consumed budget. All admitted/new checkpoints retain
512KiB limits. Fixed20MiB, initial/session512MiB and separate admin128MiB
admissions are enforced. Manifests are saved/pinned before reservation/dispatch,
included in input rebinding, and bound in native stdout. The request/profile1MiB
and per-record64KiB limits are actual checks. The retained save helper and
canonical expected serializer both use ensure_ascii=True and a final LF, so no
manifest byte/hash disagreement was found at that seam.

Tests exercise real constructor/request/graph/manifest/control-flow
code with explicitly synthetic build/image/snapshot adoption and support
loader. An inert supervisor inspects the durable manifest/reservation and
returns failure without fabricating a successful proof or artifact. The suite
does not import/repeat the previous test suite. Twelve cases cover maximal
graph/closure, stage spelling, dependency order and limits,257/258rows, file
pins, constant argv/quoted bound, new profile/geometry, capsule/parent/checkpoint
caps, real synthetic retained-index validation, fixed20MiB refusal, maximal
quote/exhaustion, and durable manifest failure accounting. The source pin under
review is `test_small.py` SHA-256
`2fb4cdd4ae165a51e532493f72111093664e88a2a348ecf687c95cf6c8a4ae54`.

**Controller/test source disposition: no blocking issue found.** The tests do
not qualify the native JSON parser, actual proof production or public v5.
Admin64KiB/128MiB refusal has source enforcement but no dedicated executed test
in these twelve controls; this coverage boundary is not hidden by the suite's
claims. Exact test selection and actual outcomes require separate review.
The native stdout/controller echo contract was source-reviewed only: the twelve
controls do not call the success `stage_output` path because the inert dispatch
returns FAIL. No successful-output validation execution is claimed.

## Exact focused-control selection

Read `Select-SmallControls01.ps1` completely:2,375bytes/SHA-256
`4021466c89c99068152a346c99a5f3032df840339c704afde6818f7f18ef5acf`.
It checks canonical cwd/fresh outputs, preserves the exact retained runner and
production-helper hashes, substitutes only the three new small-producer sources
and test entry point, and writes the new selection create-new/fsynced. It does
not import or execute project code.

Generated `experiments/v5-local-checks/small-producer-controls-01-selection.json`
is6,207bytes/SHA-256
`672a484b26f45f808966fc0967371bf7422743555ec82bf7353525bcbd094466`.
All six selected source hashes match actual source bytes. All18 runtime pins
match fixed predecessor selection
`9a814b486eed15452732293ec7e76a8c2bc1d43ef0a7712972076a8a7f31ef9e`;
limits remain20CPU/60wall/512MiB/two-process,1MiB per log. The only child argv
selects the new16,954-byte `test_small.py` under isolated Python-I/-S/-B and a
fresh evidence path. Run/attempt outputs were absent when inspected.

**Exact focused-control selection disposition: no blocker for this one bounded
synthetic run.** Actual results, source snapshot/import origins and clean Job
closure still require saved-evidence review; no execution was performed by this
reviewer and no broad campaign or retry is selected.

## Actual focused controls01 outcome

Independently read the saved enclosing result/command/logs, control report,
dispatch trace and actual durable manifest/reservation/stage/attempt records
under `experiments/v5-local-checks/small-producer-controls-01`. No rerun.

- All12 named tests pass, with zero errors/failures/skips. The control report
  expressly identifies mocked installation/supervisor/build/image/snapshot
  boundaries and zero native/build/guest/proof calls.
- The exact six original source files and all six selected snapshots match the
  plan. All four recorded product import origins are inside those selected
  snapshots and match their exact bytes/hashes. The executed test argv selects
  the snapshot, with-I/-S/-B and the expected fresh output.
- One inert dispatch has a real252-byte dependency manifest pinned by its
 2,217-byte reservation before dispatch. The stage/attempt both preserve FAIL,
  first-failure stop, zero synthetic worker charge and no retained checkpoint or
  application receipt. No `proof.checkpoint` exists. A simulated refusal is not
  relabeled proof success.
- Enclosing child exit0, directly reaped, Job closed, zero active/terminated
  processes, no cleanup errors or termination request. Job CPU0.671875 plus
  wrapper CPU0.21875 gives0.890625 known CPU seconds; outer wall1.4793442s.
  Logs are0/1,684bytes; peak Job private commit25,669,632bytes. Final independent
  run census is117files/147entries/734,315bytes, with no finalization marker.

Saved outer `RESULT.json`:2,032bytes/SHA-256
`d19aa249cd10d221d0b8543a7c2afd4c3afcbf9591e634ffc07b1d2c0774fdac`.
Saved `CONTROL-RESULT.json`:1,594bytes/SHA-256
`5492eb5016dce2fefc92313c677857fe5b905e3ba50c2705da9c8124697ea0a8`.

**Actual disposition: PASS for the selected twelve synthetic changed-boundary
controls and their enclosing clean closure only.** Native parser/proof behavior,
actual constructor/build/snapshot adoption and useful growth remain separate.

## One exact complete po18 layout selection

Read `Select-SmallLayout01.ps1` completely, SHA-256
`6a5afd15ecc8e61af8394c114cef7e600e88e9163eb43a46793884468e4ededf`.
The selector only prepares fresh configuration/selection files; it checks the
fixed old mathematics plan/config, binds actual new snapshot-build records and
source snapshots, and removes exactly the old config/host-result/host-executable
runtime pins. The new adapter performs full actual build adoption at execution.

Reviewed exact files under `experiments/v5-local-checks/`:

| File | Bytes | SHA-256 |
|---|---:|---|
| `small-aggregate-layout-01-selection.json` | 11,115 | `153736d12c8eb697dbc416ad1b30636a35c3e527d40dfecaf3e872e6c26bb37d` |
| `small-aggregate-layout-01-configuration.json` | 2,866 | `d01ce6332993d814034c20e99f1344d304f89528843b325e8dcd4b50939467c5` |

All eight selected source hashes and all36 runtime pins match actual bytes.
The source delta replaces only the old capability adapter. The runtime delta
is exactly the new configuration, five actual snapshot-build records, three
selected source snapshots and the new executable, in place of those three old
records. The same A and actual memo-image-result mathematics remain; schema,
output and execution geometry are fresh. Selected bounds remain180CPU/240wall/
3072MiB/three processes and1MiB logs. Output was absent when inspected.

**Exact layout selection: no blocker for one execute-only complete po18 layout,
conditional on root's independent snapshot-build adoption.** The build's
operational outcome audit belongs to the separately assigned reviewer; this
review does not duplicate it. No proof, native parser campaign, cost prediction,
memory sufficiency, repeat or resource escalation follows from this clearance.

## Actual layout01 refusal and narrow repair boundary

The one selected layout01 exited before native invocation or evidence-directory
creation. Independently read its saved command/result/traceback and checked all
eight source snapshots against the exact plan. Actual failure is
`adopt_host -> read_record -> C.parse_json -> NONINTEGER_JSON_NUMBER`: owner
build records contain legitimate fractional timing observations, whereas the
mathematical codec deliberately refuses noninteger JSON numbers. The initial
source review missed this owner-record/parser mismatch; the failure is retained,
not converted into layout success or blamed on proving resources.

The exact outer result is2,092bytes/SHA-256
`64c90bbfdabaaadae5b180a6c741df4aac508880b6a36de6cfa9eefae226729a`.
Exit1 is cleanly reaped with closed Job, no active/terminated processes or
cleanup errors. Job0.296875 plus wrapper0.296875 gives0.59375 known CPU seconds;
outer wall0.7127025s. Logs0/3,024bytes; final13files/22entries/64,779bytes.
The absence of `evidence/` agrees with the failing call's position before any
native invocation. No capsule, guest run or proof was produced.

Root selects a fresh02 adapter only: keep byte/hash pins and record bounds,
parse owner records with strict duplicate-key rejection and finite floats,
leave integer-only configuration/mathematics parsing unchanged. This is the
appropriate narrow correction in principle. Used01 source/evidence stays
frozen. The02 source and exact plan require review before any invocation;
neither build needs repetition.

The separate `API.md` SHA-256
`60d62f42d05a6d0dc3f2e87b97ac55bff912f269baf4345e8f91a66ad0c99096`
was read completely and matches reviewed controller/native scope and caps.
It correctly separates owner reports/checkpoints from receiving mathematical
warrants and discloses the synthetic controls' limits. No API blocker found.

## Reviewed owner-record parser02 and exact layout02 selection

Read the fresh narrow source delta and recovery decision. Final02 adapter is
13,929bytes/SHA-256
`488ebf7aa039bbeae1245e8ad1758f090c7c9cfa9c598ebc8e329dfc8c313956`.
It adds only `parse_owner_record` and changes bounded `read_record` to call it.
`json.loads` retains exact key uniqueness and rejects nonfinite constants;
`C.canonical(..., allow_nan=False)` also rejects numeric exponent overflow to
infinity. Valid fractional operational times are accepted. Unchanged original
configuration/math/result parsers remain integer-only; pins and2MiB input bounds
remain. This repairs the observed semantic mismatch without relaxing mathematics.

`Select-SmallLayout02.ps1` is5,550bytes/SHA-256
`6bffc614d05ab387c57995d9fc1258960978c1d416b48ca8406edad0a574c6d9`;
only fresh layout name and adapter path differ from reviewed selector01.

| Exact file under `experiments/v5-local-checks/` | Bytes | SHA-256 |
|---|---:|---|
| `small-aggregate-layout-02-selection.json` | 11,119 | `86aaa7caf87aabe0558cbf333056db5123bddca5b33f563c0acd2e87b96e4f0f` |
| `small-aggregate-layout-02-configuration.json` | 2,866 | `f7e057b08fbcd3955faed1cd23fcf9feb2e8b990ed3b64fbb1c924a019e8157e` |

All eight selected source hashes match actual bytes. Thirty-five runtime pins
are exactly unchanged; only the new exact configuration replaces01's config.
Configuration differs only at its fresh output path; actual build/mathematics
bindings are unchanged. Limits remain180CPU/240wall/3072MiB/three processes.
The02 output was absent when inspected. Read the separately completed
`SMALL-BUILD-OUTCOME.md` audit; both exact host builds are now adopted compile-only
results. Their audit/source work is not repeated here.

**Repair and exact layout02 selection: no blocking issue found for one bounded
complete execute-only layout.** Original failed cost/evidence remains; this is
not a proof run or a repeat of a successful native layout. Success, native
geometry/bytes and subsequent admission still need actual outcome review.

## Actual layout02: complete-layout envelope exhausted

Root's already terminal layout02 was inspected once, without relaunch. Read the
outer result/command, adapter result, native command/stderr and complete
diagnostic. Checked all eight original sources and eight actual snapshots
against plan86aaa7ca; all36 runtime pins still match. Every one of the256 saved
segment files matches the diagnostic's exact index, byte length and SHA-256.
The actual wire and192-byte header agree with the native diagnostic and same
A; the command uses the exact selected memo ELF and genuine typed parent.

| Saved record under `small-aggregate-layout-02/` | Bytes | SHA-256 |
|---|---:|---|
| `RESULT.json` | 2,091 | `5927ca108717d88d688de92c0b1493da93e10d24b0fd6e3493c62f70dec3e47a` |
| `evidence/RESULT.json` | 2,184 | `507e8725af0573449908c77e7632288492cad6922943418f5d9d7f90372ab537` |
| `evidence/diagnostic.json` | 46,256 | `5e9beb1eeb3e4b9c0849309d2501f4a8733715e0d0c30c16bedd6e015c2b5784` |
| `evidence/command.json` | 1,223 | `8535669c0e5140d35d56d9198c58bd36ed97728bb1419a14acb8b25207be95ed` |

Native failure is exactly `Session limit exceeded: 67112097 >= 67108864`.
There is one guest-execution call, zero proof calls, no completed session
statistics/result and **no capsule**.256 retained segments0..255 each havepo18,
total padded rows67,108,864 and total bytes49,437,484. Diagnostic instruction
counts total75,132,143 and padding rows6,375,638; these are distinct quantities,
not interchangeable with the selected session-cycle/row cap. Partial segments
are preserved observations, not an accepted complete operation or certificate.

Both native and outer exit1. Outer child is reaped, Job closed, no active or
terminated processes, cleanup errors or termination request. Inclusive JobCPU
4.453125 plus wrapper0.265625 gives4.71875 known CPU seconds. Outer wall is
4.9536366s and peak Job private commit86,880,256bytes. This is execution-memory
evidence only, not proving-memory evidence. Native diagnostic read reservation
is2,185,246bytes. Final whole-run census is277files/288entries/49,770,521bytes;
the adapter's pre-result evidence census was264entries/49,703,613bytes. These
scopes differ and are not contradictory. No finalization-failure marker exists.

**Outcome: the exact workload did not fit the selected po18/N256/2^26 complete
layout envelope.** It is not a successful layout, and it falsifies using this
exact envelope as the next complete producer session. It does not prove that
po18 in general is infeasible, that a particular larger N will suffice, or that
any real segment proof fits4GiB. The unseen remainder and final count must not
be invented from partial execution. All02 work/failure costs remain charged.

The native manifest gate is held because its genuine complete-capsule
prerequisite is absent. Its reviewed finish-only control-flow argument avoids
the proving branch, and the proposed branch-specific refusals are coherent,
but this provides no present runtime authority. No proof, capsule relabeling,
automatic capacity escalation or repetition follows. The next consequential
decision must resolve the complete-layout geometry/envelope in principle before
any fresh source/runtime selection.
