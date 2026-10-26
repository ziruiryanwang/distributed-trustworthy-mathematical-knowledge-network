# Current flat v5 development distribution

Root adopts the complete independent
[continuation outcome](CONTINUATION-OUTCOME.md), SHA-256
`e0116d6067bb12bb1e4a90df975090a2ec501adb4d13934bd2b1c2bfefe1a763`.
The supported current source and prebuilt now use one flat selection, not a
sequence of historical overlays. This is local, unpublished development;
the full v5 objective is not complete and licensing remains undecided.

## Obtain and use

- [Prebuilt archive](../../../experiments/v5-local-checks/current-release-continuation01/suite/prebuilt/package.zip)
  and its [receipt](../../../experiments/v5-local-checks/current-release-continuation01/suite/prebuilt/RECEIPT.json).
- [Source archive](../../../experiments/v5-local-checks/current-release-continuation01/suite/source/source.zip)
  and its [receipt](../../../experiments/v5-local-checks/current-release-continuation01/suite/source/RECEIPT.json).
- [Actual extracted operator guide](../../../experiments/v5-local-checks/current-release-continuation01/suite/prebuilt/relocated/README.md).

Use the archive's root guide and operator tools. The canonical repository's
original `prepare_selected.py` remains frozen as failed-run evidence; the
corrected archived logical entry contains the reviewed `prepare_selected02.py`
bytes. Do not run the old repository preparer or reconstruct a historical
overlay chain. Prebuilt operation requires separately approved Windows x64,
Python 3.14.6 and Lean 4.34.0 installations; it needs no native rebuild.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Source ZIP | 3,367,116 | `5811202225c5b6e72f360291fa53204e449bb3f3b73ad2c89ea1f283d250d921` |
| Source outer manifest | 16,426 | `3ca832782becf35b39b139dc94a4a3dc41bde0dbda39411cb3e6eaa0deaff0f7` |
| Prebuilt ZIP | 39,481,406 | `57f064c52778bef14560f7f92cbcaef7c3e8434556ddcb0ec33e132f78e1152e` |
| Prebuilt outer manifest | 24,491 | `acb75cab06cd3ee3e17d6d55b4ff33f138f1dae42146025af864c7c630d3ab11` |

The prebuilt package has 154 unchanged payloads, PROFILE
`dc0c19b7cf116742caa0751665da93400f6bc5b4663cfe313c3e81aa0d9c58e0`
and INSTALLATION
`32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.
Source compilation must use its own actual generated identities. Root also
adopts the full independent [direct-build outcome](BUILD-OUTCOME.md), SHA-256
`e91652aa0ff3f2653892fbb1f8e10172d0e46ad72de19efc38df491fe73cf48d`.
One build from the actual source-ZIP extraction produced all 154 files, with
clean compiler/outer closure: 123.2429436 wall seconds, 71.140625 known CPU
seconds and 923,103,232 peak Job private bytes. No overlay reconstruction ran.

The [source-built package](../../../experiments/v5-local-checks/current-release-build01/distribution/package/)
has actual PROFILE
`7c41db618e17dd9b296df6aa566d2673b72edd859023bcfb7369e11925685541`,
the same INSTALLATION above, and implementation
`fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df`.
Only its two freshly linked exporters and PROFILE differ from the prebuilt;
the other 151 files are identical. The prebuilt archive is not replaced.
This qualifies the direct source-build/assembly route, not a fresh mathematical
operation or bit-identical executable reproduction.

## What this closes

Actual corrected ZIP extraction, full exact-file verification, relocated inert
operation preparation, wrong-PROFILE refusal before writing, and loading the
offline exporter with the adopted faster binder all passed. Each corrected
archive differs from its failed-run predecessor only in the preparer and outer
manifest. The mathematical package, checker, limits and compiler lanes did not
change. The original failed controls01 and its ten previously reached negative
checks remain separate evidence; no failure was relabeled.

Continuation cost was 13.5428403 wall seconds, 4.8125 inclusive Job CPU plus
0.5 wrapper CPU, with 138,477,568 peak Job private bytes and clean closure.
Including failed controls01, these two distribution gates cost 10.6875 known
CPU seconds. Nested CPU observations are not added twice.

The archive includes current preparation, formal queries and offline export.
Use direct public `run.py peer serve` for finite serving. The historical
multi-lease service wrapper and standalone mirror are not included or selected
as compatible by this lean distribution. Their preserved evidence is not lost.

No native mathematical operation, owner/custody initialization, network trial or
growth comparison ran in this gate. It establishes a usable distribution boundary,
not universal library compatibility, accelerated discovery or worldwide release.
