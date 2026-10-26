# Coherent workflow source-bundle test plan

2026-10-26. Owner: `service_plan_tests`. Source preparation only; root must select
the final reviewed source pins, input paths and one fresh finite output before
any imports, packing, extraction or test execution. No native/network operation
is part of this gate. This is a distribution-integrity and usability-closure
check, not a new mathematical qualification or complete-v5 claim.

## Minimum decision-changing evidence

One actual source pack and relocation should establish that the distribution is
exactly the approved base plus explicitly selected companions/guides, not an
unreviewed repository snapshot. The full enlarged-root verifier must succeed
from the relocated tree. Current operational links/commands must resolve within
that tree or explicitly identify a later built package; historical evidence
references are not executable dependencies.

The test source is now complete and awaiting independent source review. Its
public CLI is `--source`, `--source-sha256`, `--source-root`, `--base-archive` and
`--output`; `--source-root` may be root's exact mirrored finite snapshot rather
than the live repository. Every spawned command still uses canonical cwd.

Selected distinct checks:

1. Verify the externally pinned approved base ZIP/manifest association, then
   obtain one actual new archive and retained receipt through the public pack
   CLI. Independently inspect every ZIP member, fixed metadata, complete manifest
   and source map. Compare all 143 original payload bytes exactly against the
   approved base and every new payload against its explicit source mapping.
2. Extract once to a fresh unrelated destination using a bounded test-owned
   extractor with an exact allowlist; execute the new relocated public verifier
   with the externally selected union-manifest hash. Independently census every
   file/directory before and after; no generated cache or undeclared file may be
   smuggled into the source closure. No base/native build is repeated.
3. Check the authoritative start guide and selected operational companion guides:
   inline local Markdown file links resolve inside the delivered tree; source
   command entry paths
   identify delivered source or explicitly later-built package outputs; source
   utilities are byte-identical to their approved source. This bounded checker
   covers six current guides, declared manifest entrypoints and explicit
   `software/v5/...py` command paths; anchors and general prose remain source-
   review obligations. There is no companion `--help` call: that would not
   exercise its deferred adjacent import, and its real closure was already tested.
   No service, custody access, native initialization or networking.
4. Target only new union-boundary refusals: wrong base association/projection,
   missing/extra companion role or changed companion byte, conflicting manifest
   selection, extra root member and old manifest hash's unsuitability for the union.
   Prefer pure validator mutations for shape/binding cases, with at most one
   preserved fresh bad extraction for the exact-census boundary. Do not rerun
   old relative-path/ZIP traversal/hash primitive suites.
5. Two tiny fresh bootstrap layouts contain the exact new utility plus an
   intentionally wrong-length or wrong-hash old helper. The helper must be
   refused before execution. A harmless assertion sentinel would fail the test
   if it were wrongly executed. Neither layout is a full archive copy or changes
   the real approved helper.

## Required input pins

The retained base archive is
`experiments/v5-local-checks/transport-release-handoff01/suite/packed/source.zip`:

- ZIP SHA-256: `897a6eb57056b911b200551413c65ce7788ba3d448ff8b6b8c143d883180ebd0`.
- Base manifest SHA-256:
  `f1beab01d43e4b5fc6d7b9999ff2795598e3f2ee77c0dc85f1d99e82a15b31f1`.
- Approved old utility SHA-256:
  `5a8742bec0c13f3c7e8104111ba883887d5569cbb1a5498d79567e998dcd4d32`.

Root additionally pins the new test, this plan, new bundle utility, all selected
distribution-specific guides and the three unchanged companion code files.
The finite pack snapshot includes all 143 original payload paths plus these ten
destination-to-source mappings (paths are relative to that selected source root):

| Archive destination | Selected source |
|---|---|
| `software/v5/ordinary_selected_export/export.py` | Same path |
| `software/v5/ordinary_selected_export/selected_export.py` | Same path |
| `software/v5/ordinary_selected_export/README.md` | `software/v5/ordinary_workflow_bundle/guides/SELECTED-EXPORT.md` |
| `software/v5/ordinary_selected_export/INTAKE.md` | Same path |
| `software/v5/ordinary_reuse_workflow/README.md` | Same path |
| `software/v5/UPDATE-AND-RECOVERY.md` | `software/v5/ordinary_workflow_bundle/guides/UPDATE-AND-RECOVERY.md` |
| `software/v5/ordinary_service_plan/service_plan.py` | Same path |
| `software/v5/ordinary_service_plan/README.md` | `software/v5/ordinary_workflow_bundle/guides/SERVICE-PLAN.md` |
| `software/v5/ordinary_workflow_bundle/bundle.py` | Same path |
| `START-HERE.md` | `software/v5/ordinary_workflow_bundle/README.md` |

Only three guide variants are new; intake and reuse remain byte-identical.
The test, plan and outer runner are additional test-only selected inputs, never
archive members. The exact old utility remains at its original relative snapshot
path because the new utility locates it from its own `__file__` ancestry. A
snapshot containing only the new utility would not supply that required closure.
There is no wildcard input discovery or live-repository source dependency.
The Python runtime executable/support is selected by root's ordinary outer Job.
No Lean installation or generated package attachment is needed for file-only
pack/verify; mere references in shipped build instructions are not executed.

## Preservation and proposed resource shape

Use one root-selected fresh evidence parent for the pack output, relocated tree,
small negative fixture and raw child stdout/stderr. Never rewrite the approved
archive, original payloads, used source, owner state or retained failures. Test
mutations create fresh synthetic documents/copies only. No recursive cleanup,
restore, overwrite or retry follows failure.

Root proposes one outer Job with 120 wall seconds, 60 inclusive Job CPU seconds,
384 MiB simultaneous commitment, four active processes and bounded 4 MiB stdout /
1 MiB stderr. The test's cooperative envelope is 110 wall / 45 controller CPU
seconds; every child is bounded by the original remaining test horizon. There
are exactly two successful child commands: one public `pack`, one relocated
public `verify`. Changed-boundary negative calls are file-only Python API calls;
they do not start product code or more pack jobs. Nested child CPU is already
included in the outer Job measurement and must not be added twice.

The pack input base manifest is read from the externally pinned approved ZIP
and written once as a fresh small input. No whole base extraction is necessary.
The new output has 154 payloads and 155 ZIP members: original143 + new10 + exact
`BASE-SOURCE-MANIFEST.json`, plus `WORKFLOW-SOURCE-MANIFEST.json`. There is no
old `SOURCE-MANIFEST.json` at the enlarged root. The new utility's explicit APIs
are `pack(source_root, base_manifest, output)` and `verify(root, union_hash)`;
its public CLI mirrors these arguments. The changed manifest controls call
`validate_manifest(base_helper, document, original143)` and preserve all fixture
documents in the test's result records by their named mutation descriptions.

Fresh outputs are `packed/`, `relocated-workflow/`, `extra-member-workflow/`, two
tiny `bootstrap-*` layouts, small base input/result files and per-command raw
stdout/stderr/argv records beneath the selected test output. Only the extra-member
fixture gets an unselected inert text file, before its expected refusal; the
successful relocated tree remains unchanged and is censused again afterwards.
No unnecessary native/package/compiler regression is authorized by this plan.
