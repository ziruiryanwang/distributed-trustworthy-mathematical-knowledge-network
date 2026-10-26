# Selective inert export: integration choice

2026-10-26. Source-only decision challenge; no implementation, product import,
state access or execution. This note addresses public integration and cost;
separate assignments own closure correctness and alternative existing workflows.

## Recommendation

If the parallel route audit confirms the missing public capability, implement a
small **separately approved, supervised export companion**, not a new native
package overlay. It may safely load the unchanged selected package, take the
existing owner lock, and emit the already supported inert baseline format.
It does not need to alter `owner.py`, `run.py`, `profile.py`, the installation,
peer protocol or native checker. Preserve the default package and its anchors.

The concrete benefit is selective offline replication from an existing checked
owner, without requiring its producer project or disclosing all mixed custody.
The resulting bundle feeds existing `owner intake-baseline`, then ordinary
publication/finite serving in a separate owner. The receiver still independently
checks the full selected proof closure; this is not a certificate substitute,
free cold verification, automatic replication or proof of useful growth.

Do not implement a separate live-serving subsystem, scheduler, migration,
compressed-proof format or automatic recipient operation for this capability.

## Why not simply add an owner operation?

The default launcher is `ordinary_contact_federation/run.py`, not the earlier
bounded-operations source. Its fixed owner operation list at 25-29 does not
include export-bundle. Loading a helper through an unrelated allowed command,
monkeypatching the operation map, or claiming an external helper is covered by
the unchanged launcher would misrepresent its boundary.

Adding `owner export-bundle` is possible without a native rebuild: an inline
controller could reuse existing argument roles and require only changed owner,
launcher, PROFILE metadata and a file-only assembly recipe. The loader's code
need not change if no auxiliary role is added. However, it is not cost-free:
`ordinary_module_anchor/module_export.py:31-43` deliberately includes `owner.py`
and `profile.py` in the anchor-support descriptor. Changing owner changes that
identity, even though the proposed operation adds no mathematical authority.
Existing anchors must not silently migrate. This is disproportionate coupling
for an inert export utility when a companion can leave those bytes unchanged.

## Minimal public surface

Use one fixed-action command, conceptually:

```text
run-export --package ABS --profile-sha256 HEX
           --python-runtime ABS --lean-runtime ABS
           --request ABS --request-sha256 HEX --diagnostics FRESH_ABS
           --wall-seconds N --cpu-seconds N --memory-mib N
           --active-processes N --stdout-bytes N --stderr-bytes N
```

This is a proposed interface, not an existing executable. The request should
have an exact new versioned schema containing catalog/custody paths, store ID,
custody-limit selection, explicit context root, exact target records
`{name, export_id, unit_id}`, fresh bundle destination and finite export limits.
It must not contain commands, import paths, provider addresses or code. Require
nonoverlap with package/runtime/state/input/diagnostic paths and no redirections.
No implicit latest-root selection, arbitrary database path traversal or retry.

The launcher can reuse the unchanged approved launcher module's
`bind_support`, `load_supervision` and `operational_result` helpers after
pinning its exact source. It must select a fixed child script whose bytes are
in a separately approved companion manifest; no generic arbitrary-command API.
The existing Job supervisor then bounds the whole child process. The companion
must preserve the original deadline and log allowance and report clean closure
separately from the child's export outcome. Hashes select approved code; they
do not establish its safety or mathematical authority.

The child can pin/load the existing owner module, call its `bootstrap` and the
selected loader's `load`, then use the installed shared `A`, `O` and
`loaded.baseline_intake.B`. This avoids a replacement evidence codec or direct
SQLite reading. Its catalogue open must be the ordinary locked API, with
exception-safe cleanup. Opening may mark abandoned operations interrupted;
therefore say **no new mathematical admission**, not literally read-only state.
The ordinary loader still requires the selected Lean runtime/support pins even
though this operation must never launch Lean, Lake, a compiler or a network call.

## Portable output and authority

Keep the existing `DMKN_ORDINARY_BASELINE_BUNDLE_V1` manifest and derived
`units/<unit_id>.json` files. `baseline_bundle.split_units` and `make_manifest`
already enforce finite whole-unit batching, canonical identities and aggregate
bounds (`baseline_bundle.py:313-355`). They do not prove dependency closure.
The export controller must separately establish the complete selected import
closure above the fixed basis and verify its bindings against the selected
protected local context. Do not export theorem signatures with scratch axioms
or silently omit proof-only imports to make a cold bundle smaller.

The explicit target selection belongs in a bounded `TARGETS.json` sidecar;
baseline intake consumes its existing manifest unchanged. Preserve original
evidence bytes and include required whole-unit peers: selective targets do not
mean perfect per-theorem secrecy. Write the manifest/completion marker only
after every output file is complete and pinned. Partial output is retained but
never described as a completed bundle.

Keep a local operation report outside the portable payload, binding request,
package PROFILE, context, target list, manifest SHA, unit/batch/byte counts and
cost. Its claim must be `INERT_EXPORT_NOT_TRANSFERABLE_WARRANT`, not a receipt
that a receiver may promote to authority. Producer filesystem paths need not
enter portable manifests. Actual receiver acceptance remains the existing
`baseline_intake.py:255-329` sequence of preflight and native admission.

## Scope and expected engineering cost

Expected new surface: two small Python files (fixed-action wrapper and export
controller), one exact companion support map, a short usage guide and focused
controls. A rough design estimate is 350-650 production lines, depending on
whether closure traversal can directly reuse a suitable existing collector;
this is not measured effort or a completion-time promise. The expensive parts
are closure/warrant correctness and output/containment failure behavior, not
compilation. A fresh native build, full package copy or archive campaign is
unnecessary. Do not turn this into another successive-overlay chain.

One bounded changed-boundary test selection after independent source review is
reasonable: target not warranted, missing/conflicting dependency, quota refusal,
lock contention, partial-write failure, exact accepted-target roundtrip through
unchanged intake. Pure controls should distinguish inert metadata from native
acceptance. Reuse existing checking evidence and test one real interoperability
boundary, not another long theory-generation or full-source rebuild campaign.

Defer if the route audit finds an already public source-free selected-export
path with equivalent custody isolation. Also defer if the implementation scope
expands into anchor migration or a new acceptance protocol. This recommendation
selects the smallest integration direction, not permission to run a campaign.

## Inspected source pins

These match current default PROFILE roles (the module-export pin is additionally
recorded for the coupling argument). Paths are under `software/v5/`.

| Source | SHA-256 |
|---|---|
| `ordinary_contact_federation/run.py` | `47a2b63c73f1bd8346c5881c6d6a76abac86d33aa8e55bfc19bf3359ea924a39` |
| `ordinary_sparse_access/profile.py` | `1f40fb7a663c10d8f09132375ac8ab7899dea5830fff4979e0dda66b668003f8` |
| `ordinary_native_package/owner.py` | `56ef042f652fcb88cae7d16ab74883016a469e2e82777c1a173f842f5ef8245a` |
| `ordinary_baseline/baseline_bundle.py` | `d5a9c13392e2de8b170cbaf4a9a27e4d1e5d99eb2714165848a640069fe42fce` |
| `ordinary_baseline/baseline_intake.py` | `b5a17aa580f8d9cfdeaaded7d93c2b12ad6e19e5018bf5e7c087cb56760069d8` |
| `ordinary_module_anchor/module_export.py` | `85f9a2b5695dd90dd888bd3868f51a41904cb0b2d0d14335abe0b65d5182b65c` |

A fresh independently generated package may have another PROFILE hash. Prefer
explicit operator-approved package selection plus these required source/API
compatibility checks over hard-coding one historical generated native receipt.
The selected package loader must still validate its complete own PROFILE and
installation. Neither matching role names nor a foreign success report suffices.
