# Renewal controls02: independent changed-boundary source review

2026-10-22, storage_outcome_audit. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

**PASS_CHANGED_BOUNDARY_SOURCE. No execution or runnable-import result yet.**
The actual controls01 failure remains FAILED_BEFORE_TEST_SUITE under independent
outcome b562efe2; its earlier source compatibility review missed this dependency.
This review neither repairs old evidence nor resets the failed run's costs.

## Exact correction reviewed

Read the complete diff from used controls01 to new controls02, complete two
added helper files, and author checkpoint TYPED-RENEWAL-CONTROLS02-SOURCE.md.
The selected existing source/helper/owner and current130 SDK map are unchanged.

| File | Bytes | SHA-256 |
|---|---:|---|
| typed_renewal/controls02.py | 25822 | `0b3a775d7e5ba6fe0b5232e83d88b0d5446fd4f9cffac80e92d2579fed6f017b` |
| aggregate_claims/prepare_mixed.py | 7502 | `2d03b635553eaffa406fba57011bf3bd346ec23fd59e0092b29d9442a95802ff` |
| aggregate_claims/input.py | 5679 | `d40b611e288fd73a060df021809e403f80b1e6c16ca8b81ff2fd528d1f2fe61f` |

The diff only changes SELF/additions from controls.py to controls02.py, adds
the two pure helpers as test-support logical files, changes snapshot census
135->137 and logical census134->136, and labels output harness_revision=2.
All six test bodies, doubles, forbidden-call hooks, claims and limits of
their assertions remain unchanged. No product API is modified or newly trusted.

## Dependency closure, not a new producer

prepare_mixed imports bindings, input.encode, delta.packet.require_closure,
delta_claims.claims.expected_journal, mixed_claims.packet and modules.codec,
plus Python standard-library dataclasses/hashlib. input imports bindings/codec;
its only function-local import is delta.packet. All nonadded module paths were
independently found in the exact current130 map. The aggregate_claims package
initializer remains the same existing file; neither helper replaces it.

Both helpers are pure structural preparation: no subprocess, file write,
receipt verifier, DB, native checker, funding or implicit proof dispatch is
introduced. prepare_mixed returns an explicitly untrusted PreparedSeal; synthetic
receipts remain inert. The test can call the real shape/encoding algorithms
without installing or invoking a producer owner. This is the smallest source
closure correction for the observed import failure.

The ordinary renewal owner does not import these two helpers. Its132-source
genuine consumer path is therefore unaffected, and still requires a real A
receipt plus its own boot/source/authority/cleanup validation. The136-file
test tree must not be relabeled a deployed client distribution.

## Required fresh selection and outcome

The fresh selector must select137 sources:130 current SDK + init/source/owner/
controls02 + prepare_mixed/input + the unchanged wrapper. Its logical test tree
then has136. Keep the same32 runtime pins, fixture, isolated Python argv and
finite30CPU/90wall/256MiB/one-process limits; use fresh controls02 output paths.
No old01 run or source is reused as a purported passed result.

No full selector, import probe, test, product operation or proof ran during this
review. Exact generated-map inspection and independently audited terminal output
are still required. An additional import/runtime failure would remain a failure;
source closure analysis is not permission to fabricate success or keep retrying.
No blocking source finding in this narrowly corrected boundary.
