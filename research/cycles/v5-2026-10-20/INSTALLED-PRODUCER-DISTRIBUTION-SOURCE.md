# Installed producer distribution successor: source checkpoint

2026-10-22; author `storage_launch_review`, under
[the root implementation selection](INSTALLED-PRODUCER-SELECTION.md).
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Source-only implementation; no imports, syntax/compile checks, tests, database,
host/proof calls, build, installation or Git operation was run. The existing
heavy proof was not inspected or interrupted.

## Exact source and preservation

Fresh physical source:
`software/v5/installed_production/body_location/distribution.py`.

- 71,246 bytes.
- SHA-256 `c831e08aeff64ec2c27bd71b784fc8d46822e68b9a9ea5193fbc1833ee58dfcb`.
- Baseline `software/v5/body_location/distribution.py` remains 54,824 bytes,
  SHA-256 `eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813`.

Before edits, an exclusive fresh copy was made and both hashes equaled the
baseline. All subsequent source edits used `apply_patch` at the absolute
canonical path. A read-only textual comparison after editing shows that the
ordinary `launch`/`_launch` block is unchanged: exactly 6,235 characters in each.
No current130 source or existing source/evidence was replaced. The current130
preservation of a future assembly still requires its actual named input-map
and installed-map audit; it is not proven by this one-file diff.

The [distribution contract](INSTALLED-PRODUCER-DISTRIBUTION-CONTRACT.md) is the
concrete design. This implementation consumes the separately authored shared
contract and parent launcher; those source hashes need joint selection before
runtime. The source above is not independently executable without them and the
selected full-release data.

## Implemented boundaries

### Build and release grammar

New exact input/release schemas are `DMKN_V5_DISTRIBUTION_INPUT_V4` and
`DMKN_V5_DIRECTORY_RELEASE_V4`. Each keeps its predecessor top-level fields
and adds required `production`; unknown or missing fields refuse.

Input production has exactly `artifacts` (three absolute pins) and
`profile_template` (one absolute pin). The three retained binaries have fixed
identities and destinations under `assets/producer/`. The template is copied
exactly to `production/PROFILE-TEMPLATE.json`. Descriptor bytes are generated
from the shared helper's closed `SOURCE_MODULES` and exact final SDK/file map,
not a directory scan or arbitrary source list supplied by the template.

The descriptor is generated as `production/ARTIFACTS.json`. Manifest production
contains exactly relative pins `descriptor` and `profile_template`. Both
metadata files are capped at 1 MiB and the two metadata/three binary namespaces
have exact file membership checks. The producer descriptor's aggregate execution
image is explicitly the selected A image, not the guest file hash. Existing six
consumer roles, ordinary consumer aggregate-image selection and individual-
relation preparation remain separate and unchanged.

The SDK limit changes from141 to144 at the two original assembly/validator
sites through one constant. Existing 128 profile-list, 20,000 file, 128-MiB
payload, 2-GiB map, 8-MiB release/input and source-size bounds remain. The new
producer core/entry roles additionally satisfy their1-MiB source bound.
Ordinary all-Python preparation projection remains: expected123, below128.
No128/64/256 limit is raised for this integration.

### One shared metadata contract, held executable bytes

`held_module` pins and reads exact bounded bytes, compiles those held bytes with
their selected file origin, rejects a preloaded private alias, and removes only
its own temporary alias after loading. It does not import a product package.
The helper is stdlib-only; its retained object owns its globals after removal.
This is trusted publisher/local bootstrap, not hostile-code isolation.

The builder calls the helper's pure
`validate_production_metadata(manifest, descriptor, template)` before creating
the destination. Full release verification pins/reads both metadata documents
and invokes the same validator; it additionally binds every core descriptor
role to the actual `sdk_sources` map and bounds all core/entry/launcher sources.
`verify_release` now returns `(helper, descriptor, template)` for producer
callers; existing callers ignore its return value. It still performs the old
complete directory census and all non-base hashing under `full=False`, and
all-file hashing under `full=True`. There is no partial-census shortcut.

The exact dependency order is sources/artifacts -> descriptor/template -> full
manifest -> externally adopted digest -> external absolute profile. Nothing
pins its containing manifest before that manifest exists. No historical build
evidence or research profile is installed.

### Public commands

```text
distribution.py producer-profile RELEASE_SHA REQUEST REQUEST_SHA
distribution.py producer RELEASE_SHA PLAN PLAN_SHA
```

Both require the exact installed isolated/no-site/no-bytecode Python, full V4
capability verification, and the explicit adopted release digest.

Profile REQUEST has exactly `schema` and `output_directory`, with schema
`DMKN_RELEASE_PRODUCER_PROFILE_REQUEST_V1`. The output directory must be fresh,
absolute, ordinary, and disjoint from the whole installation and input request.
The shared `materialize_profile(root, manifest_pin, descriptor_pin, template)`
generates the selected installed-lifecycle profile data. It is encoded using
the helper's canonical encoder, whose bytes also determine the profile ID.
No output filename/run name/time enters the profile. No owner, native host,
subprocess, receiver trust domain or funding state is created.

The profile parent checks original30-CPU/120-wall limits, rather than resetting
clocks after validation. These are explicit trusted-parent checks, not a Job
or hard preemption/sandbox claim. It rebinds request/full installation before
reporting, then verifies its final output census and profile/result/input pins.
CPU/wall measurements state their exact scope; pre-clock interpreter startup
and final report-write/rebind/stdout/commit cost are explicitly unmeasured, not
reported as zero. Later proof/service costs are not included.

Producer PLAN is the exact existing `DMKN_RELEASE_PRODUCER_LAUNCH_V1` grammar,
passed unchanged. The wrapper checks that its release tuple is the adopted
installation tuple, then held-loads only the fixed release-pinned
`sdk/v5/release_production/launch.py`. It transfers original `STARTED_NS` and
`STARTED_CPU`, and passes `[launcher_path, PLAN_PATH, PLAN_SHA]`. The dedicated
parent owns complete selection/lineage validation once. There is no generic
owner source, `runtime_mode`, consumer preparation, `client.boot` change or
new worker topology in this branch.

## Source-selection image-role correction

While deriving the actual future assembly input, its current130 source document
revealed that the consumer default `aggregate_image` is `99b9f1cf...`, not the
producer image `9d5072a6...`. The early distribution draft had incorrectly tied
these fields. Root selected the correction before any execution: restore the
predecessor nonzero/nonindividual validation for the ordinary manifest/input
field, preserve the actual old default in the input selector, and generate the
producer descriptor with the separate `PRODUCTION_IMAGE` constant. The shared
metadata helper already validates only descriptor/support against its producer
image constant and needs no change. No receiver trust default is migrated.

## Reviewer-found finalization repair

Independent reviewer `storage_outcome_audit` identified a concrete flaw in an
early draft: writing saved `PROFILE_CREATED`, followed by final checks and a
best-effort negative marker, could expose stale saved success if both the final
check and marker write failed. That source was never executed.

The current protocol writes `PROFILE-PENDING.json` before profile/result files.
Any error preserves pending; `PROFILE-FAILED.json` is an additional diagnostic
override, not the sole barrier. Success performs all result writes, exact
census/pin checks, stdout reporting and original deadline checks while pending
still exists. Removing the exact pending file is the final commit, after which
there is no further validation/reporting step in this function. An unlink
failure leaves pending and refuses completion. If the negative marker cannot
be saved, pending still blocks acceptance of a saved success.

A profile RESULT is accepted only if both pending and failed markers are absent.
Its saved `completion_rule` and shipped README state that condition. Process
termination before commit does not manufacture success. As elsewhere, stable
trusted-owner filesystem assumptions remain; arbitrary external deletion of
guards is not an adversarial-OS security claim.

The public plan supplies a profile pin/configuration, not a claimed successful
profile-creation RESULT. Validating those mathematical producer parameters does
not adopt the onboarding operation's completion claim or grant an allowance.
Any consumer claiming successful onboarding must inspect its RESULT with the
pending/failure rule. No new profile-result authority, path-name inference or
extra selection schema was invented merely to reuse valid configuration bytes.

## Required review and later evidence

The independent reviewer is examining the full shared implementation. This
checkpoint records authored source, not a source-review pass or runtime result.
Potential later controls are limited to the changed boundaries: exact V4
fields/roles/count refusal, metadata map mismatch, profile identity stability,
whole-installation overlap, original clocks, genuine plan dispatch and pending
finalization precedence. Source/map review comes first. No repeated binary build,
proof campaign or predecessor test is warranted by this change.

Before installation, root must choose one exact144-row map and actual template,
bind final helper/launcher/source hashes, verify the predicted123/31/49/60 counts,
and obtain the independent review. The full assembly and actual public-action
gate require separately selected finite execution. This is progress toward v5,
not a completed release or a claim about worldwide availability/useful growth.
