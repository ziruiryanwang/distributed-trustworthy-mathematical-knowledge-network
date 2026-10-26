# Interpret the Std closure against existing recipient routes

2026-10-26. Source-only checklist; no local execution. References use `experiments/v5-local-checks/multi-source-package01/suite/assembled/package`
under canonical `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Ceilings are not predicted costs or proof of fit; actual-review authority is separate.

## First measure the right object

Let C be the selected full declaration-unit closure above the fixed basis, D its
units not already warranted in the recipient's exact chosen parent, and A the
complete-unit frontier of an explicitly selected compatible local module anchor.
Count indivisible mutual/inductive units, not theorem names. Record raw bytes,
decoded nodes, output names and edges per unit/batch/aggregate, plus exact IDs.
One large unit cannot be repaired by splitting its declarations across batches.
`reference/baseline_bundle.py:194,290` measures units and greedily batches whole units.
`installation/py/ordinary_admission.py:390` rejects partial groups/name conflicts.

## Capacity map

| Route / object | Existing default configuration ceiling |
|---|---|
| Inert unit envelope | 8 MiB; 2097152 total nodes; 65536 imports and inventory names; lower nested expression/name/depth limits also apply |
| Producer/bundle total | 8192 units, 64 MiB evidence, 20000000 nodes, 262144 names, 262144 edges, 16 MiB binding projection; manifest 2 MiB; at most 64 batches |
| One ordinary admission batch | 1024 units, 64 MiB, 2097152 nodes, 65536 names, 1048576 import edges; native-unit-array encoding also at most 64 MiB |
| One peer receive | At most 1024 units / 64 MiB total; each unit at most 8 MiB; at most 4096 missing name/identity pairs, 1025 preflights, 8192 requests / 1 GiB reply authorization |
| Cold module realization | At most 32 targets, 32 units / 4 MiB total and per unit, 131072 nodes, 4096 names, 32768 edges; encoded request at most 4 MiB |
| Anchored realization | Same limits on unanchored acquired delta; existing anchor chain at most 32 modules, 1024 units, 16384 names, 256 MiB artifact parts, 4 MiB plan/combined records |

Sources: `installation/py/ordinary_evidence.py:35`; `reference/baseline_bundle.py:42`;
`installation/py/ordinary_admission.py:366`; `peer_api.py:39`;
`authoring/py/module_closure.py:28`; `authoring/py/anchor_store.py:35`.
Receive explicitly chooses smaller-or-equal grants. Transport maxima: 1 MiB preview/locator and 8 MiB evidence
(`support/transport/http_provider.py:33`). Preview size can fail independently.
These numeric limits are policy/protocol boundaries, not mathematical invalidity.

## Admission and transfer are distinct

`intake-baseline` plans the whole manifest, then rereads/preflights/admit-checks
each batch against the last confirmed root (`reference/baseline_intake.py:160,257`).
Planning projections are not warrants. Exact already-warranted units are reused;
new D is kernel-checked. A later failure retains the confirmed prefix, not rollback.
Default reservations are 60 CPU seconds and 64 MiB snapshot per batch, including
a CPU reservation even for reused batches. Total grant must exceed all reservations
plus controller work; call spool reserves 130 MiB per new batch, capped at 2 GiB
(`baseline_intake.py:29,74,248`). A nominal 64-batch manifest need not fit this route.
Catalog/custody occupancy, root/name/operation quotas, snapshot sizes and exact
parent-plan metadata are additional prerequisites, checked before native calls.
Default catalog: 4096 roots, 8192 operations, 1048576 names, 16 MiB manifests, 1 GiB
per artifact/4 GiB total; not automatically the actual initialized store's limits
(`installation/py/local_catalog.py:79`; `baseline_intake.py:140,214`).

Peer `bounded-closure` collects one whole missing closure before one admission;
it does not consume the baseline manifest's batches (`peer_api.py:656,713,736`).
`selected-unit-only` fetches the selected whole unit and stops with
NEED_GROUNDED_PREMISES before ancestor requests if its parent lacks premises.
This is nonacceptance, not cheap cold success; alternate-source attempts and
failed fetches consume the same original grant.
Inert custody and another branch's acceptance do not supply chosen-parent warrants.

## What actually avoids proof replay on this Lean runtime

The Lean 4.34.0 fixed basis has 456 units/581 names, not all Init/Std. Admission
restores protected checked parents and checks new units (`ordinary_admission.py:550,565`; `installation/lean-src/OrdinaryWorkflowWorker.lean:204`).
This removes old kernel additions, not selected-lineage loading/metadata costs.

Cold module collection still fetches/parses C, including nonbasis installed Init
units; local acceptance alone is not an ordinary modern-module realization.
Native module creation imports installed Init or one registered anchor, never an
arbitrary Std module (`module/OrdinaryModule.lean:177,786`). Exact installed Init
collisions can be matched by full warranted private records; unmatched units are
checked privately and again under exported public imports. Public conversion
failure still refuses (`:361,798,805`). Installed Std existence alone is no cut.

Warm export cuts only A already recorded by this owner/support and warranted in
the current context (`anchor_store.py:417`; `module_closure.py:83,152,192`). It
rehashes selected artifact parts and validates every frontier binding; it does
not fetch/decode their old proof evidence. Zero delta can reuse without a native
call (`module_export.py:210`). Fresh delta still needs native checks and private/
public fresh-process rereads. Cold initialization cannot assume a free anchor.
An indivisible group larger than the delta ceiling cannot be grown in small pieces.
No arbitrary original-library-reference adoption is in this owner CLI
(`owner.py:40`); advisory authoring associations are not warrants.

## Mechanical decision checklist and honest cost comparison

1. Verify target identity and complete group/dependency closure; distinguish first
   exporter refusal from no exported result. Never infer counts from source lines.
2. Check per-unit syntax/census first, then aggregate/batch caps, actual recipient
   occupancy and total reserved CPU/spool.
3. For peer use, recompute D relative to the chosen parent; check preview, missing
   names, source/requests and repeated-preflight budgets, not only bytes/units.
4. For ordinary module use, measure C for cold or C cut at exact A for warm;
   inspect semantic/public-conversion restrictions separately from numeric fit.
5. Record cost honestly: catalog context walks selected lineage, revalidates its
   metadata and hashes artifacts once per owner process (`portable_catalog.py:492,529`).
   Repeated preflights reparse growing evidence; depth d may produce quadratic
   cumulative parsing, before actual kernel conversion/checking. No polynomial
   kernel-time bound or global-size-independent local-history cost follows.
6. Compare with ordinary approved Lean/Lake package import using the same math,
   caches and trust approval. Already-approved Std needs no inert re-export merely
   to use its theorem; ordinary packages also retain notation/tactics/extensions
   that this declaration interchange does not. Independent inert checking is a
   different assurance choice, not automatically the faster or better workflow.

Root reports std-export01 failed after native export: 2651 units/16226 edges,
1102333 scanNodes/38094420 unitBytes, writer 38154768 B; owner exhausted budget
while writing evidence, before a manifest. These reported totals exceed the
one-receive unit cap and warn against assuming cold-module fit. They do not prove
all recipient/anchor routes impossible; exact artifact/census review is separate.
No successful bundle/intake or automatic cap increase/next target is inferred.
