# Source-only rehost closure: no Lean installation is needed in principle

2026-10-26. Source/data inspection only: no imports, runtime, network, database,
experiment or product edits. Supplemental to INERT-REHOST-PATH; implementation
is not selected. Answer: **yes, a small explicit pure-file manifest plus a new
fixed-action companion suffices; every reused file already exists in the current
investigator source extraction.** A native build or fabricated native installation
descriptor is unnecessary. The companion/standalone binding route is not shipped.

## Exact source identity and map

`D/` is `experiments/v5-local-checks/investigator-source-controls01/suite/relocated/`;
`S/` below means `D/software/v5/`. Current investigator manifest SHA-256:
`65edf28f928d4100346a4603fe508252ddc6393950c34a373fbb33da4c6491f5`.
The map below was joined by exact length/hash to the selected package PROFILE
`bde63019d1a6ac2bccd8e0c245a405ad3ca551d0606c01a5193fee6897c60346`
and its installation manifest, then all 27 source/data files were independently
length/hash checked on disk. Total: **1,212,995 bytes**, including the 823,690-byte
inventory. This is a file identity result, not executed compatibility evidence.

| Runtime module/role | Existing source relative to S/ |
|---|---|
| `ordinary_evidence` | `ordinary_lean/ordinary_evidence.py` |
| `ordinary_semantics` | `ordinary_lean/ordinary_semantics.py` |
| `portable_evidence` | `ordinary_lean/portable_evidence.py` |
| `portable_candidate` | `ordinary_lean/portable_candidate.py` |
| `ordinary_preview` | `ordinary_lean/ordinary_preview.py` |
| `portable_preview` | `ordinary_lean/portable_preview.py` |
| `formal_query` | `ordinary_formal_query/formal_query.py` |
| `baseline_bundle` | `ordinary_baseline/baseline_bundle.py` |
| `discovery.formal_features` | `discovery/formal_features.py` |
| `discovery.authenticated_index` | `discovery/authenticated_index.py` |
| `discovery.pair_access` | `ordinary_sparse_access/pair_access.py` |
| `discovery.discovery_store` | `ordinary_sparse_access/discovery_store.py` |
| `discovery.discovery_query` | `discovery/discovery_query.py` |
| `discovery.candidate_query` | `ordinary_sparse_access/candidate_query.py` |
| `discovery.summary_wire` | `discovery/summary_wire.py` |
| `discovery.ordinary_export_adapter` | `ordinary_formal_query/discovery/ordinary_export_adapter.py` |
| `custody.module_store` | `custody/module_store.py` |
| `transport.http_provider` | `ordinary_bounded_transport/http_provider.py` |
| `transport.clients` | `transport/clients.py` |
| `transport.ordinary_acquisition` | `ordinary_authoring_offers/ordinary_acquisition.py` |
| `transport.authoring_offers` | `ordinary_authoring_offers/authoring_offers.py` |
| `transport.contact_directory` | `ordinary_contact_federation/contact_directory.py` |
| Pinned launcher utility, not CLI execution | `ordinary_contact_federation/run.py` |
| Supervisor module | `ordinary_package/supervisor/commons.py` |
| `domains` module | `ordinary_package/supervisor/domains.py` |
| Job module | `ordinary_package/supervisor/run_stage.py` |
| Fixed-basis inventory data | `D/software/assets/foundation/seed-inventory-json.json` (outside S/) |

The 22 library modules are a role-specific closure, not all investigator modules.
No `ordinary_admission`, local/portable catalog, baseline_intake, owner, peer_api,
profile, module worker, Lean helper, `.olean`, compiler or certificate is needed.
Do not select similarly named historical files: three discovery and two transport
roles deliberately map to successor directories, as the exact hashes establish.
No source directory is authoritative merely because its name looks appropriate.

## Transitive and lazy imports that the loader must preserve

Load pure codecs in dependency order: evidence -> semantics -> portable evidence
-> candidate and ordinary preview -> portable preview -> formal_query/bundle.
The adapter needs the same exact module objects, not duplicate codec instances:
its limits and store dispatch enforce exact Python class identity.

Discovery order can be features -> authenticated_index -> pair_access/store
-> query -> candidate/summary -> adapter, after codecs. Then custody.module_store,
Provider -> clients -> ordinary_acquisition, plus the two optional-role modules.
These are approved source loads, not peer-selected imports. Namespace packages
`discovery`, `transport`, `custody` must be explicitly controlled; preloading the
listed qualified modules with empty package search paths avoids accidental import
of same-named older files or unselected siblings. This requires a small explicit
loader adaptation; blindly prepending all source directories is not equivalent.

`ordinary_acquisition` imports clients, and clients imports custody.module_store
at module load even though no ModuleStore instance is needed. Provider lazily
imports candidate_query for sparse queries, authoring_offers/contact_directory
for their routes *before* checking whether those optional roles are served.
Include both optional pure modules so ordinary refusal preserves current behavior;
leave those roles unset. Store imports pair_access even when access pairs are off.
formal_features lazily imports the ordinary adapter for V3 preview records.

The V4 body-profile branch mentions ordinary_body_adapter, absent from the actual
selected package. It is outside this closure: fresh index insertion uses only the
fixed ordinary V3 adapter, and remote APIs cannot insert records. The companion
must not accept a caller-selected adapter/schema or preexisting arbitrary index.
Likewise fair_search, search_session and fair_exchange are client orchestration,
not reached by this provider-only role. Adding those roles needs a new selection.

## Reuse the existing supervisor without the native package loader

Best reusable pattern is selected-export's bounded source bootstrap and fixed
parent/worker operation, **not its existing `setup()` verbatim**: setup still calls
`run.bind_support`, which requires package PROFILE/INSTALLATION metadata. Replace
only that binding edge with the explicit standalone manifest. Do not synthesize
native descriptors to fool bind_support, and do not call `profile.load`.

The new wrapper independently pins itself, manifest and selected Python runtime;
pins/reads the frozen run.py utility; then uses its `ordinary`, `read`,
`bound_file`, `load_source` and `operational_result` helpers. Its own finite source
manifest maps all roles above to exact paths/bytes/hashes. It constructs the
validated `support` map for `run.load_supervision` from the three supervisor files.
That function loads commons, then domains, then run_stage and returns Job.
This map is a supervisor-source selection, not an implementation/mathematics claim.

`commons.supervise(argv, cwd, evidence, limits, Job, started=original_start)`
requires no Release object, native profile or Lean path. `run_stage.Job` uses only
Windows ctypes/OS APIs. Its module imports domains, but no Domains constructor,
`execute()` or stage-plan parser is invoked by this route. Reuse selected-export's
approved child-environment override for the explicit Python root/DLLs. Use one
worker running its own finite Provider lease; leave supervise's `serve_seconds`
unset, since that option sends a different predecessor stdin stop protocol.

External prerequisites remain approved Windows x86-64 and Python 3.14.6 with its
stdlib/SQLite/TLS dependencies; Python runtime selection is independent of Lean.
Pin the selected python.exe/python314.dll/python3.dll as the current launcher does,
and state that this is not a hermetic runtime attestation. Jobs bound resources,
not filesystem/network privileges. Stable operator-controlled source paths remain
a premise; protect paths and reject preload/import collisions before execution.

## Smallest new integration surface

One companion entry/worker with an explicit pure-source manifest and guide:
load this closure, validate existing baseline bundles and structural closure,
prepare fresh unchanged custody/index stores, then serve only a finite approved
lease. Reuse existing wire/data formats, Provider cleanup, quotas and Job logic.
Preserve all output/failure evidence; no automatic retry, copying of live DBs,
native package build, daemon, grant or CHECKED result. A source-only maintainer
map may use the current D extraction directly; a recipient need not own P at all.

The new loader and preparation/lifecycle composition need targeted source review
and later bounded changed-boundary tests if selected. This source argument removes
the native-installation prerequisite in principle; it does not declare that new
public route already implemented or qualified.
