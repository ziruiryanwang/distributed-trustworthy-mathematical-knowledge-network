# Focused portable-catalog storage controls

2026-10-23. Author: `portable_integration_audit`. Root selected only the new
`software/v5/ordinary_lean/portable_catalog_checks.py` and this checkpoint.
The canonical workspace guard passed. **Source-only; no execution or pass is
claimed.** No Python process, syntax compilation, Lean worker, catalog operation,
test, migration, Git or network operation was run by this author.

## Decision and scope

The useful workflow is to retain an eligible owner's already checked ordinary
library while replacing local mathematical identifiers with portable identities.
The new storage seam must not expose an incomplete import, lose original native
module names, or authorize a child against a changed parent plan. These controls
discriminate that new seam without replaying the library or repeating the old
catalog, identity-translation or discovery suites.

The script uses the actual `PortableCatalog`, Windows owner lock, ordinary-file
checks and SQLite DELETE/FULL tables. It creates only fresh, explicitly named
synthetic catalogs beneath a caller-provided operation root. No existing V1
catalog is opened and no legacy importer/translator is called. Everything it
creates, including refused and interrupted states, is retained; there is no
cleanup, overwrite, retry or recursive deletion.

The fixture contains two invented source records: a 581-name basis and a
one-name extension. Names, support commitments, input hashes, audit and
correspondence documents are synthetic. Every `.olean` contains conspicuous
inert text rather than serialized Lean data. The fixed cardinality is needed
to reach this storage API; it does not qualify the real fixed inventory.

The private `_activate_import` and `_commit_checked` calls deliberately isolate
their storage behavior. Their real eligible-source/correspondence and clean
native-worker preconditions are **not** established by the fixture. A PASS would
therefore mean only the selected storage controls passed, never that these
invented records are mathematics, that migration is qualified, or that the
public controller may accept peer snapshots.

## Five finite groups

| Group | Actual boundary exercised |
|---|---|
| Importing unavailable | Context, basis reservation and extension reservation refuse before activation. Closing the importer leaves ordinary reopen refusing IMPORTING. Read-only inspection finds no accepted roots, operations or import rows. |
| Complete activation and child plan | Complete two-record activation invokes the trusted test callback twice. Context/reopen preserve original V1 module names, parent relationships, portable bindings and retained support. A new native reservation binds that original parent plan. A cloned grant and changed plan/module/input-ID slots refuse. A clearly labeled synthetic storage-only commit preserves the original parent in the child and survives reopen. |
| Required completeness and support | A cloned import grant, incomplete supplied record list, changed record hash, omitted retained support, omitted original checking support and a missing selected snapshot refuse before the source callback. Refused destinations remain unactivated with empty accepted tables. |
| Interrupted activation | The second source callback raises inside the activation transaction. The catalog closes and invalidates authority, ordinary reopen refuses, and read-only inspection confirms IMPORTING with no partial rows. This is controlled callback-failure rollback, not a power-loss or arbitrary SQLite I/O-fault campaign. |
| Current support and withdrawal | Reopening with changed current controller support refuses adoption. The active synthetic V2 store's WITHDRAWN marker denies context, reservation and fresh reopen. No automatic archival-V1 withdrawal propagation is claimed. |

The successful activation result is retained and only withdrawn at the end of
the last group. Each other group has its own fresh directory. Failed bindings
are attempted only before transaction/activation on their disposable synthetic
destination; they do not rewrite a prior result. The late-interruption group
does not resume or repair the failed import.

## Proposed invocation; root selects runtime separately

```text
<selected Python> -B <canonical-root>/software/v5/ordinary_lean/portable_catalog_checks.py
  --store-root <fresh absolute child of the selected existing operation directory>
```

Requires the selected Windows x86-64/64-bit Python environment, matching the
existing synthetic implementation fixture. Parent directories must exist and
be ordinary nonaliased directories; the final store root must not exist. The
script writes only below that root, disables bytecode writes, uses only stdlib
plus the six selected local helpers below, and launches no child processes.
It prints five individual PASS records and one final aggregate record only if
all assertions complete. All carry `storage_only=true` or explicit
`mathematical_acceptance=false` / `migration_qualified=false` labels.

Root owns exact interpreter/source selection, the bounded outer supervisor,
execution output retention, independent review and any outcome adoption. A small
native-free allocation is appropriate; no native compilation or certificate
production belongs to this test. No test has been run or silently retried here.

## Source pins

All paths below are relative to the canonical project root
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

| File | SHA-256 |
|---|---|
| `software/v5/ordinary_lean/portable_catalog_checks.py` | `98af957a970b75fcac0122020f6b469e56cf9d3ee099806c35343e1b317b4dac` |
| `software/v5/ordinary_lean/portable_catalog.py` | `2d0e91b2920abb69304b920a676da202a5e2444ddec37805d19e953b69eebf35` |
| `software/v5/ordinary_lean/local_catalog.py` | `860a9d731290b2a7fbacd4852bb68185516329ee42845648f4ba3c3856d7c751` |
| `software/v5/ordinary_lean/ordinary_evidence.py` | `fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6` |
| `software/v5/ordinary_lean/ordinary_semantics.py` | `ee601536f53640a2695e51d37d3e87e6746604ed6433cb3ace9349ae1aedf915` |
| `software/v5/ordinary_lean/portable_evidence.py` | `f8ea819bdd9344d696cef2725888828125b2ef5d1b60d2c31a0412657a62cbd8` |
| `software/v5/ordinary_lean/semantic_identity_checks.py` (fixture functions only, not its suite) | `9614df54f8bc66ab4d5086aa94eef46cd738466d38bdecdfff474e6d2ba972b4` |

The catalog's independent source review is `PORTABLE-CATALOG-REVIEW.md`, SHA-256
`7b98a06b451e275b0a938cf027d319429210252322c7dbdeead4622cd5f5f6dd`.
The implementation itself is unchanged by this control task. The new controls
remain subject to separate review and root selection before execution.
