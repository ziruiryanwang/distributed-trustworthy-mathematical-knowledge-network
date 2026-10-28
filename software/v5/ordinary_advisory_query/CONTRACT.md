# Advisory name projection without proof-snapshot reads

Status: source-only selected successor; no execution, package adoption or measured
performance result. This directory's helper and contract are independently reviewed
before use. The existing symbol-query implementation and accepted evidence remain
unchanged. Root owns package/runtime selection; caller integration and independent
controls have separate owners.

## Scope and API

`advisory_context.project(installation, catalog_directory, store_id, local_root,
names, *, limits, check, catalog_module)` accepts the existing verified
NativeInstallation, exact catalog limits and already loaded `ordinary_admission.P`.
The caller verifies the helper's auxiliary-package pin before executing it. The
helper checks module identity against already loaded core modules; it does not load
or replace a catalog implementation or mutate global classes.

`names` is a list of one through eight distinct structured original names with at
most 65,536 canonical JSON bytes. The helper validates and detaches this request
before opening state. It resolves only exact name keys from the selected root.
Its detached return value has exactly these fields:

- `local_root`, `store_id`, `semantic_id`, `foundation_id`, `implementation_id`;
- `bindings`: requested names that exist, keyed by canonical name-key bytes;
- `missing_names`: all absent structured names in request order;
- `snapshot_integrity: NOT_CHECKED`, `context_readiness: NOT_ASSERTED`;
- `mathematical_acceptance: false`, `owner_closure: CLOSED`.

The caller must refuse a ready query if any name is missing; it cannot publish a
mapped subset. No module paths, loading plans, catalog handles, reader classes or
admission grants escape. Projection returns only after successful owner close;
an opening, validation, withdrawal, allowance or closure failure raises instead.
Caller integration retains finite whole-operation supervision and checks all
input/output/catalog/support separation and final publication conditions. The
helper independently checks catalog-versus-installation/runtime separation. It
opens no custody store, reads no evidence body and calls no native worker.

## Exact bypass boundary

The only policy change lives in a class local to `project`. It inherits unchanged
PortableCatalog metadata validation. The `_validate_record` wrapper constructs an
exact pending tuple `(generated_relative_path, declared_size, declared_sha256)`
only for native `operations/<hex>/chunk.olean` or imported
`imports/<hex>/<bounded-canonical-ordinal>/chunk.olean` records. It preserves the
original positive artifact-size bound and canonical hex digest validation.

The wrapper then invokes the original `_validate_record`. In the pinned source,
its final `_artifact` call follows all record, identity, native operation/import,
source-record, correspondence-name and generated-path checks. The override skips
bytes only while that pending tuple is active, only for an exact argument match,
and only when `maximum is None`. A mismatch refuses. The scope is cleared in a
`finally` block. The returned lexical path is used only internally by inherited
context assembly and is never marked verified or returned by this public API.

Outside this record scope `_artifact` delegates to its original implementation:
import `audit.json` is still size/hash checked. Import correspondence and original
source-record reads/hashes are unchanged. A future change to the pinned base's
call order or artifact roles requires renewed source review; this auxiliary helper
is not a generic skip-verification switch.

## Invariant and lifecycle

Let `B_R` be the original-name map obtained from valid owner-recorded metadata for
selected root `R` under the existing immutable-owner/no-rollback premises. On
successful projection, for every requested key `k`, exactly one holds: the result
contains `bindings[k] = B_R[k]`, or the corresponding name occurs in `missing_names`
because `k` is absent. Projection cannot change the stored root or symbol identity.

The argument reuses all inherited bounded record parsing, selected ancestry,
basis, parent module/source, duplicate/no-shadow, import digest/ordinal, marker,
store, semantic, implementation and activation checks. Snapshot bytes are not
inputs to those name-binding predicates. The actual-check commit and protected
local records remain their authority; native root IDs alone are not independent
authentication of the entire binding map. This helper adds no such assumption.

Inherited open retains exclusive owner locking, activation validation and existing
reservation recovery. Its eager imported-root `context` uses the same private
artifact policy, so it cannot hash snapshots before requested-root projection.
This retains database mutation for abandoned-reservation recovery and is not a
database-read-only promise. Create/importing and reserve/commit/import entrypoints
are disabled. Liveness/withdrawal checks run throughout inherited context access
and again before close; there is no durable authority claim after return.

Missing or corrupt `.olean` snapshots can therefore permit an advisory result.
That result asserts recorded-name fidelity, not a currently loadable context,
retained custody, a new theorem or acceptance of a provider candidate. Ordinary
admission and use retain the original snapshot-byte verification and native checks.
Damaged metadata, missing import-audit/source files, conflicting ancestry, changed
activation and known withdrawal remain refusals. Existing post-read immutability
and owner/OS trust premises are unchanged.

## Identity and cost

No installed core file, implementation descriptor, admission method, schema,
semantic interpretation, migration formula or stored root changes. The helper is
an auxiliary query-package role with its own pin. Changing portable_catalog.py
instead would change controller support/implementation identity and is outside
this selection. The caller must open this helper directly; OrdinaryAdmission.open
would perform its original snapshot validation before any projection optimization.

For metadata bytes `M`, names `N`, lineage depth `D` and requested input bytes `b`,
the inherited metadata/context work remains O(M + N + b), with O(D + N) supporting
structures and bounded database access. Import opening can repeat metadata work.
The helper reads zero proof-snapshot bytes; imported audit/correspondence/source
records are metadata and remain read. Existing package/runtime hash checks are
additional whole-operation costs. This is neither sparse constant-time lookup nor
a global-corpus replay claim, and no measured speedup is asserted.
