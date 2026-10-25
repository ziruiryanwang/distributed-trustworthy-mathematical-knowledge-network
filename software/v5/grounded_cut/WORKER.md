# Conditional grounded-cut kernel primitive

`GroundedCut.lean` is source-only until separately reviewed and selected. It is
not a CLI, accepted-root backend, independent theorem certificate or public
acceptance authority. There is no runtime module import, source elaboration,
native snapshot write, filesystem operation or caller-supplied environment.

## Lean API

```lean
OrdinaryLean.GroundedCut.check
  (seed inventory : Lean.Json)
  (concreteUnits signatureRows : Array Lean.Json)
  (newUnit : Lean.Json)
  (limits : OrdinaryLean.GroundedCut.Limits := {})
  : IO OrdinaryLean.GroundedCut.Conditional
```

Import the approved helper module `GroundedCut` normally as build support. The
function itself reconstructs an empty-origin mathematical environment through
the existing `BootstrapProbe.receiveSeed`; it does not use the helper module's
frontend environment or call `importModules`.

The protected controller must first authenticate the exact fixed files:

- Seed: 724174 bytes, SHA-256
  `a0acdc706f5e42dca21950c14db2307a18955c63ff953019aaff413d0a976001`.
- Inventory: 823690 bytes, SHA-256
  `c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0`.

Passing JSON of the same shape/count does not establish this precondition. Input
bytes must be bounded, canonically screened and authenticated before parsing;
the function's compressed-JSON count is an additional structural bound, not a
replacement for that controller boundary.

## Input and supported slice

`concreteUnits` contains complete ordinary declaration-unit JSON in dependency
order, with exact generated inventories. Definitions, safe opaques and whole
inductive groups are permitted as **existing concrete meanings**, not as new
outputs. Decode all units, then check them in one `CheckedExtension.checkBatch`.
No theorem or arbitrary axiom enters this batch. No nonbasis theorem signatures
exist yet, so a concrete declaration needing one is unsupported and refuses.
Generated semantic references and definition/opaque group metadata are checked
against the concrete/basis name set as well as the normal kernel checks.

`signatureRows` contains topologically ordered old theorem interfaces in the
existing shape:

```text
[encodedName, 0, exactSymbolId, [universeParameters, typeDAG]]
```

Every name must be new to scratch, with canonical parameters/type and only
earlier available references. The controller must establish its exact earlier
eligible theorem warrant, logical-root membership and compatible meaning. This
function validates the row and creates an internal safe axiom-shaped handle;
it does not infer grounding from the identity string or row mode.

`newUnit` must decode to exactly one genuine theorem, with its complete proof
and exact single-record inventory. It cannot name an existing scratch symbol.
The controller additionally proves absence from the **whole logical root**, not
only the selected scratch subset. New definitions, axioms, opaques, inductives
and within-event dependent theorem batches are outside this first output slice.

Each signature and the new theorem receive an explicit real-kernel Prop check:
construct temporary safe `DMKNGroundedCutPropGuard : Prop := P`, preserving the
exact universe parameters, in a throwaway environment. This deterministic name
is reserved in this lane; selecting it as a concrete/signature/output name refuses.
The temporary environment is discarded, never
installed, returned or retried. Then perform the ordinary axiom/theorem kernel
check. Thus `P : Prop` is not a frontend heuristic or an unchecked type annotation.

Immediately before and after the new theorem check, enumerate the entire bounded
scratch environment. Every actual inventory must match either the exact fixed
basis, a checked concrete record, a selected signature, or the single new theorem.
All nonfoundation axioms must be on the signature list. Unsafe/partial/unexpected
records, changed inventories and name/category overlap refuse.

## Limits and returned data

Defaults, which callers may lower within the source-checked range:

| Resource | Ceiling |
|---|---:|
| Concrete units / old signatures | 1024 / 1024 |
| Scratch names, including 581 fixed basis names | 65536 |
| Selected encoded nodes / explicit reference scans | 20000000 / 20000000 |
| Aggregate compressed input / one input item | 64 MiB / 8 MiB |
| Kernel declaration checks | 4096 |
| New-operation per-check heartbeats / recursion depth | 20000000 / 4096 |

For C concrete units and S signatures, a successful call performs exactly
`456 + C + 2*S + 2` top-level `addDeclCore` calls: the fixed basis, one concrete
batch's declarations, a Prop guard plus axiom per signature, and a Prop guard
plus the one new theorem. The existing fixed-basis receiver retains its own
20000000-heartbeat/10000-depth settings per declaration; lowering the new-work
limits does not change those fixed initialization settings. Its bounded trace
output is unchanged and must fit the outer supervisor's log grant.

Encoded-node counters cover selected concrete/signature/new packets; the exact
fixed basis is separately count/byte-bound. `scanNodes` charges explicit new
declaration-reference scans and their repeated `checkBatch` scans, generated
concrete semantic scans and signature type scans. It is not a measurement of all
kernel reduction, JSON serialization or inventory-encoding work. Two exhaustive
inventory passes and the fixed-basis receiver remain real costs. All kernel work,
parsing, serialization, memory and logs require the original outer whole-process
budget; structural counts are not substitute CPU or memory containment.

The `Conditional` result contains `theoremName`, actual `theoremInventory`,
`signatureLabels`, `concreteUnits`, `concreteNames`, `signatures`, `scratchNames`,
`inputBytes`, `encodedNodes`, `scanNodes` and `kernelCalls`. No environment or
scratch olean escapes. The controller binds these outputs to the exact request
and clean process-tree event; labels/statistics by themselves grant no warrant.

## Unchanged authority and performance questions

The missing protected path must still ground every selected summary, preserve
the interpretation into the logical root, bind global name freshness, maintain
eligible support, and atomically commit a distinct cut-origin event and indexed
result. Reopening and recursively reusing that result must not trust saved PASS
text or restore arbitrary scratch axioms. No such path is supplied by this file.

The controller must also preserve complete new proof claims for ordinary return.
A refused cut check is neither mathematical falsity nor permission to fetch more
ancestry, repeat work or increase the allocation. Do not claim performance from
the reduced packet alone: fixed-basis checking, repeated concrete checks, census,
index updates, migration and ordinary public return must beat actual native
snapshot restoration/batching under the selected workload.
