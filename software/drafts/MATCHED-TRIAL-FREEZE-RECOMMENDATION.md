# Recommended minimal matched-trial freeze

Planning only; no shared recipe edits, code execution, consumer dispatch, or
mathematical source/proof authoring. Freeze the following policy after corpus
outcome and target-statement conformance pass. Defining the target proposition
does not prove it. Require identical freshly checked vocabulary onboarding.

Use the existing proposed request/stage/reservation limits. Make **600 seconds
an observed measured-CPU qualification ceiling**, not a hard aggregate Job
limit. Sum disjoint trial public Jobs, including inspections, plus treatment's
separately supervised service Job. Never add nested native stages or the
service's internal CPU counter again. Common onboarding is outside this marginal
ceiling and included in cold totals; report it equally for both arms. Wrapper,
agent, and other unmeasured CPU remain unknown.

Root updates the sum after each completed call. Once the observed sum reaches
600, start no further work. An outstanding call/service can overshoot; preserve
its actual cost and classify the arm outside the selected envelope even if it
eventually publishes. A completed endpoint and an in-budget endpoint are
different recorded facts. Keep existing per-call bounds. This avoids claiming
aggregate enforcement that the current interfaces do not supply.

Use a **240-second retrieval session within a 45-minute agent window**. The raw
service CLI fixes a 600-second session, while existing `run_stage` allows at
most 300 seconds and the public supervisor at most 450. Moreover, raw `serve`
explicitly requires caller process-tree supervision. Therefore the unmodified
600-second CLI is not the smallest supervised recipe.

Instead, use one small pinned owner adapter calling the existing
`peer_service.serve(..., session_seconds=240)` API under the existing 300-second
runner envelope. This is a call-site parameter, not a product change or new
supervisor. Freeze adapter/input pins, memory/storage allowances, ready path,
loopback port, and the service's existing connection/byte limits before launch.
The 60-second remainder permits startup/final bookkeeping; successful completion
within it is not assumed. The owner adapter is specified below.

Start that session once, validate its ready catalog/port, and immediately
dispatch treatment. Readiness consumes part of the retrieval window. Announce a
conservative absolute cutoff based on launch time; allow no new peer requests
after it. Acquired bytes remain usable for later admission and proof work.
Expiry is expected; a failed transfer or early service failure is retained as
an availability outcome. Do not restart, extend, preload acquisitions, or select
entries for the consumer. Disclose the shorter opportunity explicitly.

For each arm, the 45-minute clock begins with its fresh prompt. Require the
publication command to finish by that deadline for an on-time endpoint. At the
deadline stop new agent/tool work; let an already launched bounded public call
reach quiescence for evidence, without crediting late completion. No mathematical
repair, replacement arm, or feedback between arms is allowed.

Only remaining freeze items are exact prompts/model/tool/library restrictions,
randomized sequential order, file/retention limits, and the pinned service
adapter/envelope. Keep optional retrieval optional. Report cold and marginal
costs and substantive reuse separately; one pair supports no population
speedup claim.

## Owner adapter invocation and readiness

`serve_usefulness_corpus.py` is a draft owner adapter, not execution evidence.
Keep closed corpus01 untouched. In a fresh service allocation, owner-copy and
pin the helper plus all nine frozen view files; snapshot the helper as
`input/serve_usefulness_corpus.py`, and catalog, completion record and seven
bundles beneath `input/view/`. Include the runner-required pinned `domains.py`
input. Use the fixed vocabulary01 installation, a reviewed schema-2 plan,
300-second envelope, and frozen memory/storage allowances.

Select exactly one Python step with cwd `$RUN` and argv
`["-B","-E","-s","-S","$RUN/input/serve_usefulness_corpus.py","--port","<frozen-port>"]`.
The port must be 1..65535. There are no view, duration or ready-path overrides.
The adapter authenticates installed source bytes and catalog/completion bytes,
binds its staged paths through the existing domain contract, and calls the
existing loader/service once. It adds no supervisor or acceptance path.

Readiness appears atomically at `$RUN/out/ready.json`. Before treatment dispatch,
require host `127.0.0.1`, the frozen port, and catalog SHA-256
`354a5f4be37454df38b48b70f49c35efb7522fc1595d8ba44bb80eadcf8735c4`.
Retain ready bytes, bounded stdout observations, runner receipt and quiescence
evidence. A ready file alone is neither a current-liveness guarantee nor
mathematical acceptance. Do not restart after early failure or expiry.
