# Focused private parse-reuse controls

Source/test preparation only under CONTRACT.md. No control, syntax-only import,
native call, database or selector has run for this plan. Root owns the exact
selection and first launch; independent source review is required first. All
paths use `E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Test boundary

`controls.py` compares the pinned current-release predecessor with the two
fresh successors. It loads the nine explicit Python sources in its `PINS` map
directly, without invoking the package loader, reading a live owner, scanning
the full package or validating native/runtime outputs. The three retained
genuine small V2 units total 10,672 bytes. They are syntax fixtures only; the
test's selected parent, custody, grants and checking events are explicit doubles.

The successor interface under test is:

```text
_plan_with_parsed(context, raw_units, limits, check)
    -> (raw-only Preflight, private exact-bytes -> Evidence map)
```

Public `preflight` and `_plan` retain their raw-only result. Actual `admit`
independently builds a new private map from the caller's current raw bytes and
current parent. It projects immutable ordered raw bytes, IDs and native JSON,
then releases parsed objects before `_stage`, catalog and native callbacks.
Baseline metadata planning releases its private map after each batch.

Actual unchanged `_stage`, `PortableCatalog.reserve_extension`, admission grant
checks, native-input construction, report checks and cleanup control flow run
against inert storage/event doubles. `StoreDouble.put_evidence` deliberately
performs one real portable read to model the unchanged custody validation
boundary; it does not certify real custody transactions, quotas or durability.
The locator shape used in metadata quota comparison is explicitly synthetic and
identical for old/new, so its equality result is not a production schema test.
`subprocess` entry points, `os.system`, SQLite connections, sockets and real
owner/catalog opening are forbidden. No actual native checking occurs; strings
such as `CHECKED` in synthetic reports remain test-double observations.

## Eleven focused groups

1. Compare public plans, exact raw-only fields and one parse per supplied raw
   across normal/reversed input, exact duplicates, mixed existing/new units and
   complete reuse. Compare predecessor/successor output projections.
2. Check the private map's exact immutable byte keys; mutate its private document
   in a test and require a later independent public call to parse cleanly again.
3. Preserve missing-import `NEEDS` and distinct-identity/same-name conflict refusal.
4. Run real admission control flow with synthetic native events. Require exact
   native unit JSON, parent plan JSON, order, IDs and names against the predecessor;
   count eight versus five reads per new unit including the caller's preflight.
5. Forge public status/order/missing/reused metadata and attach a fake parsed
   attribute; require actual admission to recompute from raw units. All-reused
   and the next call on the same synthetic owner still parse four times per unit,
   stage/read back, and launch no new synthetic native event.
6. Change raw syntax, claimed parent, current parent bindings and import identity;
   require refusal before any custody/grant/native effect.
7. Inspect the new private `_execute` projection's immutable components. Inject
   changed ordered bytes or IDs into this internal tuple and require its exact
   binding guard plus grant abandonment before native entry. This tests the new
   guard; it does not treat private in-process tampering as the threat model.
8. Compare custody-put failure, mismatched grant, clean native failure,
   mismatched report and uncertain native closure. Require unchanged no-commit,
   abandonment or quarantine/withdrawal behavior, without retry or rollback claim.
9. Compare whole-manifest metadata projections and exact counts: four to two reads
   per fresh unit, three to two per already-held unit. For the successor require
   zero live prior-batch `Evidence` at the next batch read and at most one batch's
   parsed objects alive. The predecessor retains its last `item` loop alias across
   that boundary; this known historical lifetime is not a predecessor-test failure.
10. Run the actual two-batch intake/admission control flow against doubles and
    require thirteen to eight portable reads per fresh unit, exact native
    projections, unchanged metadata and two then one checked units in the
    synthetic event reports.
11. Change the second batch's actual reread after successful metadata planning;
    preserve exactly the first confirmed synthetic prefix, report
    `possible_unreported_commit=false`, and perform no retry.

Every counted reader wraps the real parser and retains only weak references to
returned `Evidence`. Each observed call checks that these objects are released
after completion/refusal. At custody-put entry, only `_stage`'s own strict parse
may be live; at synthetic native entry none may remain. This catches accidental
retention of the private map through callbacks. Source review must additionally
confirm no proof-document aliases escape: weak references to `Evidence` alone
cannot prove that a dictionary subtree was not separately retained. Bounded name
subtrees and immutable serialized native bytes are intentional.

The test does not measure performance, establish a memory-MiB bound from a small
fixture, exercise real native mathematics, or repeat parser/transport/kernel
campaigns. The structural count reduction is the evidence sought; practical rich
intake runtime remains a later independently selected question.

## Exact finite execution shape, not authorization

Selection name: `parse-reuse-controls01`. Existing `tools/Run-V5-Check.py` only;
no nested supervisor. Exact selected command:

```text
D:\Python314\python.exe -I -S -B
  {snapshot}/software/v5/ordinary_parse_reuse/controls.py
  --output {output}/controls
```

The test enforces 45 wall / 30 controller CPU seconds cooperatively. Proposed
outer allowance is 60 wall / 45 inclusive Job CPU seconds, 512 MiB, one process,
1 MiB stdout and 1 MiB stderr. Root may record a different prospectively reviewed
finite outer allowance; no child runtime or memory-heavy work is requested.
Only the fresh `controls/RESULT.json` is written. Virtual model paths are not
created. The runner preserves its normal selection/source snapshots and logs.
First success or failure is final for this selection; preserve it without retry.

Required immutable input census is **15 external pins**: nine exact current
package Python modules listed in `controls.py:PINS`, three exact fixture files
listed in `FIXTURES`, and `D:\Python314/python.exe`, `python314.dll`, `python3.dll`.
All fixture/module hashes are literal in the harness and must also appear in the
runner selection. No Lean executable, whole package map, mutable owner, retained
database, materialized Std tree or full Std proof is an input.

Required code snapshots are the runner, `controls.py`, successor
`ordinary_admission.py` and successor `baseline_intake.py`; also snapshot this
plan, CONTRACT and the root-assigned selector for review provenance.
This yields seven source snapshots, below the runner limits. DESIGN is a separate
source-review checkpoint, not an imported test input. The final selection must pin
the actual final successor/control bytes and be independently read before launch.

At author handoff the successor sources are:

- `ordinary_admission.py`, 41,372 bytes,
  `98c88eb0e7ea5e101f6ccd8e94b56a0cc248167c317a0440ba00dc86f503cd9a`.
- `baseline_intake.py`, 17,024 bytes,
  `9b243232603206b3a0925f639a0b8b1a6cbf0de8ca093ad4aa3642c595ff1142`.

These source pins do not authorize an execution or installation. If review
changes either successor, update the plan's recorded handoff pins and re-read
the corresponding test seam before the first use.

## Required saved outcome

Require the existing runner's `COMMAND_EXITED_ZERO_AND_CLOSED`, zero child exit,
reaping, closed Job, zero active/terminated processes, empty cleanup errors and
empty stderr. The sole test report must be
`PASS_FOCUSED_PARSE_REUSE_INERT_CONTROLS`, eleven groups, no forbidden calls,
`mathematical_acceptance=false` and the explicit double-authority label. Confirm
the exact parse counters and projection equality groups; do not infer them from
process exit alone. Record outer inclusive Job CPU plus wrapper once. Preserve
the first failed group/error if any; no native outcome is implied in either case.
