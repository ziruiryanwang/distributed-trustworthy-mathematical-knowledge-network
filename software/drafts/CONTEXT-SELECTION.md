# Historical context selection: smallest operable contract

Prospective design, 2026-09-21. Not implemented, tested, or an addition to the
frozen recovery/peer experiments. Decision: select an existing client-owned
context by metadata-only compare-and-set; ordinary later checking stays intact.

## Problem and boundary

Admission currently unions new packages into the client's current head. A
bounded proof environment eventually fills even if its older mathematics is
irrelevant to the next investigation. The corpus and a working context must
therefore be distinct: retained knowledge need not all be imported together.

Selection changes a workspace pointer, not mathematical truth, possession of
live dependencies, candidate publication, or acceptance authority. No global
agenda, human-intention field, scheduler, cross-node consensus or new identity
system is needed. The local client label retains its existing owner-trust model.

## State and exact operation

Write state as `S = (R, H, Q, U, A, P, T)`: immutable records, client heads,
request ledger, cumulative consumption, active request, publication state and
native stages. `R[h]` includes a context's exact configuration/client ownership.
Historical record authentication means the existing `record(h,"context",c)`
checks succeed, including indexed bytes, hash, kind and owner/config binding.
It does not mean that files named inside those bytes still exist or are valid.

Add one ordinary request shape, preserving the existing envelope and limits:

```json
{"client":"local","request_id":"new-id","op":"select_context",
 "args":{"context":"EXPECTED_CURRENT_HANDLE","selected":"OWN_HISTORICAL_HANDLE"}}
```

`context` is the expected current mathematical context, not an epoch number.
`selected` must be an already-existing context owned by this client under this
exact initialized configuration. A candidate/artifact handle or another
client's context is not selectable. No new context record is manufactured.
The agent retains handles from earlier successful `init`/`admit` replies;
historical-context enumeration is not a prerequisite or part of this change.

For a fresh well-formed request with sufficient ordinary allowance:

1. Preserve the existing exact-byte prior-request lookup before reservation.
2. Reserve the normal request count/byte allowance and active slot.
3. Authenticate both context records and require `H[c] = context`.
4. In the ordinary short visibility transaction, recheck that equality, set
   `H[c] := selected`, and write the exact terminal response/clear the active
   slot together. Do not import the checker or allocate a native stage.

Success returns exactly the following semantic fields (normal JSON encoding):

```text
status: OK; client: c; previous_context: context; context: selected;
changed: (context != selected); mathematicalAcceptance: false;
context_record_authenticated: true; live_context_status: UNCHECKED;
native_stages: 0
```

Do not include `accepted:true` or a purported fresh description. A caller may
use ordinary `info` for the explicitly historical description and ordinary
inspection for its existing supported live checks. Selecting the current head
is a successful no-op pointer change, still charged as a new ordinary request.

## Postconditions, errors and replay

On a completed successful fresh selection, `H'[c] = selected`; other heads are
unchanged. Every preexisting record in `R`, and all of `P` and `T`, are unchanged.
A supervised reservation adds its normal immutable owner `attempt` record to
`R`, binding this request to its original call directory; this bookkeeping is
not mathematical authority. No new context/candidate/artifact record is added.
`Q` gains only this request's ordinary pending-to-terminal history; `U` has
exactly its ordinary reservation increase, not a refund; `A` is cleared by the
existing terminal transaction. No candidate entry, publication or stage is made.

Malformed envelopes, unknown kinds/owners, stale heads and exhausted grants
follow existing parser/record/reservation errors. `STALE_CONTEXT` leaves the
head unchanged. A failure after reservation consumes that reservation; failure
before reservation does not invent a charge. Existing transaction rollback and
uncertain-outcome rules still apply; a refusal is not a mathematical judgment.

An exact terminal retry returns the original bytes without reselecting the
head, reserving again or reconsidering current state. Therefore a successful
old selection response is historical: it does not assert the current head is
still that handle. Use `info` to observe the current pointer. Different bytes
under the same request ID conflict. A pending retry remains explicitly blocked.

All old checked artifacts keep their original context references. Old replies,
charges, candidate handles, catalog cuts and published packages remain intact.
Later publication of an old private artifact uses the unchanged artifact
reauthentication path; it does not require the old context to be current.

## Live trust and race semantics

Metadata-only selection may succeed even when a selected dependency/evidence
file has become unavailable or corrupt. That is intentional: `UNCHECKED` is
not an availability promise or an authorization to execute against those bytes.
Subsequent `admit`/`submit` must still use their unchanged `Checker.context`
evidence authentication, selected package validation and union-plan binding,
followed by their ordinary fresh native stages. Missing/changed files refuse.
`Checker.context` alone does not rederive the stored historical description;
do not strengthen its guarantee by implication. Inspection has additional checks.

The current OS writer lock serializes prepare and commit, and the commit-time
head comparison must remain even if that implementation later becomes concurrent.
An admission prepared for A cannot commit while the head is B. A submission for
B does not become valid merely because selection chose a different context.
If A is selected, then B, then A again, an unexecuted request naming A can run:
handles deliberately express exact immutable mathematical context, not head
generation or a promise that no intervening work occurred. This ABA behavior
does not bypass fresh byte validation or alter exact terminal replay. Clients
needing epoch-sensitive workflow cancellation require a separate future feature.

Selection is not peer recovery: the current narrow recovery worker only covers
its explicitly permitted peer operations. A crash after selection reservation
may still leave a blocked pending operation. Do not add this operation to that
worker's allowlist without a separately reviewed interruption contract. No
general crash-completion or new availability guarantee follows from this note.

## Lower-cost native-backed discriminator

Propose one normal owner option, `configure --context-packages N`, default 16,
for a fresh node only. It writes `limits.packages` before configuration hashing;
no initialized config is edited. Current `configure` hardcodes 16 and does not
expose this option; implementation/API review is required first. `Checker`
already accepts integer caps 1..16, but `load_config` does not check this field
explicitly. Require configuration-time exact-integer validation between the
number of common packages and 16, both in `configure` and `load_config`, while
preserving the existing omitted-field default 16. The current common set has
five packages; choose six. This does not change native time/byte/lifetime grants.

One fresh consumer reuses actual G02/H01 inert bundles through ordinary candidate
acquisition; no new producer or producer proof is needed. Measure its actual
bootstrap list `C0` as length 5. Admit G to obtain length 6; admission of distinct
H must then refuse `CONTEXT_PACKAGE_COUNT` at length 7 before native allocation.
Select `C0`, admit H to length 6, and submit a checked source use of H. Predicted
work: four receiver native stages (bootstrap, G, H, source use), plus one support
build; acquisition, refusal and selection allocate none. Record actual counts.

This count is package-list length, not theorem/dependency count: `admit` appends
distinct package records, then `union` checks list length before merging their
canonical contents. Existing H already carries its needed G dependencies, so
`C0 + H` is viable without a separately listed G package. This is a cheap real
pointer/package-cap discriminator, not evidence of discarding unrelated semantic
dependencies, useful growth, or behavior at the default 16-package boundary.

Alternative, one extra source stage: this same fresh consumer submits/publishes
an independently chosen small ordinary definition X against `C0`, then admits G.
Admitting its own published X must refuse length 7; select `C0`, admit X, and
submit a checked source use of X. Existing `publish` returns an ordinary owned
candidate and `selected_candidate` accepts it; no new self-admission path is
needed. This five-stage option can use an unrelated definition such as generic
composition, avoiding H's subsumption of G and preserving a nonempty earlier
local publication/artifact across selection. Independence must be checked in
X's actual canonical dependencies, not asserted from its name or author's intent.
Root selects one workload after source/allocation review; neither is executed here.

Record exact heads/preexisting records/publications/requests/charges before and after the
selection, its zero native/checker activity, successful fresh checks, and old
terminal replies. Include targeted controls: foreign/kind-invalid target;
stale expected head; exact selection replay after a later head change; no-op
selection; and missing selected live bytes in a separate fresh test allocation.
That last control must permit metadata selection and refuse subsequent use,
without deleting or mutating evidence of the positive run. Exact launch budgets,
source authorship, failure preservation and independent review remain required.

## What this decides, and what remains unsolved

This defeats needless monotone working-context accumulation: many investigations
can branch from a small retained context while knowledge stays published. It
does not let one proof's genuine dependency closure exceed the operation limit,
resolve incompatible foundations, select arbitrary subcontexts, discover useful
packages, repair missing files, refund native work, renew lifetime allowances,
or reclaim storage. Repeated reconstruction may still be expensive. Measure
retrieval, validation and source costs separately; do not infer speedup from
the pointer operation alone. Meaningful growth remains a separate empirical
reuse/benefit question, never a consequence of the number of selectable handles.
