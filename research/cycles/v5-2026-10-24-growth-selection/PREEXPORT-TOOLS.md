# Pre-export discovery: actual upstream tools and the missing boundary

2026-10-24. Author: `preexport_tools`. Read-only primary-source comparison;
no install, build, local index, source execution, provider deployment, product
edit or migration. One small public GET checks the existing JSON response shape;
it is not an interoperability campaign or a search-quality experiment.

## Decision

Reuse Loogle for formal candidate generation. Existing LeanSearchClient and
lean-lsp-mcp already connect agents/editors to configurable Loogle providers.
Another single-endpoint client, parser, matcher or natural-language interface is
not the missing invention. The narrow potentially useful addition is **bounded,
plural-provider advisory discovery that preserves provider/corpus assertions
and explicit outcome/coverage limits** before any ordinary package acquisition
or exact evidence export. Root must decide whether this gap pays for its cost.

Loogle output is a candidate hint. It is not an accepted theorem, proof-derived
content identity, verified package locator or applicability certificate. The
provider's current JSON does not bind a response to a corpus revision at all.

## Source identity

GitHub's commit endpoint was inspected on 2026-10-24, then the selected source
files were read at those immutable commits. Earlier search-engine/raw-master
views supplied navigation only; the claims below use the pinned files.

| Tool | Pinned commit | Relevant primary sources |
|---|---|---|
| Loogle | `9f11169aaebf1ed1e7dcc4077f2aafe0fcf66fd0` | [README](https://github.com/nomeata/loogle/blob/9f11169aaebf1ed1e7dcc4077f2aafe0fcf66fd0/README.md), [HTTP server](https://github.com/nomeata/loogle/blob/9f11169aaebf1ed1e7dcc4077f2aafe0fcf66fd0/server.py), [JSON/import/index implementation](https://github.com/nomeata/loogle/blob/9f11169aaebf1ed1e7dcc4077f2aafe0fcf66fd0/Loogle.lean), [CLI](https://github.com/nomeata/loogle/blob/9f11169aaebf1ed1e7dcc4077f2aafe0fcf66fd0/LoogleMain.lean), [matching/ranking](https://github.com/nomeata/loogle/blob/9f11169aaebf1ed1e7dcc4077f2aafe0fcf66fd0/Loogle/Find.lean) |
| LeanSearchClient | `9d39f9bb0c30aa2f6200808805ff16e6ce950890` | [LoogleSyntax](https://github.com/leanprover-community/LeanSearchClient/blob/9d39f9bb0c30aa2f6200808805ff16e6ce950890/LeanSearchClient/LoogleSyntax.lean) |
| lean-lsp-mcp | `f00f625810d183dbb597a3677d2d5a83b084f761` | [Loogle transport/worker](https://github.com/oOo0oOo/lean-lsp-mcp/blob/f00f625810d183dbb597a3677d2d5a83b084f761/src/lean_lsp_mcp/loogle.py), [search tool](https://github.com/oOo0oOo/lean-lsp-mcp/blob/f00f625810d183dbb597a3677d2d5a83b084f761/src/lean_lsp_mcp/tools/search.py), [dependencies](https://github.com/oOo0oOo/lean-lsp-mcp/blob/f00f625810d183dbb597a3677d2d5a83b084f761/pyproject.toml) |

## Loogle protocol: enough to implement an adapter without guessing

### Request and transport

- `GET /json?q=<URL-encoded formal query>` is the JSON endpoint. The client
  should construct this request from an explicitly configured provider endpoint,
  not follow a returned link. `POST /zulipbot` is a separate bot interface and
  is irrelevant to this adapter.
- The HTTP wrapper accepts only one `q`, strips outer whitespace and a leading
  `#find `, then replaces Unicode whitespace with ordinary spaces. Missing,
  repeated or effectively empty query values can produce `{}` with HTTP 200;
  that is not a successful empty search.
- There is no query echo, request token, pagination/cursor or request-specific
  result-limit parameter. The operator's `--max-results n` controls the backend
  limit (default 200). Adding `limit=` to the URL would not impose a limit.
- Semantic/query/backend failures normally use HTTP 200 with an `error` field.
  Pool saturation uses HTTP 503, `Retry-After: 5`, and an error JSON object.
  Unknown paths return 404. The wrapper has a specific default-user-agent deny
  rule; use an honest identifiable client user agent, not a bypass mechanism.
- `returnJSON` sends `application/json`, serializes JSON as UTF-8, and provides
  CORS headers. It does not itself add content compression, content length,
  immutable cache validators or version headers. A reverse proxy can alter
  transport properties; do not infer every provider's behavior from this source.
- Normal adapter requests need neither `lucky` nor redirects. `lucky` can turn
  results into a redirect to a documentation page. Rejecting redirects preserves
  the explicit provider boundary and is not an upstream incompatibility for the
  ordinary JSON request.

### Response schema

Pinned `Loogle.lean` lines 83-110 emits:

```text
success = {
  header: string,
  heartbeats: nonnegative integer,
  count: nonnegative integer,
  hits: [{name: string, type: string, module: string|null, doc: string|null}],
  suggestions?: string[]
}

failure = {
  error: string,
  heartbeats?: nonnegative integer,
  suggestions?: string[]
}
```

`type` is pretty-printed text, not a round-trip expression encoding. Even pretty
printing can return a failure-message string in that position. Names, modules,
documentation, headers and suggested queries remain untrusted data; do not
execute them or assume they name locally compatible declarations.

In `Loogle/Find.lean` lines 509-529, sorting occurs before `maxShown` truncation.
`count` reports the pre-truncation count after filtering; `hits` is the returned
prefix. Thus `count > len(hits)` establishes a provider-reported truncation,
not a missing-page retrieval mechanism. Conversely equality proves neither
truthful reporting nor global or corpus completeness. The display limit is
**not** a bound on backend matching/sorting work.

### Worker and corpus binding

The wrapper launches `[loogleBin, --json, --interactive, ...forwarded args]`;
`--project-dir` wraps that launch in `lake -d <directory> env`. The root module
is selected through forwarded `--module`, normally `Mathlib`. The worker's
actual environment is therefore determined by the selected project/toolchain,
Lean search path, root module and imported artifacts. Multiple configured
workers each hold their own environment in memory; they are capacity replicas,
not mathematical corpus shards selected by the query.

The page footer and optional Prometheus metrics expose the Loogle revision and,
when obtainable, project name plus `git rev-parse HEAD`. These are not present
in the JSON search response, do not detect a dirty worktree and do not commit to
the resolved dependency/artifact closure. The public service is described as
periodically updating Mathlib. A client-side descriptor can pin an **operator
assertion**, but cannot cryptographically bind this unmodified response to it.

Consequences for a selected advisory client:

1. Preserve the exact configured descriptor identity and endpoint alongside each
   hint, calling them asserted corpus/provider information.
2. Do not claim compatibility merely from an advertised Lean version or commit.
3. Do not merge equal theorem names from distinct corpora into one mathematical
   identity. Repeated hints may be grouped while retaining their separate origins.
4. Use the descriptor's package location only as a lead for a later explicit
   acquisition; no discovery-triggered build, import or executable download.
5. The current protocol cannot report cryptographically verified query coverage.
   Stronger binding would require an explicit provider-side successor, not an
   undocumented reinterpretation of this upstream response.

### Local use and safety

Loogle can search a built Lake project's selected module without adding Loogle
as that project's dependency, provided its binary uses the matching toolchain.
The README documents `lake env <loogle binary> --module <root> <query>` and
on-disk index modes `use/read/write/none`. Dependency-trace hashes detect cache
staleness when available; `read` refuses missing/stale data, while stdlib modules
without the required trace need the documented nonpersistent fallback behavior.

This is useful existing indexing, but not hostile-input ingestion. Loogle enables
Lean initializer execution and imports environment extensions. Downloading a
package and invoking local Loogle is executable-package trust, not inert theorem
checking. A remote advisory client avoids this particular local execution path;
it does not make the remote operator or its corpus mathematically trustworthy.

## Existing clients: avoid redundant implementation

### LeanSearchClient

`getLoogleQueryJson` already honors `LEANSEARCHCLIENT_LOOGLE_API_URL` (default
includes `/json`), invokes `curl -X GET`, parses hits and creates Lean editor
suggestions. In tactic mode it tries proposed tactics in the current local
environment and displays successful ones. This already supplies local use of
remote candidates; no need for a bespoke applicability engine.

The inspected adapter caches `(query, num_results)` without endpoint/corpus in
the key, discards `module` and `count`, limits results after parsing the full
response, and supplies no explicit curl time/byte limit. It is not a bounded
multi-provider coverage client. Selecting it as-is would also involve a
toolchain-compatible Lean dependency; no such installation is selected here.

### lean-lsp-mcp

The existing `lean_loogle` tool supports configurable `LOOGLE_URL` and
`LOOGLE_HEADERS`; its remote helper issues the same GET with a 10-second socket
timeout. It reads the whole body before JSON parsing and result slicing, and
returns name/type/module without count or corpus. Local Loogle mode can switch
to remote after a local failure; that is useful convenience but must not be
mistaken for invariant corpus coverage. The pinned package is Python >=3.10,
with leanclient, MCP, orjson and certifi dependencies.

This is an existing agent integration worth documenting, not rebuilding. The
upstream README's full-Mathlib memory measurements and Unix-only local mode
are a further reason not to select a local full-Mathlib index for this bounded
decision. Those upstream measurements are not measurements on our PC.

## One actual public response, narrowly interpreted

Observed response date: `Sat, 24 Oct 2026 22:27:42 GMT`.

Request: `https://loogle.lean-lang.org/json?q=%22Nat.add_comm%22`, explicit
`MathematicalCommons-SourceAudit/1.0` user agent and `Accept-Encoding: identity`.
HTTP 200; `Content-Type: application/json`; transfer encoding `chunked`;
`Vary: Accept-Encoding`; no observed `Content-Encoding`.

```json
{"count":1,"header":"Found one declaration whose name contains \"Nat.add_comm\".\n","heartbeats":0,"hits":[{"doc":null,"module":"Init.Data.Nat.Basic","name":"Nat.add_comm","type":" (n m : ℕ) : n + m = m + n"}]}
```

This confirms that the inspected small response shape is actually available.
It does not identify the live backend commit, verify the theorem, show support
for custom packages or prove any finite-corpus/global completeness or latency
guarantee. No live error/load/large-query probing was needed.

## Smallest justified next boundary

If root selects implementation, retain the upstream search semantics. The new
part should only make configured finite advisory providers usable under explicit
aggregate budgets, preserve descriptor identities and distinguish unavailable,
invalid, truncated, empty and candidate outcomes. Bound provider count, request
size, response bytes, retained hits and elapsed time; prohibit redirects and
implicit network fallback unless explicitly represented as separate providers.
Content encoding and chunked transfer need a deliberate bounded-reader policy.
Request-origin binding is client bookkeeping, not an upstream query echo.

No replacement matcher, global registry, package installer, proof-authority
change or LLM intent interface is justified by this comparison. Discovery helps
only if selected providers already cover useful work in a compatible ecosystem;
the software should expose that unresolved condition, not fill it with fictitious
content IDs. Bounded client cost does not establish bounded server cost, nor
does transport integration itself establish useful growth.
