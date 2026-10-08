# V3 efficiency triage: authenticate already-canonical bytes once

2026-09-27. Author: `v3_efficiency`. Read-only source/evidence triage; no product
import, profile, benchmark, Lean run, service, or edit to a used source cut.
Canonical guard passed; project instructions, goal, and current desk read.

## Decision for the central agent

Select **checked canonical-byte package insertion** as the one bounded efficiency
candidate. It targets repeated encoding in the actual submission/acquisition/
admission pipeline without changing mathematical acceptance, mutable-object
guards, package grammar, foundation, native replay, or network behavior.

This is a plausible improvement, not a measured speedup. Do not build a SNARK,
persistent checked-environment cache, or new proof-compression architecture for
the deadline. Those remain serious longer-term alternatives with different
trust and measurement obligations.

## Why this seam

The retained source13 Count return admission took 33.3866865 wall seconds and
32.96875 inclusive Job CPU seconds. Its nested native process tree accounted
for 7.609375 CPU seconds (23.08%), not isolated Lean-kernel time. Six package
reads accounted for 13.678026 accumulated reader wall seconds. Submission
took 127.2798794 wall / 156.03125 inclusive CPU seconds, with ten package reads
and 25.634884 reader wall seconds. These nested scopes must not be added.
See [the retained cost note](../../audits/succinct-checking-2026-09-24/COST-EVIDENCE.md).

Actual source13/source14 reader path for each package object is:

```text
raw = bounded read of exact object file
payload = C.loads(raw)                 # strict decode, then dumps(payload)==raw
C.cid(tag, schema, payload) == ref     # dumps(payload) a second time
Store.add(tag, schema, payload)        # cid_with_encoding: dumps a third time
... closure / plan / native checks ...
```

Every successful `loads` already establishes that these immutable `raw` bytes
are the exact canonical encoding of the returned value. Re-encoding that same
value twice before insertion is unnecessary if insertion itself owns strict
decoding and digest authentication. This is a stronger candidate than merely
merging the second and third encodes.

Other repeated work remains: Store construction, mutation checks in `get`,
closure/planning, repeated checked unions, subprocesses, and native reconstruction.
The proposal does not assume all these are waste or promise to remove them.
It does not make proof search or kernel reduction intrinsically faster.

## Exact contract and implementation shape

Use two explicit paths, preserving existing value semantics:

- Existing `Store.add(tag, schema, payload)` retains exact behavior for locally
  constructed values, including bytes-as-a-CBOR-byte-string.
- New `Store.add_package_bytes(expected_ref, raw)` (name illustrative) accepts
  only an advertised typed CID and raw bytes. It must **not** accept a decoded
  payload, an alleged valid digest, a validation Boolean, or a remote receipt
  supplied by its caller. It performs its own unchanged strict `C.loads(raw)`,
  obtains the CID of those exact canonical bytes, checks equality with the
  advertised ID, then enters common insertion bookkeeping.

A codec helper can combine strict decoding and typed CID construction, returning
`(actual_ref, payload)`. Its success postcondition is:

```text
payload = loads(raw)
dumps(payload) = raw
actual_ref = [1, tag, schema, SHA256(preimage)]
preimage = b"DTMKN-CAS\x00"
         || tag.to_bytes(2, "big")
         || schema.to_bytes(2, "big")
         || len(raw).to_bytes(8, "big")
         || raw
```

`tag` and `schema` remain exact unsigned Python integers in `[0, 65535]`.
The decoder remains unchanged, including its own canonical re-encoding and
all limits. Keep the existing `cid`/`cid_with_encoding` interpretation of bytes
unchanged: do not overload bytes-as-value and bytes-as-canonical-encoding.

If sharing insertion bookkeeping, keep the unchecked insertion helper private
and reachable only immediately after locally computed encoding/digest checks.
The new public method itself must validate everything; an API taking both
`raw` and an independently supplied `payload` would introduce an avoidable
consistency obligation. Insert the computed reference, not an externally
aliased expected-reference object.

In `read_package`, replace the decode/CID/add triple with that method. Keep the
preceding exact `identity(ref)` validation, duplicate-ID check, file path and
read order/limits, aggregate raw-byte accounting, and all subsequent foundation,
inventory, exact-closure and complete-plan checks in place.

### Proof obligation

Assume stable owner-local Python inputs during the operation, as in the current
code, and the unchanged strict decoder/hash implementation. If `loads(raw)`
succeeds with `p`, it explicitly tested `dumps(p)==raw`. Consequently the new
digest preimage is byte-for-byte equal to the existing `cid(tag,schema,p)`
preimage. The existing insertion's canonical length also equals `len(raw)`.
Thus identical CID comparison, collision checks, limits and insertion yield
identical objects/length accounting. This is an exact identity argument, not a
cryptographic claim that a hash proves a theorem. Native acceptance remains
unchanged.

Preserve failed-insertion atomicity: wrong CID, unsupported encoding, collision,
object quota, or byte quota must not alter objects or `total_bytes`. Preserve
error ordering where current reader inputs can trigger more than one failure.
The inherited behavior for inserting a duplicate under an exhausted quota also
must remain unchanged. Mutable payloads are still stored and `Store.get` still
recomputes their commitment, so subsequent payload/reference mutations continue
to be refused. No cross-request trust, cache invalidation or memory-snapshot
assumption is added.

## Evidence deduplication: this is not the old candidate

I read the actual retained design and outcomes, not only summary labels:

- [Fixed-seed template result](../../../experiments/lean-package-efficiency/RESULTS.md):
  correctness passed but adoption failed; first-package wall ratios were
  1.152613 and 1.196589 and memory rose. No template/deep-copy cache is proposed.
- [Checked-insertion design](../../../experiments/checked-package-insertion/DESIGN.md):
  adds `expected=` to value insertion, removing **one** duplicate encode, while
  still doing strict decode/re-encode plus value encoding. Its ten focused
  correctness tests passed, but [timing](../../../experiments/checked-package-insertion/TIMING-OUTCOME.md)
  stopped after 27/48 reads at the frozen 150-second start-read deadline. It is
  incomplete, not a passed speed gate and not an experiment to resume or relabel.
- [Short-header result](../../../experiments/short-header-01/RESULTS.md):
  source10 already reduced per-visit encoding overhead. That improvement is in
  source13/14 and is the new baseline; do not compare against the old encoder.
- Prior profiler results establish repeated encoding as relevant mechanism
  evidence but do not estimate this candidate's source14 end-to-end savings.
  No baseline-only profiler or historical campaign is needed again.

The proposed candidate removes **two** pre-insertion payload encodes per read
object, retaining the decoder's canonicality encode. It is independently
specified against the current source, not a completion of the old allocation.

## Minimal new source scope

After root completes/selects the index successor and copies a separately verified
fresh source15, edit only:

- `py/codec.py`: explicit decode-and-CID helper; shared preimage helper only if
  useful, with existing value-CID outputs unchanged.
- `py/source_codec.py`: checked raw-byte insertion plus shared atomic bookkeeping,
  reader's one-call replacement, and exact codec-loader hash pin.
- Root-owned `assets-lock.json` and narrowly necessary API/support explanation.

Do not alter `checking.py`, native Lean code, resource grants, Store mutation
guards, storage, network, canonical grammar, identities, or foundation.
No intermediate source14 full build/campaign is needed solely to select this
source15, once its focused index gate passes and the complete map is preserved.

Read-only source14 pins at inspection:

| File | SHA-256 |
|---|---|
| `py/codec.py` | `1906a39f819f6c3aa3a4f3d8eae10b00bf02040a339efc532b42155b4d7d6bcf` |
| `py/source_codec.py` | `37f2c4976817ad91e8373867709506359de3b955a1b7c01a21266dd880d39b58` |
| `py/checking.py` | `266a200dee8ae2c5c9cc18c0f7a30e806e6cdaaa6ee72a0ad1db26e57a113d57` |

## Discriminating tests and measurements

Use one fresh focused differential allocation against the exact current
baseline. Reuse old test ideas/evidence, not old results as new qualification.
Required changed-seam controls:

- For actual common and Count packages, exact Store/base/seed/root/inventory/
  length/closure/plan equality; byte-for-byte package export equality.
- Canonical raw integer/list/bytes cases and all header widths; malformed,
  truncated, nonshortest, trailing, forbidden-type, depth/item/byte bound refusals.
- Tag/schema/domain/length/hash binding, wrong expected ref before insertion,
  no external payload/digest bypass, value-bytes versus encoded-bytes separation.
- Duplicate IDs, forced collision guard, full quotas, failed-insertion atomicity,
  payload/reference mutation after insertion, and missing/extra closure/inventory.
- Deterministic call-count control: the reader's new seam performs only the
  one decoder-owned payload encoding, versus three in the baseline, while
  `Store.get` mutation checks remain. Instrumentation belongs in correctness
  tests, never in the timing comparison.

Then one bounded unprofiled actual-reader comparison can use fresh Stores in
balanced AB/BA order on (1) a small common package and (2) the retained Count
closure. Retain every observation, including first reads, setup scope, failures,
peak private commit, exact input/code pins and process closure. Prospectively
choose a finite completion envelope and useful improvement/no-regression rule;
do not copy the old failed 48-read allocation. Root should prefer few complete
paired observations over a larger sample that misses the deadline. A specific
engineering gate could require both combined paired CPU ratios <=0.95 with
each workload's wall ratio <=1.10, but that rule is not yet commissioned here.

Most importantly, the tentative v3's already-needed installed reciprocal
scenario must record complete submit/publish/acquire/admit/reuse costs and
unchanged final mathematical outputs. If claiming a causal workflow speedup,
run a prospectively matched source14-versus-source15 workflow differing only
in this optimization on equal fresh states, grants, exact source/objects and
operation order. Historical source13 measurements may give context, not that
causal comparison. Reader benefit alone must be called reader benefit.

## Relation to quicker knowledge growth

This candidate reduces the cost of carrying/checking already-produced formal
artifacts, if its measured gate passes. It is complementary to the reuse-arm
evaluation, not a proof of mathematical novelty, efficient proof search, useful
agent output, or exponential growth. Report actual independently checked target
completion and total applicable costs separately. A faster unchanged proof
pipeline is a legitimate v3 engineering improvement even if a small reuse-arm
experiment fails; conversely successful reuse is not evidence this codec is
faster. Neither claim should hide the other.
