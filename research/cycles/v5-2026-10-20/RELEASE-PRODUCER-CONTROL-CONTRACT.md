# Release-owned producer: minimal acceptance and control contract

2026-10-22, storage_outcome_audit. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

**AGREED SOURCE-ONLY CONTRACT; no execution selected.** Root's
RELEASE-PRODUCER-SELECTION permits new controls after schema agreement, but does
not select a package, run, build, proof, installation or funding. Root adopted
the independent 315-versus-256 boundary review `1af2cc61`; the new work addresses
release adoption rather than rerunning existing producer algorithms. Core author,
root and this reviewer agreed the schema/API below. The authored controls use the
real loader's return/exception contract, not an invented test interface.
Used entry/control/profile/evidence bytes stay frozen.

## Agreed schema and API boundary

The new outer `DMKN_RELEASE_AGGREGATE_LIFECYCLE_PROFILE_V1` has exactly
`schema, base_profile, source_pins, snapshot_host_build, release`.
The new inner `DMKN_RELEASE_AGGREGATE_OWNER_PROFILE_V1` has exactly
`schema, support_profile, source_pins, relation_image, stage_memory_ceiling_mib,
host_build, image_adoption`.

`release` is exactly `{root, manifest, descriptor}`: an ordinary absolute local
root plus exact pins for the externally adopted directory manifest and descriptor.
The existing `DMKN_V5_DIRECTORY_RELEASE_V3` manifest is used only as an adopted
file-map container. This component validates its operative subset, **not the
entire consumer distribution**. Tests and reports must preserve that distinction.
The manifest pins the descriptor; the descriptor never pins the manifest.

The artifact descriptor is `DMKN_RELEASE_AGGREGATE_ARTIFACTS_V1`, with exactly
`schema, foundation, policy, relation_image, aggregate_image, roles, sources`.
Its roles are exactly `stage_host, snapshot_host, guest_image`, using relative
pins bound to the adopted manifest. Its `sources` map binds logical module names
to relative pins for the existing lifecycle24 plus new package3: exactly27.
Descriptor/manifest/core-source bytes cannot select undeclared module origins.

The explicitly redefined pin-only compatibility slots are:

```text
host_build = {release, descriptor, stage_host}
image_adoption = {release, descriptor, guest_image}
snapshot_host_build = {release, descriptor, snapshot_host}
```

Here `release` is the manifest pin, not the outer object. All values are exact
ordinary file pins; repeated role pins must be equal. These are not fabricated
historical build records. `_snapshot_build_pins` receives the snapshot role map.
No old schema or old PASS field is manufactured.

The real constructor API is `ReleaseLifecycleProducer(profile)`;
`adoption.load(release, source_pins, support_profile)` is the planned real loader.
Its returned bound roles will be checked directly once authored. Installation
closure is limited to64 pins and512MiB, leaving room under the existing256-row
outer-runtime cap. The separately invoked operator must bind its copied bytes
to the stable release operator runtime pin. Source/constants and exact exception
names will be pinned only after the author finishes them.

## Acceptance invariant

Let `D` be a bounded release descriptor, `h` its externally owner-selected digest,
`I` the chosen ordinary installation root and `R(D,I)` its resolved execution
closure. A successful construction may assert only:

```text
hash(exact descriptor bytes) = h
descriptor schema, roles and mathematical identities match the selected profile
all declared execution/source bytes in R(D,I) satisfy their exact pins
all imports originate in the selected source/runtime closure
|R(D,I)| and its byte/serialization bounds fit the unchanged operation envelope
the new profile identity binds this exact adoption and is not the old U profile
```

It must not infer a valid theorem, new certificate, funded stage, completed
snapshot, useful-growth benefit or host execution. Build provenance is checked
once by separately selected release assembly; ordinary construction must not
reopen the historical experiment tree. Owner software adoption and mathematical
receipt acceptance remain separate trust decisions.

The expected descriptor hash must be supplied through a root-selected argument,
profile or outer pin, not accepted from the descriptor itself. No descriptor
self-hash or source/descriptor digest cycle is permitted. A portable descriptor
uses relative payload identities; its separately pinned local profile binds
the chosen installation root. The exact agreed schemas above remain subject to
the independent source review and do not turn an arbitrary manifest into trust.

## Four small changed-boundary groups

| Group | Necessary checks | Evidence boundary |
|---|---|---|
| Owner adoption and grammar | Wrong expected digest refuses before product imports; known digest with wrong schema/unknown fields or incompatible declared mathematics/roles refuses; no absent-pin fallback | Tiny inert documents may exercise decoding; they are not an adopted software release |
| Relative paths, roles and origins | Parent traversal/absolute path or role alias refuses; all required roles and exact source modules are present; unexpected preloaded product origin refuses; existing hard row/byte limits remain | Reuse existing path primitives; test only the new role-to-path/schema composition, not a new generic filesystem suite |
| Immutable adoption and closure | Exact bytes/origins remain checked after construction; mutation of the effective profile cannot silently change identity; finalization override and close failure prevent a successful owner result | Use at most one targeted seam per newly introduced guard; do not duplicate already passed generic report or scheduler tests |
| No automatic action or identity migration | Construction/report/close never call prepare, snapshot, request, run, host, prover or network; new profile domain/descriptor binding cannot alias old typed profile; generic-only snapshot evidence cannot be relabeled retained U evidence | Identity/dispatch checks plus source proof of inherited exact prior-profile equality; no U receipt/capsule/checkpoint replay |

Each malformed case should target the earliest meaningful new boundary and assert
the refusal category, zero forbidden dispatch and no mathematical/funding claim.
Do not add a separate case for every syntactic variant already handled by a reused
validated parser. Cases that would require a full proof fixture should instead use
a source argument or a tiny inert record at the identity-adoption boundary.

Changing a fixture's descriptor bytes and selecting their new test digest is only
a deliberate malformed-owner-input test. It must not be reported as accepting an
unknown publisher or authenticating a release. Direct tests of original helper
functions should retain those real helpers; doubles may replace only the authority
or costly unrelated step expressly excluded from the claim.

## One cheap real relocated constructor can replace excessive doubles

After root selects a concrete release assembly, prefer one supervised ordinary
process over a fully staged installation:

1. Start the exact selected isolated interpreter, bootstrap and producer from
   fresh relocated paths. Bind the actual descriptor pin and finite source/runtime
   map prospectively, including the descriptor/profile and any new source files.
2. Construct the real release producer once. Invoke only its non-writing
   profile-document and observation APIs, then close it and obtain the actual
   closed observation. Require exact new profile identity, actual `_pins` coverage,
   bounded row/byte count and all loaded module origins. No producer or loader
   implementation is replaced by a double for this positive path.
3. Make process/network/host dispatch forbidden in the harness. Install a
   Python-level open/import monitor that permits only selected installation,
   interpreter, descriptor/profile and test evidence roots, and records/refuses
   historical experiment-file reads. Source inspection must also establish that
   no retained constructor/adoption helper reopens historical paths. The monitor
   is a test observation, not an OS sandbox or a complete native-I/O theorem.
4. Rebind selected bytes and verify terminal clean closure and absent producer
   operation outputs. Preserve the observation, imported-origin list, descriptor
   and actual pin-map identity. Report zero native/guest/proof calls, not a runtime
   proof of mathematical soundness.

This one positive integration tests the actual relocation/import/adoption boundary
that inert lifecycle controls intentionally do not exercise. It needs no packet,
U receipt, V source, snapshot guest, compiler, service, certificate verifier or
proof worker. It can share the small selected test allocation with pure negative
loader controls if process isolation/import-origin tests remain unambiguous.
Exact caps depend on the eventual closed payload manifest; they must be selected
before dispatch rather than expanded after failure.

No historical file is removed or hidden to simulate portability. No used payload
is edited for fault injection. If a new binding guard genuinely needs a real-file
mutation control, use an explicitly selected disposable test-owned fixture copy,
record its initial/final pins and preserve the failure, never the selected release
or live U installation. Existing binding-helper coverage may make that unnecessary.

## Required source argument for unchanged mechanisms

The new loader/adoption boundary must keep meaningful input sets for inherited
checks. In particular, existing snapshot/run code checks the effective profile,
`_pins`, `profile['host_build']`, `profile['image_adoption']` and
`_snapshot_build_pins`, as well as session/prior-attempt finalization overrides.
Empty or fabricated historical V1 records are not an acceptable adapter. If new
typed runtime-role records replace historical build records, their schema and
meaning must be explicit and remain bound by the unchanged closure checks.

Inherited `_request` currently requires a prior attempt's `profile_id` to equal
the current exact profile. Preserve that comparison and the separately checked
session/allowance/history fields. A new software adoption is not authority to
discard U's charges, rename its profile, reuse its unfinished allowance or promote
its checkpoints under a new identity. A new V session is separate even when it
uses the same mathematical A* image and retained host binaries.

Proving these unchanged code paths remain unchanged is the primary evidence;
do not rerun stage scheduling, receipt cryptography, previously passed grammar
controls or the heavy U operation for this release-adoption change. The later
genuine V snapshot/request is a distinct selected integration boundary, not part
of this construction contract.

## Before implementation or launch

Pin the author's actual source, identity-domain rule and loader return/exception
contract. Independent review then selects the smallest concrete cases that cover
changed code. Root separately selects package/source bytes and runtime funding.
The schema agreement permits source-only control authoring under the separate
root selection; this note does not authorize execution.

## Authored minimal controls, not run

`software/v5/release_production/controls.py`, 21,554 bytes, SHA-256
`cdeea379a36329c0b7ac2d640ed4ca49b3586ec2a0c22864270688c1208b5556`.
This source uses `adoption.load`'s real returned `root, pins, roles, descriptor,
manifest_pin, descriptor_pin` and `ProductionError` refusals. No syntax check,
import or test execution has occurred. Independent control review and root's
finite staging/selection remain necessary.

The agreed exact CLI is:

```text
--entry COPIED_RELEASE_OPERATOR --entry-sha256 HASH
--entry-fixtures FROZEN_TYPED_LIFECYCLE_CONTROLS --entry-fixtures-sha256 HASH
--profile STAGED_RELEASE_PROFILE --profile-sha256 HASH
--output EXISTING_FRESH_WRAPPER_OUTPUT
```

The sole fixture dependency is frozen `typed_production/lifecycle_controls.py`,
SHA-256 `21c26ced6138791d978dfddd28d49b5b5599fc2c2ee9abeda7d3a690f05fc1da`.
It is imported as inert helpers only; none of its five test groups executes and
its file is never modified. This avoids another copy of its real-file/fake-owner
framework. Core release tests do not use that fake owner.

Six selected groups now concretize the contract:

1. New entry profile pin/schema, 27-source count and invoked-versus-installed
   entry binding refusals; product import dispatch is forbidden in those cases.
2. Real loader manifest-digest, descriptor-schema, policy and artifact-role
   refusal. Three tiny synthetic roots contain only descriptor/manifest files;
   their rejection must precede any binary read.
3. Real relative traversal/case-alias and loaded-source-origin refusals, with
   temporary module metadata restored.
4. Two narrowly explicit inert adoption results isolate wrong artifact-map
   rejection and cleanup of a returned fake support owner after constructor
   failure. Separate method/domain assertions preserve generic snapshot/request
   inheritance, reject private historical adoption and exclude typed imports.
5. One actual relocated producer construction, profile/closure observation and
   close. Its constructor, loader and support are not doubled. Checks include
   whole-release `_install`, other-component output overlap, exact origins/map,
   64-pin/512MiB bounds, mutable-profile and snapshot-role-map refusal, and real
   calls to all inherited no-override sets. Only public action methods are made
   forbidden to catch accidental dispatch. Small temporary object mutations are
   restored; no selected source or payload is modified.
6. Root's newly selected four-action entry delta uses explicitly inert owners
   for snapshot, request, preflight and run, plus raised/unknown-closure run
   failures and a report path within an explicitly independent fake release root,
   outside its support/source roots and all other pinned-file ancestry. Thus the
   new full-release guard, not an already protected support root, must reject it.
   This independent-review correction was made before any execution. Fake successful run
   counters do not become real host/proof counts. No prior generic five-group
   failure/finalization suite is repeated.

Canonical JSON sorts role names: `guest_image` is visited first. The two tiny
role/path negatives therefore target that role, so they cannot fail earlier
because an unrelated absent binary was accessed. This was identified from source
and corrected before any launch, and independently flagged by launch_review.

The real positive requires the actual staged profile's interpreter, not a
different conveniently available Python: the inherited support owner checks
`sys.executable`. Root plans one complete selected relocated Python subtree;
that is not copied into each negative fixture. The audit monitor permits only
the selected release/interpreter/output roots and exact selected harness/profile
files. Its full bounded trace is saved; it is not a proof of native OS-loader
hermeticity. The result explicitly disclaims complete-distribution validation,
funding and mathematical admission, and claims zero actual snapshot/host/proof
calls only if forbidden-call guards remain untouched and execution actually passes.
