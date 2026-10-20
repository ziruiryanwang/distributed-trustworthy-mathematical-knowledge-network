# Build invocation identity correction

Root, 2026-10-20. The first invocation used the retained installed receiver
Python, but this reused compiler controller explicitly requires
`D:\Python314\python.exe`. It raised `ValueError: PINNED_PYTHON` at builder line
89 before creating the run/attempt directories, snapshots, Job or any compiler.
Shell exit was 1. No compile was attempted or passed. The selected source and
plan bytes remain unchanged. Controller CPU was not separately measured.

Read-only checks confirm neither `typed-rows-build-01/` nor its `-attempt.json`
exists. The required existing interpreter and DLL have exact adopted hashes:

- `python.exe`: `03168c01b7b7491423350e82c26fee71f35b43694d1319d3c668bda6903a0c38`.
- `python314.dll`: `fde89cdb5c2d08ae65de7ef4abca1876c93ba3796002f5ac0bf7e4d4f5a94da0`.

Select fresh `typed-rows-build-02-selection.json`,
`0eaf0bd562b1d501412e415394d4ce33acb2c20c44df028bca64bbdfa24846a3`,
once with that required interpreter. It changes only the run name from01;
all 39 source bindings, builder, compile scope and finite limits are unchanged.
Line endings are ordinary UTF-8/LF in the fresh JSON. The failed invocation is
not erased or relabeled and no successful operation is repeated. No installation,
compiler, checker, runtime pin or memory limit is changed to satisfy the check.
