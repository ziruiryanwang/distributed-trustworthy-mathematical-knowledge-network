# Independent outcome audit: complete local source-archive installation

2026-10-26. **PASS for the single selected local archive-only installation chain.**
The actual 143-payload source archive produced fresh native outputs, all four
public overlays and a final working inert query through the shipped launcher.
This closes the identified source-distribution integration gap; it is not full
v5, independent-host deployment, mathematical admission or useful-growth evidence.

Audit method: saved JSON/argv/logs, ordinary file hashing/census and read-only
in-memory PE inspection. No test rerun, product import, compiler, network call,
source normalization, state operation or Git mutation was performed. Root owns
adoption. The earlier source REVIEW and used inputs/evidence remain unchanged.

## Selected inputs and extraction

Evidence root: `experiments/v5-local-checks/archive-install01`.
Original and saved selection both hash to
`ff55b721aab172dc3f3b3a61bd35fbc70eb6f1a7b149261f0671a4266c36ec74`.
All three original/snapshot source pairs and all 27 external input pins still
match selection. The latter include the exact ZIP/receipt, two inert query
inputs and 23 named runtime attachments; no generated predecessor package was
selected as a build input.

The extracted `suite/source` has exactly 143 payloads, one manifest and 34
directories, no extra files or reparse entries. All 143 payload lengths/hashes
match the approved manifest, totaling 3,743,035 payload bytes. Manifest SHA-256
is `f1beab01d43e4b5fc6d7b9999ff2795598e3f2ee77c0dc85f1d99e82a15b31f1`.
The original 3,789,448-byte ZIP still has SHA-256
`897a6eb57056b911b200551413c65ce7788ba3d448ff8b6b8c143d883180ebd0`.

The actual public verifier was invoked from this extraction and returned
`VERIFIED_EXACT_SOURCE_NOT_BUILT` for the exact manifest and 143 payloads.
The actual build command likewise selected this extraction as its source root.
Saved `_build/SOURCES.json` names precisely its 84 mapped sources plus builder
and map; all 86 staged files independently match both this receipt and archive
payload pins, with no extra staged file. Native commands use fresh build-local
source/object/helper paths and the explicitly selected external runtimes.

This is successful use of the archive's complete intended source-input closure
on this host, not OS-enforced proof that arbitrary host paths were unreadable.
The retained test supervisor is external test infrastructure; runtimes and their
unnamed support files remain approved nonhermetic attachments, as before.

## Actual native build and immediate overlay chain

All seven public calls have retained command/process records, terminal exit zero,
direct-child reaping, empty stderr and stdout agreeing with their parsed reports.
The build/overlay stdout objects also agree with their actual saved receipts.
No failure receipt is present. There was one native build, not a silent retry.

The three direct build Job reports and nested base compiler Job report all show
`COMMAND_EXITED_ZERO_AND_CLOSED`, zero exit, reaped direct child, closed Job,
zero active/terminated processes, empty cleanup errors and no termination
request. Their CPU observations are known. Extractor logs contain seven successful
codegen/object pairs and both successful links; query compilation also exits zero.

Independent generated-pin comparison matches all **80 shipped native files**:
eight receiver objects, 65 original authoring companions, five newly compiled
query companions and two exporter executables. These match this run's actual
COMPILED-FILES, QUERY-OUTPUTS and EXTRACTOR-OUTPUTS records, not an older binary.

Every assembler uses the immediately preceding new package/PROFILE/receipt in
its retained argv. Independent raw receipt hashing and predecessor fields agree.
All five complete package maps were hashed, including unchanged payloads and the
declared overlay changes; there are zero size/hash/census mismatches.

| Stage | Files including PROFILE | Actual PROFILE SHA-256 |
|---|---:|---|
| Native build | 146 | `34ea1fa0fbfef4836f3fe6b00b3997173c469d6ed8c75c1b3b2ceb9b04815773` |
| Fair | 148 | `5ca74fd26351a6c8e7f24fe380ef87e0da6d3ae459ebf23f3a4279289f3b4312` |
| Contact | 150 | `8a5155cbb7469e4da48562033f9d966841bf5b300895f79ea02f3d2375fb3b20` |
| Sparse | 152 | `1fdb4cd3375cfea4b2089c3e4618acda2de6fdae07d229fdc324e55c6f424c69` |
| Transport | 154 | `1c98f0f1ae7de0c1b5839e56f95ac74cd8f2fd349aed63afc427d2d4fd9ae9cb` |

The installation manifest stays exactly
`32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`
through the chain. Final package is `suite/transport/package`, with 154 files
totaling 39,128,222 bytes, excluding external runtime attachments. The final
receipt is SHA-256
`133407068c4585d5d303a7aa3bc7b70d7ec3114711b98ce8b685252cb477c1d5`.
All native bytes remain unchanged across the four file-only overlays.

## Final public query

Actual `suite/transport/package/run.py` launches that package's query entry with
the final PROFILE, both retained inert inputs and the original finite query
allowance. No catalog/custody/context argument selects owner-state opening.
RUN reports `CLI_EXITED_ZERO`, `ok: true` and mathematical disposition
`NOT_INTERPRETED`. The raw query supervisor independently has the full clean
closure properties above. The child stdout agrees with `query/RESULT.json` and
its stderr is empty.

Query output contains exactly QUERY, SPECS and RESULT. Independently hashed QUERY
is `eb611ed660111779f3bf1a05c044c2a362735d08eb91f7a6151ea80d9108c16a`;
SPECS is `7c707bb2b3f5cc2628eef4fcb933c7944156ead940ad02465fa42084049dc72d`.
The expected input hashes, final profile binding, `mathematical_acceptance: false`
and zero worker CPU agree. This exercises actual package loading and inert query
preparation, not query execution against providers or new native mathematics.

## Exact comparison with the earlier default package

Against `transport-release-handoff01/suite/assembled/package`, a complete
154-file comparison finds the same paths and **151 byte-identical files**.
Only PROFILE and these two executables differ; sizes are unchanged:

| File | Bytes | New raw SHA-256 |
|---|---:|---|
| `authoring/bin/BaselineExporter.exe` | 809,472 | `aed83c5ec56e3607f2e0b669f66bc8f0efac35500c4400446bdfe29253514997` |
| `authoring/bin/MissingImportExporter.exe` | 768,000 | `a3dd3b88c300e7895b2cdf0cf0a86730cc3e73fb586715c615ed7e6f91fb7c58` |

Direct in-memory PE parsing locates each difference solely within its four-byte
COFF timestamp at byte offset 128 and four-byte debug-directory timestamp:
578564 for BaselineExporter and 544260 for MissingImportExporter. Exactly six
bytes differ in each file: the first three bytes of each timestamp field. All
other executable bytes match. The new two fields both hold 1793009311; their
old values were 1792892753 and 1792892752 respectively. PROFILE changes only
the corresponding two file hashes; its schema, helper paths, author worker,
installation hash and other file pins remain unchanged.

No file was normalized, patched or rewritten. This identifies ordinary rebuild
timestamp variation; it does not prove general compiler correctness, runtime
equivalence for arbitrary PE loaders or bit-reproducible builds. The new exact
PROFILE/raw executable identities must remain distinct from the old default.
The old source/qualification evidence is not rewritten as a new execution.

## Outer closure, cost and evidence

The outer raw result is `COMMAND_EXITED_ZERO_AND_CLOSED`, exit zero, direct child
reaped, Job closed, zero active/terminated processes, no cleanup error and no
termination request. Its cumulative 113 process entries are not simultaneous
active processes; the original active-process limit is eight. Outer stdout is
26,788 bytes and stderr is empty. Suite status is
`PASS_LOCAL_ARCHIVE_INSTALL_NOT_FULL_V5`.

Total outer elapsed time is **144.5682446002029 seconds**; supervision through
cleanup is 143.97370469989255 seconds. Inclusive Job CPU is **70.46875 seconds**;
separate outer-runner CPU is **1.53125 seconds**: **72.0 seconds known total CPU**.
Recorded peak Job private commitment is **941,723,648 bytes**. Native build
direct-process elapsed time is 117.98398389993235 seconds; the full driver interval
is 143.3866842002608 seconds. These are this run's measurements, not a speedup
comparison or forecast.

The original 600-wall/540-CPU-second, 2304-MiB/eight-process outer allocation was
not renewed. Inner build Job CPU, nested compiler CPU, query CPU and driver CPU
are already included in outer Job CPU and are not added again. Job commitment
is not total host RAM, and sampled logs are not hard disk quotas.

| Saved evidence relative to execution root | SHA-256 |
|---|---|
| `RESULT.json` | `f6d8d1bf4ee224af6db26def0551933bc88bcf2f2efc06057e8ae20baca5a3ff` |
| `suite/RESULT.json` | `ad36d0d966a66d0bf4e55e68991162a647543fe2b6a4aa0b84968ec459a00db4` |
| `suite/build/_build/BUILD-RESULT.json` | `66d38395eec88917b5cf59ae2ac80496eccdfb889b13fd4f795bfab06f50906c` |
| `suite/query-diagnostics/SUPERVISION.json` | `64ea9327264d02c090f8c27c6cba13ef2197765ff7ec2ab5e6e441d1a87fa8fd` |
| `suite/query-diagnostics/RUN.json` | `6f39b93d2b2d9c69a9509756fec29c188591e2575820704e797f95d5a67bf9ea` |
| `suite/query/RESULT.json` | `12d9998f0b6490c6c9f6164e92280155396686591aec31743e4a09aeca237bfd` |

Disposition: adopt this particular local installation result if root agrees.
Do not rerun unchanged native/control campaigns or equate this with mathematical
growth, hostile-input isolation, public release authentication/licensing or
independently hosted availability. The selected-export companion remains a
separate artifact, not silently included in this archive. Everything stays local
and unpublished; the broader v5 goal remains unfinished.
