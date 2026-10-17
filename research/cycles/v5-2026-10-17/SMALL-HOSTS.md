# Po18/N256 native hosts: implementation checkpoint

2026-10-17. Owner: `memo_independent_review`.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Authority: [SMALL-PRODUCER-SELECTION](SMALL-PRODUCER-SELECTION.md), adopting
the corrected [producer decision](PRODUCER-NEXT-DECISION.md) SHA-256
`33e4be91861bd97234620bc1c6148b6624db5da123bb51182e7c07c3e7ffc0ef`.

**Source implementation only. No compiler, native program, project import,
test, guest execution or proof was run.** Root owns exact review/adoption,
build/layout selection and Git. Both predecessor hosts, SDK, guest, checker,
receipt helper and historical evidence remain untouched. Read-only file/JSON
inspection and `git diff --no-index` checked the fresh source delta.

## Exact fresh source

| File under `software/v5/aggregate_small/` | Bytes | SHA-256 |
|---|---:|---|
| `aggregate_host.rs` | 20755 | `6644d9a03f25a59089fd735b0e2f2229ec8940dedbe2502568dfd8c6a36d9c25` |
| `stage_host.rs` | 32291 | `975e68dfbc8d091733cee72a18d81fb45617886585f1806fe9425cf4aa847955` |

The snapshot predecessor is `aggregate_host/aggregate_host.rs`; the stage
predecessor is `aggregate_production/stage_host.rs`. Both fresh hosts still use
`#[path = "../aggregate/receipt.rs"] mod receipt` and the same retained relation
and SDK libraries. A successful future one-link build is required; source review
is not compiler evidence or a proof-memory upper bound.

## Snapshot contract

The CLI positions are unchanged:

```text
snapshot A ELF WIRE H CYCLES PO2 MODE FRESH_CAPSULE FRESH_DIAGNOSTIC M [PARENTS...]
```

It now requires `PO2 == 18`, `1 <= CYCLES <= 2^26`, at most 256 consecutive
segments and the unchanged at-most-eight assumption limit. Each parent receipt
is at most 1 MiB. Individual segment encoding retains the original 64 MiB file
limit; the sum of retained segment bytes and separately the complete serialized
capsule are each limited to 96 MiB. The capsule retains exact `DMKNAS01`/version1
field layout; changing po2 changes the session binding and hence capsule binding.

No mathematical input changes: actual ELF image, native-derived exact H,
preverified typed parent receipts, actual ordered assumptions, final successful
guest journal/claim, no unsupported coprocessor/MMR/PoVW work, complete segment
census and create-new/fsynced custody checks remain.

The host's 512 MiB read allowance now includes initial inputs **and** every
`StoredSegment::resolve` read. An `Arc<Mutex<u64>>` holds the single allowance
across SDK segment references. Each read reserves its current ordinary file
length before I/O and never refunds a failed/partial read. The bounded reader
reads at most that reserved extent and requires its exact length to remain;
there is no extra `limit+1` probe outside the allowance. Metadata checks and
controller rebinding do not make mutable files adversarially immutable.

Snapshot stdout has the predecessor fields/status, with new schema
`DMKN_SMALL_AGGREGATE_SNAPSHOT_RESULT_V1`. The diagnostic schema is
`DMKN_SMALL_AGGREGATE_EXECUTION_DIAGNOSTIC_V1`; it additionally reports
`input_read_bytes` and
`input_read_accounting="PRE_READ_RESERVATIONS_WITH_NO_FAILURE_REFUND"`.
The first is exact successful read charge and a conservative failure charge,
not an independent measurement of disk traffic. Diagnostics remain bounded at
8 MiB. Snapshot custody's 208 MiB/288-entry whole-directory cap belongs to root's
enclosing adapter, while native component caps are independently enforced.

## Stage-manifest contract agreed with controller owner

Only `stage-manifest` (not old `stage`) dispatches proving:

```text
EXE stage-manifest A ELF WIRE H CYCLES PO2 KIND INDEX FRESH_OUTPUT M
    [PARENTS...] CAPSULE DEPENDENCIES_PATH DEPENDENCIES_BYTES DEPENDENCIES_SHA256
```

Exact argv length, including EXE, is `16+M`. Zero-based positions are A2, ELF3,
WIRE4, H5, CYCLES6, PO2=7, KIND8, INDEX9, output10, M11, parents12..11+M,
capsule12+M, dependency path13+M, dependency bytes14+M, dependency SHA15+M.
The controller separately bounds the actual quoted Windows command length;
the host does not infer short paths from the bounded argument count.

The manifest is a JSON object with exactly these named fields:

```text
schema: DMKN_AGGREGATE_DEPENDENCIES_V1
session_binding: lowercase 64-character hex
capsule_binding: lowercase 64-character hex
stage: canonical KIND:INDEX
dependencies: [{key: canonical KIND:INDEX,
                file: {path: absolute normalized ordinary path,
                       bytes: positive integer <= 512 KiB,
                       sha256: lowercase 64-character hex}}, ...]
```

Manifest bytes and SHA are checked against argv before parsing, under both the
512 MiB host read allowance and the per-kind manifest cap. The caps are segment
2 KiB, lift/resolve 4 KiB, join 6 KiB, finish 256 KiB. All manifests have at most
257 rows. The JSON-specific visitor decodes incrementally into an initially
empty vector, never preallocates from a supplied length hint, and rejects any
258th element before appending a row. The bincode capsule visitor remains a
different helper that requires its exact fixed sequence hint.

A self-review caught a Serde pitfall before compilation: derived structs can
accept positional arrays as well as maps. `JsonObject<T>` now requires a map at
all three object boundaries (manifest, dependency row, file pin), while the
derived strict fields reject duplicate, unknown and missing fields and wrong
scalar types. `decoder.end()` rejects trailing non-whitespace input. Numeric
booleans, fractional/scientific-number fields, alternate stage index spelling,
uppercase hashes and unsupported stage keys do not meet the typed contract.

Paths must be UTF-8 strings of at most 512 UTF-16 units; absolute component
reconstruction must preserve their exact spelling. Parent/current components,
symlinks, reparse ancestors and nonordinary parents refuse. The exact manifest
byte cap remains independent of string length. The reader does not follow a
transitive dependency manifest.

The host derives dependency keys from the **actual decoded capsule**:

| Stage | Ordered dependencies |
|---|---|
| `segment:i` | none |
| `lift:i` | `segment:i` |
| `join:i` | previous prefix (`lift:0` or `join:i-1`), then `lift:i` |
| `resolve:i` | last segment prefix when i=0, otherwise `resolve:i-1` |
| `finish:0` | all `segment:0..s-1` in order, then final resolve/prefix |

Exact list equality precedes checkpoint reading and proving. Each file then
must match its pin, checkpoint envelope key and capsule binding; unchanged SDK
cryptographic verification still runs when the checkpoint is consumed. A pin,
manifest or envelope is not proof authority. Leftover cache entries refuse.

Stage stdout retains old status/fields with schema
`DMKN_SMALL_AGGREGATE_PROOF_STAGE_V1`, plus:

```text
dependency_manifest: {path, bytes, sha256}
dependency_keys: [exact ordered KIND:INDEX strings]
```

The controller author confirmed these names and will bind them to the actual
written manifest pin/derived keys. The new stage read meter reserves before
I/O, just as snapshot does, so failures cannot reopen byte allowance.

## Separate caps; unchanged final acceptance

| Object | Native cap |
|---|---:|
| General original encoding/file limit | 64 MiB, unchanged |
| Parent receipt | 1 MiB |
| Retained checkpoint input | 512 KiB, independently in pin/read/envelope checks |
| Every new checkpoint and final succinct receipt | 512 KiB |
| Full capsule read/decode | 96 MiB, bounded outer vectors N256/M8 |
| Internal complete composite encode/decode | 160 MiB, dedicated helpers only |
| Total stage input reads, including manifest/dependencies | 512 MiB |

Finish still collects all segment receipts and the final resolved prefix,
checks the exact pinned composite tuple/Serde roundtrip, verifies composite
integrity, compares its claim with the exact snapshot and target claim, checks
the final succinct claim, constructs the application receipt and calls unchanged
`receipt::verify_aggregate(A,H,R)` with dev mode disabled. Dropping obsolete raw
capsule/composite serializations after their last use does not omit any check.
The 160 MiB composite allowance never widens checkpoint/final receipt readers
and never makes that internal composite a network artifact.

Both native `verify` commands retain the existing
`DMKN_AGGREGATE_VERIFY_RESULT_V1` exact receiving contract and actual verification;
their local input artifact cap is 512 KiB. Existing independently selected
general receiving hosts remain untouched.

The changes provide no total heap guarantee: nested SDK objects, witness
reconstruction, reserialization and prover allocations still need enclosing
resource limits. The owner-selected stage memory policy remains the controller's
responsibility; it is not a new CLI operand or a claim that 4 GiB suffices.

## Review status and next decision

Independent reviewer read the complete initial sources and the later object-only
repair with no source blocker reported. The last pre-read reservation refinement
and these exact final hashes have been submitted for the changed-boundary reread.
Only root can adopt the final source/review and select the two one-link builds.
No whole-test repeat, proof pilot, geometry retry or resource escalation follows
automatically. Actual complete po18 layout, resource admission and a separately
funded full-po18 segment remain subsequent decisions.
