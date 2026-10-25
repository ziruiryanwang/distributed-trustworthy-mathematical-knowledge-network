# From a discovered concept to a project to investigate

This addition is an advisory lookup, not a source downloader or Lean importer.
Runtime qualification is recorded in REVIEW.md; source preparation alone does
not establish public operation or a final v5 release.

An investigator can discover a connection, inspect its unfamiliar definitions,
and ask that provider for ordinary authoring-project hints. The investigator
chooses whether to obtain and approve a project. Its exported exact interfaces
must still be compared with the chosen mathematics, and contributed outputs
must still pass independent admission. Repository hints are not those checks.

## Client

Use the state-free `peer.py authoring-offers` command with the usual exact package
profile, runtimes, original resource allowance, pinned configuration and fresh
output directory. Do not supply catalog, custody, store-id or custody-limits.
The SDK entry is `await peer_api.authoring_offers(loaded, config, allowance,
network_budget=budget)`. Omit budget only for a new explicit standalone grant.

Configuration has exactly these fields:

```json
{
  "contacts": {"chosen-provider": "USE_THE_EXISTING_CONTACT_OBJECT"},
  "selection": {"provider": "chosen-provider", "export_id": "CHOSEN_64_HEX_EXPORT_ID"},
  "limits": {"requests": 1, "reply_bytes": 32768, "max_offers": 8}
}
```

The placeholders must be replaced with real selected values. One request uses
the package's semantic namespace and the chosen export identity. The response
is bounded, query-bound, explicitly unverified metadata. It may be empty or
truncated. Unsupported service is a failed lookup, not global absence. No
automatic retry, repository connection, checkout, installation or execution occurs.

## Provider

Existing `serve` configuration optionally adds
`"authoring_offers": {"path": "ABSOLUTE_MAP_PATH", "sha256": "EXACT_MAP_HASH"}`.
Omitting it or selecting null keeps the advisory role unavailable. The map is
an explicitly selected immutable snapshot, not a watched/live file or remote
write service. It is read and indexed once before listening; later changes to
the file do not alter that running snapshot.

CODEC.md specifies canonical JSON, map/offer fields and limits. A map has at most
2 MiB, 2,048 keys and eight offers per key. Queries inspect at most eight offers
for their exact key, not every key or every theorem worldwide. Ordinary service
request, byte, connection and lease limits also apply.

The operator must consciously approve disclosure of the selected map. Repository
locations may reveal private project names even when they contain no credentials.
Source URLs must not carry credentials, query tokens or fragments. The API never
verifies that a source repository exists or that its claimed commit is available.

## Using the information without changing mathematical authority

1. Select a hint or an independently obtained project. Treat every returned field
   as a provider claim; a valid theorem does not make linked code safe.
2. Apply local retrieval and execution policy before opening native project code.
   Do not interpolate returned strings into shell commands.
3. Use existing `produce-baseline` on the approved compiled project, selecting
   the required structured declaration names. Compare validated semantic/name/
   unit/export identities against the selected result. A different identity is
   not an automatically accepted alias or an assertion of mathematical inequality.
4. Investigate independently: propose definitions, models, countermodels, theory
   revisions or bridges. No network-prescribed research task is required.
5. Export, independently admit and publish chosen results through the existing
   workflow. New definitions and connection lemmas can be published as well as
   final propositions. Draft conjectures are not accepted premises.

This supplies a missing discovery-to-authoring information channel. It does not
establish that any advertised project is safe, reproducible, useful, available,
mathematically corresponding, or novel. Those are distinct obligations. Ordinary
project authoring and creative investigators remain necessary components.
