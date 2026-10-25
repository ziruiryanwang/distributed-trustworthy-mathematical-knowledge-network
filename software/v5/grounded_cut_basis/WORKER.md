# Fixed-basis-restoring grounded-cut worker

2026-10-24. SOURCE ONLY. This fresh successor removes repeated checked seed
reconstruction from the optional grounded-cut worker. No compilation, experiment,
mathematical acceptance, speedup claim or public accelerator adoption is supplied
by these files. Ordinary Lean/Lake authoring and ordinary native/batched admission
remain primary. The predecessor in `../grounded_cut` remains unchanged.

## Exact interface

`GroundedCut.lean` retains the `OrdinaryLean.GroundedCut` namespace inside its
distinct, separately selected support build. Its entry point is:

```lean
def check (snapshot : FixedBasisSnapshot) (seed inventory : Json)
    (concreteUnits signatureRows : Array Json) (newUnit : Json)
    (limits : Limits := {}) : IO Conditional
```

`FixedBasisSnapshot` contains only `moduleName : Name`,
`path : System.FilePath`, and `artifactBytes : Nat`. It is a protected-controller
input, not an independently verifiable claim. There is no caller-supplied
`Environment`, import list, extension root, parent or name-count option.

The driver retains four ordered absolute-path arguments:

```text
seed.json inventory.json request.json fresh-report.json
```

The request has exactly these fields:

```text
schema          = "DMKN_GROUNDED_CUT_BASIS_REQUEST_V1"
request_id      = existing exact operation identity encoding
basis_snapshot  = {module_name: encoded Lean Name,
                   path: absolute path string,
                   artifact_bytes: positive integer <= 1073741824}
concrete_units  = existing concrete-unit array
signature_rows  = existing grounded-signature array
new_unit        = existing single full theorem unit
```

`basis_snapshot` has exactly the three listed fields. The controller must derive
them from its authenticated protected descriptor; this is not a peer snapshot
upload interface. The report schema is
`DMKN_GROUNDED_CUT_BASIS_CONDITIONAL_OUTPUT_V1`. Its assurance remains
`CONDITIONAL_KERNEL_JUDGMENT_NOT_LOCAL_WARRANT`. A report alone cannot promote any
mathematical result. Fresh source/support identity, fresh cut state and the
live bound controller event separate this worker from predecessor acceptance.

## Authority before deserialization

The controller must, under the genuine source-owner and cut-owner locks:

1. Derive the descriptor from the actual committed **native basis operation**,
   not a claimed filename or an extension snapshot. The genuine initializer ran
   `receiveSeed`, checked the 456 fixed units and all 581 names, and serialized
   its returned kernel records through `BasisSnapshot.checkAndWriteBasis`.
2. Bind source store, foundation, basis root/module, zero-parent role, native
   operation, exact artifact path/size/hash, seed/inventory identities and the
   adopted runtime/implementation/support into the protected descriptor.
3. Authenticate exact artifact bytes once at the event boundary **before**
   unsafe native deserialization. Keep the approved bytes and support immutable
   throughout the event, with the original withdrawal and locking premises.
   Authenticate the fixed seed/inventory before parsing them too.
4. Bind the exact descriptor projection, request, live supervised process and
   returned conditional output; retain source eligibility, selected-root
   grounding, global name absence, clean closure and atomic protected promotion.

The Lean path cannot itself prove these premises. A saved success report,
matching hash, local-looking path, count or post-load census does not establish
genuine checked origin. In particular, the census cannot retroactively make
unsafe deserialization of previously unauthenticated bytes safe.

## Retained checks and intentionally removed work

The worker first validates bounded packet shapes/counts and charges the same
fixed seed/inventory and contribution JSON as the predecessor. These syntactic
preflights do not establish acceptance or add declarations.

It retains the seed source tag, fixed counts (456 descriptors and 581 inventory
rows/names), exact name-to-row binding, unique sorted basis names and required
roots. The controller's pinned fixed bytes remain essential: this worker does
not decode/re-kernel-check every seed descriptor.

It internally constructs exactly one `LocalSnapshot.LocalImportPlan`:

```text
basisModule = rootModule = snapshot.moduleName
modules = [{moduleName = snapshot.moduleName, path = snapshot.path,
            parentModule = none, artifactBytes = snapshot.artifactBytes,
            namesCount = 581}]
```

The existing `restoreLocal` is used with `maxModules = 1`, `maxNames = 581`,
`maxArtifactBytes = maxTotalBytes = 1073741824`, `maxPathBytes = 32768`.
It requires an ordinary single-link file and exact size, supplies only that
artifact, temporarily empties Lean's module search path, disables plugins and
extension loading, and restores private records. Its checks require quotient
state, exactly one matching imported module, no imports, no extension entries,
no extra constant names, and exactly 581 module constants. No concurrent use of
Lean's global search path is permitted in this one-shot worker.

Immediately after restoration, **before concrete declaration decoding/checking,
signature type construction or new-proof checking**, a full census verifies
every actual name and its fixed inventory row. No extra axiom/declaration is
allowed. The same actual-record safe/nonpartial and permitted-basis-axiom checks
apply. The predecessor's selected concrete declaration checking, generated
semantics scans, canonical signature types, kernel Prop guards, grounded
assumption construction, scratch freshness and one-new-theorem check remain.
The complete pre-new-theorem and final censuses remain as well.

The removed operation is precisely the per-event `BootstrapProbe.receiveSeed`
kernel reconstruction. It is not replaced with asserted inventory records or an
unverified environment. Native restoration **does read fixed basis proof bodies**;
the benefit sought is avoiding repeated fixed kernel work without adding a term
proportional to growing application proof ancestry.

## Conditional correctness argument

Assume genuine checked origin, protected descriptor derivation, exact immutable
artifact authentication, the adopted serializer/deserializer correspondence,
approved pinned runtime/helper code and all predecessor grounding/promotion
premises. Restoring the singleton recovers the previously checked fixed basis.
The full census provides an additional retained consistency check. Concrete
declarations are then genuinely kernel checked; each omitted old proof is replaced
only by a proposition signature grounded by the controller in an eligible earlier
root. The new theorem is kernel checked over exactly that classified context.
Substitution of those earlier warranted proofs gives the predecessor's same cut
induction, and protected atomic promotion binds it to the actual clean event.

This argument is conditional on native serialization/deserialization, not a new
proof of Lean's loader. `BootstrapProbe.inventoryRow` is not an injective encoding
of all raw kernel metadata: some definition/theorem/opaque `all` fields normalize
to `[name]`. Therefore inventory equality cannot replace genuine origin and the
serializer/deserializer premise. No cold public trust, malicious-source sandbox,
new certificate assurance or arbitrary native-module acceptance is claimed.

## Cost reporting and finite limits

For `c` concrete units and `s` signature rows, a successful call reports

```text
kernel_calls = c + 2*s + 2
```

Each concrete unit contributes one checked addition. Each signature contributes
one throwaway Prop guard and one checked assumption addition. The new theorem
contributes one Prop guard and one checked theorem addition. The removed 456
seed additions are not counted. `maxKernelCalls` retains its maximum 4096, with
minimum 2 instead of 458. Failed calls have no successful-output census.

`input_bytes` retains its prior meaning: compressed fixed seed/inventory plus
contribution JSON charged by the helper, not all process I/O. A new separate
`basis_artifact_bytes` count reports the positive exact restored artifact size.
It does not claim that hashing plus loading performs only one byte traversal.
Controller/support checks, snapshot hashing/deserialization, all fixed censuses,
JSON envelope overhead and supervisory work remain full-workflow costs. Existing
packet/item/name/node/scan/heartbeat/recursion bounds remain unchanged; snapshot
bytes have the separate finite 1 GiB ceiling. Root may impose tighter actual
process and artifact bounds in a reviewed later finite selection.

No metadata-check cadence is amortized here. No daemon, persistent environment,
retry, fallback, budget renewal, database migration or public protocol is added.

## Evidence needed next

Independent whole-path source review must bind this interface to the protected
descriptor/controller. Only root can select a later build or changed-boundary
test. A small unprofiled matched comparison should charge setup, artifact hash/
load, fixed census, concrete semantics, controller work and custody against both
the previous cut worker and an equally optimized ordinary/batched route. Source
shows removal of 456 additions; it does not establish net speedup or a useful
region over ordinary admission. If that useful region is implausible, shelve the
accelerator. This optimization supports continuation of theories; it neither
invents concepts automatically nor closes full deployable-v5 requirements.
