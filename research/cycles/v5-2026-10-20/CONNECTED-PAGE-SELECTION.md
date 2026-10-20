# Provision the retained page reservation and preserve partial evidence

Root, 2026-10-20. Actual02 remains failed and frozen. Both roles reached READY;
the installed public service itself reported PASS, 13 health observations and
clean closure, but the overall discovery test failed with page EOF. It is not
reclassified as a complete installed-search pass.

The existing atomic provider inherits the delta composite HTTP handler.
For the legacy page route, that handler reserves 1,048,576 reply bytes,
independently of the smaller client page limit. Its offer had already charged
1,973 bytes. With a provider total of 1,048,576, the next request necessarily
violates its cumulative quota before dispatch. This is a source-derived cause
consistent with two observed HTTP requests, one failure and no page reply;
the handler did not log an exception code. It is not a host memory failure.

Select one narrow fresh caller successor `installed_service_check03.py`:

- Fresh inner name; preserve all earlier used adapters and evidence.
- Provider total reply allowance `1 MiB + 65,536`, the sum of the selected
  offer maximum and the retained legacy page reservation. Do not change the
  product's reservation policy, client query grant, CPU/time/memory/process
  limits, or any mathematical acceptance condition.
- Save route, descriptor, offer and page observations immediately after their
  successful returns. Preserve the final workflow accounting even on failure.
  Reporting failure stays visible and cannot overwrite the primary cause,
  renew an allowance or become success.

`core_search` owns the fresh adapter and source-cause note. `core_release`
audits saved actual02 and independently reviews the exact03 delta. Root owns
`Select-InstalledService03.ps1`, differing from02 only in the linked adapter
source/invocation and fresh outer name.

After exact clearance, root may select03 once within the unchanged finite
envelope and unchanged verified installation. No product rebuild, new prover,
memory investigation or rerun of passed mathematical campaigns is involved.
The page reservation optimization is not a separate selected product task.
The principal next implementation decision remains the typed-DAG refinement,
not a growing collection of hosting conveniences.
