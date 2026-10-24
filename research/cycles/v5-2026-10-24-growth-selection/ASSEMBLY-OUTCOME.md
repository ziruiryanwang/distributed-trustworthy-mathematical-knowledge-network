# Actual native-first assembly outcome

2026-10-24. growth_boundary_review. **PASS: exact file assembly, expected pin
refusal, and actual support-loader compatibility.** This independent review reads
only the saved run and current selected file identities; it reruns no recipe,
loader, producer, checker, owner or experiment. No product/state/Git mutation.

Run: `experiments/v5-local-checks/ordinary-native-assembly-01`.
The preceding ASSEMBLY-REVIEW covers the exact changed source. All old native,
intake, original-reference and producer experiments remain unchanged.

## Bound saved evidence

| File under the run | SHA-256 |
|---|---|
| selection.json | `b0459939a3342e9b83f57029210e084184f12436343f7065de3c215bce004701` |
| RESULT.json | `ecb36ef602c6fccaba78d61dfeb1506cc0405cb8fca39c5db0a9eb01d06d2f6a` |
| CHECK.json | `0979f8401867d9fa6e475b2a8e8a6dbf1b80112c72add3641ca23b406f266c36` |
| package/PROFILE.json | `47b80c6250886c4df71525d2600f02518d5400f260a8b60c0d77afd5ccbc5ac6` |
| package/ASSEMBLY.json | `7f22a17a90f647bb21a3745d136d8ada933225f9cfc44efc692964b11df98946` |

RESULT binds the actual selection hash above. Its argv and command/command.json
select the source snapshot, reviewed assembler/map/profile hashes, adopted preview
base, retained exporter and exact supplied runtimes. No alternate source or old
reference assembly is silently substituted.

## Actual output and source correspondence

Independent read-only hash/census checks found no discrepancy:

- All 141 package payloads match ASSEMBLY's byte lengths and hashes.
- The actual package has exactly 143 files: those payloads plus PROFILE and
  ASSEMBLY. There is no extra file, pending profile or failure marker.
- All 111 profiled roles agree with the actual payload map.
- Reconstructing the base map from its profile/installation gives 134 payloads.
  The exact successor delta is 132 unchanged, owner.py/profile.py replaced,
  five support roles added, plus README.md and PRODUCER.md.
- The five support additions are baseline_production.py, baseline_worker.py,
  baseline_bundle.py, baseline_intake.py and the retained BaselineExporter.exe.
  `reference/` contains only its two baseline Python controllers. There are no
  original-reference matchers, registrations, authoring helpers or native helpers.
- All 157 selected external input hashes match the retained selection, including
  the base payloads, installation, named runtimes, exporter and selected sources.
- All 13 source-snapshot files match their selection hashes and corresponding
  current repository files. The snapshot file count is exactly 13.

The complete copied payload size is 38,957,596 bytes. The installation manifest
remains `32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`;
implementation remains `fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df`.
This is identity/preservation evidence, not a new mathematical judgment.

## Three actual control results

1. **Wrong map:** subprocess exit 1, empty stdout, and saved stderr ends with
   `NATIVE_ASSEMBLY_INPUT_PIN:` followed by the exact snapshot source-map path.
   The wrong-map output directory does not exist. This is the intended pre-copy
   rejection, not an unrelated startup failure or later timeout.
2. **File assembly:** subprocess exit 0; assembly stderr is empty. The actual
   maps/census above support the returned `ASSEMBLED_NOT_ADOPTED` result.
3. **Support loading:** CHECK records `PASS_FILE_ASSEMBLY_REFUSAL_AND_SUPPORT_LOAD`,
   actual-profile-load with the computed PROFILE hash and 111 roles. Its pinned
   harness calls the real public loader, including the exact baseline role/module
   identity checks. It does not open mathematical owner state or launch Lean.

There was one selected run and no automatic retry. The reviewed harness follows
the negative control with its separate positive operation, not a retry of failed
assembly with altered inputs or a resumed partial destination.

## Resource and closure evidence

The aggregate Job used the selected limits: 120 wall seconds, 80 CPU seconds,
512 MiB, three active processes, and 1 MiB each outer stdout/stderr allowance.
RESULT reports `COMMAND_EXITED_ZERO_AND_CLOSED`, direct child reaped, Job closed,
zero active processes, no cleanup errors and no termination request.

Actual total wrapper-observed wall time was **7.138351900037378 seconds**.
Final Job user+kernel CPU was **3.140625 seconds**; outer wrapper CPU was
**0.796875 seconds**, giving **3.9375 known inclusive CPU seconds**. Do not add
the nested supervision or harness observations again. Harness CPU alone is not
the total. Peak aggregate private commit was 32,768,000 bytes (31.25 MiB).

The report's six total processes is a cumulative count, not six concurrent
processes; the selected limit is three active processes. The final count is zero,
with zero terminated processes. Outer logs are 444 stdout bytes and zero stderr
bytes. Inner saved negative traceback is intentionally retained separately.

## What this closes, and what it does not

This closes the selected distribution dependency and changed loader boundary.
The supported native-first facade can now be assembled without the historical
original-reference package chain, from explicit adopted inputs, while retaining
the existing producer/intake and optional ordinary interfaces.

It does not check new mathematics, execute the entire producer/intake loop,
qualify original-library registration, migrate anchors, produce a certificate,
establish source-to-native reproducibility, supply a hostile-source sandbox,
demonstrate useful growth or complete final v5. The package's already reviewed
owner/profile identities create the stated new support version. Existing anchors
and accepted state remain attached to their old supported packages.

No further run is recommended by this outcome. Preserve the run, its snapshots
and selected source bytes. Next work returns to the concrete growth/default
architecture decision rather than repeating a passing package or theorem fixture.
