# Contact refresh: independent design challenge

2026-10-28, query_scaling. Source/theory review; canonical guard passed. Reviewed
NEXT-CORE-DECISION.md `4323b97bbda77b39e3438243f3b4233d50df374a92694339406a1fbec09d4af4`
and root's subsequent `ordinary_registration_refresh/SELECTION.md`. No runtime,
owner/database/network access, imports, tests or Git in this review.

**Support the selected existing-contact composition.** The principal objection
to the earlier design is resolved: exact known-route pulls already have an
authenticated, nonce-bound `/v5/ordinary/contacts` exchange. A separate registration
wire protocol, complete-feed revision ledger and persistent high-water state
would add machinery without establishing truthful or available service. The
selected single `directory-refresh-serve` operation needs none of them.

## Does this remove manual coordination?

Yes, within an explicitly delegated scope. A registrar approves feed origins,
routes, endpoint authority and quotas once per policy revision. Thereafter the
provider edits its own feed and the next invocation applies the approved policy
without a registrar copying or approving each advertisement. Onboarding a new
principal or route remains manual. Providers must still maintain their own maps
and run reachable feeds. The saving is repeated cross-operator coordination,
not universal automatic discovery or elimination of curation.

This conclusion depends on actual fresh fetching and serving in one invocation.
An offline merger that still needs a registrar to import every provider update
would merely move the work. A fresh response from a live provider can repeat an
old configuration; nonce freshness does not detect that or prove liveness.

## Conditions that close concrete counterexamples

| Counterexample | Required disposition in the selected change |
| --- | --- |
| Two individually legal feeds each return sixteen endpoints for one route. | Validate the sum of per-route slot quotas <=16 before I/O. Do not choose by arrival order, silently expand a quota or fail only after spending the refresh budget. |
| A response names a new feed URL, CA file, path or namespace. | Payload labels convey no authority. Poll only configured authenticated origins; compile only approved exact routes; apply local endpoint policy. The registrar never dials learned contacts. |
| A missing or truncated feed is treated as a complete replacement of global state. | Fresh returned subsets are the only eligible contribution. Preserve unavailable, invalid, truncated and successful-empty outcomes separately. No cached fallback or global-absence inference. |
| Every slot is empty, expired or unavailable. | Return an explicit closed no-listen result. Distinguish complete selected-slot emptiness from an incomplete refresh; no fake row or old-map server. |
| One nearly expired slot ends an otherwise useful service immediately. | Omit slots below the policy's minimum remaining useful interval at assembly and readiness. Only retained contributions determine the cutoff; duplicate provenance never silently renews an earlier included horizon. |
| Reply construction runs beyond an asyncio lease while synchronous work prevents cancellation. | Enforce the cutoff in direct contact dispatch, during ContactMap reply construction and in contact HTTP write callbacks. A timer alone is insufficient. |
| A write drains across the cutoff before the next chunk is enqueued. | Check the combined contact/operation budget immediately before every chunk and after awaited drain. Keep already charged bytes charged; close through existing bounded cleanup. |
| A reader receives a hint just before cutoff. | Its existing request-start horizon can still permit later use, currently up to sixty seconds. Directory cutoff is not client revocation or endpoint-liveness proof. |

Root resolved the final wording ambiguity by selecting per-chunk checks. The
claim is a monotonic check immediately before each new application enqueue,
under the existing execution assumptions. It is not hard real-time scheduling
or final-byte-arrival assurance: bytes already queued can arrive later.

## Smallest coherent implementation boundary

Reuse `fair_exchange.exchange`, the Contact Request/Reply parser and immutable
ContactMap. Add bounded policy validation, same-invocation slot retrieval and map
assembly to the peer API, plus one public composition route. Add the optional
`Provider(contact_deadline=None)` and internal `directory_serve` cutoff seam;
default None and noncontact services retain their current behavior. Report the
effective clipped interval separately from the requested lease. No public
configuration may invent a later refresh horizon.

The existing separate `directory-serve` endpoint can supply feed replies. Do not
imply that public ordinary `peer.serve` already advertises a contact map merely
because the lower-level Provider can combine roles. No producer operation,
owner-state migration, native bundle change, signature service or new trust
mode is needed for this initial composition.

The cost is bounded metadata refresh plus finite service on every cycle. The
existing caps (32 requests, 1 MiB aggregate reply reservation, 32 KiB per reply,
2 MiB map, 2,048 keys and 16 endpoints per key) limit work and spam within one
approved policy; they do not bound a whole network or confer relevance. A narrow
later control should exercise these new policy/expiry/composition seams, reusing
existing transport evidence. This checkpoint is a design verdict, not measured
benefit or release qualification.

Source anchors: `ordinary_contact_federation/contact_directory.py`;
`ordinary_multi_source/peer_api.py:206-477`;
`ordinary_reply_capacity/http_provider.py:125-127,412-418,500-568`;
`ordinary_sparse_access/fair_exchange.py`.
