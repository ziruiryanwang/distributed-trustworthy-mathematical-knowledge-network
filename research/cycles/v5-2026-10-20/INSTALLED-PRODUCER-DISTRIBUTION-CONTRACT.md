# Installed producer: minimal full-distribution contract

2026-10-22. Source/design review only, coordinated with `integration_adapter`.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
No product import, test, constructor, native host, proof, installation or Git
operation was performed. This note does not select execution or adopt a release.

## Decision

Extend the existing full distribution, not the small producer-component fixture.
Use explicit `DMKN_V5_DISTRIBUTION_INPUT_V4` and
`DMKN_V5_DIRECTORY_RELEASE_V4` schemas with one new `production` field. Keep
every current130 SDK row byte-identical, the six consumer artifact roles, the
individual preparation relation and the ordinary client launcher unchanged.
Add the producer source/artifact closure and a dedicated finite launcher.

The physical successor is selected separately under
`software/v5/installed_production`; logical installed paths remain `sdk/v5/...`.
The used `body_location/distribution.py` and component producer stay frozen.
The new public producer adoption explicitly requires the V4 full container;
it does not broaden the old V3 validator or turn the old component fixture into
a full distribution. Source ownership and runtime selection remain root's.

Basis: current `software/v5/body_location/distribution.py`, SHA-256
`eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813`,
especially build/manifest/verification/launch; the existing release adoption;
the separately adopted [source compatibility audit](RELEASE-PRODUCER-SOURCE-COMPATIBILITY.md)
and [public-launch design](RELEASE-PRODUCER-PUBLIC-LAUNCH.md). This note does not
repeat the verifier compatibility audit or define the launch-evidence grammar.

## Exact build input extension

V4 has exactly these top-level fields:

```text
schema, base_role, base_root, base_manifest, sdk_sources,
preparation_template, assets, aggregate_image, lean_runtime,
lean_support, distribution_source, production
```

The first twelve fields retain their existing meanings, apart from the explicit
schema and SDK-count change below. `production` is required, not nullable, with
exact fields:

```text
production = {
  artifacts: {
    stage_host: AbsolutePin,
    snapshot_host: AbsolutePin,
    guest_image: AbsolutePin
  },
  profile_template: AbsolutePin
}
AbsolutePin = {path: canonical absolute ordinary file, bytes: integer, sha256: digest}
```

This first producer distribution is one concrete capability, not a framework
of optional arbitrary artifact roles. A consumer-only old release keeps its
old V3 builder and manifest; it is not rewritten or migrated.

The new input still fits the existing 8 MiB document cap. The relative producer
template must be at most 1 MiB. Reject duplicate JSON fields, unknown fields,
invalid pins, aliases/reparse paths and overlaps using the existing helpers.
Read and verify each absolute input pin before assembly and copy pinned bytes
with the existing exact-copy primitive. The destination must be fresh and
disjoint from every selected input and the whole source/base installations.

The builder copies the template bytes exactly; it generates the descriptor
from the selected final source map and the three selected artifact pins. It
must not accept a caller's unvalidated descriptor or copy a research profile
with absolute historical paths into the product.

## Fixed artifact and metadata locations

| Role | Installed relative path | Exact retained artifact identity |
|---|---|---|
| Stage host | `assets/producer/stage_host.exe` | 68,039,168 bytes; `263841ae256af217de2c00452c7f0688a2e9e58e6aa6d95457d5118aef04ff3c` |
| Snapshot host | `assets/producer/snapshot_host.exe` | 6,630,400 bytes; `a9438205bbb091623f12bd10a7e9a0a2b437c873003fec3cb000c7d8dbbd7a05` |
| Guest bytes | `assets/producer/aggregate_image.bin` | 1,868,700 bytes; `0bb44c54238f78fe04a385b689ddcce9a1b8770eac5a2f0ae9e71de1b62b0d46` |
| Generated descriptor | `production/ARTIFACTS.json` | Generated canonical bytes, at most 1 MiB |
| Relative profile template | `production/PROFILE-TEMPLATE.json` | Exact pinned input bytes, at most 1 MiB |

Require three distinct artifact paths and their exact retained bytes, not just
an arbitrary executable under the right prefix. Do not rebuild the binaries.
The aggregate execution image is
`9d5072a67f5ab2c4f9468df03c2424d71c457021c4b442d7739c5a3d51ba2865`;
it is NOT the guest file SHA-256. The descriptor's `aggregate_image` and
producer support `image_id` must equal this execution image. The ordinary
consumer manifest/input `aggregate_image` is a DIFFERENT role: preserve the
current selected `99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60`
default. Distribution validation keeps its predecessor nonzero/nonindividual
grammar; the exact future input selector preserves its current digest. Do not
silently change consumer acceptance policy when adding production. A receiver
adopting the new producer image needs its own explicit trust selection. Retain
the current foundation/policy and individual relation identities unchanged.

The existing six `roles` remain exactly `native`, `receipt`, `aggregate`,
`image`, `frontend`, `foundation`, with their old paths/semantics. In particular:

- Consumer `receipt` is not the producer stage host.
- Consumer `aggregate` is not the producer snapshot host.
- Consumer `image` and ordinary `preparation.producer.image_id` remain the
  individual relation `9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e`.
- Producer support `host` is the stage host and its `image_id` is the aggregate
  execution image. This is a separate profile, not a mutation of preparation.

The producer namespace is closed: exactly the three binary files above under
`assets/producer/`, and exactly the two metadata files above under `production/`.
Every file participates in the full release file map and exact installation
census. No historical build folder, repository path or research command is
needed after assembly.

## Exact manifest extension

V4 has exactly:

```text
schema, base_manifest_sha256, base_role, files, sdk_sources,
roles, aggregate_image, preparation, lean_support, build_input_sha256,
production

production = {
  descriptor: RelativePin,
  profile_template: RelativePin
}
RelativePin = {path: canonical relative POSIX file path, bytes: integer, sha256: digest}
```

The two production pins must name the fixed metadata paths above, match `files`
exactly, and be distinct. `V5-RELEASE.json` remains outside its own file map.
Keep base manifest pin/projection, required reader/service sources, wrapper
bytes, Lean private-support closure and all existing full-manifest checks.
Keep all file-map bounds: 20,000 files, 128 MiB per payload, 2 GiB total,
case/directory alias rejection and file-as-parent rejection. Input/release JSON
remain at most 8 MiB. These are bounded installation limits, not corpus limits.

`validate_manifest` can validate the pins and their file-map relationships from
the manifest alone. It cannot validate the contents of descriptor/template
merely because their hashes are present. The builder must validate its selected
template and generated descriptor before committing files. `verify_release`
must additionally pin/read those two files and validate their complete content
and cross-bindings before returning success or exposing producer capability.
Do not weaken current `full=False`: it still censuses the whole installation
and hashes every non-base payload. `full=True` retains all-file verification.

Use one closed data-validation helper for this producer grammar where practical;
loading it must use its manifest-pinned held bytes without importing the producer
package or constructing an owner. The public helper is stdlib-only. Do not
duplicate loosely different template validators between build, profile creation
and the worker.

## Descriptor and template contents

The descriptor retains structural schema
`DMKN_RELEASE_AGGREGATE_ARTIFACTS_V1`, exact fields:

```text
schema, foundation, policy, relation_image, aggregate_image, roles, sources
```

`roles` has exactly `stage_host`, `snapshot_host`, `guest_image`, each a relative
pin to its fixed file. `sources` has exactly the successor's 31 named core
modules, each pinned to its fixed logical `sdk/v5` path. The 31 are the retained
27 plus `admission.pin_phase`, `admission.trust`, `admission.clean_refusal`, and
`release_production.launch_contract`. Keep the current verifier and all three
current helper bytes; do not restore the historical verifier. The selected
successor's exact source map, not the old descriptor, supplies changed hashes.

The relative template has schema `DMKN_RELEASE_PRODUCER_PROFILE_TEMPLATE_V1`
and exactly:

```text
schema, support_profile, source_pins, base_source_pins,
stage_memory_ceiling_mib
```

All nested pins are relative; there are no release-manifest pins, absolute
paths, output paths, clocks, run names, profile locations or mutable state.
`source_pins` is exactly the descriptor's 31 core pins; `base_source_pins` is
exactly the two `aggregate_small` package/producer pins. Preserve the selected
template's list order as part of identity; reject duplicates, missing or
extraneous entries. Determinism is for the same exact selected template, not
an assertion that differently ordered template bytes have one profile ID.

`support_profile` has exactly the existing `DMKN_V5_PRODUCER_PROFILE_V1`
fields. It binds the fixed base supervisor manifest, stage host, base Python
executable/DLL, two `production` source pins, aggregate image/foundation/policy,
and the exact 49 runtime pins below. Its runtime/source lists are not inferred
from arbitrary caller additions. Every template pin must agree with the file
map; source pins additionally agree with `sdk_sources` and descriptor roles.
The support supervisor/Python/helper identities must agree with the unchanged
selected base projection. Retain the existing stage-memory-ceiling grammar and
separately selected value; packaging grants no increased runtime allocation.

The parent-only `release_production.launch` is an explicit installed SDK source
and release-pinned executable role, but not part of core31 or runtime49. The
worker entry `release_production.operator` and its `aggregate_small.operator`
helper are both runtime pins. No arbitrary owner-source mechanism is added to
the producer path.

## Exact source selection and bounds

Start from the current authoritative130-entry input
`experiments/v5-local-checks/distribution-candidate-preflight-01-input.json`,
SHA-256 `25e7c849e41f394498e21a60cc7800ecffb67b0cee1b3911d7164977ce4f2364`.
Preserve those 130 name/byte/hash rows. Add the twelve logical names enumerated
by the compatibility audit, then `v5/release_production/launch.py` and
`v5/release_production/launch_contract.py`. Fresh changed producer/lifecycle
successors occupy their own newly added logical names; none replace current130.

| Selection | Predicted exact count | Contract |
|---|---:|---|
| SDK union | 144 = 130 + 12 + 2 | Raise SDK upper bound 141 to 144 in build and manifest validation; require all producer roles |
| Ordinary preparation source list | 123 = 109 + 14 | Existing all-Python enumeration, still under unchanged 128 list cap |
| Core descriptor/source list | 31 = 27 + 3 + 1 | Exact named closed set; source pins at most 1 MiB each |
| Producer support runtime list | 49 = 31 + 2 entry/helpers + 16 base runtime rows | Exact selected closure; unchanged list cap 128 |
| Repeated operative installation pins | 60 | Exact deduplicated union below; unchanged 64-count/512-MiB cap |
| Public selection runtime pins | Separately derived | Preserve existing 256 ceiling; do not substitute the full installation census |

The 60 union is: 49 runtime rows; two Python executable/DLL rows; one supervisor
manifest; three supervisor helper files; three producer artifacts; one production
descriptor; one full release manifest. The support/base source pairs already
belong to the31 and add no rows. The template and parent launcher are separately
full-release/parent-verified, not silently claimed to be worker repeated pins.
The full Python installation closure is still much larger than16 base runtime
rows. The repeated subset is not a hermetic OS/interpreter proof.

These are source-design counts, not an observed successor installation. Root's
final named map must establish them after the new source hashes exist. Do not
drop required files to meet a cap or raise another cap in anticipation. The
ordinary SDK continues to allow at most2 MiB per source; selected producer core
has its stricter1 MiB limit. If final code introduces another import, rederive
the maps before launch rather than assuming this count remains valid.

For this minimal integration retain existing all-Python preparation projection:
123 is below128 and does not change preparation semantics. It adds14 bounded
metadata/source rows to ordinary client operations. This is an explicit small
cost, not a claim of zero overhead. Producer launch does not materialize an
unused receiver preparation, and does not copy all144 SDK files into each
producer operation. A later consumer source-projection optimization is not
needed to close this integration and should not displace it.

## Acyclic release identity and materialization

```text
selected SDK/base/artifact bytes
   -> descriptor + relative template
   -> complete file map + V4 manifest
   -> externally adopted manifest digest
   -> materialized absolute profile outside the installation
   -> separately selected finite launch and its genuine result
```

The template neither pins its containing manifest nor its own hash. The
descriptor pins source/artifact payloads only. The manifest pins both metadata
files, all executable bytes, builder and README. After digest adoption,
`materialize_profile(root, manifest_pin, descriptor_pin, template)` performs
closed validation and returns the complete absolute profile without writing,
importing product modules, constructing an owner or starting a process.
The caller saves canonical profile bytes once at a fresh external path.
The selected public profile schema is
`DMKN_INSTALLED_RELEASE_AGGREGATE_LIFECYCLE_PROFILE_V1`, with a distinct
`DMKN-INSTALLED-RELEASE-AGGREGATE-LIFECYCLE-PROFILE-V1\0` identity domain.

Fill the outer release tuple and three explicit adoption maps with the SAME
exact manifest and descriptor pins. Generate source/support/base-source pins
under the actual installed root. There is no `{manifest}` string placeholder
inside a generic arbitrary template: the helper constructs the closed profile
schema and only its specified fields. Repeated materialization for the same
installation/template produces identical profile bytes/ID independently of
the destination profile filename. Relocating an installation changes absolute
paths and creates a new profile lineage; do not migrate old charges or evidence.

## Dedicated dispatch boundary

The distribution exposes `producer-profile RELEASE_SHA REQUEST REQUEST_SHA`
and `producer RELEASE_SHA PLAN PLAN_SHA`. Profile requests have exactly
`schema: DMKN_RELEASE_PRODUCER_PROFILE_REQUEST_V1` and `output_directory`.
Producer PLAN is the exact public LAUNCH_V1 selection, passed unchanged. Their
grammar is separate from `DMKN_V5_INSTALLED_REQUEST_V1`; do not overload generic
`run`, require a reader `runtime_mode`, or add a pretend entry under `owners/`.
Keep existing wrapper-map validation closed and unchanged. Parent launcher
selection is fixed to `sdk/v5/release_production/launch.py` and release-pinned;
it is not a caller-specified executable or source path.

Both branches first require the adopted V4 release and validated producer
capability. Profile creation checks whole-installation output exclusion and
writes only fresh outside files. It writes `PROFILE-PENDING.json` before any
profile/success result; a successful last commit removes pending only after
all checks and reporting. A valid `RESULT.json` requires absence of both
pending and `PROFILE-FAILED.json`. If finalization and writing the failure
marker both fail, pending still prevents a stale saved success from becoming
accepted completion. Finite operations retain original public
clocks, use the genuine launcher selection/result schemas, and preserve stable
installed core origins. Child/import/closure/accounting/evidence details belong
to the shared launch contract, not a second implementation in this document.
No normal producer launch constructs consumer runtime adoption or grants trust
to a returned mathematical result. Existing independent receipt acceptance is
unchanged.

## Required next evidence and stop boundary

Before assembly, independently inspect one exact final144 map and changed
source closure, generated descriptor/template grammar, V4 container adoption
and shared profile materializer. A pure malformed-input refusal is distinct
from a file hash/census pass. Source review can settle the deterministic schema,
path, count and digest-cycle issues; no host/proof experiment is needed for them.

Only after separate root selection: small changed-boundary checks for wrong
artifact/source/template role, oldV3/extra-field refusal, source-count overflow,
manifest/template pin disagreement, omitted forward-import helpers, identity
stability across profile output paths and whole-release output overlap. One
fresh full assembly must then verify its actual complete census and current130
preservation. One installed constructor/public-action check addresses the new
origin/evidence seam; no repeated native build or heavy proof follows from this
contract. Preserve every partial failure and finalization override.

This closes a packaging design choice, not a deployable-v5 claim. Public native
snapshot operation, genuine continued proof lifecycle, renewed knowledge reuse,
release security and independent-host deployment retain their own evidence
requirements. No ongoing proof, old profile or allowance is touched here.
