# Explicit definition-interface views

These are fresh source overlays, not changes to the installed distribution.
They let an agent opt into an authoring context that does not fetch missing
ordinary-definition bodies when its proof uses only their certified interfaces.
Default `eager` behavior remains available and is unchanged in meaning.

## Ordinary client usage

For a directly selected, genuinely admitted set of warrants:

```python
result = client.import_context(
    warrants, selected_exact_journals, group_openings, available_bodies,
    definition_mode="interface-only",
)
```

The four positional arguments have their existing meanings. The chosen mode is
fixed before the single import session is created. If more **type** declarations
are required, the existing `extend_context` continues that same session with
the same mode, grant and owners. It does not create a new allowance. Only a
READY live context may proceed to the existing `client.author(...)`, actual
admission and publication sequence.

For caller-directed acquisition through the optional helper:

```python
reader = SemanticReader(
    client, origin_candidate,
    limits=existing_reader_limits,
    definition_mode="interface-only",
)
# The caller still selects packets/members and fulfills returned demands.
status = reader.preview()
# Once structural readiness is reached, actual admission is still required.
result = reader.finish(admission_limits_by_packet)
```

Constructing a reader alone does not select or stage anything. Use its existing
`stage`, `select_member`, `resolve` and explicit supplier APIs as before. A
structural READY result is **not** mathematical acceptance. The helper passes
the same mode through preview and the subsequent live import.

Direct data-only prediction also accepts the explicit mode:

```python
status = client.preview_context(
    staged_tokens, group_openings, available_bodies,
    selected_members=chosen_members,
    definition_mode="interface-only",
)
```

Omit `definition_mode` to retain `eager`. No implicit retry, mode downgrade,
background acquisition or renewed budget follows from these calls.

## What can be omitted

Only a missing **ordinary imported definition** body can be deferred. Types
and references needed by those types remain required. Present bodies retain
their semantics and may demand further dependencies. Inductive declarations
and recursor rules remain complete/eager. This is not a general lazy-conversion
implementation or a guarantee that all proofs need only interfaces.

For the existing Lean frontend, a fresh untrusted request view represents a
deferred definition as a rigid constant with its exact type. The original
authenticated descriptor, original kind, body hash, reduction hints and
module identity remain separately stored. The final witness emitter consumes
**only those original descriptors**, retaining `moduleImportDef` rather than
turning the mathematical import into an axiom or opaque declaration. New local
axioms remain forbidden by the unchanged source decoder.

Lean may reject a proof that needs an omitted reduction or a hidden type alias.
Even if the frontend exports, the actual native checker must accept the final
witness. A native missing-body failure is fatal to that attempted admission:
no warrant or publication follows, and there is no automatic fallback or retry.

## Integration map

Select these logical modules together in the normal source map; do not import
the overlay directory as a separate identity-bypassing subclass or monkeypatch.

| Logical module | Source under this directory |
|---|---|
| `mixed_claims.imports_atomic` | `imports_atomic.py` |
| `mixed_claims.interface_projection` | `projection.py` |
| `mixed_claims.authoring_atomic` | `authoring_atomic.py` |
| `client.workspace_evidence` | `workspace_evidence.py` |
| `client.workspace_staged` | `workspace_staged.py` |
| `client.semantic_reader` | `semantic_reader.py` |
| `transport.semantic_staging` | `semantic_staging.py` |

Retain the already tested `transport.declaration_resilience` helper and the
existing `runtime_efficient` verifier/receiver/pin-phase selections. Preparation
and client owner profiles must pin the new projection module along with their
existing sources. No Lean binary, native checker, guest image or receipt trust
policy changes are selected by these overlays. Runtime tests and adoption
remain separately selected work.
