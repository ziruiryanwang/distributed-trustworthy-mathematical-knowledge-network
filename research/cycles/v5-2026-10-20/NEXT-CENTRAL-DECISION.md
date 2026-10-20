# Next central step: remove single-provider semantic closure

2026-10-20, `core_growth`. Source-only recommendation after the selected
semantic-reader integration; no implementation or runtime is selected here.
Canonical workspace guard passed. Full v5 release obligations remain open.

## Decision

**Allow the local agent to choose an already authorized supplier separately
for each exact dependency demand.** Keep one operation, one aggregate budget,
the original contact expiries, and unchanged mathematical admission.

The current reader can obtain a target from an index, but its semantic walk
implicitly requires the target's provider to supply every missing declaration,
body and newly needed evidence packet. A large distributed library need not
have such a provider. Consider a target packet at P and a required transparent
base definition held only at Q. Even when both contacts are already authorized,
the present helper routes the exact base demand back to P. This is a genuine
composition restriction, not a RAM problem or a need for another proof campaign.

## Source basis and smallest change

- `client/semantic_reader.py:resolve` always passes `self._origin` to
  `resolve_declaration`. Its names are cached by mathematical address, while
  the retained candidate also binds a supplier.
- `client/workspace_evidence.py:resolve_declaration` obtains that supplier from
  the origin candidate; `acquire_body` and `packet_offers` likewise inherit a
  candidate's provider. The current method is explicitly same-contact.
- `evidence_network/transport.py:EvidenceAcquisition` and
  `transport/receipt_client.py:_SharedAcquisition` already accept a provider
  argument and share the original acquisition ledger.
- `client/direct_contacts.py` already binds multiple exact owner-approved
  contacts, endpoint/egress policy and expiries. The located handoff also lends
  its selected contacts. No new DHT, endpoint registry or network protocol is
  needed for this step.

Add a selected successor at the public client/helper seam, not a second
acquisition stack. Expose explicit supplier choice for exact-name, body and
evidence-offer retrieval, defaulting to the present origin where appropriate.
Separate semantic deduplication from supplier choice: an already known
declaration must not prevent fetching its committed body or evidence from
another authorized holder. Never mutate a candidate's recorded provider to
simulate this capability.

The API design must preserve:

1. Exact mathematical addressing and commitment checks. Changing supplier
   cannot change the expected module/name/group, universe arity, body hash,
   selected journal or chosen packet variant.
2. Original contact authorization, predial egress/expiry checks and finite
   shared charging. No raw remote URL, new grant, refreshed deadline, silent
   referral, implicit retry or changed proof form.
3. Structural data before actual checking; final live warrants still come
   only from unchanged I/A/native admission and import.
4. Honest failure scope. This first increment need not reclassify existing
   fail-stop acquisition errors. Explicitly choosing Q beforehand must work;
   surviving a failed P request requires a separately justified typed-failure
   boundary and is not implied by supplier choice.

## Why this outranks the alternatives now

Ordinary construction, retained-workspace serving and demand-directed local
closure have already been implemented or selected. Another cost calculator
would duplicate the existing full-cost theory and v4 advisor without supplying
an optimized comparator. Another packaging or passing-workflow replay would
not remove the one-supplier assumption. This change directly permits modular
reuse across independently held portions of mathematics, using existing
transport and authenticity mechanisms and small local state.

For a fixed selected closure, mathematical acceptance is supplier-independent:
the checker consumes the same authenticated content regardless of its transport
origin. This does not prove source availability or global source discovery.
Work remains bounded by chosen demands/attempts and the original grant; do not
claim optimal search or linear total preview work.

The genuine scalable-A lane is separate and still mandatory. There is a genuine
I receipt but no genuine A receipt; retained producer lifecycle and unexecuted
po17 layout are not that evidence. Do not restart layout, proving or RAM polling
to implement this ordinary software capability, and do not count I/native
success as ancestry-cutoff certification or positive full-cost growth.

## Decisive check and stopping rule

After source review, use focused cheap controls for cross-provider exact
binding, same-provider compatibility, unauthorized/expired contact refusal,
shared-budget exhaustion and unchanged admission. At most one later local
split-custody check should reuse retained mathematics: P offers the target but
does **not** possess a demanded body; Q alone serves that exact body; the fresh
reader obtains the same warranted context with no new proof or authoring.
Provider inventories must establish the split, not merely count two endpoints.

Stop this increment when explicit split-custody retrieval and its unchanged
trust boundary are supported. Do not grow it into automatic routing, ranking,
replication, failure recovery, new corpus construction or another full
reciprocal campaign. If source review finds this already supported through an
ordinary public API, reject the proposal as duplication and document that exact
call path instead. Root owns selection, implementation ownership and runtime.
