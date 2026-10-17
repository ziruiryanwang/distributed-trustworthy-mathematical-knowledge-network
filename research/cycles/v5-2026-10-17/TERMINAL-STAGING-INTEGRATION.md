# Terminal adapter integration with structural staging

2026-10-17. Source-only plan; no product changes, imports, tests, builds,
network/proof execution or Git mutation. The committed unexecuted terminal adapter
remains unchanged until root separately selects its integration. The general
staging helper/facade are separately authored under STRUCTURAL-STAGING-SELECTION.
This plan does not create a real A receipt or select a launch.

## Exact changed seams

Only three terminal integration concerns need change:

1. `client/terminal_assets.py`: import `Workspace` from `client.workspace_staged`,
   so its exact-type owner-construction check agrees with the selected successor.
   Require `client/workspace_staged.py` and `transport/semantic_staging.py` in its
   actual source map, retaining the inherited resilient/evidence/atomic sources.
   Persisted config, owner types, foundation, mathematical profiles and grants
   stay unchanged. A future allocation decision remains separate.
2. `client/terminal_strategy.py`: import that same staged Workspace. Preserve
   the existing standalone `discover` chooser, formal query, returned-order
   selection, failure rules and fixed caps. Do not pass expected FIRST/SECOND Js,
   asset objects or author source into the chooser or pre-admission resolver.
3. Replace B's verify-then-demand ordering with stage-then-verify. Refactor the
   existing bounded `demand_context` into a structural resolver; do not add a new
   routing framework. C keeps its existing acquire/verify/offline packet import.

`terminal_inspection.py`, public location/search protocols, issuer/checker
relations and publication need no semantic change for this ordering repair.

The prospective source closure becomes100 entries:78 v5,21 portable and one
owner (the previous98 plus the two staging sources). With the same runtime rows,
the A/native issuer maps become97/79 entries, still below128. The owner strategy
remains only `owner/terminal_strategy.py`, not a duplicate v5 import. Final byte
pins must be selected from the actual integration revision.

## Actual public staging field contracts

Use `stage_packet(candidate, entry) -> StagedEvidence`; the token is opaque and
belongs only to that client. `describe_staged(token)` yields:

```text
status = STAGED_UNTRUSTED_EVIDENCE
provider
candidate = actual resolved locator/opening/descriptor data
selection = {module, journal: list[184], summary, packet_sha256, packet_bytes}
admission_consumed
mathematical_acceptance = false
```

The candidate nested in this snapshot is the held resolution; compare its
locator/opening/descriptor explicitly, not to a higher-level describe_candidate
dictionary that additionally carries a provider field. A staged journal is data,
not a warranted mathematical result.

`preview_context(staged_tokens, openings, bodies, limits=None)` requires distinct
unconsumed tokens and **the full current accumulated arrays**, not just deltas.
The pure preview has no persistent context. Openings are `{module, opening}`;
bodies are `{module, universes, expression}`. It returns only status, demands,
cost and mathematical_acceptance=false. Statuses are
NEED_STRUCTURAL_CONTEXT_DATA / STRUCTURAL_CLOSURE_STAGED; demands are
NeedModuleEvidence / NeedDeclaration / NeedBody.

Root and independent review adopted a pre-execution refinement: preview reads
the immutable staged selection metadata, not the full packet. Held groups/bodies
are still rebound. Preview therefore makes no claim that packet bytes remain
available now; a missing or changed packet must fail subsequent actual admission.

`admit_staged(token, ...)` consumes its transition, re-reads local held bytes,
performs unchanged actual admission, opens the group through the actual owner,
then rebinds its live target and local bytes. It makes no HTTP call. Preview must
finish for all selected tokens **before the first token is consumed**, because
the actual facade deliberately rejects preview of consumed tokens.

## Structural resolver algorithm

Inputs: the real client, origin candidate, its actual description and selected
offer, finite caps and an audit-record sink. No assets/evaluator Js/author source.

1. Let FIRST here mean the actual candidate's ModuleID, not the evaluator's
   expected FIRST constant. The only additionally allowed module for this fixed
   workload remains the common public BASE vocabulary. Stage the candidate's
   offered terminal and describe its staged token once. Bind selection.module,
   summary and candidate opening/locator to the actual returned candidate.
2. Initialize maps:
   - token and inert selected-record by ModuleID;
   - exact-name candidate by `(module, C.name_key(name))`;
   - full opening by `(module, group_index)`;
   - full body expression by `(module, universes, digest)`.
   Seed only the actually returned FIRST group. No origin-wide inventory is
   delivered to B and no historical reference proof determines its semantics.
3. Call `preview_context` with all current tokens/openings/bodies. Record its
   actual structural demands and cost. If READY, require no demands and exactly
   the two selected workload modules. Return the still-unconsumed tokens,
   staged records and accumulated data, not an AuthorContext.
4. For each demand use `resolve_declaration(origin_candidate, module, name, ...)
   -> describe_candidate` only if that exact name is not already cached. Bind
   returned name/module and opening. Reject demands outside BASE plus the actual
   first module. This remains same-contact demand acquisition, not a new index
   candidate or a supplied fixture endpoint.
5. For `NeedModuleEvidence`, if this batch has not already staged that module,
   call `packet_offers`, stage the actual offered packet, and describe the new
   token once. Bind its exact target summary/module to the fetched declaration.
   In a single preview batch several declarations may demand that same missing
   module: stage it once, then add each demanded group normally. A group is never
   added as an evidenced preview item before its target packet is staged.
6. Add newly received groups with the existing exact canonical conflict checks.
   For `NeedBody`, fetch with the actual corresponding candidate, verify the
   returned module/name/universes/digest and body hash, and append only a new
   body identity. Shared body demands in the same batch fetch once. A repeated
   demand already satisfied in an earlier preview is an integration failure.
7. Require strict growth in staged-module + group + body counts before the next
   preview, with unchanged MAX_STEPS32, MAX_NAMES64, MAX_GROUPS12 and MAX_BODIES11.
   Keep the current semantic reply cap2MiB and existing grant. No implicit retry,
   broader provider selection, time renewal or extra allowance follows failure.

The group's content is the codec's import unit. This computes closure for the
selected declarations' types and required definition/recursor computations, not
arbitrary theorem proof ancestry or every BASE group. In particular it does not
fetch unused binary_congr to reproduce the historical1009-row witness.

## Actual B admission and continuation

After structural READY, do the following while keeping the original reader open:

1. `admit_staged(first_token, **admit_limits)` with **no evaluator expected J**.
   Its internal exact-J binding comes only from the actual staged target. Then
   `describe` and perform the existing evaluator checks for FIRST/H2/receipt
   identity/name. Those checks remain after real mathematical admission.
2. `admit_staged(base_token, expected_exact_journal=expected_BASE, **admit_limits)`.
   Describe and require exact BASE/J plus the same actual A header and receipt
   hash/length as FIRST. Existing same-live A caching avoids another A check;
   exact membership is still independently validated and charged.
3. Call unchanged `import_context` once with both real warrants, their actual
   whole Js and all staged openings/bodies. Require its real READY status and
   no demands. A staged preview does not authorize authoring and cannot replace
   this final check. Unexpected missing data is a failed integration, not a
   reason to download using expired hints.
4. Only now release the fixed ordinary source/roots, author SECOND once and run
   the unchanged output/witness/FIRST-proof-use inspector. Preserve exact
   J_SECOND/local_spec/rank and actual carried receipt identity assertions.
   Ordinary publication, provider withdrawal, cold C and final cleanup continue
   unchanged.

The expected actual counts remain **2 A checks total,1 author call,1 native
SECOND check,0 I checks,0 guest/proof calls and0 FIRST proof replay**. B's second
staged-member admission is a membership/cache operation, not a third A check.
New structural counters should show B packets_staged2, admission_transitions2
and bounded previews; C uses no staging tokens and is independently admitted.

## Calls, bytes and no hidden budget increase

The selected facade no longer reads full packets during preview. Its immutable
same-client metadata snapshot is sufficient for a data-only closure prediction.
Each preview still charges serialized selected metadata and semantic arrays,
rebinds held groups/bodies, and consumes original call/controller/wall resources.
The former O(previews*packet_bytes) design was rejected before execution and is
not the current implementation or cost claim.

Let K be preview calls and P_F/P_B the exact terminal packet lengths. With one
description per staged token, full packet input is charged once at staging,
once at describe_staged, and twice during admit_staged (pre/post real admission).
Thus the packet-only client input charge is independent of K:

```text
4 * P_F + 4 * P_B
```

Additional charges include repeated preview arrays and metadata, initial staged
metadata, actual receipt/header/member input, final import, author source/results
and publication.
The unchanged256MiB client input cap still requires exact-size preflight:
terminal JSON hex-encodes the receipt, repeated semantic arrays are not free,
and the fixed packet term does not account for all remaining costs. Do not assert
feasibility from source-count caps or silently raise the grant. Once a real
receipt exists, root must preflight its exact packet sizes and the selected
structural closure's full counter bounds before selecting the integration run.
A refusal is preserved. The final admission still rejects a deleted/corrupted
packet even if a metadata-only structural preview had returned READY.

Under the current fixed caps the generic32 productive-round limit gives at most
33 previews. Strict progress improves the theoretical bound: initial state has
one module and one group; final state has at most2+12+11=25 objects, so at most23
productive rounds and24 previews. No tighter measured round count is claimed.

Let D be public discovery calls (at most16), N new exact-name resolutions (at
most63), B_d body fetches (at most11), and S staged modules (=2 on success).
One description per staged token, one offer per additional module, actual
admit/describe per module and final import/author/publish give:

```text
calls <= D + 2*N + 4*S + (S-1) + B_d + K + 3
      <= 189  (using K<=24), below the existing256 call limit.
```

This counts public decorated operations, not internal store/issuer checks;
those retain their own counters and4096 import/store call bound. Root's eventual
exact selection must include all enclosing setup/provider/inspection work and
source hashes; this formula does not fund it or establish positive net growth.

## Timing claim and boundaries

All semantic/network dials occur before first A verification. Each still checks
the original contact expiry before dial, and all work retains the original
grant/deadline. An already authorized exchange may complete after contact expiry
under its existing request limits. Verification duration can no longer cause a
later required semantic dial to use a stale hint, because there is no such dial.

The reader channel must remain open for the existing handoff activity checks;
do not confuse provider withdrawal with reader teardown. A transfer that is
itself too slow, unavailable semantics, malformed replies, missing staged data
or any original-budget exhaustion still fail. Contact refresh is separate future
work, not hidden in this ordering change. Final v5, independent hosting and
full-cost growth remain open.
