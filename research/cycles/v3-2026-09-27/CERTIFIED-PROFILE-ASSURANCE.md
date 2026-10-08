# Exact certified profile: assurance and production boundary

2026-09-28 UTC. `v3_efficiency`; read-only source audit, not a new proof run.
Canonical guard passed. Used sources, installations and evidence are unchanged.
This instantiates the obligations in [SCALE-CERTIFICATES](SCALE-CERTIFICATES.md)
and [SCALE-SOUNDNESS-DECISION](SCALE-SOUNDNESS-DECISION.md); it does not repeat
their general design or claim their open metatheorems have been proved.

## Decision

The inspected receiver has the important *complete* cryptographic acceptance
gates: a real Succinct/Poseidon2 receipt, trusted SDK verifier parameters,
successful execution of the adopted image, the exact application journal,
and no unresolved assumptions. No integrity-only, fake-receipt or
peer-selected-control-root acceptance shortcut was found on that path.

This supports an **experimental certificate of the exact guest computation**,
conditional on the adopted proof system and implementation. It does not yet
establish stock Lean4.34 derivability, production adaptive recursive soundness,
or useful-growth benefit. These are separate central obligations, not reasons
to require identity votes, a central server or a global ledger.

One concrete assurance-scope finding matters: the receiver uses the SDK's
**whole default allowed recursion-program root**, not only the honest
producer's `lift/join/resolve`, no-PoVW, segment-po2=18 subset. Production review
must cover that actual accepted set. Honest-prover restrictions alone do not
narrow a malicious prover's options.

## Fixed implementation being discussed

| Item | Adopted identity |
|---|---|
| Logical profile | `dmkn-experimental-certified-01` |
| Guest image | `7a8589ef226cc222696afa93f0fca96a0f3d56ca03fcdebdc9008f7e79a3f0d0` |
| Foundation | `4eeaab61471a4ab9f93209af9aad66fcb45f6322783b919851d4d95ea33f9f80` |
| Journal | `DMKNJ002`, version 2, 148 bytes |
| SDK source | retained commit directory `risc0-3bbcd44d6459b9ef6ac0df3846dc9215514934e8`, package `risc0-zkvm` 5.0.0, locally adapted Windows build |
| Producer / receiver | `experiments/general-checker-guest-02/host07.rs` / `host06.rs` |
| Proved relation | guest02 main/journal plus guest04 `relation.rs` and fixed specialization, as bound by guest04 build/adoption evidence |
| Receiver wrapper | frozen `product-local/certified-verifier-source-01/cert_verify.py`, SHA-256 `0984549a88fb5bd4971e39ae7e0531b99e69c54ad6c02916e9481cec4af27bbe` |

Below, `SDK/` denotes the exact retained source under
`experiments/general-checker-host-05/build-01/source/` followed by that commit
directory. This is not an assertion that an arbitrary stock 5.0.0 binary or
future identically named profile has these properties. Receiver policy must
adopt the full installation/profile hash out of band; a hash chosen by the
sender authenticates no independently trusted checker.

## Source-to-guarantee mapping

| Actual source | What it enforces; what it does not |
|---|---|
| `host06.rs:81`, `host07.rs:79`, their `verify` branches | Only `InnerReceipt::Succinct` with hash suite `poseidon2`; `VerifierContext::default().with_dev_mode(false)`; full `verify_with_context`; application journal validation; exact requested journal equality. Main also rejects `RISC0_DEV_MODE`. Bounded fixed-int bincode rejects trailing data. A successful intermediate checkpoint is not accepted here as an application receipt. |
| `SDK/risc0/zkvm/src/receipt.rs:163` | Checks inner/metadata parameter consistency, cryptographic integrity, then equality to the *entire* expected `ReceiptClaim::ok(image, journal_digest)`. Integrity-only verification would be insufficient; the actual path does not stop there. |
| `SDK/risc0/zkvm/src/claim/receipt.rs:75` | `ReceiptClaim::ok` binds the expected image, normalized successful `Halted(0)` post-state, no input and journal with empty-assumptions digest. Thus final full verification cannot legitimately accept an unresolved conditional claim, subject to digest binding and proof-system soundness. |
| `SDK/risc0/zkvm/src/receipt/succinct.rs:106` | Uses caller-trusted succinct parameters; checks their digest, proof-system/circuit info, seal/metadata control-ID equality, membership under trusted control root, actual STARK verification, embedded recursive-root equality, and embedded claim hash. A peer cannot substitute a new recursive verifier root merely through receipt metadata. |
| `SDK/risc0/zkvm/src/guest/env/verify.rs:47` | Guest `env::verify(image,parent_journal)` constructs the exact successful parent claim and adds the same-control-root assumption. It does **not**, by itself, produce an unconditional certificate. The SDK composition document explicitly separates adding from resolving assumptions. |
| guest02 `guest/src/main.rs:20`; guest04 `guest/src/relation.rs:212` | Bounded frames and EOF; relation success; every declared parent passed to `env::verify`; committed journal. Relation checks strict unsigned rank descent, at most eight distinct parent interfaces, base iff no parents, exact same image/foundation journals, authenticated support, exact interface use and declaration/reference census. |
| guest04 `relation.rs:310` | Nanoda runs with explicit permitted axioms, hard rejection of unpermitted axioms, unsafe-all-axioms disabled, one thread, extensions disabled; no skipped declarations. The new theorem and parent declaration types are checked; parent types must be `Prop`. Foundation support is authenticated, not independently re-proved on every contribution. |
| `host07.rs:145`, `:258`, `:268` | Honest production fully verifies parents, checks the actual successful session/journal, forbids MMR/PoVW execution, checks every lift/join/resolve result, and requires composite and final succinct claim equality to the fresh session claim. Finish then runs complete application-receipt verification. Saved segment snapshots supply coherent witnesses, not mathematical authority. |
| `cert_verify.py:197`, `:350`, `:432` | Independently adopted profile hash pins installed assets and driver; bounded bundle snapshot is passed to the genuine driver under a Job. Success retains `native_admission: false`. This wrapper does not claim that a process marker alone replaces the pinned verifier. |

The guest receives an image field rather than computing its own code hash.
That is not a missing self-hash check: final verification binds executed code
to the adopted image, application journal validation binds the committed image
field to it, and guest parent calls use that same field. All three edges are
necessary to the argument.

## The actual recursive verifier is broader than the producer

`SDK/risc0/zkvm/src/receipt/succinct.rs:398` selects the precomputed
`ALLOWED_CONTROL_ROOT`; the source constant is
`517f405d5dbda85b2dc15f3ab6f8a05170bde64980ef594a8e9fd923febe1a03`
in `SDK/risc0/circuit/recursion/src/control_id.rs:59`.
`receipt.rs:881` sets `DEFAULT_MAX_PO2 = 22`. The source's root-consistency
test associates the default root with that maximum; this audit read the test,
it did not execute it anew.

The allowed-program constructor at `succinct.rs:273` includes `join`,
`resolve`, `identity`, `union`, `unwrap_povw`, PoVW join/resolve/unwrap variants,
and ordinary/PoVW lift variants through the allowed po2 range. The final
receiver does not select a new root restricted to the producer's po2=18.

This is **not an identified exploit**: an allowed recursion program is supposed
to preserve the appropriate claim relation, and full application claim checks
still apply. But a security argument for only our executed three-program
sequence is incomplete. A production decision needs coverage of the accepted
root/program suite and its parameter generation, or a separately justified,
tested narrower successor. Do not edit the used verifier or silently narrow
its root during this campaign.

## Remaining assumptions, stated at the right boundary

Let `C` be the actual guest's semantic compliance step and `Cl(C,F)` its finite
grounded DAG closure. The intended implication is:

```text
final receipt acceptance
  => membership in Cl(C,F)             [recursive cryptographic assurance]
  => derivability under adopted Lean F [local fidelity + compatible realization].
```

The first implication requires the **adaptive multi-claim recursive/PCD
soundness property for these actual reused parameters, allowed programs,
Fiat-Shamir/hash construction, branching and security horizon**. A suitable
published construction theorem carefully instantiated to this profile can
justify it; absent that mapping it remains an explicit unestablished PCD
assumption. Rank descent and finite tests do not supply recursive extraction
or prevent exponential unrolling in an attempted reduction. This is precisely
the distinction already explained in SCALE-SOUNDNESS-DECISION, not a new demand
to mechanically prove every implementation line before any useful release.

The second implication needs faithful parsing/encoding and checking by
`nanoda_lib` commit `3a2407216ee84a75f9e1aead6803d0578be06ae7`, package 0.4.19,
relative to adopted Lean4.34 semantics; well-formed correctly interpreted
fixed foundation/support; and sound sealed-`Prop` substitution with one
compatible simultaneous realization. The differential/SEALED_PROP checks and
ordinary conditional-source checks are finite supporting evidence, not a
Nanoda-to-Lean equivalence theorem. New definitions/inductives and arbitrary
transparent-definition substitution are not authorized by this theorem-only
profile. Unsupported proof-sensitive reduction must remain refusal.

Compiler/guest-image binding, actual RISC-V and recursion circuits, verifier
implementation, canonical interface commitments and installation adoption are
also part of the declared implementation/cryptographic assumptions. A hash
pin identifies code, not its correctness. An exploitable checker bug is not a
small random probability inferred from test counts.

The selected receipt excludes Groth16. Do not add BN254 trusted-ceremony
assumptions as necessary to this path just because the SDK supports another
receipt form. SHA-based structural/image/journal binding and the selected
Poseidon2/STARK/Fiat-Shamir assumptions remain relevant.

## What the available upstream documentation actually supports

`SDK/website/api/zkvm/composition.md` explains add-assumption/resolve behavior;
`SDK/website/api/recursion.md` explains lift/join/resolve and separates succinct
STARK receipts from optional Groth16 compression. These are useful operational
guarantees matched to the source above.

`SDK/website/api/security-model.md` explicitly says adopters must validate
guest security. Its audit table refers to 2023/2024 work and its prose still
uses testnet language. Its security estimates differ from other retained
README/calculator comments. `SDK/risc0/zkp/src/prove/soundness.rs:16` explicitly
distinguishes conjectured Toy-Problem/FRI regimes from proven regimes and has
segment-size-dependent estimates. None of these inspected documents supplies
an instantiated adaptive branching/multi-claim theorem or concrete error
budget for this locally adapted SDK and our guest.

Therefore this audit assigns **no invented security-bit count or numerical
failure probability** to our profile. No current external advisory/audit
coverage review was performed here; that is not a claim that no upstream
audits exist. Production adoption needs version-specific advisory review,
actual parameter/theorem mapping and coverage of local modifications, not
transplanting old on-chain estimates or multiplying them by network size.

## Consequential next gates, without duplicating completed work

- Complete the currently selected real receipt and cold-receiver qualification;
  report the actual outcome, not a predicted finish. A rank-zero receipt alone
  does not exercise parent-assumption discharge.
- Qualify one actual ordinary-source child using the body-free parent interface,
  fully resolve its parent assumption and accept its resulting receipt freshly.
  Conditional native checking or an expected journal file is not this result.
- For a production trust label, close or explicitly scope the exact
  Nanoda/Lean fidelity and whole-accepted-root recursive assurance gaps above.
  For tentative v3, preserve the experimental label and native fallback.
- Keep proving expense, cold verification, interface import and downstream
  contribution cost separate. Removing mandatory ancestry replay may be a
  valuable scaling property even when this CPU prover has a poor finite-workload
  break-even point; it does not establish faster useful growth by itself.

No runtime gate is marked passed by this source note. Root's actual outcome
audits remain authoritative. No new dependency, build, proof campaign,
publication or source modification is commissioned here.
