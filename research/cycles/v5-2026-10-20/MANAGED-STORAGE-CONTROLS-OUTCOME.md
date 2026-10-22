# Managed storage controls: independent actual-outcome audit

2026-10-22, storage_outcome_audit. **PASS_SELECTED_PYTHON_AND_NODE_STORAGE_SEAMS.**
This is an independent saved-output audit, not control authorship or execution.
The canonical guard passed. No test rerun, product import, database connection,
service, network, proof, build, credential read, deletion or Git mutation was
performed. The two operations are terminal with clean recorded containment.

## Bound evidence

Paths below are relative to the indicated directory under
`experiments/v5-local-checks/`. Each original `*-selection.json` matches the
corresponding saved `selection.json` and outer result's selection digest.

| Operation | Evidence | Bytes | SHA-256 |
|---|---|---:|---|
| managed-storage-python-controls-01 | selection.json |9432|`03f55573baab54742fea38a24417d0a92880154cc3971c6c193e3c7b024747ba`|
| same | RESULT.json |2036|`07742121a02d21b51c123f8fd4cd7f6f4ed85fa9e09377d85dc08933ea83e0af`|
| same | python-controls-result.json |7169|`777ad6e8500c5ee415aa59f1655225421d1850b392785c5079c4c6ded38e5d99`|
| same | command/command.json |698|`92352739d74345e5c3551fa850661e77240e1a018bf0848f50ffbd4792f644bb`|
| same | command/stdout.txt |7171|`45d0be4c328d277eda41e490b45aa478606e9d45c33da9e25d46a995efbd07f0`|
| same | command/stderr.txt |999|`5c98a4a6035246274bed6b94798414a40485317d1623189a1efb10d817045597`|
| managed-storage-node-controls-01 | selection.json |9148|`a222a507d5240e14aa83d9375504cc442dbb5eb00a107c8cf6d908edcaf16e22`|
| same | RESULT.json |2045|`35dd17c56bc52981645cd8a63aebf4e9ad588bc2b16c1ff1fd7da7cae37e2720`|
| same | node-controls-result.json |9219|`eb21374250c1913c9511a9265fe1378ad1153260b215205a4d702bff5d26fec9`|
| same | command/command.json |697|`674ea108fc875f24c8f78299cb77467f817e37f9be7b4c9a4fe76c6e1ae51ede`|
| same | command/stdout.txt |9219|`eb21374250c1913c9511a9265fe1378ad1153260b215205a4d702bff5d26fec9`|
| same | command/stderr.txt |0|`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`|

All 12 Python and five Node original sources and snapshots independently match
the selections. Each snapshot has exactly that many files. Python controls are
`cda358d759fe0808ea4546601ed343ce764cd0bb222a64f21a7115baf99414c9`;
Node controls are
`8996b2e03a34e5085ea620a140a79e12847abcaa899083f94d02a883cf440491`.
The entire two controls and the pinned runner44a7bf1b were read. Executed argv,
canonical cwd and all six limit fields match selection. Python is isolated
`-I -S -B`; Node runs the selected observed01 executable without added flags.

The runner authenticates the 28 Python /31 Node explicit runtime pins before
and after each operation, authenticates its supervisor through the frozen base
manifest, and refuses final binding changes. This audit relies on that inspected
runner and successful outer results for these runtime passes; it did not repeat
a complete runtime-tree or executable sweep. The test-only adjacent protocol
alias88c2bc34 is selected in the Node snapshot, not an SDK overlay addition.

Node's actual result identifies 72 imported code files and 23 present package
metadata files. This audit independently hashed exactly that reported closure
(284359 bytes) against the authenticated base manifest or selected source pins;
all match. The control itself checks actual module-loader bytes and rechecks
imports, package metadata, manifest and executable afterward. The maintained
service is read for static checking, not imported. No 5896-file runtime scan was
substituted for this narrower boundary.

## Python observations and extent

The full stderr and inner result agree: seven named groups ran, with zero
failures, errors or skips; stderr ends `Ran 7 tests in 0.190s` and `OK`, with no
warning. Stdout equals the inner result bytes followed only by CRLF. There are
111 expected refusals across the selected strict-type/arithmetic, path, format
and layout checks, not 111 independent full-product scenarios.

The actual full F/SP/SF modules execute; only discovery_store's complete pinned
top-level `ordinary` function is AST-extracted. The checks establish:

1. The chosen closed-form arithmetic and strict scalar boundaries agree with
   independent expected expressions, including exact-fit/one-byte-short cases,
   all permitted runs and both reserved slots.
2. Fresh path checks do not create state; one-byte locks pass while malformed or
   reused locks and a fresh preexisting journal refuse without changed bytes.
3. The selected over-cap main, unsupported WAL/SHM, unknown generation entries,
   nonempty operations directory and oversized identity metadata refuse with
   preservation. Partial known metadata passes without creating missing entries.
4. An actual tiny named SQLite file is configured before DDL, written, closed,
   reopened and read successfully. Observed settings are page_size4096,
   auto_vacuum0, journal_mode delete, synchronous2, temp_store2 and max_page_count64.
5. A separately created auto_vacuum FULL database refuses with
   `MANAGED_STORAGE_EXISTING_FORMAT`; its mode remains1 and its bytes are retained.
6. Exact registry-marker metadata passes; wrong marker and unexpected entry
   refuse. This fixture is inert, never connected to SQLite.
7. Static AST controls confirm each of seven opener seams' selected lexical
   preopen/connect/configure order and matching arguments, plus reservation
   ordering. These are not executed manager paths or control-flow dominance proofs.

The actual SQLite observation is version3.50.4, source-id
`2025-07-30 19:33:53 4d8adfb30e03f9cf27f800a2c1ba3c48fb4ca1b08b0f5ed59a4d5ecbf45e20a3`.
That is a runtime observation, not a proof of SQLite implementation correctness.

Independent read-only fixture census/hash comparison exactly matches all22 files
and18 directories (including the fixture root), totaling283707 bytes. Actual
SQLite files are8192 and12288 bytes. The fake oversized main and incompatible
database remain; no cleanup, repair, replay or migration was performed.

## Node observations and extent

All seven selected groups report PASS, with no error, binding error or close
error. Stdout is byte-identical to the inner report; stderr is empty.

The actual intent-store subclass extends the actual installed QuotaDatastore,
using the actual protocol and Key. Fresh SQLite profile readbacks are
page_size4096, auto_vacuum0, journal_mode delete, synchronous2, temp_store2 and
max_page_count256; a positive cache_spill is asserted. The executed assertions
cover empty counters, put/get/has, replacement and exact byte accounting,
1025-byte value rejection with unchanged counters/value, delete and zero counters,
then close with a null handle. Synthetic identity/adoption bytes remain unchanged.

Opening the just-closed database, or a fresh directory containing a synthetic
journal, WAL, SHM or unexpected file, refuses with
`LOCATION_METADATA_STATE_ENTRIES`, a null handle and identical before/after
inventory. The four sidecar/extra fixtures have no new metadata.sqlite. This is
the fresh-state entry guard, not hot-journal recovery. Both serialized identity
buffer limits are checked before either write only by the separate static-source
group; no private key is generated or parsed.

Independent fixture census/hash comparison matches all15 files and five
directories, totaling25531 bytes. The one real database is24576 bytes; all
deliberately refused fixture files remain. The test's finally block tracks and
closes stores on failures as well as successes; this result has no close errors.

## Containment and charges

Both outer results are `COMMAND_EXITED_ZERO_AND_CLOSED`, direct child exit0 and
reaped, active_processes0, job_closed true, no cleanup errors, no requested
termination and terminated_processes0. Each reports cumulative total_processes2;
the selected limit is one simultaneously active process, not one process identity
over its lifetime. No service orderly-stop signal is expected for these fixtures.

| Measurement | Python | Node |
|---|---:|---:|
| Selected CPU / wall / memory / active processes |10s /45s /128MiB /1|10s /45s /128MiB /1|
| Final Job CPU seconds |0.46875|0.65625|
| Top-level wrapper CPU seconds |0.3125|0.421875|
| Known total CPU seconds |0.78125|1.078125|
| Outer wall seconds |1.9064894998446107|3.6390262003988028|
| Command-through-cleanup wall seconds |1.8668085001409054|3.53950780024752|
| Peak Job private commit bytes |25821184|41689088|
| Stdout / stderr bytes |7171 /999|9219 /0|

Combined known CPU is **1.859375 seconds**. Nested wrapper-supervision CPU
(Python0, Node0.03125) is not added again to top-level wrapper CPU. Node's own
501000 CPU microseconds /2065.8855ms and Python's unittest0.190s are narrower
internal observations, not total workflow costs. The two outer wall times are
reported separately; their sum is not the elapsed duration of parallel execution.
All logs remain within the selected1MiB-per-stream limits. Final tiny fixture
censuses are not peak physical-disk quotas or proof of the envelope's worst case.

## Consequential disposition

These results close the two selected changed SQLite/helper boundaries before a
fresh file-only distribution build. Root may adopt them together with the
independent integration source review; the audit itself launches nothing.

They do not execute the complete installed owner/profile/manager/supervisor
integration, establish hot-journal recovery, adopt a physical disk/free-space
bound, prove the source-to-runtime correspondence, validate custody or networking,
accept any mathematics, demonstrate independent hosting, or complete v5. The
conditional apparent default-data-stream envelope retains its reviewed runtime,
default-VFS, private-writer and no-restore premises. Used sources, selections,
snapshots and all successful/refused fixtures now remain frozen. No repeat of
these exact controls is justified.
