# Release-owned aggregate producer

This component reuses the existing generic lifecycle and finite aggregate proof
scheduler. It replaces the producer's **installation adoption**, not its
mathematics. Source-only implementation is not a verified release or a proof.
The separate command entry is owned and selected by the enclosing operator.

## Why this component exists

The retained typed producer requires315 nonempty build/source/runtime files at
construction. The generic snapshot selection permits256. More fundamentally,
ordinary operators should not need the maintainer's historical compiler outputs,
source snapshots and command logs at their original absolute paths.

A maintainer audits that evidence once. A local operator explicitly adopts an
immutable release manifest and its exact artifact descriptor. This component
checks only that release's operative source/runtime/binary subset. Returned
receipts still require independent receiver verification under the exact image,
foundation and policy. Hash equality is not checker correctness, publisher
authentication or mathematical acceptance.

## Public class

```python
from release_production import ReleaseLifecycleProducer

owner = ReleaseLifecycleProducer(exact_owner_profile)
try:
    # Choose ONE separately authorized lifecycle operation.
    result = owner.profile_document()
finally:
    owner.close()
```

The inherited operations are `prepare`, `snapshot`, `production_request`,
`preflight`, `run`, `close` and `report`. Only `run` dispatches proof stages.
`snapshot` executes the selected guest layout once but produces no certificate;
`production_request` constructs and preflights once but neither funds nor runs
it. No command automatically advances to another operation.

Imports and construction require the enclosing trusted local source-selection
boundary and isolated Windows Python. The constructor is not a safe execution
interface for downloaded peer code. Snapshot evidence presently retains the
generic local-check outer grammar; the installed launcher needs an explicit
evidence adapter before it can advertise these operations as public commands.

## Exact profile schemas

Outer schema: `DMKN_RELEASE_AGGREGATE_LIFECYCLE_PROFILE_V1`.
Exact fields:

```text
schema
base_profile
source_pins                 exact27 core absolute pins
snapshot_host_build         release/descriptor/snapshot_host pin map
release                     {root, manifest, descriptor}
```

`release.root` is the canonical ordinary installation directory.
`release.manifest` is an externally selected pin for `ROOT/V5-RELEASE.json`.
`release.descriptor` is an externally selected pin for a file inside that
manifest's file map. The release uses the existing
`DMKN_V5_DIRECTORY_RELEASE_V3` container, not another installer format.

Inner schema: `DMKN_RELEASE_AGGREGATE_OWNER_PROFILE_V1`.
Exact fields:

```text
schema
support_profile             unchanged DMKN_V5_PRODUCER_PROFILE_V1 grammar
source_pins                 exact2 aggregate_small source pins
relation_image              exact individual relation I
host_build                  release/descriptor/stage_host pin map
image_adoption              release/descriptor/guest_image pin map
stage_memory_ceiling_mib     positive, no larger than the adopted supervisor cap
```

All maps here contain ordinary `{path, bytes, sha256}` pins. Their `release`
and `descriptor` entries exactly equal the outer pins. The host/image field
names are compatibility slots under a **new explicit artifact-reference
schema**, not historical result/attempt records. Old typed/small profiles and
mixed old/new schemas are refused. No historical PASS record is synthesized.

The profile ID is SHA-256 of canonical profile bytes after the domain prefix
`DMKN-RELEASE-AGGREGATE-LIFECYCLE-PROFILE-V1\0`. This includes local paths and
release identities. Relocation creates a different operational profile; old
requests, charged allowances and checkpoints are not transparently migrated.

## Descriptor

Schema: `DMKN_RELEASE_AGGREGATE_ARTIFACTS_V1`.
Exact fields:

```text
schema, foundation, policy, relation_image, aggregate_image, roles, sources
```

`roles` has exactly `stage_host`, `snapshot_host` and `guest_image`. Each value
is a relative `{path, bytes, sha256}` pin bound to the manifest's file map.
The implementation accepts the exact selected binaries recorded in `ARTIFACTS`
in `adoption.py`, and the exact A* execution image ID. The execution image ID
is distinct from the SHA-256 of the guest file; the existing host still computes
and checks the execution image identity.

`sources` maps the27 names in `producer.SOURCE_MODULES` to exact relative pins:
`sdk/v5/PACKAGE/__init__.py` for a package and `sdk/v5/PACKAGE/MODULE.py` for a
module. The set is lifecycle24 plus `release_production`,
`release_production.producer` and `release_production.adoption`. Actual imported
origins and the outer source pins must match this exact map. No typed historical
adoption module belongs to the closure.

The manifest contains the descriptor's pin. The descriptor must not contain
the enclosing manifest's digest. The external owner supplies that digest;
neither object is self-authenticating. This avoids a manifest/descriptor hash
cycle. The component does not reinterpret the full consumer release's role
selection or claim that unrelated manifest payloads have been validated.

## Runtime closure and safeguards

All operative support/source/binary/descriptor pins are confined beneath the
selected release root and bound to its file map. Paths with traversal, reparse
points, reserved components, case aliases or a file used as a parent are refused.
The exact support supervisor manifest and its three actually loaded helpers are
also bound. The repeated-rebind installation pin set is at most64 entries,
totaling at most512MiB; the planned current composition has56. This is not the
complete set of files Python may load. The staged fixture copies and verifies
the whole584-file Python subtree once; ordinary calls retain the existing
selected-runtime pin scheme and trusted stable-installation assumption, not a
new per-call hash of every standard-library file. New operation inputs remain
separate.

The constructor reuses `production.Producer` for actual support loading, checks
that its resulting pin set exactly matches the adopted closure, and preserves
the inherited profile immutability, source-origin, no-override, failure-marker,
request, session, prior-charge and stage-bound checks. A close error during a
failed constructor is reported together with the original failure, not hidden.
No process or network call is made by artifact adoption or construction.

The aggregate owner's immutable output-exclusion root and host working directory
are the full release root. The support loader retains its separate base root.
All host/input/output arguments are absolute, and new snapshot/command evidence
binds the release working directory explicitly. Direct class calls therefore
cannot create output elsewhere inside the immutable release merely because it
lies outside the nested support directory.

Existing scheduler and generic snapshot caps remain unchanged, including the
256-entry selected runtime-map limit. Explicit legacy private build-adoption
methods refuse instead of falling back to historical records.

This assumes a trusted bootstrap and owner-controlled local files stable during
an operation. It does not prove a hermetic OS-loader closure, provide a hostile
code sandbox, authenticate publishers or implement automatic security updates.
The maintainer retains the old build evidence for independent audit; deleting
or moving old research evidence is not part of this component.

## Standalone adoption inspection

`adoption.load(release, source_pins, support_profile)` is the real bounded
component validator used by the constructor. It returns a namespace containing
`root`, `pins`, `roles`, `descriptor`, `manifest_pin` and `descriptor_pin`.
It makes no owner, host or proof calls. Its result is descriptive data, not a
mathematical handle or funding authorization. The caller must still use the
actual producer to establish its construction and lifecycle invariants.

No package, runtime invocation, new profile, selected snapshot or proof funding
is implied by these source files. Use only independently reviewed exact source
and owner-selected finite operations; preserve failures without automatic retry.
