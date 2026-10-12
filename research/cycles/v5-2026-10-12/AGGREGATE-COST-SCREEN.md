# One informative aggregate execution, not another proof campaign

## Actual bounded outcome (2026-10-12)

The one selected execution is terminal FAIL, not a completed capsule. Actual
guest A is51d51ea0ba1f4e4402615e04e64c739dcd497145aa8ecf8e89ed8d03f8177c49.
Selection224ec1f99cb8e9dc59e290eddf526be2bbc7cad7aa13a7146110e31972f08e79
ran once; stderr reports `Session limit exceeded:33557665>=33554432`
(spaces normalized here only).128 segments/25,166,009B were retained before
failure. These are not a complete resumable execution. No proof call occurred.

Diagnostic SHA256ebd87c76cea9c321d1f64f5aee9ac5f1dc0c4aef0659c1937f0af84e4b259388,
2,428,623B, is under `experiments/v5-local-checks/aggregate-snapshot-01/evidence`.
It reports39,769,880 observed instruction events,131,454 stored samples and23,898
omitted samples. The131,072 distinct-cell cap saturated. Its maximum reported
row-point field is153,044,530,811; this must not be called actual executed cycles
or instructions. There are zero backwards-field events. Use explicit omitted
and early-window bias in any attribution; no statistical cycle fractions.

Independent actual audit is now adopted: inner RESULT
`a873a4b81d36397191ee8e550d6152eb77951f6204bd80406af73994f37820c5`, outer RESULT
`f91ef77bc4eeb23c0b0945de79d2e4866f173d5a51c285ac3ba4e503f8686d0c`.
All145 changed bindings match, including all128 retained segments; independent
byte comparison confirms that only A's32-byte slot changed. No capsule exists.

Outer operation:6.65625 inclusive JobCPU+0.390625wrapperCPU,7.8319161wall;
exit1/reaped/Jobclosed/no cleanup errors. Guest/segment-custody phase wall is
5279ms, native preflight150ms and boundary receipt verification15ms; these
overlap the outer total and are not additional CPU charges. This run rejects fit at the selected cap; it
establishes neither the excess work nor a total speedup against an old image.

Decision: no automatic larger-cap retry, no staged prover implementation or
production budget. Inspect the retained exact-image prefix offline, then prove
the next optimization's acceptance/cost argument before selecting source/build.

## Original prospective decision

Root source selection, 2026-10-12. Runtime remains unselected until the actual
guest/image and exact adapter selection are independently adopted. Full v5
and the two central requirements remain open.

## Decision before measurement

The two reviewed optimizations eliminate a duplicate parse/tree and the unused
canonical proof-output tree. They preserve acceptance, but establish no total
guest speedup. Amdahl's bound prevents inferring such a speedup from removed
operations alone. The old first-child failure supplies only a lower bound on
its execution cost, not a complete current profile.

Use the already checked two-delta workload, not new mathematics or a new base
certificate. Run its new aggregate guest once with the old 2^25 session ceiling
and po2=18, obtaining sparse PC diagnostics in the SAME execution. This is a
cost discriminator: completion yields a reusable execution capsule and exact
segment statistics; a cycle-capped failure yields a bounded prefix profile
that can distinguish representation/checker/SDK work when the exact ELF's link
map identifies it. Keep unknown/inlined symbols explicitly unknown. Samples
are not exact cycle attribution, a causal speedup or proof-production cost.

No source-level argument currently establishes fit. The point of this screen
is to resolve that implementation constant, not to claim affordability merely
because a large budget was allowed. Do not increase the ceiling automatically.
If diagnostics cannot support a next intervention, return to source analysis.

## Binding and reuse

The native two-delta wire and successful native conclusion are frozen evidence.
Only the 32-byte adopted aggregate image slot (offset12) is replaced in each.
All exact member journals, graph edges, witnesses, targets, membership root and
base receipt remain unchanged. This is request preparation, not changing a
certificate or promoting native output into receipt authority. The selected
host independently checks the whole new wire, computes the actual image ID,
compares the whole header and genuinely verifies the base receipt before guest
execution. There is no separate repeated native preparation call.

Preserve one completed capsule for later staged proving if warranted. A failed
or partial execution is not resumable proof evidence. No segment, lift, join,
resolution or finish call belongs to this screen. Certification cost remains
unfunded until the complete observed layout and a justified benefit region
support the next investment. Capability feasibility and net-resource savings
remain different release claims.

## Proposed finite envelope

One selected host invocation; child timeout120seconds. Proposed outer envelope:
180CPU/240wall seconds,3072MiB,3active processes. Cycles2^25,po2=18; at most128
retained segments and64MiB each for total segments and capsule,8MiB diagnostic.
Application artifacts plus input/log/report overhead must fit144MiB/160entries.
This is much smaller than any proof-production allocation. The outer Job
charges the Python wrapper and host together; do not add child CPU again.
Source/runtime rebind and completion/closure review remain mandatory. These
resource controls are not hostile-input security isolation.

No guest operation is launched by this document. Keep the earlier graph failure
and all incurred resources in the full-cost ledger; do not bury setup/failure
cost under a favorable per-recipient number.
