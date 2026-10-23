# A broad locally checked Lean library, with an optional certified subset

2026-10-22. Narrow source-design audit by `storage_integration_adapter`.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
No build, test, import, proof, installation, Git mutation or product edit was run.
This note recommends a boundary; it does not adopt a new checker or trust policy.

## Answer

**Yes, in principle: ordinary local mathematical acceptance need not pass through
the custom cryptographic relation.** A node can establish an ordinary Lean
environment once, kernel-check each subsequent contribution against that
environment, and persist its locally warranted knowledge. Only selected supported
interfaces then need portable certification for ancestry-free cold receivers.

This is not a switch already exposed by the installed product. Its current
"native" path runs the same restricted relation used by the cryptographic
guest. Merely making proof production optional leaves those restrictions intact.
Broadening the native lane therefore needs a genuinely separate, reviewed
acceptance profile; it does not require broadening the zk relation first.

The compromise must be explicit: a cold broad-library reader initially checks
its selected missing proof closure, already possesses a matching local checked
basis, or adopts some separately disclosed basis trust. The existing certified
subset can retain its stronger ancestry-free receiving contract. Warm local
amortization does not solve arbitrary broad cold acceptance.

## What the installed sources actually do

The authoritative map is
`experiments/v5-local-checks/distribution-candidate-preflight-01-input.json`
(SHA-256 `25e7c849e41f394498e21a60cc7800ecffb67b0cee1b3911d7164977ce4f2364`).
The later producer assembly preserves its ordinary130 sources. The five mapped
Python sources below were hash-compared to this map during this audit; all match.

| Boundary | Actual implementation and consequence |
|---|---|
| Installed native executable | Map `assets.native` selects `delta-native-build-02/native_delta.exe`. Its recorded source `software/v5/delta/native.rs` directly includes `modules/receipt/src/relation.rs`, `policy.rs`, canonical commitments and journal code. It is a native execution of the custom conditional relation, not Lean's ordinary kernel acceptance API. These three source files match the retained build02 source-map hashes. |
| Restricted mathematical policy | `receipt/src/policy.rs` fixes413 foundation rows/22 declarations, no new axioms or quotient primitives, no unsafe/partial declarations, and disabled Nat/String extensions. The relation requires exact foundation rows, exact parent image/foundation/policy/rank, supported canonical groups and the Nanoda-derived conditional checker. |
| Lean authoring | Selected `authoring/native02/AuthorLean.lean` imports pinned Init and elaborates owner-authorized source. `installGroup` reconstructs imported theorem/opaque interfaces as checked **axiom declarations**; their mathematical justification comes from separately warranted imports, not that kernel constructor. Definitions/inductive groups receive checked reconstruction and exact comparison. The exported result explicitly remains untrusted until later admission. |
| Source-to-relation bridge | Installed `modules/source_rows.py` is actually `software/v5/nat_literals/source_rows.py`. Installed `mixed_claims/authoring.py` decodes exported rows through this bridge and emits another restricted relation witness. Neither frontend success nor `SourceOperation.finish` grants mathematical authority. |
| Canonical expressions | Installed `modules/codec.py` accepts bound variables, sorts, constants, applications, lambdas, foralls, lets and projections. It has no primitive native Nat/String literal form. The selected importer expands bounded Nat literals into local `Nat.zero`/`Nat.succ`; String literals still refuse. This is a representation restriction, not a necessity of mathematical trust. |
| Library usability | Authoring reconstructs selected semantic interfaces under `DMKN.Mod.<ID>...`, not complete ordinary Lean module registries. Namespace notation, instances and attributes are not supplied by those descriptors. The API explicitly recommends qualified names/recursors. Relocated Nat is not automatically Lean's built-in Nat. |
| Existing non-cryptographic closure owner | `native_closure/README.md` describes ordinary complete-DAG checking, but with the same restricted checker profile, same-live tokens and no general semantic-context/source-authoring integration. It is not already a broad persistent Lean library. |

Concrete source anchors: `delta/native.rs:4` and `:30`;
`modules/receipt/src/relation.rs:103`; `modules/receipt/src/policy.rs:7`;
`authoring/native02/AuthorLean.lean:733`, `:761`, `:838`;
`mixed_claims/authoring.py:223`; `nat_literals/source_rows.py:267`;
`modules/codec.py:169`; `authoring/API.md:164`.
Earlier API status paragraphs are historical; this note relies on source for
these limits and does not retract the later actual U-to-V qualification.

## Which restrictions must stay, and which need not

| Restriction | Trust requirement or implementation choice? |
|---|---|
| Every accepted theorem has a derivation under disclosed axioms and grounded imports | Essential. A successful check in an environment containing arbitrary `h : False` proves only a conditional judgment. |
| Exact types, universes, reduction semantics, declaration identity and compatible imports | Essential. Neither a broad kernel nor a content hash makes mismatched environments equivalent. |
| No `sorryAx` or arbitrary newly asserted axiom disguised as a theorem | Essential to the intended admission policy. An intentionally chosen axiom has to be explicit, not silently admitted because a source file compiles. |
| A no-axiom22-declaration foundation | A particular policy, not necessary for all Lean mathematics. A broader profile may explicitly support Lean's conventional logical primitives/axioms and standard definitions. Their exact declarations/semantics and adoption must be stated; do not silently relabel old certificates. |
| No quotient support; Nat encoded as successor chains; no String literal syntax | Current schema/profile choices. Lean's supported kernel semantics can treat these directly. Turning Nanoda config flags on does not by itself update canonical binding or justify the broader profile. |
| Exact zk image and184-byte journal in every native acceptance | Current protocol coupling, not a requirement for independent ordinary proof checking. A new native profile can bind its own checker/version/environment without pretending to possess an old journal warrant. |
| Finite source, depth, group, universe and byte caps | Resource safety is necessary; these particular small constants and a single16MiB whole-input envelope are not mathematical necessities. Bounded incremental checked extensions need not retain the current fixed whole-library limits. |
| No unchecked executable peer code in the trusted checker | Essential to the security boundary. Ordinary source, tactics, initializers and downloaded `.olean` files cannot simply enter the acceptance process as trusted data. Current process Jobs are resource limits, not a hostile-code sandbox. |
| Political author identity, global ledger, single canonical worldwide environment | Not required for this lane. Exact compatible local environments and independently checked evidence suffice. |

Unsafe implementation code may exist in a separately isolated producer that
returns checked mathematical proof data. This is different from accepting an
unsafe declaration or arbitrary native evaluation as a logical inference.

## Small acceptance argument for the new lane

Fix an adopted Lean kernel version/semantics and explicit axiom policy P.
Let E0 be an independently checked or explicitly trusted initial environment.
For each contribution delta:

1. Decode inert mathematical declaration data with bounded parsing. Bind the
   exact statements, values, semantic imports and supported metadata.
2. Resolve every imported fact to an already grounded local environment entry,
   or first establish it through ordinary checking or an accepted certificate
   bridge. Never replace an unresolved premise by an unqualified axiom.
3. Apply the selected kernel's checked declaration constructor to the new
   declaration/group against exactly that environment. Do not import arbitrary
   peer `ConstantInfo` or a compiled environment that bypasses this check.
4. Commit the resulting local accepted environment transactionally, preserving
   its checker/policy/basis lineage. Fresh operations get fresh grants; a stored
   result is not a reusable process token.

If E0 is valid under P and each constructor preserves validity, induction gives
validity of the accumulated environment. Protected persistence preserves a
previously established judgment; it does not supply a new mathematical axiom.
Checker bug withdrawal, policy changes and rollback assumptions remain those
spelled out in `DEMAND-PROTOCOL.md`.

For m local sessions, the checking work can have the form

    initial selected basis check
    + sum of distinct new declaration checks
    + selected semantic/import and persistent-cache integrity costs.

It need not repeat the entire old proof closure at every session. This is a
locality/amortization argument, not a measured runtime bound or a guarantee that
type conversion, large statements, memory use or initial onboarding are cheap.

Using a full ordinary Lean module library also requires elaborator convenience
state. Trusted local authoring may use locally built module artifacts; the
mathematical receiver should still rely on the independent acceptance boundary.
Reconstructing every notation/typeclass registry in the mathematical protocol
is unnecessary. Conversely, simply restoring peer `.olean` files does not
implement the induction above.

## Reuse versus genuinely new work

**Reuse without claiming new authority:** current content-addressed custody,
budgeted acquisition, provider discovery/coverage machinery, service supervision,
trust-adoption/withdrawal patterns, existing certified-subset receiver and its
selected interface/body checks. Raw source-export code and local owner-authoring
are candidate producer-side adapters, not acceptance kernels. Formal index
extractors may need an additional representation adapter; current canonical
features cannot be claimed to cover arbitrary Lean data unchanged.

**New and consequential:** an ordinary Lean-native acceptance profile and
inert declaration codec; checked restoration/extension of a protected persistent
environment; a precise initial-basis/axiom policy; full supported Lean semantic
binding rather than forced round-tripping through `DMKN_MODULE_SPEC_V1`; and
explicit evidence-class negotiation at publication/retrieval. These are a new
local assurance boundary, not a generic success-report loader.

**Keep separate:** native broad acceptance and the existing certified subset
must not share authority tokens or exact-J identities by convenience. A supported
declaration may have both representations only through checked correspondence.
The current certified interface reconstructor is useful evidence for that
bridge, but its authoring-only assumption mode is not already a broad receiver.
Unsupported certification should not prevent ordinary checked contribution;
ordinary acceptance must not advertise ancestry-free cold certification.

The retained Nanoda library has generic `check_all_declars`, configurable
Nat/String handling and quotient-checking code below the custom wrapper. That
is another reuse candidate for independent audit/checking, not evidence of
full current-Lean/Mathlib support. Removing the wrapper does not prove its
semantic correspondence. Starting a second universal checker implementation
would have lower payoff than defining an acceptance lane around the selected
Lean kernel and retaining an external checker as optional corroboration.

## One highest-payoff next step

**Select one source-only ordinary-Lean acceptance contract before another proof
backend experiment.** Specify the initial basis, allowed axioms/primitives,
inert declaration representation, exact environment binding, checked extension
entry point, persistent promotion and two distinct delivery classes. Trace one
representative ordinary Lean declaration that the existing bridge excludes
(for example a theorem using native large numerals or an explicitly permitted
quotient interface) through that contract on paper, including a hidden-axiom
counterexample and a stale-cache withdrawal counterexample.

This decides whether the broad-lane seam is genuinely small and secure before
coding. If selected, the first implementation should be that narrow acceptance
adapter plus protected local reuse, not another cryptographic guest, broad
benchmark campaign, automatic metadata-registry rebuild or receipt for V.
The software remains unfinished; a broad native lane would be a practical
coverage/local-cost advance with an explicit cold-cost compromise, not proof
of universal inexpensive global admission.
