# A deployable operating envelope for proof reuse and huge-network discovery

2026-10-06 UTC. Author: `/root/scale_economics_v4`. Theory/source checkpoint;
no test, proof, installation, peer service or product mutation was run here.
This is a new design proposal, not a claim that the proposed fragment lane is
already shipped or accepted. Used predecessors remain frozen.

## Decision and relation to earlier work

The old v4 model already separates proof history, selected semantics, discovery,
availability and usefulness. Repeating its break-even identity does not make
expensive mandatory certification operable. The consequential change proposed
here is **bounded proof fragments between certified cut points**:

1. Keep the existing genuine succinct-certificate lane for cheap cold reliance
   independent of proof ancestry.
2. Let an independent receiver check one bounded, inert proof fragment against
   an explicitly supplied frontier of genuine certified parents by executing
   the same adopted checker relation locally, without producing another SNARK.
3. To reuse an unsealed result, inline its proof into the next bounded fragment;
   never promote a local execution flag to a transferable axiom. The next
   fragment's external Prop parents must again all have genuine certificates.
4. Seal selected fragments when demand or fragment-size pressure justifies
   paying for a portable certificate. Saturated bounds cause explicit refusal
   or optional sealing, not automatic recursive history hydration.

This creates a genuine alternative to certifying every research increment.
It is not a change to what counts as a valid theorem, and it does not promise
that every theorem can be cheaply received on every device. A receiver which
accepts only succinct receipts can continue to refuse fragments.

The second selected direction is workload-aware, **scoped** discovery: exact
IDs/types and selective structural features; bounded candidate enumeration;
explicit incomplete coverage; paid distributed index maintenance. Huge total
corpus size is compatible with bounded local work only under locality and
capacity conditions, not by announcing a larger catalog limit.

## What the actual source already supplies

Inspected source paths are relative to the canonical project root:

- `experiments/certified-foundation-restore-01/project/host.rs`
- `.../guest/src/main.rs`, `relation.rs`, `journal.rs`
- `.../companion/cert_workflow.py`, `cert_capsule.py`
- `.../native/ImportTail.lean`, `SealedInterfaceSupport.lean`
- `product-local/certified-typed-directory-source-07/cert_index.py`
- the same directory's `CERTIFIED-NETWORK-API.md`

The `host.rs` command is already:

```text
execute IMAGE INPUT EXPECTED_JOURNAL CYCLES PO2 [REAL_FINAL_PARENTS...]
```

Before execution it computes the image ID; validates the exact framed header,
packet length/hash, child journal, profile tag, output targets and ranks;
independently verifies every supplied parent receipt; matches each receipt's
full journal to exactly one selected header journal; and rejects duplicates,
unselected parents and missing parents. `checked_receipt` requires real succinct
receipts, the selected hash suite and a verifier context with dev mode disabled.
The process also refuses a `RISC0_DEV_MODE` environment variable.

It executes the image using the SDK, requires `Halted(0)`, requires byte-exact
output journal equality and bounds cycles/segment count. The exact guest calls
`relation::check` on the header and inert packet, verifies each header-parent
assumption, then commits that relation's journal. The source is not a native
success-bit oracle. No remote Lean source, tactic or arbitrary plugin must be
executed to check a received fragment.

Current hard ceilings include a 4 MiB packet, 16 KiB header, up to eight parent
collections, up to 64 MiB per receipt and 512 MiB aggregate read material,
128 segments and a caller-selected finite cycle ceiling. These are ceilings,
not an affordable default or measured fragment performance. A facade must
select materially smaller finite limits when appropriate and supervise memory,
CPU, wall time and output space separately.

**Missing acceptance bindings:** `execute` computes an image ID from its IMAGE
argument; it does not itself compare that image with an independently adopted
local profile. A safe receiver must pin the ELF, host/checker/runtime profile,
foundation and expected image, bind selected capsule/member/full journal,
and authenticate the exact executed inputs. The printed execution marker is
only a local observation, never a peer-asserted proof. Current code explicitly
labels execution `EXECUTED_ONLY_NOT_A_CERTIFICATE`; that label remains correct.

The execute branch does not perform the stage branch's explicit actual-assumption
census. For the exact inspected image, independent verification of the exact
header-parent set plus execution of that image supplies the logical premise
discharge: there is no additional accepted Prop-axiom source in the relation.
This argument depends on exact image/source correspondence. Mirroring the census
would be useful defense in depth if the SDK exposes the needed execution data;
it is not permission to accept an arbitrary guest with unchecked assumptions.

## Local acceptance theorem for one fragment

Let `F` be the adopted foundation, `R` the adopted exact relation, `I` the pinned
guest image implementing it and `V` the adopted certificate verifier. A fragment
contains one inert proof packet `p`, a header, a full expected journal `j`, a
selected output capsule `c` and an explicitly bounded set of certified parent
bundles. No parent may be another raw fragment in the receiving contract.

Assume:

- soundness of `R` relative to the intended supported Lean fragment and `F`;
- faithful local execution of the pinned image and faithful local binding/parser
  code (including compiler/runtime/host integrity);
- genuine certificate soundness and exact interface binding for all selected
  parent receipts, with decreasing certified ranks;
- actual successful local execution, exact output-journal/capsule binding and
  complete discharge of the relation's external Prop premises.

Then the output interface is derivable from `F`. Proof: every external Prop
premise is derivable under the certificate assumptions; `R` checks the displayed
delta relative to those premises and actual semantic definitions; substituting
the parent derivations establishes derivability from `F`. No ancestor proof
body must be materialized for this logical substitution argument.

This is **conditional mathematical assurance**, not proof of Lean correspondence
or foundational consistency. It is not the same assurance mechanism as accepting
a child succinct receipt: local execution trusts the local executor to run `I`
faithfully, while succinct acceptance relies on the child cryptographic verifier
and proof-system soundness. The parent cryptographic assumptions are shared.
An operator can explicitly adopt a policy permitting both routes; a comparison
then concerns equal accepted mathematical endpoints under that common policy,
not identical proof objects or identical trusted computing bases.

The locally persisted outcome should say, for example,
`LOCAL_EXECUTION_VERIFIED_NOT_TRANSFERABLE`, with exact input/profile hashes.
A copied outcome file never lets a different trust domain skip its own execution.
A locally checked fragment is not a `BundleV3` receipt and cannot be inserted
into the existing certified-parent API by substituting a status JSON.

## The essential composition seam: checking alone is not accumulation

The existing contributor `prepare` only consumes genuine receipt bundles.
Its native importer loads Prop interfaces body-free; it rejects unexpected proof
constants and unused selected parents. The guest permits only one or two selected
theorem outputs, forbids cross-output references and refuses extra helper theorem
declarations. Therefore a newly checked raw fragment cannot simply be named as
the next certified parent. Shipping only a local fragment checker would not
close reciprocal accumulation.

The smallest compatible extension is **proof-term substitution before checking**.
It does not change the guest relation/image or recertify existing parents:

1. Load one bounded received fragment as inert data. Authenticate exact capsule,
   full packet/header/journal and genuine certified frontier. A previous local
   check can be used only through a correctly bound local cache; foreign flags
   have no authority.
2. During local owner-controlled authoring, make its exact Prop interface visible
   as a *conditional* premise, along with directly used certified interfaces.
   The native authoring result is not accepted or published at this stage.
3. For every occurrence `const helper [u_1,...,u_k]` in the resulting proof,
   substitute the helper's closed proof value with simultaneous substitution of
   its ordered universe parameters by those levels. Its proof is closed in term
   variables, so no term-variable lift is needed merely because the occurrence
   is under a binder. Reject arity mismatch, free/metavariables or malformed data.
4. Combine exact foundation/semantic declarations and the selected certified
   frontier; reject name/body/profile conflicts. Remove the helper's temporary
   axiom and every dead declaration, retaining precisely the supported packet.
   Rebind names, levels and expression DAG indices without changing meanings.
5. Keep the originally requested output capsule/type exact. Compute the new
   packet hash and journal and choose rank from the remaining certified frontier,
   not from the removed helper's advertised rank. Run the unchanged guest and
   exact capsule/journal binding on the *whole composed packet*.

If composition is implemented incorrectly, the safe outcome is rejection. Its
correctness need not become an additional mathematical soundness assumption:
the final independently executed relation must check the exact requested output
against only certified external premises. This requires genuinely checking the
transformed packet, not trusting that the helper previously passed.

Universe-aware substitution must be simultaneous, not a textual name replacement.
Memoize instantiated bodies by exact helper identity and universe vector; preserve
DAG sharing and bound intermediate node creation as well as final serialized bytes.
An adversarial term can demand many different specializations or large expansion;
memoization does not prove all compositions small. Reject on the declared bound.

Current source-specific coupling matters: `ImportTail` and the workflow require
direct use of every imported parent. Certified grandparents appear only *after*
helper substitution, so they must not all be injected as allegedly directly used
native premises. Authoring needs the helper capsule plus the actually direct
premises; final transformation needs the union of certified frontier receipts and
all exact semantic data used by their types and the expanded proof. Check actual
use against that final union; do not waive premise-census validation.

The output capsule embeds definitions used by its type, not necessarily every
definition appearing only in its proof. Composition must therefore preserve the
proof packet's semantic support as well as the capsule. A type-only merge loses
required definitions. Definitions remain actual checked bodies, never axioms.

### Minimal prospective source/API changes

| Surface | Consequential change | Unchanged authority |
|---|---|---|
| New fragment codec/facade | Strict versioned inert framing, hashes/lengths, exact output capsule/journal, finite certified frontier, adopted-profile binding | Does not certify mathematics by parsing |
| New composition transformer | Bounded DAG merge, simultaneous universe instantiation, helper proof substitution, conflict/census checks | Final old guest rejects an invalid or mismatched proof |
| Fresh native/workflow successor | Explicit conditional raw-interface authoring and pre-guest composition; bypass neither receipt intake nor final relation checking | Owner source stays local; native success alone is not final acceptance |
| Local verify/export calls | Execute-only path and exact local result cache; export raw fragment distinctly from receipt bundle | Every new receiver rechecks; no `mark_verified` peer authority |
| Discovery/transfer adapter | Distinct object kind/namespace and bounded frame; exact IDs/type features from actual capsule | Existing BundleV3 framing must not be silently reinterpreted |
| Certification policy | Optional sealing of the *same exact endpoint* when worthwhile/needed; finite failure-aware budget | Existing genuine receipt production/verification remains required for sealed status |

Recommended order: codec and transformation with decisive hostile tests; exact
local execute/reuse/compose/recheck path; then bounded transport. A local-only
checker without reciprocal composition or a new network lane with mocked
checking would not qualify this architectural change. No used source is editable
under this document; root must select a fresh successor explicitly.

## Cost and locality guarantees that can actually be stated

Let `N` be total corpus size, `H` all ancestral proof work, `P` fragment bytes,
`D` selected semantic bytes, `J` total immediate-parent journal/receipt bytes,
`k` selected certified parents and `T_R(P,D)` actual delta checking work.

For a cold fragment reader, the required local work has the form

```text
read/hash(P + D + J) + sum(parent_certificate_verify)
  + execute_R(P,D) + exact output binding.
```

There is no required `N` scan or `H`-sized download. There is an explicit cost
for the uncertified proof fragment. The receive limit fixes `P,D,J,k` and cycles,
so continued unsealed growth eventually refuses or needs a new certified cut.
This is a bounded-fragment guarantee, not an ancestry-independent receipt for
every intermediate result. Receipt-only acceptance retains its original stronger
proof-compression property.

At fixed adopted profile, unrelated mathematical corpus growth does not increase
these variables. Selected statements/definitions can grow with the mathematics,
and demand for reduction may be intrinsically expensive. Reading arbitrary
selected semantic bytes costs at least their size; succinct certificates cannot
remove that lower bound. If a proof requires `k` independently selected facts,
their semantic identities must be bound, either explicitly or by another sound
authenticated aggregate interface. One small receipt cannot convey arbitrarily
large meaningful input for free.

The current seed production cost of 92,976.578125 known CPU seconds is evidence
that eager certification can dominate, not an estimate for an arbitrary future
fragment. A producer cannot assume every theorem will have enough cold reuse to
repay this investment. Grouping helps only when real shared work outweighs added
payload/fan-in/proof overhead; earlier typed-row regression refutes instruction
count as a sufficient performance model.

The companion growth mechanism may use a rent-versus-buy threshold: per-use raw
checking premium versus one sealing investment. Any competitive theorem must
state known actual premiums, fixed successful purchase cost, retention horizon,
common accepted endpoint/policy and no hidden migration/storage/maintenance cost.
Estimated demand or a quoted prover price gives a heuristic decision, not the
theorem's premises. Certification failures consume budget and do not produce an
amortization benefit. Do not equate a locally checked endpoint with a portable
certificate if the latter is required by the endpoint definition.

## Huge-network search: useful scope instead of impossible completeness

The actual index already has persistent `(namespace,key,sequence)` postings,
exact interface/bundle/type keys, bounded structural shape keys, finite scan/row/
byte/time bounds, immutable-cut cursors and zero bundle-blob reads during `find`.
Definition representatives use exact DefinitionID; proposition representatives
use a name-erased exact type heuristic. `type_diverse` is direct-query-only,
not routed. These are valuable existing mechanisms, not new v4 achievements.

For a local selected shard with `n_s` rows and `s` scanned candidates, B-tree
seek plus per-row lookups is conservatively `O((s+1) log n_s)` local index work,
plus actual parsed/replied bytes. A covering layout may improve the bound, but
source inspection alone should not claim it. `n_s` remains operator-bounded.

For `R` matching objects, complete enumeration requires at least `Omega(R)`
output work. A fixed-budget search cannot guarantee finding an adversarially
positioned useful result among arbitrarily many indistinguishable matches.
Even sound representative deduplication of exact types leaves infinitely many
different propositions or same-type definitions. Neither an LLM ranker nor
Bloom filter removes this information limit.

Thus the API should distinguish:

- exact object lookup: a supplied identity, bounded routing/holder alternatives;
- exact-type/structural retrieval: a declared key and finite candidate budget;
- exploratory retrieval: local heuristics/rankers, no global recall guarantee;
- complete enumeration: only a named finite covered cut, with the entire cost
  charged, and never a global-absence claim under partitions.

For hot keys, refine by additional structural/type/context facets before fanout.
If broad search still traverses `h` shards, charge `h`; a split balances storage
but does not make broad enumeration independent of `h`. A bounded sample or
representative view is allowed only with its actual sampling/selection scope
reported. Current first-sequence representatives have early-arrival bias; they
are not uniform samples or best-result ranking.

The smallest worthwhile search API additions are explicit object-kind filtering,
local capability/profile compatibility, a query-plan record naming key/refinement,
and end-to-end budget/coverage propagation for the fragment lane. Do not claim
that an exact-type key is supplied by magic: local agents may obtain candidate
types from their own formal context or use imperfect structural search. Research
strategy remains outside mathematical validity and no global task list is added.

## Capacity and availability are algebraic deployment conditions

Let object `i` have retained bytes `b_i`, holder replication `r_i`, advertisement
keys `d_i`, metadata bytes `a_i` and metadata replication `s_i`. Any retention
plan needs, ignoring overhead, total storage at least

```text
sum_i r_i*b_i + sum_i s_i*d_i*a_i.
```

If available capacity is lower, indefinite retention of every admitted object
is impossible. The protocol must admit a bounded active corpus, allow unindexed
or retired objects and make funded retention explicit. Mathematical validity
does not expire because a lease ends; availability does. No node needs a full
ledger, but the network cannot represent bytes that no participant retains.

Under a declared stationary approximation, object arrival rate `lambda`, mean
replicated object bytes `E[r*b]` and expiry/retirement byte rate `delta`, occupied
storage has expected drift `lambda*E[r*b] - delta`. A sustainable fixed-capacity
regime needs nonpositive long-run drift or matching storage growth. This is a
resource balance, not a prediction that demand or useful mathematics is stationary.

For each service shard `v`, let refresh, query and publication arrival rates be
`lambda_{v,j}` and mean service work `E[C_{v,j}]`. A necessary utilization condition
is `sum_j lambda_{v,j} E[C_{v,j}] <= capacity_v`. We choose strict inequality
with headroom as the robust operating requirement, not a universal necessary
condition (a deterministic exactly saturated server can remain bounded). The inequality alone
does not bound latency under arbitrary bursts or heavy tails. Operators also
need bounded queues, admission control and rate ceilings. A huge network can
have a catastrophically overloaded hot key while global mean load looks low.

If each record is refreshed every `tau`, metadata renewal traffic is at least
proportional to `sum_i s_i*d_i / tau` logical record-refresh actions, before
failures and routing. Batching can reduce network/API call count, not eliminate
the per-record retention work.
To claim lease coverage, an actual scheduling/service bound must place renewal
before expiry with delay and clock-skew margin. Setting a TTL does not establish
that bound; overload should make discovery incomplete, not silently extend leases.

Replication must name a failure model. For independent holder availability
probabilities `p_j`, availability of at least one holder is `1-product_j(1-p_j)`. That
formula is invalid for correlated outages or Sybil-controlled replicas; in the
worst correlated case extra logical replicas add no protection. The earlier
quorum-intersection bound remains applicable to its named crash/omission sets,
not Byzantine completeness or independent physical placement.

The current source07 overlay has a fixed cooperative membership and one explicit
binary hot-key split. It is not a maintained arbitrary-size DHT. A mature DHT's
provider discovery, routing refresh, expiry and heterogeneous client/server roles
are preferable integration primitives to inventing global status gossip. The
already inspected libp2p Kademlia specification supports those primitives, not
interoperability of the current TLS/wire or a theorem about adversarial recall.
Finite same-machine tests cannot establish independent-host availability.

## Rejected shortcuts and concrete delivery boundary

- Do not certify every increment by default and then call cheap receipt checks
  whole-system efficiency. Allow bounded directly checked fragments and selective
  certified cut points, subject to the new implementation's actual qualification.
- Do not trust remote execute markers, local-result files, popularity, hash-only
  membership or provider reputation as mathematical proof.
- Do not publish a raw child as a certified parent. Composition must inline and
  recheck, or seal genuinely; receipt generation cannot be replaced by a label.
- Do not change the guest relation merely to allow helper declarations if a
  checked bounded transformation can preserve the deployed image and receipts.
- Do not expand limits, add a global ledger or perform full-roster status gossip
  as a substitute for selective indexing and capacity admission.
- Do not claim unconditional sustained/exponential useful growth. The mechanism
  permits cheaper resource-bounded reuse under explicit workload and service
  assumptions; the broader growth justification must identify actual capability
  gains and account for complementary prerequisites, costs and saturation.

A substantial v4 result would include a working composed fragment loop with
actual local execution and genuine frontier receipts, strict bad-proof/context/
resource refusals, an explicit local assurance profile, and bounded discover/
transfer/recheck behavior. Its theory can justify the absence of compulsory
ancestral replay and when selective sealing is rational. Repeated-split DHT
maintenance, arbitrary Lean correspondence, global Byzantine recall and
independent-host operation remain separate unsolved claims unless actually
implemented/justified. More checkpoint files alone do not close these gaps.

## Prior sources reused, not rediscovered

- `../v4-2026-10-02/CORE-MODEL.md`: exact certificates, maintained finite directory,
  selected-context locality, failed typed-row optimization and cost separation.
- `../v4-2026-10-02/PHILOSOPHY-OF-GROWTH.md`: resource-bounded capability, validity
  versus usefulness, no intention-dependent acceptance and no novelty oracle.
- `../v3-2026-09-27/SCALE-REQUIREMENTS.md`, `SCALE-DESIGN.md`,
  `SCALE-NETWORK-NEXT-DECISION.md`: recursive cut points, proof/data separation,
  bounded indexed discovery and explicit unfinished maintained routing.
- `../v4-2026-10-02/TYPED-INTEGRATION-SEAM.md`: exact type versus DefinitionID,
  typed discovery framing, and semantic-data versus receipt distinction.
- [libp2p Kademlia DHT specification](https://github.com/libp2p/specs/blob/master/kad-dht/README.md):
  primary-source inspection is recorded in the earlier CORE-MODEL; this checkpoint
  reuses that inspected conclusion and does not claim a fresh external review.
