# Adversarial review of the integrated scale design

2026-09-27. Reviewer: `v3_efficiency`. Read-only product/source review; no
proof generation, Lean execution, SDK installation or product change.
Canonical workspace guard passed.

Reviewed `SCALE-DESIGN.md`, SHA-256
`19a4cfe14cd6efdc018565faf2a42e82701d37274a7f4ff52258e98f1f585b50`,
against `SCALE-REQUIREMENTS.md`, `SCALE-CERTIFICATES.md` and the related
Lean-interface/dataflow proposals. Later edits need their own delta assessment.

## Disposition

**PASS AS A CONDITIONAL ARCHITECTURE DIRECTION; NOT READY TO ENABLE
CERTIFICATE-BACKED ACCEPTANCE.** No central unsoundness was found in the
stated conditional architecture. It addresses the user's essential requirement:
both a cold receiver and the next contribution prover must avoid mandatory
ancestral proof downloads/replay. It neither claims an existing backend nor
confuses native-local interface experiments with transferable cryptographic
verification.

Two boundary clarifications below should be fixed before coding the new format
or premise auditor. They are concrete ambiguity hazards, not a request for
another full architecture or a reason to delay the native interface experiment.
The backend remains a genuine implementation blocker for the scalable release
claim, not an omitted prose detail that can be “audited away.”

## C1 — Limit proof-instance coalescing to the sealed semantic contract

The draft says “Two proofs of one exact theorem may back one interface.” This
is defensible for the selected sealed `Prop` interface, under the simultaneous
realization/substitution obligation. It must not be generalized to native
artifact identity or proof-dependent computational behavior. The same document
correctly notes that proof-body unfolding can affect actual conversion.

Required clarification:

> Multiple proof artifacts may certify the same **sealed theorem interface**
> only when their exact type/universe/reference/semantic-profile bindings
> agree. Their native proof-instance identities remain distinct. Selecting a
> proof-sensitive body/reduction interface also selects that exact body and
> its dependencies; statement equality alone does not authorize substitution.

This matters because the capsule schema also covers computational content and
has an optional native-artifact commitment. Without the scope rule, a later
implementation could deduplicate a body-bearing interface by type and import
the wrong conversion behavior. The draft's general simultaneous-realization
requirement is correct; the wire identity rule must enforce that requirement.

## C2 — Specify support closure at certificate boundaries, not only direct syntax

The draft requires enumerating external dependencies from checked canonical
terms and gathering the actual external premise set. Directly collecting
constant names from the new proof is not sufficient: types, transparent
definition bodies, generated group interfaces and conversion can expose
additional non-base references.

Conversely, recursively traversing every certified theorem's old proof to
enumerate that support reinstates the forbidden history cost. The two errors
have opposite effects but arise at the same missing traversal contract.

Required clarification:

> The import audit traverses the new proof/type and authenticated type or
> permitted computational support, binding every reached non-base declaration
> to its exact supported certificate/import record. Traversal stops at a valid
> sealed theorem certificate: that certificate discharges its hidden proof
> dependencies. It must neither trust a directly referenced constant while
> ignoring its uncertified exposed support, nor open certified theorem proof
> histories merely to recount their already certified premises.

Similarly, `closed_external_reference_bindings` in the capsule must mean
the bindings needed to interpret the **exposed interface**, not a flattened
list of every ancestral proof dependency. Hidden support stays committed by
the recursive certificate. Actual selected interface/type size is charged;
the claim is not that this genuine support is always small.

The companion dataflow proposal already makes role-sensitive closure and
sealed proof references explicit. Link or adopt that rule in the integrated
format and exact-relation sections so that a programmer cannot substitute
the legacy full-closure walker for the intended interface operation.

## Central challenges that the draft survives

- **Self-supporting certificates:** ranks are not sold as cryptographic
  soundness. The text additionally requires grounded base cases and an actual
  adaptive recursive/PCD theorem.
- **Unproved premises disguised as imports:** the proposed registry is
  certificate/profile-bound and the new contribution discharges its imports.
  The draft does not infer proof from Lean's acceptance of an axiom entry.
- **Different hidden meanings of one constant:** simultaneous compatible
  realization, exact body/group bindings and collision refusal are required.
- **Tiny receipt followed by full replay at submission:** admission, import,
  new checking and export change together; the next prover also avoids history.
- **Unavoidable conversion costs hidden as scalability:** definition/type work
  remains charged, proof-sensitive incompatibilities may refuse, and there is
  no automatic full-history fallback in the sealed profile.
- **Trusting an external program success bit:** the exact deterministic checking
  relation must execute within the proved computation or a justified verified
  subrelation. A VM wrapper around a host result is not accepted evidence.
- **Global chain smuggled into recursion:** independent object/compatible-subset
  certification does not require one global environment, ordering or counter.
- **Proof validity mistaken for availability/growth:** the draft preserves these
  distinctions and does not credit this mechanism with useful-growth evidence.

## Concrete next coding choice and blocker

Proceed with the bounded **native-only SEALED_PROP interface/import seam**
already specified by the Lean-interface agent. Its issuer evidence is locally
trusted and honestly labeled. It should test the realization/premise-accounting
contract and produce the exact deterministic input/output fixture for the next
backend step. Do not implement a successful mock remote-certificate branch.

For the first cryptographic candidate, make one bounded **RISC Zero source
compatibility decision**, not a broad vendor survey:

1. Pin a concrete RISC Zero source revision and inspect its C/C++ guest build
   path, supported guest ABI/runtime assumptions, recursive verification API,
   unresolved-assumption behavior and final receipt verification.
2. Inspect the actual upstream Lean kernel/runtime at the project's pinned
   commit `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`; enumerate the minimal
   dependencies of checked `lean_add_decl`, not an elaborator/compiler/UI.
3. Give GO only for a concrete supported guest closure and recursive receipt
   path, with exact unresolved engineering work. A documented C guest example
   alone is not proof that this Lean C++ kernel/runtime builds or behaves
   correctly there. Unknown external dependencies are NO-GO for selecting an
   immediate full-kernel port, not permission to assume them away.
4. On GO, the next fresh code is a deterministic guest harness that checks
   one real pinned canonical Lean declaration, emits its exact interface
   commitment, and composes one actual accepted parent receipt. On NO-GO,
   do not sink the tentative release into an unbounded Lean-runtime port;
   select a separately audited restricted proof-oriented checker route or
   report crypto scale capability incomplete.

This review establishes no build readiness. Read-only local lookup found no
`cargo`, `rustc`, `clang`, `clang++`, `cmake`, `ninja`, `lean` or `lake` on PATH.
It found `wsl.exe`, which proves neither an installed Linux distribution nor
a usable compiler. The project's own pinned `lean.exe` exists under
`software/runtime/lean-4.34.0-windows/bin`; that is not a zkVM guest toolchain.
These are scoped command/file observations, not an exhaustive machine search.

The bundled `Lean/Environment.lean` declares checked `addDeclCore` through the
external symbol `lean_add_decl`; its `src/lean/kernel` directory contained no
source files in this inspection. Thus “compile this Lean file into the VM”
does not by itself include the actual native kernel implementation. Upstream
source/ABI inspection is consequential, not peripheral tooling work.

Root assigned the resulting bounded source assessment to
`SCALE-BACKEND-FEASIBILITY.md`. No SDK, runtime, paid service, clone or prover
execution is authorized by this review. No quantitative speed or overnight
port completion is predicted.

## Readiness boundary

Architecture direction: supported, with C1/C2 made explicit before format and
dependency-auditor implementation. Native semantic discriminator: ready for
its own bounded source/harness review. Transferable recursive Lean certificate:
**not implemented or qualified**. Huge-network software claim: **not ready**.
No amount of source16 reader improvement changes the last two dispositions.
