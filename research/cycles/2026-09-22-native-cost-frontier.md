# Native one-pass cost frontier

2026-09-22. Read-only attribution of the sealed `onepass-native-01` attempt.
Only retained JSON receipts and unchanged source were inspected with
PowerShell/.NET. No Python, Lean, product command, test, service or rerun was
executed; no qualification evidence was changed. This is a cost decision, not
a new mathematical or operational acceptance verdict.

## Decision

Do not select a product optimization from this one run. The expensive observed
work is build, checking/inspection preparation and submission, not the three
peer-find operations. The six nested stage Jobs account for only 113.062500
CPU seconds within 362.046875 inclusive outer-Job CPU seconds for their six
steps. The 248.984375-second difference is work outside those stage Jobs, but
the receipts do not assign it to a particular function. Canonical package
reading is a substantial measured wall-time component of the public calls;
the extraordinary support-build wall/CPU gap and variation between the two
initializations make an environment-sensitive explanation plausible too.
Measure that boundary on the same cut before changing the reader or native
path.

The primary record is [one-pass result](../../software/qualification/onepass-native-01/result.json),
SHA-256 `471a6feec01ed1b14949476b50e2b58601be3bbc2f19432bcdc8fbf4cb4f4281`.
Its 20 steps took 606.785630 wall seconds in aggregate. Their disjoint,
inclusive outer-Job CPU observations sum to 425.546875 seconds; coordinator
CPU is a separate 54.140625 seconds. The sum of individual outer-step wall
durations is 574.973662 seconds, not the aggregate elapsed time: service Jobs
overlap other work, and coordination, gaps and census lie outside those step
intervals. Nested public and stage CPU is already in outer CPU and must never
be added to it.

## Measured expensive steps

All seconds below are retained observations, rounded to three decimals. Stage
wall/CPU is nested within the corresponding outer step; `read_package` wall is
an event counter, not an additional disjoint phase.

| Step | Outer wall | Outer CPU | Nested stage wall / CPU | Canonical package-read wall |
| --- | ---: | ---: | ---: | ---: |
| `build` | 174.269 | 49.500 | 172.810 / 19.750 | — |
| `init-a` | 34.424 | 33.031 | 6.608 / 5.938 | 16.236 |
| `init-b` | 62.944 | 62.094 | 11.869 / 10.844 | 31.340 |
| `admit-a` | 60.408 | 55.531 | 26.284 / 16.594 | 16.612 |
| `submit-a` | 108.278 | 118.828 | 54.117 / 50.281 | 28.570 |
| `admit-b` | 43.389 | 43.063 | 10.620 / 9.656 | 16.064 |
| `inspect-b` | 27.976 | 26.375 | none | 15.028 |

These seven steps use 388.421875 of the 425.546875 outer CPU seconds. The
support build's first Lean compile, `BootstrapSupport`, consumed 168.796 wall
seconds but only 15.906250 nested stage-Job CPU seconds; the second compile
consumed about 3.992 wall / 3.844 CPU seconds. The build's outer-minus-stage
CPU is 29.750 seconds. There are no retained disk-wait, scheduler or
antivirus counters that explain the first compile's wall gap.

The five commands in `submit-a`'s stage comprise three Lean commands and two
Python capture/inverse commands. Cumulative stage-Job CPU increments assign
26.656250 seconds to those Lean commands and 23.625000 seconds to the two
capture/inverse workers. Across all six stages, the corresponding sums are
89.437500 Lean and 23.625000 capture/inverse CPU seconds. Capture/inverse
perform canonical export-related work; they are not serialization-only timers.
The `submit-a` outer CPU is 118.828125 seconds against 50.281250 stage CPU;
`init-b` is 62.093750 against 10.843750. This makes the public
dispatcher/checker/preparation path a consequential candidate for further
measurement, not a proven bottleneck or an excuse to skip native checking.

The thirteen ordinary public call receipts sum to 353.640625 nested Job CPU
seconds. For those calls, outer-minus-public CPU sums to 14.578125 seconds;
median outer-minus-public wall is 1.023 seconds, and median
public-minus-product-event wall is 0.254 seconds. Those are wrapper-envelope
differences, not exclusive timings of every wrapper function. They indicate
that a blanket attribution of the large outer/stage gap to the outer
supervisor would be unsupported.

[`Checker.read_package`](../../product-local/onepass-native-01/install/py/checking.py)
records `package_read_wall_seconds` around its calls at lines 195–207. The
six checking-heavy events in the table total 48 canonical package reads,
13,478,490 canonical bytes and 123.851979 seconds of recorded read wall.
`init-a` and `init-b` each report 10 reads of 2,809,752 bytes, yet their
read-wall observations are 16.236 and 31.340 seconds. Admission A reports
6 reads / 1,684,521 bytes; submission A 10 / 2,804,649; admission B and
inspection B each 6 / 1,684,908. These counters measure elapsed time inside
the reader, not CPU or the duplicated-hash slice, and cannot be added to
stage or outer time as independent cost without interval proof.

## Transport is not isolated by these receipts

The three peer-find product events took 0.150094, 0.117076 and 0.112827
seconds. Acquisition A took 7.777605 product-event seconds within 9.091706
outer wall / 8.312500 outer CPU seconds, including 4.821511 recorded
package-read wall seconds and ten fsynced package files. Acquisition B took
5.857237 event seconds within 7.114301 outer wall / 6.484375 outer CPU,
including 3.543165 package-read wall seconds and thirteen fsynced files.
Their bundles were 281,298 and 282,111 bytes. Whole acquisition includes
loopback HTTP, canonical validation, durable writes and state; no pure socket
time was recorded. The fixture and owner services charged 315,842 and 284,840
send bytes and used about 1.016 and 0.969 outer CPU seconds, respectively;
their Jobs overlap other work. These data do not benchmark an independent
host, SSH forwarding or network latency.

## Prior paged run is a warning, not a causal comparison

The sealed [prior paged result](../../software/qualification/peer-discovery-native-01/result.json),
SHA-256 `5b0a9eccecfbcd711f70a673a9fc8d1f8ac7f126f24d2e1619bd88f715706a46`,
used the same mathematical chain/template and unchanged checking, codec and
native source bytes, but a different service cut and a different fresh run
time on a shared host. Selected observations were:

| Observation | Prior paged | One-pass |
| --- | ---: | ---: |
| Aggregate wall / outer CPU seconds | 233.122 / 200.781 | 606.786 / 425.547 |
| Build outer wall / CPU | 9.772 / 9.656 | 174.269 / 49.500 |
| Support-stage wall / CPU | 8.519 / 8.063 | 172.810 / 19.750 |
| Submission outer wall / CPU | 54.472 / 56.531 | 108.278 / 118.828 |
| Submission stage wall / CPU | 29.557 / 28.063 | 54.117 / 50.281 |
| Same six event package-read wall seconds | 62.473 | 123.852 |

Fresh allocation, cache state, competing host load and I/O conditions were
not controlled across runs. Neither the one-pass service change nor a reader
regression is established as the cause of the difference. The large variation
also appears in unchanged build/checker work; a ratio of these totals is not
an optimization estimate.

## Smallest next cost experiment

Prospectively authorize a fresh **same-cut cost-stability discriminator**, not
an optimized implementation: from one pinned one-pass source/runtime and
unchanged common source package, run a support build and then two sequential,
independently fresh initializations under the current limits. Omit the peer fixture,
transport, submission and rest of the 20-step chain. Before launch, freeze
the exact inputs, order, resource limits, stop/failure rule and preservation of
every attempt. Retain outer/public/stage receipts, per-command stage wall and
CPU, canonical read counts/bytes/wall, and contemporaneous read-only host-load
and I/O observations. This small allocation retests the 168.8-second
low-CPU compile and the A/B reader spread on the same roughly 2.81-MB input.
One repeat will triage, not prove steady-state cost; an ambiguous result calls
for another predeclared independent allocation, not selective resampling.

If substantial wall/CPU gaps or read-wall spread track host/I/O conditions,
investigate that environment before changing product code. If repeated
same-cut receipts instead show stable CPU-heavy canonical reading, then
separately design and review an endpoint-level checked-insertion candidate,
preserving exact canonical identity, corruption rejection, state equality and
fresh receiving admission. The earlier
[checked-insertion timing outcome](../../experiments/checked-package-insertion/TIMING-OUTCOME.md)
failed incomplete at 27 of 48 planned reads; it supplies no adoption or
speedup authority. This note recommends a discriminating measurement only;
it does not authorize execution, a source change or a performance claim.
