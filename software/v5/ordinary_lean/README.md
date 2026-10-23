# Ordinary Lean candidate

The default-direction implementation for inexpensive native library reuse,
without mandatory cryptographic certificate production. Not a completed v5
release or an externally deployable service yet.

`OriginalExpr` preserves ordinary Lean names, binders, universes and native
literals in bounded inert DAGs. `OriginalDecl` preserves safe declaration and
generated-group records. `CheckedExtension` directly calls the Lean kernel and
compares actual output; its parent environment is an explicit warrant precondition,
not something a caller can assert through a public endpoint.

Selected syntax and conditional-parent admission controls passed in immutable
local snapshots05/07. Both Std-backed method examples compiled in01. See
`research/cycles/v5-2026-10-22-native-library/OUTCOME-CORE.md` and `CHECKPOINT.md`
from the project root for exact evidence and outstanding integration.

The next work is exact dependency binding, protected persistence, real checked
library onboarding, ordinary-project import and discovery. Successful source
compilation or a content hash alone never constitutes network acceptance.
