# Independent contact-lifetime design challenge

2026-10-17. Reviewer: `memo_independent_review`. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
Root assignment: challenge the smallest sound product seam for acquiring
selected semantic data when an A receipt check may outlast the unchanged
60-second descriptor contact. Source/theory only; no runtime, tests, build,
proof or Git mutation. The separately launched root compile is not this task.

## Decision

**Bounded structural staging before mathematical admission is a sound and
smaller candidate than introducing contact refresh into the present one-shot
protocol.** This review supports the principle, not an unimplemented source
success or a guarantee that every finite closure fits the contact window.
The final decision checkpoint is reviewed below; any implementation still
requires separate source review. No fake warrant, silent lease extension or
new grant is justified.

The existing candidate/export, exact-name declaration and body APIs already
download and commit untrusted structural mathematics before it is accepted.
`EvidenceAcquisition.packet` similarly provides exact offered packet transfer,
hash checking, store commit/readback and no verifier, but the ordinary client
currently combines that transfer with immediate checking in `acquire`.
`admit_local` already checks exact locally held packet bytes through the same
actual I/A/mixed admission rules. Thus exposing a bounded structural packet
stage need not create a second mathematical acceptance path.

## Source facts behind the timing constraint

Inspected the actual portable `location/workflow.py` and the existing
`delta/transport.py`, `transport/located_receipts.py`,
`transport/receipt_client.py`, `client/workspace_evidence.py`,
`client/workspace_mixed.py` and `mixed_claims/imports_atomic.py` contracts.

- The descriptor ticket expiry is bounded by 60 seconds and the original
  workflow deadline. Acquisition copies the resulting contact expiry once.
- `_ExpiringContact.validate` checks the original acquisition grant, expiry
  and egress policy immediately before dialing. This grants a bounded request
  start; it is not a theorem that an already-started transfer finishes before
  that timestamp. Existing request/grant timeouts still bound completion.
- Contact freshness authorizes dialing. It is not the lifetime of immutable
  held bytes or of a subsequently produced mathematical warrant.
- Local admission and import do not validate the endpoint again. They still
  require the original grant/owners and the same live reader channel through
  `EvidenceAcquisition._active` and the prospective handoff. Consequently the
  channel cannot simply be closed after staging under the current APIs.
- `find` is one-shot; the workflow moves into SEARCH; acquisition consumes a
  one-shot handoff; its prepaid configuration is frozen; additional external
  prepayment requires acquisition sequence zero. A refresh design must address
  these facts explicitly rather than changing only a timeout constant.

The integration's present dependency is therefore scheduling, not a need to
weaken verification: it checks A before discovering/fetching semantics, which
makes those later network requests wait on the check. Moving bounded untrusted
data acquisition before the expensive check removes that particular dependency.

## Soundness argument and required boundaries

Let U be bounded, untrusted staged packets/openings/bodies. Let W be actual live
warrants obtained by the unchanged admission rules on exact staged packets.
Let C be the result of the unchanged live import/materialization rules applied
to W and the exact staged data. The proposed implication is only:

```text
staging(U) succeeds                 => structural data is locally available
admit_exact(U) succeeds             => corresponding actual live warrants W
live_import(W, U) succeeds          => existing checked-import obligations hold
```

The first line implies neither later line. Staging must not mint W, a
SealedSelection, an AuthorContext, a context READY token or a transferable
certificate. If admission fails, no stage output repairs or bypasses it.
Conditional on the existing admission/import soundness assumptions and their
exact-byte bindings, adding the first line cannot create an accepted theorem
that bypasses those checks. It can waste bounded resources on invalid data;
that is a separate efficiency concern, not mathematical authority.

Required implementation conditions:

1. A public packet-stage method binds an actual candidate to an actually
   offered exact `(hash, bytes)` entry, performs the existing transfer and
   custody/summary readback, and returns inert structural identifiers only.
   It must use the original call/input/store/network allowances and charge
   unsuccessful attempts. No verifier call, warrant or hidden automatic retry.
2. Any pure semantic scanner validates selected opening/body structure and
   commitments under adopted foundation/policy data and finite byte, group,
   declaration, expression, demand and iteration caps. It follows types and
   definition/recursor semantics, not opaque ancestor theorem proofs. Its
   closure is selected declaration closure, not minimal evaluation semantics.
3. `_build_context` is reusable pure logic, but its `modules` set comes from
   every supplied item, not from an evidence/warrant check. Merely fetching a
   group for a module must not suppress that module's needed evidence packet.
   Track an explicit staged-evidence module set and exact packet identities;
   enforce that every module selected for live import has its corresponding
   staged packet. `NeedVerifiedMixedMember` may become a data-only
   `NeedModuleEvidence` demand; it must not become a claim of verification.
4. Do not expose the pure builder's packet, selection binding or
   warrant-looking census as an authoring credential. Whitelist only
   `STAGING_*` status, data demands and clearly structural census fields.
   Existing pure foundation identifier views contain data only and need no
   forged owner/session.
5. After real admission, bind actual whole journals, summaries and module IDs
   to the staged selections. Pass the actual warrants and exact held data to
   unchanged live `import_context`. Its rechecks are mandatory even if the
   scanner predicted complete closure. A mismatch or new unsatisfied demand
   must be explicit failure/remaining work, never implicit authority.
6. Keep the original reader, grant and owners alive until their normal close.
   Repeated scans and data submissions consume the same controller/input/call
   and enclosing Job budgets; local per-call caps are not fresh global credit.

## Operability and efficiency limits

Staging does not guarantee arbitrary selected closures can be acquired within
one 60-second contact. It reduces the required pre-expiry work from
`discovery + A check + acquisition` to `discovery + acquisition`, where expiry
is checked at each actual dial. Acquisition may still exhaust contacts, bytes,
calls, storage, expression work or the original grant. It must then refuse.

Invalid candidates can induce speculative semantic downloads before their
certificate is rejected. Fixed aggregate budgets, monotone deduplication and
no automatic candidate retry bound that downside; they do not prove useful
growth or universal latency. Reuse should be evaluated against the same exact
data, grants and local checking baseline rather than claiming speculation free.

This is not a global prefetch scheme. It should start only from the chosen
returned declaration and follow bounded structural demands. Known target IDs,
all-BASE bundles and the author source must not be injected into the unknown-ID
chooser merely to make the staged closure match the retained fixture.

If acquisition itself proves too long, an explicit bounded refresh/reacquisition
design may later be necessary. The present diagnosis does not justify building
that larger protocol first, nor does it forbid it as a future decision.

## Final proposal challenged

Read all of `CONTACT-LIFETIME-DECISION.md`, 16,464 bytes, SHA-256
`499ef67e2836977e31435130f049d0082a4cea582d6aaee5f00159b600cb945b`.
**No blocking theoretical defect was found in its proposed staging/admission
separation.** The author incorporated the explicit staged-evidence module set,
pure-output whitelist, original-reader lifetime, actual dial-start interpretation
and cumulative accounting conditions raised during review.

Root's proposed exact API is stronger than this review's initial minimal
stage/read-local formulation: `stage_packet(candidate, entry)` returns an
opaque same-client `StagedEvidence`; `describe_staged` exposes inert data;
`admit_staged` rereads its exact custody snapshot, consumes an admission
transition before checking, delegates to unchanged `_admit_evidence`, and
performs the same actual `owner.open_group` and final target checks as acquire.
That preserves the candidate/group binding as well as packet identity. It is
an appropriate narrow choice; no serializable report becomes authority.

The accompanying bounded `preview_context` may take explicit staged tokens and
selected openings/bodies. A pure helper may return only
`NEED_STRUCTURAL_CONTEXT_DATA` / `STRUCTURAL_CLOSURE_STAGED`, data demands and
structural census. No returned packet, authoring view or selection binding is
needed. The final actual import remains responsible for mathematical authority.

Additional concrete implementation obligations sent to root before selection:

- **Whole-J variant ambiguity:** the same ModuleID can have distinct exact
  derivations/journals. Multiple staged tokens for one module must be rejected
  as ambiguous or require an explicit exact-J choice, never silently overwrite
  each other in a dictionary keyed only by ModuleID.
- **Token lifecycle:** stage maps require the same-client identity check,
  bounded census, no use after close/failure, and explicit revocation/clearing
  on inherited failure and close. A consumed admission transition cannot be
  retried by returning to STAGED. Same-live A reuse is still the existing
  verifier cache, not this structural token map.
- **Source and resource closure:** fresh successor sources/imports must be
  selected and bound to the actual owner source maps. Staged snapshots and
  repeated preview submissions/work must remain inside the original limits;
  per-call walker caps alone are not aggregate accounting.

This is enough to proceed to a narrowly scoped source implementation, not to
launch a proof, change any frozen class, or label the genuine terminal gate
successful. A subsequent changed-boundary control can simulate expiry/slow
checking without waiting a minute or running a real prover; it must keep its
synthetic status explicit. The actual A/H2 receipt and real integration remain
separate necessary evidence.
