# Independent actual public-workflow audit

2026-10-28, growth_design_audit. Canonical guard passed. Saved JSON/log/source
and returned-byte inspection only; no product imports, database opens, reruns,
new requests or Git operations. Kit assembly/relocation is separately owned.

**PASS: the finite public init -> append -> append -> serve workflow completed
cleanly, retaining both selected contributions under one stable host descriptor.**
All four typed reads returned their selected exact data. This is the public
composition selected in PUBLIC-PLAN, not a final-v5 or worldwide-release claim.

Evidence root: `experiments/v5-local-checks/incremental-host-public01`.

| Binding | SHA256 |
| --- | --- |
| selection.json | `11e4dfd285b31129ae99acbc730cbaf61474b37895bc4b00dc3a4637e6b8b885` |
| outer RESULT.json | `ddbfbd7dd016a0740e260935488b2b1603654a4dc82597c77cee6b6b76651c30` |
| suite/RESULT.json | `4aa2be394cd7a582c43262dec00d00f3014bc863cb15fcfb149b182ec28167a0` |
| selected/executed runner | `a516e6f96f6d8dfd210c41e32fbdeee8798ae496a1cb52d1624a613800832f59` |
| package PROFILE | `e8d33500db4c0a5ce89b2dfb51c3e1f9ec8f12063bbc58fe5e4eb23c2b6dfb13` |
| actual suite/host/HOST.json | `45db32b2c53e86b03920ffab2d95fcc31700f40c2a76902899cc0f9ff75058e8` |

## Exact sequence and state

The suite reports passed:true, assertions_passed:true, phase:CLOSED and no
cleanup errors. Its saved stdout parses to the same complete result. The outer
selection hash matches the actual selection; all four snapshotted source/helper/
plan/controller pins match. Selected actual package/assembly runtime pins match
the prior audited assembly. The two saved projected manifests each contain
exactly the approved one-unit entry and semantic ID, without dependency expansion.

Each public command's actual RESULT.json and SUPERVISION.json equals the
corresponding nested suite record. Each config hash matches its saved config;
each COMMAND records one attempt. Launcher and public results are successful,
retain the selected profile/semantics/host, report mathematical_owner_opened:false
and mathematical_acceptance:false, and report zero mathematical worker CPU.

| Completed command | Custody objects / exports / logical bytes | Indexed records | Current snapshot |
| --- | --- | --- | --- |
| init | 0 / 0 / 0 | 0 | `420fd79c11e6424eaff3db64f935d915c6f60bde1b32a2f90288b2467b02990f` |
| append ResetEffects.fill | 2 / 1 / 8515 | 1 | `f35f1eaeb31620e85b49b8c0ae647913a00e9016431da33ab13b2fe51b7d3f9f` |
| append ResetEffects.contextual_iff | 4 / 2 / 40717 | 2 | `86b3b8ad8c747104dbf733b3a9aa65625222165be255a54d0c4db58fd8d54611` |
| serve | 4 / 2 / 40717 | 2 | Same second-append snapshot |

Both append results have batch_complete:true and before_content matching the
preceding observed current state. The actual HOST bytes hash agrees with every
reported descriptor identity. The real service READY and final result report
STABLE_INCREMENTAL_CONFIGURATION_NOT_CONTENT_IDENTITY separately from current
content, with prior_append_completion:NOT_ASSERTED_BY_SERVICE. These state
observations come from the successful reviewed code and saved reports; this
audit deliberately did not reopen the host databases.

## Returned bytes and bounded network activity

The service actually bound loopback at 127.0.0.1:52252 with TLS false and its
original 20-second lease. This is a historical endpoint, not a currently running
service. The four saved read rows are COMPLETE with no exception chains.

| Returned object | Bytes | Independently checked SHA256 |
| --- | --- | --- |
| fill locator | 318 | `c98504474a766d2b68d7a5a6e9c8663df4d2941d4ed653f07b8fb98768ccc2b6` |
| fill evidence | 6384 | `8bb24aa780ed89563921671715cc2659c75abe68707be5722294ea418caf527b` |
| contextual_iff locator | 355 | `ab449eac1509ba0326a801cabe50923e77eb4169ab4e58c60a3d8d0a8e768968` |
| contextual_iff evidence | 26650 | `bf13287aed53c34ccf58798d3e77ab0df1b60f74ed780641de88a9dc7fd813bd` |

Actual saved response lengths/hashes equal the report. Both evidence digests
also equal the retained original fixture files. Locator metadata identifies
the selected exact export names, unit IDs and semantic ID. All typed responses
explicitly remain inert; no new mathematical acceptance was inferred.

Client and provider agree on four requests, 33,707 reply bytes, 901 header bytes
and 890 request bytes. This is 33,034 evidence bytes plus 673 locator bytes.
The client budget is closed with zero pending requests and zero reserved reply
bytes; HTTP has four completed responses and zero failed attempts. Provider
reports four accepted attempts, no refusals/failures/handshake failures, zero
active work, zero reserved reply bytes and zero pending/failed cleanup. It
stopped accepting after its four-request bound, then its finite lease completed.

## Natural closure and cost

All four nested Jobs report COMMAND_EXITED_ZERO_AND_CLOSED, exit code 0, direct
child reaped, Job closed, final active processes 0, zero terminated processes,
no termination request and no cleanup errors. All host custody/index/lock
closures are CLOSED. All four child stderr files are empty. The final service
status is LEASE_FINISHED with quiescent:true and no cleanup errors, so this was
the natural-success branch rather than failure kill/reap cleanup.

The enclosing Job likewise exited zero and closed with no active or terminated
processes and no cleanup errors. Its measured CPU was 6.625 seconds; outer
wrapper CPU was 0.296875, totaling **6.921875 known CPU seconds**. Nested child,
supervisor and harness timers are included in the enclosing Job and must not be
added again. Overall wall time was 27.39770440000575 seconds; supervised time
through cleanup was 27.335461199982092. Peak Job private commit was 79,888,384
bytes. The outer logs contain 32,959 stdout bytes and zero stderr bytes.

The original outer selection was 230 wall/150 CPU seconds, 1,536 MiB and six
simultaneous processes; no deadline or allowance was renewed. Lifetime process
count 18 is not a simultaneous-process count. Including the distinct assembly
and focused-controls operations, this selected sequence consumed **16.984375
known CPU seconds**. No operation was repeated for this audit.

## Meaning and remaining scope

This evidence establishes that the reviewed public software can initialize an
independent inert host, add separately selected data without replacing its
operating descriptor, retain earlier data, and serve both additions through the
existing typed acquisition path. The direct controls separately established the
cumulative-target and postcommit-exception cases; this run did not repeat them.

No process kill/hot-journal/power failure, independent machine, dependency-closure
acquisition, new Lean theorem, usefulness acceleration, huge-network benchmark
or new transport assurance was tested. Source arguments support absence of a
mandatory previous-corpus scan in normal append; this small integration is not
a measurement of that asymptotic behavior. Full v5 remains active and unfinished.
