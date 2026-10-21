# One matched RC/general execution screen: source checkpoint

2026-10-21, core_release. Root-selected source-only adapter. No preparation,
supervisor, native host, guest, proof or network execution was performed.
Root owns selector, independent-review adoption and any subsequent launch.

## Selected implementation

`software/v5/restricted_composition/matched_pair.py` connects the already reviewed
pure preparer to two actual snapshot-host executions, using the retained v4
owner supervisor and Job implementation. It adds no checker, prover, backend,
public producer or trust mode. All used predecessor bytes remain untouched.

Invocation, only from a Run-V5-Check source snapshot:

```text
python -I -S -B <snapshot>/software/v5/restricted_composition/matched_pair.py
  --input <absolute-root-selected-config> --input-sha <exact-config-SHA>
  --output <outer-run>/pair
```

The input has schema `DMKN_RC_MATCHED_EXECUTION_INPUT_V1` and exactly these fields:

```text
schema
fixture: {path, bytes, sha256}
receipt: {path, bytes, sha256}
controls: {result, outer, selection}                 # each an exact file pin
general:
  host_build: {result, attempt, selection, source_map, command}
  assembly: {result, outer, guest_result, guest_attempt}
restricted:
  host_build: {result, attempt, selection, source_map, command}
  assembly: {result, outer, guest_result, guest_attempt}
```

All leaf records are `{path,bytes,sha256}`; input records are bounded to2MiB,
the fixture4MiB and receipt1MiB. Operational JSON permits finite timing numbers
but rejects duplicate keys/nonfinite values. Paths must be canonical ordinary
files under the canonical project, without reparse ancestry. Inputs are pinned
before use and rebound at finalization; build failure overrides must remain absent.

## Exact roots for the root selector

Everything below is relative to `experiments/v5-local-checks/`:

| Role | Required actual source of evidence |
|---|---|
| differential fixture | restricted-composition-controls-01/evidence/fixture.json |
| controls inner/outer | restricted-composition-controls-01/evidence/result.json and RESULT.json |
| controls selection | restricted-composition-controls-01-selection.json |
| general snapshot host | small-aggregate-snapshot-host-build-01 |
| restricted snapshot host | restricted-snapshot-host-build-01, actual success still requires root adoption |
| general guest build | typed-guest-build-01 |
| restricted guest build | restricted-guest-build-03, never either failed01/02 preflight |
| general assembly | typed-guest-image-assembly-01/assembly/RESULT.json plus enclosing RESULT.json |
| restricted assembly | restricted-guest-image-assembly-01/assembly/RESULT.json plus enclosing RESULT.json |

Host result/command/source-map are under their build directories; selections
and attempts use the sibling `<build>-selection.json` and `<build>-attempt.json`.
Guest attempts similarly sit beside their build directories. Assembly result's
exact guest-build pin, image pin and actual image ID are checked against those
records. Both enclosing assembly Jobs must be cleanly completed. Native host
production binds the adopted native-build02 result24e8ebf8; old snapshot host
source6644d9a0 and receipt source41db7677 remain identical for both arms.

RC guest03 is the final four-project-compile route: original module against the
already-adopted Nanoda, then RC core, aggregate and guest. Its exact build schema
is `DMKN_V5_RC_GUEST_FOUR_CRATE_BUILD_RESULT_V1` and required status is
`PASS_RC_GUEST_FOUR_CRATE_COMPILES_ONLY`. No historical failed module build is
promoted to success. RC assembly schema remains
`DMKN_V5_RC_GUEST_IMAGE_ASSEMBLY_RESULT_V1`. The general guest has the matching
`TYPED` four-crate schema/status. The adapter binds both exact adopted outcomes;
it does not launch compilation or re-review the source closure.

This is reuse of root-adopted exact build evidence, not a repeated compiler
source audit. Root must adopt actual new guest/image/host results before creating
the input. No placeholder A_RC or absent build record can be substituted.

## Mathematical matching and control lineage

The adapter requires the actual forty ordered cases and twenty-six refusals
from the frozen run_controls contract, their all-PASS inner result, clean outer
completion, native controls binary9711910d, exact fixture bytes/SHA and the
fixture-generator digest in the controls selection. The local selected fixture
generator must match that recorded digest. Thus the comparator is the exact
W emitted from the exact RC proof, not merely some proof with the same statement.

The pure preparer additionally binds the fixed base-I receipt/journal and exact
context-transport first target. Its predicted target module must equal the first
actual native differential result. No original FIRST workload or uncertified
recursive receipt is used.

The receipt path must be exactly
`module-base-production-01/finish-0/receipt.bin` under the experiment directory,
not an alternate same-named file. Selected preparer, fixture generator, control
contract and aggregate bindings must resolve to this run's source snapshot.

For each arm the unchanged host independently checks its own wire with its
linked native relation, verifies the genuine base receipt, recomputes the actual
ELF image and executes its guest once. Successful stdout, diagnostic, capsule,
exact H, wire/image hashes, genuine parent row, complete segment byte/hash list
and session census must agree. The final comparison checks H equality everywhere
except aggregate-image bytes12..43. That preserves exact member-J commitments,
foundation, policy, maximum rank and seal height.

The SDK `row_count` is already padded. Each segment's rows must equal
`2^po2`; their sum equals session row_count. Padding count is a subset, not an
extra quantity to add. Nonpadding rows are rows minus padding rows. Segment
instructions, padding and byte totals must also reproduce the diagnostic totals.
There must be exactly the expected consecutive segment files and no extras.

## Resource ownership and accounting

The host executions are serial, fixed order general then restricted, so they
do not interfere with each other's active process-memory footprint. Each uses
the existing supervisor with180inclusive CPU seconds,120seconds direct-host
wall timeout,3072MiB/two-process Job and1MiB stdout/stderr. The enclosing arm
has240seconds including preparation/write/readback. The pair has530seconds
and60adapter-controller CPU seconds; the root outer envelope must leave its own
setup/finalization reserve (for example600wall,420CPU,4096MiB/six processes).
These are ceilings, not expected time, new hardware requirements or sandboxing.

Each arm records its entire measured controller interval (writes, supervision,
hashing and endpoint validation) plus the inclusive host Job CPU. The retained
supervisor's reported wrapper CPU is already inside this interval and is not
added again. Remaining adapter CPU is common preparation, adoption, final input
binding and bookkeeping. It is:

- Charged in full to each standalone arm for the comparison.
- Counted exactly once in the whole-pair measured total.
- Reported separately alongside each arm's incremental known CPU.

Charging the same common term to both arms preserves the exact no-regression
comparison algebraically. It avoids repeating preparation only to manufacture
two timing observations. The outer Run-V5-Check report owns Python startup,
its own validation/snapshotting and final report/exit tails; final outcome audit
must include it in whole-operation cost without adding nested Job totals again.
One-time guest/host build and assembly costs are excluded from the execution
screen but explicitly remain required for any subsequent investment pricing.

Capsules and segment files are retained and checked, not certificates. A final
sampled424MiB/1024-entry output census is not a hard disk quota. Failed partial
outputs and charges remain; a failed arm stops the pair with no retry. Each
Job must close with zero active/limit-terminated processes and no cleanup errors.

## Exact prospective screen and outputs

After both endpoints pass, require all three unchanged conditions:

1. `4 * restricted.padded_rows <= 3 * general.padded_rows`.
2. `restricted.segment_count <= 64`, with every segment at most po18.
3. Restricted preparation-plus-execution known CPU is no greater than general.

Common costs cancel only because they are explicitly equal and fully charged
to both standalone comparisons. This is a single fixed-order engineering
investment screen, not statistical timing significance or full-cost growth.

The final report schema is `DMKN_RC_MATCHED_EXECUTION_RESULT_V1`. Status is
`PASS_RC_INVESTMENT_SCREEN` only when both endpoints and all thresholds pass;
`FAIL_RC_INVESTMENT_SCREEN` means completed matched endpoints did not meet the
investment rule. Input, execution or finalization failure is separate FAIL.
Only the PASS status exits0. A failed threshold is never relaxed after observing
the results and does not authorize a proof or another attempt.

`pair/` holds configuration, inert derivation, general/restricted arm directories
and RESULT.json. Each arm retains wire/header, host command/log/Job record,
diagnostic, capsule, segments and arm-result.json. No full-v5, certificate,
independent-host or population-growth claim is emitted.

## Selector source and runtime closure

The sixteen-source selection comprises Run-V5-Check and these fifteen v5 files:

- restricted_composition: matched_pair.py, prepare_execution.py, fixtures.py,
  run_controls.py.
- aggregate_claims: __init__.py, input.py, bindings.py.
- admission: __init__.py, bindings.py.
- modules: __init__.py, codec.py, model.py, native_rows.py.
- modules/receipt: __init__.py, witness.py.

Exact source paths, relative to the canonical project root:

```text
tools/Run-V5-Check.py
software/v5/restricted_composition/matched_pair.py
software/v5/restricted_composition/prepare_execution.py
software/v5/restricted_composition/fixtures.py
software/v5/restricted_composition/run_controls.py
software/v5/aggregate_claims/__init__.py
software/v5/aggregate_claims/input.py
software/v5/aggregate_claims/bindings.py
software/v5/admission/__init__.py
software/v5/admission/bindings.py
software/v5/modules/__init__.py
software/v5/modules/codec.py
software/v5/modules/model.py
software/v5/modules/native_rows.py
software/v5/modules/receipt/__init__.py
software/v5/modules/receipt/witness.py
```

There are23 named file pins in the config: fixture, receipt, three controls
records, and nine records for each arm. Together with the config itself,
two executable pins and two assembled-image pins taken from those records,
and four retained-supervisor files, the adapter binds32 distinct data/runtime
files. The root also supplies its established Python/runtime basis. Exact
record filenames (roots as in the table above) are:

```text
controls.result       restricted-composition-controls-01/evidence/result.json
controls.outer        restricted-composition-controls-01/RESULT.json
controls.selection    restricted-composition-controls-01-selection.json
*.host_build.result       <host-root>/RESULT.json
*.host_build.attempt      <host-root>-attempt.json
*.host_build.selection    <host-root>-selection.json
*.host_build.source_map   <host-root>/source-map.json
*.host_build.command      <host-root>/compile-command.json
*.assembly.result         <assembly-root>/assembly/RESULT.json
*.assembly.outer          <assembly-root>/RESULT.json
*.assembly.guest_result   <guest-root>/RESULT.json
*.assembly.guest_attempt  <guest-root>-attempt.json
```

Actual executable filenames are `small_aggregate_host.exe` and
`restricted_snapshot_host.exe`, respectively, inside their host-build roots.
Each image is `<assembly-root>/assembly/aggregate_image.bin`. The retained
supervisor files, relative to `product-local/v4-library-commons-02/commons-v4`,
are `RELEASE-MANIFEST.json`, `operator/commons.py`,
`receiver/helpers/domains.py`, and `receiver/helpers/run_stage.py`.

Runtime pins must cover the config and all its named records, both actual host
executables and assembled images, the parent receipt, controls fixture, retained
v4 supervisor manifest/operator/Job/domain helpers and the pinned Python runtime.
The adapter discovers no network or compiler dependency tree. Root's usual
runtime basis can be reused; no SDK installation copy or compiler library map
is required to execute the hosts. Independent source review remains pending.

Final source SHA-256 after root's guest03 interface confirmation:
`6deb0711c94fb6baba44e17a216befcd2ff8e945ede64148f7f7d54e0e241af6`.
This author has performed source reading and byte hashing only, not a syntax
parse, import, preparer call or runtime trial. Any later change requires the
root selector to bind the changed source, not this previous digest.
