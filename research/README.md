# Research workspace

This directory organizes the investigation needed to make the decentralized mathematical commons operable. It is **project research infrastructure**, not a task registry, shared research agenda or human-intention interface inside the eventual mathematics network.

The goal is unchanged: trustworthy contributions and efficient reciprocal mathematical reuse by independent local agents, initially Lean 4, without a mandatory central server. Formal arguments, source analysis, engineering judgment and useful heuristics all have roles. No implementation or executable qualification has been authorized.

## Start here

- [Current research desk](NOW.md): compact live question, owners and next handoffs; its cycle brief preserves the commissioning and decision trail.
- [Current selected design](../CURRENT-DESIGN.md): authoritative integration and frozen checkpoint.
- [Research modules](../RESEARCH-MODULES.md): decomposition, assumptions and exit criteria.
- [Work and agent ledger](registry/WORK.md): current assignments, ownership, review and next decisions.
- [Decisive bottleneck map](registry/BOTTLENECKS.md): the few unresolved questions that change operability, their next evidence and misleading substitutes.
- [Consequential comparison ledger](registry/COMPARISONS.md): competing designs, equal-service criteria, decision thresholds and reasons to stop refining an option.
- [Claim ledger](registry/CLAIMS.md): precisely what is asserted and at what evidence grade.
- [Assumption ledger](registry/ASSUMPTIONS.md): what each guarantee needs, who can enforce it, and what fails if it is absent.
- [Scenario and supply ledger](registry/SCENARIOS.md): finite operating cases, added premises, resource owners and limits on extrapolation.
- [Issue ledger](registry/ISSUES.md): contradictions, counterexamples and unresolved obligations.
- [Decision log](registry/DECISIONS.md): selected choices, alternatives and reopening triggers.
- [Interface ledger](registry/INTERFACES.md): producer/consumer obligations and targeted change-impact reviews.
- [Artifact registry](registry/ARTIFACTS.md): where specifications, notes and audits live.
- [Evidence registry](registry/EVIDENCE.md): sources and what they do—and do not—establish.

## Directory roles

| Path | Role and editing rule |
|---|---|
| `spec/` at project root | Integrated system specifications; frozen versions are immutable |
| `notes/checkpoints/` | Existing checkpoint narratives/manifests; never silently update a frozen row or file |
| `notes/analyses/`, `notes/audits/` | Existing detailed analyses/reviews, including frozen CP-001I sources; retain their paths and manifest-bound bytes |
| `research/registry/` | Mutable concise research control records; they point to evidence instead of duplicating it |
| `research/NOW.md` | Compact rotating front door to the current investigation; no copied source arguments |
| `research/cycles/` | Bounded commissioning/decision records connecting exact inputs, disjoint owners, review gates and outcomes |
| `research/modules/<module>/README.md` | Module contract, owner, dependencies, claims, countercases and current next action |
| `research/modules/<module>/audits/` | New independently authored module/interface audits |
| `research/templates/` | Lightweight optional templates for new modules and reviews |

Existing files are not moved merely to make the tree look tidy. I/J/K/L/M/N/O/P/Q and earlier checkpoints stay exactly where their manifests bind them. Module cards provide the navigable structure without relocating evidence. New independent module work should use its module directory. Avoid copied “latest” versions whose authority becomes ambiguous.

## Module cards

- [Direct-contact broker protocol](modules/direct-broker/README.md).
- [Local retry and failure handling](modules/broker-retry/README.md).
- [Broker economics and availability](modules/broker-economics/README.md).
- [Foundation/bootstrap qualification boundary](modules/foundation-bootstrap/README.md).
- [Whole reciprocal-path operability](modules/reciprocal-operability/README.md): conditional reciprocal trace, critical-path triage, selected N routing recovery, O normalization and P joint finite growth epoch; separate source reviews and fresh integration audits retain their exact scopes.
- [Unfamiliar-interface query-view expansion](modules/query-view-expansion/README.md): selected alternative J and L schedules; neither has established recall dominance.
- [Operational evidence and qualification readiness](modules/qualification-readiness/README.md): reviewed documentary handoff; all runtime gates NOT RUN.
- [Bounded cross-judgment cache selection](modules/cache-selection/README.md): selected optional CACHESEL1/K after two source reviews and integration review; usefulness remains unmeasured and durable custody separate.
- [Producer egress selection](modules/egress-selection/README.md): selected optional EGRESS1/M after two source reviews and a fresh integration review; bounded known-contact exposure, not a global discovery or measured-growth result. Existing postselection publication remains unchanged.
- [Stable placement versus logical index runs](modules/placement-separation/STATUS.md): current profile/audit/comparison status, separate from the preserved architectural card; unselected candidate for avoiding unnecessary remote ownership changes during exact local compaction.

## Coordination protocol

The root owns integration, claim/issue/decision/work ledgers and selection decisions. Each assignment names one bounded question, owned output paths, exact inputs, prohibited scope expansion, a reviewer and exit criteria. Authors do not independently mark their own substantive module audited. Reviewers own their audit records and send concrete counterexamples early.

Use the available concurrent slots for genuinely independent work. Reuse a collaborator when its context is helpful; use a fresh reviewer for a new independent perspective where capacity permits. A completed audit is a handoff, not permission to rewrite unrelated modules. If an assigned path is being edited by another owner, coordinate first.

At each meaningful handoff, record the reviewed revision, findings and exact affected claims. A hash identifies the reviewed bytes, not the truth of their claims. When an author repairs a finding, the reviewer inspects that repair and records closure or remaining scope. Reopen reverse-dependent claims only when the changed assumption actually affects them.

When collaborators cannot address one another through the available task tools, route the held source hash and concrete findings through the root. Do not assume that a sibling received a message merely because its name appeared in another agent's context. The root coordinates one repair cut for overlapping reviews and relays it to every affected reviewer.

For active multi-review work, follow the [review handoff checklist](templates/review-handoff.md). Preflight findings may be shared immediately, but final reviews must identify the same complete held source cut. Root resolves overlapping findings into one repair request, while retaining independent credit and judgments. After source closure, use a fresh reviewer for consequential integration choices where capacity permits. Avoid parallel rewrites or a proliferation of audits of unchanged claims.

Selection requires a successful paper path, explicit failure outcomes, honest costs, no unresolved blocking interface contradiction and independent review at the stated evidence grade. Actual native replay, broad-library interoperability and measured useful throughput remain separately unperformed until authorized. No document status may fabricate those results.

## Research efficiency

The [central-priority checkpoint](cycles/2026-09-20-central-priorities.md) and [research-admission gate](registry/BOTTLENECKS.md#roots-research-admission-gate) govern new commissions. Trustworthy actual mathematical reuse, supported interoperability and a usable growing corpus take priority over refinements to optional mechanisms. Existing ledgers suffice; add a registry only to solve a demonstrated research-navigation problem.

Prefer a small decisive counterexample to another general essay. Reuse frozen contracts by reference. Before adding a mechanism, state which open issue it closes and its additional obligations. A mechanism can be rejected, narrowed or left optional; not every investigated idea belongs in the product.

Administrative records should stay smaller than the underlying work. Update them when a decision, finding, assignment or evidence grade changes, not for every tool call. The work ledger plans this project's investigation; it never assigns mathematical goals to the future network's agents.
