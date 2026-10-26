# Bounded proof-free search input from ordinary Lean syntax

2026-10-26. Root adopts the two POST-BUNDLE source/architecture decisions in the
current local-discovery cycle and selects this new, separate source companion.
All old sources, the verified workflow archive and installed packages stay frozen.
Full v5 remains active, local and unpublished. No runtime is selected here.

## Why this change

A new investigator has neither a pre-existing Lean project nor a hand-written
expression DAG. They should be able to ask a formal question without first proving
it or admitting a dummy theorem. The shipped native type-query command already
does this, but no shipped bounded public launcher can execute it. A short fixed
companion can reuse that command and existing supervision; no new elaborator,
query semantics, index, proof system or mathematical acceptance rule is needed.

First support only vocabulary in the selected fixed foundation inventory. Init
contains more than those 581 names: reject/report unknown references after native
extraction. Do not bind arbitrary project names to unrelated context symbols.
Use the existing semantic/foundation descriptors and `basis_symbol_id` to form
exact search bindings, then existing `formal_query` functions to emit QUERY and
SPECS. This is deterministic query interpretation, not a local warrant. It needs
no owner initialization, catalog, custody, peer, prior theorem or proof checking.

## Public interface and inputs

`query.py --config ABS --config-sha256 HEX --output FRESH_ABS --approve-local-query`

Config has exactly schema `DMKN_ORDINARY_BASIS_QUERY_V1`, package,
profile_sha256, python_runtime, lean_runtime, query `{path, sha256}`, and limits.
The separately pinned UTF-8 query JSON has exactly `universes` (ordered, distinct
simple identifier strings, at most 32) and `type` (nonempty Lean type-expression
text, at most 64 KiB). Reject duplicate JSON keys, booleans as numbers, unknown
fields, unsupported paths/aliases, overlaps and nonfresh outputs. No executable
path, raw argv, arbitrary imports or project-search-path option is exposed.

Generate a fresh local source containing only the fixed Init/OwnerQueryCommand
imports, declared universe parameters and the existing #ordinary_type_query
invocation with a safely quoted fixed fresh output path and the supplied term.
The term is explicitly owner-approved executable Lean syntax: macros/tactics or
command injection are not a sandboxed language. Do not advertise textual filtering
or resource Jobs as hostile-source isolation. Never execute downloaded source or
infer approval from a hash. The wrapper accepts no foreign project environment.

Limits explicitly bound the child tree's wall, inclusive CPU, private commitment,
active processes and logs using the unchanged installed supervisor/Job. Retain
the existing distinction between hard/sampled child limits and bounded trusted
wrapper work/CPU reported separately. No retry, renewed allowance or hidden
fallback. Small source/file caps and original operation deadlines also cover
bootstrap/finalization; report uncertainty/failure rather than successful output
when closure or final checks fail.

## Reuse and trust boundary

Use the actual default installed run.py interface from ordinary_contact_federation
(known source SHA 47a2b63c73f1bd8346c5881c6d6a76abac86d33aa8e55bfc19bf3359ea924a39),
not the older bounded-operations launcher. Verify bytes before importing it;
reuse bind_support/load_supervision and ordinary path/binding helpers where safe.
Do not mutate the launcher CLI or its operation allowlist. Parent launches only
this companion's fixed internal worker, not a generic caller-selected command.

Within the bounded worker, use the existing exact owner/profile loading path to
validate the selected full package, installation and runtime. It opens no owner
or custody and performs no native initialization. Execute exactly one Lean type
extraction with the already built OwnerQueryCommand/helper support, selected
runtime, sanitized environment and no inherited Lean/Python overrides. Validate
the inert AST with existing formal_query.read_native_type/reference_names.
Read the installation's pinned fixed inventory, refuse nonbasis references,
derive bindings using existing semantics.basis_symbol_id, and use the existing
bind_native_type/query_spec functions unchanged. No guessed portable IDs.

Keep one fixed output tree containing generated source, native artifacts/logs,
candidate query files and actual supervision/report evidence. Publish a terminal
successful marker only after clean child closure, exact input/support bindings,
finite final checks and coherent output hashes. An incomplete/failed directory
is not usable search input. Success means ready search hints, never mathematical
acceptance, corpus availability, usefulness, semantic completeness or growth.
The success report explicitly supplies the downstream specs file and interpretation.

## Owners and economical evidence

service_lifecycle owns query.py, README.md and IMPLEMENTATION.md here, source only.
cold_start_workflow owns test_query.py and TEST-PLAN.md: focused new boundary tests
and a proposed single real proof-free extraction, not existing query/key suites.
update_trust_lifecycle owns independent REVIEW.md after the archive outcome closes.
Root owns this contract, integration, exact selections, adoption and Git. Explicit
canonical root/workdir and assigned absolute paths apply to everyone.

No native helper build, owner initialization, source archive repack, theorem,
network, concept episode or broad regression campaign is justified. The only later
native check should test this new public wrapper's actual fixed invocation and
output delivery. Reuse existing native query and context/search evidence. Stop
this seam when an investigator can prepare supported formal search independently;
do not append richer-project recovery or another index feature.
