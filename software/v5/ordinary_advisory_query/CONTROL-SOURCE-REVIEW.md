# Advisory controls: focused source review

2026-10-28. **PASS_IN_PRINCIPLE_FOR_ONE_SELECTED_INERT_CONTROL_RUN.**
No likely fixture or expected-refusal error found. No execution or new test scope.

Reviewed `control_tests.py` SHA-256
`cf08f64048759ba3ee0ac12cc41fe53b7aac3c2066a89fce7a5a9d55e26c726f`
against helper `58e20183a71a58877a34e8c8ebd9fb384afe188bfced43d4e1b9c9eb1b66a47c`,
the unchanged portable/local catalog validators and caller projection checks.
This is fixture review, separate from the implementation review and actual outcome.

- Native extension fields, input batch/root formula and inert COMMITTED operation
  tuple satisfy the original record validator. The absent generated snapshot
  succeeds through the scoped wrapper without entering `_verified_artifacts`.
  Calling the original record validator directly on the same reader, after scope
  reset, correctly delegates artifact verification and refuses missing bytes.
- Altered operation, request hash, duplicate binding and generated path reach the
  stated refusal predicates. Scope-reset expectations match the helper's finally.
- The legacy profile has the exact V1 field/policy constants. Support lists are
  sorted and retained support is the required union. Source/local root formulas,
  original record digest, origin fields, imported row digest, generated snapshot
  and source-name correspondence satisfy the isolated import/record validators.
- Tiny audit/correspondence/source files exercise actual bounded reads. Changing
  the audit's expected hash changes its verification-cache key, so the audit
  refusal cannot be masked by the previously verified correct tuple. Replacing
  source-record bytes produces the expected digest refusal before snapshot bypass.
- The ordinal-zero imported extension intentionally does not represent an accepted
  full lineage: the harness calls isolated validators and replaces context/open,
  SQL and activation with explicitly labeled inert doubles. It makes no actual
  migration, lock, eager-open, ancestry or native-acceptance claim.
- Successful/partial-missing projections, close failure and strict caller field,
  boundary, missing-set and extra-binding checks match the code's return/refusal
  ordering. The inherited close fails before a successful projection can escape.

Module loading order satisfies the helper's shared-module/type checks. Package
source pins are rechecked; native, network and real SQLite entrypoints are blocked.
The four groups are appropriately scoped. Proceed under the existing finite root
selection; an actual PASS still requires the run and independent outcome review.
