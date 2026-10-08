# Ledger-backed peer operations: implementation handoff

Authored source cut, 2026-09-21. Pending independent source review and root-only execution. This change touches `py/node.py`, `py/storage.py` and new `py/peer_node.py`; it does not alter canonical mathematics, native support, historical experiments or the peer wire/service implementation.

## Configuration and calls

Fresh schema-2 configurations now require `peers`, with zero to two safe local aliases mapped to exact `{host:"127.0.0.1",port:1..65535}` values. The limits require exactly `peer_request_bytes:67108864` and `expose_request_bytes:83886080`. Installed pins for `peer_wire`, `peer_service` and `peer_node` are mandatory and verified before lazy peer loading. Existing initialized configurations are not migrated or edited in place.

New local request operations use the unchanged envelope:

| Operation | Exact args | Result |
| --- | --- | --- |
| `peer_find` | `{peer:alias}` | Client-owned `remote` handles plus candidate-only catalog rows/hash; no checker load |
| `peer_acquire` | `{remote:handle}` | Locally checked/rederived P1 candidate, snapshot, duplicate indicator and non-authoritative acquisition record |
| `expose` | `{selected:[candidate,...]}` | Committed immutable `view` handle, catalog hash and selected count; published entries only |

All three responses explicitly carry `mathematicalAcceptance:false`, `native_stages:0` and candidate-only/untrusted labels. `peer_find.complete` means only the fetched bounded peer catalog. It does not describe all local or global mathematics.

Transport endpoint and paths come only from configuration and request-key-derived local directories. Remote selections bind the exact local client/config, alias/endpoint, foundation, complete selected row and original catalog digest. A changed remote handle or caller is not accepted. No response chooses a URL, path, source, receiver context or acceptance policy.

## Ledger, package and publication behavior

The existing request transaction reserves capacity before any network or checker work. `peer_acquire` uses its 64 MiB grant and `expose` its 80 MiB grant; other operations keep ordinary request capacity. New requests retain their complete reservation, including refusals and exact duplicates. There is no implicit refund, deletion, background transfer or new accounting database. Grant choice is rederivable from the exact stored request and immutable config; the event records the granted amount.

Acquisition initializes the checker only after resolving the local selection, which exclusively creates the request root; transfer then creates a new `incoming` child. Fresh `Checker.offer` performs the full selected-package/closure checks and local metadata derivation. Complete advertised metadata is compared using canonical JSON bytes, distinguishing booleans from integers. Acquisition never runs a native stage; the dispatcher allocator explicitly refuses all native allocation for the three new operations before calling the stage ledger.

An indexed descriptor lookup detects duplicates. Reuse requires exact descriptor/metadata/symbols, matching validated normalized manifest hashes, roots, closure IDs and inventories. Both local packages are revalidated. On equality the original offer, including its old path, is passed unchanged to the existing append method. A genuinely different package under the same descriptor refuses `DESCRIPTOR_VARIANT_UNSUPPORTED`. The same helper is used by local `publish`.

Selected visible package files and their manifest are checked against expected bytes/hashes and fsynced before the visibility transaction. No mathematical bytes are rewritten. This is a process-interruption-oriented durability measure, not a claim of complete sudden-power-loss ordering: directory-entry flushing and hardware/filesystem failure semantics are not qualified here. The receiving package/file cache and filesystem remain owner-controlled.

Local `publish` still first authenticates the checked artifact through `Checker.publication`. Its commit now also stores a deterministic owner-scoped `publication` record whose data is exactly `{provider:"P1",sequence,descriptor_id}`. Initialization, acquisition and admission do not create this marker. Publication of an exactly matching already-acquired offer can create the missing marker without another P1 entry. No political attribution policy is added.

Exposure checks each selected client's candidate handle and exact publication marker before package work. It rederives stored offer metadata without copying those packages again, builds a new bounded view, and commits its record with the terminal exposure response. The record data is exactly:

```text
{kind:"peer_view", directory, foundation,
 catalog:{path,bytes,sha256}, complete:{path,bytes,sha256},
 selected:[{provider:"P1",sequence,descriptor_id,publication}],
 mathematicalAcceptance:false}
```

The directory is `state/work/<request-key>/peer-view`; the pinned files are its exact `catalog.json` and `complete.json` children. Root's service wrapper must resolve this committed client-owned record, verify pins/domain, close its database reader and only then start the finite read-only service. A completed but uncommitted orphan view is not a normal servable handle.

Acquisition appends/reuses P1, creates its candidate and acquisition bookkeeping, and terminalizes the response in one existing transaction. No current head changes. Exposure/publication records likewise commit with their operation's response. Exact terminal request retry returns stored bytes before reserving or doing network/file work. A new request for duplicate content can legitimately have new costs.

## Bounds and remaining gaps

Peer-operation work census uses its actual reserved byte grant and a 16,448-file ceiling, sufficient for two maximum 8,192-object packages plus manifests. It runs before commit and on quiescent failure paths. Wire limits remain the streaming enforcement; the census does not provide a hard transient or physical disk-block quota. Outer process-tree CPU/wall/memory supervision remains mandatory and is owned by the operator wrapper. Metadata rederivation, fsync and exposure hashing are selected local work, not free metadata lookups.

Pending recovery is deliberately **not implemented** in this cut, as root requested. Process termination may leave the existing active request pending with retained charged files. Neither these changes nor a missing lock clears it. The explicit next gap is a separately reviewed native-free recovery command requiring authenticated local process-tree quiescence; native pending recovery remains separate. No automatic retry, cleanup, capacity replenishment, context branching or retention reclamation was added.

The author did not import, execute or compile these sources. Required root tests include malformed transfer refusal, type-sensitive false-metadata rejection, exact terminal replay without network, new-request duplicate reuse, variant refusal, unpublished exposure refusal, marker/view transactional behavior, and offline admission after acquisition. Transport-unit-test success alone does not qualify these ledger changes or the two-node reciprocal system.
