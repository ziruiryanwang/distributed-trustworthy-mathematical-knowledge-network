# Ask a formal question without first proving it

These two source-side companions turn an explicitly approved Lean type into
existing exact-type search hints. Neither performs search, produces a proof,
accepts mathematics nor assigns a research goal. Keep both programs outside the
hash-bound package; they are already included in the verified source distribution.
Use the final package from [BUILD-MODULE](BUILD-MODULE.md), its actual approved
PROFILE identity, Windows x86-64 Python 3.14.6 and Lean 4.34.0.

Choose the smallest appropriate route:

| Vocabulary in the question | Companion | Additional prerequisite |
|---|---|---|
| Only the pinned 581-declaration fixed basis | `ordinary_basis_query/query.py` | No owner, project or catalog |
| The fixed basis plus concepts in a realized local module chain | `ordinary_anchor_query/query.py` | Existing compatible registered anchor and its exact owner/context |

Both require the known contact-federation launcher SHA-256
`47a2b63c73f1bd8346c5881c6d6a76abac86d33aa8e55bfc19bf3359ea924a39`;
the final exact-module package retains it. Matching bytes is not approval.

## Write a local question

Save UTF-8 JSON with exactly `universes` and `type`, for example:

```json
{"universes":[],"type":"forall (p q : Prop), And p q -> And q p"}
```

There are at most 32 distinct ordered universe identifiers matching
`[A-Za-z][A-Za-z0-9_]{0,63}`. The nonempty type is at most 64 KiB UTF-8 without
NUL. Duplicate keys and extra fields are refused. The question is not asserted
inhabited. It may use the exact Lean names actually available in the chosen
vocabulary; do not rename a foreign concept to a same-spelled local one.

**The text is executable Lean syntax.** Macros, tactics, elaborators and injected
commands run at account permissions. Fixed imports, checking and Windows Jobs
are not a hostile-source sandbox. Approve the actual local text and environment;
never automatically approve downloaded text. Neither command accepts arbitrary
project/import paths. Hashes select file bytes, not semantic intent or safety.

## Fixed-basis configuration and invocation

Save the following config with actual approved paths and 64-character lowercase
SHA-256 values. `Get-FileHash -Algorithm SHA256` can identify exact selected files.

```json
{
  "schema":"DMKN_ORDINARY_BASIS_QUERY_V1",
  "package":"C:\\commons-builds\\exact-01\\package",
  "profile_sha256":"REPLACE_WITH_ACTUAL_APPROVED_PROFILE_SHA256",
  "python_runtime":"C:\\tools\\Python314",
  "lean_runtime":"C:\\tools\\Lean434",
  "query":{
    "path":"C:\\commons-requests\\question.json",
    "sha256":"REPLACE_WITH_QUESTION_FILE_SHA256"
  },
  "limits":{
    "wall_seconds":120,"cpu_seconds":60,"memory_mib":1024,
    "active_processes":2,"stdout_bytes":1048576,"stderr_bytes":1048576
  }
}
```

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_basis_query\query.py' `
  --config 'C:\commons-requests\basis-query.json' `
  --config-sha256 'REPLACE_WITH_APPROVED_CONFIG_SHA256' `
  --output 'C:\commons-work\basis-query-01' --approve-local-query
```

Use only an exit-zero terminal `RESULT.json` with `ok:true` and status
`BASIS_QUERY_READY`, with matching pinned output files. `WORKER.json`, an early
AST, candidate files and `RESULT.pending.json` do not suffice. The basis contains
fewer names than all of `Init`: native elaboration can succeed but binding refuse
`BASIS_QUERY_UNKNOWN_VOCABULARY`. No IDs are guessed for unknown references.

## Received-vocabulary configuration and invocation

First use [module export](BUILD-MODULE.md) once for actual needed concepts, or
select an already compatible local anchor. The successful report supplies
`anchor_id` and `source_context_root`. Use that root as initial `context_root`;
a separately selected later context is allowed only if **every** realized export
still agrees. Do not choose a guessed latest root, pass AnchorID as context, or
read private sidecars to create a binding map.

The config has this complete shape:

```json
{
  "schema":"DMKN_ORDINARY_ANCHOR_QUERY_V1",
  "package":"C:\\commons-builds\\exact-01\\package",
  "profile_sha256":"REPLACE_WITH_ACTUAL_APPROVED_PROFILE_SHA256",
  "python_runtime":"C:\\tools\\Python314",
  "lean_runtime":"C:\\tools\\Lean434",
  "query":{
    "path":"C:\\commons-requests\\question.json",
    "sha256":"REPLACE_WITH_QUESTION_FILE_SHA256"
  },
  "owner":{
    "catalog":"C:\\commons-state\\catalog",
    "custody":"C:\\commons-state\\custody",
    "store_id":"REPLACE_WITH_ACTUAL_STORE_ID",
    "context_root":"REPLACE_WITH_SELECTED_CONTEXT_ROOT",
    "anchor_id":"REPLACE_WITH_REGISTERED_ANCHOR_ID",
    "custody_limits":{
      "path":"C:\\commons-requests\\custody-limits.json",
      "sha256":"REPLACE_WITH_ORIGINAL_CUSTODY_LIMITS_SHA256"
    }
  },
  "limits":{
    "wall_seconds":120,"cpu_seconds":60,"memory_mib":1536,
    "active_processes":2,"stdout_bytes":1048576,"stderr_bytes":1048576
  }
}
```

Keep question/config/companion/limits outside catalog/custody. Reuse the original
persistent limits; this command cannot renew them. Package/runtime/catalog and
derived import paths must not contain `;`, the Windows search-path separator.
The command refuses these paths rather than escaping or accepting them.

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_anchor_query\query.py' `
  --config 'C:\commons-requests\anchor-query.json' `
  --config-sha256 'REPLACE_WITH_APPROVED_CONFIG_SHA256' `
  --output 'C:\commons-work\anchor-query-01' --approve-local-query
```

Run with exclusive owner access. Opening the owner can reconcile abandoned
reservations, so this is not state-read-only. The owner lock stays held through
anchor loading, Lean extraction, binding and final revalidation. Missing/partial/
blocked/changed/wrong-support anchors refuse. No cold fallback, export, fetch,
registration or repair occurs; an existing protected sidecar is required.

Require exit zero, `RESULT.json` with `ok:true`, `status:ANCHOR_QUERY_READY` and
`owner_handles_closed:true`, and matching pinned files. The result binds exact
owner/context/anchor/support/plan and package/installation plus input/output
hashes. `query_sha256` is the input question's hash; the canonical output query's
hash is `files["QUERY.json"]["sha256"]`. The entire validated realized view is
rechecked before owner/custody closure. A name merely present somewhere else in
the context is not enough: every AST reference must be in the fixed basis or
the complete selected module chain with exact bindings.

## Shared limits, outputs and next action

All paths must be ordinary absolute local-drive paths without redirects or shared
hard-linked files. Outputs must be fresh with existing parents and separate from
all inputs, companion directory, support and state. Preserve partial failures and
inspect phase/closure; do not delete locks, alter pins or retry automatically.

Accepted limits are 35–600 wall seconds, 4–600 inclusive child CPU seconds,
1–4096 MiB private commit, 2–4 active processes and 1–1048576 bytes per log.
Five seconds of the original wall grant are reserved for parent finalization.
The parent separately checks cooperative CPU against `min(30,cpu_seconds)`;
there is no hard combined parent-plus-child memory/CPU quota. Worker and Lean
descendants share the original worker allowance. Sampling can overshoot and
cleanup can exceed deadlines; overruns/uncertain closure cannot succeed. No timer
or CPU allowance is renewed. Example values above are not success guarantees.

Both results pin generated source, native type AST, `BINDINGS.json`, `QUERY.json`
and `SPECS.json`, with supervision and candidate reports retained. Basis extraction
also emits `Query.olean` and optional associated native outputs; those are compiler
outputs, not mathematical warrants. Anchor extraction emits only `Query.lean`
and `type.json` in its native directory, plus an `ANCHOR.json` binding the selected
module/artifact/import records. Output validation caps are not hard disk quotas.

Put the successful `SPECS.json` array into the existing find request's `specs`
field. Independently select authorized contacts, provider/egress policy and finite
budgets through the current investigator selector, as explained in
[CONTINUE](CONTINUE.md). The companions do not invent or contact providers.
The query describes an exact structural type key under a fixed namespace/profile,
not general unification or decidable mathematical equivalence. No hit proves
applicability; no hit found proves absence. Query success supplies neither a proof,
novelty, recall, a useful-growth advantage nor completed worldwide v5.

