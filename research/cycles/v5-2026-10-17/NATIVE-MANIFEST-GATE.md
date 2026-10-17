# Minimal native manifest gate: verification-only refusals

2026-10-17, `memo_tests_review`. Source/data design only under root assignment;
guard passes. No product edit, import, test, native call, proof or Git operation.
The used small controller/hosts/controls remain frozen. This note selects no
runtime and does not repeat their completed Python controls.

## No-prove argument comes first

**Invoke `stage-manifest ... finish 0 ...` in every case.** In the pinned host,
`final_receipt = kind == "finish"` selects the composite/succinct verification
branch. `get_prover_server` and `prove_segment/lift/join/resolve` occur only in
the opposite branch. Consequently, even an unexpectedly accepted manifest
cannot construct a prover or enter a proving method through this command.
Do not use `segment` with an allegedly invalid manifest as the safety barrier.
Do not use `lift` with an invalid SDK payload: that branch constructs the
prover before decoding its input, although it might never invoke `lift`.

This is a source-control-flow argument under the adopted source/build and SDK
verification assumptions, not dynamic proof-call instrumentation or a new
formal theorem about the binary. Guest execution is absent from this host.
`compute_image_id`, native relation checking, parent receipt verification,
capsule decoding and assumption verification still occur and must be charged.

Native author independently agrees with the finish-only route and the
deterministic invalid-checkpoint oracle below. No new diagnostic command or
test-specific host build is needed.

## Exact existing inputs and prerequisite

Pinned host source:
`software/v5/aggregate_small/stage_host.rs`, 32,291 bytes, SHA-256
`975e68dfbc8d091733cee72a18d81fb45617886585f1806fe9425cf4aa847955`.
The actual completed stage build reports executable
`experiments/v5-local-checks/small-aggregate-stage-host-build-01/small_aggregate_stage_host.exe`,
68,036,608 bytes, SHA-256
`8f8e444ddd9029906fee60a073a701bdd34c8b095d54f81f2554bfe1e91ad8ee`.
Root must adopt that build's actual outcome and pins before selecting this gate.

The fresh layout is configured at
`experiments/v5-local-checks/small-aggregate-layout-01/evidence`.
Its completed result did not yet exist when this design was written; do not
fabricate its capsule/session/count. Require the actual independently adopted
complete po18 layout, including clean enclosing closure and unchanged A/H:

- A: `99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60`;
- actual retained memo ELF and genuine I receipt from that layout's invocation;
- exact new wire, 192-byte expected header and whole capsule;
- actual cycles/po2, s/m, session binding and capsule binding;
- all parent receipts in their actual selected order.

Use the actual capsule, not the retained po19 capsule with a new label. Pin
all inputs and the host before/after the gate. A prior-layout/native-preflight
failure is **not** a passing manifest test. No complete-layout retry is implied
if the pending operation refuses.

## Shared fixture: one deliberately invalid checkpoint

Create one ordinary, non-reparse 72-byte file of zero bytes under the fresh
gate output; record its actual size/hash. It passes the checkpoint byte-extent
minimum but fails the exact magic/version check. It is explicitly synthetic
invalid input, not a fake cryptographic success or a retained proof.

Derive the finish dependency keys from the actual capsule metadata:

```text
segment:0, ..., segment:(s-1), final_prefix
final_prefix = resolve:(m-1), if m>0;
               join:(s-1),  if m=0 and s>1;
               lift:0,      otherwise.
```

There are s+1 rows, always at least two. Every row may point to the same invalid
file: the manifest has distinct correct keys, while the first consumed file
will fail before a checkpoint can be admitted. No per-segment fake file set is
needed. Each row is `{key,file:{path,bytes,sha256}}`. Use the exact schema,
session/capsule bindings and `stage="finish:0"`. Normal cases are encoded with
the existing canonical JSON convention. Deliberately noncanonical JSON cases
below are explicit byte fixtures, not rewritten successful records.

Every mutation except the deliberate outer-hash case gets its own correctly
recomputed manifest length/hash operands. Otherwise a parser test would stop
at the earlier hash gate and test the wrong boundary. Each manifest is at most
256 KiB; all paths are ordinary absolute canonical spellings within the native
512-UTF-16-unit cap. Each case gets a distinct fresh artifact path whose parent
already exists. Do not change filesystem state concurrently with a case.

## Ten small cases and branch-specific oracles

All rows use the genuine common invocation and `finish:0`. Each must return a
nonzero ordinary exit with clean closure, no artifact, no success JSON and no
`AGGREGATE_STAGE_PROGRESS ... phase=crypto` or `phase=written` line. Retain
complete bounded stdout/stderr. Match the listed error clause rather than the
whole diagnostic's platform-dependent formatting/line-column suffix.

| Case | Single changed boundary | Required diagnostic/reach |
|---|---|---|
| M1 | Correct ordinary manifest; flip one hex digit only in its argv SHA-256 | `exact dependency manifest bytes/hash` |
| M2 | Correctly pinned JSON bytes with duplicate top-level `schema` key | serde `duplicate field` identifying `schema`; not a hash failure |
| M3 | Replace first row's `file` object with a positional JSON array containing the same three values | serde `invalid type: sequence` / expected JSON object; exercises the nested object-only adapter |
| M4 | Replace first row's integer `bytes` with boolean `true` | serde invalid boolean/type for integer; not an artifact-cap or hash failure |
| M5 | Flip one hex digit of the manifest's capsule binding, preserving lowercase digest syntax | `manifest exact schema/session/capsule/stage` |
| M6 | Reverse the actual ordered dependency rows; keep count and all pins exact | `exact ordered dependency keys` |
| M7 | Exact ordered manifest, but flip one hex digit of first row's file SHA-256 | `exact dependency file bytes/hash` |
| M8 | Exactly 257 well-typed rows, all key `lift:0` and the ordinary invalid-file pin | Parser must reach `exact dependency count` if s<256, or `exact ordered dependency keys` if s=256; **not** `dependency row bound` |
| M9 | Exactly 258 otherwise identical well-typed rows | serde `dependency row bound`; the 258th value is consumed only as IgnoredAny and never appended |
| M10 | Unmodified exact ordered manifest and exact invalid-file pins | `aggregate checkpoint magic/version` |

M8/M9 test the parser boundary independently of the actual layout count; M8
does not assert a genuine 256-segment layout or successful finish. Its branch
oracle must be resolved from actual s before launch, not accepted by a loose
post hoc error whitelist. M10 proves that parsing, schema/session/stage binding,
the actual dependency-vector checks, all ordinary path checks and first file
size/hash checks were reached successfully before a deterministic refusal.
It does not need an SDK-serialization fixture or cryptographic verifier failure:
the native checkpoint gate is the smallest reliable positive-parser endpoint.

Missing/unknown fields, every positional-array nesting, all path refusals and
all malformed SDK encodings are not separately exercised here. Their source
review is not replaced by a claim of exhaustive runtime coverage. Do not grow
this gate into a generic fuzzer or repeat the twelve Python controls.

## Charge the real preflight; keep the operation small

The manifest is read **after** actual ELF identity checking, native aggregate
relation checking, typed application verification of all parents, complete
capsule decode and `ordered_assumptions` verification. The latter verifies each
succinct parent again. For the current one-parent layout, each case therefore
includes two parent-proof verification paths, not merely JSON parsing. None is
proof production. Shared host startup/capsule work is intentionally repeated
only for these ten distinct changed native boundaries.

Candidate finite execution envelope, subject to root's actual-capacity and
exact selector review:

- Sequential cases only; no overlapping native processes.
- Per native case: 15 CPU seconds, 20 wall seconds, 1,024 MiB process/Job cap,
  one host process, stdout/stderr at most 64 KiB each.
- Aggregate: at most ten native calls, 150 worker CPU seconds, 30 controller
  CPU seconds and 240 total wall seconds; enclosing memory at most 1,536 MiB
  and two active processes for controller plus host.
- Fresh retained output: 16 MiB / 128 entries, including all fixture bytes,
  logs, commands, reports and reserved finalization tails. Do not copy the
  retained capsule/ELF into this output; pin and read their existing locations.

These are prospective safe finite caps, not sufficiency bounds. Stop the whole
gate at the first unexpected diagnostic/exit, timeout, unknown closure, input
mutation, artifact creation, resource refusal or progress/success marker.
An expected native rejection can pass its selected control; a resource refusal
cannot. Never automatically relax a cap, rerun or continue after uncertain
closure. Record inclusive costs of failed controls too. Use the retained
supervisor/ordinary-path machinery rather than adding a new process framework.

## Result claim

A successful gate would support only: the exact built native host enforced
these ten manifest/input boundaries on the actual new capsule and verified
parents, without calling its proving branch. It would not provide an A receipt,
test a real segment proof, establish full-po18 memory sufficiency, validate a
genuine composite/finish or close reciprocal-growth/public-release obligations.

The informative actual full-po18 segment discriminator remains a separate
production decision after real constructor/request adoption and capacity review.
