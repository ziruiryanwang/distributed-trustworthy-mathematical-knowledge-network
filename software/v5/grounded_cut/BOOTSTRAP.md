# Exact grounded-cut support loading

`cut_bootstrap.py` is a source-only loader for the future approved addition. It
does not build, install, package, execute Lean, open a catalog or admit mathematics.
No runtime is selected by these source files.

## Calling contract

An approved isolated owner entrypoint first loads the exact ordinary package with
its existing profile loader. It then executes the owner-approved bootstrap and
calls:

```python
loaded = cut_bootstrap.load(addition_root, expected_manifest_sha256, base, check=check)
runtime_module = loaded.runtime
controller_module = loaded.controller
runtime = loaded.support
```

`check` is the caller's original nonrenewing operation check. It is called around
bounded reads, at finite verification steps, during exact support opening and
before return. The return contains the runtime/controller modules from one exact
loaded graph and one `CutRuntime` opened against those modules and that base.
No allowance, worker, store, source anchor or mathematical event is created here.

The owner entrypoint, Python interpreter, original base adoption and protected
immutable storage remain premises. Checking the on-disk bootstrap does not prove
how the currently executing bootstrap was initially adopted. An arbitrary hostile
caller inside Python can alter objects: this loader is not an in-process sandbox
or a cryptographic software attestation mechanism.

## Verified graph

Before executing addition modules, the loader rejects preloaded cut-map, summary,
anchor, catalog, runtime, controller or worker module names and their submodules.
The bootstrap itself is necessarily already executing and must have the exact
pinned file location and bytes. The addition root never enters `sys.path`.

The supplied ordinary namespace must share the already-loaded admission,
evidence, semantics, portable evidence and both catalog modules by object
identity. Their actual file paths and pinned source bytes must agree with the
opened installation. The current `PROFILE.json` must exactly match the supplied
descriptor; its exact installation manifest, helper paths, worker and entire
profile pin set must match the supplied installation and `AuthoringProfile`.
The actual ordinary contribution module must share that same core graph.

`CUT-SUPPORT.json` is bounded canonical JSON with precisely `schema`,
`base_profile_sha256` and `files`. Its externally selected SHA-256 and exact base
profile SHA-256 are checked. The schema is `DMKN_GROUNDED_CUT_SUPPORT_V1`.
The file census is fixed: the ten named source files including this bootstrap,
the required `lean-lib/GroundedCut.olean`, and only its four permitted auxiliary
suffixes. No manifest-provided import name or arbitrary relative path is used.

All seven Python sources in the loading path are read into bounded byte strings
and matched to their pins **before any addition module executes**. Source modules
then execute from those verified strings in this order:

```text
cut_map → cut_summary → source_anchor → cut_catalog → cut_runtime → cut_controller
```

Each module is registered only under its fixed name. This permits normal imports
of earlier exact modules and dataclass initialization without searching a peer
directory. After loading, explicit identity checks bind each helper's actual
core and cut-module references, including the controller's entire dependency
graph. File-backed imports or bytecode caches do not supply replacement sources.

The loaded runtime must declare the same support schema and exact payload set.
Its normal `CutRuntime.open` verifies the remaining payload bytes, native object
census and ordinary authoring profile, and rechecks the addition source files.
The returned support object must bind the same runtime class, root, base object,
manifest bytes/hash and support ID. The ordinary profile's full payload check
is not separately duplicated by this bootstrap before `CutRuntime.open`.

## Refusal and limits

Owner paths must be ordinary, absolute and disjoint from the base and runtime
attachments. The process must use the existing Windows isolated/no-site/no-
bytecode/unoptimized profile. Manifest reads are capped at 2 MiB, each executed
Python source at 2 MiB, each declared payload at 64 MiB and the entire declared
addition at 512 MiB. The original enclosing operation remains responsible for
CPU, wall time, memory and native-process containment.

On failure, this call removes only the exact module objects it registered, in
reverse order; it does not remove preexisting modules, change `sys.path`, mutate
catalogs or perform retries. No successfully returned graph means no permission
to proceed to the controller. The actual protected controller still has all
source-authority, grounding, worker, custody, transaction and crash-disposition
obligations. Exact loading establishes code coherence under the premises, not
mathematical validity or deployable-v5 completion.
