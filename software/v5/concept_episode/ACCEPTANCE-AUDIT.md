# Concept episode: saved acceptance evidence

2026-10-24, `thin_delta_audit`. Scope: the completed recipient initialization,
both A intakes, and B's retained compilation outcomes. **PASS for the reported
fresh local basis and corrected 66-unit A intake, with the failed first intake
preserved.** B's compiled source is not thereby independently accepted.

The canonical guard passed. This audit reads saved selections, source snapshots,
public command outputs, outer supervisor results and selected installed source.
It does not execute/import project code, call an owner/store API, inspect or
reconcile mutable catalog/custody state, rerun checking, contact B, alter Git,
or repeat the separate mathematical-content review. Hence it confirms the saved
operation boundary, not a separate later readback of persisted state.

## Selections and unchanged input identity

Each retained `selection.json` hashes to its own `RESULT.json` selection binding:

| Operation | Selection SHA-256 |
|---|---|
| `concept-recipient-init-01` | `290211c51062501bbfb074cc06138aa4ea64dce1b81989b008c53873de6ef350` |
| `concept-theory-a-intake-01` | `bf5f151e7f5f7f9f478ec3546cfaa05adf740b4fb9de0bc56ea78e4bf6e97ab2` |
| `concept-theory-a-intake-02` | `e7d48519d75a7e5fadab88afd3676bc2187867beac690046b7dfa54f2879b5a0` |
| `concept-theory-b-01` | `008e85620dcdcc1d4f133b6150802c588943285804ffd382281d59c61260e3a2` |
| `concept-theory-b-02` | `6c0dae2fb805a6e887916a62a388b8e57931342e1c68f78b8bc2dd3d7f5ed27d` |

All selected source snapshot hashes match. Both intakes have identical 216-entry
runtime/input maps. Their command argument arrays differ only at the total inner
wall and CPU allowances, 90/60 to 120/90 seconds; the fresh output/snapshot roots
are resolved separately by the runner. Their outer allowances change from
120/90 to 150/120 seconds. Inner/outer memory remain 1,024/1,280 MiB and the
outer process cap remains six. No product checker limit or mathematical input
changed to obtain the pass.

All 66 unit-file pins in the intake map agree with the previously audited
production manifest, whose identity is
`324c8a04fe7a31cd0ee3a3cba0421014f5a5136593c26bcefa65ee2e0ad36e07`.
The independent raw-byte/domain-identity audit is retained in
[EXCHANGE-ROUTE.md](EXCHANGE-ROUTE.md#independent-actual-export-audit); it is not
repeated here. The selected native-src01 PROFILE remains
`fc45893cef624978f0ab5212d0e1e172ff7c71f821124daa8751727bf7123ef6`.
The shared custody-limits snapshot is
`abf5b2dc515a06691194c47e7a320a7fdeaedbbaa18ec45e074807649968ecbe`:
16,384 database pages, 4,096 exports, 134,217,728 logical bytes and 512 objects.

## Fresh recipient and the preserved first refusal

`concept-recipient-init-01` returned `INITIALIZED_LOCAL_OWNER`; its basis result
is `CHECKED`, with 456 units checked at local root
`b0851e46d05bffc3ad289ca9d1c731940265ca9c5eca4856aa580f5d6cb8ffd3`.
The selected store ID is
`dbaa21256e87cbbf12e1694e183b8d3d25c290af9c73da54395fa4e3923f6b09`.
The public result identifies the fresh catalog/custody paths underneath this
recipient run. A successful native basis initialization is separate from A's
production and later intake; it is not free preprocessing in the cost account.

`concept-theory-a-intake-01` **failed**, exit one, with
`BASELINE_AGGREGATE_CPU_RESERVATION` in `METADATA_PREFLIGHT`. Its public output
records the selected basis as validated, the same last confirmed root, no
accepted result, no batch observations, no failed batch index, zero native CPU
reservation and zero observed worker CPU. `possible_unreported_commit` is false.
This is not a mathematical rejection of A and is not a successful intake.

The refusal has a direct source explanation. Installed
`reference/baseline_intake.py` sets `CallLimits.cpu_seconds = 60` (line 30).
`IntakeBudget.capacity` requires

\[
C_{\mathrm{controller\ elapsed}}+C_{\mathrm{already\ reserved}}
+n_{\mathrm{batches}}C_{\mathrm{per\ batch}} < C_{\mathrm{total}}.
\]

The first total allowance was exactly 60 seconds for one batch, so it could not
satisfy the strict inequality even with zero controller work. The metadata plan
calls this check at line 245; per-batch operation creation and `owner.admit`
occur later (lines 293 and 299). Saved zero reservations and no possible commit
therefore agree with the code boundary; they are not inferred merely from a zero
partial CPU observation. The root-selected fresh invocation repairs an allowance
mistake, not a measured need for 60 seconds of mathematical checking.

## Corrected A intake: what is accepted

`concept-theory-a-intake-02` returned `BASELINE_INTAKE_COMPLETE` with one actual
batch observation: `CHECKED`, **66 units**, local root
`3edb83787b85ccd2dfdb0c796c8c6636a0fa3dc671530fae6e14594cad0b0da0`.
It selects the same actual initialized basis and the exact A manifest above.
Its planning record has 66 new units / zero reused units, 78 names, 430,438 unit
bytes, 480 edges and 10,181 nodes. Planned custody additions are 66 objects,
78 exports and 475,461 logical bytes. Planning alone is expressly not a warrant;
the successful live batch observation is the acceptance evidence.

Installed intake source obtains each observation from the live `owner.admit`
result and checks its returned status; it does not accept the producer's success
receipt as mathematical authority. This separates A's prior
`PRODUCED_INERT_BASELINE_NOT_ACCEPTED` from the actual local checking boundary.
The assurance remains conditional on the selected runtime/checker and its local
acceptance relation; this audit does not independently prove their correctness.

The terminal output expressly says `ordinary_library_registered: false` and
`peer_transferable_warrant: false`. The established capability is local acceptance
of the exported A proof/definition closure. It is **not** a generated ordinary
module, rich frontend reconstruction, cold no-producer-code B development,
cryptographic certification, network transfer, discovery result, or evidence
that the previously identified Option/Prod module collision has been fixed.

## B compilation: a separate approved-source lane

The first B source, SHA-256
`bf3b0947459feca323403ea4e1263133efd5ab6a53eb69f44d6ebf9dd0fea54e`,
failed at line 69 with one retained type mismatch. Lean reported that `h x`
has type `o.le (r.apply x) (s.apply x)` but the rewritten goal expected
`o.le (r.apply (s.apply x)) (s.apply x)`. Both the failed source and failed
operation remain evidence; no successful compilation is attributed to them.

The selected `TheoryB02.lean`, SHA-256
`d1397331c7b633fec21558189c2eaa45b76642c49d5ca3f359a01f6e623c5bb4`,
uses the explicit equality motive at that point. `concept-theory-b-02` returned
zero with empty diagnostics and retained the five ordinary TheoryB artifacts.
Its `.olean` is 81,472 bytes, SHA-256
`56b319f0cea8a40f058a662d0f5351f12cd6c29942e9cb298adb6ae3c1135721`.

Both runs use the same B-SETUP SHA
`f21b196eb391cdc9192e836063800da1c4b512b86a7f0ab016487a79bac8fbd3`,
which maps `TheoryA` directly to A's original approved compiled artifacts.
They do not import a module generated from A's accepted inert closure. This
establishes successful ordinary approved-source extension after a preserved
correction, not independent acceptance of B's new work. B export/intake is a
separate prospective boundary; no outcome is claimed here. Mathematical-content
assessment belongs to [CONTENT-AUDIT.md](CONTENT-AUDIT.md), not this audit.

## Costs and process closure

The following are saved outer measurements. Observed CPU is whole child Job CPU
plus separate runner CPU; it includes internal native/controller work without
adding those nested observations again.

| Run | Outcome | Outer wall seconds | Child Job CPU | Separate runner CPU | Nonduplicated observed CPU |
|---|---|---:|---:|---:|---:|
| Recipient init01 | Success | 18.939097 | 17.046875 | 0.703125 | 17.750000 |
| A intake01 | Preflight refusal | 2.185486 | 1.531250 | 0.531250 | 2.062500 |
| A intake02 | Checked 66 units | 6.519273 | 5.593750 | 0.656250 | 6.250000 |
| B compile01 | Type mismatch | 1.096866 | 0.593750 | 0.375000 | 0.968750 |
| B compile02 | Success | 1.038792 | 0.593750 | 0.359375 | 0.953125 |

Recipient init and both A intakes together cost 27.643855 seconds summed outer
elapsed and 26.062500 observed CPU seconds. The failed first intake is included.
This subtotal excludes A/B investigation, A compilation/production, B compilation
and any later B export/intake; it is not a full-cost growth comparison.

A intake02 reports a 60-second reservation but only 2.328125 observed native
worker CPU seconds. Its own worker accounting is explicitly partial; use the
outer whole-job measurement for the observed total, and do not treat the unused
reservation as measured work or an automatic budget refund.

All five saved outer results report direct child reaped, Job closed, zero final
active processes, no cleanup error and no termination request. The two failures
remain nonzero exit outcomes despite clean closure. Peak outer Job private commit
was 691,089,408 bytes for init, 33,751,040 for intake01 and 666,177,536 for intake02.
These measurements provide a bounded implementation fact, not a hostile-input
sandbox proof, sustained growth benefit, large-network qualification or final v5.

## B export and independent return intake

2026-10-24, `thin_delta_audit`, saved-output **PASS** for the newly completed
boundary. This supersedes only the earlier prospective status of B export/intake;
the earlier failures and approved-source/inert-module distinction remain intact.
Canonical guard passed. No project code execution/import, native call, owner API,
mutable state readback, mathematics reaudit, Git action or repeated experiment.

Both actual selection hashes match their terminal `RESULT.json` bindings:

- `concept-theory-b-export-01`:
  `bb8bc9baa2e60e57c9af9fad1a3757e337f5812bedf72437a0ad82a9c9958a32`.
- `concept-theory-b-intake-01`:
  `33c62a657bb32aeb28f469215554568aa15bd90bf70b23c3fc1647fd0b93be83`.

All five export source snapshots and both intake snapshots match. The export's
159 pins preserve all 154 A-export pins unchanged and add exactly B02's five
compiled artifacts; all ten selected A/B artifact hashes match actual files.
The B project config is 362 bytes, SHA
`e882c02029e1a4036ac6f02572bd27f022a8c760ac6b3d9629d2ad15c257412f`;
its selected-name config SHA is
`86e08a1f76a650b19a78d018d65db012224ae3e7f56276ad1988f5c166e0d2a0`.
All twelve returned target names match that config and occur in their actual
returned units' inventories. No new compilation of A or B occurred in this export.

The public export result remains `PRODUCED_INERT_BASELINE_NOT_ACCEPTED`,
`mathematical_acceptance: false`, with receiver-relative acquisition fit not yet
established by production alone. Its actual manifest is 18,827 bytes, SHA
`680cd98f8d1d31ef251b1e78b1cdae7a60bbe2b733e95193b0fe52cb9855c302`.
A bounded independent pass verified all **106** actual unit files' lengths,
raw SHA-256 and `DMKN-ORDINARY-EVIDENCE-V2` domain-separated IDs, plus their
bindings in the intake's 256-entry pin map. The manifest and all four production
pins match actual bytes. The new request/writer hashes are respectively
`87aa3b16978acef8332e510b924c87c68d627556674b41519c336a8152493169` and
`a4f344137433b2105217528858b43f6342a0641fb246b1ca20b6b589a776fa6e`;
the inventory pin is unchanged from A's audited export.

The actual closure is **106 units / 122 inventory names / 822,414 unit bytes**:
46 definition descriptors, 53 theorem descriptors and seven inductive groups.
Its public census reports 819 edges and 19,745 nodes. The saved spool count
agrees with the terminal output: 117 files / 2,422,536 bytes. Intersecting the
actual A/B manifests gives exactly **39 identical units**, with equal raw hashes
and sizes. The remaining **67** are new relative to A's accepted selection;
they include any newly required dependencies, not necessarily 67 B-authored
results or 67 novel mathematical discoveries.

The intake selects A's actual root
`3edb83787b85ccd2dfdb0c796c8c6636a0fa3dc671530fae6e14594cad0b0da0`
and the exact B manifest above. Its live batch result is **`CHECKED`, 67 units**,
with terminal `BASELINE_INTAKE_COMPLETE` at local root
`03de3aa800949731dfc0823d8661374c9f216262211c9bfe1ac6afd930421e20`.
The planning report's 67 new / 39 reused split agrees with independent manifest
comparison. Planned custody additions are 67 objects, 71 exports and 630,744
logical bytes. The actual admission result, not that plan or producer report,
supports local acceptance; no separate persisted-state readback is claimed.

| New operation | Outer wall seconds | Child Job CPU | Separate runner CPU | Nonduplicated observed CPU |
|---|---:|---:|---:|---:|
| B export01 | 6.713830 | 4.484375 | 0.687500 | 5.171875 |
| B intake01 | 10.547484 | 9.171875 | 0.750000 | 9.921875 |

The new boundary totals 17.261315 summed outer wall seconds and 15.093750
observed CPU seconds. Native export's 1.4375 CPU seconds and intake's partial
2.8125 observed worker CPU seconds are already inside these whole-child charges;
the intake's 60-second reservation is not measured CPU. Peak outer Job private
commit is 503,357,440 / 672,014,336 bytes respectively. Both outer processes
returned zero, reaped their children, closed Jobs, ended with zero active
processes and no cleanup errors or termination requests. Export's retained inner
supervisor also closed cleanly and its phase log reaches `OUTPUT_WRITTEN`.

This establishes a useful additional fact: independently authored B work using
approved A artifacts was exported as inert data and locally admitted over A's
already accepted context, with exact overlap reused. The result still explicitly
has `ordinary_library_registered: false` and `peer_transferable_warrant: false`.
It does not establish publication, unknown-ID discovery, fresh third-party use,
generated-module usability, cryptographic certification, acceleration against an
optimized local baseline, sustained novelty or deployable-v5 completion. Those
limits do not negate the actual A-to-B-to-checked-context contribution boundary.
