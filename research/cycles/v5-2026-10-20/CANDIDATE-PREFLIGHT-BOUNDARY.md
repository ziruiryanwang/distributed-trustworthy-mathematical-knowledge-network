# Next candidate boundary: pure preflight before custody

2026-10-22, storage_outcome_audit. Source-only investigation. No used source,
installation, test, proof or Git state changed; no runtime was selected or run.
The current genuine refusal/continuation integration has higher priority.

## Decision

**The current API does not preserve an existing valid context when an acquired
packet is malformed before verifier invocation. A small, worthwhile pure
preflight seam exists, but wrapping the current acquisition call in a broad
catch is unsafe.** Recommend a later explicitly selected opt-in packet attempt:
settled bounded transfer, pure candidate triage, then existing custody/admission.
Do not enlarge the tested lower verifier clean-refusal rule.

This closes a concrete availability weakness: a selected peer can advertise a
digest of malformed content; its bytes can match the advertised digest exactly,
yet parsing them currently revokes unrelated valid work. Avoiding that loss has
payoff independent of whether the candidate's receipt is eventually valid.

## Exact current path

Sources are the qualified candidate-admission successor plus base map129
`328c21bb...` and frozen offer-enumeration custody `e1e35cec...`, not an arbitrary
historical installation.

1. `candidate_admission/client/workspace_evidence.py` (`e81407b9...`), lines812,
   821 and829: public terminal trials call `_acquire_packet`. Candidate identity,
   caller limits, optional exact journal and offer membership are checked first.
   The trial requests no bodies. No separate malformed-candidate result exists.
2. `exact_packet/evidence_network/transport.py` (`b3403208...`), line88:
   `_packet` validates original custody/profile/caps, fetches bounded raw bytes,
   checks exact digest/length, calls `packets.put`, then reads back.
3. `offer_enumeration/delta/custody.py` (`e1e35cec...`), line145: `put` calls
   `self.inspect(module, raw)` **before** `BEGIN IMMEDIATE`. The selected override
   is `managed_storage/evidence_network/custody.py` (`4264841e...`), line119:
   profile and byte-cap checks, `inspect_evidence`, then target ModuleID binding.
4. `terminal_i/evidence_network/packet.py` (`cf8aaa61...`) parses canonical JSON,
   terminal layout, journal/header/profile/member binding and rank/receipt caps.
   It grants no authority. `modules/codec.py` (`e01b7478...`), lines24 and73,
   provides `StructureError` and bounded-byte JSON/canonical parsing.
5. Those failures currently escape the trial decorators at facade lines71/85.
   They call `_fail`, not a candidate-result conversion. The inherited failure
   chain clears warrants/caches/context and closes original owners. The atomic
   predecessor's concrete failure body is
   `continuing_context/client/workspace_atomic.py` line436.

Thus a malformed same-digest packet is not inserted into custody, but its
exception still destroys the live client context. The currently implemented
NOT_ADMITTED path applies only after a structurally usable terminal reaches the
original verifier and satisfies its complete same-call clean-refusal contract.
UNSUPPORTED_TRIAL_FORM handles a structurally valid mixed packet, not arbitrary
bad bytes. Local `try_admit_terminal_local` starts from a custody read; treating
corruption of previously stored bytes as a harmless peer miss would be wrong.

## Necessary transport distinction

`delta/transport.py` (`18c1abda...`) line301 `_get` settles its exact budget ticket
in `finally`; a successful return has already incurred network accounting.
However its `exchange` (line34) closes the writer and **suppresses exceptions from
`wait_closed`** in its final block. Consequently a normal `_get` return is not
evidence that local transport cleanup completed successfully.

Do not classify a parser failure after that return as a safely settled attempt
without resolving this uncertainty. A later opt-in transfer should propagate
uncertain closure and cancellation and return bytes only after its explicit
closure contract. Existing body-attempt resilience is a useful local pattern
(`body_location/transport/acquisition_resilience.py`, `0dc12c02...`): it distinguishes
settled outcomes from cleanup failure and guards original owner/budget identity.
It is not a ready-made packet API; its route, demand and body semantics differ.

This is a future-boundary obligation, not a finding that changes the adopted
synthetic controls or authorizes editing frozen transport code.

## Minimal proposed separation

| Condition | Proposed opt-in disposition |
|---|---|
| Completed bounded peer bytes fail digest binding, canonical grammar, terminal member binding, or selected target summary | Candidate rejection; no write, verifier call or warrant |
| Well-formed but unsupported evidence form/profile under the unchanged selected policy | Explicit unsupported/incompatible candidate result, never mathematical invalidity |
| Original authority, profile, source pin, contact, trust or deadline changed | Fatal; no recoverable result |
| Budget exhausted, actual memory failure, cancellation, uncertain transport closure, storage/write/readback failure | Fatal; preserve charges and uncertainty |
| Foreign candidate token, malformed caller arguments, unoffered entry on offered API | Caller-contract failure; do not reinterpret as peer fault |
| Caller explicitly supplies the wrong expected exact journal | Keep current strict mismatch behavior; do not quietly weaken the requested target |

For the first row, an exact-length mismatch already rejected inside HTTP framing
need not become recoverable in the first implementation. Malformed HTTP,
timeouts, absent peers and malformed discovery offers can remain fatal/deferred;
the payoff does not require solving every transport failure in one change.
Distinguish a declared grammar/size limit that a candidate fails from exhaustion
of the running operation's resources. Neither means false mathematics.

The pure function should accept copied immutable bytes plus previously validated
immutable expectations/profile. It returns structural facts or an explicit
candidate-rejection value, never a handle. Reuse the real packet parser rather
than duplicating mathematical/journal interpretation. A narrowly scoped
`StructureError` conversion may be appropriate **only around peer-byte parsing**:
validate trusted envelope/adopted image first, outside that boundary, because
the parser also raises that class for invalid owner-supplied configuration.
Use direct comparisons for peer digest/target mismatch, not error-text matching.
Never catch the enclosing store, acquisition, `_active`, `MemoryError`, or a
general `ValueError`/`Exception` as candidate rejection.

## Conditions before selecting implementation

1. Preserve one original request/byte grant. Settle every attempt, including
   rejected bytes; no retries, refunds, fresh owners or negative-cache authority.
   Charge parsing/input work before it occurs, and check original final liveness
   after parsing and after any blocking census. No verifier reservation is made
   for a candidate rejected before invocation.
2. Keep recoverable triage before custody transaction/write and before any
   import/staging mutation. On the valid branch retain ordinary `put`, readback,
   custody checks and actual verifier issuance; do not let preflight bypass them.
   If the second ordinary validation disagrees, fail fatally rather than recover.
3. Snapshot caller entry/expectations before awaits. Validate origin/profile both
   before and after a settled transfer, and ensure no pending request remains
   before returning rejection. An old valid context is preserved by nonmutation,
   not by restoring it after failure.
4. Bound parsing by the existing raw-byte envelope and original resource limits.
   The JSON decoder is not a hostile-code sandbox and does not promise zero
   allocation risk; actual resource failure remains fatal. A preflight result
   is not mathematical/cryptographic acceptance or a portable proof.

Existing public calls do not implement this separation: acquisition commits
before it returns, while local admission reads already-custodied data. A pure
inspection helper alone could help an external caller that already holds bytes,
but would not protect the integrated peer path. The recommended follow-on is
therefore one narrow opt-in transfer/triage integration, not a new index, global
candidate policy, owner resurrection mechanism or broad exception-recovery layer.
No implementation or additional campaign is selected by this note.
