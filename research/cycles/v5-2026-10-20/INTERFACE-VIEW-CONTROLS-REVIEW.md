# Interface-view controls: independent source review

2026-10-20. **PASS for the specified native-free control selection**, not a
runtime result. Reviewer did not author the test or selector. No Python import,
test, compiler, prover, native executable or Git mutation was run in this review.

Reviewed exact files:

- `software/v5/interface_views/test_interface.py`:
  `fa98cea5aad54cdf671530d44b5db404d2dc78c509be2c040ba8f9e240341f33`.
- `research/cycles/v5-2026-10-20/Select-InterfaceView.ps1`:
  `a4560b0b9bef06994f5ed77e15a9148030d370b10b235837fd0168f69518e018`.
- Frozen baseline `declaration-continuation-controls-01-selection.json`:
  `eee5ea43dc626df9754a9e695a24b51334e45ccf5066ab67b65b8540e22f1cda`.

## Dependency and execution boundary

The 100-source baseline plus seven interface overlays, this test, and the three
retained `runtime_efficient` files (`admission/pin_phase.py`,
`admission/verifier.py`, `mixed_claims/receiver.py`) gives 111 sources. The
baseline already contains `client/workspace_validated.py` and
`transport/search_validation.py`; no additional versions are necessary.
The inherited portable location modules and semantic staging dependencies are
present. Overlay import order installs pin phase/verifier/receiver before the
new session, projection, authoring, staging, client and reader classes. The
validated facade subsequently imports the already selected staged facade.

The test does not import any predecessor test suite. Its new top-level work
loads source modules and constructs inert data; it does not construct a real
owner, dial, create a native process or invoke a prover. During the suite,
`subprocess.Popen` and both asyncio subprocess launch functions are replaced
with rejecting sentinels. The exact ten named methods are run once; there are
no skips or optional fallback tests. Output uses exclusive creation.

The selector preserves the exact old source/runtime pins, requires reviewed
hashes for new canonical Python source paths, refuses predecessor rewrites
and existing output/selection names, and creates only a fresh plan. The
planned limits are 30 CPU seconds, 60 wall seconds, 256 MiB, two processes and
1 MiB each stdout/stderr. Actual execution remains root's separate decision.

## Ten controls inspected

1. Missing ordinary definition bodies permit a bounded selected interface
   despite synthetic hidden body chains of lengths 1, 32 and 256; eager mode
   still requests a body.
2. Missing type dependencies and dependencies of supplied bodies remain
   demands; a selected module cannot substitute for its missing declaration.
3. Projection changes only the copied missing definition's kind/metadata;
   original bytes and present bodies remain unchanged, including eager mode.
4. Unsupported mode values and mismatched outer/packet bindings refuse.
5. The real native-row emitter retains `moduleImportDef`, exact body hash and
   reduction hint, not an axiom or opaque native import.
6. The real source decoder rejects a newly introduced local axiom.
7. Mode distinguishes sealed bindings; default eager reproduces the original
   binding formula; foreign views and rematerializing sealed views refuse.
8. A NEED interface selection remains valid and continues to READY under the
   same mode; cross-mode continuation and mode mutation refuse.
9. The actual source-operation methods separate projected request descriptors
   from original final-row and parent-opening descriptors; stale export binding
   refuses. Onward authority is explicitly stubbed, not asserted.
10. Actual public reader/staged-preview/direct-import method bodies propagate
    the mode through inert grant/custody/issuer shells; a mismatched preview
    mode refuses.

## Scope limits

The fixture bypasses owner construction and replaces foundation decoding with
an explicitly inert view. It checks structural behavior, exact bindings and
source-operation dataflow, **not** genuine mathematical admission, certificate
validity, native missing-body execution or installed source-pin enforcement.
The chain control does not fetch/replay a full eager chain or measure wall-time
growth; the asymptotic conclusion relies on the separate source argument.
Recursor eagerness is preserved by source inspection, not a dedicated new
recursor execution in this ten-test selection. Genuine Lean/native success and
failure still require the separately reviewed changed-boundary integration.
