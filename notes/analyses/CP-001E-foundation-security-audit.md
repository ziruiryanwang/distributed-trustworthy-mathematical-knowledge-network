# CP-001E: foundation security, corrected Lean pin, and requalification

Date: 2026-09-19. Method: read-only inspection of official source commits, release metadata, issue reports, and patches. No exploit was executed, no checker was built, and no contributed declaration was replayed.

## Decision

**Withdraw CP-001D's Lean v4.22.0 kernel from current deployment candidacy.** Retain frozen CP-001D as historical evidence, not as the latest security recommendation. Select **Lean v4.34.0**, source commit `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`, as the corrected practical foundation candidate for qualification. Select matching mathlib commit `5ed2965256430c3649e86755f9576b54eca72435`; its lean-toolchain says `leanprover/lean4:v4.34.0`.

This is a new foundation, not an automatically trusted software update. Its exact seed descriptors, native-rule record, reserved-name interpretation, adapter, and checker image require qualification. The user specified Lean 4, not the obsolete release. Keeping a known-vulnerable kernel and adding a general soundness assumption would not satisfy the trustworthiness requirement.

The practical target retains safe definitions, complete theorem/opaque bodies, mutual/nested inductives, structures/projections, quotient support, native literals, and explicitly permitted standard axioms. We do not evade the defect by relabeling the tiny six-type demonstration as the practical product.

## Why source-only execution restrictions do not solve kernel soundness

The acceptance boundary is inert native data reconstructed into checked declarations. This removes a large executable attack surface, but it deliberately exposes raw native terms to the checker. Surface elaboration can reject or normalize expressions that the kernel itself accepts incorrectly. Avoiding the elaborator does not inherit the elaborator's protections.

For a qualified foundation F and checker C, the intended conditional contract is

\[
\operatorname{Accept}_{C,F}(d)\Longrightarrow F\vdash d,
\]

under explicit assumptions about the foundation, decoder, implementation, runtime, and hardware. A known counterexample to C invalidates the justification for relying on that implication; a small dependency footprint or a successful execution of C cannot repair it.

## Confirmed source evidence and profile relevance

| Upstream item | Evidence | Relevance and disposition |
|---|---|---|
| PR 14613, normalized Prop detection | Old `type_checker::is_prop` compares `whnf(infer_type(e)) == mk_Prop()`; upstream reports `Sort (imax 1 0)` permits data projection from a proof and ultimately False without axioms | CP-001D admits raw imax levels without algebraic identity normalization, checked contributed inductive groups, and native projections. These syntactic ingredients are admitted; no elaborator-normalization defense applies. The old source contains the faulty check. This is sufficient to withdraw the pin; we have not executed an encoded protocol exploit |
| PR 14577, missing nested-parameter checks | Original nested transformation drops parameters from generated auxiliaries; patch checks the substituted nested applications in the restored environment | Nested groups and projections are practical supported constructs. CP-D cannot assume kernel-positive means every supplied parameter was checked. Detailed reproducer conversion through fixed adapter metadata has not been executed |
| PR 14616, temporary `_nested` names | Upstream reports ill-typed restored constructors and False without axioms from references to temporary auxiliary names, including projection names | The selected content-reference grammar and generated-name mapping block arbitrary `_nested` constant/projection names if correctly implemented. Do not falsely classify every upstream exploit as reachable. The corrected kernel supplies an additional check |
| PR 14621, restored-declaration rechecks | Checks restored constructor types, recursor types and rule bodies | Defense in depth over practical nested support, not proof of total soundness |
| PR 14806, history-dependent equality cache | Upstream reports cache-history-dependent classification during recursor construction; replacement uses exact pair caches instead of a union-find closure | Practical inductives require consistent native decisions. This is also a warning against unproved cache optimizations in our adapter. Mathematical transitivity is not permission to alter the behavior of an incomplete algorithm used by another construction |
| PR 14807 and follow-on 14843, require a sort | Upstream reports another False derivation when a stuck inferred type is treated as merely non-Prop; fixes require `ensure_sort`, including the inductive helper | Patching only the imax case is insufficient. The selected candidate includes the follow-on fix too |

Old pin inspected: `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`. Its `src/kernel/type_checker.cpp` lines 348–350 contain the syntactic Prop comparison; `src/kernel/inductive.h` line 70 has the corresponding syntactic comparison. Its nested-inductive insertion lacks the later parameter/recheck blocks. This is source evidence, not a new independent exploit demonstration.

### Inclusion of fixes is checked, not inferred from release dates

GitHub compare metadata reports the selected v4.34.0 commit ahead of, with zero commits behind, each of:

- `17dbc815cf3055e73a9e37d854b8427dc1e9c46c` — PR 14613.
- `a39eab69e1eee9ad38f4efe507907b1026a77808` — PR 14577.
- `35f696862cdd30727a343356102af696803d91d4` — PR 14616.
- `448dc4441e76a0b17404e7d41a1a13dbb1642933` — PR 14621.

The original master commits for PR 14806/14807 are **not ancestors** of the release pin: compare reports divergence. The release branch instead contains explicit cherry-picks:

| Fix | Release-branch commit |
|---|---|
| PR 14806 | `a221d8246f8d953fa6bd9b170762ab81d53445c3` |
| PR 14807 | `4576c1cf62ed2b4a4fc1cd2e19e53f1a4a97113e` |
| PR 14843, helper follow-on | `c740e4df1984194a84edf4b715bb49daa08a9c14` |
| PR 14849, native numeral bounds | `bf8db3df0fb28cb6a24625796bc32ab4a01e9458` |

The pinned source itself has `ensure_sort(infer_type(e))` in `is_prop` and the `m_success` exact-pair cache. Nested insertion checks temporary names, nested parameter applications, restored types and recursor bodies. Commit-history evidence and the actual source are used together; merely finding the original PR number in a search would not establish inclusion.

## Version-specific bootstrap changes

Changing the release tag in the old profile is not sufficient. A concrete incompatibility is already visible: v4.34.0's kernel binds its trusted string-construction name to **`String.ofList`**, where CP-001D selected `String.mk`. Both the type-checker and string-literal expansion source name `String.ofList`.

The new bootstrap recipe therefore includes the original intended arithmetic roots, exact equality/Bool/Nat/list support, explicit permitted axioms and quotient initialization, and the **v4.34-specific safe dependency closure of `String`, `String.ofList`, `Char`, and `Char.ofNat`**. Every non-primitive declaration and body must be extracted as inert descriptors and checked. Merely preserving an old export number or pretty name cannot establish the new seed meaning.

The full reserved-name audit must cover kernel initialization, literal expansion, quotient setup, recursor generation, arithmetic reductions, and expression primitives—not only the two string occurrences found here. `Lean.reduceBool`, `Lean.reduceNat`, unchecked environment insertion, arbitrary axioms, `sorryAx`, and executable compiler-assisted proof shortcuts remain outside accepted contributed evidence. A matched reserved string in source is not authority to enable it.

The pinned native declaration API still has safe theorem/definition/opaque and inductive declarations; `mutualDefnDecl` is documented for unsafe/partial definitions and remains excluded. Entry signatures and resource options have changed, including native recursion limits. The v4.34 adapter must select the checked environment-insertion API explicitly and qualify heartbeat/recursion/numeral-size refusal handling. The debugging `Kernel.check`/conversion helpers alone must not be presumed to implement the complete bounded declaration-acceptance contract.

## Distinguish soundness, representation, and availability failures

Issue 12746 reports projection-index narrowing. The selected release source has a `to_proj_idx` guard and PR 14632 hardening; an open issue label does not prove the fix is absent. Independently, the exchange schema must require exact lossless conversions, native-width representability, and index bounds. It must never reinterpret a large wire index by truncation. The [native scaling amendment](CP-001E-native-scaling.md) supplies explicit schema/ABI constraints.

Issue 15193's title mentions crashes, but its body states that the **modern kernel refuses the dangerous large shifts**; remaining reported crashes concern elaboration/compiler paths. In the selected source, `get_count_arg` checks the exponent/shift width and `reduce_shiftLeft` checks computed numeral size. We do not claim that this report demonstrates a current selected-kernel soundness exploit.

Native work still needs a separately resource-limited, non-authoritative worker. Timeout, arithmetic-resource refusal, crash, unknown exception, and malformed worker output cannot produce ACCEPT; they yield a scoped checking nondecision with diagnostics. A kernel type error is not evidence that the mathematical statement is false. Sender-selected timeouts or an exception string cannot authorize a verdict. Process isolation protects service integrity, not logical soundness if a buggy kernel returns success.

Raw free variables/metavariables and expression metadata are forbidden by our grammar, and strings require canonical valid UTF-8. Thus upstream issues involving malformed metadata or raw free-variable declarations require separate reachability analysis; a broad search hit is not sufficient to claim protocol exposure. Internal local variables created during checking remain the checker's responsibility.

## Foundation incidents and migration

The selected local activation states are `CANDIDATE`, `QUALIFIED`, `ACTIVE`, `SUSPENDED`, and `RETIRED`. A remote publisher cannot activate a foundation or clear an incident.

1. Record the known old-image/foundation defect locally and withdraw it from new reliance. Where affected scope has not been soundly narrowed, use the broad foundation/checker breaker immediately.
2. Preserve historical objects and assessment records, labeled by their original basis. Do not overwrite a prior ACCEPT to pretend it was made by a different checker; do not infer that every old statement is false.
3. Suspend current positive eligibility of affected certificates and selected dependent replays. Cache keys bind exact source semantics, decoder, checker image, interpretation view, ABI, and relevant options. Broad guard checks precede lazy descendant processing.
4. Prepare new seed/interpretation descriptors and a qualified new image; activation is a local operator decision backed by its qualification record, not network voting or elapsed time.
5. Re-export or explicitly translate old artifacts into new-foundation objects and independently recheck them. Old bytes may remain local untrusted input. No same-foundation compatibility view crosses this source-commit change.
6. Rebuild exact selected evidence and guarded local reuse under the new basis. New checked results may coexist with old historical representations; a publisher's mapping or theorem name is not a transport proof.
7. Restore affected local use only after the new check, complete protected bytes, current policy and incident guards all pass. Mathematical validity, availability, and custody remain separate states.

This process has genuine cost: rechecking a changed trust basis can touch the retained graph. Incremental representation removes avoidable repetition but must not optimize away security requalification. A deployment may prequalify a replacement before an incident, but it cannot assume future fixes preserve semantics. Physical archival copies can remain intact while trusted-current-reuse is suspended.

## Multiple checkers and succinct proofs

Lean4Lean is valuable for differential checking and formal metatheory. At inspected commit `8223d223ed98661882e95d9d6a7126df7097cd76`, its README expressly says it is derived from the C++ implementation, is **not really independent**, and may share implementation bugs. Its toolchain is v4.33.0-rc2, not our candidate release. Its normal single-module CLI assumes imports correct; `--fresh` checks imports too. Neither CLI is automatically our inert-data receiver or a qualified substitute for full selected closure checking.

The pinned proof sources impose a stronger limitation than version mismatch: `Verify/Environment.lean` line 235 contains `| inductDecl _ _ _ _ => sorry`; lines 115–117 explicitly describe the unimplemented inductive-declaration verification boundary. `Theory/Typing/UniqueTyping.lean` line 174 also has a proof placeholder, and `Verify/Axioms.lean` declares runtime/opaque-operation correspondence axioms. These observations do not establish an executable checker bug, nor do they negate the completed partial theorems. They do rule out citing this revision as a completed unconditional end-to-end verification for the inductive groups required by our practical profile.

Upstream PR 14807 reports the same bogus proof accepted by nanoda but believed rejected by Lean4Lean; PR 14806 reports exploits caught by other checkers. These observations motivate diverse checks but do not imply independent failure probabilities. Two implementations agreeing on a false acceptance remain wrong.

The selected first acceptance path uses the corrected native kernel with explicit qualification. An optional second checker may provide additional assurance only after exact feature/foundation/adapter alignment. If required by local policy, disagreement or unsupported coverage prevents the higher-assurance label; majority vote does not prove truth. No statistical multiplication of alleged checker error rates is justified.

A SNARK proving that an old checker executed and returned ACCEPT would faithfully certify the wrong computation. Succinct verification is therefore an optional later cost optimization after specifying the exact correctly qualified checker computation, input commitment, complete dependency closure, cryptographic assumptions, and proof-system implementation. It does not repair the foundation or replace the local adoption decision.

## Qualification obligations and evidence boundary

Before activating a practical image:

- derive and freeze exact new bootstrap/seed/native-rule/ABI inventories, including v4.34 strings and generated nested recursors;
- establish adapter correspondence and checked insertion, no unchecked import/environment path;
- include the identified upstream bug families and boundary cases in the future regression/adversarial corpus, through the actual native-data path;
- distinguish malformed encoding, ill-typed evidence, resource nondecision, implementation failure, and unsupported feature;
- replay representative pinned mathlib declarations with every required body, including structures/instances, classical/quotient mathematics, dependent families and nested inductives;
- validate cache/environment/witness and incident/recovery contracts against exact images;
- record source/build/runtime identities, qualification results, outstanding issues, and activation authority.

None of these execution obligations has been performed in this concept-only phase. The present evidence justifies replacing the obsolete candidate and makes the next qualification target concrete. It does not establish exhaustive absence of unknown flaws or production readiness.

## Sources

- [Old pinned type checker](https://github.com/leanprover/lean4/blob/ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05/src/kernel/type_checker.cpp).
- [PR 14613](https://github.com/leanprover/lean4/pull/14613), [PR 14577](https://github.com/leanprover/lean4/pull/14577), [PR 14616](https://github.com/leanprover/lean4/pull/14616), [PR 14621](https://github.com/leanprover/lean4/pull/14621).
- [PR 14806](https://github.com/leanprover/lean4/pull/14806), [PR 14807](https://github.com/leanprover/lean4/pull/14807), [PR 14843](https://github.com/leanprover/lean4/pull/14843), [PR 14849](https://github.com/leanprover/lean4/pull/14849), [PR 14632](https://github.com/leanprover/lean4/pull/14632).
- [Selected pinned type checker](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/type_checker.cpp), [inductive implementation](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/inductive.cpp), [inductive helper](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/inductive.h), [environment API](https://github.com/leanprover/lean4/blob/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/Lean/Environment.lean).
- [Issue 12746](https://github.com/leanprover/lean4/issues/12746), [issue 15193](https://github.com/leanprover/lean4/issues/15193), [kernel-logic renovation discussion](https://github.com/leanprover/lean4/issues/14977).
- [Pinned Lean4Lean README](https://github.com/digama0/lean4lean/blob/8223d223ed98661882e95d9d6a7126df7097cd76/README.md), [pinned toolchain](https://github.com/digama0/lean4lean/blob/8223d223ed98661882e95d9d6a7126df7097cd76/lean-toolchain), [divergences](https://github.com/digama0/lean4lean/blob/8223d223ed98661882e95d9d6a7126df7097cd76/divergences.md).
- [Pinned declaration-verification boundary](https://github.com/digama0/lean4lean/blob/8223d223ed98661882e95d9d6a7126df7097cd76/Lean4Lean/Verify/Environment.lean#L235), [correspondence axioms](https://github.com/digama0/lean4lean/blob/8223d223ed98661882e95d9d6a7126df7097cd76/Lean4Lean/Verify/Axioms.lean), [typing proof placeholder](https://github.com/digama0/lean4lean/blob/8223d223ed98661882e95d9d6a7126df7097cd76/Lean4Lean/Theory/Typing/UniqueTyping.lean#L174).
- [Matching mathlib toolchain](https://github.com/leanprover-community/mathlib4/blob/5ed2965256430c3649e86755f9576b54eca72435/lean-toolchain).

URLs without a source commit identify issue/PR records that may receive later discussion. The inspection date, resolved source commits, release backports and local review findings fix what this checkpoint actually relied on.
