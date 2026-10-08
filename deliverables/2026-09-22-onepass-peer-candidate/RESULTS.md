# One-pass peer candidate: supported result and limits

2026-09-22. Selected as the latest **locally qualified source candidate** after separate protocol, native operational, native canonical and product-hosting outcome audits. This is not an externally published release or qualification of independent-host operation.

## What changed

The ordinary owner service authenticates its selected immutable wire-v2 view once per finite session, then passes that authenticated mapping in-process to the transport loop. It still verifies every selected publication or replica-custody row before readiness and rehashes each requested page or bundle before sending it. The standalone service entry point still validates its own view. There is no persistent trust cache or receiver-supplied acceptance token.

Relative to the [paged predecessor](../2026-09-22-paged-peer-candidate/RESULTS.md), only `py/peer_service.py`, `py/service_worker.py` and eight packaged Markdown documents changed. The Lean checker, canonical codec, assets, database schema, wire routes and mathematical acceptance policy did not change. New installations and state are required; do not overwrite a used node.

## Evidence

| Gate | Observed result | Independent review |
| --- | --- | --- |
| Native-free differential | Eight cases and ten owner-service sessions per variant passed. Complete view loads across the fixed cases: predecessor 20, candidate 10; loaded file bytes: 2,728,212 versus 1,364,106. Transfer bytes and responses matched. | [Protocol review](../../experiments/peer-service-onepass/PROTOCOL-REVIEW.md) |
| Fresh genuine Lean exchange | One 20-step chain passed: A found the genuine historical result at page-two ordinal 33 after 32 inert decoys, freshly admitted it, submitted and published a distinct definition whose actual body applies the received proof; B independently acquired and freshly admitted that dependent closure. | [Operational audit](../../experiments/peer-service-onepass/NATIVE-OPERATIONAL-AUDIT.md) and [canonical audit](../../experiments/peer-service-onepass/NATIVE-CANONICAL-AUDIT.md) |
| Ordinary durable hosting | Two consecutive `manage.py host` slots served the exact catalog, three pages and last bundle of a synthetic 65-entry view. Both reached readiness within the frozen eight-second deadline, stopped naturally after five requests, reconciled their full durable grant charges and returned identical exhausted-grant CLI bytes on replay. | [Hosting outcome audit](../../experiments/peer-service-onepass/HOSTING-OUTCOME-AUDIT.md) |

The native run took 606.786 coordinator wall seconds against 1,200 and 425.546875 inclusive disjoint outer-Job CPU seconds against 800, plus 54.140625 separately measured coordinator CPU seconds. Its final retained endpoint has 892 files, 1,120 entries and 96,762,611 bytes. Every native stage, outer/public receipt, source pin and retained census file passed the stated independent checks. The two hosting slots reached readiness in 0.690 and 0.560 seconds; each completed 66,141 charged send bytes and retained 12,782 and 12,777 bytes of service evidence. The complete hosting-gate run, including fixture preparation, supervision, replay and checks, took 25.470 seconds. These are observations under different workloads and are **not** an end-to-end speedup or regression estimate against the predecessor.

The native-free comparison additionally tested changed-file and authority refusals and identical wire behavior. The 65-entry hosting view consists of inert test fixtures directly marked as publications in a fresh test-only store, not 65 genuinely published mathematical results. The actual A-to-B return leg used ordinary product publication, exposure, service, acquisition and fresh Lean admission. Discovery and transfer remained nonaccepting throughout.

## Exact delivered identity and deployment boundary

The [source archive](math-commons-source.zip) has 112 payloads plus `SOURCE-MANIFEST.json`. Archive SHA-256: `6d406e1bd0f9d2e2c5757d99b448ae02e105236a5965a9de7a307f43fe6663c3`. Manifest SHA-256: `1f3c345569bcb511fea67d62d42d457824d10567b08e926af0aa3b9f5779f9a6`. Independent package review checked every extracted member. The packager's earlier `DEVELOPMENT_SOURCE_PACKAGED_UNQUALIFIED` marker is retained; this external statement and linked audits state the subsequent qualification, without rewriting frozen machine evidence.

The supported local profile remains Windows x64 on local NTFS, Python 3.14.6/SQLite 3.50.4, and a complete Lean 4.34.0 Windows runtime. Runtime binaries are not bundled. Use the archive's `QUICKSTART.md`, `AGENT-QUICKSTART.md`, `API.md`, `HOSTING.md`, `PEER.md` and `RECOVERY.md`. Direct service is literal loopback; an authenticated SSH forwarding recipe is documented but has not been tested on an independent host. There is no public Internet service, in-place schema migration, global directory or mandatory central server.

The hosting audit could inspect the final journal, both receipts and identical replay output; its before/after journal equality also relies on a checked runner assertion because no separate pre-replay tree snapshot was retained. The 1 MiB per-slot evidence allowance is durable accounting, not a hard filesystem quota. All tests assume owner-stable local files and the declared runtime/OS trust boundary; this is not a general implementation soundness proof.

The current result does not establish mathematical novelty, autonomous theorem selection, useful or exponential knowledge growth, affordable operation at arbitrary corpus size, long-term availability or independent-host deployment. Full-workflow cost and demand-driven useful reuse are the next central local discriminators. A second physical machine is unavailable; licensing is undecided; nothing was published externally. The overall project goal remains active.
