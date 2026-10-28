# Focused controls for the ordinary contribution handoff

2026-10-28. Source-only candidate; root selects execution separately. These
controls exercise the new inert projection boundary, not the already tested host
lifecycle or Lean production. No experiment has run under this plan.

## Selected inputs and invocation

Use the real current package PROFILE
`e8d33500db4c0a5ce89b2dfb51c3e1f9ec8f12063bbc58fe5e4eb23c2b6dfb13`.
The package is a root-selected absolute path. Do not synthesize a five-codec
PROFILE: three installation codecs are bound through the installation manifest;
the helper authenticates their fixed bytes directly. The remaining two codec
roles occur directly in PROFILE.files.

The selected helper candidate is `project.py`, SHA-256
`4ca7fe20e85b75e07ef72e74dc761e7ace4aaff7a93bb444444b57e5ed401ac5`.
Root must independently pin both helper and control source before execution.
Invoke `control_tests.py` through the selected isolated Python with
`-I -S -B`, passing `--package`, `--profile-sha256`, `--project`,
`--project-sha256` and a fresh `--output` beneath
`experiments/v5-local-checks`. The root-selected outer process Job must impose
finite process, wall, CPU and memory bounds. The runner has an additional
cooperative 120-second wall / 60-second CPU ceiling; each helper invocation
retains its own 60-second wall / 30-second CPU ceiling. Cooperative checks alone
are not OS containment.

Fixtures are exactly those in [HANDOFF-FIXTURES](../ordinary_incremental_host/HANDOFF-FIXTURES.md):

- `finite-map-refinement-contribution02/contribution/RESULT.json`, SHA-256
  `37ea97b2c006b216782e7a53142ed741a53a26a86a3b89ded9252dae1279b9b0`;
  its public wrapper, SHA-256
  `06534e767bf4a04de3f2e2b4ec26d4aeb5872bfe8059a2b4a1e015763ee0bebb`.
  Preserve all 21 units / 379,701 evidence bytes, including 10 support-only units,
  and the original 11 targets.
- `ordinary-project-extraction-public-01/project/completion/RESULT.json`, SHA-256
  `d031230312290008c5b09bb0587615d9a02310b4cfdc014ccbee2b491477d298`;
  its public wrapper, SHA-256
  `b8f768361cc1378da6cb659a5e426f2721790eccd737285c6cb382424fb31e94`.
  Preserve all three units / 10,700 evidence bytes, with two support units before
  the one selected target unit.

Both prefixes are beneath `experiments/v5-local-checks`. Every original evidence
row is rehashed against its pinned report before copies are made. Originals are
read-only; all modified metadata and evidence go to fresh control directories.

## Eight finite groups

1. Real contribution wrapper through the public CLI function. Assert exact unit
   bytes, supplied order, support retention, target bindings and output census.
2. Real completion helper result through the API. Assert supplement-before-consumer
   order and all original targets without manufacturing support-unit targets.
3. Wrapper with `ok:false`, a different historical profile and malicious old
   relative `file` fields. Explicit relocated evidence must work; source claims
   remain provenance and all mathematical acceptance/publication flags remain false.
4. Incorrect report and selected-profile pins must refuse before creating output.
5. Incorrect evidence hash, target hash, actual target membership, status,
   duplicate unit/target, 33-unit/target counts, per-unit/aggregate byte caps and
   semantic identity must refuse. The membership case assigns the target name to
   a different supplied support unit and recomputes a consistent ExportID, so a
   hash-derivation-only check cannot pass it. Aggregate cap is crossed by declared
   size before reading a deliberately undersized second file.
6. A missing relocated unit must refuse without consulting its historical path.
7. Invalid evidence schema with a corrected raw byte/hash pin must be rejected
   by the actual portable codec, rather than by a stale byte pin.
8. Missing disclosure/partial-publication approvals, overlapping output and an
   existing empty output must refuse. Existing output must remain empty.

The successful outputs are separately read through the unchanged baseline bundle
parser and batch validator, with exact order and emitted bytes compared against
the real fixtures. Append config fields match the unchanged host input contract.
This validates that format boundary without opening a host or database.

## Effects, result and limits

During each projection, an audit hook allows reads only of its selected report,
relocated evidence filenames, PROFILE, five fixed codecs and new output. It
rejects input-directory enumeration, unrelated reads, output-external writes,
SQLite connection, subprocess creation and socket connect/bind. This is harness
instrumentation, not a general security sandbox. Fixture setup and unchanged-codec
output validation run outside that hook; their source is included in review.
Temporary codec import slots must be restored on success and refusal. All inputs
and selected source pins are checked again at completion.

The runner saves `RESULT.json` with group outcomes, selected pins, elapsed wall
and harness CPU, and declared zero owner/native/database/network calls after a
pass. All partial files and refusal cases remain for inspection; no cleanup,
retry, prior-state recovery or original evidence rewrite occurs. Any failure
stops the one campaign and requires diagnosis before a new root selection.

A pass supports inert preparation from these genuine contribution/completion
outputs and the stated refusals. It does not establish mathematical truth,
dependency closure, host publication, independent-host operation, general
scalability or useful mathematical growth. Do not rerun host service or Lean to
upgrade this bounded claim.
