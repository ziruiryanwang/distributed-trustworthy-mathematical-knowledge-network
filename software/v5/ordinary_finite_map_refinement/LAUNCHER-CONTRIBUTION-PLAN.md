# Use the public launcher for the corrected theory contribution

2026-10-28. Source/data invocation proposal only; root creates the exact fresh
selection and launches. No extra harness or repeated direct-owner operation.

Use `frontier-launcher-package01/distribution/package/run.py` under canonical
`experiments/v5-local-checks`, with actual PROFILE
`efa1e0894a24859bf1c7648ccaf72674c7cf136c9fce32a62020e75cb24bcd45`.
The launcher-only successor changes run.py, its profile entry and LAUNCHER.md;
the mathematical receiver, owner and frontier implementation are unchanged.
Use fresh run name `finite-map-refinement-contribution02`.

## Exact argument arrangement

The selected interpreter command starts `D:\Python314\python.exe -I -S -B`
and the new package's absolute `run.py` path. Then supply these launcher arguments
**before** the positional `owner`:

```text
--profile-sha256 efa1e0894a24859bf1c7648ccaf72674c7cf136c9fce32a62020e75cb24bcd45
--python-runtime D:\Python314
--lean-runtime E:\Distributed Trustworthy Mathematical Knowledge Network\software\runtime\lean-4.34.0-windows
--diagnostics {output}/launcher
--wall-seconds 150
--cpu-seconds 90
--memory-mib 1536
--active-processes 6
--stdout-bytes 1048576
--stderr-bytes 1048576
owner -- contribute
```

The rest is the direct contribution command's operation-specific options:

| Child option | Value |
|---|---|
| catalog | canonical `experiments/v5-local-checks/std-kernel-catalog01` |
| custody | canonical `experiments/v5-local-checks/std-kernel-custody01` |
| store-id | `fb625cc1b7d03d081e45bbcf73f7d59765f04a64a402484f23d00ac3e60ce4e7` |
| parent-root | `ad4aa90b014ff326ded6f4750dd4f6ac7e3b56d15027114b91788923d0238079` |
| custody-limits | `{snapshot}/software/v5/ordinary_std_intake/custody_limits.json` |
| source | `{snapshot}/software/v5/ordinary_finite_map_refinement/BodyParametric.lean` |
| acquired-targets | same snapshot directory's `discovered-acquired-targets.json` |
| output-names | same snapshot directory's `output-names.json` |
| project-authoring | same snapshot directory's `project-authoring.json` |
| project-authoring-sha256 | `0e049b81ae2da26afdfe4ed515ab9bf752ec1585d6bbeb803170a74a9d223e39` |
| authoring-frontier-root | `b75b2800b956aedbbb9c333806a7b369f3213442634482c1e3818137fefac6a6` |
| output | `{output}/contribution` |

Expand each table option to its exact `--name` token followed by the separate
value token. Actual selection entries are absolute paths; `{snapshot}` and
`{output}` are only the existing Run-V5-Check substitutions. Do not put literal
"canonical" or "same snapshot directory" text into argv.

Remove child profile/runtime/wall/CPU/memory arguments: run.py appends them
exactly once from its selected outer arguments. Do not add
`--approve-local-project`, which the owner reserves for produce-baseline.
The updated owner allowlist accepts authoring-frontier-root, validates lowercase
64-hex shape and forwards the exact flag/value pair unchanged. Actual existence,
ancestor-prefix and final-parent checks remain inside the unchanged owner.

## Envelope and paths

Keep Run-V5-Check's enclosing limits at 180 s wall / 110 s CPU / 2048 MiB /
eight processes / 1 MiB per stream. No increase is needed. The public launcher
keeps the owner's maximum 150/90/1536 and also bounds the whole owner subtree.
Its six-process limit covers the owner plus the existing at-most-four-process
native operation subtree; outer eight additionally covers the launcher. This is
an upper-envelope argument, not a measured prediction of elapsed time or memory.

The public launcher begins elapsed accounting before its bootstrap; passing the
same limits to the child does not renew that Job allowance. Its own CPU is
outside the public child Job but inside the enclosing Run-V5-Check Job. Report
outer aggregate CPU once; do not add nested Job CPU measurements to it.

`{output}/launcher`, `{output}/contribution` and `{output}/sources` are siblings.
This satisfies fresh diagnostics, input/output and protected-state separation.
run.py starts owner.py with the diagnostics directory as child cwd; owner.py
has no canonical-cwd requirement. The project descriptor already supplies an
approved absolute project_cwd, runtime search path and Std import, so source
elaboration does not depend on the launcher's cwd.

Inspect launcher/LAUNCH.json for the exact child argv including P/F and source,
launcher/SUPERVISION.json and RUN.json for closure, and
launcher/child/stdout.txt for the owner's report. Mathematical acceptance still
comes from the contribution's actual checked result and native evidence. Reuse
the existing endpoint and frontier assertions; preserve any failure without an
automatic retry or direct-entry fallback.
