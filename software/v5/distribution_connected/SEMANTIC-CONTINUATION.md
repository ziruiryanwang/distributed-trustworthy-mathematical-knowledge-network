# Use discovered mathematics inside one live owner operation

The installed `run` command is the interface for an agent that needs to acquire
missing definitions, try another authorized supplier, then use the resulting
context. The built-in `reader` remains a one-shot policy: it can return
`NEED_SEMANTICS` and closes its client. Its saved JSON is not a resumable handle.

This helper requires the connected distribution's exact logical source map:
the resilient `client.workspace_evidence`, member-aware
`client.workspace_staged`, `client.semantic_reader` and
`transport.acquisition_resilience`. They are ordinary installed modules, not
runtime patches. Direct-contact use does not require Node. Located discovery
and advertised serving require the explicitly selected location runtime role.

## Open once, choose locally, close once

Launch explicitly trusted owner code through the existing finite `run` command:

```text
base/receiver/runtime/python/python.exe -I -S -B distribution.py launch RELEASE_SHA run REQUEST REQUEST_SHA
```

Use absolute local paths when invoking it. `REQUEST` retains the installed
request schema and exact owner source hashes. For a validated workspace select
`runtime_mode: "aggregate"`; this selects the existing verifier configuration,
not a claim that a certificate already exists. Owner parameters can request
the installation's exact roles with singleton objects
`{"$installed":"runtime_adoption"}` and `{"$installed":"foundation"}`.

The owner uses `RuntimeProfile.from_context(context, adoption)`, opens the
selected validated `Workspace`, reserves one finite operation grant, and calls
`profile.open_operation(..., mode="validated", ...)`. Set `authoring=True`
only when subsequent authoring is intended and budgeted. Keep that client and
its workspace open throughout discovery, staging, admission and use. The
ordinary runtime API supplies exact owners; do not construct warrants from
reports or replace owners with callbacks.

Bind every permitted direct contact, including a potential alternative Q,
before the one-shot search handoff; alternatively use the existing bounded
located workflow. Search/offer/page/resolve/packet-offer produce the live
`candidate` and caller-selected `entry` used below. Stop on a refusal or miss
unless your own finite policy explicitly chooses another permitted operation.
Do not call `remote_reader.read` first: that policy already admits the packet
and is not the staging entry for this helper.

## Minimal bounded continuation example

This example is an owner function, not a new executable, task language or
automatic global policy. It handles one selected packet and its unambiguous
internal members. If another packet or an ambiguous member is needed, it stops
and reports that boundary; a richer local owner may make those choices through
the same APIs. `suppliers` is an already-authorized, finite ordered tuple chosen
by that owner. No endpoint is taken from a mathematical demand.

```python
from client.semantic_reader import SemanticReader

async def continue_one_packet(client, candidate, entry, suppliers, admission):
    if not 1 <= len(suppliers) <= 2 or len(set(suppliers)) != len(suppliers):
        raise ValueError("Choose one or two distinct authorized suppliers")
    helper = SemanticReader(client, candidate, limits={
        "modules": 8, "names": 64, "groups": 64, "bodies": 64,
        "steps": 512, "data_bytes": 1024 * 1024,
    })
    try:
        staged = await helper.stage(candidate, entry)
        packet_module = staged["module"]
        inventory = staged["members"]
        for _ in range(64):
            preview = helper.preview()
            if preview["status"] == "STRUCTURAL_CLOSURE_STAGED":
                return helper.finish({packet_module: admission})
            demand = preview["demands"][0]
            if demand["kind"] == "NeedModuleEvidence":
                choices = [m for m in inventory if m["module"] == demand["module"]]
                if len(choices) != 1:
                    return {"status": "OWNER_MUST_SELECT_MORE_EVIDENCE"}
                helper.select_member(packet_module, bytes(choices[0]["journal"]))
            elif demand["kind"] == "NeedDeclaration":
                await helper.resolve(demand, max_bytes=65536,
                                     supplier=suppliers[0])
            elif demand["kind"] == "NeedBody":
                # Acquire the exact committed declaration first if not held.
                await helper.resolve(demand, max_bytes=65536,
                                     supplier=suppliers[0])
                for supplier in suppliers:
                    attempt = await helper.try_fetch_body(
                        demand, max_bytes=65536, supplier=supplier,
                        attempt_timeout_ms=2000,
                    )
                    if attempt["status"] in ("FETCHED", "NO_PROGRESS"):
                        break
                    if attempt["status"] != "UNAVAILABLE_AT_SELECTED_SUPPLIER":
                        raise ValueError("Unexpected body-attempt outcome")
                else:
                    return {"status": "SELECTED_SUPPLIERS_UNAVAILABLE"}
            else:
                raise ValueError("Unexpected structural demand")
        return {"status": "OWNER_STEP_LIMIT"}
    finally:
        helper.close()  # Does not close the borrowed client.
```

The illustrative caps are not automatically granted. The surrounding grant
must cover all calls, requests, bytes, selected members and import data; the
helper refuses incompatible caps. A `NO_PROGRESS` result never renews a budget.
The 64-iteration limit prevents an owner mistake from becoming an endless loop.
Declarations/packets retain their existing failure behavior: the special
continuation behavior here is narrowly for settled body unavailability.

`admission` has exactly `native_cpu_seconds`, `receipt_cpu_seconds`,
`wall_seconds` and `memory_mib`; all must fit the unchanged operation/outer
budgets. `finish` admits each selected packet once and imports the explicitly
chosen member journals through the existing verifiers. `preview` only inspects
structure and never grants mathematical authority.

When the return status is `READY`, use its opaque `context` with the same live
client, for example `client.author(context, source, export_names, ...)`, then
publish through the existing client API if your owner policy selects that.
`NEED_SEMANTICS` is not READY and `finish` cannot be repeated on a consumed
helper. Neither a context handle nor a warrant can be serialized as authority
and resumed in another process. Close the client with `await client.close()`
and then close the workspace in the owner's `finally`, attempting both even
when the earlier close fails. Keep cleanup errors visible.

## What supplier continuation does and does not mean

`UNAVAILABLE_AT_SELECTED_SUPPLIER` settles that bounded attempt and charges its
full reserved reply capacity. The original client, grant, selected evidence and
current demand remain; the next explicitly chosen supplier uses the same
remaining budgets and deadline. The result does not claim global absence.

Malformed successful replies, wrong commitments, unauthorized/expired contacts,
cancellation, uncertain cleanup and custody failures are not ordinary absence.
They retain fail-stop behavior; do not catch them and continue as if Q were a
safe retry. Body success proves exact correspondence to an already selected
commitment, not that the declaration is mathematically valid before admission.

This interface exposes existing finite capabilities. It does not establish net
useful growth, universal discovery, global availability or final release safety.
