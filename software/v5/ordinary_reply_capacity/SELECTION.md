# Fit exact-object reads within a provider's remaining service capacity

Root source selection, 2026-10-28. The dedicated-host failure exposed a reusable
protocol usability problem: clients state a maximum response size, but cannot
know an independent provider's remaining aggregate allowance. A small existing
object can be refused merely because its client's maximum is large. Smaller
fixture limits work locally; they are not a general solution for unfamiliar
objects or concurrent users. The limits are upper bounds, not required spends.

Select a fresh successor of ordinary_multi_source/http_provider.py. For ordinary
locator and evidence routes only, validate the original request as before, then
cap the private parsed request's max_bytes by the positive currently unreserved
service remainder. Reserve that effective cap before lookup/dispatch. Existing
length-first lookup, response-size validation, charging before writes and finally
release remain. Refuse when no positive remainder exists, or when the actual
object does not fit. Never truncate or partially accept evidence.

There is no new wire schema, automatic retry, client reservation refund, capacity
renewal or mathematical acceptance rule. All other routes retain their behavior.
No provider completeness or service guarantee follows. Missing/oversized objects
remain ordinary bounded failures. A request cap does not authenticate data.

The current accounting temporarily double-counts bytes already charged for an
in-flight write while retaining that request's reservation until cleanup. Thus
charged+reserved is a conservative admission quantity, not an invariant bounded
by the service cap at every intermediate instant. The proof must establish that
cumulative charged output stays bounded and no uncharged concurrent dispatch can
overcommit. Do not silently change release/charging semantics to simplify a proof.

query_scaling owns fresh http_provider.py and CONTRACT.md with the exact source
argument. Root owns controls/integration and any finite runtime selection; an
independent review follows source completion. No runtime or package mutation is
selected here. Retain all current source and failures unchanged.

Small controls should use actual transport dispatch under a finite local envelope
or controlled reader/writer doubles: small objects under oversized caps, exact
exhaustion, unavailable/oversized objects, competing live reservations, interrupted
writes, and unchanged nonselected routes. No new theorem, grounding or proof run
is justified. Stop after the demonstrated false refusal is removed without budget
or acceptance weakening.
