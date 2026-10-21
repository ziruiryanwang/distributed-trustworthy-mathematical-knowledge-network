# Restricted composition: native adoption and one guest build

2026-10-21, root. The unchanged final v5 objective remains active.

Root reads and adopts the actual native-build02 audit a54c0138 and the complete
native-controls audit c340551ed6719da5c389ff908dcfb9e96bafe7da040ec8cae7f3cefb8b2d18ec.
All 40 controls and 26 intended refusals pass, including both actual original-W
comparisons. Known control CPU is 0.640625 seconds, with clean closure. These
are conditional native checks, not certificates or a universal refinement proof.
Failed build01 and all used evidence remain preserved; no native run is repeated.

Root fully reads/adopts independent guest-build source review
86cf6cd3f175e6acdd04d000167c37e67de723bb539a68536843fe89a5d50f35
and build-selector/assembler review
85cbf4ab8eab7a4ed8644206164976c24559822641bb9dcd5bb032961a1bb8ff.
Select exactly one restricted-guest-build-01 operation:

- build.py: 79a19fb822cbaed734f737e723ac9a2eabcfc8b0f13256ca1814ed728dcdff02.
- recipes.py: b2fc5d26e4504c4caf8a41c62ff47048daf13dd2c3653af8a67f7ef8e09903ed.
- selector: 037b212905bd0c33904d3a8a5f0066c3e7faac7cd777c7d315ed441a9829a638.
- Native RESULT: 24e8ebf8f774e22ec19c7172dca0a56efb81ad653e609445ae0e5d030e2233dd.
- Controls outer: 74646cc153e87c186586e97e699c19225c3a729a31377e1248a7ceb4585013a3.
- Controls inner: 1e7d6130444fd133e2f88b95e057e7338df8beaa0a42b14e9f471dd0b7b9fca2.

Invoke the reviewed selector once, then D:\Python314\python.exe -I -S -B with
the generated exact selection and digest. Only three direct project compiles;
reuse 236 retained dependency files and copy only four original project artifacts.
No checker, SDK, dependency rebuild, Cargo, proof or installed trust change.

Limits remain 240 worker CPU / 300 worker wall seconds, 4096 MiB, six processes,
40 ordinary / 60 total finalizing controller CPU, 420 total wall seconds,
256 MiB fresh output / 2048 entries / 8 MiB command logs. No retry or renewal.
Adaptive owns independent actual build adoption and then the host-source review.
Assembly, paired execution and proof funding remain separate decisions. The
prospective same-target economic screen remains unchanged.
