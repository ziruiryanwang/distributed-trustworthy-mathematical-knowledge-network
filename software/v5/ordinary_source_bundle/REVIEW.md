# Independent compact source-bundle review

2026-10-25. Reviewer: concept_software_bridge, independent of utility and test
authors. Review scope is source/contract only; no packing, verification execution,
native build, test, network operation, Git or existing-state change is authorized
or performed by this reviewer.

## Current disposition

**SOURCE GO** for the utility, manifest plan, docs and final test source at the
pins below. No unresolved source blocker was found. This is source review, not
a test pass or launch authorization. Root owns a separate exact finite selection.

The reviewer wrote the earlier optional AUTHORING-OFFERS addendum; root already
independently reviewed/adopted that document. This reviewer did not author the
bundle utility, manifest plan, root source-bundle guide/license note or tests.
Frozen native/product code is preserved by identity and its already established
source map, not independently reaudited in full by this file-only review.

## Review obligations

- Preserve the existing baseline builder/map, native sources, fair overlay and
  operator kit exactly. Resolve the full selected closure, including the utility
  and required linked instructions, without copying historical outputs/state or
  requiring old runtimes as bundle inputs.
- `pack --source-root ABS --output FRESH_DIR` must select only explicit known
  files, bound total work, preserve original relative paths, and write fresh-only
  `source.zip` and `RECEIPT.json`. Failure keeps partial output; no cleanup/retry.
- `verify --source-root EXTRACT --manifest-sha256 HASH` must use that independently
  selected manifest hash, validate bounded exact census/pins and refuse extra,
  missing, redirected or ambiguous paths under its stated owner-controlled premise.
- ZIP member names, ordering, timestamps, metadata and bytes must be determined
  by the selected source set; absolute source-root names must not leak into the
  supposedly deterministic archive. Symlinks/reparse points, traversal, case
  aliases and duplicate members must not bypass selection.
- No product import, native/compiler/agent execution, network, credentials,
  protected-state access or implicit source/runtime/manifest download. File
  identity is not author authentication, licensing, proof validity or a claim
  of a newly performed native build.
- Read full test source once stable; distinguish tests that exercise the actual
  implementation from synthetic shape checks. Check meaningful negative paths,
  exact source-selection binding and retained failures without requesting another
  full project/test campaign.

The existing guide explicitly tells operators to approve utility and selected
hash independently, keeps runtime approval separate, requires fresh external
build outputs, and describes the unchanged two-stage build. No source-security,
bit-reproducibility, growth or worldwide-release claim is made.

## Completed source analysis

Read all of bundle.py and MANIFEST-PLAN.md, all root README/LICENSE-STATUS, the
entire initial test_bundle.py and the prior selected-kit metadata. The following
facts are established by this source inspection, not by execution:

1. `known_pins` reads a fixed length/hash source map containing exactly84 entries,
   validates its source/pin shapes and combines18 disjoint fixed additions. Three
   explicitly named new utility/doc files yield105 payloads. The new bytes must
   be selected in root's runner inputs; pack proves its executing utility equals
   the selected source utility. The manifest hash binds all105 actual contents.
2. No product code is imported or evaluated. Existing build/overlay files are
   inert payloads. No native/runtime/state/history tree is read by recursion;
   pack reads only the explicit source closure. The two builders' ordinary paths
   and fixed maps are preserved. Complete external runtimes remain independent
   prerequisites, not missing archive members or automatic downloads.
3. Pack validates selection before creating its fresh output, uses exclusive
   writes, creates only ZIP then receipt, and never removes or rewrites anything.
   It rereads original inputs, running utility and ZIP before the terminal
   receipt. Failure can retain a partial directory/archive; no cleanup, refund,
   success promotion or retry path exists.
4. Sorted stored ZIP entries have fixed timestamp, host-system/mode metadata,
   empty comments/extras and exact relative names. Manifest contents have no
   source-root/output paths. Those local absolute paths occur only in the external
   nondeterministic receipt. The actual ZIP is read back for exact member/order/
   metadata/content checks before its hash is recorded. This is a deterministic
   source archive construction, not reproducible native compilation.
5. Verify first requires the externally selected manifest SHA, canonical schema,
   the complete105 path set and exact102 frozen pins. It then checks every payload
   and both pre/post exact censuses, including allowed directories. NEW file pins
   derive authority from the independently selected manifest, not from arbitrary
   filename acceptance. Empty extra directories, extra files, missing files,
   aliases, reparse/symlink paths and hardlinked files are rejected by source.
6. Bounds cover per-file/JSON/total bytes, directory depth/entries and finite
   cooperative elapsed/CPU checks, with original caller callback retained.
   Blocking I/O and synchronous library calls are not preempted. An external
   finite Job and immutable owner-controlled filesystem remain premises.
7. The guide accurately distinguishes approval/authentication/licensing,
   file identity, extraction safety and build/mathematical claims. The utility
   does not extract arbitrary ZIPs. Source counterpart links for packaged
   LAUNCHER/PRODUCER/RECEIVE-POLICY are explicit and included. Frozen evidence
   references need not be bundled and are identified as references, not evidence
   of a new build from this archive.

The utility author's earlier API.md hash typo was corrected before this review's
selected pin and before any reported runtime. The selected source has the64-digit
pin. This is a pre-execution source correction, not a hidden failed-run rewrite.

## Completed test review

The independent test derives its expected manifest before packing from its own
fixed source-map/extras selection, not the utility's FIXED table. It uses one real
pack, exact known-member extraction, negative manifest/
payload/census cases and real hardlink refusal. Symlink denial due to Windows
privilege is reported as unexecuted, not passed. Inputs/failure fixtures are kept.
The no-native/network/SQLite traps apply to the in-process utility scope; they
are not OS isolation. No partial-write fault injection occurs in this initial
suite, so failure-retention assurance here is a source argument plus preserved
negative fixtures, not a measured disk-failure recovery result.

The final delta replaces the earlier in-process positive verify with exactly one
isolated Python public `bundle.py verify` from the relocated extraction. It passes
the manifest hash preselected before packing, not a hash trusted from the output.
Its process has explicit cwd/argv/logs, no stdin, the original harness's remaining
wall allowance minus cleanup reserve, and timeout kill/reap handling. The root
Job must bound aggregate child CPU/memory; the harness reports its own CPU as
process-only rather than charging the child's work invisibly to zero.

The child is outside the in-process Popen traps, deliberately, and runs only the
pure verifier, not product/native/compiler code. Child failure is failure; no
in-process positive fallback follows it. A final independent exact file/directory
census checks for unwanted bytecode or changed extraction shape. Case accounting
requires20 completed checks minus any explicitly unexecuted privileged-symlink
case. The final child delta was read completely; no larger test is requested.

Root's planned finite source selection must pin all105 original absolute source
inputs before/after, since the runner cannot snapshot the foundation assets in
its normal source role. Its code snapshot can contain runner/utility/test source.
The test checks execution utility equality against the selected source-root bytes.
This is an explicit read-only-input design, not a wholly snapshotted/hermetic test.
No execution has occurred as part of this review.

## Exact proposed selection review

Read `experiments/source-bundle-controls01-selection.json`, SHA-256
`c677d04213e6699f705da6d7bde9dc0eab3d458762b06d6cbd54c79475ea1d18`.
It selects the final test/utility pins below, original finite runner
`44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651`,
five code/doc snapshots, and108 external pins: the complete105 payload selection
plus Python executable/two DLLs. A read-only JSON/static-table comparison found
exactly105 expected payload pins and no mismatch or additional external input
beyond those three runtime files. It did not execute the utility or tests.

The structured argv selects the snapshot test/utility, canonical read-only source
root and fresh runner-owned suite directory. Limits are90 wall seconds,
45 inclusive Job CPU seconds,512 MiB,4 active processes, and1 MiB each for outer
stdout/stderr. The existing runner checks those external pins before and after
the finite operation. The suite's internal original60-second wall cap further
narrows its one public child. SOURCE GO applies to this proposed selection;
only root can launch it, once, with no automatic renewal.

## Source pins read

| File | SHA-256 |
|---|---|
| bundle.py | `963b8248120458f1c2931b791ccb4cd0d723def40d1e540e3305c358963dac97` |
| MANIFEST-PLAN.md | `ad1d083009b92b7f105db25637636a1b0f01031f04689d13930dd9747834ba10` |
| README.md | `0db6fcc2b01d304e1e91d2ee1f4cb54e83af4b688247a88ccf644c0c53ec4892` |
| LICENSE-STATUS.md | `8d9dac0b66291f274c493aef5fa201ca99b64f79bbfd7ab524ee49e7dd384f3a` |
| Final test_bundle.py | `c322d38cc0e483368612223ab3372106f650c3a1382fbc5d94a3d75c22e0f7a1` |
