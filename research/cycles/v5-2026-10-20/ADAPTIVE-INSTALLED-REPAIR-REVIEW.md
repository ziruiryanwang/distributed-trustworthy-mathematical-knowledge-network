# Installed diagnostic repair: independent source review

2026-10-20, adaptive_audit. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

**GO for root's separately selected corrected boundary02.** Source/diff review
only; no runtime, build, test, trust adoption or Git mutation by this reviewer.

| Reviewed file | SHA-256 |
|---|---|
| `software/v5/located_queries/installed02.py` | `0660ae06ef643a6c99c680ca16807b6a5bd9202a4614c5011608a04c10e07e0d` |
| `research/cycles/v5-2026-10-20/Select-AdaptiveInstalled02.ps1` | `2d72eef26d235f1d9d2f6a1c5ac6333917797ba6b2aa14a682dcaed945c2164f` |

## Failure retained and review correction

Read the actual boundary01 `work/adaptive-installed-result.json`. It records
FAILED at cleanup with the sole reported cleanup error `NONCANONICAL_JSON`,
two queries/three client calls, same original child/owners, CLOSED client,
closed workspace/channel, zero-exit child without forced termination, and
withdrawal of the exact created temporary domain. Its raw child stderr was not
retained: 862 observed stderr bytes is not evidence of their transport counters.
Boundary01 remains failed; this review does not retrospectively pass it.

My prior source review missed the serialization distinction. Node's terminal
diagnostic uses ordinary insertion-ordered `JSON.stringify`; `F.strict` demands
canonical sorted-key JSON. The terminal field names were compatible, but the
serialization formats were not. The corrected review checks that boundary
explicitly rather than repeating the prior assertion.

## Exact repair argument

- The complete adapter diff has only two changes: use
  `C.parse_json(line, C.Limits(max_bytes=65536))` for selected diagnostic lines;
  preserve the at-most-65536-byte raw stderr as hex before diagnostic parsing.
  Every original source/identity/budget/query/cleanup/transport assertion remains.
- Read the selected `modules/codec.py` parser. It bounds bytes before UTF-8/JSON
  decoding, rejects duplicate object keys, rejects noninteger/nonfinite numbers,
  handles malformed UTF-8/JSON/recursion failures, and bounds the resulting
  canonical encoding. It intentionally does **not** require input bytes to equal
  the canonical re-encoding. No mathematical acceptance parser is modified.
- The actual Node terminal object contains status, sequence, descriptor count,
  pipe counters, transport counters and a mathematical-acceptance boolean. Read
  `node_entry_services.mjs`, `ipc_wire.mjs` and `transport.mjs`: those diagnostic
  fields use integers, strings, booleans or null, not floating-point runtime
  census timing values. Thus the selected integer-only parser is compatible.
- The deterministic status-first prefix selects the existing Node diagnostic;
  exactly one matching object is still required. Sequence, zero counters,
  clean child exit and all original failure conditions remain checked. Allowing
  JSON key order/whitespace is appropriate for telemetry and grants no authority.
- Raw capture occurs after the child is closed/reaped and before `_closed_channel`
  parses it. Its hex representation is at most 131072 characters; the existing
  one-MiB report ceiling remains enforced. If parsing fails, the final failure
  report can still preserve the original diagnostic. Oversize capture itself is
  a retained failure, not a truncation relabeled as complete evidence.
- The complete selector diff changes only adapter path, four fresh input/state/
  operation paths, boundary02 name and temporary domain identity. The same
  distribution/input pins, 111-entry validation, explicit staging-only behavior,
  budgets and cleanup margin remain. No prior used artifact is edited.

## Gate remaining

Root must separately select the exact boundary02 request and inspect its actual
result and enclosing Job closure. This review is not an execution pass. Do not
infer boundary01 transport values from boundary02, source configuration or a
reconstructed JSON object. Keep both attempts and charge both costs. No product
rebuild, theorem production or broader networking campaign is justified by this
diagnostic correction.
