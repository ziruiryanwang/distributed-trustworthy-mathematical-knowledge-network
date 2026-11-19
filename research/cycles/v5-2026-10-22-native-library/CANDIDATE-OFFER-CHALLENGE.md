# Candidate-offer challenge: adopt the split, not a growth claim

2026-10-24. Independent source/theory challenge; no runtime or code change.
Read the complete `CANDIDATE-OFFER-CONTRACT.md` and the relevant producer, binder,
exporter, custody and peer-index source. **The contract is source-consistent.**
Its main payoff is removing compulsory producer adoption, not proving that a new
peer network outperforms ordinary sharing.

## Decision

**Support an owner-free file-export facade first.** The existing
`baseline_production.produce_bundle` already opens no mathematical owner, and the
real `baseline_bundle.bind_writer` already exists. Its production-controller
controls use a native double, but the genuine compiled exporter plus real binder
succeeded in retained `ordinary-baseline-native-workflow-02`; those six units were
later intaken. Reuse those artifacts and evidence. Do not rebuild or manufacture
another mathematical fixture just to advertise a bundle.

**Keep provider ingestion optional.** A complete useful workflow can transport
the same inert bytes by ordinary file/Git means. Exposing existing index/custody
ingestion can reduce integration friction, but is not a prerequisite for sharing
or a reason to commission new routing, consensus, reputation or remote writes.
Existing checked `publish` must retain its checked-local-target meaning.

## Hard constraints on that decision

- **No false cheap-export claim.** The native exporter imports a private compiled
  environment and eagerly calls `Export.indexSource`; it exports complete semantic
  dependency closure outside the fixed 581-name seed. Owner-free does not mean
  ancestry-free, cheap for every library, or independent of the local environment.
- **No false bundle-usability claim.** Bundle bounds allow 8,192 units / 64 batches;
  current peer receive allows at most 1,024 missing units and 64 MiB. A bundle can
  be valid yet unusable in a cold receive. Selected-target fit is receiver-relative.
- **No saved-report authority.** Manifest/batch validation checks syntax and pins,
  not complete dependency supply or proof truth. `bind_writer` checks fixed-basis /
  earlier-unit closure; a new ingest boundary cannot borrow that result from a
  producer's saved success report. Incomplete offers must be explicitly candidates,
  with receiver missing-dependency outcomes preserved.
- **No unlocked provider.** Custody and discovery SQLite stores have transactions
  but no common process lock. `peer_api.serve` explicitly requires exclusive use
  of both. The existing configured provider-owner lock can serialize candidate
  ingest without mathematically admitting targets. Never create a competing lock
  domain for those same stores. Provider setup costs remain service costs.
- **No atomic-publication fiction.** Put exact evidence, then derived previews,
  then index records; report/preserve partial commits. Two databases do not form
  one transaction. Previews and index entries confer no receiver warrant.
- **One coherent profile.** Existing exporter/controller imports assume a particular
  source/helper/executable layout. Packaging is bounded glue but not zero work;
  avoid duplicate module bindings or changing current reference support merely
  to expose a producer command. Existing native artifacts can be reused.

## What would justify growth, rather than only a nicer interface?

Fix the same accepted consumer outcomes and an equally searchable/timely ordinary
sharing baseline. Let `A` be compulsory producer-adoption cost genuinely avoided;
`I` added adapter/setup cost; `S` additional hosting/filtering cost; and `F` extra
failed consumer search/acquisition/checking cost. This split has a positive
incremental cost region when `A > I + S + F`, with common export and receiver
verification costs cancelling only if they are actually equal. Include amortized
maintenance and explicit resource weights when combining CPU/storage/bandwidth.

The region can be nonempty for a one-off producer who already has compiled Lean
work but no commons node. It need not be positive for a producer already using a
checked node, or when unchecked offers mostly cause futile consumer work. Lower
participation friction can increase available candidates; useful capability growth
additionally requires real downstream demand, fit and trustworthy reuse. Neither
theorem counts nor the failed workflow's entire cost establishes that effect.

**Stop rule:** expose the existing cheap seam with bounded glue; do not extend the
protocol if the next obstacle is uneconomical whole-closure conversion or absence
of consumer demand. Use ordinary packages as comparator/fallback. The next growth
decision should identify a concrete surviving reuse friction, not another synthetic
theorem campaign. No public-deployment or final-v5 completion follows from this
source/theory clearance.

## Higher-payoff simplification: demand before exact materialization

Source feasibility review, after actual assembly03 audit. Cost theory is owned by
`DEMAND-DRIVEN-GROWTH.md`; this addition does not duplicate its argument.

**Prefer cheap ordinary-package discovery followed by selected extraction over
making full proof-data export a publication prerequisite.** Removing producer
admission saves one tax; avoiding export of never-selected mathematics can remove
an earlier tax. This is a separation of discovery from exact-evidence production,
not a relaxation of what a receiver may accept.

### Existing code forces a genuine distinction

`ordinary_lean/portable_preview.py::preview_from_evidence` parses the actual full
unit, obtains its `unit_id`, and derives exact `type_bindings`. The preview carries
less data than a proof, but its supported construction already needs exact proof
data. `discovery/ordinary_export_adapter.py` binds records to that unit-derived
export ID and exact symbolic IDs. **Cheap preview reading is not cheap
pre-export advertising.** Do not invent placeholder IDs or silently reuse this
namespace for declarations whose evidence has not been materialized.

`BaselineExporter.lean` can extract a selected target batch (at most 1,024 targets),
but it imports the private environment and runs `Export.indexSource` on every
actual extraction. It has no cheap type-hint mode, demand queue, warm environment
or exported-closure cache. Reusing an existing exact bundle avoids another export;
partially overlapping new requests can repeat import, indexing and closure work.
Batching requests is already possible; automatic batching/cache machinery is not
therefore required or selected.

### Minimum useful path, without a new remote protocol

1. Keep ordinary repositories/package mirrors and their declaration/source
   references discoverable as **untrusted hints**, not exact evidence previews.
   A hint can identify a project revision, module and declaration and show a formal
   type sketch. It can be wrong, ambiguous, obsolete or unavailable. It is not an
   executable command, acceptance record or proof of exact source correspondence.
2. A local agent decides whether the candidate is worth pursuing. Its operator
   approves an existing compiled project and the selected target names. Invoke
   the existing exporter/binder only then, or use an existing suitable bundle.
   This works with manual/file-level demand; no remote export daemon is necessary.
3. Inspect the actual resulting exact preview/type, retain the exact bundle and
   use unchanged acquisition/preflight/admission. A mismatching hint is not a
   reason to accept different mathematics as though the requested fact was proved.
   After materialization, ordinary exact-index publication is available unchanged.

This does not yet implement a new hint index. Source/docs can supply the initial
suggestions outside the exact protocol. Source-level types may depend on notation,
macros or implicit context; extracting fully elaborated types can still require
importing the environment. The current producer's project-selection hash binds
paths/modules, **not transitive artifact contents**, so it cannot establish that
an old hint denotes the exact immutable project now selected. The newly exported
evidence and receiver check establish their own claims regardless of that hint.

No peer-supplied project path, source, Lake hook, dependency download or `.olean`
is automatically executed. Extraction remains approved-local work, not a hostile
artifact sandbox. Ordinary package use can be the better approved route when the
receiver already has a compatible project; conversion is not mandatory merely to
claim commons participation.

### Architectural tradeoff, not a universal win

Unmaterialized hints require later source/toolchain/dependency availability and a
willing extractor; exact retained bundles do not require the original producer to
return. Mirrors mitigate disappearance but do not guarantee buildability. Spam,
stale type sketches and less exact matching can increase failed consumer work.
Bound hint reads and locally selected work; never grant remote parties automatic
proof-production budgets. High-demand or disappearing projects can still justify
eager selected export. Low-demand long-tail candidates are the promising lazy case.

**Recommendation:** make demand-driven selection the default product story before
expanding the offering facade. Preserve the exact lane as a cache/verification
substrate for what is actually selected. First reuse ordinary hints and the
existing exporter; add a typed-hint adapter only if a concrete consumer search
fails for lack of it. This is a source-supported design recommendation, not a
measured growth result or an implementation authorization.
