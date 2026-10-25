# B theory return: exact existing-API inputs

2026-10-24, `concept_return_inputs`. Source/input preparation only. No compiler,
owner operation, catalog/custody read, build, experiment or Git mutation was run.
Root owns the separate finite execution selection and adoption.

## Consequential interface, not a smaller substitute

The successful source is `TheoryB02.lean`, SHA-256
`d1397331c7b633fec21558189c2eaa45b76642c49d5ca3f359a01f6e623c5bb4`.
Its logical module remains **TheoryB**. The project config selects that module
with the B02 output directory first and original A output directory second.
No recompilation or generated inert module is needed for this approved-source
production lane. Both roots lie below canonical `experiments/v5-local-checks/`.

Twelve selected names, all in `RepairTheory.ClosureBridge`:

- `follows_iff_swap_le`, `mutual_follows_iff_commute`;
- `pointwise_le_iff_fixed_inclusion`, `same_fixed_same_output`;
- `run_is_least`, `same_constraints_same_run`;
- `installLeft_closure`, `propagateRight_closure`;
- `propagation_follows_installation`, `installation_does_not_follow_propagation`;
- `directed_closures_need_order`, `choices_have_no_common_closure_order`.

These expose the generic order bridge, least-solution/schedule consequences,
nonvacuous Boolean instances, failure of commutation from one-way preservation,
and the impossibility of retrofitting both of A's choices to one common closure
order. Their dependency closure must retain the new structures and computations;
they are not a theorem-count or literature-novelty criterion.

Fresh canonical JSON inputs (no BOM or terminal LF):

| File | SHA-256 |
|---|---|
| `B-EXPORT-PROJECT.json` | `e882c02029e1a4036ac6f02572bd27f022a8c760ac6b3d9629d2ad15c257412f` |
| `B-EXPORT-NAMES.json` | `86e08a1f76a650b19a78d018d65db012224ae3e7f56276ad1988f5c166e0d2a0` |

Both files were created with apply_patch; only their fresh terminal newline was
then removed as formatting, before use. `selected_project` permits 1–16 distinct
Windows roots; these two local absolute roots and one module fit. Both selected
source paths and all original A/B artifacts remain unchanged.

## Exact artifact pins

Retain all 154 runtime pins from A's existing direct export selection, including
its original five A artifacts. Add these five B artifacts for **159 total pins**,
below `Run-V5-Check.py`'s 256-pin ceiling. The A export selection hash is
`2b5887d68dc9df6e3e9d0bd4cb6d61e02405d4b9d5ab7382d7f35fff900872dd`.

| Directory / artifact | Bytes | SHA-256 |
|---|---:|---|
| `concept-theory-b-02/TheoryB.olean` | 81472 | `56b319f0cea8a40f058a662d0f5351f12cd6c29942e9cb298adb6ae3c1135721` |
| `concept-theory-b-02/TheoryB.olean.private` | 73320 | `951c4665d4e1a00c0acd17ded1fe52164376c646514475609ccad354353e3b02` |
| `concept-theory-b-02/TheoryB.olean.server` | 7640 | `950d5e8fbdb3e7b891669a6fd9fa698d36cc7505a05d488b693928026fc35ff2` |
| `concept-theory-b-02/TheoryB.ir` | 7432 | `7babbd92f2e6b8119ed24da6ed775444b027bed422350f943a7a251f2877e2e5` |
| `concept-theory-b-02/TheoryB.ir.sig` | 176 | `48f2cb021c840b3170bdc59f147f6bc3ba63046bd541e2c57d8e1df5b732d31c` |
| `concept-theory-a-01/TheoryA.olean` | 95824 | `adf357fc56674de3a766a583f401d4daa0e935a60439943f375d9ef8926e3a10` |
| `concept-theory-a-01/TheoryA.olean.private` | 58056 | `e3382acd89f5df5765bb5264ade3e70264b9479326e4c732886b0285a859ca77` |
| `concept-theory-a-01/TheoryA.olean.server` | 7840 | `eb1d5bdd8dcff55fb743412ac9296fa1c1a4a26f097d2d3c8139dbf9b085a998` |
| `concept-theory-a-01/TheoryA.ir` | 11376 | `00fd1b4ca1597e3ce9db16e5a15305228efcfffa191a36883240d6a6bd2c6ea0` |
| `concept-theory-a-01/TheoryA.ir.sig` | 176 | `e9af2a83203ae52db06f3ab7cc1372b2b5f9db05df6d1e86a7b3381b389ec695` |

These pins supplement the approved local project boundary; they do not census
all transitive Init artifacts or establish a sandbox for arbitrary `.olean`
deserialization. The export is intentionally approved-native, not hostile-input.

## Minimal next public operations

Use unchanged native-src01 package PROFILE
`fc45893cef624978f0ab5212d0e1e172ff7c71f821124daa8751727bf7123ef6`.

1. Fresh direct `produce-baseline`: use A export's unchanged entry/flags and
   allowances, replacing only source/config paths and their hashes with the B
   inputs above and choosing a fresh run/output. Preserve `--approve-local-project`
   and `--spool-mib 144`; inner 120 wall / 90 CPU / 1536 MiB and outer 150 wall /
   120 CPU / 1792 MiB / six processes. Snapshot the new configs and actual B02
   source, retain original A artifact pins, and add the B artifact pins above.
2. Inspect its actual returned manifest, selected targets and whole units before
   intake. Count exact unit-ID overlap with A's accepted manifest; name matching
   is insufficient. Do not claim export success is acceptance. If production
   refuses a real declaration, preserve that result rather than weakening B.
3. Only if actual metadata fits, call existing `intake-baseline` once using the
   existing recipient at `concept-recipient-init-01/{catalog,custody}`, store ID
   `dbaa21256e87cbbf12e1694e183b8d3d25c290af9c73da54395fa4e3923f6b09`, and **A's
   actual accepted parent**
   `3edb83787b85ccd2dfdb0c796c8c6636a0fa3dc671530fae6e14594cad0b0da0`.
   Select the actual B bundle directory, actual manifest path and actual manifest
   SHA, not an anticipated identity. Reuse unchanged CUSTODY-LIMITS.json and
   existing package/runtime pins. No fresh init or registration.

For one manifest batch, corrected A intake02's inner 120 wall / 90 CPU /
1024 MiB and outer 150 wall / 120 CPU / 1280 MiB / six processes are the direct
bounded template. Do not blindly reuse these if the actual manifest requires
more batches: `budget.capacity` reserves 60 CPU seconds **per manifest batch**,
plus controller overhead, even when some units are already present. Inspect
capacity first; no automatic larger allowance or retry is selected here.

## Manifest pinning and mathematical authority are different

The original A intake has 149 package/runtime pins, one manifest and 66 unit
pins. B may exceed the remaining 106 individual-unit slots under the runner's
256-pin cap. If so, keep all 149 package/runtime pins and pin the **exact actual
manifest**. No product validation is removed. This does not make a manifest a
mathematical warrant:

- `read_manifest` verifies its expected SHA, canonical schema, semantic identity,
  unique units, and each entry's exact raw SHA/length and derived unit path.
- `_read_batch` reads each derived file within its bound; `validate_batch`
  verifies length, raw SHA, parsed evidence identity and all structural ceilings.
- `_plan_all` performs that validation across all batches before admission and
  compares reused IDs against actual local bindings; each batch is reread and
  revalidated immediately before the live `owner.admit` call.
- New mathematical authority comes from successful independent admission, not
  a producer receipt, metadata plan or hash. Existing A authority remains local.

This supports content binding under the existing hash/checker assumptions while
avoiding an unnecessary harness rewrite. Never treat hashes as proof validity,
hide mutable-state costs, or assert that all exported B units are newly checked.

The resulting evidence could establish returned independent intake of an
independently chosen theory extension. It would still not establish cold
inert-module usability, unknown-ID discovery, research acceleration or final v5.

## Root's concrete direct selection reviewed

Read-only comparison of fresh
`experiments/v5-local-checks/concept-theory-b-export-01.selection.json`, SHA-256
`5139da11f32e4d081cf9e5e9b64147ef1cfa0cd9e70ac9d9854d97d9f9caff13`,
finds **no input-selection blocker**. All 154 A runtime entries are preserved
exactly; the five added B entries match actual saved artifacts, for 159 pins.
All four source snapshots match current exact bytes: runner, B project config,
B names config and B02 source. Original A source is not recompiled or read by
this command; its five compiled artifacts are pinned and reused. The unchanged
outer limits and intended inner limits/spool match the bounded plan above.
The selected logical TheoryB/project paths and twelve names are correct.
This is a source/input review, not a production outcome or an independent audit
of the selected mathematical content. Runtime remains root's responsibility.
