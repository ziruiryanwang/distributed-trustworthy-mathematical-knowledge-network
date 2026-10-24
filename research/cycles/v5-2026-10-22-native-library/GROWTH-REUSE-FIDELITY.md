# Reuse fidelity: declarations are not an entire Lean library API

2026-10-24. `growth_payoff`, source/theory only under
GROWTH-IMPLEMENTATION-SELECTION. No product edit, experiment, build, download or
Git mutation. All runtime references below are to the retained Lean 4.34.0 source
under `software/runtime/lean-4.34.0-windows/src/lean/Lean/`.

## Decision

**Do not make generated inert-evidence modules the default replacement for ordinary
approved packages.** They supply a checked mathematical interface, not faithful
reconstruction of the original package's entire authoring and executable API.
For mature libraries with notation, class hierarchies and domain automation, the
approved package is usually the appropriate full-fidelity route. Its execution
approval and mathematical assurance must still be stated separately; neither
trust in a publisher nor importing its compiled cache is independent proof checking.

Keep selective inert interchange as a valuable second route: a recipient can obtain
supported mathematics without approving arbitrary new publisher code. A narrow,
optional local-use layer can recover useful automation from checked declarations,
but **generic metadata/attribute replay is not a small inert feature**. Do not
build another package/elaborator reconstruction system merely to avoid this choice.

The minimal defensible consequence now is a clear product distinction, plus use
of existing explicit local Lean mechanisms for two common cases: selected theorem
rewrite sets and selected values of already known classes. No new wire schema,
parser, arbitrary attribute dispatcher or source extractor is selected here.

## What the current writer actually preserves

Relevant project source:

- `ordinary_module_anchor/OrdinaryModule04.lean:639-681` imports only Init or
  protected locally registered ancestors, with no plugins/extension loading;
  checks new declarations in private and exported views; calls `exposeAdded`;
  and writes the resulting module. It does not run the original source elaborator
  or copy its arbitrary environment extensions. Both fresh rereads remain required.
- `ordinary_lean/CheckedExtension.lean:99-156` checks grounded expressions with
  `addDeclCore ... (doCheck := true)` and compares exact generated inventories.
  It intentionally bypasses ordinary elaborator handling and recovery.
- `ordinary_lean/OwnerRebind.lean:274-309` exposes newly checked recursors when
  needed and registers name prefixes. Its comment explicitly excludes notation,
  instance and plugin loading. Namespace registration is not metadata restoration.
- `ordinary_lean/OriginalDecl.lean:86-104,122-153,221-257` carries kernel declaration
  information, universe/type/body data, kernel reducibility hints and generated
  records. Its "metadata" wording concerns those constant records, not every
  frontend/environment extension associated with the source declaration.

Thus ordinary explicit theorem application and supported definition reduction can
work. Original names, types and proof/dependency identities are not replaced with
invented equivalents. Metadata already present through the user's approved base
or imported protected ancestors need not disappear. The missing part is the new
publisher's authoring behavior which is not encoded in the mathematical units.

## Concrete API losses and why they matter

| API facet | Separate retained Lean mechanism | Consequence for new imported mathematics |
|---|---|---|
| Class recognition | `Class.lean:70-78,166-175`: persistent `classExtension`, checked `addClass`, output-parameter metadata | An inductive with the right kernel shape is not automatically registered as a type class. |
| Instance search | `Meta/Instances.lean:53-103,283-330`: scoped instance tree, priorities, synthesis order, and separate `instanceReducible` status | A definition of class type can exist but not be found by typeclass search. Merely restoring a name is insufficient. |
| Structure/field syntax | `Structure.lean:20-76,87-129` and `ProjFns.lean:15-38`: field order/names, parents and projection-function metadata | Constructors/projections may exist as constants without record-literal, structure-inheritance or projection elaboration behaving like the original source. |
| Simplification | `Meta/Tactic/Simp/Attr.lean:16-59`: theorem sets, priorities, orientation, unfolding and equation tables | Default `simp` need not discover a new valid theorem; marking a definition for simp can require equation metadata beyond its body. |
| Meta-level transparency | `ReducibilityAttrs.lean:14-35,54-98`: separate persistent/scoped statuses used by indexing and conversion heuristics | Preserved kernel `ReducibilityHints` do not restore every `[reducible]`, `[instance_reducible]` or related frontend status. |
| Notation and syntax | `Elab/Notation.lean:132-159`: parser construction, macro rules and optional unexpanders | A mathematical constant alone does not provide the producer's notation or pretty-printing behavior. |
| Tactics, custom attributes, simprocs | Registered implementation code and environment extensions | Proof terms can be transferred without transferring the tactic that constructed them; future automation may still need the approved original tooling. |
| Naming/toolchain conventions | Exact current names and the selected semantic/runtime profile | The module writer does not port another Lean version, invent aliases, repair name collisions or recreate scoped opens from source. |

The writer also does not compile arbitrary new definition code through the normal
compiler pipeline. Kernel reduction and native/bytecode evaluation are different
capabilities. Do not promise preservation of `#eval`, extracted executable behavior
or a library's performance merely because its mathematical definition checks.
This is a source boundary, not a claim that every use of `#eval` fails: imported
approved code and locally compiled wrappers can behave differently.

These losses are not cosmetic. Typeclass search often supplies long chains of
implicit arguments; missing registrations can make ordinary-looking theorem
applications fail. Missing notation/structure support can force verbose explicit
terms or block the intended authoring workflow altogether. Reproducing a declaration
does not reproduce the human/agent effort needed to use it.

## Why "copy the safe attributes" is not the right generic repair

1. `Simp/Attr.lean:45-48` dispatches `[simp]` to the simproc attribute when the named
   declaration is a registered simproc. Whitelisting the text `simp` alone does not
   establish a theorem-only data boundary. Definition unfolding also consults
   equation metadata; arbitrary attribute names may invoke arbitrary registered code.
2. `Environment.lean:2427-2432` explicitly says extension loading can use the
   interpreter and needs initializer execution enabled. Changing `loadExts := false`
   to true is an execution-boundary change, not an inert deserialization repair.
3. Instance priority, local/scoped/global applicability and registration order
   influence which data implementation gets selected. Every alternative can be
   mathematically well-typed while changing computation or producing expensive search.
4. Structure and projection APIs accept metadata with invariants beyond simple
   declaration existence. A few self-asserted field names are not enough to safely
   reconstruct all elaborator invariants. This would need a real validated subset.
5. Reducibility changes affect pre-existing discrimination indexes; the retained
   `ReducibilityAttrs.lean:100-153` documents the hazard and restricts such updates.
   Replaying attributes in arbitrary order does not restore original behavior.

The final kernel check can protect mathematical conclusions produced through an
honest local meta layer, but it does not automatically protect runtime safety,
termination, resource use or frontend meaning from arbitrary extension payloads.
No generic remote extension attachment should be called safe merely because its
last step is "check the resulting theorem."

## A useful narrow reattachment option already expressible locally

For **already admitted exact declarations**, two forms of local, opt-in automation
need no new mathematical objects:

- **Theorem-only rewrite selection.** In an approved local file, use an explicit
  `simp only [selected_theorem_1, selected_theorem_2]` or direct rewrite/application
  after resolving those names to the exact accepted exports. Do not accept remote
  tactic strings, custom attributes, simproc names, arbitrary dischargers or
  uncontrolled source snippets as part of the data-only route.
- **A selected value of an already registered class.** Use a local `letI`/explicit
  instance argument for an accepted value with the required checked class type.
  For example, an accepted `Inhabited T` value can be supplied locally rather than
  recreating the producer's global instance registration. This does not register a
  newly imported class hierarchy or repair missing structure metadata.

There is direct source support for the first restriction:
`Elab/Tactic/Simp.lean:552-579` builds a fresh theorem context initialized with
`simpOnlyBuiltins` and starts with an empty simproc set for `simp only`. It still
uses the approved local congruence theorems and tactic/configuration machinery;
`only` does not isolate that infrastructure. Its argument elaboration can add simprocs
(`:433-462`), so a future automatic wrapper must restrict arguments to the intended
checked theorem references; the word `only` is not a universal input sanitizer.
Use trusted local template/API construction, never interpolate untrusted source.
The ordinary local runtime is still executable approved code with finite budgets.

These are **local usage choices**, not claims that the original metadata has been
recovered. Keep them scoped to the particular proof/module, with explicit opt-in:
do not silently add global instances or change another file's default simp set.
The resulting complete proof is checked normally. Wrong or unhelpful selections
can fail, cause loops/expensive rewriting or choose an unintended data instance;
they cannot be assumed harmless because the selected declarations were valid.

This provides a meaningful middle option between "bare theorem only" and "approve
every producer extension." A batch of independently produced simplification laws
can become a usable local rewrite tool, and a new valid implementation of a known
interface can participate in existing local typeclass-driven code. Those are new
supported uses of the same checked knowledge, not more copies of theorem statements.
They do not require inventing a complete reattachment manifest now.

## Where this pays, and where it does not

The narrow route has a concrete favorable workload: the consumer already has the
relevant class/notation/tactic infrastructure; the contribution adds a modest set
of facts or an instance value; and executing or reviewing the entire publisher
environment is unnecessary or disallowed. The local instructions are a short
selected rewrite list or one explicit instance binding, not reconstruction of
a framework. Exact evidence checking and the actual proof application remain costs.

This can enable an approval-compatible use that a source-only delivery did not
provide, or reduce repeated manual instantiation. It is not a theorem that the
strongest ordinary tactic is slower. A Git repository may carry the same inert
artifacts and instructions; the useful adapter belongs to both routes. Conversely,
ordinary Git does not already implement our missing safe artifact admission merely
because it can transport files: its real integration/verification work still counts.

The unfavorable workload is equally concrete: a new algebraic hierarchy with
custom notation, coercions, structure inheritance, simp/congruence attributes and
domain tactics. Repairing six extension systems to imitate its package can cost
more than approving/building the package, and may still miss its intended API.
Examples already inspected in GROWTH-CASE-SELECTION use custom optimization or
compiler automation and different toolchains. An inert reattachment list does not
port them or solve an unproved refinement bridge. Prefer approved packages, or
explicitly decline automatic rich-API reuse under the receiver's stricter policy.

This decision does not require a fabricated external customer or new experiment.
The two source-level paths differ in real required mechanisms. Which workload is
prevalent needs later usage evidence, but generic software can support the useful
small path now without claiming universal package replacement or exponential growth.

## Minimal software consequence and stop boundary

For the current native-first consolidation, make the generated-module contract
explicitly **mathematical-declarations-only** and preserve the approved-package
route as the default for rich ordinary API use. Document the existing explicit
rewrite/instance techniques as local options; no metadata protocol is required.
Keep the original-reference failure parked rather than using it as a reason to
reconstruct arbitrary original extensions in the inert lane.

If subsequent implementation needs one optional automatic attachment, choose only
the theorem-reference rewrite selection in a trusted local consumer wrapper,
with exact accepted-reference resolution and ordinary proof checking. First reuse
existing local Lean commands; do not add generic `[attribute name]` replay. A
broader class/structure/transparency restoration project requires a separate
source-led case because its invariants and cost are materially different.

**Actionable conclusion:** adjust the public usage promise and route selection,
not the checker or wire format. The developer of an independent contribution
should not have to strip a whole library's usable API just to participate. The
recipient should not have to execute that API merely to reuse a small proved fact.
Supporting both choices is a stronger deployable architecture than pretending
one declaration-only representation fully substitutes for every Lean package.

## Independent narrow facade review

Root's subsequent assignment reviewed only the new
`ordinary_native_package/owner.py` and `profile.py` against the stable preview
owner/loader and tested producer donor named by NATIVE-CONSOLIDATION-SOURCE.
Disposition: **no new source-level blocker found within this consolidation**.
This is not an installed workflow, growth result or runtime qualification.

Independently read the complete new owner and loader. Read-only .NET source-block
comparisons confirm exact source equality for the five stable owner helpers
(`need`, `project_json`, `bootstrap`, `separated`, `status`), the tested producer's
`Allowance`, argument gate, operation body and intake dispatch, and all eight
stable loader helpers. The checked new hashes are:

- owner: `56ef042f652fcb88cae7d16ab74883016a469e2e82777c1a173f842f5ef8245a`.
- profile: `d63ea79f527e5519c19afcf1b98ae262b6eabb662fe454d30b1a4a75722ed8a6`.

Producer dispatch occurs before owner state opening, requires explicit approved
local project/selection/outputs and spool allowance, and refuses unrelated state
or operation arguments before loading support. Non-producer operations require
their owner fields and reject producer-specific flags. Intake remains an explicit
parent plus exact manifest pin, calling the unchanged intake controller; ordinary
contribution/completion/export paths retain their existing checked controllers.
No reference registration, matching, delta or authoring branch survives. The
historical `OWNER_REFERENCE_BUNDLE_PIN` string is only a diagnostic label.

The parent allowance continues across stages; ordinary output reservation remains
64 MiB and only the producer supplies its explicit bounded spool. Intake's CPU
report remains honestly labeled a partial observation, not complete measured CPU.
This consolidation does not strengthen cooperative parent limits into hard
containment or weaken mathematical admission into trust in production.

The loader pins and censuses the five added baseline roles before imports,
rejects their preloaded module names and checks exact loaded module paths. The
logical `reference/` directory contains only baseline bundle/intake; it adds no
reference native-helper path. The single original authoring-helper profile and
native installation verification remain. New facade bytes imply a new anchor
support identity, as the README explicitly states; old anchors are not migrated.

Process disclosure: one earlier read-only `git diff --no-index` call was used
despite this assignment's no-Git scope; an incorrect old-owner path prevented
that comparison, while the profile comparison returned source differences.
No index/repository change occurred. The independent comparisons above used the
correct donor paths and .NET file reads, without further Git calls. No test,
product import, build, download, package assembly or runtime was launched.
