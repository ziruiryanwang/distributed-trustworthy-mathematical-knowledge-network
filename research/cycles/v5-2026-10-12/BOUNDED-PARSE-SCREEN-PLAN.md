# One new image, one unchanged-cap execution screen

2026-10-12. Root-assigned source work. The unused assembly adapter is now aligned
to the fresh **three-project direct build**, not the failed resolver build02.
No assembly, guest execution or proof is selected by this note. The full v5 goal
remains active. Preserve every used source and all failed predecessor records.

## Current direct-build alignment

Root authorized adapting only unused `bounded_parse_guest/assemble.py` after
source inspection of `build_projects.py` / `recipes.py`. The accepted prospective
input is now `bounded-parse-direct-build-01/RESULT.json` with
`DMKN_V5_BOUNDED_PARSE_DIRECT_PROJECT_BUILD_RESULT_V1` and
`PASS_BOUNDED_PARSE_THREE_PROJECT_COMPILES_ONLY`. No successful outcome is assumed.

The prerequisite is one actually successful, independently adopted new operation:
three completed rustc commands named `module`, `aggregate`, `guest`; exactly
three compiler calls; zero Cargo/graph/dependency/checker/guest/proof/assembly/
network calls; clean quiescent final Job within its recorded limits; matching
terminal attempt; no overriding failure marker in the **new** direct-build run.
The adapter binds its source/map/recipes/retained-graph records and exact user
ELF/link map before and after one retained-assembler invocation. It does not
repeat compilation or the retained SDK/dependency-tree census.

The old `bounded-parse-guest-build-02` outcome is explicitly **FAIL_FINALIZATION**,
not successful-build authority. Its pinned RESULT is
`792ed5825ae3110dc3ddc1a85b49636b63469f5e4cb1d662e70d8ddf27d6b4b6`;
its overriding marker is
`36c6f5c6b7084dbb08d461c008ea8b39e71e80bf95cc90860e455936b637cf55`.
The new builder separately selects its exact 39-file source snapshot and retained
297-unit graph, then compiles three projects into a new directory. Reusing these
identified inputs does not promote the failed operation or its old ELF. The
assembler verifies this preserved failure lineage and refuses build02 directly.

## Decision

Only **one fresh thin assembly adapter** is necessary. Reuse the existing
`software/v5/aggregate_host/snapshot.py` unchanged with a fresh configuration,
and reuse its exact existing `aggregate_host.exe`. Do not rebuild the host or
change the mathematical workload to accommodate the new guest.

The new guest is the reviewed bounded-parse optimization of the same relation.
Its exact graph/build must first finish, be independently audited and adopted.
A resulting ELF is not an adopted execution image, receipt or evidence of gain.

| Existing piece inspected | Reuse decision |
|---|---|
| `aggregate_guest/assemble.py` | Cannot accept the new build by configuration: hard-pins old compile/result/failed-finalization/revalidation lineage and exact old ELF path. Leave unchanged. |
| `modules/receipt/assemble_guest.py` | Also not configuration-compatible: checks module-build status/name and module ELF. Its short assembly pattern is reusable source material, not a callable new-build adapter. |
| `aggregate_host/snapshot.py` | Already takes selected assembly RESULT hash, A and fresh output. Its workload, real I premise, cap and host remain exactly reusable. |
| `aggregate_host/aggregate_host.rs` and existing executable | Independently compute actual image ID, derive exact conditional H from WIRE, verify typed parents, execute once and require exact successful H. A is an explicit argument, not hardcoded. No host rebuild required. |

The old native host remains a conservative preflight for this same-format input.
The adopted bounded-parse native comparison already preserves both complete
retained conclusions. This does not prove all-program equivalence; actual new
guest execution must still produce exact expected H. Do not interpret old host
bytes as executing the old guest: the guest is the separately selected new image.

## Fresh adapter: exact proposed source/API

Proposed sole new implementation file:
`software/v5/bounded_parse_guest/assemble.py`.

Proposed entry point, run only from an exact source snapshot inside a separately
selected `Run-V5-Check.py` Job:

```text
python.exe -I -S -B <snapshot>/software/v5/bounded_parse_guest/assemble.py
  --guest-result <new-build>/RESULT.json
  --guest-result-sha256 <independently-adopted-result-hash>
  --output <fresh-local-assembly-directory>
```

The adapter uses ordinary absolute paths and fresh-exclusive output. It performs
one existing assembler invocation, no compiler/graph/native/guest/prover call.
It does not import the build controller or instantiate its build workflow.

Required input contract:

1. `<new-build>` is exactly the canonical local-check directory named
   `bounded-parse-direct-build-01`. RESULT has schema
   `DMKN_V5_BOUNDED_PARSE_DIRECT_PROJECT_BUILD_RESULT_V1`, status
   `PASS_BOUNDED_PARSE_THREE_PROJECT_COMPILES_ONLY`, exactly three compiler calls,
   zero Cargo/graph/dependency/checker/guest/proof/image-assembly/network calls,
   and a closed quiescent Job with no terminated child. Its exact
   terminal attempt agrees with RESULT's hash and success status, and no
   overriding `FINALIZATION-FAILED.json` exists. Require exactly the two
   project-library compiles `module`, `aggregate`, then one `guest` compile:
   three successful closed commands in total, matching recorded recipe argv.
2. Pin the saved selection to RESULT's `selection_sha256`. Require its expected
   build schema `DMKN_V5_BOUNDED_PARSE_DIRECT_PROJECT_BUILD_V1`, name, two exact
   adapter keys and explicit retained-artifact/three-compile authorization.
   Pin small `ARTIFACT.json`, `GRAPH-COMPARISON.json`, `SOURCE-MAP.json`,
   `INPUT-MAP.json`, `RECIPES.json` and the exact retained graph/source records.
   Artifact must equal RESULT's artifact; graph is an explicit retained graph
   projection, not a claim of new Cargo execution. Rebind the 39 actual project
   snapshot files and two selected adapters to both source and input maps.
   Root's independent adoption remains responsible for the complete actual
   build/source/resource audit; this adapter does not repeat the copied library
   or SDK census. Retained input record lists exactly 238 library/macro artifacts.
3. Exact user ELF path is `<new-build>/outputs/dmkn-aggregate-claim-guest`.
   Check current length/hash against adopted artifact and outputs records and
   the final recipe destination; separately pin its recorded link map. Do not
   synthesize an artifact from a nominal success string or consume an old failed
   build's ELF. Preserve the pinned old failure and override in new provenance.
4. Reuse the exact already qualified assembler from
   `experiments/general-checker-guest-02/driver-build-04/RESULT.json`, whose hash is
   `d89626da253ade06a4482d6e7f4a7e9aac0f93d360a2eab2f1b39ba25cc8c43a`.
   Rebind its executable bytes and the same58,736-byte v1compat kernel with hash
   `9dd8af014a24db3752b9beda71c837f553ff361fc1bca83cc79584bd38ac9de5`.
5. Recheck selected records, absence of overriding failure, ELF, link map,
   assembler and kernel before and after the one call. Output image is fresh;
   parse the assembler's exact `COMBINED_IMAGE image_id=... bytes=...` record,
   bind actual output length/hash, and preserve stdout/stderr/argv and failures.
   The image ID comes from the pinned assembler, never the image file SHA-256.

Use a new inner result schema `DMKN_V5_BOUNDED_PARSE_IMAGE_ASSEMBLY_RESULT_V1`
with actual build/artifact/selection provenance and generic assembly fields:
`status=PASS_NEW_AGGREGATE_IMAGE_ASSEMBLY_ONLY`, `image`, `image_id`,
`image_id_origin`, `assembler_calls=1`, `guest_executions=0`, `proof_calls=0`,
`mathematical_admission=false`. This status describes the same assembly-only
capability consumed by existing snapshot.py; it does not pretend the old failed
compile/revalidation lineage occurred. Errors have an explicit failure status.

Existing snapshot.py checks these generic result fields, not an old schema name
or old artifact-validation hash. Its compatibility is therefore source-visible
without editing or falsifying an old result. Root must adopt the new inner AND
outer assembly outcome, not merely the new image ID. Same approach applies to
the later screen's inner and outer completion records.

## Unchanged execution screen

After successful adopted assembly, prepare a fresh configuration with the
existing five-field `DMKN_AGGREGATE_COST_SCREEN_V1` schema:

```text
schema, image_result, image_result_sha256, aggregate_image, output
```

Only the new result path/hash, resulting A and fresh output destination differ.
The existing controller source hash remains
`d99656a17891983e2ae5ee0afb78fd4695b0ac4746a58aade34977b36fd2f442`.
Use a fresh root selection and exact source snapshot; do not reuse an old run
directory or edit the previous configuration/selection.

The controller uses the original215,540-byte `actual-two-delta.bin` and native
conclusion, replacing only byte interval `[12,44)` in both wire and192-byte H
with the new32-byte A. Every member journal, edge, module, exact warrant, proof
body, Merkle path and foundation/policy byte outside that slot remains identical.
It binds all three members, maximum member rank2, seal height1 and the one
existing genuine I receipt. Receipt hash remains
`850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47`.

The one selected command remains:

```text
aggregate_host.exe snapshot NEW_A NEW_IMAGE WIRE H
  33554432 18 pc-samples FRESH_CAPSULE FRESH_DIAGNOSTIC 1 EXISTING_I_RECEIPT
```

That is the **same2^25 session cap**, same segment po2=18, same diagnostic mode,
same maximum128 segments and same existing host binary
`b1605995c957e06b7c4529d28dfc2a49e496cefae7629b3fdddfc4a1bfb6f6d1`.
The host checks the new image itself. No I proof is repeated, no old partial
segments reused, no proof production occurs, and no cap increase follows failure.

For the root's later runtime selection, retain the old screen's enclosing
180CPU/240wall/3072MiB/three-active-process limits,120-second subprocess timeout,
1MiB stdout/stderr ceilings and144MiB/160-entry output census. These are finite
ceilings, not predicted expenditure or an authority to launch. Assembly can use
a separately reviewed small allowance; its original outer120CPU/120wall/1024MiB/
two-active profile is already sufficient precedent, not a required minimum.

## Outcome and stop rule

- **Success:** one clean actual complete capsule and exact H, independently
  adopted with its bindings, actual segment counts, rows/padding, diagnostics,
  costs and output custody. This qualifies the new image's bounded execution
  feasibility on this retained fixture, not a certificate, useful-growth result
  or universal speedup. Next proof funding remains a separate decision.
- **Failure:** preserve exact failure, costs and diagnostic prefix. No automatic
  retry, larger cap or proof follows. Prefix segments are not a complete capsule.
  Analyze a decision-changing residual from retained evidence before any new work.
- Do not rerun the old image for comparison. Its2^25 failure is preserved.
  New completion within that cap can establish a threshold improvement on this
  fixture; old saturated sampling is not a complete timing/cycle baseline from
  which to invent a precise percentage gain.

No additional guest build, host build, changed mathematical workload, broad
network test or new benchmark suite is needed to make this one decision.

## Authorized source implementation checkpoint

Root approved the exact plan for source-only implementation. The sole fresh
`software/v5/bounded_parse_guest/assemble.py` now implements it; none of the five
guest-build files, existing snapshot controller, host or frozen records changed.
Its CLI is the proposed three arguments, accepted only from the owner's exact
source snapshot, with output fixed to that fresh Job directory's `assembly/`.

Preflight checks actual selected RESULT/selection/attempt/artifact/graph records,
three closed successful project commands, exact new ELF/map and the retained pinned
assembler/kernel. It rebinds this finite explicit set and absent failure marker
before and after the one call, including failure finalization. Direct-file logs
are retained on timeout/failure rather than held in an unbounded capture buffer;
the64KiB log limits are checked afterward, with the enclosing owner providing
aggregate runtime supervision. A post-call binding failure overrides an inner
success. Generic assembly-only fields preserve unchanged snapshot compatibility.

Historical context: the first new guest graph attempt failed before compilation because
an additional optional-resolution archive was needed. This adapter neither
accepts nor repairs that failure. The subsequent resolver build02 also failed
finalization; the current adapter accepts only a separately independently adopted
successful `bounded-parse-direct-build-01` outcome. No success is presumed,
no failing artifact is reclassified, and no run has been selected or performed
by this implementation lane. Source inspection is not runtime qualification.

### Historical resolver-successor contract alignment (superseded)

Root previously authorized adapting this still-unused assembler after inspecting the fresh
`build_resolver.py` source, initially hashed
`ad8182636c7b87a54bfcf41fbf66983a45f8aaf02f00c1010485d6d990651e8e`.
At that checkpoint RESULT and saved-selection required resolver-specific names,
and the only accepted build directory was02. PASS, two successful command
labels,297-unit graph conclusion and artifact/ELF/map layout remain unchanged.
The adapter additionally binds `CACHE-SELECTION.json` to RESULT's
`resolver_cache_selection` and carries the source-bound `predecessor_failure`
descriptor in its own report without rerunning or reclassifying that failure.
That outcome did not pass, and the direct-build alignment above supersedes this
input contract without deleting failure evidence. No historical build controller
or existing snapshot source was edited.
