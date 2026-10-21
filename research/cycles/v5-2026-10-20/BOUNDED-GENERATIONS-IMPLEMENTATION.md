# Implement sustained custody without an unbounded history

2026-10-21, root. Source-only selection following the already specified
PLACEMENT-LIFECYCLE-SEAM and PLACEMENT-LIFECYCLE-SPACE-BOUND. This is not another
status survey or a new retention design. Consolidated installation/restart
qualification proceeds independently and must not include these unused sources.

## Why this is the next software boundary

The consolidated service can retain and rediscover a sealed generation, but its
finite immutable stores eventually fill. Reopening does not reclaim capacity.
Continued reciprocal contributions therefore need a bounded replacement cycle,
not larger page caps or an indefinite service lease. Implement the existing
two-slot design; retain explicit refusal whenever safety cannot be established.

Use the consolidated 121-source map, including retained advertisement5aa23ee7,
service7e735337, controller ef1c9b59 and ledger d955990c. No changes to any used
source, fixture, installation or evidence. Do not reimplement advertisement,
native caching, discovery, certificate production or the placement transaction.

## Selected source work, with a concrete composition requirement

Fresh `software/v5/bounded_generations/placement/lifecycle.py` and
`software/v5/bounded_generations/client/serve_generations.py` may implement the
owner-local registry and composition of the exact existing PlacementService.
Add a small profile/clock helper only if keeping these modules comprehensible
requires it. Checkpoint BOUNDED-GENERATIONS-SOURCE.md in this cycle.

The registry owns exactly two slots, bounded monotone allocation sequence and
retired floor, original generation horizons, finite per-generation run allowance,
and durable intent/closure phases. Allocate before creating a managed generation;
reserve a run before its fresh locator directories; failures remain charged.
Start/reopen must consume the current registered identity and exact configuration,
never create an absent old generation. No saved token/deadline grants authority.
New runs use fresh explicit finite owner authority and preserve original charges.

Compose existing services directly: distinct endpoint/location roles, no shared
locator rewrite. Seal only with the current idle owner. Persist retirement intent,
then require actual exact-role closure and a conservative adopted time lower bound
at least the original retention horizon, before durable RETIRED. Unknown recovery
closure remains held, never inferred from a lock, PID absence or free port. A
retired record cannot be reopened. Two occupied slots forbid a third generation.

Implement safe source-level planning of reclamation, but **no deletion invocation
is selected now**. Actual reclamation needs a separately reviewed exact ordinary
managed-path/marker/file-inventory boundary and finite authority; no broad-root
recursive deletion. A slot cannot become FREE merely because retirement was
recorded. Unknown files, links or incomplete cleanup keep it occupied and charged.
Preserve all current project data. Later focused fixtures must be newly enrolled
manager-owned paths, never any existing experiment or product directory.

Reuse the existing supported-storage argument, not a disk-filling experiment.
Bounded logical records are not a physical quota. Keep page/journal/temp/output
requirements explicit; if exact selected runtime/VFS correspondence is needed
to enable a physical-envelope claim, name that concrete dependency rather than
inventing a coefficient or silently making it an adopted fact. No memory survey,
system tuning, cloud use, dependency rebuild or large benchmark is selected.

## Ownership and economy

Canonical root E:\Distributed Trustworthy Mathematical Knowledge Network;
explicit workdir, absolute apply_patch edits, guard/AGENTS and no subagent Git.
Core_release completes actual consolidated-build audit first, then authors the
small lifecycle/composition cut above. Root owns decisions and integration.
Support_guest reviews the lifecycle source after its current smoke review;
support_screen can author disjoint focused controls after smoke completion.

Before runtime, require the exact composition and clock/closure/reclamation
boundaries to be reviewed. Tests should distinguish early retirement, live/unknown
actors, cap exhaustion, crash-intent recovery and stale generation identities,
not repeat the passing math or network campaigns. No new runtime is selected by
this note. The intended result is a working bounded custody lifecycle; neither
that result nor storage boundedness proves net growth or completes final v5.
