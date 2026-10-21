# Consolidated candidate: exact demonstrated source union

2026-10-21, core_release. Source-map checkpoint for
[CONSOLIDATED-CANDIDATE-SELECTION](CONSOLIDATED-CANDIDATE-SELECTION.md).
This records the existing demonstrated components and their composition; it is
not installation, runtime or final-v5 qualification. No product source,
installed state, trust policy or used evidence is changed by this note.

## Exact construction

Let B be the `sdk_sources` mapping in
`experiments/v5-local-checks/distribution-terminal-i-01-input.json`:

- Length: 2,805,479 bytes.
- SHA-256: `d3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0`.
- Census: 114 logical SDK files, comprising 93 `v5/*.py` and 21 portable files.

The candidate U is B with exactly the twelve rows below applied by logical
key. Rows R1-R5 replace existing keys; A1-A7 add previously absent keys. For
every other key k, U[k] = B[k] including physical source path, size and digest.
Thus U contains **121 logical SDK files: 100 v5 Python files and 21 unchanged
portable files**. Exactly 109 basis files are untouched. Resolve modules through
this mapping, not through similarly named physical directories in `software/`.

All physical paths in the table are relative to `software/v5/` under the sole
canonical root `E:\Distributed Trustworthy Mathematical Knowledge Network`.
All twelve physical source lengths/digests were checked in this source review.

| Row | Logical SDK path | Physical source path | Bytes | SHA-256 |
|---|---|---|---:|---|
| R1 | `v5/admission/pin_phase.py` | `standalone_validation/admission/pin_phase.py` | 8677 | `ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881` |
| R2 | `v5/mixed_claims/imports_atomic.py` | `continuing_context/mixed_claims/imports_atomic.py` | 45513 | `45b082863525fb08c1e8925e998113b55deff4b92482c8cf9b63cea2093725ad` |
| R3 | `v5/mixed_claims/receiver.py` | `incremental_native/mixed_claims/receiver.py` | 27837 | `5436569971c272b129fbaec480d51d57a1ec521d43fd4d4ad14133b786691d5b` |
| R4 | `v5/client/workspace_atomic.py` | `continuing_context/client/workspace_atomic.py` | 51319 | `32e3b95ea2e6d3f8dc35d63000728e9e075a16de3e13fb1a0b718bce45e11773` |
| R5 | `v5/discovery/discovery_store.py` | `selective_placement/discovery/discovery_store.py` | 19886 | `1c8543d4903754174b80d107ee923116ddb402d41a3b5af3f1d255abdfc6a328` |
| A1 | `v5/placement/__init__.py` | `selective_placement/placement/__init__.py` | 78 | `8fe08470d7fd15e96d1305f0e49a8b359cb53ce0c542bf7473b68d869159112e` |
| A2 | `v5/placement/codec.py` | `selective_placement/placement/codec.py` | 6363 | `6f32569d4807f96130350b85233161603f6860f082c75f81a8bfacf4f0a58999` |
| A3 | `v5/placement/ledger.py` | `selective_placement/placement/ledger.py` | 12537 | `d955990c347ed466617c752893dded8b8494dd266a050b045352c77c48f21a91` |
| A4 | `v5/placement/controller.py` | `selective_placement/placement/controller.py` | 18192 | `ef1c9b59072127379e955bafeea001a22d6e3d10c9c46dca1304f85ab09e2b49` |
| A5 | `v5/placement/network.py` | `placement_network/placement/network.py` | 31301 | `1ec5c452ec129ae033f0577ebac6223e2cf3192d4724a3d31fe2e5c27a06cd4b` |
| A6 | `v5/placement/advertisement.py` | `retained_advertisement/placement/advertisement.py` | 23256 | `5aa23ee76115355ad319ae4acfd4ab418e010166e53b6ed02c82eb25d34d4510` |
| A7 | `v5/client/serve_placement.py` | `retained_advertisement/client/serve_placement.py` | 22670 | `7e735337d595894e25fd07a8dcc9ad8cd3ba9f1c042ba930684b7798232cb7fa` |

This exact union matches root's
`Select-ConsolidatedDistribution01.ps1`, SHA-256
`497cff81294e8f709996ba8332b33eb8c283244a153289b336565cf4af7daf38`.
The selector separately requires the independent composition review before
creating a fresh immutable input/selection. It does not itself execute a build.
No second manifest or parallel installation is selected by this note.

## Deliberate overlap resolution

The sharing workload's `software/v5/sharing_margin/actual.py::REPLACEMENTS`
selects precisely R1-R4. Placement and retained-advertisement maps agree on
R1/R3. The remaining overlaps are resolved by their reviewed successor chains,
not by arbitrary overlay order:

- **Atomic import:** continuing-context R2 supersedes the older
  `standalone_validation/mixed_claims/imports_atomic.py` (`8a831337...`). It
  retains that selected standalone-validation basis and adds `begin_extension`.
  Applying the older placement map after sharing must not downgrade R2.
- **Atomic workspace:** R4 derives from the conjunction-index atomic workspace
  (`eea95...`) and adds `advance_context`; its sealed-view requirements remain.
  This is the continuing workspace already exercised by the sharing workload,
  not a newly invented continuation layer.
- **Discovery storage:** R5 derives from the instantiation Store (`32df0...`).
  Its added optional keyword-only `before_commit` callback runs before fresh
  and duplicate COMMIT. Existing continuing-client calls omit it, preserving
  the prior behavior and storage schemas. Placement can use the callback at
  its existing atomic publication boundary.
- **Placement service:** retained A7 supersedes service02 (`319ddf07...`),
  retaining its shutdown repair and adding ownership/tracking of the retained
  advertisement task. Install A7, not the older service at the same logical key.
- **Advertisement:** retained A6 supersedes `b552...`, keeping the route schemas,
  ledger and controller while adding owner-only restoration by an explicit
  original request ID. Restoration republishes an advisory route, not a new
  mathematical acceptance or transferable trust warrant.

The same-owner exact-witness native reuse mechanism is already R3. Its
successful M then M+V integration is existing evidence; another cache module or
cache experiment would duplicate work. No restricted-composition/typed guest
profile is added. No saved owner state, warrant or trust authority is transferred.

## Portable contracts used by the installed smoke

These are unchanged B rows, not additions. Their installed logical namespace is
**`portable/location/`**, not `location/`. Physical paths remain relative to
`software/v5/`.

| Logical SDK path | Physical source path | Bytes | SHA-256 |
|---|---|---:|---|
| `portable/location/controller_services.py` | `body_location/portable/location/controller_services.py` | 5854 | `eeb82d5dd6fe34915d07b2927e7ddd44ee2b5b80278dbf4d2889b87222ad1501` |
| `portable/location/observed_route.py` | `portable_runtime/location/observed_route.py` | 3591 | `9800b5fd3a1f922dcc2e59818916b2333f79004b7f4b6ed42eb89d40891740f1` |
| `portable/location/available_descriptor.py` | `portable_runtime/location/available_descriptor.py` | 3224 | `d3b215f59c0b4745562fdc76339a53f22d0fa009932dfecbef4fecfff6743fba` |
| `portable/location/node_entry_services.mjs` | `body_location/portable/location/node_entry_services.mjs` | 10492 | `7efae4a2be0de16d20f9d8f334e514a8a042798aee61f3c0e70b093904944205` |

The existing directory builder is `software/v5/body_location/distribution.py`,
SHA-256 `eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813`.
Its existing namespace/census interface admits this proposed map; no builder
rewrite is indicated. The independent reviewer owns the complete builder and
preparation-cap compatibility assessment. Root owns the sole fresh destination:
`product-local/v5-distribution-consolidated-01/Mathematical Commons v5`.
Existing distributions and their state must remain untouched.

## Evidence reused, not rerun

All following files are in this cycle. Their claims remain scoped exactly as
recorded in the adopted outcomes; their conjunction alone is not a claim that
the new installed union has executed.

| Existing outcome | SHA-256 | Relevant established boundary |
|---|---|---|
| `INCREMENTAL-NATIVE-INTEGRATION02-OUTCOME.md` | `779fa9f3b9cfbdd93fa289fe990543d4927176d85375ce3da8c997199fd96124` | Actual same-owner M then M+V, exact native-prefix reuse. |
| `CONTINUING-CONTEXT-OUTCOME.md` | `9f9b373720a6aa260e343fce107532ae26e9d36f464abc1269bc88600e578575` | Nine focused continuing-context controls. |
| `SHARING-MARGIN-OUTCOME.md` | `77529a968af14cd1dc82ceb389b47181baa0ada3fdd2fa582f56b9f0c58cc475` | Actual R1-R4 union, genuine same READY mathematics and local advancement; one observed CPU comparison, not universal growth. |
| `PLACEMENT-NETWORK-INTEGRATION02-OUTCOME.md` | `e1771fe06e945c67431b6357d38181d1869acd132951f0629b53307f229441d7` | Actual remote placement, source-offline discovery and genuine received-I admission with service02. |
| `RETAINED-ADVERTISEMENT-OUTCOME.md` | `7895dcad623a159cc2827e688c4e55c02a31643b9ca98fef24ac93642e8b6f55` | Nine focused retained-advertisement controls with 121 staged SDK files; not actual restarted networking. |

## The genuinely new installed boundary

The already selected `RETAINED-ADVERTISEMENT-INTEGRATION-PLAN.md` supplies one
remaining composition test. Execute it once against the new installed candidate,
not once as an overlay and again after installation:

1. Use a fresh prospective generation permitting two runs. Keep B's workspace,
   configuration and read endpoint unchanged across its close/reopen.
2. Stop A; seal and completely close B1. Reopen B2 with fresh locator identity
   and locator state, retaining the same sealed generation.
3. Call `advertise_retained(original_request_id)` through the public owner
   boundary. This restores only an advisory route for retained exact custody.
4. Give the reader only formal goal, policy, locator and budget, never known
   answer IDs. Allow bounded alternatives for typed stale-peer unavailability.
5. Keep the existing aggregate bound: one observed route (peer cap two), at most
   two available-descriptor calls and four search calls prepay seven requests;
   acquisition limit twelve leaves five for the three selected reads.

Do not force a stale-peer scenario if it is not naturally observed; report the
actual coverage. This smoke performs zero proof generation, native checking,
verifier invocation or trust adoption. Prior genuine admission evidence is
reused without pretending that the new smoke repeats admission. Independent
installed-map and actual-outcome review still follow root's finite launches.
The full deployable-v5 objective remains open.
