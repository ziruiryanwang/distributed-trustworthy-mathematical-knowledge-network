# Independent public query integration source review

2026-10-23, `public_query_review`. Source/data inspection only; no product
imports, compilation, test execution, database open, state mutation or Git
operation. Canonical workspace guard passed. The saved assembly outcome is
reviewed separately; this document does not duplicate or substitute for it.

## Disposition

**No remaining blocking source defect found in the corrected harness and exact
selection below.** Clear the finite seven-call check after root adopts the
separate assembly audit. This is launch-source clearance, not an observed pass.

| Input | SHA-256 |
| --- | --- |
| `software/v5/ordinary_query_package/public_check.py` | `585c7943c48fd62f085387ccf74144ce7ef41b90603f0f9b6311b0c196012488` |
| `ORDINARY-QUERY-PUBLIC-CHECK-PLAN.md` | `87b69de42c520c5e54a4d93bbf4971a0128641eeff4d970d142703fef43e554e` |
| `experiments/v5-local-checks/ordinary-query-public-01.selection.json` | `c2264507bec1660e80264f4b1edc0c56e9d49f7bd8ccd546eb8d8128f1e7ff0a` |

## Defect caught and corrected before execution

The initial unused harness `afd81998...` indexed `found["provider_errors"]`.
The actual `ordinary_peer_package/peer_api.py` `_begin`/`find` never produce
that field. It would raise `KeyError` after a successful public search.

Root corrected only that assertion to use the existing report contract:

- `termination == SELECTED_CONTACTS_FINISHED_NO_COMPLETENESS_CLAIM`;
- `search.http.failed_requests == 0`;
- `search.session.last_refusal is None`;
- `search.session.pending_requests == 0`.

I checked these fields against `transport/clients.py` and
`discovery/search_session.py`: `SearchClient.report` nests its HTTP counters
and session report exactly this way. The normal selected-contact path sets
that termination string. Budget refusal changes termination/last_refusal;
other transport/validation exceptions fail the public command. No absent-field
default or weaker global-completeness claim was introduced. The corrected source
hash was reread and the changed assertion inspected. No failed workload exists
for this unused-source correction.

## Dataflow and authority

The fresh query source names only its requested Nat type, not a target theorem,
proof or returned identifier. Its AST is emitted by the selected installed
command, then used by the public query CLI with previously known vocabulary
bindings. The harness checks AST/QUERY identity, semantic namespace, actual
SPECS, profile and byte hashes. It does not reconstruct a successful search key
from the candidate. This is an independently supplied test statement, not an
independent real-user problem or evidence of useful mathematical discovery.

Public publication uses the already accepted C context and one exact target.
The package's complete installation bytes and implementation must match the
retained owner's adoption before opening it. This permits in-place ordinary
owner reuse, not copying or promoting a foreign snapshot. The fresh index uses
the changed adapter namespace; the old index is not migrated or relabeled.

Find receives no owner arguments. Its actual SPECS and the service's actual
READY port drive the existing socket path. The returned record must equal the
published record and snapshot; its locator/object ID is then used to construct
the export-target file consumed by the public export command. A matching index
key never establishes mathematical validity. The result retains explicit
incomplete-search and non-acceptance labels.

The export check matches the actual controller's cache-key schema, source/helper
census, full two-unit request, fixed inventory, V2 match/add partition, complete
inventories and five artifact parts. The worker's build/private-reread/exported-
reread phase trace and clean native closure are required. Artifact ordering
agrees with the retained helper's `PARTS`, including server/private and IR suffix
order. The ordinary consumer imports only Init and the freshly generated module
and explicitly applies the discovered new theorem. It cannot use the query
helper import path, a copied old module, `rfl` or direct `Nat.add_zero` fallback.

## Concurrency, preservation and cost

All seven child calls have fixed identities and at-most-once dispatch. Serving
and find reserve both CPU grants before dispatch. Remaining original CPU/wall
budgets narrow each grant; delayed find re-narrows wall at actual launch. Only
the finite service supervisor runs in a second thread. Inspection of the pinned
supervisor and Job shows per-call handles/records and no signal-handler or global
environment mutation. Both commands remain under the selected outer Job.

Each child's final inclusive CPU replaces its reservation once. Nested export
worker CPU is checked but not added again. The supervising thread's CPU belongs
to the harness process; overlapping wrapper counters are not summed. Unknown
accounting charges the full grant and blocks success. The service must finish
its original lease, close cleanly and become quiescent before export reopens the
owner. Failure cleanup does not renew the lease or launch another command.

Preflight and successful final verification rehash the old immutable-file map,
selected package/runtime bytes and actual outputs. Mutable SQLite/lock files are
not falsely promised byte-identical: publication and supported reopen bookkeeping
are explicitly allowed. Failure preserves partial outputs and requires a later
saved-file audit instead of claiming final preservation. The outer report remains
authoritative for full-tree closure and whole-operation CPU. These process limits
are not a hostile-input security sandbox.

## Exact selection consistency

Selection `c2264507...` binds three current source hashes and exactly 163 runtime
pins: the same 29 external runtime pins as the saved native selection, plus all
133 assembled payloads and PROFILE. Data comparison found zero source, external-
runtime or payload-map mismatches. Its profile is
`2b8ac8cad152dde90a1b51d19dd1a821305bd7242b601c10eaa7a39f0db572f5`.
This map comparison is not the separate complete assembly outcome audit.

The outer envelope is 210 wall seconds, 130 CPU seconds, 2048 MiB and eight
processes; the inner envelope is 180/110/1536 with a fixed cleanup reserve.
Isolated argv passes the actual assembled package and `{output}/public`, matching
the harness's fresh child-directory requirement without colliding with the
runner-created parent. No new native command build, init, contribution, missing-
library extraction, acceptance or certificate campaign is selected.

A pass would close this same-host public compatibility boundary only. It would
not establish fresh-receiver admission, scalable semantic recall, independent
hosting, useful-growth advantage, broad library compatibility or final v5.
