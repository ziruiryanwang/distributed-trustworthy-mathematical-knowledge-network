# Separate export-location operator distribution

2026-10-28, root. This plan selects the source shape; exact execution remains
pending final source reviews and immutable source/guide/runner hashes.

The standalone package has 42 pinned source/support payloads plus SOURCES.json
and OPERATOR-USAGE.md shipped as USAGE.md. It contains no mathematical owner,
Lean executable, kernel installation, library evidence or historical state.
Its approved external Python and Node runtimes remain separate dependencies.
The Node controller authenticates the retained 5,896-file overlay/Node runtime
closure against its existing immutable release manifest before and after use.
Those checks bind runtime bytes; they are not a formal security proof.

`assemble_operator.py` adapts the already reviewed standalone-host file builder.
It uses the unchanged pinned file helper, captures all bounded selected files,
creates one deterministic stored ZIP, extracts only that exact member list,
and rechecks the inputs, extraction and census. All source paths are build-time
provenance. Runtime import paths come from the shipped role manifest.

Only the file helper executes during assembly. No product import, service,
database, Node, mathematical owner or Lean call occurs. The builder's own
cooperative limits are 45 wall / 20 CPU seconds. The prospective outer Job is
60 wall / 30 CPU seconds, 256 MiB, one process, 1 MiB per log. Expected payload
is below 1 MiB, within the fixed 4 MiB package ceiling. Limits are ceilings,
not measured cost claims.

Required arguments are `--source-root`, `--profile`, `--profile-sha256`,
`--guide`, `--guide-sha256`, `--output`. Select fresh output under
`experiments/v5-local-checks/export-operator-pack01/packed`. Root authenticates
the exact Python executable and two DLLs through the existing finite runner.
The output folder contains `export-operator.zip`, `export-operator/` and
BUILD.json. Failure preserves partial output; no automatic retry follows.

Focused controls and the real unknown-holder workflow consume the exact
extracted role. A package build establishes byte completeness only. Actual
service behavior, reader integration, public entrypoints and mathematical
acceptance retain their separate evidence scopes. Existing passed mathematical
and transport checks are reused; this change does not justify replaying them.
