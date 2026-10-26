# Multi-source package integration: independent actual-outcome review

## Decision

**PASS for the selected file-only package assembly and offline configuration
integration.** The single `multi-source-package01` run completed all five groups
and 28 refusal cases, with `COMMAND_EXITED_ZERO_AND_CLOSED` and clean containment.
No test was rerun. This is not mathematical acceptance, existing-state reopen,
an end-to-end receive, independent-host operation, a growth-speedup result, or
completion of deployable v5.

The new overlay makes the previously tested optional multi-source receive policy
available through an exact selected package and strict offline preparer. It does
not change checking semantics, turn preparer metadata into mathematical evidence,
or retroactively alter the older investigator archive.

## Evidence and identity

Run root: `experiments/v5-local-checks/multi-source-package01`.
Reviewed the actual saved outer result, command/stdout/stderr, test result,
refusal list, complete map, terminal assembly receipt, prepared files and frozen
harness. Rehashed all 16 selected sources in both current and snapshot locations,
all 158 external pins, all 154 base-package files and all 154 assembled files.
No selected-pin, actual-map or length mismatch was found.

| Evidence | SHA-256 |
|---|---|
| selection.json | eba0bda543dc4aac4ffcc60ad7e2c93964a3f7c5bcc6bd4c29fbe7976939a695 |
| RESULT.json | c28133c72f43f234ba0b5c93a6f9011d52dc7df03c7661cf29d924257001773d |
| suite/TEST-RESULT.json | 73f7eff7fc917100d15db3fd527f7e09ce8729b7030fb9f132934b550311453e |
| suite/MAP.json | fb9982e37bfc408dbb08842804f4b33e0606efd5ebeba83feea46fc37515c5f8 |
| suite/REFUSALS.json | 3b91c820d7d192ae89d917d9287bc78d30b0a07f5ce714e82239a5d5ea255c32 |
| suite/assembled/ASSEMBLY.json | ec5ab7709aba2c4a896fa1898e925effb8f7a95f17bdb300c55307fcc5c10d6c |

The source/launch review is `INTEGRATION-REVIEW.md`, SHA-256
`8e402a2aa1295e150b0e395eee1751edb219b9b0e50d13765acc49119d20a3a8`.

### Actual assembly

The terminal receipt reports `ASSEMBLED_NOT_ADOPTED`. It identifies the genuine
retained exact-module base, the reviewed assembler and fixed three-file overlay.
Actual new package:
`experiments/v5-local-checks/multi-source-package01/suite/assembled/package`.

| Identity | SHA-256 |
|---|---|
| Old PROFILE | bde63019d1a6ac2bccd8e0c245a405ad3ca551d0606c01a5193fee6897c60346 |
| New PROFILE | ca257419f464c2e9d968011983673160377f743ebbe2a27e2399b510dce1ce67 |
| Unchanged INSTALLATION | 32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2 |

Both actual package trees contain exactly the same 154 file paths. Exactly four
files differ: PROFILE and the three approved payloads:

| Changed payload | Bytes | SHA-256 |
|---|---:|---|
| peer_api.py | 68115 | dcaea5226f58e4254dd4cff0d6c621cf593aabe9b4d511d127194816c8ddc0ef |
| support/transport/http_provider.py | 31361 | d9c342d1dcb5ee3e4b293e8dc0566397a321cc59a6f545e2f2afde452c760251 |
| support/transport/ordinary_acquisition.py | 30121 | 076130f7a34b505df33ee550501d1c4276bb46e408ff226df765225933a0658e |

Thus 150 of 153 non-PROFILE payloads are byte-identical, including the complete
native installation, narrow module-anchor support and eight old documents.
All 117 auxiliary PROFILE roles match actual lengths/hashes; all non-role
PROFILE fields are unchanged. The complete saved map matches actual files.
The original base remains equal to the preselected external pins. These facts
support the precise unchanged-footprint argument, not an inference that a real
owner was reopened or that state compatibility was executed here.

### Actual preparation and refusals

Default, legacy-default and optional-policy preparations each contain inert
configuration/arguments/receipt files. Independently verified all nine receipt
file pins, all nine input references and each config hash embedded in argv.
The default config is byte-identical to the old preparer's output under the
same explicitly selected private PROFILE; arguments agree after changing only
the prepared-directory path. Optional config adds exactly:

```json
{"acquisition_sources":["B","A"],"attempt_timeout_ms":3000,"finalization_reserve_ms":2000}
```

Order is preserved, and every other configuration field is unchanged. The
optional config hash is
`820e3a3e805ea6f0bdc55c8b66b2a089e2611fb68cc4f615ef1f69a52c099acf`.
These preparations execute zero product commands and certify no mathematics.

The five saved groups and the actual 28-element refusal array reconcile with
the frozen harness:

- Six assembly refusals: wrong PROFILE, receipt and overlay pins; existing
  output; wrong fixed base interface; wrong base assembler receipt.
- Sixteen invalid receive policies: all six nonempty partial subsets of the
  optional fields, empty/duplicate/unknown/oversized/non-string source lists,
  boolean/zero/out-of-range/nonintegral time values, and an unknown extra field.
- One preview rejection for receive-only policy, plus two historical-PROFILE
  parent/find report refusals. Reports were not relabeled.
- Three final selector/preparer refusals: old interface, wrong PROFILE pin and
  existing prepared output.

No refused preparation created a new prepared directory. The catalog and custody
fixture directories are still empty; the requested operation output is absent.
The explicit `METADATA-NOT-MATHEMATICS.json` and harness make the synthetic parent,
find and CHECKED strings unmistakable. There was no real owner/database or Lean
execution. Network, subprocess and shell-entry calls were guarded in the test;
the reviewed code path imports only approved file/preparation helpers.

## Cost and closure

The original selected outer envelope remained 130 wall seconds, 75 inclusive Job
CPU seconds, 768 MiB, one active process, 2 MiB stdout and 1 MiB stderr. Nested
harness/assembler budgets were not renewed.

| Measurement | Actual |
|---|---:|
| Full selected operation wall time | 7.3889341 s |
| Supervised command through cleanup | 7.2219591 s |
| Inclusive Job CPU | 2.921875 s |
| Outer wrapper CPU | 0.421875 s |
| Known total CPU | 3.34375 s |
| Peak Job private commit | 42,438,656 bytes |
| stdout / stderr | 2,916 / 0 bytes |

Harness time 6.5199589 seconds and assembly time 4.4083804 seconds are nested,
not additional wall charges. Harness CPU 2.75 seconds and assembly CPU 1.34375
seconds are included in the Job measurement; the separately displayed supervisor
CPU 0.03125 seconds is within the outer wrapper measurement, not added again.

Exit code is zero; direct child reaped, Job closed, final active processes zero,
terminated processes zero, no termination requested and no cleanup errors.
Raw Windows `total_processes` is 2, a cumulative counter distinct from the active
process cap of 1. No identity census was saved, so this audit neither invents its
cause nor infers native execution from it. Explicit runtime pins are not a
hermetic-toolchain proof, and sampled limits are not hard disk caps.

## Disposition

Root may adopt this exact package/preparer integration within its tested scope.
Public raw-config receive remains the previously reviewed route for explicitly
selected existing owners whose historical reports bind an older PROFILE; this
file-only run neither exercised that route nor authorized rewriting those
reports. Any eventual existing-state end-to-end operation needs its own selected
inputs and ordinary mathematical authority. No repetition of the passed native,
mirror or acquisition campaign is justified merely by this overlay.

All used sources, selections, base files and saved outcomes remain preserved.
This reviewer used only inert saved-file inspection and hashing, made no product
or state calls, changed no Git state and did not run another experiment. Full v5
remains open; this is a completed practical integration slice, not a replacement
for its remaining release requirements.
