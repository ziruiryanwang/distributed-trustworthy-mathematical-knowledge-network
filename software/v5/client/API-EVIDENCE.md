# Two-form mathematical evidence client

This source candidate adds standalone certified targets to the existing ordinary
mixed-extension workflow. It is not a new checker, a proof-production service or
a completed v5 release. It requires the existing trusted-owner Windows execution
environment and an actual enclosing resource Job. A Job is not a security sandbox.

Import `Workspace` from `client.workspace_evidence`. Keep using the existing
I/A/mixed verifier and atomic preparation classes. A is required, I optional;
the mixed verifier must hold precisely `(selected_I_or_None, selected_A)`.

## Fresh workspace and ownership

Use a fresh path with schema `DMKN_V5_CLIENT_EVIDENCE_WORKSPACE_V1` and
`evidence_network.custody.public_profile(adopted_A_image)`. The configuration
has the same finite fields as `API-MIXED.md` plus:

```text
terminal_receipt_bytes: integer, 1 through 8 MiB
```

`packet_envelope` remains the unchanged mixed `Envelope` dictionary. Its packet
byte ceiling also bounds terminal JSON. Hex-encoded receipt overhead must fit
that ceiling. The new evidence store has a separate schema; do not open an old
mixed/I-only database with the new client or rewrite its config.

Call `reserve` before constructing actual issuers inside the enclosing Job.
The owner pairing, pristine counters, earlier-or-equal deadlines, controller
start times, nested CPU/input/output/member caps and preparation suballocation
requirements in `API-MIXED.md` are unchanged. Only successful `operation(...)`
transfers issuer ownership. The caller closes failed-construction owners.

Runtime source pins must include all predecessor required origins plus:

```text
client/workspace_evidence.py
evidence_network/__init__.py
evidence_network/packet.py
evidence_network/custody.py
evidence_network/transport.py
```

Actual issuers retain their own additional checker/runtime/source pins. These
five files do not replace those adoption requirements. The client checks exact
loaded source origins, source-pin records, owners, stores and profile throughout
the operation. No remote object chooses the checker or adopted A image.

## One discovery path, two evidence forms

`find`, `search_offer`, `search_page`, `resolve`, `describe_candidate` and
`packet_offers` retain their familiar signatures. There is one original
one-shot location/search handoff and one acquisition budget. The same discovered
ModuleID can offer both:

- An unchanged mixed packet whose target is its last native delta.
- `DMKN_CERTIFIED_TERMINAL_MEMBER_V1`: exact A receipt, header H, selected
  journal J, member index and ordered membership path, with no target delta.

The new evidence profile accepts exactly these two forms. Offers contain only
bounded digest/length locators; inspect the actual canonical bytes to determine
the form. The structural acquisition object has no verifier and cannot admit
mathematics. The public client dispatches to the actual existing issuers.

```python
warrant = await client.acquire(
    candidate, selected_offer,
    expected_exact_journal=known_journal_or_none,
    receipt_cpu_seconds=30, native_cpu_seconds=30,
    wall_seconds=60, memory_mib=1024,
)
```

`admit_local(module, packet_sha256, packet_bytes, *, expected_exact_journal=None,
native_cpu_seconds=30, receipt_cpu_seconds=30, wall_seconds=600,
memory_mib=1024)` admits already-custodied evidence through the same dispatcher.

If `expected_exact_journal` is present, it is immutable 184-byte J and must
match both the structurally selected target before verification and the actual
live fact afterward. This also applies on cache hits. Equal ModuleID is not
enough: distinct rank-bearing J can name the same mathematical interface.
Unknown-ID discovery can omit it and inspect the actually returned J.

Terminal admission uses actual A receipt verification and exact member selection;
its returned `describe(warrant)["kind"]` is `A-member`. Mixed admission remains
`mixed`. Remote `acquire` then binds the selected declaration group through the
actual issuer and reads back custody before returning. Local `admit_local`
has no selected-opening parameter; later semantic import binds its openings.
A copied report or parser result
is never a warrant.

Direct A, optional I, mixed and terminal admission all spend the same original
acquisition verification allowance. Terminal reserves one receipt check and no
native target-delta check. Mixed keeps the existing claim/delta reservation.
Same-live receipt hits can amortize receipt verification but still charge/check
exact membership. Exact cached evidence can avoid a second packet download;
changed receipt/header/J/path, issuer lifetime or profile cannot borrow that hit.
No failure refunds, retries or fresh budget are implicit.

Network reply bytes, submitted client bytes and issuer verification-input bytes
are distinct nested accounting scopes, not additive actual CPU/physical bytes.
Terminal client input includes the envelope plus the inherited direct-member
receipt/H/J/path/index submissions. The verifier allowance charges the receipt
actually submitted to A, once per new same-live binding.

## Fetch the semantics actually needed

A terminal receipt warrants an interface; it does not supply every definition
body or make missing data appear. `describe_candidate(candidate)` returns the
actual resolved opening and descriptor. Existing `acquire(..., bodies=...)`
requests bodies of that selected descriptor.

For further exact-name demands on the same already authorized provider:

```python
dependency = await client.resolve_declaration(
    candidate, required_module_id, required_relative_name, max_bytes=65536
)
body = await client.acquire_body(dependency, required_digest, max_bytes=65536)
```

These methods reuse existing group/body routes and the original budget. They
do not perform a new global search, add a contact or fabricate an index record.
The returned candidate is marked `EXACT_NAME_NOT_INDEX_SEARCH`; it is structural
data, not a mathematical handle. This also retrieves bodies of siblings/other
groups when actual semantic imports demand them. Another module still needs an
appropriate actual warrant before import; discovering its name is insufficient.

`acquire_body` returns the existing response dictionary with `body`, assurance
and `mathematical_acceptance=False`. Its full body record contains `schema`,
`module_id`, `relative_name`, `universes`, `body_hash`, `expression`.

Use the existing `import_context` / `extend_context` with actual warrants,
explicit selected exact journals and acquired group/body records. Atomic import
selection, conflicts, live source authority and materialization remain unchanged.
`author` produces an ordinary mixed extension using the existing preparation
owner. No terminal wrapper theorem is necessary.

## Export, retain and publish

`export_evidence(warrant)` returns transferable bytes, not transferable local
authority. For a mixed warrant they are its exact bound packet. For A-member,
the client reconstructs canonical terminal bytes from the live exact H/J/index/
path and its bound receipt. Direct I and foreign/revoked warrants cannot be
turned into A by this API. If a locally admitted large A receipt cannot fit the
selected terminal envelope, export refuses rather than widening its bounds.

Before publishing a terminal target, retain its selected semantic data:

```python
client.retain_semantics(
    [{"module": module_id, "opening": exact_group_opening}],
    [complete_body_response],  # May be empty when no body is currently held.
)
packet = client.export_evidence(warrant)
publication = client.publish(
    packet, selected_export_names,
    retention_policy={"mode": "quota-bounded-local-custody"},
)
```

`retain_semantics(openings, bodies)` validates/commits/readbacks existing
ModuleStore groups and body responses under the grant and store quotas. It is
structural custody, not proof verification or publication. Its list/byte/call
limits are finite; each database write is transactional, but a failed batch may
leave earlier valid items retained. It is not a cross-database atomic batch.

Terminal `publish` accepts no detached semantic arrays. Every explicitly exported
name must already have a durably retained exact group under the terminal target
ModuleID/summary before publication intent is created. It then writes/readbacks
evidence, reads selected semantic data and indexes the unchanged formal export
identities. Missing bodies are counted; corrupt present bodies refuse. Neither
successful indexing nor custody is mathematical acceptance, remote replication,
permanent retention or a promise of all future bodies.

The unchanged mixed publication path still derives its semantic data from its
actual packet. Both forms use the existing bounded intent/outcome ledger. A
partial publication yields `PartialPublicationError`; preserve its identifier.
After orderly closure, a new operation can call `reconcile(publication_id)`.
For a terminal it reloads the exact envelope and selected immutable groups from
custody, not missing caller memory. Missing/corrupt required data refuses. No
rollback, authority restoration or fresh allowance is hidden inside recovery.

## Lifetime and scope

Warrants/candidates/contexts belong to one client and live issuer lifetime.
Closing or failing the client clears them. All originally transferred issuers
are closed even if a public owner reference was replaced; replacement objects
are not adopted. Cleanup uncertainty remains sticky and prevents another grant
in that live workspace. Reopening durable storage restores untrusted data and
historical records only; new mathematical use needs actual admission again.

The implementation preserves the original controller/resource trust model.
Proof soundness, checker correspondence, semantic availability, provider service
capacity and positive full-cost growth remain separate obligations. Synthetic
integration controls cannot establish genuine A verification or worldwide
deployment readiness.
