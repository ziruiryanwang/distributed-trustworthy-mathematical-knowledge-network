# Continue the repair and closure theories in ordinary Lean

This small source project contains two independently developed mathematical
modules. It is an authoring handoff, not a new theorem generator, a full commons
release, or evidence of faster research. Actual build/admission evidence is
recorded separately; the instructions below do not assert that you ran it.

## What to retain

Retain these five files together: `TheoryA.lean`, `TheoryB02.lean`,
`lakefile.toml`, `lean-toolchain`, and this `AUTHORING.md`.
Their only external mathematical dependency is `Init` from Lean 4.34.0.
No Mathlib, external Lake packages, generated input, Git submodule, LFS object,
or experiment-specific artifact path is required by this selected project.
The full compatible Lean runtime remains a separately required retained input;
the `lean-toolchain` label does not download or contain it.

`TheoryA` defines asymmetric idempotent repairs and finite safe schedules.
`TheoryB02` connects them to closure operators, with comparison results and
countermodels. These are substantive formal developments, not claims of
new-to-literature mathematics. Read the formal source for exact hypotheses.

The library target is `RepairConcepts`; its explicit module roots are
`TheoryA` and `TheoryB02`. The preserved failed `TheoryB.lean` in the research
checkout is not selected and must not be substituted into this five-file handoff.
There is no `RepairConcepts.lean` umbrella module: import the actual roots.

## Build an independently obtained copy

Use an approved complete Windows x86-64 Lean 4.34.0 distribution, including Lake
and compiler support. Obtain/approve source and runtime independently before
execution. Extract/copy the five-file project into a fresh working directory;
do not build in the project's frozen research-evidence directory.

Invoke the actual distribution's Lake binary, not an `elan` shim that might
install a toolchain. For example, replacing both paths with your chosen paths:

```powershell
& 'C:\tools\lean-4.34.0-windows\bin\lake.exe' `
  --no-cache -d 'C:\research\repair-concepts' build RepairConcepts
```

Run with an ordinary clean environment: do not override Lean/Lake executables,
library search paths or toolchain locations to unrelated installations.
`--no-cache` disables build-cache downloads. Offline sufficiency here comes from
having no package dependencies or custom hooks, Init-only source dependencies,
and the complete local runtime; it is not a build-network isolation option.
In this Lake version, `--offline` does not disable networking for `build`.
The package also disables Lake's local artifact cache; use a fresh working copy.
This command is not a security sandbox for arbitrary approved source code.
Lake may create `lake-manifest.json` and `.lake/` in your working copy; generated
artifacts are outputs, not retained private inputs needed by a new recipient.

The command checks/builds ordinary source and preserves ordinary frontend
metadata. It does not independently admit anything into a commons catalog,
establish source safety, or prove correspondence to an offered export identity.

## Develop a new direction

Work in your own copy. Add `MyTheory.lean` beginning with:

```lean
module
public import TheoryB02
public section

namespace MyInvestigation
-- Introduce definitions, models, conjectures and completed proofs here.
end MyInvestigation
```

Add `"MyTheory"` to the library's `roots` array in your copy and repeat the
ordinary Lake build. You may instead import `TheoryA` alone, or use this approved
project as a normal local Lake dependency from your own compatible project.
There is no prescribed research endpoint or network-wide list of tasks.
Unproved conjectures remain drafts; do not use `sorry` or new axioms as warranted
contributions. Recheck the actual completed work under your chosen axiom policy.

For commons exchange, select completed declarations through the supported
`produce-baseline` route and independently admit the resulting exact evidence.
Keep acquisition, execution approval, exact correspondence and mathematical
admission separate. A native build does not replace those boundaries.

## Exact retained source versus historical acceptance

The successful source bytes retained here have these SHA-256 hashes:

| File | SHA-256 |
|---|---|
| `TheoryA.lean` | `d2391e4a1a69d1ce57274ed011cd16734457e8239d2831a8e6eddd3349cbd9d9` |
| `TheoryB02.lean` | `d1397331c7b633fec21558189c2eaa45b76642c49d5ca3f359a01f6e623c5bb4` |

Prior episode evidence compiled corrected B under the logical module name
`TheoryB` using an explicit setup. This standard project instead exposes
`TheoryB02`. Equal source bytes do not establish identical compiled artifacts,
private generated names or export identities under that changed module mapping.
Historical independent acceptance reached receiver-local root
`03de3aa800949731dfc0823d8661374c9f216262211c9bfe1ac6afd930421e20`.
That is evidence about the original selected exports, not an acceptance token
for this rebuilt package or a root another receiver may simply trust.

A locally produced Git archive of the exact five-file selection can preserve
this handoff without experiment directories or build outputs. Record the exact
commit and compare archive bytes with that selection. Such a local archive is
not external publication, an open-source license, or independent hosting.
Licensing/public distribution remains undecided. A second copy on one PC does
not establish failure independence; toolchain and selected source retention
must both be arranged if future practical continuation is promised.
