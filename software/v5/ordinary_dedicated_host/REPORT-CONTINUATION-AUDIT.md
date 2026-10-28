# Continuing from earlier reports without treating them as warrants

2026-10-28. Independent source-only architecture audit. **The narrowly selected
field-extraction opt-in is sound under the current product's existing trust model.**
It removes an offline preparation restriction; it does not establish equivalence
of packages, import old acceptance into new state, or waive current native checks.
No code, test, product import, owner/database access or Git operation was performed.
The implementation successor is selected separately under
`../ordinary_report_selection/SELECTION.md` and still needs its own source review.

## The actual restriction and the smaller authority boundary

The current operator companion requires `report.profile_sha256 == PROFILE` in
`Inputs.report`, `accepted_report` and `query_specs`. This is useful default
consistency checking, but PROFILE includes auxiliary software. Adding hosting or
changing query preparation changes PROFILE even when the installed implementation
and the selected local catalog remain unchanged. The offline helper consequently
refuses some continuations which the current public product already supports.

The old report is not the warrant. For parent/acquired/frontier selection, it is
a convenient bounded encoding of identifiers the caller could otherwise type:

\[
x=(r,\;[(n_i,e_i,u_i)]_i,\;r_f),
\]

where `r` is a selected local root, each triple is a declaration name/export/unit
identity, and the optional `r_f` is a selected authoring ancestor. The fresh
request still chooses state, source, project approvals, contacts, budgets and
outputs explicitly. None of those is recovered by following report-contained
paths or executing report-contained commands.

Let `Extract(R)` produce only those identifiers, and let `Run(P, S, x)` be the
existing current product running with its approved support `P` and protected
local state `S`. If preparation emits the same public inputs as explicit selection
of `x`, and `Run` preserves all its actual-state checks, its acceptance assurance
is the assurance of `Run(P, S, x)`. No inference from the truth of `R.ok`, the
trustworthiness of its author, or compatibility of its former PROFILE is needed.
The report's success/closure checks remain conservative workflow checks; they
are not what makes the mathematical reuse safe.

This argument assumes the existing current product and protected local storage
are trustworthy within their documented model. It does not show that a buggy
checker becomes safe merely because it revalidates fields. Wrong selections may
still consume a bounded allowance, create diagnostic files or choose an unintended
but valid local branch. Preparation success must not promise runtime success.

## Actual consumer chain

The reviewed dedicated-host package is PROFILE `21bcb169...`; the following
selected product sources remain unchanged by the proposed operator-only work.

| Consumer | What the current code actually validates |
|---|---|
| Owner opening | `ordinary_parse_reuse/ordinary_admission.py:OrdinaryAdmission.open` binds the actual installation, selected custody semantics and separated state/support paths. `ordinary_lean/portable_catalog.py:_open` constructs the exact expected ADOPTION marker from current implementation, store ID and limits, checks it, and acquires the owner lock. An equal path string alone is insufficient. |
| Parent root | `PortableCatalog.context` reads the selected actual root and its lineage, checks stored record/origin bindings, implementation/semantic/foundation requirements and retained artifact hashes. A report cannot add a root or supply substitute bindings/snapshots. Native snapshots are local warrants under the existing model, not portable report authority. |
| Receive | `ordinary_multi_source/peer_api.py:receive` validates the current record namespace and explicit contacts/config, then calls `owner.catalog.context(parent)` before network I/O. Exact preview/evidence binding, dependency planning and `owner.admit` still execute. The old parent report is not passed to admission. |
| Intake | `ordinary_intake_progress/baseline_intake.py:intake` validates the selected manifest and actual parent context, reads exact bundle units, preflights each batch, then calls the live owner's admission. Producer status/targets cannot substitute for these calls. |
| Contribution targets | `ordinary_demand_frontier/ordinary_contribution.py:_acquired` checks bounded names and the export-identity formula under current semantics. `request_targets` requires each identity to equal the actual parent's warranted name binding. Selected unit locators/evidence are fetched from actual custody and rechecked. |
| Contribution result | `contribute_source` binds the generated candidate to the exact selected parent, current semantics/foundation, prepared bindings and expected output names. It then runs current preflight and admission; new contribution success requires a fresh `CHECKED` result. The report cannot assert away these steps. |
| Authoring frontier | `contribute_source` obtains both roots from the same locked catalog. `_require_frontier_prefix` compares semantic/foundation/implementation/basis and the authenticated module prefix. A different branch cannot become an ancestor by being called one in a report. Current project and source approval remain separate. |
| Symbol-query preparation | Current `ordinary_advisory_query/query.py` resolves selected names against recorded actual context metadata under its existing advisory boundary. Snapshot integrity/readiness stays unasserted. Exact-type query uses its existing full context route. Allowing a parent identifier does not import a foreign query interpretation. |

`OrdinaryAdmission.admit` independently reconstructs its plan from raw units and
the actual context; it does not trust a caller-supplied READY status, reused-unit
list or report. Thus the proposed opt-in cannot turn an unaccepted target into a
warrant merely by copying its identity into `acquired-targets.json`.

## Producer and publication are separately traceable, but outside this cut

Producer reports contain inert manifest/target metadata. For intake, the helper's
producer-report use binds the selected actual manifest's semantic ID, length and
hash; the current intake still checks and admits the actual units. In principle
an old producer report could be treated as such inert metadata, provided those
bindings, original pins and current semantics remain checked and no old project
approval/path is inherited. It would still certify no theorem by itself.

Likewise `peer_api.publish` obtains the actual selected catalog context, requires
each target name/export ID to match that context, recomputes its export identity,
reads exact custody evidence, generates/resolves its preview and only then admits
the index record. An older report supplying root/target fields cannot by itself
make an unaccepted declaration eligible for this current publication path.

These observations establish the boundary in principle, not permission to widen
this change. Root selected only **parent, acquired-target and authoring-frontier
roles**. Producer reports, publish's accepted-report shortcut, and its combined
producer/intake shortcut stay strict in this version. They have extra selection
and workflow claims, and the present continuation fix does not need to change them.

## Exact scope and required implementation conditions

1. Keep exact-PROFILE behavior by default. Require an explicit opt-in selecting
   report fields as data. Validate the original reported PROFILE as an identifier;
   record it separately from the current selected PROFILE. Never rewrite either
   report or claim that the profiles are equivalent.
2. Read bounded original bytes through the existing explicit path/hash reference.
   Preserve duplicate-key, nesting, input-total and report shape/operation limits.
   Keep the original bytes/hash and request policy in the receipt's input trace.
3. Keep all successful-status, closure and internal-consistency checks, including
   contribution admission/root agreement, complete-intake shape and target identity
   formulas. This is not a failed-operation salvage or recovery mechanism.
4. Keep exact equality to the request's selected state fields. A report from a
   different catalog/custody/store is not a same-state continuation merely because
   it names a valid-looking root. Do not follow paths found in the report.
5. Relax only the PROFILE comparison at explicitly allowed extraction call sites:
   ordinary parent selection, acquired targets and optional authoring frontier.
   A receive/contribute report may be used in those roles. That does not relax a
   find report consumed by receive, a preview report consumed by inspect, or a
   publication shortcut consuming the very same report schema.
6. **Do not make `accepted_report` globally permissive.** It is also called by
   `publish`. Pass an explicit role/permission from the allowed call sites, with
   strict default behavior for every other caller. `Inputs.report` and
   `query_specs` must not inherit a blanket bypass accidentally.
7. Continue using the current package's ordinary CLI/config inputs and all current
   validation. Source/project approvals, source bytes, local paths, outputs,
   contacts, bounds and execution choice stay in the new explicit request. The
   opt-in must not select an older executable, modify native profile pins or
   migrate ADOPTION/custody state.

A request-level policy is acceptable if its meaning is explicitly restricted to
the three roles and each source report is disclosed. A per-reference
`allow_foreign_profile:true` is more precise for mixed references, but requires
new reference grammar at more call sites. Neither is safer by itself: the decisive
property is that no other report role or current product validator changes.
Root's selected scoped request policy avoids unnecessary per-action proliferation.

## Direct root selection versus report-field selection

Direct `context_root` already exists for symbol-query preparation. Extending that
pattern to parents and explicit acquired target rows would be mathematically sound
under the same product checks. It also avoids needing an old report at all. It
does not solve the practical work of recovering several exact declaration triples
without manual copying, and extending every request schema would add more surface
than a carefully scoped report projection.

The practical recommendation is therefore to retain explicit root selection where
it already exists and add the selected scoped report-field opt-in for continuation.
The old pinned report is useful traceable input; requiring an old package to remain
active solely to read its identifiers offers no additional mathematical guarantee.
Do not infer from this recommendation that reports are universally interchangeable.

## Concrete counterexamples and expected outcomes

| Attempt | Why a broad shortcut would be wrong; current required behavior |
|---|---|
| Fabricate an old successful report with a nonexistent root | Offline preparation may emit a syntactically valid selector. The actual catalog must refuse the absent root; no report bytes may materialize a record or snapshot. |
| Supply a well-formed export/unit/name triple absent from the selected parent | The current identity formula alone is insufficient. `request_targets` must refuse `CONTRIBUTION_TARGET_NOT_WARRANTED`; available bytes in custody do not grant acceptance. |
| Reuse the same directory after a native implementation change or under another store ID | The exact ADOPTION check must still refuse. Same path, same Lean version string or a field-only opt-in is not a migration, native compatibility result or approval of old checker defects. |
| Select a valid root from a sibling branch as authoring frontier | Both roots can be valid but the module-prefix condition fails. The report cannot bypass the ancestor check or select a source environment unrelated to the current parent. |
| Reuse an old declared-type query key after key normalization changes | The adapter namespace commits to the feature revision and type-key profile, but current `find` recompiles supplied specs in its current namespace. A syntactically valid old key can therefore silently select the wrong feature meaning. Keep old query-result interpretation strict; regenerate query specs from explicit current context/type inputs instead. |
| Treat a successful old preview or index match as a checked theorem | Even today's preview/find outputs do not establish acceptance or complete search. Those report-role shortcuts remain strict, and acquisition/admission must still validate actual candidates. |
| Inherit `approve_local_project` or source paths from a report | A report is untrusted data and can name executable code. Keep explicit fresh approval and pinned source/project inputs in the request; never copy approval authority from a report. |
| Replace a failed report by its inner accepted-root fragment | This opt-in preserves complete successful wrapper/closure requirements. Manual explicit root selection may have a separate valid recovery use, but no automatic report repair or failed-run relabeling is introduced here. |

Same-state report equality is intentionally conservative: moving an intact catalog
to a new path can make the report fail this check even when current direct root
selection might be valid. That is a separate relocation workflow, not a reason to
infer equivalence or weaken this bounded continuation change.

The next useful evidence is a focused inert preparer check: strict refusal versus
explicitly opted-in selection produces unchanged identifiers and current-profile
arguments, wrong-state/failed/malformed reports still refuse, unrelated report
roles stay strict, and input bytes remain unchanged. One retained-report preparation
is sufficient for this seam; no theorem, grounding or network replay is needed.
