# Compact witness transport: a comparative fallback

2026-10-12. Source/theory only; no implementation, import, build, test or guest
execution. **Not selected.** Root is first pursuing the smaller no-wire-change
strict-JSON length/validation-token seam. Base owns actual saved-profile
interpretation and checker-validation work; neither is repeated here.

## Decision

The smallest binary alternative is a **lossless typed encoding of the existing
`serde_json::Value` algebra**, decoded to that same Value before the unchanged
`module_relation::check(Value)`. It changes lexical transport, not mathematical
expressions, proof rules, semantic identities or commitment algorithms. Do not
start by replacing the checker with a typed arena.

This can remove JSON punctuation/escape/decimal-number parsing from the guest's
input path. It does **not** remove Value allocation, map insertion, structural
traversal, canonical hashing, correspondence, native DAG construction or proof
checking. It needs a new wire version, guest image and certificate production.
Prefer the smaller selected optimization unless its remaining cost makes these
changes worthwhile. No compression ratio or speedup has been measured here.

## Exact present boundary

`aggregate_claims/relation.rs` reads one length-delimited JSON witness, calls
`aggregate_parse_once/census.rs::Census::charge`, then
`modules/receipt/src/relation.rs::check`. The first strict-parses and performs
`canonical_size` plus aggregate census; `check` repeats `canonical_size` before
the same bound relation. `input.rs::extract` moves the Value's large fields
without reparsing JSON; map and positional-array records are both accepted.

The actual selected parser is **serde_json1.0.151**, not the older1.0.143 cache:

`E:\Distributed Trustworthy Mathematical Knowledge Network\experiments\v5-local-checks\aggregate-guest-compile-01\cargo-home\registry\src\index.crates.io-1949cf8c6b5b557f\serde_json-1.0.151\src\de.rs`

It is86840bytes, SHA256
`4998d7e252eb513be85b298e287048b4fb283882e9ba7df905f572f07200f3f3`.
Lines63,1372–1385 and1433–1456 initialize depth128, decrement before entering
each array/object, refuse at zero, and restore on exit. Thus at most127
simultaneously open containers are accepted. This is **not** identical to the
aggregate visitor's Value-depth128 check. Both limits must remain explicit.

Source anchors inspected, before any proposed change:

| File under `software/v5` | SHA256 |
|---|---|
| `aggregate_claims/relation.rs` | `698e0e1bfacdad37fe1720881b2034083b357a2fbeef7b233d83e2f7c1eb6a49` |
| `aggregate_claims/wire.rs` | `b3aa350bc0883a5a958ec67d856fb82183c65c9ff56ca9992f7d8e039c3859d8` |
| `aggregate_parse_once/census.rs` | `88e9796bbb5493187f541d40e7c777afa8bfd4059929a9a2a1f118cfae815b04` |
| `modules/receipt/src/canonical.rs` | `23ca5fa1bfe536db08136bef9956426e4d43e90fa36d00a1886e97eef6892d9b` |
| `modules/receipt/src/relation.rs` | `3625bc9c7708e5a03580e1e61bc7019f5b7cf6ad48ee37f6d749919d245e2eb8` |
| `modules/receipt/src/input.rs` | `4b5da4aefeef4ca7dc2ce3d2bd10cd0f270a3d5682f2ea16d8ea2e37c63bfa46` |

## Candidate grammar, with no hidden semantic normalization

One small possible encoding, not an adopted protocol:

| Tag | Payload and decoded Value |
|---|---|
| `00..7f` | Inline unsigned integer0..127 |
| `80` | Minimal unsigned LEB128 integer128..u64::MAX |
| `81`,`82`,`83` | Null, false, true respectively |
| `84` | Minimal byte length, then exact valid UTF-8 string bytes |
| `85` | Minimal array length, then that many encoded Values |
| `86` | Minimal object length, then length-prefixed UTF-8 key and encoded Value per entry |

All other tags refuse. Every LEB128 has at most10bytes, refuses overflow before
shift/add, refuses redundant leading high zero groups and has a terminating
byte; lengths additionally fit u32 and the remaining selected budgets before
conversion to target `usize`. A zero-length string/collection is valid; semantic
rules still decide whether it is allowed in a particular field. Integer values
remain u64, never floats, negatives, negative zero or booleans coerced to integers.

Object keys must be strictly increasing under Rust `str` order. This refuses
duplicates before map insertion; valid UTF-8 byte order agrees with that order.
Keep exact strings, including embedded controls/null and Unicode scalar values;
do not normalize Unicode, rename keys, trim strings, infer omitted fields, turn
arrays into maps or specialize mathematical expressions. JSON's escaped spelling
is representation only; decode/reencode preserves its string value. Invalid UTF-8
and isolated surrogate encodings refuse. Exact container lengths and exact frame
EOF prevent trailing or concatenated values from being ignored.

There are no backreferences, dictionaries, default fields or general decompressor
in this smallest proposal. They would add distinct expansion/aliasing obligations.
It is compact for many short integers and collections, but a long unescaped
string can gain length-prefix overhead. All repeated field names, full strings
and repeated subtrees remain present; this is not generic compression.

## Correspondence argument

Let `P` be the existing strict integer-only JSON parser, `C` its existing canonical
encoder, `E` the proposed deterministic encoder, and `D` the checked binary
decoder. Values have only null, bool, u64, valid UTF-8 string, arrays and finite
unique-key maps. Let `V` satisfy the existing structure/canonical-size limits and
the127-container limit. The following are mathematical specification lemmas,
not yet machine-checked implementation theorems:

1. **Value round trip:** `D(E(V)) = V`, when both selected byte envelopes fit.
   Structural induction suffices. Primitive tags preserve exact types/values;
   length fields identify exact string and child extents; induction preserves
   ordered array children; sorted unique keys identify exactly the original map.
   Minimal integers and lengths plus ordered keys make the encoding unique.
2. **Old-parser witness:** for every accepted binary frame `b`,
   `P(C(D(b))) = D(b)`. Canonical unsigned decimal is parsed as u64; canonical
   strings round-trip through the strict UTF-8/escape parser; object keys are
   unique; container nesting stays below the actual parser's refusal boundary.
   The existing canonical byte limit guarantees the old parser's raw byte bound.
3. **Mathematical relation preservation:** calling the unchanged deterministic
   `check` with equal Values gives the same success conclusion or mathematical
   refusal. In particular the same spec, canonical commitment bytes, body hashes,
   imported openings, rows, parent Js, image I and rank produce exactly the same
   ModuleID and184-byte J. The binary bytes are never substituted for canonical
   semantic hashing. Graph insertion/closure and genuine assumption verification
   remain unchanged. A decoder proves no theorem merely by constructing a Value.

This is equality of decoded mathematical input, not equality of arbitrary original
JSON bytes: whitespace and object-key order were never witness provenance in this
existential profile. Fresh binary data is still untrusted. A hostile encoder can
choose any Value, but cannot bypass the unchanged relation. Bugs in `D` remain a
new trusted-computing-base risk requiring independent review and correspondence
controls before a guest is adopted.

## Bounds must cover expansion and allocation, not just wire size

Preserve the aggregate maxima:16MiB total wire,16 deltas,8 assumptions,32
frontiers,48 warrants,128 parent edges; globally250000 rows,8192 bodies,4096
openings,500000 Values and depth128. Preserve each canonical Value's16MiB and
one-million-node/256-depth caps through unchanged `check`; the stricter aggregate
limits continue to apply. Count keys' bytes but not keys as Value nodes, matching
the old census. Retain127 open-container restriction separately.

Require **both** new binary wire size<=16MiB and the size of the equivalent
canonical-JSON aggregate wire<=16MiB. The latter includes original aggregate
fixed fields and frame lengths plus `sum(len(C(V_i)))`. Otherwise a16MiB binary
packet could silently expand into a much larger previously inadmissible JSON
workload. Compute exact canonical lengths using the existing string-escape,
unsigned-decimal and punctuation rules; a sender's claimed length is no evidence.
This restricts the format to a domain with an old-wire counterpart. It does not
promise every old accepted packet fits the new binary envelope.

Before allocating any string/frame, check remaining input and global byte limits.
Before allocating collections from declared lengths, reserve **global child
slots**: across all trees, roots plus declared array/object child counts equals
the eventual Value-node count. Charging these counts before `with_capacity`
prevents many nested huge, mostly empty allocations from each borrowing the
same remaining-node allowance. Alternatively grow incrementally under a proven
capacity bound. Merely checking each count against500000 independently is not
sufficient. Check arithmetic for overflow, including canonical expansion, before
allocation; cap explicit decode stack and reject truncation without authority.

For successfully bounded decoder data, memory is O(Value nodes + string/key
bytes + one frame + depth), with nontrivial Value/BTreeMap overhead. The unchanged
relation still clones selected groups, builds correspondence/native DAG data,
serializes canonical hash inputs and allocates checker intermediates. This is
not a numerical peak-RAM guarantee; owner process/output limits remain necessary.
Keeping every old independent validation traversal initially makes the change
easier to audit, even if it reduces the attainable saving.

## Why not jump directly to a typed arena?

| Route | What it removes | What must be justified |
|---|---|---|
| No-wire-change validation token | Selected redundant validation work | Root/base's separate current correspondence argument; no transport migration |
| Tagged binary to existing Value | JSON lexical input parsing | Decoder round trip, exact bounds, new wire/image; all downstream algorithms remain |
| Schema-typed arena all the way through | Potentially Value allocations, repeated names/subtrees and repeated tree walks | Typed extraction, canonical serializer/hash equality, correspondence and native parser redesign, reference/cycle/ownership rules |

Converting an arena back to Value just before existing `check` restores most of
the allocations it purported to save. Avoiding that conversion genuinely changes
the checker boundary and is not a small transport patch. Likewise bypassing
canonical hashing with a sender-supplied digest would weaken acceptance, not
optimize the same relation.

Write `T_old = L_json + A_Value + V + H + K` and
`T_new = L_binary + A_Value + V + H + K + extra_bound_work`, where `V` is retained
validation/census, `H` canonical commitments and `K` correspondence/type checking.
The possible saving is lexical work minus binary decoding/extra bounds, not the
entire old parser stack or all serialization. Actual saved-prefix attribution
may motivate this question, but omitted samples, caller overlap and incomplete
execution prohibit inferred whole-run cycle shares or an Amdahl speedup here.

## Deployment blockers and adoption condition

A format change needs an unambiguous new outer wire version, e.g. `DMKNAI03`,
and a new independently adopted guest image A'. The fixed module relation I,
foundation/policy and member Js can remain exact; aggregate H/receipt image
bindings cannot. Current A-parent processing calls `parent.bind_image(A')`, so
an old-A aggregate receipt cannot silently become a parent under A'. Legacy I
receipts remain a different unchanged boundary. No receipt/header patching or
reuse of a failed partial capsule is justified. Keep old guest/input/evidence
immutable; new image means fresh build/adoption and proof-production cost.

Select this fallback only if the cheaper current change leaves a consequential
input-parsing bottleneck and the anticipated repeated savings justify that
migration/certification cost. The next justified evidence would be one narrow
decoder-correspondence/adversarial-bound control and one matched retained
mathematical input—not a new broad network campaign. If implementation is ever
selected, preserve negative controls for duplicate keys, malformed UTF-8,
overflow/nonminimal integers, truncation, exact EOF, depth, global slots and
canonical expansion, followed by exact-J comparison under the unchanged relation.
No such implementation or experiment is commissioned by this note.
