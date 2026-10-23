# Explicit trusted-project authoring backend

2026-10-23, `project_hook_design`. Root adopted the design and selected fresh
`software/v5/ordinary_project_package/ordinary_contribution.py` and
`author_worker.py` for source-only implementation. Implementation is complete
pending independent review; no product import, test, build or native execution
was performed. All predecessor source/package/evidence bytes remain unchanged.

## Smallest useful change

Retain one `contribute_source` request/bind/preflight/admit/retention flow.
Add an optional closed-data `TrustedProjectAuthoring` backend; it changes source
construction and approved worker invocation only. No arbitrary Python callbacks,
global monkeypatching, second acceptance implementation or new mathematical
authority. `None` preserves the existing source-body wrapper and worker argv.

The initial backend supports **newly authored target modules**, not arbitrary
existing-file migration, project builds, package installation or general header
parsing. Its caller body remains the existing bounded UTF-8 source argument.
An owner's editor may edit that body normally, using explicitly approved imports.

## Implemented closed configuration

- `module_name`: bounded dotted ASCII Lean module name; nonempty valid identifier
  segments, no path separators, quotes, traversal or arbitrary command text.
- `project_cwd`: explicit already-existing owner-approved working directory.
- `project_search_paths`: 1–16 explicit ordered already-existing directories
  containing compatible compiled project dependencies. Not an ambient LEAN_PATH.
- `imports`: 1–64 distinct module records `(module_name, meta: bool)`; render as
  bounded `public import` or `public meta import`, not arbitrary Lean source.

Use exact data types, fixed field sets and conservative bounds. These authoring
inputs are owner-trusted executable support selections, not remote metadata.
The installed Lean 4.34.0 runtime and pinned authoring helpers remain unchanged.
Project support is not advertised as hermetic or hostile-code isolated; do not
hash an entire large project on every contribution merely to imitate that claim.

Public constructor: `TrustedProjectAuthoring.from_document(document)` with exact
fields `schema`, `module_name`, `project_cwd`, `project_search_paths`, `imports`.
Schema is `DMKN_ORDINARY_TRUSTED_PROJECT_AUTHORING_V1`; import records contain
exactly `module` and boolean `meta`. Constructor validation performs no I/O.
`verify(check_budget)` revalidates data and ordinary existing directory paths
without a project census. CLI calls it before opening state; contribution
rechecks before authoring. Root's CLI author owns the bounded file/hash selector.

## Source and worker construction

The generated source is fresh under `output/owner-source/<module_name>.lean`.
Its explicit module root is `output/owner-source`; the module's relative layout
determines its Lean identity. It is distinct from the project's working directory.
The source uses `module`, Init, approved bounded imports, pinned meta helper
imports, public section, existing construction hook, exact caller body and export
hook. Hooks remain in the authoring module. Original project files are untouched.

The successor worker preserves the old `--author-worker` branch and adds an
explicit project branch. Invoke the installed Lean with `-DElab.async=false`,
`-R <generated-source-root>`, fresh scratch `.olean` output and generated source;
run Lean with the separately selected `project_cwd`. Scrub ambient LEAN/PYTHON
variables/PATH as today. No shell, Lake, toolchain resolution or dependency build.

Ordered `LEAN_PATH`: pinned helpers; selected runtime `lib/lean`; approved
project search paths. Lean 4.34.0 `Lean/Util/Path.lean` resolves the first matching
namespace root, not a later arbitrary file override. Explicit runtime precedence
therefore matters: simply placing project roots before Lean's automatically
appended runtime path could shadow Init/Lean. This route intentionally does not
support overlaying shipped helper or standard-library namespace roots.

Before launch, require generated source containment, fresh build/output paths,
valid ordinary selected directories and bounded arguments. Retain the exact
backend description, module root, cwd, import list and path order in REQUEST.
Preserve existing before/after source/request/helper pins and Job accounting.
Compilation alone remains only candidate production. Existing source limits,
candidate limits, binding, native checking, durable evidence/preview publication
and failure-after-acceptance reporting remain the sole unchanged continuation.

## File ownership and public integration

The two selected successor files were created by apply_patch as exact predecessor
copies, and their hashes were verified before narrow edits. Root owns source maps,
profile/manifest and packaging. `ordinary_api_flow` owns the new public owner CLI.
Its paired `--project-authoring <json>`/`--project-authoring-sha256 <hash>` selector
feeds this closed backend through existing `contribute`; omission is the old route.
Do not modify the current peer package during its selected reciprocal check.

## Source identity and static inspection

Frozen predecessor contribution SHA-256:
`c856d4b60e1324191207a918a42e37779e509a3c92f4ccd13f308dbda3e6f4f0`.
Frozen predecessor worker SHA-256:
`5af3d6c7aef81f5eee0a6b7d00b51d65fd010b4ab470947f69474cff9be0f353`.
Both predecessor hashes remained identical after implementation.

New contribution SHA-256:
`b8eefe6af368d8a7f5c498d563a12b31416c48c877ea471361eadd2a56a90b31`.
New worker SHA-256:
`19f9375fdf4b12cac05baeece6a750aa0d2d363112f51876d451f54c71ab2b02`.

Read-only literal-text comparison confirms the entire contribution tail from
the post-authoring `current = operation()` through binding, preflight, admission,
retention and failure reporting is unchanged. The original `author_worker`
function is also literally unchanged; only a separate project branch/dispatch
was added. Default generated source and argv remain identical by source analysis;
no execution-based compatibility result is claimed. Project argv is explicitly
bounded before launching; module names cannot inject paths or Lean commands.

## Decision-changing checks, not another mathematics campaign

Pure controls can check exact default-source/argv compatibility, import/module
injection refusal, strict data shapes, source-root containment, search-path order
and unchanged binding/admission calls. Review that backend branches end before
the existing binding phase and cannot supply arbitrary candidate IDs or budgets.
These controls cannot establish Lean import or real-project compatibility.

One actual compatible owner project remains unselected. Do not manufacture a
toy project and call it ecosystem evidence. Until a suitable project is supplied
or explicitly selected, keep the adapter's project compatibility unclaimed.
Ordinary package sharing remains the strong comparator: if the adapter's
translation/integration cost dominates selective checked exchange's benefit,
stop expanding authoring machinery and retain commons discovery/custody instead.
