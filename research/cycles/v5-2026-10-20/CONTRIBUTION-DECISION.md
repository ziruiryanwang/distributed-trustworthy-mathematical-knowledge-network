# Contribution after installation: do not add another orchestration layer

2026-10-20, core_growth. Canonical guard passed. Read-only source/evidence
inspection; no product edits, runtime, test, proof or Git action.

## Decision

**The public installed `run` command plus current client APIs already support
ordinary caller-selected contribution. A new mandatory contributor command or
protocol is not the highest-payoff gap.** `remote_reader.run` deliberately closes
a reader-only operation; contribution owners must instead call its public
`read(client, query)` inside their own still-live authoring operation.
That function returns actual candidate/warrant/context handles, not merely a
saved report. No fixture factory or global task/intention authority is needed.

The remaining install-specific uncertainty is narrower: the relocated reader
does not execute the newly shipped AuthorLean frontend or six Lean runtime
files. Consequently its PASS cannot by itself establish relocated authoring.
If root selects another actual operation after relocation, use **one small
caller-owned contribution example to exercise that boundary**, not another
full reciprocal/growth campaign. No new receipt proof need be produced.

## Exact existing sequence

An explicitly trusted owner selected by installed `run` can already:

1. Obtain release-derived `runtime_adoption` and `foundation` through exact
   singleton installed-role markers; open its persistent validated Workspace.
2. Reserve one finite grant, then use
   `RuntimeProfile.from_context(...).open_operation(..., mode="validated",
   authoring=True, foundation_bytes=..., foundation_sha256=...)`.
   Total worker CPU must strictly exceed acquisition worker CPU; only the
   difference funds source preparation. All work keeps the original deadline.
3. `answer = await remote_reader.read(client, query)`. Continue only on
   `answer["report"]["status"] == "READY"` and use `answer["context"]` before
   closing the client. MISS/refusal/semantic demands do not authorize authoring.
4. Inspect actual descriptors/material via `describe_candidate`, `describe`,
   `semantic_material` as needed. Source names are determined by
   `modules.codec.relocated_name(module, relative_name)`, not fixture aliases.
   The local agent chooses Lean source, formal roots and exported names.
5. `prepared = client.author(answer["context"], source, roots, **author_limits)`.
   Require `UNTRUSTED_MIXED_DELTA_PACKET_PREPARED`; the result deliberately grants
   no admission authority, even though the frontend exported successfully.
6. For check-before-index policy, structurally store
   `prepared["child"]["packet"]` with public
   `workspace.packets.put(prepared["child"]["local_module"], packet,
   before_commit=grant.remaining_seconds)`, then call
   `client.admit_local(module, sha256, bytes, **admission_limits)`.
   The store call is quota/outer-Job bounded lower-level custody, not a client
   action charge or mathematical warrant. The actual admission charges its
   submitted bytes and verification allowance. No private client method is needed.
7. Only after that live check succeeds, optionally use
   `client.export_evidence(warrant)` and then
   `client.publish(packet, export_names,
   retention_policy={"mode":"quota-bounded-local-custody"})`.
8. Close client then Workspace; serve that retained workspace with the existing
   finite `serve` entry after its exclusive lock is released. A recipient still
   independently verifies. Publication promises local custody/indexing, not
   remote replication, global visibility or permanent retention.

Publishing structural bytes before local admission is also explicitly allowed
by the existing model, but must never be presented as accepted mathematics.
The suggested ordering is a caller policy, not a new network trust rule.

## Smallest justified source scope and evidence reuse

Prefer one **ordinary example owner** (or an exact API example first), not a
new client subclass, workflow DSL, verifier, planner or mandatory task list.
It takes caller query/configuration, pinned caller Lean source, roots/export
names and finite author/admission limits; existing owner-run supplies runtime.
No mathematical name, packet ID, old report or research path is hardcoded.
The only coordination is owner-selected source after actual read/import.
Independent source judgment from core_search agrees: the real usability gap is
having to reconstruct nested configuration/budget schemas and author-result
packet extraction from implementation files. A complete documented owner example
addresses that gap without creating a second lifecycle implementation.

Retained `actual_resume_owner.py` already demonstrates genuine packet-only
import, substantive polymorphic successor authoring/publication and fresh
readmission. Its workload-specific asset/history factory must not be copied
into ordinary code. Remote01 separately exercises current validated
discovery/acquisition/import. Existing unchanged source APIs justify composing
these capabilities; composition is not yet an executed installed-author claim.

If one installed author check is selected, reuse the retained mathematical
dependency and source construction; change only the ordinary/relocated owner
composition. Verify an actual dependency edge and fresh output admission.
Do not regenerate the seed/certificate, repeat every old control, invent another
growth inequality or run a larger peer-count demonstration. Claims about net
useful growth, economical recursive certification and final public deployment
remain separate and open; an additional wrapper cannot settle them.
