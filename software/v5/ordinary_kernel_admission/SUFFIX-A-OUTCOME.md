# Independent actual suffix A audit

Disposition: **PASS_SELECTED_TWO_BATCH_SUFFIX_A**.

Saved run: `experiments/v5-local-checks/std-kernel-suffix-a01`. Reviewed selection
SHA-256: `d7c7c12a6e17e0aebe1375780b2dd73582d73c3c77f0786e8c8ddf7525cb3611`.
All three current/source-snapshot pairs and all **243 external pins** match.
Saved and original selections agree; outer argv equals the exact selected argv
after prescribed placeholder expansion. Public LAUNCH/SUPERVISION argv agree,
and public RUN equals the JSON returned on outer stdout.

The audit used saved-file reads, hashes and standalone standard-library JSON
comparisons. No product module was imported; no owner/status/database/native or
Git operation was performed. Root retains adoption and any next launch decision.

## Actual checked chain

The public owner returned `ok=true` and BASELINE_INTAKE_COMPLETE, binding:

- PROFILE `60b6e0d6c7d4e7d7761ed5f7ebb2d449afc55547f46f6924f0b93234a5a30f3b`.
- Installation `9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27`.
- Implementation `86b6fcce8d8f13479e8131e1a386782b7bda5b6ee579df46e640ca8005affbea`.
- Store `fb625cc1b7d03d081e45bbcf73f7d59765f04a64a402484f23d00ac3e60ce4e7`.
- Selected parent `c3d0f6209f42abdc98a6975a358545b0d61701e849b6ed0a3e69bdc1b7f400f6`.
- Part A manifest `9eee85273f5fcbc0b91f9f0975c10bfad557b6cb555d334e580499fdf0fedb9c`.

The exact catalog/custody paths and unchanged catalog/custody quotas match the
selection. There are two CHECKED batch results:

| Batch | Whole units | Inert input bytes | New names | Returned local root |
|---:|---:|---:|---:|---|
| 0 | 620 | 8,552,756 | 624 | `9592c3cff8e0066c10d858a0adf72b9d95ef22bd697a1d0aeba4d4763d591c9d` |
| 1 | 404 | 8,595,160 | 406 | `674e33cbe441566ea8385e3bb6011b9f2cecaae4b587b50645c975e48c27c95b` |

Every one of the 1,024 selected inert files matches its manifest length, raw
hash and independently recomputed V2 unit identity. For each batch, the native
projected unit payload multiset equals the selected inert payload multiset
exactly. The projection uses dependency order, which need not equal manifest
row order. In that actual order, every output name matches the worker report.

Using the existing domain-separated identity formulas in standalone audit code,
the actual projected unit IDs give batch request hashes
`4b2d61dfbae9a571c806a2e4d3e8c0b99545a4d73d71cbad7d04c319a2bdc232`
and `501dacb798dd10a73fe8efe152290f27c0a6961c8668e2a10c8023739b5c5692`.
The selected implementation/store and successive parents independently produce
exactly the two reported roots. Both copied installation descriptors equal the
selected installation bytes. Worker reports have the expected schema, extension
kind, unit count, ordered names, parent module, new module and actual output size.

The first plan restores the adopted basis and prefix. The second restores that
same chain plus the actual first new artifact. Every plan parent-module edge,
basis/root-module binding and artifact size agrees. Existing basis/prefix hashes
remain unchanged. The derived resulting chain has **four modules / 2,773 names /
7,900,096 artifact bytes**; this is a chain sum from the actual events, not a new
status invocation or full database inventory.

## Exact artifacts for a later selection

All paths below are relative to
`experiments/v5-local-checks/std-kernel-catalog01` under the canonical root.

| Batch | Native call directory |
|---:|---|
| 0 | `admission-calls/06e887b21c548b5a3f5332bd33db0e1fd285f9bc8b8584c95f2d12ecf018ebf0` |
| 1 | `admission-calls/69a4250e6688060c078716eb553a8477027227d3ca1080f951e74879f5578d09` |

| Actual artifact path | Bytes | SHA-256 |
|---|---:|---|
| `operations/a0eef708fd11d034016fc2231d5e56c8784b8ad39df675c5e14a99415b4da851/chunk.olean` | 2,331,104 | `41ec2dcb79f902ba46b4e7fe82fc021951ad5ec75e5fc7dd4632689ea2c2cfc5` |
| `operations/8b1a43283e800819bdd240d833c8e0012010adad18360147210980527c00a26f/chunk.olean` | 2,748,840 | `9086d6e0f463505762c8725d3e2fda7827c52ff751ff6f733950ca88495f165a` |

These are the paths supplied to the actual supervised workers, and their sizes
match the returned reports. The second plan explicitly includes the first
artifact; no artifact from the unsuccessful prior second event is substituted.

## Closure, diagnostics and cost

Both native events, the public launcher and the outer runner exit zero and
report COMMAND_EXITED_ZERO_AND_CLOSED, with direct child reaped, Job closed,
zero final active processes, no cleanup errors and no termination request.
All four stderr streams are empty; both native stdout streams are empty.
Public RUN is `ok=true` / CLI_EXITED_ZERO; the owner has no close errors.

| Native batch | Granted CPU seconds | Actual CPU seconds | Actual wall seconds |
|---:|---:|---:|---:|
| 0 | 41 | 24.046875 | 24.6219096 |
| 1 | 40 | 23.34375 | 23.7682896 |

The original 60-CPU per-operation bound and all public/outer limits were
unchanged. Actual grants now accommodate both selected events. This is useful
evidence for the smaller-batch decision, not a matched speedup experiment.

The progress directory `intake-diagnostics/5608843f755e3edce3275042772fcff9`
contains **19 records / 13,512 bytes**, consecutive sequences 0 through 18,
two BATCH_CONFIRMED records and final COMPLETE at the returned second root.
ENTRY has the expected not-yet-validated parent and null manifest hash; subsequent
records bind the selected manifest. COMPLETE reports two confirmed batches,
120 reserved CPU seconds, 47.390625 observed worker CPU and no possible
unreported commit for this successful invocation. The earlier failed intake's
uncertainty flag remains untouched. The known delayed worker accounting in each
immediate confirmation record is settled in subsequent records and COMPLETE.

Whole run wall time is **110.4974515 seconds**. Inclusive outer Job CPU
**107.140625** plus wrapper CPU **1.421875** gives **108.5625 known CPU seconds**.
The public Job 106.6875, owner controller 59.21875 and native 47.390625 figures
are nested observations and must not be charged again. Outer peak aggregate
private commit is 956,452,864 bytes. Fresh init, failed full intake, prefix
status and this suffix total **276.375 known CPU seconds**; earlier historical
routes remain separate retained costs. No failure is refunded or relabeled.

Planning reports zero custody additions because the previous failed batch had
already staged these 1,024 inert objects. The two new native checks still ran;
custody presence did not transfer mathematical acceptance. No ordinary library
registration or peer-transferable warrant is claimed by this operation.

## Evidence bindings and next boundary

| Evidence | SHA-256 |
|---|---|
| Outer RESULT | `b3eead9c03fa242c7106076e5aea9d16f351630921db7a36760b4c728de10481` |
| Owner stdout | `b5380376ebc5dd21f601208dc2b64e669b1cee2544780ba43eef81c828da97fa` |
| Public RUN | `e935be483cb903a2626951f1b0f69a8415f15daa363734976159edc7f18e8d99` |
| Public SUPERVISION | `df7a0836369f821434a57a4f746af0b6bab48dc6c176bb251339e79b237c646e` |
| Batch 0 worker report | `88e41ee7ddbece8be40423d13a1b6a5f9b71723d8930b37d8d8b0eb144aae0f8` |
| Batch 0 supervision | `e7c876630d2789c0b7fb39d498e253b73608b1bec5d8be3cd5012eae8d05a755` |
| Batch 1 worker report | `ca2db2049a663528a9a8a5ea3976f1c2619dba12f9e6c8757ec1da8e7647d08e` |
| Batch 1 supervision | `8ec4130ebd9d69150cfab30be873f4bc3a961044bf87e9893ad36028742b094b` |
| COMPLETE diagnostic | `80d209113cdf37352189ad1f83d524d28a90fb5a56cb8e01e90d94392518b17f` |

This completes the selected part A, not the complete original baseline. The
remaining part B has **603 units** and remains unexecuted by this audit. Root
may adopt the actual final root and two exact artifacts when preparing its
separately reviewed selection. No additional status, larger allowance,
automatic retry, new checker or full v5 completion is implied.
