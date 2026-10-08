# Scale is an acceptance-and-reuse requirement

2026-09-27. Root checkpoint after the user's explicit very-large-scale update.
This selects a redesign problem, not an implemented cryptographic capability.
The master goal remains active; the tentative v3 deadline remains03:00 Chicago
on2026-09-28. No used source, allocation or result is changed.

## What changed in priority

The network may contain an enormous mathematical corpus and extremely long
derivation histories, even if this machine only tests a small instance. A
receiver must not be required to acquire and replay the transitive proof bodies
of every lemma it uses. Increasing package/stage limits or reducing a constant
factor in full-closure replay cannot discharge this requirement.

Source16's completed local reader comparison saved27.1845%CPU under its fixed
finite gate. That result and its independent audit remain valid in their scope,
but do not justify the large-scale architecture. Root has held new installed/
growth campaigns while resolving the more central boundary. No pending consumer
experiment is reclassified as a scale experiment.

## Separate variables, rather than saying only “efficient”

For one contribution q let:

- N be the number/size of all network results, most irrelevant to q.
- H be the total size/checking work of q's ancestral proof bodies.
- I be the bytes of authenticated mathematical interfaces actually selected.
- D be definition/inductive/computational data actually needed for q's checking.
- p be q's new proof or local certificate and K(p;I,D) its own checking work.
- k be the number of directly selected authenticated premises.
- lambda be the security parameter of an explicitly selected proof system.

The redesign's primary target is a cold receiving path with no mandatory
linear term in N or H. Network-wide completeness is not a prerequisite for
accepting one exact result. A node's previously checked cache may improve the
warm path but cannot be the only answer: a new trust domain must have a compact
way to authenticate old lemmas.

For a selected succinct scheme, the target shape is:

    receive-and-authenticate(q)
      = read(selected interface bytes) + verify(certificate, bound inputs)
        + any bounded authenticated lookups

    contribute(p)
      = materialize selected I,D + K(p;I,D)
        + certify this new checking step and its certified premises

The first expression is independent of ancestral proof-body transfer. Its
certificate verification may be constant or polylogarithmic in the encoded
checking trace depending on the scheme; no numeric performance is assumed.
The second must not expand every parent's ancestral proof history merely to
generate the child's certificate. That requires compositional/recursive
certification, not just a monolithic SNARK of every closure from scratch.

These are scoped cost requirements, not a promise of constant-time mathematics.
Reading a large selected statement has a linear byte cost. A proof can invoke
expensive definitional reduction. Its genuinely necessary D or k can be large.
Searching for p and proving its cryptographic certificate can be expensive.
No mechanism can guarantee that every mathematical question has a cheap proof.

## Architectural direction selected for detailed review

Separate five objects that today's complete package/replay path conflates:

1. A mathematical interface: kind, universes, exact type, semantic identifiers,
   and commitments to relevant definitional/computational content.
2. A native proof/body artifact: retained/fetchable when needed for audit,
   alternate checking, learning, or computation, not mandatory theorem intake.
3. A transferable validity certificate: binds the exact interface, foundation,
   policy and permitted checking relation, including certified dependencies.
4. A local accepted-interface registry and Lean import boundary: certificate
   validity must make the lemma usable in later ordinary mathematical work.
5. Independent storage/discovery views: find and fetch selected certified data
   without assuming any index or holder is a truth authority.

The intended large-scale mode is certificate-backed sealed theorem reuse plus
selective authenticated definitions, with recursive proof-carrying composition.
The current native-replay mode remains a valuable independent route/fallback;
it is not silently relabeled as the scalable mode. The crypto backend and new
Lean import profile remain unselected until the design review identifies their
actual implementation and soundness obligations.

## Non-negotiable failure distinctions

- A signed assertion, majority vote, Merkle membership path or hash equality
  is not by itself evidence that a theorem follows from the selected foundation.
- A proof that some checker accepted something is insufficient unless the
  statement, environment, identities, policy and output interface all bind.
- Verifying one certificate cannot be followed by mandatory full historical
  replay in submit/export; that would move, not remove, the bottleneck.
- Loading certified premises as Lean axiom-shaped interface entries, if used,
  requires a separately enforced certificate registry and a composition theorem
  discharging every such premise. It is not permission to accept user axioms.
- Theorem erasure is not unconditional preservation of all Lean reductions.
  In particular the pinned Lean implementation documents proof-dependent
  unfolding cases. The sealed-interface profile must state its supported
  semantics and return a controlled sealed-profile refusal when appropriate.
  A need-for-body diagnostic never triggers implicit ancestral hydration;
  only a separately selected, separately charged transparent mode may fetch it.
- Certificate soundness does not imply source/body availability or permanence.
  Availability and acceptance must be separately represented, not inferred.
- A toy hash/signature or dummy verifier cannot qualify a succinct-proof mode.

## Reuse of previous investigation and deliberate supersession

The2026-09-24 succinct assessment already identified the exact acceptance
relation and the certificate-to-Lean reuse gap. Reuse that analysis rather
than issuing another generic “SNARKs might help” recommendation. The current
work must resolve a concrete boundary, message format, logical composition
argument, cost contract and first implementation discriminator.

Earlier P0 specifications deliberately excluded succinct acceptance and often
coupled public reusability to possession of the complete native witness closure.
Those remain historical/current-native-profile facts, not an architectural
prohibition for the newly requested scale mode. A new versioned assurance
profile must explicitly state the changed computational-soundness assumptions.
Do not weaken the old profile or retroactively upgrade its receipts.

The guarantee that a theorem can be safely *used as a lemma* must be separated
from the ability to inspect/replay its proof body. Body archival remains useful
for resilience and revalidation; mandatory body download on every use does not.
No global root task, central prover, canonical global environment, ledger or
political identity system is added by this redesign.

## Active disjoint work

- v3_efficiency: SCALE-CERTIFICATES.md, exact certificate relation/composition,
  backend tradeoffs, cryptographic/adversarial assumptions and costs.
- v3_index: SCALE-LEAN-INTERFACES.md, actual pinned Lean import/proof-erasure/
  conversion boundary and exact implementation seams.
- v3_growth: SCALE-DATAFLOW.md, selective hydration, availability, indexing,
  local views and whole-loop cost rather than a verifier-only benchmark.
- Root: synthesis, existing-research deduplication, source-grounded technology
  selection, cross-audit and a concrete next experiment. No implementation
  claim or new product edit is authorized merely by these design notes.

## Required new discriminator

Hold selected theorem interface and downstream task fixed while increasing
ancestral proof material and unrelated corpus size. A genuinely scalable cold
receiver must acquire neither full ancestral bodies nor a global corpus scan.
It must verify real certificates, use the exact lemma in a new Lean contribution,
and export a composable certificate without reconstructing the ancestry.
Report receiver bytes, CPU, memory, selected definition bytes, author/checker
cost, certificate generation cost/size, direct fan-in and failure behavior.
Local-cache-only, mock-certificate and full-history-prover experiments may be
useful partial discriminators but must never be labeled this completed gate.

No such new experiment has run. The existing source16 reader gate is not it.
