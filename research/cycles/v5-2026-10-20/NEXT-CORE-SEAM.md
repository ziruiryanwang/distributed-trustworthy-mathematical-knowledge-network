# Next core seam: ordinary demand-directed semantic acquisition

2026-10-20, core_search. Source-only decision; no implementation, imports,
runtime or Git changes. Read GOAL, current desk, v5 README, latest growth
critical path and the ordinary service/reader/contribution sources.

## Recommendation

After the installed repair closes, select **one fixture-free bounded helper
that stages the selected evidence and its demanded semantic closure before
actual admission**. Proposed new source: `software/v5/client/semantic_reader.py`.
Compose it from an explicit successor of `remote_reader.read`; preserve the
frozen reader and its evidence. This is an optional local acquisition strategy,
not a new mathematical acceptance rule or mandatory agent research policy.

The concrete gap is in `client/remote_reader.py:read`: after search it calls
`acquire`, then `semantic_material`, and returns `NEED_SEMANTICS` unless the
selected packet already carries its semantics. Terminal certified evidence
therefore cannot complete ordinary reuse through that entry. Even mixed
packets can lack demanded definitions. Fetching after a slow check can also
consume the finite provider-contact window.

All necessary lower-level operations already exist in
`client/workspace_staged.py` (inherited by `workspace_validated.py`):
`stage_packet`, `preview_context`, `admit_staged`, plus the evidence client's
`resolve_declaration` and `acquire_body`. `transport/semantic_staging.py` uses
the same dependency walker as live import. The only composed demand loop is
`client/terminal_strategy.py:demand_context`; it hard-codes `{BASE, first}`,
fixture group counts and a particular two-module workload. Do not ship that
restriction as the commons algorithm or copy its whole campaign.

## Small contract and invariant

Given a live validated client, a returned candidate/offer, and finite
owner-selected module/name/group/body/round/byte limits:

1. Stage the selected packet and committed selected group.
2. Follow only the preview's `NeedModuleEvidence`, `NeedDeclaration` and
   `NeedBody` requests through the existing authorized provider. Deduplicate
   exact module/name, group index and module/universe/body-hash addresses.
   Select at most one exact journal/packet per module; ambiguous variants
   require explicit policy or stop. Each round must add new held data or stop.
3. At structural closure, consume each one-shot `admit_staged` transition,
   then invoke unchanged live `import_context`. Only its actual returned
   context permits authoring. Preview/data custody never grants authority.
4. Return bounded `READY`, missing-data, unsupported-selection or exhausted
   outcomes. Do not refresh contacts, renew grants, infer global absence,
   fetch ancestral opaque theorem proofs or add a provider-routing system.

The local caller supplies the demand-fulfilment policy and every offered-packet
or variant choice; the helper may expose pending demands and accept explicit
choices rather than autonomously exhausting them. It must not silently choose
the first variant, switch an A requirement to I, or synthesize a proof. A local
agent's solver/source choice remains outside this helper. Every chosen fetch
uses the original contact permission, grant and deadline.

The number of network acquisitions depends on the selected modules, names and
bodies, not the global theorem count; repeated full previews can cost
`O(rounds × selected-closure-work)`, not necessarily linear work. Existing
whole-operation caps remain decisive. Missing material at this provider is an
honest bounded failure, not permission to invent a global completeness claim.

## Reuse evidence; do not duplicate campaigns

- The nine audited structural-staging controls in
  `v5-2026-10-17/STAGING-REVIEW.md` already cover tokens, preview and real-owner
  admission separation using inert owners. Keep that scope; no rerun.
- Ordinary remote integration `68af5327` already reached real I/native READY
  with the retained fusion packet. Keep its search/admission evidence.
- `client/serve_workspace.py` and `examples/contribute.py` already connect
  local publication to reopenable read-only service. Serving02/03 cover its
  lifecycle/reopen boundary. No new provider or publishing subsystem is needed.
  Once current contribution succeeds, its persisted output can be the next
  ordinary service input without regenerating earlier seed mathematics.
- Add only helper-specific controls: arbitrary demanded third module,
  same-address deduplication, progress/cap exhaustion, explicit variant choice,
  no admission before complete staging, and no preview authority. Genuine A
  remains a separate unmet prerequisite; no synthetic A qualifies it.
- If a genuine changed-boundary call is later needed, use one retained I/mixed
  result through the existing service, starting from only its selected group
  and fetching the actual missing committed semantics before unchanged
  admission/import. No new proof or authoring is required. This validates the
  helper's actual fetch/order path, not terminal-A acceptance or broad growth.

This seam turns existing scalable import primitives into ordinary operation
and is higher payoff than another cost calculator, prover/RAM investigation,
provider implementation or broad reciprocal replay. It does not establish
positive full-cost growth or final-v5 completion by itself.
