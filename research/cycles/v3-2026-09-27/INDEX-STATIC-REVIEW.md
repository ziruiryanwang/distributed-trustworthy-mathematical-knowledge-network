# Source14 index: independent static review checkpoint

2026-09-27. Reviewer: `v3_efficiency`. Read-only inspection, no product import
or test execution. Scope is the held index implementation; tests are being
authored separately and final launch review remains pending.

## Current disposition

No correctness defect found in the held three-function delta, SHA-256
`be0a480a41f0a70ba6a2cbb5f4cf15ae0b95f7cf020c8c1425223931bb62cacc`.
This is not a test result or permission to call source14 qualified.

Compared frozen source13's complete `symbol_index.py` with held source14,
read `source_codec.transform_dag` and the relevant source/planner reference
grammar, and checked the existing [contract](../../../experiments/complete-type-index-01/CONTRACT.md).

- `_type_ref` first uses the unchanged exact external-reference grammar and
  then restricts projections to seed or exact group-type selector kind0.
  This matches existing canonical/source planner restrictions; membership and
  actual typing remain later checker obligations.
- Old tags0-5 use the same validation callback result, symbol condition and
  traversal branches. Removing the postvalidation unsupported-tag rejection
  has no effect when every tag is already in that old domain.
- Let's LIFO push order produces type, value, body traversal. Natural/string
  literals are leaves. Projection emits its structure key before pushing the
  target. Sharing is still expanded as occurrences under unchanged ceilings.
- Whole-DAG structural validation precedes collection. Failure returns trace
  plus failure fields, not partial keys or symbols. Malformed literals and
  projections remain refused by existing validation plus the new restriction.
- Group-root closure retains exact ordinary local-type closing, explicitly
  refuses local projections, and permits valid external projections. Its
  derived type identity remains a metadata value, not a new package dependency.
- No normalization, index schema, native/source rules, root identity, proof
  policy, peer wire, storage or resource limit changes were observed.

The native frontend's separate new-external-string restriction remains in
force. Index-only tag9 coverage must not be presented as shipped native string
support. Final review must inspect actual test files and their precise retained
Count fixture before root executes a fresh finite allocation.

## Final test/runner review, before first execution

Read all of `test_contracts.py` and `TESTS.md`, the source14 runner adapter,
its entire frozen inherited `nested-groups-01/run_contracts.py`, the two changed
public documentation sections, and the actual original Count public reply.

Held suite: 21,183 bytes, SHA-256
`90f050ca44277408a34a895b785db7cacd8378baaab52e5d536a26cb7a9ad783`.
Fourteen test methods. TESTS.md SHA-256
`4f45e8e3f77392e694a25c185a4f26aa90d1a0a484fdd226285c00c472818469`.
Source map SHA-256
`6378a2ebb4531b97243fb7f25d8be4276ae8acbdb718fedf9f62056f6fce19a1`.

The suite uses real pinned canonical validation and actual old/new metadata
methods. Its synthetic group fixtures explicitly do not claim native validity.
It compares complete old-domain results/formal bytes, traverses every new child
kind/order, exercises exact selectors and invalid projection references, and
tests inclusive/exceeding depth64, occurrences4096, symbols32 and literal1MiB.
The Count fixture is the original stage-0002 numeral-bearing package with the
actual accepted public root/type and original refusal reason; no constructor-
spelled continuation substitutes for the bug. Store mutation/proof-body reads
are separately disallowed during the selected metadata call. No unsafe native,
SQL, socket or subprocess execution is part of the test body.

No test correctness blocker found. The runner preserves fresh-directory
allocation, full source/baseline/explained-delta pins, fixed runtime/supervisor,
real Count tree pins, before/after input equality, exact14/all-zero-failures gate
and clean Job closure. The requested finite envelope is180 wall seconds,
150 Job CPU seconds,768 MiB, with unchanged8-process/output bounds.

One small launch correction was requested: add the separately read Count public
reply to runner FIXED, not only the suite's entry pin. This makes its bytes part
of the retained before/after input manifest like the rest of the evidence.
Root's preliminary bound runner hash was
`cf6587773022513690a201c8734ee39c51ce8acda465738f0960428229423316`;
the final corrected runner hash must be recorded before launch.

Disposition: **STATIC_REVIEW_PASS_CONDITIONAL_ON_REPLY_INPUT_BINDING**.
After that finite pin addition, root may launch the one reviewed allocation.
This is static clearance only; no source14 test or mathematical success is
inferred. Independent actual-outcome review remains required.

### Final correction verified

Reread the corrected complete runner and independently hashed it. The only
postreview change adds the exact Count public reply and its expected hash to
`prior.FIXED`. Final runner SHA-256:
`beabe1aa130aa3d67eb141b421371f618d9b1b1d33246604e24657336a2ba766`.
The source/test/map pins and14-test finite envelope are unchanged.

Final disposition: **STATIC_REVIEW_PASS_FOR_ONE_SOURCE14_NATIVE_FREE_ALLOCATION**.
No remaining prelaunch finding in this reviewed scope. No execution occurred
in this review; outcome and installed acceptance remain separate gates.
