# Native output grant: source-only path and retention audit

2026-10-28, query_scaling. **The default 64 MiB grant bounds catalog reservation
and successful admission, not physical snapshot writes. Failed oversized chunks
remain on disk while future calls count only their original reservation.** This
is a storage-accounting gap, not a bypass of mathematical admission. No runtime,
import, owner/database access, source edit, Git operation or experiment occurred.

Selection is current `ordinary_reply_capacity/source-map.json`, SHA-256
`05d96f671ecb755b20bcb55d0a93a33a8e70abdaa559017c750635deaba1eef5`.
The selected source and the extracted kit's package copies rehash identically for
all eleven inspected path components (admission, two catalogs, worker, snapshot,
basis, owner, peer, peer API, contribution and author worker). In particular:

| Source under `software/v5/` | SHA-256 |
|---|---|
| `ordinary_parse_reuse/ordinary_admission.py` | `98c88eb0e7ea5e101f6ccd8e94b56a0cc248167c317a0440ba00dc86f503cd9a` |
| `ordinary_lean/portable_catalog.py` | `aeaf0c7d507baa6b63d401c432ca71557bf29b6b576b1f6cd8381e4e87c7473e` |
| `ordinary_kernel_admission/OrdinaryWorkflowWorker.lean` | `eaed9462acec910e89591e8d9969a34531e792594ff4f3315503d33d887a8be9` |
| `ordinary_kernel_admission/LocalSnapshot.lean` | `ae8bc1c9d2e8e01c293d9757d3ab2db744a6a65c2281c965406bdaba993e0f95` |
| `ordinary_lean/BasisSnapshot.lean` | `8952d82460d972e4176becdc0f16e09015ccf8298c37898b55e7b7959057727a` |

## Where the grant stops

`OperationBudget` defaults `output_bytes` to 64 MiB and permits a direct API caller
to choose 1 byte through 1 GiB (`ordinary_admission.py:321-340`). Both initialize
and new-unit admission pass that value to catalog reservation (`:573-574,608-609`).
`portable_catalog.py:551-583` checks the per-artifact catalog ceiling and the sum
of every operation's `reserved_bytes`, plus import charges, before adding the new
reservation. Default catalog limits are 1 GiB per artifact and 4 GiB total
(`ordinary_lean/local_catalog.py:77-86`).

The exact native command carries mode, two input paths, root, output path and
report path; it carries no output-byte grant (`ordinary_admission.py:645-655`).
The Python internal worker accepts exactly eleven arguments and forwards the
six-field command to Lean (`:719-751`). `OrdinaryWorkflowWorker.lean:185-227`
calls basis/snapshot writers without an explicit snapshot limit. The unrelated
`author_worker.py` is the trusted source-authoring route, not this admission shim.

The selected `LocalSnapshot.lean` is under `ordinary_kernel_admission`, not
`ordinary_kernel_validation`. Its default `maxArtifactBytes` is 1 GiB (`:17-23`).
Its fresh extension writer calls `saveModuleData` before `ordinarySize`; the basis
writer has the same order. Therefore merely forwarding 64 MiB into the existing
post-write check would not establish a pre-write cap.

## Success, failure and durable authority

A successful native event must be cleanly closed. Python then binds report fields,
module/parent/names/unit census and exact artifact size, requiring size at most
`budget.output_bytes` (`ordinary_admission.py:662-683`). Catalog commit separately
requires exactly one `chunk.olean`, size at most its stored reservation, hashes and
flushes the artifact, and atomically inserts the root while replacing the
reservation with actual size (`portable_catalog.py:637-685`). A saved report or
leftover native file cannot create this live authority.

Clean failure calls `abandon`: it changes state to `FAILED_RETAINED` without
measuring, deleting or changing the original byte reservation
(`portable_catalog.py:780-784`). Reopening similarly changes `RESERVED` to
`INTERRUPTED` without changing its charge (`:237-238`). Cleanup uncertainty instead
withdraws/closes the catalog (`ordinary_admission.py:693-711`). Failed and
interrupted rows remain included in future `sum(reserved_bytes)` queries; there is
no state filter (`portable_catalog.py:558-560`). Thus failure is charged, but an
oversized failure is undercharged relative to its retained physical chunk.

For example, a completed 96 MiB artifact under a 64 MiB reservation can pass the
writer's default size check and then be refused by Python, leaving 96 MiB retained
and 64 MiB charged. An artifact over 1 GiB can be refused by the writer only after
its write, also leaving bytes. Interrupted/failed writes may leave partial files.
These are source implications, not claims that such cases have been executed.
The ledger proves a bound on recorded charges, not on those retained file sizes.
Neither deletion of failed evidence nor retry/reset authority follows.

Existing protected parent artifacts have a different boundary: catalog context
checks their selected sizes/digests before native use (`portable_catalog.py:319-331`),
and `restoreLocal` checks each existing file's size plus 4 GiB aggregate before
import (`LocalSnapshot.lean:197-269`). These are pre-load input checks. A new output
grant must not silently lower limits for already admitted parent snapshots.
Exact reused units have no new native snapshot reservation/write; inert custody
staging still precedes the `REUSED` return (`ordinary_admission.py:599-603`).

## Public scope and decision

The current owner/receive CLI uses the 64 MiB default; it exposes no per-admission
output-byte option (`owner.py:156-161,544,580,601,611,619`; `peer_api.py:700`).
Init-only `--catalog-limits` sets catalog ceilings. Producer-only `--spool-mib`
(144-256 MiB) is a separate bundle allowance and is rejected for normal owner
operations; it does not change this snapshot grant. A distinct read-only subreview
confirmed these public paths.

Memory has no public default: owner/peer require `--memory-mib`, accepting 1-8192
MiB. The guide's owner-launch example selects 1,280 MiB and its direct source-build
example selects 2,048 MiB; these are example allocations, not a derived output
limit. The native allowance forwards the selected memory value to the Job's
aggregate private-commit limit (`supervisor/run_stage.py:235-238`), alongside
process/user-CPU controls. Direct owner Python checks remain cooperative; the
public outer launcher additionally encloses the controller and descendants.
Nested Job CPU is already included in the outer figure. No reviewed argument
derives a disk bound or a serialization-size cap from this memory allocation.

Selected documentation does not promise a whole-workflow hard physical disk cap:
`LAUNCHER.md:107` explicitly denies one; `EXECUTION-TRUST.md:43-46` denies a filesystem
sandbox; GUIDE calls example ceilings non-capacity promises. Admission's own
module docstring discloses retained staging/call spool and separate spool disk
capacity. Its phrase "charged snapshot staging" is accurate only as reservation
accounting when a failed writer exceeds the reservation. Catalog quota must not
be presented as a physical bound over successful plus failed artifacts, much less
custody, call spool, SQLite journals, source compilation and logs together.

The smallest candidate seam is to carry the exact grant into the fixed worker and
apply a separately named fresh-output cap at serialization, preserving existing
input limits. A proved bound before writing or a genuinely bounded serializer
sink is needed; forwarding a value to the existing post-check is insufficient.
Serializer feasibility belongs to next_value's companion review. If that boundary
is not cheaply available, retain an explicit independently bounded scratch-storage
premise, or record overrun and quarantine before further calls, without relabeling
post-write detection as prevention. Accurate failure charging alone cannot undo
an earlier disk overrun. No implementation or storage setup is selected here.
