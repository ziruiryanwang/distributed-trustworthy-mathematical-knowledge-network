# Generic ordinary source contribution: implementation checkpoint

2026-10-23. Author: portable integration agent. Source implementation, not an
executed contribution or a deployable-v5 claim. Root owns finite runtime
selection, installation support adoption and final outcome interpretation.

## User workflow and consequential change

An owner has already checked some useful mathematics. Its local person or agent
wants to write new Lean source using any selected subset of that mathematics,
then contribute the resulting definitions and theorems. The old helper accepted
only one discovered method, one fixed successor template and one fixed output
name. Those restrictions obstructed actual use without improving acceptance.

The new helper removes exactly those fixture restrictions. It reuses the existing
portable owner request, complete-unit exporter, candidate binder, ordinary native
admission, custody and type-preview APIs. It does not add a certificate scheme,
task planner, mandatory task list, usefulness rule, network protocol or new trust
mode. Research direction remains outside the mathematical acceptance rules.

## Public contract

`software/v5/ordinary_lean/ordinary_contribution.py` provides:

```python
contribute_source(
    owner, parent_root, acquired_targets, source_body, output_names,
    *, output_directory, profile, parent_deadline,
    make_budget, account_worker_cpu, check_parent,
)
```

The caller owns an already-open `OrdinaryAdmission` and its durable evidence
store. The helper never initializes or copies an owner or launches a peer role.

- `acquired_targets`: zero to 32 exact `{name, export_id, unit_id}` values.
  Every selected export must already have the exact protected-context warrant.
  Inputs are validated and detached before controller callbacks use them.
- `source_body`: 1 through 1 MiB of owner-approved UTF-8 Lean body bytes, no NUL.
  No sentinel substitution or dotted-string name approximation occurs.
- `output_names`: one to 32 distinct encoded Lean names, bounded to 64 KiB of
  canonical JSON, all absent from the protected parent. Caller order is kept.
- `output_directory`: fresh ordinary absolute local directory. Partial artifacts
  and accepted state are retained on failure, not silently cleaned or retried.
- The three callbacks share the original parent wall/CPU allocation. Preparation,
  profile verification, authoring, binding, admission and publication remain
  inside it. A new operation budget may contain only the remaining allocation.

The generated source has fixed `module`, `public import Init`, two meta imports,
`public section`, the existing portable construction command, exact caller bytes
and the new multi-output export command. Absolute path literals retain the
predecessor's explicit ASCII limitation; declaration names can contain UTF-8.
The internal `OrdinaryProducer.lean` filename is retained only to reuse the
unchanged worker shim, not to retain its fixture source.

When there are no acquired targets, request construction selects the genuine
protected `Eq` basis symbol. This is not an invented assumption or new empty
request grammar. The fixed basis must already be admitted in the owner.

`PortableContributionExportCommand.lean` accepts the exact bounded names file:

```lean
#ordinary_export_contribution "absolute-targets.json" "absolute-candidate.json"
```

Its explicit targets are safe, new, current-module definitions or theorems. It
does not allow a fresh axiom or unsafe/partial target. Generated dependencies and
complete declaration groups remain the unchanged exporter's responsibility.
The exporter is invoked once with the array; no Python merge invents a closure.
The independent native admission still enforces the full admitted policy on all
complete units, including generated declarations and dependencies.

## Support is selected, not inferred from paths

The frozen `AuthoringProfile` fields are:

```python
installation_manifest_sha256: str
helper_paths: tuple[Path, ...]
author_worker_script: Path
file_pins: tuple[tuple[Path, int, str], ...]  # path, bytes, SHA-256
```

Root constructs this profile from the exact retained helper build/support map.
Its installation pin must match the open owner's installation. `verify(check)`
checks ordinary nonredirected paths, actual imported Python helper source paths,
shared installed core module identities, helper-directory file census and exact
file hashes. All helper-directory files are covered, including nested loadable
companions, rather than just the first `.olean` suffix. Missing, extra, changed or
unlisted support refuses. Bounds: eight helper roots; 4096 file pins/census
entries; depth eight; 128 MiB per pinned file; 512 MiB aggregate pinned bytes.
Hashing checks the original budget after each 1 MiB chunk.

The loaded contribution controller, request/binder/preview modules and their
Python helper source modules must be in the pins, together with the author
worker. Standard Python/Lean/runtime support remains under the installed owner's
existing runtime premise. The profile is checked before and after authoring.
These checks are useful exact-support controls, not proof that the support is
correct or a defense against hostile local filesystem races. Owner-approved
source is executable code, and Windows Jobs are resource controls, not a sandbox.

No installed semantic/implementation identity is changed by this helper: its
authoring output remains inert until it crosses the existing acceptance core.
This argument does not grant permission to a remote party to execute source.

## Acceptance and failure ordering

The flow is:

1. Validate/detach inputs and verify adopted support under the parent budget.
2. Read the protected context and check selected warrants/new output names.
3. Prepare exact selected semantic interfaces from local custody. Singleton
   theorem authoring uses signatures; proof-only ancestral dependencies are not
   recursively fetched. Required definition semantics/generated groups remain.
4. Save exact request files, targets and generated source, then run the selected
   worker under the remaining authoring operation allowance.
5. Charge the returned actual Job CPU once, retain its supervision report, require
   actual clean completion, and reread support/source/request/target bytes.
6. Bind the inert candidate to the exact ordered outputs and protected context.
   Only `READY` proceeds to ordinary preflight and then native admission.
7. Charge admission CPU once in `finally`. Only the actual admission result
   establishes mathematical acceptance; saved JSON is never replay authority.
8. Derive exact output previews and read them back from custody. Save complete
   new-unit evidence and return publication bytes for the caller's later service.

There is intentionally no requirement that every acquired method occurs in the
new result. Proof dependencies are computed from the actual exported units;
whether a local investigation was useful is not a prerequisite for validity.

On binder refusal, `ContributionError.report.needs_local_interpretations` exposes
the exact unresolved names. On preflight refusal, `missing_dependencies` exposes
exact name/ExportID pairs. Neither diagnostic acquires, retries or renews work.
The report retains the phase, original error, accepted admission (if any), native
CPU and partial-output retention rule. Failure to write `FAILURE.json` is itself
recorded in the exception report; it cannot hide an already returned accepted
root. An after-admission failure is not a rollback or permission to recheck from
a fresh parent allowance.

Successful result fields include `local_root`, `parent_root`, `targets`, `units`,
`previews`, `acquired_targets`, `admission`, `authoring_supervision`, and measured
native CPU/wall time. Target/preview order matches the requested outputs. Units
are saved once even when several exports belong to the same complete unit.
This result is not index publication, peer acceptance, retention funding or a
claim that the contribution is mathematically novel.

## Why this is the economical next step

This change turns the existing demonstrated ordinary workflow into a reusable
owner API. It adds no prover/certificate obligation to an ordinary contributor.
Construction follows selected semantic needs; new acceptance checks complete new
units above an existing protected owner, not a replay of every imported theorem
proof. This is a practical locality improvement, not constant-cost verification:
selected theorem evidence still has bytes, transparent semantics can be needed,
and cold owner-context loading can grow with its local library.

The decision-changing evidence is one small multi-output contribution with a
caller-chosen bare definition and theorem, using more than one already-warranted
method. Existing basis/producer/reciprocal tests should not be repeated. Pure
native-free controls cover detached inputs, bounds, exact request selection,
marker-free assembly, multi-output binding/publication and retained failure
information. Independent source review covers actual-event/budget ordering and
support adoption. These are complementary boundaries, not duplicate campaigns.

## Source pins and review status

- Wrapper, stable handoff to root:
  `dc6988a6a237f482fed6f9055d8a248e430c8c99cb17c70a4a110774717e0182`.
- Python, current implementation submitted for independent review:
  `c856d4b60e1324191207a918a42e37779e509a3c92f4ccd13f308dbda3e6f4f0`.
- Two source issues were corrected before native contribution: restore fixed
  `Init`/public scope; expose exact missing interpretations in failure diagnostics.

This agent executed no Python, Lean build, test, network or Git operation. Root's
separate selected build/results and the independent review are authoritative for
runtime status. The final deployable-v5 goal remains open beyond this bounded
operability seam.

## Actual02 source-inference failure: narrow correction audit

2026-10-23, source-only review requested by root. Actual02's retained authoring
stdout records successful construction of three groups, 584 labels and both
selected theorem signatures, then an application mismatch: `hf : Stable f P`
was expected to have type `Stable (composeFour f g h k) P` at the implicit
`stable_compose hf` application. The exporter subsequently rejected the
elaborator's error-recovery `sorry`. `FAILURE.json` records phase `AUTHORING`,
accepted `null`, and 2.46875 native CPU seconds. This is not an admission result.

The retained actual signature groups confirm these explicit binder orders:

```text
stable_compose   : α, f, g, P, hf, hg
stable_threefold : α, f, g, h, P, hf, hg, hh
```

Consequently root's proposed replacement proof body is well justified:

```lean
@DMKN.PortableMethod.stable_compose α f (fun x => g (h (k x))) P hf
  (@DMKN.PortableMethod.stable_threefold α g h k P hg hh hk)
```

The inner application has type `Stable (fun x => g (h (k x))) P`. The outer
application therefore has type `Stable (fun x => f (g (h (k x)))) P`, which is
definitionally equal to the unchanged target
`Stable (composeFour f g h k) P`: unfold the new `composeFour` definition and
beta-reduce. No theorem body, additional axiom or weakened policy is needed.
Explicit arguments remove the higher-order implicit choice implicated by the
actual error; they do not change either selected method or the intended result.

This supports one fresh caller example `GenericContributionExplicitBody.lean`,
not a controller/acceptance redesign or a guarantee that every runtime boundary
will succeed. Failed actual02 inputs, sources, logs and costs remain unchanged.
This review ran no Lean/Python operation and edited no used software/evidence.
