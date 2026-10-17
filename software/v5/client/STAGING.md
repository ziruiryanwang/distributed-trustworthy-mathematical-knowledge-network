# Acquire first, verify locally, then reuse

Implementation status: new source under review; no genuine aggregate-receipt
integration has run. The previous client and all used evidence remain unchanged.

## Why this separation exists

A provider contact is a short-lived permission to start a network request. It
is not the lifetime of downloaded mathematics. Previously, a slow local receipt
check could consume the contact's lifetime before the client fetched definitions
needed for reuse. The staged client instead supports this order:

```text
discover a declaration -> stage its evidence and required semantics
                      -> verify held evidence -> live import -> author
```

Every network request still uses the original authenticated contact, egress
policy and budgets. Staging does not renew a contact. Once acquisition is done,
local checking can continue within the original operation deadline. The reader
channel must remain open until ordinary client closure; the provider need not.

## Public operations

Use `client.workspace_staged.Workspace` with the unchanged evidence workspace
configuration and original real owners. Include `client/workspace_staged.py`
and `transport/semantic_staging.py` in their selected source-pin maps, in
addition to the required predecessor closure. These are explicit selected
successors, not an implicit change to older installed clients.

| Operation | Result and authority |
|---|---|
| `stage_packet(candidate, offered_entry)` | Fetches/read-backs one exact offered packet. Returns a same-client `StagedEvidence` token, not a mathematical warrant. |
| `describe_staged(token)` | Inert candidate, exact selected journal/summary/packet identity, and whether its admission transition was consumed. Re-reads held bytes. |
| `preview_context(tokens, openings, bodies, limits=None)` | Data-only demands or `STRUCTURAL_CLOSURE_STAGED`. No authoring context, proof acceptance, or transferable authority. |
| `admit_staged(token, ...)` | Consumes the one-shot transition and invokes the unchanged actual verifier, group opening and final target checks. Returns a real live warrant only on success. |

The preview accepts opening records `{module, opening}` and body records
`{module, universes, expression}`. Both must already be in local structural
custody. Use existing `resolve_declaration` and `acquire_body` to obtain missing
objects; use `packet_offers` and `stage_packet` for a newly needed module.

Preview demands are `NeedModuleEvidence`, `NeedDeclaration`, and `NeedBody`.
They are instructions about missing data, not an assertion that the provider's
mathematics is valid. Start from the independently selected search result and
follow these demands with a finite round limit. Deduplicate groups, bodies and
names; each iteration must make progress or stop. No global mathematics task
list or human-intention test is introduced.

After staging is complete, admit the selected tokens and call the ordinary
`import_context` with those actual warrants and the staged data. Its existing
checks are mandatory. Only its live returned context may reach `author`.
If live import still needs data, do not pretend preview was verification or
silently extend a contact; expose the mismatch/incomplete closure.

## Failure and cost rules

- Each staged module has one exact selected packet and whole journal. A second
  staged token for the same ModuleID refuses, including a different proof/rank.
  This API does not silently select between variants.
- Tokens are local to the original client and cleared on failure/close. They
  cannot be used as `LiveWarrant`, persisted as authority, or retried after a
  consumed admission transition. Ordinary structural custody may survive.
- Preview never trusts group presence as evidence that a module packet exists.
  It checks exact staged selection, group summaries and body commitments. The
  same pure dependency walker as live import determines the data demands.
- Preview uses immutable same-client staged packet identities. It rechecks held
  groups and bodies, but does not re-read the entire certificate on every round.
  A packet deleted or corrupted since staging may remain unnoticed by preview;
  unchanged exact readback before/after real admission must still reject it.
- All calls, actual packet reads, repeated metadata/input submissions, store calls and controller
  time remain charged to the original operation. The source-count and semantic
  data caps also bound retained token metadata. No new grant is created.
- Preview revisits selected data; it is not an incremental linear-time index.
  Its expression counter is not a total CPU measurement. Enclosing process
  supervision remains necessary. Provider cost is separate.

No opaque ancestor theorem proof is needed by this semantic planner. Selected
definition bodies and recursor rules are still required, including ones not
eventually reduced by Lean. The closure is therefore *selected declaration
closure*, not perfectly minimal computation data.

Invalid evidence can waste bounded semantic downloads before rejection. Staging
also cannot guarantee that an enormous closure transfers within one contact's
freshness window. Explicit budgeted refresh or alternative-custodian discovery
is separate future work. This API removes local verification from the network
freshness bottleneck; it does not solve every availability or growth problem.
