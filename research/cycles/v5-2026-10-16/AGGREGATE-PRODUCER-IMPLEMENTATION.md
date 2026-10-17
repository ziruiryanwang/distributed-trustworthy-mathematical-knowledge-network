# Aggregate producer implementation checkpoint

Status: **source candidate implemented; independent review/tests pending**.
Owner: `/root/memo_tests_review`; root owns adoption, Git and all launches.

## Scope and inspected authority

Only `software/v5/aggregate_production/__init__.py` and `producer.py` are
selected for new product source. The complete corrected
`../v5-2026-10-12/AGGREGATE-PRODUCER-PLAN.md`, existing aggregate API, full
`stage_host.rs` and full legacy `production/producer.py` have been read.
The source implementation composes the retained pure helpers and pinned loader;
it must not invoke the legacy module request/checkpoint/run workflow.

The completed frontier screen is preserved. Root reports an independently
adopted complete 113-segment, one-assumption capsule (37,187,089 bytes); that
selection is not proof funding and no capsule is regenerated here. Concrete
screen/build/image records must be bound by the owner profile and parsed against
their actual formats, not a generic saved-PASS predicate.

## Required implementation boundaries

- H is aggregate v2, `DMKNA002`, exactly 192 bytes; fixed I and adopted A differ.
- Capsule is `DMKNAS01`/1; checkpoint framing is `DMKNAP01`/1 and requires up to
  71 header bytes. Neither is an admission credential.
- Reuse unchanged graph/missing-plan helpers; finish retains all segments and
  the final prefix/resolve. Parents preserve exact native pending-claim order.
- Stage stdout has the API's exact JSON fields and types. Finish invokes no
  prover; attempts, planned prover invocations and reported prover calls differ.
- Fresh directories, durable controls/reservations, first-failure stop, explicit
  known-closure accounting and finalization override are mandatory.
- Same-allowance continuation retains source/profile/session/budget/carry
  identity, complete ordered prior history and every prior successful checkpoint.
- No tests, source imports, native execution, proof, build or Git mutation are
  authorized by this assignment. Independent controls follow source review.

## Implemented public seam

`from aggregate_production import AggregateProducer` exports an owner with
`run(request)`, `report()` and `close()`. The package has no CLI, discovery,
authoring, guest execution, build or proof-funding convenience path. It imports
the retained `production` helpers and constructs that `Producer` only for its
pinned supervisor/Job loader, `_read`, `_check` and closure method. It neither
subclasses nor invokes the legacy `_request`, `_checkpoint`, `_run` or `run`.

The new exact profile fields are `schema`, `support_profile`, `source_pins`,
`relation_image`, `host_build`, `image_adoption`. The two source pins identify the
actual new package files. `support_profile` retains the old loader's genuine
production source pins and puts the selected aggregate host in `host`, A in
`image_id`, and the adopted F/P in their usual fields.

- `host_build` pins actual `result`, `attempt`, `selection`, `source_map` and
  `command` records. The parser matches `aggregate_production/build.py`'s exact
  success format, checks command closure, executable/source-map/selection links
  and the actual retained stage-host/receipt/build source snapshots. It does not
  require the multi-gigabyte compiler inventory as runtime input.
- `image_adoption` pins actual assembly `result`, clean `outer`, outer
  `selection`, `guest_build`, `guest_selection`, `guest_source_map` and `artifact`
  records. The parser binds the memo four-crate build's selected source map and
  artifact to the actual assembled image and A. Adoption remains an independent
  local-owner decision: these records are not proof of compiler correspondence.
- `session.snapshot_evidence` pins actual inner `result`, clean `outer`, outer
  `selection`, `configuration` and native `command` records. It binds A/H,
  complete capsule, session/capsule bindings, s/m, cycle/po2, actual image,
  configuration and exact native parent argument order. Native stage calls still
  recompute the authoritative Rust bincode bindings and verify real premises.

The existing request outline is preserved. The dedicated aggregate session has
the plan's exact fields. Per-kind stage budgets explicitly select
`cpu_seconds`, `wall_seconds`, `memory_mib`, `active_processes`, `stdout_bytes`,
`stderr_bytes` and `output_bytes` (the artifact cap), under retained ceilings.
The whole allowance budget remains worker/controller CPU, wall, retained
output bytes/entries and these five stage maps. No value is an actual run
selection. The implementation reports a conservative full-missing-path envelope
before a selected prefix; failure of that envelope to fit is not disguised as a
cost prediction or full funding. Each actual launch separately must fit its
current resource reservation and 512 MiB input-read ceiling.

The new allowance-wide retained-output charges include measured pre-final
census plus a conservative 2 MiB/two-entry final report and failure-marker
reservation. These tail reservations stay charged across continuation; they
are not exact disk-use measurements. Per-stage artifact/log/control space is
reserved before launch, sampled afterward and never reclaimed by deletion.
All earlier attempt charges and prior-success checkpoint pins must survive.
The owner-held reports are not a globally tamper-proof ledger, and externally
supplied older checkpoints/costs still need their explicit owner provenance.

## Actual evidence used to define record parsers

Root confirmed adoption of:

- `frontier-capability-execution-01/RESULT.json`, SHA-256
  `4a08f6eb3a711105aaee1409c84c43260288ece99929cee7a978b541a55a4382`;
- its `evidence/RESULT.json`, SHA-256
  `5d21cb1966dc4dee52d59faf8e68f92aad92907522bb041faf078c53a39f44c6`;
- complete capsule SHA-256
  `7996306944a51e0eec597266819871115f4bdea1f799c944442e472869465ffd`;
- memo assembly inner result SHA-256
  `8a2174ad097333a54f3a314d63f0e646607a639aa5755efdd31c2ee1d08d43ea`
  and outer result SHA-256
  `50de313fbc8f20b3f48d971f3183bf66f1079cafe18af460538b414d715a2f4e`.

The current native capsule prefix was inspected data-only and agrees with
`DMKNAS01`, version1 and reported session digest
`bdd42310ed62504e78e4da164b633da7751597eda74eb00b873a06c552268649`.
None of these fixture paths/digests/counts is a controller constant.

**No aggregate stage-host build has yet been adopted.** Consequently the actual
constructor cannot be authorized with a fabricated success record. The parser
is written against the existing build source's future actual output schema;
the later one-link build/adoption remains root's separate decision. No concrete
missing schema choice was found that requires inventing a new adoption record.

## Static review and pending evidence

Source self-review checked v2 vs legacy layout, 71-byte checkpoint framing,
exact JSON types/argv, no finish prover call, uncertain CPU/closure handling,
nonzero exit before promotion, durable stage reservations/results, complete
history/profile/session binding and post-result finalization override. A failed
or absent CPU counter retains its reservation and closes the owner; an explicitly
unlaunched reserved call is recorded separately and is not an imaginary host call.

Only PowerShell file reads/hashes and `apply_patch` were used. No Python import,
test, syntax execution, native execution, build, proof or Git operation was run.
Independent source review and focused pure/fake-supervisor tests are still
required; source author self-review is not qualification. Actual cryptographic
production and any feasibility/cost claim remain completely unestablished.

Important nonclaims: no automatic retry, no saving a closure-unknown attempt by
renaming it, no filesystem-quota/security-sandbox guarantee, no theorem growth
claim, and no release/v5 completion claim.

## Narrow source repair after independent review

2026-10-16. Root selected only the unused producer's `_local_outer` repair.
Independent `AGGREGATE-PRODUCER-REVIEW.md` identified one concrete blocker:
the adopted memo assembly selection contains `--output {output}\\assembly`,
while the old candidate expanded only `{snapshot}`. Its exact-argv check
would therefore reject the genuine retained outer record. The finding is
source/data-derived, not a failed executed constructor or a reason to repeat
the assembly.

The repair now derives `output` from the pinned outer record's parent and
performs precisely the retained runner's ordered literal replacements:
`{snapshot}` then `{output}`. `tools/Run-V5-Check.py:104` has no `{root}`
replacement, so none is invented here. The reconstructed argument list must
still equal the actual outer list exactly. No path normalization, suffix-only
comparison, extra placeholder interpretation or weakened equality was added.
Schema, limits, selection pin, clean-closure predicates and every other producer
method remain unchanged.

Final source candidate:

- `producer.py`: 44,253 bytes, SHA-256
  `796eb24619370a30192db6d0f63b914516919e7cae90aee32a1750736331b86b`.
- `__init__.py`: unchanged 152 bytes, SHA-256
  `0ca27c691b5afe5ad93086251afb3259491f2ebcaf6e2a9b7ff7b209d4489bb2`.

The predecessor source hash
`f1a7e70e5049e0b71b1e21a490c92208d0c5d42f85babbd339be0521c0091d6b`
remains identified in the independent review. No used predecessor, retained
record, fixture, runtime, build, proof or Git state was changed. The reviewer
is checking the final narrow delta and retained actual argv; pure controls and
any later build/runtime remain separate root selections.
