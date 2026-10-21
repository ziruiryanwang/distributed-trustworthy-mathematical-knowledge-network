# Independent incremental-native harness and selector review

2026-10-21. core_release. **GO for root's single bounded native-free control
selection.** Source inspection only: no tests, product imports, native calls,
builds, installation, Git changes or old campaigns were run. This is not an
actual outcome or a second certification of the independently reviewed product.

## Exact reviewed inputs

| Input | SHA-256 |
|---|---|
| `software/v5/incremental_native/controls.py`, 28,909 bytes | `08be67a1fe5a65f70650b1ed5c52b34987014a492e3648f216d679327487ac81` |
| `research/cycles/v5-2026-10-20/Select-IncrementalNative01.ps1` | `7468ba2697a0c8ffcdf851155e5f62490c6a5a05402f6637edc91e03d4c61008` |
| Selected successor `software/v5/incremental_native/mixed_claims/receiver.py`, 27,837 bytes | `5436569971c272b129fbaec480d51d57a1ec521d43fd4d4ad14133b786691d5b` |
| Harness scope `INCREMENTAL-NATIVE-CONTROLS.md` | `dab9f0de81e9668ecc45d29c70687aead3f539ece1905bb131fb3c3aff4a6d41` |

Product source review is `INCREMENTAL-NATIVE-REVIEW.md`, SHA-256
`b20d525730340424ab0b764a1f6c936d3b5e4e58a7b51d041e49296a873b377e`.
This review reads receive/binding/guard seams only to check the new harness's
model, expected errors and accounting. It does not duplicate that product audit.

## Selection and source isolation

The selector checks canonical cwd and pinned distribution input `d3519be1`, then
derives all 114 SDK physical sources from its exact map. It adds the frozen
runner, three separately qualified standalone-validation sources, and only the
two supplied reviewed incremental-native files: 1+114+3+2=120 physical inputs.
Every selected source is hashed; mapped source sizes are checked. The final
reviewed two-file set is exact, not a wildcard over a mutable directory.

The retained Python closure contributes 18 pins and the exact map adds one:
19 runtime pins. The command uses isolated/no-site/no-bytecode `-I -S -B` and
only the new snapshot harness. The outer selection is 45 CPU seconds, 90 wall
seconds, 384 MiB and two active processes, with 1 MiB stdout/stderr ceilings.
The script writes a fresh selection via CreateNew and refuses an existing
selection or output directory. It does not run the test itself or renew a
previous output/allocation. The retained runner separately validates originals,
copies the finite source snapshot, uses its existing bounded Job supervisor and
checks runtime/snapshot/selection bindings after execution.

The harness stages 114 logical modules from that immutable snapshot; only
pin-phase `ac7ed228`, imports `8a831337` and receiver `54365699` replace the
mapped originals. It checks each selected/copy hash before imports and pins
runtime import origins to the fresh selected-code tree. The extra standalone
receiver is an unused retained source, not another imported receiver or old
test helper. No external mathematical fixture or native executable is needed.

## The fixture's real and simulated boundaries

The fixture deliberately creates exact-class receiver/issuer shells without
constructors. Its local TrustDomain/binding and source files are real, with
actual bounded filesystem reads and pin/origin checks. The actual receiver
`receive`, parser, exact native-output binder, graph/closure checks, final
packet readback, handle descriptions, packet export and revoke/close bodies run.
This is a controller test, not installation/adoption validation.

The supervisor is replaced by a local fixture that writes a **fabricated**
native transcript and process report. It never executes the pinned inert text
file. `bind_native` still binds the transcript's exact input digest/length,
ordered parent journals and target journal. Reports mark the fabricated process
evidence; stdout must retain the production exact schema for the real binder.
The 0.25 CPU value is explicitly an accounting probe, not measured worker time.
The fixture's limit validator is also a simple copy: assertions check the
requested limits, not the production supervisor's independent limit validation.

The main guard forbids subprocess construction, os.system, socket construction,
and actual I/A receipt receive calls; any recorded forbidden call fails the
whole campaign even if caught by a negative test. All structural witnesses have
empty receipt/frontier lists, so no fabricated receipt handle is used to
discharge a real frontier. Constructor adoption, live I/A frontier rejection and
native mathematical validity are outside this harness. Their unchanged source
checks and prior separate evidence must not be relabeled as newly exercised.

## Decision-changing assertions

All nine explicitly selected methods have relevant assertions rather than
success-only smoke checks:

- A, A+B, A+B+C require three simulated executions and three cache hits;
  exported complete packets remain exact. Each hit position lacks native input,
  process and command files and carries the explicit no-execution observation.
- Changing canonical witness bytes while preserving the target journal forces
  a miss. The unchanged child may hit only after its current parent is newly
  established. A memo alone cannot satisfy a missing parent in the new packet.
- Exact self/profile/image/foundation/policy/ordered-parent/rank mutations and
  changed output summary/rank refuse. A copied foreign entry is denied by exact
  owner identity without revoking the foreign owner.
- A failed second miss, changed packet readback and deadline failure after
  RESULT writing clear both old and pending memo/handles. The saved result is
  explicitly pre-promotion and is not sufficient authority.
- Last-successful-packet replacement, a cold fresh owner and close/reuse refusal
  are checked. Tests do not invoke a nonexistent report-restoration authority.
- Tiny actual byte/cardinality limits and the hard 16-entry cap are checked.
  The 16-MiB branch is an explicit arithmetic probe, not a large allocation or
  a claim that the empty dictionary is a real at-cap cache. A test-only one-entry
  retention adapter demonstrates that a skipped entry causes a later miss.
- Attempts, submitted bytes and full-graph CPU reservations remain charged on
  all-hit packets. CPU/output reservation refusal is exercised despite a warm
  memo. Simulated actual-worker observations increment only on misses.
- Wrong native input digest, ordered parents and target conclusion hit the real
  binder's refusals; a changed native input file hits the actual readback refusal.
  None of these denied paths may seed the memo.

The test mutations affect only fresh control-owned state/files. They do not
rewrite used product bytes, prior results or fixtures. Tear-down closes each
shell and asserts no pin/trust validation phase remains live. The output uses
CreateNew and contains method selection, observations, source bindings,
failure/error/skip counts and forbidden-call records.

## What a future PASS would mean

A passing saved outcome would qualify the controller's exact conditional-result
reuse boundary under the disclosed simulated checker model. It would not prove
mathematical acceptance, a real process speedup, constructor installation,
cryptographic soundness, cold-owner scale, net useful growth or full v5.

The warm-prefix consequence is primarily theoretical: retained exact checks can
avoid repeated native invocations while current premises are rebuilt. These
controls test the implementation assumptions cheaply. The root should not
rerun prior mirror/standalone/proof campaigns merely because this small suite
passes. Any consequential real integration requires a separate marginal-payoff
decision. The outer saved report, not the fixture's fake worker numbers, must
be used for actual CPU/wall/closure accounting.

No blocking harness/selector defect was found by this source review. Execution
and independent actual-outcome adoption remain pending and belong to root.
