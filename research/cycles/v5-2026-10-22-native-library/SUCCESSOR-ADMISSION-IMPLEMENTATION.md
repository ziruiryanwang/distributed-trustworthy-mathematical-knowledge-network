# One-batch successor admission: implementation checkpoint

2026-10-23. Source-only implementation selected by root after adopting
`SUCCESSOR-ADMISSION-PLAN.md`. No test, native process, catalog copy, admission
or Git operation was launched by this assignment. There is not yet a successful
actual consumer bundle for this controller to consume.

Source: `software/v5/ordinary_lean/run_successor_admission.py`

SHA256: `0dba8fa63db3da9898ee545e7e8f041e97fc9b714cd330f323f92b7732a55f3b`

## Invocation and exact input contract

```text
python -I -S -B <selected-source-snapshot>/run_successor_admission.py
  OUTPUT BUNDLE PREPARE_MANIFEST CATALOG_COPY_MANIFEST TARGET_DOTTED_NAME
```

`OUTPUT` is the fresh outer-run directory. All paths must be absolute beneath
canonical `experiments/v5-local-checks`; the source must belong to that output's
immutable source snapshot. The actual bundle and preparation manifest are
explicit selected arguments, not guessed future success paths/hashes.

`PREPARE_MANIFEST` uses the existing `profile_id`, `context_id`, `request_files`
fields. Its request directory is `PREPARE_MANIFEST.parent / "owner-request"`.
The exact numbered files are authenticated transitively from that root-pinned
manifest, so they do not require hundreds of separate outer runtime pins. The
projection may retain fewer than 581 basis rows; actual IDs still must match
the real accepted parent. There is no hardcoded 387-group/1,098-name request.

The root-authored copy manifest has these exact fields:

```text
schema: "DMKN_ORDINARY_SUCCESSOR_PARENT_COPY_V1"
store_directory: exact adopted recovery catalog absolute path
profile_id, basis_id, context_id, store_id: exact retained identities
directories: exact six relative directory names, including failed operation
files: exact seven relative files -> {bytes, sha256}
```

The exact adopted database hash `bcb94ff9...`, four-root context `4d70ddd6...`,
profile/store/basis IDs and canonical original/recovery paths are fixed by the
source. This is continuation of an already adopted protected local store, not
a generic foreign-catalog importer.

Outer runtime pins must include the actual bundle, preparation/copy manifests,
original admission selection, its `native-admission/PROFILE.json`, all original
profile-listed adapter source and compiled files, named kernel/Python files,
and original `sources/tools/Run-V5-Check.py`. The existing frozen supervisor
release manifest is checked against its established constant before loading.
The old 42 MB producer export and 2,852 old evidence documents are not read.

## New invariants

- The original store is byte-verified, locked, copied to a fresh directory,
  fsynced/read back and reverified. No original mutable SQLite open occurs.
  The copy retains its failed reservation and exact store identity. Only its
  database changes; copied parent chunk/ADOPTION bytes are pinned across the run.
- Native support is checked against the fixed original profile and source
  selection. It uses the unchanged old worker/checker artifacts, not mutable
  modern authoring helpers. No receiver profile relabeling or new verifier.
- Every prepared correspondence name/ID must already exist in the actual
  accepted parent. Bundle boundary rows must additionally match that prepared
  map. Same-name parent lookup is not a fallback for an unbound external name.
- `inspect_unit` derives exact per-unit imports; envelopes are canonicalized and
  re-read by existing `read_evidence`. New names may not overwrite parent or
  earlier unit names. Per-unit imported IDs come only from the selected boundary
  or previously derived new unit identities. Literal-only bundle support names
  are not injected as unused envelope imports.
- One batch only: 1,024 units, 65,536 names, 2,097,152 encoded nodes, 8 MiB per
  envelope, 64 MiB aggregate envelope/native-unit data. Larger inputs refuse
  before native spending. Preparation data is released before the native worker.
- Existing `reserve_extension` independently checks exact bytes/import IDs.
  Only a real clean supervised `extend` invocation, unchanged selected inputs
  and exact generated report binding reach `_commit_checked`. New `PANIC`
  diagnostics refuse automatic promotion; the old recovery's narrowly reviewed
  diagnostics are not blanket permission for a new operation.
- Existing reopen checks establish the new target and exact final bindings.
  No automatic retry follows failure or uncertain commit. A postcommit failure
  cannot erase the real committed root and must be resolved by inspection.

## Resource and evidence boundary

The driver permits a root-selected maximum of 120 CPU seconds, 180 wall seconds,
1,536 MiB and at least three outer process slots. It reserves controller cleanup
time and computes the inner worker's allowance from the actual remainder after
preparation. This does not itself select or authorize such a runtime.

It saves fresh exact evidence, native units, `ADMISSION-PLAN.json`, actual
supervision/report and `SUCCESSOR-RESULT.json`. The result includes target/root
IDs, request hash, selected inputs, native artifact/report hashes, name/unit/node
counts and known controller/worker cost. Failure evidence stays in place.

Independent source review and a finite root selection remain necessary. The
decisive later evidence is actual consumer source use plus real independent
successor checking; compilation or this implementation does not supply it.
Neither the controller nor a successful fixture proves discovery, novelty,
growth advantage, portable operation or final public-release readiness.
