# Reader-only file assembly

2026-10-28. Source preparation only; root selects exact execution separately.
`assemble_reader.py` is a fresh successor of the frozen owned-acquisition
assembler `48a7235c9bd1d8eacb8e5a7b44e25a2ce5ab6666ef509b25877b4f762d6c2042`.
It retains the same bounded file-only helper, checks, failure preservation and
output sealing. No product, owner, database, network or native call is added.

The adopted input is
`experiments/v5-local-checks/owned-acquisition-kit01/packed/commons`, with its
adjacent `packed/RECEIPT.json`:

| Input | SHA-256 |
|---|---|
| KIT-MANIFEST.json | `e3f7ea9e310be5424aac58f1b0ed43ae40d54a3a02a387b8b4388b335c37f3ec` |
| External RECEIPT.json | `a59e4c1491793051059403f33afdfd58eba3e21368634f0fd39f7975cad2e32f` |
| Package PROFILE.json | `85d45c928523c2b96f127ec8c15b2e2664f8428f0c1ef2415470a5b30737d3c8` |
| Installation manifest | `9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27` |
| Kit source/software/v5/ordinary_owned_acquisition/source-map.json | `797ea254070ea489643fefcba2c4f092bdd4442d0f2eb670694fadb8e5dffa10` |
| Reused ordinary_fair_search/assemble.py | `9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30` |

The new source map may substitute exactly four roles with the final author-owned
files from this directory: `peer_api.py`, `support/transport/http_provider.py`,
`support/transport/ordinary_acquisition.py`, and `support/transport/fair_exchange.py`.
Only those four payloads and PROFILE may differ in the exact 160-file package;
the other 155, including every installation, owner, profile-loader, native and
module-anchor support payload, remain byte-identical. The source-map structure
and counts remain 93 source inputs / 78 direct copies. The operator role, Node
runtime, gateway/controller and advertisement helper are packaged separately.

Current preparation state: assembler source is ready; final `source-map.json`
and its pin await query_scaling's final four reader-source pins. Do not execute
against temporary authoring bytes. Final source/plan/map pins require independent
source review and root's separate finite selection.

Proposed envelope reuses the predecessor: Windows Python 3.14.6 with `-I -S -B`,
90 wall seconds, 45 inclusive Job CPU seconds, 512 MiB, one active process,
1 MiB stdout and 1 MiB stderr. Internal checks remain 60 wall / 30 process CPU
seconds. These are proposed limits, not a runtime authorization.

Required arguments are `--source-root`, `--base-kit`, `--kit-receipt`,
`--source-map-sha256`, `--output`; all use absolute canonical paths. Suggested
fresh output is
`experiments/v5-local-checks/export-location-reader-assembly01/distribution`.
Root creates only the outer selected parent before launch. Outputs are the
160-payload `package/` and `ASSEMBLY.json`; no predecessor is overwritten.
Every shell call uses explicit workdir
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

The builder verifies baseline package bytes and complete census, manifest and
receipt bindings, exact four-role map substitution, selected input pins, every
copy readback, unchanged installation and anchor-support inputs, and final
source/input/output identity before sealing. File assembly establishes byte
identity only; ordinary-location correctness and full v5 acceptance remain
separate. No passing transport, owner or native campaign is repeated here.
