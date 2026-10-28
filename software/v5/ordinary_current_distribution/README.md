# Build the current ordinary mathematical commons

**Source candidate only: no build of this new controller has run.** Independent
review, focused changed-boundary checks and root's separate execution selection
are required before using it as an approved build recipe. This is not a final-v5
release, and everything remains local and unpublished with license undecided.

This builder combines the current ordinary checking, frontier authoring and
bounded multi-source/sparse search sources directly. It does not need historical
experiment packages, old owner state or intermediate overlay builds. Its fixed
`source-map.json` identifies 87 existing source files, plus this builder and map.
The source archive successor has not yet been prepared.

Use independently approved complete Windows x86-64 Python 3.14.6 and Lean 4.34.0
distributions. Their selected file pins are checked; other runtime files remain
part of the explicitly approved, nonhermetic toolchain. Source and build
directories must be owner-controlled and immutable during the operation.

After selection, the intended invocation is:

```powershell
& 'C:\approved\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_current_distribution\build.py' `
  --source-root 'C:\commons-source' `
  --python-runtime 'C:\approved\Python314' `
  --lean-runtime 'C:\approved\lean-4.34.0-windows' `
  --output 'C:\commons-builds\current-01' `
  --wall-seconds SELECTED_WALL_LIMIT `
  --cpu-seconds SELECTED_CPU_LIMIT `
  --memory-mib SELECTED_MEMORY_LIMIT
```

Replace the three allocation placeholders with the independently selected
integer bounds. Accepted controller ranges are 120–3600 wall seconds,
100–3600 CPU seconds and 256–8192 MiB. These are hard validation ranges, not an
estimate of required resources. The output parent must exist and the output
directory must be fresh. Use an outer owner Job for hard controller containment.

The output is `package/` plus `_build/` evidence. Require terminal command
success and clean enclosing closure, then verify `_build/BUILD-RESULT.json`
against actual `package/PROFILE.json`, `installation/INSTALLATION.json` and the
complete file map. A directory or partial receipt alone does not prove success.
Failures preserve their partial output and must not be overwritten or retried
implicitly.

Use that build's actual PROFILE and implementation identities. Compiled bytes
may change across build locations even when source is unchanged. This recipe
does not claim bit reproducibility and does not authorize reopening an existing
owner under a different implementation. Start with fresh adoption unless a
separately justified migration exists.

The built package's `run.py`, `README.md`, `LAUNCHER.md`, `RECEIVE-POLICY.md`,
`SPARSE-SEARCH.md` and `CONTACTS.md` describe the public interface. The current
[frontier API](../ordinary_demand_frontier/API.md) explains reuse above a checked
library ancestor. Agents still choose their own investigations. Mathematical
acceptance remains the actual protected-parent checker, not authoring success,
index ranking or approval of downloaded source.

Do not use the older `ordinary_operator_kit/prepare_selected.py` as a current
package entrypoint: it recognizes only earlier layouts and has no contribution
preparation schema. Direct documented launcher arguments and inert JSON
configuration are the current route. No additional platform, hosting service,
certificate engine or operator kit is introduced by this build integration.

See [the implementation contract](CONTRACT.md) for exact scope, trust premises,
required evidence and retention rules.
