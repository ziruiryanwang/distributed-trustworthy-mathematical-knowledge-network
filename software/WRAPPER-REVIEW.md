# Independent wrapper/interface review

2026-09-21. Reviewer authored the separate domains/checker/runner extraction and
therefore **does not independently certify that core**. This review covers root's
`build.py`, `manage.py`, `py/node.py`, `py/inspect_context.py`,
`py/supervise.py`, and `assets-lock.json`, including their fit to the declared
core interface. Source reads, hashes, and text diffs only: no Python/Lean import,
execution, compilation, or behavioral tests were performed.

## Findings at the reviewed cut

1. **Must fix: transport failure does not establish nonacceptance.**
   `manage.invoke` currently returns `accepted: false` on `SupervisorFailure`.
   A node may have committed accepted state before response/event persistence,
   post-exit supervision, or supervisor-receipt persistence fails. Thus the
   wrapper knows the response exchange failed, not that the operation was never
   accepted. Return an explicit unknown state/acceptance outcome and retained
   evidence location. Do not route a post-dispatch failure through a generic
   `OWNER_COMMAND_FAILED` result claiming nonacceptance. Recovery/retry must use
   the same exact request ID/bytes and existing pending/idempotency rules.

2. **Small parser hardening:** `build.read_record` rejects the literal JSON
   nonfinite constants, but default `parse_float` accepts `1e400` as infinity.
   Its stated finite-float contract therefore needs a finiteness-checked float
   parser. This is not evidence of a mathematical acceptance bypass.

3. **Small configuration operability repair:** invalid `--client` values are
   detected by `load_config` only after creating state/scratch and writing the
   configuration. A reserved `owner` label or duplicate labels consumes fresh
   paths, then the corrected retry fails `FRESH_STATE_AND_SCRATCH_REQUIRED`.
   Validate the client list before these writes. Partial filesystem failure
   still needs to remain visibly incomplete; do not silently clean it up.

These findings were sent directly to root. They are source findings, not
executed counterexamples. Fixes require an updated source cut and bounded
qualification; this note alone does not close them.

## Interface fit established by source inspection

- The build creates a new scratch request/stage, binds schema 2 and normalized
  domains, includes the exact `domains.py` input pin, and uses the required
  runner status. Its two serial Lean steps compile BootstrapSupport and then
  AgentReplayCore into the stage output library. Native imports match this
  order. No old experimental `.olean` path is referenced. Promoted installation
  outputs must match the successful runner's exact output pins.
- Configure selects installation-local freshly built support, locked
  mathematical assets, the required domain helper pin, arbitrary supported
  local client labels, and an empty offer list. Build completion and
  configuration explicitly are not mathematical acceptance; receiving bootstrap
  still passes through the checker. The build receipt is trusted operator-local
  bookkeeping, not a portable externally authenticated build certificate.
- Request/inspection launches provide `-B -E -s -S`, correct CLI arguments,
  executable/config/dispatcher/runner pins, and fresh evidence under configured
  scratch. The supervisor retains the existing Job cleanup and request/response
  event binding. It does not itself promote mathematical state.
- Node's extraction delta binds the installed node/domain helper, schema,
  configured state path, and scratch event path while preserving the existing
  prepare/commit and pending-stage behavior. Its metadata routes remain distinct
  from selected mathematical checker loading.
- Inspection retains mode=ro/query-only database access, current-client context
  selection, exact historical describe evidence, a refusing native allocator,
  and explicit historical/not-new-acceptance output. Its checker work directory
  lies under configured scratch, compatible with the new core.
- The asset lock enumerates foundation/common data, three native sources, and
  the unchanged codec/source-codec/symbol-index helpers. It is not a whole-product
  executable lock or a runtime/DLL attestation. This pass did not independently
  recompute every listed asset hash or establish manifest closure.

## Reviewed source identities

| File | SHA-256 |
| --- | --- |
| `build.py` | `FB66FE728E742B55C7AC18C1F3522ED905829CF64683740E30E17B06DA6FB9CF` |
| `manage.py` | `79035659FDA3295A893D108B3139248A5762B4451EA0BC319CA531E46E956071` |
| `py/node.py` | `832E68E8B4A5449A80BF3F324CD14790C7F20A6F5DBE34C696DA49F65EA4DD77` |
| `py/inspect_context.py` | `FD0248A77583A60C357C179E854D2109A4F6A546F67557E81737B586F842E549` |
| `py/supervise.py` | `E5F35C0A88602757ECB7FF899F923F940B588E11E2A7C9C36D51FDBB2DFCAC1B` |
| `assets-lock.json` | `887230FC0A0BB52350CF5C0B3E2233AB015EDA1649D634A3E15CF740C8FC0492` |

No native-build, fresh-relocation, reciprocal-node, or long-running operability
claim follows from source compatibility. Capacity renewal, uncertain-work
recovery, peer transfer, and independent-host qualification remain separate
requirements rather than being disguised as passed wrapper checks.

## Repair disposition

Root repaired all three findings. A narrow reread of `build.read_record`,
`manage.configure`, and the affected `manage.invoke`/`main` outcome branches
confirms the following source changes:

- Supervisor failure and nonzero public-worker exit now return `accepted: null`
  with `state_outcome: "UNKNOWN"` and the evidence location. Generic owner-command
  exceptions also report an unknown outcome. They no longer assert that a
  possibly committed operation was not accepted.
- Execution-record float parsing now converts through a `math.isfinite` check;
  literal nonfinite constants and overflowing exponent floats are refused.
- Client count, uniqueness, syntax, and reserved-owner validation precede the
  first state/scratch creation or configuration write.

All three findings are **closed at source-review level** for these updated pins:

| File | Updated SHA-256 |
| --- | --- |
| `build.py` | `9F57312577C3E48683D4BFC365134A964CF85BB2FD3C86B98D642926DD1E08CF` |
| `manage.py` | `037E1A4067837E17EF2523371C4ABCBD5F94D3FA5157297286BADFA7DCA80A69` |

The earlier findings and hashes above remain as the review trace, not unresolved
claims against this repair cut. This follow-up performed no broad re-review,
imports, execution, or tests. Native/build qualification remains unrun.
