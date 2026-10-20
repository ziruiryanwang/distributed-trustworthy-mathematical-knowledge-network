# Installed controller cost: selected synchronous pin-phase seam

2026-10-20. Source/evidence decision and implementation by core_search; root
owns source selection, independent review, actual runs and adoption.

## Actual failures and decision

The installed remote reader at
`product-local/v5-distribution-02/operations/relocated-remote-01` passed real
I/native admission, then failed during semantic import:
`AGGREGATE_CONTROLLER_CPU`, with 30.515625 controller CPU seconds against the
original 30-second cap. No A verification was performed.

The older successful public remote workflow at
`product-local/v5-client-owner-runs/client-remote-check-01` reached READY with
16.859375 controller CPU seconds (19.515625 whole known CPU). Each had ten
client calls. Their 81 selected v5 sources are exactly identical: 976,572
bytes, zero hash differences. Installation paths and concurrency differed.
This does not establish the proportion attributable to either factor.

The concurrent installed contributor reached READY input, then native
authoring failed because `Init.olean.server` was absent. That failure is not
a controller-limit or RAM failure; its complete Lean-support closure is a
separate core_growth/root assignment. Preserve both failures and budgets.

Source inspection identifies repeated immutable file hashing inside one
synchronous import validation. This is a directly removable operation count,
not an exclusive measured explanation of the observed regression. Select
that seam, not budget inflation, constructor pin-closure trimming, proof
reconstruction or memory tuning.

## Source-defined redundant work

`MixedImportSession._live` checks I, A and mixed owners. The mixed owner's
`_check` checks I and A again, plus its native/source pins. For one mixed
source, `_snapshot` calls `describe`, `members` (two `describe` calls) and
`export_packet` (one `describe`). Those four more descriptions each repeat
the mixed check. Thus this path executes six I, six A and five native pin-map
rounds. Every common SDK source pin is hashed seventeen times, in addition
to repeated supervisor pins and control-file reads. The current shared
81-source runtime map makes this nontrivial fixed controller work even for
a small mathematical packet.

The precise count depends on source kind, frontier and number of sources.
It is not a claim that every import or workflow has exactly this count, nor
that filesystem hashing is its only cost.

## Selected implementation and invariant

Fresh successors under `software/v5/runtime_efficient/` preserve actual
deployed module identities through root's source map:

| Deployed SDK key | Selected source relative to `runtime_efficient/` |
|---|---|
| `v5/admission/verifier.py` | `admission/verifier.py` |
| `v5/admission/pin_phase.py` | `admission/pin_phase.py` |
| `v5/mixed_claims/receiver.py` | `mixed_claims/receiver.py` |
| `v5/mixed_claims/imports_atomic.py` | `mixed_claims/imports_atomic.py` |

Before editing, exact byte copies were verified against these frozen originals:

| Original | Bytes | SHA-256 |
|---|---:|---|
| `admission/verifier.py` | 12381 | `9f77bd17abbf87d8f777c52c047d41cfbfd1b29078f29a173006ccad99839571` |
| `mixed_claims/receiver.py` | 24121 | `d292a966469402a24282e40377c8ac9c929504e38de7862aa9a6bd1b3ad3fb00` |
| `mixed_claims/imports_atomic.py` | 41903 | `8d5e77ea1a239c10bd745a2860080d4ea6c91e52f4da32c7f18562ca755c0ba8` |

Only `_live` enters a ContextVar-backed pin-validation phase. Its unchanged
validation body moves to `_live_phase`. That call graph is synchronous,
owner-only, with no subprocess, await, network request or user callback.
The phase shares only successful immutable installation/source pin checks.
The key is the already-canonical absolute path, exact byte-count/hash pair
and identical checker function. Conflicting expected pins/checkers refuse.
Failed comparisons are not cached.

Every original liveness, deadline, profile, source-origin, handle, journal,
mathematical and manifest/control-file check remains. Every cache access
also invokes the original session activity check before and after. Before a
successful phase return, all recorded pins are freshly hashed again with
activity checks between them. Exceptions discard the phase, revoke the
session through its existing exception boundary, and restore an enclosing
independent phase if any. No result persists across phases, public calls or
native boundaries.

The new helper must be explicitly pinned by each receipt owner; runtime
maps gain one source, not a new mathematical trust mechanism. Its loaded
module origin is checked. A owners inherit the same checked installation
mechanism; mixed owners separately pin/check its origin as well.

### Assurance statement and limit

Under the existing trusted, stable owner-controlled runtime/filesystem
premise, a successful phase establishes every required exact pin at first
use and successful exit. Identical intermediate hash checks add no new
stable-state fact. For a common pin requested seventeen times, successful
hash operations decrease to two. If a pin appears once, the phase performs
two checks; the saving is in shared repeated maps, not every individual row.
Memory is bounded by unique configured runtime pins, not theorem ancestry.

This deliberately does not preserve every transient historical sampling
instant. A malicious concurrent filesystem writer could change and restore
bytes between samples; neither this mechanism nor Windows process resource
limits supplies a hostile-code/filesystem sandbox. Dynamic data, receipt
authority, cryptographic verification, origin checks, manifest bytes and
owner control records are not cached.

## Finite evidence plan

`test_pin_phase.py` uses inert counters and AST reads, never native commands
or actual mathematical owners. Controls cover seventeen-to-two checks,
fresh next phases/public calls, final-sweep mutation, independent nesting,
exception restoration, exact-pin/checker conflicts, failure non-caching,
activity failure on hits/final exit, immutable expected snapshots and the
three actual integration seams. The output is `controls.json`.

No code was executed/imported by the author. Independent review and root's
single selected control execution remain necessary. After a pass, a fresh
installed workflow may evaluate whether the repaired method fits its
unchanged original caps; this note does not renew the failed operations,
claim a measured speedup, accept a release, or complete v5.
