# Trusted-project hook: minimal operable contract

2026-10-23; source/theory only, by `project_hook_design`. No implementation,
project import, build, native execution, network or Git operation was performed.
This refines ORDINARY-EXISTING-PROJECT-DECISION; it is not a runtime selection.

## Decision

Keep the owner's normal Lean project for authoring; export inert candidates
from the module that creates the new targets; admit independently using the
existing ordinary receiver. Do not build a package manager or a second checker.
The Lean hooks already support this separation. The public Python contribution
wrapper does not yet support an arbitrary project header/search path.
A documented hook recipe plus a small explicit invocation adapter is sufficient
in principle; compatibility with one actual owner project remains untested.

## Caller inputs and supported environment

- One exact installed ordinary profile, its protected owner/catalog/custody,
  and an immutable selected parent context root; use its S/F identities.
- Already warranted acquired targets `(name, ExportID, UnitID)` and 1–32 exact
  new output names. Names are Lean structured names, not guessed text aliases.
- One owner-approved source module, its module root, explicit ordered module
  search paths and already built project dependencies. Initially support the
  selected Windows Lean 4.34.0/Python 3.14.6 installation only.
- Exact authoring-helper identity and explicit project/toolchain selection;
  preserve source, import/search-path selection and available dependency pins.
  No ambient LEAN_PATH, toolchain switching or helper shadowing is permitted.
- Fresh request/candidate/build/diagnostic paths and one finite aggregate
  allowance covering preparation, authoring, binding, checking and retention.
  Project builds/downloads are not implicit operations inside that allowance.

The project, its macros/tactics/plugins and their native support are executable
owner-approved code. Finite Windows Job limits are not hostile-code isolation.
Never fetch or execute project code just because a peer recommended a theorem.
The native receiver and protected identity lookup remain outside producer code;
this separation is not protection from a hostile actor with the same OS rights.

## Hook placement and source restrictions

The owner adds hooks to a new authoring module or explicitly selected scratch
copy, not by automatically rewriting a valuable existing source file.
Use the project's approved import header plus the pinned meta imports
`PortableOwnerConstructCommand` and `PortableContributionExportCommand`.
After imports, before the new declarations, at top level:

```lean
#ordinary_construct_portable "<request-dir>" "<S>" "<parent>" "<F>"
-- Owner's new definitions/theorems, using the normal project support.
#ordinary_export_contribution "<targets-json>" "<fresh-candidate-json>"
```

Use one construction hook, both hooks in the same module, with
`-DElab.async=false`; preserve Lean module visibility requirements. Public
definitional equality may require `@[expose]` for the relevant definition.
The adapter must preserve the actual module root, not assume the fixed
`OrdinaryProducer.lean` layout. Native outputs go to fresh scratch storage.
Paths must satisfy existing absolute-path/bounded-string rules.

Importing an already compiled target into a separate export driver is refused
(`CURRENT_MODULE_TARGET_REQUIRED`). A new alias still depends on the imported
result; it cannot convert an unresolved library theorem into accepted evidence.
This hook is for newly authored targets, not whole-project/library migration.

## Preparation, interpretation and independent admission

1. Prepare with `portable_owner_request.prepare`, authenticating each selected
   ID and retained evidence through the exact protected parent. Reuse existing
   request limits. `owner_absent` is only a hint; conservative `True` is already
   supported and avoids scanning the entire project for a presence inventory.
2. Construction stops at existing safe local declarations; missing theorem
   handles become scratch axioms, while required missing definitions/groups
   are constructed from selected data. Presence does not prove agreement with
   the receiver. Preserve request bytes, selected bindings and context identity.
3. Compile the approved module with pinned helpers and explicit project paths;
   retain exit status and diagnostics. Export complete new units and the exact
   referenced boundary. Imported unmapped names remain unresolved names.
4. Use `portable_candidate.bind_candidate` with the unchanged protected parent
   lookup. Preserve claimed IDs exactly. Resolve only explicit unresolved names
   to that parent's actual bindings. A missing interpretation is a refusal/
   request for a separate acquisition decision, not an automatic remote fetch.
5. READY is not acceptance: use existing `owner.preflight` and `owner.admit`.
   Retain checked root, exact output IDs, inert evidence and previews using the
   existing contribution retention path. Charge failures and preserve accepted
   state even if later reporting/publication fails. Do not renew the allowance.

Formally, if producer environment E emits `(p,T)` and rho maps used names into
receiver Gamma, successful admission establishes `Gamma |- rho(p) : rho(T)`
under the existing checker assumptions. It does not establish `E = Gamma`,
semantic equivalence of matching local names, or portability of the project.
Expose the receiver's exact statement and identities; do not claim that a
successful build certifies the producer's interpretation. No intention test is
introduced into mathematical acceptance.

Scratch `.olean` files containing assumed theorem handles are not ordinary
proof-complete Lean libraries. Never publish them as such. Ordinary standalone
library export would need checked actual proofs or a separately explicit trust
policy; it is not part of this hook.

## One decisive compatibility case and refusals

Use one owner's real, already working project and a new target T that uses its
normal tactic/notation support, an acquired theorem A absent from the original
project, and an imported local lemma B already warranted at the receiver.
Success means: complete T exported in its authoring module; A/B resolved to
exact protected IDs; independent admission succeeds; resulting inert evidence
remains reusable after the producer module/build directory is unavailable.
This tests integration, not mathematical novelty, large-scale growth or speedup.
If a real suitable project is unavailable, record that dependency rather than
inventing another elementary fixture and calling it ecosystem compatibility.

Explicit refusals include wrong toolchain/profile/context, helper shadowing,
imported targets, output collisions, unsafe/unsupported declarations, partial
existing groups, missing interpretations, unsupported generated/private names,
dependency/byte/time limits and native rejection. Axiom-bearing tactic output
outside the receiver's accepted policy must not gain authority from the project.
Missing B must stop before native admission; a same-name incompatible local B
must never imply equivalence, even if a different receiver statement checks.

## Smallest adapter and stop rule

Existing hooks and preparation/binding/admission APIs suffice for an expert
manual recipe, but no current public command orchestrates this project route:
`assemble_source` fixes Init/helper imports and `author_worker` fixes its helper
paths and source-root/output layout. Select a fresh thin adapter if needed;
reuse the present request, binder, supervisor, budget and retention operations.
Its only new responsibilities are explicit project environment/module invocation
and connecting the same preparation/admission phases around it. Do not patch
frozen source or add arbitrary Lake execution, dependency installation, editor
frameworks, certificates or another environment-equivalence mechanism.

Compare against ordinary pinned Lean package sharing with the same useful
index, warm compiled caches, tactics and assurance endpoint. Count integration,
translation, checking, failed search, custody and maintenance costs. Selective
inert exchange is the prospective advantage, not a presumed universal speedup.
Stop expanding this adapter if safe package sharing serves the workflow more
cheaply: keep the commons as discovery/custody/checked-artifact infrastructure.
After one actual changed-boundary success, prioritize missing useful workflow
capabilities rather than repeated elementary theorem or certificate campaigns.
