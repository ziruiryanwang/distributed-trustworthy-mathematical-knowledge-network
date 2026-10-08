# Minimal native client for independent Lean agents

Date: 2026-09-20  
Status: read-only implementation plan; no new code or experiment executed  
Owner: `bounded_domains_author`

## Decision

Give an agent checked declarations, their actual types and usable Lean names, and a way to elaborate **its own source** and export a selected result. The agent decides when to search, which definitions to use, and how to prove its theorem. No solver, goal controller, proof-obligation queue, shared task list, or mandatory goal-to-query bridge belongs in this client.

The shortest path generalizes the already demonstrated source consumer. It does not restore a producer's `.olean`, namespace metadata, tactics, or source proof. The native client is a local interface over the existing finite data-only replay machinery, not a new network protocol.

## Existing implementation and evidence

All paths below are relative to the repository root. Held files remain unchanged.

| Capability | Existing callable implementation | Limitation |
|---|---|---|
| Validate exact package bytes and build a replay plan | `experiments/lean-source-composition/held/cut-03/source_codec.py`: `read_package`, `merge_packages`, `make_plan`; CLI `prepare` | Structural/hash validation is not native acceptance. Union refuses incompatible representative contexts. |
| Reconstruct checked declarations | `experiments/lean-proof-context-reconciliation/held/code-01/ReconcileComposition.lean`: `SourceComposition.receive`, `receiveOrdinary`, `receiveGroup`, `checkedAdd`; CLI `--receive PLAN --inventory INVENTORY` | Plan is an owner-local canonical bridge input, not an authenticated peer API. |
| Elaborate ordinary source against reconstructed declarations | Same file: `consume`, `consumeR1`, calling `Lean.Elab.process text state.env options (some path)` | Fixed presentation roles, fixed theorem names, exactly two universes, and experiment-specific dependency tests. |
| Capture the actual new declaration closure | Same file: `allowedNames`, `collectExtension`, `captureUnitsJson` | Finite supported declaration fragment; not arbitrary Lean/library coverage. |
| Convert captured source declarations into canonical contribution objects | Held `source_codec.py`: `SourceCompiler`, `capture` CLI, `--inherit` | Produces candidate bytes, not a proof-checking receipt. |
| Compare actual receiver output with canonical bytes and re-export | Held `source_codec.py`: `reexport_actual`, `reexport` CLI | Caller must bind native output to its actual run and exact inputs; a supplied JSON/log is not self-authenticating. |

The retained R1 `runs/attempt-01/A3/01.stdout.log` contains `CONSUMER_SOURCE_JSON` followed by `R1_CONSUMER_CHECKED`: a source theorem uses reconstructed `DTMKN.i.…`, `DTMKN.d.…`, and `DTMKN.w.…` declarations directly. A3/A4 then perform source capture, canonical export, fresh native replay and actual-row inverse export. This establishes the existing specialized path, not a generic client implementation.

The pinned runtime's `Lean/Elab/Frontend.lean:134` defines `Lean.Elab.process` over the supplied environment using command processing, not module import processing. Its frontend implementation gathers diagnostics across command snapshots. Do not replace it with an ordinary file compilation that implicitly imports a producer or a different mathematical environment.

## Two small native operations

The following command shapes are **proposed**, not callable today. A new experiment may provide them while retaining the held receiver and codec behavior.

### Inspect checked environment

`--inspect PLAN --inventory INVENTORY`

First call `receive`. Enumerate the resulting checked `state.bindings` in a deterministic order, with an explicit bound; expose no producer-role fields. For each admitted reference return:

- Exact typed reference and foundation/replay context.
- Actual Lean `Name` encoding and its `Name.toString` source spelling.
- Declaration kind and ordered universe-parameter names/arity.
- Actual declaration type, both as a canonical formal DAG and a readable Lean presentation.

The formal type is available from `lookup state.env.toKernelEnv name`, then `exportDag state.bindings #[] false info.levelParams info.type`. This path checks constant-to-reference bindings; it is not a lookup in an evaluator's source-name map. Seed references remain indexed by the checked seed inventory.

For readable presentation, the pinned runtime exposes `Lean.PrettyPrinter.ppExprLegacy state.env {} {} options info.type` (`Lean/PrettyPrinter.lean:68`). Request explicit arguments, full names and universes, and avoid notation-dependent output where supported. Pretty-printed text is a convenience, **not** canonical data or a guaranteed round-tripping source encoding. A failure to print must be reported separately from a successful check. The qualified source spelling and formal DAG remain available.

As an immediate diagnostic alternative, an agent can put `#check @<returned-name>` into its own source. The generalized source operation must return information messages on success, unlike the current consumer which prints frontend messages only on failure. Thus type inspection need not introduce a new source pretty-printer or an alias language.

### Check source and capture one selected root

`--check-source PLAN --inventory INVENTORY --source FILE --root NAME`

One selected root is sufficient initially: it matches the existing codec's `--root-name`. A later root-list batch can be added only if needed. Sequence:

1. Reconstruct the selected environment with `receive`; retain its checked binding table and actual replay rows.
2. Read bounded UTF-8 **agent-owned** source; record the exact bytes and supplied root name. Do not inject a proof or replace role-specific template tokens.
3. Invoke `Lean.Elab.process` over that reconstructed environment with pinned options and the actual file name.
4. Return diagnostics, including information/warning messages, source positions and severity. `Lean.Message.toJson` is available; inspect `MessageLog.reportedPlusUnreported` if needed to avoid dropping already reported diagnostics. Test early-command and final-command failures rather than assuming the final log is complete.
5. If any frontend error occurs, produce no contribution capture. Otherwise find the requested root and require a new, completed supported declaration. Remove the old exactly-two-universes and particular-theorem-name restrictions; keep the finite universe bound. For the first reciprocal trial, selecting a theorem is enough; definitions are already supported by the underlying capture machinery.
6. Run the existing declaration/closure screens and `collectExtension actual (allowedNames state.bindings) #[root]`, followed by `captureUnitsJson`. Missing proofs, open expressions, forbidden references, unsupported axioms/declarations, unsupported syntax and bound exhaustion are explicit failures, not fallbacks to axioms or `sorry`.
7. Emit the existing `SOURCE_CAPTURE_JSON` schema for canonical export. Record actual type/body dependencies as diagnostics, but do **not** require particular discovered results to occur: that is an evaluator claim, not a client acceptance rule.

Do not label this capture `REPLAY_ACCEPTED`. Its downstream candidate must still pass the independent canonical export/replay path. An agent's wrong theorem statement is not a client rejection merely because it differs from an evaluator's target; target conformance belongs in the trial evaluator.

The old `added.length == exported` check is specific to a one-theorem fixture. For an ordinary source file, report new declarations outside the selected root's closure as omitted, rather than silently publishing them or demanding their relevance. The selected closure must still be complete. Verify that preexisting checked declarations were not replaced before capture; the held `BootstrapSupport.sameConstant` provides a structural comparison helper. Independent fresh replay remains mandatory even after these local checks.

## Lean names, binders, and missing elaborator metadata

`referenceName`, `ordinaryName`, and `groupName` already derive stable native names from typed references. Definitions use `DTMKN.d`, proof instances `DTMKN.w`, semantic judgment aliases `DTMKN.j`, opaque declarations `DTMKN.o`, and inductive members `DTMKN.i.<id>.tN`, with `.cN` and `.rec` selectors. Return `Name.toString`; do not concatenate an unescaped digest token. The retained R1 source uses the required quoted components, such as `DTMKN.d.«8401…»`.

The receiver deliberately reconstructs binders with anonymous names and explicit/default binder information (`expandDag`, native tags 4/5). Agents should initially use fully qualified names with `@` and explicit argument order, optionally explicit `.{u, v}` universe arguments. The inspection output must expose this order. Original implicit-argument conventions and named-argument syntax cannot be promised.

Kernel declarations do not reproduce the producer's structure/projection tables, coercion instances, simplification attributes, notation, typeclass registration, or tactic extensions. Use returned constructor, projection-function and recursor names explicitly. Do not promise `x.val`, structure syntax, `simp`, or arbitrary imported tactics will work as in the producer's environment. The smallest documented source subset is the one already demonstrated: explicit constants/applications, lambdas, dependent function types, universes, and theorem declarations. Agent-chosen richer source may be attempted, but unsupported elaboration must return diagnostics, not change the mathematical foundation.

Readable local aliases may later improve ergonomics, but are unnecessary for the first client. Creating Lean `def`/`abbrev` aliases introduces declarations and possible export dependencies; it is not a cost-free renaming of semantic IDs.

## Reuse the existing canonical contribution pipeline

After source capture, the owner-local wrapper can invoke the held codec with these existing CLI shapes; placeholders are caller-owned paths, not shell instructions to run during this review:

```text
source_codec.py --codec-path CODEC prepare
  --seed SEED --package P1 [--package P2 ...] --plan PLAN

source_codec.py --codec-path CODEC capture
  --seed SEED --capture CAPTURE_LOG --root-name AGENT_ROOT
  --inherit P1 [--inherit P2 ...]
  --package CANDIDATE --plan CANDIDATE_PLAN --mapping LOCAL_MAPPING

ReconcileComposition.lean --receive CANDIDATE_PLAN --inventory INVENTORY

source_codec.py --codec-path CODEC reexport
  --seed SEED --package CANDIDATE --actual BOUND_NATIVE_OUTPUT
  --output REEXPORTED --plan REEXPORTED_PLAN
```

The Lean line denotes the program's existing arguments; retained plans launch it through pinned `lean -R NATIVE_DIR --run FILE`. Re-export can then be replayed in a fresh receiver, as A4 already does. A local wrapper may orchestrate these calls, but must not interpret codec success, an arbitrary `ACTUAL_BATCH_JSON` line, or a content identifier alone as mathematical acceptance.

Prepare/export must use precisely the same inherited packages/context as source checking. No producer-specific `presentation` is needed. `make_plan` without a presentation already supports compatible unions. The R1 `reconcile_fixture.prepare_plan` has fixed mathematical roles and is **not** a general-purpose conflict resolver. For the first client, return a clear context-conflict diagnostic rather than rewriting proof evidence or silently choosing a new representative; separate workspaces or a separately checked reconciliation are possible later.

## Trust and bounded failures

Remote contribution bytes remain data-only input to canonical validation and fresh native replay. Agent-owned Lean source is different: Lean elaboration/metaprogramming can execute code. `Lean.Elab.process` is **not a sandbox**, and a resource-limited process is not filesystem/network isolation. Do not fetch and execute peer source, plugins, Lake configuration, or `.olean` files as a consequence of discovery. The initial local client runs only owner-authorized source with this limitation stated.

The existing Windows runner bounds resources and records inputs/outputs; its documentation explicitly disclaims a general sandbox. Preserve those limits and distinguish resource failure from logical rejection. Native `maxHeartbeats=20000000`, `maxRecDepth=10000`, a 64-KiB source cap, and existing package/declaration/DAG ceilings are reusable initial ceilings, not per-retry entitlements. The owner wrapper must charge retries to the trial's aggregate budget; source `set_option` commands cannot enlarge the external wall/CPU/memory envelope. Diagnostics also need a byte cap with an explicit truncation marker.

At minimum return distinct outcomes for malformed/hash-mismatched package, incompatible context, native replay rejection, source elaboration error, absent/unsupported root, unsupported export closure, and resource exhaustion. On failure keep the previous accepted package set unchanged. An in-memory checked environment can be discarded and reconstructed; persistence, session continuation and cached `.olean` generation are not required for this first cut.

## Small qualification set and remaining work

Before calling this a usable client, root should run a reviewed finite probe that:

1. Inspects a reconstructed declaration without any producer-role map; checks returned source spelling, universe order, formal type and diagnostic rendering.
2. Elaborates two different agent-written source/root names, including one not using all available contributions; checks no hardcoded theorem or two-universe restriction remains.
3. Returns an early-file type error and a successful `#check` message; refuses `sorry`, an added axiom in the selected dependency closure, an unknown reference and an absent selected root.
4. Exports, independently replays and inverse-exports a contribution using the exact inherited context; confirms namespace spelling is not the mathematical identity.
5. Uses a fresh second consumer to check and use the first contribution; records that result independently of any useful-growth or blind-discovery claim.

Unimplemented here: the generic native wrapper, its role-free inspection output, structured diagnostics, a thin local orchestration command, and these tests. Retrieval implementation and trial access/accounting are separate workstreams. General projection/tactic metadata restoration, persistent sessions, automatic proof search and arbitrary-library support are not prerequisites for this bounded client qualification.
