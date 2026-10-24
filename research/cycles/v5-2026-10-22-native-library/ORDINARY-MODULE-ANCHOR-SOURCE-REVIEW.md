# Incremental ordinary-module source review

2026-10-23, `module_anchor_audit`. Source-only independent review under
`ORDINARY-MODULE-ANCHOR-IMPLEMENTATION.md`. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

Contract reviewed: `a091435bebcccacfc7241a649a988be44b696fb08f567a4c32597162c9b159ab`.
The contract/theory clearance is not implementation or runtime clearance.
No product imports, execution, database/network access or Git mutation occurred.
This checkpoint is initially **IN PROGRESS**; actual successor files are reviewed
below only after their authors report them ready.

## Controller seam: support compatibility

Use a fixed versioned descriptor with semantic/foundation/implementation IDs,
installation-manifest hash and module policy. The manifest already commits to
the six installed Python modules, supervisor/Job/domain support and the selected
runtime support; do not independently select a different core from package names.
The new descriptor must additionally bind actual loaded source pins for:

- Owner facade and profile loader: `owner.py`, `profile.py`.
- Anchor implementation: `module_export.py`, `module_closure.py`,
  `anchor_store.py`, `module_worker.py`, `OrdinaryModule.lean`.
- Direct Python helpers: `ordinary_contribution.py`, `portable_preview.py`.
- Current helper import/verification dependencies: `portable_owner_request.py`,
  `owner_request.py`, `portable_candidate.py`, `ordinary_preview.py`.
- Native helper closure: every present selected compiled part for `OriginalExpr`,
  `OriginalDecl`, `CheckedExtension`, `BootstrapSupport`, `OwnerRebind` and
  `OrdinaryExport`.

The native closure follows actual imports: OrdinaryModule imports OrdinaryExport
and OwnerRebind; these import the other four and Lean/Std runtime modules. G's
AuthoringProfile.verify explicitly checks its imported R/B/PP/R.V1/PP.P helpers.
Source selection must bind those actual objects to exact pinned paths, not just
accept a same-basename file. Stdlib/Python execution integrity retains the existing
runtime premise; the descriptor is not a hermetic runtime attestation.

Do not replace this with the entire package PROFILE hash, or include unrelated
formal-query/discovery/documentation payloads merely because the package loads
them. Existing complete profile verification still runs before and after the
operation. A query-only edit to the shared loader/facade file will nevertheless
change a genuinely selected file pin; avoiding that would require a separately
justified split, not silently excluding the registration call path.

Existing sources read for this recommendation: the selected matching controller
and worker, ordinary-query package loader, ordinary-module owner facade,
ordinary admission/contribution and preview helpers, and native import headers.
No repeated native/helper compilation is warranted by this source inspection.

## Controller seam: successful event versus completed cleanup

`ordinary_admission._clean_worker` establishes success, not merely termination.
For safe cleanup disposition reuse the separate predicate already present in
ordinary_admission's failure/finally path:

```text
cleanup_complete(result) :=
  result is dict
  and result.job_closed is True
  and result.direct_child_reaped is True
  and result.cleanup_errors == []
  and result.final_job is dict
  and result.final_job.active_processes == 0.
```

Set `native_entered` immediately before invoking the actual supervisor. With no
native entry there is no new child-cleanup uncertainty. An entered invocation
that throws or returns absent/malformed cleanup evidence is uncertain. In that
case block this sidecar; do not register a result or withdraw unrelated accepted
mathematics by default. A nonzero exit or supervised termination with the above
complete-cleanup predicate is a clean failure: retain its charged ineligible
orphan without needlessly blocking future exports.

Registration still requires the stronger unchanged success predicate: clean zero
exit, no termination request, no terminated processes, valid CPU observation and
all native/controller checks. Handle cleanup in a finally path that also covers
exceptions from accounting callbacks, report writes and subsequent validation.
Those failures must not bypass uncertainty handling. Saved reports may describe
events but cannot supply the live registration event on a later invocation.

The state author proposes a durable RESERVATION.json before native work and a
CLOSED.json only after known cleanup/no-worker disposition. Reserved operations
without CLOSED, or incomplete reservation directories, independently refuse
reopen even if writing BLOCKED failed. This is the appropriate narrow resolution
of the abrupt-controller-loss gap, pending actual code review. Cleanup metadata
after allowance expiry must be fixed-size/bounded and retain the owner lock;
normal useful work must not acquire a renewed budget through this exception.

## Actual successor review

### Pure collector

Read the complete `software/v5/ordinary_module_anchor/module_closure.py`, SHA-256
`f053e9726bdba24724e7e44baa03ffa0006f80b068440086a36023068512aa8c`.
**No source blocker found for this pure seam.** No execution was performed.

- Validates all frontier outputs against the selected warranted context before
  traversal; bounds serialized name material and unit/name counts.
- Requires portable ExportID derivation and canonical name bytes, refuses basis
  overlap and duplicate units/names, and verifies explicit target UnitIDs at cuts.
- Rejects acquired units that overlap any basis/anchored unit/name or another
  acquired group. Full portable evidence remains necessary for every new unit.
- Supplies only basis plus anchored bindings to the unchanged admission planner,
  and requires every acquired unit to remain new and topologically ordered.
- Applies existing 32-unit/4-MiB/aggregate bounds to newly acquired work.
- All-anchored reuse has request=None, empty new evidence/units, zero fetches and
  separately records reached cut units. The result does not assert acceptance.

The pure object cannot establish that its supplied unit census is complete or
that a local live generation event registered it; both remain explicit controller/
store responsibilities. This is consistent with the contract, not a missing
cryptographic verification claim. The native anchor-plan SHA is a caller-bound
input and not evidence of authority by itself.

### Remaining successor boundaries

Registry, native worker and controller/facade handoffs remain pending. No test
launch or integrated implementation is cleared by the collector review.

The later concrete reviews below supersede this initial pending status. They
clear sources for separately selected changed-boundary checks, not actual Lean
compilation, live registration or installed-package behavior.

### Focused pure-control source clearance

Read `frontier_controls.py` at
`26b2d538057a4ae7b27392689c29be1a0983501a4df44f2e8a96365e24581fa1`
and `select_frontier.py` at
`59eb157b1d94b0e81958201aed5805cb82d63fe18883bab4674e4d338c6f6917`.
**Clear these sources for root's separate finite pure-frontier selection.**
This is not a result or permission to run registry/native integration.

One pre-execution test defect was corrected: invalid AnchorID `bad` correctly
raises the inherited `HASH_ENCODING`, not a MODULE_CLOSURE-prefixed error. The
negative control now expects that actual failure category; product validation
was not weakened. The seven groups cover new-work-only bounds and decoding,
zero-fetch/zero-planner anchored reuse, every frontier warrant including
unreached outputs, malformed/duplicate frontier data, target portable identity,
name-ownership conflicts and still-required unanchored proof dependencies.

The harness uses three pinned retained real units but explicitly synthetic
warrants/frontiers. It blocks database, child-process, network and owner-operation
seams; prior closure-control functions are not called. Only pinned helper IO,
loading and original 50-wall/30-CPU checks are reused. The selector uses the
actual builder pin/read/fresh-write APIs, exact current package/profile/runtime
pins, four source snapshots and a fresh output namespace; proposed outer limits
are 60 wall seconds, 35 CPU seconds, 512 MiB and two processes. The original
source fixture hashes are rechecked. No prior passing campaign is repeated.

### Saved pure-frontier outcome

Independently read the saved result, seven group outcomes, command and stdout for
`experiments/v5-local-checks/ordinary-module-anchor-frontier-01`. **PASS within
the stated pure/mock-warrant scope.** No rerun occurred. Rehashed all 148 runtime
pins and four exact source snapshots without mismatch; original and saved
selection hashes both equal
`2c82c894c36ae80c85c41bf2fa71430e56873515bc5026d51c83a9f06c37992e`.

All seven named controls passed. The actual process exited zero, direct child was
reaped, Job closed, cleanup errors were empty, and active/terminated process counts
were zero. Stderr is empty. Wall time was 2.4493579 seconds; Job CPU 1.71875 plus
outer wrapper CPU 0.515625 gives 2.234375 known inclusive CPU seconds. No native
checking or owner opening occurred. This does not establish registered mathematics.

Saved RESULT hash:
`870732f5210afe8969ff6366aa2064c60b68968dd6da1249ca46793acb19076d`.
Saved FRONTIER-CONTROLS hash:
`5364661e342f56dafef1314658bab8d9c356a5b114c7c45e5e79608258406430`.

### Registry and final controller review

Read complete registry `db2e19f3...` and its exact quota correction; final reviewed
`anchor_store.py` hash is
`a244eaf2764b6a51f4006447eebe3b69529a46bf376f999804a99f23661a929e`.
**No remaining source blocker found in this first profile.**

The review caught a concrete failure-path issue: checking event metadata totals
only after copying could leave a clean failed operation over the same ceiling
used by reopening. The correction validates all pins and total artifact/event
sizes before creating copy directories. Its metadata envelope includes actual
reservation bytes, 4096 bytes for CLOSED and the full maximum record size. A
partial copy therefore cannot exceed its own reopening quota solely because a
capacity refusal occurred too late.

The sidecar holds the existing owner lock, checks exact store/adoption/activation
and support identities, admits only the identical live Grant/check callback,
retains incomplete reservations as fail-closed, and records cleanup separately
from success. Complete unit maps are derived from the controller-validated new
request/report; the collector remains responsible for original portable evidence
and UnitID correspondence. Warm loading reads compact registered maps and actual
artifact hashes, checks all inherited warrants and targets, refuses overlap or
incompatible support, and never parses prior proof event files.

The final canonical record is published last by a fresh non-overwriting Windows
rename after clean-event/parent/current-context checks and flushed copies. Unknown
publication/readback exposes an exact AnchorID and COMMIT_UNKNOWN; post-commit
view construction exposes committed-reporting-failure. Neither path overwrites or
revokes existing records, retries the live event or reconstructs authority from
saved reports. The registry itself cannot prove a trusted caller really ran the
worker; the reviewed controller/call-path pins and live-operation rule supply
that premise.

The complete controller and exact facade/loader deltas were reviewed, including
the final exception preservation and narrower-support wording refinement:

| File | SHA-256 |
|---|---|
| module_export.py | `85f9a2b5695dd90dd888bd3868f51a41904cb0b2d0d14335abe0b65d5182b65c` |
| ordinary_module_anchor_package/owner.py | `a17f7905f479929bf55f3ddbe8f857de9d48e528a132e4c27f2a000d1adb028d` |
| ordinary_module_anchor_package/profile.py | `8f690bd50b5ded03da309ad7c42850954aac80d889650442cbba3110028ee48d` |

The controller keeps full profile checks, reports known-clean failures without
quarantining unrelated mathematics, and marks uncertain cleanup before accounting
or logging callbacks can throw. All-anchored use reloads the exact registered
chain/current context, makes zero native calls and returns the existing owned
import directories without inventing a new anchor. Publish-then-throw structured
statuses are preserved even when the returned view was never assigned.

### Native/worker review

Read the complete native and worker sources:

| File | SHA-256 |
|---|---|
| OrdinaryModule.lean | `aa2093d2cb75636f5ce0c248321b6b06e516a42d67cb2cbbadadd3ec880d8799` |
| module_worker.py | `7d577ce31e37a07a0ac4868d10da792e4476db4df6ab0492791f9d8434b6247b` |

**No source blocker found.** Nine worker arguments, request V2 and report V3
agree with the controller. Full five-part explicit parent mappings cover every
registered ancestor with runtime-only fallback. Loaded modern module headers,
direct imports and complete own declaration censuses are checked. Old bindings
retain safe kind/name/ordered-universe checks but do not re-encode old inventories
or proof bodies; their semantic correspondence is inherited from the registered
generation event and exact protected bytes.

New decoding admits only fixed basis, registered outputs and preceding new
outputs, never all ambient imported declarations. Exact residual singleton
matching remains proof-bearing. The actual unchanged private and public delta
checks, including public theorem-erasure conversion limits, remain mandatory.
Separate private/exported rereads check child headers, inventories, partitions
and target resolution. The worker binds request to the exact plan hash and hashes
all actual parent parts before/after phases; it never opens an owner or promotes
a saved pending report alone.

The removed immediately duplicated pre-phase hash invocation is safe because
invoke performs the same check immediately before starting that phase. Remaining
artifact hashing/loading still scales with selected bytes. This source review
does not establish Lean compilation, successful actual incremental import, cheap
cold onboarding, net growth or final-v5 readiness.

### File-only assembly source clearance

Read complete `ordinary_module_anchor_package/assemble.py` at
`1c426a2ce3484448effe5dee559d52cf0c43650fcfd2f50946aba97e05c6481d`
and `select_assembly.py` at
`2ee1f9a8805b10e5ece585347e2d81aad26772e6c7881ed24bb0c8c3a50307b5`.
**Clear these sources for root's separate finite file-only assembly selection.**

The exact current query base/profile and owner/loader pins are required. The
complete resulting census is 134 payloads: 127 unchanged, six replacements and
the new anchor_store helper. All native admission installation bytes, compiled
helpers, query and discovery payloads remain unchanged. Copies are streamed into
a fresh output, bounded and hash-checked before/after; the profile is published
last. No owner state, network, native compilation or mathematical acceptance runs.
The selected source/runtime maps and original source copies are all pinned.

The selector proposes outer 90-wall/50-CPU/512-MiB/two-process limits with inner
60-wall/40-CPU limits. Actual assembly receipt, installed loading and incremental
native use remain separate outcomes; this clearance does not infer them.

### Inert storage-control source clearance

Read complete `storage_controls.py` and its final narrow added warrant/group
identity negatives, final hash
`3f9a14f667dde2ae8c5ba644c3897713da8a63fdf00d9145dcda56af47d199e2`;
read `select_storage.py` at
`41f512eed55c7544da6c1d20ea6930581b50c751fac94beeb2368d5e3e824ead`.
**Clear these sources for root's separate finite eight-group storage selection.**

The controls deliberately construct exact-class objects with inert eligibility/
context methods and an ordinary unlocked handle. Artifacts explicitly contain
NOT_A_LEAN_MODULE bytes. This bypass of authority is conspicuous and appropriate
only to test storage mechanics; it is never counted as a native event, actual
registration authority, owner lock qualification or mathematics.

The eight groups test commit-last/cleanup ordering, warm loading without old
event/proof decoding, parent-child maps, uncommitted/foreign-grant refusal,
warrant and artifact corruption, compact name/unit/ExportID conflicts, support
and address refusal, retained-orphan capacity, pre-copy quota refusal followed
by reopening, ambiguous post-rename publication with exact lookup, and unresolved
cleanup/incomplete-store refusal. Injected failures modify only newly created
test fixtures; missing-artifact variants are renamed and retained, not deleted.
Database/process/network and real owner-operation seams remain forbidden.

The selector adds only the storage script, store source and matching arguments
to the cleared frontier selection pattern: five snapshots and the same pinned
package/runtime/three evidence units. Limits remain inner 50-wall/30-CPU and
outer 60-wall/35-CPU/512-MiB/two processes. No large allocation is needed: inflated
metadata pins must fail before a copy. Actual outcome and live-native authority
remain separate evidence.

### Saved storage and file-only assembly outcomes

Independently read the saved results, command records and complete stdout for
`ordinary-module-anchor-storage-01` and `ordinary-module-anchor-assembly-01`.
**Both PASS within their selected scopes.** No runtime was repeated, product
module imported, database opened or owner/native operation performed by this
audit. All 148 storage runtime pins and five source snapshots, and all 152
assembly runtime pins and eleven source snapshots, were rehashed against the
saved selections and originals without mismatch. Saved/original selection bytes
match respectively:

- Storage: `987e7a9d5ac282c1ad453e08ffe4d14fce8872a163b8f621608347efe4c083da`.
- Assembly: `5299fed789146ca2dc82fed6f102035fd389b08ccaeb47ad67ae80ef6746178d`.

Storage reports all eight intended groups passed, zero owner opens and zero
native operations. Its fixtures remain explicitly inert/non-Lean. Actual exit
was zero, child reaped, Job closed, cleanup errors empty, active and terminated
process counts zero, stderr empty. Wall time was 4.1113099 seconds; Job CPU
2.15625 plus outer wrapper CPU 0.703125 gives 2.859375 known inclusive CPU seconds.
RESULT SHA-256 is
`4f18d8b62c6aa0542ab6ef84bcf624247a2c4de3b8626eaaf3ab6395e736f2cd`;
STORAGE-CONTROLS SHA-256 is
`f3a2a4091ef01d6ba16534e33c8e9f3e3f4dba43ae81c2a030fb90bab443d2c9`.

Assembly's actual output contains exactly 134 payloads plus PROFILE and ASSEMBLY.
Rehashed every payload against the profile/installation manifest; independently
compared all 127 unchanged payloads to the base and all six replacements/one
addition to the receipt. No content, length or census mismatch was found.
The profile is
`8404d56996180520c88f98f3fec61100809bde59297b983de686fede8958ac93`;
the unchanged installation is
`32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.
The native installation, compiled helpers and discovery/query payloads are
unchanged. This is a file-only successor, not an imported or adopted module.

Assembly exited zero with reaped child, closed Job, no cleanup errors, zero active
and terminated processes and empty stderr. Wall time was 4.4685668 seconds; Job
CPU 1.5625 plus outer wrapper CPU 0.59375 gives 2.15625 known inclusive CPU seconds.
RESULT SHA-256 is
`a1ca48cfa30ccf9d1fc5f81175fecdefcbf66e7a95f91845a7caf71db3d72586`;
ASSEMBLY SHA-256 is
`03520b9bb3fef53d78671af07269dafc327d06a23f604053128edeed538cc339`.

### Five-call native integration source clearance

Read the complete native harness and its exact receipt-census correction, and
the complete finite selector:

| File | SHA-256 |
|---|---|
| ordinary_module_anchor_package/native_check.py | `92575c61c39a36b7eed94913151ef44cd40112e836cb42dd575b9959f69f3c9b` |
| ordinary_module_anchor_package/select_native.py | `ca0c69dc0adc36d9435dc52b6bea516847fd52f7cae8b5fccd278c7553e5334c` |

**No remaining source blocker found; clear for root's separate exact finite
selection.** The selected five calls are cold definition A export/registration,
one-new-unit theorem B using registered A, ordinary Lean consumer of B, reopened
all-anchored reuse of B, and refusal under the older context. B's request must
contain exactly its new evidence unit, with A represented in the registered plan;
both normal theorem application and transparent definition reduction must compile.
The reuse call requires zero fetches/native calls and no new registration. The
wrong-context call must refuse at ANCHOR before output/native work. No new
admission, extraction, helper rebuild, peer input, corruption or retry is selected.

Reviewed inherited helper seams directly: `capture_tree` hashes each file through
`hold` as well as returning its name, so unchanged registry-tree assertions are
content-preserving; `consumer_source` uses both `applyTwice_eq` and `rfl` on
`applyTwice`; the five artifact parts agree with the reviewed worker/store; and
`clean(exit_code=1)` requires the intended nonzero exit with known clean closure,
not an arbitrary failed process. Its exact helper pin remains
`aaba6e2e30906414f539842fd7678aaaf3ab7f9c077b30c6f115db7407584831`.

The original preflight would have rejected the legitimate ASSEMBLY receipt as an
extra package file. This was caught before execution and corrected in the unused
harness: it now requires the selected receipt hash, checks profile/installation/
implementation and exact six-change/one-add bindings, then includes only that
receipt in the exact census. No evidence was deleted and arbitrary extras remain
forbidden. The exact reviewed receipt is the saved hash above.

The selector is preparation-only, pins sources/runtime/receipt, requires a fresh
output and absent registry, and does not open the owner or launch native work.
Outer limits are 270 wall seconds, 165 CPU seconds, 2048 MiB and eight processes;
inner limits are 240 wall seconds, 140 CPU seconds and 1536 MiB with per-call caps
and shared remaining allowance. The same retained synthetic owner is reopened in
place; all 252 predecessor immutable files and unchanged native installation are
held. Failure preserves partial output and unknown accounting stops the run.
Actual compilation, registration, reuse and refusal remain separate evidence.
Neither this clearance nor prior file/pure outcomes establishes cheap cold
onboarding, a net useful-growth advantage or final-v5 readiness.

### Saved native01 failure and retained-owner disposition

Independently audited the saved first attempt; **native01 remains FAILED**.
Selection is
`6719f6e513cfffe18c71c7b170d63f737be89c4ab19204124cd1e3af90318b2b`.
All 152 runtime pins, four source snapshots and 252 predecessor immutable files
were rehashed without mismatch. Original/saved selection bytes match. No product
or runtime import, owner opening, database operation or experiment rerun was
performed during this audit.

The first and only public call, cold A export, invoked the native worker once.
Lean reported parse errors at OrdinaryModule.lean 449 (record layout, expected
`}`) and 499 (reserved token `matches`). Its phase trace contains only build
STARTED and build EXITED 1. Neither reread occurred. The generated `modules`
directory is empty; there is no successful native report, public MODULE manifest
or registered anchor record. Thus no incremental import claim follows.

The public controller reports MODULE_EXPORT_NATIVE_NOT_CLEAN and accepted=null;
the harness's SMOKE_UNCLEAN_PROCESS_TREE is the generic assertion resulting from
an unexpected exit code, not evidence of a live or uncleared process. The native,
public and outer Job reports all show exit code 1, reaped direct child, Job closed,
zero active and terminated processes, empty cleanup errors and no termination
request. Stderr is empty at each layer; the compiler diagnostics are retained in
native stdout. Outer wall time is 8.7611376 seconds; outer Job CPU 6.1875 plus
wrapper CPU 0.6875 gives 6.875 known inclusive CPU seconds. The nested 3.796875
native and 5.03125 public Job CPU values are already included, not added again.

Saved RESULT SHA-256:
`6a23ba815f87d42ec03b0dba13f66a549987b5288a20b0a616f7fd3a81cddbf5`.
Saved NATIVE-CHECK-RESULT SHA-256:
`b851fef653176c9cc81e78a0037b3abb8076f23a327b68c3674214fcb1b18414`.

The actual sidecar contains its STORE marker and exactly one retained operation,
`f08b3ae81225416bbdbfe37f0ebeeea20e3628cf31696ee558622b2ed6b6733b`,
with RESERVATION.json and CLOSED.json only. CLOSED has the matching operation and
store binding and reason CLEAN_FAILED_EXPORT. The records directory is empty;
there is no BLOCKED marker or artifact/event copy. This is a charged clean orphan,
not a registration or unknown cleanup. Nothing should be removed or rewritten.

Read the exact reopening census again. STORE binds owner/adoption/activation,
implementation/foundation/semantics and fixed capacities, not one support source
version. Existing reservations must bind their operation and store and possess a
matching CLOSED record, but need not have the new operation's support_id. Actual
committed anchors still require exact support compatibility when loaded. Hence a
separately selected corrected-support cold operation can use this same owner
without deleting or rewriting the orphan; it must preserve these exact files,
account for their retained capacity, require no prior records, and use fresh
output/operation identity. This is a source-and-saved-state eligibility conclusion,
not a live reopening or native success test. Any syntax correction and successor
preflight must receive exact-delta review before another finite selection.

### Syntax-only successor source review

Read the exact `OrdinaryModule.lean` to `OrdinaryModule02.lean` diff. New native
source SHA-256 is
`57c97e06ea1b700106d61e265f6abb4a0707f2f89004e870b60bd54cd981c66c`.
**Clear the syntax-only correction.** It places the AnchorModule record fields
on distinct correctly indented lines and renames local reserved token `matches`
to `moduleMatches` at all three references. No semantic check, scope, authority,
algorithm, constant, imported helper or limit changes. The failed source remains
unchanged. Actual compilation is still untested; this review does not convert the
failed first attempt into a pass or authorize its rerun.

Read complete `assemble02.py` at
`29c534cccf76a0401962870ddeffd23b1f86adee602b3add04e6fdc1874d5f76`
and `select_repair.py` at
`5d017e1584123185a69bfeb11ae672aab0d4f324a56b4644c22d62c28cb76be1`.
**Both source-clear for separate bounded selections.** The file-only assembler
binds the fixed base/profile/receipt, validates all 134 selected payloads and
changes only module/OrdinaryModule.lean, then writes a new profile and receipt.
Its copies are checked before/after; PROFILE publishes last. The unchanged 133
payloads, native installation and actual owner remain untouched. No native or
owner operation is performed.

The two-mode selector binds the preserved native01 selection hash. Assembly mode
pins original package/runtime files plus the exact root-dependent source files.
Native mode remaps only package paths to the new output, requires unchanged hashes
for every other payload, and additionally pins all three retained sidecar files.
It preserves the original finite assembly/native budgets, snapshots its sources,
and requires fresh output/selection paths. It prepares only; no selected operation
is launched. Native mode still requires review of the exact native_check02 source
and saved assembly02 outcome before root's independent execution selection.

Read exact `native_check.py` to `native_check02.py` delta; final successor is
`08bcc96dcbe08cfd8a2d4d25ab17d8d7acd793f4eddcbff877860c6159364d15`.
**Clear the successor harness source.** Besides explanatory/selection metadata,
the only changes are one-payload receipt/base-profile binding and exact preserved
failed-sidecar preflight. The three hard-coded byte/hash pins match the audited
STORE/RESERVATION/CLOSED files; records must be empty and the old operation must
be the only operation. The inherited tree walker holds their content hashes,
which are rechecked after new work, reuse and refusal. No prior state is reset,
deleted, reconstructed or promoted from a report. All five substantive calls,
delta assertions, consumer checks and original limits remain unchanged. The saved
assembly02 audit and root's finite launch selection remain independent gates.

### Saved one-payload assembly02 outcome

**PASS, file-only scope.** Independently read result/receipt/command and rehashed
all 156 runtime pins and six saved source snapshots without mismatch. Saved and
original selection hash is
`326becd0e8d76c13db6a6b92e20fb6210ae8477ac75914c25223ec54152c7184`.
The package census is exactly 134 payloads plus PROFILE and ASSEMBLY. All 133
unchanged payloads match assembly01; the only changed payload is the reviewed
native02 source. Every one of the 106 PROFILE auxiliary pins matches actual
bytes/lengths. Relative to the old PROFILE, only that native entry changes;
schema, installation, worker and helper-path fields remain equal.

The operation exited zero, child reaped, Job closed, cleanup errors empty, zero
active/terminated processes, and empty stderr. Wall time is 4.7535127 seconds;
Job CPU 1.9375 plus outer wrapper CPU 0.703125 is 2.640625 known inclusive CPU
seconds. No rerun, native compilation, owner operation or state migration occurred.

- RESULT: `14a86e34851a78f540b72605086b82385318ec831338d457fc6201047e8a44fd`.
- PROFILE: `5e7e9a6b8679864e52f93f7704f58591799406a3226343e05ce0c01a85cc7be9`.
- ASSEMBLY: `0685b54054e6f53892ad03795444c8a7447da2b1d6acff4f80b32d1284bad0f2`.

This permits selecting the separately reviewed native02 harness against these
exact bytes; it does not infer its outcome or erase native01's failed evidence.

### Current package build-recipe delta

Reviewed the exact build03/source-map03 to current package-recipe delta:

- `ordinary_module_anchor_package/build.py`:
  `18fb486233d66dd56f8ef8ca4fbb3378edc39f69e7267baf71a4c02bbc48c79b`.
- `ordinary_module_anchor_package/source-map.json`:
  `dffd941e4c119a857cd5a95ce1219cdca772d6308c0a82467bde916f45ca8630`.

**Source-delta clear; no full build selected or performed.** The runner changes
only explanatory text, its own path/map names and exact expected counts. The map
replaces six direct payload source paths/pins and adds anchor_store, using native02
rather than the failed native source. The 47 base inputs, all four lane
descriptors, native runtime pins, artifact suffixes and extractor output remain
unchanged. Ordering-only JSON differences do not alter those mappings.

Independently rehashed all 71 source inputs against bytes/lengths and compared all
54 direct-copy sources with the corresponding actual assembly02 payloads; no
mismatches. Counts agree: 134 payloads and 106 auxiliary payloads. This records a
source recipe for the current assembled product without repeating its unchanged
compiler lanes. It does not claim a new clean build was executed or that rebuilt
native artifacts are necessarily byte-identical.

### Saved native02: cold registration succeeded, warm import failed

**The whole native02 run remains FAILED at WARM_B.** It contains two public calls,
not five. The cold A suboperation did genuinely succeed; the failure must not erase
that completed work or be labeled a passing warm-import test.

Selection:
`bf253a11b52a5f84c157a1165f69d869636a5aa960217db2c8e99faa69b2f752`.
Independently rehashed all 155 runtime pins, four source snapshots and 252 original
immutable files without mismatch. The original three failed-sidecar files are
among the preserved pins. Saved and original selection hashes match. No live
owner/database/native operation or rerun was performed by this audit.

Cold A's registered AnchorID is
`08744de1cce786beec313017da1dea24921319a8996737d02a89c3dabc40bc55`.
Recomputed its domain-separated hash from the actual record. All five artifact
parts match their recorded bytes/hash in both original output and owned sidecar
copies; all seven copied event files match original outputs and their recorded
pins. The native report's complete inventory equals the retained A evidence.
Its unit census is one newly checked definition, zero matched units, two checking
passes, and exact target applyTwice. Build, private reread and exported reread all
completed with exit zero. The record has no parent, imports Init, and binds current
support `6db6843068d2fcb3f15511f2e5ca2b79f94aeee00d19fa7b8d9764d37cb16596`.

Warm B reached collection of exactly one new B unit, cutting A at the registered
frontier. Its worker then failed in the build phase with error 4058, "no such file
or directory", naming A's owned `.olean`. That exact 319-character path exists,
has 3128 bytes and matches A's committed artifact hash. This is consistent with a
native Windows path-handling limit, but existence/hash checks alone do not prove
that diagnosis. The warm phase trace is only build STARTED and EXITED 1; its
generated module directory is empty. There is no B record or report and no later
consumer/reuse/refusal call. Prepared residual input is not successful reuse.

All native/public/outer process reports have known clean closure, reaped direct
children, closed Jobs, zero active/terminated processes and no cleanup errors or
termination request. Cold native/public exits are zero; warm native/public and
outer exits are one. Warm native stderr retains the actual file diagnostic.
Total outer wall time is 29.4592283 seconds; outer Job CPU 25.421875 plus wrapper
CPU 0.734375 gives 26.15625 known inclusive CPU seconds. Nested costs are included,
not added again. The native cold-A cost was 18.640625 CPU seconds; warm failure
cost was 2.515625 native CPU seconds.

The preserved sidecar has exactly one record and three operations: original
native01 clean failure `f08b3ae8...`, successful A `2960f88a...` with
LIVE_GENERATION_CLEAN_BEFORE_COMMIT, and warm-B clean failure `646b63d0...` with
CLEAN_FAILED_EXPORT. All have CLOSED records with matching store/operation
bindings; no BLOCKED marker exists. The failed operations remain charged; no file
is removed or rewritten. Reusing A under unchanged support remains a potential
continuation, not an actual demonstrated result. A source repair which changes
support must not silently inherit A's authority; it needs a justified compatible
path or a genuinely new checked generation under the new support.

- RESULT: `5da87a0774e56e0419db38b5c8fa5d7649efbf50897850b3f3f33e228ab26559`.
- NATIVE-CHECK-RESULT: `8fbcd38720c9e0d1f7ae47f76fee612823376119d69ef1183e534960cd0a4c02`.

The reviewed source clearances were not promises of runtime success. This actual
failure isolates a deployment boundary; neither it nor the real cold registration
establishes warm incremental verification, lower full-workflow cost, net growth or
final-v5 readiness. Preserve both before choosing the minimum decision-changing
repair.
