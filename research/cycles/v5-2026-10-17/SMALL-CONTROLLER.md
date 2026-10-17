# Bounded po18 controller implementation checkpoint

2026-10-17, `memo_tests_review`. Canonical workspace guard passes.
Scope is only fresh `software/v5/aggregate_small/producer.py`, `__init__.py`
and this checkpoint under root's SMALL-PRODUCER-SELECTION. No runtime, import,
test, build, proof or Git operation was performed. Existing producers are
unchanged. This is a source candidate awaiting independent changed-boundary
review, not production or mathematical qualification.

## Source identity

| File | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/aggregate_small/producer.py` | 52625 | `a2d23bcfe0b798f747d4a59330655a865a14a73cb4d635a50332fa65c75a6985` |
| `software/v5/aggregate_small/__init__.py` | 156 | `8226f83b753a224b57d5ef35338e437665fab72849c8f060dd61574a043ff36f` |

Narrow predecessor: frozen `aggregate_resources/producer.py`, 44,720 bytes,
SHA-256 `1d191bdc2079760ce89a57a08924254f01487d24726e10b386c7eca1ef9eec09`.
The new file was created and changed using apply_patch. The retained
`production.producer` supplies only unchanged pure helpers and the pinned
support/supervisor loader; its N128 graph functions are not borrowed or patched.

## Public constructor and identities

`aggregate_small.AggregateProducer(profile)` retains the predecessor's required
profile fields and explicit owner-selected stage-memory ceiling (1..8192 MiB,
also checked against the actual adopted supervisor ceiling). All controller
schemas use fresh prefix `DMKN_V5_SMALL_AGGREGATE_PRODUCER_` and suffixes
`PROFILE_V1`, `REQUEST_V1`, `ATTEMPT_V1`, `RESERVATION_V1`, `STAGE_V1`.
An old resource profile is not accepted. Source/profile hashes, exact same
budget/session/allowance history, prior-success retention, first-failure stop,
unknown-closure accounting, fail-closed finalization and external carried costs
are preserved. Larger resource maxima do not create an allowance or provide RAM.

The unchanged A image adoption still binds actual retained memo image assembly,
guest/library build and source records. The profile has exact new controller
source pins and new stage-host build records. `_adopt_host_build` validates the
fresh stage/snapshot builder formats, clean completed one-link command, zero
guest/proof/backend/checker/relation/network work, exact output/source path,
selection/attempt/result/source-map chain, selected limits and fresh build name.
Snapshot executable is at most 8 MiB; stage executable remains at most 128 MiB.

The snapshot adapter's new `host_build` pin bundle is required in its result
and exact configuration. `_snapshot` adopts the nested five records, adds
source snapshots and the actual snapshot executable to its input pins, checks
the actual outer invocation and host runtime pin, and keeps all finalization
overrides live during subsequent controller rebinding. `snapshot_evidence`
itself remains the existing five-key map. Snapshot status is unchanged, but
its schemas are `DMKN_SMALL_AGGREGATE_COST_SCREEN_RESULT_V1` and
`DMKN_SMALL_AGGREGATE_SNAPSHOT_RESULT_V1`.

## Changed graph and transport

Pure helper signatures available to root's focused controls:

```text
stage_key(kind, index) -> canonical stage key
split_key(key) -> (kind, integer index)
graph(segments, assumptions) -> ordered [(key, tuple(dependencies)), ...]
missing_plan(segments, assumptions, available) -> ordered missing graph
dependency_manifest(session, key, dependencies) -> exact manifest dict
stage_argv(host, adopted_image, session, key, artifact, manifest_pin) -> argv
stage_output(raw, key, session, support, artifact, manifest_pin, dependency_keys)
```

Own N256/M8 graph has `H=3s+m<=776` calls and `Q=H-1<=775` checkpoints.
Canonical stage keys reject alternative numeric spellings, booleans, finish
indices other than zero, join zero and resolve indices above seven. The
missing-plan walk is iterative and visits at most H distinct nodes; graph
order and the complete-composite finish dependencies remain unchanged.

Manifest schema agreed with the native author:

```text
schema = DMKN_AGGREGATE_DEPENDENCIES_V1
session_binding, capsule_binding
stage = canonical stage key
dependencies = [{key, file: {path, bytes, sha256}}, ...]
```

It is exactly the graph's ordered dependency vector, including all segment
proofs plus final resolved prefix at finish. Each dependency has a pin at most
512 KiB and a path at most 512 UTF-16 units. Per-kind manifest byte limits are
2/4/6/4/256 KiB for segment/lift/join/resolve/finish. The new `stage-manifest`
command has exactly `16+m` operands including the executable and manifest
path/length/hash. Windows quoting is accounted using `subprocess.list2cmdline`;
the encoded UTF-16 command, including its NUL terminator, must fit 32,767 units.
The old checkpoint-fanout argv is not emitted.

The manifest is saved create-new/fsynced through the pinned retained helper,
then checked against its canonical expected bytes. Its pin is included in the
reservation and active inputs. Native stdout must echo the exact pin and
ordered keys using `DMKN_SMALL_AGGREGATE_PROOF_STAGE_V1`; mathematical checking
still belongs to the native stage and final verifier, never these JSON records.

## Actual resource seams enforced

- po2 is exactly 18; cycles are 1..2^26. Capsule read/admission is at most
  96 MiB; image/checkpoint outer format FILE_LIMIT remains 64 MiB.
- Parents are at most 1 MiB each. Every incoming and prior retained checkpoint,
  as well as every new artifact/final receipt, is at most 512 KiB. Per-stage
  logs are at most 64 KiB each.
- Fixed initial session/snapshot inputs excluding capsule/checkpoints/prior
  reports must total at most 20 MiB. Complete initial inputs are at most
  512 MiB. Non-administrative inputs, including subsequently produced
  checkpoints/final receipt, are rechecked against 512 MiB on each rebind.
- New administrative pins have a separate 128 MiB total cap. Request/profile
  are each at most 1 MiB; reservation/stage-result records each at most 64 KiB;
  manifests retain their per-kind caps. Reservation references the manifest
  pin instead of duplicating its dependency rows. Every saved record is length/
  hash checked before being added to the active map. All maps still rehash.
- Stage reservation is selected artifact + two logs + unchanged 2 MiB
  administrative reserve **plus** 256 KiB manifest reserve, and nine entries.
  The existing four MiB/four-entry attempt allowance and final tails remain.
- Whole request maxima are 500,000 worker CPU, 7,200 controller CPU,
  172,800 wall seconds, 2,304 MiB output and 8,192 entries. Stage CPU/wall
  maxima are 1200/240, 250/150, 250/150, 600/600 and 300/120 respectively.
- `_envelope` retains its argument signature. It adds manifest read/output
  costs, nine entries per call and `selected_worker_wall_envelope`. Its
  full-path flag includes the sum of selected stage wall caps; controller
  overhead still requires additional headroom and actual admission.
- At most 16 prior attempts, each report at most 1 MiB and all prior reports
  together at most 8 MiB remain unchanged. No automatic retries or arbitrary
  stage scheduling were added.

These are file-byte and admission bounds, not memory sufficiency or completion
claims. The internal 160 MiB composite bound is implemented by the native owner,
not the Python controller. The final transmitted receipt remains at most
512 KiB. The source-derived po19 obstruction and unknown po18 costs remain as
stated in PRODUCER-NEXT-DECISION; no new measurement changes them.

## Review and next evidence boundary

Root owns changed-boundary tests, builds, the fresh complete layout and exact
future execution selectors. Source review must especially check manifest
ordinary-path/read/hash handling in the native host, generated-record lifetime,
snapshot/build adoption joins and the fixed/admin/read arithmetic. A fixture
that stubs `_snapshot` must also set `_snapshot_build_pins={}` deliberately;
the real path always sets it after exact adoption.

The next eventual proof discriminator is one actual full-po18 segment, after
real completed layout and capacity checks, not an automatic five-call prefix
or full proof campaign. All passing prior evidence remains reusable. This
source implementation is one missing producer capability; it does not close
genuine terminal public integration, full-cost useful-growth or v5 release.
