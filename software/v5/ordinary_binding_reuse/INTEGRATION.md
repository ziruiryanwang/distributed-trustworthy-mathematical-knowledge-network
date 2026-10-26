# One-payload integration decision

2026-10-26. `practical_library_route`; source/read-only only. Root selects any run.

## Exact change and loader argument

Base: `experiments/v5-local-checks/multi-source-package01/suite/assembled/package`.
Base PROFILE: `ca257419f464c2e9d968011983673160377f743ebbe2a27e2399b510dce1ce67`.
Base ASSEMBLY: `ec5ab7709aba2c4a896fa1898e925effb8f7a95f17bdb300c55307fcc5c10d6c`.
Only payload destination: `reference/baseline_bundle.py`, from this directory's
reviewed successor. Its existing predecessor hash is `d5a9c13392e2de8b170cbaf4a9a27e4d1e5d99eb2714165848a640069fe42fce`.
Update only that file's bytes/hash in a newly canonicalized PROFILE. Expect
154 total files: exactly one changed payload plus PROFILE, 152 unchanged files.
All eight historical documents remain unchanged and need external current guidance.

The **actual base** profile.py (SHA `1f40fb7a663c10d8f09132375ac8ab7899dea5830fff4979e0dda66b668003f8`)
requires this logical path in BASELINE/:183, authenticates its selected PROFILE
pin/:188-195, scans the exact reference directory, and imports/checks its actual
origin/:235-238. It does not hardcode this payload's old hash. Its module imports
and public APIs are unchanged. Thus the existing loader contract accepts the new
layout given the correct new PROFILE and unchanged approved runtime prerequisites;
this source argument is not an executed load or approval of arbitrary bytes.

INSTALLATION remains `32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.
Installed core, semantics/foundation and implementation I remain exact: I derives
from INSTALLATION's implementation/support groups, not this auxiliary payload
(`installation/py/ordinary_admission.py:241-253`). Native helpers and executables
are unchanged, so no native rebuild is needed. Existing mathematical state keeps
its exact implementation identity, subject to its normal current-owner validation.
`authoring/py/module_export.py:27-65` excludes baseline_bundle from its narrow
support descriptor; owner/loader/module dependencies are unchanged, so anchor
support also remains exact. This is identity reasoning, not a fresh state reopen.

## Cheapest safe assembly, only if selected

Use a short root-owned, finite one-shot adapter with the already reviewed file
primitives in `ordinary_fair_search/assemble.py` (SHA `9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30`).
Reuse its pin/read_json/relative/ordinary/census/fresh_bytes, **not** its specialized
assemble command or the multi-source command's fixed three-file overlay contract.

1. Pin the original PROFILE/INSTALLATION/ASSEMBLY and reviewed successor. Derive
   all 154 paths from their exact maps; reject unexpected/missing paths/redirects.
2. Copy verified old bytes into one fresh disjoint output, substituting the one
   binder during copying; never edit any of the old 154 files. Copy ordinary
   separate files, not links into the frozen package. Keep receipt outside package.
3. Revalidate all source/output pins and complete census. Require exactly the
   two intended differences. Commit new canonical PROFILE last; record full map,
   predecessor/successor pins and new PROFILE in the external exact receipt.

## Compatibility and minimal changed-boundary evidence

The existing `ordinary_multi_source_package/prepare_selected.py:56-60` compares
all 45 noncompiled roles against its pinned compatibility map, including this
binder. It will reject the successor with `SELECT_UNKNOWN_INTERFACE`; do not
silently alter that frozen map. Direct existing public CLI arguments remain usable.
Source archives likewise still map `reference/baseline_bundle.py` to the old
`ordinary_baseline` source in `ordinary_native_package/source-map.json`. Keep
all old ZIPs/manifests unchanged; a future source handoff needs an explicit one-row
overlay source map and matching companion compatibility update, not a false old
archive verification. A development overlay is not yet a revised distribution.

After independent review, smallest checks are the separately assigned small
valid/malformed equivalence controls, one finite successor-only bind of retained
Std writer bytes (summary/manifest only, no 2,651-file materialization), complete
package-map verification and one state-free public loader/query preparation.
None requires native extraction, intake or an old full Std binder rerun. Inspect
counts (2n to n) plus the source proof justify removed work; record successor
cost without inventing matched wall-time speedup. The original public Std failure
stays failed; these checks would not establish successful public production,
kernel admission, warm Std authoring or whole-v5 readiness.
