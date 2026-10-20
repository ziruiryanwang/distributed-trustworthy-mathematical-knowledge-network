# Paired discovery profile: client source implementation

Source-only under CONJUNCTION-SELECTION; canonical root guard passed. No product
imports, tests, native/proof/network execution, installs or Git. Used predecessor
sources and the installed distribution remain unchanged.

## Exact successor scope

The installed 108-source map identifies the evidence predecessor as
`software/v5/interface_views/workspace_evidence.py` (`741e225e`), not the older
logical-path source. Its complete interface-only authoring and resilient body/
declaration behavior is retained. Atomic and direct-contact predecessors match
the installed map (`01eefed1` / `97b4ead3`).

Fresh sources under `software/v5/conjunction_index/client`:

| File | SHA-256 | Change |
|---|---|---|
| `workspace_evidence.py` | `233562c663c3633e126b6761d10542e48be9145edba8b3fb731a8eafbf9c2baa` | Explicit new config profile and adapter binding; selected schema in status |
| `workspace_atomic.py` | `eea95a6bb12349e5fc7b1e80bc610710ccafc7cbbfd2b40d705d80cdc67c8022` | Existing find calls adapter compiler |
| `direct_contacts.py` | `88ce2581a7432421e2619c57ad0645f29f66d400f94c5d12db8c74c5f3d78e51` | Existing direct binding calls same adapter compiler |

The new exact schema is `DMKN_V5_CLIENT_EVIDENCE_CONJUNCTION_WORKSPACE_V1`.
It requires exactly the prior evidence fields plus `discovery_profile`. The
shared `validate_pair_profile` rejects malformed/noncanonical profiles before
workspace directory, lock, ledger or index creation. The exact config bytes are
retained by the existing immutable config and SQLite reopen checks. There is no
in-place migration, ignored field or fallback to a default profile.

The legacy evidence schema keeps its exact fields, default adapter and namespace.
The adapter constructor keyword is `discovery_profile`; `None` is only the
legacy schema's choice. New schema cannot omit the field or use `None`.
Evidence descendants (resilient/staged/validated) inherit open unchanged and
retain their exact owner/client types. No new issuer, server or transport exists.

Both real query paths invoke `workspace.adapter.compile_query(specs)`, preserving
their existing budgets, immutable source/origin checks, query ownership and
downstream authentication. Location route plans must use the same adapter's
compiled IDs; the documentation gives that ordinary API. Only the first
canonical eligible pair is selected by the discovery owner; no client-local
second pairing algorithm or automatic namespace fallback was introduced.

`CONJUNCTION-INDEX.md` documents explicit configuration, provider/consumer
matching, restart, query routes, metadata-only assurance, finite limits and
maintenance tradeoffs. The actual new scan bound uses the selected pair and
remaining atoms, not the full query intersection. Root owns finite selection,
execution and adoption; independent reviewer owns changed-boundary controls.

## Independent discovery-side source cross-read

Read the complete discovery adapter (`d1e8a437`) and changed schema allowlists
(`3ae3fd9a`, `6c5ba1e5`, `c62f357d`). No blocking finding: canonical profile
ordering makes first-pair choice deterministic; the pair exists iff its atoms
occur; all atomics remain; query contraction preserves their conjunction.
Immutable profile bytes/tuples and namespace/schema are checked for replacement.
`None` produces the same legacy namespace descriptor and empty extra-pair loop.
Overflow uses existing feature/record/work refusal, never partial indexing.
Root's source-only eight-file selector preserves the frozen basis and uses
fresh no-overwrite output; actual control behavior remains a separate review.
