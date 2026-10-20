# Evaluator snapshot: independent finite launch review

2026-10-20, core_release. **PASS for one root-selected execution-only screen**,
subject to the separate exact mathematical-binding review. No selector, guest,
native checker, proof stage or Git operation was run by this reviewer.

- Adapter: `software/v5/evaluator_method/snapshot.py`, 10,394 bytes,
  SHA-256 `1e68b9c5ee652d2d8fb82c640ee0174ebd5b8209c9b9c635d9058c634e517fa5`.
- Selector: `research/cycles/v5-2026-10-20/Select-EvaluatorSnapshot.ps1`,
  SHA-256 `236dcb0db46476b6816307b36dc69166e3a78628582408c60e6ccd8a742a79fb`.
- Existing runner: `tools/Run-V5-Check.py`, selected `44a7bf1b`.

## Selection and actual CLI

The selector checks the adopted preparation profile `edfd3b4a`, installed input
map `a0d5fad8`, six exact module helper pins, reviewed adapter and runner. The six
selected physical helper files match the installed map. Runtime pins retain the
installed Python/runtime, host, image, genuine BASE receipt, exact accepted new
witness and its saved result. Fresh input, selection and output paths are required;
create-new writes preserve prior evidence and do not restart an old allocation.

The adapter imports only that snapshotted six-module closure and issues exactly
these two existing host commands, in order:

1. `prepare IMAGE RAW_WITNESS FRESH_FRAME FRESH_EXPECTED_JOURNAL`.
2. `stage IMAGE FRAME EXPECTED 33554432 18 snapshot 0 FRESH_CAPSULE 1 BASE_RECEIPT`.

Checked both argv layouts against `modules/receipt/src/bin/module_host.rs`.
The snapshot branch has a single parent and no trailing checkpoint arguments.
It uses the existing execution branch, not segment/lift/join/resolve/finish.
The prepared image rewrite is not trusted to preserve the payload: the adapter
requires byte-for-byte framing of the original canonical witness before execution
and again at finalization. Core_growth separately reviews the exact journal,
parent and mathematical relation; this review does not duplicate that argument.

## Resource and closure boundary

The selected outer runner supplies the original 120 CPU / 240 wall second,
1,024 MiB, three-process Job and source/runtime rebinding. Only root's selected
runner invocation qualifies this boundary: the adapter's precondition text is
not itself an OS-membership test or a hostile-input sandbox.

The adapter uses at most 30 seconds for prepare and 150 for snapshot, each also
bounded by the remaining original 195-second command horizon. Rebinding requires
elapsed time below 200 seconds. There is no retry or budget renewal. Commands
are hidden, have null stdin, inherit the enclosing Job and remove all RISC0_*
environment overrides. Python's timeout kills/reaps the direct child; the outer
supervisor is still required to close/reap the process tree and report failures.

The real host bounds serialized output to 64 MiB and schema 3, at most 128
segments. The adapter additionally checks the exact host reply, capsule size,
schema prefix and final capsule digest. It rechecks configuration/input pins,
frame and journal, and rejects output links or a final census exceeding 160
entries / 128 MiB with report allowance. Child-log and directory caps here are
postchecks, not hard disk quotas; trusted finite host behavior and the outer
operation bounds remain explicit assumptions. No new resource mechanism is
needed for this narrowly selected screen.

On any command, binding, capsule or finalization error, status is FAILED and
evidence is retained. A completed capsule is explicitly not a certificate or
mathematical admission. Original input files and all earlier runs remain frozen.
The final adopted adapter includes a pre-execution review improvement that
re-hashes the completed capsule against its reported pin before success.

## Decision boundary

This operation can resolve actual completed execution and segment count only.
The `3s+1` subsequent complete host-call graph is descriptive, not permission
to launch it or an economic estimate. The actual unsealed method's native delta
cost is 0.03125 Job CPU / 0.1229064 wall seconds; successful snapshot execution
does not make certification competitive. No expensive production, new allocation,
parameter expansion or rerun is authorized by this review.
