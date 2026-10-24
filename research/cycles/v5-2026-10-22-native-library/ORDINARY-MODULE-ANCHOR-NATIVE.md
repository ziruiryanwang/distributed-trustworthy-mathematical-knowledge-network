# Native local-anchor successor: source checkpoint

2026-10-23, `query_native_boundary`. Selected by
`ORDINARY-MODULE-ANCHOR-IMPLEMENTATION.md`; canonical guard passed. Source only:
no Python/Lean execution, build, test, owner open, experiment or Git operation.
Independent review is requested; no compilation or runtime result is claimed.

## Owned fresh files

| Path below `software/v5/ordinary_module_anchor/` | Bytes | SHA-256 |
|---|---:|---|
| `OrdinaryModule.lean` | 39721 | `aa2093d2cb75636f5ce0c248321b6b06e516a42d67cb2cbbadadd3ec880d8799` |
| `module_worker.py` | 14936 | `7d577ce31e37a07a0ac4868d10da792e4476db4df6ab0492791f9d8434b6247b` |

Derived from frozen `ordinary_module_matching/OrdinaryModule02.lean`
(`45e83c3a2a53cc32968fb0ba187ca39b4b2614884284ee78aa78cf7ff28d2019`)
and `module_worker.py`
(`3872864a27e9fbb12e56eaa2ebabd9299d97a336c5e58840648a86b5c371df18`).
No predecessor, controller, collector, registry or package was edited here.

## Exact caller seam (agreed with root/state author)

Worker has **nine positional arguments** after its filename:

```text
lean source helpers sysroot inventory request anchor_plan output report
```

It calls the existing pinned Lean interpreter sequentially, in the same enclosing
Job and allowance, without a new compiled helper or per-phase allowance:

```text
build sysroot inventory request anchor_plan output pending
reread-private sysroot request anchor_plan output pending
reread-exported sysroot request anchor_plan output pending
```

Request is `DMKN_ORDINARY_MODULE_REQUEST_V2`: the predecessor's eight fields plus
`anchor_id` and `anchor_plan_sha256`. Native validates the labels/shape; the worker
actually hashes the selected plan and requires the request hash to equal it.

Plan is `DMKN_LOCAL_MODULE_ANCHOR_PLAN_V1`, exact fields
`schema, anchor_id, support_id, modules, bindings`. Names are structured Lean
names, including module names and direct imports. Modules are oldest-first:

```text
{anchor_id, module_name, direct_imports, added_names, artifact_parts}
```

Parts are five ordered `{path, bytes, sha256}` rows: `.olean`, `.olean.server`,
`.olean.private`, `.ir.sig`, `.ir`; absolute paths come only from protected owned
records. Bindings are complete unit rows `{unit_id, outputs, realization}`;
outputs are `{name, export_id, kind, level_params, inventory_sha256}`.
Realization is `added` or `installed-singleton-theorem`. The empty cold plan has
empty anchor ID/modules/bindings and the current support ID.

Pending schema: `DMKN_ORDINARY_MODULE_PENDING_V3`.
Pending assurance: `LOCAL_CHECKED_ANCHORED_MODULE_PENDING_REREADS`.
Final schema: `DMKN_ORDINARY_MODULE_OUTPUT_V3`.
Final assurance: `LOCAL_CHECKED_ANCHORED_MODULE_CONTROLLER_BOUND_IDENTITIES`.

Both reports retain all predecessor fields and add exactly:

- `anchor_id`, `anchor_plan_sha256`: echoed selected request/plan bindings.
- `direct_imports`: `[encoded Init]` cold, `[encoded parent module]` warm.
- `anchor_names`: exact ordered flattening of all plan binding output names.

`unit_ids`, inventories, matched/added partitions and checked/matched counts
describe only the supplied residual delta. Targets may be anchored or new.
The controller still validates the complete output, actual event and final pins;
these report strings and the plan are not standalone authority.

## Native changes and retained gates

`readAnchorPlan` bounds chain to 32 modules, map to 1024 whole units/16384 names,
each generated module to 4096 own names/64 MiB, and total parent parts to 256 MiB.
It rejects duplicate IDs/modules/paths/names, malformed five-part groups,
nonsequential direct imports, empty generated modules, conflicting map partitions
and unrecognized output kinds. Every parent file's actual size/type/link count
is checked; cryptographic byte hashes are checked in the worker/controller.

`checkAnchorHeaders` matches actual imported modern headers and exact own-name
censuses against the complete selected chain. `checkAnchorRecords` checks actual
resolved name, safety, kind and ordered universes in both views. Public axiom
records are permitted only for already registered theorem-kind outputs. It does
not re-encode any previous type or proof body: their full correspondence comes
from the prior protected generation event plus exact artifacts/import support.

Initial import is pinned Init or the registered parent with an explicit complete
`ImportArtifacts` map; fallback is only the pinned runtime. No inherited project
search path, plugins, extension loaders or legacy LocalSnapshot anchors.
Allowed decoder names are basis + registered outputs + earlier new outputs.
New outputs colliding with anchored names are refused before classification.
Residual installed-singleton matches retain the predecessor's complete private
inventory and public theorem-interface relation. New units still pass unchanged
`CheckedExtension.checkBatch` separately in private and public environments.

Only genuinely added declarations are written, with the exact selected direct
import. Private and exported fresh-process rereads revalidate parent headers/
record metadata, child headers/census and the entire new matched/added relation.
All-anchored reuse is a controller/registry path: the native worker still refuses
an empty residual and never manufactures an empty module or a reuse receipt.

## Worker integrity and costs

The worker checks input, pending/output and parent pins before/after phases;
every parent byte hash is compared to the bound plan. It also validates report
echoes against that actual plan and publishes final success only after both
fresh rereads. Inputs/outputs/parent files may not alias. Reports remain bounded
at 8 MiB; request and plan are separately bounded at 4 MiB.

One redundant immediately-before-reread `unchanged_inputs()` was removed because
`invoke` performs the identical check immediately before launching that phase;
this avoids hashing all parent parts twice consecutively. No check boundary or
resource allowance was removed. Parent hashing/imports and metadata visits still
scale with the selected chain. No constant-time, memory or measured speedup
claim follows from these source edits.

Independent exact native/worker source review is now clear: the reviewer read
both complete pinned files and found no source blocker. This does not establish
Lean syntax acceptance, actual importer behavior, retained authority correctness
or ordinary use success. Root owns any later package and runtime selection.

## Five-call integration harness (source only)

Root subsequently assigned one small actual-import discriminator. New source:

`software/v5/ordinary_module_anchor_package/native_check.py`

30166 bytes; SHA-256
`92575c61c39a36b7eed94913151ef44cd40112e836cb42dd575b9959f69f3c9b`.

Root caught an unused-source package-census mismatch: this assembler places its
receipt inside the package, whereas the former query assembler put its receipt
outside. The harness now requires `--assembly-sha256`, binds the exact receipt
and its profile/installation/implementation/six-change/one-add map, and includes
it in the exact package census. It does not ignore arbitrary extra files. The
earlier unexecuted `e6fe2c19...` draft was corrected before any selection.

No test, compilation, owner opening, module construction or other runtime was
performed by this author. Independent harness review is requested. This is not
a repetition of the prior query/discovery campaign or cold combined-module run.

The retained synthetic owner is reopened in place at
`experiments/v5-local-checks/ordinary-current-relocated-smoke-01/smoke`.
It already warrants `CommonsPackageExample.applyTwice` (A, a definition) and
`CommonsPackageExample.applyTwice_eq` (B, its theorem). There is no new admission,
source extraction, helper build, peer transfer, certificate or artifact damage.
The current native installation remains exactly `32236aa3...`; all 252 saved
immutable predecessor pins and all selected package/runtime pins are retained.
The sidecar must be absent before this one campaign; an existing sidecar does
not authorize an automatic retry or reset.

Exactly five supervised child calls are selected by the harness, if root later
authorizes them:

1. Cold export A alone; require one fetched/checked unit and one live local
   registration with an exact `Init` import.
2. Warm export B with A's returned AnchorID; require only B's complete exact
   inventory in the request, fetch count one, A's whole unit in the cut, both
   checking views and both fresh rereads, and B's direct import of A. The plan
   must name A's protected owned five-part artifacts, not the output copies.
3. Ordinary fresh Lean consumer imports B using its returned oldest-first owned
   directories and establishes the same polymorphic result by both application
   of B and definitional reduction of A. The source generator is reused from
   the already pinned frozen smoke helper; no helper campaign is called.
4. Reopen the owner and request B using B's AnchorID. Require zero evidence fetches,
   zero native calls, original module/key/directories, only `MODULE.json` in the
   new output, and byte-identical sidecar with exactly two registrations.
5. Reopen with the earlier context that lacks A/B and select B's AnchorID.
   Require `ANCHOR_CURRENT_CONTEXT_MISMATCH` in the anchor phase, no native CPU,
   no accepted result or new output directory, and unchanged successful anchors.

The suggested root-selected CLI supplies `--package`, `--profile-sha256`,
`--assembly-sha256` (the exact newly assembled `ASSEMBLY.json` digest),
`--python-runtime D:\Python314`, the exact `--lean-runtime`, and a fresh
`--output` below `experiments/v5-local-checks` whose parent already exists.
Suggested original inner allowance: `--wall-seconds 240 --cpu-seconds 140
--memory-mib 1536`; this requires a separately selected enclosing finite Job.
Permitted envelopes are 180–260 wall seconds, 100–160 CPU seconds and 256–1536 MiB.
Per-call caps are 90 wall/50 CPU for each module export, 35/10 for the consumer,
and 45/8 for each reopened reuse/refusal. All caps narrow to remaining original
allowance, reserving 20 wall seconds and two controller CPU seconds. Known child
Job CPU is charged once inclusively; unknown CPU charges the full child grant
and stops. No retries or renewed grants; failures/partial output remain retained.

The harness reuses only frozen path/hash/JSON/tree/supervision utilities. It
checks saved context and exact evidence IDs before opening anything, retains
each child's stdout/stderr and whole-tree closure, and saves a final immutable
map and `NATIVE-CHECK-RESULT.json`. A failure calls for saved-file audit, not a
silent repair or relabeled pass. Success would establish this local incremental
boundary only, not cheap cold onboarding, useful-growth benefit or final v5.

## Native01 failed; syntax-only successor (source only)

Root's subsequent native01 attempt failed in its first cold-A call, before any
module or anchor registration. The actual compiler stdout reports two parser
errors in the used `OrdinaryModule.lean`: line449's mixed-layout inner record
and line499's local identifier `matches` (a Lean keyword). This was a source
syntax defect, not a mathematical-refusal result. Original source, package,
operation and all diagnostics remain frozen and failed. The independent reviewer
confirmed all nested Jobs closed cleanly with exit1, no registered records and
no generated module parts.

Root selected a fresh source-only correction, superseding the unexecuted
follow-on architecture-priority assignment until this repair is handed off:

| Fresh path | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/ordinary_module_anchor/OrdinaryModule02.lean` | 39773 | `57c97e06ea1b700106d61e265f6abb4a0707f2f89004e870b60bd54cd981c66c` |
| `software/v5/ordinary_module_anchor_package/native_check02.py` | 31365 | `08bcc96dcbe08cfd8a2d4d25ab17d8d7acd793f4eddcbff877860c6159364d15` |

The Lean successor changes only that inner record to one field per line and
renames the three local `matches` occurrences to `moduleMatches`. A complete
read-only diff confirms no other changes, including no trailing-byte change.
No mathematical rule, declaration validation, import, report or budget changes.
It has not been compiled or executed by this author.

The harness02 preserves the same five calls, source inputs and assertions. It
expects root's separately selected one-payload syntax-successor receipt: 134
payloads, only `module/OrdinaryModule.lean` changed, none added, predecessor profile
`8404d56996180520c88f98f3fec61100809bde59297b983de686fede8958ac93`.
The ordinary logical filename remains unchanged; the source recipe selects
`OrdinaryModule02.lean`.

The original absent-sidecar assertion is replaced only by the audited exact
closed-failure sidecar: no registered records, precisely the retained operation
`f08b3ae81225416bbdbfe37f0ebeeea20e3628cf31696ee558622b2ed6b6733b`, and these files:

| File relative to `catalog/module-anchors-v1` | Bytes | SHA-256 |
|---|---:|---|
| `STORE.json` | 859 | `9a0b4e65b7e05b0d875d64f8b7d17a1519a02631aa4494902359db7299b2b513` |
| `operations/f08b3ae81225416bbdbfe37f0ebeeea20e3628cf31696ee558622b2ed6b6733b/RESERVATION.json` | 1141 | `f35d6f7775c7d583fd53b59216d465db30c018450f5beb610f3c80836a1ae560` |
| `operations/f08b3ae81225416bbdbfe37f0ebeeea20e3628cf31696ee558622b2ed6b6733b/CLOSED.json` | 246 | `707bbda28e33c83cb8cff88e994ebf82708d2f1afd203a5b15a244637c90ee2f` |

These files enter the immutable map and must remain unchanged. The failed
reservation stays counted; neither the harness nor product resumes that old
operation, removes its sidecar or infers authority from a saved PASS. The store's
existing policy permits a clean closed orphan with a former support ID, while
each newly selected export gets a distinct live reservation. No general registry
adoption exception is introduced.

Root owns exact prior-failure preservation, fresh file-only assembly/selection
and any later runtime; the independent reviewer has both successor sources.
This author performed only source/data reads and the two explicitly assigned
fresh-file edits. No syntax-success or successful A/B boundary is predeclared.
