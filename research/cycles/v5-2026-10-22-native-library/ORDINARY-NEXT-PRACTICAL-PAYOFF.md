# Next practical payoff: inspect a candidate before paying to receive it

2026-10-24. Source/theory decision by `cold_intake_strategy`, incorporating the
independent discovery challenge from `module_anchor_audit` and root's proposed
minimal public boundary. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
This note performs no runtime, native import, owner/database opening, network
operation or Git mutation. Implementation and execution require separate root
selections. The full deployable-v5 goal remains open.

## Decision and user endpoint

**Expose the existing bounded, exact-record-bound type-preview operation as a
public command before adding another search mechanism.** A user or local agent
should be able to inspect an unfamiliar returned theorem's complete advertised
type, universe parameters and exact symbol bindings before deciding whether to
download its missing proof closure and independently check it.

The workflow is:

```text
existing formal query / explicit feature query
    -> existing bounded find
    -> explicitly selected candidate preview        [missing public seam]
    -> local decision to reject, investigate or receive
    -> unchanged independent receive / ordinary Lean use
```

The local decision is a search strategy, not an acceptance rule. No human
intention, global research agenda, usefulness vote or mathematical truth claim
is added to the network. A misleading preview can waste bounded inspection
effort but cannot become an accepted theorem through this operation.

This choice removes a concrete cost-ordering defect in the normal public
workflow. It does not invent a new retrieval algorithm: the underlying SDK
already supports the operation. Turning that capability into an ordinary usable
entry point has higher immediate payoff than adding yet another feature profile
while users cannot cheaply inspect the resulting candidates.

## What the inspected implementation actually does

The current source map selects `ordinary_peer_package/peer.py` and
`ordinary_resilient_package/peer_api.py` in the approved-project extraction
package. Those exact predecessors remain unchanged.

- `peer_api.find` returns `matches` containing `provider`, `snapshot_id` and
  `record`. It does not return the full type preview. Existing `find` already
  accepts one to eight kind, type-symbol, result-head, binder-domain-head or
  exact-type conjuncts. Its existing posting engine chooses the rarest selected
  posting anchor per partition; another index is not required for this decision.
- `peer_api.receive` calls `OrdinaryAcquisition.preview`, then immediately
  fetches the selected evidence, resolves preview/evidence correspondence,
  acquires the missing closure and calls `owner.admit`. There is no public pause
  between type inspection and those potentially substantial costs.
- `OrdinaryAcquisition.preview` already requests one object by advertised byte
  count and SHA-256. It checks those exact bytes and invokes
  `OrdinaryExportAdapter.resolve`, which reconstructs the complete ordinary
  record from the parsed preview and checks equality. This binds the advertised
  header, portable symbol bindings, features and locator to the selected record.
- The acquisition API explicitly accepts `local_custody=None`. It therefore
  needs neither a custody database nor an accepted-owner catalog to inspect a
  candidate. It performs no native checking or proof/dependency traversal.
- The existing preview transport cap is 1 MiB; its syntax limits include at most
  65,536 total type-DAG expression/level nodes and 4,096 type bindings. These are
  existing limits, not new larger allowances.

The prior query, reciprocal, module-anchor and approved-project intake outcomes
already establish their respective narrow boundaries. Another one-result
reciprocal fixture would not answer this new candidate-selection question.
The earlier body-discovery test reduced examined postings from eight to three
but increased search bytes from 103,356 to 202,790; it does not justify making
that optional two-stage profile the default. No prior result establishes broad
relevance, a positive whole-cost growth margin or final-v5 readiness.

## Smallest software contract

If separately selected, create fresh successors only:

| Fresh source below `software/v5/` | Delta |
|---|---|
| `ordinary_preview_package/peer_api.py` | Exact successor of the resilient peer API; add one public `preview` operation. Preserve the old operations. |
| `ordinary_preview_package/peer.py` | Exact successor of the peer facade; allow `preview` and classify it with `find` as requiring no state arguments. Preserve old paths. |

Root owns focused controls, the changed two-payload package selection, source
recipe/pins and any subsequent execution. Keep the existing profile loader,
discovery namespace, index records, wire routes, native installation, acceptance
rules and all unrelated package payloads unchanged. No compiler build, registry,
daemon, scheduler, new schema family or source renderer is needed.

The reusable API is:

```text
async preview(loaded, config, allowance, *, network_budget=None)

config = {
  contacts: <existing locally selected contact configuration>,
  selection: {provider, snapshot_id, record},
  limits: {requests: 1, reply_bytes: positive integer <= PREVIEW_MAX}
}
```

Use existing exact-field, contact/TLS, limit, semantic-namespace and record
validators. The selected provider must be one of the supplied contacts. Validate
the snapshot identifier's shape and preserve it, but do not infer proof of
membership from that identifier. Refuse before I/O if `record.object_bytes`
exceeds `limits.reply_bytes`. The original selected triple must survive the
result unchanged; no provider referral, substituted record, automatic fallback
or index lookup is permitted.

Use `OrdinaryExportAdapter` and
`OrdinaryAcquisition(adapter, endpoints, ledger, local_custody=None)`, then call
its existing `preview` exactly once. Do not call `evidence`, `locator`,
`OrdinaryStore`, `OrdinaryAdmission.open`, `owner.preflight`, `owner.admit` or
`allowance.operation`. Do not import/execute peer Lean, write a native module,
open SQLite, or admit a scratch theorem. Package/profile loading still checks
the selected local support; that is not owner-state opening or native execution.

Return JSON-serializable data rather than Python byte strings:

- the exact original `selection` and selected semantic namespace;
- the full canonical parsed preview document, including original names,
  declaration kind, ordered universe parameters, type DAG and type bindings;
- the exact received raw SHA-256 and byte count, checked against the record;
- the existing acquisition/network accounting and a bounded result status;
- `snapshot_membership_reverified: false`, `evidence_bound: false`, and
  `mathematical_acceptance: false`.

Use an assurance label limited to exact preview/record binding. The complete
preview document is inert metadata; it is not executable generated Lean or a
certificate. A future pretty-printer can be optional and nonauthoritative; it
is not required to expose this machine-readable contract. Retain existing
report-size checks and failure reporting rather than duplicating the document
unboundedly in several report fields.

The CLI must reject **all** catalog, custody, store-ID and custody-limit
arguments for `preview`, as `find` already does. It must not open these stores
and then claim to be read-only: opening an existing owner may settle reservations.
The fresh output directory and result file are the only intended local writes.

## Precise assurance statement

Let `R` be the selected ordinary record and `B` the returned preview bytes.
A successful preview operation establishes, under the existing hash/parser
assumptions and supported semantic profile:

```text
|B| = R.object_bytes
SHA256(B) = R.object_sha256
OrdinaryExportAdapter.extract(B, R.object_id) = R
```

The adapter's equality covers the exact export locator, namespace and full
recomputed feature set, not merely a display string. The syntax reader also
checks the complete header and the exact ordered census of referenced symbol
bindings. Nothing here proves that those symbols have accepted meanings or
that the type is inhabited.

In particular, this operation does **not** establish:

```text
R belongs to the claimed snapshot;
B is the header of actual full evidence;
the advertised declaration or its imported dependencies are valid mathematics;
the advertised theorem applies to the caller's goal.
```

An earlier successful `find` may independently have checked positive index
membership. Preserve that earlier evidence rather than pretending this new
operation repeated it. Full evidence correspondence remains `PP.resolve` in
the subsequent unchanged `receive` path, followed by actual independent
admission and Lean checking of the downstream application. A syntactically valid
lying preview can therefore pass inspection and must still fail a later
inconsistent-evidence check. This is an intentional trust boundary, not a defect
to hide by calling the preview "verified mathematics."

## Resource and failure contract

Use the existing `_network`/`OrdinaryBudget` path. A standalone call creates one
original ledger with exactly one request and the chosen reply-byte cap. A
composed caller supplies its existing active nonpending ledger; this call only
narrows its deadline and may consume at most one additional request. It closes
only a ledger that it owns. Never reset counters, refund failed work, renew a
deadline or close a caller-owned shared ledger.

`OrdinaryAcquisition._fetch` reserves the exact advertised preview size before
the request. Success settles actual bytes; a failed begun attempt is charged
the full reserved advertised size, not zero. Input/cap refusals before a begun
request consume no invented network work but still consume controller work.
Retain transport request/header accounting in addition to reply-body charges.
There is one selected candidate and no retry or provider continuation.

Search suballocations in a composed call must already be charged before the
first acquisition fetch; the existing budget deliberately disallows starting
a new prepaid search after acquisition has begun. The proposed standalone CLI
does not pretend that separate future commands share a persisted budget. Each
is an explicit separate owner grant, and whole-workflow analysis counts all of
them. Process limits remain cooperative unless an outer supervisor supplies
hard containment; reuse the existing cleanup reserve and error path.

Inspection work depends on selected bounded metadata and package validation,
not ancestral proof length or total global theorem count. This statement does
not make preceding search sublinear, ensure the selected index contains all
mathematics, make imports cheap, or guarantee that a relevant candidate exists.
Popular feature buckets and missing local vocabulary remain separate problems.

## Why this can help, and when it cannot

For a fixed set of inspected candidates `I`, let `J` be those the caller elects
to receive after inspection. Let `C_i` be the full cost of the old public
receive-to-inspect route for candidate `i`, and `P_i` the complete new inspection
cost, including its dispatch/profile checks, metadata transfer, parsing and
reporting. Keep the eventual selected `receive` calls unchanged. Then:

```text
old route: sum(i in I) C_i
new route: sum(i in I) P_i + sum(i in J) C_i
gain:      sum(i in I \ J) C_i - sum(i in I) P_i
```

This is a conditional workflow comparison, not a theorem that users would
otherwise receive every result. It applies when receiving was actually their
available way to inspect those candidates. It includes the repeated preview
fetch for selected candidates: current `receive` still obtains its own preview,
and the new operation does not promise caching or skip that binding check.
Additional provider/support costs must be included if not already in `P_i`.

The gain can be positive when several irrelevant candidates have expensive
missing closures. It can be negative for one already known relevant result or
very cheap warm acceptance. Direct callers of the existing SDK can already
obtain the same preview, so this is public operability and integration-cost
improvement, **not** a new cryptographic or asymptotic speedup. Do not manufacture
a positive result by withholding that SDK capability from an equally capable
baseline or assigning artificial native delays.

Conventional pinned Lake libraries remain the preferred shared background when
collaborators already approve and need that library. Give that route the same
index, metadata previews, caches and existing mathematics. The commons can add
cross-provider discovery and independently checked inert exchange for unfamiliar
extensions; extra assurance has a real cost. This change lets users select that
cost deliberately. It does not prove that inert acquisition beats an approved
package workflow, nor solve cold Mathlib onboarding through the current finite
completion envelope.

Optional certificates remain a later selective investment only when the number
and cost of strict cold checks justify their production and maintenance. Paying
for certificates to avoid checking irrelevant results is inferior to first
allowing those results to be inspected and rejected as metadata.

## Smallest necessary evidence and stop rule

Source review should establish the one-fetch/no-state call graph and exact
assurance/cap semantics first. Root's focused native-free controls can exercise
the real preview/record binding against retained ordinary preview bytes, with
a controlled transport and state/native opening made unreachable:

1. A correctly matched preview returns its full header/bindings and exact input
   selection without contacting an evidence/locator route.
2. Exact-byte/hash disagreement and a mismatched recomputed record refuse;
   forged features do not become accepted metadata.
3. Over-cap input refuses before a network attempt; one failed begun attempt
   retains its conservative charge; shared ledgers are neither reset nor closed.
4. State arguments refuse at the public boundary. No catalog/custody/native call
   is made on either success or failure. Output contains JSON data, not raw
   byte objects or executable source, and no authority flag is true.
5. A false but syntactically self-consistent advertised type is not described
   as proof-checked; the existing later evidence-binding rule is unchanged.

Existing transport, native admission and reciprocal campaigns need not be
repeated. A selected file-only assembly can establish exact two-payload change
and unchanged installation/namespace. If root later needs an actual command
discriminator, one preview of retained compatible publication metadata suffices;
do not start a new theorem, native build, broad timing campaign or networking
test merely to make a demonstration larger.

Stop after the new public selection boundary is established. Reassess the next
decision against real search/use behavior, especially meaningful candidate
coverage and large common-library onboarding. Do not turn this adapter into an
autonomous search policy, cache subsystem or new acceptance implementation.

## Alternatives deliberately not selected now

- **Structural query wrapper:** useful next convenience, but existing `find`
  already supports those feature conjuncts. Automatically conjoining all goal
  symbols is not substitution-complete: instantiated goals may introduce
  constants absent from a general theorem. A result-head restriction also
  excludes parametric-head methods. At most expose explicit local rigid-anchor
  choices later; no new namespace is justified by this wrapper alone.
- **A new applicability reducer/fingerprint:** the body observer and restricted
  instantiation observer already exist with precise limitations. No evidence
  currently warrants another normalization engine or profile proliferation.
- **Concurrent serving rewrite:** current public `serve` really does hold the
  owner lock and expose all selected custody. Decoupled immutable publication
  serving is a legitimate eventual operational requirement, but would introduce
  a substantially larger storage/concurrency boundary. It does not resolve the
  immediate cost of choosing among unknown candidates; do not casually remove
  the lock to make that issue disappear.
- **Generic cold scheduler or renewed certificate campaign:** these add cost
  before establishing that the user wants the candidate at all. The latest
  approved-project intake work does not establish cheap huge-library onboarding.

The central change is therefore modest but consequential: **make proof checking
a deliberate cost paid for selected mathematical candidates, not the price of
learning what every returned candidate claims.** This advances the practical
commons while preserving its independently checked mathematical boundary.

## Subsequent source-only implementation

Root subsequently selected `ORDINARY-PREVIEW-SELECTION.md`. The assigned API
successor is now authored at `software/v5/ordinary_preview_package/peer_api.py`,
SHA-256 `8b96e3bf7b7d5e3401b682f8eebc62a1d63421b9c4108dd94567db5f4d09c84f`.
Its complete predecessor text is preserved (line-ending-neutral prefix check),
followed by one additive `preview` function. Success fields are `selection`,
`preview`, `preview_sha256`, `preview_bytes`, `namespace`, `network`,
`acquisition`, and `status = PREVIEW_BOUND_NOT_ACCEPTED`, with the three false
authority facets specified above. No runtime or integration result is claimed.
Independent source review is requested; root owns controls and package assembly.
