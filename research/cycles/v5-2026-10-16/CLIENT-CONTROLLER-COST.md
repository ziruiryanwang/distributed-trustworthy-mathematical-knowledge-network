# Client03 controller cost: atomic materialization and a sealed view

2026-10-16, source-only diagnosis by `memo_independent_review`; canonical guard
PASS. No product/test execution, import, benchmark, implementation or Git change.
Recommendation: **new bulk materialization plus a one-way sealed selection**,
not a larger CPU cap, another seed proof, OS leases or a permanent validity cache.

## Reached boundary and evidence

Actual03's `work/actual-result.json` reports `DeltaError:MIXED_CONTROLLER_CPU`.
Consumer genuine I/native mixed admission succeeded; first import session began;
author calls and publications are zero. Consumer final observations are 97.875
controller CPU / 107.1816924 wall seconds, including the failure/cleanup tail.
The mixed owner's 90-second check is the refusing boundary. Observed successful
worker CPU is 0.046875 seconds; reserved worker CPU is 60. **No saved per-row
progress identifies the exact opening/check that failed.** Do not turn these
observations into timing fractions or claim the full path below executed.

Seed authoring/publication succeeded and must be reused:

| Item | Exact retained value |
|---|---|
| Module/root | `b42957064314b6667bf05cd3eec27ce39b925491c756a69f23a739d39ebb9f94` / `ClientV5.fusion` |
| Packet | 554165 bytes; SHA `92bbe15b0c8cfcba805efe86939009a9c0c53148e1c9fbd708d48fc6e0fe507f` |
| Publication | `1573252331936645f052074a5506189fbbd2162160d93d7617d208d4af8d3a75` |
| Index snapshot | `2b7c0199b33673fe3909489c01f71d36dc0cfcddd56ec3bc82d36b78294c65a5` |

Packet material is two warrants, 12 groups/15 declarations and 11 witness bodies:
11 base groups/14 declarations plus the fusion theorem. The independent
mathematical audit owns adoption of its actual proof edge.
Use `phases.seed.closed_client` for seed costs: 28.90625 CPU / 31.711686 wall.
Late `clients.seed` says 126.796875 CPU because reporting subtracts the original
process clock even after closure; that includes later consumer work, not new
seed computation. Preserve reports and avoid double counting.

## Exact source-count cause

`MixedDeltaVerifier._active` is cheap owner/profile/deadline/CPU checking.
Its `_check` additionally scans loaded origins, calls I `_check_install`,
hashes every native/source pin and reads its owner record. The I scan hashes
**83,807,520 runtime bytes**, including the **66,652,160-byte verifier host**,
plus three loaded supervisor sources and the manifest. `commons.pin` performs
full hashing and ancestor/path checks, not a cached metadata comparison.

For one stored mixed source, `MixedImportSession._live` calls:
I installation check; mixed check; then source `_snapshot`, whose
`describe + members(two describes) + export_packet(describe)` adds four mixed
checks. A group's `open_member_group` calls `describe_member` twice, each
calling `members` and therefore two more describes.

| Successful call, one mixed source/I owner | Mixed scans | I installation scans |
|---|---:|---:|
| Session `_live` | 5 | 6 |
| Select one warrant | 5 | 6 |
| Add new opening | 14 | 16 |
| Add new body | 10 | 12 |
| `selected_data / selection`, G groups | 10 + 4G | 12 + 4G |
| Ready `prepare_mixed_context`, G groups | 30 + 8G | 36 + 8G |

With G=12, B=11 and two selections, the hypothetical successful tail after source
insertion requires **414 mixed scans / 468 I scans**:
`2*5 + 12*14 + 11*10 + 126` and `2*6 + 12*16 + 11*12 + 132`.
The I runtime alone is 39,221,919,360 requested hashing bytes. This is a logical
source-count bound, **not actual03's completed count, physical disk traffic or
a runtime estimate**. Setup/source insertion adds further checks.

Later authoring repeats the problem: `MixedSourceOperation._active` calls
`require_selection -> selection -> selected_data`, reopening every group.
Preparation, finish and onward-packet production invoke these repeatedly.
Collapsing four describes to one helps only a coefficient; bulk import alone
also fails unless later selection/context operations use the new view.

## Selected principle: staged transaction, then opt-in one-way seal

Old unsealed incremental APIs remain unchanged. Add a bulk path:

1. Establish the live source handle with the existing authority API once.
   Accept the semantic batch only as bounded canonical **built-in bytes**:
   exact journals, openings and bodies; foundation has its own exact bytes/pin.
2. Full session `_live` at entry. Capture source/profile/state bindings and copy
   semantic maps into staged maps of immutable canonical bytes.
3. Apply the same commitment/summary, selected-warrant, duplicate/conflict,
   body-membership, byte/data/call and resource checks in record order.
   Retain cheap `_active` per logical item and all charges. Verify openings with
   `C.verify_group_opening` against the exact journal's already-bound summary,
   without asking the owner to rescan its installation for each group.
4. Use a shared **pure** context helper extracted from existing authoring:
   foundation validation, references/closure, body demands, topological order
   and canonical output bounds are unchanged. No filesystem, dynamic loading,
   await, process launch, custom iterator/record or external callback occurs.
5. Full `_live` at exit; require original authority/state unchanged and check
   remaining resources. Only after all fallible checks publish staged state.
   Exception closes/discards pending state; charges are never rolled back.
6. READY commits **and seals** semantic state, issuing an exact-session opaque
   view of canonical selected items/context/binding. NEED may commit validated
   incremental data after exit checks but remains unsealed/extendable and issues
   no sealed view or ready-authority token. Existing pre-ready context bindings
   still must be checked by `extend_context`.
7. After sealing, refuse every semantic mutation: `_direct` (I/A source),
   `use_delta_handle`, `_merge`, `select_warrant`, `open_group`,
   `supply_body` and another batch; guard internal commit points too.
   Counters/liveness/close remain operative. Further development uses a new
   session over live owners within remaining budget, not a renewed grant.
8. New authoring uses the view for context, selection and onward packet work,
   with full live-owner checks at public boundaries and detached return data,
   never old per-group reopening. Preserve fresh full installation/authority
   checks before/after native Lean and final child return. A view is not a
   mathematical receipt and cannot be serialized/copied into authority.

Choose sealing over mutation-generation bookkeeping:
`representation_revision` ignores added sources/nodes, selections, groups and
bodies. It alone cannot validate a cache. The one-way seal forbids **all** such
writes after READY; the exact live session/owner registry owns immutable view
bytes. Close/revocation invalidates the view. Existing unsealed
change-and-reversal behavior remains. Do not expose “skip checks” flags or
monkeypatch `_live`.

| Smallest source successor | Required seam |
|---|---|
| `mixed_claims/imports.py` | Staged state/atomic commit; opt-in seal and all mutation guards; same-session view registry and pure onward data |
| `mixed_claims/authoring.py` | Shared pure context builder; transaction orchestration; explicit view-backed source-operation path at every later selection site |
| `client/workspace.py` | Bulk call; READY view vs NEED context; route authoring through new view |
| Focused structural controls | Boundary/refusal/charge checks and counted pin invocations, no timing/proof campaign |

No receiver/native/checker change is required in principle. With S retained
sources, F installation validation, V selected bytes and D necessary traversal,
each public boundary has `O(S*F + V + D)` work: no G/B installation-scan
multiplier. Semantic cost is still real; there is no constant-time or measured
speedup claim.

## Assurance distinction and implementation blocker

**This is not equivalence of old transient filesystem sampling.** A concurrent
writer could mutate a pin after entry, an old inner scan could detect it, and
the writer could restore it before exit. Removing that scan changes that refusal
trace. Size/mtime caching does not solve it; exact trace equivalence needs an
independently justified immutable lease or continued scanning.

The new contract is instead a synchronous, serialized trusted-owner operation:
loaded code is not reread/executed from disk inside its pure section; input
mathematics is immutable; no result commits before fresh exit validation.
Maintain every live-origin/profile/close/deadline/CPU, exact-J and semantic
refusal. Native boundaries remain fresh. This establishes the relevant safety
argument, not detection of every transient local edit at every historical instant.
Existing contracts already trust the local controller/installation; no claim
of a hostile-Python sandbox follows.

**Open implementation gate:** independently review READY/NEED transaction
semantics, complete mutator guard coverage, pure-helper output equivalence,
opaque-view ownership, and all later authoring/finish/onward uses. Source
selection and targeted tests must precede actual continuation. No CPU-cap
increase or runtime is authorized by this note.

## Economical continuation

Preserve all actual03 bytes. Use a verified fresh copy of its closed consumer
workspace, or a fresh workspace populated via structural packet custody with
the exact retained packet. Do not renew grants in actual03's SQLite files.
A fresh `admit_local` must genuinely verify that packet; saved successful
reports/closed handles are not authority. Then exercise bulk import, the
still-unproduced projection, actual exported fusion edge, publication and
fresh post-owner/provider-closure readmission as separately selected.

Do not reauthor/publish the seed or rerun successful DHT discovery for this local
seam. If a later integrated test needs a provider, serve a fresh copy of the
retained publication with its exact identities. Count original creation and
failed attempts in total cost. Target controls: old/new immutable output
equivalence; entry/final owner failure; atomic failure with retained charges;
NEED extension; all sealed mutator refusals; foreign/copied views; expiry/close;
and malformed openings/bodies. Pin-call counters prove multiplier removal.

Source anchors: receiver `d292a966`; imports `50b09b08`; authoring `8b09cb1b`;
workspace `dbf6004d`; I verifier `9f77bd17` (SHA-256 prefixes of unchanged
`software/v5/` files inspected here). Exact source pins are also retained in
actual03's selected source snapshot/plan.
