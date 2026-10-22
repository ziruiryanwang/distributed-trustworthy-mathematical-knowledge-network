# Release-owned typed producer: deployment seam

Source-only recommendation, 2026-10-22. Author: storage_integration_adapter.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Root owns implementation selection, execution, funding and release adoption.
No constructor, product import, test, snapshot, request, build or proof was run
for this note. Existing profile1242 and live U operation64938 remain untouched.

## Decision

Introduce one small, release-owned producer adoption boundary, reusing the
existing aggregate scheduler and generic lifecycle. Do not enlarge the snapshot
pin caps merely to keep an operator dependent on the maintainer's research tree.

The distinction is:

1. A maintainer reviews and freezes the exact source-to-artifact evidence once.
2. A local operator explicitly adopts a release manifest digest and its exact
   artifact-role descriptor. Runtime validates the selected release files.
3. A receiver still verifies a returned certificate against its independently
   adopted image, foundation and policy. Neither a release descriptor nor a
   successful producer command constitutes mathematical acceptance.

This is the same explicit local artifact-adoption trust boundary already used
by the installed consumer distribution. It is not a new trustless build proof,
automatic publisher authentication, or a substitute for checker correspondence.

## Concrete blocker: the old snapshot cannot be selected as-is

The source-derived installation union for
`experiments/v5-local-checks/typed-production-controls-01-profile.json`
(59,701 bytes, SHA-256
`1242b0a8430e68032bbedbddcb3c6539fbdc95a2a5cf567936545c5f891246cc`)
contains **315 unique nonempty pins, totaling 147,559,292 declared bytes**, plus
eight separately checked empty evidence files. This is a read-only union of
profile fields and retained JSON maps, not an executed constructor census.

The exact set is specified by the following derivation. Union is by exact
absolute path; duplicate paths must have identical byte counts and SHA-256.

| Constructor contribution | New unique nonempty pins | Cumulative |
|---|---:|---:|
| Support manifest, its three loaded helper files, support host/Python/DLL/source/runtime pins, base source pins and lifecycle source pins | 54 | 54 |
| Typed stage-host adoption below | 190 | 244 |
| Typed image adoption below | 62 | 306 |
| Generic snapshot-host adoption: five records, three copied sources, executable | 9 | 315 |

Stage-host contribution is five profile build records, 179 nonempty rows of the
180-row `source-map.json.files`, four additional outputs (the fifth, the stage
host, is already in support), and `environment-profile.json` plus `INPUT-MAP.json`.
The excluded empty row is `source/evidence/11-output`.

Image contribution is ten profile records, 37 copied guest project sources, two
guest-build adapter sources under the canonical root, three assembly-wrapper
source snapshots, four actual compiler command records, two nonempty compiler
logs, the user ELF and linker map, assembly stdout, and the combined image.
Six empty compiler logs and assembly stderr are checked separately.

No U wire, capsule, theorem receipt, target header, snapshot session or proof
checkpoint belongs to this constructor union. The 236-item guest retained input
map and 1,071-item old compiler runtime map are committed historical data, not
recursively added live files. Treating every JSON pin as a runtime requirement
would therefore produce a different, incorrect inventory.

All six inspected current sources match their selected stable-profile digests:

| Logical source | Stable SHA-256 |
|---|---|
| `production/producer.py` | `5555e944d7473731e3e9095e85c5c57ce89c5f59187f78c5b248b4c1227532f3` |
| `aggregate_small/producer.py` | `a2d23bcfe0b798f747d4a59330655a865a14a73cb4d635a50332fa65c75a6985` |
| `aggregate_lifecycle/snapshot.py` | `8c65e623419f846c2b7607716ce7fdec8a611ae2bb340e9a9cab18af3c741546` |
| `typed_production/producer.py` | `44c3700737300c879d5b85111361bd9e5bd55f8503a14e607d1a47c521c09692` |
| `typed_production/host_adoption.py` | `0553220f16866f8f9d0cb586f73d182e15074cf66c030421a903f4dcde7e5f87` |
| `typed_production/image_adoption.py` | `e1bf74167d09d3dbaceb841366363dc698cf290a891d5ffce743f86dfce76f4a` |

Three distinct callers impose a 256-entry snapshot runtime-map bound:
`Run-V5-Check.py`, the new lifecycle entry's `_snapshot_selection`, and
`aggregate_lifecycle.snapshot._selection`. The last additionally requires the
map to contain every constructor pin and the new configuration, profile and
packet: at least318 entries for the present profile. No selector satisfying
those requirements exists. The independent boundary review reproduces this
finding at `TYPED-SNAPSHOT-PIN-BOUNDARY-REVIEW.md`.

This is not the support profile's128-entry runtime bound (its47 rows fit), a
parent/segment limit, or a mathematical restriction on aggregation. A cap-only
repair would require fresh wrapper, entry and generic snapshot sources, with a
fresh profile; changing only a selector would not repair it. It would also leave
the fixed canonical directory and build-history dependency intact.

## What is actually required at runtime

The unchanged executed roles are:

| Role | Exact retained candidate |
|---|---|
| Stage/verification host | 68,039,168 bytes; SHA-256 `263841ae256af217de2c00452c7f0688a2e9e58e6aa6d95457d5118aef04ff3c` |
| Snapshot host | 6,630,400 bytes; SHA-256 `a9438205bbb091623f12bd10a7e9a0a2b437c873003fec3cb000c7d8dbbd7a05` |
| Combined guest image | 1,868,700 bytes; file SHA-256 `0bb44c54238f78fe04a385b689ddcce9a1b8770eac5a2f0ae9e71de1b62b0d46` |

The guest's **execution image ID** is
`9d5072a67f5ab2c4f9468df03c2424d71c457021c4b442d7739c5a3d51ba2865`.
It is not the guest file SHA-256. The selected host's existing image computation
and exact receipt/header checks remain necessary. The individual relation ID
remains `9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e`.

Also required are the ordinary producer source closure, Python/support files,
explicit foundation/policy, and a fixed adopted release descriptor. New packet,
parent receipts and session artifacts are per-operation inputs, not installation
history. Their existing checks and costs must remain.

The historical compiler/library outputs, source copies, command records and
logs explain how the release was produced. They need not remain online beside
every operator if the operator explicitly adopts the already-reviewed release
artifacts. Preserve them in the maintainer evidence archive; do not delete,
rewrite, or convert them into newly invented historical records.

## Smallest proposed code boundary

Create only the following new package, after root selects implementation:

| File | Responsibility |
|---|---|
| `software/v5/release_production/__init__.py` | Export the release-owned class; no artifact adoption or execution at import |
| `software/v5/release_production/adoption.py` | Pure bounded descriptor/relative-role validation, exact file binding, and release source-origin checks |
| `software/v5/release_production/producer.py` | Explicit new-profile constructor over the existing lifecycle/scheduler |
| `software/v5/release_production/operator.py` | Separately selected local entry using the reviewed lifecycle entry contract, but its own exact new source/profile grammar |

Do not modify current used `typed_production`, `aggregate_small`,
`aggregate_lifecycle`, `production` or the old entry. Do not fork the scheduler,
receipt formats, stage graph, snapshot mathematics or resource-accounting code.

The class is `ReleaseLifecycleProducer(LifecycleProducer)`. It inherits the
generic lifecycle methods and aggregate scheduler, not `TypedLifecycleProducer`.
It must never import the five typed historical-adoption modules merely to gain
the new image constant. Adopt the selected image explicitly from the exact
release descriptor and verify its allowed foundation/policy tuple.

The new constructor performs a small explicit initialization, as the typed
successor already does for a changed profile, but it does **not** invoke an old
constructor with fabricated historical records. The required order is:

1. Validate and canonicalize the new outer and inner schemas and new domain
   separation; initialize lifecycle readiness false and all scheduler state.
2. Validate the externally adopted release/descriptor pins and source roles.
3. Construct unchanged `production.Producer` with an ordinary exact support
   profile; obtain its supervisor, Job and initial pins. The support retains its
   own base installation. Set the aggregate owner's `_install` to the complete
   adopted release root, so inherited output-overlap guards protect the entire
   immutable release, not just its nested base directory. Host arguments remain
   absolute; new command evidence binds this release working directory.
4. Check memory ceiling against the actual supervisor ceiling; bind exact source
   pins and the three runtime roles. Check foundation/policy/I/A identities.
5. Set `_image`, `_snapshot_host` and the new ordinary artifact-reference maps
   described below. No build-adoption method executes.
6. Set the new composite profile ID and readiness true, check byte/count bounds,
   and perform the normal installation/source rebinding. Constructor failure
   closes any constructed support owner and remains attempted/unconfirmed.

Inherited `prepare`, `snapshot`, `production_request`, `preflight`, `run`,
`close` and `report` retain their existing finite-operation meanings. Request
construction preflights once, not twice. There is no automatic run, retry or
allowance renewal. Explicitly refuse legacy private adoption entry points so
there is no accidental historical fallback.

## New profiles and the no-override contract

Use distinct schemas, provisionally:

```text
DMKN_RELEASE_AGGREGATE_LIFECYCLE_PROFILE_V1
DMKN_RELEASE_AGGREGATE_OWNER_PROFILE_V1
DMKN_RELEASE_AGGREGATE_ARTIFACTS_V1
```

The agreed outer profile has exactly:

```text
schema, base_profile, source_pins, snapshot_host_build, release
```

The inner `base_profile` has exactly:

```text
schema, support_profile, source_pins, relation_image,
stage_memory_ceiling_mib, host_build, image_adoption
```

The names `host_build` and `image_adoption` here are compatibility slots used by
unchanged scheduler rebinding, **under a new schema with different explicit
meaning**. They are not claimed to be historical build-result grammars:

```text
host_build       = {release: manifest_pin, descriptor: descriptor_pin,
                    stage_host: stage_host_pin}
image_adoption   = {release: manifest_pin, descriptor: descriptor_pin,
                    guest_image: guest_image_pin}
snapshot_host_build = {release: manifest_pin, descriptor: descriptor_pin,
                       snapshot_host: snapshot_host_pin}
release = {root: absolute_installation_root, manifest: manifest_pin,
           descriptor: descriptor_pin}
```

Every value is an ordinary exact `{path,bytes,sha256}` pin; all corresponding
copies of the manifest/descriptor must be equal. No `result`, `attempt`, fake
command record or old schema marker is manufactured. Strictly reject extra
roles, changed source maps and mixed old/new schemas.

Set `_snapshot_build_pins` to an exact immutable copy of `snapshot_host_build`.
This explicitly satisfies the inherited lifecycle's field dependency without
pretending a build happened at the new location. Keep `_no_override` unchanged:

- `LifecycleProducer._check` still checks profile identity, inner/outer equality,
  its ordinary24-source origins, and the snapshot artifact pin parents.
- The subclass adds its three new module origins and exact descriptor/profile
  identity checks; it calls the inherited checker, not a weaker substitute.
- `snapshot.execute` retains both host/image map failure-marker checks.
- `AggregateProducer._run` retains host/image/snapshot map failure-marker checks,
  **and separately** all session-snapshot and prior-attempt marker checks.
- Neither a failed snapshot nor a failed earlier attempt can be laundered through
  a valid release manifest. The release changes installation adoption only.

The new profile's hash commits to all operative absolute paths at materialization
time. A relocation therefore gets a fresh operation/profile identity. Do not
reinterpret old requests or checkpoints under the relocated identity. The
mathematical image and returned certificate identities do not change merely
because an operator moved its installation.

## Release descriptor and one-time audit

Reuse the existing `DMKN_V5_DIRECTORY_RELEASE_V3` manifest's file-map container
and relative-role materialization model. The component validates only its
operative subset against the externally adopted complete manifest; it does not
claim full distribution validation or invoke the whole distribution loader.
The descriptor should have a fixed small schema containing its version, exact
foundation/policy/I/A tuple, exact stage/snapshot/guest relative artifact pins,
and the selected producer source-role map. It may commit to a bounded list of
offline evidence digests for audit retrieval. Those digests are not mandatory
local runtime file locations, executable inputs or mathematical proofs.

The containing release manifest pins the descriptor. The descriptor **must not**
contain the digest of that containing manifest, which would create a digest
cycle. External owner adoption supplies the manifest digest. The materialized
profile can then contain both manifest and descriptor pins without a cycle.

Runtime validates every operative role against the adopted manifest, confines
relative paths beneath an ordinary immutable release directory, validates
declared file sizes and SHA-256, and binds imports to the exact selected source
origins. It must not read arbitrary descriptor paths to find missing evidence,
search for a convenient executable, or manufacture trust by hashing unknown
files. Stable owner-controlled local files remain an assumption; exact hashes
are not protection against a compromised interpreter or concurrent hostile OS.

Before selecting a descriptor, the maintainer gate checks the existing complete
host/image evidence, source-to-artifact chain, absence of finalization failures,
the reviewed image-parametric stage-host behavior, actual assembled image ID,
and independent correspondence/acceptance assumptions. Record the resulting
exact release role tuple. This remains review-based artifact adoption unless a
separate reproducible-build/formal correspondence proof is actually supplied.

Later discovery of a compromised release requires an explicit trust-withdrawal
or update policy; a historical build file remaining present on one workstation
is not a global revocation mechanism. Do not silently add such a mechanism in
this small constructor change.

## Proposed installation bound

The release class's imported core is the existing lifecycle24 plus its three
new package modules:27. Its separately selected entry and existing
`aggregate_small.operator` helper add two runtime source pins. Retaining the
current16 non-source Python runtime entries gives45 support runtime pins.
The support constructor adds the manifest, three loaded helper sources, stage
host, and Python executable/DLL:52 unique paths in this proposed exact layout.
Guest image, snapshot host, adopted release manifest and descriptor add four:
**56 expected installation pins**, before any extra explicitly selected role.
This is the repeated-rebind constructor union, not the complete Python/OS file
closure. The test component separately copies and verifies the complete584-file
Python subtree once; ordinary calls retain the existing selected-runtime and
trusted stable-installation assumptions.

Use a prospective hard installation count bound64 and the existing512MiB
installation-byte bound. The exact new release/profile must independently
demonstrate its counted closure before use;56 is a source-derived design count,
not an executed or already-adopted distribution inventory. The snapshot's
configuration/profile/packet then add three runtime-map rows, leaving large
headroom under unchanged256. Parent receipt count and proof ancestry do not
enter this installation count.

This count does not authorize dropping a runtime dependency. If an actual
dependency is required, name and count it; do not raise the cap automatically.
Dynamic OS-library/loader dependencies remain the existing explicit deployment
assumption and do not become hermetically proved by this file inventory.

For reference, the old54 support/source pins total86,644,865 declared bytes;
adding only the two missing binary roles gives95,143,965 bytes before the
changed sources and release metadata. That is a storage/accounting observation,
not a measured startup saving. New exact source/manifest sizes must be counted.

## Reuse the current distribution; do not build another installer

The current candidate's selected distribution source is
`software/v5/body_location/distribution.py`,54,824 bytes, SHA-256
`eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813`.
Do not base integration on the older `software/v5/distribution/distribution.py`.
The current code already offers exact file maps, bounded copy verification,
relative roles, materialization, explicit manifest adoption, immutable fresh
output and the existing `client.launch`/`boot` resource/source boundaries.

A later selected distribution successor needs a closed optional producer
capability with stage-host, snapshot-host, aggregate guest and descriptor roles.
The existing `image` asset is the individual/native preparation image; never
silently replace it with the aggregate image. Existing `aggregate` is the
consumer verifier executable; a shared same-byte stage host may occupy two
named roles only if that equality is explicit. Producer capability must not
cause a lightweight reader to create proof work or download build history.

Importing all typed29 into the current130-source distribution would produce142
logical sources, exceeding its141 bound. The proposed closure avoids the five
typed historical modules: lifecycle24 adds seven presently absent logical files,
and the four new package files bring130 to141. This is only the source-set
arithmetic; same-named sources still require exact semantic/version review.
Do not replace an installed consumer source just because a producer profile
has another file at the same logical name. A conflict needs one reviewed common
successor or explicit source isolation, not silent last-writer-wins packaging.

## Remaining launcher seam: do not overclaim portability

The small constructor proposal makes existing generic snapshots satisfiable
without historical paths. It does not by itself make the research wrapper a
public release command. `Run-V5-Check.py` still requires the canonical root and
research selection/output directories; the old lifecycle entry recognizes that
wrapper's schema and exact invocation.

For public installed operation, reuse the existing installed launcher rather
than package that research runner. Its evidence is
`DMKN_V5_CLIENT_LAUNCH_RESULT_V1` with a pinned
`DMKN_V5_CLIENT_LAUNCH_V1` plan, boot result, source snapshot and ordinary Job
closure. That is not the generic snapshot's present
`DMKN_V5_LOCAL_CHECK_RESULT_V1` outer schema. A later explicit installed-evidence
adapter/schema must validate the actual plan, owner entry/source bindings,
configuration/packet/runtime roles, source origins, clean boot/Job closure,
limits, exact command, output census and finalization markers.

Do not relabel an installed launch as an old research result or allow failed
evidence to fall back between schema branches. Share the existing generic
snapshot mathematics and result/session checks; adapt only the externally
supervised operation evidence boundary. The current installed launcher has its
own finite1-hour/4096MiB limits; multiple explicit funded proof-stage requests
are permitted by existing scheduling, not an automatic daemon or cap increase.

Thus implementation can proceed with the small release constructor/entry first,
with current generic snapshot caps unchanged, while the product packaging and
installed-evidence adapter remain explicit subsequent release obligations. A
constructor source pass or local snapshot pass is not final-v5 completion.

## Minimal decision-changing verification after source review

Do not repeat the completed receipt campaigns or start another guest build.
The changed boundary requires small checks, selected separately by root:

- Inert descriptor/profile controls: wrong role bytes, wrong I/A tuple, old/new
  schema mixing, path escape, conflicting pins, changed source origins, excess
  count, absent file, output overlap and mutation/failure-marker refusal.
- An adopted release-role closure inspection proving the count fits64 and no
  mandatory path lies outside the selected release, apart from explicit operation
  inputs. Check dynamic-loader assumptions separately, without inventing
  missing files or scanning all historical work.
- A small relocated public constructor/request operation once that public
  evidence adapter exists; original research paths must not be used. A result
  forged from retained old records is not such an operation.
- One genuine bounded new snapshot only when actual admitted U and its new V
  packet exist, under a new profile/session/allowance. The same actual result
  should serve both the renewal and deployability evidence questions when the
  selected boundaries align; do not duplicate costly work for another label.

Stop at the first contradiction, preserve the failed bytes/charges, and return
the consequential source finding to root. No automatic retry, source mutation,
profile reset, funding increase or proof launch follows this note.
