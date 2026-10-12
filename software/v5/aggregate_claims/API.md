# Exact-warrant aggregate V2

Source-only candidate, not an adopted aggregate image, real aggregate receipt,
public receiver or v5 release. Rust/native control output remains conditional.
The exact existing mathematical module relation, legacy image I and 184-byte
module journals are unchanged. V1 aggregate sources and evidence are preserved.

## Why a second aggregate profile is necessary

ModuleID identifies the exported mathematical interface, whose theorem entries
omit proof terms. Rank records a checked derivation's direct-parent height.
Therefore different valid derivations of the **same** ModuleID can yield
different exact journals J0 and J1. Independent children may reference J0 and
J1 respectively. A graph keyed only by ModuleID rejects their honest union or
would have to rewrite exact certified premises. V2 instead preserves both.

Three identities must not be conflated:

- Semantic ModuleID M: share/discover identical interfaces and definitions.
- Exact warrant J[184]: choose the precise profile/rank conclusion supporting
  an already authored parent reference. J is not a unique proof-history ID.
- Aggregate receipt claim (A,H[192]): authenticate a bounded set of exact J
  warrants, then select a member using its commitment opening.

Duplicate exact J entries refuse. Same-M/different-J entries are permitted and
count separately against the member limit. No valid-looking rank is invented,
no semantic equivalence is inferred, and no existing parent J is substituted.
This is not a theorem-count growth mechanism: two warrant variants of one
ModuleID do not count as two new mathematical capabilities.

## Public Rust interface and authority

`relation::check_reader(Read)` and `check_bytes(&[u8])` still return a privately
constructed `ConditionalConclusion`, with unchanged getters:

- `header()`; `assumptions()` with exact `image()` / `journal()`;
- `members()`: exact 184-byte journals in strict full-byte lexicographic order;
- `census()`, `edges()`, `wire_bytes()`.

The production entry strict-parses a witness once through the path-reused
parse-once census, then invokes unchanged `module_relation::check(Value)`,
retaining both canonical-size passes. No checker callback, success flag or
caller-constructed conditional graph is accepted. Each returned exact parent
journal must already exist as a graph node. Rank and all mathematical
correspondence/kernel obligations remain checked by the unchanged relation.

The reused guest wrapper must verify **every** returned pending SDK claim with
`env::verify` before committing. A producer/receiver must fully resolve recursive
assumptions, disable proof-system dev mode, verify the adopted actual image A
and bind header.A=A. Structural header/membership functions alone confer no
mathematical authority. This library does not export an authoritative accepted
member token. V1 aggregate and legacy I-only receivers do not become V2 receivers.

## Header and commitment

The header is still exactly192 bytes, but begins `DMKNA002` followed by version2
as u32LE. Remaining fields and offsets are unchanged:

    magic[8], version:u32LE, A[32], I[32], foundation[32], policy[32],
    members_root[32], member_count:u32LE,
    maximum_member_rank:u64LE, seal_height:u64LE.

Image words are encoded as eight u32LE values. I remains
`9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e`.
Foundation and semantic policy remain the compiled relation's exact values.
A is nonzero and distinct from I, and the actual receiver must additionally
pin it. Count is1..48 exact warrants. Seal height is positive, distinct from
mathematical rank, and equals one plus the greatest imported aggregate height
(default prior maximum0), with overflow refused.

Sort the **full J bytes** lexicographically, not by ModuleID alone or numeric
rank. Rank uses little-endian bytes, so byte ordering is not rank ordering.
For n members, index i and SHA-256 H, the fresh domain-separated commitment is:

    leaf = H("DMKN-V5-AGGREGATE-V2\0LEAF\0" || u32LE(n) || u32LE(i) || J)
    node = H("DMKN-V5-AGGREGATE-V2\0NODE\0" || u32LE(n) || u32LE(level)
             || left[32] || right[32])
    root = H("DMKN-V5-AGGREGATE-V2\0ROOT\0" || u32LE(n) || top[32]).

Level0 combines leaves. Odd widths duplicate the final existing hash; a selected
odd final node's supplied sibling must equal its current hash. Paths have exact
depth, at most6 siblings. Index/count/rank/profile/root checks stay mandatory.
V1 roots/paths do not silently acquire V2 meaning.

## Wire V2

All integers are unsigned little endian; fixed fields use raw bytes.

1. `DMKNAI02`[8], version:u32=2, A[32].
2. Four u32 counts: assumptions, selected frontiers, deltas, targets.
3. Each assumption: tag0 plus exact legacy J[184], or tag1 plus prior V2 H[192].
4. Each frontier: assumption_index:u32, exact J[184], member_index:u32,
   sibling_count:u32 and that many32-byte hashes. Legacy claims require exact
   journal equality, index0 and no siblings; aggregate claims require membership.
5. Each target: **exact J[184]**, not ModuleID[32]. Validate its fixed legacy
   profile. Targets are unique, nonempty and must be newly checked deltas.
6. Each topologically ordered delta: witness_length:u32 plus that many ordinary
   witness bytes. No expected-success flag or substituted parent metadata.
7. Exact EOF.

Real receipt bodies remain separate genuine SDK assumption material. Unique
claims are keyed by exact `(image,journal)`. Several selected warrants may share
one prior aggregate receipt. The V2 decoder rejects V1 headers/framing rather
than guessing which ordering/target interpretation was intended.

Unchanged global caps:16MiB stream,8 assumptions,32 frontiers,16 deltas,48 exact
warrants,128 edges,250000 rows,8192 bodies,4096 group openings,500000 JSON Values
and depth128. The existing strict parser retains its potentially tighter depth
bound. Both per-frame and cumulative limits apply. A full-J target adds152 bytes
relative to V1's ID target; those bytes are charged to the unchanged total cap.

Frame size is checked before its byte-vector allocation. Strict JSON constructs
a bounded raw-input Value before the aggregate node census: there is no claim
of a node-before-every-allocation guarantee. Independent process memory/cycle/
output bounds remain necessary. A format maximum is not evidence that the
largest input can execute or be proved within a selected resource allowance.

## Exact graph and sound composition

The graph map key is J[184], and every edge/target is that same full key. On a
delta, use the actual relation-returned parent journals, require their exact
presence, strict rank decrease and the unchanged exact rank increment. The
unchanged local relation still refuses two direct parents with the same ModuleID
and a direct parent whose ModuleID equals the child's; V2 does not relax those
single-witness rules. It permits different branches to retain different warrants.

Every selected graph node must lie in a designated new target's backward exact
closure. Every declared assumption must support a selected frontier. Unused
variants, repeated exact journals, missing variants and ambiguous bare-ID
targets do not obtain automatic repair or substitution. They refuse.

Assume the pinned relation is a correct conditional mathematical extension
checker; the actual I/A recursive proof system is sound for the used branching
composition; and commitments bind their bytes. Induct on seal height for prior
aggregate premises, then on the topological order of new exact warrants. Every
new exact parent is established before use; the unchanged checker proves the
new conclusion. Thus every member J is valid under the stated foundation/policy.
Membership transfers that particular J, not any same-M replacement. This proof
does not need ModuleID-to-rank uniqueness or a globally synchronized ledger.

## Required consumer and host integration

An importer may store semantic groups/bodies by ModuleID while retaining all
exact warrant alternatives separately. A new local authoring operation may
explicitly choose one justified J per directly imported ModuleID. It must not
rewrite journals in already produced witnesses to match that choice. Sharing
semantic bytes is not sharing another process's acceptance authority.

The fresh aggregate host can use the unchanged `ConditionalConclusion` getter
interface, but must use V2 header/domain/framing interpretation, full-J targets
and the actual selected A. Old V1 capsules, headers, openings and byte-count
expectations are not compatible artifacts. No implicit in-place migration is
defined by this source.

The unchanged native test driver still emits
`DMKN_NATIVE_AGGREGATE_CONCLUSION_V1`: that is a diagnostic JSON field schema,
not the aggregate cryptographic profile. Its `header` now carries V2 bytes.
Status stays `CHECKED_CONDITIONAL_AGGREGATE_NOT_ADMISSION`; admission stays false.
It returns exact input hash/size, consumed wire bytes, header, pending claims,
all member journals/openings, edges and census. None is an aggregate receipt.

## Current verification boundary

Sixteen unexecuted unit groups cover V2 profile/framing/domain changes, exact
variant membership/graph/targets/caps, unchanged global census and the five
reviewed parse-once differential groups. Synthetic statements exercise graph
bookkeeping, not mathematical validity. A later independently selected native
comparison can reframe the retained actual two-delta packet, compare unchanged
J/census outputs plus V2 Python commitments, and refuse a wrong same-M exact
target and the retained invalid proof. No old binary/suite, reauthoring, guest,
proof or public deployment is needed for that changed-boundary check.
