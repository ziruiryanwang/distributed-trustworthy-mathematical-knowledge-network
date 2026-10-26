# Independent direct-build selection review

2026-10-26. `current_acceptance_challenge`. Source-only review of the local
selector and finite plan; no build or product import by this reviewer.

**CLEAR_FOR_CONDITIONAL_ROOT_SELECTION.** Root must first adopt a successful
repaired-continuation outcome and its actual source-extraction manifest hash.
Then inspect the generated exact selection before launching it once. This review
does not supply a substitute hash, approve controls01's faulty distribution or
pre-authorize any retry.

| Source | Bytes | SHA-256 |
|---|---:|---|
| `select_build.py` | 7,198 | `3e1ed8d29c08df0bb1c20e70ce6733ccc601ec3798c29b89f0e413138b629e10` |
| `BUILD-PLAN.md` | 7,799 | `3b1991938ab03210eea829915fbc0fff2c4cfb5b689b4303ac8fdb62c3a321b5` |
| existing `tools/Run-V5-Check.py` | existing frozen runner | `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651` |

The current builder and bundle remain the reviewed `86612e8c...` and `437cc3c0...`
sources. Their compiler semantics were not reaudited here; REVIEW.md records the
complete changed-source review and unchanged compiler/supervision paths.

## Actual source extraction, not a reconstructed checkout

The selector accepts an explicit absolute extraction under the canonical project's
experiments tree and an independently approved outer-manifest SHA-256. It executes
only the hash-pinned bundle and frozen file helper to verify that extraction,
requires source kind with 106 payloads, and includes its outer manifest for
**107 exact extraction files**. No original-repository copy of the 93 build inputs
is used as the build's source root; no historical overlay or extra source tree is
created. The selected builder, bundle, release and helper snapshot pins must equal
their extracted counterparts. The direct builder's own byte-equivalence check
therefore permits its reviewed snapshot entrypoint with this extracted source root.

The selector records all 107 files as external pins, adds exactly 23 runtime
files from the fixed release map, and requires 130 case-distinct total pins.
The runtime roots are the explicit installed Python 3.14.6 and Lean 4.34.0 paths;
the running interpreter must be the selected Python. Ordinary-path, length and
streamed SHA-256 checks, exact extraction census and final rechecks protect the
selection. These are named runtime pins, not a hermetic compiler/library census.

Seven small source snapshots bind the existing runner, selector, plan, builder,
bundle, release and helper. The generated command uses the existing runner's
snapshot/output placeholders and passes the adopted extraction as `--source-root`.
The selection/output names are fresh and separate from the extraction; selection
is written exclusively and read back. No compiler, owner or network operation is
launched by this selector.

## Finite containment and accounting

The proposed limits exactly match the retained bounded-investigator-src01
selection: outer 540 wall / 440 inclusive CPU seconds, 2304 MiB, eight active
processes and 1-MiB stdout/stderr; direct controller 480 wall / 360 aggregate CPU
seconds with 2048-MiB child Jobs. The retained saved result independently confirms
60.07867900002748 seconds overall wall, 52 inclusive Job CPU seconds,
1.328125 separate wrapper CPU seconds and 925,749,248-byte peak Job private
commit. This supports a finite local envelope, not a promised new runtime.

The three direct child Jobs remain sequential. Each receives remaining wall minus
25 and remaining CPU minus 62; the lower builder further subdivides its grant.
Unknown child CPU is charged its full reservation and stops the build. Inclusive
parent/child CPU is not added twice; outer-wrapper CPU is reported separately.
The nested process caps are simultaneous inherited limits, not additive quotas.
The outer runner permits these bounds and pins all extraction/runtime inputs
before and after the operation. Jobs provide containment of resource use, not a
hostile-source filesystem/network sandbox.

## Required outcome boundary

Require clean outer closure and actual complete child/nested-compiler records,
not an early build file. The final package must have 154 files, including actual
INSTALLATION and PROFILE, with 45 fixed noncompiled and 72 generated auxiliary
roles and all eight documents. Generated identities must come from actual
compiler outputs; exact prebuilt hashes are not fresh-build requirements.

A pass would establish the direct extracted-source build/assembly boundary only.
Any smallest justified public-use check is a later root decision. No repeat of
previous mathematical/growth campaigns follows automatically. Keep all partial
failures and original allocations. This source review made no local source,
runtime, state or Git changes beyond this review document.
