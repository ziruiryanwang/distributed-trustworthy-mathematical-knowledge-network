# One portable build of the current ordinary commons

2026-10-28. Source/data inspection only. No compiler, package assembly, product
import, owner/database operation, network operation or Git mutation occurred.
Root owns implementation selection and execution. This plan does not authorize a
build or change any frozen predecessor.

**Recommendation: one fresh flattened builder/source-map successor, followed by
a source-bundle successor.** Reuse the existing compiler workers, installer,
supervision and archive rules. Do not distribute the research overlay chain.

## The actual gap

The current source archive contains the older bounded-operations builder plus
the fair-search overlay. Its fixed 84-input map cannot produce the current
`frontier-launcher-package01` behavior. Later kernel/frontier builders and
assemblers deliberately name canonical experiment packages and old binary
receipts. Adding their source files to the archive would not make them portable.

The current binary target is:

`experiments/v5-local-checks/frontier-launcher-package01/distribution/package`

- PROFILE: `efa1e0894a24859bf1c7648ccaf72674c7cf136c9fce32a62020e75cb24bcd45`
- ASSEMBLY: `d3b2ccc6f3cad7dcf5ebae1852840c6238cf555b1340de7797e910bb6b01ecf0`
- 154 payload files; 117 PROFILE auxiliary entries; eight package documents.

I matched each of its **72 directly copied source/document payloads** against
canonical source by actual byte length and SHA-256. Every one has an exact source
match. Relative to `ordinary_bounded_operations/source-map.json`, there are
**40 unchanged mappings, 24 replacements and eight additions**. No missing source
requires reverse engineering a binary or copying historical state.

## Exact direct-copy delta

All source paths below are relative to `software/v5/`. Keep the other 40 mappings
from the bounded-operations map unchanged. Pin complete bytes, not this table's
path spelling alone, in the new generated source map.

| Package target | Selected source | Change |
|---|---|---|
| `BOUNDED-TRANSPORT.md` | `ordinary_transport_release/README.md` | Add |
| `CONTACTS.md` | `ordinary_contact_federation/CONTACTS.md` | Add |
| `EXECUTION-TRUST.md` | `ordinary_bounded_transport/EXECUTION-TRUST.md` | Add |
| `SPARSE-SEARCH.md` | `ordinary_sparse_access/SPARSE-SEARCH.md` | Add |
| `LAUNCHER.md` | `ordinary_demand_frontier/launcher_integration/LAUNCHER.md` | Replace |
| `README.md` | `ordinary_sparse_access/README.md` | Replace |
| `authoring/py/anchor_store.py` | `ordinary_exact_module/anchor_store.py` | Replace |
| `authoring/py/module_export.py` | `ordinary_exact_module/module_export.py` | Replace |
| `authoring/py/ordinary_contribution.py` | `ordinary_demand_frontier/ordinary_contribution.py` | Replace |
| `authoring/py/portable_owner_request.py` | `ordinary_demand_frontier/portable_owner_request.py` | Replace |
| `authoring/py/retained_preparation.py` | `ordinary_demand_frontier/retained_preparation.py` | Replace |
| `installation/lean-src/CheckedExtension.lean` | `ordinary_kernel_admission/CheckedExtension.lean` | Replace |
| `installation/lean-src/LocalSnapshot.lean` | `ordinary_kernel_admission/LocalSnapshot.lean` | Replace |
| `installation/lean-src/OrdinaryWorkflowWorker.lean` | `ordinary_kernel_admission/OrdinaryWorkflowWorker.lean` | Replace |
| `installation/py/ordinary_admission.py` | `ordinary_parse_reuse/ordinary_admission.py` | Replace |
| `module/OrdinaryModule.lean` | `ordinary_exact_module/OrdinaryModule.lean` | Replace |
| `owner.py` | `ordinary_demand_frontier/owner.py` | Replace |
| `peer.py` | `ordinary_sparse_access/peer.py` | Replace |
| `peer_api.py` | `ordinary_multi_source/peer_api.py` | Replace |
| `profile.py` | `ordinary_sparse_access/profile.py` | Replace |
| `reference/baseline_bundle.py` | `ordinary_binding_reuse/baseline_bundle.py` | Replace |
| `reference/baseline_intake.py` | `ordinary_intake_progress/baseline_intake.py` | Replace |
| `run.py` | `ordinary_demand_frontier/run_frontier.py` | Replace |
| `support/discovery/candidate_query.py` | `ordinary_sparse_access/candidate_query.py` | Replace |
| `support/discovery/discovery_store.py` | `ordinary_sparse_access/discovery_store.py` | Replace |
| `support/discovery/fair_search.py` | `ordinary_sparse_access/fair_search.py` | Add |
| `support/discovery/pair_access.py` | `ordinary_sparse_access/pair_access.py` | Add |
| `support/discovery/search_session.py` | `ordinary_sparse_access/search_session.py` | Replace |
| `support/transport/contact_directory.py` | `ordinary_contact_federation/contact_directory.py` | Add |
| `support/transport/fair_exchange.py` | `ordinary_sparse_access/fair_exchange.py` | Add |
| `support/transport/http_provider.py` | `ordinary_multi_source/http_provider.py` | Replace |
| `support/transport/ordinary_acquisition.py` | `ordinary_multi_source/ordinary_acquisition.py` | Replace |

## Build lanes: preserve the distinctions

Keep the four existing lane shapes and order: eight receiver modules, thirteen
authoring helpers, seven native-exporter modules producing two executables, and
one query helper. Preserve the four public-header transforms and the one
exporter legacy-header transform, including their exact transformed hashes.

- Receiver: select the three `ordinary_kernel_admission` sources shown above.
  The other five receiver source selections remain unchanged.
- Authoring: select `ordinary_demand_frontier/OwnerConstruction.lean` and
  `ordinary_demand_frontier/PortableOwnerConstructCommand.lean`. The other eleven
  source selections remain unchanged. Its two downstream export helpers must
  compile against these new helper objects, despite their unchanged source.
- **Authoring and extractor CheckedExtension remain the old
  `ordinary_lean/CheckedExtension.lean`.** The new receiver implementation is
  deliberately a different source. Do not flatten these distinct roles into one
  filename selection shared by all lanes.
- Native exporter and query source selections are otherwise unchanged. Keep
  separate object directories so one lane cannot resolve another's same-named
  module by accident.

The direct copies, all selected lane sources, existing
`ordinary_lean/ordinary_installation.py` and existing `ordinary_package/build.py`
form an exact **87-file existing-source union / 2,933,782 bytes**. This count
excludes the proposed new builder/map, bundle utility/guide and optional operator
materials. No `experiments/`, native binary, old package or owner state is in
that union. The new source map should derive its complete pin table from this
union; unused historical `base_inputs` are not required.

## Smallest sustainable controller change

Create a fresh successor, for example `ordinary_current_distribution/`; leave
`ordinary_bounded_operations/` and its source bundle frozen. Start with the
bounded builder's path validation, staging, runtime pins, budgets, extractor and
query workers, exact copying and final verification.

Replace only its old `BASE_BUILD` dependency on `ordinary_package.build()` with
explicit staged receiver/authoring lanes selected by the new map. The preserved
`ordinary_package/build.py --compile-worker` already accepts those four lane
directories and the selected Lean executable. Its module tuples match the
required eight/thirteen modules. It can compile their staged bytes without
calling its obsolete top-level `build()` or consuming its historical
`SOURCE_FILES` list. Reuse its file/path helpers and `public_source` transform.

After those objects exist, assemble the installation from the exact selected
core, receiver sources/objects, foundation and supervision files using the
existing `ordinary_installation.assemble` and support-group construction. Then
compile exporters/query and directly assemble the final package. There is no
need for intermediate old package copies or fair/sparse/kernel/frontier overlay
executions.

Stage the six selected core Python modules together and check their loaded paths
before importing the installer. In particular, its imported
`ordinary_admission` must be the selected parse-reuse successor. The installer
uses ordinary sibling imports; executing it from its original source directory
without explicit selected staging/preloading could silently use an older core.
Preserve the kernel assembler's exact core object/path consistency checks.

The final census is fixed:

`72 direct + 8 receiver objects + 65 authoring parts + 5 query parts + 2 executables
+ 1 installation manifest + 1 PROFILE = 154 files`.

There are 19 installed direct copies, eight documents and 45 direct auxiliary
copies. Generated auxiliary artifacts add 72, giving 117 PROFILE entries. All
metadata is derived from actual selected outputs. Do not require historical
compiled hashes or force historical installation/implementation IDs: relocation
or recompilation can produce different binary bytes and hence a new named
implementation. This build is for fresh adoption, not silent migration of owners.

## Source archive and operator route

Create a fresh successor of the existing `ordinary_source_bundle/bundle.py` and
its guide. Replace its old map/builder pins and 18-entry additions list with the
new exact source closure; retain bounded allowlisted packing, exact census,
deterministic ZIP metadata, external receipt and relocation verification. Update
fixed counts deliberately. The archive entrypoint is the flattened builder;
remove the obsolete mandatory fair-overlay step.

**The old operator kit is not compatible with this package.** Its
`prepare_selected.py::known_layout` accepts only old ordinary/fair auxiliary
maps (41/43 direct entries); current PROFILE has 45. Merely supplying a new
PROFILE hash still yields `SELECT_UNKNOWN_INTERFACE`. The kit also has no
`contribute` request builder, so an updated compatibility map alone would not
cover frontier authoring.

For the smallest complete build handoff, document direct current `run.py`
arguments, include the current frontier API guide as source documentation, and
omit the old kit from the advertised current entrypoints. Manual inert JSON
configuration is already supported by the current product. If root selects
operator preparation work later, make one explicit successor with the 45-entry
current map and current contribution/report schemas; do not relax known-layout
checking or advertise an unchanged old kit as compatible.

Keep external Windows x86-64 Python 3.14.6 / Lean 4.34.0, local unpublished status
and undecided license explicit. This integration does not establish other OS
support, independent hosting, hostile-source isolation or mathematical speedup.

## Minimal evidence, in order

1. File-only exact map/closure check: all 72 direct bytes equal the selected
   candidate, all lane sources/transforms resolve inside the new source union,
   and no experiment/binary/old-state reference is a required input.
2. Native-free controller checks focused on the changed boundary: separate
   receiver/authoring CheckedExtension selection, exact transformed source
   staging, installed core import identity, 154/117/8 output-role census,
   unchanged aggregate accounting and refusal of source/map mismatches. Do not
   rerun historical semantic/control suites merely because files were copied.
3. One file-only pack and relocated verification with the new counts/entrypoint;
   recheck changed-manifest/missing-input/extra-file refusals. Existing path/ZIP
   safety rules have retained evidence and need fresh testing only if changed.
4. Later, if root selects a build claim, one actual fresh build from that
   extracted source with separately supplied runtimes. A source audit cannot
   honestly replace this new controller composition check. Compare source-role
   identities and receipt bindings, not promised bit-reproducible binaries;
   use one small fresh public init/contribution acceptance if its new support
   identity needs operational qualification. Do not replay rich Std grounding,
   old network campaigns or certificate work just to qualify packaging.

The independent rich-recipient user flow remains the immediate critical path.
This integration can proceed source-only in parallel, but it supplies portable
construction rather than evidence of accelerated mathematical discovery.
