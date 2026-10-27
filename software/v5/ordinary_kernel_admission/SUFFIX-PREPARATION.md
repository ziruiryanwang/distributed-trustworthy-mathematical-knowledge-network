# Exact suffix manifests: file-only preparation

Root read/adopts INTAKE-COST-DECISION
`45765a4206238c636fe2fae74fd558b25c17e9c1f0c84d475981bcd027b9db9f`
and complete independent INTAKE-CONTINUATION-OPTIONS
`08f6f5e66995963c1a0b56b1836a7a488f1f24d6273b3293c4c9813365b11308`.
Select only preparation of two fresh plain JSON manifests under
`experiments/v5-local-checks/std-kernel-suffix-inputs01`.

Copy exact entries from the immutable original manifest
`std-reconstruct01/materialized/manifest.json`, SHA-256
`1de776b3d131c8c1be3414ed0e0cf066ebd05caebbcd1cf1b6ca80853962e59c`.
Preserve schema/semantic ID. Part A selects original intervals [1024,1644) and
[1644,2048); part B selects [2048,2477) and [2477,2651). Counts are 620/404/429/174;
raw bytes 8,552,756/8,595,160/8,899,687/8,867,997. Each entry is copied verbatim
as JSON data, without changing identities or splitting a unit. The separately
reviewed successful reconstruction establishes row-level dependency order.

Reference the original unit directory in future public calls. No unit file is
copied, re-exported or rewritten. Re-read the resulting manifests and compare
exact row arrays and counts against the original. Independent review precedes
any later intake. This file preparation grants no mathematical acceptance and
selects no owner/status/intake command or new allowance. Current prefix eligibility
and each next actual parent remain separately required.
