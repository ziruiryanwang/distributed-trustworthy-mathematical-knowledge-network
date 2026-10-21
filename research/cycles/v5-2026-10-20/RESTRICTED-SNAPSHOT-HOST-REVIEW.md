# RC snapshot-host relink: independent source review

2026-10-21, growth. Disposition: **PASS for the selected compile-only source
boundary**. No compiler, product import, host, guest, proof or Git operation
was run during this review. Root alone selects a launch and adopts its outcome.

| Reviewed source | Bytes | SHA-256 |
|---|---:|---|
| software/v5/restricted_guest/build_snapshot_host.py | 17581 | 719ed9058ca9a8d5dfa59a07a362f4438bd8e9b13753b7883bfb48333021c984 |
| research/cycles/v5-2026-10-20/Select-RestrictedSnapshotHost01.ps1 | 3846 | 804df1e8f1f0f7e391f4ad6d959a8229478e2b51b4d5160fb3371749b0de4dc7 |

Reviewed both files fully, the exact retained compile command, helper-loading
and bounded-phase interfaces, retained input/result metadata, and the unchanged
host's native preflight/genuine receipt/guest claim paths. Actual retained
library extents were inspected; the 2.32-GB runtime was not rehashed by review.

## Recipe and runtime correctness

The retained recipe is one successful native `rustc` command. Four substitutions
each require exactly one occurrence: crate name, source snapshot path, output
executable path, and aggregate extern. The command adds only the native-build02
dependency search path, explicit RC-core extern, and fresh metadata suffix.
The Windows target, optimized fat-LTO/bitcode, overflow checking, unwind mode,
linker and SDK/native search arguments remain unchanged. Exactly eight direct
extern paths must appear in the selected runtime map.

The runtime map is derived by exact map equality, not filesystem discovery:

\[
1071-1+2=1072,\qquad
2320491997-916696+1719004+1050594=2322344899\text{ bytes}.
\]

The removed entry is the original aggregate library; the additions are the
actual build02 RC core and aggregate libraries, with exact byte/hash/result
bindings. Original module/checker, SDK, compiler and system tool bindings are
retained. Existing native search directories remain in use; this is explicitly
a trusted retained toolchain, not a hermetic directory-closure or hostile-code
sandbox claim. The actual aggregate and RC libraries have explicit extern
paths; the old aggregate is not an executable fallback.

## Provenance and source coherence

The builder checks the retained host result, exact command/environment/input
records, original selection and terminal attempt. Native build02's result,
source-map, commands, original selection and attempt are separately pinned.
Both retained outcomes must have clean final owned-process state and no
finalization override. Critically, result `selection_sha256` is compared with
the original `*-selection.json`, not the differently serialized saved copy;
the guest01 provenance defect does not occur here.

The fresh selection has exactly the required six fields and matches the
builder's schema/name, three sources, 1072 runtime pins and all limits. Rust
source pins remain the unchanged 20,755-byte snapshot host and 3,631-byte
receipt verifier. Their relative include resolves correctly inside the new
source mirror. The new Python builder is the third selected source; all three
are copied create-new and checked again at finalization.

The new host therefore preserves native `relation::check_bytes` preflight,
exact expected-H equality, genuine fixed-I receipt verification, selected
image binding, po18 guest execution and actual resolved session-claim checks.
Those are retained source properties, not evidence that this unbuilt host has
executed successfully. No stage/proving host or public producer is introduced.

## Resource and outcome handling

The selector and builder agree on worker CPU 240 seconds, worker wall 300
seconds, 3072 MiB, six active processes, ordinary/final-total controller CPU
40/60 seconds, total wall 420 seconds, 512-MiB/8192-entry fresh outputs and
1-MiB command logs. The retained phase factory's requested 300/4096/8 shape
is checked before the intentionally tighter 240/3072/6 worker Job is created.

The complete runtime is hashed only before work and at finalization; the
intermediate check binds the smaller records/helpers/sources without a third
runtime pass. No backend view is recopied, no general dependencies are
rebuilt, and exactly one link invocation appears in the source. Owned Job
closure, reaping, final source/runtime pins and output census precede a
successful result. An explicit finalization marker overrides earlier saved
success. Partial output is retained rather than silently reused.

No material source/selector blocker was found. Actual command success, clean
outcome audit and source-to-executable identity still precede any matched-pair
execution. Compile success itself would not establish a certificate, cost
advantage, growth claim or completed v5.
