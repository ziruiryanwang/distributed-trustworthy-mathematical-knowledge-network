# Payoff audit: prove an ordinary reusable-library workflow, not another mechanism

2026-10-22. Independent source/read-only audit by `ordinary_payoff_audit`.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
No tests, builds, imports, proof production, runtime campaign or Git mutation
were performed. A subsequent explicit root assignment authorized the two
owner-authored mathematical source fixtures listed at the end. No runtime or
admission claim follows; neither fixture is claimed to have been compiled.

## Decision

The ordinary checked-library route is materially better aligned with real use
than mandatory certification. It is viable **in principle**, using existing Lean
checking and serialization primitives. It is not implemented end to end yet.
The next high-payoff deliverable is one normal-project reciprocal library use:

> An agent discovers an unfamiliar peer-only read-footprint method over the
> existing quotient-backed `Std.ExtHashMap`, independently admits its missing
> declarations, uses them through ordinary Lean names and named arguments,
> publishes a downstream snapshot-invariant theorem, closes its session, and
> later reuses the accepted mathematics without replaying the checked base.

The narrow new syntax component is justified by actual compatibility defects.
It becomes another rabbit hole if completing or polishing it displaces this
public workflow. The first useful question is not whether arbitrary Lean metadata
has a new serializer; it is whether ordinary existing mathematics and a small
new reusable method can cross this safe boundary at acceptable total cost.

## Decision-changing finding: do not invent an already existing update-log library

The initially suggested insertion-log fold and no-touch lemma already have
direct standard-library equivalents in the pinned Lean4.34.0 source:

| Source below `src/lean/Std/Data/ExtHashMap/` | Existing functionality |
|---|---|
| `Basic.lean:238` | `insertMany`, including the `List (α × β)` instance. |
| `Lemmas.lean:743` | `insertMany_cons`. |
| `Lemmas.lean:748` | `insertMany_append`. |
| `Lemmas.lean:756` | `insertMany_ind`, a reusable invariant induction principle. |
| `Lemmas.lean:785` | `getElem?_insertMany_list_of_contains_eq_false`: a log not containing a key preserves its lookup. |
| `Lemmas.lean:797` | `getElem?_insertMany_list`: the complete last-write-wins lookup formula. |

Renaming `insertMany` as `run`, reproving its append/no-touch laws, then counting
the result as new useful growth would be a misleading experiment. Both candidate
and ordinary-package baseline must receive credit for these existing facts.
The quotient compatibility target remains useful, but it is not a novelty target.

Use `insertMany` directly. The small peer contribution should be an explicit
application abstraction above it. No new inductive command datatype is needed
for the first integration. Cold onboarding still needs the actual existing
library's inductive/recursor groups; this simplification does not remove that
acceptance obligation.

## Exact proposed reusable-method endpoint

Fix the ordinary instances `[BEq α] [Hashable α] [EquivBEq α]` and
`[LawfulHashable α]`. Write `Map := Std.ExtHashMap α β`. All definitions below
are mathematical specifications, with final Lean source spelling left to the
implementing author. They are not claims of mathematical novelty.

Contributor A supplies two ordinary definitions:

```text
ReadsOnly (R : α → Prop) (F : Map → γ) :=
  ∀ m n, (∀ k, R k → m[k]? = n[k]?) → F m = F n

Avoids (R : α → Prop) (writes : List (α × β)) :=
  ∀ k, R k → (writes.map Prod.fst).contains k = false
```

Its theorem is:

```text
ReadsOnly R F → Avoids R writes →
  F (m.insertMany writes) = F m
```

This is a read-footprint frame rule: updates outside an observation's footprint
do not change that observation. The proof is direct and theoretically settled:
for each `k` satisfying `R`, apply the existing Std no-touch theorem, then use
`ReadsOnly`. No new prover or experimental search is needed to establish that
the intended statement is plausible. Actual export/admission is still necessary
to establish implementation compatibility.

The abstraction is useful precisely because `F` is arbitrary: it can be a
multi-key read, a summary, or a decision procedure over selected lookups.
The admissibility premise is explicit. The system does not infer a footprint
from an untrusted annotation and never assumes an arbitrary program respects it.

Receiver B must not receive A's theorem identifier or proof in its task prompt.
Its local objective is snapshot-invariant preservation. Define:

```text
snapshot (ks : List α) (m : Map) := ks.map (fun k => m[k]?)

applyBatches (m : Map) (batches : List (List (α × β))) :=
  batches.foldl (fun state writes => state.insertMany writes) m
```

B contributes the general downstream theorem:

```text
(∀ writes ∈ batches, ∀ k ∈ ks,
    (writes.map Prod.fst).contains k = false) →
  (Q (snapshot ks (applyBatches m batches)) ↔ Q (snapshot ks m))
```

Here `Q : List (Option β) → Prop` is arbitrary. The result says a snapshot-based
property remains valid across any finite sequence of batches that avoids its
read keys. The proof uses A's method with `R k := k ∈ ks` and `F := snapshot ks`,
establishes the footprint by list-map congruence, and inducts over the batches.
It thus consumes both the acquired definition's meaning and the acquired theorem,
rather than merely mentioning A or wrapping its statement under another name.

This is a transparent interoperability/reuse workload. A strong local baseline
can derive it directly from Std, and an ordinary package can transmit A's method.
No claim of difficult discovery, worldwide novelty, or net growth advantage
follows merely because the reciprocal path works. If this method is already in
the selected local baseline under another API, retain it as compatibility only
and choose an actual missing client abstraction before a growth comparison.

## Smallest integration that decides architecture viability

Use a finite selected library closure and two separate owner states. Physical
hosts are unnecessary for this semantic discriminator; same-host operation must
not be described as independent-host deployment. A trusted local file transport
can exercise the inert public acquisition API initially. Existing networking
and provider-failure machinery should be connected afterward, not reimplemented
to make this first semantic boundary work.

| Step | Required observable result | Existing seam or minimal missing work |
|---|---|---|
| Select exact local context | Pinned kernel, initialized checked basis, supported axioms and ordinary dependency meanings are explicit. | Existing `BootstrapSupport.receiveSeed` is the checked basis candidate; root must bind its normalized projection, not pretend it is ordinary `Init.olean`. |
| Onboard selected Std closure once | Necessary types, values, native literals and generated groups check from the warranted base. | Existing closure traversal/group reconstruction patterns plus the new inert expression/declaration projection. Count actual constant dependencies, not all source imports. |
| A exports its method | Original names/levels/binder metadata survive, and missing proof/definition evidence is independently checked. | Ordinary exporter and checked extension adapter. The frontend's successful compilation confers no network authority. |
| B searches without A's ID | A bounded query over exact shared formal symbols returns A among candidates; its type/premises are inspectable. | Existing metadata-only search engine with a versioned ordinary-profile record/feature adapter; no new DHT or learned ranker is necessary. |
| B acquires and imports | Missing declarations check; exact shared dependencies match; normal named-argument use works in an owner project. | Isolated checker plus checked rebinding of only new declarations. Never co-import the internal basis snapshot with ordinary `Init`. |
| B produces its theorem | Actual accepted proof depends on A's definitions/theorem and preserves the stated full polymorphic endpoint. | Ordinary owner authoring followed by inert export and independent admission, not a certificate. |
| Close and reopen | A fresh operation restores committed local mathematics; already checked basis/method proofs are not rechecked. | Protected local snapshot plus accepted-root catalog; operational grants remain fresh. |
| A receives B's theorem | The independently checked return adds a genuinely new local capability and can itself be served as inert evidence. | Same acceptance/publication boundary; no private fixture injection or peer truth flag. |

Before the first end-to-end attempt, finish only the seams used by these rows.
For example, arbitrary peer elaborator extensions, automatic semantic conflict
translation, comprehensive attribute replication, cross-version Lean migration,
native compilation of imported executable code, and certificate bridges are not
prerequisites. If a necessary existing library group or native construct cannot
be represented, that is a central blocker; do not silently replace the workload
with an easier equality-only fixture.

The new syntax decoder should have focused refusal controls, but exhaustive
format polish is not the deliverable. A single failed altered-dependency case
and a corrupt committed-artifact case are high-value integration controls:
neither may become accepted mathematics through local matching or restore.
Further controls should follow concrete changed-boundary risk, not a reflexive
new campaign over frozen predecessors.

## Source-derived integration cautions

1. **A new discovery adapter alone is not automatically sufficient.**
   `discovery/module_export_adapter.py` is tied to the restricted expression
   format and ends with certificate-only resolution. Moreover
   `formal_features.py:142-177` validates only the two existing record schemas,
   with fixed module-export locator fields, while
   `discovery_store.py:59-60` accepts only two feature schemas. Reuse the actual
   posting/tree/query implementation, but select a small coherent versioned
   ordinary schema/validator/adapter seam. Do not impersonate a certified module
   locator or infer mathematical authority from feature validation.
2. **Avoid a full-world dependency binding on every use.** Bind exact dependency
   meanings once per accepted local context/extension and preserve that binding.
   Rehashing/re-exporting the entire owner project or compiler installation for
   each lemma application would reintroduce the dominant operational problem.
   New imports need checks; unchanged protected context may be reused.
3. **Warm reuse and cold interoperability are different costs.** The old basis
   contains 581 exports, not all Std. A selected map proof may pull in a material
   closure through values and generated groups. The source trace does not bound
   its declaration count or prove it fits an inherited 4096-declaration cap.
   A source-only closure census/export preflight should inform a finite runtime
   selection; do not discover the entire cost only after starting certification.
4. **Do not import unchecked snapshots.** `Lean.Replay.lean:59-60` shows the real
   checked constructor, and `:176` provides useful replay machinery. The supplied
   replay also admits arbitrary axioms, skips unsafe/partial constants and uses
   unbounded resource arguments. It is a source template, not the network policy.
   Snapshot loaders are valid only for locally authenticated checker-generated
   bytes under the stated local trust model.

These cautions do not require a new generic framework. They identify where the
small public path must not reuse an incompatible old policy by accident.

## Strong comparator and the benefit that can honestly be justified

There are three different comparisons:

1. **Existing local Std.** Both routes start with the same library, ordinary
   representation, caches, tactics and kernel. Existing lemmas are free shared
   background, not network-generated knowledge. The cold cost of independently
   establishing the selected basis is recorded separately and amortized only
   under an explicit number of subsequent uses.
2. **Ordinary peer/package sharing.** Give the comparator A's real package,
   ordinary incremental builds, the same exact dependency lock and caching.
   Do not charge it repeated proof construction or flattened ancestry. If its
   source can run arbitrary tactics/plugins, either account for the isolation
   needed to match our malicious-input boundary, or label the trust difference;
   do not quietly make one route strictly safer and call all extra cost waste.
3. **Independent local derivation.** This is a meaningful missing-knowledge
   comparator, but not a demonstrated lower bound on theorem-proving cost.
   A clever local agent may derive this elementary method cheaply. Synthetic
   delay, restricted tactics or withheld Std lemmas would invalidate the claim.

Let `L_i` be the cost of the best allowed baseline route to a fixed accepted
endpoint for user i, and `N_i` the receiver's network discovery, acquisition,
independent delta checking and owner-import cost. Let `P` be the one-time cost
of creating and exposing the reusable method and `S` its incremental custody,
index and failed-query service cost. A stated scalar resource measure yields
the conditional full-cost benefit criterion:

```text
sum_i (L_i - N_i) > P + S.
```

If ordinary package sharing already finds and installs the same method more
cheaply, this workload establishes no efficiency win over that baseline. The
commons still may offer independently checkable inert exchange, cross-provider
formal discovery and smaller dependency-selected imports, but those properties
must be demonstrated rather than assumed from the name “decentralized”.

The appropriate immediate acceptance bar is narrower and consequential:
**the real workflow is possible, ordinary library meanings survive it, and
recurring costs are attributable to the new work rather than replayed history.**
That is architecture viability, not final-v5 acceptance. Once this path exists,
growth work should target actual search/reuse workloads where the expected gap
`L_i - N_i` can be positive, with service cost and equally capable baselines.
There is no reason to pay for another generic certificate to learn this first.

## Simpler alternatives considered

- **Just exchange normal Lean source packages:** excellent baseline and useful
  optional owner-approved authoring route; not safe automatic hostile-peer
  acceptance, since source elaboration can execute code. An actual security
  sandbox or a policy trusting those packages is a different assurance route.
- **Just exchange `.olean`:** useful for protected local acceleration, not peer
  mathematical evidence. Hash identity does not establish checked provenance or
  make the binary importer a safe proof checker.
- **Just call upstream `replay`:** substantially reduces implementation effort,
  but its exact policy/limits still need adaptation; it does not supply inert
  hostile parsing, accepted-state persistence, ordinary-project matching or
  unknown-ID discovery by itself.
- **Trust installed Std automatically:** can be an explicitly owner-adopted
  trust profile, but does not satisfy the selected fully checked-native lane.
  Do not quietly substitute it when the initial closure is inconvenient.
- **Prove the entire environment once cryptographically:** retains a future
  service niche for strict cold onboarding; it is not the next highest-payoff
  discriminator and reintroduces the observed production bottleneck.

The selected inert exchange plus ordinary checked library is therefore a
reasonable smallest route under the stated soundness boundary. Its practical
advantage remains conditional on the end-to-end integration, not on more prose
or isolated codecs. Complete that path before expanding the architecture.

## Selected fixture source checkpoint

Root subsequently authorized source-only mathematical inputs under
`software/v5/ordinary_lean/examples/`:

- `ReadFootprint.lean`, SHA-256
  `d60d32a30d3c51988e68191f48bc7d16c9ecaa2ede074333c0c26fa4988d26a6`:
  producer definitions and the general footprint theorem, using the actual
  Std no-touch theorem with its original named parameters.
- `ReadFootprintConsumer.lean`, SHA-256
  `8857b2aae97e574aa1305ad0bb3546a04f168c73d334ad0ab1f64386ba077e97`:
  finite snapshot, batch fold, footprint proof, inductive preservation and
  arbitrary predicate preservation. It explicitly uses the producer theorem.

The consumer imports `examples.ReadFootprint`; later selected compilation must
use the ordinary-Lean source root as its module root and generate any build
outputs in root-selected fresh locations. Neither source has been compiled in
this assignment. Source spellings of `List.map_congr_left`,
`List.mem_cons_self`, `List.mem_cons_of_mem` and the Std lemma were inspected
in the pinned runtime. No `sorry`, new axiom, new datatype, executable peer
plugin or duplicated `insertMany` definition was added.

These two fixtures have a common author and therefore **cannot** by themselves
be used as evidence of successful unknown-ID discovery or independent-agent
problem solving. They fix the semantic endpoint and provide owned inputs for
checking the new integration boundary; a genuine agent-facing workflow remains
separate. Compilation success will likewise not establish inert round-trip,
independent admission, persistence, benefit or final release.
