# Abstract authoring of warranted definitions: independent decision audit

Reviewer: `admission_event_audit`, 2026-10-23. Source/theory plus saved consumer02
outcome only; no projection, compiler, consumer or native checking was rerun.
Reviewed root note ABSTRACT-AUTHORING-BOUNDARY at
`30ef1d55ef31f9200d4627e85cc28f1eea74588a2e2634a3e9f4cd5788bfda9a`.

## Decision

GO in principle for an explicit **construction-only abstract definition view**.
An existing safe axiom-shaped public handle may denote an independently warranted
ordinary definition or non-theorem opaque of the same exact type/universes and
accepted identity. It is not a new foundation axiom or receiver acceptance mode.
Do not claim exact body correspondence for that handle. No implementation or
runtime pass follows from this review.

The root note needs one precision: erasing a definition contributes no new
*delta* reduction, but it does not erase Lean's name-dispatched primitive rules.
Nat.xor can still reduce on literal arguments while its public ConstantInfo is
axiom-shaped. The correct condition is preservation of **every actually
available inference and reduction rule**, including such primitive reductions.

## Why the construction abstraction is justified

Let K be the exact independently checked receiver context. Let A be the finite
selected construction interface, not the owner's entire unrestricted environment.
Interpret each selected name by its exact accepted declaration in K. Require
preserved universe instantiation, interface types and dependent references.
Concrete declarations and generated computation rules in A must agree with K;
abstract definition handles add their types but no new delta equations.

For ordinary constant use, the interpretation is inhabited by K's accepted
declaration. Structural typing rules are preserved by substitution. For
conversion, every reduction that A actually uses must be available in K; body
erasure removes delta reductions, and preserved primitive rules retain their
meaning. This yields the usual conditional derivation-transport argument. It is
not a mechanized refinement proof of the whole Lean implementation.

More importantly, product soundness does **not** depend on trusting local
elaboration or that informal argument: exported new units must still be checked
in actual K with exact imported IDs. A failed construction or conversion must
remain a failure, never be repaired by admitting its claim. Export must continue
to close over new units and refuse unwarranted references, including sorryAx and
the forbidden native evaluator functions.

## Necessary implementation conditions

1. Apply the new view only when the actual owner record is existing, safe
   `.axiomInfo` and the authenticated accepted declaration is ordinary kind 1
   or kind 3. Never insert a new axiom or infer warrant from type/name equality.
2. Match the accepted type and universe parameter interpretation exactly using
   the existing original/legacy representations, bind every type dependency,
   and retain the exact accepted symbol/profile/context IDs.
3. A concrete owner definition or opaque still requires exact accepted semantics;
   a differing body is not abstracted away. Existing theorem-interface behavior
   is separate. Inductive/constructor/recursor kinds 4/5/6 and quotient kind 7
   cannot use this new branch; their actual computation records remain required.
4. Keep the same pinned Lean primitive interpretation and accepted foundation.
   Native literal and operator semantics, and relevant Nat/Bool/string/generated
   data meanings, must remain preserved. Same-type arbitrary primitives or
   foreign checking profiles are not allowed by this argument.
5. Record a distinct abstract-definition match kind/count. Scan its interface
   dependencies, not a fictitious owner body; do not report it as an exact
   non-theorem match or as an ordinary warranted-theorem match. Existing prepared
   closure may conservatively retain additional authenticated dependencies.
6. Keep missing declarations on the existing actual construction/checking path.
   Keep atomic candidate installation, complete group rules and independent
   successor admission unchanged. Owner bindings remain construction plumbing,
   not transferable acceptance certificates.

The pinned C++ `reduce_nat` code inspected in the previous projection review
compares the explicit head constant before dispatch, including Nat.xor. Thus
with identical primitive semantics in A and K, the axiom-shaped public view does
not by itself create a new primitive equation unavailable in K. Merely asserting
that all abstract handles are computationally inert would be incorrect.

## Alternative and recommendation

Exact body acquisition remains necessary when useful proof construction requires
delta reduction hidden by the abstract view and available laws do not suffice.
It is not necessary merely to *name* an already warranted object. Restoring a
body over an existing public handle needs a separately justified frontend
restoration/import path; it must not silently overwrite a conflicting constant
or load the entire private proof library. Prefer the narrow abstract view now,
then acquire exact semantics only at a demonstrated missing-conversion boundary.
This has direct ordinary-workflow payoff without certificate investment or
changing receiver trust.

## Saved consumer02 outcome: safe failure, not a projection failure

Operation: `experiments/v5-local-checks/ordinary-owner-consumer-02`.

| File | SHA-256 |
|---|---|
| selection.json | `e0446ace7b6d748b6580e3bd462834156263f5a69aff346c5074b367622be7b8` |
| RESULT.json | `e3cffb061a209f46d404619cc2828ebdf309fd65b39ef2f3ddc739fdad159824` |
| PREPARE-RESULT.json | `09477faa163f9e2a6071d479552367650a41ac13218f70d66f8159740cb04d23` |
| projected header | `3d446d8694be75c222058d751f83e635f1434ba1d46d7b1453c2cf14f8844f4a` |
| consumer.stdout.txt | `dd8b364446c2e5dc50a27820ccef499cf3b87fd4303ba475a0ca8f6133b1e85a` |

Read-only file examination confirms 316 selected basis rows, 265 omitted names,
4,549,204 total request bytes and all 387 group files byte-identical to the
adopted original request. Every new request file matches its saved length/hash;
the three accepted identities are unchanged. The saved projection reports
212535 scan nodes. No projection algorithm was rerun by this review.

The first native refusal is needed `Nat.xor` at the same non-theorem basis-screen
boundary, before acquired-group checking or installation. Later unknown-name
diagnostics and NO_LOCAL_BOUND_CONTEXT are cascades. No compiled consumer,
successor-export file or successful consumer result exists. The saved outer
report shows clean child exit 1/Job closure, no cleanup errors or termination
request, 6.234375 s Job plus 0.46875 s wrapper CPU (6.703125 s known total),
10.7417557 s wall and 911867904 bytes peak Job private commit. Preserve and charge
this attempt. It demonstrates a relevant hidden-body usability boundary; it
does not authorize omitting Nat.xor, weakening K or retrying unchanged inputs.
