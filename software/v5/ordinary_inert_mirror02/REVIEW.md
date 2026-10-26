# Independent review: metadata parser successor and remaining service path

2026-10-26. **Source delta GO; continuation tests/selection pending review.**
No runtime, imports, state/database access, experiment, Git or product edit by
this reviewer. Preserve the first failed run and its actual OUTCOME unchanged.

## Exact source delta

Compared the complete first and second helper text: exactly four changed lines.
`_ready` additionally receives the already selected `formal_features` module;
READY parsing changes to `F.strict(ready_raw, MIB)`; DESCRIPTOR parsing changes
to `api["O"].F.strict(descriptor_raw, MIB)`; its `_ready` call supplies that same
module. No new import, dependency, format, data check or transport behavior.

Repaired mirror.py SHA-256:
`86d0716d51f55040233bf2572c74bfdd7307a203a241ef2815c74f7958458920`.
run.py remains exact `cef9b50b8a98231e7f9e60afb0f9021b7d5f495266b2320957076ab4e1c55bd0`;
SOURCES.json remains exact
`1bc43d4c9896476443d0d6aab95015db7af32bc46a04cfb1624a5c40e638feb9`.

## Operational metadata grammar is distinct from evidence grammar

The existing pinned `ordinary_evidence.strict_json` intentionally forbids JSON
booleans/null; actual operational DESCRIPTOR/READY correctly carry booleans and
snapshot metadata. The selected `formal_features.strict` supports that JSON,
bounds bytes/depth, rejects duplicate keys/floats/nonfinite numbers, and requires
exact canonical serialization. Its UTF-8 canonical encoder agrees with the
descriptor writer `ordinary_evidence.canonical_json`, including non-ASCII paths.
The parent's READY fields contain only ASCII fixed strings/hashes and booleans,
so its ASCII canonical writer also produces the same selected canonical bytes.

Exact local file/hash checks precede either parse; exact schema, selected
semantics, typed configuration/target validation, descriptor/seal matching and
the parent-only clean-completion readiness boundary remain. The parser does not
grant readiness or truth. Ordinary evidence, target-name and basis parsing remain
unchanged and retain their deliberately narrower grammars. The source loader's
fixed shared module closure supplies `O.F`; no caller-provided parser is selected.

This directly addresses both observed/unreached metadata failures, not the
entire service path. The latter still needs its separately selected first actual
completion. Reuse the already completed prefix; a new parent-sealed preparation
is necessary because helper identity is part of READY. Do not edit or relabel the
old seal, inputs, state, source review or failed result.

## Final bounded continuation review

2026-10-26. **GO for root's one exact service02 launch selection; no runtime
success or product adoption is asserted by this review.** Read the corrected
`test_service.py`, its TEST-PLAN and the complete proposed selection. Independently
verified all eight source pins and 37 external pins (45 exact files); the fresh
`experiments/v5-local-checks/inert-mirror-service02` output leaf was absent.

Selected file: `experiments/inert-mirror-service02-selection.json`, SHA-256
`bbf032102eb81f6e4466323cc980f28b2b6e87a9bc25aeda24b45ff80204bc73`.
Corrected test SHA-256:
`c6910ded49d8df027f8a5dd4352ca26bf4089c8fc72ff7d0555cae0e287734e8`.
TEST-PLAN SHA-256:
`732709e9a11c2c10b8ac680199a69082d9863e2f2d34b219975891945647f0cb`.

The harness now uses the actual Manifest `evidence_bytes` field, verifies four
units and 5,149 exact evidence bytes, and reuses only the predecessor helper
functions under a non-main module name. Its old main/fixture constructors and
completed negative campaign are not invoked; `prior.check` is rebound to this
new finite allocation. Direct `_ready`, Store/status/admit and refusal calls
match the selected APIs. Expected metadata errors are caught by the inherited
ValueError/RuntimeError/sqlite3.Error discriminator; forbidden Provider.start
raises AssertionError, so accidentally reaching a listener cannot count as a
successful expected refusal.

The actual new descriptor and READY are the parser discriminator, not merely a
fabricated boolean example. Public discovery is still unknown-ID at its initial
formal query; the returned exact target and evidence bytes are subsequently
compared with the retained fixture. Live-lock exclusion runs while the public
service is alive. The snapshot control runs only after clean positive service,
adds an actually unindexed retained output to the fresh synthetic state, requires
objects to increase by one and the latest snapshot to change, then forbids
Provider.start while requiring PREPARED_STATE_BINDING and lock release.

The outer envelope is 120 wall / 60 inclusive Job CPU seconds, 1,024 MiB, eight
active processes, 4 MiB stdout and 1 MiB stderr. The harness's 100-wall/40-own-CPU
checks and both 40-wall/20-CPU/512-MiB/one-worker public actions are nested limits,
not renewed or additive grants. The five-second loopback lease has ten seconds
of cleanup reserve. The parent Job remains the process-tree backstop if a child
timeout or harness cleanup raises. A terminal PASS requires all three groups,
both clean public supervision reports, unchanged readiness/descriptor bytes,
the intended snapshot refusal and retained input rechecks. Actual outer closure
and saved outputs still require outcome audit; there is no automatic retry.

No concrete source/test/selection blocker remains in this changed boundary.
The first failed run and its missed evidence-vs-metadata grammar distinction
remain preserved. This review does not qualify mathematical checking, growth,
remote-host behavior, hostile-source isolation, publication or the full v5 goal.
