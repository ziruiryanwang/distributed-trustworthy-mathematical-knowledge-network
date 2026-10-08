# Next-priority challenge: aggregate custody before general state migration

2026-09-23. Independent read-only challenge by `discovery_v1_gap`.
Canonical guard passed. No product import, command, test, state mutation or
private-key read. Source references below are relative to frozen
`product-local/peer-contacts-source-06/` unless otherwise stated.

## Recommendation

**Do not select general database/profile migration next. Select the smallest
multi-result custody/catalog improvement: one holder can advertise two
independently acquired results together through one committed view.**

This addresses a concrete obstruction to reciprocal corpus accumulation, not
an attribution mechanism or another proof-generation benchmark. It also makes
planned transfer to a successor node materially more useful. First confirm
that this is the intended small-cohort v1 role: a participant can retain and
share several contributions received from others, not only its own results.
If root deliberately excludes that role, choose a documented bounded rollover
policy instead; do not silently interpret this recommendation as required
unbounded replication or a global index.

## What is established, and what is not

- Operator05's [qualification](../../experiments/operator-onboarding-01/QUALIFICATION.md)
  establishes independently authored mathematical reuse/contribution using
  shipped instructions, with one agent operating two same-host nodes. It had
  one disclosed shell correction and a retained source refusal; it was not
  independent-host or general efficiency evidence.
- The earlier [matched pair](../../software/qualification/usefulness-consumers-01/COMPARISON.md)
  already selected a useful append theorem among seven entries without its ID
  and substantively reused it. Repeating the same fold experiment is not a
  central unresolved capability. Broader heterogeneous retrieval remains open.
- Source06's [qualification](../../experiments/peer-contacts-01/QUALIFICATION.md)
  reports root-verified real contact continuation; its independent terminal
  audit was still pending at this review. It retains checked state while adding
  a supplier and admitting another theorem. Static copied supplier views do
  not qualify new owner-hosting authority or multi-result custody.
- No result above establishes sustained useful growth, general library
  coverage, migration, indefinite storage or large-network performance.

## Existing paths already solve much of bounded continuation

| Concern | Existing supported route; remaining boundary |
| --- | --- |
| Initial allowance exhausted | `status` plus explicit supplied-capacity `renew`; no refund. Hard lifetime ceilings remain. `API.md`, `py/capacity.py:13`, `py/storage.py:490`. |
| Current context too large | Historical `select_context` selects another owned context; later work freshly checks its files. It does not shrink an intrinsically oversized dependency closure. `API.md`, `py/checking.py:243`. |
| New remote address/pin | Append a new owner-authorized alias; old handles retain old endpoint bindings. No own-listener rotation. `py/storage.py:584`, `PEER.md:194`. |
| Producer disappears after transfer | `replica_expose` retains exact received bytes; committed views are served without reopening old package copies. This already has a genuine single-result surviving-holder qualification. `API.md`, `py/service_worker.py:34`. |
| New software/configuration | Keep old installation/state read-only as the supplier; acquire selected available mathematics into a fresh node and freshly admit it. This is mathematical transfer, not request/history/state migration. Same foundation/wire compatibility and explicit service are premises. |
| Continued service | `host` resumes finite owner grants for one committed view; a new grant is an explicit new authorization, not a counter reset. Separate hosting-journal ceilings remain. `HOSTING.md`. |

The contact test already consumed operator05-origin mathematical bytes in
source06; another identical cross-cut byte transfer adds little. Nothing in
the mathematics acceptance rule requires preserving old local request IDs,
private artifact handles, source paths or historical acceptance flags across
software upgrades. Copying those is a much stronger, harder goal than carrying
useful mathematics forward with fresh checking.

## Actual obstruction: custody is not a composable shared catalog

Let `Published_H(e)` mean holder H has the authenticated local publication
record required by ordinary exposure, and `Custody_H(e)` its exact successful
acquisition record. In this implementation a product-served view V is allowed
to contain acquired-only entries only when it is a singleton:

`(exists e in V: not Published_H(e) and Custody_H(e)) => |V| = 1`.

Evidence is stronger than an absent feature description:

1. `py/peer_node.py:318-334` requires a local publication record for every
   ordinary `expose` candidate. Fresh admission of a peer result does not
   manufacture that record.
2. `py/peer_node.py:362-394` accepts exactly one `acquisition`, builds one
   original-bundle offer and requires one exact advertised entry. Its commit
   branch at `:435` reauthenticates that singleton custody binding.
3. `py/service_worker.py:54-56` independently requires `len(selected) == 1`
   for the replica-custody branch. A hand-built larger view is therefore not
   an owner-API workaround.
4. `HOSTING.md` selects one immutable view. Switching that view is not a stable
   combined catalog; old snapshot requests may become unavailable. Multiple
   endpoints/nodes are a possible manual workaround, with more services,
   contact slots and operational work, not an impossibility theorem.

Consequently, two distinct acquired-only roots cannot share one current managed
view even with exact bytes, quota and an honest willing owner. The documented
inert helpers can manually build/serve a larger view, but do not create its
ledger authority for `manage serve/host`; that is a lower-level owner-script
workaround, not an impossibility of raw transport. Integrating this existing
capability is more directly tied to usable corpus custody than preserving
configuration-bound local bookkeeping across versions.

## Smallest consequential successor

Keep the existing single-acquisition API unchanged and add a bounded plural
selection, or another explicit command if that makes compatibility clearer.
Begin with a finite cap justified by existing aggregate-byte limits; two
entries suffice for the discriminator. Do not simultaneously add mixed
publication/replica catalogs, routing, automatic retention, ranking or migration.

Reuse existing facilities: `replica_custody` authenticates each selection;
`peer_wire.build_view` already accepts a bounded list and builds wire-v2 pages
with aggregate limits (`py/peer_wire.py:406-471`); ordinary exposure already
shows sequential selected-package validation with request-local cache release.
No new wire format, native proof protocol or database table appears necessary
from this read, but the implementer must verify that conclusion.

Required invariants: every selected acquisition is client/config/endpoint/
foundation bound; no duplicate sequence or unsupported descriptor variant;
every reconstructed bundle/entry equals its original advertised bytes and
metadata; validation/reply/selected-row lengths agree; commit rechecks every
authority; the read-only service validates every row without source-package
reads. Retain existing total bytes, time, request and reservation ceilings.
Aggregation is neither publication nor mathematical acceptance. Receiver-local
fresh `admit` remains mandatory. Treat aggregate memory/work as a real bound,
not the sum of individually permitted unbounded loops.

### Plural custody, not a unified authority API

Choose `replica_expose` with exactly one of `{acquisition}` or
`{acquisitions:[...]}`; reject both/neither/empty and retain old singleton
semantics. Keep plural views custody-only. Unifying publication and custody
would add tagged input selection, mixed commit evidence and branch-specific
duplicate policy without helping the selected two-acquisition case.
The existing service already has two per-row authority shapes, so plural
custody can reuse its replica branch after removing only the singleton
restriction and preserving all other per-row/count checks.

Do not silently deduplicate: repeated acquisitions can have distinct handles
but reuse one P1 sequence (`py/peer_node.py:246`); reject repeated sequence,
descriptor or original bundle selection. Retain `DESCRIPTOR_VARIANT_UNSUPPORTED`
and exact original manifest/entry/bundle binding—do not choose a preferred
proof or replace a raw received manifest with its normalized analysis copy.
Wire bounds remain 256 entries, 18 MiB per bundle and 64 MiB per whole view;
these are ceilings, not permission to skip aggregate checker/cache/SQL/time
limits. Start with an explicitly small plural cap if those larger costs are
unqualified. No new public metadata field or wire version is required.

## Discriminator and stop condition

Use two already qualified, genuinely distinct roots under the same foundation,
preferably neither merely the other's sole advertised dependency/root. Do not
commission new proof authoring, another setup study or a usefulness contest.
On fresh allocations, acquire both through public APIs; commit one plural
replica view; stop the original suppliers; serve that view through actual
`manage serve/host` rather than the standalone test fixture adapter. A fresh
consumer enumerates both from one peer/snapshot, acquires each exact bundle,
and freshly admits both. Preserve original identifiers and nonpublication
status. The new observation is two-result continued discoverability/custody,
not single-result transfer or a claim of mathematical novelty.

Small native-free negatives should cover duplicate selection, wrong-client
custody, a corrupt selected bundle, total-byte refusal, and one invalid row
preventing view commitment; do not multiply unrelated adversarial suites.
Stop when the plural view and downstream checks pass an independent outcome
audit with costs, or a concrete authority/resource counterexample defeats the
design. Retain failures; do not relax bounds to force a pass.

## Why migration and discovery redesign are not first

Migration becomes central if the release promises transparent upgrades,
continued private unpublished work, or salvage from a source that can no
longer operate. No supported general solution currently exists. Lifetime
ceilings (4,096 requests, 256 stages, 64 GiB authorization, 64 grants) and
hosting ceilings are real; `renew` is not indefinite participation. Moreover,
`expose/replica_expose` themselves require ordinary capacity, so waiting until
all allowance is exhausted can strand unexposed local material. Planned
handoff therefore needs spare capacity and available old bytes/services.
If root cannot accept those explicit bounded-v1 premises, prioritize a narrowly
specified independently funded export/handoff path—not unrestricted database
migration or silent reset. The current positive tests do not settle that choice.

Agent-facing presentation/heterogeneous retrieval is also important: remote
discovery is paged enumeration and local indexing is one exact type-symbol key;
formal DAG interpretation before admission can be awkward. But an independent
agent already completed bounded selection and ordinary reciprocal research.
No new source-level correctness blocker warrants a search/ranking redesign yet.
A future fixed heterogeneous workload should discriminate a concrete proposed
improvement before adding one. The present proposal removes an explicit
two-result custody obstruction with existing wire/index facilities.
