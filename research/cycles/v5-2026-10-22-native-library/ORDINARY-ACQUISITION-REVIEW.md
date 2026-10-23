# Ordinary acquisition and inert custody: independent source review

2026-10-23. Reviewer: `admission_event_audit`. **No blocking source finding**
for the exact candidate below under its stated protected-owner, serialized-call
and external-containment premises. This is source review, not executed transport
qualification, native admission or deployment approval. No test, compiler, native
worker, network call or store creation was run by this reviewer.

| Reviewed file | SHA-256 |
|---|---|
| `software/v5/transport/ordinary_acquisition.py` | `e69bd0f33829e4709fdc1a7c3afe4150704dfeabfe30243195b379945081e826` |
| `software/v5/transport/http_provider.py` | `431aae7f10f1a2c0c0323c4aea720f4139e57bb4bf7b61bf98e9e5b69d6cdd59` |
| `ORDINARY-ACQUISITION-IMPLEMENTATION.md` | `b0ef512cfabe30baf831bf515924681492ea10d3c975b3cd5bfdf92117c0f86d` |

The full two implementation files and author checkpoint were read. The reviewer
also inspected the existing portable preview/evidence semantics, complete ordinary
discovery adapter, explicit-endpoint client configuration, canonical JSON and
ordinary-path helpers, and the narrow HTTP diff against the existing tracked
provider. Existing TLS, message framing and exchange cleanup are reused unchanged.

## Practical workflow and authority

The unit addressed by a known ExportID cannot be recovered by inverting that hash.
The new explicit locator operation closes that practical gap: lookup returns a
candidate `(S, UnitID, originalName)`, then the client recomputes the requested
ExportID and any independently expected original name. A separate evidence fetch
checks the exact UnitID/S and, when given the paired expected export arguments,
requires that name in the complete parsed output census. A self-consistent
locator for a nonexistent output therefore cannot pass the paired acquisition.

Preview fetches bind advertised exact byte length/hash and reconstruct the whole
index record through the ordinary adapter, including features and locator.
Neither this nor an exact evidence fetch proves the advertised mathematics.
`portable_preview.resolve` still binds the selected preview's header/type bindings
to actual complete evidence; independent native admission still checks new work
against warranted imports. All new acquisition/store/provider results retain
explicit nonacceptance. There is no accepted flag, private grant, native artifact
load, remote source execution, recursive download or hidden retry in this layer.

## Resource and failure reasoning

- Preview, locator and evidence requests use exact field sets and finite route
  caps. Provider reservation is the validated request cap, not an unchecked
  caller value. Raw ordinary replies bypass only the old object re-encoding,
  not response-size or provider-budget checks.
- One owner budget covers all explicit acquisition calls and providers. It
  reserves a reply cap and consumes a request before dispatch. Serialization
  forbids a second outstanding ticket. The `finally` settlement survives
  validation, storage, timeout and cancellation failures, charging the full cap
  unless the entire operation succeeds. Failed attempts cannot refund their
  work by switching providers.
- The absolute parent deadline is never renewed by the client or store. External
  search/location must be prepaid before the first fetch and its subbudget
  independently enforced by its owner. This is an integration obligation, not
  an automatic assertion that arbitrary external work was charged correctly.
- Reply bodies are not described as total network cost. Completed response
  counters and conservative request/header bounds are distinct. CPU, SQLite,
  TLS and incomplete I/O costs require the enclosing accounting/containment.
  The unchanged exchange can spend up to an extra second on socket cleanup;
  synchronous Python/SQLite work is not forcibly preempted by soft callbacks.

## Custody and reuse

Puts validate bounded canonical syntax and exact S, then atomically store the
raw object, every output's recomputed locator and quota counters in one SQLite
transaction. The four separate limits cover object count, export-row count,
logical bytes and physical database pages. Duplicate puts compare exact bytes
and existing locator rows without a second quota charge. Failure before commit
rolls back the new rows; failure after a successful commit can leave inert data,
which is explicitly permitted and never implies mathematical acceptance.

Reads check BLOB size before loading it and hash the actual bytes against both
the saved raw digest and requested content ID. Under the protected-owner database
premise, the syntax/S check performed at put need not be repeated for each service
read. This removes repeated full unit parsing/census from the provider hot path
by construction. A recipient independently parses its selected remote evidence.
Locator serving verifies the small canonical locator and retained evidence
presence, without rereading the full evidence merely to return its location.

Cold reopen requires exact S and quotas and retains SQLite DELETE/FULL behavior,
ordinary nonaliased paths, bounded database/journal checks and refusal of WAL/SHM
sidecars. It does not construct a Lean context. External mutation and concurrent
owner calls remain outside this source's protection model; hashing alone does not
authenticate a maliciously rewritten database plus rewritten metadata.

The prepromotion contract is important: keep the complete inert evidence in
durable custody before accepted catalog promotion. A native snapshot/UnitID
alone cannot later republish the proof-bearing portable object. The candidate
provides that API; the separate admission controller must actually call it.

## Supported-profile and integration limits

The locator's existing preview-name limits are stricter than ordinary evidence
name limits. An evidence unit with any output outside that locator profile is
rejected as a whole, not partially retained while silently omitting exports.
That is an explicit supported-profile refusal, not mathematical invalidity; the
generic admission path must expose it before promotion. Basis symbols remain
local foundation obligations and do not acquire fabricated ordinary locators.

The API is deliberately explicit: callers choose contacts, bind preview/evidence,
resolve missing imports and invoke admission. It is not yet the full public
workflow or a guarantee of independently hosted availability. Its per-object
operations do not solve arbitrary missing-closure acquisition or efficient cold
Lean environment loading. These boundaries should be addressed in the product
controller rather than hidden inside this otherwise inert transport layer.

## Recommended next discriminator

Root may select one compact changed-boundary loopback/control run, not a replay
of the old module, catalog, translation or proof campaigns. It should check the
real preview/locator/evidence routes together, wrong S/ExportID/name, a locator
whose requested output is absent, same-name exports from different units,
multi-output projection, aggregate failures/exhaustion across providers, and
cold custody re-serving after the original provider stops. This establishes the
new transport seam only; it must not be presented as a growth or release result.
