# Explicit candidate construction and complete successor export

2026-10-23. Source-only implementation by `successor_export` under root's
selected authoring-authority simplification. No Lean execution, native test,
catalog mutation, Git operation or experiment-snapshot edit was performed by
this assignment. Source review and root-selected finite execution remain gates.

## Why this boundary is useful

An ordinary local agent wants to use an accepted method and construct a new
proof. Requiring its authoring environment to reproduce all hidden receiver
semantics imposes work which is not a premise of final mathematical soundness.
The adopted `AUTHORING-AUTHORITY-REAUDIT.md` (`06dca04b` prefix) instead assigns
authority exclusively to complete checking against the actual accepted receiver.

This implementation does not weaken the receiver or claim that local success
implies receiver success. Local semantic mismatch may cause a later refusal.
Its expected benefit is avoiding irrelevant authoring correspondence and
ancestral proof work while preserving the same final acceptance event.

## Source and API

| File under `software/v5/ordinary_lean` | SHA-256 |
|---|---|
| `OwnerConstructCommand.lean` | `bded743c7ce6a76ebbfcc375dac78c4b240555acf246622ed483fe69d4abdffc` |
| `ConstructExportCommand.lean` | `6328e2a3d2f0588aaddf5f75d6ad56fb10757de3a847bd4efc2b45f795210260` |
| `SuccessorExport.lean` | `710622c74f2caced586b6fbc15440893c30dc7379379f159d21e829aecb1f788` |

New commands:

```lean
#ordinary_construct "<absolute-prepared-directory>" "<profile>" "<context>" "<basis>"
#ordinary_export_constructed Fully.Qualified.NewTheorem "<absolute-fresh-output>"
```

The construction command calls the separately authored
`OwnerConstruction.constructPrepared(owner, prepared, limits)`, with
`OwnerRebind.Prepared` and `OwnerRebind.Limits`. It retains the returned
`environment`, `interpretationLabels` and `introducedNames`; diagnostics report
`introducedSignatures`, `checkedUnits`, `scanNodes`, `encodedNodes` and
`payloadBytes`. The helper owns selective construction and its internal checks.

The new explicit low-level export entry is:

```text
SuccessorExport.selectedInterpreted(
  owner, interpretationLabels, introducedNames, targets, limits)
```

The earlier `selectedAbove`, `#ordinary_use`, `#ordinary_use_abstract` and
`#ordinary_export_above` retain their previous meanings and implementation.

## Construction command invariants

The command reuses `OwnerUse.absolutePath`, `readJsonBounded`, `headerField`
and `groupFilename`, preserving pre-parse byte/depth/integer bounds. It matches
the seven-field header and the three controller-specified expected identities,
bounds basis/target/group counts, enforces sequential once-only group reads,
and checks their complete read census and aggregate raw-byte budget.

Exact file authentication, canonical encoding, duplicate-key and alias rejection
remain the protected controller's duties. Identity strings and helper state
are conditional labels, never self-authenticating proofs of acceptance.

`ConstructContext` stores the source `mainModule`, profile/context/basis IDs,
the full finite prepared interpretation labels and the exact construction-
introduced names. Its distinct local `EnvExtension` is nonpersistent and cannot
be inherited as a warrant through importing another owner module. The getter
also requires the same main module. Repeated construction in that environment
refuses rather than overwriting the previous context.

Every fallible IO action—including final diagnostics—finishes before the
elaborator's one `modifyEnv`. Partial reads, construction failures or logging
errors therefore do not install a partial environment. The pure extension
update is applied only to the candidate environment returned by the helper.

Scratch signature declarations and any saved authoring artifacts containing
them are not warranted mathematical library artifacts. The command does not
publish them, accept them into a receiver, execute peer source or load a peer
binary module.

## Interpretation-based export invariants

`selectedInterpreted` validates bounded finite label/name/ID structure and
duplicates, but does not require unused mapped names to exist locally and
never compares their bodies or types. It uses the existing selected new-unit
closure scheduler and complete new-unit encoder.

For each **actually reached** external boundary reference:

1. Its exact ID must be in the finite prepared interpretation map.
2. The local record must exist and pass the existing safe-record filter.
3. It must be imported from the owner's local imports, or be recorded among the
   exact names introduced by this construction.

A newly authored current-module declaration sharing a prepared name therefore
cannot be silently replaced by an older receiver import. An export target may
not itself be any prepared boundary name. The command additionally requires a
nonimported, current-module full theorem record and at least one new unit.

The generic exporter still refuses an unbound axiom, checks permitted new
declarations, exports complete new theorem proofs, and keeps new generated
groups atomic. No boundary proof bodies are expanded. Ordinary theorem/definition
exports use point lookups; a genuinely new inductive group may invoke the
existing bounded actual group census.

The labels define the intended **receiver interpretation**, not correspondence
between owner and receiver. An imported local name may have a different type or
body. Such a candidate must pass the independent receiver's checking under the
accepted meaning or be rejected. Export success alone makes no mathematical
acceptance statement.

## Unchanged output and acceptance

The new command reuses the old absolute bounded fresh-output checks and opens
the output with `.writeNew`. It never mutates the owner environment. The bundle
schema remains `DMKN_ORDINARY_SUCCESSOR_BUNDLE_V1` with assurance
`INERT_OWNER_EXPORT_NOT_MATHEMATICAL_ACCEPTANCE`.

`boundary_imports` remains a selected lookup map, not a claimed exact import
list for each unit. The existing reviewed admission controller derives actual
per-unit imports from serialized evidence, checks each boundary label against
both the authenticated prepared map and actual accepted parent, and submits
all complete new units to the unchanged native receiver. Only the real checked
output, binding and commit event may establish acceptance.

For this bounded integration, retaining the existing roughly 833 prepared
labels avoids a new catalog API/provenance change. It is not a global-corpus
census or evidence of worldwide search scalability. Future pointwise protected
resolution is a separate interface design, not silently implemented here.

## Decisive remaining evidence

Independent source review must confirm the local installation boundary,
reached-name rules and unchanged acceptance provenance. Root may then select
the small changed-helper compilation and the existing substantial consumer
proof followed by real receiver admission. No broad correspondence campaign,
certificate production, ancestry replay, RAM escalation or repeated passing
test is needed to validate this specific architectural change.
