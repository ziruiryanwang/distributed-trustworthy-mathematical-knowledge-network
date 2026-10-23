# Ordinary installed API flow: smallest useful integration

Source plan and producer implementation, 2026-10-23. Owner: `ordinary_api_flow`. Canonical root is
`E:\Distributed Trustworthy Mathematical Knowledge Network`. No runtime, build,
test, network service, catalog mutation or acceptance was performed for this
note. Root selected the first producer-stage runner below and owns all runtime
selection. Root separately owns the later B integration; no overlapping edits.

The next workflow is an ordinary owner-written preservation method, found by a
second owner who does not know its theorem ID, independently checked from inert
bytes, retained after the supplier leaves, and used in a new Lean contribution.
The reusable core already exists. Add an orchestration boundary, not another
checker, importer, grant authority or certificate pipeline.

## Selected seams and remaining integration

| Stage | Existing API | Required caller obligation |
|---|---|---|
| Immutable owner support | `NativeInstallation.open(root, manifest_raw, pin, runtime_roots=...)` | Installed core and pinned isolated `-I -S -B` Python; owner-adopted runtime attachments, verified once per process |
| Separate local owners | `OrdinaryStore(..., create=True)` and `OrdinaryAdmission.open(..., create=True)` | Distinct A/B store IDs and catalog/custody directories outside install/runtime trees; one immutable install is shared |
| Fixed starting foundation | `owner.initialize(OperationBudget(...))` | One fresh owner basis each; do not import/replay the 2859-unit development library |
| Local ordinary source | `portable_owner_request.prepare`, two portable Lean wrappers, `portable_candidate.bind_candidate` | Exact protected context lookups and prepared bindings; authoring output remains inert |
| Local contribution | `owner.preflight(root, raw_units, budget=...)`, `owner.admit(root, plan, budget)` | One budget created before preparation; only new complete units; core retains evidence before native promotion |
| Publication | `portable_preview.preview_from_evidence`, `OrdinaryStore.put_preview`, discovery `Store.admit` | Publish a selected checked export; metadata membership alone is not acceptance |
| Unknown-ID search | `SearchSession`, `SearchClient.offer`, `SearchClient.candidates` | Query set before receiving publisher IDs; SID/partition/anchor derived only from authenticated offer; positive records confer no scan coverage |
| Exact acquisition | `OrdinaryAcquisition.preview/locator/evidence` | Explicit bounded calls, exact advertised record/ExportID/name checks; retain inert bytes in B custody |
| Preview selection binding | `portable_preview.resolve(preview_raw, evidence_raw)` | Mandatory after target evidence fetch: adapter `resolve` only binds record to preview, not preview to full evidence |
| Missing unit closure | `B.preflight` missing `(encoded_name, ExportID)` rows | Explicit locator then evidence for each selected missing ID; deduplicate units and keep small aggregate bounds |
| Independent acceptance | `B.admit` | The actual new B native event, not A state, grants B's warrant |
| Supplier-independent use | Stop A provider; cold reopen B custody, rehost exact bytes | Preserve semantic/unit/export identity and byte equality; no native artifacts cross the wire |

`PortableCatalog.context(root)` returns the protected context and its bindings.
There is no separate public point-lookup method: obtain that bounded context once
per stage, then use `bindings.get(ordinary_evidence.name_key(name))`. Do not add
an experiment database reader or rebuild an ID map from claims.

## Concrete small method and discovery choice

The authoring agent supplies
`software/v5/ordinary_lean/examples/PortableMethodProducer.lean`:
`DMKN.PortableMethod.Stable f P := forall x, P x -> P (f x)` and
`DMKN.PortableMethod.stable_compose`, which combines preservation by `f` and `g`.
Its only expected nonfoundation dependency is the new `Stable` definition.
Actual complete units and dependencies must come from the writer, not this
expectation. Unexpected closure stops for a concrete decision; it does not open
another cold whole-library campaign.

A's source request can be basis-only: exact 581 inventory rows, zero selected
groups, and a fixed-basis target such as `Eq` resolved from A's real context.
Replace each full quoted template sentinel exactly once, with bounded Lean
quoted values; save template/specialization pins. No B producer-module import.

B's initial query must not use the newly produced `Stable` ExportID. Preselect
these structural features before reading publisher output:

```json
[
  {"tag":"declaration-kind","value":"theorem"},
  {"tag":"binder-domain-head","head":{"tag":"forallE"}}
]
```

They express an unfamiliar theorem accepting function arguments, not a named
target. Ask the actual provider for an offer, choose the first nonempty partition
from that authenticated offer, request positive candidates, and inspect their
explicit previews. The small selected publication may contain one theorem; this
establishes unknown-ID syntactic retrieval, not broad semantic search quality.
Expected theorem IDs may appear only in outcome assertions after discovery.

Fetch the selected theorem evidence from its advertised locator, bind its exact
preview, and run B preflight with the theorem alone. The concrete discriminator
is a missing `Stable` ExportID resolved through the exact locator route, followed
by evidence acquisition and READY preflight over both complete units. No unit ID
is inferred from an ExportID hash or supplied through the expected-output map.

## Budget and minimal SDK/runner boundary

One parent workflow selection supplies fixed per-stage limits and a hard outer
supervisor envelope. Initialization and each admission have distinct one-use
`OperationBudget`s; that type deliberately permits only one native operation.
For B's receive stage create its admission `OperationBudget` before discovery and
give `OrdinaryBudget` that exact absolute deadline. Prepay the finite search
request/reply cap using `charge_external("formal-search", ...)` before the first
acquisition fetch. Use the same acquisition object/budget across preview, all
missing locators/evidence, and provider changes. No refund/retry/renewal.

`SearchSession` accepts a wall duration rather than an absolute parent deadline.
Cap its duration at the parent's remaining time, wrap the async search/fetch
stage in `asyncio.timeout_at(parent_deadline)`, and check the parent before/after
each action. Do not silently grant a fresh full search duration. Retain search
actual charges separately from the prepaid aggregate ceiling, plus HTTP request
and header bytes. `OperationBudget.check` accounts controller CPU and its own
native worker; the outer supervisor accounts the complete process tree.

The smallest source addition is one data-driven owner runner with explicit
stage functions, importing the existing APIs. Its configuration names immutable
installation manifest/pin and runtime attachments; fresh A/B state roots/IDs;
the owner source template and target names; static query specs; custody/index
quotas; and finite native/search/acquisition limits. Candidate data supplies no
paths, executable code, commands, store IDs or resource increases. Preserve
per-stage outputs and a compact whole-flow report; never write inside old stores.
Avoid a new general SDK until the single actual caller shows a reusable gap.

For a finite first run, allow at most eight acquired units/eight missing IDs,
4 MiB aggregate inert evidence, one provider/one offered snapshot and one
candidate page. Search can reuse the existing 8192-byte offer plus 131072-byte
candidate cap, 32 scanned rows and eight matches. These are proposed ceilings,
not selected runtime allocations. A separate small rehost read can retain the
same unexpired receive budget; if it has expired, report that boundary rather
than replenish it implicitly.

## What to execute next, after root selection

1. Finish/adopt the existing file-only installation and two-wrapper authoring
   support build. Neither requires a new library rebuild or broad test campaign.
2. Exercise installed A initialization, basis-only ordinary source export, exact
   V2 binding and admission of the method. Preserve those outputs; if it fails,
   stop before creating unrelated B native work.
3. Exercise B initialization, actual offer/candidate/preview/evidence/missing-ID
   sequence, independent admission, and A-offline cold B custody/rehosting. This
   combines existing individually qualified boundaries; do not repeat their
   synthetic suites or hostile-control catalogs.
4. With B's acquired checked method as the prepared target, author a small
   successor such as threefold preservation using two applications of
   `stable_compose`; independently admit only new successor units and publish
   the new preview. The method must appear as an exact bound import in the
   successor. If that actual export demands extra library closure, assess it
   before a further native call.

For the B-to-C continuation, leave A stopped while B publishes only its new
successor preview and serves both retained original method units and the new
successor units from one `Provider(index=B_index, ordinary=B_custody)`. C begins
without a target/SID, selects a returned explicit preview through the same
predeclared structural query, and fetches the successor plus its missing exact
imports from B. This directly tests whether the product retains republishable
dependencies instead of merely a usable B snapshot. First keep C a cold inert
custody consumer: that demonstrates offline availability, not C mathematical
acceptance. If root selects the full three-owner mathematical loop, C needs its
own fresh `initialize` and one `admit` of the finite acquired closure; no A/B
snapshots, saved reports or grants may stand in for that C event.

The shortest end-to-end discriminator is A source/admission -> B unknown-ID
search/complete-unit acquisition/admission -> A offline -> B source successor
and publication -> C cold retrieval of the successor and retained imports.
It establishes two actual contributions with independently checked reuse and
third-owner availability. The extended version adds C's independent native
event. Keep these claims separate and expose measured costs for every executed
stage, including both owner initializations and the original authoring step.

The decision-changing result is whether the same stable public APIs support
ordinary contribution, unknown-ID retrieval, explicit small closure, independent
checking, durable custody and downstream authoring at a measured whole cost.
It does not establish worldwide routing, general search relevance, independent
host deployment, useful-growth advantage or complete deployable v5.

## Selected producer runner source

Root selected and this agent authored only
`software/v5/ordinary_lean/run_ordinary_api_producer.py`; initial review cut
`0d69cb2d38a27898f872aa38b1ecc0ed1eec76f3e89348526926050c9aa767e0`.
Independent source review is assigned to `admission_event_audit`. No execution
or source build was performed by this agent. Root reported the separate
file-only installation and two-wrapper build02 are ready.

The CLI requires `--output` (existing selected run directory), `--installation`,
`--manifest-sha256`, `--python-runtime`, `--lean-runtime`, `--support-root`
(selected `software/v5` snapshot), `--helper-paths` (OS-path-separated selected
compiled helper directories), `--template`, `--target`, `--store-id`,
`--wall-seconds`, `--cpu-seconds`, and `--memory-mib`. Optional `--basis-target`
defaults to `Eq`. Use the pinned isolated Python with `-I -S -B` under root's
finite hard outer supervisor. Root pins the runner and complete selected
auxiliary/helper/template support; directory paths are not integrity claims.

The installed `py` directory is imported first and `NativeInstallation.open`
binds the actual loaded core. Auxiliary roots are appended afterwards, with
exact request/binder/custody module path checks. The source creates fresh
`catalog`, `custody`, `owner-request`, `owner-source`, `lean-build` and `evidence`
children; all authored files use exclusive creation and fsync. Existing output
and accepted state are never overwritten. No network provider is started here.

One original parent monotonic deadline and CPU ledger encompass installation
verification, fresh basis, request preparation, supervised authoring, binding,
preflight and final admission. Per-stage `OperationBudget` values spend only
the remaining parent allocation, including the installed supervisor's cleanup
reserve. The fixed internal authoring shim sets only the selected helper paths,
scrubs inherited language paths, invokes the installed Lean once, and never
opens/promotes a catalog. Authoring phase stdout is retained; a nonempty stderr
or unclean child-tree event refuses. A failed later stage preserves any accepted
basis and inert artifacts with an explicit failure record; no retry follows.

`OWNER-STATE.json` is the concise handoff for root's B stage. It contains:

- installation path/pin, implementation/semantic/foundation IDs, A store ID;
- catalog/custody paths and exact quotas, fixed basis root and accepted new root;
- `target = {name, export_id, unit_id}` from the exact newly accepted units;
- `units` with relative retained evidence file, bytes/hash and every output's
  name/ExportID; the same full evidence is durable in ordinary custody;
- request directory/header pin, zero group count and `AUTHORING-INPUTS.json` path.

The state file explicitly says local pointers are not transferable warrants.
`BASIS-RESULT.json`, `AUTHORING-SUPERVISION.json`, `CANDIDATE-BINDING.json`,
`PREFLIGHT.json`, and `CONTRIBUTION-RESULT.json` retain the actual stage boundary.
Root's B reader can cold reopen A custody using the saved configuration,
retrieve the exact target unit, derive the preview and admit it to the real
formal index. B does not need the producer module, source request or A snapshot.
