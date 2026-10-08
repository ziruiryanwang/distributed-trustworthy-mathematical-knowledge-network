# Fresh diagnostic profile: independent source review

2026-09-21. **PASS for the selected source-only diagnostic delta.** No material
blocker found. Root must still review the exact freshly installed cut, generated
configuration and prospective allocation before running it. This is not runtime
qualification, a performance finding or mathematical acceptance.

Reviewed completely:

- `PROFILE-NODE-IMPLEMENTATION.patch`: 6,750 bytes; SHA-256
  `6C3916F4304E1BEBB18700A124EBF27547A8485A205E4C6D0A81544CAD066462`.
- `PROFILE-NODE-IMPLEMENTATION.md`: 2,333 bytes; SHA-256
  `248AACD41A3D80A9F70FFF1643FC7DAB5366C1051582E12A95D52E358B2A48E3`.
- `PERFORMANCE-PROFILE-RECIPE.md`: 4,941 bytes; SHA-256
  `E607E366DE3E470E94F6384F9E68BF709E2810033221A26AEDC68F4027028EA7`.
- Base `software/py/node.py`: 25,402 bytes; SHA-256
  `635847507F823EF71358B0D619935B5581D2EA64C805FD4DB2162F0297D40866`.

All four patch hunk counts and old lines match that base. The delta activates
only for ordinary submit, request ID `profile-target-001`, root
`ChunkedReductionStatement`, and the exact 643-byte UTF-8 source hash. It does
not introduce a general public profiling option.

Profiler creation follows `ControlStore` construction. Profiling encloses
dispatcher construction/execute and stops in `finally` before normal store
closure. Existing dispatcher, exception handling, event/response serialization,
stdout and acceptance behavior are unchanged apart from diagnostic overhead
consuming the same resource limits. Both construction and enable explicitly
disable subcall graphs. `time.process_time` measures this process, not child
CPU; scope readings include instrumentation overhead and are not optimized
timings or whole-request cost.

Export occurs only after the normal event and stdout response are emitted. The
exclusive-create sidecar is beside the validated scratch event and binds
request, response, source and diagnostic-node hashes. Historical replay cannot
produce a fresh profile. Export processes at most 10,000 collected entries,
selects at most 60 top-exclusive/top-cumulative rows, bounds labels and requires
the complete JSON to fit 65,536 bytes. No caller graph or binary dump is written.
Collection memory remains subject to the public Job limit; the entry-count
check is not a hard pre-collection memory quota.

Ordinary diagnostic start/stop/export exceptions are caught without replacing
the request reply; unavailable export emits at most 512 stderr bytes and leaves
any partial file retained. Resource exhaustion or process termination can still
fail the overall request: profiling is not promised to be behaviorally free.
The existing supervisor does not pin this extra sidecar; root must authenticate
and census it separately. Neither a sidecar nor its absence changes acceptance.

The selected final recipe supersedes its earlier vocabulary-only proposal:
fresh installation, four ordinary vocabulary-onboarding requests, then one
target-definition submit; five requests, four stages, 552 MiB, no target
publication, retries, source repair or consumer dispatch.

The 643-byte `UsefulnessTargetStatement.lean` source was read and its SHA-256
verified as `2C1F0832C82E73423D212CA5782CA28EE4088D6EC4C53C4D72F8726E3F76570E`.
It defines the proposition that folding flattened chunks equals folding their
individual folds under the stated algebraic assumptions. It contains no proof
of that proposition. Frontend/canonical representability remains an actual
execution question; acceptance of the definition cannot count as solving the
consumer target.

Reviewer coordinated the stable cut directly with the author. No patch was
applied by the reviewer, and no product import, Python, Lean, test or public CLI
was executed. Inspection was read-only PowerShell/.NET plus this Markdown note.

## Exact fresh target-profile01 launch addendum

Before the first build, the reviewer completely read the selected observer and
plan and issued **PASS for the fixed fail-stop launch sequence**:

- `qualification/target-profile-01/observe.ps1`: 13,268 bytes; SHA-256
  `F2AE6908165715FE5033D0C30C23A652E0D35097D0030AA2A6C7258AC526D5F2`.
- `qualification/target-profile-01/PLAN.md`: 4,331 bytes; SHA-256
  `3A48036DA1FFBF61DA2D22B0039D652DA3185381FAF8A49EDE1B283C6EC518A3`.
- Fresh installed diagnostic `py/node.py`: 31,315 bytes; SHA-256
  `59C0C0D9CACA7295713167DD1FE379FB30A44A263F1B036CD5EEFA39DC8EB8C1`.

An in-memory line reconstruction of the reviewed patch matched all 566 installed
node lines exactly. All 108 archive-manifest payloads were authenticated, using
only that explicit node override; the fresh installation contained exactly 109
files including the unchanged base manifest. Support-work, state, scratch and
request directories were absent at inspection. The base manifest is not an
assertion that the diagnostic installation is an unmodified release.

The observer pins source/runtime cuts, separately checks the support build,
uses synchronous exit-code collection, response-bound ordinary requests and
public quiescence gates, and requires exact vocabulary reproduction before the
single target submit. No target publication is selected. Its endpoint census
is not a transient quota, and it has no enclosing aggregate Job. Final complete
installation-set checks, diagnostic-sidecar pins, resource/state reconciliation
and canonical target-value inspection remain separate outcome obligations.
The final reporter is separately reviewed, not included in this clearance.

## Separate final reporter review

The reviewer subsequently read all of `qualification/target-profile-01/finish.py`
and issued **PASS for root-only use after the selected sequence is quiescent**:
16,336 bytes, SHA-256
`9900F9E3054467466230287110A964CCAC711B572CDC699052B0F14BB2D05683`.
Its actual build/node/supervisor field expectations match installed sources.
It authenticates the complete installation map before importing `storage` and
again after its owner-locked, bounded read-only database projection; the
database hash must remain unchanged. It independently binds and bounds the
profile sidecar and keeps diagnostic failure separate from ordinary results.
Invalid/missing profiling yields a retained failure result, not borrowed
acceptance. Complete data/evidence census and disjoint build/public accounting
remain explicit. The reporter does not itself require exactly one sidecar
throughout scratch/calls; that finite-set check is assigned to the independent
operational outcome audit. No source change or execution was performed by this
reviewer.
