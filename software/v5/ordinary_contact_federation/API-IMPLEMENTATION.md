# Ordinary directory API successor: source checkpoint

Owner: `search_locality_argument`, 2026-10-25. Source authored under the selected
CONTRACT; no product import, Python execution, socket, test or native build run.
Independent test/source review and root adoption remain required. Full v5 and
useful-growth/global-discovery claims remain unfinished.

`peer_api.py` starts from the exact selected fair ordinary package's peer API.
Before independent review, a read-only normalized-line-ending text comparison
confirmed the old `find`-to-end tail was unchanged. Review then identified a
relative-timeout entry-drift risk. Root explicitly selected one additional
`find` change: create its SearchSession, narrow its absolute deadline to the
original ledger deadline, then construct FairSearch. All other original function
bodies remain unchanged. New imports/constants and three definitions before
`find` supply the directory compositions. No predecessor file was modified.

## Interfaces

```python
await directory_find(loaded, config, allowance, *, network_budget=None)
await directory_serve(loaded, config, allowance, *, ready=None)
```

`directory_find` config has exactly:

```text
contacts    existing owner contact map, including any locally pinned seed CAs
directories unique selected contact labels, 1..8
specs       full ordinary formal query, existing 1..8-spec rules
routes      1..8 lists of ordinary specs; unique compiled keys, subset of query
directory   {requests,reply_bytes,max_contacts,max_bytes,max_age_ms,attempt_timeout_ms}
egress      explicit OwnerEgressPolicy config
search      {limits,offer,page}, unchanged ordinary search schemas
```

`directory` bounds: requests 1..32; reply_bytes 1..1 MiB; max_contacts 1..64;
max_bytes 1024..32768; max_age_ms 1..60000; attempt_timeout_ms 1..5000.
reply_bytes must fund at least one max_bytes reply. Number of selected directory
and route pairs is at most 32. Pairs are visited route-major so all seeds are
offered the first route before any seed's second route. Each request/response
contains only exact namespace/features/nonce and bounded contact metadata.

`directory_serve` config has exactly:

```text
entries          1..2048 {specs,endpoints} records
host,port,tls     existing owner server binding/TLS shapes
lease_seconds    1..3600
cleanup_seconds  10..60, within original allowance
limits           existing PROVIDER_LIMITS
```

The directory compiles ordinary specs locally, constructs one immutable
`ContactMap` and starts `H.Provider(contact_directory=directory)` without
catalogue, custody or index. Input endpoint suggestions are inert registrations,
not authorized client egress. A served map is bounded to 2 MiB and exact keys;
there is no remote registration/write route or background renewal.

## One grant, not one grant per referral

Both slices are validated together against the original shared ledger's
remaining capacity before I/O. New outer ledgers contain the sum of the slices.
Directory work uses `charge_external('directory-find', ...)`, so the ordinary
ledger's fetch sequence stays zero. Existing `find` is then called at most once
with that SAME ledger and prepays its `peer-find` slice. External label/slot
checks occur before I/O to avoid a predictable late search-prepayment refusal.
Directory calls never use `begin/settle`, refund their prepayment or construct
one search session per contact. Acquisition under a composed future owner flow
must remain within its separately included original capacity.

Each directory attempt independently consumes one request and its full reply
reservation before transport. Actual payload/header counters are additional
observations, not budget refunds. Bad, duplicate, rejected, stale and truncated
responses retain charges. At most min(directory.max_contacts,
search.limits.providers) distinct endpoint tuples are adopted; all returned
entries remain bounded/charged even when deduplicated. This also avoids relying
on Endpoint.label alone, which omits TLS name, for distinct-contact limits.

The new root-owned `fair_exchange.py` allows the additional exact
`H.CONTACT_DIRECTORY_ROUTE` and an absolute deadline. The API passes the minimum
of its original attempt deadline and request-start contact horizon; root's
FairSearch successor propagates its original session deadline too. Transport
checks that absolute limit after local TLS setup immediately before connection.
The API uses that settled exchange, not the weaker
ordinary HTTP exchange. Uncertain cleanup, cancellation, local failures and
unclassified errors remain terminal. Only settled refusals and a pure bounded
directory-reply parse failure can move to the next planned lookup.

## Expiry and egress

The hint horizon starts before the directory request, not upon response arrival:
`until = min(original ledger deadline, request_start + owner max_age_ms)`.
Attempts reserve one second of cleanup; a horizon too short for a legal attempt
returns explicit incompleteness without a dial. Request setup time narrows the
already selected attempt deadline rather than restarting it.

Replies are accepted only before that horizon. Duplicate endpoint suggestions
cannot extend it: retained expiry is the minimum of observations. Expired
contacts are removed before search; among usable contacts the ledger deadline
narrows to the earliest original expiry. A private `_DirectorySearchAllowance`
then checks the owner allowance, that common horizon, immutable egress policy,
and every retained endpoint before the unchanged find's requests. FairSearch's
existing exact endpoint/session binding remains in force.

This is deliberately a conservative common-horizon design: one short-lived
contact can shorten the whole search. It is not a claim of per-contact scheduling
or guaranteed useful recall. A local monotonic lease is permission to try, not
proof of provider freshness. Cached report rows carry no persistent future dial
authority. Public mode is literal public IPv4/TLS/system roots/selected ports;
only explicit test mode allows its exact loopback endpoint list. Remote hints
cannot choose a CA path, new root, DNS resolution, redirect, arbitrary local path
or another directory tier.

## Reports and cleanup

`directory_find` returns top-level `matches`, the full unchanged ordinary find
report under `search` (or null), `learned_contacts`, bounded `lookups`, directory
charges, final outer `network` accounting, and explicit incomplete/false-acceptance
flags. `learned_contacts` contains contact hash, endpoint tuple and remaining
local milliseconds, labeled `ADVISORY_NOT_PERSISTENT_DIAL_AUTHORITY`. It is not an
owner configuration update. Unknown/unsupported namespace can return an empty
advisory list; it is not mathematical nonexistence. Truncation remains in both
attempt and aggregate directory reporting.

`directory_serve` reports namespace, immutable map hash, route/contact counts,
finite readiness and provider counters. It waits only through its original
lease, then attempts provider stop and quiescence verification. On cleanup error
it still closes the listener/cancels remaining tasks within the SAME reserve;
failure is retained. No owner mathematical state can be admitted or modified.

## Remaining review gates

Independent source review must check the same-ledger/prepay phase, coherent
new helper/HTTP/fair-exchange profile loading, rejected endpoints never dial,
short/expired hints, combined cap rejection before I/O, report bounds, and public
state-free directory dispatch. A prospective actual loopback test may discover
an unknown ordinary provider and fetch synthetic metadata. That would be new
composition evidence, not new verified mathematics, global scale or net growth.
