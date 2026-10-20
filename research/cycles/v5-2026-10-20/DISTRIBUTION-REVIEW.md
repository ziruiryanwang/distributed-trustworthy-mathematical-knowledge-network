# Relocatable distribution: independent review

2026-10-20, `core_release`. Source-only coordination after the independently
audited ordinary remote-use integration. No new run, package, proof, build,
test or Git operation is performed by this reviewer.

## Agreed design boundaries before source review

Use one small standard-library build/verify/public-launch utility, an exact
nested base, selected SDK source map, explicit relative asset roles and an
owner-adopted release-manifest digest. Generate the existing launcher's absolute
plan/profile in a fresh external controls directory; do not modify its fixed
base-manifest pin or import/admission policy.

The ordinary `read`, `serve` and explicitly adopted custom-owner entries should
reduce user setup, not introduce a second workflow DSL or agent planner.
Persistent workspaces, operations, downloaded evidence and TLS secrets remain
outside the immutable installation.

## Source obligations

- The nested base manifest remains exact
  `a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed`.
  Selected base payload bytes must match it. V5 additions belong outside base.
- Validate the complete bounded release/input structure before constructing
  outputs or launching. Reject duplicate/case-aliased, escaping, reserved or
  reparse paths. Each source/asset role must resolve to a selected immutable
  manifest entry, not an arbitrary caller/peer path.
- Rebind preparation host, guest image, native checker, frontend and required
  Lean runtime paths explicitly. The unchanged RuntimeProfile may rebase its
  already-supported base Python and SDK worker/source roles. No unchecked
  string-replacement or inferred directory-wide executable authority.
- Preserve image/foundation/policy/encoding relationships. An exact hash
  identifies bytes; it establishes neither mathematical soundness nor publisher
  identity. Real same-call I/A/native verification remains unchanged.
- Full byte verification belongs at build and explicit verify. Launch may
  validate the complete manifest structure and hash its selected SDK/assets,
  retaining the unchanged base/boot/runtime checks, without rereading all
  unused base payload per operation. State that limited launch-check scope.
- A release digest passed to an already executing script cannot authenticate
  a malicious replacement of that script or Python itself. The bootstrap
  interpreter and distribution utility must already be independently trusted
  or verified by the owner; eventual signed installer/update policy is separate.
- New operational role/profile maps must have no dependency on old project or
  experiment paths after relocation. Historical strings inside immutable base
  documentation are not grounds to rewrite frozen payload.
- Fresh outputs only; no mutation of retained installations, source snapshots,
  existing state or historical evidence. Failure and cleanup uncertainty must
  not be relabeled as release success.

The proposed schema satisfies these boundaries in principle. Product source,
exact payload selection and any later relocation test still need separate
review. Current integration evidence does not itself qualify the distribution
or complete aggregate-certification, growth and public-release obligations.

## Exact-input selector source

Reviewed `select_distribution.py` SHA-256
`bf7d502a4a927139062c4a90a3c82adeeaa2c573a74ed97ed8ef972ae9c4e4f8`:
no source blocker for eventual data-only generation after the distribution
utility's final independently reviewed hash is supplied. No selector was run
by this reviewer.

The exact nine-field input keyset matches the proposed builder contract.
The selector preserves remote-plan `68af5327...`, excludes its one fixture
owner, and checks 102 exact SDK/portable source pins. That map has no additional
test/actual/check/assets fixture entries. It pins the exact base manifest/map
census, exact preparation template and host/image/foundation/policy relations,
six external asset roles and six explicitly enumerated Lean runtime files.
It requires canonical non-reparse source paths, finite file sizes, the separately
reviewed distribution source digest and exclusive fresh JSON output.

The selector intentionally does not verify/copy all nested-base payload files;
that remains the builder's full-file verification obligation. Its original
absolute paths are build inputs only, not installed runtime profile values.
The approximately 526 MB installed footprint is a file-copy/storage matter,
not a reason to reopen proof-generation or RAM experiments.

## Product and changed-boundary control review

Reviewed the complete `software/v5/distribution/distribution.py`, including
the final explicit nested-role substitution and directory-component case
checks. Observed source SHA-256:
`28e1b8f5648894df0eb90a44b38b240988d18797fdb4098ef230f58202bec3a0`.
The source is clear for the selected small controls and eventual file-only
build, provided this exact identity is retained. Source review is not evidence
that an installation or relocated operation succeeded.

The builder preserves the fixed nested base, checks the declared template
relationships, constructs a wholly relative installed profile and performs
streamed copy/readback followed by full selected-file verification. It does not
overwrite an existing installation. Case spelling is checked on each path
component before output construction, including `one/a` versus `One/b`;
file-as-parent conflicts and reserved/escaping paths are rejected.

The public launcher checks the owner-adopted manifest/request, selected payload
map and runtime path. It uses unchanged `client.launch`/`boot`, with the original
wrapper wall/CPU clocks rather than a new allowance. The release-relative
preparation roles match `RuntimeProfile.from_context`'s existing exact rebasing:
base Python/helpers remain in the nested base, external I/A/native/frontend/
image/Lean roles point into installed assets, and SDK worker/source roles are
subsequently rebound to the selected source snapshot. No mathematical owner
or admission rule is replaced.

`run` now replaces only explicit exact singleton markers, recursively, with
deep-copied runtime/foundation bindings. It does not add unrelated top-level
fields to arbitrary owner schemas. Unknown/malformed markers and excessive
nesting refuse. This closes the concrete compatibility issue with the already
frozen remote-check owner; no fixture-specific launcher branch was introduced.
The built-in reader separately injects its expected top-level fields.

The generic manifest validator is a shape/role/pin validator, not an executable
closure theorem: e.g. the synthetic controls' intentionally small source map
is not a runnable SDK. Actual release construction enforces required entries,
the exact selector preserves the established 102-file map, and unchanged
`client.launch`/runtime enforce their own closure. These source and structural
checks are not a security sandbox against arbitrary trusted local owner code.

Reviewed the seven-control suite
`software/v5/distribution/test_distribution.py`, SHA-256
`fd2b57464f92157894aaee46131fd425f75a53b934217a253e366d3118a00db9`.
It checks duplicate/noninteger JSON refusal, relative-path constraints, file/
directory case aliases and bounds, role/policy/pin binding, nonmutating relative
profile materialization, exact nested-role substitution/depth refusal, and
tiny streamed copy/no-overwrite/retained failed bytes. It imports no SDK or
mathematical worker and runs no native checker/proof. No source blocker for
root's once-only 20 CPU-second / 60 wall-second / 128 MiB selection was found.

## Relocation-selector source review

Reviewed `select_relocation.py`, SHA-256
`13929069f1cfc1a358047355dc8414ebbb9120887052df475cede05e38f9517c`.
It is clear for eventual data-only staging after the exact installation is
built and its manifest digest independently adopted. It preserves the existing
102 SDK source identities; stages only the frozen owner and retained packet;
uses fresh, disjoint caller-data/operations/controls siblings; and requests the
two installed roles through explicit nested markers. It neither imports the
product nor launches it, and retained proof bytes are not treated as a prior
acceptance result. The only later runtime boundary selected in principle is
the separately bounded installed-public-entry/relocation check.

## Pre-execution builder snapshot compatibility correction

Before any selected distribution control/build ran, root identified that the
unchanged bounded check runner executes the selected source snapshot, whereas
the builder initially required `distribution_source.path == __file__`.
That unnecessary original-directory equality would reject identical reviewed
code run from the runner's immutable snapshot.

Reviewed the narrow correction, current distribution source SHA-256
`b6d4998462fe0f50d31b7e10f1d039c1bc8b0eef0067e02210fd0bab83ff69e9`.
This supersedes `28e1b8f5...` for the first actual selection. The builder still
validates the original independently adopted `distribution_source` pin and
additionally validates its own executing file against that same byte count and
SHA-256. It copies the original selected source into the installation. It does
not infer authority from newly measured bytes, and has no build-time imports or
executable dependencies relative to the snapshot directory.

The unchanged runner checks its selected original source before snapshotting
and checks the snapshot after execution. The correction therefore permits the
existing bounded runner without adding a second supervisor or adapter. The
installed public launcher's exact origin/runtime checks are unchanged. No
source blocker was found; no execution was performed by this reviewer.

## Actual seven-control audit and exact build clearance

The once-only controls at
`experiments/v5-local-checks/distribution-controls-01` pass their independent
saved-output audit. Plan and retained plan copy both hash to
`b8828e68483c57cbad17b29c88ef80e45afbe471c57312bc227d41385a6b492a`.
All seven named controls ran; zero failures/errors, native calls, proof calls
or SDK imports. Independently rehashed all three original/snapshot source
pairs and all nineteen declared runtime pins; no mismatch. The unchanged
runtime map contains the inert foundation data pin, not a new runtime action.

The child exited zero, the Job reached zero active processes, the direct child
was reaped, the Job closed, and cleanup errors are empty. Known CPU is
0.578125 seconds (0.296875 Job + 0.28125 wrapper), wall 0.6766119003 seconds,
peak Job private commit 22,597,632 bytes. Do not add the nested supervision CPU
observation again. Result SHA-256:
`7515a7aa58dfafe0dd6a775995c418e93cd9dc5341046fa1d1c19eb19d1b0a99`;
inner controls SHA-256:
`f54012d7827a46d8bab7f9497f9ff4002de02588942d963c5c0548cc4febae33`;
stderr SHA-256:
`99b3d4bdfad0fe39510cb5111bcf171ed4f60b8af93450adbb29389b9fd0793e`.
No repeat of these passing controls is required.

The exact 32,182-byte build input is
`experiments/v5-local-checks/distribution-01-input.json`, SHA-256
`cf32059db4f9c6001efe3266ca34127f85b4ee4cd93a4e737c3183e3e2f9e64a`.
Independently rehashed its 117 direct selected pins (102 SDK, six assets, six
Lean files, base manifest, preparation template, distribution source) with
no mismatch. All 102 SDK entries equal the retained remote plan's selection
apart from its excluded owner; the base manifest has exactly 6,652 payload
files totaling 235,662,448 bytes. Full nested payload copying/verification
remains the builder's actual work, not an unperformed audit claim.

Build selection SHA-256
`44eb38b8889b77d9b4f9e86ebf124a2a70aeacff64aa0615a3730d47e6f44fa1`
selects unchanged `Run-V5-Check`, the exact `b6d49984...` builder snapshot,
the exact input above, two sources and nineteen runtime pins, with 60 CPU
seconds / 180 wall seconds / 128 MiB / two processes. The destination
`product-local/v5-distribution-01/Mathematical Commons v5` was absent and its
ordinary parent existed at review. The argv performs only file-only `build`;
no native/proof command or new supervisor is introduced. Cleared for root's
once-only invocation. Actual installation and subsequent public relocation
still require their distinct output reviews.

## Actual file-build outcome: wall limit, installation not accepted

The once-only `distribution-build-01` operation ended at its original
180-second wall limit with `RESOURCE_LIMIT`, exit 1 and empty stdout/stderr.
It did not report successful creation/verification. The Job reached zero active
processes, the direct child was reaped, the Job closed, and cleanup errors
are empty. Known CPU was 43.46875 seconds (42.34375 Job + 1.125 wrapper);
wall 180.0905709001 seconds; peak private commit 38,666,240 bytes.
This is a per-file installation-time failure, not evidence of insufficient RAM.

Independently rehashed the two original/snapshot source pairs, all nineteen
runtime pins and retained plan: unchanged. Terminal result SHA-256:
`33ea8cbbb21e51fc485c9ba7a7f158426c6ae982904a549e9ccecff6d3e42dc9`.

The preserved partial destination contains 6,537 files / 134,253,805 bytes.
There is no `V5-RELEASE.json` and no root-level generated payload. Copying
had reached the nested Python library's `xml/dom/__init__.py`; the complete
base, SDK/assets, release manifest and final verification had not completed.
No installed-map PASS or relocation is possible from these bytes. Do not
resume or overwrite this partial tree, renew its allowance, or repeat the
already passing controls.

Source reasoning identifies repeated canonical/ancestor metadata work per
file as an avoidable cost to examine before any separately selected successor.
This is a prospective optimization hypothesis, not a measured attribution or
permission to weaken per-file identity/copy checks. No additional experiment
or runtime was performed by this reviewer.

The not-yet-used relocation selector now points to the separately selected
successor parent `product-local/v5-distribution-02`, preserving partial `-01`.
Its updated SHA-256 is
`b92a659f9d5cbecf32f8b29518b32747f8e52e6544d4be5cf79026d3073c708e`;
the corresponding corrected `RELOCATION-CHECK.md` is
`c3478ab370277dbfac7dd7d13169fa4e0a582299f89e5afd44fdc039bf090f0f`.
This is a routing-only prospective update, not a new runtime or completion claim.

## Efficient-path successor: source argument before implementation

Root selected a fresh source successor rather than extending the failed build's
wall cap or inspecting RAM. Under the explicitly trusted stable local-filesystem
assumption (no concurrent mutation of adopted directory trees), directory-prefix
validation may be shared within one operation. A validated ordinary canonical
parent plus a lexically confined leaf and current non-reparse regular-file
`lstat` is sufficient for selected-file containment without resolving the whole
ancestry again for every read/hash/copy/readback.

Required preserved boundaries: scope-local directory-only cache; validation
after a newly created directory exists; no cached file freshness, size, hash
or exceptions; unchanged exclusive output creation, per-file identity and
readback; unchanged final bounded census. Scope cleanup must restore/reset
even on failure, and final verification may use a new independent cache.
This is not hostile-filesystem race protection; arbitrary concurrent owner
mutation was not an accepted guarantee of the prior utility either.
The argument supports a small changed-boundary source/control review, not
rerunning the seven unrelated already passing controls. Actual efficient
successor source and outcomes remain unreviewed at this checkpoint.
