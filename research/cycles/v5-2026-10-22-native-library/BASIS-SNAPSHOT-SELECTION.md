# Selected actual-basis snapshot seam

2026-10-22. Root explicitly selects source-only implementation of
`software/v5/ordinary_lean/BasisSnapshot.lean` before this file is authored.

Implement the internal `checkAndWriteBasis (seed inventory : Lean.Json)
(moduleName : Lean.Name) (freshPath : System.FilePath) : IO WrittenBasis` path,
with distinct `SavedBasis`/`WrittenBasis` descriptors and actual environment.
Call the fresh narrow-copy `BootstrapProbe.receiveSeed` and gather only its
actual581 constants in the exact fixed seed[2]/inventory name order. Write
empty-import ModuleData with no environment extensions or IR. No duplicate
kernel receiver, owner-Init shortcut, peer JSON promotion or generic catalog.

The controller must authenticate and hold immutable exact selected seed bytes
724174B/SHA `a0acdc706f5e42dca21950c14db2307a18955c63ff953019aaff413d0a976001`
and inventory823690B/SHA
`c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0` before
parsing/passing their JSON. These are preconditions, not inferred from source
labels, JSON flags or a caller-supplied hash. Root owns actual pinning and later
runtime selection.

Do not change the successfully compiled LocalSnapshot source merely to share
small path checks. The basis wrapper may duplicate a small explicitly scoped
fresh-path/file-size guard. Fixed-basis receipt checking remains in the existing
receiveSeed body; the wrapper serializes that actual result, not expected data.
No tests/builds/runtime/Git are selected for this agent.

## Source implementation checkpoint

Implemented the exact selected wrapper in `BasisSnapshot.lean`,5485B, SHA-256
`8952d82460d972e4176becdc0f16e09015ccf8298c37898b55e7b7959057727a`.
It calls the existing checked receiver, collects actual kernel records in fixed
export order and writes a distinct basis chunk. It returns both the file
descriptor and actual checked environment for immediate ordinary continuation.
The formerly successful LocalSnapshot source is unchanged. The input byte/hash
precondition is explicit; the wrapper does not pretend fixed counts authenticate
arbitrary JSON. No compile or execution evidence yet.
