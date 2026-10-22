# Six Python stores: pre-open and connection guard wiring

2026-10-21, support_screen, author checkpoint. **SOURCE ONLY; NOT TESTED OR
INTEGRATED.** Root delegated these six files after the public02 actual audit,
under `MANAGED-STORAGE-INTEGRATION-SELECTION.md`. Root/guest retain independent
review; root owns helper implementation, source-map/profile binding, installation,
runtime selection and Git.

## Basis and exact delta map

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
The workspace guard passed. All six initial copies came exclusively from the
127-entry `sdk_sources` map in
`experiments/v5-local-checks/distribution-managed-observed-01-input.json`,
SHA-256 `e0f0dc5d63dee0d088b8edd9e61d9a1d1bebbe31d3dde76b53887d1c901f7201`.
Every selected source length/hash was checked before copying; each destination
was absent, under the canonical fresh successor root, and copied byte-identically.
Only subsequent absolute-path `apply_patch` additions changed the successors.

New files below are under `software/v5/managed_storage/`.

| Relative successor | Selected predecessor path under `software/v5/` | Old bytes | Old SHA-256 |
|---|---|---:|---|
| `client/workspace_evidence.py` | `terminal_i/client/workspace_evidence.py` | 51539 | `8531ee14e24d60617491b9f00e14ea1f7c410a279d116322489fe763a421ea68` |
| `custody/module_store.py` | `custody/module_store.py` | 10535 | `39e8eee8fd556c4ec66b76ac2e9abc73efdf039dc2b488ffa237040438a4da28` |
| `evidence_network/custody.py` | `terminal_i/evidence_network/custody.py` | 8166 | `c039af086cf73d57191187e9d5b02292c5c9b8a3fb455d67dc719ad8f7d183a0` |
| `discovery/discovery_store.py` | `selective_placement/discovery/discovery_store.py` | 19886 | `1c8543d4903754174b80d107ee923116ddb402d41a3b5af3f1d255abdfc6a328` |
| `placement/ledger.py` | `selective_placement/placement/ledger.py` | 12537 | `d955990c347ed466617c752893dded8b8494dd266a050b045352c77c48f21a91` |
| `placement/advertisement.py` | `retained_advertisement/placement/advertisement.py` | 23256 | `5aa23ee76115355ad319ae4acfd4ab418e010166e53b6ed02c82eb25d34d4510` |

| Relative successor | New bytes | New SHA-256 | Added lines |
|---|---:|---|---:|
| `client/workspace_evidence.py` | 51821 | `d94e38257444da3bda04e4d9b298d422280a573becc27eaa063fdbc01f9c02a2` | 4 |
| `custody/module_store.py` | 10754 | `580515e461c95b424bc59011b8bf87e4776039f7d6cb87c27599f295c602dcbb` | 3 |
| `evidence_network/custody.py` | 8385 | `4264841e55ebc21899d8967ef9ac439d0682da5ea4a0d1c2097eddc930f1300e` | 3 |
| `discovery/discovery_store.py` | 20113 | `7f3c884b3ef3455e51563d233a2ca4a19087bc8097186e6b43e949abededa2c5` | 3 |
| `placement/ledger.py` | 12758 | `59f87b9334c44a8a9f8feb236084f419081d2484582917aded55eaac15f8351d` | 3 |
| `placement/advertisement.py` | 23475 | `13b0ef1ae400990f237e5e1957a77008d7f2ac51fb96758560152cfda3ecdf28` | 3 |

There are19 added lines and no removed/reordered predecessor lines. A read-only
inverse text check removed only those import/call additions, reconstructed each
entire predecessor exactly, and recomputed its original SHA-256 from the restored
UTF-8 content. All six original source files still hash to the selected pins.
Each successor has exactly one `sqlite3.connect`, one pre-open database call and
one connection configuration call.

## Actual call sites

Every file adds:

`from placement import storage_profile as SP, storage_paths as SF`

Every pre-open gate is before its existing SQLite connection. Every
`SP.configure_connection` is the first protected connection operation inside the
existing cleanup `try`, before all predecessor PRAGMAs, reads, DDL or writes.
The ledger's existing workspace attachment between connect and `try` is retained;
it performs no SQLite operation. Failure of configuration reaches the existing
connection cleanup. No helper result is promoted into a profile/adoption flag.

| Store/database | Original cap passed unchanged to both gates | Pre-open / configure lines |
|---|---|---|
| workspace `workspace.sqlite` | `config["ledger_pages"]` | 108 / 110 |
| module `modules.sqlite` | `limits["db_pages"]` | 48 / 51 |
| packet `evidence-packets.sqlite` | `limits["db_pages"]` | 92 / 95 |
| discovery `discovery.sqlite` | `limits["max_db_pages"]` | 70 / 73 |
| placement `placement.sqlite` | `cfg["ledger_pages"]` | 37 / 41 |
| advertisement `placement-routes.sqlite` | `journal_pages` | 66 / 68 |

The workspace additionally calls `SF.preopen_lock(lock, create=create)` at102,
before its original `lock.open("a+b")`. The required helper contract is fresh
absence for create, and an ordinary existing exactly-one-byte lock for reopen,
without helper mutation. Under that contract, reopen cannot reach the old
zero-length initialization branch to repair a bad lock silently. Fresh creation
retains the original one-byte write/flush/fsync and locking code. No lock mode or
ownership policy was rewritten here.

## Preserved behavior and integration pitfalls

- Existing SQL schemas, reads, transactions, rollback/error paths, mathematical
  guards, identity bindings and resource budgets are textually unchanged.
  Original foreign-key, mmap, cache-size and duplicate journal/synchronous/temp
  PRAGMAs remain in their original order after the new shared configuration.
  No tuning or duplicate-PRAGMA cleanup was performed.
- `preopen_database` is needed before connect because SQLite may perform journal
  recovery before post-connect configuration. Metadata bounds alone do not prove
  same-profile history or exclude races from other writers. Root's managed
  marker/layout/lineage and source/runtime binding must establish those premises
  before store calls. Direct callers obtain gates, not a whole managed-root bound.
- Some original constructors create their directory before the new pre-open
  check. This assignment did not move directory creation or reservation logic.
  Root/guest's separate manager/generation admission must refuse inadequate
  reservations before filesystem or PROVISIONING writes; these store insertions
  alone do not establish that property.
- Shared configuration now runs on both fresh and reopened connections, including
  discovery reopen where the predecessor's explicit page-cap write was within
  `if create`. This enforces the selected existing cap rather than adding a new
  budget. An incompatible old database must refuse, not migrate or auto-repair.
- `SP` is the root-owned reviewed connection helper; `SF` is the root-owned path
  helper contract. The import graph requires SF's `ordinary` dependency to stay
  lazy, as selected by root, because discovery_store itself imports SF. No local
  replacement, import shim or monkey patch was added. Runtime/import behavior
  still requires the later independently selected changed-boundary gate.
- Packaging must add/select both helpers and these exact six successors, and
  update the managed owner/composer's authenticated writer/source profile. No
  caller boolean, returned calculation, or file hash alone establishes the full
  apparent-stream premise. Physical allocation, free disk, external outputs,
  hostile local writers and general migration remain outside this patch.
- Workspace configuration validation remains its original inline implementation.
  No pure validator extraction or duplicate schema logic was authorized in this
  six-file task; any lifecycle requirement for that is a separate root decision.

No imports, AST parsing, tests, SQLite opens, builds, installations, runtime,
private data access, deletions or Git operations were performed for this task.
The only created files are the six assigned source successors and this note.
This is an authored narrow wiring checkpoint, not an independent review or a
whole-profile storage guarantee.
