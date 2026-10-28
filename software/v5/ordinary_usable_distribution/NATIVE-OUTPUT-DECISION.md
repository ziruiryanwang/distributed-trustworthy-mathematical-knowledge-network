# Native output limit: source feasibility decision

2026-10-28. Source-only. Read with `RELEASE-BLOCKERS.md` and the independent
`OUTPUT-GRANT-PATH.md`. Current adopted kit and native support remain unchanged.

## Decision

The pinned serializer already constructs the full selected snapshot in memory.
This permits a conservative per-artifact bound from the existing hard native Job
private-commit ceiling `M`, under the allocator/OS premises below. Reserving
`M + 88` bytes separately from the successful-output cap would need no serializer
change. It would require a deliberate accounting change and larger failed-call
charges; the current 64 MiB reservation does not provide this guarantee.

An exact pre-write limit equal to the smaller output cap is also technically
straightforward at the native save boundary, with no second full serialization
buffer. But the installed Lean API exposes no supported hook for it. Merely
forwarding the grant into existing snapshot `Limits` still checks after writing.

No code, native rebuild, runtime patch, OS quota setup or experiment is selected
by this result. Prefer evaluating the conservative existing-Job accounting option
before a version-specific C++ change. Retaining the explicit operator-storage
premise remains reasonable if tighter public-input storage accounting has little
practical benefit. This is resource hardening, not a false-acceptance repair.

## Exact pinned path

Bundled `Lean/Environment.lean:1792` implements `saveModuleData` with
`CompactedRegion.save fname mod data #[] none`. Bundled
`Lean/CompactedRegion.lean:95` binds that opaque operation to
`lean_compacted_region_save`; its only optional behavior is closure support,
which defaults to false. Therefore the ordinary writer uses the v2 format,
one fresh compactor, no dependency-region borrowing and no prior part.

Root authorized a bounded retrieval of the implementation at exact revision
`293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`. Five original source files and their
URLs/SHA-256 values are retained under
`research/references/lean-293d5d0-output/PROVENANCE.md`. No upstream source was
executed. The defining `module.cpp:268-425` establishes this order:

1. Construct the compactor and derive its deterministic base address.
2. Open `chunk.olean.tmp.<pid>`.
3. Reserve the header in memory and write the v2 header to the temporary file.
   On the pinned 64-bit target the header is 88 bytes.
4. Run `compactor(odata)`, constructing the complete compacted object graph in
   memory. The buffer includes the reserved header and root-address slot.
5. Write the compacted body from `compactor.data()` using its exact size, close
   and check the stream, then rename the temporary file to the requested path.

With the actual fresh-compactor call, the final file length is exactly
`compactor.size()` after step 4. In the general multipart implementation it is
`compactor.size() - file_offset`. The header is not a compressed-size estimate;
this is the actual byte count passed to the writer. The current code checks no
grant at this point. A process kill can also leave the temporary file, so a
future physical bound must cover temporary and final paths, not just final stat.

## Conservative bound from the existing Job

`compact.cpp` allocates its buffer with ordinary `malloc`, copies used bytes on
growth, and zero-initializes every new used span with `memset`. Its included
`util/alloc.h` specializes STL allocators but does not override `malloc`; the
installed `lean.h`/`mimalloc.h` likewise provide no such macro replacement.
The complete `S`-byte output prefix therefore occupies initialized private heap
storage before the body write. The current call starts fresh (`prev = none`),
with no external dependency regions and no chained parts.

The existing supervisor sets `JOB_OBJECT_LIMIT_JOB_MEMORY` and the selected
aggregate `JobMemoryLimit = M` before resuming the native process tree. Under the
existing trusted Windows/allocator premise that this ordinary initialized heap
is charged private commitment and the Job cap is enforced, `S <= M`. Other live
state and resize overlap consume that same budget and only reduce the available
output-buffer space. This argument does not confuse working-set residency with
commitment: paging/compression does not turn the initialized heap into uncharged
file-backed storage. A replacement allocator using uncharged shared backing,
unsupported runtime changes or broken Job enforcement would invalidate it.

Before compaction finishes, at most the 88-byte header has been requested for
the artifact. Afterward, partial or full body writes are prefixes of the same
`S`-byte buffer. The temp file is renamed, not copied, and the fresh grant has
one save. Since supported `M >= 1 MiB`, total logical content of the grant's
temporary/final artifact is at most `M`; `R = M + 88` is an intentionally looser
per-call reservation that avoids relying on the header being inside the buffer.
This includes a worker killed during writing. It bounds file-content bytes,
not filesystem allocation units or metadata.

An accounting successor could retain the successful cap `q` (normally 64 MiB)
while reserving `R` before launch. Success already reduces the ledger charge to
actual size; failures must retain the full conservative reservation. At the
guide's 1280 MiB Job allocation, that reserve is about 20 times the current
64 MiB charge; an 8192 MiB allocation needs correspondingly more capacity even
for small intended results. Catalog capacity/allowed allocations, public budget
meaning, grant bindings and support identity would need coordinated review.
Existing catalogs cannot silently inherit stronger accounting claims.

This does not yet give a whole-operation physical quota. Controller call files,
report, supervision metadata and logs are separate. In particular log ceilings
are sampled at 50 ms intervals, so their configured limits are not hard write
caps. The independent `OUTPUT-GRANT-PATH.md` records these boundaries. Do not add
nominal log/spool limits to `R` and claim a total hard bound without closing their
write paths. No additional C++ investigation is needed for this decision.

## Minimum seam and its limits

The smallest exact native design would carry the controller's validated output
grant through the fixed worker into the save operation. After compaction, compare
the full v2 length with that grant before opening the temporary file or writing
the header. If it is too large, return refusal with no artifact bytes; otherwise
the existing header/body/close/rename sequence writes at most the grant. Keep
the current post-write and catalog commit checks as independent consistency
checks. Apply the same grant contract to basis and extension writes. Keep parent
snapshot load limits separate from the new-output bound.

The source-level theorem is conditional on the existing trusted runtime,
exclusive fresh output path and correct arithmetic/IO premises: a single save
either refuses before opening its artifact, or attempts at most `q` bytes across
its temporary/final representation. Rename moves the same file. Since failed
grants remain charged, this would make the snapshot reservation meaningful for
retained snapshot bytes as well as accepted bytes. It would not bound separate
call spool, logs, filesystem metadata, backups or all same-account writes.

| Available boundary | Feasibility |
|---|---|
| Current Lean `saveModuleData` / `CompactedRegion.save` | No cap or pre-save buffer/size primitive; cannot enforce the exact pre-write condition with the current API. Returned `Compactor` is opaque and arrives after saving. |
| Native `object_compactor` | `compact.h` declares a `LEAN_EXPORT` C++ class with public `size()`, `data()` and `alloc()`. These primitives can support a new native implementation. They are internal C++ interfaces, absent from the installed development headers. |
| Small change inside `lean_compacted_region_save` | Reuses existing compactor and format writer; requires a new cap-bearing native API and rebuilding/qualifying selected runtime support. No runtime patch is presently selected. |
| Separate C++ helper using that class | Could avoid modifying the runtime, but requires compatible internal headers/linkage and ownership of the version-specific header/save logic. `module.cpp` keeps the header and opaque-handle access helpers private. Exported class visibility alone does not establish a stable supported ABI or drop-in helper. |

Thus a runtime change is not logically the only possible implementation, but no
supported Lean-only fix or already-installed bounded-save operation was found.
Do not cast the opaque handle or duplicate object layouts to evade that boundary.
Stream polling, post-write deletion and lowering the existing 1 GiB size check
also do not prove a pre-write bound.

## Resource estimate

`compact.cpp:138-181` starts with a 1 MiB buffer and doubles capacity as needed.
At a resize it allocates the new buffer, copies the old contents, then frees the
old buffer. If peak compactor demand is `H`, its capacity `C` is the least power
of two MiB at least `max(H, 1 MiB)`; a resize temporarily retains at most
`C + C/2` bytes of these two buffers. The live checked environment, decoded units,
pointer-identity table, structural-sharing table and recursion scratch are
additional. Structural sharing can roll back the buffer end, so final file size
alone is not a complete peak-memory estimate.

An exact post-compaction/pre-write check adds no second buffer or graph traversal
to the current save. It still permits a large rejected candidate to consume
memory before refusal. The existing aggregate Windows Job private-commit limit
remains that resource boundary. Public calls require an explicit `memory_mib`
(1 through 8192 MiB); the guide's owner example uses 1280 MiB. That number cannot
be treated as a proof that a particular live parent plus candidate will fit.

A separate cap inside `alloc` could bound compaction growth itself, but changes
the native API/allocator and may conservatively reject a transient candidate
whose deduplicated final output would fit. If it bounded peak demand by a 64 MiB
grant, the buffer capacity would be at most 64 MiB and its largest resize would
temporarily hold 96 MiB, plus all other state. This is a source estimate for that
unimplemented design, not an observed cost or current guarantee. It is unnecessary
for the narrower exact disk-output check and should not be added automatically.

The feasibility question is closed. The lowest-change candidate is conservative
artifact accounting based on the existing Job, with spool/log scope kept explicit.
An exact smaller native cap is a separate maintenance choice. Another unchanged
admission run cannot decide which cost/coverage tradeoff is worthwhile.
