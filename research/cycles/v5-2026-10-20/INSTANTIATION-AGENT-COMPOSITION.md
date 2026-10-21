# Local goal to discovery: public composition decision

2026-10-20, core_growth. Source-only; no imports, tests, builds or proof work.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Current selection is `distribution-adaptive-01-input.json` (`a74eaf51`), not a
historical logical-path predecessor. Fingerprint helper `ac32cf53` is unchanged.

## Decision

**Use and document the existing codec-native path. No new admission or import API
is needed for it.** A local agent can construct a bounded formal goal using exact
shared vocabulary already obtained through public descriptors. The target
theorem's ID, name and complete telescope need not be known.

**Do not claim a live Lean tactic-goal exporter exists.** The current frontend
exports successful declaration roots, not arbitrary unfinished `MVarId` goals
and local contexts. An optional agent-side export bridge is a real later
ergonomic seam, but it is not selected by this decision and is not required for
an agent already manipulating the codec. No extra experiment resolves this
source-visible distinction.

## Exact vocabulary available through public APIs

1. An agent obtains vocabulary candidates by an ordinary authorized formal query,
   or retains vocabulary from an earlier investigation. This is independent of
   knowing the theorem now sought. Exact vocabulary identity cannot be inferred
   from a human-readable name shared by unrelated definitions.
2. `client.describe_candidate(candidate)` returns a public copied description
   with `locator.module_id`, `locator.relative_name`, `descriptor.name`,
   `descriptor.universes` and `descriptor.type`. The resolved description also
   carries its group opening. These are authenticated structural data, not yet
   mathematical authority. `codec.export_id(module, relative_name)` derives the
   exact symbol address; no private workspace access is needed.
3. `SemanticReadPlan.stage`, `select_member`, `resolve`/`try_resolve`,
   `fetch_body` and `preview` collect the selected semantic closure. Public
   `resolve` returns its resolved candidate and description, so newly encountered
   dependency vocabulary is also inspectable. `finish` performs actual admission
   and returns a same-client author context. It does not return a goal AST.
4. The direct path is `client.acquire`/the current public admission methods,
   `client.describe(warrant)`, `client.semantic_material(warrant)`, then
   `import_context`. `semantic_material` exposes available opened declarations
   and bodies from actual mixed packets. I/A-member receipts may need separate
   provider/caller semantics; the API reports this rather than inventing them.
5. Retain the explicit descriptors used to select the import. The public
   `AuthorContext` is intentionally opaque, not a descriptor repository. A
   READY context is sealed. For discoveries from several query generations,
   acquire/retain genuine warrants first and make one combined import; do not
   finish a vocabulary-only READY context and assume later extension is allowed.
   See `MULTIQUERY-IMPORT-COMPOSITION.md` for the already selected composition.

For ordinary Lean authoring, `codec.relocated_name(M, n)` denotes exactly
`DMKN.Mod.«M».n`. `AuthorLean.absoluteName` installs that same name; the current
`MixedSourceOperation.finish` maps it back to external `(M, n)`. Reusing the
same imported symbol is different from recapturing a similarly named definition.

## Concrete codec-native example (documentation, not executed evidence)

Assume public descriptions `a_desc` and `r_desc` identify already inspected
monomorphic declarations `A : Sort u` and `R : A -> Prop`. They may belong to
different exact modules. The local agent wants to investigate `R a` for `a : A`.
It has not selected or named a theorem proving that goal.

```python
def external_constant(description):
    module = description["locator"]["module_id"]
    name = description["descriptor"]["name"]
    return ["const", ["external", module, name], []]

A = external_constant(a_desc)
R = external_constant(r_desc)
closed_goal = ["forall", "default", A, ["app", R, ["bvar", 0]]]
alternatives = goal_queries(
    codec, a_desc["locator"]["module_id"], 0, closed_goal, profile,
    context_binders=1,
)
```

This example assumes no universe parameters; polymorphic symbols require their
actual explicit level arguments and wrapper universe arity. The helper validates
syntax, not the assumed mathematical typing. The `owner_module_id` argument
resolves only constant references tagged `local`. Here every nonfoundation
constant is explicitly `external`, so the supplied vocabulary module is a valid
but unused owner: no future contribution ID needs to be predicted. A bound
variable `bvar` is not a `local` constant reference. Do not put a foreign symbol
in a `local` reference unless its actual owner is the supplied module.

For a type copied from module M's descriptor, its `local` constant references
are relative to M; preserve that owner or convert them explicitly to external
references before combining syntax from different modules. `codec.relocate_expr`
returns an absolute-name AST, not codec input accepted by `goal_queries`; do not
pass that different representation to the helper.

Each returned singleton spec list can be compiled by the selected workspace
adapter and tried through existing direct/located successive-query APIs. The
agent chooses and funds attempts, then acquires relevant evidence before its
candidate generation retires. The theorem name/ID appears only after discovery.
Its premises, applicability and actual mathematical admission remain separate.

## Why the current Lean authoring frontend is not a goal exporter

The selected executable is `author-lean-link-01/link/AuthorLean.exe`; its source
lineage is `authoring/native02/AuthorLean.lean`. `SourceFrontend.run` requires
nonempty new declaration roots, completes `Lean.Elab.process`, refuses reported
errors, checks the roots exist, and exports their dependency rows. `dumpExprAux`
and `removeMData` explicitly reject free variables and metavariables. The public
request/export schemas carry source, roots, rows and exact selection binding,
not an unfinished goal/context pair. `MixedSourceOperation` builds that request
from a sealed imported context and returns a candidate delta, not goal queries.

A future optional Lean-to-codec bridge would have to abstract the intended local
context into exactly n forall binders, distinguish local definitions from free
parameters, resolve/explicitly refuse metavariables, preserve exact imported
constant identities and universe scope, and obey the existing input limits.
It must remain an untrusted query producer, with no acceptance authority. Do not
route unfinished proofs through `sorry`, treat generated assumptions as admitted
mathematics, or enlarge the network core merely to provide this convenience.

## Accounting clarification and compatibility scope

The earlier `INSTANTIATION-GOAL-CONTEXT.md` phrase "Charge n stripping visits"
described the intended work accounting, but the implemented public goal helper
returns only alternatives. Its n stripping visits are **bounded local caller
computation**, not an externally settled search/acquisition charge or a returned
cost report. `_derive_conclusion` does return work, and source adapter extraction
adds that source work to its existing extraction limit. This clarification
supersedes that phrase without changing the reviewed historical contract bytes.

The README now explicitly restricts key compatibility to successful validation
within bounds, the same profile, common exact rigid symbol identities, and a
well-scoped raw capture-avoiding instance. It does not cover oversized inputs,
definitional equality, semantic symbol transport or successful retrieval from
an unavailable/omitting index. No helper, acceptance or runtime behavior changed.

## Source anchors

- `conjunction_index/client/workspace_atomic.py`: public description methods,
  sealed author context and semantic-material extraction (selected logical
  `client/workspace_atomic.py`).
- `client/workspace_mixed.py` and `type_pattern/client/workspace_evidence.py`:
  exact mixed/I/A owner semantics and public import results.
- `iterative_queries/client/semantic_reader.py`: public dependency descriptions,
  structural preview and live final import.
- `type_pattern/discovery/module_export_adapter.py`: descriptor/locator data;
  `modules/codec.py`: reference encoding and exact export IDs.
- `interface_views/authoring_atomic.py`: request schema and exact external-name
  mapping; `authoring/native02/AuthorLean.lean`: actual frontend/export boundary.

Stop here: documentation is sufficient for the supported codec-native path;
optional live-tactic ergonomics need a separately selected practical use case.
