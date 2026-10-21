# Restricted guest03: independent changed-boundary review

Disposition: **PASS for the selected four-crate source/build-preparation
boundary**, not for compilation, guest execution, proof, image or release.
No product/helper module was imported or executed by this review. No compiler,
host, guest, proof or network operation was launched. Root owns runtime
selection and eventual adoption.

## Why this successor is justified

The two preflight failures remain preserved in
`RESTRICTED-GUEST-PREFLIGHT-OUTCOME.md`, SHA-256
`037ff59bf1a718ee65a4dce80c1340ede3c1a02de3ca20c0b7bb6620bd72e0fd`.
Guest02's refusal exposed an old aggregate-build finalization override. A later
successful validator established source/ELF lineage, not adoption of every
intermediate library. In particular, historical compiler logs name the old
module outputs but do not establish their contemporaneous SHA-256 values.
Treating those intermediate files as historically hash-bound would add an
unsupported inference.

Root selected the simpler alternative: compile the small original module
fresh, then the restricted core, aggregate and guest; retain only the separately
adopted original Nanoda pair and filtered dependencies. This adds one project
compile without a checker/SDK rebuild or a new artifact-trust exception. The
old failed operation remains explicitly failed. This review agrees with that
decision and the author's checkpoint
`RESTRICTED-GUEST-RETAINED-ARTIFACT-DECISION.md`, SHA-256
`9bdb44465b5e832ce9cac69906a2b40b911a1857395f652b674bb79d4da810da`.

## Exact source pins reviewed

| Source | SHA-256 |
|---|---|
| `software/v5/restricted_guest/build03.py` | `847589a36df894a022fe3dc8bf8251d32d49cfc605c2357a3311dd30ac1e8fbb` |
| `software/v5/restricted_guest/recipes03.py` | `e51b7b02d24c430599a021acaf92262fd7c49f6a3ebc2aa34287d6d5e29ccdef` |
| This cycle's `Select-RestrictedGuestBuild03.ps1` | `e4f17794310792989df3f73706f78c67abec3c3ea1f83192161e65b1db958e8c` |
| `software/v5/restricted_guest/assemble.py` | `0ebc655842b1092f4314e27fa4f6e57e452303eae06b2e60b1b5a19bac46a957` |

Read full build03/recipes03 and actual02-to03 diffs, the full fresh selector,
and changed assembler consumer fields. Original used01/02 bytes are untouched.
The assembler inspection is an interface-coherence check, not a repeated full
assembly review or authority to execute it.

## Evidence-binding and source checks

Independently checked the seven newly added direct-build/validation record
digests. The direct result binds its actual selected bytes and successful
terminal status; the later validator's source/ELF-only status is not promoted
to an intermediate-library or mathematical-admission claim.

For all nine original module files, compared original native map to original
guest project map, compared the validator's bound snapshot entry, and rehashed
both current canonical source and original validated snapshot. All agree.
The unchanged guest-entry snapshot also matches the validator binding. Source
inspection finds the seven `lib.rs` modules and `foundation_static.rs`'s
`foundation_data.rs` include: nine declared source files. This is a static
closure argument, not an observed compiler dep-info claim.

The21 selected production files are exactly the earlier12 restricted/aggregate/
entry files plus these nine original module files. No Lean/checker, mathematical
relation, native-control or guest-entry semantic source changes are introduced
by this build adapter successor. The existing corrected native original/saved
selection binding and40-control/26-refusal adoption checks remain intact.

The two retained Nanoda outputs are separately bound by
`bounded-parse-direct-build-01` selection and copied-input map and are copied
from that successful operation, not the failed aggregate directory. Their
current retained bytes were independently rehashed:

- rlib6,360,054 bytes:
  `8ec342c7f606b9ccf34cdd5fbf4bf86cd75f6239fd2cd025c7d837d442cf5fde`.
- rmeta2,446,327 bytes:
  `d5266e9ea875433bff5b2c4f084ee48f64be6d5bb6104316a44096a85cc7d62e`.

The236-entry typed dependency map contains no module, aggregate or Nanoda
project outputs. Thus the original module cannot be silently selected from that
retained view. New build source requires exact maps and rebinds all selected
inputs before/after use. This review did not redundantly rehash the unchanged
compiler/dependency tree.

The original `FINALIZATION-FAILED.json` is pinned, parsed to its exact known
failure and required to remain present. Only separately successful predecessors
must lack failure overrides. The fresh report records the old effective failure
and distinct Nanoda adoption. Removing the original directory from the generic
absence loop is therefore **not** ignoring its marker: the new route checks it
positively and never consumes its unadopted module binaries.

## Recipes and consumer consistency

The retained recipe data supports every replacement and profile check. The
four new commands are topologically ordered:

1. Original module from its fresh nine-file source snapshot, using adopted
   original Nanoda.
2. Restricted core using that new module.
3. Restricted aggregate using that new module and restricted core.
4. Unchanged guest entry using the new module and aggregate.

Their direct extern counts are11/10/11/11. Output, source, dep-info, metadata,
map and project lookup paths change to the fresh run; no old typed project or
output argument remains. The retained libraries/macros remain allowed. Fresh
metadata uses `dmkn_v5_rc_guest03_`. The selected target, opt-level3, overflow
checks and abort profile remain unchanged. The recipe basis is explicitly
reconstructed equivalent profile, not captured historical Cargo argv.

Builder, selector and changed assembler fields agree on run03; two adapters;
21 source files; four commands; seven outputs (three rlib/rmeta pairs and guest
ELF); two copied Nanoda artifacts; and the new four-crate schemas. The assembler
requires exact four-command order/argv, seven output identities, successful
termination and one actual module compiler launch. The builder computes launch
counts from recorded PIDs and does not predeclare success.

All limits, helper chain and output-finalization rules remain unchanged,
including the frozen `common_build02.py` helper rather than a nonexistent03
helper. No Cargo/dependency/checker compile or proof execution is selected.

## Gate and remaining distinction

No changed-boundary blocker was found in these exact bytes. They are suitable
for root's finite fresh compile selection. A source-gate PASS still cannot
promise that a compiler accepts, that an output meets its performance envelope,
or that an eventual zkVM execution is economical. Those outcomes must be read
from the single selected operation, preserving any failure and measuring only
newly necessary boundaries. No full historical campaign should be repeated.
