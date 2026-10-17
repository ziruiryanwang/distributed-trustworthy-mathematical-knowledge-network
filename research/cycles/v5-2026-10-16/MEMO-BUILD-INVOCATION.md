# Root invocation correction before compilation

The first invocation used the installed receiver's Python instead of the exact
interpreter required by retained build helpers. It failed `PYTHON_PIN` in
`common_build02.py:93` before creation of the output directory or attempt record,
and before any compiler call. Tool chunk `e88a80`, exit 1, reported 1.1868366 wall
seconds. CPU was not measured; it is not reported as zero. This is a root
invocation error, not a compiler or mathematical failure.

Read-only checks then found both `proof-memo-guest-build-01` and its attempt
record absent. No evidence was overwritten and no source changed. The exact
retained `provision_build.py` requires `D:\Python314\python.exe`, SHA-256
`03168c01b7b7491423350e82c26fee71f35b43694d1319d3c668bda6903a0c38`, and
`python314.dll`, SHA-256
`fde89cdb5c2d08ae65de7ef4abca1876c93ba3796002f5ac0bf7e4d4f5a94da0`.

The independently reviewed selection
`16730dce90438a8ee83215af842babfc0def7ef1ef89a6a8bf901c8e05b855b9` still
authorizes the one fresh four-crate operation. Correcting this invocation
does not renew a completed/failed compile, raise any budget, or relabel the
preflight refusal. Later actual build evidence is separate.
