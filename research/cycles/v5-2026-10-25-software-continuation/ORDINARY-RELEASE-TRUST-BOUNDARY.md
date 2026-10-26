# Ordinary release: executable trust boundary

2026-10-25. Source-only audit by `concept_software_bridge`; root owns adoption.
No product import, test, build, state access, native execution, network operation,
Git mutation or used-source edit was performed. This is a finite control/data-flow
argument, not a complete parser, runtime-exploit or public-release security audit.

## Decision

The ordinary peer path does **not intentionally execute downloaded Lean source,
peer Python, peer bytecode, peer plugins or peer native `.olean` objects**. It
parses inert mathematical data and, on receive, may execute the owner's fixed
approved checker over that data. I found no concrete reachable contrary path in
the traced dispatch, acquisition, admission, decoder and snapshot pipeline.

A general sandbox for arbitrary hostile Lean/Lake projects is therefore **not a
logical prerequisite for the inert peer protocol** under the assumptions below.
It would be a prerequisite for claiming that arbitrary untrusted projects can
safely execute with access to this user's machine. That is a different facility,
and the current software does not provide it.

This corrects a blanket use of “sandbox missing” as a single undifferentiated
release blocker. It does not say that resource supervision is a sandbox, that
remote bytes cannot expose implementation vulnerabilities, or that all remaining
assurance work is external testing. The trusted implementation and protected
local-state premises still require clear deployment boundaries and scrutiny.

## Exact object reviewed

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
All source references below are relative to the exact package:

`experiments/v5-local-checks/sparse-access-assembly01/assembled/package`.

| Binding | SHA-256 |
|---|---|
| `PROFILE.json`, rehashed in this audit | `97f93cc66f77ebcecd7a3a341baaaf4725236a8dec5fb9cee3c3e67d478f2834` |
| Selected installation manifest | `32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2` |

The independently audited assembly census is 152 files with 117 auxiliary roles.
Its native checker and installation payloads are unchanged by contact/sparse
discovery work. `SPARSE-ASSEMBLY-OUTCOME.md` records the full byte/census argument;
this review does not rerun that assembly or transfer sparse-search evidence into
a claim about native checking.

## Threat model and three different inputs

1. **Untrusted remote protocol data.** A provider may fabricate, omit, corrupt or
   repeatedly offer mathematical candidates. A query result is a claim, not a
   warrant. The receiver need not trust the provider's identity for correctness.
2. **Owner-approved executable project.** An owner can separately select local
   Lean source, imports and compiled project assets. Approval here must mean
   *trusted to execute with the process's actual privileges*, not “interesting
   mathematics,” “worth trying,” or merely “the source hash matches.”
3. **Protected local implementation and state.** The selected Python/Lean
   implementation, runtime libraries, catalog, generated native snapshots and
   state locks are trusted local authority. A hostile same-user process capable
   of changing those bytes or calling private controller methods is outside the
   current acceptance model. Hashes in an equally writable catalog do not remove
   that limitation.

An honest owner may accidentally run malicious source. Such a mistake crosses
boundary 2; this source audit must not silently reclassify it as boundary 1.
Similarly, a parser/runtime exploit would violate the trusted-implementation
premise, not be stopped merely because the transport is called “inert.”

## Finite source argument

| Step | Selected source and actual boundary |
|---|---|
| Bootstrap | `profile.py:175` onward checks the selected local file census/hashes and runtime/profile bindings before importing the owner-selected support modules. `peer_api.py` is loaded from exact approved local source. Loading local authoring helpers is not executing a peer project. The installation explicitly remains non-hermetic. |
| Dispatch | `peer.py:150` onward permits `find`, `directory-find`, `directory-serve`, `preview`, `inspect`, `authoring-offers`, `receive`, `publish`, and `serve`. None is a project producer or arbitrary command executor. State-free operations reject owner catalog/custody arguments; receive opens the actual local admission adapter. Configuration and paths are owner inputs. |
| Acquisition | `support/transport/ordinary_acquisition.py:345` onward performs bounded exchanges through configured endpoints and known routes. Evidence is parsed by `portable_evidence.read_evidence`; preview and locator bindings are checked. Custody retains raw inert claims, not native modules or source execution authority. `authoring_offers` never follows repository hints or retrieves/runs source. |
| Discovery/inspection | `peer_api.py:492` (`find`), `:922` (`authoring_offers`), `:984` (`inspect`) and `:1081` (`preview`) operate on metadata or parsed units. Inspect explicitly reports `dependencies_checked=False` and `native_usable=False`. Directory discovery provides contact hints, not mathematical authority. No acceptance is obtained by a successful lookup. |
| Receive planning | `peer_api.py:573` onward validates the selected local parent, fetches selected evidence and resolves exact bindings. `selected-unit-only` returns a grounded-premise requirement instead of automatically fetching ancestry. Explicit `bounded-closure` can fetch missing units under the existing aggregate limits. Only a READY plan reaches actual `owner.admit` at `:693`. |
| Inert grammar | `installation/py/portable_evidence.py:46` requires exactly schema, semantic ID, imports and unit, with canonical bounded JSON and an exact external-name/import census. `installation/lean-src/OriginalExpr.lean:321` constructs bounded `Expr`/`Level` nodes from closed tags. It has no source interpreter, callback, filesystem path or executable attribute in that grammar. `OriginalDecl.lean:295` constructs only safe definitions, theorems, safe opaque declarations and nonunsafe inductive groups. |
| Actual checking | `installation/py/ordinary_admission.py:565` recomputes the plan rather than trusting a caller's READY/order assertion. `:587` stages only exact declaration data and the locally constructed parent plan. `_worker_main` at `:676` accepts fixed `basis`/`extend` commands; `:709` runs the selected local Lean executable and fixed worker. Peer fields do not select its executable or source file. |
| Kernel boundary | `OrdinaryWorkflowWorker.lean:198` restores the selected local parent, decodes units, and invokes `LocalSnapshot.checkAndWriteChunk`. `CheckedExtension.lean:110` onward rejects unsupported/unsafe/axiomatic/open/unresolved additions, checks all references, and at `:131` calls `addDeclCore ... (doCheck := true)`. Actual generated kernel inventories must equal the advertisements. This bypasses elaborator fallback-axiom recovery. |
| Snapshot production | `LocalSnapshot.lean:107` has a private writer accepting the actual checked result. `:130` writes actual generated constants; extension entries and extra constant names are empty. A peer inventory is compared with kernel output, never installed as unchecked `ConstantInfo`. |
| Durable promotion | After clean live worker completion and exact output/report/census checks, `ordinary_admission.py:647` calls private `_commit_checked`. `portable_catalog.py:628` requires the identical live, unexpired reserved grant; `:637` binds the artifact digest/size, exact local parent/module, inputs and bindings before committing. A saved success report or peer assertion cannot recreate this live event through the public path. |

Kernel evaluation of a term for type conversion is not Lean source execution:
it does not execute a peer tactic, macro, `#eval`, module initializer, native
plugin or an `IO` action merely because such a type or value occurs in a term.
It can nevertheless consume substantial resources or expose checker defects.

### The native-deserialization qualification matters

`LocalSnapshot.lean:232` is explicitly an unsafe native-deserialization boundary,
not a safe reader for arbitrary `.olean` files. It clears search paths and calls
`Lean.importModules` using the exact local artifact map, `plugins := #[]`, and
`loadExts := false`. The plan contains only selected catalog-owned chain artifacts.
`portable_catalog.py:318` authenticates artifact size/digest against protected
local records; `:490` builds the bounded exact local parent chain.

This is legitimate **only because these native bytes were previously generated
by the actual approved checking path and remain protected**. Post-load census,
header and parent checks do not make an arbitrary hostile binary safe to load.
The per-owner-process verification cache and hash-before-load sequence rely on
immutability through use; they are not protection against a concurrent writer
with the same authority. No downloaded peer `.olean` is admitted through receive.

### Approved authoring is intentionally a different lane

`author_worker.py` executes the selected source using Lean and may import the
approved project's compiled modules. Its project branch explicitly assumes
trusted plugins and does not claim sandboxing. `owner.py:273` requires explicit
local-project approval for `produce-baseline`; `authoring/py/baseline_worker.py`
uses the selected local exporter and approved project paths. Export produces
inert evidence; recipient intake then checks that evidence independently.

The fixed executable/argv and Windows Job bounds prevent neither filesystem
access nor network access by approved source. The admission shim removes the
relevant `LEAN*`, `PYTHON*` and `PATH` environment influence before its fixed
checker call, but it does not claim a scrubbed secret-free environment or OS
permission isolation. Ordinary external Lean/Lake builds are also executable
workflows; repository URLs offered by peers must never automatically authorize
them. A trusted project may use arbitrary build plugins without becoming
mathematical authority for the receiving peer.

## Conditional acceptance statement

Let `W(C)` mean that every binding in local context `C` is warranted under the
selected foundation and semantic policy. Assume:

- the owner-selected implementation/runtime and kernel implement their stated
  checks correctly, including decoding, conversion, inductives and serialization;
- identity commitments are collision resistant and bind the intended exact
  bytes/semantics;
- the selected base is warranted, and protected local snapshots/catalog/control
  state have not been replaced or changed between authentication and use;
- public acceptance can only be promoted by the actual clean checking event and
  its correctly bound live commit, not by a hostile in-process caller.

Then the traced rule has the intended implication:

`W(C) and Receive(C, bytes) = CHECKED(C') => W(C')`.

Reason: every newly decoded declaration has grounded references, is added with
actual kernel checking, and is bound to the exact accepted inventory and durable
snapshot; previous bindings are neither overwritten nor silently reinterpreted.
`REUSED` instead depends on an already warranted exact binding. Inert metadata,
preview success and storage possession alone have no such implication. This is
a source-level conditional argument, not a mechanized proof of this implementation
or of Lean/runtime correctness. It also does not prove mathematical importance,
availability, discovery completeness or global scalability.

## Minimum remaining security obligations

| Obligation | Existing enforcement / exact remaining premise |
|---|---|
| Keep executable authority local | Fixed dispatch/worker paths and owner-selected hashes exist. Distribution still needs a trustworthy source of the approved package/runtime pins and a clear update policy; a digest supplied by an attacker is not approval. |
| Protect warrant state through use | Catalog locks, exact grants, paths, hashes and bindings exist. Installation/runtime/catalog/snapshot roots must stay out of hostile writers' control, including source-authoring programs. Current same-account execution does not enforce a separate security principal. |
| Keep code approval separate from data selection | Peer offers and ordinary receive remain non-executing. User documentation must make the authoring approval meaning unmistakable. If projects cannot be trusted at the owner principal, run them under genuine separately controlled permissions/VM before exchanging inert outputs; no such facility is established here. |
| Bound hostile data costs | Wire/grammar/dependency bounds, operation budgets and live Job CPU/memory/process/wall containment exist. They are not an access-control sandbox. Cumulative disk/custody/catalog capacity, repeated requests, concurrency and service exposure still require the stated operator limits and resource policy; one bounded request does not bound lifetime cost. |
| Assess implementation compromise | Parsing, HTTP/TLS, Python, native Lean/kernel and native serialization remain an attack surface. This audit found no intentional remote-code path; it did not establish memory safety/exploit absence across those dependencies. Independent targeted security review remains useful before broad hostile-network deployment. Least-privilege separation reduces consequences of bugs but is not a substitute for the mathematical checks. |
| Preserve the public claim | Do not advertise arbitrary source safety, peer-native import safety, hermetic runtime integrity, global service availability or complete v5 readiness from this result. Conversely, do not require a speculative general hostile-source execution framework merely to ship an inert mathematical-data protocol. |

If the deployment threat model includes execution of hostile projects or hostile
same-user co-tenants, the protected-state premise is false without stronger
separation. That is a concrete deployment restriction, not a warning cured by
more proof certificates. A sandbox alone likewise cannot turn an unsound checker
or exported hypotheses into warranted mathematics.

## Existing evidence reused, not repeated

- `research/cycles/v5-2026-10-22-native-library/OUTCOME-CORE.md` records the actual
  conditional-fixture core controls, including genuine invalid-proof type
  mismatch, unsafe/axiom refusals, generated inventory matching and no accepted
  failed-batch prefix. It is finite correctness evidence, not exploit assurance.
- `.../SNAPSHOT-OUTCOME.md` records the conditional snapshot/restore controls,
  including later proof use without ancestor kernel replay. Its author review
  is explicitly not an independent software audit or peer-binary safety result.
- `.../ORDINARY-PROJECT-CONTROLS-OUTCOME.md` independently records the five
  native-free configuration/default-source/invocation controls with explicit
  mocks; it is not actual project import safety or mathematical acceptance.
- Current sparse assembly/public outcome audits establish their changed routing
  and packaging boundaries, not a new native or security campaign.

## Recommended root consequence

Keep ordinary inert checking as the default. Do not reopen the costly certificate
campaign or build a generic sandbox solely because the peer protocol handles
untrusted mathematical data. The highest-payoff assurance follow-through is an
accurate executable-trust/deployment contract, preservation of protected state
against authoring execution, and targeted review of the actual exposed boundary.
An independently operated trial is still valuable, but is not the only remaining
assurance obligation. This checkpoint neither closes the full v5 goal nor selects
a new runtime or mechanism.
