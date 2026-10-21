# Focused exact-custody Node controls: source checkpoint

2026-10-20, core_release, explicitly reassigned by root. No execution, Node
startup, network, import, dependency installation, build, proof or Git operation.
Only the test source was authored; root owns the single prospective execution.

Source:
`software/v5/body_location/tests/controls01.mjs`

SHA-256: `d7c161310d8ecb4c45ee65f6293acee2a022763aa3610f647141e91ed8d58fea`

Size:22957 bytes.

## Parent contract

```text
node.exe controls01.mjs
  --code ABS_OUTPUT/selected-code
  --vectors ABS_OUTPUT/protocol-vectors.json
  --output ABS_OUTPUT/node-controls-result.json
```

The Python control author owns the exact selected logical-code tree, pinned
Node invocation, subprocess accounting, timeout/closure, vector file and report
readback. The vector is the object produced by
`test_protocol_exact_vectors_and_domain_separation`; fields are domain, body,
namespace, spec, key, request, reply, policy, index_spec and index_key (extra
Python diagnostic fields are ignored). Input/output size bounds are64KiB.
Output uses exclusive creation; no retry or overwrite.

The output schema is `DMKN_V5_EXACT_CUSTODY_NODE_CONTROLS_V1`, with status
PASS/FAIL, a four-entry `groups` object, explicit inert scope and
`mathematical_acceptance:false`. All groups run independently after successful
loading. Each group records PASS or bounded error/stack. Any failed group makes
the process exit nonzero; the parent must also require four PASS groups, not
merely trust the final exit code or stdout. Stdout contains one compact summary.

## Four changed-boundary groups

| Group | Actual source exercised | Inert boundary |
|---|---|---|
| Protocol parity and role isolation | Python-produced namespace/spec/key/request/reply equals JavaScript; old index key unchanged; mutation/role/schema/endpoint refusals | Pure finite vector |
| Same-locator wrappers/shared caps | V1 body refusal; V2 index+body publication share advertised-key/command limits; same reader peer cache and distinct descriptor protocols; reader cannot publish/withdraw | Finite DHT/peer-store/dial methods, actual wrapper/framing code |
| Intent transaction and withdrawal | Exact two-role key validation; one common published prefix; paired transaction call; revoke prevents later own-provider insertion | In-memory transactional quota primitive, not fresh SQLite qualification |
| Descriptor serving and IPC | Actual `_serve`/`_serveBody`, Reader/sendBody; common two-handler, request and reply-byte caps; missing-intent failure; closed IPC command/sequence/frame caps | Finite stream arrays/promises, no transport |

The fake maintained locator is constructed but never started. It receives one
inert node/store and a finite time cutoff. Its fake runtime rejects any attempted
real node startup. Each constructed locator is stopped in a finally block; the
held-stream gate releases in finally too. Transport counters stay at zero.

The executable `node_entry_services.mjs` is never imported: doing so would run
its process bootstrap. Only bounded source-branch assertions inspect the four
dispatch cases, foreign-clock guard and two-command narrow unavailable branch.
These assertions are explicitly labeled source coverage, not runtime dispatcher
qualification. Shared intent atomicity is asserted through the existing glue
against an inert rollback primitive; previously qualified SQLite behavior is
not rerun or newly claimed.

## Review and remaining work

Manual source review checked fixture shapes against current protocol/config,
actual transport report fields, framing semantics and the same-child wrappers.
No parser or runtime check was performed. The parent/test author must review
this exact source, then root may select one bounded mixed Python/Node control.
Do not create another proof/network campaign or qualify deployment from it.
