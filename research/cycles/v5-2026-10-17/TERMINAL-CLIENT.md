# Ordinary client for mixed extensions and certified terminal targets

Design checkpoint, 2026-10-17. Sole project root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
Selected by `TERMINAL-SELECTION.md`; product implementation and execution are
not authorized by this checkpoint alone. No product import, source edit, test,
native process, proof, network operation or Git mutation occurred in this task.

## Decision and invariant

Use one explicitly closed two-form evidence profile/store/acquisition:

1. The unchanged existing mixed packet, checked by the unchanged mixed parser
   and actual `MixedDeltaVerifier`.
2. A separately tagged terminal envelope containing one exact A receipt, H,
   selected J, member index and ordered membership path. Check the actual
   receipt with `AggregateReceiptVerifier`, then select that exact member.

No wrapper theorem, empty fabricated delta, new checker, automatic prover or
downloaded verifier configuration is introduced. The original mixed packet's
requirement for a final native delta stays unchanged. A terminal target is the
same selected J, with the same ModuleID and formal export identities; it is
not a newly generated theorem about the target.

The ordinary client extends `client.workspace_mixed`, retaining neutral methods
and exact mathematical owners. A new concrete workspace schema selects the new
union store. It does not migrate or rewrite old mixed or I-only workspaces.
The duplicated concrete open/constructor/type-bound logic is approximately
200 source lines, not a duplicate of the whole workspace/client implementation.
This estimate is a source-mapping estimate, not an implementation size result.

Root considered separate terminal custody beside the existing mixed store.
That would reuse more constructor code, but would require choosing an evidence
mode before learning what an unknown-ID result offers, or adding multiplexing.
The selected two-form profile permits both alternatives in one original query,
one endpoint profile and one acquisition budget. No third extensible plugin
case or generic registry is needed.

## Concrete collaboration boundary

The evidence-network author supplies these interfaces. Final spelling may be
coordinated without changing the contracts; no implicit protocol alternative is
authorized by this note.

| Interface | Required contract |
|---|---|
| Original mixed `Envelope` plus `terminal_receipt_bytes` | No new envelope class. Common packet bytes are bounded by the unchanged mixed packet-byte ceiling; terminal decoded receipt has its own explicit cap. |
| `inspect_evidence(raw, envelope, *, aggregate_image, terminal_receipt_bytes)` | Return `(kind, summary, exact_J, census)` after canonical bounded tagged dispatch. A mixed branch delegates to the unchanged parser and derives its final J with existing `expected_journal`. No authority. |
| `parse_terminal(raw, envelope, *, aggregate_image, terminal_receipt_bytes)` | Return `(receipt, H, J, index, tuple_siblings, structural_member)`, never a live member handle. |
| `pack_terminal(header, journal, index, siblings, receipt, *, aggregate_image, envelope, terminal_receipt_bytes)` | Canonical exact terminal encoding with structural rebinding; no claim that input receipt is genuine. |
| `PacketStore` / `public_profile(A)` | Exact closed two-form class/profile. Existing content-addressed blob and transaction methods; `inspect(M, raw)` returns the target summary and census in the existing custody shape. |
| `EvidenceAcquisition.from_search(...)` | Same original one-shot handoff and same `AcquisitionBudget`; structural-only, with `verifier=None`. No mathematical admission. |
| `EvidenceAcquisition.export/packet/offers/body/custody_ready` | Existing search-origin, exact offer/byte/hash, semantic custody, budget and deadline checks with the new exact profile. Offer entries retain digest/size shape; raw typed evidence decides form. |
| `EvidenceAcquisition.declaration(provider, M, name, max_bytes)` | Wrap existing `structural.declaration`, then store/read back the exact group as `export` already does. Same authorized endpoint and budget; no index hint or new route. |
| `EvidenceAcquisition.admit(...)` | Explicit refusal, preventing accidental inherited native-delta admission. The ordinary client alone dispatches actual authority. |

`Workspace._envelope` remains the original mixed envelope because actual delta
and authoring owners compare it exactly. A fixed `terminal_receipt_bytes`
configuration field controls the additional receipt cap. Do not replace `_envelope`
with a union object and thereby weaken existing owner-envelope checks.

## Ordinary public APIs

The existing `find`, `search_offer`, `search_page`, `resolve`, `packet_offers`,
`acquire`, `describe`, `import_context`, `extend_context`, `author`, `publish`,
`reconcile`, status/report and close workflow remains recognizable. One result
can offer either evidence form without a new search or handoff.

The selected new or extended signatures are:

```text
acquire(candidate, entry, *, bodies=(), expected_exact_journal=None,
        native_cpu_seconds=30, receipt_cpu_seconds=30,
        wall_seconds=600, memory_mib=1024) -> LiveWarrant

admit_local(module, packet_sha256, packet_bytes, *,
            expected_exact_journal=None, existing resource arguments)
            -> LiveWarrant

resolve_declaration(origin_candidate, module, relative_name, *, max_bytes)
    -> Candidate

acquire_body(candidate, digest, *, max_bytes) -> exact structural body response

export_evidence(warrant) -> exact mixed bytes or canonical terminal bytes

retain_semantics(openings, bodies) -> structural custody/readback report
```

`expected_exact_journal`, when supplied, must be immutable bytes of length 184
and pass the existing journal decoder. Require equality with the parsed target
before admission and with the actual live fact after admission. It is not
inferred from ModuleID: different exact journals/ranks can name the same module.
Unknown-ID discovery may omit this constraint; the growth comparison must set
it to the original fixed target J.

`resolve_declaration` takes an existing same-client candidate only to choose its
already authorized provider. The caller supplies an exact module/name demand.
It uses the existing `/v5/modules/group` route without another search and returns
a fresh same-client inert Candidate. Describe its provenance as an exact-name
request, not an originating index result or completeness claim. It may resolve
another module, but that module still needs its own actual warrant before
mathematical use. No new contact, endpoint referral or fake search record.

`acquire_body` uses that candidate's actual bound descriptor and the existing
hash/permission-checked body route. This also handles siblings in an indivisible
declaration group: resolve the exact sibling name, then request its committed
body. Returning a terminal certificate does not imply all these bodies exist.

## Admission sequence and accounting

Inside one serialized async action, `acquire` performs:

1. Validate the same-client candidate and selected offer. Fetch any explicit
   selected-declaration body requests through the existing acquisition API.
2. Fetch/read back the exact offered evidence into the new PacketStore, or use
   exact already-held bytes under the retained offer/custody checks.
3. Parse its concrete form and target. Bind target summary to the resolved
   opening, and bind optional expected J before expensive verification.
4. For mixed bytes, invoke the inherited mixed `_admit_packet` core. For a
   terminal, invoke the existing direct A admission method's `__wrapped__`
   core with exact receipt/H/J/index/path. The outer action owns serialization,
   fail-stop cleanup and final activity/output checks; do not nest a decorated
   public action or create another acquisition admission reservation.
5. Through the actual selected issuer, open the resolved group and require its
   summary to equal the actual target's summary. Revalidate the live warrant,
   exact optional J, custody readback and owner lifetimes before returning.

The terminal result is the existing kind `A-member`, with its actual
`VerifiedAggregateMember`. The mixed result remains kind `mixed`. Existing
`_warrant`, fact normalization and atomic import dispatch therefore remain valid.
No acquisition return dictionary, stored receipt, index record or parser result
can issue `LiveWarrant` by itself.

One `AcquisitionBudget` pays location/search preallocation, all network attempts,
group/body transfers and actual admission reservations. Mixed receipt/native
reservation remains `claims * receipt_cpu + deltas * native_cpu`; terminal uses
one A receipt reservation and zero native target-delta reservations. Exact same
live receipt cache hits use existing A amortization, with membership rebinding
on every submission. No automatic fallback, retry or refunded failure.

The existing direct A core charges receipt bytes to verification-input allowance
and H/J/path/index to client submitted-input accounting. The envelope itself is
also bounded/charged as client input and as network reply when downloaded. This
is nested submitted-work accounting, not an additive claim about unique physical
bytes. Do not charge a second receipt verification from acquisition. Validate
all public resource arguments and preserve the original grant/deadline caps.

The existing `_packet_cache` becomes a typed same-live acquisition locator:
both forms can avoid a repeated exact packet download. A terminal hit still
passes the existing direct A core, charging/rebinding membership and checking
its receipt cache. No new cache or authority token is introduced.
`export_evidence` needs no stored envelope mapping:
for an A-member, `_warrant` supplies live H/J/index/path and exact receipt bytes;
canonical packing reconstructs the terminal. For mixed, export the existing
bound raw packet. A bare I warrant is not silently converted into A evidence.

## Semantic retention, publication and recovery

`retain_semantics` is a bounded structural operation, not verification:

- `openings` contains `{module, opening}` rows; validate each exact group opening
  and persist/read back with existing ModuleStore methods.
- `bodies` contains existing complete body-response records, including module,
  relative name, universes, committed body hash and expression. Require a stored
  owning descriptor and existing `put_body/get_body` permission/hash checks.
- Charge encoded inputs, calls and normal store quotas; use before-commit
  activity checks. Each group/body write is atomic only within its existing
  database transaction; the batch is not cross-database atomic. Return no
  mathematical acceptance or promise of all future semantic data.

An agent with a live A member can call `export_evidence`, retain selected semantic
data, then use ordinary `publish(evidence, export_names, retention_policy=...)`.
Another custodian can retain/forward structurally valid unverified evidence;
publication never upgrades its trust status. This matches existing mixed
publication policy.

Override `_publish` with two explicit branches:

- Mixed delegates to the original mixed publication code unchanged.
- Terminal binds J/summary/ModuleID, checks unique selected export names and
  reads their exact groups from already durable ModuleStore custody. Persist
  the existing bounded publication intent, put/read back terminal evidence,
  read back selected groups and available committed bodies, then index the
  same `export_id(ModuleID, name)` using the existing adapter. Count missing
  bodies honestly. Never require or fabricate a target delta witness.

Retaining semantics first avoids a new manifest database, large semantic arrays
inside audit reports, or ephemeral publication-only semantic state. The existing
publication intent's packet hash/length, exports and retention policy suffice
to rederive the terminal publication plan from immutable custody. Inherited
`reconcile` reloads the exact packet and dispatches `_publish` again under a new
explicit grant. Missing packet or damaged/missing semantics still refuses; no
rollback, data recovery or complete-availability promise follows. Prior partial
publication remains recorded, as with the existing path.

Terminal semantic acquisition is demand-driven. The inherited A-member
`semantic_material` correctly says caller/provider semantics are needed; the
candidate, exact-name resolver and body APIs supply them. Feed those records and
the actual A-member into existing `import_context`. Its actual `open_group`,
selection/conflict and materialization rules remain the mathematical boundary.

## Minimal source map

A fresh `client/workspace_evidence.py` subclasses the frozen mixed implementation.
Do not edit used files or monkeypatch module globals/classes.

| Area | Change versus inherited source |
|---|---|
| Workspace open/operation | Concrete successor schema, exact new PacketStore/profile/evidence limits, instantiate new client; existing ledger/module/index creation logic copied narrowly. |
| Client constructor | Retain all pristine-owner, exact pairing/profile, original deadline, suballocation, foundation and cleanup initialization checks; change only concrete custody/profile bindings and include new source-origin pins. |
| `_active` | Preserve original owner identities and checks; additionally bind exact new store/profile/parser/acquisition source origins and unchanged handoff alias. |
| `resolve` | Instantiate structural-only EvidenceAcquisition using the same handoff and budget, then use actual export resolution. |
| `_admit_packet`, `admit_local`, `acquire` | Closed form dispatch, exact target constraint, one admission core and one outer action; actual issuer group opening/readback. |
| Exact-name/body methods | Thin bounded wrappers over real acquisition declaration/body methods; no search or proof bypass. |
| `export_evidence`, `retain_semantics`, `_publish` | Exact live extraction; structural semantic retention; terminal publication/reconciliation branch. |
| Neutral inherited methods | Grant reservation, routing/search, candidate/receipt/member descriptions, direct I/A admission, atomic imports, authoring, mixed semantic extraction/publication, original-owner cleanup, audit records and grant consumption remain inherited where exact gates permit. |

Do not silently inherit old `acquire`: it calls acquisition-side mixed admission
and opens groups with the delta issuer. The new branch must make that authority
choice explicit. Similarly, the old `resolve` hardcodes mixed acquisition.

Dynamic constructor dispatch deserves review: overridden `_active` may be called
during initialization. Set needed immutable fields before such calls, or use a
private construction-only phase followed by complete checks before ownership
transfer. No initialized client may skip new origin checks. Include frozen
parent modules and every new parser/store/transport/client module in selected
source bindings. Existing `_fail`/close must still close original issuers and
preserve cleanup uncertainty; avoid new live state requiring additional owners.

## Distinguishing qualification plan

Reuse prior 16 A-client controls; do not rerun their unchanged boundary. New
finite controls should test these new decisions only:

1. Both forms under one exact union profile/query/budget; terminal is original
   J/ModuleID, contains no target witness, and invokes A rather than native
   target verification. Mixed continues to invoke the existing mixed core.
2. Reject wrong A, membership path, target ModuleID/summary, exact requested J,
   receipt bytes, unsupported schema and profile before authority promotion.
   A same-ModuleID/different-J fixture is essential for the exact-target check.
3. Charge one admission reservation, no nested decorated-action entry; mixed
   and terminal cannot exceed the same original acquisition allowance. Actual
   A same-receipt cache reuse remains under the original owner/profile/lifetime.
4. Real descriptor-bound exact-name and body retrieval through existing routes,
   including a group sibling; no fake index candidate, second query, fresh
   budget or unconfigured provider. Bad/missing body remains non-acceptance.
5. Retain terminal semantics, publish the same exports, reopen and reconcile
   a selected interrupted publication without ephemeral semantic inputs.
   Missing/corrupt selected material refuses; no new mathematical authority.
6. Exact live A export reconstructs canonical terminal bytes; mixed export
   retains exact raw bytes; direct I and foreign/revoked tokens cannot forge A.

Synthetic owner controls qualify only integration contracts. The eventual
genuine campaign should cover this final route once: original fixed target J
becomes terminal-certified, a fresh reader discovers/acquires it without target
witness, imports needed semantics, authors a substantive extension and publishes
that unchanged mixed extension for another reader after selected provider loss.
The source-free terminal route's actual receipt size/verification/semantic and
service costs then enter the full-cost comparator. Zero target-delta work is
not itself evidence of positive total growth benefit; producer/certification,
failed searches, storage/maintenance and downstream costs remain accounted.

This checkpoint removes a concrete design ambiguity; it does not declare the
full v5 software implemented, tested, deployed or complete.
