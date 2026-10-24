# Mixed ordinary modules: selected installed-theorem reuse

2026-10-23, root. Source implementation only; no runtime is selected here.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.

## User workflow and decision

A user wants to export a checked new commons theorem into a normal Lean project.
Its proof uses an already installed theorem such as `Nat.add_zero`. The present
module bridge refuses that collision even though the exact full proof is already
locally warranted. Renaming standard-library declarations is not an acceptable
ordinary workflow. The saved mixed collision already establishes this obstacle;
do not reproduce the old failure or invent another theorem workload.

Root read the full existing-declarations analysis and independent
[theorem-interface review](ORDINARY-THEOREM-INTERFACE-REVIEW.md). Adopt its
conditional interpretation argument, including its non-converse: public use of a
proved theorem interface is sound under the stated dependency interpretation;
private success does **not** guarantee public conversion after proof erasure.
The actual public compatibility check therefore remains mandatory.

Select a fresh successor under `software/v5/ordinary_module_matching/`, starting
from the frozen module03 bridge/controller/worker. The highest-payoff first scope
is **singleton theorem collisions only**. Existing computational-declaration and
group collisions continue to refuse. This avoids implementing a larger matching
mechanism than the observed workflow needs. Completely absent declarations and
groups retain their existing checked-insertion behavior.

## Unchanged authority and exact new rule

- Keep the collector, complete selected evidence, exact UnitID/ExportID/import
  bindings, original codecs, fixed foundation, core checker and runtime policy
  unchanged. A match never terminates closure collection or substitutes a peer
  assertion for a locally established warrant.
- Decode with only the exact basis and preceding selected outputs available.
  A reusable unit must be a theorem, have exactly one inventory output, and have
  descriptor metadata `all = [name]`; run existing name/safety screening.
- Require the final actual private installed theorem record to equal the full
  selected inventory, including its proof and ordered universes. Check actual
  key/name agreement. A same statement with a different proof is refused by this
  deliberately exact identity route, not declared mathematically false.
- The final public record must be the exact theorem or a safe axiom-shaped handle
  with the same name, ordered universes and encoded type. That handle is interpreted
  by the already warranted full theorem. It is never new foundation/axiom evidence.
- Check all actual additions with the unchanged kernel checker in both relevant
  environments. Refuse missing public computation or failed conversion. Proof
  irrelevance must not be used to waive the `Acc.rec`/erasure compatibility issue.
- Keep explicit matched and added sets, with counts and inventories in reports.
  Write only additions. Both fresh-process rereads must check the actual matched
  relation, additions and module-own census. Preserve artifact binding, one original
  allowance, clean closure and final-report-last adoption.

No theorem-origin service, arbitrary native-module import, general proof
equivalence or definition-erasure rule is selected. When every selected unit is
already installed, return an explicit unsupported/no-new-module outcome before
artifact writing; do not manufacture an empty module or claim a new contribution.
A later useful all-installed resolution API is separate from this mixed-module fix.

## Implementation boundaries and evidence

Use fresh `OrdinaryModule.lean`, `module_worker.py` and `module_export.py` in the
new directory, with an explicit new policy/report schema binding the matched/added
meaning. Keep the public command's calling convention where possible. The current
distribution source map remains on its reviewed module03 sources until this
successor has its own review and selected changed-boundary validation.

Author saves a compact implementation note in this directory's README. Root owns
integration, exact selectors and Git. Independent source review must precede any
execution. The next finite discriminator should reuse the saved mixed closure,
require ordinary consumer use, and challenge exact-proof/signature/group mismatch
and absence of premature success. Pure controls and one actual native boundary
are distinct; do not rerun earlier package/network/certificate campaigns.

Expected payoff is removal of a concrete normal-project blocker without weaker
mathematical acceptance. This is not a performance, mathematical novelty, full
library compatibility or useful-growth claim. Full deployable v5 remains open.
