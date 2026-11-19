# Source-only plan: compact ordinary source handoff

Status: implementation awaiting independent review and root's exact file-only
execution selection. No native build, product import, experiment repetition,
network request, mathematical state or public release is selected.

## Exact source closure

Preserve the existing layout; do not edit any predecessor. The handoff has 105
payload files plus its generated `SOURCE-MANIFEST.json`:

- 84 unchanged inputs from the exact bounded-operations source map.
- Its own `build.py` and `source-map.json` (86 baseline files in all).
- Six fair overlay files: assemble.py, profile.py, peer_api.py, fair_exchange.py,
  fair_search.py, README.md.
- Eight operator files: prepare.py, prepare_selected.py, compatibility.json,
  examples.json, START-HERE.md, SELECTED-PACKAGE.md, SELECTED-KIT.json,
  AUTHORING-OFFERS.md.
- Two necessary authoring-offer reference documents: CODEC.md and API.md.
- Three new bundle files: bundle.py, README.md, LICENSE-STATUS.md.

The 102 unchanged files total 3,137,466 bytes. Their bytes are pinned by the
fixed bounded map SHA and utility's fixed 18-entry additions map. The new
utility/guide/license-note bytes are owner-selected, hashed into the generated
manifest, and must be explicitly pinned in root's execution selection. The
running utility must equal the selected `source-root` utility bytes. This permits
execution from a pinned finite-run snapshot without requiring inherited cwd or
silently using another utility implementation.

No archive, runtime, binary, retained state, experiment, test suite, audit ledger,
build output or private user data is a payload. MANIFEST-PLAN.md and the separate
test/review files are evidence, not compilation dependencies or payloads.

## CLI and import-safe file-only APIs

```text
bundle.py pack --source-root ABSOLUTE_SOURCE --output FRESH_DIRECTORY
bundle.py verify --source-root ABSOLUTE_EXTRACTION --manifest-sha256 EXACT_HASH
```

Use approved Windows Python with `-I -S -B`. Importing bundle.py defines only
stdlib helpers and constants. Direct selected tests may call:

```text
pack(source_root, output, *, check=None)
verify(source_root, manifest_sha256, *, check=None)
```

The optional callback enforces a caller's original aggregate deadline; each API
also retains its own cooperative maximum 60 wall / 30 CPU seconds. No call can
renew the caller's allowance. Internal checks cannot preempt a blocking disk/OS
operation; use an external Job when hard containment is required. No resource
framework or automatic retry is introduced.

## Output and manifest

Packing creates only a fresh selected directory with `source.zip`, then a
terminal external `RECEIPT.json`. Inputs are read only by the allowlist; no
recursive scan of the research workspace occurs. ZIP members are sorted, stored
without compression, fixed at 1980-01-01, Unix regular-file mode 0644, without
comments/extras. This avoids compression-version variability and costs only
about 3 MiB. No platform permission grants are implied by ZIP metadata.

The ZIP root is `SOURCE-MANIFEST.json` plus the original `software/...` paths.
Manifest canonical encoding is UTF-8, sorted keys, compact separators, no BOM
or trailing newline, nonfinite numbers or duplicate object keys. Exact fields:

```text
schema: DMKN_ORDINARY_SOURCE_DISTRIBUTION_V1
claim: EXACT_SOURCE_INPUTS_NOT_BUILD_OR_MATHEMATICAL_ACCEPTANCE
files: relative path -> {bytes: positive integer, sha256: lowercase 64-hex}
entrypoints: fixed build, overlay and operator relative entry paths
external_profile: Windows x86-64 / Python 3.14.6 / Lean 4.34.0
license_status: UNDECIDED_NO_PUBLIC_RELEASE_AUTHORIZATION
```

The manifest excludes itself; its hash is in the external receipt and root's
selected handoff. The receipt also pins the whole ZIP and records the 105/106
payload/archive counts, total payload bytes, source/output paths and scoped
claim. A receipt is an integrity statement from selected code, not signature,
source approval, license, mathematical acceptance or final-v5 qualification.

Verify requires an externally selected manifest hash, canonical manifest bytes,
exact frozen 102 pins, the exact 105 path set, file contents and exact extracted
tree census including its only allowed directories. It never extracts an
arbitrary archive or executes any payload. Callers must first approve the utility
and ZIP hash independently before extraction/execution.

## Validation and failure invariants

Bounds: 2 MiB per payload/JSON; 8 MiB payload total; 16 MiB archive read; 105
payload files and 106 members; 256 scanned extraction entries; path depth at
most 12. The extraction census rejects extra files **and empty directories**.
Paths reject traversal, Windows reserved names, alternate streams, control
characters, absolute/UNC member paths, trailing dot/space, casefold duplicates,
file/directory aliases and redirected/hardlinked files. Every ancestor is checked
for a symlink/reparse point; only ordinary local drive paths are supported.

File immutability/owner control is a premise: these checks do not eliminate all
concurrent filesystem races or create a sandbox. Before committing the receipt,
packing rereads its output ZIP, checks all metadata/content and rereads every
source plus the running utility. Verification checks before/after census and
manifest identity. Failed output remains untouched; no overwrite, deletion,
cleanup or implicit retry is possible.

No fresh native build is justified to establish that unchanged source was copied.
The selected test should perform one actual file-only pack, controlled extraction
and relocated verify, plus direct adversarial/path/pin/partial-output controls.
An independent test author derives expected files without using the utility's
allowlist as its own oracle. Native build and mathematical qualification remain
with their existing evidence and any future explicitly selected changed boundary.
