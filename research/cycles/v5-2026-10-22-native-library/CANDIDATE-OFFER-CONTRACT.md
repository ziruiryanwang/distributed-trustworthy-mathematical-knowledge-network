# Candidate offers: bounded contribution, unchanged receiver trust

2026-10-24. `growth_payoff`, source-only cost/closure contract. This does not select
an experiment, source edit or public deployment. Read the existing producer,
worker, native exporter, bundle binder, ordinary custody, preview and peer-index
boundaries. No new mathematics schema, certificate, task list or intention input.

## Separate three operations

1. **Export approved local mathematics.** The existing
   `baseline_production.produce_bundle` opens no mathematical owner/catalog. It
   calls the pinned exporter once on explicitly approved already compiled local
   modules, then uses `baseline_bundle.bind_writer` to construct an inert bundle.
   Approval is local execution approval, not mathematical acceptance.
2. **Offer existing inert bytes.** A provider validates an explicitly selected
   bundle and selected target identities, puts evidence/previews in custody and
   publishes candidate index records. It does not check a theorem or load a
   producer binary. A Git/file route can carry the same bytes without a server.
3. **Receive and use.** The unchanged receiver selects candidates, obtains missing
   dependencies, independently checks them against its own warranted environment
   and uses only the resulting accepted mathematics. A candidate record, producer
   report or index membership is never this acceptance event.

Do not couple all three into a compulsory producer workflow. A producer may
already have a suitable bundle; a provider need not be its mathematical author;
a receiver may decline it. Keep existing accepted `publish` semantics unchanged.

## The principal cost limitation: owner-free is not cheap cold export

The actual `BaselineExporter.lean` imports the selected modules' **private compiled
environment**, calls `Export.indexSource` eagerly, and exports the complete selected
dependency closure outside the fixed 581-name seed. Module import can load much
more than the requested theorem's dependency closure. The scan counts all source
constant records, though it retains only grouping records in its auxiliary index.
It does not stream an arbitrarily large library or stop at a receiver's warm cache.

Let `E` be the imported environment, `D` the selected whole-unit dependency closure
outside the seed, and `B(D)` its encoded bytes. The honest cost decomposition is

    export = import(E) + source census(E) + closure/encoding(D)
             + writer parsing/binding(D) + retained output(B(D)).

This has no mandatory dependence on the total network size, but can still be
large for one local library or one theorem. There is no universal small bound on
`D`, dependency conversion or import memory. A single indivisible declaration
group can exceed the unit bound. Native writer construction, its serialized JSON,
Python parsed input and output units can coexist; a 64 MiB wire ceiling is not
a 64 MiB peak-memory guarantee. Limits provide bounded refusal, not success.

Relevant current fixed ceilings:

| Boundary | Selected ceiling |
|---|---|
| Native source census | 262,144 constants; 65,536 grouping records |
| Export closure | 8,192 units; 262,144 edges; 20,000,000 scanned nodes |
| Encoded evidence | 8 MiB per unit; 64 MiB total writer/evidence ceilings separately |
| Bundle | 64 batches; 1,024 units per batch; 2 MiB manifest; 1,024 targets |
| Current peer receive | 1,024 selected missing units; 4,096 missing exports; 1,025 preflights; 64 MiB selected evidence |

Native bounds are fixed in the selected executable. Lower Python bundle limits
can refuse *after* native export; they do not retroactively shrink native work.
`produce_bundle` therefore reserves the writer ceiling plus output allowance,
manifest and metadata/log allowances before launch. Its controller is cooperative;
the public command still needs an enclosing process-tree budget. No automatic
retry, quota increase, recompilation or repartitioning campaign follows refusal.

A valid maximum-sized producer bundle need not fit one current peer receive.
Do not label every legal bundle immediately usable. A particular target's missing
closure can fit even when the whole bundle does not; that is a per-receiver fact.
The first facade should report the bundle/target census and the receiver profile
limits, not promise arbitrary cold acquisition. Normal approved packages remain
the fallback/comparator for large common backgrounds. Avoid a new producer cache
or dynamic-boundary protocol until a real repeated-export cost justifies it.

## Re-offer existing bytes; do not re-export for an advertisement

For the retained six-unit bundle, or any supported exact bundle already obtained,
the offering operation needs no native importer, original `.olean`, source project,
producer owner, old match report or saved successful `PRODUCTION.json`. It needs:

- Exact manifest bytes/hash and a selected ordinary input directory, using only
  canonical entry-derived filenames; no arbitrary paths nominated by peer JSON.
- Bounded reading and `read_manifest`/`validate_batch` for every selected entry,
  checking lengths, hashes, unit identities and aggregate census across batches.
- Selected target triples whose name/export/unit IDs derive from those actual
  evidence units; derive previews using existing `preview_from_evidence` and
  resolve them against the exact same bytes.
- Explicit finite storage/index resources and an operational serialization owner.

`read_manifest` and `validate_batch` do **not** establish complete dependency
closure. The first offer command can honestly say “these exact candidate objects
are hosted” and retain incomplete-dependency outcomes at receive; it must not say
“all proofs are available” from manifest success alone. If complete fixed-seed
closure is a required local policy, add only a bounded structural dependency check:
each import ID/name must be supplied by the fixed seed or an earlier actual unit's
derived exports, with unique names/units and no forward/cyclic references. That
checks representational supply, not proof validity. Do not fake an accepted context
or reuse a saved producer-PASS as authority for that check.

Put evidence first, then previews, then index records. Report each committed
object/record and preserve partial results on failure. SQLite transactions in the
two stores do not make a cross-store batch atomic. Evidence-first reduces newly
advertised missing objects; it does not provide perpetual availability or remove
the need for custody retention policy.

Re-offering still pays parsing, hashing, storage lookups and index work. Its useful
property is **no repeated native export/admission**, not zero-cost publication.
Existing `OrdinaryStore.put_evidence` is exact-byte idempotent and already derives
locators; reuse it, `put_preview` and the current index adapter. The old
certificate-packet `offer_enumeration` is unrelated. Existing candidate wire/type
previews already denote untrusted claims; do not create a second wire format.

## Operational ownership is not mathematical adoption

`OrdinaryStore` and discovery `DS.Store` do not supply a shared process lock.
Current service requires exclusive serialized use of both stores; the public CLI
obtains that via the configured mathematical owner's lock. **Do not simply remove
that lock while adding owner-free contribution.**

The cheapest compatible split is an owner-free file exporter plus an explicit
provider candidate-ingest operation using its existing configured owner lock,
without requiring targets in its accepted context and without calling admission.
This leaves provider setup/custody costs in the service account, not in each
producer's obligations. A dedicated nonmathematical provider lock may be justified
later; it must not silently create a second lock domain for existing stores.
No public remote-write endpoint is needed: a provider explicitly chooses inputs.

Unaccepted candidate indexing can increase spam and futile checking. Each provider
may filter, charge, quota or independently check before advertising; consumers can
choose providers and retain finite aggregate budgets. Such filtering affects
availability/relevance, never the receiver's mathematical rule. Existing accepted
publication remains the sensible route when its producer already maintains warrants.

## Missing glue and payoff decision

The costly core exists. Missing work is a coherent pinned **public producer facade**
and optional **candidate-to-custody/index facade**. The producer source currently
assumes worker/executable/binder layout; the consolidated package separates some
roles. Reuse exact selected modules/native artifacts through one reviewed profile,
not duplicate import-name modules or a new native build. Avoid changing an existing
reference support ID solely to expose a producer command; separately pinned tooling
outside the current import-search trees is a candidate packaging solution, subject
to the normal exact-map review. Never modify a used installation in place.

Compared with compulsory producer adoption, the removed work is the producer's
otherwise unnecessary basis initialization, selected-library native intake and
reference registration/retained realization. The unchanged work is original
ordinary Lean development, approved extraction, closure serialization, hosting and
all receiver checks. Provider filtering and failed consumer trials can increase.
Therefore the route pays when removed incremental adoption cost exceeds added
facade/service/filtering costs; an already participating producer may save nothing.
Do not treat the full failed workflow cost as the avoidable amount.

The next implementation should expose these existing capabilities, not manufacture
a new theorem workload. Existing retained bundle bytes suffice for the offering
boundary; source analysis already rules out cheap-global-closure claims. If a
case cannot fit economical export/receive, use normal packages or defer it rather
than pushing all work into expensive certificates. An ordinary sharing tool may
use the same adapter: useful software, not unique peer-protocol superiority, is
the justified target. None of these claims establishes measured uptake or final v5.
