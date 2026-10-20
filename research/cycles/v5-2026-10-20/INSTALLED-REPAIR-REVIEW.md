# Installed mathematical-loop repair: independent review

Reviewer: `core_release`. Canonical project root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Scope and current disposition

This is the new review for `INSTALLED-REPAIR-SELECTION.md`. The predecessor
`DISTRIBUTION-REVIEW.md` and `CONTRIBUTOR-REVIEW.md`, the failed installed
operations, and the predecessor installation remain unchanged. This reviewer
performed source and saved-output inspection, one new-installation hash/census
audit, and read-only inspection of the closed publication databases. The
reviewer launched no mathematical workflow, test, build, proof, budget
increase or retry, and did not rehash a predecessor installation.

The selected boundaries are:

- Root's `software/v5/distribution_complete/distribution.py`.
- The source-derived Lean Init private-import closure selector and its small
  structural controls, owned by `core_growth`.
- A separately selected synchronous runtime-pin deduplication successor, owned
  by `core_search`, scoped to `MixedImportSession._live`.

Final disposition: **PASS for the exact repaired installation and both
selected installed workflows under unchanged limits; not full-v5 release
acceptance**. The sections below preserve the progression from source review
through narrow controls, exact build adoption and actual mathematical use.

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

## Generated input03 and prospective build: PASS for selection

Root generated the new inputs without compiling, proving or building.
The reviewer independently hashed the four small records:

| Record | SHA-256 |
|---|---|
| `distribution-03-input.json` (1,278,297 bytes) | `d71ab60ff1be199e86278fa10fe9a84a6161b822343ad90a35594d0e98a40042` |
| `distribution-03-source-closure.json` | `e42072880912909f4863cc5d7d310c03dc235bbcec992c5d262f872d5dc32d01` |
| `distribution-03-sdk-overrides.json` | `743b1870093dcd24a5dd488a5f6085d3cf3a8e9d6066b09a36ffcff31f0312b3` |
| `distribution-build-03-selection.json` | `6153ba4c5a63cd612445693877192f59d3332d88bd585297696627b82e16623d` |

Compact parsed-record comparison with input02 confirms:

- Base root, base manifest, preparation template, all six external assets,
  aggregate image and the six minimum Lean runtime pins are unchanged.
- Of the old 102 SDK rows, exactly three change to the reviewed successors;
  the other 99 remain unchanged. The exact reviewed `admission/pin_phase.py`
  is the only added row, yielding 103 SDK sources. All four override paths,
  byte lengths and digests agree with the explicit override record.
- The new support graph has 649 reachable Init nodes and no absent edge
  target. Its exact 3,245 file names are the five artifact classes per node.
  Every graph row agrees with the sidecar's header imports after
  flag-independent deduplication.
- The sidecar binds the exact new input and reviewed selector; its retained
  source-graph fingerprint matches `ecbece96...`.
- The selected base projection contains 587 payloads/30,536,285 bytes.
  The complete support map totals 389,437,304 bytes.

The build selection snapshots only the reviewed builder and retained bounded
runner, pins input03, targets the fresh
`product-local/v5-distribution-03/Mathematical Commons v5` directory, and
retains 60 CPU seconds/180 wall seconds/128 MiB/two processes. The target
was absent at review. No independent build was launched.

This review deliberately did not rehash all 3,245 retained support inputs:
the selector already pinned them and the actual builder must verify them
while copying. This is prospective map/adoption clearance only, not evidence
that an installation exists or that the authoring path works.

## Actual build03: PASS for exact installation

Root executed the selected file-only build once. The reviewer inspected its
terminal report, exact command and stdout, verified both original/snapshot
source pairs, and independently checked the new installation:

`product-local/v5-distribution-03/Mathematical Commons v5`.

The release manifest SHA-256 is
`3b7a8f8f0d6379f7df0e33c50f08e8118face909f6b878b40af3a28c187cec31`.
Its exact V2 schema, base role and build-input digest agree with the selected
input03. The actual map agrees with:

- All 587 base-projection payloads, plus the unchanged fixed manifest.
- All 103 selected SDK sources and their exact installed keys.
- All six unchanged external asset roles.
- All 3,245 selected Lean support artifacts and the identical support graph.
- Six minimum Lean worker pins and 82 preparation source pins.

The reviewer streamed/hash-checked each of the 3,951 installed payloads
**once**, totaling 712,019,419 bytes, with zero size/hash failures. The
independent census found exactly 3,952 files including the release manifest,
181 descendant directories and no reparse entries. No predecessor package
or retained support tree was rehashed.

The build child exited 0 with no forced termination. Its direct child was
reaped, the Job closed, final active processes were zero, and cleanup errors
were empty. Known CPU was 14.015625 seconds = 13.640625 Job + 0.375 wrapper;
wall was 60.9143643 seconds; peak Job private commit was 41,078,784 bytes.
All are within the original 60 CPU/180 wall/128 MiB selection. The nested
supervision CPU counter is included in wrapper accounting, not added again.

Result SHA-256:
`4c4f90ba8c0c1671d4cd2690f3ad04b9a0e788e652399065bce0afe934d8a571`.

This accepts the exact directory installation only. It does not claim that
the installed reader or contributor succeeded. The source-fixed failures
still require separately selected fresh ordinary calls under their unchanged
limits; no old failed call or install is overwritten.

## Fresh installed requests: PASS for selection

Root staged the two requests beneath the new distribution03 allocation:

| Call | Exact request SHA-256 |
|---|---|
| Reader, `controls/relocated-remote-01-request.json` | `9e0f1e7e3dc69e6dfd168e089e12de4213cac6e57563dd6f9275dad74b2a068e` |
| Contributor, `contributor-controls/installed-contribution-01-request.json` | `4bec7a144f38bc6834abf059a8952e2cc84c59ea24c50633a2eff40d1e0ade02` |

Independent complete parsed-request comparison confirms exact equality to
the respective old request after replacing only the old allocation-path
prefix with the new one. Thus mathematics, packet choice, strategies, inner
grants, outer limits and refusal behavior are unchanged.

All five staged caller-input pins were independently checked: reader owner
and packet; contributor owner, packet and Lean source. All matched. Both
run directories, request-output directories and mathematical workspaces
were absent at review.

The reader retains 45 CPU seconds/120 wall seconds/512 MiB, and the
contributor retains 150 CPU seconds/240 wall seconds/1,024 MiB, with four
processes per outer Job. These are fresh source-repaired operations, not
renewed allocations for failed calls. Root alone selects and launches them;
the reviewer launched neither.

## Actual installed reader: PASS

The fresh reader's generated plan SHA-256 is
`1d583332afc9ba01610196ec59cbcf301348cc99cc8917f6070d5380358a80d7`.
Its operation ID is
`7e8168063b597579bc571d49b12a33fd5ec70eda8b89597a524580e0295da8cb`.
The wrapper completed, the reader returned `COMPLETED`/`READY`, and the
service returned `PASS`.

Independent saved-output checks confirm:

- All 104 original/snapshot source pairs match the plan. The successful
  final boot report binds that plan, reports `OWNER_EXITED_ZERO`, and
  includes the adopted `admission.pin_phase` import origin. All reported
  source origins belong to the selected map.
- The actual I verifier reports `REAL_MODULE_RECEIPT_VERIFIED`,
  `fully_resolved: true`, for the exact 223,594-byte retained receipt. Its
  journal equals the native delta's sole parent journal. The native
  conclusion equals the saved mixed-admission journal and returned
  `b4295706...` input module. The packet hash is exact.
- The native child is not itself unconditional admission: its conditional
  result is combined with the current live I verification by the unchanged
  mixed-admission owner. No saved report substitutes for that owner.
- The returned semantic context has 12 groups, 15 declarations, no demands,
  and zero frontend ancestral theorem-proof bytes. This field does not
  assert zero certificate, witness or fixed-foundation cost.
- The local HTTP service handled five requests, 561,628 reply bytes,
  1,189 request-body bytes and 1,141 header bytes, with no failure/refusal.
  Its HTTP/workspace cleanup and the reader/client/workspace cleanup closed
  without errors.

The reader's controller used 14.890625 CPU seconds within its unchanged
30-second grant. Whole known cost was 19.609375 CPU seconds =
16.90625 Job + 2.703125 wrapper; wall 35.2549433 seconds; peak Job private
commit 113,831,936 bytes. Both nested verifier/native processes and the
outer Job exited successfully, nonforced, reaped and closed with zero final
active processes. No A verification, authoring or publication occurred.

This is an installed, source-repaired success under the original budgets.
The change includes the reviewed count reduction; these separate runs do
not isolate the full observed timing difference to one cause. It is local
direct-contact discovery with declared coverage, not public networking or
global completeness.

## Actual installed contributor: PASS

The fresh contributor's generated plan SHA-256 is
`3659317a3ef97e0a121e3c3eb47467a019369a5c0179b5b07588564a4dab4c8d`.
Its operation ID is
`e045a52cdcb18dec0bcea6ae9a79a899565f2024522b099b6c067e1e4562bf5a`.
The wrapper completed and the example returned
`COMPLETED`/`CONTRIBUTED`, not merely exit zero.

### Source and actual admission chain

All 104 original/snapshot source pairs match the plan; final boot succeeds
with selected import origins, including the new helper. The actual worker
configuration points to installed `assets/frontend/AuthorLean.exe` and
installed `assets/lean`, with the unchanged six minimum runtime pins. The
worker exports successfully with no timeout; its export hash matches the
actual saved 6,667-byte export. The worker's result remains explicitly
`PASS_NATIVE_EXPORT_ONLY`, not mathematical admission.

The export is the one local theorem `ClientV5.project_summary`, with three
universe parameters. Independent traversal of its exported proof expression
finds the exact external constant
`DMKN.Mod.b42957064314b6667bf05cd3eec27ce39b925491c756a69f23a739d39ebb9f94.ClientV5.fusion`.
Thus the output uses the intended imported method, rather than just carrying
an unused dependency label.

The current I verification and input native journal chain agree exactly.
For output admission, native delta 0 rechecks the input extension and native
delta 1 has exactly the current I journal and that extension journal as
parents. Each native output's input hash/length matches its actual saved
witness, and each command uses the installed native executable. The final
native journal equals both the fresh mixed-admission result and the
contributor's checked-output journal.

The resulting module is
`6ea8fa600c3ec9eb64992466c2c897d6455b53a6d0461a2b655fcb3f2c86d55f`.
Its 658,554-byte packet hash is
`6998ba92d064c8ce790192a434655d4b99bf0e7018f422ec24be757de55db2eb`,
identical in preparation, fresh output admission, the final report, and
published local custody.

### Persistent publication, independently inspected

Read-only immutable SQLite inspection was performed only after confirming
no corresponding WAL files remained. It did not open the SDK workspace or
mutate its state.

- The operation row is `CLOSED`.
- Publication
  `5960b490e88eebfbd6f34989897952a85aa87c6efa9996782791d572e9ad0fe9`
  records the exact report intent and outcome, with
  `phase: LOCALLY_PUBLISHED`.
- The custody packet exists with the exact bytes, digest and output module,
  and an offer exists for the selected wire profile.
- The output module and its single local group/name exist in module storage.
- The discovery database contains the indexed locator for
  `ClientV5.project_summary` in that exact module. Its latest snapshot is
  the reported
  `944736d1c042a0ca6aa0a5ef1e2258791e29c9fc46db2e285acfc0948638be59`,
  and the snapshot row exists.

The client records two admission submissions, one author call and one
publication attempt. There is one actual I verification, one input native
check and two output native checks, not a new aggregate proof campaign.
The publication report's 13 groups includes reused stored groups; it is
not thirteen newly discovered mathematical results. Remote placement is
unconfirmed, all-future-body coverage is false and cross-database atomicity
is not claimed.

### Costs and closure

Controller cost was 30.34375 CPU seconds within its unchanged 90-second
grant. Whole known CPU was 36.96875 seconds = 34.15625 Job + 2.8125 wrapper;
wall 40.4323397 seconds; peak Job private commit 532,041,728 bytes.
The author worker consumed 1.84375 Job CPU seconds with clean closure.
Preparation's 29.046875 controller lifetime and nested worker costs are
included/overlapping accounting, not amounts to add to whole-operation CPU.

All inspected actual I/native/author children and the outer Job exited
successfully, nonforced, reaped and closed with zero final active processes
and no cleanup errors. Preparation, client and workspace closed without
failure. Both installed operations therefore succeeded without enlarging
their original allocations or modifying predecessor evidence.

## Actual outcome record hashes

Paths are relative to `product-local/v5-distribution-03/`.

| Record | SHA-256 |
|---|---|
| Reader outer `RESULT.json` | `df36e8ff0f583627d9cd051537646f91bf4be55d0d70d9d85ef2d58e1e3b9575` |
| Reader `BOOT-RESULT.json` | `2cc66150b2687e7c052cd7d76b24bbe6a70122e25becab25e1ecd519559793df` |
| Reader `work/remote-check-result.json` | `f62553d72fd107949159856f2bf765239d8ccfb712ddce00d053ea836838bd3e` |
| Reader `work/reader/remote-reader-result.json` | `13e7be7496f8fc7a2c841781d3e2dffe99ddba2fcc638a50423ab8a2c9c8fdee` |
| Reader `work/service/service-result.json` | `83990d53e93b0de0ffe215e644bcc43cf0ac55cd6085c13ae6a469fedcba3909` |
| Contributor outer `RESULT.json` | `45972f43d709fdd709d7d5de393e014ab6cb7e9d8e4db83b8672ff95a791d990` |
| Contributor `BOOT-RESULT.json` | `bf22e3214779d5172fd6d6b79eb04615c4850b5b79def23a7596c01845076b36` |
| Contributor `work/contribution-result.json` | `889cfda718678395acf672b43151b1128ec041c859f967c094cbfda675c3cd50` |
| Contributor operation `preparation/author-1/worker-result.json` | `ac77b2375154c9ac8b386e13844c1ad7d641610ae0fa449ce223091d87a27744` |

## Final disposition for this repair

**PASS: exact installation, installed direct-contact reader and installed
local-input contribution/publication under unchanged budgets.**

This closes the two specific installed failures. The retained theorem was
already produced in earlier source-mode work; replaying it through the
installed path demonstrates operability, not newly measured useful growth.
There is no independently hosted pilot, public-deployment acceptance,
complete semantic discovery, aggregate-certification economics result or
completed-v5 claim here. All used sources, requests, installation and
outcomes remain frozen; no repetition is selected.
