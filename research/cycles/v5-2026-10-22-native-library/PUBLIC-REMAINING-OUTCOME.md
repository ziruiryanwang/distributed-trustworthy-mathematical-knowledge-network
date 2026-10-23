# Public-support remaining build: independent saved-output audit

2026-10-23. Reviewer: `admission_event_audit`. Read-only source/saved-data audit;
no compiler, test, native worker or prior campaign was rerun. No Git or source
mutation. The original failed operation remains a failure.

## Disposition

**The three successful support-module prefixes are reusable. OwnerRebind did not
compile.** Only its narrow source repair and new isolated compilation are needed;
there is no reason to repeat these support modules or the retained OriginalExpr.

Operation: `experiments/v5-local-checks/ordinary-public-remaining-01`.

```text
selection SHA 24aa7daa0ccdb293638f180a7ff6334f8881801fd21fea2589bd8c71fa4634c0
RESULT SHA    5fefce2368cc09e5e017122aa623ebf133c2f0b509ee201f8102b1f2d6122b01
source-map SHA e15c06ac2878981909f258c4e2f05036728b844eee6e44aafeef9024f1aed41c
```

The actual outer status is `COMMAND_FAILED`, exit 1, with the direct child reaped,
closed Job, zero active/terminated processes, no requested termination and no
cleanup errors. Worker Job CPU: 8.15625 seconds; wrapper CPU: 0.453125 seconds;
outer wall: 10.0706566 seconds; peak Job private commit: 655,523,840 bytes. Keep
this failure cost charged. It was neither a timeout nor an out-of-memory report.

## Actual compiler sequence and failure

| Module | Exit | Recorded wall seconds | Compiler diagnostics |
|---|---:|---:|---|
| OriginalDecl | 0 | 1.7672897 | Empty stdout/stderr |
| CheckedExtension | 0 | 1.5110961 | Empty stdout/stderr |
| BootstrapSupport | 0 | 4.1897714 | Empty stdout/stderr |
| OwnerRebind | 1 | 1.7716355 | Return-record syntax error |

Every actual command uses `-DElab.async=false`, the selected public-source root,
and its exact output path. The saved OwnerRebind stdout says:

```text
OwnerRebind.lean:456:70: error: unexpected identifier; expected '}'
```

This points to the multiline `return { environment := candidate, bindings,
targetNames := targets, ... }` expression. OwnerRebind stderr is empty. The outer
Python traceback reports `PUBLIC_SUPPORT_COMPILE_FAILED:OwnerRebind`, consistently
with the selected runner's nonzero-exit branch. No OwnerRebind artifact or final
`COMPILE-RESULT.json` exists; neither is inferred from the successful prefixes.

## Source/artifact correspondence

The audit independently hashes all seven immutable source snapshot files against
the selection. For all four legacy helpers it reconstructs the declared
header-only transformation: prepend `module`, change the initial imports to
`public import`, add `public section`, and preserve every remaining body byte.
Each full generated/source/body digest matches the saved map. The failed
OwnerRebind public source equals its selected original source exactly at
`a7fbb85189fbee3d816c822d56bb8642e48e24f8952776ec9439fea12b6f6e01`.

The generated OriginalExpr is byte-identical to the previously successful
`ordinary-public-expr-sync-01/public-source/OriginalExpr.lean`. Its five retained
artifacts match the current selection's exact pins. It was not rebuilt: the
actual sequence starts at OriginalDecl. The runtime import path is the new build
directory followed by that selected retained expression build, not the old
legacy admission build directories.

The new `lean-build` directory contains exactly these 15 nonempty successful
artifacts and nothing from OwnerRebind:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| BootstrapSupport.ir | 1470384 | `66d0a516746e7ee7346c56d91b2452b5ad1a259a8d57472eb1068256ef673ecd` |
| BootstrapSupport.ir.sig | 176 | `af27a3358ca762299bed575406518000b6d34995bffa10e46fbfa0c2d4f00463` |
| BootstrapSupport.olean | 527528 | `c02b2276ae18ac44252caedc6afd4c953200d9e98ccb14f729c62d091f977e09` |
| BootstrapSupport.olean.private | 3879072 | `7956d852691e7259369ff7b4300469153ce2fa8ed9f3f162bb4ee01d22a3394b` |
| BootstrapSupport.olean.server | 22072 | `0c222e73d933e052afaea5dc54832217bc6e8c603d7694e338c636836f9f3ce6` |
| CheckedExtension.ir | 220096 | `6f5e7e9b254cf2cd8adee3d18df752f764cc7e6e00bb11d569c630bfe0325ed2` |
| CheckedExtension.ir.sig | 176 | `5fb33f5280a5ec3ada4438cb2af1dd52b483dd1b25c4adc7b5ea68e5f43dfec8` |
| CheckedExtension.olean | 83928 | `1d486d4e6820c7c38c7ec5c70e6c496a12faa4b09589c5dc37ed7933a85fe89f` |
| CheckedExtension.olean.private | 701232 | `d9b310739f4e624d805a26c20b9c9819321e5094ccbe63408e59f91deebd1640` |
| CheckedExtension.olean.server | 5120 | `5d6c5172ea18244e8f32e9c8e290547e4b169b82612e1104cc828be0b9ff6814` |
| OriginalDecl.ir | 480840 | `10c687be4f4a5111a4a640bc56a9b9646230c64a797e835d157651cabc38cd21` |
| OriginalDecl.ir.sig | 176 | `cf45214135c7e5f2911ade9c7c0d84418d2d8b2838350c1dd3328d85e1724466` |
| OriginalDecl.olean | 89720 | `26ad96f8b74cdb00bf845e20bdf5464f65063cd93493879b47e7f6c5094350a9` |
| OriginalDecl.olean.private | 1141160 | `6a60ebb14b95d9e95433bfac2ed26b3d85f3b40e1e6f81afd9347645d3b50d5d` |
| OriginalDecl.olean.server | 8288 | `75b801270842fe141aa4d0e8d8bdddd34230b1687022518b96ed98d97805dc70` |

## Reuse boundary

Root may pin and reuse these complete public-module artifact sets in the fresh
OwnerRebind-only compilation after the narrow syntax change. Preserve both
source-map provenance and private/server/IR sidecars; an unrelated `.olean` with
the same filename is not a substitute. Header-publication changes are for owner
authoring support only; no existing receiver profile, accepted context, basis,
snapshot or prior admission artifact is changed or requalified by this build.

Compilation of these support modules is not actual owner rebinding, successful
semantic correspondence, source use, successor export, mathematical admission,
discovery or growth. Review of the new owner command and selected-boundary
successor exporter remains separately assigned.
