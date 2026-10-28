# Dedicated hosting package integration review

2026-10-28. **PASS for the selected source/map and file-only assembly boundary.**
This review read source, JSON metadata, documentation and file hashes only. No
product import, build, assembler, test, service, database, owner or Git operation
was executed. It supplements [REVIEW.md](REVIEW.md), whose changed-role source
argument is not repeated here.

| Input | SHA-256 |
|---|---|
| `assemble.py` | `68f2104d7fbd4e162f9a49665f112a8480a7d58fac880aa2e24e523d02057fbd` |
| `build.py` | `c20461653e11a6cc17fb1c12fa18e87a8603632f8d94ae9a3334dd15552d4f4f` |
| `source-map.json` | `4d81960236ca77ed192626990b64c9a4d06965529879ace0c89b6af860e1cf1d` |
| `PAYLOADS.json` | `ee406ee04f7763ca45791cf2faba6e69ad23235fa834c4b43ab7f463388d65d2` |
| `HOSTING.md` | `388f52744ae2686c3fc0231c0c17ef892e764032c55809a55fcbcf825b26ea52` |
| `LAUNCHER.md` | `cfed6e6a96fb3847990f418cc085bd435162c2a98b8e6b258248f1623971c179` |

## Exact selection and arithmetic

All **91** source-map entries were compared with the current selected files;
every byte count and SHA-256 matches. The exact source closure is the union of
direct-copy origins, compiler-lane origins and the two selected build tools:
91 entries, no missing or extraneous source. All nine PAYLOADS entries agree with
their source-map roles and pins.

The original current build receipt and PROFILE were read and hashed:

- Receipt: `08ef24292afc45b7cfae7075c0ea2231f45ea88e02cc05bca2dd263f95612863`.
- PROFILE: `d5e56dd3bb2d1a531abeaabf06aea1864a7037c88a2035749230574455d7d4b0`.

The receipt has 154 package paths and the expected build/profile/installation
bindings. All 45 compatibility direct-source pins match its PROFILE; its other
72 auxiliary roles are the existing generated outputs. This review reuses the
prior package audit rather than rehashing all old generated binaries. The actual
assembler still checks every base file and exact directory census before use.

Applying the selected nine payloads implies exactly:

- Six changed existing files: `LAUNCHER.md`, `PROFILE.json`, `owner.py`,
  `profile.py`, `query.py`, `run.py`.
- Four additions: `HOSTING.md`, `advisory_context.py`, `custodian.py`, `host.py`.
- 148 unchanged existing files and 158 total files.

None of the nine selected payloads is accidentally unchanged. PROFILE gains the
three auxiliary roles and replaces the four existing executable-role pins; its
installation hash, worker and helper path retain their values. Documentation
stays outside PROFILE's executable auxiliary map, while remaining pinned in the
assembly receipt and portable source map.

The full-builder arithmetic also agrees everywhere it is enforced or reported:

\[
76=19\text{ installed direct}+48\text{ auxiliary direct}+9\text{ documents},
\]
\[
157=76+8\text{ receiver}+65\text{ authoring}+5\text{ query}
       +2\text{ extractor}+1\text{ installation manifest}.
\]

There are 120 auxiliary payloads (48 direct plus 72 generated), followed by the
one PROFILE file. Source validation, case-folded census, traversal cap, final
auxiliary assertion and result fields all use the corresponding updated counts.
No stale prior 87/72/153/117/8 source/copy/payload/auxiliary/document count was
found in the changed builder conditions.

## Preserved native boundary and assembly behavior

Relative to `ordinary_current_distribution`, the map's compiler lanes and their
transforms, native runtime pins, native output roles, authoring companion suffixes,
profile configuration and build tools are unchanged. All 19 installed direct
roles retain both their selected sources and exact pins. The builder's textual
changes are confined to its prefix/map pin, hosting documentation and the derived
counts; the compiler, installer and final verification code remain unchanged.

The file-only assembler starts from the explicitly pinned original current build,
not an intermediate overlay. It validates that receipt/profile/compatibility
intersection, captures all nine exact replacements/additions, checks the exact
six/four delta, writes fresh files and readbacks, rechecks source and base bytes,
then creates PROFILE and a full receipt. It neither imports product code nor
invokes native tools or owner state. Its file helper is separately pinned. Stable
operator-controlled local files remain a premise; this is not hostile-source
attestation. A partial failed output is preserved, not automatically retried.

HOSTING and LAUNCHER match the reviewed public CLI and schemas: explicit fresh
generation, pinned config/seal, complete bundle disclosure, finite service,
invocation-specific listening readiness, whole-process supervision and unchanged
recipient checking. Their examples disclose placeholders and remain source-stage
instructions. They do not claim internet operation or mathematical acceptance.

## Selected next operation

Root's `dedicated-host-assembly01-selection.json` selects this assembler, the
original receipt and PROFILE above, all nine payloads and their pinned helper/map
inputs. All 14 selected source hashes match. Its 60-second / 30-CPU-second /
768-MiB / two-process envelope is finite; the selected output was absent at this
review. No native build is selected. Actual successful assembly, focused new-role
controls and retained-data host execution remain separate outcomes to inspect.

This pass closes the integration-source decision; it does not promote an unrun
package to deployed software or establish full v5 completion.
