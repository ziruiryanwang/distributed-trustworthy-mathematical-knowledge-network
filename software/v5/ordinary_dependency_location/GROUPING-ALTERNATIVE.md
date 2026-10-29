# Optional bundle and direct-import location hints

2026-10-28. Source-only competing alternative to `OPERATOR-MODEL.md`.
No implementation, import, owner/database open, runtime, network operation or
benchmark was performed for this decision. Existing product/evidence is unchanged.

## Decision and exact improvement

A cheaper **covered dependency graph** alternative is feasible. After ordinary
discovery identifies a target and its provider, that known provider can expose
bounded inert referrals for the target unit's actual missing imports. A referral
names a contribution bundle and a reachable descriptor anchor; the descriptor
names current candidate custodians for that bundle. A reader can thereby learn a
support custodian absent from its configured supplier set. The custodian still
answers the existing exact `(SemanticID, ExportID)` locator/evidence requests.

This needs new metadata, an operator-supplied location association, a bounded
sidecar lookup route and receiver integration. Current bundles and authoring
offers do not supply it unchanged. It is cheaper in continuing publication when
many exports share a group and stable endpoint descriptor, and it avoids a DHT
process/routing service for this narrower workflow. It is not a cheaper solution
to arbitrary uncovered ExportID location. Uncovered imports retain configured
fallback and honest bounded failure. There is no universal absence result.

Select it only if the next required workflow is discovery-led use of contributions
whose publishers can preserve explicit dependency referrals. If independently
held arbitrary exports must be found without such referrals, the selected
operator DHT model has broader coverage; grouping does not discharge that need.
Do not build both to establish this distinction: it follows from their inputs.

## What the current files actually retain

Paths below are relative to the canonical root.

| Source | Available metadata | Consequence |
|---|---|---|
| `software/v5/ordinary_lean/portable_evidence.py:47-70` | Exact S, unit bytes and ordered `(name, ExportID)` imports, including proof-only references; all output declarations are in `unit[2]`. | Derive complete member and direct-import identities from each newly supplied unit; no supplier, endpoint or package provenance. |
| `software/v5/ordinary_binding_reuse/baseline_bundle.py:96-121` | Manifest S, exact manifest hash, batches, UnitIDs, raw hashes/lengths. | A manifest is a finite unit grouping, not an export-to-group or import-to-supplier map. Reading only it is insufficient. |
| `software/v5/ordinary_contribution_bundle/project.py:248-388` | Reads/parses the selected new units, validates selected targets, emits exact units/manifest/append config/receipt. Current caps include 32 units and 4 MiB evidence. | Derive all-output membership and import edges during this already required new-bundle pass; current code does not emit them. Target lists alone omit support-only outputs. |
| `software/v5/ordinary_demand_frontier/ordinary_contribution.py:162-178,632-635` | `acquired_targets` has exactly name, ExportID, UnitID. | Some prior identity associations survive; provider/group/package/receipt lifetime does not. These targets also need not exhaust all imports. |
| `software/v5/ordinary_library_package/completion_api.py` final result | Targets, units, previews, candidate/supplement hashes and admission. | No durable external supplier/group association to reuse. |
| `software/v5/ordinary_multi_source/ordinary_acquisition.py:172-224` | Custody already derives indexed locators for every actual unit output and commits them with evidence. | Support-only output lookup works at a known holder. Its put result is not a membership/delta or supplier-provenance feed. |
| `software/v5/ordinary_authoring_offers/authoring_offers.py:24-29,95-108,133-182` | Bounded exact export-key map of strict Git repository/commit/project/module/export/toolchain offers. | Its request binding and bounded map pattern are reusable; its schema and authoring claim are not custody referrals. Do not overload Git fields or fetch repositories as inert evidence. |

Previews expose type bindings, so they cannot replace raw evidence when producing
the complete direct-import graph. Native source module imports do not identify
custody suppliers either. No new export, earlier proof-corpus scan or owner open
is needed to derive identities from the selected contribution units. Conversely,
no content hash can recover absent location provenance. A new optional explicit
hint input, or a future acquisition-provenance handoff, is necessary for external
groups. It must be retained separately from mathematical owner state.

The retained contribution-bundle controls illustrate why selected targets are
insufficient: `bundle-contribution` has 21 units but 11 targets, and
`bundle-completion` has 3 units but 1 target. The completion evidence for
`CommonsProjectIntake.applyFour_eq` actually imports
`CommonsPackageExample.applyTwice_eq` and `CommonsPackageExample.applyTwice`.
Its current mathematical bytes supply those exact import identities, not where
another operator holds them. The saved preparation receipts do not claim
dependency completeness or host publication. These are retained file facts, not
a grouping experiment or evidence of a currently live remote holder.

## Smallest complete proposed contract

1. **Immutable bundle identity and membership.** Define a domain-separated GroupID
   from S and the exact baseline-manifest hash. Derive rows
   `(GroupID, S, ExportID, name, UnitID)` for every output of every supplied unit.
   A group identifies that exact finite bundle, not a mathematical theorem,
   universal package name, transitive closure or permanently available custody.
   Keep all hints outside evidence, preview, locator and public discovery-record
   bytes; their strict schemas and mathematical identities stay unchanged.
2. **Actual direct-import associations.** For each referring UnitID derive every
   exact imported name/ExportID. Associate a locally included import with the
   same group. An external import receives up to two explicitly approved
   GroupRefs or remains uncovered. A GroupRef is `(GroupID, descriptor_anchor)`;
   the anchor is an explicit stable HTTPS authority/route, not a value derived
   from GroupID. Validate input associations against the actual import keys;
   keep their origin and approved retention horizon in separate operator data.
   Initial coverage cannot be manufactured from `acquired_targets`.
3. **Shared mutable descriptor.** An approved anchor serves the group's finite
   candidate endpoint list, descriptor revision and expiry. A listed holder
   claims custody of the group's member set; a partial holder needs a different
   smaller group or must not be advertised as holding the full group. This is
   still an untrusted routing claim: exact locator/evidence checking remains
   decisive. An operator can run its own anchor or explicitly choose another;
   there is no remote arbitrary registration API or compulsory global service.
4. **Point sidecar query at the acquired unit's provider.** A new route takes
   `(S, referring UnitID, missing ExportID, expected name)` and bounded reply
   limits. It returns only capped matching GroupRefs, or partial/unavailable.
   Lookup checks a locally prepared actual-import row. The initial provider is
   already known through discovery/acquisition; no extra global group search is
   needed. Transitive units may supply their own such sidecars when acquired.
   A provider without the route remains usable through existing fallback.
5. **Resolve and acquire.** Query an allowed GroupRef anchor, cache its descriptor
   only through its expiry, then try bounded allowed endpoints via the existing
   ordinary locator/evidence path. Referrals cannot authorize egress or bypass
   name/S/UnitID/ExportID, evidence or mathematical acceptance checks. Preserve
   the referring unit/provider association within this acquisition so later
   actual imports can request their corresponding sidecar.

The new value is step 2's explicit external association. If the discovered
provider already holds all required units, its existing exact routes suffice;
grouping adds no location coverage. A target provider holding only the target
can instead name a reachable group held by an independent supplier unknown to
the reader. Success requires that hint, anchor and holder to remain usable under
the reader's policy and original grant. A new unannounced mirror is invisible.

Stable anchors are a real service assumption. If only bare current endpoints are
copied into every import row, an address change needs all incoming copies updated.
Factoring endpoints into one reachable group descriptor avoids those rewrites.
Changing the anchor itself still requires updating inbound referrals or retaining
an approved forwarding/alias service; GroupID alone cannot resolve the change.
Descriptor expiry/renewal is independent of proof validity and does not promise
the service will last. Retiring a group leaves stale cached referrals until their
expiry; unavailable attempts remain charged.

## Full-manifest work versus point lookup

The proposed production pass reads the new bundle once. The read path must not
download or rescan its entire manifest, membership map or proof corpus for every
missing export. A concrete source cut is a separate locally built indexed sidecar
store with exact `(S, referring UnitID, imported ExportID)` lookup, capped GroupRef
rows, and group-descriptor lookup. Reuse the custody store's transactional indexed
metadata pattern, including persistent quota counters, rather than a process-wide
rebuild of all earlier sidecars. This is new storage behavior requiring review,
not something present in `OfferMap` or today's host.

Store the selected bundle digest and its insertion completion in the same local
metadata transaction as its rows/counter delta; a completed exact retry compares
that digest and returns without recounting all previous groups. Any stronger
raw-byte retry comparison charges the selected input bytes. Publish metadata
only after relevant custody exists. Crash before sidecar commit leaves valid
custody with absent hints; it does not require cross-store mathematical atomicity.
Pending entries must not produce descriptors claiming full group custody. Normal
startup reads persisted metadata; database recovery is charged, and a repair
that rebuilds the index is explicitly linear in retained sidecar bytes/rows.
Never reopen all historical proofs to reconstruct lost external GroupRefs.

For a deliberately small host, one immutable capped map parsed once at service
startup is a simpler acceptable variant. Its startup cost is the whole map;
replacement reparses it, and a bounded cache must charge cold reparses after
eviction. It cannot be described as incremental unbounded operation. A per-group
map downloaded once by a reader similarly charges its entire bounded byte size;
point replies avoid that cost. None of these maps discovers an arbitrary group
from only an uncovered ExportID.

## Publisher, overlap and continuing service costs

Let B be selected new evidence bytes, E its output exports, I its direct-import
rows, H the retained external GroupRef associations, and G the retained groups.
Count metadata encodings/indices and descriptor endpoint bytes separately from
proof bytes. With bounded rows, H <= 2I in the proposed profile.

| Operation | Work and retained cost |
|---|---|
| First group preparation | O(B + E + I + H) traversal/encoding; O(E + I + H) logical rows, plus actual encoded bytes. This can reuse the existing new-unit parse but adds metadata work. |
| First host insertion | Indexed row work, conservatively O((E + I + H) log N) for N retained index rows, plus selected-byte checks. Persist row/byte/group counters transactionally; no earlier-corpus count scan. |
| Exact duplicate group | Exact group-key lookup and committed input-digest comparison; charge selected bytes if reread. No repeated network publication per member. Modified hint associations are a separate approved metadata revision, not an exact retry. |
| Overlap | Membership remains a many-to-many relation. Across bundles count sum(E_g), sum(I_g), sum(H_g), not unique exports. Deduplicating raw units does not deduplicate all memberships/referrals. Limiting a key to preferred groups is local selection and can reduce coverage. |
| Endpoint renewal | One descriptor update per active group/anchor revision, plus its endpoint-list bytes and requests. If E_active exports share G_active groups, renewal can fall from per-export to per-group multiplicity; no guaranteed factor without the actual group/overlap distribution. |
| Ongoing serving | Fund descriptor and hint requests independently of the reader's grant, alongside ordinary custody/HTTP serving. There is no DHT routing maintenance, but anchors and target-sidecar retention are not free. |
| Expiry/withdrawal | Check expiry on every use. Descriptor tombstone/expiry prevents new use; cached rows may remain stale. Indexed expiry work can process bounded due descriptors. Removing full group metadata costs its E_g + I_g + H_g rows and is a separately budgeted operation. |
| Restart/recovery | Database open/recovery and selected durable counters; no claim of zero startup cost. Index rebuild/repair costs all retained sidecar metadata and needs an explicit grant. A lost association cannot be reconstructed from proof IDs. |

Grouping does not remove the O(E) member identities or O(I) import edges. I may
exceed E, singleton/high-overlap groups may offer no renewal saving, and descriptor
requests add reader cost. Compare the DHT alternative's real operator costs,
not only its publication count. In particular, the old runtime controller's
192 MiB check is a **verified payload-byte limit**, not a process RAM ceiling;
process/Job memory is separate. No performance or break-even measurement is
claimed here.

## Finite reader and server envelope

The following is a concrete candidate comparison profile, not an adopted default
or assurance that every otherwise valid contribution fits. The caller may select
smaller caps. Scope every counter to the original receive, never to a referral.

| Bound | Candidate ceiling / behavior |
|---|---|
| Hint traversal | At most 32 point hint requests for actual missing-import demands; at most 256 referral edges considered and depth 4 from the discovered target. Never recursively explore unrelated advertised members. |
| Groups and anchors | At most 8 distinct GroupRefs/descriptors; up to 2 GroupRefs per missing key. No repeated descriptor refresh in the operation after expiry/failure. |
| Candidate endpoints | Descriptor holds at most 2 endpoints; attempt at most 2 learned endpoints per missing key in total, deduplicated across groups. At most 16 distinct learned network origins including anchors. Configured fallback remains separately capped at its existing 1-8 sources. |
| Metadata responses | Hint body <= 8 KiB; descriptor body <= 4 KiB. At most 32 * 8 + 8 * 4 = 288 KiB reply-body grant, with bounded request bodies and transport/header limits also explicit. |
| Shared request/deadline grant | Hint and descriptor calls consume at most 40 requests; all metadata, locator, evidence, configured fallback and failed attempts share one owner-selected total, for example 128 requests, plus the original byte/time limits. The total cap can stop earlier than individual maxima. |
| Deduplication | Track exact `(S, referring UnitID, missing ExportID, hint provider)` requests and `(GroupRef, revision)` descriptor use, and cap candidate retries per demanded key. A stale/negative result is never proof of global absence. |

The larger ordinary evidence-byte grant remains explicit and unchanged; the
288 KiB figure covers only maximum metadata reply bodies. Anchors/hints must be
charged on failures and truncation as well as success. `OrdinaryBudget` currently
allows `charge_external` only before sequence zero ends: a discovered late hint
cannot obtain a fresh prepaid grant. Either reserve the complete finite hint
slice before the first acquisition, conservatively charging unused reservation,
or add an explicitly reviewed typed begin/settle integration under the same
ledger. Neither permits a counter reset. Root's separate `RECEIVER-SEAM.md`
assignment owns the transport implementation choice.

For each learned dial the effective deadline is the minimum of the original
receive deadline, relevant descriptor expiry and any original contact expiry.
Check it after setup and immediately before dial; preserve it across retries.
The existing ordinary relative-timeout HTTP path is not enough by itself.
`ordinary_connect_ownership/fair_exchange.py` supplies an absolute-deadline owned
transport pattern but its current route allowlist does not include these new
routes or every ordinary acquisition route. That extension is shared necessary
receiver work, not a free grouping advantage. Owner egress policy still applies
to every learned anchor and endpoint; a rejected origin is a bounded failure.

Servers independently cap connection count, request count, reply bytes, duration
and metadata rows/bytes. An indexed hint reply does O(log N + k) row work with
k <= 2; a descriptor emits at most two endpoints. A caller cannot enlarge the
operator's service or retention allocation. Return a typed unavailable/partial
answer on a cap, missing association, wrong actual-import key or expired group.

## What would change the choice

The source record supports a narrow viable alternative, not automatic adoption.
For the discovery-led workflow, choose grouping if explicit dependency GroupRefs
can be carried at contribution preparation, stable anchors are acceptable, and
actual bundles share enough exports/endpoints to offset edge storage and extra
lookups. The next deciding evidence is the required coverage and source-level
size of that integration compared with `SOURCE-FEASIBILITY.md`; no new benchmark
is required to identify the missing provenance or distinguish the coverage.

Choose the DHT model if the important demand is an exact import with no reachable
referring sidecar/group path but with a participating arbitrary holder. Choose
existing known suppliers if neither model's additional covered workflow merits
its producer, retention, service and receiver costs. In every case, mathematical
truth, discovery of a target, location of support and continued service remain
separate claims. This checkpoint authorizes none of those implementations.
