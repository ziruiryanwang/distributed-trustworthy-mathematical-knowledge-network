# Smaller-segment producer: source implementation selection

2026-10-17, root. Canonical root is
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
The final deployable v5 goal remains active. This selects source work only,
not a build, layout, proof attempt, public deployment or release.

## Decision

Adopt `PRODUCER-NEXT-DECISION.md` (24,737 bytes, SHA-256
`33e4be91861bd97234620bc1c6148b6624db5da123bb51182e7c07c3e7ffc0ef`)
and the independent review's three refinements: incremental bounded JSON
sequences, caps on retained as well as new checkpoints, and one actual full-po18
segment as the first eventual proof discriminator. There is no source-level
conceptual blocker. Final exact review disposition is recorded separately.

The unchanged po19 source has a proven memory lower bound above the old 4 GiB
cap. The fresh po18 path retains A/I/F/P/H and SDK verification; it changes
execution geometry, capsule identity and bounded orchestration, not mathematics.
The changed geometry has no certificate or memory-sufficiency claim yet.

## Disjoint owners

All new implementation paths are under `software/v5/aggregate_small/`.

| Owner | Exclusive source paths | Checkpoint |
|---|---|---|
| memo_tests_review | producer.py, __init__.py | SMALL-CONTROLLER.md |
| memo_independent_review | aggregate_host.rs, stage_host.rs | SMALL-HOSTS.md |
| root | build_snapshot.py, build_stage.py, capability_snapshot.py, test_small.py, API.md, finite selectors if separately selected | this decision and SMALL-RESULTS.md |
| v5_growth_decision | No product edits; independent changed-boundary review | SMALL-REVIEW.md |

All checkpoints are in `research/cycles/v5-2026-10-17/`.
Authors coordinate exact schemas/command/result fields directly. They read
canonical AGENTS/guard and the adopted decision before edits. Root alone owns
Git and runtime selections. Existing SDK/guest/receiver/evidence-client and
all used predecessor sources, selections, outputs and failures remain frozen.
Source copies and edits use apply_patch; no separate project is created.

## Boundaries that must survive implementation

- N256/M8, po18 selected layout, existing 2^26 session cap; distinct fresh
  source/build/profile/request/result identities and session/capsule bindings.
- Existing FILE_LIMIT64MiB, separate capsule96MiB and composite160MiB;
  parents1MiB and all retained/new checkpoints/final receipt512KiB.
- `stage-manifest` only: exact ordered dependency file, argv length/digest,
  incremental strict JSON decoding, host-derived dependency list, ordinary
  normalized non-reparse paths, exact byte/hash/key/capsule checks, no fallback.
- Preserve full composite and final fully resolved exact-A/H verification.
- Initial inputs512MiB with actual fixed remainder20MiB, separate new admin
  pins128MiB, exact input rebinding, complete retained success/history checks,
  same allowance and all failed costs. Caps are not predictions or funding.
- Explicit bounds/fees from the adopted decision, including manifest output,
  full-path quotes and controller work; no unreviewed caching framework.

## Shortest evidence path

Implement and review changed seams in parallel; run only focused controls after
exact selection. Two one-link host builds may then use retained libraries under
one combined finite capacity decision. One complete fresh po18 layout determines
actual geometry, count and bytes. Real constructor/request adoption and actual
full-path/capacity analysis precede any proof selection. Never relabel the old
capsule or automatically escalate caps/retry. Completed synthetic controls and
old public-client campaigns are reused, not repeated.

The genuine terminal gate uses two A checks, one authoring and one native delta
check, after a real receipt exists. This validates missing integration, not
novel mathematics or positive growth by itself. Production and failure costs
remain in the fixed-target full-cost comparison. Neither component success
nor this source checkpoint satisfies the whole v5 goal.
