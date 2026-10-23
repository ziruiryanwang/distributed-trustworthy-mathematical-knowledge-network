# Existing Lean projects: the smallest useful integration boundary

2026-10-23. Source/theory decision by `owner_cli`; no project import, Lake call,
code change, build, test, peer action or Git operation. This is separate from the
package audit and does not reopen its source selection.

## Decision

After the thin owner workflow works, prefer a **local candidate-export adapter
inside an owner's existing trusted Lean project**, retaining ordinary admission
as an independent final step. Do not promise that scratch theorem assumptions
can be installed as ordinary proved Lean libraries, and do not implement a new
package manager or custom tactic environment first.

The user workflow is: keep normal editor, tactics, notation and pinned project
dependencies; select an already accepted commons context; construct/use the
needed interfaces in one contribution source module; export the new complete
declarations; independently check those declarations against the actual receiver
context; then share inert evidence. A project build and successful elaboration
are candidate production, not receipt of mathematical authority.

## Two different capabilities

**A. Trusted local project support during candidate production.** This is
compatible with the current trust separation. Tactics/metaprograms can run in
the owner's already approved environment and produce candidate proof terms.
The receiver still decodes and checks the complete new terms against exact
accepted imports. A broken tactic can cause refusal or wasted work; its success
flag is never admission. Executing that local support is nevertheless a code
execution decision: final mathematical checking does not sandbox the producer.

**B. Ordinary checked libraries usable without the commons receiver.** Missing
acquired theorem handles currently enter construction as scratch `axiomDecl`
records. Their types are kernel-checked for well-formedness, not their truth.
Compiling a module that depends on those handles therefore does not give an
ordinary independently proved Lean library. That endpoint needs actual proofs
checked in an appropriate environment, or an explicit additional trust policy.
Shipping the scratch `.olean` files or relabeling these handles as theorems does
not supply those proofs. Our current checked local snapshots are an explicitly
protected receiver optimization, not portable proof authority for another Lean
project/process. This distinction must remain visible in editor/export tooling.

## What inspected code already permits and forbids

- `PortableOwnerConstructCommand.run` accepts an existing top-level environment
  and records construction metadata for the current module only.
- `OwnerConstruction.demand` stops at an existing safe local declaration; it does
  not traverse its body or prove that its semantics match the receiver's label.
  Missing demanded definitions/groups are reconstructed from selected data;
  missing accepted theorem types become explicitly classified scratch axioms.
- `SuccessorExport.selectedDeferred` exports complete new units. Safe imported
  constants may stop traversal; unmapped ones become **unresolved names**, not
  guessed portable IDs or evidence. New local declarations do not stop merely
  because they have familiar names.
- `portable_candidate.bind_candidate` preserves all claimed IDs, resolves only
  explicitly unclaimed names through the protected selected receiver context,
  and reports missing interpretations together. The resulting READY packet is
  still not mathematical acceptance. Final native admission remains mandatory.
- `PortableContributionExportCommand` requires targets created in the current
  source module. Importing an existing compiled theorem and exporting its name
  is refused. A new alias does not bypass this: its imported dependency still
  needs a genuine receiver interpretation and checked evidence when absent.
- The current Python source wrapper fixes Init/helper imports before its body;
  the source-body argument is not an arbitrary Lean import header. The isolated
  worker supplies only selected helper paths. Thus trusted arbitrary-project
  import support is a possible next adapter, **not implemented today**.

Interpretation mismatch has a precise consequence. Let the owner elaborate in
environment E and export term/type (p,T), then let rho bind used names to the
receiver's exact symbols. Acceptance establishes Gamma |- rho(p) : rho(T),
conditional on the existing checker assumptions. It does not establish that E
and Gamma are equivalent or that the result has the same meaning as an existing
package's theorem. Expose the exact admitted statement/IDs; no human-intention
comparison is needed in the mathematical acceptance protocol.

## Smallest next source interface, if selected

1. A caller supplies a trusted local module/import environment using the same
   supported Lean version, an exact accepted parent, selected acquired handles,
   explicit target names and one finite allowance. Do not fetch/build dependencies
   automatically, execute a peer build script or infer the global environment.
2. Place construction and export hooks in the module that authors the new
   targets: after its approved imports/before authoring, and after authoring.
   A separate driver that merely imports the finished target module is not
   compatible with the current target rule. Preserve the original project file;
   an explicit adapter may produce a selected scratch copy/hook wrapper.
3. Keep the resulting candidate, exact source/import selection and diagnostics.
   Hand the inert candidate to the existing binder/preflight/native-admission
   path. Missing imported local results trigger an explicit acquisition or
   separate checked-export decision, not automatic transitive source execution.
4. Return the exact new checked root/targets and retained publication bytes.
   Do not export scratch assumptions as proved library artifacts. A future
   ordinary-library export is a separate endpoint with its own assurance proof.

An initial adapter need not manage arbitrary Lake plugins. A documented hook
recipe plus one explicit project-environment invocation can expose the boundary
first. Tactics that generate opaque evaluation dependencies or use axioms outside
the fixed receiver policy may fail; source compilation is not compatibility proof.
Name collisions, private/generated names, module visibility and version mismatch
are explicit refusals, not reasons to weaken native checking or silently rename.

## When conventional package sharing is better

Use ordinary pinned package imports when collaborators already trust the code,
need most of that library, and want its established editor/tactic/notation stack.
Cache compiled support and proofs normally. Do not replace this with a bespoke
commons authoring environment just to keep every operation inside our software.
The commons' distinctive prospective value is selective discovery, inert exchange,
independent checking and durable re-serving across otherwise separate operators.
Those gains must exceed added translation/integration/service costs at the same
assurance endpoint; this note does not assert that they always do.

The next decisive evidence is one realistic trusted-project contribution through
the unchanged receiver boundary, only after a source-only compatibility contract.
No large corpus, synthetic growth fixture or certificate campaign is needed to
decide whether that narrow integration is viable. If ordinary package integration
is cheaper and equally safe, keep the commons as its discovery/custody/checking
layer instead of building a competing project workflow.
