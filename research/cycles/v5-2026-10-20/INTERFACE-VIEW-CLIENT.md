# Explicit interface view: ordinary-client and source plumbing

Source-only implementation checkpoint, 2026-10-20; owner `core_search`.
No compiler, native checker, proof generation, network operation, test execution,
installation, RAM inspection or Git mutation was performed by this author.
Root retains selection, execution, installation and adoption ownership.

## Implemented vertical path

An explicit `definition_mode="interface-only"` now passes through the ordinary
client and the optional `SemanticReader`, including data-only preview, genuine
admission, atomic context materialization and source authoring. The selected
mode is fixed for the client's one import session; inherited `extend_context`
retains it rather than silently returning to eager mode. Client and reader
liveness checks refuse a changed stored mode. The session overlay separately
anchors its own mode and exact selection binding.

The default remains `eager`. Its request bytes, result fields and staging
binding/data shape stay unchanged where no interface option was selected.
The eager source-operation path does not perform a new full-context projection
copy. A caller still chooses each acquisition and supplies explicit original
admission allowances. No retry, implicit contact, new grant or automatic mode
switch is introduced.

Source authoring receives the exact session's full READY record. In interface
mode only, `project_frontend_context` creates a separate proposal view for the
existing Lean executable. `MixedSourceOperation._context` is not replaced.
`finish()` builds external name bindings and final relation rows from the
**original** packet's descriptors. Therefore an authenticated ordinary
definition remains a `moduleImportDef` with its exact committed value hash and
reduction hints at the final native checking boundary. The frontend surrogate
is not sent as an authenticated opening or adopted mathematical fact.

The original unsealed `prepare_mixed_context` path now forwards the session's
fixed mode, including after a partial materialization. It cannot silently
reinterpret an incomplete interface selection as eager. Untouched legacy
unsealed sessions remain eager. Source/export bindings, exact root census,
local-only checks and the unchanged decoder's `SOURCE_LOCAL_AXIOM` prohibition
remain in force. A generated packet is still untrusted until actual admission.

The declaration supplier continuation from `supplier_complete` is preserved.
This change neither regresses to the older `supplier_resilient` client nor
changes its original accounting and fatal invalid-data behavior.

## Exact source selection

Every file below is a fresh successor under `software/v5/interface_views`.
Used predecessors and the installed distribution remain untouched. Initial
copying through `apply_patch` used normalized new-file line endings only;
no frozen predecessor bytes were normalized or rewritten.

| Logical module | Fresh file | Actual predecessor |
|---|---|---|
| `mixed_claims.authoring_atomic` | `authoring_atomic.py` | `software/v5/mixed_claims/authoring_atomic.py` |
| `client.workspace_evidence` | `workspace_evidence.py` | `software/v5/client/supplier_complete/workspace_evidence.py` |
| `client.workspace_staged` | `workspace_staged.py` | `software/v5/staging_members/workspace_staged.py` |
| `client.semantic_reader` | `semantic_reader.py` | `software/v5/client/supplier_complete/semantic_reader.py` |
| `transport.semantic_staging` | `semantic_staging.py` | `software/v5/transport/semantic_staging.py` |

Actual installed logical selection was resolved from
`experiments/v5-local-checks/distribution-connected-01-input.json`, plus the
separately tested supplier-complete overrides recorded in
`DECLARATION-CONTINUATION-IMPLEMENTATION.md`. In particular, the staged client
retains its existing explicit aggregate-member selection support.

These five changes require the two disjoint `core_growth` overlays:

| Logical module | Fresh file |
|---|---|
| `mixed_claims.imports_atomic` | `software/v5/interface_views/imports_atomic.py` |
| `mixed_claims.interface_projection` | `software/v5/interface_views/projection.py` |

Keep current `runtime_efficient` receipt verifier, mixed receiver and
`admission.pin_phase` selections together, and keep the tested
`transport.declaration_resilience` helper. Do not remap those to old files by
their logical names. No changes to `workspace_atomic`, `workspace_mixed`,
`workspace_validated` or their exact class identity contracts are needed.

Preparation-owner required source pins now include
`mixed_claims/interface_projection.py`. The concrete evidence client includes
the same module in its required origin/pin set. Normal source-map installation
must place it at that logical location; no monkeypatch, subclass identity
bypass, alternate checker or new binary is introduced.

## Source hashes at review handoff

| File under `software/v5/interface_views` | Bytes | SHA-256 |
|---|---:|---|
| `authoring_atomic.py` | 18,921 | `081d9d18d16d1cd68b40a5f3cf52493bac7e2e2dbdfb9bd632b72d74de235dbc` |
| `workspace_evidence.py` | 42,141 | `741e225ed1554e316cf2083dc25d28823b0bcb688a94fe9a0b37f3706fb7dadc` |
| `workspace_staged.py` | 16,440 | `23829a95bc047010487f16db39f6259cff35cb9bd75f722643f5e2a046851d76` |
| `semantic_reader.py` | 30,017 | `eb925191365d9f4daf04b86804f484e4096713f7ad9dd4b0919d1ab584bbe641` |
| `semantic_staging.py` | 10,991 | `e0a3223c0a92174f1ba8831e8a585e122f51d32fd17eff7f99f0d39284327ab5` |
| `README.md` | 4,418 | `e635f23c9b13119cfd0257d402e43ae8677e8ac5f4bf21b5cf1915c66003b188` |

Root's final exact selection must incorporate the final session/projection
hashes and independent controls; they are not implied by this author handoff.

## Public use and honest scope

`software/v5/interface_views/README.md` gives exact direct-client, preview and
reader examples. This option is intended for reasoning independent of hidden
reductions. Types, present bodies, inductive groups and recursor rules retain
their existing obligations. A hidden alias may prevent frontend elaboration;
a final checker may demand an absent body. Neither failure yields a warrant or
publication, and neither triggers retry or fresh authority automatically.

This is a concrete reduction of unnecessary semantic acquisition for an
explicit workload class, not proof of constant-cost import, universal frontend
completeness, affordable certificate production or final v5 completion.
Independent source review and changed-boundary controls are still required.
