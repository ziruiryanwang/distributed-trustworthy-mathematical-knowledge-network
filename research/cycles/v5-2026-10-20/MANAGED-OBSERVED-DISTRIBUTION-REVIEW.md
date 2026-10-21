# Independent review: observed-owner distribution selector

2026-10-21, core_release. **PASS for preparation only, conditional on the
separate independent owner review.** This review does not review or adopt this
reviewer's owner implementation. No selector, builder or product was executed.

Reviewed new selector `Select-ManagedObservedDistribution01.ps1`,5838bytes,
SHA-256 `885bfee018ce7bb52f5a032b2b8a281377385cea3dc871642142b15a22d0f622`.
Compared full source with the adopted contribution selector `2e83c316...`.

## Exact change and mapping

- Basis is authenticated `distribution-managed-contribution-01-input.json`,
  SHA-256 `33bd99d7c3a1db865a6abcb92c96b5df2d0923a793535135e133aebc54aacc0c`.
  Read-only inspection confirms127 SDK rows and106 `v5/` preparation rows,
  old owner75c0e8a9 and credential helper7116e2d9.
- The successor copies those rows and assigns **only**
  `v5/client/managed_owner.py` to
  `software/v5/managed_observed/client/managed_owner.py` with the supplied
  reviewed owner pin. Root's selected invocation must supply
  `1c022737e4d51a25d873e6fd255cd87ee8427f21d7455f78b29d4b2e4d133503`.
  The other126 rows, including the credential helper, are not modified.
- The selector rehashes/size-checks each basis source, checks the replacement,
  and requires the same127/106 census. All non-SDK basis input fields persist.
- It requires the separately supplied pin of MANAGED-OBSERVED-OWNER-REVIEW.md.
  This selector pass does not substitute for that independent owner adoption.

## Builder and runtime identity

The exact build basis is
`distribution-managed-contribution-build-01-selection.json`, independently
hashed as `ad982f4d49107a6bc6ed4e6268adad9e9e88f963930106ba06eda57faedd5959`.
Its29 runtime rows contain exactly one key equal to the current basis input
path, with value33bd99d7. The selector removes **that exact key**, retains the
other28 unchanged, then adds the newly written observed input and its hash.
There is no stale managed-contribution input used as the build argv or runtime
pin. Earlier ancestral input pins remain intentional unchanged builder inputs.

The same pinned v4 bootstrap Python remains argv[0] and must still occur in
the runtime map. This is not an accidental reference to the new installation.
Runner44a7bf1b and body_location builder eb1348f6 remain the only two source
snapshots. Source key, builder path, fixed builder hash, build command and
CPU120/wall600/128MiB/two-process/log limits are unchanged.

## Freshness and effects

All four exact intended targets were absent during this review:

- `experiments/v5-local-checks/distribution-managed-observed-01-input.json`
- `experiments/v5-local-checks/distribution-managed-observed-build-01-selection.json`
- `experiments/v5-local-checks/distribution-managed-observed-build-01/`
- `product-local/v5-distribution-managed-observed-01/`

The selector rechecks absence, writes input/selection with bounded CreateNew
and flush, then creates only the fresh installation parent. Its generated build
argv names that new input/hash and the new `Mathematical Commons v5` target.
It does not launch the builder, change old installations, create credentials,
or reset public-test horizons. Actual build/adoption is a later root decision.

Recommendation: after the separate owner review passes, use exactly885bfee0
with owner1c022737 and that review's actual pin for one preparation. Inspect
the generated map/selection before any build. No large install sweep or repeated
old qualification is needed for this delta.
