# Contribution02 adapter and preparation delta review

2026-10-21, support_screen. **PASS, SOURCE ONLY**, for the exact corrected
adapter/actor/selector below. This is a changed-boundary review, not a repeated
review or execution of the predecessor integration. The observed owner still
requires its own review, exact build and actual adoption before any public02
launch. Root owns every preparation, build, runtime and Git decision.

## Exact reviewed source

| File | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/managed_contribution02/installed_contribution.py` | 24316 | `7b208288cb3a7ae7e370fd4e269ea6bd0ac6d0eac74324932cd6b8f21a840432` |
| `software/v5/managed_contribution02/contributor.py` | 8762 | `fa38dae4e6c2bf5ea4a59796170da44d8243b4a5c50af023917255ab94f97431` |
| `research/cycles/v5-2026-10-20/Select-ManagedContribution02.ps1` | 10529 | `39580e003e4b273dec9658096ac7140b4829953d53334f9e0fab1b0249fd48cc` |

Read `MANAGED-CONTRIBUTION02-SELECTION.md` and the source checkpoint, compared
the new actor/driver against their exact used predecessor sources, inspected
every changed control-flow block and read the preparation selector. Reused
predecessor integration reviewaca1c1e2, contributor review699f23dd and actual
failure audit2615e899. No old source/payload sweep or old campaign was repeated.

The initial unexecuted driver6a6eee46 and selector5d4dc128 named in the first
source checkpoint are superseded by the exact pins above. Root corrected two
review findings before use:

1. The selector snapshotted the02 driver but argv still named the old
   `managed_contribution` path. Its final argv now names
   `{snapshot}\software\v5\managed_contribution02\installed_contribution.py`.
2. The first driver amendment captured the primary failure but left
   `future.result` outside the secondary-failure guard and could propagate the
   secondary close error instead. The final amendment covers that wait, retains
   the original exception, records the secondary failure and restores the
   first-failure stage in the final report/summary.

No source-level blocker remains in these three exact files.

## Source-provider reservation correction

The actor changes only the source-provider reply allowance4 MiB to20 MiB and
adds its explanation. The unchanged group route initially reserves16 MiB,
then replaces the temporary reservation with actual bytes sent. The retained
opening is1595 bytes; subsequent offer and447887-byte packet requests are
sequential and have their existing request-specific reservations. Thus20 MiB
covers this exact three-request source path without changing provider route
validation or requiring16 MiB of actual transfer.

The host's exact nine-field placement quote, caller request/byte caps, finite
deadlines, artifact pins, manifest, structural-only policy and success/cleanup
assertions are unchanged. In particular the changed source allowance is not a
refund or increase to the failed01 grant. Its original chargedINCOMPLETE request,
private credential and host state remain preserved. Source01 cannot be repaired
in place and is not reclassified as successful.

## First-failure and cleanup retention

The driver records only stage and exception class for its primary failure;
messages, repr, traceback, locals and credential objects are not serialized.
The original exception remains in flight through `finally`. That block waits
for the same separately bounded host supervisor; both a wait failure and failed
host completion are recorded as `host_completion_failure`. A secondary error
is rethrown only if no primary error already exists. This does not suppress a
failure into PASS, skip waiting, cancel/restart a host or invent closure.

The top-level failure handler restores `primary_failure.stage` for the report
and displayed summary. Successful contribution followed by failed host completion
remains a host-close failure. Later checks are explicitly staged
`validate-closed-custody`; all former exact success requirements remain:actual
three source pulls, one completed intake, committed receipt/quote, genuineCLOSED,
session/source bindings, durable state/artifact checks, empty hosting operations,
bounded token scan and completion within the original driver deadline.

The original finite intervals remain:driver400 seconds, outer420 seconds,
host wrapper335/public300/child230, contributor wrapper85/public60, readiness
poll within75 seconds, service60 seconds and cleanup reservations unchanged.
The host launches only if its original335+20 reservation fits. This review does
not claim the unknown01 close cause has been fixed or that scheduling guarantees
success. Captured observed-owner diagnostics are not closure authority.

## Fresh preparation and selected map

All writable paths name `managed-contribution-02`; selected code names
`managed_contribution02`, and installation is
`product-local/v5-distribution-managed-observed-01/Mathematical Commons v5`.
An exact old-name/path/pin search across the three final files found no stale01
driver/actor/input/private-root path. Historical template, fixture, lifecycle
support and runtime-basis pins intentionally remain unchanged.

The selector binds this review's caller-supplied exact digest, final driver/actor
pins, adopted observed release and its build input. Exact127 SDK rows are compared
to build rows and installed bytes. Its four snapshots and160 runtime pins retain
the reviewed closure; it performs no product import or builder/runner invocation.
Input/selection/allocation/private-child paths must be absent. JSON creation is
exclusive and failures leave any created preparation evidence in place.

The actual supported outer cap is8 active processes from the start, not the
rejected12. The unchanged remaining envelope is200 CPU seconds,420 wall seconds,
1024 MiB and1 MiB per log. Current UTC horizons remain fresh15/16/17/18/19-minute
values in the new input; the driver rejects stale preparation, and no original01
allowance is renewed. No new public02 input or selection is claimed to exist.

The DirectoryInfo ancestor correction is retained. Only a fresh private child
is created, with a protected current-user+SYSTEM FullControl DACL and explicit
readback; existing directory ACLs are not intentionally altered. Invocation must
use Windows `powershell.exe -NoProfile -ExecutionPolicy Bypass` for the selected
.NET Framework directory-security overload. Trusted local provisioning remains
the premise; no same-account/administrator isolation, secure erasure or general
secrecy proof follows. No credential is created by this selector.

## Boundary and next gate

This review used source reads, line comparisons and small-file hashes only.
No selector, source import, AST parse, private-directory creation, credential
access, test, service, build, deletion or Git operation was performed. Author
syntax-check reports are not execution evidence. The exact observed owner and
one-owner127-map build remain separate prerequisites. Root must pin the actual
generated selection after preparation and separately authorize any finite02
launch. The whole original01 result remainsFAIL, and its unknown close cause is
not assigned a speculative explanation by this source-only pass.
