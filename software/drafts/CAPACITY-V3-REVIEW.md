# Independent source review of the v3 capacity drafts

2026-09-21. This review covers the full operating envelope and the four draft
components below. It is source-only: no Python import, compilation, test,
database query, Windows capacity query or native execution was performed.
The drafts are not installed, and this is not a v3 or usable-v1 qualification.

## Reviewed scope and identities

SHA-256 values identify the reviewed development cut, not deployed code.

| Source | SHA-256 |
| --- | --- |
| `OPERATING-ENVELOPE.md` | `2245ed1608a995294c7558ad90c62fa1e17820e69b2c9c74eb5f26e04c520a53` |
| `capacity_v3.py` | `e37bff768e643317f8f0ae0972b2f6e47c40c0a2ed80aa3bfd726cfb36fbf768` |
| `storage_v3.py` | `e880e30f7dea26bf8f8971b112394b9f5858fb6916add81de38b7d4cffbd0795` |
| `admin_worker_v3.py` | `c72921d130711bf65c412a82ce925563721cf0bbd4c6ece8a3357aeef1ae50ee` |
| `admin_manage_v3.py` | `c26c7212a5301451a3704164f4047f6542f9a79220a136b135b5e317f5d4e120` |

## Capacity helper

The parser checks exact integers, excludes Boolean increments, bounds every
dimension, rejects unsupported caps and uses the strict storage JSON decoder
for duplicate fields and noninteger numbers. A cap-only proposal is permitted;
durable-state checks decide whether it increases the selected cap. Exact raw
grant bytes remain available for replay and whitespace conflicts.

Physical supply compares actual Windows volume GUIDs, requires fixed local
NTFS, and samples caller-available bytes against remaining authorized bytes
plus twice the proposed metadata cap plus one GiB. It neither subtracts used
credits from actual file sizes nor reserves disk. Status uses `enforce=False`
to retain an insufficiency observation. No future-availability guarantee follows.

## Control store

Under the external owner lock, intact typed state and atomic SQLite behavior,
the source preserves `0 <= U <= A` using checked Python sums and SQL assignments.
The fresh schema has the existing eight tables plus authorization and grants;
stage IDs remain 0 through 255. Unsupported existing versions are rejected
before writable setup pragmas. Authorization is durable, not reconstructed from
configuration or a grant-history scan.

Ordinary replay is indexed and independent of new reservation headroom.
Connection opening selects the durable total cap; new reservation separately
checks the admission margin before ordinary writes. Ordinary, terminal and
administrative transactions select their distinct page ceilings. A terminal
refusal rechecks the exact pending request, excludes acceptance, changes only
the terminal response/phase and active slot, and preserves charges.

Grant replay precedes active-work, new-grant, proposal and physical-supply
checks. Fresh renewal modifies only authorization and one exact grant record,
rechecks state in the transaction, and verifies consumed counters remain equal.
Cap expansion is included in that transaction; an uncommitted connection pragma
is not durable authorization. Failed COMMIT or uncertain rollback sets an
uncertainty flag that prevents later terminalization; administrative uncertainty
uses `RENEWAL_OUTCOME_UNKNOWN`.

Readonly opening uses `mode=ro` and query-only, without changing the durable cap.
It can report pages exceeding that cap. Memory temp storage and disabled mmap
also apply to the readonly connection. The noncreating owner-lock path now
locks before reading its bytes, preserving `BUSY` under Windows byte locks.

## Administrative worker and owner adapter

Status reads the actual authorization/usage singleton, bounded heads, indexed
active request/provider, and page counters. It does not reserve ordinary work
or invoke mathematics. Existing locks are acquired before an absent-database
answer; an absent lock and absent database can be observed without creation.
Historical contexts are explicitly not asserted live or intact.

Known refusals, including malformed envelopes before operation selection,
declare no recorded grant and unchanged renewal state. Generic renewal errors
remain conservatively unknown, including known-rollback generic errors; same
exact-envelope retry can discover whether a grant exists. No ambiguous commit
is declared rolled back. The adapter forwards successful response bytes exactly.

The owner adapter supervises valid-size envelope parsing, preserves failure
CPU/cleanup observations, and counts success or failure evidence only after
confirmed quiescence. Empty/oversized-input preflight explicitly discloses
unmeasured owner-prefix CPU and a definite unchanged refusal.

## Required before integration or qualification

- Wire configuration schema 3 and fresh initial-capacity validation into the
  actual configure/load paths. Keep mathematical stage-plan schema 2 separate:
  `run_stage.execute` must not pass a schema-2 plan to a schema-3 config reader.
- Wire ordinary prior lookup before new-work guards, supply `scratch`, and
  map confirmed ordinary `SQLITE_FULL` rollback to bounded `METADATA_SPACE`
  terminal refusal. Uncertain transactions or failed terminal persistence must
  remain pending/unknown; neither renewal nor a retry may clear them.
- Integrate the owner CLI commands and pre-config `OWNER_COMMAND_FAILED`
  boundary. Invalid configuration cannot authorize an event-file write.
- Qualify exact replay, read-only status, page tiers and margins, cap-only
  reopening, ceilings, grant conflicts, malformed input, caller-output loss,
  and cleanup with separately retained evidence. Numeric limits and this source
  argument do not establish actual SQLite, Windows or long-run behavior.

Earlier lock ordering, generic-renewal error coding, unhashable operation input,
pre-operation refusal fields, failed-call census, empty input and readonly-profile
findings were corrected in the reviewed cut. Beyond the listed integration work,
this review found no further source-level
violation of the central authorization/replay invariants. Physical supply,
SQLite margins and continuing native operation remain empirical obligations.
