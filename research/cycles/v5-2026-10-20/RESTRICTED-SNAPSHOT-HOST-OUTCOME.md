# Restricted snapshot host: actual one-link audit

Disposition: **PASS for the selected snapshot-host compilation and linkage.**
This is not a host-execution, guest-execution, receipt, mathematical-admission
or product-release result. Root invoked the finite link once (session41294);
the reviewer inspected retained outputs and did not rerun it.

## Exact operation

Run: `experiments/v5-local-checks/restricted-snapshot-host-build-01`.

| Record | SHA-256 |
|---|---|
| Original and saved selection | `60b345d6ebe4f1bfa578ef4da28cc9e53bdca59438f85cb23a3f33d60c373447` |
| `RESULT.json` | `ecbfeb97fe6d290b687945a1b8975c85d976274bdaa29943563453b36074a404` |
| `restricted_snapshot_host.exe` (5,426,176 bytes) | `e3f35fb15ac19ce9862796e50f01807145583307b9b607c8219411c8206271b9` |
| Used `software/v5/restricted_guest/build_snapshot_host.py` | `719ed9058ca9a8d5dfa59a07a362f4438bd8e9b13753b7883bfb48333021c984` |

All listed file hashes were independently checked. The attempt record exactly
binds this RESULT and `PASS_RC_SNAPSHOT_HOST_ONE_LINK_ONLY`. Neither the fresh
run nor its two adopted predecessor runs has a finalization-failure override.
The original and saved selection bytes are identical here.

## Source and linkage checks

Independently rehashed the three original selected sources and their three
snapshots, checked exact source closure, and checked both saved source maps:

- The builder above.
- Unchanged `software/v5/aggregate_small/aggregate_host.rs`,20,755 bytes,
  SHA-256 `6644d9a03f25a59089fd735b0e2f2229ec8940dedbe2502568dfd8c6a36d9c25`.
- Unchanged `software/v5/aggregate/receipt.rs`,3,631 bytes,
  SHA-256 `41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254`.

The source snapshot contains exactly these three files. No host semantic source
change was made: the existing native preflight and receipt-verification code
remain present through exact source identity. Their execution is not established
by compilation.

Independently rehashed all11 retained record pins and15 helper pins in
`INPUT-MAP.json`. Compared the entire finite runtime map structurally to the
adopted predecessor map:1071 entries, minus the old aggregate library, plus
the exact two native restricted-composition libraries, equals1072 entries.
The selection and saved input map agree at every key and digest. The reported
runtime byte total is2,322,344,899. The used builder rechecked that whole map
before and after compilation; this audit did not redundantly rehash the
unchanged2.3GB runtime tree. It independently rehashed all eight direct extern
libraries, including the two changed edges:

- Restricted core1,719,004 bytes, SHA-256
  `1bdfd6a0943b6a09248ae99aefd793b63384a957bf8d98c0cd8d8b430fd04a0b`.
- Restricted aggregate1,050,594 bytes, SHA-256
  `be8bdcb4c815e5c610145e5fea28a6d6601fe8dd9ae8cd04f3bf35c5b9dbcbba`.

The recorded actual command equals `compile-command.json` exactly (71
arguments). Independently reconstructed it from the old host's command: four
one-occurrence substitutions (crate name, snapshot source path, output path,
aggregate library) plus six appended arguments for restricted library lookup,
its explicit extern and fresh metadata. All other flags and dependencies stay
unchanged: Windows target, opt-level3, fat LTO, embedded bitcode, overflow checks,
unwind panic, no test compilation. Eight direct extern paths all belong to the
selected finite runtime map.

## Actual terminal result and cost

Exactly one compiler/link command completed with exit0. The stdout log is empty.
The2,002-byte stderr log, SHA-256
`718171018e20585963065e7ab9f985bb48f6f0d60fe8ec34a72f18da17327767`,
contains four ordinary unused-field/method warnings in the unchanged receipt
source, not compiler errors. Both log digests and lengths were independently
checked.

The phase Job report and RESULT agree: closed, no cleanup errors, zero active
processes, zero limit-terminated processes, four total owned processes.
The selected owned VCTIP telemetry cleanup is explicitly recorded and its exit
was observed; it is not an unreported resource-limit termination. No
finalization-failure marker exists.

| Resource | Observed value |
|---|---:|
| Inclusive worker Job CPU |84.34375 seconds|
| Disjoint controller CPU |6.0625 seconds|
| Known sum |90.40625 CPU-seconds|
| Wrapper wall |98.77934810006991 seconds|
| Peak Job private commit |883,806,208 bytes|
| Sampled maximum fresh bytes |25,869,473|
| Sampled maximum entries |73|
| Final recorded fresh bytes/entries |7,647,116 /50|

CPU accounting excludes the final report/exit tail as explicitly declared by
RESULT. Worker CPU already includes its children; no child or phase subset is
added again. All reported values lie within the selected caps. This is an
implementation-preparation cost, not a demonstrated search or growth benefit.

The builder reports zero checker/backend/relation rebuilds and zero host,
guest, proof or network calls. The actual recipe and retained command count
support that narrow claim. A source-bound executable is now available for a
separately selected subsequent operation; neither its existence nor this audit
authorizes such an operation automatically. Used source, selection, executable
and all evidence remain frozen.
