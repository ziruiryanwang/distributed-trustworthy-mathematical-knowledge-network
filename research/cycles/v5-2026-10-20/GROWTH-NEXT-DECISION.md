# Next growth decision: distinguish the frontier requirement from aggregate A

2026-10-20. `core_growth`, source/theory only. No import, native execution,
proof, test, RAM investigation, installation or Git mutation was performed.
All predecessor sources and evidence remain unchanged. Root owns selection.

## Decision

**The constructor/helper work does not establish a positive full-cost growth
margin. Another calculator, matched-native-context implementation or repeated
small receiving benchmark will not resolve the decisive uncertainty.** Existing
break-even and exact-DAG-cut arguments already suffice in principle.

There is, however, an important architectural alternative to making aggregate
image A a prerequisite for every future frontier:

> The existing individual-module image I already supports recursive, branching
> certified modules. One I certificate can cover many local declarations. A
> valid new I certificate can advance the cold-receiver frontier without
> downloading the old theorem proofs and without any A certificate.

This is a source-supported route, **not a cheaper-production result**. The actual
first-child I snapshot previously failed its selected execution cap. A later
optimized A execution capsule exists, whereas a completed child-I capsule does
not. Do not discard that stronger A execution evidence or launch I proving on
the assumption that an older, simpler wrapper must cost less.

The next core decision is therefore a **choice of successful frontier-production
route**, with exact output obligations, rather than a new definition of growth.
Keep direct I as an explicit alternative and A as the route that batches already
published exact native nodes without separately certifying their intermediates.
Do not automatically build a second product lane or repeat either old attempt.

## What a direct-I route actually establishes

Let `Valid(J)` mean that the exact 184-byte journal J denotes a valid module
extension under the current adopted foundation, semantic policy and checking
interpretation. Its truth is conditional on the existing checker/correspondence
assurance, not a newly proved equivalence to all of Lean.

The unchanged `modules/receipt/src/relation.rs::check_bound`:

- binds every parent to the same I, foundation and policy;
- verifies the selected group openings and committed body interpretations;
- reconstructs the selected imported environment and checks every local
  declaration with `check_module_extension_conditional`;
- requires the child's rank to be exactly one greater than the greatest parent
  rank, or zero with no parents; and
- returns the exact child J and every exact parent J used as a premise.

The unchanged `modules/receipt/src/main.rs` calls
`env::verify(conclusion.journal.image, parent)` for **every** returned parent,
then commits the exact child journal. Final application verification must pin
the actual adopted I, require the journal's I to match and discharge all
recursive assumptions in non-development mode.

Assuming the adopted recursive multi-premise certificate system is sound and
the conditional checking interpretation is correct, induction on strict rank
gives:

1. A rank-zero accepted I receipt establishes `Valid(J)` from the adopted
   foundation and the checked local declarations.
2. At positive rank, actual I receipts establish all exact parent premises.
   The conditional relation then establishes the child extension.
3. Consequently a fresh receiver needs the child's I receipt and selected
   interfaces/semantics, not the parents' theorem-proof witnesses or their
   certificates merely to establish the child's mathematical validity.

Semantic imports may still name other modules. Resolving genuinely demanded
types, definitions, recursor rules or conversion dependencies can require their
authenticated interfaces/bodies and further warrants. The argument removes
mandatory **proof-ancestry replay**, not semantic dependencies, communication,
cryptographic assumptions or service costs. It is the current supported Lean
semantic envelope, not unrestricted Lean or hostile-source execution.

The relation supports branching directly. Receipt count, parent count, ranks,
semantic material, source and execution bounds remain finite. No global root,
consensus, popularity judgment, natural-language interpretation or new trust
policy is introduced by this alternative.

## Why A is useful but not logically mandatory

| Publication shape | Existing I possibility | What A additionally supplies |
|---|---|---|
| A new module imports only already I-certified modules | Certify its local declarations once; direct parent receipts suffice | Optional batching with other modules |
| Many new declarations are developed as one coherent module | The authoring API accepts multiple roots and exports their local dependency closure; one certificate covers the module | No inherent requirement for A merely because there are many theorems |
| Existing native chain or DAG must retain every exact module and journal identity | Certify every needed unsealed node in topological order, then certify the target | Certify the whole bounded DAG in one application seal without separate intermediate I certificates |
| Existing parent is available only as an A-member | Current I guest cannot treat that A receipt as an I receipt | Existing A-aware aggregation/reuse supports this case |

The third row is the major difference. A source-level repackaging of several
already published modules into a new combined module changes owner-qualified
references and generally changes ModuleIDs. It may be a useful new contribution,
but it is not exact frontier replacement. Never rewrite journals/ranks or call
the repackage the original mathematical object to claim a saving.

Current I permits only same-I parents. Building a faster I' changes executable
identity; the same-I rule then prevents importing old I as if it were I'. The
multi-image semantic-adoption problem in
[NEXT-AGGREGATE-COST-DECISION](../v5-2026-10-12/NEXT-AGGREGATE-COST-DECISION.md)
applies here too. Therefore optimized aggregate code cannot simply be called a
faster old-I producer. That would require a separately justified new profile.

## Existing source hooks and the genuinely missing seams

The direct-I mathematics is not a missing checker implementation:

| Existing source | Reusable behavior |
|---|---|
| `authoring/source.py::SourceOperation` | Owner-source and roots binding; supervised frontend export converted to an untrusted child input |
| `authoring/imports.py::ImportSession.make_request` | Exact selected parent journals, group openings, bodies and actual I receipt bytes; no ancestral theorem proofs |
| `preparation/owner.py::OwnerPreparation.snapshot` | Parent-aware I preparation and execution; derives expected exact J and a producer session |
| `production/producer.py` | Existing segment/lift/join/resolve/finish graph, finite accounting and genuine final application receipt |
| `client/workspace_atomic.py::admit_receipt` | Actual I admission; the existing context path accepts the resulting same-client I warrant |
| `mixed_claims/authoring_atomic.py::MixedSourceOperation.finish` | Ordinary authoring already emits the exact V2 native witnesses, with current I, semantic spec, parents and rank |

The current ordinary `client.author` deliberately returns mixed native evidence,
not an I producer request. Two seams remain for an **immutable-native-packet to
the current unified ordinary facade** integration. They are not logically
necessary for every direct-I workflow: the older `SourceOperation` pipeline
already reached real parent-aware preparation, and the lower-level
`LocatedReceiptWorkflow` already exposes pure-I remote receipt admission.
There is no missing pure-I checking or transport protocol to reinvent.

1. **Exact witness to I-producer handoff.** From the immutable authored mixed
   packet and an exact selected target J, parse with the existing grammar and
   `aggregate_image=None`. Select its backward closure and the unchanged native
   witness bytes. For each selected node require a genuine I receipt for every
   exact direct parent before preparing that node. Native parents not yet sealed
   become explicit preceding work, never fabricated assumptions. A minimal
   first implementation should return `NEEDS_I_PARENT` rather than autonomously
   launch a chain of new proof jobs. Preserve original I, rank, ModuleID, local
   groups, bodies and parent Js; bind the actual final receipt back to the same J.
   Untrusted wire preparation need not invent a saved live authority token.

   `OwnerPreparation._child` currently also requires a source-specific result
   schema including source/roots/selection metadata. A packet-only sealer must
   not fabricate those values to pass it. Extract/reuse its structural checks
   through an explicitly selected packet-preparation entry, or use the existing
   reviewed host prepare/snapshot boundary with a new exact-input controller.
   Do not copy the mathematical export conversion or loosen the source gate.

2. **Ordinary discovery/publication of a pure I target.** The current atomic
   mixed grammar requires at least one delta. The newer evidence grammar's
   terminal form denotes an **A-member**, not an I receipt;
   `workspace_evidence.export_evidence` explicitly rejects an I warrant. A pure
   newly sealed I module is therefore not a zero-delta packet that the present
   ordinary facade already publishes. Lower-level `custody/receipt_store.py`,
   `transport/http_provider_receipts.py`, `transport/receipt_client.py` and
   `transport/located_receipts.py` provide an existing receipt transport route.
   An ordinary facade could expose that route, or a fresh explicitly tagged
   terminal-I evidence form could reuse the current store/transport lifecycle.
   Bind exact J/summary/profile/receipt and unchanged semantic custody; require
   the real I owner for admission. Do not create a dummy A owner or use a new
   theorem wrapper just to make a nonempty mixed packet.

These seams are independent of new mathematics and do not require a new A
receipt. The second could be validated on the retained genuine I artifact if
selected, but it is not evidence of a **new** advancing frontier. Root should
select it only as part of a useful direct-I production/distribution choice, not
as another detached transport exercise.

## The growth conclusion does not wait for a new inequality

The existing three-route comparison remains decisive: independently optimized
local development L, ordinary optimized decentralized library sharing O, and
certified reuse V. A method-sharing gain against L is not a certificate gain
against O; O can distribute the identical parametric method and optimize/cache
its uses equally.

For the retained tiny workload, there is no supported positive full-cost
O-to-V margin. The real zero-assumption native membership component cost
1.3125 known whole CPU seconds / 1.5337696 wall seconds. It did not implement
the entire semantic-READY/authoring endpoint. The current base witness is
91,311 bytes and the raw I receipt is 223,594 bytes before packet encoding.
Those facts constrain claims; they do not settle a matched whole-route cost.
Recent semantic-reader whole-workflow timings cannot be compared directly with
that native-only component as if they delivered the same endpoint.

Source factoring can cancel common mathematical algorithms **in an explicitly
declared operation-cost model**. It cannot equate actual lifecycle, custody,
transfer, cache state or controller costs of two unimplemented matching paths.
The ordinary route may obtain semantics directly from its complete witness;
forcing it to make the certified route's separate body requests would handicap
the comparator. Therefore no positive marginal bound follows just by subtracting
the currently recorded timers, and no new native semantic-context utility should
be built solely to manufacture that subtraction.

For an implemented, full-cost beneficial frontier, the precise missing inputs
remain:

- a justified **positive lower bound on the matched per-eligible-use saving**
  after acquisition, validation, semantic-use, controller, variable service and
  failed-search costs, against both relevant optimized alternatives;
- a **finite successful production and maintenance upper bound** for the
  chosen new I or A frontier, including assumptions, completion, failures and
  useful supported lifetime, not just an attempt timeout;
- enough genuinely otherwise-uncached useful uses within that finite lifetime
  and sustainable producer/provider capacity for the already established
  break-even threshold to be feasible.

The thresholds already proved in
[GROWTH-CRITICAL-PATH](../v5-2026-10-16/GROWTH-CRITICAL-PATH.md) and
[SELECTIVE-CERTIFICATION-POLICY](../v5-2026-10-17/SELECTIVE-CERTIFICATION-POLICY.md)
are rigorous sufficient conditions. They establish a nonempty **conditional
architectural region** where their premises hold. They do not provide the
missing positive margin or successful-seal price for today's implementation.
No additional generic inequality changes that distinction.

## Useful progress that needs neither a new I nor a new A

A retained certified parametric method may support many independent, substantive
applications with short proofs rooted directly at that method. If each selected
application has bounded witness and demanded semantics, each can use the current
I-plus-native-delta route with a bound independent of the number of other
applications in the corpus. The reasoning is by direct dependency shape, not by
counting peer identities or declaring a usage counter to be knowledge.

This provides a real capability family and a route to practical useful growth
without certifying every instance. Its bound still depends on each application's
parameters, proof and semantic demands. It is not universal compression: an
arbitrary novel chain may lack a short direct derivation from that fixed method.
Replacing the chain by recursively nested method applications can merely move
its length into the new witness; calling that witness a template does not remove
the work. The optimized ordinary library can also use the same method.

Thus improving access to, and independent mathematical use of, the existing
method library is not blocked by A. **Generally advancing cold frontiers is
still blocked on an actually successful supported seal supply path.** Removing
A from that path does not remove the need for succinct certification, another
proved shorter witness, or an explicitly different trust model. Saved native
success, signatures, popularity, partial spot checks and proof hashes alone do
not meet the present acceptance requirement.

## Root action recommendation

Finish the already selected connected ordinary-software boundary. Then choose
between two central frontier actions using the existing evidence, not RAM probes:

1. Retain the current A route if retrospective exact-DAG batching is the needed
   capability. Its complete 113-segment capsule and 340-call graph are already
   available; do not re-execute it. The unresolved task is a supported successful
   production route and complete cost decision, not another receiver replay.
2. Select direct-I source integration only if coherent module-sized publication
   and same-I parents suffice for the intended deployment path. First bind the
   exact-witness handoff and terminal-I public interface above. Treat its prior
   failed child execution as negative evidence; it needs a cause-supported
   production decision before any genuine frontier-advance claim or proof job.

Do not implement both merely to keep agents occupied. A pure source plan for
the existing exact native packet can resolve direct-I eligibility without
running a prover: report which direct parents lack I receipts and how many
intermediate seals the choice entails. If that count/cost structure already
dominates the supported A route, stop the alternative before building it.

The highest-payoff question after ordinary integration is now explicit:
**which actual certificate supply route can maintain useful frontiers within a
supported resource/service envelope?** Neither a completed helper nor this note
closes it. Public release, mathematical assurance and the full v5 goal remain
open; none is relabeled as satisfied.

## Follow-up: activate the typed-row acceptance audit, not a rewrite yet

Root subsequently asked whether the constructor/field and refinement audit in
[AFFORDABLE-FRONTIER-DECISION](../v5-2026-10-16/AFFORDABLE-FRONTIER-DECISION.md)
now has the highest source-work payoff. **Yes: select that finite source audit
now, before either new I proving or a typed-row implementation.** It attacks a
real repeated producer representation cost and can establish whether a narrow
implementation exists. It requires no RAM investigation or proof campaign.

The earlier note's failed-screen paragraph is historical: the later complete
113-segment A capsule supersedes absence of a complete execution. The proposed
audit is justified by avoidable representation and supply cost, not by claiming
the current image cannot execute. No sample-based whole-cost percentage or
prediction of reduced segment/proof count is available.

### Two newly isolated design hazards

1. **`OwnedExportRow` is not a lossless correspondence representation.** Native
   `ExportJsonVal::{Defn,Thm,Opaque}` omits `all`; Serde ignores that field, while
   `match_declaration` requires it and checks exact `all == [name]`. A refactor
   that first converts to only `OwnedExportRow` has lost information needed to
   reproduce old acceptance. Keep the correspondence-required field in the
   shared row or a private sidecar; do not delete that check. Native
   `IndInfo.is_reflexive` also remains needed by correspondence even though
   native `apply_row` does not use it in its resulting declaration.
2. **Reachability affects the accepted inner syntax domain.** Inventory creation
   checks outer row shape/index ordering for every row, but defers most level
   and expression payload checks until the row is visited from a selected
   declaration/type/body/proof. Native decoding/application still processes
   every row. Some valid but unused expression payloads can therefore have
   native-accepted positional/extra-field forms that reachable correspondence
   rejects. Requiring exact object fields for every typed expression would be
   a compatibility restriction, not an established equivalent optimization.

Neither hazard needs a new kernel. Both require an explicit row projection and
rejection-state design before implementation.

### Constructor census from the actual retained sources

This is the finite starting table, not a claim that every Serde corner case has
already been proved. The native enum has **27 variant tags**. All suffix rows
are still processed; unsupported rows cannot be ignored as dead data.

| Family / native tags | Native payload information to preserve | Correspondence/success restriction |
|---|---|---|
| `meta` | Lean/exporter/format version strings | Exact adopted foundation row, not arbitrary new metadata; native format check is `[3.1.0,3.2.0)` |
| `str`, `num` | `pre:u32`; string or `i:u32` | Lowercase `in`, exact two-key outer row, continuous name index; exact payload fields and backward prefix |
| `succ`, `param` | One `u32` | Lowercase `il`, continuous level index; reached successor is backward, reached parameter is in the ordered universe list |
| `max`, `imax` | Exactly two `u32`s | Same level index checks; both reached references backward |
| `bvar` | `u16` | Lowercase `ie`, continuous expression index; retain native width even though correspondence first reads an unsigned integer |
| `sort` | Level `u32` | Same expression index domain; reached level must satisfy correspondence |
| `const` | `name:u32`, `us:Vec<u32>` | Reached exact fields, at most 256 universes and exact owner/foundation reference interpretation |
| `app` | `fn:u32`, `arg:u32` | Reached exact fields and backward expression references |
| `lam`, `forallE` | `name/type/body:u32`; four-valued binder style | Reached exact fields, name bounds and backward type/body; preserve each binder style |
| `letE` | `name/type/value/body:u32`, `nondep:bool` | Reached exact fields and `nondep=false`; unused valid native `nondep=true` is not globally ruled out by this correspondence check |
| `proj` | `typeName/struct:u32`, `idx:usize` | Reached exact fields and canonical owner/reference interpretation; preserve actual target-width conversion |
| `natVal`, `strVal`, `mdata` | Decimal natural string, string, or expression+metadata | Always refused by this relation's native execution config or `mdata` panic, including unused rows; do not enable them |
| `axiom`, `quot` | Native declaration fields | Existing adopted foundation can contain its fixed records; cannot introduce these as new supported local declarations |
| `def`, `thm`, `opaque` | Native declaration fields **plus correspondence `all`** | Exact record census, safe flags, singleton `all`, universe order, type/body/proof correspondence; native hint `regular` is `u16` |
| `moduleImportDef`, `moduleImportOpaque`, `moduleImportTheorem` | Name/type/universe list; optional hint and exact 32-byte hash | Only genuinely imported roles; exact field sets and commitments, no synthetic proof authority |
| `inductive` | Ordered `types/ctors/recs` vectors and all nested metadata/rules | Complete atomic group and exact census; retain all `all/ctors/isRec/isReflexive/k` metadata and each `u16` count/rule field |

The outer `BackRef` enum accepts aliases such as `In`, but successful
correspondence requires literal lowercase `in/il/ie` and exact row shapes; native
aliases alone do not imply an accepted relation input. Conversely, the old
`decode_corresponded_owned_row` explicitly falls back to the general decoder for
positional payloads, so that branch cannot simply be erased. The acceptance
table must describe the **intersection** of strict JSON, correspondence and
native application, not the union of their individually supported formats.

### Recommended extraction/refinement boundary

Keep the existing kernel-facing `parse_owned_rows` / `apply_row` / finalization
semantics. Introduce a private shared row representation that retains all native
fields **and** the extra correspondence observations above. Give correspondence
immutable typed views. Only after it succeeds may the same row's native portion
be consumed by `parse_owned_rows`; no full conversion back to generic `Value`.

For exact-domain compatibility, retain shape/extra-field information or a
carefully bounded legacy-row fallback for exceptional accepted payload forms.
Do not claim that a typed enum with `deny_unknown_fields` automatically preserves
the old domain. A fallback is acceptable only if common supported rows really
avoid generic row maps/redecoding; falling back for every row defeats the stated
intervention. The chosen decoder must preserve duplicate-key detection, strict
integer-only JSON, exact EOF, UTF-8 and original virtual node/depth census for
every field, including ignored native fields.

`foundation_static::matches_rows` currently performs exact recursive comparison
against generic Values, including metadata and otherwise ignored fields. Two
bounded choices exist: preserve the fixed 413-row prefix in its old form for an
initial typed-suffix implementation, or prove an exact static-value-to-typed-row
comparison including all fields. The first has lower assurance scope but saves
no generic-prefix work; the second is part of the refinement, not a free hash
substitution. Root should choose one explicitly after the table, not silently
weaken the exact foundation check. For the retained two-delta row census, keeping
both fixed prefixes would leave 1,538 of 2,364 rows as possible typed suffix
rows; that is a count, not a cost fraction.

The audit's deliverable should be one exact acceptance table plus these four
obligations, discharged or marked with the specific counterexample/blocker:

1. Strict decoder/projection and virtual-census equality on the selected domain.
2. Correspondence observation, canonical output and logical-work/depth equality,
   including reachable versus unused rows and the current syntax memo behavior.
3. Equality of each consumed native record and unchanged ordered application,
   including ignored native fields that remain correspondence-significant.
4. Same exact J and parent-premise list through unchanged commitments, conditional
   checking and aggregate graph; no change to actual recursive verification.

Stop before implementation if retaining these observations requires rebuilding
all generic row Values, if the accepted/refused domain remains ambiguous, or if
the change spreads into kernel/commitment semantics. Otherwise root can price a
specific source change and differential boundary test. Actual cycle/segment/
proof-cost evidence would remain a later single decision-changing measurement,
not an automatically launched campaign. The present source audit is worthwhile
because it can accept or reject the design before that expense.
