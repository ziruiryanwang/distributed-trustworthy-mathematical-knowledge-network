# Actual concept-theory discovery inputs

2026-10-24. `concept_return_inputs`, source/input preparation only. Root selects
runtime separately. No owner API, state inspection, server, experiment or Git
operation was performed. The existing source route and query justification are
in `PRODUCT-DECISION.md`; this note records only the concrete configuration.

## Publication selection

`DISCOVERY-PUBLISH.json`: 5,371 bytes, SHA-256
`6ddd890a3c5380a26876b976c42128b9ac0377e1ac28c38ecadea0fa7c4437df`.
Created with apply_patch, then only the fresh terminal newline removed for
canonical compact UTF-8 JSON. All twelve `name`, `unit_id`, `export_id` rows are
copied unchanged from the saved actual B production reply at
`experiments/v5-local-checks/concept-theory-b-export-01/command/stdout.txt`.
These are not fabricated discovery results or preselected query answers.

The selected accepted context is root's actual returned B-intake root
`03de3aa800949731dfc0823d8661374c9f216262211c9bfe1ac6afd930421e20`.
The fresh index directory is
`E:\Distributed Trustworthy Mathematical Knowledge Network\experiments\v5-local-checks\concept-discovery-index-01`;
it was absent during preparation, and its existing parent is outside all
selected owner/custody/package/runtime directories. `create` is true.

Publication uses existing native-src01 `peer.py publish` with the same exact
PROFILE/runtime/recipient/store/custody-limits arguments as B intake. Replace
the owner entry/operation with peer entry/publish; use `--config`,
`--config-sha256` and a separately fresh `--output` spool. Keep the runtime and
profile pins; snapshot this config and unchanged CUSTODY-LIMITS.json. No module
generation, baseline recheck, registration, build or new mathematical fixture
is required. Root owns the finite allowance and outer runner selection.

## Bounded size choices

The twelve selected unit files total **169,565 bytes**, with maximum **19,945
bytes**. These counts were read from actual saved B unit files, not extrapolated
from theorem count. `max_unit_bytes=32768` and `max_total_bytes=262144` therefore
cover the exact preparation-stage inputs; the public call checks actual custody
bytes again. The total is the sum per target, matching `publish` accounting.

Index ceilings are:

| Limit | Selected |
|---|---:|
| Objects | 16 |
| Postings | 2,048 |
| Distinct features | 2,048 |
| Snapshots | 16 |
| Logical bytes | 67,108,864 |
| Database pages | 32,768 |

There are twelve targets. Each successful adapter record has at most 128
features, so total postings and distinct features cannot exceed 1,536 for this
selection. There is one initial snapshot plus at most twelve publication
snapshots. The logical/database quotas are finite conservative storage
allowances, not measured allocation or memory consumption; live accounting must
still succeed. No claim is made that every theoretical worst-case index fitting
the count caps fits those byte quotas.

## Existing checks and partial-state boundary

`peer_api.publish` (lines 429–467 in the selected package) requires exactly the
config's five top-level keys; each target's exact three keys; unique structured
names; agreement with the live accepted context binding; and the export identity
derived from semantic ID, unit ID and name. It reads the selected unit from local
custody under both byte ceilings, derives and resolves its preview, and checks
the preview's export identity before any index publication. Publication is not
new mathematical admission and does not trust the old export success receipt.

All target previews are prepared before the fresh index is opened. Each later
`put_preview`/index admission is a separate persistent step; publication of the
twelve records is **not atomic**. Preserve any successful prefix on failure;
never retry the same fresh-index operation blindly or report zero progress from
a late failure. Actual results, not this preparation, establish discoverability.

## Minimal subsequent commands, not yet configured or selected here

`concept_product_decision` owns the full existing-API source map and finite
serve/find/preview recommendations in `PRODUCT-DECISION.md`, avoiding duplicate
route analysis. Essential constraints for the next root decision:

- Serve the existing index (`create:false`, identical index limits) on
  `127.0.0.1`, requested port 0, `tls:null`, with a finite lease and cleanup
  reserve. Read the actual `READY` port, never predict it. Public serve requires
  `share_all_custody:true` and `exclusive:true`: it exposes the whole selected
  concept-recipient custody, and holds its catalog lock for the lease. Do not
  run publish/intake against that recipient concurrently.
- Find is owner/custody-free. Use a caller-chosen A concept's known portable
  symbol in `specs`, not a B theorem name/ID disguised as unknown-ID discovery.
  Contacts require all six fields (`host`, `port`, `tls`, `server_name`,
  `ca_file`, `ca_sha256`), with loopback actual port, false TLS, null server/CA
  fields. Select the provider label explicitly. All search/offer/page budget
  keys are required and must lie within the selected public source bounds.
- Preview is also owner/custody-free. Build its `selection` only from an actual
  find result (`provider`, `snapshot_id`, `record`). Limit it to one request and
  a byte ceiling covering the returned record's `object_bytes`. It fetches and
  recomputes the exact type record; it is not acceptance of the whole theorem,
  no-producer-code authoring, or proof of broad semantic relevance/recall.

No keys, server startup, later config files or automatic continuation are
created by this preparation. The intended new evidence is a finite public
query from A's known concept to independently developed B connections, not
large-network qualification or a claim of research acceleration.
