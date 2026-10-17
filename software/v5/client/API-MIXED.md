# A-capable commons client

This explicit client joins the existing aggregate verifier, mixed-packet receiver,
atomic imports, custody, search and authoring APIs. It does not add a checker or
produce a cryptographic proof. The frozen `workspace_atomic.py` remains I-only.
Source implementation is not evidence of genuine aggregate acceptance; that
requires a separately selected actual receipt and runtime gate.

## What I and A mean

- **I:** an individually certified module under the fixed module relation.
- **A:** an aggregate certificate containing exact module journals, selected
  through authenticated member openings. A member is not an I receipt.
- **Mixed packet:** one or more new native-checked module extensions with I/A
  certified frontiers. The existing parser requires at least one extension.

Use `client.workspace_mixed.Workspace` when a locally adopted A verifier is
available. A is mandatory; I is optional. The configuration cannot silently
switch proof formats or adopt an image supplied by a remote peer.

## Open a fresh workspace and reserve one operation

The configuration has the same fields and finite storage limits as the atomic
client, except these two explicit values:

```python
from client.workspace_mixed import Workspace, SCHEMA
from mixed_network.custody import public_profile

config["schema"] = SCHEMA  # DMKN_V5_CLIENT_MIXED_WORKSPACE_V1
config["wire_profile"] = public_profile(locally_adopted_aggregate_image)
workspace = Workspace.open(fresh_absolute_directory, config, create=True)
grant = workspace.reserve(operation_limits, outer_deadline=original_deadline)
```

Other configuration fields are `module_limits`, `packet_limits`, `index_limits`,
`packet_envelope`, `max_operations`, `max_report_bytes`, and `ledger_pages`.
Reopening requires the exact same configuration. It restores bytes and history,
never a grant, issuer handle or mathematical warrant. Do not open an I-only
workspace with this schema or migrate its database in place.

The trusted caller constructs actual owners **after** reserving the grant, within
its actual enclosing Windows Job. No factory is hidden in the client:

```python
client = workspace.operation(
    grant,
    aggregate_owner=actual_A_owner,
    delta_owner=actual_mixed_owner,
    receipt_owner=actual_I_owner_or_None,
    preparation_owner=actual_preparation_owner_or_None,
    foundation_bytes=exact_foundation_bytes,
    foundation_sha256=exact_foundation_sha256,
)
```

Owner classes must be exactly `AggregateReceiptVerifier`, `MixedDeltaVerifier`,
optional `ReceiptVerifier`, and optional `MixedOwnerPreparation`. The mixed
owner must hold those very same I/A objects as `(I_or_None, A)`. Its selected A,
the A owner's image and the workspace wire profile must agree. Owner attempts
and handles are pristine; deadlines cannot exceed the original grant. Only a
successful `operation` return transfers ownership. On construction failure,
the caller is responsible for closing its owners and the untransferred grant.

All admission CPU/input caps fit the acquisition suballocation; the mixed
operation count fits `verify_attempts`. A's controller/output caps fit the
grant, and its member call/storage/byte caps fit `imports.max_calls`,
`imports.max_members`, and total input bytes, respectively. Preparation CPU
plus acquisition CPU must fit the total worker allowance. Nested issuer
counters describe the same work; do not add them as independent worker totals.

The selected runtime/source closure must include the frozen atomic base and the
new mixed module. Configured owner pin maps must cover `client/__init__.py`,
`client/workspace_atomic.py`, `client/workspace_mixed.py`, and the mixed-network
package, custody and transport modules, in addition to the existing complete
verifier/import/authoring closure. Actual import origins and these pins are
checked. The owner-controlled installation/Python process remains trusted;
resource Jobs are not hostile-source security sandboxes.

## Admit exact aggregate members

```python
warrant = client.admit_aggregate_member(
    receipt_bytes, expected_header, exact_journal, member_index, sibling_digests,
    cpu_seconds=30, wall_seconds=60, memory_mib=1024,
)
member = client.describe(warrant)
```

The header is exactly 192 bytes; the journal exactly 184 bytes. Siblings are an
ordered list of 32-byte digests. The existing bindings check header/profile and
membership structure; actual receipt verification supplies mathematical warrant.

The first receipt calls the real A verifier. Another member of exactly the same
receipt/header can reuse that live aggregate handle. The cache key includes A,
owner profile, receipt hash and length, and exact header. Every call still charges
its supplied receipt/header/journal/index/path bytes and invokes the real
`select_member` for the requested journal, index and ordered path. There is no
member-token cache that could confuse different members. Later warrant uses
revalidate the genuine issuer handle. No saved success record can enter this path.

`describe` identifies this warrant as `A-member`, not `I`. Its bytes remain exact;
internal comparison copies normalize the known journal/header/path fields only.
Returned dictionaries are inert descriptions, not transferable credentials.

`admit_receipt` remains available when I was configured; without I it fails
explicitly. Direct I, direct A and mixed admissions spend one shared
`AcquisitionBudget`. A cache hit saves receipt verification, not member/controller
work or input charging. Mixed admission reserves
`claims * receipt_cpu_seconds + deltas * native_cpu_seconds`; the existing
600-CPU-second per-admission ceiling remains. Nothing splits work into new grants
or retries a refusal automatically.

## Import, investigate, extend and publish

For direct A members, `semantic_material(warrant)` reports
`NEED_CALLER_OR_PROVIDER_SEMANTICS`. A receipt authenticates commitments; it does
not supply declaration openings or transparent bodies. Supply the selected exact
journals and authentic semantic material to the unchanged atomic import path:

```python
ready = client.import_context(
    [{"warrant": warrant, "resolutions": None}],
    selected=[exact_journal], openings=group_openings, bodies=required_bodies,
)
```

Inspect `status` and `demands`. When incomplete, use `extend_context` with the
returned context and demanded material. A ready context is sealed: subsequent
authoring uses the same immutable selection. `author` requires the separately
configured preparation owner and produces the existing mixed packet, not a new
succinct certificate. Independent local agents decide what to investigate.

`publish(packet, export_names, retention_policy={"mode":
"quota-bounded-local-custody"})` preserves exact packet bytes, selected semantics
and formal index records. Publication is structural custody, not mathematical
acceptance. Partial cross-database publication has explicit intent/outcome
records and the inherited `reconcile` path; it is not falsely reported atomic.

## Search and independent reuse

The existing `find`, `search_offer`, `search_page`, `resolve`, `packet_offers`
and `acquire` workflow is retained. Routing contacts and results remain advisory.
The mixed acquisition uses the same original query/acquisition grant and the
locally selected mixed profile, followed by actual mixed verification.
Serve the workspace with the existing `mixed_network.transport.CompositeProvider`.

This version's remote packet target is the **last substantive extension**, not a
bare aggregate member. Direct A admission is a local/bootstrap entry point. After
an extension, the resulting mixed packet carries its A frontier and new delta to
independent recipients. Do not invent a wrapper theorem to pretend bare A members
are already a supported remote target. No global discovery completeness claim
follows from bounded search.

## End every operation

```python
report = await client.close()
workspace.close()
```

Calls are serialized. Cancel and await any outstanding call before closing.
Failure, expiry or changed owner identity stops use and clears client warrants,
caches, candidates and context references. Failure and close explicitly close
all originally transferred issuers, including A; replacing an attribute does
not strand its original owner or transfer ownership of the replacement.
Async channel cleanup completes in `close`, so it is still required after failure.

A cleanup exception remains `cleanup_uncertain` even if a later close succeeds.
The workspace is poisoned against a new grant; reopening does not turn the old
operation into success or revive its handles. Reports use original owner
accounting, identify absent I as `None`, and remain historical data rather than
proof. Actual enclosing Job closure and any unmeasured tail are caller evidence.

This seam does not itself establish economical A production, genuine public A
reuse, independent hosting or full v5 deployment readiness.
