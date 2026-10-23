# One public ordinary-peer reciprocal boundary

2026-10-23. Source-only harness/checkpoint by `ordinary_api_flow`; canonical guard
PASS. No script import, CLI, native operation, service or test was run. Used
package/API sources remain frozen. Root owns exact selection, launch and adoption.

## Exact candidate and existing inputs

New `software/v5/ordinary_peer_package/reciprocal_check.py`:
SHA-256 `b89cc7d6f7f2e51d036e55d99a6ef4874181a6b284a957b4d073efb741e7af3c`.
Its arguments are only `--package`, `--profile-sha256`, `--output`; it uses
selected `D:\Python314\python.exe` and the canonical Lean 4.34.0 runtime.
It imports only Python standard library, never private/product APIs.

Root's file-only assembly produced
`experiments/v5-local-checks/ordinary-peer-package-assembly-01/package`, profile
`06649545f962e8ca95b21ab1c87626444bdc06c16e5191b96a8f27e7766505e5`.
Native implementation remains
`fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df`.
The harness checks supplied profile bytes and every public result's implementation.
Root's frozen select_validation.py selects exact package/runtime/source pins.

Existing A remains `ordinary-package-lifecycle-01` catalog/custody, store
`7becc8b2d689d7240c791c44f22599bb22cee92bf6da097c2a028b535c5a0b5c`, root
`b5632acbab2d88f5e66436bc9bd7e4a47578ab6f41e35ecb20f9b2e00c0fb334`.
The retained continuation report is pinned to
`81b70c4894fe218dc7daf890c37cf4a51810a7517294d9881a2884b9c90066e7`.
It selects `CommonsPackageExample.applyTwice_eq`, ExportID
`bb47ce4786c4f5c22505952133e5220c0650452fb0006c83a395de131fee1355`, UnitID
`c4639e6e5f70e259ea1611adba8e168aa74dbfb91f98e2512cd465f82705e61e`.
Its actual evidence imports the definition ExportID
`b5054e3c29436f1fe8d175b47df405405f76683d7c1e27531d9e597f2e55ee02`, UnitID
`25ae588e95228a64196a576aa9c9dd78249c23b0c26189c5671a434b93afa1b3`.

The saved report is target selection, never acceptance authority. Public publish
checks actual protected A bindings; B performs fresh native admission. Before
operations, the harness checks retained source/evidence/preview hashes against
the exact continuation record and takes a bounded before-map of A's catalog,
custody and selected source/evidence. It requires an identical after-map. Nothing
under A or its continuation is copied, rewritten or deleted. All new indexes,
configs, logs, caller source, B state and results are under the fresh output root.
The output must be disjoint from both old roots and the selected package.

## Nine public commands, no extra campaign

1. A `peer publish`: one existing theorem into a fresh index; definition remains
   available through A custody's exact locator/evidence route, not in that index.
2. B `owner init`: initialize one genuinely new receiver once, before A's lease
   starts. This is necessary setup, not replay of an already initialized owner.
3. A `peer serve`: selected entire custody/fresh index, loopback, 45-second lease.
   The public CLI holds A's existing owner lock through cleanup.
4. B `peer find`: only ordinary-export/theorem features, no target/snapshot IDs.
   The controlled fresh index has one result; expected identity is checked only
   after discovery. This is a boundary test, not a retrieval-quality benchmark.
5. B `peer receive`: use the returned selection and new B parent. Require actual
   missing-definition frontier, two exact acquired units, READY then native
   CHECKED admission. No preview/index/status string is promoted into acceptance.
6. After A's natural lease and clean stop, B `owner contribute` authors one new
   theorem using the acquired theorem twice. No new definition/export opacity.
7. B `peer publish`: index the new exact locally accepted target in a fresh index.
8. B `peer serve`: 15-second finite lease, same explicit whole-custody scope.
9. Cold C `peer find`: no C owner, basis or custody; discover B's new target by the
   same ID-free feature query. Wait for B's natural clean stop. C has metadata
   discovery only, not acquired evidence or mathematical acceptance.

No competing same-owner-lock refusal test is added. The pure controls mock owner
binding and do not acquire that lock. Lock lifetime is source-reviewed; the
normal service lifecycle is exercised here, while competing same-owner refusal
remains untested. No C initialization is justified solely for this demonstration.
The existing lower-level inert acquisition evidence remains separate and is reused.

## Exact source argument before runtime

Let `T = CommonsPackageExample.applyTwice`. The selected law is
`applyTwice_eq {a : Type u} (f : a -> a) (x : a) : T f x = f (f x)`.
The new source declares `universe u` and proves
`T f (T f x) = f (f (f (f x)))` by:

1. `@applyTwice_eq a f (T f x)` gives `T f (T f x) = f (f (T f x))`.
2. `congrArg (fun y : a => f (f y)) (@applyTwice_eq a f x)` gives
   `f (f (T f x)) = f (f (f (f x)))`.
3. `Eq.trans` joins those exact terms. Both applications supply `a`, `f` and `x`
   explicitly; no result-guided operand inference or unfolding of T is needed.

Independent reviewer agrees with this source argument. Read-only inspection
confirmed both `Eq.trans` and `congrArg` in the exact package's 581-name inventory;
the harness also checks this before spending native work. The source is a fixed
reviewed byte string, and the new returned evidence must actually import the
acquired theorem's ExportID. This is not executed qualification or novelty.

## One original resource envelope and closure

Frozen selector envelope: 240 wall seconds, 160 CPU seconds, 2048 MiB, 10 processes.
Harness original lifetime is at most 210 seconds: work stops at 190, leaving 20
for cleanup/reporting. Accounted CPU cap is 145 seconds. Every subordinate wall
grant is clipped to original remaining work time minus five seconds. Completed
successful child controller+worker costs are charged once; failed/unknown calls
keep the whole reserved CPU cap. Concurrent service CPU caps remain reserved
until their terminal reports. The enclosing Job is actual aggregate authority.

Largest native grants: new B init 85 wall/60 CPU/1536 MiB; receive 65/45/1536;
contribute 70/50/1536, all further clipped by original remaining allowance.
A service is 65/8/256 with lease45; B service40/8/256 with lease15. Each reserves
ten seconds for its API cleanup. Find is <=45/8/256; publish <=45/12/512.
The only native/service overlap is receiver1536 plus service256 within outer2048.
Both find sessions cap requests4/pages2/examined32/candidates8/replies1 MiB and
10-second search time. Receive caps requests12/replies4 MiB/units4/evidence4 MiB/
missing4/preflights4, so no unbounded dependency or provider walk exists.

Each command/config is saved fresh with exact config hash, stdout/stderr and
terminal receipt. Ready polling is bounded to15 seconds; logs are sampled under
finite caps. No command retries. A failing command preserves every prior result
and accepted B state. Cleanup targets only exact child handles launched here;
forced termination is failure, never a clean-service claim. The outer Job must
independently establish final descendant quiescence. No broad process killing,
application intervention, external deployment or file deletion is involved.

PASS requires the actual nine-command path, both clean natural service stops,
two-unit B receiving admission, one-unit B contribution, exact returned ID, A's
unchanged retained map, original final limits and the outer clean Job outcome.
The endpoint is public local operability, not independent-host deployment,
complete discovery, safe arbitrary-project execution, useful-growth advantage,
ancestry-free cold ordinary checking, or completion of final v5.
