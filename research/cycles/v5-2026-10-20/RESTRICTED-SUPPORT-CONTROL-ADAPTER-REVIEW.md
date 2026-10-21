# Independent source review: support-control runner and selector

2026-10-21, core_growth. **PASS_SOURCE_REVIEW_CONTROL_ADAPTER_ONLY.** No blocking
source defect found. No source was changed and no selector, import, test, native
child or other product code was executed. This review does not adopt the future
build or controls outcome.

Exact reviewed files:

| File | SHA-256 |
|---|---|
| `software/v5/restricted_support/run_controls.py` | `ff5d4317fd498b6f5de03524947d0ef06569b83128950fa7c001e0ca557e18d7` |
| `research/cycles/v5-2026-10-20/Select-RestrictedSupportControls01.ps1` | `698ed9da2c2e820954fbf0f8cb38fbc0c6b1b6f5a7dffee1e7aae67cfd94230d` |

Scope is the two files above and their existing owner/build interfaces, not a
repeat of core, controls or builder review. The actual eight-source support
build schema/map/output shape was checked against the builder source only.

## Input and build bindings

The selector requires root-supplied exact build-result, binary and adapter
digests. A successful two-compile result must use the expected schema/status;
an existing overriding finalization-failure marker refuses selection. The
fixed controls executable's hash and length must equal its output entry in
that result. The sibling terminal attempt must bind exactly that result/status.
The original sibling build selection is matched to `selection_sha256`; it is
not confused with any reserialized saved copy.

The exact eight-source build map is checked against the original selection by
name/hash/length, and each current source byte is verified. Adding the frozen
Run-V5-Check owner and reviewed wrapper gives exactly ten selected sources.
The fixture is the already used84727-byte differential fixture at its exact
original path, SHA-256 `019219ca4548dafbdaa814c209a4ec087229091750db3f3cf48fcc155269f40a`.
Read-only verification corroborated its digest. No fixture generation or new
mathematical target occurs in the wrapper.

The retained pinned runtime basis supplies18 Python files and the exact Python
entry; this shape was checked by reading the existing basis record. The selector
also pins build result, actual binary, attempt, original selection, source map
and fixture. Result/binary hashes are adoption inputs from root, not inferred
authority from mere file existence. Root must supply them only after independent
actual build adoption. The selector is not a standalone build-outcome auditor.

## Canonical paths and process ownership

The wrapper requires Windows, explicit canonical cwd, isolated/no-site/no-bytecode
Python, no optimization, no extra arguments and its exact expected Run-V5-Check
snapshot path. It invokes only the fixed absolute controls executable with the
fixed absolute fixture path, with canonical cwd. The environment is reduced to
Windows system variables/System32 and disabled Rust backtraces; it does not load
the surrounding development Python packages or regenerate inputs.

Run-V5-Check validates the selected ordinary absolute runtime paths, snapshots
all ten sources, and pins runtime bytes before and after the command. Its
canonical-path checks reject reparse ancestors/targets. The native process
inherits the already established enclosing Windows Job; no breakaway or new
background process is requested. The wrapper launches exactly one child, with
a30-second direct timeout. It passes through the exit code; a timeout raises
after Python's direct-child kill/wait, leaving the outer owner responsible for
whole-tree cleanup. Outer limits are30inclusive CPU/60wall/512MiB/three processes,
with1MiB stdout/stderr. Threads in the Rust harness do not consume process slots.

Inherited stdout/stderr go directly into the outer bounded retained logs. This
deliberately avoids another nested report or JSON reserialization. No second
supervisor CPU total is introduced and no fixture/readback report is fabricated.
If the wrapper or native child fails, or any descendant remains, the established
outer supervisor cannot report a clean exit0. The owner retains raw failures,
performs final bindings and writes its own result. No retry path is present.

The selection/output directory must be fresh and selection is create-new and
durably flushed. The support build and its terminal failure marker are assumed
closed/immutable after root adoption, as required by project rules; the wrapper
is not a concurrent hostile filesystem authorization service or security sandbox.

## Required terminal interpretation

Exit0 and clean outer closure establish only that the selected binary completed.
Independent actual audit must still parse its retained native stdout and check
the exact named control contract, expected refusals, both real fixture endpoint
comparisons, work counters and any structural fixture bindings. It must inspect
the final outer pin/cleanup outcome and preserve all failures. The wrapper does
not substitute a generic PASS string for that audit.

No mathematical admission, guest-row improvement, proof investment or v5 release
claim follows from this source-review pass. No changes requested.
