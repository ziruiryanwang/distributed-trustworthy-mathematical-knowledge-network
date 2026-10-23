# Owner rebinding implementation checkpoint

2026-10-22. Author: `ordinary_native_controller`.

Source-only candidate:
`software/v5/ordinary_lean/OwnerRebind.lean`.
No compilation, execution, experiment, checker mutation, catalog admission or
Git operation was performed by this assignment. Root controls review and any
later finite compilation/integration. This is not yet a working command or a
completed v5 feature.

## Why this implementation is worth doing

A normal user already has an ordinary Lean project. Requiring that user to
replace its environment with a special checker snapshot, or reload all private
proofs in its dependencies, defeats the ordinary-library redesign. The helper
instead retains the actual owner environment and checks selected correspondence
to its independently accepted knowledge context. Existing theorem handles need
their accepted type interfaces, not original proof bodies. Missing declarations
still need full construction data and actual kernel checking.

The relevant endpoint is ordinary source use and reciprocal export of the
ReadFootprint method. That endpoint also requires root's protected request
preparation and selected-boundary successor exporter. This helper alone neither
demonstrates that endpoint nor establishes search or useful growth.

## Implemented internal API

`OrdinaryLean.OwnerRebind.rebindPrepared owner prepared limits : IO Rebound`.

`Prepared` is deliberately conditional, trusted-controller plumbing:

| Field | Meaning |
|---|---|
| `profileId`, `contextId`, `basisId` | Exact controller-authenticated identities. Their 64-character lowercase hex shape is checked, but shape is not authority. |
| `basisRows` | Array of `[basisSymbolId, normalizedLegacyRow]` pairs, taken from actual fixed-basis acceptance. |
| `targets` | Array of `[originalEncodedName, acceptedSymbolId]` pairs. |
| `groupCount` | Number of dependency-ordered group records. |
| `readGroup` | Trusted `Nat -> IO Json` callback for immutable, controller-selected numbered records. It is not a peer file-fetch API. |

Each normalized basis row retains its original five-field inventory shape. For
a theorem, and only a theorem already warranted by the fixed basis, the fifth
field is replaced by `[]`:

```text
[legacyName, 2, universeArity, normalizedTypeDAG, []]
```

No theorem proof data is requested or compared. Other basis kinds retain the
exact existing normalized inventory projection, including its selected
definition-height convention. Actual owner records are compared with
`BootstrapProbe.dagJson`/`inventoryRow`; the controller cannot replace that
comparison by an assertion. Basis theorem handles may be safe existing
`.thmInfo` or `.axiomInfo`; fixed genuine axioms and quotient primitives retain
their explicit fixed-profile restrictions.

Each group JSON value has this shape:

```text
["DMKN_OWNER_GROUP_V1", rows, optionalUnitArray]
```

Each row is:

```text
[originalEncodedName, mode, acceptedSymbolId, payload]
```

- Mode `0`: an already warranted theorem's interface. Payload is
  `[originalUniverseParameterNames, originalTypePacket]` using existing ordinary
  codec representations. The actual owner record may be a safe theorem or a
  safe existing axiom-shaped handle. Neither creates a new axiom or warrant.
- Mode `1`: exact non-theorem `DeclCodec.inventoryRow`. Transparent definitions
  require their real bodies and metadata; non-theorem opaques retain their
  actual values; generated records retain computation/group metadata. An
  axiom-shaped replacement cannot satisfy this mode.

`optionalUnitArray` is either `[]` or `[fullOrdinaryUnit]`. A completely absent
group requires a full unit. An existing single theorem does not require one;
when supplied, its proof is not decoded or semantically consulted, although
its encoded-node and byte costs are charged.

Generated inductive/constructor/recursor groups require their actual accepted
full inductive unit even when already present. That unit has no theorem-proof
history requirement: it carries group declaration and generated inventory data.
The helper checks expected-name equality with the supplied rows, actual common
`BootstrapProbe.owner` key and relevant group references. The controller must
obtain the **complete** unit from actual accepted evidence. A selected list of
names alone cannot establish complete generated inventory without another census
or check. The helper deliberately does neither a whole-owner census nor a replay
of an already accepted generated group.

## Algorithm and assurance boundary

1. Require a top-level owner (`asyncPrefix? = none`) with quotient initialization.
   There is no `unlockAsync`, second `importModules`, or environment replacement.
2. Validate the bounded fixed-basis correspondence directly against selected
   owner kernel records. Its selected semantic reference closure must be present.
3. Stream dependency-ordered group records. Existing complete groups are
   matched. Completely absent groups are decoded using **only previously bound
   names**, plus the decoder's permitted inductive self-types, then passed to
   unchanged `CheckedExtension.checkBatch`. Partially present groups refuse.
4. Ordinary singleton semantics can refer only to previous bindings, not their
   own name. Within-group references are reserved for generated inductive groups;
   arbitrary multi-record groups and mixed owners refuse.
5. Scan theorem types only, transparent/opaque data bodies, recursor rules and
   generated group references. Exact matching without dependency correspondence
   is insufficient. Missing proofs' construction references must also be bound.
6. Expose only genuinely newly checked hidden `.recInfo` records, using the
   previously reviewed `addConstAsync`/`commitConst`/`commitCheckEnv` pattern with
   actual checked records. No preexisting private records are copied/promoted.
   Register normal namespace prefixes using the small upstream rule.
7. Resolve each requested target to its exact prepared symbol identity; require
   both its kernel record and usable frontend view to satisfy the corresponding
   interface/exact-semantic comparison. Basis lookup is direct, not a repeated
   full basis scan per target.
8. Return the candidate environment and complete bound-name/identity mapping
   only after all checks pass. A future command performs one `modifyEnv` after
   this return. This helper itself never mutates the command environment.

The result includes interface/exact match counts, checked units, added names,
explicit scan count, encoded-node count and canonical input payload bytes.
These are construction/accounting outputs, not acceptance certificates.

The mathematical acceptance event remains the independently checked successor
against the actual accepted receiver context. A forged low-level Prepared value
does not establish its precondition and cannot legitimately promote anything in
the local acceptance catalog. Public assembly must wire preparation,
supervision, owner authoring and receiver admission together.

## Resource and import choices

Imports are only `BootstrapSupport`, `CheckedExtension` and `Lean.Namespace`,
using `module`/`public import` and `public section`. The actual current
BootstrapSupport imports are narrow; no `import all Lean`, compiler import or
legacy exporter module is added. Source inspection finds the required APIs
public. Runtime feasibility still needs actual root-selected compilation; it is
not inferred from import spelling.

Defaults cap 4096 basis rows, 8192 groups, 65536 total correspondence rows, 1024
targets, 1024 actually checked units, 65536 new names, 20 million explicit scan
nodes, 20 million encoded DAG nodes, 8 MiB per group and 64 MiB aggregate
canonical JSON input payload. Existing checker limits remain unchanged,
including 1024 units/batch, 65536 new names, 131072 stage-two names, 2097152
scan nodes, and finite heartbeat/recursion limits. Each missing atomic group is
currently one checker call; for the intended few missing method declarations
this is the smallest implementation. Large sequences of missing groups may
justify later batching if actual integration exposes stage-two scan cost.

The explicit aggregate scan counter charges both the helper's restricted-name
construction scan and the unchanged checker's corresponding declaration scan.
It does not claim to count every encoder operation or kernel reduction.
CPU/wall/memory supervision remains external. The encoded-node counter includes
ignored supplied optional units, not just rows actually used for matching.

The in-memory helper counts canonical JSON payload bytes. It is **not** a raw
file parser, file authenticator, whitespace-size limiter or security sandbox.
The launcher must authenticate/pin request and support bytes, enforce raw file
and aggregate byte/depth/number limits before parsing, and keep them immutable
during authoring. Native literal/foundation correspondence remains part of the
selected exact profile and controller's complete selected semantic closure.

## Remaining narrow integration work

Root owns `owner_request.py`, selected-boundary successor export and the future
command adapter. Request preparation must follow theorem *type* dependencies
for already available handles, but full construction dependencies for an absent
declaration. It must authenticate all names/IDs to the protected accepted context
and fixed basis. It must not infer existing theorem warrants from a public stub.

Before execution, review the fresh Lean source for API/type correctness and the
request producer for complete generated groups and dependency order. Decisive
changed-boundary controls are unbound theorem stub, transparent same-type/different
body, missing semantic dependency, partial group, failed later group without
caller-visible environment leakage, and wrong target identity/frontend view.
Generated-recursion exposure needs a runtime control only if the actual selected
workflow uses it. No such execution was performed here.

The original owner export/admission evidence, recovery source, codecs, checker,
receiver worker, fixtures and previous checkpoints remain unchanged.
