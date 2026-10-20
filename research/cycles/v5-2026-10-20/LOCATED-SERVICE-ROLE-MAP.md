# Reuse the existing optional location role

2026-10-20, source/manifest mapping only. No runtime, tree-wide hashing, copying,
installation, build, test or RAM investigation was performed.

## Decision and current-installation distinction

Reuse the already retained location runtime at
`E:\Distributed Trustworthy Mathematical Knowledge Network\product-local\v4-library-commons-02\commons-v4`.
The existing `AdoptedLocationRuntime` constructor accepts this explicit root
separately from the source and mutable workspace roots. No new runtime package
or second Node stack is needed on this PC.

**Do not use the current distribution's `context.installation` blindly.**
`product-local/v5-distribution-03/Mathematical Commons v5/V5-RELEASE.json` now
declares `base_role: mathematical-client-v1`; its `base/runtime/node/node.exe`
is absent. `DISTRIBUTION-ROLES.md` correctly maps the separable roles, but its
earlier "future projection" wording predates this installed projection.

The retained full root contains `runtime/node/node.exe`, observed size
92,279,112 bytes. Its unchanged release-manifest row specifies SHA-256
`b3094d0b49f9ad602262a9921551737bb97637c05dd357a06ae98188d7290aa3`;
this is a retained expected pin, **not a new hash of that binary**. The fixed
manifest SHA is
`a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed`.

## Existing exact APIs and source evidence

- `portable_runtime/location/controller.py:62` defines
  `AdoptedLocationRuntime(source_directory, source_pins, *, installation_root,
  workspace_root)`. Its nine `SOURCE_NAMES` are the base JavaScript modules.
  `verify()` selects exactly 5,896 `overlay/` and `runtime/node/` manifest rows,
  requires exact subtree census and validates their bytes (130,118,221 bytes per
  the existing role map). Reuse the complete selected role; do not prune npm
  dependencies or bypass its mandated pre/post checks.
- `portable_runtime/location/controller_services.py:19` defines
  `ServiceLocationProcess(adoption, role_pins, configuration, evidence, *,
  deadline)`. Five `ROLE_NAMES` add maintained roles, role composition/entry
  and service composition/entry. Use this service class; the portable base
  `LocationProcess._start_core` deliberately refuses direct launch.
- `client/launch.py:23,133` requires all **21** portable location source files
  in the boot plan, not merely the fourteen JavaScript launch pins. The retained
  `experiments/v5-local-checks/client-retained-reuse-01-plan.json` already records
  that exact source closure and the full retained installation root. For example,
  portable controller is pinned `4dc0824d...`, service controller `8591c49d...`,
  maintained roles `9824559f...`, and Node service entry `2eae8676...` there.
- `client/boot.py:17,177` already exposes `sources_portable`, `source_sha256`,
  `location_workspace`, `installation` and the original absolute `deadline`.
  The source map is enough to derive both exact JavaScript pin sets without
  inventing a pin or importing a second location package.
- `client/actual_owner03.py:202` and `client/terminal_strategy.py:284` already
  compose these objects. They are source examples, not a reason to rerun their
  mathematical workloads. `node_entry_services.mjs` already supports bounded
  `publish`, `withdraw`, `status` and `stop` commands.

## Only the next wiring gap

The ordinary HTTP service must accept an explicit optional owner-selected
location installation root; construct the existing adoption from that root,
the pinned portable source directory and fresh mutable service output. HTTP
must bind first, so the `index-provider` config advertises the actual selected
HTTP endpoint and the workspace's exact formal namespace.

Existing configuration fields are `schema`, `role`, fresh `state`, `namespace`,
`egress`, `listen`, `announce`, `bootstrap`, `endpoints`, `limits`. The fixed
schema is `DMKN_V5_MAINTAINED_LOCATION_ROLES_V1`; provider role is
`index-provider`. Existing validation requires one listen address, at most four
advertised HTTP endpoints, owner-approved bootstrap addresses with peer IDs,
bounded transport/query/metadata/service limits and the TTL/reprovide margin.
Public mode already requires explicit announce addresses; it supplies no NAT
traversal or universal reachability guarantee.

Use fresh, disjoint state and evidence paths below the boot work directory and
the original service deadline with cleanup margin. Advertise only caller-chosen
finite feature/stripe routes; do not add automatic global topic enumeration.
Stop/drain location before HTTP and workspace closure, including partial-start
failures. A dispatched hint is still advisory, not acknowledged replication.

Thus the next work is a small optional service composition/lifecycle seam, not
runtime installation or new discovery theory. An independently distributable
location-role package remains a later packaging obligation; local reuse of the
existing full root does not establish portable public distribution of that role.
