# Explicit terminal-candidate trials

Source-only successor selected by `research/cycles/v5-2026-10-20/CANDIDATE-ADMISSION-IMPLEMENTATION.md`. Not an installation, release or runtime qualification. Predecessor source and state remain unchanged.

## What this changes

A mathematically useful candidate can have several receipt variants. The ordinary strict acquisition API fails the entire live client if verification fails. The new optional APIs permit a narrowly checked **clean verifier nonacceptance** without discarding earlier live mathematical work. The local agent explicitly decides whether to try a different variant; the software does not retry, renew an allowance or choose a research agenda.

The trust boundary is unchanged: a successful candidate still needs the original real I or A verifier, exact receipt/summary/journal binding, live original owners and the applicable member/opening checks. A saved outcome is never a proof or a reusable acceptance capability.

## Public client APIs

Each method retains the existing serialized entry/fatal-cleanup contract and original finite grant. Its trial-only wrapper checks live authority again after the final output census, then checks original grant/owner deadlines and controller CPU after all blocking work. Strict predecessor methods keep their existing wrappers.

```python
client.try_admit_terminal_local(
    module, packet_sha256, packet_bytes,
    expected_exact_journal=None,
    receipt_cpu_seconds=30, wall_seconds=600, memory_mib=1024,
)

await client.try_acquire_terminal(
    candidate, entry,
    expected_exact_journal=None,
    receipt_cpu_seconds=30, wall_seconds=600, memory_mib=1024,
)

await client.try_acquire_terminal_exact(
    candidate, entry,
    expected_exact_journal=None,
    receipt_cpu_seconds=30, wall_seconds=600, memory_mib=1024,
)
```

`entry` is the existing exact dictionary with `packet_sha256` and `packet_bytes`. The offered method requires that entry to have been offered by the original selected supplier. The exact method can request an already known digest and size without offer membership; it does not discover unknown identities. The local method uses exact bytes already held in the client's packet custody. No method acquires definition bodies, stages a packet, selects a staged variant, imports a module or changes an existing context.

The returned dictionary has `status`, `evidence_kind`, `module`, `packet_sha256`, `packet_bytes` and `authority`. Only `ADMITTED` also has `warrant`:

| Status | Meaning |
|---|---|
| `ADMITTED` | The usual live same-client warrant exists and has passed the ordinary positive bindings. Use it through existing import APIs. It is not transferable proof. |
| `NOT_ADMITTED` | The real verifier declined this attempt and the complete clean-nonacceptance gate succeeded. No new warrant or positive cache entry exists. No conclusion about mathematical truth or the cause of failure follows. |
| `UNSUPPORTED_TRIAL_FORM` | The packet is structurally valid mixed/native evidence, outside this terminal-only trial. No verifier is called. The caller may choose another path explicitly; there is no automatic strict fallback. |

Example outcome handling after the caller has obtained an ordinary live candidate and exact entry:

```python
result = await client.try_acquire_terminal_exact(candidate, entry)
if result["status"] == "ADMITTED":
    warrant = result["warrant"]
    # Supply warrant to the existing import workflow when appropriate.
elif result["status"] == "NOT_ADMITTED":
    # The caller may explicitly choose another variant within remaining limits.
    # This is not a claim that the theorem or receipt is false.
    pass
else:
    assert result["status"] == "UNSUPPORTED_TRIAL_FORM"
```

Existing strict methods keep returning ordinary warrants or raising failures. The new methods do not revive a client, reader or owner that has already failed. They do not erase an earlier staged variant. Existing contexts and staged selections can remain present because the trial never mutates them; the existing workflow determines whether/how a later positive warrant is used.

Positive terminal results enter the existing live receipt/aggregate/packet caches. Later ordinary admission still rechecks exact live bindings and may reuse that authority. This does not promise zero transfer cost: the current staged reader may fetch bytes again. Nonacceptance has no negative cache and does not affect other candidates' mathematical validity.

## What can return normally after a failed verification

The lower original owner permits `None` from its explicit `try_receive` only for this invocation's natural integer exit1, actual empty stdout, no supervisor error, complete unforced Job closure, independently checked final resource/log/output bounds, exact unchanged inputs, fresh original pins/trust and a still-live original deadline. The client converts that one result to `NOT_ADMITTED`. Old `receive` never gains a `None` result.

Every exception still follows the ordinary fatal path. In particular, malformed packets, wrong exact journals, invalid A membership, changed custody, bad positive output, trust withdrawal, changed pins, cancellation, missed deadlines, observed resource overruns and uncertain cleanup are not recoverable misses. A final client output/liveness check may fail even after the lower verifier has returned. Expiry or withdrawal during the final census must fail, not expose an already prepared `NOT_ADMITTED` result.

All transfer, custody, input, verification and output charges already incurred remain charged. There is no automatic second attempt, new owner, refreshed provider contact, new grant, deadline extension or refund. Windows Job supervision is resource control, not hostile-code sandboxing.

## Source composition

Four replacements and one new helper compose with the selected actual129 SDK map and the separately frozen offer-enumeration custody successor:

- `admission/clean_refusal.py`: new shared lower nonacceptance gate.
- `admission/verifier.py`: I issuer's explicit `try_receive`.
- `aggregate_claims/aggregate_admission.py`: A issuer's explicit `try_receive`.
- `client/workspace_evidence.py`: shared ordinary/trial terminal helpers and three public trial methods.
- `client/managed_owner.py`: selected facade source pin only.

No cryptographic host/image, supervisor, wire/schema, staged-reader, mixed verifier or import implementation changes are included. Root owns exact source-map selection, controlled execution and adoption. See `research/cycles/v5-2026-10-20/CANDIDATE-ADMISSION-FACADE.md` for the facade source checkpoint and the separate independent review before use.
