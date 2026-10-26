# Source-only workflow-distribution implementation

2026-10-26. Owner: service_lifecycle. Implements the root-selected CONTRACT;
independent review and a separately selected file-only gate are still required.
No utility import, tests, packing, extraction, build, native execution, networking,
state mutation or Git mutation was performed by this author.

## Boundary and mapping

The new `bundle.py` defines an explicit destination-to-source `SOURCES` map and
five fixed unchanged companion pins. The original 143-file manifest is selected
by exact SHA-256, validated by the original manifest parser and bounded source
map, and preserved as `BASE-SOURCE-MANIFEST.json`. All original payloads retain
their exact path and bytes. The new root manifest is
`WORKFLOW-SOURCE-MANIFEST.json`: 154 payloads plus itself, 155 ZIP members.

The ten explicitly mapped additions are the eight companion destinations,
the new utility at its normal software path and this directory's README mapped
to root `START-HERE.md`. The retained base manifest is the eleventh addition.
The README documents every map and all three copied-guide changes. Commands in
those guide variants are unchanged; only missing navigation and service status
text are replaced, with new copies using LF. Original guides stay preserved.
Tests/contracts/reviews/this checkpoint are not payload files.

## Public interface

```text
bundle.py pack --source-root ABS --base-manifest ABS --output FRESH_ABS
bundle.py verify --source-root EXTRACTED_ABS --manifest-sha256 HEX
```

Python APIs are `pack(source_root, base_manifest, output, *, check=None)` and
`verify(source_root, manifest_sha256, *, check=None)`. Source-only reviewer/test
helpers are `helper()`, `base_files(base, raw, root, check)` and
`validate_manifest(base, doc, original_files)`.

Packing is repository-only because explicit guide variant sources are mapped
to their operational destinations, not redundantly shipped. Relocated verify,
the unchanged build chain and all end-user workflows are standalone. Repacking
an extracted archive is deliberately not another supported feature.

## Trust and boundedness

Before executing the original helper, bootstrap logic checks absolute local
ordinary paths, every ancestor for redirects, the helper's single-link regular
file identity, 22,041-byte bound and exact approved SHA-256. It executes only the
checked byte buffer. Product modules are not imported. Owner-controlled stable
inputs remain a premise; this is neither a sandbox nor an authentication scheme.

The union validator checks exact schema/roles, original projection, fixed
unchanged companions, path and size limits. Verification checks the complete
ordinary census twice and all payload hashes, including association and running
utility equality. Packing checks all inputs, writes only a fresh stored ZIP,
reads actual members/metadata back, rechecks all selected source bytes and writes
its external terminal receipt last. Partial failures are retained. Existing pure
helper path/read/hash/JSON/guard/census primitives are reused, not its old full
pack/verify contract. Cooperative limits remain 60 wall / 30 CPU seconds plus
the small fixed bootstrap and terminal-report boundary; hard limits require an
enclosing Job.

Service status text uses root-confirmed adopted finite controls and two idle
loopback leases only. It does not claim loaded service, mathematical outcomes,
continuous availability, full v5 or external publication.

## Initial author checkpoint hashes

| File | Bytes | SHA-256 |
|---|---:|---|
| bundle.py | 13182 | ceae62463c13dccd3a58faea0b8548d1454e09de3877b8058303dd51619b10c7 |
| README.md | 14151 | 16928d92d9d789078d980a5aba36fa82508e06de36e4a5e4d55f06698bfbb47f |
| guides/SELECTED-EXPORT.md | 7435 | 0960fcee0a4427463918f2590d7c30dffb9f3abf7c97b1346d963b551b7ef5cf |
| guides/UPDATE-AND-RECOVERY.md | 6055 | 2145ebf632263c1289b025ff6d31977c2cd3de994c2063dc0e17128f21f2e2d7 |
| guides/SERVICE-PLAN.md | 9476 | a161d98eb21205d124b56415d48bdb08b6f66ca54802cf41c6719d9feae10d04 |

These are source checkpoint identities, not runtime outcome evidence. A later
explicit review repair must select its changed identities before execution.
