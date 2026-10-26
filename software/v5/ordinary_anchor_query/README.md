# Ask a question using received vocabulary

This source-side companion accepts an approved local Lean type expression and
one existing registered module anchor. It produces ordinary exact-type search
hints without requiring a proof or theorem identifier. It does not export a new
module, accept mathematics, search peers, or create a missing anchor sidecar.
This implementation is source-only until its separate review/qualification is
adopted. The completed received-query composition test is not qualification of
this new companion.

Keep `query.py` outside the hash-bound package. Use the approved Windows x86-64
Python/Lean installation and current ordinary package, including its existing
anchor-store, type-query helper and public launcher. Do not change a package
manifest or copy this file into an old archive extraction. The compatible
launcher has SHA-256
`47a2b63c73f1bd8346c5881c6d6a76abac86d33aa8e55bfc19bf3359ea924a39`.
Package, runtime and source approval remain separate from matching hashes.

## 1. Select an existing anchor and write the question

Use a registered anchor belonging to this owner and compatible with this exact
package support. A successful existing `owner export-module` response supplies
`anchor_id` and `source_context_root`; use that context root, not the AnchorID,
as the initial `context_root`. A separately selected later context is allowed
only when every realized export still agrees exactly. Do not guess the latest
context or read private sidecar files to construct a binding map. For setup and
module-export commands, see [WORKFLOW](../ordinary_exact_module/WORKFLOW.md).

Save a UTF-8 question file containing exactly `universes` and `type`. For an
anchor realizing the indicated AllClosure vocabulary, one possible question is:

```json
{"universes":["u"],"type":"forall {T : Type u} (o : RepairTheory.ClosureBridge.OrderData T) (r : RepairTheory.Repair T) (rs : List (RepairTheory.Repair T)), RepairTheory.ClosureBridge.AllClosure o (List.cons r rs) -> RepairTheory.ClosureBridge.AllClosure o rs"}
```

The question is not asserted true. Choose your own type using the selected
vocabulary. There may be at most 32 distinct universe names matching
`[A-Za-z][A-Za-z0-9_]{0,63}`. The type is nonempty UTF-8, at most 64 KiB, without
NUL. Duplicate JSON keys and extra fields are refused.

## 2. Prepare the exact local configuration

Replace every placeholder with your actual approved absolute paths and lowercase
64-character SHA-256 hashes/IDs. Keep the question, config, companion and custody
limits outside the catalog/custody trees. Reuse the owner's original custody
limits; this command cannot renew or increase them.

```json
{
  "schema":"DMKN_ORDINARY_ANCHOR_QUERY_V1",
  "package":"C:\\commons-builds\\exact\\package",
  "profile_sha256":"REPLACE_WITH_APPROVED_PROFILE_SHA256",
  "python_runtime":"C:\\tools\\Python314",
  "lean_runtime":"C:\\tools\\Lean434",
  "query":{
    "path":"C:\\commons-requests\\question.json",
    "sha256":"REPLACE_WITH_QUESTION_FILE_SHA256"
  },
  "owner":{
    "catalog":"C:\\commons-owner\\catalog",
    "custody":"C:\\commons-owner\\custody",
    "store_id":"REPLACE_WITH_ACTUAL_STORE_ID",
    "context_root":"REPLACE_WITH_SELECTED_CONTEXT_ROOT",
    "anchor_id":"REPLACE_WITH_REGISTERED_ANCHOR_ID",
    "custody_limits":{
      "path":"C:\\commons-requests\\custody-limits.json",
      "sha256":"REPLACE_WITH_CUSTODY_LIMITS_FILE_SHA256"
    }
  },
  "limits":{
    "wall_seconds":120,
    "cpu_seconds":60,
    "memory_mib":1536,
    "active_processes":2,
    "stdout_bytes":1048576,
    "stderr_bytes":1048576
  }
}
```

Use `Get-FileHash -Algorithm SHA256` to select exact file bytes, including the
finished config. No historical experiment path or historical PROFILE is needed.
All paths must be ordinary absolute drive paths without redirects/hard links.
Package, runtime, catalog and derived import/search directories must not contain
`;`, the Windows search-path separator; these paths are refused, not escaped.
The output must be fresh with an existing parent and separate from all inputs,
the companion directory, support and owner state. The parent validates these
separations before creating any output.

## 3. Run the explicitly approved question

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B 'C:\commons-query\query.py' `
  --config 'C:\commons-requests\anchor-query.json' `
  --config-sha256 'REPLACE_WITH_APPROVED_CONFIG_SHA256' `
  --output 'C:\commons-work\anchor-query-01' `
  --approve-local-query
```

The approval is consequential: Lean syntax, macros, tactics and injected commands
execute with account permissions. Fixed imports, hash checks and Windows Jobs
are not a hostile-source sandbox. Never automatically approve downloaded text.
There is no arbitrary-project/import-path option. The wrapper imports Init, the
validated top module and the selected OwnerQueryCommand; it uses the complete
validated chain, fixed helpers/runtime and supported Windows long-path spelling.

Run with exclusive owner access. Opening the owner can reconcile abandoned
reservations, so this is not state-read-only. Its existing lock remains held
through anchor loading, Lean extraction, reference binding and final revalidation.
A missing, partial, blocked, changed or wrong-support anchor refuses; there is no
cold fallback, repair, warm-export call, fetch or registration. Both owner and
custody handles close before any successful worker candidate publication.

The original allocation covers worker plus Lean descendants: 35–600 wall seconds,
4–600 inclusive child CPU seconds, 1–4096 MiB private commit, 2–4 active processes,
and 1–1048576 bytes per stdout/stderr stream. Five wall seconds are reserved for
parent finalization; no timer or CPU allowance is renewed. Wrapper CPU is reported
separately. Resource/log sampling can overshoot; overruns fail. Protected immutable
support, OS/runtime integrity and cooperative storage remain assumptions.

## 4. Read the terminal result and use the hints

Use hints only after the parent exits zero and its fresh `RESULT.json` has
`ok:true`, `status:"ANCHOR_QUERY_READY"` and `owner_handles_closed:true`.
`WORKER.json`, an early native AST, or successful Lean exit alone is insufficient.
Failures/partial files remain preserved: inspect their phase and closure report;
do not delete locks, repair state or retry automatically.

The result binds config/question/companion/custody-limit hashes, package and
installation, store/context, anchor/support/plan, namespace/features and costs.
`files` pins the generated source, native type AST, `BINDINGS.json`, `QUERY.json`,
`SPECS.json` and `ANCHOR.json`. The last records selected modules/artifacts,
import paths and registered-record digests. `query_sha256` denotes the input
question file; the canonical output query's digest is `files["QUERY.json"]["sha256"]`.
The native directory contains only `Query.lean` and `type.json`, no compiled output.

Every AST reference must be in the pinned fixed basis or complete validated
anchor chain, with the exact SymbolID/ExportID in the authenticated context.
A name elsewhere in that context is insufficient. The worker re-reads the
context and requires the entire anchor view unchanged before closing handles.
These are selected realized-vocabulary hints, not arbitrary project equivalence.

For search, put the `SPECS.json` array into the existing find config's `specs`
field, retaining its separately selected contacts/providers and finite budgets;
see [the existing query/search mapping](../../../research/cycles/v5-2026-10-26-local-discovery/RECEIVED-QUERY-COMPOSITION.md).
For developing a proof, use the selected context as existing `owner contribute`
`--parent-root` and explicitly choose warranted acquired targets; see
[the no-project reuse recipe](../ordinary_reuse_workflow/README.md).
Neither follow-up is performed by this command. Hints prove neither theorem
truth, novelty, recall, growth benefit, nor final-v5 readiness.
