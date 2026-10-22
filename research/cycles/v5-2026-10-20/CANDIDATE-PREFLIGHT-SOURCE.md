# Settled packet preflight: source checkpoint

2026-10-22, `storage_integration_adapter`. Root-selected source implementation
under CANDIDATE-PREFLIGHT-SELECTION.md; canonical root
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
No execution, Python import, compilation, test, build, installation, proof,
state migration, Git mutation or runtime qualification by this assignment.

## Exact fresh files

| File under `software/v5/candidate_preflight/` | Bytes | SHA-256 |
|---|---:|---|
| `evidence_network/transport.py` |18485|`1dbc083447569a70c62910fec904e49d7df154c09684b26f28b30e071efa14c7`|
| `client/workspace_evidence.py` |65596|`62c4ea578cf92c85b398880e8cfba9e914ecf6668e3916bd1d87ce5ee02efcce`|
| `client/managed_owner.py` |33789|`860fbea914c0de2515d14d3ceacad7fcae8f7c14d79cbfea1632ead172f9cd83`|
| `README.md` |6859|`feb5534183bd6f9d22e8d4149b60f76b15c12478acb9ef8c3209af739cc07954`|

All three initial copies were hash-verified against the selected exact
predecessors: transport `b3403208...`, facade `e81407b9...`, managed owner
`3fb4e619...`. Used predecessors remain unchanged. Read-only full diffs show
transport185 added/zero removed lines; facade39 added/four removed; managed
owner exactly one changed facade-pin line. No new logical SDK module is added.

## Implemented boundary

The two network terminal-trial methods alone use the new branch when their
same-live packet cache has no hit. Strict network APIs and all local admission
remain unchanged. A cached packet is still local custody: corruption does not
become a recoverable peer refusal.

`EvidenceAcquisition._trial_packet_bytes(provider, module, entry, *, offered)`
copies the selected entry and captures the original acquisition/structural
owner/budget/contact through the already-selected body-binding helpers. It also
captures profile, envelope identity/state, packet limits and HTTP-counter owner.
Its offered variant requires original offer membership. It reserves one budget
ticket, invokes `_exchange_packet_settled`, accounts ordinary HTTP counters and
settles exactly once in `finally`, conservatively charging the full reply cap
on unknown outcomes. It returns `(raw, bound)` only after original binding and
quiescence checks, without parsing or mutating custody.

The packet-specific exchange preserves existing request/response framing,
exact Content-Length, TLS and EOF rules. Its original deadline covers both the
transfer and bounded writer closure. `wait_closed` exceptions are not suppressed;
cancellation propagates, and uncertain ordinary closure raises PacketCleanupError.
Malformed HTTP, absent peers, timeouts and non-200 responses remain fatal. This
does not change inherited provider/search/ordinary delta cleanup behavior.

The facade rechecks selected source origins and charges raw bytes before
preflight. `preflight_packet(raw, entry, summary, *, envelope, aggregate_image,
terminal_receipt_bytes, terminal_i)` validates trusted arguments and selected
configuration outside the recoverable parser catch. It checks digest/size,
invokes the exact selected `inspect_evidence`, and compares the parsed target
with the selected summary/module. Its new public result is:

```text
CANDIDATE_REJECTED_UNDER_SELECTED_POLICY
```

The result records local reason, requested selection, received digest/size,
module and explicit no-mathematical-acceptance/authority labels. It contains
no warrant and does not claim false mathematics or a well-formed unknown schema.
Only exact StructureError/DeltaError raised by pure parsing may reach it.

Exception chains are inspected as typed objects, without error-string matching.
At most16 exact reviewed nodes are allowed: StructureError/DeltaError and the
decoder's JSONDecodeError, UnicodeDecodeError, UnicodeEncodeError or ValueError.
MemoryError/RecursionError, unexpected subclasses/types, divergent cause/context
branches, cycles or excessive chain length rethrow. This specifically prevents
the existing codec's wrapped RecursionError from hiding a runtime resource limit.

The valid preflight result is internal structural data only. A parsed journal
different from explicit caller-expected J still fails strictly before custody.
Ordinary `put`, exact readback, custody readiness and admission follow outside
the recoverable catch; even another parser error there is fatal. No duplicate
raw-input charge is introduced by moving the original charge earlier. Existing
receipt/member input and verifier reservations remain unchanged.

Existing terminal `NOT_ADMITTED`, supported mixed `UNSUPPORTED_TRIAL_FORM` and
positive `ADMITTED` preserve their earlier meanings. No verifier is called or
reserved for preflight rejection. The original clean verifier refusal rules
are not weakened or reused to classify malformed transport.

## Noninterference and finalization

No new path writes `_warrants`, positive caches, `_session`, `_context`, staged
tokens or selection views before rejection. Existing objects survive by
nonmutation; no owner resurrection or rollback exists. Transfer/input costs
remain charged. No retries, refunds, new grants, new contacts or deadlines.

Original binding/quiescence is checked after transfer, parsing and ordinary
admission. Existing `_terminal_final` is unchanged: active, census, active,
then nonblocking original owner/grant deadline and controller-CPU checks.
Only the asynchronous terminal wrapper adds a final nonblocking assertion of
zero budget pending ticket, structural inflight requests and reserved bytes;
this also covers its strict cache path. The synchronous/local wrapper is unchanged.
Every escaped error retains ordinary fatal client cleanup.
Contact validity is required through the completed attempt/triage/admission
checks, not during the later purely local final census. The README makes this
explicit; original client/issuer grant deadlines, CPU and quiescence still hold
at return. No all-transports contact-at-return guarantee is introduced.

## Review and next boundary

Stable interfaces/source hashes and the complete error/cost contract were sent
to `storage_launch_review` for focused controls and independent source review,
and to `storage_outcome_audit` for its separate fixture/selector review. The
README documents the same contract. Reviews may require fresh unused-source
corrections; no source acceptance or runtime outcome is inferred here.

Root owns the final130-logical-source map, selection, launch, adoption and Git.
The selected changes add no v5 module, retaining109 v5 Python rows and the
current128 I/A runtime-pin ceiling. After focused controls, the high-payoff
next boundary is one combined installed integration reusing the retained I
receipt, not another proof production or general transport-recovery campaign.
