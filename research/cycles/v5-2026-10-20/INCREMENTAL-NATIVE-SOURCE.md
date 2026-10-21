# Incremental native admission: source checkpoint

2026-10-21, core_growth. Source implementation only. No imports, compilation,
tests, native processes, certificate production, installation or Git changes.
Independent source review and focused controls belong to adaptive_audit; root
owns execution and adoption.

## Exact source

- New file: `software/v5/incremental_native/mixed_claims/receiver.py`.
- Bytes: 27,837.
- SHA-256: `5436569971c272b129fbaec480d51d57a1ec521d43fd4d4ad14133b786691d5b`.
- Basis: `software/v5/standalone_validation/mixed_claims/receiver.py`, SHA-256
  `835d59809045c3e49f9d7e5483108f4034c591a3a82224e4155f4f7d0f6dcced`.
- Authority: INCREMENTAL-NATIVE-SELECTION; independent decision challenge
  NEXT-GROWTH-REVIEW, SHA-256
  `ef197b308c929b49ed22777fc08cf2b0d8a3fd6c0901ee159d353842e3018378`.

The predecessor remains unchanged. Public signatures, packet format, relation,
owner profile calculation, exported proof forms and existing report keys remain.
The new source pin naturally produces its own installed owner profile; no old
profile is relabeled as the successor.

## Implementation boundary

`_native_memo` is initialized before this receiver's first `_check`. It is private
to one live receiver and cleared by `_revoke`. Its exact immutable bytes keys
denote canonical witnesses. Dictionary hashing is only lookup: complete bytes
equality determines a hit. Values are immutable tuples:

```text
(exact_owner_object, profile, image, foundation, policy,
 ordered_exact_parent_journals, rank, actual_returned_J)
```

Only the actual unchanged native subprocess plus `bind_native` creates a new
conditional observation. The hit branch checks exact object identity and every
stored binding, then decodes the retained actual J and checks its image,
foundation, policy, complete summary and rank against this packet. It neither
constructs a replacement J nor reruns `bind_native` on fabricated output.

Every current packet still undergoes ordinary parsing/resource checks, genuine
current receipt/member processing, graph reconstruction, exact parent/rank
checks, actual-graph checks, final target closure and complete packet readback.
The original per-witness pre/post `_check` and `_live_frontiers` calls remain on
both paths. No prior packet's frontier list grants current authority.

The native launch's minimum remaining whole second, input readback, process
report and stdout binding apply to actual misses. A hit does not launch a
process and therefore creates none of those files; original live deadline
checks still apply. No exact equivalence of near-deadline refusal timing is
claimed.

## Retention and promotion

`pending_native` starts empty for each packet. `_retain_native` is a private
static inert-data helper: it receives that pending dictionary and byte count,
adds one record only if both limits permit, and returns the actual byte count.
It never assigns `_native_memo` or creates a live warrant. The helper clamps the
configured limits to 16 records and 16 MiB; actual canonical witness lengths are
counted, duplicates are not counted twice, and skipped entries cause only future
misses. This factorization permits direct tiny-limit retention controls without
large allocations or changing an active owner's envelope.

Only after the existing final census, final source/frontier checks and `_active`
check, and alongside the normal live-handle promotion, does the complete pending
dictionary replace `_native_memo`. Prior-packet entries absent from the latest
successful packet are dropped. Failed prefixes or finalization never promote
pending records. The existing exception path revokes the owner and clears its
old memo; the unpublished local pending dictionary is discarded.

The retained memo alone has at most 16 records/16 MiB of witness bytes. During
admission there can also be a bounded pending dictionary, parsed inputs and
existing packet handles; this is not a claim that total receiver memory is only
16 MiB. No persistent cache, disk loader, cross-owner restoration, general LRU,
new budget parameter or API for installing observations was added.

## Honest evidence and accounting

The full original packet remains available through unchanged live export and
import APIs. Those APIs consume stored packet bytes and live descriptions, not
private native execution paths; the independent exact selected-source search in
NEXT-GROWTH-REVIEW found no contrary public dependency.

Each completed pre-promotion RESULT now contains `native_observations`, indexed
by packet witness position, with exact witness hash/length and actual J. Tags:

- `NATIVE_EXECUTED_CONDITIONAL_CHECK` for a freshly executed/bound native result.
- `SAME_OWNER_REUSED_CONDITIONAL_CHECK_NO_EXECUTION` for a hit.

The RESULT still explicitly says `SAVED_REPORT_NOT_TRANSFERABLE_PROOF`, and its
status remains `MIXED_BOUND_BEFORE_LIVE_PROMOTION`: subsequent finalization can
still fail. These diagnostics neither restore authority nor invent process
output. Historical audit scripts expecting one process file per witness must
not reinterpret absent hit files as execution success.

Added report fields are `native_check_attempts`, `native_reuse_observations`,
`retained_native_records` and `retained_native_witness_bytes`. The first counts
calls attempted through the native supervisor; the second counts bound hit
observations. Either may include work in a packet that subsequently fails, so
neither is an admitted-theorem count. Retained counts are zero after revocation.
Existing `observed_success_worker_cpu` is updated only from actual clean worker
reports. Original attempts, submitted bytes, full-graph CPU reservations and
conservative output reserves are unchanged, including charges on hits/failures.

## Acceptance refinement and warranted consequence

Under the existing native relation, exact binding, live authority and execution
integrity assumptions, a successful native check establishes one exact
conditional implication from its ordered parent journals to its returned J.
An exact witness hit reuses that implication, not its old premises. Induction
over the newly rebuilt current graph establishes the same target because all
current parents are separately required before every insertion. A changed
witness is a miss; changed stored bindings or owner identity are refused;
missing premises remain refused independently of hits.

This preserves the existing checker-assumption boundary. It does not establish
new Lean correspondence, cryptographic soundness, hostile in-process isolation
or a persistent acceptance trust mode.

Within the supported finite warm-prefix case, when each previous prefix fits,
native invocations can fall from n(n+1)/2 to n. Parsing, transferred proof bytes,
current premises, semantics and closure remain cumulative. Reservations remain
unchanged; no extra admissible work under a fixed reservation grant follows.
An equally optimized comparator receives this same improvement. No numerical
end-to-end speedup, positive full-cost growth margin, economical new certificate,
cold-scale solution or v5 completion is claimed. No old circulation or proof
campaign needs repeating to review this source boundary.
