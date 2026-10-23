# Small ordinary owner source package

Source-only audit, 2026-10-23. No build, native check, install, Git operation,
runtime launch, old-source edit or old-state mutation was performed. Only this
checkpoint is new. Canonical root is
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Recommendation

Make one small Windows owner package with two isolated Lean build lanes,
the existing installation assembler, the existing generic contribution API,
and a thin persistent-owner CLI. Do not first build an arbitrary Lake-project
plugin, change admission/installation schemas, or package the experiment tree.

The concrete obstacle is reproducibility and ordinary invocation, not a missing
mathematical export mechanism. The current generic API already accepts caller
source, zero or more acquired targets and several output names. Its support is
still assembled from seven retained experiment build directories; the selected
receiver additionally needs an older exporter and three ignored v4 supervisor
files. These are specific, repairable source-selection gaps.

The smallest next source selection is: preserve/promote four exact existing
files, add a path-parameterized two-lane builder, extract the existing author
worker, and add a small CLI/profile loader. Leave core checking, portable
semantics, custody, schemas and the generic contribution implementation intact.
This is a proposal, not authority to rebuild or qualify anything.

## Selected receiver and exact source gaps

The audited reference is `experiments/v5-local-checks/ordinary-api-install-02`:
installation manifest SHA-256
`97d183aa62e11b67db2dbd77478af5a936256a36085fba0d38556193b574fcab`.
Its plan is `experiments/v5-local-checks/ordinary-api-install-02.plan.json`.

All six installed Python core files and both foundation files match their
current source-tree inputs. Seven of the eight installed Lean source files
match current `software/v5/ordinary_lean/` byte-for-byte:

| Core module | SHA-256 of selected/current source |
|---|---|
| OriginalExpr | `8278826700b17f8a926bebcf36e0408540ddfa3e84637ce4c8ff8f37c9dce72b` |
| OriginalDecl | `bfb5fc910808d9dc178977cfa6edeacf0b5cbfe7bd99bc6277ee11a456d516c1` |
| CheckedExtension | `4c3f3d600eda6319dd6d4578797e16ae6dc0ab81cf97ca4d7bce014081463ea1` |
| LocalSnapshot | `488a76f4b8599a95bdc748c5e89187bc55e23f63d34cf52952702d93ff68795c` |
| BootstrapSupport | `8a5771cc9f4e51cc0072959174bdc3a917bb0684b3dfdc8cdda2318bb8fd1bb0` |
| BasisSnapshot | `8952d82460d972e4176becdc0f16e09015ccf8298c37898b55e7b7959057727a` |
| OrdinaryWorkflowWorker | `442c2d479d4df6b1c7ee456cb521b8c760b54258a3f8d5fb71a15fa391c77f9b` |

Four exact selected inputs need a durable source-tree home before a clone-only
build can recreate this receiver without ignored paths:

| Selected input | Bytes | SHA-256 | Present source |
|---|---:|---|---|
| receiver OrdinaryExport.lean | 8611 | `ecab2be2b5ba3535547621e4d21d43ca5c8fbf23bd94cfe91d69a3916b9147bf` | `experiments/v5-local-checks/ordinary-native-admission-01/sources/software/v5/ordinary_lean/OrdinaryExport.lean` |
| supervisor commons.py | 41984 | `6ea16154f4533e80d2e4e27e12fb6fa0ab7abfa0ff2c52cfb7479c1a35a8c1c9` | `product-local/v4-library-commons-02/commons-v4/operator/commons.py` |
| supervisor run_stage.py | 30037 | `bdd2cbc28258f49ef08b678ba54b437ff541ef4deb0af4aa36795d2baa19b028` | same product's `receiver/helpers/run_stage.py` |
| supervisor domains.py | 4934 | `651db5f6bb707159c0d29dd6092174bfcebd1dc17b833fdfdacf7e2a66d8522a` | same product's `receiver/helpers/domains.py` |

The current `OrdinaryExport.lean` is not merely the old file with public headers.
It adds `DynamicBoundary`, `selectedFromBoundary`, dynamic stopping and boundary
references, lazy group enumeration, and makes `selected` call the shared
scheduler. Its SHA is `1d4df6817098f5ad9cd0106d98f39a6905a55be8b23484294b5c3d22653a7d4f`.
Keep it for authoring; do not silently substitute it into receiver provenance.
A proposed exact preservation path is
`software/v5/ordinary_lean/receiver_source/OrdinaryExport.lean`.

No `commons.py` source-tree copy was found. The existing `software/py` copies
of run_stage/domains are different bytes (`2b2a33de45490d124f0828f0e1de15e5c57c91facd326fd4ae054027c7952f4d`
and `1ff763737af54286b3c676dbb8cc4b30b8a34f87f48b9f4145b7ad0954a77ea7`).
Do not substitute them by basename. Preserve the three selected files verbatim
under a small source supervisor directory. Extracting/refactoring the old large
commons facade is optional later; its existing `supervise` and `limits_checked`
are sufficient now. Its unrelated v4 entry points need not be invoked.

The foundation is already in `software/assets/foundation/`:
`seed-verified.json` (724174 bytes,
`a0acdc706f5e42dca21950c14db2307a18955c63ff953019aaff413d0a976001`),
and `seed-inventory-json.json` (823690 bytes,
`c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0`).

This audit inspected source-tree files and the documented ignored boundary,
not the Git index/HEAD. Root must confirm the eventual selected source set is
tracked. `.gitignore` and `VERSION-CONTROL.md` already identify experiments,
product-local, runtimes and generated binaries as excluded and explain why
the present clone is not self-contained.

## Two native lanes and exact compile order

**Receiver lane:** compile in this dependency-safe order, with only this lane's
output plus the pinned Lean distribution visible:

1. OriginalExpr
2. OriginalDecl
3. CheckedExtension
4. LocalSnapshot
5. BootstrapSupport
6. OrdinaryExport — the preserved `ecab2be2...` receiver source
7. BasisSnapshot
8. OrdinaryWorkflowWorker

BootstrapSupport is independent of the first four and can precede them, but
parallel compilation is unnecessary for the initial small builder. Keep all
eight source identities explicit. Do not use authoring public variants here.

**Authoring lane:** one fresh flat helper directory can replace the seven
layered directories. This is the full transitive local import closure of
`PortableContributionExportCommand` and the wrapper's
`PortableOwnerConstructCommand` import, in dependency-safe order:

1. OriginalExpr — generated public form
2. OriginalDecl — generated public form
3. CheckedExtension — generated public form
4. BootstrapSupport — generated public form
5. OwnerRebind
6. OwnerConstruction
7. OwnerUseCommand
8. OrdinaryExport — current public/deferred source
9. SuccessorExport
10. SuccessorExportCommand
11. PortableOwnerConstructCommand
12. PortableConstructExportCommand
13. PortableContributionExportCommand

`OwnerConstructCommand` and `ConstructExportCommand` are not in this portable
contribution import closure. Neither LocalSnapshot, BasisSnapshot nor
OrdinaryWorkflowWorker belongs in the authoring lane. Lean/Std/Init dependencies
come from the owner-supplied pinned Lean distribution. Keep the two lanes out
of each other's `LEAN_PATH`; identical module names do not mean identical code.

Each retained module-public authoring build emits five companions:
`.olean`, `.olean.private`, `.olean.server`, `.ir`, `.ir.sig`.
The seven old helper directories contain 100 files for 20 module occurrences,
including shadows and two unused module names. The proposed closure is 13
modules, normally 65 such files; inventory the actual fresh outputs instead of
assuming this count. Existing AuthoringProfile checks *every* helper-directory
file. Omitting unused directories is cleaner than inheriting their pin burden.
This is directly relevant to the retained generic actual01 support-census
refusal: five unused ConstructExportCommand companions existed but lacked pins.

### Reproducible public sources

The existing `run_public_support_build.public_source` transforms only the
contiguous initial legacy import block: prefix `module`, make imports public,
insert `public section`, preserve the original remainder byte-for-byte. Read-only
in-memory application of this transform to current source exactly reproduced
the four generated hashes in both retained `PUBLIC-SOURCE-MAP.json` files:

| Module | Selected public source SHA-256 |
|---|---|
| OriginalExpr | `2064205249945563302b0ef4c0d3562ff1864730ee4644083a3b888433db2fb9` |
| OriginalDecl | `6a1adbab4496e351b3c66946c84a34eefc7270c214b684b44e77e10371dc89c8` |
| CheckedExtension | `60eba9cf947571f4336dd6e1f89a098b710a50f1e803a79d5691cc6292d2ae5a` |
| BootstrapSupport | `ccc6b864aba8e7239401a787930ea208e6d99653225e7565fd8a613b7db9e40c` |

Thus these four are not missing source-body variants. Reuse the exact small
transform and its source map in a new builder, not the old experiment-bound
runner. The old maps also mention an early OwnerRebind, but that is shadowed
by the later abstract-helper build and is not the version to select.

### Existing first-wins selection

The actual helper search order is the following `experiments/v5-local-checks/`
build directories, each with suffix `/lean-build`:

| Priority | Directory stem | Effective modules for the proposed closure |
|---:|---|---|
| 1 | ordinary-generic-contribution-build-01 | PortableContributionExportCommand |
| 2 | ordinary-portable-authoring-build-02 | PortableOwnerConstructCommand, PortableConstructExportCommand |
| 3 | ordinary-deferred-import-helpers-01 | OrdinaryExport, SuccessorExport, SuccessorExportCommand |
| 4 | ordinary-construct-helpers-02 | OwnerConstruction |
| 5 | ordinary-abstract-helpers-01 | OwnerRebind, OwnerUseCommand |
| 6 | ordinary-public-remaining-01 | OriginalDecl, CheckedExtension, BootstrapSupport |
| 7 | ordinary-public-expr-sync-01 | OriginalExpr |

At priority 3 ConstructExportCommand also wins if requested, but this closure
does not request it. Priority 4's OwnerConstructCommand is similarly unused.
Older SuccessorExport and ConstructExportCommand sources are genuinely
different, not safe substitutes. SuccessorExportCommand's repeated source
bytes match, but retain the priority-3 selection when describing old evidence.

All nine non-generated sources needed by the proposed authoring closure match
their first-wins retained source versions:

| Module | Source SHA-256 |
|---|---|
| OwnerRebind | `63ffaac12ae23d5e21ddbee7857e08f2a3f6d01a950b87a4128f27ae48594cc3` |
| OwnerConstruction | `04f605717af3b907195756455c2ec645e37e20ce9897c0510f47d7da24895ed3` |
| OwnerUseCommand | `cfeaaf28f48234de86000694c52a0350bd62f1120ae4bbd18d76ee5f42776313` |
| OrdinaryExport | `1d4df6817098f5ad9cd0106d98f39a6905a55be8b23484294b5c3d22653a7d4f` |
| SuccessorExport | `c68286f46711d0f2c2e13db972ffbc207feb6a4bfea157a53a251bfb5cb1d8c8` |
| SuccessorExportCommand | `1b5a381476d84b832d5200456aa6087c3c9e5e25d322c61076e86d9bf538a741` |
| PortableOwnerConstructCommand | `250a8dd1292c1dd5d228d69eaeb7abdbb5f0e9ad96c48a8b32d80203c27619b2` |
| PortableConstructExportCommand | `8251bc13836fde6620203752b9378bfafccefeef16587788221dec7ad7e95a8b` |
| PortableContributionExportCommand | `dc6988a6a237f482fed6f9055d8a248e430c8c99cb17c70a4a110774717e0182` |

Source equality and deterministic source generation do not prove identical
fresh `.olean` bytes, equivalent new installation identity, or successful fresh
compilation. A selected rebuild must report its actual output hashes and use
its own manifest. No migration of existing owner stores is implied.

## Python package and runtime boundary

Keep the existing installed six-file core together:
`ordinary_admission.py`, `ordinary_evidence.py`, `ordinary_semantics.py`,
`portable_evidence.py`, `portable_catalog.py`, `local_catalog.py`.
Keep its source modules distinct from the auxiliary authoring import root.

The authoring Python closure adds exactly these six local files:
`ordinary_contribution.py`, `portable_owner_request.py`, `owner_request.py`,
`portable_candidate.py`, `portable_preview.py`, `ordinary_preview.py`.
AuthoringProfile verifies the actual loaded helpers share the installed core;
the launcher must put installation `py/` first and must not ship a competing
copy of the six core modules on an earlier path.

Extract the small `author_worker` branch from `run_ordinary_api_producer.py`
into a standalone pinned worker with the same five arguments and
`--author-worker` entry point. It already has no fixture dependency: pinned
Python `-I -S -B`, sanitized Python/Lean variables, explicit helper `LEAN_PATH`,
restricted PATH, `-DElab.async=false`, and one compile to private scratch output.
The existing profile accepts a worker path, so this needs no core change.

For an immediately usable persistent owner, retain the existing OrdinaryStore
instead of inventing another custody implementation. Its current import closure
is eight Python files, even for local-only use:

- `transport/ordinary_acquisition.py`, `transport/http_provider.py`,
  `transport/clients.py`;
- `discovery/formal_features.py`, `discovery/discovery_store.py`,
  `discovery/authenticated_index.py`, `discovery/summary_wire.py`;
- `custody/module_store.py`.

These are namespace-package directories today. Keep their layout under one
support root. Carrying those eight files is smaller and safer initially than
extracting a new store solely to trim imports. Importing them need not start a
provider or authorize any network request. Higher-level discovery orchestration,
the optional body adapter, fixture drivers and services are not prerequisites
for local contribution. A later peer CLI can reuse the existing transport APIs.

The current selected runtime is Windows Lean 4.34.0 and Python 3.14.6 (the latter
read from the selected executable's file metadata, without executing it).
The plan pins Python `python.exe`, `python314.dll`, `python3.dll`, and Lean's
executable plus five DLLs. These nine pins are **named support, not complete
runtime closure**: Python stdlib/SQLite/SSL and Lean library modules still come
from the owner-supplied distributions. Document/provision those full external
distributions and accept explicit runtime roots. Do not claim hermeticity or
cross-platform support from the existing manifest. No download was attempted.

## Reuse the assembler; keep authoring adjacent

`ordinary_installation.assemble` is already a reusable file-only assembler.
Its plan fields are `schema, roles, compiled_dirs, support_groups, files`;
each selected file supplies absolute source path, bytes and SHA-256. It copies
selected support, checks external runtime attachments and emits a manifest.
It does not compile, initialize a mathematical basis, adopt a catalog or run
source. Its CLI already accepts explicit destination, plan/pin, runtime roots
and finite time allowance.

Generate that unchanged plan from the freshly selected receiver build and
source files. The core intentionally restricts `compiled_dirs` to the eight
`NATIVE_MODULES`. Do **not** put 13 authoring modules there or expand that schema.
Place authoring helper outputs and six helper Python files beside the receiver
installation, with a small local descriptor used to construct the existing
`AuthoringProfile`. Bind it to the new installation-manifest hash, list the
standalone worker and exact helper pins, and resolve package-relative paths
under the owner-selected package root. No new acceptance authority is required.

The current build runners are not this builder:
`run_public_support_build.py`, `run_workflow_build.py`, and
`run_deadline_compile.py` hardcode the canonical workspace/experiments/runtime
and reuse retained helper directories. The latter also accepts at most eight
modules per call. A new small builder should take source/runtime/output roots,
use the two explicit orders above, emit the four public source maps and exact
output census, and feed the existing assembler. It must not execute those old
runners as hidden prerequisites or widen their frozen allocations.

## Missing user-facing operation

`contribute_source(owner, parent_root, acquired_targets, source_body,
output_names, ...)` is a real generic API, but the caller still supplies profile
loading, owner/custody lifecycle and one original budget ledger. The body is
inserted after a fixed module/Init/authoring header. This is caller-chosen Lean
declarations/proofs in that supported environment, not an arbitrary Lake project
or arbitrary top-level module/import graph.

`run_generic_contribution.py` is deliberately not the user CLI: it requires a
selected source snapshot, copies a retained local experiment store, reads
selection.json pins, and asserts a fixture-specific definition/theorem pair
using two acquired methods. `select_generic_contribution.py` follows previous
receiver/build selections. Neither belongs in the normal package workflow.

Add only a thin owner command surface:

1. `init`: explicit installation/profile/runtime roots, fresh owner/custody
   directories, store ID and finite budget; run the existing initialization once.
2. `status`: report the existing local owner/context roots without rebuilding.
3. `contribute`: explicit existing owner, parent root, source file, acquired-target
   records (possibly empty), output-name records, fresh output directory and one
   finite parent allowance; call the existing API and return its actual result.

Keep exact structured Lean names/ExportIDs/UnitIDs in bounded JSON for the first
version rather than adding a name parser. Do not silently infer a parent root,
fork/copy an owner, reacquire the basis, renew allowances, repeat failed calls,
publish remotely or clean failed output. Report `ContributionError.report`,
including accepted-state information when later publication logging fails.
Owner-approved source is executable code, not hostile input; Windows Job limits
are resource containment, not a sandbox. Explicit acquisition/admission can be
added as the next thin command using existing APIs when needed.

## Why this precedes an arbitrary Lake plugin

This package immediately lets a new local owner build from selected source,
keep a persistent checked context and submit their own definitions/theorems
without a prior experiment archive. It uses the established native relation and
portable IDs. An arbitrary Lake plugin additionally needs project dependency
capture, import/search-path precedence, package/plugin execution provenance,
and a decision about exporting existing project environments. Those are useful
future integration questions, but they do not remove the four source gaps or
the missing owner command. A plugin can later call the same generic API/worker.

## Small next selection and stop condition

First select source-only preservation of the four exact missing inputs and
implementation of the builder/worker/CLI/profile descriptor, with disjoint
review ownership. Review exact lane separation, imported Python identity,
full helper census and unchanged original-budget/failure behavior.

Only then select a fresh finite two-lane build/package qualification using the
pinned runtimes and no retained experiment helper directory on any path. Check
generated public source hashes, fresh module inventory and the assembled
manifest. Any fresh output identity is new evidence, not reuse of saved PASS.
One separately selected package-only owner init and caller-authored multi-output
contribution can then exercise the new launcher boundary; no old basis/proof
campaign is resumed. An additional old-library stress suite, certificate system,
portability framework or arbitrary project plugin is not needed for this gate.

Stop when the selected source package plus explicit runtime distributions can
build and run that ordinary owner flow with no required experiments/product-local
path. This would qualify source reproducibility and local usability only, not
worldwide deployment, hermetic toolchain trust, useful-growth advantage,
cross-platform operation, arbitrary Lake imports or public distribution licensing.
