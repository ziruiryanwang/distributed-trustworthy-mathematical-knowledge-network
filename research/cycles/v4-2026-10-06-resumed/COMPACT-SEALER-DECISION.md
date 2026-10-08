# Compact source-free sealer: remove an adoption boundary, not rebuild a prover

2026-10-06. Scale source-only decision for root's extended16:00UTC milestone.
Canonical root only. No product import, build, proof, native check or network
operation was executed. Existing source/evidence/installations remain frozen.
Independent reviewer challenged the proposed authority boundary in parallel.

## Decision and exact finding

**Feasible with no additional executable or formal-data payload.** The current
agent03 compact receiver already contains the actual full stage-capable prover
driver, its unchanged guest image, source-free prepare/advance code and final
verification/export code. It is currently blocked by the installed action scope
and public CLI, not by missing cryptographic machinery.

| Already shipped asset | Bytes | SHA-256 |
|---|---:|---|
| receiver/bin/commons-certified-checker.exe |66458624|32356c4f1aa94d0cf1404e23eb092f2bdeb75ab3f88396e90ea88747a54db0a7|
| receiver/assets/checker.bin |1418472|3a3391d70d23659e62823c4fa5510bf5e797c4d21e5cf1b0070957ae592a8745|
| receiver/cert_workflow.py |54688|a86a01537be230f9ff7e3861faea503e59f9d87200f5827fb551225a033cedef|
| receiver/cert_stages.py |40997|02b1429d47b17b3b9fdc8bcecfb1fb4ee821c75f67df83cb01f111d1d7af632a|

Both driver and guest were independently rehashed at the current agent03 and
older full contributor locations and are exactly identical. Their mathematical
image and foundation IDs also match. This is stronger than assuming a binary
named "checker" contains the prover; the existing Session.stage_args/advance
explicitly invoke this exact driver's `stage` command for all proof stages.

## Concrete dependency closure

The source-free path is:

`prepare-seal -> fragment load/snapshot -> group_parents real verification ->
Session.capture -> driver stage snapshot -> READY -> bounded advance ->
driver segment/lift/join/resolve/finish -> driver verify in cold directory ->
finalize_bundle -> exact capsule/journal/receipt export`.

It needs the adopted Python runtime/stdlib and CRTs; workflow/stages/Job/domain
helpers; capsule, bundle, fragment and composition modules; schema, registry,
foundation witness; driver and guest. Current initialize also loads the composer
and validates the foundation witness even though no owner-source frontend runs.
Application is loaded only for apply/apply-fast. Native_relation and thin receipt
verification are not called by this sealer route; the existing driver handles
its genuine frontier and final verification.

For this iteration retain the already audited **606-file,101249548-byte crypto
closure**, not a newly hand-pruned stdlib distribution. It includes the two
unneeded sealer binaries, application module and four guide files because they
are part of the current combined receiver role. No requirement forces an exact
mathematically minimal runtime subset; further dynamic-import/DLL pruning is
unnecessary risk and produces no incremental download saving for current users.

The current profile describes12402assets/2347787453bytes. Its excluded authoring
set is11796files/**2246537905bytes**: runtime/lean, native authoring files, support
plan and inventory. These are already absent physically in compact agent03.
The source-free worker environment removes LEAN_PATH and authoring PATH roots.
Thus the proposal prevents a sealer invocation from demanding those absent files;
it does not pretend their integrity was freshly checked.

Current combined package:6639files/236496031bytes, including profile/manifests.
Current compact base-manifest payload:6636files/235424720bytes; remaining files
are the base and two supplemental manifests. Existing full-package manifest
payload:12496files/2349258239bytes. These are uncompressed file-map totals, not
archive-size estimates.

**Exact additional binary/image/runtime/formal-data bytes:0.** New Python/API/
profile/manifest bytes depend on the final selected edits and cannot honestly be
given an exact delta before those edits exist. The assembler must report that
small textual delta and full resulting size; do not promise an exact future size
from this decision alone.

## Why current public commands cannot already do this

Installed.receiving_only currently applies only to check-fragment/apply and the
two fast actions. prepare-seal and advance instead demand an exact complete
profile inventory, including the absent authoring files. Current receiving worker
policy permits driver verify/execute, not stage. The public commons.py facade also
rejects both actions, requires every --run to be fresh, and requires new budget/
deadline flags on every currently supported workflow. That latter behavior is
wrong for a continuation and must not be reused unchanged.

## Minimal selected implementation plan

1. Introduce immutable **SEAL_ACTIONS={prepare-seal,advance}**, separate from
   existing receiving/fast action classes. A derived source-free-adoption scope
   is receiving OR sealer. Use it for module/path/inventory/initialize/final
   rebind rules. Sealer uses the full existing crypto closure, never fast_hash_names.
   Preserve old receiving allowlists exactly; adding stage to all receivers
   would be an authority expansion.
2. For sealer actions permit only the adopted driver with genuine verify and
   the exact stage family. prepare-seal needs snapshot plus frontier verify;
   advance needs segment/lift/join/resolve/finish and final verify. Reject
   native=True, owner Lean, foreign executables and unrelated commands. Bind
   stage image to the adopted guest; operation paths and dependency arguments
   remain generated from the validated operation, not peer-selected executable
   strings. No new driver/image/Cargo/native build is necessary.
3. Keep prepare_seal, group_parents, Session.capture/advance, state validation,
   reserve/observe, final last_verified and commit logic unchanged where possible.
   Existing worker stages already require direct exit AND zero active Job count
   before accepting; do not add the recently fixed facade race here by accident.
4. Extend the public facade with exact action-specific grammars:
   prepare-seal has fresh run, held fragment, expected manifest SHA/interface,
   original explicit budget/deadline; advance has existing run and bounded
   max-new-stages, **no replacement allowance or deadline**. The adopted profile
   remains injected by the facade, never taken from a peer.
5. Repin the fresh workflow in profile; repin profile in facade; update the
   base and both supplemental manifests plus relevant adopted documentation.
   Old package/operations stay unchanged. This likely needs no cert_stages edit.
   The source-free installed-asset-scope label must describe sealer scope honestly.

The exact primitive implementation should be independently reviewed before
root selects one bounded new boundary qualification. This decision itself is
not source-edit or runtime authority.

## Compatibility and non-negotiable checks

prepare-seal remains **proposition-fragment only**. It does not directly certify
D1/D2 standalone definition artifacts. Native-fast fragments are compatible as
inert proof wires because the sealer ignores sender local-assurance metadata and
executes its adopted guest. Native success does not promise guest capacity.

Mathematical profile ID, image, foundation, receipt/journal binding, rank descent,
singleton final binding and actual distinct-frontier verification stay unchanged.
Every required stage still uses the original budget/deadline, resource caps and
preserved failure state. Final export still requires last_verified=True from the
current completing invocation, full plan completion, closed workers and exact
child binding. Persisted flags and locally checked markers never certify output.

The changed profile digest intentionally prevents continuing an old full/agent03
operation under the new installation. Do not rewrite/migrate old state to make it
fit, reset allowances or resume failed campaigns. Fresh prepare-seal creates its
own original allocation; only its clean READY prefix can continue.

## Efficient discriminating qualification, not another proof campaign

Pure changed-boundary controls should establish: sealer snapshot/stage/verify
permit and native/execute/foreign-executable refusal; unchanged receiving stage
refusal; default/final sealer rebind remains crypto; missing/corrupt driver/image
refusal; exact public grammar and no advance budget renewal; old profile-state
refusal and unchanged final-invocation verify requirement.

A fresh actual public compact prepare-seal on a separately selected compatible
held fragment can discriminate the absent-authoring dependency removal and
generate a genuine snapshot. A bounded no-progress/reserve continuation can
exercise the ordinary advance entrypoint without renewing budget. Neither would
be a completed new certificate. Existing exact driver stage/cold-verify evidence
and unchanged stage/export code should be reused; do not repeat a successful
proof campaign merely to create another release checkbox. If root needs an
actual completed compact seal, it requires a separately justified finite input,
capacity/cost allowance and deadline; do not infer it from a prepare pass.

## Growth consequence and remaining risk

This materially lowers sealer **adoption** overhead and makes the same software
distribution able to produce owner-funded certified cuts. It does not reduce the actual
cryptographic proving work, guarantee affordability, add a payer market or make
seals automatic. The existing funded-cut theorem gains a concrete compact
execution route; its positive capacity/funding/demand premises remain real.

Sources read: FULL-SEALER-PATH; current agent03 workflow, stages, facade and
profile; full contributor profile; both installed driver/guest hashes. Tool
d78067 provides exact closure arithmetic and matched binaries. No product ran.
