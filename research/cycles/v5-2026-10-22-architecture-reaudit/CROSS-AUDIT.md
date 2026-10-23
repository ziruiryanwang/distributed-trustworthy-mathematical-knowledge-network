# Independent cross-audit of the architecture synthesis

Reviewer: `/root/storage_outcome_audit`, 2026-10-22.
Scope: the complete `ARCHITECTURE-REAUDIT.md`, SHA-256
`c3891a1db2949d85b8cd28c1f5d2c861686377ac8b5f87ad9afd949b5e0885e5`.
Source/theory review only; no runtime or product changes.

## Disposition

**PASS for the recommended architecture direction and its stated trust/cost
boundaries.** No blocking correction found in the read synthesis. This is not
qualification of a durable cache, alternative mathematical witness, new prover,
deployment, or completed v5. The recommendation is materially stronger than
either mandatory per-contribution certification or unverified interface reuse.

## Challenges applied

| Adversarial question | Finding |
|---|---|
| Does a downstream type-check turn an advertised false premise into truth? | No. The synthesis requires grounded leaves and conditional derivability, explicitly rejects peer checked-status flags, and links the concrete `h : False` counterexample in the trust audit. |
| Does native-first silently abandon the user's cold no-history contract? | No. It separates ancestry-free receiving from ordinary closure fallback and says missing assurance is deferred/unavailable. A short independent proof is allowed only relative to an accepted basis. |
| Is universal cheap cold access promised after making certificates optional? | No. Certificate availability, capacity and custody remain explicit obligations, including possible postponement. This limitation must remain visible in final user-facing decisions. |
| Can a peer-supplied snapshot populate a durable mathematical cache? | No. Cache entries require actual acceptance, exact bindings and a protected local provenance boundary. Downloaded flags, old handles and spent allowances are excluded. |
| Are immutable theorem validity and revocable implementation trust conflated? | No. The synthesis explicitly distinguishes mathematical truth from the current warrant for relying on a checker. New operations obtain new resource/lifetime grants. |
| Is proof independence allowed without changing mathematical identity dishonestly? | Yes. Alternative witnesses can preserve a module only when its exact descriptors do; changed types/definitions/commitments require a new object or checked transport. |
| Does cryptographic hashing supply the base case of the soundness induction? | No. It supplies binding; actual semantic and recursive cryptographic assumptions establish the base. No numerical error bound is invented. |
| Are portable proof claims borrowed from TEE/quorum/optimistic alternatives? | No. They are expressly different assurance mechanisms, not unchanged replacements. Independent operator/watchdog/hardware assumptions remain to be instantiated. |
| Does the cost comparison divide different mathematical obligations? | No. It warns that U production divided by V's conditional native check is invalid. Nested verification/checking measurements are not added to complete-operation cost. |
| Are generic zkVM gains asserted from removing work never inside the guest? | No. It states that current guests already exclude LLM search and Lean tactic execution. Relation/backend improvements remain investigations, not achieved speedups. |

## Mathematical example independently checked

The GCD witness argument is correct for the stated integers and positive `g`.
The equalities `a = g*u` and `b = g*v` show `g` divides both inputs. If `d`
divides both, then `d` divides `a*x + b*y = g`. Hence `g` has the usual
greatest-common-divisor characterization; positivity selects the positive
representative. Signs and a zero single input cause no problem. The exclusion
of both inputs zero is consistent with the positive witness requirement.

The receiver must still evaluate the integer equalities and apply an already
warranted generic theorem. The synthesis says this and does not claim that
the example is implemented in the current supported Lean subset. This is an
appropriate illustration of certifying an answer rather than the entire
algorithm that found it.

## Two nonblocking precision points for the next design

1. **Persistent cache support must include assurance lineage, not only semantic
   dependencies.** Two identical mathematical objects can be warranted through
   different checker/certificate policies. If the implementation persists a
   warrant, its current-support check must follow the actual chosen assurance
   route or establish an alternative still-supported route. This follows from
   the synthesis's withdrawal requirement but should be explicit in the next
   state schema. It does not require replaying all proof terms: an integrity-
   protected support index or exact owner/adoption generation can provide the
   dependency bookkeeping under a stated local threat model.
2. **No-history is an acceptance guarantee, not a universal availability
   guarantee.** Existing certificates or a genuinely short independent proof
   can support it. Optional native closure checking remains a separate
   caller-selected mode. A public API should expose the distinction in its
   requested delivery class and terminal result; timeout or budget refusal
   must not silently switch to social attestation or historical replay.

Neither point requires another expensive experiment to decide the principle.
They should be incorporated when root selects the smallest new public seam.

## Assurance limits of this review

This review checks the logical architecture and internal interpretation of
retained costs. It does not independently re-audit every external primary paper
or reproduce the economics worker's numerical extraction. The synthesis
correctly labels those sources as mechanism precedents, not transferred
end-to-end performance evidence. Its cryptographic-recursion hypothesis is
still an explicit assurance obligation, not a completed theorem about the
entire accepted stack.

No universal proof-size bound, automatic shortest-proof procedure, unconditional
global search completeness, indefinite availability, or inevitable exponential
growth was found in the synthesis. No new deployment, license, purchase,
trust policy or proof campaign is authorized by this pass.
