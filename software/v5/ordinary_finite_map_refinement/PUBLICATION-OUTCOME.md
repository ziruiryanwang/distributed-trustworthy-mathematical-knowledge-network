# Refinement publication: actual public-boundary audit

2026-10-28. Read-only review of saved
`experiments/v5-local-checks/finite-map-refinement-publication01`.
**The checked refinement theory was published successfully through the standard
bounded launcher into the existing local index.** No service, search, native
operation or owner/database operation ran during this audit; no 21-unit evidence
audit was repeated.

The exact request SHA is
`c51fc2d3668f356f9e801254c0989786bc5cc7c471f29f4cb0ee566c36c6170c`.
The public peer returns `ok=true`, `INDEXED_LOCAL_TARGETS`, context
`d06c73e7dbd80203deee01e565f508fa239f9b819e58b44588033718dd80e559`, and exactly
**200,395 evidence bytes read**. All twelve returned publications have `new=true`.
Their object IDs, locator unit IDs and structured names match the selected
Context-plus-eleven-target list exactly, in order. Twelve object IDs and twelve
returned snapshots are distinct. Mathematical acceptance remains false for this
indexing operation; acceptance came from the earlier contribution.

Continuity is checked at the public API boundary: the request opens the same
`finite-map-index01` with **`create=false`** and unchanged limits; old and new
records use the same namespace; the twelve new object IDs are disjoint from the
retained nine. The old publication RESULT remains exactly SHA
`0e3d52235f03daf26707fc7deb18510d4f205f99ea34449a6e08353cdf10aa04`.
Under the unchanged append API, those records give 21 objects, 371 postings and
73 distinct features. These are derived from saved publication records, **not a
fresh full-index census or independent snapshot-chain check**. SQLite was not
opened. The final newly returned snapshot is
`17c0bf9f8065dbf50e74ad97a80fe80a36fa43bd401a1a83e64654e82a9807d3`.

All four selected source snapshots match their pins, and selection SHA matches
the outer result. Outer stdout parses identically to `launcher/RUN.json`;
launcher-child stdout parses identically to `publication/RESULT.json`. Launcher
status is `CLI_EXITED_ZERO`. Inner and outer supervision both report
`COMMAND_EXITED_ZERO_AND_CLOSED`, child exit zero, reaped, Job closed, final
active/terminated processes zero, no termination requested and empty cleanup
errors. Both stderr files are empty; public cleanup errors are also empty.

Outer elapsed time is **3.0593944 seconds**. Known measured CPU is **2.75 seconds**:
2.171875 Job + 0.578125 outer-wrapper CPU. Nested launcher/peer counters overlap
the Job scope and are not added again. Peak Job private commitment is 56,012,800
bytes. No native worker CPU was reported. These publication-only costs are not a
whole-cycle growth or novelty measurement.

| Saved evidence | SHA-256 |
|---|---|
| `selection.json` | `6ffdbfd182579cc33bb86f8add6ee879f218da1a60ee8a20ceb86e9e512d72a9` |
| Outer `RESULT.json` | `bbf951d632aa6169c46919716fc87a09ed88de9ecd2b5ab53d45a393fa21cdb3` |
| `publication/RESULT.json` | `2293b2c92d5e027f2b9f86703e5d202d2e26f5bc24fb45831423f7ec3941c245` |
| `launcher/RUN.json` | `b7365803d5b840b7a6c962fa6a7060d5a60506795d6fdcd149b4eb2e2499a134` |
| `launcher/SUPERVISION.json` | `79e1374b89e4cd3b7fe24b7c5c7c78ccaca73e9d33bdae823abf2c6fc852b386` |

This completes the bounded local search-to-interface-to-theory-to-index path.
Independent-recipient reuse, broad relevance, sustained availability, causal
growth benefit and full-v5 deployability remain separate requirements. No repeat
serving/search campaign or new mechanism is warranted by this audit alone.
