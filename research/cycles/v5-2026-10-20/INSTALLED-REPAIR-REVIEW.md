# Installed mathematical-loop repair: independent review

Reviewer: `core_release`. Canonical project root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Scope and current disposition

This is the new review for `INSTALLED-REPAIR-SELECTION.md`. The predecessor
`DISTRIBUTION-REVIEW.md` and `CONTRIBUTOR-REVIEW.md`, the failed installed
operations, and the used installation remain unchanged. This reviewer has
performed source inspection only: no execution, proof, broad test campaign,
installation rehash, budget increase or retry.

The selected boundaries are:

- Root's `software/v5/distribution_complete/distribution.py`.
- The source-derived Lean Init private-import closure selector and its small
  structural controls, owned by `core_growth`.
- A separately selected synchronous runtime-pin deduplication successor, owned
  by `core_search`, scoped to `MixedImportSession._live`.

Current disposition: **source review permits narrow controls, not runtime or
release acceptance**. No source blocker has been found in the distribution
projection/support-map, retained-source selector, or scoped pin-phase
implementation. Final control source/map review and actual results remain
separate gates.

## Why these are consequential repairs

The installed reader completed genuine I/native input admission but exceeded
the 30-second aggregate-controller lifetime limit during semantic import. The
contributor completed input admission and reached authoring, then failed to
load `Init.olean.server` from the relocated runtime. Its native author child
consumed only 0.59375 CPU seconds. Neither saved failure indicates inadequate
RAM. An unchanged retry or merely adding the first missing file would not
resolve the source-level defects.

## Versioned base projection

The distribution successor changes input and release schemas to V2 and names
the projection `mathematical-client-v1`. It retains the unchanged, hash-fixed
base manifest as a catalogue. Its exact installed base payload map is:

1. Every manifest entry under `receiver/runtime/python/`.
2. `operator/commons.py`.
3. `receiver/helpers/domains.py`.
4. `receiver/helpers/run_stage.py`.

This matches the actual consumer boundary:

- `client.launch` loads exactly those three helpers and checks the selected
  interpreter and Python DLL.
- `client.boot.verify_runtime` derives the same Python subtree from the fixed
  manifest, checks its exact census, and pins every runtime file and helper.
- Receipt admission and production load the same three supervisor helpers.
- Preparation pins interpreter/runtime roles against that same retained
  manifest. The successor accepts those roles only when they belong to the
  exact projection.

`verify_release` compares the installed base payload map to the projection,
not to the full historical package. It does not delete or reinterpret the
predecessor installation. The new README explicitly excludes historical v4
and Node commands; optional location requires its own separately adopted
runtime. This is a precise new mathematical-client installation contract, not
a claim that the old full-package contract still holds.

## Separate complete Lean support map

The successor adds an owner-adopted `LEAN_4_34_INIT_PRIVATE_V1` support graph
and file map, separate from the worker's bounded minimum runtime pins.

`support_layout` checks the following finite structural properties:

- Between 1 and 4,096 well-formed Init module names, with an `Init` root.
- Each import edge references a listed module; duplicate imports are refused.
- At most 256 imports per module and 32,768 total edges.
- All and only the listed modules are reachable from `Init`.
- Exactly five selected loader artifacts per listed module:
  `.olean`, `.olean.server`, `.olean.private`, `.ir.sig`, and `.ir`.

Build checks each source artifact's canonical location under the adopted
Lean root and exact size/hash. A support artifact overlapping a minimum
runtime pin is accepted only with identical source path, size and digest.
The release contains exactly the union of the minimum runtime files and
support files under `assets/lean/`.

The existing streamed copy, target readback, full final file census and
verification remain. Because the support lives outside `base/`, ordinary
launch checks every selected support file's bytes, not just the short worker
pin list. The original wrapper start clock remains in force; this additional
launch work is not free or given a renewed allowance.

The graph is owner-adopted source-extraction evidence. These structural
checks do **not** derive imports from arbitrary binary artifacts, establish
source/binary compiler correspondence, or prove Lean/kernel soundness.
They also do not by themselves establish that the source parser recognizes
the retained release's complete import syntax; that is a separate review.

## Trust and authority remain unchanged

The worker and native mathematical admission rules are unchanged. Authoring
output remains untrusted until actual output admission. Correct compilation,
file equality, or a complete support map is not mathematical acceptance.

The installation must remain stable and owner-controlled during the
operation. Source pin checks and Windows resource Jobs do not create a
hostile-code or concurrent-hostile-filesystem sandbox. No independently
hosted operation, growth benefit, aggregate-certificate economics or full-v5
public readiness follows from this repair.

## Independently inspected loader boundary

The installed preparation template selects
`software/runtime/lean-4.34.0-windows`. Direct inspection of that retained
tree, rather than a repeated closure traversal, confirms:

- `AuthorLean.lean` calls `Lean.importModules` for `Init` with `loadExts :=
  true`, without overriding the default private import level.
- `readModuleDataPartsOfMod` in `Lean/Environment.lean` reads the main
  `.olean` and, when its data marks it as a module, reads both the server and
  private parts. It does not stop after the first `.olean`.
- `readIRPartsOfMod` tests for `.ir.sig` and, when it exists, reads both the
  signature and `.ir` body.
- `Lean/Parser/Module.lean` consumes the header in the reported order:
  optional `module`, optional `prelude`, then repeated optional
  `public`/`meta`, `import`, optional `all`, and the module identifier.

Including every import edge irrespective of public/private/meta flags and
all five file classes is therefore a conservative closure for this retained
private-Init import, conditional on the explicitly retained source/binary
toolchain correspondence. The author's 649-module/3,245-artifact census has
not been independently rerun and is not treated as runtime evidence here.

## Selection adapter review

`Select-InstalledRepair.ps1` constructs selections but does not run them.
It pins the exact prior controls basis and its unchanged runtime pins,
retains the known bounded runner, uses fresh selection/run paths, and
retains 20 CPU seconds/60 wall seconds/128 MiB for controls and
60 CPU seconds/180 wall seconds/128 MiB for a later file-only build.
The build input binds the reviewed distribution source digest.

The helper selector and three runtime call-site hashes are generated from
their current files rather than supplied as expected command arguments.
Root must therefore review the resulting exact source map against this
source review before launching, as already required by the selection plan.
No generated selection or runtime outcome existed at this review stage.

The later `select_installed_successor.py` stages fresh requests only after it
checks the exact V2 release, selected input digest, SDK map and installed
entry digest. Its two bases are the exact failed request hashes. Recursive
relocation changes only strings prefixed by the old allocation root; limits,
mathematics and caller sources otherwise remain identical. It copies only
the few hash-pinned caller inputs, requires fresh data/control/workspace/run
targets and prints the launch arguments without executing them. Root must
still adopt the actual new request digests before any calls.

## Retained-source selector

`select_inputs.py` imports only the exact hash-adopted pure builder utility,
not the mathematical SDK. It hashes the retained 102-entry SDK input map,
checks the fixed predecessor input and template, and permits exactly four
named runtime successor mappings: three replacements and the new pin-phase
helper. Other SDK rows remain unchanged.

The source lexer skips whitespace, line comments and nested block comments,
then parses the restricted explicit `module`/`prelude` header and ordered
public/meta/import/all syntax. Every import is an ASCII Init-family name;
public+all is refused. All flags and repeated edges are retained in a
fingerprint that includes each source byte count and digest. The exact
adopted fingerprint must equal
`ecbece96120350a2c14df2b519c6500b82c607a4c17d31c0157ac370dde4bbcd`
before deduplicated graph edges are used. This exact retained-corpus binding
is important: the lexer is not a standalone parser for arbitrary future Lean
syntax. It stops at the first non-import command, and unusual unknown syntax
would be rejected by the fixed source fingerprint rather than necessarily by
the isolated lexer.

The selector hashes every required artifact, checks exact graph/file
closure, checks the fixed retained loader source, and writes fresh input and
source-closure sidecar files with readback. It does not compile, prove, copy a
release or launch an installed operation. Source/binary correspondence
remains explicit. The raw-source inventory is currently audit-sidecar
evidence; the release directly commits the graph and artifact map, not that
inventory. This distinction must not be described as a release-embedded
source-inventory guarantee.

## Synchronous pin-phase assurance

Exact diffs show only the intended three call-site successors and helper:

- `ReceiptVerifier._check_install` retains its active checks and fresh
  manifest-byte read, replaces only repeated installation-pin comparisons,
  and requires an exact helper pin and actual loaded helper origin.
- `MixedDeltaVerifier._check` retains origin/symbol/profile/lifetime and
  owner-control-byte checks. Only the installation-pin comparison uses the
  helper; its required source origins and symbol checks include the helper.
- Only `MixedImportSession._live` opens a phase. Its original validation
  body moves intact to `_live_phase`, with helper origin/symbol inclusion.

The phase caches only a successful exact `(bytes, digest)` tuple for an
already canonical absolute path and the identical checker function.
Expected-pin or checker conflicts fail. Failed checks are not cached.
Each access performs activity checks before and after, and successful exit
performs a fresh check of every recorded pin with activity checks between
them. `finally` discards the context state and restores any independent
outer phase. Exceptions cannot produce a successful session validation.
Repeated closing through the moved body and wrapper is idempotent.

Independent inspection of the selected call graph—not merely the AST
control—confirms that `_snapshot` calls current live owners'
describe/members/export methods, without native execution, await, network
I/O or user callback. Authority and control data are not memoized. Source
pin checks outside the phase retain the original ordinary comparison.

Under the stable owner-controlled runtime/filesystem assumption, identical
intermediate hashes add no new stable-state fact. A common pin checked
seventeen times in the identified path is instead checked at first use and
successful exit. A pin used once gains an extra final check; this is not a
universal twofold speedup or a measured whole-operation speedup. Transient
hostile write-and-restore events between samples remain outside the trust
model.

The eleven inert controls cover the count reduction, fresh later phases and
ordinary calls, final mutation, nested scope isolation, body/active failure,
conflicting expected pins/checkers, noncaching of failures, immutable
expected tuples and parsed integration seams. They import no mathematical
owners and invoke no native tool. Their source supports one finite control
run; it does not establish installed operability by itself.

Reviewed runtime sources, independently hashed:

| Source under `software/v5/runtime_efficient/` | SHA-256 |
|---|---|
| `admission/pin_phase.py` | `4b302fc472ced49a7681deb019c20a92674353d9adf109949cba7d3034b0deca` |
| `admission/verifier.py` | `00dc31632a3f8950a71d747874d0bc218284a42b856a1ebd0d8c2ca2a527ba7a` |
| `mixed_claims/receiver.py` | `aa591a1829deff82576ba30af484ab560ee04900200fd79ac93c19a9c2c7bf7f` |
| `mixed_claims/imports_atomic.py` | `2b80a02fb36e6332028595d0e4eea0a528a7dd087ec2cd1ade0b762db3514a49` |
| `test_pin_phase.py` | `ff8fede258473856cb2a43fd625f5c374ef44a04d8a891774d2a470add3106ea` |

Reviewed distribution builder SHA-256:
`8cf3b4dfa448481a9facb0cb0ae892ad07305c6fd1d75bbdcafac149e575ac4f`.

## Complete-support controls: source correction before execution

The seven small controls cover restricted header parsing and exact source
fingerprinting, missing/extra support files and graph edges, role overlap,
exact base projection, pin dispatch for every support file on each launch,
and the exact four SDK overrides. The I/O mocks are limited to pure
projection/dispatch/override tests; they do not claim to exercise an actual
Lean loader or copied installation.

Root caught a test-fixture defect before execution: the missing-sidecar
negative case addressed `Init.Small.olean.server` whereas the support
generator creates `Init/Small.olean.server`. The reviewer's initial source
clearance missed this typo. The author corrected that single key, and the
reviewer checked the corrected key and remaining fixture paths. No test run
was wasted and no failure evidence was rewritten.

The old unexecuted test hash `193f033e...` is superseded. Reviewed final
test SHA-256 is
`5852436bfde11cb4f7737dfde4209e68a7acb52ffd0e47c1ebf7f3abc1982c7a`;
selector SHA-256 is
`7c836fc33fa8af75a60e94241495dbd45a06cec5a81dde5c6aa441666688ed25`.

## Actual pin-phase controls: PASS

Root ran the eleven controls once in
`experiments/v5-local-checks/installed-pin-phase-controls-01`.
Independent saved-output review confirms:

- Exact selection SHA-256
  `6464890361e8116ce2e6830b709819eb47591418237e9afe2d1d745cacf91c78`.
- All six original/snapshot source pairs match the exact selected hashes.
- All eleven named stderr tests passed; `controls.json` reports 11 tests,
  zero errors, zero failures and the reviewed source map.
- The seventeen inert common-pin requests caused two checker invocations,
  first use and successful final sweep.
- Child exit 0, no forced termination, direct child reaped, Job closed,
  zero final active processes, no cleanup errors.
- Known CPU 0.625 seconds = 0.359375 Job + 0.265625 wrapper;
  wall 0.778705 seconds; peak Job private commit 23,941,120 bytes.
- No mathematical owner import, native call or proof production.

Result SHA-256:
`48401574c13eb2e04386138021d0ee09ec383a953c2f0e7490791b76be2862c7`.
Controls SHA-256:
`638e373e1327aac27c54789f493beda9acc26865eb13608ea154fa4234af2be2`.

This adopts only the selected inert pin-phase mechanism and parsed seams.
It is not installed reader success, a measured whole-operation speedup, or
full-v5 acceptance. The used runtime sources, test, selection and evidence
are now frozen; do not repeat these passing controls.

## Actual complete-support controls: PASS

Root ran the seven controls once in
`experiments/v5-local-checks/installed-complete-controls-01`.
Independent saved-output review confirms:

- Exact selection SHA-256
  `4da48bf2a2b4ad14c9c02eb7aeff2a35ef5350a7259d6704e0d5eb6b0507365c`.
- All four original/snapshot source pairs match the selected digests,
  including the corrected `5852436b...` test.
- All seven named stderr tests passed; `controls.json` reports 7 tests,
  zero errors and zero failures with the reviewed source map.
- Child exit 0, no forced termination, direct child reaped, Job closed,
  zero final active processes and no cleanup errors.
- Known CPU 1.140625 seconds = 0.765625 Job + 0.375 wrapper;
  wall 1.2512865 seconds; peak Job private commit 25,657,344 bytes.
- No SDK import, native call or proof production. The selected mocks are
  explicitly reported and do not constitute a Lean-loader experiment.

Result SHA-256:
`fbc4cc3983dc47ed43c48921d6a02bf4ffea4f382adb555578af20adfe7a461a`.
Controls SHA-256:
`b6c4f181d3fe744313edefa25e2842d099792ac72c14243dde3486e4bf4622fc`.

The distribution builder, selector and complete-support test are now
used/frozen. No repeated controls or unchanged installed retries are
authorized by this pass. The two changed-boundary suites together consumed
1.765625 known CPU seconds; an installed successor and actual mathematical
loop remain separate evidence obligations.

## Pending checks

- Review the new selected input/source-closure record and a separately
  selected file-only build when root provides their exact identities.
- Record build and installed outcomes only after root selects them and the
  saved outputs exist. No repaired-install acceptance follows from these
  source and pure-control passes.
