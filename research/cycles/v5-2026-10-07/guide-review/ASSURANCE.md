# Candidate v5 guide: mathematical acceptance and assurance

Documentation-only synthesis, 2026-10-08. Independent reviewer:
`/root/v4_oct7_assurance`. This note explains the candidate architecture, not a
completed v5 release. No runtime, proof-result audit, product change or Git change
was performed. Background proof71174 is deliberately not inspected; its latest
adopted status remains the historical observation in [PAUSE-HANDOFF](../PAUSE-HANDOFF.md).

## 1. The shortest accurate explanation

A node does not trust a theorem because another node says it is true. It verifies
a certificate that commits to an exact mathematical module under an explicitly
adopted checker, foundation and semantic policy. It can then authenticate selected
declarations from that module without downloading the proofs of all earlier
theorems. To write a new proof, it may still need the definitions, types and
computation rules that the new proof actually uses.

Three objects must stay separate:

| Object | What it contains | What it establishes |
|---|---|---|
| Module specification | Exact declaration interfaces, definition-body commitments and complete inductive-group metadata | An immutable mathematical identity; a hash alone proves no mathematical validity |
| Checking witness | New proof/value terms, selected imported declarations, demanded bodies and parent conclusions | Material a checker can examine; possessing it is not acceptance |
| Resolved certificate | A cryptographic receipt with the exact public module conclusion | Conditional on the adopted assurance assumptions, existence of a successful check with its imported premises discharged |

Search results, saved status JSON, custody records, native diagnostics and proving
checkpoints are not additional forms of mathematical authority.

## 2. Exact identity and the current certificate statement

Write a module summary as `S = (schema, F, P, n, R)`: foundation ID `F`, semantic
policy ID `P`, group count `n`, and canonical Merkle group root `R`. The current
codec computes `M = H("module-spec", canonical(S))`, using domain-separated
SHA-256 framing. Each committed group contains exact descriptors and structured
names. This is exact structural identity, not an algorithm deciding whether two
arbitrary mathematical theories are equivalent.

Local references are encoded relative to their own module before hashing; after
hashing, they become names beneath `DMKN.Mod.<M>`. External references carry their
owner ModuleID and structured relative name. Thus two independent modules may
both display a name such as `Tree` without creating one mutable global name, and
the construction does not require solving a self-referential hash equation.

The current public journal is **DMKNM002, profile2, exactly184 bytes**:

`J = (magic, profile, image, F, P, M, R, n, rank)`.

It contains **no whole-witness digest and no source-file digest**. Its intended
meaning is existential: there exists a successfully checked witness for this
exact module and conclusion. Two valid proofs of the same theorem may preserve
ModuleID; they need not preserve parent choices, receipt bytes or rank. The
certificate therefore does not attest that an arbitrary separately supplied proof
file, source file or provenance claim was used. Host-side immutable input hashes
remain necessary operational bindings without becoming public mathematical identity.

Image identity is also separate from ModuleID. The semantic policy describes the
meaning of declarations, while local adoption pins the implementation that checks
them. Upgrading an image does not automatically authorize old/new-image mixing:
current parent checks require exact image, foundation and policy compatibility.
Semantic-policy changes can change ModuleID even if human-facing names look equal.

The rank is zero without module parents and exactly one plus the maximum parent
rank otherwise. Arithmetic overflow refuses. No module may use its own ModuleID
as an imported parent. Strict rank descent makes a finite dependency-induction
argument possible, but rank is not a proof of validity by itself and is not part
of the module's mathematical identity. Where a child uses a parent conclusion,
the complete selected journal matters, not merely its ModuleID.

Sources: [journal.rs](../../../../software/v5/modules/receipt/src/journal.rs),
[policy.rs](../../../../software/v5/modules/receipt/src/policy.rs),
[codec.py](../../../../software/v5/modules/codec.py),
[receipt README](../../../../software/v5/modules/receipt/README.md).
Earlier216-byte/profile1 descriptions in historical notes are superseded, not
alternative formats accepted by the current profile.

## 3. What the mathematical relation checks

For finite imported groups `I`, ordered new local groups `L`, and witness `W`, the
implemented relation derives its conclusion from the supplied data; it does not
accept a caller's `verified` flag or caller-chosen imported/new role.

Its essential obligations are:

1. Parse the bounded exact input and match the adopted foundation. The current
   foundation is a narrow22-declaration,413-row, no-declared-axiom foundation,
   not all Lean or Mathlib. “No declared axioms” does not remove the underlying
   type theory, checker or implementation assumptions.
2. Recompute the local summary/ModuleID and verify each selected imported group
   opening against its exact compatible parent journal. Bind real body bytes to
   their committed canonical expressions, rejecting duplicate/unused openings.
3. Match those canonical descriptors to the **same native rows** that will be
   checked. Derive role assignments from this correspondence. A certificate for
   one descriptor must never authorize a different checker declaration.
4. Reconstruct an immutable environment. Imports precede locals; ordinary local
   declarations retain earlier-declaration visibility, while each complete
   inductive block has its carefully delimited mutual visibility.
5. Check every new local declaration and every new complete inductive group.
   New axioms, new quotient primitives, unsafe/partial declarations and missing
   new values are refused by this policy. Exact authenticated imported groups
   may skip redundant original-body checking because their validity is a premise.
6. Return the computed journal and all exact parent-journal premises. In the
   guest, every premise becomes an actual recursive verification obligation.
   Only a fully resolved final receipt can discharge them for cold acceptance.

A native preflight runs the conditional relation but does not discharge those
cryptographic premises. “Conditional check passed” is consequently weaker than
“module certificate accepted,” even when the native checker code is identical.

Sources: [relation.rs](../../../../software/v5/modules/receipt/src/relation.rs),
[guest entry](../../../../software/v5/modules/receipt/src/main.rs),
[conditional module checker](../../../../software/v5/modules/native/checker/src/module.rs),
[row correspondence](../../../../software/v5/modules/native/checker/src/module_correspondence.rs).

## 4. Different mathematical objects require different reuse rules

| Declaration | Original contribution | Later reuse |
|---|---|---|
| Theorem | Check its proof against its exact proposition | Authenticate the certified proposition; the imported theorem proof can remain absent |
| Transparent definition | Check and commit its exact type, body and reduction hints | Preserve Definition kind/hints; retrieve its committed body when conversion needs it |
| Opaque value | Check its original body and commit the type/kind/body identity | Preserve opacity; downstream conversion does not unfold its private implementation |
| Inductive group | Check the entire type/constructor/recursor group and its rules | Authenticate a complete group, not an arbitrary constructor or recursor on its own |

The theorem shortcut has a specific justification: a certified `Prop` proof can
be represented by a sealed proof interface under the supported proof-irrelevance
semantics. The revised checker retains theorem kind and a `SealedProof` slot;
it does not grant arbitrary new axioms. This narrow argument cannot be extended
to erase computational definition bodies or invent recursor rules.

Missing data is not a mathematical answer. An unavailable imported declaration
or transparent body produces `NeedDeclaration`/`NeedBody` or refusal, never a
default term, false equality answer, axiom, or silently opaque definition. Fetching
exact demanded material may allow a fresh immutable reconstruction and retry.
Previous attempts count against the original budget. A timeout is not evidence
that the proposition is false.

Two costs are therefore distinct:

- **Proof-history cost:** replaying how every imported theorem was originally
  established. Resolved recursive certificates are intended to avoid this.
- **Semantic dependency cost:** reading and computing with types, definitions
  and rules actually demanded by a new proof. Certificates do not abolish this.

A demanded semantic dependency owned by another module may require that owner's
own resolved certificate and group opening, but not that certificate's proof
ancestors. Demand closure may still be large. Repeated reconstruction can repeat
work; sound missing-data handling alone is not a speedup theorem.

Sources: [ValueSlot/environment](../../../../software/v5/modules/native/checker/src/env.rs),
[module relation design](../MODULE-RELATION.md),
[native preflight API](../../../../software/v5/modules/native/PREFLIGHT-API.md).

## 5. Why a receipt is not automatically a theorem about Lean

The assurance argument has two different implications:

`accepted receipt -> successful execution of the adopted relation`

`successful relation, with grounded valid premises -> valid module under F/P`.

The first needs the concrete cryptographic construction, verifier, compiled
image and recursive composition to be sound. The second needs the mathematical
checker and all descriptor-to-kernel translations to implement their intended
semantics. A perfect proof of a buggy checking program faithfully proves the
buggy program ran; it does not repair the program.

Current receiving code accepts only the selected real succinct Poseidon2 receipt
form, disables development mode, verifies the **full application claim**, and
checks the expected image and exact journal/module binding. Successful halt and
empty remaining assumptions are required. An `env::verify` call inside the guest
records an obligation that later recursion/resolve must discharge; calling it is
not itself a finished certificate. Fake/dev, unresolved, wrong-image or wrong-
profile receipts do not become valid because an output file says they passed.

The concrete trust case still includes:

- Canonical encoding, hashes, namespace relocation, raw-row correspondence,
  universe/binder preservation, atomic groups and imported-proof substitution.
- The modified Nanoda checker, rooted in the pinned0.4.19 source, and its scoped
  correspondence to the selected Lean4.34 frontend. There is no completed
  universal equivalence proof for all Lean/Mathlib constructs.
- The actually accepted RISC0 verifier parameter/control-root set, SDK/circuit
  implementation and adopted guest image. Honest producer settings do not alone
  restrict everything a malicious prover could submit to a broader verifier.
- Adaptive, branching, multi-claim recursive soundness over an explicit finite
  security horizon. Rank descent does not replace this cryptographic assumption;
  ordinary one-shot soundness is not automatically a theorem for arbitrary joins.
- The trusted local owner process, adopted installation, operating system and
  selected runtime dependencies. Current Windows Jobs supervise resources and
  cleanup; they are not a hostile-code sandbox.

Engineering evidence can combine precise arguments, source review, adversarial
regressions and independent differential tests without mechanically proving every
implementation line. It must state this honestly. Exact upstream audit/advisory
coverage, broader checker correspondence and a usable adoption/revocation/update
policy remain release obligations; do not invent a numerical security level.

Sources: [prior assurance reasoning](../ASSURANCE.md), especially “Exact existing
acceptance chain” and “Checker correspondence”; [host03 source](../../../../experiments/v5-local-checks/module-host-build-03/source/src/bin/module_host.rs),
functions `checked_receipt` and `receive`; [admission bindings](../../../../software/v5/admission/bindings.py).

## 6. Live handles bridge verified bytes to local authoring

`ReceiptVerifier.receive` runs the owner-adopted real verifier on immutable receipt
bytes, then checks exact output binding, unchanged runtime, deadline and clean
whole-process closure. Only afterward does it register a `VerifiedModule` object
in its private in-memory registry. Creating a lookalike object or reloading a JSON
report does not place it in that registry. These are API safety boundaries inside
a trusted owner process, not protection against an attacker executing arbitrary
Python in that same process.

`describe` and `open_group` require that exact live originating verifier and handle.
The latter authenticates the selected declaration group against the already
accepted module summary. Closing or expiring the verifier revokes its handles.
Stored receipt bytes are reusable data; stored acceptance flags are not authority.

`ImportSession` is tied to one exact supported live verifier and a deadline no
later than the original workflow/verifier deadlines. It holds exact receipt
copies, selected groups and demanded bodies. Cache hits recheck liveness and byte
identity; one module gets one selected exact parent journal in that operation.
Different receipts/ranks for the same ModuleID are not silently merged.

`SourceOperation` preserves that session and verifier identity through preparation
and its one-shot finish. The ordinary Lean frontend reconstructs the exact imported
context. For elaboration only, theorem/opaque interfaces are represented by exact
registered assumptions; transparent definitions use their committed bodies and
complete inductives are regenerated through Lean's checked construction and compared
exactly. Fresh exported axioms and unsafe declarations refuse. Those authoring-only
assumptions cannot themselves certify a new module.

The returned child request is deliberately **untrusted**. It may outlive the old
session only because the host/guest independently reverify the real parent
receipts and all new local obligations. This separates convenient authoring from
the final acceptance boundary.

Sources: [verifier.py](../../../../software/v5/admission/verifier.py),
[imports.py](../../../../software/v5/authoring/imports.py),
[source.py](../../../../software/v5/authoring/source.py),
[native02 frontend](../../../../software/v5/authoring/native02/AuthorLean.lean),
[import/authoring contract](../VERIFIED-IMPORT-AUTHORING-CONTRACT.md).

## 7. Hybrid native deltas: a proposed cost mechanism, not shipped authority

The [delta-frontier design](../DELTA-FRONTIER-NATIVE-SEAM.md) proposes allowing a
receiver to verify real certified frontiers and then natively check a bounded DAG
of new unsealed proof witnesses above them. Its induction is straightforward only
if each checked delta's **actual returned parent journals** already belong to the
verified frontier or previously checked deltas. The target's complete uncertified
closure must accompany the packet; claimed graph edges or saved success flags
cannot replace that check.

Its whole closure must be bounded by aggregate bytes, nodes, edges, bodies,
receipt verifications and actual CPU/wall/memory. Bounding depth alone does not
bound a high-fanout DAG. Shared nodes should be processed once. When this closure
becomes too expensive, a new certificate can compress a selected frontier for
future consumers. There is no unlimited cheap chain with fixed cold work and no
periodic sealing cost.

This remains **a proposal, not an implemented v5 receiving path**. Host03 does not
contain the proposed native-relation checker. A future `VerifiedDelta` must be a
different authority class from certificate-backed `VerifiedModule`; current
certificate-parent APIs must not accept it. Current profile2 guest can certify a
child only over genuine receipt parents. Compressing a whole unsealed DAG in one
seal requires a separately justified aggregate relation or explicit repacking;
it is not already provided by the existing guest.

## 8. What is evidenced, and what remains open

The adopted pause checkpoint records a real profile2 guest build/image and a
successful retained base execution capsule, plus five retained cryptographic
proof checkpoints. It also records a compiled/linked ordinary-source frontend
with five conditional native controls, and completed worker/preparation controls
(20 and9 respectively). The latter suites mock native work and mint no positive
module handles. This documentation turn does not inspect later proof output and
therefore makes no new claim about a final base receipt or cold acceptance.

The following are central gaps, not qualifications that make v5 complete:

1. Independently adopt the actual current-profile terminal proof outcome, then
   demonstrate genuine cold admission, live ordinary-source reuse, parent-aware
   child production and cold reciprocal receipt use through public APIs.
2. Complete the checker/Lean and concrete recursive-cryptography assurance case,
   including changed-boundary attack controls and actionable policy updates.
3. Make the full discovery/acquisition/import path work at bounded local cost;
   authenticate semantic dependencies without secretly requiring global search
   or complete ancestral-proof replay.
4. Implement the hybrid frontier path if adopted; compare actual whole-workflow
   costs rather than advertising the proposal as a deployed optimization.
5. Demonstrate justified useful-growth benefit against an equally endowed,
   optimized local-reuse baseline, including production, service, failure,
   retention and consumer costs. Validity alone proves neither novelty nor
   usefulness, and no architecture guarantees exponential mathematical discovery.
6. Finish availability/recovery, independent public installation/operation,
   hostile-input containment, exact release artifacts, rights/license choices
   and release/update policy. These are the six open release obligations in
   [PLAN](../PLAN.md), not extra requirements introduced by this note.

## Guide review checklist

- Never equate native diagnostic success, a snapshot or a proof checkpoint with
  an accepted resolved module certificate.
- State the184-byte existential profile2 statement; do not revive the removed
  witness digest or treat a certificate as source provenance.
- Separate mathematical ModuleID, semantic policy, verifier adoption and rank.
- Separate proof ancestry from genuinely demanded computation/semantic data.
- Explain that hashes and index membership authenticate identity/membership,
  not validity, novelty, usefulness or global coverage.
- Label native deltas and arbitrary-DAG sealing as proposed, not implemented.
- Report the historical pause observations as historical, without polling the
  background proof or predicting that its finite allocation must succeed.

The candidate architecture is technically substantive, but the broad deployable
v5 objective remains unfinished. Documentation does not change its status.

## Full-guide review, 2026-10-08

Read the full932-line `notes/V5-ARCHITECTURE-GUIDE.md` draft, observed SHA256
`07c0e9980b592f3640fea238f751863ca90dc62f304bb0dac28632b1c8d1a859`.
Disposition: the main architecture, mathematical statements and implementation
status are appropriately qualified; no architectural contradiction or new
mathematical overclaim found. The guide covers the complete local-agent loop,
validity/discovery/custody boundaries, two core scale/growth objectives, meaningful
comparators, operational trust, update policy and open release obligations.
Its existential184-byte journal, rank/DAG caveat, semantic-versus-proof-ancestry
cost decomposition and expressly unimplemented native-delta route match sources.
Growth inequalities are conditional accounting arguments, not evidence of demand
or a claimed exponential-discovery theorem.

Sent root three necessary explanatory corrections before finalizing:

1. Section5 must distinguish the **sealed Prop theorem interface**, whose scope
   depends on the supported proof-irrelevance semantics, from an **Opaque data
   declaration**, whose original body is checked/committed but not unfolded by
   downstream conversion. The existing “Opaque theorem interfaces” heading
   alone risks conflating these central reuse mechanisms.
2. State the concrete current receiving gate: real Succinct/Poseidon2 only,
   development mode disabled, full successful application claim with empty
   assumptions, exact independently adopted image and profile2 journal/module
   bindings. Explain that guest env::verify creates a recursive obligation;
   only final resolution/verification discharges it.
3. Section7's authoring assumptions cover imported opaque interfaces **as well
   as theorems**. Keep the explanation that these are local elaboration devices,
   never newly admitted axioms; the final relation retains the correct kinds.

Optional wording correction: content addressing *identifies and permits
coalescing* exact duplicates; it does not itself remove replicas or equivalent
but differently encoded mathematics. Root owns the guide and all edits. Scale
lane owns the remaining discovery-specific additions. No experiments, proof
polling, terminal-result adoption, product edits or Git operations occurred in
this review. Review completed; stopping after transmitting these findings.
