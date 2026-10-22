# Exact-packet source, controls and selectors: independent review

2026-10-22, storage_outcome_audit. **PASS for the selected source boundary and
one proposed finite control run; NOT RUN and not installed adoption.** Root
owns selection, execution, result adoption and Git. This review performed only
file/source reads, comparisons and hashes; no product imports, tests, database
opens, secrets, services or proof operations.

## Exact reviewed sources

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Base129 map SHA-256:
`a629df82718f6a9d0560cacbfdc459739c15a56a1f2a46dd87929a1db51c22a4`.
All six predecessor pins match that map. The source review read the complete
transport and every other complete predecessor-to-successor diff, then the
surrounding admission, staging, ownership, profile and budget paths. The earlier
design challenge is `EXACT-PACKET-ACQUISITION-CHALLENGE.md`, SHA `7a721ff3` prefix.

All successor paths below start `software/v5/exact_packet/`; actual hashes were
independently recomputed and agree with the author/root's final selection.

| Source | Bytes | SHA-256 |
|---|---:|---|
| `evidence_network/transport.py` |8581|`b34032085bca3ddbd248afe57e655777a140d2c34b6f33ea61b80721a07b926c`|
| `placement/controller.py` |18008|`77820241984b9dc7ba5d2117a4b11bc89bf217b81697ed8d8ce90fff15e115f2`|
| `client/workspace_evidence.py` |53636|`3f39d9b594490f04e2737c0f0595c881785a9a6a168cf8fc679d25a5cdef700e`|
| `client/workspace_staged.py` |17110|`5d96c8cb891eabeb083b0bc501df1a7b268c21b73f4c17da7eb536d2428ad995`|
| `client/semantic_reader.py` |35110|`253b0ffb5825de15c239be785edcda7e15647038716679402cdf990b81f4128d`|
| `client/managed_owner.py` |33789|`9a459df2cf2c81b953044b4b5172aaefb9a3001cede6f3a1a23b29f8beb6dcb1`|

## Code judgment

- `packet` and `packet_exact` share a private `_packet`; the offered branch
  retains actual offer membership. Strict closed SHA/size entry, module,
  profile/store identity and object/envelope cap checks precede `_get`. Scalar
  entry copying precedes the first await. Both paths retain exact hash/length,
  typed put, before-COMMIT liveness, exact readback and explicitly nonmathematical
  result. No invented offer, alternate HTTP route or new authority is introduced.
- The existing `_get` remains responsible for original budget/deadline/contact,
  finite framing and settlement. A consumed failed attempt is not renewed or
  refunded. Closed/retired generations refuse. Transactional storage capacity
  remains a real later gate; preflight is not a free-space guarantee.
- `acquire`/`acquire_exact` use one undecorated helper beneath the existing public
  action decorator. Candidate ownership, body commitments/custody, genuine
  `_admit_evidence`, live-cache warrant checks, owner `open_group` and final exact
  journal checks remain. Entry and all body scalar selections are copied before
  any transfer. Body range/membership checks still occur in their unchanged
  per-body calls: this is not atomic validation of all bodies before any I/O.
- `stage_packet`/`stage_packet_exact` similarly share one private body. Exact
  snapshots, one-module variant policy, selected member inventory, metadata caps
  and original staged-token/admission separation remain. `admit_staged` and its
  consumed transition/exact-journal/local-readback tail are unchanged.
- `SemanticReader.stage`/`stage_exact` share one original `_call` scope and retain
  origin-or-pending-demand selection, limits, exact snapshot/member checks and
  conflict refusal. Existing same-selection `NO_PROGRESS` can return without an
  offered-transfer check; it transfers/adopts nothing. The README now states
  this explicitly rather than promising an offer check for every no-op call.
- Placement changes only the missing-packet offer branch. Existing local reuse,
  exact manifest/opening checks, receipt phases, recovery, idempotent old request
  and independently charged new request remain. Its sufficient full conservative
  quote is unchanged even though actual remote requests decrease by one.
- The managed-owner diff changes only its evidence-client pin. Across current129
  selected sources this was the only explicit changed-predecessor hash found.
  Staged/source protection is not absent: constructor-selected owner pins bind
  staged code; evidence binds its transport/source origins; body-location
  activation adds the semantic-reader selected pin. Full SDK writer identity
  changes, so no old managed-state compatibility or migration follows.

No blocking implementation defect was found within this selected boundary.
Unchanged verifier correctness, host/runtime trust and ordinary owner isolation
assumptions are not reproved by this source review.

## Focused controls reviewed

`software/v5/exact_packet/controls.py`: **34036 bytes**, SHA-256
`bd9a48119a3ae428e343a2d6061256026fc530cf0b281bf33e49e554214f2883`.
Root confirmed this final pin and no more edits. All eight groups and the full
staging/guard/report/cleanup infrastructure were read, including final edits.

| Groups | What the source can establish if actual execution passes |
|---|---|
|01–02|Nine real typed packet variants; max8 offer omission; real exact HTTP transfer; offered refusal, no offer insertion, duplicate custody without attempt refund; caller mutation during real provider dispatch cannot change demand.|
|03–04|Strict/bool/cap/profile preflight; missing/wrong packet identity, wrong module/profile, injected dishonest same-length response; budget/contact/closed/retired refusal; injected expiry at real SQLite before-COMMIT guard rolls back insertion; structural admission forbidden.|
|05|Actual controller, ledger, group/packet HTTP, typed stores and formal index; no offer request; full exact quote in receipt and ledger, idempotent request without new reservation, new request using retained custody but charged its full quote.|
|06–08|Exact selected AST method bodies exercise direct/staged/reader dispatch, frozen packet and later-body selection, stale-cache/foreign-candidate/refused final-journal paths, untrusted staging and pending-demand/variant checks. Owner, admission, acquisition and some call guards are explicit doubles.|

The nine receipt payloads are deliberately inert, not valid mathematical proofs.
Real structural acceptance of their packet form is not a cryptographic pass.
Groups06–08 remove decorators by explicit extraction: they do not qualify live
owner construction, source-pin enforcement, actual issuer admission or an
end-to-end mathematical workflow. Group06's changed warrant journals are stubs;
the actual retained `FINAL_TARGET` comparison is what it exercises. Group04's
commit expiry is injected into the real transaction guard, not a natural timing
race. Unchanged cancellation and recovery remain source/evidence arguments, not
new executed-control claims.

The controls assemble selected129 logical modules only from the runner snapshot:
old rows retain map pins, six replacements use expected pins in the saved
selection. Imports occur after staging. Socket dialing is limited to127.0.0.1
and the test's registered listening ports; process creation and verifier receive
paths are forbidden. This is a bounded trusted test, not a hostile-code sandbox.
Teardown closes providers/acquisitions/controllers/stores; unexpected event-loop
errors or retained registered ports fail the reported suite. New fixtures and
failed attempts are retained, not cleaned up or hidden.

## Both selectors reviewed

Both scripts are in `research/cycles/v5-2026-10-20/` and were read completely.

| Selector | Bytes | SHA-256 |
|---|---:|---|
| `Select-ExactPacketControls01.ps1` |4795|`d49129ee9686d79601f439910716354a1e7436765329124e37f8ea5ab98f1ccb`|
| `Select-ExactPacketDistribution01.ps1` |5456|`e10e6c19776eedc327fc7fe2a47205ecac941743d936607052e39569157f698a`|

The controls selector requires canonical cwd, exact129 base map, all base source
pins/sizes, exactly the six allowed new paths and expected control hash. It
assembles137 snapshot files (129 base +6 replacements +runner +controls), with29
retained runtime/map pins. It creates only a fresh selection, not a test process.
The proposed single isolated Python process has30CPU/90wall seconds,256MiB,
one process and1MiB stdout/stderr each. The frozen runner's source totals,
immutable snapshot, runtime recheck and final binding checks were also read.

The distribution selector preserves the current input's other choices and
replaces exactly6 existing SDK names:129 total,123 unchanged,0 additions and108
preparation sources. The frozen builder remains `eb1348f6` and runner `44a7bf1b`.
It drops only the predecessor map runtime pin and adds the fresh input's exact
pin, retaining29. Explicit fresh input/selection/product/output paths use
CreateNew/freshness guards; it does not overwrite old installations, migrate
state or execute a build. The proposed build envelope is120CPU/600wall seconds,
128MiB/two processes; actual launch/adoption still belongs to root after controls.
Partial preparation failure is preserved, not silently retried or overwritten.

The scripts take reviewer-supplied expected hashes; observed bytes are not
automatically promoted to trusted pins. No selector change was needed for the
facade groups because they reside in the same single control file.

## Documentation and handoff

The full source checkpoint4501B/SHA `0650870e` and API README4629B/SHA `c7d80cc2`
were read; the README's no-progress precision correction changes no code.
The final controls note/SHA `6a1035b5` was also read, including its final control
pin and later-body/final-journal description. Its synthetic/real boundary is
consistent with the reviewed suite.

This source pass supports root preparing the exact finite selection above.
Actual saved outputs, supervisor closure and final unchanged source bindings
must still be audited. It is not installed mathematical acceptance, global
discovery/availability/growth evidence or completion of the full v5 goal.
