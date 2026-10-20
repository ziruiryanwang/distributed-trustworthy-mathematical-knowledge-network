# Demanded-body acquisition resilience: independent review

2026-10-20, `core_release`. Canonical guard passed. Source-only review under
ACQUISITION-RESILIENCE-SELECTION.md; no imports, tests, runtime, memory work or
Git changes. Current disposition: **source review clear and the single selected
control outcome independently audited PASS within its stated inert-authority
scope**. This is not release clearance. Root alone owns selection, execution
and adoption. Source clearance and subsequent outcome audit are separated below.

## Principle and existing boundary

The proposed normal refusal concerns only one selected body's transport before
any body validation or custody write. It does not justify continuing after an
invalid committed body, a failed database commit/readback, changed source/owner
bindings, cancellation, expired authorization or uncertain socket cleanup.
Those cases continue through the facade's existing fail-stop wrapper.

The unchanged `EvidenceAcquisition` uses an exact `_SharedAcquisition` plus one
original `AcquisitionBudget`. The former already records structural request,
reply, reservation, inflight and failure counters; the latter accounts the
shared discovery/acquisition/verification grant. A continuation must settle both
layers without refund or replacing either object. Counting a refusal as a
normal return does not make it free or let another request overlap it.

Under those invariants, a clean P refusal has the state transition

```text
(live authority, selected semantics, pending demand, remaining budget)
  -> (same authority, same semantics, same demand, budget minus charged attempt).
```

A subsequent caller-selected Q request is then a separate charged operation,
not an automatic retry. If Q returns exact valid bytes and enough original
resources remain, the existing commitment/custody checks can advance the helper.
This removes a failed-supplier prerequisite, not a proof that Q exists or that
discovery is complete. Neither response gives new mathematical authority.

## Source inspection obligations

- Fresh logical replacements only; frozen supplier-selected source unchanged.
- Every new executable helper participates in the actual issuer source-pin
  closure before requests, including the reused route-neutral response parser.
- Exact original acquisition, structural object, adapter, contact, policy,
  search/handoff, shared budget and deadlines. No alternative endpoint factory.
- Reserve before dial, validate the actual guarded contact immediately before
  connection, settle exactly once, and recheck unchanged bindings with no
  pending shared reservation or structural inflight work before refusal return.
- Full selected reply allowance charged on a refusal at both accounting layers;
  any actual observed bytes remain separately labelled, not invented.
- Selected refusal classes only; no recovery around body parsing, commitment
  validation, custody, readback or ordinary client's final activity checks.
- The real absent-body provider behavior can be EOF. A returned writer must
  close and complete `wait_closed`; cancellation or uncertain closure remains
  fatal. Failed connection cleanup assumptions must be stated explicitly.
- No helper group/body/member/candidate/demand/revision mutation on refusal;
  facade calls, helper steps and consumed network counters still advance.
- Success preserves exact module/name/universe/digest/descriptor checks and
  performs the existing custody/readback before returning usable structural data.

Inspected unchanged references: `transport/search_resilience.py`,
`transport/clients.py`, `transport/receipt_client.py`,
`transport/located_receipts.py`, `delta/transport.py`,
`evidence_network/transport.py`, `client/workspace_resilient.py`,
`client/workspace_validated.py`, and the supplier-selected facade/helper.

## Final inspected source identities

All paths below are relative to the canonical root. The new facade/helper were
compared with the frozen supplier-selected predecessors; old methods remain
unchanged. No test or product module was imported during this review.

| Source | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/transport/acquisition_resilience.py` | 12,484 | `43fa1acd66219c7d28a37a263dee04a20edd993bd24383c54680aa303202c09d` |
| `software/v5/client/supplier_resilient/workspace_evidence.py` | 35,948 | `a7c4979c35e904f096cba23b7fcb5cb8361e4679fc16d37d2fcec69041afd5ab` |
| `software/v5/client/supplier_resilient/semantic_reader.py` | 26,114 | `9b82de53bdcc8db74908622fc43c965a7b003111a752a8f579d25b5964dffe60` |
| `software/v5/client/supplier_resilient/test_resilience.py` | 28,624 | `c19a5b137133af39fe0ce0e3e5f24f4887a1f91d634e8fd4b1921904fb3ddbb8` |
| `research/cycles/v5-2026-10-20/Select-AcquisitionResilience.ps1` | 3,421 | `1aa99cf4fafce85f34ca046e002c33725594a40299004d6f5fa2cfbacf6abd6c` |

The selector preserves the predecessor selection's source closure and 19
runtime pins and adds exactly the four new sources above. It prepares a new
selection only; it does not import or execute product/test code. Its command is
the pinned Python runtime with `-I -S -B`, the new test file and an explicit
output directory. Its finite envelope is 20 CPU seconds, 60 wall seconds,
128 MiB, two processes and 1 MiB each for stdout/stderr. Existing selection or
output paths cause refusal. Review does not authorize expanding that envelope.

## Findings resolved before clearance

1. The initial exact `_ExpiringContact` condition excluded the ordinary direct
   contact's exact `_Contact` class. The final source permits precisely those
   two issued classes, preserves the direct binding identity and calls the
   original contact validation. Arbitrary subclasses remain excluded.
2. The initial final-settlement guard omitted the actual reply/header deltas.
   The final guard checks them against independent observations as well as the
   original request, charge, failure and upper-bound counters.
3. The normal refusal now carries the exact requested module, name, universe
   arity and body hash. The helper checks this request and supplier, schema,
   settlement and absence of mathematical/global-completeness claims.
4. The default candidate supplier now passes the same selected-supplier check
   as an explicit supplier. A cache hit still validates an explicitly selected
   supplier and the new timeout argument.
5. The final controls include the request identity and all nine required source
   pins. A replaced `_try_body` alias is rejected before the injected function
   can execute. This is a source-binding control, not evidence that arbitrary
   hostile Python code in the same process can be contained.

The transport never writes custody. Its successful payload is parsed and
validated against the selected descriptor before the facade uses the existing
`put_body` and exact readback. No recoverable catch encloses parsing, validation,
commit/readback or final activity checks. Refusal never calls helper `_group` or
`_retain` and does not change selected semantics, pending demands, held bodies
or revision. Ordinary helper/facade operation counts and network costs advance.

The failed-connect case relies on Python asyncio's failed-connect cleanup
contract. Once a writer is returned, `close()` and successful `wait_closed()`
are required. Timeout without an acquired writer, cancellation and uncertain
cleanup remain fatal. The operation deadline is not renewed; expiration during
attempt or cleanup can therefore make an otherwise clean refusal fatal. This
is intentional original-budget behavior, not a retry bug.

## Control scope and disposition

The fourteen explicitly selected methods exercise the new boundary, not the
inherited predecessor suites. One method uses actual loopback providers: P
holds the group but no body and closes the request with EOF; Q holds the exact
committed body. The facade, guarded contacts, structural/shared budgets,
descriptor validator and SQLite body custody are real. Mathematical owner
fixtures are explicitly inert, and the inherited direct-contact fixture
replaces `_active`, `_census` and `report`. Its preserved warrant is only a
sentinel. Consequently this run cannot establish preservation of a genuine live
mathematical warrant or all real owner-liveness checks.

Other transport methods use real parsing and settlement over explicit fake
streams; helper composition uses an explicit inert client. The suite covers
selected normal refusals, malformed/incorrect successful responses, forged
peer refusal JSON, fatal local custody and after-commit readback faults,
exhausted original allowance, unauthorized/expired/changed contacts, uncertain
closure and cancellation. Native/subprocess entry points are forbidden. Output
is `controls-result.json`, distinct from the launcher result on Windows.

These are proportionate controls for the changed transport/custody transition.
Re-running full READY, native verification or crypto campaigns is not required
to answer this increment's question. Earlier genuine evidence is reused only
for its original claims; it is not relabelled as execution of these new sources.

**At source clearance:** root could select and run exactly the reviewed finite
control suite; executed PASS was not yet claimed. **Not claimed by this suite:** genuine authority preservation,
automatic supplier discovery, universal availability, semantic READY, new
mathematical admission, ancestry-independent certification, net knowledge
growth, public deployment readiness or completed v5. Any source change after
the identities above requires a focused source re-review before adoption.

## Single-run outcome audit

Read-only audit of saved `experiments/v5-local-checks/acquisition-resilience-controls-01/`:
**14 tests, zero failures/errors/skips; terminal exit zero and clean closure**.
No repeats, imports or native/proof executions were performed by this reviewer.
Original and saved selection both hash to
`5eff81de1ed686cf3db2d6d901073f7f7070c3497762d22aef998736c4ddc4e4`.
All 96 selected source hashes match both original and snapshot files; all 19
runtime pins match. Reported executed source identities match this review.

The real loopback outcome is P `PEER_EOF`, followed by Q's exact 267-byte body
using the same operation. Shared charge is `327947 = 262144 + 65536 + 267`
bytes (prepaid discovery + full failed-attempt cap + successful body), with
six total charged requests and no pending reservation. Structural acquisition
records two requests, one failure, 65,803 charged bytes and zero inflight or
reserved work. Each provider records one request and zero active/reserved work
at closure. Preserved authority remains **only an inert sentinel**; the mocked
owner-liveness scope above is unchanged. Native/proof calls are both zero.

The outer result records a reaped child, zero active job processes, closed job,
no cleanup errors, and no termination request. Known worker CPU is 1.734375 s;
wrapper CPU is 0.359375 s; their total is **2.09375 s**. Recorded whole-run wall
time is **3.8775427998043597 s**. The original selected caps were not enlarged.

Evidence SHA-256: outer `RESULT.json`
`45dbaadce266f0ce917f7673927a98ea0708dabe320df7df6423b32c1c3098ab`;
`controls-result.json`
`5c1d727376b95bd0efcbcef257875359ad91125082924be509d9090de64bbca2`.
**Disposition:** the bounded transport/custody resilience increment is supported
for root's adoption. It establishes neither new mathematical acceptance nor a
genuine full-authority continuation, semantic READY, growth or completed v5.
