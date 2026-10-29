# Independent source review: owned ordinary acquisition

2026-10-28, growth_design_audit. **GO for root's finite file assembly and focused
validation selection.** No runtime or package adoption follows from this review.
Read-only source/diff/hash review; no product import, owner/database access,
network, native operation or Git action.

| Source | Reviewed SHA-256 |
|---|---|
| `ordinary_acquisition.py` | `677b6a6acd17de5ad60dbdd5700aac3014fc7a571876757b39382f8642f6d37e` |
| `fair_exchange.py` | `a04c4577a4fd6b3f68a48a869397d5ee35ec5075f7e5c1c496f5bb31fb06fc9a` |
| `CONTRACT.md` | `c8ad3988d790238b5919ffa04b47e0bc6ade6e121a066ae5a7a7f5f14f50ea5a` |

The exact source comparison is against ordinary_multi_source acquisition
`076130f7a34b505df33ee550501d1c4276bb46e408ff226df765225933a0658e`
and ordinary_connect_ownership exchange
`05cf2b5baef0130dbe3b43e594d6c800baf6b625c77125dd3356f59f78509575`.
Only the acquisition module description and `_fetch` differ; exchange changes
only its module description and closed route allowlist. The socket ownership,
framing, timers and cleanup paths are unchanged and reuse their adopted evidence.

## Correct scope and real improvement

The ordinary fetch predecessor used relative-timeout `H.exchange`, whose timeout
began after TLS context setup and whose writer-close errors could be suppressed.
The successor unconditionally uses the already owned exchange in both default
and explicit-fallback modes. It cannot silently fall back to the old transport.
This repairs an existing configured-supplier workflow independently of any DHT,
grouping or learned-source feature.

The four existing typed read routes are explicitly added: preview, locator,
evidence and authoring offers. There is no arbitrary-route admission. Authoring
offers still use default no-retry behavior, unchanged schemas and no retention
or repository following. Their shared `_fetch` use is therefore not broken by
the new transport's otherwise closed allowlist.

## Time, accounting and failure classification

`attempt_started` is captured at `_fetch` entry. The absolute horizon is the
minimum of the original ledger deadline and that start plus the validated
attempt cap, or the existing 60-second ceiling. It is passed explicitly through
the owned exchange, whose post-TLS/address check happens before socket creation.
Late setup cannot create a renewed interval. The remaining relative timeout
only narrows transport work; no new ledger is created.

The lazy fair-exchange import is inside the begun-ticket `try`, resolving the
current package loader's import order. Import failure is terminal and passes
through full-cap settlement. Existing exact request validation, one begin,
success validation/retention, before-commit liveness, HTTP counters and the
single `finally` settlement remain unchanged.

Owned `SettledRefusal` is handled as a value. Only timeout, connection refusal,
connection reset, broken pipe and peer EOF map to existing retryable reasons;
EOF maps to INCOMPLETE_READ. This mapping requires `unavailable_errors=True`.
HTTP_PROTOCOL, unknown reasons and all default-mode settled failures produce
terminal ValueError. HTTP 404/503 retain their existing opt-in handling; HTTP 400
and malformed or mismatched bytes remain terminal. TLS, cancellation, unobserved
cleanup and unknown exceptions are not intercepted by a broad retry catch.

The narrower behavior for ConnectionAbortedError is intentional: no owned settled
classification exists, so it is now terminal. The contract explicitly documents
that default returned refusals need not preserve the predecessor's exception
class. No caller should infer unavailability from an arbitrary exception class.

Every begun failure still settles its full reply cap. Only after settlement and
an additional original-budget liveness check can AcquisitionUnavailable escape.
The existing source scheduler catches only that type; expired grants and uncertain
cleanup cannot thereby authorize another provider. Successful validation is not
enough for discounted settlement if required retention or final liveness fails.

The unchanged owned helper needs up to one second of observed cleanup beyond
its attempt timer. The original outer allowance/reserve remains necessary.
Async timers do not preempt synchronous TLS/CA/parsing work; existing trusted
runtime/OS and external process containment premises remain.

## Unchanged mathematics and integration obligations

Locator semantic/export/name checks, evidence UnitID/output census, exact preview
binding and inert storage are unchanged. No admission, Lean, native helper,
semantic identity, mathematical schema or owner policy changes. A successful
acquisition remains explicitly non-acceptance.

The selected full investigator profile already imports/pins fair exchange.
Root should make a fresh two-payload source-map/PROFILE successor, keep the
installed core manifest/I exact, and compare the narrow local-anchor support
descriptor. Keeping owner.py, profile.py and the listed mathematical helpers
exact preserves anchor support in principle. Neither fact is proven merely by
this source review. The frozen standalone inert-host role has a different
closure without fair exchange and must not be patched with the new helper.

Focused controls should use the selected assembled successor, real typed codecs
and ledger, scripted transport outcomes, and the real unchanged source scheduler
where fallback is relevant. One post-setup no-dial control per typed route is
sufficient to connect the new allowlist to the existing owned mechanism; do not
repeat the whole raw-socket failure campaign. No new proof campaign is warranted.
No unresolved source blocker was found in the selected two-helper cut.
