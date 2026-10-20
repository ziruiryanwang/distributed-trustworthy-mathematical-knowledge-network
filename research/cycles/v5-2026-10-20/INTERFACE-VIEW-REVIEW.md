# Interface-view independent source review and focused controls

2026-10-20, core_release. Canonical project guard passed. This is a source
review and a fresh unexecuted control suite, not mathematical admission, a
certificate, performance evidence, or final v5 completion. No native/proof
process, runtime installation, RAM investigation or prior test campaign ran.

## Disposition

The reviewed change preserves the mathematical acceptance boundary, conditional
on the existing exact-parent discharge and native-checker assumptions. It is
appropriate for one finite, independently reviewed native-free control run.
Actual retained-Lean frontend compatibility and native missing-value behavior
remain separate integration checks; this memo does not count them as run.

Root found an operability defect during concurrent review: interface-only NEED
used a mode-bound selection digest, but unsealed `selection()` initially
reconstructed the eager digest. The final sources correct it before execution:
the first successful NEED or READY atomically fixes the mode; unsealed selection,
subsequent materialization and source preparation retain it. Switching modes
requires a different operation, not reinterpretation of retained data. The
focused NEED-to-READY control below directly guards this correction.

## Consequential source checks

- `imports_atomic._build_context` defers only absent ordinary definition bodies.
  It still traverses every selected type, every present definition body and all
  recursor computation bodies. No arbitrary semantic-reference waiver exists.
- `materialize` binds nondefault mode into selection, commits it with the same
  atomic semantic update, and includes both mode fields in sealed state. Invalid
  mode, cross-mode continuation and sealed rematerialization refuse. Default
  eager hash inputs and packet fields are unchanged.
- `projection.project_frontend_context` copies a complete READY record, verifies
  equal outer/packet selection bindings and changes only absent ordinary
  definition `kind`/`meta` in that copy. Names, types, universe arity and hashes
  remain. The resulting object is explicitly untrusted proposal data, not an
  authenticated opening or proof that opacity equals transparency.
- `MixedSourceOperation` retains original `_context`; only the interface-only
  frontend request receives the projection. Default eager avoids the additional
  projection copy. `finish` constructs externals, parents and native rows from
  the original packet. Source-export selection/source/root bindings remain.
- `decode_source` retains `SOURCE_LOCAL_AXIOM`; an untrusted frontend cannot
  introduce an accepted local axiom. Foreign interfaces are reconstructed from
  exact original imports for the final checker, not trusted from frontend rows.
- `NativeRows.group` represents a missing imported definition as
  `moduleImportDef` with original body hash and reduction hint. Rust parsing
  retains `Definition` with `ValueSlot::Missing`, whose demand path is unchanged.
  The selected receiver still performs actual parent and native checks; a needed
  missing value fails without producing a warrant or publication. Current failure
  revokes that operation rather than implementing an automatic fetch/retry.
- The public staged preview, reader, direct import and inherited continuation
  preserve the explicit mode. Reader preview verifies returned mode before
  recording readiness. Source pin sets include the new projection module.

No further acceptance bypass or erroneous body-skipping branch was found in
these reviewed sources. This does not independently prove checker correctness.

## Theory review

`INTERFACE-VIEW-ARGUMENT.md` has an appropriately conditional conclusion.
For independently certified fixed-type definitions whose only dependency chain
lies in their bodies, eager acquisition follows the chain while absent-body
interface construction need not. This removes a real mandatory acquisition term
from our current system. It is neither constant-cost arbitrary Lean checking nor
an advantage over every equally optimized local library. Certificate production,
address lengths, type support, needed conversions and service costs remain.

Hidden type aliases can defeat elaboration or positivity checking. Refusal is
permitted; frontend completeness or semantic equivalence is not promised.
The correctness argument is that the original final relation remains necessary,
not that every frontend-generated proposal is correct.

## Focused control contract

Fresh file: `software/v5/interface_views/test_interface.py`.
SHA-256: `fa98cea5aad54cdf671530d44b5db404d2dc78c509be2c040ba8f9e240341f33`.

Ten explicitly named tests, without importing any predecessor suite:

1. Synthetic hidden body chains of lengths 1, 32 and 256 require one eager body
   demand; interface-only selected type visits/groups/demands remain `(1,1,0)`.
   These fixtures have no certificates and measure only structural traversal.
2. Missing type references still demand exact member/declaration data; present
   bodies still introduce their real dependencies.
3. Projection changes only missing-definition kind/meta, preserves original
   bytes, and leaves present-body/default-eager records unchanged.
4. Invalid modes and inconsistent projection bindings refuse.
5. The real pure native-row emitter retains definition kind, exact hash and hint.
   The local fixture uses a distinct body hash so it cannot accidentally provide
   the supposedly missing imported body through the shared body table.
6. The actual source decoder rejects a new local axiom.
7. Default eager selection digest remains exactly the prior digest construction;
   interface mode differs, foreign views and sealed reinterpretation refuse.
8. Interface-only NEED has a usable same-mode selection binding, then reaches
   READY after adding one explicitly inert dependency; cross-mode continuation
   and selected-mode alteration refuse.
9. Actual source-operation preparation projects the frontend while actual
   finish uses original imported descriptors and exact parent opening. Only
   onward packet emission is intercepted with an explicitly inert sentinel;
   no mathematical acceptance or authentic onward packet is asserted. Stale
   export selection refuses before emission.
10. Reader → public staged-preview body → actual structural preview, and public
    direct-import body → actual session materialization forward the selected
    mode. A stale returned preview mode refuses. This control bypasses owner/
    grant/custody authority with explicitly inert shells, not validation logic.

The session fixture deliberately bypasses constructor/installation/issuer
authority. It retains actual mode, selection, sealing, charging, context and
source logic; hash-opening validation is real but not mistaken for proof.
The test runner forbids `subprocess.Popen` and both asyncio subprocess APIs,
accepts the retained `--output` convention, and exclusively creates
`controls-result.json`. No socket, native, receipt or proof call is selected.

The loader explicitly selects the seven fresh logical overlays and three retained
runtime-efficient admission/receiver modules. A root selection must pin those
files, this test and the complete imported source graph. In particular retain
`client/workspace_validated.py` and `transport/search_validation.py`; no old test
fixtures are required. All tests remain **unexecuted** at this checkpoint.

## Reviewed source identities

All paths below are relative to `software/v5/interface_views/`:

| File | SHA-256 |
|---|---|
| imports_atomic.py | e38ac52a888f354e8e878984397a5c93c82ac38284b9e6fc89051063537aa459 |
| projection.py | d4e717606d449321d20c138f7b85153409198e016b064b4bad731e39c0a4ff87 |
| authoring_atomic.py | 081d9d18d16d1cd68b40a5f3cf52493bac7e2e2dbdfb9bd632b72d74de235dbc |
| workspace_evidence.py | 741e225ed1554e316cf2083dc25d28823b0bcb688a94fe9a0b37f3706fb7dadc |
| workspace_staged.py | 23829a95bc047010487f16db39f6259cff35cb9bd75f722643f5e2a046851d76 |
| semantic_staging.py | e0a3223c0a92174f1ba8831e8a585e122f51d32fd17eff7f99f0d39284327ab5 |
| semantic_reader.py | eb925191365d9f4daf04b86804f484e4096713f7ad9dd4b0919d1ab584bbe641 |

No used predecessor, installation or evidence bytes were edited.
