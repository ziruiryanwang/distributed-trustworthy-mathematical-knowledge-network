# Independent contribution projector source review

2026-10-28, query_scaling. Disposition: **PASS_SOURCE_SELECTED_OFFLINE_PROJECTION**.
No unresolved source blocker remains in the candidate pinned below. This is a
source/file review, not execution evidence, mathematical acceptance, host
publication, a packaged-kit pass or full v5 acceptance. Root owns runtime
selection, integration and adoption.

## Reviewed bytes

| File | SHA-256 |
| --- | --- |
| `project.py` (19,689 bytes) | `4ca7fe20e85b75e07ef72e74dc761e7ace4aaff7a93bb444444b57e5ed401ac5` |
| `CONTRACT.md` | `f7b680266b4180b18e0cf14987d0f80aa753292b19d680489656d4ff4f6b0d85` |
| `GUIDE.md` | `485f914308acffaa89b50aa148d41bf33f4baec7e942f77915fbc2a38bed8d30` |
| `KIT-SOURCE.md` | `cec9e4c673c498ac4522f2aa581563c8f2f2ce895370b941da0bfc74dae1e630` |

The selection and the earlier
[`CONTRIBUTION-HANDOFF-CHALLENGE.md`](../ordinary_incremental_host/CONTRIBUTION-HANDOFF-CHALLENGE.md)
define the reviewed boundary. The challenge is already adopted; this review
checks the implementation rather than repeating the architectural decision.

## Binding and bounded work

`project_selected` requires explicit caller-selected package/profile and report
hashes, evidence directory, fresh output, and both disclosure flags before output
creation. It recognizes the exact helper result statuses and explicit outer
`contribute`/`complete` layouts. An outer operation must agree with its result
kind. Outer `ok`, cleanup failures and historical profile are provenance; no
success, ADMISSION or original-closure gate was reintroduced. A historical profile
can differ from the chosen codec package. Required provenance identifiers remain
bounded identifiers, not execution authority.

Every `result.units` row is visited in supplied order, including rows containing
no selected target. Validated hex UnitIDs alone derive local evidence filenames.
The report's `file` field is checked as text but never followed; previews,
catalogs, custody and source locations do not become inputs. The code checks raw
length and SHA-256, parses the portable envelope, checks its UnitID and selected
semantic identity, and refuses duplicate unit IDs. Each target must name an
actual output in its named supplied unit and have the derived ExportID; duplicate
target names and ExportIDs refuse. It does not slice declaration groups or
reserialize evidence.

The selected 1..32 units, 4 MiB aggregate evidence and 1..32 targets match the
public contribution/completion return bounds. Node/name/import ceilings match
the producer preflight limits. Metadata is bounded to 2 MiB, has bounded depth
and numeric tokens, and rejects duplicate JSON keys and nonfinite numbers.
Existing `baseline_bundle.split_units`, `make_manifest`, `read_manifest` and
`validate_batch` enforce the existing format and structural bounds. The flattened
manifest order must equal the supplied unit order. No dependency environment is
invented or checked: missing older imports remain a receiver/availability matter.

This agrees with `ordinary_contribution.py:238-264,627-639` and
`completion_api.py:93-159`: all bound units are public output, while targets are
only selected outputs. Completion's supplemental support units retain their place
before original consumers. The projector does not decide global novelty or
whether the host already holds a unit.

## Pure loader and resolved source finding

The five codec files were read and hashed directly in the current package:
`experiments/v5-local-checks/incremental-host-assembly01/distribution/package`.
Its PROFILE SHA-256 is
`e8d33500db4c0a5ce89b2dfb51c3e1f9ec8f12063bbc58fe5e4eb23c2b6dfb13`.

| Package-relative codec | Bytes | SHA-256 |
| --- | ---: | --- |
| `installation/py/ordinary_evidence.py` | 17,058 | `fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6` |
| `installation/py/ordinary_semantics.py` | 10,283 | `ee601536f53640a2695e51d37d3e87e6746604ed6433cb3ace9349ae1aedf915` |
| `installation/py/portable_evidence.py` | 2,993 | `f8ea819bdd9344d696cef2725888828125b2ef5d1b60d2c31a0412657a62cbd8` |
| `authoring/py/portable_candidate.py` | 10,437 | `29ae111a362472b09b2b1ff16b567b352be793d76c2cd1b5421e0aee29219331` |
| `reference/baseline_bundle.py` | 21,363 | `e4b52c2f2e823cc98aa37c8cc7adb0cf79952def9c19b54d7072116a39fa19b6` |

All actual files match the candidate's fixed length/hash pins. The loader captures
all five exact sources before executing any of them and restores their previous
module slots in `finally`. Their imports close over these modules and the Python
standard library; no owner/native/database/network module is loaded. The CLI
requires isolated Windows Python without site imports or bytecode writes. Callable
users must serialize mutation/import-slot access as documented.

Review found one blocker in the unused initial candidate
`43f98bfddc070a28b61604ee9e1a543f84c19fa39f0c5c8e248f68a1bd9da568`:
it required all five roles in `PROFILE.files`. The current PROFILE directly lists
only the authoring/reference roles; installation is represented by
`installation_manifest_sha256`, whose value is
`9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27`.
The old code would always refuse `PROFILE_CODEC_PIN:ordinary_evidence` with the
selected package. The author repaired the unused source: direct PROFILE row checks
apply to its two listed roles, while every codec still requires its fixed captured
byte pin. The revised branch and actual package records were inspected. No failed
runtime was created, and no full installation/native loader was added.

## Output, failure and host boundary

Ordinary local path checks reject links/reparse points, file hardlinks, unsafe
components and overlapping output. Existing input ancestry is inspected without
enumerating the evidence directory. Output must have an existing parent and a
fresh path. Source/input concurrency is caller-controlled; this is not a hostile
concurrent-filesystem guarantee.

Exact evidence bytes, existing manifest, append config and preparation receipt
are written with exclusive creation, flush/fsync and readback. Saved manifest
and batches are checked again. Selected report/profile bytes are rechecked before
and after output. Any partial output remains on failure; even a late failure may
leave a manifest/config/receipt. No rollback, deletion or automatic retry occurs.
The single wall/CPU allowance is cooperative, as disclosed, not OS containment.

The generated append fields exactly match unchanged
`ordinary_incremental_host/custodian.py:363-388`: existing append schema, bundle
directory, manifest path/hash, targets, both explicit disclosures and optional
lowered bundle limits. The 32-target projection ceiling fits the existing host's
64-target call ceiling. Host root and stable descriptor approval remain separate.
The helper opens no host. Its receipt explicitly denies mathematical acceptance,
dependency checking, host publication, full-package authentication, native
validation and original-closure verification.

The contract explains whole-unit sharing, unindexed declarations, permitted
partial publication, separate missing-import retention, and path re-pinning after
relocation. These are operational requirements, not assertions that the report
proved acceptance or that preparation has published anything.

## Kit integration conclusion and remaining evidence

Reusing incumbent `ordinary_incremental_host/kit/kit.py` unchanged is supported.
Its SHA-256 is
`8ae7b24e354daa45efb8a0ae918fc519c81677c7f87cd8a2666151db377d5ad8`.
`files_checked` already accepts 250..384 explicitly selected payloads, validates
every path/length/hash, requires exactly 160 package payloads and binds the current
PROFILE/source-map/builder/helper pins. A utility change or package assembly is
unnecessary.

The GUIDE comparison found only the companion table row and the paragraph
directing returned contribution/completion evidence to the offline projector.
It retains receiver checking and missing-import obligations. The intended kit
delta is two new payloads, `contribution/project.py` and `CONTRIBUTION.md` (the
reviewed contract), plus GUIDE replacement: 268 payloads with all remaining
incumbent pins unchanged. No final 268-file selection or packed archive is
qualified by this review; root must check that exact delta when selecting it.

No projector, codec, control, host, native or network execution was performed by
this review. Focused controls and any selected relocated invocation must use the
actual package PROFILE and cover the changed file boundary. Existing successful
host-service and native campaigns need not be repeated. Source approval does not
authorize a run or establish its outcome.

## Exact kit selection follow-up

Disposition: **PASS_SOURCE_INTEGRATION_SELECTION_268**. The later supplied
`SELECTED-FILES.json`, SHA-256
`8859a47808e3967e8a79973379c579d36c6a5cbeec438d16a325757dcba47dac`,
resolves the selection check left pending above. Compared field by field with
incumbent selection
`a1c7402e71d9f399a374215454cd31a51d5790c4fae0b578449be9116ab1ee1e`,
it has 268 entries: precisely two additions, `CONTRIBUTION.md` and
`contribution/project.py`, one replacement, `GUIDE.md`, and no removal. All 265
other origin/path/length/hash records are unchanged, including all 160 package
entries, the prior kit utility, helper, source map, source closure, build recipe
and existing companions. JSON property ordering changed without altering those
record values.

The two additions select the reviewed `CONTRACT.md` and repaired `project.py`;
GUIDE selects the reviewed successor. Direct length/SHA checks of all three
actual changed source files match their selected records. Every selection record
has exactly origin/path/bytes/sha256 fields. This closes the source integration
check without a new utility or package change. It does not qualify a packed
archive, extraction or relocated execution; their actual outcomes remain separate.
