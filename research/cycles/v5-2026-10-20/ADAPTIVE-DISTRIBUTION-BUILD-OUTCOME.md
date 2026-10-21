# Adaptive distribution build: independent saved-evidence audit

Disposition: **GO for exact built candidate identity; no installed-operation or mathematical acceptance claim.**

Reviewed by `core_release`, 2026-10-20. This audit reads saved artifacts and
hashes selected small payloads. It launches no product, test, proof or network
operation, changes no installation, and performs no Git operation.

## Exact boundary

The selected run is `experiments/v5-local-checks/distribution-adaptive-build-01`.
The new candidate is
`product-local/v5-distribution-adaptive-01/Mathematical Commons v5`.
The predecessor remains preserved at
`product-local/v5-distribution-discovery-01/Mathematical Commons v5`.

| Artifact | SHA-256 |
|---|---|
| Original and saved selection | `7ec39f9f533582768617e902ab8bcd0875ce734a3bd795f0fa54fd70abbfd4fb` |
| Adaptive build input | `a74eaf51a71b5e0ec49a762fd5c7e6cce4f8fc6b107e97ae6e71fd7ec0cf1e32` |
| New release manifest | `ad2e3ba04a2e12b6076fbf1d6be9fe068c35ae71970a5dee1eedb4188781e193` |
| Predecessor release manifest | `769506990ea10be5c6ce812e5cfd457922f4955ad4831bcdbc9d7a9ec9561108` |
| Saved RESULT.json | `08ac81c84acd1d35e037a4403fdd36d5e9be7490d1a3e36058f85ecef15217fb` |
| Saved command/command.json | `17bfa9201bd429544e3019db3b53803448d0587db4d5c84a220ece0d7f624b1d` |
| Saved command/stdout.txt | `7a28e4d8a3bbc0a37689240a8a03171b0389425feb11cea524d8c042e857e99a` |

Both original/snapshot source pairs match their selected hashes:
`tools/Run-V5-Check.py` is
`44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651`;
the unchanged `software/v5/distribution_coherent/distribution.py` is
`6d6f541112f5f25493a67da6a67065535d8a5e8347456004c89435cbfdc14ee6`.
The installed builder also matches that selected builder hash.

## Complete manifest delta and selected payloads

Independent comparison of all predecessor and successor file-map rows
(path, byte length and SHA-256) found exactly four replacements and one addition,
with no removals or other payload changes. The predecessor contains 9,855
payloads; the successor contains 9,856. All 111 selected installed SDK files were
independently checked for exact hash/length agreement with the input and release
manifest: zero mismatches. The five changed actual installed files were also
checked directly against the manifest:

| Installed path | Change | Bytes | SHA-256 |
|---|---|---:|---|
| `sdk/v5/client/direct_contacts.py` | Replace | 19214 | `e243a094b9fdce2adef221514923bf6753d04b8cc3ed8ae60e392c0ebd804545` |
| `sdk/v5/client/workspace_validated.py` | Replace | 5577 | `901ffd191131a8eb293c4f11ca8a890a5edd800d3d90156dc298ff13ac15a4be` |
| `sdk/v5/client/semantic_reader.py` | Replace | 30406 | `ec040740ad00b913c3061156d019f40887f926bf7be1ef144b116fa366c47c0b` |
| `sdk/v5/evidence_network/transport.py` | Replace | 6451 | `5808c0e253b203cdf38bd2069c593888ea4814d47f756871237c38eb3e0caab7` |
| `sdk/v5/client/located_queries.py` | Add | 23155 | `419df8428528203858eff69da43c7e3ed7e5634d06007dc5e30ca2f33df82c4e` |

The build input's assets and aggregate-image identity are unchanged from the
predecessor. The base role remains `mathematical-client-location-v1`.
No checker, image, foundation, policy or runtime payload changed. Large unchanged
runtime files were not redundantly rehashed by this audit: unchanged manifest
pins plus the selected builder's full exact-verification outcome are the
available evidence for those copied files, not a second independent full census.

## Terminal outcome and cost

Saved stdout reports `DIRECTORY_CREATED_AND_EXACTLY_VERIFIED`, 9,856 payloads,
842,336,174 payload bytes, the exact new manifest above, and
`mathematical_acceptance: false`. Stderr is empty. The supervisor reports child
exit zero, direct child reaped, Job closed, zero active processes, no cleanup
errors, no requested termination and no terminated processes.

Known CPU is 39.6875 Job CPU + 0.84375 outer-wrapper CPU = **40.53125 seconds**.
Outer wall time is **232.69924079999328 seconds**. Nested command wall time
232.63718979991972 seconds is not additive. Embedded supervision CPU 0.5625 is
already within outer-wrapper accounting and is not added again. Peak Job private
commit is 56,782,848 bytes. Selected limits were 120 CPU seconds, 300 wall
seconds, 128 MiB and two active processes. These are build-operation observations,
not ordinary client cost or a mathematical growth measurement.

## Consequence

The candidate exactly integrates the previously reviewed four direct-query
successors and one located-query helper using the unchanged distribution
machinery. Root may adopt this exact build identity for the separately reviewed
installed-boundary action. This audit does not establish that action's outcome,
provider discovery, reciprocal mathematical growth, broad deployment readiness,
or completion of v5. No rerun is needed to establish this saved build result.
