# Bounded release decision audit

2026-10-28. Source-only; current local kit PROFILE
`c8c8b5971e43361b7b09847b35b0e44c2645b284e59c59b90ab993136ccdb146`.
This audit selects no runtime, owner access, code change or package replacement.

## Result

No new admission-soundness defect was demonstrated. The retained source reviews
already trace inert acquisition through fresh planning, actual kernel checking,
protected snapshot restoration and clean live-event commit. The actual kernel
controls include false=true rejection and no snapshot on failed checking.
Reopening those unchanged gates is not the highest-value next step.

One concrete implementation boundary remains relevant to public-input operation:
snapshot output reservations constrain promotion and ledger accounting, but do not
constrain the bytes written before promotion. This is an explicitly disclosed
resource-isolation gap, not a newly discovered false-acceptance bug. No current
oversized-output witness or disk-exhaustion event is claimed.

## Exact distinction

Let `q` be a grant's reserved output bytes and `Q` the catalog's artifact allowance.
The current catalog enforces its reservation ledger against `Q`. A clean successful
promotion additionally requires actual artifact bytes `b <= q`. These statements
do not imply that physical transient or retained failed output stays within `Q`.

| Current source | Enforced boundary |
|---|---|
| `ordinary_parse_reuse/ordinary_admission.py`, `OperationBudget` and `_execute` | Default `q = 64 MiB`; caller may select 1 byte through 1 GiB. The fixed worker command does not transmit `q`. Report/file agreement and `b <= q` are checked after worker exit. |
| `ordinary_kernel_admission/OrdinaryWorkflowWorker.lean`, `extend` | Calls the snapshot writer with its default limits. |
| `ordinary_kernel_admission/LocalSnapshot.lean`, `writeCheckedRecords` | Calls `saveModuleData` first, then checks the file against a default 1 GiB bound. Even the native bound is post-write. |
| `ordinary_lean/portable_catalog.py`, `_reserve`, `_commit_checked`, `abandon` | Reservations and promotion are bounded. Failed grants retain their original charge and may retain the already-written artifact. |
| `ordinary_parse_reuse/ordinary_admission.py`, module contract | Per-operation call spool is outside the snapshot-byte ledger; its capacity is a separate operator responsibility. |

The existing `ADMISSION-EVENT-REVIEW.md` already names the larger native default
and post-write check. `ordinary_dedicated_host/LAUNCHER.md` explicitly excludes a
hard disk quota. Physical storage isolation/capacity remains an honest deployment
premise where the operator supplies it. No generic hostile-source sandbox is
required merely because the protocol receives inert portable records.

## Selected next decision

Root selected only a source feasibility check of bounding fresh native output.
`NATIVE-OUTPUT-DECISION.md` closes it: the serializer has an internal exact
pre-write seam but no supported Lean-level hook. More economically, the existing
hard Job memory ceiling `M` yields a conditional worst-case artifact bound; a
separate reservation of `M + 88` bytes could cover failed output while preserving
the smaller successful-output cap. This requires changed accounting, not a
serializer rewrite. No implementation, native rebuild, proof/fuzz campaign or
OS/admin quota setup is selected here.

A future accounting theorem must bind each grant to its actual output write
path, either by conservative Job-derived reservation or by a new exact native
cap. Accepted and failed artifacts could then fit the same reserved bound. This
would still not prove a whole-process disk quota: call spool, sampled logs and
other storage remain separate obligations. Rechecking the same successful
mathematical admission does not resolve that distinction.

## Reused assurance and scope

- `research/cycles/v5-2026-10-25-software-continuation/ORDINARY-RELEASE-TRUST-BOUNDARY.md`:
  finite end-to-end trust trace and protected-state/runtime premises.
- `software/v5/ordinary_kernel_admission/REVIEW.md` and `CONTROLS-OUTCOME.md`:
  actual checked-addition and exact names/references/inventory.
- `software/v5/ordinary_parse_reuse/REVIEW.md`: fresh raw-input planning and private
  parse reuse preserve admission authority.
- `research/cycles/v5-2026-10-22-native-library/OWNER-REBIND-SOURCE-REVIEW.md`,
  `OWNER-CONSUMER-SOURCE-REVIEW.md` and `ADMISSION-EVENT-REVIEW.md`: semantic
  correspondence, actual owner presence, clean event and commit ordering.
- `research/cycles/v5-2026-10-26-local-discovery/UPDATE-TRUST-DECISION.md`:
  changed implementations cannot inherit old catalog authority silently.

This is a bounded local software decision, not completion of final v5. License,
independent-host/user evidence and broad practical benefit remain separate release
questions; none is fabricated into a local implementation defect.
