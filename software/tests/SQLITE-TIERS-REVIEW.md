# SQLite tiers: source and exact-launch review

## Decision

**PASS — no unresolved pre-execution blocker found in this reviewed cut.** This is a bounded source and exact-launch review, not a test result or approval of product renewal. Root remains the sole executor. The reviewer performed no Python/Lean execution, import, compilation, or SQLite query.

The complete suite, source note, operating-envelope proposal, original runner, and complete revised runner were read. Relevant unchanged supervisory interfaces were checked against their earlier complete source review. The exact prospective `software/qualification/sqlite-tiers-launch-01.json` was subsequently supplied, read, and independently checked; this decision does not extend to an uninspected launch.

## Frozen review inputs

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `software/tests/test_sqlite_tiers.py` | 25190 | `75d1422afc445166d8b412488ca346fd9c455ff5ddf500e3fde6c17350e623d9` |
| `software/tests/run_metadata_contracts.py` | 11193 | `a0990a7f06d30aab19b6371f6357f4045244a7c6d9c32bf03d9c7cac29b5239d` |
| `software/tests/SQLITE-TIERS.md` | 13006 | `4399cdb583e02e9f22f31a77717e194382c02d5a271d11821bd09c3b8d5b40a8` |
| `software/drafts/OPERATING-ENVELOPE.md` | 22245 | `2245ed1608a995294c7558ad90c62fa1e17820e69b2c9c74eb5f26e04c520a53` |
| `software/qualification/sqlite-tiers-launch-01.json` | 1693 | `e846c6c5301d5c63e1e8a37b358aa9433e51f66f83856e4208728ea645e7a18a` |

The launch has exactly six ordered input pins, totaling 192,416 bytes: Python, coordinator, `run_stage.py`, `supervise.py`, `domains.py`, suite. Each path, length, hash, row field set, and position matched actual files. Besides the coordinator/suite above, the checked inputs are:

| Input | Bytes | SHA-256 |
|---|---:|---|
| `D:\Python314\python.exe` | 106208 | `03168c01b7b7491423350e82c26fee71f35b43694d1319d3c668bda6903a0c38` |
| `software/py/run_stage.py` | 26505 | `3c84f507dbb788827dbd50de2d0d7552e4f72bd615f425cfd5f1da278ac5a5be` |
| `software/py/supervise.py` | 18611 | `e5f35c0a88602757ecb7ff899f923f940b588e11e2a7c9c36d51fdbb2dfcac1b` |
| `software/py/domains.py` | 4709 | `a3f44cce31ddd79056f0683de17d46712bfd46c99dfe71fac56e27dd1deb59c9` |

The launch itself becomes the seventh supervisor pin. It fixes allocation `sqlite-tiers-01`, the exact suite, five tests, 60 wall seconds, 30 Job CPU seconds, 512 MiB memory, eight active processes, and 65,536-byte stdout/stderr/event bounds. Combined retained endpoint limits are 256 MiB, 4,096 files, and 8,192 entries. Both `product-local/sqlite-tiers-01` and `software/qualification/sqlite-tiers-01` were absent at the final exact-launch check; their parent ancestry showed no reparse point.

## Fixture correctness and claim boundaries

The selected 4096-byte-page tiers agree with the operating-envelope proposal: total 8192, ordinary 6144, terminal-only 7168, and new-admission threshold 4096 pages. Expansion to total 16384 yields ordinary 14336 and admission 12288. These are engineering guard choices, not certified universal storage margins.

The five source-level test contracts are coherent:

- High-water/replay writes enough bounded payload to require pages above the ordinary tier, tests the actual returned ceiling when requesting an impossible lowering, reopens at the durable total cap, and checks exact historical response bytes and unchanged logical rows. Read-only status separately requires absent/empty sidecars, `mode=ro` plus query-only, actual `SQLITE_READONLY`, and identical file-name/size/hash maps.
- Full/rollback requires an actual `SQLITE_FULL` at the selected oversized write, not any generic error. It observes transaction state, rolls back, verifies the entire committed logical projection and pending binding, and only then permits the small terminal-only refusal. The expected logical delta changes exactly the selected phase/response and active key; it preserves consumption and disallows visible rows.
- Cap-only expansion distinguishes a rolled-back durable-cap update from a transient connection pragma, then commits one grant with only the selected cap/grant-count changes. A subsequent actual synthetic reservation incurs its ordinary charge. The pre-expansion refusal portion evaluates the Boolean admission predicate; it does not exercise an implemented product refusal path.
- Near-limit data checks payload lengths, an actual committed index root transition from leaf-index `0A` to interior-index `02`, 64 bounded grants, and SQLite integrity checking. Direct page-byte inspection is applied to a committed database with known page size, not unflushed speculative pages.
- Persisted SQL checks reject invalid ranges, nonintegral values, and overflowing arithmetic. Separate rolled-back demonstrations explicitly show that INTEGER affinity loses original Boolean/numeric-string token distinctions. Parser validation remains an independent obligation.

Every fixture is synthetic and unpromoted. The shared `state` row is not the proposed production schema, historical reads are not product replay qualification, and successful transactions are not crash testing. No native checker, accepted context, product renewal, physical reserve, indefinite availability, or mathematical growth is established by these examples.

## Resource and evidence checks

The intended successful source path has **37 large-payload attempts totaling 70 MiB minus 320 bytes**. This arithmetic was independently checked. Attempts, including failed writes, are bounded to 64 and 96 MiB; each is at most 2 MiB. Separate small/grant rows are bounded and explicitly excluded from that counter. There is no fill-until-success loop or retry.

SQLite must report version 3.50.4. Each connection has a 3-MiB value/row length bound and a progress callback every 100 VM instructions; a method interrupts after callback-accounted work exceeds 500,000. These callbacks do not measure every sub-callback instruction. Fixture enumeration is bounded to 128 entries/256 MiB, observations to 256 rows, and each report to 1 MiB. These are sampled/endpoint checks, not hard transient filesystem quotas. The enclosing Job is the wall/CPU/memory/lifetime envelope.

Teardown attempts rollback/close for all registered connections and preserves observations on ordinary assertion failure. Unittest success, exact test count, and no skipped tests determine the worker outcome; report existence alone does not. OS termination or persistence failure may prevent a report. Such absence cannot justify success or zero cost.

The revised coordinator authenticates six ordered pins before allocation, snapshots reviewed source, checks imported module origins, and uses the unchanged reviewed supervisor. The worker reauthenticates the pins, exact request, fresh state binding, suite module origin, and five-case discovery count before running. Launch parsing rejects duplicate keys/nonfinite constants, requires schema/type/field constraints, and fixes the bounds. A returned worker pass additionally needs successful transport and verified direct-child reaping, zero final active processes, Job closure, and no cleanup errors.

Post-allocation setup/snapshot/import/transport failures enter retained failure reporting where the filesystem permits. Census is allowed only after verified quiescence or when transport was never attempted. The final census accounts for both roots and reserves two final records plus 65,536 result bytes; failures cannot silently become passes. The strongest successful coordinator result is `PASS_PENDING_AUDIT`.

Job CPU includes worker execution once. Coordinator CPU/time start at coordinator entry and are measured separately through final report preparation. Interpreter startup and final persistence remain excluded, and `cpu_complete` stays false. Failure observations are not converted to zero. Exact runtime-library attestation and hostile-local isolation are outside the trusted Windows/Python/SQLite profile; an executable hash alone does not provide them.

## Review corrections and required outcome audit

Before this final cut, the coordinator gained explicit coordinator accounting, worker pin reauthentication, exact import/suite origins, stricter launch parsing, and post-allocation setup-failure retention. The source note's journal claim was corrected: SQLite DELETE mode normally removes journals on commit/rollback; retained evidence consists of database files, observations, and surviving sidecars, not every journal's contents. Journal/page peaks remain sampled peaks.

No remaining source or exact-launch blocker was found. After root's single prospective execution, independently check the actual five outcomes, real SQLite error and page observations, rollback/delta evidence, read-only file maps, intended workload counts, retained hashes, resource accounting, and cleanup. A version mismatch, unexpected failure location, missing evidence, limit failure, or predicate failure must remain a failed allocation; this review authorizes neither a silent adjustment nor automatic retry.

Even a complete finite pass only supports proceeding to a separately reviewed implementation decision. It does not discharge the operating envelope's production-schema, crash/reconciliation, physical-supply, cumulative-renewal, native-acceptance, or longer-horizon obligations.
