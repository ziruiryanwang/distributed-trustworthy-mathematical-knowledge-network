# Public investigator path: expressible, with a live-service boundary

2026-10-24. Independent source-only audit by investigator_public_path_audit.
No build,test,network request,native operation,owner-state access or Git mutation.
Only public README,producer contract and selected source interfaces were used;
private experiment selections were not treated as required product inputs.

## Verdict

**The bounded ordinary-project investigator loop is source-expressible.** No
missing public identity or hidden-state operation was found between discovery,
inspection,advisory source lookup,approved native investigation,production,
independent intake and publication. A new generic orchestration/comparison wrapper
is not justified by a missing input. This is an API-composition finding,not a
fresh end-to-end run,turnkey-usability study or final-v5 acceptance.

The material remaining operational restriction is different:the shipped service
holds the same exclusive owner lock needed by local checking/publication. It is
not a continuously updating single-node research service. That restriction is
explicit and safe,not a reason to remove locks without a new concurrency argument.

## Concrete input/output crosswalk

The selected build map uses ordinary_native_package/owner.py and
ordinary_authoring_offers/{peer.py,peer_api.py}. Packaged PRODUCER.md comes from
ordinary_producer_package/README.md. The following uses those actual contracts.

| Transition | Obtainable input | Actual boundary |
|---|---|---|
| Start search | Investigator-selected contacts,TLS policy,formal specs and finite limits | peer_api.find validates contacts/specs; no premise that initial contacts are discovered from nothing |
| Search to preview | find.result.matches rows contain provider,snapshot_id,record | preview requires exactly those fields as selection and rederives the record from fetched bytes |
| Preview to concept inspection | Preview document exposes structured names and ExportIDs in its type bindings | inspect selects provider,name,export_id; gets one exact locator/unit,not ancestry or acceptance |
| Selected export to project lead | Same selected ExportID,plus contact and one-read limits | authoring-offers returns inert repository/commit/module/export-name/toolchain claims |
| Lead to ordinary investigation | Investigator obtains and approves a compatible native project,then builds it normally | Deliberate local retrieval/execution choice; no hint grants safety,correspondence or approval |
| Project to inert outputs | Project search paths/modules and investigator-chosen structured target names | produce-baseline validates explicit approval,produces manifest,units and exact target rows without owner state |
| Output to mathematical warrant | Exact bundle directory/manifest/hash; receiver-selected parent from init/status or earlier actual acceptance | intake-baseline preflights and independently checks batches,returning actual local_root |
| Accepted result to publication | Actual accepted local_root plus produced name/export_id/unit_id target rows | publish checks each target against the selected context and recomputes identity/preview before indexing |
| Publication to availability | Existing index,selected custody,explicit disclosure,TLS and finite lease | serve exposes that selected store; availability after lease or provider loss requires another holder |

These are genuinely obtainable values. Budget,path,index-capacity,disclosure and
execution-policy decisions are operator inputs,not missing values an automatic
helper can infer correctly. Selection of a mathematical question/concept remains
local;none is required as a network acceptance field or global task catalogue.

## Exact source evidence

- peer_api.py:176-198 validates find configuration;240-242 returns the exact
  provider/snapshot/record selection consumed at preview:792-809.
- preview:826-831 returns the actual parsed preview document,not just a success
  flag. inspect:665-756 validates its name/export selection,binds the locator and
  entire inert unit,and keeps dependencies_checked/native_usable false.
- authoring-offers:603-663 is state-free and returns exact-key inert metadata.
  Optional map setup is an operator choice,not required source correctness proof.
- ordinary_native_package/owner.py:285-345 explicitly separates production from
  owner operations. Its local project/name inputs are files selected by the caller;
  required schema and spool rules are in packaged PRODUCER.md.
- ordinary_baseline/baseline_production.py:281-314 exposes the bound target rows,
  semantic ID,manifest SHA and exact output files. The producer's observation
  PRODUCTION.json is deliberately written before the manifest and is not itself
  a completion warrant;retain exact bundle bytes and actual terminal outcome.
- owner.py:510-520 returns initialization basis;status:237-259 supplies basis
  and paged context-root identities without a private database edit by the caller.
- baseline_intake.py:281-318 validates the manifest,uses actual preflight/admit
  calls and reports the confirmed final root. Producer assertions never become
  receiver authority merely because the file is named PRODUCTION.json.
- peer_api.publish:432-463 checks selected root bindings against name/export/unit
  triples and resolves an evidence-derived preview before indexing. Supplying
  target rows from an untrusted source therefore does not bypass acceptance.

A consumer may investigate an explicitly approved native package before inert
intake;its final selected closure still requires independent checking for commons
acceptance. This is not equivalent to safely executing hostile source. Conversely,
mathematical acceptance does not grant source-execution approval retroactively.

## Named live-service obstruction

peer.py:219-224 opens OrdinaryAdmission before serving;263-269 holds that handle
until serving and cleanup return. portable_catalog.py:187-188 obtains the catalog's
nonblocking exclusive Windows byte lock. Thus another supported owner or stateful
peer command using the same catalog cannot successfully open it during that lease.
In particular intake,publish,receive and even status do not concurrently operate
on that catalog while its shipped serve CLI is active.

peer_api.serve:486-493 explicitly requires serialization of both stores;507-511
requires exclusive=true and a lease of at most3600seconds. The README accurately
describes exclusive finite service. Ordinary source editing,Lean investigation,
state-free discovery and owner-free production can continue on separate outputs.
After clean service shutdown,the investigator can admit/publish,then select a new
service lease. The bounded reciprocal workflow therefore remains possible.

What is not established is uninterrupted serving while that same node accumulates
new accepted results. Shorter leases or additional replicas can change the tradeoff,
but no availability bound follows from their mere possibility. Removing the owner
lock would invalidate an explicit existing storage precondition,not merely improve
performance. Role separation should precede any change to acceptance-critical locks.

## Existing SDK rehosting route: no unrelated owner required

The selected source-map names discovery/discovery_store.py (Store:54-116,
admit:213-266),ordinary_authoring_offers/ordinary_acquisition.py (OrdinaryStore:
68-128,put_preview/put_evidence:215-219),and the formal-query ordinary export
adapter. These are shipped source interfaces,not an unshipped experiment script.
An explicitly approved SDK controller can compose them as follows:

1. Load the approved package with profile.load;this verifies installed support
   and runtime bindings but opens no mathematical state (profile.py:155-156).
2. Create a separate OrdinaryStore(root,semantic_id,limits,create=True);put selected
   inert evidence and previews through its public methods. Evidence insertion
   creates exact export locators;none of these operations grants acceptance.
3. Create a separate discovery.Store with OrdinaryExportAdapter(semantic_id),
   admit the exact preview bytes with their expected export IDs,then close it.
   Metadata indexing does not certify the claims or imply complete custody.
4. Call peer_api.serve(loaded,custody,config,allowance) against that existing index,
   under caller-provided exclusive serialization,finite lease/TLS/quotas,protected
   disjoint paths and outer hard containment. Close custody after service cleanup.

serve calls _state(loaded,None,custody) and _index(loaded,None,custody,...):neither
opens an OrdinaryAdmission or catalog. Thus a separate same-PC custody/index
service need not lock or initialize the contributor's catalog,or any unrelated
catalog. It still needs the approved package/runtime installation;it is not yet
a lightweight runtime-free host. Same-PC separation is not failure independence.

This is a composable lower-level SDK path requiring a caller-written controller,
not a shipped custody-only CLI or complete documented operational workflow.
The actual peer.py serve command still requires initialized owner state. Replica
preparation must use selected exact inert bytes,not copy a live SQLite database.
Refresh must respect the replica's own serialization;continuous refresh and repair
are not provided by this composition. Prefer this existing separation boundary
before inventing a new daemon,database,trust mode or relaxed acceptance lock.

## Remaining usability and scope judgments

Current docs and readable SDK contracts make the values expressible;they do not
prove an unfamiliar undergraduate can perform the sequence without assistance.
Structured Lean-name encoding and detailed query/custody/index limits are still
expert-facing. Better examples may be useful,but that is documentation/onboarding
work,not evidence for a missing mathematical or network primitive.

An offer can be false,stale or absent. Exact identity mismatch does not decide
mathematical inequivalence. Missing remote coverage cannot be supplied by a local
wrapper. Cold intake and network-receive caps remain finite and distinct;large
produced bundles need not fit one receive operation. Source/repository availability,
security isolation,independent hosting and growth-cost advantage remain unproved.

**Recommended disposition:** adopt the clean source/API composition after its own
build audit;do not add a generic investigator wrapper now. Preserve the specific
live-service limitation for the next availability/role-separation decision instead
of spending another episode proving the already-supported finite authoring loop.

## Current release workflow: do not revive the parked reference lane

2026-10-24. Source-only follow-up by current_research_path after the standard
authoring-project handoff. No native call, store opening, protected-state read,
network operation, test or Git mutation. Existing saved audit was read as evidence.

**The preserved thin-delta reporting failure is not a current shipped command
failure.** source-map.json:404,411-412 selects ordinary_module_anchor's store,
closure and exporter;442 selects ordinary_native_package/owner.py. Under reference/
only baseline_bundle and baseline_intake are copied (449-450). No ReferenceModule,
reference_store, reference_registration or reference_module role is selected.
The public owner's choices at41-43 omit register-reference/export-reference-delta;
its export-module dispatch at543-551 uses the separate generated-module anchor.
The clean builder/profile contain no hidden reference-delta dispatch. Thus fixing
the parked package would not repair the default investigator distribution.

THIN-DELTA-SOURCE-REVIEW's retained actual audit still establishes a genuine
experimental failure: registration and intake succeeded, native delta construction
and both rereads succeeded, record10a905f4... committed, then its postcommit loader
failed. The wrapper omits the chained inner exception. Source tracing of
reference_store03.py:1150-1163 confirms commit/readback precedes load_delta and
ReferenceCommittedError. Existing CLOSED marking occurs before commit; this is
not a source-supported missing-closure-marker diagnosis. The saved audit supplies
no inner predicate/traceback, so neither a budget explanation nor a semantic bug
is proved. No new recovery call or expensive integration rerun is justified here.

### One actual shipped fix candidate

There is a narrower shared operational blind spot in the current module route:

- ordinary_module_anchor/anchor_store.py:58-64 preserves the exact AnchorID and
  COMMITTED_LOCAL_ANCHOR_REPORTING_FAILED but no bounded inner diagnostic.
- _commit_generated:688-691 wraps any postcommit load exception in that class.
- module_export.py:363-380 serializes the outer type/message and anchor disposition,
  not the chained inner exception. The public owner returns that structured detail.

Therefore a supported caller facing a late budget, integrity or I/O refusal after
commit receives the correct retention disposition but cannot distinguish those
causes from this report. This is a source-established diagnosability limitation,
not evidence that current successful exports are invalid or that this package
has reproduced the old thin-delta failure. Current intake separately retains its
last confirmed root, possible-unreported-commit flag and bounded inner error
(baseline_intake.py:320-330); that path should not be replaced or retested.

The smallest consequential software action, if root selects it, is to retain a
bounded inner error type/message in the existing AnchorCommittedError report and
carry it unchanged through existing public failure reporting. Preserve exact ID,
commit-vs-unknown distinction, no automatic retry, no changed mathematical authority
and all current loader checks. Do not log arbitrary locals, source contents or
full traces. Apply this in a fresh selected successor, not to frozen source bytes.
A native-free injected postcommit loader refusal can test the changed reporting
boundary; a full compiler/export/recovery campaign would add little information.

This is lower priority than any substantive scale or acceptance/security defect
found by parallel review. It is a small current-product repair candidate, not a
reason to promote optional reference materialization, add a generic workflow
wrapper, or claim the real-v5 growth requirement complete. The ordinary-project
concept-development/return sequence remains source-expressible under its existing
approval, compatibility, cost and availability conditions.
