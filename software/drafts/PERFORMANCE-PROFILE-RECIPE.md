# Diagnostic submission profile recipe

Proposal only; no implementation, imports, execution, or tests performed.
This is one separately allocated diagnostic run, subject to the root's later
selection after producer/corpus work.

Prepare a fresh installation copy with only the diagnostic `node.py` change
below, record its source hash, and perform the standard support build/configure
sequence. Use new state/scratch, client `local`, two requests, two stages,
272 MiB reserved capacity, and 32 MiB metadata. Keep ordinary time, memory,
byte, and supervision limits unchanged. Initialize the existing five common
packages. No offers, configuration edits, imported acceptance receipts, or
new mathematics are needed.

Submit exactly the existing 207-byte `UsefulnessVocabulary.lean`, root
`Reduction`, SHA-256
`b3d65406fa204268f74bb3cbdcd623991127aa5d3ccc06595c63890f9fd9e48a`,
against that fresh initial context, using request ID `profile-vocabulary-001`.
Allow one submission attempt. Do not publish, rerun, or substitute another
source if it fails. Preserve failure/pending evidence under existing rules.

The instrumentation location is `software/py/node.py:423`, inside `main`,
immediately around the existing
`Dispatcher(config, store, event).execute(req, raw)` invocation, after
`ControlStore` creation. In the diagnostic copy only, activate a
`cProfile.Profile(timer=time.process_time, subcalls=False)` for this exact
submit request ID, source hash, and root. Enable immediately before that
invocation and disable in `finally`. Retain all existing exception handling,
store closure, response bytes, acceptance conditions, and receipt generation.

This measures dispatcher-process CPU, including checker initialization and
submission validation. It excludes child-process CPU, process startup,
configuration loading, owner-lock acquisition, `ControlStore` construction,
and final response/event serialization. Time spent waiting for child processes
does not become their CPU time. Profiling overhead is unmeasured and included
in the diagnostic cost; this is not an optimized timing result.

After profiling is disabled and the normal response is flushed, save one
exclusive-create `dispatcher-profile.json` beside the validated public-call
event in scratch. Bind it to the request digest and diagnostic node hash.
Do not change stdout. Profile collection/export failure must leave ordinary
request results intact and mark the diagnostic unavailable through bounded
stderr, without retrying.

Bound the export to 64 KiB and at most 60 function rows: the union of the top
30 by exclusive CPU and top 30 by cumulative CPU. Include calls, recursive
calls, exclusive/cumulative seconds, bounded filename/function labels, and
the exact scope above. Cap processed profile entries at 10,000; above that,
report unavailable. Do not export caller graphs or an unbounded binary dump.
Retain ordinary supervisor/stage receipts and pin the sidecar separately.

The review table compares exclusive hotspots and cumulative parent functions;
never sum overlapping cumulative times. Decide whether foundation, commitment,
or planning work dominates the measured dispatcher scope before commissioning
an optimization. All three fresh Lean invocations and inverse/evidence checks
remain unchanged. Report one diagnostic observation, with no speedup claim.

## Root's selected next preparation: combine two readiness questions

After producer02 and corpus01, root selects a combined **prospective** diagnostic:
verify the target statement's source representation while profiling that one
submission. This supersedes the two-request allocation above, not any executed
allocation. No diagnostic code has been executed or consumer dispatched.

`UsefulnessTargetStatement.lean` is 643 bytes, SHA-256
`2C1F0832C82E73423D212CA5782CA28EE4088D6EC4C53C4D72F8726E3F76570E`,
root `ChunkedReductionStatement`. It defines a proposition expressing the fixed
chunked-reduction target; **it does not prove that proposition**. Acceptance
would establish well-formed source/canonical representation only, not completion
of the consumer task. Its bytes and any private artifact stay evaluator-only.

Use the four-request common vocabulary onboarding described in the matched
recipe, then one target-definition submission: five requests / four stages /
552 MiB, no target publication. Freeze a fresh diagnostic cut, source changes,
pins and exact limits before execution. The profile is gated to request ID
`profile-target-001`, that source hash and root. The mathematical checking path
remains unchanged; observed profile overhead cannot support a speedup claim.
This combines an actual unresolved interface gate and a cost diagnosis without
another mathematical proof, corpus rebuild or consumer hint. The older failed
constructor-efficiency adoption remains negative evidence; do not repeat an
unmeasured optimization merely because this profile identifies similar code.
