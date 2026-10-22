# Packet preflight: independent source challenge

2026-10-22, `storage_integration_adapter`. Source-only, root-assigned challenge
of CANDIDATE-PREFLIGHT-BOUNDARY, SHA-256
`6307aa6f3be29a45008e878b4f58a73e0a9ed5353869deeba83713185c285590`.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
No product, predecessor, runtime, test, installation or Git state changed.
The selected actual verifier/context integration remains higher priority.

## Decision

**Proceed later with one narrow opt-in packet-preflight successor, not a broad
exception-recovery layer.** The proposed boundary is sound in principle with
two taxonomy corrections and an explicit transport-closure gate. It requires
no new logical Python module and no increase to the 128-runtime-pin cap.

Current selected paths confirm the obstacle: exact-packet transport
`software/v5/exact_packet/evidence_network/transport.py:88` (`b3403208...`)
downloads, checks digest, then calls `packets.put`. The selected
`managed_storage/evidence_network/custody.py:119` (`4264841e...`) inspects peer
bytes; inherited `offer_enumeration/delta/custody.py:145` (`e1e35cec...`) does
that inspection before its transaction. A parser refusal therefore avoids a
bad custody write, but escapes the current terminal-trial wrapper and revokes
unrelated valid work. Catching `packets.put`, `_acquire_packet` or their enclosing
public method would also swallow owner/storage failures and is unacceptable.

## Two corrections to the proposed taxonomy

1. **StructureError is not the whole parser contract.** Selected
   `terminal_i/evidence_network/packet.py:85` (`cf8aaa61...`) delegates mixed
   packets to `mixed_claims.packet.parse_packet`. That path also raises the
   exact `delta.packet.DeltaError` class (`delta/packet.py:14`), whose labels
   include declared packet/depth/count bounds. These labels are not evidence
   that the operation exhausted CPU/RAM, and none establishes false mathematics.
   A future pure-parser catch may cover exactly these two reviewed classes,
   never all `ValueError` or `Exception`. Unexpected exception types stay fatal.
2. **The decoder already wraps a resource exception.**
   `modules/codec.py:63,73` (`e01b7478...`) converts `RecursionError` into
   `StructureError` using exception chaining. A naive StructureError catch would
   classify interpreter stack exhaustion as a harmless grammar refusal.
   Conservatively propagate direct or chained `RecursionError`/`MemoryError`
   rather than return candidate rejection. Inspect typed exception causes,
   not diagnostic strings; cycles/unknown chain shape must fail closed.
   Intentional finite grammar-limit failures can remain policy-relative
   rejection. No decoder/compiler patch is needed for this first seam.

Do not promise to distinguish malformed from incompatible unknown mathematics.
An unknown schema, disabled I capability or nonadopted embedded profile may be
reported as `CANDIDATE_REJECTED_UNDER_SELECTED_POLICY`, with no mathematical
judgment. Only an actually parsed supported mixed form may retain the existing
`UNSUPPORTED_TRIAL_FORM` result. Do not infer well-formedness from a schema tag.
Keep `NOT_ADMITTED` exclusively for the existing real-verifier clean refusal.

## Minimal implementable separation

Use fresh successors of **three existing logical files**:

| Logical source | Exact predecessor | Permitted change |
|---|---|---|
| `evidence_network/transport.py` |`exact_packet/...`, `b34032085bca3ddbd248afe57e655777a140d2c34b6f33ea61b80721a07b926c`|Add one settled packet-byte transfer and one pure triage helper; ordinary `packet`, `packet_exact`, provider and offer behavior unchanged.|
| `client/workspace_evidence.py` |`candidate_admission/...`, `e81407b9296d14a3f3f2f1a1c8554efa2747829fa6a2639fc29215c7ed29cb44`|Route only the two network terminal-trial APIs through that seam; retain original final trial guards and all strict/local methods.|
| `client/managed_owner.py` |`candidate_admission/...`, `3fb4e619ddff115220eee4b6d594a41b2d051e6f8b6c731d63cca15b2c8555a3`|Update only the facade source pin after review.|

Suggested fresh source root: `software/v5/candidate_preflight/`. This is a
proposal, not permission to create it. New controls/adapters belong outside
SDK source roots. Source-map composition remains 130 SDK/109 v5-Python rows;
do not add a 110th module. No custody/parser/verifier change is necessary.

The sequence should be:

1. Validate original candidate, caller entry, exact expected-J syntax, caps,
   source identities and selected owner/profile **outside any recoverable
   catch**. Copy the scalar packet entry and immutable expectation bytes before
   awaits. Retain offered-API membership; exact-API remains known digest/size.
2. Capture the original acquisition/budget/contact/deadlines. Existing
   `body_location/transport/acquisition_resilience.py:125,158` (`0dc12c02...`)
   supplies reusable `_binding`/`_unchanged` checks without its body semantics.
   Use runtime-local imports if necessary to avoid its EvidenceAcquisition
   import cycle; keep exact function/source identity guards. No callback,
   replacement budget or new endpoint is supplied by the peer.
3. Fetch bounded bytes through a new packet-specific strict-closure exchange.
   Preserve existing HTTP/TLS/framing/EOF rules and one original budget ticket.
   It returns bytes only after `writer.close()` and bounded `wait_closed()`
   succeed within the original operation deadline. Cancellation, timeout,
   malformed HTTP, non-200 response and uncertain closure all remain fatal.
   The ticket settles exactly once in `finally`; unknown outcomes charge its
   full reservation. A closure failure must never become a normal peer result.
4. Recheck original binding and quiescence. Charge the returned raw input before
   hashing/parsing. The facade moves its existing raw-input charge earlier;
   do not accidentally double-charge the valid path or skip rejected input.
   Passing bytes to the pure helper must not commit/stage/import anything.
5. Pure triage validates trusted envelope, terminal cap, adopted image and
   expected summary outside its parser catch. With fixed immutable bytes and
   expectations, compare length/digest directly, then invoke the real
   `inspect_evidence` parser inside the narrowly typed catch above. Compare
   parsed target summary/module directly to the selected target. Rejection
   returns only local structural data; no warrant, verifier reservation, cache
   insertion or custody write. A parsed exact J different from the caller's
   explicit expected J remains a strict fatal mismatch outside this catch.
6. On valid preflight, perform ordinary `put`, exact readback, custody readiness
   and existing admission. All are **outside** recoverable triage. Revalidation
   disagreement, store quota/commit uncertainty/corruption and final liveness
   failure are fatal. Valid mixed evidence may follow the existing structural
   custody then unsupported-trial result; no new mixed-verifier path is added.
7. Before any normal result, check the original owner/contact/budget again,
   require no pending request or structural inflight/reservation, then retain
   `_terminal_final`: active, census, active, nonblocking original deadlines
   and controller-CPU checks. No I/O follows those final checks.

The same-live packet-cache path remains strict: bytes already in local custody
are not newly received peer input. Its corruption or local read failure must
not become candidate rejection. Local `try_admit_terminal_local` remains
unchanged for the same reason. Existing warrants/context/stages survive by
nonmutation, not restoration after failure.

## Existing wait_closed suppression: exact impact

Selected `delta/transport.py:34,76,301` (`18c1abda...`) requests writer closure,
suppresses ordinary exceptions from its one-second `wait_closed`, then lets
`_get` settle its network ticket. Consequently settlement of accounting is not
proof of successful socket closure. The provider has analogous suppression at
line164; `server is None` and an empty task set do not reconstruct missing
per-socket closure evidence.

This does **not** invalidate the current narrow actual integration's genuine
I-verifier report, exact input binding or retained-context/stage checks: its
one-byte receipt is inside a well-formed packet and reaches the separately
contained verifier, whose clean-refusal gate checks the actual process tree,
logs and limits. It does limit the conclusion: current successful loopback
operation is not evidence of recoverable malformed transport or guaranteed
all-socket cleanup. Do not re-run it to manufacture that broader claim or edit
its used transport. The proposed new byte-transfer method must independently
establish strict client closure before declaring a peer-byte rejection; it
does not thereby repair inherited provider or search-route cleanup generally.

## Small failure matrix before one selected integration

Focused controls should distinguish causes, not require new proofs:

- Hash-correct malformed canonical JSON; duplicate fields; terminal journal
  or membership inconsistency; target-summary mismatch; same-length wrong
  digest: rejection, paid transfer/input, zero verifier/custody mutation, old
  warrant/context/stage retained. Fixed advertised byte count remains framing.
- Valid terminal I/A preflight and valid mixed unsupported behavior still use
  ordinary custody/admission; one-byte receipt reaches the unchanged verifier
  refusal, not preflight rejection. Exact-J mismatch remains fatal.
- Envelope/profile/caller/token/offer/source/contact substitution before or
  after await; actual MemoryError; direct/chained RecursionError; cancellation;
  settlement error; closure error/timeout; deadline or CPU expiry during parse
  or final census: fatal, no recoverable result or resource renewal.
- `put`/readback failure, quota exhaustion and disagreement after successful
  triage: fatal. Valid old cache corrupted in custody: fatal. No catch surrounds
  the store. Successful peer rejection followed by public old-context/stage use
  must not issue a new grant or verifier merely to reconstruct lost state.

A single bounded real malformed-packet transfer plus continued existing work
would test the new integration after source controls. Existing genuine-I
refusal evidence should be reused; no new proof production, large rebuild,
full network test or broad availability mechanism is justified by this seam.
Root must separately select scope, exact sources and finite execution.
