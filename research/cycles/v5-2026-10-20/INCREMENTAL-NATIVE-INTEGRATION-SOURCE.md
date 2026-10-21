# Genuine warm-prefix integration adapter: source ready

2026-10-21, core_release. Source-only implementation under root's
`INCREMENTAL-NATIVE-INTEGRATION-SELECTION.md`; no product import, runtime, test,
build, proof or Git mutation has been performed.

`software/v5/incremental_native/integration.py`: 16006 bytes, SHA-256
`d64453541ae3c9f130ff69d73d6de1361b0a867eab62995de131385221446d6b`.

CLI: `integration.py --output <existing runner output> --input <pinned JSON>`.
The closed schema is `DMKN_INCREMENTAL_NATIVE_INTEGRATION_INPUT_V1`, with root's
agreed `map`, `installation`, `supervisor_manifest`, `native`, `receipt`,
`python_runtime` and ordered `packets` fields. The existing outer runner owns
exact input/snapshot/runtime pins and its fixed resource ceiling.

## Implemented scope

- Stages only the mapped 114 selected SDK files and three exact replacements,
  checks copied bytes, and imports the real staged classes. No `__new__`, patch,
  synthetic verifier, receipt callback or changed supervision path is used.
- Uses the installed immutable native/receipt executables and supervisor helpers
  in place. Its actual 18-file Python runtime must contain `sys.executable`.
  Constructor maps contain 119 receipt pins and 101 native pins.
- Explicitly creates one fresh test-local trust adoption for its exact selected
  source/runtime/helper/executable/owner roles. The adapter compares the adopted
  support ID itself; it does not assume the low-level constructor derives the
  larger facade's role mapping. Aggregate image is null; no aggregate is used.
- Admits retained M then retained M+V on the same genuine mixed receiver. Exact
  packet hashes, module summaries, witness hashes, journals and all expected
  native/receipt/reservation/memo counters are asserted. The second prefix hit
  must have no input, process, stdout directory or fresh receipt call artifacts.
- Saves two small successful-call records plus source/support/final outcome.
  Both live owners are closed and the domain withdrawn in `finally`; cleanup
  failures make the final outcome fail. Failed inputs/state remain preserved.

Caps match the selected plan without refunds or extensions: receipt one call /
223594 bytes / 10 CPU reserved; mixed two calls / 1048097 bytes / 50 CPU reserved /
60 controller CPU / 150 wall / 64 MiB output / 512 entries. Each receive has
10 CPU per checker / 60 wall / 512 MiB. Expected actual counts: two native checks,
one exact conditional reuse, one I receipt check. No network, frontend, authoring,
import, source preparation, new proof or old circulation is performed.

The final pass is local integration evidence, not a transferable certificate or
full-cost growth claim. Actual native CPU is retained in the genuine process
reports and the receiver's observed-worker report, never fabricated. Cold-owner
ancestry, all-system scale, and whole-v5 readiness remain outside this check.

Independent source review and root launch selection remain required. This file
does not authorize execution; no run is pending from this agent.
