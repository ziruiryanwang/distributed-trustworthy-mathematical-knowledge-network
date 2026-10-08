# Can succinct proofs make local checking substantially cheaper?

2026-09-24. Source13/v2 assessment answering the user's question. This is
read-only diagnosis and conceptual analysis, not a selected implementation,
new benchmark, change to the release, or claim of completed scalability.

## Answer

Current complete receiving admission is substantial for the small demonstrated
example. Succinct verification is a plausible major scaling tool, particularly
for many independent receivers and constrained clients. It is not established
as an economical or drop-in replacement for v2's complete check-and-reuse path.

The central distinction is **verifying a result's validity versus installing
usable mathematics into an agent's Lean environment**. Our project needs both.

This checkpoint reuses the existing cost/trust investigation rather than
rerunning its experiments. The follow-up adds explicit non-cryptographic
alternatives and an independent check of the numerical and reuse conclusions.

## What the existing measurements actually say

Read the preserved source13 continuation result, not the earlier source09
cost baseline. Root independently extracted these ordinary-operation records:

| Operation in the retained continuation | Wall seconds | Inclusive Job CPU seconds |
|---|---:|---:|
| A admits B's returned counting theorem | 33.3866865 | 32.96875 |
| B submits its revised counting theorem | 127.2798794 | 156.03125 |

Source: `experiments/auxiliary-frontend-01/continuation-01/RESULT.json`,
`steps` labels `producer-count-publishable-admit` and
`receiver-count-publishable-submit`. These are observed runs, not controlled
mean timings, minimum inherent verification costs, or generic per-theorem costs.
They include selected foundations/dependencies and workflow overhead.

The receiving admission's native stage consumed 7.609375 CPU seconds out of
32.96875 inclusive CPU seconds, approximately 23.08%. Its single selected-native
step covers a Job process tree, not isolated Lean kernel execution. The full
stage wall was 8.3368168 seconds; the recorded native step interval is about
7.9381 seconds. Startup, runtime loading, reconstruction, checking, descriptions
and output can be inside the native interval. The receipt's operating-system
`kernel_cpu_seconds` means Windows kernel time, **not Lean proof-kernel time**.

If only this native stage's measured child computation became free, with all
other work literally unchanged, the hypothetical CPU reduction would be only
23.08%, an approximately 1.30x speedup. This is an arithmetic counterfactual,
not a measured optimization or a bound on broader redesign. A suitably defined
succinct relation might also replace other validation computations; data
handling, actual materialization and subsequent source reuse still need analysis.

The complete 627.71875-CPU-second v2 campaign is not the cost of one proof
check. It includes preparation, multiple operations, contributions and a
retained failed publication. No cost is inferred from that aggregate alone.

See [cost evidence](COST-EVIDENCE.md) for detailed nested accounting, package
reader observations and exact evidence paths. Source observations in
[trust design](TRUST-DESIGN.md) explain the current native/reconstruction path.

## What a succinct certificate would mean

A prover would construct a compact cryptographic argument that the **exact
permitted acceptance relation** accepts the committed mathematical object and
its supported dependencies, under the selected foundation and policy, yielding
the committed checked interface. Receivers could verify that argument locally
instead of repeating all computation certified by that relation.

This is stronger than trusting a sender's signature and different from voting
on a blockchain. Any capable participant can generate the certificate; it need
not be a central server or an authority on mathematical truth. Zero knowledge
is optional: public mathematics chiefly needs verification compression, not
concealment of proof material.

Important conditions, detailed in TRUST-DESIGN.md:

- Bind checker/relation version, encoding, foundation, policy, exact objects,
  dependencies and output interfaces. A success bit from an arbitrary program
  is insufficient; so is a sound kernel run on an unrelated input plan.
- Ground dependencies in permitted foundations or already certified contexts.
  A hash of an arbitrary assumption set is not a certificate of its validity.
- Recursive certificates must compose with a grounded base and sound,
  well-founded dependency/transition rule. This does not require a global order
  on all mathematics or prohibit legitimate kernel-checked inductive groups.
- Preserve a usable artifact path. Certificate validity does not imply future
  data availability, and reading/verifying a downloaded object still costs work
  proportional to the data handled at the relevant boundary.
- Record the changed assurance basis: relation fidelity, cryptographic
  soundness, verifier implementation and any setup/VM/recursion assumptions
  supplement the existing foundation/checker assumptions.

The standard computational-soundness guarantee excludes efficient adversaries
producing accepting arguments for false relation instances, except with the
scheme's stated error probability and assumptions. It is not an unconditional
new Lean proof of an arbitrary mathematical proposition.

## Why active reuse is harder than light verification

In current v2, `admit` rebuilds/checks the selected context union; later
`submit` reconstructs its context again before authoring/canonical replay.
An unmodified Lean checker does not accept a SNARK receipt as the original
theorem's proof term. Merely accepting a certificate in the networking layer
does not provide the environment needed by the next contribution.

Possible future choices must therefore remain distinct:

- Light verification of exact certified claims: potentially large receiver
  savings without constructing a complete native environment.
- Current native contribution path: still fetch and reconstruct the required
  objects; a receipt alone may save little end-to-end work.
- Certificate-aware authenticated environment import: a serious possible
  design, requiring explicit semantics/byte binding and a new audited trust
  boundary; not silently treating imported assertions as axioms.
- Compact ordinary certificates for suitable domains: sometimes a smaller
  checker and a proper Lean soundness connection can avoid general SNARK cost.

Proof bodies may be unnecessary for some opaque uses; definitions and reduction
behavior can remain necessary. Keep original reusable mathematical artifacts
available rather than replacing the commons with disconnected validity badges.

This import issue is an engineering boundary to solve, not an impossibility
theorem against succinct verification. One could design a certificate-aware
loader or deferred native materialization, but neither exists in delivered v2.

## Non-cryptographic alternatives deserve equal attention

V2 already obtains the basic benefit of proof-carrying mathematics: a receiver
checks supplied formal evidence instead of searching for the proof again.
The additional opportunity is to make that evidence cheaper to check, and to
avoid repeating checks already established within the receiver's own trust
boundary. These are several distinct mechanisms, not one universal shortcut.

| Mechanism | Potential saving | Required qualification |
|---|---|---|
| Shared proof DAGs and named opaque lemmas | Avoid repeated proof subtrees; let later arguments refer to earlier results. | Exact sharing is not a proof of validity. The dependency must be checked or already locally accepted; v2 already has canonical sharing, so no new speedup is presumed. |
| Persistent, exact local checked environments | Avoid rebuilding/rechecking identical foundations and dependencies for every request. | Bind all semantically relevant inputs, checker, foundation and policy; prevent stale state and invalidation errors. This is not a succinct proof and is not trust transferable from a remote cache. |
| Specialized proof certificates | Replace a large search trace or expanded derivation with evidence suited to a smaller checker. | The certificate checker needs a Lean soundness connection; certificate size and checking cost are workload-dependent. Source13 compatibility is a further gate. |
| Verified computational reflection | Reuse one proved checker-correctness theorem across many instances. | Kernel evaluation of the instance can still be expensive; a short proof term does not imply small computation. |

For a specialized checker, the schematic interface is:

```text
check_sound : for every instance a and certificate c,
              check(a, c) = true implies P(a)
```

With a kernel-checked proof of `check_sound` and a supported Lean proof that
the particular check returns true, one obtains an ordinary Lean proof of
`P(a)`. This need not introduce cryptographic soundness assumptions. It also
does not permit trusting a solver's printed success flag. For example, an
UNSAT certificate can let a receiver check a solver's derivation without
repeating its search, but such certificates are not universally small, and
this example does not assert that v2 ships a general SAT adapter.

Three measures must remain separate: source-script length, elaborated proof
size, and checking cost. A tiny reflexivity proof may require substantial
definitional computation. An LLM may search for a simpler proof or useful
intermediate lemma, but its proposed replacement still needs ordinary checking.
There is no established generic deterministic compression method here that
makes every Lean proof both tiny and cheap to verify.

Cryptographic succinct arguments address a different case: even after these
improvements, the correct checker may have to do a large computation. A prover
can do additional work so that many other trust domains verify much less of
that computation. Neither route should be dismissed before comparing the
same end-to-end acceptance-and-reuse workload.

## Economics: one expensive production, many cheap verifications

For the same chosen consumer workflow, define comparable costs:

- `N`: independent receiving trust domains that would otherwise redo checking,
  after legitimate local caching; not raw agent count.
- `c`: complete relevant native cost per receiver.
- `P`: additional one-time succinct proving cost, including chosen amortized
  setup/engineering overhead when evaluating total deployment economics.
- `v`: succinct verification and public-input checking per receiver.
- `r`: remaining per-receiver data, materialization and reuse cost.

After canceling equal costs, compare `N*c` with `P + N*(v+r)`. Total savings
require `c > v+r` and `N > P/(c-v-r)`. All terms must use comparable resource
or monetary units; GPU time and CPU seconds are not automatically equivalent.

This formula is illustrative, not a v2 cost estimate. There is no measured `P`
or `v` for this exact relation. A small receiver can benefit even below global
break-even by shifting work to stronger provers; the total system can still
consume more resources. Prover concentration, waiting time, proof size, memory,
upgrade cost and loss of availability remain relevant to democratization.

## Recommendation

Take succinct certificates seriously as a possible scale mechanism, without
attributing all current latency to Lean or claiming that a small cryptographic
receipt solves native reuse. The next decision-changing comparison would be
an optimized exact native boundary versus a fixed-relation succinct prototype,
measuring both receiver-only acceptance and actual downstream contribution.
Profile/safe incremental reuse are proposals, not permission to remove current
fresh checks or alter frozen v2. No such experiment ran in this assessment.

The preferred next measurement separates package decoding/commitments,
environment construction, actual kernel checking, description/export and
supervision. Compare safe native reuse and an optional fixed-relation succinct
route against the same mathematical objects, including a subsequent genuine
contribution. Measuring only a succinct verifier would miss the central reuse
cost. Any proof-generation experiment should target a deterministic checking
relation, not attempt to certify the entire Windows/filesystem/process wrapper.

Reuse [the earlier SNARK assessment](../../SNARK-ASSESSMENT.md) for general
techniques, trust assumptions and existing research. Its historical policy
names are not shipped v2 mechanisms. Relevant prior work includes Laufer,
Ozdemir and Boneh, [zkPi: Proving Lean Theorems in Zero-Knowledge](https://doi.org/10.1145/3658644.3670322),
CCS 2024. This turn verified its title/authors/2024 publication metadata through
Crossref; no fresh reading or benchmark of that system is claimed, and no
compatibility with Lean 4.34.0 or source13 follows from the citation.

## Scope and checkpoint ownership

Root: this synthesis and independent extraction of the two operation totals
and native receipt totals. `succinct_cost_evidence`: cost note from retained
records. `succinct_trust_design`: source-informed correctness/import analysis.
All work used the canonical Trustworthy root after its guard. Product, sealed
release, guide and source14 files remain unchanged. No new benchmark, Lean run,
network service, implementation or external publication occurred.

The separate [independent review](INDEPENDENT-REVIEW.md) checks the retained
timing arithmetic and the active-Lean-reuse boundary. The extended
[trust-design note](TRUST-DESIGN.md) records the non-cryptographic alternatives.
