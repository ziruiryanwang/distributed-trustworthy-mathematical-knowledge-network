# Ordinary owner package: selected source interface

2026-10-23. This is the coordination contract for the new source-only package,
not a completed release. Preserve the existing acceptance core and generic
contribution API. All old used sources, installations and evidence stay frozen.

## Layout and ownership

The builder takes explicit repository source, Lean distribution, Python
distribution and fresh output roots. It must not use experiments or product-local
as dependencies. Its output has these separate roots:

- `installation/`: unchanged ordinary_installation assembler output.
- `authoring/helpers/`: the 13-module authoring compiled closure only.
- `authoring/py/`: the six authoring Python helpers from the package plan.
- `support/`: the eight namespace-package store/transport/discovery helpers.
- `author_worker.py`, `owner.py`, `profile.py`: the new standalone entry points.
- `PROFILE.json`: local package descriptor, emitted last and bound to the exact
  installation manifest and every auxiliary payload. It is not peer evidence.

Root owns this interface, exact preserved receiver/supervisor sources, selections,
integration and Git. ordinary_api_flow owns `build.py` and its build checkpoint.
The owner CLI agent owns `owner.py`, `profile.py`, `author_worker.py` and its CLI
checkpoint. admission_event_audit independently reviews these new boundaries.
No agent edits another owner's files or the used generic contribution source.

## Shared descriptor

Use schema `DMKN_ORDINARY_OWNER_PROFILE_V1`. It contains exactly `schema`,
`installation_manifest_sha256`, `helper_paths`, `author_worker`, `files`.
Helper paths and worker are package-relative POSIX paths; helper_paths is
`["authoring/helpers"]`, author_worker is `author_worker.py`. Each files entry
maps a package-relative auxiliary payload path to `{bytes, sha256}`. Include
all authoring Python/helpers, support files and new CLI/profile/worker files;
exclude installation payloads (separately pinned), build logs and PROFILE.json.
Canonical JSON follows the existing ordinary evidence codec. CLI requires an
owner-supplied exact profile SHA-256; the hash is selection, not authentication.
Runtime roots remain explicit and external. No absolute build paths in PROFILE.

The CLI validates the descriptor/pins before importing auxiliary code; installs
the installed core import root first and checks shared actual module identities.
The profile loader constructs the unchanged AuthoringProfile. Namespace support
and authoring Python roots must not shadow installed core. All helper-directory
files are covered; no receiver helpers may leak into authoring LEAN_PATH.

## Initial operations

Only init/status/contribute. Explicit local owner/custody/store identities,
explicit parent root for contribution, source file, acquired-target JSON,
output-name JSON, fresh output directory and one finite resource allowance.
No owner copying, inferred parent, implicit retry, basis replay, certificate,
network request or remote publication. Preserve actual accepted state on later
failure. Source is owner-approved executable Lean, not untrusted peer data;
Windows Job limits are not a hostile-source sandbox.

The agents may propose a smaller or safer concrete interface adjustment, but
must coordinate before depending on it. One reviewed clean build and one new
ordinary lifecycle boundary are sufficient next runtime evidence. Runtime
selection remains root-owned and is not authorized by this source contract.
