# Independent saved public-query outcome

2026-10-26. `practical_library_route`; **PASS_SELECTED_PUBLIC_PROFILE_LOAD**.
Saved-data audit only. No rerun, product import, Lean, state operation, network or
Git mutation. Root owns adoption. This is the query selected in QUERY-REVIEW.md.

## Exact evidence

Under `experiments/v5-local-checks/`:

| Artifact | SHA256 |
|---|---|
| binding-package-query01.command.json | `09fd84bca537d4ca2073666aec219f65065af66c036dac22b2ab97dae6c3a51f` |
| binding-package-query01-launch/LAUNCH.json | `5629369d5d648d0e2ab9c3c39db9f53b0ccb3dc892b7861ea1af07bab4d92be2` |
| binding-package-query01-launch/RUN.json | `6606d744adebc488bccaad3bce55e470837bb9849cdc53785b066cae08cdc510` |
| binding-package-query01-launch/SUPERVISION.json | `c2f9847031d59c17f5549c6bb13416fe9d40e4ced4508f41b7dce74084143c4f` |
| binding-package-query01-launch/child/command.json | `872514ce779a2205dc48692c02174d871b7530f75551d57b4f640b05a1720cc5` |
| binding-package-query01-launch/child/stdout.txt | `6eaabbde5960cb0c2ddd1b2c41d631ef7df3bc26cbe785c363b79477a7ea8ea9` |
| binding-package-query01-result/RESULT.json | `77c9799a82c672d36d6d25f9f28bfbcc27aad63763151989aa7d0eaf85219a60` |

All 166 selected package/receipt/runtime/input pins independently rehashed and
still match. Actual child command equals LAUNCH/SUPERVISION argv, follows the
selected public runner's argument transformation and uses the original inert
inputs. Its limits agree across all three records. No fixture copy was used.
LAUNCH's initial `NO_CHILD_LAUNCHED` is a prelaunch record; terminal RUN and
SUPERVISION establish the later outcome, not an inconsistent second attempt.

## Result and preserved meaning

Terminal RUN is `CLI_EXITED_ZERO`, exact new PROFILE
`dc0c19b7cf116742caa0751665da93400f6bc5b4663cfe313c3e81aa0d9c58e0`, unchanged
INSTALLATION `32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.
Child stdout is exactly RESULT.json plus one LF; stderr is empty. Result contains
`ok:true`, `operation:prepare-query`, zero worker CPU and
`mathematical_acceptance:false`. Native-type and binding hashes equal selection.

Against retained `ordinary-query-public-01/public/query-prepared/`, actual new
QUERY.json is byte-identical (1035 bytes; `eb611ed660111779f3bf1a05c044c2a362735d08eb91f7a6151ea80d9108c16a`)
and SPECS.json is byte-identical (104 bytes; `7c707bb2b3f5cc2628eef4fcb933c7944156ead940ad02465fa42084049dc72d`).
The parsed operation, namespace, specs, features, key profile, query/input hashes,
acceptance, claim, next and ok fields all match. Original result has its historical
PROFILE `2b8ac8cad152dde90a1b51d19dd1a821305bd7242b601c10eaa7a39f0db572f5`;
profile identity and measured costs are deliberately not required to match.
The fresh result directory contains exactly QUERY.json, SPECS.json and RESULT.json.

## Closure and cost

SUPERVISION records `COMMAND_EXITED_ZERO_AND_CLOSED`, child exit 0, child reaped,
Job closed, zero final active/terminated processes, no termination request and
no cleanup errors. Cumulative process count 2 is not simultaneous occupancy;
the selected one-active-process ceiling reports no violation. Bounds remain
35 wall / 10 CPU seconds, 512 MiB and 1 MiB per output stream.

Launcher wall is **1.1261235 seconds**. Child Job CPU **0.953125** plus launcher
wrapper CPU **0.109375** gives **1.0625 known CPU seconds**. Peak Job private
commit is **31342592 bytes**. Query controller CPU 0.875 and supervisor wrapper
CPU 0.015625 are nested observations, not additional costs. Wrapper containment
remains cooperative as prospectively stated.

The actual new profile and auxiliary binder load successfully through the public
manual-query path. This is not writer binding, Std production, mathematical
admission, owner-state compatibility, a speedup comparison, revised distribution
or final-v5 completion. The earlier failed Std operation remains failed; this
pass authorizes no retry or additional runtime.
