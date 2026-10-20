# Explicit semantic suppliers within one operation

2026-10-20, core_search. Source-only implementation under
[the root selection](SPLIT-CUSTODY-SELECTION.md). No source import, tests,
native/proof work, installation, original-state mutation or Git changes.

## Existing-path check and concrete gap

The ordinary client can already resolve a returned index record at an explicitly
named provider. More precisely, `DeltaAcquisition.export` checks membership of
`(object_id, record_id)` in the originating search session, not membership keyed
by the supplier label. Therefore `resolve(Q, record_from_P)` can work when Q holds
that exact already-returned group. It is incorrect to claim that every
cross-provider resolution was impossible.

That path does not generally suffice for exact dependency demands. Q may hold
only a needed base group/body, have no indexed result, and not hold the returned
target group at all. The old public `resolve_declaration` fixes its supplier to
the origin candidate; `acquire_body` fixes it to the held candidate. The helper
additionally caches just one candidate per mathematical address. The existing
lower acquisition stack already supports selected authorized suppliers and the
same budget. We extend only its ordinary client/helper access.

## Files and API

Two fresh exact baseline copies, then narrow edits:

| New source | Logical installed/source-map replacement | Baseline SHA-256 |
|---|---|---|
| `software/v5/client/supplier_selected/workspace_evidence.py` | `client/workspace_evidence.py` | `1bdc7dfb6058c0057eb8fe56daf0f370941d275538b6cb7ab964a455a9646f8e` |
| `software/v5/client/supplier_selected/semantic_reader.py` | `client/semantic_reader.py` | `175de65f72f056681237387c854d21671d7b3787b61f6685789a382b8a06ae18` |

The logical overlay preserves existing exact validated-client types, imports
and required source paths. It does not monkey-patch a running mathematical
owner or relax source checks.

New optional keyword `supplier=None`:

```python
await client.resolve_declaration(origin, module, name,
                                 max_bytes=limit, supplier="Q")
await client.acquire_body(candidate_from_P, body_hash,
                          max_bytes=limit, supplier="Q")
await helper.resolve(current_demand, max_bytes=limit, supplier="Q")
await helper.fetch_body(current_body_demand, max_bytes=limit, supplier="Q")
```

`client.check_supplier("Q")` is a synchronous, no-I/O live-contact check.
It consumes an ordinary facade call and submitted metadata, returns only
`AUTHORIZED_LIVE_CONTACT` data, and neither reserves a network attempt nor
returns an authority token. The helper calls it for every explicit choice,
including cached/no-progress branches. It must not silently ignore an
unauthorized or expired supplier merely because it already has the bytes.

No extra packet API is needed:

```python
resolved = await helper.resolve(current_module_demand,
                                max_bytes=limit, supplier="Q")
offers = await client.packet_offers(resolved["candidate"], ...)
# Caller chooses an exact returned entry; the helper never chooses a variant.
await helper.stage(resolved["candidate"], chosen_entry)
```

Resolving at Q actually requests Q's exact-name opening and mints a new
Q-origin candidate. The original P candidate and its origin remain unchanged.
Existing packet-offer selection and staging then use Q normally. No Q index
hit is fabricated.

## Mathematical identity is separate from supplier

For a mathematical address `(module, name)`, an additional supplier candidate
must agree exactly with the first held candidate's locator, group opening and
descriptor. Descriptive metadata about how the candidate was acquired may
differ. The helper keeps:

- A first candidate per mathematical address for default body requests.
- Bounded candidate variants per `(supplier, module, name)`.
- Groups and bodies deduplicated by their existing mathematical keys.

Thus knowing a name at P does not prevent requesting it at Q for evidence.
The existing `names` limit bounds **all supplier variants**, not just distinct
names; each retained description consumes the original byte cap. There is no
unbounded contact-by-name product hidden behind one name count.

For a body request, Q need not redundantly supply the name opening. The already
held P descriptor fixes the module/name/universe/body commitment, and the
unchanged transport validates Q's response against it before custody.
Neither candidate identity nor mathematical acceptance is reassigned to Q.
If the body is already held, `NO_PROGRESS` does not claim that Q supplied it.

Conditional on the unchanged commitment/checker assumptions, mathematical
acceptance depends on exact checked content and its live warrant, not the
transport supplier. This is not an availability theorem or supplier honesty
assumption.

## Original authority and resource boundaries

An explicit supplier must be in both the acquisition contact map and the
originating search's adopted contacts. The selected contact must be the same
object used by structural acquisition and bind the original budget, endpoint,
policy and minimum of original contact/operation expiry. Unknown, replaced or
expired contacts refuse; this code creates no URL, contact or allowance.

Actual requests still use the existing guarded endpoint immediately before
dial, after the existing shared attempt reservation. The helper's earlier
no-I/O validation is not a replacement for that check. No new search session,
grant, budget refund or deadline extension is introduced. Ordinary facade
fail-stop behavior is unchanged: choosing Q in advance is supported; retrying
Q after a failed P call is not promised.

`supplier=None` preserves the previous policies: name resolution uses the
origin candidate's supplier, while body retrieval uses the first held name
candidate's supplier. On default-only use the original call signatures and
submitted metadata are retained. Explicit supplier metadata is charged only
when selected.

Admission, staged-member inventories, exact journal selection, packet variant
binding, I/A/native checking and final live import are unchanged.

## Review candidate identity

- Evidence overlay: 32,729 bytes; SHA-256
  `0b4c9f191fdc96c94b61d7834a5cf11d404b0c6553eb12658ea0a54b1536109c`.
- Helper overlay: 22,778 bytes; SHA-256
  `c71feed31c152f587851f537598ff4dcd3472380050f777783fc22a7a61354cd`.

Independent review and focused controls have separate owners. Root selects
any finite runtime. The decisive later run must establish that P genuinely
lacks a demanded body and Q supplies it, not merely that two endpoints exist.
No aggregate-A production, automatic routing/failover, full-cost growth or
public release claim follows from this source increment.

## Next marginal-payoff recommendation after this feature

Return to the **genuine A capability boundary**, not another client helper.
The installed constructor, contribution, retained serving and actual semantic
demand path now exist; split suppliers removes a real further restriction.
None has produced the required ancestry-cutting A receipt.

The cheapest currently prepared decision is the already reviewed, never
executed fixed-po17 H2 layout: see
`../v5-2026-10-17/GEOMETRY-LAYOUT-EXACT-REVIEW.md`, selection `a717a88a`.
Its host is already built. The analogous retained selected-frontier layout
used 3.53125 inclusive Job CPU seconds and 93.78125 MiB peak Job commit;
this supports considering the small execution-only decision, not predicting
its exact count or proving a peak bound. One normal existing launch guard is
enough. If it refuses, defer immediately: no RAM investigation, repeated
polling, cap ladder or proof campaign follows.

Exact retained references, relative to the canonical root:

- `experiments/v5-local-checks/selected-frontier-layout-01/RESULT.json`,
  SHA-256 `f11c567f70d5543fe648f32df2bb254736deada086bcc40e3f6b01c87d493d6f`.
  Its actual peak is 98,336,768 bytes. Its separate outer-wrapper CPU is
  0.296875 seconds; the quoted 3.53125 is explicitly the inclusive Job,
  not an all-process total.
- `experiments/v5-local-checks/geometry17-layout-01-selection.json`,
  SHA-256 `a717a88af4df86338888582ad48dbaad7dccdce7c307d471d51828c0bc071aa4`.
- `research/cycles/v5-2026-10-17/GEOMETRY-LAYOUT-EXACT-REVIEW.md`,
  with the exact 28 source/88 runtime pin and profile checks.
- `research/cycles/v5-2026-10-17/GEOMETRY-LAYOUT-PLAN.md` and
  `GEOMETRY-RUNTIME.md`, preserving the execution-only scope and prior
  prelaunch deferral without execution.

A complete new capsule would provide actual segment/count/geometry input for
the missing po17 stage-host/producer and complete-path funding decision.
It would not itself be a certificate, and those later steps must not be
implemented on the assumption that an unexecuted layout succeeded.

For growth, reuse the existing `GROWTH-WORKLOAD` and `GROWTH-CRITICAL-PATH`
theory. Another cost inequality or popularity calculator adds no evidence.
The current tiny native method does not support a positive certification
margin merely because more consumers exist. The next independent
implementation, if A must be deferred, should be the optimized ordinary
shared-library comparator **O** using the same installed semantic endpoint,
initial cache/endowment and allowed local optimizations. That supplies the
missing comparison needed to decide a full-cost region, rather than another
unmatched v5-only timing. Its exact design/source selection belongs to root.

This is a source/evidence recommendation only. No layout, benchmark, proof
or new comparator implementation was run or authorized by this appendix.
