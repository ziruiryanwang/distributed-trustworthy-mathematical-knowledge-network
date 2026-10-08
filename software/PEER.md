# Bounded same-host peer transport

Current scope: bounded loopback transport, with passing retained transport,
installed reciprocal-use and negative-control audits summarized in
[CHECKPOINT](CHECKPOINT.md). Those outcomes bind their preserved source cuts;
they do not automatically qualify every later development change or independent-
host deployment. The [replica proposal](drafts/REPLICA-CUSTODY.md) and its
[source review](drafts/REPLICA-CODE-REVIEW.md) are now integrated into the mutable
development tree. Fourteen state contracts have an independent
[outcome PASS](qualification/replica-custody-contract-01/OUTCOME.md), using real
SQLite/locks but synthetic packages/quiescence and mocked preparation/supply.
The genuine [native02 outcome](qualification/replica-native-02/OUTCOME.md) now
passes exact received-byte replication, post-supplier-stop serving with missing
original custody paths, corruption refusal and fresh receiver-native substantive
proof reuse. All roles share one host; no independent-host claim follows.
The API and limits below describe the existing transport boundary. No public
deployment, indispensable central endpoint or borrowed peer acceptance is implied.

`py/peer_wire.py` imports only the standard library. `py/peer_service.py` imports that module and the standard library. Neither imports the checker, codec, SQLite, old experiments, Lean, a source author or a process launcher. The receiver must still run full package/closure validation, metadata derivation and a separate fresh local admission.

## Callable API

| Call | Result and responsibility |
| --- | --- |
| `parse_catalog(raw_bytes, expected_foundation)` | Strict bounded catalog dictionary; contents remain untrusted hints |
| `make_bundle(package_dir)` | Bounded filename-free bundle bytes; object syntax/CIDs checked, not root closure or native acceptance |
| `receive_bundle(stream, entry, expected_foundation, new_destination)` | New local package path/manifest pin, root/descriptor, `advertised_metadata`, bundle digest, `mathematicalAcceptance:false`, `native_stages:0` |
| `build_view(new_destination, foundation, offers)` | Owner-selected immutable view and parsed catalog; each offer supplies `package:{path,manifest_sha256}`, `descriptor_id`, `formal_metadata`; extra local offer fields are not transmitted |
| `fetch_catalog(port, foundation)` | `{catalog,sha256}` from literal `127.0.0.1`; no arbitrary URL |
| `acquire(port, entry, foundation, new_destination)` | HTTP acquisition followed by `receive_bundle`; no registry commit |
| `serve(view, port, ready=None, ...)` | Finite synchronous read-only service; optional new local readiness file; returns observations |

Failures use `WireError.code`. Local filesystem/socket failures may additionally raise ordinary `OSError`; owner wrappers must preserve these as local/transport failures, not mathematical rejection. No helper edits an existing destination. A failed transfer or view build may retain incomplete bytes; no helper silently deletes them.

The public service routes are only `GET /v1/catalog` and `GET /v1/bundle/<sha256>`. Bundle lookup is exact membership in the frozen view. Unknown/private routes return 404; malformed HTTP closes the connection with a diagnostic recorded in returned session observations. No source, receipt, accepted-context, filesystem or SQLite route exists. Both valid and error responses have bounded explicit lengths and close the connection. The client rejects redirects, compression, chunking, duplicate headers and extra/truncated body bytes.

Run the service through the selected isolated local interpreter with `-B -E -s -S`, `--view`, `--port`, and a new `--ready` path. The CLI enforces all four startup flags: no bytecode writing, ignored Python environment settings, no user site, and no site initialization. Port 0 is allowed only for service-side OS selection; its actual literal loopback port is written to the readiness file. Readiness is published as a complete fsynced sibling temporary file using an atomic non-overwriting hard link, then that temporary link is removed; the selected local filesystem must support hard links. Client ports must be 1–65535. A caller must map a configured peer alias to that port; a wire response cannot select another endpoint.

## Bytes and checking boundaries

Catalog entries have exactly `descriptor_id`, `root`, `manifest_sha256`, `bundle_sha256`, `bundle_bytes`, `formal_metadata`. The formal metadata field set matches the current receiver's nine projected fields. Only shallow internal correspondence is checked here; coherent lies still require local metadata rederivation. `build_view` verifies the offered manifest pin and root/foundation binding, but publication authority belongs exclusively to its local caller.

The bundle is `DTMKN-PEER-BUNDLE-1\n`, a big-endian four-byte manifest length, exact manifest JSON, then one big-endian eight-byte length and canonical object payload for each manifest ID, followed by EOF. There are no member filenames. Object destinations are derived as the existing `CBOR(typedID).hex() + '.cbor'` beneath a newly created local directory. Reparse points/symlinks in existing local path ancestry refuse; owner-controlled filesystem quiescence remains a premise, not hostile race isolation.

Framing/size checks occur while receiving. Whole-bundle and manifest hashes are checked before object CBOR/CID validation, so unchanged advertised digest plus mutated object yields `BUNDLE_DIGEST_MISMATCH`; a coherently repinned transfer containing an unchanged object ID yields `OBJECT_ID_MISMATCH`. The independent canonical scanner accepts only shortest unsigned integers, bytes and definite arrays, with full consumption, physical nesting and item bounds. It does not validate mathematical object semantics. The returned basis is explicitly `TRANSPORT_AND_OBJECT_IDENTITIES_ONLY`.

Root's required sequence is: reserve quota and new local staging; fetch under supervision; run full `Checker.offer`/closure checks; compare the complete rederived descriptor/formal metadata to `advertised_metadata`; resolve exact duplicates to the existing owned offer; commit candidate visibility atomically; later run fresh `admit` on a receiver-selected context. A returned directory or success flag from these helpers is never sufficient for registry or head advancement.

## Fixed bounds and external obligations

Catalog 64 KiB/32 entries; manifest 1 MiB; at most 8,192 objects; each and aggregate canonical payload at most 16 MiB; framed bundle 18 MiB; retained view bundles 64 MiB. JSON nesting is 64 and parsed value count 262,144. CBOR physical nesting follows the existing 64-depth envelope; scanner item bound is 8,388,608. Unsupported object kind/schema pairs refuse.

HTTP first line 2 KiB and total headers 8 KiB; one synchronous connection plus backlog one; connect timeout two seconds; idle IO five seconds; selected transfer thirty seconds. Default service session stops at 128 accepted connections, 256 MiB charged sends, 600 wall seconds or 120 observed process CPU seconds. Owner-only keyword arguments can make request/byte/wall limits stricter. No automatic retries. Failed/partial sends consume their full reserved allowance; `completed_send_bytes` counts completed send calls and is a lower bound if one fails, while `charged_send_bytes` is the authoritative conservative quota counter. Received bytes are counted even for malformed headers. A stopped session does not automatically restart or reset its grant.

These counters/timeouts do not constitute a hard OS resource sandbox. Root must supervise the service's process tree with the prospectively chosen 256 MiB memory/CPU/wall bounds, and receiving parsing/rederivation with 1,024 MiB and 120 CPU/wall seconds. `make_bundle` materializes a bounded bundle in memory; it is not a zero-copy streaming exporter. Caller reserves at least the selected complete 64 MiB transfer/staging allowance for incoming bytes, checked copy and retained diagnostics. Quota reservation, worker quiescence, cleanup, durable request replay, offer deduplication, context retention and commit recovery belong to the owner integration, not these helpers. A missing lock or failed call is not proof that a worker stopped.

Plain loopback HTTP authenticates no peer and provides no confidentiality. It is only the same-host test profile. Public/non-loopback service, remote source execution and acceptance-credential transfer are unsupported.

## Independent finite tests

`tests/test_peer_wire.py` builds small synthetic byte fixtures using its own CID/framing/filename calculations. Their payloads intentionally are not valid mathematics; transport success must remain explicitly nonaccepting. Cases include strict schemas, wrong foundations, quotas before reads, malformed framing, digest-vs-object-ID separation, noncanonical CBOR, filename injection, no overwrite, incomplete views, advertised metadata limits and an actual bounded loopback catalog/acquisition/private-route cycle. Separate one-response loopback servers exercise length, redirect and chunking refusals.

Root alone runs tests after source review, using the selected interpreter's `-B -E -s -S` profile and a separately bounded native-free supervisor. Set `DTMKN_TEST_ROOT` to an existing absolute owner-selected run directory before launch. Qualification fails if this variable is absent, relative, nonexistent or has a symlink/reparse-point ancestor. Each test exclusively creates a new child with `mkdtemp`, records its case name, and retains every fixture and partial transfer there. There is no `TemporaryDirectory` destructor, recursive cleanup or fallback to the global temporary directory; root records the encompassing run directory. `-E` does not suppress this non-`PYTHON*` application variable.

The tests do not import acceptance machinery or mock a successful proof check. Passing them would establish only the exercised transport behavior; the separately audited two-installation reciprocal/offline scenario remains required.
