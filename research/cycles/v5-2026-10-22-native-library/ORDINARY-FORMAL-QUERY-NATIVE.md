# Native type-query discriminator: source preparation

2026-10-23; author `query_native_boundary`. Source only: no Python test, Lean
compile, owner operation, query execution, network operation or Git mutation
was performed. Root owns exact selection and launch after review.

## Decision-changing question

Can an ordinary local Lean file ask about a formal contract, with neither its
theorem name nor a proof, using the new type-only command and actual Python
parser? This is the only missing native boundary selected here. Pure key,
adapter and refusal controls remain a separate assigned discriminator.

The contract is independently specified as pointwise equality of two arbitrary
dependent functions: `forall a, f a = g a`. It is deliberately **not asserted
true**, and no proof is supplied. Dependent section variables `A`, `B`, `f`, `g`
must close correctly; unused `Nat` variable must disappear; ordered universes
must remain `[u, v]`. Only the already known basis symbol `Eq` is referenced.
No returned theorem type is copied to manufacture this query.

## Fresh source files

Paths are under `software/v5/ordinary_formal_query/`.

| File | Bytes | SHA-256 |
|---|---:|---|
| `native_query_check.py` | 12174 | `45c2a50b8d6a423846fe884ae5b42e1e55d25cad5f401593ceb36d234679971f` |
| `QueryNativeFixture.lean` | 1065 | `91e58051c4e32886a420fc3aad71971b53e8e52bad70b7ceadec846a02d18795` |
| Existing `OwnerQueryCommand.lean` | 3055 | `d488268d3e5118dcd121b504f051d3875d7e4d3d52badaf7198c9c86093fe59b` |
| Existing `formal_query.py` | 7811 | `7901236768784a399f9ae5c56b374d040bce56536b0a47a6ee85093440cabcee` |

The last two product sources are unchanged. The fixture contains exactly one
output-path placeholder. The harness substitutes a fresh owner-local output
path, preserving the template and generated actual fixture separately.
Before execution, the author moved `query_spec` computation before final
pin/budget validation; the table records those final source-only bytes.

## Exactly two native calls

1. Compile only `OwnerQueryCommand.lean`, against existing compiled
   `OriginalExpr` and pinned Lean 4.34 libraries. No C generation, native linking,
   complete package build or support recompilation is needed.
2. Compile the fixture importing that newly compiled command. A test-only
   wrapper invokes the **actual** `#ordinary_type_query`, comparing current-file
   declaration-name arrays immediately before and after it. This checks no
   declaration insertion in that command invocation. `foldStage2` inspects only
   local name keys, not imported proof terms, declaration bodies or dependency
   ancestry. Ordinary macro registration performed before the query is test
   instrumentation, not claimed product output.

Each native command runs under the retained exact Windows Job supervisor. A
small isolated child wrapper sets the Lean search path to the fresh directory,
the retained selected helper directory, and the pinned Lean standard library.
No current working directory or environment variable supplies an extra module
path. No native call is made by this source preparation.

The harness requires zero exit, clean process closure, no termination request,
zero diagnostic output and actual resources within the granted limits. It
retains all five generated companions for each compilation:
`.olean`, `.olean.private`, `.olean.server`, `.ir`, `.ir.sig`.

After native extraction, the harness loads the actual selected pure Python
closure (`ordinary_evidence`, `ordinary_semantics`, `ordinary_preview`,
`portable_evidence`, `portable_preview`, `formal_query`). It checks:

- The real native query is accepted by `read_native_type`.
- Ordered universe names are exactly `u, v`.
- Exact reference census contains only `Eq`.
- Outer binders are `A` implicit, then `B, f, g, a` explicit, with no `unused`.
- `Eq` exists exactly once in the fixed, package-bound basis inventory.
- Its already known foundation-relative SymbolID can form actual canonical
  bindings, a bound query document and the ordinary `declared-type-key` spec.
- All held input/output bytes remain unchanged at the final check.

This does not enumerate proofs or infer a portable ID from an arbitrary local
name. The selected fixed foundation supplies the known `Eq` mapping. Bindings
and search keys remain advisory, not warrants. Missing-symbol and malformed
syntax refusal tests are already assigned to pure controls; no additional
native negative or timing campaign is added here.

## Proposed exact selection

Use the unchanged runtime-only package:

`experiments/v5-local-checks/ordinary-current-relocated-smoke-01-payload`

Profile SHA-256:
`192dfee12ac186fbdac0634212b28c1c6324222da2b035f8f295ec764303a68d`.

Reuse all 156 runtime pins from the current relocated-smoke selection (or the
matching-native02 selection minus its two saved request/inventory additions).
They include the package, Python, Lean and retained supervision support. Add
five snapshot sources: the four query files listed above plus the unchanged
`tools/Run-V5-Check.py`. No adapter or owner source is needed for this boundary.

Suggested fresh run name: `ordinary-formal-query-native-01`. Its outer selection
would run the snapshot `native_query_check.py --package <above> --output
{output}/native` using isolated Python `-I -S -B`.

One inner allowance is **80 wall seconds / 50 CPU seconds / 1536 MiB**. Each of
the two commands receives at most **35 wall / 20 CPU / four processes**, reduced
by remaining allowance with 10 seconds of wall and CPU reserve. Complete child
Job CPU is charged once; missing CPU accounting retains the full grant and
fails. Final allowance checking includes native Job CPU plus harness CPU.

Suggested outer allowance is **90 wall / 60 CPU / 2048 MiB / eight processes**,
1 MiB for each captured stream. The outer Job is authoritative for whole-run
cost, including initial helper/pin work and final reporting. These are proposals,
not a launch or permission to repeat failure. Root must bind the actual exact
selection and preserve its single outcome.

## Reusable compiled command and claim boundary

On actual success, exact companions would be at:

`experiments/v5-local-checks/ordinary-formal-query-native-01/native/OwnerQueryCommand.*`

The result explicitly records their five lengths/hashes in
`compiled_command_artifacts`. Those exact outputs could be reused by root's
separately selected coherent query-package assembly, after saved-outcome review.
No companion hashes exist yet; this source proposal must not invent them.

Expected result is `PASS_NATIVE_TYPE_ONLY_QUERY`, not mathematical theorem
acceptance, query quality, discovery, global scalability, measured benefit,
real-user usefulness or completed v5. The user has no external project; this
is controlled interoperability evidence only.

## Native02 partial success and pure saved-output continuation

Later 2026-10-23: native01 failed to compile the original command's IO lift;
that run and source remain preserved. Root's fresh `OwnerQueryCommand02.lean`
(`f71bb36f23edff62b8e48fde803e159a93e1ec5f62541d11d357c59e79971992`)
and `native_query_check02.py` were executed once as
`ordinary-formal-query-native-02`, selection
`56b4cd0613f3753040f903386469d78f6b1ef6d6a6169a496da46e30da6430cd`.

Both actual Lean calls compiled cleanly, creating all ten command/fixture
companions and the 649-byte query. The actual parser, section-binder and exact
reference checks ran before a **harness error**: the approved fixed basis
inventory is operational JSON ending in LF, not an inert canonical evidence
envelope. Calling `ordinary_evidence.strict_json` on it refused
`JSON_LEXICAL_TOKEN`. The whole native02 run is **FAILED** and remains so.
Its outer launcher used 4.3129556 wall seconds and 4.015625 known inclusive CPU
seconds. Native child CPU is already inside that outer Job total, not additive.
No recompilation or repeated successful native call is justified.

Root therefore assigned a new **pure saved-output continuation**, now prepared
but unexecuted:

`software/v5/ordinary_formal_query/native_query_finish.py`

- 13,578 bytes; SHA-256
  `40b2b17e0c536c1987199970f5db795ab9d9e1826c95d2075636fcfa46fc0dd3`.
- Reuses inert read/pin/save/diagnostic-JSON/clean-record helpers from the exact
  already used matching harness `native_check02.py` (`8d0238e3...`). Its `main`,
  worker, compiler and consumer functions are never invoked.
- Verifies exact original outer/native reports, original selection, all five
  original/source-snapshot pins, all 156 runtime pins, all 16 saved input pins,
  all ten compiled companions, actual command/fixture source and actual query.
- Checks the original clean exit-1 outer closure separately from the two clean
  exit-zero native calls, their exact command logs and empty native streams.
- Reconstructs the fixture's single output-path substitution and verifies the
  actual command source equals the retained source snapshot.
- Runs the actual unchanged query parser, binder/reference checks, known fixed
  basis `Eq` mapping, binding helper and key/spec helper.
- Uses the approved supervisor's existing `strict` loader **only** for the exact
  bounded fixed inventory. It accepts its LF, forbids duplicate keys and
  noninteger numbers. Operational timing reports use the existing finite-number
  diagnostic JSON reader. `E.strict_json` remains unchanged for real inert
  queries and evidence.
- Places tripwires on process launch, sockets, SQLite, shell execution and
  `startfile`; no Lean, owner, database or network call is permitted.

Suggested fresh selection: `ordinary-formal-query-postcheck-01`, output
`{output}/postcheck`; inner 35 wall / 20 CPU seconds, outer 45 wall / 25 CPU /
512 MiB / two processes. Root selects exact source/runtime pins before launch.
No execution was performed by this author.

Successful continuation would write exactly three fresh files:
`REPORT.json`, `bound-query.json`, `bindings.json`. Report schema is
`DMKN_ORDINARY_QUERY_SAVED_POSTCHECK_V1`, status
`PASS_SAVED_NATIVE_QUERY_POSTCHECK`, and `original_run_status` remains `FAILED`.
It binds the original selection, outer result and native result, original
profile, command source, actual query, postcheck outputs and all revalidated
pins. `compiled_command_artifacts` maps the five suffixes to exact byte/hash
pairs of **saved native02 outputs**, not newly compiled copies. Source and
native reports remain untouched. The report explicitly requires independent
saved-output review and root adoption; it does not self-authorize packaging or
mathematical acceptance.

For root's assembly receipt, bind the new postcheck's outer `RESULT.json` and
`selection.json` plus these three postcheck files separately from the original
native02 receipts. Never rewrite the native02 `FAILED` result into a pass, and
never reuse native01 artifacts in this chain.
