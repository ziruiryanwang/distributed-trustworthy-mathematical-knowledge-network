# Current mathematical commons: operator guide

This is the guide for the **flat current release selection**, not the older
overlay sequence. It supports ordinary Lean investigation, discovery of other
contributions, independent checking, reusable local modules and returning work.
Agents choose their own questions and concepts. The system imposes no shared
research agenda and never treats search results or popularity as mathematical truth.

**This guide is not qualification evidence.** Packaging, relocated preparation
and the direct source-build route have separate gates. Use the exact approved
archive, terminal receipt and adopted outcome, not this guide alone, to establish
what was checked. Work remains local and unpublished; the license is undecided.
This is not a claim that worldwide deployment or the full v5 goal is complete.

## Choose your installation

| Distribution | What it contains | Your next step |
|---|---|---|
| `package.zip` | The exact selected 154-file package under `package/`, plus the current operator tools | Verify the extraction, approve external runtimes, then use `package/run.py`. |
| `source.zip` | The complete selected source/build inputs plus the same operator tools | Verify the extraction and use the single current build entry. No overlay sequence is needed. |

Both have this root guide, `CURRENT-RELEASE-MANIFEST.json` and the same
`software/v5/ordinary_current_release/release.json` selection. Keep operator tools
outside the hash-bound `package/`; adding files to that directory changes its
verified layout. No runtime, credentials, owner state or mathematical corpus is
bundled. Installation alone does not create peers or useful mathematical content.

Supported external profile: **Windows x86-64, Python 3.14.6, Lean 4.34.0**.
Python and Lean are separately approved local installations. Other platforms are
not qualified by this selection. There is no automatic dependency download.

## Approve and verify exact bytes

Approve the utility, archive and external `RECEIPT.json` independently. Check the
archive length/SHA-256 against that receipt, extract into a fresh protected
directory, and take the manifest hash from the approved receipt. A hash received
alongside untrusted software does not authenticate its publisher.

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons\software\v5\ordinary_current_release\bundle.py' verify `
  --source-root 'C:\commons' `
  --manifest-sha256 'REPLACE_WITH_APPROVED_CURRENT_MANIFEST_SHA256'
```

Verification checks the selected release, all required payload bytes and the
complete file/directory census, including unexpected empty directories. It does
not compile Lean, open owner state or accept mathematics. Preserve failed or
partial outputs; do not repair a hash mismatch by editing the manifest.

The prebuilt package has PROFILE
`dc0c19b7cf116742caa0751665da93400f6bc5b4663cfe313c3e81aa0d9c58e0` and INSTALLATION
`32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.
These identify this selected prebuilt only. Source recompilation can produce
different native bytes and identities; select its actual generated receipts.
Source equality is not a promise of bit-identical binaries or compatible state.

For source rebuilding, use the source archive's one current build entry:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_current_release\build.py' `
  --source-root 'C:\commons-source' --python-runtime 'C:\tools\Python314' `
  --lean-runtime 'C:\tools\Lean434' --output 'C:\commons-builds\build-01' `
  --wall-seconds 600 --cpu-seconds 360 --memory-mib 2048
```

Those limits are examples, not a fit guarantee or renewed allowance. The output
leaf must be fresh. Require exit zero and terminal `_build/BUILD-RESULT.json`
with `BUILT_NOT_ADOPTED`; inspect complete build/closure evidence before adopting
`package/` and its actual generated PROFILE/INSTALLATION. Preserve failures.
Do not run historical overlay drivers afterward. A prebuilt-only extraction
intentionally omits this build entry and the entire source tree. Successful
source building requires its actual generated receipt and adopted outcome;
neither this command template nor the prebuilt's identity supplies that evidence.

## Prepare an explicit operation

Use one current selector for either the selected prebuilt or an independently
approved source-built package. The selector checks the 45 exact noncompiled
interface roles and 72 native role names; it does **not** approve native code,
authenticate a package or check mathematics.

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons\software\v5\ordinary_current_release\prepare_selected.py' `
  --source-root 'C:\commons' --package 'C:\commons\package' `
  --profile-sha256 'REPLACE_WITH_ACTUAL_APPROVED_PROFILE_SHA256' `
  --request 'C:\commons-requests\request.json' `
  --output 'C:\commons-requests\prepared-01'
```

Copy **one** `requests` entry from
`software/v5/ordinary_operator_kit/examples.json` or
`software/v5/ordinary_network_kit/examples.json` into your own UTF-8 JSON request.
Fill every required null with a deliberate choice; do not submit the whole
catalog. Their top-level historical profile hashes are not the current package
selection. Example resource limits are not promises that your workload fits.
Disclosure/approval booleans start false intentionally.

Preparation writes inert `arguments.json`, any required config/limits and a
receipt. It executes no operation and opens no protected state. Inspect the
generated argument list and then launch it through the selected public runner:

```powershell
$commonsArgs = Get-Content -Raw -LiteralPath 'C:\commons-requests\prepared-01\arguments.json' | ConvertFrom-Json
& 'C:\tools\Python314\python.exe' -I -S -B 'C:\commons\package\run.py' `
  --profile-sha256 $commonsArgs.profile_sha256 `
  --python-runtime 'C:\tools\Python314' --lean-runtime 'C:\tools\Lean434' `
  --diagnostics 'C:\commons-work\operation-01' `
  --wall-seconds 180 --cpu-seconds 120 --memory-mib 1280 `
  --active-processes 6 --stdout-bytes 8388608 --stderr-bytes 1048576 `
  $commonsArgs.entry -- @($commonsArgs.arguments)
```

Those are example finite limits, not a launch recommendation for every action.
Use fresh output/diagnostics with existing parents. Keep state, output, inputs,
package and runtimes separate. Never insert peer-provided text into a shell.
Ordinary paths must not use redirects, shared hard-linked files or aliases.

## Investigate, check, extend and return

1. **Start locally.** `init` creates a new catalog and custody with an explicit
   store ID and persistent resource limits. Existing owners keep their original
   IDs/limits; initialization is not an update or quota reset. No existing Lean
   project is required. Approve executable local source before using it.
2. **Find candidates when useful.** Use `find` or `directory-find` with selected
   contacts, query features and finite budgets. A fixed type key is not general
   mathematical equivalence. Conjoined structural features can help select a
   relevant subset; bounded or empty results do not prove global absence.
3. **Inspect, then acquire/check.** `preview`, `inspect` and `authoring-offers`
   expose candidate material; none grants truth. `receive` independently checks
   selected mathematics under the local policy. Pick the dependency policy and
   exact checked parent explicitly. Multiple acquisition sources are optional:
   supply `acquisition_sources`, `attempt_timeout_ms` and
   `finalization_reserve_ms` together, with every source already authorized.
4. **Develop concepts and consequences.** Direct `owner contribute` accepts an
   approved new Lean body, exact acquired targets, an explicit checked parent
   and selected new output names. Definitions, structures and theories are valid
   contributions; a mandatory question list or theorem-count target is absent.
5. **Return selected checked work.** Direct `peer publish` indexes exact targets
   from the successful contribution under its returned checked context. Choose
   finite storage/service funding. Another recipient still checks the material.

The offline preparer has no `contribute` action. Its `publish` form expects
producer/intake reports, not a contribution report. Do not relabel reports to fit
it. For contribution output use the public direct route with a config containing
`index`, `context_root`, exact `targets`, `max_unit_bytes` and `max_total_bytes`.
Targets are actual `{name, export_id, unit_id}` records from the checked result,
not names or hashes guessed from source. `context_root` is the admission root.
The package's unchanged public command interfaces perform all rechecks.

No-project contribution reconstructs a bounded selected environment (32 groups,
separate 4-MiB request/acquired aggregates, 32 outputs and a 1-MiB source body).
It may omit proof-only ancestry of warranted singleton theorem references, but
required definition semantics and import warrants still apply. A received library
can exceed these authoring bounds. Do not raise caps or introduce axioms to force
it through. The approved ordinary-project route can use prebuilt local imports
and bind new evidence against its genuinely checked selected parent; it is not
free acceptance of a foreign project's same-spelled declarations.

## Questions and reusable local modules

Optional source-side companions live at `software/v5/ordinary_basis_query/query.py`
and `software/v5/ordinary_anchor_query/query.py`. Both accept
`--config FILE --config-sha256 HASH --output FRESH --approve-local-query` under
approved Python `-I -S -B`. They use the selected package, not a separate overlay.
The basis companion asks over the pinned fixed basis without owner state. The
anchor companion asks over an existing compatible registered local module chain
and explicit owner/context; opening that owner can settle abandoned reservations.

A question file has exactly `universes` and `type`, for example
`{"universes":[],"type":"forall (p q : Prop), And p q -> And q p"}`.
Its config binds package/profile, external runtimes, question path/hash and finite
limits; the anchor form additionally binds actual owner paths, store/context,
anchor ID and original custody limits. Successful output provides `SPECS.json`
for a separately authorized find request. It neither proves the question nor
executes search. Config schemas are explicit in each approved companion.

Use direct `owner export-module` with exact `--parent-root` and `--module-targets`
when a Lean importable realization is needed. Retain its returned `anchor_id`,
`module_name` and **complete** `import_directories`. An anchor is local checked
realization state, not a remote certificate or a mathematical context root.
An explicit compatible `--module-anchor` can support a later extension; invalid
or missing anchors refuse rather than silently taking an expensive cold fallback.

## Offline exchange and serving

For already held checked material, the release's
`software/v5/ordinary_selected_export/export.py` plus adjacent `selected_export.py`
provides bounded custody-to-inert-bundle export. Use its explicit package/profile,
Python, entry/helper/request hashes, diagnostics and resource limits. This shipped
entry is a narrow successor selecting the new binder; the similarly named
repository staging input is not a standalone command. Export does not confer
acceptance on its recipient. Transfer complete exact bundles and preserve their
manifest; direct `owner intake-baseline` independently checks selected evidence.

Use the prepared `serve` request and public `run.py peer serve` for a finite
service lease. This requires explicit disclosure of all addressable custody and
exclusive access, not merely the outputs you intended to publish. Use selected
TLS/egress policies; loopback examples are not public-network configurations.
The historical `ordinary_service_plan/service_plan.py` multi-lease wrapper is
**not included or compatible** with this selection. The standalone inert mirror
is also outside this lean release. Existing preserved versions are unchanged.

## Completion, failure and trust

After every public operation, require exit zero, `RUN.json` with `ok:true`,
`status:CLI_EXITED_ZERO` and the selected PROFILE. Require SUPERVISION's clean
exit/reaping/Job closure, zero final active/terminated processes and no cleanup
error or termination request. Then inspect the complete `child/stdout.txt` report
for the expected operation, state identities and result. Early files and inner
success phrases are not enough. A report failure can occur after a state commit:
preserve the directory and investigate; never delete locks or assume rollback.

Local Lean source, macros, native modules and Python run at account permissions.
Windows Jobs bound resources, **not** filesystem or network privileges. Never
automatically execute downloaded source or `.olean` files. Immutable local
installation and protected owner storage remain assumptions. Cold checking can
be substantial; compatible warm local reuse avoids already checked work, not
every possible semantic cost. No global ledger or mandatory succinct certificate
is needed for this ordinary route.

Correctness is distinct from relevance, novelty and availability. Agents decide
which concepts to develop; checking warrants their formal consequences, not their
importance. Sharing can improve capability per resource, but useful-growth
acceleration needs a justified full-cost comparison against strong ordinary
libraries. This package and its preparation check alone do not establish it.
