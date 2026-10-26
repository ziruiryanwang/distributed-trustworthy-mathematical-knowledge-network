# Ask a formal question before writing a proof

This source-side companion turns an explicitly approved local Lean type expression
into the existing ordinary commons' exact-type search input. You do not need a
theorem name, proof, owner initialization, catalog, custody or existing project.
It executes one bounded Lean extraction, binds only the selected fixed-basis
vocabulary, and writes `QUERY.json` and `SPECS.json`. It does not search peers or
accept mathematical evidence.

The supported profile is Windows x86-64, Python 3.14.6 and Lean 4.34.0, with the
approved final ordinary package built using the workflow source distribution.
Keep `query.py` outside that hash-bound package. This new companion is separate
from the frozen workflow archive: do not insert it into an existing extraction
or change its manifest. Runtime binaries are not bundled or downloaded here.
All current work is local and unpublished; the license remains undecided.
Source review and actual qualification are recorded separately from this guide.

## 1. Write the question and select the package

Save a UTF-8 JSON file containing exactly `universes` and `type`. For example:

```json
{"universes":[],"type":"forall (p q : Prop), And p q -> And q p"}
```

This asks for a formal type; it does not assert that the type is inhabited.
Universe parameters are an ordered list of at most 32 distinct simple identifiers
matching `[A-Za-z][A-Za-z0-9_]{0,63}`. The type must be nonempty and at most 64 KiB
of UTF-8, without NUL. Duplicate JSON keys and additional fields are refused.

Create a separate UTF-8 config with exactly these fields. Replace paths and
64-character lowercase SHA-256 placeholders with your actual approved inputs:

```json
{
  "schema":"DMKN_ORDINARY_BASIS_QUERY_V1",
  "package":"C:\\commons-builds\\transport\\package",
  "profile_sha256":"REPLACE_WITH_ACTUAL_APPROVED_PROFILE_SHA256",
  "python_runtime":"C:\\tools\\Python314",
  "lean_runtime":"C:\\tools\\Lean434",
  "query":{
    "path":"C:\\commons-requests\\question.json",
    "sha256":"REPLACE_WITH_QUESTION_FILE_SHA256"
  },
  "limits":{
    "wall_seconds":120,
    "cpu_seconds":60,
    "memory_mib":1024,
    "active_processes":2,
    "stdout_bytes":1048576,
    "stderr_bytes":1048576
  }
}
```

Use the final package's actual generated `PROFILE.json` identity, not a historical
profile from another build. Obtain byte digests with `Get-FileHash -Algorithm
SHA256`; a matching hash establishes byte selection, not code approval or trust.
Independently approve this script, package, runtimes and local question first.
The supported installed `run.py` is the existing contact-federation launcher,
SHA-256 `47a2b63c73f1bd8346c5881c6d6a76abac86d33aa8e55bfc19bf3359ea924a39`.
Other launcher versions are refused before import.

## 2. Execute one explicitly approved local query

All paths must be absolute, ordinary drive paths without redirects or hard-linked
input files. The output directory must not exist, its parent must exist, and it
must not overlap the companion's directory, package, runtimes or selected inputs.

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B 'C:\commons-query\query.py' `
  --config 'C:\commons-requests\query-config.json' `
  --config-sha256 'REPLACE_WITH_APPROVED_CONFIG_FILE_SHA256' `
  --output 'C:\commons-work\query-01' `
  --approve-local-query
```

**The question text is executable local Lean syntax.** Elaborator macros, tactics
and injected commands can run with your account's permissions. Fixed imports,
hash checks, type checking and resource Jobs are not a hostile-source sandbox.
Never approve downloaded text automatically. No foreign project/import/search-path
option is supplied. Run only in your protected, unchanged local environment.

The child tree contains the fixed Python worker, Lean and any descendants. Limits
are wall time (35–600 seconds), inclusive child CPU (4–600 seconds), private commit
(1–4096 MiB), active processes (2–4), and each log (1–1,048,576 bytes). Five seconds
of the original wall allocation are reserved for parent finalization. The parent
checks its own CPU cooperatively against `min(30, cpu_seconds)` and reports it
separately; this is not one hard parent-plus-child memory/CPU quota. The unchanged
supervisor checks wall, total CPU and log caps by sampling and after cleanup;
overshoots or uncertain cleanup cannot succeed. Cleanup can outlast the deadline.
Native output inherits the supervised worker logs. There is no retry or renewal.

## 3. Require the terminal result, then use its search specs

Require exit code zero and `RESULT.json` with `ok: true` and status
`BASIS_QUERY_READY`. Its hashes must match the retained output files. Do not use
an AST, `WORKER.json`, candidate files or `RESULT.pending.json` alone. The parent
publishes `RESULT.json` only after clean worker closure, final input/support and
output checks, and a complete pending-report write/readback. A failed or interrupted
operation preserves partial output and supplies no usable-result claim. Never
overwrite it or edit its expected hashes into agreement.

The output directory includes:

| File | Meaning |
|---|---|
| `native/Query.lean` | Generated fixed-import source containing your question |
| `native/type.json` | Existing inert, validated native expression AST |
| `native/Query.olean` and optional associated native artifacts | Local compiler output, not a mathematical warrant |
| `BINDINGS.json` | Exact referenced fixed-basis name-to-symbol associations |
| `QUERY.json`, `SPECS.json` | Existing query format and one exact-type feature spec |
| `LAUNCH.json`, `child/`, `SUPERVISION.json`, `WORKER.json` | Actual operation and candidate evidence |
| `RESULT.json` | Parent terminal result, interpretation, namespace, compiled features and file hashes |

Use the JSON array in the successful result's `specs_file` as the `specs` field
of the existing separately prepared `peer find` configuration. Select contacts,
egress policy and finite search budgets independently using the existing network
guide and final `ordinary_bounded_transport/prepare_selected.py` selector. The
result's `namespace` and `features` are computed by the installed discovery
adapter, not a new index format. This companion never contacts providers.
Previewing, receiving and independently checking a returned candidate remain
separate operations; successful hint preparation grants no mathematical acceptance.

## Interpretation and limits

Only names in the pinned **581-declaration foundation inventory** are supported.
`Init` contains more names than this inventory. Native elaboration can therefore
succeed while hint preparation refuses `BASIS_QUERY_UNKNOWN_VOCABULARY` and lists
the unknown structured names in `WORKER.json`. It derives no guessed IDs for them.
Do not replace an unknown project name with a same-named owner declaration:
different projects may assign that name different meanings.

Search uses the existing exact structural type key: binder/universe spelling is
normalized as already specified, but this is not general unification, mathematical
equivalence, theorem proving or complete semantic retrieval. No result is not
evidence that the mathematics does not exist. The result describes the fixed
semantic/foundation/key profile and explicitly says `mathematical_acceptance:false`.

Known native artifacts are capped at 16 MiB each, other candidate files at 1 MiB,
with at most 64 MiB total candidate output and at most seven native files. These
are post-execution validation caps, **not hard disk quotas**. Package/runtime
integrity, protected local storage, the OS and approved executing code remain
premises; selected runtime pins are not a hermetic attestation of every library.
This capability removes one cold-start input barrier. It does not establish
global coverage, useful growth, source isolation or completed worldwide v5.
