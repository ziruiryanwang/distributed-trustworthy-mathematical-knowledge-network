# Selected custody closure to an inert baseline bundle

2026-10-26. Source-only feasibility review. No implementation, product imports,
runtime, protected-state access, native work, tests or Git mutation. This review
does not select execution or a new mathematical authority.

## Conclusion

**Compatible in principle and smaller than generating a native module. Root's
challenge improves the design: do not require a source acceptance context.**
The first proposed contract tied export to protected accepted bindings. That is
unnecessary when the output deliberately asserts no acceptance and the receiver
checks independently. Removing it avoids selected-parent validation/restoration,
catalog opening, and the mistaken suggestion that producer authority transfers.
It also permits exporting a structurally complete claim not yet locally checked.

The
existing baseline manifest has no producer-specific authority: it contains only
`schema`, `semantic_id`, and ordered batches of exact `unit_id`, `raw_sha256`,
`raw_bytes` entries (`ordinary_baseline/baseline_bundle.py:235-276`). Paths are
derived as `units/<unit_id>.json`. The receiver does not require a producer
PROFILE, compiler receipt, project identity, source approval or target intent.

Use existing `split_units` and `make_manifest` on unchanged portable evidence.
Do **not** fabricate a `bind_writer` input, native extraction statistics or
`PRODUCTION.json` report: those belong to the different compiled-project route.
The ordinary receiver's `_plan_all` checks all dependencies before native work;
each actual batch is then independently admitted above its confirmed local root
(`baseline_intake.py:156-255,257-333`). Exported provenance cannot waive this.

## Existing routes checked first

- An already retained complete baseline bundle can directly use `intake-baseline`
  above a smaller eligible root. No new export is needed for that case.
- `produce-baseline` executes the approved compiled-project exporter. It cannot
  export selected local inert custody alone and would add unnecessary native work.
- `export-module` collects the selected full proof closure but ordinarily creates
  and checks a native module. Its all-anchored shortcut reuses a local module;
  neither result is the requested self-contained inert baseline bundle.
- `peer publish` creates previews/index records; `inspect` reads one unit. Neither
  exports a selected self-contained closure. `peer receive` can re-admit a closure
  through an available provider, but adds service/network work and is not an
  offline export. `OrdinaryAcquisition` uses local custody for retention, **not**
  a local read-through shortcut: preview/locator/evidence all call `_fetch`.
- `ordinary_module_anchor/module_closure.py` already demonstrates the needed
  complete-import/group traversal and exact warrant checks. Its 32-unit/4-MiB
  ceilings and native-request construction are specific to module generation;
  do not enlarge or secretly repurpose that used implementation.

Thus a small new data-only public seam has a distinct missing capability when
the investigator has inert custody but no original compiled project or
retained complete bundle. It is not justified as another way to copy an already
available bundle, nor as an automatic archive of an entire owner history.

## Bounded algorithm and contract

1. Select actual supported custody and semantics, a fresh disjoint output
   directory, original finite resource allowance and exact
   nonempty target triples `{name, export_id, unit_id}`. Bound target bytes/count,
   reject duplicates and fixed-basis-only targets (the bundle requires units).
   Use the bounded read-only custody snapshot described below. No source parent,
   owner catalog, accepted-result flag or imported success report is required.
2. Read the exact pinned 581-name basis inventory and construct its existing
   `basis_symbol_id` map. It is the fixed interpretation of these imported names,
   not a fabricated locally checked context.
   Stop only at a matching basis **name and identity**, not a familiar name,
   arbitrary local acceptance, module anchor, or an unstated receiver parent.
3. For each pending nonbasis export, resolve its existing custody locator,
   verify name/export/unit binding,
   and fetch the bounded complete raw V2 unit. Reparse identity/semantics/census;
   verify the requested name is actually exported and target UnitID agrees.
4. Deduplicate by complete UnitID; retain bytes unchanged. Derive exact identities
   for every exported name in that atomic group; refuse shadowed basis names,
   overlapping groups or conflicting names/identities. Traverse **all**
   declared imports, including theorem proof-only imports. The authoring-signature
   frontier is insufficient for this self-contained independently checkable export.
5. Bound each fetch before allocating its BLOB; bound aggregate bytes, unique
   units, names, nodes, import edges, queued identities, bindings and output bytes
   during traversal. Missing custody/locator, unsupported semantics, conflict,
   cycle or exceeded budget is refusal, never an omitted dependency.
6. Topologically order the complete selected units relative to exact fixed-basis
   bindings. The smallest implementation can reuse `ordinary_admission._plan`
   with a **planning-only** basis projection, require READY/no missing/no reused
   units, then use `B.split_units` and `B.make_manifest`. This invokes no owner
   preflight/admit or fabricated acceptance. Do not present the projection as a
   protected environment. Cap the selection at the existing planner's limits.
7. Write each exact raw file once in fresh output, checking length/hash. Write a
   separately named inert selection/provenance sidecar, then `manifest.json` last;
   verify the complete expected output census and final byte pins. Do not overwrite
   a previous result or silently resume. The result returns explicit bundle path,
   manifest hash and exact original target triples, not a new checked root.

Use the intersection of existing baseline/planner/evidence limits, not a new
larger allowance: at most 1024 units, 64 MiB evidence, 8 MiB per unit, 2,097,152
nodes, 65,536 names and 262,144 import edges, with baseline manifest/binding/native
array limits also enforced. All may be lowered. `split_units` retains whole
topologically ordered groups; the receiver may still refuse its smaller local
capacity or native resource needs. Extending to 8192 units is unnecessary for
this first seam and would require a different aggregate planning argument.

The provenance sidecar records exporter/support identity, custody selection,
semantic/basis identities, ordered target triples, manifest and raw pins, census
and actual cost/closure status. It must explicitly say
`mathematical_acceptance=false`, source acceptance not checked, and no transferable
warrant. Do not invent a source context or local admission. Do not reuse producer helper
report schemas to make an offline selector accept it; existing explicit
`intake-baseline` arguments already suffice.

## Read-only custody access, without an owner catalog

`OrdinaryStore` is byte custody, not accepted mathematics. Its current constructor
sets journal/max-page PRAGMAs and has no OS owner lock. Do not reuse that constructor
and label it read-only. Its selected getter checks are reusable source patterns.

A small standalone reader should require the same supported ordinary nonaliased
path/file shape, bounded database size and exact custody config/semantic selection;
open an escaped SQLite URI with `mode=ro`, `query_only=ON`, `trusted_schema=OFF`,
bounded busy timeout/cache, and no journal-mode/max-page writes. Begin a read
transaction before reading meta/config and retain it for all selected lookups.
Validate schema/config and use fixed parameterized primary-key queries, with
length checks before reading each bounded BLOB. Validate locator name/export/unit
binding and each raw SHA/content identity, then independently parse V2 semantics
and full imports. Close/rollback the read transaction on every exit.

SQLite snapshot consistency handles normal supported transactions; in the
current DELETE journal mode the finite reader can delay writer commits. Report
that interference as cost. Do not use `immutable=1` on live custody, bypass hot
journal errors, or copy the entire database to obtain a snapshot. Unsupported
sidecars/hot recovery needs should refuse; retain existing no-external-file-
mutation and protected-path premises. Concurrent malicious OS replacement is
not solved by a read transaction. The first implementation should state its
ordinary serialized-use expectation even though SQLite also protects snapshot
consistency against supported writers.

No mathematical source-trust rule is weakened: exported claims may be false.
The guarantee is exact complete *syntactic dependency* closure under selected
semantics, not well-typedness or derivability. Recipient admission remains the
unchanged authority. Hash collisions and implementation correctness remain their
ordinary assumptions; a source acceptance check would not eliminate them.

## Cost, failure and assurance boundaries

Let D be selected complete nonbasis closure, S selected raw bytes and E import
edges. Charge fixed reader/support validation, selected locator lookups,
hashing/parsing S, topology `O(|D| log |D| + E)` under ordinary map models, repeated
bounded validation in existing constructors, and writing/readback of S. Retain
bounded raw buffers; discard per-unit parsed syntax after extracting bounded
metadata. No proof checking is done by export. It is **not** proof-free transfer:
the destination subsequently reads/checks this full selected closure above its
chosen exact parent, pays setup/restoration/custody, and may fail.

No source catalog open/admission, custody mutation, native loading, network or
Lean-source execution is needed by this standalone transformation. A command
implemented through the existing owner facade would reintroduce catalog opening
and interruption bookkeeping; do not take that path merely for CLI symmetry.
Source-parent restoration K is absent, not hidden as prevalidated input.

Failure before output writing leaves no exported bundle. Failure during writing
may leave a partial fresh directory; retain it and report phase/manifest-write
uncertainty, never delete or declare success automatically. Manifest presence
alone is neither a successful export invocation nor mathematical acceptance.
The receiver already revalidates exact manifest/evidence bytes and dependencies.
Its multi-batch failure can retain a checked prefix; export must not promise
atomic receiver acceptance or automatic retry/branch migration.

This is a plausible convenience with a concrete use: extracting just the needed
inert closure for independent smaller-context intake without rebuilding a
producer project. It neither proves a net growth benefit nor removes selected
proof ancestry; choose it only if that workflow, rather than an existing retained
bundle, is actually the next obstruction. No code or experiment is selected here.
