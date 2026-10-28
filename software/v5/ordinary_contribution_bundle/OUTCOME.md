# Independent saved pack and control outcome

2026-10-28, query_scaling. **PASS_SELECTED_KIT_AND_INERT_PROJECTION_CONTROLS**.
Both selected operations completed once with their reported outputs, exit 0 and
observed clean closure. This audit read saved source, selections, archive,
extraction, reports and evidence bytes; it ran no projector, control, product
codec, owner, host, database, native operation or network request.

The scope is the contribution/completion file handoff described in
[`EXECUTION.md`](EXECUTION.md), not mathematical acceptance, dependency closure,
host publication, public deployment or full v5 acceptance. Root owns adoption.

## Actual kit

Run: `experiments/v5-local-checks/contribution-kit-pack01`.
The actual source selection is
`8859a47808e3967e8a79973379c579d36c6a5cbeec438d16a325757dcba47dac`.
The archive and extraction contain exactly its 268 payloads plus
`KIT-MANIFEST.json`: 269 files/entries. Every archive entry and extracted payload
matches its selected length and SHA-256. Manifest records match the selection;
file and directory censuses have no additions or omissions. ZIP inspection was
read-only and did not extract or execute another copy.

The 160 package payloads match the unchanged incumbent selection, PROFILE
`e8d33500db4c0a5ce89b2dfb51c3e1f9ec8f12063bbc58fe5e4eb23c2b6dfb13`,
installation
`9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27`.
As established in REVIEW's exact selection comparison, the only kit changes are
two additions (`contribution/project.py`, `CONTRIBUTION.md`) and GUIDE replacement;
265 incumbent records, including utility/map/build/source roles, are unchanged.
The extracted projector is the reviewed repaired `4ca7fe20` candidate. License
status remains `UNDECIDED_LOCAL_ONLY`.

| Saved artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `packed/commons-local.zip` | 43,116,243 | `856935e7f4bd180030bb5fb8b95e714cd8aa32d6f919410ee08c3be1b9284d05` |
| `packed/commons/KIT-MANIFEST.json` | 38,725 | `07410919be2cf14b50adcad5739c0453e2863ec70fa7393111cfb90ac7aa7050` |
| `packed/RECEIPT.json` | 743 | `4b0bf3889863af36cbfa4bf91b8af509c347afd57bfe352dfd56fe805aecf64f` |

The receipt's selected hash, counts and actual byte pins agree with the files.
Its `PACKED_AND_RELOCATED_LOCAL_KIT`/`VERIFIED_LOCAL_KIT_BYTES` claims are supported
within that file scope.

## Actual focused controls

Run: `experiments/v5-local-checks/contribution-bundle-controls01`.
Its selected source is `control_tests.py`
`d50d49a359d33244794b89e12ab50a052148836216894ff4ea0143a2b04e67df`;
plan `bf7170fa015c8ecad18be6762687bc372045be24ae0a68124b98af025e3d7df1`.
The invocation selects the actual pack01 extracted `commons/package` and
`commons/contribution/project.py`, not a fabricated PROFILE or a development
substitute. All four source snapshots in each operation match its selection.

The saved control result and stdout agree: `passed:true`, eight completed groups.
The source was inspected to bind those claims to the checks performed:

| Group | Observed result |
| --- | --- |
| Real contribution wrapper | All 21 units, 379,701 evidence bytes, 11 targets and 10 support-only units retained. |
| Real completion helper result | All three units, 10,700 bytes and one target retained; the two support units precede the consumer. |
| Untrusted provenance and paths | `ok:false`, a different historical profile and malicious `../../` file fields succeed only through the explicit relocated evidence; receipt preserves provenance and denies acceptance/closure. |
| Selected input pins | Wrong report/profile hashes refuse with `PROJECTION_REPORT_PIN` and `PROJECTION_PROFILE_PIN`. |
| Binding, layout and bounds | Eleven cases refuse at evidence hash, target identity/membership, status, duplicate unit/target, 33-unit/target count, per-unit/aggregate byte or semantic checks. |
| Missing evidence | `FileNotFoundError` for the selected local filename; no historical fallback. |
| Malformed evidence | Corrected raw length/hash reaches the actual codec, which refuses `PORTABLE_EVIDENCE_SCHEMA`. |
| Approval and output boundaries | Both missing approvals, overlap and existing output refuse; the existing directory stays empty. |

The first group calls the extracted projector's public `main()` with its actual
path and CLI arguments inside the isolated `-I -S -B` control worker. It is not
a separately launched projector child and does not exercise the script's outer
`__main__` exception wrapper. The remaining groups use its callable API.

Direct saved-file comparison confirms exact original-to-output bytes, manifest
unit order, target rows, receipt pins and exact output census for all three
successful projections. Original helper/wrapper hashes match the selected real
fixtures; original evidence is still pinned. All 18 expected fresh refusal
outputs are absent, and the separately existing output remains empty. The
wrong-unit membership fixture really lacks the requested name despite its
recomputed ExportID. The malformed schema has a matching raw byte pin, and the
aggregate fixture declares 4,201,434 bytes against the 4,194,304-byte ceiling.

The harness rereads successful outputs through the unchanged bundle parser and
batch validator. Its guarded projector calls restrict reads to selected files
and output, refuse input enumeration and specified database/process/network
effects, and check temporary module-slot restoration. This is instrumentation,
not a general security sandbox. Zero owner/native/database/network fields are
harness declarations supported by the reviewed call graph and these guards,
not independent system-wide telemetry. No host compatibility execution occurred;
the tested seam is the existing manifest/batch format and append-config fields.

Saved `checks/RESULT.json` SHA-256:
`d28e5f761b901579dce783842a2506e913442081ba470bd314292ea40ceb6ca2`.

## Closure, cost and disposition

Both outer results report `COMMAND_EXITED_ZERO_AND_CLOSED`, direct child reaped,
Job closed, zero active processes, no cleanup errors, no termination request and
empty stderr. These recorded closure observations support the result; no new
process was launched to repeat them.

| Operation | Job CPU seconds | Outer wrapper CPU seconds | Known total CPU seconds | Outer wall seconds |
| --- | ---: | ---: | ---: | ---: |
| Pack01 | 1.984375 | 0.140625 | 2.125 | 6.455525 |
| Controls01 | 1.453125 | 0.09375 | 1.546875 | 2.483058 |
| Combined | 3.4375 | 0.234375 | **3.671875** | 8.938583 |

The inner supervision CPU is contained in the outer wrapper figure and is not
added twice. Peak reported Job private commit was 147,836,928 bytes for pack and
28,532,736 bytes for controls, within their selected 512 MiB allowances. The
90-wall/45-CPU pack and 150-wall/75-CPU control selections were not renewed.

Outer pack RESULT hash:
`157784a595006087b798b4e9160302483aa63a03f1eb227c3e5fc86964451004`;
outer controls RESULT hash:
`c6995244ba69baaa0b441f58ec61eccde70502f99d3e5e226330e33ebde720df`.
Their selection hashes are respectively
`8569aba1e4767433ffffec691b22cf65ebfce6c6fa5ccb46e836d10f57b90a24` and
`481fa700487dd192c23f4e9e33ba69f529898c4cb24a9224538d8195451fb407`.

The selected file-only companion and coherent kit are supported for adoption at
this boundary. Native/host-service campaigns were not repeated. No claim follows
about authoring costs, missing-import availability, mathematical truth, broad
scale or useful-growth speedup. All used source, fixture and evidence bytes stay
frozen; this outcome selects no further run.
