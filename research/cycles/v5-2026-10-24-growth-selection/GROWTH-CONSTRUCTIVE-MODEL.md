# Consumer-native evidence: share a solver's results without importing its world

2026-10-24. `growth_constructive_model`; source/theory-only investigation.
No implementation, executable input, installation, experiment or Git mutation.
This is an architectural option for review, not an implemented v5 capability or
a claim of measured mathematical growth. Companion: GROWTH-OPPORTUNITY-CHOICE.

## Decision

For suitable mathematical families, consider **consumer-native witness exchange**
before exporting a producer's general theorem-library closure. An agent chooses
a formal problem locally. Another participant can apply a sophisticated,
untrusted solver and return finite inert evidence. The consumer checks that
evidence with an already warranted local verification interface and constructs
its own proof of the result. The producer need not prove its search algorithm
correct, expose its tactic dependencies, or produce a cryptographic certificate
of the computation.

This is the established proof-producing/verified-certificate-checking pattern,
not a new cryptographic invention. The potentially consequential architectural
change is **where we place knowledge and evidence**. A reusable method need not
always cross the network as a library to be installed before use. It can remain
in independently operated search software while its successful answers cross
as evidence that the recipient's existing mathematics already knows how to check.

Keep ordinary theorem/package sharing for cases where this pattern is unsuitable.
It cannot cheaply turn every arbitrary Lean theorem into a short certificate.
Do not build a general remote-solver protocol merely because the model is sound.
First identify one worthwhile family and an existing checker/provider route.

## What this adds to the previous arguments

The inspected prior notes already supply resource-bounded capability semantics,
method/bridge factorization, complementarity, selected-output validation,
rent-or-buy, bounded fallback, and fair comparison with ordinary package sharing.
No part of this note renames those results as a new growth theorem.

Their predominant interchange unit is a theorem/method and its required semantic
or proof dependencies. Here the supplier's method can be **unwarranted executable
problem-solving knowledge**: it proposes witnesses, not premises. Each accepted
answer obtains a new local warrant from the consumer's fixed relation. This can
remove a large producer dependency closure from a particular use. It is stronger
than trusting a remote success bit and cheaper in some cases than proving the
supplier's entire computation, but the actual witness must justify that claim.

The user still chooses investigations independently. A private, optional request
to a selected provider is not a network-wide task list, shared root goal, or a
human-intention input to mathematical acceptance. A human-readable description
is unnecessary at the protocol's mathematical boundary.

## Formal interface and trust boundary

Fix a receiver's genuinely warranted environment K and checking policy P. In K,
assume an exact supported problem type X, certificate type C(x), proposition R(x),
a computable predicate V, and a warranted theorem

```text
V     : (x : X) -> C(x) -> Bool
sound : forall x c, V x c = true -> R(x).
```

All parameters, dimensions, number representations and interpretations are part
of these actual definitions. A printed formula or equal declaration name is not
an environment identity. The receiver has selected x before interpreting the
answer; a provider may not substitute an easier x' and present it as that answer.

The mathematical request consists of the required exact interface/profile and
input x. A provider returns c. It may search, use machine learning, execute foreign
libraries, consult humans, make mistakes, or refuse. None of those actions grants
mathematical authority. The response is inert bounded data, not Lean source,
an executable tactic, an arbitrary import path, or a compiler-success report.

Local validation must obtain a real checked proof e of `V x c = true`, and check
`sound x c e : R(x)` under P. Merely running an external checker binary that says
true does not supply e. Kernel reduction, or a justified reflected computation
whose result is itself checked, can supply it. The allowed axiom policy and actual
evaluation path still matter; do not insert a new unchecked evaluation axiom.

### Proposition 1: the consumer-native evidence cut

Assume (i) K and sound are warranted under P; (ii) input/certificate decoding and
binding produce the actual well-typed x and c; (iii) local verification really
checks e and `sound x c e`; and (iv) the validator, K and evidence are protected
against tampering during the operation. Then acceptance warrants R(x), independent
of the producer's search algorithm, library history or asserted identity.

**Proof.** By (iii), K derives `e : V x c = true`. By (i), K derives sound with the
displayed dependent type. Two argument applications and application to e yield
`K |- sound x c e : R(x)`. Assumptions (ii) and (iv) bind that judgment to the
actual selected request and retained acceptance. No premise mentions the producer
or its research history. A false candidate either fails local validation or
violates one of the stated checking assumptions. This is the ordinary reflection/
soundness pattern, not a new proof of Lean or of a particular implementation.

The local cost can consequently be decomposed as

```text
input formation and binding + certificate acquisition/decoding
+ verified predicate evaluation + final proof construction/kernel checking.
```

There is no mandatory term for replaying the solver's private search history.
The input, certificate and verification computation may still be large. A bound
on abstract arithmetic operations is not automatically a bound on Lean reduction,
integer bit complexity, parsing, memory or resulting proof size. A concrete
checker needs these separate implementation bounds.

This is not free cold onboarding: K, V and sound must already be warranted or be
adopted through the receiver's explicit assurance route. Sharing an unchanged
verifier across many requests can amortize that investment; assigning it zero
cost or silently trusting a foreign compiled module would invalidate the claim.

## Endogenous investigations and recursive accumulation

Let a local agent choose its next x from its own history, including previously
accepted results, failures and discoveries. There is no need to assume a fixed
global sequence of problems or stationary demand. The correctness argument
above applies to each actual request. If a new response becomes a premise of
later work, it does so through its locally warranted proof, not a provider label.
Induction over actual sound extensions therefore preserves the checking boundary
for an adaptively chosen finite investigation.

What may grow is the set of **affordable available procedures and warranted
answers**, not the unrestricted deductive closure. A better solver may now find
certificates for inputs on which previous affordable strategies failed. A useful
new verifier relation may admit an entire different witness family. An accepted
answer can enable a new investigation. These are distinct effects:

| Contribution | What it changes | What it does not establish |
|---|---|---|
| An exact successful input/witness pair | Available warranted answer for that exact problem; later replication/recheck possible | A general solver, novelty, or usefulness to other inputs |
| Better untrusted solver/search policy | A potentially larger practical certificate-production frontier | Truth of its claims without checking; a proved superiority bound |
| A warranted reusable verifier and soundness theorem | Which independently produced evidence can safely establish which results | Existence or cheap production of witnesses |
| A checked reduction from another problem family | Applicability of existing verification machinery to additional local problems | A free reduction, or correctness of a name-only translation |

A count of successful requests is not a growth measure. Repeating cached answers,
splitting an input into aliases or selecting only newly easy examples can inflate
it. For a declared request history, compare equal verified results and all costs.
For adaptive research, prescribe the initial resources and continuation policies
before comparison; acknowledge that the two histories may select different later
problems. A fixed-task speed comparison and an expanded-opportunity claim are not
interchangeable. Neither requires a system-wide usefulness score.

## A service is not yet accumulated mathematical knowledge

An API that can disappear with one operator is insufficient for the commons.
Separate the generating service from durable mathematical artifacts. Preserve
the exact input, certificate, verifier/profile identity and local result binding
when publication/retention is chosen. Another holder can serve those same inert
bytes, and another consumer can verify them independently. Do not retain only a
URL or a past `accepted=true` flag. Conversely, retaining certificates does not
reconstruct the unavailable algorithm's capacity to solve new inputs.

### Proposition 2: exact-answer substitutability

Fix an immutable verifier/profile interpretation and exact input x. Suppose an
acquired certificate c has the same bytes/interpretation regardless of its
holder, and the consumer performs the validation in Proposition 1 against its
own x and warranted K. Replacing the generating provider by any other holder of
c preserves the resulting mathematical acceptance judgment.

**Proof.** The local term, evidence interpretation and checking environment are
unchanged; the provider is absent from that judgment. Transport authenticity
serves the byte-binding premise, not a claim that the holder knows mathematics.
The same reasoning allows a different candidate c' from a different solver, but
c' must pass its own validation. No proof or trust flag is inherited from c.

Thus exact-answer custody and solver replacement are different interfaces. The
former can reuse existing immutable custody. The latter needs the same supported
mathematical request semantics, available compute and possibly different methods.
Neither needs a globally synchronized registry or all nodes to store every answer.
Provider independence and retention still require operational evidence.

Only exact instance reuse follows here. Semantically equivalent problems require
an actual checked transformation, not an unsafe cache key based on similar text.
Instances that share no expensive work may be better recomputed than indexed.

## Whole-cost choice: use this route only where it removes real work

For each receiver, compare three actual options: an already available local solver;
adopting a compatible ordinary package/method; and requesting/acquiring a certificate
then checking it locally. Permit ordinary sharing the same solver and witnesses.
This model justifies an interoperable capability, not unique superiority of our
transport over Git, HTTP, an editor integration or an existing proof-producing tool.

Charge solver development/setup, all requested and failed searches, provider CPU,
queues, response construction, network, verifier adoption, local computation,
retention/repair and maintenance. Producer cost moves, it does not vanish. Remote
service can be attractive when adoption of large or unapproved executable tooling
is the obstacle and evidence is small. Repeated cheap local solves can instead
make local installation best. A witness as hard to produce or check as a full
proof supplies no miracle. No additional economic theorem is needed to assert
these comparisons; the prior full-cost and investment models already apply.

The companion opportunity note supplies the concrete rational optimization
witness construction. It is useful because witness checking can avoid the
optimization search trace, not because remote computation is intrinsically faster.
Its arithmetic/bit/resource assumptions must survive the ordinary-solver comparator.
It also identifies a stronger accumulation route: a checked dual vector can give
a uniform bound under varying right-hand sides, and an appropriate checked active
basis can give an affine optimizer on an explicit parameter region. Such a
certificate-derived parametric theorem is reusable mathematics, not only an RPC
answer cache. Generalization is justified by the actual parametric proof, never
by extrapolating from a few successful instances. Ordinary sensitivity analysis
and basis reuse must receive the same credit in the comparator.

## Concrete architecture consequence and stopping rule

Treat **mathematical evidence interfaces** as possible integration boundaries,
alongside ordinary packages and exact theorem bundles. Do not make every new
useful algorithm carry its executable dependencies into every receiver. Existing
local contribute/intake/checking operations may supply parts of the output path;
the present native-first facade is not already a tested remote-witness service.

The smallest next decision is source-only: for one substantive witness family,
identify the existing local verifier, exact soundness theorem, supported data
representation, actual input binding and ordinary alternatives. If those exist,
decide whether the missing software is just a small data adapter or already an
existing tool. If absent, estimate verifier-adoption/maintenance cost before
inventing a new solver, protocol, global index or benchmark.

Queries can disclose unpublished mathematical data. Remote dispatch must remain
an explicit local choice; discovery of a candidate must not automatically send a
private goal elsewhere. Client/provider quotas and hostile-data limits remain
necessary. Refusal/timeout does not grant a new search allocation. Compatibility,
kernel safety and service availability are separate gates.

Stop this direction if certificates are too large, actual evaluation is too
expensive, useful cases require unsupported assumptions, a standard local tool
already gives the same benefit cheaply, or no nontrivial adoption friction
survives the comparator. Do not add remote-service machinery just to demonstrate
that a valid witness verifies. The central question is whether the capability
becomes affordable and usable for independently chosen work.

## Sources and deduplication

- `v4-2026-10-02/PHILOSOPHY-OF-GROWTH.md`: resource-bounded capability and the
  distinctions between truth, access and usefulness.
- `v4-2026-10-06/GROWTH-MECHANISM.md`: method families, certified cuts,
  rent-or-buy, direct-route protection and complementarity. These are reused,
  not claimed as new contributions here.
- `v5-2026-10-22-native-library/GROWTH-FIRST-ARCHITECTURE-DECISION.md` and
  `GROWTH-COMPARATOR-CHALLENGE.md`: method/bridge argument, ordinary-sharing
  comparison, advice-erasure and causal limits.
- Current cycle `GROWTH-DECISION.md`, `BRIDGE-INVESTMENT.md`: selected endpoint
  checking and ordinary named consumer bridges.
- `software/v5/ordinary_native_package/README.md` and native-library
  `ABSTRACT-AUTHORING-BOUNDARY.md`: current public surface and distinction between
  authoring assumptions and actual receiver warrants. No new runtime was inferred.

No external scientific source was newly retrieved. The two propositions are
elementary derivations stated in full, not claims of a novel general theory.
