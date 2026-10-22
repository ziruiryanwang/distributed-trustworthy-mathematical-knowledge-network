# Installed producer: independent source review

2026-10-22; reviewer `storage_outcome_audit`. Canonical root only.
Selection: `INSTALLED-PRODUCER-SELECTION.md`, SHA-256
`dbaca172035ada81ae82edcd5d57b2424eb758b9692e9e68299d27ba0d4f8f16`.
Design review: `RELEASE-PRODUCER-PUBLIC-LAUNCH-REVIEW.md`, SHA-256
`cda443bc17dfecc7dafc76f17fcf70acf756a86c34c6eb096ea3da55078beef4`.

Status: **PASS for the exact source-only integration scope below.** All complete
source paths and the last metadata cap repair have been reviewed and pinned.
No unresolved blocking source finding remains in this selected boundary.
No product import, constructor, syntax/test
execution, build, proof or Git mutation is performed by this review. Findings
are sent to the responsible author/root immediately rather than waiting for a
single late report. All prior used source/evidence and live proof work remain
untouched.

## Reviewed slices so far

- Full first authored `release_production/launch.py` in the fresh overlay.
- Full first authored `release_production/launch_contract.py`.
- Complete diff of `release_production/operator.py` against the frozen release
  component entry, plus its unchanged action/finalization logic.
- Complete fresh core/adoption diffs against the frozen release component.
- Complete fresh distribution diff against current `body_location/distribution.py`
  `eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813`.
- Existing producer support-loader, generic snapshot/outer validators and inner
  request lineage contracts relevant to these changes.

Physical overlay is `software/v5/installed_production/`; logical names remain
the installed SDK names. A final review will bind exact terminal source pins;
intermediate mutable hashes are not an approval of later bytes.

## Exact reviewed cut

All eight physical paths below are relative to `software/v5/installed_production/`.
Unchanged package initializers are reused, not additional fresh overlay files.

| Source | Bytes | SHA-256 |
|---|---:|---|
| `release_production/adoption.py` | 10818 | `dcedd229c64120beaaf755b2653ff923da2c896f6ed6dd8f103859f8becc2baf` |
| `release_production/producer.py` | 7883 | `a466726b79c9a5851ea4e085307aa5ba593c83e2881dc4e168446cbc4f573b1a` |
| `release_production/operator.py` | 26808 | `f404f0ba4d5177654fd02e999b00c0d8d104f1a4b85295414dff2720ddf6021a` |
| `release_production/launch_contract.py` | 30932 | `ad2e63a2236d52b2507834dce32f77c1dc3fc55f198dbf39382cb1374a95c802` |
| `release_production/launch.py` | 16594 | `3310fbacc7c7724aea37bc2370a29d574fb49685389614e983e0dacf7329a337` |
| `aggregate_lifecycle/producer.py` | 8947 | `ee5b11911ebb7d77c860c0b441de45257e43fea890b44af248bb669e0a7be7b7` |
| `aggregate_lifecycle/snapshot.py` | 22644 | `c38b6ffc14d47cb35e20eb128db098dda878c0194cbdfd7bb73ed5ce17b91666` |
| `body_location/distribution.py` | 71246 | `c831e08aeff64ec2c27bd71b784fc8d46822e68b9a9ea5193fbc1833ee58dfcb` |

## Findings and disposition

### IP-S1: saved success can outlive failed finalization and failed marker write

Initial launcher code saved `COMMAND_EXITED_ZERO_AND_CLOSED` before its final
rebind/census/deadline checks. On failure it attempted a failure marker, but
suppressed marker-write failure. A saved PASS without any override could then
survive, while only stdout/exit status indicated failure. A later adopter
reading the files cannot recover that missing negative evidence.

The profile creator had the same structure: saved `PROFILE_CREATED`, later
checks, then a failure marker that might itself fail to persist. Raising an
exception does not change the already saved result.

Sent immediately to root and distribution author. The chosen repair is a
precreated pending-state marker, retained on every precommit failure and removed
only at the documented final successful commit. Consumers must refuse pending
as well as failed records. **Resolved in reviewed source:** both creators write
pending first, retain it on failure, and unlink it only after all checks and
reporting. `completed_outer` rejects pending; the current parent's worker
validator permits its own pending marker but rejects failure markers. No
failable validation/reporting follows the commit unlink. This is a trusted
local-filesystem convention, not a power-loss transaction or hostile-host proof.

### IP-S2: contradictory public output limits

Initial shared contract accepted up to 2 GiB/32,768 entries while launcher
`output_census` rejected above 1 GiB/16,384. A helper-valid plan could therefore
fail before execution at a different layer's undocumented cap.

**Resolved in reviewed source:** helper and parent both enforce the same
1 GiB/16,384 boundary. No output resource cap was increased.

### IP-S3: pin-map merge must not silently choose the runtime row

Initial `rebind_selection` used `{**selected.pins, **selected.runtime_pins}`.
Only the direct profile/input/entry overlap had been compared explicitly;
release/provenance metadata overlaps also require exact pin equality. A later
map entry must not silently override a selected record's expected identity.

**Resolved in reviewed source:** `rebind_selection` checks exact equality at
every intersection before merging the maps. No runtime was used to expose this
source-level issue.

### IP-S4: checking only the last import finder does not bind import policy

The new worker held-byte loader replaced the last `PathFinder`, but its final
guard checked only `sys.meta_path[-1] is guard`. Inserting/replacing an earlier
finder could bypass that finder while passing the final condition, contrary to
the selected policy-change refusal contract.

**Resolved in reviewed source:** entry captures the entire installed meta-path
tuple and checks tuple equality after product imports and during final binding,
together with the complete expected `sys.path`. The owner host/code remain
trusted; this closes a specific consistency hole and is not a claim of
hostile-code sandboxing.

### IP-S5: consumer default is not the new producer execution image

The distribution author found that the first distribution cut accidentally
required the ordinary consumer aggregate-image field to equal producer image
`9d5072a6...`. The current130 candidate has consumer default `99b9f1cf...`.
Adding production must not silently change an existing receiver acceptance
policy. **Resolved in reviewed distribution `c831e08a...`:** both ordinary
image validators retain the predecessor nonzero/nonindividual grammar; the
producer descriptor uses separate fixed `PRODUCTION_IMAGE`. The shared helper
binds descriptor/support to that producer identity without equating the two
roles. The future exact assembly input must retain the old consumer digest.

### IP-S6: new public evidence must fit the existing metadata envelope

The core author correctly questioned whether the generic 14-MiB reserve still
covered two new public evidence reads. Existing worst-case additions are
8 MiB diagnostic + 1 MiB inner result + 2 MiB outer + 1 MiB staging + 1 MiB
native stdout + 64 KiB command + 64 KiB actual invocation = 13.125 MiB.
Bounding the copied entry and worker report to 64 KiB each gives 13.25 MiB,
below the unchanged 14 MiB reserve by 0.75 MiB. **Resolved in reviewed source:**
parent, helper and entry enforce those caps; the entry writes its report under
the same bound. The helper also remembers copied-entry/produced-result pins in
the shallow outer metadata table. No generic scheduler/table redesign or
resource-cap expansion was introduced.

This is a bound on distinct retained session/evidence bytes, not on cumulative
disk I/O across repeated pin checks. Installed runtime and shallow public
lineage validation have their separately specified bounds; the generic final
input-table sum alone must not be presented as accounting for every public
metadata read. No native experiment is needed for this arithmetic.

## Cross-component agreement

The public selection includes both explicit `prior_launches` and `input_launch`;
run/preflight have no manual bypass. The helper checks outer evidence shallowly
rather than recursively replaying predecessor lists. The fresh core chooses
new public profile identity and outer adoption hooks; the old component is not
relabelled. Dedicated parent command derivation is fixed and preserves original
public clocks. Stable product modules execute from held checked bytes, while
the full Python tree is separately checked under the trusted-host assumption.

The distribution diff explicitly adds V4 production metadata/artifacts and
producer commands, raises only its SDK cap to144 at both gates, retains exact
whole-release census and keeps the six consumer roles distinct from producer
binaries. The profile template has no manifest back-reference. None of these
observations substitutes for reviewing the completed byte-pinned source.

The complete ordinary `launch`/`_launch` implementation is unchanged in the
distribution diff. V4 verification additionally validates producer metadata,
so this is not a claim that ordinary calls incur no new bounded metadata work.
The producer commands do not initialize an unused receiver preparation or
invoke `client.boot`. `production_metadata` explicitly matches descriptor
source roles to the installed SDK map after the shared pure validator.

The new protected generic lifecycle hook defaults to historical `N._selection`;
exactly the snapshot execute/adopt sites use it. The installed subclass uses
the new public selector and public outer validator. There is no historical
LOCAL_CHECK translation, monkey patch or fallback after failed public checks.
The actual public command binds the copied selection and entry, installed
source root, exact profile/input digests and owner-report location. The worker
checks this against `sys.orig_argv`; the parent checks the supervisor's actual
argv, cwd and limits. The complete source closure is held and pinned before
product imports, with fixed installed origins; the Python tree is separately
censused and rebound. Neither mechanism is represented as a security sandbox.

Snapshot output and the launch directory are disjoint fresh roots. Request and
preflight must leave the future action output absent. Request output is fixed
to `RUN/request.json`; later run/preflight require the completed request outer
pin naming exactly that input. Each prior inner attempt matches one explicit
completed public outer in order and profile/allowance. The outer check is
shallow; inner scheduler prefix validation remains unchanged. A predecessor's
pending or failed completion is not usable. Operational records grant neither
mathematical trust nor funding authority.

Counts are consistent as a source argument: current130 plus12 union additions
and2 new launcher/contract names gives144 SDK rows; ordinary preparation has123
rows under128. The core is31, the entry pre-import set33, support runtime49,
and deduplicated operative installation60 under64. The full Python subtree,
template and parent launcher have separate explicit validation. These counts
must still be established by the actual selected map/installation; they do not
permit dropping files or changing the current verifier to meet a cap.

The parent uses original public clocks and inclusive child Job CPU. Its output
observation is before result publication; a second census bounds final output.
Precommit report timing omits a bounded tail, not a zero-cost tail. Exact final
byte totals and whole-operation postcommit timing are not claimed.

## Disposition and next evidence

Source disposition is PASS for the exact eight-file cut and integration contract,
not runtime readiness, mathematical acceptance, security certification or final
v5 release. Minor historical V3 wording remains in the adoption docstring/error
label; its actual schema constant and acceptance are explicitly V4. This does
not broaden accepted schemas or require source churn before the next gate.

Actual controls and installed
operation require separate root selection; no heavy proof or repeated campaign
is needed for this source review. The next discriminants are the changed
metadata/lineage/completion boundaries and a genuine installed public action,
not repetition of the six previously passing component groups. An independent
terminal-U outcome/reuse assignment can proceed separately; this source review
does not gate or authorize it.
