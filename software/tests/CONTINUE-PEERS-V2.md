# Positive reciprocal continuation: refusal-accounting repair

Prospective second coordinator cut. No execution or qualification is claimed.
`continue_peers.py`, the original G run, original author source, requests, native
records and original failure report remain unchanged. Root alone may launch a
separately reviewed new allocation. This is not an automatic retry or a reset
of the node's existing charges.

The positive eleven-command sequence, source/runtime trust premises, service
grant, public interface boundary and substantive-dependency audit requirement
remain those in [CONTINUE-PEERS.md](CONTINUE-PEERS.md). This note specifies the
changed launch/attempt schema and corrected refusal accounting. The v2 source
is a retained copy of the original coordinator with these bounded changes, not
a modification of an executed artifact.

## Why this cut is necessary

The original G attempt reached an actual public `SOURCE_REJECTED` response.
Its failure occurred during the first source-check child, before publication,
service startup or peer transfer. The original coordinator incorrectly required
the five-child success profile before binding/accounting the actual failed
submission. Thus its `NATIVE_PIPELINE_PROFILE` failure obscured the public
refusal and omitted that call's actual stage/CPU from its aggregate; it also
overwrote the already available cleanup observation with an unconfirmed label.

The original report is historical evidence of this reporting defect, not the
authoritative aggregate cost of that attempt. The independent original
`OUTCOME.md` and underlying actual supervisor/event/native receipts carry its
audit correction. Pinning that Markdown note preserves the trace; the note does
not grant mathematical acceptance or overwrite the original machine report.

The independently revised author source is a new exact input. The coordinator
does not inspect diagnostics to synthesize a repair, edit that source, change
the selected theorem, or force success. A second refusal remains a recorded
refusal and stops this new allocation without further attempts.

## Exact launch schema and attempt identities

```text
python -B -E -s -S software/tests/continue_peers_v2.py --launch ABS_JSON

{
  schema:2,
  phase:"g_to_beta" | "h_to_alpha",
  attempt:"g02" | "h01",
  coordinator:FilePin,
  helper:FilePin,
  python:FilePin,
  prepare:FilePin,
  previous:FilePin,
  author:FilePin,
  original_failure:FilePin | null,
  original_outcome:FilePin | null,
  limits:{command_seconds:500,active_wall_seconds:1800,
          observed_cpu_seconds:1800,retained_bytes:1073741824,
          service_seconds:120,service_max_requests:2,
          service_max_bytes:67108864}
}
FilePin = {path:absolute_path,bytes:positive_integer,sha256:hex_digest}

author file = {schema:1,node:"alpha" | "beta",context:opaque_context,
               root:author_selected_Lean_declaration,source:FilePin}
```

There are exactly two supported phase/attempt pairs:

| Phase | Attempt | Exclusively new evidence root | Request/service prefix |
| --- | --- | --- | --- |
| `g_to_beta` | `g02` | `qualification/peer-01-g02` | `peer-g02` |
| `h_to_alpha` | `h01` | `qualification/peer-01-h01` | `peer-h01` |

For G02, `previous` is the same pin as the actual successful `prepare` receipt.
`original_failure` must pin the retained
`qualification/peer-01-g/continue-failure.json`, whose status is `STOPPED`, phase
is G and preparation lineage matches. `original_outcome` must pin the separate
`qualification/peer-01-g/OUTCOME.md`; it is checked as retained bytes, not parsed
as an acceptance or state-repair instruction.

For H01, both original-history fields must be exactly `null`. `previous` must
pin the successful schema-2 G02 result at
`qualification/peer-01-g02/continue-result.json`, including its actual
`attempt = g02`, G phase and preparation lineage. That pinned predecessor
transitively retains the original failed attempt and its audit note. No original
G failure is treated as a successful contribution.

Prepared installations, configuration, support and runtime pins remain
unchanged. G02 still checks actual public heads/snapshots/descriptions against
the successful preparation: the prior source refusal made no visibility
change. Existing request/stage/byte charges are nevertheless retained. A new
baseline inventory includes the old failed source and evidence; it is not
required to equal the pre-failure whole-tree seal. No counter refund, row edit,
file deletion, old request-ID replay, service restart or old-root overwrite is
performed. H01 is a separate future allocation, not implicitly executed by G02.

## Authentication, observation, then success checks

For a public call with a completed supervisor receipt, v2 orders its work as
follows:

1. Authenticate the actual adjacent request bytes, response bytes, request and
   response hashes, event origin, supervisor success/zero-active observation and
   direct-child reap. These are transport/process premises, not mathematical
   acceptance.
2. Preserve observed process quiescence on the command record. Read exact-typed
   actual event stage/checker/pipeline counters, record them in `actual_work`,
   add actual stages/pipeline children to this attempt's observations, and add
   the unique actual public Job CPU once. Write the immutable binding before
   any expected successful-workload assertion or aggregate-budget refusal.
3. Inspect the public response status. A non-`OK` response records its public
   status/code and stops with `PUBLIC_REFUSAL:<code>`; for example,
   `PUBLIC_REFUSAL:SOURCE_REJECTED`. The exact diagnostic response remains in
   retained stdout. It is not replaced by a five-child success assertion.
4. Only for an `OK` response, enforce the expected workload: a successful source
   submission has one native stage and five pipeline children; successful
   admission has one stage and one child; metadata/transport paths allocate no
   native stages. Further acceptance/identity checks are unchanged.

Thus a properly authenticated one-stage/one-child source rejection records
that actual work and its actual Job CPU despite not satisfying the successful
submission profile. If a later status/workload/identity assertion fails,
`failed_direct` does not overwrite already authenticated process-quiescence
evidence. It retains the old conservative unknown-cleanup behavior when that
evidence was never established.

Missing/malformed/unbound events or supervisor records still cannot be called
complete evidence. Optional absent checker counters are represented as `null`;
an absent pipeline count after a reported checker load marks the bound-call
pipeline observation incomplete, instead of inventing a zero. The draft does
not claim every possible process/transport failure can be fully accounted.

`native_stages` and `observed_pipeline_children` are observations for this new
allocation only. The original attempt's costs remain in its separate audited
records, and the live node still carries all earlier consumed charges. CPU is
still a declared incomplete subset: coordinator CPU plus each bound unique
public/service Job, without double-counting nested native Jobs; direct wrappers
and missing final receipts remain unmetered. The repair does not retroactively
rewrite old totals or label total CPU complete.

## Unchanged positive path and interpretation

Each successful direction still requires exactly eleven public CLIs and two
new native stages: sender/receiver info, sender submit/publish/expose, one sender
service, receiver find/acquire/pre-admission info, stopped-service observation,
receiver offline admit and post-admission info. There is no extra product call
for this repair. The service has exactly the original two-connection
catalog/bundle grant and must be authenticated stopped/reaped before admission.

G02 still yields an actual Beta packet for an independent H author. H01 still
requires a distinct identity and ends with
`POSITIVE_RECIPROCAL_OFFLINE_LOOP_COMPLETED_AWAITING_DEPENDENCY_AUDIT`, never an
overall reciprocal qualification PASS. Direct, substantive dependency use and
the remaining controls need independent evidence. A changed reporting harness
does not itself establish mathematical correctness, usefulness or operability.

All existing cooperative wall/output/CPU-subset and retained-byte bounds remain
unchanged. The coordinator has no new outer OS container and no new recovery or
cleanup authority. Failure stops; all prior and current evidence remains.
