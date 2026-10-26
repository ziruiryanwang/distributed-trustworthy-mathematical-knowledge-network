# Coherent commons source handoff: independent actual outcome

## Decision

**PASS for the selected source-consolidation gate.** One pack and one relocated
public verifier completed all six groups and 15 intended refusals with clean
outer closure. The actual archive contains the exact 169-row predecessor
projection and 17 additions, with one current root guide and manifest. No product,
mirror, native checker, owner state or network service was run in this gate.

Run root: `experiments/v5-local-checks/commons-source-controls01`.
Source/selection review: `REVIEW.md`, SHA-256
`ab832e63290f9cfe17464373f656b6d64bd9b5e6a6bbd877d8a6da043077adaf`.
This audit used saved reports, file hashes and inert .NET ZIP-member reads only.
It neither reran the verifier/test nor imported archive/product code.

## Exact handoff

The actual artifact is `suite/packed/source.zip`; terminal external receipt is
`suite/packed/RECEIPT.json`. The successfully verified extraction is
`suite/relocated`. These remain local, unpublished, source-only artifacts.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| source.zip | 4577899 | 079383e415eb84e3edec1f96f74d29be956ef6f1fd166ef128224c13108298b2 |
| COMMONS-SOURCE-MANIFEST.json | 28018 | f5134135204f980b90df449a3a9a07bfed61fd9ff6b9fd5b5dde305b00cd2861 |

There are 186 manifest payload rows totaling 4,517,567 bytes, plus the current
manifest: 187 archive/extracted files and 47 extracted directories, hence 234
entries within the unchanged 256-entry bound. The archive itself is under the
16-MiB bound; no source/manifest limit was widened.

Independently rehashed all 21 source inputs at both current and snapshot paths,
all 173 external pins (170 complete predecessor files and three Python files),
every actual relocated file, and every actual ZIP member. No mismatch was found.
All 187 ZIP member identities/lengths agree with the 187-file extraction; path
sets are identical. ZIP member stored/compressed lengths and fixed 1980 timestamp
agree. The reviewed harness additionally checked the full fixed ZIP metadata,
sorted census, no directory/duplicate members and no extra/comment data.

The original 169 rows match the current manifest exactly after only
`README.md` -> `HISTORICAL-INVESTIGATOR-README.md`. The retained old manifest is
the exact 25,231-byte file with SHA-256
`65edf28f928d4100346a4603fe508252ddc6393950c34a373fbb33da4c6491f5`.
Its historical README association was not rewritten. The new root guide and
current manifest explicitly describe the projection instead. The 16 new mapped
source files plus that old manifest are the 17 additions, without copying tests,
state, runtimes or experiment reports into the archive.

## Actual six-group result

| Group | Saved evidence and independent reconciliation |
|---|---|
| One pack/full readback | Terminal `PACKED_COMMONS_SOURCE_NOT_BUILT` receipt; archive hash, all member bytes, independent predecessor projection and exact counts agree. |
| Relocated public verifier | Its own approved utility ran with `-I -S -B`, actual new manifest digest and relocated source root; returned `VERIFIED_EXACT_COMMONS_SOURCE_NOT_BUILT`, matching manifest/payload totals and empty stderr. |
| Current guides/mirror association | Seven current entrypoint guides, 37 local links, 27 exact mirror dependencies; actual destinations and original/current dependency pins reconcile. |
| Manifest/association refusals | Eight saved cases reject missing addition, changed old row, wrong projection, wrong old-manifest association, changed fixed mirror, wrong selector, case alias and fabricated predecessor bytes. |
| Actual malformed-root/refusal controls | Four separate retained roots reject changed old manifest, changed old payload, missing payload and extra payload; wrong current digest, existing pack output and old whole-root census also refuse. |
| Final immutability | Original extraction, selected additional sources, valid relocated extraction and archive retain their selected bytes; failures remain separate. |

The actual refusal list has exactly 15 entries and each expected source error.
Independently inspected the four retained malformed-root distinctions: changed
prior manifest is 25,232 rather than 25,231 bytes, changed START-HERE is 17,493
rather than 17,492 bytes, missing mirror payload remains absent, and the extra
fixture file is present. They were not patched into a pass or deleted afterward.

The mirror dependency map still pins the original investigator manifest and all
27 original source/data rows, not the newly installed acquisition implementation.
Their preserved paths and bytes match both old and current manifests. This is a
static loader association, not a rerun of mirror preparation or serving.

Every saved local guide target resolves to an actual file inside the extraction.
Fragment anchors and external website validity were not independently tested.
Current package/selector pairing and old-report restrictions remain as described
in the source review. The old exact-census primitive correctly rejected the new
root; no old verifier was weakened or advertised as the new root verifier.

## Operational closure and cost

The outer result is `COMMAND_EXITED_ZERO_AND_CLOSED`, exit zero, direct child
reaped, Job closed, zero final active/terminated processes, no termination
request and no cleanup errors. Both outer stderr and verifier stderr are empty.
The reviewed subprocess control required the sole verifier child to exit zero
before recording its successful result. No incomplete ready marker is used.

| Measurement | Actual |
|---|---:|
| Full selected operation wall | 7.7555915 s |
| Supervised command through cleanup | 7.2714201 s |
| Inclusive outer Job CPU | 2.9375 s |
| Outer runner CPU | 0.3125 s |
| Known total CPU | 3.25 s |
| Peak Job private commit | 44,961,792 bytes |
| Outer stdout / stderr | 7,250 / 0 bytes |

The harness's 6.7974507 wall seconds and 2.15625 CPU seconds are nested, not added
to those totals. Its CPU excludes the verifier child; the inclusive outer Job
already includes that child. The supervisor's displayed 0.03125 seconds is part
of outer runner CPU. Raw cumulative process count 3 is not the two-active-process
cap; no process-identity explanation is inferred from that counter.

The original 130-wall/70-inclusive-CPU/768-MiB/two-active-process envelope and
2-MiB stdout/1-MiB stderr caps remained unchanged. Per-call/harness cooperative
limits did not renew it. The verifier's small saved file logs were not separately
hard-disk capped, as disclosed. Exact runtime pins are not a hermetic toolchain
or hostile-source sandbox claim.

## Evidence pins

| File under run root | SHA-256 |
|---|---|
| selection.json | 1e4b122c27908180d3b88c9856578c329484b35e196bdea16c9f46dab25c6ec0 |
| RESULT.json | 73ee5f891a22614bb6cb19b017490526909d1311c641a5a57391ddf2176cfa17 |
| suite/RESULT.json | a1efc2eb13cefdedc6ed3527f109ba50c4bf4c54bd498de33a8f32ad2e84c732 |
| suite/packed/RECEIPT.json | a7017d9f9f5a1da83350f35d4623e874d89365ba51280f7ce33faf9ddb2b30bf |
| suite/verify-stdout.json | 65b5a14f6230e55c0bb02f6a945a16d15426506e564685c612d5193e7577b545 |
| suite/VERIFY-COMMAND.json | db9e6bb8253042ee483de9e166f38d4fd913f734fdcbc21eb279fb4603c12bf5 |

## Disposition

Root may adopt this one coherent exact source handoff and stop consolidation.
Recipients no longer need separately gathered mirror/multi-source sidecars or
to guess the current selector. Mathematical investigators still need separately
approved external runtimes, the existing selected build route, real data/contacts
and normal independent checking. Storage-only operators need approved Python,
selected inert data and separately authorized finite operations, not Lean.

The archive does not grant a license or publication permission. It does not prove
compilation on another machine, public deployment, native acceptance, independent
hosting, useful-growth advantage or final-v5 completion. Existing adopted results
retain their original scope. Full v5 remains active; the next work should address
a distinct central user obstruction, not repeat this passed consolidation gate.
