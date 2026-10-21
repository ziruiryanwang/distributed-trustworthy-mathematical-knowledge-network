# Continued context: independent source and control review

2026-10-21, adaptive_audit. **PASS for the narrow source boundary and the finite
control preparation.** No product module, selector, control or native/proof
workload was run by this reviewer. Root may select the controls separately;
actual adoption and genuine I-to-M integration remain outstanding.

## Exact reviewed source

| File | Bytes | SHA-256 |
|---|---:|---|
| `continuing_context/client/workspace_atomic.py` |51319| `32e3b95ea2e6d3f8dc35d63000728e9e075a16de3e13fb1a0b718bce45e11773` |
| `continuing_context/mixed_claims/imports_atomic.py` |45513| `45b082863525fb08c1e8925e998113b55deff4b92482c8cf9b63cea2093725ad` |
| `continuing_context/controls.py` |27524| `1dc40485f144568d67bd751eca295d5abcde421c48365cf1a9901b5758cf67e7` |
| `continuing_context/API.md` |—| `b1f560061bb638ec7934a43c3354733da9fea59cf56b2f5a627e668f6c3d1c99` |
| `Select-ContinuingContextControls01.ps1` |5096| `20533624650c4a6fc3c93f8fddd972751afc66ab6ac4e3694d983d4f7de062b5` |

Product paths are under `software/v5`; selector/checkpoints are in this cycle.
Read selection, API, author checkpoint and final controls checkpoint `b24f2a53`.
Compared both product files against their authoritative predecessors and read
the inherited active/view/materialization/action paths, current evidence facade
override and real `MixedSourceOperation` lifetime checks. The complete diff is
one added method in each file; predecessor methods remain unchanged. Python
syntax was parsed as data, without importing or executing product modules.

## Correctness argument for the added transition

Write a READY state as `(D,R,O,L,V)`: mathematical/evidence data D, consumed
resources R, original owners O, finite limits/deadline L, and current sealed
view V. `begin_extension(V)` first executes the existing charged `require_view`.
That checks current live owners, exact object identity and sealed semantic state;
it then refuses an active batch. Only the four seal fields are cleared. D, O,
L, definition policy and prior counters are not reallocated or reset. The
transition's session-call charge remains consumed; inherited owner checks may
also consume their existing counters. No refund or new budget is implied.

Further imports/materialization run through existing rules. READY allocates a
new `SealedSelection` object; NEED retains no sealed view and remains extendable.
An old view cannot match the new object even if all mathematical data and the
selection-binding hash happen to be unchanged. Existing `MixedSourceOperation`
captures its exact view and calls `require_view` before each operative step, so
its captured capability cannot regain validity. The four-field revocation is
not deletion of evidence, proof checking or a new admission mode.

The public `advance_context` is inside the existing synchronous `_action`
serialization/charging/fail-stop wrapper. It validates the exact current
`AuthorContext`, requires READY, revokes its session view, removes the old wrapper
and calls dynamic `self._context_data`. There is no await/callback gap between
revocation and wrapper removal. The selected evidence subclass therefore keeps
its existing aggregate/I/mixed handling and fixed `definition_mode`; no fallback
to the old eager-only implementation is imposed by the new method.

The entire original session, grant, owners and maps continue. Any later exception
fails the enclosing operation; the prior view/wrapper is never restored.
Existing `extend_context` still refuses READY and handles only NEED. Direct
internal misuse, such as supplying a foreign view to `begin_extension`, closes
the session under its new catch. A stale lower-level author operation remains
invalid rather than being silently rebound to replacement mathematics.

The retained selection remains additive and finite. This does not add concurrent
snapshot branches, garbage collection, restored authority, a changed definition
policy or new owners. Original immutable direct-journal/representation conflict
rules still apply. The API correctly distinguishes mathematical equality from
owner/source-bound `selection_binding` equality.

## Focused controls and limits of their evidence

Read all nine selected methods and their fixture/loader/guards. They exercise
real session construction, materialization, view checking, added transition,
public action methods and a real old `MixedSourceOperation.prepare`. They cover:

- State/map identity and accounting preservation, new import and fresh reseal.
- Copied/foreign/wrong-type/unsealed/reused views; expiry, owner/source/trust
  withdrawal, semantic tamper and active batching.
- Exhaustion without renewal/refund; preserved interface-only policy and refusal
  of eager reinterpretation.
- Old author operation invalidation even when mathematics is unchanged.
- Public same-grant advancement, NEED followed by ordinary extend, and fail-stop
  malformed input after revocation, foreign context and old extend-on-READY.

The authority registries, foundation, installation/persistent trust, client
construction/owners, persistence/census and acquisition ledger are explicitly
synthetic. Actual cryptography, native checking and networking are forbidden.
The public positive starts with preloaded synthetic warrants; adding an actual
just-produced M is deliberately reserved for the integration pair. These tests
cannot be cited as an actual I-to-M contribution or a growth/performance result.

The author caught a fixture mismatch with the current origin-phase verifier
before execution. Final `1dc40485` supplies exact-class TrustBinding/current
source-origin fields and mocks only its local persistence check; real aggregate
and receipt `_active` paths remain in force. The earlier `202dc225` was unused,
not a failed test hidden by rewriting. Each intentional fail-stop variant uses
a fresh fixture; no old capability is revived to continue testing.

The loader stages the exact114 logical SDK map with four explicit replacements.
Read-only independent rehash confirms all114 current map rows and replacement
pins, with120 distinct physical files after runner/controls. The selector pins18
Python runtime files plus the distribution map,19 direct pins, and writes one
fresh selection without running it. Recommended unchanged allowance is60CPU/
120wall/384MiB/two processes,1MiB per outer log. No descendant workload is selected.
Nine tests/observations, no skips, forbidden calls or old test imports are
required for harness success. Outer clean completion and actual selected-source
binding still require independent outcome audit.

No blocking source defect found. This resolves the specific source-level READY
continuation obstruction, not the genuine endpoint until integration is observed.
The earlier `CORE-NEXT-REVIEW` endpoint assertion remains superseded and preserved.
No old campaign, install copy, matched timing pair or proof is authorized here.
