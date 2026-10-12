# Full architecture guide: authoring and full-cycle review

Reviewed `notes/V5-ARCHITECTURE-GUIDE.md` in full, without modifying it or
launching code. Reviewer: `v5_receipt_source_loop`. This is a documentation
review, not an implementation or cryptographic audit.

## Findings

The guide covers the whole candidate architecture rather than only verification:
foundation/policy, content identity, modular imports, custody, discovery, routing,
local-agent interfaces, growth/investment, resource limits, security, recovery
and release are connected to the discover/extend/return example in section11.
The initial flow and layer/role tables provide an understandable entry point.

The agent/system boundary in section7 matches the user's intent: API/skill-driven
local research decisions need no global agenda or human-intention field, while
live verifier identity, exact import binding, lifetime and budgets remain actual
software responsibilities. That is a substantive architectural distinction, not
an attempt to put the whole agent inside the protocol.

The authoring trust explanation is accurate within the inspected source scope:
`ReceiptVerifier.receive` mints an in-process handle; `ImportSession` binds exact
receipt bytes; `SourceOperation` exports an untrusted child; `OwnerPreparation`
executes source and creates a parent-aware capsule; later actual production and
admission are still required. Sections4,6,7 and16 consistently distinguish a
receipt, a handle, a frontend success report and an execution capsule.

The complete-cycle example does not falsely claim current end-to-end operation.
Section16 expressly leaves genuine current-profile source/import/child/return,
actual worker/native process envelope, useful retrieval, custody continuation
and public deployment open. The retained new unrun integration harness does not
close any of those entries and should not be promoted into implemented evidence.

The scale theory is unusually careful: it separates corpus, proof ancestry and
needed semantics; flags expression-tree blowup; distinguishes exact routing from
semantic search; and separates provider hints from independent custody. Those
limitations are central rather than peripheral qualifications.

The growth sections use a defensible bounded-capability model, compare equally
optimized local libraries and distinguish sharing from cryptography. Reuse of
`binary_congr` in the small pending source integration would only establish the
ordinary-source interface path, not the full fusion workload, new mathematical
discovery, or the network-benefit inequality. Keep that difference explicit in
any future progress update.

## Optional clarity improvements, not blockers

- In section11's example, readers may benefit from one explicit sentence that
  proof-source elaboration is not the child's acceptance event; the later receipt
  is what makes that child transferable on the currently implemented route.
  Sections6/7 already establish this, so no correctness repair is necessary.
- The guide intentionally anchors implementation status to Git `fdfcd80` and
  October8. If delivered again on October12, retain that clear baseline or add a
  separate dated evidence update. Do not silently refresh receipt success from
  a finished-background status file: actual result/admission audit is separate.
- The document is long but its opening route and source map are sufficient for
  a theoretical reference. A shorter first-read summary could be useful later;
  it is not a reason to omit the complete architecture requested here.

## Disposition

No material authoring/full-cycle clarity defect found. Existing implemented-vs-
proposed boundaries should remain. No guide edits, no runtime, no deployment,
no Git mutation. Feature work stopped per root instruction; draft disposition is
in `RECEIPT-SOURCE-LOOP.md`. Reviewer is quiescent.
