# Cross-build semantic boundary: conditional source argument

2026-10-25. Author: `ordinary_routing_gap`. Source-only review of the ordinary
runtime sources selected by the audited transport-release handoff (`bdbee38`).
Canonical guard passed. No imports, executions, tests, network, state access,
Git operation or predecessor edit. The package/outcome audit is not repeated.

## Finding

**No additional requirement that a remote node share the receiver's generated
native hashes, installation ID or PROFILE was found in the selected ordinary
discover -> acquire -> local admit -> author -> publish path.** Different local
build identities do not by themselves obstruct that loop. No new feature or
experiment is proposed by this finding.

Let A and B adopt supported implementations with different local identities
`I_A`, `I_B` and profiles `P_A`, `P_B`, but the same selected semantic contract S,
foundation F and discovery feature profile. For exact portable evidence bytes e:

```text
UnitID(e) = H(evidence-domain || 0 || e)
ExportID(S,e,n) = H(export-domain || 0 || canonical([S, UnitID(e), n]))
BasisSymbol(S,F,n) = H(basis-domain || 0 || canonical([S,F,n]))
```

Neither `I_A` nor `P_A` is an input. The evidence envelope contains exactly
schema, semantic_id, imports and unit; imports bind complete direct references
to portable symbol identities. Thus B can recognize the same exact claimed
mathematics without accepting A's compilation, local snapshots or checking report.
Recognition is not mathematical acceptance: B must establish its own warrant.

## Actual source trace

Paths below are relative to `software/v5/`; line numbers identify current frozen
source, not a new implementation selection.

Correction before adoption: `ordinary_bounded_operations/source-map.json:425`
selects installed `authoring/py/ordinary_contribution.py` from
`ordinary_project_return/ordinary_contribution.py`. The earlier draft incorrectly
cited its `ordinary_lean` predecessor as the installed authoring implementation.
The table now traces the selected successor itself; the conclusion is unchanged.

| Stage | Controlling source and consequence |
|---|---|
| Portable identity | `ordinary_lean/ordinary_semantics.py:86,175,198,204` and `portable_evidence.py:46`: S fixes foundation/codec/checking policy, not installed native pins. Unit/export/basis identities above omit I and PROFILE. |
| Discover | `ordinary_formal_query/discovery/ordinary_export_adapter.py:32` derives the namespace from S and fixed preview/feature/type-key formats. `ordinary_sparse_access/peer_api.py:492` searches in that namespace; no remote implementation identity is compared. Matching S alone is insufficient if feature profiles differ, but the two stipulated supported builds share this fixed adapter. |
| Acquire | `ordinary_authoring_offers/ordinary_acquisition.py:442,462` requests locator/evidence by S and ExportID/UnitID, validates exact returned identity/name/bytes and stores inert evidence. No producer I, PROFILE, local-root or native snapshot is requested as authority. |
| Local admit | `ordinary_sparse_access/peer_api.py:573` uses B's selected local parent and finite dependency policy. `ordinary_lean/ordinary_admission.py:390,518,565` matches S and exact name/symbol imports, rebuilds the plan and invokes B's own installed checker. A foreign checking report is not used as a warrant. |
| Local authoring | `ordinary_project_return/ordinary_contribution.py:162,197,345` accepts acquired `(name,export_id,unit_id)` targets only when B's context warrants them, fetches their exact local-custody evidence at lines 417-438 and authors through B's selected support. The profile/installation equality at line 364 is B-to-B, not A-to-B. |
| Portable successor | `ordinary_lean/portable_candidate.py:114` binds the candidate to B's context; lines 229-239 construct portable envelopes containing S/imports/unit, not that local context or implementation. The selected `ordinary_project_return/ordinary_contribution.py:520,530` binds and preflights these units, then locally admits them before producing publication bytes. |
| Publish and reverse reuse | `ordinary_sparse_access/peer_api.py:738` requires B's local accepted bindings and exact custody evidence, constructs previews and indexes under S's namespace. A can receive the new evidence by the same route. Publication does not itself confer peer acceptance. |

The selected authoring successor adds optional `TrustedProjectAuthoring` support
(`ordinary_project_return/ordinary_contribution.py:61,396,488`). Its default
backend preserves the inherited ordinary-source path; the optional branch
changes source assembly and owner-approved worker invocation. Both converge on
the same candidate binding, local preflight/admission and portable output flow.
Its project paths/imports are B's executable-code trust selections, not a demand
for A's implementation or PROFILE. They do not grant remote native acceptance.

## Why local implementation checks are not a hidden network restriction

`ordinary_lean/ordinary_semantics.py:210` intentionally includes implementation
and store identity in **local materialization** roots. `portable_catalog.py:428`
requires native snapshot provenance to match the current local implementation;
`ordinary_admission.py:503` opens the local catalog with that implementation.
These comparisons prevent using another installation's compiled cache as a
local warrant. Each receiver independently materializes the portable evidence.
Local roots, private snapshots, candidate envelopes and reports are not the
portable exchange unit. They should not be copied across builds as accepted state.

## Precise conditions and limits

The source argument is conditional on both approved implementations conforming
to S, protected local state/support, collision-resistant content identities,
available matching providers/evidence, sufficient finite budgets, and compatible
local name/import bindings. Missing dependencies require the explicitly permitted
bounded closure or prior local admission. Conflicting names are correctly refused
(`ADMISSION_PARENT_NAME_CONFLICT`/`ADMISSION_PARENT_IMPORT_CONFLICT`), not repaired
by changing build hashes. Existing source language/size limits still apply.

Two independently authored proofs of the same informal theorem may yield
different units/ExportIDs because their exact proof content differs. This is not
an accidental dependency on a producer's implementation; the protocol does not
claim proof-irrelevant semantic deduplication. Equal source intent also does not
guarantee byte-identical compiler output or mathematical equivalence.

The already documented foreign producer-report convenience limitation and
explicit intake alternative remain in `FRESH-BUILD-CLOSURE-REVIEW.md`; they are
not rediscovered as a new blocker here. This finding establishes a conditional
source-level compatibility path, not an independently built two-node execution,
universal discovery completeness, cheap arbitrary closure replay or useful-growth
result. No additional identity relaxation is justified by this question.
