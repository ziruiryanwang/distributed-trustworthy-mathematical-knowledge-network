# Independent selector delta review: observed owner plus close drain

2026-10-21, core_release. **PASS for preparation only, conditional on screen's
separate service review and the already adopted owner review.** This does not
review or adopt this reviewer's service implementation. No selector was run.

Reviewed full revised
`research/cycles/v5-2026-10-20/Select-ManagedObservedDistribution01.ps1`,
SHA-256 `865d97c12383dbd415fbad7403739b8cb641e66c3a1a51e053326444640b7aa2`.
This supersedes the unused one-replacement preparation reviewed in
MANAGED-OBSERVED-DISTRIBUTION-REVIEW.md, SHA7800f2d7.

The only new map replacement is `v5/client/serve_placement.py`, from the
authenticated predecessor7e735337 to the explicitly supplied reviewed pin
at `software/v5/managed_close_drain/client/serve_placement.py`. The existing
owner replacement remains fixed to its assigned fresh path. The selector now
requires separate close source/review SHA arguments and verifies the exact
MANAGED-CLOSE-DRAIN-REVIEW.md bytes before preparation. It explicitly validates
both old logical rows and reports replaced=2, added=0.

Read-only basis inspection confirms127 SDK rows,106 preparation rows, old
owner75c0e8a9 and service7e735337. Iteration first copies every authenticated
basis row, rehashes and size-checks them, then the fixed two-key changes map
replaces only those two. Thus125 SDK rows remain unchanged, including the
credential helper7116e2d9. No non-SDK input field is modified.

Buildereb1348f6, runner44a7bf1b, exact contribution basis input33bd99d7 and build
selectionad982f4d remain unchanged. The29-row runtime map removes only the
exact contribution input key and adds only the new observed input pin; the
other28 rows, bootstrap Python, two-source snapshot map, build argv shape,
CPU120/wall600/128MiB/two-process limits are unchanged.

The four output targets from the earlier review were again absent. CreateNew
writes and the final new-parent creation remain preparation-only. There is no
builder invocation, credential read, service launch, old-state mutation, deletion,
or horizon renewal.

A selected invocation should supply owner
`1c022737e4d51a25d873e6fd255cd87ee8427f21d7455f78b29d4b2e4d133503`
and service
`c815331f035618b36f504d604a1fb75d8682439f0488453c72e9801a63d78bd8`,
plus the exact independent review pins after adoption. The selector only binds
review bytes; root must actually read/adopt their conclusions. A later source
change needs a new explicit pin and corresponding review. Combining the two
reviewed deltas avoids a diagnostic-only distribution build without broadening
this review into implementation or release acceptance.

