# Compiler-only envelope decision

2026-10-17. Independent reviewer: `memo_independent_review`. Canonical workspace
guard PASS. Read-only inspection of two retained build results and the already
reviewed source/recipe delta; no imports, compiler, test, proof, new memory
observation or Git mutation. Root owns any selection and source revision.

## Decision

**Yes: a fixed1,536 MiB compiler Job cap with an additional1 GiB immediately
available physical AND actual commit margin is justified for one snapshot-host
link.** It is a bounded empirical discriminator, not a proved peak upper bound
or guaranteed completion. No current geometry compiler attempt has occurred;
the2 GiB plan was deferred at its preflight, so this is a prospective compiler
envelope refinement, not a retry/cap ladder. It changes no proof or layout cap.

The new launch threshold would be **2,684,354,560 bytes (2.5 GiB)** of both
available physical memory and actual commit headroom, for a hard compiler cap
of1,610,612,736 bytes. Keep the1 GiB margin for the separate Python controller,
launcher and unrelated activity. That margin is not an OS reservation.

## Closest actual evidence

| Retained operation | Compiler Job peak private commit | Compiler CPU / command wall |
|---|---:|---:|
| `small-aggregate-snapshot-host-build-01` | 977,940,480 B =932.63671875 MiB |60.8125 /60.07052540010773 s|
| Last corrected `prover-allocation-build-01` stage-host link |1,240,559,616 B =1,183.08984375 MiB|158.34375 /169.1342953001149 s|

The snapshot result hash is
`7ad07e35602092833d9f40e7f0775f0b4eceb451e52853875bd5baeaf63f78b1`.
Its successful attempt agrees, no finalization-failure marker is present, and
its retained closed Job record agrees on CPU/peak with zero active/terminated
processes. Its compiled snapshot source is exactly the frozen6644d9a0
predecessor already compared with the new7f3fefab source. No full audit or
toolchain census was repeated.

The corrected five-step result remains
`ac259e9db55275a0a8404e9cf881fd3779f2e7259ccfe134c8e93e3b180b4102`.
The quoted peak is specifically its final stage-host command's disjoint Job,
not the sum of unrelated jobs. It uses the same four refined Rust libraries
that the new snapshot link will consume.

The proposed cap exceeds these observed peaks by **603.36328125 MiB** and
**352.91015625 MiB**, respectively. This is materially more support than merely
choosing a cap because the current machine happens to have that much free.

## Why the comparison is relevant, and where it stops

The actual old snapshot already compiled the same execution-only host shape
with the same compiler, target, optimization/fat-LTO flags and native inputs.
The new host changes only the comment, runtime segment-count constant, runtime
geometry check and two operational schema strings. N512 does not introduce a
512-element compile-time template/unrolling expansion in this host.

The old snapshot used predecessor Rust libraries. The corrected stage link is
therefore a second useful comparator: it actually consumed the exact refined
libraries and current retained recipe family, within1,184 MiB. The new snapshot
uses the reviewed four-argument substitution of that recipe and unchanged
library edges. The resulting executable is not invoked during compilation.

Neither comparison proves a monotonic compiler-memory ordering. Fat LTO,
monomorphization, allocator behavior and code reachability can change peak
memory, and the two observations do not bound every future run. Success under
1,536 MiB remains unqualified until this exact link completes. A hard cap and
preserved failure make one such attempt reasonable; they do not justify an
automatic second attempt at another cap.

## Required implementation/launch conditions

1. Preserve the original9c3f00c2 selection and its deferred launcher evidence.
   Root reports the23:27:08 UTC preflight found3,804,200,960 B physical and
   2,961,518,592 B commit headroom, with no compiler/run/attempt created.
   Those old numbers would exceed the proposed threshold but are **not fresh
   launch clearance**.
2. Record one fresh exact compiler-only selection and align builder Job cap,
   selection limits, adopter contract and launcher threshold/source hashes.
   Do not edit already used launch evidence or silently keep contradictory
   2 GiB fields. All unchanged source/runtime/library identities remain bound.
3. Retain240 compiler CPU/300 command wall, six processes, existing output/log
   and controller/tail limits, honest one-link schema and owned-process cleanup.
   The snapshot executable, guest and prover must not run in this operation.
4. Immediately require >=2.5 GiB physical and true commit, valid counters and
   no heavy overlap. Do not terminate user applications, change system memory
   settings, sweep thresholds or repeatedly poll to force admission.
5. One failure, resource refusal, changed binding or uncertain cleanup stops.
   Preserve all costs/output. A successful compiler result requires the ordinary
   saved-result/executable/source/closure audit; it authorizes no layout or proof.

If the immediate gate is unavailable, continue selected useful source work.
If the compiler itself fails, diagnose that exact failure before another design
decision; this checkpoint preauthorizes no fallback allocation. All proof and
full-v5 obligations remain unchanged.
