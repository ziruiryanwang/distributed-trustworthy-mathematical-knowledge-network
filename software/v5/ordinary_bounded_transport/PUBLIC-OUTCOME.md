# Bounded transport public01: independent saved-output audit

2026-10-25. Reviewer: `concept_software_bridge`; canonical guard PASS.

Disposition: **PASS for the selected assembled public-launcher boundary**:
new-wrapper preparation, intentional old-wrapper refusal, and the actual public
two-second directory lease closing a live unfinished-header client. Root owns
adoption. No rerun, product import, network operation, database/state access,
native mathematical stage or Git mutation was performed by this audit.

Evidence root: `experiments/v5-local-checks/bounded-transport-public01`.
Full predecessor/successor assembly-map checking is separately recorded in
`ASSEMBLY-OUTCOME.md`; it was not duplicated here.

## Exact evidence and selection

| Artifact relative to the evidence root | SHA-256 |
|---|---|
| `selection.json` | `ede5aeedeeb55a18ff287771efd250e1046db877f89122f9f9151fa5061702c9` |
| outer `RESULT.json` | `fd96cb1169beaa7b1a18186ac38008df36e3c3ce795a39d3832c2c70b820a4d1` |
| `suite/RESULT.json` | `b5ea7a1695885466589b83d3ed96769add28c51d9366d1bb0e03756888936ae4` |
| `suite/public/RESULT.json` | `df36d78cba061b0384d00d47bb6ccaedda25ee77be0ec14e2bb20c1848e37f08` |
| `suite/diagnostics/RUN.json` | `96927d99a6e237614a2e84e982dad305f3ceeef123a52d7857b4065d5415edb1` |
| `suite/diagnostics/SUPERVISION.json` | `423f5165ab6618df4da4f099aa3f3d909df4aff41f96272a30e64053f9092cfd` |

All seven source pins independently match both immutable snapshots and current
selected files, including public test
`156b56539dbbf3640534b2faff5a2535eb9c839f1d0813fc8ccbc2b878386d09`.
The original prospective selection, saved selection and outer result agree.
Nine targeted selected runtime/package pins were independently rechecked: the
three Python binaries, PROFILE, installation manifest, launcher, peer dispatcher,
profile loader and provider. This is not a new full census of the selection's
164 runtime/package entries; the separate assembly audit owns that map boundary.

The actual public package is
`experiments/v5-local-checks/bounded-transport-assembly01/assembled/package`, with
PROFILE `b047d4492da79e363fcd154144a6d9088a93100fde7aac3c385f3a296a41dad7`
and unchanged installation manifest
`32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.

The outer argv exactly matches selection placeholder expansion; actual child
commands match their saved supervision records. Suite stdout parses to the same
complete object as suite RESULT. Embedded ready/public/launcher/supervision
objects equal their independently saved counterparts. Service stdout equals RUN;
peer child stdout equals the actual public result. Preparation stdout embeds
the exact saved receipt. All receipt input/output lengths and hashes match.

## Actual public behavior

- The new bounded-transport wrapper successfully prepares `directory-serve`,
  reporting `bounded-transport-v1`, 45 known noncompiled roles, no commands
  executed and no protected state opened. It creates the exact arguments and
  configuration subsequently consumed by the real launcher; configuration SHA
  is `cae314d86afe5d43d2340dc93d51396f13e927846fd1e3100e7887f80fbe5eb8`.
- The old wrapper exits with the expected `KIT_SELECT_UNKNOWN_INTERFACE`
  traceback. Its stdout is empty and its output directory does not exist. This
  is the intended fail-closed negative, not a failed public-service run hidden
  by the top-level PASS.
- `SERVICE-COMMAND.json` selects the actual assembled `run.py`, which launches
  actual `peer.py directory-serve`. The exact configuration gives a two-second
  lease, ten-second cleanup reserve, K=1, four accepted attempts and a 60-second
  HTTP operation timeout. No helper substitutes a fabricated service result.
- The service exposes its ready loopback endpoint; the harness connects and
  sends a request line plus Host header **without the terminating header block**.
  The source keeps that client open while awaiting EOF. The actual provider
  reports one accepted attempt and one entered request, so this is not merely
  an idle-service expiry test.
- Actual client closure is **EOF**, observed after 2.0397416 seconds from the
  connection attempt through child completion, below the fixed eight-second
  assertion and far below the original 60-second operation timeout. The public
  result is `LEASE_FINISHED`, `quiescent=true`, with no cleanup errors, zero
  active/handshake/cleanup-pending records, zero reserved reply bytes and
  `accepting=false`. No reply body or completed HTTP request is credited.
- Public catalog, custody and store ID are null. The one advertised contact is
  an in-memory hint; no advertised provider is contacted and no mathematics is
  accepted. Preparation and lease reports explicitly keep mathematical
  acceptance false.

The complete public harness was read, including its error/finally paths. All
three actual children—new preparation, old-wrapper refusal and service—are
reported reaped, with no harness cleanup errors. Command, preparation, service
and peer-child stderr are empty; only the intended old-wrapper stderr is nonempty.
The pre-execution LAUNCH record's `NO_CHILD_LAUNCHED` is an initial intent record,
not the final outcome: RUN and SUPERVISION supply the completed zero-exit event.

## Closure and inclusive costs

Both nested public supervision and outer supervision report
`COMMAND_EXITED_ZERO_AND_CLOSED`, direct children reaped, Jobs closed, zero final
active processes, no termination request and no cleanup errors. The public
launcher stays within its selected 35-wall/15-CPU-second, 768-MiB/four-process
envelope inside the original outer 70-wall/45-CPU-second, 1280-MiB/eight-process
envelope. Outer cumulative process count is ten, not a peak-concurrency reading.

Known total CPU is **1.984375 seconds**: 1.328125 inclusive outer Job CPU plus
0.65625 outer-wrapper CPU. The nested 0.8125 Job CPU, public wrapper 0.09375,
harness 0.078125 and supervision subintervals are already included; do not add
them again. Total outer wall is **8.7110629 seconds**, with 8.4438875 seconds
command wall through cleanup. Peak outer Job private commitment is 70,746,112
bytes. Outer stdout is 7,103 bytes and stderr zero. There was one selected run,
not a renewed allowance or retry.

## Claim boundary

This closes the tested wrapper-to-public-service integration boundary, in
addition to the separate direct TLS/socket controls. This public run itself is
plaintext loopback; it is not another TLS interoperability test, mathematical
reuse test, growth result, independent-host pilot, exploit audit or proof of
global availability. The measured short shutdown is a finite observation,
not a universal latency guarantee. No additional unchanged rerun is recommended.
