# Caller-directed acquisition of mathematical semantics

`semantic_reader.SemanticReader` is an optional local helper over the existing
**exact validated client**. It takes one already returned candidate and helps
the caller acquire its selected dependency data before expensive verification.
It does not search automatically, choose a theorem or variant, synthesize a
proof, create a new grant, renew contacts, or establish new mathematical trust.
The previously used `remote_reader.py` remains unchanged.

The sequence is:

```text
caller-selected candidate and offered packet
  -> stage exact untrusted evidence
  -> preview missing semantic data
  -> caller explicitly resolves selected demands
  -> structural closure
  -> actual admission of each selected packet, once
  -> unchanged live import
  -> usable same-client context only if that import is READY
```

The local agent still decides what to investigate, which demands to fulfill,
which offered packet to choose, and whether to stop. There is no global task
list or interpretation of human intention.

## Construction and ownership

```python
from client.semantic_reader import SemanticReader

reader = SemanticReader(client, candidate, limits={
    "modules": 8, "names": 64, "groups": 64, "bodies": 128,
    "steps": 256, "data_bytes": 4 * 1024**2,
})
await reader.stage(candidate, explicitly_chosen_packet_offer)
preview = reader.preview()
```

`client` must have exact type `client.workspace_validated.CommonsClient` and
be live under its original grant. `candidate` comes from that client. The
caller owns the enclosing process/resource containment and must serialize
all use of this client, including calls made outside the helper.

All six limit fields are required positive integers. Ceilings are respectively
128 modules, 4096 names, 4096 groups, 8192 bodies, 65536 steps and 16 MiB of
canonical retained data. The module and data ceilings must also fit the
original import grant's `max_members` and `data_bytes`; packet roots separately
obey its `max_sources`. These are maximum supported values, not recommended
allocations. Choose smaller limits for the intended operation.

The helper borrows the client; `reader.close()` only discards helper data.
The caller must still close the client/workspace through its ordinary lifecycle.
No saved helper report or token can resume a finished operation.

Select `staging_members/workspace_staged.py` under the existing logical source
key `client/workspace_staged.py`, alongside the new helper. This selected
successor adds a bounded structural packet-member inventory and explicit
member preview; it preserves target-only preview when the optional selection
is omitted. Frozen predecessor files remain unchanged.

The new helper belongs in the normal selected trusted-owner source closure.
It does not load an alternative verifier or replace the client's exact adopted
runtime/source checks. This is not a hostile-source execution sandbox.

## Explicit incremental operations

| Call | What it does |
|---|---|
| `await stage(candidate, entry)` | Stage exactly the caller-selected offered `{packet_sha256, packet_bytes}`. First stage is the original candidate. Later stages must address a current `NeedModuleEvidence` demand previously resolved by this helper. |
| `preview()` | Invoke existing structural preview on all selected tokens/groups/bodies. Return only status, detached demands/cost and `mathematical_acceptance=False`; never a context. |
| `select_member(packet_module, exact_journal)` | Explicitly select a demanded internal member from the already staged packet's returned inventory. The journal is immutable 184-byte `bytes`, not a guessed module ID. |
| `await resolve(demand, max_bytes=n)` | Resolve one exact demand from the latest preview through the original candidate's provider. Reuse an already resolved exact module/name. Retain its group if that module is already selected. Return `{status, candidate, description}`. |
| `await fetch_body(demand, max_bytes=n)` | For a current `NeedBody`, fetch its exact committed body using the previously resolved candidate. Its module must already be selected. |
| `finish(admission, resolutions=None)` | One-shot actual checking of all selected staged packet tokens, followed by unchanged live import of chosen journals. Requires a READY preview at the current data revision. |
| `report()` | Inert state, step/count/data information. No handles or mathematical authority. |
| `close()` | Discard only this helper; cannot interrupt an active helper call. |

For `NeedDeclaration`, explicitly call `resolve`; it retains the newly acquired
group. For `NeedBody`, call `resolve` first if necessary, then `fetch_body`.
For `NeedModuleEvidence`, inspect the `members` returned by earlier `stage`
calls. If the needed module is already represented inside a staged packet,
choose its exact journal explicitly:

```python
reader.select_member(containing_packet_module, chosen_member_journal_bytes)
await reader.resolve(chosen_demand, max_bytes=65536)
```

This selects structural metadata, not a standalone I/A receipt. It does not
perform another packet transfer or admission. The resulting group may still
demand more declarations or bodies.

If the needed module is not in a chosen packet's inventory, explicitly obtain
another offered packet:

```python
resolved = await reader.resolve(chosen_demand, max_bytes=65536)
offers = await client.packet_offers(
    resolved["candidate"], max_offers=4, max_bytes=4096)
# The caller inspects the actual offers and explicitly chooses one.
await reader.stage(resolved["candidate"], chosen_entry_from_these_offers)
```

There is intentionally no default “first packet” choice. Missing offers mean
the caller must stop or use a separately authorized strategy; the helper
does not fabricate evidence or change proof form. It supports one chosen exact
journal per mathematical module and one packet per packet-root module.
Conflicting journals or a different packet for an already selected packet root
refuse. Group conflicts refuse; no last-write-wins representation policy is
hidden in this helper.

Identical already-selected packets, names or body addresses return
`NO_PROGRESS` without a new corresponding download. They still spend a helper
step and the existing live metadata checks. After adding data, explicitly call
`preview` again. A bounded caller may stop with unresolved demands at any point;
there is no implicit loop or retry. A demand must exactly match a record from
the latest preview. Returned demand dictionaries are detached from helper state.

## Internal members remain structural until their packet is admitted

The staged-member successor derives a bounded inventory from the existing
mixed-packet parser's exact frontiers and expected delta journals. It includes
the internal I/A frontiers and native-delta ancestors already carried by that
packet, without inventing additional evidence. Terminal evidence exposes only
its selected member, never unopened members of the aggregate.

Thus a mixed packet can support preview of a needed internal module even when
the provider offers no separate packet for it. `select_member` is an explicit
caller choice of exact journal, not extraction of a new warrant. Packet
readbacks rederive and compare the inventory before and after actual admission;
the helper also compares it with the admitted packet's live member inventory.
Only those actual live warrants reach final import.

Selecting a subset of interfaces does **not** mean partial packet admission.
The unchanged mixed receiver verifies every bounded witness in each selected
packet and checks all its required frontiers. Inventory extraction scans that
bounded packet, never a global result corpus. A demanded transparent body is
separate semantic data; this helper creates no shortcut around theorem checking.

A demanded module absent from available inventories still needs another
supported offered packet or an explicit stop. No naked I receipt is accepted
as terminal evidence and A is never replaced by I. Different journals naming
the same module cannot be silently conflated.

## Actual checking and use

When the latest preview returns `STRUCTURAL_CLOSURE_STAGED`, supply an exact
map from every selected **packet-root** module ID to its admission limits:

```python
ready = reader.finish({
    module_id: {
        "native_cpu_seconds": 10, "receipt_cpu_seconds": 10,
        "wall_seconds": 60, "memory_mib": 512,
    },
    # One entry per selected packet root, not per internal member.
})
if ready["status"] == "READY":
    context = ready["context"]  # Same still-live client only.
    # The caller may now use the existing client.author API.
```

These are example suballocations, not additional resources. All admissions
share the original client/acquisition budgets and deadline. The helper passes
each packet root's exact journal to `admit_staged` and admits in sorted
packet-root order, once per packet. It then supplies those actual warrants,
all explicitly chosen member journals and selected data to unchanged
`import_context`.

Optional `resolutions` maps a packet-root module to an explicit
`{exact_journal_bytes: "existing" | "incoming"}` representation-choice map for
that source. The unchanged live importer rejects missing, unknown or unused
choices and enforces its existing conflict semantics. Omitting a map does not
choose a winning conflicting representation implicitly.

`finish` is consumed before the first admission. A later failure cannot return
success because an earlier module was accepted; no automatic retry follows.
If live import still reports missing data, the result is `NEED_SEMANTICS` with
`context=None`. A genuinely ready import returns its actual opaque context;
the accompanying report remains nontransferable operational data.

Helper errors or expired original authority mark the helper FAILED. Exceptions
from actual client operations preserve that client's existing failure and
charging behavior. A helper-only input error does not claim to revoke unrelated
client authority; the caller remains responsible for cleanup.

## Cost and limits

Requests depend on explicitly selected modules, names and bodies, not the global
corpus size. Bodies are deduplicated by module, universe arity and hash; groups
by module and index; exact names by module and formal name. Full previews
revisit the accumulated closure, so total preview work can scale as
`rounds × selected-closure-work`. No linear-time claim is made.

`data_bytes` bounds canonical candidate/selection/member-inventory/group/body metadata plus
current demands retained by the helper, not Python object overhead or packet
custody on disk. Original client request/input/store/worker limits and enclosing
CPU/memory/wall supervision remain mandatory. Failed attempts retain their cost.
No helper counter is a full physical-cost measurement.

The implementation is a local strategy seam, not evidence of useful growth,
global discovery completeness, permanent availability or genuine aggregate
certification. Those original v5 obligations remain separate.
