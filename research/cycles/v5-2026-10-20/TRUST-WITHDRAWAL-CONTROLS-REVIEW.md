# Independent withdrawal-controls source review

Source-only review by core_search. No import, test, native command or proof ran.
Reviewed `software/v5/trust_withdrawal/controls.py`, SHA-256
`748bd8bd6ddeed3680c74f67ef84f5e9fa62427af8f1943c6f2d8ccebec6dfef`,
against current trust/I/A successors and runtime `70c52b51`.

**PASS for the proposed 11 focused native-free controls.** This is not their
execution outcome or mathematical verification evidence.

- Real new inert adoption records exercise exact binding, ordinary reopen,
  mismatch/missing/partial state, create refusal, withdrawal persistence and
  sticky denial. A forged exact-class binding with a genuine domain but no
  registration also refuses. Test-only tampering stays in fresh fixtures.
- Failed marker creation is explicitly *not* counted as durable withdrawal;
  failed fsync leaves denial/partial-marker evidence and no success response.
- I/A shells use the real liveness methods, original helper/binding/domain and
  inert registry sentinels. Busy-safe revoke clears handles/member caches without
  calling public busy-forbidden close. No accepted mathematical fact is invented.
- Post-worker control uses an explicitly inert supervisor result only to reach
  the real post-worker gate. It requires refusal before binding or minting and
  checks the original reservation remains charged; native invocation is patched
  to fail. It is not real cryptographic or OS-supervisor evidence.
- Runtime shell tests use the real live guard/open-operation method: substituted
  binding refuses; preexisting withdrawal refuses before workspace access; fake
  I/A receive the same binding; fake delta applies withdrawal before the real
  final check; cleanup is delta/A/I, with no transfer or grant consumption.
- Mandatory constructor signatures have no default. Fresh helper overlays load
  before dependent source; interface projection precedes authoring's import.

These focused controls do not qualify full support derivation, installed startup,
hostile-code isolation, process-restart behavior or large-network trust updates.
One separately selected actual receipt/RuntimeProfile integration addresses the
real-source/owner seam. Root owns execution and actual outcome adoption.
