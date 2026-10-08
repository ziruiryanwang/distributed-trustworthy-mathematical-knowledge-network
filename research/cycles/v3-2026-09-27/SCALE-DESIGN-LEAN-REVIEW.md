# Scale design: narrow Lean bridge review

2026-09-27. Reviewer `/root/v3_index`, independent of root's integration draft,
but author of `SCALE-LEAN-INTERFACES.md`, which informs it. Canonical guard
passed. Read-only comparison with the actual bundled Lean4.34.0 API/source
findings; no implementation, experiment or duplicate cryptographic review.

Reviewed `SCALE-DESIGN.md` SHA-256:
`19a4cfe14cd6efdc018565faf2a42e82701d37274a7f4ff52258e98f1f585b50`.

Disposition: **NO BLOCKING LOGICAL-BRIDGE DESIGN DEFECT FOUND IN THIS PROPOSAL**.
This clears the narrow design question for a separately reviewed native seam
experiment, not cryptographic implementation, mathematical metatheorem proof,
product acceptance-mode selection or execution.

## Central findings

The design correctly distinguishes Lean checking a proof *relative to derived
premises* from discharging those premises to the adopted base. It requires one
compatible realization of shared definitions/types/rules, not merely two
individually certified but incompatible name-based environments. The proposed
registry is evidence-gated; a well-formed axiom declaration does not certify
its own proposition. The source frontend cannot expand the base trust policy.

SEALED_PROP is the appropriate first scope. It does not identify arbitrary
same-typed data implementations, import trusted arbitrary module images or
install unchecked inductive computation rules. Its explicit absence of an
automatic ancestor-body fallback is important: this really changes the scale
contract rather than putting an optimistic cache in front of full replay.

The actual pinned sources support the proposed seam: theorem module exports
can be axiom-shaped, and `addDeclCore` checks such a declaration's type. They
also support the stated limitation: theorem proofs can matter for `Acc.rec`
conversion. Certified propositional equations, checked by ordinary rewriting,
are a legitimate alternative to unproved new reduction rules, without a promise
that every old proof can be repaired this way.

The release gates correctly separate local premise-registry compatibility from
a real recursive certificate backend and cold history-independent operation.
No static API argument supplies the latter two results.

## Implementation-critical interpretations to retain

These are exact readings of the draft, not requests for peripheral modules:

- “Opaque derived premise” is a semantic description of sealed reliance. The
  simplest tested representation would be an **axiom-shaped** entry, not an
  `opaqueDecl`/`thmDecl` with a fabricated body. The registry records its derived
  evidence separately; the base axiom allowlist is not expanded globally.
- Require actual kernel-confirmed Prop classification and exact universe
  binding. A packet's `declaration_kind` tag is not this check.
- A common logical interface may have multiple certified proof backings under
  SEALED_PROP. This does not merge their distinct archival proof-instance CIDs,
  nor authorize proof-sensitive conversion on an unspecified representative.
- The realization argument must cover references in types and computational
  declarations too. Its conclusion is the realized statement in the compatible
  extension, not an unrelated statement obtained by silently renaming constants.
- Auditing only explicit final-proof constant occurrences is insufficient if
  other installed declarations or conversion rules introduce hidden premises.
  The draft's authenticated selected environment and dependency coverage must
  be applied to those declarations as well.

With these interpretations, the consolidated design does not overclaim the
pinned Lean APIs or universal proof erasure. The remaining obligations are
explicit, central and suitable for implementation discrimination.

## Fresh-process evidence requirement

The first native test must not merely change lookup behavior in an environment
which still stores old proof values. Proposed exact source/executable/input
separation is appended to `SCALE-LEAN-INTERFACES.md`. Each consumer imports only
proof-free shared support, starts a new checking environment, and receives a
body-free interface/locally authorized evidence packet. C must not receive
either L's body or M's body, and need not receive L's interface at all.

This is physical absence from the prescribed consumer inputs and checking
environments, plus audited module/import graphs—not a hostile filesystem
sandbox claim. Root-held original proofs remain separately available for the
local evidence audit. No mock cryptographic verifier substitutes for them.
