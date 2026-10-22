# Independent review: typed snapshot installation pin boundary

2026-10-22, storage_outcome_audit. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

**CONFIRMED_STATIC_BLOCKER.** The current retained typed profile cannot satisfy
the generic snapshot selection contract. This is established by source and
finite metadata inspection, without a producer constructor, import, test,
snapshot, request, proof, build, installation or live-proof inspection.
Do not launch a generic snapshot with this unchanged profile.

## Exact scope and method

Profile:
`experiments/v5-local-checks/typed-production-controls-01-profile.json`, SHA-256
`1242b0a8430e68032bbedbddcb3c6539fbdc95a2a5cf567936545c5f891246cc`.
Its exact hash was checked. The six relevant source records below refer to the
stable `typed-production-controls-01/sources/software/v5` tree; their small-file
hashes were checked and their bodies agree with the reviewed development sources.

| Source | SHA-256 |
|---|---|
| `production/producer.py` | `5555e944d7473731e3e9095e85c5c57ce89c5f59187f78c5b248b4c1227532f3` |
| `aggregate_small/producer.py` | `a2d23bcfe0b798f747d4a59330655a865a14a73cb4d635a50332fa65c75a6985` |
| `aggregate_lifecycle/snapshot.py` | `8c65e623419f846c2b7607716ce7fdec8a611ae2bb340e9a9cab18af3c741546` |
| `typed_production/producer.py` | `44c3700737300c879d5b85111361bd9e5bd55f8503a14e607d1a47c521c09692` |
| `typed_production/host_adoption.py` | `0553220f16866f8f9d0cb586f73d182e15074cf66c030421a903f4dcde7e5f87` |
| `typed_production/image_adoption.py` | `e1bf74167d09d3dbaceb841366363dc698cf290a891d5ffce743f86dfce76f4a` |

The reviewer independently walked the profile and its saved JSON records in
PowerShell, following constructor `_add`/`_records`/`_retain` statements. Entries
were merged by exact path with conflicting byte/hash rows refused. Only JSON
and small source files were read or hashed; binary payloads were not rehashed.
This proves the selected metadata's finite pin requirement, not present freshness
of every large artifact. One initial read-only calculation failed at PowerShell's
`Split-Path` parameter binding; correcting that calculation to
`[IO.Path]::GetDirectoryName` produced the counts below. No product work occurred
in either calculation.

## Constructor-only inventory

| Addition | Newly distinct nonempty pins | Cumulative |
|---|---:|---:|
| Support loader, manifest/helper files, interpreter/runtime, host and producer/source closure | 54 | 54 |
| Refined stage-host adoption | 190 | 244 |
| Typed guest/image adoption | 62 | 306 |
| Snapshot-host adoption | 9 | 315 |

The 315 unique nonempty records describe 147,559,292 bytes. Eight empty historical
evidence files are checked separately, not members of `_pins`: one refined-build
output, six guest compiler logs and one assembly stderr log. They do not reduce
the contradiction and are an additional historical availability dependency.

The increments are independently reproduced as follows:

- Support: manifest and its three loaded helper files; host, Python and its DLL;
  two support sources; 47 support-runtime rows; two aggregate sources; 29 typed
  lifecycle source rows. Existing repeated paths collapse to 54, not the sum of
  those raw list lengths.
- Stage: five build records, 179 nonempty rows from the 180-row source map, four
  newly distinct outputs (the fifth is the stage host already present), and two
  environment/input-map records: `5 + 179 + 4 + 2 = 190`.
- Image: ten adoption records, 37 project sources, two original adapters, three
  assembly-wrapper source copies, four compiler command records, two nonempty
  compiler logs, user ELF plus link map, assembly stdout and final image:
  `10 + 37 + 2 + 3 + 4 + 2 + 2 + 1 + 1 = 62`.
- Snapshot host: five build records, three source copies and one executable:
  `5 + 3 + 1 = 9`.

No U packet, receipt, current production continuation, capsule, checkpoint or
prospective V material appears in this constructor union. In particular, the
110-row runtime map of the currently running retained production operation is
not the generic snapshot's required map and cannot replace this calculation.

## Formal contradiction

Let `P` be the constructor's path-keyed `_pins` and `R` the generic snapshot
selection's `runtime_pins` map. The unchanged `_selection` requires both

```text
|R| <= 256
for each p in P: R[p.path] = p.sha256
```

The distinct-key count is `|P| = 315`. Inclusion implies `|R| >= 315`, contradicting
the cap before any workload-specific input is considered. For ordinary distinct
configuration, profile document and packet paths, the same loop requires at least
318 rows. The contradiction is unconditional on proof speed, RAM, packet size or
choice of U/V mathematics.

There are three independent 256-row gates: `tools/Run-V5-Check.py`'s `RUNTIME_COUNT`,
the new entry's `_snapshot_selection`, and generic `snapshot._selection`.
Changing only the new entry cannot repair it. The exact entry review remains a
conditional source-boundary review; it does not establish that the current
retained profile can execute a generic snapshot. Its inert controls intentionally
cannot detect or qualify this real installation-adoption boundary.

## Duplication versus necessary runtime data

Path duplication has already been removed. Some different paths may contain the
same bytes, but the current historical adoption code consumes their separate
locations and provenance roles. Deduplicating by digest or dropping arbitrary
rows from the outer map would violate the reviewed contract, not optimize it.

The host's snapshot execution needs the selected executable, guest image,
packet-derived wire/header, selected parent receipts and the actual runtime and
supervisor dependencies. Its recurring need for 261 additional installation pins
comes predominantly from re-adopting build history, source copies, compiler
records, intermediate outputs and logs. Those bytes are essential to the current
historical-adoption algorithm, but are not inherently mathematical or execution
inputs for every future snapshot. A build recipe or compiler log is not a lemma
proof or a premise of the final cryptographic statement.

This distinction must be implemented as a new explicit adoption boundary. Merely
omitting historical checks under the old profile would silently weaken that
profile's meaning. Raising all three caps could make this one retained research
installation operable, but would retain hardcoded experiment paths, historical
availability dependence and repeated provenance work. It is not the preferred
production remedy and is not authorized by this review.

## Smallest principled production remedy

Select a fresh **release-owned installation profile** with a separate schema and
identity, over the unchanged mathematical image, hosts and stage semantics:

1. A bounded one-time assembly/adoption operation checks the already retained
   complete build evidence and exact final payloads. It records the correspondence
   between source/build evidence, native host hashes and the actual adopted A*
   image ID. The image ID must not be replaced by the image file's SHA-256.
   This operation requires no compiler, guest execution or new cryptographic proof.
2. It emits a locally owner-adopted, immutable release manifest of relative paths,
   byte/hash identities and explicit runtime roles: producer sources, runtime and
   supervisor, stage host, snapshot host and guest image. Historical provenance
   remains retained and addressable in the release evidence, but is not reopened
   by each mathematical operation. An untrusted peer's self-asserted manifest is
   insufficient; the owner must select its exact identity or a separately trusted
   release-signing policy. Software release trust remains distinct from theorem
   verification.
3. A separate release loader resolves only ordinary paths inside the selected
   installation, verifies the bounded declared closure and roles, and instantiates
   the existing prepare/snapshot/request/stage behavior without invoking historical
   adoption. New sources and profile identity must themselves be selected. Do not
   monkey-patch the current producer, rewrite profile1242, or change a live
   installation. Existing session, allowance and checkpoint identity constraints
   remain unchanged; no automatic migration is implied.
4. Generic outer selections bind the compact execution closure plus their finite
   operation inputs. Preserve hard caps on count, serialized bytes and payload
   bytes, exact pin equality, source origins, final rebinding, fresh outputs and
   closure reporting. The current metadata suggests 54 support/source paths plus
   guest image and snapshot host, before new release metadata: approximately 56
   execution/source candidates, well below 256. This is a design estimate, not a
   completed DLL/import dependency inventory or an accepted installation manifest.

This is narrower than rewriting the scheduler, changing the proof relation,
introducing a new certificate format, rebuilding hosts or authorizing a larger
proof campaign. It addresses both the concrete cap contradiction and the public
deployment obstacle of depending on the research machine's historical paths.
Existing reusable release-map/installation mechanisms should be inspected and
reused before introducing another package framework.

## Consequential checks, not a new broad campaign

The successor's first review must establish exact required roles, source/import
closure, owner-adoption authority and continued receipt/journal/image binding.
Small inert controls should reject wrong/missing/duplicate pins, excessive maps,
path escape/alias, wrong image identity, changed source and finalization failure.
A source assertion or guarded file-access control should establish that ordinary
operation does not read the historical experiment tree. Do not delete history to
test that property. A single later fresh installation/constructor/snapshot boundary
can check the actual runtime closure, using an already selected workload only
after root authorizes it. Passing old proofs or grammar tests need not be repeated.

Root owns selection, funding, installation and adoption. This review preserves
profile1242 and live proof64938 unchanged. It authorizes no new runtime or product
edit and does not declare deployable v5 complete.
