# Read remote mathematics through ordinary APIs

`remote_reader.py` composes the existing runtime factory, validated client and
direct contacts. One bounded operation asks an owner-selected service for a
formal query, selects one returned candidate, acquires/verifies its packet and
imports its available semantics. It contains no theorem ID, fixture directory,
proof-production call, authoring routine or mandatory research task.

Use `main(context)` as a trusted owner entry through `client.launch` / `boot`.
Select its exact source closure, including `runtime`, `direct_contacts`,
`workspace_validated` and `serve_workspace` (only its existing workspace-close
helper is reused; no server starts). Existing mathematical owners enforce their
own source/runtime pins. The enclosing Job is required and is not a hostile-code
sandbox.

## Caller-supplied parameters

The launcher `parameters` has exactly:

```text
schema: "DMKN_V5_REMOTE_READER_V1"
runtime_adoption: RuntimeProfile's locally adopted runtime configuration
workspace_path: absolute canonical persistent workspace path
workspace_config: exact validated/evidence workspace configuration
create_workspace: boolean, explicitly fresh or explicitly reopen
operation_limits: existing Workspace grant limits
foundation: {path, bytes, sha256}
query:
  contacts: local label -> {host, port, tls, server_name}
  egress_policy: existing OwnerEgressPolicy configuration
  specs: existing formal query specifications
  search_limits: existing SearchSession limits
  contact_lifetime_ms: positive finite contact lifetime
  selection:
    provider: one configured local contact label
    partition_index: zero-based ordinal among returned nonempty partitions
    start: position in that selected partition
    candidate_index: zero-based ordinal in this one page's returned matches
    packet_index: zero-based ordinal in this candidate's offered packets
  offer: {max_bytes, max_expanded_bytes, max_age_ms, attempt_timeout_ms}
  page: {limits: existing positive-candidate page limits, attempt_timeout_ms}
  packets: {max_offers, max_bytes}
  admission: {native_cpu_seconds, receipt_cpu_seconds, wall_seconds, memory_mib}
```

Use RUNTIME.md, API-EVIDENCE.md and DIRECT-CONTACTS.md for unchanged schemas and
owner requirements. The runtime mode is explicitly **validated**; A is required,
I optional. Configuring an A verifier is not evidence that an A receipt exists.
The actual returned packet determines which unchanged mathematical owners run.
`authoring=False`: this entry never prepares a new proof.

The workspace must be disjoint in both directions from the installation, current
run and selected source snapshots. Its parent must exist when creating it.
It is a persistent sibling of a fresh run, not scratch below `run/work`.
Frozen evidence must not be used as mutable workspace input. Source choices,
paths, configuration and budgets come from the local owner, not network replies.

## Deliberately small selection policy

The operation makes exactly one configured-provider offer request and at most
one candidate-page request. It picks the explicitly supplied ordinals in the
actual returned data; zero selects the first. It scans only bounded returned
partition metadata to exclude empty partitions, not the corpus. It neither
scans further pages/providers nor retries a refusal. Ordinal selection is a
simple example strategy, not a mathematical usefulness measure.

If selected, the candidate's exact packet offer is acquired through unchanged
real admission before any semantic import. No target ModuleID is supplied in
the query-selection schema. The result ID comes from the authenticated returned
record; authenticated indexing alone does not make that result mathematically
valid. Native deltas may still require their bounded unsealed ancestry.

This example imports all members of its one admitted packet using their actual
exact journals and available committed semantics. It does not choose between
conflicting journals or optimize a dependency slice; unchanged import rules
can refuse. Terminal certified evidence may need separately acquired semantics.
Missing groups/bodies produce `NEED_SEMANTICS`; no automatic resolver, provider
refresh or new allowance is invented.

## Outcomes and continuation

The standalone entry writes `run/work/remote-reader-result.json`. Top-level
`COMPLETED` means the finite procedure and cleanup finished normally, not that
a theorem was found. Inspect `read.status`:

- `READY`: actual live admission followed by semantic-context materialization.
- `NEED_SEMANTICS`: warranted data was acquired, but this example cannot finish
  its import with available semantics.
- `MISS`: the selected bounded offer/page/ordinal supplied no chosen result.
- `REFUSED`: the selected provider attempt was refused.

No outcome establishes global absence, completeness or usefulness. The saved
report contains no transferable warrant; `mathematical_acceptance=False` refers
to this operational artifact, not a denial that its live owners checked data.
Top-level `FAILED` preserves an error or uncertain cleanup; result-write failure
raises. Exit zero means `COMPLETED` with any of the four outcomes above.

For an agent that needs to continue inside the same live operation:

```python
result = await remote_reader.read(client, query)
if result["report"]["status"] == "READY":
    context = result["context"]  # same-client opaque reference, not JSON
# Missing semantics: inspect demands, use result["candidate"]/["warrant"],
# and the existing resolve_declaration/acquire_body/import/extend APIs.
```

The helper does not close the caller's client. Its candidate, warrant and context
references expire with that client. The standalone `run/main` instead closes all
owned state and persists only the JSON report; it cannot later resume those
handles. The standalone grant ends no later than the original outer deadline
minus five seconds for ordinary cleanup, never a renewed allowance. Actual
hard containment and closure evidence remain the enclosing launcher's role.

This connects existing data service to usable mathematical imports. It does not
establish new theorem generation, positive full-cost growth, genuine aggregate
certification, independent hosting or completion of v5.
