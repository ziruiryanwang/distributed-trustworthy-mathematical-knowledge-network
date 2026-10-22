# Typed renewal controls: independent source review

Disposition: **PASS_SOURCE_REVIEW_FOR_ROOT_SELECTION**. This is source review,
not an executed-control result, actual receipt acceptance or v5 release evidence.
The reviewer is the renewal-adapter author, independent of the control author;
this does not replace the separate review of the adapter itself.

Reviewed `software/v5/typed_renewal/controls.py` in full: 25,533 bytes,
SHA-256 `94659d28dd92f2a525d29aaca3a8548771c74c34069151542c2da6475d8e3f1c`.
Compared against source `fc5902f778fa37b484a4ab50d0594a1d5a0afe8b91896928bf321cce64dac019`
and owner `2bae25aecfd5935674a540d79580531334179ecce7a1e00ca6171d858fde87ac`.
Read the relevant current-map model implementation; only read-only file/JSON/hash
inspection was performed. No import, syntax check, test, selector or native call
was run in this review.

## What the six controls establish if executed successfully

| Control | Actual exercised boundary | Explicitly absent authority |
|---|---|---|
| Retained semantics and sealing shape | Pinned fixture U/V specifications; real material, packet, membership and preparation algorithms | Receipt bytes and one membership companion are synthetic; no cryptographic verification |
| Seven refusals | Exact fields, missing receipt, wrong U journal/header, terminal-I substitution, changed receipt, wrong V journal | No claim that shape validation detects a cryptographically invalid but well-shaped receipt |
| Fixed source and proof edge | Real conditional model and precise 18-binder `Eq.trans (U ...) hd` AST inspection; wrong edge and binder style refused | Decoder return is explicitly doubled; neither Lean export nor native proof checking occurs |
| Six preparation-return refusals | Missing parent, falsely asserted admission, wrong input hash, omitted selected delta, wrong edge census and wrong height | Producer return is doubled; no producer snapshot or run |
| Owner success sequence | Actual owner control flow and packet checks; exact A-only import/author/admit order and withdrawal ordering | Parameters, authority, filesystem, runtime, client and source-export inspector are expressly inert doubles |
| Ten owner failure points | Domain-create uncertainty, post-create withdrawal attempts, cleanup continuation and no saved V journal before admission | No actual DB/trust-domain mutation, process failure or hostile-input isolation test |

The latest two preparation-return negatives match guards already present in
the reviewed source; the case count is computed from the six selected cases.
The same-occurrence wrong-edge negative changes the final two proof arguments
without relying on occurrence counting. `supply_local_value` records structurally
valid theorem bodies without performing type checking, so it does not silently
replace the intended exact-edge check with a native validation claim.

## Selection and containment checks

- Current map is fixed to the 2,813,950-byte candidate130 input, SHA-256
  `25e7c849e41f394498e21a60cc7800ecffb67b0cee1b3911d7164977ce4f2364`.
  The control snapshots 130 unchanged logical sources plus four renewal files;
  the root-selected runner is the 135th selection source, not an SDK module.
- Retained fixture is fixed to 84,727 bytes and SHA-256
  `019219ca4548dafbdaa814c209a4ec087229091750db3f3cf48fcc155269f40a`.
- Staging verifies ordinary paths and selected hashes before imports; it requires
  isolated, no-site, no-bytecode Windows execution and refuses preimported product
  packages. Writes are new files in the separately selected output only.
- Subprocess, shell, async-subprocess and SQLite entry points are patched to
  refusal during product imports and all controls. These are targeted test
  tripwires, not a security sandbox or a universal prohibition on native APIs.
- Owner doubles disclose their scope in source and report. The fake work path
  must remain nonexistent. Success and fault cases record zero native, proof,
  crypto-verification and real trust-state calls.

No blocking source defect was found in this bounded review. Root still selects
the exact runner, finite limits and fresh output before any execution. A later
successful result would qualify only these six stated control boundaries; the
genuine A receipt and ordinary U-to-V operation remain separate gates.
