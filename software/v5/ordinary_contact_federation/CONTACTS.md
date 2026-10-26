# Finding an unfamiliar specialist provider

This optional layer fills one gap: knowing a few directory contacts can now be
enough to learn a specialist index endpoint. The usual `find` still works with
explicit providers. The directory neither checks mathematics nor assigns research
tasks. A directory may be incomplete, stale, mistaken or malicious; returned
mathematics still needs the existing independent ordinary acceptance procedure.

No designated central server, inbound listener, Node runtime, DHT or certificate
production is required on the reader. Directory operators run finite read-only
services with locally approved registrations. A future DHT backend is optional
and is **not implemented by this layer**. Someone still has to maintain useful
registrations and give new participants an initial contact.

## Two public operations

Use the package's existing bounded `run.py ... peer` entry and an explicitly
selected new PROFILE. `directory-find` and `directory-serve` both reject catalogue,
custody and store arguments: they open no mathematical owner state. They still
use the package's approved Windows/Python/Lean runtime profile, but invoke no
Lean compiler or checker. The existing runtime dependency is not removed here.

For either operation, supply the same required configuration hash, fresh output,
runtime paths and original wall/CPU/memory/process/log limits as in LAUNCHER.md.
Example command shape (replace every placeholder with the local approved value):

```powershell
& 'D:\Python314\python.exe' -I -S -B 'C:\commons\package\run.py' `
  --profile-sha256 'SELECTED_NEW_PROFILE_SHA256' `
  --python-runtime 'D:\Python314' --lean-runtime 'C:\tools\lean-4.34.0-windows' `
  --diagnostics 'C:\runs\find-diagnostics-01' `
  --wall-seconds 90 --cpu-seconds 45 --memory-mib 512 --active-processes 3 `
  --stdout-bytes 1048576 --stderr-bytes 1048576 `
  peer directory-find --config 'C:\config\directory-find.json' `
  --config-sha256 'SELECTED_CONFIG_SHA256' --output 'C:\runs\find-result-01'
```

The diagnostic/output leaves must not exist, and their parents must exist. Do
not use the predecessor operator-kit compatibility wrapper for this new PROFILE:
it does not select these added operations. Use the explicit public command until
a later, separately reviewed kit supports this exact layout.

## Directory registration

`directory-serve` configuration has exactly these fields:

```json
{
  "entries": [
    {
      "specs": [{"tag": "declaration-kind", "value": "theorem"}],
      "endpoints": [
        {"host": "127.0.0.1", "port": 18443, "tls": false, "server_name": null}
      ]
    }
  ],
  "host": "127.0.0.1", "port": 18080, "tls": null,
  "lease_seconds": 30, "cleanup_seconds": 10,
  "limits": {
    "max_connections": 2, "max_requests": 64,
    "max_reply_bytes": 1048576, "operation_ms": 1000
  }
}
```

This is a **loopback configuration example**, not a live service or public
deployment. Port 18443 represents a separately running ordinary index provider;
the directory does not start it. Remote directory serving requires the existing
locally pinned certificate/key `tls` fields from the standard serve API. Remote
specialist hints must use public numeric IPv4, HTTPS and a certificate valid for
the given server_name (or literal address); hints never contain a CA file.

The service compiles specs into the exact namespace of its selected ordinary
semantics. One entry is an exact route predicate, not an assertion that its
provider contains every matching result. Up to 2048 distinct keys, 16 endpoints
per key and a 2 MiB registration map are permitted. There is no remote write or
recursive directory registration API. For an update, approve a new finite
configuration/operation; there is no hidden renewal daemon.

## Reader configuration

```json
{
  "contacts": {
    "community": {
      "host": "127.0.0.1", "port": 18080, "tls": false,
      "server_name": null, "ca_file": null, "ca_sha256": null
    }
  },
  "directories": ["community"],
  "specs": [{"tag": "declaration-kind", "value": "theorem"}],
  "routes": [[{"tag": "declaration-kind", "value": "theorem"}]],
  "egress": {
    "schema": "DMKN_V5_OWNER_EGRESS_V1", "mode": "loopback-test",
    "public_ports": [], "test_endpoints": [{"host": "127.0.0.1", "port": 18443}]
  },
  "directory": {
    "requests": 1, "reply_bytes": 32768, "max_contacts": 4,
    "max_bytes": 32768, "max_age_ms": 30000, "attempt_timeout_ms": 2000
  },
  "search": {
    "limits": {
      "providers": 4, "snapshots": 8, "requests": 12, "pages": 8,
      "examined": 64, "candidates": 8, "bytes": 1048576,
      "wall_ms": 20000, "inflight": 1
    },
    "offer": {"max_bytes": 65536, "max_expanded_bytes": 65536, "max_age_ms": 20000},
    "page": {
      "scanned": 8, "matches": 4, "bytes": 65536, "timeout_ms": 500,
      "record_probes": 256, "node_reads": 2048, "hash_calls": 4096,
      "sql_vm_steps": 100000
    }
  }
}
```

Public readers use `mode: "public-ipv4"`, an explicit sorted public_ports list
(normally `[443]`), and empty test_endpoints. That is a deliberate permission to
try unknown public HTTPS servers on those ports. It is not permission to access
private/link-local services, follow redirects, resolve destination DNS, use IPv6,
install a CA or execute source. Explicit bootstrap-directory trust settings do
not propagate to suggestions. Environment-specific routing/firewall restrictions
remain an operator responsibility; numerical IP classification is not a network
isolation mechanism. Queries also disclose their selected features to directories.

The example's broad theorem-kind route is useful for understanding the interface,
not a scale recommendation. Real specialists should agree on selective known
symbol/structural route predicates. Each requested route must be a subset of the
full query; an exact registration must exist at a queried directory. No automatic
synonym expansion, unfamiliar-vocabulary discovery or global coverage follows.

## Budget, lifetime and output meaning

Choose at most eight directories and eight routes, with product at most 32.
Directory requests/reply bytes and the existing search allowance fit one original
aggregate grant. Failed lookups keep their reserved costs; duplicates and empty
answers do not buy another attempt. Search is issued at most once, never once
per returned endpoint. TCP/TLS framing and provider maintenance are additional
costs, not part of a reported reply-body byte count.

Each hint gets an owner-monotonic horizon beginning when its directory request
starts, capped by max_age_ms and the original deadline. Slow replies do not
extend it. Duplicate suggestions do not refresh it. The whole search is narrowed
to the earliest retained horizon: conservative and simple, but an early short
lease can reduce progress on other contacts. This is permission to try a hint
briefly, not proof that a provider is alive or the map was recently updated.

Inspect result status, directory outcomes/truncation, search matches/errors and
original budget accounting. Successful transport does not mean mathematical
acceptance, complete coverage or even that a useful result exists. No contacts,
timeouts and exhausted budgets are incomplete outcomes, not mathematical negatives.
Learned contacts in a report are advisory diagnostics; a later independently
authorized operation must explicitly approve its own endpoints and limits.

This layer does not cure large nonselective posting lists, authenticate index
construction, supply missing proof semantics, guarantee persistent custody,
prove useful growth or qualify the complete public v5 release. It closes one
specific end-to-end discovery gap with no change to the mathematical trust base.
