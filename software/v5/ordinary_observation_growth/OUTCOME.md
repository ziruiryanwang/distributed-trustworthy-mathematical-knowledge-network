# Observation theory: actual producer, intake and publication

2026-10-28. **PASS for the three completed local operations.** Independent
saved-artifact audit by fresh_recipient_plan records their distinct claims. No operation was
rerun, no owner/catalog/custody/index state was opened, and no Git action was
performed. All paths below are relative to `experiments/v5-local-checks` unless
otherwise stated. Source-flow review remains in REVIEW.md.

## Inert production: PASS

The saved `observation-growth-produce-launch01` run exited zero with
`PRODUCED_INERT_BASELINE_NOT_ACCEPTED`, `mathematical_acceptance:false`, matching
PROFILE `efa1e0894a24859bf1c7648ccaf72674c7cf136c9fce32a62020e75cb24bcd45`
and receiver `86b6fcce8d8f13479e8131e1a386782b7bda5b6ee579df46e640ca8005affbea`.
The complete output wrapper is 3173 bytes, SHA-256
`06e3eba09f5b92b687c0ca57d342793a0451a0a34ca19c8b9f6acd4f70343283`.
This phase did not admit mathematics into B.

Independently verified every preparation receipt file/input pin, every production
inventory/project/request/writer pin, the 8436-byte manifest
`d31ee8536962cff8c60c856f107594610d7b82f851c518ec37a838885f3bb4b6`,
and all 47 unique unit files against its exact size/hash rows: **695269 bytes,
one batch**. Reported census is 68 names, 437 edges and 17114 nodes. Actual
returned names match prepared names in order: `ResetEffects.fill` and
`ResetEffects.contextual_iff`. Reported final spool is 58 files / 2207935 bytes,
against the 144 MiB reservation. Native stderr contains phase observations,
including its 112709-record loaded-source census, not a failure diagnostic.

Public and inner native supervisors both report child reaped, Job closed, zero
final active/terminated processes, no requested termination and no cleanup errors.
Outer limits were 90 wall seconds / 45 CPU seconds / 1280 MiB / 6 processes.
Actual outer wall was **8.9163904 seconds**; child Job CPU **4.28125 seconds**
plus separate trusted-wrapper CPU **0.140625 seconds** gives **4.421875 known
CPU seconds**. Inner native 2.09375 CPU seconds are already contained in the
outer Job measurement and are not added again. Peak Job private commit was
964800512 bytes; stdout/stderr were 3173/0 bytes.

Evidence pins: preparation RECEIPT
`63ad3a8fb8b06aba56af67fc29940e4af1f23ce093f34eb70c78cf2a05542570`;
RUN `554af6789077b8d9f4a66a2e49c189982d49f2cf1016e51f752b5188ca15e068`;
SUPERVISION `37fd8973fc64b53614b46eb62745a3cf3c2d58b6ff96fe77afc1bc253e48967b`.

## Checked intake: PASS

`observation-growth-intake-launch01` returned `BASELINE_INTAKE_COMPLETE` for
the exact producer manifest. Its one batch is `CHECKED`: **39 new units checked,
8 existing units reused**, one native launch. The selected parent remains
`6e5fbf1f8418ac78173197096520f786c943766415bfd3fa8236894559fa9a2d`;
the resulting B root is
`1b8761f807bba6c5ebe628636621a556e4271b955cc6cd3e836b9a5c5bc728ee`.
The actual 60-second native reservation fits the selected 90-second invocation
CPU ceiling. It is reservation accounting, not measured CPU consumption.

Independently verified all intake receipt files/input pins, the exact B
parent-report binding, producer-wrapper/manifest identity, catalog/custody/store
selection, unchanged PROFILE/receiver and the 47-unit/695269-byte census.
The complete 2783-byte intake wrapper is SHA-256
`3293c38f03865c134f38df6c9b83531aa2d94dda4d37a98791eee4e65e5f7bc5`;
RECEIPT `4229f9f49f33ec56cf63e7d079a0f22cc694ee6ba2af6d5f2f6dac18af65e677`;
RUN `1e3dd183f0c46ab9326aa53ee0b726e11f2bc5b4d977f5bf97aae8a4a0109fdf`;
SUPERVISION `4a8b9a9f8a0f7ef41d06a7e21ffe5c6b16f8c888b76c97f96310b1e270af9d93`.
This is local mathematical checking and exact reuse; the report explicitly
does not claim an ordinary-library registration or peer-transferable warrant.

## Local publication: PASS

`observation-growth-publish-launch01` returned `INDEXED_LOCAL_TARGETS` and both
records have `new:true` in the existing `refinement-recipient-index01`.
The prepared config has `create:false`, the reviewed existing index limits,
and exactly the producer's two name/export/unit tuples. Each actual publication
record matches its tuple and semantic ID, and publication's `local_context`
equals the complete intake root above. This operation adds index records; its
`mathematical_acceptance:false` does not undo the preceding intake acceptance.

| Interface | Exact export ID |
|---|---|
| `ResetEffects.fill` | `9c99432c3c567d7ca63d40e9e2a76e11df45d985218361a63a15cc565bd58c9c` |
| `ResetEffects.contextual_iff` | `b093eb970b89de31662abccdb05552270225e26b93e4f0dc47a6463b1590f8be` |

Final reported snapshot is
`94773cdf3acc709dc6ea7bad24785541c57479f1c2e277f526523869d499d4c8`.
Reported evidence read is **33034 bytes**, independently equal to the two
already verified target unit files' 6384 + 26650 bytes. All publication receipt
files/input pins match, including actual producer/intake wrappers; saved RESULT
and complete stdout parse to identical reports. Complete 5273-byte stdout SHA
is `869500e942fe18627b758fded6b6eeb66f52cbb045a8f34e8d7396f3aa664a32`;
RECEIPT `a2066fa3145c143bd1c9155410e4ddcbf46210f718656995c3aefa29a9c3e050`;
RUN `28165c9282480e279fc60fd892bc7b1360c9444b1e21e0209992235f7ba3f881`;
SUPERVISION `6da1175253178da3bc4176e91a13a90fd8d0591b15491e5d872548cd42fbdd74`;
publication RESULT
`dffa20cb1c613b0a5585508a75126c363a2b8edf78c7338f336c96b1e2daad85`.

Independent math_argument decoding of only the two saved inert target units
confirms their canonical, domain-separated UnitID hashes. The exported `fill`
type is `{A : Type u} -> Context (Plan A) -> Plan A -> Plan A`. The
`contextual_iff` type binds `p q : Plan A` and states contextual refinement iff
refinement of their summaries, retaining the atomic-law premise and both
observation witnesses. Both bind `Plan` to the identical portable symbol
`dd71ac44349aa741c617ddd920ebe9f899bf36c8b929cfa4f621fdfde2ee02ca`.
Thus `Context -> fill -> Plan -> contextual_iff` is an actual path through
shared type symbols, not a direct dependency chain or an executed discovery
result. `contextual_iff` does not directly import `fill`; its proof does import
`Context.hole`, `guarantee_iff` and `contextual_of_summary`.

## Closure and operation costs

All three public operations exited zero, reaped the child and closed its Job,
with zero final active/terminated processes, no termination request and no
cleanup errors. Selected intake ceilings were 150 wall / 90 CPU seconds,
1536 MiB, 6 processes; publication ceilings were 60 wall / 30 CPU seconds,
768 MiB, 3 processes. Intake/publication peak Job private commit was
690204672/36651008 bytes; stdout/stderr were 2783/0 and 5273/0 bytes.

| Operation | Wall seconds through report | Child Job CPU | Separate wrapper CPU | Known CPU total |
|---|---:|---:|---:|---:|
| Produce | 8.9163904 | 4.28125 | 0.140625 | 4.421875 |
| Intake | 8.9490213 | 8.21875 | 0.1875 | 8.40625 |
| Publish | 1.5833133 | 1.359375 | 0.140625 | 1.5 |
| Total | **19.448725** | **13.859375** | **0.46875** | **14.328125** |

Nested native and controller observations are not added again. The wrapper's
CPU is separately measured/cooperatively bounded; child-tree Job supervision
does not establish hard containment of the wrapper. Totals exclude kit
preparation, copying, prior proof checks, prior grounding and research effort.

## Claim boundary

The actual path establishes inert export, B checking/reuse and local publication
of the two interfaces. No new query, external service or downstream discovery
was run. It does not establish discovery speedup, autonomous theory selection,
independent-host availability or completed v5. The failed original proof check
remains preserved and charged; source/review effort is outside the operation
CPU totals above.
