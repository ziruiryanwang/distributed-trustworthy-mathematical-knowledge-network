# Contact freshness and long local verification

2026-10-17. Source-only decision for the ordinary terminal-to-extension path.
No implementation, imports, tests, network execution, proof work or Git mutation.
This does not select a future runtime or enlarge an existing allowance.

## Recommendation

**Stage the selected evidence and its bounded, structurally demanded semantic
closure before the expensive local A verification. Then admit and materialize
using the unchanged live verifier/import rules.** Do not renew contact lifetimes,
invent receipt handles, fetch the whole module, or require old full-context bytes.

This is a general separation between acquiring immutable data and checking it,
not a FIRST/BASE fixture bypass. It removes verification time from the freshness
condition for subsequent semantic downloads. A separately budgeted contact-refresh
facility remains relevant for transfers that themselves exceed contact freshness,
but it is not the smallest repair to the current integration ordering.

## What the actual implementation permits

The current ordinary B strategy does: discover FIRST, `acquire` its packet and
verify A, then resolve the declarations and bodies demanded by `import_context`.
Those later calls still dial the original expiring contact. If A verification
consumes its remaining freshness, correct later downloads refuse.

The limit is an owner-selected advisory freshness bound, not a mathematical
validity lifetime or a globally authenticated wall-clock lease:

- `portable_runtime/location/workflow.py:125` permits descriptor age at most
  60,000ms and computes expiry from descriptor-request issuance, clamped by the
  original workflow deadline. `accept_descriptor` binds its nonce/request,
  authenticated peer, namespace/route and owner egress policy.
- `workflow.py:178` transitions once from LOCATING to SEARCH. Its descriptor and
  route methods subsequently refuse the phase; `begin_search` cannot restart it.
- `client/workspace_atomic.py:508` permits one `find` per client. Its handoff
  prospectively prepays route/descriptor/search capacity, not subsequent grants.
- `delta/transport.py:205` binds the exact workflow, query, configuration,
  deadlines and prepaid ledger; `from_search` at line268 consumes a one-shot
  handoff and snapshots contacts into `_ExpiringContact` wrappers.
- `transport/located_receipts.py:42` checks original acquisition activity,
  contact expiry and egress binding immediately before each HTTP dial. Merely
  retaining a candidate, offer or valid mathematical warrant cannot renew it.
- `transport/receipt_client.py:39` allows external prepayment only while
  acquisition `sequence == 0`. Adding a fresh ledger after acquisition begins
  is not an existing supported API.

Expiry gates **dial start**, not a retrospective invalidation of completed bytes.
An in-flight request still has its original request/operation limits; this
decision does not change that behavior. Acquisition/readback and mathematical
handles remain bounded by their original operation and owner deadlines.

Let descriptor expiry be E, original operation deadline D, and t_j the start of
each selected network dial. The invariant is t_j < min(E,D). There is no soundness
reason to impose t_verify_done < E once all needed data has been retained; live
admission/import must instead finish within D and their original owner limits.

## Alternatives and why the narrower seam wins now

| Option | Benefit | Necessary changes / cost |
|---|---|---|
| Increase or overwrite expiry | Hides the symptom | Rejected: silently changes freshness policy and defeats frozen contact bindings. |
| Restart `find`, grant or owner | Repeats location | Rejected as a repair: current APIs are one-shot; new grants/owners cannot silently replace the original allowance or preserve old live handles. |
| Explicitly budgeted refresh/rediscovery | Supports later new demands, long transfers and replacement providers | Legitimate future mechanism, but needs prospective refresh quotas, allowed phase transitions, authenticated endpoint replacement, binding to original query/candidate identity, no new search allowance, and updated handoff snapshots. Existing APIs do not already implement it. |
| Stage selected immutable closure before checking | Supports slow verification and provider disappearance after acquisition | One structural packet-stage operation, a data-only demand helper, and reordering of the ordinary strategy. Existing cryptographic admission, authoring and contact rules remain intact. |

A future refresh must pay all route/descriptor attempts from finite allowances
reserved before work, retain D, settle failures, preserve the original search
coverage and verify fresh descriptor authentication/egress. Refreshing one known
peer can avoid a new global query, but still needs an explicit transition while
SEARCH/ACQUIRING and a new endpoint epoch bound to that same authenticated peer.
Finding a replacement provider is broader still. Mutating `_expiries`, replacing
the acquisition endpoint dictionary, or reconstructing a handoff is not that
mechanism. No such refresh implementation is selected here.

## Smallest proposed product seam

Use fresh successors if selected; do not edit frozen used sources. This is an API
proposal, not permission to add it yet.

1. Add a public **structural packet stage** operation to the ordinary evidence
   client. `stage(candidate, offered_entry)` uses the candidate's actual
   provider, requires its actual recorded offer, calls the existing
   `EvidenceAcquisition.packet`, and performs `custody_ready` readback. It charges
   ordinary calls/input/store and the existing acquisition ledger. It returns
   an opaque same-client staged token, backed only by an internal exact snapshot
   of the candidate/group/summary and staged packet identity/profile. An inert
   description may expose those data identities and `mathematical_acceptance:
   false`; it is not a LiveWarrant or admission capability transferable between
   clients/restarts. No verifier, verification reservation or cache hit is invented.
   The implementation seam is the download/readback portion of
   `client/workspace_evidence.py:315`, before `_admit_evidence`. Underlying packet
   integrity/custody logic already exists in `delta/transport.py:353` and :367.

2. Add a bounded **structural semantic-demand planner** over actual acquired
   openings/bodies, selected structural module summaries/evidence identities,
   and the locally adopted foundation/policy. Reuse the pure
   `mixed_claims/imports_atomic.py:606` `_build_context` algorithm and its explicit
   context bounds; it has no owner/session callbacks. The foundation decoder at
   line599 is also data-only. Do not impersonate a MixedImportSession, manufacture
   a VerifiedAggregateMember or insert fake receipt fields.

   Use a domain-separated deterministic *data* binding over the actual staging
   inputs internally. Whitelist output: return only
   `NEED_STRUCTURAL_CONTEXT_DATA` or `STRUCTURAL_CLOSURE_STAGED`, a finite demand
   list and structural-work census. Drop the internal `selection_binding`,
   `warrant_census` and other authority-looking fields rather than returning
   the raw helper result.
   Map its `NeedVerifiedMixedMember` to `NeedModuleEvidence` at this untrusted
   boundary. Never expose its provisional context as AuthorContext,
   SealedSelection, live verification, or permission for `author`. Do not return
   the helper's frontend packet as if live import had succeeded.

3. Existing `resolve_declaration` and `acquire_body` already resolve and retain
   exact Merkle-bound groups and committed bodies without mathematical admission
   (`workspace_evidence.py:295`, :306 and `evidence_network/transport.py:56`).
   Apply those operations only to the planner's actual new demands. For a newly
   referenced module obtain its actual provider offer and stage its exact packet;
   no evaluator-supplied hidden module inventory or witness supplies the closure.
   If no selected live provider can supply it, stop with incomplete acquisition.
   Maintain an explicit **staged-evidence module set**. The pure walker's modules
   are just its input item owners: adding a group's module would otherwise
   suppress `NeedVerifiedMixedMember` without any evidence. Every supplied
   module item must therefore have its own exact target packet staged and its
   groups' summary bound to that staged target. A merely fetched group cannot
   turn `NeedModuleEvidence` into a satisfied demand.

4. Once the bounded closure is locally present, call a narrow
   `admit_staged(staged_token, ...)` operation. It requires the exact same-client
   token, consumes its admission transition before verification, re-reads the
   retained exact packet/group, delegates to unchanged `_admit_evidence`, then
   performs actual `owner.open_group` and final live-target checks as `acquire`
   does. Local custody readback does not dial or require an unexpired contact.
   It does still require the same live reader channel and original grant.
   This is more explicit than using `admit_local` and accidentally omitting
   `acquire`'s group-opening evidence. Bind each actual selected J/module/
   foundation/policy to the staged data; a staged J is never trusted as valid.
   Reuse of
   the *same* admitted A receipt for another exact member uses the existing
   live aggregate cache and independently checked membership; it is not another
   proof, nor a structural cache promoted into authority.

5. Call the unchanged `import_context` once with the real warrants and actual
   staged data. It rechecks selected membership, groups, body commitments and
   context closure. Only its live returned context may reach `author`. If it
   returns a missing demand, do not silently download through an expired
   contact: report the incomplete staged closure. A disagreement is evidence of
   a planner/integration defect, not permission to weaken import.

The selected integration therefore becomes:

```text
unknown-ID search -> actual group/offer -> bounded structural staging
    -> local real A admission -> real live context -> ordinary SECOND authoring
```

This does not require changes to portable location, the A relation or verifier,
mixed native checking, publication, or C's already self-contained acquired mixed
packet path. B still uses one actual A verification; selection of BASE under the
same A receipt uses the retained exact-membership/cache rule. C still performs
its independent A plus native SECOND check. No ancestor theorem proof is fetched.

## Required invariants

- **Separate authority:** staged data is content-bound and untrusted. Only actual
  receipt/native admission supplies derivability; popularity, provider identity,
  staging status and the pure planner never substitute.
- **Exact final binding:** final live Js and summaries match the actual staged
  evidence and opening modules; foundation/policy are locally adopted. Different
  representations/proofs cannot be silently substituted between stages.
- **Every module has evidence:** the set of items passed to the preview walker
  is a subset of the actual same-client staged-evidence modules. Groups alone
  do not satisfy a missing-module-evidence demand. Preview completion must
  report this explicit set, not infer certification from the walker's module set.
- **Demand-only semantics:** start from the returned selected declaration group;
  follow its type references and required definition/recursor bodies recursively.
  Opaque theorem proof bodies are not demands. Do not enumerate all module groups
  merely because origin has them. An inductive group remains the codec's atomic
  import unit. The adopted builder includes all supplied groups, so avoid extra
  seed groups and enforce its finite group/declaration/data/work caps.
- **Monotone bounded progress:** deduplicate module/name, group and body identities;
  each incomplete iteration must add a new demanded object or terminate. Set an
  explicit round cap and cumulative request/byte/work ceilings before staging.
  A cap failure is not mathematical nonexistence or permission to renew limits.
- **One operation:** no new owner, grant, search, absolute deadline, verification
  budget, candidate provenance or contact is created by staging.
- **No early reader teardown:** `CommonsClient._active` and the structural
  acquisition's handoff check still require the original reader channel open.
  Provider withdrawal is allowed after staging; closing the reader early is not
  part of this seam. No receipt-stage token survives client close or failure.
- **Persisted-data readback:** packet/group/body stores remain structural and
  separately transactional. Read back exact selected bytes; partial staging is
  retained as untrusted custody, not a successful atomic contribution.
- **Unchanged failures:** stale contacts, malformed or unauthenticated replies,
  commitment mismatches, owner/source drift and cancellation retain existing
  fail-closed semantics and charges. Current search-only recoverable refusals do
  not automatically make semantic HTTP failures recoverable.

## Cost and operability argument

Let S be bounded discovery/acquisition plus structural closure work, V the local
verification cost, and M final live import/authoring. The new ordering is S;V;M.
Both phases share D and their original budgets. Unlike verify-then-fetch, no dial
time includes the elapsed V. Thus arbitrary V within the selected owner/grant
allowance no longer causes later required semantic dials to inherit stale hints.
This is an ordering/locality argument, not a claim that S fits 60 seconds.

Network content is proportional to selected evidence, selected declaration groups
and required computation semantics, not all knowledge or theorem-proof ancestry.
If R bounded planner rounds each revisit at most W selected expression nodes,
the simple reused planner may cost O(RW), in addition to bounded canonical/hash
and foundation-decoding work. Do not advertise a linear incremental algorithm;
the final live materialization is another separately charged traversal. Each
preview call/input and its repeated scans consume the original client's call,
input, controller-CPU and wall budgets. Per-call walker caps must not reset the
operation's cumulative limits or make the work unaccounted.

Staging may waste more bandwidth on invalid evidence: a bad receipt is discovered
after its bounded semantics were downloaded. Against verify-first, the extra
invalid-input cost is at most the selected staging allowance, not unbounded remote
work. In a mixture with invalid fraction p and semantic cost S_sem, the additional
expected semantic expenditure is approximately p*S_sem, subject to the stated
workload model. No measured values or net growth claim follow. Early cheap packet
shape, summary, membership-opening and commitment checks should reject obvious
invalidity before expensive staging; those checks remain structural.

Once all needed data is retained, disappearance of the original provider need not
prevent admission/import; the original reader channel and local owners must still
satisfy their existing lifecycle contracts. This helps useful reuse even when
verification is slow, without adding a central service or trusted provider.

## Remaining limits and next discriminator

An enormous selected semantic closure or sufficiently slow network may itself
outlive 60-second contacts. Staging does not solve that; a future explicitly
budgeted authenticated refresh/alternative-custodian seam is then necessary.
Unknown later research demands likewise require a later authorized acquisition,
not an automatic continuation from this finite closure. Neither outcome requires
downloading every theorem or choosing a global task list.

Before implementation: independently challenge the staging/live-import boundary
and confirm reuse of the pure context walker cannot manufacture authority. After
separate root source selection, the minimal changed-boundary discriminator is:
structurally stage before expiry, perform a simulated long local check, and show
no later network dial is required; reject a staged missing/mismatched member or
body at final live import. Such inert tests must not be called real A evidence.
The genuine terminal gate remains separately blocked on a real A receipt and
finite runtime selection; no campaign is started by this note.
