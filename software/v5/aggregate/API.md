# Aggregate-DAG relation: source interface

Source-only, not a deployable certificate route. No aggregate guest image,
genuine aggregate receipt, host integration or receiver authority has yet been
selected or produced. All synthetic unit-test journals are structural fixtures,
not mathematical evidence. Existing module, checker and native delta bytes stay
unchanged.

## Purpose and trust boundary

One new aggregate execution checks a finite topological DAG of delta witnesses
against a genuine certified boundary. It returns one commitment to all supplied
members. This removes the requirement for a separate certificate at every new
intermediate delta. It does not remove checking/proving new mathematics, checking
needed definition semantics, or providing the receipt and selected openings.

`relation::check_reader(Read)` and `check_bytes(&[u8])` return a
`ConditionalConclusion`. Its construction is private, and it has getters for:

- `header()`: the conditional 192-byte header;
- `assumptions()`: every unique exact pending claim, with `image()` and
  `journal()` getters;
- `members()`: exact legacy 184-byte journals sorted by ModuleID;
- `census()`, `edges()`, `wire_bytes()`: finite submitted resource counts.

No checker/verification callback, receipt-valid flag, supplied successful native
trace or caller-created graph conclusion is accepted. The sole production delta
entry calls unchanged `dmkn_module_relation::relation::check_bytes`.

The guest `main.rs` must verify **every** pending claim with real `env::verify`
before committing `header.encode()`. A full producer/receiver must resolve all
recursive SDK assumptions, use the selected genuine receipt scheme with dev mode
disabled, verify the actual adopted image A and bind `header.aggregate_image=A`.
The old 184-byte I-only receiver cannot admit these new 192-byte A claims.

The library's header decoder and membership functions authenticate only a
structural commitment. An unverified header and opening can be fabricated and
carry no theorem authority. There is deliberately no `VerifiedAggregateMember`
in this crate. A genuine receiver requires separately selected implementation.

## Header bytes and commitment

The encoded header is exactly:

| Byte offsets | Content |
|---|---|
| 0..8 | ASCII `DMKNA001` |
| 8..12 | version 1, u32 little endian |
| 12..44 | aggregate image A, eight little-endian u32 words |
| 44..76 | fixed legacy relation image I, same image-word encoding |
| 76..108 | foundation digest |
| 108..140 | semantic policy digest |
| 140..172 | member root digest |
| 172..176 | member count, u32 little endian |
| 176..184 | maximum member mathematical rank, u64 little endian |
| 184..192 | aggregate recursive seal height, u64 little endian |

I is `9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e`.
The fixed foundation/policy come from the exact existing relation dependency.
A must be nonzero and different from I. Count is 1..48 and seal height is
positive. Rank and seal height are distinct: imported low-rank members can occur
inside earlier high-height aggregates. The new height is one plus the maximum
imported aggregate height (zero if none), with overflow refused.

For n sorted unique ModuleIDs, index i, exact J[184], and SHA-256 H:

    leaf = H("DMKN-V5-AGGREGATE\0LEAF\0" || u32LE(n) || u32LE(i) || J)
    node = H("DMKN-V5-AGGREGATE\0NODE\0" || u32LE(n) || u32LE(level)
             || left[32] || right[32])
    root = H("DMKN-V5-AGGREGATE\0ROOT\0" || u32LE(n) || top[32])

Level 0 combines leaves. At each odd-width level, duplicate the last existing
hash as its right sibling. A membership path must have exactly the tree depth,
at most six hashes. If a selected node is the unmatched final node at a level,
its supplied sibling must equal its current hash. Index, count, fixed member
profile, maximum-rank bound and final root are checked. A changed rank changes
leaf bytes even when its ModuleID is unchanged.

`membership::commitment`, `opening` and `verify` enforce this one exact scheme.
They do not infer that any committed member is mathematically valid.

## Stream encoding

All integer fields below are unsigned little endian. Fixed-size digests use raw
bytes; no JSON/hex receipt bodies or platform-dependent serialization occur.

1. `DMKNAI01`[8], version:u32=1, A[32].
2. Four u32 counts: assumptions, selected frontiers, new deltas, targets.
3. Each assumption: tag:u8=0 plus legacy J[184], or tag:u8=1 plus prior H[192].
4. Each selected frontier: assumption_index:u32, exact J[184], member_index:u32,
   sibling_count:u32, followed by that many 32-byte hashes. Legacy selections
   require member index zero, zero siblings and exact equality to their claim J.
5. Each target: ModuleID[32]. Targets are unique, nonempty and newly checked.
6. Each delta: witness_length:u32 followed by that many exact ordinary witness
   bytes. Process deltas in topological order. No expected-output flags.
7. Exact EOF.

Actual receipt bodies must be supplied separately through the genuine SDK
assumption mechanism. Claims are unique by exact `(image,journal)`; multiple
different selected members may share one genuine prior-aggregate claim.

Limits: entire stream 16 MiB, 8 claims, 32 selected frontiers, 16 deltas,
48 total members, 128 edges, 250,000 rows, 8,192 bodies, 4,096 imported group
openings, 500,000 JSON Values, depth 128. The retained strict JSON parser keeps
its own potentially stricter depth behavior. Every sum uses checked arithmetic.
There are no remote-selectable larger limits.

The frame length is checked against the remaining total wire budget **before
the witness byte vector is allocated**. The preliminary JSON census uses the
retained parser, which constructs its bounded raw-input tree before the global
node/depth census. It is not a node-budget-before-every-allocation guarantee.
That temporary tree drops before the unchanged mathematical relation parses the
same frame; only one witness is checked at a time. A separately enforced process
memory/cycle/output envelope is still necessary. Maximum accepted format size
is not evidence that it fits a selected guest execution/proof allocation.

## Graph and compositional argument

For each selected frontier, check its exact typed assumption descriptor and, if
needed, Merkle membership. For each actual new relation conclusion, require
every exact returned parent journal already present, strict exact mathematical
rank and no duplicate/conflicting ModuleID. Record edges from those actual
returned parents, never from independently supplied metadata.

Every supplied graph node must lie in the backward closure of at least one
designated new target. Every assumption must support at least one selected
frontier. Duplicate selected modules and unused frontiers/deltas/claims refuse.
The graph commits only this bounded closure, not the global mathematical corpus.

Subject to the pinned checker's conditional extension correctness, sound real
I/A recursive receipts, and commitment binding, induction on aggregate seal
height establishes the validity of frontier members. Induction on topological
delta order then establishes each new member. Membership transfers that
conclusion to a selected leaf only after genuine A-receipt verification.
The argument is conditional on the actual branching recursive proof system;
this source implementation does not independently prove that cryptosystem.

## Pending integration and controls

Source tests cover exact header/profile/length, image binding, count/rank,
odd-width membership and tampering, framing-before-payload-read, exact EOF,
duplicate/unused claims/selections/targets, seal-height overflow, global census,
missing/changed/unordered premises and full branching target closure. Private
graph tests fabricate structural conditional statements solely to exercise
bookkeeping, never as an alternative production checker.

No tests/builds were executed by the author. Root may later select narrow native
controls, using the actual corrected two-delta packet and retained current
checker library, then a finite guest feasibility screen. A new mixed I/A host,
fully resolved production route, real A member receiver, frontier/import
successor, custody and discovery descriptors are still necessary. Neither this
crate nor a passing structural test would justify a v5 release claim.
