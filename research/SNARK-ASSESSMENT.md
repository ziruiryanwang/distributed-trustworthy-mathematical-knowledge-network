# SNARK and succinct-verification assessment

## 1. Decision

SNARKs, STARKs, zkVMs, recursive aggregation, and cryptographic proof-carrying data are **not on the P0 acceptance path**.

P0 uses receiver-local checking of native Lean artifacts or small domain-specific certificates. Succinct verification becomes useful only when measured verification fanout, constrained consumers, expensive native checking, or confidentiality outweigh its prover cost and enlarged trusted base.

The central distinction is:

> A succinct argument can remove trust that a remote operator executed an exact checker, but it cannot improve the checker's logic, implementation, formalization fidelity, or underlying mathematics.

It can faithfully attest satisfaction of a buggy encoded relation, subject to its declared computational-soundness error, and adds arithmetization/VM/compiler/setup/cryptographic assumptions. Verifier acceptance does not establish that native checker execution occurred. A second small independent checker or independently reconstructed formalization often improves trustworthiness more directly.

## 2. Exact relations

Let public input \(x\) bind a claim, logical environment, dependency root, checker profile/binary, and policy epoch; let \(w\) be a proof artifact.

Native replay checks:

\[
R_K(x,w)=
[\operatorname{DigestsMatch}(x,w)]
\land
[\operatorname{Run}(K,x,w)=\texttt{ACCEPT}].
\]

Given correct environment binding and checker soundness:

\[
R_K(x,w)=1\Longrightarrow \Gamma\vdash_K\varphi.
\]

A domain certificate checker \(C\) establishes \(C(x,c)=1\), which implies property \(P(x)\) only if the checker's correctness relation gives:

\[
C(x,c)=1\Longrightarrow P(x).
\]

A signature establishes only:

\[
\operatorname{VerifySig}(pk,m,\sigma)=1
\Longrightarrow
\operatorname{Says}(pk,m).
\]

A succinct argument is meaningful only relative to setup and verification material bound to the exact encoded relation. For every probabilistic polynomial-time adversary \(\mathcal A\), require:

\[
\Pr\!\left[
\begin{array}{l}
(pp,pk,vk,tr)\leftarrow
\operatorname{Setup}(1^\lambda,R_K,\textit{proofSystemID});\\
(x,\Pi)\leftarrow\mathcal A(pp,pk,vk,tr):\\
\operatorname{KeyValid}(pp,vk,R_K,tr)=1
\land\operatorname{Verify}(pp,vk,R_K,x,\Pi)=1\\
\land\neg\exists w\;R_K(x,w)=1
\end{array}
\right]\leq\epsilon(\lambda).
\]

The receiver pins and validates \((pp,vk,R_K,tr,\textit{proofSystemID})\). A verifier key for another relation, setup transcript, proof system, or security parameter proves nothing about this one. Setup randomness, adversary randomness, serialization, and relation/public-input commitments are inside the experiment.

If possession of \(w\) is claimed, knowledge soundness is required. Zero knowledge adds witness privacy:

\[
\operatorname{View}(x,\Pi)\approx_c\operatorname{Sim}(x),
\]

but does not strengthen the mathematical proposition.

## 3. Validation bases

```text
ValidationBasis =
    LOCAL_REPLAY
  | DOMAIN_CERTIFICATE
  | SUCCINCT_ARGUMENT
  | TRUSTED_ATTESTATION
```

Every assessment records its basis, exact relation ID, checker or verifier-key ID where applicable, public-input root, TCB profile, policy epoch, and native-witness availability.

- `LOCAL_REPLAY`: P0 default.
- `DOMAIN_CERTIFICATE`: P0 preferred for SAT/SMT, computations, or domains with small checkers.
- `SUCCINCT_ARGUMENT`: later identity-free verification compression.
- `TRUSTED_ATTESTATION`: cache/routing hint unless receiver policy explicitly trusts the operational validator; it receives an `ATTESTED` reliance grade, not `MECHANICALLY_CHECKED`.

Only the first three bases can produce a mechanically checked state after receiver-local verification. The strict P0 formal-closure profile uses the first two; a later locally verified succinct argument may join them after the stated break-even and TCB gates. A valid signature authenticates the attestation's source and bytes, not the theorem.

Keep native `proofArtifact` separate from optional `SuccinctArgument`.

## 4. Trusted-base comparison

| Mechanism | Principal trusted components |
|---|---|
| Native Lean replay | Logic/axioms, environment binding, Lean kernel source/binary, local runtime/hardware; source replay also involves elaboration/build |
| Native certificate | Small certificate checker and its correctness argument |
| Signed attestation | Signature/key binding, signer honesty, and the signer's checker/build/platform stack |
| SNARK/STARK | Encoded relation, arithmetization, serialization, verifier, hashes/commitments, cryptographic assumptions, and any setup |
| zkVM | Succinct-proof TCB plus ISA semantics, VM, guest compiler/binary, syscalls, and memory model |
| Recursive PCD | Underlying proof TCB plus recursive verifier gadget, accumulator, membership roots, and anti-cycle/epoch rules |
| Zero knowledge | Corresponding proof-system TCB plus blinding, hiding commitments, transcript assumptions, and side-channel resistance |

Succinct verification is a scalability/privacy tool, not foundational diversity.

## 5. Break-even condition

Let:

- \(c_L\): warm native replay cost;
- \(s_L\): native evidence bytes transferred to one validation domain;
- \(c_P\): succinct prover cost;
- \(c_V\): succinct verifier cost;
- \(s_V\): succinct proof/public-input bytes;
- \(F\): amortized implementation, audit, setup, and upgrade cost;
- \(\mu\): byte transfer/storage cost in compute-equivalent units;
- \(h\): distinct validation domains that would otherwise replay.

Then:

\[
C_{\mathrm{native}}(h)=h(c_L+\mu s_L),
\]

\[
C_{\mathrm{VC}}(h)=c_P+F+h(c_V+\mu s_V).
\]

Succinct verification is economical only when the denominator is positive and:

\[
h>h^*=\frac{c_P+F}
{(c_L-c_V)+\mu(s_L-s_V)}.
\]

The relevant \(h\) is distinct validator-cell reuse, not total logical-agent count. Cell-level checking, CAS deduplication, warm Lean environments, compiled caches, and proof-result caching reduce \(c_L\) and \(s_L\), often making \(h^*\) large.

Recursive aggregation has its own threshold and can be counterproductive when consumers need small subsets rather than one global batch.

## 6. When it is useful

| Situation | Recommendation |
|---|---|
| Public Lean proof consumed by servers | Native replay |
| SAT/SMT or computation with a compact transparent certificate | Check the specialized certificate |
| Repeated result inside one administrative cell | Locally authorized signed cache attestation may suffice by policy |
| Unknown remote signer | Treat signature as a hint; replay or verify certificate |
| Many low-power, bandwidth-limited, or on-chain consumers | Benchmark a succinct argument after measured break-even |
| Rapidly changing checker/program | zkVM reduces custom-circuit work but raises prover cost and TCB |
| Transparent setup/post-quantum preference | Consider STARK-like systems, accepting larger proofs/hashing cost |
| Stable, repeatedly consumed validation checkpoint | Consider recursive aggregation after measured demand |
| Public claim with genuinely confidential proof witness | Zero knowledge may be appropriate |
| Confidential statement/dependencies | Define a narrow committed relation first; expect reuse/repair/explanation costs |
| Semantic fidelity, novelty, usefulness, or agent judgment | SNARKs do not establish these |

Native artifacts should remain retrievable for public mathematical knowledge. Under the Core's separate `ReuseClass` field, a succinct proof without its available native proof/certificate/witness closure is labeled `OPAQUE_RELIANCE`. It may satisfy only an explicitly opaque local evidence contract and cannot satisfy the strict P0 or a public reusable-knowledge contract.

## 7. Recursive support proofs

The ordinary DTMKN justification DAG is already proof-carrying data in the systems sense. A later recursive proof may aggregate it only if the recursive relation checks:

- every leaf's allowed evidence contract;
- every composition rule and exact dependency root;
- public-input and policy roots;
- base cases;
- cycle exclusion or an explicit fixed-point rule;
- witness/data-availability status.

Recursive compression does not make the underlying artifacts available, explainable, or semantically faithful.

## 8. Staged plan

### P0

- native Lean/domain certificates;
- receiver-local checking;
- exact validation cache;
- advisory remote attestations;
- validation-basis metadata;
- measurement of cold/warm cost, proof size, memory, and distinct validation-domain fanout.

### P0.5

Freeze the exact validation relation and gather actual reuse/cost distributions. Benchmark native replay, a specialized certificate, signature verification, one zkVM, and one specialized succinct construction on the same objects.

### P1

Try public non-ZK succinct verification for one expensive, high-reuse deterministic checker relation. Generate proofs asynchronously only when forecast \(h>h^*\). Succinct proving must never consume the mandatory validation reserve.

Before enabling it, obtain an adaptive multi-theorem/concurrent soundness statement for at most \(q_{\max}\) receiver verifications per parameter/key epoch and freeze \(q_{\max}\). With setup/key-validation failure term \(\epsilon_{\mathrm{setup}}\), require a deployment budget

\[
\Pr[\text{any false accept in the epoch}]
\leq
\epsilon_{\mathrm{mt}}(\lambda,q_{\max})
+\epsilon_{\mathrm{setup}}
\leq\epsilon_{\mathrm{epoch}}.
\]

A union bound \(q_{\max}\epsilon(\lambda)\) may instantiate \(\epsilon_{\mathrm{mt}}\) only when the proof-system theorem covers the required adaptive/concurrent use and key reuse. Stop accepting, rekey, or increase \(\lambda\) before the counter reaches \(q_{\max}\). Recursive aggregation requires a separate composition theorem and explicit accounting for every base and recursive soundness/setup term.

### P2

Consider recursive cell/checkpoint aggregation only if repeated batch verification exceeds its own measured threshold.

### P3

Use zero knowledge only for a precise confidentiality requirement, preferably beginning with SAT/SMT or another small exported checker rather than a universal private Lean network.

## 9. Evaluation

Measure:

- cold and warm native replay;
- domain-certificate check cost and size;
- succinct prover/verifier time and peak memory;
- proof/public-input size;
- setup, audit, circuit/VM upgrade, and key-management cost;
- distinct validator-domain fanout;
- batching/subset access patterns;
- witness availability;
- cooperation loss from hiding proofs or dependencies;
- cross-checks against the native reference relation.

No decision should infer cryptographic viability from a simulated million-agent count. The break-even variable is repeated verification across actual trust/validation domains.

## 10. Existing feasibility evidence

Useful precedents include:

- zkPi, *Proving Lean Theorems in Zero-Knowledge* (CCS 2024), DOI `10.1145/3658644.3670322`;
- recursive SNARK/proof-carrying-data composition (STOC 2013), DOI `10.1145/2488608.2488623`;
- Nova folding/IVC (CRYPTO 2022), DOI `10.1007/978-3-031-15985-5_13`;
- *Proving UNSAT in Zero Knowledge*, IACR ePrint `2022/206`.

These establish feasibility in selected relations, not immediate economics or universal Lean coverage. Versions and local source hashes should be recorded before implementation dependence.
