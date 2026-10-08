# Compact source-free sealer: independent assurance challenge

2026-10-06 15:05 UTC; `v4_central_reaudit`. Initial source-only assessment of
the proposed change, not clearance of a not-yet-written successor or runtime.
Root owns implementation selection and launch. Canonical workspace only.

## Why this is central, and the smallest adequate change

The compact agent03 receiver already contains the real adopted proof driver,
guest image, `prepare_seal`, staged `Session.capture/advance`, and
`finalize_bundle`. Source-free sealing is blocked by action-scoped installation
adoption, not by an absent proof backend: `RECEIVING_ACTIONS` excludes
`prepare-seal` and `advance`, so these actions demand absent authoring assets;
the receiving-only worker allowlist correctly forbids stage execution.

A fresh explicit source-free sealer action scope can remove the separate
full-authoring-installation requirement without adding an executable payload
or changing mathematical assurance. This is a consequential deployability
improvement for funded recurrent cuts. It does not reduce cryptographic proving
work, guarantee a profitable cut, or certify every native-valid fragment.

For context, the retained full contributor profile lists 12,398 assets totaling
2,345,416,272 bytes. Its old crypto-assets filter retains 602 assets totaling
98,878,367 bytes (metadata arithmetic, not another installed/executed product).
The current agent03 profile contains later additions and must be measured on
its own exact map, not assigned these historical byte figures.

Subsequently read scale's `COMPACT-SEALER-DECISION.md` in full and independently
recomputed current agent03 metadata: 606 crypto assets / **101,249,548 bytes**;
11,796 excluded authoring assets / **2,246,537,905 bytes**. Rehashed the actual
current and full driver and guest at both locations: equal respectively
`32356c4f1aa94d0cf1404e23eb092f2bdeb75ab3f88396e90ea88747a54db0a7`
and `3a3391d70d23659e62823c4fa5510bf5e797c4d21e5cf1b0070957ae592a8745`.
The zero-new-executable premise is therefore independently supported; it is not
merely an inference from a filename. Prospective decision is favorable.

## Subsequent cost/discriminator review

Independently read `COMPACT-SEALER-COST-DECISION.md` and the relevant actual
`rollover_policy.py` parser. The proposed funding formula is correct:

`Q(n,a,m) = 600*(m+1) + 300*(a+1) + 1800*(3*n+a-1) + 600`.

There are n segment, n lift, n-1 join and a resolve ordinary workers; finish
and final verify are two short workers. Preparation adds a distinct-frontier
verifications plus one snapshot; m advance calls plus preparation each charge
600 controller seconds. Conditional successful per-worker caps bound the booked
CPU, not serial wall time, storage feasibility or successful proving. Its sample
values (5700, 11100, 16500, 223800) are arithmetically correct. The old n=41,a=1
case exceeds the current 120000-second operation cap under this worst-case
envelope even though measured workers can consume less.

The fresh zero-frontier proposition
`forall P Q R : Prop, (Q -> R) -> (P -> Q) -> P -> R`
has the direct proof `fun P Q R g f p => g (f p)`. That is a valid distinct
small semantic discriminator for the native-fragment-to-guest-snapshot seam,
not discovery or empirical useful-growth evidence. Actual new graph/plan bytes
still require audit. A small term does not imply a small guest segment count;
the threshold and full original allowance must be selected before preparation.

The legacy advisor mismatch is real: its exact local fields omit `backend`,
and `segments` must be an integer at least one. It safely rejects the native-fast
backend with null segments. The mathematical recurrent-cut argument remains
conditional, but direct native-fast-to-advisor integration is not implemented
by that old script. Never coerce unknown guest segments to zero or strip backend
metadata. A selected state-aware successor, or explicitly documented manual
quotation, is necessary for that route. A compact sealer does not itself repair
the advisor or establish uniform cheap successful cuts.

## Conditional preservation argument

Let P be the adopted full sealer, Q the proposed compact action-scoped sealer,
and F the same inert proof fragment. Suppose:

1. Q uses exactly P's adopted guest image/relation, foundation, journal/bundle
   interpretation, driver and actual verification semantics.
2. F passes the unchanged exact-tree, aggregate-byte, packet/capsule, singleton
   proposition, exact rank, selected-member/full-journal and frontier checks.
3. Every loaded module and invoked worker lies in Q's independently adopted
   crypto closure, freshly rebound at the existing boundaries. No omitted
   authoring executable or source file is transitively used.
4. Q preserves P's durable intent/charge chain, fixed original operation
   budget/deadline, snapshot binding, dependency sequence, failed-state refusal,
   actual final cold verification and clean worker closure.
5. The owner supplies enough real resources for the selected finite operation.

Then removing unused authoring files does not change the fragment's accepted
mathematical proposition or make a weaker receipt transferable: successful Q
completion exports the same warrant kind under the same relation. This is a
source-level noninterference/composition argument, not a proved bound on worker
runtime. New orchestration bytes still require their own review and tests.

In particular, `last_verified` starts false in each invocation and must become
true by actual cold verification in the completing invocation. Persisted READY
state, a local native result, a snapshot, a stage checkpoint, a sender success
label or a handoff file is never a certificate. Finalize must preserve the
singleton capsule/journal/receipt binding and no-live-worker requirement.

## Changed-boundary obligations

- Define a separate immutable seal-action scope. Keep fast receiving and
  ordinary guest receiving command allowlists unchanged; do not permit `stage`
  merely because an action is source-free.
- For seal actions, permit only the adopted full driver's exact internally
  constructed `stage` and `verify` routes. Reject native authoring, arbitrary
  executables and all unselected entrypoints.
- Use the full crypto closure, not the native-fast hash subset: the actual
  guest and stage-capable driver must be hashed. Default/final rebind must not
  accidentally expand to missing authoring files or skip required crypto files.
- Exact selected files/directories, module pins, isolated Python and PATH
  remain enforced. No duplicate imports or peer-selected profile escape.
- `prepare-seal` binds actual fragment manifest hash and interface before
  snapshot; `advance` receives only existing operation and bounded stage count,
  never fresh budget/deadline. A changed profile does not authorize migrating
  old failed/full-profile operations into a fresh allowance.
- Preserve all CPU/wall/storage/process reservations and their distinction from
  observed cost. An unfunded READY prefix is deferred, not secretly renewed.
- The public facade must bind its new action to the adopted workflow/profile,
  close its entire process tree, and report mathematical status separately from
  clean command closure.

Minimum discriminating pure controls: seal stage/verify allowed; native,
foreign executable and inappropriate execute routes refused; receiving stage
still refused; missing/corrupt guest/driver refused; fixed crypto scope at final
rebind; no budget-renewal flags. Actual preparation can additionally distinguish
the missing-authoring installation seam. Repeating an unchanged complete proof
campaign solely to re-demonstrate the unchanged cryptographic relation is not
automatically warranted.

## Important limits

The selected `prepare_seal` consumes proposition proof fragments. It is not a
standalone direct-definition certification interface: recent D1/D2 local body
checks remain nontransferable. The compiler/native relation remains unchanged.
The actual wire supports exact bounded frontiers and selected 1/2-member journal
contexts; no ancestor proof replay is introduced. Requested semantic interfaces,
fresh proof checking and demanded definition computation remain real costs.

Removing adoption overhead reduces the A term in complete-cost economics;
the S term for a successful cut and M/F terms for custody, renewal and failure
remain. Profitable reuse is justified only when the same-service comparison
`sum(lower(a_i) - upper(b_i)) > upper(S + A + M + F)` actually has supported
premises. Do not count hypothetical demand or reservations as measured savings.

## Reviewed sources

Read actual agent03 `receiver/cert_workflow.py` action scopes, loader, module
and rebind logic, alongside retained full `prepare_seal`, `group_parents`,
`finalize_bundle`, and `cert_stages.py` sequence, dependency, reserve, capture,
invoke and completion code. `FULL-SEALER-PATH.md` records the previously adopted
full route. This checkpoint will need a delta review for actual successor bytes.
