# Minimal frontier launcher integration

2026-10-28. Root-selected source preparation only. No controls, package assembly,
native build, owner operation, installation mutation or Git operation has run.
The substantive BodyMath contribution remains the central mathematical gate.

## Decision and source scope

The current direct `owner.py` supports the protected authoring frontier, but the
public bounded `run.py` rejects its flag. Adopt the already reviewed two-site
`run_frontier.py` change through a fresh package only after root selects it.
No checker, authoring helper, native artifact, state format or certificate changes.

The file-only adapter uses the pinned existing
`ordinary_fair_search/assemble.py` helpers for path validation, hashes, exact
census, strict JSON and fresh metadata writes. Existing overlay entrypoints have
different fixed schemas; none directly accepts the current exact receipt.
The new adapter is 111 lines and supplies only this package/overlay binding and
copy/readback loop. It never imports product modules or opens owner state.

| Prepared source | Bytes | SHA-256 |
|---|---:|---|
| `../run_frontier.py` | 18,991 | `63f70a8f27645e4e3e3f2ae85296f9c43bc2f0337b4534744dbd5eb0411029dd` |
| `control_tests.py` | 4,773 | `80735dbebe8bf9f7affa7d50d03dfc488886cb4962aaad5d4d9028f836e198d3` |
| `assemble.py` | 6,412 | `a1608522d25b574755a8e0a83764abc29c9d8909c0a8d1e8754e3656094890e3` |
| `LAUNCHER.md` | 7,607 | `66b58b9512df12b2e4bed0b18fd81f1343e406293a3ac68ef135eaa41cc3173a` |

The unchanged file-helper SHA is
`9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30`.
Both new Python sources pass static `ast.parse`; their functions have not run.

## One focused native-free control invocation, if selected

Snapshot the control source and `run_frontier.py`. Run only `control_tests.py`
under the existing `Run-V5-Check.py` with Python `-I -S -B`, explicit canonical
cwd and suggested outer limits 30 wall seconds / 10 CPU seconds / 256 MiB /
three processes / 1 MiB streams. Root binds exact sources and the selected Python
runtime; additionally pin frozen package `run.py`
`47a2b63c73f1bd8346c5881c6d6a76abac86d33aa8e55bfc19bf3359ea924a39`.

Seven groups cover: exact new flag forwarding without changing the parent;
four malformed hex values; duplicate flag; missing/equals syntax; refusal by
peer/query; unchanged no-frontier invocation against the frozen parser and the
frozen omission; and exact two-site source delta with unchanged other routing,
path sets and limits. The test loads only launcher definitions under a non-main
name and calls `child_arguments`; it never calls launcher `run`, owner code,
supervision, network or native workers. This is not a broad regression suite.

Require the exact seven named groups, zero child/native/owner calls, outer clean
closure and independent saved-output review. Preserve any failure. This does not
qualify an installed public operation.

## One file-only assembly, if separately selected

Exact base is `demand-frontier-package01/distribution/package`, with sibling
ASSEMBLY SHA `6ada680868401735ea4abd2fb04b43c064b67d78da7eb46db1032c0b590517a8`,
PROFILE SHA `6af0c3dee0a08d0ba0ec9f126dc6510481fc99569535c41b4ecb56c4bf3c3735`
and INSTALLATION SHA
`9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27`.

Snapshot `assemble.py`, `LAUNCHER.md`, `../run_frontier.py` and the existing
file helper at their canonical project-relative paths. Run the adapter once
with `--output {output}/distribution` under a fresh `Run-V5-Check.py` selection.
Suggested outer limits: 75 wall seconds / 40 CPU seconds / 512 MiB / three
processes / 1 MiB streams. The adapter enforces its own 60 wall / 30 CPU bound;
each selected file is at most 128 MiB and the package at most 256 MiB. It copies
using bounded-size stream buffers; the outer Job contains any interrupted copy.

The adapter verifies the exact 154-file base census and all hashes, replaces
only `run.py` and `LAUNCHER.md`, updates only run.py's PROFILE entry, and verifies
all source/output bytes again. PROFILE is written last in the package; the final
`ASSEMBLY.json` is a sibling, not a 155th payload. Expected actual delta is exactly
`LAUNCHER.md`, `PROFILE.json`, `run.py`: 151 payloads remain byte-identical,
including every installation/native/owner artifact. External runtime files are
not copied or asserted newly qualified. Fresh output is retained on failure;
there is no overwrite, deletion, retry, old-package edit or state migration.

Independent actual-map review and an eventual selected public-launcher use remain
separate gates. Assembly success alone is `ASSEMBLED_NOT_ADOPTED`, not v5 release
or mathematical acceptance. No package or larger campaign is launched here.
