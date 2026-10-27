# Four-helper build preparation

Root owns a source-only bounded compiler adapter in this directory. Rebuild only
OwnerConstruction, PortableOwnerConstructCommand, PortableConstructExportCommand
and PortableContributionExportCommand in that order. The last two source copies
are byte-identical to ordinary_lean (respectively hashes
`8251bc13836fde6620203752b9378bfafccefeef16587788221dec7ad7e95a8b`
and `dc6988a6a237f482fed6f9055d8a248e430c8c99cb17c70a4a110774717e0182`);
both verified by the root copy receipt. Only the two assigned native successors
may change.

Use the existing Run-V5-Check supervisor as the single outer Job for the script
and its four sequential compiler children. Its selected wall/CPU/memory/process
and log limits cover the whole build; no per-module allocation or retry is added.
The adapter stages four source files, uses a fresh output directory first in
LEAN_PATH, then the pinned current package's unchanged authoring helpers, then
the selected Lean runtime. No receiver build, owner state, test, package assembly
or installation is part of this operation.

Retain input/output hashes, commands and compiler output. Check current PROFILE,
INSTALLATION, all selected base helper parts and final source identity, with
ordinary local paths and exact output census. The outer supervisor owns cleanup
even if the adapter exits or is interrupted before its final BUILD report.
The adapter is not a security sandbox or hermetic-toolchain proof.

Runtime selection awaits independent source/control review. A later package
overlay must replace only four Python files and the four helper artifact sets,
plus PROFILE, preserving every admission byte and all unrelated auxiliary/docs.
