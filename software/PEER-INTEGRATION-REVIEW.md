# Independent peer-integration source review

2026-09-21. Reviewed the author's stable `py/node.py`, `py/storage.py`, and `py/peer_node.py` against [PEER-INTEGRATION-PLAN.md](PEER-INTEGRATION-PLAN.md), including the actual checker, package codec, wire, and service interfaces they invoke. This reviewer did not import, execute, compile, open SQLite, launch a service, or run Lean. Only this review file was authored for the review assignment.

## Disposition

**No source-level blocker found for separately supervised, bounded integration checks of this cut.** This is not a runtime pass, mathematical acceptance, release qualification, or a finding that the complete integration plan has been implemented.

The central source boundaries are coherent: reservation precedes network work; remote hints are not candidates; locally reconstructed candidates are not admitted contexts; candidate/publication/view visibility shares the terminal-response transaction; only locally published entries can be exposed. Exact retries and new-request duplicates have distinct, appropriate behavior.

The planned native-free pending-recovery operation is explicitly deferred by root and absent from this cut. That remains an operability gap, not a solved condition. A killed request can leave the single active slot pending and prevent further requests. The bounded success/refusal path can be tested now; interruption recovery and sustained unattended operation cannot be claimed from this source.

## Scope and premises

The review assumes the declared cooperative owner-controlled installation/filesystem, immutable configuration, the selected Python/SQLite/Windows profile, and the separately reviewed process-tree supervisor. SHA-256 content/handle binding relies on its collision and second-preimage resistance. Local aliases and client ownership are not authentication against an adversarial OS user.

The transport remains literal same-host loopback HTTP with a bounded selected catalog. This review neither upgrades it to multi-host deployment nor treats peer service identity as a mathematical trust anchor. Peer bytes may be malicious; installation code and locally pinned configuration are trusted. No peer-provided source, executable, checker plan, receipt, path, URL, or receiver head is made authoritative.

The operator wrappers in `manage.py` and the forthcoming service worker are outside this source cut. They must independently enforce the declared receiver/service memory, wall, CPU, output and process-tree limits, and restrict serving to committed view handles. The integration source alone cannot supply those outer guarantees.

## State-transition argument

Let `H` be current client heads, `E` the P1 entries and provider snapshot, `P` publication markers, `V` committed view records, and `R` request/terminal records. For a new request, `Dispatcher.execute` first chooses the immutable operation-specific grant and calls `ControlStore.reserve`; only after that transaction commits does preparation run. Preparation performs read-only ledger lookups and selected filesystem/network work, not candidate or head insertion.

All visibility changes listed below occur inside `Dispatcher.execute`'s single `store.transaction()` together with `terminal(key, reply)`:

| Operation | Prepared evidence | Permitted visibility changes | Invariants |
| --- | --- | --- | --- |
| `peer_find` | Strict fetched catalog and its exact wire-byte hash | Client/config-bound remote-selection records; terminal reply | `H`, `E`, `P`, `V` unchanged; checker/native-free |
| `peer_acquire` | Locally normalized package, rederived metadata, exact advertised correspondence, duplicate decision, selected file seals | Append/reuse `E`; candidate/acquisition records; terminal reply | `H`, `P`, `V` unchanged; no native stage |
| `expose` | Client-owned candidates with exact publication markers; locally rederived offers; completed selected view and pins | View record `V`; terminal reply | `H`, `E`, `P` unchanged; no native stage |
| Ordinary `publish` | Existing artifact gate, then validated exact duplicate handling and selected package seal | Append/reuse `E`; marker `P`; candidate; terminal reply | `H` unchanged; acquisition alone cannot create `P` |

`PeerOperations.commit` has no `set_head` call. Receiving `admit` remains a separate operation using the existing current-context guard and fresh native checking. `publish` still invokes `Checker.publication` before the new publication helper. The new code does not replace that artifact/source/receipt binding with a peer claim.

An exception before the visibility transaction leaves no new visible candidate, marker or view. Under the declared SQLite atomicity premise, the visibility transaction commits the complete set or none; its context manager attempts rollback on an exception. A failed or uncertain commit must not simply be assumed to have rolled back. Ordinary quiescent refusal attempts to store a terminal refusal in a separate transaction; if the active-slot/terminal outcome cannot be established or persisted, the code returns uncertainty, not a fabricated success. Exact retry consults the stored terminal record first. Filesystem existence alone does not create a ledger record. The owner lock spans preparation and commit, preventing another cooperating writer from racing the prepared duplicate decision.

## Detailed boundary checks

### Selection, acquisition, and native separation

`node.load_config` bounds aliases to two literal loopback endpoints, validates integer ports, and binds the three peer-module pins to exact installation paths. `Dispatcher.peering` authenticates all three files before loading the integration module; `PeerOperations.__init__` checks the imported transport modules' actual paths.

`peer_find` uses the caller's stored current context only to obtain the adopted foundation. It does not load `Checker`, append P1, or claim fresh verification. Remote records bind caller/config, configured alias and endpoint, foundation, full selected entry and the actual fetched catalog hash. That hash is not reconstructed from re-encoded JSON.

`peer_acquire` resolves the caller-owned remote record, checks endpoint/foundation correspondence and entry shape before connecting, and creates the request root through `Dispatcher.checking` before selecting its new `incoming` child. This avoids the prior exclusive-directory creation collision. Its successful transport return is explicitly nonaccepting and bound to the selected destination/digest/root.

Fresh `Checker.offer` validates the canonical package and exact root closure, normalizes a local copy, and derives the receiver's metadata. The integration then compares full descriptor/formal metadata and replay root using encoded JSON equality, which distinguishes booleans from integers. A coherently advertised false type therefore is not silently replaced with a different successful candidate. Only the locally produced offer proceeds toward visibility.

`Dispatcher.allocate` refuses `peer_find`, `peer_acquire` and `expose` before `store.stage`. The peer methods directly launch no native child. `PeerOperations.observe` additionally requires zero checker stage allocations, zero pipeline children and zero event stage allocations. This combines a source-level allocator boundary with counters; literal `native_stages:0` response fields alone are not the argument. The guard does not make arbitrary future source edits safe without renewed review.

`WireError.code` is preserved through `Refusal`. Synchronous socket calls close through the transport's `finally` block; ordinary peer-local IO failures are not reported as mathematical rejection or acceptance. The outer supervisor remains responsible if the node process itself is terminated.

### Exact reuse and publication

`ControlStore.descriptor` uses the existing unique descriptor index. `PeerOperations.reuse` checks entry size/capacity and, for an existing descriptor, requires exact metadata/symbol correspondence, validates both selected packages, and compares manifest commitments, roots, closures and inventories. It returns the original existing offer unchanged, preserving its local package path for the existing append-equality check.

This is conservative byte/content identity under the declared hash assumption, not semantic theorem equivalence. Differently represented or different-proof variants can be refused as `DESCRIPTOR_VARIANT_UNSUPPORTED`. Neither usefulness nor absence of semantically duplicated mathematics follows from it.

The same path is used after successful ordinary publication, so a matching already-acquired entry can acquire its previously missing publication marker without a second P1 entry. `mark_published` is called only in the ordinary publication commit path. The marker's deterministic data binds P1, exact sequence and descriptor; exposure verifies that exact owner-scoped record through indexed lookup. Initialization, acquisition and admission do not create it.

Exposure resolves all selected client-owned candidate handles and checks distinct entry sequences/publication markers before package reconstruction or copying. It rederives existing package metadata without another package export, then builds and pins the new request-owned view. A completed but uncommitted directory is still an orphan. Enforcing the corresponding committed-view-only service entry point remains the operator wrapper's separate obligation.

### Accounting, errors, and retention

Operation-selected reservation is ordinary `request_bytes` for discovery, 64 MiB for acquisition, and 80 MiB for exposure. It is charged with the request counter/active slot in the existing reservation transaction, before IO. The selected grant is recorded in the event and rederivable from immutable config plus stored exact request bytes; peers cannot choose it.

The request-local census uses that actual grant and a 16,448-file peer ceiling. Two 8,192-object packages plus two manifests require 16,386 files, below that ceiling. The census runs before visibility commit and on quiescent error exits; a census failure is itself converted to a retained refusal where terminal persistence succeeds. Streaming transfer caps, not this after-the-fact census, bound received data while it is materialized. Directory-entry overhead, disk blocks, transient allocations and physical free-space guarantees are not covered by logical-byte charging.

An exact terminal request replay returns stored response bytes before a reservation, peer load, network operation or file copy. A same-ID request with different bytes refuses. A new request ID for exact duplicate content remains charged and may repeat transfer/checking while reusing the P1 entry. There is no refund or cleanup that silently erases retained evidence. An old terminal success does not promise present availability of its files or peer endpoint.

### Durability boundary

Before candidate/publication visibility, `seal_package` checks the selected owner-state package and verifies each canonical object's byte count/hash plus manifest commitment through write-capable handles, then flushes/fsyncs them. It does not rewrite mathematical bytes. This also checks actual bytes against reconstructed expectations even where the request-local checker cache supplied the parsed package.

View helpers flush their selected output files and write the completion marker last. The ledger then records exact catalog/completion pins. These are coherent process-interruption-oriented ordering measures under the owner-controlled filesystem premise. No directory-entry flush strategy, hardware guarantee or power-failure experiment establishes a stronger power-loss claim. SQLite `synchronous=FULL` alone is not a proof that all external package/view files are power-loss durable.

## Remaining qualification obligations

The following are requirements for later evidence, not failures inferred from unexecuted tests:

- Exercise unknown alias/foreign selection, malformed or oversized transfer, and coherent false metadata; show exact refusal, unchanged head/P1/native counters, and legitimate reservation/retained-file deltas.
- Exercise exact request replay with the sender stopped, new-request duplicate reuse, and conservative descriptor-variant refusal. Record request/counter differences rather than calling all duplicate behavior free.
- Show acquired and admitted-but-unpublished entries cannot be exposed; show ordinary publication creates the exact marker, including for an already-acquired identical offer.
- Show exposure produces a committed servable handle only after completed local validation, and that the operator wrapper cannot serve an uncommitted orphan by normal handle-based invocation.
- Stop the sender before receiving admission and body inspection; demonstrate those later steps need only retained receiver-local bytes.
- Implement and independently review authenticated native-free pending recovery before claiming recovery. Then inject an actual supervised interruption, prove the exact original process tree is empty/reaped, preserve charges/partial files, terminalize only that pending request, and retry under a fresh ID. Missing locks/processes alone are insufficient evidence.

The planned recovery requirement is the one explicit implementation deviation accepted for this finite source cut. Existing transport tests and the separate owner-contract tests do not exercise these ledger-level scenarios. They cannot substitute for this evidence. Capacity renewal, garbage collection, branching contexts, public-network deployment, autonomous discovery and useful long-run growth remain outside the cut as documented.

## Reviewed source pins

The three integration sources and handoff note matched the author's declared stable hashes on readback. These are review identifiers, not a future execution allowlist; root must bind the complete worker/config/import closure for any run.

| File | SHA-256 |
| --- | --- |
| `py/node.py` | `986279A99EDE271CB1D2039F1433B02C2DCB7EB6D1940863AAA95E3E8C8A73CB` |
| `py/storage.py` | `2BEF745773269C0D80B8855FB40F2C38F36692B531D154C2597287BDDD492387` |
| `py/peer_node.py` | `99B7F3AF3C4C4E0B66827157E743A75EAC320A54D04E90C1E4A9912991A90B18` |
| `IMPLEMENTATION-PEER.md` | `DBB8F5BDC699B4A5F4336DF301A1303A03212C3F7CF9BFA52408E9DA0B223E2B` |
| `py/checking.py` | `13AFA1FA31F58F273C0364B9679FD56400587F2977EA24BDDD85AAD9471F840B` |
| `py/peer_wire.py` | `B4AAD584E9F6F6D83872501D277C1F1CDE79E5A89618EFBF1260497BEB8D4946` |
| `py/peer_service.py` | `58D355B183790E54C0BC5C96738E3AC0C2358AA1C65D0C1704D45E9EF8F28407` |

Source anchors for follow-up: `Dispatcher.execute` at `node.py:314`, allocator guard at `node.py:140`, publication commit at `node.py:305`, reservation/terminal methods at `storage.py:181`, descriptor/publication helpers at `storage.py:275`, acquisition at `peer_node.py:89`, reuse at `peer_node.py:134`, package sealing at `peer_node.py:175`, exposure at `peer_node.py:206`, and peer visibility commit at `peer_node.py:238`.

## Addendum: original-attempt association

Later on 2026-09-21, root supplied a six-line node/storage delta for narrow independent source review. The original pins above remain historical identifiers; this addendum does not retroactively change that cut or any test result. The archived `qualification/owner-01/source-cut/node.py` and `storage.py` match those original hashes. Read-only line comparison identified only the one added node line and five added storage lines described below. No import, compilation, execution, SQLite opening or recovery was performed during this review.

| Revised file | SHA-256 |
| --- | --- |
| `py/node.py` | `CC9ACD8B5E2E9E2957A9C56908A4F7CC1BBBE9A1D628D32B40100F9278A78AB0` |
| `py/storage.py` | `1D815B3C5CAA8209FB5F0811B4ED2FA9588240727DB0EF2E0512B6BA4C1A2DBF` |

The new `event["origin_directory"]` is assigned from the resolved event file's parent only after `node.main` validates that the event is a new file beneath the configured scratch domain with an existing parent. `ControlStore.reserve` then checks an available origin's absolute string representation and writes `put_record("attempt", "owner", {"request": key, "call_directory": origin})` inside the same transaction as pending-request insertion, charging and active-slot assignment. The record is config-bound by the existing `put_record` envelope. Failure to create it rolls back that reservation transaction; it is not a separate best-effort afterthought.

This closes the *association* gap: exact terminal or pending retries consult `prior` before reservation, so they cannot mint or replace the original attempt marker. A later receipt with equal request bytes but a different call directory is not evidence about the original execution. No event argument means no marker; a future marker-requiring recovery must remain unavailable for that attempt.

**No source-level blocker found in this narrow delta.** It records which invocation future recovery must authenticate; it does not itself prove that invocation was supervised, that its processes stopped, or that recovery is safe. The future recovery command must still require this exact marker, bind the original local supervisor receipt/command/request/config/worker to it, establish original-tree quiescence and direct-child reaping, restrict the operation to supported native-free requests with zero native-stage records, and atomically terminalize only the active pending request. It must not substitute a retry's event or an arbitrary matching-request receipt. No recovery operation or recovery-pass claim is added by these six lines.
