# One-payload overlay: independent source/allocation review

2026-10-26. `current_acceptance_challenge`. **SOURCE/ALLOCATION-CLEAR** for
root's one file-only `binding-package01` operation. No assembler, product code,
test, native work or state was executed by this reviewer. No architecture gate
is reopened and no automatic follow-up is authorized.

Read complete final assembler, PACKAGE-PLAN, INTEGRATION, and pinned helper
source including its path/hash/census/write primitives. Exact reviewed pins:

- Assembler: `8067e7e862e5e3d6abd5513a30197f9bd167552f9223fd49fc0f263a0dec9e3c`.
- PACKAGE-PLAN: `5724d68d2a91c942e26f67819b4a062722221dac62bbcc740c3b606f6d03d205`.
- INTEGRATION: `819509939611d2e6ed08fe379e6b095025ac079575b28965a364874843dee7f9`.
- File helper: `9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30`.
- Selection `experiments/v5-local-checks/binding-package01.selection.json`:
  `aeafac34504288f3fee12f78681d0b0bc65b04310dba056d555a6453fd07933c`.

All **six source and 158 external pins** independently match. The externals are
the complete 154-file predecessor, its adjacent original receipt and three
Python runtime files. Future output is absent. The reviewed final CLI uses
`--base-assembly`; it pins predecessor identities internally and defaults the
successor to the exact reviewed snapshot and fixed `e4b52c2f...fa19b6` digest.

The complete baseline map derives from exact authenticated PROFILE,
INSTALLATION and original receipt. It requires 154 paths and 117 auxiliary roles,
bounded file sizes and the old binder identity. Exact file census, safe relative
paths, ordinary nonredirected files and every old hash are checked before copying.
Output is fresh and disjoint from selected inputs. Only the exact successor
binder and canonical PROFILE can differ; an explicit map-delta check enforces
those two paths. The other 152 files, including INSTALLATION and eight documents,
are copied as new separate files and retained byte-exact.

Every destination is exclusively created, bounded while copying, flushed and
hashed. Before PROFILE publication, complete source/output maps and selected
receipt/helper/successor/assembler pins are rechecked. PROFILE is written to a
fresh pending file, verified and renamed last; final census/hash follow. The
external receipt records the complete map and is read back. Failures preserve
partial files without retry/deletion. A late failure can leave a profile present;
process closure and complete output audit remain necessary, never receipt alone.
This relies on immutable owner-controlled inputs, not adversarial concurrent
filesystem mutation or a claim of crash-proof transactional durability.

Actual selected argv is isolated Python `-I -S -B`, snapshotted assembler,
`--source-root {snapshot}`, exact predecessor package/receipt and
`--output {output}/assembled`. The snapshot contains both helper and successor;
its path and the future output are siblings, not overlapping inputs. Inner
45-wall/20-CPU seconds sit inside **60-wall/30-CPU/512-MiB/one-active-process**
outer supervision, with 262144-byte stdout and 131072-byte stderr caps. No
product import, native rebuild, state open, network or repeated Std export occurs.

No blocker found. The unchanged loader's selected profile supplies the new
auxiliary hash; this is source compatibility, not an executed load. INTEGRATION
correctly retains the old preparer/source-map mismatch as an explicit later
distribution issue. This operation creates only a development overlay, not a
rewritten source archive, new implementation identity, qualified public release
or completed mathematical workflow. Next evidence may be a complete saved map
audit and one separately selected state-free public command, not another suite.

