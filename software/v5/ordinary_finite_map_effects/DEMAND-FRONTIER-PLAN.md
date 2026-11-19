# Optimistic ancestor frontier for contribution

Source-only checkpoint, 2026-10-26; canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
No implementation, native execution, owner access or Git mutation occurred.
P means `experiments/v5-local-checks/kernel-admission-package01/distribution/package`.

**Recommend this bounded auxiliary correction over compiling/copying received
theory source for the next inert-reuse workflow.** Keep the current publication
and source preparation usable. This removes eager ancestor acquisition without
claiming exact installed-module correspondence or creating durable module anchors.

**Input and authority.** Add optional contribute-only
`--authoring-frontier-root`, requiring the existing approved project backend.
Under the same owner lock, open that root through `owner.catalog.context` and
require its authenticated module plan to be an exact prefix of the selected
parent's plan. The frontier expresses an expectation that approved imports supply
these names, not evidence that they do. The descriptor's module names/search paths
cannot establish presence; project code/plugins remain owner-approved execution.
Charge the additional catalog traversal; existing artifact validation can reuse
its process-local cache. No installed-environment census is needed.

**Exact delta and wire.** Use fresh successors of these P files:

- `owner.py`: parse/validate/pass the optional root; reject it elsewhere.
- `authoring/py/ordinary_contribution.py::contribute_source`: authenticate the
  prefix, pass a frontier lookup, merge reached labels into prepared bindings,
  and record the root in existing `REQUEST.project_authoring` metadata.
- `authoring/py/portable_owner_request.py::prepare`: before enqueue/fetch, stop
  at an exact name/ID present in both contexts; record only reached cuts. Exclude
  cuts from topological dependencies. Preserve acquired target triples and their
  existing export/unit validation; never substitute an ID or infer a namespace cut.
- `authoring/py/retained_preparation.py::reconstruct_preparation`: recover the
  additional labels with the same current-parent warrant checks, preserving the
  existing extraction/completion route.

Without the flag, retain exact V2 behavior/wire. With it, emit
`DMKN_OWNER_REQUEST_V3`: the seven V2 fields plus `frontier_root` and
`frontier_labels`, the latter sorted unique `[name, export_id]` pairs disjoint
from basis/group outputs. The controller binds both fields to its authenticated
selection and pinned header. Retained metadata must agree with the header.
Keep 32 fetched groups, 4096 aggregate basis/frontier/group names, 1-MiB header
and group bounds, 4-MiB acquisition/payload bounds and existing node/edge limits.

In `software/v5/ordinary_lean/PortableOwnerConstructCommand.lean`, parse V3
explicitly alongside unchanged V2. Pass labels as a separate optional parameter
to `OwnerConstruction.constructPrepared/makeIndex`; leave `OwnerRebind.Prepared`
unchanged. Index labels without construction packets. In `demand`, a reached
frontier name must already have safe kernel/frontend presence; missing/hidden
names fail once, without automatic fallback or another allocation. Preserve
whole fetched groups, partial-existing-group refusal and exact private names;
never synthesize missing siblings or promote hidden records. This promises no
restoration of notation, instances or other original frontend metadata.

**Why no probe.** Native presence need not be established before an optimistic
scratch cut: absence safely fails in the existing single authoring invocation.
A batched probe knows only names already discovered; recursive absent groups can
reveal more. Completing it requires another probe, a broad cached inventory, or
a persistent demand protocol. Iterative compilation pays import/startup repeatedly.
None is needed for an explicitly chosen Std ancestor.

**Acceptance.** Labels designate intended receiver meanings. Wrong claimed IDs
refuse; same-name semantic differences may fail elaboration or final checking,
but need not universally refuse when the resulting candidate is valid under the
real parent. Keep `portable_candidate.bind_candidate`, preflight and exact-parent
native admission unchanged and mandatory. Exported partial imports retain exact
protected IDs; unused requested targets remain allowed by existing policy.

**Build footprint.** Rebuild only OwnerConstruction, PortableOwnerConstructCommand,
PortableConstructExportCommand and PortableContributionExportCommand, in order;
reuse unchanged helpers. Avoid `ordinary_package/build.py`'s full two-lane rebuild.
New profile/pins are required; all eight admission modules, installed manifest
and implementation I can stay byte-identical. Changed owner/request paths change
anchor-support identity; preserve old-package anchors without migration.

**One meaningful control:** a paired small end-to-end fixture constructs a received
definition above the frontier with zero ancestor-evidence fetches, then checks its
successor. A same-name imported definition variant makes a locally valid successor
false under the protected parent: final admission must refuse. Missing demanded
frontier names must fail closed. Ancestor fetching, additional compilation rounds,
or acceptance of that invalid successor falsifies the design.
