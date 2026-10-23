# Thin ordinary peer CLI: source implementation

2026-10-23. Agent `owner_cli`; source-only, no native/build/network/test/Git run.
Owned new files are `software/v5/ordinary_peer_package/peer.py` and `profile.py`.
`ordinary_api_flow` separately owns `peer_api.py`; root owns file-only assembly
and finite selections. Existing used ordinary_package source and installations
remain unchanged. Review/runtime adoption are separate from this implementation.

## Scope and public commands

This is the direct-contact peer surface from ORDINARY-PEER-SURFACE-PLAN, not a
new protocol or a new mathematical checker. The old `owner.py contribute` still
authors new local results. The new CLI only routes bounded owner configuration
to the coordinator API:

```text
<selected-python> -I -S -B <package>/peer.py <find|receive|publish|serve>
  --profile-sha256 <exact PROFILE.json hash>
  --python-runtime <absolute Python distribution root>
  --lean-runtime <absolute Lean distribution root>
  --config <absolute JSON file> --config-sha256 <exact config hash>
  --output <fresh absolute result directory>
  --wall-seconds <35..3600> --cpu-seconds <4..200000>
  --memory-mib <1..8192>
```

All operations except `find` additionally require explicit existing
`--catalog`, `--custody`, `--store-id`, and `--custody-limits` as in the old owner
entrypoint. `find` refuses these state arguments rather than opening an unused
mathematical owner. No command creates a basis, copies a store, compiles Lean
source, infers a latest parent or automatically retries an operation.

`find` returns candidates and bounded-search accounting, not mathematics or
global completeness. `receive` explicitly means acquire **and independently
check** through the existing native admission core. Inert acquisition alone is
the lower-level API. `publish` indexes exact selected warranted targets locally;
it is neither another mathematical check nor a remote write. `serve` is one
finite read-only network service over explicitly selected local stores.

## Shared API/configuration contract

The coordinator signatures agreed with its author are:

```text
await find(loaded, config, allowance)
await receive(loaded, owner, custody, config, allowance)
publish(loaded, owner, custody, config, allowance)
await serve(loaded, custody, config, allowance, ready=callback)
```

API-only composition may supply one existing `network_budget` to find/receive;
CLI commands are separate explicit owner grants and do not nest one another.
The coordinator owns mathematical input validation, bounded network ledgers,
contact/CA policies, native checking, index lifecycle and provider cleanup.
`PeerFailure.report` must retain partial outcomes, especially actual acceptance.
The CLI preserves that report rather than converting failure to rollback.

Configuration is bounded to 2 MiB, exact-hash-selected, parsed with duplicate
keys/nonfinite/floating numbers refused, and rechecked after successful use.
Ordinary JSON whitespace, booleans and nulls are allowed; lease/cleanup seconds
are therefore integers. The CLI does not print raw configuration or TLS keys.
The API validates exact fields/types and its operational limits:

| Command | Configuration fields |
|---|---|
| find | contacts, providers, specs, limits, offer, page |
| receive | contacts, selection, parent_root, limits |
| publish | index, context_root, targets, max_unit_bytes, max_total_bytes |
| serve | index, host, port, tls, lease_seconds, cleanup_seconds, limits, share_all_custody, exclusive |

Contacts are bounded label-to-endpoint records with literal host IP, port, tls,
server_name, ca_file and ca_sha256. Remote traffic requires verified TLS;
plaintext is loopback-only. A null CA pair explicitly chooses system trust.
Non-null selected CA bytes must match their hash through the API's checks.
Serve TLS selects certificate/key files and their hashes, not key contents.
Before/after hash checks assume immutable owner-controlled files; they do not
defeat an adversarial local race attacker or pin the system CA store.

`index` is `{path, limits, create}`. Only publish may explicitly create a fresh
index; serve requires an existing one. CLI validates index/output/catalog/custody
and package/runtime separation before opening state. Index paths cannot hide
under protected support or another selected state root. Index configuration and
failure persistence remain the existing Store's semantics.

Profile/configuration hash refusal precedes output creation and state opening.
Full operation-specific API schema validation occurs **after** `output.mkdir`
and, except for find, owner opening. Opening the existing owner may settle prior
RESERVED operations as INTERRUPTED. Therefore a malformed but correctly pinned
operation configuration is not promised to be free of local recovery effects;
this CLI preserves the ordinary owner's existing recovery semantics.

## Enforced ordinary-owner serialization for serve

Root selected stronger CLI serialization than merely trusting `exclusive:true`:
serve opens the same ordinary catalog and holds its existing owner lock until
the coordinator's provider/index cleanup finishes. Old `owner.py` mutations and
this CLI's receive/publish therefore cannot run concurrently through that same
catalog authority. The flag remains explicit authorization, not the lock itself.

The supported CLI requires an owner-associated custody. Independently rehosting
an inert-only custody without a mathematical catalog remains a lower-level API
capability whose caller must provide serialization; it is not implemented by
this first CLI. The lock does not cover arbitrary low-level users, unrelated
catalogs pointed at the same physical custody/index, hostile local file edits or
other applications. Owners must not alias those stores across catalog owners.

Serve requires both `share_all_custody:true` and `exclusive:true` before any store
opening. The sharing consent covers **every addressable object in that custody**,
not just selected/indexed/accepted results. Provider has no per-object ACL.
Opening/querying local stores may perform ordinary metadata/recovery writes;
"read-only service" describes its remote routes, not a read-only database open.

## Package/import boundary

The successor keeps `DMKN_ORDINARY_OWNER_PROFILE_V1` and its exact existing fields,
helper_paths and author_worker values. This is compatible with unchanged
owner.py. Only the loader's exact local payload allowlist expands:

- root peer.py and peer_api.py;
- support/discovery/ordinary_export_adapter.py;
- support/discovery/search_session.py;
- support/discovery/discovery_query.py;
- support/discovery/candidate_query.py.

The file-only successor retains every existing installation/native/helper byte;
new profile/code selection does not change the installation implementation ID.
No Lean rebuild or migration is necessary solely to add these public helpers.

The peer entry's stdlib bootstrap checks the supplied PROFILE hash and selected
peer.py/owner.py bytes before executing old owner helper code. That unchanged
bootstrap checks profile.py before loading it. The successor loader preserves
the prior pre-import auxiliary/core checks, complete search-path file censuses,
actual imported module identity checks and AuthoringProfile verification. It
then explicitly compiles/loads exact checked peer_api bytes (root scripts are not
added to sys.path). CLI requires peer_api.A to be the same installed core object.
No module import is allowed to initiate networking, state opening or native work.

Entrypoint, Python/OS, immutable owner storage and owner package selection remain
trust premises. Profile hashes select code; they do not authenticate an unknown
publisher. Runtime attachments still name selected files, not a hermetic runtime.

## Allowances, reporting and failure behavior

The unchanged owner Allowance is reused, with its clock anchors set to this peer
entry's original startup. Bootstrap, configuration, state opening, API phases,
cleanup and reporting share that original allowance. Subsequent native budgets
derive from its remainder; worker CPU is charged by the API exactly once.
The coordinator's network budget is separately finite in requests/reply bytes.

Controller limits are cooperative; native workers retain existing Windows Job
containment. Hard limits on the whole CLI/service require an outer Job/process
supervisor. Memory-mib is not a controller RSS cap. No daemon or lease renewal is
created by this CLI. The original grant still controls cleanup/report formation;
exhaustion produces failure without deleting state or disguising earlier acceptance.

Serve readiness is saved once as `<output>/READY.json`; it contains the actual
endpoint and scope, not a private key. A terminal `<output>/RESULT.json` and stdout
report preserve success/failure, exact selection hashes, partial API report and
costs. The report ceiling is 16 MiB. Oversized reporting becomes an explicit
failure retaining known admission data; accepted local state is never rolled
back. Both owner and custody closes are attempted even if one fails; cleanup or
final-budget failures make the command unsuccessful. Early invalid-profile
failures create no output/state. Native and outer CPU reports must not be summed
twice, and controller cost is sampled before final JSON/file output overhead.

The terminal-report fallback reads both the coordinator's `admission` field and
the older `accepted` spelling. It therefore retains the checked/reused status and
local root even if a `PeerFailure` is followed by another reporting-budget error.
For partially completed publication it retains at most 64 committed record and
snapshot identities, without carrying large discovery records into the fallback.

The next evidence is the independently reviewed, root-selected installed peer
boundary. This source implementation alone demonstrates no networking, accepted
knowledge, net resource advantage, independent-host deployment or final v5.
