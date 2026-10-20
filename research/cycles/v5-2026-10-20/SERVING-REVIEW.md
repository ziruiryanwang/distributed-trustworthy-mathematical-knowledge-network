# Ordinary serving entry: independent review

2026-10-20; `core_release`. Source-only disposition: **no blocking issue found**.
Clear root's exact-plan generation for the eleven focused serving controls;
no execution has occurred in this review.

| Reviewed file | SHA-256 |
|---|---|
| `software/v5/client/serve_workspace.py` | `89723f2e8a03abcaa709560f6d991ffc5d2bb349ef6cb662aadad7589a73936c` |
| `software/v5/client/test_serve_workspace.py` | `5b51a5a8d78fe98927e27de98f09b6e0b004fb2a137b3be3cb9d1a4feba31361` |
| `software/v5/client/SERVING.md` | `5526391af45181340e60f15e3c6e030b0b9cd0c2c92827426a6de452167200a9` |
| `research/cycles/v5-2026-10-20/Select-ServingChecks.ps1` | `b1056630ce78265051f1f5c07fa4767cb60e435899907a0d06e6e86906fabd4d` |

## Consequential checks

- The closed five-mode mapping selects exact existing Workspace/provider types.
  Existing constructors enforce schema/profile/store compatibility, with
  `create=False`, no migration or fallback and no mathematical owner.
- Canonical ordinary existing input and fresh output paths are checked.
  Workspace and installation/run/snapshot roots must be disjoint in both
  directions. Missing data cannot silently become an empty workspace.
- HTTP/TLS/bind, connection/request/reply and per-request limits remain the
  existing provider's rules. A live READY file precedes the finite wait.
  Effective service lifetime never exceeds the original outer deadline minus
  the explicit cleanup reserve. There is no location or indefinite-daemon work.
- HTTP is stopped before workspace closure. Startup failure after real bind
  retains a provider to clean up. Stop failure additionally attempts listener
  close, handler cancellation and bounded drain. Workspace-close failure
  attempts remaining stores, ledger and lock. Primary and cleanup failures
  remain distinct; attempted fallback cleanup never manufactures PASS.
  Unreturned partial constructor state remains under its existing constructor
  cleanup and the outer process boundary, explicitly not certified closed.
- The API is remote-read-only, not filesystem-immutable: lock/recovery metadata
  and index snapshots may change. Documentation states this. Tests create only
  fresh synthetic structural stores, never open frozen retained evidence as a
  mutable service workspace.

## Focused tests and selection

Eleven controls exercise two actual IPv4 loopback service lifetimes, offer and
known-ID group retrieval, stop/reopen, missing/config/mode/bind/limit/path
refusals, all five exact provider/store combinations, partial-bind failure,
original-deadline shortening, cancellation, and both new fallback cleanup paths.
The stop-failure case now raises **before** any normal stop, with a real bound
listener and waiting handler; it requires EOF, endpoint refusal, drained tasks,
workspace reopen and preserved cleanup uncertainty. This materially tests the
fallback rather than merely injecting an error after resources were closed.

The selector retains the exact previously passing 85-source/19-runtime-pin
map, adding only the entry and this suite (87 sources expected). Direct imports
and their existing workspace/provider closure fit that map; no old test module
is imported or old test suite executed. Only this new suite is selected, with
30 CPU seconds / 90 wall seconds / 256 MiB / two processes. Native subprocess
construction is forbidden by the test. No verifier, proof, compiler, location
service, external endpoint or public-network run is selected.

A pass would establish this entry's service lifecycle over real fresh stores
and synthetic untrusted structural metadata. The offer query uses formal
features, but the group retrieval supplies its known identifier: this is **not
unknown-ID candidate discovery**, genuine mathematical admission, evidence of
net useful growth, or final v5/public deployment acceptance. No rerun or budget
renewal is authorized by this review.

Exact prepared selection reviewed:
`experiments/v5-local-checks/ordinary-serving-controls-01-selection.json`,
SHA-256 `448e4b56c4d94ab9fb454e5e2ec2568b56d229758837bfc01fde5f01674949bc`.
It binds the entry/test hashes above, the stated 87-source/19-pin map, only the
new test entry and the unchanged finite limits. No blocker to root's one
bounded execution decision; no test had run when this disposition was written.

## Actual controls01 failure

The selected run failed: 11 controls, three passed, eight errors, zero assertion
failures/skips. Every error is the same test-context layout mistake:
`sources_portable=SOURCE/"portable_runtime"` names a directory absent from this
runner's retained source snapshot. Its selected location Python package is
actually at `SOURCE/"location"`. All eight errors arose in service parameter
prevalidation, before HTTP start. Observed loopback exchanges, successful service
lifetimes and injected lifecycle faults are all zero.

The source review checked Python import closure but missed this fixture-path
mismatch; the earlier source clearance did not establish a passing lifecycle.
The product and test snapshots match their reviewed hashes. No product defect
has been demonstrated by this failure. Keep product source and failed01 frozen;
a fresh test-only successor correcting the fixture path is the minimal
appropriate next selection, not extra imported sources merely to create a
directory.

The enclosing child exited one and was reaped; Job closed with no cleanup errors,
zero active/terminated processes. Known CPU: **1.59375 seconds**
(1.234375 Job + 0.359375 wrapper); wall **3.1739714997820556 seconds**;
peak Job private commit **30,683,136 bytes**.

| Failed01 evidence | SHA-256 |
|---|---|
| Outer `RESULT.json` | `9ef30e4a723db275f6bc0d587c853a28df3d11ecee4c05c667cceda34b7108cf` |
| `controls/RESULT.json` | `c0af7c1092fdf5d06abb7536b8b28e9983cc73f1d7626a7b5301c41c08a6a8e1` |
| Raw `command/stderr.txt` | `ac66b84f8b41d0f56c383884fa7bf2550bf4215c79afaa81943d4570f20d47c2` |

No rerun was performed by this reviewer. The corrected successor and exact
selection require their own disposition; the eight unexercised lifecycle
controls have not passed.

## Minimal test-only correction

Reviewed `client/test_serve_workspace02.py`, SHA-256
`cfd47d2573fcddcf93bb0c60e6c493794f49b01841ca34ab287b72e62b5dcf02`,
and `Select-ServingChecks02.ps1`, SHA-256
`41102f0f1053d0a498302e7d1640802c984d250e90ee5185a56f3ea41624b8d5`.
The 24-line adapter subclasses the original test class, overrides only the
context's `sources_portable` root to the selected `SOURCE/"location"`, and
invokes the unchanged original suite/main. All eleven methods, assertions and
the subprocess prohibition remain unchanged. The source root is only checked
as an existing protected directory by this service; no location process or
extra source import is enabled.

The selector verifies the frozen prior selection, retains all 87 source pins
and 19 runtime pins, adds this one adapter, and changes only the selected entry
and fresh run name. Existing limits remain unchanged. No blocker to preparing
the exact 88-source successor selection; no product source change or widened
test allowance is needed.

Exact02 selection inspected after preparation:
`ordinary-serving-controls-02-selection.json`, SHA-256
`5d3a3581e68341d8a98dffc588bc73b5b63672350dc2e59f75c10ed7ff10f25d`.
Confirmed 88 source pins, 19 runtime pins, exact correction adapter and unchanged
30 CPU / 90 wall / 256 MiB / two-process limits. No blocker to root's one bounded
execution decision.

## Actual controls02 and source-derived final correction

Controls02 produced **ten passing controls and one failed assertion**, not a
suite pass. Independently checked all 88 original/snapshot source pairs, 19
runtime pins and 81 recorded imported origins. The passing controls include
actual partial-bind closure, cancellation, original-deadline shortening,
all mode/refusal cases, active-handler stop fallback and workspace-close
fallback. Eight injected lifecycle faults occurred. Their success is retained;
they should not run again to resolve the remaining case.

The first offer/group/reopen control received HTTP 200 with `REFUSED`, whereas
the fixture expected `OFFERED`; it had requested a 65,536-byte expanded-summary
ceiling. In the inherited `Store.summary`, each present feature expands to 256
partition descriptors and 256 sibling hashes. For this fixture each feature
row is 44,543 bytes (27,283 + 17,153 + 107), so two present features exceed
64 KiB even for this one-object index. Compact wire size and expanded size are
different limits. The preserved request therefore admits a source-derived
diagnosis: the chosen test expectation is inconsistent with its expanded cap,
not evidence that the product should bypass the inherited refusal.

The failed control stopped after that one offer exchange; it did not reach
group retrieval or two-lifetime persistence. Test teardown cancelled the
service; its saved result confirms clean HTTP/workspace closure and zero active
handlers/reservations. The enclosing Job also reaped and closed cleanly with
zero active/terminated processes. Known CPU **1.953125 seconds**, wall
**6.329838099889457 seconds**, peak **29,499,392 bytes**.

| Controls02 evidence | SHA-256 |
|---|---|
| Outer `RESULT.json` | `50626d6ace240f95bfb1af15231c470eb5a64492ed28f58bb99355edbb831ae6` |
| `controls/RESULT.json` | `23b17caf8455e2466a77594441e940d4b3d5af0fe2fd896a55a32555bbf365d4` |
| Raw `command/stderr.txt` | `93588660c570dbf26e3f93a0dd2ccf9b13b86b99e71ea7116e17f6c5be43279c` |

Reviewed the small failed-control-only successor:
`client/test_serve_workspace03.py`, SHA-256
`de73a77e70af98109f5f57514228a782e848ee4af5c1890bd2b3227e3652f778`.
It retains the corrected context and original test method/assertions, changing
only the outgoing offer's expanded ceiling to 128 KiB, sufficient for this
fixture's less-than-92-KiB expansion. Wire ceiling remains 64 KiB. Exactly the
one unresolved control is selected; the ten passes are not repeated.

Its selector `Select-ServingChecks03.ps1`, SHA-256
`d7149495382d770f06846b210cedcb235e112213abc74cc5f6fb49a7f4cbcc19`,
retains the previous 88 sources/19 runtime pins and unchanged outer limits,
adding only that adapter and a fresh entry/run name. No product source or
mathematical rule changes. No blocker to exact successor selection and one
bounded execution decision; reviewer performed no test or new experiment.

Exact03 inspected:
`ordinary-serving-controls-03-selection.json`, SHA-256
`64b269af83ea802f8437f69225b9e22000ad906e4f3a10691e5020fe64d6ae64`.
Confirmed 89 source pins / 19 runtime pins, exact one-control adapter and
unchanged limits. No blocker to the single selected run.

## Final actual disposition

**The eleven selected serving boundaries now have passing evidence: ten from
controls02 and the remaining one from controls03.** Controls01 and controls02
retain their failed-run status; neither is relabeled as an all-passing suite.
No additional test is recommended for this changed boundary.

Controls03 ran only the unresolved offer/group/persistence case: one pass,
zero errors/failures/skips. Independently checked its 89 original/snapshot
source pairs, all 19 runtime pins and 82 recorded imported origins. Product
source remains `89723f2e...`; only the reviewed test adapters differ.
Inputs are the fresh synthetic descriptor determined by the selected test
source, not frozen external workspaces or accepted mathematical artifacts.

Actual evidence records two fresh finite service lifetimes over the same
retained workspace and four IPv4 loopback exchanges (offer + known-ID group
each lifetime). Both reports are PASS, each with two requests, 2,511 reply
bytes, no refusal/failure, zero handlers/reservations and clean HTTP/workspace
closure. The test checked group opening equality, structural opening validity,
endpoint refusal after stop and successful workspace reopening with retained
index/group data. Each lifetime ended after its selected one-second deadline
and before the original outer deadline.

The outer process exited zero, was reaped and its Job closed with no cleanup
errors and zero active/terminated processes. Controls03 known CPU is
**1.390625 seconds**, wall **5.520850799977779 seconds**, peak private commit
**29,171,712 bytes**. Total known CPU across preserved01,02,03 is
**4.9375 seconds**, including the failed attempts; nested counters are not
added again. Pre-clock startup remains unmeasured.

| Controls03 evidence | SHA-256 |
|---|---|
| Outer `RESULT.json` | `875a9b43a4a48866a0bbbda954e47a88ce280d8f51cdd781e11ab39296a115b1` |
| `controls/RESULT.json` | `c47ff73ecb3ac8a3cbe54d22236f3151d9c36a445a3c94771178b1f3b4d1c28f` |
| Raw `command/stderr.txt` | `22fe77a54c30eed485af2b34cc84bc0819d1d6c8e8357fb16e67f09e072f7438` |

This establishes ordinary service lifecycle and retained structural retrieval,
including the separately passed cleanup/refusal controls. It does not establish
unknown-ID candidate discovery, genuine receipt admission, positive full-cost
growth, independent hosting or final v5 readiness. Those boundaries remain
separate. Preserve all used sources, selections and outcomes.
