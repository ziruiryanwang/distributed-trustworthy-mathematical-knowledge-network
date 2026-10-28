# Dedicated inert host: independent review

2026-10-28. **Design and changed-boundary source review PASS.**
This checkpoint is source-only. No product imports, owner-state reads, database
connections, services, native checks, tests or Git operations were performed.

Reviewed contract: `2a78b97140c8d4da7ae7b9a439ac00142c554b08ac11762fb41624af05a595fb`.
Data-path note: `5f494814ae36c6b3ea60b711a37d78aec0716fcb00a2b28fd36b0ff81318c954`.
Implementation note: `daa077e4655943b1e9d9507bf321b03bf739aaa38a1468d85d5a1fa67b7e0880`.
The contract's helper signature now matches the reviewed synchronous implementation;
the asynchronous SDK stays unchanged.

| Reviewed source | SHA-256 |
|---|---|
| `custodian.py` | `63c500ce84e6f1bb0459645d93a6bb84b75efc30958b5e6eabcb8623a343daef` |
| `host.py` | `2a6f43fc1e2d36d2720374ab945aae95c06f4df5b934a12cbe073fb5b5b03a36` |
| `run.py` | `3ab60e82b00cc89caffa6e04e67ed387d39baa8e94d9d5c9cb1e93ba2cd25c50` |
| `profile.py` | `176a489ecd9211aa1cae38345f2f8dffd6f57500d52d4ab638f65def9003fd32` |
| `owner.py` | `ee78fc2430ad52ed77d468b86673db2c8671cf48518afb1f2a28288959c80aaa` |

These are source-review pins, not a constructed package or permission to reuse an
old execution allocation. Root owns exact assembly, targeted controls and actual
selection. No new native proof campaign is warranted by this role.

## Why this role is sound and useful

Availability and indexing do not require the host to accept mathematics. The
existing ordinary custody store validates exact bounded inert evidence; preview
and index code bind selected exported names to those bytes. The existing
`peer_api.serve(loaded, custody, ...)` expressly supports owner-free hosting when
the caller serializes access. Recipients still perform unchanged acquisition,
identity, dependency and mathematical checks. No new protocol, native checker,
foundation setup, global ledger or owner migration is necessary for this role.

The prepared bundle need not contain its full dependency closure. All stored unit
bytes and generated locators are addressable, even when only some exports are
indexed. The contract correctly requires explicit whole-bundle disclosure and
retains the inert assurance in seals and reports. Neither hosting nor an index
record becomes evidence of theorem truth or complete dependency availability.

The final contract selects embedded, uniquely identified targets (one to 64)
pinned by the exact prepare config. This supersedes DATA-PATH's earlier separate
target-file suggestion. No separate target-file mechanism is needed. Existing
per-batch validators must still accumulate all operation-wide census limits.

## Exclusion and lifecycle argument

The fixed marker `DMKN-DEDICATED-HOST.json` is written before either fresh store
exists. The exact one-byte `host.lock` is never deleted/recreated to bypass
contention; every prepare/serve holds its offset-zero exclusive OS lock until
all owned handles and provider tasks are closed. A fresh prepare cannot silently
adopt an owner's preexisting custody. Ancestor state-marker checks, fixed children
and explicit path disjointness give a practical conservative boundary without a
global registry or directory scan.

A marker alone is not exclusion. The current owner successor rejects any supplied
path with a marker-bearing ancestor before its pairwise separation checks, and
separately guards producer output before `produce_bundle`. Source inspection
confirms ordinary owner state/output, peer state/index/output and query paths use
that shared seam. The launcher additionally guards diagnostics and writable
arguments, including peer config's indirect index, before creating diagnostics.
Its host-root exemption is limited to the parsed dedicated host entry; it does
not exempt external outputs or expose a generic bypass to ordinary commands.

Marker-before-store creation, fresh constructors and delayed seal publication
prevent a failed racing preparation from being advertised as a complete mixed
generation. The guard denies marker existence regardless of content and fails
on unexpected path errors. Known aliases remain subject to existing ordinary-path
validation. These are supported-command guarantees under protected local storage.
Old executables, arbitrary same-user SDK calls and approved source with arbitrary
filesystem effects remain outside them. The contract correctly makes no sandbox
or OS-principal isolation claim.

Preparation installs `HOST.json` only after final input/profile validation and
successful index/custody closure, while still holding the root lock. A late report
failure retains the seal and records uncertainty; it cannot trigger automatic
serve. Serve separately selects that exact seal hash, revalidates the fixed marker
and identities, and holds the same lock through status checks, listener lifetime
and all cleanup. Preparation readiness and each invocation's listening READY are
different facts; a stale READY file is not current listener evidence.

## Source implementation and exact status checks

The final schema seals actual custody `objects/exports/logical_bytes` and index
`latest/objects` values. Those have existing bounded status APIs. Units and raw
evidence-byte totals are report accounting, not fictitious store-status fields.
Preopening the index to compare those values and then closing it before the
existing SDK serve opens it is sound under the same continuously held root lock.
No new full-database hash, persisted native snapshot or direct SQL mechanism is
required. SQLite reopen/configuration/recovery effects mean logical content is
fixed, not that filesystem access is read-only.

The helper implements the selected bounded data path using the actual selected
`ordinary_multi_source/peer_api.py`, `ordinary_acquisition.py`,
`ordinary_sparse_access/discovery_store.py`, `ordinary_lean/portable_preview.py`
and baseline manifest/batch readers. Their call signatures and return shapes were
cross-checked against the helper: evidence identity/hash/length, exact evidence
and preview readback, target locator, admitted record and snapshot identity all
match. Per-batch structural censuses are accumulated under the existing global
limits. Targets are distinct by export identity, present in the selected bundle
and bound to the actual preview. No complete dependency closure is inferred.

Both store closures are attempted even when insertion or another close fails.
The seal is published only after successful closure and final manifest, marker,
config and profile checks. Errors retain partial stores and distinguish whether
seal publication was attempted or completed. Serve validates the exact seal,
limits and actual status values under the root lock; it closes its preflight
index before the existing SDK reopens that index. Success follows SDK closure,
custody closure, final validation and root-lock release. Uncertain cleanup remains
a failure even if a later phase closes some resources successfully.

Three draft issues were corrected before execution:

- The public helper is now synchronous and calls `asyncio.run(api.serve(...))`
  **inside** the held host lock. The previous asynchronous wrapper could release
  that lock before the outer runner cancelled/drained surviving provider tasks
  on SDK cleanup failure. Runner shutdown now precedes custody close and lock
  release; a stuck drain remains subject to the original outer Job allowance.
- Config and seal parsing use the existing general compact/strict JSON codec,
  which accepts the required booleans and nullable TLS value. The mathematical
  writer codec's narrower token grammar was unsuitable here.
- Recognized ancestor state checks use `lstat`, catching only `FileNotFoundError`.
  Unexpected permission/path errors propagate rather than being treated as absence
  by `lexists`.

The root wrapper captures and rechecks exact config bytes, pins the helper before
executing it, keeps outputs separate from H/support and checks bundle/manifest or
TLS input overlap before creating output. It writes READY only from the SDK's
actual listening callback. Its final report preserves nested helper failures.
The launcher checks indirect peer index paths before diagnostics creation, adds
only the dedicated host entry and exact host-root exemption, and keeps its prior
whole-process supervision. The profile change adds the two required auxiliary
payloads; it changes neither mathematical IDs nor native installation semantics.

The retained-data ACTUAL-PLAN is an appropriate next integration discriminator:
one fresh inert host generation followed by ordinary find/preview/inspect without
owner setup. Its known-data success would not establish new growth, internet
operation or full v5 completion. Actual package pins and results still need their
separate root selection and saved-outcome assessment. No performance conclusion
follows from this source review.

This is a focused role separation, not a new mathematical acceptance architecture.
Small tests of the changed lifecycle are appropriate after source review; a new
proof campaign, broad benchmark or repeated mathematics experiment is unnecessary.
