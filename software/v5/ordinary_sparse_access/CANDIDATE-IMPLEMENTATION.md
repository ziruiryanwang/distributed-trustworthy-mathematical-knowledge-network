# Sparse candidate and provider source checkpoint

2026-10-25. Author: `ordinary_routing_gap`. Implemented only the root-selected
successors in this directory; no import, test, native stage, network operation,
package assembly, retained-state edit or Git operation occurred. Source review
and finite execution remain separate. Full v5 is not complete.

## Exact sources

| Successor | SHA-256 |
|---|---|
| `candidate_query.py` | `62de52fdd95df045632e865f90e5ec6ea076c8a1f68937d437597905e63a478b` |
| `http_provider.py` | `f81cdcaebbf05ad97342b81ac64444b33695b576045c8da41ba6f0a0903dd691` |

Baseline is the selected contact-federation assembly, PROFILE
`3d127796190ca3d049bd956288025c10c4ac7e383a15685aca6ea8d2fbc61479`.
Its original candidate/provider hashes are respectively
`b5d87baa539ce734b95891ea7358db96f137b39520151fd05c8e8272efe2d639` and
`250543498b83deb4a0893bd159ef6b890fcdd3744be4ca562079368a7f110954`.
Those used bytes were not modified.

## Implemented boundary

`validate_request`, `page` and `verify_page` accept keyword-only `sparse=False`,
reject non-Boolean selection and retain V1 default schemas, fields, atomic
traversal and delta/scan verification. Explicit True selects V2 request/page/
cursor schemas and the exact contract's `access_used` diagnostic. Proof
verification is shared; it is not a separate weaker implementation.

V2 planning calls `pair_access.plan` through the same `_ReadIO` before publishing
a non-null anchor count. Disabled/no-eligible pair chooses atomic traversal in
that same operation. Enabled cache errors propagate; no retry, construction or
replacement meter exists. All data SQL remains inside the original progress
handler/deadline envelope, with its cleanup in `finally`.

Each sparse driver attempt charges `scanned` before `next_row`, whose helper
charges its own indexed SQL/probe allowance. An empty completed seek is paid
before moving to the old anchor boundary. Nonempty rows require original
anchor and companion posting bindings, both old ordinal bounds, admission cut
and exact object/admission correspondence. A candidate rejected by an extra
conjunct first loads its canonical record and checks that the secondary
postings agree with that record; it consumes one record load but no proof.
Thus encountered corruption is not silently treated as a legitimate negative.

Full matches use the original atomic vector proof at their actual ordinal.
Byte-cap/proof/resource interruption does not advance past an unreported hit.
The wire upper bound includes the widest exact access diagnostic even before
planning, so later plan selection cannot overflow an otherwise empty page.

The V2 verifier alone omits the atomic ordinal-distance/scan inequality. All
record/proof/range/order/duplicate/byte/counter checks remain. V2 cursors also
explicitly validate integer partition/next values before mapping equality,
avoiding Python's Boolean/integer equality ambiguity. Returned V2 diagnostics
state `ATTEMPTED_DRIVER_SEEKS_NOT_ATOMIC_DISTANCE`; no scan coverage or
mathematical acceptance is created.

`http_provider.py` adds `SPARSE_CANDIDATE_ROUTE` to its closed routes and updates
all candidate dispatch, request validation, response reservation and effective
timeout sites. Route choice determines `sparse`; an incoming schema cannot
switch the selected mode. Existing V1 route behavior remains.

## Integration and remaining review

Root owns held-ticket dispatch, session charging, FairSearch mode binding,
public/CLI forwarding, `fair_exchange` allowlist and package/profile inclusion.
The helper author owns transactional cache/readiness/store limits. These sources
implement neither seam independently and must be reviewed as one selected
successor before execution.

No algorithm or test is claimed executed. The relevant discriminator remains
tiny inert late-AB retrieval plus changed-boundary controls; no native proof,
large corpus, network-wide recall or mathematical-growth experiment is needed
to check this local index/wire change.
