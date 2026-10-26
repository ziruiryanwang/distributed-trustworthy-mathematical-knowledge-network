# Same-owner concurrency audit

2026-10-26. Source-only audit; no product import, experiment, native call,
state read or state mutation. Selection is the default source handoff in
`software/v5/ordinary_release_bundle/ADOPTION.md`, not the optional correlation
overlay. No same-owner authority race found. No new lock, scheduler or runtime
test is selected by this note.

## Concrete workflow and finding

Two local agents accidentally invoke supported public operations against the
same existing catalog: contribute/intake/receive/publish, or one of those while
finite serving is active. Serialization is enforced, not merely requested.
One process owns the catalog; the competing process fails opening it before it
can reserve or commit mathematical authority. This is an explicit refusal and
possible wasted setup effort, not a lost-update protocol.

The enforcement argument has these premises: selected Windows implementation,
ordinary owner-controlled files, no hostile administrator/replacement of the
lock file, and use of the public entrypoints rather than unsynchronized calls
into the trusted in-process API. This is not a security proof against hostile
local code or arbitrary storage failure.

## Source evidence

- `ordinary_native_package/owner.py:508-511` opens custody then
  `OrdinaryAdmission`; all state-bearing owner operations use this path.
  Its `finally` block at 612-620 closes the owner and custody. Owner-free
  `produce-baseline` is deliberately separate and creates no catalog warrant.
- `ordinary_sparse_access/peer.py:174-226` marks only advisory network
  operations state-free. Receive, publish and serve open that same admission
  object. The lock lasts through API cleanup (274-282).
- `ordinary_lean/ordinary_admission.py:496-515` delegates locking to
  `PortableCatalog.open` before admission-call setup and closes it on failure.
- `ordinary_lean/portable_catalog.py:185-200` validates/opens `owner.lock`,
  takes `msvcrt.LK_NBLCK` on its first byte, then opens the catalog database.
  The losing opener closes in the constructor's exception handler. It cannot
  mark another live operation interrupted: the reopen update at 238 is after
  lock acquisition. Existing-lock read/lock refusal is also possible and safe.
- `portable_catalog.py:637-686` binds the live grant and generated artifact,
  then inserts the new immutable root and operation status in one
  `BEGIN IMMEDIATE` transaction. A commit exception requires reopen rather
  than claiming rollback (772-779). Lock release is at close (786-794).
- `ordinary_authoring_offers/ordinary_acquisition.py:176-213` stores inert
  bytes/locators and quota counters in an immediate SQLite transaction. Opening
  custody before the catalog lock can incur SQLite contention or a refusal;
  custody is not mathematical authority. An overlapping failed public call is
  not promised to leave no diagnostic output or zero setup cost.
- `ordinary_sparse_access/peer_api.py:804-912` deliberately requires exclusive
  finite serving and keeps provider/index cleanup inside that call. The public
  entrypoint still owns the catalog lock when cleanup finishes or fails.

Two contributions can later extend the same explicit parent serially. They
produce separate checked roots; there is no single mutable HEAD whose second
write silently erases the first. This does not automatically merge the roots.

## Real limitation, without misclassifying it as corruption

Serve holds the owner lock throughout its lease (1..3600 seconds), including
cleanup. Consequently a serving owner cannot simultaneously contribute,
receive, publish or even run the locking status command. Operations refuse;
they are not queued, and fairness or eventual progress is not guaranteed.

The current workable route is short finite leases and explicit serialized
mutation/publication between them. A separate independently checked owner can
serve while another investigates, at the cost of transfer/checking and separate
state. Do not bypass the lock or copy mutable catalog files to obtain this.
Continuous read-serving alongside mutation would be a separate availability
design decision (e.g. immutable custody/index snapshots), not a correctness
repair justified by this audit. It should only be selected against a concrete
workflow requiring uninterrupted service.

The catalog lock is not a global mutex for every custody/index path. Different
catalogs can be configured with overlapping external custody/index stores;
direct API rehosting likewise requires caller-owned serialization, as the
serve docstring explicitly says. This audit does not infer stronger ownership
enforcement, consistency guarantees, or throughput for those configurations.

## Exact source identity and next decision

The following inspected source hashes match their roles in the default
package's `PROFILE.json` (metadata only; no executable loading):

| Source under `software/v5/` | SHA-256 |
|---|---|
| `ordinary_native_package/owner.py` | `56ef042f652fcb88cae7d16ab74883016a469e2e82777c1a173f842f5ef8245a` |
| `ordinary_sparse_access/peer.py` | `968d13e4c926b1520cba00502f3e98a87ffda7bdfefa0ec3fcf362c2d3efb655` |
| `ordinary_sparse_access/peer_api.py` | `48ec02f0ecf76f44d7ab64e6e029bdfb4f7ccb3aba8513711dd6b07952c917e9` |
| `ordinary_authoring_offers/ordinary_acquisition.py` | `d4599471b1285650876d53763c4a618a4dd5d7a953197954249052771a9df64f` |
| `ordinary_bounded_transport/http_provider.py` | `9288996fa1d4e737f500043cddfc1c7935d9b7830ac6638596b6f7f278f2add7` |

The pinned bounded-operations source map also matches
`ordinary_lean/portable_catalog.py` (`aeaf0c7d507baa6b63d401c432ca71557bf29b6b576b1f6cd8381e4e87c7473e`)
and `ordinary_lean/ordinary_admission.py`
(`9653a710a089393d189830a26aa8dd0723ee75859ce577d9713dae569b5e8575`).

No timing experiment is needed to decide whether serialization exists. If a
later change weakens lock scope to enable continuous serving, require a focused
two-process contention/cleanup control for that changed boundary, not another
native theorem campaign. This audit alone justifies neither that change nor a
full concurrency qualification.
