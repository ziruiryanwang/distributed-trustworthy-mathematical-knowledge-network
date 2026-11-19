# Find a custodian for an exact missing import

This optional service connects the existing ordinary reader to independently
operated custodians. It does not decide mathematical truth. The reader still
checks the exact locator, evidence and mathematical imports using its selected
Lean-based checking policy.

There are two separate roles. A **custodian operator** advertises selected outputs
that an existing ordinary HTTP host currently serves. A **gateway operator**
searches the maintained DHT and returns bounded advisory endpoint hints over HTTP.
Readers need Python and their normal mathematical installation, not Node or an
inbound listener. Operators use the separately pinned Node runtime; they need no
mathematical owner or Lean installation. One person may run both roles separately.

The sources in this folder are under integration review. Their existence is not
an adopted release or evidence of a running network. The current adopted reader
and host remain identified by their existing ADOPTION documents.

## Practical sequence

1. Export a new contribution with the existing ordinary workflow and create its
   baseline bundle. Append that bundle to an ordinary incremental host and serve
   it using the existing host role.
2. Give the custodian operator that bundle and the host's approved endpoint.
   It derives exact export identities from the new units, including support
   declarations. Before each publication it reads the exact locator from its own
   endpoint and checks its semantic ID, unit ID and declaration name.
3. Start a separate gateway with an operator-approved bootstrap peer. Configure
   the reader to use that gateway with prepaid metadata limits in its original
   ordinary acquisition budget.
4. When a selected theorem needs an import absent from configured suppliers,
   the reader requests holders by `(SemanticID, ExportID)`. Returned endpoint
   hints must satisfy local egress policy and expiry checks. The reader fetches
   the locator, then the exact evidence, and continues ordinary checking.

Neither a locator readback nor a DHT advertisement promises future retention.
The host must remain available independently. An empty bounded lookup is not
proof that no copy exists. Replication, independent hosting and useful search
coverage remain separate deployment responsibilities.

## Finite public launcher

The standalone operator package contains `run.py`, `operator_support.py`,
`operator.py`, pinned Python support, Node source and `SOURCES.json`. Its
`--profile-sha256` is the externally chosen SHA-256 of that exact SOURCES file.
The installed Python runtime is selected separately and must match those pins.
The Node runtime is the retained manifest-bound runtime closure; it is not
downloaded or installed automatically by the launcher.

Use Python 3.14.6 on Windows, with `-I -S -B`. The command is:

```text
python.exe -I -S -B run.py create|reopen
  --profile-sha256 HASH --python-runtime ABSOLUTE_PYTHON_DIRECTORY
  --node-runtime ABSOLUTE_PINNED_NODE_INSTALLATION
  --workspace ABSOLUTE_MUTABLE_WORKSPACE
  --config ABSOLUTE_OPERATION_JSON --config-sha256 HASH
  --output FRESH_OUTPUT_DIRECTORY --diagnostics FRESH_DIAGNOSTICS_DIRECTORY
  --wall-seconds N --cpu-seconds N --memory-mib N --active-processes N
  --stdout-bytes N --stderr-bytes N
```

All limits are required. They are ceilings, not work the service must consume.
The worker and Node descendant run in the existing Windows Job containment.
The wrapper reports its own CPU separately. Allow enough original wall time for
setup, the selected service interval and cleanup; a service interval cannot use
the final ten seconds reserved for closure. Process limits are not a hostile
source sandbox. This operator never executes remote mathematical source.

Source, Python and Node installations must be protected, disjoint from the
mutable workspace. State, output and diagnostics are distinct descendants of
that workspace. Input bundles/configuration/TLS keys may not overlap writable
state or output. New state uses `create`. Use `reopen` only with the identical
persisted Node configuration and retained state; the outer operation may select
new publication/withdrawal work. A reopen is a new explicitly funded service
interval, not a renewal of an expired reader's budget.

## Operation configuration

The exact outer fields are `schema`, `node`, `gateway`, `publication` and
`withdraw_exports`. Schema is `DMKN_ORDINARY_EXPORT_OPERATOR_OPERATION_V1`.
`node` follows the exact role/transport/metadata schema in `WIRE-CONTRACT.md`.
Its fixed semantic ID must match the ordinary software. Configurations have an
external content hash; no field selects arbitrary code.

For a custodian, `gateway` is null, and `node.endpoints` contains one approved
ordinary host endpoint. `publication` is null or an object with exactly:

- `bundle_directory`: absolute directory containing manifest-derived unit paths.
- `manifest`: `{path, sha256}` for the selected new baseline bundle manifest.
- `selected_export_ids`: null for all outputs, or a nonempty explicit subset.
- `requests`, `reply_bytes`, `attempt_timeout_ms`: finite own-locator read limits.

`withdraw_exports` is a distinct list of export IDs, possibly empty. Withdrawals
run before publications. Partial success is preserved: a later failure does not
undo completed changes. No remote registration or write API is provided.

For a gateway, `publication` is null, `withdraw_exports` is empty, and
`node.endpoints` is empty. `gateway` has exactly `listener`, `limits`, `provider`.
The listener has `host`, `port`, `tls`; TLS is null or `{cert_file, key_file}`.
Remote HTTP listeners require TLS. Provider fields are `max_connections`,
`max_requests`, `max_reply_bytes`, `operation_ms`. Gateway limits are `requests`,
`reply_bytes`, `descriptors`, `event_cap`, `max_providers`, `max_descriptors`,
`max_bytes`, `max_age_ms`, `operation_ms`. Requests cannot enlarge these grants.

## Outcomes and operational boundaries

`READY.json` identifies the started role and optional HTTP endpoint. It does not
assert a connected DHT, remote replication, mathematical acceptance or retention.
The service ends at its original horizon. Shutdown closes HTTP admission before
Node status/stop and owned pipe/process cleanup. `RESULT.json` is the worker's
report; diagnostics `RUN.json` additionally requires successful supervision and
all descendant processes closed. Preserve partial results on failure and inspect
them before deliberately selecting any new operation.

Current scope deliberately separates the gateway from publication. The retained
DHT skips its own peer when locating providers. A combined self-locating operator
is not supported. Gateway concurrency fails fast with BUSY; it has no unbounded
request queue. Exhaustion and expiry have explicit bounded unavailable replies.
Malformed, unauthenticated or uncertain backend outcomes terminate admission;
they are never presented as a trustworthy empty search result.

The advertised-key ceiling bounds charged publications. Startup/reopen performs
a bounded census; each publish reserves capacity before effects, and ambiguous
failure retains the charge. Capacity is released only after confirmed local
revocation. Remote stale hints may persist. See the wire contract and reviewed
backend invariant for these boundaries.
