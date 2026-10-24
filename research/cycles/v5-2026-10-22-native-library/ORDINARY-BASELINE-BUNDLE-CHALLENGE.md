# Independent challenge: strict baseline bundles before authoring

2026-10-24. Reviewer: `module_anchor_audit`. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
Source/theory only: no implementation, experiment, owner/database opening,
network operation or Git mutation is selected by this note.

## Decision

**A strict, finite inert-bundle onboarding path is a plausible next high-payoff
boundary, but its success criterion must include subsequent ordinary Lean use.**
It should expose the existing checking primitives, not introduce a new trust
mode, progress authority, task scheduler or automatic network fetcher. Root's
selection and the companion contract own any implementation.

The intended user chooses a useful common background before authoring a new
contribution. The supplied bundle contains ordinary complete-proof evidence,
not trusted compiled modules or a saved owner catalog. The local owner checks
its missing units once, preserves its own warrant, and later uses that context
for queries and ordinary Lean authoring. This avoids the artificial requirement
to first author a consumer that fails for a missing vocabulary. No user-supplied
project is available, so a controlled representative is not outside-user evidence.

The strongest open challenge is not another proof of batch-induction soundness.
It is whether a selected realistic background can pass **both** strict intake
and ordinary module realization under coherent finite resource bounds. Merely
lifting a public 32-unit intake ceiling does not answer that question.

## Existing source already permits exact reuse from an explicit root

`OrdinaryAdmission.preflight(parent_root, raw_units, ...)` obtains a warranted
context through `catalog.context(parent_root)` and invokes `_plan`. The source
does not require that `parent_root` be the original root associated with a prior
consumer, nor that it be a particular manifest prefix. It may be any explicitly
selected committed root under the owner's supported semantic policy.

For each supplied complete unit, the existing planner:

1. Parses its exact canonical portable evidence and computes its UnitID.
2. Recomputes every output's ExportID from semantic identity, UnitID and name.
3. Requires each existing output name to have precisely that identity. A
   conflicting name refuses; a partially present group refuses.
4. Classifies the unit as reused only when **all** its outputs are already
   present with those exact identities.
5. Independently verifies the complete imported-symbol census. Every reused
   unit's imports must already match the selected warranted context; no new
   selected unit or manifest hint may supply a reused unit's missing lineage.
6. Topologically orders only new units and reports missing dependencies or
   cycles rather than inventing axioms, aliases or provisional acceptance.

`admit` then recomputes this plan from its raw evidence; caller-supplied status,
order, missing list and reused-ID list are not trusted. If every selected unit
is reused, it returns `REUSED`, the same root and zero checked units without
launching native checking. Otherwise only the new complete units enter the
existing checked-extension path. Atomic local promotion remains the authority.

Consequently, **a new persistent cursor/journal framework is unnecessary for the
first bundle intake slice**. On a later explicitly authorized call, the caller
can choose an already warranted root and the same exact bundle. Existing
whole-unit tests determine what is missing. A manifest ID may record input
selection, but its claimed progress never overrides the protected catalog.
An unrelated branch with incompatible bindings refuses; the importer is not
authorized to silently merge, rename or rebase it.

This conclusion applies to onboarding before authoring. The existing retained-
consumer completion path deliberately binds its original parent/prepared map;
it should not be weakened or silently redirected to a new root. No such consumer
exists in the proposed first workflow, so no rebase adapter is needed.

## Precise safety statement and its limits

Let `K` be the actual warranted selected context, `U` a finite collection of
exact portable complete units, and `N` the units `_plan` classifies as new.
Under the existing codec, exact-identity, kernel and protected-storage premises:

```text
Warrant(K) and current-preflight(K, U) = READY
and successful existing native checking/promotion of N
    imply Warrant(K') and preservation of every prior binding in K.
```

If `N` is empty, `K'=K`; no new mathematical capability was established by the
reuse return. For several batches, apply the existing checked-prefix induction
to each actual committed result. A bundle manifest, copied `.olean`, source
compiler success, cursor or prospective root cannot supply the induction premise.

The existing planner's finite ceilings are 1,024 units, 64 MiB of evidence,
2,097,152 encoded nodes, 65,536 output names and 1,048,576 import edges per call.
These are maximum accepted shapes, not promised performance or a new allowance.
Smaller selected limits and all existing catalog/custody/storage caps still
apply. Recursive declaration groups remain atomic even when one group would
not fit a chosen batch. Refuse an oversized group rather than splitting it.

The safety implication does not establish that all advertised targets were
delivered, that a theorem is useful, or that a local ordinary Lean project can
use the accepted context. Successful completion must additionally check the
explicit requested target identities against the final real context. Partial
valid progress must be reported as partial, not relabeled complete.

## Minimum input and orchestration boundary

The companion contract should select a finite immutable manifest, exact input
hash, bounded per-unit files, an explicit completion criterion, explicit starting
root and one original total allowance. Evidence identities remain the existing
portable identities; a manifest is packaging metadata, not a new calculus or
an acceptance certificate.

The reviewed minimal contract defines completion as admission or exact reuse of
**every listed complete unit**. That is sufficient without an additional target
list. If a later producer promises selected entrypoints, those exact identities
must additionally be checked; they must not excuse omitted listed evidence.

Metadata can guide file selection and batching, but its claimed UnitIDs, names,
imports, sizes and ordering must be checked against actual bounded evidence
before those claims affect checking or completion. Use existing path/size/hash
guards, no executable archive entries, symlink traversal, remote-selected local
paths, project scripts or compiled modules. Inputs and partial outputs stay
preserved. If future bundle production needs archive extraction, that is a
separate explicitly bounded implementation boundary, not implicit here.

A simple deterministic batch planner can order exact unit dependencies and fill
each batch subject to all selected caps. It need not solve an optimal packing
problem. Dependencies must come from the real selected parent or earlier new
units. No hidden missing-dependency download or endless retry belongs in this
initial local onboarding operation.

Any saved plan is a convenience record. At each actual step, the existing
admission API revalidates the precise batch against its explicit actual parent.
The UI/API can report last confirmed root, next unprocessed candidate units and
known charges without introducing an authoritative progress database. Choosing
a root in a later command is a fresh explicit operation, not revival of a prior
native grant or continuation based on a trusted cursor.

## Reuse is not zero work; account for the real costs

The current implementation does not magically skip the bytes of supplied reused
units. `_plan` reparses them and checks their imports. `admit` stages and reads
back **all** `actual.raw_units`, including exact reused units, before deciding
that no new units require checking. Idempotent custody avoids duplicate durable
objects, not all parsing, hashing, database or I/O work.

Likewise, `catalog.context` reconstructs the selected chain. Retained artifact
hashes are reused once per owner process, but fresh processes revalidate selected
snapshots, and fresh native extension workers load their selected parent context.
For batch sizes `b_j` and prefix sizes `s_j`, a cost model must include terms such
as `sum_j Load(s_j)` in addition to `sum_j Check(b_j)`. Many tiny batches can
therefore impose poor cumulative costs despite no ancestral theorem proof replay.

The importer must distinguish:

- Reusing previously **checked mathematical authority**: allowed by exact
  whole-unit matches in the actual selected context.
- Reading/validating a previously processed manifest prefix: still work and
  still charged if performed again.
- Rechecking an already warranted theorem proof: not required by `_plan` reuse.
- Loading selected parent native artifacts: may still be necessary and costly.

Do not call a repeated full scan a zero-cost resume. Conversely, avoiding that
scan by trusting an unauthenticated cursor would be the wrong optimization.
First use the bounded exact implementation and name its cost; only a demonstrated
bottleneck could justify an additional index of prior checked units.

Every batch grant must be derived from the remaining original wall/CPU allowance,
not reset to the full configured budget. Charge controller work, actual inclusive
child CPU once, failed attempts, retained call spool and custody/snapshot storage.
The native core's call spool is separately bounded per operation and is not
charged to the catalog snapshot-byte quota; aggregate disk planning must include
it rather than treating the catalog quota as a complete disk cap.

There is a concrete accounting pitfall: `OperationBudget.worker_cpu` starts at
zero, and `_execute` increments it only when final Job CPU is available. If a
native-path exception leaves no final accounting, zero is not proof that no
native CPU was spent. Reserve the batch's selected allocation before entering
it. In the now selected nonrefundable-grant mode, retain that entire reservation
even if the final CPU observation is missing. A known clean successful admission
may continue under the remaining reserved envelope: no measurement is needed to
refund a grant because no refund is performed. Label observations as partial,
never as zero actual expense. Unknown checking, commit or cleanup outcomes still
stop. A future refund-based mode would need explicit trustworthy final accounting
before releasing any reservation; unknown failures cannot justify a refund.

## Commit uncertainty must stay explicit

The current catalog catches uncertain transaction outcomes, closes the owner and
raises `CATALOG_TRANSACTION_UNCERTAIN_REOPEN_REQUIRED`. A COMMIT exception does
not prove rollback. The wrapper must stop, preserve evidence and report that
actual durable progress is unknown. Its last confirmed root is not a claim
that no later root committed.

Only a later explicitly selected reopening and actual protected catalog/context
validation can determine which roots exist. Existing status/context operations
can support that decision; opening the owner can settle abandoned reservations
and is not advertised as a purely read-only database operation. No immediate
automatic retry, replacement budget, deletion of an uncertain root, or guessed
promotion is justified. A reporting failure after a known successful promotion
must preserve the known accepted result instead of presenting it as rollback.

## End-to-end blockers that must remain visible

The companion `ORDINARY-NEXT-RELEASE-BOTTLENECK.md` correctly identifies the
ordinary materialization barrier. Current module realization admits at most
32 new units per request with a 4 MiB request bound; anchor chains permit at
most 32 modules and 1,024 units total. Thus accepting the retained 2,852-unit
closure is insufficient: splitting it into 90 small module calls violates
both the chain and total-unit limits. These are not bypassed by more grants.

Before an importer is represented as usable common-library support, root must
select a coherent finite baseline realization profile or another justified
ordinary-use route. That requires coordinated limits for request bytes/nodes,
new units, chain length, total units/names, artifact parts and aggregate cost,
while preserving exact interpretation/private-public checks. The interactive
delta profile can remain small; silently enlarging one field is not a design.

Evidence production also remains separate. Existing closure-export machinery
does not by itself provide a public complete baseline producer independent of
retained-consumer extraction, nor guarantee affordable private module imports.
Using retained inert evidence can test intake without rerunning expensive
extraction, but a release needs a usable way to obtain an appropriate bundle.
Name preservation/conflicts, compatibility with ordinary imported projects and
re-export/query vocabulary must be resolved for the selected representative.

The saved 2,852-unit admission/recovery result already shows that this selected
class of strict cold checking was not inherently infeasible on this PC. Reuse
that evidence; do not repeat it merely to give the same operation a new name.
It does not establish affordable complete Mathlib onboarding or subsequent
ordinary realization. Operator-approved compiled baselines remain a possible
different-assurance alternative, not the selected default or an excuse to label
assumed base soundness as independently checked mathematics.

## Payoff and next decision

The proposed payoff is removing a concrete workflow barrier: establishing a
common formal vocabulary once, then using it repeatedly. No new theorem-count
or exponential-growth claim follows. The strong comparator gets the same
background, ordinary Lean package manager/build cache, previewing and local
indexes; independent checking and representation conversion must earn their
extra whole-cost burden through actual useful exchange under the stated trust
policy. Amortization is a model, not evidence that any number of later uses will
occur.

The next decision should require one coherent input-to-ordinary-use contract,
source-derived feasible finite envelopes, and only changed-boundary tests.
Primitive intake without a viable materialization route can be useful internal
progress, but must not become another long mechanism campaign detached from
usable mathematics. No generic scheduler, network bundle protocol, custom
cursor journal, trust waiver or new proof-production campaign is needed now.

## Exact source evidence

The reviewed current source identities are:

| Source below `software/v5/` | SHA-256 |
|---|---|
| `ordinary_lean/ordinary_admission.py` | `9653a710a089393d189830a26aa8dd0723ee75859ce577d9713dae569b5e8575` |
| `ordinary_lean/portable_catalog.py` | `aeaf0c7d507baa6b63d401c432ca71557bf29b6b576b1f6cd8381e4e87c7473e` |
| `ordinary_lean/portable_evidence.py` | `f8ea819bdd9344d696cef2725888828125b2ef5d1b60d2c31a0412657a62cbd8` |
| `ordinary_library_package/completion_api.py` | `76767855da84ee64cfe6c70098b2671a5c3523643803b034b3de6b151bb74982` |
| `ordinary_library_package/library_completion.py` | `b587c74e156c81a392f394b263b27b13de427753c41009ecc3b99193f88b93d9` |

The source-derived companion bottleneck note reviewed here has SHA-256
`79eebcbeed24979943674c29dcdbf51c87612daf24ee54054c6be599ba0ddc6b`.
Its broader baseline proposal is not treated as implementation authority. The
baseline contract reviewed after this initial note has SHA-256
`fe21a2353417f7b5fd35823d2cd1e097f1dfd076f46e63b88f77d304b791b17b`.
Its prospective binding projection is explicitly planning-only; actual admission
replans against the real committed parent. Its all-listed-units completion rule,
cross-batch backward-only dependency rule, conservative unknown-CPU reservation,
complete custody quota accounting and uncertain-commit stop are consistent with
this challenge. No blocking source/theory defect was found in that bounded
contract. This is not permission to implement it ahead of the realization choice.

## Higher-payoff semantic decision: existing installed complete units

Source review of `OrdinaryModule04.lean` finds a barrier prior to numeric
capacity. `classifyUnits` refuses any installed non-theorem/group collision even
when every actual record equals the corresponding already warranted evidence.
Thus a larger bundle facade alone cannot make a normal Init-heavy background
operable. Fixing this semantic boundary is plausibly higher payoff than adding
a batch wrapper or raising limits first.

A justified generalization must preserve two distinct premises:

1. **Warrant:** the protected controller obtains the exact complete raw unit
   from its independently admitted context and checks its output/import
   identities. Neither `decodeUnit`, an inventory JSON object nor an installed
   `.olean` supplies this premise.
2. **Correspondence:** the actual private and public imported environments
   represent those same warranted records, under the same foundation and pinned
   kernel semantics. Ambient installed names do not become warranted names.

For a warranted unit with output set `O`, require either no installed output or
every installed output in `O`; a partial group refuses. The absent case keeps
the actual checked-extension path. The present case must compare every full
private inventory row, including exact kind, universes, type and all remaining
semantic fields. The codec retains:

- Definitions' values, reducibility hints and `all` metadata.
- Opaques' full values, safety flag and `all` metadata.
- Inductives' parameter/index counts, complete `all`/constructor lists, nested
  count and recursion/reflexivity/safety flags.
- Constructors' owner, index, parameter/field counts and safety flag.
- Recursors' full group list, parameter/index/motive/minor counts, constructor
  cases, full right-hand-side expressions and `k`/safety flags.

For non-theorems in the selected public interface closure, the public view
must expose exactly the same full inventory,
not merely a type or an axiom-shaped placeholder. Existing theorem proof-erasure
handling remains theorem-specific: its permitted public signature-only view is
conditional on the full private proof match and earlier independent warrant.
It cannot be generalized to definitions or opaque bodies. Hidden or differing
public computation semantics must refuse.

The group census is important but must not be justified circularly. Existing
strict `CheckedExtension.checkBatch` checked the descriptor, compared generated
inventories and performed the exact stage-two no-unadvertised-output census.
That retained event is what establishes that the selected evidence describes a
complete generated group. Merely observing the named expected rows in a larger
environment would not establish completeness for untrusted evidence. Conversely,
an additional whole-environment `indexSource` pass is not automatically necessary
when exact complete warranted inventories already exist. Reconstructing an
original inductive descriptor with `BootstrapProbe.makeUnit` is not a universal
identity criterion: nested inductives can have expanded generated representations
that need not reconstruct the exact original descriptor. Preserve the original
warranted descriptor and match its actual complete generated records.

The closure argument also has a precise boundary. `decodeUnits` permits only
the fixed basis, registered anchor outputs and prior selected whole-unit outputs;
it does not authorize arbitrary ambient declarations. The portable import census
binds expression constants/projections in descriptor and inventory expressions.
It does **not** separately list every `all`/constructor metadata name or implicit
literal root. Therefore:

- Complete inductive group metadata must be justified by the prior checked
  generated census, not by an assumed new import-census guarantee.
- Literal/quotient and other pinned native reductions remain fixed-foundation
  obligations. Successful matching does not allow arbitrary native support.
- Ordinary non-inductive `all` metadata may contain more than one name even
  though this codec's unit inventory is singleton. The pinned runtime's
  `Lean/Declaration.lean` explicitly documents `DefinitionVal.all` as **not used
  by the kernel**: it retains source mutual-block information, while recursive
  definitions are compiled using recursors and `WellFounded.fix`. `TheoremVal`
  and `OpaqueVal` refer to that same comment. Thus exact equality of this
  metadata is required by our identity contract, but its names are not thereby
  extra semantic assumptions needing independently warranted import edges.
  Restricting it to singleton form could be an explicit frontend compatibility
  choice; it is not a demonstrated kernel-soundness necessity. This corrects
  the earlier conservative uncertainty, using the documented pinned-runtime
  contract rather than claiming a formal proof of the unavailable C++ kernel.
  Inductive/constructor/recursor group metadata is a different case and keeps
  the full checked-census and semantic correspondence obligations above.

An appropriate conditional statement is:

```text
Warrant(K, U) and closed selected identity interpretation
and exact private full-record correspondence for U
and exact public non-theorem correspondence plus permitted theorem view
and actual new-delta checks under both imported views
and exact artifact binding plus successful private/public rereads
    imply a reusable representation of those selected warranted declarations
          and the checked new delta, under the existing kernel/profile premises.
```

This is a source-derived refinement argument, not a machine-checked proof of
Lean's kernel, importer or correspondence adapter.

### All-matched generated wrapper is an explicit A1 case

Current source refuses both `addedUnits.isEmpty` and a pending matched-count
equal to the raw-unit count. If the selected background is entirely installed,
a generated-wrapper successor must explicitly support or explicitly refuse that
case. If supported through a wrapper, no dummy theorem should be inserted. Skip
`checkBatch` only for
the empty added set, since there are no new declarations to check; still run
all private/public matches, exact import/header checks, actual module writing,
both fresh-process rereads and protected registration. The emitted own-constant
census should be empty. Report zero checked declarations/passes truthfully,
distinct from correspondence validations. A useful wrapper is not new mathematics.

The report parser, realization enumeration, Python anchor-record validation,
support identity and later warm validation must all agree about complete-unit
matches and the empty-own-output case. Changing only `classifyUnits` is not a
coherent implementation. Frozen earlier artifacts cannot be relabeled into the
new correspondence rule. This reviewer selects no implementation or runtime.

The later reviewed A2 contract makes a better distinct choice: an all-matched
baseline registers an exact original-library reference, without generating a
wrapper at all. That operation has no new module to write or reread and no
`checkBatch` call. Its authority comes from the live exact private/public
correspondence, validated snapshot and protected record-last registration.
Actual generated deltas still require their writer and both fresh rereads.
These result types must not be conflated to satisfy old nonempty-output fields.

## Whole-workflow alternative: preserve the approved ordinary project

Root proposes avoiding mass reification by importing owner-approved local
project modules with their ordinary notation, instance, simp and tactic state,
while emitting only remote/new deltas. This is a **strong practical candidate**:
bare `ModuleData` reconstructed from mathematical declarations does not recreate
arbitrary frontend metadata. Metadata available through its actual dependencies
still imports normally; current dependencies do not include a user's arbitrary
library. A user expects their existing tactics and notation to work. This route
deserves a source contract before bulk materialization.

There are two different authorities, which should remain separate:

- The owner may authorize existing local code/modules/plugins to execute while
  authoring. This is already the approved-project authoring model, not a sandbox.
- Mathematical acceptance still comes from strict local admission and exact
  correspondence of selected used units to that warranted context. Local code
  approval does not assert every project theorem or artifact is mathematically
  sound. Unrelated imported names cannot become portable accepted symbols.

Consequently this alternative need not introduce the weaker approved-base trust
mode. It can retain the strict base while preserving ordinary project usability.
Each exported contribution must still be independently admitted with exact
complete imports; a compiler success is merely candidate production. A local
source project containing a false unrelated axiom need not be globally certified,
but any selected result depending on it must be refused by the strict boundary.

There is a concrete missing implementation boundary: current
`TrustedProjectAuthoring` and `library_extraction.py` explicitly approve paths
and execution without pinning all transitive artifact contents. Such a selection
cannot be promoted unchanged to a warm semantic correspondence anchor. Either:

1. Register the exact semantic artifact/import closure, check selected used
   records under both required views once, preserve those bytes and validate
   their identity at reuse; or
2. Freshly compare the selected used records against their warrant on each use,
   accepting and accounting for that repeated work.

Neither option is an ambient `LEAN_PATH` shortcut. Resolve shadowing, exact
module/import identities, hidden definitions, complete groups, fixed literal
support, partial/missing private artifacts and changed files explicitly. Semantic
artifact integrity and permission to execute frontend plugins are different
claims. A source plugin can alter the frontend environment after import; thus
an initial module correspondence check cannot by itself authenticate the final
extracted proof. Keep correspondence at the actual extraction/use boundary and
keep final independent admission. Any generated remote delta that needs private
conversion unavailable to ordinary public consumers must still refuse or use
an explicitly justified different representation.

The next high-payoff decision is which of these two compatible mechanisms best
supports a real user workflow: exact installed complete-unit matching for the
existing runtime, and/or explicit selected project correspondence with a small
delta module. A strict baseline bundle is useful infrastructure only once that
ordinary-use route is coherent. This avoids committing to a large scheduler or
another certificate campaign before resolving the actual semantic bottleneck.

## A2 contract review: private proofs are not public computational interfaces

Read the revised `ORDINARY-BASELINE-REALIZATION-CONTRACT.md`, SHA-256
`258846eb77c5da80c2cd03fe7a79e2fbed386304e8a5cc7ec75295d51f33c9e1`.
The actual-public-view closure amendment resolves the substantive overrestriction
identified in review. No source/theory blocker remains for this sufficient
relation. Implementation and finite actual validation are separate gates.

Let `Q` be the complete private evidence/unit closure of exact requested exposed
targets, and `P` the public interface closure. Every unit in `Q` must have its
full accepted warrant and exact private correspondence. Derive `P` from the
actual imported public representation, closing at complete-unit boundaries:

1. Start with the request's exact exposed target identities, not every accepted
   name or every name appearing anywhere in private proof history.
2. For an actually erased, permitted singleton-theorem handle, include exact
   type references only. Its proof and proof-only support remain in `Q`.
3. For a full actual public `thmInfo`, include full proof references too. The
   theorem label alone does not prove its body cannot affect conversion.
4. For definitions, opaques and complete inductive/generated units, keep full
   exact public rows and their computational/type support. Group selection is
   atomic. Preserve the fixed foundation's implicit literal/primitive contract.
5. Iterate under bounded unit/name/edge/node limits until closed. An unsupported
   or hidden required public dependency refuses. Non-inductive `all` metadata
   is retained exactly but is not a new semantic dependency, as documented above.

This allows a theorem `t : T` with an erased public proof to be reused when its
private proof depends on a hidden helper `h` that is absent from `T`. It does
not allow a public definition that actually computes through `h` to waive the
full public meaning of `h`. If the public theorem still carries its full proof,
that proof's support is retained conservatively as well. Thus this is a smaller
public **domain**, not an abstract-definition relaxation or new axiom policy.

Only protected `P` outputs may form the delta collector's cut boundary and both
delta decoders' allowed set, alongside the fixed basis and preceding checked
new outputs. `Q \ P` must not leak through an all-context binding map. A later
delta needing a private-only member requires a separately established public
closure extension or an honest realization refusal. An already accepted theorem
can remain mathematically accepted while its chosen ordinary public
representation is unavailable; those outcomes must be reported separately.

The native matcher derives full/erased modes from actual records. Caller labels
such as `proof-only` are not authority. The protected reference binds exact
expose targets, complete private closure, derived public unit/output membership,
projection modes, current warrant/support identities and immutable snapshot.
Two different interfaces over one baseline must not share an ambiguous cache
entry. Dynamic frontend plugins remain owner-approved code; their later output
still undergoes exact extraction and independent admission.

The revised contract also correctly distinguishes all-matched reference
registration from generated modules, fixes the concrete exporter's eager
`indexSource` census cost, and preserves original frontend artifacts under
controlled later module-name resolution. Do not weaken the artifact snapshot
requirement to a mutable directory or project-selection hash.

The companion producer amendment reviewed at SHA-256
`c21182e96a12a87df1a7af494f32c7d4b0dc06b03cd0b62669c50e11642ec2c1`
has no identified contract blocker: a parameterized local exporter plus pure
fixed-seed V2 envelope/whole-unit batching loop can produce inert claims without
a fake protected context. Export is not kernel admission. Wrapper/portable
overhead can make near-limit output refuse, and private imports plus JSON
construction are not constant-memory. These are explicit refusal/cost bounds,
not claims that a 64-MiB file fits every available process budget.

Root subsequently selected only the disjoint fresh producer, binder and intake
source seams in `ORDINARY-BASELINE-IMPLEMENTATION-SELECTION.md`. No matcher,
runtime or public adoption follows from this theory review. The first useful
integration must still reach original-library use and a strict reciprocal
contribution; a passing bundle parser is not the project outcome.

### Additional source pins for this amendment

| Source below `software/v5/` | SHA-256 |
|---|---|
| `ordinary_lean/OriginalDecl.lean` | `bfb5fc910808d9dc178977cfa6edeacf0b5cbfe7bd99bc6277ee11a456d516c1` |
| `ordinary_lean/CheckedExtension.lean` | `4c3f3d600eda6319dd6d4578797e16ae6dc0ab81cf97ca4d7bce014081463ea1` |
| `ordinary_lean/BootstrapSupport.lean` | `8a5771cc9f4e51cc0072959174bdc3a917bb0684b3dfdc8cdda2318bb8fd1bb0` |
| `ordinary_module_anchor/OrdinaryModule04.lean` | `901e4fc06351f6ad658eba9b5ea23ab644648646c8567fc035b057aa1883cfe8` |
| `ordinary_project_package/ordinary_contribution.py` | `b8eefe6af368d8a7f5c498d563a12b31416c48c877ea471361eadd2a56a90b31` |
| `ordinary_project_extraction/library_extraction.py` | `cd79d9050fbc80a94faef845ddf99fe7d1b8ba5e376048aa4a7698f06f396061` |

The additionally inspected runtime source
`software/runtime/lean-4.34.0-windows/src/lean/Lean/Declaration.lean` has SHA-256
`fcb928c1686f0655279a790f92bd61f8c0d6df3be51a5eccaa2880de058e5e24`.
Its `DefinitionVal`, `TheoremVal` and `OpaqueVal` documentation is the source
evidence for the non-inductive `all` distinction, not proof of native C++
implementation conformance.

## Independent source clearance: bounded baseline producer/intake controls

Reviewed the complete native producer and pure binder, the complete intake with
its final changes, and the controls/selector including the final 24-case revision.
No remaining source blocker was identified for the selected bounded **inert
syntax/planning control**. This reviewer performed only source/evidence-file
reads and this checkpoint edit: no native build, test execution, owner opening,
database opening, network operation or Git mutation.

| Source below `software/v5/ordinary_baseline/` | SHA-256 |
|---|---|
| `BaselineExporter.lean` | `403f1f4369cd73ea905265f3df42d52f70c68cb5d4f24c03b696dd65f2fc629e` |
| `baseline_bundle.py` | `d5a9c13392e2de8b170cbaf4a9a27e4d1e5d99eb2714165848a640069fe42fce` |
| `baseline_intake.py` | `b5a17aa580f8d9cfdeaaded7d93c2b12ad6e19e5018bf5e7c087cb56760069d8` |
| `controls.py` | `a9b1bdd6382cc1f46e663d72f2be405a8539e0d187d5d8d5d4f0d469972c28b7` |
| `select_controls.py` | `71e1ea3768a632dcf5d9a1440a3f7a24c98185ea881a0ea5354f376c7acd348d` |

The producer requires an explicit approved project-root/module/target request,
uses the existing complete-unit exporter and fixed inventory, and emits inert
candidate data. Its source indexing is eager, not a constant-memory or
already-checked-library claim. The binder authenticates the exact fixed inventory,
constructs current V2 unit/export identities, rejects forward or unbound imports
and duplicate outputs, and deterministically partitions whole units. Its bounds
do not make full writer parsing streaming; the outer resource envelope remains
necessary.

The intake uses the existing strict admission owner, not direct promotion. It
first validates the entire bundle against a disposable exact binding projection;
then each live batch is reread, preflighted and admitted against the actual last
confirmed root. Exact whole-unit reuse is valid above any explicitly selected
compatible protected root. The projection is not a warrant and no automatic
root selection or rebase is introduced. Existing custody bytes and locators are
checked; prospective custody accounting includes locator overhead. A later
failure retains the confirmed prefix and full consumed reservations. An exception
during admission can mean an unreported commit and is not described as rollback.

Review found three preflight/accounting defects, all corrected before this
clearance: the worker's separate hard 16-MiB wrapper-plan bound now includes
wrapper fields and future root spelling; aggregate binding bytes count a single
canonical array rather than repeated array brackets; an all-reused bundle is no
longer refused merely because its unused output allowance exceeds a lowered
per-artifact cap. Full finite per-batch CPU grants are nonrefundable; incomplete
worker observations are explicitly labeled
`PARTIAL_CORE_OBSERVATION_NO_COMPLETENESS_CLAIM`. This bounds authorized work
without pretending that absent measurements are actual zero CPU. Unknown
admission/cleanup/commit state still stops the sequence.

The controls use the actual parsers and planner plus three pinned small retained
proof-data fixtures. Their synthetic contexts, custody, filesystem, commits and
worker outcomes are explicit doubles. The fixtures have the required dependency
chain: `applyTwice_eq` imports `applyTwice`, and `applyFour_eq` imports both. The
generic refusal helper catches `ValueError`; the actual catalog refusal type is
`CatalogError(ValueError)`, so these expected-refusal checks are well-typed.
Every successful intake case checks exact aggregate binding-array bytes; the
final all-reused/lowered-artifact-cap regression and partial-observation label
assertion are present. Forward dependencies and later metadata conflicts must
refuse before any admit; changed later bytes retain the confirmed prefix;
simulated commit-then-lost-response retains uncertainty and does not retry.

Forbidden mocks cover SQLite connect, subprocess creation, sockets, owner/native
opening/execution, protected catalog promotion and custody construction/writes.
The known package bootstrap before those mocks is read-only support loading;
source identity and shared-helper identity are checked. This does not qualify
the mocked storage/commit implementations or genuine Lean acceptance. The
synthetic preexisting logical-byte counter omits locator cost, but the locator
capacity refusal starts empty and therefore still tests its intended new-byte
accounting; this is not a full persistent-store quota campaign.

The selector retains only the prior frozen package and Python/Lean input pins,
adds exact fixtures and the three explicit source hashes, and selects fresh
output/source snapshots. It does not reuse a former operation or allowance.
Its proposed outer limits are 60 wall seconds, 35 CPU seconds, 768 MiB and two
active processes; controls additionally enforce 45 wall/25 controller CPU.
Root alone may select/launch the one bounded run and adopt its saved outcome.

This clearance does **not** establish A2 reference registration, a native
baseline build, original-library public reuse, broad library compatibility,
useful-growth benefit or deployable v5. Those central unfinished boundaries
remain explicit; no extra campaign is selected by this review.

## Saved outcome audit: ordinary-baseline-controls-01

**PASS for the selected real syntax/planning boundary with inert owner doubles.**
Independently read the saved selection, command, complete 24-case result,
stdout/stderr sizes and outer closure receipt. Rehashed all 155 selected runtime
inputs and all five frozen source snapshots: zero mismatches. Both retained
selection files have the selected hash. The three held proof-data fixtures and
selected package/support bytes remain unchanged. This is saved-evidence review
only; no control, native operation or state-opening was rerun.

| Saved artifact | SHA-256 |
|---|---|
| `ordinary-baseline-controls-01.selection.json` and copied `selection.json` | `87642e3e603716552f00a9cf0f759f78e4efa8e3b53ffdc13a89f1a6141574c7` |
| `ordinary-baseline-controls-01/RESULT.json` | `db33440f96ddd20b3a8dc40cd5c1134b64e6ba5dbd33840c35bedc8eadd37eb2` |
| `ordinary-baseline-controls-01/controls/RESULT.json` | `0258777c7ae239677d0ecebe7ba35209a0665b668d293c1e05ecd13bd00e3c14` |

All paths in that table are below `experiments/v5-local-checks/`. The saved
command uses the selected isolated/no-site/no-bytecode interpreter, immutable
source snapshot, exact preview package, fresh output and canonical cwd. Limits
match the selected 60 wall / 35 CPU seconds, 768 MiB, two active processes and
one-MiB stdout/stderr caps.

The result contains the exact 24 selected cases, including the retained proof
unit split/bind positive, eleven expected syntax/budget refusals, four successful
mocked-intake cases, six before-admit metadata/capacity refusals and two
after-prefix stopping cases. Successful cases report the exact 668-byte aggregate
binding array for three units/three names, 10,672 proof-data bytes, eight edges
and 248 nodes. All-reused cases report zero planned native launches, zero new
snapshot/spool reservation and unchanged root, including the lowered per-artifact
cap case. The compatible independent-root case reuses two units and plans only
the one new unit. These are planner/double results, not genuine new admissions.

All six metadata/capacity refusals have zero admit calls and no unreported-commit
claim. Changed second-batch bytes retain the first confirmed root, charge only
the already reserved two CPU seconds and report no possible unreported commit.
The deliberate commit-then-lost-response simulation makes exactly two admit
calls, retains only the first confirmed root, keeps the full four-second CPU
reservation and reports `possible_unreported_commit: true`; no retry or rollback
is asserted. Every intake result retains the partial-observation label and
`ordinary_library_registered: false`. No forbidden operation was called;
`mathematical_acceptance` is false.

The actual outer run exited zero, reaped its direct child, reached zero active
Job processes, closed the Job and reported no cleanup errors or requested
termination. Logs are 84 stdout bytes and zero stderr bytes. Outer elapsed time
is 4.145423599984497 seconds; known child Job CPU is 3.140625 seconds and outer
wrapper CPU is 0.734375 seconds, totaling **3.875 known CPU seconds**. The nested
supervision CPU field is part of wrapper work and is not added again. Reported
peak Job private commit is 53,825,536 bytes. The control's own 3.043082 wall /
2.9375 controller CPU values are contained in that outer operation, not another
cost to add. These are scoped observations, not a hermetic-toolchain or exact
whole-machine resource claim.

The one selected run is complete and should not be repeated. Its used sources,
inputs and results remain frozen. Native producer compilation, controller
execution, protected baseline admission and A2 registration/use remain separate
unfinished gates; this passing syntax/planning control does not complete v5.
