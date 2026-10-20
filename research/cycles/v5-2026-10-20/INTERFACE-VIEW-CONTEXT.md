# Interface-only context implementation

Source-only checkpoint, 2026-10-20. Root selected this vertical change in
[INTERFACE-VIEW-SELECTION.md](INTERFACE-VIEW-SELECTION.md). No runtime,
Python import, native/Lean build, proof production or Git mutation was run by
this author. The installed distribution and all used predecessors are unchanged.

## Exact owned source map

| Logical source | Fresh physical source | SHA-256 |
|---|---|---|
| `mixed_claims/imports_atomic.py` | `software/v5/interface_views/imports_atomic.py` | `e38ac52a888f354e8e878984397a5c93c82ac38284b9e6fc89051063537aa459` |
| `mixed_claims/interface_projection.py` | `software/v5/interface_views/projection.py` | `d4e717606d449321d20c138f7b85153409198e016b064b4bad731e39c0a4ff87` |

The context predecessor is the actual installed-map source
`software/v5/runtime_efficient/mixed_claims/imports_atomic.py`, verified SHA-256
`2b80a02fb36e6332028595d0e4eea0a528a7dd087ec2cd1ade0b762db3514a49`.
The projection helper is new. Search owns the separate client, reader, staging
and source-operation overlays; root owns their combined map and selection.

## Contract

`materialize(..., limits=None, definition_mode="eager")` and
`_build_context(..., caps, *, definition_mode="eager")` accept exactly `eager`
or `interface-only`. The first successful materialization, including a NEED
result, fixes the session mode. A later mode change is refused. Session mode
and its origin are included in staged/sealed state checks; unsealed selection
uses the same mode-aware binding. Before any materialization the legacy
unsealed route remains eager.

Default eager packet/report/binding fields remain unchanged. Interface-only
adds the mode to the selection digest and READY packet; its cost census reports
the count of deferred ordinary definition bodies. All types remain traversed.
Only an absent body belonging to an ordinary imported definition may be skipped.
Present definition bodies, their references, inductive groups and recursor
rules preserve the existing traversal. Missing types or rule bodies still
produce demands. No descriptor, body commitment, reduction hint, owner,
opening or actual warrant is rewritten in the selected context.

`project_frontend_context(full_ready_context)` returns a bounded independent
plain-data copy and an inert report. In the explicit interface-only view, only
the copied descriptor's `kind` and `meta` change for an ordinary definition
whose body is absent: `opaque` and `{ "safety": "safe" }`. Name, universe arity,
type and value commitment remain exact. The helper does not fetch, execute,
publish, admit or modify its input. Its result is **not an authenticated
opening**. The existing Lean executable can install this rigid frontend
interface; the final native witness must instead use the original context.

The report fields are `schema`, `definition_mode`, `projected_definitions`,
`mathematical_acceptance=False`, and
`final_witness_uses_original_descriptors=True`. This last flag describes the
required integration contract; the report itself is inert, not evidence that
an arbitrary caller follows that contract.

## Assurance and limitation

[INTERFACE-VIEW-ARGUMENT.md](INTERFACE-VIEW-ARGUMENT.md) gives the acceptance
argument and body-only-chain comparison. This implementation preserves the
unchanged final relation and exact parent obligations; it does not establish
equivalence of transparent and opaque frontend environments. Missing semantic
data can still make elaboration fail or cause a typed final native body demand.
There is no automatic fetch/retry, fresh allowance, changed checker or new
mathematical acceptance rule.

Root caught a prelaunch continuation defect in the initial draft: an interface
NEED result had a mode-bound digest while the unsealed `selection()` still
computed the legacy eager digest. The revised source above anchors mode on
both NEED and READY and uses one binding function. No test was launched on the
initial draft. Review/controls must cover this exact continuation boundary,
not just ready-context projection.

This removes avoidable semantic acquisition for body-independent reuse. It is
not a completed full-cost growth result, a global scalability guarantee or a
claim that unavoidable type data and producer certification have zero cost.

## Independent review of the other owner's plumbing and root selector

After implementing the context/helper above, this author independently reviewed
the five search-owned overlay diffs against their actual logical predecessors:
tested `client/supplier_complete/{workspace_evidence,semantic_reader}.py`,
`staging_members/workspace_staged.py`, `transport/semantic_staging.py`, and
`mixed_claims/authoring_atomic.py`. No blocker remains in these inspected diffs
after the mode-continuation correction. This is not an independent review of
the author's own context/helper implementation and is not runtime evidence.

| Reviewed artifact | SHA-256 |
|---|---|
| `software/v5/interface_views/authoring_atomic.py` | `081d9d18d16d1cd68b40a5f3cf52493bac7e2e2dbdfb9bd632b72d74de235dbc` |
| `software/v5/interface_views/workspace_evidence.py` | `741e225ed1554e316cf2083dc25d28823b0bcb688a94fe9a0b37f3706fb7dadc` |
| `software/v5/interface_views/workspace_staged.py` | `23829a95bc047010487f16db39f6259cff35cb9bd75f722643f5e2a046851d76` |
| `software/v5/interface_views/semantic_reader.py` | `eb925191365d9f4daf04b86804f484e4096713f7ad9dd4b0919d1ab584bbe641` |
| `software/v5/interface_views/semantic_staging.py` | `e0a3223c0a92174f1ba8831e8a585e122f51d32fd17eff7f99f0d39284327ab5` |
| `research/cycles/v5-2026-10-20/Select-InterfaceView.ps1` | `a4560b0b9bef06994f5ed77e15a9148030d370b10b235837fd0168f69518e018` |

The reader passes one fixed mode to structural preview and actual live import;
the client keeps it through inherited continuation; the unsealed source route
uses the session mode. The client and preparation profile require the helper's
exact source pin. The source operation constructs a separate projected request
only for interface-only mode, retains the original context and binding, and
uses the original imports for final native rows and parent opening emission.
The default source request does not pay a new projection-copy cost.

The selector verifies the existing frozen declaration-control basis, all
retained source/runtime pins and explicitly reviewed new Python source hashes.
It rejects predecessor rewrites and paths outside the canonical source tree,
creates a fresh selection only, and chooses one finite 30 CPU / 60 wall second,
256 MiB, two-process native-free control envelope. It neither imports product
modules nor starts the test. Root still chooses the complete reviewed map and
separately launches; this source review does not authorize execution or imply
that tests have passed.

Accounting note: the original context's `frontend_packet_bytes` field remains
the preprojection context size. Actual request bytes are separately serialized
and pinned by preparation. Do not use the former as measured projected-network
traffic or a whole-workflow cost result.
