# Independent review: aggregate staged-production host

2026-10-12. Source-only review assigned by root after the fresh stage host was
written. Reviewer: receipt-source lane, not the stage-host author. Canonical
workspace guard passed. No compiler, Python project import, test, guest, proof,
cache mutation or Git operation was run. No author's source was modified.

## Disposition

**No blocking source-level soundness, capsule ABI or supported SDK interface
defect found in the reviewed bytes.** This permits root to consider a separately
selected compile/control operation; it does not assert compilation, actual
recursive resolution, receipt production, mathematical admission or final v5.
There is no successful aggregate capsule presumed by this review and still no
aggregate Python producer selected by these sources.

| Reviewed file | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/aggregate_production/stage_host.rs` | 22280 | `9ff95fadb46de24d52996c0ab6a018b7a984150f65526645663a3737cbb1f821` |
| `software/v5/aggregate_production/API.md` | 6394 | `185a7e4406c5d45f2e739303ab77256fccd74d0d84ed28835adfb1ffbf1d12c3` |
| `research/cycles/v5-2026-10-12/AGGREGATE-PRODUCTION-SEAM.md` | 26412 | `1421fc4b0d4529dd9bf5cd73bd9e55dfc6cf2f8f3d7ca0a24cb6a743510224b0` |

These hashes were rechecked at the end of the read; they identify this review's
scope, not an authorization to rewrite those files or execute their commands.

## Direct comparison basis

Read the complete new host/API/seam, the retained
`software/v5/aggregate_host/aggregate_host.rs`, the relevant staged paths in
`software/v5/modules/receipt/src/bin/module_host.rs`, and unchanged
`software/v5/aggregate/receipt.rs`.

Inspected the actual retained host SDK under
`experiments/general-checker-host-05/build-01/source/risc0-3bbcd44d6459b9ef6ac0df3846dc9215514934e8/`:

- `risc0/zkvm/src/receipt/composite.rs`, `segment.rs`, `succinct.rs`;
- `risc0/zkvm/src/host/server/prove/mod.rs` and `prover_impl.rs`;
- `risc0/zkvm/src/host/recursion/prove/mod.rs`;
- `risc0/zkp/src/core/digest.rs`.

Also inspected retained `bincode-1.3.3/src/de/mod.rs` at that build's cargo-home.
This is a targeted semantic/API read, not a newly claimed full SDK audit.

## Findings by obligation

### Capsule and operation identity

The new `AggregateSnapshot` retains exactly the old six serialized fields:
magic `[u8;8]`, version `u32`, session binding `Digest`, session target
`ReceiptClaim`, `Vec<Digest>` assumption order, `Vec<Segment>` segments. Only
deserialize visitors change. Deriving Serialize on the unchanged Vec fields
preserves the producer's bincode representation.

The session tuple matches the old host in order and types:

```text
("DMKN-AGGREGATE-SESSION-V1", Hash(ELF), A,
 I, foundation, policy, Hash(wire), Hash(H), cycles, po2,
 ordered_parent_receipt_byte_hashes)
```

The capsule binding also matches exactly:

```text
Hash(encode(("DMKN-AGGREGATE-SNAPSHOT-V1", S, Hash(capsule_bytes))))
```

The explicit adopted A is checked against the actual ELF and the header's image
binding. The actual native relation derives exact H and pending claims. The
capsule's target claim must match independently formed `ReceiptClaim::ok(A,H)`.
An attacker cannot establish final authority merely by rewriting S/B: they are
unkeyed operational bindings, and both documentation and final code retain the
independent cryptographic A/H acceptance boundary.

### Decoder and envelope bounds

Bincode's fixed-integer `deserialize_seq` reads a length and delegates to tuple
access whose `size_hint()` is exactly its remaining count. The custom visitor
rejects lengths over8 or128 **before** `Vec::with_capacity` or element decoding,
then reads exactly that count. This is appropriate for this private bincode-only
decoder; it is not a generic proof about arbitrary serde deserializers. Bincode
trailing-byte rejection remains enabled.

For the checkpoint envelope, the offsets agree with fixed little-endian bincode
and the SDK Digest's eight-u32 representation on the selected Windows x86-64
host. The parser first bounds the whole object, validates magic/version/binding,
bounds kind length1..7, checks the complete fixed-field extent, then requires
payload length equal the actual remainder and nonzero. Thus all slice indices
are guarded, and a declared oversized payload cannot trigger its copy first.
The allowed kind set excludes finish; duplicate and unused keys are rejected.
Neither this envelope nor its checksum proves the payload.

The documented residual is accurate: nested SDK claim/segment/receipt decoding
still lacks a proven total heap/depth bound. The64MiB encoded cap is not a64MiB
heap guarantee. A separate finite process owner remains mandatory; exhaustion,
panic or unclean closure cannot be adopted. No decoder or sandbox qualification
is silently supplied by this source review.

### Exact parent set and actual resolve operations

Before capsule use, each offered parent is fully verified using unchanged typed
`receipt::verify_pending`, including image policy, exact journal, non-dev mode
and full successful application verification. The code separately excludes
duplicate typed pending claims and duplicate parent claim digests.

`ordered_assumptions` requires equal bounded counts and removes each capsule
digest from the map of genuinely verified succinct parents, rejecting repeats,
missing and extra claims. `into_unknown()` retains the same claim digest and
proof; it is type erasure, not a change of mathematical statement. Receipt-byte
order for S and actual assumption-digest order remain correctly distinct.

The `resolve` arm calls the retained real `ProverServer::resolve` with exactly
the next parent in capsule order and the preceding prefix/resolution checkpoint.
The SDK implementation invokes the recursion resolve program, computes the
resolved expected claim, merges it with the decoded recursion claim and verifies
the resulting receipt. This is not a native/status-only discharge. The generic
API signatures agree with the supplied argument types.

### Stage dependencies and final authority

Index checks and `prefix_key` correctly cover s=1 and general s, reject join0,
bound resolve by actual m and require finish0. Every consumed segment checks
index, Poseidon2, exact selected segment-parameter digest and seal integrity.
Succinct checkpoint integrity uses the adopted non-dev verifier context; the
SDK itself checks its parameter digest. Lift preserves the input claim digest;
join and resolve use SDK-supported claim composition. The exact fresh graph is
`s + s + (s-1) + m + 1 = 3s+m`, at most392 calls, not merely s segment proofs.

Finish consumes all s segment receipts and the last resolved/full prefix proof.
The composite tuple field order matches the pinned non-exhaustive SDK structure:
`(segments, assumption_receipts, verifier_parameters)`. Encode/decode round trip
checks that adapter layout but is **followed by** actual composite verification.
SDK composite verification checks continuation and exact ordered assumption
resolution. Only afterwards does its `claim()` remove assumptions; the ordering
of those operations is correct here.

The verified composite claim must equal both the capsule target and independent
`ReceiptClaim::ok(A,H)`. The verified final succinct claim must equal that same
independent target. The host then constructs the actual application receipt and
calls unchanged `receipt::verify_aggregate` on its serialized bytes before a
fresh durable output write. That performs full A verification and exact H/journal
equality, not just integrity. A conditional joined proof cannot pass finish.

The six-field public `verify` result contract is unchanged. Stage reports remain
non-admission diagnostics. `get_prover_server` in the inspected SDK selects the
local `ProverImpl` with non-dev options; this entry point does not select an
ambient remote proving service. Finish does not instantiate a prover at all.

## Remaining qualification, not defects repaired here

1. Root must pin and compile the new host against the intended existing SDK and
   matching aggregate/module libraries. Source inspection is not a successful
   link or demonstration of ABI behavior.
2. Cheap tests should exercise count-before-allocation refusal, truncated and
   oversized checkpoint extents, magic/version/trailing-data refusal, wrong S/B,
   old module envelope refusal, and duplicate/unused dependency keys. They should
   not be represented as real cryptographic recursive-resolution evidence.
3. A successful selected complete A capsule and genuine I parent are necessary
   before funding the actual missing stage graph. The real positive endpoint is
   final A receipt verification and same-call public member admission. Do not
   repeat the I proof or guest execution merely to test this adapter.
4. An aggregate producer/owner must enforce exact source/input selection, clean
   supervised closure, aggregate cost/output reservations and failure accounting.
   A512MiB read cap can legitimately refuse some combinations allowed by separate
   per-file/count ceilings; the API already explains this. Format ceilings are
   not guaranteed successful resource bounds.
5. The checkpoint envelope is not authenticated provenance. Relabeling an
   otherwise valid payload is not prevented by its unkeyed framing; owner profile
   selection and final independent A/H verification are the actual boundaries.
   This is explicitly documented and is not being misreported as a soundness gap.

No author repair is requested on the reviewed source. A future change or actual
compile/control result requires its own bounded changed-boundary review; this
note does not silently preaccept it.
