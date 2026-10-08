# U0 read-only feasibility preflight for the eight-entry reuse gate

2026-09-22. **Read-only, partial feasibility; NOT a launch clearance.** No
Python, Lean, service, product API call or native test ran. No preserved package,
state or evidence was changed. This supplements the prospective
[hierarchical-summary gate](2026-09-22-useful-reuse-next-gate.md).

## Exact eighth result

The historical independent consumer B [outcome](../../software/qualification/usefulness-consumer-B-01/OUTCOME.md)
records an accepted and locally published universal chunk theorem, with theorem
identifier
`84011823015820cc4d81ac720c871bb03b948b47b683edfc0e9f3e81988bed514ac808eb5c0b77`
and publication
`publication:362a26e090b2091bebc07d96b1f2db6e35350f5eaecde239e4ce0a6ef0beea9c`.
Its P1 sequence-3 entry in the retained [state projection](../../software/qualification/usefulness-consumer-B-01/STATE.json)
points to this *exact* package directory:

```text
E:\Distributed Trustworthy Mathematical Knowledge Network\product-local\usefulness-consumer-B-01\state\work\bbc6f06cac3c6993ab8c4144417a82ede214a6ea48c1105535fc31250429986c\packages\168ceffcf15c3eccbc33c998e39257f3232e7352ab8e40c437c12f658765dffd
```

The state projection is 124,194 bytes, SHA-256
`f535fa2e460362f36fa3bddb83ec1ad97da7a837ec28c4fd23de078c7bb35888`,
matching its independent audit. Its sequence-3 encoded entry is 2,938 bytes
and SHA-256 `6981d6725619b9e85a0480741c2b714530cddf2203b479cbc7f10cc1c9779c45`.
The directory currently has 20 files / 286,633 bytes. Its 2,901-byte
`manifest.json` rehashes to
`168ceffcf15c3eccbc33c998e39257f3232e7352ab8e40c437c12f658765dffd`.
The manifest lists 19 object files, including that theorem CID; its root is a
distinct replay-group identifier. The previous audit binds candidate, inverse,
retained package, native proof description, P1 entry and publication. This U0
read did **not** independently rehash/rederive every object or rerun admission;
the fresh fixture builder must pin the entire 20-file map, revalidate it and
preserve the historical bytes.

## Current one-pass offering path: fixture, not borrowed authority

The now locally qualified [one-pass candidate](../../deliverables/2026-09-22-onepass-peer-candidate/RESULTS.md)
changes only `peer_service.py` and `service_worker.py` relative to the paged
candidate; the mathematical codec and wire bundle format are unchanged. Its
documented [peer API](../../product-local/peer-service-source-01/PEER.md) and
source support a **static owner-selected evaluator fixture**:

1. In a *fresh* workspace, take the seven audited source packages from
   [corpus01](../../software/qualification/usefulness-corpus-01/OUTCOME.md)
   and the eighth P1 package above. Supply each package's exact manifest pin,
   descriptor ID and complete formal metadata from its authenticated old P1
   entry to the unchanged `peer_wire.build_view` constructor. Revalidate every
   package and metadata projection before including it; no hand-edited entry.
2. Use the selected one-pass `peer_service.serve(view, port, ready,
   session_seconds=...)` under a separately frozen process-tree supervisor.
   `serve` calls `load_view` before readiness and rehashes a requested page or
   bundle before sending it. The exact selected source supports this standalone
   route with the same wire-v2 catalog/page and bundle-v1 framing.
3. Each consumer uses ordinary `peer_find`/`peer_acquire`, and fresh native
   `admit`; static serving does not grant mathematical acceptance or change
   any product node's publication ledger.

This is a supported **transport/fixture** route, conditional on the evaluator's
explicit authority to make local copies of the eight existing artifacts. It is
not `manage host` for a product-committed view. `peer_wire.build_view` explicitly
requires its caller to authenticate sharing authority and grants none itself.
The old B node cannot simply be run under the new installation's owner worker:
`service_worker.validate_selection` demands a committed local publication row
and matching selected entry. On a fresh one-pass node, `expose` likewise
requires `require_published`; merely copying the old package does not create
that row. `replica_expose` can authorize one locally acquired exact entry but
its current selection shape is one entry, not the proposed eight-entry catalog.
Therefore a fresh one-pass **owner-hosted eight-result view is unresolved**
without legitimate resubmission/publication of the B theorem and the seven
background entries. Do not edit a database, forge a publication marker, or
call fixture supply product-hosted custody. The proposed gate should select
the static fixture path before launch, and its later new output can be served
through ordinary `publish`/`expose` on its actual one-pass node.

## Calculable size frontier, not a built v2 view

Wire bundle-v1 framing is 20 magic bytes, four manifest-length bytes and
eight length bytes per object. For B this is
`286,633 + 20 + 4 + 8×19 = 286,809` bytes, versus the 18-MiB individual
bundle ceiling. Corpus01's seven audited bundles total 2,022,215 bytes.
Thus the eight *distinct intended* bundle files total **2,309,024 bytes**, below
the 64-MiB retained-bundle ceiling by 64,799,840 bytes. Eight is below the
256-entry count ceiling and below 32 entries per page by count. If the v2
builder succeeds and each row fits, at most eight pages are needed, hence the
view's bundle + page + root + completion file bytes are bounded by
`2,309,024 + 8×65,536 + 65,536 + 4,096 = 2,902,944`, excluding copied
source packages, staging, receipts and filesystem overhead. Root plus eight
pages plus all eight bundles would use at most 17 successful GETs, below the
default 128-connection session count; time/CPU and failed calls can still
exhaust it.

**Unresolved:** no wire-v2 eight-entry catalog, page or bundle set has been
built or hashed here. The prior 18,550-byte root was wire v1, not a pin for a
new v2 root. The B framed length is calculated from current directory lengths,
not authenticated bundle output. Before dispatch, freeze a new complete input
map and run one bounded builder preparation; independently audit exact v2
catalog/pages/bundles, ordered descriptor and metadata projections, distinct
bundle digests, actual service readiness and complete charges. Byte-limited
page splitting and the 64-KiB root/page limits must be observed, not inferred
from the old root or the rough stock bound. No reordering after observing a
consumer response.

## Exact statement-only preflight route

The earlier [target-conformance plan](../../software/qualification/target-conformance-01/PLAN.md)
and [passing outcome](../../software/qualification/target-conformance-01/OUTCOME.md)
establish a usable diagnostic pattern: on a fresh node, configure; then five
ordinary requests in order—`init`, submit the fixed 207-byte `R` vocabulary,
publish it, admit its returned candidate, submit a **definition of the target
proposition family**, not a proof. Bind every request to its returned handle;
the target root is the declaration authored for the new hierarchical equation.
The old plan used four native stages and 552 MiB conservative reservation,
with full candidate/inverse native round trip. This is a historical resource
guide, not an automatic grant or proof that the new statement fits.

For the new statement, author and freeze exact Lean 4 UTF-8 source using the
checked receiving name of `R`, no B theorem reference and no proof. Prelaunch
review checks the generic triple-list type, both sides, law directions and
universe. On the qualified one-pass installation, run the same bounded
statement-only path once, under a fresh reviewed allocation. Compare its
canonical *value* DAG—not merely the declaration's `Prop` type—to the
predeclared formula. Derive the expected theorem type by converting the three
outer family lambdas to Pi binders, as the previous A/B audits did, and freeze
that exact canonical target before either agent sees a packet. If elaboration,
capture, inverse replay or exact identity fails, stop and retain the failure;
do not use a consumer arm to repair the formal target.

Remaining prelaunch decisions: owner authorization of local fixture copies,
final frozen corpus order and full file maps, source statement text and
independent canonical reviewer, exact supervision/retention grants, consumer
packets and cooperative information isolation. None is discharged by U0.
