# Selected implementation: incremental inert host

2026-10-28 root selection. Canonical root is
`E:\Distributed Trustworthy Mathematical Knowledge Network`; every shell uses
that explicit workdir and every edit uses its absolute canonical path. Read
AGENTS.md. No native build, owner access or runtime is selected by this note.

The concrete workflow is an independent custodian accepting successive selected
inert bundles, preserving earlier knowledge and serving from one retained host.
The earlier immutable host permits only 64 lifetime targets and no append.
Current owner publication is preferable for owner-backed collections, but does
not implement this independent role. Static shards avoid repeated byte copies
at the cost of more roots/services/contact slots. The existing stores already
support atomic idempotent inserts and bounded indexed access.

Root adopts the principle in
`ordinary_connect_ownership/INCREMENTAL-HOST-INVARIANT.md`, with independent
reviewers' explicit in-principle agreement. Exact whole-batch generation seals
are not necessary for a role that preapproves partial disclosure. Use the
custody -> preview -> index invariant and one permanent host lock. A stopped
process leaves a permitted committed prefix; later service makes no assertion
that the interrupted batch completed. No intent/recovery subsystem is selected.
Final independent challenge may still identify a concrete blocker before runtime.

## Interface selected for disjoint implementation

Preserve `prepare` and `serve` for static hosts created by the current profile.
Add `init` and `append` for fresh incremental hosts; no old-root migration.
Both use the existing HOST.json location and --host-sha256 option, whose V2
meaning is a stable configuration identity, explicitly not current content.

- init config: schema `DMKN_INCREMENTAL_HOST_INIT_V1`, custody_limits,
  index_limits, partial_publication:true. Create empty stores, verify metadata,
  close them, then atomically install the stable descriptor. Failed uninitialized
  roots are preserved and are not usable; no initialization recovery is promised.
- descriptor schema: `DMKN_INCREMENTAL_HOST_DESCRIPTOR_V1`; profile_sha256,
  semantic_id, namespace, custody_limits, index_limits, partial_publication:true,
  assurance and mathematical_acceptance:false. No lifetime target list/count seal.
- append config: schema `DMKN_INCREMENTAL_HOST_APPEND_V1`, bundle_directory,
  manifest, targets, share_all_bundle:true, allow_partial_publication:true;
  optional existing bundle_limits. Require the descriptor pin and exact limits.
  Validate each stored unit against the approved manifest; <=64 targets per call.
- serve retains its existing config. V1 checks sealed counts/head as before;
  V2 selects current committed metadata/snapshot while holding the same lock.
  Reports distinguish stable descriptor identity and current content snapshot.
- Python helper: initialize(loaded, host_root, config, allowance,
  profile_sha256=..., finalize=...); append has the same parameters plus
  expected_host_sha256. Existing prepare/serve signatures stay unchanged.

The existing 64 MiB bundle ceiling and all fixed cumulative store capacities
remain. No global-size-independent claim for SQLite open/recovery, producer
export or broad search. Duplicated supplied bytes are charged. No automatic
retries, daemon, new wire protocol, mathematical acceptance or certificates.

## Ownership and evidence

- operable_scale_decision: fresh custodian.py and implementation contract here;
  no other source, Git or runtime. Start from unchanged dedicated_host source.
- root: fresh host.py/run.py public integration, HOSTING.md, later map/profile
  and explicit bounded runtime selections, adoption and Git.
- growth_design_audit: principle challenge then changed-boundary source review.
- query_scaling: finish payoff comparison; then disjoint minimal focused control
  source/plan after confirming these interfaces. No broad theorem experiment.

Keep used predecessors and evidence unchanged. Small controls must exercise
partial committed prefixes, re-opened service, duplicate/conflict behavior,
profile/limits/lock/refusal, cumulative targets beyond 64, and initialization
failure. Reuse existing valid inert evidence and native checking outcomes.
Only a new-boundary public host continuation is a candidate for later execution.
Do not repeat transport, proof or full network campaigns.
