# Hosting cost cross-check

2026-10-28. Source/theory only, under the canonical project root. No imports,
tests, databases, owners, native work, sockets, code changes or Git operations.
This is a narrow cost check for HOSTING-PAYOFF-CHALLENGE.md, not a hosting
selection or a runtime qualification.

## Findings and corrections

1. **A supplied inert delta need not repeat dependency closure.**
   The selected `ordinary_binding_reuse/baseline_bundle.py:221-258` validates
   manifest identity, entries and aggregate ceilings. `validate_batch:261-286`
   checks each supplied unit's exact bytes, identity and structural bounds and
   explicitly says it does not check dependencies against a local mathematical
   environment. `make_manifest:335-355` measures chosen units and batches;
   `_measure:194-218` parses the evidence, measures outputs/imports and binds
   its identity. There is no dependency-availability traversal in this route.
   Thus repeated dependencies in immutable shards are a choice needed for some
   availability promises, not an unconditional bundle-format requirement.
   This conclusion begins with **already supplied delta files**. It does not
   show that a public producer can generate those files without reconstructing
   its selected writer closure. That materialization cost must be charged
   separately.

2. **Owner publication is incremental in index writes, but context preparation
   is not generally incremental.** The selected
   `ordinary_registration_refresh/peer_api.py:1103` calls
   `owner.catalog.context(context_root)` before selecting target evidence.
   `ordinary_lean/portable_catalog.py:530-547` walks the selected parent chain;
   `_root_row:306-317` parses each root record; `_context_rows:492-528`
   validates every selected record and reconstructs all selected name bindings.
   `_validate_record:390-490` finishes by checking its retained artifact.
   `_artifact:319-331` hashes the full artifact unless already verified in that
   catalog instance. The cache starts empty on open at line171. A fresh public
   owner process can therefore pay the bytes of the full selected artifact
   lineage, as well as its records/bindings, even for one newly published target.
   Repeated calls on one retained instance reuse artifact hashes, but still
   reconstruct/validate the selected context metadata. This is a selected-lineage
   traversal, not a claim that every unrelated root in the catalog is scanned.
   It is also artifact authentication, not native mathematical proof replay.

3. **Normal dedicated startup does not rescan retained evidence or index
   records.** `ordinary_multi_source/ordinary_acquisition.py:87-134` checks
   path/file/sidecar bounds, opens SQLite, sets pragmas and reads its config.
   `status:147-154` reads one aggregate counter row.
   `ordinary_sparse_access/discovery_store.py:57-118,147-159` similarly opens
   SQLite and validates config/quota metadata. Even the optional pair index
   uses only bounded configuration and aggregate rows plus a `LIMIT 0` table
   check (`pair_access.py:45-70,103-104`), not a pair-row enumeration.
   Dedicated `custodian.py:324-359` checks the seal, custody counts and index
   head/count, closes the preflight index, and calls `api.serve`, which opens
   the index again (`peer_api.py:1207`). Charge both opens.

   These are source-level metadata access facts, not constant wall-time or
   constant physical-I/O guarantees. SQLite may perform journal recovery while
   opening/reading; file/page work, B-tree lookup, storage latency, runtime/package
   verification, close and failure recovery remain real terms. There is no
   source-mandated full corpus replay on an ordinary clean reopen.

4. **Duplicate reuse saves retained growth, not all repeated work.**
   Custody `_put:187-204` first parses/hashes the supplied raw object, projects
   all evidence export locators, then checks stored length/hash, compares the
   complete stored raw bytes and verifies every projected locator. Its duplicate
   transaction performs no new object/locator inserts, but a cumulative input
   bundle still incurs cumulative supplied-byte and locator validation.
   Index `admit:221-237` extracts and validates the preview record before its
   duplicate lookup and exact record equality check. A duplicate then returns
   the current snapshot without adding a snapshot or postings.

5. **A new index record updates affected paths, not all historical records.**
   `discovery_store.py:245-266` processes each extracted feature, updates its
   posting vector, partition tree and feature map, then adds one snapshot.
   `authenticated_index.py:145-166` appends on a vector path of logarithmic
   height in that feature/partition's posting count; `205-230` reads/rebuilds
   the eight-level partition path; `314-348` follows one compressed feature
   path within a fixed 256-bit key. A useful cost model separates supplied
   evidence/preview validation, affected authenticated-node work, SQL B-tree
   accesses/journal writes, and fixed opening/closing costs. The node-path
   description does not license an exact one-digest-per-node or fixed-I/O claim:
   compressed-map validation and hashing have their own charged steps.
   Historical nodes/snapshots are retained, so physical/logical and snapshot
   quotas can eventually refuse new admissions. Bounded per-operation work
   and a small update do not imply unlimited node growth.

The resulting comparison must not call existing owner publication a whole-corpus
index rebuild, and must not call proposed append free of size-dependent database
cost. It can accurately say that dedicated delta append would avoid the owner's
selected-context/artifact authentication and preserve one retained custody/index
without mandating historical byte copying. The ingestion/recovery protocol itself
is still proposed and is outside this cross-check.

## Selected source pins

The selected map is
`ordinary_connect_ownership/source-map.json`,
SHA256 `80d46cbedad723a90a87db80c4b5ac1dd6054526911c643c425ede48ce00f713`.
The following exact source hashes were checked against its recorded selection:

- `ordinary_binding_reuse/baseline_bundle.py`:
  `e4b52c2f2e823cc98aa37c8cc7adb0cf79952def9c19b54d7072116a39fa19b6`.
- `ordinary_lean/portable_catalog.py`:
  `aeaf0c7d507baa6b63d401c432ca71557bf29b6b576b1f6cd8381e4e87c7473e`.
- `discovery/authenticated_index.py`:
  `77a12cda9dd4a303153b59d00998de8aa6bf08bb572af10136e21dfa9c96cc95`.
- `ordinary_multi_source/ordinary_acquisition.py`:
  `076130f7a34b505df33ee550501d1c4276bb46e408ff226df765225933a0658e`.
- `ordinary_sparse_access/discovery_store.py`:
  `26ccca0fda86a255c38f7c3cc39b6b1fd88deba2ae10c6f79bc562b872c9502c`.
- `ordinary_sparse_access/pair_access.py`:
  `7d3f2fc199736df54d76b421f3587ebc8a0167bd75363921385a1916b832116c`.
