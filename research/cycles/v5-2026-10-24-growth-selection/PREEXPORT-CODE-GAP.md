# Pre-export ordinary search: smallest current code gap

2026-10-24. Source-only recommendation; no product edit, build, install or test.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Read with PREEXPORT-SELECTION and PREEXPORT-TOOLS in this directory.

## Decision

Add a **standalone, bounded advisory Loogle consumer**, if root selects it.
It should search explicitly configured existing providers before ordinary proof
export, without loading an acceptance owner, Lean runtime or native profile.
Return provider-labelled declaration hints; leave acquisition, compatibility,
local applicability and exact output acceptance to their existing boundaries.

This is integration of an existing useful formal search engine, not a new
mathematical search algorithm or evidence of superiority to ordinary Loogle.
Do not build a hint registry merely because the project already has an index.

## What the current product actually exposes

- `software/v5/ordinary_preview_package/peer.py:145` loads owner bootstrap and
  the full profiled support/runtime mapping before `find` dispatch. `find` is
  owner-state-free, but not independent of that installed checking support.
- `ordinary_preview_package/peer_api.py:161` binds search to
  `OrdinaryExportAdapter(loaded.installation.semantic_id)` and exact feature
  specifications. Explicit contacts, shared budgets, no automatic referrals and
  incomplete-search reports are sound patterns worth retaining.
- `ordinary_formal_query/discovery/ordinary_export_adapter.py:32` binds its
  namespace to semantic ID, exact preview/evidence/unit formats and type-key
  profile. Its query uses proof-derived portable symbol identities, not ordinary
  Lean names interpreted in an arbitrary remote corpus.
- That adapter's `validate_record_locator:94` requires a real exact export
  locator and recomputed export identity. `describe` derives metadata from an
  actual portable preview. This path cannot honestly advertise an unmaterialized
  ordinary declaration by inventing its missing proof-unit identity.
- `ordinary_formal_query/README.md` already notes that ordinary Loogle or local
  `#check` can be cheaper. Existing exact type keys do not perform general
  reduction, unification or specialization.

The missing public operation is therefore **advisory ordinary-corpus search
without exact export**, not another acceptance mode.

### Important reuse qualification

`discovery/formal_features.py:146` also accepts generic V1 records with arbitrary
bounded `kind`, namespace, object identity, byte commitment and feature hashes.
The low-level store is not intrinsically restricted to proof-derived exports.
A new hint adapter in a distinct namespace is possible in principle.
It still needs useful query semantics, hint storage/locators, maintenance,
provider ingestion and a public facade. Snapshot inclusion would certify only
metadata inclusion, not correct extraction, compatibility, availability or truth.
That larger option is not the cheapest way to use an existing formal search tool.

## At most three integration choices

| Choice | Actual new responsibility | Judgment |
|---|---|---|
| Thin advisory Loogle client | Explicit providers, bounded GET, exact response parser, labelled report | Select first: supplies ordinary formal search before export |
| Distinct generic V1 hint index | New extractor/corpus, hint custody, query semantics and provider maintenance | Defer until an important corpus is demonstrably missing from existing tools |
| Put source names/fake IDs into ordinary V3 export records | Change proof-derived identity meaning and mislead existing consumers | Reject: invalid semantic substitution |

Several replaceable configured providers are sufficient for this first boundary.
No compulsory central directory, globally synchronized registry, bootstrap
network, provider-discovery protocol or new mathematical authority is needed.
This does not make unpublished/unindexed packages discoverable automatically.

## Why the existing HTTP implementation is not the right adapter

`transport/http_provider.py:29,44,75,114` admits fixed `/v5` POST routes, IP-literal
endpoints and a narrow Content-Length/JSON/Connection-close header profile.
Loogle uses GET `/json?q=...`; its actual public response can be chunked and have
ordinary additional HTTP headers. Existing `SearchClient` also expects our
snapshot/ticket protocol, not Loogle JSON. Pointing it at Loogle will not work.

Reuse the budget/trust principles, not by broadening the existing exact evidence
transport or making its isolated assemblies depend on an unrelated upstream API.
A small standard-library `http.client` adapter is adequate. It needs no external
HTTP dependency, no source execution and no modification of mathematical state.

## Proposed minimal contract

This section is a source-selection proposal, not a claim of implementation.

### Input and local context

Accept a bounded UTF-8 Loogle query and a finite explicit provider list. Each
provider has a locally unique label, HTTP(S) origin and optional owner-supplied
corpus description: project/repository, revision and Lean toolchain. Unknown
values stay unknown. Configuration claims are not authenticated corpus facts.
Use HTTPS with normal certificate/hostname verification for remote providers;
plain HTTP is only an explicit loopback test/local-service option.

Reject URL credentials, fragments and ambiguous endpoint paths. Build only the
fixed `/json` request with a properly percent-encoded `q`. Returned names, docs,
module names and suggestions are inert strings: never commands, paths, imports,
referrals or follow-up queries. No auto-download, package installation or Lean
execution; no automatic suggestion following or retry.

Use direct connections with no ambient proxy lookup, cookies, authentication or
credential injection. Reject redirects and compressed content. A configured
origin authorizes that exact request destination, not arbitrary returned URLs.
DNS results do not establish operator independence or corpus identity.

### Exact upstream JSON shape

Pinned adapter reference: Loogle commit
`9f11169aaebf1ed1e7dcc4077f2aafe0fcf66fd0`,
[`Loogle.lean:83-110`](https://github.com/nomeata/loogle/blob/9f11169aaebf1ed1e7dcc4077f2aafe0fcf66fd0/Loogle.lean#L83-L110).

Success requires:

```text
{header: string, heartbeats: nonnegative-integer, count: nonnegative-integer,
 hits: [{name: string, type: string, module: string|null, doc: string|null}],
 suggestions?: [string]}
```

Error shape is distinct:

```text
{error: string, heartbeats?: nonnegative-integer, suggestions?: [string]}
```

An empty object is not an empty successful result. Query errors can arrive with
HTTP 200; HTTP failure statuses remain failures. Integers must reject booleans.
Reject duplicate JSON object keys, nonfinite numbers, wrong types and malformed
JSON; bound strings, collection counts and body size before treating it as a
report. `count >= len(hits)` is a consistency check, not proof of completeness.

Use a versioned local parsing profile with strict recognized fields and a
clear unsupported-response outcome. Upstream explicitly does not promise format
stability. A server revision is not established merely by parsing the expected
shape; the pinned source identifies the adapter's interpretation only.

The response supplies no package/revision binding and no query echo. Pair it
with the locally recorded request and explicit provider context; do not invent
those missing claims. A module/name is a useful advisory locator within that
provider's claimed corpus, not an exact globally unique mathematical identity.

### Resource boundaries

Specify one original aggregate allocation: providers attempted, requests,
UTF-8 request/query bytes, response entity-body bytes, returned hits and deadline.
Deduct failed/malformed attempts too. Do not silently renew it per provider.
Finite conservative defaults can be small, e.g. eight providers/eight requests,
2 MiB aggregate body, 256 returned hits and 30 seconds; exact chosen constants
belong to root's implementation contract, not mathematical acceptance rules.

Chunked responses need support for the actual service. A bounded body read bounds
decoded entity bytes, **not all network wire bytes**: HTTP headers, chunk framing,
TLS and transport overhead are separate. Do not call a payload counter a hard
bandwidth guarantee. Reject unexpected content encoding and enforce response
caps while reading, not only after collecting an unbounded body.

Socket timeout alone does not bound synchronous DNS or repeated slow reads.
For a hard elapsed-time boundary, use a fixed same-file worker in a separately
terminable process, with no renewed overall deadline. Parent output collection
must itself be bounded; timeout kills only the owned worker. Without this
containment, report the deadline as cooperative, not hard.

Client caps do not bound external provider computation. Pinned Loogle
`Find.lean:509-529` sorts matches before limiting them; client clipping cannot
make an expensive server query cheap. Never infer global sublinear semantic
search, fairness or bounded remote CPU from a finite client response.

### Output and trust separation

Return per-provider status, local query/context, bounded parsed hits, response
body hash where acquired, parsing profile, provider-reported count/heartbeats,
local truncation/failure flags and aggregate costs. Distinguish owner-configured
corpus labels from provider-reported fields. Missing revision stays unknown.

Always state `mathematical_acceptance=false`, `verified_coverage=false` and
`global_complete=false`. A no-hit result means only that the queried provider
returned no hits for that request. Results from different provider/corpus
contexts must not be semantically deduplicated merely because names coincide.
The report is local integration data, not a new authenticated index protocol.

The safe flow remains: advisory hint -> explicitly chosen approved ordinary
package -> actual Lean applicability/authoring -> optional selected export ->
existing independent exact-output validation. Neither discovery success nor
upstream compilation may bypass the final mathematical acceptance policy.

## Targeted later qualification, if selected

One native-free contract suite can cover known-shaped success, genuine empty
success, upstream query error, `{}`, duplicate/wrong-type fields, oversized body,
unexpected compression, redirect refusal, chunked response, timeout and shared
two-provider budget exhaustion. Test same-name/different-corpus separation and
absence of owner/profile/native imports. A fixed-worker timeout control is
needed if the product claims a hard wall deadline; socket tests alone cannot
establish it for a blocked resolver. No proof or package rebuild is needed.

Fixtures establish parser/accounting behavior, not relevance. One separately
selected actual upstream request can test live API compatibility; source-only
inspection already supports design feasibility. PREEXPORT-TOOLS retains the
existing observed public response, so do not repeat it without a changed boundary.

## Growth meaning and stop rule

The candidate payoff is lower search/integration friction before expensive
conversion, with no mandatory prover work. It is not theorem-count growth or
proved speedup over a browser/local Loogle. Its incremental benefit exists only
where repeatable bounded multi-provider use is worth more than its integration
and service costs. Ordinary existing clients remain valid alternatives.

Stop after this boundary if existing tools already serve the consumer. Do not
continue into a new ranker, bridge miner, package registry, checker campaign or
certificate system without a separate concrete consumer failure and cost case.
Meaningful uptake and source-policy compatibility still need real downstream use;
the user's lack of an existing local Lean project is not evidence of that use.
