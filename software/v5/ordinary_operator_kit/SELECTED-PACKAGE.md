# Use the kit with an explicitly selected compatible package

The frozen `prepare.py` and `START-HERE.md` remain valid for their exact original
profile. Do not edit that constant. `prepare_selected.py` adds an optional entry
for the same public interfaces, including the fair-search successor and a fresh
build of either supported layout. Its current execution disposition belongs in
the separate review/results checkpoint; a source file alone is not a passed test.

Approve the source/build and native runtime independently. Select your package's
exact PROFILE hash from that approved build's receipt, then use:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons\operator-kit\prepare_selected.py' `
  --package 'C:\commons\package' `
  --profile-sha256 'REPLACE_ME_WITH_APPROVED_PROFILE_SHA256' `
  --request 'C:\commons-work\request-find.json' `
  --output 'C:\commons-work\prepared-find-01'
```

The wrapper requires the adjacent exact `prepare.py` and `compatibility.json`.
It reads bounded PROFILE metadata and verifies every known noncompiled auxiliary
role's actual bytes: 41 for the original layout, 43 for fair search. It requires one
coherent layout, not a mix of their loaders and APIs. It never imports those
product files. Generated native file pins and the installation-manifest identity
may differ across builds. The installation's core Python, supervisor, foundation
and native artifacts are outside this auxiliary-interface check; **the wrapper
does not verify or approve those installed components**. Operator approval and
the actual product loader must cover them. Its result is compatibility with the
known auxiliary interface, not complete package compatibility, release authentication,
compiler equivalence, mathematical acceptance or a security sandbox.

The original request schemas, exact reports, input/output path protections and
manual approvals are unchanged. Generated `arguments.json` and `RECEIPT.json`
carry the explicitly selected profile. Use the same structured-token launcher
instructions from START-HERE. The wrapper prints a compatibility observation
around the ordinary preparation receipt; it executes no product commands.

Known source hashes are pinned in compatibility.json, whose own hash is pinned
by the wrapper. Unknown code requires a deliberate reviewed compatibility update,
not a fallback, guessed schema or arbitrary profile override. The preparer still
does not authenticate reports: the actual product revalidates all selected state
and mathematical bindings. Package/source files must remain owner-controlled and
immutable during selection and operation. Local cooperative guards are 60 wall /
30 CPU seconds; use external containment if a hard process limit is needed.
