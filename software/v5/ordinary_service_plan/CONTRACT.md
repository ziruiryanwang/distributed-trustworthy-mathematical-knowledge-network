# Finite unattended serving: selected implementation boundary

2026-10-26. Root selects source implementation, not execution, after reading
SERVICE-LIFECYCLE-DECISION.md in the current local-discovery research cycle.
Everything remains local/unpublished. The current default package and its source
archive remain unchanged; this is a separate companion to that public interface.

## Concrete benefit and simpler alternative

An operator should be able to authorize one evening's service without manually
approving each sub-hour lease. Independent agents can investigate using separate
state while the disclosure-approved owner serves. The existing public launcher
correctly runs one lease, but no supported unattended sequence validates all its
reports and bounds costs across leases. A hand-written loop needs these same
checks; Task Scheduler alone does not supply them. Implement one small reusable
runner rather than change the owner lock, checking rules or storage protocol.

The runner performs only `peer serve` with one pinned package/profile, supported
runtimes, catalog/store/custody and exact local configuration. It never publishes,
admits, mutates source, chooses mathematics or runs arbitrary shell commands.
Publication remains explicit between plans. No overlap of serving and mutation,
automatic future-result queue or indefinite availability is promised.

## Required invariants

- One owner-approved strict JSON plan, externally hash-bound, with a bounded
  lease count, original total wall horizon, and explicit aggregate CPU, accepted
  attempt, response-payload and log allowances. Bound plan/report sizes and counts.
  Exact hashes identify selected inputs; they do not authenticate an untrusted
  download or grant source/disclosure approval by themselves.
- Reserve all per-lease allowances up front. CPU for the nested public launcher
  must be included in an outer per-lease Job; count outer Job usage once and the
  final runner separately. Memory/process caps are simultaneous, not sums. Payload
  caps are not total wire bytes; sampling/cleanup overshoot remains explicit.
- One finite plan, fresh output root, no resume or automatic retry. Atomically
  claiming that root prevents two invocations of this plan's output. Existing
  owner locking still handles different plans selecting the same catalog. Never
  delete locks or claim cross-catalog store serialization.
- Validate all selected paths/configuration and their disjointness before output
  creation or launching. Preserve the launcher's ordinary absolute-path/no-reparse
  protections, including the index and all selected files. Stable nonzero port,
  deliberate whole-custody/exclusive approvals, existing index and unchanged
  hash-bound configuration across all epochs. No automatically inferred endpoint.
- Use existing approved package launcher and Job supervisor only after verifying
  their known source/manifest bindings. No experiment supervisor is a production
  dependency. Helpers may be loaded from checked bytes; no arbitrary module hook,
  caller-provided executable or test-double mode belongs to the public interface.
- Each child selects fresh diagnostics and output. Before launching a child,
  record its intent and require enough original horizon for its fixed allowance
  and cleanup. Run the unchanged public launcher under existing Job supervision;
  cancellation/failure cannot permit another epoch while ownership is uncertain.
- Continue only after actual outer and inner clean closure, no termination
  requested, no active/terminated descendants, and matching actual RUN/peer
  reports. Require `LEASE_FINISHED`, `quiescent=true`, no close/cleanup/budget/write
  errors, exact state/profile/config bindings and internally consistent provider
  counters. Read bounded raw reports; exit zero/READY is insufficient.
- Stop after any failed or missing service report, source/config change, exhausted
  original horizon or aggregate budget, accept-owner failure, or cleanup uncertainty.
  Preserve partial files and all completed epochs. An unknown result is not
  rollback or a mathematical rejection. Ordinary failed client requests and quota
  exhaustion are not failed service cleanup. Record them and permit the next
  already-prepaid epoch after clean closure: all N epoch allowances are explicitly
  authorized up front, including this case. Never add an extra epoch or allowance.
  Stopping the entire plan on one malformed request would be an avoidable denial
  of service. The old provider cannot distinguish every byte-quota refusal from
  other request failures; do not invent that distinction in reports.
- Report planned vs observed costs, finished count, terminal reason and exact
  bindings. Do not claim uninterrupted service: startup gaps, quota exhaustion,
  unavailable networks and other operators remain outside that guarantee.

The accounting argument is finite composition: if each epoch is authorized once,
the sum of reserved epoch caps fits the selected aggregate allowance, and only
clean terminal epochs authorize the next, neither failure nor success renews the
original allowance. This does not turn sampled ceilings into exact hard bounds.

## Ownership and finite evidence gate

`service_lifecycle` owns only new `service_plan.py` and README.md here. Root owns
this contract, integration/selection/checkpoint, actual launches and Git. Separate
agents own focused tests and complete source review; no shared NOW/WORK/CURRENT,
paper work, old code, existing state or evidence may be edited.

First finish/review source. Tests should cover plan/refusal/report sequencing
without native work, then one tiny genuine two-lease loopback execution if safe
fresh inert fixtures can use the unchanged public CLI. Synthetic fixture state
is never evidence of admitted mathematics; do not copy mutable historical owner
state or silently build new Lean support. If genuine public setup needs native
initialization, report that cost before selecting it. No runtime is selected yet.

Stop this work after the narrow orchestration boundary is established. Do not
extend into publication scheduling, a general daemon, permanent service renewal,
concurrent storage, or a new proof campaign. Full deployable v5 stays unfinished.
