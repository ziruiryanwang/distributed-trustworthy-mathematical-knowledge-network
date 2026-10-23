# Ordinary source package: independent outcome audit

2026-10-23. Reviewer `admission_event_audit`. Read-only saved-evidence audit;
no native execution, controller import, state opening, package mutation or Git
operation. The source review is `ORDINARY-PACKAGE-REVIEW.md`. Root owns execution
selection and adoption. All paths below are under the canonical project root.

## Build disposition

`PASS_SELECTED_TWO_LANE_SOURCE_BUILD_AND_ASSEMBLY`.

The fresh source build completed all eight receiver and thirteen authoring
compiles, assembled the unchanged receiver installation and emitted a bound
auxiliary profile. Saved source, lane, compiled output and package maps agree
with actual bytes. Both nested and outer process trees closed cleanly. This
establishes a clean build from the selected source closure and explicit runtime
distributions, not mathematical owner acceptance or completion of v5.

Run: `experiments/v5-local-checks/ordinary-source-package-build-01`.
Selection SHA-256:
`0dcb34cb2604e27f07d4ab9709e1674f609e5294caceaa3e55b74ef92c8667d8`.
The exact reviewed builder/CLI bytes are unchanged. Root launched the fresh
build once; this reviewer did not poll the live operation or rerun it.

| Artifact relative to run | SHA-256 |
|---|---|
| `RESULT.json` | `0bd48fa10b93a7270459059bd9d8779e55f74980ac808260a1f7696833376354` |
| `package/_build/BUILD-RESULT.json` | `f541b45f359458494b307d9026da11c2561aec2e252921ffbc582fe4c3049fc1` |
| `package/_build/SOURCES.json` | `7d54de36bf572f2cd77c19fe98541ad0121bb5e17ffdea25b8a223af4c2d7876` |
| `package/_build/PUBLIC-SOURCE-MAP.json` | `8dc6f8d6c32fa5f2c4239bcf226a495f13a48b9e82a03d551fd4239a2441ae9f` |
| `package/_build/COMPILED-FILES.json` | `41d40735ffe716c4a0324b72c0f364bc9d1baa5ca7fb5edd7f04d1d560d1419f` |
| `package/_build/SUPERVISION.json` | `3360492cc4a304a05f621c91cc7c2e881ebc97d4e0283a624e9af4c4638ee8ef` |
| `package/PROFILE.json` | `881adbf54898e08bf8906614c9cf6b76c1f8aec8428e5a4f26f467719a25b232` |
| `package/installation/INSTALLATION.json` | `32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2` |

New implementation identity:
`fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df`.
This is a new installation, not an old catalog migration.

## Exact source and lane correspondence

Read-only hashing checked all 47 selected snapshot source files, and all 47
builder inputs against both the current selected source and the staged copy.
The counts happen to coincide; the sets differ: selection additionally records
the selector/outer runner, whereas the builder input map includes the two
foundation files. Each builder input is bound by the selection's source map or
explicit foundation pin. The staged input tree has exactly its declared files.

All eight receiver sources match the selected source mapping. In particular
receiver `OrdinaryExport` is the preserved `ecab2be2...` source, not the current
authoring `1d4df681...` source. All thirteen authoring source-map entries match
their original/generated/body hashes. An independent in-memory reconstruction
of the four public header transformations reproduced the generated files and
their exact hashes:

- OriginalExpr: `2064205249945563302b0ef4c0d3562ff1864730ee4644083a3b888433db2fb9`
- OriginalDecl: `6a1adbab4496e351b3c66946c84a34eefc7270c214b684b44e77e10371dc89c8`
- CheckedExtension: `60eba9cf947571f4336dd6e1f89a098b710a50f1e803a79d5691cc6292d2ae5a`
- BootstrapSupport: `ccc6b864aba8e7239401a787930ea208e6d99653225e7565fd8a613b7db9e40c`

The nine other authoring sources are unchanged original bytes. The saved worker
command names the fresh separate receiver and authoring directories. Its stdout
contains exactly the expected 21 module completions in dependency order, each
with exit code zero. Source review establishes the worker's lane-specific
LEAN_PATH; no old experiment helper directory is selected.

The actual receiver object directory contains exactly eight `.olean` files.
The authoring helper directory contains exactly 65 outputs: thirteen modules,
each with `.olean`, `.olean.private`, `.olean.server`, `.ir`, `.ir.sig`. Every
size/hash and both exact file censuses match COMPILED-FILES. This avoids the old
accumulated/shadowed helper-directory support dependency.

## Installation and profile correspondence

The installation manifest names 36 files: 27 copied files totaling 15,688,635
bytes, plus nine external runtime attachments. Every copied/runtime file's
actual size and SHA-256 matches. The installed tree contains exactly the 27
payloads and INSTALLATION.json, with no extra core/native search-path files.
The manifest's eight compiled modules, receiver sources, six core Python files,
foundation and preserved supervisor are the reviewed assembler mapping.

Independently reconstructed domain-separated digests reproduce all five
implementation support commitments and the new implementation ID above.
PROFILE has 82 auxiliary payloads: 65 authoring outputs, six authoring Python
files, eight namespace-support files and three entry points. Every actual pin
matches; authoring/helpers, authoring/py and support have exact declared file
censuses. PROFILE binds the actual installation-manifest hash and contains
package-relative payload locations, not absolute build dependencies. Both the
saved build result and command stdout report these actual profile/manifest IDs.

Named runtime attachment verification is not a proof of the entire externally
provided Python/Lean distribution. This build uses the selected Windows/Python
3.14.6/Lean 4.34.0 support; no portable or hermetic claim follows.

## Complete saved operation cost and closure

| Quantity | Actual |
|---|---:|
| Full outer-wrapper elapsed seconds | 46.80176200019196 |
| Outer supervised tree CPU seconds | 39.859375 |
| Outer wrapper CPU seconds | 1.125 |
| Known inclusive CPU seconds | 40.984375 |
| Peak outer Job private commit bytes | 903,823,360 |
| Inner compile-tree CPU seconds | 36.109375 |
| Inner compile-tree elapsed through cleanup seconds | 38.88397580012679 |
| Builder controller CPU before final marker seconds | 3.578125 |

The compile-tree CPU and builder controller CPU are already within the outer
tree CPU: do not add them again to 40.984375. The outer supervisor's narrower
0.359375-second wrapper submeasure is likewise already within the 1.125-second
full-wrapper measure. The pre-marker builder elapsed value is not the complete
run elapsed value.

Original outer limits were 420 wall seconds, 300 CPU seconds, 2,304 MiB private
commit, six active processes and 1 MiB per log. Builder limits were 360 wall,
260 CPU and 2,048 MiB. The single nested compile tree used the original remainder
(333 wall/257 CPU seconds), not twenty-one renewed allocations. Both reports
record exit zero, reaped direct child, closed Job, zero active and terminated
processes, no termination request, no cleanup errors and empty stderr. The outer
tree counted 46 total process instances; the inner compile tree counted 44.
Total instances are not concurrent-process counts. Logs remain within limits.

## Next boundary and limits

The separately reviewed lifecycle adapter should exercise an exact minimal
relocated payload: PROFILE, selected auxiliary files and selected nonruntime
installation files, without `_build` or source snapshots. One wrong-profile
refusal, fresh init, two-output caller contribution and separate reopen/status
will test that changed launcher/persistence boundary. Its selector and aggregate
outer Job require root selection; no lifecycle success is inferred here.

There was no certificate production, old owner copy, store migration, index
publication or peer operation in this build. No reciprocal-network CLI, broad
library interoperation, useful-growth benefit, global scalability or final-v5
acceptance follows from successful compilation and packaging.

## Relocated lifecycle01: retained failure and accepted basis

Disposition: `PASS_RELOCATED_PROFILE_REFUSAL_AND_NATIVE_INIT;
FAIL_CALLER_CONTRIBUTION_BEFORE_ADMISSION`. The full four-call lifecycle did
**not** pass. The separate status step was never reached. This does not change
the successful build disposition or turn a failed example into a qualification.

Run: `experiments/v5-local-checks/ordinary-package-lifecycle-01`.
Selection SHA-256:
`adf5d883fd81b25e293715276f10de1a58240206d2d13089efd748e648f872c7`.
The minimal package is adjacent `ordinary-package-lifecycle-01-payload`.
All 111 files, totaling 36,577,885 bytes, independently match both the file-only
payload receipt and their original built bytes. The exact payload census has
no `_build` or source-snapshot tree. PROFILE/installation IDs are unchanged.
Selected snapshot sources, saved CLI stdout/stderr hashes and actual native
commands were also checked; authoring selects only the relocated helper path.

| Artifact relative to lifecycle run | SHA-256 |
|---|---|
| `RESULT.json` | `82dc56d157fb793a8936566ab30ea570b7eed6aa6b405bf9b2c3ccf089a4328b` |
| `LIFECYCLE-RESULT.json` | `0750aee435624397351f6089291e95bd6755efea79bf9eb335242797926472d4` |
| `CallerBody.lean` | `1e8c2848f9307ccdc544f2bc5755cebeb22bc24be537a46acd73fd37b4028868` |
| `contribution/FAILURE.json` | `18d7838bd108c8338ce7599468c94393f33795548474442302d895c2be2ba051` |
| `contribution/candidate.json` | `d49c2e19d979ec4835029846afefd98a9f14a57c1e8dd53fae206a085213437b` |

Adjacent `ordinary-package-lifecycle-01.payload.json` receipt SHA-256:
`46466fb45548507a88d14cc216f296d005b71305a7605f975fbfb14b7bfe4b8e`.

### Actual three calls and failure cause

1. Wrong-profile init returned `OWNER_PROFILE_PIN` in SUPPORT with no accepted
   state; the adapter checked that catalog/custody paths still did not exist
   before proceeding. Expected exit one, empty CLI stderr.
2. Fresh relocated init returned CHECKED for 456 basis units/581 names. Its
   successful native process, retained artifact and committed catalog agree.
3. Contribution reached authoring, but Lean exited one: its exported theorem's
   `rfl` proof needed to unfold `applyTwice`, whose definition was not exposed.
   The diagnostic explicitly says exported theorems require definitions needed
   for unfolding to be exposed. The generic helper returned AUTHORING failure,
   with accepted state null, before binding/preflight/admission. Its native
   candidate file exists but is only inert candidate data, not an accepted
   result. File existence must not override the failed authoring process.

The immutable original caller source lacks `@[expose]`. A caller-only corrected
source can be considered in a fresh explicitly selected contribution operation;
no package/checker/source rewrite, new init, catalog copy or unrecorded retry is
warranted by this failure. Root retains all original failure evidence and costs.

### Precontinuation underlying state

Before any continuation, stdlib SQLite was opened solely with
`mode=ro&immutable=1`; no product catalog opener or controller was imported.
Both database hashes were unchanged after those reads. The catalog contains:

- One ACTIVE native-bootstrap basis root:
  `32728b6f5b8d66cce285d7540cc91b900c9b40544fae2e73879daa5f7d3962fd`.
- One operation, COMMITTED:
  `2e98579e2fb7aa683fb35d844468db0da0bc90f7aa99ef8b3befad0b84c6399a`.
- Exactly 581 bindings, no extension root and zero legacy imports.
- Store ID `7becc8b2d689d7240c791c44f22599bb22cee92bf6da097c2a028b535c5a0b5c`,
  semantic/foundation/implementation IDs matching the selected installation.
- The native worker report's basis kind, module name, 456 units, 581 names and
  artifact byte count agree with the retained basis snapshot and root record.
  The exact unique name sets match. Their list orders differ as designed:
  `reserve_basis` sorts catalog bindings by canonical name key, while the native
  report retains basis construction order; raw list-order equality is not the
  contract and was not counted as a product failure.
- Custody has zero objects, zero exports and zero logical bytes. The failed
  contribution did not publish admitted evidence or previews there.

The following exact precontinuation identities distinguish mutable database
state from old immutable evidence. A later selected public contribution may
append to the database; it must not rewrite the original basis record/artifact.

| Retained object | SHA-256 / bytes |
|---|---|
| `catalog/catalog.sqlite` | `ca47cfa31085b468e6ffe22cf5575287806064e696c650bf77e6499d63536348` / 118784 |
| `catalog/ADOPTION.json` | `bd98f4672f608be70a268e1b73db82ead5492fc739f9db73a83ac16a531e4027` / 1160 |
| Basis root-record bytes | `41efe618b521ddcc52cbc4fe4cd226aa6666ff9f93fd774456a3b613cce62d9f` |
| Basis `operations/2e98579e.../chunk.olean` | `40bb6790705c3c5838a3f7eb6d63bb1ebc03aed8208c0c866bafd8dd728e12b7` / 669968 |
| `custody/ordinary.sqlite` | `7591090b583803ce78540a8d5019a3de129563b3a691e54e4ca7d70c64f1dffe` / 16384 |

There is no pending native admission or uncommitted contribution to recover.
Ordinary reuse of this initialized owner is the relevant next boundary; repeating
the already successful basis initialization would add no useful evidence.

### Failure cost and clean closure

Full lifecycle01 elapsed: **30.56886549992487 seconds**. Outer tree CPU:
27.796875; full wrapper CPU: 1.03125; **28.828125 known inclusive CPU seconds**.
The successful basis worker consumed 22.90625 and the failed authoring tree
2.09375 CPU seconds, already included in the outer total. Peak outer Job private
commit was 933,408,768 bytes. The original aggregate allocation was 240 wall /
180 CPU seconds / 2,048 MiB; no allowance was renewed inside this attempt.

Outer, basis and failed-authoring trees all ended with direct child reaped, Job
closed, zero active/terminated processes, no termination request or cleanup
errors. Basis exited zero; authoring and the enclosing validation exited one.
All three CLI stderr files are empty; Lean's diagnostic is in authoring stdout.
The outer 1,487-byte stderr is the expected validation traceback reporting
`VALIDATION_OPERATION_RESULT:contribute`, not clean empty success stderr.

Build plus lifecycle01 consumed 77.37062750011683 elapsed seconds and
69.8125 known inclusive CPU seconds across the two separately selected runs.
This sum excludes read-only audit/selection overhead and is not a throughput
benchmark. The failed contribution remains charged even if a later separately
selected caller correction succeeds.

## Continuation01: corrected caller and persistent reopen

Disposition: `PASS_SELECTED_RELOCATED_CONTRIBUTION_AND_PERSISTENT_REOPEN`.
The separately selected continuation succeeded using the existing initialized
owner and the unchanged minimal package. Combined with the original wrong-pin
refusal and native init, this establishes the selected local package workflow
with one disclosed caller-source correction. Original lifecycle01 remains
FAILED; neither its evidence nor its resource charge has been replaced.

Run: `experiments/v5-local-checks/ordinary-package-lifecycle-continuation-01`.
Selection SHA-256:
`3866e2d67ef6d6ece345a14e129958b2befa6340f859481cf534d9a48c256e73`.

| Artifact relative to continuation run | SHA-256 |
|---|---|
| `RESULT.json` | `3aa59bfbe3e50471f146f625e2661b01bfb2c503d9bdbf6cb9929f785bd7f3a7` |
| `CONTINUATION-RESULT.json` | `81b70c4894fe218dc7daf890c37cf4a51810a7517294d9881a2884b9c90066e7` |
| `CallerExposedBody.lean` | `9e4fc8324f4ff62474c004e995c06908deffdae095f6e0ae2d3c9dca8bd6ffdd` |
| `contribution/RESULT.json` | `edc14a0b309ad4435a105482401fbb7f3d8bf0639dd9c3f2c124ce997c18c967` |
| `contribution/AUTHORING-SUPERVISION.json` | `d0f79c58a9f443f44e861a23e49ac0cecf8a917cb641f1f9a0a93109f52467e2` |
| `contribute.stdout` | `16fb7318562203a64a54cc7dd570d9c5764d2ceebb9635b04e39796fd117c15b` |
| `status.stdout` | `e6892feb331a9654c76fdb5e03b164add12be1b0ed80173a48fd63ae88e7486f` |

### Exact operation and package boundary

Both selected source snapshots and all 126 selected runtime/payload/retained
input pins match actual bytes. The minimal relocated package remains exactly
111 files / 36,577,885 bytes, with the prior PROFILE, manifest and implementation
IDs. There is no added build tree, helper shadow or package-code correction.
The new caller body differs from the original only by inserting `@[expose]`
before `def applyTwice`; all other caller bytes and requested names are retained.

The adapter performs exactly two public commands, `contribute` then `status`.
Their saved commands and stdout match the returned records. Both name the same
original catalog, custody, store ID, package/profile and implementation. The
contribution's explicit parent is the original basis root; its outputs are fresh
under the continuation directory. No init, build, state copy, private adoption
or direct database write is part of this continuation. Both CLI processes exit
zero, with empty stderr. Status requests the exact newly returned context, not
a guessed current/latest root, and invokes no native worker.

### Mathematical and durable-data correspondence

The two new exports are:

| Name under `CommonsPackageExample` | UnitID | ExportID |
|---|---|---|
| `applyTwice` | `25ae588e95228a64196a576aa9c9dd78249c23b0c26189c5671a434b93afa1b3` | `b5054e3c29436f1fe8d175b47df405405f76683d7c1e27531d9e597f2e55ee02` |
| `applyTwice_eq` | `c4639e6e5f70e259ea1611adba8e168aa74dbfb91f98e2512cd465f82705e61e` | `bb47ce4786c4f5c22505952133e5220c0650452fb0006c83a395de131fee1355` |

The polymorphic definition maps `(f,x)` to `f (f x)`; the theorem gives its
definitional equality. Its statement/proof references the exported definition.
This is a small supported owner-authoring example, not a useful-growth benchmark
or a claim of new mathematics.

Actual candidate units exactly equal the units supplied to the successful native
extension worker. Each canonical evidence file contains the corresponding unit;
independent domain-separated hashing reproduces its UnitID and the requested
ExportID. Native output reports exactly those two names and two checked units.
The two saved previews match each exported unit's name, type header and identity.
Saved evidence/preview bytes exactly equal their four custody objects; both
custody export locators resolve to the corresponding unit/name. The root's two
bindings exactly equal the two advertised ExportIDs. No extra target is accepted.

Notably, the candidate file's SHA-256 is the same as in failed01:
`d49c2e19d979ec4835029846afefd98a9f14a57c1e8dd53fae206a085213437b`.
The visibility annotation changes exportability, not the captured declaration
semantics. This does not rehabilitate the failed compiler invocation: only the
new clean authoring event followed by the actual successful admission supplies
this continuation's acceptance. An inert candidate file alone remains no warrant.

### Persistent state and preservation

New local root:
`b5632acbab2d88f5e66436bc9bd7e4a47578ab6f41e35ecb20f9b2e00c0fb334`.
New operation:
`4f02c71545111168d583de97aa2e9079cc9992e8690d097b664cb37d78594c12`.
Its 2,960-byte native snapshot SHA-256 is
`52a5756407d7cd0258abcae3208ad46d3276446589799c26dff25138942965bc`;
its root-record SHA-256 is
`59e362c8c047bc43c5e5944910afc6ccb4b2756b5e2d7968586f105b5b844100`.

Read-only immutable SQLite inspection establishes exactly two roots and two
COMMITTED operations, zero imports, and no pending operation. The new root's
parent and parent module are precisely the original basis. Its input UnitIDs,
module name, native report, artifact hash/size and committed operation agree.
The original basis record, original 669,968-byte artifact and ADOPTION marker
retain the exact precontinuation hashes above. Original failure source, candidate
and outcome bytes also remain unchanged. The databases change only as expected
for the appended extension and its inert evidence/preview custody.

At this audit, catalog SHA-256 is
`7bf382d382b9fa83704025b2e0652a17800c0b4eb1a9ffb6c4734129443a58a0`;
custody SHA-256 is
`df36f08badb6a4ea9377f925f5e26d0907fcf858465fc5dc04a1fab8dfdfa993`.
Both were unchanged by the read-only audit. Custody contains four objects, two
exports and 9,324 charged logical bytes. The four published files total 7,773
bytes; the larger quota charge includes the store's locator/record overhead.
The separate status process validates 583 context names, two modules and 672,928
artifact bytes. Its native worker CPU charge is zero, not a hidden basis replay.

### Complete costs and terminal state

| Scope | Elapsed seconds | Known inclusive CPU seconds |
|---|---:|---:|
| Continuation01 | 7.814375299960375 | 7.25 |
| Original lifecycle01 plus continuation01 | 38.383240799885245 | 36.078125 |
| Clean build plus both lifecycle attempts | 85.185002800077205 | 77.0625 |

Continuation outer tree CPU is 6.375 and full wrapper CPU is 0.875. Authoring
2.109375 and admission 1.265625 CPU seconds are already contained in the outer
tree total, and are not added again. Peak Job private commit was 930,271,232
bytes. The original aggregate continuation limit was 150 wall / 100 CPU seconds
/ 1,792 MiB; its two public calls and descendants share that outer envelope.

The outer, authoring and admission trees all exited zero, reaped their direct
children and closed their Jobs with zero active or terminated processes, no
termination request, no cleanup errors and empty stderr. The outer tree counted
14 process instances; no process remains live. Cost sums retain the failed
attempt and exclude only separate read-only audit/selection overhead, not any
native stage. These are observed local workflow costs, not scalable throughput
or growth-efficiency evidence.

This closes the selected source-package/relocated-local-owner boundary. It does
not finish reciprocal peer operation, unknown-ID discovery, broad native-library
interoperability, independent-host availability, useful-growth justification or
full deployable-v5 readiness. Those should now advance through the existing
reusable interfaces; no repeat of this passed build/basis campaign is indicated.
