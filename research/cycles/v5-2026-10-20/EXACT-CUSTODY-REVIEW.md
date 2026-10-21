# Independent exact-demand custody review

2026-10-20, core_growth. Source/theory review only; no code imports, tests,
builds, proof operations, network calls or Git mutations. Root owns adoption.

Selected SDK map: `distribution-projection-01-input.json`, 113 entries,
SHA-256 `ad2c15a27a51f749104ac09f9cafee210a108fb0bf46bafad8b2a9542f86d38f`.
Decision reviewed: `SHARDED-DISCOVERY-DECISION.md`,
SHA-256 `a32e0d5f0d472e8159e104e5f625b474f86d5433483bdb1c44ddbe3831ab4366`.

## Decision challenge

The proposed counterexample is real. A body can be retained by a new reachable
Q while the live reader is unable to use it. Current `_selected_supplier`
requires Q in both acquisition endpoints and original adopted search contacts.
`SemanticReader._active` pins the actual search/acquisition objects. The current
`next_located_query` cannot be used as a workaround: `_LocatedEnvelope.retire`
retires that acquisition, clears staged handles/candidates and invalidates the
reader. The earlier split-supplier feature only covers already adopted contacts.

**GO for the selected direction.** This is a necessary availability improvement,
not a speculative growth benchmark or evidence of net useful-growth benefit.
The body address is already known, so unknown-theorem search complexity does
not apply. Under successful exact-key routing and one reachable advertised copy,
the acquisition work can depend on the finite demand/attempt set rather than on
all mathematical results. No global completeness or future retention follows.

## Same-child compatibility findings

The existing child can multiplex this operation without a second node or new
provider framework, but the role is fixed at several independent boundaries:

| Selected source | Required deliberate extension |
|---|---|
| `portable_runtime/location/protocol.py` and `protocol.mjs` | Fixed index role, key domain, request fields and reply role. Add one exact body-role/spec/key branch; preserve old index bytes. |
| `portable_runtime/location/maintained_roles.mjs` | `locate`, `descriptor` and `_serve` force `cfg.namespace`; route construction forces index predicates. A startup-pinned semantic namespace must coexist with, not replace, the index namespace. |
| `portable_runtime/location/intent.mjs` | `enableIntent` independently rejects every non-index spec. Dispatch exact spec/key validation here too; keep atomic intent/published insertion and shared quota. |
| `portable_runtime/location/node_entry_services.mjs` and `ipc_wire.mjs` | Fixed publish/withdraw payload and command allow-list. Any new body publication command must remain on the same original pipe and sequence. |
| `portable_runtime/location/controller_services.py` | Exact configuration schema and reader/provider role checks. Explicitly select a backward-compatible configuration successor rather than mutating a started child. |
| `located_queries/client/located_queries.py` | Entire original child configuration and index namespace are pinned. Body reservation must bind the semantic configuration before first startup and must not mutate search dictionaries. |

The retained DHT protocol, CID construction, transport budget, authenticated
peer identity, known-peer cache and private-pipe framing can be shared. Index
and body advertisements must consume the same `advertised_keys`, metadata,
commands, service lifetime and transport counters. A known-peer cache entry is
not authorization: descriptor role/key/nonce/channel-peer checks remain required.

The hard pipe limits remain 16 KiB per frame, 1 MiB per direction and 64 frames;
the command limit reserves room for startup/closure. Per-role counters cannot
silently multiply these bounds. Deadline reduction is permitted; a fresh child,
fresh absolute deadline or replacement budget is not.

## Exact addressing and authority

An index namespace includes an optional discovery profile. A body semantic
namespace must instead bind its module format, foundation and semantic policy,
independently of profile, feature schema and partition layout. Derive it from
the owner's actual selected adapter/codec, never from a remote claim.

Use existing `C.export_id(module, name)` for exact declaration-name binding in
the compact location spec, alongside module, universe arity and body hash.
Raw supported names can exceed the existing 2048-byte descriptor request cap
(64 parts of up to 1024 UTF-8 bytes each). A hash-bound export address avoids
inventing another name codec or silently excluding these names. The original
validated name remains available locally for the existing exact body HTTP path.

A descriptor supplies only a possible endpoint. Its identity or reputation
never authenticates the mathematics. The body path must still bind the staged
declaration and exact module/name/arity/body hash, validate canonical expression
bytes, retain ordinary custody checks, and defer mathematical acceptance to the
existing admission path. The original index candidate and provider provenance
must not be replaced by a fabricated candidate attributed to Q.

## Reservation and lifecycle obligations

`AcquisitionBudget.charge_external` is legal only before its first acquisition
ticket (`sequence == 0`). Reserve the finite body-location allowance before the
first query/acquisition, using the original budget and same fixed deadline.
This can be a separate prepaid slice, not an implicit enlargement of an already
active query. Route events, peer slots, descriptor requests/replies and retained
contacts need finite total caps. Failed attempts do not renew them. HTTP body
attempts continue through existing acquisition reservations/settlement.

The supplier capability must be private, owner-created, finite and bound to
the exact current reader, original client/grant/search/acquisition, staged
candidate, still-pending demand, semantic address, owner policy and expiration.
It grants only one exact body path, not search, declarations or packet evidence.
Starting another query, reader terminal state or successful body fulfillment
must make it unusable. Ordinary settled pre-validation unavailability may
preserve staged state; commitment mismatch or post-custody uncertainty must
not be converted into an ordinary network miss.

## Concrete contract review

One concrete predecessor defect must be covered by the shared transport change:
`transport/acquisition_resilience.py` SHA-256
`43fa1acd66219c7d28a37a263dee04a20edd993bd24383c54680aa303202c09d`
admits exact contact types only `_ExpiringContact` and
`client.direct_contacts._Contact`. The selected adaptive located query creates
the distinct `client.located_queries._Contact`. Thus `try_body` rejects this
otherwise ordinary original contact at `BODY_ATTEMPT_EXACT_CONTACT`;
`declaration_resilience.try_declaration` uses the same `_binding` and inherits
the defect. `configured()` retains the original objects, so it does not erase
that type difference. A precise located-contact branch retaining its actual
generation guard is needed; arbitrary subclass/callback admission is not.
This source finding was sent to root and core_release without running a test.

Reviewed `EXACT-CUSTODY-CONTRACT.md`, SHA-256
`21f4a0950eda43c0e3c381469458f1f3c8cc56b1e287e5fea7405572a7af45c1`.
**GO for root-selected finite implementation; no unresolved contract blocker.**
The updated contract incorporates the role-dispatched intent check, startup V2
semantic domain, compact ExportID, exact located-contact correction, and shared
child/publication counters. Existing query generations and mathematical
acceptance remain unchanged.

The proposed prepayment is compatible with actual `charge_external`: it occurs
after `reserve_located_queries` but before any first query or acquisition ticket,
while `sequence == 0`; both prepaid slices fit the unchanged outer budget.
Prospective combined query/body command caps fit the original child. Body GETs
use the original structural counters and outer reservation, not another
acquisition owner. Only the finite location work is prepaid separately.

The one-use rule is now precise: validated issuance transitions to ATTEMPTING
before outer reservation; only its private current-attempt binding may validate
the guard; every exit makes it SPENT. `body_attempts` increments only for an
issued outer ticket. A local budget refusal consumes the token but neither
settles an unissued ticket nor creates capacity. Normal post-reservation
predial expiry/egress refusal remains charged. Implementation must keep this
distinction instead of testing "token unused" inside its own active exchange.

The V3 provider can advertise selected body refs without an invented index
predicate, yet reuses the actual composite provider and workspace lock. Its
read-back-before-start and combined key/command caps are finite. Publication
remains advisory. The explicit 16 KiB existing body-HTTP request bound is an
honest remaining limit even though the locator wire supports compact hashes
for longer names. Clean locator-only expiry is not treated as proof that an
already verified HTTP hint is dead; its fixed expiry and original ownership
checks still apply.

The decisive changed-boundary controls are: exact located original contacts
work through the shared body/declaration binder while unrelated subclasses
refuse; an absent-original-map Q works only through a demand capability;
same-attempt predial/postreturn checks succeed without reopening the token;
retirement, reuse, expiry, mismatched body/role/namespace and owner changes
refuse; counters settle on both ordinary availability and fatal outcomes.
Keep old index wire vectors, atomic intent behavior and combined child limits.
These controls need no new mathematics/proof generation or broad network run.

This is design review, not implementation or runtime qualification. Root owns
source selection, testing, integration and any release claim. The full v5 goal
and full-cost useful-growth evidence remain open.
