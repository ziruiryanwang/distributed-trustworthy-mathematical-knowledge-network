# Source-package contracts: independent source and launch review

2026-09-21. **SOURCE AND EXACT LAUNCH PASS.** No concrete blocker was found for
one root-controlled execution of the selected fresh allocation. This is a
pre-execution review, not an observed test result or release qualification.

The reviewer fully read the packager, ten-test suite, reusable runner, exact
launch, implementation handoff and prior packager source review. Checks used
read-only PowerShell content/path/hash operations. No imports, AST parsing,
Python/product execution, fixture creation, ZIP operation, native tool or network
operation was performed. This review is the reviewer's sole write.

## Selected cut and exact launch

| File relative to `software` | Bytes | SHA-256 |
| --- | ---: | --- |
| `release/package_source.py` | 14,011 | `8062FE2B4D9CC75279F512FC288727617CCC4017DEA1B74F5A1A10FD2286E837` |
| `tests/test_source_package.py` | 25,894 | `8B1CB07AA9FAB00F0DC1FED51662B948DC354003246C483FA9C089A9AFC1029B` |
| `tests/run_state_contracts.py` | 12,795 | `404AC805BF1F7146F152EAD2E50262910C5477301984862939F2966051884BB7` |
| `qualification/source-package-contract-launch-01.json` | 1,938 | `BF27B1972AB12CFB10D75356DB194E6923C361983685A4D5D8C32047FCB13F8F` |

All seven launch inputs independently match their current bytes and SHA-256,
in the runner's exact order: selected Python executable, runner, `run_stage.py`,
`supervise.py`, `domains.py`, builder and suite. The launch is the eighth
supervisor pin. The runner's limits are exactly 60 wall seconds, 30 Job CPU
seconds, 512 MiB, eight active processes and 65,536 bytes for each output/event;
the retained endpoint is 256 MiB, 4,096 files and 8,192 entries.

Removing the new 305-character source-package registry entry produces the
retained `replica-custody-contract-01/sources/run_state_contracts.py` exactly;
there is no other runner delta. The new entry selects exactly ten methods, the
`source-package-contract` allocation prefix and only the builder as its
suite-specific source. At review, both `software/qualification/source-package-contract-01`
and `product-local/source-package-contract-01` are absent. Their parents exist;
selected input ancestry has no observed reparse point. Runtime preflight must
still recheck all pins and fresh allocation conditions immediately before use.

## Contract assessment

- Exactly ten `test_` methods exist. The fixture vocabulary is separately listed:
  108 selected payloads, an 81-row lock including 75 assets, and 109 ZIP members
  after the embedded manifest is added. Actual builder helpers package, read and
  repackage these inert bytes. Deterministic outputs, member hashes, external
  manifest/result bindings and ZIP metadata are independently asserted.
- Missing/extra selected trees, malformed lock paths/types/duplicates, incorrect
  content pins and ambiguous quickstart placement have discriminating refusal
  assertions. Excluded runtime/state/test/draft sentinels remain outside the ZIP.
- The byte-bound test uses actual 2-MiB and 2-MiB-plus-one inputs and nine unlocked
  selected 2-MiB files. It crosses the actual 16-MiB aggregate bound with a valid
  lock; limits are not replaced with smaller test constants.
- Namespace/root/traversal/ADS/reserved-component checks call the real path guard.
  Reparse attributes and canonical-parent aliasing are explicitly mocked and do
  not qualify real Windows junction/alias behavior. Main argument/refusal paths
  are exercised in-process; fixture `__file__` substitution does not establish
  authentic public CLI execution or entrypoint provenance.
- Change/corruption hooks really modify only freshly owned test files. Original
  README/ZIP bytes are retained first. Source revalidation and unexpected-member
  detection must preserve failed output and omit the success marker. The ZIP
  mutation is a valid extra member, not CRC damage or torn-write coverage. No
  historical file is mutated or deleted and no retry allocation is used.
- All fixture paths originate below a fresh suite root in the external runner
  state directory. Each method retains its bounded census/report. Fixed fixture
  construction fits the declared endpoint by inspection; actual complete census,
  elapsed time, Job CPU and clean process-tree quiescence remain run-time gates,
  not findings established by this source review.

The suite imports only the exact hash-bound packager and standard library. Its
tearDown also rejects loaded modules beneath the product `py` directory. The
separate coordinator retains its already-selected supervision imports; these are
not executed as product/node operations by the test worker. There is no test
subprocess, Lean execution, socket, database, installation or external mutation.

An audited pass would establish these narrow synthetic packaging contracts only.
Actual-source packaging, authentic CLI use, extraction/build/operator usability,
mathematical acceptance, independent-host replication and useful growth remain
separate evidence requirements. No product readiness conclusion follows here.

## Addendum: actual-source package plan preflight

**PLAN PASS**, still not an execution result. The separately selected
`qualification/source-package-plan-01.json` is 42,712 bytes, SHA-256
`79A7AA7191C8AB34567322D82A3B7A87936B7A118695F9CC32A800DA81F4CB0C`.
Its 108 rows match an independently reconstructed builder selection in exact
ordinal order. Every current path, byte count and hash matches; their sum is
3,555,524 bytes and maximum input is 823,690 bytes. The 81 lock rows agree with
selected rows, and actual `py`, `native` and `assets` file sets have no missing or
extra file. The sole quickstart is the mapped draft; the top-level alternative
is absent. No selected input ancestor has an observed reparse point.

The argv is the ordinary authentic selected builder CLI with the selected
`D:\Python314\python.exe`, `-B -E -s -S`, absolute source and absolute output.
The runtime hash remains the independently checked launch value above. The
planned output `product-local/source-package-01` is absent with an existing
ordinary parent, disjoint from `software`; no output was created by this review.
This plan calls the real entrypoint, unlike the synthetic suite's origin mocks.

The builder's 2-MiB input, 16-MiB aggregate and 18-MiB archive bounds are source
guards, not OS process/transient-disk quotas. The plan's 24-MiB/four-file retained
endpoint must be checked against actual output. Elapsed observation is not a
separate enforced wall/CPU/Job budget. One attempt only; retain partial output on
failure. Root must recheck selected bytes/freshness before launching, then bind
the actual archive/manifest/result to these rows. No release, public deployment,
runtime inclusion or mathematical-acceptance claim is authorized by this gate.

## Execution finding: contract 01 failed; prior actual-source gate withdrawn

The first allocation completed with three errors and five failure records across
seven of ten methods. Every recorded error/failure originates in
`FILE_CHANGED_BEFORE_READ`; see its retained `OUTCOME.md` and diagnostic. The
pre-execution review missed that the selected Windows runtime's `lstat`/`fstat`
ctime values can differ on an unchanged file. No actual-source output exists.
The plan 01 PASS above is historical and **is no longer an executable gate**.
It binds the old builder and must be replaced by a fresh exact plan after the
correction is qualified. Contract allocation 01 remains failed permanently.

**CORRECTION SOURCE PASS**, not an execution result: current builder is 14,422
bytes, SHA-256
`8E180422926D07A3C41F4F6A47BDEE2FC8B6A7BCD4788076B2761B8DC40795E1`.
Independent reconstruction against the retained failed-cut builder establishes
that its complete delta is the split-stamp correction. `binding_stamp` compares
device/inode/size/mtime/birthtime/attributes/mode across path/handle APIs;
`stamp` adds ctime for same-API comparisons. The opened handle's full stamp is
compared before/after reading; the path's full stamp is compared before/after
the handle lifetime. Final byte comparison and later source revalidation remain
unchanged. The correction does not simply discard ctime monitoring and does not
claim atomic hostile-filesystem isolation.

The additional method-06 source was read: it keeps the real 2-MiB boundary read,
then mocks stable cross-API ctime disagreement (must accept), handle identity
disagreement (must refuse before read), changing handle ctime (must refuse during
read) and changing path ctime (must refuse after read). Existing real size bounds
remain unchanged. These injected guards complement, rather than replace, the
actual-runtime positive read. This addendum does not select the next suite or
launch hash; root must freeze and independently check the next exact allocation.

## Corrected contract 02 exact-launch gate

**SOURCE DELTA AND EXACT LAUNCH PASS**, not an observed result. The corrected
suite is 27,703 bytes, SHA-256
`AA34BE1E5120A8CCB7C486863A6D1B2E76BCAE3D140DFEA7AFE311245C00AA6B`.
Reversing its 1,809-character method-06 insertion and two builder-pin replacements
exactly reproduces the retained failed-cut suite. Ten methods remain; method 09
is unchanged and still detects its actual README change by comparing newly read
bytes/full path observation with the initial capture. Its refusal is not weakened
by the cross-API comparison correction.

The updated release README, 8,476 bytes and SHA-256
`CBD17FA97B8CF6C3AEBAF0D593E10233ED75A058D6CCDD06C8FCABD6A9B92EB8`,
was read completely. It accurately explains split-API ctime handling and preserves
the cooperative-filesystem/non-atomic/non-release boundaries.

Launch `qualification/source-package-contract-launch-02.json` binds the unchanged
runner, selected runtime/supervision modules and corrected builder/suite in seven
ordered input rows, plus itself as the eighth supervisor pin. All current bytes
and hashes match. Limits/retained endpoint are unchanged from contract 01; both
allocation-02 roots are absent at this check. Root may execute this new allocation
once after immediate freshness/pin recheck; allocation 01 must never be reused.

## Corrected actual-source plan 02 preflight

**PLAN SOURCE PASS, conditional on contract-02 outcome audit.** The replacement
`qualification/source-package-plan-02.json` is 42,839 bytes, SHA-256
`967B13D17548E59B0B6E7BC4C99F595B94C36F6BFAF3D52B1CC764BC02002004`.
All 108 current paths/sizes/hashes were independently checked again. Exact
selection/order is unchanged, and only the reviewed builder and release README
rows differ from unexecuted plan 01. Sum is now **3,556,230 bytes**. Selected tree
file sets remain exact; the alternate quickstart and planned output are absent.
The command and resource/retention scope are unchanged. The output name remains
`source-package-01` because no actual-source packaging attempt has yet occurred;
this is not reuse of a failed allocation. Successful corrected contract evidence
and immediate fresh-source/pin checks are required before that one CLI attempt.
