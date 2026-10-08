# CP-001E: independent foundation-source cross-audit

Review dates: 2026-09-19–20. Status: bounded, read-only source and release-history audit. No code was implemented, no exploit was executed, no checker was built, and no native replay or test suite was run. CP-001D remains frozen.

## Scope and conclusion

This review independently checks selected claims supporting the [foundation security audit](../analyses/CP-001E-foundation-security-audit.md). It does not establish that the entire selected release is secure, that its compiled binary corresponds to its source, or that the proposed native import adapter has been qualified.

The proposed Lean v4.34.0 source contains the inspected post-v4.22 fixes, including the release-branch backports of PR14806 and PR14807. Their original master merge commits need not be ancestors of the release: the exact backports are. Follow-on PR14843, which applies the `is_prop` correction in the inductive-reduction helper, is also present. The specified mathlib revision selects the same Lean version.

This is sufficient to correct a mistaken claim that these particular fixes are absent. It is not sufficient to certify the new foundation. Source-version qualification, native-name/bootstrap compatibility, host representation, build identity, complete checked reconstruction, resource isolation, and the actual mathematical checking boundary remain separate obligations.

Lean4Lean is valuable additional checking and metatheory work, but the inspected revision is neither an automatically independent implementation nor a complete end-to-end verification of our proposed native inductive profile. Its own README qualifies implementation independence; its toolchain is different; its declaration-verification theorem still has an inductive-case proof placeholder; and its proof development states additional implementation assumptions explicitly.

## Evidence method

The reviewer read official GitHub API release refs, pull-request descriptions, candidate-branch file history and compare results, and immutable raw source at the exact commits below. Source inspection was targeted to the properties enumerated here, not an exhaustive review of every relevant implementation path. Historical PR descriptions are maintainer claims about the reported defect and repair; observed source checks and ancestry are separately identified.

GitHub's compare API reported `status = ahead`, `behind_by = 0`, and `merge_base_commit.sha = base` for each backport comparison recorded below. This establishes the reported ancestor relation in that repository history. The source inspections additionally guard against treating ancestry alone as proof that code has not subsequently been reverted.

## Exact release and library selection

| Artifact | Independently observed source selection |
|---|---|
| Lean tag `v4.34.0` | Commit `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b` |
| mathlib tag `v4.34.0` | Commit `5ed2965256430c3649e86755f9576b54eca72435` |
| That mathlib commit's `lean-toolchain` | `leanprover/lean4:v4.34.0` |
| Lean4Lean inspected separately | Commit `8223d223ed98661882e95d9d6a7126df7097cd76` |
| That Lean4Lean commit's `lean-toolchain` | `leanprover/lean4:v4.33.0-rc2` |

These are source selections, not built-image identities. Agreement between a library toolchain file and a Lean release tag does not prove that our proposed export/import representation can round-trip that library, nor that the library and its dependencies have been successfully rechecked under the proposed axiom and native-operation policy.

## Exact release backports and inspected effects

| Upstream change | Candidate-release ancestor | Source/history observation |
|---|---|---|
| PR14806, pair-keyed definitional-equality success caching | `a221d8246f8d953fa6bd9b170762ab81d53445c3` | Cherry-picked from `d108aae3bf7edbaf705b71c01ddb3b264ef72c44`; candidate is 11 commits ahead in the comparison. |
| PR14807, require a genuine sort in `is_prop` | `4576c1cf62ed2b4a4fc1cd2e19e53f1a4a97113e` | Cherry-picked from `7412bc4c852c9a9fafa69b67a11e4bf9f5dcbc24`; candidate is 10 commits ahead. |
| PR14843, carry that `is_prop` correction into `inductive.h` | `c740e4df1984194a84edf4b715bb49daa08a9c14` | Cherry-picked from `dea8490d55aeb88cbc792497652e0e9b155c28ca`; candidate is 8 commits ahead. |
| PR14849, bound kernel-computed natural-number sizes | `bf8db3df0fb28cb6a24625796bc32ab4a01e9458` | Cherry-picked from `44a3664c18cd5ca21e7806c2cd618c36cb21c2a2`; candidate is 6 commits ahead. |
| PR14632, harden local kernel invariants including projection-index conversion | `393d38abb065d369a8a84b5a3da1f4da2e8517ad` | Original merge is an ancestor; candidate is 65 commits ahead. |

The four earlier fixes were also independently compared against the candidate: PR14613 `17dbc815cf3055e73a9e37d854b8427dc1e9c46c`, PR14577 `a39eab69e1eee9ad38f4efe507907b1026a77808`, PR14616 `35f696862cdd30727a343356102af696803d91d4`, and PR14621 `448dc4441e76a0b17404e7d41a1a13dbb1642933` each returned an ancestor relation with zero commits behind. At candidate `inductive.cpp:1222`, the temporary-prefix guard covers both constant and projection names; at lines 1315–1323 the substituted nested applications are checked in the restored environment; at lines 1333–1346 restored constructor types, recursor types, and rule right-hand sides are checked. These source blocks support the root note's bounded inclusion claims, not proof of complete nested-inductive soundness.

The historical pin `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` was separately inspected: `type_checker.cpp:348` returns the syntactic comparison `whnf(infer_type(e)) == mk_Prop()`, and `inductive.h:70` uses the corresponding syntactic comparison. At old `type_checker.cpp:1224`, the string construction name is `String.mk`. This verifies the reported source differences independently; no complete old-protocol exploit was instantiated.

### Definitional-equality history dependence

At candidate `src/kernel/type_checker.cpp:960`, `succeeded_before` looks up the actual expression pair in `m_success`, with an order determined by expression hashes and both orientations checked when hashes tie. At line 972, `cache_success` inserts the actual pair. The inspected implementation is not the former union-find transitive-success cache.

PR14806 explains a subtle distinction that the project should retain: the specified definitional-equality relation can be transitive while a sound but incomplete decision procedure is not a transitive Boolean test. A cache can contain only mathematically justified equalities and still change an algorithm's observable outcomes in ways that break another component's assumptions. The reported failure occurred in recursor construction, which required consistent answers across repeated classification queries.

Consequently, the native integration contract must state the invariants consumed by recursor/declaration construction; “each cached pair is a valid equality” is not by itself a sufficient correctness argument for the entire construction algorithm. This source inspection verifies the intended pair-cache mechanism, not a theorem of order independence for every complete checker execution or cross-environment cache reuse.

### Proposition recognition and inductive reduction

At candidate `type_checker.cpp:383`, `is_prop(e)` uses `ensure_sort(infer_type(e))` and then `normalizes_to_zero(sort_level(s))`. These are two distinct protections: require a sort rather than silently returning false for a stuck non-sort, and recognize level expressions denoting zero rather than only syntactic zero.

At candidate `src/kernel/inductive.h:62`, `to_cnstr_when_structure` receives an `is_prop` callback; line 71 calls it before eta expansion. At `type_checker.cpp:399`, the recursor-reduction call supplies the corrected `is_prop` function. This independently confirms the follow-on PR14843 path, not just the primary PR14807 edit.

The review does not independently replay the reported proofs of `False`. The reported exploitability and independent-checker behavior in PR14806/14807 remain attributed to those official reports. In particular, one must not conflate “another implementation rejected one historical bad input” with general soundness or compatibility.

### Projection-width issue is corrected in the candidate

Issue12746 remained open when read, but its issue status does not describe the selected source accurately. Candidate `type_checker.cpp:237` defines `to_proj_idx`, which first requires a small natural number, then compares the machine value to `std::numeric_limits<unsigned>::max()`, and only then converts it to `unsigned`. `infer_proj` uses this helper and separately checks the actual structure/name/field conditions. The inspected projection-reduction call sites also use the bounded conversion.

The correct conclusion is “the reported truncation path has a source correction in this candidate,” not “an open issue proves the candidate remains vulnerable.” Conversely, the code uses the host's `unsigned` limit; our protocol's intended u32 meaning still requires a qualified ABI and exact decoding/conversion rules. Protocol integer widths must not be inferred solely from a C++ type name.

### Dangerous natural-number computation and resource failure

Candidate `type_checker.cpp:308` checks the exponent/shift count against `UINT_MAX` before passing it to runtime operations that require that bound. `reduce_shiftLeft`, at line 677, applies this check for nonzero values and checks the resulting numeral-size bound. The source also bounds admitted natural literals and other numeral-producing computations, with `LEAN_NAT_MAX_SIZE` and a default of 128 MiB.

Issue15193's title mentions crashes in `rfl`, `decide`, `simp`, `cbv`, `grind`, and compilation. Its body explicitly states that the kernel no longer has this problem and refuses the dangerous shift with a kernel exception; the remaining report concerns elaborator/compiler call sites. It must not be cited as evidence of this candidate native kernel's shift crash.

This does not eliminate denial of service. Size bounds do not supply a universal running-time bound, and tactic/compiler execution is still hazardous if a later agent integration executes untrusted material. The chosen inert native-object route should remain separated from source/tactics/plugins/compiler execution. An isolated budget limit, crash, interruption, or unsupported representation is a nondecision, not evidence that the mathematical proposition is false. Validation must not accidentally report `ACCEPT` from a partial operation.

### New foundation entails new bootstrap interpretation

Candidate `type_checker.cpp:1342` binds `g_string_mk` to `String.ofList`. The frozen v4.22 practical profile described the older `String.mk` behavior. This is a concrete compatibility difference, not merely a new release label.

The new foundation's reserved native names, primitive definitions, literal expansions, seed/prelude closure, declaration restrictions, and adapter reconstruction rules must be audited against the new source. A mechanical copy of the old reserved-name/bootstrap manifest is not qualified. Existing CP-001D identities remain historical; they must not be silently assigned the new implementation's meaning. No complete replacement bootstrap is claimed by this review.

## Lean4Lean: exact benefits and exact limits

The pinned README states that the implementation is derived directly from the C++ implementation, “likely shares some implementation bugs,” and is “not really an independent implementation.” It distinguishes the executable/library targets from the metatheory and verification targets. It also states that checking a module without `--fresh` assumes its imports correct, while `--fresh` rebuilds its import closure. This is a useful illustration of why the receiver must independently establish its whole required predecessor environment rather than inheriting unchecked imports.

The pinned source provides a direct limit stronger than a generic caution:

- `Lean4Lean/Verify/Environment.lean:221` introduces `addDecl.WF` and explicitly says that inductives still need a constructive `AddInduct` model. At line 235 the `inductDecl` branch is `sorry`.
- The same file, lines 115–117, says that `AddInduct` currently has no constructors and that the relevant quotient-initialization argument becomes constructive when the inductive-declaration verification boundary is implemented.
- `Lean4Lean/Theory/Typing/UniqueTyping.lean:174` contains a further `sorry` in a weakening-inverse result.
- `Lean4Lean/Verify/Axioms.lean` explicitly assumes properties of partial, opaque, and runtime-backed routines. Examples include persistent-array behavior, persistent-hash-map lookup, `Level.normalize = Total.normalize` at line 257, lawful level equality at line 292, and expression loose-bound-variable metadata at line 360. These are declared assumptions, not all consequences of the ordinary mathematical axiom set.
- `divergences.md` documents deliberate semantic/operational differences, including native reduction support, primitive checking, universe-level comparison, projection handling, and checking fuel. Its statements about upstream release status are contextual to that revision and are not automatically current for our selected v4.34.0 candidate.

These observations do not establish that the Lean4Lean executable is unsound. They establish that the inspected source cannot support an unconditional claim that every required declaration path has a completed assumption-free correctness proof. In particular, compiling a development that contains `sorry` is not a proof-completion check. This review did not build the executable or compute the actual transitive axiom dependencies of each theorem; it makes no exact dependency-count claim.

Selected use: a separately pinned, explicitly qualified additional checker and source of mathematical invariants, only after adapter compatibility and coverage have been established. Neither its name nor the number of available checkers should supply authority to accept evidence outside the common qualified domain.

## Formal implications for the commons

### Conditional checked acceptance, not reputation

Let `Decode_F(b)` give the exact native object represented by bytes b under foundation/adapter profile F. Let `K_F(E, d)` be the selected checked declaration-insertion operation, and let `WF_F(E)` be the intended environment invariant. A required checker property has the form

\[
\operatorname{WF}_F(E)\land K_F(E,d)=\operatorname{ACCEPT}(E')
\;\Longrightarrow\;
\operatorname{WF}_F(E')\land E\preceq_F E'.
\]

The native mathematical meaning of `WF_F` and extension must be specified; they cannot merely abbreviate “the same implementation returned success.” For imported bytes, the implication also depends on exact decoding, reference binding, checked predecessor reconstruction, primitive/axiom restrictions, and faithful execution. A publisher's identity does not repair failure of this implication. Nor does majority acceptance.

For the full architecture, receiver-owned acceptance additionally binds the exact foundation, checker image, decoder/adapter, interpretation view, typed root, and selected witnesses. A security-corrected foundation is not automatically the old foundation with a larger operational budget. The cache and incident rules in the [native scaling amendment](../analyses/CP-001E-native-scaling.md) must preserve that distinction.

### What a second checker can and cannot establish

Suppose two qualified checkers interpret exactly the same object as judgment J, and the receiver accepts only if both accept. If at least one checker is sound for that common domain under the stated foundation assumptions, then conjunctive acceptance implies J is justified under those assumptions. The proof uses the accepting sound checker; probabilistic independence is not required for this logical implication.

However, implementing two programs does not establish that at least one is sound. Shared parsing, primitives, specifications, algorithms, runtime libraries, translation errors, or proof assumptions can create common failure modes. Nor can one multiply two guessed failure probabilities without a justified joint model. A checker disagreement is diagnostic evidence and blocks this conjunctive acceptance policy; it does not alone identify the faulty checker or prove the negation of J.

### What succinct execution proofs can and cannot establish

A sound SNARK for execution of K can establish a relation such as “the committed program K accepted the committed input b,” subject to the SNARK relation, public-input binding, setup, cryptographic assumptions, and faithful arithmetization. It does not establish the missing implication from K's acceptance to intended native mathematical validity. A bug in K can be proved to have executed correctly.

Thus succinct verification is a possible later performance layer over a qualified mathematical checker, not a substitute for foundation qualification. Neither a blockchain nor a consensus ledger changes this logical fact. The receiver's ability to reuse a result safely rests on exact evidence and its interpreted checking boundary, not publication order, author popularity, or immutable recording of an old acceptance.

## Findings and remaining gates

| Finding | Disposition |
|---|---|
| PR14806/14807 apparently absent when checking original master merge ancestry | Resolved: exact release backports and retained source mechanisms independently located. |
| Follow-on `is_prop` path in inductive reduction | Confirmed: PR14843 backport and callback in candidate source. |
| Open projection-index issue misread as candidate status | Resolved for this inspected path: PR14632 conversion is present; ABI qualification remains. |
| Shift issue title misread as native-kernel failure | Corrected scope: issue body distinguishes already-guarded kernel from elaborator/compiler. |
| Old native string-name/bootstrap assumptions reused after source replacement | Open qualification gate: regenerate and audit new foundation interpretation; `String.ofList` observed. |
| Lean4Lean treated as fully independent, compatible, completed end-to-end verification | Unsupported: explicit shared derivation, toolchain mismatch, proof assumptions, and unfinished inductive verification. |
| General release security, executable correspondence, adapter correctness, and practical replay compatibility | Not established by this source review. |

The correct checkpoint claim is that the specified source fixes and some remaining qualification boundaries have been independently examined. It is not “production-ready,” “all vulnerabilities closed,” or “formal verification completed.” Reliable reciprocal knowledge growth requires these boundaries precisely because one accepted defect can otherwise become a shared premise for many downstream agents.

## Reviewed root-note disposition

The reviewer read the complete root [foundation security audit](../analyses/CP-001E-foundation-security-audit.md) at SHA-256 `C7393FBF236A2C4DDE41E32597B6733D9D4B04481B1F8BF46CC11D7B542EDFE7`. Its candidate status, exact source/backport selection, old-grammar reachability qualifications, source-versus-execution distinctions, new bootstrap gate, migration invalidation, and Lean4Lean limitations agree with the independent evidence above. No contradictory claim was identified in that reviewed revision. This is not an exhaustive verification of every referenced API, source path, or historical exploit, and later edits require their own review.

## Sources

- [Lean v4.34.0 immutable source](https://github.com/leanprover/lean4/tree/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b), especially [type_checker.cpp](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/type_checker.cpp) and [inductive.h](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/inductive.h).
- [Lean release tag API](https://api.github.com/repos/leanprover/lean4/git/ref/tags/v4.34.0), [mathlib release tag API](https://api.github.com/repos/leanprover-community/mathlib4/git/ref/tags/v4.34.0), and [pinned mathlib toolchain](https://github.com/leanprover-community/mathlib4/blob/5ed2965256430c3649e86755f9576b54eca72435/lean-toolchain).
- [PR14806](https://github.com/leanprover/lean4/pull/14806) and its [release backport](https://github.com/leanprover/lean4/commit/a221d8246f8d953fa6bd9b170762ab81d53445c3).
- [PR14807](https://github.com/leanprover/lean4/pull/14807) and its [release backport](https://github.com/leanprover/lean4/commit/4576c1cf62ed2b4a4fc1cd2e19e53f1a4a97113e).
- [PR14843 follow-on release backport](https://github.com/leanprover/lean4/commit/c740e4df1984194a84edf4b715bb49daa08a9c14) and [PR14849 numeral-bound release backport](https://github.com/leanprover/lean4/commit/bf8db3df0fb28cb6a24625796bc32ab4a01e9458).
- [PR14632](https://github.com/leanprover/lean4/pull/14632), [issue12746](https://github.com/leanprover/lean4/issues/12746), and [issue15193](https://github.com/leanprover/lean4/issues/15193).
- [Historical pinned type checker](https://github.com/leanprover/lean4/blob/ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05/src/kernel/type_checker.cpp), [historical inductive helper](https://github.com/leanprover/lean4/blob/ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05/src/kernel/inductive.h), and [candidate nested-inductive checks](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/inductive.cpp#L1219).
- [Pinned Lean4Lean README](https://github.com/digama0/lean4lean/blob/8223d223ed98661882e95d9d6a7126df7097cd76/README.md), [toolchain](https://github.com/digama0/lean4lean/blob/8223d223ed98661882e95d9d6a7126df7097cd76/lean-toolchain), and [deliberate divergences](https://github.com/digama0/lean4lean/blob/8223d223ed98661882e95d9d6a7126df7097cd76/divergences.md).
- [Pinned Lean4Lean declaration-verification theorem](https://github.com/digama0/lean4lean/blob/8223d223ed98661882e95d9d6a7126df7097cd76/Lean4Lean/Verify/Environment.lean#L221), [metatheory proof placeholder](https://github.com/digama0/lean4lean/blob/8223d223ed98661882e95d9d6a7126df7097cd76/Lean4Lean/Theory/Typing/UniqueTyping.lean#L172), and [explicit verification assumptions](https://github.com/digama0/lean4lean/blob/8223d223ed98661882e95d9d6a7126df7097cd76/Lean4Lean/Verify/Axioms.lean).
