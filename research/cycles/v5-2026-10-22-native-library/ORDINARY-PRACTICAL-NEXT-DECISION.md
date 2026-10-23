# Practical next decision after the public reciprocal workflow

2026-10-23. Source/theory-only review by `practical_path_audit`.
No code, test, build, network operation, owner mutation or Git operation.
This is a prioritization decision, not a repeat of the exporter/error audits.

## Largest barrier and selected direction

**The largest adoption barrier is existing-Lean-library interoperability.**
The new project adapter permits owner-approved tactics and imports during
authoring, but imported mathematics absent from the receiver still refuses.
Ordinary projects use imported mathematics routinely. Requiring a user to
manually translate that dependency closure into commons objects makes the
working reciprocal CLI insufficient as a normal Lean-library workflow.

The highest-payoff immediate slice is therefore **explicit bounded ingestion
of selected existing-library declarations**, through the existing inert
export/bind/admit/retain path. Reuse the exporter/closure mechanisms identified
by `ORDINARY-LIBRARY-INGEST-DECISION.md`; its author owns the exact source seam.
Do not weaken the current-module rule for ordinary contribution or accept
producer success, a name match, or downloaded `.olean` files as proof authority.

This does not yet solve the reverse integration direction: a scratch module
containing assumed acquired handles is not an ordinary proof-complete Lean
library. A real project's independently checked use must either supply its
required proof evidence or explicitly remain inside the commons acceptance
boundary. Document this before calling ingestion full project interoperability.

## Relative payoff of the three candidate tasks

| Candidate | Immediate value | Sequencing judgment |
|---|---|---|
| Selected library ingestion | Removes a structural refusal affecting otherwise ordinary project proofs; admits an existing useful corpus without reauthoring it | First substantive implementation, with finite closure and explicit owner selection |
| Continue after one failed discovery provider | Keeps a replaceable provider from becoming an availability single point of failure | Small parallel change if its error boundary is clear; no new routing/ranking subsystem |
| New corpus/search usability features | May improve relevance and turn a local Lean goal into usable queries | Do not add another index profile until a selected real-library result can enter the public flow |

Provider continuation is valuable independently of ingestion, but cannot repair
the mathematical-import refusal. Better search cannot help if the result found
cannot be incorporated. Conversely ingestion alone does not establish relevance:
after it works, the next question is whether an unfamiliar useful result can be
found from a naturally available formal query, without a hidden result ID.
Existing structural and definition-body profiles already supply starting points;
the body-search result also showed increased bytes despite fewer postings.

## One falsifiable user workflow, without another synthetic theorem campaign

1. Select an already built owner-approved Lean module and one existing useful
   theorem, with a compatible toolchain, an exact receiver parent and a finite
   operation allowance. A real user project is preferable when supplied.
2. Export that theorem and only its genuinely missing supported mathematical
   closure, stopping at the exact locally warranted frontier. No whole-library
   enumeration, automatic Lake build/download, or fixture-state copying.
3. Bind and independently admit the resulting inert evidence using the unchanged
   ordinary receiver; retain exact IDs and complete refusals/costs.
4. Make the selected theorem discoverable using existing publication/search,
   and use it in a caller-chosen new contribution through the normal authoring
   adapter. The acquired result must actually occur in the checked proof.
5. Reopen and reuse the accepted local result without replaying its old proof.
   Existing successful persistence/peer evidence need not be rerun where unchanged.

The preexisting installed-Std examples are appropriate compatibility inputs to
a new public seam, not evidence of new mathematics or an advantage over Std
already installed in the comparator. Reuse saved evidence for unchanged exporter
and admission boundaries. Do not execute this whole workflow merely because
the list exists; root should select only the newly uncertain boundary.

## Stop rule and architecture rejection

Let `D(X,A)` be the missing supported closure for selected targets `X` against
the owner's warranted frontier `A`. Ingestion must have explicit byte, node,
time and memory bounds. Neither small `X` nor a familiar theorem name implies
small `D`. If closure is unavailable, policy-incompatible or exceeds the
allowance, stop with a reason and preserve the partial work; do not silently
assume the missing mathematics or launch unlimited dependency acquisition.

Reject the architecture **as a replacement Lean development environment**.
Prefer ordinary pinned package imports when users trust the package code and
need most of its library. The commons' prospective advantage is a selective,
independently checked data layer with replaceable discovery and custody, not
forcing normal Lean work through custom scratch modules or new package tooling.
If existing package sharing reaches the same assurance endpoint more cheaply,
integrate with that route instead of investing to defend this mechanism.

For each route compare the same initial mathematics, warm caches, useful index,
and checking endpoint. Added ingestion, search failures, custody and translation
must be outweighed by actual avoided integration/checking/discovery costs.
No positive margin has been established by this note. The existing full-cost
growth condition in `ORDINARY-NEXT-VALUE-DECISION.md` remains sufficient; a new
economic ledger, benchmark suite or certificate campaign is unnecessary here.

## Evidence consulted

Prior `ORDINARY-NEXT-VALUE-DECISION.md`, `ORDINARY-PRACTICAL-COST.md`,
`ORDINARY-EXISTING-PROJECT-DECISION.md`, `ORDINARY-APPLICABILITY-DESIGN.md`,
and the current ordinary-peer/project package READMEs. This decision advances
their sequencing after the now-completed public CLI and optional adapter;
it does not replace the separate source audits or claim real-project support.
