# Bounded module producer

This is new source under review, not a deployed service or completed v5 release.
The supported adapter is relocatable Windows Python; there is no OS portability
claim. No guest/image/backend change is required. Owner-controlled code, files,
runtime installation and OS remain trusted. Windows Jobs provide resource and
process closure supervision, not filesystem/network isolation.

```python
from production import Producer

producer = Producer(owner_profile)
try:
    outcome = producer.run(owner_request)
    # A receipt artifact still goes through the receiving agent's admission API.
finally:
    producer.close()
```

The CLI accepts `--profile`, `--profile-sha256`, `--request` and
`--request-sha256`. Both documents are bounded to1MiB, independently pinned,
owner-authored JSON. Invoke with the adopted Python's `-I -S -B` flags. Source
paths are derived from the installed module; there is no hardcoded project,
experiment, segment count or calibration hash. Remote callers must not supply
the profile, allowance or executable paths. The profile/request are decoded to
private request state, saved create-new, pinned and rebound during execution.
The owner filesystem is cooperative: these pins are not protection against
malicious Python executing in the same process or a hostile OS.

## Exact input schema

Every file pin is `{ "path": absolute_path, "bytes": positive_integer,
"sha256": lowercase_sha256 }`. No field may be omitted or added. `file_pin` in
the module is an owner convenience for inspecting an already adopted file;
hashing a downloaded executable does not establish its trustworthiness.

`owner_profile` has:

- `schema`: `DMKN_V5_PRODUCER_PROFILE_V1`.
- `supervisor_manifest`: a pin of the independently adopted compact supervisor
  release manifest. Its pinned `operator/commons.py`, `receiver/helpers/domains.py`
  and `receiver/helpers/run_stage.py` are the actual supervisor implementation.
- `host`, `python`, `python_dll`: pins of the adopted module host, running Python
  and its adjacent `python314.dll`.
- `source_pins`: exactly the installed `producer.py` and `__init__.py` pins.
- `runtime_pins`: up to128 additional independently adopted file pins. All
  runtime/source/helper pins together are at most512MiB. This is not a claim of
  a hermetic OS/DLL closure.
- `image_id`, `foundation`, `policy`: exact adopted 64-character lowercase hashes.

`owner_request` has:

- `schema`: `DMKN_V5_PRODUCER_REQUEST_V1`.
- `allowance_id`: a fresh owner-generated 64-character lowercase identifier for
  one finite allowance lineage. A resumed attempt reuses it; a newly authorized
  allowance must use a new identifier and explicitly carry previous costs.
- `session`: the schema below.
- `checkpoints`: an array of `{ "key": "kind:index", "file": file_pin }`.
  At most391; no `finish` entries. Keys must belong to the generated graph.
- `output_directory`: a fresh absolute directory, nonoverlapping all inputs,
  installed supervisor and adopted runtime/source files.
- `stage_limit`:1..392 maximum missing stages for this attempt. A small value
  selects an explicit prefix; no further attempt or budget is started by itself.
- `budget`: the schema below, unchanged throughout one allowance lineage.
- `prior_attempts`: ordered final RESULT pins of every earlier attempt in this
  allowance, at most16/8MiB. Each record must name exactly its earlier prefix.
  All earlier retained checkpoints must be included unchanged in this request.
- `carried_external_costs`: `{worker_cpu_seconds, controller_cpu_seconds,
  wall_seconds, scope}`. Nonnegative finite observations and an explicit scope
  string (1..1024characters). They are recorded separately, not charged again
  against this newly authorized allowance. Initial calibration, old attempts
  from another allowance, builds and failures are not implicitly free. The
  owner must state omissions/uncertainties; this field is not cost attestation.

`session` has `image`, `frame`, `expected`, `capsule` file pins;
`parents` (0..8 exact receipt pins); `binding` (capsule hash binding);
`cycles` (1..2^28); `po2` (12..20); `segments` (1..128);
`assumptions` (0..8, no more than supplied parents). Capsule schema is3;
checkpoint schema is5. The expected journal is exactly184bytes, profile2
`DMKNM002`, matching adopted image/foundation/policy. Counts are planning data,
not mathematical evidence: the unchanged host independently validates the
actual capsule, assumptions, proofs and final expected claim. An incorrect
count or binding causes failure, not acceptance. No guest reexecution occurs.

`budget` has:

| Field | Meaning / implementation ceiling |
|---|---|
| `worker_cpu_seconds` | Positive aggregate allowance, ≤250,000 |
| `controller_cpu_seconds` | Positive aggregate observed controller CPU, ≤3,600 |
| `wall_seconds` | Positive cumulative attempt-wall allowance, ≤86,400 |
| `output_bytes` |70MiB..2GiB retained new-attempt sampled envelope |
| `output_entries` |16..8,192 retained new-attempt entries |
| `stages` | Exactly `segment`, `lift`, `join`, `resolve`, `finish` maps |

Each stage map has positive integer `cpu_seconds` and `wall_seconds`. Maximum
CPU is1,800 for segment,600 for lift/join/resolve,300 for finish; wall≤600.
Every actual child uses4,096MiB Job memory,2active processes and1MiB per log.
These implementation maxima are not recommended allocations or performance
predictions. The root must separately choose the exact current finite request.

## Generated graph and reuse

For n segments, the graph has n segment proofs, n lifts, n-1 prefix joins,
a ordered resolves and one finish. Finish consumes every segment checkpoint
plus the final joined/resolved receipt. For n=1 there is no join and the prefix
is lift0. An existing joined checkpoint can cover missing intermediate lifts
without replaying them; required segment files are still needed by finish.
Only graph nodes needed for finish and not already supplied are executed, in
the generated topological order, up to `stage_limit`.

A checkpoint header establishes only schema/binding/kind/index/payload-length
agreement. The actual host cryptographically verifies each dependency when it
is consumed. Saved success JSON is never a mathematical premise. The existing
five actual base checkpoints import directly, without rewriting their bytes.
Preserve them: later finish needs segment0/1, while join1 already incorporates
the two retained lifts. Do not pass unused lifts as additional finish arguments.

Possible successful statuses are `PASS_SELECTED_PREFIX_ONLY` and
`PASS_FINISHED_RECEIPT_ARTIFACT`. The latter requires the unchanged host's full
final receipt verification and exact application marker, followed by binding,
closure and finalization checks. Neither outcome returns a `VerifiedModule`.
Only a receiving agent's separate public receipt-admission call creates that
live authority. There is no search, network, publication or automatic cold call.

## Budgets, failure and resumption

Each stage reservation is create-new/fsynced before launch. Prior settled
worker charges plus this attempt's charge plus the next reservation must fit
the finite allowance. Reliable final Job accounting reconciles the reservation
to actual usage; actual overshoot remains recorded and stops the attempt.
Unknown counters or cleanup keep the full reservation, mark uncertainty and
close the producer. A reservation is bookkeeping, not a proved upper bound on
all CPU: the retained hard Job time limit is user CPU; total CPU, wall and logs
are sampled. No automatic retry or renewal exists.

Before a stage,70MiB and10entry slots are reserved against sampled retained
output limits, covering a64MiB artifact, bounded logs/reports and final report
headroom. Inputs are pinned, not copied per stage. Outputs are never deleted to
make room. Size/entry overruns or finalization failure refuse the operational
pass; `FINALIZATION-FAILED.json` overrides any candidate status written before
the final check. These controls are not filesystem quotas.

A live producer remembers the latest completed history for each allowance and
refuses a repeated run omitting it. Across a process restart, completeness of
the owner-supplied prior-attempt list is an explicit owner custody assumption:
the library cannot infer that someone hid a directory. Pins and hash chains are
not a global accounting ledger. All supplied earlier records must form the
exact same session/allowance/budget chain. Their observed controller and wall
costs are also deducted, rather than restarting a full wall allowance. This
wall accounting sums active attempt durations, not downtime; cross-restart
calendar deadlines require a separate trusted owner wall-clock policy.

Unknown closure, missing final accounting, missing RESULT or finalization
failure returns/refuses with an owner-recovery requirement. The source does not
pretend to reconstruct unknown costs or automatically resume such an attempt.
A reservation may be the only durable record if settlement decoding/report I/O
fails; the producer then closes. The owner must inspect cleanup, preserve its
cost reservation and explicitly authorize recovery. Useful proof bytes may be
salvaged by pinning and later cryptographic consumption, without changing the
failed operation's status or treating saved JSON as proof.

## Accounting boundary

Successful `run` observations include request prevalidation and all supervisor
work from entry to the pre-final-report measurement. Startup, constructor/CLI
document reading, process exit and post-observation tails are explicitly not
included; meter the enclosing process when those matter. Nested supervisor
CPU must not be added again. For a refused preflight with no safe fresh output
directory, `producer.report()["last_call_failure"]` records observed CPU/wall
and whether an attempt directory existed. This is an in-memory observation, not
a durable resource reservation. Owner code must retain it and account refused
calls; they are not declared free or automatically deducted from a lineage
that could not be validated. A constructor failure has no producer instance;
the owner/enclosing process must account its cost.

Source/profile/request pinning is local engineering assurance. It does not
prove Lean soundness, cryptographic security, optimal proving cost, useful
growth or globally workable deployment. The full-base run, real recursive
child, cold public admission and ordinary agent workflow remain separate gates.
