# Fresh managed-storage manager and supervisor source

2026-10-21, support_guest. Root-selected source-only implementation after
MANAGED-STORAGE-PROFILE-BINDING-REVIEW. No imports, parser execution, tests,
database opens, processes, network, installation edits or Git. The source is
ready for independent review, not runtime/profile adoption.

## Exact new source

| File under software/v5/managed_storage/placement | Bytes | SHA-256 |
|---|---:|---|
| lifecycle.py |39828|`0fa3dcc4285aa4afc87dfda5741e5c68334f8c0398138c3f218351e705a1f427`|
| sessions.py |20462|`6e07010c47b0e95abbb80125e838b759e2a4206bdc3cafa735e31c7015d1a63b`|

Copied through apply_patch from the exact selected supervised_generations
predecessors. Their independently re-read SHA-256 values remain unchanged:
lifecycle `bec62143313e1abd400550bae45a6334be2ddffb94d77a14ba9b5853b565042f`;
sessions `b4cfab61c990464756e87a7344e2a029a5374602283a4255d4d5aa854090b7f7`.
New sources use LF; predecessor bytes were not normalized.

## Manager changes and ordering

- Fresh schema: `DMKN_V5_TWO_GENERATION_MANAGER_STORAGE_V1`. Exact config adds
  `storage_profile`, required equal to SP.PROFILE, and hex writer_profile_sha256.
  The existing manager marker hashes the whole immutable config. Generation
  identity hashes that marker, so generation marker/config binding transitively
  includes both profiles without a new per-store authority token.
- `ManagedGenerations.open` now requires keyword `writer_profile_sha256`.
  Compare it to config before any manager write, retaining `_writer_profile`.
  The installed owner must independently reconstruct it from the verified full
  SDK logical `{bytes,sha256}` map, fixed base manifest and fixed SP.PROFILE.
  The argument is identity supplied by trusted current code, not an untrusted
  digest that proves its own code/runtime correctness.
- SP.registry_envelope runs before mkdir/lock/SQLite creation. Marker serialized
  length is also checked before mkdir. Existing manager reopen runs
  SF.registry_preopen before append-mode lock open or SQLite connect: exact
  marker/profile/config/root, known root grammar, lock and DB/journal bounds.
- SF.preopen_lock precedes the existing one-byte lock writer/acquisition;
  SF.preopen_database precedes connect. SP.configure_connection immediately
  follows connect, before every existing PRAGMA or schema statement. Existing
  stricter pragmas, schema/config checks and close/refusal path remain unchanged.
- `_active` retains immutable config checks and compares current config/profile
  with `_writer_profile`. Allocation runs SP.generation_envelope before the
  sequence/PROVISIONING transaction; `_records` revalidates the same storage
  fields/reservation for stored generations, including retired/reclaiming ones.
  No payload/file walk was added to `_records` and no deleted file is demanded
  back during reclamation.

The allocation gate covers every storage-bearing cap/type, explicit Node
metadata and existing allocation role bindings. It does not duplicate/extract
full workspace, service, egress or Node semantic validators. Those existing
validators still run before their respective writers; a later non-storage
configuration failure stays charged. No refund, retry, migration or free-space
promise was added. Fresh enrollment interrupted before manager.json is written
cannot reopen: its partial root stays preserved/held, not adopted or repaired.

## Supervisor changes

The only sessions changes are three additive lines: `_Launch` captures the
current manager `_writer_profile`, with a comment, and `_open_launch` passes it
as the required keyword. This covers both suspended-worker binding and exact
surviving-Job quiescence recovery. It does not copy the config value as authority
or change deadlines, session profile, process identity, Job ownership, calls,
charges or recovery semantics.

## Static verification and integration boundary

A read-only text LCS comparison against each selected predecessor confirmed
only the changes above: lifecycle679->701 substantive lines, sessions400->403.
All original DDL/transactions, generation/run accounting, reclamation, current
handle checks and false adoption flags remain. New file sizes/hashes were read
directly. No syntax/runtime/control result is claimed.

Root owns storage_profile/storage_paths, owner/composer and final source-map
integration. Required shared APIs are `registry_preopen(root, expected_marker,
max_pages=...)`, `preopen_lock(path, create=...)`, `preopen_database(path,
max_pages=..., create=...)` and `configure_connection(connection, max_pages=...)`.
The composer separately owns exact generation marker + generation_preopen before
service construction. Screen owns six store successors; core owns Node guard
and pre-write identity/adoption caps. All these edges need independent integrated
source review before any execution or conditional apparent-bound claim.

`physical_envelope_adopted` remains false everywhere in these two successors.
The fresh source neither adopts a physical allocation envelope nor certifies
SQLite binary/source correspondence, OS/VFS premises, mathematical acceptance,
reclamation progress or external lifetime output accounting.
