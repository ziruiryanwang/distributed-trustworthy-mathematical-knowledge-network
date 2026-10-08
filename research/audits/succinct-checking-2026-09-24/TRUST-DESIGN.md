# Succinct checking: current-v2 trust-boundary delta

Date: 2026-09-24. Status: read-only source-informed proposal, not an implemented
or benchmarked acceptance mode. Scope: delivered v2/source13. The unfinished
source14 successor is not evaluated. No product code, tests, or services ran.

## Bottom line

Succinct proofs could make **repeated assurance that exact mathematical artifacts
passed an exact checker** much cheaper for receivers. They do not automatically
make those artifacts cheap to install in the Lean environment used to construct
the next contribution. This distinction is particularly important for v2,
whose central purpose is reciprocal production, not merely displaying a
verified-result badge.

Reuse the existing [SNARK assessment](../../SNARK-ASSESSMENT.md) for the general
relation, economics, and prior-work map. Its older policy/validator-cell labels
are conceptual history, not claims about implemented v2 APIs. This note adds
the current implementation boundary and avoids prescribing a proof system
before profiling.

## What v2 presently does

Source observations from the frozen
[API](../../../product-local/auxiliary-frontend-source-13/API.md),
[checking bridge](../../../product-local/auxiliary-frontend-source-13/py/checking.py),
and [native replay](../../../product-local/auxiliary-frontend-source-13/native/AgentReplayCore.lean):

- `admit` authenticates prior evidence/package bindings, forms the selected
  package union with the current context, and runs native `--describe`.
  Native `receive` reconstructs the seed and batch; `checkedAdd` explicitly
  calls `addDeclCore` with `doCheck := true`.
- `submit` reconstructs the context for owner-authorized source checking, then
  executes canonical native replay and inverse-export native replay. The bridge
  checks actual exported objects, selected references, foundation, and replay
  roots. Source checking alone is not the complete acceptance relation.
- The source frontend matches imported shared declarations to the checked
  inventory. The native replays reconstruct from the selected foundation, not
  from arbitrary externally supplied Lean imports.
- The received group's generated declarations and recursors have an exact
  inventory/correspondence check. An assertion that a group declaration was
  valid is narrower than the actual acceptance/binding obligation.

These are source facts, not a cost profile: CPU time in kernel checking,
serialization, hashing, process startup, foundation reconstruction, or source
elaboration cannot be inferred from the number of stages alone.

## A candidate cryptographic statement

Use a pinned deterministic acceptance relation `K`, not an informal statement
such as “Lean accepted this.” An illustrative public input is

`x = (relationID, checkerID, encodingID, foundationID, policyID,
      inputClosureRoot, priorContextRoot?, selectedReferences,
      outputContextRoot, outputInterfaceRoot)`.

These are design roles, not new v2 fields. Some can be transitively committed
by a single typed root; they need not all be duplicated on the wire.

The witness contains the exact canonical bytes and proof material needed by
`K`, and, for a recursive scheme, prerequisite certificates. The relation must
establish all of the following:

1. Canonical decoding, typed hash/commitment checks, root selection, dependency
   resolution, and policy checks apply to the objects actually used by `K`.
2. The foundation is the receiver's permitted foundation; new external axioms,
   unsafe declarations, and unsupported constructs are not silently admitted.
3. Native proof/type checking and generated-group inventory correspondence
   succeed for the selected complete dependency boundary.
4. The output declaration identities, formal types, bodies where relevant,
   and receiving interface match the committed input and actual checked output.

The receiver pins the proof-system/verifier parameters and relation, validates
`x` against its own requested object and policy, and locally checks the
cryptographic proof. Peer identity is not a substitute for any of these checks.

Proving only that an untrusted peer supplied a `true` status field, or that a
kernel accepted an arbitrary plan disconnected from the downloaded package,
would not preserve v2's acceptance guarantee. The canonical bridge's input and
output binding checks must either remain trusted local work or be included in
the proved relation. A filesystem/process receipt is not that relation.

Successful cryptographic verification establishes, under the selected scheme's
soundness assumptions, that a satisfying acceptance witness exists. It does
not necessarily establish that a particular peer historically ran the native
binary. No private witness requirement exists here: public, non-zero-knowledge
succinct verification may be sufficient.

## Context and recursion: the easily missed trap

There are two defensible relation shapes:

- **Closed object/closure certificate:** certify a complete supported dependency
  closure back to the permitted foundation. This is readily reusable across
  nodes; each receiver still checks that its selected union has compatible
  identities, policy, and interfaces.
- **Context-extension certificate:** certify `Γ -> Γ′` for exact committed
  contexts. The prior context must itself already have a valid basis under the
  receiver's policy. Merely putting the hash of an arbitrary environment into
  the public inputs does not prove that environment sound.

For recursion, every prerequisite certificate must bind its foundation,
policy, dependency identities, and interface to the next step. Require a
grounded base case and a well-founded composition rule (for example, strictly
decreasing dependency ranks or a proved append-only transition rule). Mutually
supporting receipts with no grounded base cannot certify each other. Supported
mutual inductive declarations remain one kernel-checked group; this is not a
ban on the legitimate recursion inside such a group.

There is no requirement that all nodes share one context, one recursive batch,
or one globally agreed ledger. Immutable certificates and locally selected
dependency closures suffice for the acceptance problem. One enormous global
aggregate may be inefficient when a consumer needs only a small subset.

## A receipt is not a Lean theorem body

An unchanged Lean kernel does not accept a SNARK/STARK receipt as a proof term
of the original proposition. For an active contributor, distinguish:

| Consumer path | What remains necessary |
|---|---|
| Check a result's validity without building on it in Lean | Verify the exact certificate and policy/statement bindings; source availability remains separate. |
| Use the original theorem/definition through unchanged native replay | Retrieve the required artifacts and construct the checked Lean environment; this can retain much of today's cost. |
| Bypass native replay using a certified environment image | Design and audit a new trusted import boundary binding exact image bytes and their semantics to the certificate; this changes the acceptance basis. |
| Use a compact domain-specific native certificate | Supply a certificate/checker whose result has an appropriate Lean proof connection; benchmark this distinct alternative. |

A future certificate-aware importer could be useful. However, replacing
`admit` with `Verify(receipt)` alone does not provide the context required by
the next `submit`, which currently reconstructs/checks it again. Treating a
received assertion as an axiom would evade rather than solve that problem.
Formalizing a cryptographic verifier inside Lean does not by itself turn its
computational soundness assumption into an unconditional Lean proof of the
underlying arbitrary theorem.

## Trust shift and availability

The assurance would be conditional on the original mathematical foundation
and checker, plus faithful relation encoding, proof-system soundness,
commitments, verifier implementation, and any setup assumptions. A zkVM adds
the relevant VM/ISA, guest compilation/image, memory, and syscall semantics;
it does not make arbitrary host I/O automatically trustworthy. Recursion adds
its own composition and soundness-accounting obligations.

The goal is less **repeated computation**, not fewer assumptions in every
dimension. Proving execution of a buggy or mismatched checker faithfully
certifies the wrong thing. Strong prover identity and blockchain consensus do
not repair that issue.

Keep native packages, definition bodies, dependency interfaces, and useful
proof material separately retrievable. A receipt is not storage, retention,
or future availability. Even a proof that the prover knew the package at one
time is not a promise that a future agent can fetch it. Definitions and
reduction data can be indispensable for further proof construction even when
the old theorem's proof checking is cryptographically compressed.

## Recommendation to the central agent

Answer “possibly significant, but unmeasured and not a drop-in replacement.”
Separate current whole-workflow cost from the replaceable checking component.
For the active-reuse case, charge any unavoidable materialization/import and
subsequent-submission cost to the succinct path, not only its tiny verifier.
For light receivers, check whether they genuinely avoid native imports and
artifact transfer. Count independent receiver trust domains, not raw agents
sharing one checked context/cache.

First determine whether repeated native reconstruction/checking is dominant
after simple safe reuse/caching opportunities. Then compare a frozen exact
relation on identical objects: native checking, a suitable specialized native
certificate if one exists, and a succinct prototype. Measure prover cost,
verifier cost, proof size, memory, full reuse cost, and cumulative fanout.
Existing literature establishes candidate techniques, not the economics or
compatibility of this particular v2 path. No SNARK integration, new import
authority, deployment, or whole-goal claim follows from this note.

## Optional extension: non-cryptographic succinctness and cheaper checking

The user's broader question also includes ordinary mathematical/computational
certificates, not just SNARKs. These alternatives often preserve the native
proof boundary more directly. They are proposals to evaluate, not newly
implemented v2 features.

| Alternative | What can become cheaper | What must still be checked |
|---|---|---|
| Shared expression/proof DAGs | Repeated representation, transfer, storage, and sometimes traversal | Exact decoding, references, typing, and reductions; sharing by itself is not a verification certificate. |
| Modular lemmas with opaque proof bodies | Later proofs reference a checked lemma rather than copying its proof; its proof need not be unfolded during ordinary use | Each prerequisite's proof must have a valid acceptance basis. Rebuilding a fresh v2 context can still recheck it. |
| Exact locally checked environment cache | Repeated foundation/context reconstruction and rechecking of unchanged declarations | Exact foundation/checker/policy/dependency identities, locally established acceptance, cache integrity, compatibility, and safe reuse across operations. |
| Specialized deterministic certificate and verified checker | Expensive search/computation can be replaced by cheaper certificate checking | A soundness theorem connecting the certificate check to the mathematical proposition, and a native proof of this certificate's successful check. |

### Proof compression is not a universal speed guarantee

V2 already exchanges shared expression DAGs and named declarations; that is a
useful starting point, not evidence that its entire checking pipeline memoizes
all shared work. Deduplicating the byte representation may not avoid repeated
kernel traversals or expensive definitional equality. Conversely, producing
a slightly longer proof with explicit intermediate lemmas can avoid a costly
computation and be cheaper to check.

An opaque theorem has its type available for later reasoning without unfolding
the proof body. This does not authorize deleting its proof before independent
validation, treating a remotely reported theorem as an axiom, or hiding a
definition body required for reduction. The existing code reconstructs and
checks selected declarations; modular source alone does not install a
persistent checked-environment cache.

### A native certificate can be much cheaper than finding the result

For a problem instance `a`, candidate certificate `c`, and deterministic
checker `check`, a Lean-level design can provide

`check_sound : check a c = true -> P a`.

The expensive producer searches for `c`. A receiver obtains a Lean proof of
`check a c = true` through permitted kernel-checked computation or ordinary
proof construction, and applies `check_sound`. The receiver need not repeat
the producer's search. The trusted logical boundary can remain the original
foundation and native checking, rather than add computational cryptographic
soundness assumptions.

Examples to investigate include arithmetic normalization certificates,
certified decision procedures, and proof traces for satisfiability/unsatisfiability
problems. A certificate family with a verified checker is the requirement;
no particular external format or Lean library is claimed to be integrated in
v2. An unchecked external solver saying `true` or a fast external evaluation
result does not meet this requirement.

The cost can still be poor: certificates can be enormous, `check` can perform
expensive reductions, and encoding the successful computation as a native
proof can undo an apparent savings. A short tactic script is not necessarily
a short elaborated proof; a short proof term is not necessarily cheap to
normalize. The certificate, checker, soundness theorem, and their dependency
closure must all fit v2's actual capture, native, index, and resource limits.

### Local cache reuse is different from trusting someone else's cache

The most direct architecture-level saving may be to avoid repeating checking
already completed by the same trusted local node. A proposed cache entry must
be keyed by the exact relevant artifact/context, foundation, checker, policy,
and dependency bindings, and must have protected locally established evidence.
An arbitrary peer's serialized environment or statement that it checked the
same hash is not such evidence. Cache invalidation, process isolation,
failure recovery, and safe extension become part of the implementation
contract; the current v2 does not already supply the proposed persistent
native-environment optimization merely because it retains historical receipts.

For this project, evaluate these non-cryptographic savings before committing
to a general succinct-cryptographic stack: first isolate repeated reconstruction
and checking, then examine local exact reuse; for computationally expensive
mathematics, compare native domain certificates and proof representation choices.
Cryptographic receipts remain a complementary option when many independent
receivers would still repeat a genuinely expensive check. None of these
techniques can universally promise tiny proofs or cheap verification for all
mathematics.
