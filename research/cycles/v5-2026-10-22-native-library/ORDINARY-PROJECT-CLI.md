# Optional owner-selected project authoring CLI

2026-10-23, `ordinary_api_flow`. Source-only checkpoint; canonical guard PASS.
No Python import, command invocation, build, service, test or Git action was run.
Root owns successor profile/package integration and any later exact selection.

## Selected successor and preserved predecessor

New source: `software/v5/ordinary_project_package/owner.py`, SHA-256
`fed0c9a03833d3ab16338eb84accd84d1458e17d712431260bdad0ca3950f74b`.
It is a narrow successor of frozen `software/v5/ordinary_package/owner.py`,
whose unchanged SHA-256 is
`91359645d82ee556de37637bae74da9ab1aaabad3a4d1678346f761d54b737cb`.
The peer package and all old used source/state/evidence remain untouched.

This source implements only public input selection for the approved
ORDINARY-PROJECT-ADAPTER-IMPLEMENTATION and ORDINARY-PROJECT-HOOK-CONTRACT.
It is not a second preparation, binding, checking or retention flow.

## Public delta

`contribute` accepts two new optional arguments:

```text
--project-authoring FILE --project-authoring-sha256 HASH
```

Supply both or neither. Either option on `init` or `status`, or a partial pair,
is refused before owner state opens. HASH must be an exact lowercase SHA-256
digest selecting FILE's actual bytes; it does not authenticate the project or
prove its correctness. FILE uses the existing absolute, ordinary nonredirected,
single-file reader and must contain 1 through 65,536 bytes of UTF-8 JSON.

The new owner-only JSON parser rejects duplicate keys at every level, invalid
UTF-8/syntax, all numeric/nonfinite values, unterminated strings/brackets and
nesting deeper than eight containers before the general parser is called.
Booleans are needed for import visibility; the inert peer/evidence parser is
not changed. Exact fields and types are validated by
`G.TrustedProjectAuthoring.from_document(document)`.

The closed schema agreed with `project_hook_design` is illustrated below.
These names and paths are placeholders, not a selected or tested project:

```json
{
  "schema": "DMKN_ORDINARY_TRUSTED_PROJECT_AUTHORING_V1",
  "module_name": "NewWork.Contribution",
  "project_cwd": "E:/owner-approved-project",
  "project_search_paths": ["E:/owner-approved-project/compiled"],
  "imports": [{"module": "Project.Support", "meta": false}]
}
```

The backend constructor enforces bounded dotted ASCII module names, exact field
sets, 1-16 ordered distinct absolute non-traversing search paths, and 1-64
distinct module imports with exact Boolean `meta`. The CLI calls
`backend.verify(allocation.check)` before `OrdinaryStore` or
`OrdinaryAdmission.open`: cwd and search roots must already be ordinary existing
directories. This bounded check does not scan, build, import or execute them.
The contribution backend rechecks the selected directories before native use.

Profile/bootstrap validation and existing source, selected-ID, limits, parent,
output and protected-path validation remain before owner opening. Only after
config pin, shape and directory validation does the CLI pass the closed backend
as `authoring_backend` to the existing `G.contribute_source` call. No callback,
arbitrary Python object, native argv or acceptance flag is loaded from JSON.

## Default compatibility and evidence boundary

Without the pair, the keyword dictionary is empty: no `authoring_backend`
argument is supplied, no project file is read, and the existing default
contribution path is selected. Init/status, original allocation accounting,
owner/custody opening and closure, native budgets, output/source bounds and
failure-after-acceptance reporting remain unchanged. The new parser has no
effect on existing custody limits, source inputs or inert mathematical evidence.

When FILE is supplied, the terminal report also records its requested file and
digest as `project_authoring_selection`, including on failure. This describes
the caller's selection, not successful validation or mathematical acceptance.
The backend retains the validated description in its existing REQUEST record;
only the unchanged native receiver can establish accepted mathematics.

Project support is owner-approved executable code, not hostile-code isolation.
The new route never follows a peer recommendation into project execution and
does not add Lake, downloads, toolchain switching, dependency builds, retries,
owner-state copying or receiver-context inference. Existing source is still a
body for a newly generated authoring module, not arbitrary existing-file import.
Root's successor profile must pin the matching contribution/worker source before
this CLI is packaged; placing this file beside an old profile is not supported.

## Source-only review and remaining boundary

Read-only comparison checked the predecessor hash, new argument pairing,
bounded parsing, pin-before-parse order, backend verification before owner open,
empty-default keyword forwarding and unchanged exception/closure/accounting
structure. `project_hook_design` agreed to `from_document(document)`,
`verify(check_budget)`, and optional `contribute_source(authoring_backend=...)`.
This is source inspection, not executed qualification or independent audit.

No actual compatible owner project has been selected. Import/tactic support,
module construction and real-project interoperability therefore remain untested;
an illustrative elementary fixture would not establish those claims. No new
broad audit or test campaign is requested by this checkpoint.
