# Minimum ledger-backed peer integration

Source-based implementation plan, 2026-09-21. This note changes no Python and records no execution result. It was checked against the current `py/node.py`, `py/storage.py`, `py/checking.py`, `py/domains.py`, `manage.py` and [PEER.md](PEER.md). Historical experiment code/state remain outside this product change.

## Selected design

Add three ordinary owner-local request operations: `peer_find`, `peer_acquire`, and `expose`. Run them through the existing `Dispatcher.execute` reservation/prepare/commit/terminal pipeline. Keep the single local P1 registry, existing handles, SQLite transaction, current-head admission rule and native stage ledger. The service continues reading only immutable views; it never calls these operations remotely.

`peer_find` produces a client-owned remote selection, not a local mathematical candidate. `peer_acquire` produces a locally reconstructed candidate, not acceptance. `expose` builds a view from explicitly selected entries that completed the local `publish` gate, not from every acquired row. Existing `admit` remains the only subsequent receiving-context promotion operation.

The following invariants distinguish this from a standalone downloader followed by an unsafe database append:

1. Every network/write operation follows a committed local request/quota reservation.
2. A visible acquired offer contains only the receiver's reconstructed metadata and package pin, never a copied remote offer.
3. Candidate insertion, its receiver-owned handle and terminal response commit in one existing transaction.
4. A transfer failure, discovery result, duplicate acquisition or exposure does not advance a head or allocate a native stage.
5. An exposure selection requires a durable local publication marker committed with `publish`.
6. An exact terminal retry returns the old response without downloading, rebuilding a view or checking again. A historical response is not a current-availability promise.

## Public inputs and durable records

All operations keep the existing exact request envelope and caller ownership rules. They can be normal configured local-client operations: this is already a cooperative owner-authorized local interface, not new remote authority. `init` alone continues using the reserved `owner` client. There is no need to let the public request supply a port, URL, directory, source, checker plan or receipt.

| Operation | Exact proposed arguments | Main response |
| --- | --- | --- |
| `peer_find` | `{peer: configured_alias}` | `rows:[{remote, descriptor_id, formal_metadata, ...bounded transfer identity...}]`, catalog hash, `candidate_only:true`, `mathematicalAcceptance:false` |
| `peer_acquire` | `{remote: receiver_owned_handle}` | Existing/new local `candidate`, P1 snapshot, descriptor, `existing`, `candidate_only:true`, `mathematicalAcceptance:false` |
| `expose` | `{selected:[client_owned_candidate,...]}`; 1–32 distinct entries | Client-owned `view` handle, catalog hash and count; no acceptance |

Use `put_record("remote", client, data)` for selections. Data binds the configured alias and exact endpoint, adopted foundation, exact fetched catalog SHA-256 and the complete selected catalog entry. The config-bound record hash already provides a local immutable binding. No sender handle is adopted. The same remote handle can be acquired after later discovery; its bundle identity must not be silently updated. If its exact bytes disappear, return the transport's unavailability outcome.

Use `put_record("view", client, data)` for completed exposures. Data binds the new request-owned view directory, complete catalog hash, foundation, selected local entry identities and completion marker pin. The ordinary public response can return this opaque handle rather than a filesystem path. `manage serve --config ... --client ... --view ...` resolves the committed record locally and launches the service for its exact directory. The low-level helper accepts a path, but that is an operator primitive; a remote request never chooses it.

### Publication marker without a new table

The existing `records` table can supply an exact-key publication marker. For a local P1 entry, define data exactly as `{provider:"P1", sequence, descriptor_id}`; use `put_record("publication", "owner", data)` only in the successful `publish` commit transaction, after artifact checking and offer append/deduplication. Its normal config-bound handle is computable from those exact values, so exposure can perform a primary-key lookup and `record(...,"publication","owner")` verification without scanning records or adding a new index/table.

The marker asserts only that this exact immutable local entry passed the local publication path. It need not allocate political attribution or select a globally preferred proof. The checked artifact/source evidence remains in its existing artifact/request records. A repeated publication can insert the identical marker idempotently. Initialization and acquisition never create it. The publication marker and P1 append must commit with the terminal publication response, never in separate transactions.

If a new checked artifact is exactly the same package as a previously acquired offer, successful local publication may create its previously absent marker without another P1 entry. Merely receiving or admitting that candidate does not create the marker. The source/receipt binding still goes through `Checker.publication`.

## Config and operator changes

Fresh product configurations need these additions before initialization:

- A bounded `peers` mapping, at most two configured aliases, each `{host:"127.0.0.1", port:integer1..65535}`. Validate alias shape with the existing safe-ID rule. No URLs, DNS, redirects or peer-provided replacements. Select fixed ports before creating both immutable configurations; do not edit config after initialization merely because a service selected a new port.
- Pins for installed `peer_wire.py` and `peer_service.py`, included in operator process supervision and verified before lazy transport-module loading. They have no checker/source authority. Configuration and installation immutability remain trust premises, not proof of remote honesty.
- Explicit operation-specific work grants: suggested `peer_request_bytes=64 MiB` and `expose_request_bytes=80 MiB`, leaving ordinary `request_bytes=8 MiB` unchanged. All derive from local configuration and consume the existing total `staging_bytes` allowance.

The selected transfer maximum can retain 16 MiB canonical payload plus 1 MiB manifest twice: incoming bytes and the checker's normalized copy. A 64 MiB grant covers their bounded logical bytes and small local records. Exposure can retain 64 MiB of bundles plus catalog/completion data; a 64 MiB grant would be insufficient at its upper boundary, hence 80 MiB. These are logical-byte reservations, not a hard physical disk-block quota; file allocation overhead and free-space exhaustion remain local IO conditions.

Do not merely raise the ordinary request limit for all operations. Extend `ControlStore.reserve` to accept an internal operation-selected grant, or derive it from the already parsed operation under the immutable config. The selected amount must be used in the same transaction that increments requests, charges bytes and sets `meta.active`. Never add a second network-specific accounting database. Record the grant in request-local metadata/event or an added request grant column if desired; for this fixed cut it can be rederived unambiguously from immutable config and exact stored request bytes.

The config raw hash already makes these schema additions a new configuration identity. They do not migrate an initialized old state. `manage.configure` must emit them in new states; `node.load_config` must validate them. No need to change domain schema 2 solely for adding peer policy keys if its path-domain fields remain unchanged.

`manage.invoke` currently grants every call 450 wall/CPU seconds and 6,144 MiB. Select stricter outer limits for the new operations: metadata discovery is native-free; acquisition gets the declared transport plus parsing/rederivation allowance; exposure has its own finite hash/build allowance. Include the transport modules in the supervisor input pins. A service requires its own native-free process-tree supervisor with the specified 256 MiB memory/session limits, not a normal request wrapper that assumes `node.py` arguments. A direct unsupervised service launch cannot claim the full resource profile.

No shell expansion or arbitrary child command comes from a public request. Source submission keeps its existing separate, owner-authorized execution model.

## Exact call graph and preparation work

```text
manage request -> supervised node process
  -> load config / parse exact request / owner lock / ControlStore
  -> exact stored reply, if terminal
  -> reserve(request_id, operation-selected grant), committed
  -> Dispatcher.prepare: bounded network/checking/filesystem work
  -> one visibility transaction:
       commit_operation + receiver-owned records + terminal response
  -> emit stored response

later, separately:
  admit(current local context, selected local candidates)
    -> existing canonical/context gate + fresh native stage
    -> existing head commit
```

The owner writer lock remains held through each finite request, as in the current implementation. This serializes local acquisition against publication/admission and simplifies duplicate decisions. It is a deliberate small-slice availability limit, not high-concurrency design. Peer service reads only the separate immutable view, so its request handling does not need this writer lock.

### `peer_find`

After ordinary reservation, validate the peer alias; read the caller's already stored context description to obtain its adopted foundation. This is a config-bound historical foundation selection, not fresh acceptance. Call `peer_service.fetch_catalog(configured_port, foundation)`. It already returns the strict parsed catalog and exact fetched-byte hash. Prepare the bounded result without loading `Checker` or allocating native work. In the visibility transaction, insert client-owned remote records and commit the terminal response. The result remains an untrusted remote hint and does not append P1 entries.

The existing 64 KiB catalog bound plus at most 32 opaque handles fits the 1 MiB response cap. The 32,768-byte local P1 entry limit remains a separate later gate; a remotely advertised row can fit the catalog but still be too large to commit locally. Refuse this honestly. Do not claim that `encode(parsed_catalog)` reproduces the exact original wire bytes: its whitespace/order may differ. If recording exact raw catalog bytes becomes an evidence requirement, expose them explicitly from the transport helper; do not counterfeit them from parsed data.

### `peer_acquire`

Resolve `record(remote,"remote",client)` and validate its alias/endpoint/foundation binding before connecting. Reserve the larger work grant before any transfer. The operation chooses all paths below its own `state/work/<request-key>`; public arguments contain none.

There is an existing directory-creation collision to avoid: `Dispatcher.checking()` currently creates `state/work/<key>` with `exist_ok=False`. If acquisition creates that root first, later checker loading fails. The smallest coherent implementation is to call `self.checking()` once after selection guards and reservation, then choose its new `incoming` child as the transfer destination. This does load the checker before transfer, but launches no native stage and introduces no new path domain. Alternatively refactor request-root ownership explicitly; do not broadly change all directory creation to `exist_ok=True` and lose collision detection.

Call `peer_service.acquire(port, selected_entry, foundation, new_incoming_directory)`. Preserve exact `WireError.code` through a local `Refusal`, rather than burying transport outcomes inside `INTERNAL_ERROR`. If it fails, do not call `offer`, append P1 or promote a context. Complete/refuse only once the synchronous socket call has returned; it closes its socket in `finally` and creates no background worker. If the enclosing supervised process was terminated, use the pending recovery rule below instead.

On a successful transport return:

1. Require `mathematicalAcceptance:false`, the expected bundle digest/root and the exact local destination. These are consistency checks, not imported acceptance credentials.
2. Call fresh `self.check("offer", transferred["package"])`. This reopens selected bytes, checks adopted foundation and exact root closure/inventories, normalizes a local copy, and derives actual metadata. No native stage is allocated.
3. Compare the complete fresh `descriptor_id` and `formal_metadata` with the selected advertised values; also bind `formal_metadata.replay` to the selected/received root. Use type-sensitive equality (`S.same` or canonical JSON byte comparison), not Python's loose `True == 1` equality. Do not replace dishonest advertised metadata and silently call the different result a successful acquisition.
4. Keep only the fresh local offer as the prepared candidate. Peer endpoint/catalog identity stays in its separate acquisition record, never inside the mathematical offer structure.
5. Resolve exact duplicates as below; enforce entry-size/count capacity before commit. Recheck filesystem byte pins as required by the owner-controlled immutable-file premise.
6. In the existing commit transaction, append/reuse P1, create the normal client-owned candidate handle, record acquisition provenance as non-authoritative local bookkeeping, and terminalize the exact response. No head call is permitted here.

Use the existing stage allocator boundary defensively: for `peer_find`, `peer_acquire`, and `expose`, allocator invocation must refuse before `store.stage` charges or launches anything. Record/check zero stage allocations and pipeline children. Returning `native_stages:0` without such source/counter evidence is not the safety argument.

### `expose`

Resolve each selected candidate under the caller, its immutable P1 entry and the exact publication marker. Reject duplicate entry identities and absent markers before copying package bytes. Do not treat a candidate handle returned from acquisition as proof of publication.

For marked entries, revalidate selected local package pins and derive metadata against the current local checker before exposure, without a native stage. Compare full descriptor/formal metadata with the stored offer. Prefer `checker.package` plus `checker.metadata` on the existing package; calling `offer` here would needlessly copy it into a new request directory and defeat the 80 MiB exposure accounting. The marker already records the successful historical local publication gate; this operation need not allocate a new source or native verification stage.

Build only the selected view: `peer_wire.build_view(new_request_owned_view, foundation, validated_offers)`. Its manifest/bundle checks do not replace the preceding local metadata binding. The complete file marker is written last by the helper. Commit a config/client-bound view record and terminal response only after the view is complete and pinned. The service wrapper accepts only a committed view handle through its normal operator interface; existence of an orphan `complete.json` is not permission to serve it.

Do not needlessly invent a global snapshot protocol. This immutable finite view is one explicitly selected exposure cut. Another exposure after publication produces a new view record under a new request ID; older views remain honest historical cuts until their local retention policy removes them. The first slice can retain all charged views and refuse exhausted capacity rather than invent garbage collection.

## Exact duplicates and descriptor conflicts

Add one indexed store helper to look up an existing P1 offer by `digest(encode(descriptor_id))`, returning sequence and full raw offer. It uses the existing unique `(provider,descriptor_key)` index. Perform expensive content comparison in preparation, not inside the short commit transaction; the owner lock prevents another writer from racing that decision.

For a repeated exact package, ignore only the request-local package path difference. Require identical descriptor, type-sensitive full formal metadata, derived symbol keys, normalized manifest identity, root, inventory and canonical object set/content identities. Reopen/recheck the existing package before choosing it. Content hash equality relies on the declared SHA-256 assumption and the complete canonical package validation; it is not a theorem-equivalence heuristic.

The practical narrow rule can be: freshly normalize and validate incoming bytes; require the existing owned package's validated normalized manifest bytes/ID to match exactly; its complete validated closure and root must match. If manifest formatting differs on the wire, the locally normalized copy can still agree. If normalization/inventory order or proof content differs, conservatively refuse `DESCRIPTOR_VARIANT_UNSUPPORTED`; no need to decide semantic equivalence for this cut.

On equality, pass the original existing offer unchanged to `append`, allowing the existing full-record equality check to succeed and preserving its original local package path. Retain/charge the new request's copied bytes for now; do not silently delete them or refund quota. Reusing an offer does not mean a new request had no cost. Apply this helper to local `publish` too, so publication of an exactly matching already-acquired artifact can create the marker without a false local-path conflict.

Same terminal request ID: no new transfer or charge. Same bytes under a new request ID: a new bounded reservation/check may occur, but no duplicate P1 entry or native stage. Same request ID with different bytes: existing `REQUEST_ID_CONFLICT`. Same descriptor with different supported package: explicit variant refusal, preserving the old entry/head/publication marker.

## Accounting and failure gaps that must be closed

`selected_work_bound` currently uses ordinary `request_bytes` and a 16,384-file ceiling. A maximum acquisition retaining two 8,192-object packages plus two manifests needs at least 16,386 files. Select a prospective peer work-file ceiling such as 16,448, and use the operation's actual reserved byte grant; otherwise valid upper-envelope acquisition can fail after successful transfer/checking for an unrelated fixed bound. Enforce/census on both successful preparation and safe error exit, not only inside `self.check` after normal completion. Framing limits remain the streaming bound; a final census is an observation, not its replacement.

The larger grant must not be charged by `stage()`: that would consume native capacity and confuse zero-native observations. Keep acquisition and exposure within the request grant, using the existing request counter and `meta.charged`. Native stage grants continue only for the existing native operations.

`Checker.import_package` currently writes its normalized copy through `export_package`, whose ordinary file writes do not explicitly fsync. Before a new package becomes a durable visible offer, flush/fsync the selected immutable copied files and manifest, then verify their pins before the SQL visibility commit. Apply the same reasoning to exposing a view: bundle/manifest helpers fsync file contents, but directory-entry/power-loss durability requires platform-specific treatment. Declare the supported guarantee precisely: process interruption with completed file writes is not automatically full sudden-power-loss durability. A complete power-loss ordering claim requires its own filesystem flush strategy and test; do not cover it with SQLite `synchronous=FULL` alone.

| Interruption boundary | Required state/result |
| --- | --- |
| Before reservation commits | No network or new package/view directory; ordinary pre-reservation refusal/uncertainty rules |
| After reservation, during transfer/check/copy | Pending request and charged non-visible files; no entry/marker/view/head promotion |
| After files complete, before SQL commit | A non-visible orphan may remain; do not infer acquisition/publication from filesystem existence |
| During P1/handle/terminal transaction | All visibility rows and terminal response commit together or roll back; unchanged old head |
| Commit succeeded, stdout lost | Exact-byte retry retrieves the stored terminal response; it does not rerun network/checking |
| Normal refusal after malformed bytes/IO error | Retain charged evidence/incoming data; atomically store exact refusal and clear active request once the current operation is quiescent |

No new ledger is required to represent these states. The existing `requests.phase`, `meta.active`, terminal reply and immutable records suffice for this finite slice. The missing part is an explicit safe recovery command, not a permission to manually clear `meta.active`.

### Minimum native-free pending recovery

Provide an owner-local recovery path restricted to pending `peer_find`, `peer_acquire` and `expose` requests. It must validate the exact stored request/config, assert that no native stage record belongs to that request, and consume locally authenticated supervisor evidence that the exact original node process tree is empty and the direct child reaped. A missing process, lock or Python exception by itself is insufficient. Do not import a peer's receipt or expose this recovery operation over HTTP.

If already terminal, preserve and return the existing exact result. If genuinely pending and quiescence is established, atomically record a terminal refusal such as `INTERRUPTED_PEER_OPERATION` and clear only that request's active slot via the existing `terminal` method. Leave partial files and quota charges intact. A fresh request ID may then retry with a fresh directory. If quiescence cannot be established, remain blocked and diagnosable; do not infer safe completion or fabricate a successful candidate from orphan files. Native-operation recovery is outside this narrowly justified command.

## Required integration checks before the two-node run

These are additional to the transport's independent unit tests:

- `peer_find` is checker/native-free, charges exactly one ordinary request grant, binds each handle to the local client/config and does not append P1.
- Unknown alias/foreign handle/changed selection refuses before network. The configured endpoint, not a response field, controls the connection.
- Oversized/malformed transfer preserves head, native counters and P1; exact error code survives `WireError` conversion. Its permitted request/accounting/filesystem deltas are recorded.
- Coherent but false advertised metadata passes the transport shallow shape gate, then fails type-sensitive local rederivation comparison without candidate visibility.
- Successful acquisition followed by the same request replay performs no network; new-request duplicate reuses the same P1 sequence despite a different work path. Variant refusal preserves existing data.
- Acquired/admitted-but-unpublished candidates cannot be exposed. Successful ordinary publication creates the marker atomically, including publication of an exact already-acquired offer.
- A failed exposure never yields a committed servable handle. A complete orphan directory is not selected by normal `manage serve`.
- Inject one supervised native-free acquisition interruption, preserve the actual supervisor result, recover only with confirmed quiescence, and retry under a new request ID. No broad deletion or counter reset.
- Stop the sending service after acquisition and before receiving admission. Both local admission and needed formal-body inspection use only retained local bytes.

After these checks, the planned two independently installed nodes can exercise G-to-H reciprocal reuse without a root-only plan patch or direct database promotion. This closes the local transport/storage/checking boundary; it still does not establish autonomous discovery, unrestricted Lean support, large-scale retrieval quality or sustained useful mathematical growth.
