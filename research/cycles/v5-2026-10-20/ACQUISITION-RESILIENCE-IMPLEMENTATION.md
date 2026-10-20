# Semantic-body attempt continuation: implementation and API

2026-10-20, `core_search`. Implements only the three files assigned by
ACQUISITION-RESILIENCE-SELECTION. Source-only checkpoint; no test or other
runtime was executed, no Git index changed, and no used predecessor edited.

## Public shape

The fresh logical `client.workspace_evidence` overlay adds:

```python
await client.try_acquire_body(candidate, digest, max_bytes=cap,
                              supplier=existing_contact,
                              attempt_timeout_ms=5000)
```

It returns `status == "BODY_CUSTODIED"` plus the existing validated body on
success, after actual structural custody commit and readback. A selected
pre-custody transport failure returns this exact data-only shape instead:

```python
{
    "schema": "DMKN_SEMANTIC_BODY_ATTEMPT_V1",
    "status": "UNAVAILABLE_AT_SELECTED_SUPPLIER",
    "supplier": existing_contact,
    "reason": "PEER_EOF",  # or the narrowly classified reasons below
    "request": {"module_id": module, "relative_name": name,
                "universes": arity, "body_hash": digest},
    "settlement": "FULL_REPLY_RESERVATION_CHARGED",
    "global_complete": False,
    "mathematical_acceptance": False,
}
```

The fresh logical semantic helper adds:

```python
await reader.try_fetch_body(demand, max_bytes=cap,
                            supplier=existing_contact,
                            attempt_timeout_ms=5000)
```

It returns the same refusal unchanged, or the previous `FETCHED`/`NO_PROGRESS`
success shape. The caller decides whether and where to make another attempt.
Old `acquire_body` and `fetch_body` retain their fail-stop behavior unchanged.

## Boundary and reuse

`transport/acquisition_resilience.try_body` takes the **actual existing**
EvidenceAcquisition and its exact `_SharedAcquisition`/AcquisitionBudget.
It creates no acquisition subclass, budget, grant, source callback or issuer.
Both located `_ExpiringContact` and the exact ordinary direct `_Contact` are
supported; no arbitrary subclass is accepted. Original endpoint/policy/direct
binding, owners, caps and deadlines are checked before/after the attempt.

The existing route-neutral `search_resilience._response` parses HTTP. A small
body-only exchange owns the stream and positively observes `wait_closed`.
Only refused connect, clean incomplete-read EOF, acquired-stream reset,
broken pipe, acquired-stream timer expiry, or complete HTTP 404/503 can return
a refusal. Protocol errors, connect/handshake timeout without an owned stream,
cancellation, unknown close, policy/expiry/budget errors and malformed/hash-
invalid successful body remain exceptions. Full HTTP 400 remains fatal too.

The shared budget reserves before dial; the existing structural counters also
reserve and advance. Refusals consume the full maximum reply allocation in
both layers, even for a short explicit 404. All exits settle the shared ticket
and structural reservations; final normal returns verify exact accounting and
zero inflight/pending state. Complete reply/header observations remain separate
from conservative charges. No bytes from a refused attempt enter custody.

Success reuses descriptor-permitted-hash checking and `validate_body`. The
facade performs the original `put_body`/readback/active checks outside any
recovery catch. Store/commit/readback, input charging and final source checks
can still fail-stop. A helper refusal does not modify selected groups, bodies,
pending demand, member selection or revision; normal call/step/input/network
costs still accrue. In particular `_group(data)` is postponed until success.

The facade requires preselected pins for the new helper and eight reused source
modules, including the response parser and direct-contact guard. It does not
adopt arbitrary code by hashing it. The imported `try_body` symbol and reused
response parser identity are checked, and the regular source-origin/hash gates
run before and after the operation.

## Source map and review state

Logical replacements (fresh originals, mapped by root's ordinary selection):

- `client/supplier_resilient/workspace_evidence.py` -> `client/workspace_evidence.py`.
- `client/supplier_resilient/semantic_reader.py` -> `client/semantic_reader.py`.
- New `transport/acquisition_resilience.py` stays at that logical path.

Initial coherent identities, before independent review:

| File | Bytes | SHA-256 |
|---|---:|---|
| `transport/acquisition_resilience.py` | 12,484 | `43fa1acd66219c7d28a37a263dee04a20edd993bd24383c54680aa303202c09d` |
| `client/supplier_resilient/workspace_evidence.py` | 35,951 | `22c01a28de725d85b6a23de59eb3d0e7511b8d33b9f84f4eb9c4cd192128b099` |
| `client/supplier_resilient/semantic_reader.py` | 26,030 | `dd5805371d31d852f78efcfe156f6c78c5bbf71b3e4ee2d5ca17da91422608ad` |

The final preselection source contains two small hardenings: validate the
attempt timeout even when the semantic body is already cached, and check the
original supplier binding even when the caller omits an explicit supplier.
Final identities submitted to the reviewer are:

| File | Bytes | SHA-256 |
|---|---:|---|
| `transport/acquisition_resilience.py` | 12,484 | `43fa1acd66219c7d28a37a263dee04a20edd993bd24383c54680aa303202c09d` |
| `client/supplier_resilient/workspace_evidence.py` | 35,948 | `a7c4979c35e904f096cba23b7fcb5cb8361e4679fc16d37d2fcec69041afd5ab` |
| `client/supplier_resilient/semantic_reader.py` | 26,114 | `9b82de53bdcc8db74908622fc43c965a7b003111a752a8f579d25b5964dffe60` |

The facade/helper differ from their frozen supplier-selected predecessors by
52 and 50 added lines respectively. Focused controls and independent review
are assigned separately. Passing those controls would establish the changed
continuation boundary, not new mathematical verification, net useful growth,
new contact discovery or final v5 readiness. No broad replay is needed.
